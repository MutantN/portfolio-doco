**Author:** Amadea Schaum  
**Date:** March 2026

# Monte Carlo Engine In The Portfolio Dashboard

This page describes the Monte Carlo engine specifically, not the full dashboard optimization stack.

## Overview

The current production dashboard supports both a Monte Carlo engine and a deterministic engine.

This page covers the Monte Carlo path only.

In practice, that engine is used to:

- sample candidate portfolio weights

- compare portfolio objectives under random search

- provide a direct comparison path against the deterministic engine in the UI

---

## What The Dashboard Compares

Within the Monte Carlo path, the dashboard focuses on three portfolio views:

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

- aligned historical daily return matrix from Yahoo Finance

- expected return vector from the selected return mode
  - historical annualized mean return
  - or modeled return blending target-implied return with historical mean

- annualized covariance matrix from historical returns

- user-selected VaR method

### Constraints

- long-only weights

- fully invested portfolio

### Search approach

- pseudo-random weight generation

- repeated scoring under the objective function

- best candidate retained

This is a practical search approach that keeps the dashboard responsive enough for interactive use, even though it is less efficient than the deterministic optimizer for standard portfolio objectives.

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
    -> selected expected return vector + historical covariance
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

- side-by-side engine comparison between Monte Carlo and deterministic optimization

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
