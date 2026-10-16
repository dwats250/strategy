import gzip
import hashlib
import json

import pandas as pd
import pytest

from stratlab.data import store
from stratlab.data.sessions import assign_regular_sessions, coverage, resample_session_bars, session_table
from stratlab.data.validate import validate_frame
from stratlab.synthetic import flat_session_bars


def _write_canonical(path, rows):
    text = "t_ms,utc_iso,et_iso,session,o,h,l,c,v,vw,n\n" + "\n".join(rows) + "\n"
    with gzip.open(path, "wt") as f:
        f.write(text)
    return hashlib.sha256(path.read_bytes()).hexdigest()



def test_resolve_fails_closed_on_sha_mismatch(tmp_path, monkeypatch):
    p = tmp_path / "X.csv.gz"
    _write_canonical(p, ["1735828200000,a,b,RTH,1,1,1,1,10,1,1"])
    rec = store.DatasetRecord("x", "X.csv.gz", "0" * 64, 1, "august-canonical-v1", {"known_locations": []})
    monkeypatch.setenv("STRATLAB_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(store, "DEFAULT_STORE", tmp_path / "nowhere")
    with pytest.raises(store.DatasetError, match="MISMATCH"):
        store.resolve("x", {"x": rec})


def test_resolve_and_read_good_file(tmp_path, monkeypatch):
    p = tmp_path / "X.csv.gz"
    sha = _write_canonical(p, ["1735828200000,a,b,RTH,1,2,0.5,1.5,10,1.2,3"])
    rec = store.DatasetRecord("x", "X.csv.gz", sha, 1, "august-canonical-v1", {"known_locations": []})
    monkeypatch.setenv("STRATLAB_DATA_DIR", str(tmp_path))
    r, path = store.resolve("x", {"x": rec})
    df = store.read_canonical(path, r.format)
    assert df.index[0] == pd.Timestamp("2025-01-02 14:30", tz="UTC")
    assert df.iloc[0].tolist()[:5] == [1, 2, 0.5, 1.5, 10]


def test_session_assignment_excludes_extended_hours_and_auction_minute():
    s = session_table("2024-12-24", "2024-12-24")
    idx = pd.date_range("2024-12-24 08:00", "2024-12-24 18:00", freq="1min", tz="America/New_York").tz_convert("UTC")
    bars = pd.DataFrame({"Open": 1.0, "High": 1.0, "Low": 1.0, "Close": 1.0, "Volume": 1.0}, index=idx)
    rth = assign_regular_sessions(bars, s)
    assert len(rth) == 210
    et = rth.index.tz_convert("America/New_York")
    assert et[0].strftime("%H:%M") == "09:30" and et[-1].strftime("%H:%M") == "12:59"


def test_resample_anchored_complete_and_flags_missing():
    s = session_table("2025-01-02", "2025-01-02")
    b = flat_session_bars(s).drop(pd.Timestamp("2025-01-02 09:37", tz="America/New_York").tz_convert("UTC"))
    rth = assign_regular_sessions(b, s)
    b5 = resample_session_bars(rth, 5, s)
    assert len(b5) == 78
    assert b5.complete.sum() == 77 and b5.iloc[1].n_1m == 4
    b3 = resample_session_bars(rth, 3, s)
    assert len(b3) == 130
    cov = coverage(rth, s)
    assert int(cov.missing.iloc[0]) == 1


def test_validate_frame_counts_problems():
    s = session_table("2025-01-02", "2025-01-03")
    b = flat_session_bars(s)
    b.iloc[5, b.columns.get_loc("High")] = 0.5       # OHLC violation
    b = pd.concat([b, b.iloc[[10]]]).sort_index()      # duplicate
    rep = validate_frame(b)
    assert rep["duplicate_timestamps"] == 1
    assert rep["ohlc_violations"] == 1
    assert rep["sessions_not_starting_0930_et"] == []


def test_replaced_file_is_rejected_even_with_same_size_and_mtime(tmp_path, monkeypatch):
    import os
    p = tmp_path / "X.csv.gz"
    sha = _write_canonical(p, ["1735828200000,a,b,RTH,1,2,0.5,1.5,10,1.2,3"])
    rec = store.DatasetRecord("x", "X.csv.gz", sha, 1, "august-canonical-v1", {"known_locations": []})
    monkeypatch.setenv("STRATLAB_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(store, "DEFAULT_STORE", tmp_path / "nowhere")
    store.resolve("x", {"x": rec})
    st = p.stat()
    _write_canonical(p, ["1735828200000,a,b,RTH,1,2,0.5,9.5,10,1.2,3"])
    os.utime(p, (st.st_atime, st.st_mtime))
    with pytest.raises(store.DatasetError, match="MISMATCH"):
        store.resolve("x", {"x": rec})
