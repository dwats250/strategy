# Handoff — current state

**As of 2026-10-16. Seam 1 (executable foundation) delivered and awaiting review.**
Branch `lab/restart-2026-10` (worktree `~/Projects/strategy-lab`), based on `study/vwap-lab-2026-08@4780dbf`.

## Done

- Recovery verified: refs, the corpus SHA and rows, raw pages, and the August code and ledger assessed.
  See `RECOVERY_FINDINGS_2026-10-16.md`.
- Lab package `src/stratlab`: data registry and validation, XNYS sessions, Backtesting.py execution
  contract, strategy base, metrics, windows, experiment runner, ledger, HTML report, CLI.
- Engine behaviour demonstrated by 23 hand-checkable tests (`ENGINE_BEHAVIOR.md`). 52 tests in total;
  51 run in CI, and the August parity test is local-only.
- Instagram reel retrieved anonymously and transcribed locally. Rule table and provisional
  interpretation IG-AUSTIN-P0 written.
- VWR family proposal (VWR0 + 4 variants), **PROPOSED**, not run. The machine config refuses real-data
  runs while PROPOSED.
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
6. Proposed one-line §j amendment for model point releases (Opus 5.5 / Fable / Haiku): governance text,
   not made.

## Next (seam 2, after approval)

1. Freeze `VWR_FAMILY_v1.0.md` and `VWR0_EXPERIMENT_v1.0.toml` (status FROZEN) in their own commit.
2. `uv run stratlab run studies/vwap-ema9-2026-10/manifests/VWR0_EXPERIMENT_v1.0.toml`: one run,
   with ledger rows appended.
3. Reconcile: equity against trades, windows against the full run, ambiguous-exit counts, and the
   raw-mask robustness rerun. Write the interpretation in `analysis/`. Stop for review.

## Known gaps

- The report's price-chart y-axis labels clip slightly at phone width. Cosmetic.
- `stratlab report <run_dir>` rebuilds without price-chart bars (they need market data); `run` builds
  the full report.
- No benchmark series (e.g. session-hold SPY) in the report yet.
