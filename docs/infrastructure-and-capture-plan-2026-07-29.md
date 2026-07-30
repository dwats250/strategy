# Infrastructure and capture plan — 2026-07-29

**Status:** `DRAFT — OBSERVATIONAL. AUTHORIZES NOTHING.`

Created 2026-07-29 UTC. Companion to `gap-register-2026-07-29.md` and
`engine-program-draft-2026-07-29.md`.

Addresses the four stated pain points: no local run/test loop, no real market data, governance
overhead per change, and TradingView as the only execution venue — under the binding constraint
that **TradingView backtesting is available for a few more weeks only**.

---

## 1. The organizing principle: capture-now vs compute-later

Everything in this program is one of two kinds:

| | Needs TradingView | Can be done any time |
|---|---|---|
| **What it is** | Producing CSV exports from chart history | Every analysis, harness, spec, and governance change |
| **Scarce?** | **Yes — weeks** | No |
| **If you get it wrong** | The data is gone and cannot be regenerated | Redo it whenever |

**The CSV export is the interface between the two halves.** Once a CSV exists, TradingView can
lapse without blocking anything downstream — `BACKTEST_PROTOCOL.md` already anticipated this
("Export the trade list to CSV and compute DSR, PBO, and WFE yourself. That export is the natural
interface").

So the priority for the remaining Premium window is not "run the best experiments." It is
**maximize the set of exports you will later wish you had.** An export you did not take is
unrecoverable; an analysis you did not run is a Tuesday.

**Concrete implication:** do not spend Premium weeks building the Python harness. Build it after.
Spend Premium weeks capturing.

---

## 2. Capture list — before Premium lapses

Ordered by irreversibility, not by interest.

### Tier 0 — today

- [ ] **Close G-01.** Record `tv_plan`, data provider from the chart legend, `run_date`, and any
      non-default chart setting for the existing `CBASIS_…_048f5c66.csv` capture. Four fields.
      Everything else in that manifest is now recoverable by arithmetic (gap register, G-01).
- [ ] **Settle the TradingView Sharpe question** (G-09). One long smooth backtest, export monthly
      equity, compute annualized Sharpe by hand, compare to TV's figure and to yours ÷ 3.46.
      Ten minutes. Record it once in run metadata, not per run. Every Sharpe logged for the rest
      of the sprint depends on the answer.

### Tier 1 — deep history that only Premium can reach

- [ ] Deep Backtesting exports for every strategy family you intend to evaluate later. Bar limits
      are the binding constraint on sample adequacy, not your patience.
- [ ] **Work at 15m and 1h.** Premium gives ~3 years at 15m and ~11 at 1h. At 1m it gives 51 days
      and at 5m ~256. Against MinTRL at 80% power — 6.2 years to detect a true SR of 1.0 —
      **51 days of 1-minute data cannot establish anything at all.** This is a Gate 2 constraint,
      not a preference.
- [ ] Correlated-basket captures for anything promising: SPY/QQQ/IWM/DIA or ES/NQ/RTY. A real
      edge degrades gracefully across these; vanishing means it was fit to one symbol's noise.
      These cost minutes now and are impossible later.

### Tier 2 — the sprint itself

- [ ] Per-run trade-list CSVs, exported the day they are generated. The chart's first bar drifts
      forward over time and exchanges revise bars after the fact, so a re-run next month is a
      different experiment. Define every window by absolute timestamps in code.

### Two silent hazards to guard on every single run

- **Order-count trimming.** Pine v6 no longer errors past the 9,000-order cap — it silently trims
  the oldest orders. The report looks complete while early history has been deleted. Check
  `strategy.closedtrades.first_index` every run.
- **Properties override code.** Properties-tab settings override the `strategy()` declaration and
  persist across code edits. **This lesson is already encoded in your own repo** —
  `CAMPAIGN_MANIFEST_v2.4.md` frozen-environment block: *"Strategy Properties untouched: no
  commission override, fill-on-bar-close OFF, recalc options OFF."* Copy that line verbatim into
  whatever the sprint pre-registers.

---

## 3. Pain point: TradingView is the only execution venue

**Gates 3, 4, and 5 structurally cannot run inside TradingView.** No Monte Carlo, no bootstrap,
no confidence intervals on any reported metric, no portfolio backtest, no bid/ask spread — limit
orders get zero slippage and fill on touch, which for passive-side mean reversion is the largest
unmodeled cost in the whole exercise.

So a Python harness is required regardless of how the sprint goes. It needs **no** TradingView
access to build, which is why it belongs after the capture window, not during it.

### Proposed harness shape

```
harness/
  ingest/      # TradingView trade-list CSV -> normalized trade/return series
  metrics/     # the Part-1 gate computations
  gates/       # accept/reject against thresholds, given N and T
  report/      # one row per run, appendable to LEDGER.csv
```

**Metrics worth having, in build order:**

1. `deflated_sharpe` (Gate 3) — needs the trial count N, which is why G-03 comes first
2. `pbo_cscv` (Gate 4) — S=16 splits, C(16,8) = 12,870 combinations. The cleanest single
   diagnostic available: it needs neither an estimate of N nor a distributional model, because it
   measures your selection process directly. Existing implementations: Python `pypbo`, R `pbo`
3. `walk_forward_efficiency` (Gate 5) — plus Pardo's hard assertion, worth encoding as an
   automatic failure: **no single trade, winning run, or period may exceed 50% of total net
   profit**
4. `rolling_sharpe`, `ulcer_index`, `implementation_shortfall` — the three most valuable and
   least commonly implemented metrics. A level Sharpe hides regime dependence; Ulcer captures
   drawdown depth *and* duration; implementation shortfall is the only honest measure of whether
   your cost assumptions were right

**Conventions to adopt** (from `pwb-toolbox`, which got these right): `periods_per_year = 252`,
`max_drawdown` as a `(depth, duration)` tuple, `calmar = CAGR / |max_dd|`, signals computed on the
prior bar as a deliberate look-ahead guard.

**Convention to explicitly reject:** `risk_free_rate = 0.0`. Make it a required argument with no
default (G-08). This is the flaw that inflates paperswithbacktest's entire published library.

---

## 4. Pain point: no local run/test loop

The engine cannot currently be run and inspected without the full audit containment apparatus —
which is correct for an audit and wrong for iteration.

**The unlock is `--dry-run --trace`** (engine program §A7): run over historical bars, emit the
full decision trace, form no order intent. Inherently safe, so it needs far lighter ceremony than
a live-capable run. `engine/trace/SCHEMA_v1.md` already defines the trace format.

**Note the asymmetry worth exploiting:** the Pine proxy already gives you a working, inspectable
gate-level loop today — 3,620 bars with every gate boolean, no engine execution required. For
gate-structure questions (which gates matter, what is redundant, what the cascade looks like),
the proxy is sufficient and available now. Reserve the engine loop for questions the proxy
genuinely cannot answer — chain validation, the five-step decision chain, the accepted path.

---

## 5. Pain point: governance overhead per change

This is what pushed the v0.5 work outside the repo (G-06), and it is the largest risk to the next
three weeks.

**The fix is not more governance and not less — it is a cheap tier that is still pre-registered.**

The repository currently has three tiers: `studies/` (full §a skeleton), `audits/` (§h
lifecycle), `exploratory/` (ungoverned, retained for reference). The gap is between the second and
third: there is nothing between "full pre-registered campaign manifest" and "no manifest at all."

### Proposed: a one-page exploratory pre-registration

Everything in it is knowable before the run and takes about five minutes:

```markdown
# PROBE <id> — <one line>
Date: <UTC>            Status: EXPLORATORY — NO EDGE CLAIM
Symbol / timeframe / session / window (absolute timestamps):
Script + SHA-256:
trials_planned (N):                    <-- the number, committed now
dsr_threshold_implied:                 <-- observed SR needed at this N and T
Question:
Stop condition:
Properties: untouched — no commission override, fill-on-bar-close OFF, recalc OFF
```

Two fields carry nearly all the value. `trials_planned` is the only one of the eight framework
gates that **cannot be reconstructed afterward** — the manifest is the only place it can live.
`dsr_threshold_implied` turns it into a number you have to beat, computed before you know whether
you beat it.

This converts an uncitable packet into a weak but citable one. It does not make exploratory work
into a study, and it should not try to.

**It should exist before 2026-07-30**, or the sprint reproduces the v0.5 pattern at higher volume.

---

## 6. Pain point: no real market data

The blocker that stopped EA-9, and the one item here with a hard authorization gate in front of
it. `DATA_PROVENANCE_CONTRACT.md` is `DRAFT / EXPLORATORY — FROZEN IMPLEMENTATION NOT AUTHORIZED`
and "selects no provider, authorizes no download, and specifies no acquisition code."

Worth being precise about what the closeout actually says, because it is easy to misread: **this
is a statement about authorization and provenance within that audit, not about the world.** Real
market data plainly exists. It was not selected, not retrieved, and not authorized *there*.
Acquiring it is a normal task; it simply needs its own scope, and it cannot be back-doored
through the closed audit.

**Sequence:** fill `DATA_PROVENANCE_CONTRACT.md` (provider, retrieval method, symbol identity,
timeframe, timezone, session, bar-timestamp convention, adjustment semantics, coverage, checksum
— no field blank) → acquire → run the EA-8 look-ahead suite on it **including its negative
control** → only then is any empirical claim available.

**The convention fields are not bureaucracy.** EA-8 §4.4 records that an off-by-one bar
convention is indistinguishable from look-ahead, and the suite cannot detect it. That is the
specific reason the contract demands them.

---

## 7. Suggested shape of the next three weeks

Running the sprint and the planning work in parallel, per your call.

| Week | TradingView (scarce) | Everything else (not scarce) |
|---|---|---|
| **Now** | Close G-01's four fields · settle the Sharpe question | Probe template exists before first run |
| **1** | Sprint runs at 15m/1h · export every run same-day | A0 gate-contribution analysis on the existing proxy export |
| **2** | Correlated-basket and regime-split captures | Harness: ingest + `deflated_sharpe` + `pbo_cscv` |
| **3** | Deep-history captures for anything surviving | `conventions.md` amendments: embargo (G-04), trial budget (G-03), §i decision (G-23) |
| **After** | *(Premium may lapse)* | WFE, engine Phase A/B, everything remaining |

**The test of whether this worked** is not how many strategies survive the sprint. It is whether,
on the day Premium lapses, every analysis you want to run is still runnable. If yes, the capture
list was right. If you find yourself needing one more export, it was not.

---

## 8. What is deliberately not proposed

No new directory conventions beyond the probe template. No process layers. No CuttingBoard
changes. No priority ordering beyond dependency and irreversibility.

Adding any of this to the standing rules is a separate, explicit change to `conventions.md` —
same closing rule as `retrospective-ea-audit-2026-07-28.md`.
