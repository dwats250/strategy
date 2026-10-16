import json
import re

import pandas as pd
import pytest

from stratlab.experiment import prepare_market, run_experiment
from stratlab.synthetic import random_walk_bars

CONFIG = """
limitations = ["synthetic"]
[experiment]
id = "T-PIPE"
study = "experiments"
trials_planned = 3
[data]
dataset = "synthetic"
warmup_sessions = 3
[execution]
cash = 50000.0
commission_per_share = 0.0035
slippage_per_share = 0.01
[windows]
calendar_halves = true
recent_months = 1
[[variants]]
id = "B"
role = "baseline"
strategy = "stratlab.strategies.vwap_reclaim:VwapReclaim"
params = {}
[[variants]]
id = "R"
strategy = "stratlab.strategies.vwap_reclaim:VwapReclaim"
params = { exit_mode = "fixed_r" }
[[variants]]
id = "IG"
strategy = "stratlab.strategies.instagram_austin_vwap_ema9:InstagramAustinVwapEma9P0"
params = {}
"""


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("exp")
    cfg = tmp / "t.toml"
    cfg.write_text(CONFIG)
    bars = random_walk_bars("2025-06-02", "2025-08-29", seed=5)
    md = lambda: prepare_market({}, bars_1m=bars, identity={"dataset_id": "synthetic", "sha256": "n/a"})
    a = run_experiment(cfg, out_root=tmp / "a", market=md(), synthetic_label="SYNTHETIC", ledger=False, now="T1")
    b = run_experiment(cfg, out_root=tmp / "b", market=md(), synthetic_label="SYNTHETIC", ledger=False, now="T1")
    return a, b, cfg


def test_equity_reconciles_with_trades_in_every_window(runs):
    a, _, _ = runs
    m = json.loads((a / "metrics.json").read_text())
    for vid, ws in m.items():
        for wid, r in ws.items():
            assert r["status"] == "ok", (vid, wid, r)
            t = pd.read_csv(a / "trades" / f"{vid}__{wid}.csv")
            assert r["equity"]["net_pnl"] == pytest.approx(t["pnl"].sum(), abs=0.01)
            assert r["trade"]["costs"] == pytest.approx(t["costs"].sum(), abs=1e-6)


def test_window_trades_are_the_full_run_trades_in_that_window(runs):
    a, _, _ = runs
    rec = json.loads((a / "run_record.json").read_text())
    for vid in ("B", "R", "IG"):
        full = pd.read_csv(a / "trades" / f"{vid}__full.csv")
        halves = [w for w in rec["windows"] if w["kind"] == "calendar_half"]
        parts = pd.concat([pd.read_csv(a / "trades" / f"{vid}__{w['id']}.csv") for w in halves])
        assert sorted(full.signal_start + full.side) == sorted(parts.signal_start + parts.side)


def test_reruns_are_deterministic(runs):
    a, b, _ = runs
    assert (a / "metrics.json").read_text() == (b / "metrics.json").read_text()
    for p in (a / "trades").iterdir():
        assert p.read_text() == (b / "trades" / p.name).read_text()


def test_run_dirs_are_immutable(runs, tmp_path):
    a, _, cfg = runs
    bars = random_walk_bars("2025-06-02", "2025-06-30", seed=5)
    with pytest.raises(FileExistsError):
        run_experiment(cfg, out_root=a.parent, market=prepare_market({}, bars_1m=bars, identity={}),
                       synthetic_label="S", ledger=False, now="T1")


def test_report_is_self_contained(runs):
    a, _, _ = runs
    html = (a / "report.html").read_text()
    assert "SYNTHETIC" in html
    assert not re.search(r"<script[^>]+src=", html)
    assert not re.search(r"<link[^>]+href=\"?https?:", html)
    assert "window.__DT=" in html and "Plotly" in html


def test_run_record_has_identity_and_trials(runs):
    a, _, _ = runs
    rec = json.loads((a / "run_record.json").read_text())
    assert rec["code"]["code_tree_sha256"] and rec["packages"]["backtesting"] == "0.6.6"
    assert rec["trials"]["planned"] == 3 and rec["trials"]["dsr_threshold_implied"]["sr_annualized"] > 0
    assert rec["windows"][0]["kind"] == "full" and rec["windows"][-1]["kind"] == "recent"


def test_proposed_config_refuses_real_data(tmp_path):
    cfg = tmp_path / "p.toml"
    cfg.write_text(CONFIG.replace('trials_planned = 3', 'trials_planned = 3\nstatus = "PROPOSED"'))
    with pytest.raises(PermissionError, match="PROPOSED"):
        run_experiment(cfg, out_root=tmp_path, market=None, ledger=False)
