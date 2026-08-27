# analysis/ — reproduction code (per `docs/conventions.md` §d)

Empty until there are runs to analyze. No headline number exists yet to reproduce.

The VDC local parity foundation lives here: `parity_foundation.py` (RTH-only 5m bar
reconstruction + Fast Alpha v0 feature calculator per the ingested source; no simulation,
no P/L) with deterministic tests in `test_parity_foundation.py`. Derived outputs stay
under the gitignored `../data/cache/derived/`. Parity status: `../PARITY_GATES.md`.

The PVAE offline analysis is pre-registered in
[`../manifests/PVAE_ANALYSIS_PREREG_v0.1.md`](../manifests/PVAE_ANALYSIS_PREREG_v0.1.md);
code implementing it lands here only after R1 passes the R0 identity gate.

**2026-08-26 — offline FastAlpha execution engine + V0/V1 A/B** (owner charge; TradingView
de-gated as a research dependency). The engine `fastalpha_engine.py` adds only the execution
layer Pine performs (orders, fills, ATR stop, thesis/EOD exits, the `flat` gate, per-trade P/L)
on top of `parity_foundation`'s feature seam; its broker-emulator assumptions are stated a priori
in the module docstring and never tuned against P/L. Tests: `test_fastalpha_engine.py` (11
engine-path cases). Calibration `v0_calibration.py` asserts the R0 headline, reproduces 89.86% of
R0 by (fill bar, side), validates the execution logic against the ~1% dividend feed scale, and
classifies the residual — the absolute-P/L gap is corpus bad-ticks (141 spike bars), not logic:
**LOCAL ENGINE RESEARCH-READY** (evidence `V0_CALIBRATION_RESULTS_2026-08-26.json`). The controlled
A/B `v0_v1_ab.py` runs V0 (EMA 9/20) vs V1 (EMA 10/22) on identical bars/engine, determinism-checked
and spike-robust: **V1 DEVELOPMENT NEUTRAL** (evidence `V0_V1_AB_RESULTS_2026-08-26.json`). Full
record: [`../manifests/RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md`](../manifests/RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md).
Recommended next offline step: pre-registered corpus bad-tick screening (not implemented).

Analysis code here is part of the experiment, not a scratch step: it is versioned, committed, and
held to the same rigor as the manifest and scripts. When runs exist, a reproduction script here
must, at minimum:

- assert the headline numbers the study reports and **fail loudly** (nonzero exit) if they don't
  reproduce;
- print the package versions it ran under;
- print the checksum of every input file it reads (the ledger and the exports it consumes).

`reproduce_campaign.py` in `studies/spy-orb-first-break/` is the template for this pattern.

No analysis runs during the bootstrap scaffold: no ranked backtests, no parameter comparisons, no
performance interpretation.
