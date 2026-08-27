# PREP — MIM-0 first development run · v0.1 · 2026-08-27 · NOT RUN (BLOCKED — C)

Run manifest for the first MIM development configuration (MIM-0). Under the family
autonomy protocol the baseline would be run here — but outcome access is a
**DATA/SEMANTIC BLOCKER (status C)** on the previous-close dividend issue, so the
development regression and economics are **not** executed. MIM-0 is pre-registered,
implemented, and unit-tested; this manifest pins the frozen code and the exact charge
to run once the blocker is resolved. Governing charter: `MIM_CHARTER_v0.1.md`.

## Status

**BLOCKED — DATA/SEMANTIC (C).** See `MIM_CHARTER_v0.1.md` §Blocker: `early_return`
crosses the previous RTH close; the corpus is dividend-unadjusted; SPY ex-dividend
drops (~30–40 bps) are indistinguishable from ordinary overnight moves (median
overnight `|gap|` 27.6 bps; the twelve largest are genuine macro/news gaps). Clean
dividend handling needs an external ex-dividend calendar or a dividend-adjusted
previous-close series — a new-provider decision for HELM. No guess is made.

Autonomy-protocol steps completed: **1 provenance, 2 pre-registration, 3 implement,
4 self-test, and the semantic-resolution check.** Stopped at **step 5 (run)** on the C
blocker. Steps 6–8 (evidence, ledger result row, classify) are deferred to the run.

## Frozen code (pinned)

| File | SHA256 |
|---|---|
| `analysis/mim.py` | `74f577b10e2210021c3483d6caa2a7bae9baa6c5dfd2d308ce1b688f433b0d77` |
| `analysis/test_mim.py` | `91e8be9949f75d22b1b1c0aab3e7e971f89a891fd07d9c56346e5465cf9f83aa` |
| `analysis/mim_overnight_diagnostic.py` | `936af3aae076668e13bf6e608c571b4ccb9af46c00092119914a2902238fafeb` |
| `analysis/MIM_OVERNIGHT_DIAGNOSTIC_2026-08-27.json` | `7bb922d86c37d6b801add4563ffafa5287716b44fbdd0ac6e778b147d48a9348` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`.
`mim.py` has **no development `__main__`** — outcome access is gated on the blocker.
Tests: `python3 test_mim.py` (6/6 synthetic — clock semantics, OLS/HC1, sign strategy,
cost ordering, kill/advance gates). No engine change; MIM is a standalone module.

## Budget (§9/§f)

MIM-dev **≤ 4** (default new-family allowance). **0 spent** (blocked before execution);
a `family=MIM, budget_class=development` ledger row is written only at the first run.

## Exact next development-run charge (executes only after the blocker is resolved)

> "STRATEGY LAB — MIM-0 FIRST DEVELOPMENT RUN (unblocked). With an approved SPY
> ex-dividend calendar (or a dividend-adjusted previous-close series) now in the repo,
> freeze the ex-dividend handling convention (exclude or adjust the ~5–6 ex-dividend
> sessions) BEFORE outcomes. Freeze `RUN_MIM0_DEV_v1.0.md`; then run `mim.py` over
> 2024-09-03 → 2025-12-31: build observations (frozen clock semantics), OLS/HC1
> regression (β>0 primary), sign-strategy economics (bps, long/short, PF, win, max-DD
> fixed-notional, bootstrap CI, monthly, outliers), and the three frozen cost views
> (zero / lab-slippage / 5 bps stress). Classify by the frozen gates: FAMILY DEAD if
> β≤0 or gross≤0 or fails the cost stress; else EDGE CANDIDATE — VALIDATION DECISION
> REQUIRED (do not run validation). Spend MIM config 1/4. Update the research ledger.
> Development only. Commit and push. No merge."

## Amendments

*(append dated amendments here; never edit the text above in place)*
