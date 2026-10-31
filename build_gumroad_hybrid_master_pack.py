#!/usr/bin/env python3
"""
build_gumroad_hybrid_master_pack.py — Gumroad Hybrid Storefront Master Setup Pack & 600x600 Square Thumbnail Builder
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)
Author: OMAR SUNNY

Builds:
1. 3 Vector SVGs + 3 Exact 600x600 px Square Discover Thumbnails in 08-COVER-DESIGN/ (and copied to 10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/)
2. 4 Exact 1280x720 px (16:9) Gumroad Cover Banners in 10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/
3. 6 Comprehensive Markdown Playbooks inside 10-MARKETING/Gumroad-Hybrid-Master-Setup/:
   - 00-UNIFIED-2-LINK-MASTER-STRATEGY-AND-LOCKED-SETUP.md
   - 01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md (>= 1,500 words)
   - 02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md (>= 2,500 words)
   - 03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md (>= 1,800 words)
   - 04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md (>= 1,800 words)
   - 05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md (>= 1,800 words)
"""

import base64
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from PIL import Image, ImageFilter

STUDIO_ROOT = Path(__file__).resolve().parent
COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
MARKETING_DIR = STUDIO_ROOT / "10-MARKETING"
GUMROAD_DIR = MARKETING_DIR / "Gumroad-Hybrid-Master-Setup"
THUMBS_DIR = GUMROAD_DIR / "Thumbnails-and-Covers"

GUMROAD_DIR.mkdir(parents=True, exist_ok=True)
THUMBS_DIR.mkdir(parents=True, exist_ok=True)

BANNED_REPLACEMENTS = {
    r"\bdelve(?:s|d|ing)?\b": "examine",
    r"\btapestr(?:y|ies)\b": "architecture",
    r"\btestament(?:s)?\b": "proof",
    r"\bbeacon(?:s)?\b": "signal",
    r"\bsymphon(?:y|ies)\b": "coordination",
    r"\bunlock(?:s|ed|ing)?\b": "activate",
    r"\bunleash(?:es|ed|ing)?\b": "deploy",
    r"\bskyrocket(?:s|ed|ing)?\b": "accelerate",
    r"\bsupercharg(?:e|es|ed|ing)\b": "upgrade",
    r"\bgame-changer(?:s)?\b": "core advantage",
    r"\bpivotal\b": "critical",
    r"\brealm(?:s)?\b": "domain",
    r"\bfoster(?:s|ed|ing)?\b": "build",
    r"\bunderscor(?:e|es|ed|ing)\b": "highlight",
    r"\butiliz(?:e|es|ed|ing|ation)\b": "use",
    r"\bleverag(?:e|es|ed|ing)\b": "apply",
}


def sanitize_text(text: str) -> str:
    for pat, repl in BANNED_REPLACEMENTS.items():
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text


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
    raise RuntimeError("No headless Chromium browser (Edge or Chrome) found.")


def render_svg_to_exact_png(browser_exe: str, svg_path: Path, png_path: Path, width: int, height: int):
    svg_xml = svg_path.read_text(encoding="utf-8")
    svg_xml = re.sub(r"<\?xml[^>]+\?>", "", svg_xml).strip()

    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: #0F172A;
  }}
  svg {{
    width: {width}px;
    height: {height}px;
    display: block;
  }}
</style>
</head>
<body>
{svg_xml}
</body>
</html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(wrapper_html)
        temp_html_path = Path(tf.name)

    try:
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={str(png_path)}",
            temp_html_path.as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=45)
        # Ensure exact pixel dimensions via PIL in case headless browser adds 1px border
        im = Image.open(png_path).convert("RGB")
        if im.size != (width, height):
            im = im.resize((width, height), Image.Resampling.LANCZOS)
            im.save(png_path, format="PNG", optimize=True)
    finally:
        if temp_html_path.exists():
            temp_html_path.unlink()


def get_omar_sunny_cover_thumb_b64() -> str:
    src = COVER_DIR / "omar-sunny-custom-front-cover.jpg"
    if not src.exists():
        return ""
    im = Image.open(src).convert("RGB")
    im = im.resize((220, 328), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def build_square_svg_1(cover_b64: str) -> str:
    img_tag = (
        f'<image x="395" y="150" width="165" height="246" rx="8" href="{cover_b64}" />'
        if cover_b64
        else ""
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="sq1_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="55%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <linearGradient id="sq1_cyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284C7" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
  </defs>
  <rect width="600" height="600" fill="url(#sq1_bg)" />
  <rect x="18" y="18" width="564" height="564" rx="18" fill="none" stroke="#334155" stroke-width="2.5" />
  <rect x="28" y="28" width="544" height="544" rx="14" fill="none" stroke="#0284C7" stroke-width="1.5" stroke-opacity="0.7" />

  <!-- Top Badge -->
  <rect x="42" y="46" width="516" height="48" rx="10" fill="url(#sq1_cyan)" />
  <text x="300" y="77" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="21" font-weight="900" letter-spacing="1.5">
    $0 FREE STARTER KIT • 5-DAY AUDIT
  </text>

  <!-- Main Headline Left -->
  <text x="42" y="152" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="700" letter-spacing="1.5">
    SMALL BUSINESS AI AUTOMATION OS
  </text>
  <text x="42" y="198" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="36" font-weight="900">
    TIME &amp; LEAD-LEAK
  </text>
  <text x="42" y="240" fill="#34D399" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="36" font-weight="900">
    AUDIT RESCUE PACK
  </text>

  <!-- Feature Pills Left -->
  <rect x="42" y="268" width="335" height="38" rx="8" fill="#1E293B" stroke="#059669" stroke-width="1.5" />
  <text x="58" y="293" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="15" font-weight="700">
    ✓ 32-Page Ch.1 + Fillable Audit PDF
  </text>

  <rect x="42" y="316" width="335" height="38" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="1.5" />
  <text x="58" y="341" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="15" font-weight="700">
    ✓ Offline ROI Calculator Web App
  </text>

  <rect x="42" y="364" width="335" height="38" rx="8" fill="#1E293B" stroke="#D97706" stroke-width="1.5" />
  <text x="58" y="389" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="15" font-weight="700">
    ✓ 5 AI Prompts + Crisis Script 01
  </text>

  <!-- Right Book Mockup Frame -->
  <rect x="391" y="146" width="173" height="254" rx="10" fill="#0F172A" stroke="#38BDF8" stroke-width="2.5" />
  {img_tag}

  <!-- Bottom Metrics Strip -->
  <rect x="42" y="424" width="516" height="84" rx="12" fill="#1E293B" stroke="#334155" stroke-width="2" />
  <text x="300" y="458" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="20" font-weight="800">
    CMF ROI SIMULATOR + P.A.C.E. MATRIX + CSV SHEET
  </text>
  <text x="300" y="488" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="700">
    INSTANT ZIP DOWNLOAD • 100% OFFLINE PRIVACY
  </text>

  <!-- Author Footer -->
  <text x="300" y="548" text-anchor="middle" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="17" font-weight="800" letter-spacing="3">
    SYSTEM ARCHITECT: BY OMAR SUNNY
  </text>
</svg>
"""


def build_square_svg_2(cover_b64: str) -> str:
    img_tag = (
        f'<image x="395" y="142" width="165" height="246" rx="8" href="{cover_b64}" />'
        if cover_b64
        else ""
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="sq2_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="55%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <linearGradient id="sq2_em" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="100%" stop-color="#10B981" />
    </linearGradient>
  </defs>
  <rect width="600" height="600" fill="url(#sq2_bg)" />
  <rect x="18" y="18" width="564" height="564" rx="18" fill="none" stroke="#334155" stroke-width="2.5" />
  <rect x="28" y="28" width="544" height="544" rx="14" fill="none" stroke="#059669" stroke-width="2" />

  <!-- Top Badge -->
  <rect x="42" y="44" width="516" height="48" rx="10" fill="url(#sq2_em)" />
  <text x="300" y="75" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="19" font-weight="900" letter-spacing="1.2">
    COMPLETE SMALL BUSINESS AI AUTOMATION OS
  </text>

  <!-- Main Headline Left -->
  <text x="42" y="138" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" letter-spacing="1.5">
    4-TIER HYBRID EDITION ($0 • $19 • $39 • $59)
  </text>
  <text x="42" y="182" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="35" font-weight="900">
    THE 5-DEPARTMENT
  </text>
  <text x="42" y="222" fill="#34D399" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="35" font-weight="900">
    AI OPERATING SYSTEM
  </text>

  <!-- Feature Pills Left -->
  <rect x="42" y="244" width="335" height="36" rx="8" fill="#1E293B" stroke="#059669" stroke-width="1.5" />
  <text x="56" y="268" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14.5" font-weight="700">
    ✓ 50 AI Prompts • 12 Crisis Scripts • Book
  </text>

  <rect x="42" y="288" width="335" height="36" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="1.5" />
  <text x="56" y="312" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14.5" font-weight="700">
    ✓ Pro Offline Web App + 5-DB Notion OS
  </text>

  <rect x="42" y="332" width="335" height="36" rx="8" fill="#1E293B" stroke="#D97706" stroke-width="1.5" />
  <text x="56" y="356" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14.5" font-weight="700">
    ✓ 8-Tab Charted Excel + 5 JSON Workflows
  </text>

  <!-- Right Book Mockup Frame -->
  <rect x="391" y="138" width="173" height="254" rx="10" fill="#0F172A" stroke="#059669" stroke-width="2.5" />
  {img_tag}

  <!-- Bottom Tier Strip -->
  <rect x="42" y="410" width="516" height="96" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="300" y="444" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="19" font-weight="800">
    50 AI PROMPTS • WEB APP • 8-TAB EXCEL • NOTION OS
  </text>
  <text x="300" y="472" text-anchor="middle" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="700">
    MAKE.COM • ZAPIER • N8N • WORKBOOKS • VISUAL ATLAS
  </text>
  <text x="300" y="495" text-anchor="middle" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="700">
    SAVE 15+ HOURS/WEEK WITHOUT HIRING EXTRA STAFF
  </text>

  <!-- Author Footer -->
  <text x="300" y="548" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="17" font-weight="800" letter-spacing="3">
    BY OMAR SUNNY
  </text>
</svg>
"""


def build_square_svg_3(cover_b64: str) -> str:
    img_tag = (
        f'<image x="395" y="142" width="165" height="246" rx="8" href="{cover_b64}" />'
        if cover_b64
        else ""
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="sq3_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="55%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <linearGradient id="sq3_gold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D97706" />
      <stop offset="100%" stop-color="#F59E0B" />
    </linearGradient>
  </defs>
  <rect width="600" height="600" fill="url(#sq3_bg)" />
  <rect x="18" y="18" width="564" height="564" rx="18" fill="none" stroke="#334155" stroke-width="2.5" />
  <rect x="28" y="28" width="544" height="544" rx="14" fill="none" stroke="#D97706" stroke-width="2" />

  <!-- Top Badge -->
  <rect x="42" y="44" width="516" height="48" rx="10" fill="url(#sq3_gold)" />
  <text x="300" y="75" text-anchor="middle" fill="#0F172A" font-family="JetBrains Mono, Consolas, monospace" font-size="20" font-weight="900" letter-spacing="1.5">
    VIP MONTHLY VAULT &amp; OFFICE SUITE
  </text>

  <!-- Main Headline Left -->
  <text x="42" y="138" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" letter-spacing="1.5">
    RECURRING MEMBERSHIP ($12/MO OR $59/YR)
  </text>
  <text x="42" y="182" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="34" font-weight="900">
    LIVING AUTOMATION
  </text>
  <text x="42" y="222" fill="#FBBF24" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="34" font-weight="900">
    VAULT &amp; OFFICE KIT
  </text>

  <!-- Feature Pills Left -->
  <rect x="42" y="244" width="335" height="36" rx="8" fill="#1E293B" stroke="#D97706" stroke-width="1.5" />
  <text x="56" y="268" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14.5" font-weight="700">
    ✓ 7 Editable Word (.DOCX) SOP Manuals
  </text>

  <rect x="42" y="288" width="335" height="36" rx="8" fill="#1E293B" stroke="#059669" stroke-width="1.5" />
  <text x="56" y="312" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14.5" font-weight="700">
    ✓ 3 PowerPoint (.PPTX) Training Decks
  </text>

  <rect x="42" y="332" width="335" height="36" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="1.5" />
  <text x="56" y="356" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14.5" font-weight="700">
    ✓ Design Studio + Monthly Industry Drops
  </text>

  <!-- Right Book Mockup Frame -->
  <rect x="391" y="138" width="173" height="254" rx="10" fill="#0F172A" stroke="#D97706" stroke-width="2.5" />
  {img_tag}

  <!-- Bottom Strip -->
  <rect x="42" y="410" width="516" height="96" rx="12" fill="#1E293B" stroke="#D97706" stroke-width="2" />
  <text x="300" y="444" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="19" font-weight="800">
    FULL FLAGSHIP OS + WORD/PPTX + MONTHLY DROPS
  </text>
  <text x="300" y="472" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="700">
    INCLUDES CLINIC, HVAC &amp; B2B AGENCY PLAYBOOKS
  </text>
  <text x="300" y="495" text-anchor="middle" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="700">
    PRO KEY INCLUDED: SMALLBIZ-OS-PRO-2026
  </text>

  <!-- Author Footer -->
  <text x="300" y="548" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="17" font-weight="800" letter-spacing="3">
    BY OMAR SUNNY
  </text>
</svg>
"""


def copy_and_resize_1280x720_covers():
    mapping = [
        ("gumroad-tier0-free-audit-cover.png", "03-gumroad-tier0-free-audit-cover-1280x720.png"),
        ("gumroad-tier2-workbook-atlas-cover.png", "04-gumroad-tier2-workbook-edition-cover-1280x720.png"),
        ("gumroad-tier3-flagship-os-bundle-cover.png", "05-gumroad-tier3-flagship-bundle-cover-1280x720.png"),
        ("gumroad-tier4-living-vault-membership-cover.png", "06-gumroad-tier4-vip-vault-cover-1280x720.png"),
    ]
    for src_name, dst_name in mapping:
        src_p = COVER_DIR / src_name
        if src_p.exists():
            # Also copy raw 1600x1200 and a 1280x720 16:9 version
            shutil.copyfile(src_p, THUMBS_DIR / src_name)
            im = Image.open(src_p).convert("RGB")
            canvas = Image.new("RGB", (1280, 720), (15, 23, 42))
            scaled_w = int(round(im.width * (720 / im.height)))
            im_r = im.resize((scaled_w, 720), Image.Resampling.LANCZOS)
            canvas.paste(im_r, ((1280 - scaled_w) // 2, 0))
            canvas.save(THUMBS_DIR / dst_name, format="PNG", optimize=True)

    # Also copy 16:9 promo scenes 04, 05, 06, 07, 08, 09 resized to 1280x720 into THUMBS_DIR
    scenes_dir = STUDIO_ROOT / "16-VIDEO-PROMO-KIT" / "visual-scenes-16x9"
    if scenes_dir.exists():
        for sc in sorted(scenes_dir.glob("*.png"))[:6]:
            im = Image.open(sc).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
            im.save(THUMBS_DIR / f"slide-{sc.name}", format="PNG", optimize=True)


def write_guide_00_unified_strategy() -> int:
    content = """# Gumroad Unified 2-Link Hybrid Master Strategy & Locked Storefront Architecture
## Project: "The Small Business AI Automation Operating System" (By OMAR SUNNY)
**Storefront Root:** `https://sunnyomar.gumroad.com`  
**Primary Unified Product Link (All 4 Tiers `$0 / $19 / $39 / $59`):** `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`  
**Secondary Recurring Membership Link (`$12/mo` or `$59/yr`):** `https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`  

---

## 1. Executive Research Verdict: Why Putting `$0`, `$19`, `$39`, and `$59` Inside ONE Single Link (Plus 1 Separate Membership Link) Is the #1 Highest-Converting Setup on Gumroad

When selling a multi-tier digital operating system on Gumroad in 2025–2026, creators face a core structural choice:
- **Option A (4 Separate Links):** Uploading Tier 0 (`$0`), Tier 1 (`$19`), Tier 2 (`$39`), and Tier 3 (`$59`) as four disconnected product URLs.
- **Option B (The Locked Unified 2-Link Hybrid Architecture — WINNER):** Putting **all 4 one-time tiers (`$0`, `$19`, `$39`, `$59`) inside ONE flagship product URL (`sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`) using Gumroad's `Versions` feature**, while keeping the recurring **VIP Living Automation Vault & Editable Office Suite (`$12/mo` or `$59/yr`)** as a separate **`Membership`** product (`sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`) and cross-linking both pages.

### 1.1 Four Algorithmic & Psychological Reasons Why Option B Wins by a Landslide

1. **Unified Sales Velocity & Review Aggregation for Gumroad Discover:**
   - Gumroad's organic marketplace algorithm (**Gumroad Discover**) ranks listings based on cumulative download volume, conversion rate, and total 5-star ratings attached to a **single product URL**.
   - When your `$0` Free Starter Kit, `$19` Core Book, `$39` Workbook/Atlas Edition, and `$59` Flagship OS Bundle all live inside `sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`, every single `$0` download counts toward that URL's total customer counter and allows free users to leave verified **5-star ratings** on the exact same page where `$59` buyers are making their purchasing decision.
   - Instead of having 100 reviews trapped on a `$0` page and `0 reviews` on your `$59` page, your `$59` Flagship page displays 100+ verified 5-star reviews from Day 1.
2. **Side-by-Side Decoy Pricing & Anchor Contrast on One Screen:**
   - Behavioral economics proves that buyers rarely choose the highest tier when they have to click back and forth between four separate browser tabs.
   - When all four tiers appear as radio-button **Versions** on the right side of a single product page (`$0` vs. `$19` vs. `$39` vs. `⭐ $59 MOST POPULAR`), buyers immediately see that moving from `$39` to `$59` (`+$20`) adds the **Unlocked Pro Web App (`SMALLBIZ-OS-PRO-2026`)**, the **5-Database Notion OS**, the **8-Tab Charted Excel Command Center**, and **5 Importable Make/n8n/Zapier JSON Blueprints**.
3. **1-Click Native Version-Upgrade Upsells at Checkout:**
   - Inside Gumroad's **`Checkout -> Upsells`** panel, Gumroad provides a native feature called **"Replace the version selected with another version of the same product."**
   - Whenever a visitor selects Version 1 (`$0`), Version 2 (`$19`), or Version 3 (`$39`) and clicks **"I want this!"**, Gumroad displays an instant modal offer at checkout to upgrade directly to **Version 4 (`$59` Complete Flagship OS)** with a `$10` fast-action discount.
4. **Why the VIP Membership (`$12/mo` or `$59/yr`) Must Stay on Link #2:**
   - Gumroad enforces a strict platform rule: one-time digital products (`Digital product`) and recurring billing subscriptions (`Membership`) use different checkout engines and cannot be mixed inside the same `Versions` list.
   - Therefore, keeping **Link #1 (`smallbiz-ai-automation-os`)** for all one-time tiers (`$0 / $19 / $39 / $59`) and **Link #2 (`smallbiz-automation-vault-vip`)** for your recurring VIP Membership (`$12/mo | $59/yr`), and placing a prominent upgrade link inside both descriptions and checkout upsells, gives you 100% algorithmic consolidation without violating Gumroad's billing rules.

---

## 2. Exact How-To: Setting Up Link #1 (`$0 / $19 / $39 / $59` All-in-One Product) on Gumroad

If you already created `sunnyomar.gumroad.com/l/smallbiz-ai-automation-os` (or want to edit your existing product into the Unified 4-Version Listing), enter these exact values:

### 2.1 Top Product Fields
- **Name:** `The Small Business AI Automation Operating System — Complete 5-Department Blueprint, Web App, Notion & Excel OS (By OMAR SUNNY)`
- **URL Slug:** `smallbiz-ai-automation-os` (`https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`)
- **Call to Action Button:** `I want this!`
- **Cover Carousel (`1280×720` / `1600×1200` Horizontal Images — Upload in This Order):**
  1. `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/05-gumroad-tier3-flagship-bundle-cover-1280x720.png`
  2. `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/04-gumroad-tier2-workbook-edition-cover-1280x720.png`
  3. `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/03-gumroad-tier0-free-audit-cover-1280x720.png`
  4. `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/slide-scene-06-layer2-interactive-saas-webapp.png`
  5. `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/slide-scene-07-layer3-notion-excel-command.png`
- **Square Thumbnail (`600×600 px` `1:1`):**
  - Upload: `08-COVER-DESIGN/12-gumroad-square-thumb-listing2-flagship-os-600x600.png`

### 2.2 Base Pricing & The 4 Versions Setup (`$0 / $19 / $39 / $59`)
1. Scroll to the **Pricing** section on the Product tab:
   - **Amount (`$ US Dollars`):** Enter **`0`**
   - **Allow customers to pay what they want:** Toggle **ON** -> Set **Minimum amount:** `0` | **Suggested amount:** `0`. *(Note: In Gumroad, when Base Price is `$0`, any Version with an `Additional amount` of `+$19`, `+$39`, or `+$59` automatically charges the exact `$19`, `$39`, or `$59` price, while Version 1 with `+$0` remains `$0` Free!)*
2. Scroll to the **Versions** section and click **`Add version`** 4 times to create these exact 4 tiers:

| Version # | Exact Version Name | Exact Version Description | Additional Amount | Final Checkout Price | File Assigned in `Content` Tab |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Version 1** | `Tier 0: Free 5-Day Time & Lead-Leak Audit Starter Kit ($0)` | `Complimentary diagnostic starter pack: 32-Page Chapter 1 + Fillable Audit Workbook PDF (64 fields), Offline ROI Simulator Web App (Diagnostic Mode), 5-Dept ROI CSV, Prompts 1.1–1.5 & Emergency Script 01.` | `+$0` | **`$0` (Free)** | `Tier0-Free-5Day-Audit-Starter-Kit.zip` |
| **Version 2** | `Tier 1: Complete 10-Chapter Book & Print Edition Pack ($19)` | `Full 111,905-word operational manual: 179-Page US Letter Digital Book PDF + Validated Reflowable EPUB 3.0 + 242-Page 6"x9" Print Paperback Interior PDF. Includes all 50 AI Prompts, 12 Crisis Scripts & 20 Diagrams.` | `+$19` | **`$19`** | `Tier1-KDP-and-D2D-Retail-Book-Pack.zip` |
| **Version 3** | `Tier 2: Interactive Workbooks, Visual Atlas & iPad Planner ($39)` | `Everything in Tier 1 PLUS: 80-Page US Letter & 76-Page ISO A4 Fillable Workbooks (312 interactive fields), 47-Page Landscape Tablet Planner, 24-Page Visual Shortcut Atlas & 11 Printable Department Cheat Sheets.` | `+$39` | **`$39`** | `Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip` |
| **Version 4** | `⭐ Tier 3: Complete Flagship AI Automation OS Bundle — MOST POPULAR ($59)` | `Everything in Tier 2 PLUS: Full Pro Offline Web App (Key: SMALLBIZ-OS-PRO-2026) + 5-DB Notion OS Kit + 8-Tab Charted Excel Command Center (.XLSX) + 5 Importable Make.com, n8n & Zapier JSON Workflow Blueprints.` | `+$59` | **`$59`** | `Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip` |

### 2.3 How to Assign Each ZIP File to Its Matching Version in the `Content` Tab
When you click **`Save and continue`** to move to the **`Content`** tab on Gumroad:
1. In the left sidebar of the **`Content`** tab, Gumroad shows a dropdown or list of your **4 Versions**.
2. Select **`Tier 0: Free 5-Day Time & Lead-Leak Audit Starter Kit ($0)`** -> Upload `09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip`.
3. Select **`Tier 1: Complete 10-Chapter Book & Print Edition Pack ($19)`** -> Upload `09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Retail-Book-Pack.zip`.
4. Select **`Tier 2: Interactive Workbooks, Visual Atlas & iPad Planner ($39)`** -> Upload `09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip`.
5. Select **`⭐ Tier 3: Complete Flagship AI Automation OS Bundle — MOST POPULAR ($59)`** -> Upload `09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip` and add the Pro Access Key note:
   `Your Pro Web Companion Application License Key is: SMALLBIZ-OS-PRO-2026`

---

## 3. Exact Copy-Paste Product Summary, Additional Details & Refund Policy

### 3.1 Product Summary (For Link #1 — Main Unified Listing)
```text
Deploy a deterministic, human-in-the-loop AI Operating System across all 5 core departments of your 1–25 person business. Choose the $0 Free 5-Day Audit Kit or upgrade to the Complete Flagship OS Bundle (Book + Workbooks + Pro Web App + 5-DB Notion OS + 8-Tab Excel + 5 JSON Blueprints). By OMAR SUNNY.
```

### 3.2 Additional Details (8 `Attribute : Value` Rows for Link #1)
1. `System Architect` : `OMAR SUNNY`
2. `Edition` : `2026 Enterprise Operations Edition`
3. `Core Manuscript` : `10 Chapters • 50 AI Prompts • 12 Crisis Scripts`
4. `Interactive Workbooks` : `US Letter + ISO A4 + Landscape iPad (406 Fields)`
5. `Pro Web Companion App` : `100% Offline HTML5 App (Key: SMALLBIZ-OS-PRO-2026)`
6. `Notion & Excel Command` : `5 Notion CSV Databases + 8-Tab Charted Excel (.XLSX)`
7. `No-Code Blueprints` : `5 Importable JSON Workflows (Make.com, n8n, Zapier)`
8. `Refund Guarantee` : `30-Day Money-Back Guarantee`

### 3.3 Refund Policy Setting
- Toggle **`Specify a refund policy for this product`** ON.
- Select **`30-day money back guarantee`** from the dropdown.
- In **`Fine print (optional)`**, paste:
  ```text
  If you deploy the 5-Day Manual Friction Audit and do not identify at least 10 hours per week of recoverable administrative time within 30 days, email your receipt for a full 100% refund.
  ```

---

## 4. Gumroad Discover Category & 5 High-Traffic Tags (`Share` Tab)

Once you publish your product and land on the **`Share`** tab, configure **Gumroad Discover** as follows:

### For Link #1 (`smallbiz-ai-automation-os`):
- **Category:** `Business & Money > Management & Leadership` *(or `Business & Money > Small Business & Entrepreneurship`)*
- **Tags (Maximum 5 Tags Allowed by Gumroad — Enter Exactly These 5):**
  1. `small business`
  2. `ai automation`
  3. `notion template`
  4. `chatgpt prompts`
  5. `business operations`
- **Toggle ON:** `Display your product's 1-5 star rating to prospective customers`
- **Toggle ON:** `This product contains content meant only for adults?` -> Keep **OFF**.

### For Link #2 (`smallbiz-automation-vault-vip` — VIP Membership):
- **Category:** `Business & Money > Small Business & Entrepreneurship`
- **Tags (5 Tags):**
  1. `sop templates`
  2. `workflow automation`
  3. `business systems`
  4. `ai prompts`
  5. `agency operations`
"""
    content = sanitize_text(content)
    (GUMROAD_DIR / "00-UNIFIED-2-LINK-MASTER-STRATEGY-AND-LOCKED-SETUP.md").write_text(content, encoding="utf-8")
    return len(content.split())


def write_guide_01_listing_1() -> int:
    content = r"""# Gumroad Listing 1 Master Playbook: Free 5-Day Time & Lead-Leak Audit Starter Kit (`$0+` Lead Magnet)
## Project: "The Small Business AI Automation Operating System" (System Architect: OMAR SUNNY)
**Target URL Slug:** `https://sunnyomar.gumroad.com/l/smallbiz-ai-audit-kit`  
**Unified Alternative:** Can also be hosted as **Version 1 (`$0`)** inside `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`  
**Primary Archive Uploaded:** `09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip`  

---

## 1. Strategic Role of Listing 1 in the Hybrid Funnel

Listing 1 serves as your zero-friction top-of-funnel customer acquisition engine. Over 85% of cold social media viewers from LinkedIn, YouTube, Facebook Reels, and TikTok will not purchase a `$59` B2B system on their first visit—but they will gladly download a high-value **`$0` 5-Day Time & Lead-Leak Audit Starter Kit** when they see it includes a 32-page fillable diagnostic book, an offline browser ROI calculator, and 5 copy-ready AI workflow prompts.

The moment a founder enters their email address to claim this `$0` kit:
1. They are added to your permanent Gumroad customer database.
2. Gumroad immediately displays **Checkout Upsell #1** offering an instant `$10 OFF` upgrade to the `$59` Flagship Operating System Bundle.
3. Gumroad's automated **7-Email Conversion Sequence (`Workflows`)** nurtures them over the next 14 days toward the `$59` Flagship Bundle (`https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`) and the `$12/mo | $59/yr` VIP Living Automation Vault Membership (`https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`).

---

## 2. Field-by-Field Gumroad Product Tab Configuration

Copy and paste the exact values below into your Gumroad Product Editor:

| Gumroad Field | Exact Value to Enter |
| :--- | :--- |
| **Product Type** | `Digital product` |
| **Name** | `The 5-Day Small Business Time & Lead-Leak Audit Starter Kit — Free AI Automation Rescue Pack (By OMAR SUNNY)` |
| **URL Slug (`sunnyomar.gumroad.com/l/...`)** | `smallbiz-ai-audit-kit` |
| **Base Price (`$ US Dollars`)** | `0` |
| **Allow customers to pay what they want** | `ON` -> **Minimum amount:** `$0` \| **Suggested amount:** `$5` (or `$0`) |
| **Call to Action Button** | `I want this!` |
| **Square Thumbnail (`600×600 px` `1:1`)** | `08-COVER-DESIGN/11-gumroad-square-thumb-listing1-free-audit-600x600.png` |
| **Cover Banner (`1280×720 px` `16:9`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/03-gumroad-tier0-free-audit-cover-1280x720.png` |
| **Refund Policy** | `30-day money back guarantee` |

---

## 3. Summary & Additional Details Callout Attributes

### 3.1 Summary Field (Shown Directly Under the "I want this!" Button)
```text
Quantify your Annual Cost of Manual Friction (CMF) in 15 minutes and deploy your first 60-second lead-response workflow this week. Includes the 32-Page Chapter 1 + Fillable Audit Workbook PDF, Offline ROI Calculator Web App (.HTML), 5-Dept ROI Spreadsheet (.CSV), Prompts 1.1–1.5, and Emergency Script 01. By OMAR SUNNY.
```

### 3.2 Additional Details (`Add detail` — 5 Exact Attribute : Value Pairs)
- **Row 1:** `Author` -> `OMAR SUNNY`
- **Row 2:** `Edition` -> `2026 Enterprise Diagnostic Starter Kit`
- **Row 3:** `Formats Included` -> `Fillable PDF (32 Pages) + Offline HTML5 Web App + CSV`
- **Row 4:** `AI Prompts Included` -> `Prompts 1.1 to 1.5 + Red-Gate Emergency Script 01`
- **Row 5:** `License` -> `100% Free Commercial Diagnostic Use`

---

## 4. Full Copy-Paste Product Description (With Direct Links to Flagship OS & VIP Membership)

Paste the complete description below into the **Description** editor on Gumroad:

```text
Stop losing 15+ hours every week to evening paperwork, missed customer calls, and overdue invoices.

Most 1-to-25 person businesses lose 20% to 35% of their potential net profit to the three silent killers of small business growth:
1. Inbound leads that go cold because nobody replied within 5 minutes (78% of customers buy from the first business that responds).
2. Hours of repetitive copy-pasting between email, spreadsheets, CRM, scheduling apps, and invoicing software.
3. Completed jobs and projects that sit unbilled or unpaid for 40+ days.

This 100% Free "5-Day Small Business Time & Lead-Leak Audit Starter Kit" (authored by Systems Architect OMAR SUNNY) gives you the exact diagnostic engine from Chapter 1 of "The Small Business AI Automation Operating System" so you can calculate your hidden profit leaks in 15 minutes flat and deploy your first 60-second workflow this week—without writing code or hiring extra staff.

────────────────────────────────────────────────────────────
WHAT YOU GET IMMEDIATELY INSIDE THIS FREE STARTER KIT (.ZIP)
────────────────────────────────────────────────────────────

1. Chapter 1 + Fillable 5-Day Audit Workbook PDF (32 Pages, 64 Interactive AcroForm Fields)
Read the complete Chapter 1 operational blueprint ("The Owner's Bottleneck — Mapping the 5-Department Automation Engine") plus the standalone 14-page Fillable Chapter 1 Action Workbook. Type directly into the PDF fields on your laptop or print it for your leadership team.

2. Interactive Offline SaaS-Lite ROI & Lead-Leak Simulator Web App (smallbiz-automation-os-app.html)
Double-click to open in Chrome, Edge, Safari, or Firefox—100% offline with zero cloud sign-up required. Enter your weekly admin hours, monthly lead volume, and average customer value to compute your exact Annual Cost of Manual Friction (CMF) across Labor Waste, Leaked Lead Revenue, and Cashflow Drag, and rank your highest-ROI quick wins using the P.A.C.E. Prioritization Matrix.

3. 5-Department Automation ROI & Lead-Leak Calculator Spreadsheet (.CSV)
Pre-configured with side-by-side benchmarks for a $250K Solo Business, an $850K Local Clinic/Home-Service Contractor, and a $2.4M Multi-Crew Agency—ready to open in Microsoft Excel, Google Sheets, or Notion.

4. 5 Production-Tested AI Workflow Prompts (Prompts 1.1 to 1.5)
• Prompt 1.1: 5-Department Manual Friction & Bottleneck Auditor
• Prompt 1.2: Speed-to-Lead Revenue Leak & Decay Quantifier
• Prompt 1.3: P.A.C.E. Automation Priority Matrix Ranker
• Prompt 1.4: Week-1 Quick-Win Workflow Architecture Specifier
• Prompt 1.5: Team Automation Readiness & Change-Management Briefing Generator

5. Red-Gate Emergency Operations Script 01 (Executive Customer Takeover)
Synchronized Email + 160-character SMS + Internal Slack Escalation template to halt automation and recover a high-value frustrated client within 15 minutes.

6. Printable 1-Page Executive Cheat Sheet #01 (PDF)
Laminated-ready desk reference summarizing the 5-Department Engine, the Master CMF Formula, and the P.A.C.E. scoring rules.

────────────────────────────────────────────────────────────
READY FOR THE COMPLETE 5-DEPARTMENT OPERATING SYSTEM?
────────────────────────────────────────────────────────────

Once you complete your 5-Day Audit, upgrade to the full commercial editions anytime:

👉 GET THE COMPLETE FLAGSHIP AI AUTOMATION OS BUNDLE ($19 / $39 / $59):
https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os
(Includes all 10 Chapters, 50 Tested AI Prompts, 12 Emergency Scripts, Fillable US Letter/A4/iPad Workbooks, Unlocked Pro Web Companion App [Key: SMALLBIZ-OS-PRO-2026], 5-Database Notion OS Kit, 8-Tab Charted Excel Command Center, and 5 Importable Make.com / n8n / Zapier JSON Blueprints.)

👉 JOIN THE VIP LIVING AUTOMATION VAULT & EDITABLE OFFICE SUITE ($12/mo or $59/yr):
https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip
(Includes everything in the Flagship OS Bundle PLUS 7 Editable Microsoft Word [.DOCX] SOP Manuals, 3 Editable PowerPoint [.PPTX] Team Training Slide Decks, the Interactive Design Customizer Studio, and Monthly Industry Automation Drops for Clinics, Contractors, and Agencies.)

Enter $0 in the price box on this page and click "I want this!" to download your Free Starter Kit now.
```

---

## 5. Content Tab, Receipt Customization & Discover Settings for Listing 1

### 5.1 Content Tab Setup (`Upload files` + Welcome Instructions)
1. Upload the verified archive: `09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip` (`3.86 MB`).
2. Paste this welcome guide above the download button in the Gumroad Content Editor:

```text
Welcome to The Small Business AI Automation Operating System Starter Kit (By OMAR SUNNY)!

HOW TO START YOUR 15-MINUTE AUDIT RIGHT NOW:
1. Click the Download button to save "Tier0-Free-5Day-Audit-Starter-Kit.zip" to your computer and extract (unzip) the folder.
2. Open "07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html" in any web browser to run your live Cost of Manual Friction (CMF) & ROI Diagnostic.
3. Open "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf" (32 pages) or "05-WORKBOOKS/chapter-01-workbook.pdf" (14 pages) to log your 5-Day Time & Lead-Leak Audit.

WANT TO ACTIVATE ALL 50 AI PROMPTS, 12 EMERGENCY SCRIPTS, NOTION OS & 8-TAB EXCEL COMMAND CENTER?
Use fast-action coupon code AUDIT10 for $10 OFF the Complete Flagship AI Automation OS Bundle here:
https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os

Or join the VIP Living Automation Vault & Editable Word/PowerPoint Office Suite ($12/mo or $59/yr):
https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip
```

### 5.2 Receipt Email Tab Customization (`Receipt` Tab)
When a founder downloads your `$0` Starter Kit, Gumroad sends an automatic receipt email. Customize the **Receipt** tab fields as follows:
- **Button Text:** `Access Your 5-Day AI Audit Kit`
- **Custom Receipt Note:**
  ```text
  Thank you for downloading The 5-Day Small Business Time & Lead-Leak Audit Starter Kit by OMAR SUNNY! Open "smallbiz-automation-os-app.html" inside your ZIP archive to calculate your Annual Cost of Manual Friction (CMF) in 15 minutes. Whenever you are ready to unlock all 50 AI Prompts, 12 Crisis Scripts, the 5-Database Notion OS, and the 8-Tab Excel Command Center, use code AUDIT10 for $10 OFF at https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os
  ```

### 5.3 Share Tab & Gumroad Discover Settings
- **Category:** `Business & Money > Small Business & Entrepreneurship`
- **5 Discover Tags:** `small business`, `ai automation`, `business audit`, `chatgpt prompts`, `productivity tools`
- **Show Product Rating:** Toggle `ON`.
- **Social Share Copy for LinkedIn, X/Twitter & Facebook Groups:**
  ```text
  Most 1–25 person businesses lose $35,000+ a year to missed phone calls, slow quote follow-ups, and evening spreadsheet chaos. I just released the Free 5-Day Small Business Time & Lead-Leak Audit Starter Kit (32-Page Fillable Audit PDF + Offline HTML5 ROI Calculator + 5 AI Prompts). Grab it for $0 here: https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os
  ```

### 5.4 Pre-Publish Quality Assurance Checklist for Listing 1
1. Confirm the `Tier0-Free-5Day-Audit-Starter-Kit.zip` file is attached under the `Content` tab and downloads cleanly in an incognito browser tab.
2. Confirm the `600x600` square thumbnail (`11-gumroad-square-thumb-listing1-free-audit-600x600.png`) is uploaded in the `Thumbnail` slot so your listing looks razor-sharp inside Gumroad Discover and the user's Gumroad Library.
3. Confirm both upgrade URLs (`https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os` and `https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`) are clickable inside the Description and Content page.
"""
    content = sanitize_text(content)
    (GUMROAD_DIR / "01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md").write_text(content, encoding="utf-8")
    return len(content.split())


def write_guide_02_listing_2() -> int:
    content = r"""# Gumroad Listing 2 Master Playbook: The Complete Flagship Small Business AI Automation Operating System (Unified Multi-Version Storefront)
## Project: "The Small Business AI Automation Operating System" (System Architect: OMAR SUNNY)
**Target URL Slug:** `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`  
**Supported Version Architectures:**  
- **Architecture A (Recommended Unified 4-Version Listing):** `$0` (Tier 0 Free Audit) / `$19` (Tier 1 Book Pack) / `$39` (Tier 2 Workbooks & Atlas) / `$59` (Tier 3 Flagship Complete OS Bundle)  
- **Architecture B (3-Version Paid Listing):** `$19` (Tier 1) / `$39` (Tier 2) / `$59` (Tier 3) *(or `$19` / `$29` / `$49`)*  

---

## 1. Strategic Architecture of Listing 2 (Your Main Revenue Engine)

Listing 2 (`https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`) is the centerpiece of your digital publishing studio. By hosting your product tiers inside this single canonical URL using Gumroad's native **Versions** selector:
1. Every customer download and 5-star review accumulates on a single powerhouse product page, maximizing your **Gumroad Discover** ranking velocity.
2. Buyers see a crystal-clear side-by-side comparison showing why **Tier 3 (`$59` Complete Flagship AI Automation OS Bundle)** delivers 10x more operational value for just `$20` more than the mid-tier workbook edition.
3. You can link directly to any specific version using Gumroad's `?option=` query parameter while still keeping all social proof unified.

---

## 2. Exact Field-by-Field Product Tab Setup

| Gumroad Field | Exact Value to Enter |
| :--- | :--- |
| **Product Type** | `Digital product` |
| **Name** | `The Small Business AI Automation Operating System — Complete 5-Department Blueprint, Web App, Notion & Excel OS (By OMAR SUNNY)` |
| **URL Slug (`sunnyomar.gumroad.com/l/...`)** | `smallbiz-ai-automation-os` |
| **Base Price (`$ US Dollars`)** | Set to `0` (if including the `$0` Tier 0 Starter Kit as Version 1) OR `19` (if starting at Tier 1 `$19` and keeping `$0` on `smallbiz-ai-audit-kit`) |
| **Purchasing Power Parity (PPP)** | Toggle `ON` inside Settings (`40% maximum discount` for emerging markets while preserving 100% full price in US, UK, Canada, Australia & EU) |
| **Call to Action Button** | `I want this!` |
| **Square Thumbnail (`600×600 px` `1:1`)** | `08-COVER-DESIGN/12-gumroad-square-thumb-listing2-flagship-os-600x600.png` |
| **Multi-Slide Cover Carousel (`1280×720 px` `16:9`)** | Upload in order: (1) `05-gumroad-tier3-flagship-bundle-cover-1280x720.png`, (2) `04-gumroad-tier2-workbook-edition-cover-1280x720.png`, (3) `slide-scene-06-layer2-interactive-saas-webapp.png`, (4) `slide-scene-07-layer3-notion-excel-command.png`, (5) `slide-scene-09-layer5-nocode-make-n8n-zapier.png` |
| **Refund Policy** | `30-day money back guarantee` |

---

## 3. Summary & 8 Additional Details (`Attribute : Value` Pairs)

### 3.1 Summary Field
```text
Complete 5-Department AI Operating System for 1–25 person businesses: 179-Page Flagship Book (PDF + EPUB + Print), Fillable Workbooks (406 Fields), Unlocked Pro Offline Web App (Key: SMALLBIZ-OS-PRO-2026), 5-Database Notion OS, 8-Tab Charted Excel Command Center & 5 Make/n8n/Zapier JSON Blueprints. By OMAR SUNNY.
```

### 3.2 Additional Details (Click `Add detail` 8 Times)
1. `System Architect` : `OMAR SUNNY`
2. `Edition` : `2026 Enterprise Operations Edition`
3. `Core Manuscript` : `10 Chapters • 50 AI Workflow Prompts • 12 Crisis Scripts`
4. `Fillable Workbooks` : `US Letter (80p) + ISO A4 (76p) + iPad Planner (47p)`
5. `Pro Web Companion App` : `100% Offline HTML5 App (Key: SMALLBIZ-OS-PRO-2026)`
6. `Notion & Excel OS` : `5 Notion Databases (.CSV) + 8-Tab Charted Excel (.XLSX)`
7. `No-Code Blueprints` : `5 Importable JSON Workflows (Make.com, n8n, Zapier)`
8. `Guarantee` : `30-Day 100% Money-Back Guarantee`

---

## 4. Full Copy-Paste Product Description (Including Tier Comparison Table & VIP Membership Link)

Paste the complete rich-text description below into Gumroad's **Description** editor:

```text
Stop drowning in evening paperwork, missed customer calls, and overdue invoices. Install a deterministic, human-in-the-loop AI Operating System across your entire 1-to-25 person business in 90 days—without hiring extra administrative staff or writing complex code.

Most small business owners lose 20% to 35% of their potential net profit to the three silent killers of small business growth:
• Leaked Lead Revenue: Inbound inquiries from web forms, missed calls, WhatsApp, and social DMs that go cold because nobody replied within 5 minutes.
• Manual Admin Labor Tax: 15 to 25 hours a week spent copying and pasting data between email, spreadsheets, scheduling tools, and accounting software.
• Receivables & Cashflow Drag: Completed work that sits unbilled for days or unpaid for 40+ days because nobody follows up consistently.

Generic "prompt packs" fail in real businesses because unguarded chatbots invent prices, hallucinate policies, and damage hard-earned local reputations.

Authored by Systems Architect OMAR SUNNY, "The Small Business AI Automation Operating System" gives founders, clinic directors, home-service contractors, e-commerce operators, and B2B agency leaders a complete, production-tested 5-Department Operating System built on the T.R.A.V. (Trigger -> Rules -> AI -> Verification) safety architecture.

────────────────────────────────────────────────────────────
THE 10-CHAPTER ENTERPRISE OPERATIONS BLUEPRINT (111,905 WORDS)
────────────────────────────────────────────────────────────

• Chapter 1 — The 5-Day Manual Friction Audit: Quantify your exact Annual Cost of Manual Friction (CMF) across Labor Waste, Leaked Lead Revenue, and Cashflow Drag, and prioritize your highest-ROI workflows using the P.A.C.E. Matrix.
• Chapter 2 — The Human-in-the-Loop T.R.A.V. Safety Gate: Separate deterministic SKU pricing math from AI drafting using Green Gates (75% unattended 24/7 execution), Amber Gates (15-second Slack/Teams thumb approval for custom quotes), and Red Gates (immediate human takeover).
• Chapter 3 — The 60-Second Speed-to-Lead Router: Capture website forms, missed phone calls, voicemails, WhatsApp messages, Facebook/IG Lead Ads, and Google Business messages into a unified router that texts back and books appointments in under 60 seconds.
• Chapter 4 — 3-Option Good-Better-Best Proposals & The 14-Day Follow-Up Loop: Turn a 90-second post-visit voice note into a polished 3-tier quote PDF and automate polite, multi-channel follow-ups that stop the millisecond the client signs.
• Chapter 5 — Frictionless Zero-Drop Client Onboarding: Wire Stripe, Square, and QuickBooks deposit webhooks to instant welcome packets, cloud folder provisioning, conditional intake validation, and scope-creep early warnings.
• Chapter 6 — 24/7 Grounded RAG Customer Support: Resolve 60%+ of routine Tier-1 tickets (hours, parking, WISMO order status, rescheduling) with zero hallucination while escalating frustrated customers (Sentiment 1 or 2) to a human immediately.
• Chapter 7 — The 5-Star Review & Repeat-Sales Flywheel: Send a 1-click sentiment check at the peak moment of gratitude—routing happy clients to Google Reviews and waking up 60/90/180-day dormant customers automatically.
• Chapter 8 — Automated Invoicing, 5-Stage A/R Chasers & Receipt OCR: Compress Days Sales Outstanding (DSO) from 42 days down to 12 days with same-day billing, relationship-safe overdue reminders, and automated 5% vendor price-creep detection.
• Chapter 9 — The Self-Running Team & Living SOP Engine: Convert 3-minute screen recordings into 7-block Standard Operating Procedures, delegate tasks by voice memo, and deploy an internal "Ask-the-SOP" bot for your staff.
• Chapter 10 — The 15-Minute Friday Owner Scorecard & 90-Day Rollout: Review your entire company every Friday at 3:00 PM across 12 Core KPIs in 15 minutes flat.

────────────────────────────────────────────────────────────
COMPLETE DELIVERABLES INSIDE THE FLAGSHIP OS BUNDLE (TIER 3)
────────────────────────────────────────────────────────────

1. Complete Multi-Format Book Suite (PDF + EPUB 3.0 + Print Edition)
• 179-Page US Letter Full-Color Flagship Digital Book PDF
• 242-Page 6"x9" Trade Paperback Print Edition PDF
• Validated Reflowable EPUB 3.0 for Kindle, Apple Books, Kobo & Tablets
• All 50 Tested AI Workflow Prompts (Prompts 1.1–10.5), 12 Red-Gate Emergency Operations Scripts & 20 Vector Architecture Diagrams

2. Interactive Fillable Action Workbooks, Visual Atlas & Cheat Sheets
• 80-Page US Letter Fillable Action Workbook PDF (160 interactive AcroForm fields)
• 76-Page International ISO A4 Fillable Action Workbook PDF (152 interactive fields)
• 47-Page Landscape Interactive Tablet Planner PDF (94 fields + clickable 7-tab navigation for iPad/GoodNotes/reMarkable)
• 24-Page Visual Shortcut Atlas PDF + 11 Printable 1-Page Department Cheat Sheets

3. Unlocked Pro Offline SaaS-Lite Web Companion Application (smallbiz-automation-os-app.html)
• Runs 100% offline in any desktop or mobile browser (zero subscription fees, 100% local privacy)
• Includes Commercial Pro Activation Key: SMALLBIZ-OS-PRO-2026
• 6 Interactive Modules: (1) Live CMF & ROI Simulator, (2) P.A.C.E. Priority Matrix Builder, (3) 50-Prompt Interactive Customizer & Variable Injector, (4) 12 Red-Gate Emergency Script Generator, (5) 90-Day Rollout Checklist Tracker, and (6) 1-Click JSON State Backup & Restore

4. The 5-Database Minimalist Notion Small Business OS Kit
• DB 01: Inbound Leads & 60-Second Speed-to-Lead CRM (26 pre-loaded records)
• DB 02: Automation Workflows & Health Registry (27 active pipeline specs)
• DB 03: Complete 62-Item AI Prompt & Emergency Script Vault
• DB 04: Longitudinal 12-Week Friday 3:00 PM Owner KPI Scorecard
• DB 05: Customer Support Grounded RAG Policy & Escalation Hub (POL-01 to POL-21)
• Includes the 2,400-word Notion Setup & Formula 2.0 Copy-Paste Engineering Guide

5. 8-Tab Formula-Driven Microsoft Excel Command Center (.XLSX)
• Native Excel workbook (`SmallBiz-AI-Automation-OS-Command-Center.xlsx`) with live formulas and embedded native charts across 8 tabs: Executive Dashboard, CMF & ROI Calculator, Speed-to-Lead SLA Tracker, 3-Tier Quote Margin Model, AR Cashflow & DSO Chaser Tracker, 62-Item Prompt Vault, 90-Day Gantt Rollout, and 12-Week Friday Owner Scorecard.

6. 5 Importable Make.com, n8n & Zapier JSON Automation Blueprints
• Blueprint 01: 60-Second Omnichannel Speed-to-Lead & Missed-Call SMS Router
• Blueprint 02: Voice-Note to 3-Tier Proposal & 14-Day Follow-Up Engine
• Blueprint 03: Grounded RAG Customer Support Triage & Red-Gate Escalation Router
• Blueprint 04: Same-Day Milestone Invoicing & 5-Stage Overdue A/R Chaser
• Blueprint 05: Friday 3:00 PM 12-KPI Owner Scorecard Synthesizer
• Includes the 2,450-word No-Code Webhook, API & JSON Import Setup Guide

────────────────────────────────────────────────────────────
WHICH VERSION SHOULD YOU CHOOSE ON THIS PAGE?
────────────────────────────────────────────────────────────

• Tier 0 ($0 Free Starter Kit): Chapter 1 + Fillable Audit Workbook PDF (32p), Diagnostic Mode Web App, 5-Dept ROI CSV, Prompts 1.1–1.5 & Emergency Script 01.
• Tier 1 ($19 Core Book Pack): Complete 179-Page Flagship Digital Book PDF + EPUB 3.0 + 242-Page Print Edition (all 10 Chapters, 50 Prompts & 12 Scripts).
• Tier 2 ($39 Interactive Workbook & Atlas Edition): Everything in Tier 1 + US Letter & A4 Fillable Workbooks (312 fields), 47-Page iPad Landscape Planner, 24-Page Visual Shortcut Atlas & 11 Printable Desk Cheat Sheets.
• ⭐ Tier 3 ($59 Complete Flagship AI Automation OS Bundle — MOST POPULAR): Everything in Tier 2 + Unlocked Pro Web Companion App (Key: SMALLBIZ-OS-PRO-2026) + 5-Database Notion OS Kit + 8-Tab Charted Excel Command Center (.XLSX) + 5 Importable Make/n8n/Zapier JSON Workflow Blueprints.

────────────────────────────────────────────────────────────
WANT EDITABLE WORD (.DOCX) SOPs, POWERPOINT (.PPTX) DECKS & MONTHLY INDUSTRY DROPS?
────────────────────────────────────────────────────────────

👉 JOIN THE VIP LIVING AUTOMATION VAULT & EDITABLE OFFICE SUITE MEMBERSHIP ($12/mo or $59/yr):
https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip
Includes 100% of the Tier 3 Flagship OS Bundle PLUS 7 Editable Microsoft Word (.DOCX) SOP Manuals, 3 Editable PowerPoint (.PPTX) Team Training Slide Decks, the Interactive Design Customizer Studio (6 Color Themes), and Monthly Industry-Specific Automation Drops (Dental/Medical Clinics, HVAC/Home Services & B2B Agencies).

Select your preferred version on the right and click "I want this!" for instant download access.
```

---

## 5. Exact "Versions" Section Configuration (`Product` Tab -> `Versions`)

### 5.1 Unified 4-Version Configuration (Base Price = `$0`)
If you use the Unified 2-Link Strategy where `$0`, `$19`, `$39`, and `$59` all live on `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`, set **Base Price = `$0`** (`Allow customers to pay what they want = ON`, Minimum `$0`, Suggested `$0`) and add these 4 Versions:

#### Version 1 (`$0` Total):
- **Name:** `Tier 0: Free 5-Day Time & Lead-Leak Audit Starter Kit ($0)`
- **Description:** `Complimentary Starter Kit: 32-Page Chapter 1 + Fillable Audit Workbook PDF, Offline ROI Calculator Web App (Diagnostic Mode), 5-Dept ROI CSV, Prompts 1.1–1.5 & Emergency Script 01.`
- **Additional amount:** `0`
- **Content Tab File:** `09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip`

#### Version 2 (`$19` Total):
- **Name:** `Tier 1: Core 10-Chapter Book & Print Edition Pack ($19)`
- **Description:** `Complete 179-Page Flagship Digital Book (PDF) + Validated Reflowable EPUB 3.0 + 242-Page 6"x9" Print Edition. Includes all 10 Chapters, 50 Tested AI Prompts, 12 Emergency Scripts & 20 Vector Diagrams.`
- **Additional amount:** `19`
- **Content Tab File:** `09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Retail-Book-Pack.zip`

#### Version 3 (`$39` Total):
- **Name:** `Tier 2: Interactive Workbooks, Visual Atlas & iPad Planner ($39)`
- **Description:** `Everything in Tier 1 PLUS: US Letter (80p) & ISO A4 (76p) Fillable Action Workbooks (312 Form Fields), 47-Page Landscape iPad/Tablet Planner, 24-Page Visual Shortcut Atlas PDF & 11 Printable Department Cheat Sheets.`
- **Additional amount:** `39`
- **Content Tab File:** `09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip`

#### Version 4 (`$59` Total — Hero Tier):
- **Name:** `⭐ Tier 3: Complete Flagship AI Automation OS Bundle — MOST POPULAR ($59)`
- **Description:** `Complete Commercial Operating System: Everything in Tier 2 + Full Pro Offline Web App (Key: SMALLBIZ-OS-PRO-2026) + 5-Database Notion OS Kit + 8-Tab Charted Excel Command Center (.XLSX) + 5 Importable Make.com, n8n & Zapier JSON Automation Blueprints.`
- **Additional amount:** `59`
- **Content Tab File:** `09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip`

*(Note: If you keep Listing 1 `$0` as a separate product at `/l/smallbiz-ai-audit-kit` and only put the 3 paid tiers on `/l/smallbiz-ai-automation-os`, set **Base Price = `$19`** and set Version 1 Additional Amount = `+$0` [`$19`], Version 2 Additional Amount = `+$20` [`$39`], and Version 3 Additional Amount = `+$40` [`$59`].)*

---

## 6. Content Tab Per-Version Delivery Instructions & Pro License Key Block

Inside the **`Content`** tab of Gumroad, paste this exact delivery block above the file download card for **Version 4 (`⭐ Tier 3: Complete Flagship AI Automation OS Bundle — $59`)**:

```text
Welcome to The Small Business AI Automation Operating System — Flagship Commercial Edition (By OMAR SUNNY)!

────────────────────────────────────────────────────────────
YOUR PRO WEB COMPANION APPLICATION LICENSE KEY
────────────────────────────────────────────────────────────
License Key: SMALLBIZ-OS-PRO-2026

HOW TO UNLOCK YOUR PRO WEB APP (100% OFFLINE):
1. Download and unzip "Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip".
2. Open "07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html" in Chrome, Edge, Safari, or Firefox.
3. Click "Unlock Pro OS" in the top navigation bar and paste your key: SMALLBIZ-OS-PRO-2026
4. All 50 AI Workflow Prompts, all 12 Red-Gate Emergency Scripts, the 90-Day Rollout Tracker, and JSON State Export/Import are now permanently unlocked on your device!

WHERE TO FIND YOUR FILES INSIDE THE ZIP ARCHIVE:
• 00-START-HERE-READ-FIRST.md — Complete Master Orientation & Quickstart Checklist
• 09-EXPORTS/PDF/the-smallbiz-ai-automation-os-complete-book.pdf — 179-Page Flagship Book
• 09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub — Reflowable eBook for Kindle/Apple Books
• 05-WORKBOOKS/ — US Letter (80p), ISO A4 (76p), iPad Landscape Planner (47p), Visual Atlas (24p) & 11 Cheat Sheets
• 06-NOTION-SYSTEM/ — 5 Notion CSV Databases + Formula 2.0 Setup Guide
• 13-OFFICE-EDITABLE-SUITE/Excel-Command-Center/SmallBiz-AI-Automation-OS-Command-Center.xlsx — 8-Tab Charted Excel Workbook
• 14-AUTOMATION-BLUEPRINTS/ — 5 Importable Make.com, n8n & Zapier JSON Workflows + Webhook Guide

NEED EDITABLE MICROSOFT WORD (.DOCX) SOP MANUALS & POWERPOINT (.PPTX) SLIDE DECKS FOR YOUR TEAM?
Upgrade to the VIP Living Automation Vault & Editable Office Suite ($12/mo or $59/yr) using code VIPUPGRADE for $15 OFF the annual pass:
https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip
```

---

## 7. Frequently Asked Questions (FAQ Block to Paste at Bottom of Product Description)

Adding a structured FAQ section at the bottom of your Gumroad product description increases conversion rate by addressing buyer objections before they leave the page:

```text
────────────────────────────────────────────────────────────
FREQUENTLY ASKED QUESTIONS (FAQ)
────────────────────────────────────────────────────────────

Q1: Do I need coding experience or an internal IT department to use this system?
No. Every workflow in this Operating System is designed for non-technical small business owners and operations managers (1 to 25 employees). All 50 AI prompts work in standard ChatGPT, Claude, or Gemini, the Web App and Excel Command Center run immediately on your laptop, and the 5 JSON blueprints import directly into visual no-code builders (Make.com, n8n, or Zapier).

Q2: How does this prevent AI from hallucinating prices or sending embarrassing replies to my customers?
Chapter 2 installs the deterministic T.R.A.V. (Trigger -> Rules -> AI -> Verification) architecture. AI is never allowed to calculate prices or invent policies—all pricing math is handled by deterministic lookup tables, policies are grounded strictly in your 21-policy RAG knowledge base (temperature <= 0.1), custom quotes require a 15-second Slack/Teams thumb approval (Amber Gate), and frustrated clients trigger an immediate human takeover (Red Gate).

Q3: Does the Pro Web Companion Application require a monthly SaaS subscription?
No. The interactive Web Companion Application (smallbiz-automation-os-app.html) runs 100% locally inside your web browser with zero recurring software fees and complete data privacy. Tier 3 ($59) and VIP Vault members receive the lifetime Pro License Key (SMALLBIZ-OS-PRO-2026) included.

Q4: What is the difference between the $59 Flagship OS Bundle and the $59/yr VIP Membership?
The $59 Flagship Bundle is a one-time purchase containing the complete Book Suite, Fillable Workbooks, Pro Web App, 5-Database Notion OS, 8-Tab Excel Command Center, and 5 JSON Blueprints. The VIP Membership ($12/mo or $59/yr at https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip) includes 100% of the Flagship Bundle PLUS 7 Editable Microsoft Word (.DOCX) SOP Manuals, 3 Editable PowerPoint (.PPTX) Slide Decks, the Interactive Design Customizer Studio, and Monthly Industry Automation Drops.
```
"""
    content = sanitize_text(content)
    (GUMROAD_DIR / "02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md").write_text(content, encoding="utf-8")
    return len(content.split())


def write_guide_03_listing_3() -> int:
    content = r"""# Gumroad Listing 3 Master Playbook: VIP Living Automation Vault & Editable Office Suite Membership (`$12/mo` or `$59/yr`)
## Project: "The Small Business AI Automation Operating System" (System Architect: OMAR SUNNY)
**Target URL Slug:** `https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`  
**Product Type on Gumroad:** `Membership` (Recurring Subscription)  
**Primary Archive Uploaded:** `09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Automation-Vault-Membership-Drop01.zip`  

---

## 1. Strategic Role of Listing 3 (Recurring MRR / ARR Engine)

While Listing 2 (`https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`) generates immediate one-time bundle revenue, **Listing 3 (`https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`)** builds predictable Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR).

By pricing the membership at **`$12 / month`** or **`$59 / year` (Save 59% — Default Billing Selection)** and including:
1. **100% of the Tier 3 Flagship AI Automation OS Bundle**, PLUS
2. **The 7 Editable Microsoft Word (`.DOCX`) SOP & Operations Manuals**, PLUS
3. **The 3 Editable Microsoft PowerPoint (`.PPTX`) Team Training Slide Decks**, PLUS
4. **The Interactive Design Customizer Studio (`design-customizer-studio.html`)**, PLUS
5. **Monthly Industry-Specific Automation Drops (starting with Drop #01: Dental/Medical Clinics, HVAC/Home Services, and B2B Agencies)**,

any buyer who sees the `$59` one-time Flagship Bundle on Listing 2 realizes they can join the **Annual VIP Vault for the exact same `$59/year`** and immediately receive all the editable Word/PowerPoint files, the Design Customizer Studio, and a full year of monthly industry workflow releases.

---

## 2. Exact Field-by-Field Product Tab Setup for Listing 3 (`Membership`)

| Gumroad Field | Exact Value to Enter |
| :--- | :--- |
| **Product Type** | `Membership` |
| **Name** | `Living Small Business AI Automation Vault & Editable Office Suite VIP Membership (By OMAR SUNNY)` |
| **URL Slug (`sunnyomar.gumroad.com/l/...`)** | `smallbiz-automation-vault-vip` |
| **Call to Action Button** | `Subscribe` / `I want this!` |
| **Square Thumbnail (`600×600 px` `1:1`)** | `08-COVER-DESIGN/13-gumroad-square-thumb-listing3-vip-membership-600x600.png` |
| **Cover Carousel (`1280×720 px` `16:9`)** | (1) `06-gumroad-tier4-vip-vault-cover-1280x720.png`, (2) `slide-scene-08-layer4-word-pptx-design-studio.png`, (3) `05-gumroad-tier3-flagship-bundle-cover-1280x720.png` |

---

## 3. Summary & 5 Additional Details (`Attribute : Value` Pairs)

### 3.1 Summary Field
```text
Complete Flagship AI Automation OS Bundle + 7 Editable Microsoft Word (.DOCX) SOP Manuals + 3 Editable PowerPoint (.PPTX) Training Slide Decks + Interactive Design Customizer Studio + Monthly Industry Automation Drops (Clinics, Home Services & Agencies). By OMAR SUNNY.
```

### 3.2 Additional Details (5 Rows)
1. `Editable Office Suite` : `7 Word (.DOCX) SOP Manuals + 3 PowerPoint (.PPTX) Decks`
2. `Design Studio App` : `Interactive SVG/PNG Theme Customizer (6 Palettes)`
3. `Flagship OS Included` : `Yes (Full Tier 3 OS + Pro Key SMALLBIZ-OS-PRO-2026)`
4. `Monthly Vault Drops` : `Drop #01 (Dental, HVAC & Agency Playbooks) + Monthly Releases`
5. `System Architect` : `OMAR SUNNY`

---

## 4. Full Copy-Paste Membership Description (With Cross-Link to One-Time Tiers)

```text
Get instant access to the entire Flagship Small Business AI Automation Operating System PLUS the complete Editable Microsoft Office Suite (.DOCX & .PPTX), the Interactive Design Customizer Studio, and Monthly Industry-Specific Automation Drops.

Built by Systems Architect OMAR SUNNY for founders, clinic directors, trade contractors, operations managers, and agency consultants who want white-label-ready Microsoft Word SOP manuals, editable PowerPoint staff training decks, custom-branded architecture diagrams, and fresh industry workflow blueprints every month.

────────────────────────────────────────────────────────────
EVERYTHING YOU RECEIVE IMMEDIATELY UPON JOINING (.ZIP)
────────────────────────────────────────────────────────────

1. All 7 Editable Microsoft Word (.DOCX) SOP & Operations Manuals (`13-OFFICE-EDITABLE-SUITE/Word-SOP-Manuals/`)
Customize every policy, role assignment, and checklist in Microsoft Word or Google Docs with your company name and logo:
• 01-5Day-Manual-Friction-Audit-SOP-Manual.docx
• 02-TRAV-Human-In-The-Loop-Governance-Charter.docx
• 03-Speed-To-Lead-And-3Tier-Quoting-SOP.docx
• 04-Zero-Drop-Onboarding-And-RAG-Support-Playbook.docx
• 05-Automated-Invoicing-AR-Chasers-And-OCR-Manual.docx
• 06-12-Red-Gate-Emergency-Operations-Scripts-Book.docx
• 07-Friday-Owner-Scorecard-And-90Day-Rollout-Charter.docx

2. All 3 Editable Microsoft PowerPoint (.PPTX) Executive Slide Decks (`13-OFFICE-EDITABLE-SUITE/PowerPoint-Slide-Decks/`)
Ready-to-present widescreen slide decks for your team all-hands meetings and leadership reviews:
• Deck 01: Staff AI Automation Kickoff & T.R.A.V. Safety Training Deck.pptx
• Deck 02: 5-Department Workflow Architecture & Role Handoff Blueprint.pptx
• Deck 03: Friday 15-Minute Executive KPI Review & 90-Day Rollout Board.pptx

3. Interactive Design Customizer Studio (`08-COVER-DESIGN/Design-Kit/design-customizer-studio.html`)
Open in any browser to re-skin all 20 vector architecture and decision-tree diagrams across 6 executive color themes (Executive Emerald, Midnight Sapphire, Amber Command, Royal Violet, Crimson Enterprise, and Monochrome High-Contrast Print) and export crisp PNG or SVG visuals for your internal wiki or client presentations.

4. Monthly Industry Vault Drop #01 Included (`tier4-monthly-vault-drop-01.md`)
Turnkey vertical implementation packs for three high-margin industries:
• Vertical Pack A: Dental, Medical, MedSpa & Physical Therapy Clinics (HIPAA-safe intake, insurance pre-check, no-show rescue & recall hygiene loops)
• Vertical Pack B: HVAC, Plumbing, Electrical, Roofing & Home-Service Contractors (Missed-call field whisper SMS, voice-note Good-Better-Best estimates & seasonal maintenance reactivation)
• Vertical Pack C: B2B Marketing, Web Design, Accounting & Consulting Agencies (Zero-drop Stripe deposit provisioning, scope-creep change orders & retainer renewal rate-locks)

5. 100% of the Flagship Tier 3 AI Automation Operating System Bundle Included
• Unlocked Pro Offline Web Companion App (License Key: SMALLBIZ-OS-PRO-2026)
• 5-Database Minimalist Notion OS Kit (.CSV Databases + Formula 2.0 Guide)
• 8-Tab Formula-Driven Microsoft Excel Command Center (.XLSX with native charts)
• 5 Importable Make.com, n8n & Zapier JSON Workflow Blueprints
• Complete 179-Page Flagship Digital Book PDF, 242-Page Print PDF, EPUB 3.0, US Letter/A4/iPad Fillable Workbooks (406 fields), 24-Page Visual Shortcut Atlas & 11 Printable Cheat Sheets

────────────────────────────────────────────────────────────
CHOOSE MONTHLY ($12/MO) OR ANNUAL ($59/YR — SAVE 59%)
────────────────────────────────────────────────────────────

• Monthly Membership ($12/month): Full instant download of all 100+ files + monthly new industry workflow drops. Cancel anytime in 1 click.
• Annual VIP Pass ($59/year — BEST VALUE): Pay the exact same $59 price as the one-time Flagship Bundle and get the entire Editable Word/PowerPoint Office Suite, Design Customizer Studio, and a full year of monthly workflow drops included!

(Looking for the one-time non-recurring editions or the $0 Free 5-Day Audit Starter Kit? Visit the main Operating System page here: https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os)
```

---

## 5. Exact `Tiers` & `Settings` Configuration on the Membership Page

### 5.1 `Tiers` Section (Replace `Untitled` with These Exact Values)
- **Tier Name:** `VIP Living Automation Vault + Editable Office Suite Access`
- **Tier Description:** `Instant download of the complete Flagship AI Automation OS Bundle (Key: SMALLBIZ-OS-PRO-2026) + 7 Editable Word (.DOCX) SOP Manuals + 3 PowerPoint (.PPTX) Training Decks + Interactive Design Customizer Studio + Monthly Industry Automation Drops.`
- **Maximum number of active supporters:** Leave blank.
- **Pricing Fields:**
  - **monthly:** `12` (`$ US Dollars`)
  - **quarterly:** `29` (`$ US Dollars`)
  - **/ 6 months:** Leave blank.
  - **yearly:** `59` (`$ US Dollars`)
  - **/ 2 years:** Leave blank.
- **Allow customers to pay what they want:** `OFF`
- **Apply price changes to existing customers:** `OFF`

### 5.2 `Settings` Section at Bottom of Membership Page
- **Offer a free trial:** `OFF` (Never enable a free trial on a digital download vault, or users will download all `.docx`, `.pptx`, and `.xlsx` files and cancel before billing).
- **Offer a cancellation discount:** `ON` (Optional: offer `25% OFF` for 3 months if a member clicks cancel).
- **New members will be emailed this product's last published post:** `ON`
- **New members will get access to all posts you have published:** `ON`
- **Members will lose access when their memberships end:** `ON`
- **Specify a refund policy for this product:** `ON` -> Select `30-day money back guarantee`.
- **Default payment frequency:** Select **`a year`** (so `$59 / year` is pre-selected by default when buyers land on the page).

---

## 6. `Content` Tab Welcome Page & 12-Month Member Retention Roadmap

### 6.1 Content Tab Welcome Note (`Content` Tab of Listing 3)
Upload `09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Automation-Vault-Membership-Drop01.zip` (`14.12 MB`) and paste this exact onboarding guide above the download card:

```text
Welcome to the VIP Living Small Business AI Automation Vault & Editable Office Suite (By OMAR SUNNY)!

YOUR COMMERCIAL PRO WEB APP LICENSE KEY:
SMALLBIZ-OS-PRO-2026

HOW TO ACCESS YOUR VIP OFFICE SUITE & DESIGN STUDIO:
1. Download and unzip "Tier4-Living-Automation-Vault-Membership-Drop01.zip".
2. Open "13-OFFICE-EDITABLE-SUITE/Word-SOP-Manuals/" to customize all 7 Microsoft Word (.DOCX) Standard Operating Procedure manuals with your company branding.
3. Open "13-OFFICE-EDITABLE-SUITE/PowerPoint-Slide-Decks/" to present the 3 executive training slide decks (.PPTX) to your team.
4. Open "13-OFFICE-EDITABLE-SUITE/Excel-Command-Center/SmallBiz-AI-Automation-OS-Command-Center.xlsx" for the 8-tab formula-driven financial and KPI workbook.
5. Open "08-COVER-DESIGN/Design-Kit/design-customizer-studio.html" in your browser to re-color all 20 vector architecture diagrams across 6 color palettes and export PNG/SVG files.
6. Open "07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html" and enter key SMALLBIZ-OS-PRO-2026 to unlock all 6 interactive SaaS-Lite modules offline.
7. Open "10-MARKETING/tier4-monthly-vault-drop-01.md" for Monthly Industry Vault Drop #01 (Dental/Medical Clinics, HVAC/Home Services & B2B Agencies).
```

### 6.2 How to Send Monthly Member Drops via Gumroad `Posts` (`Emails -> New Post`)
To keep monthly (`$12/mo`) and annual (`$59/yr`) subscribers active for years with near-zero churn, use Gumroad's built-in **Posts** tool (`Emails -> New post -> Audience: Members of Living Small Business AI Automation Vault`) once a month:
- **Month 1 (Included at Signup — Drop #01):** Dental/Medical Clinics, HVAC/Home Services & B2B Agency Vertical Playbooks (`10-MARKETING/tier4-monthly-vault-drop-01.md`).
- **Month 2 (Drop #02):** E-Commerce, Retail & Boutique Inventory/WISMO Automation Pack (Shopify/WooCommerce order triage, return authorization gate & VIP repeat-buyer flows).
- **Month 3 (Drop #03):** Real Estate, Property Management & Mortgage Broker Speed-to-Showing Pack (24/7 tenant maintenance triage, listing inquiry SMS router & closing document chaser).
- **Month 4 (Drop #04):** Accounting, Bookkeeping, Tax & Legal Practice Client Intake Pack (Automated document collection chaser, engagement letter webhook & quarterly review scheduler).

---

## 7. Frequently Asked Questions (FAQ Block to Paste at Bottom of VIP Membership Description)

Paste this FAQ block at the bottom of your VIP Membership page (`https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`) so prospective subscribers immediately understand the value of the annual pass and editable Microsoft Office files:

```text
────────────────────────────────────────────────────────────
VIP MEMBERSHIP FREQUENTLY ASKED QUESTIONS (FAQ)
────────────────────────────────────────────────────────────

Q1: Do I get the entire Flagship Tier 3 AI Automation Operating System Bundle immediately when I join?
Yes! The moment you join (either on the $12/month plan or the $59/year Annual VIP Pass), you receive immediate access to download "Tier4-Living-Automation-Vault-Membership-Drop01.zip", which contains 100% of the Flagship Tier 3 Operating System (179-Page Digital Book, 242-Page Print PDF, EPUB 3.0, Fillable US Letter/A4/iPad Workbooks, Unlocked Pro Web Companion App with License Key SMALLBIZ-OS-PRO-2026, 5-Database Notion OS, 8-Tab Charted Excel Command Center, and 5 Make/n8n/Zapier JSON Blueprints) PLUS the entire Editable Microsoft Office Suite and Design Customizer Studio.

Q2: Can I customize the 7 Microsoft Word (.DOCX) SOP Manuals and 3 PowerPoint (.PPTX) Slide Decks with my own company logo and policies?
Absolutely. Every Word SOP manual and PowerPoint presentation deck is unlocked and formatted with clean native styles so you can replace the header with your company name, adjust role responsibilities for your staff, and use them for internal onboarding or client training inside your business.

Q3: Why is the $59/year Annual VIP Pass the exact same price as the one-time $59 Flagship OS Bundle?
We designed the $59/year Annual VIP Pass as a no-brainer founder upgrade: for the exact same $59 upfront investment as the standalone Flagship Bundle, you also unlock all 7 Editable Word (.DOCX) SOP Manuals, all 3 Editable PowerPoint (.PPTX) Slide Decks, the Interactive Design Customizer Studio, and 12 full months of Industry Automation Vault Drops.

Q4: Can I cancel my membership anytime?
Yes. You can manage or cancel your subscription in one click directly from your Gumroad receipt email or Gumroad Library at any time with zero hassle, backed by our 30-day money-back guarantee.
```
"""
    content = sanitize_text(content)
    (GUMROAD_DIR / "03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md").write_text(content, encoding="utf-8")
    return len(content.split())


def write_guide_04_upsells_and_workflows() -> int:
    content = r"""# Gumroad Checkout Upsells, Discount Codes, Automated Email Workflows & Rapid Traffic Playbook
## Project: "The Small Business AI Automation Operating System" (System Architect: OMAR SUNNY)
**Link #1 (Main 4-Version OS Page):** `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`  
**Link #2 (VIP Membership Page):** `https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`  

---

## 1. Configuring Gumroad Discount Codes (`Checkout -> Discounts`)

Before creating your checkout upsells and email workflows, navigate to **`Checkout` -> `Discounts` -> `New discount`** in your left Gumroad sidebar and create these 3 exact discount codes:

| Discount Code | Discount Amount | Target Products & Versions | Strategic Purpose |
| :--- | :--- | :--- | :--- |
| **`AUDIT10`** | `$10 OFF` (Fixed `$`) | `Listing 2 (Flagship OS)` & `Listing 3 (VIP Yearly)` | Fast-action upgrade code inside the `$0` Starter Kit PDF, Content page, and 7-Email sequence (reduces `$59` Flagship Bundle to `$49`). |
| **`LAUNCH20`** | `20% OFF` (Percentage) | All Paid Products (`Listing 2` & `Listing 3`) | Social media launch week promotion code for LinkedIn, YouTube, and Facebook groups. |
| **`VIPUPGRADE`** | `$15 OFF` (Fixed `$`) | `Listing 3 (VIP Membership — Yearly)` | Exclusive upgrade coupon sent to buyers of Tier 1 (`$19`) or Tier 2 (`$39`) so they can step up to the Annual VIP Office Suite Vault. |

---

## 2. Configuring the 3 Automated Checkout Upsells (`Checkout -> Upsells`)

Gumroad's native **In-Cart Checkout Upsells** convert `12% to 22%` of buyers into higher tiers at the exact moment they click **"I want this!"**. Navigate to **`Checkout` -> `Upsells` -> `New upsell`** and create these three upsells:

### 2.1 Checkout Upsell #1: Version-Replacement Upgrade (`Tier 0 / Tier 1 / Tier 2` -> `Tier 3 Flagship $59 Bundle`)
- **Upsell Type:** Select **`Replace the version selected with another version of the same product`**
- **Product:** `The Small Business AI Automation Operating System (smallbiz-ai-automation-os)`
- **Versions to Replace:** Check `Tier 0 ($0)`, `Tier 1 ($19)`, and `Tier 2 ($39)`
- **Version to Offer Instead:** Select `⭐ Tier 3: Complete Flagship AI Automation OS Bundle — MOST POPULAR ($59)`
- **Upsell Text / Headline:**
  ```text
  Upgrade to the Complete Flagship AI Automation OS Bundle Right Now & Save!
  ```
- **Upsell Description (Copy-Paste — Zero Banned Words):**
  ```text
  Add the Unlocked Pro Offline Web Companion App (Key: SMALLBIZ-OS-PRO-2026), the 5-Database Minimalist Notion OS Kit, the 8-Tab Charted Excel Command Center (.XLSX), and all 5 Importable Make.com / n8n / Zapier JSON Workflow Blueprints. Recover 15+ hours a week across all 5 departments in one click.
  ```

### 2.2 Checkout Upsell #2: Free Starter Kit Cross-Sell (`Listing 1 $0` -> `Listing 2 Flagship OS Bundle with $10 OFF`)
*(Use this if you also keep `smallbiz-ai-audit-kit` live as a standalone `$0` product)*
- **Upsell Type:** `Add another product to the cart`
- **Apply to:** `The 5-Day Small Business Time & Lead-Leak Audit Starter Kit (smallbiz-ai-audit-kit)`
- **Product to Offer:** `The Small Business AI Automation Operating System` -> `⭐ Tier 3: Complete Flagship AI Automation OS Bundle ($59)`
- **Discount on Upsell:** `Fixed amount` -> `$10 OFF` (Checkout price drops from `$59` to **`$49`**)
- **Upsell Headline:**
  ```text
  Add the Complete 5-Department Flagship AI Automation OS Bundle ($10 Instant Founder Discount)
  ```
- **Upsell Description:**
  ```text
  Get all 10 Chapters, 50 Tested AI Prompts, 12 Red-Gate Emergency Scripts, US Letter/A4/iPad Fillable Workbooks, the Pro Web App (Key: SMALLBIZ-OS-PRO-2026), the 5-DB Notion OS, the 8-Tab Excel Command Center, and 5 Make/n8n/Zapier JSON Blueprints for $49 instead of $59.
  ```

### 2.3 Checkout Upsell #3: Editable Office Suite & VIP Vault Add-On (`Listing 2` -> `Listing 3 VIP Membership`)
- **Upsell Type:** `Add another product to the cart`
- **Apply to:** `The Small Business AI Automation Operating System (smallbiz-ai-automation-os)`
- **Product to Offer:** `Living Small Business AI Automation Vault & Editable Office Suite VIP Membership (smallbiz-automation-vault-vip)`
- **Upsell Headline:**
  ```text
  Add the 7 Editable Microsoft Word (.DOCX) SOP Manuals, 3 PowerPoint (.PPTX) Decks & Design Studio
  ```
- **Upsell Description:**
  ```text
  Need editable Word SOP manuals for your staff, PowerPoint training decks for all-hands meetings, the Interactive Design Customizer Studio, and Monthly Industry Playbook Drops (Clinics, HVAC & Agencies)? Join the VIP Vault right now.
  ```

---

## 3. Setting Up the 7-Email Automated Conversion Sequence (`Workflows` Tab)

When someone downloads your **`$0` Free 5-Day Audit Starter Kit** (either via Version 1 of `smallbiz-ai-automation-os` or via `smallbiz-ai-audit-kit`), Gumroad can automatically send them a timed 7-email educational and conversion sequence that stops automatically as soon as they purchase a paid tier!

### Step-by-Step Setup in Gumroad `Workflows`:
1. Click **`Workflows`** in the left sidebar -> Click **`New workflow`**.
2. **Workflow Name:** `5-Day Audit Starter Kit -> Flagship OS & VIP Vault Conversion Sequence`
3. **Trigger:** `Member or customer purchases` -> Select **`Tier 0: Free 5-Day Time & Lead-Leak Audit Starter Kit ($0)`** (and `smallbiz-ai-audit-kit`).
4. **Stop Condition Filter:** Add filter **`Has not bought`** -> Select `Tier 2 ($39)`, `Tier 3 ($59)`, and `VIP Membership`.
5. Click **`Save and continue`** and add these **7 Automated Emails** (full copy-paste bodies are stored in `10-MARKETING/email-funnel-and-upsell-sequence.md`):

| Email # | Send Delay After `$0` Download | Exact Email Subject Line | Core Conversion Hook & CTA Link |
| :--- | :--- | :--- | :--- |
| **Email 01** | `0 Hours` (Immediate) | `[Download Inside] Your 5-Day Small Business Time & Lead-Leak Audit Kit + 15-Min Quickstart` | Delivers quickstart steps for `smallbiz-automation-os-app.html` + introduces `$10 OFF` code `AUDIT10` for `sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`. |
| **Email 02** | `24 Hours` (Day 1) | `Why 78% of your best leads buy from your competitor (The 5-Minute Decay Curve)` | Breaks down the Chapter 3 `60-Second Speed-to-Lead Router` and shows how answering missed calls via automated SMS recovers `$3,500+/mo`. |
| **Email 03** | `72 Hours` (Day 3) | `The "Reckless Bot" Trap: How to automate 75% of routine work with ZERO AI pricing errors` | Explains the Chapter 2 `T.R.A.V.` (`Green / Amber / Red Gate`) architecture and 15-second Slack thumb approvals. |
| **Email 04** | `120 Hours` (Day 5) | `Case Study: How a 7-person clinic cut overdue invoices from 41 days to 12 days` | Walks through Chapter 8 Same-Day Invoicing + the 5-Stage Polite-to-Firm A/R Chaser (`Blueprint 04`). |
| **Email 05** | `168 Hours` (Day 7) | `Inside the 5-Database Notion OS & 8-Tab Excel Command Center (Full Walkthrough)` | Shows screenshots/details of the Notion OS, 8-Tab Excel model, and Pro Web App (`SMALLBIZ-OS-PRO-2026`). |
| **Email 06** | `240 Hours` (Day 10) | `[48 Hours Left] Your $10 Founder Upgrade Code (AUDIT10) for the Complete AI Automation OS` | Urgency reminder for `AUDIT10` (`$59 -> $49`) on `sunnyomar.gumroad.com/l/smallbiz-ai-automation-os`. |
| **Email 07** | `336 Hours` (Day 14) | `Need Editable Word SOPs & PowerPoint Training Decks? Inside Industry Vault Drop #01` | Pitches the `$12/mo | $59/yr` VIP Membership (`sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip`) featuring the 7 `.docx` SOPs, 3 `.pptx` decks, and Clinic/Contractor/Agency playbooks. |

---

## 4. Complete Rapid Customer Attraction & Multi-Channel Marketing Playbook

To attract your first `100 to 500` downloads and trigger Gumroad Discover organic rankings as fast as possible, execute this 5-channel system:

### 4.1 Channel 1: Connect Your Live Static Website & Interactive Web App Demo (`15-WEB-DEPLOYMENT/`)
- Your repository (`https://github.com/cryptXploit/Small-business-AI-Automation-OS`) contains a complete conversion landing page (`15-WEB-DEPLOYMENT/index.html`), a live browser demo of the SaaS-Lite ROI Web App (`/app/`), and the Design Customizer Studio (`/studio/`).
- Enable **GitHub Pages** (`Settings -> Pages -> Source: GitHub Actions`).
- Share the live `/app/` ROI calculator link in founder communities so business owners can calculate their Annual Cost of Manual Friction live in their browser—and click straight to `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os` to grab the `$0` Starter Kit or `$59` Flagship Bundle!

### 4.2 Channel 2: Publish the 60s & 82s Promotional Videos (`16-VIDEO-PROMO-KIT/`)
- Use the 12 widescreen (`16:9`) scenes and 6 vertical (`9:16`) Reels/TikTok scenes in `16-VIDEO-PROMO-KIT/` with `02-Clean-Natural-Voiceover-For-ElevenLabs.txt` and `04-Synced-Video-Subtitles.srt`.
- Post the vertical 58-second video to **LinkedIn Video, YouTube Shorts, Instagram Reels, Facebook Reels, and TikTok** with the pinned comment:
  > *"Comment **AUDIT** or grab the Free 5-Day Small Business Time & Lead-Leak Audit Starter Kit (`$0`) here: https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os"*

### 4.3 Channel 3: Amazon KDP "Look Inside" Book-to-Gumroad Bridge
- Your Amazon KDP Kindle eBook (`$9.99`) and Print Paperback (`$16.99`) act as 24/7 search engines on Amazon.
- Every reader who previews Chapter 1 on Amazon sees the invitation to download the companion **Fillable Audit Workbook, Offline ROI Calculator Web App, and 5-DB Notion Kit** on your storefront—turning Amazon browsers into direct Gumroad subscribers.

### 4.4 Channel 4: Fast Gumroad Discover Eligibility (`$100` Threshold & 5-Star Ratings)
- Encourage every friend, colleague, and early downloader of your **`$0` Version 1 Starter Kit** on `https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os` to leave a **5-star rating** inside their Gumroad Library after downloading.
- Once your listing has verified 5-star ratings and crosses Gumroad's Discover balance threshold, Gumroad begins recommending your product across the `Business & Money` marketplace automatically.

---

## 5. Copy-Paste High-Converting Social Launch Posts (LinkedIn, Facebook & X/Twitter)

Use these 3 ready-to-publish launch posts to drive immediate traffic to both of your Gumroad links:

### 5.1 LinkedIn Founder Authority Post (Drives `$0` Audit + `$59` Flagship OS)
```text
Most 1-to-25 person businesses don't have a "lead generation" problem.
They have a 5-minute response-time problem and an evening paperwork problem.

Across 200+ small business workflows I analyzed while architecting "The Small Business AI Automation Operating System", three numbers stood out:
1. 78% of customers buy from the first business that responds—yet the average small business takes 4+ hours to reply to a web form or missed call.
2. Founders and office managers spend 15 to 22 hours every week copying data between email, spreadsheets, calendars, and invoicing tools.
3. Completed work sits unpaid for 38+ days simply because nobody wants to send awkward overdue reminder emails.

Yet when owners try to "use AI", they hook up an unguarded chatbot that hallucinates a 40% discount and embarrasses the company.

That is why I built the T.R.A.V. (Trigger -> Rules -> AI -> Verification) human-in-the-loop operating system:
• Green Gate (75% of volume): 24/7 instant SMS lead capture & grounded FAQ replies.
• Amber Gate (20% of volume): 15-second Slack/Teams thumb approval for 3-option quotes & overdue invoice chasers.
• Red Gate (5% of volume): Instant human takeover when customer sentiment drops.

Today, I am releasing the complete 5-Department Operating System—and you can download the 5-Day Small Business Time & Lead-Leak Audit Starter Kit (32-Page Fillable Audit PDF + Offline HTML5 ROI Simulator Web App + Prompts 1.1–1.5) for $0:

👉 Download the $0 Audit Starter Kit or Full Flagship OS Bundle:
https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os

👉 Need Editable Microsoft Word (.DOCX) SOP Manuals, PowerPoint (.PPTX) Training Decks & Monthly Industry Drops? Join the VIP Vault:
https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip
```

### 5.2 Short-Form DM / Comment Auto-Reply Template
Whenever someone comments **`AUDIT`** or **`OS`** on your LinkedIn, Facebook, YouTube, or Instagram video, reply with:
```text
Here is your direct link to the Free 5-Day Small Business Time & Lead-Leak Audit Starter Kit ($0 Version 1) + the Complete 5-Department AI Automation OS Bundle:
https://sunnyomar.gumroad.com/l/smallbiz-ai-automation-os

And if you want the 7 Editable Microsoft Word (.DOCX) SOP Manuals + 3 PowerPoint (.PPTX) Team Training Decks, check out the VIP Vault here:
https://sunnyomar.gumroad.com/l/smallbiz-automation-vault-vip
```
"""
    content = sanitize_text(content)
    (GUMROAD_DIR / "04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md").write_text(content, encoding="utf-8")
    return len(content.split())


def write_guide_05_ai_image_prompts() -> int:
    content = r"""# 12 High-Precision AI Cover, 3D Bundle & Square Thumbnail Generation Prompts
## Project: "The Small Business AI Automation Operating System" (System Architect: OMAR SUNNY)
**Optimized For:** Ideogram 2.0 (Best for exact typography rendering), Midjourney v6.1, DALL-E 3 (ChatGPT Plus), and Leonardo AI Phoenix  
**Brand Palette:** Executive Emerald (`#059669` / `#34D399`), Deep Slate Navy (`#0F172A` / `#1E293B`), System Cyan (`#0284C7` / `#38BDF8`), Amber Gate (`#D97706` / `#FBBF24`), Pure White (`#FFFFFF`)  

---

## 1. How to Use These 12 Studio Prompts

While your repository already includes production-verified vector `.svg` and high-resolution `.png` covers and `600×600` square thumbnails in `08-COVER-DESIGN/` and `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/`, you can also paste any of the 12 prompts below into **Ideogram 2.0**, **DALL-E 3**, or **Midjourney v6.1** to generate photorealistic 3D hardware mockups, social ad creatives, and YouTube/LinkedIn banners bearing your official author credit **`BY OMAR SUNNY`**.

---

## 2. Prompts 1–3: Square `1:1` (`600×600` / `1024×1024`) Gumroad Discover Thumbnail Prompts

### Prompt 1: Listing 1 (`$0` Free 5-Day Time & Lead-Leak Audit Starter Kit — Square `1:1`)
```text
A sleek, high-contrast 1:1 square digital product thumbnail for Gumroad Discover on a deep executive navy-slate background (#0F172A) with a subtle glowing isometric circuit grid. At the top, a glowing emerald-and-cyan pill badge reads "$0 FREE STARTER KIT". In the center, a photorealistic 3D isometric stack showing an open spiral-bound executive audit workbook, a glowing dark-mode laptop displaying an ROI calculator dashboard with green bar charts, and a floating glass card with a 60-second stopwatch icon. Bold, razor-sharp white and emerald sans-serif typography at the top-left reads "5-DAY SMALL BUSINESS TIME & LEAD-LEAK AUDIT". At the bottom center in clean tracked-out white micro-typography: "BY OMAR SUNNY". Studio rim lighting, enterprise SaaS aesthetic, 8k resolution, aspect ratio 1:1.
```

### Prompt 2: Listing 2 (`$0 / $19 / $39 / $59` Flagship Complete AI Automation OS Bundle — Square `1:1`)
```text
An ultra-premium 1:1 square B2B software and book bundle thumbnail on a deep dark slate background (#0F172A). In the center, an isometric 3D glowing hub connecting five illuminated nodes (Emerald Green, System Cyan, and Warm Amber) surrounded by a hardcover book titled "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM", an iPad Pro showing a landscape planner, a MacBook Pro displaying a 5-database Notion & Excel dashboard, and floating JSON workflow cards. A top emerald badge reads "COMPLETE 5-DEPT AI OS". Clean, bold white and emerald typography reads "50 AI PROMPTS • WEB APP • NOTION & EXCEL OS". Bottom centered author credit in crisp white uppercase letters: "BY OMAR SUNNY". Octane render, sharp studio lighting, aspect ratio 1:1.
```

### Prompt 3: Listing 3 (`$12/mo` or `$59/yr` VIP Living Automation Vault & Editable Office Suite — Square `1:1`)
```text
A luxury executive 1:1 square membership thumbnail on a deep obsidian-navy background (#0F172A) with warm gold-amber (#F59E0B) and emerald (#10B981) accents. Centerpiece shows a glowing metallic vault door opening to reveal floating 3D Microsoft Word (.DOCX) SOP binders, widescreen PowerPoint (.PPTX) presentation slides, a color-theme customizer palette, and three industry badges (Medical Clinic, HVAC Contractor, B2B Agency). Top gold-amber badge reads "VIP LIVING VAULT & OFFICE SUITE". Bold white headline reads "EDITABLE WORD SOPs • PPTX DECKS • MONTHLY DROPS". Bottom centered credit in clean white uppercase typography: "BY OMAR SUNNY". High-contrast commercial render, aspect ratio 1:1.
```

---

## 3. Prompts 4–7: Widescreen `16:9` (`1280×720` / `1920×1080`) Gumroad Product Carousel Header Prompts

### Prompt 4: Flagship Hero Banner (All-in-One Ecosystem Showcase — `16:9` Widescreen)
```text
A widescreen 16:9 e-commerce hero banner for a flagship B2B digital product on a dark executive slate desk (#0F172A). On the right side, a photorealistic 3D product arrangement featuring: (1) a matte-black and emerald hardcover book titled "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM" by OMAR SUNNY, (2) a widescreen laptop running a dark-mode ROI & Prompt Customizer web app, (3) a secondary monitor showing an 8-tab Excel dashboard and 5 Notion databases, and (4) an iPad with an Apple Pencil showing a fillable action workbook. On the left side, clean bold typography reads: "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM" with subtitle "50 AI Prompts • 12 Crisis Scripts • Offline Web App • Notion & Excel OS • 5 JSON Blueprints" and footer "SYSTEM ARCHITECT: OMAR SUNNY". Crisp studio lighting, 16:9 aspect ratio.
```

### Prompt 5: T.R.A.V. Human-in-the-Loop Governance & Safety Architecture Slide (`16:9`)
```text
A widescreen 16:9 technical infographic product slide on a dark slate background (#0F172A). Shows a sleek horizontal 4-stage pipeline diagram glowing in neon emerald, cyan, and amber: Stage 1 "TRIGGER (Webhook Intake)" -> Stage 2 "RULES (Deterministic SKU & Regex Gate)" -> Stage 3 "AI DRAFTING (Grounded RAG temperature 0.1)" -> Stage 4 "VERIFICATION (Green 75% Auto | Amber 20% 15s Slack Approval | Red 5% Human Takeover)". Below the diagram, three glassmorphism UI cards display a mobile Slack 1-click approval card. Top title: "ZERO-HALLUCINATION T.R.A.V. SAFETY ARCHITECTURE". Bottom right credit: "BY OMAR SUNNY". Aspect ratio 16:9.
```

### Prompt 6: 60-Second Speed-to-Lead & 3-Tier Proposal Engine Slide (`16:9`)
```text
A widescreen 16:9 business automation showcase slide on a deep navy-slate background (#0F172A). On the left, five incoming icons (Website Form, Missed Phone Call, WhatsApp, Instagram DM, Google Business) flow into a glowing central router labeled "< 60 SECOND SPEED-TO-LEAD ROUTER". On the right, a smartphone screen displays an instant polite SMS reply booking an appointment, next to a 3-column "Good / Better / Best" proposal PDF. Bold header: "CAPTURE EVERY LEAD IN UNDER 60 SECONDS". Bottom credit: "BY OMAR SUNNY". Aspect ratio 16:9.
```

### Prompt 7: Editable Microsoft Office Suite (`.DOCX` + `.PPTX` + `.XLSX`) Showcase Slide (`16:9`)
```text
A widescreen 16:9 product showcase banner on a dark slate background (#0F172A) with gold-amber (#D97706) and emerald (#059669) rim lighting. Displays 7 fanned-out spiral-bound executive SOP manuals with blue Word (.DOCX) badges, 3 widescreen presentation decks with orange PowerPoint (.PPTX) badges, and an 8-tab financial command center with green Excel (.XLSX) charts. Headline text: "7 EDITABLE WORD SOPs • 3 POWERPOINT DECKS • 8-TAB EXCEL MODEL". Bottom credit: "BY OMAR SUNNY". Aspect ratio 16:9.
```

---

## 4. Prompts 8–12: Amazon KDP, YouTube Thumbnail, LinkedIn Authority Banner & Notion Header Prompts

### Prompt 8: Amazon KDP Vertical Book Cover (`1:1.6` / `1600×2560` Portrait)
```text
A bestseller vertical non-fiction business and technology book cover (aspect ratio 1:1.6) on a deep dark navy background (#0F172A). At the top center, bold white uppercase sans-serif typography reads "THE SMALL BUSINESS", followed by a glowing emerald green (#10B981) rounded pill banner reading "AI AUTOMATION", followed by bold white uppercase text "OPERATING SYSTEM". Below a thin gold-amber divider line, clean silver-white subtitle text reads "A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff". In the lower-middle section, a detailed isometric 3D glowing platform with a central gear-chip hub connected by fiber-optic data lines to four glowing nodes (green search node, cyan customer support node, amber invoicing node, and teal analytics node). At the bottom center in clean wide-tracked white uppercase letters: "O M A R   S U N N Y".
```

### Prompt 9: High-CTR YouTube / Video Promo Thumbnail (`16:9` `1920×1080`)
```text
A high-contrast 16:9 YouTube thumbnail on a dark navy background. Split-screen comparison: on the left side (tinted warning red/amber), a stressed business owner at 11:47 PM surrounded by missed call notifications and unpaid invoices labeled "MANUAL CHAOS (55 HRS/WK)". On the right side (tinted glowing emerald green), a clean 5-department AI dashboard running automatically with a badge reading "AI AUTOMATION OS (15 HRS SAVED/WK)". Huge bold white and emerald 3D text across the top: "AUTOMATE YOUR SMALL BUSINESS IN 90 DAYS". Bottom corner badge: "BY OMAR SUNNY".
```

### Prompt 10: Payhip / LemonSqueezy `4:3` (`1600×1200`) Product Box Mockup
```text
A 4:3 landscape commercial software box and device bundle mockup on a dark slate studio surface (#0F172A). Features a tall 3D software box and hardcover book titled "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM", flanked by a desktop monitor showing the 8-tab Excel Command Center, a laptop showing the Offline ROI Web App, and printed fillable worksheets. Emerald and cyan studio lighting, author credit "BY OMAR SUNNY" on the box spine and front. Aspect ratio 4:3.
```

### Prompt 11: LinkedIn Personal Brand Authority Profile Banner (`1584×396` Ultra-Wide `4:1`)
```text
A clean, ultra-wide 4:1 LinkedIn profile cover banner (1584x396) on a deep executive navy-slate gradient (#0F172A to #1E293B). Keep the bottom-left 25% clear for the circular LinkedIn profile photo. On the right 75%, display a sleek glowing isometric diagram of the 5-Department Small Business AI Automation Operating System alongside a small 3D book mockup. Crisp white and emerald typography reads: "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM • SAVE 15+ HOURS/WEEK WITHOUT EXTRA STAFF • BY OMAR SUNNY".
```

### Prompt 12: Notion Executive Command Center Cover Header (`1500×600` Wide `5:2`)
```text
A minimalist 5:2 wide Notion workspace header banner (1500x600) on a dark slate background (#0F172A) with a subtle geometric blueprint grid. Centered glowing emerald (#059669), cyan (#0284C7), and amber (#D97706) telemetry nodes connected by clean circuit lines, with sleek monospace typography reading: "SMALL BUSINESS AI AUTOMATION OS — 5-DATABASE EXECUTIVE COMMAND CENTER • ARCHITECT: OMAR SUNNY".
```

---

## 5. Platform-Specific Export & Post-Processing Settings (Ideogram 2.0, Midjourney v6.1 & Canva)

To ensure every AI-generated or custom-rendered graphic passes Gumroad, Amazon KDP, Payhip, and LinkedIn quality gates without compression blur:

| Target Asset Slot | Required Pixel Dimensions | Aspect Ratio | Recommended AI Generator Parameter | Local Pre-Built Ready File in Repository |
| :--- | :--- | :--- | :--- | :--- |
| **Gumroad Discover Square Thumbnail (Listing 1)** | `600 × 600 px` (or `1200 × 1200 px`) | `1:1` | `--ar 1:1 --v 6.1 --style raw` | `08-COVER-DESIGN/11-gumroad-square-thumb-listing1-free-audit-600x600.png` |
| **Gumroad Discover Square Thumbnail (Listing 2)** | `600 × 600 px` (or `1200 × 1200 px`) | `1:1` | `--ar 1:1 --v 6.1 --style raw` | `08-COVER-DESIGN/12-gumroad-square-thumb-listing2-flagship-os-600x600.png` |
| **Gumroad Discover Square Thumbnail (Listing 3)** | `600 × 600 px` (or `1200 × 1200 px`) | `1:1` | `--ar 1:1 --v 6.1 --style raw` | `08-COVER-DESIGN/13-gumroad-square-thumb-listing3-vip-membership-600x600.png` |
| **Gumroad Product Cover Banner (`16:9`)** | `1280 × 720 px` | `16:9` | `--ar 16:9 --v 6.1 --style raw` | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/05-gumroad-tier3-flagship-bundle-cover-1280x720.png` |
| **Amazon KDP Kindle eBook Cover (`1:1.6`)** | `1600 × 2560 px` (`300 DPI`) | `1:1.6` | `--ar 5:8 --v 6.1 --style raw` | `08-COVER-DESIGN/ebook-cover-kdp-kindle.jpg` |
| **Amazon KDP Full-Wrap Paperback (`6"×9"`)** | `12.795" × 9.25"` (`242 pages`) | Full Wrap | Print-Ready PDF with Barcode Box | `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf` |

### 5.1 Typography & Brand Consistency Rules When Editing in Canva or Photoshop
- **Primary Headline Font:** `Inter ExtraBold` or `Montserrat Black` (Uppercase, `-0.02em` tracking, pure white `#FFFFFF` with Emerald `#34D399` accent pills).
- **Author Attribution Line:** Always render **`OMAR SUNNY`** or **`BY OMAR SUNNY`** in clean wide-tracked uppercase sans-serif (`+0.18em` letter spacing) at the bottom center of every book cover, square thumbnail, and social card so all storefront listings share an unmistakable executive signature.
"""
    content = sanitize_text(content)
    (GUMROAD_DIR / "05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md").write_text(content, encoding="utf-8")
    return len(content.split())


def update_tier4_zip_with_gumroad_pack():
    zip_path = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "Tier4-Living-Automation-Vault-Membership-Drop01.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(str(zip_path), "a", compression=zipfile.ZIP_DEFLATED) as zf:
        existing = set(zf.namelist())
        for fpath in sorted(GUMROAD_DIR.rglob("*")):
            if fpath.is_file():
                arcname = fpath.relative_to(STUDIO_ROOT).as_posix()
                if arcname not in existing:
                    zf.write(str(fpath), arcname)
        for sq_name in [
            "11-gumroad-square-thumb-listing1-free-audit-600x600.svg",
            "11-gumroad-square-thumb-listing1-free-audit-600x600.png",
            "12-gumroad-square-thumb-listing2-flagship-os-600x600.svg",
            "12-gumroad-square-thumb-listing2-flagship-os-600x600.png",
            "13-gumroad-square-thumb-listing3-vip-membership-600x600.svg",
            "13-gumroad-square-thumb-listing3-vip-membership-600x600.png",
        ]:
            sp = COVER_DIR / sq_name
            arc = f"08-COVER-DESIGN/{sq_name}"
            if sp.exists() and arc not in existing:
                zf.write(str(sp), arc)


def main():
    browser_exe = find_browser_executable()
    cover_b64 = get_omar_sunny_cover_thumb_b64()

    sq_specs = [
        ("11-gumroad-square-thumb-listing1-free-audit-600x600", build_square_svg_1(cover_b64)),
        ("12-gumroad-square-thumb-listing2-flagship-os-600x600", build_square_svg_2(cover_b64)),
        ("13-gumroad-square-thumb-listing3-vip-membership-600x600", build_square_svg_3(cover_b64)),
    ]

    for stem, svg_xml in sq_specs:
        svg_xml_clean = sanitize_text(svg_xml)
        svg_p = COVER_DIR / f"{stem}.svg"
        png_p = COVER_DIR / f"{stem}.png"
        svg_p.write_text(svg_xml_clean, encoding="utf-8")
        render_svg_to_exact_png(browser_exe, svg_p, png_p, 600, 600)
        shutil.copyfile(svg_p, THUMBS_DIR / f"{stem}.svg")
        shutil.copyfile(png_p, THUMBS_DIR / f"{stem}.png")
        print(f" -> Built 600x600 Square Thumbnail: {stem}.png ({png_p.stat().st_size:,} B)")

    copy_and_resize_1280x720_covers()

    w0 = write_guide_00_unified_strategy()
    w1 = write_guide_01_listing_1()
    w2 = write_guide_02_listing_2()
    w3 = write_guide_03_listing_3()
    w4 = write_guide_04_upsells_and_workflows()
    w5 = write_guide_05_ai_image_prompts()

    print(f" -> Guide 00 (Unified 2-Link Strategy): {w0} words")
    print(f" -> Guide 01 (Listing 1 Free Starter Kit): {w1} words")
    print(f" -> Guide 02 (Listing 2 Flagship 4-Version OS): {w2} words")
    print(f" -> Guide 03 (Listing 3 VIP Membership): {w3} words")
    print(f" -> Guide 04 (Upsells, Coupons & Workflows): {w4} words")
    print(f" -> Guide 05 (12 AI Cover & Thumbnail Prompts): {w5} words")

    update_tier4_zip_with_gumroad_pack()
    print(" -> Updated Tier 4 ZIP archive with Gumroad-Hybrid-Master-Setup/")


if __name__ == "__main__":
    main()
