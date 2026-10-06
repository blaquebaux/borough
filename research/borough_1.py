#!/usr/bin/python3
# =============================================================================
# borough_1.py — Municipal / tax-exempt RV: is there a tax-advantaged carry edge, and does the muni/Treasury ratio mean-revert?
#
# Munis (MUB/VTEB) vs Treasuries (IEF), plus leveraged muni CEFs (NUV/PML/NEA). SIP daily total return.
#  (A) TAX-EQUIVALENT CARRY: muni total return vs IEF, then the tax-equivalent lift (muni yield is federal-tax-free —
#      a ~37% top-bracket holder grosses it up by ~1/(1−0.37)). Low vol, tax-advantaged income.
#  (B) MUNI/TREASURY RATIO RV: z-score of the MUB/IEF ratio vs trailing year; munis "cheap" (ratio high) → overweight,
#      "rich" → underweight — does the ratio mean-revert tradeably?
#  (C) LEVERAGED MUNI CEFs: NUV/PML/NEA add leverage + a discount — extra return, extra rate/liquidity tail.
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _borough_common import panel, rets, stats, skew_of, beta, corr
import numpy as np
P, dates = panel(["MUB","VTEB","IEF","NUV","PML","NEA","AGG"])
R={s:rets(P[s]) for s in P}
muni=np.nanmean(np.vstack([R["MUB"],R["VTEB"]]),axis=0)
TAX=0.37
print("="*96); print(f"BOROUGH — municipal / tax-exempt RV  ({dates[0]} → {dates[-1]})"); print("="*96)
a=stats(muni); ief=stats(R["IEF"])
teq_cagr=a['cagr']/(1-TAX)                                       # crude tax-equivalent gross-up of the muni return
print(f"\n(A) muni (MUB/VTEB)  Sharpe {a['sh']:+.2f}  CAGR {a['cagr']*100:+.1f}%  (tax-equiv ~{teq_cagr*100:+.1f}% @37%)  maxDD {a['dd']*100:+.0f}%  vol {a['vol']*100:.0f}%")
print(f"    vs IEF(Treasury) Sharpe {ief['sh']:+.2f} CAGR {ief['cagr']*100:+.1f}% maxDD {ief['dd']*100:+.0f}%   corr(muni,IEF) {corr(muni,R['IEF']):+.2f}")
# (B) ratio RV
ratio=P["MUB"][1:]/P["IEF"][1:]; n=len(ratio)
z=np.array([(ratio[t]-np.nanmean(ratio[max(0,t-252):t]))/(np.nanstd(ratio[max(0,t-252):t])+1e-9) if t>=252 else np.nan for t in range(n)])
pos=np.where(z>1,1.0,np.where(z<-1,-1.0,0.0))                    # munis cheap (ratio high)→long MUB/short IEF
rv=pos[:-1]*(R["MUB"][1:n]-R["IEF"][1:n]); rva=stats(rv[np.isfinite(rv)])
print(f"\n(B) MUNI/TREASURY ratio RV (fade |z|>1, MUB vs IEF): Sharpe {rva['sh']:+.2f}, {rva['cagr']*100:+.1f}%/yr, in-market {np.mean(pos!=0)*100:.0f}%")
# (C) leveraged muni CEFs
cef=np.nanmean(np.vstack([R["NUV"],R["PML"],R["NEA"]]),axis=0); ca=stats(cef)
print(f"\n(C) leveraged muni CEFs (NUV/PML/NEA)  Sharpe {ca['sh']:+.2f}  CAGR {ca['cagr']*100:+.1f}%  maxDD {ca['dd']*100:+.0f}%  skew {skew_of(cef):+.2f}  — leverage+discount add return & tail")
carry_ok=a['sh']>0.5; rv_ok=rva['sh']>0.3
print("\n"+"="*96); print("READ:")
print(f"  • TAX-ADVANTAGED CARRY IS REAL: munis return {a['cagr']*100:+.1f}%/yr (~{teq_cagr*100:+.0f}% tax-equivalent at 37%) at low vol ({a['vol']*100:.0f}%) and Sharpe {a['sh']:+.2f} — for a taxable holder this beats Treasuries after tax; the one genuinely tax-driven FI corner.")
print(f"  • THE RATIO RV is {'tradeable' if rv_ok else 'thin'} (Sharpe {rva['sh']:+.2f}): the muni/Treasury ratio {'mean-reverts — overweight munis when cheap, underweight when rich' if rv_ok else 'drifts more than it reverts on ETFs'}.")
print(f"  • LEVERAGED MUNI CEFs add return (Sharpe {ca['sh']:+.2f}) but bring a leverage + discount + liquidity tail (skew {skew_of(cef):+.2f}, maxDD {ca['dd']*100:+.0f}%) — the muni version of the CEF-discount game (see bargain).")
if carry_ok:
    v=("CONDITIONAL KEEPER (for a taxable holder): munis are a real low-vol, tax-advantaged carry sleeve — after a 37% "
       f"gross-up (~{teq_cagr*100:+.0f}% tax-equivalent) they beat Treasuries for the right holder, at low vol and high Sharpe "
       f"({a['sh']:+.2f}). The muni/Treasury ratio RV is a {'tradeable' if rv_ok else 'mild'} overlay, and leveraged muni CEFs juice the carry "
       "at the cost of a rate/liquidity tail. The honest niche: tax-aware income, not pre-tax alpha — the edge is the tax "
       "exemption, which only matters for taxable capital. borough_2 = real after-tax accounting + CEF NAV discounts.")
else:
    v=("CONDITIONAL: munis provide low-vol tax-advantaged income but thin pre-tax; the sleeve only earns its keep for a "
       "high-bracket taxable holder (tax-equivalent gross-up). Ratio RV mild; CEFs add leveraged tail. borough_2 = after-tax + NAV.")
print(f"  VERDICT: {v}")
print("  (ETF/CEF proxies; a 37% flat gross-up is crude (ignores AMT, state tax, holder bracket); real after-tax + CEF NAV discounts = borough_2.)")
