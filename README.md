# Blaque Baux Borough

**Municipal / tax-exempt RV — a tax-advantaged carry edge, and does the muni/Treasury ratio mean-revert?**

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/borough_1.py   # needs Alpaca data keys in the environment
```

Munis (MUB/VTEB) vs Treasuries (IEF), plus leveraged muni CEFs.

## Finding (conditional — for a taxable holder)
- **Tax-advantaged carry is real:** munis +2.1%/yr (~**+3.3% tax-equivalent** at 37%) at low vol (5%), Sharpe **+0.46** vs IEF +0.19 — after tax this beats Treasuries for the right holder.
- **Ratio RV is thin** (Sharpe +0.02 — it drifts more than it reverts), and **leveraged muni CEFs** add return (+0.29 Sharpe) with a rate/liquidity tail (skew −1.53, maxDD −37%).

## Verdict
**CONDITIONAL KEEPER for taxable capital.** The edge *is the tax exemption* — low-vol tax-advantaged income, not pre-tax alpha. `borough_2` = real after-tax accounting (AMT, state) + CEF NAV discounts.

## Status
**Research.** Honest white-space study — verdict falls where it falls, proxy limits named, `borough_2` path noted. Fat-tail scorecard, causal, Alpaca SIP daily total return. No live capital.
