# WATCHLIST — setups that do not yet justify capital

**Version:** Round 4 — Claude (Fable 5.1) · 2026-10-01 · supersedes Round 3 (changes in `ROUNDS.md`)

**Round 4 note.** The sleeve was reset to an Opportunity Sleeve (`PROPOSAL.md` Round 4). Sections 1–6
below are kept as macro reference and as the evidence stack for Strategy D; Brazil (5a) and the
duration ladder (1) are no longer funded from this sleeve. Section 0 is the live tactical board.
Each entry has a status, the evidence for it (with observation dates), the activation
conditions, and invalidation. Funding for anything activated comes from the SGOV sleeve under
`PROPOSAL.md` §4. A trigger counts only once it is logged here or in `ROUNDS.md` with date and
evidence.

Status vocabulary: **WATCH** (no capital) · **PRE-APPROVED** (conditional entry written in `PROPOSAL.md`) · **ACCUMULATE** (staged buying allowed) ·
**ACTIVE** (held) · **INVALIDATED** (stand aside until re-set) · **PARKED** (rejected for now).

---

## 0. Round 4 tactical board — armed triggers (Oct 1, 2026)

| Candidate | Strategy | Trigger (objective) | Size / stop | Status |
|---|---|---|---|---|
| **VRT** $248.65 | E — base breakout | Weekly close > 262 (50-day) on ≥1.5× avg volume; base 234–257 | 3–4 sh; stop 232 (risk C$128–171) | Armed |
| **ACN** $216.81 | A — gap continuation | Day-1 close in upper half of 214.50–227.63, or a close > 227.63 within 10 sessions | 3 sh; stop under 214.50 (risk ≈ C$57) | Armed — day-1 close pending |
| **MU** $1,077 | B — pullback continuation | Retest of 20/50-day (50d 953) holding 3 sessions, then close > prior high | 1 sh only; stop 2×ATR | Armed (extended now) |
| **CLS** C$506 | B — pullback continuation | First 8–12% pullback into the 20-day, then close > prior day's high | 2 sh; stop 2×ATR (≈C$56/sh) | Armed (extended now) |
| **UNH** $364 | A — on Oct 13 reaction | Gap ≥ +8% on beat/raise with day-1 close in upper half | 2 sh; stop gap-day low | Watch |
| **HWM** $228 | E — base breakout | Weekly close > 50-day (260) from the 224–233 range | 3 sh; stop 222 | Watch |
| **FICO** $662 | C — post-shock reversion | ≥10 sessions without a new low (< 586), reclaim of 20-day, then close > base high | 1 sh; stop under base low | Watch — not qualified |
| **SPY** 764.5 | D — macro downside | Daily close < 750 with ≥3/5 evidence conditions | Dec 18 720/700 put spread, debit ≤ 2.60 (C$350) | Armed; price condition not met |
| **CEG** $260 | D variant — single-name downside | Close < 229 (52w low) then failed retest | Put spread if debit ≤ C$350 | Watch |

Durable-hold alternates (Strategy F) if a core name is invalidated: **SPGI** ($390, 20.9x,
−29% from high) for CBOE; **ICE** ($152, 18.5x) for CBOE if a rates-turn kicker is wanted;
**ASML** and **FFH.TO** are quality names blocked by share price at this account size.

---

## 1. The yield curve — two-stage rates ladder (MBB first, TLT second)

**Status: WATCH.**

### The curve as an opportunity set (Sep 30, 2026, Treasury par and real curves)

| Segment | Instrument | Yield | Duration | Read |
|---|---|---|---|---|
| Bills / near-cash | SGOV, USFR | 3M bill 4.20%; SGOV SEC 3.67%, USFR 3.81% (Sep 29) | ~0.1 / ~0.0 | **Held.** Paid optionality. Floating (USFR) slightly better while the Fed hikes. |
| Front end | 2Y note | 4.88% | ~1.9 | Already prices roughly 100 bp above the 3.75–4.00% funds range. Rallies first when the Fed stops. |
| Belly | **MBB** (agency MBS; IEF fallback) | MBB YTM 5.94%, SEC 4.50%; IEF YTM 5.24%, SEC 4.91% (Sep 29–30) | 5.92 (IEF 6.84) | **Stage A instrument** (Round 3: MBB replaces IEF). +70 bp yield for less duration; current-coupon OAS 36 bp, widest since Aug 2025 (Goldman, Sep 17). Low WAC (3.63%) vs 7.6% mortgage rates means little refinancing convexity cost. Fallback to IEF if MBB OAS > 50 bp. |
| Long end | TLT (20Y+) | SEC 5.49%; 30Y 5.64% | 14.63 | **Stage B candidate.** Carries term-premium and supply risk on top of the Fed path. |
| Inflation-protected | TIP | 10Y real 2.93%, 30Y real 3.33%; 10Y breakeven 2.36% | 6.16 | Real yields near their highest since the mid-2000s (interpretation; long history not retrieved). Preferred over nominals if the inflation branch activates. |
| Canada | ZTL (unhedged US long Treasuries, CAD-listed) / ZTL.F (CAD-hedged) | YTM 5.31%, duration 14.9 (Aug 31) | ~15 | Same exposure as TLT in CAD wrapping. ZTL.F's hedge costs roughly the US–Canada short-rate gap (~1.8 pp/yr: 4.20% vs 2.39% 3M bills). |
| Canada | ZFL (long Canada) | YTM 4.09%, duration 15.7 (Aug 31) | ~16 | Different thesis: BoC at 2.25% and on hold, Canadian CPI-trim 1.9%. Not a substitute for US long duration. |

### Why WATCH and not ACCUMULATE (OBSERVED, dated)

- TLT $77.56 (Oct 1) — 52-week low 76.76, below its 50-day (81.90) and 200-day (85.52) averages (Financhill, Sep 30). Downtrend intact.
- The 10Y rose 4.44% → 5.29% in Q3 (+85 bp); about 73 bp of that is real yield, about 12 bp breakeven (Treasury, Jun 30 vs Sep 30). The market is demanding more real return and term premium, not pricing more inflation.
- Fed hiked 25 bp to 3.75–4.00% on Sep 16 (12–0); SEP median ~4.1% for end-2026; next FOMC Oct 27–28. October hike odds swung between ~39% and ~72% in the last week of September across sources; December odds reported near 90%.
- Kim-Wright 10Y term premium ~1.02% (Sep 25), up from 0.93% (Sep 22).
- MOVE 101.8 (Sep 28) to 106.6 (Sep 29) — a record in Saxo's 83-reading sample, up ~35% in September. VIX ~16–17.
- Auctions mixed: 10Y (Sep 9) and 30Y (Sep 10) stopped through; 20Y (Sep 15) tailed 2.0 bp with 52.5% indirects; 5Y (Sep 23) tailed 3.1 bp.
- Reported drivers (several, none sole): deficits and supply; oil (Brent ~+40% from late-June lows) tied to the Iran conflict; the Fed's hiking path; stronger growth data (Q2 GDP revised to 2.2%, ADP +90k); global long-end pressure (BoJ, France/Italy); a debate about the Fed's reaction function. Treasury has doubled long-end liquidity buybacks (≥$4B per operation, Sep 9–Nov 4).
- TLT 30-day IV 16–18%, IV rank 96–100 (Sep 30). Options on TLT are expensive.

**Interpretation.** Long duration is cheap on valuation (5.6% nominal, 3.3% real at 30 years)
but nothing yet says the repricing is finished. The Fed is still hiking, rates volatility is
at a high, and the drivers are term premium and real yields, which can keep rising after the
Fed stops. "High rates = buy TLT" ignores that the front end and the long end will likely turn
at different times. If the Fed stops first, the belly rallies first; the long end needs its own
evidence (supply absorbed, volatility falling).

### State machine (Round 3): NONE → STAGE A (MBB) → STAGE B (TLT)

"Fed stops hiking" is **not** a gate in either transition (ChatGPT Round 2, accepted); it is one
signal among several. Transitions are built from the long-yield trend, the real-yield trend,
breakevens, curve and volatility behaviour, and price confirmation.

**NONE → STAGE A (buy MBB, ≤ US$300 from the reserve)** — all three mandatory, plus any one optional:

- (M1) **Nominal trend:** 10Y weekly close below its 10-week (≈50-day) average, and that average no longer rising.
- (M2) **Price:** MBB weekly close above its 50-day average.
- (M3) **Not an inflation scare reversing:** 10Y breakeven ≤ 2.45% and not rising over the prior four weeks.
- Optional (one of): (a) 30Y real yield ≥ 20 bp below its cycle high for two weeks; (b) MOVE < 95; (c) 2Y yield ≥ 25 bp below its cycle high for five sessions; (d) core PCE 3-month annualized ≤ 2.75%; (e) 3-month average payrolls < 50k or 4-week claims ≥ 15% above their cycle low.

Sizing: two tranches of US$150; second only if the first is not under water after two weeks.
Alternative equity expression logged: ITB (homebuilders, −15% 3M, trailing P/E 14) tends to
lead a duration turn; eligible under the tactical template on the same M1–M3 signals.

**STAGE A → STAGE B (buy TLT, ≤ US$300 — from the reserve; if the reserve is exhausted, roll MBB into TLT)** — all three mandatory, plus any two optional:

- (M4) Stage A held ≥ 2 weeks and not under water.
- (M5) **Price:** TLT weekly close above its 50-day average with that average flat or rising.
- (M6) 30Y yield ≥ 30 bp below its cycle high on a weekly close.
- Optional (two of): (f) MOVE < 90; (g) two consecutive 20Y/30Y auctions without a tail; (h) 30Y real yield < 3.0%; (i) 2s10s stops steepening for four weeks; (j) 10Y breakeven stable or falling while nominals fall.

**Exception — flight to quality.** If HY OAS ≥ 4.0%, one US$150 TLT tranche is allowed on price
confirmation alone (TLT weekly close above its 20-day average after the spread move), because a
credit shock can pull long Treasuries up before any of M1–M6 are met.

**Not chasing.** If TLT rallies ≥ 8% from its low without the transitions, the miss is accepted;
re-entry on a retest that satisfies M5.

### INVALIDATED (once held)

- A weekly close with the 10Y ≥ 40 bp above the yield at the first tranche — exit everything. At TLT's ~14.6 duration that caps the mark-to-market loss near ~6% of the tranche; ~2.4% on MBB (duration 5.9).
- MBB-specific: current-coupon OAS > 50 bp (an MBS-specific dislocation) — switch to IEF rather than exit duration.
- Or: 10Y breakeven > 2.60% and rising **together with** real yields (an inflation regime, not a term-premium regime) — exit nominals; consider TIP instead.
- After invalidation the status resets to WATCH; the conditions above must be met again from scratch.

**Not chasing.** If TLT rallies 8%+ from its low without the triggers, the miss is accepted.
Re-entry comes on a retest that meets the price rule.

---

## 2. Gold (GLD / CGL.C) and metals

**Status: WATCH.**

OBSERVED: gold ~$4,166/oz (Oct 1), about −25% from its ~$5,589 record (Jan 28, 2026); about
−8.5% in September. GLD 380.84 (Sep 30) vs 50-day ~396 and 200-day ~416. The 10Y TIPS real
yield rose ~44 bp in September, the fastest monthly rise in four years. Central banks bought
~130 t through July (WGC, Sep 3). COMEX managed-money net long 127,389 contracts (Sep 22) —
positioning not yet washed out. GLD 30-day IV 20.5%, IV rank 12 (Sep 30). Silver ~$60.67,
about −50% from its January record.

Interpretation: the long-term case (official-sector buying, fiscal stress) is intact, but the
short-term driver — real yields — is still moving against gold, and the trend is down on both
averages. A falling price is not a reason to own it.

Activation (either):
- **Trend route:** GLD weekly close above its 50-day average **and** the 10Y real yield ≥ 20 bp below its cycle high for two weeks → US$175. Second US$175 on a weekly close above the 200-day.
- **Capitulation route:** gold ≤ $3,800/oz (≈ −32% from the record) **with** the latest WGC monthly central-bank figure still net buying → US$175 starter without trend confirmation.

Once held, gold is a strategic diversifier capped at ~10% of the C$5,000. Vehicle: GLD (USD),
or CGL.C (TSX, unhedged CAD) to avoid FX; CGL is CAD-hedged.

Invalidation (once held): weekly close 8% below the starter fill, or the 10Y real yield making
a new high above 3.2% while GLD makes a new low.

Silver, GDX: **PARKED.** Higher-beta versions of the same thesis while its driver is still adverse.

---

## 3. Power and electrification — tactical candidates

**Status: WATCH (tactical only; not strategic at current valuations).**

On "BE vs TE": in hindsight BE was the far stronger expression — but they were never the same
thesis. **TE is T1 Energy**, a US solar-module/cell manufacturer ($3.73, −44% YTD, Oct 1); its
drivers are solar trade policy and manufacturing margins. **BE (Bloom Energy)** sells on-site
fuel-cell power to data centers ($276.57, +218% YTD, market cap ~$81.5B, Oct 1). The lesson
is not "buy BE now"; it is to match the instrument to the mechanism (AI power demand → firm,
on-site or grid capacity).

| Ticker | Oct 1 | YTD | vs 50 / 200-day | Note |
|---|---|---|---|---|
| BE | $276.57 | +218% | above both (234.8 / 206.4) | 52-wk high $351; 2026 revenue guide $3.9–4.2B (≈20× sales); island-reversal flagged after Oracle/"Project Jupiter" concerns; Nebius 328 MW deal. |
| GEV | $997.88 | +53% | above both | Cleanest trend in the group. |
| ETN | $434.61 | +38% | above both | Lower volatility; electrical equipment. |
| GRID | $177.11 (Sep 30) | +17% | n/a | Basket expression; 52-wk range 144.62–199.99. |
| VST / CEG | $140.33 / $260.92 | −13% / −26% | below both | Independent power producers are being hit by rates; not a buy on trend. |

Hyperscaler 2026 capex guidance among the five calendar-year guiders is ~$600–634B, with
Alphabet flagging a further increase in 2027.

Activation (per the PROPOSAL §3.4 template): weekly trend up (price above a rising 50-day,
50-day above 200-day), 3-month relative strength vs SPY positive, entry on a breakout above
a defined pivot or a pullback holding the 50-day, stop at about 2× ATR. Preference order:
GEV or ETN (trend quality) → GRID (diversified) → **BE only** on a close above the top of its
island-reversal gap (Dustin to mark the level on the chart before any order).

Invalidation: weekly close below the 50-day with the 50-day rolling over; or a capex-cut
headline from two or more hyperscalers.

---

## 4. Energy (XLE / XEG)

**Status: WATCH.**

OBSERVED: XLE 61.50 (Sep 30), just below its 50-day (~61.91), ~+41% YTD (unverified
snapshot); XEG.TO +58% YTD. S&P energy forward P/E 13.3, the lowest of 11 sectors; Q3
earnings growth estimate +111% (FactSet, Sep 25). WTI 90.42 (Sep 30 settle), ~+30% since late
June; Brent ~+40%. US–Iran talks stalled; OPEC+ expected to hold targets; Qatar LNG force
majeure extended through November.

Interpretation: earnings support is real, but the price carries a geopolitical risk premium
that a deal could remove quickly. That is a binary, not a trend to join after +40–60%.
XEQT's Canadian weight already holds energy.

Activation (tactical long, either):
- WTI holds ≥ $85 for 10 sessions **after** a material talks outcome (deal or breakdown) **and** XLE closes a week back above its 50-day.
- After a risk-premium collapse (oil −20% from here), XLE re-tests its 200-day and holds for two weeks with WTI stabilizing.

Invalidation: WTI < $75, or XLE weekly close below its 200-day after entry.
Energy calls (USO/XLE): **PARKED** — the premium already prices the shock (USO IV30 ~46%).

---

## 5. Semiconductors / AI momentum (SMH)

**Status: WATCH (tactical only).** XLK was the only S&P sector up in September (+5.1%);
SMH +9.4% in September and ~+69% YTD (24/7 Wall St, Oct 1). A genuine trend, but crowded, and
XEQT already owns it. Eligible under the §3.4 template if a pullback holds the 50-day; not a
chase.

---

## 5a. Brazil — EWZ · **PRE-APPROVED** (new, Round 2 scan)

Conditional entry written in `PROPOSAL.md` §3.4: no entry before the election result (Oct 4 /
runoff Oct 25); then ≤ US$400 on a weekly close above both the 200-day and the Oct 2 close; the
earmark lapses after 8 weeks without confirmation. OBSERVED (Oct 1): EWZ $36.86, P/E 9.8–11.1,
trailing yield ~4%, 3M +7.8%, above 200-day; Selic 13.75% (5th cut Sep 17); IPCA 4.22%; USD/BRL
5.23; polls ~even. Invalidation: weekly close below the 200-day; USD/BRL > 5.60; BCB pause with
IPCA > 5%.

## 5b. Uranium — U.UN (Sprott Physical), URNM, CCO · **WATCH** (new, Round 2 scan)

OBSERVED (Aug 31 / Sep 30): spot U3O8 $89.68 and term $96.50, both +19% y/y; URA −14% and URNM
−19% over 1 year; SPUT (U.UN) at a **13% discount to NAV** (NAV US$21.52, price $18.72, 81.7M lb);
Cameco forward P/E ~66, realized Q2 price $67.79 vs ~$85 spot. Interpretation: the discount is
the mechanism — while SPUT trades below NAV it cannot issue units to buy pounds, so the spot
market has lost its marginal financial buyer; producers' realized prices lag term prices until
legacy contracts roll. Activation: SPUT discount < 5% for two weeks **and** URNM weekly close
above its 50-day → tactical position in U.UN (TSX, CAD, physical) under the template.
Invalidation: discount re-widens past 10%; term price falls below $90. Rejected for capital now
— a closed-end discount with no catalyst can persist for years.

## 5c. Candidates screened in the Round 2 scan and parked

| Idea | Evidence (Oct 1) | Why parked | Revive if |
|---|---|---|---|
| Tankers (FRO, STNG, INSW) | +67–134% YTD; VLCC composite ~$490k/day (Sep 10); Hormuz traffic 5–10% of normal; orderbook 20–25% of fleet | War premium already repriced 2–3× in the equities; single binary (Iran) with a two-sided tail; supply wave coming | Tactical only, on confirmed re-acceleration of spot rates after a pullback |
| Japan banks | BoJ 1.25% (hiked Sep 18); JGB 10Y 3.10% (30-yr high); EWJ +21% YTD, CAPE 35.6 | Thesis sound, no verified retail bank vehicle; DXJ is hedged exporters; XEQT holds ~6% Japan | A liquid Japan-financials ETF or ADR basket is verified |
| Homebuilders (ITB) | −15% 3M, trailing P/E 14, 5% above 52-wk low; mortgage 7.60% | Same bet as duration with equity beta | Logged as Stage A alternative (above) |
| Munis (MUB) | 10-yr ratio ~80% vs 71% avg; worst month since 1987 | Tax exemption is worthless to a Canadian; 3.4% < bills | — |
| Agency mREITs (NLY, AGNC) | ~16% yields at 52-wk lows | Levered MBS; MBB is the clean version | — |
| Coal / aluminum / lithium equities | Commodity up, equity down (BTU −26% 3M; AA −22% YTD; ALB −26% YTD) | Company-specific; tactical only | Template setup with trend confirmation |
| Canadian telecoms (T, RCI.B) | T −35% YTD after a 55% dividend cut | Deteriorating, not dislocated | — |
| Poland / Greece (EPOL, GREK) | +27% / +31% YTD, above 200-day, GREK P/E 12.6 | Not inspected; small funds | Next scan |
| Canadian rate-reset preferreds (ZPR) | +16.7% YTD, 5.1% yield, at highs | Fine instrument, wrong mandate | — |

## 6. "Chaos regime" map

Each mechanism is separate. "Activated" means the observable condition is met; the instrument
column says what a $5,000 TFSA could actually do.

| Regime | Activation evidence | Retail instrument | Status (Oct 1) | Conclusion |
|---|---|---|---|---|
| Inflation re-acceleration | Core PCE 3-mo annualized > 3.5%; 10Y breakeven > 2.6%; oil > $100 sustained | TIP over nominals; energy watch | **Partial:** oil shock yes; core CPI 2.4% y/y, core PCE 3.0% y/y; breakeven 2.36% stable | Inactive. Keep duration closed; TIPS preferred if it activates. |
| Long-duration selloff (bear steepener) | 30Y > 5.75%; tailing auctions; MOVE > 110 | Avoid duration (bills); TLT puts | **In progress:** 30Y 5.64%; MOVE ~102–107 | No trade. TLT puts are at IV rank ~100 — paying peak price for a move already made. Being in bills is the hedge. |
| Recession / disinflation | Payrolls 3-mo avg < 50k; claims rising; 2Y falling fast; bull steepening | MBB → TLT ladder | Inactive: Q2 GDP 2.2%, ADP +90k | The rates ladder (§1) is the expression. |
| Credit-spread shock | HY OAS > 4%; CCC stress; private-credit gating spreading to public markets | HYG puts ≥ 6 months out, ~8% OTM, under the three-part trigger in `PROPOSAL.md` §4.7 | Early warnings: HY OAS 3.12% and rising; gating headlines; IV rank 26 | **Budget authorized, $0 deployed** (Round 3: the Round 1 put had EV ≈ 0.73× premium). |
| Energy shock | Brent > $110 or a Hormuz/Red Sea disruption | XLE/USO calls | Premium already in price (Brent ~+40% since June) | Parked. The tail is two-sided (peace deal). |
| Equity volatility shock | VIX > 25 with term-structure backwardation | SPY puts, VIX calls | VIX ~16.8, futures in contango (18.25 → 21.00); SKEW ~145 | Parked. OTM SPY puts carry a high skew; VIX products bleed in contango. A credit shock large enough to matter would also hit equities, so the HYG put does double duty. |
| Liquidity event | Treasury-market dysfunction: MOVE > 130, failed or badly tailed auction, emergency facilities | Bills / cash | MOVE elevated, not dysfunctional | The SGOV sleeve is the instrument. |
| Sustained commodity trend | Broad commodity index above rising 200-day for 3+ months | Commodity ETFs | Mixed: oil up, gold and silver in drawdowns, copper firm ($6.49/lb) | No clean broad trend. |

---

## 7. Parked — considered and rejected for now

| Idea | Why parked | What would revive it |
|---|---|---|
| TLT calls (long-duration convexity) | IV rank 96–100; you pay peak volatility | IV rank < 50 with Stage B signals live |
| TBT / TBF (short long bonds) | Late in a +85 bp quarter; inverse/leveraged decay; adds to an already rates-short regime | Not planned |
| UVXY / VIX calls | Contango carry | VIX term structure inverts |
| Silver / GDX | Higher beta to an adverse driver | Gold's activation conditions met first |
| Canadian long bonds (ZFL, XLB) | Different central bank and cycle; lower yield than US long end | A Canadian-specific disinflation thesis |
| Copying Ackman's instruments (CDX, payer swaptions) | Not available in a TFSA; minimum sizes far above $5,000 | — |
| Short-dated HYG puts (Round 1) | Breakeven −6.5% in 3.5 months; a 2023-size spread widening pays zero; EV ≈ 0.73× premium | Replaced by the three-part trigger in `PROPOSAL.md` §4.7 |
