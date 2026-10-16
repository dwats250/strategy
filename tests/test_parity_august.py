"""Local-only: lab indicators vs the August parity_foundation implementation on the
original corpus. Skipped when the corpus is not available (e.g. CI)."""
import importlib.util

import numpy as np
import pandas as pd
import pytest

from stratlab.data.store import DatasetError, REPO_ROOT, load_dataset, resolve
from stratlab.data.sessions import assign_regular_sessions, resample_session_bars, session_table
from stratlab.indicators import ema, session_vwap

DS = "spy-1m-polygon-20240901-20260822-a4afaa70"


@pytest.fixture(scope="module")
def corpus():
    try:
        _, path = resolve(DS)
    except DatasetError:
        pytest.skip("original corpus not available locally")
    return path


def test_vwap_and_ema9_match_august_implementation(corpus):
    spec = importlib.util.spec_from_file_location(
        "pf", REPO_ROOT / "studies/vwap-lab-2026-08/analysis/parity_foundation.py")
    pf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pf)
    old_bars = pf.build_5m_bars(pf.load_corpus_rth(str(corpus)))
    # August keeps a 1-minute 13:00 bucket on half days (TradingView does not); drop it
    # so both implementations see the same bar sequence.
    old_bars = [b for b in old_bars if not (b["hm"] == 1300 and b["constituent_count"] == 1)]
    old = pd.DataFrame(pf.compute_features(old_bars))

    df, _ = load_dataset(DS)
    s = session_table(df.index[0], df.index[-1])
    b5 = resample_session_bars(assign_regular_sessions(df, s), 5, s)
    assert len(b5) == len(old)
    new_vwap = session_vwap(b5, "hlc3").to_numpy()
    new_ema = ema(b5["Close"], 9).to_numpy()
    np.testing.assert_allclose(new_vwap, old["session_vwap"].astype(float).to_numpy(), rtol=0, atol=1e-9)
    o = old["ema9"].astype(float).to_numpy()
    assert np.isnan(new_ema[:8]).all()
    np.testing.assert_allclose(new_ema[8:], o[8:], rtol=0, atol=1e-9)
