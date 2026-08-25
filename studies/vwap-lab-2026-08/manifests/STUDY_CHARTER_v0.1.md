# VWAP STRATEGY LAB — STUDY CHARTER v0.1 (FROZEN) · 2026-08-24

Pre-registered charter for the VWAP Strategy Lab, Aug 24–28 2026 sprint. Frozen per
`docs/conventions.md` §b: this file is never edited in place. Corrections are a dated amendment
appended below, or a new version with the version in the filename.

**This is a scaffold, not a running study.** No source strategy exists yet (see §8). No run has
occurred. No holdout has been accessed. Nothing in this file authorizes a backtest.

---

## 0. Status line

```
VDC_SOURCE_STATUS = SOURCE_REQUIRED
VMR_SOURCE_STATUS = NOT_SPECIFIED (no sprint implementation)
VREV_SOURCE_STATUS = NOT_SPECIFIED (held at 0 tests this sprint)
DAY-1 CONTEXT FREEZE = PENDING (awaiting source ingest)
```

---

## 1. Research charter

The lab studies whether SPY intraday price behavior **relative to session VWAP** carries a
tradable, out-of-sample-durable signal, under a fixed, pre-registered test budget and a frozen
holdout discipline (`docs/conventions.md` §g).

The unit of study is the **VWAP excursion** — signed displacement of price from the session
volume-weighted average price — and the **session VWAP acceptance state** (§4). Families of
hypotheses are enumerated in §3; the concrete trigger/entry/stop/exit logic for the primary
family is **not** determined by this charter and is `SOURCE_REQUIRED` (§8).

The charter fixes: the families under test, the acceptance vocabulary, the excursion metric, the
test budget, the provisional execution context, the two claim boundaries (§6, §7), and the
provenance discipline. It deliberately leaves unfixed everything that depends on the not-yet-
supplied Pine source, and marks each such field UNRESOLVED rather than inventing a value.

---

## 2. What this study is not

- **Not a CuttingBoard artifact.** See the frozen boundary in §6. This study reads no CuttingBoard
  evidence and feeds nothing back into it.
- **Not an options study.** See the claim boundary in §7. It measures SPY underlying price only.
- **Not a source of entry/exit logic.** The primary family's implementation is `SOURCE_REQUIRED`;
  this charter does not, and may not, infer it (§8).
- **Not a performance claim.** No ranked backtest, parameter comparison, or performance
  interpretation is part of this scaffold.

---

## 3. Strategy families under study

Families are **hypothesis classes**, defined by the behavior they target relative to session VWAP.
A family definition here is *not* an implementation. Concrete triggers, entries, stops, and exits
are out of scope for this charter and — for VDC — are `SOURCE_REQUIRED`.

| Family | Name | Hypothesis class | Sprint status |
|---|---|---|---|
| **VDC** | VWAP Drift Continuation | Price that has established directional drift relative to session VWAP continues in that direction. | Primary. Implementation `SOURCE_REQUIRED`. |
| **VMR** | VWAP Mean Reversion | Price displaced from session VWAP reverts toward it. | Defined only. No sprint implementation. |
| **VREV** | VWAP Reversal | Directional reversal at/around session VWAP. | Held at **0 tests** this sprint. |

The VDC family is the mirrored long/short continuation concept in the known lineage (§8); its
long and short sides are conceptually mirrored, but the exact construction is unresolved.

---

## 4. VWAP acceptance vocabulary

Two named session-acceptance states classify how price is behaving relative to session VWAP over
a window. These are the study's shared vocabulary; the **quantitative thresholds that separate
them are UNRESOLVED** and are frozen at source ingest / spec time, not invented here.

- **ESTABLISHED** — price has accepted a definite single side of session VWAP: sustained,
  one-sided acceptance over the measurement window, consistent with a directional (drift/
  continuation) regime.
- **MIXED** — price oscillates across session VWAP within the window without sustained one-sided
  acceptance, consistent with a chop / no-clear-regime state.

UNRESOLVED for ESTABLISHED/MIXED (freeze at spec time): the measurement window length; the price
reference (close vs typical price vs OHLC4); the acceptance band (in ATR or in absolute terms);
the minimum bar count or fraction that qualifies as "sustained"; how a mid-session transition
between states is labeled.

---

## 5. ATR-normalized VWAP excursion — metric definition

The excursion metric **is** fixed by this charter (it is a measurement primitive, not entry
logic):

```
vwap_excursion_atr(t) = ( price_ref(t) - session_vwap(t) ) / atr_len(t)
```

- **Signed.** Positive above VWAP, negative below.
- **session_vwap(t)** — the standard session-anchored VWAP, reset at each RTH session open,
  volume-weighted over the session's bars to `t`.
- **atr_len(t)** — Average True Range; provisional length **ATR(14)**, from the known lineage
  (§8). The exact ATR smoothing (RMA/Wilder vs SMA) is stated at spec time.
- **price_ref(t)** — provisional **bar close**. The exact reference (close vs typical price) is
  confirmed at spec time and, once frozen for a run, recorded in the ledger.

Provisional choices (ATR length, price reference) are marked provisional deliberately; they are
not entry logic and do not depend on the missing source, but they are pinned in the run manifest
before the first run.

---

## 6. Frozen boundary — no CuttingBoard context

**FROZEN.** This study draws **no context, data, threshold, or evidence from `dwats250/cuttingboard`
or any CuttingBoard checkout, remote, ref, or the audited pin.** It is independent VWAP research.
No CuttingBoard artifact informs a definition, parameter, or conclusion here, and no result here
feeds back into CuttingBoard. `docs/conventions.md` §i governs; CuttingBoard remains a read-only,
forbidden-mutation target, and this study does not even read it. Any future need to consult
CuttingBoard would be a separate, explicitly Dustin-authorized charge in a separate session — not
a widening of this one.

---

## 7. Frozen boundary — SPY underlying vs options

**FROZEN.** This study measures **SPY underlying price behavior only** (AMEX:SPY bars). It makes
**no claim** about SPY options — no 0DTE, premium, implied volatility, greeks, assignment, or
options P&L claim is made or implied. Any translation of an underlying signal into an options
position is **out of scope and unsupported by this evidence**. A result here is a statement about
underlying price excursion relative to VWAP, and nothing more.

---

## 8. VDC source status — SOURCE_REQUIRED

**`VDC_SOURCE_STATUS = SOURCE_REQUIRED`.**

### Source gap (accepted as truthful)

There is **no exact current FastAlpha / VWAP Drift v0 Pine source** in `dwats250/strategy` or its
history. The study scaffold proceeds with an explicit `SOURCE_REQUIRED` state.

The entry/exit logic **must not** be reconstructed from any of:

- chat-memory summaries,
- `session_compass_v2.3.pine`,
- older VWAP indicators,
- conceptual descriptions.

Those are **context only, not source authority.**

### Known conceptual lineage (NON-AUTHORITATIVE context)

Recorded only as non-authoritative lineage:

- SPY
- session VWAP
- EMA 9 / EMA 20 baseline family
- ATR(14)
- continuation / drift family
- mirrored long/short concept

### Explicitly insufficient

This lineage is **insufficient to determine**, and this charter does **not** infer:

- the exact trigger,
- the exact entry,
- the exact stop construction,
- the exact exit hierarchy,
- the exact position timing,
- the exact Pine implementation.

These remain **unresolved** until Dustin supplies the actual TradingView Pine source, **or**
explicitly commissions a brand-new VDC-0 specification. Until then, no VDC implementation exists to
test.

---

## 9. Hard test budget (pre-registered)

Interpreted-run budget for the sprint. These are `trials_planned` in the sense of
`docs/conventions.md` §b (amendment 2026-07-30): the count of independent configurations committed
before the first run.

| Class | Family / role | Budget (max interpreted runs) |
|---|---|---|
| Development | VDC | **≤ 18** |
| Development | VMR | **≤ 12** |
| Development | VREV | **0** |
| Validation | (cross-family) | **≤ 6** |
| Holdout | (cross-family) | **≤ 2** |
| **Total interpreted** | | **≤ 38** |

Rules:

- The budget is a **ceiling**, not a target. Fewer is better; unused budget is not a reason to run
  more.
- **`dsr_threshold_implied` is UNRESOLVED** at charter time — it depends on the sample length,
  which is TradingView-context-dependent and not yet known (§10). It is computed and recorded in
  each run manifest before that run, per the §b amendment.
- **Holdout runs (≤ 2)** are governed by `docs/conventions.md` §g: the holdout is frozen forward
  data under a frozen spec, separated from any fitted window by an embargo of at least the longest
  indicator lookback (§g amendment). No holdout access occurs during this scaffold or during
  development.
- VREV stays at 0 this sprint by pre-registration; running it would require a manifest amendment
  stating the reason.

---

## 10. Provisional execution context

Provisional and subject to confirmation at Day-1 context freeze:

| Field | Provisional value |
|---|---|
| Symbol | **SPY** (provisional exchange `AMEX:SPY`) |
| Timeframe | **5-minute** |
| Session | **RTH** (regular trading hours, 09:30–16:00 ET) |
| Candles | standard (provisional) |
| Chart timezone | Exchange / ET (provisional — see §11) |

---

## 11. Unresolved TradingView context fields

To be resolved at Day-1 context freeze; each is a run-manifest field and must not be guessed:

- TradingView account / plan tier and its available chart-history depth.
- Exact data feed / exchange (is `AMEX:SPY` the feed, or another).
- Chart timezone setting (exchange vs local vs UTC).
- Extended-hours toggle state (must be OFF for RTH, to be confirmed and captured).
- Bar-magnifier / bar-replay vs live evaluation.
- Broker emulator settings: commission and slippage assumptions.
- Loaded-bar range actually available at capture (start/end).
- Capture method (List-of-Trades export path; screenshot fingerprint).

---

## 12. Unresolved firewall (holdout) date fields

The "firewall" separates fitted development data from deferred-inspection / holdout data, per §g.
All UNRESOLVED, to be frozen before any run:

- Development window start / end dates.
- Embargo length (≥ longest indicator lookback used; §g amendment) and embargo boundary dates.
- Deferred-inspection window start / end (if any is used — labeled as such, never "out of sample").
- Holdout pre-registration date and the frozen-forward holdout window.

Until these are frozen, no run is a fitted run and no window is a holdout.

---

## 13. Provenance & artifacts (pointers)

- **Run ledger schema** — `../LEDGER.csv` (header) and `../README.md` §"Ledger schema".
- **Per-run pre-registration** — `RUN_MANIFEST_TEMPLATE_v0.1.md` (fill and freeze before capture).
- **TradingView capture requirements** — `../exports/README.md`.
- **Immutable export locations & naming** — `../exports/README.md` (per `docs/conventions.md` §e).
- **Scripts** — `../scripts/README.md` (currently `SOURCE_REQUIRED`; no strategy script present).
- **Analysis reproduction** — `../analysis/README.md` (per `docs/conventions.md` §d).

---

## Amendments

*(append dated amendments here; never edit the text above in place)*

---

### Amendment A1 — 2026-08-25 — PVAE adjudication, acceptance rule, notation correction, sealed-capture ruling

**Authority.** Owner charge of 2026-08-24 (Dustin / HELM), adjudicating the lane-2 PVAE
adversarial review delivered by Fable 5 against the bootstrap pin
`77a9484f652990829ce33339139114b66fc6a452`. Owner disposition: **TEST WITH CORRECTIONS**.
Lane record for this amendment: by explicit owner per-charge authorization, Fable 5 acted as
lane 1 for this charge only; the `docs/conventions.md` §j role-to-model table is unchanged.

Nothing in this amendment changes `VDC_SOURCE_STATUS = SOURCE_REQUIRED`, authorizes a run,
weakens §g, or touches CuttingBoard.

#### A1.1 PVAE — adjudicated hypothesis

PVAE (Persistent VWAP-Aligned Expansion) is adopted as a **stratification hypothesis first**.
Primary question: among trades taken by the exact naked VDC strategy, does persistent
VWAP-aligned EMA expansion identify a subset with better per-trade expectancy?

- TradingView runs change the trade set only when necessary. Questions about dispersion,
  persistence, shock state, EMA-family agreement, and VWAP-state interaction are answered
  offline from an instrumented baseline trade set whenever possible.
- Long and short effects are reported separately; the symmetric PVAE hypothesis requires the
  contrast direction to agree across sides.
- PVAE is not claimed to be novel; it may simply be a trend-quality stratifier. If the exact
  VDC trigger already captures equivalent state and PVAE adds no contrast, that is a valid
  negative result.

#### A1.2 VWAP acceptance rule — frozen (resolves the §4 UNRESOLVED thresholds)

At each signal-evaluation bar close, use the four most recently **completed** bars from the
**current RTH session**, including the just-completed signal bar.

- **ESTABLISHED LONG** — at least 3 of those 4 closes are strictly `>` that bar's session
  VWAP, **and** the most recently completed close is strictly `>` session VWAP.
- **ESTABLISHED SHORT** — mirror, using strictly `<` session VWAP.
- **MIXED** — anything else.

Edge rules, all frozen: `close == VWAP` counts toward neither side; classification is
**unavailable** until four current-session bars have completed; acceptance band = **zero**;
the state is independently recalculated after every completed bar; no ESTABLISHED label is
carried forward merely because the previous bar was ESTABLISHED; completed bars only; no
lookahead. The first eligible classification is defined by **bar sequence**, not by an
assumed timestamp label. Price reference for this rule: bar close.

#### A1.3 Excursion notation correction (§5)

The §5 metric's denominator is the **ATR value**, not the integer lookback length. Corrected
form (intent unchanged; ATR length provisionally 14):

```
vwap_excursion_atr(t) = ( price_ref(t) - session_vwap(t) ) / ATR_value(t)
```

The `atr_len(t)` denominator notation in the frozen §5 text is superseded by this amendment.

#### A1.4 PVAE state variables — frozen definitions

- **Executed state family:** EMA 9 / 20 / 50. Dispersion
  `S_t = abs(EMA9_t - EMA50_t) / ATR14_t`. Ordering is a separate directional gate:
  LONG requires `EMA9 > EMA20 > EMA50`; SHORT requires `EMA9 < EMA20 < EMA50`.
- **Expansion:** `expanding_t = S_t > S_(t-2)`. No ΔS magnitude thresholds this sprint.
- **Persistence:** primary condition is the aligned-expansion state true for **≥ 2
  consecutive completed bars**; the consecutive count is captured as a covariate. Offline
  sensitivity at 1 and 3 is permitted later; no separate TradingView runs for 1 / 2 / 3.
- **Dispersion buckets:** the invented absolute grid (0.10 / 0.20 / 0.30 ATR) is rejected.
  Primary development stratification uses **terciles of `S_t` measured at naked-VDC entry
  observations in the development dataset**. The tercile *rule* is pre-registered before any
  trade outcome is inspected; the numeric boundaries are computed once from the development
  covariate distribution, then frozen, and reused unchanged for historical validation.
  Boundaries are never moved on P/L.
- **Shock (capture / stratify only, never an entry rule or exclusion filter):**
  `ShockRatio_i = TrueRange_i / ATR14_(i-1)` — the denominator uses the **prior** completed
  bar's ATR value so the shock bar does not partially normalize itself away. At a VDC entry,
  `RecentShock = max(ShockRatio)` over the current and previous 3 completed bars.
  `RecentShock >= 2.0` is a descriptive label only, not an optimized threshold.
- **Other families:** no independent TradingView run for 10/22/55. If computationally
  trivial and identity-safe in the future instrumented strategy, `S_10_22_55` and
  `ordered_10_22_55` are permitted as **observational covariates only**, for later offline
  label-agreement / robustness analysis. 12/26/60 is not tested this sprint.

#### A1.5 Cut list — this sprint

Not added, not measured, not tested: VWAP flip count; fast/medium sign-flip count; any
"chop score"; gap metadata (reconstructable later from OHLC, not deadline-bound); EMA
12/26/60; separate fast–medium / medium–slow spread thresholds; RSI; volume filters; ADX;
time-of-day optimization.

#### A1.6 Hypothesis-source labeling and firewall vocabulary

The visual screenshot discovery pool (approximately late May through August 2026)
contributed to hypothesis formation and is labeled **HYPOTHESIS-SOURCE / VISUALLY
INSPECTED**. It cannot serve as independent historical validation of PVAE, and its sessions
are never treated as unseen. Primary development is placed outside the visual source period
whenever available TradingView history permits.

Vocabulary for this study, under existing `docs/conventions.md` §g (which is not weakened):
**DEVELOPMENT** (historical fitted/reused data) · **HYPOTHESIS-SOURCE** (historical data
visually inspected during hypothesis generation) · **EMBARGO** (≥ longest relevant lookback
between fitted and deferred-inspection data) · **VALIDATION / DEFERRED-INSPECTION**
(pre-registered historical data inspected once) · **FROZEN-FORWARD HOLDOUT** (future data
arriving only after specification freeze). No untouched historical block is called a
holdout.

#### A1.7 Sealed-capture budget ruling

Owner ruling for this study: a **pre-registered** TradingView capture that (i) has a frozen
run manifest before capture, (ii) is exported, (iii) is hashed, (iv) is sealed, and (v) is
not examined for research/performance decisions **does not consume an interpreted-run budget
slot (§9) until it is first unsealed/interpreted**. The capture still requires full
provenance under `../exports/README.md`. A sealed capture is recorded at capture time — its
frozen run manifest plus a ledger row whose `notes` field marks it `SEALED-UNINTERPRETED` —
and the §9 budget draw is recorded at first unsealing by a dated note. Prior frozen records
are not retroactively rewritten.

#### A1.8 Planned TradingView run sequence — PLAN ONLY

Blocked until source ingest (`VDC_SOURCE_STATUS = SOURCE_REQUIRED`); nothing here executes:

- **R0** — exact naked VDC development reference.
- **R1** — instrumented VDC development. Instrumentation must not alter strategy behavior.
  Before R1 evidence is admissible, parity against R0 on the common window is established
  mechanically — preferring exact comparison of trade count, side, entry/exit timestamps,
  entry/exit prices, and P/L, allowing only explicitly documented export precision
  differences. If instrumentation changes the trade set: STOP; PVAE is not analyzed.
- **R2** — instrumented historical validation / deferred-inspection capture, **SEALED**.
- **Optional archive** — instrumented VDC over the widest Deep Backtesting range available,
  exported, hash-recorded, SEALED, and marked `ARCHIVE / NON-INFERENTIAL / NOT DEVELOPMENT /
  NOT VALIDATION / NOT HOLDOUT`. Lower priority than R0/R1/R2 source and provenance capture.

Planned instrumented entry stamp: `direction`, `vwap_acceptance_state`, `S_9_20_50`,
`ordered_9_20_50`, `expanding_yes_no`, `aligned_expansion_consecutive_count`,
`recent_shock_ratio`; plus `S_10_22_55` / `ordered_10_22_55` only if trivial and
identity-safe. No filtered PVAE strategy is authorized.

The PVAE offline-analysis pre-registration skeleton is
[`PVAE_ANALYSIS_PREREG_v0.1.md`](PVAE_ANALYSIS_PREREG_v0.1.md).

*(end Amendment A1)*

---

### Amendment A2 — 2026-08-25 — VDC source ingested; parity pending

**Authority.** Owner charge of 2026-08-25 (bounded lane-1 source-ingest and
parity-foundation charge; Fable 5 as lane 1 by the owner's standing in-session per-charge
disposition; §j table unchanged).

The §0/§8 status `VDC_SOURCE_STATUS = SOURCE_REQUIRED` is superseded:

```
VDC_SOURCE_STATUS = INGESTED@scripts/VWAP_Continuation_FastAlpha_v0.pine
                    sha256 c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e
                    / PARITY PENDING
```

- The exact owner-supplied TradingView Pine source (`VWAP Continuation - Fast Alpha v0`,
  Pine v6) is preserved verbatim as an immutable tracked artifact; provenance and full
  mechanical characterization: `../scripts/VWAP_Continuation_FastAlpha_v0_PROVENANCE.md`.
- Parity is tracked in `../PARITY_GATES.md`: DATA/BAR parity **PENDING**; SEMANTIC/FEATURE
  parity **LOCALLY VERIFIED / TV CONFIRMATION PENDING**; EXECUTION parity **PENDING R0**.
- Local data status: SPY corpus **READY** (`../data/CORPUS_SPY_1m_2024-09-01_2026-08-22.md`);
  bar+feature foundation built (`../analysis/parity_foundation.py`, tests passing).
- R0 preparation: `RUN_VDC_SPY_5m_dev_R0_PREP_v0.1.md` (PREP, not frozen, not a run
  authorization). **Development/validation windows remain UNRESOLVED (§12): WINDOW FREEZE
  REQUIRED BEFORE R0.**
- Nothing in this amendment interprets performance, computes expectancy, or touches PVAE
  outcomes; §8's prohibition on reconstruction is now moot for VDC v0 but its lineage
  remains non-authoritative context.

*(end Amendment A2)*
