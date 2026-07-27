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

Read-only inspection only. Do not fetch, checkout, switch, branch, stash, commit, reset,
merge, rebase, push, modify remotes, or run any command that changes that checkout's Git
metadata or working tree. See `docs/conventions.md` §i.

## Cross-repository isolation

The binding rule is `docs/conventions.md` §i, carried in brief in the root `CLAUDE.md` and
`AGENTS.md`. In short: `dwats250/strategy` is the only repository this audit may mutate;
`dwats250/cuttingboard` — its remote, its PRs and issues, and every local checkout — is a
read-only evidence source and a forbidden mutation target.

Every GitHub or connector mutation must supply its repository target explicitly, and that
target must be exactly `dwats250/strategy`. A missing, inferred, or ambiguous target is a
STOP condition; a CuttingBoard target is a STOP condition outright.

### D-3 disposition — credential capability

`KNOWN RESIDUAL CAPABILITY — GOVERNED BY EXPLICIT DENY RULE`

The observation stands and is not softened: the credentials available in these sessions are
technically capable of writing to `dwats250/cuttingboard`. No technical barrier prevents such
a write.

That capability is now governed by the explicit deny rule in `docs/conventions.md` §i rather
than by procedural convention alone. **Capability is not authorization.** An action is
authorized because a charge permits it, never because the token allowed it to succeed.

This disposition changes no key, token, remote, GitHub setting, or Claude permission setting.
It records the residual capability and binds it. TV-0R reviews whether that binding is
sufficient; it does not reopen whether the capability exists.

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

### Mandatory TV-1 repository preflight

`TV-1-PINE-IMPLEMENTATION.md` is a frozen authority and cannot be amended in place, so this
requirement is imposed here and is binding on the implementer. It **adds to** TV-1's own
mandatory preflight; it replaces none of it.

Before editing any file, a TV-1 session reports:

1. `pwd -P`
2. Resolved Git repository root
3. Exact `origin` URL
4. Current branch and HEAD
5. Working-tree status
6. Sole authorized mutation target: `dwats250/strategy`
7. Forbidden mutation target: `dwats250/cuttingboard`

**If the working repository or remote is not exactly `dwats250/strategy`, STOP.** Do not
switch repositories or branches to make the preflight pass — report the mismatch and wait for
Dustin. This is in addition to TV-1's own requirement to confirm that
`dwats250/cuttingboard` is not the writable repository and that the pinned SHA resolves.

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

---

# Post-TV-0R effective authority

Added: 2026-07-26. Status: `BINDING ONCE THE AMENDMENT PR IS MERGED AND HASHES VERIFY`

Everything above this line is the original installation record and is **unchanged**. The
frozen TV-0 hashes recorded above still verify byte-exact and are not superseded,
re-issued, or replaced by anything in this section.

## Chain of custody

TV-0R was performed substantively by fresh-context GPT-5.6 / Sol **outside this
repository**, and its result was delivered directly to Dustin. No repository review
artifact was created, so `reviews/` holds no TV-0R review output. Dustin adjudicated the
delivered result and authorized a narrow amendment. Claude acted as scribe for that
amendment only and is not the TV-0R reviewer.

Full detail:
[`adjudications/TV-0R-DUSTIN-ADJUDICATION.md`](adjudications/TV-0R-DUSTIN-ADJUDICATION.md).

## Amendment records and hashes

| Path | Role | SHA-256 |
|---|---|---|
| [`adjudications/TV-0R-DUSTIN-ADJUDICATION.md`](adjudications/TV-0R-DUSTIN-ADJUDICATION.md) | Dustin adjudication record | `a0020ae97bfa579a14bb37f22a6d335cc1ad53b57f553b955b31a29c3a50999d` |
| [`spec/TV-0R-LITERAL-RULE-APPENDIX.md`](spec/TV-0R-LITERAL-RULE-APPENDIX.md) | Active narrow implementation clarification — R-01, R-02, R-05, E-04 only | `f01b8d939f99c736449e425ab68d9d39f21e5421fd8d5cd81a8640e0373fb83d` |
| [`spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md`](spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md) | Active narrow interpretation correction — 2022–2026 window only | `dd65f878d35c5db3b109c45eab38e27488390f1550d2cb115e28b3f48a484b36` |

## Precedence

Read in this order. A lower-numbered rule wins only within the gap it is scoped to.

1. **Frozen TV-0 authority governs by default.** The four documents hashed above remain
   intact, unedited, and controlling for everything.
2. **The literal-rule appendix controls the implementation literals of R-01, R-02, R-05,
   and E-04 — and nothing else.** It supplements the frozen matrix for those four gates.
   It silently redefines no other gate, row, classification, variant, or safeguard. Where
   it is silent, `spec/GATE_TRANSLATION_MATRIX.md` governs.
3. **The backtest interpretation amendment controls the naming and interpretation of the
   2022-01-01 – 2026-07-24 period — and nothing else.** It supersedes the frozen protocol
   only to that extent. Every guard condition, window, threshold, export, and acceptance
   criterion in `spec/BACKTEST_PROTOCOL.md` is unchanged.
4. **This installation record remains binding for repository paths only**, per its
   original scope statement. It is not an audit authority and cannot alter a gate formula,
   threshold, classification, variant, safeguard, or review rule.

Where an amendment and a frozen document disagree about anything outside the two
adjudicated gaps, the frozen document governs.

## TV-1 effective-authority manifest

A TV-1 session must read all of the following, and confirm in its preflight report that
it has done so:

| # | Document | Why |
|---|---|---|
| 1 | `README.md` | TV-0 authority |
| 2 | `spec/GATE_TRANSLATION_MATRIX.md` | TV-0 authority — governing matrix |
| 3 | `spec/BACKTEST_PROTOCOL.md` | TV-0 authority — governing protocol |
| 4 | `charges/TV-1-PINE-IMPLEMENTATION.md` | TV-0 authority — the charge itself |
| 5 | `spec/TV-0R-LITERAL-RULE-APPENDIX.md` | Literals for R-01, R-02, R-05, E-04 |
| 6 | `spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md` | 2022–2026 window naming |
| 7 | `adjudications/TV-0R-DUSTIN-ADJUDICATION.md` | Accepted dispositions and amendment scope |
| 8 | This record, in full | Repository-path correction, preflight, and this section |
| 9 | `docs/conventions.md` (§g, §h, §i) and root `CLAUDE.md` / `AGENTS.md` | Standing lab rules and cross-repository isolation |

TV-0R's raw findings are **not** part of the handoff, and the reviewer's own report is
held by Dustin outside this repository. The implementer receives the frozen documents,
the accepted dispositions, and these amendments — not an invitation to reinterpret them.

Every earlier requirement in this record still applies to TV-1 unchanged: the binding
repository-path correction, its scope limit, the change-surface ceiling, the
CuttingBoard-mutation ban, the no-merge rule, and the mandatory repository preflight.

## TV-1 is blocked

**TV-1 must not begin.** It remains blocked until both of the following hold:

1. the amendment pull request carrying this section is **merged** into
   `dwats250/strategy` `main`; and
2. the three amendment-record SHA-256 hashes above are **independently verified** against
   the merged files.

A hash mismatch between what was adjudicated and what a later stage consumes means the
authority drifted, and the later stage stops. See `docs/conventions.md` §h.

## Source pin — unchanged

`dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`, committed
`2026-07-26T01:35:59Z`. Mutation permission: **NONE**. Read only at the pin, read-only
inspection only, never from a local CuttingBoard working tree. Nothing in this amendment
authorizes any CuttingBoard change or back-feed.

---

# Post-TV-1 literal-recovery effective authority

Added: 2026-07-26. Status: `ACTIVE`

Everything above this line — the original installation record and the post-TV-0R
effective-authority section — is **unchanged**. The five frozen TV-0 hashes and the three
TV-0R amendment hashes recorded above still verify byte-exact and are not superseded,
re-issued, or replaced by anything in this section.

## Authorization and chain of custody

A fresh-context source-pin evidence recovery was performed against
`dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518` using immutable
commit-addressed reads only — no clone, no working tree, no branch tip. It recovered the
executable literals for the three gate rows that the frozen matrix classified
`EXACT_FORMULA` / `FORMULA_EXACT_DATA_PROXY` while omitting the literals a translation
requires: **S-02, S-03/S-04, and D-02**. These are the same defect class as accepted TV-0R
finding F-2, for gate rows F-2's remedy did not reach.

**Dustin authorized this documentation-only amendment directly on 2026-07-26.** Unlike the
TV-0R amendments there is no separate adjudication-record document; this section is the
record of the authorization and its scope. Claude acted as scribe for the transcription
only, and is not a reviewer or adjudicator of it.

## Amendment record and hash

| Path | Role | SHA-256 |
|---|---|---|
| [`spec/TV-1-LITERAL-RECOVERY-AMENDMENT.md`](spec/TV-1-LITERAL-RECOVERY-AMENDMENT.md) | Active narrow implementation clarification — S-02, S-03/S-04, D-02 only | `ec56939c65313b1b936892285a3bcb8fcd561fe8ae9c9deaa3d111744b5c3869` |

Verify this hash before consuming the document. A mismatch between what was authorized and
what a later stage consumes means the authority drifted, and the later stage stops. See
`docs/conventions.md` §h.

## Precedence — extends the list above, replaces none of it

The four-item precedence order in *Post-TV-0R effective authority* stands unchanged. This
amendment inserts one further narrow overlay, at the same standing as the TV-0R
literal-rule appendix and scoped as narrowly:

> **The TV-1 literal-recovery amendment controls the implementation literals of S-02,
> S-03/S-04, and D-02 — and nothing else.** It supplements the frozen matrix for those
> three rows. It silently redefines no other gate, row, classification, variant, threshold,
> or safeguard. Where it is silent, `spec/GATE_TRANSLATION_MATRIX.md` governs.

It does not modify, reopen, or overlap `spec/TV-0R-LITERAL-RULE-APPENDIX.md`, whose scope
remains exactly R-01, R-02, R-05 and E-04. Where this amendment and a frozen document
disagree about anything outside the three adjudicated rows, the frozen document governs.

## TV-1 effective-authority manifest — item 10

The nine-item manifest above is unchanged and still binding in full. One document is added
to it:

| # | Document | Why |
|---|---|---|
| 10 | `spec/TV-1-LITERAL-RECOVERY-AMENDMENT.md` | Literals for S-02, S-03/S-04, D-02 |

Any session consuming the TV-1 effective authority must read all ten documents and confirm
in its preflight report that it has done so.

## Scope limit

This section registers one document and records its hash. It is not an audit authority in
its own right, and — like the rest of this record — it cannot alter a gate formula,
threshold, classification, variant, safeguard, or review rule.

It changes no TV-1 or TV-1R status. It does not correct, endorse, or invalidate the held
pre-parity implementation checkpoint, authorize a merge or a pull request, lift any review
requirement, or authorize compilation, a chart run, or TV-2. Checking any implementation
against these literals remains TV-2's task under the frozen contract.

## Source pin — still unchanged

`dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`, committed
`2026-07-26T01:35:59Z`. Mutation permission: **NONE**. CuttingBoard was read only at the
pin, through immutable commit-addressed reads, and was not modified in any way. Nothing in
this amendment authorizes any CuttingBoard change or back-feed.
