#!/usr/bin/env python3
"""R0/R1 mechanical identity gate · v1.0 · 2026-08-25.

Authorized by the owner R1-capture charge of 2026-08-25 and pre-registered in
manifests/RUN_VDC_SPY_5m_dev_R1_v1.0.md. This is the ONLY analysis permitted
on the sealed R1 capture: an exact trade-set identity comparison against the
preserved R0 List-of-Trades export. It computes no aggregate, no expectancy,
no stratification, and prints no performance quantity — only identity
verdicts and, on failure, the first divergences needed to classify them.

Pre-registered export-format normalization (manifest, frozen):
  - UTF-8 BOM stripping;
  - leading/trailing whitespace on cell values;
  - numeric cells compared after decimal parsing (so "1.5" == "1.50");
  - column-set differences reported explicitly; the intersection is
    compared, and a missing IDENTITY column is a FAIL, not a skip.
Row order and trade numbering must agree as exported.

Usage:
  identity_gate_r0_r1.py --selftest
  identity_gate_r0_r1.py <r1_tradelist.csv> [--chartdata <r1_chartdata.csv>]

Exit status: 0 PASS · 2 FAIL/STOP · 3 usage or input-identity error.
"""

import csv
import hashlib
import io
import os
import platform
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.normpath(os.path.join(HERE, ".."))

R0_TRADELIST = os.path.join(
    STUDY, "exports", "VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv")
R0_SHA256 = (
    "8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241")

EXPECTED_TRADES = 1331

# Columns whose agreement constitutes the identity requirement. Absence of
# any of these from either export is a FAIL.
IDENTITY_COLUMNS = [
    "Trade number", "Type", "Date and time", "Signal",
    "Price USD", "Size (qty)", "Net PnL USD",
]

INSTRUMENTATION_COLUMNS = [
    "ACCEPT_STATE_DIR", "EMA50", "S_9_20_50", "ORDERED_9_20_50",
    "EXPANDING_9_20_50", "ALIGNED_EXP_COUNT_9_20_50", "SHOCK_RATIO",
    "RECENT_SHOCK", "S_10_22_55", "ORDERED_10_22_55",
]

MAX_DIVERGENCES_SHOWN = 10


def read_rows(text):
    """Parse CSV text (BOM already handled by caller) into header + rows of
    stripped cell strings."""
    reader = csv.reader(io.StringIO(text))
    table = [[cell.strip() for cell in row] for row in reader]
    return table[0], table[1:]


def load_file(path):
    with open(path, "rb") as fh:
        blob = fh.read()
    sha = hashlib.sha256(blob).hexdigest()
    return blob.decode("utf-8-sig"), sha


def cells_equal(a, b):
    """Numeric cells compare after decimal parsing; others compare as
    stripped strings."""
    if a == b:
        return True
    try:
        return float(a) == float(b)
    except ValueError:
        return False


def compare_tradelists(hdr0, rows0, hdr1, rows1, out=print):
    """Return (passed, divergences). Mechanical only."""
    divergences = []

    cols0, cols1 = set(hdr0), set(hdr1)
    if cols0 != cols1:
        out(f"column sets differ: only in R0 {sorted(cols0 - cols1)}; "
            f"only in R1 {sorted(cols1 - cols0)}")
    missing_identity = [c for c in IDENTITY_COLUMNS
                        if c not in cols0 or c not in cols1]
    if missing_identity:
        divergences.append(("IDENTITY COLUMN MISSING", missing_identity))
        return False, divergences
    shared = [c for c in hdr0 if c in cols1]
    skipped = sorted((cols0 | cols1) - set(shared))
    if skipped:
        out(f"non-shared columns excluded from comparison "
            f"(none are identity columns): {skipped}")

    n0 = {}
    for r in rows0:
        n0.setdefault(int(r[hdr0.index("Trade number")]), []).append(r)
    trades0 = len(n0)
    trades1 = len({r[hdr1.index("Trade number")] for r in rows1})
    if trades0 != EXPECTED_TRADES:
        divergences.append(
            ("R0 REFERENCE TRADE COUNT", trades0, EXPECTED_TRADES))
        return False, divergences
    if len(rows1) != len(rows0) or trades1 != trades0:
        divergences.append(
            ("ROW/TRADE COUNT", f"R0 rows={len(rows0)} trades={trades0}",
             f"R1 rows={len(rows1)} trades={trades1}"))
        return False, divergences

    idx0 = {c: hdr0.index(c) for c in shared}
    idx1 = {c: hdr1.index(c) for c in shared}
    for i, (r0, r1) in enumerate(zip(rows0, rows1)):
        for c in shared:
            if not cells_equal(r0[idx0[c]], r1[idx1[c]]):
                divergences.append(
                    (f"row {i + 2} (trade {r0[idx0['Trade number']]}, "
                     f"{r0[idx0['Type']]})", c,
                     f"R0={r0[idx0[c]]!r}", f"R1={r1[idx1[c]]!r}"))
                if len(divergences) >= MAX_DIVERGENCES_SHOWN:
                    return False, divergences
    return (len(divergences) == 0), divergences


def check_chartdata_header(path):
    """Header-only inspection of the sealed R1 chart-data export: confirms
    volume + the ten instrumentation columns are present. Reads no data
    rows and no values."""
    with open(path, "rb") as fh:
        blob = fh.read()
    sha = hashlib.sha256(blob).hexdigest()
    first_line = blob.decode("utf-8-sig").splitlines()[0]
    header = [c.strip() for c in next(csv.reader(io.StringIO(first_line)))]
    print(f"chart-data {os.path.basename(path)} sha256 {sha}")
    print(f"chart-data columns ({len(header)}): {header}")
    vol = [c for c in header if c.lower() == "volume"]
    print(f"volume column present: {'YES (' + vol[0] + ')' if vol else 'NO'}")
    missing = [c for c in INSTRUMENTATION_COLUMNS if c not in header]
    if missing:
        print(f"instrumentation columns MISSING: {missing}")
    else:
        print("all 10 instrumentation columns present: YES")
    return bool(vol) and not missing


def run_gate(r1_path, chartdata_path=None):
    print("python", platform.python_version(), "| stdlib only")
    text0, sha0 = load_file(R0_TRADELIST)
    print(f"R0 reference {os.path.relpath(R0_TRADELIST, STUDY)} "
          f"sha256 {sha0}")
    if sha0 != R0_SHA256:
        print(f"INPUT IDENTITY FAILURE: R0 reference sha256 != {R0_SHA256}")
        return 3
    text1, sha1 = load_file(r1_path)
    print(f"R1 candidate {r1_path} sha256 {sha1}")

    hdr0, rows0 = read_rows(text0)
    hdr1, rows1 = read_rows(text1)
    passed, divergences = compare_tradelists(hdr0, rows0, hdr1, rows1)

    chart_ok = None
    if chartdata_path:
        chart_ok = check_chartdata_header(chartdata_path)

    if passed:
        print(f"IDENTITY GATE PASS: {EXPECTED_TRADES} trades; side, "
              f"timestamps, prices, and P/L identical under the "
              f"pre-registered normalization.")
        if chart_ok is False:
            print("NOTE: trade-set identity passed but the chart-data "
                  "export is missing required columns — see above.")
        print("R1 ADMISSIBLE (SEALED-UNINTERPRETED). STOP: development "
              "analysis remains sealed pending owner/HELM unseal "
              "authorization.")
        return 0

    print("IDENTITY GATE FAIL — STOP (A1.8: PVAE is not analyzed).")
    print(f"first divergence(s), up to {MAX_DIVERGENCES_SHOWN}:")
    for d in divergences:
        print("  ", d)
    print("Classify before any action: feed/context difference vs "
          "export-format difference vs instrumentation-induced behavior "
          "change vs unresolved. Repair nothing silently.")
    return 2


def selftest():
    """Deterministic self-test on the pinned R0 export: identical input
    passes; format-normalized input passes; perturbed input fails."""
    text0, sha0 = load_file(R0_TRADELIST)
    if sha0 != R0_SHA256:
        print("SELFTEST ABORT: R0 reference hash mismatch")
        return 3
    hdr, rows = read_rows(text0)
    quiet = lambda *a, **k: None

    ok, div = compare_tradelists(hdr, rows, hdr,
                                 [list(r) for r in rows], out=quiet)
    assert ok and not div, "identical comparison must PASS"

    # format normalization: pad decimals and whitespace on a numeric cell
    ip = hdr.index("Price USD")
    rows_fmt = [list(r) for r in rows]
    rows_fmt[0][ip] = " " + rows_fmt[0][ip] + "0 ".rstrip() + "0"
    hdr_fmt, rows_fmt2 = read_rows(
        "\n".join([",".join(hdr)] + [",".join(r) for r in rows_fmt]))
    ok, div = compare_tradelists(hdr, rows, hdr_fmt, rows_fmt2, out=quiet)
    assert ok, f"decimal-padded value must PASS normalization: {div}"

    # perturbation: one price changed by a cent must FAIL
    rows_bad = [list(r) for r in rows]
    rows_bad[5][ip] = str(float(rows_bad[5][ip]) + 0.01)
    ok, div = compare_tradelists(hdr, rows, hdr, rows_bad, out=quiet)
    assert not ok and div, "perturbed price must FAIL"

    # dropped trade must FAIL on counts
    ok, div = compare_tradelists(hdr, rows, hdr,
                                 [list(r) for r in rows[:-2]], out=quiet)
    assert not ok, "dropped trade must FAIL"

    # missing identity column must FAIL
    it = hdr.index("Type")
    hdr_cut = [c for c in hdr if c != "Type"]
    rows_cut = [[c for j, c in enumerate(r) if j != it] for r in rows]
    ok, div = compare_tradelists(hdr, rows, hdr_cut, rows_cut, out=quiet)
    assert not ok and div[0][0] == "IDENTITY COLUMN MISSING"

    print("SELFTEST PASS: identical=PASS, decimal-normalized=PASS, "
          "perturbed-price=FAIL, dropped-trade=FAIL, "
          "missing-identity-column=FAIL")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) < 2:
        print(__doc__)
        return 3
    chartdata = None
    if "--chartdata" in argv:
        chartdata = argv[argv.index("--chartdata") + 1]
    return run_gate(argv[1], chartdata)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
