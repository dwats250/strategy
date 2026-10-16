"""Benchmarks: simple reference strategies run through the same engine, capital and costs.

SPY-SESSION-HOLD — every session: when the first 1-minute bar (09:30) completes, buy
99.9% of equity notional; the fill is the 09:31 open. Hold with no stop and no target;
the engine's calendar flatten sells at the 15:55 open (12:55 on early closes). Nothing is
held overnight. Same per-share costs as every strategy. It measures what being long
during the same regular-session hours earned, net of the same costs. It is not a
buy-and-hold benchmark, and it has no R multiple (no stop).
"""

from __future__ import annotations

import pandas as pd

from ..engine import LabStrategy

STRATEGY_ID = "SPY-SESSION-HOLD"


class SessionHold(LabStrategy):
    signal_minutes = 1

    @classmethod
    def build_features(cls, sig, **params):
        return pd.DataFrame({"s_close": sig["Close"]}, index=sig.index)

    def init(self):
        super().init()
        self._entered_session = None

    def on_signal_bar(self):
        sess = self.data.session_code[-1]
        if self._entered_session == sess or self.position or self.has_pending_entry():
            return
        self._entered_session = sess   # one attempt per session, on its first completed minute
        self.enter(1, None, None, reason="session_open")
