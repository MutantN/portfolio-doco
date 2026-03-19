**Author:** Amadea Schaum  
**Date:** March 2026

# Portfolio Dashboard Quick Start

This quick start is for the current production Portfolio Dashboard app in `/Users/A/portfolio-dashboard`.

---

## Project Mapping

| Item | Value |
|------|-------|
| Local folder | `/Users/A/portfolio-dashboard` |
| GitHub repo | `https://github.com/MutantN/portfolio-dashboard` |
| Vercel project | `portfolio-dashboard` |
| Domain route | `https://as-hobby-labs.com/portfolio-dashboard/` |

---

## Before You Start

- Node.js
- npm
- Vercel CLI if you want to deploy manually

If you want live quotes and analyst overlays locally, you will also need:

- `FINNHUB_API_KEY`
- `FMP_API_KEY`

---

## Install Dependencies

```bash
cd /Users/A/portfolio-dashboard
npm install
```

---

## Run It Locally

```bash
cd /Users/A/portfolio-dashboard
npm run dev
```

This starts the app and the local API middleware defined in `vite.config.js`, including:

- `/api/yahoo-chart`
- `/api/quotes`

---

## Build The Production Version

```bash
cd /Users/A/portfolio-dashboard
npm run build
```

You should get:

- static app in `dist/`
- relative asset paths suitable for:
  - standalone Vercel hosting
  - routed deployment at `/portfolio-dashboard/`

---

## Check The Live Version

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

## Files You Will Most Likely Touch

| File | Purpose |
|------|---------|
| `src/App.jsx` | UI, simulation engine, VaR logic, live data orchestration |
| `vite.config.js` | Vite config plus dev/preview middleware for API routes |
| `api/yahoo-chart.js` | production serverless Yahoo Finance proxy |
| `vercel.json` | Vercel production build/output/rewrite config |

---

## Common Maintenance Tasks

### Update the docs

Edit:

- `README.md`
- `portfolio-doco/README.md`
- this documentation set

### Check path-safe asset behavior

Confirm `vite.config.js` still uses:

```js
base: "./"
```

### Deploy an update

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
