#!/usr/bin/env python3
"""PVAE development analysis (R1 unsealed) — v1.0 · 2026-08-26.

FIRST UNSEALING of the R1 instrumented development capture, authorized by the
owner/HELM development-unseal charge of 2026-08-26 (one interpreted VDC-dev
draw under the frozen §9 budget). Executes EXACTLY the frozen pre-registration:

  - STUDY_CHARTER_v0.1.md Amendment A1 (A1.2 acceptance, A1.4 state variables /
    tercile rule / expansion / persistence / shock);
  - PVAE_ANALYSIS_PREREG_v0.1.md (primary comparison, required reporting,
    park conditions);
  - RUN_VDC_SPY_5m_dev_R1_v1.0.md (admissible R1 == R0 trade set; identity gate
    PASS).

Covariate source: the frozen R1 instrumentation mirror (analysis/
instrumentation_r1.py) over the hash-guarded local SPY corpus. The supplied R1
TradingView chart-data export is only a 300-bar recent visible-window sample and
carries no development-window per-bar stamps, so the frozen local mirror IS the
R1 observational state for development bars (foundation columns proven
byte-identical to R0; PARITY_GATES Gate 2).

Signal/fill timing (frozen, from the R0 parity pass Gate-3 probe): the trade
list Entry "Date and time" is the FILL bar start; the signal-evaluation bar is
fill - 5m. Instrumentation is read at that signal bar's close.

FEED SEAM (recorded, not repaired): the local corpus is split-only; TradingView
R0/R1 is dividend-adjusted (ADJ). Covariates near a threshold can differ from
the exact TV stamp. This script quantifies near-threshold exposure; it does not
adjust, filter, or optimize around it.

FIREWALL: reads instrumentation only at development signal bars (<= 2025-12-31).
No embargo/validation/holdout bar value is inspected. No threshold is moved on
P/L. No new TradingView run. Outputs one JSON evidence file; interprets only the
development trade set.

Exit status: 0 on success; nonzero on any input-identity or containment failure.
"""

import copy
import csv
import datetime as dt
import hashlib
import json
import os
import platform
import sys

import parity_foundation as pf
import instrumentation_r1 as ir

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))

# Admissible R1 trade list == R0 export (identity gate PASS; byte-identical).
TRADELIST = os.path.join(
    STUDY, "exports", "VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0R1.csv")
TRADELIST_SHA256 = (
    "8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241")

DEV_END = "2025-12-31"          # charter A3 development window end (inclusive)
EXPECTED_TRADES = 1331


def sha256_file(path, expected):
    with open(path, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    print(f"input {os.path.relpath(path, STUDY)} sha256 {got}")
    if got != expected:
        sys.exit(f"INPUT IDENTITY FAILURE: {path} sha256 {got} != {expected}")
    return got


def load_trades():
    sha256_file(TRADELIST, TRADELIST_SHA256)
    with open(TRADELIST, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    trades = {}
    for r in rows:
        n = int(r["Trade number"])
        kind = "exit" if r["Type"].startswith("Exit") else "entry"
        trades.setdefault(n, {})[kind] = r
    if len(trades) != EXPECTED_TRADES:
        sys.exit(f"TRADE COUNT {len(trades)} != {EXPECTED_TRADES}")
    return trades


def build_instrumentation_index():
    """Frozen R1 mirror over the hash-guarded corpus; assert containment
    (foundation columns byte-identical), then index rows by signal-bar key
    'YYYY-MM-DDTHH:MM'."""
    feats = pf.compute_features(pf.build_5m_bars(pf.load_corpus_rth()))
    snapshot = copy.deepcopy(feats)
    instr = ir.compute_instrumentation(feats)
    if feats != snapshot:
        sys.exit("CONTAINMENT FAILURE: instrumentation mutated foundation rows")
    for f, r in zip(feats, instr):
        for k in ir.GUARDED_FIELDS:
            if f[k] != r[k]:
                sys.exit(f"CONTAINMENT FAILURE: column {k} altered at "
                         f"{f['et_start']}")
    print(f"containment verified: {len(ir.GUARDED_FIELDS)} foundation columns "
          f"identical across {len(instr)} rows")
    return {r["et_start"][:16]: r for r in instr}


def frozen_terciles(svals):
    """Count-based tercile split of the pooled naked-VDC entry S_9_20_50
    observations. Computed ONCE, from the S_t distribution only (no P/L, no
    side, no outcome). Boundaries frozen on return.

    Method (frozen): sort defined entry S_t ascending; b_lo = value at index
    floor(N/3), b_hi = value at index floor(2N/3) (0-indexed). Membership:
    lower  S_t <  b_lo ; middle  b_lo <= S_t < b_hi ; upper  S_t >= b_hi.
    'Upper development-entry tercile' = the upper group (S_t >= b_hi).
    """
    s = sorted(svals)
    n = len(s)
    b_lo = s[n // 3]
    b_hi = s[(2 * n) // 3]
    counts = {
        "lower": sum(1 for v in s if v < b_lo),
        "middle": sum(1 for v in s if b_lo <= v < b_hi),
        "upper": sum(1 for v in s if v >= b_hi),
    }
    return {
        "method": ("count-based split of pooled defined naked-VDC entry "
                   "S_9_20_50; b_lo=sorted[floor(N/3)], b_hi=sorted[floor(2N/3)]"
                   " (0-indexed); upper tercile = S_t >= b_hi"),
        "n_defined_entry_S": n,
        "b_lo": b_lo,
        "b_hi_upper_boundary": b_hi,
        "tercile_counts": counts,
    }


def grp_stats(pnls):
    n = len(pnls)
    if n == 0:
        return {"n": 0, "expectancy": None, "total_pnl": 0.0,
                "win_rate": None, "expectancy_ex_top": None, "best": None}
    total = sum(pnls)
    wins = sum(1 for p in pnls if p > 0)
    best = max(pnls)
    rest = pnls.copy()
    rest.remove(best)
    return {
        "n": n,
        "expectancy": total / n,
        "total_pnl": total,
        "win_rate": wins / n,
        "wins": wins,
        "best": best,
        "expectancy_ex_top": (sum(rest) / len(rest)) if rest else None,
    }


def contrast_block(rows):
    """rows: list of dicts with keys side, pnl, pvae. Returns pooled/long/short
    PVAE-vs-other stats and expectancy contrasts (PVAE - other)."""
    out = {}
    for label, sel in (("pooled", lambda r: True),
                       ("long", lambda r: r["side"] == "long"),
                       ("short", lambda r: r["side"] == "short")):
        sub = [r for r in rows if sel(r)]
        pv = grp_stats([r["pnl"] for r in sub if r["pvae"]])
        ot = grp_stats([r["pnl"] for r in sub if not r["pvae"]])
        contrast = (pv["expectancy"] - ot["expectancy"]
                    if pv["expectancy"] is not None
                    and ot["expectancy"] is not None else None)
        contrast_ex_top = (pv["expectancy_ex_top"] - ot["expectancy_ex_top"]
                           if pv["expectancy_ex_top"] is not None
                           and ot["expectancy_ex_top"] is not None else None)
        out[label] = {"pvae": pv, "other": ot,
                      "expectancy_contrast_pvae_minus_other": contrast,
                      "expectancy_contrast_ex_top_trade": contrast_ex_top}
    return out


def main():
    print("python", platform.python_version(), "| stdlib only")
    print("PVAE DEVELOPMENT ANALYSIS v1.0 — R1 unsealed (first interpretation)")

    trades = load_trades()
    idx = build_instrumentation_index()

    # ---- Join each trade to its signal-bar instrumentation state ----
    joined = []
    missing_bar = 0
    for n in sorted(trades):
        e = trades[n]["entry"]
        side = "long" if "long" in e["Type"].lower() else "short"
        pnl = float(trades[n]["exit"]["Net PnL USD"])
        fill = dt.datetime.strptime(e["Date and time"], "%Y-%m-%d %H:%M")
        sig = fill - dt.timedelta(minutes=5)
        key = sig.strftime("%Y-%m-%dT%H:%M")
        row = idx.get(key)
        if row is None:
            missing_bar += 1
            joined.append({"n": n, "side": side, "pnl": pnl, "sig_key": key,
                           "row": None})
            continue
        if row["session_date"] > DEV_END:      # firewall guard (must not fire)
            sys.exit(f"FIREWALL VIOLATION: trade {n} signal bar {key} "
                     f"post-development")
        joined.append({"n": n, "side": side, "pnl": pnl, "sig_key": key,
                       "row": row})
    if missing_bar:
        print(f"WARNING: {missing_bar} trades had no local signal bar")

    dir_of = {"long": 1, "short": -1}

    # ---- Frozen tercile boundaries from pooled entry S_9_20_50 (compute once)
    entry_S = [j["row"]["s_9_20_50"] for j in joined
               if j["row"] is not None and j["row"]["s_9_20_50"] is not None]
    terc = frozen_terciles(entry_S)
    b_hi = terc["b_hi_upper_boundary"]
    print("\n=== FROZEN S_9_20_50 DEVELOPMENT-ENTRY TERCILE BOUNDARIES ===")
    print(json.dumps(terc, indent=2))
    print("(boundaries frozen from the S_t distribution only — no P/L, no side, "
          "no outcome inspected to compute them)\n")

    # ---- PVAE classification (all five frozen conditions) ----
    undefined_cov = 0
    for j in joined:
        r = j["row"]
        d = dir_of[j["side"]]
        if r is None:
            j["pvae"] = False
            j["cond"] = None
            continue
        s = r["s_9_20_50"]
        cond = {
            "accept": r["accept_state_dir"] == d,                    # A1.2
            "ordered": r["ordered_9_20_50"] == d,                    # A1.4
            "upper_tercile": (s is not None and s >= b_hi),          # A1.4
            "expanding": r["expanding_9_20_50"] == 1,                # A1.4
            "persist_ge2": (r["aligned_exp_count_9_20_50"] is not None
                            and r["aligned_exp_count_9_20_50"] >= 2),  # A1.4
        }
        if (s is None or r["accept_state_dir"] is None
                or r["ordered_9_20_50"] is None
                or r["expanding_9_20_50"] is None):
            undefined_cov += 1
        j["cond"] = cond
        j["pvae"] = all(cond.values())

    classifiable = [j for j in joined if j["row"] is not None]
    pvae_rows = [j for j in classifiable if j["pvae"]]
    print(f"classifiable trades (local signal bar present): {len(classifiable)}")
    print(f"entries with >=1 undefined covariate (warm-up etc.): {undefined_cov}")
    print(f"PVAE-qualified N: {len(pvae_rows)}  "
          f"non-PVAE N: {len(classifiable) - len(pvae_rows)}")

    # ---- Condition attrition (how many pass each gate; funnel) ----
    def count(pred):
        return sum(1 for j in classifiable if pred(j))
    funnel = {
        "accept": count(lambda j: j["cond"]["accept"]),
        "accept+ordered": count(lambda j: j["cond"]["accept"]
                                and j["cond"]["ordered"]),
        "accept+ordered+upper": count(
            lambda j: j["cond"]["accept"] and j["cond"]["ordered"]
            and j["cond"]["upper_tercile"]),
        "accept+ordered+upper+expanding": count(
            lambda j: j["cond"]["accept"] and j["cond"]["ordered"]
            and j["cond"]["upper_tercile"] and j["cond"]["expanding"]),
        "all5_pvae": count(lambda j: j["pvae"]),
    }

    # ---- Primary comparison: PVAE vs other, pooled/long/short ----
    contrasts = contrast_block(classifiable)

    print("\n=== PRIMARY: PVAE vs non-PVAE expectancy (per-trade Net PnL USD) ===")
    for label in ("pooled", "long", "short"):
        c = contrasts[label]
        pv, ot = c["pvae"], c["other"]
        print(f"[{label}] PVAE  n={pv['n']:<4} "
              f"exp={_f(pv['expectancy'])} win={_p(pv['win_rate'])} "
              f"tot={_f(pv['total_pnl'])}")
        print(f"[{label}] other n={ot['n']:<4} "
              f"exp={_f(ot['expectancy'])} win={_p(ot['win_rate'])} "
              f"tot={_f(ot['total_pnl'])}")
        print(f"[{label}] contrast (PVAE-other) = "
              f"{_f(c['expectancy_contrast_pvae_minus_other'])}   "
              f"ex-top-trade = {_f(c['expectancy_contrast_ex_top_trade'])}")

    # ---- Secondary descriptive covariates (no thresholds, no optimization) ----
    def desc(selector):
        vals = [selector(j["row"]) for j in pvae_rows
                if selector(j["row"]) is not None]
        allv = [selector(j["row"]) for j in classifiable
                if selector(j["row"]) is not None]
        return {"pvae_available": len(vals),
                "pvae_mean": (sum(vals) / len(vals)) if vals else None,
                "all_available": len(allv),
                "all_mean": (sum(allv) / len(allv)) if allv else None}
    secondary = {
        "recent_shock": desc(lambda r: r["recent_shock"]),
        "s_10_22_55": desc(lambda r: r["s_10_22_55"]),
        "ordered_10_22_55_agrees_side": {
            "pvae_share_agree": _share(
                pvae_rows, lambda j: j["row"]["ordered_10_22_55"]
                == dir_of[j["side"]]),
            "all_share_agree": _share(
                classifiable, lambda j: j["row"]["ordered_10_22_55"]
                == dir_of[j["side"]]),
        },
    }

    # ---- Feed-seam exposure: entries whose S_t sits within +/-5% of b_hi ----
    band = 0.05 * b_hi
    near_boundary = sum(1 for j in classifiable
                        if j["row"]["s_9_20_50"] is not None
                        and abs(j["row"]["s_9_20_50"] - b_hi) <= band)
    seam = {
        "note": ("local split-only feed vs TV ADJ; covariates near a threshold "
                 "may differ from the exact TV stamp. Descriptive exposure only."),
        "entries_within_5pct_of_upper_boundary": near_boundary,
        "r0_parity_candidate_flips_53_of_1331": True,
    }

    # ---- Park-rule evaluation (frozen; no rescue) ----
    pooled_c = contrasts["pooled"]["expectancy_contrast_pvae_minus_other"]
    long_c = contrasts["long"]["expectancy_contrast_pvae_minus_other"]
    short_c = contrasts["short"]["expectancy_contrast_pvae_minus_other"]
    park = {
        "A_pvae_N_lt_30": len(pvae_rows) < 30,
        "B_pooled_contrast_le_0": (pooled_c is not None and pooled_c <= 0),
        "C_long_short_signs_disagree": (
            long_c is not None and short_c is not None
            and (long_c > 0) != (short_c > 0)),
        "D_requires_rule_change": (
            "n/a — no rule/threshold/persistence/acceptance change was made or "
            "explored; primary computed once under the frozen definitions"),
        "E_validation": "not evaluated — validation remains sealed",
    }
    if park["A_pvae_N_lt_30"]:
        disposition = "PVAE INSUFFICIENT / PARKED (A: qualified N < 30)"
    elif park["B_pooled_contrast_le_0"]:
        disposition = "PVAE DEVELOPMENT SIGNAL ABSENT / PARKED (B: pooled contrast <= 0)"
    elif park["C_long_short_signs_disagree"]:
        disposition = "SYMMETRIC PVAE PARKED (C: long/short contrast signs disagree)"
    else:
        disposition = "PVAE DEVELOPMENT SIGNAL PRESENT (pending owner/HELM validation decision)"

    print("\n=== PARK-RULE EVALUATION ===")
    print(json.dumps(park, indent=2))
    print(f"\nDEVELOPMENT DISPOSITION: {disposition}")
    validation_earned = disposition.startswith("PVAE DEVELOPMENT SIGNAL PRESENT")
    print(f"ONE PLANNED VALIDATION LOOK EARNED: {validation_earned}")

    results = {
        "role": "PVAE development analysis (R1 first unsealing) — frozen prereg",
        "authority": ("owner/HELM development-unseal charge 2026-08-26; "
                      "STUDY_CHARTER Amendment A1; PVAE_ANALYSIS_PREREG_v0.1; "
                      "RUN_VDC_SPY_5m_dev_R1_v1.0"),
        "trade_list_sha256": TRADELIST_SHA256,
        "corpus_sha256": pf.CANONICAL_SHA256,
        "n_trades": len(trades),
        "signal_fill_timing": "signal bar = entry fill time - 5m (frozen)",
        "covariate_source": ("frozen local R1 instrumentation mirror; foundation "
                             "byte-identical to R0"),
        "trades_missing_local_signal_bar": missing_bar,
        "entries_with_undefined_covariate": undefined_cov,
        "frozen_terciles": terc,
        "pvae_condition_funnel": funnel,
        "pvae_N": len(pvae_rows),
        "non_pvae_N": len(classifiable) - len(pvae_rows),
        "contrasts": contrasts,
        "secondary_descriptive": secondary,
        "feed_seam": seam,
        "park_rules": park,
        "development_disposition": disposition,
        "one_validation_look_earned": validation_earned,
    }
    out = os.path.join(HERE, "PVAE_DEV_RESULTS_2026-08-26.json")
    with open(out, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"\nresults written: {os.path.relpath(out, STUDY)}")


def _f(x):
    return "   None" if x is None else f"{x:+.4f}"


def _p(x):
    return "  None" if x is None else f"{100*x:5.2f}%"


def _share(rows, pred):
    if not rows:
        return None
    return sum(1 for j in rows if pred(j)) / len(rows)


if __name__ == "__main__":
    main()
