"""Massive/Polygon-compatible 1-minute aggregates: entitlement probe and capture.

Ported from studies/vwap-lab-2026-08/data/fetch_spy_aggs.py (frozen; not edited), with:
  * any ticker, output to the lab store, capture-stamped names that never overwrite;
  * raw pages saved and hashed AS RECEIVED (the August script re-serialized them);
  * retries with backoff on 429/5xx;
  * a credential guard: the key goes only in the Authorization header, is never printed
    or logged, and every byte about to be written is checked for it (abort if found).
The canonical CSV format is unchanged ("august-canonical-v1"), so `store.read_canonical`
and every check written for the original corpus apply to new captures.

Credential: MASSIVE_API_KEY or POLYGON_API_KEY in the environment (e.g. by sourcing
~/.config/stratlab/credentials.env in the same shell invocation).
"""

from __future__ import annotations

import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_URL = "https://api.polygon.io"
PAGE_LIMIT = 50000
ET = ZoneInfo("America/New_York")
RTH_START, RTH_END = dt.time(9, 30), dt.time(16, 0)
CANONICAL_FIELDS = ["t_ms", "utc_iso", "et_iso", "session", "o", "h", "l", "c", "v", "vw", "n"]


class CredentialError(RuntimeError):
    pass


def api_key() -> str:
    key = os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")
    if not key:
        raise CredentialError("MASSIVE_API_KEY / POLYGON_API_KEY not set (value is never printed)")
    return key


def _redact(text: str, key: str) -> str:
    return text.replace(key, "<redacted>") if key else text


def get_bytes(url: str, key: str, opener=urllib.request.urlopen, retries: int = 5) -> bytes:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    delay = 15.0
    for attempt in range(retries + 1):
        try:
            with opener(req, timeout=120) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(_redact(f"HTTP {e.code} for {url.split('?')[0]}", key)) from None
    raise RuntimeError("unreachable")


def aggs_url(ticker: str, start: str, end: str, base: str = BASE_URL) -> str:
    q = urllib.parse.urlencode({"adjusted": "true", "sort": "asc", "limit": str(PAGE_LIMIT)})
    return f"{base}/v2/aggs/ticker/{ticker}/range/1/minute/{start}/{end}?{q}"


def normalize(results: list[dict]) -> list[dict]:
    """Identical to the August normalize(): bar-start t_ms kept, ET derived, EXT kept."""
    rows = []
    for bar in results:
        t_ms = int(bar["t"])
        utc = dt.datetime.fromtimestamp(t_ms / 1000, tz=dt.timezone.utc)
        et = utc.astimezone(ET)
        rows.append({
            "t_ms": t_ms, "utc_iso": utc.isoformat(), "et_iso": et.isoformat(),
            "session": "RTH" if RTH_START <= et.time() < RTH_END else "EXT",
            "o": bar["o"], "h": bar["h"], "l": bar["l"], "c": bar["c"], "v": bar["v"],
            "vw": bar.get("vw", ""), "n": bar.get("n", ""),
        })
    rows.sort(key=lambda r: r["t_ms"])
    return rows


def canonical_bytes(rows: list[dict]) -> bytes:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CANONICAL_FIELDS)
    w.writeheader()
    w.writerows(rows)
    return gzip.compress(buf.getvalue().encode("utf-8"), mtime=0)


def _describe(results: list[dict]) -> dict:
    fields = sorted(set().union(*(b.keys() for b in results))) if results else []
    iso = lambda ms: dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc).isoformat()
    ts = [int(b["t"]) for b in results]
    return {"row_count": len(results), "fields_present": fields,
            "first_bar_utc": iso(min(ts)) if ts else None, "last_bar_utc": iso(max(ts)) if ts else None}


def _guarded_write(path: Path, data: bytes, key: str) -> str:
    if key and key.encode() in data:
        raise CredentialError(f"refusing to write {path.name}: payload contains the credential")
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def probe(ticker: str, date: str, opener=urllib.request.urlopen) -> dict:
    """One-day request: proves entitlement for that date by behaviour, not documentation."""
    key = api_key()
    payload = json.loads(get_bytes(aggs_url(ticker, date, date), key, opener))
    res = payload.get("results", []) or []
    rth = [b for b in res if RTH_START <= dt.datetime.fromtimestamp(int(b["t"]) / 1000, tz=dt.timezone.utc).astimezone(ET).time() < RTH_END]
    return {"ticker": ticker, "date": date, "status": payload.get("status"),
            "adjusted": payload.get("adjusted"), "rth_bars": len(rth), **_describe(res)}


def capture(ticker: str, start: str, end: str, out_dir: Path, sleep_s: float = 13.0,
            opener=urllib.request.urlopen, now: dt.datetime | None = None) -> dict:
    key = api_key()
    now = now or dt.datetime.now(dt.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%MZ")
    stem = f"{ticker}_1m_{start}_{end}_cap{stamp}"
    out_dir = Path(out_dir)
    raw_dir = out_dir / "raw" / stem
    canon = out_dir / f"{stem}.csv.gz"
    manifest_path = out_dir / f"{stem}.manifest.json"
    for p in (raw_dir, canon, manifest_path):
        if p.exists():
            raise FileExistsError(f"{p} exists; captures never overwrite")
    raw_dir.mkdir(parents=True)
    url, pages, results = aggs_url(ticker, start, end), [], []
    while url:
        body = get_bytes(url, key, opener)
        page_no = len(pages) + 1
        sha = _guarded_write(raw_dir / f"page{page_no:04d}.json", body, key)
        payload = json.loads(body)
        if payload.get("status") not in ("OK", "DELAYED"):
            raise RuntimeError(f"page {page_no}: provider status {payload.get('status')!r}")
        pages.append({"page": page_no, "file": f"raw/{stem}/page{page_no:04d}.json", "sha256": sha,
                      "bytes": len(body), "resultsCount": payload.get("resultsCount"),
                      "status": payload.get("status")})
        results.extend(payload.get("results", []) or [])
        url = payload.get("next_url")
        print(f"page {page_no}: {len(results):,} rows", file=sys.stderr)
        if url:
            time.sleep(sleep_s)
    rows = normalize(results)
    blob = canonical_bytes(rows)
    canon_sha = _guarded_write(canon, blob, key)
    manifest = {
        "provider": "Massive/Polygon-compatible stocks aggregates",
        "endpoint_family": "/v2/aggs/ticker/{ticker}/range/1/minute", "base_url": BASE_URL,
        "ticker": ticker, "interval": "1 minute", "adjusted": True,
        "query_start": start, "query_end": end, "captured_utc": now.isoformat(),
        "timezone_semantics": "t_ms = bar start, epoch ms, UTC; et_iso derived, original t_ms preserved",
        "session_flag_rule": "RTH iff 09:30 <= ET bar start < 16:00; EXT bars kept",
        "raw_hash_semantics": "sha256 of the response bytes exactly as received",
        "format": "august-canonical-v1", "pages": pages,
        "canonical": {"file": canon.name, "sha256": canon_sha, "row_count": len(rows)},
        **_describe(results),
    }
    _guarded_write(manifest_path, json.dumps(manifest, indent=2).encode(), key)
    return {"canonical": str(canon), "sha256": canon_sha, "rows": len(rows), "pages": len(pages),
            "manifest": str(manifest_path), "first_bar_utc": manifest["first_bar_utc"],
            "last_bar_utc": manifest["last_bar_utc"]}
