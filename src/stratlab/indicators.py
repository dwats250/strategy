"""Indicator math. Pure functions over bar frames; no execution logic.

Conventions follow TradingView/Pine where a strategy cites a chart setting:
- `ema`: alpha = 2/(n+1), seeded with the SMA of the first n values (Pine `ta.ema`),
  continuous across sessions (an RTH-only chart feeds it RTH bars only).
- `session_vwap`: cumulative sum(source * volume) / cumulative volume, reset at each
  session open ("Anchor Period: Session" on an RTH-only chart).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SOURCES = {
    "close": lambda b: b["Close"],
    "hlc3": lambda b: (b["High"] + b["Low"] + b["Close"]) / 3.0,
    "ohlc4": lambda b: (b["Open"] + b["High"] + b["Low"] + b["Close"]) / 4.0,
    "hl2": lambda b: (b["High"] + b["Low"]) / 2.0,
}


def price_source(bars: pd.DataFrame, source: str) -> pd.Series:
    try:
        return SOURCES[source](bars)
    except KeyError:
        raise ValueError(f"unknown price source {source!r}; choose from {sorted(SOURCES)}") from None


def ema(values: pd.Series, length: int) -> pd.Series:
    """Pine-style EMA: NaN for the first n-1 values, SMA seed at index n-1, then recursion."""
    x = values.to_numpy(dtype="float64")
    out = np.full(len(x), np.nan)
    if len(x) < length:
        return pd.Series(out, index=values.index)
    alpha = 2.0 / (length + 1.0)
    out[length - 1] = x[:length].mean()
    for i in range(length, len(x)):
        out[i] = alpha * x[i] + (1.0 - alpha) * out[i - 1]
    return pd.Series(out, index=values.index)


def session_vwap(bars: pd.DataFrame, source: str = "hlc3", session_col: str = "session") -> pd.Series:
    """Session-anchored VWAP. A session whose cumulative volume is still 0 yields NaN."""
    src = price_source(bars, source)
    pv = (src * bars["Volume"]).groupby(bars[session_col]).cumsum()
    vol = bars["Volume"].groupby(bars[session_col]).cumsum()
    return (pv / vol.where(vol > 0)).rename("vwap")


def crossed_above(a: pd.Series, b: pd.Series, a_prev: pd.Series, b_prev: pd.Series) -> pd.Series:
    """True on the bar where a moves from <= b to > b (Pine `ta.crossover`)."""
    return (a > b) & (a_prev <= b_prev)


def crossed_below(a: pd.Series, b: pd.Series, a_prev: pd.Series, b_prev: pd.Series) -> pd.Series:
    return (a < b) & (a_prev >= b_prev)
