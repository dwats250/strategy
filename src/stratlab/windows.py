"""Evaluation windows with exact session dates.

* `full`         every scored session (after the warm-up sessions).
* calendar halves  fixed Jan-Jun / Jul-Dec partitions, clipped to the scored range and
                 flagged `partial` when clipped.
* `recent_Nm`    the latest N calendar months ending on the last COMPLETE session in
                 the data. Exploratory: it overlaps the full sample and the halves, it
                 is not a holdout (docs/conventions.md §g).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class Window:
    id: str
    label: str
    start: str      # first session (inclusive), YYYY-MM-DD
    end: str        # last session (inclusive)
    sessions: int
    kind: str       # full | calendar_half | recent
    partial: bool = False
    note: str = ""

    def to_dict(self):
        return asdict(self)


def scored_sessions(coverage: pd.DataFrame, warmup_sessions: int) -> pd.DatetimeIndex:
    s = pd.DatetimeIndex(coverage.index)
    return s[warmup_sessions:]


def last_complete_session(coverage: pd.DataFrame) -> pd.Timestamp:
    full = coverage[coverage["present"] == coverage["minutes"]]
    return pd.Timestamp(full.index.max())


def build_windows(coverage: pd.DataFrame, warmup_sessions: int, recent_months: int = 6,
                  halves: bool = True) -> list[Window]:
    scored = scored_sessions(coverage, warmup_sessions)
    end = min(pd.Timestamp(scored.max()), last_complete_session(coverage))
    scored = scored[scored <= end]
    out = [Window("full", "Full scored history", scored[0].date().isoformat(), end.date().isoformat(),
                  len(scored), "full")]
    if halves:
        for (y, h), grp in pd.Series(scored, index=scored).groupby([scored.year, (scored.month - 1) // 6]):
            lo = pd.Timestamp(y, 1 if h == 0 else 7, 1)
            hi = pd.Timestamp(y, 6, 30) if h == 0 else pd.Timestamp(y, 12, 31)
            partial = grp.index.min() > lo + pd.offsets.BDay(3) or grp.index.max() < hi - pd.offsets.BDay(3)
            out.append(Window(f"{y}H{h + 1}", f"{y} H{h + 1}", grp.index.min().date().isoformat(),
                              grp.index.max().date().isoformat(), len(grp), "calendar_half",
                              bool(partial), "clipped to available data" if partial else ""))
    if recent_months:
        start_bound = end - pd.DateOffset(months=recent_months) + pd.Timedelta(days=1)
        rec = scored[scored >= start_bound]
        out.append(Window(f"recent_{recent_months}m", f"Latest {recent_months} months",
                          rec[0].date().isoformat(), end.date().isoformat(), len(rec), "recent",
                          False, "EXPLORATORY — overlaps the full sample; not a holdout"))
    return out
