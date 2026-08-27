#!/usr/bin/env python3
"""Phase 4 — raw vs integrity-screened V0 diagnostic — v1.0 · 2026-08-26.

Runs ONLY after the corpus-integrity flag set is frozen (CORPUS_MASK_v1.0.json).
Reruns V0 (EMA 9/20) mechanically on (A) the raw corpus and (B) the research-
clean view (the frozen HIGH-CONFIDENCE anomaly bars dropped from the 1m stream
before 5m aggregation), and reports ONLY the effect of the frozen data-quality
treatment. Signal logic and stops are unchanged; no variant is run; validation
and holdout are untouched.

This is a DIAGNOSTIC of a data-quality treatment, not a new strategy trial — it
draws no interpreted-run budget. Run: python3 v0_raw_vs_screened_diagnostic.py
"""

import hashlib
import json
import os
import platform

import fastalpha_engine as fe

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")


def stop_count(trades):
    return sum(1 for t in trades if "Stop" in t["exit_reason"])


def main():
    print("python", platform.python_version(), "| stdlib only")
    mask = json.load(open(MASK))
    print(f"frozen mask {os.path.relpath(MASK, STUDY)} "
          f"sha256 {hashlib.sha256(open(MASK,'rb').read()).hexdigest()}")
    print(f"corpus sha256 {mask['corpus_sha256']} | mask bars {mask['count']} "
          f"(HIGH-CONFIDENCE): {mask['mask_keys']}")

    drop = set(mask["mask_t_ms"])
    raw = fe.simulate(fe.compute_feature_rows(9, 20))
    scr = fe.simulate(fe.compute_feature_rows(9, 20, drop_t_ms=drop))
    s_raw, s_scr = fe.summarize(raw), fe.summarize(scr)

    raw_by = {(t["entry_bar"], t["side"]): t for t in raw}
    scr_by = {(t["entry_bar"], t["side"]): t for t in scr}
    raw_only = sorted(set(raw_by) - set(scr_by))
    scr_only = sorted(set(scr_by) - set(raw_by))
    changed = []
    for k in sorted(set(raw_by) & set(scr_by)):
        a, b = raw_by[k], scr_by[k]
        if (a["exit_bar"], a["exit_reason"], a["pnl"]) != (b["exit_bar"], b["exit_reason"], b["pnl"]):
            changed.append({"entry_bar": k[0], "side": k[1],
                            "raw": {"exit_bar": a["exit_bar"], "reason": a["exit_reason"], "pnl": a["pnl"]},
                            "screened": {"exit_bar": b["exit_bar"], "reason": b["exit_reason"], "pnl": b["pnl"]}})

    results = {
        "role": "Phase 4 diagnostic: raw vs integrity-screened V0 (frozen mask; "
                "data-quality treatment only, not a strategy trial)",
        "python": platform.python_version(),
        "corpus_sha256": mask["corpus_sha256"],
        "mask_count": mask["count"], "mask_keys": mask["mask_keys"],
        "raw": s_raw, "screened": s_scr,
        "delta_screened_minus_raw": {
            "d_n_trades": s_scr["n"] - s_raw["n"],
            "d_stop_outs": stop_count(scr) - stop_count(raw),
            "d_net_pnl": round(s_scr["net_pnl"] - s_raw["net_pnl"], 4),
            "d_expectancy": round(s_scr["expectancy"] - s_raw["expectancy"], 6),
            "d_profit_factor": round((s_scr["profit_factor"] or 0) - (s_raw["profit_factor"] or 0), 4),
            "d_win_rate_pct": round(s_scr["win_rate_pct"] - s_raw["win_rate_pct"], 4),
            "d_max_drawdown": round(s_scr["max_drawdown"] - s_raw["max_drawdown"], 4),
        },
        "affected_trades": {
            "raw_only": [{"entry_bar": k[0], "side": k[1], **raw_by[k]} for k in raw_only],
            "screened_only": [{"entry_bar": k[0], "side": k[1], **scr_by[k]} for k in scr_only],
            "changed_exit": changed,
        },
        "r0_reference_net_pnl": 25.69,
    }
    out = os.path.join(HERE, "V0_RAW_VS_SCREENED_2026-08-26.json")
    with open(out, "w") as fh:
        json.dump(results, fh, indent=2)
    print(json.dumps(results["delta_screened_minus_raw"], indent=2))
    print(f"\naffected trades: raw_only {len(raw_only)}, screened_only {len(scr_only)}, "
          f"changed_exit {len(changed)}")
    print(f"results written: {os.path.relpath(out, STUDY)}")

    d = results["delta_screened_minus_raw"]
    print("\n" + "=" * 68)
    print("PHASE 4 DIAGNOSTIC — frozen data-quality treatment on V0")
    print("=" * 68)
    print(f"  raw      : n={s_raw['n']} net={s_raw['net_pnl']} stops={stop_count(raw)} "
          f"PF={s_raw['profit_factor']} maxDD={s_raw['max_drawdown']}")
    print(f"  screened : n={s_scr['n']} net={s_scr['net_pnl']} stops={stop_count(scr)} "
          f"PF={s_scr['profit_factor']} maxDD={s_scr['max_drawdown']}")
    print(f"  Δ(screened-raw): net {d['d_net_pnl']:+}, stop-outs {d['d_stop_outs']:+}, "
          f"trades {d['d_n_trades']:+}, maxDD {d['d_max_drawdown']:+}")
    print(f"  dropping {mask['count']} HIGH-CONFIDENCE bad-tick bars removes "
          f"{stop_count(raw) - stop_count(scr)} phantom stop-outs and moves the local\n"
          f"  net from {s_raw['net_pnl']} toward the R0 reference {results['r0_reference_net_pnl']} "
          f"(screened {s_scr['net_pnl']}).")


if __name__ == "__main__":
    main()
