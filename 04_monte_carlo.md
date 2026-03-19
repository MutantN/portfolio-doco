**Author:** Amadea Schaum  
**Date:** March 2026

# Optimization Approaches / Methodology

This page explains the optimization methods used in the Portfolio Dashboard and how Monte Carlo and deterministic approaches differ in the current production app.

## What This Page Covers

The production dashboard supports two optimization engines:

- Monte Carlo search
- deterministic projected optimization

This page explains:

- what each engine is trying to solve
- how each engine works
- where each engine is stronger or weaker
- how both engines fit into the same dashboard

---

## Shared Portfolio Setup

Both engines work with the same portfolio inputs:

- selected stock tickers
- expected return vector
- historical covariance matrix
- fixed risk-free rate of `4%`
- long-only constraint
- fully invested constraint

The shared feasible region is:

$$
\Delta = \{ \mathbf{w} \in \mathbb{R}^n \mid w_i \ge 0,\; \sum_{i=1}^{n} w_i = 1 \}
$$

Both engines evaluate portfolios using the same core measures:

$$
R_p = \mathbf{w}^\top \boldsymbol{\mu}
$$

$$
\sigma_p = \sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}
$$

$$
\text{Sharpe}(\mathbf{w}) = \frac{R_p - R_f}{\sigma_p}
$$

---

## Monte Carlo Approach

### Core idea

The Monte Carlo engine samples many valid portfolios and keeps the strongest candidate for the chosen objective.

### Weight generation

If positive random values $u_i$ are drawn, the app constructs valid weights by normalization:

$$
w_i = \frac{u_i}{\sum_{j=1}^{n} u_j}
$$

This guarantees:

- $w_i \ge 0$
- $\sum_i w_i = 1$

### Optimization logic

The engine does this:

1. generate random valid portfolios
2. compute return, volatility, and Sharpe for each portfolio
3. compare those sampled portfolios under the chosen objective
4. retain the best sampled candidate

In the current dashboard implementation, each Monte Carlo pass evaluates 2,000 candidate weight sets.

### Strengths

- simple to implement
- easy to adapt to different scoring rules
- useful for exploratory comparison

### Weaknesses

- depends on sampled candidates rather than solving directly for an optimum
- less stable than deterministic optimization for standard portfolio objectives
- may require many samples to get close to the true optimum

---

## Deterministic Approach

### Core idea

The deterministic engine replaces random search with projected optimization over the same feasible portfolio set.

### Projection framework

Starting from a feasible portfolio $\mathbf{w}^{(k)}$, the optimizer takes an improving step and then projects the result back onto the simplex:

$$
\tilde{\mathbf{w}}^{(k+1)} = \mathbf{w}^{(k)} + \alpha_k \nabla f\left(\mathbf{w}^{(k)}\right)
$$

$$
\mathbf{w}^{(k+1)} = \Pi_{\Delta}\left(\tilde{\mathbf{w}}^{(k+1)}\right)
$$

Where:

- $f(\mathbf{w})$ is the target objective
- $\alpha_k$ is the step size
- $\Pi_{\Delta}$ projects back to a valid long-only, fully invested portfolio

### Objectives used in the dashboard

#### True Min Variance

$$
\min_{\mathbf{w} \in \Delta} \; \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}
$$

#### Best Max Sharpe

$$
\max_{\mathbf{w} \in \Delta} \; \frac{\mathbf{w}^\top \boldsymbol{\mu} - R_f}{\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}}
$$

#### Best Min Variance by Sharpe

$$
\max_{\mathbf{w} \in \Delta} \; \frac{\mathbf{w}^\top \boldsymbol{\mu} - R_f}{\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}}
\quad \text{subject to} \quad
\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}} \le \sigma_{\max}
$$

This means the user chooses an annualized volatility cap and the optimizer finds the best risk-adjusted portfolio within that limit.

### Strengths

- faster and more stable for standard portfolio objectives
- closer to a direct optimization solution
- easier to interpret when the objective is clearly defined

### Weaknesses

- less flexible than Monte Carlo for ad hoc search rules
- still depends on the quality of the projected optimization routine
- not a full industrial optimization stack or complete efficient-frontier solver

---

## How The Two Approaches Differ In Practice

Monte Carlo answers the problem by sampling many admissible portfolios and keeping the best sampled one.

Deterministic optimization answers the problem by moving directly through the feasible region toward a better solution under the stated objective.

In practical dashboard terms:

- Monte Carlo is more exploratory
- deterministic optimization is more efficient for standard objectives
- both use the same market data, return model, covariance model, and VaR options

---

## Role Of Return And Risk Inputs

Both engines use:

- historical covariance from aligned Yahoo Finance daily returns
- either historical expected return or modeled expected return
- the same VaR options for risk display

Expected return can come from:

- historical annualized mean return
- modeled return blending target-implied upside with historical mean

Covariance remains historical in both engines.

---

## Production Data Flow

```text
Yahoo Finance history
    -> daily returns
    -> expected return vector + historical covariance
    -> Monte Carlo engine or deterministic engine
    -> portfolio comparison
    -> VaR analysis

Finnhub + FMP live data
    -> current price / target / rating overlays
    -> dashboard context for optimized outputs
```

---

## Where These Methods Live In The App

- optimization logic is implemented inside `src/App.jsx`
- historical chart fetching is handled by `api/yahoo-chart.js`
- live quote and analyst data are handled by `api/quotes.js`
- deployment configuration is controlled by `vercel.json`

---

## When To Update This Page

Update this page if any of the following change:

- optimization objectives
- deterministic optimization method
- Monte Carlo sampling rule
- risk-free rate
- VaR implementation
- upstream data providers
