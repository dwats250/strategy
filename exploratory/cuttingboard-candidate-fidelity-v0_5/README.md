# CuttingBoard Candidate Fidelity v0.5 — Exploratory Lineage Packet

**Status: EXPLORATORY LINEAGE — NOT A STUDY, NOT THE FROZEN AS-IS PROXY RUN.**

## What this is

This directory preserves the exploratory CuttingBoard "candidate fidelity" line of Pine
development — v0 → v0.3 → v0.4 → v0.5 — which was developed **outside** the repository's
governed studies, prior to execution of the frozen `studies/cuttingboard-asis-proxy/` baseline.

It is retained as **diagnostic lineage and regression reference only**.

## What this is not

This packet must never be cited as:

- an official run of `studies/cuttingboard-asis-proxy/`;
- an amendment to, or a reopening of, the closed CuttingBoard engine audit;
- evidence of profitability, edge, or strategy performance.

No artifact here was produced under a pre-registered manifest. No artifact here carries
study-grade provenance. The evidence boundary of this directory is: *these files existed, in
this form, with these hashes, at the stated capture dates.* Nothing beyond that is established.

## Key semantic finding preserved here

The v0.5 strategy required **both** the ATR-floor check and the extension check to pass — a hard
`AND` — before a bar could surface as a candidate.

Documented CuttingBoard semantics treat the representable Gates 5–11 as **soft gates**:

| Gate misses | Disposition |
|---|---|
| 0 | QUALIFIED |
| 1 | WATCHLIST |
| 2 or more | REJECT |

Under hard-`AND` behaviour, v0.5 therefore **under-surfaces 239 potential single-miss WATCHLIST
candidates** across the captured window.

The authoritative statement of this finding, and of everything else v0.5 established, is
`EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md` in this directory. Where this README and that record
differ, that record governs.

## Layout

```
EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md
CBF05_CHECKPOINT_POSTURE_PATCH_COMPARISON.md
scripts/
exports/
execution/
handoff/
```

### Root records

- **`EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md`** — lineage record; authoritative summary of what
  v0.5 established.
- **`CBF05_CHECKPOINT_POSTURE_PATCH_COMPARISON.md`** — checkpoint record comparing the pre-patch
  (confidence ≥ 0.50) and post-patch (confidence ≥ 0.55) exports.

### `scripts/`

Retired versions are retained per `docs/conventions.md` §c.

- `cuttingboard_core_spy_strategy.pine` — v0 baseline
- `cuttingboard_core_spy_strategy_v0_3.pine`
- `cuttingboard_direct_path_ladder_v0_4.pine`
- `cuttingboard_direct_path_fidelity_v0_5.pine`
  — SHA-256 `3136a812c285878d416490f25dfbb62110fb39a863e47b34ef23b495d1b75726`

### `exports/`

| File | Notes |
|---|---|
| `CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv` | Canonical. Pre-patch. 3,173 rows. SHA-256 `e28aa87468d1922500b119bf02ded470c5528d327edf0bf09d2f124b1448ab8b` |
| `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-prepatch-c050.csv` | Byte-identical to canonical; retained because the checkpoint record pins this filename |
| `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-postpatch-c055.csv` | SHA-256 `2d375b4c1b60671012e834bd093057cdd0c964fee7a09c031e635c1eec5065e9` |

### `execution/`

Strategy Tester artifacts. **Execution artifacts are not candidate-gate counts** and must not be
read as such.

- `CB_Fidelity_v0.5_AMEX_SPY_1D_2015-01-01_to_2026-07-28_V4_capture-2026-07-29.csv` — 95 trades
- `CBF05_SPY1D_V4_2015-20260728_strategy.xlsx` — known margin-call contamination
- `CB_Ladder_v0.4_BATS_SPY1D_trades_2015-2026_V0..V4_capture-2026-07-28.csv` — five files, the
  v0.4 gate-ladder rungs V0 through V4

### `handoff/`

Provenance of how this packet arrived in the repository:

- `ARTIFACT_DISPOSITION.md`
- `CLAUDE_TECHNICAL_ONBOARDING.md`
- `ARTIFACT_DISPOSITION_AMENDMENT_2026-07-30.md` — dated amendment

## Known provenance gaps

Recorded, not fixable retroactively:

- No chart or table screenshot accompanies any v0.5 capture.
- No full TradingView session/provider record exists for the v0.5 captures.

These gaps are a further reason this lineage cannot be promoted to study-grade evidence.

## Next step

The authorized next action is execution of the frozen `studies/cuttingboard-asis-proxy/` v0.1
baseline under its pre-registered run manifest. **Nothing in this directory feeds into, informs,
or modifies that run.**
