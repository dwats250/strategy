#!/usr/bin/env python3
"""Reconcile one stratlab run directory (conventions §d). Exit nonzero on any mismatch.

Checks, for every configuration x window:
  1. equity: net P&L from session-close equity == sum of trade P&L (to the cent), and the
     equity file's last value == cash + sum of trade P&L
  2. costs: each closed trade paid exactly 2 x shares x cost/share; gross - costs == net
  3. sizing: shares == floor(0.999 x equity before entry / (fill + cost/share)); never above 1x
  4. sessions: every trade enters and exits on the same ET date (nothing overnight) and
     exits no later than the calendar flatten minute
  5. windows: the calendar halves partition the full-window trades exactly, and the recent
     window's trades are a subset of the full window's (same signal bar and side)
  6. diffs: same + altered + removed == baseline trades; same + altered + added == variant trades
  7. ledger: one row per configuration for this run, matching metrics.json
Prints package versions and the SHA-256 of every input file read.

usage: reconcile_run.py <run_dir> [<run_dir> ...]
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

from stratlab.data.sessions import ET, session_table
from stratlab.experiment import package_versions

FAILS: list[str] = []
READ: dict[str, str] = {}


def sha(p: Path) -> str:
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    READ[str(p)] = h
    return h


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAILS.append(msg)


def reconcile(run_dir: Path) -> dict:
    rec_p, met_p = run_dir / "run_record.json", run_dir / "metrics.json"
    sha(rec_p); sha(met_p)
    rec = json.loads(rec_p.read_text())
    met = json.loads(met_p.read_text())
    cash = rec["execution"]["cash"]
    cps = rec["execution"]["cost_per_share_per_side"]
    variants = rec["config"]["variants"]
    windows = rec["windows"]
    full = windows[0]["id"]
    sess = session_table(windows[0]["start"], windows[0]["end"])
    flat_min = {str(d.date()): (c.tz_convert(ET) - pd.Timedelta(minutes=rec["execution"]["flatten_minutes"]))
                for d, c in zip(pd.DatetimeIndex(sess.index), sess["close"])}
    summary = {"run_id": rec["run_id"], "checks": 0}
    trades_by = {}
    for v in variants:
        for w in windows:
            vid, wid = v["id"], w["id"]
            r = met[vid][wid]
            check(r["status"] == "ok", f"{vid}/{wid}: status {r['status']}")
            tp = run_dir / "trades" / f"{vid}__{wid}.csv"
            ep = run_dir / "equity" / f"{vid}__{wid}.csv"
            sha(tp); sha(ep)
            t = pd.read_csv(tp, parse_dates=["entry_time", "exit_time"])
            e = pd.read_csv(ep)
            trades_by[(vid, wid)] = t
            net = r["equity"]["net_pnl"]
            check(abs(net - t.pnl.sum()) < 0.01, f"{vid}/{wid}: equity net {net:.2f} != trades {t.pnl.sum():.2f}")
            check(abs(e.equity.iloc[-1] - (cash + t.pnl.sum())) < 0.01, f"{vid}/{wid}: final equity mismatch")
            closed = t[t.exit_reason != "open_at_end"]
            check((t.exit_reason == "open_at_end").sum() == 0, f"{vid}/{wid}: open position at end")
            dev = (closed.costs - 2 * closed["size"] * cps).abs().max() if len(closed) else 0
            check(dev < 1e-6, f"{vid}/{wid}: cost per trade off by {dev}")
            check(((closed.gross_pnl - closed.costs - closed.pnl).abs() < 1e-6).all(), f"{vid}/{wid}: gross-costs != net")
            if len(t):
                # 1x sizing identity: shares == floor(0.999 x equity_before / (fill + cost/share)).
                # (Integer shares: at ~$76k equity and SPY ~$740 one share is ~1% of equity.)
                expect = (0.999 * t.equity_before / (t.entry_price + cps)).apply(lambda x: int(x // 1))
                bad = (t["size"] != expect).sum()
                check(bad == 0, f"{vid}/{wid}: {bad} trades violate the 1x sizing identity")
                check((t.notional_pct_equity <= 0.999 + 1e-9).all(), f"{vid}/{wid}: notional above 99.9% (leverage)")
                ed = t.entry_time.dt.tz_convert(ET).dt.date.astype(str)
                xd = t.exit_time.dt.tz_convert(ET).dt.date.astype(str)
                check((ed == xd).all(), f"{vid}/{wid}: {(ed != xd).sum()} trades held overnight")
                late = [i for i, (x, d) in enumerate(zip(t.exit_time.dt.tz_convert(ET), xd)) if x > flat_min[d]]
                check(not late, f"{vid}/{wid}: {len(late)} exits after the flatten minute")
            summary["checks"] += 1
    # windows partition
    for v in variants:
        if v.get("role") == "benchmark":
            # Backtesting.py never decides on a run's first bar, so each window run's first
            # session fills one minute later than in the full run; match on session date.
            key = lambda d: set(d.entry_time.dt.tz_convert(ET).dt.date.astype(str) + "|" + d.side)
        else:
            key = lambda d: set(d.signal_start.astype(str) + "|" + d.side)
        f = key(trades_by[(v["id"], full)])
        halves = [w["id"] for w in windows if w["kind"] == "calendar_half"]
        parts = [key(trades_by[(v["id"], h)]) for h in halves]
        union = set().union(*parts)
        check(union == f and sum(map(len, parts)) == len(f), f"{v['id']}: halves do not partition full ({len(union)} vs {len(f)})")
        rec_w = [w["id"] for w in windows if w["kind"] == "recent"]
        for rw in rec_w:
            check(key(trades_by[(v["id"], rw)]) <= f, f"{v['id']}: recent window trades not a subset of full")
    # diffs
    base = rec["baseline"]
    for v in variants:
        d = met[v["id"]][full].get("diff_vs_baseline")
        if not d:
            continue
        nb = len(trades_by[(base, full)]); nv = len(trades_by[(v["id"], full)])
        check(d["same"] + d["altered"] + d["removed"] == nb, f"{v['id']}: diff does not reconcile with baseline count {nb}")
        check(d["same"] + d["altered"] + d["added"] == nv, f"{v['id']}: diff does not reconcile with variant count {nv}")
    # ledger (real-data runs only; synthetic runs never write ledger rows)
    if rec.get("synthetic"):
        return summary
    lp = Path(__file__).resolve().parents[1] / "LEDGER.csv"
    rows = [r for r in csv.DictReader(open(lp)) if r["run_id"] == rec["run_id"]]
    sha(lp)
    check(len(rows) == len(variants), f"ledger has {len(rows)} rows for {rec['run_id']}, expected {len(variants)}")
    for row in rows:
        m = met[row["variant_id"]][full]
        check(abs(float(row["net_pnl"]) - m["equity"]["net_pnl"]) < 0.01, f"ledger net_pnl mismatch for {row['variant_id']}")
        check(int(row["trades"]) == m["trade"]["trades"], f"ledger trades mismatch for {row['variant_id']}")
    return summary


def main(argv):
    print("packages:", json.dumps(package_versions()))
    out = [reconcile(Path(p)) for p in argv[1:]]
    print("inputs read (sha256):")
    for p, h in sorted(READ.items()):
        print(f"  {h}  {p}")
    for s in out:
        print(f"{s['run_id']}: {s['checks']} configuration-window checks")
    if FAILS:
        print(f"RECONCILIATION FAILED ({len(FAILS)}):")
        for f in FAILS:
            print("  -", f)
        return 1
    print("RECONCILIATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
