# TV-1 — Pine v6 Direct-Path Proxy

Status: COMMISSIONED AFTER COMPANION-REPOSITORY PREFLIGHT

## Authority

- Source evidence:
  `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
- Governing matrix: `spec/GATE_TRANSLATION_MATRIX.md`
- Governing protocol: `spec/BACKTEST_PROTOCOL.md`
- Governing repository: a separate `cuttingboard-gate-lab` companion
  repository
- CuttingBoard mutation permission: NONE
- Merge permission: NONE

If the companion repository does not exist, STOP for Dustin to create or name
it. Do not place these files in `dwats250/cuttingboard`.

## Objective

Implement one compiling Pine Script v6 strategy that translates the frozen
TV-0 direct-path contract, exposes incremental gate variants, and exports
enough visible state for parity and rejection analysis.

## Work type

- Mode: IMPLEMENTATION
- Risk: RESEARCH-ONLY
- Mutation permission: companion repository only
- Live alerts, broker integration, or order routing: FORBIDDEN

## Mandatory preflight

Report before editing:

1. Repository name and remote.
2. Actual branch.
3. Full starting SHA.
4. Clean working tree.
5. Confirm `dwats250/cuttingboard` is not the writable repository.
6. Confirm the pinned source SHA resolves.
7. Read all three TV-0 documents completely.
8. Confirm no Pine implementation already supersedes this charge.

STOP on any mismatch. Do not switch or reset without Dustin's explicit
authorization.

## Allowed files

- `pine/cuttingboard_direct_proxy_v0.1.pine`
- `spec/PARITY_CASES.md`
- `runs/RUN_MANIFEST_TEMPLATE.md`
- `README.md` only for a link to the new script and its status

No other file may change.

## Change-surface ceiling

- Pine files: 1
- Documentation files: 3
- Dependencies: 0
- Workflows: 0
- Generated exports: 0 in this packet

## Required implementation

### Script declaration

- `//@version=6`
- `strategy(...)`
- standard-OHLC fills enabled where supported;
- pyramiding disabled;
- commission and slippage parameters declared;
- runtime refusal on any timeframe other than one day.

### Named state

The source must use named intermediate values for:

- every regime vote;
- vote coverage, raw net, bounded net, confidence, regime, and posture;
- expansion conditions;
- kill-switch legs;
- EMA/ATR/momentum/volume values;
- structure conditions and final structure;
- Gates 1 through 11, including explicit `AVAILABLE`, `INERT`, or
  `UNAVAILABLE` metadata;
- soft-failure count over available gates only;
- macro-pressure components and overall pressure;
- every incremental variant entry condition.

### Visibility

Provide:

- a compact last-bar table showing variant, regime, posture, structure,
  gate states, missing-data count, and first rejection reason;
- plots for EMA9/21/50;
- stop and target plots only while a simulated position is open;
- cumulative rejection counters by gate;
- data-window controls;
- explicit cross-symbol inputs.

Do not add discretionary scoring, weights, alerts, predictions, optimization,
or thresholds absent from TV-0.

### Strategy behavior

- Signal only on confirmed daily bars.
- Entry at the next bar open.
- Stop/target geometry follows `BACKTEST_PROTOCOL.md`.
- Long and short enabled.
- One position at a time.
- No same-bar reversal.
- Ambiguous stop-and-target bars use conservative stop-first headline
  treatment and expose an ambiguity counter.

## Discriminating tests and parity cases

Document fixture cases that prove:

1. strict versus inclusive threshold operators;
2. missing-vote bounding;
3. RISK_ON, RISK_OFF, CHAOTIC, EXPANSION, and computed NEUTRAL behavior;
4. the apparent NEUTRAL reachability issue;
5. BREAKOUT/REVERSAL priority;
6. direct 2R construction;
7. stop ATR-floor equality and independent 1% floor;
8. zero/one/two available soft failures;
9. kill-switch strict `>` comparisons;
10. macro-pressure conflict;
11. unavailable gates do not silently report PASS;
12. no repainting after confirmation.

Performance is not a test oracle. A change that improves results but breaks a
fixture is wrong.

## Validation

1. Pine v6 compiles.
2. Strategy loads on a standard SPY daily chart.
3. Non-daily chart produces the intended refusal.
4. Every variant can be selected without changing source.
5. Parity cases are documented with observed results.
6. No lookahead/future leak.
7. Diff contains allowed files only.
8. No CuttingBoard write occurred.

## Review

- One fresh-context semantic review of the final Pine SHA.
- Review the implementation against TV-0, not performance.
- Maximum one bounded correction cycle.
- If cross-symbol mapping or ATR initialization remains ambiguous, stop for a
  recorded proxy decision rather than recursively reviewing.

## Landing

- One intentional commit after parity checks.
- Draft PR only.
- No auto-merge.
- No agent merge.
- Final state: `Held for your merge`.

