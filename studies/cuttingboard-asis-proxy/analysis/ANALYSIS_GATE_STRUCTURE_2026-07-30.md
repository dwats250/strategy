# Gate-structure analysis — RUN_SPY_1D_2015-01-01 export

Status: `PUBLISHED 2026-07-30 UTC — descriptive analysis of registered evidence. AUTHORIZES NOTHING.`

Input: `../exports/CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv`, SHA-256
`d1b537506ed1cec9559ad9dd66a35d4a9798d751ee1896e07e6e1739dfe0b970`, 3,620 data rows.
Code: `gate_structure_analysis_v0_1.py` (§d — asserts every headline number, verifies the input
checksum, stdlib only). Pre-registered hypotheses: `docs/gap-register-2026-07-29.md` G-13…G-16,
committed (`16ac7fe`) before this analysis ran. Pinned-source reads are commit-addressed at
`dwats250/cuttingboard@59f8279d…` per §i; no working tree was read and nothing was mutated.

This analyzes the already-registered export. It is not a new run, does not reopen the study,
tunes nothing, and recommends no engine change. Counts below are full-window (3,620 rows)
unless stated.

---

## G-13 — CONFIRMED, upgraded to a row-level identity

`g7_rr` fail ⟺ `regime_code == 3`, on all 3,620 rows (cross-tab: regime-3 pass 0 / fail 1,157;
other pass 2,463 / fail 0). The `rr` column has **zero influence**: 585 rows with rr < 2.0
passed g7; 282 rows with rr > 2.0 failed it. On this window, Gate 7 carries no information
beyond the regime code. Mechanism (pinned source, `options.py` geometry): stop = 1×ATR,
target = 2×ATR ⇒ rr ≈ 2.0 by construction; NEUTRAL demands ≥ 3.0 (always fails), every other
regime demands ≥ 2.0 (always passes). The mapping §3.2 boundary doubt is thereby settled *for
this window*: the boundary never independently decided anything.

## G-14 — CONFIRMED

`g5_stop_defined` passes 3,620 / 3,620. Tautological on this window, exactly as the geometry
predicts. Inert-here is not redundant-everywhere; recorded as observation only.

## G-15 — RESOLVED: genuine falsification, not a proxy artifact

`g3_direction` fails 527 / 3,620 rows (14.6%), decomposing **exactly** into 147 CHAOTIC bars +
380 NEUTRAL bars with `net_score == 0` (0 unexplained). The proxy's `dir_code` is a faithful
transcription of the pinned `qualification.py:635 direction_for_regime`, which returns no
direction in precisely those two states — and the pinned qualification loop's own comment
(PRD-235) confirms the engine treats "no regime direction (e.g. NEUTRAL with net_score 0)" as
an exclusion. `GATE_TRANSLATION_MATRIX.md` Q-03 (`CURRENTLY_INERT`, "constructed to pass") is
**falsified**: the direction gate binds. Caveat: it never binds *solely* here — every g3
failure co-occurs with another hard-gate failure (sole-hard-failure rows: 0), so it is
decisive only jointly on this window.

## G-16 — REFINED: two identities hold, one was a count coincidence

Row-level checks upgrade (or demote) the register's exact count identities:

| Claimed identity | Row-level result |
|---|---|
| `g1 == (posture_code == 1)` | **HOLDS on all rows** — g1 is a restatement of the posture floor |
| `g7-fail == (regime_code == 3)` | **HOLDS on all rows** (G-13) |
| `g3 == (direction_code != 0)` | **HOLDS on all rows** (definitional in the proxy; G-15 shows the underlying state is reachable) |
| `g4-fail == (regime_code == 2)` | **VIOLATED** — 477 g4-fails outside regime 2 and 477 g4-passes inside it; the 619 = 619 count match was offsetting, not structural |

Additionally: `g1` and `g2` differ on **35 rows** — near-total overlap (both fail 2,500
non-kill rows) but **not** duplicates. EA5-005's duplication finding reads, on this evidence,
as near-duplication with a small genuine divergence; the mechanism of the 35 rows is not
established here.

## Marginal structure — the effective decision surface on this window

Among the 729 hard-pass, non-kill rows: only `g6_stop_distance` (fails 373, **141 sole**) and
`g10_extension` (fails 388, **156 sole**) ever reject; they co-fail on 232 rows. Sole failures
sum to 297 = the WATCHLIST count exactly. `g5`, `g7`, `g9` never fail at this stage. Among
non-kill rows, hard-gate sole failures: `g4` 165 (= first-rejection code 5), `g1`/`g2`/`g3`
never solely (g1 and g2 shadow each other; g3 is shadowed by g1).

Net: of the 11 mapped gates, on SPY 1D 2012–2026 — two are NOT REPRESENTABLE (g8, g11), three
cannot independently reject (g5 tautological, g9 fail-open, g7 a regime restatement), and the
live surface is **regime/posture (g1, with g2 nearly identical), structure (g4), direction
(g3, jointly), stop-distance (g6), extension (g10), plus the kill switch**. First-rejection
distribution: {0: 200, 1: 226, 2: 2,500, 5: 165, 7: 373, 10: 156}.

## Boundary checks

- No profitability, edge, or future-performance claim; no trading recommendation; no threshold
  change proposed.
- Engine attribution appears only where a commit-addressed pinned-source read supports it
  (`qualification.py` direction logic; `options.py` geometry); everything else is proxy-level.
- No claim that an inert-here gate is redundant; one symbol, one window.
- Every number traces to the registered export checksum above and is asserted in the committed
  script.

## Uncertainty

- The 35 g1/g2-divergent rows are recorded but not mechanistically explained.
- All structure statements are conditional on SPY 1D over this window; none generalize to other
  symbols, timeframes, or engine states the proxy cannot represent (EXPANSION, CONTINUATION,
  PULLBACK_IMBALANCE, the accepted path).
- What follows from the falsified Q-03 classification for the matrix document itself is an
  owner decision (a dated correction to that record), not something this analysis performs.
