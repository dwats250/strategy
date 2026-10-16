#!/usr/bin/env python3
"""Compact EMA fast/slow response surface — v1.0 · 2026-08-26.

Maps a frozen 3x3 EMA-length grid around the existing V0 control (EMA 9/20),
using naked SYMMETRIC VDC. Only the trading EMA fast/slow lengths change; every
other V0 semantic (session VWAP, ATR14, ATR_STOP_MULT=1.0, opposing-candle
trigger, entry window, stop logic, VWAP thesis exit, EOD, sizing, execution,
costs) is untouched. This is a robustness / local-topology probe, NOT an
optimization: no production pair is selected, no intermediate/neighbouring value
is added after seeing results.

FROZEN GRID (declared before any outcome inspection):
    fast EMA in {8, 9, 10}  x  slow EMA in {18, 20, 22}  = 9 cells
      9/20  = EXISTING CONTROL (V0; no new budget draw)
      10/22 = ALREADY EXPLORED (V0/V1 A/B; no new budget draw)
    The remaining SEVEN cells are new interpreted VDC-development configs
    (8/18, 8/20, 8/22, 9/18, 9/22, 10/18, 10/20): budget 8/18 -> 15/18.

For every cell: screened corpus (frozen CORPUS_MASK_v1.0) is PRIMARY, raw is
sensitivity. Reports the standard tear sheet per cell (trades, cumulative R,
expectancy R, net $, PF, win%, max-DD R, long/short N+expectancy R+PF, a fixed-
seed bootstrap CI in $ and R, outlier concentration) plus raw/screened direction
agreement, then classifies the 3x3 surface topology and the persistence of the
long-positive / short-negative directional asymmetry — WITHOUT ranking by best
cell alone. Development window only; no validation/holdout/embargo; no PVAE, no
sizing/stop/trigger change; no long-only rerun (the secondary long/short question
is answered descriptively from the symmetric decomposition).

Determinism: each cell is simulated twice and the serialized trade lists must be
byte-identical; the whole report is byte-stable across reruns (fixed bootstrap
seed). Run: python3 ema_surface.py
"""

import csv
import json
import os
import platform
import statistics as st

import fastalpha_engine as fe
import parity_foundation as pf
import tearsheet as ts

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")

# ---- FROZEN before any outcome inspection ----
FROZEN_FAST = [8, 9, 10]
FROZEN_SLOW = [18, 20, 22]
CELLS = [(f, s) for f in FROZEN_FAST for s in FROZEN_SLOW]
CONTROL = (9, 20)            # existing V0 — no new budget draw
ALREADY_EXPLORED = (10, 22)  # V0/V1 A/B — no new budget draw
NEW_CELLS = [c for c in CELLS if c not in (CONTROL, ALREADY_EXPLORED)]

# PREDECLARED classification threshold: economic materiality on the risk-
# normalized primary metric (expectancy R / trade). Same value used for the
# frozen ATR-stop surface, chosen there before outcomes and reused unchanged.
MATERIAL_R = 0.03


def _sign(x, eps=1e-12):
    return 0 if abs(x) < eps else (1 if x > 0 else -1)


def _side_r(trades, side):
    s = [t for t in trades if t["side"] == side]
    rs = [t["pnl_r"] for t in s]
    w = sum(x for x in rs if x > 0)
    l = -sum(x for x in rs if x < 0)
    return {"n": len(s),
            "expectancy_r": round(sum(rs) / len(rs), 6) if rs else None,
            "profit_factor": round(w / l, 6) if l > 0 else None,
            "net_r": round(sum(rs), 6)}


def _boot_r_ci(trades, seed=ts.BOOTSTRAP_SEED, B=ts.BOOTSTRAP_B):
    """Bootstrap CI of mean expectancy in R, reusing tearsheet's exact resampling
    code by mapping pnl_r into the 'pnl' slot (identical algorithm, deterministic
    seed) — so the $ and R CIs share one implementation."""
    shim = [{"pnl": t["pnl_r"]} for t in trades]
    b = ts.bootstrap_ci(shim, seed=seed, B=B)
    return {"mean": b.get("mean_expectancy"), "iid_ci95": b.get("iid_ci95"),
            "block_ci95": b.get("block_ci95"), "block_len": b.get("block_len")}


def cell_summary(trades):
    tm = ts.trade_metrics(trades)
    rm = ts.r_metrics(trades)
    re = ts.r_equity(trades)
    eq = ts.equity_series(trades)
    bs = ts.bootstrap_ci(trades)
    oc = ts.outlier_concentration(trades)
    ec = tm["exit_reason_counts"]
    stops = ec["Long ATR Stop"] + ec["Short ATR Stop"]
    n = tm["n"]
    return {
        "n": n,
        "net_usd": tm["net_pnl"],
        "expectancy_usd": tm["expectancy"],
        "cumulative_r": re["cumulative_r"],
        "expectancy_r": rm["mean_r"],
        "median_r": rm["median_r"],
        "profit_factor": tm["profit_factor"],
        "win_rate_pct": tm["win_rate_pct"],
        "max_dd_usd": eq["max_drawdown"],
        "max_dd_r": re["max_drawdown_r"],
        "stop_outs": stops,
        "stop_out_pct": round(100 * stops / n, 3) if n else None,
        "thesis_exits": ec["VWAP Failure"],
        "eod_exits": ec["EOD"],
        "avg_bars_held": tm["avg_bars_held"],
        "long": _side_r(trades, "long"),
        "short": _side_r(trades, "short"),
        "bootstrap_expectancy_usd": {
            "mean": bs["mean_expectancy"], "iid_ci95": bs["iid_ci95"],
            "block_ci95": bs["block_ci95"], "block_len": bs["block_len"]},
        "bootstrap_expectancy_r": _boot_r_ci(trades),
        "outliers": {"best_10_pct_of_gross": oc["best_10"]["pct_of_gross_profit"],
                     "net_excl_best_10": oc["net_excl_best_10"],
                     "best_1_pct_of_gross": oc["best_1"]["pct_of_gross_profit"]},
    }


def _neighbors(cell):
    """Orthogonal grid neighbours (one step in fast OR slow)."""
    f, s = cell
    fi, si = FROZEN_FAST.index(f), FROZEN_SLOW.index(s)
    out = []
    for dfi, dsi in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nf, ns = fi + dfi, si + dsi
        if 0 <= nf < len(FROZEN_FAST) and 0 <= ns < len(FROZEN_SLOW):
            out.append((FROZEN_FAST[nf], FROZEN_SLOW[ns]))
    return out


def _contiguous(cellset):
    """Is a set of cells connected via orthogonal grid adjacency?"""
    if not cellset:
        return True
    cellset = set(cellset)
    seen, stack = set(), [next(iter(cellset))]
    while stack:
        c = stack.pop()
        if c in seen:
            continue
        seen.add(c)
        for nb in _neighbors(c):
            if nb in cellset and nb not in seen:
                stack.append(nb)
    return seen == cellset


def _marginal_monotone(expr, axis):
    """Is the marginal mean expectancy_r monotone (and materially sloped) along
    an axis? axis='fast' averages over slows for each fast; 'slow' vice versa.
    Returns (is_monotone, direction, marginal_spread)."""
    levels = FROZEN_FAST if axis == "fast" else FROZEN_SLOW
    other = FROZEN_SLOW if axis == "fast" else FROZEN_FAST
    means = []
    for lv in levels:
        vals = [expr[(lv, o)] if axis == "fast" else expr[(o, lv)] for o in other]
        means.append(sum(vals) / len(vals))
    diffs = [means[i + 1] - means[i] for i in range(len(means) - 1)]
    spread = max(means) - min(means)
    inc = all(d > 0 for d in diffs)
    dec = all(d < 0 for d in diffs)
    direction = "increasing" if inc else ("decreasing" if dec else "non-monotone")
    return (inc or dec), direction, round(spread, 6), [round(m, 6) for m in means]


def classify(expr_s, expr_r, ls_s, ls_r):
    """Deterministic, predeclared 3x3 topology classification on the SCREENED
    primary view (pooled expectancy_r per cell), cross-checked against raw and
    the long/short decomposition. expr_* map cell->expectancy_r; ls_* map
    cell->(long_expr_r, short_expr_r)."""
    vals = [expr_s[c] for c in CELLS]
    spread = max(vals) - min(vals)
    median = st.median(vals)
    ctrl = expr_s[CONTROL]

    # raw/screened direction agreement per non-control cell (sign of cell-control)
    disagree = []
    for c in CELLS:
        if c == CONTROL:
            continue
        ds = _sign(expr_s[c] - ctrl)
        dr = _sign(expr_r[c] - expr_r[CONTROL])
        if ds != 0 and dr != 0 and ds != dr:
            disagree.append(c)

    # neighbour smoothness
    seen_pairs, njumps = set(), []
    for c in CELLS:
        for nb in _neighbors(c):
            key = tuple(sorted((c, nb)))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            njumps.append(abs(expr_s[c] - expr_s[nb]))
    max_njump = max(njumps)
    mean_njump = sum(njumps) / len(njumps)

    best = max(CELLS, key=lambda c: expr_s[c])
    worst = min(CELLS, key=lambda c: expr_s[c])
    near_best = [c for c in CELLS if (max(vals) - expr_s[c]) < MATERIAL_R]
    near_best_contig = _contiguous(near_best)
    best_isolated = (len(near_best) == 1 and
                     all(expr_s[best] - expr_s[nb] >= MATERIAL_R for nb in _neighbors(best)))
    worst_isolated = (all(expr_s[nb] - expr_s[worst] >= MATERIAL_R for nb in _neighbors(worst))
                      and len([c for c in CELLS if (expr_s[c] - min(vals)) < MATERIAL_R]) == 1)

    mono_f = _marginal_monotone(expr_s, "fast")
    mono_s = _marginal_monotone(expr_s, "slow")

    # --- decision tree (priority order; predeclared) ---
    if len(disagree) >= 4:                       # majority of 8 non-control cells flip
        shape = "6. UNSTABLE / CONFLICTED"
        why = (f"raw and screened disagree on the sign of (cell-control) for "
               f"{len(disagree)} of 8 non-control cells")
    elif spread < MATERIAL_R:
        shape = "5. FLAT / PARAMETER-INSENSITIVE"
        why = f"pooled expectancy_r spread {round(spread,4)} < MATERIAL_R {MATERIAL_R}"
    elif best_isolated:
        # Only an isolated PEAK is the distrust case (one good cell, worse
        # neighbours). An isolated TROUGH (one bad cell, the rest clustered high)
        # is a broad stable region with an outlier and is handled below.
        shape = "4. ISOLATED PEAK/TROUGH"
        why = (f"one cell {best} is an isolated peak: it exceeds every grid "
               f"neighbour by >= {MATERIAL_R} R while the rest lie in a lower band")
    elif (mono_f[0] and mono_s[3] and mono_s[2] < MATERIAL_R) or \
         (mono_s[0] and mono_f[3] and mono_f[2] < MATERIAL_R) or \
         (mono_f[0] and mono_s[0] and mono_f[1] == mono_s[1]):
        # one axis materially monotone with the other flat/aligned -> coherent tilt
        shape = "3. MONOTONIC GRADIENT"
        why = (f"coherent tilt: fast-marginal {mono_f[1]} (spread {mono_f[2]}), "
               f"slow-marginal {mono_s[1]} (spread {mono_s[2]}); best/worst at "
               f"opposite grid regions ({best} vs {worst})")
    elif near_best_contig and len(near_best) >= 6:
        shape = "1. BROAD STABLE REGION"
        why = (f"{len(near_best)} of 9 cells are a contiguous block within "
               f"{MATERIAL_R} R of the best")
    elif near_best_contig and 2 <= len(near_best) <= 5:
        shape = "2. LOCAL PLATEAU"
        why = (f"a contiguous cluster of {len(near_best)} cells {sorted(near_best)} "
               f"sits within {MATERIAL_R} R of the best; the rest are materially lower")
    else:
        shape = "6. UNSTABLE / CONFLICTED"
        why = (f"favourable cells {sorted(near_best)} are non-contiguous / non-coherent "
               f"and no coherent gradient is present")

    # is the control 9/20 inside a stable region?
    ctrl_near_best = (max(vals) - ctrl) < MATERIAL_R
    ctrl_in_stable = ctrl_near_best and CONTROL in near_best and near_best_contig
    # is 10/22's prior NEUTRAL-vs-9/20 result consistent with the surface?
    d_1022 = expr_s[ALREADY_EXPLORED] - ctrl
    consistent_1022 = abs(d_1022) < MATERIAL_R

    # directional asymmetry persistence (screened primary; raw cross-check)
    long_pos_s = sum(1 for c in CELLS if (ls_s[c][0] or 0) > 0)
    short_neg_s = sum(1 for c in CELLS if (ls_s[c][1] or 0) < 0)
    long_pos_r = sum(1 for c in CELLS if (ls_r[c][0] or 0) > 0)
    short_neg_r = sum(1 for c in CELLS if (ls_r[c][1] or 0) < 0)
    if long_pos_s >= 7 and short_neg_s >= 7:
        asymmetry = "PERSISTENT"
    elif long_pos_s <= 3 or short_neg_s <= 3:
        asymmetry = "ABSENT"
    else:
        asymmetry = "MIXED"

    # disposition label from shape
    label = {
        "1. BROAD STABLE REGION": "EMA SURFACE BROADLY ROBUST",
        "2. LOCAL PLATEAU": "EMA SURFACE LOCALLY ROBUST",
        "3. MONOTONIC GRADIENT": "EMA SURFACE LOCALLY ROBUST",  # coherent, no fragile optimum
        "4. ISOLATED PEAK/TROUGH": "EMA SURFACE SHOWS ISOLATED OPTIMUM",
        "5. FLAT / PARAMETER-INSENSITIVE": "EMA SURFACE PARAMETER-INSENSITIVE",
        "6. UNSTABLE / CONFLICTED": "EMA SURFACE UNSTABLE",
    }[shape]

    return {
        "primary_metric": "pooled expectancy_r per cell (screened) — risk-normalized",
        "screened_expectancy_r_by_cell": {f"{f}/{s}": expr_s[(f, s)] for f, s in CELLS},
        "raw_expectancy_r_by_cell": {f"{f}/{s}": expr_r[(f, s)] for f, s in CELLS},
        "range_expectancy_r": round(spread, 6),
        "median_expectancy_r": round(median, 6),
        "material_r_threshold": MATERIAL_R,
        "neighbour_smoothness": {"max_adjacent_jump_r": round(max_njump, 6),
                                 "mean_adjacent_jump_r": round(mean_njump, 6)},
        "fast_marginal": {"direction": mono_f[1], "spread_r": mono_f[2], "means": mono_f[3]},
        "slow_marginal": {"direction": mono_s[1], "spread_r": mono_s[2], "means": mono_s[3]},
        "best_cell": f"{best[0]}/{best[1]}", "worst_cell": f"{worst[0]}/{worst[1]}",
        "best_is_isolated_peak": bool(best_isolated),
        "worst_is_isolated_trough": bool(worst_isolated),
        "cells_within_material_of_best": [f"{f}/{s}" for f, s in near_best],
        "near_best_contiguous": near_best_contig,
        "raw_screened_cells_disagreeing_on_direction": [f"{f}/{s}" for f, s in disagree],
        "response_shape": shape,
        "shape_rationale": why,
        "control_9_20_within_stable_region": bool(ctrl_in_stable),
        "control_9_20_gap_below_best_r": round(max(vals) - ctrl, 6),
        "ema_10_22_consistent_with_surface": bool(consistent_1022),
        "ema_10_22_delta_vs_control_r": round(d_1022, 6),
        "directional_asymmetry": {
            "screened_cells_long_expectancy_positive": f"{long_pos_s}/9",
            "screened_cells_short_expectancy_negative": f"{short_neg_s}/9",
            "raw_cells_long_expectancy_positive": f"{long_pos_r}/9",
            "raw_cells_short_expectancy_negative": f"{short_neg_r}/9",
            "verdict": asymmetry,
        },
        "disposition_label": label,
        "note": "descriptive topology only; NO production EMA pair selected, no "
                "intermediate/neighbouring value interpolated or tested. A single "
                "best cell whose neighbours are materially worse is treated as an "
                "isolated (distrusted) optimum, not a recommendation.",
    }


def run_cell(fast, slow, drop):
    rows_s = fe.compute_feature_rows(fast, slow, drop_t_ms=drop)
    rows_r = fe.compute_feature_rows(fast, slow)
    tr_s = fe.simulate(rows_s)
    tr_r = fe.simulate(rows_r)
    # determinism: re-simulate and require byte-identical serialization
    if json.dumps(tr_s) != json.dumps(fe.simulate(fe.compute_feature_rows(fast, slow, drop_t_ms=drop))):
        raise SystemExit(f"DETERMINISM FAILURE (screened) EMA {fast}/{slow}")
    if json.dumps(tr_r) != json.dumps(fe.simulate(fe.compute_feature_rows(fast, slow))):
        raise SystemExit(f"DETERMINISM FAILURE (raw) EMA {fast}/{slow}")
    return cell_summary(tr_s), cell_summary(tr_r)


def main():
    print("python", platform.python_version(), "| tearsheet stdlib-only")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    drop = set(json.load(open(MASK))["mask_t_ms"])
    print(f"FROZEN EMA grid (pre-outcome): fast {FROZEN_FAST} x slow {FROZEN_SLOW}; "
          f"control {CONTROL[0]}/{CONTROL[1]}")

    screened, raw = {}, {}
    for (f, s) in CELLS:
        screened[(f, s)], raw[(f, s)] = run_cell(f, s, drop)
        cs = screened[(f, s)]
        tag = " [CONTROL]" if (f, s) == CONTROL else (
            " [EXPLORED]" if (f, s) == ALREADY_EXPLORED else "")
        print(f"  EMA {f}/{s}{tag}: screened n={cs['n']} net=${cs['net_usd']} "
              f"cumR={cs['cumulative_r']} expR={cs['expectancy_r']} PF={cs['profit_factor']}")

    expr_s = {c: screened[c]["expectancy_r"] for c in CELLS}
    expr_r = {c: raw[c]["expectancy_r"] for c in CELLS}
    ls_s = {c: (screened[c]["long"]["expectancy_r"], screened[c]["short"]["expectancy_r"]) for c in CELLS}
    ls_r = {c: (raw[c]["long"]["expectancy_r"], raw[c]["short"]["expectancy_r"]) for c in CELLS}
    cls = classify(expr_s, expr_r, ls_s, ls_r)

    report = {
        "role": "Compact EMA fast/slow response surface (3x3), naked symmetric VDC; "
                "screened primary, raw sensitivity; robustness/topology, not optimization",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "engine": {"mintick": fe.MINTICK, "slippage_ticks": fe.SLIPPAGE_TICKS,
                   "atr_stop_mult": 1.0, "dev_window": [fe.DEV_START, fe.DEV_END]},
        "frozen_grid": {"fast": FROZEN_FAST, "slow": FROZEN_SLOW,
                        "control": f"{CONTROL[0]}/{CONTROL[1]}",
                        "already_explored": f"{ALREADY_EXPLORED[0]}/{ALREADY_EXPLORED[1]}"},
        "determinism": "PASS (each cell byte-identical across re-simulation)",
        "budget_accounting": {
            "control_9_20": "existing V0 — no new draw",
            "already_explored_10_22": "V0/V1 A/B — no new draw",
            "new_interpreted_configs": [f"{f}/{s}" for f, s in NEW_CELLS],
            "vdc_dev_before": 8, "vdc_dev_after": 15, "ceiling": 18,
            "multiple_testing": "all seven new cells recorded individually as "
                                "explored candidates; NOT 'one test'. No post-hoc "
                                "interpolation of 7/17, 11/24, intermediate lengths.",
        },
        "screened": {f"{f}/{s}": screened[(f, s)] for f, s in CELLS},
        "raw": {f"{f}/{s}": raw[(f, s)] for f, s in CELLS},
        "classification": cls,
    }
    out = os.path.join(HERE, "EMA_SURFACE_2026-08-26.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)

    # canonical CSV (per cell, both views)
    csv_path = os.path.join(HERE, "EMA_SURFACE_2026-08-26.csv")
    cols = ["view", "fast", "slow", "n", "net_usd", "expectancy_usd", "cumulative_r",
            "expectancy_r", "median_r", "profit_factor", "win_rate_pct", "max_dd_usd",
            "max_dd_r", "stop_out_pct", "thesis_exits", "eod_exits", "avg_bars_held",
            "long_n", "long_expectancy_r", "long_pf", "short_n", "short_expectancy_r",
            "short_pf", "boot_expR_lo", "boot_expR_hi", "best_10_pct_of_gross"]
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for view, d in (("screened", screened), ("raw", raw)):
            for (f, s) in CELLS:
                a = d[(f, s)]
                br = a["bootstrap_expectancy_r"]["block_ci95"]
                w.writerow([view, f, s, a["n"], a["net_usd"], a["expectancy_usd"],
                            a["cumulative_r"], a["expectancy_r"], a["median_r"],
                            a["profit_factor"], a["win_rate_pct"], a["max_dd_usd"],
                            a["max_dd_r"], a["stop_out_pct"], a["thesis_exits"],
                            a["eod_exits"], a["avg_bars_held"], a["long"]["n"],
                            a["long"]["expectancy_r"], a["long"]["profit_factor"],
                            a["short"]["n"], a["short"]["expectancy_r"],
                            a["short"]["profit_factor"], br[0], br[1],
                            a["outliers"]["best_10_pct_of_gross"]])

    print("\n" + "=" * 72)
    print("EMA SURFACE — TOPOLOGY CLASSIFICATION (screened primary, expectancy R)")
    print("=" * 72)
    print(f"  expectancy_r by cell: {cls['screened_expectancy_r_by_cell']}")
    print(f"  range {cls['range_expectancy_r']} R | median {cls['median_expectancy_r']} R "
          f"| material {MATERIAL_R} R")
    print(f"  max adjacent-cell jump {cls['neighbour_smoothness']['max_adjacent_jump_r']} R")
    print(f"  fast-marginal {cls['fast_marginal']['direction']} "
          f"(spread {cls['fast_marginal']['spread_r']}); "
          f"slow-marginal {cls['slow_marginal']['direction']} "
          f"(spread {cls['slow_marginal']['spread_r']})")
    print(f"  raw/screened cells disagreeing on direction: "
          f"{cls['raw_screened_cells_disagreeing_on_direction'] or 'none'}")
    print(f"  SHAPE: {cls['response_shape']} — {cls['shape_rationale']}")
    print(f"  control 9/20 within stable region: {cls['control_9_20_within_stable_region']} "
          f"(gap below best {cls['control_9_20_gap_below_best_r']} R)")
    print(f"  10/22 consistent with surface: {cls['ema_10_22_consistent_with_surface']} "
          f"(delta vs control {cls['ema_10_22_delta_vs_control_r']} R)")
    da = cls["directional_asymmetry"]
    print(f"  directional asymmetry: long+ {da['screened_cells_long_expectancy_positive']}, "
          f"short- {da['screened_cells_short_expectancy_negative']} "
          f"(raw {da['raw_cells_long_expectancy_positive']}/"
          f"{da['raw_cells_short_expectancy_negative']}) => {da['verdict']}")
    print(f"\n  DISPOSITION: {cls['disposition_label']}; ASYMMETRY {da['verdict']}")
    print(f"  (best cell {cls['best_cell']}, worst {cls['worst_cell']}; "
          "NO production pair selected)")
    print(f"\nwritten: {os.path.relpath(out, STUDY)}, {os.path.relpath(csv_path, STUDY)}")


if __name__ == "__main__":
    main()
