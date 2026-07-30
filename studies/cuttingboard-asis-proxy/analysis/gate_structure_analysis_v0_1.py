#!/usr/bin/env python3
"""Gate-structure analysis of the registered RUN_SPY_1D_2015-01-01 export.

Pre-registered hypotheses: docs/gap-register-2026-07-29.md G-13..G-16 (committed
before this script existed, commit 16ac7fe). Descriptive only: no threshold is
tuned, no engine attribution is made here, and nothing reopens the study.
Conventions: docs/conventions.md §d — this script asserts its headline numbers
and prints the input checksum.

Full-window counts (all exported rows) are reported alongside the declared
2015-01-01+ analysis window where the distinction matters.
"""

import csv
import hashlib
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

EXPORT = Path(__file__).resolve().parent.parent / "exports" / (
    "CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv")
EXPECTED_SHA = "d1b537506ed1cec9559ad9dd66a35d4a9798d751ee1896e07e6e1739dfe0b970"

SOFT = ["g5_stop_defined", "g6_stop_distance", "g7_rr", "g9_earnings_failopen",
        "g10_extension"]
HARD = ["g1_regime", "g2_confidence", "g3_direction", "g4_structure"]


def main():
    data = EXPORT.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    print(f"python {sys.version.split()[0]}  (stdlib only)")
    print(f"input  {EXPORT.name}")
    print(f"sha256 {sha}")
    assert sha == EXPECTED_SHA, "input is not the registered export"

    rows = list(csv.DictReader(data.decode().splitlines()))
    n = len(rows)
    assert n == 3620, n
    f = lambda r, k: float(r[k])

    # Partition sanity
    q = sum(f(r, "qualified") == 1 for r in rows)
    w = sum(f(r, "watchlist") == 1 for r in rows)
    rj = sum(f(r, "rejected") == 1 for r in rows)
    kill = sum(f(r, "kill_switch") == 1 for r in rows)
    assert (q, w, rj, kill) == (200, 297, 3123, 226), (q, w, rj, kill)
    assert q + w + rj == n
    assert all(f(r, "votes_cast") == 8 for r in rows)

    # G-14: Gate 5 tautology
    g5_pass = sum(f(r, "g5_stop_defined") == 1 for r in rows)
    print(f"\nG-14  g5 passes {g5_pass}/{n} (tautology confirmed)")
    assert g5_pass == n

    # G-13: Gate 7 vs regime_code, and rr influence
    ct = Counter((f(r, "regime_code") == 3, f(r, "g7_rr") == 1) for r in rows)
    print("G-13  g7 x regime cross-tab "
          f"(regime3,pass)={ct[(True, True)]} (regime3,fail)={ct[(True, False)]} "
          f"(other,pass)={ct[(False, True)]} (other,fail)={ct[(False, False)]}")
    assert ct[(True, True)] == 0 and ct[(False, False)] == 0, \
        "g7 is NOT a perfect alias of regime_code != 3"
    rr_lo_pass = sum(f(r, "rr") < 2.0 and f(r, "g7_rr") == 1 for r in rows)
    rr_hi_fail = sum(f(r, "rr") > 2.0 and f(r, "g7_rr") == 0 for r in rows)
    print(f"G-13  rr<2.0 yet g7 pass: {rr_lo_pass}; rr>2.0 yet g7 fail: {rr_hi_fail}"
          "  (rr column has no influence)")

    # G-16: row-level identity checks (count identity upgraded to row identity)
    ids = {
        "g1 == (posture_code==1)":
            all((f(r, "g1_regime") == 1) == (f(r, "posture_code") == 1) for r in rows),
        "g4-fail == (regime_code==2)":
            all((f(r, "g4_structure") == 0) == (f(r, "regime_code") == 2) for r in rows),
        "g7-fail == (regime_code==3)":
            all((f(r, "g7_rr") == 0) == (f(r, "regime_code") == 3) for r in rows),
        "g3 == (direction_code!=0)":
            all((f(r, "g3_direction") == 1) == (f(r, "direction_code") != 0) for r in rows),
    }
    print("G-16  row-level identities:")
    for k, v in ids.items():
        print(f"      {k}: {'HOLDS on all rows' if v else 'VIOLATED'}")

    # G-15: Gate 3 is not inert
    g3_fail = sum(f(r, "g3_direction") == 0 for r in rows)
    print(f"G-15  g3 fails {g3_fail}/{n} rows ({100*g3_fail/n:.1f}%) — not inert")
    assert g3_fail == 527, g3_fail

    # Marginal (unique-fail) power among hard-pass, non-kill rows
    hp = [r for r in rows
          if all(f(r, g) == 1 for g in HARD) and f(r, "kill_switch") == 0]
    print(f"\nhard-pass & non-kill rows: {len(hp)}")
    for g in SOFT:
        uniq = sum(f(r, g) == 0 and all(f(r, o) == 1 for o in SOFT if o != g)
                   for r in hp)
        tot = sum(f(r, g) == 0 for r in hp)
        print(f"      {g}: fails {tot}, sole-failure rows {uniq}")

    # Pairwise soft-gate fail overlap
    print("pairwise soft-gate co-failures (hard-pass, non-kill):")
    for a, b in combinations(SOFT, 2):
        both = sum(f(r, a) == 0 and f(r, b) == 0 for r in hp)
        if both:
            print(f"      {a} & {b}: {both}")

    # Hard-gate unique failure (among non-kill rows failing exactly one hard gate)
    nk = [r for r in rows if f(r, "kill_switch") == 0]
    print(f"non-kill rows: {len(nk)}")
    for g in HARD:
        uniq = sum(f(r, g) == 0 and all(f(r, o) == 1 for o in HARD if o != g)
                   for r in nk)
        tot = sum(f(r, g) == 0 for r in nk)
        print(f"      {g}: fails {tot}, sole-hard-failure rows {uniq}")

    # g1 vs g2 row identity (EA5-005 / draft B3: gates 1-2 duplicated)
    g12_diff = sum((f(r, "g1_regime") != f(r, "g2_confidence")) for r in rows)
    print(f"g1 vs g2: differ on {g12_diff}/{n} rows"
          f" ({'row-identical — EA5-005 confirmed empirically' if g12_diff == 0 else 'NOT identical'})")

    # G-16 g4/regime2 violation detail
    v_a = sum(f(r, "g4_structure") == 0 and f(r, "regime_code") != 2 for r in rows)
    v_b = sum(f(r, "g4_structure") == 1 and f(r, "regime_code") == 2 for r in rows)
    print(f"g4-fail/regime2 violations: g4-fail outside regime2: {v_a}; "
          f"g4-pass inside regime2: {v_b}")

    # First-rejection distribution (full window)
    fr = Counter(int(f(r, "first_rejection")) for r in rows)
    print("first_rejection distribution:", dict(sorted(fr.items())))
    assert fr[0] == 200 and fr[1] == 226

    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
