"""Hand-built bars that should (and should not) trigger each rule."""
import pandas as pd
import pytest

from conftest import et, make_frame
from stratlab.data.sessions import ET, assign_regular_sessions, resample_session_bars, session_table
from stratlab.engine import ExecutionConfig, build_execution_frame, run_backtest
from stratlab.strategies.instagram_austin_vwap_ema9 import InstagramAustinVwapEma9P0
from stratlab.strategies.vwap_reclaim import VwapReclaim
from stratlab.synthetic import flat_session_bars, set_bar

CFG = ExecutionConfig(cash=100_000, commission_per_share=0, slippage_per_share=0)


def _frame(bars, sessions, cls, **params):
    rth = assign_regular_sessions(bars, sessions)
    m = params.get("signal_minutes", cls.signal_minutes)
    sig = resample_session_bars(rth, m, sessions)
    feats = cls.build_features(sig, **params)
    return build_execution_frame(rth, sig, feats, sessions, m, 5), feats


def _ramp(sessions, day, start, end, p0, p1):
    """Linear minute closes from p0 to p1 between ET times (inclusive)."""
    times = pd.date_range(f"{day} {start}", f"{day} {end}", freq="1min")
    b = flat_session_bars(sessions, price=p0)
    for i, t in enumerate(times):
        px = p0 + (p1 - p0) * i / (len(times) - 1)
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), px, px, px, px)
    after = pd.date_range(f"{day} {end}", f"{day} 15:59", freq="1min")[1:]
    for t in after:
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), p1, p1, p1, p1)
    return b


def test_vwr_touch_reclaim_long_with_ema_confirmation():
    s = session_table("2025-01-02", "2025-01-03")
    b = flat_session_bars(s, price=100.0)
    # Day 2: drift up 100 -> 101 by 10:30 so VWAP < price and EMA9 < price, then a 5m bar
    # 10:30-10:34 that dips through VWAP and closes back above both.
    d = "2025-01-03"
    for i, t in enumerate(pd.date_range(f"{d} 09:30", f"{d} 10:29", freq="1min")):
        px = 100 + i / 59
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), px, px, px, px)
    for t in pd.date_range(f"{d} 10:30", f"{d} 15:59", freq="1min"):
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), 101, 101, 101, 101)
    set_bar(b, f"{d} 10:32", 101, 101, 100.2, 100.9)      # touch below session VWAP (~100.5)
    set_bar(b, f"{d} 10:34", 100.9, 101.2, 100.9, 101.2)  # close > VWAP and > EMA9
    frame, feats = _frame(b, s, VwapReclaim)
    row = feats.loc[pd.Timestamp(f"{d} 10:30", tz=ET).tz_convert("UTC")]
    assert row.s_low <= row.vwap < row.s_close and row.s_close > row.ema
    out = run_backtest(VwapReclaim, frame, CFG)
    t = out.trades[out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == d]
    first = t.iloc[0]
    assert et(first.entry_time) == f"{d} 10:35" and first.side == "long"
    assert first.initial_stop == pytest.approx(min(100.2 - 0.01, round(101.2 * (1 - 5e-4), 2)))


def test_vwr_fixed_r_target_is_set_from_signal_close():
    s = session_table("2025-01-02", "2025-01-03")
    b = flat_session_bars(s, price=100.0)
    d = "2025-01-03"
    for i, t in enumerate(pd.date_range(f"{d} 09:30", f"{d} 10:29", freq="1min")):
        px = 100 + i / 59
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), px, px, px, px)
    for t in pd.date_range(f"{d} 10:30", f"{d} 15:59", freq="1min"):
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), 101, 101, 101, 101)
    set_bar(b, f"{d} 10:32", 101, 101, 100.2, 100.9)
    set_bar(b, f"{d} 10:34", 100.9, 101.2, 100.9, 101.2)
    set_bar(b, f"{d} 10:50", 101.2, 103.5, 101.2, 103.0)   # reaches target
    frame, _ = _frame(b, s, VwapReclaim, exit_mode="fixed_r")
    out = run_backtest(VwapReclaim, frame, CFG, {"exit_mode": "fixed_r"})
    t = out.trades[out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == d].iloc[0]
    risk = 101.2 - t.initial_stop
    assert t.target == pytest.approx(round(101.2 + 2 * risk, 2))
    assert t.exit_reason == "target" and t.exit_price == pytest.approx(t.target)


def test_vwr_entry_window_blocks_late_signals():
    s = session_table("2025-01-02", "2025-01-03")
    b = flat_session_bars(s, price=100.0)
    d = "2025-01-03"
    for i, t in enumerate(pd.date_range(f"{d} 09:30", f"{d} 12:29", freq="1min")):
        px = 100 + i / 179
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), px, px, px, px)
    for t in pd.date_range(f"{d} 12:30", f"{d} 15:59", freq="1min"):
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), 101, 101, 101, 101)
    set_bar(b, f"{d} 12:32", 101, 101, 100.2, 100.9)
    set_bar(b, f"{d} 12:34", 100.9, 101.2, 100.9, 101.2)
    frame, _ = _frame(b, s, VwapReclaim)
    morning = run_backtest(VwapReclaim, frame, CFG, {"entry_end": "11:30"}).trades
    allday = run_backtest(VwapReclaim, frame, CFG).trades
    late = lambda t: t[pd.to_datetime(t.entry_time, utc=True).dt.tz_convert(ET).dt.strftime("%H:%M") == "12:35"] if len(t) else t
    assert len(late(allday)) == 1 and len(late(morning)) == 0


def test_ig_p0_enters_on_completed_3m_cross_and_exits_on_close_through_ema():
    s = session_table("2025-01-02", "2025-01-03")
    d = "2025-01-03"
    b = flat_session_bars(s, price=100.0)
    # Fall then rise: EMA9 dips below VWAP, then crosses back above.
    for i, t in enumerate(pd.date_range(f"{d} 09:30", f"{d} 10:29", freq="1min")):
        px = 100 - i / 59
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), px, px, px, px)
    for i, t in enumerate(pd.date_range(f"{d} 10:30", f"{d} 11:29", freq="1min")):
        px = 99 + 2 * i / 59
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), px, px, px, px)
    for t in pd.date_range(f"{d} 11:30", f"{d} 15:59", freq="1min"):
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), 98, 98, 98, 98)     # collapse -> close < EMA9
    frame, feats = _frame(b, s, InstagramAustinVwapEma9P0)
    f = feats[feats.index.tz_convert(ET).strftime("%Y-%m-%d") == d]
    cross = f[(f.ema_prev <= f.vwap_prev) & (f.ema > f.vwap)]
    assert len(cross) >= 1
    out = run_backtest(InstagramAustinVwapEma9P0, frame, CFG)
    longs = out.trades[(out.trades.side == "long") & (out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == d)]
    first_cross_end = cross.index[0] + pd.Timedelta(minutes=3)
    assert longs.iloc[0].entry_time == first_cross_end      # next minute after the 3m bar completes
    assert longs.iloc[0].exit_reason in ("ema9_close_through", "stop")
