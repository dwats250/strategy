#!/usr/bin/env python3
"""FPC-0 first development run — v1.0 · 2026-08-27.

Runs the FIRST FPC development configuration (FPC-0 symmetric, signal_mode="fpc",
EMA 9/20, ATR stop 1.0) over the development window 2024-09-03 .. 2025-12-31, with
the retired VDC symmetric V0 as the benchmark/research control, on the same engine
and corpus. Screened (frozen CORPUS_MASK_v1.0) is primary; raw is sensitivity.

FPC-0 differs from VDC ONLY in entry geometry (first opposing-color pullback per
FRESH VWAP/EMA regime, one entry per continuous regime) — every other semantic is
V0. This is DEVELOPMENT, not confirmation; the classification below is frozen BEFORE
any outcome is accessed (predeclared constants + manifest RUN_FPC0_DEV_v1.0.md), and
no production configuration is selected. No validation/holdout/fresh-window data is
touched. Run: python3 fpc0_dev.py
"""

import json
import os
import platform

import fastalpha_engine as fe
import parity_foundation as pf
import tearsheet as ts

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")

# ---- FROZEN classification (predeclared, before outcome access) ----
MATERIAL_R = 0.03            # existing convention
# delta_R = FPC mean expectancy R - VDC mean expectancy R
#   BETTER    : screened delta_R > +MATERIAL_R AND raw delta_R > 0
#   WORSE     : screened delta_R < -MATERIAL_R AND raw delta_R < 0
#   NEUTRAL   : screened delta_R in [-MATERIAL_R, +MATERIAL_R]
#   CONFLICTED: screened material move but raw opposite direction


def _side_r(trades, side):
    s = [t for t in trades if t["side"] == side]
    rs = [t["pnl_r"] for t in s]
    w = sum(x for x in rs if x > 0)
    l = -sum(x for x in rs if x < 0)
    return {"n": len(s),
            "expectancy_r": round(sum(rs) / len(rs), 6) if rs else None,
            "profit_factor": round(w / l, 6) if l > 0 else None,
            "net_r": round(sum(rs), 6)}


def _boot_r(trades):
    b = ts.bootstrap_ci([{"pnl": t["pnl_r"]} for t in trades])
    return {"mean": b.get("mean_expectancy"), "iid_ci95": b.get("iid_ci95"),
            "block_ci95": b.get("block_ci95"), "block_len": b.get("block_len")}


def arm_report(trades):
    tm = ts.trade_metrics(trades)
    rm = ts.r_metrics(trades)
    re = ts.r_equity(trades)
    eq = ts.equity_series(trades)
    bs = ts.bootstrap_ci(trades)
    oc = ts.outlier_concentration(trades)
    dist = ts.distribution(trades)
    ec = tm["exit_reason_counts"]
    return {
        "n": tm["n"],
        "net_usd": tm["net_pnl"],
        "expectancy_usd": tm["expectancy"],
        "cumulative_r": re["cumulative_r"],
        "expectancy_r": rm["mean_r"],
        "median_r": rm["median_r"],
        "profit_factor": tm["profit_factor"],
        "win_rate_pct": tm["win_rate_pct"],
        "max_dd_usd": eq["max_drawdown"],
        "max_dd_r": re["max_drawdown_r"],
        "avg_bars_held": tm["avg_bars_held"],
        "median_bars_held": tm["median_bars_held"],
        "exit_reason_counts": ec,
        "long": _side_r(trades, "long"),
        "short": _side_r(trades, "short"),
        "bootstrap_expectancy_usd": {"mean": bs["mean_expectancy"],
                                     "iid_ci95": bs["iid_ci95"],
                                     "block_ci95": bs["block_ci95"]},
        "bootstrap_expectancy_r": _boot_r(trades),
        "monthly": {"n_months": dist.get("n_months"),
                    "profitable_months": dist.get("profitable_months"),
                    "pct_profitable_months": dist.get("pct_profitable_months")},
        "outliers": {"best_10_pct_of_gross": oc["best_10"]["pct_of_gross_profit"],
                     "net_excl_best_10": oc["net_excl_best_10"],
                     "best_1_pct_of_gross": oc["best_1"]["pct_of_gross_profit"]},
    }


def _hhmm(et_start_iso):
    d, t = et_start_iso.split("T")
    return f"{d} {t[:5]}"


def regime_scan(bars):
    """Analysis-only: continuous bullish/bearish regimes over the windowed bars,
    using the precomputed bullish_state/bearish_state (same definitions the engine
    reads). Returns (bull_regimes, bear_regimes, et2idx). Each regime is
    {start_idx, start_et, indices:set}. Fresh at i == state[i] and not state[i-1]
    (state[-1]=False), matching the engine's prev_* init."""
    n = len(bars)
    et2idx = {_hhmm(b["et_start"]): i for i, b in enumerate(bars)}

    def scan(field):
        st = [bool(b.get(field)) for b in bars]
        regimes, cur = [], None
        for i in range(n):
            fresh = st[i] and not (st[i - 1] if i > 0 else False)
            if fresh:
                cur = {"start_idx": i, "start_et": _hhmm(bars[i]["et_start"]),
                       "indices": {i}}
                regimes.append(cur)
            elif st[i] and cur is not None:
                cur["indices"].add(i)
            else:
                cur = None
        return regimes
    return scan("bullish_state"), scan("bearish_state"), et2idx


def entry_geometry(bars, fpc_trades):
    """Descriptive regime/entry statistics + mechanical FPC invariants on the REAL
    dev run. Raises on any invariant breach."""
    bull_regimes, bear_regimes, et2idx = regime_scan(bars)

    def side_geo(regimes, side):
        starts = {r["start_idx"] for r in regimes}
        # map each regime to the fpc trades whose signal_bar sits inside it
        per_regime = {id(r): [] for r in regimes}
        idx_to_regime = {}
        for r in regimes:
            for i in r["indices"]:
                idx_to_regime[i] = r
        offsets = []
        for t in fpc_trades:
            if t["side"] != side:
                continue
            si = et2idx[t["signal_bar"]]
            # INVARIANT: signal bar cannot be a fresh-regime start bar
            assert si not in starts, \
                f"FPC {side} signal on a fresh-regime bar: {t['signal_bar']}"
            r = idx_to_regime.get(si)
            assert r is not None, \
                f"FPC {side} signal outside any continuous regime: {t['signal_bar']}"
            per_regime[id(r)].append(si)
            offsets.append(si - r["start_idx"])
        # INVARIANT: at most one FPC signal per continuous regime
        for rid, sigs in per_regime.items():
            assert len(sigs) <= 1, f"more than one FPC {side} signal in a regime: {sigs}"
        n_with_signal = sum(1 for sigs in per_regime.values() if sigs)
        # offset distribution (bars from fresh start to signal)
        hist = {}
        for o in offsets:
            hist[o] = hist.get(o, 0) + 1
        return {"n_regimes": len(regimes), "n_with_signal": n_with_signal,
                "signal_rate_pct": round(100 * n_with_signal / len(regimes), 3)
                if regimes else None,
                "bars_from_fresh_to_signal_hist": dict(sorted(hist.items())),
                "min_offset": min(offsets) if offsets else None,
                "max_offset": max(offsets) if offsets else None,
                "median_offset": (sorted(offsets)[len(offsets) // 2]
                                  if offsets else None)}
    return {"long": side_geo(bull_regimes, "long"),
            "short": side_geo(bear_regimes, "short"),
            "invariants_verified": [
                "<=1 FPC signal per continuous regime (asserted from trades)",
                "no FPC signal on a fresh-regime start bar (asserted)",
                "unit tests test_fpc_signals.py cover regime-break disarm, "
                "entry disarm, out-of-window non-consumption, non-flat "
                "non-consumption, and re-arm"]}


def entry_diff(vdc, fpc):
    ev = {(t["entry_bar"], t["side"]) for t in vdc}
    ef = {(t["entry_bar"], t["side"]) for t in fpc}
    retained = ev & ef
    return {"vdc_entries": len(ev), "fpc_entries": len(ef),
            "retained": len(retained),
            "dropped_from_vdc": len(ev - ef),
            "unique_to_fpc": len(ef - ev),
            "pct_vdc_retained": round(100 * len(retained) / len(ev), 3) if ev else None,
            "pct_vdc_suppressed": round(100 * len(ev - ef) / len(ev), 3) if ev else None}


def classify(ds, dr):
    if -MATERIAL_R <= ds <= MATERIAL_R:
        return "FPC DEVELOPMENT NEUTRAL"
    if ds > MATERIAL_R:
        return "FPC DEVELOPMENT BETTER" if dr > 0 else "FPC DEVELOPMENT CONFLICTED"
    return "FPC DEVELOPMENT WORSE" if dr < 0 else "FPC DEVELOPMENT CONFLICTED"


def main():
    print("python", platform.python_version(), "| FPC-0 development run")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    drop = set(json.load(open(MASK))["mask_t_ms"])

    rows_s = fe.compute_feature_rows(9, 20, drop_t_ms=drop)
    rows_r = fe.compute_feature_rows(9, 20)
    win_s = [r for r in rows_s if fe.DEV_START <= r["session_date"] <= fe.DEV_END]
    win_r = [r for r in rows_r if fe.DEV_START <= r["session_date"] <= fe.DEV_END]

    vdc_s = fe.simulate(rows_s, signal_mode="vdc")
    fpc_s = fe.simulate(rows_s, signal_mode="fpc")
    vdc_r = fe.simulate(rows_r, signal_mode="vdc")
    fpc_r = fe.simulate(rows_r, signal_mode="fpc")
    # determinism
    for name, rows, mode, ref in (("vdc_s", rows_s, "vdc", vdc_s),
                                  ("fpc_s", rows_s, "fpc", fpc_s),
                                  ("vdc_r", rows_r, "vdc", vdc_r),
                                  ("fpc_r", rows_r, "fpc", fpc_r)):
        if json.dumps(fe.simulate(rows, signal_mode=mode)) != json.dumps(ref):
            raise SystemExit(f"DETERMINISM FAILURE: {name}")

    rep = {"vdc_screened": arm_report(vdc_s), "fpc_screened": arm_report(fpc_s),
           "vdc_raw": arm_report(vdc_r), "fpc_raw": arm_report(fpc_r)}
    ds = round(rep["fpc_screened"]["expectancy_r"] - rep["vdc_screened"]["expectancy_r"], 6)
    dr = round(rep["fpc_raw"]["expectancy_r"] - rep["vdc_raw"]["expectancy_r"], 6)
    verdict = classify(ds, dr)
    raw_agrees = (ds == 0 and dr == 0) or (ds > 0 and dr > 0) or (ds < 0 and dr < 0)

    geo_s = entry_geometry(win_s, fpc_s)
    geo_r = entry_geometry(win_r, fpc_r)
    diff_s = entry_diff(vdc_s, fpc_s)
    diff_r = entry_diff(vdc_r, fpc_r)
    abd = ts.ab_dual(vdc_s, fpc_s, vdc_r, fpc_r, label="VDC(control) vs FPC-0(variant)")

    report = {
        "role": "FPC-0 first development run — symmetric FPC vs VDC benchmark, "
                "screened primary + raw sensitivity; DEVELOPMENT ONLY",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "development_window": [fe.DEV_START, fe.DEV_END],
        "engine": {"mintick": fe.MINTICK, "slippage_ticks": fe.SLIPPAGE_TICKS,
                   "atr_stop_mult": 1.0, "ema": [9, 20]},
        "determinism": "PASS (each arm byte-identical across re-simulation)",
        "frozen_classification": {"material_r": MATERIAL_R,
            "rule": "delta_R=FPC-VDC mean expectancy R; BETTER if screened>+0.03 & "
                    "raw>0; WORSE if screened<-0.03 & raw<0; NEUTRAL if screened in "
                    "[-0.03,+0.03]; CONFLICTED if screened material but raw opposite"},
        "budget": {"family": "FPC", "config": "FPC-0", "fpc_dev_before": 0,
                   "fpc_dev_after": 1, "ceiling": 12,
                   "note": "independent of the retired VDC 18-slot budget"},
        "primary": {
            "vdc_expectancy_r_screened": rep["vdc_screened"]["expectancy_r"],
            "fpc_expectancy_r_screened": rep["fpc_screened"]["expectancy_r"],
            "delta_expectancy_r_screened": ds,
            "vdc_expectancy_r_raw": rep["vdc_raw"]["expectancy_r"],
            "fpc_expectancy_r_raw": rep["fpc_raw"]["expectancy_r"],
            "delta_expectancy_r_raw": dr,
            "raw_screened_agree_on_direction": bool(raw_agrees),
            "fpc_absolute_expectancy_r_screened": rep["fpc_screened"]["expectancy_r"],
            "classification": verdict,
            "absolute_edge_note": "a relative improvement from negative to "
                                  "less-negative is NOT a positive edge; read the "
                                  "FPC absolute expectancy R.",
        },
        "arms": rep,
        "entry_diff": {"screened": diff_s, "raw": diff_r},
        "entry_geometry": {"screened": geo_s, "raw": geo_r},
        "ab_dual": abd,
    }
    out = os.path.join(HERE, "FPC0_DEV_2026-08-27.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)

    print("\n" + "=" * 72)
    print("FPC-0 DEVELOPMENT — VDC benchmark vs FPC-0 (screened primary, expectancy R)")
    print("=" * 72)
    for k in ("vdc_screened", "fpc_screened", "vdc_raw", "fpc_raw"):
        a = rep[k]
        print(f"  {k:12} n={a['n']:5} expR={a['expectancy_r']:+.5f} cumR={a['cumulative_r']:+.2f} "
              f"net=${a['net_usd']:+.2f} PF={a['profit_factor']} win%={a['win_rate_pct']} "
              f"ddR={a['max_dd_r']}")
    print(f"  delta_R screened {ds:+.5f} | raw {dr:+.5f} | raw agrees {raw_agrees}")
    print(f"  FPC absolute expR (screened) {rep['fpc_screened']['expectancy_r']:+.5f} "
          f"(long {rep['fpc_screened']['long']['expectancy_r']}, "
          f"short {rep['fpc_screened']['short']['expectancy_r']})")
    print(f"  entries: VDC {diff_s['vdc_entries']} -> FPC {diff_s['fpc_entries']} "
          f"(retained {diff_s['pct_vdc_retained']}%, suppressed {diff_s['pct_vdc_suppressed']}%, "
          f"unique-to-FPC {diff_s['unique_to_fpc']})")
    print(f"  bull regimes {geo_s['long']['n_regimes']} ({geo_s['long']['n_with_signal']} signalled), "
          f"bear regimes {geo_s['short']['n_regimes']} ({geo_s['short']['n_with_signal']} signalled)")
    print(f"\n  CLASSIFICATION: {verdict}")
    print(f"\nwritten: {os.path.relpath(out, STUDY)}")


if __name__ == "__main__":
    main()
