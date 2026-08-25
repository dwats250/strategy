# analysis/ — reproduction code (per `docs/conventions.md` §d)

Empty until there are runs to analyze. No headline number exists yet to reproduce.

The PVAE offline analysis is pre-registered in
[`../manifests/PVAE_ANALYSIS_PREREG_v0.1.md`](../manifests/PVAE_ANALYSIS_PREREG_v0.1.md);
code implementing it lands here only after R1 passes the R0 identity gate.

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
