#!/usr/bin/env python3
"""EA-7 deterministic replay harness.

Hardens the EA-2 seam into a repeatable replay: regenerate inputs from the
deterministic library, run the pinned engine under enforced isolation, capture a
trace with the EA-6 wrapper, and compare the CANONICAL DECISION PAYLOAD against a
recorded manifest hash.

What it proves and what it does not:

  * LOGIC PARITY  — same inputs through the same pinned code path produce the
    same canonical decision payload. This harness tests exactly that.
  * DATA-PROVIDER PARITY — whether reconstructed inputs match what a live
    CuttingBoard run saw. This harness CANNOT test that: it has no live
    CuttingBoard output to compare against, and acquiring one would require live
    market data, which is forbidden. Reported as unavailable, never estimated.

The run-metadata envelope is excluded from every comparison, by enumeration.

Usage:
    python3 replay.py --src <pin> --base <base-fixture> --work <scratch> \\
                      --case <case-id> [--expect <payload-sha256>] \\
                      --snapshot-sha <sha> [--env-lock-sha <sha>] [--passes N]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HARNESS_VERSION = "EA-7-replay/1.0.0"
HERE = Path(__file__).resolve().parent
ENGINE_DIR = HERE.parent.parent                      # .../engine
BUILD_INPUTS = ENGINE_DIR / "fixtures" / "build_inputs.py"
CAPTURE = ENGINE_DIR / "tools" / "trace_capture" / "capture.py"

# Cases that do not need an OHLCV cache: they halt before derived metrics run.
NO_CACHE_CASES = {"halted-killswitch", "halted-validation"}


def canonical_payload_sha256(trace_path: Path) -> str:
    """Hash the canonical decision payload only. The envelope never participates."""
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    payload = trace["canonical_decision_payload"]
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def envelope_keys(trace_path: Path) -> list[str]:
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    return sorted(trace.get("envelope_excluded_from_equality", []))


def one_pass(*, src: Path, base: Path, work: Path, case: str, pass_no: int,
             snapshot_sha: str, env_lock_sha: str) -> tuple[str, Path]:
    """Regenerate inputs from scratch, run the engine, capture, hash."""
    root = work / f"{case}-p{pass_no}"
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)
    (root / "fx").mkdir(parents=True)
    (root / "cache").mkdir(parents=True)

    subprocess.run(
        [sys.executable, str(BUILD_INPUTS), "--base", str(base),
         "--out-fixtures", str(root / "fx"), "--out-cache", str(root / "cache")],
        check=True, capture_output=True, text=True,
    )

    run_dir = root / "run"
    run_dir.mkdir()
    out = root / "trace.json"
    cmd = [
        sys.executable, str(CAPTURE),
        "--src", str(src),
        "--fixture", str(root / "fx" / f"fixture-{case}.json"),
        "--run-dir", str(run_dir),
        "--case-id", case,
        "--snapshot-sha", snapshot_sha,
        "--env-lock-sha", env_lock_sha,
        "--out", str(out),
    ]
    if case not in NO_CACHE_CASES:
        cmd += ["--cache", str(root / "cache")]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return canonical_payload_sha256(out), out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--base", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--case", required=True)
    ap.add_argument("--expect", default=None)
    ap.add_argument("--snapshot-sha", required=True)
    ap.add_argument("--env-lock-sha", default="NOT_OBSERVABLE")
    ap.add_argument("--passes", type=int, default=2)
    a = ap.parse_args()

    hashes: list[str] = []
    trace_path: Path | None = None
    for i in range(1, a.passes + 1):
        h, p = one_pass(src=a.src, base=a.base, work=a.work, case=a.case,
                        pass_no=i, snapshot_sha=a.snapshot_sha,
                        env_lock_sha=a.env_lock_sha)
        hashes.append(h)
        trace_path = p

    stable = len(set(hashes)) == 1
    result = {
        "harness_version": HARNESS_VERSION,
        "case": a.case,
        "passes": a.passes,
        "payload_sha256_per_pass": hashes,
        "self_consistent": stable,
        "envelope_excluded_from_equality": envelope_keys(trace_path) if trace_path else [],
    }
    if a.expect:
        result["expected_payload_sha256"] = a.expect
        result["matches_manifest"] = (stable and hashes[0] == a.expect)
    print(json.dumps(result, sort_keys=True))
    if a.expect:
        return 0 if result["matches_manifest"] else 1
    return 0 if stable else 1


if __name__ == "__main__":
    raise SystemExit(main())
