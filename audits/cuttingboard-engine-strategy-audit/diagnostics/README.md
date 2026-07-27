# Diagnostics — local directory index

Status: `LOCAL DIRECTORY INDEX ONLY — NOT A REGISTRATION`

Created: 2026-07-27 UTC

## What this file is

An index of what this directory currently contains. Nothing more.

## What this file is not

**It is not a registration.** `diagnostics/` has no standing in the governing
TV-0 → TV-4 protocol. No frozen TV-0 authority, no charge, no amendment, and no
adjudication record names this directory or anything in it. Writing this index does not
change that: **UV02 remains unregistered in every governing document.** This index narrows a
documentation gap; it does not close it, and it confers nothing.

**It grants no status.** Nothing in this directory is canonical, is a work packet, or is
parity evidence for the pinned engine at
`dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`. Nothing here may be cited
as such.

**It repairs no authority issue.** This file has no bearing on any frozen-document hash, on
the recorded hashes in [`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md), or on any
question about whether a later stage may consume a given document. It resolves no hash
mismatch and creates no precedence.

Where this index and any governing document appear to disagree, **the governing document
governs**, without exception.

## Relationship to the audit lifecycle

`docs/conventions.md` §h describes an audit's shape as `spec/`, `charges/`, `reviews/`,
`parity/`, and `runs/`. `diagnostics/` is none of those. It holds side-studies that are not
TV-0 → TV-4 packet evidence: work that used the audit's materials but that no packet
commissioned and no packet consumes.

A side-study here may become useful context for a later stage. It is never automatically
promoted into one, and it never contributes to TV-2 parity acceptance or a TV-3 run package.

## Contents

### `uv02/` — Universe Relevance Study

A diagnostic study of gate behaviour under a deliberately different breadth and leadership
universe than the pinned engine's. Because that membership differs by construction, its R-01
output is **not comparable to the pinned engine** and cannot be used for TV-1 or TV-2 parity.

| File | Role |
|---|---|
| [`uv02/UV02_STUDY_CONTRACT.md`](uv02/UV02_STUDY_CONTRACT.md) | The study's formal identity, claim boundary, and prohibitions |
| [`uv02/UNIVERSE_V0.2.md`](uv02/UNIVERSE_V0.2.md) | Universe membership note — what changed from v0.1 and why |
| [`uv02/UV02_CAPTURE_LOG.md`](uv02/UV02_CAPTURE_LOG.md) | Capture-session record and recorded provenance gaps |
| [`uv02/UV02_CAPTURE_LOG_AMENDMENT_2026-07-27.md`](uv02/UV02_CAPTURE_LOG_AMENDMENT_2026-07-27.md) | Dated corrections to the capture log — the log itself is unedited |
| [`uv02/UV02_EVIDENCE_CAPABILITY.md`](uv02/UV02_EVIDENCE_CAPABILITY.md) | What the captured artifacts can and cannot establish |
| [`uv02/manifests/UV02_RUN_MANIFEST_v0.1.md`](uv02/manifests/UV02_RUN_MANIFEST_v0.1.md) | Versioned run-manifest contract for any future UV02 run |
| [`uv02/LEDGER.csv`](uv02/LEDGER.csv) | Authoritative run record under `docs/conventions.md` §f |
| [`uv02/cuttingboard_direct_proxy_v0.2.pine`](uv02/cuttingboard_direct_proxy_v0.2.pine) | The v0.2 source, SHA-256 `d2420bc3…3ce`. Never edited in place |
| `uv02/exports/` | Seven raw TradingView List of Trades captures, V0–V6. Immutable |

## Standing rules that still apply here

`docs/conventions.md` applies in full to everything in this directory:

- **§b** — frozen documents are never edited in place; corrections are dated amendments or
  new versioned files.
- **§e** — exports are self-describing and immutable. A re-capture produces new files, never
  an edit to an existing one.
- **§f** — `LEDGER.csv` is authoritative. When an export, a screenshot, and the ledger
  disagree, the ledger wins.
- **§h** — unavailable is not the same as passing. The audited source is read-only evidence
  pinned to a commit, and no result here may mutate it or feed back into it.
- **§i** — cross-repository isolation. `dwats250/strategy` is the only repository this work
  may mutate; `dwats250/cuttingboard` is a forbidden mutation target.
