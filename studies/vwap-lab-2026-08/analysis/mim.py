#!/usr/bin/env python3
"""MIM-0 — Market Intraday Momentum, exact replication baseline — v1.0 · 2026-08-27.

Literature: Gao, Han, Li & Zhou, "Market Intraday Momentum." Core hypothesis (owner
charge 2026-08-27): the SPY return from the previous RTH close through the end of the
first 30 minutes positively predicts the return during the final 30 minutes.

This module IMPLEMENTS and is UNIT-TESTED on synthetic data (test_mim.py). It is NOT
run on the development corpus in the design packet: MIM-0's `early_return` crosses the
previous RTH close, and the local corpus is DIVIDEND-UNADJUSTED, so ex-dividend
sessions contaminate that overnight return; that corporate-action issue cannot be
resolved cleanly from OHLCV alone (see MIM_OVERNIGHT_DIAGNOSTIC and the MIM charter),
so outcome access is a DATA/SEMANTIC BLOCKER pending an external ex-dividend calendar.

Clock semantics (frozen, ET; 1-minute bar-START timestamps):
  previous_close  = previous RTH session's final RTH bar close.
  price_10_00     = the 09:59 bar CLOSE (price observed at 10:00).
  late_open       = the 15:30 bar OPEN  (executable late-window-start proxy).
  late_close      = the 15:59 bar CLOSE (CONTINUOUS-session close proxy — NOT an
                    official closing-auction fill).
  A session is used only if it has all three standard-clock bars 09:59 / 15:30 /
  15:59; early closes and sessions missing any of these produce NO observation.

  early_return = price_10_00 / previous_close - 1
  late_return  = late_close  / late_open     - 1

Statistics (frozen before outcome access): OLS late_return = alpha + beta*early_return;
primary condition beta > 0. Robust SE convention = HC1 (White heteroskedasticity-
consistent, small-sample-corrected) as PRIMARY; classical OLS SE reported secondary.
95% CI uses the normal 1.96 multiplier (N ~ 300). No covariance-estimator shopping.
"""

import math
import os
import random
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
DEV_START, DEV_END = "2024-09-03", "2025-12-31"
Z95 = 1.959963984540054
BOOTSTRAP_SEED = 20260827
BOOTSTRAP_B = 2000
# Frozen conservative cost diagnostics (before outcomes; not optimized):
MINTICK = 0.01               # SPY
SLIP_TICKS = 1               # existing lab adverse-slippage convention, per fill
COST_STRESS_RT_BPS = 5.0     # one clearly-labelled conservative round-trip stress


def load_ex_dividends(path=None):
    """{ex_date: cash_per_share} from the frozen SPY corporate-action sidecar
    (data/SPY_EX_DIVIDENDS_v1.0.json; State Street provenance)."""
    if path is None:
        path = os.path.join(HERE, "..", "data", "SPY_EX_DIVIDENDS_v1.0.json")
    import json
    d = json.load(open(path))
    return {r["ex_date"]: float(r["cash_per_share"]) for r in d["distributions"]}


def build_observations(rth_rows, dev_start=DEV_START, dev_end=DEV_END,
                       ex_dividends=None):
    """Session observations with the frozen clock semantics. rth_rows: RTH 1m rows
    with et_iso and o/h/l/c. Requires 09:59/15:30/15:59 bars; else the session is
    skipped. DIVIDEND-NEUTRAL early_return (frozen convention, owner/HELM 2026-08-27):
    ordinary session `(P_10_00 - previous_close)/previous_close`; SPY ex-dividend
    session `(P_10_00 + cash_distribution - previous_close)/previous_close` — removes
    the mechanical ex-dividend price drop while preserving the session. late_return is
    intraday and unchanged."""
    ex_dividends = ex_dividends or {}
    by = {}
    for r in rth_rows:
        by.setdefault(r["et_iso"][:10], []).append(r)
    dates = sorted(by)
    obs = []
    for i in range(1, len(dates)):
        d = dates[i]
        if not (dev_start <= d <= dev_end):
            continue
        cur = sorted(by[d], key=lambda r: r["et_iso"])
        prev = sorted(by[dates[i - 1]], key=lambda r: r["et_iso"])
        hm = {r["et_iso"][11:16]: r for r in cur}
        if not ({"09:59", "15:30", "15:59"} <= set(hm)):
            continue                                   # early close / missing bars
        prev_close = float(prev[-1]["c"])
        p_1000 = float(hm["09:59"]["c"])
        late_open = float(hm["15:30"]["o"])
        late_close = float(hm["15:59"]["c"])
        if prev_close <= 0 or late_open <= 0:
            continue
        div = ex_dividends.get(d, 0.0)                 # 0 ordinary; cash on ex-date
        obs.append({
            "date": d, "is_ex_dividend": d in ex_dividends,
            "ex_dividend_cash": div,
            "previous_close": prev_close, "price_10_00": p_1000,
            "late_open": late_open, "late_close": late_close,
            "early_return": (p_1000 + div - prev_close) / prev_close,
            "late_return": late_close / late_open - 1.0,
        })
    return obs


def ols_hc1(x, y):
    """Univariate OLS y = a + b x with classical and HC1 robust SE. Stdlib only."""
    n = len(x)
    if n < 3:
        return {"n": n, "note": "too few observations"}
    xb, yb = sum(x) / n, sum(y) / n
    sxx = sum((xi - xb) ** 2 for xi in x)
    sxy = sum((xi - xb) * (yi - yb) for xi, yi in zip(x, y))
    b = sxy / sxx
    a = yb - b * xb
    resid = [yi - a - b * xi for xi, yi in zip(x, y)]
    sse = sum(e * e for e in resid)
    sst = sum((yi - yb) ** 2 for yi in y)
    s2 = sse / (n - 2)
    se_classical = math.sqrt(s2 / sxx)
    # HC1 (White), univariate: Var(b) = n/(n-2) * Σ (x-xb)^2 e^2 / Sxx^2
    meat = sum(((xi - xb) ** 2) * (e ** 2) for xi, e in zip(x, resid))
    var_hc1 = (n / (n - 2)) * meat / (sxx ** 2)
    se_hc1 = math.sqrt(var_hc1)
    r2 = 1.0 - sse / sst if sst > 0 else None
    t_hc1 = b / se_hc1 if se_hc1 > 0 else None
    return {
        "n": n, "beta": b, "intercept": a,
        "se_hc1_primary": se_hc1, "t_hc1": t_hc1,
        "ci95_hc1": [b - Z95 * se_hc1, b + Z95 * se_hc1],
        "se_classical": se_classical,
        "t_classical": b / se_classical if se_classical > 0 else None,
        "r_squared": r2,
        "se_convention": "HC1 (White heteroskedasticity-consistent, small-sample "
                         "corrected) PRIMARY; classical OLS secondary; 95% CI via "
                         "normal 1.96. Frozen before outcomes; no estimator shopping.",
    }


def _bootstrap_mean_ci(vals, seed=BOOTSTRAP_SEED, B=BOOTSTRAP_B):
    n = len(vals)
    if n < 2:
        return None
    rng = random.Random(seed)
    means = []
    for _ in range(B):
        s = 0.0
        for _ in range(n):
            s += vals[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo = means[min(B - 1, int(0.025 * B))]
    hi = means[min(B - 1, int(0.975 * B))]
    return [round(lo * 1e4, 4), round(hi * 1e4, 4)]      # bps


def sign_strategy(obs):
    """Sign strategy: early>0 -> long the final half hour; early<0 -> short;
    early==0 -> no trade. realized = sign(early)*late_return. Fixed-notional
    convention: 1 unit notional per trade, so realized fractional return IS the
    per-trade P/L; reported in bps. One trade max/day."""
    trades = []
    for o in obs:
        er = o["early_return"]
        if er == 0:
            continue
        side = "long" if er > 0 else "short"
        realized = (o["late_return"] if er > 0 else -o["late_return"])
        trades.append({"date": o["date"], "side": side, "realized": realized,
                       "bps": realized * 1e4})
    if not trades:
        return {"n": 0}
    r = [t["realized"] for t in trades]
    bps = [t["bps"] for t in trades]
    wins = [x for x in r if x > 0]
    losses = [x for x in r if x < 0]
    gp, gl = sum(wins), -sum(losses)
    # fixed-notional equity + max drawdown (fractional)
    cum, peak, maxdd = 0.0, 0.0, 0.0
    for x in r:
        cum += x
        peak = max(peak, cum)
        maxdd = max(maxdd, peak - cum)

    def side_block(s):
        ss = [t["realized"] for t in trades if t["side"] == s]
        if not ss:
            return {"n": 0}
        w = sum(x for x in ss if x > 0)
        l = -sum(x for x in ss if x < 0)
        return {"n": len(ss), "mean_bps": round(sum(ss) / len(ss) * 1e4, 4),
                "profit_factor": round(w / l, 6) if l > 0 else None}
    # monthly consistency
    monthly = {}
    for t in trades:
        monthly.setdefault(t["date"][:7], []).append(t["realized"])
    months = sorted(monthly)
    prof_m = sum(1 for m in months if sum(monthly[m]) > 0)
    # outlier concentration (by |bps|)
    srt = sorted(bps, key=lambda v: -abs(v))
    net_bps = sum(bps)
    excl10 = round(net_bps - sum(srt[:10]), 4)
    return {
        "n": len(trades),
        "mean_bps": round(sum(bps) / len(bps), 4),
        "median_bps": round(st.median(bps), 4),
        "cumulative_bps": round(net_bps, 4),
        "profit_factor": round(gp / gl, 6) if gl > 0 else None,
        "win_rate_pct": round(100 * len(wins) / len(trades), 4),
        "max_drawdown_bps": round(maxdd * 1e4, 4),
        "long": side_block("long"), "short": side_block("short"),
        "bootstrap_mean_ci95_bps": _bootstrap_mean_ci(r),
        "monthly": {"n_months": len(months), "profitable_months": prof_m},
        "outliers": {"net_bps_excl_top10_abs": excl10, "net_bps": round(net_bps, 4)},
    }


def cost_diagnostics(obs, spy_price_ref=None):
    """Frozen conservative cost views (before outcomes): (1) zero-cost gross,
    (2) lab adverse slippage 1 tick per fill (2 fills: 15:30 open entry, 15:59
    close exit), (3) a conservative round-trip bps stress. Costs are subtracted
    from each trade's realized return. Not optimized. spy_price_ref: representative
    SPY price for the slippage->bps conversion (defaults to mean late_open)."""
    ss = sign_strategy(obs)
    if ss.get("n", 0) == 0:
        return {"n": 0}
    px = spy_price_ref or (sum(o["late_open"] for o in obs) / len(obs))
    slip_rt_bps = (2 * SLIP_TICKS * MINTICK / px) * 1e4        # 2 fills, 1 tick each
    gross = ss["mean_bps"]
    return {
        "spy_price_ref": round(px, 4),
        "zero_cost_mean_bps": gross,
        "lab_slippage_mean_bps": round(gross - slip_rt_bps, 4),
        "lab_slippage_rt_bps": round(slip_rt_bps, 4),
        "stress_mean_bps": round(gross - COST_STRESS_RT_BPS, 4),
        "stress_rt_bps": COST_STRESS_RT_BPS,
        "note": "gross association is reported separately from executable economics; "
                "the 15:59 close is a CONTINUOUS-session proxy, NOT an auction fill — "
                "no auction-executable alpha is claimed from OHLCV. Costs frozen, not "
                "optimized.",
    }


def classify(reg, ss, costs):
    """Frozen kill/advance gates. FAMILY DEAD if beta<=0 OR gross expectancy<=0 OR
    positive gross does not survive the conservative cost stress. Else EDGE
    CANDIDATE — VALIDATION DECISION REQUIRED (validation NOT run autonomously)."""
    beta = reg.get("beta")
    gross = ss.get("mean_bps")
    stressed = costs.get("stress_mean_bps")
    if beta is None or gross is None:
        return {"verdict": "INDETERMINATE", "reason": "insufficient observations"}
    if beta <= 0:
        return {"verdict": "FAMILY DEAD", "reason": f"beta {beta:.6g} <= 0"}
    if gross <= 0:
        return {"verdict": "FAMILY DEAD",
                "reason": f"gross sign-strategy expectancy {gross} bps <= 0"}
    if stressed is not None and stressed <= 0:
        return {"verdict": "FAMILY DEAD",
                "reason": f"positive gross ({gross} bps) does not survive the frozen "
                          f"conservative cost stress ({COST_STRESS_RT_BPS} bps RT): "
                          f"{stressed} bps <= 0"}
    return {"verdict": "EDGE CANDIDATE — VALIDATION DECISION REQUIRED",
            "reason": f"beta {beta:.6g} > 0, gross {gross} bps > 0, survives "
                      f"{COST_STRESS_RT_BPS} bps stress ({stressed} bps); "
                      "validation is NOT run autonomously."}


def _arm(obs):
    x = [o["early_return"] for o in obs]
    y = [o["late_return"] for o in obs]
    reg = ols_hc1(x, y)
    ss = sign_strategy(obs)
    costs = cost_diagnostics(obs)
    return {"regression": reg, "sign_strategy": ss, "costs": costs,
            "classification": classify(reg, ss, costs)}


def main():
    """Development replication over 2024-09-03..2025-12-31. Dividend-neutral
    early_return is PRIMARY (frozen convention + State Street sidecar); an ex-dividend-
    EXCLUDED view is a corporate-action SENSITIVITY diagnostic only (not a gate).
    Screened (frozen CORPUS_MASK_v1.0) primary; raw sensitivity."""
    import json
    import platform
    import parity_foundation as pf
    print("python", platform.python_version(), "| MIM-0 development replication")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    exdiv = load_ex_dividends()
    mask = set(json.load(open(os.path.join(HERE, "CORPUS_MASK_v1.0.json")))["mask_t_ms"])
    rth = pf.load_corpus_rth()
    rth_scr = [r for r in rth if r["t_ms"] not in {str(x) for x in mask}]

    obs_scr = build_observations(rth_scr, ex_dividends=exdiv)
    obs_raw = build_observations(rth, ex_dividends=exdiv)
    # ex-dividend-excluded SENSITIVITY (diagnostic only)
    obs_scr_exdiv_excl = [o for o in obs_scr if not o["is_ex_dividend"]]

    primary = _arm(obs_scr)
    raw = _arm(obs_raw)
    sens = _arm(obs_scr_exdiv_excl)

    report = {
        "role": "MIM-0 exact replication (development); dividend-neutral early_return "
                "PRIMARY (screened), raw sensitivity, ex-dividend-excluded sensitivity",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "development_window": [DEV_START, DEV_END],
        "dividend_convention": "PRIMARY dividend-neutral: ex-date early_return = "
            "(P_10_00 + cash - previous_close)/previous_close; ordinary otherwise. "
            "Sidecar data/SPY_EX_DIVIDENDS_v1.0.json (State Street provenance).",
        "ex_dividend_sessions_in_obs": [o["date"] for o in obs_scr if o["is_ex_dividend"]],
        "n_obs_screened": len(obs_scr), "n_obs_raw": len(obs_raw),
        "screened_primary": primary,
        "raw_sensitivity": raw,
        "ex_dividend_excluded_sensitivity": {
            "note": "corporate-action SENSITIVITY only — NOT a second configuration, "
                    "NOT a gate, NOT a rescue; the dividend-neutral screened result is "
                    "primary.",
            "n_obs": len(obs_scr_exdiv_excl), **sens},
        "verdict": primary["classification"]["verdict"],
    }
    out = os.path.join(HERE, "MIM0_DEV_2026-08-27.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)

    r, s, c = primary["regression"], primary["sign_strategy"], primary["costs"]
    print("\n" + "=" * 72)
    print("MIM-0 DEVELOPMENT — dividend-neutral (screened primary)")
    print("=" * 72)
    print(f"  N={r['n']} beta={r['beta']:+.5f} (HC1 SE {r['se_hc1_primary']:.5f}, "
          f"t {r['t_hc1']:+.3f}, CI95 [{r['ci95_hc1'][0]:+.5f},{r['ci95_hc1'][1]:+.5f}]) "
          f"R2={r['r_squared']:.5f}")
    print(f"  sign strategy: mean {s['mean_bps']} bps, cum {s['cumulative_bps']} bps, "
          f"PF {s['profit_factor']}, win {s['win_rate_pct']}%, maxDD {s['max_drawdown_bps']} bps")
    print(f"  long {s['long']}  short {s['short']}")
    print(f"  costs: zero {c['zero_cost_mean_bps']} | lab-slip {c['lab_slippage_mean_bps']} "
          f"| 5bps-stress {c['stress_mean_bps']} bps")
    print(f"  bootstrap mean CI95 {s['bootstrap_mean_ci95_bps']} bps | months "
          f"{s['monthly']['profitable_months']}/{s['monthly']['n_months']}")
    print(f"\n  VERDICT: {report['verdict']}")
    print(f"  ({primary['classification']['reason']})")
    print(f"\nwritten: {os.path.relpath(out, os.path.normpath(os.path.join(HERE, '..')))}")


if __name__ == "__main__":
    main()
