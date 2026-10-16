#!/usr/bin/env python3
"""Deterministic tests for the corpus integrity screen (trade-blind).

Covers: anomaly detection (Rule A impossible OHLC, Rule B isolated reverting
spike, clean bars not flagged, EXT downgraded to PLAUSIBLE), no mutation of the
input, reversible masking, corpus-file immutability, and repeatability.
Run: python3 test_corpus_integrity_screen.py
"""

import copy
import hashlib
import json
import os
import sys

import corpus_integrity_screen as cis
import fastalpha_engine as fe

HERE = os.path.dirname(os.path.abspath(__file__))


def row(tms, hh, mm, o, h, l, c, session="RTH", v=100000.0, n=500):
    return {"t_ms": str(tms), "et_iso": f"2025-06-02T{hh:02d}:{mm:02d}:00-04:00",
            "session": session, "o": o, "h": h, "l": l, "c": c, "v": v,
            "vw": (o + c) / 2, "n": n, "date": "2025-06-02",
            "key": f"2025-06-02T{hh:02d}:{mm:02d}"}


def calm_session(session="RTH", spike=None, n_bars=12):
    """A quiet session (~0.10 ranges near 500) with an optional spike row dict
    merged in at index 6."""
    rows = []
    base = 1_700_000_000_000
    for i in range(n_bars):
        px = 500.0 + i * 0.02
        rows.append(row(base + i * 60000, 10, i, px, px + 0.05, px - 0.05,
                        px + 0.01, session=session))
    if spike:
        rows[6].update(spike)
    return rows


def test_ruleB_flags_isolated_reverting_downspike():
    rows = calm_session(spike={"l": 490.0, "o": 500.1, "c": 500.12, "h": 500.2})
    flags, _ = cis.screen(copy.deepcopy(rows))
    b = [f for f in flags if f["rule"] == "B_isolated_reverting_excursion"]
    assert len(b) == 1 and b[0]["key"] == "2025-06-02T10:06", b
    assert b[0]["confidence"] == "HIGH-CONFIDENCE DATA ANOMALY"
    assert b[0]["evidence"]["direction"] == "down"


def test_ruleB_ext_spike_is_plausible_not_high_confidence():
    rows = calm_session(session="EXT",
                        spike={"l": 490.0, "o": 500.1, "c": 500.12, "h": 500.2})
    flags, _ = cis.screen(rows)
    b = [f for f in flags if f["rule"] == "B_isolated_reverting_excursion"]
    assert len(b) == 1 and b[0]["confidence"] == "PLAUSIBLE EXTREME MARKET PRINT", b


def test_clean_session_no_flags():
    flags, structural = cis.screen(calm_session())
    assert flags == [], flags
    assert structural["timestamp_monotonic"] and structural["timestamp_duplicates"] == 0


def test_ruleA_flags_impossible_ohlc():
    rows = calm_session(spike={"h": 499.0, "l": 500.0, "o": 499.5, "c": 499.8})
    flags, structural = cis.screen(rows)
    a = [f for f in flags if f["rule"] == "A_ohlc_impossible"]
    assert len(a) == 1 and a[0]["confidence"] == "HIGH-CONFIDENCE DATA ANOMALY", a
    assert len(structural["ohlc_impossible"]) == 1


def test_genuine_move_not_flagged_when_confirmed_by_neighbor():
    # a real breakout: the low is matched by the NEXT bar (not isolated) -> no flag
    rows = calm_session()
    rows[6].update({"o": 500.1, "h": 500.2, "l": 496.0, "c": 496.1})
    rows[7].update({"o": 496.1, "h": 496.3, "l": 495.9, "c": 496.0})  # confirms
    flags, _ = cis.screen(rows)
    assert [f for f in flags if f["rule"].startswith("B")] == [], flags


def test_screen_does_not_mutate_input():
    rows = calm_session(spike={"l": 490.0, "o": 500.1, "c": 500.12, "h": 500.2})
    before = json.dumps(rows, sort_keys=True)
    cis.screen(rows)
    assert json.dumps(rows, sort_keys=True) == before, "screen mutated its input"


def test_determinism_synthetic():
    rows = calm_session(spike={"l": 490.0, "o": 500.1, "c": 500.12, "h": 500.2})
    f1, s1 = cis.screen(copy.deepcopy(rows))
    f2, s2 = cis.screen(copy.deepcopy(rows))
    assert json.dumps(f1) == json.dumps(f2) and s1 == s2


def test_corpus_file_not_mutated_by_screen():
    sha_before = hashlib.sha256(open(cis.CANON, "rb").read()).hexdigest()
    rows, _ = cis.load_corpus()
    cis.screen(rows)
    sha_after = hashlib.sha256(open(cis.CANON, "rb").read()).hexdigest()
    assert sha_before == sha_after == cis.CANON_SHA, "corpus file changed!"


def test_reversible_mask_is_pure_filter():
    # applying the mask drops bars; not applying recovers the full set; the mask
    # is not sticky across calls (reversible / non-mutating).
    mask = json.load(open(os.path.join(HERE, "CORPUS_MASK_v1.0.json")))
    drop = set(mask["mask_t_ms"])
    raw1 = fe.compute_feature_rows(9, 20)
    scr = fe.compute_feature_rows(9, 20, drop_t_ms=drop)
    raw2 = fe.compute_feature_rows(9, 20)
    assert len(scr) <= len(raw1), "screened view should not add bars"
    assert len(raw1) == len(raw2), "raw not recovered — mask leaked (not reversible)"
    assert json.dumps(raw1) == json.dumps(raw2), "raw view not identical across calls"


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} CORPUS-INTEGRITY TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
