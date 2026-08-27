# VMR — VWAP MEAN REVERSION · family charter / preregistration · v0.1 · 2026-08-27

A **new, independent research family**, opened by owner/HELM charge 2026-08-27 after
the VWAP continuation lane closed at NO EDGE FOUND
(`CONTINUATION_TERMINAL_DISPOSITION_v1.0.md`). VMR is **not** a repair of VDC/FPC: it
is a structurally opposite hypothesis (fade extremes toward VWAP, rather than ride
drift away from it), traced to committed pre-continuation-outcome charter material.
This packet is **DESIGN ONLY** — VMR-0 is **not run** and **no VMR outcome is
inspected.** Frozen on commit; corrections are dated amendments (§b/§c).

## 1. Family definition

**VMR — VWAP Mean Reversion.** Hypothesis class (charter §3, frozen 2026-08-24):
*price displaced from session VWAP reverts toward it.* The conceptual chain
(pre-existing, owner-stated and consistent with the committed record):

> extension / shock → failed acceptance → compression / loss of directional
> control → reversion toward VWAP.

## 2. Provenance (committed, pre-continuation-outcome)

Unlike FPC's H3 (which needed an owner/HELM attestation), VMR's antecedents are
genuinely committed in `STUDY_CHARTER_v0.1.md` (frozen **2026-08-24**, before every
continuation outcome):

- **§3 families table** — "**VMR** — VWAP Mean Reversion — Price displaced from
  session VWAP reverts toward it. **Defined only.**" The family was pre-registered.
- **§5 + §A1.3** — the charter **fixes the excursion measurement primitive**
  (a measurement, not entry logic): `vwap_excursion_atr(t) = (close − session_vwap)
  / ATR14`. VMR-0's extension condition is built directly on this frozen metric.
- **§4 + §A1.2** — the ESTABLISHED / MIXED VWAP-acceptance vocabulary (and the frozen
  4-bar acceptance rule) supply a committed definition of "failed acceptance."

No fabrication is required: the family, the extension metric, and the acceptance
vocabulary all predate the continuation results.

## 3. VMR-0 — primary hypothesis (first configuration)

*When price is extremely extended from session VWAP and shows a reversal (failed
acceptance at the extreme), it reverts toward session VWAP — a mean-reversion entry
taken AGAINST the displacement, targeting VWAP, has positive risk-normalized
expectancy.* Symmetric (long + short). Structurally opposite to continuation (it
fades the extreme; it uses **no** EMA-alignment regime filter).

## 4. VMR-0 mechanics (frozen, smallest falsifiable form)

Retain V0 primitives: SPY, 5m RTH, session VWAP, ATR14 (RMA/Wilder), entry window
09:35–15:25, EOD flatten at 15:50, next-bar-open fills, slippage 1 tick, fixed qty 1,
mintick 0.01. **No EMA9/20 regime filter** (that is continuation's directional gate).

Metric (frozen §5/§A1.3): `E(t) = (close(t) − session_vwap(t)) / ATR14(t)` (signed).

**Three components — exactly one each:**

1. **Extension condition:** `|E(t)| ≥ K`, with **K = 4.0916 ATR** (see §5, distribution-
   derived, frozen before outcomes).
2. **Reversal / failed-acceptance condition:** the extended bar is an **opposing-color
   bar** — extended **below** VWAP (`E ≤ −K`) with a **green** bar (`close > open`), or
   extended **above** (`E ≥ +K`) with a **red** bar (`close < open`).
3. **VWAP-directed objective:** the target is **session VWAP** — exit when a completed
   bar's close has reverted to/through VWAP.

Signal (evaluated fresh each completed bar while **flat** and in the entry window; no
arm-state persistence — the simplest form):

- **LONG** when `E(t) ≤ −K` **and** bar `t` is green → enter LONG at next bar open.
- **SHORT** when `E(t) ≥ +K` **and** bar `t` is red → enter SHORT at next bar open.

Exits (per-bar priority, mirroring V0's structure with the VWAP target in the role of
V0's thesis exit):

1. fill the pending market order at this bar's open (± slippage);
2. resting **ATR stop**, intrabar — `ATR_STOP_MULT = 1.0`, `risk_points = 1×ATR14`
   at the signal bar, placed on the **further-extension** side (LONG stop =
   `entry − 1·ATR`; SHORT stop = `entry + 1·ATR`); V0 stop fill mechanics
   (fills at stop unless gapped through, then at open; slippage 1 tick);
3. at the close: **EOD** flatten if `hm == 1550`; else the **VWAP target** — LONG
   exits when `close ≥ session_vwap` (fill next open − slip), SHORT when
   `close ≤ session_vwap` (fill next open + slip); else, if flat, a new VMR entry.

Direction is set by the **sign of E** (extended up → short; extended down → long) —
the exact opposite of continuation, which trades with the established side.

## 5. The one numeric parameter — K — and its justification

`K = 4.091616` (ATR units). **Derivation (trade-blind, P/L-independent):** the
**90th percentile of `|E|`** over development-window RTH 5m bars (screened corpus,
frozen `CORPUS_MASK_v1.0`), computed by `analysis/vmr_excursion_profile.py`
(evidence `VMR_EXCURSION_PROFILE_2026-08-27.json`). This is a market-data
distribution quantile frozen **before any VMR outcome exists**; it is not tuned on
strategy results.

Sanity check (why a canonical value is rejected): the development `|E|` distribution
is wide (session-anchored VWAP vs small 5m ATR) — median **1.54**, P75 **2.77**,
P90 **4.09**, P95 **4.98** ATR; **39% of bars exceed even 2.0 ATR**. A naive
"2.0 ATR = extended" would fire on 39% of bars — not "extreme." The distribution-
derived P90 selects a genuine tail (~10% of bars). Raw-corpus P90 = **4.068** ATR
(≈ screened) → the threshold is robust to the 9 masked bad-tick bars.

Every other VMR-0 value reuses a frozen definition: ATR length 14 (§8 lineage);
`price_ref = close` (§5 provisional, frozen for this run); `ATR_STOP_MULT = 1.0`
(V0 canonical); red/green bar (frozen); entry window / EOD / slippage / qty / mintick
(V0). **K is the only new parameter, and it is distribution-frozen, not guessed.**

## 6. Ambiguities requiring HELM adjudication

1. **K quantile.** VMR-0 pre-declares **P90** (`K = 4.0916`). P85 = 3.52, P95 = 4.98
   are the neighbouring levers. The quantile is a magnitude choice, **not** outcome-
   tuned; HELM may adopt a different quantile (or a canonical ATR magnitude) **before**
   the first run.
2. **"Failed acceptance" form.** VMR-0 uses a single **reversal candle** as the
   failure condition (smallest). The frozen **§A1.2** acceptance rule (extended above
   VWAP but **not ESTABLISHED LONG** → short) is a more literal "failed acceptance"
   alternative. Adjudicate whether to keep the candle or adopt the §A1.2 form (it adds
   the 4-bar acceptance computation — one more moving part).
3. **VWAP-target execution.** VMR-0 exits on a **bar-close** reversion to VWAP, filled
   next open (matches V0's thesis-exit execution model). An **intrabar touch** of VWAP
   (a limit target) is the alternative; it needs new intrabar-limit machinery. Flag
   if HELM wants intrabar.
4. **No arm-state persistence.** VMR-0 evaluates extension+reversal on a single
   in-window bar (no FPC-style arming). If HELM wants the extended state to *arm* and
   fire on a later reversal bar, that is a distinct (larger) design.

## 7. No additional structure (frozen boundary)

VMR-0 adds none of: RSI, ADX, volume thresholds, EMA50/55 filters, multiple
time-of-day filters, gap filters, news/macro or CuttingBoard context, multiple profit
targets, or trailing stops. Any such element is a **later, separately authorized** VMR
configuration, not part of VMR-0.

## 8. Independent budget (proposed)

VMR is budgeted **independently**; it does **not** inherit the closed VDC/FPC budgets.

- **Proposed VMR interpreted-development budget: ≤ 8 configurations.**
- **VMR-0 is configuration 1** (spent at the first VMR development run).
- **This DESIGN packet spends 0** — no VMR outcome is inspected. VMR-dev **0 / 8**.

## 9. Data & confirmation policy (frozen)

- **Development** may use **2024-09-03 → 2025-12-31** (development, not confirmation).
- **Do not inspect**, for VMR: the consumed VDC validation window (2026-01-06 →
  2026-04-30 — **not** VMR confirmation), the unused historical buffer, the
  late-May..Aug hypothesis-source outcomes, or the frozen-forward holdout.
- **Before any VMR confirmation**, a **genuinely fresh** source/window must be selected
  and frozen later — untouched older historical SPY data acquired only after VMR
  freezes, or future-forward data. **None is fetched or inspected in this packet.**

## Amendments

*(append dated amendments here; never edit the text above in place)*
