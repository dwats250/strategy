#!/usr/bin/env python3
"""Minimal deterministic SPY intraday aggregate acquisition seam.

Provider: Massive / Polygon-compatible Stocks Aggregates API (consolidated U.S.
aggregates). This is MARKET-DATA INFRASTRUCTURE for the VWAP Strategy Lab — it is
not strategy evidence, computes no strategy or PVAE outcome, and runs no backtest.

Credential: MASSIVE_API_KEY or POLYGON_API_KEY in the environment. Sent only as an
Authorization header; never printed, never written to any output file.

Entitlement is verified by API behavior (`probe`), never assumed from docs.

Commands:
  probe    --date YYYY-MM-DD          one-day SPY 1m entitlement probe (read-only)
  capture  --start YYYY-MM-DD --end YYYY-MM-DD
                                      paginated capture -> raw pages + canonical
                                      CSV.gz + metadata manifest, all under cache/
  selftest                            offline: normalize + 5m-resample the synthetic
                                      fixture and assert exact expected values

Stdlib only. Canonical format is CSV.gz (this repo's studies track CSV exports;
Parquet would add a dependency for no current consumer).
"""

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

BASE_URL_DEFAULT = "https://api.polygon.io"
TICKER = "SPY"
PAGE_LIMIT = 50000
RATE_LIMIT_SLEEP_S = 13  # free tier: 5 requests/min; stay under it
ET = ZoneInfo("America/New_York")
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
FIXTURE = os.path.join(HERE, "fixtures", "sample_aggs_response.json")

RTH_START = dt.time(9, 30)
RTH_END = dt.time(16, 0)  # bar-start convention: RTH iff 09:30 <= start < 16:00 ET

CANONICAL_FIELDS = [
    "t_ms", "utc_iso", "et_iso", "session", "o", "h", "l", "c", "v", "vw", "n",
]


def api_key():
    key = os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")
    if not key:
        sys.exit("DATA CREDENTIAL / ENTITLEMENT UNAVAILABLE: set MASSIVE_API_KEY "
                 "or POLYGON_API_KEY. This tool never prints or stores the key.")
    return key


def get_json(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def aggs_url(base, start, end):
    path = f"/v2/aggs/ticker/{TICKER}/range/1/minute/{start}/{end}"
    query = urllib.parse.urlencode(
        {"adjusted": "true", "sort": "asc", "limit": str(PAGE_LIMIT)})
    return f"{base}{path}?{query}"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def normalize(results):
    """Provider aggregate rows -> canonical rows. Keeps every bar; extended-hours
    bars are flagged EXT, never deleted, so RTH filtering stays an analysis-time
    decision with the original timestamp preserved."""
    rows = []
    for bar in results:
        t_ms = int(bar["t"])  # bar START, epoch ms, UTC
        utc = dt.datetime.fromtimestamp(t_ms / 1000, tz=dt.timezone.utc)
        et = utc.astimezone(ET)
        session = "RTH" if RTH_START <= et.time() < RTH_END else "EXT"
        rows.append({
            "t_ms": t_ms,
            "utc_iso": utc.isoformat(),
            "et_iso": et.isoformat(),
            "session": session,
            "o": bar["o"], "h": bar["h"], "l": bar["l"], "c": bar["c"],
            "v": bar["v"],
            "vw": bar.get("vw", ""),   # vendor per-bar VWAP; NOT TV session VWAP
            "n": bar.get("n", ""),     # transaction count, if provided
        })
    rows.sort(key=lambda r: r["t_ms"])
    return rows


def resample_5m(rows):
    """1m -> 5m feasibility reconstruction, ET-wall-clock aligned buckets.
    o=first, h=max, l=min, c=last, v=sum, n=sum, vw=volume-weighted vendor vw."""
    buckets = {}
    for r in rows:
        et = dt.datetime.fromisoformat(r["et_iso"])
        start = et.replace(minute=et.minute - et.minute % 5, second=0, microsecond=0)
        buckets.setdefault(start, []).append(r)
    out = []
    for start in sorted(buckets):
        rs = buckets[start]
        vol = sum(float(r["v"]) for r in rs)
        vw_num = sum(float(r["vw"]) * float(r["v"]) for r in rs if r["vw"] != "")
        out.append({
            "et_iso": start.isoformat(),
            "session": rs[0]["session"],
            "o": rs[0]["o"],
            "h": max(float(r["h"]) for r in rs),
            "l": min(float(r["l"]) for r in rs),
            "c": rs[-1]["c"],
            "v": vol,
            "vw": (vw_num / vol) if vol > 0 else "",
            "n": sum(int(r["n"]) for r in rs if r["n"] != ""),
            "bars": len(rs),
        })
    return out


def write_canonical_csv_gz(path, rows):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CANONICAL_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    data = gzip.compress(buf.getvalue().encode("utf-8"), mtime=0)  # deterministic
    with open(path, "wb") as fh:
        fh.write(data)
    return sha256_bytes(data)


def describe(results):
    fields = sorted(set().union(*(bar.keys() for bar in results))) if results else []
    first = min(int(b["t"]) for b in results) if results else None
    last = max(int(b["t"]) for b in results) if results else None
    iso = lambda ms: dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc).isoformat()
    return {
        "row_count": len(results),
        "fields_present": fields,
        "vendor_vwap_field": "vw" in fields,
        "transaction_count_field": "n" in fields,
        "first_bar_utc": iso(first) if first else None,
        "last_bar_utc": iso(last) if last else None,
    }


def cmd_probe(args):
    key = api_key()
    url = aggs_url(args.base_url, args.date, args.date)
    payload = get_json(url, key)
    report = {
        "provider": "Massive/Polygon-compatible stocks aggregates",
        "endpoint_family": "/v2/aggs/ticker/{ticker}/range/1/minute",
        "base_url": args.base_url,
        "probe_date": args.date,
        "status": payload.get("status"),
        "adjusted_requested": True,
        "adjusted_reported": payload.get("adjusted"),
        "timezone_semantics": "t = bar start, epoch ms, UTC",
        **describe(payload.get("results", [])),
    }
    print(json.dumps(report, indent=2))


def cmd_capture(args):
    key = api_key()
    raw_dir = os.path.join(CACHE, "raw")
    canon_dir = os.path.join(CACHE, "canonical")
    manifest_dir = os.path.join(CACHE, "manifests")
    for d in (raw_dir, canon_dir, manifest_dir):
        os.makedirs(d, exist_ok=True)

    stem = f"{TICKER}_1m_{args.start}_{args.end}"
    url = aggs_url(args.base_url, args.start, args.end)
    pages, results, page_no = [], [], 0
    while url:
        page_no += 1
        payload = get_json(url, key)
        raw_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        raw_path = os.path.join(raw_dir, f"{stem}_page{page_no:04d}.json")
        with open(raw_path, "wb") as fh:
            fh.write(raw_bytes)
        pages.append({"page": page_no,
                      "path": os.path.relpath(raw_path, HERE),
                      "sha256": sha256_bytes(raw_bytes),
                      "resultsCount": payload.get("resultsCount")})
        results.extend(payload.get("results", []))
        url = payload.get("next_url")  # provider pagination; reuse auth header
        print(f"page {page_no}: total rows {len(results)}", file=sys.stderr)
        if url:
            time.sleep(RATE_LIMIT_SLEEP_S)

    rows = normalize(results)
    canon_path = os.path.join(canon_dir, f"{stem}.csv.gz")
    canon_sha = write_canonical_csv_gz(canon_path, rows)
    manifest = {
        "provider": "Massive/Polygon-compatible stocks aggregates",
        "endpoint_family": "/v2/aggs/ticker/{ticker}/range/1/minute",
        "base_url": args.base_url,
        "ticker": TICKER,
        "interval": "1 minute",
        "adjusted": True,
        "query_start": args.start,
        "query_end": args.end,
        "captured_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "timezone_semantics": "t_ms = bar start, epoch ms, UTC; et_iso derived, "
                              "original t_ms preserved",
        "session_flag_rule": "RTH iff 09:30 <= ET bar start < 16:00; EXT bars kept",
        "pages": pages,
        "canonical": {"path": os.path.relpath(canon_path, HERE),
                      "sha256": canon_sha,
                      "row_count": len(rows)},
        **describe(results),
    }
    man_path = os.path.join(manifest_dir, f"{stem}.manifest.json")
    with open(man_path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps({"manifest": os.path.relpath(man_path, HERE),
                      "canonical_sha256": canon_sha,
                      "row_count": len(rows)}, indent=2))


def cmd_selftest(_args):
    with open(FIXTURE) as fh:
        payload = json.load(fh)
    rows = normalize(payload["results"])
    assert len(rows) == 12, f"expected 12 rows, got {len(rows)}"
    assert [r["session"] for r in rows[:2]] == ["EXT", "EXT"], "pre-open must be EXT"
    assert all(r["session"] == "RTH" for r in rows[2:]), "09:30+ must be RTH"
    assert rows[2]["et_iso"].endswith("09:30:00-04:00"), rows[2]["et_iso"]

    five = resample_5m(rows[2:])  # RTH-only feasibility check
    assert len(five) == 2, f"expected 2 buckets, got {len(five)}"
    b0 = five[0]
    assert b0["bars"] == 5 and b0["session"] == "RTH"
    assert abs(float(b0["o"]) - 640.20) < 1e-9
    assert abs(b0["h"] - 640.80) < 1e-9
    assert abs(b0["l"] - 640.00) < 1e-9
    assert abs(float(b0["c"]) - 640.65) < 1e-9
    assert abs(b0["v"] - 5200.0) < 1e-9
    assert abs(b0["vw"] - 640.4319230769231) < 1e-6
    assert b0["n"] == sum(range(52, 57))

    canon_sha = write_canonical_csv_gz(
        os.path.join(tempfile.gettempdir(), "spy_selftest.csv.gz"), rows)
    print(json.dumps({"selftest": "PASS", "rows": len(rows),
                      "resample_5m_buckets": len(five),
                      "canonical_sha256": canon_sha}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("probe")
    p.add_argument("--date", required=True)
    p.add_argument("--base-url", default=BASE_URL_DEFAULT)
    p.set_defaults(func=cmd_probe)
    p = sub.add_parser("capture")
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--base-url", default=BASE_URL_DEFAULT)
    p.set_defaults(func=cmd_capture)
    p = sub.add_parser("selftest")
    p.set_defaults(func=cmd_selftest)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
