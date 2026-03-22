**Author:** Amadea Schaum  
**Date:** March 2026

# Optimization Method Considerations

This page explains the optimization methods used in the Portfolio Dashboard and how Monte Carlo and deterministic approaches differ in the current production app.

## What This Page Covers

The production dashboard supports two optimization engines:

- Monte Carlo search
- deterministic optimization

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
- user-selected annualized risk-free rate
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

The Monte Carlo engine samples stock subsets and valid portfolios, then keeps the strongest candidate for the chosen objective.

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

1. run the user-selected number of simulation passes
2. in each pass, randomly select the chosen number of stocks from the S&P 500 list
3. for each objective on that stock subset, generate random valid portfolios
4. compute return, volatility, and Sharpe for each portfolio
5. compare those sampled portfolios under the chosen objective
6. retain the best sampled candidate for that pass

In the current dashboard implementation, each Monte Carlo objective search evaluates 2,000 candidate weight sets.

The user separately controls how many Monte Carlo passes are run.

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

The deterministic engine still samples stock subsets, but replaces random weight search inside each subset with direct optimization over the same feasible portfolio set.

### Search structure

The deterministic path does this:

1. sample the user-selected number of stock subsets from the S&P 500 list
2. build expected returns and historical covariance for each subset
3. regularize the covariance matrix for numerical stability
4. solve a deterministic portfolio set inside each subset
5. rank the solved subsets and keep the best resulting portfolios

So the current deterministic mode is:

- deterministic for weights inside each tested subset
- sampled and heuristic for stock-universe selection

### Quadratic programming framework

For each sampled subset, the engine regularizes covariance as:

$$
\Sigma_{\text{reg}} = \frac{1}{2}(\Sigma + \Sigma^\top) + \lambda I
$$

It then solves long-only quadratic programs over:

$$
\Delta = \{ \mathbf{w} \in \mathbb{R}^n \mid w_i \ge 0,\; \sum_i w_i = 1 \}
$$

To build the efficient frontier, it repeatedly solves:

$$
\min_{\mathbf{w} \in \Delta} \; \mathbf{w}^\top \Sigma_{\text{reg}} \mathbf{w}
\quad \text{subject to} \quad
\mathbf{w}^\top \mu \ge R_{\text{target}}
$$

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

In the current implementation, the capped portfolio is chosen from efficient-frontier points that satisfy the volatility cap, not from a projected feasible-search routine.

### Strengths

- faster and more stable for standard portfolio objectives
- closer to a direct optimization solution
- easier to interpret when the objective is clearly defined
- reproducible for the same sampled subsets and inputs

### Weaknesses

- still depends on sampled subset coverage, so it is not globally optimal over stock selection
- more computational work per subset than pure random-weight sampling
- not a mixed-integer global stock-selection optimizer

---

## How The Two Approaches Differ In Practice

Monte Carlo answers the problem by sampling many admissible portfolios and keeping the best sampled one.

Deterministic optimization answers the problem by sampling stock subsets, then solving a QP-backed efficient-frontier problem inside each subset and enforcing the cap explicitly at the frontier-selection step.

In practical dashboard terms:

- Monte Carlo is more exploratory
- deterministic optimization is more efficient for standard objectives inside a tested subset
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
