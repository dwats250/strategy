#!/usr/bin/env python3
"""FastAlpha offline execution engine — v1.0 · 2026-08-26.

The smallest deterministic local simulator of the exact FastAlpha family
(scripts/VWAP_Continuation_FastAlpha_v0.pine and its V1 EMA-10/22 perturbation).
It is NOT a generic backtester: it reproduces only the v0 mechanics, bar by bar,
over the RTH 5-minute bars reconstructed by `parity_foundation` from the verified
SPY 1-minute corpus.

INDICATOR SEMANTICS ARE NOT RE-IMPLEMENTED HERE. All per-bar state (session
VWAP, EMA fast/slow, ATR14, directional state, red/green, entry window, the
flat-agnostic long/short candidates) comes from `parity_foundation.compute_features`
— the single source of truth for the feature seam (PARITY_GATES.md Gate 2). This
module adds ONLY the execution layer Pine performs and `parity_foundation`
deliberately omits: order placement, fills, the ATR stop, the thesis/EOD exits,
the `flat` position gate, and per-trade P/L.

================================================================================
BROKER-EMULATOR ASSUMPTIONS (stated, not tuned)
================================================================================
The charge requires the smallest documented deterministic assumption justified
by Pine/TradingView semantics and the R0 evidence, stated explicitly, with
residual mismatches CLASSIFIED rather than tuned away. These are fixed a priori
and never adjusted against P/L:

  A. Bar model. Pine strategy runs once per bar at the close
     (calc_on_every_tick=false). Orders placed in a bar's body are processed
     starting at the NEXT bar (process_orders_on_close=false):
       * market orders (entries, thesis closes) fill at the next bar's OPEN;
       * the attached ATR stop (strategy.exit loss=) is a resting stop checked
         intrabar against every subsequent bar, beginning with the SAME bar the
         entry fills on (entry and stop-out can occur on one bar).
  B. Within-bar processing order: (1) fill the pending market order at this
     bar's open; (2) if still in a position, test the resting stop intrabar
     against this bar; (3) at the close, evaluate EOD, then thesis failure, then
     (only if flat) a new entry signal. A pending thesis close therefore fills
     at the open BEFORE the stop can act that bar, so a thesis exit pre-empts the
     stop when both are live on the same bar — a direct reading of "market fills
     at open, stop rests intrabar."
  C. mintick = 0.01 for SPY. Verified from the R0 export: every price in the
     preserved trade list lies on a 0.01 grid. `atrStopTicks =
     max(1, round(atr14 / mintick))`, frozen on the signal bar.
  D. Slippage = 1 tick, applied ADVERSELY to every market and stop fill (the
     documented TradingView behaviour: slippage moves market and stop fills by
     the configured ticks against the position; limit orders are unaffected —
     this strategy uses none):
       long  entry (buy)          fill = open  + 1 tick
       short entry (sell)         fill = open  - 1 tick
       long  stop / close (sell)  fill = level - 1 tick
       short stop / close (buy)   fill = level + 1 tick
       EOD long  (sell at close)  fill = close - 1 tick
       EOD short (buy  at close)  fill = close + 1 tick
  E. Stop trigger + fill price. Long stop at S triggers when bar low <= S; it
     fills at S unless the bar OPENED at/below S (a gap through the stop), in
     which case it fills at the open. Short stop mirrored (high >= S; open >= S
     gap). Slippage per (D) is then applied. On the entry bar the entry fills at
     open and S is strictly inside the bar, so a same-bar stop fills at S (never
     the gap branch).
  F. EOD flatten fires only on a bar whose START hm == 1550 while a position is
     open, closing at that bar's close with `immediately=true`. On shortened
     sessions no 15:50 bar exists, so EOD never fires and the position persists
     into later bars exactly as the source dictates (an "early-close/session"
     effect, not special-cased).
  G. Backtest range. Orders are entered only on signal bars with session_date
     within the development window; the simulation is run over bars up to and
     including DEV_END so an end-of-window position is EOD-flattened on the final
     day, matching a TradingView backtest whose range ends at DEV_END. Indicators
     warm up from the corpus start (2024-09-03), which equals the development
     window start — no pre-window history exists to diverge over.

None of the above is fitted. Where they leave a residual against R0, the
calibration script classifies it; it does not adjust these rules.
"""

import parity_foundation as pf

MINTICK = 0.01          # SPY; assumption C (verified from R0 export price grid)
SLIPPAGE_TICKS = 1      # strategy() slippage; assumption D
SLIP = SLIPPAGE_TICKS * MINTICK
DEV_START = "2024-09-03"
DEV_END = "2025-12-31"
EOD_BAR_HM = pf.EOD_BAR_HM   # 1550


def compute_feature_rows(ema_fast, ema_slow, drop_t_ms=None):
    """Feature rows for a given EMA pair, via parity_foundation (indicator
    seam). Temporarily rebinds the module's EMA-length globals — the exact,
    already-used pattern from v1_ema1022_diff_proof.py — and restores them, so
    indicator semantics stay owned by one module. Returns the full-corpus rows;
    `simulate` applies the development window.

    `drop_t_ms` (optional): a set of 1-minute bar `t_ms` timestamps to REMOVE
    from the RTH stream before 5m aggregation. This is how the corpus-integrity
    research-clean view is applied — a pure, reversible filter that never mutates
    the corpus. Default None = raw corpus."""
    save_fast, save_slow = pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN
    try:
        pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN = ema_fast, ema_slow
        rth = pf.load_corpus_rth()
        if drop_t_ms:
            drop = {str(x) for x in drop_t_ms}
            rth = [r for r in rth if r["t_ms"] not in drop]
        rows = pf.compute_features(pf.build_5m_bars(rth))
    finally:
        pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN = save_fast, save_slow
    return rows


def _hhmm(et_start_iso):
    """'2024-09-03T11:10:00' -> '2024-09-03 11:10' (R0 trade-list format)."""
    d, t = et_start_iso.split("T")
    return f"{d} {t[:5]}"


def simulate(rows, dev_start=DEV_START, dev_end=DEV_END, atr_stop_mult=1.0,
             enable_longs=True, enable_shorts=True, signal_mode="vdc"):
    """Run the FastAlpha execution model over development-window feature rows.

    Returns a list of closed-trade dicts, in entry order. Deterministic: pure
    float arithmetic over a fixed bar sequence, no RNG, no wall-clock.

    `atr_stop_mult` scales ONLY the initial ATR stop distance (the source's
    ATR_STOP_MULT; v0 = 1.0). `enable_longs`/`enable_shorts` gate ENTRY PERMISSION
    by side (default both True = symmetric V0); disabling a side changes flat-state
    occupancy and therefore the whole path — it is NOT the same as filtering that
    side out of the symmetric output. Long/short thresholds and every other
    semantic are unchanged. Defaults reproduce V0 exactly.

    `signal_mode` selects the ENTRY SIGNAL rule only; execution (fills, ATR stop,
    thesis/EOD exits, the flat gate, P/L) is identical in every mode.
      * "vdc"  (default) — the frozen V0 rule: enter on the flat-agnostic
        `long_candidate`/`short_candidate` precomputed by parity_foundation
        (`inEntryWindow and bullishState and redBar`, mirrored). Byte-identical to
        every prior result.
      * "fpc"  — FIRST PULLBACK CONTINUATION (family FPC, hypothesis FPC-0): on a
        FRESH bullish regime (`bullish_state` true on this bar, false on the prior
        bar) arm ONE long opportunity; do NOT enter on the fresh bar itself; while
        that regime stays continuously true, the FIRST subsequent red bar
        (`red_bar`) inside the entry window taken while flat is the only permitted
        long entry, after which the side disarms (one entry per continuous regime).
        A regime turning false disarms; a later false->true transition re-arms.
        Short is the exact mirror (fresh bearish regime, first green bar). This
        state is execution-dependent ("while flat"), so it lives here, not in the
        flat-agnostic feature seam. FPC reads only precomputed parity_foundation
        fields (`bullish_state`, `bearish_state`, `red_bar`, `green_bar`,
        `in_entry_window`); it re-implements no indicator.
    """
    bars = [r for r in rows if dev_start <= r["session_date"] <= dev_end]

    pos = 0                     # 0 flat, +1 long, -1 short
    entry_price = None
    stop_price = None
    risk_points = None          # 1R: frozen initial entry-to-stop distance (pts)
    entry_bar = None            # fill-bar 'YYYY-MM-DD HH:MM'
    signal_bar = None           # signal-bar 'YYYY-MM-DD HH:MM'
    entry_idx = None
    pending = None              # (kind, atr_ticks|reason, signal_bar)
    trades = []

    # FPC (signal_mode="fpc") arm-state — inert in "vdc" mode
    prev_bullish = False
    prev_bearish = False
    armed_long = False
    armed_short = False

    def close_trade(exit_bar, exit_price, reason, exit_idx):
        nonlocal pos, entry_price, stop_price, risk_points
        nonlocal entry_bar, signal_bar, entry_idx
        pnl = (exit_price - entry_price) if pos > 0 else (entry_price - exit_price)
        trades.append({
            "side": "long" if pos > 0 else "short",
            "signal_bar": signal_bar,
            "entry_bar": entry_bar,
            "entry_price": round(entry_price, 4),
            "stop_price": round(stop_price, 4),
            "risk_points": round(risk_points, 4),   # 1R denominator (frozen)
            "exit_bar": exit_bar,
            "exit_price": round(exit_price, 4),
            "exit_reason": reason,
            "pnl": round(pnl, 4),
            "pnl_r": round(pnl / risk_points, 6) if risk_points else None,
            "bars_held": exit_idx - entry_idx,
        })
        pos = 0
        entry_price = stop_price = risk_points = None
        entry_bar = signal_bar = entry_idx = None

    for i, b in enumerate(bars):
        o, h, l, c = b["o"], b["h"], b["l"], b["c"]
        vwap, atr14 = b["session_vwap"], b["atr14"]
        et = _hhmm(b["et_start"])

        # ---- 0. FPC regime arm-state (advanced every bar, before any continue) --
        bull = bear = fresh_bull = fresh_bear = False
        if signal_mode == "fpc":
            bull = bool(b.get("bullish_state"))
            bear = bool(b.get("bearish_state"))
            fresh_bull = bull and not prev_bullish
            fresh_bear = bear and not prev_bearish
            prev_bullish, prev_bearish = bull, bear      # advance for the next bar
            if not bull:
                armed_long = False                       # regime ended -> disarm
            elif fresh_bull:
                armed_long = True                        # fresh regime -> arm one
            if not bear:
                armed_short = False
            elif fresh_bear:
                armed_short = True

        # ---- 1. fill the pending market order at THIS bar's open ----
        if pending is not None:
            kind, payload, sig = pending
            pending = None
            if kind == "entry_long":
                pos = 1
                entry_price = o + SLIP
                risk_points = payload * MINTICK
                stop_price = entry_price - risk_points
                entry_bar, signal_bar, entry_idx = et, sig, i
            elif kind == "entry_short":
                pos = -1
                entry_price = o - SLIP
                risk_points = payload * MINTICK
                stop_price = entry_price + risk_points
                entry_bar, signal_bar, entry_idx = et, sig, i
            elif kind == "close_long":
                close_trade(et, o - SLIP, payload, i)
            elif kind == "close_short":
                close_trade(et, o + SLIP, payload, i)

        # ---- 2. resting ATR stop, intrabar against THIS bar ----
        if pos > 0 and l <= stop_price:
            raw = stop_price if o > stop_price else o     # gap-through fills at open
            close_trade(et, raw - SLIP, "Long ATR Stop", i)
        elif pos < 0 and h >= stop_price:
            raw = stop_price if o < stop_price else o
            close_trade(et, raw + SLIP, "Short ATR Stop", i)

        # ---- 3. at the close: EOD, then thesis, then (if flat) a new entry ----
        if pos != 0 and b["hm"] == EOD_BAR_HM:
            close_trade(et, (c - SLIP) if pos > 0 else (c + SLIP), "EOD", i)
            continue                                      # 1550 is not an entry bar
        if pos > 0 and vwap is not None and c < vwap:
            pending = ("close_long", "VWAP Failure", signal_bar)
            continue
        if pos < 0 and vwap is not None and c > vwap:
            pending = ("close_short", "VWAP Failure", signal_bar)
            continue
        if pos == 0 and atr14 is not None:              # pos==0 IS the 'flat' gate
            atr_ticks = max(1, round(atr14 * atr_stop_mult / MINTICK))
            if signal_mode == "fpc":
                long_c = (armed_long and bull and not fresh_bull
                          and b.get("red_bar") and b.get("in_entry_window"))
                short_c = (armed_short and bear and not fresh_bear
                           and b.get("green_bar") and b.get("in_entry_window"))
            else:
                long_c = b["long_candidate"]
                short_c = b["short_candidate"]
            if enable_longs and long_c:
                pending = ("entry_long", atr_ticks, et)
                if signal_mode == "fpc":
                    armed_long = False                   # one entry per continuous regime
            elif enable_shorts and short_c:
                pending = ("entry_short", atr_ticks, et)
                if signal_mode == "fpc":
                    armed_short = False

    return trades


def summarize(trades):
    """Aggregate metrics for a trade list (no external deps)."""
    if not trades:
        return {"n": 0}
    pnls = [t["pnl"] for t in trades]
    net = sum(pnls)
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    gp, gl = sum(wins), -sum(losses)

    # max drawdown on the per-trade equity curve (in P/L points, qty 1)
    peak = 0.0
    eq = 0.0
    max_dd = 0.0
    for p in pnls:
        eq += p
        peak = max(peak, eq)
        max_dd = max(max_dd, peak - eq)

    def side_block(side):
        s = [t for t in trades if t["side"] == side]
        sp = [t["pnl"] for t in s]
        return {
            "n": len(s),
            "pnl": round(sum(sp), 4),
            "expectancy": round(sum(sp) / len(s), 6) if s else None,
        }

    return {
        "n": len(trades),
        "net_pnl": round(net, 4),
        "expectancy": round(net / len(trades), 6),
        "profit_factor": round(gp / gl, 4) if gl > 0 else None,
        "win_rate_pct": round(100.0 * len(wins) / len(trades), 4),
        "wins": len(wins),
        "losses": len(losses),
        "gross_profit": round(gp, 4),
        "gross_loss": round(gl, 4),
        "max_drawdown": round(max_dd, 4),
        "avg_bars_held": round(sum(t["bars_held"] for t in trades) / len(trades), 4),
        "exit_reason_counts": {
            r: sum(1 for t in trades if t["exit_reason"] == r)
            for r in ("Long ATR Stop", "Short ATR Stop", "VWAP Failure", "EOD")
        },
        "long": side_block("long"),
        "short": side_block("short"),
    }


# ---------------------------------------------------------------------------
# Analysis helpers — NOT part of the execution path. Used by the calibration
# and A/B scripts to attribute divergence to input-data quality. They read the
# already-computed feature rows; the engine never consults them.
# ---------------------------------------------------------------------------

SPIKE_WICK_PTS = 2.0   # a reverting wick this large on a 5m SPY bar is a
                       # data-anomaly (bad-tick) signature, not microstructure:
                       # ~0.35% at $560 in 5 min, vs a median ATR14 of ~0.66pt.


def spike_bars(feat_by_key, wick_pts=SPIKE_WICK_PTS):
    """Set of 5m-bar keys ('YYYY-MM-DDTHH:MM') whose low or high is a wick
    excursion greater than `wick_pts` beyond BOTH the open and the close — the
    corpus bad-tick signature (a spike that reverts inside the bar). Analysis
    only; the simulator faithfully consumes whatever bars it is given."""
    out = set()
    for k, r in feat_by_key.items():
        body_lo, body_hi = min(r["o"], r["c"]), max(r["o"], r["c"])
        if (body_lo - r["l"]) > wick_pts or (r["h"] - body_hi) > wick_pts:
            out.add(k)
    return out


if __name__ == "__main__":
    import json
    rows = compute_feature_rows(pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN)  # 9/20
    tr = simulate(rows)
    print(json.dumps({"v0_9_20": summarize(tr)}, indent=2))
