#!/usr/bin/env python3
"""Deterministic tests for the R1 instrumentation mirror (no corpus, no
network): frozen A1.2 / A1.4 rule edges plus containment purity on a
synthetic bar sequence."""

import copy
import datetime as dt

import parity_foundation as pf
import instrumentation_r1 as ir


# ---------- A1.2 acceptance rule ----------

def test_accept_three_of_four_with_last_close_gate():
    # 3 of 4 above own-bar VWAP and last close above -> ESTABLISHED LONG
    assert ir.accept_state([101, 99, 101, 101], [100, 100, 100, 100]) == 1
    # mirrored short
    assert ir.accept_state([99, 101, 99, 99], [100, 100, 100, 100]) == -1


def test_accept_last_close_gate_blocks():
    # 3 of 4 above but the most recent close is below its VWAP -> MIXED
    assert ir.accept_state([101, 101, 101, 99], [100, 100, 100, 100]) == 0


def test_accept_tie_counts_toward_neither():
    # two above + one tie + last above = only 3 votes long IF the tie
    # counted long; frozen rule says it doesn't -> 2 votes -> MIXED... but
    # here bars 1,3,4 are above (3 votes) and bar 2 ties -> LONG.
    assert ir.accept_state([101, 100, 101, 101], [100, 100, 100, 100]) == 1
    # two above + tie + last above = 3rd vote missing -> MIXED
    assert ir.accept_state([101, 100, 100, 101], [100, 100, 100, 100]) == 0


def test_accept_votes_use_each_bars_own_vwap():
    # constant closes; per-bar VWAPs put 3 of 4 closes above their own bar's
    # VWAP (and the last one above) even though close < the LAST bar's
    # VWAP would fail a compare-to-current-vwap reading on earlier bars.
    closes = [100, 100, 100, 100]
    vwaps = [99, 99, 101, 99]   # bars 1,2,4 above own VWAP; bar 3 below
    assert ir.accept_state(closes, vwaps) == 1


def test_accept_unavailable_before_four_session_bars_and_session_reset():
    rows = []
    for day, n in (("2026-01-05", 5), ("2026-01-06", 4)):
        for i in range(n):
            rows.append({
                "session_date": day, "et_start": f"{day}T09:{30+5*i:02d}",
                "hm": 930 + 5 * i, "o": 100.0, "h": 101.0, "l": 99.0,
                "c": 101.0, "v": 1.0, "session_vwap": 100.0,
                "ema9": None, "ema20": None, "atr14": None,
            })
    out = ir.compute_instrumentation(rows)
    states = [r["accept_state_dir"] for r in out]
    # day 1: bars 1-3 unavailable, bars 4-5 classified
    assert states[:3] == [None, None, None]
    assert states[3] == 1 and states[4] == 1
    # day 2 resets: unavailable again until its 4th bar
    assert states[5:8] == [None, None, None]
    assert states[8] == 1


# ---------- A1.4 ordering / dispersion / expansion ----------

def test_ordered_dir():
    assert ir.ordered_dir(3, 2, 1) == 1
    assert ir.ordered_dir(1, 2, 3) == -1
    assert ir.ordered_dir(2, 3, 1) == 0
    assert ir.ordered_dir(2, 2, 1) == 0          # equality is not ordered
    assert ir.ordered_dir(None, 2, 1) is None    # warm-up


def test_dispersion_and_expansion():
    assert ir.dispersion(102.0, 100.0, 0.5) == 4.0
    assert ir.dispersion(None, 100.0, 0.5) is None
    assert ir.expanding_flag(1.1, 1.0) == 1
    assert ir.expanding_flag(1.0, 1.0) == 0      # strict inequality
    assert ir.expanding_flag(1.0, None) is None


def test_consecutive_count_reset_and_direction_flip():
    # not aligned -> 0
    assert ir.consec_update(3, 1, 0, 1) == 0
    # not expanding -> 0
    assert ir.consec_update(3, 1, 1, 0) == 0
    # fresh run
    assert ir.consec_update(0, None, 1, 1) == 1
    # continuation
    assert ir.consec_update(1, 1, 1, 1) == 2
    # direction flip while aligned+expanding starts a NEW run at 1
    assert ir.consec_update(2, 1, -1, 1) == 1


# ---------- A1.4 shock ----------

def test_recent_shock_na_guard_and_max():
    assert ir.recent_shock([1.0, 2.0, 0.5, 1.5]) == 2.0
    assert ir.recent_shock([None, 2.0, 0.5, 1.5]) is None   # any None -> None
    assert ir.recent_shock([2.0, 0.5, 1.5]) is None         # short window


def _synthetic_bars(n=80):
    """Deterministic mildly trending 5m session bars across two days."""
    bars = []
    base = dt.datetime(2026, 1, 5, 9, 30)
    px = 100.0
    for i in range(n):
        day, slot = divmod(i, 78)
        start = (base + dt.timedelta(days=day, minutes=5 * slot))
        px += 0.1 if (i % 7) else -0.25
        o, c = px, px + (0.15 if i % 3 else -0.2)
        h, l = max(o, c) + 0.05, min(o, c) - 0.05
        bars.append({
            "session_date": start.date().isoformat(),
            "et_start": start.isoformat(), "hm": start.hour * 100 + start.minute,
            "o": o, "h": h, "l": l, "c": c, "v": 1000.0 + i,
            "first_1m_t_ms": 0, "last_1m_t_ms": 0,
            "constituent_count": 5, "partial": False,
        })
    return bars


def test_synthetic_integration_formulas_and_purity():
    feats = pf.compute_features(_synthetic_bars())
    snapshot = copy.deepcopy(feats)
    out = ir.compute_instrumentation(feats)
    assert feats == snapshot, "input rows must not be mutated"

    closes = [f["c"] for f in feats]
    ema50 = pf.ema(closes, 50)
    trs = pf.true_ranges(feats)
    s = [None] * len(feats)
    for i, (f, r) in enumerate(zip(feats, out)):
        # foundation columns pass through unchanged
        for k in pf.FEATURE_FIELDS:
            assert r[k] == f[k]
        # S and expansion match the frozen formulas
        s[i] = (abs(f["ema9"] - ema50[i]) / f["atr14"]
                if None not in (f["ema9"], ema50[i], f["atr14"]) else None)
        assert r["s_9_20_50"] == s[i]
        want_exp = (None if i < 2 or s[i] is None or s[i - 2] is None
                    else (1 if s[i] > s[i - 2] else 0))
        assert r["expanding_9_20_50"] == want_exp
        # shock uses the PRIOR bar's ATR
        atr_prev = feats[i - 1]["atr14"] if i >= 1 else None
        want_shock = trs[i] / atr_prev if atr_prev is not None else None
        assert r["shock_ratio"] == want_shock
        # count is 0 whenever not aligned-and-expanding
        if not (r["ordered_9_20_50"] in (1, -1)
                and r["expanding_9_20_50"] == 1):
            assert r["aligned_exp_count_9_20_50"] == 0
        else:
            assert r["aligned_exp_count_9_20_50"] >= 1


if __name__ == "__main__":
    import sys
    mod = sys.modules[__name__]
    for name in sorted(dir(mod)):
        if name.startswith("test_"):
            getattr(mod, name)()
            print(f"{name}: PASS")
