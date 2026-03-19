**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard API Reference

This project is now a deployed React dashboard with lightweight serverless and dev-middleware endpoints.

---

## Project-Level Interfaces

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
- allows the app to work both:
  - on its standalone Vercel domain
  - under `/portfolio-dashboard/`

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
- returns raw JSON used to build return series and risk inputs

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
- returns data merged from:
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

The current app logic lives in `src/App.jsx`.

### `historicalVaRProxy(dailyReturns, weights)`

- computes a worst realized rolling loss proxy from historical returns

### `parametricVaR(dailyReturns, weights, oneInYears=2)`

- computes a normal-approximation VaR from annualized return and volatility

### `optimize(mu, cv, seed, mode)`

- Monte Carlo search over random long-only weights
- returns the best portfolio under the requested objective

### `runSim(...)`

- runs a simulation instance over selected stocks
- produces portfolio statistics for the reported portfolio variants

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
