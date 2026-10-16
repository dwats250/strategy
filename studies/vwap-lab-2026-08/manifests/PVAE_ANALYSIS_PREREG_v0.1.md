# PVAE ANALYSIS PRE-REGISTRATION v0.1 (FROZEN SKELETON) · 2026-08-25

Pre-registered offline-analysis plan for the PVAE stratification hypothesis, per
`docs/conventions.md` §b and `STUDY_CHARTER_v0.1.md` Amendment A1. Frozen: never edited in
place; corrections are dated amendments appended below or a new version with the version in
the filename.

**Status: SKELETON — NO DATA ANALYZED.** This document freezes the analysis *before* any
trade outcome exists to inspect. It authorizes nothing until:

1. `VDC_SOURCE_STATUS` is no longer `SOURCE_REQUIRED`;
2. run R1 (instrumented development) exists and has **passed the R0/R1 identity gate**
   (Amendment A1.8) — if instrumentation changed the trade set, this analysis does not run.

Zero PVAE outcome interpretation has occurred as of this freeze.

---

## 1. Trial accounting (`docs/conventions.md` §b amendment 2026-07-30)

- `trials_planned` (this pre-registration): **1** — the single primary comparison in §2.
  Sensitivity rows (§4) are descriptive context for that one trial, not additional trials.
- `dsr_threshold_implied`: **UNRESOLVED** here — depends on sample length, unknown until the
  development window and R1 trade count exist. Computed and recorded in the R1 run manifest
  before that run, per the §b amendment.

## 2. Primary development comparison (frozen)

**PVAE-qualified naked-VDC entries vs all other naked-VDC entries**, per-trade expectancy,
in the development dataset only.

A naked-VDC entry is **PVAE-qualified** iff, at its entry-evaluation bar close, all of:

1. correct-direction **ESTABLISHED** VWAP acceptance state (frozen rule, Amendment A1.2);
2. directionally **ordered EMA 9/20/50** (long: `EMA9 > EMA20 > EMA50`; short mirrored);
3. `S_t` in the **upper development-entry tercile** (tercile rule, Amendment A1.4 — numeric
   boundaries computed once from development-entry `S_t` observations, then frozen);
4. **expanding**: `S_t > S_(t-2)`;
5. aligned-expansion **persistence ≥ 2 consecutive completed bars**.

All covariates come from the R1 instrumented entry stamps; nothing is recomputed with
hindsight.

## 3. Required reporting (all mandatory)

- Pooled contrast (qualified vs other).
- Long-side contrast, reported separately.
- Short-side contrast, reported separately.
- Qualifying N and non-qualifying N.
- Expectancy per group; profit factor per group if meaningful at the observed N.
- Top-trade dependence (contrast with the single best trade removed per group).
- Year / subperiod breakdown if the sample supports it.

**No optimization.** No threshold, boundary, family, or persistence value moves in response
to any number produced here.

## 4. Permitted sensitivity rows (descriptive only)

Sensitivity findings **cannot replace a failed primary test**:

- lower / middle / upper `S_t` tercile strata;
- persistence ≥ 1 / ≥ 2 / ≥ 3;
- `RecentShock` descriptive strata (≥ 2.0 label per Amendment A1.4);
- VWAP state × EMA state 2×2;
- 9/20/50 vs 10/22/55 label agreement, only if those covariates exist in R1.

## 5. Park conditions (frozen — no rescue)

Symmetric PVAE is **PARKED without rescue** if any of:

- **A.** PVAE-qualified development N < 30. Disposition: `INSUFFICIENT / PARKED`.
- **B.** Pooled qualified-vs-other expectancy contrast ≤ 0.
- **C.** Long and short contrast signs disagree. Disposition: symmetric PVAE `PARKED`. An
  asymmetry observation may be registered for future research but may not rewrite this test
  long-only or short-only.
- **D.** A positive result exists only after moving away from the tercile rule, the
  persistence ≥ 2 primary, or the frozen acceptance rule.
- **E.** Development passes but the single pre-registered historical validation look fails
  to reproduce the contrast sign. No new historical rescue slice.

## 6. Data firewall bindings

- Development dataset: per the windows frozen in the R-run manifests, placed outside the
  HYPOTHESIS-SOURCE period (late May–Aug 2026) whenever available history permits
  (Amendment A1.6).
- Validation: the single sealed R2 capture, unsealed once; frozen tercile boundaries reused
  unchanged (Amendment A1.4, A1.7).
- No holdout access. The frozen-forward holdout (`docs/conventions.md` §g) is untouched by
  this analysis.

---

## Amendments

*(append dated amendments here; never edit the text above in place)*

### Amendment P1 — 2026-08-26 · Primary comparison executed (R1 development, first unsealing)

The §2 primary comparison was run once, under the frozen definitions, on the admissible R1
development trade set (identity gate PASS; R1 == R0). Authority: owner/HELM development-unseal
charge 2026-08-26. Full record, frozen tercile boundaries, condition funnel, per-split table, and
park-rule evaluation are in `RUN_VDC_SPY_5m_dev_R1_v1.0.md` Amendment 3; tool
`../analysis/pvae_dev_analysis_r1_v1.0.py`; evidence `../analysis/PVAE_DEV_RESULTS_2026-08-26.json`.

- Frozen upper-tercile boundary `b_hi = 1.3297578122368192` (b_lo = 0.5320216540492776; N=1330
  defined entry S_t). Computed once from S_t only; reused unchanged for any future validation look.
- PVAE N = 263, non-PVAE N = 1068. Per-trade expectancy contrast (PVAE − other): pooled +0.0051,
  long −0.0824, short +0.1074.
- **Park condition C fires** (long and short contrast signs disagree). Disposition:
  **SYMMETRIC PVAE PARKED — no rescue.** The marginally positive pooled contrast does not satisfy
  the frozen symmetry requirement (§5.C). No §5.C short-only variant is created; it may only be
  separately pre-registered as future research. The single validation look is **not earned**;
  validation stays sealed (§5.E). No definition, threshold, tercile rule, persistence value, or
  acceptance rule was moved.
- `trials_planned` for this pre-registration was 1 (§1); that one trial is now spent.
