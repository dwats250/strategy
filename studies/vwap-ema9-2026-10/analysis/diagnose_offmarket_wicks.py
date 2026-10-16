#!/usr/bin/env python3
"""Post-run DIAGNOSTIC (not a frozen check, not a rerun): suspicious wick clusters (unresolved).

Found while reviewing VWR0-EXP__20261016T211249Z: on 2025-04-23, after ~11:28 ET, over a
hundred RTH minutes print highs at $544-545 while their bodies trade at $534-539 and the
vendor per-minute VWAP stays at the body. That pattern is consistent with late-reported prints at
the morning's price level, but it is UNRESOLVED: no tick condition codes are available, and an
independent hourly source (Yahoo) lacks these prints without proving they were unexecutable.
See docs/lab/DATA_QUALITY_2026-10-16.md. (Docstring wording corrected 2026-10-16; logic unchanged.)
The frozen integrity mask v1.0 (isolated-spike rule) does not catch clusters.

Part 1 is trade-blind: it flags minutes with a wick more than 0.5% beyond the body while the
vendor VWAP stays within 0.15% of the body, and counts them per session.
Part 2 measures each configuration's exposure, using the run's own trade files: P&L on the
affected session, and stop exits that occurred on flagged minutes.
No strategy is re-run and no result is replaced.

usage: diagnose_offmarket_wicks.py <run_dir>
"""

import json
import sys
from pathlib import Path

import pandas as pd

from stratlab.data.sessions import ET, assign_regular_sessions, session_table
from stratlab.data.store import load_dataset

WICK = 0.005      # wick beyond the body, as a fraction of price
VW_BAND = 0.0015  # vendor VWAP within this band of the body


def flags(dataset: str, mask: str | None) -> pd.Series:
    df, _ = load_dataset(dataset, mask=mask)
    r = assign_regular_sessions(df, session_table(df.index[0], df.index[-1]))
    bh = r[["Open", "Close"]].max(axis=1)
    bl = r[["Open", "Close"]].min(axis=1)
    inside = (r.VendorVWAP <= bh * (1 + VW_BAND)) & (r.VendorVWAP >= bl * (1 - VW_BAND))
    f = ((r.High / bh - 1 > WICK) | (1 - r.Low / bl > WICK)) & inside
    return pd.Series(f.to_numpy(), index=r.index), r["session"]


def main(run_dir: str) -> int:
    run = Path(run_dir)
    rec = json.loads((run / "run_record.json").read_text())
    data = rec["config"]["data"]
    f, sess = flags(data["dataset"], data.get("mask"))
    per = f.groupby(sess.to_numpy()).sum()
    print(f"flagged minutes: {int(f.sum())}; sessions with any: {int((per > 0).sum())}; "
          f"sessions with >=10: {int((per >= 10).sum())} -> {[str(d.date()) for d in per[per >= 10].index]}")
    flagged = set(f[f].index)
    worst = str(per.idxmax().date())
    print(f"\nexposure by configuration (full window), affected session {worst}:")
    for v in rec["config"]["variants"]:
        t = pd.read_csv(run / "trades" / f"{v['id']}__full.csv", parse_dates=["entry_time", "exit_time"])
        day = t.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == worst
        st = t[(t.exit_reason == "stop") & t.exit_time.isin(flagged)]
        ex = t[~day]
        mean_r = ex.r_multiple.mean()
        t_r = mean_r / ex.r_multiple.std() * len(ex) ** 0.5 if ex.r_multiple.notna().any() else float("nan")
        print(f"  {v['id']:6s} total ${t.pnl.sum():9,.0f} | {worst}: {int(day.sum()):3d} trades ${t[day].pnl.sum():9,.0f}"
              f" | stops on flagged minutes: {len(st):3d} ${st.pnl.sum():8,.0f}"
              f" | excl. {worst}: ${ex.pnl.sum():9,.0f}, mean R {mean_r:+.4f} (t {t_r:+.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
