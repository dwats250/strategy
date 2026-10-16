#!/usr/bin/env python3
"""SPY corpus integrity screen — TRADE-BLIND data-quality screen — v1.0 · 2026-08-26.

A deterministic market-data-only anomaly screen for the verified local SPY 1m
corpus. It flags bars ONLY on price-series / print characteristics. It never
reads a trade, a P/L, a stop, a strategy entry, or a strategy variant, and it
imports no engine or trade-list code — the firewall the charge requires. The
thresholds below are frozen from distributional / market-microstructure
reasoning BEFORE any strategy effect is inspected (see the pre-registration
manifest CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md); they are NOT tuned to any
outcome.

The raw corpus is never mutated: the screen is read-only over the hash-guarded
canonical file and emits (1) a full evidence report and (2) a frozen, reversible
mask of HIGH-CONFIDENCE data anomalies as a separate derived layer. A
research-clean 5m view is obtained by DROPPING masked 1m bars before
aggregation; the raw corpus is recovered simply by not applying the mask.

Run: python3 corpus_integrity_screen.py
"""

import csv
import gzip
import hashlib
import json
import os
import statistics as st
import sys
from collections import defaultdict

import parity_foundation as pf   # CONSTANTS ONLY (corpus path + sha); no trades

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
CANON = os.path.join(STUDY, "data", "cache", "canonical",
                     "SPY_1m_2024-09-01_2026-08-22.csv.gz")
CANON_SHA = pf.CANONICAL_SHA256

# ============================================================================
# FROZEN THRESHOLDS — justified from data properties, fixed before Phase 4.
# ============================================================================
# Rule B isolates a bar whose high or low is an excursion beyond BOTH immediate
# same-session neighbours that then REVERTS inside the bar (a wick, not a body
# move). Genuine price discovery is confirmed by at least one neighbour trading
# into the new area; an isolated round-trip is the bad-tick signature.
K_ISO = 15.0        # excursion >= K_ISO x the session's median 1m range. In the
                    # RTH isolation-ratio distribution this sits beyond ~99.5th
                    # pct; the RTH flag count is stable (9) for pct_floor in
                    # 0.2-0.5%, i.e. insensitive to the companion floor.
PCT_FLOOR = 0.003   # AND excursion >= 0.30% of bar price: an economic-materiality
                    # floor that also guards dead-calm sessions (tiny scale).
REV_FRAC = 0.5      # AND the reverting wick is >= half the excursion (the body
                    # did not hold at the extreme) -> a round-trip, not a break.
VOL_OUTLIER_MULT = 40.0   # v >= 40 x the session median volume: reported as
                          # corroborating EVIDENCE (real volume spikes exist at
                          # opens/closes/events, so this alone is PLAUSIBLE).
FLOAT_EPS = 1e-9

# Cross-check only (NOT a threshold input): the four bad ticks surfaced by the
# prior offline-engine work. A blind screen should rediscover them.
KNOWN_EXAMPLES = {"2025-05-27T13:13", "2025-03-14T13:44",
                  "2024-12-20T11:10", "2025-04-16T14:31"}


def load_corpus():
    """Full 1m corpus (all sessions), hash-guarded. Read-only."""
    blob = open(CANON, "rb").read()
    got = hashlib.sha256(blob).hexdigest()
    if got != CANON_SHA:
        sys.exit(f"CORPUS IDENTITY FAILURE: sha256 {got} != {CANON_SHA}")
    rows = list(csv.DictReader(gzip.decompress(blob).decode().splitlines()))
    for r in rows:
        for k in ("o", "h", "l", "c", "v", "vw"):
            r[k] = float(r[k]) if r[k] not in (None, "") else None
        r["n"] = int(r["n"]) if r["n"] not in (None, "") else None
        r["date"] = r["et_iso"][:10]
        r["key"] = r["et_iso"][:16]
    return rows, got


def screen(rows):
    """Apply the frozen rules. Returns (flags, structural). Pure/deterministic."""
    # per-(date,session) robust scale + median volume
    by_sess = defaultdict(list)
    for i, r in enumerate(rows):
        by_sess[(r["date"], r["session"])].append(i)
    scale = {}
    med_vol = {}
    for k, idxs in by_sess.items():
        scale[k] = st.median([rows[i]["h"] - rows[i]["l"] for i in idxs]) or FLOAT_EPS
        vv = [rows[i]["v"] for i in idxs if rows[i]["v"]]
        med_vol[k] = st.median(vv) if vv else 0.0

    # ---- structural integrity (timestamp / OHLC validity) ----
    ts = [int(r["t_ms"]) for r in rows]
    structural = {
        "timestamp_duplicates": len(ts) - len(set(ts)),
        "timestamp_monotonic": all(ts[i] < ts[i + 1] for i in range(len(ts) - 1)),
        "ohlc_impossible": [],   # Rule A
    }

    flags = []
    for k, idxs in by_sess.items():
        sc, mv, sess = scale[k], med_vol[k], k[1]
        for pos, i in enumerate(idxs):
            r = rows[i]
            o, h, l, c, v = r["o"], r["h"], r["l"], r["c"], r["v"]

            # ---- Rule A: impossible / internally inconsistent OHLC ----
            a_bad = []
            if h < l - FLOAT_EPS:
                a_bad.append("high<low")
            if h < max(o, c) - FLOAT_EPS:
                a_bad.append("high<max(open,close)")
            if l > min(o, c) + FLOAT_EPS:
                a_bad.append("low>min(open,close)")
            if min(o, h, l, c) <= 0:
                a_bad.append("nonpositive_price")
            if a_bad:
                structural["ohlc_impossible"].append(r["key"])
                flags.append(_rec(r, "A_ohlc_impossible",
                                  "HIGH-CONFIDENCE DATA ANOMALY",
                                  {"violations": a_bad}))
                continue

            # ---- Rule B: isolated reverting excursion (needs both neighbours) ----
            if 0 < pos < len(idxs) - 1:
                pr, nx = rows[idxs[pos - 1]], rows[idxs[pos + 1]]
                blo, bhi = min(o, c), max(o, c)
                wdn, wup = blo - l, h - bhi
                ex_dn = min(pr["l"], nx["l"]) - l
                ex_up = h - max(pr["h"], nx["h"])
                price = (o + c) / 2.0
                floor = PCT_FLOOR * price
                down = (ex_dn >= K_ISO * sc and ex_dn >= floor
                        and wdn >= REV_FRAC * ex_dn)
                up = (ex_up >= K_ISO * sc and ex_up >= floor
                      and wup >= REV_FRAC * ex_up)
                if down or up:
                    ex = ex_dn if down else ex_up
                    conf = ("HIGH-CONFIDENCE DATA ANOMALY" if sess == "RTH"
                            else "PLAUSIBLE EXTREME MARKET PRINT")
                    vol_out = (mv > 0 and v is not None and v >= VOL_OUTLIER_MULT * mv)
                    flags.append(_rec(r, "B_isolated_reverting_excursion", conf, {
                        "direction": "down" if down else "up",
                        "excursion_pts": round(ex, 4),
                        "excursion_over_scale": round(ex / sc, 2),
                        "excursion_pct_of_price": round(100 * ex / price, 4),
                        "session_median_range": round(sc, 4),
                        "reverting_wick_pts": round(wdn if down else wup, 4),
                        "volume": v, "session_median_volume": round(mv, 1),
                        "volume_outlier_corroborates": bool(vol_out),
                        "prev": _ctx(pr), "next": _ctx(nx),
                    }))
    return flags, structural


def _ctx(r):
    return {"o": r["o"], "h": r["h"], "l": r["l"], "c": r["c"], "v": r["v"]}


def _rec(r, rule, conf, evidence):
    return {"key": r["key"], "t_ms": int(r["t_ms"]), "et_iso": r["et_iso"],
            "session": r["session"], "rule": rule, "confidence": conf,
            "o": r["o"], "h": r["h"], "l": r["l"], "c": r["c"],
            "v": r["v"], "vw": r["vw"], "n": r["n"], "evidence": evidence}


def build(rows, flags, structural, corpus_sha):
    hi = [f for f in flags if f["confidence"] == "HIGH-CONFIDENCE DATA ANOMALY"]
    pl = [f for f in flags if f["confidence"] == "PLAUSIBLE EXTREME MARKET PRINT"]
    # clustering by date (which dates carry >1 flag)
    by_date = defaultdict(list)
    for f in flags:
        by_date[f["key"][:10]].append(f["key"][11:])
    clusters = {d: v for d, v in sorted(by_date.items()) if len(v) > 1}
    rediscovered = sorted(k for k in KNOWN_EXAMPLES
                          if k in {f["key"] for f in hi})
    report = {
        "role": "TRADE-BLIND SPY corpus integrity screen (data properties only)",
        "corpus": os.path.relpath(CANON, STUDY), "corpus_sha256": corpus_sha,
        "frozen_thresholds": {"K_ISO": K_ISO, "PCT_FLOOR": PCT_FLOOR,
                              "REV_FRAC": REV_FRAC,
                              "VOL_OUTLIER_MULT": VOL_OUTLIER_MULT},
        "total_1m_bars": len(rows),
        "structural": {"timestamp_duplicates": structural["timestamp_duplicates"],
                       "timestamp_monotonic": structural["timestamp_monotonic"],
                       "ohlc_impossible_count": len(structural["ohlc_impossible"])},
        "counts": {
            "flagged_1m_total": len(flags),
            "high_confidence": len(hi),
            "high_confidence_RTH": sum(1 for f in hi if f["session"] == "RTH"),
            "high_confidence_EXT": sum(1 for f in hi if f["session"] == "EXT"),
            "plausible_extreme_print": len(pl),
            "plausible_RTH": sum(1 for f in pl if f["session"] == "RTH"),
            "plausible_EXT": sum(1 for f in pl if f["session"] == "EXT"),
        },
        "sessions_affected": len({f["key"][:10] for f in flags}),
        "date_clusters_multi_flag": clusters,
        "known_examples_rediscovered": rediscovered,
        "known_examples_all_rediscovered": sorted(KNOWN_EXAMPLES) == rediscovered
                                            or set(KNOWN_EXAMPLES) <= {f["key"] for f in hi},
        "high_confidence_flags": sorted(hi, key=lambda f: f["t_ms"]),
        "plausible_flags": sorted(pl, key=lambda f: f["t_ms"]),
    }
    # frozen reversible mask = HIGH-CONFIDENCE only (Rule A + Rule B RTH)
    mask = {
        "role": "Frozen reversible mask of HIGH-CONFIDENCE data anomalies. Apply "
                "by DROPPING these 1m bars before 5m aggregation; the raw corpus "
                "is unchanged and recovered by not applying the mask.",
        "corpus_sha256": corpus_sha,
        "frozen_thresholds": report["frozen_thresholds"],
        "mask_t_ms": sorted(f["t_ms"] for f in hi),
        "mask_keys": sorted(f["key"] for f in hi),
        "count": len(hi),
    }
    return report, mask


def main():
    print("python", __import__("platform").python_version(), "| stdlib only")
    rows, sha = load_corpus()
    print(f"corpus {os.path.relpath(CANON, STUDY)} sha256 {sha} ({len(rows)} 1m bars)")
    flags, structural = screen(rows)
    report, mask = build(rows, flags, structural, sha)

    rep_path = os.path.join(HERE, "CORPUS_INTEGRITY_SCREEN_2026-08-26.json")
    mask_path = os.path.join(HERE, "CORPUS_MASK_v1.0.json")
    with open(rep_path, "w") as fh:
        json.dump(report, fh, indent=2)
    with open(mask_path, "w") as fh:
        json.dump(mask, fh, indent=2)

    c = report["counts"]
    print(f"\nflagged {c['flagged_1m_total']} 1m bars | HIGH-CONFIDENCE {c['high_confidence']} "
          f"(RTH {c['high_confidence_RTH']}, EXT {c['high_confidence_EXT']}) | "
          f"PLAUSIBLE {c['plausible_extreme_print']} (RTH {c['plausible_RTH']}, "
          f"EXT {c['plausible_EXT']})")
    print(f"structural: {report['structural']}")
    print(f"known examples all rediscovered blind: {report['known_examples_all_rediscovered']} "
          f"({report['known_examples_rediscovered']})")
    print(f"multi-flag date clusters: {report['date_clusters_multi_flag']}")
    print(f"\nHIGH-CONFIDENCE mask ({mask['count']} bars, reversible): "
          f"{[k for k in mask['mask_keys']]}")
    print(f"\nwritten: {os.path.relpath(rep_path, STUDY)}, "
          f"{os.path.relpath(mask_path, STUDY)}")


if __name__ == "__main__":
    main()
