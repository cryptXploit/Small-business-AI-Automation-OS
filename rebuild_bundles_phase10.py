#!/usr/bin/env python3
"""
Rebuild all 5 commercial .zip bundles with Phase 10 assets:
1. START-HERE-LAUNCHPAD.html inside root of all 5 zips
2. Upgraded smallbiz-automation-os-app.html (Full CRUD + 3-Tier + Thirst Engine)
3. tier0-free-lite-command-sheet.xlsx, Tier0-Free-Notion-Quickstart, Tier0-Free-Starter-Automation in Tier 0
Author: OMAR SUNNY
"""

import os
import zipfile
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent
BUNDLE_DIR = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE"
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)


def create_bundle_zip(zip_filename: str, tier_title: str, file_mappings: list) -> dict:
    zip_path = BUNDLE_DIR / zip_filename
    inventory_lines = [
        "================================================================================",
        "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM (2026 ENTERPRISE EDITION)",
        f"FINAL PRODUCTION PACKAGE INVENTORY: {tier_title}",
        "Author: OMAR SUNNY",
        "================================================================================",
        "",
        "INCLUDED FILES IN THIS ARCHIVE:",
    ]

    total_uncompressed = 0
    seen_arcnames = set()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src_rel, arcname in file_mappings:
            if arcname in seen_arcnames:
                continue
            seen_arcnames.add(arcname)
            src_path = STUDIO_ROOT / src_rel
            if not src_path.is_file():
                raise FileNotFoundError(f"Missing source file for {zip_filename}: {src_rel}")
            fsize = src_path.stat().st_size
            total_uncompressed += fsize
            zf.write(src_path, arcname=arcname)
            inventory_lines.append(f"  - {arcname} ({fsize:,} bytes)")

        inventory_lines.extend([
            "",
            "--------------------------------------------------------------------------------",
            "QUICK-START LAUNCH INSTRUCTIONS:",
            "1. Extract this .zip archive to a local folder on your workstation.",
            "2. Double-click `START-HERE-LAUNCHPAD.html` to open the interactive starter dashboard.",
            "3. Double-click `smallbiz-automation-os-app.html` to launch the 100% offline",
            "   SaaS-Lite Web Companion Suite in any browser.",
            "   (Tier 2 code: STUDIO-TIER2-2026 | Tier 3 & Tier 4 code: STUDIO-PRO-OS-2026).",
            "4. Open PDF editions in Adobe Acrobat Reader, Microsoft Edge, or GoodNotes.",
            "================================================================================",
        ])
        readme_bytes = "\n".join(inventory_lines).encode("utf-8")
        zf.writestr("README-BUNDLE-INVENTORY.txt", readme_bytes)

    zip_size = zip_path.stat().st_size
    print(f"  [+] Built {zip_filename}: {zip_size:,} bytes ({len(file_mappings)} files, {total_uncompressed:,} uncompressed bytes)")
    return {
        "filename": zip_filename,
        "size_bytes": zip_size,
        "files_count": len(file_mappings) + 1,
        "uncompressed_bytes": total_uncompressed + len(readme_bytes)
    }


def main():
    print("=== Rebuilding All 5 Commercial Bundles with Phase 10 Upgrades ===")

    # 1. Tier 0: Free Starter Kit ($0)
    tier0_files = [
        ("START-HERE-LAUNCHPAD.html", "START-HERE-LAUNCHPAD.html"),
        ("09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf", "01-Book-Sample-and-Audit/tier0-free-sample-chapter01-and-audit.pdf"),
        ("05-WORKBOOKS/chapter-01-workbook.pdf", "01-Book-Sample-and-Audit/chapter-01-workbook.pdf"),
        ("07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html", "02-Interactive-ROI-Web-App/smallbiz-automation-os-app.html"),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", "02-Interactive-ROI-Web-App/README-WEB-APP.md"),
        ("06-NOTION-TEMPLATES/Spreadsheets/tier0-free-lite-command-sheet.xlsx", "03-Spreadsheet-Calculator/tier0-free-lite-command-sheet.xlsx"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", "03-Spreadsheet-Calculator/sheet1-automation-roi-and-leak-calculator.csv"),
        ("06-NOTION-TEMPLATES/Tier0-Free-Notion-Quickstart/01-Core-Starter-Database.csv", "04-Free-Notion-Quickstart/01-Core-Starter-Database.csv"),
        ("06-NOTION-TEMPLATES/Tier0-Free-Notion-Quickstart/FREE-NOTION-QUICKSTART-GUIDE.md", "04-Free-Notion-Quickstart/FREE-NOTION-QUICKSTART-GUIDE.md"),
        ("14-AUTOMATION-BLUEPRINTS/Tier0-Free-Starter-Automation/01-60s-instant-lead-router-and-sms-intake.json", "05-Free-Automation-Blueprint/01-60s-instant-lead-router-and-sms-intake.json"),
        ("14-AUTOMATION-BLUEPRINTS/Tier0-Free-Starter-Automation/FREE-AUTOMATION-1CLICK-TEST-GUIDE.md", "05-Free-Automation-Blueprint/FREE-AUTOMATION-1CLICK-TEST-GUIDE.md"),
        ("13-VISUAL-CHEAT-SHEETS/00-ECOSYSTEM-MASTER-MAP-POSTER.png", "06-Visual-Cheat-Sheets/00-ECOSYSTEM-MASTER-MAP-POSTER.png"),
        ("13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch01.png", "06-Visual-Cheat-Sheets/cheat-sheet-ch01.png"),
        ("04-VISUAL-ASSETS/chapter-01-mindmap.svg", "07-Architecture-Diagrams/chapter-01-mindmap.svg"),
        ("04-VISUAL-ASSETS/chapter-01-flowchart.svg", "07-Architecture-Diagrams/chapter-01-flowchart.svg"),
        ("08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png", "08-Cover/gumroad-tier0-free-audit-cover.png"),
    ]

    # 2. Tier 1: KDP & D2D Retail Book Pack ($9.99 / $19.99)
    tier1_files = [
        ("START-HERE-LAUNCHPAD.html", "START-HERE-LAUNCHPAD.html"),
        ("09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub", "01-Kindle-and-D2D-EPUB3/the-smallbiz-ai-automation-os.epub"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf", "02-KDP-Print-6x9-Interior/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf"),
        ("08-COVER-DESIGN/ebook-cover-kdp-kindle.png", "03-Retail-Covers/ebook-cover-kdp-kindle.png"),
        ("08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf", "03-Retail-Covers/kdp-paperback-full-wrap-cover.pdf"),
        ("08-COVER-DESIGN/kdp-paperback-full-wrap-cover.png", "03-Retail-Covers/kdp-paperback-full-wrap-cover.png"),
        ("10-MARKETING/marketplace-listings-and-bd-launch-runbook.md", "04-Publishing-Runbooks/marketplace-listings-and-bd-launch-runbook.md"),
        ("08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md", "04-Publishing-Runbooks/COVER-DESIGN-AND-PACKAGING-SPEC.md"),
    ]

    # 3. Tier 2: Interactive Workbook & Atlas Edition ($29)
    tier2_files = [
        ("START-HERE-LAUNCHPAD.html", "START-HERE-LAUNCHPAD.html"),
        ("07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html", "00-Interactive-Web-Companion/smallbiz-automation-os-app.html"),
        ("09-EXPORTS/PDF/the-smallbiz-ai-automation-os-complete-book.pdf", "01-Master-Book/the-smallbiz-ai-automation-os-complete-book.pdf"),
        ("09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub", "01-Master-Book/the-smallbiz-ai-automation-os.epub"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-us-letter.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-us-letter.pdf"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-a4.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-a4.pdf"),
        ("09-EXPORTS/PDF/the-smallbiz-ai-automation-os-tablet-planner.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-tablet-planner.pdf"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/02-Editable-10-Chapter-Action-Workbook.docx", "02-Fillable-Workbooks-and-Planner/02-Editable-10-Chapter-Action-Workbook.docx"),
        ("13-VISUAL-CHEAT-SHEETS/the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf", "03-Visual-Shortcut-Atlas-and-Posters/the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf"),
        ("13-VISUAL-CHEAT-SHEETS/00-ECOSYSTEM-MASTER-MAP-POSTER.svg", "03-Visual-Shortcut-Atlas-and-Posters/00-ECOSYSTEM-MASTER-MAP-POSTER.svg"),
        ("13-VISUAL-CHEAT-SHEETS/00-ECOSYSTEM-MASTER-MAP-POSTER.png", "03-Visual-Shortcut-Atlas-and-Posters/00-ECOSYSTEM-MASTER-MAP-POSTER.png"),
        ("06-NOTION-TEMPLATES/Spreadsheets/62-Item-Prompt-and-SOP-Vault.csv", "04-Prompt-and-SOP-Vault/62-Item-Prompt-and-SOP-Vault.csv"),
        ("08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png", "07-Covers/gumroad-tier2-workbook-atlas-cover.png"),
    ]
    for ch in range(1, 11):
        tier2_files.append((f"13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch{ch:02d}.svg", f"03-Visual-Shortcut-Atlas-and-Posters/cheat-sheet-ch{ch:02d}.svg"))
        tier2_files.append((f"13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch{ch:02d}.png", f"03-Visual-Shortcut-Atlas-and-Posters/cheat-sheet-ch{ch:02d}.png"))
        tier2_files.append((f"04-VISUAL-ASSETS/chapter-{ch:02d}-mindmap.svg", f"05-Chapter-Architecture-Diagrams/chapter-{ch:02d}-mindmap.svg"))
        tier2_files.append((f"04-VISUAL-ASSETS/chapter-{ch:02d}-flowchart.svg", f"05-Chapter-Architecture-Diagrams/chapter-{ch:02d}-flowchart.svg"))
        tier2_files.append((f"05-WORKBOOKS/worksheet-{ch:02d}.md", f"06-Markdown-Workbooks/worksheet-{ch:02d}.md"))

    # 4. Tier 3: Complete Small Business AI Automation OS Flagship Bundle ($59)
    tier3_files = list(tier2_files) + [
        ("07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt", "08-Pro-Web-Companion-App/PRO-ACCESS-LICENSE-KEY.txt"),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", "08-Pro-Web-Companion-App/README-WEB-APP.md"),
        ("06-NOTION-TEMPLATES/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv", "09-Notion-OS-5-Database-Kit/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv"),
        ("06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv", "09-Notion-OS-5-Database-Kit/02-Automation-Workflows-and-Health-Registry.csv"),
        ("06-NOTION-TEMPLATES/03-AI-Prompt-and-SOP-Vault-62.csv", "09-Notion-OS-5-Database-Kit/03-AI-Prompt-and-SOP-Vault-62.csv"),
        ("06-NOTION-TEMPLATES/04-Weekly-Owner-KPI-Scorecard.csv", "09-Notion-OS-5-Database-Kit/04-Weekly-Owner-KPI-Scorecard.csv"),
        ("06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.csv", "09-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.csv"),
        ("06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.md", "09-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.md"),
        ("06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md", "09-Notion-OS-5-Database-Kit/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"),
        ("06-NOTION-TEMPLATES/Spreadsheets/tier0-free-lite-command-sheet.xlsx", "10-Excel-8Tab-Command-Center/tier0-free-lite-command-sheet.xlsx"),
        ("06-NOTION-TEMPLATES/Spreadsheets/the-smallbiz-ai-automation-os-financial-and-roi-matrix.xlsx", "10-Excel-8Tab-Command-Center/the-smallbiz-ai-automation-os-financial-and-roi-matrix.xlsx"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", "10-Excel-8Tab-Command-Center/sheet1-automation-roi-and-leak-calculator.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet2-5day-time-and-task-audit.csv", "10-Excel-8Tab-Command-Center/sheet2-5day-time-and-task-audit.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet3-speed-to-lead-latency-and-recovery-model.csv", "10-Excel-8Tab-Command-Center/sheet3-speed-to-lead-latency-and-recovery-model.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet4-3option-quote-and-14day-nurture-roi.csv", "10-Excel-8Tab-Command-Center/sheet4-3option-quote-and-14day-nurture-roi.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet5-support-deflection-and-90day-winback.csv", "10-Excel-8Tab-Command-Center/sheet5-support-deflection-and-90day-winback.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet6-invoicing-ar-chasers-and-dso-cashflow.csv", "10-Excel-8Tab-Command-Center/sheet6-invoicing-ar-chasers-and-dso-cashflow.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet7-friday-16week-owner-kpi-scorecard.csv", "10-Excel-8Tab-Command-Center/sheet7-friday-16week-owner-kpi-scorecard.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet8-90day-rollout-and-tool-stack-budget.csv", "10-Excel-8Tab-Command-Center/sheet8-90day-rollout-and-tool-stack-budget.csv"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/01-Full-Editable-Book-Manuscript.docx", "11-Editable-Word-SOP-Suite/01-Full-Editable-Book-Manuscript.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/02-Editable-10-Chapter-Action-Workbook.docx", "11-Editable-Word-SOP-Suite/02-Editable-10-Chapter-Action-Workbook.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/03-AI-Automation-Rollout-Proposal-and-Charter.docx", "11-Editable-Word-SOP-Suite/03-AI-Automation-Rollout-Proposal-and-Charter.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/04-Customer-Escalation-and-Refund-SOP-Matrix.docx", "11-Editable-Word-SOP-Suite/04-Customer-Escalation-and-Refund-SOP-Matrix.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/05-Staff-AI-Usage-and-Data-Privacy-Policy.docx", "11-Editable-Word-SOP-Suite/05-Staff-AI-Usage-and-Data-Privacy-Policy.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/06-Vendor-and-Tool-Stack-Onboarding-Checklist.docx", "11-Editable-Word-SOP-Suite/06-Vendor-and-Tool-Stack-Onboarding-Checklist.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/07-Weekly-Owner-Executive-Brief-Template.docx", "11-Editable-Word-SOP-Suite/07-Weekly-Owner-Executive-Brief-Template.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Slide-Decks/01-Team-AI-Automation-Onboarding-and-SOP-Deck.pptx", "12-Executive-Slide-Decks/01-Team-AI-Automation-Onboarding-and-SOP-Deck.pptx"),
        ("12-EDITABLE-OFFICE-SUITE/Slide-Decks/02-Quarterly-Automation-ROI-and-KPI-Review-Deck.pptx", "12-Executive-Slide-Decks/02-Quarterly-Automation-ROI-and-KPI-Review-Deck.pptx"),
        ("12-EDITABLE-OFFICE-SUITE/Slide-Decks/03-Client-and-Partner-Operational-Excellence-Pitch-Deck.pptx", "12-Executive-Slide-Decks/03-Client-and-Partner-Operational-Excellence-Pitch-Deck.pptx"),
        ("14-AUTOMATION-BLUEPRINTS/01-60s-instant-lead-router-and-sms-intake.json", "13-Automation-Blueprints-JSON/01-60s-instant-lead-router-and-sms-intake.json"),
        ("14-AUTOMATION-BLUEPRINTS/02-ai-support-triage-and-amber-approval-gate.json", "13-Automation-Blueprints-JSON/02-ai-support-triage-and-amber-approval-gate.json"),
        ("14-AUTOMATION-BLUEPRINTS/03-3option-instant-quote-and-14day-followup.json", "13-Automation-Blueprints-JSON/03-3option-instant-quote-and-14day-followup.json"),
        ("14-AUTOMATION-BLUEPRINTS/04-overdue-invoice-5stage-payment-chaser.json", "13-Automation-Blueprints-JSON/04-overdue-invoice-5stage-payment-chaser.json"),
        ("14-AUTOMATION-BLUEPRINTS/05-friday-3pm-owner-kpi-executive-digest.json", "13-Automation-Blueprints-JSON/05-friday-3pm-owner-kpi-executive-digest.json"),
        ("14-AUTOMATION-BLUEPRINTS/NO-CODE-AUTOMATION-SETUP-GUIDE.md", "13-Automation-Blueprints-JSON/NO-CODE-AUTOMATION-SETUP-GUIDE.md"),
        ("08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png", "07-Covers/gumroad-tier3-flagship-os-bundle-cover.png"),
        ("08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html", "14-Design-Customizer-Studio/design-customizer-studio.html"),
    ]

    # 5. Tier 4: Living Automation Vault VIP Membership Drop 01
    tier4_files = list(tier3_files) + [
        ("08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png", "07-Covers/gumroad-tier4-living-vault-membership-cover.png"),
    ]

    create_bundle_zip("Tier0-Free-5Day-Audit-Starter-Kit.zip", "Tier 0: Free 5-Day Audit Starter Kit ($0)", tier0_files)
    create_bundle_zip("Tier1-KDP-and-D2D-Retail-Book-Pack.zip", "Tier 1: KDP & D2D Retail Book Pack ($9.99 / $19.99)", tier1_files)
    create_bundle_zip("Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip", "Tier 2: Interactive Workbook & Atlas Edition ($29)", tier2_files)
    create_bundle_zip("Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip", "Tier 3: Complete Small Business AI Automation OS Flagship ($59)", tier3_files)
    create_bundle_zip("Tier4-Living-Automation-Vault-Membership-Drop01.zip", "Tier 4: Living Automation Vault VIP Membership Drop 01", tier4_files)

    print("\nAll 5 commercial .zip bundles rebuilt successfully!")


if __name__ == "__main__":
    main()
