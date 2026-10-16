#!/usr/bin/env python3
"""Bounded deterministic tests for the EMA-surface topology classifier.

Feeds the pure classifier synthetic 3x3 surfaces (expectancy_r per cell) that
exercise each predeclared branch, isolating the classification logic from the
engine/corpus. Run: python3 test_ema_surface.py
"""
import sys

import ema_surface as es

FAST, SLOW = es.FROZEN_FAST, es.FROZEN_SLOW      # [8,9,10], [18,20,22]
CTRL = es.CONTROL                                # (9,20)


def grid(vals):
    """vals: dict '{f}/{s}' -> expectancy_r, or a flat value for a uniform grid."""
    if isinstance(vals, (int, float)):
        return {(f, s): float(vals) for f in FAST for s in SLOW}
    return {(f, s): vals[f"{f}/{s}"] for f in FAST for s in SLOW}


def ls_all(long_r, short_r):
    return {(f, s): (long_r, short_r) for f in FAST for s in SLOW}


def classify(expr_s, expr_r=None, long_r=0.05, short_r=-0.03):
    if expr_r is None:
        expr_r = dict(expr_s)
    return es.classify(expr_s, expr_r, ls_all(long_r, short_r), ls_all(long_r, short_r))


def test_flat_parameter_insensitive():
    # every cell within a hair -> spread < MATERIAL_R
    g = grid({f"{f}/{s}": 0.010 + 0.001 * (f - 9) for f in FAST for s in SLOW})
    c = classify(g)
    assert c["response_shape"].startswith("5."), c["response_shape"]
    assert c["disposition_label"] == "EMA SURFACE PARAMETER-INSENSITIVE"


def test_broad_stable_region():
    # 8 of 9 cells clustered high, one distant low corner
    base = {f"{f}/{s}": 0.10 for f in FAST for s in SLOW}
    base["10/22"] = -0.20                     # one materially-lower cell
    c = classify(grid(base))
    assert c["response_shape"].startswith("1."), c["response_shape"]
    assert c["disposition_label"] == "EMA SURFACE BROADLY ROBUST"
    assert c["near_best_contiguous"] is True


def test_isolated_peak():
    # one cell far above every neighbour; the rest in a tight low band
    base = {f"{f}/{s}": 0.00 for f in FAST for s in SLOW}
    base["9/20"] = 0.40                        # isolated peak at the interior control
    c = classify(grid(base))
    assert c["response_shape"].startswith("4."), c["response_shape"]
    assert c["disposition_label"] == "EMA SURFACE SHOWS ISOLATED OPTIMUM"
    assert c["best_cell"] == "9/20"


def test_unstable_conflicted_raw_screened_disagree():
    # screened and raw flip sign vs control on a majority of non-control cells
    s = {f"{f}/{s}": 0.02 * (f - 9) + 0.03 * (s - 20) / 2 for f in FAST for s in SLOW}
    r = {k: -v for k, v in s.items()}          # raw is the mirror -> most cells flip
    c = classify(grid(s), grid(r))
    assert c["response_shape"].startswith("6."), c["response_shape"]
    assert c["disposition_label"] == "EMA SURFACE UNSTABLE"
    assert len(c["raw_screened_cells_disagreeing_on_direction"]) >= 4


def test_monotonic_gradient():
    # expectancy rises coherently with fast length; slow flat
    base = {f"{f}/{s}": 0.05 * (f - 8) for f in FAST for s in SLOW}
    c = classify(grid(base))
    assert c["response_shape"].startswith("3."), c["response_shape"]
    assert c["fast_marginal"]["direction"] == "increasing"
    assert c["slow_marginal"]["spread_r"] == 0.0


def test_directional_asymmetry_persistent_vs_absent():
    g = grid(0.01)
    cp = classify(g, long_r=0.05, short_r=-0.03)
    assert cp["directional_asymmetry"]["verdict"] == "PERSISTENT"
    ca = classify(g, long_r=-0.02, short_r=0.02)   # inverted -> pattern absent
    assert ca["directional_asymmetry"]["verdict"] == "ABSENT"


def test_control_and_1022_flags():
    # broad-stable grid where control and 10/22 are both near the top
    base = {f"{f}/{s}": 0.10 for f in FAST for s in SLOW}
    base["8/18"] = -0.30
    c = classify(grid(base))
    assert c["control_9_20_within_stable_region"] is True
    assert c["ema_10_22_consistent_with_surface"] is True


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} EMA-SURFACE CLASSIFIER TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
