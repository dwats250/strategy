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

*(none yet — append dated amendments here; never edit the text above in place)*
