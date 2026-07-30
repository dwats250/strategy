# Handoff — external advisor briefing

**Prepared 2026-07-29 for use outside the repository.** Self-contained: assumes the reader has
**no file access**. Paste in full.

---

## 0. What you are being asked to do

You are advising on a quantitative trading research project. You are a **steering and reasoning
partner**, not an implementer — you cannot see the repository, run code, or read files, and you
should not write as though you can.

The person you are advising is Dustin, who owns the project and is the sole authorizing
authority. Work is implemented by a coding agent with repo access; your role is to help think
about direction, priorities, statistical soundness, and tradeoffs.

**One thing to understand before advising:** this project is unusually strict about the
difference between *what has been established* and *what is plausible*. That discipline is the
main asset here. Advice that blurs it is worse than no advice. If you are inferring, say so.

---

## 1. The project

**Repository:** `dwats250/strategy` — a quantitative trading research lab. Pine Script
indicators and strategies, pre-registered studies, and the raw exports and analysis behind them.

**A second repository, `dwats250/cuttingboard`**, holds a live trade *decision engine*. It is the
subject of the work but is a **read-only evidence source** from `strategy` — see §2.

**Dustin's three stated goals**, in his priority order:

1. Improve the CuttingBoard engine *(primary)*
2. Test trading strategies
3. Learn robust backtesting methodology

**Current activity:** a three-week TradingView backtesting sprint starting 2026-07-30, revisiting
simple setups that worked for him before — mean reversion, reversals, continuation trades, built
from EMA, RSI, volume, and VWAP anchors.

---

## 2. The governance model — read this before giving any advice

The repo runs on a written set of lab conventions. Several will constrain what advice is usable,
so they are reproduced here in substance.

**Pre-registered manifests, never edited.** A manifest is written and frozen *before* data is
collected. Corrections are dated amendments or new versioned files; prior versions stay as the
audit trail.

**Studies vs audits vs exploratory.** `studies/` follows a fixed skeleton (README, LEDGER.csv,
manifests, scripts, exports, analysis). `audits/` audits another repo's behaviour and has its own
lifecycle. `exploratory/` holds explicitly ungoverned diagnostic work retained for reference.

**The ledger is authoritative.** `LEDGER.csv` is one row per run. When an export, a screenshot,
and the ledger disagree, the ledger wins.

**The holdout rule (§g), which is stricter than standard practice.** A holdout is *forward data
collected under a frozen specification going forward from pre-registration* — never a slice of
history already examined. A held-back historical window inspected once is called a
**"deferred-inspection window"** and explicitly must **not** be called out-of-sample.

*Advisory consequence:* standard walk-forward advice ("hold out the last 20%") conflicts with
this vocabulary. Do not import the term "out of sample" for historical slices. You may recommend
walk-forward *construction* rules; use the project's naming.

**"Unavailable is not the same as passing."** Where a check cannot be reproduced honestly, it is
labelled unavailable and excluded from the arithmetic rather than silently counted as satisfied.

**Cross-repository isolation (§i).** An agent may mutate **only** `dwats250/strategy`.
`dwats250/cuttingboard` is a forbidden mutation target — read only at a pinned commit SHA.
Possessing credentials that could write to it does not authorize doing so.

*Advisory consequence:* you cannot recommend "just change the engine." Any CuttingBoard change
needs its own separate authorization. See §6, decision 1.

---

## 3. Where things stand

**The CuttingBoard engine audit is closed.** A multi-phase audit (EA-0 … EA-8) ran and closed on
2026-07-28. What it established: bounded engine behaviour on reject and halt paths, deterministic
replay (6 of 6 run manifests reproduce byte-for-byte), as-of and look-ahead control machinery
demonstrated to *catch* injected leakage, and contamination control proven by controls that had
to fail.

What it explicitly did **not** establish, stated as plainly in the source: no strategy-quality
claim, no profitability claim, no accepted-trade frequency or quality claim, no real-market
representativeness (all datasets were synthetic), and **no basis for fitting or optimization**.

**EA-9 — empirical evaluation — is BLOCKED, not failed.** The reason is an evidence boundary: no
authorized, provenance-bearing historical OHLCV dataset exists within that audit's scope. Real
market data obviously exists in the world; it was not selected, retrieved, or authorized *there*.

**Four standing limitations carried forward:**

- **L-1** — the accepted path is structurally unobservable under the authorized method. A fixture
  function returns `MANUAL_CHECK` unconditionally, so `outcome = TRADE` cannot occur.
- **L-2** — per-candidate gate vectors are computed in memory then discarded. `gates_passed` /
  `gates_failed` appear in no durable artifact.
- **L-3** — synthetic data validates harness mechanics only, never market behaviour.
- **L-4** — data-provider parity unavailable without a real dataset.

**A prior study closed at no demonstrated edge** (SPY opening-range first-break). Its ledger
carries t-statistics with monthly-block bootstrap CIs — reasonably sophisticated for retail work.

---

## 4. What a repository appraisal established on 2026-07-29

All figures below were verified against source files; a separate read-only verification pass
re-checked fourteen load-bearing claims and confirmed all fourteen.

### 4a. An unpre-registered capture (time-critical)

A real data export exists — 3,620 daily SPY bars, 2012-03-06 to 2026-07-29 — carrying every gate
boolean per bar. But the ledger is empty, the study README says "no run executed," and the run
manifest has ~15 fields still marked "to be filled at capture," including TradingView plan, data
provider, and run date.

Most fields were recovered by counting the file: **2,909 bars evaluated** from 2015-01-01 (711
warm-up), **200 qualified / 297 watchlist / 3,123 rejected**, 226 kill-switch bars, and
confirmation that all seven required macro series resolved on all 3,620 rows.

Four fields remain recoverable only from Dustin's memory or a still-open chart.

### 4b. No performance-statistics layer exists anywhere

The frozen backtest protocol specifies trade count, exposure, win rate, average trade, profit
factor, max drawdown, long/short split. **The word "Sharpe" does not appear in it at all.** Absent
repo-wide: deflated Sharpe, PBO, walk-forward efficiency, multiple-testing-adjusted t, Calmar,
Sortino, Ulcer, rolling Sharpe, implementation shortfall.

### 4c. Trial budgets are enforced qualitatively but not numerically

A campaign manifest already says "exactly three OOS inferential contrasts" and forbids re-runs
with tweaked parameters. But one campaign logged **11 configuration rows over ~1.5 years**, where
the minimum-backtest-length rule (MinBTL, target Sharpe 1.0) supports roughly 5–6 independent
configurations. Nothing was mis-concluded — the study found no edge — but the budget was spent
before the answer arrived. Two of the eleven rows are numerically *identical*, illustrating that
nominal trial count overstates effective trial count.

### 4d. No embargo rule exists

The frozen protocol has out-of-sample beginning the day after in-sample ends — zero gap. With
EMA50/ATR14 on daily bars the leakage window is roughly 50 trading days.

### 4e. Governed process has already leaked once

One work packet was developed entirely outside the governed studies, has no pre-registered
manifest, and carries provenance gaps recorded as "not fixable retroactively." It was retained as
ungoverned lineage. Its disposition record documents a guardrail being crossed. This is the
predicted failure mode of heavy governance, already realized once.

---

## 5. Three new findings — the most consequential part

Produced 2026-07-29 by counting all 3,620 rows of the existing export. Every partition was
consistency-checked (all sum to 3,620).

**Finding 1 — Gate 7 (risk/reward ratio) carries no independent information.**

It partitions *perfectly* on the regime field: 100% of rows in regime 3 fail (1,157 of 1,157),
100% of all other rows pass (2,463 of 2,463). The actual risk/reward value has **zero** influence
— 585 rows with RR strictly *below* the 2.0 threshold passed, and 282 rows strictly *above* it
failed.

The mechanism: candidates are constructed with stop = 1×ATR and target = 2×ATR, so RR ≈ 2.0
always. Regime 3 requires ≥ 3.0; everything else requires ≥ 2.0. So the gate is an alias for
"regime ≠ 3," not a risk/reward test.

**Finding 2 — Gate 5 (stop defined) is a pure tautology.** Passes on 3,620 of 3,620. Zero
failures.

**Finding 3 — Gate 3 (direction) may be misclassified.** Project documentation classifies it as
inert and states "direction alignment is constructed to pass." It fails on **527 of 3,620 rows
(14.6%)**. This is either a genuine falsification of a pre-registered hypothesis or an artifact
of the Pine proxy differing from the engine. It cannot be resolved from the export alone.

**Plus three exact cross-column identities** suggesting further redundancy: one regime value's row
count exactly equals one gate's failure count, in three separate cases.

**The implication that matters.** The engine has 30 gates and 54 configured values, but the
*independent* decision surface looks considerably smaller. Any optimization program that treats
all 54 as tunable will spend statistical trial budget on parameters that cannot change an
outcome. This is why the proposed program leads with a gate marginal-contribution analysis on
data that already exists — before any engine change, any new data, or any authorization.

---

## 6. Open decisions where Dustin's judgment is needed

**Decision 1 — where CuttingBoard changes happen.** Three options were laid out and none chosen:

- *Separate CuttingBoard-rooted authorization per change.* Keeps the isolation rule intact and
  the audit re-runnable by a third party. Slow; this friction is what pushed work outside the
  repo once already.
- *A fork Dustin owns becomes the mutation target*, with `strategy` holding specs and harness.
  Fast iteration, production protected. Costs: fork drift, two sources of truth, merge-back
  becomes its own governance event.
- *Relax the isolation rule*, arguing it existed to protect an audit that has now closed.
  Simplest. But the pinned-SHA discipline is also what makes the audit verifiable by anyone else
  later, and that value did not expire with the program.

**An important subtlety that cuts across all three:** the isolation rule contains *two* separate
locks — a mutation lock, and a "no back-feeding" rule stating that audit results do not authorize
refactoring, parameter changes, or documentation changes in the audited repo. **Relaxing the
first does not relax the second.** Since essentially every proposed engine fix derives from audit
findings, each needs its own authorization regardless of which option is chosen.

**Decision 2 — what "optimizing the engine" means.** Dustin selected "all three, properly
sequenced": observability first, then logic/coherence fixes, then measurement and tuning. The
dependency is strict — you cannot tune what you cannot measure, or measure what you cannot
observe. Currently the engine is at the left edge of that chain.

**Decision 3 — sequencing.** Dustin chose to run the sprint and the planning work in parallel.

---

## 7. Hard constraints on any advice

1. **TradingView Premium expires in a few weeks** (roughly mid-to-late August 2026). Chart-history
   exports are a scarce, non-regenerable resource. Everything splits into *capture-now* (needs
   TradingView) and *compute-later* (everything else). Advice that spends the remaining window on
   building Python tooling is wrong; that tooling can be built after.

2. **No authorized market dataset exists yet.** Any advice requiring empirical evaluation of the
   engine is blocked until data acquisition is separately scoped, with full provenance (provider,
   retrieval, symbol identity, timeframe, timezone, session, bar-timestamp convention, adjustment
   semantics, coverage, checksum — no field blank).

3. **CuttingBoard cannot be modified from this repository.** See §2 and §6.

4. **TradingView structurally cannot compute** deflated Sharpe, PBO, or walk-forward efficiency.
   No Monte Carlo, no bootstrap, no confidence intervals on any reported metric, no portfolio
   backtest, no bid/ask spread. Those must run in Python over exported trade lists.

5. **An unresolved measurement question:** whether TradingView annualizes its Strategy Tester
   Sharpe ratio. Its documented formula uses average monthly return with no √12 term, and no
   documentation states the answer. If it is not annualized, a true annualized Sharpe of 1.0
   displays ≈ 0.29. This is being settled empirically on day one.

---

## 8. Where you can genuinely help

Ordered by likely value:

1. **Pressure-test the gate-redundancy conclusion in §5.** If most of the engine's configured
   surface is inert or collinear, that reframes the entire optimization program. Is the inference
   sound? What would falsify it? What is the right way to measure marginal contribution across
   correlated binary gates?

2. **Think about the trial-budget problem concretely.** A 54-value configured surface generates
   far more than 45 combinations in one afternoon, and MinBTL allows ~45 independent trials on
   five years of data. How should a budget be allocated across a mostly-inert parameter space?
   How should correlated grid points be converted to an effective independent-trial count — the
   literature offers no agreed mechanical procedure.

3. **Sanity-check the sequencing.** Observability → logic → measurement → tuning. Is anything
   mis-ordered? Is anything on the critical path that could be parallelized?

4. **Challenge the simple-strategy premise.** The project leans on Suhonen et al. (2017) — 215
   live bank products, median backtested Sharpe 1.20 → median live 0.31, with the most complex
   strategies degrading by 30+ percentage points more than the simplest. Is this being
   over-applied?

5. **Governance calibration.** The heavy process demonstrably caught real problems *and*
   demonstrably pushed work outside the repo once. The proposed fix is a five-minute
   pre-registration for exploratory work rather than heavier or lighter governance overall. Is
   that the right lever?

---

## 9. Ground rules

- **You cannot see the repository.** If a recommendation depends on a file's contents, say what
  you would need rather than assuming.
- **Distinguish established from inferred**, every time. This project's core discipline is
  refusing to treat unavailable evidence as passing evidence, and advice should hold the same
  line.
- **Do not manufacture numbers.** Every figure in this document was verified against source. If
  you compute something new, show the derivation so it can be checked.
- **Respect the vocabulary.** "Out of sample" has a specific, narrow meaning here; historical
  slices are deferred-inspection windows.
- **Nothing in this document authorizes anything.** It is observational. Recommendations are
  input to Dustin's decisions, not decisions.
