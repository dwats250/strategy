#!/usr/bin/env python3
"""Long-only single-look VALIDATION — v1.0 · 2026-08-26.

THE ONE pre-registered validation look at the long-only hypothesis (owner/HELM
charge 2026-08-26). Control = V0 symmetric; variant = V0 long-only (short entries
disabled). Both are RERUN through the frozen engine over the VALIDATION window
2026-01-06 .. 2026-04-30 — NOT derived by filtering symmetric trades. Primary
metric: mean trade expectancy in R (1R = frozen initial entry-to-stop). Screened
(frozen CORPUS_MASK_v1.0) is primary; raw is sensitivity. No parameter is changed;
no rescue.

FIREWALL / holdout hygiene. The verified corpus spans 2024-09-03 .. 2026-08-21 —
it extends PAST the validation window into the frozen-forward holdout and the
late-May..Aug hypothesis-source region. EMA/ATR/VWAP are strictly CAUSAL (a bar's
feature depends only on bars at or before it; session VWAP resets per session), so
truncating the 1m stream at 2026-04-30 BEFORE any 5m aggregation yields feature
values for every in-window bar that are identical to a full-corpus computation,
while guaranteeing that NO bar after the validation window ever enters the
indicator or trade path. This is done here, in the validation script, WITHOUT any
engine change. `simulate` additionally windows trades to [2026-01-06, 2026-04-30].

Success criteria and the strength classification are frozen in
`manifests/RUN_LONG_ONLY_VALIDATION_v1.0.md` and reproduced in `classify()` below;
they were fixed before this script was run on any validation data.

Determinism: each arm is simulated twice and the serialized trade lists must be
byte-identical. Run: python3 long_only_validation.py
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

VAL_START = "2026-01-06"   # first session AFTER the 2026-01-02 + 2026-01-05 embargo
VAL_END = "2026-04-30"     # single planned validation look; holdout begins after


def capped_feature_rows(fast, slow, drop_t_ms=None, end_cap=VAL_END):
    """Mirror of fastalpha_engine.compute_feature_rows but with a FIREWALL end
    cap: the RTH 1m stream is truncated to session_date <= end_cap before 5m
    aggregation, so no bar after the validation window enters the indicator or
    trade path. Causal features => identical in-window values. No engine change."""
    save_fast, save_slow = pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN
    try:
        pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN = fast, slow
        rth = pf.load_corpus_rth()                       # hash-verified (integrity)
        rth = [r for r in rth if r["et_iso"][:10] <= end_cap]   # firewall cap
        if drop_t_ms:
            drop = {str(x) for x in drop_t_ms}
            rth = [r for r in rth if r["t_ms"] not in drop]
        rows = pf.compute_features(pf.build_5m_bars(rth))
    finally:
        pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN = save_fast, save_slow
    return rows


def arm(rows, enable_shorts):
    return fe.simulate(rows, dev_start=VAL_START, dev_end=VAL_END,
                       enable_shorts=enable_shorts)


def mean_r(trades):
    rs = [t["pnl_r"] for t in trades if t.get("pnl_r") is not None]
    return sum(rs) / len(rs) if rs else None


def short_mean_r(trades):
    rs = [t["pnl_r"] for t in trades if t["side"] == "short"]
    return sum(rs) / len(rs) if rs else None


def boot_r_block_ci(trades):
    """Moving-block bootstrap 95% CI of mean expectancy in R (serial-dependence-
    aware; the CI that decides STRONG vs DIRECTIONAL, frozen in the manifest).
    Reuses tearsheet's exact resampling via the pnl_r shim."""
    shim = [{"pnl": t["pnl_r"]} for t in trades]
    b = ts.bootstrap_ci(shim)
    return {"block_ci95": b.get("block_ci95"), "iid_ci95": b.get("iid_ci95"),
            "block_len": b.get("block_len"), "mean": b.get("mean_expectancy"),
            "n": b.get("n")}


def arm_report(trades):
    tm = ts.trade_metrics(trades)
    rm = ts.r_metrics(trades)
    re = ts.r_equity(trades)
    oc = ts.outlier_concentration(trades)
    dist = ts.distribution(trades)
    ec = tm["exit_reason_counts"]
    monthly = {m: v["pnl"] for m, v in dist.get("monthly", {}).items()} if tm["n"] else {}
    return {
        "n": tm["n"],
        "expectancy_r": rm.get("mean_r"),
        "cumulative_r": re.get("cumulative_r"),
        "net_usd": tm.get("net_pnl"),
        "profit_factor": tm.get("profit_factor"),
        "win_rate_pct": tm.get("win_rate_pct"),
        "max_dd_r": re.get("max_drawdown_r"),
        "short_expectancy_r": short_mean_r(trades),
        "long_expectancy_r": mean_r([t for t in trades if t["side"] == "long"]),
        "exit_reason_counts": ec,
        "monthly_pnl_usd": monthly,
        "profitable_months": dist.get("profitable_months"),
        "n_months": dist.get("n_months"),
        "outliers": {"best_1": oc.get("best_1"), "best_5": oc.get("best_5"),
                     "best_10": oc.get("best_10"),
                     "net_excl_best_1": oc.get("net_excl_best_1"),
                     "net_excl_best_5": oc.get("net_excl_best_5"),
                     "net_excl_best_10": oc.get("net_excl_best_10")},
    }


def path_difference(symmetric, long_only):
    """Compare the symmetric control's LONG book to the long-only rerun."""
    sym_long = {t["entry_bar"]: t for t in symmetric if t["side"] == "long"}
    lo = {t["entry_bar"]: t for t in long_only}   # variant is all long
    sset, lset = set(sym_long), set(lo)
    inter = sset & lset
    changed = sum(1 for k in inter
                  if (sym_long[k]["exit_bar"], sym_long[k]["exit_reason"], sym_long[k]["pnl"])
                  != (lo[k]["exit_bar"], lo[k]["exit_reason"], lo[k]["pnl"]))
    union = sset | lset
    return {
        "symmetric_long_entries": len(sset),
        "long_only_entries": len(lset),
        "retained_identical_exit": len(inter) - changed,
        "changed_exit_same_entry": changed,
        "path_created_long_entries": len(lset - sset),
        "lost_symmetric_longs": len(sset - lset),
        "long_entry_jaccard": round(len(inter) / len(union), 6) if union else None,
    }


def classify(lo_s, sym_s, lo_r, sym_r, lo_block_ci_lower):
    """FROZEN pre-registered decision (mirrors the manifest). Screened primary
    A/B/C; raw must agree on SIGN; block-bootstrap lower bound decides strength."""
    def sgn(x):
        return 0 if x is None else (1 if x > 0 else (-1 if x < 0 else 0))
    # screened primary conditions
    A = lo_s["expectancy_r"] is not None and lo_s["expectancy_r"] > 0
    B = (lo_s["expectancy_r"] is not None and sym_s["expectancy_r"] is not None
         and lo_s["expectancy_r"] > sym_s["expectancy_r"])
    C = sym_s["short_expectancy_r"] is not None and sym_s["short_expectancy_r"] < 0
    screened_pass = A and B and C
    # raw sign agreement on the three required conditions
    aS, aR = sgn(lo_s["expectancy_r"]), sgn(lo_r["expectancy_r"])
    bS = sgn((lo_s["expectancy_r"] or 0) - (sym_s["expectancy_r"] or 0))
    bR = sgn((lo_r["expectancy_r"] or 0) - (sym_r["expectancy_r"] or 0))
    cS, cR = sgn(sym_s["short_expectancy_r"]), sgn(sym_r["short_expectancy_r"])
    raw_agrees = (aS == aR and bS == bR and cS == cR)

    if not screened_pass:
        verdict = "FAILS VALIDATION"
    elif not raw_agrees:
        verdict = "CONFLICTED VALIDATION"
    elif lo_block_ci_lower is not None and lo_block_ci_lower > 0:
        verdict = "STRONG CONFIRMATION"
    else:
        verdict = "DIRECTIONAL REPLICATION"
    return {
        "A_long_only_expectancy_r_gt_0": bool(A),
        "B_long_only_gt_symmetric_expectancy_r": bool(B),
        "C_symmetric_short_expectancy_r_lt_0": bool(C),
        "screened_ABC_pass": bool(screened_pass),
        "raw_sign_agreement_ABC": bool(raw_agrees),
        "long_only_block_ci95_lower": lo_block_ci_lower,
        "verdict": verdict,
    }


def main():
    print("python", platform.python_version(), "| tearsheet stdlib-only")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    print(f"VALIDATION window {VAL_START}..{VAL_END} (single look); "
          f"firewall end-cap at {VAL_END}")
    drop = set(json.load(open(MASK))["mask_t_ms"])

    rows_s = capped_feature_rows(9, 20, drop_t_ms=drop)
    rows_r = capped_feature_rows(9, 20)
    sym_s, lo_s = arm(rows_s, True), arm(rows_s, False)
    sym_r, lo_r = arm(rows_r, True), arm(rows_r, False)
    # determinism
    for name, rows, es, ref in (("sym_s", rows_s, True, sym_s),
                                ("lo_s", rows_s, False, lo_s),
                                ("sym_r", rows_r, True, sym_r),
                                ("lo_r", rows_r, False, lo_r)):
        if json.dumps(arm(rows, es)) != json.dumps(ref):
            raise SystemExit(f"DETERMINISM FAILURE: {name}")

    screened_equals_raw = (json.dumps(sym_s) == json.dumps(sym_r)
                           and json.dumps(lo_s) == json.dumps(lo_r))

    rep_sym_s, rep_lo_s = arm_report(sym_s), arm_report(lo_s)
    rep_sym_r, rep_lo_r = arm_report(sym_r), arm_report(lo_r)
    lo_ci = boot_r_block_ci(lo_s)
    lo_block_lower = lo_ci["block_ci95"][0] if lo_ci.get("block_ci95") else None
    lo_ci_raw = boot_r_block_ci(lo_r)

    cls = classify(rep_lo_s, rep_sym_s, rep_lo_r, rep_sym_r, lo_block_lower)
    path_s = path_difference(sym_s, lo_s)
    path_r = path_difference(sym_r, lo_r)

    report = {
        "role": "Long-only SINGLE-LOOK validation (2026-01-06..2026-04-30); "
                "control symmetric V0 vs variant long-only, both rerun through the "
                "frozen engine; screened primary, raw sensitivity",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "validation_window": [VAL_START, VAL_END],
        "firewall_end_cap": VAL_END,
        "engine": {"mintick": fe.MINTICK, "slippage_ticks": fe.SLIPPAGE_TICKS,
                   "atr_stop_mult": 1.0, "ema": [9, 20]},
        "determinism": "PASS (each arm byte-identical across re-simulation)",
        "screened_equals_raw_in_window": screened_equals_raw,
        "screened_equals_raw_note": ("the frozen dev-derived CORPUS_MASK_v1.0 flags "
            "0 bars inside the validation window, so screened and raw coincide "
            "in-window; raw sign-agreement therefore holds by construction and the "
            "block-bootstrap CI is the operative discriminator. Disclosed "
            "pre-outcome in the manifest."),
        "primary": {
            "symmetric_expectancy_r": rep_sym_s["expectancy_r"],
            "long_only_expectancy_r": rep_lo_s["expectancy_r"],
            "delta_expectancy_r": (round(rep_lo_s["expectancy_r"] - rep_sym_s["expectancy_r"], 6)
                                   if rep_lo_s["expectancy_r"] is not None
                                   and rep_sym_s["expectancy_r"] is not None else None),
            "symmetric_short_expectancy_r": rep_sym_s["short_expectancy_r"],
            "long_only_block_ci95_r": lo_ci["block_ci95"],
            "long_only_iid_ci95_r": lo_ci["iid_ci95"],
            "classification": cls,
        },
        "screened": {"symmetric": rep_sym_s, "long_only": rep_lo_s,
                     "long_only_bootstrap_r": lo_ci, "path_difference": path_s},
        "raw": {"symmetric": rep_sym_r, "long_only": rep_lo_r,
                "long_only_bootstrap_r": lo_ci_raw, "path_difference": path_r},
        "outlier_rule": "best-1/5/10 removal is DESCRIPTIVE robustness only, NOT a "
                        "validation gate (frozen in the manifest).",
        "no_rescue": "single look; no parameter/EMA/stop/filter/slice change after "
                     "this run regardless of outcome.",
    }
    out = os.path.join(HERE, "LONG_ONLY_VALIDATION_2026-08-26.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)

    print("\n" + "=" * 72)
    print("LONG-ONLY VALIDATION — PRIMARY (screened)")
    print("=" * 72)
    print(f"  symmetric expectancy R  {rep_sym_s['expectancy_r']}")
    print(f"  long-only expectancy R  {rep_lo_s['expectancy_r']}  "
          f"(delta {report['primary']['delta_expectancy_r']})")
    print(f"  symmetric SHORT expectancy R  {rep_sym_s['short_expectancy_r']}")
    print(f"  A (LO>0): {cls['A_long_only_expectancy_r_gt_0']}  "
          f"B (LO>sym): {cls['B_long_only_gt_symmetric_expectancy_r']}  "
          f"C (short<0): {cls['C_symmetric_short_expectancy_r_lt_0']}")
    print(f"  long-only block CI95 R  {lo_ci['block_ci95']}  (iid {lo_ci['iid_ci95']})")
    print(f"  screened A/B/C pass: {cls['screened_ABC_pass']}  | raw sign agreement: "
          f"{cls['raw_sign_agreement_ABC']}  | screened==raw in-window: {screened_equals_raw}")
    print(f"  trades sym {rep_sym_s['n']} / long-only {rep_lo_s['n']}; "
          f"path-created long entries {path_s['path_created_long_entries']}, "
          f"lost {path_s['lost_symmetric_longs']}, Jaccard {path_s['long_entry_jaccard']}")
    print(f"\n  FINAL CLASSIFICATION: {cls['verdict']}")
    print(f"\nwritten: {os.path.relpath(out, STUDY)}")


if __name__ == "__main__":
    main()
