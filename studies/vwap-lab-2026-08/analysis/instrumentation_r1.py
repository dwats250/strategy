#!/usr/bin/env python3
"""R1 instrumentation mirror — observational covariates only · v1.0 · 2026-08-25.

Local mirror of the R1 Pine instrumentation section
(scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine), computing
the Amendment A1 / PVAE-prereg covariate series on top of the untouched
parity foundation. Definitions mirrored exactly, including the recorded
interpretations:

  - A1.2 acceptance votes compare each of the four completed current-session
    closes against ITS OWN bar's session VWAP; ties count toward neither
    side; unavailable (None) until four current-session bars have completed.
  - ALIGNED_EXP_COUNT counts direction-consistent runs; a direction flip
    while aligned-and-expanding starts a new run at 1.
  - RECENT_SHOCK is None until all four window ShockRatio values exist
    (mirrors the Pine's explicit na guard).

This module is ADDITIVE ONLY: it never modifies a foundation row or any
trading-semantics column, and `main()` asserts both (fails nonzero
otherwise). It computes no entries, no exits, no P/L, no expectancy, and no
tercile boundaries (those are frozen later from R1 TradingView entry stamps
per A1.4 — never from this mirror).
"""

import copy
import gzip
import hashlib
import io
import csv
import json
import os
import platform
import sys

import parity_foundation as pf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DERIVED_DIR = os.path.join(DATA, "cache", "derived")

EMA_MID_LEN = 50
ALT_FAST_LEN, ALT_MID_LEN, ALT_SLOW_LEN = 10, 22, 55
ACCEPT_WINDOW = 4
ACCEPT_MIN_VOTES = 3
SHOCK_WINDOW = 4          # current + previous 3 completed bars

INSTR_FIELDS = [
    "accept_state_dir",
    "ema50",
    "s_9_20_50",
    "ordered_9_20_50",
    "expanding_9_20_50",
    "aligned_exp_count_9_20_50",
    "shock_ratio",
    "recent_shock",
    "s_10_22_55",
    "ordered_10_22_55",
]

# Trading-semantics columns that must pass through byte-identical.
GUARDED_FIELDS = pf.FEATURE_FIELDS


def vote_sign(close, vwap):
    """A1.2 vote for one completed bar: close vs that bar's session VWAP.
    Tie (or missing value) counts toward neither side."""
    if close is None or vwap is None:
        return 0
    return 1 if close > vwap else (-1 if close < vwap else 0)


def accept_state(closes4, vwaps4):
    """A1.2 classification given exactly the four most recently completed
    current-session (close, vwap) pairs, oldest first. Returns 1 / -1 / 0."""
    signs = [vote_sign(c, v) for c, v in zip(closes4, vwaps4)]
    long_votes = sum(1 for s in signs if s == 1)
    short_votes = sum(1 for s in signs if s == -1)
    last = vote_sign(closes4[-1], vwaps4[-1])
    if long_votes >= ACCEPT_MIN_VOTES and last == 1:
        return 1
    if short_votes >= ACCEPT_MIN_VOTES and last == -1:
        return -1
    return 0


def ordered_dir(fast, mid, slow):
    """Directional full ordering: 1 if fast>mid>slow, -1 mirrored, else 0;
    None while any input is None (warm-up)."""
    if fast is None or mid is None or slow is None:
        return None
    if fast > mid > slow:
        return 1
    if fast < mid < slow:
        return -1
    return 0


def dispersion(fast, slow, atr):
    """S = abs(fast - slow) / ATR14; None while any input is None."""
    if fast is None or slow is None or atr is None:
        return None
    return abs(fast - slow) / atr


def expanding_flag(s_now, s_2back):
    """A1.4: expanding_t = S_t > S_(t-2), strict; None during warm-up."""
    if s_now is None or s_2back is None:
        return None
    return 1 if s_now > s_2back else 0


def consec_update(prev_count, prev_dir, dir_now, expanding_now):
    """Aligned-expansion consecutive count (direction-consistent run).
    Not aligned-and-expanding -> 0; run continues only while the ordered
    direction is unchanged; a flip starts a new run at 1."""
    aligned_now = (dir_now is not None and dir_now != 0
                   and expanding_now == 1)
    if not aligned_now:
        return 0
    if prev_count > 0 and dir_now == prev_dir:
        return prev_count + 1
    return 1


def recent_shock(shocks_window):
    """A1.4: max ShockRatio over current + previous 3 completed bars; None
    unless all four values exist (mirrors the Pine na guard exactly)."""
    if len(shocks_window) < SHOCK_WINDOW or any(
            s is None for s in shocks_window):
        return None
    return max(shocks_window)


def compute_instrumentation(feats):
    """Return new rows = foundation rows + instrumentation columns.
    Input rows are not mutated."""
    closes = [f["c"] for f in feats]
    ema50 = pf.ema(closes, EMA_MID_LEN)
    ema10 = pf.ema(closes, ALT_FAST_LEN)
    ema22 = pf.ema(closes, ALT_MID_LEN)
    ema55 = pf.ema(closes, ALT_SLOW_LEN)
    trs = pf.true_ranges(feats)

    out = []
    s_series = []
    session_bars = 0
    prev_date = None
    prev_count = 0
    prev_dir = None
    shock_series = []
    for i, f in enumerate(feats):
        row = dict(f)

        # A1.2 acceptance state
        if f["session_date"] != prev_date:
            session_bars = 1
            prev_date = f["session_date"]
        else:
            session_bars += 1
        if session_bars >= ACCEPT_WINDOW:
            window = feats[i - ACCEPT_WINDOW + 1:i + 1]
            row["accept_state_dir"] = accept_state(
                [w["c"] for w in window],
                [w["session_vwap"] for w in window])
        else:
            row["accept_state_dir"] = None

        # A1.4 executed family 9/20/50
        row["ema50"] = ema50[i]
        s = dispersion(f["ema9"], ema50[i], f["atr14"])
        s_series.append(s)
        row["s_9_20_50"] = s
        d = ordered_dir(f["ema9"], f["ema20"], ema50[i])
        row["ordered_9_20_50"] = d
        exp = expanding_flag(s, s_series[i - 2] if i >= 2 else None)
        row["expanding_9_20_50"] = exp
        count = consec_update(prev_count, prev_dir, d, exp)
        row["aligned_exp_count_9_20_50"] = count
        prev_count, prev_dir = count, d

        # A1.4 shock
        atr_prev = feats[i - 1]["atr14"] if i >= 1 else None
        shock = (trs[i] / atr_prev) if atr_prev is not None else None
        shock_series.append(shock)
        row["shock_ratio"] = shock
        row["recent_shock"] = recent_shock(
            shock_series[max(0, i - SHOCK_WINDOW + 1):i + 1])

        # A1.4 observational-only alternate family 10/22/55
        row["s_10_22_55"] = dispersion(ema10[i], ema55[i], f["atr14"])
        row["ordered_10_22_55"] = ordered_dir(ema10[i], ema22[i], ema55[i])

        out.append(row)
    return out


def main():
    print("python", platform.python_version(), "| stdlib only")
    print(f"input corpus sha256 {pf.CANONICAL_SHA256} "
          f"(guarded by parity_foundation)")

    feats = pf.compute_features(pf.build_5m_bars(pf.load_corpus_rth()))
    snapshot = copy.deepcopy(feats)

    instr = compute_instrumentation(feats)

    # Containment proof 1: the foundation rows were not mutated.
    if feats != snapshot:
        sys.exit("R1 CONTAINMENT FAILURE: compute_instrumentation mutated "
                 "foundation rows")
    # Containment proof 2: every trading-semantics column passes through
    # unchanged — R1 local candidates ARE the R0 foundation candidates.
    for f, r in zip(feats, instr):
        for k in GUARDED_FIELDS:
            if f[k] != r[k]:
                sys.exit(f"R1 CONTAINMENT FAILURE: column {k} altered at "
                         f"{f['et_start']}")
    print(f"containment verified: {len(GUARDED_FIELDS)} foundation columns "
          f"identical across {len(instr)} rows; "
          f"long/short candidates unchanged")

    os.makedirs(DERIVED_DIR, exist_ok=True)
    stem = "SPY_5m_RTH_features_R1instr_2024-09-03_2026-08-21"
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=GUARDED_FIELDS + INSTR_FIELDS)
    writer.writeheader()
    writer.writerows(instr)
    payload = gzip.compress(buf.getvalue().encode(), mtime=0)
    out_path = os.path.join(DERIVED_DIR, f"{stem}.csv.gz")
    with open(out_path, "wb") as fh:
        fh.write(payload)

    # Availability summary — DEVELOPMENT WINDOW ONLY; counts of field
    # availability and state codes. No outcomes, no expectancy, no terciles.
    dev = [r for r in instr if r["session_date"] <= "2025-12-31"]
    summary = {
        "dev_rows": len(dev),
        "accept_state_available": sum(
            1 for r in dev if r["accept_state_dir"] is not None),
        "accept_state_counts": {
            str(k): sum(1 for r in dev if r["accept_state_dir"] == k)
            for k in (1, -1, 0)},
        "ordered_9_20_50_counts": {
            str(k): sum(1 for r in dev if r["ordered_9_20_50"] == k)
            for k in (1, -1, 0)},
        "expanding_available": sum(
            1 for r in dev if r["expanding_9_20_50"] is not None),
        "aligned_exp_count_ge2": sum(
            1 for r in dev if r["aligned_exp_count_9_20_50"] >= 2),
        "recent_shock_available": sum(
            1 for r in dev if r["recent_shock"] is not None),
    }

    manifest = {
        "role": "R1 INSTRUMENTATION MIRROR — foundation columns unchanged + "
                "A1/PVAE observational covariates; no simulation, no P/L, "
                "no terciles",
        "pine_source": "scripts/VWAP_Continuation_FastAlpha_v0_R1_"
                       "instrumented_v1.0.pine",
        "input_canonical_sha256": pf.CANONICAL_SHA256,
        "rows": len(instr),
        "derived_path": os.path.relpath(out_path, DATA),
        "derived_sha256": hashlib.sha256(payload).hexdigest(),
        "dev_window_availability": summary,
    }
    man_path = os.path.join(DERIVED_DIR, f"{stem}.manifest.json")
    with open(man_path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
