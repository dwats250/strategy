# Proxy findings — template v0.1

Status: `TEMPLATE — COPY PER RUN`

Created: 2026-07-28 UTC

Copy to `analysis/FINDINGS_<run_id>.md`. Its whole job is to keep **proxy behaviour** and
**live-engine evidence** apart, so no reader can mistake one for the other.

---

## 0. The separation — restate it, do not assume it

| | Proxy behaviour (this study) | Live-engine evidence (the closed audit) |
|---|---|---|
| What it is | What the mapped gate semantics do on declared TradingView chart history | What the pinned engine did under enforced isolation |
| Where it lives | `studies/cuttingboard-asis-proxy/` | `audits/cuttingboard-engine-strategy-audit/` |
| What it can support | Descriptive frequency, funnel, gate behaviour, chronology | Structural mapping, replay determinism, observability limits |
| What it can never support | Profitability, edge, live equivalence, accepted-path claims | Strategy quality, profitability, accepted-trade metrics |

**No finding here may be carried back into the closed audit**, and no audit record may be cited
as evidence that a proxy result reflects live behaviour.

## 1. Descriptive outputs only

Report only these. Each is a count or a sequence, not a judgement.

### 1.1 Signal / opportunity frequency
Bars evaluated; qualified; watchlist; rates. State the denominator explicitly.

### 1.2 Evaluated → qualified → emitted funnel, where representable
Bars with sufficient history → hard-gate pass → soft-gate pass → qualified.
**"Emitted" stops at qualified.** The proxy has no chain validation and no decision chain, so
there is no emitted-trade stage. Say so rather than substituting `qualified`.

### 1.3 Which mapped gates appear decisive, inert, or overlapping
From the `first_rejection` distribution and per-gate fail counts.

- **Decisive** — accounts for a material share of first rejections.
- **Inert** — never fails across the window. Record *why* if the reason is structural: Gate 5
  cannot fail given the deterministic geometry, and Gate 9 is fail-open by construction.
- **Overlapping** — two gates that fail on nearly the same bars.

Report counts. **Do not infer that an inert gate is useless** — a gate that never binds on one
symbol over one window is not thereby shown to be redundant.

### 1.4 Chronology of representative signals
A short dated list. Descriptive, not a trade log.

### 1.5 Unrecoverable gaps and proxy limitations
Every `UNRECOVERABLE` field from the run manifest, plus the standing limitations, plus anything
this run specifically could not establish.

## 2. Boundary checks before publishing

- [ ] No profitability, edge, expectancy, or future-performance claim anywhere.
- [ ] No claim of equivalence to a live CuttingBoard run.
- [ ] No accepted-path claim — unobservable here, as in the closed audit.
- [ ] Gate 8 and Gate 11 reported as NOT REPRESENTABLE, not as passing.
- [ ] `EXPANSION`, CONTINUATION, PULLBACK_IMBALANCE reported as not represented.
- [ ] `volume_ratio` and `ema_spread_pct` labelled approximations.
- [ ] Gate 6 and Gate 7 boundary behaviour reported as observed, not assumed (mapping §3.2).
- [ ] No trading recommendation of any kind.
- [ ] Every number traces to an export with a recorded checksum.

## 3. Uncertainty

State plainly what this run could not settle. A finding with an unknown consequence is recorded
as unknown — it is not rounded up to a conclusion.
