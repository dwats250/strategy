#!/usr/bin/env python3
"""VMR-0 extension threshold — TRADE-BLIND excursion profile — v1.0 · 2026-08-27.

Derives the ONLY numeric parameter VMR-0 needs — the extension threshold K, in ATR
units — from the DEVELOPMENT distribution of the charter-frozen VWAP-excursion metric
(STUDY_CHARTER §5, corrected §A1.3):

    vwap_excursion_atr(t) = ( close(t) - session_vwap(t) ) / ATR14(t)

This is a MARKET-DATA measurement, not a strategy run: it computes no entries, exits,
or P/L. K is frozen as a PRE-DECLARED quantile of |excursion| over development RTH 5m
bars — a distribution-derived threshold fixed before any VMR outcome exists, never by
inspecting strategy results. Screened corpus (frozen CORPUS_MASK_v1.0) is primary; raw
is reported for sensitivity. Development window only. Run: python3 vmr_excursion_profile.py
"""

import json
import os
import platform

import fastalpha_engine as fe
import parity_foundation as pf

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
MASK = os.path.join(HERE, "CORPUS_MASK_v1.0.json")

# PRE-DECLARED before computing: K = the 90th percentile of |excursion| over
# development RTH 5m bars — "extended" = the upper decile of absolute displacement
# from session VWAP. A magnitude choice, independent of any strategy P/L.
FROZEN_QUANTILE = 0.90
REPORT_QUANTILES = [0.50, 0.75, 0.80, 0.85, 0.90, 0.95, 0.99]
# canonical ATR magnitudes reported only to sanity-check that K is non-degenerate:
CANONICAL_KS = [1.0, 1.5, 2.0, 2.5]


def _quantile(sorted_vals, q):
    if not sorted_vals:
        return None
    idx = min(len(sorted_vals) - 1, int(q * len(sorted_vals)))
    return round(sorted_vals[idx], 6)


def excursions(rows):
    """|vwap_excursion_atr| over development-window RTH 5m bars with both
    session_vwap and atr14 defined. Signed values kept for the sign split."""
    signed = []
    for r in rows:
        if not (fe.DEV_START <= r["session_date"] <= fe.DEV_END):
            continue
        v, a = r["session_vwap"], r["atr14"]
        if v is None or a is None or a <= 0:
            continue
        signed.append((r["c"] - v) / a)
    return signed


def profile(signed):
    absv = sorted(abs(x) for x in signed)
    n = len(absv)
    above = {str(k): sum(1 for x in absv if x >= k) for k in CANONICAL_KS}
    return {
        "n_bars": n,
        "abs_quantiles": {str(q): _quantile(absv, q) for q in REPORT_QUANTILES},
        "frac_above_canonical_k": {k: round(c / n, 5) for k, c in above.items()},
        "count_above_canonical_k": above,
        "n_above_vwap": sum(1 for x in signed if x > 0),
        "n_below_vwap": sum(1 for x in signed if x < 0),
    }


def main():
    print("python", platform.python_version(), "| TRADE-BLIND excursion profile")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    drop = set(json.load(open(MASK))["mask_t_ms"])
    rows_s = fe.compute_feature_rows(9, 20, drop_t_ms=drop)
    rows_r = fe.compute_feature_rows(9, 20)

    prof_s = profile(excursions(rows_s))
    prof_r = profile(excursions(rows_r))
    k_screened = prof_s["abs_quantiles"][str(FROZEN_QUANTILE)]
    k_raw = prof_r["abs_quantiles"][str(FROZEN_QUANTILE)]

    report = {
        "role": "TRADE-BLIND VMR-0 extension-threshold derivation; NO strategy run, "
                "no P/L; distribution-derived K frozen before outcomes",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "metric": "vwap_excursion_atr = (close - session_vwap)/ATR14 (charter §5/§A1.3)",
        "development_window": [fe.DEV_START, fe.DEV_END],
        "frozen_quantile": FROZEN_QUANTILE,
        "K_screened_primary": k_screened,
        "K_raw_sensitivity": k_raw,
        "screened": prof_s,
        "raw": prof_r,
        "note": "K = |excursion| P90 (screened primary). Pre-declared quantile; a "
                "magnitude choice, not tuned on strategy outcomes. HELM may instead "
                "adopt a canonical ATR magnitude (see frac_above_canonical_k) before "
                "the first VMR run.",
    }
    out = os.path.join(HERE, "VMR_EXCURSION_PROFILE_2026-08-27.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)

    print(f"\nmetric: vwap_excursion_atr = (close - session_vwap)/ATR14 (§5/§A1.3)")
    print(f"dev RTH 5m bars (screened): {prof_s['n_bars']}")
    print(f"|excursion| quantiles (screened): {prof_s['abs_quantiles']}")
    print(f"fraction above canonical K (screened): {prof_s['frac_above_canonical_k']}")
    print(f"\nFROZEN K = |excursion| P{int(FROZEN_QUANTILE*100)} (screened primary) = {k_screened} ATR")
    print(f"          (raw sensitivity K = {k_raw} ATR)")
    print(f"\nwritten: {os.path.relpath(out, STUDY)}")


if __name__ == "__main__":
    main()
