# Portfolio strategy collaboration — 2026

**Owner:** Dustin Watson · **Collaborators:** Claude and ChatGPT · **Opened:** 2026-10-01 · **Status:** operating (Round 13). History of Rounds 1–13: `ROUNDS.md`.

**What this is.** A living market-research and decision system. It exists to help Dustin continuously:
- understand the present market state and the mechanisms that connect its parts;
- separate facts from interpretation;
- generate and test hypotheses;
- find promising businesses, assets, instruments and setups;
- keep a useful watch universe;
- preserve knowledge between sessions;
- improve decision quality;
- discover whether repeatable edges exist;
- allocate capital only when evidence and opportunity justify it.

A trading journal, a macro newsletter, a screener, a portfolio tracker, an archive and an earnings experiment are all *components* of it, not what it is.

**Who decides.** Investment decisions are Dustin's.

**Boundaries.** This is not a study or an audit under `docs/conventions.md`, and it authorizes nothing in CuttingBoard or any other repository.

**To start a market day,** open `WATCHLIST.md` §1.

---

## Operating constraints

> **"The core architecture may stabilize. The learning process never freezes."** — owner decision, Round 13

- **No learning freeze.** Daily work, research, new hypotheses, new candidates and new instruments continue whenever they are justified. "No repeatable edge has been demonstrated yet" is true; it is not a reason to reduce inquiry. *(Round 12's build freeze was withdrawn; see `ROUNDS.md` Round 13.)*
- **Architecture discipline.** Seven files are enough. A new durable file needs a demonstrated information-management problem that the existing files cannot absorb cleanly. If one is ever needed: state the gap, say why no existing file can hold it, and keep its scope narrow. Small omissions are fixed in place.
- **No yes-men.** Disagree with Dustin, ChatGPT, earlier Claude rounds and existing positions when the evidence warrants it. Never disagree for show.
  - Dustin liking a name is not evidence.
  - A favourite that does not qualify is left out.
  - A failed thesis of our own is invalidated.
- **Intuition is a valid starting point.** It must eventually show its work: INTUITION → OBSERVABLE QUESTION → EVIDENCE → HYPOTHESIS → PREDICTION → REALITY (intake: `RESEARCH_MAP.md`).
- **Independent discovery.** Candidates may disappear when the evidence stops supporting them. They come back only with new evidence, never because they were mentioned before.
- **Capital stewardship.** The C$5,000 is a realism anchor and the approximate current deployment budget, not the limit of the opportunity set. See `PROPOSAL.md` §8.
- **Corrections are valuable.** Correct the error, preserve provenance, check whether any frozen result was affected, and extract the reusable lesson. Never hide a correction. Frozen records are never rewritten.
- **Build only what current use demands.** No ontologies, knowledge graphs, scoring systems, automated narratives, piles of derived indicators, giant watch universes, or architecture for hypothetical futures. Fix a gap that repeats; record a one-off and move on.

## Evidence maturity — two different things

**1. Process learning: demonstrated, from real failures and corrections in this collaboration.**

| Lesson | The incident that showed it |
|---|---|
| Separating state from story improves analysis | Round 11's measurements overturned five claims in Round 10's agreed narrative |
| Explicit labels expose hidden assumptions | The review caught a model-estimated 55/45 split and an inferred oil → Fed link that had been stated as fact |
| Adversarial review catches errors | Round 11 review: XLU/VNQ misused as evidence, mixed time windows. Round 12 review: contradictions admitted without prior expectations |
| Frozen records prevent hindsight editing | The ACN level was kept as frozen; annotations were used instead of edits; the timestamp errors were corrected by dated note |
| Current and historical documents belong apart | *Reasoned rather than shown by a failure* (Round 12). Included because it is plausible, not because it is demonstrated |

**Caveat.** These lessons show that the process catches errors in our own records. They do not yet show better decisions or returns.

**2. Market-edge evidence: immature.** We do not yet know whether earnings continuation, leader pullbacks, duration turns, post-shock reversals, or any tactical rule has positive expectancy.

| Item | Count at Round 13 (2026-10-01) |
|---|---|
| Frozen setups written · triggered · completed and graded | 10 · 0 · 0 |
| Expired without trigger | 1 (PT-001 ACN; shadow open to Dec 11) |
| Cohort events completed through D+20 | 0 of 10 (first: UNH, Oct 13) |
| Post-earnings thesis reviews | 0 (first: TSM, Oct 15) |
| Thesis-state changes on evidence after the register opened | 0 |
| Predictions resolved (P1–P10) · contradictions resolved | 0 · 0 (10 OPEN: 5 contradictions, 5 research notes) |
| Real-money decisions informed by the system (recorded) | 0 |
| Decisions taken outside a written rule | Not yet tracked; needs Dustin's report |

Update this table at each weekly review.

## Operating cadence

**Daily — nearly every market day.** Purpose: identify what changed, decide whether it matters, and decide whether anything deserves attention or capital.

**Automation.** The daily cycle runs unattended as the scheduled task **"Strategy · daily market state"**, every weekday at 13:20 Pacific, starting 2026-10-02.
- It skips full-market U.S. holidays and adds the weekly review on Fridays.
- It cannot redesign the system, create files, or deploy capital. Instead it flags `STRUCTURAL GAP — REVIEW REQUIRED` or `CAPITAL DECISION REQUIRED` for an interactive session.
- Interactive sessions can write a state too; whichever runs later builds on the earlier one.

| Step | What to do |
|---|---|
| 1. Observe | Update only the measurements that matter (WATCHLIST §2). Don't collect data because it is available |
| 2. Detect change | Ask what changed *materially* since the previous state, not what happened in every market |
| 3. Interpret | Does each change confirm the model, contradict it, weaken it, need an alternative, or stay ambiguous? Label interpretation as interpretation |
| 4. Cross-market check | Ask what other markets should be doing if the explanation is right. Disagreement across markets is evidence |
| 5. Opportunity scan | Does anything change a setup, a business thesis, a regime watch, a candidate or a capital decision? Never manufacture a trade; **NO ACTION** is valid |
| 6. Preserve | Write the DAILY STATE (WATCHLIST §1). Touch other files only if something meaningful changed |

**Weekly — at the end of each trading week.** A deeper review, not a redesign. Ask:
- What changed this week?
- Which hypotheses strengthened or weakened, and which contradictions remain open?
- Which setups went stale, and which candidates earned promotion or should be archived?
- Which gauges added nothing?
- Did a repeated one-off reveal a structural gap?
- Did the system make or prevent a meaningful decision?
- What relationship did we discover that we do not understand?

**Weekly outputs:**
- a short **"Weekly review — week ending <date>"** entry in `ROUNDS.md`;
- the evidence-maturity table updated;
- stale material moved out of current pages and recorded in that entry: archived roster items, resolved contradictions, superseded thesis history, finished research items.

Small refactors are allowed. Large changes need a demonstrated recurring problem.

**Event-driven.** Earnings reviews, CPI, FOMC, auction and refunding checks against the predictions, and cohort records are done on the day (WATCHLIST §6).

**Rounds (ChatGPT ↔ Claude).** A round is held when there is new evidence, a real disagreement, or a recurring structural gap. A round must do at least one of:
- find a materially new opportunity;
- resolve or sharpen a disagreement;
- reveal a methodological problem;
- convert an observation into a repeatable strategy;
- materially change a long-horizon thesis;
- produce evidence about an existing family.

**When the architecture may freeze.** Not on a calendar date. Freeze the schema harder once all of these hold:
- several weekly cycles have passed;
- real events have flowed through the system;
- one-off omissions have stopped recurring;
- the file boundaries keep working;
- new insights change content rather than structure.

Research never freezes.

## Working loop

Each question runs on its own clock — minutes, days, weeks, months or years.

```
REALITY
   ↓
OBSERVATION ............... Market Brief (read-only) · live data · Dustin · Claude · ChatGPT
   ↓
CURRENT STATE ............. WATCHLIST §1 (daily state) · §2 gauges
   ↓
MODEL / ALTERNATIVES ...... MARKET_MODEL §1–§6, §8
   ↓
CONTRADICTIONS & TESTS .... MARKET_MODEL §7–§8 (contradictions, predictions P/W)
   ↓
OPPORTUNITY? ── NO ──► keep watching (WATCHLIST §2–§5) · open research (RESEARCH_MAP)
   │ YES
   ↓
THESIS → SETUP → VEHICLE → INVALIDATION ... RESEARCH_MAP / WATCHLIST §3 · PAPER_TRADES · PROPOSAL rules
   ↓
PAPER / MICRO-LIVE → OUTCOME ............... PAPER_TRADES
   ↓
LEARNING ................. ROUNDS · RESEARCH_MAP (findings, pillar candidates) ──► back to MODEL
```

New ideas are classified on intake — OBSERVATION · RESEARCH LEAD · HYPOTHESIS · WATCH · SETUP · INVESTMENT THESIS · SPECULATION — and each class has a home (`RESEARCH_MAP.md`, Intake). Exploration can be messy at first; the discipline comes afterward.

## Files

| File | Answers | Holds | How material leaves it |
|---|---|---|---|
| `README.md` | How does this work, and how mature is the evidence? | Purpose, constraints, evidence maturity, cadence, loop, file map, memory boundary, evidence rules, frozen owner brief | The brief is frozen (amend only by dated note) |
| `WATCHLIST.md` | What matters right now? | Daily state, gauges, businesses, setups, candidates, dated decisions and events, roster rules | Latest two daily states only (older in git). Stale items leave at the weekly review and are recorded in `ROUNDS.md` |
| `MARKET_MODEL.md` | What do we think is happening, why, and what would prove us wrong? | Hypotheses and states, mechanisms, causality and evidence classes, contradictions, competing explanations, predictions and falsification conditions | Current only. Resolved contradictions and superseded state history move to `ROUNDS.md` at the weekly review |
| `RESEARCH_MAP.md` | What deserves deeper investigation? | Intake, programs, long-horizon theses, methodology findings, the cohort, the research queue, pillar candidates, gap map | Items that produce understanding, a setup, background knowledge or abandonment leave with a one-line note in `ROUNDS.md` |
| `PAPER_TRADES.md` | How do setups and rules perform when written before outcomes? | Frozen setups, triggers, expiries, shadows, thesis/timing/vehicle grades, family results | Never rewritten; changes only by dated annotation |
| `PROPOSAL.md` | What rules govern capital? | The sleeve, gates, speculation lane, capital reallocation, stewardship, deployment classes, exposure-map schema | Replaced in place; material changes logged in `ROUNDS.md` |
| `ROUNDS.md` | How did the system evolve? | Rounds, weekly reviews, corrections, decisions, rejected approaches, handoffs, archived material | Append-only |

**Memory boundary.**

> **Memory helps the AIs resume work; Markdown proves what the work currently says.**

- **These Markdown files are the source of truth** and win any conflict.
- **Work memory** holds only resume pointers: where the next session begins, the latest commit, open questions and scheduled items. It never holds values, states, rules or roster contents.
- **The claude.ai project copies** are read-only mirrors, each stamped with its commit.
- **Timestamps come from the clock:** the git commit time is authoritative.

## Standing assumptions (Round 1; challenge in any round)

- Figures in **CAD** unless marked US$. USD/CAD 1.4244 (Oct 1, 2026).
- Accounts (Round 6): TFSA, margin account and LIRA are all available; account choice is an execution note made at the trigger and never limits what the lab studies.
- Options toolkit: long calls and long puts only (no spreads, no written options). Paper research has no premium cap; live premium at risk ≤ C$100 (C$150 A+, earned by a family) — see `PAPER_TRADES.md` §2.
- The $5,000 is incremental, experimental capital — not the whole retirement portfolio.
- **Instrument universe (Round 13):** common equities and ETFs, including Treasury, credit, commodity and inverse ETFs; long calls and puts; cash equivalents; and other liquid instruments Dustin's accounts permit. An instrument may be a gauge, a vehicle, both, or neither. Affordability affects deployment, never whether an instrument is worth understanding.

## Evidence rules

- Live sources for live claims; an observation date beside every changing value.
- **Label claims (pillar P1, Round 12):**
  - **OBSERVED** — a printed price or official number;
  - **DERIVED** — arithmetic on observed values;
  - **MODEL ESTIMATE** — output of a model with assumptions;
  - **INTERPRETATION** — an explanation or causal claim;
  - **PREDICTION** — a dated claim about the future;
  - **UNMEASURED** — the evidence is missing.
- A proxy never inherits the certainty of a measurement.
- Relationships carry a causality label in addition (`MARKET_MODEL.md`).
- State the bridge from interpretation to any action.
- *Round 1–11 wording: OBSERVED / INTERPRETATION / ACTION.*
- Historical analogues inform; they do not prove.
- No single-cause political explanations; model the variables (fiscal impulse, monetary policy, supply, energy, credit, productivity, capex, market pricing).
- **"Consistent with" is not a test.** A test needs an alternative that predicts something different (methodology finding 10).

---

## Owner brief (frozen, verbatim, 2026-10-01)

Claude Handoff — Personal Investment Strategy Collaboration

Date: 2026-10-01
Owner: Dustin Watson
Collaborators: Claude and ChatGPT
Status: New exploratory experiment
Capital budget: $5,000 of incremental capital
Planning horizon: approximately 25 years, to age 65

Purpose

Create a small, durable research experiment in the market journal/strategy repository in which Claude and ChatGPT collaboratively develop an actionable personal investment framework for Dustin.

This is not intended to become another large trading system or governance project. Keep it lean. The goal is to use the two systems' different reasoning, research tools, market context, and accumulated context about Dustin's investing process to produce something that can actually guide capital allocation.

The experiment should distinguish clearly between:

1. long-horizon holdings;
2. tactical swing positions;
3. short-duration downside or hedge trades;
4. liquidity / dry powder;
5. regime-dependent opportunities that should remain inactive until their conditions appear.

The final output should answer a practical question:

If Dustin gave the two systems $5,000 of incremental capital today, how should that capital be deployed, staged, or intentionally left undeployed, and what rules should govern it afterward?

Owner brief

Dustin has approximately 25 years until age 65 and is comfortable with an aggressive portfolio.

He does not want “aggressive” to mean indiscriminate risk. The portfolio should have a durable component containing assets or businesses the collaborators believe can survive severe downturns and compound over long periods.

Alongside that core, Dustin wants the ability to take shorter-term positions when genuine trends or momentum are developing. Swing positions may last days, weeks, or months depending on the thesis.

Very short-term downside trades are also permitted, especially in markets already being followed closely — for example gold, equity indices, rates, oil, or major macro themes — but these are tactical trades rather than permanent portfolio allocations.

Every tactical trade must be developed before capital is committed. At minimum it needs:

- thesis;
- entry/confirmation condition;
- position size;
- expected holding period;
- invalidation;
- protective exit mechanics;
- maximum acceptable loss;
- conditions for taking profit or scaling out.

Options and other convex instruments are permitted where appropriate, but a position must have mechanical risk containment. Do not allow an option to drift from a defined tactical loss into a 60–100% loss merely because the thesis might eventually recover.

Paper trading should not be used casually. It is appropriate when an A-quality opportunity exists and the genuine decision is whether to deploy real capital or test the trade without capital.

Do not anchor on Dustin's suggestions

The following are hypotheses and areas of interest, not instructions to own them:

- energy may have attractive characteristics in the current regime;
- BE may have been a stronger expression of an energy/power thesis than TE;
- precious metals may deserve a modest allocation;
- gold, rates, oil and the major indices are already familiar markets;
- long-duration Treasury instruments such as TLT may eventually become attractive;
- high-rate, inflationary, credit-stress, geopolitical or otherwise disorderly regimes may create unusual asymmetric opportunities.

Claude and ChatGPT are explicitly permitted to reject any of these ideas.

Likewise, do not assume an asset belongs in the portfolio simply because its price has recently fallen, its yield is high, or its narrative sounds macroeconomically plausible.

Rates research

Treat the yield curve as an investable opportunity set rather than treating “bonds” as one asset.

Compare at minimum:

- Treasury bills / near-cash;
- floating-rate Treasury exposure;
- intermediate-duration Treasuries;
- long-duration Treasuries;
- inflation-protected bonds;
- appropriate Canadian equivalents where relevant.

Specifically investigate TLT rather than assuming that “high rates = buy TLT.”

As of late September / October 1, 2026, long U.S. yields have risen substantially and the 10-year Treasury yield has moved above 5.3%.

TLT currently has roughly 15 years of effective duration. That means it can offer substantial upside if long rates fall, but substantial mark-to-market losses if long rates continue rising.

Determine what macro and market evidence would change TLT from:

WATCH → ACCUMULATE → INVALIDATED

Possible evidence may include rate trend, inflation trend, real yields, term premium, Fed path, growth deterioration, curve behavior, fiscal supply, credit stress and price/trend confirmation. Do not presuppose which signals are decisive.

Also examine whether short-duration or floating-rate Treasury exposure is currently the better way to earn income and preserve optionality while awaiting a long-duration setup.

“Chaos regime” research

Separate this into distinct mechanisms rather than using “chaos” as an asset class.

Bill Ackman's well-known 2020 COVID hedge and his later rising-rate trades illustrate two different ideas:

Credit-dislocation hedge: Pershing Square bought relatively inexpensive credit protection on investment-grade and high-yield credit indexes before spreads exploded during the COVID shock.

Rates hedge: Pershing Square later used payer swaptions to profit from a substantial rise in interest rates.

The lesson to investigate is not “copy Ackman.” Institutional CDS and swaption positions may be inaccessible, inappropriate or badly sized for a $5,000 retail account.

Instead ask:

Are there simple, liquid, retail-executable instruments that provide useful convexity when a specific macro regime becomes severely mispriced?

Investigate possibilities, but do not force a trade. A satisfactory conclusion may be that no affordable retail analogue currently has positive enough expected value.

Possible regimes include:

- renewed inflation acceleration;
- long-duration bond selloff;
- recession/disinflation;
- credit-spread shock;
- energy shock;
- equity volatility shock;
- liquidity event;
- sustained commodity trend.

Each regime should specify what observable evidence activates it.

Avoid assigning one political actor or policy a single-cause explanation for inflation or market behavior. Model the actual variables — fiscal impulse, monetary policy, supply constraints, energy, credit conditions, productivity, capital spending and market pricing.

Portfolio architecture

Treat the $5,000 as incremental experimental capital, not Dustin's entire retirement portfolio.

Avoid false diversification. A $5,000 account does not need fifteen tiny positions.

The collaborators should determine the appropriate number of holdings and may keep part of the capital unallocated if current opportunities do not justify immediate deployment.

The final framework should distinguish between:

Strategic capital
Positions intended to survive ordinary bear markets and compound for years.

Tactical capital
Capital available for strong swing/trend opportunities.

Defensive/dry-powder capital
Capital earning a reasonable return while retaining optionality.

Asymmetric-risk budget
A deliberately small maximum amount, if warranted, that may be spent on convex or downside opportunities.

These are conceptual sleeves, not predetermined percentages. The collaborators must determine whether each one deserves capital.

Account and implementation realism

State explicitly:

- whether figures are CAD or USD;
- FX assumptions and conversion costs;
- the intended account type where it materially affects implementation;
- whether a proposed instrument is actually available in that account;
- tax/account restrictions that materially affect the trade;
- liquidity, spread and option-contract-size constraints.

Do not construct a position that is theoretically attractive but impractical with a $5,000 capital base.

Required final proposal

For every proposed position, provide:

Field| Requirement
Instrument| Exact ticker / security
Role| Strategic, tactical, defensive, hedge, etc.
Allocation| Dollar amount and percentage
Thesis| Why this exposure exists
Entry| Buy now, staged, or conditional trigger
Horizon| Expected holding period
Invalidation| What would prove the thesis wrong
Risk control| Stop, sizing rule or other containment
Exit / rebalance| Conditions for reducing or closing
Key risks| The important ways the thesis can fail

Also provide an unallocated-capital rule. “Wait” must be a legitimate portfolio decision rather than a failure to produce an idea.

The final proposal must total no more than $5,000.

Collaboration protocol

Keep the interaction bounded.

Round 1 — Claude independent proposal

Claude performs current research using live market information, repository context and available tools.

Produce an independent proposal before optimizing toward what ChatGPT might prefer.

Write the result into the experiment record.

Round 2 — ChatGPT independent review and counterproposal

Dustin will hand Claude's Round 1 output to ChatGPT.

ChatGPT will:

- identify agreement;
- identify material disagreements;
- challenge weak assumptions;
- identify missing instruments or regime risks;
- propose changes where warranted;
- distinguish factual disagreement from differences in portfolio philosophy.

ChatGPT should not change something merely to appear independent.

Round 3 — Claude synthesis

Dustin will return ChatGPT's review to Claude.

Claude should adjudicate the disagreements using evidence and produce a revised proposal.

If the substantive disagreements are resolved, stop here.

Optional Round 4 — ChatGPT red-team

Use only if a material unresolved question remains.

Focus only on unresolved issues rather than reopening the entire design.

Optional Round 5 — Claude final

Use only if Round 4 produced a material correction.

Five interactions is a hard ceiling. Two or three substantive exchanges are preferred.

Suggested repository structure

Keep this intentionally small:

exploratory/portfolio-strategy-collab-2026/
├── README.md
├── ROUNDS.md
├── PROPOSAL.md
└── WATCHLIST.md

README.md
The frozen owner brief, purpose, assumptions, collaboration protocol and evidence rules.

ROUNDS.md
Append-only record of Claude and ChatGPT exchanges. Each entry includes date, model, claims, disagreements and changes proposed.

PROPOSAL.md
The current consolidated $5,000 portfolio proposal. Do not treat it as immutable; preserve material changes in "ROUNDS.md".

WATCHLIST.md
Assets and macro setups that are interesting but do not currently justify capital. Include activation conditions and invalidation.

Do not create additional architecture unless actual use demonstrates a need.

Evidence standard

Use live sources for live claims.

Record the observation date beside changing values such as yields, valuation multiples, commodity prices, option pricing, volatility or trend state.

Distinguish:

OBSERVED — directly supported by current evidence.
INTERPRETATION — what the evidence may imply.
ACTION — what the portfolio actually does because of it.

Do not convert an interpretation into an action without stating the bridge between them.

Historical analogues are useful but are not proof that the current regime will resolve the same way.

Initial question for Claude

Start with the portfolio, not the documentation.

Given the market as it exists on October 1, 2026, what would you do with the $5,000?

Research enough to make the answer executable.

You may allocate all of it, some of it, or none of it immediately.

Pay particular attention to:

- the unusual long-rate environment;
- whether long duration is becoming attractive or remains premature;
- short-duration yield as paid optionality;
- energy and power infrastructure;
- broad equities versus concentrated opportunities;
- gold/metals;
- genuine trend/momentum setups;
- practical retail-accessible asymmetric hedges.

Then create the four lean repository files above and record your work as Round 1 — Claude.

Do not ask Dustin to choose among a menu of ideas before doing the analysis. Make a proposal, show your assumptions, and leave the final investment decision with him.