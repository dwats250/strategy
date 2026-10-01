# Portfolio strategy collaboration — 2026

**Owner:** Dustin Watson · **Collaborators:** Claude and ChatGPT · **Opened:** 2026-10-01
**Status:** exploratory. Round 1 (Claude) complete; awaiting Round 2 (ChatGPT).

A small, bounded experiment: two AI systems independently and then jointly propose how
$5,000 of incremental capital should be deployed, staged or deliberately left undeployed, and
the rules that govern it afterward. The investment decision stays with Dustin.

This is not a study or an audit under `docs/conventions.md`, and it authorizes nothing in
CuttingBoard or any other repository. It is not a trading system. Keep it to these four files
unless real use shows a need for more.

## Files

| File | What it holds | Edit rule |
|---|---|---|
| `README.md` | Purpose, assumptions, protocol, evidence rules, frozen owner brief | Brief is frozen; amend only by a dated note below it |
| `ROUNDS.md` | Each exchange: date, model, claims, disagreements, changes | Append-only |
| `PROPOSAL.md` | The current consolidated proposal | Replaced each round; material changes logged in `ROUNDS.md` |
| `WATCHLIST.md` | Setups without capital: evidence, activation, invalidation | Updated each round; trigger events logged with date and evidence |

## Standing assumptions (Round 1; challenge in any round)

- Figures in **CAD** unless marked US$. USD/CAD 1.4244 (Oct 1, 2026).
- Account: **Questrade TFSA** (a LIRA cannot accept new contributions). RRSP is the alternative for US-listed holdings because of the treaty withholding exemption.
- Registered accounts allow long calls/puts, covered calls and cash-secured puts — **no spreads**.
- The $5,000 is incremental, experimental capital — not the whole retirement portfolio.

## Protocol

1. **Round 1 — Claude:** independent proposal. *(done 2026-10-01)*
2. **Round 2 — ChatGPT:** agreement, material disagreements, weak assumptions, missing instruments or regimes, proposed changes; separate factual disagreement from philosophy. Do not change something just to appear independent.
3. **Round 3 — Claude:** adjudicate with evidence; revised proposal. Stop here if resolved.
4. **Round 4 — ChatGPT (optional):** unresolved issues only.
5. **Round 5 — Claude (optional):** only if Round 4 produced a material correction.

Five rounds is a hard ceiling; two or three is the target.

## Evidence rules

- Live sources for live claims; an observation date beside every changing value.
- Label claims **OBSERVED** (supported by current evidence), **INTERPRETATION** (what it may imply) or **ACTION** (what the portfolio does). State the bridge from interpretation to action.
- Historical analogues inform; they do not prove.
- No single-cause political explanations; model the variables (fiscal impulse, monetary policy, supply, energy, credit, productivity, capex, market pricing).

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