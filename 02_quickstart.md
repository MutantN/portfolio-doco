**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard Quick Start

This quick start reflects the **current production React dashboard** in `/Users/A/portfolio-dashboard`.

---

## Project Mapping

| Item | Value |
|------|-------|
| Local folder | `/Users/A/portfolio-dashboard` |
| GitHub repo | `https://github.com/MutantN/portfolio-dashboard` |
| Vercel project | `portfolio-dashboard` |
| Domain route | `https://as-hobby-labs.com/portfolio-dashboard/` |

---

## Prerequisites

- Node.js
- npm
- Vercel CLI if you want to deploy manually

Optional for local live-data behavior:

- `FINNHUB_API_KEY`
- `FMP_API_KEY`

---

## Install

```bash
cd /Users/A/portfolio-dashboard
npm install
```

---

## Run Locally

```bash
cd /Users/A/portfolio-dashboard
npm run dev
```

This starts the Vite app and the dev middleware in `vite.config.js`, including:

- `/api/yahoo-chart`
- `/api/quotes`

---

## Build For Production

```bash
cd /Users/A/portfolio-dashboard
npm run build
```

Expected output:

- static app in `dist/`
- relative asset paths suitable for:
  - standalone Vercel hosting
  - routed deployment at `/portfolio-dashboard/`

---

## Verify Live Production

### Main domain route

```text
https://as-hobby-labs.com/portfolio-dashboard/
```

### Direct Vercel deployment

```text
https://portfolio-dashboard-two-pearl.vercel.app
```

### Live API checks

Quotes:

```bash
curl 'https://as-hobby-labs.com/portfolio-dashboard/api/quotes?symbols=AAPL'
```

Yahoo chart:

```bash
curl 'https://as-hobby-labs.com/portfolio-dashboard/api/yahoo-chart?ticker=AAPL&period1=1704067200&period2=1735689600'
```

---

## Environment Variables

For live market overlays, configure:

```text
FINNHUB_API_KEY
FMP_API_KEY
```

These can live in:

- local `.env.local`
- Vercel project environment variables

---

## Core Files

| File | Purpose |
|------|---------|
| `src/App.jsx` | UI, simulation engine, VaR logic, live data orchestration |
| `vite.config.js` | Vite config plus dev/preview middleware for API routes |
| `api/yahoo-chart.js` | production serverless Yahoo Finance proxy |
| `vercel.json` | Vercel production build/output/rewrite config |

---

## Common Maintenance Tasks

### Update production documentation

Edit:

- `README.md`
- `portfolio-doco/README.md`
- this documentation set

### Check deployment-safe asset behavior

Confirm `vite.config.js` still uses:

```js
base: "./"
```

### Re-deploy

Git-connected deployment:

```bash
git add .
git commit -m "Update portfolio dashboard"
git push origin main
```

Manual production deploy:

```bash
vercel --prod --yes
```
