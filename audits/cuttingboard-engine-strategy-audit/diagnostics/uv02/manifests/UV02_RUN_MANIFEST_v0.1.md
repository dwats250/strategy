# UV02 Run Manifest — contract v0.1

Status: `ACTIVE CONTRACT — TEMPLATE. CREATING IT AUTHORIZES NO RUN.`

Created: 2026-07-27 UTC · Gate: `UV02-E1`

Governed by [`../UV02_STUDY_CONTRACT.md`](../UV02_STUDY_CONTRACT.md).

---

## How to use this contract

Copy this file to `manifests/<run-id>/RUN_MANIFEST.md` and fill **every** field before
exporting anything. A UV02 run is not preserved unless it has **both** this manifest and its
raw exports.

Manifests are **pre-registered and never edited in place** (`docs/conventions.md` §b).
Corrections are a dated amendment appended as a separate file, or a new manifest version with
the version in the filename. A re-run producing new numbers is a **new run**, never an edit
to an old one (§e).

**This contract is not `RUN_MANIFEST_TEMPLATE.md`.** That template belongs to TV-3 and names
v0.1's symbol list. This one is UV02-specific. Neither substitutes for the other, and
completing this one does not produce a TV-3 run package.

### Why this is not a TV-3 package

`../../spec/BACKTEST_PROTOCOL.md` § *Required exports* demands per-bar gate booleans,
rejection sets, regime/posture/confidence, structure labels, and a missing-data mask. See
[`../UV02_EVIDENCE_CAPABILITY.md`](../UV02_EVIDENCE_CAPABILITY.md) for what is and is not
obtainable today. A completed UV02 manifest records a **diagnostic run**.

---

## Field status vocabulary — binding

Every field carries a value or exactly one of these labels. **A blank is a defect, not a
pass** — a run with an unlabelled blank is not preserved (`docs/conventions.md` §h,
"unavailable is not the same as passing").

| Label | Meaning | Requires |
|---|---|---|
| `UNRECOVERABLE` | The value existed at run time and **cannot now be established** from surviving artifacts | A one-line reason. Never inferred, never defaulted, never back-filled from a declaration default |
| `UNRECORDED` | The value was **never captured** | A one-line reason |
| `PARTIALLY_RECOVERED` | Part of a compound field is established from artifacts, part is not | What was established, **the derivation that established it**, and what remains open |
| `NOT_APPLICABLE` | The field cannot apply to this run | Why |

### `PARTIALLY_RECOVERED` — the rule that makes it honest

A `PARTIALLY_RECOVERED` field **never collapses to a value**. It records a component-level
breakdown, and the parent field keeps the weakest label of its components.

The friction field of the 2026-07-26 captures is the reference case:

```
friction:  UNRECOVERABLE
  ├─ commission_reported : 0 on every row of all seven exports  [observation]
  │    derivation: Commission USD column; Net PnL reconciles to the exact
  │    price difference with no residual
  │    limit: a reported zero is not a proven Properties setting — display
  │    rounding at these price levels is uncharacterized
  ├─ slippage            : UNRECOVERABLE — the export carries no independent
  │    reference price to compare a fill against
  └─ scenario            : UNRECOVERABLE — PARITY / BASE / STRESS not established.
       A zero-commission / nonzero-slippage configuration matches none of them
```

The parent stays `UNRECOVERABLE` because the scenario is what the protocol asks for. Recording
the commission observation does not upgrade it.

### `OPERATOR` fields must be recorded *before* export — binding

These are not readable from Pine and **cannot be recovered afterwards**:

- friction scenario, commission type, commission value, slippage
- chart timezone, session setting, extended-hours flag
- data provider / exchange feed
- initial capital

This is the direct lesson of the 2026-07-26 session: TradingView's Properties tab overrides
the script's declaration defaults, so the declared value proves nothing about what ran. No
Properties screenshot was saved, and the setting is now permanently unrecoverable.

> **A run that exports before recording its `OPERATOR` fields has destroyed evidence that no
> later analysis can reconstruct.** Record them first. A Properties screenshot, checksummed
> and referenced here, is the cheapest sufficient record.

---

## 1. Identity

| Field | Value |
|---|---|
| Run ID | `UV02-<script8>-<symbol>-<tf>-<candles>-<window>-<variant>-ASOF-<YYYY-MM-DD>` |
| Run timestamp (UTC) | |
| Operator | |
| Gate | `UV02-<n>` |
| Study contract | `../UV02_STUDY_CONTRACT.md` |
| Manifest contract version | `v0.1` (this file) |

The run ID embeds the first eight hex digits of the script SHA-256, so the ID, the export
filename, and the source are checkable against one another.

## 2. Source and code

| Field | Value | Source |
|---|---|---|
| CuttingBoard source SHA | `59f8279d796335149afdec4aa507b6f927233518` | frozen |
| CuttingBoard mutation permission | **NONE** | frozen |
| Pine source file | | |
| Pine source SHA-256 | | OPERATOR — `sha256sum` of the exact bytes pasted into TradingView |
| Pine version | `v6` | |
| strategy repository commit | | OPERATOR |
| Universe membership | per `../UNIVERSE_V0.2.md`, or name the deviation | |

If the pasted script differs from the committed file by **one byte**, the run is attributed to
code that does not exist in the repository. Re-hash before recording.

## 3. Chart and instrument

| Field | Value | Source |
|---|---|---|
| Chart symbol | | AUTO (state table) |
| Timeframe | `1D` — the script refuses anything else | AUTO |
| Candle type | standard OHLC — the script refuses Heikin-Ashi, Renko, Range, Kagi, Line Break, Point & Figure | AUTO |
| Chart timezone | | **OPERATOR — record before export** |
| Session setting | | **OPERATOR — record before export** |
| Extended hours | | **OPERATOR — record before export** |
| Data provider / exchange feed | | **OPERATOR — record before export** |
| Properties screenshot | filename + SHA-256, or `UNRECORDED` | **OPERATOR** |

## 4. Cross-symbol IDs actually used

Record what the inputs **contained for this run**, not the defaults. All 20 rows are required.
Formula parity and data parity are separate: a formula can be correct while a provider or
session mapping remains `PROXY`. Record the mapping status honestly.

| Role | Configured ID | Resolved? | Notes |
|---|---|---|---|
| SPY (breadth) | | | |
| QQQ (breadth) | | | |
| IWM (breadth) | | | |
| GLD (breadth) | | | |
| SLV (breadth) | | | |
| GDX (breadth) | | | |
| SIL (breadth) | | | |
| GDXJ (breadth) | | | |
| USO (breadth) | | | |
| XLE (breadth) | | | |
| NVDA (breadth + leadership) | | | |
| AVGO (breadth + leadership) | | | |
| AMD (breadth + leadership) | | | |
| MU (breadth + leadership) | | | |
| TSLA (breadth) | | | |
| SOXX (breadth + leadership) | | | |
| VIX (macro — **not** breadth) | | | |
| DXY (macro — **not** breadth) | | | |
| TNX (macro — **not** breadth) | | | |
| BTC (macro — **not** breadth) | | | |

Breadth denominator: `TRADABLE_UNIVERSE_SIZE = 16.0`. The four macro drivers are excluded from
it. A missing requested value **stays missing**; breadth counts an absent tradable symbol as
**not advancing**. A missing value never becomes a neutral vote.

## 5. Variant and window

| Field | Value | Source |
|---|---|---|
| Variant | `V0` … `V6` | AUTO (`variant_index`) |
| Window name | | AUTO |
| Window start / end | | AUTO |
| Bars evaluated | | AUTO |
| First / last trade date | | from the export |

**Window naming constraint — binding.** The 2022-01-01 – 2026-07-24 period is a
`deferred-inspection descriptive window`. **No** manifest, report, summary, annotation, or
filename may call it a forward holdout or out-of-sample
(`../../spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md`). It has already been inspected in
the 2026-07-26 FULL-history capture and its pre-inspection status cannot be restored.

`FULL chart history` is **not** a predetermined protocol window. A run using it records that
plainly and does not map its results onto the protocol's window structure.

## 6. Friction

Declared in the script at `PARITY`, and **overridden in the Properties tab**. Pine cannot read
the effective values back. Friction is **recorded, never chosen or optimized.**

| Field | Value |
|---|---|
| Scenario | `PARITY` / `BASE` / `STRESS` / a status label |
| Commission type | |
| Commission value | |
| Slippage (ticks) | |
| Initial capital | |
| Order size | one directional unit |
| Pyramiding | `0` |

Scenario definitions (frozen): `PARITY` zero/zero; `BASE` 0.01% per transaction and one
minimum tick per fill; `STRESS` 0.03% per transaction and three minimum ticks per fill.

## 7. Thresholds in force

State `unchanged from cuttingboard_direct_proxy_v0.2.pine § 2` and give the Pine SHA-256 in
§2 — or record the block verbatim. **No threshold may differ between variants or between
runs.** A run that changed one is not a variant; it is a different study.

## 8. Missing data

| Field | Value | Source |
|---|---|---|
| Bars with ≥1 missing symbol | | AUTO |
| Missing symbols on the final bar (of 20) | | AUTO |
| Missing **breadth** symbols on the final bar (of 16) | | AUTO |
| Missing-vote distribution (0–8) | | from the per-bar export, or a status label |

## 9. Gate results

Record per gate. Where per-bar state is unavailable, use a status label — **never a blank and
never an assumed pass.**

| Gate | Class | Rejections | Notes |
|---|---|---|---|
| V0 no regime direction | — | | |
| Gate 1 REGIME | AVAILABLE | | |
| Posture rejections (R-05, separate) | AVAILABLE | | |
| Gate 2 CONFIDENCE | INERT | | |
| Gate 3 DIRECTION | INERT | | |
| Gate 4 STRUCTURE | AVAILABLE | | |
| Gate 5 STOP_DEFINED | INERT | | |
| Gate 6 STOP_DISTANCE | AVAILABLE | | |
| Gate 7 RR_RATIO | INERT | | |
| Gate 8 MAX_RISK | INERT / `UNAVAILABLE_LITERAL` | | |
| Gate 9 EARNINGS | INERT (`SKIPPED_FAIL_OPEN`) | n/a | |
| Gate 10 EXTENSION | AVAILABLE | | |
| Gate 11 TIME | **UNAVAILABLE** | n/a | Excluded from the soft arithmetic. Record the bar count it was unavailable on |
| Q-12 soft aggregation | AVAILABLE (Gate 6, Gate 10 only) | | |
| K-01 kill switch | AVAILABLE | | |
| E-04 macro conflict | AVAILABLE | | |
| T-01 / I-01 / E-05 | INERT diagnostics | | Not emitted per bar by v0.2 — see the capability document |

## 10. Provenance and file hashes

Every artifact the run produced. **A result that cannot name the code and the file that
produced it is not evidence.**

| File | SHA-256 | Contents |
|---|---|---|
| | | List of trades (raw, immutable) |
| | | Per-bar state export, if any |
| | | Properties screenshot, if any |

Exports are immutable (`docs/conventions.md` §e). A re-capture produces new files, never an
edit.

## 11. Known limitations carried forward

Carry every open item forward and add any this run surfaced. **A limitation that is not
written down is not disclosed.**

| # | Limitation | Status |
|---|---|---|
| 1 | v0.2 universe is not the pinned membership — **no parity claim possible** | permanent, by design |
| 2 | Pinned source not resolved during TV-1 | open |
| 3 | EMA warm-up divergence (D-01) | open |
| 4 | ATR initialization divergence (D-02) | open |
| 5 | Provider / session mapping `PROXY` | open |
| 6 | End-of-day percent-change proxy, not time-of-day parity | permanent, declared |
| 7 | Tick quantization of protective distances | permanent, declared |
| 8 | Same-bar stop-and-target ambiguity — conservative stop-first headline | permanent, declared |

## 12. Declaration

- [ ] All `OPERATOR` fields were recorded **before** export.
- [ ] No threshold was changed for this run.
- [ ] No field is blank; every unknown carries a status label and a reason.
- [ ] No unavailable gate was recorded as passing.
- [ ] The Pine SHA-256 in §2 is the hash of the exact source that produced these exports.
- [ ] No parity claim against the pinned engine is made.
- [ ] No profitability, alpha, live-execution, or options-return claim is made.
- [ ] The 2022–2026 window is described only as a deferred-inspection descriptive window.
- [ ] No CuttingBoard file, ref, branch, PR, issue, workflow, setting or remote was mutated.
- [ ] Nothing from this run was fed back into CuttingBoard.
- [ ] A row was added to `../LEDGER.csv` for this run.

---

## Appendix — mapping to `BACKTEST_PROTOCOL.md` § *Required run manifest*

Completeness check for this contract. UV02 is a diagnostic study, so protocol requirements are
either **mapped** or marked out of scope **with a reason** — never silently dropped.

| Protocol field | This contract |
|---|---|
| CuttingBoard source SHA | §2 |
| Pine source SHA-256 | §2 |
| Pine version | §2 |
| Run timestamp | §1 |
| SPY chart symbol, timeframe, timezone, session | §3 |
| All cross-symbol IDs | §4 — all 20 |
| Variant | §5 |
| Date window | §5 |
| Every threshold | §7 |
| Commission and slippage | §6 |
| Missing-data counts | §8 |
| Known parity exceptions | §11 |
| Raw export filenames | §10 |

**Out of scope, with reason:** the protocol's parity-exception framing assumes a run intended
to establish parity. UV02 cannot (§5 of the study contract), so §11 records limitations rather
than parity exceptions. Extended-hours flag, data feed, and the Properties screenshot are
**added** here beyond the protocol's list, because their absence is what made the 2026-07-26
friction unrecoverable.
