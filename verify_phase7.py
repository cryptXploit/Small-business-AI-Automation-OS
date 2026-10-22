#!/usr/bin/env python3
"""
Phase 7 Automated Verification Gate (verify_phase7.py)
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)
Verifies:
  1. 5-Database Minimalist Notion OS Kit CSV row counts, uniform column counts, and Markdown guides (>=1,500 & >=2,000 words)
  2. 6 Master Vector Cover SVGs (valid XML + Executive Emerald & Slate palette)
  3. 6 High-Res PNG Covers (valid PNG header + IHDR pixel dimensions + size > 40 KB)
  4. KDP Full-Wrap Print Cover PDF (1 page, 12.795" x 9.25" / 921.24 x 666.0 pt within ±2 pt)
  5. Zero banned AI clichés & zero placeholders across all Phase 7 files
  6. Updates PROJECT_STATE.json and writes 11-QA-REPORTS/phase7-qa-report.json & phase7-qa-report.md
"""

import csv
import datetime
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader

STUDIO_ROOT = Path(__file__).resolve().parent
NOTION_DIR = STUDIO_ROOT / "06-NOTION-TEMPLATES"
COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
QA_DIR = STUDIO_ROOT / "11-QA-REPORTS"
QA_DIR.mkdir(parents=True, exist_ok=True)

BANNED_WORDS = [
    "delve",
    "tapestry",
    "testament",
    "beacon",
    "symphony",
    "unlock",
    "unleash",
    "skyrocket",
    "supercharge",
    "game-changer",
    "pivotal",
    "realm",
    "foster",
    "underscore",
    "utilize",
    "leverage",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"Lorem ipsum",
    r"\[XX\]",
]


def scan_banned_and_placeholders(file_path: Path, text: str, errors: list):
    rel = file_path.relative_to(STUDIO_ROOT).as_posix()
    for bw in BANNED_WORDS:
        pat = re.compile(r"\b" + re.escape(bw) + r"(?:s|ed|ing|er)?\b", flags=re.IGNORECASE)
        matches = pat.findall(text)
        if matches:
            errors.append(f"[{rel}] Banned word '{bw}' detected ({len(matches)} occurrences: {matches[:3]})")
    for ph in PLACEHOLDER_PATTERNS:
        pat = re.compile(ph, flags=re.IGNORECASE if "Lorem" in ph else 0)
        matches = pat.findall(text)
        if matches:
            errors.append(f"[{rel}] Forbidden placeholder '{ph}' detected ({len(matches)} occurrences)")


def verify_csv_file(rel_path: str, min_rows: int, exact_rows: int, errors: list) -> dict:
    fpath = STUDIO_ROOT / rel_path
    if not fpath.is_file():
        errors.append(f"Missing CSV file: {rel_path}")
        return {"exists": False}

    raw_text = fpath.read_text(encoding="utf-8")
    scan_banned_and_placeholders(fpath, raw_text, errors)

    with fpath.open("r", encoding="utf-8", newline="") as f:
        reader = list(csv.reader(f))

    if not reader:
        errors.append(f"CSV file {rel_path} is empty.")
        return {"exists": True, "data_rows": 0, "columns": 0}

    headers = reader[0]
    data_rows = reader[1:]
    col_count = len(headers)

    for idx, r in enumerate(data_rows, start=2):
        if len(r) != col_count:
            errors.append(f"[{rel_path}] Row {idx} has {len(r)} columns, expected {col_count}")

    if exact_rows is not None and len(data_rows) != exact_rows:
        errors.append(f"[{rel_path}] Expected exactly {exact_rows} data rows, found {len(data_rows)}")
    elif min_rows is not None and len(data_rows) < min_rows:
        errors.append(f"[{rel_path}] Expected >= {min_rows} data rows, found {len(data_rows)}")

    return {
        "bytes": fpath.stat().st_size,
        "size_kb": round(fpath.stat().st_size / 1024, 2),
        "columns": col_count,
        "data_rows": len(data_rows),
    }


def verify_md_file(rel_path: str, min_words: int, errors: list) -> dict:
    fpath = STUDIO_ROOT / rel_path
    if not fpath.is_file():
        errors.append(f"Missing Markdown file: {rel_path}")
        return {"exists": False}

    text = fpath.read_text(encoding="utf-8")
    scan_banned_and_placeholders(fpath, text, errors)
    words = len(text.split())
    if words < min_words:
        errors.append(f"[{rel_path}] Word count {words} is below minimum {min_words}")
    return {
        "bytes": fpath.stat().st_size,
        "size_kb": round(fpath.stat().st_size / 1024, 2),
        "lines": len(text.splitlines()),
        "words": words,
    }


def verify_svg_and_png(stem: str, expected_w: int, expected_h: int, errors: list) -> dict:
    svg_rel = f"08-COVER-DESIGN/{stem}.svg"
    png_rel = f"08-COVER-DESIGN/{stem}.png"
    svg_path = STUDIO_ROOT / svg_rel
    png_path = STUDIO_ROOT / png_rel
    res = {}

    if not svg_path.is_file():
        errors.append(f"Missing SVG cover: {svg_rel}")
    else:
        svg_text = svg_path.read_text(encoding="utf-8")
        scan_banned_and_placeholders(svg_path, svg_text, errors)
        try:
            ET.fromstring(svg_text)
        except Exception as e:
            errors.append(f"[{svg_rel}] XML parse error: {e}")

        for req_hex in ("#0F172A", "#059669"):
            if req_hex.lower() not in svg_text.lower():
                errors.append(f"[{svg_rel}] Missing required palette color {req_hex}")

        res["svg_bytes"] = svg_path.stat().st_size
        res["svg_kb"] = round(svg_path.stat().st_size / 1024, 2)

    if not png_path.is_file():
        errors.append(f"Missing PNG cover: {png_rel}")
    else:
        png_bytes = png_path.stat().st_size
        if png_bytes < 40 * 1024:
            errors.append(f"[{png_rel}] File size ({png_bytes} B) is below 40 KB minimum.")
        with png_path.open("rb") as pf:
            hdr = pf.read(24)
        if len(hdr) < 24 or hdr[:8] != b"\x89PNG\r\n\x1a\n" or hdr[12:16] != b"IHDR":
            errors.append(f"[{png_rel}] Invalid PNG binary signature or IHDR chunk.")
        else:
            w, h = struct.unpack(">II", hdr[16:24])
            res["png_bytes"] = png_bytes
            res["png_kb"] = round(png_bytes / 1024, 2)
            res["png_dimensions"] = f"{w}x{h}"
            if expected_w and expected_h and (w != expected_w or h != expected_h):
                errors.append(f"[{png_rel}] Expected {expected_w}x{expected_h} px, got {w}x{h} px.")

    return res


def verify_kdp_wrap_pdf(rel_path: str, errors: list) -> dict:
    fpath = STUDIO_ROOT / rel_path
    if not fpath.is_file():
        errors.append(f"Missing KDP Full-Wrap PDF: {rel_path}")
        return {"exists": False}

    reader = PdfReader(str(fpath))
    page_count = len(reader.pages)
    if page_count != 1:
        errors.append(f"[{rel_path}] Expected 1 page, found {page_count} pages.")

    mb = reader.pages[0].mediabox
    w_pt = float(mb.width)
    h_pt = float(mb.height)
    expected_w_pt = 12.795 * 72.0  # 921.24 pt
    expected_h_pt = 9.250 * 72.0   # 666.00 pt

    if abs(w_pt - expected_w_pt) > 2.0 or abs(h_pt - expected_h_pt) > 2.0:
        errors.append(
            f"[{rel_path}] Dimensions {w_pt:.2f}x{h_pt:.2f} pt outside ±2 pt tolerance of {expected_w_pt:.2f}x{expected_h_pt:.2f} pt."
        )

    return {
        "bytes": fpath.stat().st_size,
        "size_kb": round(fpath.stat().st_size / 1024, 2),
        "pages": page_count,
        "dimensions_pt": f"{w_pt:.2f} x {h_pt:.2f}",
        "dimensions_in": f"{w_pt / 72.0:.3f} x {h_pt / 72.0:.3f}",
    }


def main():
    errors = []
    if not (STUDIO_ROOT / "build_phase7.py").is_file():
        errors.append("Missing build_phase7.py in studio root.")

    notion_metrics = {
        "06-NOTION-TEMPLATES/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv", 25, None, errors
        ),
        "06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv", 25, None, errors
        ),
        "06-NOTION-TEMPLATES/03-AI-Prompt-and-SOP-Vault-62.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/03-AI-Prompt-and-SOP-Vault-62.csv", None, 62, errors
        ),
        "06-NOTION-TEMPLATES/Spreadsheets/62-Item-Prompt-and-SOP-Vault.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/Spreadsheets/62-Item-Prompt-and-SOP-Vault.csv", None, 62, errors
        ),
        "06-NOTION-TEMPLATES/04-Weekly-Owner-KPI-Scorecard.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/04-Weekly-Owner-KPI-Scorecard.csv", 12, None, errors
        ),
        "06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.csv", 20, None, errors
        ),
        "06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv": verify_csv_file(
            "06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", 20, None, errors
        ),
        "06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.md": verify_md_file(
            "06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.md", 1500, errors
        ),
        "06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md": verify_md_file(
            "06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md", 2000, errors
        ),
    }

    cover_metrics = {
        "ebook-cover-kdp-kindle": verify_svg_and_png("ebook-cover-kdp-kindle", 1600, 2560, errors),
        "kdp-paperback-full-wrap-cover": verify_svg_and_png("kdp-paperback-full-wrap-cover", 2559, 1850, errors),
        "gumroad-tier0-free-audit-cover": verify_svg_and_png("gumroad-tier0-free-audit-cover", 1600, 1200, errors),
        "gumroad-tier2-workbook-atlas-cover": verify_svg_and_png("gumroad-tier2-workbook-atlas-cover", 1600, 1200, errors),
        "gumroad-tier3-flagship-os-bundle-cover": verify_svg_and_png("gumroad-tier3-flagship-os-bundle-cover", 1600, 1200, errors),
        "gumroad-tier4-living-vault-membership-cover": verify_svg_and_png("gumroad-tier4-living-vault-membership-cover", 1600, 1200, errors),
        "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf": verify_kdp_wrap_pdf(
            "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf", errors
        ),
        "09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf": verify_kdp_wrap_pdf(
            "09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf", errors
        ),
        "08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md": verify_md_file(
            "08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md", 1500, errors
        ),
    }

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    status = "PASSED" if len(errors) == 0 else "FAILED"

    report = {
        "phase": 7,
        "status": status,
        "timestamp": now_utc,
        "error_count": len(errors),
        "errors": errors,
        "kdp_spine_calculation": {
            "interior_pages": 242,
            "spine_width_in": 0.545,
            "full_wrap_width_in": 12.795,
            "full_wrap_height_in": 9.250,
            "full_wrap_pt": "921.24 x 666.00",
        },
        "notion_os_kit": notion_metrics,
        "commercial_cover_suite": cover_metrics,
    }

    (QA_DIR / "phase7-qa-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# Phase 7 QA Report — 5-Database Minimalist Notion OS Kit & Commercial Cover Suite",
        "",
        f"- **Status:** `{status}`",
        f"- **Timestamp (UTC):** `{now_utc}`",
        f"- **QA Errors:** `{len(errors)}`",
        "",
        "## 1. Notion OS Kit Verification (`06-NOTION-TEMPLATES/`)",
        "",
        "| Deliverable | Size (KB) | Rows / Words | Columns / Lines |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for k, v in notion_metrics.items():
        if "data_rows" in v:
            md_lines.append(f"| `{k}` | `{v['size_kb']} KB` | `{v['data_rows']} rows` | `{v['columns']} cols` |")
        else:
            md_lines.append(f"| `{k}` | `{v['size_kb']} KB` | `{v['words']} words` | `{v['lines']} lines` |")

    md_lines.extend([
        "",
        "## 2. Commercial Cover Suite Verification (`08-COVER-DESIGN/`)",
        "",
        "| Asset | SVG Size | PNG Size & Dimensions | PDF / Spec Verification |",
        "| :--- | :--- | :--- | :--- |",
    ])
    for k, v in cover_metrics.items():
        if "svg_kb" in v:
            md_lines.append(
                f"| `{k}` | `{v['svg_kb']} KB` | `{v['png_kb']} KB` (`{v['png_dimensions']} px`) | XML & IHDR Verified |"
            )
        elif "dimensions_pt" in v:
            md_lines.append(
                f"| `{k}` | N/A | N/A | `{v['size_kb']} KB`, `{v['pages']} page`, `{v['dimensions_pt']} pt` (`{v['dimensions_in']} in`) |"
            )
        else:
            md_lines.append(f"| `{k}` | N/A | N/A | `{v['size_kb']} KB`, `{v['words']} words` |")

    (QA_DIR / "phase7-qa-report.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if len(errors) == 0:
        state_path = STUDIO_ROOT / "PROJECT_STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "PHASE_7_COMPLETE"
        if 7 not in state.get("phases_completed", []):
            state["phases_completed"].append(7)
        state["phases"]["Phase 7"] = {
            "title": "5-Database Minimalist Notion OS Kit & Commercial Cover Suite",
            "status": "COMPLETED",
            "verified": True,
            "qa_errors": 0,
            "verified_at_utc": now_utc,
            "deliverables": list(notion_metrics.keys()) + [
                "08-COVER-DESIGN/ebook-cover-kdp-kindle.svg",
                "08-COVER-DESIGN/ebook-cover-kdp-kindle.png",
                "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.svg",
                "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.png",
                "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf",
                "09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf",
                "08-COVER-DESIGN/gumroad-tier0-free-audit-cover.svg",
                "08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png",
                "08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.svg",
                "08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png",
                "08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.svg",
                "08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png",
                "08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.svg",
                "08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png",
                "08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md",
                "11-QA-REPORTS/phase7-qa-report.json",
                "11-QA-REPORTS/phase7-qa-report.md",
                "build_phase7.py",
                "verify_phase7.py",
            ],
        }
        state["cumulative_metrics_phase7"] = {
            "notion_os_kit": notion_metrics,
            "commercial_cover_suite": cover_metrics,
        }
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    sys.exit(0 if len(errors) == 0 else 1)


if __name__ == "__main__":
    main()
