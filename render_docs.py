#!/usr/bin/env python3
"""
Markdown to HTML Renderer with LaTeX Math Support
==================================================

Converts markdown documentation files to styled HTML with:
- LaTeX equation rendering via MathJax
- Syntax highlighting for code blocks
- Responsive CSS styling
- Table of contents generation
- Navigation between documents

Usage:
    python render_docs.py                    # Render all .md files in current dir
    python render_docs.py --input docs/      # Specify input directory
    python render_docs.py --output html/     # Specify output directory
    python render_docs.py --single file.md   # Render single file

Requirements:
    pip install markdown pygments

Author: Portfolio Optimization Documentation Generator
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from markdown.extensions.toc import TocExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.codehilite import CodeHiliteExtension
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    print("Warning: 'markdown' package not installed. Using basic converter.")
    print("For better results: pip install markdown pygments")


# =============================================================================
# HTML TEMPLATE
# =============================================================================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Portfolio Optimization Documentation</title>
    
    <!-- MathJax for LaTeX rendering -->
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
            }},
            startup: {{
                ready: function() {{
                    MathJax.startup.defaultReady();
                }}
            }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <!-- Highlight.js for code syntax highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --background-color: #ffffff;
            --text-color: #333333;
            --code-bg: #f8f8f8;
            --border-color: #e1e4e8;
            --nav-bg: #f6f8fa;
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: var(--background-color);
        }}
        
        /* Navigation */
        nav {{
            background-color: var(--nav-bg);
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 1px solid var(--border-color);
        }}
        
        nav ul {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        nav a {{
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 500;
            padding: 8px 12px;
            border-radius: 4px;
            transition: background-color 0.2s;
            font-size: 0.9em;
        }}
        
        nav a:hover {{
            background-color: var(--secondary-color);
            color: white;
        }}
        
        nav a.active {{
            background-color: var(--primary-color);
            color: white;
        }}
        
        /* Headings */
        h1 {{
            color: var(--primary-color);
            border-bottom: 3px solid var(--secondary-color);
            padding-bottom: 10px;
            margin-top: 0;
        }}
        
        h2 {{
            color: var(--primary-color);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
            margin-top: 40px;
        }}
        
        h3 {{
            color: var(--secondary-color);
            margin-top: 30px;
        }}
        
        h4 {{
            color: var(--primary-color);
            margin-top: 25px;
        }}
        
        /* Links */
        a {{
            color: var(--secondary-color);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Code */
        code {{
            font-family: 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
        }}
        
        :not(pre) > code {{
            background-color: var(--code-bg);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
        }}
        
        pre {{
            background-color: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            overflow-x: auto;
        }}
        
        pre code {{
            background: none;
            border: none;
            padding: 0;
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
            table-layout: fixed;
            display: block;
            overflow-x: auto;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border: 1px solid var(--border-color);
            overflow-wrap: anywhere;
        }}
        
        th {{
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background-color: var(--nav-bg);
        }}
        
        tr:hover {{
            background-color: #e8f4f8;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid var(--secondary-color);
            margin: 20px 0;
            padding: 10px 20px;
            background-color: var(--nav-bg);
            border-radius: 0 8px 8px 0;
        }}
        
        blockquote p {{
            margin: 0;
        }}
        
        /* Math display */
        mjx-container[jax="CHTML"][display="true"] {{
            margin: 25px 0 !important;
            overflow-x: auto;
            overflow-y: hidden;
        }}
        
        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 40px 0;
        }}
        
        /* Lists */
        ul, ol {{
            padding-left: 25px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        /* Footer */
        footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        /* Author info */
        .author-info {{
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 15px;
            }}
            
            nav ul {{
                flex-direction: column;
                gap: 8px;
            }}
            
            table {{
                font-size: 0.85em;
            }}
            
            th, td {{
                padding: 8px 10px;
            }}
        }}
        
        /* Print styles */
        @media print {{
            nav, footer {{
                display: none;
            }}
            
            body {{
                max-width: none;
                padding: 0;
            }}
            
            pre {{
                white-space: pre-wrap;
            }}
        }}
    </style>
</head>
<body>
    <nav>
        <ul>
            {navigation}
        </ul>
    </nav>
    
    <main>
        {content}
    </main>
    
    <footer>
        <p>Portfolio Optimization Documentation | Generated on {date}</p>
        <p>Built with Python, MathJax, and Highlight.js</p>
    </footer>
</body>
</html>
'''


# =============================================================================
# LATEX PROTECTION
# =============================================================================

def protect_latex(md_content):
    """
    Protect LaTeX blocks from markdown processing.
    
    This prevents underscores, asterisks, and other markdown syntax
    inside LaTeX from being incorrectly interpreted as formatting.
    
    Returns: (protected_content, latex_blocks_list)
    """
    latex_blocks = []
    
    def save_block(match):
        idx = len(latex_blocks)
        latex_blocks.append(match.group(0))
        return f'%%LATEXBLOCK{idx}%%'
    
    # Protect display math ($$...$$) - handles multi-line
    protected = re.sub(r'\$\$[\s\S]*?\$\$', save_block, md_content)
    
    # Protect inline math ($...$) - but not $$
    # Match $ followed by non-$ content, followed by $
    protected = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]+?)\$(?!\$)', save_block, protected)
    
    return protected, latex_blocks


def restore_latex(html_content, latex_blocks):
    """Restore LaTeX blocks after markdown processing."""
    for idx, latex in enumerate(latex_blocks):
        html_content = html_content.replace(f'%%LATEXBLOCK{idx}%%', latex)
    return html_content


# =============================================================================
# MARKDOWN PROCESSING
# =============================================================================

def basic_markdown_to_html(text):
    """
    Basic markdown to HTML converter (fallback when markdown package unavailable).
    """
    html = text
    
    # Headers
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Code blocks
    def code_block_replacer(match):
        lang = match.group(1) or ''
        code = match.group(2)
        # Escape HTML in code
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="language-{lang}">{code}</code></pre>'
    
    html = re.sub(r'```(\w*)\n(.*?)```', code_block_replacer, html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Horizontal rules
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
    
    # Simple table handling
    lines = html.split('\n')
    in_table = False
    result_lines = []
    table_lines = []
    
    for line in lines:
        stripped = line.strip()
        if '|' in stripped and not stripped.startswith('```'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(stripped)
        else:
            if in_table:
                result_lines.append(convert_table(table_lines))
                in_table = False
                table_lines = []
            result_lines.append(line)
    
    if in_table:
        result_lines.append(convert_table(table_lines))
    
    html = '\n'.join(result_lines)
    
    # Paragraphs - wrap non-tagged content
    paragraphs = html.split('\n\n')
    processed = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('%%LATEX'):
            p = f'<p>{p}</p>'
        processed.append(p)
    
    html = '\n\n'.join(processed)
    
    return html


def convert_table(lines):
    """Convert markdown table lines to HTML table."""
    if len(lines) < 2:
        return '\n'.join(lines)
    
    html = ['<table>']
    
    # Header row
    header_cells = [c.strip() for c in lines[0].split('|') if c.strip()]
    html.append('<tr>' + ''.join(f'<th>{c}</th>' for c in header_cells) + '</tr>')
    
    # Skip separator row (line with dashes)
    # Data rows
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if cells:
            html.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    
    html.append('</table>')
    return '\n'.join(html)


def convert_markdown_to_html(md_content):
    """
    Convert markdown content to HTML, protecting LaTeX blocks.
    """
    # Step 1: Protect LaTeX from markdown processing
    protected, latex_blocks = protect_latex(md_content)
    
    # Step 2: Convert markdown to HTML
    if MARKDOWN_AVAILABLE:
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            TocExtension(permalink=True),
            'attr_list',
            'def_list'
        ])
        html = md.convert(protected)
    else:
        html = basic_markdown_to_html(protected)
    
    # Step 3: Restore LaTeX blocks
    html = restore_latex(html, latex_blocks)
    
    return html


def extract_title(md_content):
    """Extract title from markdown (first H1)."""
    match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Documentation"


# =============================================================================
# FILE PROCESSING
# =============================================================================

def get_doc_files(input_dir):
    """Get all markdown files in directory, sorted by name."""
    input_path = Path(input_dir)
    md_files = sorted(input_path.glob('*.md'))
    return md_files


def generate_navigation(doc_files, current_file):
    """Generate navigation HTML."""
    nav_items = []
    for f in doc_files:
        name = f.stem
        # Create display name from filename
        display_name = name.replace('_', ' ')
        # Remove leading numbers and clean up
        display_name = re.sub(r'^\d+\s*', '', display_name)
        display_name = display_name.title()
        
        html_name = f"{name}.html"
        active = 'class="active"' if f.name == current_file.name else ''
        nav_items.append(f'<li><a href="{html_name}" {active}>{display_name}</a></li>')
    
    return '\n            '.join(nav_items)


def render_file(md_file, output_dir, doc_files):
    """Render a single markdown file to HTML."""
    print(f"  Rendering: {md_file.name}")
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = convert_markdown_to_html(md_content)
    title = extract_title(md_content)
    navigation = generate_navigation(doc_files, md_file)
    
    # Fill template
    final_html = HTML_TEMPLATE.format(
        title=title,
        navigation=navigation,
        content=html_content,
        date=datetime.now().strftime('%Y-%m-%d %H:%M')
    )
    
    # Write output
    output_file = output_dir / f"{md_file.stem}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    return output_file


def create_index_redirect(output_dir, doc_files):
    """Create index.html that redirects to first doc."""
    if not doc_files:
        return
    
    first_doc = doc_files[0].stem + '.html'
    index_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={first_doc}">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="{first_doc}">documentation</a>...</p>
</body>
</html>
'''
    
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Render Markdown documentation to HTML with LaTeX support'
    )
    parser.add_argument('--input', '-i', default='.',
                       help='Input directory containing .md files (default: current directory)')
    parser.add_argument('--output', '-o', default='html',
                       help='Output directory for HTML files (default: html)')
    parser.add_argument('--single', '-s',
                       help='Render a single file instead of directory')
    
    args = parser.parse_args()
    
    # Handle single file mode
    if args.single:
        md_file = Path(args.single)
        if not md_file.exists():
            print(f"Error: File not found: {args.single}")
            return 1
        
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = render_file(md_file, output_dir, [md_file])
        print(f"\nRendered: {output_file}")
        return 0
    
    # Directory mode
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return 1
    
    # Get all markdown files
    doc_files = get_doc_files(input_dir)
    
    if not doc_files:
        print(f"No markdown files found in {input_dir}")
        return 1
    
    print(f"Found {len(doc_files)} markdown files")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Render each file
    print("\nRendering documentation:")
    rendered_files = []
    for md_file in doc_files:
        output_file = render_file(md_file, output_dir, doc_files)
        rendered_files.append(output_file)
    
    # Create index redirect
    create_index_redirect(output_dir, doc_files)
    
    print(f"\n{'='*50}")
    print(f"Successfully rendered {len(rendered_files)} files to {output_dir}/")
    print(f"{'='*50}")
    print("\nGenerated files:")
    for f in rendered_files:
        print(f"  - {f.name}")
    print(f"  - index.html (redirect)")
    
    print(f"\nTo view: open {output_dir}/index.html in a browser")
    
    return 0


if __name__ == '__main__':
    exit(main())
