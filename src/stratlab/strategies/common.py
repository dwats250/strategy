"""Shared feature construction for VWAP/EMA strategies (signal-timeframe bars)."""

from __future__ import annotations

import pandas as pd

from ..indicators import ema, session_vwap


def hhmm_to_min(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def vwap_ema_features(sig: pd.DataFrame, vwap_source: str, ema_length: int) -> pd.DataFrame:
    """Completed-bar features. `*_prev` are the previous signal bar's values within the
    same session (NaN on a session's first bar, so no cross is detected across the
    overnight gap for VWAP; EMA itself is continuous across sessions)."""
    f = pd.DataFrame(index=sig.index)
    f["s_open"] = sig["Open"]
    f["s_high"] = sig["High"]
    f["s_low"] = sig["Low"]
    f["s_close"] = sig["Close"]
    f["vwap"] = session_vwap(sig, vwap_source)
    f["ema"] = ema(sig["Close"], ema_length)
    g = sig["session"]
    f["vwap_prev"] = f["vwap"].groupby(g).shift(1)
    f["ema_prev"] = f["ema"].groupby(g).shift(1)
    return f
