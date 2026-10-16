"""Deterministic synthetic minute bars on real exchange sessions.

For framework tests and clearly-labelled demonstrations only. Nothing produced here
is market evidence.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data.sessions import ET, session_table

SYNTHETIC_LABEL = "SYNTHETIC — framework demonstration, not market data"


def flat_session_bars(sessions: pd.DataFrame, price: float = 100.0, volume: float = 1000.0) -> pd.DataFrame:
    """Every RTH minute of every session at a constant price."""
    frames = []
    for sess, row in sessions.iterrows():
        idx = pd.date_range(row["open"], row["close"], freq="1min", inclusive="left")
        frames.append(pd.DataFrame({"Open": price, "High": price, "Low": price, "Close": price,
                                    "Volume": volume}, index=idx))
    out = pd.concat(frames)
    out.index = pd.DatetimeIndex(out.index, name="ts_utc").as_unit("ns")
    return out


def set_bar(bars: pd.DataFrame, et_time: str, o: float, h: float, l: float, c: float,
            volume: float | None = None) -> None:
    """Overwrite one minute addressed by Eastern wall-clock time 'YYYY-MM-DD HH:MM'."""
    ts = pd.Timestamp(et_time, tz=ET).tz_convert("UTC")
    if ts not in bars.index:
        raise KeyError(f"{et_time} ET is not an RTH minute in this frame")
    bars.loc[ts, ["Open", "High", "Low", "Close"]] = [o, h, l, c]
    if volume is not None:
        bars.loc[ts, "Volume"] = volume


def random_walk_bars(start: str, end: str, seed: int = 7, s0: float = 500.0,
                     drift_bp: float = 0.0, vol_bp: float = 4.0) -> pd.DataFrame:
    """Seeded random-walk RTH minutes with intraday trend episodes, for demos.

    Each session gets a random trend regime so VWAP/EMA logic has something to do.
    """
    rng = np.random.default_rng(seed)
    sessions = session_table(start, end)
    frames = []
    price = s0
    for sess, row in sessions.iterrows():
        n = int(row["minutes"])
        regime = rng.choice([-1.0, 0.0, 1.0]) * rng.uniform(0.0, 0.25)
        gap = rng.normal(0, 15) / 1e4
        price *= 1 + gap
        rets = rng.normal((drift_bp + regime) / 1e4, vol_bp / 1e4, size=n)
        # mid-session reversal episode
        k = rng.integers(60, max(61, n - 60))
        rets[k:k + 45] -= 2 * regime / 1e4
        closes = price * np.cumprod(1 + rets)
        opens = np.r_[price, closes[:-1]]
        wig = np.abs(rng.normal(0, vol_bp / 2e4, size=n)) * closes
        highs = np.maximum(opens, closes) + wig
        lows = np.minimum(opens, closes) - np.abs(rng.normal(0, vol_bp / 2e4, size=n)) * closes
        vol = rng.lognormal(10, 0.4, size=n) * (1 + 2 * np.exp(-np.arange(n) / 30))
        idx = pd.date_range(row["open"], periods=n, freq="1min")
        frames.append(pd.DataFrame({"Open": opens.round(2), "High": highs.round(2),
                                    "Low": lows.round(2), "Close": closes.round(2),
                                    "Volume": vol.round()}, index=idx))
        price = closes[-1]
    out = pd.concat(frames)
    out["High"] = out[["Open", "High", "Close"]].max(axis=1)
    out["Low"] = out[["Open", "Low", "Close"]].min(axis=1)
    out.index = pd.DatetimeIndex(out.index, name="ts_utc").as_unit("ns")
    return out
