# CuttingBoard engine — optimization program (draft)

**Status:** `DRAFT — OBSERVATIONAL. AUTHORIZES NOTHING. NOT A CHARGE.`

Created 2026-07-29 UTC. Companion to `gap-register-2026-07-29.md`.

This document proposes a shape for work. It creates no charge, no scope, and no permission, and
it does not authorize any CuttingBoard mutation. Per `EA-AUDIT-CLOSEOUT.md` §5, empirical
evaluation and any fitting or optimization each require their own explicit Dustin authorization,
and per §i no CuttingBoard write is authorized from this repository at all.

---

## 0. The one thing to internalize first

**The dependency chain is strict, and it runs backwards from where the instinct points.**

```
   observability  ──▶  measurement  ──▶  tuning
   (what happened)     (was it good)     (make it better)
```

You cannot tune what you cannot measure. You cannot measure what you cannot observe. Right now
the engine is at the left edge: per-candidate gate vectors are computed and discarded (G-10), the
accepted path cannot be reached at all under the authorized method (G-11), and no authorized real
dataset exists (G-12).

Adding deflated Sharpe and PBO to a system in that state would be roofing a house with no walls.
Every one of the eight framework gates needs an accepted-population return series as input, and
there is currently no way to produce one.

**The corollary is the useful part:** the highest-value work available today needs no
CuttingBoard change, no new data, and no authorization — because it is analysis of an export that
already exists. That is §A0.

---

## A. Phase A — Observability

*No market data required. No fitting. This is the phase that unblocks everything else.*

### A0 · Gate marginal-contribution analysis — **available today, blocks nothing, blocked by nothing**

`studies/cuttingboard-asis-proxy/exports/CBASIS_…_048f5c66.csv` already carries every gate boolean
across 3,620 bars. Before touching the engine, answer from that file:

- Which gates ever change an outcome, and which are deterministic restatements of an upstream
  field? Three exact identities already point at redundancy (G-16), and two gates are already
  settled: Gate 7 is a perfect alias for `regime_code != 3` (G-13), Gate 5 never fails (G-14).
- What is the marginal rejection power of each gate, holding the others fixed?
- What does the rejection cascade look like — the first-rejection distribution is already
  extremely concentrated (2,500 of 3,620 on a single code).
- Which gates are pairwise redundant, and what is the rank of the decision surface?

**Why this comes first.** The engine has 30 gates and 54 configured values. If a large fraction
are inert or collinear, the *real* tunable surface is a handful of parameters, and both the trial
budget (G-03) and the optimization plan look completely different. Doing this after the tuning
plan is written means writing the wrong tuning plan.

**Cost:** hours. **Prerequisite:** G-01 closed first, so the analysis runs against a run with a
complete record rather than compounding an unpre-registered capture.

### A1 · Durable per-candidate gate vector — *closes G-10 / L-2*

The single highest-value engine change. `QualificationResult.gates_passed` / `.gates_failed`
exist in memory and reach no artifact. Persist them per candidate, per bar.

**A working specification already exists in this repository.** The Pine proxy's 35-column export
schema — `g1_regime` … `g10_extension`, `soft_fail_count`, `first_rejection`, `qualified`,
`watchlist`, `rejected` — *is* the target schema. It was built to answer exactly the question
L-2 says the engine cannot answer. Port it as JSONL rather than designing a new one.

### A2 · Structured reason-code enum — *closes G-17 / EA-6-004*

Reason codes are prose with interpolated numerals, so cross-run grouping requires string parsing.
**The enum already exists**: `engine/EA-4-GATE-INVENTORY.csv` has all 30 gates with stable IDs.
It lives in the audit rather than in the engine. Moving it is mechanical.

### A3 · Ordered decision / override event stream — *closes G-18 / EA-6-002*
### A4 · Persist stale and excluded evidence — *closes G-19 / EA-6-003*
### A5 · Distinguish evaluated candidates from emitted opportunities — *EA-6-005*

Denominator integrity. Without it no selectivity or coverage measure has a defensible
denominator, and a HALT currently preserves zero opportunities.

### A6 · Accepted-path observability — *closes G-11 / L-1* · **needs separate authorization**

Closeout §5 condition 3 requires this to be separately authorized, and only if an analysis
actually needs accepted-path metrics. Every framework gate does. Sequence it last in Phase A
because it is the one item with an authorization gate in front of it.

### A7 · The single change with the widest blast radius — a `--dry-run --trace` mode

If only one thing gets built: a mode that runs the engine over historical bars, emits the full
decision trace, and forms **no order intent whatsoever**. It subsumes A1–A5 in practice, it is
inherently safe (nothing can reach a broker), and it converts the engine from a live-only system
into something testable. `engine/trace/SCHEMA_v1.md` already defines the trace format.

---

## B. Phase B — Logic and coherence

*No market data required. Independent of Phase A; can run in parallel.*

Every item is an existing audit finding, carried at its recorded classification. **None was
upgraded, and none is a demonstrated wrong pass/fail decision** — `EA-5-ELIGIBILITY.csv`
classifies all 30 gates as 6 ELIGIBLE / 24 CONDITIONAL / **0 EXCLUDED-DEFECTIVE**.

| # | Item | Source | Note |
|---|---|---|---|
| B1 | HALT reported as `status=FAIL` + exit 1, indistinguishable from an unhandled-exception HALT, while the contract reports `STAY_FLAT` | EA5-001 | **Do this one first.** Cheap, and until it is fixed no automated harness can distinguish "correctly refused to trade" from "crashed" — which makes every downstream test ambiguous |
| B2 | Three terminal-HALT thresholds outside `config.py` | EA5-003 | Explicitly a *fitting-readiness* gap: you cannot sweep what you cannot enumerate. Blocks Phase C |
| B3 | Gates 1–2 duplicated | EA5-005 | UNKNOWN consequence |
| B4 | Kill switch evaluated twice | EA5-009 | UNKNOWN consequence |
| B5 | CONTINUATION omits the ATR stop floor DIRECT enforces | EA5-010 | Documented, reasoned asymmetry; path comparability open |
| B6 | Documented "Polygon fallback" absent from pinned source | EA5-004 | Coherence — doc or code is wrong |
| B7 | Gate redundancy — Gate 7 inert, Gate 5 tautological, Gate 3 misclassified | G-13/14/15 | **New.** Resolve G-15 by reading the proxy's direction logic against the pinned source |
| B8 | Gate 9 (EARNINGS) is `None` → fail-open, always | Q-09 | See below |

**On B8, a cross-application of your own rule.** `conventions.md` §h says "unavailable is not the
same as passing" — where a check cannot be reproduced honestly it is labelled unavailable and
excluded from the arithmetic, because silently treating an unreproducible check as satisfied
manufactures a result the evidence does not support. Gate 9 does precisely what that rule
forbids: earnings data is absent, so the gate fails open and counts as a pass. The proxy already
handles this correctly (`NOT REPRESENTABLE`, excluded from the soft count). The engine does not.
That asymmetry is worth naming.

---

## C. The CuttingBoard boundary — tradeoffs, no recommendation taken

You asked for the options laid out. Here they are with consequences. **Nothing is selected.**

### The constraint that survives all three options

§i has two separate locks, and they are often conflated:

1. **The mutation lock** — no agent may write to CuttingBoard from this repo.
2. **The no-back-feeding lock** — audit results "do not authorize refactoring, issue creation,
   parameter changes, documentation changes, or any other back-feed into CuttingBoard."

**Relaxing the first does not relax the second.** Every finding in Phase B came out of the audit,
so acting on any of them needs its own commission regardless of which option below is chosen.
This is the single most important thing to understand before picking.

### Option 1 — Separate CuttingBoard-rooted charge per change

| | |
|---|---|
| **For** | §i intact. The boundary demonstrably caught real problems. Audit evidence stays clean and the pin stays meaningful, so the EA record remains re-runnable by a third party. |
| **Against** | Session-switching overhead per change. Slow iteration. This is precisely the friction that pushed the v0.5 work outside the repo (G-06) and cost that packet its evidence value. |
| **Fits when** | Changes are few, large, and consequential. |

### Option 2 — Fork you own becomes the mutation target

| | |
|---|---|
| **For** | Somewhere to actually build. `strategy/` holds the spec and the harness; the fork holds the work. The audit line keeps its pin untouched, so EA evidence is unaffected. Fast iteration without touching production. |
| **Against** | Fork drift and two sources of truth. "Which is real CuttingBoard?" becomes a live question. Merge-back is itself a governance event needing its own rule. |
| **Fits when** | You expect a lot of experimental change and want production protected. |

### Option 3 — Relax §i now the audit is closed

| | |
|---|---|
| **For** | Simplest. §i was written to protect an active audit; that audit closed at EA-8. |
| **Against** | §i is also what makes the audit *re-runnable* — the pinned-SHA discipline protects any future independent review, and that value did not expire with the program. "Capability is not authorization" is a good principle independent of any audit. And the no-back-feeding lock is untouched, so this buys less than it appears to. |
| **Fits when** | You are confident no third party will ever need to re-verify the EA record. |

### A hybrid worth considering

Option 2 for the development loop, Option 1 retained for anything touching the audited pin, and
an explicit rule that any change *derived from audit evidence* needs its own commission
regardless of where it lands. This keeps iteration fast, keeps the EA record verifiable, and
makes the back-feeding lock explicit rather than implicit.

**The decision is yours and should be written into `conventions.md` §i as a dated amendment
rather than settled in chat** — which is exactly the failure mode retrospective item #2 names.

---

## D. Phase C — Measurement and tuning

*Gated on Phase A, on authorized data, and on separate authorization. Not startable now.*

| # | Item | Gated on |
|---|---|---|
| C1 | Authorized, provenance-bearing historical OHLCV | Closeout §5 condition 1 — every field in `DATA_PROVENANCE_CONTRACT.md`, none blank |
| C2 | EA-8 look-ahead suite passing on that dataset, including its negative control | Condition 2 |
| C3 | Metrics layer — the eight framework gates | A1, A6, C1 |
| C4 | Trial-budgeted parameter work | Condition 4, plus A0's answer on the real tunable surface |

**On C4, the thing that will bite.** The trial budget is not a formality. At target SR 1.0, MinBTL
allows ~45 independent configurations on 5 years of data and ~7 on 2 years. A 54-value configured
surface generates far more than 45 combinations from a single afternoon of sweeping. The budget
must be committed *before* the first sweep — it is the only one of the eight gates that cannot be
reconstructed afterward, which is exactly why it belongs in a pre-registered manifest (G-03).

A0 is what makes this tractable: if most of the 54 values turn out to be inert or collinear, the
independent-trial count is far lower than the nominal combination count, and the budget becomes
affordable. Doing A0 first is the difference between a feasible tuning program and one that is
statistically dead before it starts.

---

## E. Ideas for the CuttingBoard repo

Offered as observations. **None is authorized, and none is a bug report.**

1. **The Pine proxy is a finished specification for the trace writer the engine lacks.** Its
   35-column schema answers exactly the question L-2 says cannot be answered. Do not design a new
   one — port it.
2. **The reason-code enum already exists** as `EA-4-GATE-INVENTORY.csv`, 30 gates with stable
   IDs. It is in the wrong repository, that is all.
3. **Measure gate redundancy before optimizing anything.** Gate 7 is an alias for
   `regime_code != 3` across all 3,620 rows; Gate 5 never fails; three further exact
   count-identities suggest more of the same. Optimization effort aimed at inert gates is wasted
   effort that also spends trial budget.
4. **Consolidate the config surface.** Three thresholds outside `config.py` (EA5-003) make the
   tunable surface unenumerable, which blocks any principled sweep.
5. **Fix the HALT/FAIL collision early.** It is small, and until it is fixed every automated test
   is ambiguous about whether a refusal was correct behaviour or a crash.
6. **Make fail-open gates explicit rather than silent** — Gate 9 today, and any future gate whose
   data source is absent. Your own §h already says how.
7. **Build `--dry-run --trace`.** One change, and the engine becomes testable without ever
   forming order intent.

**A closing caution.** Items 1–7 are all *observability and coherence*. None of them makes the
engine trade better, and that is deliberate: nothing in the EA-1 … EA-8 record supports any
strategy-quality, profitability, or accepted-trade claim, and no basis for fitting or
optimization was established. The honest sequence is to make the engine measurable, measure it,
and only then decide whether it is worth improving — and be genuinely willing to find that it is
not.
