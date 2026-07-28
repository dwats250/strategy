#!/usr/bin/env python3
"""EA-7 deterministic input library.

Regenerates, from a base quote fixture plus a small declarative case table, the
complete input set every EA-7 replay needs:

  * per-case quote fixtures (JSON), and
  * a synthetic daily OHLCV cache (parquet) that lets the pipeline reach the
    decision layer.

Determinism is the whole point. There is no RNG, no wall-clock read, and no
network access anywhere in this file. Given the same base fixture and the same
CASES table, it emits byte-identical JSON and numerically identical OHLCV.

The OHLCV series is SYNTHETIC. It is a harness input for exercising code paths,
not market data, and it supports no claim about market behaviour.

Usage:
    python3 build_inputs.py --base <base-fixture.json> --out-fixtures <dir> \\
                            --out-cache <dir> [--only <case>]
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

# Deterministic series parameters — changing any of these changes every hash.
BARS = 260
END_DATE = "2026-04-10"
DRIFT_LOG = 0.28          # total log-drift across the window
WOBBLE_AMP = 0.004        # deterministic sinusoid amplitude
WOBBLE_PERIOD = 7.0
HIGH_K, LOW_K, OPEN_K = 1.006, 0.994, 0.999
VOLUME_FLOOR = 1_000_000.0

# Case table. Each entry is (case_id, mutation) where mutation edits the quote
# dict in place. Mutations are pure and order-independent.
CASES: dict[str, str] = {
    "rejected": "baseline — no mutation",
    "boundary-vix-at-35": "^VIX price = 35.0 (kill-switch threshold, strict > must not trip)",
    "halted-killswitch": "^VIX price = 35.01 (just above threshold, must trip)",
    "halted-validation": "drop SPY (a HALT_SYMBOLS member)",
    "stale-data": "PAAS fetched_at_utc skewed 2h older than the newest quote",
    "missing-data": "drop PAAS (not a HALT_SYMBOLS member)",
}


def mutate(case_id: str, d: dict) -> dict:
    if case_id == "rejected":
        pass
    elif case_id == "boundary-vix-at-35":
        d["^VIX"]["price"] = 35.0
    elif case_id == "halted-killswitch":
        d["^VIX"]["price"] = 35.01
    elif case_id == "halted-validation":
        d.pop("SPY")
    elif case_id == "stale-data":
        # age_seconds is inert for validation: _fixture_validation_clock freezes
        # now() to max(fetched_at_utc) and validation recomputes age from
        # timestamps. Staleness must therefore be expressed as a timestamp skew.
        d["PAAS"]["fetched_at_utc"] = "2026-04-12T11:00:00Z"
        d["PAAS"]["age_seconds"] = 7200.0
    elif case_id == "missing-data":
        d.pop("PAAS")
    else:
        raise ValueError(f"unknown case: {case_id}")
    return d


def safe_symbol(sym: str) -> str:
    return sym.replace("^", "").replace("-", "_").replace(".", "_").upper()


def build_ohlcv(price: float, volume: float | None) -> pd.DataFrame:
    """A deterministic, gently-trending synthetic daily series ending at `price`."""
    idx = pd.bdate_range(end=END_DATE, periods=BARS)
    n = len(idx)
    drift = np.linspace(0.0, 1.0, n)
    wobble = WOBBLE_AMP * np.sin(np.arange(n) / WOBBLE_PERIOD)
    close = price * np.exp(-DRIFT_LOG * (1.0 - drift)) * (1.0 + wobble)
    close = close * (price / close[-1])          # land the last close exactly on `price`
    df = pd.DataFrame(
        {
            "Open": close * OPEN_K,
            "High": close * HIGH_K,
            "Low": close * LOW_K,
            "Close": close,
            "Volume": np.full(n, max(float(volume or VOLUME_FLOOR), VOLUME_FLOOR)),
        },
        index=idx,
    )
    df.index.name = "Date"
    return df


def content_digest(df: pd.DataFrame) -> str:
    """Hash the DATA, not the parquet container.

    Parquet embeds writer metadata, so its bytes are not a stable identity across
    library versions. The replay contract therefore pins the numeric content.
    """
    h = hashlib.sha256()
    h.update(df.index.astype("int64").values.tobytes())
    for col in ("Open", "High", "Low", "Close", "Volume"):
        h.update(np.ascontiguousarray(df[col].values, dtype="float64").tobytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, type=Path)
    ap.add_argument("--out-fixtures", required=True, type=Path)
    ap.add_argument("--out-cache", required=True, type=Path)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()

    base = json.loads(a.base.read_text(encoding="utf-8"))
    a.out_fixtures.mkdir(parents=True, exist_ok=True)
    a.out_cache.mkdir(parents=True, exist_ok=True)

    for case_id in CASES:
        if a.only and case_id != a.only:
            continue
        d = mutate(case_id, copy.deepcopy(base))
        p = a.out_fixtures / f"fixture-{case_id}.json"
        # Canonical: sorted keys, fixed indent, newline-terminated.
        p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"fixture {case_id:22s} sha256={hashlib.sha256(p.read_bytes()).hexdigest()}")

    digests = {}
    for sym, q in sorted(base.items()):
        df = build_ohlcv(float(q["price"]), q.get("volume"))
        df.to_parquet(a.out_cache / f"{safe_symbol(sym)}_ohlcv.parquet")
        digests[sym] = content_digest(df)
    combined = hashlib.sha256(
        json.dumps(digests, sort_keys=True).encode("utf-8")
    ).hexdigest()
    print(f"ohlcv symbols={len(digests)} bars={BARS} content_digest={combined}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
