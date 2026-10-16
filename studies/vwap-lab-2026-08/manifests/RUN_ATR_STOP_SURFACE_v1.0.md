# RUN RECORD — Fixed-risk diagnostic + ATR-stop response surface · v1.0 · 2026-08-26

Fixed-risk re-expression of V0 (Part A) and a frozen five-value ATR_STOP_MULT
response-surface experiment (Parts B/C). Only the initial ATR stop distance is
varied; every other strategy semantic is exactly V0. Frozen on commit; corrections
are dated amendments (§b/§c). Authorization: owner charge 2026-08-26, "FIXED-RISK
DIAGNOSTIC + ATR STOP RESPONSE SURFACE."

## Firewall (binding)

Development window **2024-09-03 → 2025-12-31** only. No validation, no holdout, no
embargo inspection. No EMA-family change, no PVAE rescue, no ATR-regime filter, no
position-sizing strategy change, no new provider, no TradingView dependency. The
only parameter changed is `ATR_STOP_MULT` (source default 1.0).

## Inputs & code

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`
(hash-guarded). Screened view = frozen `CORPUS_MASK_v1.0.json` (primary); raw =
sensitivity.

| File | SHA256 |
|---|---|
| `analysis/fastalpha_engine.py` | `975f747d8c4aef9d2ff209c904410aa31adb6ce4c3c11348d52e57b8a736221c` |
| `analysis/tearsheet.py` | `c950bc6f55cfe1c7493db8ceaf38d529309e67ccd84c435b7fe60b588d0a8fb6` |
| `analysis/v0_fixed_risk_diagnostic.py` | `c605832c6b54c3bc4eeb5fc7673fd94152a860f9a0b7699e813668c8935efc16` |
| `analysis/atr_stop_surface.py` | `f05e801c74e3dc8bb903266013e2fd20942293304f8b6324c8d9485ee48bf433` |
| `analysis/V0_FIXED_RISK_DIAGNOSTIC_2026-08-26.json` | `619056bb39a19d63c81b4e89e8fad451e79bbea7b895beb3d2fd1b9d83a90250` |
| `analysis/ATR_STOP_SURFACE_2026-08-26.json` | `86fe2e21a1079952dd1a421b32abb43d4e275d39492430e96afdef57c93c8f35` |
| `analysis/ATR_STOP_SURFACE_2026-08-26.csv` | `8385387c6062c94ee71901954f89a3c59d0122e0e6c9e276db69259b59135b98` |

Engine change: `simulate(..., atr_stop_mult=1.0)` scales only the initial stop
distance; default 1.0 reproduces V0 byte-identical. Tear sheet gained the additive
`r_equity` helper (R-space equity/drawdown). Both re-verified against prior
results (see `EXPERIMENT_TEARSHEET_v0.1.md` and `RUN_OFFLINE_ENGINE_...` amendments).

## PART A — fixed-risk V0 diagnostic (no new trial, no budget draw)

Existing V0 (EMA 9/20, stop 1.0) re-expressed under equal initial risk (1R per
trade). Evidence `V0_FIXED_RISK_DIAGNOSTIC_2026-08-26.json`. Screened:

- **Fixed-share net −$86.64 but fixed-risk cumulative +12.19R** (mean +0.009R) —
  **signs disagree.** Pearson($ vs R) = 0.79. Under equal risk per trade V0 is a
  hair positive; the dollar loss is a **position-sizing** effect (losses fall on
  higher-ATR / higher-risk trades that cost more per share at fixed size), **not**
  stop geometry.
- Long R-expectancy **+0.047**, short R-expectancy **−0.032** (longs carry the
  edge; shorts are the R-drag). Max drawdown 75.7R.
- ATR/risk vs R outcome, by **predeclared** risk_points quintiles (descriptive, no
  filter, not optimized): mean R = [0.076, −0.026, 0.134, −0.055, −0.084] — no
  clean monotone ATR→R relationship; the highest-risk quintile is mildly worst.
- $100/trade figure is an **ACCOUNT-CONSTRUCTION EXAMPLE ONLY**; CAGR not computed.

## PART B — frozen ATR-stop family (pre-outcome)

Frozen before any outcome inspection: `ATR_STOP_MULT ∈ {0.75, 1.00 [CONTROL],
1.25, 1.50, 1.75}`. Predeclared classification threshold **MATERIAL_R = 0.03**
R/trade (economic materiality on the risk-normalized primary metric). The 1.00 arm
is the existing V0.

## PART C — response surface (screened primary; raw sensitivity)

From `ATR_STOP_SURFACE_2026-08-26.csv`:

**Screened (primary):**

| mult | n | stop% | net $ | exp $ | **exp R** | PF | win% |
|---|--:|--:|--:|--:|--:|--:|--:|
| 0.75 | 1560 | 63.4 | −68.0 | −0.0436 | 0.0198 | 0.908 | 19.2 |
| **1.00** | 1354 | 47.9 | −86.6 | −0.0640 | **0.0090** | 0.885 | 21.7 |
| 1.25 | 1231 | 33.1 | −25.5 | −0.0207 | 0.0189 | 0.963 | 23.7 |
| 1.50 | 1168 | 22.9 | −5.5 | −0.0047 | 0.0186 | 0.992 | 24.8 |
| 1.75 | 1128 | 16.1 | +2.2 | +0.0019 | 0.0217 | 1.003 | 25.5 |

**Raw (sensitivity):** exp R = {0.75: −0.0002, 1.00: −0.0091, 1.25: +0.0028,
1.50: +0.0030, 1.75: +0.0045}; net $ = {−91.0, −111.6, −51.7, −33.8, −33.4}.

- **Widening the stop** monotonically cuts stop-out% (63→16), raises win% (19→26)
  and PF (0.91→1.00), lifts thesis-exit count, and improves fixed-share **$**
  (−87 → +2.2 screened). Long/short: longs stay positive in R, shorts negative,
  at every arm (no long/short sign flip; asymmetry is not stop-driven).
- **Raw/screened directional agreement:** 0 of 4 arms disagree on the sign of
  (arm − control) in expectancy R. Directionally consistent across views.
- **BUT expectancy R is FLAT:** all five arms lie in [0.009, 0.022], spread
  **0.0127 R < 0.03**. In risk-adjusted terms the stop multiple has **no material
  effect**; the $ / PF improvement with width is a **position-sizing artifact**
  (Part A), not a risk-adjusted edge.
- The only $-positive arm (1.75) is **marginal and view-dependent** (screened
  +$2.2 vs raw −$33.4) — not a real optimum.
- Bootstrap CIs of mean $-expectancy overlap zero for every arm (evidence JSON).

### Classification & control assessment (descriptive; no value selected)

- **Response shape (primary, risk-adjusted R): `4. FLAT / NO MATERIAL SENSITIVITY`.**
  Fixed-share **$** shows a monotonic-with-width shape, explicitly attributed to
  sizing, not stop geometry.
- **Control 1.00:** **reasonable** in risk-adjusted (R) terms — within the flat
  band (it is a negligible trough at 0.009R); it looks **"too tight"** only in
  fixed-share **$** terms, which is the sizing artifact.
- Best arm by expectancy R = 1.75, but the spread is immaterial and its $ edge is
  view-dependent — **no production value is selected, and no intermediate multiple
  is interpolated or tested.**

## Budget accounting (§9/§f) & multiple testing

- **1.00** = existing V0 — **no new draw.**
- **0.75, 1.25, 1.50, 1.75** = four new interpreted VDC-development configurations.
  VDC-dev interpreted runs **3 → 7 of ≤ 18**. All four are recorded in the ledger
  as **explored candidates** — this family is **not** counted as "one test."
- No post-hoc interpolation: 0.8 / 0.9 / 1.1 / 1.3 / … were **not** tested; an
  apparent $-optimum between frozen values is recorded as an observation only.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 v0_fixed_risk_diagnostic.py   # Part A -> V0_FIXED_RISK_DIAGNOSTIC_*.json
python3 atr_stop_surface.py           # Parts B/C -> ATR_STOP_SURFACE_*.json + .csv
python3 test_fastalpha_engine.py      # incl. atr_stop_mult scaling
python3 test_tearsheet.py             # incl. r_equity
```

## Recommended next SINGLE research question (not implemented)

The stop multiple is risk-neutral, and both Part A and the surface localize the
negative risk-adjusted contribution to the **short side** (long R-expectancy
+0.047 vs short −0.032, at every stop). The next single research question:
**"Is the naked VDC edge long-only?"** — a single controlled offline A/B of
long-only vs symmetric V0 (screened primary) through `ab_dual`, testing whether
the short side is a persistent R-drag. It is a trade-side-scope change to be
separately authorized; no sizing or entry-logic change.

## Amendments

*(append dated amendments here; never edit the text above in place)*
