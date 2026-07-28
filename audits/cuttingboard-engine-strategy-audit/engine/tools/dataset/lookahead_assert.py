#!/usr/bin/env python3
"""EA-8 look-ahead assertion suite.

For every as-of dataset, asserts the single invariant that makes the whole
program's evidence trustworthy:

    NO INPUT ROW MAY CARRY A TIMESTAMP AFTER THE AS-OF BOUNDARY.

Checks per dataset:

  A1  every parquet's maximum bar timestamp is <= the as-of boundary
  A2  the manifest's recorded `max_bar_timestamp` matches the file on disk
      (a manifest that disagrees with its data is not evidence)
  A3  every parquet's content digest matches the manifest
  A4  no duplicate bar timestamps
  A5  the manifest declares a truncation rule and an as-of boundary

Exit code is 0 only if every assertion passes for every dataset. A violation is
reported per-symbol and per-check, never summarised away.

This suite is only worth its cost if it can FAIL. `--self-test` deliberately
injects a future bar into a scratch copy and asserts the suite catches it; that
negative control is run alongside the real pass in EA-8's evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

import pandas as pd

SUITE_VERSION = "EA-8-lookahead/1.0.0"
REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def content_digest(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(df.index.astype("int64").values.tobytes())
    for col in REQUIRED_COLUMNS:
        h.update(df[col].to_numpy(dtype="float64").tobytes())
    return h.hexdigest()


def check_dataset(ds_dir: Path) -> tuple[bool, list[str]]:
    failures: list[str] = []
    mf_path = ds_dir / "manifest.json"
    if not mf_path.exists():
        return False, [f"{ds_dir.name}: A5 no manifest.json"]
    mf = json.loads(mf_path.read_text(encoding="utf-8"))

    as_of_str = mf.get("as_of_boundary")
    if not as_of_str:
        failures.append(f"{ds_dir.name}: A5 manifest declares no as_of_boundary")
        return False, failures
    if not mf.get("truncation_rule"):
        failures.append(f"{ds_dir.name}: A5 manifest declares no truncation_rule")
    as_of = pd.Timestamp(as_of_str)

    by_symbol = {s["canonical_symbol"]: s for s in mf.get("symbols", [])}
    cache = ds_dir / "data" / "cache"
    files = sorted(cache.glob("*_ohlcv.parquet"))
    if not files:
        return False, [f"{ds_dir.name}: A1 no parquet found under {cache}"]

    for f in files:
        sym = f.name.replace("_ohlcv.parquet", "")
        df = pd.read_parquet(f)

        # A1 — the invariant.
        mx = df.index.max()
        if mx > as_of:
            failures.append(
                f"{ds_dir.name}/{sym}: A1 LOOK-AHEAD — max bar {mx:%Y-%m-%d} > as-of {as_of_str}"
            )

        rec = by_symbol.get(sym)
        if rec is None:
            failures.append(f"{ds_dir.name}/{sym}: A2 present on disk but absent from manifest")
            continue

        # A2 — manifest agrees with disk.
        if rec.get("max_bar_timestamp") != mx.strftime("%Y-%m-%d"):
            failures.append(
                f"{ds_dir.name}/{sym}: A2 manifest max_bar {rec.get('max_bar_timestamp')} "
                f"!= disk {mx:%Y-%m-%d}"
            )

        # A3 — content digest.
        if rec.get("content_digest_sha256") != content_digest(df):
            failures.append(f"{ds_dir.name}/{sym}: A3 content digest mismatch")

        # A4 — duplicates.
        dup = int(df.index.duplicated().sum())
        if dup:
            failures.append(f"{ds_dir.name}/{sym}: A4 {dup} duplicate bar timestamp(s)")

    return (not failures), failures


def self_test(ds_dir: Path) -> bool:
    """Negative control: inject a future bar and require the suite to catch it."""
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / ds_dir.name
        shutil.copytree(ds_dir, scratch)
        cache = scratch / "data" / "cache"
        target = sorted(cache.glob("*_ohlcv.parquet"))[0]
        df = pd.read_parquet(target)
        future = df.index.max() + pd.Timedelta(days=30)
        row = df.iloc[[-1]].copy()
        row.index = pd.DatetimeIndex([future], name=df.index.name)
        pd.concat([df, row]).to_parquet(target)

        ok, failures = check_dataset(scratch)
        caught = (not ok) and any("A1 LOOK-AHEAD" in f for f in failures)
        verdict = "CAUGHT it (expected)" if caught else "MISSED IT — SUITE IS UNSOUND"
        print(f"SELF-TEST negative control: injected bar {future:%Y-%m-%d} into "
              f"{target.name} -> suite {verdict}")
        for f in failures[:3]:
            print(f"    {f}")
        return caught


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", required=True, type=Path,
                    help="directory containing asof-* dataset directories")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    dirs = sorted(d for d in a.datasets.glob("asof-*") if d.is_dir())
    if not dirs:
        print(f"no asof-* datasets under {a.datasets}")
        return 2

    print(f"suite={SUITE_VERSION} datasets={len(dirs)}")
    all_ok = True
    for d in dirs:
        ok, failures = check_dataset(d)
        print(f"  {d.name:22s} {'PASS' if ok else 'FAIL'}")
        for f in failures:
            print(f"      {f}")
        all_ok = all_ok and ok

    if a.self_test:
        if not self_test(dirs[0]):
            print("SUITE UNSOUND — negative control not caught")
            return 3

    print(f"RESULT: {'ALL DATASETS PASS' if all_ok else 'VIOLATIONS PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
