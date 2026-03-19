# Portfolio Doco

Canonical local project for the Portfolio Dashboard HTML documentation.

## Purpose

This folder is the maintained source for the `portfolio-doco` Vercel project.
It contains:

- Markdown source files
- the HTML renderer
- generated HTML output in `html/`

## Production Mapping

- Local folder: `/Users/A/portfolio-doco`
- Vercel project: `portfolio-doco`
- Production URL: `https://portfolio-doco.vercel.app`
- Subject app: `portfolio-dashboard`

## Update Flow

1. Edit the Markdown files in this folder.
2. Regenerate HTML with `python3 render_docs.py --input . --output html`.
3. Deploy with Vercel or push to GitHub.
