# PREP — VMR-0 first development run · v0.1 · 2026-08-27 · NOT RUN

Pre-run manifest for the **first VMR development configuration (VMR-0)**. This is a
**PREP / DESIGN** record: the run is **not executed** and **no VMR outcome is
inspected** (owner/HELM charge 2026-08-27, DESIGN ONLY). When separately authorized,
the run is frozen to a `RUN_VMR0_DEV_v1.0.md` first, then executed. Governing family
charter: `VMR_CHARTER_v0.1.md`.

## What this run WILL do (when authorized)

- Implement the smallest engine support for VMR-0 (a new entry rule + a VWAP-target
  exit), additively — `signal_mode="vmr"` alongside `"vdc"`/`"fpc"`, defaults
  unchanged so all prior results stay byte-identical — with deterministic unit tests
  for: extension threshold, the opposing-color reversal, the VWAP-target exit, the
  1×ATR further-extension stop, and symmetry. **(Not done in this DESIGN packet.)**
- Simulate **VMR-0 symmetric** over the development window **2024-09-03 → 2025-12-31**,
  screened (frozen `CORPUS_MASK_v1.0`) **primary**, raw sensitivity.
- Produce the standard tear sheet (`tearsheet.py`) — trades, cumulative R, **mean
  expectancy R (primary)**, net $, PF, win rate, max-DD R, long/short decomposition,
  bootstrap CI, outlier concentration, monthly consistency.
- Report VMR-0 descriptively; VDC symmetric remains available only as an unrelated
  benchmark (VMR is a different hypothesis, not a VDC comparison).
- VMR-specific diagnostics: number of extension events (|E| ≥ K) by side, how many
  produced an entry, distribution of bars-to-target and target-hit vs stop vs EOD
  exit mix.

## VMR-0 mechanics (frozen in the charter; restated for the run)

Metric `E(t) = (close − session_vwap)/ATR14` (§5/§A1.3). Extension `|E| ≥ K`,
**K = 4.091616 ATR** (dev `|E|` P90, screened; trade-blind, frozen — see
`VMR_EXCURSION_PROFILE_2026-08-27.json`). LONG when `E ≤ −K` and green bar; SHORT when
`E ≥ +K` and red bar; enter next open. Target = session VWAP (bar-close reversion,
fill next open); stop = 1×ATR14 further-extension; EOD flatten 15:50; V0 window /
execution / costs. No EMA regime filter. Symmetric. Full spec + ambiguity flags:
`VMR_CHARTER_v0.1.md` §4–§6.

## Firewall (binding)

Development window only. No inspection of the consumed VDC validation window
(2026-01-06 → 2026-04-30), the embargo, the unused historical buffer, the
late-May..Aug hypothesis-source outcomes, or the frozen-forward holdout. No RSI, ADX,
volume, EMA50/55, multi time-of-day, gap, news/macro, CuttingBoard context, multiple
targets, or trailing stops (charter §7). No new confirmation data. No TradingView
dependency, no CuttingBoard contact, no merge.

## Parameter discipline

The only new parameter, **K = 4.0916 ATR**, is distribution-derived (dev `|E|` P90,
screened; raw 4.068) and frozen **before** any VMR outcome — not chosen by inspecting
strategy P/L. All other values reuse frozen definitions (ATR14, close reference,
`ATR_STOP_MULT=1.0`, red/green, window, EOD, slippage, qty). K's quantile is a flagged
HELM lever (charter §6.1).

## Code (pinned; DESIGN artifacts only — no VMR engine yet)

| File | SHA256 |
|---|---|
| `analysis/vmr_excursion_profile.py` | `f354acda6134e200f4f13e75359854f4a489d32db7226129dcc7660d7b931ce6` |
| `analysis/VMR_EXCURSION_PROFILE_2026-08-27.json` | `736e166ca1907c907a5f18ec1a41b7cd3b81733529f4e800749ae20b87287ab6` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`.
The `signal_mode="vmr"` engine support and its tests are authored in the run packet,
not here.

## Budget (§9/§f)

Executing the run spends **VMR configuration 1 of ≤ 8** — VMR-dev **0 → 1/8** — a new
`family=VMR, budget_class=development` ledger row **at execution**. **No draw in this
DESIGN packet.** The VDC (15/18) and FPC (1/12) budgets are **closed** and not
inherited.

## Exact proposed first development-run charge (NOT executed)

> "STRATEGY LAB — VMR-0 FIRST DEVELOPMENT RUN. Implement additive `signal_mode='vmr'`
> in `fastalpha_engine.simulate` (extension |E|≥K with K=4.0916; opposing-color
> reversal; enter next open toward VWAP; exit at session VWAP on bar-close reversion;
> 1×ATR14 further-extension stop; V0 window/EOD/execution; symmetric; no EMA regime
> filter), defaults byte-identical, with deterministic unit tests. Freeze
> `RUN_VMR0_DEV_v1.0.md`, then run VMR-0 over 2024-09-03 → 2025-12-31, screened primary
> + raw. Emit the standard tear sheet: mean expectancy R (primary), long/short
> decomposition, bootstrap CI, outlier concentration, monthly consistency, and
> VMR-specific extension-event / target-hit / exit-mix diagnostics. Classify the
> development effect against a frozen R criterion without selecting a production config.
> Spend VMR config 1/8. Development only — no validation, no holdout, no fresh-window
> confirmation. Commit and push. No merge."

## Amendments

*(append dated amendments here; never edit the text above in place)*
