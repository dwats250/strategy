"""Experiment runner: one config -> baseline + variants x windows -> immutable run directory.

A run directory holds everything needed to audit or reproduce the result:
  run_record.json   config (verbatim + hash), code identity, dataset identity, package
                    versions, windows with exact dates, trials/hurdle, warnings
  metrics.json      per variant x window: equity metrics, trade metrics, diffs
  trades/<variant>__<window>.csv, equity/<variant>__<window>.csv (session close),
  report.html       self-contained interactive report (built from the files above)
and one LEDGER.csv row per variant (every configuration evaluated, including failures).
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import importlib
import json
import platform
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from . import metrics as M
from .data.sessions import assign_regular_sessions, coverage, resample_session_bars, session_table
from .data.store import REPO_ROOT, load_dataset
from .engine import ExecutionConfig, build_execution_frame, run_backtest
from .windows import Window, build_windows

LEDGER_FIELDS = [
    "run_id", "run_utc", "experiment_id", "variant_id", "role", "strategy", "params_json",
    "config_sha256", "code_commit", "code_dirty", "code_tree_sha256", "dataset_id",
    "dataset_sha256", "mask", "window", "window_start", "window_end", "sessions",
    "trials_planned", "dsr_threshold_implied", "trades", "net_pnl", "total_return",
    "sharpe_daily_ann", "max_dd_session_close", "expectancy_r", "status", "notes",
]


# ----------------------------------------------------------------------------------
# Config and identity
# ----------------------------------------------------------------------------------

def load_config(path: Path) -> tuple[dict, str]:
    raw = Path(path).read_bytes()
    return tomllib.loads(raw.decode()), hashlib.sha256(raw).hexdigest()


def resolve_strategy(spec: str):
    mod, _, name = spec.partition(":")
    return getattr(importlib.import_module(mod), name)


def code_identity() -> dict:
    src = REPO_ROOT / "src" / "stratlab"
    h = hashlib.sha256()
    files = sorted(p for p in src.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for p in files:
        h.update(str(p.relative_to(REPO_ROOT)).encode())
        h.update(p.read_bytes())

    def git(*args):
        try:
            return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
                                  check=True).stdout.strip()
        except Exception:
            return None
    dirty = git("status", "--porcelain", "--", "src", "pyproject.toml", "uv.lock")
    return {"git_commit": git("rev-parse", "HEAD"), "git_dirty_paths": dirty.splitlines() if dirty else [],
            "code_tree_sha256": h.hexdigest(), "files_hashed": len(files)}


def check_frozen(exp: dict, config_path) -> None:
    """Real-data runs need a FROZEN config pinned to the exact code it was frozen against.

    Allow-list, not deny-list: anything but status = "FROZEN" is refused. The frozen
    config must carry `code_tree_sha256` (from `stratlab identity`) and the source tree
    must match it and be clean, so a frozen experiment cannot silently run new code.
    """
    if str(exp.get("status", "")).upper() != "FROZEN":
        raise PermissionError(f"{config_path}: status is {exp.get('status')!r}; only a FROZEN config "
                              "may run on real data (conventions §b).")
    ident = code_identity()
    pinned = exp.get("code_tree_sha256")
    if not pinned:
        raise PermissionError(f"{config_path}: FROZEN config lacks code_tree_sha256")
    if ident["code_tree_sha256"] != pinned:
        raise PermissionError(f"{config_path}: code tree {ident['code_tree_sha256'][:12]} != pinned {pinned[:12]}; "
                              "the code changed after the freeze")
    if ident["git_dirty_paths"]:
        raise PermissionError(f"uncommitted changes in {ident['git_dirty_paths']}; commit before a real-data run")


def package_versions() -> dict:
    import backtesting, exchange_calendars, numpy, pandas, plotly
    return {"python": platform.python_version(), "backtesting": backtesting.__version__,
            "pandas": pandas.__version__, "numpy": numpy.__version__,
            "exchange_calendars": exchange_calendars.__version__, "plotly": plotly.__version__}


# ----------------------------------------------------------------------------------
# Market data preparation (shared across variants)
# ----------------------------------------------------------------------------------

@dataclass
class MarketData:
    rth: pd.DataFrame
    sessions: pd.DataFrame
    coverage: pd.DataFrame
    identity: dict
    signal_bars: dict


def prepare_market(data_cfg: dict, bars_1m: pd.DataFrame | None = None, identity: dict | None = None) -> MarketData:
    if bars_1m is None:
        bars_1m, identity = load_dataset(data_cfg["dataset"], data_cfg.get("mask"))
    sessions = session_table(bars_1m.index[0], bars_1m.index[-1])
    rth = assign_regular_sessions(bars_1m, sessions)
    sessions = sessions.loc[sessions.index.isin(pd.Index(rth["session"].unique()))]
    cov = coverage(rth, sessions)
    return MarketData(rth, sessions, cov, identity or {}, {})


def signal_bars(md: MarketData, minutes: int) -> pd.DataFrame:
    if minutes not in md.signal_bars:
        md.signal_bars[minutes] = resample_session_bars(md.rth, minutes, md.sessions)
    return md.signal_bars[minutes]


# ----------------------------------------------------------------------------------
# Running
# ----------------------------------------------------------------------------------

def _slice_sessions(df: pd.DataFrame, w: Window, col: str = "session") -> pd.DataFrame:
    s = pd.to_datetime(df[col])
    return df[(s >= pd.Timestamp(w.start)) & (s <= pd.Timestamp(w.end))]


def mark_ambiguous_exits(trades: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    """Flag stop exits whose exit minute ALSO reached the target (resolution ambiguity)."""
    t = trades.copy()
    t["ambiguous_exit"] = False
    if t.empty:
        return t
    hi = frame["High"]
    lo = frame["Low"]
    for i, r in t.iterrows():
        if r["exit_reason"] != "stop" or pd.isna(r.get("target")) or pd.isna(r["exit_time"]):
            continue
        k = pd.Timestamp(r["exit_time"]).tz_convert(None)
        if k not in hi.index:
            continue
        if r["side"] == "long":
            t.at[i, "ambiguous_exit"] = bool(hi[k] >= r["target"] and lo[k] <= r["initial_stop"])
        else:
            t.at[i, "ambiguous_exit"] = bool(lo[k] <= r["target"] and hi[k] >= r["initial_stop"])
    return t


def run_variant(md: MarketData, variant: dict, exe: ExecutionConfig, w: Window) -> dict:
    cls = resolve_strategy(variant["strategy"])
    params = dict(variant.get("params", {}))
    minutes = int(params.get("signal_minutes", cls.signal_minutes))
    sig_all = signal_bars(md, minutes)
    feats_all = cls.build_features(sig_all, **params)          # causal, full history
    sig = _slice_sessions(sig_all, w)
    feats = feats_all.loc[sig.index]
    rth = _slice_sessions(md.rth, w)
    frame = build_execution_frame(rth, sig, feats, md.sessions.loc[w.start:w.end], minutes, exe.flatten_minutes)
    warm_cols = [c for c in ("vwap", "ema") if c in feats.columns]
    if warm_cols and feats.iloc[0][warm_cols].isna().any():
        raise RuntimeError(f"{variant['id']}: indicators not warm at window start {w.start}")
    out = run_backtest(cls, frame, exe, params)
    trades = mark_ambiguous_exits(out.trades, frame)
    em = M.equity_metrics(out.session_equity, exe.cash, out.equity["Equity"])
    tm = M.trade_metrics(trades)
    closed = trades[trades["exit_reason"] != "open_at_end"]
    em["exposure_minutes_frac"] = float(closed["minutes_spanned"].sum() / len(frame)) if len(frame) else 0.0
    return {"trades": trades, "session_equity": out.session_equity, "equity": em, "trade": tm,
            "library_stats": out.library_stats, "warnings": out.warnings,
            "flatten_fallback_sessions": int(frame.groupby("session_code")["flatten_fallback"].max().sum()),
            "minutes": minutes, "frame_rows": len(frame), "params": params,
            "_frame": frame, "_features": feats}


def diff_trades(base: pd.DataFrame, var: pd.DataFrame) -> dict:
    key = lambda d: d["signal_start"].astype(str) + "|" + d["side"]
    b = base.assign(k=key(base)).set_index("k") if len(base) else pd.DataFrame(columns=list(base.columns)).set_index(pd.Index([]))
    v = var.assign(k=key(var)).set_index("k") if len(var) else pd.DataFrame(columns=list(var.columns)).set_index(pd.Index([]))
    removed = b.index.difference(v.index)
    added = v.index.difference(b.index)
    common = b.index.intersection(v.index)
    altered = [k for k in common if (str(b.at[k, "exit_time"]) != str(v.at[k, "exit_time"]))
               or not np.isclose(b.at[k, "exit_price"], v.at[k, "exit_price"])]
    same = len(common) - len(altered)
    return {
        "same": int(same), "altered": len(altered), "added": len(added), "removed": len(removed),
        "pnl_added": float(v.loc[added, "pnl"].sum()) if len(added) else 0.0,
        "pnl_removed_from_baseline": float(b.loc[removed, "pnl"].sum()) if len(removed) else 0.0,
        "pnl_altered_variant": float(v.loc[altered, "pnl"].sum()) if altered else 0.0,
        "pnl_altered_baseline": float(b.loc[altered, "pnl"].sum()) if altered else 0.0,
        "r_added": float(v.loc[added, "r_multiple"].mean()) if len(added) else None,
        "r_removed": float(b.loc[removed, "r_multiple"].mean()) if len(removed) else None,
        "keys": {"added": list(map(str, added)), "removed": list(map(str, removed)),
                 "altered": list(map(str, altered))},
    }


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if (isinstance(x, float) or isinstance(x, np.floating)) and not np.isfinite(x) else float(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, (pd.Timestamp, dt.date)):
        return x.isoformat()
    return x


def run_experiment(config_path: Path, out_root: Path | None = None, market: MarketData | None = None,
                   synthetic_label: str | None = None, ledger: bool = True, now: str | None = None) -> Path:
    cfg, cfg_sha = load_config(config_path)
    exp = cfg["experiment"]
    if not synthetic_label:
        check_frozen(exp, config_path)
    md = market or prepare_market(cfg["data"])
    exe = ExecutionConfig(**cfg.get("execution", {}))
    wcfg = cfg.get("windows", {})
    windows = build_windows(md.coverage, int(cfg["data"].get("warmup_sessions", 5)),
                            int(wcfg.get("recent_months", 6)), bool(wcfg.get("calendar_halves", True)))
    variants = cfg["variants"]
    baseline = next(v["id"] for v in variants if v.get("role") == "baseline")
    run_utc = now or dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{exp['id']}__{run_utc}"
    study = REPO_ROOT / exp["study"]
    out_root = Path(out_root) if out_root else study / "exports" / "runs"
    run_dir = out_root / run_id
    if run_dir.exists():
        raise FileExistsError(f"{run_dir} exists; runs are immutable")
    (run_dir / "trades").mkdir(parents=True)
    (run_dir / "equity").mkdir()

    full = windows[0]
    hurdle = M.expected_max_sharpe(int(exp.get("trials_planned", len(variants))), full.sessions)
    results: dict = {}
    keep: dict = {}
    for v in variants:
        results[v["id"]] = {}
        for w in windows:
            try:
                res = run_variant(md, v, exe, w)
                status = "ok"
            except Exception as e:  # recorded, never hidden
                res, status = None, f"error: {type(e).__name__}: {e}"
            if res is None:
                results[v["id"]][w.id] = {"status": status}
                continue
            stem = f"{v['id']}__{w.id}"
            res["trades"].to_csv(run_dir / "trades" / f"{stem}.csv", index=False)
            res["session_equity"].rename("equity").to_csv(run_dir / "equity" / f"{stem}.csv", index_label="session")
            results[v["id"]][w.id] = {"status": status, "equity": res["equity"], "trade": res["trade"],
                                      "warnings": res["warnings"], "minutes": res["minutes"],
                                      "flatten_fallback_sessions": res["flatten_fallback_sessions"],
                                      "library_stats": res["library_stats"]}
            keep[(v["id"], w.id)] = res
    # Diffs vs baseline (per window)
    for v in variants:
        if v["id"] == baseline or v.get("role") in ("independent", "benchmark"):
            continue  # independent strategies are compared side by side, never diffed as variants
        for w in windows:
            if (v["id"], w.id) in keep and (baseline, w.id) in keep:
                results[v["id"]][w.id]["diff_vs_baseline"] = diff_trades(
                    keep[(baseline, w.id)]["trades"], keep[(v["id"], w.id)]["trades"])

    record = {
        "run_id": run_id, "run_utc": run_utc, "experiment": exp, "config_path": str(Path(config_path)),
        "config_sha256": cfg_sha, "config": cfg, "baseline": baseline,
        "synthetic": synthetic_label, "code": code_identity(), "packages": package_versions(),
        "dataset": md.identity, "execution": exe.to_dict(),
        "windows": [w.to_dict() for w in windows],
        "coverage": {"sessions": int(len(md.coverage)), "early_close_sessions": int(md.coverage.early_close.sum()),
                     "sessions_with_missing_minutes": int((md.coverage.missing > 0).sum()),
                     "missing_minutes_total": int(md.coverage.missing.clip(lower=0).sum()),
                     "first_session": str(md.coverage.index.min().date() if hasattr(md.coverage.index.min(), 'date') else md.coverage.index.min()),
                     "last_session": str(md.coverage.index.max().date() if hasattr(md.coverage.index.max(), 'date') else md.coverage.index.max()),
                     "warmup_sessions": int(cfg["data"].get("warmup_sessions", 5))},
        "trials": {"planned": int(exp.get("trials_planned", len(variants))), "evaluated_in_this_run": sum(1 for v in variants if v.get("role") != "benchmark"),
                   "benchmarks": [v["id"] for v in variants if v.get("role") == "benchmark"],
                   "dsr_threshold_implied": hurdle},
    }
    (run_dir / "run_record.json").write_text(json.dumps(_jsonable(record), indent=2, sort_keys=False))
    (run_dir / "metrics.json").write_text(json.dumps(_jsonable(results), indent=2))
    from .report.build import build_report
    report_status = "ok"
    try:
        build_report(run_dir, md=md, keep=keep)
    except Exception as e:  # the run is still recorded; the failure is visible in the ledger
        report_status = f"report_error: {type(e).__name__}: {e}"
        (run_dir / "REPORT_ERROR.txt").write_text(report_status)
    if ledger and not synthetic_label:
        _append_ledger(study / "LEDGER.csv", record, results, variants, full, report_status)
    if report_status != "ok":
        raise RuntimeError(f"run recorded at {run_dir}, but {report_status}")
    return run_dir


def _append_ledger(path: Path, record: dict, results: dict, variants: list, full: Window,
                   report_status: str = "ok") -> None:
    new = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        if new:
            w.writeheader()
        for v in variants:
            r = results[v["id"]].get(full.id, {})
            em, tm = r.get("equity", {}), r.get("trade", {})
            w.writerow({
                "run_id": record["run_id"], "run_utc": record["run_utc"],
                "experiment_id": record["experiment"]["id"], "variant_id": v["id"],
                "role": v.get("role", "variant"), "strategy": v["strategy"],
                "params_json": json.dumps(v.get("params", {}), sort_keys=True),
                "config_sha256": record["config_sha256"], "code_commit": record["code"]["git_commit"],
                "code_dirty": bool(record["code"]["git_dirty_paths"]),
                "code_tree_sha256": record["code"]["code_tree_sha256"],
                "dataset_id": record["dataset"].get("dataset_id"), "dataset_sha256": record["dataset"].get("sha256"),
                "mask": (record["dataset"].get("mask") or {}).get("id"),
                "window": full.id, "window_start": full.start, "window_end": full.end, "sessions": full.sessions,
                "trials_planned": record["trials"]["planned"],
                "dsr_threshold_implied": f"illustrative independent-trials null: {record['trials']['dsr_threshold_implied']['sr_annualized']:.3f} ann. (N={record['trials']['planned']}, T={full.sessions}); not a significance threshold",
                "trades": tm.get("trades"), "net_pnl": em.get("net_pnl"), "total_return": em.get("total_return"),
                "sharpe_daily_ann": em.get("sharpe_daily_ann"), "max_dd_session_close": em.get("max_dd_session_close"),
                "expectancy_r": tm.get("expectancy_r"), "status": r.get("status", "missing"),
                "notes": ("" if report_status == "ok" else f"[{report_status}] ") + v.get("hypothesis", "")[:200],
            })
