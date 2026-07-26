# Primary Charge — Strategy Repository Organization and CuttingBoard Audit Scaffold

Status: READY FOR CLAUDE CODE PLAN MODE

Prepared: 2026-07-26 UTC

## Session role

Use Claude Code with Opus 5 as the primary planner and orchestrator.

Begin in **Plan Mode**. The first pass is read-only reconnaissance and planning.
Do not edit, move, commit, push, invoke an implementation agent, or open a pull
request until Dustin has reviewed and approved the plan.

After approval, the same session may execute the approved bounded plan if its
repository state and source assumptions remain unchanged. If they changed,
repeat preflight and report the difference before editing.

## Repositories and authority

### Writable repository

- Repository: Dustin's existing `strategy` repository
- Exact remote, branch, and starting SHA: resolve during preflight
- Merge permission: NONE
- Auto-merge permission: NONE

### Read-only source repository

- Repository: `dwats250/cuttingboard`
- Immutable audit snapshot:
  `59f8279d796335149afdec4aa507b6f927233518`
- Mutation permission: NONE

CuttingBoard is evidence only. This project is an external historical audit,
not a CuttingBoard feature, PRD, migration, or backtesting subsystem.

No result, parameter, threshold, code, or conclusion may feed back into
CuttingBoard. Any future CuttingBoard refactoring must be commissioned through
a separate, independent review and an explicit CuttingBoard decision. Backtest
performance alone cannot authorize an engine change.

## Materials supplied with this charge

Read these four documents completely:

1. `README.md`
2. `spec/GATE_TRANSLATION_MATRIX.md`
3. `spec/BACKTEST_PROTOCOL.md`
4. `charges/TV-1-PINE-IMPLEMENTATION.md`

They constitute the commissioned TV-0 package. They are not assumed perfect:
they must pass the independent TV-0R semantic review before Pine
implementation begins.

## Primary objective

Prepare the existing `strategy` repository to support:

1. The CuttingBoard engine strategy audit as a self-contained audit folder.
2. The existing SPY ORB study and future independent studies without mixing
   their data, claims, specifications, or results.
3. Reproducible TradingView/Pine experiments in the preliminary round.
4. A later offline-data and Python-backtesting phase.
5. Clear provenance, run manifests, review records, and separation between raw
   data, normalized data, derived results, specifications, and implementation.

The repository should become easier to extend without inventing unnecessary
frameworks, shared abstractions, or empty process layers.

## Economic-depth rule

Pull as much evidence as is reasonably useful while remaining effective and
economic in time and depth.

Apply this rule concretely:

- Inventory the entire repository shallowly.
- Read repository governance, indexes, active study specifications, and files
  that determine current organization deeply.
- Inspect representative manifests, scripts, results, and data conventions.
- Do not exhaustively read every historical result, generated file, large
  dataset, or redundant export unless it affects a proposed move or contract.
- Stop reconnaissance when the evidence is sufficient to propose a safe,
  coherent organization and identify material conflicts.
- Record uncertainty instead of extending the probe indefinitely.
- No recursive review loops. Each independent review receives at most one
  bounded correction pass.

## Mandatory read-only preflight

Report:

1. Repository name and remote.
2. Current branch and full starting SHA.
3. Working-tree state, including untracked files.
4. Existing top-level tree and study/audit layout.
5. Current location and status of the SPY ORB study.
6. Existing repository instructions, `CLAUDE.md`, `AGENTS.md`, README, indexes,
   manifests, ignore rules, and naming conventions.
7. Whether any existing files collide with the proposed CuttingBoard audit
   paths.
8. Whether the pinned CuttingBoard commit resolves and remains read-only.
9. Whether the four supplied TV-0 documents are byte-identical to any versions
   already present.
10. Any user-owned or unrelated changes that constrain reorganization.

STOP if:

- the wrong repository is open;
- the writable repository is CuttingBoard;
- the working tree is not clean and the changes could overlap this work;
- the pinned CuttingBoard commit cannot be resolved;
- repository instructions conflict with this charge;
- a destructive move, deletion, or history rewrite appears necessary; or
- the requested organization would overwrite an existing study or authority.

Do not switch branches, reset, stash, delete, or overwrite without Dustin's
explicit authorization.

## Plan-mode deliverable

Return one decision-ready plan containing:

1. **Current-state inventory**
   - Existing studies, audits, data areas, scripts, and documentation.
   - Active versus archival or ambiguous material.
   - Current strengths and concrete organization problems.

2. **Proposed repository tree**
   - Show the complete relevant target tree.
   - Prefer the target structure below, but adapt it to existing repository
     conventions when the evidence supports a better fit.
   - Explain every deviation.

3. **Move/create/update table**
   - Exact source path.
   - Exact destination path.
   - Operation: `MOVE`, `CREATE`, `UPDATE`, or `LEAVE`.
   - Reason.
   - References that must be repaired.

4. **Authority and lifecycle map**
   - Which files are authoritative specifications.
   - Which are exploratory notes.
   - Which are implementation charges.
   - Which are review outputs.
   - Which are run-specific evidence.

5. **Independent-review sequence**
   - TV-0R semantic review before Pine implementation.
   - TV-1R implementation review after Pine compiles and parity evidence exists.
   - Fresh context and strict separation between implementation and review.

6. **Validation plan**
   - Link checks.
   - Expected file set.
   - Git diff boundaries.
   - Existing study preservation.
   - No CuttingBoard mutation.

7. **Commit and PR plan**
   - Prefer one organizational/scaffold commit if the moves are mechanical and
     reviewable.
   - Split the work only if existing repository complexity makes a single
     commit unsafe.
   - Draft PR and manual merge only.

8. **Questions and stop conditions**
   - Ask only questions that materially change the plan.
   - Do not ask Dustin to choose between equivalent mechanical details.

Do not implement from Plan Mode. End with:

`HELD FOR DUSTIN PLAN APPROVAL`

## Preferred target organization

This is the preferred shape, not permission to overwrite existing paths:

```text
strategy/
├── README.md
├── docs/
│   └── REPOSITORY_ORGANIZATION.md
├── studies/
│   └── spy-orb/
└── audits/
    └── cuttingboard-engine-strategy-audit/
        ├── README.md
        ├── spec/
        │   ├── GATE_TRANSLATION_MATRIX.md
        │   ├── BACKTEST_PROTOCOL.md
        │   └── DATA_PROVENANCE_CONTRACT.md
        ├── charges/
        │   ├── TV-0R-INDEPENDENT-REVIEW.md
        │   ├── TV-1-PINE-IMPLEMENTATION.md
        │   └── TV-1R-PINE-SEMANTIC-REVIEW.md
        ├── reviews/
        ├── pine/
        ├── parity/
        ├── scripts/
        ├── data/
        │   ├── README.md
        │   ├── raw/
        │   ├── normalized/
        │   └── manifests/
        └── runs/
            └── README.md
```

Guidance:

- Do not create a `shared/` framework until two real studies require the same
  stable component.
- Preserve the SPY ORB study's content and provenance.
- Use `git mv` for approved moves.
- Update internal links and indexes in the same commit as their move.
- Never delete raw research or results merely to make the tree tidy.
- If moving the SPY ORB study would cause significant reference breakage,
  leave it in place during this preliminary round and document the intended
  migration instead.
- Avoid empty placeholder directories unless an explanatory README or tracked
  manifest contract gives them current purpose.

## Preliminary-round scope

The preliminary round consists of:

1. Repository organization/scaffold.
2. Installation of the four TV-0 documents.
3. A draft data-provenance contract.
4. TV-0R independent semantic review.
5. One bounded adjudication/correction/freeze pass.
6. TV-1 Pine implementation.
7. TradingView compilation and bounded parity work.
8. TV-1R independent semantic review.
9. Frozen TradingView evaluation and export preservation.

The preliminary round does **not** include:

- an offline Python backtester;
- bulk market-data acquisition;
- provider abstraction;
- data-vendor selection as a permanent architecture decision;
- live broker connectivity;
- alerts-to-orders or automated execution;
- option-chain return simulation;
- parameter optimization;
- CuttingBoard refactoring;
- automatic parameter or code transfer into CuttingBoard.

## Offline CSV/data status

Offline CSV and external historical-data work is **exploratory** during the
preliminary round and is the next major focus after the TradingView audit.

Create `spec/DATA_PROVENANCE_CONTRACT.md` with status:

`DRAFT / EXPLORATORY — FROZEN IMPLEMENTATION NOT AUTHORIZED`

It should define, without downloading data or choosing a permanent provider:

- required provenance fields;
- source and retrieval timestamp;
- vendor symbol and canonical symbol;
- timeframe, timezone, exchange session, and calendar;
- raw versus adjusted OHLCV semantics;
- split and dividend treatment;
- missing-bar and duplicate-bar policy;
- date range and row count;
- file checksum;
- immutable raw-data handling;
- normalized schema expectations;
- TradingView chart-data and Strategy Report export roles;
- redistribution/licensing caution;
- trade-by-trade parity requirements;
- discrepancy logging;
- the future sequence: TradingView parity, offline normalization, bounded
  reproduction, then expanded historical testing.

Create `data/README.md` to state:

- raw vendor exports are private/untracked unless their redistribution rights
  are known;
- manifests, checksums, schemas, acquisition code, and permitted derived
  results may be tracked;
- raw files must never be silently edited;
- normalized files must point back to an immutable raw manifest;
- no download or acquisition script is authorized in this packet.

Add or refine narrow ignore rules only after inspecting existing repository
conventions. Do not blanket-ignore all CSV files if the repository already
tracks small fixtures or permitted result tables.

Offline implementation begins only after the preliminary TradingView round
reaches a recorded stopping point. It should receive its own future charge,
likely TV-4.

## TV-0R — Independent semantic review

TV-0R is a separate fresh-context Sol/GPT-5.6 review. Opus may prepare the
charge and assemble inputs, but it may not impersonate the reviewer or edit
the documents during review.

### Inputs

- The four commissioned TV-0 documents.
- The pinned CuttingBoard SHA.
- Read-only access to the pinned CuttingBoard source.
- The draft data-provenance contract only for boundary/provenance review.
- No performance results.

### Review questions

1. Is the gate inventory complete for the declared direct-path scope?
2. Does each formula, threshold, comparison operator, priority rule, and
   missing-data behavior match pinned source?
3. Are `EXACT`, `PROXY`, `INERT`, `EXCLUDED`, and `DEFERRED` classifications
   defensible?
4. Are the seven semantic hypotheses properly derived and testable?
5. Are completed-bar, next-open, session, adjustment, and cross-symbol
   assumptions explicit and honest?
6. Can the proposed Pine implementation repaint, leak future data, or
   accidentally treat unavailable gates as passing?
7. Do the incremental variants isolate gate-family effects without changing
   thresholds?
8. Are the required exports sufficient for later offline reproduction?
9. Does any language overclaim CuttingBoard parity, options profitability, or
   future performance?
10. Does the separation from CuttingBoard prevent back-feeding?

### Output contract

Each finding must be:

- `BLOCKING`
- `NON-BLOCKING`
- `QUESTION`

Each finding must include:

- exact document location;
- exact pinned-source evidence where applicable;
- consequence;
- smallest sufficient correction.

The reviewer may not:

- edit files;
- write Pine;
- tune thresholds;
- propose CuttingBoard refactoring;
- expand the audit beyond the declared direct path;
- review performance; or
- begin a review of its own review.

After review, Opus prepares one adjudication table. Dustin approves the
dispositions. Apply at most one bounded correction pass, record the reviewed
document hashes, and freeze TV-0 for TV-1.

## TV-1 execution

After TV-0R acceptance, execute the existing
`charges/TV-1-PINE-IMPLEMENTATION.md` unchanged except for repository-path
corrections approved during organization.

Do not fold TV-0R into the TV-1 implementer's task. The implementer receives
the frozen documents and accepted review disposition, not an invitation to
reinterpret them.

## TV-1R — Independent Pine semantic review

TV-1R is a second fresh-context Sol/GPT-5.6 review after:

- Pine v6 compiles;
- the script loads on a standard SPY daily chart;
- named gates and variants are present;
- parity fixtures and known proxy exceptions are recorded; and
- the implementation SHA is frozen for review.

TV-1R reviews implementation fidelity, temporal safety, missing-data handling,
variant isolation, export visibility, and compliance with the frozen contract.
It does not optimize performance or redesign the strategy.

Use the same finding taxonomy and one-correction-cycle limit as TV-0R.

## Execution authorization after plan approval

Once Dustin explicitly approves the Plan Mode output, execution may:

- create the approved branch;
- perform the approved mechanical reorganization;
- install and link the four TV-0 documents;
- create the two independent-review charge files;
- create the draft data-provenance contract and data README;
- update the repository index and organization documentation;
- validate links and file boundaries;
- create one intentional commit;
- push once; and
- open a draft PR.

Execution may not:

- invoke TV-0R before the scaffold PR state and document inputs are stable;
- implement Pine in the organization/scaffold packet;
- download or commit market data;
- mutate CuttingBoard;
- merge any PR; or
- broaden into unrelated repository cleanup.

Final execution state:

`DRAFT PR — HELD FOR DUSTIN MERGE`

## Required final report

Report:

1. Starting and ending branch/SHA.
2. Exact moves, creates, and updates.
3. Validation performed and results.
4. Any existing study intentionally left in place and why.
5. Current lifecycle state of TV-0, TV-0R, TV-1, TV-1R, and future TV-4.
6. Known questions or limitations.
7. Commit and draft PR links.
8. Confirmation that CuttingBoard was not modified and no implementation,
   data acquisition, optimization, or merge occurred.

