# Handoff — current state

**As of 2026-10-16. Seam 2 (first real experiment) delivered and awaiting review.** PR #20 is open and
unmerged. Branch `lab/restart-2026-10` (worktree `~/Projects/strategy-lab`).

## Seam 2 — done

- Owner amendments 1–7 implemented and tested (68 tests; 67 in CI). They are recorded in
  `studies/vwap-ema9-2026-10/manifests/VWR_FAMILY_v1.0.md`. The §j model-release amendment is committed to
  `docs/conventions.md`.
- Pre-freeze lane-2 review: 14 findings, 13 confirmed and fixed. Code pinned at `6d25dd1`, tree
  `393e0ab9…`. Frozen in `1f4af3a`: `VWR0_EXPERIMENT_v1.1.toml` and `VWR0_RAW_ROBUSTNESS_v1.1.toml`. The
  v1.0 TOMLs carry a placeholder hash and were never run (see the dated amendment).
- Each config was run once: `VWR0-EXP__20261016T211249Z` and `VWR0-RAW__20261016T211405Z`. There are 8
  ledger rows. Reconciliation passed 56/56, and the non-exported determinism rerun matched 99/99 files byte
  for byte.
- Findings: `studies/vwap-ema9-2026-10/analysis/VWR0_EXP_FINDINGS_2026-10-16.md`. All seven trials are
  negative and below the SPY session-hold benchmark. A post-run data defect on 2025-04-23 (an unmasked
  off-market wick cluster) inflates VWR0, VWR1 and VWR3 losses without changing any sign. A lane-2
  fact-check confirmed 130 numeric claims; its 6 issues are fixed.
- Annotated report: `exports/runs/VWR0-EXP__20261016T211249Z/report_rebuild_20261016T212214Z.html`. The
  run's own `report.html` is the unannotated original.

## Waiting on Dustin (seam-2 review)

1. Accept the seam-2 findings, or ask for changes.
2. Decide on a trade-blind integrity mask v2 (findings, "Decision for Dustin"). It would be a new frozen
   data treatment plus a separately ledgered rerun. Nothing is done without your approval.
3. Seam 3 (a structurally different strategy through the same workflow) when you are ready.

## Report v2 (presentation only) — 2026-10-16

- `exports/runs/VWR0-EXP__20261016T211249Z/report_v2_20261016T223632Z.html` has four views: Summary,
  Compare, Inspect trades and Technical details. It was built by `stratlab report --from-report` from
  the committed `report_rebuild_20261016T212214Z.html`.
- How the data was verified: the payload was regenerated with the pinned `build_report`, after
  asserting that 12 computation modules are byte-identical to `1f4af3a`. It matched in 942,917 values.
  Nothing was recomputed for display.
- `report.html` and `report_rebuild_…html` are unchanged. The presentation code is at `680aa26`.
- Lane-2 review: 16 confirmed findings, all addressed (`docs/lab/reviews/REPORT_V2_LANE2_REVIEW_2026-10-16.json`).
  Two of them dropped three previously saved but never-displayed fields (gross P&L, average R of
  added/removed trades) to honour "no new metrics". Both remain in `metrics.json` and the findings note.
- **Waiting on Dustin:** a quick visual review.

## Fresh data — captured 2026-10-16 (not yet used by any experiment)

- Entitlement probed by behaviour. Minute data is available 2024-10-16 → 2026-10-15; 2024-10-15 and
  today (2026-10-16) return HTTP 403, so the plan has a two-year window and no same-day data.
- New dataset `spy-1m-polygon-20241016-20261015-cap20261016-729dc4e9`: 431,355 rows, SHA-256 `729dc4e9…`,
  data through 2026-10-15, the latest completed session the plan serves. It validates clean: 501/501
  sessions, no missing minutes, DST and early closes correct
  (`docs/lab/DATA_VALIDATION_spy-1m-729dc4e9_raw_2026-10-16.json`).
- **The original corpus is preserved** (`a4afaa70…`, unchanged). Over their overlap (2024-10-16 →
  2026-08-21) the two captures are **identical in all 179,670 RTH minutes**, so the vendor revised nothing
  and the 2025-04-23 off-market wick cluster is in the vendor's current data
  (`docs/lab/DATA_COMPARE_a4afaa70_vs_729dc4e9_2026-10-16.json`). The new weeks (2026-08-24 → 2026-10-15)
  show 2 flagged minutes on 2026-08-28.
- Mask v1.0 is bound to the August corpus's SHA, so it cannot be applied to the new dataset as is.
  Using the new data in an experiment needs a decision on its data treatment (it ties into the mask-v2
  question) and a new frozen config.

## Outstanding (non-blocking)

- **Off-device backup:** copy `~/.local/share/stratlab/` (now about 107 MB) off this disk
  (`DATA_BACKUP_RECOVERY.md`).

---

# Seam 1 record (historical)

## Done

- Recovery verified: refs, the corpus SHA and rows, raw pages, and the August code and ledger assessed.
  See `RECOVERY_FINDINGS_2026-10-16.md`.
- Lab package `src/stratlab`: data registry and validation, XNYS sessions, Backtesting.py execution
  contract, strategy base, metrics, windows, experiment runner, ledger, HTML report, CLI.
- Engine behaviour demonstrated by 25 hand-checkable tests (`ENGINE_BEHAVIOR.md`). 61 tests in total;
  60 run in CI, and the August parity test is local-only.
- Lane-2 review of seam 1: 24 findings, all confirmed by a separate refuter, all addressed in one
  correction cycle (`docs/lab/reviews/`). Real-data runs now require `status = "FROZEN"` plus a matching
  pinned code-tree hash and a clean `src/`.
- Instagram reel retrieved anonymously and transcribed locally. Rule table and provisional
  interpretation IG-AUSTIN-P0 written.
- VWR family proposal (VWR0 + 4 variants) and the pre-committed raw-corpus robustness rerun:
  **PROPOSED**, not run. N = 7 trials; chance-maximum Sharpe ≈ 1.00 annualized.
- Synthetic demo report (`uv run stratlab demo`).

## Waiting on Dustin (seam-1 review)

1. Approve or amend the IG-AUSTIN-P0 assumptions (`SOURCE_RULES_IG_AUSTIN_v0.1.md`, "Material
   ambiguities"): underlying, exit rule, stop, and whether an anticipatory P1 is wanted.
2. Approve or amend the VWR baseline and variants (`VWR_FAMILY_PROPOSAL_v0.1.md`), plus sizing (1×
   notional) and costs ($0.0135/share/side).
3. Mask decision: apply v1.0 (proposed), with a raw-corpus robustness rerun of VWR0.
4. **Data freshness:** set `MASSIVE_API_KEY` (or `POLYGON_API_KEY`) if an October-current window is
   wanted. That creates a new dataset id; the old corpus stays as is.
5. **Backup:** copy `~/.local/share/stratlab/` off this disk (`DATA_BACKUP_RECOVERY.md`).
6. **§j stop condition, needs your decision.** The model point releases differ from §j's table. The
   roles are unchanged, but read literally it is a model-role conflict. Proposed one-line amendment, not
   committed:
   > *Amendment 2026-10-16 — model point releases.* Lane bindings name a model family. A point release
   > of the bound family (e.g. Opus 5.5, Fable 5.1, Haiku 5.5) fills the same lane without further
   > amendment; a change of family requires one.
7. IG first-bar cross: exclude (current default) or include (`SOURCE_RULES_IG_AUSTIN_v0.1.md`, item 4).

## Next (seam 2, after approval)

1. Apply any review amendments to code, then commit. Run `uv run stratlab identity` and copy
   `code_tree_sha256` into the v1.0 TOMLs.
2. Freeze `VWR_FAMILY_v1.0.md`, `VWR0_EXPERIMENT_v1.0.toml` and `VWR0_RAW_ROBUSTNESS_v1.0.toml`
   (`status = "FROZEN"`) in their own commit, before any run.
3. `uv run stratlab run …/VWR0_EXPERIMENT_v1.0.toml` and `uv run stratlab run …/VWR0_RAW_ROBUSTNESS_v1.0.toml`:
   one run each, with ledger rows appended.
4. Reconcile: equity against trades, windows against the full run, ambiguous-exit counts, and the
   raw-mask robustness difference. Write the interpretation in `analysis/`. Stop for review.

## Known gaps

- `stratlab report <run_dir>` writes a new `report_rebuild_<UTC>.html` (it never overwrites) without
  price-chart bars, which need market data. `run` builds the full report.
- The report embeds its data gzip+base64 and inflates it with the browser's `DecompressionStream`
  (Chrome 80+, Safari 16.4+, Firefox 113+).
- No benchmark series (e.g. session-hold SPY) in the report yet.
