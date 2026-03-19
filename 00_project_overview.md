**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard Project Overview

## What This Dashboard Is

Portfolio Dashboard is a live web app for exploring portfolio ideas, comparing a few portfolio construction styles, and layering current market context on top of historical analysis.

The production version is a dashboard that brings together:

1. historical price history from Yahoo Finance

2. live prices from Finnhub

3. analyst targets and ratings from Financial Modeling Prep

4. Monte Carlo portfolio search

5. on-screen portfolio comparison and risk views

Production deployment is live at:

- `https://as-hobby-labs.com/portfolio-dashboard/`
- `https://portfolio-dashboard-two-pearl.vercel.app`

---

## Project Identity

| Item | Value |
|------|-------|
| Local folder | `/Users/A/portfolio-dashboard` |
| GitHub repo | `MutantN/portfolio-dashboard` |
| Vercel project | `portfolio-dashboard` |
| Main app file | `src/App.jsx` |
| Serverless function | `api/yahoo-chart.js` |
| Production config | `vercel.json` |

---

## What You Can Do In It

The current production dashboard supports:

A. Monte Carlo portfolio simulation across a chosen stock set

B. Comparison of **Best Min Variance by Sharpe**, **Best Max Sharpe**, and **True Min Variance** portfolios

C. Historical and parametric VaR analysis

D. Live quote overlays

E. Analyst target price and rating overlays

F. Production-safe deployment on both:

- its own Vercel project domain

- the routed path `as-hobby-labs.com/portfolio-dashboard/`

---

## System Architecture

```text
┌────────────────────────────────────────────────────────────────┐
│                      PORTFOLIO DASHBOARD                      │
├────────────────────────────────────────────────────────────────┤
│ React UI (`src/App.jsx`)                                      │
│  ├─ portfolio simulation controls                             │
│  ├─ optimization summaries                                    │
│  ├─ live quote / analyst overlays                             │
│  └─ risk and VaR displays                                     │
├────────────────────────────────────────────────────────────────┤
│ Data Endpoints                                                 │
│  ├─ `/api/yahoo-chart`  -> Yahoo Finance historical chart API │
│  └─ `/api/quotes`       -> Finnhub + FMP aggregation          │
├────────────────────────────────────────────────────────────────┤
│ Deployment                                                     │
│  ├─ Vercel project: `portfolio-dashboard`                     │
│  ├─ direct URL: `portfolio-dashboard-two-pearl.vercel.app`    │
│  └─ custom route: `as-hobby-labs.com/portfolio-dashboard/`    │
└────────────────────────────────────────────────────────────────┘
```

---

## How The App Works

### Historical market data

- Endpoint: `/api/yahoo-chart`

- Purpose: fetch adjusted historical prices and turn them into return series

- Used for:

  - mean return estimation

  - covariance estimation

  - Monte Carlo simulation inputs

  - historical VaR proxy

### Live market overlays

- Endpoint: `/api/quotes`

- Finnhub provides:

  - live prices

  - previous close

- Financial Modeling Prep provides:

  - target price

  - analyst count

  - analyst rating

### Risk model

- Fixed risk-free rate: `4%`

- Weight constraints: long-only and fully invested

- VaR methods:

  - historical rolling-loss proxy

  - parametric normal approximation

---

## Deployment Notes

- `vite.config.js` uses `base: "./"` so assets resolve correctly under the custom routed path
- `vercel.json` explicitly configures:
  - Vite framework
  - `npm run build`
  - `dist` output
  - SPA rewrite fallback
- The app is designed to work both as a standalone Vercel deployment and behind the main site router

---

## Documentation Map

| Document | Purpose |
|----------|---------|
| `00_project_overview.md` | Product identity, architecture, deployment |
| `01_theory.md` | Optimization and VaR math used by the dashboard |
| `02_quickstart.md` | Local development and production verification |
| `03_api_reference.md` | Current endpoints, env vars, and key files |
| `04_monte_carlo.md` | Monte Carlo engine behavior in the dashboard |
