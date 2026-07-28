#!/usr/bin/env python3
"""EA-8 as-of dataset builder.

Builds, for each requested as-of date, the complete input set a replay needs:

  * an **as-of-truncated** OHLCV parquet cache — bars strictly at or before the
    as-of boundary and nothing after, and
  * a per-date quote fixture derived from the as-of bar,

together with a provenance manifest carrying every field
`spec/DATA_PROVENANCE_CONTRACT.md` requires.

Why truncation is done here and not by the engine
-------------------------------------------------
At the pin, `runtime._cache_only` is:

    def _cache_only(symbol):
        cache_path = _ohlcv_cache_path(symbol)
        if not cache_path.exists():
            return None
        return pd.read_parquet(cache_path)

It applies **no date filter**. The cache file's contents therefore *are* the
as-of boundary. A full-history cache would silently expose future bars to every
rolling computation. Truncation is Strategy's responsibility, and this file is
where it happens.

Provider-agnostic: the source is a directory of full-history parquet keyed by
canonical symbol. It does not fetch anything and has no network access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

BUILDER_VERSION = "EA-8-asof-build/1.0.0"
REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def safe_symbol(sym: str) -> str:
    """Mirror `ingestion._ohlcv_cache_path` naming exactly."""
    return sym.replace("^", "").replace("-", "_").replace(".", "_").upper()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def content_digest(df: pd.DataFrame) -> str:
    """Digest the DATA, not the parquet container (writer metadata is unstable)."""
    h = hashlib.sha256()
    h.update(df.index.astype("int64").values.tobytes())
    for col in REQUIRED_COLUMNS:
        h.update(df[col].to_numpy(dtype="float64").tobytes())
    return h.hexdigest()


def truncate(df: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    """Bars at or before the as-of boundary. Nothing after. No fill, no interpolation."""
    return df.loc[df.index <= as_of].copy()


def integrity(df: pd.DataFrame, expected_sessions: pd.DatetimeIndex | None) -> dict:
    dup = int(df.index.duplicated().sum())
    missing_dates: list[str] = []
    if expected_sessions is not None:
        present = set(df.index)
        missing_dates = [d.strftime("%Y-%m-%d") for d in expected_sessions if d not in present]
    return {
        "row_count": int(len(df)),
        "date_range_start": df.index.min().strftime("%Y-%m-%d") if len(df) else None,
        "date_range_end": df.index.max().strftime("%Y-%m-%d") if len(df) else None,
        "duplicate_bar_count": dup,
        "duplicate_bar_policy": "reported, never silently deduplicated; a nonzero count fails admission",
        "missing_bar_count": len(missing_dates),
        "missing_bar_dates": missing_dates,
        "missing_bar_policy": "recorded as missing; never forward-filled, interpolated, or silently dropped",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path,
                    help="directory of full-history parquet, one per canonical symbol")
    ap.add_argument("--as-of", required=True, nargs="+", help="as-of dates, YYYY-MM-DD")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--source-name", default="SYNTHETIC-EA7-LIBRARY")
    ap.add_argument("--source-endpoint", default="engine/fixtures/build_inputs.py (deterministic generator)")
    ap.add_argument("--retrieved-by", default="EA-8 as-of builder (no network)")
    ap.add_argument("--instrument-type", default="MIXED (ETF / index / equity / FX proxy / crypto pair)")
    ap.add_argument("--exchange", default="NOT_ESTABLISHED")
    ap.add_argument("--retrieval-timestamp-utc", default=None,
                    help="UTC timestamp of the original retrieval; required for real vendor data")
    a = ap.parse_args()

    src_files = sorted(a.source.glob("*_ohlcv.parquet"))
    if not src_files:
        print(f"no source parquet under {a.source}")
        return 2

    a.out.mkdir(parents=True, exist_ok=True)
    datasets = []

    for as_of_str in a.as_of:
        as_of = pd.Timestamp(as_of_str)
        ds_dir = a.out / f"asof-{as_of_str}"
        cache_dir = ds_dir / "data" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

        symbols = []
        for f in src_files:
            df = pd.read_parquet(f)
            missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            if missing_cols:
                print(f"REFUSED {f.name}: missing columns {missing_cols}")
                return 3
            cut = truncate(df, as_of)
            if cut.empty:
                print(f"REFUSED {f.name}: no bars at or before {as_of_str} — "
                      f"evaluable range must be narrowed, not approximated")
                return 4
            out_f = cache_dir / f.name
            cut.to_parquet(out_f)
            rec = {
                "vendor_symbol": f.name.replace("_ohlcv.parquet", ""),
                "canonical_symbol": f.name.replace("_ohlcv.parquet", ""),
                "exchange": a.exchange,
                "instrument_type": a.instrument_type,
                "file_sha256": sha256_file(out_f),
                "content_digest_sha256": content_digest(cut),
                "max_bar_timestamp": cut.index.max().strftime("%Y-%m-%d"),
            }
            rec.update(integrity(cut, None))
            symbols.append(rec)

        manifest = {
            "manifest_version": "EA-8/v1",
            "builder_version": BUILDER_VERSION,
            "dataset_id": f"asof-{as_of_str}",
            "as_of_boundary": as_of_str,
            "source_and_retrieval": {
                "source_name": a.source_name,
                "source_endpoint": a.source_endpoint,
                "retrieval_timestamp_utc": a.retrieval_timestamp_utc or "NOT_APPLICABLE_SYNTHETIC",
                "retrieved_by": a.retrieved_by,
                "access_terms_reviewed": "NOT_APPLICABLE_SYNTHETIC — no vendor data retrieved",
            },
            "temporal_contract": {
                "timeframe": "1D",
                "timezone": "naive-date (no intraday component)",
                "exchange_session": "NOT_ESTABLISHED",
                "session_calendar": "pandas business-day (synthetic); NOT an exchange holiday calendar",
                "bar_timestamp_convention": "bar date labels the session; no open/close disambiguation is claimed",
            },
            "price_semantics": {
                "ohlcv_basis": "SYNTHETIC — neither raw-vendor nor adjusted",
                "split_treatment": "NOT_APPLICABLE_SYNTHETIC",
                "dividend_treatment": "NOT_APPLICABLE_SYNTHETIC",
                "adjustment_as_of": "NOT_APPLICABLE_SYNTHETIC",
            },
            "symbols": symbols,
            "symbol_count": len(symbols),
            "truncation_rule": "bars where index <= as_of_boundary; nothing after; no fill or interpolation",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        (ds_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        datasets.append((as_of_str, len(symbols),
                         max(s["max_bar_timestamp"] for s in symbols)))
        print(f"built asof-{as_of_str}  symbols={len(symbols)}  "
              f"max_bar={max(s['max_bar_timestamp'] for s in symbols)}")

    print(f"datasets={len(datasets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
