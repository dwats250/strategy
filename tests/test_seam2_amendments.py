"""Owner amendments before the seam-2 freeze (2026-10-16)."""
import numpy as np
import pandas as pd
import pytest

from conftest import et, make_frame, run_plan
from stratlab.data.sessions import ET, assign_regular_sessions, resample_session_bars, session_table
from stratlab.engine import ExecutionConfig, build_execution_frame, run_backtest
from stratlab.strategies.benchmarks import SessionHold
from stratlab.strategies.vwap_reclaim import VwapReclaim
from stratlab.synthetic import flat_session_bars, set_bar

D = "2025-01-02"


def test_initial_account_risk_columns_hand_checked(one_session):
    b = flat_session_bars(one_session)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0)}).trades.iloc[0]
    assert t["size"] == 99
    assert t.equity_before == pytest.approx(10_000.0)
    assert t.initial_risk_usd == pytest.approx(99 * 1.0)
    assert t.initial_risk_pct_equity == pytest.approx(99 / 10_000)
    assert t.notional_pct_equity == pytest.approx(99 * 100 / 10_000)
    assert np.isnan(t.initial_reward_risk)          # no target


def test_signal_close_target_reports_actual_reward_risk_after_gap(one_session):
    """Target 101 and stop 99 are set at the 09:40 decision (signal close 100). The fill
    gaps to 100.5, so the ACTUAL reward/risk is (101-100.5)/(100.5-99) = 1/3, not 1."""
    b = flat_session_bars(one_session)
    for hm in pd.date_range(f"{D} 09:41", f"{D} 15:59", freq="1min"):
        set_bar(b, hm.strftime("%Y-%m-%d %H:%M"), 100.5, 100.5, 100.5, 100.5)
    t = run_plan(b, one_session, {f"{D} 09:40": ("buy", 99.0, 101.0)}).trades.iloc[0]
    assert t.entry_price == 100.5
    assert t.initial_reward_risk == pytest.approx(0.5 / 1.5)
    assert t.risk_per_share == pytest.approx(1.5)


def test_vwr_rejects_fill_relative_target_basis(one_session):
    rth = assign_regular_sessions(flat_session_bars(one_session), one_session)
    sig = resample_session_bars(rth, 5, one_session)
    frame = build_execution_frame(rth, sig, VwapReclaim.build_features(sig), one_session, 5, 5)
    with pytest.raises(ValueError, match="signal_close"):
        run_backtest(VwapReclaim, frame, ExecutionConfig(cash=10_000), {"target_basis": "fill"})


def _bench(sessions, bars):
    rth = assign_regular_sessions(bars, sessions)
    sig = resample_session_bars(rth, 1, sessions)
    frame = build_execution_frame(rth, sig, SessionHold.build_features(sig), sessions, 1, 5)
    return run_backtest(SessionHold, frame, ExecutionConfig(cash=10_000, commission_per_share=0.0035,
                                                            slippage_per_share=0.01))


def test_session_hold_benchmark_enters_0931_exits_flatten_including_early_close():
    s = session_table("2024-12-23", "2024-12-24")            # 12-24 closes 13:00
    b = flat_session_bars(s)
    set_bar(b, "2024-12-23 09:32", 101, 101, 101, 101)
    set_bar(b, "2024-12-23 15:55", 102, 102, 102, 102)
    out = _bench(s, b)
    t = out.trades
    # Backtesting.py never calls next() on a backtest's FIRST bar, so the first session of a
    # run decides on 09:31 and fills at 09:32; every later session fills at 09:31.
    assert [et(x) for x in t.entry_time] == ["2024-12-23 09:32", "2024-12-24 09:31"]
    assert [et(x) for x in t.exit_time] == ["2024-12-23 15:55", "2024-12-24 12:55"]
    first = t.iloc[0]
    assert first.entry_price == 101 and first.exit_price == 102
    assert first["size"] == int(9990 // (101 + 0.0135))
    assert first.pnl == pytest.approx(first["size"] * 1.0 - 2 * first["size"] * 0.0135)
    assert t.r_multiple.isna().all()                          # no stop -> no R
    assert set(t.exit_reason) == {"session_flatten"}


def test_findings_parser_reads_bullets_under_findings_heading(tmp_path):
    from stratlab.cli import _findings_from_md
    p = tmp_path / "a.md"
    p.write_text("# T\n\n## Context\n- not this\n\n## Findings\n- one\n  continued\n- two\n\n## Other\n- no\n")
    assert _findings_from_md(p) == ["one continued", "two"]
