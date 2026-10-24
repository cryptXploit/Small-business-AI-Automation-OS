#!/usr/bin/env python3
"""
build.py — Single-Source Multi-Format Publishing Compiler (Phase 5 of 9)
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)

Compiles 8 Production Deliverables from Single-Source Markdown & Vector SVGs:
1. 09-EXPORTS/PDF/the-smallbiz-ai-automation-os-complete-book.pdf (US Letter 8.5x11 Digital Flagship)
2. 09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf (KDP 6x9 Print Interior)
3. 09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub (Validated Reflowable EPUB 3.0)
4. 09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-us-letter.pdf (Fillable AcroForm US Letter)
5. 09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-a4.pdf (Fillable AcroForm ISO A4)
6. 09-EXPORTS/PDF/the-smallbiz-ai-automation-os-tablet-planner.pdf (Landscape 11x8.5 Hyperlinked + AcroForm)
7. 09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf (Tier 0 Lead Magnet Sample Book)
8. 05-WORKBOOKS/chapter-01-workbook.pdf & 09-EXPORTS/PDF/chapter-01-workbook.pdf (Standalone Fillable Ch 1 Workbook)
"""

import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import markdown
import pypdf
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)

STUDIO_ROOT = Path(__file__).resolve().parent

CHAPTER_PARTS = {
    1: ("Part I", "Operations Audit & Zero-Hallucination Safety Architecture"),
    2: None,
    3: ("Part II", "The Revenue Frontline — Speed-to-Lead & Instant Quoting"),
    4: None,
    5: ("Part III", "Customer Experience — Zero-Drop Onboarding, Support & Retention"),
    6: None,
    7: None,
    8: ("Part IV", "Back-Office Autopilot, Living Team SOPs & Executive Command"),
    9: None,
    10: None,
}

CHAPTER_TITLES = {
    1: "Chapter 1: The Owner's Bottleneck — Mapping the 5-Department Automation Engine",
    2: "Chapter 2: The Human-in-the-Loop Architecture — Designing Safe, Zero-Hallucination Workflows",
    3: "Chapter 3: The 60-Second Speed-to-Lead & Multi-Channel Intake System",
    4: "Chapter 4: Automated Estimating, Quotes & Follow-Up Sequences That Close",
    5: "Chapter 5: Frictionless Customer Onboarding, Scheduling & Order Handoffs",
    6: "Chapter 6: 24/7 AI Customer Support Triage, FAQ Resolution & Smart Escalation",
    7: "Chapter 7: Automated Customer Retention, Review Generation & Reactivation Campaigns",
    8: "Chapter 8: Back-Office Autopilot — Invoicing, Payment Chasers, Bookkeeping Prep & Vendor Triage",
    9: "Chapter 9: Internal Team SOPs, Meeting Synthesis & Instant Staff Training Systems",
    10: "Chapter 10: The 15-Minute Friday Owner Scorecard & 90-Day Automation Rollout Roadmap",
}


def find_browser_executable() -> str:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise RuntimeError("No headless Chromium browser (Edge or Chrome) found on system.")


def load_svg_inline(svg_filename: str) -> str:
    svg_path = STUDIO_ROOT / "04-VISUAL-ASSETS" / svg_filename
    if not svg_path.exists():
        return f"<!-- Missing SVG: {svg_filename} -->"
    raw = svg_path.read_text(encoding="utf-8")
    # Remove XML declaration if present
    raw = re.sub(r"<\?xml[^>]*\?>", "", raw).strip()
    # Ensure responsive class on <svg>
    if "<svg " in raw and 'class="' not in raw:
        raw = raw.replace("<svg ", '<svg class="inline-vector-svg" ', 1)
    return raw


def preprocess_markdown_math_and_links(md_text: str) -> str:
    """Convert display/inline LaTeX math formulas into clean styled formula blocks for HTML/EPUB."""
    def replace_display_math(match):
        expr = match.group(1).strip()
        expr = (
            expr.replace(r"\text{", "")
            .replace(r"\left(", "(")
            .replace(r"\right)", ")")
            .replace(r"\times", "×")
            .replace(r"\div", "÷")
            .replace(r"\ge", "≥")
            .replace(r"\le", "≤")
            .replace(r"\$", "$")
            .replace(r"\%", "%")
            .replace("}", "")
        )
        expr = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1) / (\2)", expr)
        expr = expr.replace("_", " ")
        return f'\n<div class="formula-callout"><code>{html.escape(expr)}</code></div>\n'

    md_text = re.sub(r"\$\$(.*?)\$\$", replace_display_math, md_text, flags=re.DOTALL)
    return md_text


def md_to_html_with_inline_svgs(md_text: str, section_id: str) -> str:
    md_text = preprocess_markdown_math_and_links(md_text)
    rendered = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    # Add id to first <h1>
    rendered = re.sub(
        r"<h1>(.*?)</h1>",
        lambda m: f'<h1 id="{section_id}">{m.group(1)}</h1>',
        rendered,
        count=1,
        flags=re.DOTALL,
    )

    # Inline any <img alt="..." src="../04-VISUAL-ASSETS/chapter-XX-....svg" />
    def replace_svg_img(match):
        full_tag = match.group(0)
        alt_match = re.search(r'alt="([^"]*)"', full_tag)
        src_match = re.search(r'src="([^"]*)"', full_tag)
        alt_text = alt_match.group(1) if alt_match else "Architecture Diagram"
        src_val = src_match.group(1) if src_match else ""
        svg_name = os.path.basename(src_val)
        svg_xml = load_svg_inline(svg_name)
        return (
            f'<div class="svg-diagram-box">'
            f'<div class="svg-header-bar">{html.escape(alt_text)}</div>'
            f'<div class="svg-canvas-wrap">{svg_xml}</div>'
            f'</div>'
        )

    rendered = re.sub(
        r'<img[^>]+src="[^"]*04-VISUAL-ASSETS/[^"]+\.svg"[^>]*/?>',
        replace_svg_img,
        rendered,
    )
    return rendered


def get_book_css(mode: str = "digital_letter") -> str:
    """
    Returns print-grade CSS for either:
    - 'digital_letter': Full-color Executive Emerald & Slate US Letter (8.5in x 11in)
    - 'kdp_6x9': Monochrome/Grayscale High-Contrast KDP 6in x 9in with mirrored gutter margins
    """
    if mode == "kdp_6x9":
        page_rule = """
        @page {
            size: 6in 9in;
            margin: 0.65in 0.68in 0.65in 0.68in;
        }
        @page :left {
            size: 6in 9in;
            margin: 0.65in 0.82in 0.65in 0.58in;
        }
        @page :right {
            size: 6in 9in;
            margin: 0.65in 0.58in 0.65in 0.82in;
        }
        """
        accent_primary = "#0F172A"
        accent_secondary = "#1E293B"
        accent_tertiary = "#334155"
        cover_bg = "#FFFFFF"
        cover_fg = "#0F172A"
        cover_border = "4px double #0F172A"
        part_bg = "#F8FAFC"
        part_fg = "#0F172A"
        th_bg = "#1E293B"
        th_fg = "#FFFFFF"
        body_pt = "9.8pt"
        code_pt = "8.4pt"
        table_pt = "8.5pt"
        svg_filter = "filter: grayscale(100%) contrast(115%);"
    else:
        page_rule = """
        @page {
            size: 8.5in 11in;
            margin: 0.75in 0.75in 0.75in 0.75in;
        }
        """
        accent_primary = "#0F172A"
        accent_secondary = "#059669"
        accent_tertiary = "#0284C7"
        cover_bg = "#0F172A"
        cover_fg = "#FFFFFF"
        cover_border = "6px solid #059669"
        part_bg = "#0F172A"
        part_fg = "#FFFFFF"
        th_bg = "#0F172A"
        th_fg = "#FFFFFF"
        body_pt = "10.5pt"
        code_pt = "9.2pt"
        table_pt = "9.5pt"
        svg_filter = ""

    return f"""
    {page_rule}
    * {{
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}
    html, body {{
        margin: 0;
        padding: 0;
        background-color: #FFFFFF;
        color: #1E293B;
        font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
        font-size: {body_pt};
        line-height: 1.56;
    }}
    .title-cover-page {{
        page-break-after: always;
        padding: 0.6in 0.4in;
        background: {cover_bg};
        color: {cover_fg};
        border: {cover_border};
        border-radius: 8px;
        min-height: 8.2in;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .title-cover-badge {{
        display: inline-block;
        background: {accent_secondary};
        color: #FFFFFF;
        font-size: 9pt;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 4px;
        margin-bottom: 18px;
    }}
    .title-cover-h1 {{
        font-size: 26pt;
        font-weight: 800;
        line-height: 1.18;
        margin: 0 0 16px 0;
        color: {cover_fg};
    }}
    .title-cover-subtitle {{
        font-size: 12.5pt;
        font-weight: 400;
        line-height: 1.48;
        opacity: 0.92;
        margin-bottom: 28px;
    }}
    .title-cover-meta-grid {{
        border-top: 2px solid {accent_secondary};
        padding-top: 16px;
        font-size: 9.5pt;
        line-height: 1.6;
    }}
    .toc-page {{
        page-break-after: always;
        padding: 0.2in 0;
    }}
    .toc-title {{
        font-size: 20pt;
        font-weight: 800;
        color: {accent_primary};
        border-bottom: 3px solid {accent_secondary};
        padding-bottom: 8px;
        margin-bottom: 16px;
    }}
    .toc-list {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}
    .toc-part-item {{
        font-weight: 800;
        font-size: 10.5pt;
        color: {accent_secondary};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 14px;
        margin-bottom: 4px;
        border-bottom: 1px solid #CBD5E1;
        padding-bottom: 2px;
    }}
    .toc-chapter-item {{
        margin: 5px 0;
        padding-left: 10px;
        font-size: 10pt;
    }}
    .toc-chapter-item a {{
        color: #0F172A;
        text-decoration: none;
        font-weight: 600;
    }}
    .toc-chapter-item a:hover {{
        text-decoration: underline;
    }}
    .part-divider-banner {{
        page-break-before: always;
        background: {part_bg};
        color: {part_fg};
        border-left: 8px solid {accent_secondary};
        border-top: 1px solid #CBD5E1;
        border-right: 1px solid #CBD5E1;
        border-bottom: 1px solid #CBD5E1;
        padding: 24px 28px;
        border-radius: 6px;
        margin-bottom: 22px;
    }}
    .part-divider-label {{
        font-size: 9.5pt;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: {accent_secondary if mode != 'kdp_6x9' else '#475569'};
        margin-bottom: 6px;
    }}
    .part-divider-title {{
        font-size: 18pt;
        font-weight: 800;
        margin: 0;
    }}
    .chapter-section {{
        page-break-before: always;
    }}
    .chapter-with-part {{
        page-break-before: avoid;
    }}
    h1 {{
        font-size: 19pt;
        font-weight: 800;
        color: {accent_primary};
        border-bottom: 3px solid {accent_secondary};
        padding-bottom: 8px;
        margin-top: 0;
        margin-bottom: 16px;
        line-height: 1.25;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 14pt;
        font-weight: 700;
        color: {accent_primary};
        border-left: 4px solid {accent_secondary};
        padding-left: 10px;
        margin-top: 22px;
        margin-bottom: 10px;
        line-height: 1.3;
        page-break-after: avoid;
    }}
    h3 {{
        font-size: 11.5pt;
        font-weight: 700;
        color: {accent_tertiary};
        margin-top: 16px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    h4 {{
        font-size: 10.5pt;
        font-weight: 700;
        color: #334155;
        margin-top: 12px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }}
    p {{
        margin: 0 0 10px 0;
        text-align: left;
        orphans: 3;
        widows: 3;
    }}
    ul, ol {{
        margin: 0 0 12px 0;
        padding-left: 22px;
    }}
    li {{
        margin-bottom: 4px;
    }}
    hr {{
        border: 0;
        border-top: 1px solid #CBD5E1;
        margin: 18px 0;
    }}
    blockquote {{
        margin: 14px 0;
        padding: 12px 16px;
        background: #F8FAFC;
        border-left: 4px solid #D97706;
        color: #0F172A;
        border-radius: 0 6px 6px 0;
        page-break-inside: avoid;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: {table_pt};
        line-height: 1.4;
        page-break-inside: auto;
    }}
    tr {{
        page-break-inside: avoid;
        page-break-after: auto;
    }}
    thead {{
        display: table-header-group;
    }}
    th {{
        background-color: {th_bg};
        color: {th_fg};
        font-weight: 700;
        text-align: left;
        padding: 7px 9px;
        border: 1px solid #334155;
    }}
    td {{
        padding: 6px 9px;
        border: 1px solid #CBD5E1;
        vertical-align: top;
        overflow-wrap: anywhere;
        word-break: break-word;
    }}
    tbody tr:nth-child(even) {{
        background-color: #F8FAFC;
    }}
    pre {{
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid {accent_tertiary};
        border-radius: 5px;
        padding: 10px 12px;
        font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, 'Courier New', monospace;
        font-size: {code_pt};
        line-height: 1.42;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: anywhere;
        margin: 12px 0;
    }}
    code {{
        font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, 'Courier New', monospace;
        font-size: {code_pt};
        background-color: #F1F5F9;
        padding: 1px 4px;
        border-radius: 3px;
        color: #0F172A;
    }}
    pre code {{
        background: none;
        padding: 0;
    }}
    .formula-callout {{
        background: #F8FAFC;
        border: 1px solid #94A3B8;
        border-left: 4px solid {accent_secondary};
        padding: 10px 14px;
        margin: 12px 0;
        border-radius: 4px;
        font-weight: 600;
        page-break-inside: avoid;
    }}
    .svg-diagram-box {{
        margin: 16px 0;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        background: #FFFFFF;
        padding: 8px;
        page-break-inside: avoid;
        text-align: center;
        {svg_filter}
    }}
    .svg-header-bar {{
        font-size: 9pt;
        font-weight: 700;
        color: {accent_primary};
        background: #F1F5F9;
        padding: 5px 10px;
        margin-bottom: 6px;
        border-radius: 4px;
        text-align: left;
    }}
    .svg-canvas-wrap svg {{
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        display: block;
        margin: 0 auto;
    }}
    """


def get_omar_sunny_cover_b64() -> str:
    import base64
    cover_jpg = STUDIO_ROOT / "08-COVER-DESIGN" / "omar-sunny-custom-front-cover.jpg"
    if not cover_jpg.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(cover_jpg.read_bytes()).decode("ascii")


def build_complete_book_html(mode: str = "digital_letter") -> str:
    css = get_book_css(mode)
    edition_badge = (
        "2026 Digital Flagship Operating Edition (US Letter)"
        if mode == "digital_letter"
        else "2026 Trade Paperback Print Edition (6\" × 9\" KDP Specification)"
    )

    toc_items_html = [
        '<li class="toc-chapter-item"><a href="#front-matter">Front Matter: Executive Preface, 3 Execution Tracks &amp; Safety Covenant</a></li>'
    ]
    for ch_num in range(1, 11):
        if CHAPTER_PARTS[ch_num] is not None:
            p_code, p_title = CHAPTER_PARTS[ch_num]
            toc_items_html.append(f'<li class="toc-part-item">{p_code} — {html.escape(p_title)}</li>')
        toc_items_html.append(
            f'<li class="toc-chapter-item"><a href="#chapter-{ch_num:02d}">{html.escape(CHAPTER_TITLES[ch_num])}</a></li>'
        )
    toc_items_html.append(
        '<li class="toc-part-item">Back Matter &amp; Reference Vault</li>'
        '<li class="toc-chapter-item"><a href="#back-matter">Master 50-Prompt Index, 12 Emergency Operations Scripts &amp; 40-Term Glossary</a></li>'
    )

    sections_html = []

    # Front Matter
    fm_text = (STUDIO_ROOT / "03-MANUSCRIPT" / "front-matter.md").read_text(encoding="utf-8")
    sections_html.append(
        f'<section class="chapter-section">{md_to_html_with_inline_svgs(fm_text, "front-matter")}</section>'
    )

    # Chapters 1 to 10
    for ch_num in range(1, 11):
        ch_text = (STUDIO_ROOT / "03-MANUSCRIPT" / f"chapter-{ch_num:02d}.md").read_text(encoding="utf-8")
        ch_html = md_to_html_with_inline_svgs(ch_text, f"chapter-{ch_num:02d}")
        if CHAPTER_PARTS[ch_num] is not None:
            p_code, p_title = CHAPTER_PARTS[ch_num]
            sections_html.append(
                f'<div class="part-divider-banner">'
                f'<div class="part-divider-label">{p_code}</div>'
                f'<div class="part-divider-title">{html.escape(p_title)}</div>'
                f'</div>'
                f'<section class="chapter-with-part">{ch_html}</section>'
            )
        else:
            sections_html.append(f'<section class="chapter-section">{ch_html}</section>')

    # Back Matter
    bm_text = (STUDIO_ROOT / "03-MANUSCRIPT" / "back-matter.md").read_text(encoding="utf-8")
    sections_html.append(
        f'<section class="chapter-section">{md_to_html_with_inline_svgs(bm_text, "back-matter")}</section>'
    )

    cover_b64 = get_omar_sunny_cover_b64()
    img_max_h = "3.45in" if mode == "kdp_6x9" else "4.6in"
    img_filter = "filter: grayscale(100%) contrast(110%);" if mode == "kdp_6x9" else ""
    cover_img_html = (
        f'<div style="text-align:center; margin: 6px 0 10px 0;">'
        f'<img src="{cover_b64}" alt="Book Cover" style="max-height:{img_max_h}; width:auto; border-radius:6px; border:1px solid #334155; {img_filter}"/>'
        f'</div>'
        if cover_b64
        else ""
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>The Small Business AI Automation Operating System</title>
<style>
{css}
.title-cover-page {{
    min-height: {"7.2in" if mode == "kdp_6x9" else "8.2in"} !important;
    padding: {"0.28in 0.3in" if mode == "kdp_6x9" else "0.4in 0.4in"} !important;
}}
.title-cover-h1 {{
    font-size: {"18pt" if mode == "kdp_6x9" else "22pt"} !important;
    margin: 0 0 8px 0 !important;
}}
.title-cover-subtitle {{
    font-size: {"9.5pt" if mode == "kdp_6x9" else "11pt"} !important;
    margin-bottom: 8px !important;
}}
</style>
</head>
<body>
<div class="title-cover-page">
  <div>
    <div class="title-cover-badge">{edition_badge}</div>
    <h1 class="title-cover-h1" style="border:none;">The Small Business AI Automation Operating System</h1>
    <div class="title-cover-subtitle">
      A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff
    </div>
    {cover_img_html}
  </div>
  <div class="title-cover-meta-grid">
    <strong>Author:</strong> Omar Sunny &nbsp;|&nbsp; <strong>System ID:</strong> SMALLBIZ-AI-AUTOMATION-OS-V1 &nbsp;|&nbsp; <strong>Access Code:</strong> SMALLBIZ-OS-PRO-2026<br/>
    <strong>Architecture:</strong> 10 Core Modules &bull; 50 Tested AI Prompts &bull; 20 Vector Architecture Diagrams &bull; 12 Emergency Scripts
  </div>
</div>

<div class="toc-page">
  <div class="toc-title">Master Table of Contents</div>
  <ul class="toc-list">
    {"".join(toc_items_html)}
  </ul>
</div>

{"".join(sections_html)}
</body>
</html>"""

    # For KDP 6x9 Print Interior, strip clickable <a href="..."> tags so zero non-printable PDF link annotations are emitted
    if mode == "kdp_6x9":
        full_html = re.sub(r'<a\s+[^>]*href="[^"]*"[^>]*>(.*?)</a>', r'<span>\1</span>', full_html, flags=re.DOTALL)

    return full_html


def render_html_to_pdf(browser_exe: str, html_content: str, output_pdf_path: Path) -> None:
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "render_input.html"
        tmp_html.write_text(html_content, encoding="utf-8")
        file_url = tmp_html.as_uri()
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-extensions",
            "--no-pdf-header-footer",
            f"--print-to-pdf={str(output_pdf_path)}",
            file_url,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def inject_pdf_metadata_and_acroform(
    pdf_path: Path,
    title: str,
    subject: str,
    inject_form_fields: bool = False,
    field_prefix: str = "OS_Workbook",
    strip_non_printable_annots: bool = False,
) -> dict:
    """
    Opens a rendered PDF with pypdf, attaches standard document metadata,
    and optionally injects interactive /AcroForm text fields (/FT /Tx) across pages
    or strips non-printable link annotations (/Annots) for KDP Print-on-Demand.
    Returns {"pages": int, "width_pt": float, "height_pt": float, "acroform_fields": int}.
    """
    reader = pypdf.PdfReader(str(pdf_path))
    writer = pypdf.PdfWriter()
    for page in reader.pages:
        if strip_non_printable_annots and "/Annots" in page:
            del page[NameObject("/Annots")]
        writer.add_page(page)
    if strip_non_printable_annots:
        for page in writer.pages:
            if "/Annots" in page:
                del page[NameObject("/Annots")]

    writer.add_metadata(
        {
            "/Title": title,
            "/Author": "Omar Sunny",
            "/Subject": subject,
            "/Keywords": "Small Business AI Automation, T.R.A.V. Gate, SOPs, Speed-to-Lead, Make.com, n8n, Zapier",
            "/Creator": "SmallBiz AI Automation OS Single-Source Compiler v1.0",
            "/Producer": "Executive Systems Publishing Studio (pypdf)",
        }
    )

    total_fields = 0
    if inject_form_fields:
        helv_font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/Helvetica"),
            }
        )
        helv_ref = writer._add_object(helv_font)
        fields_array = ArrayObject()

        # Add interactive text fields across pages so users can type notes & sign-offs directly in the PDF
        num_pages = len(writer.pages)
        for idx, page in enumerate(writer.pages):
            mb = page.mediabox
            w = float(mb.width)
            h = float(mb.height)

            # Create 2 interactive fields per page (Owner Action Notes + Verification Sign-Off)
            field_specs = [
                (
                    f"{field_prefix}_Page_{idx+1:02d}_Action_Notes",
                    "Enter implementation notes, owner assignments, or threshold overrides...",
                    [36.0, 22.0, w - 210.0, 40.0],
                ),
                (
                    f"{field_prefix}_Page_{idx+1:02d}_Verified_By",
                    "Owner Sign-Off & Date",
                    [w - 200.0, 22.0, w - 36.0, 40.0],
                ),
            ]
            if NamedAnnots := page.get("/Annots"):
                annots = NamedAnnots
            else:
                annots = ArrayObject()
                page[NameObject("/Annots")] = annots

            for f_name, f_tip, rect_coords in field_specs:
                widget = DictionaryObject(
                    {
                        NameObject("/Type"): NameObject("/Annot"),
                        NameObject("/Subtype"): NameObject("/Widget"),
                        NameObject("/FT"): NameObject("/Tx"),
                        NameObject("/T"): TextStringObject(f_name),
                        NameObject("/TU"): TextStringObject(f_tip),
                        NameObject("/V"): TextStringObject(""),
                        NameObject("/DV"): TextStringObject(""),
                        NameObject("/Ff"): NumberObject(0),
                        NameObject("/F"): NumberObject(4),
                        NameObject("/Rect"): ArrayObject([FloatObject(c) for c in rect_coords]),
                        NameObject("/DA"): TextStringObject("/Helv 8.5 Tf 0.06 0.09 0.16 rg"),
                        NameObject("/P"): page.indirect_reference,
                    }
                )
                widget_ref = writer._add_object(widget)
                annots.append(widget_ref)
                fields_array.append(widget_ref)
                total_fields += 1

        acroform = DictionaryObject(
            {
                NameObject("/Fields"): fields_array,
                NameObject("/NeedAppearances"): BooleanObject(True),
                NameObject("/DA"): TextStringObject("/Helv 9 Tf 0.06 0.09 0.16 rg"),
                NameObject("/DR"): DictionaryObject(
                    {
                        NameObject("/Font"): DictionaryObject({NameObject("/Helv"): helv_ref}),
                    }
                ),
            }
        )
        writer._root_object[NameObject("/AcroForm")] = writer._add_object(acroform)

    tmp_out = pdf_path.with_suffix(".tmp.pdf")
    with open(tmp_out, "wb") as f:
        writer.write(f)
    tmp_out.replace(pdf_path)

    verify_reader = pypdf.PdfReader(str(pdf_path))
    p0 = verify_reader.pages[0].mediabox
    return {
        "pages": len(verify_reader.pages),
        "width_pt": round(float(p0.width), 2),
        "height_pt": round(float(p0.height), 2),
        "acroform_fields": total_fields,
        "bytes": pdf_path.stat().st_size,
    }


def build_workbook_html(page_size_css: str, edition_label: str, chapters_range=range(1, 11)) -> str:
    sections_html = []
    toc_rows = []
    for i in chapters_range:
        ws_path = STUDIO_ROOT / "05-WORKBOOKS" / f"worksheet-{i:02d}.md"
        ws_text = ws_path.read_text(encoding="utf-8")
        ws_html = md_to_html_with_inline_svgs(ws_text, f"worksheet-{i:02d}")
        # Include the chapter's mindmap SVG (and flowchart SVG for standalone Ch 1 workbook) as visual architecture reference
        svg_ref_box = (
            f'<div class="svg-diagram-box">'
            f'<div class="svg-header-bar">Chapter {i} System Mindmap Quick-Reference Diagram</div>'
            f'<div class="svg-canvas-wrap">{load_svg_inline(f"chapter-{i:02d}-mindmap.svg")}</div>'
            f'</div>'
        )
        if len(list(chapters_range)) == 1:
            svg_ref_box += (
                f'<div class="svg-diagram-box">'
                f'<div class="svg-header-bar">Chapter {i} Operational Decision Tree Reference</div>'
                f'<div class="svg-canvas-wrap">{load_svg_inline(f"chapter-{i:02d}-flowchart.svg")}</div>'
                f'</div>'
            )
        interactive_box = (
            f'<div class="fillable-signoff-box">'
            f'<strong>Interactive Implementation Notes &amp; Owner Sign-Off (Worksheet {i:02d}):</strong><br/>'
            f'<span>Assigned Champion: ______________________ &nbsp;|&nbsp; Target Go-Live Date: ____/____/2026 &nbsp;|&nbsp; Gate Status: [ ] Green [ ] Amber</span>'
            f'</div>'
        )
        sections_html.append(
            f'<section class="chapter-section">{ws_html}{svg_ref_box}{interactive_box}</section>'
        )
        toc_rows.append(
            f'<tr><td><strong>Worksheet {i:02d}</strong></td>'
            f'<td><a href="#worksheet-{i:02d}">{html.escape(CHAPTER_TITLES[i])}</a></td>'
            f'<td>[ &nbsp; ] Not Started &nbsp; [ &nbsp; ] In Progress &nbsp; [ &nbsp; ] Live</td></tr>'
        )

    base_css = get_book_css("digital_letter")
    custom_css = f"""
    @page {{
        size: {page_size_css};
        margin: 0.65in 0.65in 0.72in 0.65in;
    }}
    .fillable-signoff-box {{
        margin-top: 14px;
        padding: 12px 14px;
        background: #F0FDF4;
        border: 1.5px dashed #059669;
        border-radius: 6px;
        font-size: 9.5pt;
        page-break-inside: avoid;
    }}
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Action Workbooks — {edition_label}</title>
<style>{base_css}\n{custom_css}</style>
</head>
<body>
<div class="title-cover-page">
  <div>
    <div class="title-cover-badge">{html.escape(edition_label)} &bull; Interactive AcroForm Edition</div>
    <h1 class="title-cover-h1" style="border:none;">The Small Business AI Automation Action Workbook Suite</h1>
    <div class="title-cover-subtitle">
      Fill-in-the-Blank Audit Scorecards, Deterministic SKU Canvases, T.R.A.V. Gate Checklists &amp; 90-Day Rollout Trackers
    </div>
  </div>
  <div class="title-cover-meta-grid">
    <strong>Companion to:</strong> The Small Business AI Automation Operating System (SMALLBIZ-OS-PRO-2026)<br/>
    <strong>Interactive PDF Instructions:</strong> Type directly into the interactive AcroForm fields at the bottom of any page or print for tabletop team workshops.
  </div>
</div>

<div class="toc-page">
  <div class="toc-title">Master Implementation Scoreboard &amp; Workbook Index</div>
  <table>
    <thead>
      <tr><th style="width:18%;">Worksheet</th><th style="width:54%;">Module &amp; Operational Focus</th><th style="width:28%;">Rollout Status</th></tr>
    </thead>
    <tbody>
      {"".join(toc_rows)}
    </tbody>
  </table>
</div>

{"".join(sections_html)}
</body>
</html>"""


def build_tablet_planner_html() -> str:
    """Builds the Landscape 11in x 8.5in Hyperlinked Interactive Tablet Planner HTML."""
    nav_bar = """
    <div class="tablet-top-nav">
      <span class="nav-brand">SMALLBIZ AI OS</span>
      <a href="#tab-home">1. Command Home</a>
      <a href="#tab-audit">2. 5-Day Audit</a>
      <a href="#tab-depts">3. 5-Dept Boards</a>
      <a href="#tab-worksheets">4. Worksheets 1–10</a>
      <a href="#tab-prompts">5. 50 Prompts &amp; 12 Scripts</a>
      <a href="#tab-rollout">6. 90-Day Sprint</a>
      <a href="#tab-scorecard">7. Friday Scorecard</a>
    </div>
    """

    # Collect condensed interactive views + diagrams + worksheets so it spans 22+ rich landscape pages
    dept_boards_html = []
    dept_mappings = [
        ("Dept 01: Sales, Speed-to-Lead & Proposals", 3, 4),
        ("Dept 02: Zero-Drop Onboarding & Scheduling", 5, 2),
        ("Dept 03: 24/7 Support Triage & 5-Star Retention", 6, 7),
        ("Dept 04: Back-Office Invoicing, A/R & OCR Bills", 8, 1),
        ("Dept 05: Living Team SOPs & Executive Command", 9, 10),
    ]
    for dept_title, ch_a, ch_b in dept_mappings:
        dept_boards_html.append(
            f'<div class="planner-page">'
            f'{nav_bar}'
            f'<h2>{html.escape(dept_title)} — Architecture Board</h2>'
            f'<div class="two-col-svg">'
            f'<div class="svg-diagram-box"><div class="svg-header-bar">Ch {ch_a} System Mindmap</div>'
            f'<div class="svg-canvas-wrap">{load_svg_inline(f"chapter-{ch_a:02d}-mindmap.svg")}</div></div>'
            f'<div class="svg-diagram-box"><div class="svg-header-bar">Ch {ch_b} Decision Flowchart</div>'
            f'<div class="svg-canvas-wrap">{load_svg_inline(f"chapter-{ch_b:02d}-flowchart.svg")}</div></div>'
            f'</div>'
            f'</div>'
        )

    ws_summary_pages = []
    for i in range(1, 11):
        ws_md = (STUDIO_ROOT / "05-WORKBOOKS" / f"worksheet-{i:02d}.md").read_text(encoding="utf-8")
        # Take the first ~3,500 chars of each worksheet for crisp landscape execution boards
        ws_excerpt = "\n".join(ws_md.splitlines()[:65])
        ws_html = md_to_html_with_inline_svgs(ws_excerpt, f"planner-ws-{i:02d}")
        ws_summary_pages.append(
            f'<div class="planner-page" id="tab-ws-{i:02d}">'
            f'{nav_bar}'
            f'{ws_html}'
            f'</div>'
        )

    bm_md = (STUDIO_ROOT / "03-MANUSCRIPT" / "back-matter.md").read_text(encoding="utf-8")
    bm_index_lines = []
    for line in bm_md.splitlines():
        if line.startswith("## Part II:"):
            break
        bm_index_lines.append(line)
    prompt_index_html = md_to_html_with_inline_svgs("\n".join(bm_index_lines), "tab-prompts-table")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Interactive Landscape Tablet Planner — The Small Business AI Automation OS</title>
<style>
@page {{
    size: 11in 8.5in;
    margin: 0.45in 0.5in 0.55in 0.5in;
}}
* {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}
body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.45;
    color: #1E293B;
    background: #FFFFFF;
}}
.planner-page {{
    page-break-before: always;
}}
.planner-cover {{
    background: #0F172A;
    color: #FFFFFF;
    padding: 0.55in;
    border: 5px solid #059669;
    border-radius: 10px;
    min-height: 7.2in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.tablet-top-nav {{
    background: #0F172A;
    color: #FFFFFF;
    padding: 7px 12px;
    border-radius: 6px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 3px solid #059669;
}}
.tablet-top-nav .nav-brand {{
    font-weight: 800;
    color: #10B981;
    font-size: 9.5pt;
    letter-spacing: 1px;
}}
.tablet-top-nav a {{
    color: #FFFFFF;
    text-decoration: none;
    font-size: 8.5pt;
    font-weight: 600;
    padding: 4px 8px;
    background: #1E293B;
    border-radius: 4px;
    border: 1px solid #334155;
}}
h1, h2 {{
    color: #0F172A;
    margin-top: 6px;
    margin-bottom: 8px;
    border-bottom: 2px solid #059669;
    padding-bottom: 4px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-bottom: 10px;
}}
th {{
    background: #0F172A;
    color: #FFFFFF;
    padding: 5px 7px;
    border: 1px solid #334155;
    text-align: left;
}}
td {{
    padding: 5px 7px;
    border: 1px solid #CBD5E1;
    vertical-align: top;
}}
tbody tr:nth-child(even) {{
    background: #F8FAFC;
}}
.two-col-svg {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}}
.svg-diagram-box {{
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px;
    background: #FFFFFF;
}}
.svg-header-bar {{
    font-size: 8.5pt;
    font-weight: 700;
    background: #F1F5F9;
    padding: 4px 8px;
    margin-bottom: 4px;
}}
.svg-canvas-wrap svg {{
    width: 100% !important;
    height: auto !important;
}}
.grid-cards {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 10px;
}}
.nav-card {{
    border: 1.5px solid #059669;
    background: #F8FAFC;
    border-radius: 6px;
    padding: 10px 12px;
}}
.nav-card a {{
    font-weight: 800;
    color: #0F172A;
    text-decoration: none;
    font-size: 10.5pt;
}}
</style>
</head>
<body>
<div class="planner-cover" id="tab-home">
  {nav_bar}
  <div>
    <div style="color:#10B981;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">
      Interactive Landscape Tablet Command Planner (11" × 8.5" &bull; AcroForm + Hyperlinked Tabs)
    </div>
    <h1 style="color:#FFFFFF;font-size:24pt;border:none;margin:0 0 10px 0;">
      The Small Business AI Automation Operating System — Executive Tablet Planner
    </h1>
    <p style="color:#E2E8F0;font-size:11pt;margin-bottom:16px;">
      Tap any tab in the top navigation bar or the quick-jump cards below to navigate across your 5-Day Bottleneck Audit, 5-Department Architecture Boards, Worksheets 1–10, 50 Prompt Index, 90-Day Sprint Tracker, and 15-Minute Friday Owner Scorecard.
    </p>
    <div class="grid-cards" style="color:#0F172A;">
      <div class="nav-card"><a href="#tab-audit">Tab 2: 5-Day Time &amp; Lead-Leak Audit &rarr;</a><br/>Log staff hours, calculate Cost of Manual Friction (CMF), and score P.A.C.E. priorities.</div>
      <div class="nav-card"><a href="#tab-depts">Tab 3: 5-Department Visual Boards &rarr;</a><br/>Interactive system mindmaps and deterministic flowcharts for all 5 departments.</div>
      <div class="nav-card"><a href="#tab-worksheets">Tab 4: Worksheets 1–10 Execution Grids &rarr;</a><br/>Direct jump to all 10 departmental implementation worksheets.</div>
      <div class="nav-card"><a href="#tab-prompts">Tab 5: 50 Prompts &amp; 12 Emergency Scripts &rarr;</a><br/>Complete master lookup table for Prompts 1.1–10.5 and Red-Gate crisis scripts.</div>
      <div class="nav-card"><a href="#tab-rollout">Tab 6: 90-Day Phased Rollout Sprint &rarr;</a><br/>12-week milestone tracker with Day 30 / Day 60 / Day 90 exit gates.</div>
      <div class="nav-card"><a href="#tab-scorecard">Tab 7: 15-Minute Friday Owner Scorecard &rarr;</a><br/>12-week executive telemetry log across all 18 core small business vital signs.</div>
    </div>
  </div>
  <div style="border-top:1px solid #334155;padding-top:10px;font-size:8.5pt;color:#94A3B8;">
    Access Code: <strong>SMALLBIZ-OS-PRO-2026</strong> &nbsp;|&nbsp; Compatible with iPad (GoodNotes / Notability / PDF Expert), Android Tablets &amp; Desktop Adobe/Edge PDF Readers
  </div>
</div>

<div class="planner-page" id="tab-audit">
  {nav_bar}
  <h2>Tab 2: 5-Day Business Time &amp; Lead-Leak Audit Tracker</h2>
  <p>Record every repetitive administrative task, missed call, slow quote, and manual invoice batch across 5 consecutive business days, then compute your Cost of Manual Friction (CMF) and P.A.C.E. Priority Score.</p>
  <table>
    <thead>
      <tr><th>Department</th><th>Repetitive Task / Bottleneck</th><th>Freq / Wk</th><th>Mins / Occurrence</th><th>Weekly Hours</th><th>Hourly Cost ($)</th><th>Annual Bleed ($)</th><th>P.A.C.E. Score (1–20)</th><th>Target Prompt ID</th></tr>
    </thead>
    <tbody>
      <tr><td>01. Sales &amp; Leads</td><td>After-hours web inquiries &amp; missed-call callbacks</td><td>35</td><td>8 mins</td><td>4.67 hrs</td><td>$35.00</td><td>$8,499</td><td>19 / 20</td><td>Prompt 3.1 / 3.3</td></tr>
      <tr><td>01. Sales &amp; Quotes</td><td>Rewriting field notes into 3-tier quotes + 14d follow-up</td><td>18</td><td>25 mins</td><td>7.50 hrs</td><td>$45.00</td><td>$17,550</td><td>18 / 20</td><td>Prompt 4.1 / 4.3</td></tr>
      <tr><td>02. Onboarding</td><td>Chasing signed contracts, deposits &amp; incomplete intake forms</td><td>12</td><td>20 mins</td><td>4.00 hrs</td><td>$32.00</td><td>$6,656</td><td>17 / 20</td><td>Prompt 5.1 / 5.3</td></tr>
      <tr><td>03. Support &amp; Reviews</td><td>Answering repetitive Tier-1 FAQs &amp; requesting Google reviews</td><td>60</td><td>6 mins</td><td>6.00 hrs</td><td>$28.00</td><td>$8,736</td><td>17 / 20</td><td>Prompt 6.2 / 7.2</td></tr>
      <tr><td>04. Finance &amp; A/R</td><td>Friday billing batch, overdue invoice chasing &amp; receipt OCR</td><td>40</td><td>12 mins</td><td>8.00 hrs</td><td>$40.00</td><td>$16,640</td><td>19 / 20</td><td>Prompt 8.1 / 8.2 / 8.3</td></tr>
      <tr><td>05. Team &amp; Admin</td><td>Answering repetitive staff SOP questions &amp; Friday KPI prep</td><td>25</td><td>10 mins</td><td>4.17 hrs</td><td>$65.00</td><td>$14,095</td><td>18 / 20</td><td>Prompt 9.4 / 10.1</td></tr>
      <tr><td><strong>Your Custom Row 1</strong></td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
      <tr><td><strong>Your Custom Row 2</strong></td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
      <tr><td><strong>Your Custom Row 3</strong></td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
    </tbody>
  </table>
</div>

<div id="tab-depts">
  {"".join(dept_boards_html)}
</div>

<div id="tab-worksheets">
  {"".join(ws_summary_pages)}
</div>

<div class="planner-page" id="tab-prompts">
  {nav_bar}
  {prompt_index_html}
</div>

<div class="planner-page" id="tab-rollout">
  {nav_bar}
  <h2>Tab 6: 90-Day Phased Automation Rollout Sprint Board (Weeks 1–12)</h2>
  <table>
    <thead>
      <tr><th>Sprint Phase</th><th>Week</th><th>Chapter &amp; Prompts</th><th>Core Operational Milestone</th><th>Champion</th><th>Budget Hrs</th><th>Exit Gate Verified</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Phase I (Days 1–30)</strong></td><td>Week 1</td><td>Ch 1 (Prompts 1.1–1.5)</td><td>Complete 5-Dept Audit &amp; P.A.C.E. Priority Matrix</td><td>Owner</td><td>2.5 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase I (Days 1–30)</strong></td><td>Week 2</td><td>Ch 2 (Prompts 2.1–2.5)</td><td>Deploy T.R.A.V. Safety Gate, DLQ &amp; Slack #approvals</td><td>Ops Lead</td><td>3.0 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase I (Days 1–30)</strong></td><td>Week 3</td><td>Ch 3 (Prompts 3.1–3.5)</td><td>Launch 60-Second Lead Capture &amp; Missed-Call Text-Back</td><td>Sales Lead</td><td>3.5 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase I (Days 1–30)</strong></td><td>Week 4</td><td>Ch 4 (Prompts 4.1–4.5)</td><td>Activate Voice-to-Quote &amp; 14-Day Proposal Follow-Up</td><td>Sales Lead</td><td>3.0 hrs</td><td>[ &nbsp; ] GATE 1 PASSED</td></tr>
      <tr><td><strong>Phase II (Days 31–60)</strong></td><td>Week 5</td><td>Ch 8A (Prompts 8.1–8.2)</td><td>Deploy Instant Milestone Invoicing &amp; 5-Stage AR Chaser</td><td>Billing</td><td>3.5 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase II (Days 31–60)</strong></td><td>Week 6</td><td>Ch 8B (Prompts 8.3–8.5)</td><td>Launch OCR Receipt Triage, 5% Price-Creep &amp; Pre-Close</td><td>Billing</td><td>3.0 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase II (Days 31–60)</strong></td><td>Week 7</td><td>Ch 5 (Prompts 5.1–5.5)</td><td>Wire Zero-Drop Payment-to-Onboarding &amp; Intake Chaser</td><td>Onboarding</td><td>3.0 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase II (Days 31–60)</strong></td><td>Week 8</td><td>Ch 6 (Prompts 6.1–6.5)</td><td>Launch Grounded 30-Doc Support RAG Bot &amp; Red Escalation</td><td>Support</td><td>3.5 hrs</td><td>[ &nbsp; ] GATE 2 PASSED</td></tr>
      <tr><td><strong>Phase III (Days 61–90)</strong></td><td>Week 9</td><td>Ch 7 (Prompts 7.1–7.5)</td><td>Activate Sentiment-Gated 5★ Reviews &amp; 60/90/180d Win-Back</td><td>Marketing</td><td>3.0 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase III (Days 61–90)</strong></td><td>Week 10</td><td>Ch 9A (Prompts 9.1–9.2)</td><td>Record Top 25 3-Min Looms &rarr; 7-Block Living SOP Vault</td><td>All Leads</td><td>3.5 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase III (Days 61–90)</strong></td><td>Week 11</td><td>Ch 9B (Prompts 9.3–9.5)</td><td>Launch @SOP-Bot in #ask-the-sop &amp; 7-Day New-Hire Quiz</td><td>Ops Lead</td><td>3.0 hrs</td><td>[ &nbsp; ] Done</td></tr>
      <tr><td><strong>Phase III (Days 61–90)</strong></td><td>Week 12</td><td>Ch 10 (Prompts 10.1–10.5)</td><td>Activate 15-Minute Friday Owner Scorecard &amp; Monday Brief</td><td>Owner</td><td>2.5 hrs</td><td>[ &nbsp; ] GATE 3 PASSED</td></tr>
    </tbody>
  </table>
</div>

<div class="planner-page" id="tab-scorecard">
  {nav_bar}
  <h2>Tab 7: 15-Minute Friday Owner KPI Scorecard Log (12-Week Rolling Telemetry)</h2>
  <table>
    <thead>
      <tr>
        <th>Department &amp; Vital Sign KPI</th><th>Green Target</th>
        <th>W1</th><th>W2</th><th>W3</th><th>W4</th><th>W5</th><th>W6</th><th>W7</th><th>W8</th><th>W9</th><th>W10</th><th>W11</th><th>W12</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>Sales:</strong> Median Speed-to-Lead (Sec)</td><td>&lt; 60s</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Sales:</strong> Booked Consults / Visits</td><td>&ge; 45%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Sales:</strong> 14-Day Quote Close Rate %</td><td>&ge; 38%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Onboarding:</strong> Intake Complete &lt; 48h %</td><td>&ge; 85%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Onboarding:</strong> On-Time Delivery SLA %</td><td>&ge; 95%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Support:</strong> Tier-1 AI Deflection %</td><td>60–78%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Reputation:</strong> New 5★ Google Reviews</td><td>&ge; 4/wk</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Retention:</strong> Dormant Win-Back Revenue ($)</td><td>Tracked</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Finance:</strong> Weekly Cash Collected ($)</td><td>&ge; 95%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Finance:</strong> Overdue A/R &gt; 15 Days %</td><td>&lt; 5.0%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Finance:</strong> Days Sales Outstanding (DSO)</td><td>&le; 16d</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Team OS:</strong> @SOP-Bot Deflection Rate %</td><td>&ge; 75%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Team OS:</strong> Workflow Exception Rate %</td><td>&lt; 1.5%</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><td><strong>Team OS:</strong> Total Staff Hours Saved / Wk</td><td>&ge; 25h</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    </tbody>
  </table>
</div>
</body>
</html>"""


def build_tier0_sample_html() -> str:
    css = get_book_css("digital_letter")
    fm_text = (STUDIO_ROOT / "03-MANUSCRIPT" / "front-matter.md").read_text(encoding="utf-8")
    ch1_text = (STUDIO_ROOT / "03-MANUSCRIPT" / "chapter-01.md").read_text(encoding="utf-8")
    ws1_text = (STUDIO_ROOT / "05-WORKBOOKS" / "worksheet-01.md").read_text(encoding="utf-8")

    upgrade_cta_html = """
    <section class="chapter-section">
      <h1>Upgrade to the Complete Small Business AI Automation Operating System</h1>
      <p>You have just completed <strong>Chapter 1</strong> and <strong>Worksheet 1 (The 5-Day Business Time &amp; Lead-Leak Audit)</strong> from <em>The Small Business AI Automation Operating System</em>.</p>
      <h2>Complete 5-Tier Product Ecosystem &amp; Value Ladder</h2>
      <table>
        <thead>
          <tr><th>Edition Tier</th><th>Included Deliverables &amp; Assets</th><th>Ideal For</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Tier 0: Free Starter Audit Kit</strong><br/><em>(Current Edition)</em></td><td>Executive Front Matter + Complete Chapter 1 + 2 Vector Architecture Diagrams + Prompts 1.1–1.5 + Fillable Worksheet 1 Audit</td><td>Owners benchmarking their 5-department time &amp; lead bleed</td></tr>
          <tr><td><strong>Tier 1: Digital Core Book &amp; EPUB</strong></td><td>Full 111,900-word, 10-Chapter Operating Manual (PDF + EPUB 3.0) + 50 Copy-Paste Prompts + 20 Vector Diagrams + 12 Emergency Scripts</td><td>Self-implementers building workflows step-by-step</td></tr>
          <tr><td><strong>Tier 2: Action Workbook &amp; Planner Suite</strong></td><td>All 10 Fillable Action Workbooks (US Letter &amp; ISO A4) + Landscape Interactive Tablet Planner + Visual Shortcut Desk Cards</td><td>Hands-on workshops with office managers &amp; department leads</td></tr>
          <tr><td><strong>Tier 3: Pro Interactive Web App &amp; Notion/Excel OS</strong></td><td>Offline-First Interactive Web App (<code>SMALLBIZ-OS-PRO-2026</code>) + 5-Database Notion OS Kit + 8-Tab Charted Excel Command Center</td><td>Teams centralizing SOPs, KPI scorecards &amp; ROI calculators</td></tr>
          <tr><td><strong>Tier 4: Master Hybrid Bundle &amp; JSON Blueprints</strong></td><td>Everything in Tiers 1–3 + 5 Importable Make.com/Zapier/n8n JSON Workflow Blueprints + Editable Word (.docx) SOPs &amp; PowerPoint (.pptx) Decks</td><td>Turnkey 90-day 5-department deployment saving 15–25+ hrs/week</td></tr>
        </tbody>
      </table>
      <blockquote>
        <strong>Unlock Your Companion Web Application Today:</strong> Open <code>07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html</code> and enter Edition Access Code <strong><code>SMALLBIZ-OS-PRO-2026</code></strong> to launch the interactive 5-Department ROI Calculator and 50-Prompt Customizer.
      </blockquote>
    </section>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Tier 0 Free Starter Kit — Chapter 1 &amp; 5-Day Automation Audit</title>
<style>{css}</style>
</head>
<body>
<div class="title-cover-page">
  <div>
    <div class="title-cover-badge">Tier 0 Free Executive Starter Kit &bull; Sample Chapter + Audit Workbook</div>
    <h1 class="title-cover-h1" style="border:none;">The Small Business AI Automation Operating System</h1>
    <div class="title-cover-subtitle">
      Complimentary Executive Preview: Full Front Matter, Chapter 1 (The Owner's Bottleneck), Prompts 1.1–1.5 &amp; Fillable Worksheet 1 Audit
    </div>
  </div>
  <div class="title-cover-meta-grid">
    <strong>Pro Upgrade Code:</strong> SMALLBIZ-OS-PRO-2026 &nbsp;|&nbsp; <strong>Full Edition:</strong> 10 Chapters &bull; 50 Prompts &bull; 20 Vector Diagrams
  </div>
</div>
<section class="chapter-section">{md_to_html_with_inline_svgs(fm_text, "front-matter")}</section>
<section class="chapter-section">{md_to_html_with_inline_svgs(ch1_text, "chapter-01")}</section>
<section class="chapter-section">{md_to_html_with_inline_svgs(ws1_text, "worksheet-01")}</section>
{upgrade_cta_html}
</body>
</html>"""


def sanitize_html_Fragment_to_strict_xhtml(html_fragment: str) -> str:
    """
    Converts HTML output from Python-Markdown into 100% strict, well-formed XHTML/XML
    using Python's standard HTMLParser stack serializer so ET.fromstring() always succeeds.
    """
    from html.parser import HTMLParser
    from xml.sax.saxutils import escape as xml_escape, quoteattr as xml_quoteattr

    html_fragment = re.sub(
        r'src="\.\./04-VISUAL-ASSETS/([^"]+\.svg)"',
        r'src="images/\1"',
        html_fragment,
    )

    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }
    ALLOWED_TAGS = {
        "div", "span", "p", "h1", "h2", "h3", "h4", "h5", "h6",
        "ul", "ol", "li", "dl", "dt", "dd", "table", "thead", "tbody",
        "tfoot", "tr", "th", "td", "pre", "code", "blockquote", "em",
        "strong", "b", "i", "u", "s", "del", "ins", "sub", "sup", "a",
        "hr", "br", "img", "section", "article", "nav", "header", "footer"
    }

    class StrictXHTMLSerializer(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.out = []
            self.stack = []

        def handle_starttag(self, tag, attrs):
            tag = tag.lower()
            if tag not in ALLOWED_TAGS:
                # Was a raw '<something>' in prose that HTMLParser treated as a tag
                self.out.append(xml_escape(f"<{tag}>"))
                return
            attr_str = ""
            seen_attrs = set()
            for k, v in attrs:
                k_clean = re.sub(r"[^a-zA-Z0-9_:-]", "", k.lower())
                if not k_clean or k_clean in seen_attrs:
                    continue
                seen_attrs.add(k_clean)
                val = v if v is not None else k_clean
                attr_str += f" {k_clean}={xml_quoteattr(str(val))}"
            if tag in VOID_TAGS:
                self.out.append(f"<{tag}{attr_str}/>")
            else:
                self.out.append(f"<{tag}{attr_str}>")
                self.stack.append(tag)

        def handle_startendtag(self, tag, attrs):
            tag = tag.lower()
            if tag not in ALLOWED_TAGS:
                self.out.append(xml_escape(f"<{tag}/>"))
                return
            attr_str = ""
            seen_attrs = set()
            for k, v in attrs:
                k_clean = re.sub(r"[^a-zA-Z0-9_:-]", "", k.lower())
                if not k_clean or k_clean in seen_attrs:
                    continue
                seen_attrs.add(k_clean)
                val = v if v is not None else k_clean
                attr_str += f" {k_clean}={xml_quoteattr(str(val))}"
            self.out.append(f"<{tag}{attr_str}/>")

        def handle_endtag(self, tag):
            tag = tag.lower()
            if tag in VOID_TAGS or tag not in ALLOWED_TAGS:
                return
            if tag in self.stack:
                while self.stack:
                    top = self.stack.pop()
                    self.out.append(f"</{top}>")
                    if top == tag:
                        break

        def handle_data(self, data):
            self.out.append(xml_escape(data))

    serializer = StrictXHTMLSerializer()
    serializer.feed(html_fragment)
    serializer.close()
    while serializer.stack:
        serializer.out.append(f"</{serializer.stack.pop()}>")
    return "".join(serializer.out)



def build_epub3(epub_path: Path) -> dict:
    """Packages a validated, reflowable EPUB 3.0 archive at epub_path."""
    epub_path.parent.mkdir(parents=True, exist_ok=True)
    if epub_path.exists():
        epub_path.unlink()

    book_uuid = "urn:uuid:7c9e6679-7425-40de-944b-e07fc1f90ae7"
    modified_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    epub_css = """
    body {
        font-family: 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif;
        color: #1E293B;
        background-color: #FFFFFF;
        line-height: 1.58;
        margin: 1.2em;
    }
    h1 {
        color: #0F172A;
        border-bottom: 3px solid #059669;
        padding-bottom: 0.3em;
        font-size: 1.65em;
    }
    h2 {
        color: #0F172A;
        border-left: 4px solid #059669;
        padding-left: 0.5em;
        font-size: 1.3em;
        margin-top: 1.4em;
    }
    h3 {
        color: #0284C7;
        font-size: 1.1em;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        font-size: 0.88em;
    }
    th {
        background-color: #0F172A;
        color: #FFFFFF;
        padding: 6px 8px;
        border: 1px solid #334155;
        text-align: left;
    }
    td {
        padding: 6px 8px;
        border: 1px solid #CBD5E1;
        vertical-align: top;
    }
    pre {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #0284C7;
        padding: 10px;
        font-family: monospace;
        font-size: 0.85em;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    blockquote {
        background-color: #F8FAFC;
        border-left: 4px solid #D97706;
        padding: 10px 14px;
        margin: 1em 0;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    .formula-callout {
        background-color: #F8FAFC;
        border-left: 4px solid #059669;
        padding: 8px 12px;
        margin: 1em 0;
        font-family: monospace;
    }
    """

    content_docs = [
        ("front-matter", "front-matter.xhtml", "Front Matter: Executive Preface & Ecosystem Guide", STUDIO_ROOT / "03-MANUSCRIPT" / "front-matter.md"),
    ]
    for i in range(1, 11):
        content_docs.append(
            (
                f"chapter-{i:02d}",
                f"chapter-{i:02d}.xhtml",
                CHAPTER_TITLES[i],
                STUDIO_ROOT / "03-MANUSCRIPT" / f"chapter-{i:02d}.md",
            )
        )
    content_docs.append(
        ("back-matter", "back-matter.xhtml", "Back Matter: 50-Prompt Index, 12 Emergency Scripts & Glossary", STUDIO_ROOT / "03-MANUSCRIPT" / "back-matter.md")
    )

    xhtml_payloads = {}
    for item_id, filename, title_str, md_path in content_docs:
        raw_md = preprocess_markdown_math_and_links(md_path.read_text(encoding="utf-8"))
        body_html = markdown.markdown(raw_md, extensions=["tables", "fenced_code", "sane_lists"])
        body_xhtml = sanitize_html_Fragment_to_strict_xhtml(body_html)
        full_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>{html.escape(title_str)}</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
{body_xhtml}
</body>
</html>"""
        # Validate XML well-formedness at build time
        ET.fromstring(full_xhtml.encode("utf-8"))
        xhtml_payloads[filename] = full_xhtml

    # Build nav.xhtml
    nav_lis = "\n".join(
        f'        <li><a href="{fname}">{html.escape(t_str)}</a></li>'
        for _, fname, t_str, _ in content_docs
    )
    nav_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Table of Contents — The Small Business AI Automation Operating System</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
{nav_lis}
    </ol>
  </nav>
</body>
</html>"""
    ET.fromstring(nav_xhtml.encode("utf-8"))

    # Build toc.ncx
    nav_points = []
    for idx, (item_id, fname, t_str, _) in enumerate(content_docs, start=1):
        nav_points.append(
            f"""    <navPoint id="navPoint-{idx}" playOrder="{idx}">
      <navLabel><text>{html.escape(t_str)}</text></navLabel>
      <content src="{fname}"/>
    </navPoint>"""
        )
    toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_uuid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>The Small Business AI Automation Operating System</text></docTitle>
  <navMap>
{chr(10).join(nav_points)}
  </navMap>
</ncx>"""
    ET.fromstring(toc_ncx.encode("utf-8"))

    # Build content.opf
    manifest_items = [
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="css" href="styles.css" media-type="text/css"/>',
    ]
    spine_items = []
    for item_id, fname, _, _ in content_docs:
        manifest_items.append(
            f'    <item id="{item_id}" href="{fname}" media-type="application/xhtml+xml"/>'
        )
        spine_items.append(f'    <itemref idref="{item_id}"/>')

    svg_files = []
    for i in range(1, 11):
        for s_type in ["mindmap", "flowchart"]:
            s_name = f"chapter-{i:02d}-{s_type}.svg"
            s_id = f"svg-{i:02d}-{s_type}"
            svg_files.append(s_name)
            manifest_items.append(
                f'    <item id="{s_id}" href="images/{s_name}" media-type="image/svg+xml"/>'
            )

    content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_uuid}</dc:identifier>
    <dc:title>The Small Business AI Automation Operating System: A Practical System to Automate Lead Capture, Customer Follow-Ups, Invoicing, and Daily Operations</dc:title>
    <dc:creator>Executive Systems Publishing Studio</dc:creator>
    <dc:publisher>Executive Systems Publishing Studio</dc:publisher>
    <dc:language>en</dc:language>
    <dc:rights>Copyright (c) 2026 Executive Systems Publishing Studio. All rights reserved.</dc:rights>
    <dc:description>Complete 10-chapter operational manual with 50 tested AI workflow prompts, 20 vector architecture diagrams, and 12 emergency scripts for 1-to-25 person businesses.</dc:description>
    <meta property="dcterms:modified">{modified_utc}</meta>
  </metadata>
  <manifest>
{chr(10).join(manifest_items)}
  </manifest>
  <spine toc="ncx">
{chr(10).join(spine_items)}
  </spine>
</package>"""
    ET.fromstring(content_opf.encode("utf-8"))

    container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
    ET.fromstring(container_xml.encode("utf-8"))

    with zipfile.ZipFile(str(epub_path), "w") as zf:
        # Entry 0: uncompressed mimetype with zero extra fields
        mime_info = zipfile.ZipInfo("mimetype")
        mime_info.compress_type = zipfile.ZIP_STORED
        mime_info.extra = b""
        zf.writestr(mime_info, b"application/epub+zip")

        zf.writestr("META-INF/container.xml", container_xml.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/styles.css", epub_css.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/content.opf", content_opf.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/toc.ncx", toc_ncx.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)

        for fname, payload in xhtml_payloads.items():
            zf.writestr(f"OEBPS/{fname}", payload.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)

        for s_name in svg_files:
            svg_bytes = (STUDIO_ROOT / "04-VISUAL-ASSETS" / s_name).read_bytes()
            ET.fromstring(svg_bytes)
            zf.writestr(f"OEBPS/images/{s_name}", svg_bytes, compress_type=zipfile.ZIP_DEFLATED)

    return {
        "bytes": epub_path.stat().st_size,
        "xhtml_files": len(xhtml_payloads) + 1,
        "svg_files": len(svg_files),
    }


def main():
    browser_exe = find_browser_executable()
    print(f"[build.py] Using Headless Browser: {browser_exe}")
    results = {}

    # 1. Deliverable 1: Complete Digital Flagship Book PDF (US Letter)
    pdf_complete = STUDIO_ROOT / "09-EXPORTS" / "PDF" / "the-smallbiz-ai-automation-os-complete-book.pdf"
    print("[build.py] Compiling Deliverable 1: Complete Digital Flagship Book PDF...")
    render_html_to_pdf(browser_exe, build_complete_book_html("digital_letter"), pdf_complete)
    results["complete_book_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_complete,
        title="The Small Business AI Automation Operating System — Complete Digital Edition",
        subject="Complete 10-Chapter Small Business AI Automation Operating System (US Letter)",
        inject_form_fields=False,
    )

    # 2. Deliverable 2: Amazon KDP 6"x9" Paperback Print-Ready Interior PDF
    pdf_kdp = STUDIO_ROOT / "09-EXPORTS" / "PRINT" / "the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf"
    print("[build.py] Compiling Deliverable 2: Amazon KDP 6x9 Paperback Print Interior PDF...")
    render_html_to_pdf(browser_exe, build_complete_book_html("kdp_6x9"), pdf_kdp)
    results["kdp_6x9_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_kdp,
        title="The Small Business AI Automation Operating System — KDP 6x9 Print Edition",
        subject="Amazon KDP 6x9 Trade Paperback Print Interior with Mirrored Gutter Margins",
        inject_form_fields=False,
        strip_non_printable_annots=True,
    )

    # 3. Deliverable 3: Validated Reflowable EPUB 3.0
    epub_out = STUDIO_ROOT / "09-EXPORTS" / "EPUB" / "the-smallbiz-ai-automation-os.epub"
    print("[build.py] Compiling Deliverable 3: Reflowable EPUB 3.0 eBook...")
    results["epub_3"] = build_epub3(epub_out)

    # 4. Deliverable 4: Fillable Action Workbooks (US Letter)
    pdf_wb_letter = STUDIO_ROOT / "09-EXPORTS" / "PRINT" / "the-smallbiz-ai-automation-os-workbook-us-letter.pdf"
    print("[build.py] Compiling Deliverable 4: Fillable Action Workbook (US Letter)...")
    render_html_to_pdf(
        browser_exe,
        build_workbook_html("8.5in 11in", "US Letter (8.5\" × 11\") Fillable Edition"),
        pdf_wb_letter,
    )
    results["workbook_us_letter_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_wb_letter,
        title="The Small Business AI Automation Action Workbook — US Letter Fillable Edition",
        subject="10-Chapter Interactive AcroForm Action Workbook (US Letter 8.5x11)",
        inject_form_fields=True,
        field_prefix="WB_USLetter",
    )

    # 5. Deliverable 5: Fillable Action Workbooks (ISO A4)
    pdf_wb_a4 = STUDIO_ROOT / "09-EXPORTS" / "PRINT" / "the-smallbiz-ai-automation-os-workbook-a4.pdf"
    print("[build.py] Compiling Deliverable 5: Fillable Action Workbook (ISO A4)...")
    render_html_to_pdf(
        browser_exe,
        build_workbook_html("210mm 297mm", "International ISO A4 (210mm × 297mm) Fillable Edition"),
        pdf_wb_a4,
    )
    results["workbook_a4_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_wb_a4,
        title="The Small Business AI Automation Action Workbook — ISO A4 Fillable Edition",
        subject="10-Chapter Interactive AcroForm Action Workbook (ISO A4 210x297mm)",
        inject_form_fields=True,
        field_prefix="WB_ISO_A4",
    )

    # 6. Deliverable 6: Hyperlinked Landscape Interactive Tablet Planner PDF
    pdf_tablet = STUDIO_ROOT / "09-EXPORTS" / "PDF" / "the-smallbiz-ai-automation-os-tablet-planner.pdf"
    print("[build.py] Compiling Deliverable 6: Landscape Interactive Tablet Planner PDF...")
    render_html_to_pdf(browser_exe, build_tablet_planner_html(), pdf_tablet)
    results["tablet_planner_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_tablet,
        title="The Small Business AI Automation OS — Interactive Landscape Tablet Planner",
        subject="Hyperlinked 7-Tab Landscape Tablet Command Planner (11x8.5) with AcroForm Fields",
        inject_form_fields=True,
        field_prefix="Tablet_Planner",
    )

    # 7. Deliverable 7A: Tier 0 Free Sample Book (Front Matter + Ch 1 + WS 1 + Value Ladder)
    pdf_tier0 = STUDIO_ROOT / "09-EXPORTS" / "PDF" / "tier0-free-sample-chapter01-and-audit.pdf"
    print("[build.py] Compiling Deliverable 7A: Tier 0 Free Starter Kit Sample PDF...")
    render_html_to_pdf(browser_exe, build_tier0_sample_html(), pdf_tier0)
    results["tier0_sample_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_tier0,
        title="The Small Business AI Automation OS — Free Starter Kit (Chapter 1 + Audit)",
        subject="Complimentary Executive Sample: Front Matter, Chapter 1 & Worksheet 1 Audit",
        inject_form_fields=True,
        field_prefix="Tier0_Audit",
    )

    # 8. Deliverable 7B: Standalone Chapter 1 Fillable Workbook PDF
    pdf_ch1_wb = STUDIO_ROOT / "05-WORKBOOKS" / "chapter-01-workbook.pdf"
    pdf_ch1_wb_export = STUDIO_ROOT / "09-EXPORTS" / "PDF" / "chapter-01-workbook.pdf"
    print("[build.py] Compiling Deliverable 7B: Standalone Chapter 1 Fillable Workbook PDF...")
    render_html_to_pdf(
        browser_exe,
        build_workbook_html("8.5in 11in", "Chapter 1 Standalone Audit Workbook", chapters_range=range(1, 2)),
        pdf_ch1_wb,
    )
    results["chapter_01_workbook_pdf"] = inject_pdf_metadata_and_acroform(
        pdf_ch1_wb,
        title="Worksheet 1: The 5-Day Business Time & Lead-Leak Audit (Fillable Workbook)",
        subject="Standalone Fillable Chapter 1 Action Workbook",
        inject_form_fields=True,
        field_prefix="Ch01_Workbook",
    )
    shutil.copyfile(pdf_ch1_wb, pdf_ch1_wb_export)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
