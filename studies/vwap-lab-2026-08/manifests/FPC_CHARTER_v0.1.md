# FPC — FIRST PULLBACK CONTINUATION · family charter / preregistration · v0.1 · 2026-08-26

A **new, independent research family**, opened by owner/HELM charge 2026-08-26 after
the VDC terminal disposition (`VDC_TERMINAL_DISPOSITION_v1.0.md`). FPC is **not** a
repair of failed VDC: its entry idea (a single, orderly *first pullback* after a
freshly established directional alignment) traces to pre-existing hypothesis work
that predates the VDC validation result (see Provenance). Frozen on commit;
corrections are dated amendments (§b/§c). This charter authorizes **no** outcome
inspection — the first FPC development run is a separate, later packet.

## 1. Family definition

**FPC — First Pullback Continuation.** Hypothesis class: *after price freshly
establishes a one-sided directional alignment relative to session VWAP, the FIRST
orderly opposing-color pullback continues the move; subsequent same-regime pullbacks
carry less edge.* This is a distinct hypothesis class from VDC (VWAP Drift
Continuation), which enters on **every** opposing-color bar while aligned. FPC keeps
VDC's regime definition but restricts entry to one pullback per fresh regime.

## 2. Provenance (traceability) — with an honest evidentiary note

FPC's antecedents in the **committed** study record, all frozen **before** the VDC
validation result (`STUDY_CHARTER_v0.1.md`, committed 2026-08-24; validation
committed 2026-08-26 at `d8a20dd`):

- **Charter §4 — VWAP acceptance vocabulary.** ESTABLISHED = "price has accepted a
  definite single side of session VWAP: sustained, one-sided acceptance … consistent
  with a directional (drift/continuation) regime." FPC operationalizes a *fresh*
  ESTABLISHED alignment as the setup for a first pullback.
- **Charter §3 — families are hypothesis classes.** The charter explicitly frames a
  multi-family research program (VDC primary; VMR, VREV defined) — room for a
  continuation-entry hypothesis distinct from VDC was pre-registered, not invented to
  rescue VDC.
- **Charter §A1.6 — visual hypothesis-source pool** (late-May..Aug 2026), labeled
  HYPOTHESIS-SOURCE / VISUALLY INSPECTED and firewalled: the visual-discovery work
  that generated pullback-shaped hypotheses predates and is walled off from all VDC
  interpretation.

**Evidentiary flag for HELM (do not gloss).** A search of the committed study records
(manifests, docs, scripts, plans, git history) finds the **antecedent concepts**
above but **no verbatim "first orderly pullback / H3" pre-registered line-item.** The
"H3 / deferred visual hypothesis" the charge cites appears to live in owner/HELM
visual work not committed as a study artifact. This charter therefore traces FPC to
the genuine committed antecedents (§3/§4/§A1.6) and records the missing verbatim H3
record as an **open provenance item for HELM adjudication** — it is neither
fabricated here nor treated as if committed. FPC's independence from the VDC failure
rests on those dated antecedents, not on a verbatim H3 citation.

## 3. FPC-0 — primary hypothesis (first configuration)

*A continuation entry restricted to the FIRST opposing-color pullback after a FRESH
directional VWAP/EMA regime begins has better expectancy than naked VDC's repeated
opposing-candle entry rule.*

FPC-0 is **symmetric** (long + short). It does **not** inherit the failed VDC
long-only hypothesis.

## 4. FPC-0 mechanics (frozen)

Retain V0 exactly — SPY, 5m RTH, session VWAP, EMA9, EMA20, ATR14,
`ATR_STOP_MULT=1.0`, the 09:35–15:25 entry window, next-bar-open execution, the VWAP
thesis-failure exit, the EOD flatten, fixed qty, costs, and every broker-emulator
assumption. **Only the entry-signal rule changes.**

Regime (identical to V0):

- **bullish** = `close > sessionVWAP AND ema9 > ema20`; **bearish** mirrored.
- **fresh bullish** at bar *t* = `bullish_t AND NOT bullish_{t-1}`; fresh bearish
  mirrored.

Long FPC signal:

1. On a **fresh bullish** regime, **arm** one long opportunity. Do **not** enter on
   the fresh-regime bar itself.
2. While that bullish regime stays **continuously true**, the **FIRST** subsequent
   **red** bar (`close < open`) that is **inside the entry window** and taken **while
   flat** is the only permitted long entry.
3. After that entry, **disarm** — no second long entry during the same continuous
   bullish regime.
4. If the bullish regime becomes false before an entry, **disarm**. A later
   false→true transition creates a **new** opportunity (re-arm).

Short is the **exact mirror** (fresh bearish regime, first subsequent green bar).

Implementation: `fastalpha_engine.simulate(..., signal_mode="fpc")` (engine sha
`26e1fb07641b35deb8461cf7d3af45d25eefcf45462e66448a4c390cba5f5b0e`). The arm-state is
execution-dependent ("while flat"), so it lives in the engine, not the flat-agnostic
feature seam; it reads only precomputed parity_foundation fields
(`bullish_state`, `bearish_state`, `red_bar`, `green_bar`, `in_entry_window`) and
re-implements no indicator. Deterministic tests: `analysis/test_fpc_signals.py`
(8 cases — fresh-regime arming, arming-bar exclusion, first-red-only, one-entry-per-
regime with a VDC(2)-vs-FPC(1) contrast, out-of-window suppression, disarm/re-arm,
short mirror, determinism).

## 5. Semantic ambiguities requiring HELM adjudication

1. **"first red bar … while flat" when NOT flat (rare corner).** The only way a fresh
   bullish regime's first in-window red bar occurs while the strategy is *not* flat is
   a cross-regime open position (a prior-regime trade still open because the regime
   turned false via an EMA cross while price stayed on the same VWAP side, so no
   thesis exit, then turned fresh-true again). FPC-0 as implemented (interpretation
   **(a)**) keeps the opportunity **armed** and takes the first *later* red-in-window
   bar that is flat (disarm only on an actual entry or on regime-false). The
   alternative **(b)** would expire the opportunity on the first in-window red bar
   regardless of flat. (a) reads "while flat" as part of the signal; (b) reads it as
   the ordinary flat gate. **Adopted: (a).** Flagged because it is a genuine choice,
   though it affects only this rare corner.
2. **Verbatim H3 provenance** (see §2): the committed record lacks a verbatim "first
   orderly pullback / H3" hypothesis. Adjudicate whether the §3/§4/§A1.6 antecedents
   suffice as FPC's pre-VDC-failure provenance, or whether HELM will supply/commit the
   original H3 articulation.

Resolved readings (no adjudication needed): a red bar **outside** the entry window
does not fire and does not consume the opportunity (the first red-**in-window** bar
fires); doji bars (`close == open`) are neither red nor green and neither trigger nor
disarm.

## 6. No additional structure (frozen boundary)

FPC-0 adds none of: EMA50/55; PVAE acceptance definitions; expansion/persistence
thresholds; ShockRatio filters; volume filters; RSI; ADX; gap conditions;
time-of-day optimization; ATR-regime filters; new stops or targets. Any such element
is a **later, separately authorized** FPC configuration, not part of FPC-0.

## 7. Independent budget (proposed)

FPC is budgeted **independently**; it does **not** inherit VDC's 18-slot ceiling.

- **Proposed FPC interpreted-development budget: ≤ 12 configurations.**
- **FPC-0 is configuration 1** (to be spent at the first FPC development run).
- **This PREP packet spends 0 FPC configurations** — no FPC outcome is interpreted.

Running FPC-dev interpreted: **0 / 12.**

## 8. Data & confirmation policy (frozen)

- **Development** may use **2024-09-03 → 2025-12-31** (freely reusable historical
  development data). This is development, **not** independent confirmation.
- **Do not inspect**, for FPC: the prior VDC validation window (2026-01-06 →
  2026-04-30, **consumed** — it may **not** become FPC validation), the unused
  historical buffer, the late-May..Aug hypothesis-source outcomes, or the
  frozen-forward holdout.
- **Before any future FPC confirmation**, choose and **freeze a genuinely fresh
  source/window** first: (A) older untouched historical SPY data acquired only after
  the FPC hypothesis is frozen, or (B) future-forward data arriving after FPC freezes.
- **No confirmation data is fetched or inspected in this packet**, and none may be
  inspected for FPC until such a fresh window is separately frozen.

## Amendments

### Amendment 1 — 2026-08-27 — owner/HELM provenance attestation (H3 first-pullback)

The §2 evidentiary flag is resolved by an owner/HELM attestation, recorded here
verbatim as the missing provenance link (no historical git citation is invented):

> During the pre-validation visual hypothesis work, before the VDC validation
> outcome was known, the working hypothesis set explicitly included: *"first orderly
> pullback after established alignment may be better entry geometry"*, and the later
> working disposition: *"H3 first-pullback = DEFER."* This existed in the HELM/chat
> research record but was not committed verbatim to the Strategy repository.

Standing of this record: the committed repository antecedents remain **§3** (multi-
family framework), **§4** (ESTABLISHED alignment vocabulary), and **§A1.6** (visual
hypothesis-source pool), all frozen 2026-08-24 — before the VDC validation
(`d8a20dd`, 2026-08-26). This attestation supplies the specific "first-pullback / H3
= DEFER" articulation that lived in the HELM/chat record but was not committed as a
repo artifact. FPC's provenance is therefore: committed antecedents (§3/§4/§A1.6) +
this dated owner/HELM attestation. It is **not** framed as a repair of failed VDC —
the hypothesis and its DEFER disposition predate the validation outcome.
