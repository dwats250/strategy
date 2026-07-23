#!/usr/bin/env python3
"""
REPRODUCE_CAMPAIGN v1.0 · 2026-07-22
Supersedes the final3 stub (which contained documentation, not code).
Self-contained reproduction of every headline campaign number from the
four archived deep exports. Exits nonzero if any assertion fails.

Inputs (must sit beside this script's parent dir or pass a dir arg):
  deep_R1_SPY_C0_TX30_2010-2026_v0.3.0.csv
  deep_R3_SPY_C0_TX15_2010-2026_v0.3.0.csv
  deep_R4_SPY_C0_TX60_2010-2026_v0.3.0.csv
  deep_R2_QQQ_2016-2026_v1.1.7.csv

Method notes:
  * bps returns are price-derived: dir*(exit-entry)/entry*1e4.
  * Governing intervals: monthly-block bootstrap, 20,000 resamples,
    numpy default_rng(seed=7).
  * H2 equity path is an EQUITY-NORMALIZED RECONSTRUCTION:
    r_i = pnl_i / (25000 + cum P&L of ALL prior trades), compounded
    over VALID trades only (valid = exit comment != ORPHAN and entry
    date == exit date). Equivalent to recursively rescaling P&L by
    clean/TradingView equity (continuous-share approximation).
  * H2 slice endpoint: entries THROUGH 2023-02-17 inclusive, i.e.
    entry timestamp < 2023-02-18 00:00. (The first analysis pass used
    <= Timestamp('2023-02-17') = midnight and wrongly dropped Feb 17.)
  * Both PF bases reported; manifest never specified one -> criterion
    scored NOT CLEANLY PASSED.
"""
import sys, os, hashlib
import numpy as np, pandas as pd
from math import erf

DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..')
FILES = {
 'R1':'deep_R1_SPY_C0_TX30_2010-2026_v0.3.0.csv',
 'R3':'deep_R3_SPY_C0_TX15_2010-2026_v0.3.0.csv',
 'R4':'deep_R4_SPY_C0_TX60_2010-2026_v0.3.0.csv',
 'R2':'deep_R2_QQQ_2016-2026_v1.1.7.csv'}

print("package versions: python %s | pandas %s | numpy %s" %
      (sys.version.split()[0], pd.__version__, np.__version__))
for k,f in FILES.items():
    p=os.path.join(DIR,f)
    print("sha256 %s  %s" % (hashlib.sha256(open(p,'rb').read()).hexdigest()[:16], f))

def load(key):
    df=pd.read_csv(os.path.join(DIR,FILES[key]),encoding='utf-8-sig')
    df.columns=[c.strip() for c in df.columns]
    df['dt']=pd.to_datetime(df['Date and time'])
    e=df[df['Type'].str.contains('Entry')].set_index('Trade number')
    x=df[df['Type'].str.contains('Exit')].set_index('Trade number')
    d=np.where(e['Type'].str.contains('long'),1,-1)
    t=pd.DataFrame({'edt':e['dt'].values,'xdt':x['dt'].values,'dir':d,
        'epx':e['Price USD'].values,'xpx':x['Price USD'].values,
        'qty':e['Size (qty)'].values,'pnl':e['Net PnL USD'].values,
        'xsig':x['Signal'].values})
    t['bps']=t['dir']*(t['xpx']-t['epx'])/t['epx']*1e4
    t['date']=pd.to_datetime(t['edt']).dt.date; t['xdate']=pd.to_datetime(t['xdt']).dt.date
    t['mon']=pd.to_datetime(t['edt']).dt.to_period('M')
    t['et']=pd.to_datetime(t['edt']).dt.strftime('%H:%M')
    return t.sort_values('edt').reset_index(drop=True)

def block_ci(v,mon,n=20000,seed=7):
    rng=np.random.default_rng(seed); g=[v[mon==m] for m in pd.unique(mon)]
    k=len(g); o=np.empty(n)
    for i in range(n): o[i]=np.concatenate([g[j] for j in rng.integers(0,k,k)]).mean()
    return np.percentile(o,[2.5,97.5])

def welch_p(a,b):
    d=b.mean()-a.mean(); se=np.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))
    t=d/se; return d,t,2*(1-0.5*(1+erf(abs(t)/np.sqrt(2))))

fails=[]
def check(name,cond,detail=""):
    print(("PASS " if cond else "FAIL ")+name+(" · "+detail if detail else ""))
    if not cond: fails.append(name)

# ── H1 ──
R1=load('R1'); v=R1['bps'].values
lo,hi=block_ci(v,R1['mon'].values)
print(f"\nH1  n={len(v)}  mean {v.mean():+.3f}  block CI [{lo:+.3f},{hi:+.3f}]")
check("H1 n==3300", len(v)==3300)
check("H1 mean == -0.380", abs(v.mean()-(-0.380))<0.005, f"{v.mean():+.4f}")
check("H1 CI upper < +1.0 (closure rule)", hi<1.0, f"upper {hi:+.3f}")

# ── H3 (R4/TX60, OOS pre-2025-01-21) ──
R4=load('R4'); oos=R4[pd.to_datetime(R4['edt'])<pd.Timestamp('2025-01-21')]
bd=oos[oos['et']=='07:30']['bps'].values; nb=oos[oos['et']!='07:30']['bps'].values
d3,t3,p3=welch_p(nb,bd)  # boundary minus non-boundary
print(f"\nH3  contrast {d3:+.3f} bps  t={t3:+.2f} p={p3:.3f}")
check("H3 contrast negative (in-sample +5.52 failed OOS)", d3<0, f"{d3:+.3f}")

# ── H4 (R1, OOS) ──
o1=R1[pd.to_datetime(R1['edt'])<pd.Timestamp('2025-01-21')]
d4,t4,p4=welch_p(o1[o1['dir']==1]['bps'].values,o1[o1['dir']==-1]['bps'].values)
print(f"H4  short−long {d4:+.3f} bps  p={p4:.3f}")
check("H4 |gap| < 1 bps (in-sample -3.4 failed OOS)", abs(d4)<1.0, f"{d4:+.3f}")

# ── H2 ──
R2=load('R2')
R2['valid']=(R2['xsig']!='ORPHAN')&(R2['xdate']==R2['date'])
eqb=25000+np.concatenate([[0],np.cumsum(R2['pnl'].values)[:-1]])
R2['r']=R2['pnl']/eqb; R2['rbps']=R2['r']*1e4
cut=pd.Timestamp('2023-02-18')            # Feb 17 INCLUSIVE
paper=R2[pd.to_datetime(R2['edt'])<cut]; post=R2[pd.to_datetime(R2['edt'])>=cut]
pv=paper[paper['valid']]
equity=25000*np.prod(1+pv['r'].values)
pf_norm=pv['rbps'][pv['rbps']>0].sum()/abs(pv['rbps'][pv['rbps']<=0].sum())
pf_dollar=pv['pnl'][pv['pnl']>0].sum()/abs(pv['pnl'][pv['pnl']<=0].sum())
print(f"\nH2  paper slice trades={len(paper)} valid={len(pv)}  equity ${equity:,.2f}")
print(f"    PF(normalized)={pf_norm:.4f}  PF(dollar)={pf_dollar:.4f}  threshold 1.20")
check("H2 trades == 1769", len(paper)==1769)
check("H2 valid == 1766", len(pv)==1766)
check("H2 equity == $212,426.75 (±$1)", abs(equity-212426.75)<1.0, f"${equity:,.2f}")
check("H2 orphans/cross-session == 3", int((~R2['valid']).sum())==3)
check("H2 PF straddles 1.20 -> NOT CLEANLY PASSED", pf_dollar<1.20<pf_norm,
      f"{pf_dollar:.3f} < 1.20 < {pf_norm:.3f}")
postv=post[post['valid']]
plo,phi=block_ci(postv['rbps'].values,pd.to_datetime(postv['edt']).dt.to_period('M').values)
dd,td,pd_=welch_p(pv['rbps'].values,postv['rbps'].values)
print(f"    post-paper n={len(postv)} mean {postv['rbps'].mean():+.2f} bps  CI [{plo:+.2f},{phi:+.2f}]  deterioration {dd:+.2f} p={pd_:.3f}")
check("post-paper CI spans 0 (persistence NOT established)", plo<0<phi)

print()
if fails: print("REPRODUCTION FAILED:",fails); sys.exit(1)
print("ALL ASSERTIONS PASSED — campaign numbers reproduce from the archived exports.")
