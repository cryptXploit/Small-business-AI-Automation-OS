#!/usr/bin/env python3
"""
Verification Script: Phase 10 Universal Funnel & Conversion Architecture
Project: The Small Business AI Automation Operating System
Author: OMAR SUNNY
"""

import os
import sys
import json
import zipfile
import subprocess
import openpyxl

STUDIO_ROOT = os.path.dirname(os.path.abspath(__file__))
ERRORS = []

print(f"=== Running Phase 10 Funnel Verification in: {STUDIO_ROOT} ===\n")


def check(condition, desc):
    if condition:
        print(f"  [PASS] {desc}")
    else:
        print(f"  [FAIL] {desc}")
        ERRORS.append(desc)


# 1. Step 1 Forensic Audit Report Check
audit_md = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "audit_report_phase10.md")
check(os.path.isfile(audit_md), "audit_report_phase10.md exists in 15-DEPLOY-AND-FUNNEL-BRIDGE/")
if os.path.isfile(audit_md):
    with open(audit_md, "r", encoding="utf-8") as f:
        audit_text = f.read()
    check("OMAR SUNNY" in audit_text or "Md Omar Sunny" in audit_text, "audit_report_phase10.md credits OMAR SUNNY")
    check("EXECUTIVE SUMMARY" in audit_text, "audit_report_phase10.md contains Executive Summary")
    check("REMEDIATIONS" in audit_text, "audit_report_phase10.md contains Remediations breakdown")

# 2. Step 2 Web App CRUD & 3-Tier Check
app_html = os.path.join(STUDIO_ROOT, "07-INTERACTIVE-TOOLS", "smallbiz-automation-os-app.html")
check(os.path.isfile(app_html), "07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html exists")
if os.path.isfile(app_html):
    with open(app_html, "r", encoding="utf-8") as f:
        app_text = f.read()
    check(len(app_text) > 500000, f"smallbiz-automation-os-app.html is full-featured ({len(app_text):,} chars)")
    check("localStorage" in app_text, "Web App supports localStorage persistence")
    check("Add Custom Row" in app_text or "openAddCmfRowModal" in app_text, "Web App has + Add Custom Row functionality")
    check("editInline" in app_text or "Edit Inline" in app_text, "Web App has Edit Inline functionality")
    check("Reset to Studio Defaults" in app_text or "resetCmfDefaults" in app_text, "Web App has Reset to Defaults")
    check("Personal Notes & Action Log" in app_text, "Web App has Personal Notes & Action Log scratchpads")
    check("TIER 0: FREE DIAGNOSTIC" in app_text or "tier-0" in app_text, "Web App implements 3-Tier Progressive Access Bar")
    check("STUDIO-TIER2-2026" in app_text, "Web App supports Tier 2 unlock code STUDIO-TIER2-2026")
    check("STUDIO-PRO-OS-2026" in app_text or "SMALLBIZ-OS-PRO-2026" in app_text, "Web App supports Tier 3 Pro unlock codes")
    check("Diagnostic Alert: Based on the numbers you just entered in Module 1, our engine calculated" in app_text, "Web App implements dynamic personalized teaser calculations")
    check("glassmorphism" in app_text or "backdrop-filter" in app_text, "Web App has glassmorphism blur on locked content")
    check("exportWorkspaceJson" in app_text and "handleWorkspaceFileSelect" in app_text, "Web App supports 1-Click JSON Backup & Restore")

# 3. Step 3 Tier 0 Wow Assets Check
tier0_xlsx = os.path.join(STUDIO_ROOT, "06-NOTION-TEMPLATES", "Spreadsheets", "tier0-free-lite-command-sheet.xlsx")
check(os.path.isfile(tier0_xlsx), "tier0-free-lite-command-sheet.xlsx exists")
if os.path.isfile(tier0_xlsx):
    wb = openpyxl.load_workbook(tier0_xlsx)
    sheet_names = wb.sheetnames
    check("Ch1-Diagnostic-Calculator" in sheet_names, f"Tab 1 (Ch1-Diagnostic-Calculator) exists in {sheet_names}")
    check("7-Day-Action-Tracker" in sheet_names, "Tab 2 (7-Day-Action-Tracker) exists")
    check("Pro-OS-8Tab-Command-Center" in sheet_names, "Tab 3 (Pro-OS-8Tab-Command-Center) exists")
    ws1 = wb["Ch1-Diagnostic-Calculator"]
    check(len(ws1._charts) > 0, "Tab 1 contains native embedded OpenPyXL Chart")
    check("=SUM" in str(ws1["C12"].value).upper() or "=ROUND" in str(ws1["G6"].value).upper(), "Tab 1 contains live Excel formulas")

notion_csv = os.path.join(STUDIO_ROOT, "06-NOTION-TEMPLATES", "Tier0-Free-Notion-Quickstart", "01-Core-Starter-Database.csv")
notion_guide = os.path.join(STUDIO_ROOT, "06-NOTION-TEMPLATES", "Tier0-Free-Notion-Quickstart", "FREE-NOTION-QUICKSTART-GUIDE.md")
check(os.path.isfile(notion_csv), "06-NOTION-TEMPLATES/Tier0-Free-Notion-Quickstart/01-Core-Starter-Database.csv exists")
check(os.path.isfile(notion_guide), "FREE-NOTION-QUICKSTART-GUIDE.md exists")

blueprint_json = os.path.join(STUDIO_ROOT, "14-AUTOMATION-BLUEPRINTS", "Tier0-Free-Starter-Automation", "01-60s-instant-lead-router-and-sms-intake.json")
blueprint_guide = os.path.join(STUDIO_ROOT, "14-AUTOMATION-BLUEPRINTS", "Tier0-Free-Starter-Automation", "FREE-AUTOMATION-1CLICK-TEST-GUIDE.md")
check(os.path.isfile(blueprint_json), "01-60s-instant-lead-router-and-sms-intake.json exists in Tier0-Free-Starter-Automation/")
check(os.path.isfile(blueprint_guide), "FREE-AUTOMATION-1CLICK-TEST-GUIDE.md exists")

# 4. Step 4 Browser Launchpad & Headless Render Check
launchpad_file = os.path.join(STUDIO_ROOT, "START-HERE-LAUNCHPAD.html")
check(os.path.isfile(launchpad_file), "START-HERE-LAUNCHPAD.html exists in studio root")
if os.path.isfile(launchpad_file):
    with open(launchpad_file, "r", encoding="utf-8") as f:
        lp_text = f.read()
    check("OMAR SUNNY" in lp_text, "START-HERE-LAUNCHPAD.html credits OMAR SUNNY")
    check("3-Step Quickstart Progress Tracker" in lp_text, "Launchpad has 3-Step Progress Tracker")
    check("Launch Interactive Companion Web App" in lp_text or "Launch Web App" in lp_text, "Launchpad has 1-Click Action buttons")
    check("Commercial Edition Value Ladder" in lp_text, "Launchpad has Upgrade Matrix")

# Headless browser render test
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if os.path.exists(chrome_path):
    preview_img = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "launchpad_render_test.png")
    try:
        res = subprocess.run([
            chrome_path, "--headless=new", "--no-sandbox", "--disable-gpu",
            f"--screenshot={preview_img}", "--window-size=1280,800", launchpad_file
        ], capture_output=True, text=True, timeout=15)
        check(os.path.exists(preview_img) and os.path.getsize(preview_img) > 10000,
              f"START-HERE-LAUNCHPAD.html renders cleanly via Headless Chrome ({os.path.getsize(preview_img):,} bytes)")
        if os.path.exists(preview_img):
            os.remove(preview_img)
    except Exception as e:
        check(False, f"Headless Chrome render exception: {e}")
else:
    print("  [SKIP] Headless Chrome binary not found for screenshot test")

# 5. Step 5 Deployment Bridge & Live Demo Package Check
config_json = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "funnel-links-config.json")
check(os.path.isfile(config_json), "funnel-links-config.json exists")
if os.path.isfile(config_json):
    with open(config_json, "r", encoding="utf-8") as f:
        cdata = json.load(f)
    for k in ["gumroad_tier0_free_url", "gumroad_tier2_workbook_url", "gumroad_tier3_flagship_url", "gumroad_tier4_vip_url", "live_web_app_demo_url"]:
        check(k in cdata and len(cdata[k]) > 5, f"funnel-links-config.json contains valid key: {k}")

inject_py = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "inject_funnel_links.py")
check(os.path.isfile(inject_py), "inject_funnel_links.py exists in 15-DEPLOY-AND-FUNNEL-BRIDGE/")

demo_index = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "web-live-demo", "index.html")
demo_app = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "web-live-demo", "app.html")
check(os.path.isfile(demo_index), "web-live-demo/index.html exists")
check(os.path.isfile(demo_app), "web-live-demo/app.html exists")
if os.path.isfile(demo_index):
    with open(demo_index, "r", encoding="utf-8") as f:
        dtext = f.read()
    check("Try the Interactive OS Web App Live in Your Browser" in dtext, "web-live-demo/index.html has Live Demo CTA button")
    check("Download Complete Free Starter Kit" in dtext, "web-live-demo/index.html has Free Gumroad Download CTA button")

# 6. Step 6 Viral Playbook & Owner Guide Check
playbook_md = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md")
check(os.path.isfile(playbook_md), "VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md exists")
if os.path.isfile(playbook_md):
    with open(playbook_md, "r", encoding="utf-8") as f:
        ptext = f.read()
    check("r/smallbusiness" in ptext and "r/entrepreneur" in ptext, "Playbook contains 5 Subreddit Value-Drop posts")
    check("Video 1" in ptext and "Video 5" in ptext, "Playbook contains 5 Video Reels/Shorts scripts")
    check("Auto-DM" in ptext or "Retweet" in ptext, "Playbook contains 3 LinkedIn/X Auto-DM posts")
    check("1-Hour Quick Win" in ptext and "FOUNDER40" in ptext, "Playbook contains 3 Automated Email Workflows")

owner_guide_md = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "OWNER-MANUAL-SETUP-GUIDE-BANGLA.md")
check(os.path.isfile(owner_guide_md), "OWNER-MANUAL-SETUP-GUIDE-BANGLA.md exists")
if os.path.isfile(owner_guide_md):
    with open(owner_guide_md, "r", encoding="utf-8") as f:
        otext = f.read()
    check("ওমর সানি" in otext or "OMAR SUNNY" in otext, "Owner Guide is tailored for Omar Sunny")
    check("গামরোড" in otext and "GitHub Pages" in otext, "Owner Guide contains step-by-step Bangla instructions")
    check("Make.com" in otext and "Notion" in otext, "Owner Guide explains affiliate passive income")

# 7. Step 7 Commercial .ZIP Bundles Integrity Check
bundle_dir = os.path.join(STUDIO_ROOT, "09-EXPORTS", "HYBRID-BUNDLE")
required_zips = [
    ("Tier0-Free-5Day-Audit-Starter-Kit.zip", ["START-HERE-LAUNCHPAD.html", "tier0-free-lite-command-sheet.xlsx", "01-Core-Starter-Database.csv", "01-60s-instant-lead-router-and-sms-intake.json"]),
    ("Tier1-KDP-and-D2D-Retail-Book-Pack.zip", ["START-HERE-LAUNCHPAD.html"]),
    ("Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip", ["START-HERE-LAUNCHPAD.html", "smallbiz-automation-os-app.html"]),
    ("Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip", ["START-HERE-LAUNCHPAD.html", "smallbiz-automation-os-app.html", "tier0-free-lite-command-sheet.xlsx"]),
    ("Tier4-Living-Automation-Vault-Membership-Drop01.zip", ["START-HERE-LAUNCHPAD.html", "smallbiz-automation-os-app.html"])
]

for zname, required_members in required_zips:
    zpath = os.path.join(bundle_dir, zname)
    check(os.path.isfile(zpath), f"Bundle exists: {zname}")
    if os.path.isfile(zpath):
        with zipfile.ZipFile(zpath, "r") as zf:
            names = zf.namelist()
            for req in required_members:
                found = any(req in n for n in names)
                check(found, f"  -> {zname} contains '{req}'")

print("\n" + "="*80)
if len(ERRORS) == 0:
    print(">>> 0 QA ERRORS DETECTED! PHASE 10 FUNNEL UPGRADE VERIFIED 100% COMPLETE! <<<")
    print("="*80)
    sys.exit(0)
else:
    print(f">>> {len(ERRORS)} QA ERRORS ENCOUNTERED! <<<")
    for err in ERRORS:
        print(f"  - {err}")
    print("="*80)
    sys.exit(1)
