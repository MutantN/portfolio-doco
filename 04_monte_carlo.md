**Author:** Amadea Schaum  
**Date:** March 2026

# Monte Carlo Engine In The Portfolio Dashboard

## Overview

The current production dashboard still uses Monte Carlo logic, but now it lives inside the app rather than in a separate Python workflow.

In practice, that engine is used to:

- sample candidate portfolio weights
- compare portfolio objectives
- surface interactive results in the UI

---

## What The Dashboard Compares

The dashboard focuses on three portfolio views:

- Best Min Variance by Sharpe
- Best Max Sharpe
- True Min Variance

Each variant is evaluated using:

- annualized return
- annualized volatility
- Sharpe ratio
- selected VaR method

---

## How The Simulation Works

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

This is a practical search approach that keeps the dashboard responsive enough for interactive use.

---

## What You See In The Results

For each portfolio family the UI can summarize:

- average return
- return dispersion
- average volatility
- volatility dispersion
- average Sharpe
- Sharpe dispersion
- average VaR loss
- worst VaR loss

The dashboard also highlights the strongest candidate portfolios and shows their allocations.

---

## How VaR Fits In

### Historical VaR proxy

Uses realized portfolio return history and finds the worst rolling-window loss over the chosen history length.

### Parametric VaR

Uses annualized mean and annualized volatility under a normal approximation.

The dashboard lets you switch between these methods depending on whether you want the more intuitive historical view or the smoother model-based one.

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

## What Changed From The Older Version

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

## When To Update This Page

If the dashboard changes materially, update this document when any of the following change:

- optimization objectives
- risk-free rate
- VaR implementation
- upstream data providers
- deployment path or environment model
