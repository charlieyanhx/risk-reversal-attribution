import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.size": 9, "figure.dpi": 150})
labels = ["slope\nvega", "vanna", "carry\n(theta+gamma)", "level\nvega", "volga, costs,\nresidual"]
pt = [128, -59, 59, -19, -9]
lo = [47, -195, -32, -88, np.nan]
hi = [307, 15, 161, 37, np.nan]
fig, ax = plt.subplots(figsize=(5.6, 3.2))
colors = ["#31567a" if v > 0 else "#a63d40" for v in pt]
ax.bar(range(5), pt, 0.55, color=colors)
err_lo = [pt[i]-lo[i] if not np.isnan(lo[i]) else 0 for i in range(5)]
err_hi = [hi[i]-pt[i] if not np.isnan(hi[i]) else 0 for i in range(5)]
ax.errorbar(range(4), pt[:4], yerr=[err_lo[:4], err_hi[:4]], fmt="none",
            ecolor="black", capsize=3, lw=1)
ax.axhline(0, color="black", lw=0.8)
ax.axhline(100, color="#888", lw=0.8, ls=":")
ax.text(4.4, 104, "net = 100%", fontsize=7, color="#555", ha="right")
for i, v in enumerate(pt):
    ax.text(i, (hi[i]+12 if not np.isnan(hi[i]) else v+8) if v > 0 else
               (lo[i]-22 if not np.isnan(lo[i]) else v-16), f"{v:+d}%", ha="center", fontsize=8)
ax.set_ylabel("share of net P&L (%), 95% block-bootstrap CI")
ax.set_xticks(range(5)); ax.set_xticklabels(labels, fontsize=8)
ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig("fig_p4_attribution.pdf")
print("ok")
