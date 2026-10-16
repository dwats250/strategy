#!/usr/bin/env python3
"""MIM previous-close corporate-action diagnostic — TRADE-BLIND — v1.0 · 2026-08-27.

MIM-0's `early_return` crosses the PREVIOUS RTH close (previous_close -> 10:00). The
local corpus is split-adjusted but DIVIDEND-UNADJUSTED (data/CORPUS_*.md: Polygon
adjusted=true = splits only; R0 ledger: "split-only ... NOT ADJ"). On SPY ex-dividend
sessions the previous_close->open overnight gap therefore contains an unadjusted
dividend drop that is NOT momentum.

This script measures ONLY the overnight gap `open(session)/close(prev_session) - 1`
per session — a corporate-action / data-semantics check. It computes NO MIM predictor
(nothing to 10:00), NO late-window return, NO regression, and NO strategy P/L. Its sole
purpose is to establish, before any MIM outcome access, whether a clean dividend
convention can be formed from the corpus alone. Run: python3 mim_overnight_diagnostic.py
"""

import json
import os
import platform

import parity_foundation as pf

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
DEV_START, DEV_END = "2024-09-03", "2025-12-31"


def sessions(rth):
    by = {}
    for r in rth:
        by.setdefault(r["et_iso"][:10], []).append(r)
    out = []
    for d in sorted(by):
        rows = sorted(by[d], key=lambda r: int(r["t_ms"]))
        out.append({"date": d, "open": float(rows[0]["o"]),
                    "close": float(rows[-1]["c"]),
                    "first_hm": rows[0]["et_iso"][11:16],
                    "last_hm": rows[-1]["et_iso"][11:16], "nbars": len(rows)})
    return out


def main():
    print("python", platform.python_version(), "| TRADE-BLIND overnight-gap diagnostic")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    sess = sessions(pf.load_corpus_rth())
    gaps = []
    for i in range(1, len(sess)):
        prev, cur = sess[i - 1], sess[i]
        if not (DEV_START <= cur["date"] <= DEV_END):
            continue
        g = cur["open"] / prev["close"] - 1.0
        gaps.append({"date": cur["date"], "prev_date": prev["date"],
                     "gap_bps": round(g * 1e4, 2),
                     "prev_close": prev["close"], "open": cur["open"]})
    gaps_sorted = sorted(gaps, key=lambda x: x["gap_bps"])
    absv = sorted(abs(x["gap_bps"]) for x in gaps)

    def q(p):
        return round(absv[min(len(absv) - 1, int(p * len(absv)))], 2) if absv else None

    # SPY pays a quarterly dividend (~0.3-0.4% of price); an unadjusted ex-div
    # session shows a ~-30 to -40 bps overnight drop attributable to the dividend,
    # not momentum. Flag the most-negative overnight gaps (candidate ex-div days).
    most_negative = gaps_sorted[:12]
    report = {
        "role": "TRADE-BLIND overnight-gap / corporate-action diagnostic for MIM-0; "
                "no MIM predictor, no late window, no regression, no P/L",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "corpus_adjustment": "split-adjusted, DIVIDEND-UNADJUSTED (Polygon adjusted=true "
                             "= splits only; data/CORPUS_SPY_1m_2024-09-01_2026-08-22.md; "
                             "R0 ledger 'split-only ... NOT ADJ')",
        "development_window": [DEV_START, DEV_END],
        "n_overnight_gaps": len(gaps),
        "abs_gap_bps_quantiles": {"p50": q(0.50), "p90": q(0.90), "p95": q(0.95),
                                  "p99": q(0.99), "max": round(absv[-1], 2) if absv else None},
        "twelve_most_negative_overnight_gaps": most_negative,
        "note": "Distinguishing a dividend ex-date drop from a genuine overnight news "
                "gap using OHLCV alone requires a threshold heuristic (a guess) that "
                "would also drop real momentum gaps. Clean ex-dividend identification "
                "needs an external SPY corporate-action calendar, which is not in the "
                "repository and is not fetched in this packet.",
    }
    out = os.path.join(HERE, "MIM_OVERNIGHT_DIAGNOSTIC_2026-08-27.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"\ncorpus adjustment: {report['corpus_adjustment']}")
    print(f"overnight gaps in dev window: {len(gaps)}")
    print(f"|gap| bps quantiles: {report['abs_gap_bps_quantiles']}")
    print("twelve most-negative overnight gaps (candidate ex-dividend sessions):")
    for g in most_negative:
        print(f"  {g['date']} (prev {g['prev_date']}): {g['gap_bps']} bps")
    print(f"\nwritten: {os.path.relpath(out, STUDY)}")


if __name__ == "__main__":
    main()
