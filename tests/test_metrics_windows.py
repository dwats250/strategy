import math

import numpy as np
import pandas as pd
import pytest

from stratlab import metrics as M
from stratlab.windows import build_windows


def test_session_returns_and_sharpe_use_session_sampling():
    eq = pd.Series([101.0, 100.0, 102.0, 102.0], index=pd.date_range("2025-01-02", periods=4).date)
    r = M.session_returns(eq, 100.0)
    assert r.tolist() == pytest.approx([0.01, -1 / 101, 0.02, 0.0])
    m = M.equity_metrics(eq, 100.0)
    assert m["sharpe_daily_ann"] == pytest.approx(r.mean() / r.std(ddof=1) * math.sqrt(252))
    assert m["max_dd_session_close"] == pytest.approx(100 / 101 - 1)
    assert m["pct_sessions_flat"] == pytest.approx(0.25)


def test_trade_metrics_are_per_trade_and_not_annualized():
    t = pd.DataFrame({"pnl": [100.0, -50.0, 300.0, -50.0], "gross_pnl": [101, -49, 301, -49],
                      "costs": [1.0] * 4, "r_multiple": [1.0, -0.5, 3.0, -0.5],
                      "side": ["long", "short", "long", "short"], "exit_reason": ["stop"] * 4,
                      "bars_held": [5, 5, 5, 5]})
    m = M.trade_metrics(t)
    assert m["expectancy_r"] == pytest.approx(0.75)
    assert m["profit_factor"] == pytest.approx(400 / 100)
    assert m["t_stat_r"] == pytest.approx(0.75 / np.std([1, -0.5, 3, -0.5], ddof=1) * 2)
    assert m["top1_share_of_gross_profit"] == pytest.approx(0.75)
    assert m["net_pnl_ex_top1"] == pytest.approx(0.0)
    assert "sharpe" not in " ".join(m)


def test_open_trades_excluded_from_closed_trade_stats():
    t = pd.DataFrame({"pnl": [10.0, 99.0], "gross_pnl": [10, 99], "costs": [0, 0], "r_multiple": [1.0, 9.0],
                      "side": ["long", "long"], "exit_reason": ["stop", "open_at_end"], "bars_held": [1, 1]})
    m = M.trade_metrics(t)
    assert m["trades"] == 1 and m["open_at_end"] == 1 and m["expectancy_r"] == 1.0


def test_monthly_returns_chain_from_initial_capital():
    idx = pd.to_datetime(["2025-01-30", "2025-01-31", "2025-02-27", "2025-02-28"]).date
    mr = M.monthly_returns(pd.Series([105.0, 110.0, 99.0, 99.0], index=idx), 100.0)
    assert mr.tolist() == pytest.approx([0.10, 99 / 110 - 1])


def test_expected_max_sharpe_grows_with_trials():
    a = M.expected_max_sharpe(1, 250)["sr_annualized"]
    b = M.expected_max_sharpe(6, 250)["sr_annualized"]
    c = M.expected_max_sharpe(50, 250)["sr_annualized"]
    assert a == 0 and 0 < b < c
    assert b == pytest.approx(1.27, abs=0.05)


def _cov(dates, full=True):
    d = pd.DatetimeIndex(dates)
    return pd.DataFrame({"minutes": 390, "early_close": False, "present": 390 if full else 300,
                         "missing": 0}, index=d)


def test_windows_exact_dates_recent_and_warmup():
    sessions = pd.bdate_range("2024-09-03", "2026-08-21")
    w = build_windows(_cov(sessions), warmup_sessions=5, recent_months=6)
    full = w[0]
    assert full.start == sessions[5].date().isoformat() and full.end == "2026-08-21"
    rec = w[-1]
    assert rec.kind == "recent" and rec.end == "2026-08-21" and rec.start == "2026-02-23"
    halves = [x for x in w if x.kind == "calendar_half"]
    assert [x.id for x in halves] == ["2024H2", "2025H1", "2025H2", "2026H1", "2026H2"]
    assert halves[0].partial and halves[-1].partial and not halves[1].partial
    assert sum(x.sessions for x in halves) == full.sessions


def test_recent_window_ends_on_last_complete_session():
    sessions = pd.bdate_range("2025-01-02", "2025-12-31")
    cov = _cov(sessions)
    cov.iloc[-1, cov.columns.get_loc("present")] = 100      # last session truncated
    w = build_windows(cov, 5, 6)
    assert w[0].end == sessions[-2].date().isoformat() and w[-1].end == sessions[-2].date().isoformat()


def test_concentration_share_counts_winners_only():
    c = M.concentration(pd.Series([100.0, -50.0]))
    assert c["top1_share_of_gross_profit"] == 1.0 and c["top5_share_of_gross_profit"] == 1.0
    assert c["net_pnl_ex_top1"] == -50.0


def test_recent_window_flagged_when_history_shorter_than_n_months():
    sessions = pd.bdate_range("2025-03-03", "2025-05-30")
    rec = build_windows(_cov(sessions), 5, 6)[-1]
    assert rec.partial and "CLIPPED" in rec.note
