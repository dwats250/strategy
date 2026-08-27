# RUN RECORD — Long-only VDC path-dependent A/B · v1.0 · 2026-08-26

Control = V0 symmetric (long + short). Variant = V0 **long-only** (short entries
disabled; every other semantic identical). The variant was **rerun through the
engine**, not obtained by filtering shorts from the symmetric output. Frozen on
commit; corrections are dated amendments (§b/§c). Authorization: owner charge
2026-08-26, "LONG-ONLY VDC PATH-DEPENDENT A/B."

## Hypothesis provenance (binding caveat)

The long-only hypothesis is **DEVELOPMENT-GENERATED**: prior development analyses
repeatedly showed long R-expectancy positive and short R-expectancy negative,
persisting across every frozen ATR-stop arm. A favorable development result here is
therefore **not independent confirmation.**

## Firewall

Development window **2024-09-03 → 2025-12-31** only. Screened corpus (frozen
`CORPUS_MASK_v1.0`) primary; raw sensitivity. No short-only variant, no EMA change,
no stop change, no PVAE, no time-of-day or ATR-regime filter, no sizing change, no
validation, no holdout, no TradingView dependency. The only change is **short entry
permission (disabled)**; long thresholds and logic are untouched.

## Code & evidence

| File | SHA256 |
|---|---|
| `analysis/fastalpha_engine.py` | `11af1c55db3dd0d1cbca5a489f1dbe7194344311e4ffcdc1142b9da1bcde86f5` |
| `analysis/long_only_ab.py` | `1874ff93853f2a72a79d1fc7ce4b3b49d98be3c3d755b357f7f7223a5d52c358` |
| `analysis/test_fastalpha_engine.py` | `2d64d9113afb527c3db6d4a1d90daab1c60d24262243feff427e64a8020f2b06` |
| `analysis/LONG_ONLY_AB_2026-08-26.json` | `9bffb2e6239605cf7d3f5c617ceb33cbde9fcdabdaf34277a3425e60235d29b1` |

Engine change: additive `simulate(..., enable_longs=True, enable_shorts=True)`;
defaults reproduce V0 (prior results unchanged, no drift). A synthetic unit test
(`test_enable_shorts_false_creates_path_dependent_long`) proves the engine DOES
model short→long path creation, so the null path result below is a real property of
V0 data, not an engine blind spot.

## Why a rerun (not a filter)

Disabling shorts changes flat-state occupancy and could create, lose, or alter long
trades. The long-only strategy path was therefore run through the engine and the
long book compared against the symmetric control's long book.

## Symmetric vs long-only tear sheet (development)

| metric | screened ctrl | screened LO | raw ctrl | raw LO |
|---|---:|---:|---:|---:|
| trades | 1354 | 701 | 1363 | 708 |
| net $ | −86.64 | **+31.05** | −111.61 | **+17.18** |
| cumulative R | +12.19 | **+33.11** | −12.40 | **+18.88** |
| expectancy R | 0.0090 | 0.0473 | −0.0091 | 0.0267 |
| profit factor | 0.885 | **1.093** | 0.855 | **1.050** |
| win rate % | 21.7 | 27.4 | 21.4 | 26.6 |
| max drawdown R | 75.7 | **29.8** | 89.0 | **31.8** |

Long-only is directionally favorable in **both** views: positive net $ and R,
PF > 1, and roughly **half** the max R-drawdown.

## Path-difference analysis (the essential check)

Comparing the symmetric control's LONG book with the long-only rerun:

| | screened | raw |
|---|---:|---:|
| symmetric long entries | 701 | 708 |
| long-only entries | 701 | 708 |
| retained, identical exit | 701 | 708 |
| changed-exit (same entry) | 0 | 0 |
| **path-created long entries** | **0** | **0** |
| lost symmetric longs | 0 | 0 |
| long-entry Jaccard | 1.000 | 1.000 |

**Verified by rerun: ZERO path divergence.** The long-only long book coincides
exactly with the symmetric control's long book. This is a *verified* result, not the
forbidden "long-only = V0 minus shorts" assumption. Mechanism: V0 longs and shorts
occupy mutually-exclusive VWAP regimes (close > vwap vs close < vwap), and a short
exits via the thesis rule (close > vwap) at the very regime boundary where a long
could begin — so an open short never occupies a bar that a long would otherwise
take. Consequently the entire long-only-vs-symmetric difference **is** the removal
of the (net-negative) short book; the contribution of path-created trades is **0**.

## Robustness

- **Raw/screened qualitative agreement: YES** — favorable in both views.
- **Bootstrap (fixed seed):** long-only mean-expectancy 95% CI **straddles zero**
  in both $ and R (screened R-CI [−0.096, +0.208]; raw R-CI [−0.120, +0.182];
  screened $-CI [−0.097, +0.242]; raw $-CI [−0.124, +0.208]).
- **Outlier sensitivity:** the positive net does **NOT** survive removing the best
  10 trades — screened +31.05 → **−74.21**; raw +17.18 → **−88.09**.

## Disposition

**LONG-ONLY DEVELOPMENT EFFECT MODEST / UNCERTAIN.** Removing shorts turns a losing
symmetric system into a marginally positive one, consistently across raw and
screened and with far lower drawdown — but the long book's own edge is small,
statistically indistinguishable from zero (CI straddles zero in $ and R), and
outlier-dependent (best-10 removal flips it deeply negative). It is neither ABSENT
nor WORSE, and not STRONGLY FAVORABLE. Because the hypothesis is
development-generated, this is **not** confirmation.

**Validation:** a separately **pre-registered, single-look** validation appears
**plausibly warranted** — the effect is coherent (it removes the demonstrated
short-side R-drag) and consistent across views — but it must carry a realistic
(small) expected effect given the modest, outlier-dependent, CI-straddling-zero
development edge. **Validation was NOT inspected in this packet.** No rescue, no
threshold change.

## Budget accounting (§9/§f)

One new interpreted VDC-development configuration (long-only). Interpreted VDC-dev
**7 → 8 of ≤ 18**. Ledger row `OFFLINE_FASTALPHA_LONG_ONLY_dev_2024-09-03_2025-12-31`.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 long_only_ab.py            # -> LONG_ONLY_AB_2026-08-26.json
python3 test_fastalpha_engine.py   # incl. path-dependence test
```

## Recommended next SINGLE research question (not implemented)

Given the long-only edge is outlier-dependent and CI-straddling-zero, the sharpest
next question is **not** another parameter — it is **"does the long-only edge hold
out of sample?"** i.e. the one pre-registered validation look described above,
authored as its own frozen manifest before any validation data is touched.

## Amendments

*(append dated amendments here; never edit the text above in place)*
