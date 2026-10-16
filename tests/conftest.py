import pandas as pd
import pytest

from stratlab.data.sessions import ET, assign_regular_sessions, resample_session_bars, session_table
from stratlab.engine import ExecutionConfig, LabStrategy, build_execution_frame, run_backtest


class Scripted(LabStrategy):
    """Test strategy: actions keyed by the ET decision minute 'YYYY-MM-DD HH:MM'."""
    plan: dict = {}

    def on_signal_bar(self):
        key = pd.Timestamp(self.now(), tz="UTC").tz_convert(ET).strftime("%Y-%m-%d %H:%M")
        act = self.plan.get(key)
        if not act:
            return
        kind = act[0]
        if kind in ("buy", "sell"):
            stop = act[1] if len(act) > 1 else None
            target = act[2] if len(act) > 2 else None
            self.enter(1 if kind == "buy" else -1, stop, target, reason="scripted")
        elif kind == "exit":
            self.exit_all("scripted_exit")
        elif kind == "buy_units":
            self.buy(size=act[1], tag=-1)


def make_frame(bars_1m, sessions, signal_minutes=1, flatten_minutes=5, features=None):
    rth = assign_regular_sessions(bars_1m, sessions)
    sig = resample_session_bars(rth, signal_minutes, sessions)
    feats = features(sig) if features else pd.DataFrame(index=sig.index)
    return build_execution_frame(rth, sig, feats, sessions, signal_minutes, flatten_minutes)


def run_plan(bars_1m, sessions, plan, cfg=None, **kw):
    cls = type("ScriptedRun", (Scripted,), {"plan": plan})
    frame = make_frame(bars_1m, sessions, **kw)
    return run_backtest(cls, frame, cfg or ExecutionConfig(cash=10_000, commission_per_share=0.0,
                                                          slippage_per_share=0.0))


def et(ts_utc):
    return pd.Timestamp(ts_utc).tz_convert(ET).strftime("%Y-%m-%d %H:%M")


@pytest.fixture
def one_session():
    return session_table("2025-01-02", "2025-01-02")
