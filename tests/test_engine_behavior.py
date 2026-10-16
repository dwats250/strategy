"""Hand-checkable demonstrations of the installed Backtesting.py through the lab's engine.

Every expected number below is derivable by hand from the bars set in the test.
Prices sit at 100.00 unless a test overrides a minute. Default config: cash 10,000,
zero costs, notional fraction 0.999  ->  size = floor(9990 / fill_price).
These tests pin behaviour of backtesting==0.6.6; a version bump that changes any of
them must be re-validated, not silently accepted.
"""

import warnings

import numpy as np
import pandas as pd
import pytest
from backtesting import Backtest

from conftest import Scripted, et, make_frame, run_plan
from stratlab.data.sessions import ET, session_table
from stratlab.engine import ExecutionConfig, LabStrategy, run_backtest
from stratlab.synthetic import flat_session_bars, set_bar

D = "2025-01-02"


def test_installed_version_is_the_validated_one():
    import backtesting
    assert backtesting.__version__ == "0.6.6"


# --- completed-bar signals and next-bar execution ------------------------------------

def test_market_entry_fills_at_next_minute_open(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:40", 100, 100, 100, 100)
    set_bar(b, f"{D} 09:41", 101, 101, 101, 101)
    out = run_plan(b, one_session, {f"{D} 09:40": ("buy", None)})
    t = out.trades.iloc[0]
    assert et(t.entry_time) == f"{D} 09:41"
    assert t.entry_price == 101.0          # not the 100.00 decision-minute close
    assert t["size"] == int(9990 // 101)   # 98


def test_five_minute_signal_published_on_last_minute_and_filled_next_bucket(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:34", 100, 100, 100, 103)   # 09:30-09:34 bucket closes at 103
    set_bar(b, f"{D} 09:35", 102, 102, 102, 102)
    feats = lambda sig: pd.DataFrame({"sclose": sig["Close"]})
    frame = make_frame(b, one_session, signal_minutes=5, features=feats)
    at = lambda hm: frame.loc[pd.Timestamp(f"{D} {hm}", tz=ET).tz_convert("UTC").tz_convert(None)]
    assert np.isnan(at("09:33")["sclose"]) and at("09:33")["sig_new"] == 0   # bucket not complete
    assert at("09:34")["sclose"] == 103.0 and at("09:34")["sig_new"] == 1
    assert at("09:34")["sig_end_et_min"] == 9 * 60 + 35
    out = run_plan(b, one_session, {f"{D} 09:34": ("buy", None)}, signal_minutes=5, features=feats)
    t = out.trades.iloc[0]
    assert et(t.entry_time) == f"{D} 09:35" and t.entry_price == 102.0


def test_missing_last_minute_publishes_early_but_fills_after_bucket_end(one_session):
    b = flat_session_bars(one_session)
    b = b.drop(pd.Timestamp(f"{D} 09:39", tz=ET).tz_convert("UTC"))
    feats = lambda sig: pd.DataFrame({"n": sig["n_1m"].astype(float)})
    frame = make_frame(b, one_session, signal_minutes=5, features=feats)
    pub = frame[frame.sig_new == 1].index[:2]
    assert [et(pd.Timestamp(x, tz="UTC")) for x in pub] == [f"{D} 09:34", f"{D} 09:38"]
    out = run_plan(b, one_session, {f"{D} 09:38": ("buy", None)}, signal_minutes=5, features=feats)
    assert et(out.trades.iloc[0].entry_time) == f"{D} 09:40"   # first minute after bucket end


# --- protective stops ----------------------------------------------------------------

def test_initial_stop_can_trigger_in_the_entry_minute(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:41", 100, 100.5, 98.5, 99.5)
    out = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0)})
    t = out.trades.iloc[0]
    assert et(t.entry_time) == et(t.exit_time) == f"{D} 09:41"
    assert t.exit_price == 99.0 and t.exit_reason == "stop" and t.bars_held == 0
    assert t.r_multiple == pytest.approx(-1.0)


def test_gap_through_stop_fills_at_the_worse_open(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:42", 97, 97.5, 96.5, 97)
    out = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0)})
    t = out.trades.iloc[0]
    assert t.exit_price == 97.0 and t.exit_reason == "stop"
    assert t.r_multiple == pytest.approx(-3.0)   # (97-100)/(100-99)


def test_stop_and_target_in_same_minute_resolves_to_stop(one_session):
    """Bar-resolution ambiguity: both levels inside one minute's range. The library
    assumes the stop came first (pessimistic). The lab keeps that assumption and
    counts such trades (see metrics.ambiguous_exits)."""
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:42", 100, 101.5, 98.5, 100)
    long_ = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0, 101.0)}).trades.iloc[0]
    short = run_plan(b, one_session, {f"{D} 09:40": ("sell", 101.0, 99.0)}).trades.iloc[0]
    assert (long_.exit_price, long_.exit_reason) == (99.0, "stop")
    assert (short.exit_price, short.exit_reason) == (101.0, "stop")


def test_target_gapped_through_fills_at_the_better_open(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:42", 103, 103.5, 102.5, 103)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0, 101.0)}).trades.iloc[0]
    assert t.exit_price == 103.0 and t.exit_reason == "target"


def test_discretionary_exit_precedes_a_later_stop_touch_in_the_same_minute(one_session):
    """exit_all() removes the stop before closing, so the market exit fills at the
    minute's open — the first event in that minute."""
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:46", 100, 100, 98, 98.5)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0), f"{D} 09:45": ("exit",)}).trades.iloc[0]
    assert t.exit_price == 100.0 and t.exit_reason == "scripted_exit"


def test_raw_library_close_with_live_stop_also_fills_at_open(one_session):
    """Checked hypothesis: a plain trade.close() with the stop still attached ALSO
    fills at the open (the library queues close orders ahead of the stop). So
    exit_all()'s stop removal is belt-and-braces, not a workaround for a library bug."""
    class RawClose(Scripted):
        def on_signal_bar(self):
            k = pd.Timestamp(self.now(), tz="UTC").tz_convert(ET).strftime("%Y-%m-%d %H:%M")
            if k == f"{D} 09:40":
                self.enter(1, 99.0)
            if k == f"{D} 09:45":
                for tr in self.trades:
                    tr.close()
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:46", 100, 100, 98, 98.5)
    frame = make_frame(b, one_session)
    out = run_backtest(RawClose, frame, ExecutionConfig(cash=10_000, commission_per_share=0,
                                                        slippage_per_share=0))
    assert out.trades.iloc[0].exit_price == 100.0


# --- costs -----------------------------------------------------------------------------

def test_per_share_costs_charged_on_both_sides(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:51", 102, 102, 102, 102)
    cfg = ExecutionConfig(cash=10_000, commission_per_share=0.004, slippage_per_share=0.006)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", None), f"{D} 09:50": ("exit",)}, cfg=cfg).trades.iloc[0]
    assert t["size"] == int(9990 // (100 + 0.01))         # 99: sizing includes the cost
    assert t.gross_pnl == pytest.approx(99 * 2.0)
    assert t.costs == pytest.approx(2 * 99 * 0.01)
    assert t.pnl == pytest.approx(198.0 - 1.98)
    assert t.entry_price == 100.0 and t.exit_price == 102.0  # fills unadjusted; costs are cash


def test_equity_reconciles_to_trade_pnl(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:51", 102, 102, 102, 102)
    cfg = ExecutionConfig(cash=10_000, commission_per_share=0.004, slippage_per_share=0.006)
    out = run_plan(b, one_session, {f"{D} 09:40": ("buy", None), f"{D} 09:50": ("exit",)}, cfg=cfg)
    assert out.equity.Equity.iloc[-1] == pytest.approx(10_000 + out.trades.pnl.sum())


# --- sizing and insufficient capital -----------------------------------------------------

def test_order_larger_than_capital_is_cancelled_with_warning(one_session):
    b = flat_session_bars(one_session)
    out = run_plan(b, one_session, {f"{D} 09:40": ("buy_units", 200)})   # 200*100 > 10,000
    assert out.trades.empty
    assert any("insufficient margin" in w for w in out.warnings)


def test_relative_size_with_equity_below_one_share_is_cancelled(one_session):
    b = flat_session_bars(one_session, price=20_000.0)
    out = run_plan(b, one_session, {f"{D} 09:40": ("buy", None)})
    assert out.trades.empty
    assert any("insufficient margin" in w for w in out.warnings)


def test_relative_size_uses_the_fill_price_not_the_decision_close(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:41", 110, 110, 110, 110)   # gaps up after the decision
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", None)}).trades.iloc[0]
    assert t["size"] == int(9990 // 110)           # 90, still affordable


# --- sessions: flatten, early close, DST, overnight -----------------------------------

def test_session_flatten_normal_day_fills_at_1555_open(one_session):
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 15:55", 101, 101, 101, 101)
    t = run_plan(b, one_session, {f"{D} 10:00": ("buy", None)}).trades.iloc[0]
    assert et(t.exit_time) == f"{D} 15:55" and t.exit_price == 101.0
    assert t.exit_reason == "session_flatten"


def test_early_close_uses_calendar_not_fixed_clock():
    s = session_table("2024-12-24", "2024-12-24")
    assert bool(s.early_close.iloc[0]) and int(s.minutes.iloc[0]) == 210
    b = flat_session_bars(s)
    assert et(b.index[-1]) == "2024-12-24 12:59"   # the 13:00 auction minute is outside
    t = run_plan(b, s, {"2024-12-24 10:00": ("buy", None)}).trades.iloc[0]
    assert et(t.exit_time) == "2024-12-24 12:55" and t.exit_reason == "session_flatten"


def test_dst_transition_keeps_eastern_clock_rules():
    s = session_table("2025-03-07", "2025-03-10")   # EST Friday, EDT Monday
    assert list(s.index.astype(str)) == ["2025-03-07", "2025-03-10"]
    assert [x.strftime("%H:%M") for x in s.open] == ["14:30", "13:30"]   # UTC
    b = flat_session_bars(s)
    out = run_plan(b, s, {"2025-03-07 10:00": ("buy", None), "2025-03-10 10:00": ("buy", None)})
    assert [et(x) for x in out.trades.entry_time] == ["2025-03-07 10:01", "2025-03-10 10:01"]
    assert [et(x) for x in out.trades.exit_time] == ["2025-03-07 15:55", "2025-03-10 15:55"]


def test_no_entries_after_flatten_decision_and_no_overnight_carry():
    s = session_table("2025-01-02", "2025-01-03")
    b = flat_session_bars(s)
    out = run_plan(b, s, {"2025-01-02 15:50": ("buy", None),   # opens, then flattened
                          "2025-01-02 15:56": ("buy", None)})  # inside flatten zone: ignored
    assert len(out.trades) == 1
    t = out.trades.iloc[0]
    assert et(t.exit_time) == "2025-01-02 15:55"
    assert out.session_equity.index.tolist()[0].isoformat() == "2025-01-02"


def test_interior_session_missing_close_flattens_at_last_available_minute_and_flags():
    s = session_table("2025-01-02", "2025-01-03")
    b = flat_session_bars(s)
    cut = (b.index >= pd.Timestamp("2025-01-02 15:00", tz=ET)) & (b.index < pd.Timestamp("2025-01-03 00:00", tz=ET))
    b = b[~cut]
    frame = make_frame(b, s)
    out = run_plan(b, s, {"2025-01-02 10:00": ("buy", None)})
    t = out.trades.iloc[0]
    assert et(t.exit_time) == "2025-01-02 14:59"      # last available minute's open
    assert frame.flatten_fallback.sum() > 0


# --- unrealized P&L and open positions at the end ----------------------------------------

def test_open_position_at_data_end_is_marked_not_closed(one_session):
    b = flat_session_bars(one_session)
    b = b[b.index < pd.Timestamp(f"{D} 11:00", tz=ET)]   # data ends mid-session
    for t in pd.date_range(f"{D} 10:30", f"{D} 10:58", freq="1min"):
        set_bar(b, t.strftime("%Y-%m-%d %H:%M"), 105, 105, 105, 105)
    set_bar(b, f"{D} 10:59", 105, 106, 104, 105.5)
    out = run_plan(b, one_session, {f"{D} 10:00": ("buy", 90.0)})
    t = out.trades.iloc[0]
    assert t.exit_reason == "open_at_end" and pd.isna(t.exit_time)
    assert t.exit_price == 105.5 and t.pnl == pytest.approx(99 * 5.5)
    # equity marks the open position to the final CLOSE at every bar
    assert out.equity.Equity.iloc[-1] == pytest.approx(10_000 + 99 * 5.5)
    assert out.equity.Equity.iloc[-2] == pytest.approx(10_000 + 99 * 5.0)


def test_library_finalize_would_close_at_last_open_documented(one_session):
    """Why the lab does not use finalize_trades=True: it closes at the last bar's OPEN."""
    b = flat_session_bars(one_session)
    b = b[b.index < pd.Timestamp(f"{D} 11:00", tz=ET)]
    set_bar(b, f"{D} 10:59", 105, 106, 104, 105.5)
    frame = make_frame(b, one_session)
    cls = type("P", (Scripted,), {"plan": {f"{D} 10:00": ("buy", None)}})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        st = Backtest(frame, cls, cash=10_000, finalize_trades=True).run()
    assert st._trades.ExitPrice.iloc[0] == 105.0


# --- determinism -------------------------------------------------------------------------

def test_reruns_are_identical(one_session):
    from stratlab.synthetic import random_walk_bars
    s = session_table("2025-01-02", "2025-01-08")
    b = random_walk_bars("2025-01-02", "2025-01-08", seed=3)
    plan = {f"{d} 10:00": ("buy", None) for d in ["2025-01-02", "2025-01-03", "2025-01-06"]}
    a = run_plan(b, s, plan)
    c = run_plan(b, s, plan)
    pd.testing.assert_frame_equal(a.trades, c.trades)
    pd.testing.assert_frame_equal(a.equity, c.equity)


def test_entry_minute_opening_beyond_stop_has_no_defined_risk(one_session):
    """Review finding: a long whose fill opens BELOW its stop is stopped in the same
    minute at the open; it never had a defined risk, so R is NaN and it is labelled."""
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:41", 98, 98.2, 97.8, 98)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0)}).trades.iloc[0]
    assert t.entry_price == 98.0 and t.exit_price == 98.0
    assert t.exit_reason == "stop_beyond_fill" and np.isnan(t.r_multiple) and np.isnan(t.risk_per_share)


def test_open_beyond_target_with_stop_touch_still_resolves_to_stop_pessimistic(one_session):
    """Review finding: the minute OPENS above the target (so a resting target would have
    filled at the open), but the same minute also trades through the stop. The library
    processes the stop first and fills it at the stop: a pessimistic bias, not just an
    unknowable path. Such exits are flagged ambiguous by the experiment runner."""
    b = flat_session_bars(one_session)
    set_bar(b, f"{D} 09:42", 103, 103.5, 98.5, 103)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0, 101.0)}).trades.iloc[0]
    assert (t.exit_price, t.exit_reason) == (99.0, "stop")
