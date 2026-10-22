#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 8 Automated QA Verification Suite (verify_phase8_master.py)
Project: The Small Business AI Automation Operating System
Verifies:
  1. 10-MARKETING/index.html (>= 60 KB, 0 external HTTP dependencies, interactive ROI calculator, 5 tiers, Headless Edge DOM check)
  2. 10-MARKETING/marketplace-listings-and-bd-launch-runbook.md (>= 3,000 words, W-8BEN, Article 12, 10%, Payoneer, Amazon KDP, Draft2Digital, Gumroad)
  3. 10-MARKETING/email-funnel-and-upsell-sequence.md (>= 3,000 words, Email 01..Email 07)
  4. 10-MARKETING/tier4-monthly-vault-drop-01.md (>= 2,500 words, 4 industry verticals, 8 specialized prompts)
  5. 09-EXPORTS/HYBRID-BUNDLE/*.zip (5 commercial ZIP bundles, testzip() is None, non-empty member files, required manifest files)
  6. Zero banned words, banned phrases, or placeholders across all Phase 8 files
  7. Updates PROJECT_STATE.json and writes 11-QA-REPORTS/phase8-qa-report.json & .md
"""

import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent
MARKETING_DIR = STUDIO_ROOT / "10-MARKETING"
BUNDLE_DIR = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE"
QA_DIR = STUDIO_ROOT / "11-QA-REPORTS"
STATE_PATH = STUDIO_ROOT / "PROJECT_STATE.json"

BANNED_WORDS = [
    "delve", "tapestry", "testament", "beacon", "symphony", "unlock",
    "unleash", "elevate", "supercharge", "game-changer", "game changer",
    "paradigm", "cutting-edge", "skyrocket", "seamless", "seamlessly",
    "holistic", "synergy", "revolutionary", "groundbreaking", "transformative",
    "empower", "harness", "foster", "spearhead", "pivotal", "underscore",
    "realm", "landscape"
]

BANNED_PHRASES = [
    "in today's fast-paced world",
    "in the ever-evolving landscape",
    "whether you're a seasoned pro or just starting out",
    "it's not just about",
    "at the end of the day",
    "without further ado",
    "let's dive in",
    "buckle up"
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"Lorem ipsum",
    r"\[XX\]"
]


def find_browser_executable() -> str:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    raise FileNotFoundError("Neither Microsoft Edge nor Google Chrome was found on this system.")


def count_document_words(md_text: str) -> int:
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", md_text, flags=re.DOTALL)
    words = re.findall(r"\b[\w'-]+\b", text)
    return len(words)


def scan_lexical_violations(text: str) -> list:
    violations = []
    lower_text = text.lower()
    for bw in BANNED_WORDS:
        pattern = r"\b" + re.escape(bw) + r"(?:s|ed|ing|er)?\b"
        matches = re.findall(pattern, lower_text)
        if matches:
            violations.append(f"Banned word '{bw}' found ({len(matches)}x)")
    for bp in BANNED_PHRASES:
        if bp in lower_text:
            violations.append(f"Banned phrase '{bp}' found")
    for pat in PLACEHOLDER_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            violations.append(f"Placeholder pattern '{pat}' found ({len(matches)}x)")
    return violations


def main() -> int:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    errors = []
    report = {
        "phase": 8,
        "title": "Conversion Marketing Funnel, 7-Email Sequence, Bangladesh W-8BEN/Payoneer Runbook, Tier 4 Vault Drop #01 & Initial 5-Tier ZIP Packaging",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sales_page": {},
        "markdown_assets": {},
        "zip_bundles": {},
        "lexical_audit": {},
        "errors": [],
        "total_errors": 0,
        "status": "PENDING"
    }

    # 1. Verify 10-MARKETING/index.html
    index_path = MARKETING_DIR / "index.html"
    if not index_path.is_file():
        errors.append("Missing 10-MARKETING/index.html")
    else:
        html_text = index_path.read_text(encoding="utf-8")
        size_bytes = index_path.stat().st_size
        size_kb = round(size_bytes / 1024.0, 2)

        ext_scripts = re.findall(r'<script[^>]+src=["\']https?://', html_text, flags=re.IGNORECASE)
        ext_links = re.findall(r'<link[^>]+href=["\']https?://', html_text, flags=re.IGNORECASE)
        ext_imgs = re.findall(r'<img[^>]+src=["\']https?://', html_text, flags=re.IGNORECASE)
        ext_imports = re.findall(r'@import\s+url\(["\']?https?://', html_text, flags=re.IGNORECASE)
        total_ext = len(ext_scripts) + len(ext_links) + len(ext_imgs) + len(ext_imports)

        has_roi = "updateMarketingRoi" in html_text and "setMarketingPreset" in html_text
        required_tiers = ["Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4"]
        missing_tiers = [t for t in required_tiers if t.lower() not in html_text.lower()]

        # Headless Edge DOM validation
        dom_ok = False
        dom_len = 0
        try:
            browser_exe = find_browser_executable()
            cmd = [
                browser_exe,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--dump-dom",
                index_path.resolve().as_uri()
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45)
            dom_out = proc.stdout or ""
            dom_len = len(dom_out)
            if proc.returncode == 0 and "Small Business AI Automation" in dom_out and "updateMarketingRoi" in dom_out:
                dom_ok = True
            else:
                errors.append(f"Headless Edge --dump-dom check failed for index.html (rc={proc.returncode}, len={dom_len})")
        except Exception as exc:
            errors.append(f"Headless Edge execution error on index.html: {exc}")

        if size_bytes < 61440:
            errors.append(f"10-MARKETING/index.html size {size_kb} KB ({size_bytes} bytes) is below 60 KB (61,440 bytes) floor")
        if total_ext > 0:
            errors.append(f"10-MARKETING/index.html contains {total_ext} external HTTP/HTTPS resource links")
        if not has_roi:
            errors.append("10-MARKETING/index.html missing interactive ROI calculator functions")
        if missing_tiers:
            errors.append(f"10-MARKETING/index.html missing pricing tiers: {missing_tiers}")

        lex_html = scan_lexical_violations(html_text)
        report["lexical_audit"]["10-MARKETING/index.html"] = lex_html
        for v in lex_html:
            errors.append(f"10-MARKETING/index.html lexical violation: {v}")

        report["sales_page"] = {
            "path": "10-MARKETING/index.html",
            "size_bytes": size_bytes,
            "size_kb": size_kb,
            "external_http_dependencies": total_ext,
            "has_interactive_roi_calculator": has_roi,
            "tiers_present": len(required_tiers) - len(missing_tiers),
            "headless_dom_verified": dom_ok,
            "headless_dom_length": dom_len
        }

    # 2. Verify Markdown Marketing & Vault Assets
    md_specs = [
        (
            "marketplace-listings-and-bd-launch-runbook.md",
            3000,
            ["W-8BEN", "Article 12", "10%", "Payoneer", "Amazon KDP", "Draft2Digital", "Gumroad"]
        ),
        (
            "email-funnel-and-upsell-sequence.md",
            3000,
            ["Email 01", "Email 02", "Email 03", "Email 04", "Email 05", "Email 06", "Email 07"]
        ),
        (
            "tier4-monthly-vault-drop-01.md",
            2500,
            [
                "Vertical 1: Local Medical, Dental, Physical Therapy & Wellness Clinics",
                "Vertical 2: HVAC, Plumbing, Electrical, Roofing & Home Service Contractors",
                "Vertical 3: Omni-Channel E-Commerce, Specialty Retail & D2C Brands",
                "Vertical 4: B2B Agencies, CPA/Accounting Firms, Legal Practices & Consultancies",
                "Vault Prompt V1.1",
                "Vault Prompt V1.2",
                "Vault Prompt V2.1",
                "Vault Prompt V2.2",
                "Vault Prompt V3.1",
                "Vault Prompt V3.2",
                "Vault Prompt V4.1",
                "Vault Prompt V4.2"
            ]
        )
    ]

    for fname, min_words, req_tokens in md_specs:
        fpath = MARKETING_DIR / fname
        if not fpath.is_file():
            errors.append(f"Missing 10-MARKETING/{fname}")
            continue
        raw = fpath.read_text(encoding="utf-8")
        wc = count_document_words(raw)
        missing_toks = [t for t in req_tokens if t not in raw]
        lex_v = scan_lexical_violations(raw)
        report["lexical_audit"][f"10-MARKETING/{fname}"] = lex_v

        if wc < min_words:
            errors.append(f"10-MARKETING/{fname} word count {wc} < {min_words} required")
        if missing_toks:
            errors.append(f"10-MARKETING/{fname} missing required tokens: {missing_toks}")
        for v in lex_v:
            errors.append(f"10-MARKETING/{fname} lexical violation: {v}")

        report["markdown_assets"][fname] = {
            "word_count": wc,
            "min_words_required": min_words,
            "required_tokens_found": len(req_tokens) - len(missing_toks),
            "required_tokens_total": len(req_tokens),
            "lexical_violations": len(lex_v)
        }

    # 3. Verify 5 Commercial ZIP Bundles in 09-EXPORTS/HYBRID-BUNDLE/
    expected_zips = {
        "Tier0-Free-5Day-Audit-Starter-Kit.zip": [
            "README-BUNDLE-INVENTORY.txt",
            "01-Book-Sample-and-Audit/tier0-free-sample-chapter01-and-audit.pdf",
            "01-Book-Sample-and-Audit/chapter-01-workbook.pdf",
            "02-Interactive-ROI-Web-App/smallbiz-automation-os-app.html",
            "03-Spreadsheet-Calculator/sheet1-automation-roi-and-leak-calculator.csv",
            "05-Cover/gumroad-tier0-free-audit-cover.png"
        ],
        "Tier1-KDP-and-D2D-Retail-Book-Pack.zip": [
            "README-BUNDLE-INVENTORY.txt",
            "01-Kindle-and-D2D-EPUB3/the-smallbiz-ai-automation-os.epub",
            "02-KDP-Print-6x9-Interior/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf",
            "03-Retail-Covers/ebook-cover-kdp-kindle.png",
            "03-Retail-Covers/kdp-paperback-full-wrap-cover.pdf",
            "04-Publishing-Runbooks/marketplace-listings-and-bd-launch-runbook.md"
        ],
        "Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip": [
            "README-BUNDLE-INVENTORY.txt",
            "01-Master-Book/the-smallbiz-ai-automation-os-complete-book.pdf",
            "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-us-letter.pdf",
            "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-a4.pdf",
            "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-tablet-planner.pdf",
            "03-Prompt-and-SOP-Vault/62-Item-Prompt-and-SOP-Vault.csv"
        ],
        "Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip": [
            "README-BUNDLE-INVENTORY.txt",
            "01-Master-Book/the-smallbiz-ai-automation-os-complete-book.pdf",
            "07-Pro-Web-Companion-App/smallbiz-automation-os-app.html",
            "07-Pro-Web-Companion-App/PRO-ACCESS-LICENSE-KEY.txt",
            "08-Notion-OS-5-Database-Kit/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv",
            "08-Notion-OS-5-Database-Kit/02-Automation-Workflows-and-Health-Registry.csv",
            "08-Notion-OS-5-Database-Kit/03-AI-Prompt-and-SOP-Vault-62.csv",
            "08-Notion-OS-5-Database-Kit/04-Weekly-Owner-KPI-Scorecard.csv",
            "08-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.csv",
            "08-Notion-OS-5-Database-Kit/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"
        ],
        "Tier4-Living-Automation-Vault-Membership-Drop01.zip": [
            "README-BUNDLE-INVENTORY.txt",
            "01-Master-Book/the-smallbiz-ai-automation-os-complete-book.pdf",
            "07-Pro-Web-Companion-App/smallbiz-automation-os-app.html",
            "09-Living-Vault-Drops/tier4-monthly-vault-drop-01.md",
            "10-Commercial-Funnel-Suite/index.html",
            "10-Commercial-Funnel-Suite/email-funnel-and-upsell-sequence.md",
            "10-Commercial-Funnel-Suite/marketplace-listings-and-bd-launch-runbook.md"
        ]
    }

    for zip_name, req_members in expected_zips.items():
        zpath = BUNDLE_DIR / zip_name
        if not zpath.is_file():
            errors.append(f"Missing ZIP bundle: 09-EXPORTS/HYBRID-BUNDLE/{zip_name}")
            continue
        zsize = zpath.stat().st_size
        try:
            with zipfile.ZipFile(zpath, "r") as zf:
                bad_file = zf.testzip()
                if bad_file is not None:
                    errors.append(f"{zip_name} failed CRC testzip() on member: {bad_file}")
                names = zf.namelist()
                infos = zf.infolist()
                zero_byte_members = [i.filename for i in infos if i.file_size == 0]
                if zero_byte_members:
                    errors.append(f"{zip_name} contains 0-byte member files: {zero_byte_members}")
                missing_members = [m for m in req_members if m not in names]
                if missing_members:
                    errors.append(f"{zip_name} missing required manifest files: {missing_members}")

                report["zip_bundles"][zip_name] = {
                    "size_bytes": zsize,
                    "size_mb": round(zsize / (1024 * 1024), 2),
                    "file_count": len(names),
                    "crc_valid": bad_file is None,
                    "zero_byte_members": len(zero_byte_members),
                    "missing_manifest_members": len(missing_members)
                }
        except Exception as exc:
            errors.append(f"Failed to inspect {zip_name}: {exc}")

    report["errors"] = errors
    report["total_errors"] = len(errors)
    report["status"] = "PASS" if len(errors) == 0 else "FAIL"

    # Write JSON report
    json_report_path = QA_DIR / "phase8-qa-report.json"
    json_report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Write Markdown report
    sp = report.get("sales_page", {})
    md_lines = [
        "# Phase 8 QA Verification Report — Conversion Marketing Funnel, Bangladesh W-8BEN Runbook & 5-Tier ZIP Packaging",
        "",
        f"- **Timestamp:** `{report['timestamp']}`",
        f"- **Status:** `{report['status']}`",
        f"- **Total Errors:** `{report['total_errors']}`",
        "",
        "## 1. Offline Conversion Sales Page (`10-MARKETING/index.html`)",
        f"- **File Size:** `{sp.get('size_kb', 0)} KB` (`{sp.get('size_bytes', 0):,}` bytes)",
        f"- **External HTTP/HTTPS Dependencies:** `{sp.get('external_http_dependencies', -1)}`",
        f"- **Interactive ROI Calculator Verified:** `{sp.get('has_interactive_roi_calculator', False)}`",
        f"- **Pricing Tiers Verified:** `{sp.get('tiers_present', 0)} / 5`",
        f"- **Headless Edge `--dump-dom` Verified:** `{sp.get('headless_dom_verified', False)}` (`{sp.get('headless_dom_length', 0):,}` chars)",
        "",
        "## 2. Marketing, Bangladesh W-8BEN/Payoneer & Tier 4 Vault Markdown Assets",
        "| File | Total Words | Required Minimum | Required Tokens | Lexical Violations |",
        "|---|---:|---:|---:|---:|"
    ]
    for fname, stats in report["markdown_assets"].items():
        md_lines.append(
            f"| `{fname}` | {stats['word_count']:,} | {stats['min_words_required']:,} | {stats['required_tokens_found']}/{stats['required_tokens_total']} | {stats['lexical_violations']} |"
        )

    md_lines.extend([
        "",
        "## 3. Commercial 5-Tier `.zip` Bundles (`09-EXPORTS/HYBRID-BUNDLE/`)",
        "| ZIP Bundle | Size (MB) | Member Files | CRC `testzip()` | Zero-Byte Files |",
        "|---|---:|---:|---|---|"
    ])
    for zname, zstats in report["zip_bundles"].items():
        md_lines.append(
            f"| `{zname}` | {zstats['size_mb']:.2f} MB (`{zstats['size_bytes']:,}` B) | {zstats['file_count']} | `{'PASS' if zstats['crc_valid'] else 'FAIL'}` | {zstats['zero_byte_members']} |"
        )

    if errors:
        md_lines.extend(["", "## 4. Errors Detected"])
        for e in errors:
            md_lines.append(f"- ❌ {e}")
    else:
        md_lines.extend(["", "## 4. Verification Summary", "- ✅ Zero errors across all Phase 8 deliverables."])

    md_report_path = QA_DIR / "phase8-qa-report.md"
    md_report_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    # Update PROJECT_STATE.json if 0 errors
    if len(errors) == 0 and STATE_PATH.is_file():
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        state["status"] = "PHASE_8_COMPLETE"
        if "phases_completed" in state and 8 not in state["phases_completed"]:
            state["phases_completed"].append(8)
        if "phases" in state:
            state["phases"]["Phase 8"] = {
                "title": "Conversion Marketing Funnel, 7-Email Sequence, Bangladesh W-8BEN/Payoneer Runbook, Tier 4 Vault Drop #01 & Initial 5-Tier ZIP Packaging",
                "status": "COMPLETED",
                "verified": True,
                "qa_errors": 0,
                "verified_at_utc": report["timestamp"],
                "deliverables": [
                    "10-MARKETING/index.html",
                    "10-MARKETING/marketplace-listings-and-bd-launch-runbook.md",
                    "10-MARKETING/email-funnel-and-upsell-sequence.md",
                    "10-MARKETING/tier4-monthly-vault-drop-01.md",
                    "09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip",
                    "09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Retail-Book-Pack.zip",
                    "09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip",
                    "09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip",
                    "09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Automation-Vault-Membership-Drop01.zip",
                    "11-QA-REPORTS/phase8-qa-report.json",
                    "11-QA-REPORTS/phase8-qa-report.md",
                    "build_phase8.py",
                    "verify_phase8_master.py"
                ]
            }
        state["cumulative_metrics_phase8"] = {
            "sales_page": sp,
            "markdown_assets": report["markdown_assets"],
            "zip_bundles": report["zip_bundles"]
        }
        STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print("=" * 72)
    print(f"PHASE 8 QA VERIFICATION STATUS: {report['status']} (Total Errors: {len(errors)})")
    print("=" * 72)
    if errors:
        for e in errors:
            print(f" [ERROR] {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
