"""VWR — VWAP touch-and-reclaim research family (lab-defined, not sourced from anyone).

One completed signal bar decides. For a LONG on bar t (shorts mirror it):
  context       close_t > VWAP_t                      price holds above session VWAP
  trigger       touch_reclaim: low_t <= VWAP_t        the bar traded at/through VWAP
                ema_vwap_cross: EMA_{t-1} <= VWAP_{t-1} and EMA_t > VWAP_t
  confirmation  (if ema_confirm) close_t > EMA_t      momentum confirmed by EMA9
  stop          min(low_t - 1 tick, close_t - stop_floor_bps)
  exit          ema_close:  a later completed bar closes below EMA_t'
                fixed_r:    target = close_t + target_r * (close_t - stop); no EMA exit
  window        entries only when the bar ENDS within [entry_start, entry_end] ET
Always: one position at a time, fills at the next minute's open, flat 5 min before the
session close (calendar close, so early closes are respected), no new entry on a signal
bar with missing minutes, and no EMA/VWAP cross on a session's first bar.
"""

from __future__ import annotations

import numpy as np

from ..engine import LabStrategy
from .common import hhmm_to_min, vwap_ema_features

STRATEGY_ID = "VWR"


class VwapReclaim(LabStrategy):
    signal_minutes = 5
    vwap_source = "hlc3"
    ema_length = 9
    trigger = "touch_reclaim"      # | "ema_vwap_cross"
    ema_confirm = True
    exit_mode = "ema_close"        # | "fixed_r"
    target_r = 2.0
    entry_start = "09:45"
    entry_end = "15:30"
    stop_floor_bps = 5.0
    tick = 0.01

    @classmethod
    def build_features(cls, sig, **params):
        p = {k: params.get(k, getattr(cls, k)) for k in ("vwap_source", "ema_length")}
        return vwap_ema_features(sig, p["vwap_source"], int(p["ema_length"]))

    def _setup(self, side: int) -> bool:
        c, lo, hi = self.f("s_close"), self.f("s_low"), self.f("s_high")
        v, e = self.f("vwap"), self.f("ema")
        if side > 0:
            context = c > v
            if self.trigger == "touch_reclaim":
                trig = lo <= v
            else:
                trig = self.f("ema_prev") <= self.f("vwap_prev") and e > v
            confirm = (c > e) if self.ema_confirm else True
        else:
            context = c < v
            if self.trigger == "touch_reclaim":
                trig = hi >= v
            else:
                trig = self.f("ema_prev") >= self.f("vwap_prev") and e < v
            confirm = (c < e) if self.ema_confirm else True
        return bool(context and trig and confirm)

    def on_signal_bar(self):
        c, e, v = self.f("s_close"), self.f("ema"), self.f("vwap")
        if np.isnan(e) or np.isnan(v):
            return
        if self.position:
            if self.exit_mode == "ema_close":
                if (self.position.is_long and c < e) or (self.position.is_short and c > e):
                    self.exit_all("ema_close_through")
            return
        if self.has_pending_entry() or not self.signal_bar_complete():
            return
        if self.trigger == "ema_vwap_cross" and (np.isnan(self.f("ema_prev")) or np.isnan(self.f("vwap_prev"))):
            return
        t = self.f("sig_end_et_min")
        if not (hhmm_to_min(self.entry_start) <= t <= hhmm_to_min(self.entry_end)):
            return
        floor = c * self.stop_floor_bps / 1e4
        for side in (1, -1):
            if self._setup(side):
                if side > 0:
                    stop = round(min(self.f("s_low") - self.tick, c - floor), 2)
                else:
                    stop = round(max(self.f("s_high") + self.tick, c + floor), 2)
                target = None
                if self.exit_mode == "fixed_r":
                    target = round(c + side * self.target_r * abs(c - stop), 2)
                self.enter(side, stop, target, reason=f"{self.trigger}{'+ema' if self.ema_confirm else ''}")
                return
