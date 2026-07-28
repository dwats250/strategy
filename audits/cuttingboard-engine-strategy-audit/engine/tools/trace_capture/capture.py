#!/usr/bin/env python3
"""EA-6 decision-trace capture — a Strategy-owned wrapper that OBSERVES the engine.

It never imports, patches, or instruments pinned CuttingBoard source. It runs the
pinned engine under the EA-2 seam and maps the artifacts the engine itself wrote
into the EA-6 trace schema (see ../../trace/SCHEMA_v1.md).

Any schema field the engine does not expose is emitted as the literal string
NOT_OBSERVABLE. No value is ever inferred, reconstructed, or synthesised.

Usage:
    python3 capture.py --src <extracted-pin> --fixture <quotes.json> \\
                       --run-dir <writable-dir> --case-id <id> \\
                       [--cache <ohlcv-parquet-dir>] --out <trace.json>

The caller is responsible for establishing isolation (bwrap --unshare-net,
read-only root, single writable bind). This tool records, but does not enforce,
that boundary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

WRAPPER_VERSION = "EA-6-capture/1.0.0"
SCHEMA_VERSION = "EA-6-trace/v1"
NOT_OBSERVABLE = "NOT_OBSERVABLE"

# Per-gate status vocabulary required by the plan (§8).
GATE_STATUS = ("PASS", "FAIL", "UNKNOWN", "NOT_EVALUATED", "INERT")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_pipeline_records(p: Path) -> list:
    """audit.jsonl carries two record families; the doctrine's canonical filter
    excludes notification events."""
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if rec.get("event") != "notification":
            out.append(rec)
    return out


def run_engine(src: Path, fixture: Path, run_dir: Path, cache: Path | None) -> int:
    for sub in ("logs", "reports/output", "data/cache"):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    if cache is not None:
        for f in cache.glob("*.parquet"):
            (run_dir / "data" / "cache" / f.name).write_bytes(f.read_bytes())
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(run_dir),
        "LANG": "C.UTF-8",
        "PYTHONPATH": f"{src}:{os.environ.get('EA6_SITE_PACKAGES', '')}",
        "PYTHONDONTWRITEBYTECODE": "1",
        "FIXTURE_MODE": "1",
    }
    proc = subprocess.run(
        [sys.executable, "-m", "cuttingboard", "--mode", "fixture",
         "--fixture-file", str(fixture)],
        cwd=str(run_dir), env=env, capture_output=True, text=True,
    )
    (run_dir / "stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
    return proc.returncode


def build_trace(*, case_id: str, src: Path, fixture: Path, run_dir: Path,
                exit_code: int, snapshot_sha: str, env_lock_sha: str) -> dict:
    logs = run_dir / "logs"
    contract = load_json(logs / "latest_contract.json") or {}
    summary = load_json(logs / "latest_run.json") or {}
    records = load_pipeline_records(logs / "audit.jsonl")
    record = records[0] if records else {}
    fixture_quotes = load_json(fixture) or {}
    config_path = src / "config.toml"

    # ---------------- identities (canonical) ----------------
    identities = {
        "snapshot_sha": snapshot_sha,
        "config_sha256": sha256_file(config_path) if config_path.exists() else NOT_OBSERVABLE,
        "environment_lock_sha256": env_lock_sha,
        "wrapper_version": WRAPPER_VERSION,
        "schema_version": SCHEMA_VERSION,
        "fixture_sha256": sha256_file(fixture),
    }

    # ---------------- temporal ----------------
    temporal = {
        "run_at_utc": summary.get("run_at_utc", contract.get("generated_at", NOT_OBSERVABLE)),
        "generation_id": summary.get("generation_id", contract.get("generation_id", NOT_OBSERVABLE)),
        "session_date": contract.get("session_date", NOT_OBSERVABLE),
        # The engine derives run_at_utc from max(fetched_at_utc); it publishes no
        # separate as-of boundary field.
        "as_of_boundary": NOT_OBSERVABLE,
        "as_of_boundary_note": "engine exposes no distinct as-of field; run_at_utc is fixture-derived",
    }

    # ---------------- input provenance & missing-data mask ----------------
    inputs = []
    for sym, q in sorted(fixture_quotes.items()):
        inputs.append({
            "symbol": sym,
            "price": q.get("price"),
            "pct_change_decimal": q.get("pct_change_decimal"),
            "volume": q.get("volume"),
            "fetched_at_utc": q.get("fetched_at_utc"),
            "source": q.get("source"),
            "units": q.get("units"),
            "age_seconds": q.get("age_seconds"),
        })
    excluded = record.get("excluded_symbols", NOT_OBSERVABLE)
    missing_mask = {
        "fixture_symbols": sorted(fixture_quotes.keys()),
        "excluded_symbols": excluded if excluded != NOT_OBSERVABLE else NOT_OBSERVABLE,
        "data_status": summary.get("data_status", NOT_OBSERVABLE),
    }

    # ---------------- regime / intermediate state ----------------
    intermediate = {
        "regime": summary.get("regime", record.get("regime", NOT_OBSERVABLE)),
        "posture": summary.get("posture", record.get("posture", NOT_OBSERVABLE)),
        "confidence": summary.get("confidence", record.get("confidence", NOT_OBSERVABLE)),
        "router_mode": summary.get("router_mode", NOT_OBSERVABLE),
        "energy_score": summary.get("energy_score", NOT_OBSERVABLE),
        "index_score": summary.get("index_score", NOT_OBSERVABLE),
        "kill_switch": summary.get("kill_switch", NOT_OBSERVABLE),
        "system_halted": summary.get("system_halted", NOT_OBSERVABLE),
        # EA-5 finding EA5-002: the per-candidate gate vector is computed in
        # QualificationResult and discarded at the audit boundary.
        "regime_vote_detail": NOT_OBSERVABLE,
        "structure_labels": NOT_OBSERVABLE,
    }

    # ---------------- per-candidate opportunities ----------------
    opportunities = []
    for cand in contract.get("trade_candidates", []) or []:
        opportunities.append({
            "symbol": cand.get("symbol", cand.get("ticker", NOT_OBSERVABLE)),
            "disposition": "EVALUATED_CANDIDATE",
            "decision_status": cand.get("decision_status", NOT_OBSERVABLE),
            "block_reason": cand.get("block_reason", NOT_OBSERVABLE),
            "decision_trace": cand.get("decision_trace", NOT_OBSERVABLE),
            "entry_mode": cand.get("entry_mode", NOT_OBSERVABLE),
            "geometry": {
                "entry": cand.get("entry_price", NOT_OBSERVABLE),
                "stop": cand.get("stop_price", NOT_OBSERVABLE),
                "target": cand.get("target_price", NOT_OBSERVABLE),
                "size": cand.get("max_contracts", NOT_OBSERVABLE),
                "dollar_risk": cand.get("dollar_risk", NOT_OBSERVABLE),
            },
            "explanation": cand.get("explanation", NOT_OBSERVABLE),
            # Required per-gate vector — EA5-002.
            "gate_results": NOT_OBSERVABLE,
            "gate_results_note": "gates_passed/gates_failed computed in QualificationResult; not persisted (EA5-002)",
        })
    for rej in contract.get("rejections", []) or []:
        opportunities.append({
            "symbol": rej.get("symbol", NOT_OBSERVABLE),
            "disposition": "REJECTED",
            "stage": rej.get("stage", NOT_OBSERVABLE),
            "reason": rej.get("reason", NOT_OBSERVABLE),
            "detail": rej.get("detail", NOT_OBSERVABLE),
            "gate_results": NOT_OBSERVABLE,
            "gate_results_note": "single reason string only; per-gate vector not persisted (EA5-002)",
        })

    # ---------------- terminal decision ----------------
    terminal = {
        "outcome": summary.get("outcome", contract.get("outcome", NOT_OBSERVABLE)),
        "contract_status": contract.get("status", NOT_OBSERVABLE),
        "summary_status": summary.get("status", NOT_OBSERVABLE),
        "halt_reason": summary.get("halt_reason", NOT_OBSERVABLE),
        "system_state": contract.get("system_state", NOT_OBSERVABLE),
        # Engine emits prose reasons; there is no machine-readable reason-code enum.
        "machine_reason_codes": NOT_OBSERVABLE,
        "machine_reason_codes_note": "engine emits prose reason strings; no stable code enum exists",
        "process_exit_code": exit_code,
    }

    # ---------------- precedence / ordering events ----------------
    ordering = {
        "regime_short_circuited": record.get("regime_short_circuited", NOT_OBSERVABLE),
        "regime_failure_reason": record.get("regime_failure_reason", NOT_OBSERVABLE),
        "continuation_rejection_counters": record.get("continuation_audit", NOT_OBSERVABLE),
        "gate_order_events": NOT_OBSERVABLE,
        "gate_order_events_note": "engine records no per-gate ordering/override event stream",
    }

    canonical = {
        "case_id": case_id,
        "identities": identities,
        "temporal": temporal,
        "inputs": inputs,
        "missing_data_mask": missing_mask,
        "intermediate_state": intermediate,
        "opportunities": opportunities,
        "ordering_and_precedence": ordering,
        "terminal": terminal,
        # Attached later by a separate, separately-versioned phase.
        "realized_outcomes": NOT_OBSERVABLE,
    }

    envelope = {
        "run_dir_basename": run_dir.name,
        "pipeline_record_count": len(records),
        "artifacts_present": sorted(
            str(p.relative_to(run_dir)) for p in run_dir.rglob("*") if p.is_file()
        ),
    }

    return {
        "canonical_decision_payload": canonical,
        "run_metadata_envelope": envelope,
        "envelope_excluded_from_equality": sorted(envelope.keys()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--fixture", required=True, type=Path)
    ap.add_argument("--run-dir", required=True, type=Path)
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--cache", type=Path, default=None)
    ap.add_argument("--snapshot-sha", required=True)
    ap.add_argument("--env-lock-sha", default=NOT_OBSERVABLE)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()

    rc = run_engine(a.src, a.fixture, a.run_dir, a.cache)
    trace = build_trace(
        case_id=a.case_id, src=a.src, fixture=a.fixture, run_dir=a.run_dir,
        exit_code=rc, snapshot_sha=a.snapshot_sha, env_lock_sha=a.env_lock_sha,
    )
    a.out.parent.mkdir(parents=True, exist_ok=True)
    # Canonical serialization: sorted keys, fixed encoding, newline-terminated.
    a.out.write_text(
        json.dumps(trace, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    payload = json.dumps(trace["canonical_decision_payload"], sort_keys=True,
                         ensure_ascii=False, separators=(",", ":"))
    print(f"{a.case_id}  exit={rc}  "
          f"outcome={trace['canonical_decision_payload']['terminal']['outcome']}  "
          f"payload_sha256={sha256_text(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
