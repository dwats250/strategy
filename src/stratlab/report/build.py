"""Build the self-contained interactive HTML report for one run directory.

Everything the page needs is inlined: Plotly (from the pinned `plotly` package),
DataTables (from the pinned `itables` offline bundle), and the run's data. The page
opens from a file:// path with no server and no network.

Statistics are computed in Python and embedded. In the browser, window buttons switch
between precomputed backtests (each a separate run started with fresh capital); zoom,
date filters and table searches only change the VIEW and never recompute statistics.
"""

from __future__ import annotations

import html as _html
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from ..data.sessions import ET

HERE = Path(__file__).resolve().parent

PALETTE_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
PALETTE_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]


def _vendor_assets() -> tuple[str, str, str]:
    import itables
    import plotly.offline
    plotly_js = plotly.offline.get_plotlyjs()
    base = Path(itables.__file__).resolve().parent / "html"
    dt_js = (base / "dt_bundle.js").read_text()
    dt_css = (base / "dt_bundle.css").read_text()
    found = list(re.finditer(r"export\{([^}]*)\};?", dt_js))
    if len(found) != 1:
        raise RuntimeError(f"unexpected itables bundle format ({len(found)} export clauses)")
    m = found[0]
    pairs = [p.strip().split(" as ") for p in m.group(1).split(",")]
    assign = ",".join(f"{(p[1] if len(p) > 1 else p[0])}:{p[0]}" for p in pairs)
    dt_js = (dt_js[: m.start()] + f"window.__DT={{{assign}}};window.dispatchEvent(new Event('dt-ready'));"
             + dt_js[m.end():])
    # A literal U+FFFD inside a vendored regex is rewritten as its JS escape (same meaning),
    # so the page survives tools that treat U+FFFD as a lost-character marker.
    plotly_js = plotly_js.replace("�", "\\ufffd")
    dt_js = dt_js.replace("�", "\\ufffd")
    if "</script" in dt_js.lower() or "</script" in plotly_js.lower():
        raise RuntimeError("vendored script contains a closing script tag")
    return plotly_js, dt_js, dt_css


def _f(x, nd=6):
    if x is None:
        return None
    try:
        if isinstance(x, (float, np.floating)) and not np.isfinite(x):
            return None
    except TypeError:
        pass
    if isinstance(x, (float, np.floating)):
        return round(float(x), nd)
    if isinstance(x, np.integer):
        return int(x)
    return x


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return _f(o)


def _et(ts) -> str | None:
    if ts is None or (isinstance(ts, float) and np.isnan(ts)) or pd.isna(ts):
        return None
    return pd.Timestamp(ts).tz_convert(ET).strftime("%Y-%m-%d %H:%M")


def _bars_payload(md, keep, variants, full_id) -> tuple[dict, dict]:
    """Per feature-set, per session: signal-timeframe OHLC + VWAP + EMA for the chart."""
    fsets, vmap = {}, {}
    for v in variants:
        res = keep.get((v["id"], full_id))
        if res is None or not {"vwap", "ema"} <= set(res["_features"].columns):
            continue  # e.g. the session-hold benchmark has no indicator overlay
        from ..experiment import resolve_strategy
        cls = resolve_strategy(v["strategy"])
        p = {k: res["params"].get(k, getattr(cls, k, None)) for k in ("vwap_source", "ema_length")}
        key = f"{res['minutes']}m|{p['vwap_source']}|{p['ema_length']}"
        vmap[v["id"]] = key
        if key in fsets:
            continue
        feats = res["_features"]
        sig = md.signal_bars[res["minutes"]].loc[feats.index]
        et_idx = feats.index.tz_convert(ET)
        days = {}
        for sess, idx in pd.Series(np.arange(len(feats)), index=sig["session"].astype(str).to_numpy()).groupby(level=0):
            ii = idx.to_numpy()
            days[sess] = {
                "t": [x.strftime("%H:%M") for x in et_idx[ii]],
                "o": np.round(sig["Open"].to_numpy()[ii], 2).tolist(),
                "h": np.round(sig["High"].to_numpy()[ii], 2).tolist(),
                "l": np.round(sig["Low"].to_numpy()[ii], 2).tolist(),
                "c": np.round(sig["Close"].to_numpy()[ii], 2).tolist(),
                "vwap": [None if np.isnan(x) else round(float(x), 2) for x in feats["vwap"].to_numpy()[ii]],
                "ema": [None if np.isnan(x) else round(float(x), 2) for x in feats["ema"].to_numpy()[ii]],
            }
        fsets[key] = {"minutes": res["minutes"], "vwap_source": p.get("vwap_source"),
                      "ema_length": p.get("ema_length"), "days": days}
    return fsets, vmap


def _pack(payload: dict) -> str:
    """Deterministic gzip+base64 of the JSON payload (mtime=0)."""
    import base64
    import gzip
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return base64.b64encode(gzip.compress(raw, compresslevel=9, mtime=0)).decode()


def _slim(res: dict) -> dict:
    """Drop bulky fields the page never renders (diff key lists, library stats)."""
    out = {}
    for w, r in res.items():
        r = dict(r)
        r.pop("library_stats", None)
        if "diff_vs_baseline" in r:
            r["diff_vs_baseline"] = {k: v for k, v in r["diff_vs_baseline"].items() if k != "keys"}
        out[w] = r
    return out


def _keep_from_record(record: dict):
    """Recompute (without backtesting) what the price charts need: market data and each
    variant's full-window features. Used when rebuilding a report from a run directory."""
    from ..experiment import prepare_market, resolve_strategy, signal_bars
    cfg = record["config"]
    md = prepare_market(cfg["data"])
    if md.identity.get("sha256") != record["dataset"].get("sha256"):
        raise RuntimeError("dataset identity differs from the run record; refusing to rebuild charts")
    w = record["windows"][0]
    keep = {}
    for v in cfg["variants"]:
        cls = resolve_strategy(v["strategy"])
        params = dict(v.get("params", {}))
        minutes = int(params.get("signal_minutes", cls.signal_minutes))
        sig = signal_bars(md, minutes)
        s = pd.to_datetime(sig["session"])
        sig = sig[(s >= pd.Timestamp(w["start"])) & (s <= pd.Timestamp(w["end"]))]
        feats = cls.build_features(signal_bars(md, minutes), **params).loc[sig.index]
        keep[(v["id"], w["id"])] = {"params": params, "minutes": minutes, "_features": feats}
    return md, keep


def build_report(run_dir: Path, md=None, keep=None, out_name: str = "report.html",
                 findings: list[str] | None = None, rebuild_charts: bool = False) -> Path:
    run_dir = Path(run_dir)
    record = json.loads((run_dir / "run_record.json").read_text())
    results = json.loads((run_dir / "metrics.json").read_text())
    cfg = record["config"]
    variants = cfg["variants"]
    windows = record["windows"]
    full_id = windows[0]["id"]

    vdata = []
    slot = 0
    for v in variants:
        if v.get("role") == "benchmark":
            c_light = c_dark = "#898781"          # neutral, never a categorical slot
        else:
            c_light, c_dark = PALETTE_LIGHT[slot % 8], PALETTE_DARK[slot % 8]
            slot += 1
        series = {}
        for w in windows:
            p = run_dir / "equity" / f"{v['id']}__{w['id']}.csv"
            if p.exists():
                e = pd.read_csv(p)
                series[w["id"]] = {"d": e["session"].astype(str).tolist(),
                                   "eq": np.round(e["equity"].to_numpy(), 2).tolist()}
        trades = []
        tp = run_dir / "trades" / f"{v['id']}__{full_id}.csv"
        if tp.exists():
            t = pd.read_csv(tp, parse_dates=["entry_time", "exit_time"])
            for _, r in t.iterrows():
                trades.append(_clean({
                    "id": int(r.trade_id), "session": _et(r.entry_time)[:10], "side": r.side,
                    "entry": _et(r.entry_time), "exit": _et(r.exit_time),
                    "entry_px": r.entry_price, "exit_px": r.exit_price, "stop": r.initial_stop,
                    "target": r.target if pd.notna(r.target) else None, "size": int(r["size"]),
                    "pnl": round(float(r.pnl), 2), "r": r.r_multiple, "reason": r.exit_reason,
                    "mins": int(r.minutes_spanned), "sig": str(r.signal_start),
                    "amb": bool(r.get("ambiguous_exit", False)),
                    "riskp": r.get("initial_risk_pct_equity"), "rr": r.get("initial_reward_risk"),
                }))
        monthly = {}
        ep = run_dir / "equity" / f"{v['id']}__{full_id}.csv"
        if ep.exists():
            from ..metrics import monthly_returns, rolling_sharpe
            e = pd.read_csv(ep, index_col=0)["equity"]
            mr = monthly_returns(e, record["execution"]["cash"])
            monthly = {str(k): _f(x) for k, x in mr.items()}
            rs = rolling_sharpe(e, record["execution"]["cash"])
            rolling = {"d": [str(x) for x in rs.index], "v": [_f(x, 3) for x in rs.to_numpy()]}
        else:
            rolling = {"d": [], "v": []}
        vdata.append({
            "id": v["id"], "role": v.get("role", "variant"), "label": v.get("label", v["id"]),
            "strategy": v["strategy"], "params": v.get("params", {}),
            "hypothesis": v.get("hypothesis", ""), "difference": v.get("difference", ""),
            "mechanism": v.get("mechanism", ""), "primary_metric": v.get("primary_metric", ""),
            "uninformative_if": v.get("uninformative_if", ""),
            "color_light": c_light, "color_dark": c_dark,
            "series": series, "trades": trades, "monthly": monthly, "rolling": rolling,
            "results": _slim(results.get(v["id"], {})),
        })

    bars, vmap = ({}, {})
    if (md is None or keep is None) and rebuild_charts:
        md, keep = _keep_from_record(record)
    if md is not None and keep is not None:
        bars, vmap = _bars_payload(md, keep, variants, full_id)

    payload = _clean({
        "record": {k: record[k] for k in ("run_id", "run_utc", "experiment", "config_sha256", "baseline",
                                          "synthetic", "code", "packages", "dataset", "execution",
                                          "windows", "coverage", "trials")},
        "limitations": cfg.get("limitations", []),
        "findings": findings if findings is not None else cfg.get("findings", []),
        "variants": vdata, "bars": bars, "bar_map": vmap,
        "config_toml": Path(record["config_path"]).read_text() if Path(record["config_path"]).exists() else "",
    })
    plotly_js, dt_js, dt_css = _vendor_assets()
    tpl = (HERE / "template.html").read_text()
    title = record["experiment"].get("title", record["experiment"]["id"])
    html = (tpl.replace("/*__DT_CSS__*/", dt_css)
               .replace("__TITLE__", _html.escape(("SYNTHETIC · " if record.get("synthetic") else "") + title))
               .replace("/*__PLOTLY__*/", plotly_js)
               .replace("/*__DT_JS__*/", dt_js)
               .replace("/*__DATA__*/", _pack(payload)))
    out = run_dir / out_name
    if out.exists():
        raise FileExistsError(f"{out} exists; run directories are immutable (write a new name)")
    out.write_text(html)
    return out
