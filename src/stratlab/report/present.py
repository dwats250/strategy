"""Presentation-only re-render of an existing report (no recomputation).

The data payload embedded in a report built by the pinned computation (`build.py` at the
run's code tree, identity-checked when its chart overlays were generated) is decoded,
verified field by field against the run directory's saved files, and rendered with the
current presentation template. Nothing is recomputed: if the payload and the saved files
disagree anywhere, rendering stops.

Two identities are recorded in the output:
  * computation: the run's code identity and the source report's SHA-256 (where the
    payload came from);
  * presentation: the code identity of the tree that rendered the new page.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import html as _html
import json
import re
import subprocess
from pathlib import Path

import pandas as pd

from .build import HERE, _pack, _vendor_assets


class PayloadMismatch(RuntimeError):
    pass


def extract_payload(report_path: Path) -> dict:
    html = Path(report_path).read_text()
    m = re.search(r'<script id="payload" type="application/octet-stream">([A-Za-z0-9+/=\s]+)</script>', html)
    if not m:
        raise PayloadMismatch(f"{report_path}: no embedded payload found")
    return json.loads(gzip.decompress(base64.b64decode(m.group(1).strip())))


# Every module whose code shapes the payload. A regenerated payload counts as "the pinned
# original computation" only if each of these is byte-identical to the run's commit.
PINNED_MODULES = [
    "src/stratlab/report/build.py", "src/stratlab/metrics.py", "src/stratlab/indicators.py",
    "src/stratlab/strategies/common.py", "src/stratlab/strategies/vwap_reclaim.py",
    "src/stratlab/strategies/instagram_austin_vwap_ema9.py", "src/stratlab/strategies/benchmarks.py",
    "src/stratlab/data/sessions.py", "src/stratlab/data/store.py", "src/stratlab/experiment.py",
    "src/stratlab/windows.py", "src/stratlab/engine.py",
]


def _git(*args) -> str:
    from .build import HERE as _H
    root = _H.parents[2]
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def check_pinned_modules(commit: str) -> list[dict]:
    """Refuse unless every payload-shaping module equals its blob at the run's commit."""
    out, bad = [], []
    for path in PINNED_MODULES:
        try:
            pinned = _git("rev-parse", f"{commit}:{path}")
        except subprocess.CalledProcessError:
            bad.append(f"{path}: not in commit {commit[:12]}")
            continue
        now = _git("hash-object", path)
        (out if now == pinned else bad).append({"path": path, "blob": now} if now == pinned else f"{path}: {now[:12]} != {pinned[:12]}")
    if bad:
        raise PayloadMismatch("computation modules differ from the run's commit; cannot regenerate under the "
                              "pinned computation:\n  " + "\n  ".join(bad))
    return out


def check_source_tracked(path: Path) -> dict:
    """The source report must be committed and unmodified (its bytes equal the HEAD blob)."""
    from .build import HERE as _H
    try:
        rel = Path(path).resolve().relative_to(_H.parents[2])
    except ValueError:
        raise PayloadMismatch(f"{path} is outside the repository, so it is not committed; refusing it") from None
    try:
        head = _git("rev-parse", f"HEAD:{rel}")
    except subprocess.CalledProcessError:
        raise PayloadMismatch(f"{rel} is not committed; refusing an untracked source report") from None
    now = _git("hash-object", str(rel))
    if now != head:
        raise PayloadMismatch(f"{rel} differs from its committed version; refusing a modified source report")
    return {"path": str(rel), "git_blob": head, "added_in_commit": _git("log", "-1", "--format=%H", "--", str(rel))}


def _pinned_keep(record: dict):
    """Market data and full-window features, via the same pinned calls as build._keep_from_record.
    (That function's whole-tree identity check is replaced, not skipped, by check_pinned_modules.)"""
    from ..experiment import prepare_market, resolve_strategy, signal_bars
    cfg = record["config"]
    md = prepare_market(cfg["data"])
    if md.identity.get("sha256") != record["dataset"].get("sha256"):
        raise PayloadMismatch("dataset identity differs from the run record")
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


def _leaves(o) -> int:
    if isinstance(o, dict):
        return sum(_leaves(v) for v in o.values())
    if isinstance(o, list):
        return sum(_leaves(v) for v in o)
    return 1


def _first_diff(a, b, path="") -> str:
    if type(a) is not type(b):
        return f"{path}: {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}.{k}: missing on one side"
            if a[k] != b[k]:
                return _first_diff(a[k], b[k], f"{path}.{k}")
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return _first_diff(x, y, f"{path}[{i}]")
    return f"{path}: {a!r} vs {b!r}"


def verify_payload(payload: dict, run_dir: Path, regenerate_bars: bool = True) -> dict:
    """Regenerate the expected payload with the pinned build_report and compare everything
    the page can display. Only `findings` is excluded (supplied separately from the findings
    note); `bars`/`bar_map` are excluded only when regenerate_bars=False (synthetic runs,
    whose generated prices are not stored), and that is recorded."""
    import shutil
    import tempfile
    from .build import build_report
    run_dir = Path(run_dir)
    rec = json.loads((run_dir / "run_record.json").read_text())
    cfg_path = Path(rec["config_path"])
    if not cfg_path.exists() or hashlib.sha256(cfg_path.read_bytes()).hexdigest() != rec["config_sha256"]:
        raise PayloadMismatch(f"experiment config {cfg_path} is missing or differs from config_sha256")
    modules = check_pinned_modules(rec["code"]["git_commit"])
    md = keep = None
    if regenerate_bars:
        md, keep = _pinned_keep(rec)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / run_dir.name
        tmp.mkdir()
        for name in ("run_record.json", "metrics.json"):
            shutil.copy2(run_dir / name, tmp / name)
        for sub in ("trades", "equity"):
            shutil.copytree(run_dir / sub, tmp / sub)
        expected = extract_payload(build_report(tmp, md=md, keep=keep, out_name="expected.html"))
    keys = [k for k in expected if k != "findings" and (regenerate_bars or k not in ("bars", "bar_map"))]
    bad = [k for k in keys if expected[k] != payload.get(k)]
    extra = sorted(set(payload) - set(expected) - {"presentation"})
    if bad or extra:
        detail = [_first_diff(payload.get(k), expected[k], k) for k in bad] + [f"unexpected key {k}" for k in extra]
        raise PayloadMismatch("payload does not match the pinned regeneration:\n  " + "\n  ".join(detail[:20]))
    return {"method": "regenerated with pinned build_report; full structural equality",
            "sections_compared": keys, "values_compared": sum(_leaves(expected[k]) for k in keys),
            "mismatches": 0, "bars_regenerated": regenerate_bars, "pinned_modules": modules,
            "pinned_commit": rec["code"]["git_commit"]}


def _related(run_dirs: list[Path]) -> list[dict]:
    out = []
    for d in run_dirs:
        rec = json.loads((Path(d) / "run_record.json").read_text())
        met = json.loads((Path(d) / "metrics.json").read_text())
        full = rec["windows"][0]["id"]
        for v in rec["config"]["variants"]:
            r = met[v["id"]][full]
            out.append({"run_id": rec["run_id"], "code_tree_sha256": rec["code"]["code_tree_sha256"],
                        "config_sha256": rec["config_sha256"], "dataset_sha256": rec["dataset"]["sha256"],
                        "mask": (rec["dataset"].get("mask") or {}).get("id"), "id": v["id"], "label": v.get("label", v["id"]),
                        "difference": v.get("difference", ""),
                        "total_return": r["equity"]["total_return"], "max_dd": r["equity"]["max_dd_session_close"],
                        "trades": r["trade"]["trades"], "expectancy_r": r["trade"].get("expectancy_r")})
    return out


def build_presentation(run_dir: Path, source_report: Path, out_name: str, presentation: dict,
                       related_runs: list[Path] | None = None, findings: list[str] | None = None,
                       findings_source: Path | None = None, require_tracked_source: bool = True,
                       regenerate_bars: bool = True) -> Path:
    from ..experiment import code_identity
    run_dir, source_report = Path(run_dir), Path(source_report)
    out = run_dir / out_name
    if out.exists():
        raise FileExistsError(f"{out} exists; reports are never overwritten")
    source_meta = check_source_tracked(source_report) if require_tracked_source else {"path": str(source_report), "tracked": False}
    payload = extract_payload(source_report)
    check = verify_payload(payload, run_dir, regenerate_bars=regenerate_bars)
    if findings is not None:
        payload["findings"] = findings
    ident = code_identity()
    payload["presentation"] = {
        **presentation,
        "related": _related(related_runs or []),
        "provenance": {
            "payload_source": {**source_meta, "sha256": hashlib.sha256(source_report.read_bytes()).hexdigest()},
            "payload_computed_under_code_tree": payload["record"]["code"]["code_tree_sha256"],
            "verification": check,
            "findings_source": ({"path": str(findings_source), "sha256": hashlib.sha256(Path(findings_source).read_bytes()).hexdigest()}
                                if findings_source else "as embedded in the source report"),
            "presentation_code": ident,
            "template": "template_v2.html",
        },
    }
    plotly_js, dt_js, dt_css = _vendor_assets()
    tpl = (HERE / "template_v2.html").read_text()
    title = presentation.get("title_short") or payload["record"]["experiment"].get("title", payload["record"]["experiment"]["id"])
    html = (tpl.replace("/*__DT_CSS__*/", dt_css)
               .replace("__TITLE__", _html.escape(title))
               .replace("/*__PLOTLY__*/", plotly_js)
               .replace("/*__DT_JS__*/", dt_js)
               .replace("/*__DATA__*/", _pack(payload)))
    out.write_text(html)
    return out
