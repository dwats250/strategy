#!/usr/bin/env python3
"""PART A — fixed-risk V0 diagnostic — v1.0 · 2026-08-26.

Re-expresses the EXISTING V0 (EMA 9/20) trade sets under EQUAL INITIAL RISK
(1R per trade), on the screened (primary) and raw (sensitivity) corpus views. It
reruns no strategy and changes no trade — it only re-weights the already-computed
V0 outcomes from fixed-1-share into fixed-risk (R) space, to separate position-
sizing effects from stop geometry before the ATR-stop surface experiment.

NOT a new strategy trial; draws no interpreted-run budget. CAGR is not used as a
discovery metric; the $100/trade figure is an ACCOUNT-CONSTRUCTION EXAMPLE ONLY.
Run: python3 v0_fixed_risk_diagnostic.py
"""

import json
import math
import os
import platform

import fastalpha_engine as fe
import tearsheet as ts

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")

# PREDECLARED descriptive buckets for the ATR/risk-vs-R relationship (NOT a
# filter, NOT optimized): quintiles of per-trade risk_points (∝ entry ATR).
RISK_QUANTILES = [0.20, 0.40, 0.60, 0.80]
ACCOUNT_EXAMPLE_RISK_USD = 100.0     # arbitrary; labelled account-construction only


def _pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return round(sxy / math.sqrt(sxx * syy), 6) if sxx > 0 and syy > 0 else None


def _quantile_edges(vals, qs):
    s = sorted(vals)
    return [s[min(len(s) - 1, int(q * len(s)))] for q in qs]


def risk_r_relationship(trades):
    """Mean R outcome by predeclared risk_points quintile. Descriptive only."""
    rp = [t["risk_points"] for t in trades]
    edges = _quantile_edges(rp, RISK_QUANTILES)
    buckets = [[] for _ in range(len(edges) + 1)]
    for t in trades:
        k = 0
        while k < len(edges) and t["risk_points"] > edges[k]:
            k += 1
        buckets[k].append(t)
    out = []
    for i, b in enumerate(buckets):
        rs = [t["pnl_r"] for t in b]
        rpv = [t["risk_points"] for t in b]
        out.append({
            "bucket": i + 1, "n": len(b),
            "risk_points_range": [round(min(rpv), 4), round(max(rpv), 4)] if b else None,
            "mean_r": round(sum(rs) / len(rs), 6) if rs else None,
            "net_r": round(sum(rs), 4) if rs else None,
            "win_rate_pct": round(100 * sum(1 for x in rs if x > 0) / len(rs), 3) if rs else None,
        })
    return {"predeclared_quantiles": RISK_QUANTILES,
            "risk_points_quintile_edges": [round(e, 4) for e in edges],
            "note": "descriptive quintiles of frozen entry risk_points (∝ ATR); "
                    "NOT an ATR filter and NOT optimized",
            "buckets": out}


def view_report(trades, view):
    tm = ts.trade_metrics(trades)
    rm = ts.r_metrics(trades)
    re = ts.r_equity(trades)
    eq = ts.equity_series(trades)
    long = [t for t in trades if t["side"] == "long"]
    short = [t for t in trades if t["side"] == "short"]

    def r_exp(ts_):
        rs = [t["pnl_r"] for t in ts_]
        return round(sum(rs) / len(rs), 6) if rs else None

    pnl = [t["pnl"] for t in trades]
    pr = [t["pnl_r"] for t in trades]
    return {
        "view": view,
        "n": tm["n"],
        "fixed_share_net_usd": tm["net_pnl"],       # 1-share $ (arbitrary sizing)
        "fixed_risk_cumulative_r": re["cumulative_r"],
        "mean_r": rm["mean_r"], "median_r": rm["median_r"],
        "max_drawdown_r": re["max_drawdown_r"],
        "longest_drawdown_r_trades": re["longest_drawdown_r_trades"],
        "max_drawdown_usd_fixed_share": eq["max_drawdown"],
        "long_r_expectancy": r_exp(long), "short_r_expectancy": r_exp(short),
        "long_cum_r": round(sum(t["pnl_r"] for t in long), 4),
        "short_cum_r": round(sum(t["pnl_r"] for t in short), 4),
        "fixed_share_vs_fixed_risk": {
            "net_usd_sign": "pos" if tm["net_pnl"] > 0 else "neg",
            "cum_r_sign": "pos" if re["cumulative_r"] > 0 else "neg",
            "signs_disagree": (tm["net_pnl"] > 0) != (re["cumulative_r"] > 0),
            "pearson_pnl_usd_vs_pnl_r": _pearson(pnl, pr),
            "interpretation": "when the $ and R signs disagree, position sizing "
                              "(risk per trade), not stop geometry, drives the "
                              "headline: larger-risk (higher-ATR) trades dominate "
                              "the $ total but each counts as 1R in R space",
        },
        "account_example_usd": {
            "risk_per_trade_usd": ACCOUNT_EXAMPLE_RISK_USD,
            "final_equity_usd": round(ACCOUNT_EXAMPLE_RISK_USD * re["cumulative_r"], 2),
            "max_drawdown_usd": round(ACCOUNT_EXAMPLE_RISK_USD * re["max_drawdown_r"], 2),
            "label": "ACCOUNT-CONSTRUCTION EXAMPLE ONLY — arbitrary $100 risk/trade; "
                     "CAGR intentionally not computed (account-construction-dependent)",
        },
        "atr_risk_vs_r_outcome": risk_r_relationship(trades),
        "r_equity_curve": re["r_equity_curve"],
        "r_underwater_curve": re["r_underwater_curve"],
    }


def main():
    print("python", platform.python_version(), "| tearsheet stdlib-only")
    drop = set(json.load(open(MASK))["mask_t_ms"])
    screened = fe.simulate(fe.compute_feature_rows(9, 20, drop_t_ms=drop))
    raw = fe.simulate(fe.compute_feature_rows(9, 20))
    rep = {
        "role": "PART A — fixed-risk (1R) re-expression of existing V0; not a "
                "new strategy trial; no budget draw",
        "python": platform.python_version(),
        "arm": "EMA 9/20 (V0), ATR_STOP_MULT 1.0",
        "screened": view_report(screened, "screened"),
        "raw": view_report(raw, "raw"),
    }
    out = os.path.join(HERE, "V0_FIXED_RISK_DIAGNOSTIC_2026-08-26.json")
    with open(out, "w") as fh:
        json.dump(rep, fh, indent=2)

    s = rep["screened"]
    print(f"\nV0 screened fixed-risk: n={s['n']} cum_R={s['fixed_risk_cumulative_r']} "
          f"mean_R={s['mean_r']} maxDD_R={s['max_drawdown_r']}")
    print(f"  fixed-share net ${s['fixed_share_net_usd']} vs cum_R {s['fixed_risk_cumulative_r']} "
          f"-> signs_disagree={s['fixed_share_vs_fixed_risk']['signs_disagree']} "
          f"(pearson $ vs R = {s['fixed_share_vs_fixed_risk']['pearson_pnl_usd_vs_pnl_r']})")
    print(f"  long R-exp {s['long_r_expectancy']} / short R-exp {s['short_r_expectancy']}")
    print("  ATR/risk quintile mean R:",
          [b["mean_r"] for b in s["atr_risk_vs_r_outcome"]["buckets"]])
    print(f"results written: {os.path.relpath(out, STUDY)}")


if __name__ == "__main__":
    main()
