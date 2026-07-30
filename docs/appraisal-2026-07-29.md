# Appraisal — `dwats250/strategy`

**Date:** 2026-07-29 · **Basis:** files read in session, listed in §7
**Status:** `OBSERVATIONAL. AUTHORIZES NOTHING.` Creates no charge, no scope, no permission.

Companion documents: `gap-register-2026-07-29.md`, `engine-program-draft-2026-07-29.md`,
`infrastructure-and-capture-plan-2026-07-29.md`.

---

## 0. The prior handoff's premise was stale

A blocked cloud session (2026-07-30 note) framed four questions on the assumption that the
CuttingBoard engine audit was live and that the repo's governance was untested against real work.
Neither holds.

The EA program **closed at EA-8 on 2026-07-28**. EA-9 is BLOCKED/UNEXECUTED — not failed —
because no authorized, provenance-bearing historical OHLCV dataset exists inside the audit's
boundary (`EA-AUDIT-CLOSEOUT.md` §2). The TV-0→TV-4 Pine line closed earlier: TV-1's commission
withdrawn, TV-1R/TV-2/TV-3/TV-4 never commissioned.

The questions still have answers, but three of four land differently than framed, one is
inverted, and there is a live seam that matters more than any of them.

---

## 1. Urgent and time-sensitive — an unpre-registered capture

`studies/cuttingboard-asis-proxy/exports/CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv`
exists. It is a real capture: **exactly 3,620 daily bars**, first bar 2012-03-06, **last bar
2026-07-29 — today** — with the full per-bar gate column set (`g1_regime` … `g10_extension`,
`soft_fail_count`, `first_rejection`, `qualified`, `watchlist`, `rejected`).

That the last bar is today's is why this section is first. The capture happened within hours.

| Record | Says |
|---|---|
| `LEDGER.csv` | header only — no rows |
| `README.md` | `PACKAGE COMPLETE — NO RUN EXECUTED`; "`exports/`, `analysis/` — Empty pending the first run" |
| `manifests/RUN_SPY_1D_2015-01-01.md` | `run_date`, `data_provider`, `tv_account`, `tv_plan`, non-default chart settings, all seven macro-series flags, export `sha256`, and **every** result-summary field still read `TO BE FILLED AT CAPTURE` / `PENDING CAPTURE` |

Per §f the ledger is authoritative, and it records no run. This is the exact failure the
manifest's own warning box cites — UV02's friction scenario is permanently `UNRECOVERABLE`
because Properties were never captured before export, and "the cost was not the missing field —
it was that the field could not be recovered later at any price."

**Recovered from the export itself** (arithmetic on an existing file; see the gap register
Appendix A for method and consistency checks):

| Manifest field | Value |
|---|---|
| Bars evaluated (from 2015-01-01) | **2,909** (warm-up 711; total 3,620) |
| Qualified / Watchlist / Rejected | **200 / 297 / 3,123** |
| Kill-switch bars | **226** |
| First-rejection distribution | 0 → 200 · 1 → 226 · 2 → 2,500 · 5 → 165 · 7 → 373 · 10 → 156 |
| Macro series resolved | all seven — `votes_cast` = 8 on **all 3,620 rows without exception** |

**Still decaying, recoverable only from Dustin or a live chart:** `tv_plan`, the data provider in
the chart legend, `run_date`, whether any chart setting was non-default.

**Suggested action, which is Dustin's to authorize:** record those four now. The clean form is a
dated capture record beside the manifest, not an edit to it — the manifest says
`NEVER EDITED AFTER CAPTURE`, and §b makes a correction an amendment or a new version. No field
was filled by this session.

Minor note: the filename encodes `20150101` while the file begins 2012-03-06. Consistent with the
manifest's warm-up instruction, so defensible — but it is the same filename/content divergence
class as Amendment 2 in the candidate-fidelity disposition, and deserves one sentence.

---

## 2. Q1 — Gap analysis: the question contains a category error

The prior note asked what the CuttingBoard engine computes versus Part 1 of the evaluation
framework. The intersection is empty **by construction**, and that is not a gap.

The engine is a live trade *qualification* engine: 30 gates, an 8-vote regime model, a structure
classifier, deterministic 1-ATR/2-ATR geometry. It computes **no performance statistic at all**.
Part 1's eight gates evaluate whether a strategy's track record means anything. The engine emits
candidates; it never scores itself.

**The real comparison surface** is `spec/BACKTEST_PROTOCOL.md`, whose "Required exports" section
is where performance metrics were actually specified:

| Part 1 needs | In the protocol? |
|---|---|
| Trade count, exposure, win rate, average trade, profit factor, max drawdown, long/short split | **Present** |
| Results by regime / structure, incremental variant deltas | **Present** — richer than the framework asks |
| Sharpe, in any form | **Absent** — the word does not appear in the file |
| Deflated Sharpe / PBO / WFE | Absent |
| Multiple-testing t-stat | Absent here; **present** in `studies/spy-orb-first-break/LEDGER.csv` as `t_stat` with monthly-block bootstrap CI, 20k resamples, seed 7 |
| Calmar, Sortino, Ulcer, rolling Sharpe, implementation shortfall | Absent |

Two caveats: `BACKTEST_PROTOCOL.md` is `FROZEN FOR TV-1` and its line is closed, so amending it
is not the move — a new spec would be. And the ORB `t_stat` is unadjusted for multiplicity.

**The zero-risk-free-rate flaw does not currently apply**, because nothing computes a Sharpe. It
goes live the instant anything does.

**The binding constraint is not missing statistics.** It is L-2 (per-candidate gate vectors
computed then discarded) and L-1 (accepted path structurally unobservable). Without an observable
accepted path and authorized data, no accepted-population metric is computable — which blocks all
eight gates upstream of any statistics work.

**One cheap asymmetry worth noting:** the proxy export has `first_rejection` and per-gate
booleans — exactly the substrate L-2 says CuttingBoard lacks. The proxy already solves in Pine
what the engine does not persist in Python.

---

## 3. Q2 — Trial budget in the manifest: yes, and it half-exists

`CAMPAIGN_MANIFEST_v2.4.md` already contains, pre-registered and frozen:

> Exactly **three OOS inferential contrasts: H3, H4, H5.**

> **Not licensed:** no new cohorts/filters/horizons/symbols mid-campaign; no re-runs with tweaked
> parameters after seeing results.

That is Gate 1 in prose — committed before results, unfalsifiable afterward, enforced by the
freeze. The apparatus is right. **What is missing is the number and its consequence.**

From `LEDGER.csv`: the shallow ORB campaign logged **11 configuration rows** over ~1.5 years.
MinBTL at target SR 1.0 gives ≈ 1.4 yr for N=5 and 1.9 yr for N=7 — so ~1.5 years supports 5–6
independent configurations. Eleven was over budget. The study closed at no-edge so nothing was
mis-concluded, but the budget was spent before the answer arrived.

An instance of the framework's "N must be *independent* trials" caveat sits in the same file: rows
C0 and C1 are **numerically identical on every field** (n=318, mean −1.203 bps, sd 25.66,
t = −0.84). Nominal N overcounts effective N.

The deep runs are comfortable: 2010–2026 (16 years), 3,300 trades. At N=10 the DSR-0.95 bar is
`(1.57 + 1.645)/√16 ≈ 0.80` annualized Sharpe.

**Recommendation:** add `trials_planned` and `dsr_threshold_implied` to the run-manifest template
and `LEDGER.csv`. Both computable before any data exists. Highest leverage per unit effort found.

---

## 4. Q3 — Holdout: the repo is *stricter* than the framework

This inverts the prior note's hypothesis, which anticipated a loose definition.

`conventions.md` §g:

> Slicing history after the fact to manufacture an "out of sample" test does not produce a real
> holdout.

> A historical window held back and inspected only once … is still not a §g holdout. Call it a
> deferred-inspection window and state what it can support. **Do not call it out of sample.**

Consequences:

1. **Gate 5's entire walk-forward apparatus is historical slicing.** Under §g it yields
   deferred-inspection windows, never holdouts. Not a defect in either document — §g asks "what
   can this evidence support?", Gate 5 asks "is this parameter set stable across regimes?" Both
   are worth having; they must not share a word.
2. **The frozen TV-0 windows do not meet the framework's construction rules.** IS
   2016-01-01→2021-12-31 (6 yr), OOS 2022-01-01→2026-07-24 (~4.6 yr) — a ratio of ~**1.3:1**
   against 4:1–6:1, as a single split rather than 20–40 windows. (Frozen, line closed; an
   observation, not a defect to fix.)
3. **No embargo rule exists anywhere in the repo.** OOS begins the day after IS ends — zero gap.
   The word "embargo" does not appear. With EMA50/ATR14 on daily bars the leakage window is ~50
   trading days. **This is the one real additive gap here, and it is small.**

Credit where due: the ORB campaign's OOS slice ("entries before 2025-01-21, dates untouched by
the in-sample n=318 analysis") is a correctly constructed deferred-inspection window, and is
nowhere called a §g holdout.

**Reconciliation:** adopt the framework's ratios and embargo as *construction rules*; keep §g's
naming. Importing the vocabulary along with the arithmetic would quietly undo the strongest rule
in the conventions.

---

## 5. Q4 — Three goals: hypothesis confirmed, and it already happened

The conventions do have a lighter path — §h separates audits from studies, and `README.md`
documents `exploratory/` for "ungoverned diagnostic work retained for reference."

**But the tier did not prevent the migration; it absorbed it afterward, at cost.**
`exploratory/cuttingboard-candidate-fidelity-v0_5/README.md` states the v0 → v0.5 line was
"developed **outside** the repository's governed studies," carries no pre-registered manifest and
no study-grade provenance, and its evidence boundary is reduced to "these files existed, in this
form, with these hashes, at the stated capture dates." Its provenance gaps — no chart screenshot,
no TradingView session/provider record — are "recorded, not fixable retroactively." The packet's
disposition amendment (2026-07-30) records an execution deviation where a Downloads-deletion
guardrail was treated as blanket approval. No bytes were lost — proven by hash, not asserted —
but the guardrail was crossed.

So the hypothesis is not speculative. It describes something that already occurred and cost a
real packet its evidence value. The appraisal should not say "already handled."

**The fix is not more governance.** Making the exploratory tier heavier pushes the next packet
further out. The fix is making the *cheap* path pre-registered: a one-page manifest with N,
window, symbol, script hash, and an explicit "exploratory — no edge claim" label costs five
minutes and converts an uncitable packet into a weak but citable one. The difference between
`exploratory/` as a catch-basin and as a real tier is whether anything is written down *before*
the run.

This is also the largest governance risk to the next three weeks.

---

## 6. The sprint, briefly

- **The simple-strategy instinct is right.** Suhonen et al. (2017), 215 live bank products: median
  backtested Sharpe 1.20 → median live 0.31, and the most complex strategies degraded by 30+
  percentage points more than the simplest.
- **Day one:** settle whether TradingView annualizes its Strategy Tester Sharpe. If it does not,
  a true annualized Sharpe of 1.0 displays ≈ 0.29. Ten minutes; record once.
- **Timeframe is a Gate 2 question, not a preference.** Premium gives 51 days at 1m and ~256 at
  5m. Against MinTRL at 80% power (6.2 years to detect SR 1.0) neither establishes anything.
  Work at 15m and 1h (~3 and ~11 years).
- **Two silent hazards:** Pine v6 silently trims orders past the 9,000 cap (check
  `strategy.closedtrades.first_index`); Properties override `strategy()` and persist across edits.
- **That second lesson is already encoded** — `CAMPAIGN_MANIFEST_v2.4.md`: "Strategy Properties
  untouched: no commission override, fill-on-bar-close OFF, recalc options OFF." Inherit verbatim.

---

## 7. What was read, and what was not

**Read:** `CLAUDE.md`; `README.md`; `docs/conventions.md`;
`docs/retrospective-ea-audit-2026-07-28.md`; `audits/…/EA-AUDIT-CLOSEOUT.md`;
`audits/…/spec/GATE_TRANSLATION_MATRIX.md`; `audits/…/spec/BACKTEST_PROTOCOL.md`;
`studies/spy-orb-first-break/manifests/CAMPAIGN_MANIFEST_v2.4.md`;
`studies/spy-orb-first-break/LEDGER.csv`; `studies/cuttingboard-asis-proxy/README.md`,
`LEDGER.csv`, `manifests/RUN_MANIFEST_TEMPLATE_v0.1.md`, `manifests/RUN_SPY_1D_2015-01-01.md`,
and its export; `exploratory/cuttingboard-candidate-fidelity-v0_5/README.md` and
`handoff/ARTIFACT_DISPOSITION_AMENDMENT_2026-07-30.md`; plus the uploaded
`baseline-evaluation-parameters.md`.

**Not read**, therefore not characterised: `plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md` in full (status
taken from `README.md` and the closeout); EA-5/EA-6 findings files in full (taken from the
closeout's summary tables); the engine `LEDGER.csv`; `RULE_MAPPING_v0.1.md`; any `.pine` source;
`AGENTS.md`.

**Not done:** nothing was written to, moved within, or deleted from any governed directory during
the appraisal. No manifest field was filled. No frozen record was touched. CuttingBoard was not
read, not fetched, and not contacted — every statement about the engine is sourced from
`strategy`'s own audit artifacts, not from the audited source.

**Claim discipline:** §1–§5 rest on files read and quote them where wording matters. Arithmetic in
§3 is recomputed from source formulas, not transcribed. The engine characterisation in §2 is
second-hand by necessity — from the audit's own records, the only reading of CuttingBoard the
boundary permits.

**Verification pass.** Fourteen load-bearing claims were re-checked against source files by a
separate read-only pass: the empty ledger, the unfilled manifest fields, the export's row count
and date range, `votes_cast` universality, the 11-shallow/15-total ledger counts, the C0/C1
identity, and every direct quotation. All fourteen confirmed. Two were *strengthened* and
corrected upward: the export is exactly 3,620 rows ending 2026-07-29, and `votes_cast` = 8 holds
on all rows rather than a sample. C0/C1 are identical across every numeric field, not only the
four cited.

---

## 8. If you want one thing

§1. The rest is analysis and keeps. The capture-time fields on that export decay.
