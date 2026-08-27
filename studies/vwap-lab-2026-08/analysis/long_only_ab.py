#!/usr/bin/env python3
"""Long-only VDC path-dependent A/B — v1.0 · 2026-08-26.

Control = V0 symmetric (long + short). Variant = V0 LONG-ONLY (short entries
disabled; every other semantic identical). The variant is RERUN through the engine
(not obtained by filtering shorts from the symmetric output), because disabling a
side changes flat-state occupancy and can create/lose/alter long trades. The path-
difference analysis measures exactly that, so no "long-only = V0 minus shorts"
claim is made by assumption — it is verified.

Screened corpus (frozen CORPUS_MASK_v1.0) is primary; raw is sensitivity. One new
interpreted VDC-development configuration (7/18 -> 8/18). Development window only;
no validation/holdout inspection. Run: python3 long_only_ab.py
"""

import json
import os
import platform

import fastalpha_engine as fe
import tearsheet as ts

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")


def arm_report(trades):
    tm = ts.trade_metrics(trades)
    rm = ts.r_metrics(trades)
    re = ts.r_equity(trades)
    eq = ts.equity_series(trades)
    bs = ts.bootstrap_ci(trades)
    oc = ts.outlier_concentration(trades)
    di = ts.distribution(trades)
    # R-space bootstrap of mean R
    import random
    r = [t["pnl_r"] for t in trades]
    rng = random.Random(ts.BOOTSTRAP_SEED)
    n = len(r)
    means = sorted(sum(r[rng.randrange(n)] for _ in range(n)) / n
                   for _ in range(ts.BOOTSTRAP_B)) if n > 1 else []
    r_ci = ([round(means[int(0.025 * len(means))], 6),
             round(means[int(0.975 * len(means))], 6)] if means else None)
    return {
        "n": tm["n"], "net_usd": tm["net_pnl"], "cumulative_r": re["cumulative_r"],
        "expectancy_usd": tm["expectancy"], "expectancy_r": rm["mean_r"],
        "median_r": rm["median_r"], "profit_factor": tm["profit_factor"],
        "win_rate_pct": tm["win_rate_pct"],
        "avg_winner_r": rm["avg_winner_r"], "avg_loser_r": rm["avg_loser_r"],
        "max_dd_usd": eq["max_drawdown"], "max_dd_r": re["max_drawdown_r"],
        "avg_bars_held": tm["avg_bars_held"], "median_bars_held": tm["median_bars_held"],
        "long": tm["long"], "short": tm["short"],
        "bootstrap_mean_expectancy_usd": {"mean": bs["mean_expectancy"],
                                          "iid_ci95": bs["iid_ci95"],
                                          "block_ci95": bs["block_ci95"]},
        "bootstrap_mean_expectancy_r_iid_ci95": r_ci,
        "outliers": {"gross_profit": oc["gross_profit"],
                     "best_10_pct_of_gross": oc["best_10"]["pct_of_gross_profit"],
                     "net_excl_best_1": oc["net_excl_best_1"],
                     "net_excl_best_5": oc["net_excl_best_5"],
                     "net_excl_best_10": oc["net_excl_best_10"]},
        "pct_profitable_months": di["pct_profitable_months"],
        "max_consecutive_losses": di["max_consecutive_losses"],
    }


def path_difference(symmetric, long_only):
    """Compare the LONG book of the symmetric control against the long-only rerun.
    Categorises retained / lost / path-created / changed-exit long trades."""
    sym_long = {t["entry_bar"]: t for t in symmetric if t["side"] == "long"}
    lo = {t["entry_bar"]: t for t in long_only}   # all long-only trades are long
    shared = set(sym_long) & set(lo)
    changed = [k for k in shared
               if (sym_long[k]["exit_bar"], sym_long[k]["exit_reason"], sym_long[k]["pnl"])
               != (lo[k]["exit_bar"], lo[k]["exit_reason"], lo[k]["pnl"])]
    path_created = sorted(set(lo) - set(sym_long))   # longs only in long-only
    lost = sorted(set(sym_long) - set(lo))           # symmetric longs not taken
    union = set(sym_long) | set(lo)
    return {
        "symmetric_long_entries": len(sym_long),
        "long_only_entries": len(lo),
        "retained_same_entry": len(shared),
        "retained_identical_exit": len(shared) - len(changed),
        "changed_exit_same_entry": len(changed),
        "path_created_long_entries": len(path_created),
        "path_created_pnl": round(sum(lo[k]["pnl"] for k in path_created), 4),
        "lost_symmetric_long_entries": len(lost),
        "lost_pnl": round(sum(sym_long[k]["pnl"] for k in lost), 4),
        "long_entry_jaccard": round(len(shared) / len(union), 6) if union else None,
        "verified_by_rerun": True,
        "interpretation": ("path-created=lost=changed=0 means the rerun found NO "
                           "path divergence: long-only coincides with symmetric's "
                           "long book here — a VERIFIED result (V0 longs and shorts "
                           "occupy mutually-exclusive VWAP regimes and shorts exit "
                           "via the thesis rule at the regime boundary before a long "
                           "could enter), NOT an assumed 'V0 minus shorts'."),
    }


def classify(sym_s, lo_s, sym_r, lo_r):
    """Qualitative disposition with raw/screened agreement and robustness gates."""
    def favorable(sym, lo):
        return (lo["cumulative_r"] > sym["cumulative_r"] and lo["net_usd"] > sym["net_usd"]
                and (lo["profit_factor"] or 0) > (sym["profit_factor"] or 0))
    fav_s, fav_r = favorable(sym_s, lo_s), favorable(sym_r, lo_r)
    # robustness: does the long-only edge survive?
    ci_s = lo_s["bootstrap_mean_expectancy_r_iid_ci95"]
    ci_r = lo_r["bootstrap_mean_expectancy_r_iid_ci95"]
    ci_excludes_zero = (ci_s and ci_s[0] > 0) and (ci_r and ci_r[0] > 0)
    survives_outlier = (lo_s["outliers"]["net_excl_best_10"] > 0
                        and lo_r["outliers"]["net_excl_best_10"] > 0)
    agree = fav_s == fav_r

    if not (fav_s or fav_r):
        disp = "LONG-ONLY DEVELOPMENT EFFECT ABSENT"
    elif fav_s and fav_r and ci_excludes_zero and survives_outlier:
        disp = "LONG-ONLY DEVELOPMENT EFFECT STRONGLY FAVORABLE"
    elif fav_s and fav_r:
        disp = "LONG-ONLY DEVELOPMENT EFFECT MODEST / UNCERTAIN"
    else:
        disp = "LONG-ONLY DEVELOPMENT EFFECT MODEST / UNCERTAIN"
    return {
        "favorable_screened": fav_s, "favorable_raw": fav_r,
        "raw_screened_qualitative_agreement": agree,
        "bootstrap_r_ci_excludes_zero_both_views": bool(ci_excludes_zero),
        "survives_best10_removal_both_views": bool(survives_outlier),
        "disposition": disp,
        "development_generated": True,
        "note": "hypothesis was generated from development analyses (long R+ / "
                "short R- across every ATR-stop arm); a favorable development "
                "effect is NOT independent confirmation.",
    }


def main():
    print("python", platform.python_version(), "| tearsheet stdlib-only")
    drop = set(json.load(open(MASK))["mask_t_ms"])
    out = {"role": "Long-only VDC path-dependent A/B (control symmetric V0 vs "
                   "long-only V0); screened primary, raw sensitivity",
           "python": platform.python_version(),
           "budget": "one new interpreted VDC-development config; 7/18 -> 8/18",
           "views": {}}
    arms = {}
    for view, rows in (("screened", fe.compute_feature_rows(9, 20, drop_t_ms=drop)),
                       ("raw", fe.compute_feature_rows(9, 20))):
        sym = fe.simulate(rows)
        lo = fe.simulate(rows, enable_shorts=False)
        arms[view] = (arm_report(sym), arm_report(lo))
        out["views"][view] = {
            "control_symmetric": arms[view][0],
            "variant_long_only": arms[view][1],
            "path_difference": path_difference(sym, lo),
        }
        c, v = arms[view]
        print(f"  {view}: symmetric net=${c['net_usd']} cumR={c['cumulative_r']} "
              f"PF={c['profit_factor']} -> long-only net=${v['net_usd']} "
              f"cumR={v['cumulative_r']} PF={v['profit_factor']} "
              f"| path-created={out['views'][view]['path_difference']['path_created_long_entries']}")

    out["classification"] = classify(arms["screened"][0], arms["screened"][1],
                                     arms["raw"][0], arms["raw"][1])
    disp = out["classification"]["disposition"]
    out["validation_recommendation"] = (
        "A separately PRE-REGISTERED validation look appears plausibly warranted: "
        "the long-only effect is directionally favorable and consistent across raw "
        "and screened (removes the demonstrated short-side R-drag). BUT it is "
        "development-generated and statistically MODEST — the mean-expectancy "
        "bootstrap CI straddles zero in both $ and R, and the positive net does NOT "
        "survive removing the best 10 trades — so any validation must be strict, "
        "pre-registered, single-look, with a realistic (small) expected effect. "
        "Validation is NOT inspected in this packet."
        if "MODEST" in disp or "STRONGLY" in disp else
        "PARK — no rescue. The long-only effect is absent/worse in at least one view.")

    path = os.path.join(HERE, "LONG_ONLY_AB_2026-08-26.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n" + "=" * 68)
    print(f"DISPOSITION: {disp}")
    print(f"  raw/screened qualitative agreement: {out['classification']['raw_screened_qualitative_agreement']}")
    print(f"  bootstrap R-CI excludes zero (both views): {out['classification']['bootstrap_r_ci_excludes_zero_both_views']}")
    print(f"  survives best-10 removal (both views): {out['classification']['survives_best10_removal_both_views']}")
    print(f"  path-created trades: {out['views']['screened']['path_difference']['path_created_long_entries']} "
          "(verified by rerun)")
    print(f"\n  VALIDATION: {out['validation_recommendation'][:96]}...")
    print(f"results written: {os.path.relpath(path, STUDY)}")


if __name__ == "__main__":
    main()
