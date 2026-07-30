# Gate Translation Matrix — Q-03 correction, 2026-07-30

Status: `DATED CORRECTION — narrowly scoped. The corrected record is not edited.`

**Corrects:** `GATE_TRANSLATION_MATRIX.md` (Status: FROZEN FOR TV-1, SHA-256
`04e130a51cf1d1a9f98377f8f4b372c457f4a2f5c974557fa6363af5764d605d`), specifically the Q-03
classification and, in part, load-bearing semantic finding #4. Per `docs/conventions.md` §b/§h,
the frozen matrix is preserved unmodified; this dated correction is the amendment.

**Authorization and boundary.** This correction is Dustin-chartered (Q-03 correction gate,
2026-07-30). The proxy study's findings discipline forbids carrying proxy findings back into
the closed audit by default; this record is the explicit owner authorization for exactly one
classification correction. It amends a pre-registered *hypothesis classification*, not any
EA-phase conclusion; the closed audit's results, closure, and evidence are untouched, and no
engine, Pine, rule, threshold, data, or study is changed.

---

## 1. The corrected claim

The frozen matrix classifies:

> | Q-03 | Gate 3 DIRECTION | Candidate direction must match regime | `CURRENTLY_INERT` |
> Preserve and count; direct candidate direction is generated from regime |

and semantic finding #4 states: "**Direction alignment is constructed to pass.** The same
regime function creates the candidate direction and checks it."

On the registered AMEX:SPY 1D AS-IS proxy window (export
`CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv`, SHA-256
`d1b537506ed1cec9559ad9dd66a35d4a9798d751ee1896e07e6e1739dfe0b970`, 3,620 rows), **g3 DIRECTION
failed on 527 rows**, decomposing exactly and exhaustively into:

- **147 CHAOTIC-regime bars**, and
- **380 zero-net NEUTRAL bars** (`regime_code == 3` with `net_score == 0`),

with zero unexplained rows.

## 2. Why the classification is falsified, not a proxy artifact

Commit-addressed source review at the pinned SHA
(`dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`,
`cuttingboard/qualification.py:635 direction_for_regime`) confirms the proxy transcribes the
pinned direction logic faithfully: the function returns no direction in exactly those two
states, and the pinned qualification loop's own PRD-235 comment records that a symbol with "no
regime direction (e.g. NEUTRAL with net_score 0)" lands in `excluded`. The failing states are
therefore reachable engine states, not Pine artifacts. Under the matrix's own vocabulary
(`CURRENTLY_INERT`: "present in the engine but cannot change the SPY direct" outcome), the
Q-03 classification is **falsified on this window**: the direction condition does change
outcomes. Semantic finding #4 remains true as a statement about *directional* regimes; it fails
as grounds for inertness because regimes with no direction are reachable.

## 3. The limit of the correction

In this window g3 had **no sole exclusions**: every g3 failure co-occurred with a g1
posture/confidence-floor failure (147 CHAOTIC bars fail the posture floor directly; the 380
zero-net NEUTRAL bars carry zero confidence, below the 0.50 floor). This correction therefore
establishes only that Q-03 is not inert. It does **not** establish independence from g1,
redundancy with g1, a production defect, or any basis for a threshold change, and it makes no
claim beyond the registered SPY daily window.

## 4. Related record — Gates 1 and 2 are near-duplicates here, not duplicates

On the same window, `g1` and `g2` **differ on 35 of 3,620 rows**. The strict duplicate
relationship previously implied (EA5-005, "Gates 1–2 duplicated"; carried as draft item B3) is,
on this evidence, near-total overlap with a small genuine divergence. The mechanism of the 35
rows is **recorded as unexplained**; none is inferred here.

## 5. Evidence chain

| Artifact | Identifier |
|---|---|
| Frozen matrix (corrected record) | SHA-256 `04e130a5…` |
| Registered export | SHA-256 `d1b53750…`; ledger row `RUN_SPY_1D_2015-01-01` |
| Producing script (frozen) | `cuttingboard_asis_proxy_v0_1.pine`, SHA-256 `048f5c66…` |
| Gate 2 analysis + §d script | `studies/cuttingboard-asis-proxy/analysis/ANALYSIS_GATE_STRUCTURE_2026-07-30.md`, `gate_structure_analysis_v0_1.py` (commit `aa692db`, merged `3cb17b2`) |
| Pinned source reads | commit-addressed at `59f8279d…`: `qualification.py:635` (`direction_for_regime`), PRD-235 comment in the qualification loop |
