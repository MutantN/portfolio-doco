# Portfolio Dashboard Docs

This is the source project for the Portfolio Dashboard documentation site.

If you want to update the docs that appear at `portfolio-doco.vercel.app` or `as-hobby-labs.com/portfolio-dashboard-docs`, this is the folder to edit.

## What Lives Here

- the Markdown source files
- the HTML renderer
- the generated HTML output in `html/`

## Production Mapping

- Local folder: `/Users/A/portfolio-doco`
- GitHub repo: `MutantN/portfolio-doco`
- Vercel project: `portfolio-doco`
- Docs URL: `https://portfolio-doco.vercel.app`
- Custom-domain route: `https://as-hobby-labs.com/portfolio-dashboard-docs/`

## Typical Update Flow

1. Edit the Markdown files.
2. Rebuild the HTML with `python3 render_docs.py --input . --output html`.
3. Commit and push the changes.
4. Deploy with Vercel if you want the update to go live immediately.
