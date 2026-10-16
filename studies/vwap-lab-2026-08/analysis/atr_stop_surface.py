#!/usr/bin/env python3
"""PARTS B+C — ATR-stop response-surface experiment — v1.0 · 2026-08-26.

Freezes a five-value ATR_STOP_MULT family BEFORE inspecting outcomes and runs the
full family on the screened (primary) and raw (sensitivity) corpus views. Only the
initial ATR stop distance changes; entries, EMA/VWAP/session logic, the trigger,
thesis exit, EOD, and sizing are exactly V0. For every arm it produces the standard
tear-sheet metrics, a bootstrap CI, and outlier concentration, then classifies the
response shape and assesses the 1.00 control — WITHOUT selecting a production value.

Budget: 1.00 is the existing V0 (no new draw); 0.75/1.25/1.50/1.75 are four new
interpreted VDC-development configurations (3/18 -> 7/18). Development window only;
no validation/holdout/embargo; no EMA/PVAE/sizing change. Run: python3 atr_stop_surface.py
"""

import csv
import json
import os
import platform

import fastalpha_engine as fe
import tearsheet as ts

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")

# FROZEN before any outcome inspection (Part B):
FROZEN_MULTS = [0.75, 1.00, 1.25, 1.50, 1.75]
CONTROL = 1.00
# PREDECLARED classification threshold (economic materiality in R/trade):
MATERIAL_R = 0.03


def arm_summary(trades):
    tm = ts.trade_metrics(trades)
    rm = ts.r_metrics(trades)
    re = ts.r_equity(trades)
    eq = ts.equity_series(trades)
    bs = ts.bootstrap_ci(trades)
    oc = ts.outlier_concentration(trades)
    ec = tm["exit_reason_counts"]
    stops = ec["Long ATR Stop"] + ec["Short ATR Stop"]
    n = tm["n"]

    def side_r(side):
        s = [t for t in trades if t["side"] == side]
        rs = [t["pnl_r"] for t in s]
        w = sum(x for x in rs if x > 0)
        l = -sum(x for x in rs if x < 0)
        return {"n": len(s),
                "expectancy_r": round(sum(rs) / len(rs), 6) if rs else None,
                "profit_factor": round(w / l, 6) if l > 0 else None}
    return {
        "n": n,
        "stop_outs": stops,
        "stop_out_pct": round(100 * stops / n, 3) if n else None,
        "thesis_exits": ec["VWAP Failure"],
        "eod_exits": ec["EOD"],
        "net_usd": tm["net_pnl"],
        "expectancy_usd": tm["expectancy"],
        "expectancy_r": rm["mean_r"],
        "median_r": rm["median_r"],
        "profit_factor": tm["profit_factor"],
        "win_rate_pct": tm["win_rate_pct"],
        "avg_winner_r": rm["avg_winner_r"],
        "avg_loser_r": rm["avg_loser_r"],
        "max_dd_usd": eq["max_drawdown"],
        "max_dd_r": re["max_drawdown_r"],
        "avg_bars_held": tm["avg_bars_held"],
        "median_bars_held": tm["median_bars_held"],
        "long": side_r("long"),
        "short": side_r("short"),
        "bootstrap_mean_expectancy_usd": {
            "mean": bs["mean_expectancy"], "iid_ci95": bs["iid_ci95"],
            "block_ci95": bs["block_ci95"], "block_len": bs["block_len"]},
        "outliers": {"best_10_pct_of_gross": oc["best_10"]["pct_of_gross_profit"],
                     "net_excl_best_10": oc["net_excl_best_10"]},
    }


def classify(screened, raw):
    """Deterministic, predeclared response-shape classification on the SCREENED
    primary view (expectancy_r), cross-checked against raw and long/short."""
    xr = [screened[m]["expectancy_r"] for m in FROZEN_MULTS]
    ctrl = screened[CONTROL]["expectancy_r"]
    spread = max(xr) - min(xr)

    # raw/screened directional agreement per arm (sign of arm - control)
    def sign(x):
        return 0 if abs(x) < 1e-12 else (1 if x > 0 else -1)
    disagree = 0
    for m in FROZEN_MULTS:
        if m == CONTROL:
            continue
        ds = sign(screened[m]["expectancy_r"] - ctrl)
        dr = sign(raw[m]["expectancy_r"] - raw[CONTROL]["expectancy_r"])
        if ds != 0 and dr != 0 and ds != dr:
            disagree += 1
    # long/short conflict at the best arm
    best_m = max(FROZEN_MULTS, key=lambda m: screened[m]["expectancy_r"])
    ls_conflict = (sign(screened[best_m]["long"]["expectancy_r"] or 0)
                   != sign(screened[best_m]["short"]["expectancy_r"] or 0))

    # monotonic check (allowing sub-material wiggle)
    diffs = [xr[i + 1] - xr[i] for i in range(len(xr) - 1)]
    inc = all(d > -MATERIAL_R for d in diffs)
    dec = all(d < MATERIAL_R for d in diffs)

    if disagree >= 2:
        shape = "5. UNSTABLE / CONFLICTED"
        why = f"raw and screened disagree on the sign of (arm−control) for {disagree} arms"
    elif spread < MATERIAL_R:
        shape = "4. FLAT / NO MATERIAL SENSITIVITY"
        why = f"screened expectancy_r spread {round(spread,4)} < MATERIAL_R {MATERIAL_R}"
    elif inc != dec:      # exactly one of monotone-inc / monotone-dec holds
        shape = "2. MONOTONIC RESPONSE"
        why = ("expectancy_r " + ("improves" if inc else "deteriorates")
               + " coherently as the stop widens")
    else:
        # peak vs broad region
        best = max(xr)
        near_best = [m for m, x in zip(FROZEN_MULTS, xr) if best - x < MATERIAL_R]
        contiguous = (len(near_best) >= 2 and
                      all(abs(near_best[i + 1] - near_best[i] - 0.25) < 1e-9
                          for i in range(len(near_best) - 1)))
        if len(near_best) == 1:
            shape = "3. ISOLATED PEAK"
            why = f"one value ({near_best[0]}) leads neighbours by ≥ {MATERIAL_R} R"
        elif contiguous:
            shape = "1. BROAD STABLE REGION"
            why = f"adjacent arms {near_best} are within {MATERIAL_R} R of the best"
        else:
            shape = "5. UNSTABLE / CONFLICTED"
            why = "favourable arms are non-adjacent / non-coherent"

    # control assessment (risk-adjusted primary)
    wider = [screened[m]["expectancy_r"] for m in FROZEN_MULTS if m > CONTROL]
    tighter = [screened[m]["expectancy_r"] for m in FROZEN_MULTS if m < CONTROL]
    wider_better = max(wider) - ctrl > MATERIAL_R
    tighter_better = max(tighter) - ctrl > MATERIAL_R
    if shape.startswith(("4", "5")):
        control_r = "reasonable (within a flat band)" if shape.startswith("4") else "indeterminate"
    elif wider_better and not tighter_better:
        control_r = "too tight"
    elif tighter_better and not wider_better:
        control_r = "too wide"
    elif wider_better and tighter_better:
        control_r = "non-convex — indeterminate"
    else:
        control_r = "reasonable"

    # $-space (fixed-share) shape — reported for transparency and attributed to
    # sizing per Part A, NOT used to pick a parameter.
    usd = [screened[m]["net_usd"] for m in FROZEN_MULTS]
    ud = [usd[i + 1] - usd[i] for i in range(len(usd) - 1)]
    usd_monotone_up = all(d > 0 for d in ud[1:])   # from control outward widening
    usd_shape = ("net improves monotonically as the stop widens (fixed-share $)"
                 if usd_monotone_up else "no clean monotone $ trend")
    divergence = (shape.startswith("4")
                  and (max(usd) - min(usd)) > 20)   # R-flat but $-spread material
    usd_ctrl = screened[CONTROL]["net_usd"]
    usd_wider_best = max(screened[m]["net_usd"] for m in FROZEN_MULTS if m > CONTROL)
    control_usd = "too tight" if usd_wider_best - usd_ctrl > 20 else "reasonable"

    return {
        "primary_metric": "expectancy_r (screened) — risk-normalized",
        "screened_expectancy_r_by_mult": dict(zip(map(str, FROZEN_MULTS), xr)),
        "screened_net_usd_by_mult": dict(zip(map(str, FROZEN_MULTS), usd)),
        "spread_r": round(spread, 4),
        "material_r_threshold": MATERIAL_R,
        "raw_screened_arms_disagreeing_on_direction": disagree,
        "long_short_conflict_at_best_arm": bool(ls_conflict),
        "best_arm_by_expectancy_r": best_m,
        "response_shape": shape,
        "shape_rationale": why,
        "usd_space_shape": usd_shape,
        "r_vs_usd_divergence": bool(divergence),
        "divergence_note": ("R-space is FLAT while fixed-share $ improves with a "
                            "wider stop — a POSITION-SIZING artifact (wider stop = "
                            "fewer high-$ stop-outs on high-ATR trades), NOT a "
                            "risk-adjusted edge. See PART A." if divergence else ""),
        "control_1p00_assessment_risk_adjusted": control_r,
        "control_1p00_assessment_fixed_share_usd": control_usd,
        "note": "classification is descriptive; NO production value is selected, "
                "no intermediate multiple is interpolated or tested. The primary "
                "reading is risk-adjusted (R); the $ reading is a sizing artifact.",
    }


def main():
    print("python", platform.python_version(), "| tearsheet stdlib-only")
    drop = set(json.load(open(MASK))["mask_t_ms"])
    print(f"FROZEN ATR_STOP_MULT family (pre-outcome): {FROZEN_MULTS}; control {CONTROL}")

    screened, raw = {}, {}
    for m in FROZEN_MULTS:
        rows_s = fe.compute_feature_rows(9, 20, drop_t_ms=drop)
        rows_r = fe.compute_feature_rows(9, 20)
        screened[m] = arm_summary(fe.simulate(rows_s, atr_stop_mult=m))
        raw[m] = arm_summary(fe.simulate(rows_r, atr_stop_mult=m))
        print(f"  mult {m}: screened n={screened[m]['n']} net=${screened[m]['net_usd']} "
              f"exp_R={screened[m]['expectancy_r']} stops%={screened[m]['stop_out_pct']}")

    cls = classify(screened, raw)
    report = {
        "role": "PARTS B+C — frozen ATR-stop response surface (screened primary, "
                "raw sensitivity); single-factor ATR_STOP_MULT only",
        "python": platform.python_version(),
        "frozen_mults": FROZEN_MULTS, "control": CONTROL,
        "development_window": [fe.DEV_START, fe.DEV_END],
        "budget_accounting": {
            "control_1p00": "existing V0 — no new draw",
            "new_interpreted_configs": [0.75, 1.25, 1.50, 1.75],
            "vdc_dev_before": 3, "vdc_dev_after": 7, "ceiling": 18,
            "multiple_testing": "all four new configs recorded as explored "
                                "candidates; NOT 'one test'. No post-hoc "
                                "interpolation of intermediate multiples.",
        },
        "screened": {str(m): screened[m] for m in FROZEN_MULTS},
        "raw": {str(m): raw[m] for m in FROZEN_MULTS},
        "classification": cls,
    }
    out = os.path.join(HERE, "ATR_STOP_SURFACE_2026-08-26.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)

    # canonical CSV (per arm, both views)
    csv_path = os.path.join(HERE, "ATR_STOP_SURFACE_2026-08-26.csv")
    cols = ["view", "atr_stop_mult", "n", "stop_outs", "stop_out_pct",
            "thesis_exits", "eod_exits", "net_usd", "expectancy_usd",
            "expectancy_r", "median_r", "profit_factor", "win_rate_pct",
            "avg_winner_r", "avg_loser_r", "max_dd_usd", "max_dd_r",
            "avg_bars_held", "long_n", "long_expectancy_r", "long_pf",
            "short_n", "short_expectancy_r", "short_pf"]
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for view, d in (("screened", screened), ("raw", raw)):
            for m in FROZEN_MULTS:
                a = d[m]
                w.writerow([view, m, a["n"], a["stop_outs"], a["stop_out_pct"],
                            a["thesis_exits"], a["eod_exits"], a["net_usd"],
                            a["expectancy_usd"], a["expectancy_r"], a["median_r"],
                            a["profit_factor"], a["win_rate_pct"], a["avg_winner_r"],
                            a["avg_loser_r"], a["max_dd_usd"], a["max_dd_r"],
                            a["avg_bars_held"], a["long"]["n"], a["long"]["expectancy_r"],
                            a["long"]["profit_factor"], a["short"]["n"],
                            a["short"]["expectancy_r"], a["short"]["profit_factor"]])

    print("\n" + "=" * 70)
    print("RESPONSE-SURFACE CLASSIFICATION")
    print("=" * 70)
    print(f"  screened expectancy_r by mult: {cls['screened_expectancy_r_by_mult']}")
    print(f"  spread {cls['spread_r']} R (material threshold {MATERIAL_R})")
    print(f"  raw/screened arms disagreeing: {cls['raw_screened_arms_disagreeing_on_direction']}")
    print(f"  SHAPE (R, primary): {cls['response_shape']} — {cls['shape_rationale']}")
    print(f"  $-space: {cls['usd_space_shape']} | R-vs-$ divergence="
          f"{cls['r_vs_usd_divergence']}")
    print(f"  CONTROL 1.00: risk-adjusted={cls['control_1p00_assessment_risk_adjusted']}; "
          f"fixed-share $={cls['control_1p00_assessment_fixed_share_usd']}")
    print(f"  (best arm by expectancy_r = {cls['best_arm_by_expectancy_r']}; NO "
          "production value selected)")
    print(f"\nwritten: {os.path.relpath(out, STUDY)}, {os.path.relpath(csv_path, STUDY)}")


if __name__ == "__main__":
    main()
