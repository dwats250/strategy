# Audit data

Governed by [`../spec/DATA_PROVENANCE_CONTRACT.md`](../spec/DATA_PROVENANCE_CONTRACT.md),
which is `DRAFT / EXPLORATORY` — not frozen.

**No download or acquisition script is authorized in this packet.** This directory documents
where data will live and under what rules. It holds no data today.

## Rules

1. **Raw vendor exports are private and untracked** unless their redistribution rights are
   affirmatively known. Unknown rights are treated as no rights.

2. **Raw vendor exports belong only under `data/raw/`**, which is gitignored. This is the
   single permitted location for them anywhere in this repository. Do not place raw vendor
   files in `runs/`, `parity/`, or beside a result that references them.

3. **Manifests, checksums, schemas, acquisition code, and permitted derived results may be
   tracked.** A derived result is trackable only if it does not reconstitute the underlying
   raw series.

4. **Raw files are never silently edited.** They are immutable once written. Corrections
   produce a new normalized file; they never modify the raw input. A wrong raw file stays as
   it is, and the record of it being wrong is part of the evidence.

5. **Normalized files must point back to an immutable raw manifest** — by `file_sha256`, not
   by filename. A normalized file whose raw ancestry cannot be reconstructed is not evidence.

## Layout

These directories are created when they first hold something. They are not committed empty.

| Path | Tracked | Contents |
|---|---|---|
| `data/raw/` | **No** — gitignored | Raw vendor exports, exactly as retrieved. Immutable. |
| `data/normalized/` | Case by case | Datasets derived under the provenance contract, each referencing its raw manifest by checksum. Trackable only where rights and size permit. |
| `data/manifests/` | **Yes** | Provenance manifests and checksums. Tracked even when the data they describe is not — the manifest is the durable record. |

The manifest for an untracked raw file is the only thing that survives in version control.
It must be complete enough to identify exactly what was retrieved, from where, when, and under
what terms — and to detect if the file ever changes.

## Relationship to run folders

Run folders under [`../runs/`](../runs/README.md) reference their inputs by manifest and
checksum. They **do not duplicate raw vendor files**. A run that copies its raw inputs
alongside its results has created a second, unmanaged copy that can drift from the immutable
original and that carries the same redistribution problem the ignore rule exists to prevent.

One raw file, one location, referenced by checksum from everywhere else.

## Ignore rule

`.gitignore` at the repository root ignores `audits/cuttingboard-engine-strategy-audit/data/raw/`
and nothing else. The rule is deliberately narrow: this lab tracks study CSV exports under
`studies/*/exports/`, and a blanket CSV ignore would break that.
