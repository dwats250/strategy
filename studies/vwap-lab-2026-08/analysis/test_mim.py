#!/usr/bin/env python3
"""Bounded deterministic tests for MIM-0 (mim.py) on SYNTHETIC data.

No corpus, no development outcomes: exercises the clock semantics, the OLS/HC1
regression, the sign strategy, the frozen cost views, and the kill/advance gates on
hand-built inputs. Run: python3 test_mim.py
"""
import sys

import mim


def bar(date, hm, o, c):
    return {"et_iso": f"{date}T{hm}:00", "o": o, "h": max(o, c), "l": min(o, c), "c": c}


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_clock_semantics_and_skip_early_close():
    rows = []
    # prev session (final close 100 at 15:59)
    rows += [bar("2024-09-03", "09:59", 99, 99.5), bar("2024-09-03", "15:30", 99.8, 100.2),
             bar("2024-09-03", "15:59", 100.1, 100.0)]
    # current full session: 09:59 close 101, 15:30 open 102, 15:59 close 103
    rows += [bar("2024-09-04", "09:59", 100.5, 101.0), bar("2024-09-04", "15:30", 102.0, 102.5),
             bar("2024-09-04", "15:59", 102.9, 103.0)]
    # early-close session: no 15:59 bar -> must be skipped
    rows += [bar("2024-09-05", "09:59", 103.0, 103.5), bar("2024-09-05", "12:59", 104.0, 104.0)]
    obs = mim.build_observations(rows)
    assert len(obs) == 1, obs                       # only 2024-09-04
    o = obs[0]
    assert o["date"] == "2024-09-04"
    assert approx(o["previous_close"], 100.0) and approx(o["price_10_00"], 101.0)
    assert approx(o["late_open"], 102.0) and approx(o["late_close"], 103.0)
    assert approx(o["early_return"], 101.0 / 100.0 - 1)      # crosses previous close
    assert approx(o["late_return"], 103.0 / 102.0 - 1)


def test_dividend_neutral_early_return():
    # ordinary session: no adjustment; ex-dividend session: +cash added to P_10_00.
    rows = []
    rows += [bar("2024-12-19", "09:59", 99, 99.5), bar("2024-12-19", "15:30", 99.8, 100.2),
             bar("2024-12-19", "15:59", 100.1, 100.0)]        # prev close 100.0
    rows += [bar("2024-12-20", "09:59", 98.3, 98.0), bar("2024-12-20", "15:30", 98.1, 98.4),
             bar("2024-12-20", "15:59", 98.3, 98.5)]          # EX-DIV date, price dropped
    exd = {"2024-12-20": 1.965548}
    ordinary = mim.build_observations(rows)                    # no ex_dividends
    adjusted = mim.build_observations(rows, ex_dividends=exd)
    o0 = ordinary[0]; a0 = adjusted[0]
    assert o0["date"] == a0["date"] == "2024-12-20"
    assert not o0["is_ex_dividend"] and a0["is_ex_dividend"]
    assert approx(o0["early_return"], (98.0 - 100.0) / 100.0)               # raw drop
    assert approx(a0["early_return"], (98.0 + 1.965548 - 100.0) / 100.0)    # dividend-neutral
    assert a0["early_return"] > o0["early_return"]             # adjustment lifts the ex-date
    assert approx(a0["late_return"], o0["late_return"])        # late unchanged


def test_ols_exact_line():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.0 + 2.0 * xi for xi in x]                # exact y = 1 + 2x
    r = mim.ols_hc1(x, y)
    assert approx(r["beta"], 2.0) and approx(r["intercept"], 1.0)
    assert approx(r["r_squared"], 1.0)
    assert r["t_hc1"] is None                        # zero residuals -> SE 0


def test_ols_positive_beta_noisy():
    x = [i * 0.001 for i in range(-50, 51)]
    y = [0.5 * xi + (0.0001 if i % 2 else -0.0001) for i, xi in enumerate(x)]
    r = mim.ols_hc1(x, y)
    assert r["beta"] > 0 and r["se_hc1_primary"] > 0 and r["t_hc1"] > 0


def test_sign_strategy_directions():
    obs = [
        {"date": "2025-01-02", "early_return": 0.01, "late_return": 0.02,
         "late_open": 100, "previous_close": 99, "price_10_00": 100},   # long -> +200 bps
        {"date": "2025-01-03", "early_return": -0.01, "late_return": 0.02,
         "late_open": 100, "previous_close": 101, "price_10_00": 100},  # short -> -200 bps
        {"date": "2025-01-06", "early_return": 0.0, "late_return": 0.05,
         "late_open": 100, "previous_close": 100, "price_10_00": 100},  # zero -> no trade
    ]
    ss = mim.sign_strategy(obs)
    assert ss["n"] == 2, ss
    assert approx(ss["mean_bps"], 0.0)
    assert ss["long"]["n"] == 1 and ss["short"]["n"] == 1


def test_cost_ordering_and_stress():
    obs = [{"date": "2025-01-02", "early_return": 0.01, "late_return": 0.02,
            "late_open": 550.0, "previous_close": 545, "price_10_00": 550}]
    c = mim.cost_diagnostics(obs)
    assert c["zero_cost_mean_bps"] >= c["lab_slippage_mean_bps"]     # slippage subtracts
    assert approx(c["stress_mean_bps"], c["zero_cost_mean_bps"] - mim.COST_STRESS_RT_BPS)


def test_classify_gates():
    dead_beta = mim.classify({"beta": -0.1}, {"mean_bps": 10}, {"stress_mean_bps": 5})
    assert dead_beta["verdict"] == "FAMILY DEAD"
    dead_gross = mim.classify({"beta": 0.1}, {"mean_bps": -3}, {"stress_mean_bps": -8})
    assert dead_gross["verdict"] == "FAMILY DEAD"
    dead_cost = mim.classify({"beta": 0.1}, {"mean_bps": 3}, {"stress_mean_bps": -2})
    assert dead_cost["verdict"] == "FAMILY DEAD"
    alive = mim.classify({"beta": 0.1}, {"mean_bps": 10}, {"stress_mean_bps": 5})
    assert alive["verdict"].startswith("EDGE CANDIDATE"), alive


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} MIM-0 TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
