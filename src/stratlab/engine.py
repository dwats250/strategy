"""Execution layer: Backtesting.py on 1-minute bars, signals from completed higher-timeframe bars.

Timeline contract (tested in tests/test_engine_behavior.py):

* Strategies decide on COMPLETED signal bars (e.g. 3m or 5m). A signal bar's values
  are published on the execution (1m) bar that is the last existing minute of that
  bucket; Backtesting.py calls `next()` "a moment before" that minute closes, at
  which point the 1m close equals the signal-bar close. Orders placed then fill at
  the NEXT 1m bar's open, which starts at or after the signal bar's end. No order can
  fill inside the bar that generated it.
* Protective stops and targets are evaluated on 1-minute OHLC, starting with the
  entry minute itself (the entry fills at that minute's open, so the whole minute is
  after the entry).
* Session flatten: on each session the engine marks a decision minute so that the
  closing market order fills at the open of the first minute at or after
  `close - flatten_minutes` (calendar close, so early closes are handled). From that
  decision minute to the session end, entries are blocked and pending orders cancelled.
  Positions therefore never carry overnight.
* Costs: a per-share amount per side (commission + slippage allowance) charged as
  cash through Backtesting.py's commission hook. Fill prices themselves are
  unadjusted; a stop gapped through fills at the (worse) open.
"""

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass, field

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

from .data.sessions import ET


@dataclass(frozen=True)
class ExecutionConfig:
    cash: float = 100_000.0
    commission_per_share: float = 0.0035
    slippage_per_share: float = 0.01
    margin: float = 1.0
    flatten_minutes: int = 5

    @property
    def cost_per_share(self) -> float:
        return self.commission_per_share + self.slippage_per_share

    def to_dict(self) -> dict:
        d = asdict(self)
        d["cost_per_share_per_side"] = self.cost_per_share
        return d


def per_share_cost(cost: float):
    """Backtesting.py commission hook: called once per fill with (size, price)."""
    def _fn(size, price):
        return abs(size) * cost
    _fn.__name__ = f"per_share_{cost:.4f}"
    return _fn


# ----------------------------------------------------------------------------------
# Frame preparation
# ----------------------------------------------------------------------------------

def et_minute_of_day(ts: pd.DatetimeIndex) -> np.ndarray:
    et = ts.tz_convert(ET)
    return (et.hour * 60 + et.minute).to_numpy()


def build_execution_frame(rth_1m: pd.DataFrame, signal_bars: pd.DataFrame,
                          features: pd.DataFrame, sessions: pd.DataFrame,
                          signal_minutes: int, flatten_minutes: int) -> pd.DataFrame:
    """Merge completed-signal-bar features onto the 1-minute execution timeline.

    `features` is indexed like `signal_bars` (bucket start). Each feature column is
    published on the bucket's `last_1m` minute and forward-filled; `sig_new` marks the
    publish minute. Feature names must not collide with OHLCV.
    """
    f = features.copy()
    f["sig_start_ns"] = signal_bars.index.as_unit("ns").asi8.astype("float64")
    end = signal_bars.index + pd.Timedelta(minutes=signal_minutes)
    f["sig_end_et_min"] = et_minute_of_day(pd.DatetimeIndex(end)).astype("float64")
    f["sig_complete"] = signal_bars["complete"].astype("float64").to_numpy()
    publish_at = pd.DatetimeIndex(signal_bars["last_1m"]).as_unit("ns")
    f.index = publish_at
    if f.index.has_duplicates:
        raise ValueError("two signal bars publish on the same minute")

    ex = rth_1m[["Open", "High", "Low", "Close", "Volume", "session"]].copy()
    ex.index = ex.index.as_unit("ns")
    missing = f.index.difference(ex.index)
    if len(missing):
        raise ValueError(f"{len(missing)} publish minutes absent from execution frame")
    joined = ex.join(f, how="left")
    joined["sig_new"] = joined["sig_start_ns"].notna().astype("float64")
    fcols = list(f.columns)
    # Forward-fill within session only: a value never leaks across the overnight gap.
    joined[fcols] = joined.groupby("session")[fcols].ffill()

    # Session flatten markers.
    flat = np.zeros(len(joined))
    sess_codes, sess_index = pd.factorize(joined["session"])
    ts_ns = joined.index.asi8
    closes = pd.DatetimeIndex(sessions.loc[sess_index, "close"]).as_unit("ns").asi8
    cutoff_by_sess = closes - flatten_minutes * 60_000_000_000
    starts = np.r_[0, np.flatnonzero(np.diff(sess_codes)) + 1]
    ends = np.r_[starts[1:], len(joined)]
    fallback = np.zeros(len(joined))
    for k, (s, e) in enumerate(zip(starts, ends)):
        cut = cutoff_by_sess[sess_codes[s]]
        rel = np.searchsorted(ts_ns[s:e], cut, side="left")
        if rel == e - s:
            # No minute at/after the cutoff exists in this session's data.
            if k == len(starts) - 1:
                # Data ends mid-session: flattening early would use knowledge that no
                # more data is coming. Leave any position open; it is reported as
                # `open_at_end`, marked to the final close.
                continue
            # Interior session missing its closing minutes: flatten at the last
            # available minute so nothing carries overnight, and flag it.
            fallback[s:e] = 1.0
        fill_pos = s + min(rel, e - s - 1)
        decision = max(fill_pos - 1, s)
        flat[decision:e] = 1.0
    joined["flatten"] = flat
    joined["flatten_fallback"] = fallback
    joined["session_code"] = sess_codes.astype("float64")
    joined = joined.drop(columns=["session"])
    joined.index = joined.index.tz_convert(None)  # Backtesting.py works on naive UTC
    return joined


# ----------------------------------------------------------------------------------
# Strategy base
# ----------------------------------------------------------------------------------

class LabStrategy(Strategy):
    """Base class: session flatten, signal-bar gating, trade bookkeeping.

    Subclasses implement `on_signal_bar()` and read published features through
    `self.f(name)` (current completed signal bar). Entries go through `self.enter()`
    and discretionary exits through `self.exit_all(reason)` so every trade carries its
    initial stop (for R) and exit reason.
    """

    notional_fraction = 0.999

    def init(self):
        self.trade_meta: dict[int, dict] = {}
        self.exit_reasons: dict[int, str] = {}
        self._next_tag = 0
        self._pending_meta: dict[int, dict] = {}

    # -- helpers -------------------------------------------------------------------
    def f(self, name: str) -> float:
        return getattr(self.data, name)[-1]

    def now(self) -> pd.Timestamp:
        return self.data.index[-1]

    def signal_bar_complete(self) -> bool:
        """False when the signal bar is missing constituent minutes (e.g. a masked print).
        Strategies take no NEW entries on such bars; exits are still evaluated."""
        return self.f("sig_complete") == 1.0

    def has_pending_entry(self) -> bool:
        return any(not o.is_contingent for o in self.orders)

    def enter(self, side: int, stop: float | None, target: float | None = None,
              reason: str = "signal", **meta) -> None:
        tag = self._next_tag
        self._next_tag += 1
        info = dict(side=side, initial_stop=stop, target=target, entry_reason=reason,
                    decision_time=str(self.now()), signal_close=float(self.data.Close[-1]),
                    signal_start=pd.Timestamp(int(self.f("sig_start_ns"))).isoformat())
        info.update(meta)
        self.trade_meta[tag] = info
        kw = dict(size=self.notional_fraction, sl=stop, tp=target, tag=tag)
        (self.buy if side > 0 else self.sell)(**kw)

    def exit_all(self, reason: str) -> None:
        for t in self.trades:
            # The market exit fills at the next open, before any later intrabar
            # stop/target touch. Backtesting.py 0.6.6 already orders it that way
            # (tested); detaching the stop/target makes the intent explicit.
            t.sl = None
            t.tp = None
            self.exit_reasons[t.tag] = reason
            t.close()

    # -- main loop -------------------------------------------------------------------
    def next(self):
        if self.data.flatten[-1] == 1.0:
            for o in list(self.orders):
                if not o.is_contingent:
                    o.cancel()
            if self.trades:
                self.exit_all("session_flatten")
            return
        if self.data.sig_new[-1] != 1.0:
            return
        self.on_signal_bar()

    def on_signal_bar(self):  # pragma: no cover - abstract
        raise NotImplementedError


# ----------------------------------------------------------------------------------
# Running and extracting results
# ----------------------------------------------------------------------------------

@dataclass
class RunOutput:
    trades: pd.DataFrame
    equity: pd.DataFrame          # per execution bar (UTC index)
    session_equity: pd.Series     # equity at each session's last bar
    library_stats: dict
    warnings: list = field(default_factory=list)


def run_backtest(strategy_cls, frame: pd.DataFrame, cfg: ExecutionConfig,
                 params: dict | None = None) -> RunOutput:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        bt = Backtest(frame, strategy_cls, cash=cfg.cash,
                      commission=per_share_cost(cfg.cost_per_share), margin=cfg.margin,
                      trade_on_close=False, hedging=False, exclusive_orders=False,
                      finalize_trades=False)
        stats = bt.run(**(params or {}))
    strat = stats._strategy
    eq = stats._equity_curve.copy()
    eq.index = pd.DatetimeIndex(eq.index).tz_localize("UTC")
    trades = _trade_table(stats._trades, strat, frame)
    open_rows = _open_trade_rows(strat, frame)
    if open_rows:
        trades = pd.concat([trades, pd.DataFrame(open_rows)], ignore_index=True)
    trades = add_risk_columns(trades, eq["Equity"].to_numpy(), cfg.cash)
    sess = frame["session_code"]
    last_bar = ~sess.duplicated(keep="last").to_numpy()
    session_equity = pd.Series(eq["Equity"].to_numpy()[last_bar],
                               index=pd.DatetimeIndex(frame.index[last_bar]).tz_localize("UTC")
                               .tz_convert(ET).normalize().date, name="equity")
    lib = {k: (v.isoformat() if isinstance(v, pd.Timestamp) else
               str(v) if isinstance(v, pd.Timedelta) else
               (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else None))
           for k, v in stats.items() if not k.startswith("_")}
    msgs = sorted({str(w.message)[:200] for w in caught
                   if "remain open at the end of backtest" not in str(w.message)})
    return RunOutput(trades, eq, session_equity, lib, msgs)


def add_risk_columns(trades: pd.DataFrame, equity: np.ndarray, cash: float) -> pd.DataFrame:
    """Per-trade initial exposure and risk, measured against account equity just
    before the entry minute (the previous minute's mark-to-market close).

    initial_risk_usd         shares x |fill - initial stop|  (NaN when R is undefined)
    initial_risk_pct_equity  that amount / equity before entry
    notional_pct_equity      shares x fill / equity before entry (~0.999 by sizing)
    initial_reward_risk      side x (target - fill) / |fill - stop|  (targets only); the
                             target is placed from the signal close, so this is the
                             ACTUAL reward/risk at the fill, not the nominal multiple
    """
    t = trades.copy()
    if t.empty:
        for c in ("equity_before", "initial_risk_usd", "initial_risk_pct_equity",
                  "notional_pct_equity", "initial_reward_risk"):
            t[c] = pd.Series(dtype=float)
        return t
    eb = t["entry_bar"].astype(int).to_numpy()
    before = np.where(eb > 0, equity[np.clip(eb - 1, 0, len(equity) - 1)], cash)
    sign = np.where(t["side"].to_numpy() == "long", 1.0, -1.0)
    t["equity_before"] = before
    t["initial_risk_usd"] = t["size"].astype(float) * t["risk_per_share"].astype(float)
    t["initial_risk_pct_equity"] = t["initial_risk_usd"] / before
    t["notional_pct_equity"] = t["size"].astype(float) * t["entry_price"].astype(float) / before
    tgt = pd.to_numeric(t["target"], errors="coerce")
    t["initial_reward_risk"] = sign * (tgt - t["entry_price"]) / t["risk_per_share"]
    return t


def _risk(side: int, entry: float, stop) -> float:
    """Initial risk per share. NaN when the stop is missing or on the wrong side of the
    actual fill (the entry minute opened beyond the stop): such a trade never had a
    defined risk, so it gets no R multiple and exit_reason `stop_beyond_fill`."""
    if stop is None or (isinstance(stop, float) and np.isnan(stop)):
        return np.nan
    d = side * (entry - stop)
    return float(d) if d > 0 else np.nan


def _open_trade_rows(strat: LabStrategy, frame: pd.DataFrame) -> list[dict]:
    """Positions still open when the data ends, marked to the final close (not closed).

    Backtesting.py's own `finalize_trades=True` would close them at the last bar's
    OPEN; the lab instead reports them as open and lets the equity curve carry the
    mark-to-market at the last close.
    """
    rows = []
    last_close = float(frame["Close"].iloc[-1])
    for t in strat.trades:
        meta = strat.trade_meta.get(t.tag, {})
        side = 1 if t.size > 0 else -1
        size = abs(int(t.size))
        stop = meta.get("initial_stop")
        risk = _risk(side, t.entry_price, stop)
        entry_cost = float(strat._broker._commission(t.size, t.entry_price))
        unreal = side * (last_close - t.entry_price) * size - entry_cost
        rows.append(dict(
            trade_id=t.tag, side="long" if side > 0 else "short", size=size,
            entry_time=pd.Timestamp(t.entry_time).tz_localize("UTC"), exit_time=pd.NaT,
            entry_price=float(t.entry_price), exit_price=last_close, initial_stop=stop,
            target=meta.get("target"), risk_per_share=risk, pnl=unreal, costs=entry_cost,
            gross_pnl=side * (last_close - t.entry_price) * size,
            return_pct=side * (last_close / t.entry_price - 1),
            r_multiple=(unreal / size) / risk if risk and risk > 0 else np.nan,
            r_gross=side * (last_close - t.entry_price) / risk if risk and risk > 0 else np.nan,
            exit_reason="open_at_end", entry_reason=meta.get("entry_reason"),
            entry_bar=int(t.entry_bar), bars_held=int(len(frame) - 1 - t.entry_bar),
            minutes_spanned=int(len(frame) - t.entry_bar),
            signal_start=meta.get("signal_start"), decision_time=meta.get("decision_time"),
        ))
    return rows


def _trade_table(t: pd.DataFrame, strat: LabStrategy, frame: pd.DataFrame) -> pd.DataFrame:
    if t.empty:
        cols = ["trade_id", "side", "size", "entry_time", "exit_time", "entry_price", "exit_price",
                "initial_stop", "target", "risk_per_share", "pnl", "costs", "gross_pnl",
                "return_pct", "r_multiple", "r_gross", "exit_reason", "entry_reason",
                "entry_bar", "bars_held", "minutes_spanned", "signal_start", "decision_time"]
        return pd.DataFrame(columns=cols)
    rows = []
    for _, r in t.iterrows():
        tag = int(r["Tag"])
        meta = strat.trade_meta.get(tag, {})
        side = 1 if r["Size"] > 0 else -1
        size = abs(int(r["Size"]))
        entry, exit_ = float(r["EntryPrice"]), float(r["ExitPrice"])
        stop = meta.get("initial_stop")
        target = meta.get("target")
        risk = _risk(side, entry, stop)
        gross = side * (exit_ - entry) * size
        costs = float(r["Commission"])
        pnl = float(r["PnL"])
        reason = strat.exit_reasons.get(tag)
        if reason is None:
            sl, tp = r.get("SL"), r.get("TP")
            if pd.notna(sl) and ((side > 0 and exit_ <= sl + 1e-9) or (side < 0 and exit_ >= sl - 1e-9)):
                reason = "stop"
            elif pd.notna(tp) and ((side > 0 and exit_ >= tp - 1e-9) or (side < 0 and exit_ <= tp + 1e-9)):
                reason = "target"
            else:
                reason = "unclassified"   # should not occur; surfaced, never hidden
        if stop is not None and np.isnan(risk):
            reason = "stop_beyond_fill" if reason == "stop" else reason
        rows.append(dict(
            trade_id=tag, side="long" if side > 0 else "short", size=size,
            entry_time=pd.Timestamp(r["EntryTime"]).tz_localize("UTC"),
            exit_time=pd.Timestamp(r["ExitTime"]).tz_localize("UTC"),
            entry_price=entry, exit_price=exit_, initial_stop=stop, target=target,
            risk_per_share=risk, pnl=pnl, costs=costs, gross_pnl=gross,
            return_pct=float(r["ReturnPct"]),
            r_multiple=(pnl / size) / risk if risk and risk > 0 else np.nan,
            r_gross=(side * (exit_ - entry)) / risk if risk and risk > 0 else np.nan,
            exit_reason=reason, entry_reason=meta.get("entry_reason"),
            entry_bar=int(r["EntryBar"]), bars_held=int(r["ExitBar"] - r["EntryBar"]),
            minutes_spanned=int(r["ExitBar"] - r["EntryBar"]) + 1,
            signal_start=meta.get("signal_start"), decision_time=meta.get("decision_time"),
        ))
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
