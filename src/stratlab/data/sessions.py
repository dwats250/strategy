"""Exchange sessions and session-anchored bars.

Session boundaries come from `exchange_calendars` (XNYS by default), so early closes
(13:00 ET), holidays and DST are calendar facts rather than fixed clock rules. A bar
belongs to a session iff  session_open <= bar_start < session_close. On early-close
days that excludes the 13:00 closing-auction print, matching TradingView's RTH
chart (which ends at 12:55 on 5m half-days).

Timestamps are bar STARTS, stored in UTC. Eastern time is derived for display and
for clock-based rules only.
"""

from __future__ import annotations

from functools import lru_cache

import exchange_calendars as xcals
import numpy as np
import pandas as pd

ET = "America/New_York"


@lru_cache(maxsize=4)
def _calendar(name: str):
    return xcals.get_calendar(name, start="2000-01-03")


def session_table(start, end, calendar: str = "XNYS") -> pd.DataFrame:
    """One row per trading session in [start, end]: open/close (UTC), length, early-close flag."""
    cal = _calendar(calendar)
    sched = cal.schedule.loc[pd.Timestamp(start).strftime("%Y-%m-%d"):pd.Timestamp(end).strftime("%Y-%m-%d")]
    out = pd.DataFrame({
        "open": sched["open"].dt.tz_convert("UTC"),
        "close": sched["close"].dt.tz_convert("UTC"),
    })
    out.index = pd.DatetimeIndex(out.index.date, name="session")
    out["minutes"] = ((out["close"] - out["open"]).dt.total_seconds() // 60).astype(int)
    out["early_close"] = out["minutes"] < 390
    return out


def assign_regular_sessions(bars: pd.DataFrame, sessions: pd.DataFrame) -> pd.DataFrame:
    """Keep bars inside a regular session; add `session` (date) and `minute` (minutes since open)."""
    ts = bars.index
    opens = pd.DatetimeIndex(sessions["open"]).as_unit("ns").asi8
    closes = pd.DatetimeIndex(sessions["close"]).as_unit("ns").asi8
    t = ts.as_unit("ns").asi8
    pos = np.searchsorted(opens, t, side="right") - 1
    valid = pos >= 0
    pos_c = np.clip(pos, 0, len(opens) - 1)
    inside = valid & (t >= opens[pos_c]) & (t < closes[pos_c])
    out = bars[inside].copy()
    p = pos_c[inside]
    out["session"] = sessions.index.to_numpy()[p]
    out["minute"] = ((t[inside] - opens[p]) // 60_000_000_000).astype(int)
    return out


def resample_session_bars(rth_1m: pd.DataFrame, minutes: int, sessions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate 1-minute RTH bars into `minutes`-bars anchored at each session open.

    Index = bucket start (UTC). Never fills missing minutes. `n_1m` counts constituent
    minutes; `complete` is True when every expected minute is present. `last_1m`
    holds the start time of the bucket's last existing 1-minute bar, which is when
    the completed bar becomes knowable on the execution timeline.
    """
    df = rth_1m
    bucket = df["minute"] // minutes
    key = [df["session"], bucket]
    g = df.groupby(key, sort=True)
    agg = pd.DataFrame({
        "Open": g["Open"].first(), "High": g["High"].max(), "Low": g["Low"].min(),
        "Close": g["Close"].last(), "Volume": g["Volume"].sum(),
        "n_1m": g["Open"].size(),
    })
    last_ts = pd.Series(df.index, index=df.index).groupby(key, sort=True).last()
    agg["last_1m"] = last_ts.to_numpy()
    sess = agg.index.get_level_values(0)
    b = agg.index.get_level_values(1).to_numpy()
    opens = pd.DatetimeIndex(sessions.loc[sess, "open"])
    sess_len = sessions.loc[sess, "minutes"].to_numpy()
    start = opens + pd.to_timedelta(b * minutes, unit="min")
    expected = np.minimum(minutes, sess_len - b * minutes)
    agg["expected_1m"] = expected
    agg["complete"] = agg["n_1m"].to_numpy() == expected
    agg["session"] = sess
    agg.index = pd.DatetimeIndex(start, name="ts_utc")
    return agg


def coverage(rth_1m: pd.DataFrame, sessions: pd.DataFrame) -> pd.DataFrame:
    """Per-session expected vs present 1-minute bar counts."""
    present = rth_1m.groupby("session").size()
    cov = sessions[["minutes", "early_close"]].copy()
    cov["present"] = present.reindex(cov.index).fillna(0).astype(int)
    cov["missing"] = cov["minutes"] - cov["present"]
    return cov
