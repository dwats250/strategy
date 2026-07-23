# PREMIUM CAMPAIGN MANIFEST — v2.2 (FROZEN) · 2026-07-22
v2.2: QQQ effective version is **v1.1.5-rep** (deep-history data-hole
fix — the campaign's first execution-discovered blocker, per the fix-
gets-a-new-version rule). At 2013-12-02 the invariant halt caught a
position crossing the Thanksgiving half-day weekend because the prior
session's closing bar never fired islastbar_regular. v1.1.5 converts
that one condition to counted quarantine: such positions are liquidated
at the session open with exit comment ORPHAN. H2 gains a gate: ORPHAN
and cross-session trades (exit date > entry date) are counted and
EXCLUDED from the H2 slice; expected rare (single digits across full
depth); frequent occurrence = data-quality problem = partial-
replication label. All other invariants remain halts. `immediately` is
permitted only for calendar/session-boundary triggers.
v2.1 supersedes v2 with two pre-result text corrections (H2 entry gate;
restored frozen-environment block) and declares the CODE FREEZE: QQQ
v1.1.4-rep and SPY v0.3.0-tier0 are final for this campaign. Further
script churn is now likelier to introduce drift than improve the
experiment. Known, accepted doc drift in the frozen code: the QQQ
header describes the entry-comment format without the parameter
fingerprint the code actually writes; the code is correct, the comment
is stale, and it stays stale until after the campaign.
**This file is the operating document.** It consolidates the original
manifest plus amendments A1–A8 into one canonical statement; nobody
should apply eight patches mentally while running the campaign.
Provenance: `CAMPAIGN_MANIFEST.md` (original + dated amendments) remains
in the repo untouched. Still pre-result: zero valid deep runs exist.
Filename convention from here on: manifest versions in the filename.

---

## Effective configuration

| Model | Script | Version |
|---|---|---|
| SPY experiment | `spy_orb_tier0_v0_3_0.pine` | **v0.3.0-tier0** |
| QQQ replication | `qqq_orb_replication_v1_1_5.pine` | **v1.1.5-rep** |

QQQ v1.0.0 → v1.1.3: all retired **unrun** (compile blocker; bracket-gap
defect; EOD-seam state bug; margin-trim phantom trades; audit/label
corrections). v1.1.4 changes diagnostics and contamination guards only;
the entry/stop/target/EOD path is v1.1.3's.

**Leverage language (frozen):** Position size is capped using the
first-bar close estimate. Emulator margin enforcement is disabled.
Actual fills may slightly exceed 4×; frequency and magnitude are audited
on-chart and reconstructed offline (leverage = qty × entry ÷ running
equity rebuilt from $25,000 + cumulative net P&L). This is a documented
approximation, not at-fill enforcement.

## Effective run list

| Run | Chart | Script/config | Deep range | Export |
|---|---|---|---|---|
| R1 | SPY 15m, ETH off | v0.3.0 · C0 · Both · TX30 | 2010-01-01 → today (max) | `deep_R1_SPY_C0_TX30.csv` |
| R2 | QQQ 5m, ETH off | v1.1.5 · frozen params (1%/10R/4×) | 2010-01-01 → today (max) | `deep_R2_QQQ_full.csv` |
| R3 | SPY 15m | C0 · Both · TX15 | max | `deep_R3_SPY_C0_TX15.csv` |
| R4 | SPY 15m | C0 · Both · TX60 | max | `deep_R4_SPY_C0_TX60.csv` |

There is **no separate R0** (depth is read from R1/R2's earliest trade)
and **no separate R5 run** (post-paper QQQ is an offline slice of R2).
Tier 3 exploratory if time permits: R6 = SPY C4 TX30 max; R7 = SPY C5
TX30 max; R8 = SPY 5m C0 TX30 max. All Tier 3 output is labelled
exploratory.

## Analysis slices (from the two full-depth exports)

- **H2 slice:** R2 entries 2016-01-01 → 2023-02-17 only.
- **Post-paper slice (was "R5"):** R2 entries 2023-02-18 → today.
- **Pre-2016 R2 entries:** depth diagnostics, exploratory only.
- **OOS slice for H3–H5:** R1/R4/R6 entries before **2025-01-21**
  (dates untouched by the in-sample n=318 analysis).

## Hypotheses (final form)

**H1 (primary).** R1 full-history mean bps. Governing interval: the
**monthly-block bootstrap 95% CI** (20k resamples, seed 7); IID CI
reported, decides nothing. Decision rule: upper bound < +1.0 bps →
event closed permanently. Lower bound > +1.0 bps → surprise branch:
freeze everything, design forward paper test. Between → closed for
options, discretionary for shares. Prediction: |mean| < 2, CI spans 0.

**H2 (replication).** On the H2 slice: strongly positive equity path,
PF > 1.2, ending equity a multiple of start (generous tolerance —
the paper's fills are idealized). **Harness gates first**, all from the
export: (a) NO session contains more than one entry, zero split-size
same-timestamp trades, and every missing session is attributable via
the approximate doji / zero-quantity / data-gap reconciliation; (b) approximate count reconciliation — sessions in
range minus entries = dojis + zero-qty + data gaps (decomposition
spot-checked on chart-loaded window only); (c) long/short near 51/49;
(d) leverage-excess frequency/magnitude and gap-through-stop frequency
reported from the offline reconstruction; (e) first session in range
yields a trade or identifiable skip. Any gate fails → harness audit
before market conclusions.

**H3 (confirmation latency, OOS).** R4 pre-2025 slice: boundary-entry
(final legal bar, 10:30 ET) minus non-boundary mean bps, two-sided
Welch t, α=0.05. In-sample contrast under test: **+5.52 bps** (TX60).
Prediction: fails to replicate. TX30/TX15 boundary contrasts descriptive.

**H4 (short-side deficit, OOS).** R1 pre-2025 slice: short mean vs long
mean, two-sided Welch t. In-sample gap: −3.4 bps. Prediction: shrinks.

**H5 (RVOL dispersion, OOS).** R6's accepted events vs the C0 events
C4 rejected (disjoint, pre-2025). **Primary: sd ratio** (accepted ÷
rejected), bootstrap CI, predicted > 1. Mean lift and MFE/MAE deltas
descriptive. Exactly **three OOS inferential contrasts: H3, H4, H5.**

## Frozen environment (every run, both symbols)

- Standard candles only (scripts also guard this).
- **Extended hours OFF for every run** — binding even beyond bar budget:
  v0.3.0's EMA and RVOL consume whatever bars the chart supplies, so an
  ETH-on run changes C2–C5/R6–R7 calculations, not just history depth.
- Strategy Properties untouched: no commission override, fill-on-bar-
  close OFF, recalc options OFF.
- Symbols recorded exactly: `AMEX:SPY`; QQQ = NASDAQ listing, exact
  tickerid transcribed from the chart legend into the ledger at R2.
- SPY inputs frozen at defaults: OR15 · cutoff 60 · Both · EMA 9/20 ·
  chop 6 · RVOL 20/min10/floor0/hot1.5 · RVOL-history gate ON · scored
  window 2000→2099 (wide open). Only `Time exit` and `Filter cohort`
  vary, exactly as the run list specifies.
- QQQ inputs frozen: 1% / 10R / 4× (fingerprinted in every entry
  comment; any other values in an export disqualify it).
- Fill-bar-target classification: the on-chart proximity counter can
  miss a favorable gap through the target; the exported **exit comment
  (TGT/STP/EOD) is the authoritative classifier** offline.

## Not licensed
No new cohorts/filters/horizons/symbols mid-campaign; no re-runs with
tweaked parameters after seeing results; anomalies get exactly the
tests above; new patterns go to the open-items ledger for a future
pre-registration.

## Refund decision (Tue Jul 28 calendar reminder)
Keep Premium only if H1's surprise branch triggers or a standing Deep
Backtesting need emerges. Null = refund by Jul 29. Exports are
permanent either way.
