# Portfolio strategy collaboration — 2026

**Owner:** Dustin Watson · **Collaborators:** Claude and ChatGPT · **Opened:** 2026-10-01
**Status:** exploratory. Rounds 1–12 complete, all on 2026-10-01. **Round 12 was a consolidation round.** It:
- audited ten candidate principles and kept **four first pillar candidates** (not doctrine);
- wrote a gap map;
- made `MARKET_MODEL.md` current-only;
- defined the memory boundary and a do-not-build list;
- named the strongest self-deception risk;
- put the project under a **build freeze until the Nov 4 review**.

The investment decision always stays with Dustin.

What this is: a small, bounded experiment. Two AI systems propose, and then jointly refine, how $5,000 of incremental capital should be deployed, staged or deliberately left undeployed, and the rules that govern it afterward. It is not a study or an audit under `docs/conventions.md`, and it authorizes nothing in CuttingBoard or any other repository. It is not a trading system.

---

## Start here — the state of the collaboration (2026-10-01, after Round 12)

**What we know (observed, dated)**
- **Market state:** the Oct 1 DAILY STATE (`WATCHLIST.md` §1).
  - Rates and credit: 10Y 5.24%, real 10Y 2.93% (Sep 30); HY OAS 3.12%, IG 0.84%, CCC 11.79%.
  - Vol and dollar: VIX 16.4 vs MOVE 108; broad dollar flat since June.
  - Equities: SPY on its 50-day, with 23% of members above theirs.
- **Our evidence base is almost empty.** See the ledger below: zero completed paper trades, zero completed cohort events, zero tested thesis-state changes, and 12 rounds written in a single day.

**What we think (interpretation)**
- **Base case:** a policy-led real-rate repricing, with oil the likely but *inferred* trigger. Best alternative: growth-led normalisation (`MARKET_MODEL.md` §8).
- **Four first pillar candidates** (`RESEARCH_MAP.md`):
  - P1 — state before story, labelled honestly;
  - P2 — commit before you look;
  - P3 — the decision chain has separate links;
  - P4 — capital follows evidence.
- Reading rate-shock transmission is a skill for interpreting markets, not a trading edge.

**What remains uncertain** (the gap map in `RESEARCH_MAP.md`)
- Whether any strategy family has an edge: there are no outcomes yet.
- What drove the policy path: oil or growth.
- Dustin's whole-program exposures.
- Whether the daily state is maintainable and actually changes decisions.

**What would change our minds**
- W1–W5 (`MARKET_MODEL.md` §8).
- The pillar overturn conditions (`RESEARCH_MAP.md`).
- The single cohort read (~Nov 30).
- The first graded paper records.
- Program C's end-January test.

**Next dated evidence**

| Date | Event |
|---|---|
| Oct 7 | NFCI (week to Oct 2) and the 10Y auction |
| Oct 8 | 30Y auction |
| Oct 12 | UNH pre-registration (scheduled) |
| Oct 13 | UNH reports — the first cohort event |
| Oct 14 | CPI — tests P9 |
| Oct 15 | TSM — the first post-earnings thesis review |
| Oct 28 | FOMC — tests P10 |
| **Nov 4** | Refunding, base-case re-run, and the **build-freeze review** |

### Evidence ledger (update at every round; the counter that keeps the documentation honest)

| Item | Count at Round 12 (2026-10-01) |
|---|---|
| Rounds written · calendar days | 12 · **1** (Round 1 committed 12:59 ET, Round 11 at 20:25 ET; Round 12 — see its commit) |
| Frozen setups written · triggered · completed and graded | 10 · **0** · **0** |
| Expired without trigger | 1 (PT-001 ACN; shadow open to Dec 11) |
| Cohort events completed through D+20 | **0** of 10 (first: UNH, Oct 13) |
| Post-earnings thesis reviews | **0** (first: TSM, Oct 15) |
| Thesis-state changes made on evidence after the register opened | **0** |
| Predictions resolved (P1–P10) · contradictions resolved | **0** · **0** (10 OPEN: 5 contradictions, 5 research notes after the Round 12 re-screen) |
| Real-money decisions informed by the system (recorded) | **0** |
| Decisions taken outside a written rule | Not yet tracked — needs Dustin's report |

**Build freeze (Round 12, until the Nov 4 review).**
- **Not allowed:** new files, gauges, theses, strategy families or taxonomy.
- **Allowed:** daily states, scheduled records (cohort events, completions, reviews), dated annotations, and corrections. A correction includes verifying the source of an existing input; it does not include adding a new one. Each gap-map step carries a "When" that fits inside the freeze.
- **Early exit:** the freeze lifts early only for an outcome the current structure cannot record.
- **At the Nov 4 review the ledger decides two things:** what (if anything) is added, and what is cut. Any file section not used in a decision or review since Round 12 is a candidate for removal.

---

## System map

**Current system (as built after Round 12)**

```
INPUTS        live data (FRED, Yahoo, Treasury, filings) · Market Brief (read-only) · ChatGPT round prompts
                  │                                         Dustin decides; only he moves capital ─┐
                  ▼                                                                                │
OBSERVATION   a Claude session reads the data by hand                                              │
STATE         WATCHLIST §1   DAILY STATE (latest + previous)                                       │
MODEL         MARKET_MODEL   current interpretation: links, labels, theses, open contradictions, P/W│
OPPORTUNITY   WATCHLIST §3–§6  four buckets   ◄──  RESEARCH_MAP  programs, questions, gap map       │
DECISION      PROPOSAL  sleeve, gates, reallocation  ·  PAPER_TRADES  frozen setups  ◄──────────────┘
OUTCOME       PAPER_TRADES  completions, shadows, cohort            ← EMPTY: nothing completed yet
LEARNING      ROUNDS (history) → RESEARCH_MAP findings and pillar candidates
                  └─ so far fed by argument between two models, not by outcomes
MIRRORS       claude.ai project copies (read-only, stamped with a commit) · memory (pointers only)
```

**Probable mature system (only if the evidence supports it; still small)**

```
OBSERVATION   Market Brief + at most one small script that fills the daily state's Observed fields
                 (the only software that may earn a place, and only after the freeze)
STATE         WATCHLIST: daily state, gauges, four buckets
MODEL         MARKET_MODEL: current only; resolved items leave for ROUNDS
OPPORTUNITY   WATCHLIST buckets ◄── RESEARCH_MAP (questions that produce candidates)
DECISION      PROPOSAL, matured into decision rules: gates, sizing, reallocation, the exposure map
              PAPER_TRADES: frozen setups; paper and micro-live records in one ledger
OUTCOME       PAPER_TRADES graded completions · cohort reads · post-earnings reviews
LEARNING      ROUNDS → MARKET_DOCTRINE (only pillars that survived graded outcomes)
                 └──► MODEL (links and theses revised) · STATE (gauges kept or cut) · DECISION (rules for future records)
```

**Size ceiling:** no more than eight Markdown files (the seven above plus `MARKET_DOCTRINE`), no database, and at most one small script.

**Market Brief's place:** OBSERVATION only. Its hypotheses (H1–H5) enter at MODEL as claims to be tested, never as STATE.

---

## Memory and source-of-truth boundary (Round 12)

> **Memory helps the AIs resume work; Markdown proves what the work currently says.**

| Layer | Holds | Never holds | On conflict |
|---|---|---|---|
| **Markdown in `dwats250/strategy`** (source of truth) | Current hypotheses and states, frozen rules and records, the roster, paper observations, research conclusions, pillar candidates, decision rules | Chat transcripts; claims without a date or source | **Wins** |
| **Work memory** (Claude memory, chat context) | Where the next round begins; the latest round and commit; open questions for the other model; scheduled items; Dustin's standing working preferences | Values, thesis states, rules or roster contents — anything that goes stale and competes | Corrected from Markdown |
| **Mirrors** (claude.ai project copies) | Read-only copies for reading on other surfaces, each stamped with the commit it copies | Edits | Superseded by the repo |
| **History** (git, `ROUNDS.md`, archive sections) | Superseded interpretations, old rounds, stale setups, resolved contradictions, past daily states | The current state | Recoverable, not current |

**Timestamps come from the clock.** The git commit time is authoritative; a time written in a file is either read from a clock or written as "see commit" (methodology finding 11).

---

## What not to build (Round 12)

The objective is the smallest credible system capable of learning from markets.

| Not now | Why |
|---|---|
| Knowledge graphs, ontologies, tag systems beyond the exposure-map tags | Structure without outcomes to organise |
| Scores for assets, theses or setups; numeric confidence | Nothing to calibrate them against yet. Words (FORMING…DORMANT) are honest about that |
| More derived indicators | The five daily cogs are the ceiling until one is retired |
| AI-written daily narratives | The daily state cites thesis names and contradiction IDs. Prose invites storytelling, which P1 forbids |
| A backtesting engine or historical-study infrastructure | The queued studies are one-off reads, not systems |
| A dashboard or web app for the roster | Markdown is read; a dashboard would need maintaining |
| A wider universe (new tickers outside the cohort mechanics) | The cohort and roster already exceed what has been graded |
| A new file before the Nov 4 review; `MARKET_DOCTRINE` before graded outcomes | Build freeze; doctrine needs evidence (December target, conditional) |
| New theses in the register until an existing one changes state on evidence | Thirteen theses opened in one day is already a lot |
| Any coupling to CuttingBoard | A separate repository and a read-only boundary (`docs/conventions.md` §i) |
| Alerts, automation or order routing | Decisions stay with Dustin |

---

## Files

Keep it to these seven files (README, ROUNDS, PROPOSAL, WATCHLIST, PAPER_TRADES, RESEARCH_MAP, MARKET_MODEL) unless real use shows a need for more. MARKET_MODEL (added in Round 11) holds *current interpretation*; RESEARCH_MAP holds *open questions and programs*. The purposes differ, so the files stay separate.

| File | Question it answers | What it holds | Edit rule |
|---|---|---|---|
| `README.md` | Where are we, and how does this work? | Status, Start here, evidence ledger, system map, memory boundary, do-not-build, protocol, evidence rules, frozen owner brief | Brief frozen (amend only by dated note); the rest updated in place |
| `WATCHLIST.md` | What is happening now? | DAILY STATE (template + latest + previous), base case, four buckets, dated decision points, lifecycle, archive | Latest two daily states only (older in git); stale items archived, not deleted |
| `MARKET_MODEL.md` | Why might it be happening, and what would show we are wrong? | Transmission map, causality labels, instrument map, missing cogs, thesis register, contradictions, adversarial challenge | **Current only** (Round 12): resolved contradictions and old state changes move to `ROUNDS.md` with their evidence when the round closes |
| `RESEARCH_MAP.md` | What deserves continued investigation? | Programs, long-horizon theses, methodology findings, cohort, research queue, pillar candidates, gap map | Updated in place; one-line note in `ROUNDS.md` |
| `PAPER_TRADES.md` | Were our setups, timing, vehicles and decisions useful? | Frozen setups, ledger, completions, shadows, dated annotations | Plans frozen; changes only by dated annotation |
| `PROPOSAL.md` | What rules govern deployment? | The sleeve, gates, speculation lane, capital reallocation | Replaced each round; material changes logged in `ROUNDS.md` |
| `ROUNDS.md` | How did the system evolve? | Each exchange; resolved contradictions and state history at round close; provenance corrections | Append-only |

## Standing assumptions (Round 1; challenge in any round)

- Figures in **CAD** unless marked US$. USD/CAD 1.4244 (Oct 1, 2026).
- Accounts (Round 6): TFSA, margin account and LIRA are all available; account choice is an execution note made at the trigger and never limits what the lab studies.
- Options toolkit: long calls and long puts only (no spreads, no written options). Paper research has no premium cap; live premium at risk ≤ C$100 (C$150 A+, earned by a family) — see `PAPER_TRADES.md` §2.
- The $5,000 is incremental, experimental capital — not the whole retirement portfolio.

## Protocol

1. **Round 1 — Claude:** independent proposal. *(done 2026-10-01)*
2. **Round 2 — ChatGPT:** agreement, material disagreements, weak assumptions, missing instruments or regimes, proposed changes; separate factual disagreement from philosophy. Do not change something just to appear independent. *(done 2026-10-01; added a required anti-anchor scan, executed by Claude)*
3. **Round 3 — Claude:** adjudicate with evidence; revised proposal. Stop here if resolved. *(done 2026-10-01)*
4. **Round 4 — ChatGPT (optional):** unresolved issues only. *(used 2026-10-01 as a mandate reset: Opportunity Sleeve, individual stocks, options, strategies; answered by Claude the same day)*
5. **Round 5 — Claude (optional):** only if Round 4 produced a material correction. *(ceiling first extended to Round 8 in ChatGPT Round 5, then removed in Round 7)*

**Convergence rule (Round 7, replaces the round cap).** A new round is justified only if it does at least one of:
- discovers a materially new opportunity;
- resolves or sharpens an important disagreement;
- reveals a methodological problem;
- converts an observation into a repeatable strategy;
- materially changes a long-horizon thesis;
- produces evidence about an existing strategy family.

No rounds for allocation or wording changes alone. The Round 10 checkpoint ("still discovering, or mostly repeating?") was held; see `ROUNDS.md` Round 10.

**Round 12 addition:** until the Nov 4 review, a round is justified mainly by the last criterion — **new evidence about something already specified.**

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