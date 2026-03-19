**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard Theory

## What This Page Explains

This page explains the logic behind the Portfolio Dashboard in plain language.

The dashboard is trying to answer a simple question:

- given a portfolio objective, what stock mix and weight allocation best satisfies it?

It answers that by:

- estimating return and risk from market data
- generating many candidate portfolios
- scoring those portfolios against the chosen objective
- surfacing the strongest result for each portfolio view

---

## The Building Blocks

The dashboard works with a few core ingredients:

- a list of selected stocks
- a weight for each stock
- an expected return for each stock
- a covariance matrix showing how stocks move together
- a fixed risk-free rate of `4%`

The portfolio rules are intentionally simple:

- weights cannot be negative
- weights must add up to 1

That means the dashboard is always showing a long-only, fully invested portfolio.

---

## The Main Portfolio Measures

### Expected return

The dashboard combines stock-level expected returns into a portfolio-level expected return:

$$
R_p = \mathbf{w}^\top \boldsymbol{\mu}
$$

In plain English:

- each stock gets a weight
- each stock has an expected return
- the portfolio return is the weighted combination of those returns

### Volatility

Portfolio risk is represented by volatility:

$$
\sigma_p = \sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}
$$

This captures two things at once:

- how volatile each stock is by itself
- how the stocks move together

### Sharpe ratio

The dashboard ranks risk-adjusted performance with a Sharpe ratio:

$$
\text{Sharpe} = \frac{R_p - R_f}{\sigma_p}
$$

Where:

- $R_p$ is portfolio return
- $R_f$ is the fixed `4%` risk-free rate
- $\sigma_p$ is portfolio volatility

Higher Sharpe means better return for the amount of risk taken.

---

## The Three Portfolio Views In The Dashboard

The dashboard focuses on three portfolio views.

### 1. Best Min Variance by Sharpe

This is meant to represent the strongest risk-adjusted portfolio within the low-volatility part of the search results.

You can think of it as:

- stay in the safer part of the opportunity set
- then choose the candidate with the better Sharpe profile inside that group

### 2. Best Max Sharpe

This is the clearest best risk-adjusted return portfolio in the dashboard.

It is the portfolio that gives the strongest Sharpe ratio among the sampled candidates.

### 3. True Min Variance

This is the absolute lowest-volatility portfolio found by the search.

It does not try to improve return once volatility has been minimized.

That makes it the most conservative portfolio view shown in the app.

---

## How The Optimization Method Works

The dashboard uses a Monte Carlo search heuristic.

It does **not** run a classical deterministic optimizer in the live UI path.

Instead, it does this:

1. generate many random candidate weight sets
2. normalize each weight set so total allocation is 100%
3. calculate return, volatility, and Sharpe for each candidate
4. keep the strongest candidates for the relevant portfolio objective

In the current implementation, each optimization pass evaluates 2,000 candidate weight sets.

### Random weight generation

If random positive values $u_i$ are drawn, the app converts them to valid weights like this:

$$
w_i = \frac{u_i}{\sum_{j=1}^{n} u_j}
$$

That guarantees:

- every weight stays non-negative
- all weights sum to 1

This approach is practical for an interactive dashboard because it is simple, fast, and easy to rerun.

---

## How Historical Returns Are Built

The historical mode starts from Yahoo Finance price history.

From that data, the dashboard builds daily returns and annualizes them using a 252-trading-day convention.

### Annualized mean return

$$
\mu_i = 252 \cdot \frac{1}{T} \sum_{t=1}^{T} r_{it}
$$

### Annualized covariance

$$
\sigma_{ij} = 252 \cdot \text{Cov}(r_i, r_j)
$$

This historical return and covariance framework is the base model underneath the dashboard.

---

## How Modeled Returns Work

The dashboard also supports a modeled return mode.

This mode does **not** replace the historical framework entirely. Instead, it changes the expected return input while keeping covariance historical.

The modeled return path blends:

- target-implied return from analyst target prices
- historical annualized mean return

### Target-implied return

Conceptually, the dashboard derives implied upside as:

$$
\text{implied return} = \frac{\text{target price}}{\text{current price}} - 1
$$

### Blending logic

That implied return is then blended with the historical mean.

The blend weight depends on analyst confidence, using analyst count as a proxy.

In practical terms:

- more analyst coverage gives more influence to the modeled return
- less analyst coverage leaves more influence on the historical return estimate
- covariance still comes from historical daily returns

So the modeled mode changes the expected return vector, but not the covariance matrix.

---

## How Risk Is Presented

The dashboard supports two VaR-style risk views.

### Historical VaR proxy

This is the more intuitive option.

It looks back through realized return history and asks:

- what was the worst rolling loss over the selected history window?

This gives a stress-style view based on what actually happened in the past.

### Parametric VaR

This is the smoother, model-based option.

It uses annualized mean and annualized volatility with a normal approximation:

$$
\text{VaR} = \mu_{\text{annual}} + z_p \sigma_{\text{annual}}
$$

Here the left-tail probability is interpreted as a `1 / N years` event.

This method is cleaner mathematically, but it depends more heavily on modeling assumptions.

---

## Where Live Data Fits In

The optimization engine is still driven by return and covariance modeling, but the dashboard adds live context on top of that model.

The live overlay layer includes:

- Finnhub quote data for current price and previous close
- FMP analyst target, rating, and analyst-count data

These fields do not replace the portfolio engine.

They help answer questions like:

- what does this portfolio look like right now?
- how does analyst sentiment compare with the historical picture?

---

## Important Limits

This is still a simplified analytical tool.

It does **not** model:

- shorting
- leverage
- taxes
- transaction costs
- slippage
- liquidity constraints
- a full deterministic efficient-frontier solver

So the dashboard is best understood as an exploratory portfolio analysis tool, not a trading system or execution engine.
