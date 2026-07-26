# Installation Record — CuttingBoard Engine Strategy Audit

Status: BINDING FOR REPOSITORY-PATH CORRECTIONS ONLY

Installed: 2026-07-25

This file is installation metadata and a binding path-correction instrument. It is
**not** an audit authority. It cannot alter any gate formula, threshold, classification,
variant, safeguard, or review rule. Where this file and a TV-0 document disagree about
anything other than a repository path, the TV-0 document governs.

## Why this file exists

The four commissioned TV-0 documents are installed **byte-identical** so their SHA-256
hashes can be recorded and handed to the TV-0R reviewer. Nothing may be appended to them
during this scaffold packet. Corrections that must be recorded now — repository paths,
declared deviations, and installed hashes — therefore live here instead.

## Source bundle

- Bundle: `strategy-cuttingboard-audit-commission-v0.1.zip`
- Retained outside this repository at `~/Downloads/` (operator-held; not tracked here)
- Unpacked into the `strategy` worktree, then installed by this packet
- All seven bundle files were verified byte-identical against the archive before any
  file was moved or removed

## Installed documents and hashes

Record these hashes when commissioning TV-0R. A hash mismatch at review time means the
frozen contract drifted and the review must stop.

| Path | Role | SHA-256 |
|---|---|---|
| `README.md` | TV-0 authority | `95b8fc4baa63d6b2319a7427617b79d21ddf2ef28a21fe6dbb0eb994ecb3aad3` |
| `spec/GATE_TRANSLATION_MATRIX.md` | TV-0 authority | `04e130a51cf1d1a9f98377f8f4b372c457f4a2f5c974557fa6363af5764d605d` |
| `spec/BACKTEST_PROTOCOL.md` | TV-0 authority | `5d45c21c45f1b2ddde3c75f7ef76b3ef6608abdd5c1010ed9482a32252bb33f3` |
| `charges/TV-1-PINE-IMPLEMENTATION.md` | TV-0 authority | `b2f3c0b24047ffdf8924d3e4a423069a9ccf2334cb3286783a9e519d52e31d90` |
| `charges/PRIMARY-CHARGE-STRATEGY-REPOSITORY-AND-CUTTINGBOARD-AUDIT.md` | Commission provenance | `c45c58e93d985bcb4b70db5ee7585e25b66636bc4ac785153e099c77a1e032a9` |

Two bundle files were **not** installed: `MANIFEST.md` and `CLAUDE-SESSION-START.md`. The
bundle declares both "operator aids… not additional audit authorities." Both were confirmed
byte-identical inside the retained archive before being removed from this worktree. Neither
was ever tracked, so no git history was affected.

## Pinned source snapshot

- Repository: `dwats250/cuttingboard`
- Commit: `59f8279d796335149afdec4aa507b6f927233518`
- Commit date: `2026-07-26T01:35:59Z`
- Resolution verified at install time via the GitHub API and against a local clone
- Mutation permission: **NONE**

**Reading pinned source.** The local clone at `~/Projects/cuttingboard` sits ahead of the
pin with a dirty working tree. Pinned evidence must be read with
`git show 59f8279d796335149afdec4aa507b6f927233518:<path>`, never from that working tree.
Reading the working tree would silently substitute unpinned code for pinned evidence.

## Binding repository-path correction to TV-1

`charges/TV-1-PINE-IMPLEMENTATION.md` names "a separate `cuttingboard-gate-lab` companion
repository" and instructs the implementer to stop if it does not exist. The primary charge
names Dustin's existing `strategy` repository as the writable target and pre-authorizes
"repository-path corrections approved during organization."

**Dustin approved this resolution on 2026-07-25: `strategy` is the companion repository.**

TV-1's `Allowed files` are root-relative to the assumed companion repository. Those paths
are stale. This record overrides **only** those paths, as follows:

| TV-1 `Allowed files` entry | Corrected path |
|---|---|
| `pine/cuttingboard_direct_proxy_v0.1.pine` | `audits/cuttingboard-engine-strategy-audit/pine/cuttingboard_direct_proxy_v0.1.pine` |
| `spec/PARITY_CASES.md` | `audits/cuttingboard-engine-strategy-audit/spec/PARITY_CASES.md` |
| `runs/RUN_MANIFEST_TEMPLATE.md` | `audits/cuttingboard-engine-strategy-audit/runs/RUN_MANIFEST_TEMPLATE.md` |
| `README.md` (link-only edit) | `audits/cuttingboard-engine-strategy-audit/README.md` |

TV-1's companion-repository STOP condition is satisfied by this approved correction and
must not be re-triggered on path grounds alone.

### Scope limit of this override

This override reaches repository paths and nothing else. Every other TV-1 boundary is
**unchanged and still binding**:

- change-surface ceiling: 1 Pine file, 3 documentation files, 0 dependencies, 0 workflows,
  0 generated exports;
- CuttingBoard mutation permission: NONE;
- merge permission: NONE — draft PR only, no auto-merge, no agent merge;
- the full mandatory preflight, including confirming that `dwats250/cuttingboard` is not
  the writable repository and that the pinned SHA resolves;
- every required implementation, visibility, strategy-behavior, parity-case, and validation
  clause;
- the one-bounded-correction-cycle review limit.

`README.md` remains link-only. The correction does not widen TV-1's writable surface; it
relocates it.

## Required TV-1 handoff

**The TV-1 implementer must read this record before editing any file**, and must confirm in
its preflight report that it has done so. The handoff packet is exactly:

1. the four frozen TV-0 documents, at the hashes recorded above (or their post-TV-0R
   frozen replacements, re-hashed here);
2. the accepted TV-0R review disposition;
3. this installation record.

TV-0R's raw findings are not part of the implementer's task. The implementer receives the
frozen documents and the accepted disposition — not an invitation to reinterpret them.

A TV-1 session that has not read this record will resolve `Allowed files` to repository-root
paths and write outside the audit folder. That is a boundary violation, not a path typo.

## Declared deviations from the primary charge's preferred tree

Each was approved by Dustin during the organization pass.

1. **No `docs/REPOSITORY_ORGANIZATION.md`.** The charge made this conditional on recon
   finding no existing document that already serves the purpose. `README.md` (`## Layout`)
   and `docs/conventions.md` §a already do. Both were extended instead, avoiding a third
   overlapping document that would drift.

2. **`pine/`, `parity/`, `scripts/`, `data/raw/`, `data/normalized/`, and `data/manifests/`
   were not created.** The charge forbids empty placeholder directories without a README or
   tracked manifest giving them current purpose. TV-1 creates `pine/` when it has content
   for it; the `data/` subdirectories are specified in `data/README.md` instead.

3. **The SPY ORB study stays at `studies/spy-orb-first-break/`,** not the charge's
   illustrative `studies/spy-orb/`. The existing name is more precise, it is referenced from
   the repository README, and renaming would strand the filename-based audit trail in
   `CHECKSUMS_PRE_REORG.txt`. The charge explicitly permits leaving it in place. Its content
   and provenance are untouched by this packet.

4. **Plain `mv` was used instead of `git mv`.** The bundle files were untracked, so `git mv`
   is not applicable to them. Byte-identity was verified by re-hashing after the move, which
   is a stronger guarantee than rename detection.

## What this packet did not do

No Pine was written. No market data was downloaded or committed. No threshold was tuned. No
frozen TV-0 document was edited. CuttingBoard was not modified. Nothing was merged.
