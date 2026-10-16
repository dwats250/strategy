# Handoff — current state

*Updated 2026-10-16. The repository is the source of truth; chat context and private artifact links are
conveniences. Direction: [`../research/ROADMAP.md`](../research/ROADMAP.md). Hypotheses and results:
[`../research/STRATEGY_RESEARCH_LEDGER.md`](../research/STRATEGY_RESEARCH_LEDGER.md).*

## Where things stand

- **Branch / PR:** `lab/restart-2026-10` (worktree `~/Projects/strategy-lab`), PR #20 against `main`,
  **open and unmerged**. The PR carries the 31 inherited August commits (`study/vwap-lab-2026-08`, preserved
  unchanged) plus the lab restart.
- **Active question:** the **VMR-L mean-reversion strategy-definition review**
  (`studies/vwap-mr-2026-10/manifests/VMRL_FAMILY_PROPOSAL_v0.1.md`), including its data choice.
- **Next action after approval:** freeze `VMRL_EXPERIMENT_v1.0.toml` (status FROZEN, code-tree pin), run it
  once, reconcile, then update its ledger card and this file.

| Item | Status | Canonical record |
|---|---|---|
| VWR family + IG-AUSTIN-P0 + benchmark | Completed, negative | `studies/vwap-ema9-2026-10/analysis/VWR0_EXP_FINDINGS_2026-10-16.md` |
| Seam-2 report (presentation only) | Accepted; saved fields restored. Earlier report files in the run directory are superseded presentations of the same frozen run | `studies/vwap-ema9-2026-10/exports/runs/VWR0-EXP__20261016T211249Z/report_v2_20261016T233149Z.html` |
| VMR-L (mean reversion) | Proposed; synthetic tests pass; real data not run | `studies/vwap-mr-2026-10/` |
| VWR fresh-data extension | Proposed (38 new sessions, 2026-08-24 → 2026-10-15) | `studies/vwap-ema9-2026-10/manifests/VWR0_FRESH_EXTENSION_v0.1.toml` |
| Data quality (2025-04-23 and other extreme prints) | Unresolved, scope measured | `docs/lab/DATA_QUALITY_2026-10-16.md` |
| Fresh data | Captured: `spy-1m-polygon-20241016-20261015-cap20261016-729dc4e9` | `datasets/REGISTRY.json` |

## Blockers (each needs Dustin)

1. **Off-device backup.** A verified archive is staged at `~/stratlab-backup/` (same disk, so not yet a
   backup). Copy that folder to a USB drive or cloud drive, then, in the copy, run
   `sha256sum -c stratlab-store-2026-10-16.tgz.sha256`.
2. **VMR-L review:** the rules, the variants and the data choice (fresh capture recommended).
3. **Data treatment:** leave as is, adopt mask v2, or buy condition-coded ticks (`docs/lab/DATA_QUALITY_2026-10-16.md`).
4. **Committed vendor export (PR closeout):** the August study committed a TradingView BATS SPY 5m chart-data
   export (`studies/vwap-lab-2026-08/exports/TV_CHARTDATA_BATS_SPY_5m_RTH_2025-08-11_2026-08-25_FastAlphaV0.csv`,
   2.4 MB). It is a frozen August artifact. Decide: keep it, with a provenance/redistribution note, or remove
   it in a new dated commit before merging.

## Resume commands

```bash
cd ~/Projects/strategy-lab && git status --short --branch && git log --oneline -3
uv sync && uv run pytest -q                       # 101 tests; the 2 August-parity tests need the local corpus
uv run stratlab data verify spy-1m-polygon-20241016-20261015-cap20261016-729dc4e9
uv run stratlab identity                          # code-tree hash for freezing a config
# after VMR-L approval: copy the TOML to VMRL_EXPERIMENT_v1.0.toml, set status="FROZEN" and
# code_tree_sha256, commit, push, then:
uv run stratlab run studies/vwap-mr-2026-10/manifests/VMRL_EXPERIMENT_v1.0.toml
uv run python studies/vwap-ema9-2026-10/analysis/reconcile_run.py <run_dir>
```

Market-data key, for probe or capture only: `set -a; . ~/.config/stratlab/credentials.env; set +a` in the
**same** shell command as `stratlab data …`. The key is never printed or logged.

## Rules that bite

- Real-data runs need a **FROZEN** config pinned to the current code tree, with a clean `src/`.
- Run directories and reports are never overwritten. A rebuild gets a new file name.
- **Do not edit the 12 computation modules pinned for VWR0-EXP.** They are listed in `PINNED_MODULES` in
  `src/stratlab/report/present.py` and include `strategies/common.py`. Doing so breaks verified re-presentation of that run. New shared code goes in **new**
  modules (as `volatility.py` did).
- No rescue variants after a negative result. Every configuration evaluated gets a ledger row.
