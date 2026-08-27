#!/usr/bin/env python3
"""Bounded deterministic tests for ODR-0 (odr.py) on SYNTHETIC data. No corpus, no
development outcomes. Run: python3 test_odr.py"""
import sys

import odr


def bar(date, hm, o, c):
    return {"et_iso": f"{date}T{hm}:00", "o": o, "h": max(o, c), "l": min(o, c), "c": c}


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


def _full(date, o0930, o0931, c0959):
    return [bar(date, "09:30", o0930, o0930 + 0.05), bar(date, "09:31", o0931, o0931),
            bar(date, "09:59", c0959 - 0.02, c0959), bar(date, "15:59", c0959, c0959)]


def test_clock_semantics_and_full_session_only():
    rows = _full("2024-09-03", 99.0, 99.1, 100.0)             # prev, final close 100.0
    rows += _full("2024-09-04", 101.0, 101.2, 100.5)          # traded session
    # early close (no 15:59) -> skipped
    rows += [bar("2024-09-05", "09:30", 100.5, 100.6), bar("2024-09-05", "09:31", 100.6, 100.6),
             bar("2024-09-05", "09:59", 100.4, 100.7)]
    obs = odr.build_observations(rows)
    assert len(obs) == 1 and obs[0]["date"] == "2024-09-04", obs
    o = obs[0]
    assert approx(o["previous_close"], 100.0) and approx(o["open_0930"], 101.0)
    assert approx(o["overnight_return"], (101.0 - 100.0) / 100.0)         # crosses prev close
    assert approx(o["first_half_hour_return"], 100.5 / 101.0 - 1)         # 09:30->10:00
    assert approx(o["trade_return"], 100.5 / 101.2 - 1)                   # 09:31->09:59


def test_dividend_neutral_overnight():
    rows = _full("2025-12-18", 99.0, 99.1, 100.0)             # prev close 100.0
    rows += _full("2025-12-19", 98.0, 98.1, 98.4)             # EX-DIV date (price dropped)
    exd = {"2025-12-19": 1.993368}
    ordn = odr.build_observations(rows)[0]
    adj = odr.build_observations(rows, ex_dividends=exd)[0]
    assert approx(ordn["overnight_return"], (98.0 - 100.0) / 100.0)
    assert approx(adj["overnight_return"], (98.0 + 1.993368 - 100.0) / 100.0)
    assert adj["overnight_return"] > ordn["overnight_return"]
    assert approx(adj["first_half_hour_return"], ordn["first_half_hour_return"])   # intraday unchanged


def test_sign_strategy_reversal_direction():
    obs = [
        {"date": "2025-01-02", "overnight_return": 0.01, "trade_return": -0.005,
         "open_0931": 100},   # up overnight -> SHORT -> profit as it falls: +50 bps
        {"date": "2025-01-03", "overnight_return": -0.01, "trade_return": 0.005,
         "open_0931": 100},   # down overnight -> LONG -> profit as it rises: +50 bps
        {"date": "2025-01-06", "overnight_return": 0.0, "trade_return": 0.02,
         "open_0931": 100},   # zero -> no trade
    ]
    ss = odr.sign_strategy(obs)
    assert ss["n"] == 2 and approx(ss["mean_bps"], 50.0), ss
    assert ss["short"]["n"] == 1 and ss["long"]["n"] == 1


def test_classify_gates():
    assert odr.classify({"beta": 0.1}, {"mean_bps": 10}, {"stress_mean_bps": 5})["verdict"] == "FAMILY DEAD"
    assert odr.classify({"beta": -0.1}, {"mean_bps": -3}, {"stress_mean_bps": -8})["verdict"] == "FAMILY DEAD"
    assert odr.classify({"beta": -0.1}, {"mean_bps": 3}, {"stress_mean_bps": -2})["verdict"] == "FAMILY DEAD"
    good = odr.classify({"beta": -0.1}, {"mean_bps": 10}, {"stress_mean_bps": 5})
    assert good["verdict"].startswith("EDGE CANDIDATE"), good


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} ODR-0 TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
