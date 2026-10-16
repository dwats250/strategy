#!/usr/bin/env python3
"""Post-run DIAGNOSTIC: Massive 1-minute bars vs an independent hourly source (Yahoo Finance).

Nothing is re-run and no result is replaced. The script:
  1. aggregates the run's dataset (RTH) into Yahoo's hourly buckets (09:30, 10:30, ... ET);
  2. lists every hour where Massive's high or low lies more than $0.50 beyond Yahoo's;
  3. counts the run's STOP exits whose fill price lies outside Yahoo's range for that hour, at
     $0.01 and $0.50 tolerances, with the exceedance of each fill. Those fills are not supported
     by the independent source. That is not proof they were unexecutable: without tick condition
     codes the reason for the difference is unknown;
  4. treats hours where Yahoo has no bar, or < 50% of Massive's volume, as uncheckable (Yahoo
     itself has gaps), and reports body-level discrepancies separately (those indicate missing
     Yahoo data, not a suspicious wick);
  5. calibrates against mask v1.0: does Yahoo show each masked minute's extreme?

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
from stratlab.data.store import REPO_ROOT, load_dataset

TOLS = (0.01, 0.50)      # stop-fill tolerances reported side by side
WICK_TOL = 0.50          # hour-level extreme discrepancy
MIN_VOL_RATIO = 0.5      # Yahoo hours with < 50% of Massive's volume are treated as incomplete


def hourly(df: pd.DataFrame) -> pd.DataFrame:
    r = assign_regular_sessions(df, session_table(df.index[0], df.index[-1]))
    r.index = r.index.tz_convert(ET)
    start = r.index.floor("h") + pd.Timedelta(minutes=30)
    start = start.where(r.index.minute >= 30, start - pd.Timedelta(hours=1))
    r["BodyHi"] = r[["Open", "Close"]].max(axis=1)
    r["BodyLo"] = r[["Open", "Close"]].min(axis=1)
    return r.groupby(start).agg(High=("High", "max"), Low=("Low", "min"), Close=("Close", "last"),
                                Volume=("Volume", "sum"), BodyHi=("BodyHi", "max"), BodyLo=("BodyLo", "min"))


def hour_key(ts: pd.Series) -> pd.Series:
    x = ts.dt.tz_convert(ET)
    k = x.dt.floor("h") + pd.Timedelta(minutes=30)
    return k.where(x.dt.minute >= 30, k - pd.Timedelta(hours=1))


def main(run_dir: str, yahoo_csv: str) -> int:
    run = Path(run_dir)
    rec = json.loads((run / "run_record.json").read_text())
    data = rec["config"]["data"]
    df, _ = load_dataset(data["dataset"], mask=data.get("mask"))
    m = hourly(df)
    y = pd.read_csv(yahoo_csv, header=[0, 1], index_col=0)
    y.columns = [c[0] for c in y.columns]
    y.index = pd.to_datetime(y.index, utc=True).tz_convert(ET)
    lo, hi = y.index.min(), y.index.max()
    mw = m[(m.index >= lo) & (m.index <= hi)]
    j = mw.join(y[["High", "Low", "Close", "Volume"]], rsuffix="_y", how="left")
    missing = j[j.High_y.isna()]
    thin = j[j.High_y.notna() & (j.Volume_y < MIN_VOL_RATIO * j.Volume)]
    ok = j[j.High_y.notna() & (j.Volume_y >= MIN_VOL_RATIO * j.Volume)]
    print(f"dataset {data['dataset']} mask {data.get('mask')} | Massive hours in Yahoo span: {len(j)} "
          f"({j.index.min().date()} -> {j.index.max().date()})")
    print(f"uncheckable: {len(missing)} hours with no Yahoo bar; {len(thin)} Yahoo bars with < {MIN_VOL_RATIO:.0%} of Massive volume")
    print("  sessions:", sorted({t.strftime('%Y-%m-%d') for t in list(missing.index) + list(thin.index)}))
    dc = (ok.Close - ok.Close_y).abs()
    print(f"checkable hours: {len(ok)} | hourly closes identical to the cent: {(dc < 0.005).mean():.1%} | median |close diff| ${dc.median():.2f}")
    body = ok[(ok.BodyHi > ok.High_y + WICK_TOL) | (ok.BodyLo < ok.Low_y - WICK_TOL)]
    up = ok[(ok.High - ok.High_y) > WICK_TOL]
    dn = ok[(ok.Low_y - ok.Low) > WICK_TOL]
    print(f"hours where Massive's BODY lies > ${WICK_TOL} beyond Yahoo's range (likely missing Yahoo data): {len(body)}")
    print(f"hours where Massive's HIGH exceeds Yahoo's by > ${WICK_TOL}: {len(up)}; LOW below Yahoo's by > ${WICK_TOL}: {len(dn)}")
    for name, d in (("high", up), ("low", dn)):
        for t, r in d.iterrows():
            print(f"  {name:4s} {t:%Y-%m-%d %H:%M}  Massive {r.High if name == 'high' else r.Low:8.2f}  Yahoo {r.High_y if name == 'high' else r.Low_y:8.2f}")
    print("\nstop exits whose fill lies outside Yahoo's range for that hour (checkable hours, full-window trades):")
    yr = ok[["High_y", "Low_y"]]
    for v in rec["config"]["variants"]:
        t = pd.read_csv(run / "trades" / f"{v['id']}__full.csv", parse_dates=["exit_time"])
        st = t[t.exit_reason == "stop"].copy()
        if st.empty:
            print(f"  {v['id']:6s} no stop exits"); continue
        k = hour_key(st.exit_time)
        st["yh"], st["yl"] = k.map(yr.High_y), k.map(yr.Low_y)
        chk = st[st.yh.notna()].copy()
        chk["exceed"] = (chk.exit_price - chk.yh).clip(lower=0) + (chk.yl - chk.exit_price).clip(lower=0)
        parts = []
        for tol in TOLS:
            out = chk[chk.exceed > tol]
            parts.append(f"> ${tol:.2f}: {len(out):3d} fills, net P&L ${out.pnl.sum():10,.0f}")
        big = chk[chk.exceed > TOLS[-1]]
        days = sorted(big.exit_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d").unique())
        print(f"  {v['id']:6s} checkable {len(chk):5d} | " + " | ".join(parts) + f" | sessions (> ${TOLS[-1]:.2f}) {days}")
        for _, r in chk[chk.exceed > TOLS[0]].iterrows():
            print(f"         {r.exit_time.tz_convert(ET):%Y-%m-%d %H:%M} fill {r.exit_price:.2f} exceeds Yahoo range by ${r.exceed:.2f}")
    if data.get("mask"):
        print("\nmask calibration (raw minutes dropped by the mask vs Yahoo's hourly range):")
        raw, _ = load_dataset(data["dataset"])
        maskfile = json.loads((REPO_ROOT / "studies/vwap-lab-2026-08/analysis/CORPUS_MASK_v1.0.json").read_text())
        for tms in maskfile["mask_t_ms"]:
            ts = pd.Timestamp(tms, unit="ms", tz="UTC")
            b = raw.loc[ts]
            hk = hour_key(pd.Series([ts])).iloc[0]
            if hk not in yr.index:
                print(f"  {ts.tz_convert(ET):%Y-%m-%d %H:%M}: hour not checkable (outside Yahoo span or incomplete)"); continue
            yh, yl = yr.loc[hk]
            seen = (b.High <= yh + 0.01) and (b.Low >= yl - 0.01)
            print(f"  {ts.tz_convert(ET):%Y-%m-%d %H:%M}: minute H/L {b.High:.2f}/{b.Low:.2f} | Yahoo hour {yh:.2f}/{yl:.2f} | "
                  + ("Yahoo SHOWS this extreme" if seen else "Yahoo does NOT show it"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
