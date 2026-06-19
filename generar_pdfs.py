#!/usr/bin/env python3
"""Convierte los docs principales de KORMAN a PDF abribles en cualquier dispositivo."""
import markdown2
from weasyprint import HTML, CSS
import os

OUT = "/home/user/Marketing-y-empresa-/docs-pdf/"
os.makedirs(OUT, exist_ok=True)

CSS_STYLE = """
@page {
    margin: 2.5cm 2.8cm;
    size: A4;
}
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
}
h1 {
    font-size: 22pt;
    font-weight: 700;
    color: #080808;
    border-bottom: 2px solid #080808;
    padding-bottom: 8px;
    margin-top: 0;
}
h2 {
    font-size: 15pt;
    font-weight: 700;
    color: #080808;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
    margin-top: 28px;
}
h3 {
    font-size: 12pt;
    font-weight: 700;
    color: #333;
    margin-top: 20px;
}
p { margin: 8px 0; }
ul, ol { padding-left: 22px; }
li { margin: 4px 0; }
code {
    background: #f4f4f4;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 9.5pt;
    font-family: monospace;
}
pre {
    background: #f4f4f4;
    padding: 12px;
    border-radius: 4px;
    font-size: 9pt;
    overflow-x: auto;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
}
th {
    background: #080808;
    color: #fff;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 7px 10px;
    border-bottom: 1px solid #e0e0e0;
}
tr:nth-child(even) td { background: #f9f9f9; }
blockquote {
    border-left: 3px solid #ccc;
    padding-left: 14px;
    color: #555;
    margin: 10px 0;
}
a { color: #080808; }
strong { font-weight: 700; }
em { font-style: italic; color: #444; }
.header-bar {
    background: #080808;
    color: #fff;
    padding: 18px 24px;
    margin: -2.5cm -2.8cm 24px -2.8cm;
    font-size: 9pt;
    letter-spacing: 2px;
}
"""

DOCS = [
    {
        "src": "/home/user/Marketing-y-empresa-/KORMAN-CONTEXTO-EMPRESA.md",
        "out": "KORMAN-Contexto-Empresa.pdf",
        "header": "KORMAN ETIQUETAS BORDADAS  ·  DOCUMENTO INTERNO  ·  CONFIDENCIAL"
    },
    {
        "src": "/home/user/Marketing-y-empresa-/KORMAN-PROYECTO-TRACKER.md",
        "out": "KORMAN-Proyecto-Tracker.pdf",
        "header": "KORMAN ETIQUETAS BORDADAS  ·  TRACKER DE PROYECTO"
    },
    {
        "src": "/home/user/Marketing-y-empresa-/.agents/instagram/batch-01-diferenciadores.md",
        "out": "KORMAN-Captions-Instagram.pdf",
        "header": "KORMAN ETIQUETAS BORDADAS  ·  CAPTIONS INSTAGRAM  ·  BATCH 01"
    },
    {
        "src": "/home/user/Marketing-y-empresa-/.agents/whatsapp-templates.md",
        "out": "KORMAN-Templates-WhatsApp.pdf",
        "header": "KORMAN ETIQUETAS BORDADAS  ·  TEMPLATES WHATSAPP"
    },
    {
        "src": "/home/user/Marketing-y-empresa-/.agents/paginas/korman-vs-china.md",
        "out": "KORMAN-vs-China.pdf",
        "header": "KORMAN ETIQUETAS BORDADAS  ·  COMPARACIÓN VS IMPORTACIÓN CHINA"
    },
]

def md_to_pdf(src, out_path, header_text):
    with open(src, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown2.markdown(
        md_content,
        extras=["tables", "fenced-code-blocks", "strike", "task_list"]
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>{CSS_STYLE}</style>
</head>
<body>
<div class="header-bar">{header_text}</div>
{html_body}
</body>
</html>"""

    HTML(string=html).write_pdf(out_path, stylesheets=[CSS(string=CSS_STYLE)])

print("Generando PDFs de KORMAN...\n")
for doc in DOCS:
    out = OUT + doc["out"]
    print(f"  {doc['out']}...", end=" ")
    md_to_pdf(doc["src"], out, doc["header"])
    print("✓")

print(f"\n✓ {len(DOCS)} PDFs listos en docs-pdf/")
