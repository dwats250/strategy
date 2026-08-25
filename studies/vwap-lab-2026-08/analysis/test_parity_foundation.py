#!/usr/bin/env python3
"""Bounded deterministic tests for the VDC local parity foundation.

Tests local semantics only. TradingView emulator behavior that has not been
observed (fills, stops, order timing) is deliberately NOT tested here.
Run: python3 test_parity_foundation.py
"""

import datetime as dt
import hashlib
import os
import sys

import parity_foundation as pf

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_PINE = os.path.normpath(os.path.join(
    HERE, "..", "scripts", "VWAP_Continuation_FastAlpha_v0.pine"))
SOURCE_SHA256 = (
    "c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e")

ET = dt.timezone(dt.timedelta(hours=-4))  # synthetic rows use fixed EDT offset


def synth_1m(day, hh, mm, session, o=100.0, h=101.0, l=99.0, c=100.5, v=100.0):
    et = dt.datetime(2026, 8, day, hh, mm, tzinfo=ET)
    return {"t_ms": str(int(et.timestamp() * 1000)),
            "et_iso": et.isoformat(), "session": session,
            "o": str(o), "h": str(h), "l": str(l), "c": str(c), "v": str(v)}


def test_source_hash_recorded():
    with open(SOURCE_PINE, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    assert got == SOURCE_SHA256, f"ingested source hash drifted: {got}"


def test_corpus_identity_guard():
    try:
        pf.load_corpus_rth(expected_sha="0" * 64)
    except SystemExit as e:
        assert "LOCAL CORPUS IDENTITY FAILURE" in str(e)
    else:
        raise AssertionError("identity guard did not trip on wrong sha")


def test_rth_filter_before_resample_no_ext_contamination():
    rows = [synth_1m(3, 9, 25, "EXT", c=500.0),   # would poison o/h/l/c if kept
            synth_1m(3, 9, 30, "RTH"), synth_1m(3, 9, 31, "RTH"),
            synth_1m(3, 9, 32, "RTH"), synth_1m(3, 9, 33, "RTH"),
            synth_1m(3, 9, 34, "RTH")]
    rth = [r for r in rows if r["session"] == "RTH"]  # the load path's filter
    bars = pf.build_5m_bars(rth)
    assert len(bars) == 1 and bars[0]["hm"] == 930
    assert bars[0]["constituent_count"] == 5 and not bars[0]["partial"]
    assert bars[0]["c"] == 100.5  # EXT 500.0 close never entered the sequence


def test_partial_bucket_preserved_not_fabricated():
    rows = [synth_1m(3, 13, 0, "RTH")]  # lone shortened-session terminal minute
    bars = pf.build_5m_bars(rows)
    assert len(bars) == 1 and bars[0]["partial"] and \
        bars[0]["constituent_count"] == 1


def test_session_vwap_resets_and_accumulates():
    bars = [
        {"session_date": "2026-08-03", "et_start": "x", "hm": 930,
         "o": 10, "h": 12, "l": 8, "c": 10, "v": 100,
         "first_1m_t_ms": 0, "last_1m_t_ms": 0, "constituent_count": 5,
         "partial": False},
        {"session_date": "2026-08-03", "et_start": "x", "hm": 935,
         "o": 10, "h": 21, "l": 15, "c": 18, "v": 300,
         "first_1m_t_ms": 0, "last_1m_t_ms": 0, "constituent_count": 5,
         "partial": False},
        {"session_date": "2026-08-04", "et_start": "x", "hm": 930,
         "o": 10, "h": 33, "l": 27, "c": 30, "v": 50,
         "first_1m_t_ms": 0, "last_1m_t_ms": 0, "constituent_count": 5,
         "partial": False},
    ]
    feats = pf.compute_features(bars)
    hlc3 = [(12 + 8 + 10) / 3, (21 + 15 + 18) / 3, (33 + 27 + 30) / 3]
    assert abs(feats[0]["session_vwap"] - hlc3[0]) < 1e-12
    expected = (hlc3[0] * 100 + hlc3[1] * 300) / 400
    assert abs(feats[1]["session_vwap"] - expected) < 1e-12
    assert abs(feats[2]["session_vwap"] - hlc3[2]) < 1e-12  # reset on new day


def _flat_bars(n, close=100.0, day_split=None):
    bars = []
    for i in range(n):
        date = "2026-08-03" if (day_split is None or i < day_split) \
            else "2026-08-04"
        bars.append({"session_date": date, "et_start": "x", "hm": 1000,
                     "o": close, "h": close, "l": close, "c": close, "v": 1,
                     "first_1m_t_ms": 0, "last_1m_t_ms": 0,
                     "constituent_count": 5, "partial": False})
    return bars


def test_ema_warmup_and_continuity_across_session_boundary():
    closes = [float(i) for i in range(1, 25)]
    out = pf.ema(closes, 9)
    assert out[:8] == [None] * 8, "EMA must be na during warm-up"
    assert abs(out[8] - sum(closes[:9]) / 9) < 1e-12, "SMA seed"
    # continuity: same closes, with a session boundary at index 12, must give
    # the identical series — no session reset
    bars_a = _flat_bars(24)
    bars_b = _flat_bars(24, day_split=12)
    for i, (a, b) in enumerate(zip(bars_a, bars_b)):
        a["c"] = b["c"] = closes[i]
    fa = pf.compute_features(bars_a)
    fb = pf.compute_features(bars_b)
    assert all((x["ema9"] is None and y["ema9"] is None) or
               abs(x["ema9"] - y["ema9"]) < 1e-12 for x, y in zip(fa, fb))


def test_atr_continuity_gap_enters_true_range():
    bars = _flat_bars(20, close=100.0, day_split=10)
    for b in bars[10:]:  # next session gaps to 110, zero intrabar range
        b.update(o=110.0, h=110.0, l=110.0, c=110.0)
    trs = pf.true_ranges(bars)
    assert trs[10] == 10.0, "first TR of new session must see prior session close"
    assert trs[9] == 0.0 and trs[11] == 0.0
    a = pf.atr(bars, 14)
    assert a[12] is None and a[13] is not None  # SMA-seeded at index 13
    assert abs(a[13] - (10.0 / 14)) < 1e-12


def test_entry_window_boundaries_and_doji():
    base = {"session_date": "2026-08-03", "et_start": "x",
            "o": 100.0, "h": 101.0, "l": 99.0, "v": 1,
            "first_1m_t_ms": 0, "last_1m_t_ms": 0, "constituent_count": 5,
            "partial": False}
    hms = [930, 935, 1525, 1530, 1550]
    bars = [{**base, "hm": hm, "c": 100.0} for hm in hms]
    feats = pf.compute_features(bars)
    assert [f["in_entry_window"] for f in feats] == \
        [False, True, True, False, False]
    doji = feats[1]
    assert doji["doji"] and not doji["red_bar"] and not doji["green_bar"]
    assert not doji["long_candidate"] and not doji["short_candidate"]


def test_real_corpus_session_bar_counts_if_present():
    """Conditional on the local gitignored corpus: one normal session must
    yield 78 five-minute bars; a shortened session 43 (42 full + 1 partial)."""
    if not os.path.exists(pf.CANONICAL):
        print("  (corpus absent — skipped)")
        return
    bars = pf.build_5m_bars(pf.load_corpus_rth())
    by_day = {}
    for b in bars:
        by_day.setdefault(b["session_date"], []).append(b)
    assert len(by_day["2024-09-03"]) == 78
    assert not any(b["partial"] for b in by_day["2024-09-03"])
    short = by_day["2024-12-24"]
    assert len(short) == 43
    assert sum(1 for b in short if b["partial"]) == 1
    assert short[-1]["partial"] and short[-1]["constituent_count"] == 1


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        print(f"- {t.__name__}")
        t()
    print(f"PASS: {len(tests)} tests")


if __name__ == "__main__":
    sys.exit(main())
