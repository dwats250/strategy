#!/usr/bin/env python3
"""FastAlpha experiment tear-sheet layer — v0.1 · 2026-08-26.

Reusable, deterministic analysis infrastructure for FastAlpha-family LOCAL
research. It consumes trade lists produced by `fastalpha_engine.simulate` (each
trade carries pnl, pnl_r, risk_points, side, bars_held, entry_bar, exit_bar,
exit_reason) and produces a canonical machine-readable report: trade-level and
R-normalized metrics, equity/drawdown series, monthly/distribution/streak stats,
outlier-concentration diagnostics, a deterministic bootstrap CI, and trade-based
Sharpe/Sortino. It also provides a raw-vs-screened dual report and a controlled
A/B comparison mode.

This is INFRASTRUCTURE, not a strategy experiment: it defines no signal, runs no
new variant, and interprets no validation/holdout data. Stdlib only (so it runs
without numpy); the reference cross-check against numpy lives in the tests.

Conventions frozen here (descriptive defaults, NOT optimized against results):
  * 1R = the frozen initial entry-to-stop distance `risk_points` (= atr_stop_ticks
    x mintick). pnl_r = pnl / risk_points. Trades that exit via thesis/EOD/stop
    all use this SAME initial-R denominator — no retroactive resizing. A realized
    stop-out loses slightly MORE than 1R because of the 1-tick exit slippage.
  * Monthly P/L is attributed to a trade's EXIT month (realized).
  * Rolling stats use a TRADE-INDEX window of ROLLING_WINDOW trades.
  * Bootstrap uses a fixed seed; the IID bootstrap is labelled PROVISIONAL
    (trade outcomes may be serially dependent); a fixed-block bootstrap with a
    rule-of-thumb block length is also provided.
  * Sharpe/Sortino are TRADE-BASED (per-trade P/L series). CAGR/Calmar are
    DEFERRED: fixed-1-share vs $50k is arbitrary capital utilization, so they are
    account-construction-dependent, not discovery metrics.
"""

import math
import os
import random
import statistics as st

ROLLING_WINDOW = 50          # trades (descriptive default; not optimized)
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 20260826
R_BIN_WIDTH = 0.5            # R histogram bin width
PNL_BIN_WIDTH = 0.5         # P/L histogram bin width (points)
DUR_BIN_WIDTH = 5           # holding-duration histogram bin width (bars)


# ---------------------------------------------------------------------------
# small stdlib numeric helpers
# ---------------------------------------------------------------------------
def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def _median(xs):
    return st.median(xs) if xs else None


def _stdev(xs):
    return st.stdev(xs) if len(xs) > 1 else 0.0


def _pf(wins_sum, losses_sum_abs):
    return round(wins_sum / losses_sum_abs, 6) if losses_sum_abs > 0 else None


def _r(x, nd=6):
    return round(x, nd) if isinstance(x, (int, float)) else x


def _hist(values, width):
    """(edges, counts) with fixed-width bins spanning the data. Deterministic."""
    if not values:
        return {"bin_width": width, "edges": [], "counts": []}
    lo = math.floor(min(values) / width) * width
    hi = math.ceil(max(values) / width) * width
    nb = max(1, int(round((hi - lo) / width)))
    counts = [0] * nb
    for v in values:
        k = min(nb - 1, int((v - lo) / width))
        counts[k] += 1
    edges = [round(lo + i * width, 6) for i in range(nb + 1)]
    return {"bin_width": width, "edges": edges, "counts": counts}


# ---------------------------------------------------------------------------
# metric blocks
# ---------------------------------------------------------------------------
def _side_block(trades, side):
    s = [t for t in trades if t["side"] == side]
    p = [t["pnl"] for t in s]
    w = sum(x for x in p if x > 0)
    l = -sum(x for x in p if x < 0)
    return {"n": len(s), "net_pnl": _r(sum(p), 4),
            "expectancy": _r(_mean(p)) if s else None,
            "profit_factor": _pf(w, l)}


def trade_metrics(trades):
    p = [t["pnl"] for t in trades]
    n = len(trades)
    if n == 0:
        return {"n": 0}
    wins = [x for x in p if x > 0]
    losses = [x for x in p if x < 0]
    gp, gl = sum(wins), -sum(losses)
    durs = [t["bars_held"] for t in trades]
    return {
        "n": n,
        "net_pnl": _r(sum(p), 4),
        "expectancy": _r(_mean(p)),
        "median_pnl": _r(_median(p)),
        "win_rate_pct": _r(100.0 * len(wins) / n, 4),
        "wins": len(wins), "losses": len(losses),
        "avg_winner": _r(_mean(wins)) if wins else None,
        "avg_loser": _r(_mean(losses)) if losses else None,
        "payoff_ratio": _r(abs(_mean(wins) / _mean(losses)))
                        if wins and losses else None,
        "profit_factor": _pf(gp, gl),
        "largest_win": _r(max(p), 4),
        "largest_loss": _r(min(p), 4),
        "stdev_pnl": _r(_stdev(p)),
        "avg_bars_held": _r(_mean(durs), 4),
        "median_bars_held": _r(_median(durs), 4),
        "exit_reason_counts": {rr: sum(1 for t in trades if t["exit_reason"] == rr)
                               for rr in ("Long ATR Stop", "Short ATR Stop",
                                          "VWAP Failure", "EOD")},
        "long": _side_block(trades, "long"),
        "short": _side_block(trades, "short"),
    }


def r_metrics(trades):
    rs = [t["pnl_r"] for t in trades if t.get("pnl_r") is not None]
    if not rs:
        return {"n": 0, "note": "no risk_points on trades"}
    w = [x for x in rs if x > 0]
    l = [x for x in rs if x < 0]
    return {
        "definition": "1R = frozen initial entry-to-stop distance risk_points "
                      "(= atr_stop_ticks x mintick). pnl_r = pnl / risk_points. "
                      "All exit types use this initial-R denominator; realized "
                      "stop-outs lose slightly more than 1R (1-tick exit "
                      "slippage). No retroactive resizing.",
        "n": len(rs),
        "total_r": _r(sum(rs), 4),
        "mean_r": _r(_mean(rs)),
        "median_r": _r(_median(rs)),
        "avg_winner_r": _r(_mean(w)) if w else None,
        "avg_loser_r": _r(_mean(l)) if l else None,
        "stdev_r": _r(_stdev(rs)),
        "r_histogram": _hist(rs, R_BIN_WIDTH),
    }


def equity_series(trades):
    p = [t["pnl"] for t in trades]
    n = len(p)
    if n == 0:
        return {"n": 0}
    eq, cum = [], 0.0
    peak, uw, max_dd, dd_len, longest_dd = 0.0, [], 0.0, 0, 0
    for x in p:
        cum += x
        eq.append(round(cum, 4))
        peak = max(peak, cum)
        d = peak - cum
        uw.append(round(-d, 4))
        max_dd = max(max_dd, d)
        dd_len = 0 if d <= 1e-12 else dd_len + 1
        longest_dd = max(longest_dd, dd_len)
    # trade-index rolling expectancy / PF
    roll_exp, roll_pf = [], []
    W = ROLLING_WINDOW
    for i in range(n):
        if i + 1 >= W:
            win = p[i + 1 - W:i + 1]
            roll_exp.append(round(_mean(win), 6))
            gp = sum(x for x in win if x > 0)
            gl = -sum(x for x in win if x < 0)
            roll_pf.append(_pf(gp, gl))
    cum_long, cum_short, cl, cs = [], [], 0.0, 0.0
    for t in trades:
        if t["side"] == "long":
            cl += t["pnl"]
        else:
            cs += t["pnl"]
        cum_long.append(round(cl, 4))
        cum_short.append(round(cs, 4))
    return {
        "n": n,
        "equity_curve": eq,
        "underwater_curve": uw,
        "max_drawdown": round(max_dd, 4),
        "longest_drawdown_trades": longest_dd,
        "rolling_window_trades": W,
        "rolling_expectancy": roll_exp,
        "rolling_profit_factor": roll_pf,
        "cum_long_pnl": cum_long,
        "cum_short_pnl": cum_short,
    }


def r_equity(trades):
    """Fixed-risk (R) equity + drawdown: each trade contributes pnl_r (equal
    initial risk per trade). Returns the cumulative-R curve, max drawdown in R,
    longest R-drawdown (trades), and long/short cumulative R. Additive helper —
    not part of full_report(), so existing reports are unchanged."""
    rs = [t.get("pnl_r") for t in trades]
    if not rs or any(x is None for x in rs):
        return {"n": 0, "note": "missing pnl_r on some trades"}
    cum, curve, peak, uw, max_dd, dd_len, longest = 0.0, [], 0.0, [], 0.0, 0, 0
    for x in rs:
        cum += x
        curve.append(round(cum, 6))
        peak = max(peak, cum)
        d = peak - cum
        uw.append(round(-d, 6))
        max_dd = max(max_dd, d)
        dd_len = 0 if d <= 1e-12 else dd_len + 1
        longest = max(longest, dd_len)
    cl = cs = 0.0
    cum_long, cum_short = [], []
    for t in trades:
        if t["side"] == "long":
            cl += t["pnl_r"]
        else:
            cs += t["pnl_r"]
        cum_long.append(round(cl, 6))
        cum_short.append(round(cs, 6))
    return {
        "n": len(rs),
        "cumulative_r": round(cum, 6),
        "r_equity_curve": curve,
        "r_underwater_curve": uw,
        "max_drawdown_r": round(max_dd, 6),
        "longest_drawdown_r_trades": longest,
        "cum_long_r": cum_long,
        "cum_short_r": cum_short,
    }


def distribution(trades):
    p = [t["pnl"] for t in trades]
    if not p:
        return {"n": 0}
    monthly = {}
    for t in trades:
        m = t["exit_bar"][:7]
        d = monthly.setdefault(m, [])
        d.append(t["pnl"])
    months = sorted(monthly)
    mo = {m: {"pnl": _r(sum(monthly[m]), 4), "n": len(monthly[m]),
              "expectancy": _r(_mean(monthly[m]))} for m in months}
    prof_months = sum(1 for m in months if sum(monthly[m]) > 0)
    # streaks
    max_w = max_l = cur_w = cur_l = 0
    for x in p:
        if x > 0:
            cur_w += 1; cur_l = 0
        elif x < 0:
            cur_l += 1; cur_w = 0
        else:
            cur_w = cur_l = 0
        max_w = max(max_w, cur_w); max_l = max(max_l, cur_l)
    return {
        "monthly": mo,
        "n_months": len(months),
        "profitable_months": prof_months,
        "pct_profitable_months": _r(100.0 * prof_months / len(months), 4),
        "pnl_histogram": _hist(p, PNL_BIN_WIDTH),
        "duration_histogram": _hist([t["bars_held"] for t in trades], DUR_BIN_WIDTH),
        "max_consecutive_wins": max_w,
        "max_consecutive_losses": max_l,
    }


def outlier_concentration(trades):
    p = sorted((t["pnl"] for t in trades), reverse=True)
    n = len(p)
    if n == 0:
        return {"n": 0}
    net = sum(p)
    gross_profit = sum(x for x in p if x > 0)   # stable denominator (net can be <0)

    def contrib(k):
        k = min(k, n)
        return {"n": k, "pnl": _r(sum(p[:k]), 4),
                "pct_of_gross_profit": _r(100.0 * sum(p[:k]) / gross_profit, 4)
                                       if gross_profit > 0 else None}

    def net_without_best(k):
        k = min(k, n)
        return _r(sum(p[k:]), 4)

    top1pct = max(1, int(round(0.01 * n)))
    return {
        "net_pnl": _r(net, 4),
        "gross_profit": _r(gross_profit, 4),
        "best_1": contrib(1), "best_5": contrib(5),
        "best_10": contrib(10), "best_20": contrib(20),
        "top_1pct": {**contrib(top1pct), "k": top1pct},
        "net_excl_best_1": net_without_best(1),
        "net_excl_best_5": net_without_best(5),
        "net_excl_best_10": net_without_best(10),
        "note": "robustness diagnostics only — removals are NOT alternate "
                "strategies.",
    }


def bootstrap_ci(trades, seed=BOOTSTRAP_SEED, B=BOOTSTRAP_B):
    p = [t["pnl"] for t in trades]
    n = len(p)
    if n < 2:
        return {"n": n, "note": "too few trades"}
    rng = random.Random(seed)

    def pct(sorted_means, q):
        idx = min(len(sorted_means) - 1, int(q * len(sorted_means)))
        return round(sorted_means[idx], 6)

    # IID bootstrap (PROVISIONAL — ignores serial dependence)
    iid = []
    for _ in range(B):
        s = 0.0
        for _ in range(n):
            s += p[rng.randrange(n)]
        iid.append(s / n)
    iid.sort()

    # fixed-block (moving-block) bootstrap — block length = round(n**(1/3))
    L = max(1, int(round(n ** (1.0 / 3.0))))
    nblocks = math.ceil(n / L)
    rng2 = random.Random(seed + 1)
    blk = []
    for _ in range(B):
        vals = []
        for _ in range(nblocks):
            start = rng2.randrange(n)
            for j in range(L):
                vals.append(p[(start + j) % n])
        vals = vals[:n]
        blk.append(sum(vals) / n)
    blk.sort()

    return {
        "n": n, "B": B, "seed": seed,
        "mean_expectancy": _r(_mean(p)),
        "iid_ci95": [pct(iid, 0.025), pct(iid, 0.975)],
        "iid_label": "PROVISIONAL — IID resampling ignores possible serial "
                     "dependence in trade outcomes",
        "block_len": L,
        "block_ci95": [pct(blk, 0.025), pct(blk, 0.975)],
        "block_label": f"moving-block bootstrap, block length {L} = round(n^(1/3)) "
                       "(rule-of-thumb, not tuned against results)",
    }


def portfolio_metrics(trades):
    p = [t["pnl"] for t in trades]
    n = len(p)
    if n < 2:
        return {"n": n}
    mu = _mean(p)
    sd = _stdev(p)
    downs = [min(0.0, x) for x in p]
    dd = math.sqrt(sum(x * x for x in downs) / n)
    # trades/year from the span, for a labelled annualization
    try:
        y0 = trades[0]["entry_bar"][:4]
        y1 = trades[-1]["exit_bar"][:4]
        span_days = (int(y1) - int(y0)) or 1
        # better: use actual dates
        import datetime as dt
        d0 = dt.date.fromisoformat(trades[0]["entry_bar"][:10])
        d1 = dt.date.fromisoformat(trades[-1]["exit_bar"][:10])
        years = max((d1 - d0).days / 365.25, 1e-9)
        tpy = n / years
    except Exception:
        tpy, years = None, None
    sharpe = round(mu / sd, 6) if sd > 0 else None
    sortino = round(mu / dd, 6) if dd > 0 else None
    ann = {}
    if tpy:
        f = math.sqrt(tpy)
        ann = {"trades_per_year_assumed": round(tpy, 2),
               "sharpe_annualized": round(sharpe * f, 6) if sharpe is not None else None,
               "sortino_annualized": round(sortino * f, 6) if sortino is not None else None,
               "label": "ANNUALIZED via sqrt(trades/year) from the trade span — "
                        "assumption-dependent"}
    return {
        "n": n,
        "sharpe_per_trade": sharpe,
        "sortino_per_trade": sortino,
        "downside_deviation": _r(dd),
        "annualized": ann,
        "deferred": {
            "CAGR": "DEFERRED — ACCOUNT-CONSTRUCTION-DEPENDENT (fixed 1-share vs "
                    "$50k = arbitrary capital utilization); not a discovery metric",
            "Calmar": "DEFERRED — depends on CAGR (see above)",
        },
    }


def full_report(trades):
    return {
        "trade_metrics": trade_metrics(trades),
        "r_metrics": r_metrics(trades),
        "equity": equity_series(trades),
        "distribution": distribution(trades),
        "outliers": outlier_concentration(trades),
        "bootstrap": bootstrap_ci(trades),
        "portfolio": portfolio_metrics(trades),
    }


# ---------------------------------------------------------------------------
# raw vs screened dual report + controlled A/B mode
# ---------------------------------------------------------------------------
_HEADLINE = ["net_pnl", "expectancy", "median_pnl", "win_rate_pct",
             "profit_factor", "payoff_ratio", "avg_bars_held"]


def _headline(tm):
    out = {k: tm.get(k) for k in _HEADLINE}
    out["n"] = tm.get("n")
    out["max_drawdown"] = None
    return out


def dual_report(fast, slow, mask_t_ms=None):
    """Screened (primary) + raw (sensitivity) + delta, running the engine both
    ways. `mask_t_ms` is the frozen HIGH-CONFIDENCE corpus mask; if None the
    module loads CORPUS_MASK_v1.0.json next to this file."""
    import json
    import fastalpha_engine as fe
    if mask_t_ms is None:
        here = os.path.dirname(os.path.abspath(__file__))
        mask_t_ms = json.load(open(os.path.join(here, "CORPUS_MASK_v1.0.json")))["mask_t_ms"]
    drop = set(mask_t_ms)
    screened = fe.simulate(fe.compute_feature_rows(fast, slow, drop_t_ms=drop))
    raw = fe.simulate(fe.compute_feature_rows(fast, slow))
    rs, rr = full_report(screened), full_report(raw)
    ts_s, ts_r = rs["trade_metrics"], rr["trade_metrics"]

    def d(a, b):
        return round(a - b, 6) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None

    delta = {k: d(ts_s.get(k), ts_r.get(k)) for k in _HEADLINE + ["n"]}
    delta["max_drawdown"] = d(rs["equity"].get("max_drawdown"),
                              rr["equity"].get("max_drawdown"))
    return {
        "arm": f"EMA {fast}/{slow}",
        "primary_view": "screened",
        "screened": rs, "raw": rr,
        "screened_minus_raw_headline": delta,
        "mask_bars": len(drop),
        "note": "screened corpus (frozen CORPUS_MASK_v1.0) is primary; raw is "
                "mandatory sensitivity evidence. Both are reported; neither the "
                "corpus nor the mask is altered here.",
    }


def ab_report(control, variant, label_control="control", label_variant="variant"):
    """Controlled A/B on two trade sets (same view). Reports metric deltas and
    entry-set overlap. Causality is not inferred beyond the changed parameter."""
    def d(a, b):
        return round(a - b, 6) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None
    tc, tv = trade_metrics(control), trade_metrics(variant)
    ec = {(t["entry_bar"], t["side"]) for t in control}
    ev = {(t["entry_bar"], t["side"]) for t in variant}
    inter, union = ec & ev, ec | ev
    cby = {(t["entry_bar"], t["side"]): t for t in control}
    vby = {(t["entry_bar"], t["side"]): t for t in variant}
    changed = sum(1 for k in inter
                  if (cby[k]["exit_bar"], cby[k]["exit_reason"], cby[k]["pnl"])
                  != (vby[k]["exit_bar"], vby[k]["exit_reason"], vby[k]["pnl"]))
    deltas = {k: d(tv.get(k), tc.get(k)) for k in _HEADLINE + ["n"]}
    deltas["long_net_pnl"] = d(tv["long"]["net_pnl"], tc["long"]["net_pnl"])
    deltas["short_net_pnl"] = d(tv["short"]["net_pnl"], tc["short"]["net_pnl"])
    return {
        "control": label_control, "variant": label_variant,
        "control_metrics": tc, "variant_metrics": tv,
        "variant_minus_control": deltas,
        "entry_overlap": {
            "shared": len(inter), "control_total": len(ec), "variant_total": len(ev),
            "trades_added": len(ev - ec), "trades_removed": len(ec - ev),
            "changed_exit_same_entry": changed,
            "jaccard": round(len(inter) / len(union), 6) if union else None,
        },
        "note": "Do not infer causality beyond the explicitly changed parameter.",
    }


def ab_dual(control_screened, variant_screened, control_raw, variant_raw,
            label="experiment"):
    """A/B under BOTH views, plus whether screened and raw AGREE on the sign of
    the headline net-P/L effect."""
    scr = ab_report(control_screened, variant_screened, "control", "variant")
    raw = ab_report(control_raw, variant_raw, "control", "variant")
    ds = scr["variant_minus_control"]["net_pnl"]
    dr = raw["variant_minus_control"]["net_pnl"]
    agree = (ds is not None and dr is not None
             and ((ds > 0) == (dr > 0) or (ds == 0 and dr == 0)))
    return {
        "experiment": label,
        "screened": scr, "raw": raw,
        "screened_net_delta": ds, "raw_net_delta": dr,
        "views_agree_on_direction": bool(agree),
        "primary_view": "screened",
    }


# ---------------------------------------------------------------------------
# optional pure-stdlib SVG (derived from canonical series; no plotting library)
# ---------------------------------------------------------------------------
def equity_drawdown_svg(equity, underwater, w=900, h=320, title="V0 equity"):
    """Two stacked panels (equity, underwater) as a self-contained SVG string,
    derived purely from the canonical numeric series."""
    def poly(series, y0, y1, color, fill=None):
        if not series:
            return ""
        lo, hi = min(series), max(series)
        rng = (hi - lo) or 1.0
        n = len(series)
        pts = [(x / max(1, n - 1) * (w - 60) + 50,
                y1 - (v - lo) / rng * (y1 - y0)) for x, v in enumerate(series)]
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        el = ""
        if fill:
            el += (f'<polygon points="50,{y1:.1f} {d} {pts[-1][0]:.1f},{y1:.1f}" '
                   f'fill="{fill}" opacity="0.25"/>')
        el += f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="1.5"/>'
        el += (f'<text x="50" y="{y0-4:.0f}" font-size="11" fill="#888">'
               f'{title} [{lo:.1f}..{hi:.1f}]</text>')
        return el
    body = poly(equity, 24, 150, "#2b8a3e", "#2b8a3e")
    body += poly(underwater, 190, 300, "#c92a2a", "#c92a2a")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="sans-serif">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>'
            f'<text x="50" y="16" font-size="12" fill="#333">'
            f'FastAlpha tear sheet — cumulative P/L (top) and underwater (bottom), '
            f'trade index</text>{body}</svg>')
