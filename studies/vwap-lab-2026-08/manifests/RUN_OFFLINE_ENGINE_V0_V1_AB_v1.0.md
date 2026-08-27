# RUN RECORD — Offline FastAlpha execution engine + V0/V1 A/B · v1.0 · 2026-08-26

Authoritative record for the first fully-offline FastAlpha run: a deterministic
local execution engine, its calibration against the preserved TradingView R0,
and the controlled V0 (EMA 9/20) vs V1 (EMA 10/22) development A/B. Frozen on
commit; corrections are dated amendments or a new versioned file (§b/§c).

## Identity & authorization

- Run id: `OFFLINE_FASTALPHA_ENGINE_V0_V1_AB_dev_2024-09-03_2025-12-31`
- Family: `VDC` · Budget class: `development` · Symbol SPY · 5m · RTH.
- Authorization: **owner charge 2026-08-26 (Dustin), "OFFLINE FASTALPHA EXECUTION
  ENGINE + V0/V1 A/B."** Standing owner direction in that charge: *TradingView is
  no longer a gating dependency; the preserved R0 is an external reference/oracle
  only; development experimentation runs locally where the frozen corpus and a
  deterministic implementation permit.*
- Scope executed: build the smallest deterministic local engine reproducing the
  exact FastAlpha family; calibrate local V0 against R0 and classify residuals;
  run the local V0/V1 A/B; prove determinism. **No validation, no holdout, no new
  parameter, no filter, no threshold search, no merge.**

## Inputs (checksummed)

| Input | SHA256 |
|---|---|
| Local 1m corpus `data/cache/canonical/SPY_1m_2024-09-01_2026-08-22.csv.gz` | `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a` |
| R0 trade list `exports/VWAP_VDC_SPY_5m_RTH_dev_..._v0.csv` (calibration oracle) | `8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241` |
| Base source `scripts/VWAP_Continuation_FastAlpha_v0.pine` | `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e` |
| Variant `scripts/VWAP_Continuation_FastAlpha_V1_EMA10_22.pine` | `bca7f7eaf8fd7c93e3400dd72a8661f3d8f9d99219509a2f0fedf3cc03b32519` |

## Code (versioned, §c/§d)

| File | SHA256 | Role |
|---|---|---|
| `analysis/fastalpha_engine.py` | `f3862da80f797be2e203660afb4784d9ed7f915ebbbaee44b79b4c370f71942b` | The engine (execution layer) + analysis-only spike detector |
| `analysis/v0_calibration.py` | `dce3c066ef9b225996cfc686fb5b485834000f90615e11fd379f9503ba141119` | V0 calibration vs R0 (asserts R0 headline; classifies) |
| `analysis/v0_v1_ab.py` | `ab8d00186bb975d0523082bfa678f0525a53db517f2a6b8ffaf953213f847776` | The controlled A/B (deltas, determinism, robustness) |
| `analysis/test_fastalpha_engine.py` | `1ad1f377848840f256b6184a94e69ffd515db10d8f3d2ec9659af279f101277e` | 11 deterministic engine-path tests |

Indicator semantics (session VWAP, EMA fast/slow, ATR14, directional state,
candidates) are NOT re-implemented — they remain owned by `parity_foundation.py`
(PARITY_GATES.md Gate 2). The engine adds only the execution layer Pine performs.

## Broker-emulator assumptions — fixed a priori, never tuned against P/L

The charge requires the smallest documented deterministic assumption, stated,
with residuals classified rather than tuned. Full text in the engine docstring;
in brief:

- **Bar model.** Script runs at each bar close; market orders (entries, thesis
  closes) fill at the **next bar's open**; the ATR stop rests and is checked
  **intrabar**, beginning with the entry bar (entry + stop-out can share a bar).
- **Within-bar order.** (1) fill the pending market order at the open; (2) if
  still in a position, test the resting stop intrabar; (3) at the close evaluate
  EOD, then thesis failure, then (only if flat) a new entry. A pending thesis
  close therefore pre-empts the stop on the bar it fills.
- **mintick = 0.01** (SPY; verified from the R0 export price grid); `atrStopTicks
  = max(1, round(atr14 / mintick))`, frozen on the signal bar.
- **Slippage = 1 tick**, applied adversely to every market and stop fill (TV's
  documented behaviour; limit orders — none here — excepted).
- **Stop fill.** Long stop at S triggers when low ≤ S, fills at S, unless the bar
  opened at/below S (gap) in which case it fills at the open; short mirrored.
- **EOD** fires only on a `hm == 1550` bar with a position open (immediate, at the
  close). Half-day sessions have no 15:50 bar, so EOD cannot fire and the position
  persists — recorded, not special-cased.
- **Backtest range.** Orders entered only within the development window; indicators
  warm from the corpus start (= window start), so no pre-window history diverges.

## Windows & firewall (charter A3 — unchanged)

Development **2024-09-03 → 2025-12-31 inclusive** only. Embargo, validation
(SEALED), unused buffer, hypothesis-source, and holdout were **not inspected, not
loaded, not read**. No forward data touched.

## Calibration result — local V0 vs preserved R0

Machine evidence: `analysis/V0_CALIBRATION_RESULTS_2026-08-26.json`. R0 headline
(1331 trades, net +25.69, 295 wins, long +43.68, short −17.99) re-asserted from
the preserved export before comparison.

- **Structure (feed-robust).** 89.86% of R0 trades reproduced by (fill bar, side)
  (1196/1331); 79.64% fully identical on (fill bar + exit bar + exit reason).
- **Execution logic validated.** On the 1124 matched trades whose exit *path*
  agrees, local−TV P/L sums to only −3.90 and the local/TV P/L ratio is 1.020
  (p05–p95 0.91–1.14) — i.e. the pure dividend-adjustment feed scale (local
  split-only prices are ~1% higher than TV ADJ). Fills, slippage, and mintick are
  therefore correct.
- **Divergence is input-data, not logic.** The local net (−111.61) disagrees with
  R0 (+25.69) almost entirely because of **corpus bad-ticks**: 141 development-
  window 5m bars carry a >2-point reverting wick (single-minute price spikes, e.g.
  2025-05-27 13:13 low 578.43 amid ~589.9; 2024-12-20 11:10 low 581.52 with volume
  7.88M vs ~150k neighbours). 39 phantom ATR stop-outs land on such bars (−129.19);
  removing them brings the local net to **+17.58**, back into the R0 ballpark.
- **Discrepancy classification** (charge's classes):
  - *feed/adjustment* — matched path-agreeing trades reconcile at the ~1% scale;
    53 R0-only entries are near-threshold candidate flips (split-only vs ADJ).
  - *signal-boundary* — 82 R0-only entries are flat-gate path drift (local *would*
    signal but was not flat); 167 local-only entries mirror the same drift.
  - *intrabar execution* — 35 matched stop/hold flips, 12 on corpus spike bars
    (bad ticks) carrying −52.87 of the flip P/L; input-data, not logic.
  - *early-close/session* — 0 entry-set diffs touch the five half-day sessions.
  - *implementation defect* — **NONE demonstrated.**
  - *unresolved* — residual small-magnitude entry-set drift inherent to a path-
    dependent strategy on a near-identical but not identical feed.

**Disposition: LOCAL ENGINE RESEARCH-READY** for controlled differential (A/B)
research. Absolute local P/L is corpus-data-quality limited and must not be
compared to TV at face value; the execution logic is calibrated and bounded.

## A/B result — V0 EMA 9/20 vs V1 EMA 10/22 (development, local)

Machine evidence: `analysis/V0_V1_AB_RESULTS_2026-08-26.json`. Same corpus, same
engine, same window; only the trading EMA pair differs, so the feed seam and the
corpus bad-ticks act on both arms and cancel where trades overlap.

| Metric | V0 (9/20) | V1 (10/22) | V1 − V0 |
|---|---:|---:|---:|
| Trades | 1363 | 1366 | +3 |
| Net P/L | −111.61 | −114.63 | **−3.02** |
| Expectancy / trade | −0.0819 | −0.0839 | −0.0020 |
| Profit factor | 0.855 | 0.851 | −0.005 |
| Win rate | 21.35% | 21.30% | −0.05 pt |
| Max drawdown | 143.94 | 144.35 | +0.41 |
| Avg bars held | 12.50 | 12.36 | −0.14 |
| Long P/L (N) | +17.18 (708) | +15.48 (715) | −1.70 |
| Short P/L (N) | −128.79 (655) | −130.11 (651) | −1.32 |

- **Entry-set overlap** 1277 shared (Jaccard 0.880); V0-only 86, V1-only 89 — the
  EMA change moves ~6% of trades.
- **Spike-robustness.** Removing phantom stops on corpus spike bars: V0 net +17.58,
  V1 net +16.12, **Δ −1.46** (vs raw Δ −3.02); only a 1-trade spike asymmetry
  separates the arms. The delta is small and negative under both treatments.
- **Determinism.** Each arm was simulated twice and is byte-identical; 11 engine-
  path unit tests pass.

**Disposition: V1 DEVELOPMENT NEUTRAL.** EMA 9/20 → 10/22 produces no material,
robust difference on the local development window. The delta is a trivial,
non-robust negative lean (|Δexpectancy| ≈ 0.001–0.002 / trade; magnitude roughly
halves under spike removal) — within the corpus data-quality noise and not
separable from it. It is not an improvement; it is not meaningfully worse.

## Budget & ledger treatment (§9/§f) — flagged for owner

- V0-local is **calibration** (a re-derivation of the already-counted R0); it draws
  no new development slot.
- V1-local is a **new interpreted development comparison**; per §f (one row per
  interpreted run) it is recorded as one VDC-development interpreted run, taking the
  count to **3 of ≤ 18** (R0 = 1; R1 PVAE unseal = 2; this = 3). The ledger row maps
  the TV-capture columns to `LOCAL-ENGINE (offline; no TV capture)`.
- **Owner adjudication invited:** this treats a local interpreted development run as
  budget-consuming, the conservative reading. If the owner intends offline runs to be
  accounted on a separate track, amend here and correct the ledger row.

## Recommended next single offline experiment (NOT implemented)

**Corpus bad-tick screening.** A versioned, pre-registered 1-minute spike filter
(flag/repair single-minute reverting wicks beyond a stated multiple of local ATR,
e.g. the 141 bars this run isolated), re-run the same V0 calibration, and confirm
the local net converges toward R0 — lifting the engine from "differential-ready"
to TV-grade absolute fidelity. It is the one item between local research and
absolute-P/L trust, and it is orthogonal to any parameter change. Do not tune the
filter against P/L; register the rule, then measure.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 test_fastalpha_engine.py     # 11 engine-path tests
python3 v0_calibration.py            # asserts R0 headline; writes V0_CALIBRATION_RESULTS_*.json
python3 v0_v1_ab.py                  # determinism-checked A/B; writes V0_V1_AB_RESULTS_*.json
```

## Amendments

*(append dated amendments here; never edit the text above in place)*

### Amendment 1 — 2026-08-26 — additive engine extension (corpus-integrity packet)

`analysis/fastalpha_engine.py` gained an **additive, backward-compatible**
parameter `compute_feature_rows(..., drop_t_ms=None)` that drops named 1-minute
bars before 5m aggregation, so the corpus-integrity research-clean view can be
applied as a pure reversible filter. New engine sha256
`b8825ed553889cb3b8ce73ea0d39e93ffab096194a30b7e2d9c36151fd06d0f9` (was
`f3862da80f797be2e203660afb4784d9ed7f915ebbbaee44b79b4c370f71942b`). The default
path (`drop_t_ms=None`) is unchanged, and the V0/V1 A/B and V0 calibration result
JSONs were re-verified **byte-identical** under the extended engine — no result in
this run record changes. No version bump required (§c: the change cannot alter
existing results). See `CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md`.

### Amendment 2 — 2026-08-26 — additive per-trade risk fields (tear-sheet packet)

`analysis/fastalpha_engine.py` now records `stop_price`, `risk_points`
(= `atr_stop_ticks × mintick`, the frozen 1R denominator), and `pnl_r` on each
trade dict, to support R-normalized reporting. Additive only — the P/L, exit
mechanics, and every existing metric are unchanged. New engine sha256
`42db304e9467426d666f2141486267cb362a24710d143b21949291a71f531efd` (was
`b8825ed553889cb3b8ce73ea0d39e93ffab096194a30b7e2d9c36151fd06d0f9`). The V0/V1
A/B and V0 calibration result JSONs were re-verified **byte-identical**; no result
in this run record changes. No version bump required (§c). See
`EXPERIMENT_TEARSHEET_v0.1.md`.

### Amendment 3 — 2026-08-26 — additive stop-multiple parameter (ATR-stop-surface packet)

`analysis/fastalpha_engine.py` gained `simulate(..., atr_stop_mult=1.0)`, scaling
only the initial ATR stop distance; default 1.0 reproduces V0 exactly. New engine
sha256 `975f747d8c4aef9d2ff209c904410aa31adb6ce4c3c11348d52e57b8a736221c` (was
`42db304e9467426d666f2141486267cb362a24710d143b21949291a71f531efd`). The V0/V1 A/B
and calibration result JSONs are unchanged (no drift on `git status`). No version
bump required (§c). See `RUN_ATR_STOP_SURFACE_v1.0.md`.

### Amendment 4 — 2026-08-26 — additive side-permission parameters (long-only packet)

`analysis/fastalpha_engine.py` gained `simulate(..., enable_longs=True,
enable_shorts=True)`, gating entry permission by side; defaults reproduce V0
exactly. New engine sha256
`11af1c55db3dd0d1cbca5a489f1dbe7194344311e4ffcdc1142b9da1bcde86f5` (was
`975f747d8c4aef9d2ff209c904410aa31adb6ce4c3c11348d52e57b8a736221c`). Prior result
JSONs unchanged (no drift). No version bump (§c). See `RUN_LONG_ONLY_AB_v1.0.md`.
