"""P4 attribution-share CIs — block bootstrap on the persisted daily bucket series."""
import numpy as np, pandas as pd

d = pd.read_parquet("data/cache/skew_attribution_buckets.parquet")
print("columns:", list(d.columns))
print("rows:", len(d))
tot = "TOTAL" if "TOTAL" in d.columns else d.columns[-1]
# canonical buckets per the theory note
name = {"SLOPE": None}
cols = {c.lower(): c for c in d.columns}
def pick(*cands):
    for c in cands:
        if c.lower() in cols: return cols[c.lower()]
    return None
slope = pick("VegaSlp")
vanna = pick("Vanna")
theta = pick("Theta"); gamma = pick("Gamma")
lvl = pick("VegaLvl","Level","VegaLevel")
print("mapped:", slope, vanna, theta, gamma, lvl, "| total:", tot)

rng = np.random.default_rng(0)
n = len(d); bl = 21; k = int(np.ceil(n / bl)); NB = 5000
rows = []
for _ in range(NB):
    idx = np.concatenate([np.arange(s, min(s + bl, n)) for s in rng.integers(0, n - bl, k)])[:n]
    b = d.iloc[idx]
    net = b[tot].sum()
    if abs(net) < 1e-9: continue
    carry = (b[theta].sum() + b[gamma].sum()) / net * 100
    rows.append((b[slope].sum()/net*100, b[vanna].sum()/net*100, carry, b[lvl].sum()/net*100))
r = pd.DataFrame(rows, columns=["slope","vanna","carry","level"])
print(f"\npoint estimates (full sample): slope {d[slope].sum()/d[tot].sum()*100:+.0f}%  "
      f"vanna {d[vanna].sum()/d[tot].sum()*100:+.0f}%  "
      f"carry {(d[theta].sum()+d[gamma].sum())/d[tot].sum()*100:+.0f}%  "
      f"level {d[lvl].sum()/d[tot].sum()*100:+.0f}%")
print(f"\nblock-bootstrap 95% CIs on shares of net ({len(r):,} draws, block=21d):")
for c in r.columns:
    print(f"  {c:>6}: [{r[c].quantile(.025):+7.0f}%, {r[c].quantile(.975):+7.0f}%]  median {r[c].median():+6.0f}%")
print("\nsign stability (share of draws with the point-estimate sign):")
for c, s in [("slope",1),("vanna",-1),("carry",1),("level",-1)]:
    print(f"  {c:>6}: {100*(np.sign(r[c])==s).mean():.1f}%")
