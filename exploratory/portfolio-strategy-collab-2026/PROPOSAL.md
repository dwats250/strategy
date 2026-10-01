# PROPOSAL — $5,000 Opportunity Sleeve

**Version:** Round 5 — Claude (Fable 5.1) · 2026-10-01 · amends Round 4 (full boards, option chains,
TSM/CBOE-CME/LNG analyses in `ROUNDS.md`, Rounds 4–5; prospective setups in `PAPER_TRADES.md`)
**Status:** Proposal for owner decision. Not executed. The final decision is Dustin's.

Claude is not a licensed financial advisor. Every figure carries its observation date in
`ROUNDS.md`; prices are Oct 1 intraday; USD/CAD 1.4244.

---

## 1. The answer

Three concentrated businesses (65%), one swing slot and one single-leg option slot armed with
written triggers (23%), a reserve (12%). No index fund, no bond fund, no bills.

| Slot | Instrument | Shares | CAD | % | Entry |
|---|---|---|---|---|---|
| Concentrated #1 | **TSM** (Taiwan Semiconductor ADR) | 2 | 1,299 | 26% | 1 now · 1 only if the Oct 15 print confirms (Q4 guide ≥ consensus, capex held/raised, >40% growth outlook intact) |
| Concentrated #2 | **CBOE** (Cboe Global Markets) | 3 | 1,194 | 24% | 2 now · 1 after Oct 30 earnings |
| Infrastructure | **LNG** (Cheniere Energy) | 2 | 767 | 15% | 1 now · 1 after Oct 29 earnings |
| Swing slot | First to qualify: VRT (base breakout) · ACN (gap continuation) · CLS or MU (pullback) | — | 1,000 earmark | 20% | Trigger only; risk ≤ C$150 |
| Option slot | Single-leg only (premium ≤ C$150). Today's only qualifying market: TLT Jan '27 82 call, if PT-006 triggers by Oct 17 | — | 150 earmark | 3% | Trigger only |
| Reserve | USD cash | — | 590 | 12% | — |
| **Total** | | | **5,000** | 100% | |

**Account (Round 5):** the **Questrade TFSA**. Options Level 2 — long calls and puts only, no
spreads. A margin account is opened only when a paper strategy reaches the MICRO-LIVE rung of
the `PAPER_TRADES.md` ladder; it is a graduation, not a prerequisite.

---

## 2. Why these three

**TSM — the bottleneck.** Forward P/E 20.1 for +63% FY26 EPS growth; August revenue +53% y/y;
capex raised to $60–64B; 4% below its high, above both moving averages. Every AI capex dollar
the hyperscalers have guided ($600B+ for 2026) passes through TSMC's fabs. The accepted tail is
Taiwan; the fundamental invalidation is two or more hyperscalers cutting capex or an N2 ramp
failure. No stop; a −30% quarter is tolerated.

**CBOE — owning the casino.** Of the three exchanges, CBOE has the growth (Q2 revenue +25%,
adjusted EPS +45%, 2026 organic growth guided up to mid/high-teens) at the lowest multiple
(19.0x forward), a 6.5% FCF yield, a dividend raised 19%, and the S&P/VIX licence just extended
to 2051 — and it is 25% below its high after an unexplained September slide. CME was the
mandate's suggestion and was rejected on evidence: 21x for +5.5% growth, and its 2022 EPS rose
only 1.5% through the biggest volatility year in a decade — the "chaos tollbooth" earns on
rates volume, not on fear. CBOE's index options franchise is the purer expression. Invalidation:
options volumes negative y/y for two quarters, a regulatory fee cap, or loss of exclusivity.

**LNG — contracted gas exports, not a gas price bet.** Forward P/E 15.4, EV/EBITDA 10.5, 2026
distributable cash flow guided to $5.3–5.8B (~10% of market cap) with Stage 3 substantially
complete so capex falls from here; $1.1B bought back in H1; a new Petrobras SPA. WMB, the
mandate's suggestion, was rejected: 28x forward for +6.7% growth with negative free cash flow
and 4.3x leverage — a bond proxy with execution risk. Invalidation: a contract default or a
supply glut that breaks take-or-pay recontracting.

Three mechanisms — AI silicon manufacturing, structural hedging demand, US gas exports — with
little fundamental overlap. Concentration is the point; variance is accepted.

---

## 3. The armed slots

**Swing slot (C$1,000 earmark, risk ≤ C$150 per trade, one at a time).** Strategies and
triggers are in `ROUNDS.md` Round 4 §B. Current status:
- **VRT** (Strategy E): 3-week base 234–257, 50-day 262. Trigger = weekly close above 262 on ≥1.5× volume. Buy 3–4 shares, stop 232. Earnings Oct 21 sit inside the hold.
- **ACN** (Strategy A): gapped +18% today on ~3.8× volume. Qualifies only if day-1 closes in the upper half of 214.50–227.63, or on a close above 227.63 within 10 sessions. Buy 3 shares, stop under 214.50 (risk ≈ C$57).
- **CLS / MU** (Strategy B): both extended; wait for an orderly 8–12% pullback into the 20-day, then buy the first close above the prior day's high.
- Not qualified today: none of the four. The slot stays armed, not filled.

**Option slot (single leg, premium ≤ C$150, ≥ 60 DTE, bid–ask ≤ 10%, OI ≥ 500).** Read live
Oct 1 ~14:00 ET: the only structure that passes is the **TLT Jan 15 '27 82 call** at 1.05/1.07
(IV 15.7%, OI 28,594) = C$152, used only if PT-006's duration-turn trigger fires by Oct 17 so
that ≥ 90 DTE remain; afterwards the vehicle is TLT shares. Everything else was priced and
rejected: SPY Dec 740 put C$1,697; ACN Dec 240 call C$1,370; VRT Dec 260 call C$3,170; CBOE
Jan 300 call C$2,140 (IV 40%); MU Dec 1100 call C$14,000; ITB chain illiquid with non-standard
strikes; FICO markets $5–18 wide. **Downside** is expressed with SH shares (paper reference:
short SPY) under PT-005 — the Round 4 put spread is deleted. If a single leg is too expensive,
the answer is NO TRADE, not a bigger budget.

---

## 4. Rules

1. Stock swing: risk = stop distance × shares ≤ **C$150**; notional ≤ C$1,300; one open at a time (two only if uncorrelated).
2. Option: one single-leg position open; premium ≤ **C$150**; ≥ 60 DTE at entry; thesis expiry stated; exit at −50% of premium or at the underlying invalidation, whichever first; never hold into the last 30 days.
3. Durable holds: no stop. A −20% mark-to-market forces a written review in `ROUNDS.md`; only fundamental invalidation forces a sale.
4. No borrowing on margin. No averaging down a tactical position.
5. Every entry is logged (date, trigger evidence, source) before the order.
6. Unused risk budget is a position. If no swing or option trigger fires by **Jan 15, 2027**, the earmarks are re-screened through the candidate board — not spent.
7. Correlation check: TSM and a semis swing (MU/CLS) count as correlated; if the swing slot holds one, no second long in the same theme.
8. Live capital enters the swing slot only for a setup that has passed PAPER TRADE and REPEATED OBSERVATIONS in `PAPER_TRADES.md`.

---

## 5. Against the boring benchmark

The benchmark is one all-in-one global equity ETF at roughly the index multiple (19.2x), broad,
in a TFSA, needing no attention. The sleeve accepts single-name risk (65% in three names, with
TSM's Taiwan tail), earnings-timing risk (all three report within 30 days), 100% USD exposure,
a taxable account, and the behavioural load of six rule-sets.

It expects to be paid because all three holdings sit at or below the index multiple with growth
far above it (TSM 20x / +63%; CBOE 19x / +45%; LNG 15x / ~10% cash yield), two of the three
return cash aggressively, and each owns a multi-year mechanism the benchmark dilutes to noise.
Said plainly: concentration raises variance more reliably than return; CBOE's case rests on
volumes staying elevated; the tactical slots are where retail accounts leak. If Dustin would
not hold TSM through a −30% quarter, the benchmark wins. If he would, this is a market-multiple
bet on three above-market businesses with tactical risk capped near C$500 in total.

Full candidate board (18 names), strategy board (6 setups) and option chains: `ROUNDS.md`, Round 4.
TSM staging, CBOE-vs-CME engines and the LNG stress test: `ROUNDS.md`, Round 5. CME is approved
as a regime candidate (Strategy F trigger ≤ ~$220); LNG's "capex falls from here" is corrected to
"capex stays elevated and self-funded" with two open items (contracted % / expansion coverage).
