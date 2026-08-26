# PARITY GATES — VDC Fast Alpha v0 local reproduction · status record

Created 2026-08-25 (dated status entries only; append, don't rewrite). Three gates
separate what the local foundation can and cannot claim. **No gate being open blocks
TradingView R0 capture; every gate being closed is required before any local backtest
result could ever substitute for TradingView evidence.**

> **Status header convention:** the headline states after each gate title are the
> original 2026-08-25 creation states; current status is the most recent dated entry
> inside each gate section.

## Gate 1 — DATA / BAR PARITY: `PENDING`

Do the locally reconstructed Massive 5-minute OHLCV bars match the actual TradingView
chart bars used for R0? **Not assumed.** The recent authoritative TradingView experiment
was identified as `BATS:SPY`; Massive/Polygon stock aggregates may represent a
different/consolidated feed, so exact OHLC — and especially **VOLUME** — may differ.
Because VDC session VWAP is volume-sensitive, feed mismatch can produce legitimate
signal differences. **Never classify such differences as code defects before bar parity
is checked.** Open sub-item: shortened-session 211-bar behavior and the terminal partial
5-minute bucket vs TradingView early-close bars.

**2026-08-25 — R0 ingest + parity pass → `PARTIAL — FEED-CHARACTERIZED; AMEX-CHART BAR
PARITY STILL OPEN`.** Compared local reconstruction against the preserved TV 5m
chart-data export (`exports/TV_CHARTDATA_BATS_SPY_5m_RTH_2025-08-11_2026-08-25_FastAlphaV0.csv`,
**BATS-chart provenance**, no volume column) on the development-window overlap
2025-08-11 → 2025-12-31 (100 sessions, 7,728 TV bars); rows after 2025-12-31 dropped
uninspected (validation firewall). Results (`analysis/R0_PARITY_RESULTS_2026-08-25.json`):
timestamp alignment exact — 0 TV bars missing locally, 2 local-only bars, both the
13:00 terminal partial bucket on early closes 2025-11-28 / 2025-12-24 (classified
**resampling/session difference**, the pre-registered sub-item above). Raw OHLC differs
by a stepwise-constant ratio with steps exactly at SPY ex-dividend dates 2025-09-19 and
2025-12-19 (segment ratios 0.98904 / 0.99178 / 0.99471): classified **source/feed —
dividend adjustment** (TV ADJ vs split-only local corpus), not a defect. After
per-segment ratio normalization: highs/lows match to ~5e-9 median (essentially exact);
opens/closes median |diff| ≈ half a cent, 98.3–99.6% within 5¢ — classified
**source/feed — venue prints** (BATS chart vs consolidated corpus). VOLUME:
**UNAVAILABLE** — the chart export carries no volume column. Bar parity against the
actual R0 chart (AMEX:SPY) remains **OPEN**: this artifact is from a different chart.
No local implementation defect demonstrated; no parity code changed.

## Gate 2 — SEMANTIC / FEATURE PARITY: `LOCALLY VERIFIED / TV CONFIRMATION PENDING`

Given identical 5-minute OHLCV input bars, does local code reproduce session VWAP, EMA9,
EMA20, ATR14, state, and trigger per Pine semantics? Local status (2026-08-25):
`analysis/parity_foundation.py` implements the exact source mechanics (manual 5m-hlc3
session VWAP with per-session reset; continuous cross-session EMA/ATR over the RTH-only
sequence; entry-window/bar-color/doji rules), verified by the deterministic tests in
`analysis/test_parity_foundation.py` (9/9 pass). EMA/RMA/ATR recurrences and SMA seeding
follow the published Pine reference pseudocode; **exact TradingView initialization /
warm-up / float behavior remains unconfirmed against TV output — this gate does not
reach full PARITY until compared with TradingView evidence.**

**2026-08-25 — first TV comparison → `CORROBORATED ON BATS CHART DATA — RESIDUALS
CLASSIFIED SOURCE/FEED; NO DEFECT DEMONSTRATED`.** Same overlap and firewall as the
Gate 1 entry. After dividend-ratio normalization and skipping the first 5 overlap
sessions (the TV chart's own EMA warm-up starts at its 2025-08-11 history edge —
classified **initialization/warmup**, handled by exclusion): EMA9 median |diff| ≈ $0.002,
96.6% of 7,338 bars within 1¢; EMA20 median ≈ $0.0015, 97.2% within 1¢ — residuals
propagate from venue close differences, classified **source/feed**. Session VWAP median
|diff| ≈ $0.030, 96.9% within 25¢ — larger than OHLC as expected because the TV value is
weighted by that chart's (BATS) venue volume vs consolidated local volume; classified
**source/feed — volume weights** (a defect cannot be fully excluded until same-feed
volume is available, but magnitude and shape are consistent with the weight seam and the
local mechanics remain test-verified). Semantic signals: TV plotted signals are
flat-gated; testable implication TV=1 ⇒ local candidate=1 holds 203/208 long (97.6%) and
172/181 short (95.0%); all inspected failures sit at decision boundaries (close-vs-VWAP
sign within ~5¢, or bar-color flip from venue open/close prints) — classified
**source/feed**. No parity logic was modified.

## Gate 3 — EXECUTION / BROKER-EMULATOR PARITY: `PENDING R0 TRADE-LIST EXPORT`

Entry fills, slippage, ATR-stop placement/fills, same-bar stop behavior, thesis-exit
order/fill timing, EOD immediate fill, early-close session handling (no 15:50 bar
exists on shortened sessions, so the source's EOD flatten never fires there), pending-
order interactions with `flat`, trade sequence, and P/L. **No emulator is implemented
and none may be built under the current charge.** Nothing local claims execution parity.

**2026-08-25 — R0 trade-list probe → `PROBED — SIGNAL-BAR CORRESPONDENCE 96.0%; NO
EMULATOR BUILT; EXECUTION PARITY NOT CLAIMED`.** The preserved R0 List-of-Trades export
(`exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv`, 1,331 trades)
reproduces the owner-observed benchmark exactly (asserted by
`analysis/parity_r0_pass.py`: net +$25.69, PF 1.0401, 295/1331 = 22.16%, long +$43.68,
short −$17.99; closed-trade cumulative max DD $46.31 vs TV's $47.07 equity metric).
Smallest execution-parity probe, full development window: every entry fill maps to an
existing local 5m signal bar (fill − 5min; 1331/1331), entry fills span 09:40–15:30 ET
exactly as the source's window+next-bar semantics require, and the local flat-agnostic
candidate flag matches the entry side on 1,278/1,331 (96.0%; long 671/697, short
607/634). The 53 misses inspected are boundary cases (close-vs-VWAP within a few cents,
EMA gap near zero, or bar-color/doji flips) — classified **source/feed at decision
boundaries**, not local defects. Cross-feed observation: of 392 entries in the
chart-data overlap, 388 (99.0%) coincide with the BATS chart's own flat-gated signal
flags — the feed seam moves ~1% of signals. Stops, thesis-exit timing, fills, slippage,
and P/L remain unverified locally; the gate stays short of parity by design.
