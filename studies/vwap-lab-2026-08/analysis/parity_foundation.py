#!/usr/bin/env python3
"""VDC local parity foundation — BAR + FEATURE seam only.

Reconstructs the Pine input bars (RTH-only 5-minute OHLCV) from the verified SPY
1-minute corpus and computes the Fast Alpha v0 feature set under the mechanics
recorded in scripts/VWAP_Continuation_FastAlpha_v0_PROVENANCE.md.

This is NOT a backtester. It computes no entry/exit simulation, no fills, no
P/L, no expectancy. `long_candidate` / `short_candidate` are LOCAL SEMANTIC
CANDIDATES: they apply window+state+trigger only and are FLAT-AGNOSTIC — the
Pine `flat` (position_size == 0) condition is execution state and is not
modeled here. They are not TradingView-proven VDC signals.

Semantics implemented per the published Pine reference pseudocode:
  ta.ema  — alpha = 2/(len+1), seeded with SMA of the first len values
  ta.rma  — alpha = 1/len,     seeded with SMA of the first len values
  ta.atr  — RMA of true range; first-bar TR = high-low (no previous close)
Exact TradingView initialization/warm-up and float behavior remain
TV-CONFIRMATION PENDING (PARITY_GATES.md, Gate 2).

Corpus identity is guarded: on hash mismatch this exits with
LOCAL CORPUS IDENTITY FAILURE and touches nothing.
"""

import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
CANONICAL = os.path.join(
    DATA, "cache", "canonical", "SPY_1m_2024-09-01_2026-08-22.csv.gz")
CANONICAL_SHA256 = (
    "a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a")
DERIVED_DIR = os.path.join(DATA, "cache", "derived")

EMA_FAST_LEN = 9
EMA_SLOW_LEN = 20
ATR_LEN = 14
ENTRY_START_HM = 935
ENTRY_CUTOFF_HM = 1530
EOD_BAR_HM = 1550

FIVE_MIN_FIELDS = [
    "session_date", "et_start", "hm", "o", "h", "l", "c", "v",
    "first_1m_t_ms", "last_1m_t_ms", "constituent_count", "partial",
]
FEATURE_FIELDS = FIVE_MIN_FIELDS + [
    "session_vwap", "ema9", "ema20", "atr14",
    "in_entry_window", "red_bar", "green_bar", "doji",
    "bullish_state", "bearish_state",
    "long_candidate", "short_candidate",  # LOCAL SEMANTIC CANDIDATES, flat-agnostic
]


def load_corpus_rth(path=CANONICAL, expected_sha=CANONICAL_SHA256):
    """Verify corpus identity, then return RTH 1m rows ONLY (EXT removed before
    any resampling or indicator input is built — the Pine requires an RTH-only
    chart and EXT bars would contaminate EMA/ATR)."""
    with open(path, "rb") as fh:
        blob = fh.read()
    got = hashlib.sha256(blob).hexdigest()
    if got != expected_sha:
        sys.exit(f"LOCAL CORPUS IDENTITY FAILURE: sha256 {got} != expected "
                 f"{expected_sha}. Not repairing or replacing the corpus.")
    rows = list(csv.DictReader(gzip.decompress(blob).decode().splitlines()))
    return [r for r in rows if r["session"] == "RTH"]


def build_5m_bars(rth_1m_rows):
    """RTH 5-minute bars on America/New_York wall-clock boundaries
    (09:30, 09:35, ...). Missing minutes are never filled; shortened-session
    terminal partial buckets are preserved, not fabricated away."""
    buckets = {}
    for r in rth_1m_rows:
        et = dt.datetime.fromisoformat(r["et_iso"])
        start = et.replace(minute=et.minute - et.minute % 5, second=0,
                           microsecond=0)
        buckets.setdefault(start, []).append(r)
    bars = []
    for start in sorted(buckets):
        rs = sorted(buckets[start], key=lambda r: int(r["t_ms"]))
        bars.append({
            "session_date": start.date().isoformat(),
            "et_start": start.isoformat(),
            "hm": start.hour * 100 + start.minute,
            "o": float(rs[0]["o"]),
            "h": max(float(r["h"]) for r in rs),
            "l": min(float(r["l"]) for r in rs),
            "c": float(rs[-1]["c"]),
            "v": sum(float(r["v"]) for r in rs),
            "first_1m_t_ms": int(rs[0]["t_ms"]),
            "last_1m_t_ms": int(rs[-1]["t_ms"]),
            "constituent_count": len(rs),
            "partial": len(rs) < 5,
        })
    return bars


def _seeded_recursive(values, length, alpha):
    """SMA seed at index length-1, then out[i] = alpha*x + (1-alpha)*prev.
    Returns list with None during warm-up (Pine: na)."""
    out = [None] * len(values)
    if len(values) < length:
        return out
    prev = sum(values[:length]) / length
    out[length - 1] = prev
    for i in range(length, len(values)):
        prev = alpha * values[i] + (1 - alpha) * prev
        out[i] = prev
    return out


def ema(values, length):
    return _seeded_recursive(values, length, 2.0 / (length + 1))


def true_ranges(bars):
    """TR across the continuous RTH 5m sequence: the first bar of a session
    references the PREVIOUS session's final close (no reset), so overnight gaps
    affect ATR. Only the very first bar of the whole sequence has no previous
    close (TR = high - low)."""
    trs = []
    prev_close = None
    for b in bars:
        if prev_close is None:
            trs.append(b["h"] - b["l"])
        else:
            trs.append(max(b["h"] - b["l"],
                           abs(b["h"] - prev_close),
                           abs(b["l"] - prev_close)))
        prev_close = b["c"]
    return trs


def atr(bars, length=ATR_LEN):
    return _seeded_recursive(true_ranges(bars), length, 1.0 / length)


def compute_features(bars):
    """Feature rows per the exact source mechanics. Session VWAP resets on the
    first bar of each session; EMA/ATR run continuously across sessions."""
    closes = [b["c"] for b in bars]
    ema9 = ema(closes, EMA_FAST_LEN)
    ema20 = ema(closes, EMA_SLOW_LEN)
    atr14 = atr(bars)

    rows = []
    cum_pv = cum_v = 0.0
    prev_date = None
    for i, b in enumerate(bars):
        hlc3 = (b["h"] + b["l"] + b["c"]) / 3.0
        if b["session_date"] != prev_date:            # newRTH: session reset
            cum_pv, cum_v = hlc3 * b["v"], b["v"]
            prev_date = b["session_date"]
        else:                                         # inRTH accumulation
            cum_pv += hlc3 * b["v"]
            cum_v += b["v"]
        vwap = (cum_pv / cum_v) if cum_v > 0 else None

        in_window = ENTRY_START_HM <= b["hm"] < ENTRY_CUTOFF_HM
        red = b["c"] < b["o"]
        green = b["c"] > b["o"]
        doji = b["c"] == b["o"]
        e9, e20 = ema9[i], ema20[i]
        bullish = (vwap is not None and e9 is not None and e20 is not None
                   and b["c"] > vwap and e9 > e20)
        bearish = (vwap is not None and e9 is not None and e20 is not None
                   and b["c"] < vwap and e9 < e20)
        rows.append({
            **b,
            "session_vwap": vwap,
            "ema9": e9,
            "ema20": e20,
            "atr14": atr14[i],
            "in_entry_window": in_window,
            "red_bar": red,
            "green_bar": green,
            "doji": doji,
            "bullish_state": bullish,
            "bearish_state": bearish,
            # LOCAL SEMANTIC CANDIDATES — flat-agnostic, not TV-proven signals
            "long_candidate": in_window and bullish and red,
            "short_candidate": in_window and bearish and green,
        })
    return rows


def main():
    rth = load_corpus_rth()
    bars = build_5m_bars(rth)
    feats = compute_features(bars)

    os.makedirs(DERIVED_DIR, exist_ok=True)
    stem = "SPY_5m_RTH_features_2024-09-03_2026-08-21"
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=FEATURE_FIELDS)
    writer.writeheader()
    writer.writerows(feats)
    payload = gzip.compress(buf.getvalue().encode(), mtime=0)
    out_path = os.path.join(DERIVED_DIR, f"{stem}.csv.gz")
    with open(out_path, "wb") as fh:
        fh.write(payload)

    manifest = {
        "role": "LOCAL PARITY FOUNDATION — bars+features only; no simulation, "
                "no P/L, no expectancy; candidates are flat-agnostic",
        "input_canonical_sha256": CANONICAL_SHA256,
        "source_script": "scripts/VWAP_Continuation_FastAlpha_v0.pine",
        "bars_5m": len(bars),
        "partial_5m_buckets": sum(1 for b in bars if b["partial"]),
        "sessions": len({b["session_date"] for b in bars}),
        "derived_path": os.path.relpath(out_path, DATA),
        "derived_sha256": hashlib.sha256(payload).hexdigest(),
    }
    man_path = os.path.join(DERIVED_DIR, f"{stem}.manifest.json")
    with open(man_path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
