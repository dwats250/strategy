#!/usr/bin/env python3
"""ODR-0 — Overnight / Opening Dislocation Reversal, baseline — v1.0 · 2026-08-27.

Literature: Liu & Tse (2017), "Overnight returns of stock indexes: Evidence from ETFs
and futures," Int. Rev. Econ. & Finance 48:440-451 — US ETF overnight returns are
significantly positive while intraday returns are negative (intraday reversal of the
overnight move). Owner/HELM charge 2026-08-27.

Smallest baseline hypothesis: SPY's dividend-neutral previous-RTH-close → 09:30 opening
return NEGATIVELY predicts its 09:30 → 10:00 first-half-hour return.

Association test (frozen): first_half_hour_return = α + β·overnight_return; preregistered
sign **β < 0**. Robust SE = HC1 (White, small-sample corrected) PRIMARY (frozen; no
shopping); classical secondary; 95% CI via normal 1.96.

Clock semantics (ET; 1-minute bar-START timestamps):
  previous_close = previous RTH session final close.
  open_0930      = 09:30 bar OPEN (the opening print; the signal is observed here).
  open_0931      = 09:31 bar OPEN (causal entry — one bar after the signal print).
  close_0959     = 09:59 bar CLOSE (the 10:00 price; exit).
  A session is used only if it is a NORMAL FULL session with bars 09:30 / 09:31 / 09:59
  / 15:59 (early closes and sessions missing any of these produce no observation/trade).

  overnight_return = (open_0930 + cash_distribution − previous_close)/previous_close
                     (dividend-neutral; cash added only on SPY ex-dividend sessions, via
                     the frozen State Street sidecar — the SAME convention as MIM).
  first_half_hour_return = close_0959 / open_0930 − 1     (09:30→10:00, intraday, clean).
  trade_return           = close_0959 / open_0931 − 1     (09:31→09:59, executable).

Causal sign strategy: overnight_return > 0 → SHORT; < 0 → LONG; == 0 → no trade.
realized = −sign(overnight_return) · trade_return. One trade max per normal full session.
No threshold/VWAP/EMA/ATR/stop/target/filter/side-rescue/alternate-window.
"""

import os
import statistics as st

import mim  # reuse ols_hc1, load_ex_dividends, bootstrap, and frozen cost constants

HERE = os.path.dirname(os.path.abspath(__file__))
DEV_START, DEV_END = "2024-09-03", "2025-12-31"


def build_observations(rth_rows, dev_start=DEV_START, dev_end=DEV_END, ex_dividends=None):
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
        if not ({"09:30", "09:31", "09:59", "15:59"} <= set(hm)):
            continue                                   # normal full session only
        prev_close = float(prev[-1]["c"])
        open_0930 = float(hm["09:30"]["o"])
        open_0931 = float(hm["09:31"]["o"])
        close_0959 = float(hm["09:59"]["c"])
        if prev_close <= 0 or open_0930 <= 0 or open_0931 <= 0:
            continue
        div = ex_dividends.get(d, 0.0)
        obs.append({
            "date": d, "is_ex_dividend": d in ex_dividends, "ex_dividend_cash": div,
            "previous_close": prev_close, "open_0930": open_0930,
            "open_0931": open_0931, "close_0959": close_0959,
            "overnight_return": (open_0930 + div - prev_close) / prev_close,
            "first_half_hour_return": close_0959 / open_0930 - 1.0,
            "trade_return": close_0959 / open_0931 - 1.0,
        })
    return obs


def sign_strategy(obs):
    """Causal reversal: overnight>0 -> SHORT, <0 -> LONG, ==0 -> flat; enter 09:31 open,
    exit 09:59 close. realized = -sign(overnight)*trade_return. Fixed-notional: 1 unit
    per trade, realized fractional return = per-trade P/L, reported in bps."""
    trades = []
    for o in obs:
        ov = o["overnight_return"]
        if ov == 0:
            continue
        side = "short" if ov > 0 else "long"
        realized = -o["trade_return"] if ov > 0 else o["trade_return"]
        trades.append({"date": o["date"], "side": side, "realized": realized,
                       "bps": realized * 1e4})
    if not trades:
        return {"n": 0}
    r = [t["realized"] for t in trades]
    bps = [t["bps"] for t in trades]
    wins = [x for x in r if x > 0]
    gp = sum(wins)
    gl = -sum(x for x in r if x < 0)
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
    monthly = {}
    for t in trades:
        monthly.setdefault(t["date"][:7], []).append(t["realized"])
    months = sorted(monthly)
    prof_m = sum(1 for m in months if sum(monthly[m]) > 0)
    srt = sorted(bps, key=lambda v: -abs(v))
    net_bps = sum(bps)
    return {
        "n": len(trades),
        "mean_bps": round(sum(bps) / len(bps), 4),
        "median_bps": round(st.median(bps), 4),
        "cumulative_bps": round(net_bps, 4),
        "profit_factor": round(gp / gl, 6) if gl > 0 else None,
        "win_rate_pct": round(100 * len(wins) / len(trades), 4),
        "max_drawdown_bps": round(maxdd * 1e4, 4),
        "long": side_block("long"), "short": side_block("short"),
        "bootstrap_mean_ci95_bps": mim._bootstrap_mean_ci(r),
        "monthly": {"n_months": len(months), "profitable_months": prof_m},
        "outliers": {"net_bps_excl_top10_abs": round(net_bps - sum(srt[:10]), 4),
                     "net_bps": round(net_bps, 4)},
    }


def cost_diagnostics(obs, spy_price_ref=None):
    ss = sign_strategy(obs)
    if ss.get("n", 0) == 0:
        return {"n": 0}
    px = spy_price_ref or (sum(o["open_0931"] for o in obs) / len(obs))
    slip_rt_bps = (2 * mim.SLIP_TICKS * mim.MINTICK / px) * 1e4
    gross = ss["mean_bps"]
    return {
        "spy_price_ref": round(px, 4),
        "zero_cost_mean_bps": gross,
        "lab_slippage_mean_bps": round(gross - slip_rt_bps, 4),
        "lab_slippage_rt_bps": round(slip_rt_bps, 4),
        "stress_mean_bps": round(gross - mim.COST_STRESS_RT_BPS, 4),
        "stress_rt_bps": mim.COST_STRESS_RT_BPS,
        "note": "gross reported separately from executable economics; costs frozen, not "
                "optimized; entry 09:31 open, exit 09:59 close (2 fills).",
    }


def classify(reg, ss, costs):
    """Frozen gates: FAMILY DEAD if β ≥ 0 (reversal requires β<0) OR gross causal
    expectancy ≤ 0 OR positive gross fails the frozen conservative cost stress.
    Else EDGE CANDIDATE — VALIDATION DECISION REQUIRED (validation NOT run)."""
    beta = reg.get("beta")
    gross = ss.get("mean_bps")
    stressed = costs.get("stress_mean_bps")
    if beta is None or gross is None:
        return {"verdict": "INDETERMINATE", "reason": "insufficient observations"}
    if beta >= 0:
        return {"verdict": "FAMILY DEAD",
                "reason": f"beta {beta:.6g} >= 0 (reversal requires beta < 0)"}
    if gross <= 0:
        return {"verdict": "FAMILY DEAD",
                "reason": f"gross causal sign-strategy expectancy {gross} bps <= 0"}
    if stressed is not None and stressed <= 0:
        return {"verdict": "FAMILY DEAD",
                "reason": f"positive gross ({gross} bps) fails the frozen "
                          f"{mim.COST_STRESS_RT_BPS} bps cost stress: {stressed} bps <= 0"}
    return {"verdict": "EDGE CANDIDATE — VALIDATION DECISION REQUIRED",
            "reason": f"beta {beta:.6g} < 0, gross {gross} bps > 0, survives "
                      f"{mim.COST_STRESS_RT_BPS} bps stress ({stressed} bps); "
                      "validation is NOT run autonomously."}


def main():
    import json
    import platform
    import parity_foundation as pf
    print("python", platform.python_version(), "| ODR-0 development run")
    print(f"input local corpus sha256 {pf.CANONICAL_SHA256} (guarded)")
    exdiv = mim.load_ex_dividends()
    mask = set(json.load(open(os.path.join(HERE, "CORPUS_MASK_v1.0.json")))["mask_t_ms"])
    rth = pf.load_corpus_rth()
    rth_scr = [r for r in rth if r["t_ms"] not in {str(x) for x in mask}]

    def arm(rth_rows):
        obs = build_observations(rth_rows, ex_dividends=exdiv)
        x = [o["overnight_return"] for o in obs]
        y = [o["first_half_hour_return"] for o in obs]
        reg = mim.ols_hc1(x, y)
        ss = sign_strategy(obs)
        costs = cost_diagnostics(obs)
        return obs, {"regression": reg, "sign_strategy": ss, "costs": costs,
                     "classification": classify(reg, ss, costs)}

    obs_scr, primary = arm(rth_scr)
    obs_raw, raw = arm(rth)
    report = {
        "role": "ODR-0 baseline (development); dividend-neutral overnight_return; "
                "first_half_hour_return = a + b*overnight_return (b<0 preregistered); "
                "causal reversal sign strategy (enter 09:31 open, exit 09:59 close)",
        "python": platform.python_version(),
        "corpus_sha256": pf.CANONICAL_SHA256,
        "development_window": [DEV_START, DEV_END],
        "literature": "Liu & Tse (2017), Int. Rev. Econ. & Finance 48:440-451",
        "n_obs_screened": len(obs_scr), "n_obs_raw": len(obs_raw),
        "screened_primary": primary, "raw_sensitivity": raw,
        "verdict": primary["classification"]["verdict"],
    }
    out = os.path.join(HERE, "ODR0_DEV_2026-08-27.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)
    r, s, c = primary["regression"], primary["sign_strategy"], primary["costs"]
    print("\n" + "=" * 72)
    print("ODR-0 DEVELOPMENT — overnight -> first-half-hour reversal (screened primary)")
    print("=" * 72)
    print(f"  N={r['n']} beta={r['beta']:+.5f} (HC1 SE {r['se_hc1_primary']:.5f}, "
          f"t {r['t_hc1']:+.3f}, CI95 [{r['ci95_hc1'][0]:+.5f},{r['ci95_hc1'][1]:+.5f}]) "
          f"R2={r['r_squared']:.5f}  [preregistered beta<0]")
    print(f"  sign strategy: mean {s['mean_bps']} bps, cum {s['cumulative_bps']} bps, "
          f"PF {s['profit_factor']}, win {s['win_rate_pct']}%, maxDD {s['max_drawdown_bps']} bps")
    print(f"  long {s['long']}  short {s['short']}")
    print(f"  costs: zero {c['zero_cost_mean_bps']} | lab-slip {c['lab_slippage_mean_bps']} "
          f"| 5bps-stress {c['stress_mean_bps']} bps | bootstrap CI {s['bootstrap_mean_ci95_bps']}")
    print(f"\n  VERDICT: {report['verdict']}")
    print(f"  ({primary['classification']['reason']})")
    print(f"\nwritten: {os.path.relpath(out, os.path.normpath(os.path.join(HERE, '..')))}")


if __name__ == "__main__":
    main()
