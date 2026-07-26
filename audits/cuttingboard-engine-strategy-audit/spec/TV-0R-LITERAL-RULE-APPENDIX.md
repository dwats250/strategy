# TV-0R Literal Rule Appendix — R-01, R-02, R-05, E-04

Status: `ACTIVE NARROW IMPLEMENTATION CLARIFICATION`

Created: 2026-07-26

Authorized by:
[`../adjudications/TV-0R-DUSTIN-ADJUDICATION.md`](../adjudications/TV-0R-DUSTIN-ADJUDICATION.md)
finding F-2, adjudicated by Dustin.

## Scope and standing

This appendix **supplements
[`GATE_TRANSLATION_MATRIX.md`](GATE_TRANSLATION_MATRIX.md) for exactly four gates —
R-01, R-02, R-05, and E-04** — by supplying the implementation literals the frozen
matrix omitted. It exists so TV-1 can implement those gates without inventing policy.

It **does not** redefine, extend, narrow, or reinterpret any other gate, row,
classification, variant, threshold, or safeguard. Every other matrix row is untouched
and governs as frozen. Where this appendix is silent, the frozen matrix governs.

Every statement below is a transcription of pinned source. **Nothing here is a design
choice.** No threshold, list member, fallback, default, proxy, or interpretation has
been added. Where the pinned source produces a result that looks surprising, it is
recorded as found and flagged as an observation — never corrected, normalized, or
smoothed.

## Source pin and citation form

- Repository: `dwats250/cuttingboard`
- Commit: `59f8279d796335149afdec4aa507b6f927233518`
- Commit date: `2026-07-26T01:35:59Z`
- Mutation permission: **NONE**

Every literal below carries a citation in this form:

> `path` L*start*–*end* — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L84-L123)

Each blob link is pinned to the commit SHA, not to a branch, so it resolves to the
exact reviewed bytes permanently. An implementer must be able to open every link and
read the literal without inference. Read pinned evidence only at this commit — never
from a local CuttingBoard working tree. See `docs/conventions.md` §i.

---

## Shared universe constants

Referenced by R-01. All from `cuttingboard/config.py`.

| Constant | Value | Citation |
|---|---|---|
| `MACRO_DRIVERS` | `["^VIX", "DX-Y.NYB", "^TNX", "BTC-USD", "CL=F", "GC=F", "SI=F"]` | `cuttingboard/config.py` L198 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L198) |
| `NON_TRADABLE_SYMBOLS` | `frozenset(MACRO_DRIVERS)` | `cuttingboard/config.py` L199 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L199) |
| `INDICES` | `["SPY", "QQQ", "IWM"]` | `cuttingboard/config.py` L200 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L200) |
| `COMMODITIES` | `["GLD", "SLV", "GDX", "PAAS", "USO", "XLE"]` | `cuttingboard/config.py` L201 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L201) |
| `HIGH_BETA` | `["NVDA", "TSLA", "AAPL", "META", "AMZN", "COIN", "MSTR"]` | `cuttingboard/config.py` L202 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L202) |
| `ALL_SYMBOLS` | `MACRO_DRIVERS + INDICES + COMMODITIES + HIGH_BETA` | `cuttingboard/config.py` L204 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L204) |

---

## R-01 — `regime.detect_expansion_regime`

Function body: `cuttingboard/regime.py` L84–123 —
[blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L84-L123)

Input is `valid_quotes: dict[str, NormalizedQuote]`. Quote fields used are
`pct_change_decimal` (a decimal fraction, not percentage points) and `price`.

All four conditions must hold. Any failure returns `False` immediately.

### Symbol lookups

Keys are looked up as `"SPY"`, `"QQQ"`, `"^VIX"`.

> `cuttingboard/regime.py` L93–95 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L93-L95)

### Condition 1 — index alignment

`False` if `spy is None or qqq is None`; `False` if
`spy.pct_change_decimal <= 0 or qqq.pct_change_decimal <= 0`. Both must therefore be
**strictly greater than 0**.

> `cuttingboard/regime.py` L98–101 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L98-L101)

### Condition 2 — VIX confirmation

`False` if `vix is None or vix.pct_change_decimal > EXPANSION_VIX_PCT_THRESHOLD`.
Passing therefore requires `vix.pct_change_decimal <= -0.01`.

> `cuttingboard/regime.py` L104–105 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L104-L105)
> `EXPANSION_VIX_PCT_THRESHOLD = -0.01` — `cuttingboard/config.py` L144 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L144)

### Condition 3 — breadth

```
advancing = count of (s, q) in valid_quotes
            where s not in NON_TRADABLE_SYMBOLS and q.pct_change_decimal > 0
total     = count of s in ALL_SYMBOLS where s not in NON_TRADABLE_SYMBOLS
False if total == 0 or (advancing / total) < EXPANSION_MIN_BREADTH
```

The denominator is the **configured** tradable universe, not the symbols that
reported. A symbol absent from `valid_quotes` therefore counts as not advancing.

> `cuttingboard/regime.py` L110–116 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L110-L116)
> `EXPANSION_MIN_BREADTH = 0.70` — `cuttingboard/config.py` L143 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L143)

Resolving the constants above, the tradable denominator is these **16** symbols:

`SPY, QQQ, IWM, GLD, SLV, GDX, PAAS, USO, XLE, NVDA, TSLA, AAPL, META, AMZN, COIN, MSTR`

### Condition 4 — leadership

```
leading = count of s in EXPANSION_LEADERSHIP_SYMBOLS
          where s in valid_quotes and valid_quotes[s].pct_change_decimal >= EXPANSION_LEADERSHIP_MIN_PCT
return leading >= EXPANSION_LEADERSHIP_MIN_COUNT
```

> `cuttingboard/regime.py` L119–123 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L119-L123)

| Constant | Value | Citation |
|---|---|---|
| `EXPANSION_LEADERSHIP_SYMBOLS` | `["NVDA", "COIN", "MSTR", "SMCI", "TSLA"]` | `cuttingboard/config.py` L142 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L142) |
| `EXPANSION_LEADERSHIP_MIN_PCT` | `0.015` | `cuttingboard/config.py` L145 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L145) |
| `EXPANSION_LEADERSHIP_MIN_COUNT` | `2` | `cuttingboard/config.py` L146 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L146) |

### Observations recorded as found

1. **Breadth threshold is a strict `<` on the ratio.** With a denominator of 16,
   `advancing / 16 >= 0.70` requires `advancing >= 11.2`, i.e. **at least 12 advancing
   symbols**. Eleven advancing symbols (`0.6875`) fails.
2. **`SMCI` appears in `EXPANSION_LEADERSHIP_SYMBOLS` but not in `ALL_SYMBOLS`.** It is
   absent from `MACRO_DRIVERS`, `INDICES`, `COMMODITIES`, and `HIGH_BETA`, so it cannot
   be present in `valid_quotes` on this path, and the effective leadership pool is the
   four symbols `NVDA, COIN, MSTR, TSLA`. Recorded as observed at the pinned SHA. TV-1
   must reproduce the configured list verbatim, including `SMCI`, and must not
   substitute, drop, or supplement it.

Both items are transcriptions and arithmetic on the cited literals. Neither changes a
rule, and neither is a proposed correction to CuttingBoard.

---

## R-02 — `regime.compute_regime` vote model and aggregation

Function body: `cuttingboard/regime.py` L126–230 —
[blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L126-L230)

### EXPANSION short-circuit precedes the vote model

`detect_expansion_regime` is evaluated first. When it returns `True`, `compute_regime`
returns immediately with `regime=EXPANSION`, `posture=EXPANSION_LONG`,
`confidence=1.0`, `net_score=0`, `risk_on_votes=0`, `risk_off_votes=0`,
`neutral_votes=0`, `total_votes=0`, `vote_breakdown={}`. **The eight-vote model never
runs on the EXPANSION path**, and the posture function is never called.

> `cuttingboard/regime.py` L142–157 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L142-L157)

### Symbol lookups

`^VIX` (L138); `SPY`, `QQQ`, `IWM`, `DX-Y.NYB`, `^TNX`, `BTC-USD` (L159–164).
`vix_level` is `vix.price`; `vix_pct` is `vix.pct_change_decimal`.

> `cuttingboard/regime.py` L138–140 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L138-L140)
> `cuttingboard/regime.py` L159–164 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L159-L164)

### The eight vote cutoffs

Declared in this order. Order is load-bearing only for `vote_breakdown` key order.

> `cuttingboard/regime.py` L167–176 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L167-L176)

| # | Vote key | Symbol | Field | Helper | RISK_ON when | RISK_OFF when |
|---|---|---|---|---|---|---|
| 1 | `SPY pct_change` | `SPY` | `pct_change_decimal` | `_vote_pct_up` | `> 0.003` | `< -0.003` |
| 2 | `QQQ pct_change` | `QQQ` | `pct_change_decimal` | `_vote_pct_up` | `> 0.003` | `< -0.003` |
| 3 | `IWM pct_change` | `IWM` | `pct_change_decimal` | `_vote_pct_up` | `> 0.004` | `< -0.004` |
| 4 | `VIX level` | `^VIX` | `price` | `_vote_lvl_low` | `< 18` | `> 25` |
| 5 | `VIX pct_change` | `^VIX` | `pct_change_decimal` | `_vote_pct_low` | `< -0.03` | `> 0.05` |
| 6 | `DXY pct_change` | `DX-Y.NYB` | `pct_change_decimal` | `_vote_pct_low` | `< -0.002` | `> 0.003` |
| 7 | `TNX pct_change` | `^TNX` | `pct_change_decimal` | `_vote_pct_low` | `< -0.005` | `> 0.008` |
| 8 | `BTC pct_change` | `BTC-USD` | `pct_change_decimal` | `_vote_pct_up` | `> 0.015` | `< -0.020` |

**All six comparisons are strict.** Anything not satisfying either bound is `NEUTRAL`.
The cutoffs are exclusive bounds, so a value exactly equal to a cutoff votes `NEUTRAL`.

| Helper | Semantics | Citation |
|---|---|---|
| `_vote_pct_up` | `None` if quote is None; `p > risk_on_gt` → RISK_ON; `p < risk_off_lt` → RISK_OFF; else NEUTRAL | `cuttingboard/regime.py` L247–260 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L247-L260) |
| `_vote_pct_low` | `None` if quote is None; `p < risk_on_lt` → RISK_ON; `p > risk_off_gt` → RISK_OFF; else NEUTRAL | `cuttingboard/regime.py` L263–276 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L263-L276) |
| `_vote_lvl_low` | `None` if quote is None; `lvl < risk_on_lt` → RISK_ON; `lvl > risk_off_gt` → RISK_OFF; else NEUTRAL | `cuttingboard/regime.py` L279–292 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L279-L292) |

### Missing votes

A vote of `None` (symbol absent from `valid_quotes`) is logged and **skipped** — it
does not enter `vote_breakdown` and increments no counter.

> `cuttingboard/regime.py` L181–191 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L181-L191)

### Aggregation

```
total_votes = risk_on_votes + risk_off_votes + neutral_votes
net_score   = risk_on_votes - risk_off_votes
missing     = 8 - total_votes
bounded_net = max(0, net_score - missing)   if net_score > 0
              min(0, net_score + missing)   otherwise
confidence  = abs(bounded_net) / 8
```

The denominator is the structural **eight-vote** count (`len(raw_votes)`), not
`total_votes`. Bounding is clamped at zero so it never crosses sign. Note the
`net_score > 0` test: a `net_score` of exactly `0` takes the second branch.

> `cuttingboard/regime.py` L193–206 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L193-L206)

`_classify_regime` and `_determine_posture` are called with **`bounded_net`** and the
bounded `confidence` — never with the raw `net_score`. The returned `RegimeState`
nevertheless reports the **raw** `net_score`, not the bounded value.

> `cuttingboard/regime.py` L208–209 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L208-L209)
> `cuttingboard/regime.py` L217–230 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L217-L230)

### Classification outcome consumed by the aggregation

Reproduced here because R-02's aggregation output is meaningless without the function
that consumes it. These literals **already appear in the frozen matrix as rows R-03
and R-04**; nothing about those rows is changed, widened, or reinterpreted.

```
if vix_pct is not None and vix_pct > VIX_CHAOTIC_SPIKE:  return CHAOTIC
if bounded_net >=  4 and confidence >= 0.60:             return RISK_ON
if bounded_net >=  2:                                    return RISK_ON
if bounded_net <= -4 and confidence >= 0.60:             return RISK_OFF
if bounded_net <= -2:                                    return RISK_OFF
return NEUTRAL
```

`vix_pct` here is the **raw** `^VIX` `pct_change_decimal`, unaffected by bounding.

> `cuttingboard/regime.py` L299–316 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L299-L316)
> `VIX_CHAOTIC_SPIKE = 0.15` — `cuttingboard/config.py` L113 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L113)

---

## R-05 — `regime._determine_posture`

Function body: `cuttingboard/regime.py` L319–347 —
[blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L319-L347)

Called as `_determine_posture(regime, confidence, vix_level)` where `confidence` is
the bounded confidence and `vix_level` is the raw `^VIX` `price`.

### Evaluation order — literal

```
1. if regime == CHAOTIC or confidence < MIN_REGIME_CONFIDENCE:  STAY_FLAT
2. if regime == RISK_ON:
       confidence >= 0.75   ->  AGGRESSIVE_LONG
       confidence >= 0.55   ->  CONTROLLED_LONG
       otherwise            ->  STAY_FLAT
3. if regime == RISK_OFF:
       confidence >= 0.55   ->  DEFENSIVE_SHORT
       otherwise            ->  STAY_FLAT
4. if regime in (NEUTRAL, TRANSITION):
       vix_level is not None and vix_level >  25  ->  STAY_FLAT
       vix_level is not None and vix_level >= 18  ->  NEUTRAL_PREMIUM
       otherwise                                  ->  STAY_FLAT
5. STAY_FLAT
```

| Literal | Value | Citation |
|---|---|---|
| `MIN_REGIME_CONFIDENCE` | `0.50` | `cuttingboard/config.py` L62 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L62) |
| Global floor | `regime == CHAOTIC or confidence < 0.50` → `STAY_FLAT` | `cuttingboard/regime.py` L325–326 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L325-L326) |
| RISK_ON branch | `>= 0.75` AGGRESSIVE_LONG; `>= 0.55` CONTROLLED_LONG; else STAY_FLAT | `cuttingboard/regime.py` L328–333 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L328-L333) |
| RISK_OFF branch | `>= 0.55` DEFENSIVE_SHORT; else STAY_FLAT | `cuttingboard/regime.py` L335–338 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L335-L338) |
| NEUTRAL / TRANSITION branch | VIX `> 25` STAY_FLAT; VIX `>= 18` NEUTRAL_PREMIUM; else STAY_FLAT | `cuttingboard/regime.py` L340–345 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L340-L345) |
| Fallthrough | `STAY_FLAT` | `cuttingboard/regime.py` L347 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/regime.py#L347) |

Missing `^VIX` (`vix_level is None`) in the NEUTRAL branch falls through both tests to
`STAY_FLAT`. `EXPANSION` never reaches this function — its posture is assigned
directly at `regime.py` L149.

Threshold operators: `>= 0.75`, `>= 0.55`, `>= 18` are inclusive; `< 0.50` and `> 25`
are strict.

### Derived from the cited literals — arithmetic only, no new rule

Because `confidence = abs(bounded_net) / 8` and `bounded_net` is an integer, the only
attainable confidence values on the computed branch are:

`0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0`

Therefore, on the computed branch:

- `confidence >= 0.50` ⟺ `abs(bounded_net) >= 4`
- `confidence >= 0.55` ⟺ `confidence >= 0.625` ⟺ `abs(bounded_net) >= 5`
- `confidence >= 0.60` ⟺ `confidence >= 0.625` ⟺ `abs(bounded_net) >= 5`
- `confidence >= 0.75` ⟺ `abs(bounded_net) >= 6`

The `0.50 <= confidence < 0.55` comments at `regime.py` L333 and L338 describe an
interval that the computed branch cannot land in.

This subsection states no threshold of its own. It is arithmetic over cited literals,
supplied so TV-1 implements the comparisons exactly rather than approximating them.
It does **not** adjudicate semantic hypothesis 1 in
[`GATE_TRANSLATION_MATRIX.md`](GATE_TRANSLATION_MATRIX.md) — confirming, narrowing, or
falsifying that hypothesis remains TV-2's task under the frozen contract.

---

## E-04 — macro pressure and its conflict-only execution effect

E-04 spans three modules. All are cited.

### Driver → symbol mapping and field construction

| Driver | Symbol | Citation |
|---|---|---|
| `volatility` | `^VIX` | `cuttingboard/contract.py` L49–53 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/contract.py#L49-L53) |
| `dollar` | `DX-Y.NYB` | same |
| `rates` | `^TNX` | same |
| `bitcoin` | `BTC-USD` | same |

`oil`, `gold`, and `silver` are also mapped but are visibility-only and are excluded
from pressure synthesis.

> `cuttingboard/contract.py` L54–64 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/contract.py#L54-L64)
> `cuttingboard/macro_pressure.py` L14–23 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L14-L23)

Field construction in `_build_macro_drivers`:

```
change_pct = pct_change_decimal * 100.0
change_bps = pct_change_decimal * price * 100.0     # rates driver only
```

> `cuttingboard/contract.py` L527–559 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/contract.py#L527-L559)

**Unit consequence, recorded as found:** `change_pct` is expressed in **percentage
points**, not as a decimal fraction. A −1% VIX move yields `change_pct == -1.0`, not
`-0.01`. The component cutoffs below are therefore in percentage points. TV-1 must
reproduce the units exactly as pinned; it must not rescale, normalize, or "correct"
them.

### Component field selection

| Driver | Field compared |
|---|---|
| `volatility` | `change_pct` |
| `dollar` | `change_pct` |
| `rates` | `change_bps` |
| `bitcoin` | `change_pct` |

> `cuttingboard/macro_pressure.py` L25–30 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L25-L30)

### Component cutoffs — `_classify_driver`

A missing driver block, or a block whose field is absent or `None`, yields `UNKNOWN`.
Non-numeric, boolean, or non-finite values raise.

> `cuttingboard/macro_pressure.py` L47–90 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L47-L90)

| Driver | RISK_ON | RISK_OFF | else | Citation |
|---|---|---|---|---|
| `volatility` | `value <= -0.01` | `value >= 0.01` | NEUTRAL | `cuttingboard/macro_pressure.py` L66–71 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L66-L71) |
| `dollar` | `value <= -0.0025` | `value >= 0.0025` | NEUTRAL | `cuttingboard/macro_pressure.py` L72–77 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L72-L77) |
| `rates` | `value <= -3.0` | `value >= 3.0` | NEUTRAL | `cuttingboard/macro_pressure.py` L78–83 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L78-L83) |
| `bitcoin` | `value >= 0.01` | `value <= -0.01` | NEUTRAL | `cuttingboard/macro_pressure.py` L84–89 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L84-L89) |

All four use **inclusive** comparisons, and `bitcoin`'s direction is inverted relative
to `volatility`, `dollar`, and `rates`.

Allowed enums: components `{RISK_ON, RISK_OFF, NEUTRAL, UNKNOWN}`; overall
`{RISK_ON, RISK_OFF, MIXED, NEUTRAL, UNKNOWN}`.

> `cuttingboard/macro_pressure.py` L32–33 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L32-L33)

### Aggregation — `_overall_pressure`

Evaluated in this order over the **known** (non-`UNKNOWN`) components only:

```
known = [c for c in components if c != UNKNOWN]
if not known:                                   return UNKNOWN
if risk_on_count >= 2 and risk_off_count == 0:  return RISK_ON
if risk_off_count >= 2 and risk_on_count == 0:  return RISK_OFF
if risk_on_count >= 1 and risk_off_count >= 1:  return MIXED
if all(c == NEUTRAL for c in known):            return NEUTRAL
return MIXED
```

Order matters: a single `RISK_ON` with no opposing component and no second agreeing
component falls through every branch to the terminal `MIXED`.

> `cuttingboard/macro_pressure.py` L93–109 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L93-L109)
> `build_macro_pressure` — `cuttingboard/macro_pressure.py` L112–136 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/macro_pressure.py#L112-L136)

### Conflict-only behavior — `_apply_macro_pressure`

```
UNKNOWN | NEUTRAL  ->  allow,  size unchanged
MIXED              ->  allow,  size * 0.75
RISK_OFF           ->  direction == LONG   ->  BLOCK "macro_pressure_conflict", size 0.0
                       otherwise           ->  allow, size * 0.5
RISK_ON            ->  direction == SHORT  ->  BLOCK "macro_pressure_conflict", size 0.0
                       otherwise           ->  allow, size * 0.5
```

Pressure **blocks only on direct directional conflict**. In every other case it
adjusts the size multiplier and allows the trade.

> `cuttingboard/execution_policy.py` L239–251 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/execution_policy.py#L239-L251)
> `POLICY_MACRO_PRESSURE_CONFLICT = "macro_pressure_conflict"` — `cuttingboard/execution_policy.py` L32 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/execution_policy.py#L32)

### Directly coupled execution constraints

`_apply_macro_pressure` is reached **only** as the final step of
`evaluate_execution_policy`. Every constraint below short-circuits before pressure is
ever consulted, in this exact order. Stating E-04's behavior faithfully requires them,
because pressure can only alter an outcome that has already survived all of them.

| Order | Condition | Result |
|---|---|---|
| 0 | `overall_pressure` not in `{RISK_ON, RISK_OFF, MIXED, NEUTRAL, UNKNOWN}` | raises `ValueError` |
| 1 | `decision.status != ALLOW_TRADE` | block, `pre_policy_block` |
| 2 | `confidence < 0.60` | block, `low_confidence` |
| 3 | `market_regime == "CHAOTIC"` | block, `chaotic_regime` |
| 4 | `posture == "STAY_FLAT"` | block, `stay_flat` |
| 5 | `prior_trade_count >= EXECUTION_POLICY_MAX_TRADES_PER_DAY` (`2`) | block, `session_trade_limit` |
| 6 | `consecutive_losses >= 2` | block, `loss_lockout` |
| 7 | cooldown active (`EXECUTION_POLICY_COOLDOWN_MINUTES` = `15`) | block, `cooldown` |
| 8 | ORB constraint returns `orb_inside_range` | block, `orb_inside_range` |
| 9 | ORB returns `orb_unavailable` | **not** a block — carried as `base_reason` |
| 10 | `_apply_macro_pressure(direction, overall_pressure, size, base_reason)` | as tabulated above |

> `cuttingboard/execution_policy.py` L202–236 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/execution_policy.py#L202-L236)
> `_VALID_PRESSURE_VALUES` — `cuttingboard/execution_policy.py` L34 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/execution_policy.py#L34)
> `_evaluate_orb_constraint` — `cuttingboard/execution_policy.py` L254–273 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/execution_policy.py#L254-L273)
> `EXECUTION_POLICY_MAX_TRADES_PER_DAY = 2`, `EXECUTION_POLICY_COOLDOWN_MINUTES = 15` — `cuttingboard/config.py` L118–119 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L118-L119)

The `size` that pressure scales comes from `size_multiplier_for_confidence`:

```
confidence < 0.60   ->  0.0
confidence >= 0.80  ->  1.0
confidence >= 0.70  ->  0.75
otherwise           ->  0.50
```

> `cuttingboard/execution_policy.py` L59–68 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/execution_policy.py#L59-L68)

### Boundary reminder for TV-1

Constraints 2 and 5–9 above correspond to matrix rows E-01, E-02, and E-03, which the
frozen matrix classifies `EXCLUDED_OPERATIONAL`. **Those classifications are
unchanged.** They are documented here solely so TV-1 can state E-04's reachability
honestly. Documenting a constraint is not authorization to implement it, and an
excluded gate is never treated as passing — see `docs/conventions.md` §h.

---

## What this appendix does not do

- It changes no gate classification, threshold, variant, safeguard, or review rule.
- It adds no threshold, list member, fallback, default, proxy, or interpretation that
  the pinned source does not contain.
- It proposes no CuttingBoard change. Observations recorded as found are evidence
  only, and no finding here authorizes an engine change.
- It authorizes no implementation. TV-1 remains blocked per
  [`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md).
