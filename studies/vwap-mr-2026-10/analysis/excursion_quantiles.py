#!/usr/bin/env python3
"""TRADE-BLIND: distribution of |E| = |close - VWAP| / ATR14 on completed 5m RTH bars.

No strategy is simulated and no P&L is computed. Used only to pre-declare K for VMR-L.
Bars are those whose END falls inside the VMR-L entry window (10:00-15:00 ET), on scored
sessions (after the first `warmup` sessions).

usage: excursion_quantiles.py <dataset_id> [--mask MASK_ID] [--warmup 5]
"""
import argparse, json
import numpy as np, pandas as pd
from stratlab.data.store import load_dataset
from stratlab.data.sessions import ET, assign_regular_sessions, resample_session_bars, session_table
from stratlab.strategies.vwap_mean_reversion import mr_features

ap = argparse.ArgumentParser(); ap.add_argument("dataset"); ap.add_argument("--mask"); ap.add_argument("--warmup", type=int, default=5)
a = ap.parse_args()
df, ident = load_dataset(a.dataset, a.mask)
s = session_table(df.index[0], df.index[-1])
rth = assign_regular_sessions(df, s)
sig = resample_session_bars(rth, 5, s)
f = mr_features(sig)
sessions = pd.DatetimeIndex(sorted(sig["session"].unique()))
scored = sig["session"].isin(sessions[a.warmup:])
end = (sig.index + pd.Timedelta(minutes=5)).tz_convert(ET)
m = end.hour * 60 + end.minute
inwin = (m >= 600) & (m <= 900)
e = f["E"][scored & inwin & sig["complete"]].abs().dropna()
q = {str(p): round(float(e.quantile(p)), 4) for p in (0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99)}
out = {"dataset": ident["dataset_id"], "sha256": ident["sha256"], "mask": (ident.get("mask") or {}).get("id"),
       "scored_sessions": [str(sessions[a.warmup].date()), str(sessions[-1].date())], "bars": int(len(e)),
       "abs_E_quantiles": q, "share_bars_absE_ge": {str(k): round(float((e >= k).mean()), 4) for k in (2, 3, 4, 5)}}
print(json.dumps(out, indent=2))
