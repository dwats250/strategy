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

### Amendment 1 — 2026-08-26 · Capture supplied · IDENTITY GATE FAIL — STOP (wrong window)

Owner supplied two files on 2026-08-26 for the R1 capture:

- Trade list: `VWAP_FastAlpha_v0_AMEX_SPY_20260826.csv`
  sha256 `dd7433f1b833ce6d40093d083cf1ade007fc9b77d9bc5fdfeb558c26f81f827d`
- Chart data: `BATS_SPY_5.csv`
  sha256 `f5d3c5b44a29923c4d69b92401e604a3c949e7277a6ed9f15315dfacd3cbead4`

**Mechanical identity gate (the only authorized analysis) result: FAIL — STOP (A1.8).**
Selftest PASS. Gate on the supplied trade list vs the preserved R0 reference:

```
R0 rows=2662 trades=1331   (dev window 2024-09-03 → 2025-12-31)
R1 rows=1320 trades=660    (supplied capture)
→ ROW/TRADE COUNT divergence; exit 2
```

The gate returned early on the count divergence; no per-trade P/L cell was read or
printed. No validation-window outcome was inspected or interpreted.

**First divergence, classified: execution-context / loaded-range mismatch (not an
instrumentation-induced behavior change, not an export-format difference).** The supplied
trade list does not cover the development window. Its first trade is dated **2025-12-31**
and its trades run forward to **2026-08-25** (660 trades) — i.e. the capture's strategy-tester
range began at the development window's final day and ran forward through the **embargo
(2026-01-02 / 2026-01-05)**, the **sealed validation window (2026-01-06 → 2026-04-30)**, and
beyond. The development window 2024-09-03 → 2025-12-31 (1,331 trades) is absent; the two
ranges overlap only on the single day 2025-12-31.

**Corroborating evidence that the wrong artifact was captured (inferential, not the gate
verdict):** (1) the trade-list export filename carries `v0`, the R0 short-title, not `v0R1`;
(2) the chart-data header is
`time,open,high,low,close,Volume,Session VWAP,EMA 9,EMA 20,Long Fast-Alpha Signal,Short
Fast-Alpha Signal` — it carries Volume but **none of the ten instrumentation columns**
(`ACCEPT_STATE_DIR` … `ORDERED_10_22_55`). That column set is the base v0 plot set, consistent
with the base `VWAP_Continuation_FastAlpha_v0.pine` rather than the R1 instrumented source. So
this looks like the base v0 script captured over a recent (validation-forward) range, not the
R1 instrumented source over the development range.

**Firewall action (A3):** because the supplied files physically contain sealed
validation-window rows (trade outcomes in the trade list; OHLCV/indicator bars in the chart
data), they were **withheld from `../exports/` and not committed** — recording a validation
capture into the development repo would breach the A3 firewall. The files are referenced here
by name and sha256 only. No ledger row is written: no run was admitted, none was interpreted,
and **no §9 budget slot is drawn** (SEALED-UNINTERPRETED; A1.7). The contingency in this
manifest (display-only `display =` change for missing instrumentation columns) is **not**
triggered — the missing columns are a symptom of the wrong artifact/window, not a display-export
gap to patch; nothing in this repo is changed in response.

**Re-capture required — exact requirements (unchanged from this manifest):** load the R1
instrumented source `../scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine`
(sha256 `32aaaa4d2148186774921c8529c5ab3600bfe4110ffff2fd0213a6631ff72bc4`) — confirm the strategy
short-title reads **`VWAP FastAlpha v0R1`** — on AMEX:SPY, 5m, RTH, exchange timezone, ADJ on,
all R0 Properties; set the strategy-tester / Deep Backtesting range to **2024-09-03 → 2025-12-31
inclusive** and confirm it yields **1,331 trades** before exporting; keep Volume on the chart;
export the List of Trades CSV and the chart-data CSV and confirm the ten instrumentation columns
are present. The identity gate is re-run on the re-capture; nothing else proceeds until it PASSES.

### Amendment 3 — 2026-08-26 · FIRST UNSEALING · PVAE development analysis · SYMMETRIC PVAE PARKED (rule C)

**Authority.** Owner/HELM development-unseal charge of 2026-08-26 — authorizes unsealing the R1
DEVELOPMENT capture only, as one interpreted VDC-development draw under the frozen §9 budget, to
run exactly the frozen PVAE primary comparison. Firewall reaffirmed: development only
(2024-09-03 → 2025-12-31); embargo, validation, unused buffer, hypothesis-source, and holdout
untouched; no new TradingView run; no frozen definition or threshold changed.

**§9 budget draw (A1.7 dated note).** This is the first unsealing of this SEALED-UNINTERPRETED
capture, so the interpreted-run budget slot is now drawn. **VDC development interpreted runs: 2 of
≤ 18** (R0 = 1; this R1 unsealing = 2). Per A1.7 the prior SEALED-UNINTERPRETED ledger row and
Amendment 2 are **not** rewritten; the draw is recorded here and by an appended interpreted-run
ledger row (`…_v0R1_UNSEAL_PVAE`).

**Method (frozen prereg executed, not amended).** Covariates were read from the frozen R1
instrumentation mirror (`../analysis/instrumentation_r1.py`) over the hash-guarded local SPY
corpus (foundation columns byte-identical to R0; containment re-verified: 24 columns identical
across 38,357 rows). The supplied R1 chart-data export is only a 300-bar recent visible-window
sample, so the local mirror is the R1 observational state for development bars. Each trade was
joined to its **signal bar = entry-fill time − 5m** (the frozen R0-parity Gate-3 timing). All
1,331 trades joined; **group P/L reconciles exactly to the R0 headline** (long +43.68, short
−17.99, net +25.69) — a complete, conservative join. Analysis tool:
`../analysis/pvae_dev_analysis_r1_v1.0.py`; evidence `../analysis/PVAE_DEV_RESULTS_2026-08-26.json`.

**Frozen S_9_20_50 development-entry tercile boundaries (computed once, from the S_t distribution
only — no P/L, side, or outcome used; recorded before inspecting conditional outcomes):**

```
method : count-based split of pooled defined naked-VDC entry S_9_20_50;
         b_lo = sorted[floor(N/3)], b_hi = sorted[floor(2N/3)] (0-indexed);
         upper development-entry tercile = S_t >= b_hi
N (defined entry S_t) : 1330   (1 entry undefined at warm-up; excluded from ranking)
b_lo (lower boundary) : 0.5320216540492776
b_hi (UPPER boundary) : 1.3297578122368192
tercile counts        : lower 443 · middle 443 · upper 444
```

These boundaries are frozen and are the ones reused unchanged for the single sealed validation
look if and when it is ever earned (A1.4).

**PVAE classification (all five frozen conditions; A1.2 acceptance + A1.4 ordering / upper tercile
/ expansion / persistence ≥ 2). Condition funnel over 1,331 trades:**

```
accept (ESTABLISHED, correct dir)            1121
  + ordered EMA 9>20>50 (dir)                 730
    + S_t in upper tercile                     352
      + expanding (S_t > S_{t-2})              273
        + persistence >= 2  = PVAE            263
```

Qualified **PVAE N = 263**, non-PVAE N = 1068 (54 entries carried ≥1 undefined covariate at
warm-up and cannot qualify).

**Primary comparison — per-trade expectancy (Net PnL USD), PVAE vs other:**

| Split | PVAE n | PVAE exp | PVAE win | other n | other exp | other win | contrast (PVAE−other) | ex-top-trade |
|---|---|---|---|---|---|---|---|---|
| pooled | 263 | +0.0234 | 23.95% | 1068 | +0.0183 | 21.72% | **+0.0051** | +0.0050 |
| long | 162 | −0.0006 | 25.31% | 535 | +0.0818 | 22.62% | **−0.0824** | −0.0224 |
| short | 101 | +0.0619 | 21.78% | 533 | −0.0455 | 20.83% | **+0.1074** | +0.0388 |

**Park-rule evaluation (frozen; no rescue):**

- **A** (qualified N < 30): **NO** — N = 263.
- **B** (pooled contrast ≤ 0): **NO** — pooled contrast = +0.0051.
- **C** (long and short contrast signs disagree): **YES** — long −0.0824, short +0.1074.
  **This governs.**
- **D** (positive only after changing the tercile rule / persistence ≥ 2 / acceptance rule): **n/a**
  — nothing was changed or threshold-shopped; the primary was computed once under frozen
  definitions.
- **E** (validation): **not evaluated** — validation remains sealed.

**DEVELOPMENT DISPOSITION: SYMMETRIC PVAE PARKED (rule C).** The symmetric-PVAE hypothesis requires
the contrast to agree in sign across sides; here the long-side contrast is negative while the
short-side contrast is positive, so the symmetric hypothesis is parked without rescue. Although the
pooled contrast is marginally positive (+0.0051), it is carried entirely by the short side and does
not satisfy the frozen symmetry requirement. Per PVAE-prereg §5.C an asymmetric (short-only)
variant is **not** created now; it may only be separately pre-registered as future research. No
rule, threshold, persistence value, or acceptance definition is moved on this result.

**ONE PLANNED VALIDATION LOOK: NOT EARNED.** No validation capture is unsealed; the R2 validation
window (2026-01-06 → 2026-04-30) remains sealed and untouched.

**Secondary observational covariates (descriptive only — no thresholds, no optimization, not a
hypothesis):** PVAE vs all-entries means — `RecentShock` 1.78 vs 1.72; `S_10_22_55` 2.64 vs 1.27;
`ordered_10_22_55` agrees with trade side 100% (PVAE) vs 62.3% (all). Reported as context; nothing
is promoted or filtered on them.

**Feed-seam caveat (recorded, not repaired).** Covariates come from the split-only local corpus,
whereas TradingView R0/R1 is dividend-adjusted (ADJ); near a threshold a covariate may differ from
the exact TV stamp. Exposure is bounded and descriptive: 43 entries sit within ±5% of the upper
tercile boundary, and the R0 parity probe recorded 53/1331 near-threshold VDC-candidate flips. This
seam does not change the disposition — the governing fact is the long/short sign disagreement, and
the sides differ by far more than seam-scale perturbation — but it is a standing limitation on the
exactness of the covariate stamps and is noted for any future validation decision.

### Amendment 2 — 2026-08-26 · Corrected re-capture supplied · IDENTITY GATE PASS — R1 ADMISSIBLE (SEALED-UNINTERPRETED)

Owner supplied the corrected R1 capture on 2026-08-26 (the re-capture required by Amendment 1).
Both files preserved byte-identical under `../exports/`:

- Trade list: `../exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0R1.csv`
  sha256 `8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241`
  (source filename `VWAPFAv0R1_AMEX_SPY_2026-08-26.csv`)
- Chart data: `../exports/TV_CHARTDATA_BATS_SPY_5m_RTH_2026-08-21_2026-08-26_FastAlphaV0R1_instrumented_sample.csv`
  sha256 `e0e3d432203cceb5673eb726fe56f0ee14412d5d09ebda018817ffea65870df4`
  (source filename `BATS_SPY, 5 (3).csv`)

**Mechanical identity gate (the only authorized analysis) result: PASS — R1 ADMISSIBLE (A1.8).**
Selftest PASS. Gate on the supplied trade list vs the preserved R0 reference:

```
R0 reference exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv  sha256 8d2db8dc…
R1 candidate exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0R1.csv sha256 8d2db8dc…
IDENTITY GATE PASS: 1331 trades; side, timestamps, prices, and P/L identical
  under the pre-registered normalization.
R1 ADMISSIBLE (SEALED-UNINTERPRETED); exit 0
```

The R1 trade list is **byte-identical to the preserved R0 export** (same sha256; `cmp` clean) —
the strongest possible form of the identity requirement: the R1 instrumentation did not alter
trading behavior down to the byte. Trade #1 is dated 2024-09-03 and trade #1331 is dated
2025-12-31 — exactly the frozen development window; no embargo/validation/holdout rows are present
in the trade list.

**Chart-data header check: PASS.** Header carries Volume and **all ten** instrumentation columns
(`ACCEPT_STATE_DIR`, `EMA50`, `S_9_20_50`, `ORDERED_9_20_50`, `EXPANDING_9_20_50`,
`ALIGNED_EXP_COUNT_9_20_50`, `SHOCK_RATIO`, `RECENT_SHOCK`, `S_10_22_55`, `ORDERED_10_22_55`).
This corrects the Amendment-1 symptom (base-v0 column set) — the R1 instrumented source was run.
The chart-data export is a 300-bar visible-window sample spanning 2026-08-21 10:30 → 2026-08-26
15:55 America/New_York; it was read **header-only** (column names), no value column inspected. It
is preserved as feed/presentation infrastructure exactly as the R0-era BATS chart-data already in
`../exports/` is, and per the A3 rule above any post-development rows are never value-read.

**Disposition (unchanged from authorization): `SEALED-UNINTERPRETED`.** No performance summary was
inspected, no outcome relationship examined, no PVAE terciles computed, validation and holdout
untouched. Ledger row appended with `SEALED-UNINTERPRETED` notes; **no §9 budget slot is drawn**
(A1.7 — the identity gate is pre-registered as not an unsealing). Draw is recorded by dated note at
first unsealing, which requires separate owner/HELM authorization.

**STOP.** R1 is admissible and sealed. Nothing further proceeds — no development analysis, no
tercile computation, no unsealing — until owner/HELM issues explicit unseal authorization.

**Out-of-packet finding (flagged, not repaired):** the pre-existing committed R0 ledger row is
malformed — it has 26 fields instead of the header's 27 (the `script_file` value is missing, so
every field from `script_sha256` onward is shifted by one on parse). This defect predates this
charge (present at HEAD `f7e45fe`) and is outside the R1 capture packet; it is a frozen committed
record, so it is left untouched here and referred to the owner for a separate dated correction. The
newly appended R1 ledger row is well-formed at 27 fields.
