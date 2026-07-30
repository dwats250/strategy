# Proxy findings — RUN_SPY_1D_2015-01-01

Status: `PUBLISHED 2026-07-30 UTC — descriptive findings for one registered run`

Run record: `../manifests/RUN_SPY_1D_2015-01-01.md` (FROZEN). Export:
`../exports/CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv`, SHA-256
`d1b537506ed1cec9559ad9dd66a35d4a9798d751ee1896e07e6e1739dfe0b970`. Ledger row 1 of
`../LEDGER.csv`. Instantiated from `../manifests/FINDINGS_TEMPLATE_v0.1.md`.

---

## 0. The separation — restated

| | Proxy behaviour (this study) | Live-engine evidence (the closed audit) |
|---|---|---|
| What it is | What the mapped gate semantics do on declared TradingView chart history | What the pinned engine did under enforced isolation |
| Where it lives | `studies/cuttingboard-asis-proxy/` | `audits/cuttingboard-engine-strategy-audit/` |
| What it can support | Descriptive frequency, funnel, gate behaviour, chronology | Structural mapping, replay determinism, observability limits |
| What it can never support | Profitability, edge, live equivalence, accepted-path claims | Strategy quality, profitability, accepted-trade metrics |

No finding here may be carried back into the closed audit, and no audit record may be cited as
evidence that a proxy result reflects live behaviour.

## 1. Descriptive outputs

### 1.1 Signal / opportunity frequency

Denominator: 2,909 daily bars, 2015-01-01 → 2026-07-29, AMEX:SPY RTH, from the registered export.

| Classification | Count | Rate |
|---|---:|---:|
| QUALIFIED | 170 (125 long / 45 short) | 5.8 % of bars |
| WATCHLIST | 239 (179 long / 60 short) | 8.2 % of bars |
| REJECT | 2,500 | 85.9 % of bars |
| Kill-switch bars (within REJECT) | 204 | 7.0 % of bars |

### 1.2 Evaluated → qualified funnel

2,909 bars evaluated → 602 hard-gate pass (g1–g4) → 579 hard-pass and not kill-switched →
170 QUALIFIED (zero soft misses) + 239 WATCHLIST (exactly one) + 170 soft-REJECT (two misses).
23 hard-pass bars were kill-switched.

**"Emitted" stops at qualified.** The proxy has no chain validation and no decision chain, so
there is no emitted-trade stage.

### 1.3 Gates: decisive, inert, overlapping

First-rejection distribution (sums to 2,909): none 170; kill-switch 204; g1 regime 1,988;
g4 structure 138; g6 stop-distance 273; g10 extension 136.

- **Decisive:** g1 regime — 68.3 % of all bars are first rejected here. Kill switch (204),
  g6 stop-distance (273 first rejections), g4 structure (138), g10 extension (136) each bind a
  material share.
- **Inert:** g2 confidence and g3 direction never appear as a first rejection in this window.
  g5 stop-defined cannot fail given the deterministic geometry (structural); g9 earnings is
  fail-open by construction; g7 rr never failed — the rr = 2.0 floating-point boundary
  (mapping §3.2) resolved as pass on every hard-pass bar observed. Inert here does not mean
  redundant: one symbol, one window.
- **Overlapping:** g6 and g10 fail together on 170 hard-pass non-kill bars (g6-only 103,
  g10-only 136, both 170).

### 1.4 Chronology of representative signals

First QUALIFIED bars of the window: 2015-01-22 (long), 2015-02-03 (long), 2015-03-18 (long).
Most recent: 2026-07-09, 2026-07-10, 2026-07-15 (all long). Per-year QUALIFIED counts range
from 28 (2025) down to 4 (2016) and **0 (2017)** — 2017 nonetheless carries 23 WATCHLIST bars,
so the attention stream was not empty; the strict zero-miss bar was simply never reached.
Descriptive only; not a trade log.

### 1.5 Unrecoverable gaps and limitations

No manifest field was `UNRECOVERABLE` for this run. Standing limitations in force, per the
frozen manifest: Gate 8 and Gate 11 NOT REPRESENTABLE (excluded from the soft count, never
counted as passing); `EXPANSION`, CONTINUATION, and PULLBACK_IMBALANCE not represented; chain
validation and the decision chain not represented (accepted path unobservable, as in EA-6-006);
`volume_ratio` and `ema_spread_pct` are approximations. Run-specific: the export contains 3,619
of the 8,431 bars loaded in the chart series (TradingView emits only fetched bars); the declared
2015-01-01 analysis window is fully covered with ~3 years of prior warm-up data, and the
on-chart full-series funnel table (since 1993) is corroborating display evidence only. A first
capture attempt covering only 2023-02-13 onward was rejected and archived outside the
repository.

## 2. Boundary checks

- [x] No profitability, edge, expectancy, or future-performance claim anywhere.
- [x] No claim of equivalence to a live CuttingBoard run.
- [x] No accepted-path claim.
- [x] Gate 8 and Gate 11 reported as NOT REPRESENTABLE, not as passing.
- [x] `EXPANSION`, CONTINUATION, PULLBACK_IMBALANCE reported as not represented.
- [x] `volume_ratio` and `ema_spread_pct` labelled approximations.
- [x] Gate 6 and Gate 7 boundary behaviour reported as observed (g7 always passed at the 2.0
      boundary; g6 failures observed), not assumed.
- [x] No trading recommendation of any kind.
- [x] Every number traces to the export with SHA-256 `d1b53750…` (this study) or the v0.5
      export with SHA-256 `e28aa874…` (exploratory packet).

## 3. Uncertainty

- Per-bar agreement with v0.5 (§4) was measured on two different chart feeds (NYSE Arca vs
  BATS) over daily bars; it demonstrates that the daily-bar gate arithmetic is insensitive to
  that feed difference on this window. It says nothing about live-engine equivalence.
- The g7 rr = 2.0 boundary never bound in this window, so the floating-point boundary doubt
  recorded in mapping §3.2 remains unexercised, not resolved.
- Gate inertness (g2, g3) is an observation about SPY 1D over 2015–2026 only.

## 4. Compact comparison — AS-IS proxy vs exploratory v0.5

Comparison basis: row-level join on UTC bar date, 2015-01-01 → 2026-07-28 (v0.5 export ends
2026-07-28; the proxy's additional 2026-07-29 bar is excluded). Inputs: this run's export
(`d1b53750…`, AMEX:SPY) and the v0.5 canonical export (`e28aa874…`, BATS:SPY) in
`exploratory/cuttingboard-candidate-fidelity-v0_5/`. v0.5 is exploratory diagnostic evidence
only.

| Dimension | Common bars | Disagreements |
|---|---:|---:|
| Bar-date coverage | 2,908 | 0 in either direction |
| v0.5 V2 candidate vs proxy hard-gate pass | 2,908 | **0** (602 = 602) |
| Kill switch | 2,908 | **0** |
| v0.5 stop-distance pass vs g6 (hard-pass, non-kill bars) | 579 | **0** |
| v0.5 extension pass vs g10 (hard-pass, non-kill bars) | 579 | **0** |
| v0.5 V4 candidate vs proxy QUALIFIED | 2,908 | **0** (170 = 170, 125L/45S both) |
| v0.5 single-miss bars vs proxy WATCHLIST | 579 | **0** (239 = 239) |

Reading: the two implementations are **bar-for-bar identical on every comparable stage** of the
candidate funnel, across different chart feeds. The only difference between them is
classification policy, exactly as recorded in the exploratory packet: v0.5 required both soft
checks to pass (hard AND) and therefore discarded the 239 single-miss bars that the documented
soft-gate semantics classify WATCHLIST. The AS-IS proxy surfaces them. This settles the
candidate-classification fidelity question this study was built to answer: the intended
QUALIFIED / WATCHLIST / REJECT classifications are visible, internally consistent, and
reproducible on declared chart history.
