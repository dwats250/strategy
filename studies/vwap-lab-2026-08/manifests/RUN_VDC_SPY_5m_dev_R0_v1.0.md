# RUN MANIFEST — R0 (VDC naked development reference) · v1.0 · FROZEN 2026-08-25

Frozen per `docs/conventions.md` §b: never edited in place; corrections are dated
amendments or a new version with the version in the filename. Supersedes
`RUN_VDC_SPY_5m_dev_R0_PREP_v0.1.md` (PREP, retained as audit trail). The PREP manifest
was committed **before** capture; this v1.0 freeze fills the OWNER-OBSERVE fields from
the owner's R0 charge of 2026-08-25 and records the preserved capture artifacts.

**Evidence classes.** `MECHANICAL(source)` = established by the ingested Pine.
`OWNER-ATTESTED` = observed TradingView UI state as stated by Dustin in the R0 charge of
2026-08-25. The owner reports properties/context screenshots were captured; the image
files were not present in this session and are **not** preserved here — the attestation
below is the charge text, not the screenshots.

## Identity & authorization

- Run id: `VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0`
- Family: `VDC` · Budget class: `development`
- Charter governing: `STUDY_CHARTER_v0.1.md` + Amendments A1, A2, A3
- Source status at run time: `INGESTED@scripts/VWAP_Continuation_FastAlpha_v0.pine
  sha256 c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`
  (hash re-verified against the tracked file at freeze time)
- Authorization: **owner charge of 2026-08-25 (Dustin), "STRATEGY LAB — R0 INGEST +
  PARITY PASS"** — preserve the completed TradingView R0 benchmark and run the smallest
  local parity comparison. Lane record: Fable 5 acted as lane 1 for this charge only, by
  the owner's standing in-session per-charge disposition (as in Amendments A1–A3); the
  `docs/conventions.md` §j role-to-model table is unchanged.

## Pre-registered trial accounting (§b amendment)

- `trials_planned`: **18** — the charter §9 pre-registered VDC development ceiling
  (independent configurations committed before the first run of this class).
- `dsr_threshold_implied`: expected maximum Sharpe under the null at N=18 trials over
  T=334 development sessions (daily observations), Bailey/López de Prado approximation
  `E[max Z] = (1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(N·e))` with γ≈0.5772 → E[max Z]=1.854 →
  **daily SR 0.1014 ≈ annualized 1.61**. Recorded as the pre-registered hurdle for any
  later interpretation; **no interpretation against it occurs in this packet.**
- Budget draw: **R0 = 1 of VDC ≤ 18, INTERPRETED at capture** (the owner observed the
  performance summary; A1.7 sealed-capture deferral does not apply). Running total: 1/18.

## Execution context — observed TradingView state

| Field | Value | Evidence class |
|---|---|---|
| Strategy title | `VWAP Continuation - Fast Alpha v0` | MECHANICAL(source) |
| Pine version | 6 | MECHANICAL(source) |
| Symbol ID | **AMEX:SPY** | OWNER-ATTESTED |
| Displayed exchange | NYSE Arca | OWNER-ATTESTED |
| Timeframe | 5m | OWNER-ATTESTED + MECHANICAL(source guard) |
| Session | RTH | OWNER-ATTESTED + MECHANICAL(source guard) |
| Chart timezone | Exchange / America/New_York | OWNER-ATTESTED |
| Data adjustment | **ADJ enabled** (dividend-adjusted) | OWNER-ATTESTED |
| Candles | standard | MECHANICAL(source docs); UI not separately attested |
| Initial capital | $50,000 | OWNER-ATTESTED (= source declaration) |
| Sizing | fixed quantity 1 | OWNER-ATTESTED (= source declaration) |
| Pyramiding | 0 | OWNER-ATTESTED (= source declaration) |
| Commission | 0% | OWNER-ATTESTED (= source declaration) |
| Slippage | 1 tick | OWNER-ATTESTED (= source declaration) |
| Script execution | on bar close | OWNER-ATTESTED |
| Bar detalization | Default (4 ticks/bar) | OWNER-ATTESTED |
| Order execution delay | one tick | OWNER-ATTESTED |
| Limit execution | requested price | OWNER-ATTESTED |
| `syminfo.mintick` | not attested; not assumed | UNRECORDED |
| Deep Backtesting available history | not attested | UNRECORDED |
| Loaded-bar range at capture | not attested | UNRECORDED |
| TV account / plan tier | not attested | UNRECORDED |

## Windows & firewall (§g, A3 — frozen by charter Amendment A3)

- Development window: **2024-09-03 → 2025-12-31 inclusive**. Trade list confirms: first
  entry fill 2024-09-03 11:10 ET, last exit 2025-12-31 15:50 ET — no fills outside it.
- Embargo: 2026-01-02 and 2026-01-05 (untouched).
- Validation / deferred-inspection: 2026-01-06 → 2026-04-30, **sealed, not inspected**.
  The chart-data artifact below physically contains post-2025 rows; the parity pass
  drops them on load before any value column is read (`analysis/parity_r0_pass.py`).
- Holdout: frozen-forward only (§g); not applicable to R0.

## Strategy specification

Unchanged from PREP v0.1 (established from the ingested source; see
`../scripts/VWAP_Continuation_FastAlpha_v0_PROVENANCE.md`): opposing-candle trigger
inside directional state, signal-bar window [09:35, 15:30) ET, market entry next bar,
ATR(14)×1.0 tick-converted stop frozen at signal bar, VWAP-failure thesis exit, EOD
`close_all(immediately=true)` on the 15:50 bar. No VWAP acceptance state (naked VDC v0).

## Capture & artifacts (preserved byte-identical; sha256 of file as supplied)

1. **List-of-Trades export** (TradingView, AMEX:SPY chart, supplied filename
   `VWAP_FastAlpha_v0_AMEX_SPY_2026-08-25.csv`, 2662 rows = 1331 trades × entry+exit):
   `../exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv`
   sha256 `8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241`
   (an identical-hash duplicate `… (2).csv` existed in the supply directory; one copy
   preserved).
2. **5m chart-data export** (TradingView, supplied filename `BATS_SPY, 5 (2).csv`;
   OHLC + Session VWAP + EMA9 + EMA20 + flat-gated Fast-Alpha signal fields; **no
   volume column**; 20,363 bars, 2025-08-11 → 2026-08-25 ET):
   `../exports/TV_CHARTDATA_BATS_SPY_5m_RTH_2025-08-11_2026-08-25_FastAlphaV0.csv`
   sha256 `9e0a49183edbb165a760b5bc4f56a79d9710b205e71d623c3dc2328792a14dfc`
   **Provenance seam (recorded, not resolved):** the export filename indicates a
   **BATS:SPY** chart, while the R0 trade list ran on **AMEX:SPY**; the export's EMA
   warm-up `na` rows at its 2025-08-11 start show its chart had only ~20k bars of
   history loaded. It is preserved as feature-parity evidence, not as the R0 chart's
   bar record. Bar parity against the actual R0 (AMEX) chart remains open (Gate 1).
3. **Screenshots** — reported captured by owner; files not supplied in this session;
   NOT preserved. UI state above is owner-attested text.
4. Capture method: owner TradingView UI exports at the laptop; preservation and hashing
   by this session (no re-export, no content modification — hashes match the supplied
   files byte-for-byte).

## R0 benchmark metrics — REFERENCE ONLY (no edge interpretation)

Owner-observed in TradingView and independently reproduced from the preserved trade
list by `analysis/parity_r0_pass.py` (asserts, nonzero exit on mismatch):

| Metric | Owner-observed | Reproduced from export |
|---|---|---|
| Completed trades | 1,331 | 1,331 |
| Net PnL | +$25.69 | +$25.69 |
| Profit factor | 1.04 | 1.0401 |
| Profitable trades | 295 / 1,331 = 22.16% | 295 / 1,331 = 22.16% |
| Max drawdown | $47.07 | $46.31 on closed-trade cumulative PnL (TV's figure is an equity metric incl. intra-trade excursion; ordering consistent) |
| Long contribution | +$43.68 | +$43.68 (697 trades) |
| Short contribution | −$17.99 | −$17.99 (634 trades) |

These numbers are recorded to anchor R1-vs-R0 identity checks and local parity. They
are **not** evaluated against any acceptance rule, expectancy claim, or the DSR hurdle
in this packet.

## Post-run

- Ledger row appended: **yes** (2026-08-25, `../LEDGER.csv`).
- Parity pass over the preserved artifacts: `analysis/parity_r0_pass.py` v1.0, results
  `analysis/R0_PARITY_RESULTS_2026-08-25.json`; gate dispositions appended to
  `../PARITY_GATES.md` (dated 2026-08-25 entries).
- Anomalies: early-close sessions 2025-11-28 and 2025-12-24 — local reconstruction
  carries a terminal 13:00 partial bucket that the TV chart data does not (classified
  resampling/session difference, pre-registered Gate 1 sub-item); trade-list vs
  chart-data feed seam as recorded above.
