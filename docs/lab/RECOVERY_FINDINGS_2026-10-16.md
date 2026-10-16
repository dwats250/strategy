# Recovery findings — 2026-10-16

## Repository state verified before acting

| Item | Observed |
|---|---|
| Remote | `https://github.com/dwats250/strategy.git` |
| `main` | `1aefaaab53d907b5452939f4a26c5eb69aa45961`, matching the previously observed value |
| `study/vwap-lab-2026-08` | `4780dbff88d9d9a49c73b3cd821f39a4475238f0`, matching; 31 ahead of main, 0 behind |
| Local unpushed commits | none on any tracked branch. `tv1/validation-v0.1` (e298ba2) and `docs/agent-lanes-section-j` have no upstream and are older, already-dispositioned lines; both were left untouched. |
| Working tree | Only an untracked `studies/vwap-lab-2026-08/analysis/__pycache__/` (bytecode, not unique work). Left in place. |
| Other remote refs | Open PR #19 (`docs/section-j-assigned-decisions`, a §j amendment); new `exploratory/portfolio-strategy-collab-2026` (d32bf6f, 2026-10-13). Both untouched. |
| Work location | New branch `lab/restart-2026-10` from `4780dbf`, in a separate worktree `../strategy-lab`. The main checkout was not switched. |

The branch is based on the August tip, not on `main`. The lab reuses that study's corpus by identity
and its parity reference, and the August records exist only on that branch. Merging the lab without
them would leave its provenance pointing at unmerged files. The PR therefore also carries the 31
August commits.

## Original corpus

`~/Projects/strategy/studies/vwap-lab-2026-08/data/cache/canonical/SPY_1m_2024-09-01_2026-08-22.csv.gz`
is **present and verified**: SHA-256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`
and 422,657 rows (422,658 lines including the header), matching the record. The capture manifest and
all 9 raw provider pages are also present, and their SHA-256s match the manifest. Copies of all of it
are now in the local lab store (`~/.local/share/stratlab/datasets/`). See `DATA_BACKUP_RECOVERY.md`.

Trade-blind validation of the corpus (`stratlab data validate`):

- 494/494 XNYS sessions present; 0 duplicates; 0 OHLC violations.
- Every session's first RTH minute is 09:30 ET (325 sessions open at 13:30 UTC, 169 at 14:30 UTC). DST is handled.
- 5 early closes, all 210 RTH minutes ending 12:59. 489 full sessions of 390 minutes. No missing RTH minutes in the raw file; the mask removes 9.
- 9 one-minute moves above 1% close-to-close, all real: 2025-04-07 and 2025-04-09, the tariff sessions.
- Last session 2026-08-21, which is 56 days stale on 2026-10-16.
- Adjustment: `adjusted=true` was requested, which means split-adjusted. Dividend adjustment is **unverified**, and no splits occurred in range.

## What was reused, and why

| Reused | Where now | Why it earned its place |
|---|---|---|
| Corpus and its identity record | `datasets/REGISTRY.json` + local store | Verified, deterministic capture with raw pages |
| Integrity mask v1.0 (9 bars) | Applied as a declared run option | Pre-registered and trade-blind. It matters more now because stops are evaluated on 1-minute bars. |
| Session VWAP / Pine-style EMA semantics | `src/stratlab/indicators.py` | Re-implemented in pandas and **proved equal** to the August `parity_foundation` on all 38,352 5m bars (489×78 + 5×42) (|Δ| ≤ 1e-9; `tests/test_parity_august.py`, local only) |
| Capture approach (`fetch_spy_aggs.py`) | Kept in place; referenced for the next download | Works and is credential-gated. It needs a ticker parameter and a new dataset id per download. |
| Ideas: outlier concentration, bootstrap labelling, frozen-threshold discipline | `metrics.concentration`, conventions | Sound practice |

## What was not reused, and why

| Not reused | Reason |
|---|---|
| `fastalpha_engine.simulate` | FastAlpha-specific (hard-coded EMA 9/20, ATR 14, 15:50 EOD bar). It silently drops positions open at window end. Replaced by Backtesting.py plus a tested execution contract. |
| August 5m bar builder | Keeps a 1-minute 13:00 closing-auction bucket on half-days. TradingView has no such bar (verified against the preserved TV export), and it produced one phantom trade in the August dev window (2025-11-28 13:00 → filled 2025-12-01 09:30). The lab's calendar-based builder excludes it. |
| `tearsheet.py` | Trade-based only. Its "Sharpe" is a per-trade ratio scaled by √(trades/year); it is labelled as such, so this is not a misuse, but it is not a portfolio metric. Output is JSON/SVG, not interactive. |
| MIM/ODR accounting | Re-implemented their own accounting outside the engine (~90 duplicated lines). This is the pattern the lab exists to prevent. |
| `v0_calibration.py` conclusions | Its disposition strings are hard-coded text, not computed. Not treated as evidence. |
| Fixed-clock EOD (15:50 bar) | Never fires on half-days. Replaced by calendar-driven flatten. |

## Historical results and their status (preserved, not rewritten)

From `studies/vwap-lab-2026-08/LEDGER.csv`: 20 data rows. 19 are development rows (VDC 16, FPC 1,
MIM 1, ODR 1). One of them (R1) is sealed and uninterpreted, which leaves **18 interpreted development
draws** (VDC 15, FPC 1, MIM 1, ODR 1) over **17 distinct configurations** (R0, R1 and the PVAE unseal share
one). There was 1 validation look and 0 holdout draws.
Terminal dispositions: the VDC/continuation lane found **no edge** (VDC kept as a benchmark); long-only
**failed validation**; FPC was **worse**; MIM and ODR were **family dead**; VMR was design only.

None is re-proposed. The VWR family is a different rule set (touch-and-reclaim, not opposing-candle
continuation), but it shares the VWAP/EMA9 idea space and the same data. That is why its results are
labelled exploratory.

Record defects found during recovery (all in frozen August records; **not edited**, listed for the
record):

- The ledger's R0 row has 26 fields against a 27-field header (the `script_file` column is missing, so
  columns 15+ are shifted).
- `trials_planned` holds family budget ceilings, not committed configuration counts.
- The validation look ran on the local engine although `PARITY_GATES.md` says no local result may
  substitute for TradingView evidence until every gate closes.
- The tearsheet manifest's test-file hash and test count are stale (12 tests, not 11; hash `3790b6…`
  against the recorded `07c4a1…`).
- The capture manifest is gitignored even though the data README says it is committed.

## Lane declaration (conventions §j)

- **Lane 1 (orchestrator, Opus 5.5):** every repository write, git operation and synthesis.
- **Lane 3 (mechanical, Haiku):** five read-only readers with non-overlapping scopes (engine, data,
  tearsheet, ledger/records, families). No repository writes; their claims were spot-checked.
- **Lane 2 (review, Fable):** one skeptic per reader scope during recovery, and one independent
  review of the seam-1 packet (4 dimensions, each finding put to a separate refuter): 24 findings, all
  confirmed, and all addressed in one correction cycle. The raw outputs are committed in
  `docs/lab/reviews/` (`RECOVERY_RECON_2026-10-16.json`, `SEAM1_LANE2_REVIEW_2026-10-16.json`).
- **Model-version drift (a §j stop condition, reported, not resolved here):** §j's table names Opus 5,
  Fable 5 and Haiku 4.5. This session ran Opus 5.5, and the available Fable and Haiku models are newer
  point releases. The roles match. Read literally, though, "a lane assigned differently from the table"
  is a §j stop condition. I proceeded because Dustin's charge for this session explicitly directs the
  work and the roles are unchanged. **Dustin's call:** adopt the one-line dated amendment §j itself
  provides for model releases. It is drafted in `HANDOFF.md` and not committed to `conventions.md`,
  because governance text is outside this charge.
