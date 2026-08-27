#!/usr/bin/env python3
"""Example driver — V0 FastAlpha tear sheet (raw vs screened) — v0.1 · 2026-08-26.

Applies the reusable `tearsheet` layer to V0 (EMA 9/20) and emits canonical
machine-readable evidence (JSON) plus a human markdown summary and a pure-SVG
equity/drawdown figure derived from the canonical series. Screened corpus (frozen
CORPUS_MASK_v1.0) is the primary view; raw is the mandatory sensitivity view.

This runs NO new strategy variant and draws no interpreted-run budget — it is a
reporting-layer demonstration on the existing V0 arm. Run: python3 v0_tearsheet.py
"""

import json
import os
import platform

import parity_foundation as pf
import tearsheet as ts

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))


def _row(name, s, r, d):
    def f(x):
        return "" if x is None else (f"{x:.4f}" if isinstance(x, float) else str(x))
    return f"| {name} | {f(s)} | {f(r)} | {f(d)} |"


def to_markdown(rep):
    s, r = rep["screened"], rep["raw"]
    sd = rep["screened_minus_raw_headline"]
    tm_s, tm_r = s["trade_metrics"], r["trade_metrics"]
    out = [f"# V0 (EMA 9/20) tear sheet — {rep['arm']}",
           "",
           "Primary view **screened** (frozen CORPUS_MASK_v1.0); raw is sensitivity. "
           "Local development window; corpus/mask unaltered. Not TV-equivalent "
           "(split-only vs ADJ feed seam).",
           "",
           "## Headline (screened | raw | Δ screened−raw)",
           "| metric | screened | raw | Δ |", "|---|---|---|---|"]
    for k in ("n", "net_pnl", "expectancy", "median_pnl", "win_rate_pct",
              "profit_factor", "payoff_ratio", "avg_bars_held"):
        out.append(_row(k, tm_s.get(k), tm_r.get(k), sd.get(k)))
    out.append(_row("max_drawdown", s["equity"]["max_drawdown"],
                    r["equity"]["max_drawdown"], sd.get("max_drawdown")))
    out += ["",
            f"long/short (screened): long n={tm_s['long']['n']} net={tm_s['long']['net_pnl']} "
            f"PF={tm_s['long']['profit_factor']} | short n={tm_s['short']['n']} "
            f"net={tm_s['short']['net_pnl']} PF={tm_s['short']['profit_factor']}",
            ""]
    rm = s["r_metrics"]
    out += ["## R-normalized (screened; 1R = frozen initial stop distance)",
            f"total_r={rm['total_r']} mean_r={rm['mean_r']} median_r={rm['median_r']} "
            f"avg_winner_r={rm['avg_winner_r']} avg_loser_r={rm['avg_loser_r']} "
            f"stdev_r={rm['stdev_r']}", ""]
    oc = s["outliers"]
    out += ["## Outlier concentration (screened) — robustness diagnostic only",
            f"(% of gross profit {oc['gross_profit']}) best 1: {oc['best_1']['pnl']} "
            f"({oc['best_1']['pct_of_gross_profit']}%) · best 5: {oc['best_5']['pnl']} "
            f"({oc['best_5']['pct_of_gross_profit']}%) · best 10: {oc['best_10']['pnl']} "
            f"({oc['best_10']['pct_of_gross_profit']}%) · top 1%: {oc['top_1pct']['pnl']} "
            f"({oc['top_1pct']['pct_of_gross_profit']}%)",
            f"net excl best 1/5/10: {oc['net_excl_best_1']} / {oc['net_excl_best_5']} "
            f"/ {oc['net_excl_best_10']}", ""]
    bs = s["bootstrap"]
    out += ["## Uncertainty (screened) — bootstrap CI of mean expectancy",
            f"mean={bs['mean_expectancy']} · IID 95% CI {bs['iid_ci95']} "
            f"(**{bs['iid_label']}**) · block(L={bs['block_len']}) 95% CI "
            f"{bs['block_ci95']}", ""]
    pm = s["portfolio"]
    out += ["## Portfolio (screened) — trade-based",
            f"Sharpe/trade={pm['sharpe_per_trade']} Sortino/trade={pm['sortino_per_trade']} "
            f"· annualized {pm['annualized'].get('sharpe_annualized')}/"
            f"{pm['annualized'].get('sortino_annualized')} "
            f"(tpy={pm['annualized'].get('trades_per_year_assumed')}, assumption-dependent)",
            "CAGR / Calmar: **DEFERRED** (account-construction-dependent).", ""]
    di = s["distribution"]
    out += ["## Consistency (screened)",
            f"months={di['n_months']} · profitable months "
            f"{di['profitable_months']}/{di['n_months']} ({di['pct_profitable_months']}%) · "
            f"max win streak {di['max_consecutive_wins']} · max loss streak "
            f"{di['max_consecutive_losses']}", ""]
    return "\n".join(out)


def main():
    print("python", platform.python_version(), "| tearsheet stdlib-only")
    print(f"corpus sha256 {pf.CANONICAL_SHA256} (guarded by parity_foundation)")
    rep = ts.dual_report(9, 20)

    out_json = os.path.join(HERE, "V0_TEARSHEET_2026-08-26.json")
    out_md = os.path.join(HERE, "V0_TEARSHEET_2026-08-26.md")
    out_svg = os.path.join(HERE, "V0_TEARSHEET_equity_2026-08-26.svg")
    with open(out_json, "w") as fh:
        json.dump(rep, fh, indent=2)
    with open(out_md, "w") as fh:
        fh.write(to_markdown(rep))
    eq = rep["screened"]["equity"]
    with open(out_svg, "w") as fh:
        fh.write(ts.equity_drawdown_svg(eq["equity_curve"], eq["underwater_curve"],
                                        title="V0 9/20 screened cum P/L"))

    tm = rep["screened"]["trade_metrics"]
    sd = rep["screened_minus_raw_headline"]
    print(f"\nV0 screened: n={tm['n']} net={tm['net_pnl']} exp={tm['expectancy']} "
          f"PF={tm['profit_factor']} win%={tm['win_rate_pct']} "
          f"maxDD={rep['screened']['equity']['max_drawdown']}")
    print(f"screened−raw net Δ={sd['net_pnl']} (screened primary; raw sensitivity)")
    print(f"metric inventory: {sum(len(v) if isinstance(v,dict) else 1 for v in rep['screened'].values())} "
          f"top-level blocks: {list(rep['screened'])}")
    for p in (out_json, out_md, out_svg):
        print("written:", os.path.relpath(p, STUDY))


if __name__ == "__main__":
    main()
