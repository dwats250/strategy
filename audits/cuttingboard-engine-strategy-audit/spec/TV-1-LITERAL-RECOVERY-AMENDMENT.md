# TV-1 Literal Recovery Amendment — S-02, S-03/S-04, D-02

Status: `ACTIVE NARROW IMPLEMENTATION CLARIFICATION`

Created: 2026-07-26

Authorized by: **Dustin Watson**, directly, on 2026-07-26, following the completed
source-pin evidence recovery for the TV-1 literal gaps. Unlike the two TV-0R amendments,
this one has no separate adjudication-record document; the authorization and its scope are
registered in [`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md) §
*Post-TV-1 literal-recovery effective authority*.

## Scope and standing

This amendment **supplements
[`GATE_TRANSLATION_MATRIX.md`](GATE_TRANSLATION_MATRIX.md) for exactly three gate rows —
S-02, S-03/S-04, and D-02** — by supplying the implementation literals the frozen matrix
omitted. It exists so TV-1's declared interpretations DI-1, DI-2 and DI-3 can be resolved
against pinned source rather than left as unratified choices.

It **does not** redefine, extend, narrow, or reinterpret any other gate, row,
classification, variant, threshold, or safeguard. Every other matrix row is untouched and
governs as frozen. Where this amendment is silent, the frozen matrix governs. It does not
modify, reopen, or overlap
[`TV-0R-LITERAL-RULE-APPENDIX.md`](TV-0R-LITERAL-RULE-APPENDIX.md), whose scope remains
exactly R-01, R-02, R-05 and E-04.

Every statement below is a transcription of pinned source. **Nothing here is a design
choice.** No threshold, denominator, operator, band, default, fallback, or interpretation
has been added. Where the pinned source produces a result that looks surprising, or where
the source disagrees with itself, it is recorded as found — never corrected, normalized,
or smoothed.

**Executable code governs this transcription.** Where a docstring, comment, or field
annotation disagrees with the executable statement it describes, the executable statement
is what is transcribed, and the disagreement is recorded as an observation. One such
disagreement exists and is recorded under D-02 below.

## Source pin and citation form

- Repository: `dwats250/cuttingboard`
- Commit: `59f8279d796335149afdec4aa507b6f927233518`
- Commit date: `2026-07-26T01:35:59Z`
- Mutation permission: **NONE**

Every literal below carries a citation in this form:

> `path` L*start*–*end* — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L146-L213)

Each blob link is pinned to the commit SHA, not to a branch, so it resolves to the exact
reviewed bytes permanently. Read pinned evidence only at this commit — never from a local
CuttingBoard working tree, and never from a branch tip. See `docs/conventions.md` §i.

Blob identities of the three files read, verified byte-exact at the pin:

| File | Git blob SHA |
|---|---|
| `cuttingboard/structure.py` | `a4ab4237fe3074848fd3c28072d752d1415529f4` |
| `cuttingboard/derived.py` | `f631b2e1a1dc4f33b68e9fca6eb23662b50c685e` |
| `cuttingboard/config.py` | `8f19e0587b56e547436fc866ff4002fb4950f9e7` |

### Module disambiguation, recorded as found

The pinned repository contains both `cuttingboard/structure.py` and
`cuttingboard/trend_structure.py`. **`structure.py` is the operative implementation of
S-01 … S-04.** `trend_structure.py` is a sidecar snapshot builder over a curated symbol
tuple; it emits `BULLISH`/`BEARISH`/`MIXED` and `SUPPORTIVE`/`AVOID`/`NEUTRAL` from
SMA50/SMA200/VWAP and never emits `TREND`, `PULLBACK`, `BREAKOUT`, `REVERSAL`, or `CHOP`.
It is not cited by this amendment and carries no authority here.

## Shared constants

All from `cuttingboard/config.py`.

| Constant | Value | Citation |
|---|---|---|
| `EMA_FAST` | `9` | `cuttingboard/config.py` L109 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L109) |
| `EMA_SLOW` | `21` | `cuttingboard/config.py` L110 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L110) |
| `EMA_TREND` | `50` | `cuttingboard/config.py` L111 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L111) |
| `ATR_PERIOD` | `14` | `cuttingboard/config.py` L112 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L112) |
| `OHLCV_MIN_BARS` | `21` | `cuttingboard/config.py` L107 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/config.py#L107) |

The structure-layer thresholds below are declared at module level in `structure.py` and are
**not** in `config.py`.

| Constant | Value | Citation |
|---|---|---|
| `_BREAKOUT_MOMENTUM_MIN` | `0.02` | `cuttingboard/structure.py` L39 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L39) |
| `_BREAKOUT_VOLUME_MIN` | `1.3` | `cuttingboard/structure.py` L40 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L40) |
| `_REVERSAL_SPREAD_MAX` | `0.002` | `cuttingboard/structure.py` L41 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L41) |
| `_REVERSAL_MOMENTUM_MIN` | `0.003` | `cuttingboard/structure.py` L42 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L42) |

---

## S-02 — the EMA9/EMA21 spread: denominator, sign, and threshold

The frozen matrix states S-02 as "absolute EMA9/21 spread `<0.2%` plus absolute five-day
momentum `>0.3%`" without supplying the denominator. The denominator is `ema21`.

### Definition — signed, computed once in the derived-metrics layer

```
ema_spread_pct = (ema9 - ema21) / ema21   if ema21 != 0
                 None                     otherwise
```

> `cuttingboard/derived.py` L106 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L106)
> Field annotation `# (ema9 - ema21) / ema21` — `cuttingboard/derived.py` L34 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L34)

The stored value is **signed**. The `ema21 != 0` guard yields `None`, not a substituted
number.

The three EMAs it is built from are pandas `ewm(span=…, adjust=False)` on close:

> `cuttingboard/derived.py` L100–102 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L100-L102)

### Evaluation — absolute value, strict comparison

The structure layer takes the absolute value at the point of use, and compares strictly:

```
spread = abs(ema_spread_pct) if ema_spread_pct is not None else 0.0
...
if spread < 0.002 and abs(momentum) > 0.003:
    return REVERSAL
```

> `cuttingboard/structure.py` L169 (absolute value and the `0.0` substitution) — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L169)
> `cuttingboard/structure.py` L188–189 (the REVERSAL test) — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L188-L189)

Both comparisons are **strict**: `<` on the spread, `>` on the absolute momentum. A value
exactly equal to either cutoff does not satisfy that leg.

Storage is signed and evaluation is absolute. Both facts are transcribed because an
implementation that exports the field, rather than only testing it, needs the sign.

---

## S-03 / S-04 — structure classification, exact executable order

Function body: `cuttingboard/structure.py` L146–213 —
[blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L146-L213)

Labels are `TREND`, `PULLBACK`, `BREAKOUT`, `REVERSAL`, `CHOP`.

> `cuttingboard/structure.py` L26–30 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L26-L30)

### Strict EMA alignment definitions

```
ema_aligned_bull = ema9 > ema21 > ema50
ema_aligned_bear = ema9 < ema21 < ema50
```

Both are **strict chained comparisons**. Equality at any link satisfies neither.

> `cuttingboard/derived.py` L104–105 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L104-L105)
> Field annotations — `cuttingboard/derived.py` L32–33 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L32-L33)

### Executable branch order, with every operator preserved

Evaluated top to bottom; each `return` exits immediately.

```
1.  if dm is None or not dm.sufficient_history:              return CHOP        # L157-158
2.  if ema9 is None or ema21 is None or ema50 is None:       return CHOP        # L164-165

    momentum  = dm.momentum_5d     if not None else 0.0                         # L167
    vol_ratio = dm.volume_ratio    if not None else 0.0                         # L168
    spread    = abs(dm.ema_spread_pct) if not None else 0.0                     # L169

3.  if momentum >  0.02 and vol_ratio > 1.3 and price > ema9:  return BREAKOUT  # L175-178
    if momentum < -0.02 and vol_ratio > 1.3 and price < ema9:  return BREAKOUT  # L179-182

4.  if spread < 0.002 and abs(momentum) > 0.003:               return REVERSAL  # L188-189

5.  if ema_aligned_bull:                                                        # L192
        if price >= ema9:   return TREND                                        # L193-195
        if price >= ema21:  return PULLBACK                                     # L196-198
        return CHOP                                                             # L199-200

    if ema_aligned_bear:                                                        # L202
        if price <= ema9:   return TREND                                        # L203-205
        if price <= ema21:  return PULLBACK                                     # L206-208
        return CHOP                                                             # L209-210

6.  return CHOP                                                                 # L212-213
```

> `cuttingboard/structure.py` L157–213 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L157-L213)

The docstring at L149–155 states the same five-step priority in prose and agrees with the
executable order.

> `cuttingboard/structure.py` L146–156 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L146-L156)

### Band boundaries and operators — the omitted literals

- **Bull-aligned:** `price >= ema9` → `TREND`; else `price >= ema21` → `PULLBACK`; else
  `CHOP`. Both boundary comparisons are **inclusive**.
- **Bear-aligned:** `price <= ema9` → `TREND`; else `price <= ema21` → `PULLBACK`; else
  `CHOP`. Both boundary comparisons are **inclusive**.
- The comparand is `price`, the quote price passed into the classifier, compared against
  EMAs computed from closes.

> `cuttingboard/structure.py` L192–210 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L192-L210)
> `price` is supplied as `quote.price` — `cuttingboard/structure.py` L103 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L103)

### Both CHOP terminals

S-04's CHOP arises from **five** distinct paths, all transcribed above:

1. no derived metrics, or insufficient history (L157–158);
2. any of `ema9`, `ema21`, `ema50` missing (L164–165);
3. **degraded bull** — aligned bull with `price < ema21` (L199–200);
4. **degraded bear** — aligned bear with `price > ema21` (L209–210);
5. **non-aligned fallthrough** — neither alignment holds, and neither BREAKOUT nor
   REVERSAL matched (L212–213).

Terminal 5 is reached whenever the three EMAs are not in strict monotone order, absent a
BREAKOUT or REVERSAL match.

### REVERSAL requires no alignment

The REVERSAL test at L188–189 is evaluated **before** either alignment branch and does not
reference `ema_aligned_bull` or `ema_aligned_bear`. It therefore applies in aligned,
non-aligned, and crossing states alike. The source comment records this intent explicitly.

> `cuttingboard/structure.py` L184–189 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/structure.py#L184-L189)

BREAKOUT's own literals are already supplied by the frozen matrix row S-01 and are
**unchanged**; the two BREAKOUT branches are reproduced above solely to preserve the
executable order, and this amendment adds nothing to S-01.

### Recorded as found — the `0.0` substitutions

At L167–169 a missing `momentum_5d`, `volume_ratio`, or `ema_spread_pct` is replaced by
`0.0` and classification continues. This is transcribed because the branch logic is not
well-defined without it. **This amendment does not adjudicate how a Pine translation
should treat missing metrics** — it records only what the pinned source does.

---

## D-02 — true range, RMA equivalence, seed, and history guards

Function body: `cuttingboard/derived.py` L138–160 —
[blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L138-L160)

Called once per symbol at L108.

> `cuttingboard/derived.py` L108 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L108)

### True-range formula

```
prev_close = close.shift(1)
tr = pd.concat(
    [high - low, (high - prev_close).abs(), (low - prev_close).abs()],
    axis=1,
).max(axis=1)
```

That is `TR = max(H − L, |H − C₋₁|, |L − C₋₁|)`.

> `cuttingboard/derived.py` L144–152 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L144-L152)

### Smoothing

```
atr = float(tr.ewm(alpha=1 / 14, adjust=False).mean().iloc[-1])
```

`alpha = 1 / ATR_PERIOD = 1/14`, `adjust=False`. This matches the frozen matrix row D-02
verbatim and is restated here only because the seed below cannot be stated without it.

> `cuttingboard/derived.py` L159 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L159)

### Executable seed — the first TR is `H − L`

`pandas.DataFrame.max(axis=1)` defaults to `skipna=True`. On the first row `prev_close` is
`NaN`, so the two absolute-difference columns are `NaN` while `high - low` is a valid
number, and the row-wise maximum is therefore `H₀ − L₀` — **not** `NaN`. Consequently
`tr.dropna()` at L155 removes no row, and `ewm(adjust=False)` seeds its recursion on
`TR₀ = H₀ − L₀`.

> `cuttingboard/derived.py` L148–155 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L148-L155)

**Executable seed, transcribed: the first true range is `H − L`, and the RMA is seeded on
it.**

### Recorded as found — the source disagrees with itself on the seed

The comment at L154 reads *"Drop the first row whose prev_close is NaN before applying
RMA."* Under `skipna=True` that first row's true range is not `NaN`, so the `dropna()` at
L155 is a no-op and no row is dropped. **The comment does not describe the behaviour of
the code it annotates.**

> `cuttingboard/derived.py` L154–155 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L154-L155)

This disagreement is **recorded, not resolved.** Per this amendment's standing rule, the
executable statement governs the transcription above. Nothing here proposes a change to
the source, and this observation is not a defect report against CuttingBoard.

The docstring at L139–142 additionally asserts *"Matches TradingView's ATR implementation
exactly."* That is an assertion in the pinned source, transcribed here as found. **This
amendment makes no parity claim on its behalf**, and it does not relieve the frozen matrix
row D-02's standing instruction not to call a Pine ATR exact until initialization parity is
demonstrated.

### History guards, accurately scoped

Two separate guards exist at different layers. They are **not** interchangeable:

| Guard | Literal | Scope | Citation |
|---|---|---|---|
| ATR-local | `if len(tr) < ATR_PERIOD: return None` → `ATR_PERIOD = 14` | Applies **only to `atr14`**. Yields `None`; no substituted value | `cuttingboard/derived.py` L156–157 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L156-L157) |
| Metrics-wide | `if df is None or len(df) < OHLCV_MIN_BARS` → `OHLCV_MIN_BARS = 21` | Applies to the **whole derived-metrics record**: returns `sufficient_history=False` with *every* metric field `None` | `cuttingboard/derived.py` L70–76 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L70-L76) |

The metrics-wide guard is evaluated first: below 21 bars no ATR is attempted at all. The
`len(tr) < 14` guard is therefore reachable only for inputs that already cleared 21 bars.

The insufficient-history sentinel sets all metric fields to `None` and both alignment flags
to `False`:

> `cuttingboard/derived.py` L189–204 — [blob](https://github.com/dwats250/cuttingboard/blob/59f8279d796335149afdec4aa507b6f927233518/cuttingboard/derived.py#L189-L204)

**This amendment does not adjudicate warm-up behaviour** in any translation. It records the
two guards, their literals, and their distinct scopes.

---

## What this amendment does not do

- It changes no gate classification, threshold, variant, safeguard, or review rule.
- It adds no threshold, denominator, operator, band, default, fallback, proxy, or
  interpretation that the pinned source does not contain.
- It does not modify, reopen, or extend
  [`TV-0R-LITERAL-RULE-APPENDIX.md`](TV-0R-LITERAL-RULE-APPENDIX.md); R-01, R-02, R-05 and
  E-04 are untouched.
- It does not edit any frozen TV-0 document, and every recorded frozen hash is unchanged.
- It adjudicates nothing outside S-02, S-03/S-04 and D-02. Q-08 / DI-5, the
  `iv_environment` output, unreferenced module constants, ATR warm-up behaviour,
  missing-metric behaviour, and every implementation-level comparison detail remain open
  and are **not** decided here.
- It makes no statement about, and no correction to,
  `pine/cuttingboard_direct_proxy_v0.1.pine`. Checking any implementation against these
  literals is TV-2's task under the frozen contract.
- It proposes no CuttingBoard change. Observations recorded as found are evidence only, and
  no finding here authorizes an engine change or any back-feed. See `docs/conventions.md`
  §i.
- It authorizes no implementation, no compilation, no run, and no parity acceptance.
