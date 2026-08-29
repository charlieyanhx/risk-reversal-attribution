# Delta-Matched Risk Reversal — Attribution

Code and data-availability statement for:

> **A Formal Theory of the Delta-Matched Risk Reversal: Slope Vega, Irreducible Vanna, and a Dollar-Reconciling Attribution**
> Charlie Yan, 2026. [`paper/p4_delta_matched_rr.pdf`](paper/p4_delta_matched_rr.pdf)

## What the paper claims

A delta-matched risk reversal is a near-pure differential-vega instrument carrying an irreducible vanna coupling. The vanna term is the tax on the harvest, not its source — refuting the standard vanna-centric account of the structure.

**Headline result.** Attribution as shares of net: **+128% slope vega, −59% vanna, +59% θ−γ carry, −19% residual level**, closing to 100% exactly. Slope-share sign stability 99.7%; the vanna share's interval marginally includes zero.

## Reproducibility

**PARTIALLY RUNNABLE — the bootstrap needs the persisted daily bucket series (not shipped; derived from licensed data).** The script is published so the interval construction is auditable: block bootstrap, 5,000 draws, 21-trading-day blocks.

**Operating parameters of the studied strategy are deliberately withheld** (entry bands, holding and exit rules, sizing). The structure and its Greek attribution are published; the trading rules are not.

## What is here

`code/p4_share_cis.py` — attribution-share confidence intervals.
`paper/` — paper and exhibit.

## Evidence conventions used throughout

Every performance figure in the paper carries its accounting basis inline. Unless labelled
otherwise: **line 3** = full cross-spread fills (buy at ask, sell at bid, every leg both ways),
ex-commission, marked to market daily, padded to the full business calendar. Figures labelled
**screen** are descriptive or information-coefficient statistics and are never annualised into a
Sharpe ratio. Numbers marked **invalid** appear only as invalidated examples, with the corrected
figure alongside.

All tests reported in the paper were pre-registered — horizons, controls, nulls and decision bars
fixed before execution — and deviations are recorded rather than edited away. Where pre-registration
documents exist in this repository they are included verbatim.

## Citation

```bibtex
@techreport{yan2026riskreversalattribution,
  title  = {A Formal Theory of the Delta-Matched Risk Reversal: Slope Vega, Irreducible Vanna, and a Dollar-Reconciling Attribution},
  author = {Yan, Charlie},
  year   = {2026},
  type   = {Working paper}
}
```

## License

Code MIT (see `LICENSE`). The paper PDF is © 2026 Charlie Yan, all rights reserved.
