# RUN RECORD — Compact EMA fast/slow response surface · v1.0 · 2026-08-26

A frozen **3×3 EMA-length grid** around the existing V0 control (EMA 9/20), run
with naked **symmetric** VDC. Only the trading EMA fast/slow lengths change; every
other V0 semantic is identical. This is a **robustness / local-topology** probe,
**not** an optimization — no production pair is selected and no
intermediate/neighbouring length is added after seeing results. Frozen on commit;
corrections are dated amendments (§b/§c). Authorization: owner charge 2026-08-26,
"COMPACT EMA RESPONSE SURFACE."

## Firewall (binding)

Development window **2024-09-03 → 2025-12-31** only. Screened corpus (frozen
`CORPUS_MASK_v1.0`) primary; raw sensitivity. The **only** change is EMA fast/slow
length. No `ATR_STOP_MULT` change (stays 1.0), no trigger/entry-window/stop/thesis/
EOD/sizing/execution/cost change, no PVAE, no time-of-day or ATR-regime filter, no
long-only rerun, no validation, no holdout, no embargo inspection, no TradingView
dependency.

## Frozen grid (declared before any outcome inspection)

`fast ∈ {8, 9, 10}` × `slow ∈ {18, 20, 22}` = **9 cells**, encoded as predeclared
constants in `ema_surface.py`:

```
        slow 18   slow 20        slow 22
fast 8   8/18      8/20           8/22
fast 9   9/18      9/20 [CTRL]    9/22
fast 10  10/18     10/20          10/22 [EXPLORED]
```

- **9/20** = existing V0 control — **no new budget draw.**
- **10/22** = already explored (V0/V1 A/B) — **no new budget draw.**
- The remaining **seven** cells are new interpreted VDC-development configs.

Predeclared classification threshold **MATERIAL_R = 0.03** R/trade (economic
materiality on the risk-normalized primary metric; the same value frozen for the
ATR-stop surface, reused unchanged).

## Inputs & code

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`
(hash-guarded by `parity_foundation`). Screened view = frozen `CORPUS_MASK_v1.0`
(9 HIGH-CONFIDENCE bars).

| File | SHA256 |
|---|---|
| `analysis/fastalpha_engine.py` | `11af1c55db3dd0d1cbca5a489f1dbe7194344311e4ffcdc1142b9da1bcde86f5` |
| `analysis/tearsheet.py` | `c950bc6f55cfe1c7493db8ceaf38d529309e67ccd84c435b7fe60b588d0a8fb6` |
| `analysis/ema_surface.py` | `6ff838fb8cdcb48b4e3efd76a55e48ce575bb7b682d654e2ec330bfe7870de01` |
| `analysis/test_ema_surface.py` | `351e0944c13a21fd5f389c71487b125314034d405cd78f5fd482bdc0859eda05` |
| `analysis/EMA_SURFACE_2026-08-26.json` | `6010a894c268b01aa4e87e4543cc262efbc3aaa405982b4adc873fa39dbf5151` |
| `analysis/EMA_SURFACE_2026-08-26.csv` | `982ad1b88c6f54c48e39c59ecfcc3836d553403e9317af6bde8e4e2d02bf150b` |

**No engine or tearsheet change was required or made** — the EMA-pair sweep uses
the pre-existing `compute_feature_rows(fast, slow, drop_t_ms=)` seam and the
existing tear-sheet metrics. The engine and tearsheet shas above are byte-identical
to the long-only packet, so every prior committed result is unchanged.

Determinism: each cell is simulated twice and the serialized trade lists are
byte-identical; the full report JSON is byte-stable across whole-script reruns
(fixed bootstrap seed).

## Response surface — screened (PRIMARY)

Pooled per-cell metrics (both directions), fixed 1-share sizing, `ATR_STOP_MULT`
1.0. Full table in `EMA_SURFACE_2026-08-26.csv`.

| cell | n | net $ | cum R | **exp R** | PF | win% | max-DD R |
|---|--:|--:|--:|--:|--:|--:|--:|
| 8/18 | 1376 | −101.33 | 1.05 | 0.00076 | 0.869 | 21.4 | 82.4 |
| 8/20 | 1366 | −93.62 | 3.58 | 0.00262 | 0.877 | 21.4 | 77.9 |
| 8/22 | 1359 | −89.39 | 9.92 | 0.00730 | 0.882 | 21.6 | 75.2 |
| 9/18 | 1372 | −99.06 | 1.40 | 0.00102 | 0.871 | 21.4 | 78.0 |
| **9/20** [CTRL] | 1354 | −86.64 | 12.19 | **0.00900** | 0.885 | 21.7 | 75.7 |
| 9/22 | 1357 | −85.66 | 7.31 | 0.00539 | 0.886 | 21.7 | 74.1 |
| 10/18 | 1359 | −91.08 | 8.63 | 0.00635 | 0.880 | 21.7 | 76.3 |
| 10/20 | 1357 | −88.34 | 4.37 | 0.00322 | 0.883 | 21.6 | 75.0 |
| 10/22 [EXPL] | 1357 | −89.67 | −0.87 | −0.00064 | 0.881 | 21.7 | 75.5 |

**Raw (sensitivity)** — same shape, uniformly lower (bad ticks): exp R spans
[−0.0186 (10/22) … −0.0091 (9/20)], all nine net-negative in $ (−110.6 … −126.4),
and **9/20 is again the least-negative cell**. Raw/screened agree on the sign of
(cell − control) for **0 of 8** non-control cells (fully directionally consistent).

## Directional decomposition (from the SYMMETRIC result; no long-only rerun)

| | screened | raw |
|---|--:|--:|
| cells with **long** expectancy R **> 0** | **9 / 9** | **9 / 9** |
| cells with **short** expectancy R **< 0** | **9 / 9** | **9 / 9** |
| long expectancy R range | +0.032 … +0.047 | +0.012 … +0.027 |
| short expectancy R range | −0.030 … −0.040 | −0.046 … −0.056 |

The long-positive / short-negative asymmetry holds in **every cell of the
neighbourhood, in both views** — descriptive evidence **supporting** the existing
long-only development candidate. **Not promoted to confirmation** (this packet ran
no long-only strategy and inspected no validation).

## Topology classification (descriptive; no cell selected)

- Pooled **expectancy R range 0.00964 R across all nine cells** (min −0.00064 at
  10/22, max +0.00900 at 9/20), **median +0.00322 R** — the whole grid lies inside
  **one 0.0096 R band, < MATERIAL_R 0.03**.
- **All nine cells are within MATERIAL_R of the best and form one contiguous
  block.** Max adjacent-cell jump **0.00798 R**; both axis marginals are
  sub-material (fast spread 0.0022 R, slow spread 0.0022 R) and non-monotone.
- No isolated peak (best 9/20 leads its neighbours by < MATERIAL_R) and no isolated
  trough.
- **Response shape: `5. FLAT / PARAMETER-INSENSITIVE`.** In risk-adjusted (R) terms
  the EMA fast/slow lengths in this neighbourhood have **no material effect**.
- **Control 9/20 lies within the stable region** — it is in fact the top R-cell of
  the flat band (gap below best 0.0 R), so the source's chosen pair is well-placed.
- **10/22's prior NEUTRAL result is consistent with the surface** (delta vs control
  −0.0096 R, sub-material) — the V0/V1 A/B is corroborated by the wider grid.
- Every cell's bootstrap mean-expectancy CI **straddles zero** in $ and R, and
  `net_excl_best_10` is deeply negative for **every** cell (−233 … −248 screened) —
  the marginal R-positivity is outlier-dependent and statistically indistinguishable
  from zero across the whole family (the same fragility seen for long-only).

### Disposition

**EMA SURFACE PARAMETER-INSENSITIVE.** Directional asymmetry **PERSISTENT.**

The EMA-length neighbourhood around 9/20 is a flat, smooth, view-consistent plateau
with no material risk-adjusted structure and no fragile optimum to chase; the
control pair is well-placed within it, and 10/22's earlier neutral finding is
confirmed by the surrounding grid. The one robust, coherent feature is the
long-positive / short-negative asymmetry, which persists in every cell of the
neighbourhood and in both corpus views — reinforcing (not confirming) the standing
long-only candidate. **No production EMA pair is selected; no intermediate or
neighbouring length is interpolated or tested.**

## Budget accounting (§9/§f) & multiple testing

- **9/20** = existing V0 control — **no new draw.**
- **10/22** = already explored — **no new draw.**
- **8/18, 8/20, 8/22, 9/18, 9/22, 10/18, 10/20** = seven new interpreted
  VDC-development configurations. Interpreted VDC-dev runs **8 → 15 of ≤ 18**. Each
  of the seven is recorded in the ledger as an **explored candidate** — this grid is
  **not** counted as "one test."
- No post-hoc interpolation: 7/17, 11/24, and all intermediate lengths were **not**
  tested; the within-band cell ranking is recorded as an observation only.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 ema_surface.py          # -> EMA_SURFACE_2026-08-26.json + .csv
python3 test_ema_surface.py     # classifier branches on synthetic surfaces
```

## Recommended next SINGLE research question (not implemented)

Three independent development probes now converge on the same picture: the naked
symmetric VDC family is **risk-neutral-flat** to both stop width and EMA length,
while a **persistent long-positive / short-negative asymmetry** is its one coherent
structural feature. The sharpest next question is therefore **not** another
development parameter — it is the already-identified **pre-registered, single-look
validation of the long-only hypothesis**, authored as its own frozen manifest
before any validation data is touched. This surface strengthens the rationale for
that look (the asymmetry is stable across the EMA neighbourhood) but does **not**
lower the bar: the development long-only edge remains small, CI-straddling-zero, and
outlier-dependent.

## Amendments

*(append dated amendments here; never edit the text above in place)*
