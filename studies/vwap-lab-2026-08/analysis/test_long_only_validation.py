#!/usr/bin/env python3
"""Bounded tests for the FROZEN long-only-validation decision function.

Exercises every branch of `classify()` on synthetic arm-report dicts (no engine,
no corpus, no validation data) so the pre-registered A/B/C + strength logic is
verified independently of any outcome. Run: python3 test_long_only_validation.py
"""
import sys

import long_only_validation as v


def arm(exp_r, short_r=None):
    return {"expectancy_r": exp_r, "short_expectancy_r": short_r}


def test_strong_confirmation():
    # A,B,C pass; raw agrees on signs; block CI lower bound > 0
    c = v.classify(arm(0.05), arm(0.01, short_r=-0.03),
                   arm(0.04), arm(0.008, short_r=-0.02), lo_block_ci_lower=0.005)
    assert c["screened_ABC_pass"] and c["raw_sign_agreement_ABC"]
    assert c["verdict"] == "STRONG CONFIRMATION", c


def test_directional_replication():
    # A,B,C pass; raw agrees; but block CI includes zero
    c = v.classify(arm(0.05), arm(0.01, short_r=-0.03),
                   arm(0.04), arm(0.008, short_r=-0.02), lo_block_ci_lower=-0.01)
    assert c["verdict"] == "DIRECTIONAL REPLICATION", c


def test_fails_when_A_false():
    c = v.classify(arm(-0.01), arm(-0.02, short_r=-0.03),
                   arm(-0.01), arm(-0.02, short_r=-0.03), lo_block_ci_lower=-0.05)
    assert c["verdict"] == "FAILS VALIDATION", c


def test_fails_when_C_false():
    # long-only positive and > symmetric, but symmetric short is NOT negative
    c = v.classify(arm(0.05), arm(0.01, short_r=0.02),
                   arm(0.05), arm(0.01, short_r=0.02), lo_block_ci_lower=0.01)
    assert c["C_symmetric_short_expectancy_r_lt_0"] is False
    assert c["verdict"] == "FAILS VALIDATION", c


def test_conflicted_when_raw_sign_disagrees():
    # screened A/B/C pass, but raw long-only expectancy flips negative (A sign differs)
    c = v.classify(arm(0.05), arm(0.01, short_r=-0.03),
                   arm(-0.02), arm(0.03, short_r=-0.02), lo_block_ci_lower=0.01)
    assert c["screened_ABC_pass"] is True
    assert c["raw_sign_agreement_ABC"] is False
    assert c["verdict"] == "CONFLICTED VALIDATION", c


def main():
    tests = [x for k, x in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\nALL {len(tests)} LONG-ONLY-VALIDATION CLASSIFIER TESTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
