"""Metrics. Two families, never mixed:

* Portfolio metrics come from ACCOUNT EQUITY sampled at each session's close
  (session returns). Sharpe/Sortino/volatility are annualized with sqrt(252) because
  the sample is one return per trading session, flat days included.
* Trade metrics are per-trade R multiples and P&L. They are never annualized; a
  per-trade t-statistic is reported instead of a "trade Sharpe".
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def session_returns(session_equity: pd.Series, initial_cash: float) -> pd.Series:
    eq = session_equity.astype(float)
    prev = eq.shift(1)
    prev.iloc[0] = initial_cash
    return (eq / prev - 1.0).rename("ret")


def drawdown(equity: pd.Series) -> pd.Series:
    peak = equity.cummax()
    return equity / peak - 1.0


def equity_metrics(session_equity: pd.Series, initial_cash: float,
                   bar_equity: pd.Series | None = None) -> dict:
    r = session_returns(session_equity, initial_cash)
    n = len(r)
    final = float(session_equity.iloc[-1]) if n else initial_cash
    total = final / initial_cash - 1.0
    years = n / TRADING_DAYS
    sd = r.std(ddof=1) if n > 1 else np.nan
    downside = math.sqrt(float((r.clip(upper=0) ** 2).mean())) if n else np.nan
    eq_with_start = pd.concat([pd.Series([initial_cash]), session_equity.reset_index(drop=True)])
    mdd_close = float(drawdown(eq_with_start).min()) if n else 0.0
    out = {
        "sessions": n,
        "start_equity": initial_cash,
        "final_equity": final,
        "net_pnl": final - initial_cash,
        "total_return": total,
        "cagr": (1 + total) ** (1 / years) - 1 if years > 0 and final > 0 else np.nan,
        "ann_vol": sd * math.sqrt(TRADING_DAYS) if n > 1 else np.nan,
        "sharpe_daily_ann": (r.mean() / sd * math.sqrt(TRADING_DAYS)) if n > 1 and sd > 0 else np.nan,
        "sortino_daily_ann": (r.mean() / downside * math.sqrt(TRADING_DAYS)) if downside and downside > 0 else np.nan,
        "max_dd_session_close": mdd_close,
        "pct_sessions_up": float((r > 0).mean()) if n else np.nan,
        "pct_sessions_flat": float((r == 0).mean()) if n else np.nan,
        "best_session": float(r.max()) if n else np.nan,
        "worst_session": float(r.min()) if n else np.nan,
    }
    if bar_equity is not None and len(bar_equity):
        out["max_dd_intraday"] = float(drawdown(pd.concat([pd.Series([initial_cash]), bar_equity.reset_index(drop=True)])).min())
    out["calmar"] = (out["cagr"] / -out["max_dd_session_close"]
                     if out["max_dd_session_close"] < 0 and not np.isnan(out["cagr"]) else np.nan)
    return out


def trade_metrics(trades: pd.DataFrame) -> dict:
    closed = trades[trades["exit_reason"] != "open_at_end"]
    n = len(closed)
    out: dict = {"trades": n, "open_at_end": int((trades["exit_reason"] == "open_at_end").sum())}
    if n == 0:
        return out
    pnl = closed["pnl"].astype(float)
    r = closed["r_multiple"].astype(float).dropna()
    wins, losses = pnl[pnl > 0], pnl[pnl <= 0]
    out.update({
        "win_rate": float((pnl > 0).mean()),
        "net_pnl_trades": float(pnl.sum()),
        "gross_pnl_trades": float(closed["gross_pnl"].sum()),
        "costs": float(closed["costs"].sum()),
        "avg_win": float(wins.mean()) if len(wins) else np.nan,
        "avg_loss": float(losses.mean()) if len(losses) else np.nan,
        "profit_factor": float(wins.sum() / -losses.sum()) if losses.sum() < 0 else np.nan,
        "expectancy_r": float(r.mean()) if len(r) else np.nan,
        "median_r": float(r.median()) if len(r) else np.nan,
        "std_r": float(r.std(ddof=1)) if len(r) > 1 else np.nan,
        "t_stat_r": float(r.mean() / r.std(ddof=1) * math.sqrt(len(r))) if len(r) > 1 and r.std(ddof=1) > 0 else np.nan,
        "avg_minutes_spanned": float(closed["minutes_spanned"].mean()) if "minutes_spanned" in closed else np.nan,
        "stop_beyond_fill": int((closed["exit_reason"] == "stop_beyond_fill").sum()),
        "r_undefined": int(closed["r_multiple"].isna().sum()),
        "long_trades": int((closed["side"] == "long").sum()),
        "short_trades": int((closed["side"] == "short").sum()),
        "expectancy_r_long": float(closed.loc[closed.side == "long", "r_multiple"].mean()) if (closed.side == "long").any() else np.nan,
        "expectancy_r_short": float(closed.loc[closed.side == "short", "r_multiple"].mean()) if (closed.side == "short").any() else np.nan,
        "exit_reasons": closed["exit_reason"].value_counts().to_dict(),
        "ambiguous_stop_target_minutes": int(closed.get("ambiguous_exit", pd.Series(False, index=closed.index)).sum()),
    })
    out.update(concentration(pnl))
    return out


def concentration(pnl: pd.Series, ks=(1, 5, 10)) -> dict:
    """How much of the result depends on a few large winners."""
    net = float(pnl.sum())
    s = pnl.sort_values(ascending=False)
    winners = s[s > 0]
    out = {}
    gross_profit = float(winners.sum())
    for k in ks:
        # share: the k largest WINNERS / gross profit (never diluted by losers)
        out[f"top{k}_share_of_gross_profit"] = float(winners.head(k).sum()) / gross_profit if gross_profit > 0 else np.nan
        # net with the k largest trades removed
        out[f"net_pnl_ex_top{k}"] = net - float(s.head(k).sum())
    return out


def monthly_returns(session_equity: pd.Series, initial_cash: float) -> pd.Series:
    eq = session_equity.copy()
    eq.index = pd.to_datetime(pd.Index(eq.index))
    month_end = eq.groupby(eq.index.to_period("M")).last()
    prev = month_end.shift(1)
    prev.iloc[0] = initial_cash
    return (month_end / prev - 1.0).rename("monthly_return")


def rolling_sharpe(session_equity: pd.Series, initial_cash: float, window: int = 63) -> pd.Series:
    r = session_returns(session_equity, initial_cash)
    return (r.rolling(window).mean() / r.rolling(window).std(ddof=1) * math.sqrt(TRADING_DAYS)).rename("rolling_sharpe")


def expected_max_sharpe(n_trials: int, n_obs: int) -> dict:
    """Expected maximum Sharpe of N independent zero-skill trials (Bailey & Lopez de Prado).

    Per-period SR estimates under the null have variance ~ 1/(T-1); the hurdle is the
    expected maximum of N such estimates. Returned per-session and annualized. With
    N=1 the expectation is 0 (no selection), so the hurdle is reported as 0.
    """
    from statistics import NormalDist
    if n_trials <= 1 or n_obs < 3:
        return {"n_trials": n_trials, "n_obs": n_obs, "sr_per_session": 0.0, "sr_annualized": 0.0}
    gamma = 0.5772156649
    nd = NormalDist()
    z = (1 - gamma) * nd.inv_cdf(1 - 1 / n_trials) + gamma * nd.inv_cdf(1 - 1 / (n_trials * math.e))
    sr = z * math.sqrt(1 / (n_obs - 1))
    return {"n_trials": n_trials, "n_obs": n_obs, "sr_per_session": sr,
            "sr_annualized": sr * math.sqrt(TRADING_DAYS)}
