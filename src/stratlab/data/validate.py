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


def compare_datasets(a_id: str, b_id: str, tol: float = 1e-9) -> dict:
    """Bar-by-bar comparison of two captures over their overlapping RTH sessions.

    Reports matching and differing minutes, minutes present in only one capture, and
    the sessions with the most price differences, so vendor revisions are visible
    before a new capture is used in place of an older one."""
    a, _ = load_dataset(a_id)
    b, _ = load_dataset(b_id)
    lo, hi = max(a.index.min(), b.index.min()), min(a.index.max(), b.index.max())
    sess = session_table(lo, hi)
    ra = assign_regular_sessions(a[(a.index >= lo) & (a.index <= hi)], sess)
    rb = assign_regular_sessions(b[(b.index >= lo) & (b.index <= hi)], sess)
    common = ra.index.intersection(rb.index)
    cols = ["Open", "High", "Low", "Close", "Volume"]
    d = (ra.loc[common, cols] - rb.loc[common, cols]).abs()
    price_diff = (d[["Open", "High", "Low", "Close"]] > tol).any(axis=1)
    vol_diff = d["Volume"] > tol
    by_sess = price_diff.groupby(ra.loc[common, "session"]).sum()
    big = (d[["High", "Low"]].max(axis=1) / ra.loc[common, "Close"])
    return {
        "a": a_id, "b": b_id,
        "overlap_sessions": [str(pd.Timestamp(sess.index.min()).date()), str(pd.Timestamp(sess.index.max()).date())],
        "rth_minutes_a": int(len(ra)), "rth_minutes_b": int(len(rb)), "common_minutes": int(len(common)),
        "only_in_a": int(len(ra.index.difference(rb.index))), "only_in_b": int(len(rb.index.difference(ra.index))),
        "minutes_identical_ohlcv": int((~price_diff & ~vol_diff).sum()),
        "minutes_price_differs": int(price_diff.sum()), "minutes_volume_only_differs": int((vol_diff & ~price_diff).sum()),
        "minutes_high_or_low_differs_over_0.5pct": int((big > 0.005).sum()),
        "sessions_with_price_differences": int((by_sess > 0).sum()),
        "top_sessions_by_price_differences": {str(pd.Timestamp(k).date()): int(v) for k, v in by_sess.sort_values(ascending=False).head(10).items() if v > 0},
    }
