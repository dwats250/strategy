import numpy as np
import pandas as pd
import pytest

from stratlab.indicators import crossed_above, crossed_below, ema, price_source, session_vwap


def test_ema_is_pine_style_sma_seeded():
    x = pd.Series([1.0, 2, 3, 4, 5, 6])
    e = ema(x, 3)
    assert np.isnan(e[0]) and np.isnan(e[1])
    assert e[2] == pytest.approx(2.0)                 # SMA of 1,2,3
    assert e[3] == pytest.approx(0.5 * 4 + 0.5 * 2)   # alpha = 2/(3+1)
    assert e[5] == pytest.approx(0.5 * 6 + 0.5 * (0.5 * 5 + 0.5 * 3))


def test_session_vwap_resets_each_session_and_uses_source():
    bars = pd.DataFrame({
        "Open": [10, 11, 20, 22], "High": [11, 13, 21, 23], "Low": [9, 11, 19, 21],
        "Close": [10, 12, 20, 22], "Volume": [100, 300, 50, 50],
        "session": ["d1", "d1", "d2", "d2"]})
    v = session_vwap(bars, "hlc3")
    assert v[0] == pytest.approx(10.0)
    assert v[1] == pytest.approx((10 * 100 + 12 * 300) / 400)
    assert v[2] == pytest.approx(20.0)                # reset
    o4 = session_vwap(bars, "ohlc4")
    assert o4[1] == pytest.approx((10 * 100 + 11.75 * 300) / 400)   # (11+13+11+12)/4
    assert v[1] != o4[1]


def test_vwap_nan_until_volume():
    bars = pd.DataFrame({"Open": [1, 2], "High": [1, 2], "Low": [1, 2], "Close": [1, 2],
                         "Volume": [0, 10], "session": ["d", "d"]})
    v = session_vwap(bars)
    assert np.isnan(v[0]) and v[1] == pytest.approx(2.0)


def test_cross_helpers():
    a, b = pd.Series([1.0, 3.0]), pd.Series([2.0, 2.0])
    assert crossed_above(a, b, pd.Series([1.0, 1.0]), pd.Series([2.0, 2.0])).tolist() == [False, True]
    assert crossed_below(pd.Series([1.0]), pd.Series([2.0]), pd.Series([3.0]), pd.Series([2.0])).tolist() == [True]


def test_unknown_source_rejected():
    with pytest.raises(ValueError):
        price_source(pd.DataFrame({"Close": [1]}), "vwap")
