#!/usr/bin/env python3
"""
Centralized Conversion Funnel Link Injector
Project: The Small Business AI Automation Operating System
Author: OMAR SUNNY
Synchronizes live Gumroad, Payhip, and Amazon links across the entire studio ecosystem.
"""

import os
import json
import re
import sys

STUDIO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "funnel-links-config.json")

print(f"Loading funnel configuration from: {CONFIG_PATH}")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

print(f"Target author: {config.get('_author', 'OMAR SUNNY')}")
print(f"Tier 0 Free URL: {config.get('gumroad_tier0_free_url')}")
print(f"Tier 2 URL: {config.get('gumroad_tier2_workbook_url')}")
print(f"Tier 3 URL: {config.get('gumroad_tier3_flagship_url')}")
print(f"Tier 4 VIP URL: {config.get('gumroad_tier4_vip_url')}")
print(f"Live Web App URL: {config.get('live_web_app_demo_url')}")

# Files to inject links into
TARGET_FILES = [
    os.path.join(STUDIO_ROOT, "10-MARKETING", "index.html"),
    os.path.join(STUDIO_ROOT, "07-INTERACTIVE-TOOLS", "smallbiz-automation-os-app.html"),
    os.path.join(STUDIO_ROOT, "START-HERE-LAUNCHPAD.html"),
    os.path.join(STUDIO_ROOT, "15-WEB-DEPLOYMENT", "dist", "app", "index.html"),
    os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "web-live-demo", "index.html"),
    os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE", "web-live-demo", "app.html")
]

updated_count = 0
for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    orig_content = content
    # Replace dummy or old links
    if config.get("gumroad_tier0_free_url"):
        content = re.sub(r'https://[a-zA-Z0-9_-]+\.gumroad\.com/l/smallbiz-automation-[a-zA-Z0-9_-]*free[a-zA-Z0-9_-]*', config["gumroad_tier0_free_url"], content)
    if config.get("gumroad_tier2_workbook_url"):
        content = re.sub(r'https://[a-zA-Z0-9_-]+\.gumroad\.com/l/smallbiz-automation-[a-zA-Z0-9_-]*workbook[a-zA-Z0-9_-]*', config["gumroad_tier2_workbook_url"], content)
    if config.get("gumroad_tier3_flagship_url"):
        content = re.sub(r'https://[a-zA-Z0-9_-]+\.gumroad\.com/l/smallbiz-automation-[a-zA-Z0-9_-]*flagship[a-zA-Z0-9_-]*', config["gumroad_tier3_flagship_url"], content)
    if config.get("gumroad_tier4_vip_url"):
        content = re.sub(r'https://[a-zA-Z0-9_-]+\.gumroad\.com/l/smallbiz-automation-[a-zA-Z0-9_-]*vault[a-zA-Z0-9_-]*', config["gumroad_tier4_vip_url"], content)
    if config.get("live_web_app_demo_url"):
        content = re.sub(r'https://[a-zA-Z0-9_-]+\.github\.io/[a-zA-Z0-9_-]+/app/?', config["live_web_app_demo_url"], content)

    if content != orig_content:
        with open(fpath, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"Updated links in: {os.path.relpath(fpath, STUDIO_ROOT)}")
        updated_count += 1
    else:
        print(f"No link replacements needed in: {os.path.relpath(fpath, STUDIO_ROOT)}")

print(f"Link injection complete. Updated {updated_count} files.")
