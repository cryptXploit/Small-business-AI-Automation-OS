#!/usr/bin/env python3
"""
verify_phase5.py — Automated Enterprise QA Verifier for Phase 5
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)
Phase 5: Single-Source Multi-Format Book, EPUB 3.0 & Fillable AcroForm Workbook Compiler
"""

import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import pypdf

STUDIO_ROOT = Path(__file__).resolve().parent

PDF_DELIVERABLES = {
    "09-EXPORTS/PDF/the-smallbiz-ai-automation-os-complete-book.pdf": {
        "min_kb": 500,
        "min_pages": 120,
        "expected_w_pt": 612.0,
        "expected_h_pt": 792.0,
        "require_acroform": False,
    },
    "09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf": {
        "min_kb": 500,
        "min_pages": 180,
        "expected_w_pt": 432.0,
        "expected_h_pt": 648.0,
        "require_acroform": False,
    },
    "09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-us-letter.pdf": {
        "min_kb": 200,
        "min_pages": 25,
        "expected_w_pt": 612.0,
        "expected_h_pt": 792.0,
        "require_acroform": True,
    },
    "09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-a4.pdf": {
        "min_kb": 200,
        "min_pages": 25,
        "expected_w_pt": 595.0,
        "expected_h_pt": 842.0,
        "require_acroform": True,
    },
    "09-EXPORTS/PDF/the-smallbiz-ai-automation-os-tablet-planner.pdf": {
        "min_kb": 200,
        "min_pages": 20,
        "expected_w_pt": 792.0,
        "expected_h_pt": 612.0,
        "require_acroform": True,
    },
    "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf": {
        "min_kb": 150,
        "min_pages": 20,
        "expected_w_pt": 612.0,
        "expected_h_pt": 792.0,
        "require_acroform": False,
    },
    "05-WORKBOOKS/chapter-01-workbook.pdf": {
        "min_kb": 80,
        "min_pages": 4,
        "expected_w_pt": 612.0,
        "expected_h_pt": 792.0,
        "require_acroform": True,
    },
    "09-EXPORTS/PDF/chapter-01-workbook.pdf": {
        "min_kb": 80,
        "min_pages": 4,
        "expected_w_pt": 612.0,
        "expected_h_pt": 792.0,
        "require_acroform": True,
    },
}

EPUB_REL_PATH = "09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub"
EPUB_MIN_KB = 150

BANNED_WORDS_REGEX = [
    r"\bdelve\b", r"\btapestry\b", r"\btestament\b", r"\bbeacon\b",
    r"\bsymphony\b", r"\bunlock\b", r"\bunleash\b", r"\bskyrocket\b",
    r"\bsupercharge\b", r"\bgame-changer\b", r"\bpivotal\b", r"\brealm\b",
    r"\bfoster\b", r"\bunderscore\b", r"\butilize\b", r"\bleverage\b"
]

BANNED_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further"
]

BANNED_PLACEHOLDERS = [
    r"\bTODO\b", r"\bTBD\b", r"Lorem ipsum", r"\[\s*XX\s*\]"
]


def main():
    errors = []
    deliverable_metrics = {}

    # 1. Verify build.py syntax
    build_py = STUDIO_ROOT / "build.py"
    if not build_py.exists():
        errors.append("Missing required compiler script: build.py")
    else:
        try:
            compile(build_py.read_text(encoding="utf-8"), "build.py", "exec")
        except SyntaxError as e:
            errors.append(f"Syntax error in build.py: {e}")

    # 2. Verify all PDF deliverables
    kdp_page_count = 0
    for rel_path, spec in PDF_DELIVERABLES.items():
        full_path = STUDIO_ROOT / rel_path
        if not full_path.exists():
            errors.append(f"Missing required PDF deliverable: {rel_path}")
            continue

        size_bytes = full_path.stat().st_size
        size_kb = round(size_bytes / 1024.0, 2)
        if size_kb < spec["min_kb"]:
            errors.append(
                f"File size below floor for {rel_path}: {size_kb} KB < {spec['min_kb']} KB"
            )

        try:
            reader = pypdf.PdfReader(str(full_path))
            num_pages = len(reader.pages)
            if "kdp-paperback-6x9.pdf" in rel_path:
                kdp_page_count = num_pages

            if num_pages < spec["min_pages"]:
                errors.append(
                    f"Page count below floor for {rel_path}: {num_pages} < {spec['min_pages']}"
                )

            # Check page 0 dimensions
            mb = reader.pages[0].mediabox
            w_pt = float(mb.width)
            h_pt = float(mb.height)
            if abs(w_pt - spec["expected_w_pt"]) > 3.0 or abs(h_pt - spec["expected_h_pt"]) > 3.0:
                errors.append(
                    f"Page dimension mismatch in {rel_path}: got {w_pt:.1f}x{h_pt:.1f} pt, expected {spec['expected_w_pt']}x{spec['expected_h_pt']} pt"
                )

            # Check non-empty content streams
            empty_pages = 0
            for p_idx, page in enumerate(reader.pages):
                if page.get_contents() is None:
                    empty_pages += 1
            if empty_pages > 0:
                errors.append(f"{rel_path} has {empty_pages} pages with empty content streams")

            # Check AcroForm fields
            fields = reader.get_fields() or {}
            acroform_count = len(fields)
            has_acroform_dict = "/AcroForm" in reader.trailer["/Root"]
            if spec["require_acroform"] and (not has_acroform_dict or acroform_count == 0):
                errors.append(
                    f"{rel_path} missing required interactive /AcroForm fields (found {acroform_count})"
                )

            deliverable_metrics[rel_path] = {
                "type": "PDF",
                "bytes": size_bytes,
                "size_kb": size_kb,
                "pages": num_pages,
                "dimensions_pt": f"{w_pt:.1f} x {h_pt:.1f}",
                "acroform_fields": acroform_count,
            }
        except Exception as e:
            errors.append(f"Failed to parse PDF {rel_path} with pypdf: {e}")

    # 3. Verify EPUB 3.0 archive & XML/XHTML validity
    epub_full = STUDIO_ROOT / EPUB_REL_PATH
    epub_summary = {}
    if not epub_full.exists():
        errors.append(f"Missing required EPUB 3.0 deliverable: {EPUB_REL_PATH}")
    else:
        e_bytes = epub_full.stat().st_size
        e_kb = round(e_bytes / 1024.0, 2)
        if e_kb < EPUB_MIN_KB:
            errors.append(f"EPUB size below floor: {e_kb} KB < {EPUB_MIN_KB} KB")

        try:
            with zipfile.ZipFile(str(epub_full), "r") as zf:
                infolist = zf.infolist()
                namelist = zf.namelist()
                if not infolist or infolist[0].filename != "mimetype":
                    errors.append("EPUB entry 0 is not 'mimetype'")
                else:
                    if infolist[0].compress_type != zipfile.ZIP_STORED:
                        errors.append("EPUB 'mimetype' is not stored uncompressed (ZIP_STORED)")
                    if zf.read("mimetype") != b"application/epub+zip":
                        errors.append("EPUB 'mimetype' content does not equal 'application/epub+zip'")

                required_epub_entries = [
                    "META-INF/container.xml",
                    "OEBPS/content.opf",
                    "OEBPS/nav.xhtml",
                    "OEBPS/toc.ncx",
                    "OEBPS/styles.css",
                    "OEBPS/front-matter.xhtml",
                    "OEBPS/back-matter.xhtml",
                ]
                for i in range(1, 11):
                    required_epub_entries.append(f"OEBPS/chapter-{i:02d}.xhtml")
                    required_epub_entries.append(f"OEBPS/images/chapter-{i:02d}-mindmap.svg")
                    required_epub_entries.append(f"OEBPS/images/chapter-{i:02d}-flowchart.svg")

                for req_entry in required_epub_entries:
                    if req_entry not in namelist:
                        errors.append(f"EPUB missing required internal file: {req_entry}")

                xml_parsed_count = 0
                for entry_name in namelist:
                    if entry_name.endswith((".xml", ".opf", ".ncx", ".xhtml", ".svg")):
                        raw_data = zf.read(entry_name)
                        try:
                            ET.fromstring(raw_data)
                            xml_parsed_count += 1
                        except Exception as xml_err:
                            errors.append(f"EPUB XML/XHTML parse error in {entry_name}: {xml_err}")

                    if entry_name.endswith(".xhtml") and "nav.xhtml" not in entry_name:
                        text_str = zf.read(entry_name).decode("utf-8")
                        for pat in BANNED_WORDS_REGEX:
                            if re.search(pat, text_str, flags=re.IGNORECASE):
                                errors.append(f"Banned word '{pat}' found inside EPUB {entry_name}")
                        lower_str = text_str.lower()
                        for phrase in BANNED_PHRASES:
                            if phrase in lower_str:
                                errors.append(f"Banned phrase '{phrase}' found inside EPUB {entry_name}")
                        for ph in BANNED_PLACEHOLDERS:
                            if re.search(ph, text_str):
                                errors.append(f"Banned placeholder '{ph}' found inside EPUB {entry_name}")

                epub_summary = {
                    "type": "EPUB 3.0",
                    "bytes": e_bytes,
                    "size_kb": e_kb,
                    "total_zip_entries": len(namelist),
                    "xml_xhtml_svg_files_validated": xml_parsed_count,
                    "mimetype_uncompressed_first": True,
                }
                deliverable_metrics[EPUB_REL_PATH] = epub_summary
        except Exception as e:
            errors.append(f"Failed to inspect EPUB archive {EPUB_REL_PATH}: {e}")

    # 4. Update PROJECT_STATE.json if 0 errors
    state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    if state_path.exists() and len(errors) == 0:
        state_data = json.loads(state_path.read_text(encoding="utf-8"))
        state_data["status"] = "PHASE_5_COMPLETE"
        state_data["phases_completed"] = [1, 2, 3, 4, 5]
        state_data["kdp_paperback_page_count"] = kdp_page_count
        state_data["phases"]["Phase 5"] = {
            "title": "Single-Source Multi-Format Book, EPUB 3.0 & Fillable AcroForm Workbook Compiler",
            "status": "COMPLETED",
            "verified": True,
            "qa_errors": 0,
            "verified_at_utc": datetime.now(timezone.utc).isoformat(),
            "kdp_paperback_page_count": kdp_page_count,
            "deliverables": list(PDF_DELIVERABLES.keys()) + [EPUB_REL_PATH, "build.py", "verify_phase5.py"],
        }
        state_data["cumulative_metrics_phase5"] = deliverable_metrics
        state_path.write_text(json.dumps(state_data, indent=2), encoding="utf-8")

    # 5. Write Phase 5 QA Reports
    report = {
        "phase": 5,
        "status": "PASSED" if len(errors) == 0 else "FAILED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_count": len(errors),
        "errors": errors,
        "kdp_paperback_page_count": kdp_page_count,
        "deliverables": deliverable_metrics,
    }
    qa_dir = STUDIO_ROOT / "11-QA-REPORTS"
    qa_dir.mkdir(parents=True, exist_ok=True)
    (qa_dir / "phase5-qa-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# Phase 5 QA Verification Report — Multi-Format PDF, KDP 6x9, EPUB 3.0 & Fillable AcroForm Suite",
        f"- **Execution Status:** `{report['status']}`",
        f"- **Timestamp:** `{report['timestamp']}`",
        f"- **Total QA Errors:** `{report['error_count']}`",
        f"- **Recorded KDP 6\"×9\" Paperback Page Count:** `{kdp_page_count}` pages",
        "",
        "## Compiled Production Deliverables",
        "| Deliverable Path | Format | Size (KB) | Pages / Entries | Dimensions (pt) | AcroForm Fields |",
        "| :--- | :--- | ---: | ---: | :--- | ---: |",
    ]
    for rel_p, m in deliverable_metrics.items():
        if m["type"] == "PDF":
            md_lines.append(
                f"| `{rel_p}` | PDF | {m['size_kb']:,.2f} KB | {m['pages']} pages | `{m['dimensions_pt']}` | {m['acroform_fields']} |"
            )
        else:
            md_lines.append(
                f"| `{rel_p}` | EPUB 3.0 | {m['size_kb']:,.2f} KB | {m['total_zip_entries']} entries ({m['xml_xhtml_svg_files_validated']} XML validated) | Reflowable | N/A |"
            )

    if errors:
        md_lines.append("\n## Errors Detected")
        for err in errors:
            md_lines.append(f"- ❌ {err}")
    else:
        md_lines.append(
            "\n## QA Certification\n- ✅ All 8 PDF and EPUB 3.0 production deliverables passed geometry, page-count, AcroForm, XML/XHTML well-formedness, and anti-cliché verification with 0 errors."
        )

    (qa_dir / "phase5-qa-report.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
