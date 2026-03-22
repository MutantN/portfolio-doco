**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard API Reference

This page is the practical reference for the data endpoints and helper pieces behind the Portfolio Dashboard.

---

## Main Moving Parts

| Interface | File | Purpose |
|-----------|------|---------|
| React app | `/Users/A/portfolio-dashboard/src/App.jsx` | Portfolio UI, simulation logic, live overlays |
| Vite config | `/Users/A/portfolio-dashboard/vite.config.js` | Vite build config and dev/preview API middleware |
| Vercel config | `/Users/A/portfolio-dashboard/vercel.json` | Production build/output/rewrite behavior |
| Yahoo endpoint | `/Users/A/portfolio-dashboard/api/yahoo-chart.js` | Production serverless chart proxy |

---

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `FINNHUB_API_KEY` | Yes for live quotes | Fetches latest quote data |
| `FMP_API_KEY` | Yes for analyst overlays | Fetches target price and rating data |

---

## Frontend Helper

### `apiPath(path)`

Location:

- `src/App.jsx`

Purpose:

- builds API URLs from `import.meta.env.BASE_URL`

- keeps requests working both:

  - on the standalone Vercel deployment

  - under `/portfolio-dashboard/` on the main domain

---

## Endpoint: `/api/yahoo-chart`

### Production file

- `api/yahoo-chart.js`

### Dev/preview implementation

- `vite.config.js`

### Method

- `GET`

### Query parameters

| Name | Required | Description |
|------|----------|-------------|
| `ticker` | Yes | Symbol, normalized for Yahoo Finance |
| `period1` | Yes | Unix start timestamp |
| `period2` | Yes | Unix end timestamp |

### Purpose

- fetches historical chart data from Yahoo Finance

- returns the raw data used to build return series and portfolio risk inputs

---

## Endpoint: `/api/quotes`

### Dev/preview implementation

- `vite.config.js`

### Method

- `GET`

### Query parameters

| Name | Required | Description |
|------|----------|-------------|
| `symbols` | Yes | Comma-separated ticker list |

### Purpose

- aggregates live quote and analyst context

- returns merged data from:

  - Finnhub

  - Financial Modeling Prep

### Response shape

```json
{
  "source": "Finnhub+FMP",
  "quotes": {
    "AAPL": {
      "price": 250.12,
      "prev": 255.76,
      "name": "AAPL",
      "exchange": "US",
      "time": 1773432000,
      "targetPrice": 316.36,
      "targetDate": "",
      "analystCount": 109,
      "rating": "Buy",
      "ratingDate": ""
    }
  },
  "missing": []
}
```

---

## Core Portfolio Functions

The main portfolio logic still lives in `src/App.jsx`.

### `historicalVaRProxy(dailyReturns, weights)`

- computes a worst realized rolling-loss proxy from historical returns

### `parametricVaR(dailyReturns, weights, oneInYears=2)`

- computes a normal-approximation VaR from annualized return and volatility

### `solvePortfolioSet(mu, cv, engineMode, seed, volatilityCap, riskFreeRate)`

- Monte Carlo mode runs random long-only weight searches for the requested objectives

- deterministic mode runs the QP-backed optimizer on a sampled stock subset

- returns the portfolio set used by the dashboard views

### `runSim(...)`

- runs one simulation pass over the selected stocks

- produces the portfolio statistics used in the dashboard views

---

## Deployment Behavior

### Vite

- `base: "./"` ensures relative assets in production

### Vercel

- framework: `vite`

- build command: `npm run build`

- output directory: `dist`

- non-file routes rewrite to `index.html`

---

## Operational Notes

- The dashboard is Git-connected to `MutantN/portfolio-dashboard`

- Production deployment is triggered from Git pushes or manual `vercel --prod`

- Routed custom-domain access is provided through `as-hobby-home`
