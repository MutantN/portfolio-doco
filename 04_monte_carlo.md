**Author:** Amadea Schaum  
**Date:** March 2026

# Monte Carlo Engine In The Portfolio Dashboard

## Overview

The current production dashboard still uses Monte Carlo logic, but it is now embedded inside a React application instead of a standalone Python script.

The engine is used to:

- sample candidate portfolio weights
- compare portfolio objectives
- surface interactive results in the UI

---

## Current Portfolio Variants

The dashboard reports and compares:

- Best Min Variance by Sharpe
- Best Max Sharpe
- True Min Variance

Each variant is evaluated using:

- annualized return
- annualized volatility
- Sharpe ratio
- selected VaR method

---

## Simulation Model

### Inputs

- selected stock tickers
- historical return matrix from Yahoo Finance
- annualized mean returns
- annualized covariance matrix
- user-selected VaR method

### Constraints

- long-only weights
- fully invested portfolio

### Search approach

- pseudo-random weight generation
- repeated scoring under the objective function
- best candidate retained

This is a practical search heuristic suitable for interactive dashboard use.

---

## Statistical Outputs Shown In The Dashboard

For each portfolio family the UI can summarize:

- average return
- return dispersion
- average volatility
- volatility dispersion
- average Sharpe
- Sharpe dispersion
- average VaR loss
- worst VaR loss

The dashboard also highlights best-performing candidate portfolios and presents allocation breakdowns.

---

## VaR Integration

### Historical VaR proxy

Uses realized portfolio return history and finds the worst rolling-window loss over the chosen history length.

### Parametric VaR

Uses annualized mean and annualized volatility under a normal approximation.

The dashboard lets the user switch between these methods to compare risk interpretation styles.

---

## Production Data Flow Around The Monte Carlo Layer

```text
Yahoo Finance history
    -> daily returns
    -> annualized means / covariance
    -> Monte Carlo optimization
    -> VaR analysis

Finnhub + FMP live data
    -> current price / target / rating overlays
    -> dashboard context for the optimized outputs
```

---

## Differences From The Original Documentation Set

The older documentation described:

- a Python CLI workflow
- multiprocessing jobs
- CSV outputs
- checkpoint files
- standalone simulation scripts

That is no longer the production model for `portfolio-dashboard`.

The current production model is:

- React frontend
- Vite build
- Vercel deployment
- server-backed market-data endpoints
- in-app interactive simulation and comparison

---

## Operational Notes

- Monte Carlo behavior is implemented inside `src/App.jsx`
- dev and preview API behavior is implemented in `vite.config.js`
- production chart fetching is handled by `api/yahoo-chart.js`
- deployment config is controlled through `vercel.json`

---

## Recommended Documentation Maintenance

If the dashboard changes materially, update this document when any of the following change:

- optimization objectives
- risk-free rate
- VaR implementation
- upstream data providers
- deployment path or environment model
