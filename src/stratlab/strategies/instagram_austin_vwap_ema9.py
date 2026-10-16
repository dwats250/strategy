"""IG-AUSTIN-P0 — PROVISIONAL executable interpretation of an Instagram reel.

Source: https://www.instagram.com/reel/Dd-ClqHtd-1/ by @austin.daytrades (shared with
the lab by Marc; Marc is not the author). Source evidence and the rule table are in
studies/vwap-ema9-2026-10/manifests/SOURCE_RULES_IG_AUSTIN_v0.1.md.

This is NOT an exact replication. The source states the chart settings and an entry
idea; it does not state the instrument, stop, exit trigger, sizing or session rules,
and the creator trades options. Everything marked ASSUMED below is the lab's choice.

Stated in the source (spoken + on-screen settings):
  * 3-minute chart; VWAP source OHLC4, anchor Session; EMA length 9, source close.
  * Entry "right before or right when the VWAP and the EMA cross"; calls on an upside
    cross, puts on a downside cross.
Visible in the source (inferred, not stated): RTH-only chart (axis jumps from the prior
day's 2:45 PM to 8:45 AM, consistent with Central-time 08:30-15:00 RTH).
ASSUMED here:
  * Underlying-only proxy on SPY shares/short shares (options not modelled).
  * Entry when a COMPLETED 3m bar shows the EMA9 crossing VWAP, filled at the next
    minute's open (the creator anticipates the cross on the live bar; this is later).
  * Exit when a later completed 3m bar closes back through EMA9 ("EMA9 manages exits").
  * Protective stop beyond the signal bar's extreme (min 5 bps from the signal close),
    so trades have a defined initial risk for R accounting.
  * No cross is evaluated on a session's FIRST 3m bar (the previous bar belongs to the
    prior session, and VWAP has just reset), so the earliest decision is the bar ending
    09:36. Entries on bars ending up to 15:30 ET; flat 5 minutes before the close.
  * No new entry on a signal bar with missing minutes (e.g. a masked bad print).
"""

from __future__ import annotations

import numpy as np

from ..engine import LabStrategy
from .common import hhmm_to_min, vwap_ema_features

STRATEGY_ID = "IG-AUSTIN-P0"
LABEL = "PROVISIONAL interpretation — not an exact replication"


class InstagramAustinVwapEma9P0(LabStrategy):
    signal_minutes = 3
    vwap_source = "ohlc4"
    ema_length = 9
    entry_start = "09:36"
    entry_end = "15:30"
    stop_floor_bps = 5.0
    tick = 0.01

    @classmethod
    def build_features(cls, sig, **params):
        p = {k: params.get(k, getattr(cls, k)) for k in ("vwap_source", "ema_length")}
        return vwap_ema_features(sig, p["vwap_source"], int(p["ema_length"]))

    def on_signal_bar(self):
        close, ema_, vwap = self.f("s_close"), self.f("ema"), self.f("vwap")
        ema_p, vwap_p = self.f("ema_prev"), self.f("vwap_prev")
        if np.isnan(ema_) or np.isnan(vwap):
            return
        # Exit management first.
        if self.position:
            if (self.position.is_long and close < ema_) or (self.position.is_short and close > ema_):
                self.exit_all("ema9_close_through")
            return
        if self.has_pending_entry() or not self.signal_bar_complete():
            return
        if np.isnan(ema_p) or np.isnan(vwap_p):
            return  # first bar of a session: no cross against a freshly reset VWAP
        t = self.f("sig_end_et_min")
        if not (hhmm_to_min(self.entry_start) <= t <= hhmm_to_min(self.entry_end)):
            return
        floor = close * self.stop_floor_bps / 1e4
        if ema_p <= vwap_p and ema_ > vwap:
            stop = min(self.f("s_low") - self.tick, close - floor)
            self.enter(1, round(stop, 2), reason="ema9_cross_up_vwap")
        elif ema_p >= vwap_p and ema_ < vwap:
            stop = max(self.f("s_high") + self.tick, close + floor)
            self.enter(-1, round(stop, 2), reason="ema9_cross_down_vwap")
