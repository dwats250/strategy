#!/usr/bin/env python3
"""V1 (EMA 10/22) controlled-perturbation static diff proof + candidate sanity.

Proves that scripts/VWAP_Continuation_FastAlpha_V1_EMA10_22.pine is the smallest
controlled variant of the v0 base — the ONLY strategy-semantic change is the
FastAlpha trading EMA pair 9/20 -> 10/22 — and runs a flat-agnostic candidate
sanity comparison against v0 over the development window.

NO OUTCOME ANALYSIS: no fills, no P/L, no expectancy, no trades are simulated.
The sanity section compares LOCAL SEMANTIC CANDIDATES only (the same
flat-agnostic objects parity_foundation already computes), over 2024-09-03 ->
2025-12-31; it never inspects embargo/validation/holdout, and never reads a
trade outcome. Deterministic, stdlib-only. Exit 0 on proof success, nonzero on
any classification or containment failure.
"""

import copy
import datetime as dt
import hashlib
import os
import re
import sys

import parity_foundation as pf

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
SCRIPTS = os.path.join(STUDY, "scripts")

V0 = os.path.join(SCRIPTS, "VWAP_Continuation_FastAlpha_v0.pine")
V1 = os.path.join(SCRIPTS, "VWAP_Continuation_FastAlpha_V1_EMA10_22.pine")
V0_SHA = "c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e"

DEV_END = "2025-12-31"

# Lines (1-indexed) expected to differ, with their classification.
EXPECT_DIFF = {
    3:  "identity (strategy title string) — non-semantic",
    4:  "identity (shorttitle string) — non-semantic",
    79: "SEMANTIC: EMA_FAST_LEN 9 -> 10 (trading fast EMA length)",
    80: "SEMANTIC: EMA_SLOW_LEN 20 -> 22 (trading slow EMA length)",
}


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def strip_comments_and_strings(line):
    """Neutralize non-semantic text: remove // comment to EOL and blank every
    double-quoted string literal. Leaves code tokens (incl. numeric literals)
    intact, so identity/title/plot-title/guard-message text cannot register as
    a semantic difference, but an EMA length literal does."""
    out, i, n, in_str = [], 0, len(line), False
    while i < n:
        ch = line[i]
        if not in_str and line[i:i + 2] == "//":
            break
        if ch == '"':
            in_str = not in_str
            out.append('"')
            i += 1
            continue
        if not in_str:
            out.append(ch)
        i += 1
    return re.sub(r'"[^"]*"', '""', "".join(out)).rstrip()


def main():
    print("python", __import__("platform").python_version(), "| stdlib only")

    # ---- Input identity ----
    v0_sha, v1_sha = sha256_file(V0), sha256_file(V1)
    print(f"v0 sha256 {v0_sha}")
    print(f"V1 sha256 {v1_sha}")
    if v0_sha != V0_SHA:
        sys.exit(f"BASE IDENTITY FAILURE: v0 sha {v0_sha} != {V0_SHA}")
    if v1_sha == v0_sha:
        sys.exit("PROOF FAILURE: V1 is byte-identical to v0 (no change made)")

    v0_lines = open(V0).read().split("\n")
    v1_lines = open(V1).read().split("\n")
    if len(v0_lines) != len(v1_lines):
        sys.exit(f"PROOF FAILURE: line count differs "
                 f"({len(v0_lines)} vs {len(v1_lines)}) — not a minimal variant")

    # ---- (1) Raw byte-level diff: exactly the 4 expected lines ----
    diff_lines = [i + 1 for i, (a, b) in enumerate(zip(v0_lines, v1_lines))
                  if a != b]
    print("\n=== (1) RAW LINE DIFF (v0 -> V1) ===")
    for ln in diff_lines:
        print(f"  line {ln}: {EXPECT_DIFF.get(ln, 'UNEXPECTED')}")
        print(f"    - {v0_lines[ln - 1].strip()}")
        print(f"    + {v1_lines[ln - 1].strip()}")
    if set(diff_lines) != set(EXPECT_DIFF):
        sys.exit(f"PROOF FAILURE: differing lines {diff_lines} != "
                 f"expected {sorted(EXPECT_DIFF)} — variant is not minimal")

    # ---- (2) Semantic-normalized diff: only the two EMA constants remain ----
    v0_norm = [strip_comments_and_strings(l) for l in v0_lines]
    v1_norm = [strip_comments_and_strings(l) for l in v1_lines]
    sem_diff = [i + 1 for i, (a, b) in enumerate(zip(v0_norm, v1_norm))
                if a != b]
    print("\n=== (2) SEMANTIC-NORMALIZED DIFF (comments + string literals "
          "neutralized) ===")
    for ln in sem_diff:
        print(f"  line {ln}:  {v0_norm[ln - 1].strip()}   ->   "
              f"{v1_norm[ln - 1].strip()}")
    if sem_diff != [79, 80]:
        sys.exit(f"PROOF FAILURE: semantic diff at lines {sem_diff}, "
                 f"expected exactly [79, 80] (the EMA length constants)")
    # exact token check
    checks = [
        ("int EMA_FAST_LEN = 9", "int EMA_FAST_LEN = 10", 79),
        ("int EMA_SLOW_LEN = 20", "int EMA_SLOW_LEN = 22", 80),
    ]
    for want0, want1, ln in checks:
        if v0_lines[ln - 1].strip() != want0 or v1_lines[ln - 1].strip() != want1:
            sys.exit(f"PROOF FAILURE: line {ln} not the expected EMA constant "
                     f"change")
    print("\nPROOF: the ONLY strategy-semantic change is the FastAlpha trading "
          "EMA pair 9/20 -> 10/22 (lines 79-80). Lines 3-4 are identity strings "
          "(non-semantic). All other bytes are identical.")

    # ---- (3) Local semantic candidate sanity (flat-agnostic; NO OUTCOMES) ----
    # Same corpus for both, so the split-only/ADJ feed seam cancels in the
    # differential; this isolates the EMA-length perturbation on trigger state.
    feats0 = pf.compute_features(pf.build_5m_bars(pf.load_corpus_rth()))
    save_fast, save_slow = pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN
    try:
        pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN = 10, 22
        feats1 = pf.compute_features(pf.build_5m_bars(pf.load_corpus_rth()))
    finally:
        pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN = save_fast, save_slow
    if (pf.EMA_FAST_LEN, pf.EMA_SLOW_LEN) != (9, 20):
        sys.exit("SANITY FAILURE: parity_foundation module state not restored")

    dev0 = [f for f in feats0 if f["session_date"] <= DEV_END]
    dev1 = [f for f in feats1 if f["session_date"] <= DEV_END]
    assert len(dev0) == len(dev1)
    long0 = sum(1 for f in dev0 if f["long_candidate"])
    short0 = sum(1 for f in dev0 if f["short_candidate"])
    long1 = sum(1 for f in dev1 if f["long_candidate"])
    short1 = sum(1 for f in dev1 if f["short_candidate"])
    long_flips = sum(1 for a, b in zip(dev0, dev1)
                     if a["long_candidate"] != b["long_candidate"])
    short_flips = sum(1 for a, b in zip(dev0, dev1)
                      if a["short_candidate"] != b["short_candidate"])
    print("\n=== (3) LOCAL SEMANTIC CANDIDATE SANITY — dev window "
          f"2024-09-03..{DEV_END}, flat-agnostic, NO P/L ===")
    print(f"  dev 5m bars: {len(dev0)}")
    print(f"  long_candidate  v0(9/20)={long0}  V1(10/22)={long1}  "
          f"bars differing={long_flips}")
    print(f"  short_candidate v0(9/20)={short0}  V1(10/22)={short1}  "
          f"bars differing={short_flips}")
    print("  (candidate-state only — confirms the perturbation is live and "
          "bounded; no trades, fills, or outcomes computed)")
    if long_flips == 0 and short_flips == 0:
        sys.exit("SANITY FAILURE: EMA 10/22 produced identical candidates to "
                 "9/20 — perturbation appears inert (unexpected)")

    print("\nV1 CONTROLLED-PERTURBATION PROOF: PASS")


if __name__ == "__main__":
    main()
