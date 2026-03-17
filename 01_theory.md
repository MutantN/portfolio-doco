**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard Theory

## Problem Framing

The production dashboard models a long-only portfolio over a selected stock universe. It estimates annualized returns and covariance from historical data, searches for candidate portfolios with Monte Carlo weight generation, and reports risk and performance measures for multiple portfolio objectives.

---

## Notation

- $n$ = number of assets
- $\mathbf{w} = (w_1, \dots, w_n)^\top$ = portfolio weights
- $\boldsymbol{\mu}$ = annualized expected return vector
- $\boldsymbol{\Sigma}$ = annualized covariance matrix
- $R_f = 0.04$ = fixed annual risk-free rate in the current production app

Constraints in production:

- $w_i \ge 0$
- $\sum_i w_i = 1$

---

## Portfolio Statistics

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

The dashboard uses this exact fixed-rate Sharpe formulation to score simulated portfolios.

---

## Portfolio Objectives

### Best Min Variance by Sharpe

$$
\min_{\mathbf{w}} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}
$$

### Best Max Sharpe

$$
\max_{\mathbf{w}} \frac{\mathbf{w}^\top \boldsymbol{\mu} - R_f}{\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}}
$$

### True Min Variance

$$
\max_{\mathbf{w}} \mathbf{w}^\top \boldsymbol{\mu}
$$

---

## Monte Carlo Search

The production dashboard does **not** solve the weight problem with a deterministic quadratic optimizer. Instead, it samples many random long-only weights and retains the best portfolio for each objective.

### Random weight generation

If random positive weights $u_i$ are drawn, production normalizes them as:

$$
w_i = \frac{u_i}{\sum_{j=1}^{n} u_j}
$$

This guarantees:

- all weights are non-negative
- total allocation sums to 1

---

## Historical Return and Covariance Estimation

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

## VaR Methods In Production

### Historical VaR proxy

The app computes a worst realized rolling loss proxy from the selected lookback window.

### Parametric VaR

The app also supports a normal-approximation annual VaR.

$$
\text{VaR} = \mu_{\text{annual}} + z_p \sigma_{\text{annual}}
$$

where the left-tail probability is interpreted as `1 / N years`.

---

## Live Overlay Theory

The optimization engine remains historical/covariance driven, but the dashboard enriches the results with live market context:

- Finnhub quote data for latest price
- FMP analyst target consensus and rating data

These live fields do not replace the covariance engine; they augment the dashboard’s explanatory layer.

---

## Production Caveats

- no shorting
- no leverage
- no transaction costs
- no taxes
- no slippage
- no liquidity modeling
- no deterministic frontier solver

The dashboard is an interactive analytical tool, not an execution engine.
