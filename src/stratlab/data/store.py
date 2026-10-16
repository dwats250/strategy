"""Local dataset store: registry lookup, SHA-256 identity check, canonical load.

Datasets are local-only and content-addressed. The committed registry
(`datasets/REGISTRY.json`) records each dataset's identity; the bytes live outside
git. Every load verifies the SHA-256 before parsing, so a run can never silently
consume a different file under a familiar name.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = REPO_ROOT / "datasets" / "REGISTRY.json"
DEFAULT_STORE = Path(os.path.expanduser("~/.local/share/stratlab/datasets"))


class DatasetError(RuntimeError):
    pass


@dataclass(frozen=True)
class DatasetRecord:
    id: str
    filename: str
    sha256: str
    rows: int
    format: str
    meta: dict


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, DatasetRecord]:
    raw = json.loads(Path(path).read_text())
    out = {}
    for ds_id, m in raw["datasets"].items():
        out[ds_id] = DatasetRecord(ds_id, m["filename"], m["sha256"], int(m["rows"]), m["format"], m)
    return out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def candidate_paths(rec: DatasetRecord) -> list[Path]:
    paths = []
    env = os.environ.get("STRATLAB_DATA_DIR")
    if env:
        paths.append(Path(env).expanduser() / rec.filename)
    paths.append(DEFAULT_STORE / rec.filename)
    for loc in rec.meta.get("known_locations", []):
        p = Path(os.path.expanduser(loc))
        paths.append(p if p.is_absolute() else REPO_ROOT / p)
    return paths


def resolve(ds_id: str, registry: dict[str, DatasetRecord] | None = None) -> tuple[DatasetRecord, Path]:
    """Find a local copy of `ds_id` whose SHA-256 matches the registry. Fail closed."""
    registry = registry or load_registry()
    if ds_id not in registry:
        raise DatasetError(f"unknown dataset id {ds_id!r}; registered: {sorted(registry)}")
    rec = registry[ds_id]
    tried = []
    for p in candidate_paths(rec):
        if not p.exists():
            tried.append(f"{p} (absent)")
            continue
        if sha256_file(p) == rec.sha256:
            return rec, p
        tried.append(f"{p} (SHA-256 MISMATCH)")
    raise DatasetError(
        f"dataset {ds_id} not available with sha256 {rec.sha256}.\nTried:\n  " + "\n  ".join(tried)
        + "\nSee docs/lab/DATA_BACKUP_RECOVERY.md for recovery.")


def read_canonical(path: Path | io.BytesIO, fmt: str) -> pd.DataFrame:
    """Parse a canonical file into a UTC-indexed OHLCV frame (bar-start timestamps)."""
    if fmt != "august-canonical-v1":
        raise DatasetError(f"unsupported dataset format {fmt!r}")
    df = pd.read_csv(path, compression="gzip", usecols=["t_ms", "o", "h", "l", "c", "v", "vw", "n"],
                     dtype={"t_ms": "int64", "o": "float64", "h": "float64", "l": "float64",
                            "c": "float64", "v": "float64", "vw": "float64", "n": "float64"})
    idx = pd.to_datetime(df["t_ms"], unit="ms", utc=True)
    out = pd.DataFrame({
        "Open": df["o"].to_numpy(), "High": df["h"].to_numpy(), "Low": df["l"].to_numpy(),
        "Close": df["c"].to_numpy(), "Volume": df["v"].to_numpy(),
        "VendorVWAP": df["vw"].to_numpy(), "Trades": df["n"].to_numpy(),
    }, index=pd.DatetimeIndex(idx, name="ts_utc").as_unit("ns"))
    return out


def load_mask(rec: DatasetRecord, mask_id: str) -> set[int]:
    masks = rec.meta.get("masks", {})
    if mask_id not in masks:
        raise DatasetError(f"dataset {rec.id} has no mask {mask_id!r}")
    m = masks[mask_id]
    p = REPO_ROOT / m["path"]
    if sha256_file(p) != m["sha256"]:
        raise DatasetError(f"mask {mask_id} SHA-256 mismatch at {p}")
    body = json.loads(p.read_text())
    if body.get("corpus_sha256") not in (None, rec.sha256):
        raise DatasetError(f"mask {mask_id} is bound to a different corpus")
    return {int(t) for t in body["mask_t_ms"]}


def load_dataset(ds_id: str, mask: str | None = None) -> tuple[pd.DataFrame, dict]:
    """Load a verified dataset. Returns (bars, identity) where identity is run-record ready."""
    registry = load_registry()
    rec, path = resolve(ds_id, registry)
    blob = Path(path).read_bytes()
    # Hash the exact bytes that are parsed, so verification and parsing cannot diverge.
    if hashlib.sha256(blob).hexdigest() != rec.sha256:
        raise DatasetError(f"{ds_id}: SHA-256 changed between resolve and read ({path})")
    df = read_canonical(io.BytesIO(blob), rec.format)
    if len(df) != rec.rows:
        raise DatasetError(f"{ds_id}: row count {len(df)} != registered {rec.rows}")
    identity = {"dataset_id": rec.id, "sha256": rec.sha256, "rows": rec.rows,
                "path_used": str(path), "mask": None}
    if mask:
        drop = load_mask(rec, mask)
        t_ms = df.index.as_unit("ns").asi8 // 1_000_000
        keep = ~pd.Index(t_ms).isin(list(drop))
        identity["mask"] = {"id": mask, "sha256": rec.meta["masks"][mask]["sha256"],
                            "bars_dropped": int((~keep).sum())}
        df = df[keep]
    return df, identity
