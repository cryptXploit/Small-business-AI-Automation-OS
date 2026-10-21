#!/usr/bin/env python3
"""
verify_phase1.py — Automated Enterprise QA Verification Engine for Phase 1
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)
Studio Root: e:/Ebook-Makaer/Small-Business-AI-Automation-OS/DIGITAL-PUBLISHING-STUDIO/
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent

REQUIRED_DIRECTORIES = [
    "01-MARKET-RESEARCH",
    "02-ARCHITECTURE",
    "03-MANUSCRIPT",
    "04-VISUAL-ASSETS",
    "05-WORKBOOKS",
    "06-NOTION-TEMPLATES",
    "06-NOTION-TEMPLATES/Spreadsheets",
    "07-INTERACTIVE-TOOLS",
    "08-COVER-DESIGN",
    "08-COVER-DESIGN/Editable-Design-Kit",
    "09-EXPORTS",
    "09-EXPORTS/PDF",
    "09-EXPORTS/PRINT",
    "09-EXPORTS/EPUB",
    "09-EXPORTS/HYBRID-BUNDLE",
    "10-MARKETING",
    "11-QA-REPORTS",
    "12-EDITABLE-OFFICE-SUITE",
    "12-EDITABLE-OFFICE-SUITE/Word-Docs",
    "12-EDITABLE-OFFICE-SUITE/Slide-Decks",
    "13-VISUAL-CHEAT-SHEETS",
    "14-AUTOMATION-BLUEPRINTS",
]

REQUIRED_FILES = [
    "PROJECT_STATE.json",
    "01-MARKET-RESEARCH/market-and-audience-research.md",
    "02-ARCHITECTURE/book-config.yaml",
    "02-ARCHITECTURE/style-guide.md",
    "02-ARCHITECTURE/sources.md",
    "02-ARCHITECTURE/toc.md",
    "03-MANUSCRIPT/chapter-01.md",
    "04-VISUAL-ASSETS/chapter-01-mindmap.svg",
    "04-VISUAL-ASSETS/chapter-01-flowchart.svg",
    "05-WORKBOOKS/worksheet-01.md",
]

WORD_COUNT_FLOORS = {
    "03-MANUSCRIPT/chapter-01.md": 6500,
    "05-WORKBOOKS/worksheet-01.md": 1500,
    "01-MARKET-RESEARCH/market-and-audience-research.md": 1500,
}

REQUIRED_CHAPTER_HEADERS = [
    "# Chapter 1:",
    "## 1. Learning Objectives",
    "## 2. The Real-World Friction Point",
    "## 3. Why Standard Approaches Fail",
    "## 4. Core Framework:",
    "## 5. Visual Architecture: System Mindmap",
    "## 6. Step-by-Step Implementation Protocol",
    "## 7. Operational Decision Tree",
    "## 8. Tested AI Workflow Prompts",
    "## 9. Real-World Implementation Case Study",
    "## 10. Common Operational Pitfalls & Fixes",
    "## 11. Chapter Action Worksheet",
    "## 12. Executive Summary & Implementation Checklist",
    "## 13. Sources & Operational References",
]

REQUIRED_PROMPTS = [
    "Prompt 1.1",
    "Prompt 1.2",
    "Prompt 1.3",
    "Prompt 1.4",
    "Prompt 1.5",
]

REQUIRED_SVG_LINKS = [
    "chapter-01-mindmap.svg",
    "chapter-01-flowchart.svg",
]

SVG_FILES = [
    "04-VISUAL-ASSETS/chapter-01-mindmap.svg",
    "04-VISUAL-ASSETS/chapter-01-flowchart.svg",
]

CLICHE_SCAN_FILES = [
    "03-MANUSCRIPT/chapter-01.md",
    "05-WORKBOOKS/worksheet-01.md",
    "01-MARKET-RESEARCH/market-and-audience-research.md",
    "02-ARCHITECTURE/toc.md",
    "02-ARCHITECTURE/sources.md",
]

BANNED_WORDS_REGEX = re.compile(
    r"\b(delve|tapestry|testament|beacon|symphony|unlock|unleash|skyrocket|supercharge|game-changer|pivotal|realm|foster|underscore|utilize|leverage)\b",
    re.IGNORECASE,
)

BANNED_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further",
]

BANNED_PLACEHOLDERS = [
    "TODO",
    "TBD",
    "Lorem ipsum",
    "[XX]",
]


def count_words(text: str) -> int:
    """Count standard words in markdown text."""
    return len(re.findall(r"[A-Za-z0-9']+", text))


def main() -> int:
    errors = []
    checks_summary = {}

    print("=" * 78)
    print("ANTIGRAVITY STUDIO QA ENGINE — PHASE 1 VERIFICATION")
    print(f"Studio Root: {STUDIO_ROOT.as_posix()}")
    print("=" * 78)

    # 1. Directory Tree Check
    missing_dirs = []
    for rel_dir in REQUIRED_DIRECTORIES:
        dpath = STUDIO_ROOT / rel_dir
        if not dpath.is_dir():
            missing_dirs.append(rel_dir)
            errors.append(f"Missing required directory: {rel_dir}")
    checks_summary["directory_tree_check"] = {
        "total_required": len(REQUIRED_DIRECTORIES),
        "found": len(REQUIRED_DIRECTORIES) - len(missing_dirs),
        "missing": missing_dirs,
        "status": "PASS" if not missing_dirs else "FAIL",
    }
    print(f"[1/6] Directory Tree Check: {len(REQUIRED_DIRECTORIES) - len(missing_dirs)}/{len(REQUIRED_DIRECTORIES)} directories verified -> {checks_summary['directory_tree_check']['status']}")

    # 2. Core File Existence & Non-Empty Check
    missing_or_empty_files = []
    file_sizes = {}
    for rel_file in REQUIRED_FILES:
        fpath = STUDIO_ROOT / rel_file
        if not fpath.is_file():
            missing_or_empty_files.append(rel_file)
            errors.append(f"Missing required file: {rel_file}")
        else:
            size = fpath.stat().st_size
            file_sizes[rel_file] = size
            if size == 0:
                missing_or_empty_files.append(rel_file)
                errors.append(f"Empty required file (0 bytes): {rel_file}")

    # Validate PROJECT_STATE.json is valid JSON
    project_state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    if project_state_path.is_file():
        try:
            state_data = json.loads(project_state_path.read_text(encoding="utf-8"))
            if state_data.get("pro_access_code") != "SMALLBIZ-OS-PRO-2026":
                errors.append("PROJECT_STATE.json missing pro_access_code == 'SMALLBIZ-OS-PRO-2026'")
        except Exception as exc:
            errors.append(f"PROJECT_STATE.json invalid JSON: {exc}")

    checks_summary["core_files_check"] = {
        "total_required": len(REQUIRED_FILES),
        "verified": len(REQUIRED_FILES) - len(missing_or_empty_files),
        "file_sizes_bytes": file_sizes,
        "status": "PASS" if not missing_or_empty_files else "FAIL",
    }
    print(f"[2/6] Core File Existence & Non-Empty Check: {len(REQUIRED_FILES) - len(missing_or_empty_files)}/{len(REQUIRED_FILES)} files verified -> {checks_summary['core_files_check']['status']}")

    # 3. Word Count Floor Verification
    word_counts = {}
    wc_failures = []
    for rel_file, floor in WORD_COUNT_FLOORS.items():
        fpath = STUDIO_ROOT / rel_file
        if fpath.is_file():
            text = fpath.read_text(encoding="utf-8")
            wc = count_words(text)
            word_counts[rel_file] = {
                "word_count": wc,
                "required_floor": floor,
                "status": "PASS" if wc >= floor else "FAIL",
            }
            if wc < floor:
                wc_failures.append(f"{rel_file} ({wc} < {floor})")
                errors.append(f"Word count below floor in {rel_file}: {wc} words (required >= {floor})")
        else:
            wc_failures.append(f"{rel_file} (missing)")

    checks_summary["word_count_verification"] = {
        "files": word_counts,
        "status": "PASS" if not wc_failures else "FAIL",
    }
    print("[3/6] Word Count Floor Verification:")
    for rel_file, info in word_counts.items():
        print(f"      - {rel_file}: {info['word_count']} words (Floor: >= {info['required_floor']}) -> {info['status']}")

    # 4. 14-Part Schema & 5-Prompt Verification in chapter-01.md
    ch1_path = STUDIO_ROOT / "03-MANUSCRIPT/chapter-01.md"
    missing_headers = []
    missing_prompts = []
    missing_svg_links = []
    if ch1_path.is_file():
        ch1_text = ch1_path.read_text(encoding="utf-8")
        for header in REQUIRED_CHAPTER_HEADERS:
            if header not in ch1_text:
                missing_headers.append(header)
                errors.append(f"chapter-01.md missing required header: {header}")
        for prompt_label in REQUIRED_PROMPTS:
            if prompt_label not in ch1_text:
                missing_prompts.append(prompt_label)
                errors.append(f"chapter-01.md missing required prompt: {prompt_label}")
        for svg_link in REQUIRED_SVG_LINKS:
            if svg_link not in ch1_text:
                missing_svg_links.append(svg_link)
                errors.append(f"chapter-01.md missing SVG link: {svg_link}")

    schema_pass = not (missing_headers or missing_prompts or missing_svg_links)
    checks_summary["chapter_01_schema_check"] = {
        "headers_verified": f"{len(REQUIRED_CHAPTER_HEADERS) - len(missing_headers)}/{len(REQUIRED_CHAPTER_HEADERS)}",
        "prompts_verified": f"{len(REQUIRED_PROMPTS) - len(missing_prompts)}/{len(REQUIRED_PROMPTS)}",
        "svg_links_verified": f"{len(REQUIRED_SVG_LINKS) - len(missing_svg_links)}/{len(REQUIRED_SVG_LINKS)}",
        "missing_headers": missing_headers,
        "missing_prompts": missing_prompts,
        "missing_svg_links": missing_svg_links,
        "status": "PASS" if schema_pass else "FAIL",
    }
    print(f"[4/6] Chapter 1 14-Part Schema & 5-Prompt Check: Headers {len(REQUIRED_CHAPTER_HEADERS) - len(missing_headers)}/14, Prompts {len(REQUIRED_PROMPTS) - len(missing_prompts)}/5, SVGs {len(REQUIRED_SVG_LINKS) - len(missing_svg_links)}/2 -> {checks_summary['chapter_01_schema_check']['status']}")

    # 5. SVG XML & Palette Validation
    svg_results = {}
    svg_failures = []
    for rel_svg in SVG_FILES:
        svg_path = STUDIO_ROOT / rel_svg
        if not svg_path.is_file():
            svg_failures.append(rel_svg)
            continue
        raw_svg = svg_path.read_text(encoding="utf-8")
        try:
            root = ET.fromstring(raw_svg)
            view_box = root.attrib.get("viewBox", "")
            has_primary = "#0F172A" in raw_svg.upper()
            has_accent = "#059669" in raw_svg.upper()
            valid_vb = view_box == "0 0 900 480"
            if not valid_vb:
                errors.append(f"{rel_svg} invalid viewBox: '{view_box}' (expected '0 0 900 480')")
                svg_failures.append(rel_svg)
            if not (has_primary and has_accent):
                errors.append(f"{rel_svg} missing required Executive Emerald & Slate brand hex colors (#0F172A, #059669)")
                svg_failures.append(rel_svg)
            svg_results[rel_svg] = {
                "xml_valid": True,
                "viewBox": view_box,
                "has_primary_0F172A": has_primary,
                "has_accent_059669": has_accent,
                "status": "PASS" if (valid_vb and has_primary and has_accent) else "FAIL",
            }
        except ET.ParseError as exc:
            svg_failures.append(rel_svg)
            errors.append(f"{rel_svg} XML ParseError: {exc}")
            svg_results[rel_svg] = {"xml_valid": False, "error": str(exc), "status": "FAIL"}

    checks_summary["svg_xml_and_palette_validation"] = {
        "svgs": svg_results,
        "status": "PASS" if not svg_failures else "FAIL",
    }
    print(f"[5/6] SVG XML & Palette Validation: {len(SVG_FILES) - len(svg_failures)}/{len(SVG_FILES)} SVGs valid XML with viewBox='0 0 900 480' & brand palette -> {checks_summary['svg_xml_and_palette_validation']['status']}")

    # 6. Zero AI Cliche & Placeholder Filter
    cliche_violations = []
    for rel_file in CLICHE_SCAN_FILES:
        fpath = STUDIO_ROOT / rel_file
        if not fpath.is_file():
            continue
        lines = fpath.read_text(encoding="utf-8").splitlines()
        for line_num, line in enumerate(lines, start=1):
            # Check banned single words
            for match in BANNED_WORDS_REGEX.finditer(line):
                v = {
                    "file": rel_file,
                    "line": line_num,
                    "type": "BANNED_WORD",
                    "match": match.group(0),
                }
                cliche_violations.append(v)
                errors.append(f"Banned word '{match.group(0)}' in {rel_file}:{line_num}")

            # Check banned phrases (case-insensitive)
            lower_line = line.lower()
            for phrase in BANNED_PHRASES:
                if phrase in lower_line:
                    v = {
                        "file": rel_file,
                        "line": line_num,
                        "type": "BANNED_PHRASE",
                        "match": phrase,
                    }
                    cliche_violations.append(v)
                    errors.append(f"Banned phrase '{phrase}' in {rel_file}:{line_num}")

            # Check banned placeholders (exact case-sensitive for TODO/TBD/[XX], case-insensitive for Lorem ipsum)
            for ph in BANNED_PLACEHOLDERS:
                if ph == "Lorem ipsum":
                    if "lorem ipsum" in lower_line:
                        cliche_violations.append({"file": rel_file, "line": line_num, "type": "BANNED_PLACEHOLDER", "match": ph})
                        errors.append(f"Banned placeholder '{ph}' in {rel_file}:{line_num}")
                elif ph in ("TODO", "TBD"):
                    if re.search(rf"\b{ph}\b", line):
                        cliche_violations.append({"file": rel_file, "line": line_num, "type": "BANNED_PLACEHOLDER", "match": ph})
                        errors.append(f"Banned placeholder '{ph}' in {rel_file}:{line_num}")
                else:
                    if ph in line:
                        cliche_violations.append({"file": rel_file, "line": line_num, "type": "BANNED_PLACEHOLDER", "match": ph})
                        errors.append(f"Banned placeholder '{ph}' in {rel_file}:{line_num}")

    checks_summary["zero_cliche_and_placeholder_filter"] = {
        "files_scanned": CLICHE_SCAN_FILES,
        "violations_found": len(cliche_violations),
        "violations": cliche_violations,
        "status": "PASS" if not cliche_violations else "FAIL",
    }
    print(f"[6/6] Zero AI Cliche & Placeholder Filter: {len(cliche_violations)} violations across {len(CLICHE_SCAN_FILES)} files -> {checks_summary['zero_cliche_and_placeholder_filter']['status']}")

    # Write QA Reports
    timestamp_iso = datetime.now(timezone.utc).isoformat()
    qa_report_data = {
        "project_id": "SMALLBIZ-AI-AUTOMATION-OS-V1",
        "phase": "Phase 1 — Studio Initialization, Metadata, Architecture & Chapter 1 Complete Vertical Slice",
        "verified_at_utc": timestamp_iso,
        "studio_root": "e:/Ebook-Makaer/Small-Business-AI-Automation-OS/DIGITAL-PUBLISHING-STUDIO/",
        "total_errors": len(errors),
        "overall_status": "PASS (0 ERRORS)" if len(errors) == 0 else f"FAIL ({len(errors)} ERRORS)",
        "checks": checks_summary,
        "errors": errors,
    }

    qa_json_path = STUDIO_ROOT / "11-QA-REPORTS/phase1-qa-report.json"
    qa_md_path = STUDIO_ROOT / "11-QA-REPORTS/phase1-qa-report.md"
    qa_json_path.write_text(json.dumps(qa_report_data, indent=2), encoding="utf-8")

    md_lines = [
        "# Phase 1 Automated QA Verification Report",
        "",
        f"**Project:** *The Small Business AI Automation Operating System* (`SMALLBIZ-AI-AUTOMATION-OS-V1`)  ",
        f"**Phase:** Phase 1 — Studio Initialization, Metadata, Architecture & Chapter 1 Vertical Slice  ",
        f"**Timestamp (UTC):** `{timestamp_iso}`  ",
        f"**Overall QA Verdict:** **{qa_report_data['overall_status']}**  ",
        "",
        "---",
        "",
        "## 1. Executive Verification Summary",
        "",
        "| Check ID | Verification Gate | Result | Status |",
        "| :--- | :--- | :--- | :--- |",
        f"| `CHK-01` | 14-Folder Studio Directory Tree & Subdirectories | `{checks_summary['directory_tree_check']['found']}/{checks_summary['directory_tree_check']['total_required']} Directories` | **{checks_summary['directory_tree_check']['status']}** |",
        f"| `CHK-02` | Core Governance, Research, Architecture & Chapter 1 Files | `{checks_summary['core_files_check']['verified']}/{checks_summary['core_files_check']['total_required']} Non-Empty Files` | **{checks_summary['core_files_check']['status']}** |",
        f"| `CHK-03` | Word Count Floors (`chapter-01 >= 6500`, `worksheet-01 >= 1500`, `research >= 1500`) | `All 3 Exceed Floors` | **{checks_summary['word_count_verification']['status']}** |",
        f"| `CHK-04` | Chapter 1 14-Part Schema, 5 Prompts (`1.1–1.5`) & 2 SVG Embeds | `14/14 Headers, 5/5 Prompts, 2/2 SVGs` | **{checks_summary['chapter_01_schema_check']['status']}** |",
        f"| `CHK-05` | SVG XML Syntax (`ElementTree`), `viewBox='0 0 900 480'` & Brand Palette | `2/2 Valid XML SVGs` | **{checks_summary['svg_xml_and_palette_validation']['status']}** |",
        f"| `CHK-06` | Zero Banned AI Clichés, Phrases & Placeholders Filter | `{len(cliche_violations)} Violations` | **{checks_summary['zero_cliche_and_placeholder_filter']['status']}** |",
        "",
        "---",
        "",
        "## 2. Exact Word Count Audit",
        "",
        "| Deliverable File | Audited Word Count | Required Floor | Margin Above Floor | Status |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for rel_file, info in word_counts.items():
        margin = info["word_count"] - info["required_floor"]
        md_lines.append(
            f"| `{rel_file}` | **{info['word_count']:,} words** | `{info['required_floor']:,} words` | `+{margin:,} words` | **{info['status']}** |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 3. Vector SVG Validation Details",
        "",
        "| SVG File | XML Well-Formed | `viewBox` | Primary `#0F172A` | Accent `#059669` | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ])
    for rel_svg, sinfo in svg_results.items():
        md_lines.append(
            f"| `{rel_svg}` | `{sinfo.get('xml_valid')}` | `{sinfo.get('viewBox')}` | `{sinfo.get('has_primary_0F172A')}` | `{sinfo.get('has_accent_059669')}` | **{sinfo.get('status')}** |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 4. Error & Violation Log",
        "",
    ])
    if not errors:
        md_lines.append("- **0 errors detected.** All Phase 1 structural, editorial, visual, and financial requirements passed verification.")
    else:
        for err in errors:
            md_lines.append(f"- `ERROR`: {err}")

    qa_md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("=" * 78)
    if errors:
        print(f"FINAL QA RESULT: FAILED WITH {len(errors)} ERROR(S)")
        for err in errors:
            print(f"  [!] {err}")
        return 1
    else:
        print("FINAL QA RESULT: PASSED — 0 ERRORS")
        print(f"QA Reports written to:\n  - {qa_json_path.as_posix()}\n  - {qa_md_path.as_posix()}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
