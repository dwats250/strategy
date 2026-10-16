"""Presentation-only re-render: reuse a report's verified payload, never recompute."""
import json
import shutil

import pytest

from stratlab.experiment import prepare_market, run_experiment
from stratlab.report.present import PayloadMismatch, build_presentation, extract_payload, verify_payload
from stratlab.synthetic import random_walk_bars

CONFIG = """
limitations = ["synthetic"]
[experiment]
id = "T-PRES"
study = "experiments"
trials_planned = 2
[data]
dataset = "synthetic"
warmup_sessions = 3
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
id = "H"
role = "benchmark"
strategy = "stratlab.strategies.benchmarks:SessionHold"
params = {}
"""


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("pres")
    cfg = tmp / "c.toml"
    cfg.write_text(CONFIG)
    md = prepare_market({}, bars_1m=random_walk_bars("2025-06-02", "2025-08-15", seed=9), identity={"dataset_id": "synthetic", "sha256": "n/a"})
    return run_experiment(cfg, out_root=tmp, market=md, synthetic_label="SYNTHETIC", ledger=False, now="T")


def test_payload_matches_pinned_regeneration(run):
    p = extract_payload(run / "report.html")
    chk = verify_payload(p, run, regenerate_bars=False)    # synthetic prices are not stored
    assert chk["mismatches"] == 0 and chk["values_compared"] > 1000
    assert set(chk["sections_compared"]) == {"config_toml", "limitations", "record", "variants"}


def test_presentation_records_both_identities_and_never_overwrites(run):
    out = build_presentation(run, run / "report.html", "report_v2_test.html",
                             {"title_short": "Demo <b>title</b>", "headline": "h", "data_notice": "n"},
                             require_tracked_source=False, regenerate_bars=False)
    p = extract_payload(out)
    prov = p["presentation"]["provenance"]
    assert prov["payload_source"]["tracked"] is False and prov["verification"]["mismatches"] == 0
    assert prov["payload_computed_under_code_tree"] == json.loads((run / "run_record.json").read_text())["code"]["code_tree_sha256"]
    assert prov["presentation_code"]["code_tree_sha256"] and prov["template"] == "template_v2.html"
    assert "<title>Demo &lt;b&gt;title&lt;/b&gt;</title>" in out.read_text()
    with pytest.raises(FileExistsError):
        build_presentation(run, run / "report.html", "report_v2_test.html", {}, require_tracked_source=False,
                           regenerate_bars=False)


def test_tampered_saved_results_are_refused(run, tmp_path):
    copy = tmp_path / run.name
    shutil.copytree(run, copy)
    m = json.loads((copy / "metrics.json").read_text())
    m["B"]["full"]["equity"]["total_return"] += 0.01
    (copy / "metrics.json").write_text(json.dumps(m))
    with pytest.raises(PayloadMismatch, match="total_return"):
        build_presentation(copy, copy / "report.html", "x.html", {}, require_tracked_source=False,
                           regenerate_bars=False)


def test_untracked_source_report_is_refused(run):
    with pytest.raises(PayloadMismatch, match="not committed"):
        build_presentation(run, run / "report.html", "y.html", {})


def _tamper(p, how):
    v = p["variants"][0]
    if how == "monthly":
        k = next(iter(v["monthly"])); v["monthly"][k] = 0.5
    elif how == "rolling":
        v["rolling"]["v"][-1] = 3.0
    elif how == "trade_field":
        v["trades"][0]["entry_px"] = 0.0
    elif how == "trade_pnl_swap":
        a, b = v["trades"][0], v["trades"][1]; a["pnl"], b["pnl"] = b["pnl"], a["pnl"]
    elif how == "role":
        p["variants"][1]["role"] = "benchmark"
    elif how == "label":
        v["label"] = "Something else"
    elif how == "coverage":
        p["record"]["coverage"]["last_session"] = "2030-01-01"
    elif how == "synthetic_flag":
        p["record"]["synthetic"] = None
    elif how == "drop_variant":
        p["variants"].pop()
    elif how == "extra_metric":
        v["results"]["full"]["trade"]["made_up"] = 1.0
    elif how == "config_toml":
        p["config_toml"] = "x"
    elif how == "limitations":
        p["limitations"] = []
    elif how == "equity_point":
        v["series"]["full"]["eq"][3] += 0.5


@pytest.mark.parametrize("how", ["monthly", "rolling", "trade_field", "trade_pnl_swap", "role", "label", "coverage",
                                 "synthetic_flag", "drop_variant", "extra_metric", "config_toml", "limitations", "equity_point"])
def test_payload_side_tampering_is_refused(run, how):
    p = extract_payload(run / "report.html")
    _tamper(p, how)
    with pytest.raises(PayloadMismatch):
        verify_payload(p, run, regenerate_bars=False)
