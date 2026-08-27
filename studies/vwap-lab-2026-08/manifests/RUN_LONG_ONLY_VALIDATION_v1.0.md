# RUN RECORD — Long-only SINGLE-LOOK validation · v1.0 · 2026-08-26

**THE ONE pre-registered validation look** at the long-only hypothesis, authorized
by owner/HELM charge 2026-08-26 ("LONG-ONLY SINGLE-LOOK VALIDATION"). This document
is the **frozen pre-registration**: everything above the Amendments section was
fixed and committed **before any validation outcome was computed or inspected**.
After outcomes, this text is never edited in place — results are recorded only as a
dated **result amendment** (§b/§c) that leaves the pre-registration intact.

## Hypothesis (frozen)

For FastAlpha VDC under the frozen V0 parameters, **restricting the strategy to
LONG entries improves risk-normalized performance because the SHORT side has
negative expectancy.** The hypothesis is **development-generated** (long
R-expectancy positive / short negative persisted across every ATR-stop arm, across
the 3×3 EMA surface, and in an actual long-only development rerun); this single
validation look is its first out-of-development test.

## Control / variant (frozen)

- **Control** = V0 **symmetric** (long + short): EMA 9/20, ATR14, `ATR_STOP_MULT`
  1.0, all original FastAlpha semantics. `enable_longs=True, enable_shorts=True`.
- **Variant** = V0 **long-only**: identical to control, **short entries disabled**,
  no other change. `enable_longs=True, enable_shorts=False`.

Both are **rerun through the frozen engine** (`fastalpha_engine.simulate`), NOT
derived by filtering symmetric trades (disabling a side changes flat-state
occupancy and therefore the path).

## Validation window (frozen) & firewall

**2026-01-06 → 2026-04-30 inclusive** — the single planned look. Trade-blind
precondition check (dates/counts only, no features, no simulation): the window
holds **80 RTH sessions**, first 2026-01-06, last 2026-04-30.

The verified corpus spans **2024-09-03 → 2026-08-21** — it extends PAST the window
into the frozen-forward holdout and the late-May..Aug hypothesis-source region.
Firewall: **do not touch** the 2026-01-02 / 2026-01-05 embargo (both exist in the
corpus but fall before the window and are never simulated), the unused historical
buffer after validation, the late-May..Aug hypothesis-source outcomes, or the
frozen-forward holdout. No TradingView dependency, no CuttingBoard contact, no
merge.

**Holdout hygiene (method):** EMA/ATR/VWAP are strictly **causal** (a bar's feature
depends only on bars at/before it; session VWAP resets per session), so the
validation script truncates the 1m stream at 2026-04-30 **before** any 5m
aggregation. In-window feature values are therefore identical to a full-corpus
computation, while **no bar after 2026-04-30 ever enters the indicator or trade
path.** `simulate` additionally windows trades to [2026-01-06, 2026-04-30]. No
engine change is made.

## Corpus view (frozen)

Screened (frozen **`CORPUS_MASK_v1.0`**, 9 HIGH-CONFIDENCE bars) is **primary**;
raw is sensitivity. **Disclosed pre-outcome:** all 9 mask bars are dev-window
(2024–2025) timestamps and **0 fall inside the validation window**, so screened and
raw views **coincide in-window**. The mask is **not** re-derived on validation data
(that would be a forbidden new degree of freedom). Consequently raw sign-agreement
holds by construction, and the **block-bootstrap CI is the operative discriminator**
between STRONG and DIRECTIONAL (see below).

## Primary metric (frozen)

**Mean trade expectancy in R.** 1R = the frozen initial entry-to-stop distance
`risk_points` already recorded per trade by the engine; `pnl_r = pnl / risk_points`.
Dollar P/L is **secondary** (fixed-share sizing imposes ATR-dependent dollar-risk
weighting).

## Primary replication criteria (frozen)

On the **SCREENED** validation view, **all three** must hold:

- **A.** long-only mean expectancy R **> 0**
- **B.** long-only mean expectancy R **>** symmetric-control mean expectancy R
- **C.** symmetric-control **SHORT-side** mean expectancy R **< 0**

**Raw sensitivity:** the raw corpus must agree on the **SIGN** of A, B, and C for a
clean replication. **No minimum-magnitude threshold** is introduced after seeing
results.

## Statistical-strength classification (frozen)

Deciding CI = the **moving-block** (serial-dependence-aware) bootstrap 95% CI of
long-only mean expectancy R (fixed seed; `tearsheet.bootstrap_ci`); the IID CI is
reported as secondary.

- **STRONG CONFIRMATION** — screened A/B/C pass, raw agrees on all three signs, and
  the long-only **block CI lower bound > 0**.
- **DIRECTIONAL REPLICATION** — screened A/B/C pass and raw agrees, but the block CI
  still includes zero.
- **FAILS VALIDATION** — any screened primary condition A/B/C fails.
- **CONFLICTED VALIDATION** — screened A/B/C pass but raw disagrees materially on any
  required sign.

These categories are **not** redefined after outcome inspection.

## Secondary diagnostics (reported, non-gating)

Trade counts; cumulative R; PF; win rate; max drawdown R; long-only-vs-symmetric
path overlap; path-created long entries; monthly consistency; best-1/5/10-trade
removal; outlier concentration; screened/raw dollar results (clearly secondary).

## Outlier rule (frozen)

Best-1/5/10 removal is **descriptive robustness evidence only** — **NOT** a
validation gate. The hypothesis is neither failed nor rescued solely because those
diagnostics change sign.

## No-rescue rule (frozen)

After this single look: no parameter change, no alternate EMA pair, no alternate
stop, no time-of-day filter, no ATR-regime filter, no alternate/shortened/extended
validation slice, no threshold shopping. **If validation FAILS, the long-only
hypothesis is PARKED.** If it DIRECTIONALLY REPLICATES or STRONGLY CONFIRMS, **STOP
for HELM disposition** before any holdout or portability work.

## Code (frozen)

| File | SHA256 |
|---|---|
| `analysis/fastalpha_engine.py` | `11af1c55db3dd0d1cbca5a489f1dbe7194344311e4ffcdc1142b9da1bcde86f5` |
| `analysis/tearsheet.py` | `c950bc6f55cfe1c7493db8ceaf38d529309e67ccd84c435b7fe60b588d0a8fb6` |
| `analysis/long_only_validation.py` | `50d57ed77c98ac76d870a9631f19fbb05acd1ff586a21590bf7ea1422733a432` |
| `analysis/test_long_only_validation.py` | `f2f18ade76fb3ba1a92100ae18a93b8fa93d195656e386d60a222297a8de36c2` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`
(hash-guarded). **No engine change** — the validation reuses the frozen engine and
standard tear sheet; the firewall end-cap lives in the validation script.

## Phase A self-verification (freeze integrity)

Before this manifest and code were committed: **no `simulate()` call, no feature
computation, and no strategy/outcome read** was performed on the validation window.
The only validation-region access was the trade-blind precondition check above
(session dates and counts, mask-timestamp dates) — no OHLC-derived outcome, no
trade, no P/L. The frozen-code classifier test (`test_long_only_validation.py`) runs
on synthetic inputs only. Result evidence is produced in Phase B and recorded solely
by dated amendment.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 long_only_validation.py        # -> LONG_ONLY_VALIDATION_2026-08-26.json
python3 test_long_only_validation.py   # frozen A/B/C + strength classifier
```

## Budget accounting (§9/§f)

One interpreted **validation** look (VDC validation class), not a development draw.
Interpreted VDC-development remains **15/18** (unchanged; unused development budget
is **not** consumed). Ledger row `OFFLINE_FASTALPHA_LONG_ONLY_VALIDATION_2026-01-06_2026-04-30`
is added in Phase B.

## Amendments

### Amendment 1 — Phase B result (2026-08-26) — **FAILS VALIDATION**

Run under the frozen pre-registration above. Evidence
`analysis/LONG_ONLY_VALIDATION_2026-08-26.json` sha256
`a8cd0d6ce841a3afd1df5a415353e85b0db75ae05622364097b9749f712fbd72`; produced by the
frozen `long_only_validation.py` (sha `50d57ed7…`) unchanged since the freeze commit.
Determinism: report JSON byte-identical across reruns. Firewall assertion: the 1m
stream was truncated at 2026-04-30 before aggregation; no bar after the validation
window entered the indicator or trade path; no embargo/holdout/hypothesis-source
outcome was computed or inspected. As pre-disclosed, the frozen mask flags 0 bars
in-window, so **screened == raw in-window** (verified: `screened_equals_raw_in_window`
= true); raw sign-agreement therefore holds by construction.

**Primary (screened, mean expectancy R):**

| quantity | value |
|---|---:|
| symmetric expectancy R | −0.05233 |
| long-only expectancy R | **−0.01872** |
| Δ expectancy R (LO − sym) | +0.03361 |
| symmetric SHORT expectancy R | −0.08977 |
| long-only block-bootstrap 95% CI (R) | **[−0.28318, +0.32338]** |
| long-only IID 95% CI (R) | [−0.26674, +0.25042] |

**Replication criteria:**

- **A. long-only mean expectancy R > 0 — FAIL** (−0.01872 < 0).
- **B. long-only > symmetric expectancy R — PASS** (−0.01872 > −0.05233).
- **C. symmetric short expectancy R < 0 — PASS** (−0.08977 < 0).
- Screened A/B/C pass: **FALSE** (A fails). Raw sign agreement: TRUE (screened==raw).

**FINAL CLASSIFICATION: `FAILS VALIDATION`.** Any screened primary condition failing
is a fail by the frozen rule; A fails.

**What replicated and what did not.** The *directional structure* did replicate
out-of-sample — removing shorts improved risk-normalized performance (B) and the
short side was strongly negative (C, −0.090 R, the worst component). But the
operative claim — that a long-only V0 has a *positive* risk-adjusted edge (A) — did
**not** hold: over the 80-session window the long book alone is **−0.019 R** per
trade, its block CI straddles zero widely [−0.28, +0.32], and only **1 of 4 months**
(April) was positive. This is consistent with the development read (edge small,
CI-straddling-zero, outlier-dependent): the asymmetry is real but the long side's
standalone expectancy is not reliably positive.

**Secondary diagnostics (non-gating).** Long-only: n=176 (symmetric 334), cumulative
R −3.29, net −$11.82, PF 0.882, win 23.3%, max-DD 43.1 R. Path-difference: **0
path-created, 0 lost, 0 changed-exit; long-entry Jaccard 1.000** — the same verified
zero-path-divergence property seen in development (V0 longs/shorts occupy
mutually-exclusive VWAP regimes), so long-only is exactly the symmetric long book.
Outlier rule (descriptive only): long-only best-10 = +53.33 (60.4% of gross profit),
net_excl_best-10 = −65.15 — noted, **not** used to fail or rescue.

**Disposition (per the frozen no-rescue rule).** The long-only hypothesis is
**PARKED.** No parameter change, no alternate EMA/stop/filter, no alternate or
resized validation slice, no threshold shopping. No holdout or portability work is
opened. Validation budget: one interpreted validation look consumed;
interpreted VDC-development remains 15/18.
