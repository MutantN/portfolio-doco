**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard Theory

## The Big Idea

The dashboard takes a set of stocks, learns from their historical return patterns, and then looks for portfolio weight mixes that suit different goals.

In plain terms:

- it estimates expected return from historical data

- it can also estimate modeled returns from analyst target upside

- it estimates how the stocks move together

- it samples many candidate portfolios

- it keeps the portfolios that best fit each objective

- it reports return, volatility, Sharpe ratio, and VaR-style risk summaries

---

## Notation

- $n$ = number of assets
- $\mathbf{w} = (w_1, \dots, w_n)^\top$ = portfolio weights
- $\boldsymbol{\mu}$ = annualized expected return vector
- $\boldsymbol{\Sigma}$ = annualized covariance matrix
- $R_f = 0.04$ = fixed annual risk-free rate in the current production app

The current production app keeps the rules simple:

- $w_i \ge 0$

- $\sum_i w_i = 1$

---

## The Core Numbers

### Expected Return

$$
R_p = \mathbf{w}^\top \boldsymbol{\mu}
$$

### Volatility

$$
\sigma_p = \sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}
$$

### Sharpe Ratio

$$
\text{Sharpe} = \frac{R_p - R_f}{\sigma_p}
$$

The dashboard uses this fixed-rate Sharpe formula when it ranks portfolios.

---

## The Three Main Portfolio Views

### Best Min Variance by Sharpe

This is the lowest-volatility family of portfolios filtered for the strongest Sharpe outcome inside that group.

$$
\min_{\mathbf{w}} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}
$$

### Best Max Sharpe

This is the dashboard's strongest risk-adjusted portfolio.

$$
\max_{\mathbf{w}} \frac{\mathbf{w}^\top \boldsymbol{\mu} - R_f}{\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}}
$$

### True Min Variance

This is the absolute lowest-volatility portfolio the search keeps, even if its return is less attractive.

$$
\min_{\mathbf{w}} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}
$$

---

## How The Search Works

The production dashboard does **not** use a formal quadratic solver for the live UI path. Instead, it generates many random long-only weight sets and keeps the best candidates for each objective.

## Optimization Method

The dashboard uses a Monte Carlo search heuristic.

In practice, that means:

- it generates many random long-only weight sets

- each weight set is normalized so total allocation sums to 1

- each candidate portfolio is scored using return, volatility, and Sharpe ratio

- the dashboard keeps the strongest candidate for the relevant objective

- the search runs repeatedly with seeded randomness so the same simulation can be reproduced

The current implementation samples 2,000 candidate weight sets per optimization pass.

### Random weight generation

If random positive weights $u_i$ are drawn, production normalizes them as:

$$
w_i = \frac{u_i}{\sum_{j=1}^{n} u_j}
$$

That guarantees:

- all weights are non-negative

- total allocation sums to 1

---

## How Historical Data Becomes Portfolio Inputs

The app builds daily returns from Yahoo Finance price history and annualizes them using a 252-trading-day convention.

### Annualized mean return

$$
\mu_i = 252 \cdot \frac{1}{T} \sum_{t=1}^{T} r_{it}
$$

### Annualized covariance

$$
\sigma_{ij} = 252 \cdot \text{Cov}(r_i, r_j)
$$

---

## How Modeled Returns Work

The dashboard also supports a modeled return mode.

Instead of relying only on historical annualized mean returns, it can blend:

- target-implied return from analyst targets

- historical annualized mean return

The target-implied return is conceptually:

$$
\text{implied return} = \frac{\text{target price}}{\text{current price}} - 1
$$

That implied return is then blended with the historical mean.

The blend weight increases with analyst confidence, which is proxied by analyst count.

In practical terms:

- more analyst coverage gives more weight to the modeled return

- less analyst coverage leaves more weight on the historical mean

- covariance remains historical even when returns are modeled

So the modeled mode changes the expected return vector, but not the covariance matrix.

---

## How Risk Is Presented

### Historical VaR proxy

This is the more intuitive setting. It looks back through realized history and asks, “what was the worst rolling loss over this period?”

### Parametric VaR

The app also supports a smoother, model-based normal approximation.

$$
\text{VaR} = \mu_{\text{annual}} + z_p \sigma_{\text{annual}}
$$

where the left-tail probability is interpreted as `1 / N years`.

---

## Where Live Data Fits In

The optimization engine is still driven by historical returns and covariance, but the dashboard adds live market context on top:

- Finnhub quote data for latest price

- FMP analyst target consensus and rating data

These fields do not replace the optimization model. They help explain what the simulated portfolios look like in the market right now.

---

## Important Limits

- no shorting

- no leverage

- no transaction costs

- no taxes

- no slippage

- no liquidity modeling

- no deterministic frontier solver

This is an exploratory portfolio analysis tool, not an order management or execution system.
