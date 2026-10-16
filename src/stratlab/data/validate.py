"""Trade-blind dataset validation: coverage, duplicates, gaps, OHLC sanity, DST, freshness.

Reads only bars; computes no strategy quantity.
"""

from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

from .sessions import ET, assign_regular_sessions, coverage, session_table
from .store import load_dataset, load_registry, resolve


def validate_frame(bars: pd.DataFrame, today: dt.date | None = None) -> dict:
    idx = bars.index
    out: dict = {"rows": int(len(bars)), "first_bar_utc": idx.min().isoformat(), "last_bar_utc": idx.max().isoformat()}
    out["duplicate_timestamps"] = int(idx.duplicated().sum())
    out["monotonic_increasing"] = bool(idx.is_monotonic_increasing)
    o, h, l, c, v = (bars[k] for k in ("Open", "High", "Low", "Close", "Volume"))
    out["ohlc_violations"] = int(((h < np.maximum(o, c)) | (l > np.minimum(o, c)) | (l <= 0)).sum())
    out["negative_volume"] = int((v < 0).sum())

    sessions = session_table(idx.min(), idx.max())
    rth = assign_regular_sessions(bars, sessions)
    cov = coverage(rth, sessions)
    present = cov[cov.present > 0]
    out["calendar_sessions_in_span"] = int(len(cov))
    out["sessions_with_data"] = int(len(present))
    out["calendar_sessions_without_data"] = [str(d.date()) for d in pd.DatetimeIndex(cov.index[cov.present == 0])]
    out["first_session"] = str(pd.Timestamp(present.index.min()).date())
    out["last_session"] = str(pd.Timestamp(present.index.max()).date())
    full = present[present.present == present.minutes]
    out["last_complete_session"] = str(pd.Timestamp(full.index.max()).date()) if len(full) else None
    out["early_close_sessions"] = [str(pd.Timestamp(d).date()) for d in present.index[present.early_close]]
    inc = present[present.missing > 0]
    out["sessions_with_missing_minutes"] = {str(pd.Timestamp(d).date()): int(m) for d, m in inc["missing"].items()}
    out["rth_bars"] = int(len(rth))
    out["extended_hours_bars"] = int(len(bars) - len(rth))
    out["rth_zero_volume_bars"] = int((rth["Volume"] == 0).sum())
    first_et = rth.groupby("session").apply(lambda x: x.index[0].tz_convert(ET).strftime("%H:%M"))
    out["sessions_not_starting_0930_et"] = [str(pd.Timestamp(d).date()) for d, t in first_et.items() if t != "09:30"]
    utc_open = rth.groupby("session").apply(lambda x: x.index[0].strftime("%H:%M")).value_counts().to_dict()
    out["session_open_utc_clock_counts"] = utc_open  # 13:30 (EDT) and 14:30 (EST) expected
    r = rth["Close"].groupby(rth["session"]).pct_change().abs()
    out["rth_1m_abs_return_gt_1pct"] = int((r > 0.01).sum())
    if today:
        out["freshness_days_since_last_session"] = (today - pd.Timestamp(present.index.max()).date()).days
    return out


def validate_dataset(ds_id: str, mask: str | None = None, today: dt.date | None = None) -> dict:
    rec, path = resolve(ds_id)
    bars, ident = load_dataset(ds_id, mask)
    rep = validate_frame(bars, today or dt.date.today())
    rep["identity"] = ident
    rep["registered_rows"] = rec.rows
    rep["adjustment_semantics"] = rec.meta.get("adjustment_semantics")
    rep["timestamp_semantics"] = rec.meta.get("timestamp_semantics")
    return rep
