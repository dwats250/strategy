"""Offline tests of the capture seam (no network, no credential)."""
import gzip
import importlib.util
import io
import json

import pytest

from stratlab.data import polygon
from stratlab.data.store import REPO_ROOT, read_canonical

FIXTURE = REPO_ROOT / "studies/vwap-lab-2026-08/data/fixtures/sample_aggs_response.json"


def _august():
    spec = importlib.util.spec_from_file_location("fa", REPO_ROOT / "studies/vwap-lab-2026-08/data/fetch_spy_aggs.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_normalize_and_canonical_bytes_match_the_august_script(tmp_path):
    payload = json.loads(FIXTURE.read_text())
    fa = _august()
    old_rows = fa.normalize(payload["results"])
    new_rows = polygon.normalize(payload["results"])
    assert new_rows == old_rows
    old_path = tmp_path / "old.csv.gz"
    old_sha = fa.write_canonical_csv_gz(str(old_path), old_rows)
    assert polygon.canonical_bytes(new_rows) == old_path.read_bytes()
    df = read_canonical(io.BytesIO(polygon.canonical_bytes(new_rows)), "august-canonical-v1")
    assert len(df) == len(new_rows)


class _Resp:
    def __init__(self, body): self.body = body
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def read(self): return self.body


def test_capture_paginates_hashes_raw_bytes_and_never_overwrites(tmp_path, monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "TESTKEY123")
    payload = json.loads(FIXTURE.read_text())
    r = payload["results"]
    p1 = json.dumps({"status": "OK", "resultsCount": 6, "results": r[:6], "next_url": "https://api.polygon.io/next?cursor=abc"}).encode()
    p2 = json.dumps({"status": "OK", "resultsCount": len(r) - 6, "results": r[6:]}).encode()
    seen = []
    def opener(req, timeout):
        seen.append(req)
        assert req.get_header("Authorization") == "Bearer TESTKEY123"
        assert "TESTKEY123" not in req.full_url
        return _Resp(p1 if len(seen) == 1 else p2)
    import datetime as dt
    now = dt.datetime(2026, 10, 16, 21, 45, tzinfo=dt.timezone.utc)
    out = polygon.capture("SPY", "2026-08-03", "2026-08-03", tmp_path, sleep_s=0, opener=opener, now=now)
    assert out["rows"] == len(r) and out["pages"] == 2
    man = json.loads((tmp_path / "SPY_1m_2026-08-03_2026-08-03_cap20261016T2145Z.manifest.json").read_text())
    import hashlib
    assert man["pages"][0]["sha256"] == hashlib.sha256(p1).hexdigest()   # as received
    for f in tmp_path.rglob("*"):
        if f.is_file():
            assert b"TESTKEY123" not in f.read_bytes()
    with pytest.raises(FileExistsError):
        polygon.capture("SPY", "2026-08-03", "2026-08-03", tmp_path, sleep_s=0, opener=opener, now=now)


def test_payload_containing_the_key_is_never_written(tmp_path, monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "TESTKEY123")
    leaky = json.dumps({"status": "OK", "results": [], "next_url": "https://x/?apiKey=TESTKEY123"}).encode()
    with pytest.raises(polygon.CredentialError):
        polygon.capture("SPY", "2026-08-03", "2026-08-03", tmp_path, sleep_s=0,
                        opener=lambda req, timeout: _Resp(leaky))
    assert not any(p.is_file() for p in tmp_path.rglob("*"))


def test_missing_credential_fails_without_printing_anything(monkeypatch, capsys):
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    with pytest.raises(polygon.CredentialError):
        polygon.api_key()
