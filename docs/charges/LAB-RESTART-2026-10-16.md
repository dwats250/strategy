# Charge — LAB-RESTART-2026-10-16

**Issued by:** Dustin, in a Claude Code session on 2026-10-16. This file transcribes that charge into
the repository, because chat history is not authority (`CLAUDE.md`). Where this transcription and
Dustin's words differ, Dustin's words govern, and the difference is a defect in this file.

## Authorized

- Restart `dwats250/strategy` as a durable, reusable Python strategy research lab.
- Recovery of prior work, implementation, tests, documentation and commits; pushing a working branch;
  opening and updating a PR **in `dwats250/strategy` only**.
- **Not authorized:** merging; mutating CuttingBoard or any other repository; live trading; broad
  parameter optimization; paid data or model services; signing up for services; contacting the
  creator; unrelated repository cleanup.

## Direction (summary)

- Backtesting.py is the first execution engine. NautilusTrader is the fallback only after a
  demonstrated limitation. Do not implement two engines.
- Workflow: idea or source → explicit rules → baseline and named variants → repeatable runs →
  interactive results and comparisons. Independent strategy comparisons, not shared capital pools.
- First strategy: an Instagram reel by @austin.daytrades, shared by Marc. Produce a source/rule table
  and a provisional interpretation. Never call it an exact replication, and never import the FastAlpha
  rules as the creator's.
- Main experiment: a separately named, fully specified VWAP baseline plus 3–5 one-factor variants,
  frozen before results are examined, with every configuration tracked.
- Validate the engine with hand-checkable examples. Use exchange calendars. Use equity-based portfolio
  metrics kept separate from trade R statistics.
- Report the full history, fixed calendar subperiods, and the latest six months ending on the last
  complete session (exploratory, not a holdout). Separate running from reset equity.
- Provide a self-contained interactive HTML report (offline, mobile-readable).
- Durability: pinned dependencies, one command, preserved identities, deterministic reruns,
  START_HERE, handoff, lightweight CI and a backup plan.

## Review seams

1. **Executable foundation.** Recovery findings, demonstrated engine behaviour, source ambiguities,
   the proposed VWR baseline and variants, and an initial HTML from a simple verified example. **Stop
   before interpreting the proposed experiment's outcomes.**
2. **First real experiment.** After review: run, reconcile, explain limitations. Stop.
3. **Reuse.** A structurally different strategy through the same workflow.

## Interaction with standing rules

- Conventions §i: the sole mutation target is `dwats250/strategy`. CuttingBoard is not read or touched
  by this charge.
- Conventions §j lanes are declared in `docs/lab/RECOVERY_FINDINGS_2026-10-16.md`.
- Conventions §a/§b apply to the new study `studies/vwap-ema9-2026-10/`. Frozen August records are not
  edited.
