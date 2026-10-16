#!/usr/bin/env python3
"""Post-run DIAGNOSTIC: Massive 1-minute bars vs an independent hourly source (Yahoo Finance).

Nothing is re-run and no result is replaced. The script:
  1. aggregates the run's dataset (RTH) into Yahoo's hourly buckets (09:30, 10:30, ... ET);
  2. lists every hour where Massive's high or low lies more than $0.50 beyond Yahoo's;
  3. counts the run's STOP exits whose fill price lies outside Yahoo's range for that hour.
     Those fills are not supported by the independent source. That is not proof they were
     unexecutable: without tick condition codes the reason for the difference is unknown.

Independent data is not committed (third-party terms). To reproduce, fetch it with the free
`yfinance` package (no account) into a CSV:
  yf.download("SPY", start="2024-12-18", end="2026-08-22", interval="1h", auto_adjust=False,
              prepost=False).to_csv(PATH)
Yahoo serves hourly history for about two years, so hours before 2024-12-18 cannot be checked.

usage: compare_independent_hourly.py <run_dir> <yahoo_1h_csv>
"""

import json
import sys
from pathlib import Path

import pandas as pd

from stratlab.data.sessions import ET, assign_regular_sessions, session_table
from stratlab.data.store import load_dataset

TOL = 0.50


def hourly(dataset: str, mask: str | None) -> pd.DataFrame:
    df, _ = load_dataset(dataset, mask=mask)
    r = assign_regular_sessions(df, session_table(df.index[0], df.index[-1]))
    r.index = r.index.tz_convert(ET)
    start = r.index.floor("h") + pd.Timedelta(minutes=30)
    start = start.where(r.index.minute >= 30, start - pd.Timedelta(hours=1))
    return r.groupby(start).agg(High=("High", "max"), Low=("Low", "min"), Close=("Close", "last"))


def main(run_dir: str, yahoo_csv: str) -> int:
    run = Path(run_dir)
    rec = json.loads((run / "run_record.json").read_text())
    data = rec["config"]["data"]
    m = hourly(data["dataset"], data.get("mask"))
    y = pd.read_csv(yahoo_csv, header=[0, 1], index_col=0)
    y.columns = [c[0] for c in y.columns]
    y.index = pd.to_datetime(y.index, utc=True).tz_convert(ET)
    j = m.join(y[["High", "Low", "Close"]], rsuffix="_y", how="inner")
    print(f"dataset {data['dataset']} mask {data.get('mask')} | hours compared {len(j)} "
          f"({j.index.min().date()} -> {j.index.max().date()})")
    print(f"hourly closes identical to the cent: {(j.Close.round(2) == j.Close_y.round(2)).mean():.1%}")
    up = j[(j.High - j.High_y) > TOL]
    dn = j[(j.Low_y - j.Low) > TOL]
    print(f"hours where Massive's HIGH exceeds Yahoo's by > ${TOL}: {len(up)}; LOW below Yahoo's by > ${TOL}: {len(dn)}")
    for name, d in (("high", up), ("low", dn)):
        for t, r in d.iterrows():
            print(f"  {name:4s} {t:%Y-%m-%d %H:%M}  Massive {r.High if name == 'high' else r.Low:8.2f}  Yahoo {r.High_y if name == 'high' else r.Low_y:8.2f}")
    print("\nstop exits whose fill lies outside Yahoo's range for that hour (full-window trades):")
    yr = j[["High_y", "Low_y"]]
    for v in rec["config"]["variants"]:
        t = pd.read_csv(run / "trades" / f"{v['id']}__full.csv", parse_dates=["exit_time"])
        st = t[t.exit_reason == "stop"].copy()
        if st.empty:
            print(f"  {v['id']:6s} no stop exits"); continue
        x = st.exit_time.dt.tz_convert(ET)
        hk = x.dt.floor("h") + pd.Timedelta(minutes=30)
        hk = hk.where(x.dt.minute >= 30, hk - pd.Timedelta(hours=1))
        st["yh"] = hk.map(yr.High_y)
        st["yl"] = hk.map(yr.Low_y)
        chk = st[st.yh.notna()]
        out = chk[(chk.exit_price > chk.yh + 0.01) | (chk.exit_price < chk.yl - 0.01)]
        days = sorted(out.exit_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d").unique())
        print(f"  {v['id']:6s} stop exits checkable {len(chk):5d} | outside Yahoo range {len(out):3d} "
              f"| their net P&L ${out.pnl.sum():10,.0f} | sessions {days}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
