#!/usr/bin/env python3
"""Bounded deterministic tests for FPC-0 (first pullback continuation) signals.

Exercises the `signal_mode="fpc"` arm-state added to fastalpha_engine.simulate on
hand-built synthetic feature rows (regime/red/green/window supplied directly, so
these isolate the FPC ENTRY logic from indicator computation). Execution (fills,
ATR stop, thesis/EOD, flat gate) is the shared V0 machinery. The rows also carry
V0 `long_candidate`/`short_candidate` (the frozen VDC rule) so the SAME rows can
be run in "vdc" mode for a direct contrast. Run: python3 test_fpc_signals.py
"""
import sys

import fastalpha_engine as fe

DAY = "2025-01-02"


def frow(hm, o, h, l, c, bull=False, bear=False, vwap=90.0, atr14=1.0,
         in_window=None):
    hh, mm = divmod(hm, 100)
    red = c < o
    green = c > o
    if in_window is None:
        in_window = 935 <= hm < 1530
    return {
        "session_date": DAY, "et_start": f"{DAY}T{hh:02d}:{mm:02d}:00",
        "hm": hm, "o": o, "h": h, "l": l, "c": c,
        "session_vwap": vwap, "atr14": atr14,
        "bullish_state": bull, "bearish_state": bear,
        "red_bar": red, "green_bar": green, "in_entry_window": in_window,
        # frozen V0 (VDC) rule, so the same rows are runnable in vdc mode:
        "long_candidate": in_window and bull and red,
        "short_candidate": in_window and bear and green,
    }


def fpc(rows):
    return fe.simulate(rows, signal_mode="fpc")


def test_fresh_regime_arms_first_red_enters():
    rows = [
        frow(1000, 100, 100.3, 99.9, 100.2, bull=True),   # FRESH bull, green -> arm, no entry
        frow(1005, 100.2, 100.4, 100.0, 100.05, bull=True),  # red, in window -> FPC signal
        frow(1010, 100.1, 100.4, 100.0, 100.3, bull=True),   # fill @ open
        frow(1550, 100.3, 100.4, 100.2, 100.3, bull=True),   # EOD
    ]
    tr = fpc(rows)
    assert len(tr) == 1 and tr[0]["side"] == "long", tr
    assert tr[0]["entry_bar"] == f"{DAY} 10:10", tr        # NOT the fresh bar


def test_skips_green_takes_first_red():
    rows = [
        frow(1000, 100, 100.3, 99.9, 100.2, bull=True),      # fresh, arm
        frow(1005, 100.2, 100.6, 100.1, 100.5, bull=True),   # GREEN -> no signal
        frow(1010, 100.5, 100.7, 100.2, 100.3, bull=True),   # first RED -> signal
        frow(1015, 100.3, 100.6, 100.2, 100.5, bull=True),   # fill
        frow(1550, 100.5, 100.6, 100.4, 100.5, bull=True),
    ]
    tr = fpc(rows)
    assert len(tr) == 1 and tr[0]["entry_bar"] == f"{DAY} 10:15", tr


def test_arming_bar_excluded_even_if_red():
    rows = [
        frow(1000, 100.4, 100.5, 100.0, 100.1, bull=True),   # FRESH bull AND red -> arm, NO entry
        frow(1005, 100.1, 100.3, 100.0, 100.05, bull=True),  # first non-fresh red -> signal
        frow(1010, 100.05, 100.3, 100.0, 100.2, bull=True),  # fill
        frow(1550, 100.2, 100.3, 100.1, 100.2, bull=True),
    ]
    tr = fpc(rows)
    assert len(tr) == 1 and tr[0]["entry_bar"] == f"{DAY} 10:10", tr  # 10:10 not 10:05


def test_out_of_window_red_no_entry():
    rows = [
        frow(1000, 100, 100.3, 99.9, 100.2, bull=True),      # fresh, arm
        frow(1535, 100.2, 100.4, 100.0, 100.05, bull=True),  # red but hm>=1530 -> out of window
        frow(1550, 100.05, 100.2, 100.0, 100.1, bull=True),
    ]
    assert fpc(rows) == [], "entered outside the entry window"


def test_regime_false_disarms_then_new_fresh_rearms():
    rows = [
        frow(1000, 100, 100.3, 99.9, 100.2, bull=True),      # fresh -> arm
        frow(1005, 100.2, 100.3, 100.0, 100.05, bull=False), # regime FALSE -> disarm (red ignored)
        frow(1010, 100.05, 100.2, 100.0, 100.0, bull=False), # still false, red -> nothing
        frow(1015, 100.0, 100.4, 99.9, 100.3, bull=True),    # FRESH again -> re-arm (green)
        frow(1020, 100.3, 100.4, 100.1, 100.15, bull=True),  # first red of new regime -> signal
        frow(1025, 100.15, 100.4, 100.1, 100.3, bull=True),  # fill
        frow(1550, 100.3, 100.4, 100.2, 100.3, bull=True),
    ]
    tr = fpc(rows)
    assert len(tr) == 1 and tr[0]["entry_bar"] == f"{DAY} 10:25", tr


def test_one_entry_per_regime_vdc_would_take_two():
    # fresh bull; first red -> enter; stop-out on the fill bar (regime stays true);
    # a later red while flat+bull -> FPC disarmed (no 2nd), but VDC re-enters.
    rows = [
        frow(1000, 100, 100.3, 99.9, 100.2, bull=True, atr14=0.50),      # fresh, arm
        frow(1005, 100.2, 100.3, 100.0, 100.05, bull=True, atr14=0.50),  # red -> signal
        frow(1010, 100.0, 100.2, 99.00, 99.95, bull=True, atr14=0.50),   # fill 100.01, stop 99.51, low 99.0 -> stop-out; c>vwap so bull holds
        frow(1015, 100.0, 100.3, 99.9, 100.05, bull=True, atr14=0.50),   # red, flat, bull
        frow(1020, 100.05, 100.3, 99.9, 100.2, bull=True, atr14=0.50),   # (vdc 2nd fill)
        frow(1550, 100.2, 100.3, 100.1, 100.2, bull=True, atr14=0.50),
    ]
    lo_fpc = fe.simulate(rows, signal_mode="fpc")
    lo_vdc = fe.simulate(rows, signal_mode="vdc")
    assert len(lo_fpc) == 1, lo_fpc          # first pullback only
    assert len(lo_vdc) == 2, lo_vdc          # repeated opposing-candle entries
    assert lo_fpc[0]["exit_reason"] == "Long ATR Stop", lo_fpc


def test_short_mirror_fresh_bear_first_green():
    rows = [
        frow(1000, 100.1, 100.2, 99.7, 99.8, bear=True, vwap=110.0),   # FRESH bear, red -> arm, no entry
        frow(1005, 99.8, 100.1, 99.7, 100.0, bear=True, vwap=110.0),   # GREEN -> short signal
        frow(1010, 100.0, 100.1, 99.6, 99.7, bear=True, vwap=110.0),   # fill
        frow(1550, 99.7, 99.8, 99.6, 99.7, bear=True, vwap=110.0),     # EOD
    ]
    tr = fpc(rows)
    assert len(tr) == 1 and tr[0]["side"] == "short", tr
    assert tr[0]["entry_bar"] == f"{DAY} 10:10", tr


def test_determinism_fpc():
    rows = [
        frow(1000, 100, 100.3, 99.9, 100.2, bull=True),
        frow(1005, 100.2, 100.4, 100.0, 100.05, bull=True),
        frow(1010, 100.1, 100.4, 100.0, 100.3, bull=True),
        frow(1550, 100.3, 100.4, 100.2, 100.3, bull=True),
    ]
    import json
    assert json.dumps(fpc(rows)) == json.dumps(fpc(rows))


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} FPC-SIGNAL TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
