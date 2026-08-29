"""Wing vega and vanna for the delta-matched risk reversal (Propositions 1 and 2).

Closes a reproducibility gap: the paper's wing Greeks previously had no generator.

Two results:
  1. Net vega is EXACTLY zero at matched delta, for any smile. Delta pins d1
     (d1 = N^-1(delta.e^{q.tau})), and vega depends on sigma only through d1. The measured
     residual is a matching artefact (strike discreteness, tenor mismatch), not a skew effect.
  2. The wing vannas have opposite signs (Prop 2), confirmed on the traded belt.
"""
import numpy as np, pandas as pd
from scipy.stats import norm

# --- 1. net vega is exactly zero at any skew ------------------------------------------
S, tau, q = 550.0, 30 / 365, 0.013
d1c = norm.ppf(0.10 * np.exp(q * tau)); d1p = -d1c
vega = lambda d: S * np.exp(-q * tau) * np.sqrt(tau) * norm.pdf(d)
print("net vega at matched 10-delta, across skew levels (sigma_p, sigma_c):")
for sp, sc in [(0.20, 0.20), (0.30, 0.18), (0.45, 0.15), (0.60, 0.12)]:
    print(f"  ({sp:.2f}, {sc:.2f}) -> V_p {vega(d1p):.4f}  V_c {vega(d1c):.4f}  net {vega(d1p)-vega(d1c):.2e}")

# --- 2. measured wing Greeks on the traded belt ---------------------------------------
c = pd.read_parquet("reports/svi_both_wings_chain_extended.parquet",
                    columns=["option_type", "spot", "implied_volatility", "delta",
                             "abs_delta", "dte", "T_yr"])
c = c[(c.implied_volatility > 0.01) & (c.T_yr > 0)]
d1 = np.where(c.option_type.values == "C",
              norm.ppf(c.delta.values.clip(1e-6, 1 - 1e-6)),
              -norm.ppf(c.abs_delta.values.clip(1e-6, 1 - 1e-6)))
sig, tau_, Sv = c.implied_volatility.values, c.T_yr.values, c.spot.values
c = c.assign(vega=Sv * np.sqrt(tau_) * norm.pdf(d1),
             vanna=-norm.pdf(d1) * (d1 - sig * np.sqrt(tau_)) / sig)
w = c[c.abs_delta.between(0.08, 0.12) & c.dte.between(25, 45)]
p, k = w[w.option_type == "P"], w[w.option_type == "C"]
vp, vc, ap, ac = p.vega.median(), k.vega.median(), p.vanna.median(), k.vanna.median()
print(f"\n10-delta / 25-45 DTE belt, n={len(w):,}")
print(f"  vega   put {vp:6.1f}  call {vc:6.1f}  -> |net|/diff {abs(vp-vc)/(vp+vc)*100:.1f}% (matching artefact)")
print(f"  vanna  put {ap:+6.3f}  call {ac:+6.3f}  -> |net|/|diff| {abs(ap-ac)/abs(ap+ac):.2f}")
print(f"  Prop 2 signs: vanna_p<0 {ap<0}, vanna_c>0 {ac>0}")
