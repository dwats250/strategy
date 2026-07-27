# UV02 Study Contract — Universe Relevance Study

Status: `ACTIVE STUDY CONTRACT — DIAGNOSTIC SIDE-STUDY, NOT TV-0→TV-4 PACKET EVIDENCE`

Created: 2026-07-27 UTC · Gate: `UV02-E1`

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`.
Mutation permission: **NONE**. Nothing in this document proposes or authorizes a
CuttingBoard change.

---

## 0. Standing of this document

This contract gives UV02 a stated identity and a claim boundary. It does **not** register
UV02 in the governing TV-0 → TV-4 protocol and confers no standing under it. UV02 remains
unregistered in every governing document. See
[`../README.md`](../README.md).

Where this contract and any frozen TV-0 authority appear to disagree, **the frozen authority
governs.** This document creates no precedence, relaxes no rule, and reinterprets nothing.

---

## 1. Purpose

Measure how the incremental gate families `V0`–`V6` behave when the R-01 breadth and
leadership membership is replaced by a **historically tradable 16-symbol universe**, holding
every threshold, formula, gate order, timing model, and friction model fixed.

The question is **universe sensitivity**: how much of the gate stack's selectivity is a
property of the gate logic, and how much is a property of which symbols the breadth
denominator happens to contain.

That question exists because the pinned engine's own membership is not uniformly tradable
over the study's history. `UNIVERSE_V0.2.md` records the concrete case: `SMCI` appears in the
pinned leadership list but not in `ALL_SYMBOLS`, so under a verbatim reproduction it is
structurally ineligible and contributes a forced zero to the leadership count. UV02 asks what
the gates do when that structural artifact is removed.

---

## 2. Non-goals — stated as prohibitions

UV02 **is not**, and no artifact of it may be presented as:

1. **TV-1 evidence.** TV-1's artifact is
   `../../pine/cuttingboard_direct_proxy_v0.1.pine`, frozen at blob
   `76932a223602463813698ceb8fd9cb8f1272260a`.
2. **A correction to TV-1.** v0.2 does not fix, supersede, replace, or re-open v0.1. The two
   compile defects v0.2 corrects are **not** applied to v0.1, which stays frozen.
3. **A TV-2 parity input.** Excluded by construction — see §5.
4. **A TV-3 run package.** The captures do not satisfy `../../spec/BACKTEST_PROTOCOL.md`
   § *Required exports*. See [`UV02_EVIDENCE_CAPABILITY.md`](UV02_EVIDENCE_CAPABILITY.md).
5. **A profitability, alpha, live-execution, or options-return claim.** None is made and none
   is supported.
6. **An authorization to change CuttingBoard.** Backtest behaviour alone cannot authorize an
   engine change (`docs/conventions.md` §h).

---

## 3. Universe identity — the literal membership

`TRADABLE_UNIVERSE_SIZE = 16.0` (v0.2 source line 209). The breadth arithmetic is therefore
unchanged from v0.1: `>= 0.70` of 16 requires **at least 12 advancing**; 11 advancing
(`0.6875`) fails.

### 3.1 The 16 breadth members

| Group | Members |
|---|---|
| Broad (3) | `AMEX:SPY`, `NASDAQ:QQQ`, `AMEX:IWM` |
| Metals / miners (5) | `AMEX:GLD`, `AMEX:SLV`, `AMEX:GDX`, `AMEX:SIL`, `AMEX:GDXJ` |
| Energy (2) | `AMEX:USO`, `AMEX:XLE` |
| Semis / high beta (6) | `NASDAQ:NVDA`, `NASDAQ:AVGO`, `NASDAQ:AMD`, `NASDAQ:MU`, `NASDAQ:TSLA`, `NASDAQ:SOXX` |

### 3.2 The 5 leadership members

`NVDA`, `AVGO`, `AMD`, `MU`, `SOXX`.

Every leadership member is also a breadth member, so **no member is structurally ineligible
and none contributes a forced zero.** The leadership literals are unchanged:
`EXPANSION_LEADERSHIP_MIN_PCT = 0.015` (line 203) and
`EXPANSION_LEADERSHIP_MIN_COUNT = 2` (line 204).

### 3.3 Macro context — not breadth members

`VIX`, `DXY`, `TNX`, and `BTC/USD` feed the R-02 vote model, the K-01 kill switch, and E-04
macro pressure. They are **excluded from the breadth denominator**, exactly as the
non-tradable macro drivers were in v0.1. Their symbol IDs are unchanged.

Total requested series: **16 breadth + 4 macro = 20.**

### 3.4 Exclusions, and the recorded reason for each

| Symbol | Disposition | Recorded reason |
|---|---|---|
| `PAAS` | Removed entirely | One of the two v0.2 compile defects. Not re-added under any exchange prefix |
| `AAPL`, `META`, `AMZN`, `COIN`, `MSTR` | Replaced | Part of the deliberate universe change |
| `SMCI` | Removed entirely | Present in v0.1 only because the pinned leadership list names it while `ALL_SYMBOLS` does not, making it structurally ineligible. v0.2 does not reproduce the pinned list, so the member and its forced-zero term have no purpose |
| `SNDK`, `UCO`, `HYMC`, `DRAM` | Deliberately kept out | Discretionary dashboard members. Including them would let present-day watchlist composition drive historical breadth counts — a selection effect, not a measurement |
| `SMH` | Not added | Recorded as considered and not added |

---

## 4. Unchanged-thresholds statement

**No threshold, formula, gate order, variant logic, timing model, or friction model differs
between v0.1 and v0.2.** Only universe membership, the two compile defects, and the script
identity differ.

This is verified, not asserted. Reproduce with:

```sh
A=audits/cuttingboard-engine-strategy-audit
V1=$A/pine/cuttingboard_direct_proxy_v0.1.pine
V2=$A/diagnostics/uv02/cuttingboard_direct_proxy_v0.2.pine

# 1. Every threshold/enum constant is byte-identical. Empty output == identical.
diff <(grep -E '^[A-Z][A-Z0-9_]+ *= *[-0-9.]' $V1) \
     <(grep -E '^[A-Z][A-Z0-9_]+ *= *[-0-9.]' $V2)

# 2. The diff touches no entry/exit, gate-pass or variant logic. No output == none touched.
git diff --no-index --unified=0 $V1 $V2 | grep -E '^[-+]' | grep -vE '^[-+][-+]' \
  | grep -iE 'strategy\.(entry|exit)|g[0-9]+_pass|v[0-6]_pass|signal_pass|use_(posture|structure|softgates|killswitch|macro)'

# 3. Overall change surface.
git diff --stat --no-index $V1 $V2      # 91 insertions(+), 66 deletions(-)
```

Observed at the time of writing: check 1 produced **no output** — the constant blocks are
identical, covering the R-02 vote cutoffs, `VIX_CHAOTIC_SPIKE`, the R-04/R-05 confidence and
posture cutoffs, the K-01 kill-switch legs, the EMA/ATR/momentum/volume lengths, the S-01/S-02
structure literals, `GATE2`/`GATE6`/`GATE7`/`GATE8`/`GATE10`, the macro-pressure cutoffs, and
every regime/posture/structure/vote enum. Check 2 produced **no output**.

All seven variants live in this one source file, selected by the same `Variant` input and
reported through the same `variant_id`. **There is no per-variant script**, and a run that
changed a threshold would not be a variant — it would be a different study.

---

## 5. Separation from TV-1 and v0.1

`../../spec/TV-0R-LITERAL-RULE-APPENDIX.md` requires TV-1 to reproduce the pinned R-01 lists —
`config.ALL_SYMBOLS` minus `config.NON_TRADABLE_SYMBOLS` for breadth, and
`config.EXPANSION_LEADERSHIP_SYMBOLS` for leadership — without substituting, dropping, or
supplementing a member.

**v0.2 deliberately departs from that membership.** The departure is the experiment, not a
defect. Its consequence is binding:

> R-01 breadth and leadership output from v0.2 is **not comparable to the pinned engine, by
> construction and on purpose.** It may not be used for TV-1 or TV-2 parity, and no
> comparison of it against the pinned engine is a parity result.

Because R-01 feeds `EXPANSION`, which sets regime, posture, confidence, and therefore
candidate direction, the non-comparability propagates through the whole gate stack. It is not
confined to the R-01 row.

Fixed identities:

| Artifact | Identity |
|---|---|
| v0.1 (TV-1, frozen) | blob `76932a223602463813698ceb8fd9cb8f1272260a` |
| v0.2 (UV02) | SHA-256 `d2420bc398d3e23f477d71edbd5e6f1cdb51e377380c2e000f1a0bc63eba53ce` |

**No v0.2 result may be reported as a v0.1 result**, and the reverse likewise. Every export
filename embeds `d2420bc3` so the binding is checkable. The v0.2 file **must never be edited
in place**: doing so breaks that binding and silently orphans all seven captures. A change
gets a new file and a new hash (`docs/conventions.md` §e).

### v0.1 is known not to compile

Recorded because it bears on how the two scripts relate. `UNIVERSE_V0.2.md` documents that
v0.2 corrected an `input.time()` default using the non-const-foldable
`(timezone, y, m, d, h, m)` form, which Pine rejects as an `input.time()` default. That defect
is present in v0.1 and was deliberately **not** corrected there. So v0.1 is not merely unrun —
as committed it will not compile.

This is a TV-1 / TV-1R matter. UV02 records it and does nothing about it.

---

## 6. Allowable claims

A UV02 result may support **descriptive statements about relative gate selectivity across
`V0`–`V6` under this universe**, provided every such statement names, in the same breath:

1. the universe (`UV02 v0.2 16-symbol tradable universe`, never "the universe");
2. the script SHA-256 `d2420bc3…3ce`;
3. the friction status — currently `UNRECOVERABLE`
   (see [`UV02_CAPTURE_LOG_AMENDMENT_2026-07-27.md`](UV02_CAPTURE_LOG_AMENDMENT_2026-07-27.md));
4. the window actually captured, which for the existing seven exports is FULL chart history
   and **not** a predetermined protocol window.

Example of a claim in bounds:

> Under the UV02 v0.2 16-symbol universe, at script `d2420bc3…`, over FULL chart history and
> with the friction scenario `UNRECOVERABLE`, entry counts fall monotonically from V0 to V6.

That is a statement about counts under a stated configuration. It is not a performance claim.

---

## 7. Prohibited claims

No UV02 document, commit message, report, summary, chart annotation, or export filename may
assert any of the following:

1. **Profitability, alpha, edge, or expected future performance**, in any form.
2. **Options returns**, spread pricing, chain liquidity, or implied volatility.
3. **Live-execution fidelity** — fills, slippage realism, or runtime parity with a live
   CuttingBoard run. UV02 evaluates confirmed daily bars and acts at the next daily open.
4. **Parity with the pinned engine**, in whole or in part. Excluded by §5.
5. **Out-of-sample or forward-holdout status for 2022-01-01 – 2026-07-24.** That period is a
   `deferred-inspection descriptive window`
   (`../../spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md`). It was inspected as part of the
   FULL-history capture; **its pre-inspection status cannot be restored** and no artifact may
   describe it as untouched.
6. **That an unavailable gate passed.** Unavailable is not the same as passing
   (`docs/conventions.md` §h). Excluded gates are reported separately and never enter the
   arithmetic.
7. **That a UV02 finding authorizes a CuttingBoard change**, a parameter change, an issue, a
   refactor, or any other back-feed.
8. **That row counts are results.** Trade-leg counts in the capture log and `n` in
   `LEDGER.csv` are structural integrity figures, not findings.

---

## 8. Governing records

| Record | Role |
|---|---|
| [`LEDGER.csv`](LEDGER.csv) | **Authoritative** under `docs/conventions.md` §f — one row per run. Wins over any export or screenshot that disagrees |
| [`manifests/UV02_RUN_MANIFEST_v0.1.md`](manifests/UV02_RUN_MANIFEST_v0.1.md) | What any future UV02 run must preserve |
| [`UV02_CAPTURE_LOG.md`](UV02_CAPTURE_LOG.md) | The 2026-07-26 capture session, plus its dated amendment |
| [`UNIVERSE_V0.2.md`](UNIVERSE_V0.2.md) | Universe membership and the reason for each change |
| [`UV02_EVIDENCE_CAPABILITY.md`](UV02_EVIDENCE_CAPABILITY.md) | What the artifacts can and cannot establish |

## 9. Amendment rule

This contract is a frozen document from creation. It is **never edited in place**. A
correction is a dated amendment file or a new versioned contract, with the version in the
filename (`docs/conventions.md` §b, read across by §h). A change to the universe membership,
to any threshold, or to the claim boundary is a **new study**, not an amendment to this one.
