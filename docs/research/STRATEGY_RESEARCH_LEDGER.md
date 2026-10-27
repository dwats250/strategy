# STRATEGY RESEARCH LEDGER · v1.0 · 2026-08-27

One entry per major research family: mechanism, provenance, status, hypothesis,
metric, data, budget, and outcomes. This is a **narrative index** that links to the
canonical frozen records; it does **not** restate or rewrite historical evidence.
The authoritative per-run record remains `studies/vwap-lab-2026-08/LEDGER.csv` (§f)
and the frozen manifests. Statuses reflect the committed record as of HEAD.

Legend — status: ACTIVE · TERMINAL (no edge) · PARKED · BLOCKED · DESIGN · WATCHLIST.

---

## VDC — VWAP Drift Continuation

- **Mechanism:** established directional drift relative to session VWAP continues;
  enter on an opposing-color pullback while aligned.
- **Provenance:** owner FastAlpha v0 Pine source (`scripts/VWAP_Continuation_FastAlpha_v0.pine`); charter §3/§8.
- **Status:** TERMINAL — retained as **benchmark/control only**.
- **Primary hypothesis:** naked VDC has positive per-trade expectancy.
- **Primary metric:** mean expectancy R.
- **Data:** SPY 5m RTH, dev 2024-09-03→2025-12-31; screened primary + raw.
- **Configs spent / ceiling:** 15 / 18 (closed; 3 intentionally unused).
- **Development result:** risk-neutral-to-negative (R ≈ +0.009 screened, −0.009 raw); EMA & ATR-stop surfaces PARAMETER-INSENSITIVE/FLAT.
- **Robustness:** bootstrap CIs straddle zero; outlier-dependent.
- **Validation/OOS:** long-only sub-hypothesis got the one look → **FAILS VALIDATION**.
- **Terminal disposition:** NO EDGE FOUND (`studies/vwap-lab-2026-08/manifests/CONTINUATION_TERMINAL_DISPOSITION_v1.0.md`, `VDC_TERMINAL_DISPOSITION_v1.0.md`).
- **Reason:** no material, robust, positive risk-adjusted edge on any lever.

## PVAE — Persistent VWAP-Aligned Expansion

- **Mechanism:** persistent aligned EMA(9/20/50) expansion stratifies VDC trades into a better subset.
- **Provenance:** charter §A1.1/§A1.4 (adjudicated stratification hypothesis).
- **Status:** PARKED.
- **Primary hypothesis:** upper-dispersion-tercile trades have higher expectancy, symmetrically.
- **Primary metric:** per-trade expectancy contrast (R), long & short must agree.
- **Data:** dev; instrumented R1 trade set.
- **Configs spent / ceiling:** counted within VDC budget (1 unseal look).
- **Development result:** pooled contrast +0.0051 but long −0.0824 / short +0.1074 **disagree**.
- **Robustness:** n/a (parked on sign-disagreement rule C).
- **Validation/OOS:** not earned; R2 sealed.
- **Terminal disposition:** PARKED (part of the continuation TERMINAL lane).
- **Reason:** symmetric requirement failed; no rescue.

## FPC — First Pullback Continuation

- **Mechanism:** only the FIRST opposing-color pullback after a FRESH VWAP/EMA regime; one entry per regime.
- **Provenance:** charter §3/§4/§A1.6 antecedents + owner/HELM H3 attestation (`FPC_CHARTER_v0.1.md` Amdt 1).
- **Status:** TERMINAL (within the continuation lane).
- **Primary hypothesis:** first-pullback entry beats VDC's repeated-entry rule in R.
- **Primary metric:** mean expectancy R; ΔR vs VDC (MATERIAL_R 0.03).
- **Data:** dev; screened primary + raw.
- **Configs spent / ceiling:** 1 / 12 (closed).
- **Development result:** **FPC DEVELOPMENT WORSE** — screened ΔR −0.032, raw −0.031; FPC absolute R −0.023 (`RUN_FPC0_DEV_v1.0.md`).
- **Robustness:** raw/screened agree; bootstrap straddles zero.
- **Validation/OOS:** none (killed at development).
- **Terminal disposition:** part of NO EDGE FOUND continuation lane.
- **Reason:** first-pullback restriction lowers R on both sides; no rescue.

## VMR — VWAP Mean Reversion

- **Mechanism:** fade extreme displacement from session VWAP back toward VWAP (opposite of continuation).
- **Provenance:** charter §3 (family), §5/§A1.3 (excursion metric), §4/§A1.2 (acceptance) — committed, pre-continuation-outcome.
- **Status:** DESIGN (charter frozen; **not run; parked at owner request**).
- **Primary hypothesis:** extension + reversal reverts to VWAP with positive R.
- **Primary metric:** mean expectancy R.
- **Data:** dev (when run); screened primary + raw.
- **Configs spent / ceiling:** 0 / 8.
- **Development result:** none (design only).
- **Robustness / Validation:** n/a.
- **Terminal disposition:** none (open, parked).
- **Reason:** designed; execution deferred. Frozen K = 4.0916 ATR (dev |E| P90, trade-blind). `VMR_CHARTER_v0.1.md`, `RUN_VMR0_DEV_PREP_v0.1.md`.

## MIM — Market Intraday Momentum

- **Mechanism:** the return from previous RTH close through the first 30 min predicts the final-30-min return (Gao, Han, Li & Zhou).
- **Provenance:** literature (Gao et al., *Market Intraday Momentum*); independent Codex reconnaissance ranked #1.
- **Status:** **TERMINAL — FAMILY DEAD** (was BLOCKED-C; unblocked by the State Street seam, then run).
- **Primary hypothesis:** `late_return = α + β·early_return`, β > 0.
- **Primary metric:** regression β (HC1 robust SE) + sign-strategy gross bps, cost-stressed.
- **Data:** dev 2024-09-03→2025-12-31; screened/raw (N=328); dividend-neutral early_return (State Street sidecar).
- **Configs spent / ceiling:** **1 / 4** (remaining ≤3 not earned by a failed baseline).
- **Development result:** **β = −0.01674** (HC1 t −0.53, CI [−0.079, +0.045], R² 0.002) → β>0 FAILS; sign-strategy gross **−0.59 bps**, fails the 5 bps cost stress; robust to raw and ex-dividend-excluded views.
- **Robustness:** raw == screened; ex-dividend-excluded β −0.0157 (also dead); bootstrap CI straddles zero.
- **Validation/OOS:** none (killed at development).
- **Terminal disposition:** **FAMILY DEAD** — no intraday-momentum edge on SPY here; no rescue.
- **Reason:** previous-close→10:00 return does not positively predict the final-30-min return. `MIM_CHARTER_v0.1.md`, `RUN_MIM0_DEV_v1.0.md` Amdt 1, `analysis/MIM0_DEV_2026-08-27.json`. (Earlier blocker + State Street resolution: `data/SPY_EX_DIVIDENDS_v1.0.json`, `MIM_OVERNIGHT_DIAGNOSTIC_2026-08-27.json`.)

## ODR — Overnight / Opening-Dislocation Reversal

- **Mechanism:** an overnight/opening dislocation reverses during the first half hour.
- **Provenance:** Liu & Tse (2017), *Int. Rev. Econ. & Finance* 48:440–451 (US ETF overnight-return / intraday reversal), verified independently.
- **Status:** **TERMINAL — FAMILY DEAD.**
- **Primary hypothesis:** `first_half_hour_return = α + β·overnight_return`, β < 0 (reversal); dividend-neutral overnight (State Street sidecar).
- **Primary metric:** regression β (HC1) + causal sign-strategy gross bps, cost-stressed.
- **Data:** dev 2024-09-03→2025-12-31, N=328; screened == raw.
- **Configs spent / ceiling:** **1 / 4** (remaining ≤3 not earned by a failed baseline).
- **Development result:** **β = −0.03571** (HC1 t −0.89, CI [−0.115, +0.043], R² 0.007) — sign holds directionally but **insignificant**; causal sign-strategy gross **−0.63 bps**, fails the 5 bps cost stress.
- **Robustness:** raw == screened; bootstrap CI straddles zero.
- **Validation/OOS:** none (killed at development).
- **Terminal disposition:** **FAMILY DEAD** — reversal too weak to be significant or executable on SPY here; no rescue.
- **Reason:** gross causal expectancy ≤ 0 (β<0 alone is not enough). `ODR_CHARTER_v0.1.md` Amdt 1, `analysis/ODR0_DEV_2026-08-27.json`.

## Closing-auction / rebalance watchlist

- **Mechanism:** index-rebalance / closing-auction imbalance effects near the close.
- **Provenance:** owner watchlist item.
- **Status:** WATCHLIST (not opened).
- **Note:** OHLCV cannot represent the official closing auction; would require auction/imbalance data (a new provider) — likely a data blocker for executable claims.

---

## Lab restart entries (2026-10-16 onward)

These entries use the research-card fields from [`ROADMAP.md`](ROADMAP.md). Each links to its frozen
manifest and findings; it does not restate them. The per-run record is each study's `LEDGER.csv`.

### VWR — VWAP touch-and-reclaim (lab-defined)

- **Source / date:** lab hypothesis, 2026-10-16 (`studies/vwap-ema9-2026-10/manifests/VWR_FAMILY_v1.0.md`).
- **Rules:** lab-defined. VWR0 is a **same-bar touch/reclaim proxy**: the bar's low against VWAP at the
  bar's close, plus close beyond EMA9, with **no prior-trend requirement**. It is not the continuation
  pattern (acceptance, pullback, continuation) described in the roadmap.
- **Hypothesis / primary comparison:** VWR0 positive net R. One-factor variants VWR1–VWR4: EMA9
  confirmation, cross entry, signal-close 2R exit, morning only. Compared by Δ expectancy R; daily-equity
  Sharpe reported separately.
- **Data / execution:** SPY 1m (August corpus, mask v1.0), 2024-09-10 → 2026-08-21; Backtesting.py;
  $0.0135/share/side; 1× notional.
- **Status:** COMPLETED (frozen v1.1, run once). **Result:** negative. Every trial lost after costs and
  finished below a SPY session-hold benchmark. Suspicious prints on one session (unresolved; see the data note) inflate some losses without changing
  any sign. Findings: `studies/vwap-ema9-2026-10/analysis/VWR0_EXP_FINDINGS_2026-10-16.md`; data note:
  `docs/lab/DATA_QUALITY_2026-10-16.md`.
- **Next question:** none within VWR (no rescue variants). The unchanged rules on newly acquired sessions
  are proposed separately (`VWR0_FRESH_EXTENSION_v0.1.toml`). That would be fresh historical evidence, not
  a forward test.

### IG-AUSTIN-P0 — provisional reading of an Instagram VWAP + EMA9 reel

- **Source / date:** @austin.daytrades reel (shared by Marc), retrieved 2026-10-16. Rule table:
  `studies/vwap-ema9-2026-10/manifests/SOURCE_RULES_IG_AUSTIN_v1.0.md`.
- **Stated vs assumed:** stated are the 3-minute chart, VWAP OHLC4 with session anchor, EMA9 on close, and
  entry at the cross. Assumed are the SPY shares proxy (the creator trades options), completed-bar entry,
  EMA9 exit, signal-bar stop, and skipping the first-bar cross.
- **Status:** COMPLETED as an independent comparison in VWR0-EXP. **Result:** negative on SPY shares;
  roughly flat before costs. Says nothing about the creator's options P&L.

### VMR-L — VWAP mean reversion (lab-defined)

- **Source / date:** lab hypothesis group, 2026-10-16. The parked August VMR design is the reference; its
  metric is reused and its threshold is not revived.
- **Observation / mechanism / competing explanation:** see
  `studies/vwap-mr-2026-10/manifests/VMRL_FAMILY_PROPOSAL_v0.1.md`. Exhaustion after a fast displacement,
  set against trend days where VWAP lags.
- **Hypothesis / comparison:** MR0 (failed extension after a ≥4 ATR displacement, exit at VWAP) has
  positive net R. Variants: MR1 extension-only and MR2 K = 5.0 (entry); MR3 shock-only (context); MR4
  half-way target (exit).
- **Status:** PROPOSED, awaiting the strategy-definition review. No real-data run.

---

## Amendment 2026-10-27: statistical power, and the window nothing has scored

Claude, owner work permit (WP3). This amendment is append-only. No status, run, manifest or verdict above changes, and no family reopens. It says how far each terminal label reaches.

**Method.** Minimum detectable effect (MDE) at 80% power, two-sided α = 0.05: MDE = 2.8016 × SE. Each SE comes from the canonical record:
- from the CI width ÷ 3.92 where only a CI is given;
- from |estimate| ÷ t where a t is given.

| Family / test | Estimate | SE | MDE | Recorded 95% upper bound | Reading |
|---|---|---|---|---|---|
| VDC long-only validation, n = 176 | −0.0187 R | 0.155 R | 0.43 R | +0.323 R (block bootstrap) | **Underpowered.** Expectancy up to about +0.3 R per trade is not excluded. "FAILS VALIDATION" is a failed point-estimate criterion (A: mean > 0), not evidence of no edge. |
| VWR0 baseline, 2,428 trades | −0.038 R | 0.0345 R | 0.097 R | ≈ +0.030 R (normal) | The CI excludes expectancy above about +0.03 R per trade; this comes from the negative estimate, not from power. Power at +0.03 R is ≈ 0.14; 80% power is reached only at ≈ 0.10 R. |
| MIM β > 0, N = 328 | β −0.0167 | 0.0317 | 0.089 | +0.045 (HC1) | The β-sign hypothesis is underpowered for β < 0.09. |
| MIM sign strategy, gross | −0.59 bps | 1.32 bps | 3.7 bps | +1.98 bps (bootstrap) | For this pre-registered sign strategy, a gross mean ≥ 5 bps is excluded; power at 5 bps ≈ 0.97. |
| ODR β < 0, N = 328 | β −0.0357 | 0.0403 | 0.113 | +0.043 (HC1) | The β-sign hypothesis is underpowered for |β| < 0.11. |
| ODR sign strategy, gross | −0.63 bps | 1.46 bps | 4.1 bps | +2.39 bps (bootstrap) | For this pre-registered sign strategy, a gross mean ≥ 5 bps is excluded; power at 5 bps ≈ 0.93. |

**How to read the labels from here**
- **"FAMILY DEAD" (MIM, ODR)** fired on point-estimate gates: MIM on β ≤ 0 (and gross ≤ 0), ODR on gross ≤ 0. The cost stress decided neither verdict. MIM's primary kill, β ≤ 0, is the test this table calls underpowered. Separately, each bootstrap CI excludes a gross mean ≥ 5 bps for the one pre-registered sign strategy, and 5 bps is the round-trip stress a positive gross mean would have to survive. That exclusion is adequately powered. It is not a statement about other strategies on the same signal. Small β of either sign is not excluded.
- **"NO EDGE FOUND" / "FAILS VALIDATION" (VDC)** means not shown on 176 trades. The validation look is spent, so this cannot be rescued here; it is not a powered rejection.
- **"Negative" (VWR0)** rests on the 95% CI, which excludes net per-trade expectancy above about +0.03 R; it is +0.036 R excluding the unresolved 2025-04-23 prints (−0.032 R, t −0.92; findings line 80). The sample had 80% power only for effects of about 0.10 R.
- These figures correct the external Assurance Review Reconciliation (2026-10-26, outside this repo). It labelled all four "insufficient evidence" by applying one rule to the β tests and the sign-strategy tests alike.

**The window nothing has scored (2026-08-24 → 2026-10-15, 38 sessions).** It sits in capture `729dc4e9` (`datasets/REGISTRY.json`).
- **What has touched it:** integrity checks (row counts, OHLC validity, the overlap comparison in `docs/lab/DATA_QUALITY_2026-10-16.md`). There was also one trade-blind feature scan: `studies/vwap-mr-2026-10/analysis/EXCURSION_QUANTILES_2026-10-16.json.txt` covers the whole fresh capture, and it set VMR-L's K. No strategy has scored the window, and no P&L or return inspection is recorded.
- **Proposals that would spend it:** both are `PROPOSED` and not run.
  - `VWR0_FRESH_EXTENSION_v0.1.toml` would spend it as descriptive fresh-historical evidence. Its own notes say the VWR0 gate (200 trades) will probably not be met.
  - `VMRL_FAMILY_PROPOSAL_v0.1.md` would score the full 2024-10-16 → 2026-10-15 capture, re-spending consumed dates.
- **Status under §g:** it is a deferred-inspection window, not a holdout. Its scored start (08-24) follows the fitted window's end (08-21) with no session between them. EMA is continuous across sessions (`src/stratlab/strategies/common.py`), so this is a zero-gap boundary, which the 2026-07-30 embargo amendment forbids. A one-session embargo would satisfy the literal rule for VWR's EMA9 on 5-minute bars and IGP0's EMA9 on 3-minute bars. The frozen configurations also declare `warmup_sessions = 5`, which a cautious reading takes as the lookback to embargo.
- **Forward data:** 2026-10-16 onward is not captured. It becomes a §g holdout only for a specification frozen before its collection.
- **Reservation:** any use of either window is an owner decision, made before the run and recorded here first.

---

*Update this ledger whenever a family changes status, spends a config, or reaches a
disposition. Link the canonical manifest; never restate its evidence here.*
