# EA engine-audit data area

Status: `ACTIVE — POLICY. NO VENDOR DATA IS PRESENT OR AUTHORIZED.`

Created: 2026-07-28 UTC

Governed by [`../../spec/DATA_PROVENANCE_CONTRACT.md`](../../spec/DATA_PROVENANCE_CONTRACT.md)
and [`../EA-8-ASOF-CONTRACT.md`](../EA-8-ASOF-CONTRACT.md).

---

## What lives here

| Path | Tracked? | Contents |
|---|---|---|
| `manifests/` | **yes** | Provenance manifests and checksums for every admitted dataset, plus the look-ahead suite result |
| `raw/` | **no — git-ignored, and currently absent** | Immutable vendor exports, if any are ever authorized |
| `normalized/` | **no — git-ignored, and currently absent** | Derived series, each pointing back to a raw manifest |

`raw/` and `normalized/` are **not created** by EA-8. Per the plan, an empty placeholder
directory without current purpose is not created.

## Policy

1. **Raw vendor exports are private and untracked unless redistribution rights are known.** No
   vendor data has been retrieved, and none is authorized. If that changes it requires its own
   Dustin-authorized charge.
2. **Manifests, checksums, schemas, and acquisition code may be tracked.** They carry no
   redistribution risk and they are what makes a dataset checkable.
3. **Raw files are immutable once written.** Never edited, re-sorted, re-encoded, cleaned, or
   partially corrected in place. A correction produces a new normalized file referencing the
   immutable raw manifest it derives from.
4. **A normalized file whose raw ancestry cannot be reconstructed is not evidence.**
5. **Missing bars stay missing.** Never forward-filled, interpolated, or silently dropped.
   Duplicates are reported and resolved by a recorded rule, never silently deduplicated.

## Why the parquet itself is not tracked here

The datasets EA-8 built are **regenerable, not retrieved**. `../fixtures/build_inputs.py`
produces the full-history source deterministically and `../tools/dataset/asof_build.py`
truncates it; the manifests in `manifests/` carry a `file_sha256` and a `content_digest_sha256`
per symbol, so any regeneration is checkable against them. Tracking 100 parquet files that a
committed generator reproduces exactly would add weight without adding evidence.

**This is a synthetic dataset.** It exercises code paths. It is not market data and supports no
claim about market behaviour.

## Current admitted datasets

Five as-of datasets, 20 symbols each, all passing the look-ahead suite —
see [`../EA-8-ASOF-CONTRACT.md`](../EA-8-ASOF-CONTRACT.md) § 4 for the evaluable range and its
limits, and `manifests/EA-8-LOOKAHEAD-SUITE-RESULT.txt` for the suite output.
