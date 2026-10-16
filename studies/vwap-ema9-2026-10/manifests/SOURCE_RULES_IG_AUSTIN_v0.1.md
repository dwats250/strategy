# SOURCE_RULES_IG_AUSTIN v0.1 — source extraction and rule table

**Status:** v0.1, written 2026-10-16 before any real-data run of this interpretation. It goes to
seam-1 review. After review it is frozen as v1.0, or superseded by a versioned file (§b).

## Source

| Field | Value |
|---|---|
| URL | https://www.instagram.com/reel/Dd-ClqHtd-1/ |
| Creator | @austin.daytrades. Marc shared the reel with the lab; Marc is not the author. |
| Posted | 2026-10-01 (upload timestamp 1790895753) |
| Retrieved | 2026-10-16, anonymously (yt-dlp, no login, nothing paid, no contact with the creator) |
| Video | 79.7 s, SHA-256 `10c18b19…6ff6e21`. Stored locally only; third-party content is not committed. |
| Evidence in repo | [`source_evidence_ig_Dd-ClqHtd-1/`](source_evidence_ig_Dd-ClqHtd-1/): caption and metadata, plus a local machine transcript (faster-whisper small.en; not verified word for word) |
| Frames reviewed | 1 fps contact sheet, plus full-resolution stills at t = 1, 19, 22, 35, 40, 44, 47 and 55 s |

**Claimed performance.** The overlay reads "+$179,223.45, Selected Range 09/01/2026 – 09/30/2026". It is
an account P&L screenshot. The lab cannot verify it, and nothing here treats it as evidence about the rules.

## Rule table

Legend: **S** = stated in speech or caption. **V** = visibly demonstrated on screen. **I** = inferred from
what is visible but not stated. **—** = absent.

| Element | Source says / shows | Kind | Ambiguity | Lab assumption for IG-AUSTIN-P0 (provisional) |
|---|---|---|---|---|
| Indicators | "VWAP + EMA9" (caption). "Type in VWAP… select this one. Type in EMA…" (speech) | S, V | — | VWAP and EMA only |
| Timeframe | "one strategy on the three-minute time frame" (speech, 0:00–0:06); "3 MINUTE" overlay | S | — | 3-minute bars |
| VWAP source | "set the source to OHLC-4" (speech); dropdown highlights `(O + H + L + C)/4` (frame t=19 s) | S, V | — | `ohlc4` |
| VWAP anchor | "Set the anchor period to session"; settings show `Anchor Period: Session` | S, V | Whether "session" starts at 04:00 premarket or 09:30 depends on the chart's ETH setting | RTH-anchored (see the session row) |
| VWAP bands | All band checkboxes are unticked | V | — | No bands |
| VWAP "wait for timeframe closes" | Ticked in the settings panel | V | Affects only a higher-timeframe VWAP; irrelevant here | Ignored |
| EMA | "set the length to 9. Set the source to close" | S, V | — | EMA(9) on close; continuous across sessions, RTH bars only |
| Session / hours | The chart axis jumps from the prior day's "02:45 PM" to "08:45 AM" (frames t=47 s, 55 s). This fits an RTH-only chart in US Central time (08:30–15:00 CT = 09:30–16:00 ET). | I | Timezone and ETH setting are not stated | RTH only, 09:30–16:00 ET, calendar early closes |
| Instrument | Not named. Ticker and price scale are cropped out. He trades **options**: "buy calls" / "buy puts". | — | Underlying unknown (SPY, QQQ, SPX or a single stock); option selection (strike, DTE) unknown | **SPY shares** long/short, as an underlying-only proxy. Option P&L is not modelled. |
| Entry event | "Our entry will be right before or right when the VWAP and the EMA cross" | S | "Right before" is anticipatory, entering on the live bar before the cross completes. Not mechanically defined. | Enter after a **completed** 3m bar on which EMA9 crosses VWAP (`ema[t-1] <= vwap[t-1]` and `ema[t] > vwap[t]`), filled at the next 1-minute open. This is systematically later than the creator's anticipatory entry. |
| Direction | Upside cross → "buy calls"; downside cross → "buy puts" | S, V | — | Long on an upside cross, short on a downside cross |
| Demonstrated long | Frames t=35–44 s, "Th 01 Oct '26" around 11:30–12:00 CT: EMA dips under a flat VWAP, then turns up through it; marked "BUY CALLS" | V | The entry is marked while the cross is still forming on the live bar | Consistent with the completed-cross rule, one bar later |
| Demonstrated short | Frame t=47 s, "Mo 28 Sep '26" around 09:24 CT: EMA rolls down through VWAP after an opening drop; marked "BUY PUTS" | V | Same | Same |
| Confirmation filters | None stated. Caption: "EMA9 helps me confirm momentum". | S (vague) | "Confirm momentum" is not a rule | None beyond the cross |
| Exit | Caption: "EMA9 helps me… manage my exits once I'm in the trade". No exit is shown in the video. | S (vague) | No trigger, no target | Exit when a later completed 3m bar **closes back through EMA9** (long: close < EMA9) |
| Stop | — | — | Not stated | Protective stop 1 tick beyond the signal bar's extreme, at least 5 bps from the signal close. Needed for R accounting; it is a lab choice. |
| Sizing | — | — | Not stated. Option sizing is unrelated to share sizing anyway. | Lab default: 99.9% of equity notional, one position at a time |
| Trade frequency / filters | — | — | Not stated | All crosses inside the entry window |
| Time window | — | — | Not stated | Decisions on bars ending 09:33–15:30 ET; flat 5 min before the close |
| Reversal | Implied by calls/puts on alternate crosses | I | Whether he flips immediately is unknown | No same-bar reversal. An exit and a new entry need separate signal bars. |

## What this interpretation is and is not

- **IG-AUSTIN-P0 is a provisional, executable interpretation.** It is not an exact replication and
  must never be labelled one. Every row marked I or — above is the lab's choice.
- It is an **underlying-only proxy**. Long and short SPY shares are not the same payoff as long calls
  and long puts: no convexity, no theta, no IV crush, and no option spreads. A positive or negative
  share result says little about the creator's option P&L.
- The completed-bar entry is **later** than the creator's anticipatory entry. That lag changes the
  edge, if there is one, in an unknown direction.
- No August FastAlpha rule (EMA 9/20, ATR stops, opposing-candle entries, 09:40–15:30 window) has been
  imported as this creator's rule.

## Material ambiguities for seam-1 review

1. **Underlying.** SPY is assumed. QQQ or SPX may be closer, and the lab only has SPY data.
2. **Exit rule.** The three candidates are a close through EMA9 (chosen), the opposite EMA/VWAP cross,
   or the first close back across VWAP. Each implies a very different holding period.
3. **Stop.** The creator gives no stop. Whether a signal-bar stop is acceptable for R accounting, or
   whether P0 should run with no stop and report P&L only, is the reviewer's call.
4. **Anticipatory entry.** The creator enters "right before" the cross completes. A one-minute
   look-inside (entering when the forming 3m bar's provisional EMA/VWAP cross occurs) is possible
   but would be a second interpretation (P1), not a fix.
