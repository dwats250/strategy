"""Volatility measures on signal-timeframe bars (kept out of indicators.py, which is pinned).

`atr_wilder` follows Pine `ta.atr` and the August parity_foundation definition: true range
uses the previous bar's close even across the overnight gap (continuous RTH series), and
is smoothed by Wilder's RMA seeded with the SMA of the first `length` true ranges.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def true_range(bars: pd.DataFrame) -> pd.Series:
    h, l, c = bars["High"].to_numpy(float), bars["Low"].to_numpy(float), bars["Close"].to_numpy(float)
    prev = np.r_[np.nan, c[:-1]]
    tr = np.where(np.isnan(prev), h - l, np.maximum.reduce([h - l, np.abs(h - prev), np.abs(l - prev)]))
    return pd.Series(tr, index=bars.index, name="tr")


def atr_wilder(bars: pd.DataFrame, length: int = 14) -> pd.Series:
    tr = true_range(bars).to_numpy()
    out = np.full(len(tr), np.nan)
    if len(tr) >= length:
        out[length - 1] = tr[:length].mean()
        for i in range(length, len(tr)):
            out[i] = (out[i - 1] * (length - 1) + tr[i]) / length
    return pd.Series(out, index=bars.index, name="atr")
