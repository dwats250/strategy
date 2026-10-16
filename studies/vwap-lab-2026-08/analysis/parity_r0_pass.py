#!/usr/bin/env python3
"""R0 ingest + parity pass — v1.0 · 2026-08-25.

Compares the local parity foundation (bars + features from the verified SPY
corpus) against the owner-captured TradingView R0 evidence:

  exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv
      TradingView List-of-Trades export from the R0 chart (AMEX:SPY, ADJ).
  exports/TV_CHARTDATA_BATS_SPY_5m_RTH_2025-08-11_2026-08-25_FastAlphaV0.csv
      TradingView 5m chart-data export (filename provenance: BATS:SPY chart;
      ~20k-bar loaded history starting 2025-08-11; no volume column).

VALIDATION FIREWALL (charter A3): chart-data rows dated after 2025-12-31 ET
are dropped on load before any value column is read. The embargo and
validation/deferred-inspection windows are not inspected by this script.

This is still NOT a backtester. The Gate-3 probe below maps TradingView
entry fills back to signal bars and checks them against LOCAL SEMANTIC
CANDIDATES (flat-agnostic); it simulates nothing.

Per docs/conventions.md §d this script asserts the R0 headline numbers from
the preserved trade list and exits nonzero if they don't reproduce.
"""

import csv
import datetime as dt
import hashlib
import json
import math
import os
import platform
import statistics
import sys
from collections import Counter
from zoneinfo import ZoneInfo

import parity_foundation as pf

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))
ET = ZoneInfo("America/New_York")

TRADELIST = os.path.join(
    STUDY, "exports", "VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv")
TRADELIST_SHA256 = (
    "8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241")
CHARTDATA = os.path.join(
    STUDY, "exports",
    "TV_CHARTDATA_BATS_SPY_5m_RTH_2025-08-11_2026-08-25_FastAlphaV0.csv")
CHARTDATA_SHA256 = (
    "9e0a49183edbb165a760b5bc4f56a79d9710b205e71d623c3dc2328792a14dfc")

DEV_END = dt.date(2025, 12, 31)          # charter A3 development window end
EMA_WARMUP_SKIP_SESSIONS = 5             # chart-data EMAs seed at its own
                                         # 2025-08-11 history start; skip the
                                         # first overlap sessions before
                                         # judging EMA parity
RATIO_STEP_MIN = 5e-4                    # daily close-ratio jump that opens a
                                         # new adjustment segment (~0.05%)

# R0 headline numbers as observed by the owner in TradingView (reference
# only — reproduced from the preserved export, never interpreted here).
R0_EXPECTED = {
    "n_trades": 1331,
    "net_pnl": 25.69,
    "wins": 295,
    "long_pnl": 43.68,
    "short_pnl": -17.99,
}


def sha256_file(path, expected):
    with open(path, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    print(f"input {os.path.relpath(path, STUDY)} sha256 {got}")
    if got != expected:
        sys.exit(f"INPUT IDENTITY FAILURE: {path} sha256 {got} != {expected}")


def load_tradelist():
    sha256_file(TRADELIST, TRADELIST_SHA256)
    with open(TRADELIST, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    trades = {}
    for r in rows:
        n = int(r["Trade number"])
        kind = "exit" if r["Type"].startswith("Exit") else "entry"
        trades.setdefault(n, {})[kind] = r
    return trades


def assert_r0_headline(trades):
    net = gp = gl = longs = shorts = 0.0
    wins = 0
    for t in trades.values():
        pnl = float(t["exit"]["Net PnL USD"])
        net += pnl
        if pnl > 0:
            gp += pnl
            wins += 1
        else:
            gl += -pnl
        if "long" in t["entry"]["Type"].lower():
            longs += pnl
        else:
            shorts += pnl
    checks = {
        "n_trades": len(trades),
        "net_pnl": round(net, 2),
        "wins": wins,
        "long_pnl": round(longs, 2),
        "short_pnl": round(shorts, 2),
    }
    for k, want in R0_EXPECTED.items():
        if checks[k] != want:
            sys.exit(f"R0 HEADLINE MISMATCH: {k} = {checks[k]}, expected {want}")
    pf_ratio = gp / gl
    if abs(pf_ratio - 1.04) > 0.005:
        sys.exit(f"R0 HEADLINE MISMATCH: profit factor {pf_ratio:.4f} != ~1.04")
    win_pct = 100.0 * wins / len(trades)
    if abs(win_pct - 22.16) > 0.01:
        sys.exit(f"R0 HEADLINE MISMATCH: win% {win_pct:.2f} != 22.16")
    print(f"R0 headline REPRODUCED from preserved export: "
          f"n={checks['n_trades']} net={checks['net_pnl']} "
          f"PF={pf_ratio:.4f} win%={win_pct:.2f} "
          f"long={checks['long_pnl']} short={checks['short_pnl']}")
    return {**checks, "profit_factor": round(pf_ratio, 4),
            "win_pct": round(win_pct, 2)}


def load_chartdata_dev():
    """Chart-data rows with ET session date <= DEV_END. Rows after the
    development window are dropped before any value column is read."""
    sha256_file(CHARTDATA, CHARTDATA_SHA256)
    kept, dropped = [], 0
    with open(CHARTDATA) as fh:
        for r in csv.DictReader(fh):
            ts = dt.datetime.fromtimestamp(int(r["time"]), ET)
            if ts.date() > DEV_END:
                dropped += 1
                continue
            kept.append({
                "key": ts.strftime("%Y-%m-%dT%H:%M"),
                "date": ts.date().isoformat(),
                "o": float(r["open"]), "h": float(r["high"]),
                "l": float(r["low"]), "c": float(r["close"]),
                "vwap": float(r["Session VWAP"]) if r["Session VWAP"] else None,
                "ema9": float(r["EMA 9"]) if r["EMA 9"] else None,
                "ema20": float(r["EMA 20"]) if r["EMA 20"] else None,
                "sig_long": r["Long Fast-Alpha Signal"] == "1",
                "sig_short": r["Short Fast-Alpha Signal"] == "1",
            })
    print(f"chart-data: kept {len(kept)} dev-window rows; "
          f"dropped {dropped} rows after {DEV_END} UNINSPECTED "
          f"(embargo/validation firewall)")
    return kept


def quantiles(vals):
    if not vals:
        return None
    s = sorted(vals)
    return {
        "n": len(s),
        "max": s[-1],
        "p50": s[len(s) // 2],
        "p99": s[int(len(s) * 0.99)],
        "mean": sum(s) / len(s),
    }


def main():
    print("python", platform.python_version(), "| stdlib only")

    # ---- Trade list: reproduce R0 headline (fail loudly on mismatch) ----
    trades = load_tradelist()
    headline = assert_r0_headline(trades)

    # ---- Local foundation (corpus hash-guarded inside load_corpus_rth) ----
    print(f"input data/cache/canonical corpus sha256 {pf.CANONICAL_SHA256} "
          f"(guarded by parity_foundation)")
    bars = pf.build_5m_bars(pf.load_corpus_rth())
    feats = pf.compute_features(bars)
    local = {f["et_start"][:16]: f for f in feats}
    dev_sessions = sorted({f["session_date"] for f in feats
                           if f["session_date"] <= DEV_END.isoformat()})

    tv = load_chartdata_dev()
    overlap_dates = sorted({r["date"] for r in tv})

    results = {"r0_headline_reproduced": headline}

    # ---- Gate 1a: timestamp / session alignment ----
    tv_keys = {r["key"] for r in tv}
    loc_keys = {k for k, f in local.items()
                if overlap_dates[0] <= f["session_date"] <= overlap_dates[-1]}
    only_tv = sorted(tv_keys - loc_keys)
    only_loc = sorted(loc_keys - tv_keys)
    tv_per_day = Counter(r["date"] for r in tv)
    loc_per_day = Counter(local[k]["session_date"] for k in loc_keys)
    day_count_mismatch = {d: (loc_per_day[d], tv_per_day[d])
                          for d in overlap_dates
                          if loc_per_day[d] != tv_per_day[d]}
    results["gate1_alignment"] = {
        "overlap_first": overlap_dates[0], "overlap_last": overlap_dates[-1],
        "overlap_sessions": len(overlap_dates),
        "tv_bars": len(tv_keys), "local_bars": len(loc_keys),
        "bars_only_in_tv": len(only_tv), "bars_only_in_local": len(only_loc),
        "only_tv_examples": only_tv[:10], "only_local_examples": only_loc[:10],
        "sessions_with_bar_count_mismatch": day_count_mismatch,
    }

    matched = [(r, local[r["key"]]) for r in tv if r["key"] in local]

    # ---- Adjustment-ratio diagnostic (TV close / local close) ----
    daily_ratio = {}
    for d in overlap_dates:
        rs = [t["c"] / l["c"] for t, l in matched if t["date"] == d]
        if rs:
            daily_ratio[d] = statistics.median(rs)
    segments = []
    seg_start = overlap_dates[0]
    prev = daily_ratio[overlap_dates[0]]
    for d in overlap_dates[1:]:
        if abs(daily_ratio[d] - prev) > RATIO_STEP_MIN:
            segments.append((seg_start, d))
            seg_start = d
        prev = daily_ratio[d]
    segments.append((seg_start, None))
    seg_of = {}
    for i, (s, e) in enumerate(segments):
        for d in overlap_dates:
            if d >= s and (e is None or d < e):
                seg_of[d] = i
    seg_ratio = {}
    for i in range(len(segments)):
        vals = [t["c"] / l["c"] for t, l in matched if seg_of[t["date"]] == i]
        seg_ratio[i] = statistics.median(vals)
    within = [abs(t["c"] / l["c"] - seg_ratio[seg_of[t["date"]]])
              for t, l in matched]
    results["adjustment_ratio"] = {
        "segments": [{"start": s, "end_exclusive": e,
                      "ratio_tv_over_local": round(seg_ratio[i], 8)}
                     for i, (s, e) in enumerate(segments)],
        "within_segment_abs_dev": quantiles(within),
        "interpretation": "stepwise-constant ratio = dividend-adjustment "
                          "difference (TV ADJ vs split-only local corpus); "
                          "steps expected at SPY ex-dividend dates",
    }

    # ---- Gate 1b: OHLC (raw and ratio-normalized) ----
    ohlc = {}
    for fld in ("o", "h", "l", "c"):
        raw = [abs(t[fld] - l[fld]) for t, l in matched]
        norm = [abs(t[fld] - l[fld] * seg_ratio[seg_of[t["date"]]])
                for t, l in matched]
        ohlc[fld] = {"raw_abs": quantiles(raw), "norm_abs": quantiles(norm),
                     "norm_within_1c": sum(1 for x in norm if x <= 0.01),
                     "norm_within_5c": sum(1 for x in norm if x <= 0.05)}
    results["gate1_ohlc"] = ohlc

    # ---- Gate 1c: volume ----
    results["gate1_volume"] = "UNAVAILABLE — chart-data export carries no volume column"

    # ---- Gate 2: VWAP / EMA9 / EMA20 (ratio-normalized; raw kept too) ----
    def feature_cmp(tv_field, loc_field, skip_sessions=0):
        keep_dates = set(overlap_dates[skip_sessions:])
        pairs = [(t, l) for t, l in matched
                 if t["date"] in keep_dates and t[tv_field] is not None
                 and l[loc_field] is not None]
        raw = [abs(t[tv_field] - l[loc_field]) for t, l in pairs]
        norm = [abs(t[tv_field] - l[loc_field] * seg_ratio[seg_of[t["date"]]])
                for t, l in pairs]
        return {"pairs": len(pairs), "raw_abs": quantiles(raw),
                "norm_abs": quantiles(norm),
                "norm_within_1c": sum(1 for x in norm if x <= 0.01),
                "norm_within_5c": sum(1 for x in norm if x <= 0.05),
                "norm_within_25c": sum(1 for x in norm if x <= 0.25)}
    results["gate2_vwap"] = feature_cmp("vwap", "session_vwap")
    results["gate2_ema9"] = feature_cmp("ema9", "ema9",
                                        EMA_WARMUP_SKIP_SESSIONS)
    results["gate2_ema20"] = feature_cmp("ema20", "ema20",
                                         EMA_WARMUP_SKIP_SESSIONS)

    # ---- Gate 2: semantic signal comparison (fields permitting) ----
    # TV plotted signals are FLAT-GATED (include strategy.position_size == 0
    # on the BATS chart's own run); local candidates are flat-agnostic. The
    # testable implication is TV_signal=1 => local candidate=1.
    sig = {"tv_long": 0, "tv_long_matched": 0,
           "tv_short": 0, "tv_short_matched": 0,
           "local_long_candidates": 0, "local_short_candidates": 0,
           "unmatched_examples": []}
    for t, l in matched:
        if l["long_candidate"]:
            sig["local_long_candidates"] += 1
        if l["short_candidate"]:
            sig["local_short_candidates"] += 1
        for side, cand in (("long", "long_candidate"),
                           ("short", "short_candidate")):
            if t[f"sig_{side}"]:
                sig[f"tv_{side}"] += 1
                if l[cand]:
                    sig[f"tv_{side}_matched"] += 1
                elif len(sig["unmatched_examples"]) < 12:
                    sig["unmatched_examples"].append(
                        {"key": t["key"], "side": side,
                         "tv_close_vs_vwap": round(t["c"] - t["vwap"], 4),
                         "loc_close_vs_vwap":
                             round(l["c"] - l["session_vwap"], 4),
                         "tv_ema9_minus_ema20":
                             round((t["ema9"] or 0) - (t["ema20"] or 0), 4)
                             if t["ema9"] is not None else None,
                         "loc_ema9_minus_ema20":
                             round(l["ema9"] - l["ema20"], 4),
                         "loc_bar_red": l["red_bar"],
                         "loc_bar_green": l["green_bar"]})
    results["gate2_signals"] = sig

    # ---- Gate 3 probe: TV trade-list entries vs local candidates ----
    # Entry fill timestamp = fill bar start; signal bar = fill bar - 5m.
    probe = {"entries": 0, "signal_bar_found": 0, "candidate_match": 0,
             "by_side": {"long": [0, 0], "short": [0, 0]},
             "unmatched": []}
    entry_hms = Counter()
    for n in sorted(trades):
        e = trades[n]["entry"]
        side = "long" if "long" in e["Type"].lower() else "short"
        fill = dt.datetime.strptime(e["Date and time"], "%Y-%m-%d %H:%M")
        entry_hms[fill.strftime("%H:%M")] += 0  # touch for min/max below
        entry_hms[fill.strftime("%H:%M")] += 1
        sigbar = fill - dt.timedelta(minutes=5)
        key = sigbar.strftime("%Y-%m-%dT%H:%M")
        probe["entries"] += 1
        probe["by_side"][side][0] += 1
        l = local.get(key)
        if l is None:
            if len(probe["unmatched"]) < 12:
                probe["unmatched"].append({"trade": n, "side": side,
                                           "signal_bar": key,
                                           "reason": "no local bar"})
            continue
        probe["signal_bar_found"] += 1
        if l["long_candidate" if side == "long" else "short_candidate"]:
            probe["candidate_match"] += 1
            probe["by_side"][side][1] += 1
        elif len(probe["unmatched"]) < 12:
            probe["unmatched"].append({
                "trade": n, "side": side, "signal_bar": key,
                "reason": "local candidate flag false",
                "loc_close_vs_vwap": round(l["c"] - l["session_vwap"], 4),
                "loc_ema9_minus_ema20": round(l["ema9"] - l["ema20"], 4),
                "loc_red": l["red_bar"], "loc_green": l["green_bar"],
                "loc_in_window": l["in_entry_window"]})
    probe["earliest_entry_hm"] = min(entry_hms)
    probe["latest_entry_hm"] = max(entry_hms)
    results["gate3_probe_tradelist_vs_local_candidates"] = probe

    # Cross-feed check: overlap-window trade entries vs the BATS chart's own
    # flat-gated signal flags (different chart run; descriptive only).
    tv_by_key = {r["key"]: r for r in tv}
    xfeed = {"entries_in_overlap": 0, "bats_signal_present": 0}
    for n in sorted(trades):
        e = trades[n]["entry"]
        fill = dt.datetime.strptime(e["Date and time"], "%Y-%m-%d %H:%M")
        if fill.date() < dt.date.fromisoformat(overlap_dates[0]):
            continue
        side = "long" if "long" in e["Type"].lower() else "short"
        key = (fill - dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M")
        r = tv_by_key.get(key)
        if r is None:
            continue
        xfeed["entries_in_overlap"] += 1
        if r[f"sig_{side}"]:
            xfeed["bats_signal_present"] += 1
    results["crossfeed_amex_trades_vs_bats_signals"] = xfeed

    results["dev_window_sessions_local"] = len(dev_sessions)

    out = os.path.join(HERE, "R0_PARITY_RESULTS_2026-08-25.json")
    with open(out, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"\nresults written: {os.path.relpath(out, STUDY)}")
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
