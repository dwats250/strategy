# PROPOSAL — $5,000 incremental capital

**Version:** Round 1 — Claude (Opus 5.5) · 2026-10-01
**Status:** Proposal for owner decision. Not executed. The final decision is Dustin's.
**Supersedes:** nothing (first version). Material changes are recorded in `ROUNDS.md`.

Claude is not a licensed financial advisor. This is a research proposal built from the
observations listed in `ROUNDS.md`, with every assumption stated so it can be challenged.

---

## 1. The answer

Deploy about half now, slowly, into one durable global-equity holding. Hold most of the rest
as paid-to-wait USD T-bills, with written triggers that decide when it moves. Spend 2% on
one small credit-shock hedge. Open no tactical position today.

| # | Instrument | Sleeve | Allocation (CAD) | % | Entry |
|---|---|---|---|---|---|
| 1 | **XEQT** (iShares Core Equity ETF Portfolio, TSX) | Strategic | C$2,700 | 54% | 3 tranches: Oct 2, Nov 2, Dec 1 |
| 2 | **SGOV** (iShares 0–3 Month Treasury Bond ETF, NYSE) | Defensive / dry powder | ~C$2,145 (~US$1,506) | ~43% | Now, after FX conversion |
| 3 | **HYG Jan 15 2027 $72 put**, 2 contracts | Asymmetric hedge | ≤C$100 (≤US$70) | ≤2% | Now, limit ≤ $0.35 |
| — | Residual USD cash + conversion cost | — | ~C$55 | ~1% | — |
| — | Tactical sleeve | Tactical | C$0 today | 0% | Funded from #2 on trigger only |
| | **Total** | | **C$5,000** | 100% | |

Four instruments. The 12-month hedge cap is US$150 (about C$215, 4.3%), drawn from #2.

### Why this shape (one paragraph)

The long end is in a real-yield shock, not an inflation-expectation shock: of the 10Y's
+85 bp in Q3, about 73 bp was real yield and about 12 bp breakeven (Treasury curves,
Sep 30). The Fed hiked on Sep 16 and markets price more. Rates volatility (MOVE ~102–107) is
far above equity volatility (VIX ~16–17). Leadership is narrow, and equal-weight and small
caps sit below their 50-day averages. In that regime, the two highest-value things a small
account can hold are (a) broad equity bought patiently and (b) cash that earns ~4% while the
duration, gold and tactical setups prove themselves. Buying TLT, gold or energy today means
buying a downtrend or a geopolitical spike before its evidence turns. Waiting costs little
when bills pay 4.2%.

---

## 2. Account and implementation assumptions

| Item | Assumption | Basis |
|---|---|---|
| Base currency | **CAD.** All allocations are CAD unless marked US$. | Owner is Canadian (Questrade). |
| USD/CAD | **1.4244** (Oct 1 intraday); BoC daily average 1.4188 (Sep 29). | Trading Economics; Bank of Canada |
| Account | **TFSA** at Questrade. | A LIRA cannot accept new contributions — only transfers from pension or locked-in plans (Questrade LIRA page). The existing LIRA is therefore not where new money goes. |
| RRSP alternative | Better for US-listed ETFs if Dustin has room and a meaningful bracket: the Canada–US treaty exempts RRSPs from the 15% US withholding on US-listed ETF distributions; TFSAs are not exempt. Owner's call. | Questrade; StockScreener.ca |
| Options permissions | Registered accounts max out at **Level 2**: long calls/puts, covered calls, cash-secured puts. **Vertical spreads are margin-only.** So every option here is a single long contract. | Questrade options levels and strategies pages |
| Commissions | $0 on CA/US stocks and ETFs; $0 per US equity-option contract (C$0.99 Canadian options). Exercise fee $24.95: **never exercise — sell to close.** | Questrade pricing page, retrieved Oct 1 |
| FX conversion | Questrade charges **1.5%** (C$34.50 on C$2,300). Use **Norbert's Gambit** (buy DLR, journal to DLR.U, sell) instead: journal fee reportedly C$9.95 (third-party source; confirm on Questrade) plus a few cents of spread. Set currency settlement to "currency of transaction" first. Takes 1–3 business days. | Questrade; canadaflorida.com |
| US withholding in TFSA | Up to 15% of US-listed ETF distributions, not recoverable. On SGOV (~4% yield) that is at most ~0.6%/yr. Some Treasury-interest distributions may qualify for exemption; whether Questrade applies it is **unverified**. | CIC News; StockScreener.ca |
| TFSA trading frequency | Frequent short-term trading in a TFSA can draw CRA "carrying on a business" scrutiny. Irrelevant at one or two tactical trades a quarter; it is a reason the tactical sleeve stays small and slow. | General Canadian tax rule; not legal advice |
| Contract size | One HYG option covers 100 shares (~US$7,665 notional at 76.65). Two OTM puts ≈ 3× the account's notional, but protection only starts below $72. | — |

---

## 3. Positions

### 3.1 XEQT — strategic core

| Field | Detail |
|---|---|
| Instrument | XEQT (TSX), CAD. Equivalent alternative: VEQT. |
| Role | Strategic — the durable, compounding component. |
| Allocation | C$2,700 (54%). |
| Thesis | Over 25 years the reliable return source is owning global corporate earnings broadly. One CAD-listed ticket holds US, Canadian, international and emerging-market equity (roughly 45/25/25/5 — verify on the issuer page), needs no FX conversion, and survives bear markets through breadth rather than through being right about winners. It already carries energy, materials and banks through its Canadian weight, so energy exposure does not need a separate strategic slot. |
| Valuation context (OBSERVED) | S&P 500 forward P/E 19.2 vs 5-yr average 19.8 (FactSet, Sep 25); index ~2% below its Aug 13 record (Sep 30). 10Y real yield 2.93% (Sep 30) — near its highest since the mid-2000s (long history not retrieved), a headwind to multiples. RSP and IWM ~4–5% below their 50-day averages while QQQ is ~3% above (approx., computed Sep 30). |
| Interpretation → action bridge | Index valuation is not extreme, so there is no reason to withhold strategic capital. But breadth is weak and real yields are still rising, so the entry is staged over the next FOMC (Oct 27–28) instead of all at once. |
| Entry | Three tranches of C$900 in whole units: **T1 Oct 2** (next session), **T2 Nov 2** (after FOMC), **T3 Dec 1**. **Accelerator:** if XEQT closes ≥8% below the T1 fill, buy all remaining tranches at the next open. |
| Horizon | To age 65 (~25 years). |
| Invalidation | No price-based invalidation — a bear market is not invalidation. Structural only: a fee or mandate change that makes an equivalent (VEQT) clearly better, or an owner decision to change long-term strategy. |
| Risk control | Sizing and breadth. No leverage, no stop. Accept that a 2008-style drawdown (−35% to −50%) would take C$2,700 to roughly C$1,350–1,750 at the trough. |
| Exit / rebalance | Hold. Reinvest distributions. Review each October. Rebalance through new contributions, not sales. If the hedge (§3.3) pays out during a drawdown, its proceeds buy XEQT. |
| Key risks | Global equity bear driven by a rates shock; CAD strength (XEQT is ~75% unhedged foreign exposure); home-bias overlap with Dustin's own income, which comes from a rate- and housing-sensitive Canadian industry — one reason not to add more Canadian cyclicals on top. |

### 3.2 SGOV — dry powder that earns

| Field | Detail |
|---|---|
| Instrument | SGOV (NYSE), USD. Equivalent: USFR (floating-rate Treasuries; resets weekly). |
| Role | Defensive / dry powder. |
| Allocation | ~US$1,506 (15 units at ~$100.40, Oct 1) ≈ C$2,145 (~43%). |
| Thesis (OBSERVED) | US 3M bill 4.20% vs Canada 3M bill 2.39% (Sep 30). SGOV duration 0.11 yr; SEC yield 3.67% (Sep 29, lagging the bill repricing). The Fed hiked to 3.75–4.00% on Sep 16 and markets price more, so bill yields reset upward quickly. |
| Interpretation → action bridge | Every watchlist setup that could draw this cash (IEF/TLT, GLD, HYG puts, US tactical names) is USD-denominated. Holding the waiting money in USD bills earns ~1.8 pp more than CAD cash and avoids a second conversion later, at the cost of USD/CAD exposure. Zero duration means no exposure to the long-end selloff while it is unresolved. |
| Entry | Now: Norbert's Gambit on C$2,300 → ~US$1,600 net; buy 15 SGOV; keep ~US$25 cash; ~US$70 goes to §3.3. |
| Horizon | Until a trigger fires; formal review **Apr 1, 2027** (see §4). |
| Invalidation | None in the price sense. Switch to USFR if bills and floaters diverge materially. |
| Risk control | The draw rules in §4 are the risk control. |
| Exit / rebalance | Draw only per §4. |
| Key risks | CAD rally (a 5% CAD gain costs ~C$107 on this sleeve); TFSA withholding drag (≤~0.6%/yr); opportunity cost if equities run while cash waits — capped by the Apr 1 time rule. |

### 3.3 HYG put — credit-dislocation hedge (the retail-sized Ackman lesson)

| Field | Detail |
|---|---|
| Instrument | **HYG Jan 15 2027 $72 put**, 2 contracts. If mid > $0.35, use the $71 strike; if that is also above $0.35, **skip** and log the reason. Fallback expiry Feb 19 2027 under the same US$70 cap. |
| Role | Asymmetric-risk budget — a convex hedge, not a directional trade. |
| Allocation | ≤US$70 premium (≤C$100, 2.0%). 12-month cap US$150. |
| Thesis (OBSERVED) | HY OAS 3.12% (Sep 30), up from 2.73% on Sep 23; 1-yr low 2.80%. HYG $76.65 (Oct 1), at its 52-week low. HYG 30-day IV 6.9%, IV rank 26 (Sep 29) — protection is cheap relative to its own history. Private-credit stress: Metrics Credit Partners froze some redemptions (Sep 30); Apollo capped fund withdrawals for a third quarter (Sep 22, headline). SSGA (July) put HY defaults near 4.0% vs a 2.9% 20-yr median, with the CCC–B gap >600 bp. Real 10Y 2.93% raises refinancing costs for weak borrowers. |
| Interpretation | The Ackman lesson is not the instrument (CDX, swaptions) but the timing: buy protection while it is cheap and spreads are tight, not after the shock. HYG puts are the liquid retail analogue, and they also gain from a rates shock (HYG duration ~3 yr). |
| EV honesty | Standalone EV is probably **negative**, like most insurance. Rough check: model price ~$0.15–0.50 depending on skew (Black-Scholes, IV 8–12%, HYG distributions included). HYG → $68 (−11%, a smaller fall than in March 2020) pays $4/share = US$800 on two contracts (~11× at $0.35). The justification is portfolio-level: the payoff arrives exactly when the watchlist triggers fire and XEQT is down, and it converts into cash to buy at distressed prices. If ChatGPT or Dustin rejects portfolio-level insurance at this account size, this position goes to zero and the cash stays in SGOV. |
| Entry | Now, limit order at ≤ $0.35. Never pay the ask on a wide market. |
| Horizon | ≤ ~3.5 months. |
| Invalidation | Not applicable — the loss is defined at purchase. |
| Risk control | **Maximum loss = premium paid (US$70).** Containment is sizing: this sleeve is designed to lose 100% in the base case, so it is sized at 2%. Never add to a losing hedge. **Time stop:** sell whatever is left at ≤30 days to expiry (by Dec 16), no automatic roll. |
| Exit / take profit | HY OAS ≥ 4.0% **or** put value ≥ 3× cost → sell half. HY OAS ≥ 5.0% **or** ≥ 5× cost → sell the rest. Proceeds go to XEQT first (accelerator), then to the rates ladder if its triggers are live. |
| Renewal | Only if, at expiry: HYG IV rank < 50 **and** at least two early-warning signs persist (HY OAS > 3.0%; new private-credit gating; MOVE > 100; a weak long-end auction). Within the US$150 / 12-month cap. |
| Key risks | Spreads stay tight (the most likely outcome — premium lost); a shock arrives after Jan 15; wide bid-ask on OTM strikes. |

### 3.4 Tactical sleeve — deliberately empty today

No setup clears the bar for capital today. The candidates (power/electrification, semis,
energy, gold) are in `WATCHLIST.md` with triggers. When one fires, it is funded from SGOV
under §4 and must be written up first in this template:

| Field | Requirement |
|---|---|
| Thesis | One sentence, with the OBSERVED evidence and date. |
| Entry / confirmation | The specific price or data event; no entry on anticipation. |
| Size | **Risk ≤ C$100 (2% of capital) per trade.** Shares = C$100 ÷ stop distance. Max one open tactical position (two only if the first is at break-even stop). |
| Holding period | Stated in advance (days / weeks / months). |
| Invalidation | The level or fact that proves the thesis wrong. |
| Protective exit | Stop order placed with the entry. For long calls (no spreads in TFSA): premium ≤ C$150; exit at −50% of premium or when 50% of time to expiry has elapsed, whichever comes first. This is the mechanical rule that prevents a 60–100% drift. |
| Maximum acceptable loss | C$100 stock, C$75 options (−50% of ≤C$150). |
| Profit taking | Sell half at 2R; trail the rest under the 20-day average or prior swing low. |
| Paper-trade rule | Only when the setup is A-quality and the genuine question is real capital versus no capital. |

---

## 4. Unallocated-capital rule

1. **"Wait" is a position.** The default state of the SGOV sleeve is undeployed, earning bill yield.
2. **Earmarks (caps, first-trigger-first-served):**
   - Rates ladder (IEF, then TLT): ≤ US$800 total.
   - Gold (GLD, or CGL.C on the CAD side): ≤ US$350.
   - Tactical: one position, risk ≤ C$100, notional ≤ US$500.
   - Hedge: ≤ US$150 per 12 months.
   - **Floor:** keep ≥ US$250 in SGOV for hedge renewals and settlement.
3. **A trigger counts only if** it is logged (date, evidence, source) in `ROUNDS.md` or `WATCHLIST.md` before the order is placed.
4. **No averaging down** a tactical position with dry powder.
5. **Time rule:** on **Apr 1, 2027**, if under 25% of the SGOV sleeve is deployed and no trigger is pending, move half of the undeployed balance into strategic equity via **VT** (US-listed global equity, avoiding a round-trip FX conversion). The other half stays as dry powder.
6. **Drawdown rule:** if XEQT falls ≥ 15% from the T1 fill and the strategic tranches are complete, up to US$400 of SGOV may be added to strategic equity (VT) — strategic buying in a drawdown is the main use of dry powder, not a failure of it.

---

## 5. What would change this proposal

- **Fed-peak evidence** (2Y yield rolling over, no further hikes priced): opens Stage A of the rates ladder (IEF).
- **Term-premium relief** (MOVE back below ~90, clean long-end auctions): opens Stage B (TLT).
- **Inflation regime** (10Y breakeven > 2.6% with core accelerating): keep duration closed; TIPS before nominals; reconsider the energy watch.
- **Credit shock** (HY OAS ≥ 4%): hedge pays; accelerator buys XEQT; reassess TLT (flight to quality may arrive before Fed-peak evidence).
- **Peace deal / oil risk-premium collapse:** no portfolio change (no energy position); the energy watch re-sets.

Sources and observation dates for every figure are in `ROUNDS.md` (Round 1 — Claude).
