#!/usr/bin/env python3
"""Deterministic tests for the tear-sheet layer.

Covers metric formulas, R normalization, drawdown, profit-factor edge cases,
zero-winner / zero-loser cases, A/B overlap, raw/screened dual reporting, and
bootstrap determinism. Includes a REFERENCE CROSS-CHECK of the standard formulas
against an independent numpy implementation (numpy is used only in the test, and
only if importable — it is never a runtime dependency of tearsheet.py).
Run: python3 test_tearsheet.py
"""

import os
import sys

import tearsheet as ts


def trade(pnl, side="long", bars=5, risk=1.0, reason="EOD",
          entry="2025-01-02 10:00", exit_="2025-01-02 10:25"):
    return {"side": side, "pnl": pnl, "pnl_r": (pnl / risk) if risk else None,
            "risk_points": risk, "bars_held": bars, "exit_reason": reason,
            "entry_bar": entry, "exit_bar": exit_}


def approx(a, b, tol=1e-6):     # metrics are rounded to 6 decimals
    return abs(a - b) <= tol


def test_basic_trade_metrics():
    tr = [trade(2.0), trade(-1.0), trade(3.0), trade(-1.0)]
    m = ts.trade_metrics(tr)
    assert m["n"] == 4 and approx(m["net_pnl"], 3.0)
    assert approx(m["expectancy"], 0.75) and m["wins"] == 2 and m["losses"] == 2
    assert approx(m["profit_factor"], 5.0 / 2.0)         # gp 5 / gl 2
    assert approx(m["avg_winner"], 2.5) and approx(m["avg_loser"], -1.0)
    assert approx(m["payoff_ratio"], 2.5)
    assert approx(m["largest_win"], 3.0) and approx(m["largest_loss"], -1.0)


def test_r_normalization_uses_frozen_risk():
    tr = [trade(2.0, risk=1.0), trade(-1.5, risk=1.5), trade(3.0, risk=2.0)]
    r = ts.r_metrics(tr)
    # pnl_r = 2.0, -1.0, 1.5  -> total 2.5, mean 0.8333
    assert approx(r["total_r"], 2.5) and approx(r["mean_r"], 2.5 / 3)
    assert approx(r["avg_winner_r"], (2.0 + 1.5) / 2) and approx(r["avg_loser_r"], -1.0)


def test_drawdown_and_longest_duration():
    # equity: +5, +3, +8, +2, +6  -> peak 8 at idx2; dd to 2 (dd=6), then recover
    tr = [trade(5.0), trade(-2.0), trade(5.0), trade(-6.0), trade(4.0)]
    e = ts.equity_series(tr)
    assert e["equity_curve"][-1] == 6.0
    assert approx(e["max_drawdown"], 6.0)               # 8 -> 2
    assert e["longest_drawdown_trades"] == 2            # idx3,idx4 below peak


def test_pf_zero_losers_and_zero_winners():
    assert ts.trade_metrics([trade(1.0), trade(2.0)])["profit_factor"] is None  # no losers
    assert ts.trade_metrics([trade(-1.0), trade(-2.0)])["profit_factor"] == 0.0  # no winners


def test_outlier_concentration_gross_profit_denominator():
    tr = [trade(10.0), trade(-1.0), trade(-1.0), trade(-1.0)]
    oc = ts.outlier_concentration(tr)
    assert approx(oc["gross_profit"], 10.0)
    assert approx(oc["best_1"]["pnl"], 10.0)
    assert approx(oc["best_1"]["pct_of_gross_profit"], 100.0)
    assert approx(oc["net_excl_best_1"], -3.0)


def test_streaks_and_monthly():
    tr = [trade(1.0, exit_="2025-01-31 10:00"), trade(1.0, exit_="2025-01-31 11:00"),
          trade(-1.0, exit_="2025-02-03 10:00"), trade(-1.0, exit_="2025-02-03 11:00"),
          trade(-1.0, exit_="2025-02-04 10:00")]
    d = ts.distribution(tr)
    assert d["max_consecutive_wins"] == 2 and d["max_consecutive_losses"] == 3
    assert d["n_months"] == 2 and d["profitable_months"] == 1
    assert approx(d["pct_profitable_months"], 50.0)


def test_r_equity_cumulative_and_drawdown():
    tr = [trade(1.0, risk=1.0), trade(-0.5, risk=0.5), trade(2.0, risk=1.0),
          trade(-1.5, risk=1.0)]
    # pnl_r = 1, -1, 2, -1.5 -> cum 1, 0, 2, 0.5 ; peak 2 -> dd to 0.5 = 1.5
    re = ts.r_equity(tr)
    assert approx(re["cumulative_r"], 0.5)
    assert re["r_equity_curve"] == [1.0, 0.0, 2.0, 0.5]
    assert approx(re["max_drawdown_r"], 1.5)
    assert re["longest_drawdown_r_trades"] == 1


def test_ab_overlap():
    ctrl = [trade(1.0, entry="2025-01-02 10:00"), trade(2.0, entry="2025-01-02 11:00")]
    var = [trade(1.0, entry="2025-01-02 10:00"),   # shared, same exit
           trade(5.0, entry="2025-01-03 10:00")]   # added
    ab = ts.ab_report(ctrl, var)
    ov = ab["entry_overlap"]
    assert ov["shared"] == 1 and ov["trades_added"] == 1 and ov["trades_removed"] == 1
    assert approx(ov["jaccard"], 1 / 3)


def test_ab_dual_direction_agreement():
    c = [trade(1.0, entry="2025-01-02 10:00")]
    v = [trade(2.0, entry="2025-01-02 10:00")]      # +1 both views -> agree
    res = ts.ab_dual(c, v, c, v, label="synthetic")
    assert res["views_agree_on_direction"] is True
    assert res["screened_net_delta"] == res["raw_net_delta"] == 1.0


def test_bootstrap_determinism():
    tr = [trade(float(i % 5 - 2)) for i in range(60)]
    a = ts.bootstrap_ci(tr, seed=123, B=500)
    b = ts.bootstrap_ci(tr, seed=123, B=500)
    assert a == b, "bootstrap not deterministic under fixed seed"
    assert a["block_len"] == max(1, round(60 ** (1 / 3)))


def test_reference_crosscheck_numpy():
    try:
        import numpy as np
    except ImportError:
        print("  (numpy absent — reference cross-check skipped)")
        return
    tr = [trade(float((i * 7) % 11 - 5)) for i in range(200)]
    p = np.array([t["pnl"] for t in tr])
    m = ts.trade_metrics(tr)
    pm = ts.portfolio_metrics(tr)
    assert approx(m["expectancy"], float(p.mean()), 1e-6)
    assert approx(m["stdev_pnl"], float(p.std(ddof=1)), 1e-6)
    # profit factor vs numpy
    gp = float(p[p > 0].sum()); gl = float(-p[p < 0].sum())
    assert approx(m["profit_factor"], gp / gl, 1e-6)
    # trade-based Sharpe vs numpy
    assert approx(pm["sharpe_per_trade"], float(p.mean() / p.std(ddof=1)), 1e-6)
    # Sortino downside deviation (target 0) vs numpy
    dd = float(np.sqrt(np.mean(np.minimum(0.0, p) ** 2)))
    assert approx(pm["sortino_per_trade"], float(p.mean()) / dd, 1e-6)
    print("  (reference cross-check vs numpy: expectancy, stdev, PF, Sharpe, Sortino OK)")


def test_dual_report_raw_screened_delta():
    rep = ts.dual_report(9, 20)
    assert set(rep) >= {"screened", "raw", "screened_minus_raw_headline"}
    assert rep["primary_view"] == "screened"
    d = rep["screened_minus_raw_headline"]
    # screened net minus raw net must equal the two reports' difference
    ns = rep["screened"]["trade_metrics"]["net_pnl"]
    nr = rep["raw"]["trade_metrics"]["net_pnl"]
    assert approx(d["net_pnl"], round(ns - nr, 6), 1e-6)


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} TEARSHEET TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
