import fs from "node:fs/promises";
import path from "node:path";
import MarkdownIt from "markdown-it";
import markdownItAnchor from "markdown-it-anchor";
import hljs from "highlight.js";

const ROOT = process.cwd();
const OUTPUT_DIR = path.join(ROOT, "html");
const SKIP_FILES = new Set(["package-lock.json"]);

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return `<pre><code class="hljs language-${lang}">${hljs.highlight(code, { language: lang }).value}</code></pre>`;
    }

    return `<pre><code class="hljs">${md.utils.escapeHtml(code)}</code></pre>`;
  },
}).use(markdownItAnchor, {
  permalink: markdownItAnchor.permalink.headerLink(),
});

const styles = `
  :root {
    --bg: #f7fafc;
    --card: #ffffff;
    --ink: #0f172a;
    --muted: #475569;
    --line: #dbe4ee;
    --accent: #0f766e;
    --accent-2: #1d4ed8;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    font-family: "Inter", "Segoe UI", system-ui, sans-serif;
    color: var(--ink);
    background:
      radial-gradient(1000px 500px at 10% -10%, #dbeafe 0%, transparent 55%),
      radial-gradient(900px 500px at 100% 0%, #dcfce7 0%, transparent 55%),
      var(--bg);
  }

  .shell {
    max-width: 1080px;
    margin: 0 auto;
    padding: 32px 20px 56px;
  }

  .topbar {
    margin-bottom: 20px;
    padding: 16px 18px;
    border: 1px solid var(--line);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
  }

  .topbar h1 {
    margin: 0 0 8px;
    font-size: 20px;
  }

  .topbar p {
    margin: 0;
    color: var(--muted);
    font-size: 14px;
  }

  .layout {
    display: grid;
    grid-template-columns: 260px minmax(0, 1fr);
    gap: 20px;
    align-items: start;
  }

  .nav {
    position: sticky;
    top: 20px;
    padding: 16px;
    border: 1px solid var(--line);
    border-radius: 18px;
    background: var(--card);
  }

  .nav h2 {
    margin: 0 0 12px;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
  }

  .nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 8px;
  }

  .nav a {
    display: block;
    text-decoration: none;
    color: var(--ink);
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid transparent;
  }

  .nav a:hover,
  .nav a.active {
    background: #eff6ff;
    border-color: #bfdbfe;
  }

  .content {
    padding: 28px 32px;
    border: 1px solid var(--line);
    border-radius: 24px;
    background: var(--card);
    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.06);
  }

  .content h1 {
    margin-top: 0;
    font-size: clamp(30px, 4vw, 44px);
    line-height: 1.08;
  }

  .content h2 {
    margin-top: 32px;
    padding-top: 8px;
    border-top: 1px solid var(--line);
    font-size: 24px;
  }

  .content h3 {
    margin-top: 24px;
    color: var(--accent-2);
    font-size: 18px;
  }

  .content p,
  .content li {
    line-height: 1.75;
  }

  .content ul,
  .content ol {
    padding-left: 24px;
    margin: 14px 0;
  }

  .content li + li {
    margin-top: 8px;
  }

  .content ul ul,
  .content ol ol,
  .content ul ol,
  .content ol ul {
    margin-top: 8px;
  }

  .content code {
    font-family: "JetBrains Mono", "SFMono-Regular", monospace;
    font-size: 0.92em;
  }

  .content :not(pre) > code {
    padding: 2px 6px;
    border-radius: 8px;
    background: #f8fafc;
    border: 1px solid var(--line);
  }

  .content pre {
    overflow-x: auto;
    padding: 16px;
    border-radius: 16px;
    background: #0f172a;
  }

  .content pre code {
    color: #e2e8f0;
  }

  .content table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
  }

  .content th,
  .content td {
    padding: 12px 14px;
    border: 1px solid var(--line);
    text-align: left;
    vertical-align: top;
  }

  .content th {
    background: #f8fafc;
  }

  .content blockquote {
    margin: 20px 0;
    padding: 12px 16px;
    border-left: 4px solid var(--accent);
    background: #f8fafc;
    border-radius: 0 12px 12px 0;
  }

  .footer {
    margin-top: 20px;
    color: var(--muted);
    font-size: 13px;
  }

  @media (max-width: 900px) {
    .layout {
      grid-template-columns: 1fr;
    }

    .nav {
      position: static;
    }

    .content {
      padding: 22px 18px;
    }
  }
`;

function titleFromMarkdown(text, fallback) {
  const match = text.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : fallback;
}

function pageTemplate({ title, body, nav, currentFile }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title} - Portfolio Dashboard Docs</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/github-dark.min.css">
  <script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }
    };
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <style>${styles}</style>
</head>
<body>
  <main class="shell">
    <section class="topbar">
      <h1>Portfolio Dashboard Docs</h1>
      <p>Friendly documentation for the production Portfolio Dashboard and its supporting data flows.</p>
    </section>
    <section class="layout">
      <nav class="nav">
        <h2>Documents</h2>
        <ul>
          ${nav
            .map(
              (item) =>
                `<li><a class="${item.file === currentFile ? "active" : ""}" href="${item.file.replace(/\\.md$/, ".html")}">${item.title}</a></li>`,
            )
            .join("")}
        </ul>
      </nav>
      <article class="content">
        ${body}
        <div class="footer">Source project: <code>/Users/A/portfolio-doco</code></div>
      </article>
    </section>
  </main>
</body>
</html>`;
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  const entries = (await fs.readdir(ROOT))
    .filter((name) => name.endsWith(".md") && !SKIP_FILES.has(name))
    .sort();

  const docs = [];
  for (const file of entries) {
    const source = await fs.readFile(path.join(ROOT, file), "utf8");
    docs.push({
      file,
      source,
      title: titleFromMarkdown(source, file.replace(/\.md$/, "")),
    });
  }

  for (const doc of docs) {
    const html = md.render(doc.source);
    const full = pageTemplate({
      title: doc.title,
      body: html,
      nav: docs,
      currentFile: doc.file,
    });
    await fs.writeFile(path.join(OUTPUT_DIR, doc.file.replace(/\.md$/, ".html")), full);
  }

  const firstDoc = docs.find((doc) => doc.file === "00_project_overview.md") ?? docs[0];
  const redirect = `<!DOCTYPE html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=${firstDoc.file.replace(/\.md$/, ".html")}"></head><body></body></html>`;
  await fs.writeFile(path.join(OUTPUT_DIR, "index.html"), redirect);

  console.log(`Rendered ${docs.length} documents to ${OUTPUT_DIR}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
