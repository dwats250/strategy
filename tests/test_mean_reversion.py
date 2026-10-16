"""VMR-L mean-reversion rules on hand-built bars (synthetic; no market evidence)."""
import numpy as np
import pandas as pd
import pytest

from conftest import et
from stratlab.data.sessions import ET, assign_regular_sessions, resample_session_bars, session_table
from stratlab.engine import ExecutionConfig, build_execution_frame, run_backtest
from stratlab.strategies.vwap_mean_reversion import VwapMeanReversion, mr_features
from stratlab.synthetic import flat_session_bars, set_bar
from stratlab.volatility import atr_wilder, true_range

CFG = ExecutionConfig(cash=100_000, commission_per_share=0, slippage_per_share=0)
D = "2025-01-03"


def _bars(path_day2):
    """Day 1: 100 +/- 0.05 every minute (warms ATR). Day 2: from `path_day2` {HH:MM: (o,h,l,c)} else 100 +/- 0.05."""
    s = session_table("2025-01-02", D)
    b = flat_session_bars(s, price=100.0)
    b["High"] = 100.05; b["Low"] = 99.95
    for hm, (o, h, l, c) in path_day2.items():
        set_bar(b, f"{D} {hm}", o, h, l, c)
    return s, b


def _run(s, b, **params):
    rth = assign_regular_sessions(b, s)
    sig = resample_session_bars(rth, 5, s)
    feats = VwapMeanReversion.build_features(sig, **params)
    frame = build_execution_frame(rth, sig, feats, s, 5, 5)
    return run_backtest(VwapMeanReversion, frame, CFG, params), feats


def _shock_down(extra=None):
    p = {}
    for t in pd.date_range(f"{D} 10:30", f"{D} 10:34", freq="1min"):       # one-bar plunge to 98
        p[t.strftime("%H:%M")] = (99.6, 99.6, 97.95, 98.0)
    for t in pd.date_range(f"{D} 10:35", f"{D} 10:39", freq="1min"):       # failed extension: higher low, higher close
        p[t.strftime("%H:%M")] = (98.05, 98.35, 98.0, 98.3)
    for t in pd.date_range(f"{D} 10:40", f"{D} 11:39", freq="1min"):       # recovery to 100.2
        x = 98.3 + (t - pd.Timestamp(f"{D} 10:40")).seconds / 3600 * 1.9
        p[t.strftime("%H:%M")] = (x, x + 0.03, x - 0.03, x)
    for t in pd.date_range(f"{D} 11:40", f"{D} 15:59", freq="1min"):
        p[t.strftime("%H:%M")] = (100.2, 100.25, 100.15, 100.2)
    p.update(extra or {})
    return p


def test_true_range_and_wilder_atr_by_hand():
    bars = pd.DataFrame({"High": [10, 12, 11, 15], "Low": [9, 10, 8, 13], "Close": [9.5, 11, 9, 14]})
    assert true_range(bars).tolist() == [1, 2.5, 3, 6]            # gap-aware: |15-9| = 6
    a = atr_wilder(bars, 2)
    assert np.isnan(a[0]) and a[1] == pytest.approx(1.75) and a[2] == pytest.approx((1.75 + 3) / 2)


def test_failed_extension_long_entry_stop_and_vwap_exit():
    s, b = _bars(_shock_down())
    out, f = _run(s, b, k=3.0)
    ext = f.loc[pd.Timestamp(f"{D} 10:30", tz=ET).tz_convert("UTC")]
    cur = f.loc[pd.Timestamp(f"{D} 10:35", tz=ET).tz_convert("UTC")]
    assert ext.E <= -3.0                                          # extended bar
    assert cur.s_low > cur.low_prev and cur.s_close > cur.close_prev   # failed extension
    t = out.trades[out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == D].iloc[0]
    assert t.side == "long" and et(t.entry_time) == f"{D} 10:40"
    assert t.initial_stop == pytest.approx(97.94)                 # min(97.95, 98.0) - 0.01
    assert t.exit_reason == "vwap_reached"


def test_no_entry_while_still_extending():
    p = _shock_down({hm.strftime("%H:%M"): (98.0, 98.05, 97.5, 97.6) for hm in pd.date_range(f"{D} 10:35", f"{D} 10:39", freq="1min")})
    s, b = _bars(p)
    out, _ = _run(s, b, k=3.0)
    early = out.trades[out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d %H:%M") == f"{D} 10:40"]
    assert early.empty                                            # new low: no failed extension yet


def test_extension_only_enters_on_the_extended_bar():
    s, b = _bars(_shock_down())
    out, _ = _run(s, b, k=3.0, trigger="extension_only")
    t = out.trades[out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == D].iloc[0]
    assert et(t.entry_time) == f"{D} 10:35" and t.initial_stop == pytest.approx(97.94)


def test_half_target_is_fixed_halfway_to_vwap():
    s, b = _bars(_shock_down())
    out, f = _run(s, b, k=3.0, exit_mode="half_target")
    cur = f.loc[pd.Timestamp(f"{D} 10:35", tz=ET).tz_convert("UTC")]
    t = out.trades[out.trades.entry_time.dt.tz_convert(ET).dt.strftime("%Y-%m-%d") == D].iloc[0]
    assert t.target == pytest.approx(round(cur.s_close + 0.5 * (cur.vwap - cur.s_close), 2))
    assert t.exit_reason == "target"


def test_shock_filter_blocks_sustained_drift_but_not_a_shock():
    # sustained: a slow slide from 100 to 97.5 over two hours, then a failed-extension bar
    p = {}
    for t in pd.date_range(f"{D} 09:30", f"{D} 11:29", freq="1min"):
        x = 100 - (t - pd.Timestamp(f"{D} 09:30")).seconds / 7200 * 2.5
        p[t.strftime("%H:%M")] = (x + 0.02, x + 0.04, x - 0.04, x)
    for t in pd.date_range(f"{D} 11:30", f"{D} 11:34", freq="1min"):
        p[t.strftime("%H:%M")] = (97.5, 97.7, 97.50, 97.65)
    s, b = _bars(p)
    rth = assign_regular_sessions(b, s); sig = resample_session_bars(rth, 5, s); f = mr_features(sig)
    k = float(-f.loc[pd.Timestamp(f"{D} 11:25", tz=ET).tz_convert("UTC")].E) * 0.9
    row = f.loc[pd.Timestamp(f"{D} 11:30", tz=ET).tz_convert("UTC")]
    assert row.E_prev <= -k and row.minabsE_before_prev >= 1.0    # extended, but not a shock
    hm = lambda o: set(pd.to_datetime(o.trades.entry_time, utc=True).dt.tz_convert(ET).dt.strftime("%Y-%m-%d %H:%M")) if len(o.trades) else set()
    plain, _ = _run(s, b, k=k)
    filt, _ = _run(s, b, k=k, shock_filter=True)
    assert f"{D} 11:35" in hm(plain)
    assert f"{D} 11:35" not in hm(filt)
    s2, b2 = _bars(_shock_down())                                  # a genuine shock passes the filter
    shock, _ = _run(s2, b2, k=3.0, shock_filter=True)
    assert f"{D} 10:40" in hm(shock)


def test_k_must_be_declared():
    s, b = _bars({})
    with pytest.raises(ValueError, match="pre-declared k"):
        _run(s, b)


MR_CONFIG = """
[experiment]
id = "T-MR"
study = "experiments"
trials_planned = 5
[data]
dataset = "synthetic"
warmup_sessions = 5
[windows]
calendar_halves = true
recent_months = 2
[[variants]]
id = "MR0"
role = "baseline"
strategy = "stratlab.strategies.vwap_mean_reversion:VwapMeanReversion"
params = { k = 2.0 }
[[variants]]
id = "MR1"
strategy = "stratlab.strategies.vwap_mean_reversion:VwapMeanReversion"
params = { k = 2.0, trigger = "extension_only" }
[[variants]]
id = "MR3"
strategy = "stratlab.strategies.vwap_mean_reversion:VwapMeanReversion"
params = { k = 2.0, shock_filter = true }
[[variants]]
id = "MR4"
strategy = "stratlab.strategies.vwap_mean_reversion:VwapMeanReversion"
params = { k = 2.0, exit_mode = "half_target" }
[[variants]]
id = "BENCH"
role = "benchmark"
strategy = "stratlab.strategies.benchmarks:SessionHold"
params = {}
"""


def test_runs_through_existing_runner_and_report(tmp_path):
    """Reuse proof: the new family needs only its module + config; runner, accounting,
    metrics and report are unchanged. Synthetic prices: no market evidence."""
    import json
    from stratlab.experiment import prepare_market, run_experiment
    from stratlab.report.present import build_presentation, extract_payload
    from stratlab.synthetic import random_walk_bars
    cfg = tmp_path / "mr.toml"
    cfg.write_text(MR_CONFIG)
    md = prepare_market({}, bars_1m=random_walk_bars("2025-03-03", "2025-06-30", seed=21), identity={"dataset_id": "synthetic", "sha256": "n/a"})
    run = run_experiment(cfg, out_root=tmp_path, market=md, synthetic_label="SYNTHETIC", ledger=False, now="T")
    m = json.loads((run / "metrics.json").read_text())
    for vid in ("MR0", "MR1", "MR3", "MR4", "BENCH"):
        assert m[vid]["full"]["status"] == "ok"
    assert m["MR0"]["full"]["trade"]["trades"] > 0 and m["MR4"]["full"]["trade"]["exit_reasons"].get("target", 0) > 0
    assert "diff_vs_baseline" in m["MR1"]["full"] and "diff_vs_baseline" not in m["BENCH"]["full"]
    assert (run / "report.html").exists()
    out = build_presentation(run, run / "report.html", "report_v2.html", {"title_short": "MR synthetic"},
                             require_tracked_source=False, regenerate_bars=False)
    assert extract_payload(out)["presentation"]["provenance"]["verification"]["mismatches"] == 0
