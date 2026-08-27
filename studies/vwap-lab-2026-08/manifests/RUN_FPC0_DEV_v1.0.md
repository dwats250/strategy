# RUN RECORD — FPC-0 first development run · v1.0 · 2026-08-27

The **first FPC development configuration (FPC-0)**, authorized by owner/HELM charge
2026-08-27 on PREP HEAD `69a42ee`. FPC-0 symmetric is run against the retired VDC
symmetric V0 (benchmark/research control) on the same engine and corpus, over the
development window only. This document is a **frozen pre-registration**: the
classification below and the driver constants were fixed and committed **before any
FPC outcome was accessed**; results are recorded only by a dated **result amendment**
(§b/§c). Governing charter: `FPC_CHARTER_v0.1.md` (+ Amendment 1, owner/HELM
provenance attestation). Supersedes the PREP `RUN_FPC0_DEV_PREP_v0.1.md` for
execution.

## Owner/HELM adjudications carried in (2026-08-27)

1. **Flat-state semantics — interpretation (a) adopted.** "While flat" is part of the
   FPC signal condition: an opposing-color pullback bar met while not flat does NOT
   consume the armed opportunity; the opportunity stays armed while the same regime
   is continuously true and fires on the first subsequent opposing-color bar that is
   (a) inside the entry window and (b) flat; regime-false disarms; actual entry
   disarms. **The frozen engine already behaves this way** (engine sha
   `26e1fb07…`; `test_fpc_signals.py`), so no code change was required.
2. **H3 / first-pullback provenance** — recorded as `FPC_CHARTER_v0.1.md` Amendment 1
   (owner/HELM attestation; no historical git citation invented).

## Hypothesis (frozen)

FPC-0: *a continuation entry restricted to the FIRST opposing-color pullback after a
FRESH directional VWAP/EMA regime has better expectancy than naked VDC's repeated
opposing-candle entry rule.* Symmetric (long + short); does not inherit the failed
VDC long-only hypothesis.

## Control / variant

- **Control** = VDC symmetric V0 (`signal_mode="vdc"`), retained as benchmark only.
- **Variant** = FPC-0 (`signal_mode="fpc"`), EMA 9/20, ATR stop 1.0, entry window,
  execution, VWAP thesis exit, EOD, sizing, costs — all V0. **Only entry geometry
  differs.**

Both run through the same engine and corpus; screened (frozen `CORPUS_MASK_v1.0`)
primary, raw sensitivity.

## Firewall

Development window **2024-09-03 → 2025-12-31** only. No validation, no holdout, no
reuse of the consumed VDC validation window (2026-01-06 → 2026-04-30), no fresh
confirmation data, no embargo/hypothesis-source/holdout inspection. No EMA/stop/
window/exit/sizing/cost change from V0. No EMA50/55, PVAE, persistence/expansion
threshold, minimum pullback depth, maximum pullback delay, ATR filter, volume, RSI,
ADX, time-of-day optimization, long-only, or alternate stop/target (charter §6). No
TradingView dependency, no CuttingBoard contact, no merge.

## Primary metric & FROZEN classification (before outcome access)

Primary metric: **mean trade expectancy in R** (1R = frozen initial entry-to-stop).
`delta_R = FPC mean expectancy R − VDC mean expectancy R`. Materiality convention
**MATERIAL_R = 0.03** (unchanged from the ATR-stop / EMA surfaces).

- **FPC DEVELOPMENT BETTER** — screened `delta_R > +0.03` AND raw `delta_R > 0`.
- **FPC DEVELOPMENT WORSE** — screened `delta_R < −0.03` AND raw `delta_R < 0`.
- **FPC DEVELOPMENT NEUTRAL** — screened `delta_R ∈ [−0.03, +0.03]`.
- **FPC DEVELOPMENT CONFLICTED** — screened shows a material move but raw moves in the
  opposite direction.

FPC's **absolute** mean expectancy R is reported separately: a relative improvement
from negative to less-negative is **not** a positive edge. These categories are not
redefined after outcome inspection.

## FPC-specific invariants (verified mechanically from the real run)

`fpc0_dev.py` asserts, from the produced trade set: ≤ 1 FPC signal per continuous
regime; no FPC signal on a fresh-regime start bar. The remaining invariants
(regime-break disarms; actual entry disarms; out-of-window opposing-color bar does
not consume; non-flat opposing-color bar does not consume; later fresh regime
re-arms) are proven by `test_fpc_signals.py` (8 cases, incl. a VDC(2)-vs-FPC(1)
contrast).

## Reported quantities (frozen list)

Standard tear sheet + `ab_dual`: FPC & VDC trade counts, dropped-entry count, % of VDC
entries suppressed, entries unique to FPC, mean expectancy R, delta R vs VDC,
cumulative R, net $, PF, win rate, max-DD R, avg/median hold, bootstrap CI (\$ and R),
monthly consistency, outlier concentration, raw/screened agreement; long/short
decomposition (N / expectancy R / PF); and the entry-geometry statistics (continuous
bull/bear regime counts, how many produced a signal, bars-from-fresh-to-signal
distribution, proportion of VDC entries retained, VDC entries removed by the
one-per-regime rule). Symmetry is not changed based on results; no delay/max-wait
threshold is optimized.

## Code (frozen)

| File | SHA256 |
|---|---|
| `analysis/fastalpha_engine.py` | `26e1fb07641b35deb8461cf7d3af45d25eefcf45462e66448a4c390cba5f5b0e` |
| `analysis/tearsheet.py` | `c950bc6f55cfe1c7493db8ceaf38d529309e67ccd84c435b7fe60b588d0a8fb6` |
| `analysis/fpc0_dev.py` | `abd18d2ef3d518735cd0b508749445db9b996d382a52bcc98c62aa7839d81033` |
| `analysis/test_fpc_signals.py` | `074e73fcb78b9c992e4e17b8f4607e242fd106a88adb7d7f60a7bc5d67a715d5` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`.

## Budget (§9/§f)

Executing this run spends **FPC configuration 1 of ≤ 12** — FPC-dev **0 → 1/12** —
recorded as a `family=FPC, budget_class=development` ledger row in the result
amendment. Independent of the retired VDC budget (VDC stays **15/18**, unused slots
intentionally unused).

## No rescue (frozen)

Single configuration. If FPC-0 is NEUTRAL or WORSE: report and stop. If BETTER: report
and stop **before** designing FPC-1. No additional structure (charter §6); no second
FPC configuration is spent in this packet.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 fpc0_dev.py            # -> FPC0_DEV_2026-08-27.json
python3 test_fpc_signals.py    # FPC signal invariants
```

## Amendments

### Amendment 1 — result (2026-08-27) — **FPC DEVELOPMENT WORSE**

Run under the frozen pre-registration above; driver `fpc0_dev.py` unchanged since the
freeze commit `be03f0c`. Evidence `analysis/FPC0_DEV_2026-08-27.json` sha256
`eaa00e6d639ffcb8b2479f502fdfc9b875d30ef2956317e35631dcb72d409eb9`. Determinism:
report JSON byte-identical across reruns. FPC invariants asserted from the real trade
set (run exits 0): ≤ 1 FPC signal per continuous regime; no FPC signal on a
fresh-regime bar.

**Primary (mean expectancy R):**

| view | VDC expR | FPC expR | **delta_R (FPC−VDC)** |
|---|---:|---:|---:|
| screened (primary) | +0.00900 | −0.02319 | **−0.03219** |
| raw (sensitivity) | −0.00910 | −0.03961 | **−0.03051** |

Screened `delta_R = −0.03219` is below **−MATERIAL_R (−0.03)** and raw `delta_R =
−0.03051 < 0` agrees on sign → **FPC DEVELOPMENT WORSE.** FPC's **absolute** screened
expectancy R is **−0.02319** (negative), so this is not "negative→positive": the
first-pullback restriction makes risk-normalized expectancy *worse*, not better.

**Full tear sheet (screened primary):**

| metric | VDC | FPC-0 |
|---|---:|---:|
| trades | 1354 | 1069 |
| cumulative R | +12.19 | −24.79 |
| net $ | −86.64 | −43.65 |
| profit factor | 0.885 | 0.921 |
| win rate % | 21.71 | 21.05 |
| max drawdown R | 75.72 | 74.57 |
| avg / median hold (bars) | 12.6 / 5 | 12.6 / 4 |
| profitable months | 5 / 16 | 6 / 16 |
| best-10 % of gross | 21.95 | 25.76 |
| net_excl_best_10 (R-space via $) | −233.70 | −174.24 |
| long-only bootstrap block CI (R) | [−0.093, +0.118] | [−0.134, +0.099] |

**Direction (from the symmetric result):**

| side | VDC expR / PF | FPC expR / PF |
|---|---:|---:|
| long (screened) | +0.04723 / 1.075 (n=701) | +0.01436 / 1.022 (n=565) |
| short (screened) | −0.03204 / 0.950 (n=653) | −0.06529 / 0.900 (n=504) |
| long (raw) | +0.02666 (n=708) | −0.00095 (n=567) |
| short (raw) | −0.04776 (n=655) | −0.08310 (n=504) |

The first-pullback restriction lowers expectancy R on **both** sides (long
+0.047→+0.014, short −0.032→−0.065 screened) — VDC's later same-regime pullbacks were
not, on average, worse than the first, so removing them (and adding path-created
entries) hurts R. The $ improvement (−86.64→−43.65) is the familiar fixed-share
sizing artifact (fewer trades), **not** the primary metric.

**Entry geometry & diff (screened; raw materially identical):**

- VDC 1354 entries → FPC 1069: **retained 980 (72.4%)**, **dropped by the one-per-
  regime rule 374 (27.6% suppressed)**, **89 entries unique to FPC** (path-created:
  FPC's different flat-occupancy opens entries VDC never took — FPC is a
  path-dependent restriction, not a strict subset).
- Continuous **bullish** regimes **908**, **565 produced a long signal (62.2%)**;
  **bearish** regimes **807**, **504 signalled (62.5%)**.
- Bars from fresh-regime start to signal: **median 2** (both sides), mode 1, tail to
  21 (long) / 9 (short) — pullbacks arrive quickly; ~38% of regimes never produce an
  orderly first pullback while flat and in-window.

**raw/screened agreement: YES** (both views WORSE; `ab_dual` direction agreement
true). Every arm's bootstrap mean-expectancy CI straddles zero and `net_excl_best_10`
stays deeply negative — the whole comparison remains statistically weak in absolute
terms; the *relative* verdict (FPC worse than VDC in R) is the material, view-
consistent finding.

**Disposition (frozen no-rescue rule).** FPC-0 is **WORSE** than the VDC benchmark in
risk-normalized expectancy, consistently across screened and raw. **Report and
stop.** No FPC-1 is designed; no additional structure (charter §6); no second FPC
configuration is spent. FPC-dev budget **0 → 1/12** (config 1 consumed). Ledger row
`FPC0_DEV_2024-09-03_2025-12-31`.
