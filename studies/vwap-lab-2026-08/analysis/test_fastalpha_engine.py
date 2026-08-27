#!/usr/bin/env python3
"""Bounded deterministic tests for the FastAlpha offline execution engine.

Exercises each execution path on hand-built synthetic feature rows (indicator
values supplied directly, so these tests isolate the ORDER/FILL/STOP/EXIT logic
this module adds on top of parity_foundation's feature seam). No corpus, no RNG,
no wall-clock. Run: python3 test_fastalpha_engine.py
"""

import json
import sys

import fastalpha_engine as fe

DAY = "2025-01-02"          # a normal full RTH session, inside the dev window
SLIP = fe.SLIP             # 0.01


def frow(hm, o, h, l, c, vwap, atr14, long_c=False, short_c=False):
    hh, mm = divmod(hm, 100)
    return {
        "session_date": DAY,
        "et_start": f"{DAY}T{hh:02d}:{mm:02d}:00",
        "hm": hm, "o": o, "h": h, "l": l, "c": c,
        "session_vwap": vwap, "atr14": atr14,
        "long_candidate": long_c, "short_candidate": short_c,
    }


def one(rows):
    tr = fe.simulate(rows)
    assert len(tr) == 1, f"expected 1 trade, got {len(tr)}: {tr}"
    return tr[0]


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_long_entry_fills_next_open_with_slippage():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),  # signal
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),             # fill @ open
        frow(1550, 101.0, 101.2, 100.8, 101.0, 90.0, 0.50),            # EOD close
    ]
    t = one(rows)
    assert t["side"] == "long"
    assert approx(t["entry_price"], 100.01), t          # open 100 + 1 tick
    assert t["entry_bar"] == f"{DAY} 10:05"
    assert t["signal_bar"] == f"{DAY} 10:00"
    assert t["exit_reason"] == "EOD"
    assert approx(t["exit_price"], 100.99), t            # close 101 - 1 tick
    assert approx(t["pnl"], round(100.99 - 100.01, 4)), t


def test_long_stop_out_later_bar_fills_at_stop_minus_slip():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),   # entry 100.01, stop 99.51
        frow(1010, 100.0, 100.1, 99.00, 99.9, 90.0, 0.50),   # low 99.0 <= stop -> stop
        frow(1550, 100.0, 100.1, 99.9, 100.0, 90.0, 0.50),
    ]
    t = one(rows)
    assert t["exit_reason"] == "Long ATR Stop", t
    assert approx(t["exit_price"], 99.50), t              # stop 99.51 - 1 tick
    assert t["exit_bar"] == f"{DAY} 10:10"


def test_long_entry_and_stop_same_bar():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.3, 99.00, 100.1, 90.0, 0.50),  # fills 100.01, low 99 hits stop 99.51
        frow(1550, 100.0, 100.1, 99.9, 100.0, 90.0, 0.50),
    ]
    t = one(rows)
    assert t["exit_reason"] == "Long ATR Stop", t
    assert t["entry_bar"] == t["exit_bar"] == f"{DAY} 10:05", t
    assert approx(t["exit_price"], 99.50), t


def test_long_gap_through_stop_fills_at_open():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),   # entry 100.01, stop 99.51
        frow(1010, 99.00, 99.10, 98.50, 99.05, 90.0, 0.50),  # OPENS below stop -> fill at open
        frow(1550, 99.0, 99.1, 98.9, 99.0, 90.0, 0.50),
    ]
    t = one(rows)
    assert t["exit_reason"] == "Long ATR Stop", t
    assert approx(t["exit_price"], 98.99), t              # open 99.00 - 1 tick (gap branch)


def test_long_thesis_exit_next_open():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 99.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 99.0, 0.50),   # entry 100.01, stop 99.51
        frow(1010, 99.80, 99.90, 99.55, 99.60, 100.0, 0.50), # close 99.6<vwap100, low>stop
        frow(1015, 99.50, 99.60, 99.40, 99.45, 100.0, 0.50), # thesis close fills at open
    ]
    t = one(rows)
    assert t["exit_reason"] == "VWAP Failure", t
    assert approx(t["exit_price"], 99.49), t              # open 99.50 - 1 tick
    assert t["exit_bar"] == f"{DAY} 10:15"


def test_flat_gate_suppresses_second_entry():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),
        frow(1010, 100.4, 100.9, 100.3, 100.8, 90.0, 0.50, long_c=True),  # in position
        frow(1015, 100.8, 101.1, 100.7, 101.0, 90.0, 0.50, long_c=True),  # in position
        frow(1550, 101.0, 101.2, 100.8, 101.0, 90.0, 0.50),
    ]
    tr = fe.simulate(rows)
    assert len(tr) == 1, f"flat gate breached: {tr}"       # only the first entry


def test_short_entry_and_stop_mirror():
    rows = [
        frow(1000, 100, 100.1, 99.8, 100.0, 110.0, 0.50, short_c=True),   # signal
        frow(1005, 100.0, 100.2, 99.5, 99.6, 110.0, 0.50),   # entry 99.99, stop 100.49
        frow(1010, 100.0, 100.60, 99.9, 100.0, 110.0, 0.50), # high 100.6 >= stop -> stop
        frow(1550, 100.0, 100.1, 99.9, 100.0, 110.0, 0.50),
    ]
    t = one(rows)
    assert t["side"] == "short"
    assert approx(t["entry_price"], 99.99), t              # open 100 - 1 tick (sell)
    assert t["exit_reason"] == "Short ATR Stop", t
    assert approx(t["exit_price"], 100.50), t              # stop 100.49 + 1 tick (buy)


def test_na_atr_blocks_entry():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, None, long_c=True),  # atr na
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),
        frow(1550, 101.0, 101.2, 100.8, 101.0, 90.0, 0.50),
    ]
    assert fe.simulate(rows) == [], "entry fired with na ATR"


def test_eod_only_on_1550_bar():
    # position must persist past a non-1550 bar and flatten exactly at 1550
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),
        frow(1545, 100.4, 100.6, 100.3, 100.5, 90.0, 0.50),  # NOT eod, no exit
        frow(1550, 100.5, 100.7, 100.4, 100.6, 90.0, 0.50),  # eod
    ]
    t = one(rows)
    assert t["exit_bar"] == f"{DAY} 15:50" and t["exit_reason"] == "EOD", t


def test_atr_stop_mult_scales_stop_and_risk():
    # low 99.3 hits the 1.0x stop (99.51) but not the 2.0x stop (99.01)
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),
        frow(1010, 100.0, 100.1, 99.30, 99.9, 90.0, 0.50),
        frow(1550, 100.0, 100.1, 99.9, 100.0, 90.0, 0.50),
    ]
    t1 = one(rows)                                  # default mult 1.0
    assert t1["exit_reason"] == "Long ATR Stop" and approx(t1["risk_points"], 0.50)
    t2 = fe.simulate(rows, atr_stop_mult=2.0)
    assert len(t2) == 1 and t2[0]["exit_reason"] == "EOD"   # wider stop not hit
    assert approx(t2[0]["risk_points"], 1.00)       # 1R scales with the multiple


def test_determinism_synthetic():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),
        frow(1550, 101.0, 101.2, 100.8, 101.0, 90.0, 0.50),
    ]
    assert json.dumps(fe.simulate(rows)) == json.dumps(fe.simulate(rows))


def test_summarize_shapes():
    rows = [
        frow(1000, 100, 100.2, 99.9, 100.0, 90.0, 0.50, long_c=True),
        frow(1005, 100.0, 100.5, 99.8, 100.4, 90.0, 0.50),
        frow(1550, 101.0, 101.2, 100.8, 101.0, 90.0, 0.50),
    ]
    s = fe.summarize(fe.simulate(rows))
    assert s["n"] == 1 and s["long"]["n"] == 1 and s["short"]["n"] == 0
    assert set(s["exit_reason_counts"]) == {
        "Long ATR Stop", "Short ATR Stop", "VWAP Failure", "EOD"}


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} FASTALPHA ENGINE TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
