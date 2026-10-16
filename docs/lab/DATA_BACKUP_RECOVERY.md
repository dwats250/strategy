# Local-only datasets — backup and recovery plan

Vendor data is never committed (licensing, size). The repository commits identities instead:
`datasets/REGISTRY.json` records each dataset's SHA-256, row count, provider, query and semantics.
Every load re-verifies the SHA-256 and fails closed on a mismatch.

## Where the bytes are (2026-10-16)

| Copy | Path | Contents |
|---|---|---|
| Primary (lab store) | `~/.local/share/stratlab/datasets/` | `SPY_1m_2024-09-01_2026-08-22.csv.gz` (10.8 MB), its capture manifest, `raw/…/page0001-0009.json` (47 MB) |
| Original | `~/Projects/strategy/studies/vwap-lab-2026-08/data/cache/` (main checkout, gitignored) | Same files and the August derived features |
| Source evidence | `~/.local/share/stratlab/sources/instagram-Dd-ClqHtd-1/` | Reel video (SHA-256 `10c18b19…`), metadata, transcript |

Both data copies are **on the same disk**. That is not a backup.

## Required backup (action for Dustin, about 5 minutes)

1. Copy `~/.local/share/stratlab/` to storage that is not on this machine: an external drive, or a
   private cloud bucket or drive folder. It is about 60 MB.
   ```bash
   tar czf stratlab-store-$(date +%F).tgz -C ~/.local/share stratlab
   sha256sum stratlab-store-*.tgz > stratlab-store.sha256
   ```
2. Keep the `.sha256` next to the archive. After restoring, run `uv run stratlab data verify <dataset_id>`.
3. Repeat after every new download. A new dataset is a new registry entry, so the archive grows and is never edited.

## Recovery paths, best first

1. **Restore the archive** to `~/.local/share/stratlab/`, or point `STRATLAB_DATA_DIR` at any directory
   that holds the file. `stratlab data verify` confirms the identity.
2. **Rebuild the canonical file from the raw pages.** The 9 raw pages reproduce the canonical CSV
   deterministically through `studies/vwap-lab-2026-08/data/fetch_spy_aggs.py`'s normalize step
   (gzip `mtime=0`). The result must hash to `a4afaa70…`; if it does not, it is not the original corpus.
3. **Re-download.** `MASSIVE_API_KEY` / `POLYGON_API_KEY` is needed and is **not set** on this machine
   today. A re-download is a **new dataset with a new id and SHA-256**, even for the same date range,
   because vendors revise history. It is registered as a new entry and never presented as the original
   corpus. Runs record the dataset id they used, so the two can never be confused.

## What is blocked without the data

CI runs on synthetic fixtures only and never needs vendor data. Without a local copy, real-data runs
and the parity test against the August implementation cannot run; that test skips itself and says why.
