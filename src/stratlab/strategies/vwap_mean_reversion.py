"""VMR-L — VWAP mean-reversion family (lab-defined, 2026-10). PROPOSED; see
studies/vwap-mr-2026-10/manifests/VMRL_FAMILY_PROPOSAL_v0.1.md.

Displacement metric (the August VMR primitive, reused as a definition, not its threshold):
    E_t = (close_t - VWAP_t) / ATR14_t      VWAP session-anchored (hlc3), ATR Wilder, 5m bars

For a LONG decided on completed bar t (shorts mirror it):
  extension     E_{t-1} <= -K          the previous bar closed far below VWAP
                (variant "extension_only": E_t <= -K on the decision bar itself)
  failed ext.   low_t > low_{t-1} and close_t > close_{t-1}
                the bar did not extend further and closed back toward VWAP
  shock filter  (variant only) min |E| over the up-to-6 in-session bars before the extended
                bar < 1.0: the displacement arrived quickly from near VWAP
  stop          min(low_{t-1}, low_t) - 1 tick, at least 5 bps from close_t
                (beyond the failed extreme: a new extreme refutes "failed extension")
  exit          vwap_close: a later completed bar closes at/through VWAP (fill next open)
                half_target: a fixed target placed at entry halfway from close_t to VWAP_t
  window        entries for bars ending 10:00-15:00 ET; flat 5 min before the close
One position at a time, no cooldown: after any exit, a new entry may be taken on the next
qualifying bar, including on the same displacement. No new entry on a bar with missing
minutes; exits are evaluated on every later signal bar. Fills at the next minute's open.
K is a pre-declared number, frozen in the experiment config.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..engine import LabStrategy
from ..indicators import session_vwap
from ..volatility import atr_wilder
from .common import hhmm_to_min

STRATEGY_ID = "VMR-L"


def mr_features(sig: pd.DataFrame, vwap_source: str = "hlc3", atr_length: int = 14,
                shock_lookback: int = 6) -> pd.DataFrame:
    f = pd.DataFrame(index=sig.index)
    for c, n in (("Open", "s_open"), ("High", "s_high"), ("Low", "s_low"), ("Close", "s_close")):
        f[n] = sig[c]
    f["vwap"] = session_vwap(sig, vwap_source)
    f["atr"] = atr_wilder(sig, atr_length)
    f["E"] = (f["s_close"] - f["vwap"]) / f["atr"]
    g = sig["session"]
    f["E_prev"] = f["E"].groupby(g).shift(1)
    f["low_prev"] = f["s_low"].groupby(g).shift(1)
    f["high_prev"] = f["s_high"].groupby(g).shift(1)
    f["close_prev"] = f["s_close"].groupby(g).shift(1)
    absE = f["E"].abs()
    # min |E| over the `shock_lookback` bars BEFORE the previous (extended) bar, same session
    # (uses however many in-session bars exist, up to `shock_lookback`; NaN only when none do)
    f["minabsE_before_prev"] = absE.groupby(g).transform(
        lambda s: s.shift(2).rolling(shock_lookback, min_periods=1).min())
    # ... and before the current bar (for the extension_only variant)
    f["minabsE_before_cur"] = absE.groupby(g).transform(
        lambda s: s.shift(1).rolling(shock_lookback, min_periods=1).min())
    return f


class VwapMeanReversion(LabStrategy):
    signal_minutes = 5
    vwap_source = "hlc3"
    atr_length = 14
    k = float("nan")              # REQUIRED: frozen in the experiment config
    trigger = "failed_extension"  # | "extension_only"
    shock_filter = False
    shock_lookback = 6
    shock_near = 1.0
    exit_mode = "vwap_close"      # | "half_target"
    entry_start = "10:00"
    entry_end = "15:00"
    stop_floor_bps = 5.0
    tick = 0.01

    @classmethod
    def build_features(cls, sig, **params):
        p = {k: params.get(k, getattr(cls, k)) for k in ("vwap_source", "atr_length", "shock_lookback")}
        return mr_features(sig, p["vwap_source"], int(p["atr_length"]), int(p["shock_lookback"]))

    def init(self):
        super().init()
        if not np.isfinite(self.k) or self.k <= 0:
            raise ValueError("VwapMeanReversion needs a positive, pre-declared k (ATR units)")

    def _signal(self, side: int):
        """Return the stop price if a `side` entry is signalled on this bar, else None."""
        c, lo, hi = self.f("s_close"), self.f("s_low"), self.f("s_high")
        if self.trigger == "failed_extension":
            e_ext, ref_low, ref_high = self.f("E_prev"), self.f("low_prev"), self.f("high_prev")
            if np.isnan(e_ext) or np.isnan(ref_low):
                return None
            if side > 0:
                ok = e_ext <= -self.k and lo > ref_low and c > self.f("close_prev")
            else:
                ok = e_ext >= self.k and hi < ref_high and c < self.f("close_prev")
            shock_ref = self.f("minabsE_before_prev")
        else:  # extension_only
            e_ext = self.f("E")
            ref_low, ref_high = lo, hi
            ok = (e_ext <= -self.k) if side > 0 else (e_ext >= self.k)
            shock_ref = self.f("minabsE_before_cur")
        if not ok:
            return None
        if self.shock_filter and not (shock_ref < self.shock_near):
            return None
        floor = c * self.stop_floor_bps / 1e4
        if side > 0:
            return round(min(min(lo, ref_low) - self.tick, c - floor), 2)
        return round(max(max(hi, ref_high) + self.tick, c + floor), 2)

    def on_signal_bar(self):
        c, v = self.f("s_close"), self.f("vwap")
        if np.isnan(v) or np.isnan(self.f("atr")):
            return
        if self.position:
            if self.exit_mode == "vwap_close":
                if (self.position.is_long and c >= v) or (self.position.is_short and c <= v):
                    self.exit_all("vwap_reached")
            return
        if self.has_pending_entry() or not self.signal_bar_complete():
            return
        t = self.f("sig_end_et_min")
        if not (hhmm_to_min(self.entry_start) <= t <= hhmm_to_min(self.entry_end)):
            return
        for side in (1, -1):
            stop = self._signal(side)
            if stop is None:
                continue
            target = None
            if self.exit_mode == "half_target":
                target = round(c + 0.5 * (v - c), 2)
                if (side > 0 and target <= c) or (side < 0 and target >= c):
                    return  # already at/through VWAP: no reversion room
            self.enter(side, stop, target, reason=self.trigger + ("+shock" if self.shock_filter else ""),
                       E_signal=float(self.f("E")), k=float(self.k))
            return
