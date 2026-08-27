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
- **Status:** **BLOCKED — DATA/SEMANTIC (status C).**
- **Primary hypothesis:** `late_return = α + β·early_return`, β > 0.
- **Primary metric:** regression β (HC1 robust SE) + sign-strategy gross bps, cost-stressed.
- **Data:** dev 2024-09-03→2025-12-31; screened/raw.
- **Configs spent / ceiling:** 0 / 4 (default new-family allowance).
- **Development result:** **NOT RUN** — outcome access blocked.
- **Robustness / Validation:** n/a.
- **Terminal disposition:** none — pre-registered, implemented, tested; blocked before outcome.
- **Reason (blocked):** `early_return` crosses the previous RTH close; the corpus is dividend-**unadjusted** (Polygon `adjusted=true` = splits only). SPY ex-dividend drops (~30–40 bps) are **indistinguishable from ordinary overnight moves** (median overnight |gap| 27.6 bps) — no clean OHLCV separation. Needs an external SPY ex-dividend calendar or a dividend-adjusted previous-close series. `MIM_CHARTER_v0.1.md`, `RUN_MIM0_DEV_PREP_v0.1.md`, `analysis/MIM_OVERNIGHT_DIAGNOSTIC_2026-08-27.json`.

## Overnight / opening-dislocation reversal

- **Mechanism:** an overnight/opening dislocation reverses intraday.
- **Provenance:** Codex reconnaissance rank #2 (not yet chartered).
- **Status:** WATCHLIST (not opened).
- **Primary hypothesis / metric / data / budget:** TBD at charter.
- **Note:** would face the **same** previous-close dividend blocker as MIM if it crosses the overnight — resolve the ex-dividend convention first.

## Closing-auction / rebalance watchlist

- **Mechanism:** index-rebalance / closing-auction imbalance effects near the close.
- **Provenance:** owner watchlist item.
- **Status:** WATCHLIST (not opened).
- **Note:** OHLCV cannot represent the official closing auction; would require auction/imbalance data (a new provider) — likely a data blocker for executable claims.

---

*Update this ledger whenever a family changes status, spends a config, or reaches a
disposition. Link the canonical manifest; never restate its evidence here.*
