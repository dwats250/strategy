# RUN MANIFEST — R1 (VDC instrumented development) · v1.0 · FROZEN 2026-08-25

Frozen per `docs/conventions.md` §b **before capture**, as A1.7 requires for a sealed
capture: never edited in place; corrections are dated amendments or a new version with
the version in the filename. Supersedes `RUN_VDC_SPY_5m_dev_R1_PREP_v0.1.md` (retained).
Capture artifacts, hashes, and the ledger row are recorded at capture time by dated
amendment / ledger append — that is the pre-registered completion path, not an edit.

## Identity & authorization

- Run id: `VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0R1`
- Family: `VDC` · Budget class: `development` · Role: A1.8 R1 — instrumented VDC
  development; instrumentation must not alter strategy behavior
- Charter governing: `STUDY_CHARTER_v0.1.md` + Amendments A1, A2, A3;
  `PVAE_ANALYSIS_PREREG_v0.1.md`
- Authorization: **owner charge of 2026-08-25 (Dustin), "OWNER AUTHORIZATION — R1
  CAPTURE"** — authorizes TradingView capture of the exact committed R1 artifact and,
  after artifacts are supplied, **only** the mechanical R0/R1 identity gate. Lane
  record: Fable 5 as lane 1 for this charge only, per the owner's standing in-session
  per-charge disposition (§j table unchanged).
- **Capture disposition: `SEALED-UNINTERPRETED` (A1.7).** The performance summary is
  not inspected; no outcome relationship is examined; no PVAE terciles are computed;
  validation and holdout are untouched. No §9 budget slot is drawn until first
  unsealing, which requires separate owner/HELM authorization.

## Source pin (exact artifact to run — no edits permitted)

- Repo commit: `40c5523c3163d43e819f4cea9bdb7df4773cbe61`
- Script: `../scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine`
  sha256 `32aaaa4d2148186774921c8529c5ab3600bfe4110ffff2fd0213a6631ff72bc4`
- Base (R0 source of record): `../scripts/VWAP_Continuation_FastAlpha_v0.pine`
  sha256 `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`
- Containment record: PREP v0.1 (static byte-identity of the trading region; zero
  executable `strategy.*` references and zero v0-variable writes in the
  instrumentation region; 19/19 local mirror tests; all 24 foundation columns
  byte-identical across 38,357 local rows).
- **Contingency (owner-authorized in the capture charge):** if the ten instrumentation
  columns do not appear in the chart-data export, a presentation-only change to the
  instrumentation plots' `display =` argument is authorized, recorded as a source
  version bump per §c. **No calculation and no strategy semantics may change**; the
  trading region must remain byte-identical under the same static checks.

## Pre-registered trial accounting (§b amendment)

- `trials_planned`: **18** (charter §9 VDC development ceiling; R1 introduces no new
  configuration — trading spec identical to R0).
- `dsr_threshold_implied`: same basis as R0 — N=18, T=334 development sessions →
  daily SR 0.1014 ≈ annualized 1.61 (recorded hurdle; nothing is evaluated against it
  while sealed).
- Budget draw: **none at capture (SEALED-UNINTERPRETED).** The R0/R1 identity gate is
  a mechanical admissibility check on trade-set identity, pre-registered here as **not
  an unsealing**. Draw is recorded by dated note at first unsealing (A1.7).

## Execution context — required, exact R0 context (owner confirms at capture)

AMEX:SPY (NYSE Arca) · 5m · RTH · exchange timezone America/New_York · ADJ enabled ·
all R0 strategy Properties unchanged (capital $50,000, fixed qty 1, pyramiding 0,
commission 0%, slippage 1 tick, on bar close, bar detalization Default 4 ticks/bar,
order execution delay one tick, limit at requested price) · development range
2024-09-03 → 2025-12-31 inclusive. **TradingView Volume is added to the chart before
the chart-data export** so volume is included. Any deviation from the R0 context is a
STOP for the identity gate.

## Windows & firewall (A3 — unchanged)

Development 2024-09-03 → 2025-12-31 inclusive; embargo 2026-01-02/2026-01-05 and
validation 2026-01-06 → 2026-04-30 untouched; holdout frozen-forward only. If the
chart-data export physically contains post-development rows (as R0's did), rows after
2025-12-31 are dropped on load before any value column is read.

## Capture requirements (owner) and custody (this repo)

1. R1 List of Trades CSV.
2. R1 chart-data CSV — with Volume, and with all ten instrumentation columns
   (`ACCEPT_STATE_DIR`, `EMA50`, `S_9_20_50`, `ORDERED_9_20_50`, `EXPANDING_9_20_50`,
   `ALIGNED_EXP_COUNT_9_20_50`, `SHOCK_RATIO`, `RECENT_SHOCK`, `S_10_22_55`,
   `ORDERED_10_22_55`) confirmed present.
3. Result/context screenshot if convenient (optional per the capture charge).
4. On supply: preserve byte-identical under `../exports/`, hash, append the ledger row
   with `SEALED-UNINTERPRETED` in notes, run **only** the identity gate below, report.

## R0/R1 identity gate (frozen mechanics — the only analysis authorized)

Tool: `../analysis/identity_gate_r0_r1.py` (deterministic; self-test required to pass
before use). Reference: the preserved R0 export
`../exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv`
(sha256 `8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241`).

Requirement — exact identity: **1,331 completed trades** and exact agreement in trade
side, entry/exit timestamps, entry/exit prices, and P/L, **subject only to
demonstrated export-format normalization**, pre-registered as exactly: UTF-8 BOM
stripping; leading/trailing whitespace on cell values; numeric cells compared after
decimal parsing (so `1.5` ≡ `1.50`); and column-set differences reported explicitly
with the intersection compared and any non-comparable identity column treated as a
FAIL, not skipped. Row order and trade numbering must agree as exported.

- **PASS** → report `R1 ADMISSIBLE` and **stop** for owner/HELM authorization to
  unseal development analysis. No outcome inspection, no terciles, no further steps.
- **FAIL** → **STOP**, classify the first divergence (feed/context difference vs
  export-format difference vs instrumentation-induced behavior change vs unresolved),
  report it, repair nothing silently. PVAE is not analyzed (A1.8).

## Post-run

- Ledger row: appended at capture with `SEALED-UNINTERPRETED` notes (pending).
- Identity gate result and anomalies: recorded by dated amendment below (pending).

## Amendments

*(append dated amendments here; never edit the text above in place)*
