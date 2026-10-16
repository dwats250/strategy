"""Command line entry point.

  stratlab run <experiment.toml> [--out DIR] [--no-ledger]   real-data experiment -> run dir + report
  stratlab report <run_dir>                                  rebuild report.html from saved files*
  stratlab demo [--out DIR]                                  synthetic end-to-end demo (labelled)
  stratlab data verify <dataset_id>                          SHA-256 check of the local copy
  stratlab data validate <dataset_id> [--mask ID]            coverage / integrity summary (JSON)

* `report` writes report_rebuild_<UTC>.html and re-embeds price charts when the recorded
  dataset is available locally and the code tree matches the run; otherwise it omits them.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from .data.store import REPO_ROOT


def _demo(out: Path | None) -> Path:
    from .experiment import prepare_market, run_experiment
    from .synthetic import SYNTHETIC_LABEL, random_walk_bars
    bars = random_walk_bars("2025-01-02", "2025-09-30", seed=11, s0=580.0)
    md = prepare_market({}, bars_1m=bars, identity={"dataset_id": "synthetic-randomwalk-seed11",
                                                    "sha256": "n/a (generated in-process)", "mask": None})
    cfg = REPO_ROOT / "experiments" / "demo_synthetic.toml"
    out = out or REPO_ROOT / "local_runs"
    return run_experiment(cfg, out_root=out, market=md, synthetic_label=SYNTHETIC_LABEL, ledger=False)


def _findings_from_md(path: Path) -> list[str]:
    """Bullets ('- ...', continuation lines joined) under the first '## Findings' heading."""
    out, on = [], False
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            on = line.strip().lower().startswith("## findings")
            continue
        if not on:
            continue
        m = re.match(r"^(?:[-*]|\d+[.)])\s+(.*)$", line)
        if m:
            out.append(m.group(1).strip())
        elif line.startswith((" ", "\t")) and out and line.strip():
            sub = re.match(r"^\s+(?:[-*]|\d+[.)])\s+(.*)$", line)
            out[-1] += ("; " + sub.group(1).strip()) if sub else (" " + line.strip())
    if not out:
        print(f"warning: no '## Findings' bullets found in {path}", file=sys.stderr)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="stratlab")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("config"); r.add_argument("--out"); r.add_argument("--no-ledger", action="store_true")
    rp = sub.add_parser("report"); rp.add_argument("run_dir")
    rp.add_argument("--findings", help="markdown file; its '- ' bullets under a '## Findings' heading are embedded")
    d = sub.add_parser("demo"); d.add_argument("--out")
    sub.add_parser("identity", help="print the code identity a FROZEN config must pin")
    dd = sub.add_parser("data"); dsub = dd.add_subparsers(dest="dcmd", required=True)
    v = dsub.add_parser("verify"); v.add_argument("dataset_id")
    va = dsub.add_parser("validate"); va.add_argument("dataset_id"); va.add_argument("--mask")
    a = ap.parse_args(argv)

    if a.cmd == "run":
        from .experiment import run_experiment
        p = run_experiment(Path(a.config), out_root=Path(a.out) if a.out else None, ledger=not a.no_ledger)
        print(p / "report.html")
    elif a.cmd == "report":
        import datetime as _dt
        from .report.build import build_report
        stamp = _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")
        findings = _findings_from_md(Path(a.findings)) if a.findings else None
        print(build_report(Path(a.run_dir), out_name=f"report_rebuild_{stamp}.html",
                           findings=findings, rebuild_charts=True))
    elif a.cmd == "demo":
        print(_demo(Path(a.out) if a.out else None) / "report.html")
    elif a.cmd == "identity":
        from .experiment import code_identity
        print(json.dumps(code_identity(), indent=2))
    elif a.cmd == "data":
        from .data.store import resolve
        if a.dcmd == "verify":
            rec, path = resolve(a.dataset_id)
            print(json.dumps({"dataset_id": rec.id, "sha256": rec.sha256, "path": str(path), "verified": True}))
        else:
            from .data.validate import validate_dataset
            print(json.dumps(validate_dataset(a.dataset_id, a.mask), indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
