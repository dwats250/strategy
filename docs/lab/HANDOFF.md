# Handoff — current state

**As of 2026-10-16. Seam 1 (executable foundation) delivered and awaiting review.**
Branch `lab/restart-2026-10` (worktree `~/Projects/strategy-lab`), based on `study/vwap-lab-2026-08@4780dbf`.

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
