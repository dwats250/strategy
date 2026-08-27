# PRE-REGISTRATION — SPY corpus integrity screen · v0.1 · 2026-08-26

Frozen anomaly rules for a **trade-blind** data-quality screen of the verified
local SPY 1m corpus, plus the record of applying them (Phases 2–4). The rules and
thresholds in Phase 1 were fixed from distributional / market-microstructure
reasoning **before** any strategy effect (Phase 4) was inspected — the firewall
this packet requires. Corrections are dated amendments or a new versioned file
(§b/§c). Authorization: owner charge 2026-08-26, "SPY CORPUS INTEGRITY SCREEN."

## Firewall (binding)

A bar may be flagged **only** for its market-data characteristics. It may **not**
be flagged because it caused a losing trade, triggered a stop, would improve P/L
if removed, or differs from a desired TradingView result. The screen module
(`analysis/corpus_integrity_screen.py`) imports **no** engine or trade-list code;
it reads only the hash-guarded corpus. Thresholds were frozen from the data
distribution (below) and never tuned against any outcome. The four bad ticks
known from the prior offline-engine packet are used **only** as a blind-
rediscovery cross-check, never as a threshold input.

## PHASE 1 — frozen rules & thresholds

Robust local scale = the **median 1-minute range (high−low) within each
(date, session)**. All excursions are measured against that per-session scale, so
the screen adapts to each day's volatility without any global constant.

**Rule A — impossible / internally inconsistent OHLC (both sessions).** Flag if
`high < low`, `high < max(open,close)`, `low > min(open,close)`, or any price
≤ 0. Unconditional; no threshold. Confidence **HIGH**.
*Note:* the vendor `vw` (1m VWAP) lies just outside `[low,high]` on 92,631 bars —
**all EXT** — a systematic extended-hours vendor-rounding characteristic, not
per-bar corruption; `vw_outside` is therefore **excluded** as a standalone flag
(a decision made from the data, in Phase 1, before Phase 4).

**Rule B — isolated reverting excursion (bad-tick signature).** For a bar with
both same-session neighbours, let the excursion beyond BOTH neighbours be
`ex_dn = min(low₋₁,low₊₁) − low` (down) or `ex_up = high − max(high₋₁,high₊₁)`
(up). Flag if the excursion is simultaneously:

| Threshold | Value | Justification (data / microstructure) |
|---|---|---|
| `ex ≥ K_ISO × scale` | **K_ISO = 15** | Beyond ~99.5th pct of the RTH isolation-ratio distribution; genuine price discovery is confirmed by a neighbour trading into the new area, so a 15× isolated move is implausible as real. |
| `ex ≥ PCT_FLOOR × price` | **0.30%** | Economic-materiality floor; also guards dead-calm sessions where `scale` is tiny. RTH flag count is **stable (9)** for PCT_FLOOR ∈ [0.2%, 0.5%] — insensitive to this floor. |
| reverting wick `≥ REV_FRAC × ex` | **REV_FRAC = 0.5** | The body did not hold at the extreme (a round-trip), separating a spike from a genuine breakout that holds. |

Confidence: **HIGH** in **RTH** (liquid — an isolated reverting multi-point
round-trip is a data error); **PLAUSIBLE** in **EXT** (thin pre/post-market where
such prints occur legitimately). Session liquidity is a market-data property, not
a trade outcome.

**Rule C — volume / print corroboration.** `v ≥ VOL_OUTLIER_MULT × session-median
volume` (**40×**) is recorded as **evidence** only. Real volume spikes occur at
opens/closes/events, so volume alone is **PLAUSIBLE**, never a standalone HIGH flag.

**Rule D — timestamp / session structure.** Duplicate or non-monotonic `t_ms`,
and the OHLC-validity of Rule A. Structural.

**Sensitivity (frozen, descriptive — not used to choose the threshold):**

```
K_iso  pct_floor   RTH flags   EXT flags
 10      0.3%          19         168
 15      0.2%           9         237
 15      0.3%           9         157   <- FROZEN
 15      0.5%           9          72
 20      0.3%           5         142
 25      0.3%           5         129
```

## PHASE 2 — application to the corpus

Evidence: `analysis/CORPUS_INTEGRITY_SCREEN_2026-08-26.json` (corpus sha256
`a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`, 422,657 1m
bars).

- **Structural:** 0 timestamp duplicates, strictly monotonic, **0 impossible-OHLC
  bars** (Rule A empty) — the corpus is structurally sound.
- **Flagged: 166 1m bars** — **9 HIGH-CONFIDENCE (all RTH)**, **157 PLAUSIBLE (all
  EXT)**. The EXT flags cluster at 08:00 and 16:00–18:00 (thin session edges),
  corroborating the PLAUSIBLE classification.
- **Blind rediscovery:** all four previously-known bad ticks (2024-12-20 11:10,
  2025-03-14 13:44, 2025-04-16 14:31, 2025-05-27 13:13) reappear in the HIGH set
  without being targeted.
- The nine HIGH-CONFIDENCE bars: 2024-10-01 11:32, 2024-12-20 11:10, 2025-03-14
  13:44, 2025-04-16 14:31, 2025-05-19 12:05 / 12:18 / 12:20 (a mid-session RTH
  cluster), 2025-05-27 13:13, 2025-12-22 15:12.

## PHASE 3 — disposition

- **HIGH-CONFIDENCE DATA ANOMALY** — the 9 RTH isolated reverting excursions
  (1.2–2.2% single-minute round-trips absent from neighbours). Masked.
- **PLAUSIBLE EXTREME MARKET PRINT** — the 157 EXT excursions. Reported, **not
  masked** (thin-market prints may be real; and EXT is not used by the engine).
- **UNRESOLVED** — none.

The raw corpus is **preserved byte-for-byte** (a test asserts its sha256 is
unchanged after the screen). The research-clean view is a **frozen reversible
mask** — `analysis/CORPUS_MASK_v1.0.json` (HIGH-CONFIDENCE only) — applied by
DROPPING those 1m bars before 5m aggregation (`fastalpha_engine.compute_feature_rows(...,
drop_t_ms=)`); the raw view is recovered simply by not applying it.

## PHASE 4 — raw vs screened V0 diagnostic (data-quality treatment only)

Run **after** the flag set was frozen. Evidence: `analysis/V0_RAW_VS_SCREENED_2026-08-26.json`.
V0 (EMA 9/20) rerun on raw vs screened; signal logic and stops unchanged; **no
variant, no validation/holdout, no interpreted-run budget draw** (a diagnostic of
a data treatment, not a strategy trial).

| Metric | Raw | Screened | Δ |
|---|---:|---:|---:|
| Trades | 1363 | 1354 | −9 |
| Stop-outs | 660 | 649 | −11 |
| Net P/L | −111.61 | −86.64 | **+24.98** |
| Expectancy/trade | −0.0819 | −0.0640 | +0.0179 |
| Profit factor | 0.855 | 0.886 | +0.030 |
| Max drawdown | 143.94 | 131.98 | −11.95 |

Affected trades: 9 raw-only entries vanish, 0 screened-only, 19 change their exit
(all enumerated in the JSON).

**Reading (honest, and a correction to the prior packet).** Dropping the 9
demonstrable bad-tick bars removes 11 phantom stop-outs, improves V0 net by
+24.98 and cuts max-DD ~12 — a real, bounded data-quality effect. But it does
**not** reconcile the local net (−86.64) to the R0 reference (+25.69). The prior
offline-engine packet's loose 5m ">2-pt reverting wick" heuristic (141 bars,
"excl-spike net +17.58") **over-removed**: most of those 5m wicks are genuine
intra-bar volatility, not isolated bad ticks. This frozen screen shows only **9**
bars are defensibly bad data; the remaining local↔R0 gap is the split-only-vs-ADJ
feed seam and 1m→5m reconstruction on non-anomalous bars, **not** removable data
errors.

## Disposition answers (charge)

- **Frozen anomaly rules:** Rules A/B (+C evidence, D structural) above.
- **Counts/classes:** 166 flagged — 9 HIGH-CONFIDENCE (RTH), 157 PLAUSIBLE (EXT);
  0 impossible-OHLC; 0 structural.
- **Confidence disposition:** 9 HIGH-CONFIDENCE, 157 PLAUSIBLE, 0 UNRESOLVED.
- **Research-clean view justified?** **Yes** — it removes only demonstrable data
  errors, improves R0 fidelity, and lowers drawdown, at the cost of 9 bars.
- **Raw vs screened V0 diagnostic:** net +24.98, stops −11, max-DD −11.95 (table).
- **Proceed on raw / screened / dual-report?** **DUAL-REPORT for absolute metrics**
  (the 9 bars move them materially but do not fully reconcile to R0, so both views
  are informative), with the **screened view as the default research corpus**.
  For **differential A/B** research either view suffices — bad ticks largely cancel
  in the differential — and the screened view is the cleaner default. Do **not**
  treat the screened net as TV-equivalent; the feed seam remains.

## Files

| Path | SHA256 | Role |
|---|---|---|
| `analysis/corpus_integrity_screen.py` | `691013ed23b7b5360e63ef04b7dc4094841b157fb68d7b36cfb9284ea2d2433b` | Frozen trade-blind screen |
| `analysis/CORPUS_INTEGRITY_SCREEN_2026-08-26.json` | `74c59f63e9fa9c9718118abfa884e8890217a2d58ea1e4c261f49d157e3d5479` | Full evidence report |
| `analysis/CORPUS_MASK_v1.0.json` | `d1360f6f1d67463af0023db8a5e78dbd93293a4ca6bcda9e5d578194badd700a` | Frozen reversible HIGH-CONFIDENCE mask |
| `analysis/v0_raw_vs_screened_diagnostic.py` | `96f7c8a59365170e0be07f89b0cebb8e6e9a8a32a3a2fc6955ef99a92019f718` | Phase 4 diagnostic |
| `analysis/V0_RAW_VS_SCREENED_2026-08-26.json` | `862d7bdd5fbaca27da1a1e9d63c42df91976047e19f309da233748a137491ad7` | Phase 4 evidence |
| `analysis/test_corpus_integrity_screen.py` | `550b5b25ae5e478f92c0f4404deebd43af912e291f51e85da29ba790d6a2d2c0` | 9 tests (detection, no-mutation, reversible mask, determinism) |

## Amendments

*(append dated amendments here; never edit the text above in place)*
