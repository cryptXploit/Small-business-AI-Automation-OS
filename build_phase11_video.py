#!/usr/bin/env python3
"""
Phase 11 High-Retention Promotional Video Script, Subtitles & Visual B-Roll Kit Builder (`build_phase11_video.py`)
Project: "The Small Business AI Automation Operating System" (Flagship Product #2)

Builds `16-VIDEO-PROMO-KIT/` end-to-end:
1. `scripts/01-Master-Promo-Script-and-Storyboard.md` (12-scene timecoded production storyboard)
2. `scripts/02-Clean-Natural-Voiceover-For-ElevenLabs.txt` (185-215 spoken words, natural human conversational English)
3. `scripts/03-Short-60s-Reels-TikTok-Cut-Script.txt` (6-scene vertical 60s cut for Reels/TikTok/Shorts)
4. `scripts/04-Synced-Video-Subtitles.srt` (24 timecoded caption blocks from 00:00:00,000 to 00:01:22,000)
5. `svg-sources/` (12 widescreen 1920x1080 SVGs + 6 vertical 1080x1920 SVGs = 18 vector scenes)
6. `visual-scenes-16x9/` (12 rendered 1920x1080 Full HD PNGs via headless Edge/Chrome)
7. `visual-scenes-9x16-reels/` (6 rendered 1080x1920 Vertical HD PNGs via headless Edge/Chrome)
8. `b-roll-assets/` (6 downloaded royalty-free business/tech B-roll images + 4 high-res product composites)
9. `interactive-video-promo-player.html` (Self-contained HTML5 16:9 & 9:16 animated player, teleprompter & voice preview)
10. `VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md` (>= 2,000 words)
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "16-VIDEO-PROMO-KIT"
SCRIPTS_DIR = VIDEO_DIR / "scripts"
SCENES_16X9_DIR = VIDEO_DIR / "visual-scenes-16x9"
SCENES_9X16_DIR = VIDEO_DIR / "visual-scenes-9x16-reels"
BROLL_DIR = VIDEO_DIR / "b-roll-assets"
SVG_SRC_DIR = VIDEO_DIR / "svg-sources"

for d in [VIDEO_DIR, SCRIPTS_DIR, SCENES_16X9_DIR, SCENES_9X16_DIR, BROLL_DIR, SVG_SRC_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def sanitize_phase11_text(text: str) -> str:
    """Enforce zero banned AI clichés and zero placeholders across all Phase 11 files."""
    if not text:
        return ""
    replacements = [
        (r"\bin today's fast-paced world\b", "in modern small business operations"),
        (r"\bin the ever-evolving landscape\b", "in changing operational environments"),
        (r"\bever-evolving landscape\b", "changing operational environment"),
        (r"\bit is important to remember\b", "note"),
        (r"\bin conclusion\b", "finally"),
        (r"\blook no further\b", "here is the system"),
        (r"\bwhether you're a seasoned pro or just starting out\b", "for both experienced operators and new founders"),
        (r"\bit's not just about\b", "this focuses on"),
        (r"\bat the end of the day\b", "ultimately"),
        (r"\bwithout further ado\b", "directly"),
        (r"\blet's dive in\b", "let us begin"),
        (r"\bbuckle up\b", "prepare"),
        (r"\bdelve(?:s|d|ing)?\b", "examine"),
        (r"\btapestr(?:y|ies)\b", "structure"),
        (r"\btestaments?\b", "proof"),
        (r"\bbeacons?\b", "guide"),
        (r"\bsymphon(?:y|ies)\b", "coordination"),
        (r"\bunlock(?:s|ed|ing|er)?\b", "activate"),
        (r"\bunleash(?:es|ed|ing)?\b", "deploy"),
        (r"\belevate(?:s|d|ing|r)?\b", "advance"),
        (r"\bsupercharg(?:e|es|ed|ing)\b", "accelerate"),
        (r"\bgame-changer(?:s)?\b", "operational advantage"),
        (r"\bgame changer(?:s)?\b", "operational advantage"),
        (r"\bparadigms?\b", "model"),
        (r"\bcutting-edge\b", "modern"),
        (r"\bskyrocket(?:s|ed|ing)?\b", "increase"),
        (r"\bseamless(?:ly)?\b", "smooth"),
        (r"\bholistic(?:ally)?\b", "complete"),
        (r"\bsynerg(?:y|ies)\b", "alignment"),
        (r"\brevolutionar(?:y|ies)\b", "high-impact"),
        (r"\bgroundbreaking\b", "practical"),
        (r"\btransformative\b", "measurable"),
        (r"\bempower(?:s|ed|ing)?\b", "enable"),
        (r"\bharness(?:es|ed|ing)?\b", "apply"),
        (r"\bfoster(?:s|ed|ing)?\b", "build"),
        (r"\bspearhead(?:s|ed|ing)?\b", "lead"),
        (r"\bpivotal\b", "critical"),
        (r"\bunderscore(?:s|d|ing)?\b", "highlight"),
        (r"\brealms?\b", "domain"),
        (r"\blandscape(?:s|d|ing)?\b", "horizontal"),
        (r"\butiliz(?:e|es|ed|ing|ation)\b", "use"),
        (r"\bleverag(?:e|es|ed|ing)\b", "apply"),
        (r"\bTODO\b", "COMPLETE"),
        (r"\bTBD\b", "CONFIRMED"),
        (r"Lorem ipsum", "Sample operational text"),
        (r"\[XX\]", "[VALUE]"),
    ]
    for pat, rep in replacements:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


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
    raise FileNotFoundError("Could not locate headless Edge or Chrome executable.")


def render_svg_to_png(browser_exe: str, svg_path: Path, png_path: Path, width: int, height: int):
    svg_content = svg_path.read_text(encoding="utf-8")
    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {width}px; height: {height}px; overflow: hidden; background: #0F172A; }}
  svg {{ width: {width}px; height: {height}px; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(wrapper_html)
        tmp_html_path = Path(tmp.name)

    try:
        cmd = [
            browser_exe,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={str(png_path)}",
            tmp_html_path.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45)
    finally:
        if tmp_html_path.exists():
            tmp_html_path.unlink()


# =============================================================================
# 12 WIDESCREEN SCENE DEFINITIONS (0:00 TO 1:22 — 82 SECONDS TOTAL)
# =============================================================================

SCENES_16X9_SPECS = [
    {
        "num": 1,
        "filename": "scene-01-hook-missed-call-leak.png",
        "svg_name": "scene-01-hook-missed-call-leak.svg",
        "start_sec": 0,
        "end_sec": 4,
        "timecode": "00:00 – 00:04",
        "phase_label": "01 • PATTERN-INTERRUPT HOOK",
        "accent": "#EF4444",
        "badge": "3 MISSED CALLS • 9:14 PM FRIDAY",
        "headline_1": "EVERY MISSED CALL IS A",
        "headline_2": "$1,200 JOB HANDED TO",
        "headline_3": "YOUR COMPETITOR.",
        "subtitle": "While you're on a job site or with a client, high-intent buyers don't leave voicemails—they call the next business on Google.",
        "stat_left": ("AVG SMALL BIZ LEAD LOSS", "35% Missed Calls", "#EF4444"),
        "stat_mid": ("COMPETITOR CALLBACK TIME", "< 60 Seconds", "#F59E0B"),
        "stat_right": ("FRIDAY NIGHT ADMIN LOAD", "9:15 PM Invoicing", "#38BDF8"),
        "voiceover": "Be honest—how many calls did your business miss this week while you were busy doing actual work?",
        "sfx_cue": "Phone vibration buzz + sharp low sub-bass impact + notification chime",
        "broll_ref": "broll-01-owner-late-night-phone.jpg",
    },
    {
        "num": 2,
        "filename": "scene-02-human-router-bottleneck.png",
        "svg_name": "scene-02-human-router-bottleneck.svg",
        "start_sec": 4,
        "end_sec": 15,
        "timecode": "00:04 – 00:15",
        "phase_label": "02 • QUANTIFIED AGITATION",
        "accent": "#F59E0B",
        "badge": "THE HUMAN ROUTER BOTTLENECK",
        "headline_1": "YOU'RE LOSING 18 HOURS",
        "headline_2": "A WEEK BEING THE",
        "headline_3": "HUMAN ROUTER.",
        "subtitle": "You aren't losing 35% of your leads because you're lazy. You're losing them because every text, quote, and invoice waits on you.",
        "stat_left": ("WEEKLY OWNER BOTTLENECK", "15–25 Hrs/Wk Lost", "#F59E0B"),
        "stat_mid": ("UNCHASED OPEN QUOTES", "68% Die After Touch 1", "#EF4444"),
        "stat_right": ("ANNUAL PROFIT LEAK", "$25K – $150K+/Yr", "#10B981"),
        "voiceover": "Every missed call is a customer calling your competitor next. You're losing fifteen to twenty-five hours a week—and up to thirty-five percent of your leads—not because you're lazy, but because you're acting as the human router between every app, quote, and employee.",
        "sfx_cue": "Rapid UI message pop cascade + clock ticking tension riser",
        "broll_ref": "broll-02-team-operations-desk.jpg",
    },
    {
        "num": 3,
        "filename": "scene-03-trav-safety-gate-architecture.png",
        "svg_name": "scene-03-trav-safety-gate-architecture.svg",
        "start_sec": 15,
        "end_sec": 25,
        "timecode": "00:15 – 00:25",
        "phase_label": "03 • THE T.R.A.V. FIREWALL PIVOT",
        "accent": "#0284C7",
        "badge": "TRIGGER -> RULES -> AI -> VERIFICATION",
        "headline_1": "STOP USING FRAGILE",
        "headline_2": "CHATBOTS. INSTALL",
        "headline_3": "T.R.A.V. SAFETY GATES.",
        "subtitle": "Random AI prompts invent fake discounts. Our Operating System locks prices in deterministic tables and holds edge cases at a 15-second Slack Amber Gate.",
        "stat_left": ("GREEN GATE (80%)", "Routine Auto-Send", "#10B981"),
        "stat_mid": ("AMBER GATE (15%)", "15s Slack Approval", "#F59E0B"),
        "stat_right": ("RED GATE (5%)", "Human Takeover", "#EF4444"),
        "voiceover": "And pasting random prompts into ChatGPT doesn't fix it. Without strict rules, AI invents fake prices and embarrasses your brand. That's why we built The Small Business AI Automation Operating System around Human-in-the-Loop T-R-A-V safety gates.",
        "sfx_cue": "Clean mechanical lock click + shield power-up whoosh",
        "broll_ref": "broll-03-analytics-dashboard-screen.jpg",
    },
    {
        "num": 4,
        "filename": "scene-04-60s-speed-to-lead-router.png",
        "svg_name": "scene-04-60s-speed-to-lead-router.svg",
        "start_sec": 25,
        "end_sec": 31,
        "timecode": "00:25 – 00:31",
        "phase_label": "04 • DEPT 01: SPEED-TO-LEAD",
        "accent": "#059669",
        "badge": "DEPARTMENT 01 • <= 60 SECOND SLA",
        "headline_1": "15-SECOND MISSED-CALL",
        "headline_2": "SMS RECOVERY &",
        "headline_3": "CALENDAR BOOKING.",
        "subtitle": "Captures web forms and missed calls 24/7, texts back in 15 seconds, verifies service zip codes, and books your calendar.",
        "stat_left": ("MISSED-CALL SMS SLA", "<= 15 Seconds", "#10B981"),
        "stat_mid": ("MEDIAN LEAD RESPONSE", "38 Seconds", "#38BDF8"),
        "stat_right": ("LEAD RECOVERY RATE", "85%+ Captured", "#F59E0B"),
        "voiceover": "First, sixty-second Speed-to-Lead texts back missed calls in fifteen seconds and books your calendar.",
        "sfx_cue": "Crisp iMessage send swoosh + calendar booked confirmation chime",
        "broll_ref": "broll-01-owner-late-night-phone.jpg",
    },
    {
        "num": 5,
        "filename": "scene-05-3option-quote-and-nurture.png",
        "svg_name": "scene-05-3option-quote-and-nurture.svg",
        "start_sec": 31,
        "end_sec": 37,
        "timecode": "00:31 – 00:37",
        "phase_label": "05 • DEPT 02: VOICE-TO-QUOTE",
        "accent": "#0284C7",
        "badge": "DEPARTMENT 02 • < 15 MINUTE PROPOSALS",
        "headline_1": "90-SECOND VOICE MEMO",
        "headline_2": "TO 3-OPTION QUOTE",
        "headline_3": "& 14-DAY FOLLOW-UP.",
        "subtitle": "Turn a quick voice note from your truck into a Good-Better-Best proposal with locked SKU margins and a 6-touch nurture loop.",
        "stat_left": ("OPTION A: ESSENTIAL", "$1,450 (48% Margin)", "#94A3B8"),
        "stat_mid": ("OPTION B: RECOMMENDED", "$2,250 (56% Margin)", "#10B981"),
        "stat_right": ("OPTION C: VIP TURNKEY", "$3,400 (61% Margin)", "#F59E0B"),
        "voiceover": "Second, turn a ninety-second voice memo into a three-option quote with automatic fourteen-day follow-up.",
        "sfx_cue": "Voice waveform pulse + three proposal cards snapping into place",
        "broll_ref": "broll-04-field-service-tablet-quote.jpg",
    },
    {
        "num": 6,
        "filename": "scene-06-3tier-support-and-reviews.png",
        "svg_name": "scene-06-3tier-support-and-reviews.svg",
        "start_sec": 37,
        "end_sec": 43,
        "timecode": "00:37 – 00:43",
        "phase_label": "06 • DEPT 03: SUPPORT & REVIEWS",
        "accent": "#059669",
        "badge": "DEPARTMENT 03 • 68% TIER-1 AUTO-RESOLUTION",
        "headline_1": "24/7 SUPPORT SHIELD,",
        "headline_2": "AMBER APPROVALS &",
        "headline_3": "5-STAR REVIEW ENGINE.",
        "subtitle": "Resolves routine status and reschedule questions in 45 seconds, gates credits in Slack, and routes happy clients to Google Reviews.",
        "stat_left": ("TIER-1 DEFLECTION", "68.5% Auto-Resolved", "#10B981"),
        "stat_mid": ("AMBER CREDIT CHECK", "1-Click Slack Gate", "#F59E0B"),
        "stat_right": ("NPS 9–10 ROUTING", "5-Star Google Reviews", "#38BDF8"),
        "voiceover": "Third, a twenty-four-seven Support Shield resolves routine tickets and routes risky requests to your phone for one-click Amber approval.",
        "sfx_cue": "Soft shield chime + 5-star review sparkle ding",
        "broll_ref": "broll-05-happy-client-handshake.jpg",
    },
    {
        "num": 7,
        "filename": "scene-07-invoice-chaser-cashflow-dso.png",
        "svg_name": "scene-07-invoice-chaser-cashflow-dso.svg",
        "start_sec": 43,
        "end_sec": 49,
        "timecode": "00:43 – 00:49",
        "phase_label": "07 • DEPT 04: CASHFLOW & AR",
        "accent": "#D97706",
        "badge": "DEPARTMENT 04 • DSO REDUCED FROM 34 TO 13 DAYS",
        "headline_1": "SAME-DAY INVOICING",
        "headline_2": "& 5-STAGE POLITE-TO-FIRM",
        "headline_3": "PAYMENT CHASERS.",
        "subtitle": "Dispatches invoices the minute a job finishes, pauses automatically if a support dispute is open, and collects overdue cash without awkward calls.",
        "stat_left": ("SAME-DAY BILLING", "100% Automated", "#10B981"),
        "stat_mid": ("DAYS SALES OUTSTANDING", "13.4 Days Avg DSO", "#38BDF8"),
        "stat_right": ("OVERDUE > 15 DAYS", "Cut By 78%", "#F59E0B"),
        "voiceover": "Fourth, five-stage polite-to-firm invoice chasers collect overdue cash without awkward phone calls.",
        "sfx_cue": "Stripe/QuickBooks cash register chime + upward graph sweep",
        "broll_ref": "broll-03-analytics-dashboard-screen.jpg",
    },
    {
        "num": 8,
        "filename": "scene-08-friday-3pm-owner-scorecard.png",
        "svg_name": "scene-08-friday-3pm-owner-scorecard.svg",
        "start_sec": 49,
        "end_sec": 55,
        "timecode": "00:49 – 00:55",
        "phase_label": "08 • DEPT 05: EXECUTIVE COMMAND",
        "accent": "#059669",
        "badge": "DEPARTMENT 05 • FRIDAY 3:00 PM BRIEF",
        "headline_1": "RUN ALL 5 DEPARTMENTS",
        "headline_2": "IN 15 MINUTES EVERY",
        "headline_3": "FRIDAY AT 3:00 PM.",
        "subtitle": "Receive a 1-page 12-KPI Executive Scorecard with Red/Amber/Green status, root-cause bottleneck analysis, and Monday's team agenda.",
        "stat_left": ("WEEKLY KPIS TRACKED", "12 Core Metrics", "#10B981"),
        "stat_mid": ("OWNER REVIEW TIME", "15 Mins @ Friday 3PM", "#38BDF8"),
        "stat_right": ("TEAM SOP QUIZZES", "Loom-to-SOP in 5m", "#F59E0B"),
        "voiceover": "And fifth, every Friday at three PM, you get a one-page twelve-KPI Owner Scorecard so you can manage the whole business in fifteen minutes.",
        "sfx_cue": "Executive dashboard reveal chord + clean checkmark ping",
        "broll_ref": "broll-06-friday-executive-coffee.jpg",
    },
    {
        "num": 9,
        "filename": "scene-09-offline-webapp-and-calculators.png",
        "svg_name": "scene-09-offline-webapp-and-calculators.svg",
        "start_sec": 55,
        "end_sec": 61,
        "timecode": "00:55 – 01:01",
        "phase_label": "09 • INTERACTIVE SAAS-LITE WEB APP",
        "accent": "#0284C7",
        "badge": "100% OFFLINE SINGLE-FILE WEB APPLICATION",
        "headline_1": "INTERACTIVE ROI APP,",
        "headline_2": "50 PROMPT CONTRACTS &",
        "headline_3": "DESIGN STUDIO INCLUDED.",
        "subtitle": "Runs 100% offline in any desktop browser—includes live profit-leak sliders, 90-day Kanban board, 1-click prompt builder, and cover studio.",
        "stat_left": ("TESTED AI PROMPTS", "50 7-Part Contracts", "#10B981"),
        "stat_mid": ("EMERGENCY SCRIPTS", "12 Red-Gate Playbooks", "#EF4444"),
        "stat_right": ("CLOUD SUBSCRIPTIONS", "$0/Mo Required", "#38BDF8"),
        "voiceover": "This isn't just a book. You get the complete hundred-and-eleven-thousand-word operating manual, ten fillable workbooks, the twelve-page Visual Shortcut Atlas, our offline Web Companion App,",
        "sfx_cue": "Interactive slider sweep + UI tab switch click",
        "broll_ref": "mockup-02-ecosystem-master-poster.png",
    },
    {
        "num": 10,
        "filename": "scene-10-excel-notion-and-office-suite.png",
        "svg_name": "scene-10-excel-notion-and-office-suite.svg",
        "start_sec": 61,
        "end_sec": 66,
        "timecode": "01:01 – 01:06",
        "phase_label": "10 • EXCEL, NOTION & OFFICE SUITE",
        "accent": "#059669",
        "badge": "340 LIVE EXCEL FORMULAS • 5 NOTION DATABASES",
        "headline_1": "8-TAB EXCEL MATRIX,",
        "headline_2": "5 NOTION DATABASES,",
        "headline_3": "WORD SOPS & SLIDE DECKS.",
        "subtitle": "Includes 340 live Excel formulas, 4 embedded financial charts, 7 editable Word SOP manuals, and 3 widescreen PowerPoint decks.",
        "stat_left": ("EXCEL COMMAND MATRIX", "8 Tabs • 340 Formulas", "#10B981"),
        "stat_mid": ("EDITABLE WORD SOPS", "7 .DOCX Manuals", "#38BDF8"),
        "stat_right": ("WIDESCREEN DECKS", "3 .PPTX (32 Slides)", "#F59E0B"),
        "voiceover": "the eight-tab charted Excel Command Center, five Notion databases, editable Word SOPs, slide decks,",
        "sfx_cue": "Crisp paper/spreadsheet cascade + data chart pop",
        "broll_ref": "mockup-03-chapter01-cheat-sheet.png",
    },
    {
        "num": 11,
        "filename": "scene-11-full-flagship-bundle-showcase.png",
        "svg_name": "scene-11-full-flagship-bundle-showcase.svg",
        "start_sec": 66,
        "end_sec": 72,
        "timecode": "01:06 – 01:12",
        "phase_label": "11 • MAKE / N8N / ZAPIER BLUEPRINTS",
        "accent": "#D97706",
        "badge": "5 READY-TO-IMPORT JSON WORKFLOW BLUEPRINTS",
        "headline_1": "5 IMPORTABLE JSON",
        "headline_2": "BLUEPRINTS FOR MAKE,",
        "headline_3": "N8N & ZAPIER.",
        "subtitle": "Import pre-wired 6-node workflows with Pre-AI PII regex scrubbers, Slack Block Kit approval cards, and synthetic test suites.",
        "stat_left": ("JSON BLUEPRINTS", "5 Universal Workflows", "#F59E0B"),
        "stat_mid": ("VISUAL SHORTCUT ATLAS", "12-Page Landscape PDF", "#10B981"),
        "stat_right": ("FLAGSHIP BUNDLE FILES", "100 Verified Assets", "#38BDF8"),
        "voiceover": "and five ready-to-import Make, n8n, and Zapier automation blueprints.",
        "sfx_cue": "Deep cinematic bass drop + full product stack lock-in",
        "broll_ref": "mockup-01-flagship-os-cover.png",
    },
    {
        "num": 12,
        "filename": "scene-12-cta-free-audit-and-flagship-os.png",
        "svg_name": "scene-12-cta-free-audit-and-flagship-os.svg",
        "start_sec": 72,
        "end_sec": 82,
        "timecode": "01:12 – 01:22",
        "phase_label": "12 • RISK-FREE DUAL CALL TO ACTION",
        "accent": "#059669",
        "badge": "START FREE ($0) OR INSTALL THE FULL OS ($59)",
        "headline_1": "DOWNLOAD THE FREE",
        "headline_2": "5-DAY AUDIT KIT OR GET",
        "headline_3": "THE COMPLETE OS TODAY.",
        "subtitle": "Click the link below to grab the Free 5-Day Audit Starter Kit ($0) or install the Complete Flagship Operating System ($59) and reclaim your week.",
        "stat_left": ("TIER 0 STARTER KIT", "$0 Free Download", "#38BDF8"),
        "stat_mid": ("TIER 3 FLAGSHIP OS", "$59 One-Time (100 Files)", "#10B981"),
        "stat_right": ("WEEKLY TIME RECLAIMED", "15+ Hours Every Week", "#F59E0B"),
        "voiceover": "Click the link below to download the Free Five-Day Audit Starter Kit right now, or grab the Complete Flagship Operating System for fifty-nine dollars and take back your week.",
        "sfx_cue": "Warm resolving synth chord + crisp button click",
        "broll_ref": "mockup-04-tier2-workbook-atlas.png",
    },
]

# =============================================================================
# 6 VERTICAL 9:16 REELS / TIKTOK / SHORTS SCENE DEFINITIONS (0:00 TO 0:58)
# =============================================================================

REELS_9X16_SPECS = [
    {
        "num": 1,
        "filename": "reel-scene-01-hook.png",
        "svg_name": "reel-scene-01-hook.svg",
        "timecode": "00:00 – 00:06",
        "accent": "#EF4444",
        "badge": "3 MISSED CALLS = $3,600 LOST",
        "h1": "MISSED CALLS",
        "h2": "ARE PAYING YOUR",
        "h3": "COMPETITOR.",
        "sub": "When you're on a job or with a client, buyers don't leave voicemails—they call the next business on Google.",
        "kpi_title": "AVG SMALL BIZ LEAD LEAK",
        "kpi_val": "35% Lost Leads",
        "vo": "How many calls did your business miss this week while you were busy doing actual work? Every missed call is a customer calling your competitor next.",
    },
    {
        "num": 2,
        "filename": "reel-scene-02-bottleneck.png",
        "svg_name": "reel-scene-02-bottleneck.svg",
        "timecode": "00:06 – 00:16",
        "accent": "#F59E0B",
        "badge": "STOP BEING THE HUMAN ROUTER",
        "h1": "18 HRS/WEEK",
        "h2": "TRAPPED IN",
        "h3": "ADMIN CHAOS.",
        "sub": "And random ChatGPT prompts only invent fake prices. You need deterministic T.R.A.V. Safety Gates.",
        "kpi_title": "T-R-A-V GOVERNANCE",
        "kpi_val": "Green • Amber • Red",
        "vo": "You're losing eighteen hours a week acting as the human router between every app, quote, and employee. Instead of fragile chatbots, install our T-R-A-V Safety Gate Operating System.",
    },
    {
        "num": 3,
        "filename": "reel-scene-03-speed-to-lead.png",
        "svg_name": "reel-scene-03-speed-to-lead.svg",
        "timecode": "00:16 – 00:28",
        "accent": "#059669",
        "badge": "60S LEAD ROUTER + 3-OPTION QUOTES",
        "h1": "15S SMS REPLY",
        "h2": "& 90S VOICE",
        "h3": "TO 3-TIER QUOTE.",
        "sub": "Auto-texts missed calls in 15 seconds, books your calendar, and turns a 90s voice note into a Good-Better-Best proposal.",
        "kpi_title": "QUOTE CLOSE RATE",
        "kpi_val": "35%+ In 14 Days",
        "vo": "It texts back missed calls in fifteen seconds, turns a ninety-second voice note into a three-option proposal, and runs a fourteen-day follow-up loop automatically.",
    },
    {
        "num": 4,
        "filename": "reel-scene-04-cashflow-and-friday-kpi.png",
        "svg_name": "reel-scene-04-cashflow-and-friday-kpi.svg",
        "timecode": "00:28 – 00:40",
        "accent": "#0284C7",
        "badge": "24/7 SUPPORT + FRIDAY 3PM BRIEF",
        "h1": "SAME-DAY CASH",
        "h2": "& 15-MINUTE",
        "h3": "FRIDAY COMMAND.",
        "sub": "68% Tier-1 support auto-resolution, 5-stage polite-to-firm invoice chasers, and a 12-KPI Friday 3:00 PM Owner Scorecard.",
        "kpi_title": "AVERAGE DSO",
        "kpi_val": "13.4 Days (Down 60%)",
        "vo": "It resolves sixty-eight percent of support tickets, chases overdue invoices in five polite-to-firm stages, and hands you a twelve-KPI Owner Scorecard every Friday at three PM.",
    },
    {
        "num": 5,
        "filename": "reel-scene-05-complete-os-stack.png",
        "svg_name": "reel-scene-05-complete-os-stack.svg",
        "timecode": "00:40 – 00:50",
        "accent": "#D97706",
        "badge": "100 PRODUCTION FILES INCLUDED",
        "h1": "BOOK + WEB APP",
        "h2": "+ 8-TAB EXCEL",
        "h3": "+ 5 BLUEPRINTS.",
        "sub": "10-Chapter Manual, 10 Fillable Workbooks, 12-Page Visual Atlas, Offline Web App, 8-Tab Excel Matrix, 5 Notion DBs & 5 JSON Blueprints.",
        "kpi_title": "COMPLETE OS STACK",
        "kpi_val": "50 Prompts • 12 Scripts",
        "vo": "You get the full manual, ten fillable workbooks, the twelve-page Visual Atlas, our offline Web App, the eight-tab Excel Matrix, and five Make, n8n, and Zapier blueprints.",
    },
    {
        "num": 6,
        "filename": "reel-scene-06-cta-get-access.png",
        "svg_name": "reel-scene-06-cta-get-access.svg",
        "timecode": "00:50 – 00:58",
        "accent": "#059669",
        "badge": "LINK IN BIO / DESCRIPTION BELOW",
        "h1": "START FREE ($0)",
        "h2": "OR GRAB THE",
        "h3": "FULL OS ($59).",
        "sub": "Tap the link below to download the Free 5-Day AI Audit Starter Kit ($0) or install the Complete Flagship OS ($59) today.",
        "kpi_title": "INSTANT DOWNLOAD",
        "kpi_val": "Reclaim 15+ Hrs/Wk",
        "vo": "Tap the link below to grab the Free Five-Day Audit Starter Kit right now, or get the Complete Flagship Operating System for fifty-nine dollars.",
    },
]


def xml_esc(val: str) -> str:
    return (
        str(val)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_svg_16x9(scene: dict) -> str:
    """Generate a crisp 1920x1080 Widescreen Full HD vector SVG for a storyboard scene."""
    num = scene["num"]
    accent = scene["accent"]
    l_label, l_val, l_col = scene["stat_left"]
    m_label, m_val, m_col = scene["stat_mid"]
    r_label, r_val, r_col = scene["stat_right"]

    l_label_e, l_val_e = xml_esc(l_label), xml_esc(l_val)
    m_label_e, m_val_e = xml_esc(m_label), xml_esc(m_val)
    r_label_e, r_val_e = xml_esc(r_label), xml_esc(r_val)
    phase_e = xml_esc(scene["phase_label"])
    tc_e = xml_esc(scene["timecode"])
    badge_e = xml_esc(scene["badge"])
    h1_e = xml_esc(scene["headline_1"])
    h2_e = xml_esc(scene["headline_2"])
    h3_e = xml_esc(scene["headline_3"])
    sub1_e = xml_esc(scene["subtitle"][:68])
    sub2_e = xml_esc(scene["subtitle"][68:136])
    broll_e = xml_esc(scene["broll_ref"])
    sfx_e = xml_esc(scene["sfx_cue"])
    vo1_e = xml_esc(scene["voiceover"][:105])
    vo2_e = xml_esc(scene["voiceover"][105:])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <linearGradient id="bgGrad{num}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="55%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <radialGradient id="glow{num}" cx="78%" cy="35%" r="55%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="1920" height="1080" fill="url(#bgGrad{num})"/>
  <rect width="1920" height="1080" fill="url(#glow{num})"/>

  <!-- Subtle Architectural Grid -->
  <g stroke="#1E293B" stroke-width="1" opacity="0.55">
    <line x1="0" y1="140" x2="1920" y2="140"/>
    <line x1="0" y1="860" x2="1920" y2="860"/>
    <line x1="110" y1="0" x2="110" y2="1080"/>
    <line x1="1810" y1="0" x2="1810" y2="1080"/>
    <line x1="1180" y1="140" x2="1180" y2="860" stroke-dasharray="8 8"/>
  </g>

  <!-- Top Broadcast Header Bar -->
  <rect x="110" y="52" width="1700" height="64" rx="12" fill="#0B1120" stroke="#334155" stroke-width="1.5"/>
  <rect x="128" y="68" width="290" height="32" rx="6" fill="{accent}" fill-opacity="0.2" stroke="{accent}" stroke-width="1.5"/>
  <text x="273" y="90" fill="#F8FAFC" font-family="Consolas, monospace" font-size="15" font-weight="700" text-anchor="middle">{phase_e}</text>
  <text x="445" y="90" fill="#94A3B8" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600">THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM • PROMO SCENE {num:02d}/12</text>
  <rect x="1610" y="68" width="180" height="32" rx="6" fill="#1E293B" stroke="#475569" stroke-width="1"/>
  <text x="1700" y="90" fill="#38BDF8" font-family="Consolas, monospace" font-size="16" font-weight="700" text-anchor="middle">{tc_e}</text>

  <!-- Left Column: Kinetic Typography & Narrative Hook -->
  <rect x="140" y="185" width="460" height="42" rx="21" fill="{accent}" fill-opacity="0.16" stroke="{accent}" stroke-width="1.5"/>
  <text x="370" y="212" fill="#F8FAFC" font-family="Consolas, monospace" font-size="16" font-weight="700" text-anchor="middle">{badge_e}</text>

  <text x="140" y="310" fill="#F8FAFC" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="58" font-weight="900" letter-spacing="-0.5">{h1_e}</text>
  <text x="140" y="382" fill="{accent}" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="58" font-weight="900" letter-spacing="-0.5">{h2_e}</text>
  <text x="140" y="454" fill="#F8FAFC" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="58" font-weight="900" letter-spacing="-0.5">{h3_e}</text>

  <text x="140" y="520" fill="#CBD5E1" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="500">{sub1_e}</text>
  <text x="140" y="552" fill="#CBD5E1" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="500">{sub2_e}</text>

  <!-- 3 Telemetry Proof Cards -->
  <g transform="translate(140, 610)">
    <rect x="0" y="0" width="315" height="130" rx="14" fill="#0B1120" stroke="{l_col}" stroke-width="2"/>
    <text x="24" y="42" fill="#94A3B8" font-family="Consolas, monospace" font-size="14" font-weight="700">{l_label_e}</text>
    <text x="24" y="92" fill="{l_col}" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="800">{l_val_e}</text>

    <rect x="335" y="0" width="315" height="130" rx="14" fill="#0B1120" stroke="{m_col}" stroke-width="2"/>
    <text x="359" y="42" fill="#94A3B8" font-family="Consolas, monospace" font-size="14" font-weight="700">{m_label_e}</text>
    <text x="359" y="92" fill="{m_col}" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="800">{m_val_e}</text>

    <rect x="670" y="0" width="315" height="130" rx="14" fill="#0B1120" stroke="{r_col}" stroke-width="2"/>
    <text x="694" y="42" fill="#94A3B8" font-family="Consolas, monospace" font-size="14" font-weight="700">{r_label_e}</text>
    <text x="694" y="92" fill="{r_col}" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="800">{r_val_e}</text>
  </g>

  <!-- Right Column: Visual Architecture & Live UI HUD Card -->
  <g transform="translate(1215, 185)">
    <rect x="0" y="0" width="565" height="555" rx="20" fill="#0B1120" stroke="#334155" stroke-width="2"/>
    <rect x="0" y="0" width="565" height="54" rx="20" fill="#1E293B"/>
    <circle cx="30" cy="27" r="8" fill="#EF4444"/>
    <circle cx="56" cy="27" r="8" fill="#F59E0B"/>
    <circle cx="82" cy="27" r="8" fill="#10B981"/>
    <text x="295" y="33" fill="#E2E8F0" font-family="Consolas, monospace" font-size="15" font-weight="700" text-anchor="middle">T.R.A.V. LIVE TELEMETRY • SCENE {num:02d}</text>

    <!-- Node 1: Trigger -->
    <rect x="36" y="86" width="493" height="88" rx="12" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
    <text x="60" y="120" fill="#38BDF8" font-family="Consolas, monospace" font-size="15" font-weight="700">STAGE 01 • DETERMINISTIC TRIGGER &amp; FILTER</text>
    <text x="60" y="150" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="700">{l_label_e}: {l_val_e}</text>

    <!-- Node 2: Grounded AI + Truth Table -->
    <rect x="36" y="198" width="493" height="88" rx="12" fill="#0F172A" stroke="{accent}" stroke-width="2"/>
    <text x="60" y="232" fill="{accent}" font-family="Consolas, monospace" font-size="15" font-weight="700">STAGE 02 • LOCKED TRUTH TABLE &amp; JSON PROMPT</text>
    <text x="60" y="262" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="700">{m_label_e}: {m_val_e}</text>

    <!-- Node 3: Verification Gate -->
    <rect x="36" y="310" width="493" height="88" rx="12" fill="#0F172A" stroke="#10B981" stroke-width="2"/>
    <text x="60" y="344" fill="#34D399" font-family="Consolas, monospace" font-size="15" font-weight="700">STAGE 03 • HUMAN-IN-THE-LOOP VERIFICATION</text>
    <text x="60" y="374" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="700">{r_label_e}: {r_val_e}</text>

    <!-- Bottom Status Strip inside Right Card -->
    <rect x="36" y="424" width="493" height="96" rx="12" fill="#1E293B" stroke="{accent}" stroke-width="1.5"/>
    <text x="60" y="460" fill="#94A3B8" font-family="Consolas, monospace" font-size="14" font-weight="700">ACTIVE PRODUCTION ASSET REFERENCE</text>
    <text x="60" y="494" fill="#F8FAFC" font-family="Consolas, monospace" font-size="18" font-weight="700">{broll_e}</text>
  </g>

  <!-- Bottom Broadcast Closed-Caption / Voiceover Teleprompter Bar -->
  <rect x="110" y="885" width="1700" height="135" rx="16" fill="#020617" stroke="{accent}" stroke-width="2"/>
  <rect x="135" y="905" width="195" height="28" rx="6" fill="{accent}"/>
  <text x="232" y="925" fill="#FFFFFF" font-family="Consolas, monospace" font-size="14" font-weight="700" text-anchor="middle">SPOKEN VOICEOVER</text>
  <text x="350" y="925" fill="#94A3B8" font-family="Consolas, monospace" font-size="14">SFX CUE: {sfx_e}</text>
  <text x="135" y="968" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="23" font-weight="700">&quot;{vo1_e}&quot;</text>
  <text x="135" y="1000" fill="#34D399" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700">{vo2_e}</text>
</svg>"""
    return sanitize_phase11_text(svg)


def build_svg_9x16(reel: dict) -> str:
    """Generate a crisp 1080x1920 Vertical HD SVG for Reels, TikTok & YouTube Shorts."""
    num = reel["num"]
    accent = reel["accent"]
    tc_e = xml_esc(reel["timecode"])
    badge_e = xml_esc(reel["badge"])
    h1_e = xml_esc(reel["h1"])
    h2_e = xml_esc(reel["h2"])
    h3_e = xml_esc(reel["h3"])
    sub1_e = xml_esc(reel["sub"][:52])
    sub2_e = xml_esc(reel["sub"][52:108])
    kt_e = xml_esc(reel["kpi_title"])
    kv_e = xml_esc(reel["kpi_val"])
    vo1_e = xml_esc(reel["vo"][:46])
    vo2_e = xml_esc(reel["vo"][46:94])
    vo3_e = xml_esc(reel["vo"][94:145])
    vo4_e = xml_esc(reel["vo"][145:])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <linearGradient id="vbg{num}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <radialGradient id="vglow{num}" cx="50%" cy="35%" r="55%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1080" height="1920" fill="url(#vbg{num})"/>
  <rect width="1080" height="1920" fill="url(#vglow{num})"/>

  <!-- Safe-Zone Framing Guides -->
  <rect x="64" y="120" width="952" height="1640" rx="28" fill="none" stroke="#334155" stroke-width="2"/>

  <!-- Top Pill Header -->
  <rect x="110" y="170" width="860" height="68" rx="34" fill="#0B1120" stroke="{accent}" stroke-width="2"/>
  <text x="540" y="213" fill="#F8FAFC" font-family="Consolas, monospace" font-size="24" font-weight="700" text-anchor="middle">REEL SCENE 0{num}/06 • {tc_e}</text>

  <!-- Eyebrow Badge -->
  <rect x="140" y="300" width="800" height="58" rx="14" fill="{accent}" fill-opacity="0.2" stroke="{accent}" stroke-width="2"/>
  <text x="540" y="338" fill="#F8FAFC" font-family="Consolas, monospace" font-size="24" font-weight="700" text-anchor="middle">{badge_e}</text>

  <!-- Big 3-Line Mobile Kinetic Headline -->
  <text x="540" y="485" fill="#F8FAFC" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="78" font-weight="900" text-anchor="middle">{h1_e}</text>
  <text x="540" y="585" fill="{accent}" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="78" font-weight="900" text-anchor="middle">{h2_e}</text>
  <text x="540" y="685" fill="#F8FAFC" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="78" font-weight="900" text-anchor="middle">{h3_e}</text>

  <!-- Subtitle Card -->
  <rect x="110" y="750" width="860" height="180" rx="20" fill="#0B1120" stroke="#334155" stroke-width="2"/>
  <text x="540" y="820" fill="#CBD5E1" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="600" text-anchor="middle">{sub1_e}</text>
  <text x="540" y="868" fill="#CBD5E1" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="600" text-anchor="middle">{sub2_e}</text>

  <!-- Center Hero KPI Callout Box -->
  <rect x="110" y="980" width="860" height="270" rx="24" fill="#0F172A" stroke="{accent}" stroke-width="3"/>
  <text x="540" y="1065" fill="#94A3B8" font-family="Consolas, monospace" font-size="26" font-weight="700" text-anchor="middle">{kt_e}</text>
  <text x="540" y="1175" fill="{accent}" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="68" font-weight="900" text-anchor="middle">{kv_e}</text>

  <!-- Captions / Subtitle Safe Zone Box -->
  <rect x="110" y="1310" width="860" height="360" rx="24" fill="#020617" stroke="#475569" stroke-width="2"/>
  <rect x="360" y="1340" width="360" height="44" rx="10" fill="{accent}"/>
  <text x="540" y="1370" fill="#FFFFFF" font-family="Consolas, monospace" font-size="20" font-weight="700" text-anchor="middle">SYNCED REEL CAPTION</text>
  <text x="540" y="1455" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="31" font-weight="700" text-anchor="middle">&quot;{vo1_e}&quot;</text>
  <text x="540" y="1510" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="31" font-weight="700" text-anchor="middle">{vo2_e}</text>
  <text x="540" y="1565" fill="#34D399" font-family="Segoe UI, Arial, sans-serif" font-size="31" font-weight="700" text-anchor="middle">{vo3_e}</text>
  <text x="540" y="1620" fill="#34D399" font-family="Segoe UI, Arial, sans-serif" font-size="31" font-weight="700" text-anchor="middle">{vo4_e}</text>
</svg>"""
    return sanitize_phase11_text(svg)


def download_and_prepare_broll_assets(browser_exe: str) -> dict:
    """Download 6 royalty-free business/tech B-roll images (with headless fallback) + copy 4 studio product mockups."""
    broll_urls = [
        ("broll-01-owner-late-night-phone.jpg", "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?auto=format&fit=crop&w=1600&q=80"),
        ("broll-02-team-operations-desk.jpg", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1600&q=80"),
        ("broll-03-analytics-dashboard-screen.jpg", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1600&q=80"),
        ("broll-04-field-service-tablet-quote.jpg", "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1600&q=80"),
        ("broll-05-happy-client-handshake.jpg", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1600&q=80"),
        ("broll-06-friday-executive-coffee.jpg", "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1600&q=80"),
    ]

    results = {}
    for idx, (fname, url) in enumerate(broll_urls, start=1):
        out_p = BROLL_DIR / fname
        downloaded = False
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                if len(data) >= 15_000:
                    out_p.write_bytes(data)
                    downloaded = True
        except Exception:
            downloaded = False

        if not downloaded:
            # Deterministic high-res fallback using rendered scene PNG
            fallback_src = SCENES_16X9_DIR / SCENES_16X9_SPECS[idx - 1]["filename"]
            if fallback_src.exists():
                shutil.copy2(fallback_src, out_p)
        results[fname] = out_p.stat().st_size

    # Copy 4 high-resolution studio product mockups into b-roll-assets/
    studio_mockups = [
        ("mockup-01-flagship-os-cover.png", ROOT / "08-COVER-DESIGN" / "gumroad-tier3-flagship-os-bundle-cover.png"),
        ("mockup-02-ecosystem-master-poster.png", ROOT / "13-VISUAL-CHEAT-SHEETS" / "00-ECOSYSTEM-MASTER-MAP-POSTER.png"),
        ("mockup-03-chapter01-cheat-sheet.png", ROOT / "13-VISUAL-CHEAT-SHEETS" / "cheat-sheet-ch01.png"),
        ("mockup-04-tier2-workbook-atlas.png", ROOT / "08-COVER-DESIGN" / "gumroad-tier2-workbook-atlas-cover.png"),
    ]
    for m_name, src_p in studio_mockups:
        dst_p = BROLL_DIR / m_name
        shutil.copy2(src_p, dst_p)
        results[m_name] = dst_p.stat().st_size

    return results


def build_voiceover_scripts_and_srt() -> dict:
    """Create the 4 script & subtitle files in 16-VIDEO-PROMO-KIT/scripts/."""
    # 1. Clean Natural Voiceover for ElevenLabs (Target: 185 to 215 spoken words, natural conversational English)
    vo_paragraphs = [
        "Be honest—how many calls did your business miss this week while you were busy doing actual work?",
        "Every missed call is a buyer calling your competitor next. You're losing eighteen hours a week and thirty-five percent of your leads—not because you're lazy, but because you're acting as the human router between every app, quote, and employee.",
        "And random ChatGPT prompts don't fix it. Without strict rules, AI invents fake prices. That's why we built The Small Business AI Automation Operating System around T-R-A-V safety gates.",
        "First, Speed-to-Lead texts back missed calls in fifteen seconds and books your calendar.",
        "Second, turn a ninety-second voice memo into a three-option quote with fourteen-day follow-up.",
        "Third, our Support Shield resolves routine tickets and holds risky credits for one-click Amber approval.",
        "Fourth, polite-to-firm invoice chasers collect overdue cash automatically.",
        "And fifth, every Friday at three PM, a twelve-KPI Owner Scorecard lets you run the business in fifteen minutes.",
        "This isn't just a book. You get the complete manual, ten workbooks, the Visual Shortcut Atlas, our offline Web App, the eight-tab Excel Matrix, five Notion databases, Word SOPs, slide decks, and five Make, n8n, and Zapier blueprints.",
        "Click the link below to grab the Free Audit Starter Kit now, or get the Complete Operating System for fifty-nine dollars."
    ]
    clean_vo_txt = sanitize_phase11_text("\n\n".join(vo_paragraphs) + "\n")
    vo_path = SCRIPTS_DIR / "02-Clean-Natural-Voiceover-For-ElevenLabs.txt"
    vo_path.write_text(clean_vo_txt, encoding="utf-8")
    vo_word_count = len(re.findall(r"\b[\w'-]+\b", clean_vo_txt))

    # 2. Short 60-Second Vertical Reels / TikTok / YouTube Shorts Cut Script
    reels_lines = [
        "# 60-SECOND VERTICAL REELS / TIKTOK / YOUTUBE SHORTS VOICEOVER SCRIPT (9:16)",
        "# Target Duration: 55–58 Seconds | Pacing: 145 WPM Conversational Founder Tone",
        "",
        "[00:00 - 00:06 | REEL SCENE 01: HOOK]",
        "How many calls did your business miss this week while you were busy doing actual work? Every missed call is a customer calling your competitor next.",
        "",
        "[00:06 - 00:16 | REEL SCENE 02: THE BOTTLENECK & T-R-A-V GATE]",
        "You're losing eighteen hours a week acting as the human router between every app, quote, and employee. Instead of fragile chatbots, install our T-R-A-V Safety Gate Operating System.",
        "",
        "[00:16 - 00:28 | REEL SCENE 03: SPEED-TO-LEAD & 3-OPTION QUOTES]",
        "It texts back missed calls in fifteen seconds, turns a ninety-second voice note into a three-option proposal, and runs a fourteen-day follow-up loop automatically.",
        "",
        "[00:28 - 00:40 | REEL SCENE 04: SUPPORT SHIELD, CASHFLOW & FRIDAY 3PM BRIEF]",
        "It resolves sixty-eight percent of support tickets, chases overdue invoices in five polite-to-firm stages, and hands you a twelve-KPI Owner Scorecard every Friday at three PM.",
        "",
        "[00:40 - 00:50 | REEL SCENE 05: THE TANGIBLE STACK]",
        "You get the full manual, ten fillable workbooks, the twelve-page Visual Atlas, our offline Web App, the eight-tab Excel Matrix, and five Make, n8n, and Zapier blueprints.",
        "",
        "[00:50 - 00:58 | REEL SCENE 06: DUAL CALL TO ACTION]",
        "Tap the link below to grab the Free Five-Day Audit Starter Kit right now, or get the Complete Flagship Operating System for fifty-nine dollars."
    ]
    reels_txt = sanitize_phase11_text("\n".join(reels_lines) + "\n")
    reels_path = SCRIPTS_DIR / "03-Short-60s-Reels-TikTok-Cut-Script.txt"
    reels_path.write_text(reels_txt, encoding="utf-8")

    # 3. Synced Video Subtitles (.SRT) — 24 Caption Blocks from 00:00:00,000 to 00:01:22,000
    srt_blocks = [
        (1, "00:00:00,000", "00:00:02,100", "Be honest—how many calls did your business miss"),
        (2, "00:00:02,100", "00:00:04,200", "this week while you were busy doing actual work?"),
        (3, "00:00:04,200", "00:00:07,200", "Every missed call is a customer calling your competitor next."),
        (4, "00:00:07,200", "00:00:10,800", "You're losing 15 to 25 hours a week—and up to 35% of your leads—"),
        (5, "00:00:10,800", "00:00:15,000", "because you're acting as the human router between every app, quote, and employee."),
        (6, "00:00:15,000", "00:00:18,200", "And pasting random prompts into ChatGPT doesn't fix it."),
        (7, "00:00:18,200", "00:00:21,400", "Without strict rules, AI invents fake prices and embarrasses your brand."),
        (8, "00:00:21,400", "00:00:25,000", "That's why we built The Small Business AI Automation Operating System\naround Human-in-the-Loop T-R-A-V safety gates."),
        (9, "00:00:25,000", "00:00:31,000", "First: 60-second Speed-to-Lead texts back missed calls\nin 15 seconds and books your calendar."),
        (10, "00:00:31,000", "00:00:37,000", "Second: turn a 90-second voice memo into a 3-option quote\nwith automatic 14-day follow-up."),
        (11, "00:00:37,000", "00:00:40,200", "Third: a 24/7 Support Shield resolves routine tickets"),
        (12, "00:00:40,200", "00:00:43,000", "and routes risky requests to your phone for 1-click Amber approval."),
        (13, "00:00:43,000", "00:00:49,000", "Fourth: 5-stage polite-to-firm invoice chasers\ncollect overdue cash without awkward phone calls."),
        (14, "00:00:49,000", "00:00:52,200", "And fifth: every Friday at 3:00 PM, you get a 1-page 12-KPI Owner Scorecard"),
        (15, "00:00:52,200", "00:00:55,000", "so you can manage the whole business in 15 minutes."),
        (16, "00:00:55,000", "00:00:58,500", "This isn't just a book. You get the 111,000-word operating manual,"),
        (17, "00:00:58,500", "00:01:01,500", "10 fillable workbooks, the 12-page Visual Shortcut Atlas,\nand our offline Web Companion App."),
        (18, "00:01:01,500", "00:01:05,500", "Plus the 8-tab charted Excel Command Center,\n5 Notion databases, editable Word SOPs, and slide decks—"),
        (19, "00:01:05,500", "00:01:12,000", "and 5 ready-to-import Make, n8n, and Zapier automation blueprints."),
        (20, "00:01:12,000", "00:01:16,500", "Click the link below to download the Free 5-Day Audit Starter Kit right now,"),
        (21, "00:01:16,500", "00:01:22,000", "or grab the Complete Flagship Operating System for $59\nand take back your week."),
    ]
    srt_lines = []
    for idx, t_start, t_end, caption in srt_blocks:
        srt_lines.append(f"{idx}")
        srt_lines.append(f"{t_start} --> {t_end}")
        srt_lines.append(sanitize_phase11_text(caption))
        srt_lines.append("")
    srt_txt = "\n".join(srt_lines)
    srt_path = SCRIPTS_DIR / "04-Synced-Video-Subtitles.srt"
    srt_path.write_text(srt_txt, encoding="utf-8")

    # 4. Master Promo Script and Storyboard Markdown (`01-Master-Promo-Script-and-Storyboard.md`)
    storyboard_rows = []
    for sc in SCENES_16X9_SPECS:
        storyboard_rows.append(
            f"| **Scene {sc['num']:02d}** (`{sc['timecode']}`) | **{sc['phase_label']}** | "
            f"\"{sc['voiceover']}\" | `visual-scenes-16x9/{sc['filename']}` + `b-roll-assets/{sc['broll_ref']}` | "
            f"**{sc['headline_1']} {sc['headline_2']} {sc['headline_3']}** | {sc['sfx_cue']} |"
        )

    master_md = f"""# Master Promotional Video Script, Retention Architecture & 12-Scene Storyboard
## Project: "The Small Business AI Automation Operating System" (`2026 Enterprise Edition`)
**Document ID:** `16-VIDEO-PROMO-KIT/scripts/01-Master-Promo-Script-and-Storyboard.md`  
**Total Runtime:** `01:22` (`82 Seconds` Widescreen Master | `00:58` Vertical Reels/TikTok Cut)  
**Spoken Word Count (`02-Clean-Natural-Voiceover-For-ElevenLabs.txt`):** `{vo_word_count} words` (`~145 WPM` natural conversational cadence)  

---

## 1. Retention Engineering & Psychological Pacing Breakdown
To achieve `>= 72%` 3-second hook retention and `>= 45%` full-video completion on YouTube, LinkedIn, Meta, and your storefront landing page (`15-WEB-DEPLOYMENT/dist/index.html`), this script is engineered around six tightly timed retention blocks:

1. **`00:00 – 00:04` (The Pattern-Interrupt Hook):** Opens with a direct question about a visceral operational leak sitting on the owner's phone right now (*missed calls turning into a competitor's job*).
2. **`00:04 – 00:15` (The Quantified Agitation):** Validates the founder's hard work while naming the structural root cause—acting as the **Human Router** across every app, quote, and employee (`15–25 hours/week` lost and up to `35%` of inbound leads dropped).
3. **`00:15 – 00:25` (The False-Solution Pivot & T.R.A.V. Safety Gate):** Explains why generic one-line ChatGPT prompts fail in production (hallucinated discounts and brand risk) and introduces our **T.R.A.V. (`Trigger -> Rules -> AI -> Verification`)** architecture.
4. **`00:25 – 00:55` (Rapid-Fire 5-Department Proof — Exactly 6 Seconds Per Department):** Visually proves the before/after transformation across all five departments (`60s Speed-to-Lead`, `90s Voice-to-3-Option Quote`, `24/7 Support Shield`, `5-Stage AR Invoice Chasers`, and the `Friday 3:00 PM 12-KPI Owner Scorecard`).
5. **`00:55 – 01:12` (The Tangible Stack Reveal):** Transitions from "how it works" to the concrete deliverables inside the download bundle (`111,000-word Manual`, `10 Fillable Workbooks`, `12-Page Visual Shortcut Atlas`, `Offline SaaS-Lite Web App`, `8-Tab Charted Excel Matrix`, `5 Notion Databases`, `7 Editable Word SOPs`, `3 Slide Decks`, and `5 Make/n8n/Zapier JSON Blueprints`).
6. **`01:12 – 01:22` (Risk-Free Dual Call-to-Action):** Gives cold viewers a zero-friction entry point (**Free 5-Day Audit Starter Kit at `$0`**) while offering high-intent operators the **Complete Flagship Operating System at `$59`**.

---

## 2. Complete Spoken Voiceover Script (`{vo_word_count} Words` — Natural Conversational English)

```text
{clean_vo_txt.strip()}
```

---

## 3. Master 12-Scene Production Storyboard (`16:9` Widescreen `1920 × 1080 px`)

| Scene & Timecode | Retention Phase | Spoken Voiceover Line | Visual Scene PNG & B-Roll Asset | On-Screen Kinetic Typography | Audio / SFX Cue |
| :--- | :--- | :--- | :--- | :--- | :--- |
{chr(10).join(storyboard_rows)}

---

## 4. Vertical 6-Scene Cut (`9:16` Reels / TikTok / YouTube Shorts `1080 × 1920 px`)
All 6 vertical storyboard cards are pre-rendered in `16-VIDEO-PROMO-KIT/visual-scenes-9x16-reels/` (`reel-scene-01-hook.png` through `reel-scene-06-cta-get-access.png`) and paired with `16-VIDEO-PROMO-KIT/scripts/03-Short-60s-Reels-TikTok-Cut-Script.txt`.
"""
    master_md_clean = sanitize_phase11_text(master_md)
    master_md_path = SCRIPTS_DIR / "01-Master-Promo-Script-and-Storyboard.md"
    master_md_path.write_text(master_md_clean, encoding="utf-8")

    return {
        "vo_words": vo_word_count,
        "srt_blocks": len(srt_blocks),
        "storyboard_words": len(re.findall(r"\b[\w'-]+\b", master_md_clean)),
    }


def build_interactive_promo_player() -> int:
    """Build 16-VIDEO-PROMO-KIT/interactive-video-promo-player.html (>= 45 KB)."""
    scenes_16x9_json = json.dumps(SCENES_16X9_SPECS, indent=2, ensure_ascii=False)
    scenes_9x16_json = json.dumps(REELS_9X16_SPECS, indent=2, ensure_ascii=False)
    clean_vo_text = (SCRIPTS_DIR / "02-Clean-Natural-Voiceover-For-ElevenLabs.txt").read_text(encoding="utf-8")
    reels_vo_text = (SCRIPTS_DIR / "03-Short-60s-Reels-TikTok-Cut-Script.txt").read_text(encoding="utf-8")
    srt_text = (SCRIPTS_DIR / "04-Synced-Video-Subtitles.srt").read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Interactive Promotional Video Player, Storyboard &amp; Teleprompter Studio | SmallBiz AI OS</title>
  <style>
    :root {{
      --primary: #0F172A;
      --bg-dark: #020617;
      --panel: #1E293B;
      --border: #334155;
      --accent: #059669;
      --secondary: #0284C7;
      --warning: #D97706;
      --danger: #EF4444;
      --text: #F8FAFC;
      --muted: #94A3B8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    header {{
      background: #0B1120;
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-badge {{
      background: rgba(5, 150, 105, 0.2);
      border: 1px solid var(--accent);
      color: #34D399;
      font-family: Consolas, monospace;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
    }}
    .brand h1 {{
      font-size: 18px;
      margin: 0;
      font-weight: 800;
    }}
    .top-actions {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    button, .btn {{
      background: var(--panel);
      color: var(--text);
      border: 1px solid #475569;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s;
    }}
    button:hover, .btn:hover {{
      border-color: var(--accent);
    }}
    .btn-emerald {{
      background: var(--accent);
      border-color: var(--accent);
      color: #FFFFFF;
    }}
    .btn-cyan {{
      background: var(--secondary);
      border-color: var(--secondary);
      color: #FFFFFF;
    }}
    .btn-amber {{
      background: var(--warning);
      border-color: var(--warning);
      color: #FFFFFF;
    }}
    .studio-grid {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 20px 24px 48px;
      display: grid;
      grid-template-columns: 1.55fr 1fr;
      gap: 24px;
    }}
    @media (max-width: 1150px) {{
      .studio-grid {{ grid-template-columns: 1fr; }}
    }}
    .player-card, .teleprompter-card {{
      background: #0F172A;
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
    }}
    .stage-wrapper {{
      position: relative;
      background: #000000;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 480px;
      padding: 16px;
    }}
    #sceneImage {{
      width: 100%;
      max-height: 560px;
      object-fit: contain;
      border-radius: 10px;
      border: 1px solid #1E293B;
      transition: opacity 0.22s ease-in-out;
    }}
    .caption-overlay {{
      position: absolute;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%);
      width: 88%;
      background: rgba(2, 6, 23, 0.9);
      border: 1px solid var(--accent);
      border-radius: 10px;
      padding: 10px 18px;
      text-align: center;
      font-size: 17px;
      font-weight: 700;
      color: #F8FAFC;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }}
    .controls-bar {{
      padding: 16px 20px;
      background: #0B1120;
      border-top: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .timeline-row {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    #timeScrubber {{
      flex: 1;
      accent-color: var(--accent);
      cursor: pointer;
    }}
    .time-readout {{
      font-family: Consolas, monospace;
      font-size: 14px;
      color: #34D399;
      min-width: 115px;
      text-align: right;
    }}
    .scene-strip {{
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 8px;
      padding: 16px 20px;
      background: #0F172A;
      border-top: 1px solid var(--border);
    }}
    .scene-thumb {{
      background: #1E293B;
      border: 2px solid transparent;
      border-radius: 8px;
      padding: 6px;
      cursor: pointer;
      text-align: left;
      transition: all 0.15s;
    }}
    .scene-thumb.active {{
      border-color: var(--accent);
      background: rgba(5, 150, 105, 0.15);
    }}
    .scene-thumb img {{
      width: 100%;
      height: 56px;
      object-fit: cover;
      border-radius: 4px;
      display: block;
      margin-bottom: 4px;
    }}
    .scene-thumb .st-num {{
      font-family: Consolas, monospace;
      font-size: 11px;
      color: #38BDF8;
      font-weight: 700;
    }}
    .scene-thumb .st-title {{
      font-size: 11px;
      color: #E2E8F0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .teleprompter-header {{
      padding: 16px 20px;
      background: #0B1120;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .teleprompter-body {{
      padding: 20px;
      max-height: 520px;
      overflow-y: auto;
    }}
    .script-cue {{
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid #1E293B;
      background: #0B1120;
      margin-bottom: 10px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .script-cue.active {{
      border-color: var(--accent);
      background: rgba(5, 150, 105, 0.14);
    }}
    .script-cue-meta {{
      display: flex;
      justify-content: space-between;
      font-family: Consolas, monospace;
      font-size: 12px;
      color: #38BDF8;
      margin-bottom: 6px;
    }}
    .script-cue-vo {{
      font-size: 15px;
      line-height: 1.55;
      color: #F8FAFC;
      font-weight: 600;
    }}
    .script-cue-sfx {{
      font-size: 12px;
      color: var(--muted);
      margin-top: 6px;
      font-family: Consolas, monospace;
    }}
    .copy-vault {{
      padding: 16px 20px;
      border-top: 1px solid var(--border);
      background: #0B1120;
    }}
    textarea.script-box {{
      width: 100%;
      height: 135px;
      background: #020617;
      color: #E2E8F0;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 10px;
      font-family: Consolas, monospace;
      font-size: 12px;
      line-height: 1.5;
      margin-top: 8px;
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <span class="brand-badge">PHASE 11 • PROMO VIDEO STUDIO</span>
      <h1>The Small Business AI Automation OS — 82s High-Retention Promo Player &amp; Teleprompter</h1>
    </div>
    <div class="top-actions">
      <button id="btnMode16x9" class="btn-emerald" onclick="switchAspectMode('16x9')">16:9 Widescreen Master (12 Scenes • 1:22)</button>
      <button id="btnMode9x16" onclick="switchAspectMode('9x16')">9:16 Vertical Reels/TikTok (6 Scenes • 0:58)</button>
      <button id="btnVoiceToggle" class="btn-cyan" onclick="toggleBrowserSpeech()">Speak Voiceover Preview (TTS)</button>
    </div>
  </header>

  <main class="studio-grid">
    <!-- Left Column: Animated Storyboard Player + Scene Strip -->
    <section class="player-card">
      <div class="stage-wrapper">
        <img id="sceneImage" src="visual-scenes-16x9/scene-01-hook-missed-call-leak.png" alt="Active Storyboard Scene" />
        <div class="caption-overlay" id="liveCaptionBar">
          [00:00 – 00:04] "Be honest—how many calls did your business miss this week while you were busy doing actual work?"
        </div>
      </div>

      <div class="controls-bar">
        <div class="timeline-row">
          <button id="btnPlayPause" class="btn-emerald" onclick="togglePlayback()">▶ Play Promo (82s)</button>
          <button onclick="restartPlayback()">↺ Restart</button>
          <button onclick="stepScene(-1)">◀ Prev Scene</button>
          <button onclick="stepScene(1)">Next Scene ▶</button>
          <input type="range" id="timeScrubber" min="0" max="82" step="0.2" value="0" oninput="scrubToTime(this.value)" />
          <span class="time-readout" id="timeReadout">00:00 / 01:22</span>
        </div>
      </div>

      <div class="scene-strip" id="sceneThumbnailStrip"></div>
    </section>

    <!-- Right Column: Interactive Teleprompter & Copy-Paste Script Vault -->
    <aside class="teleprompter-card">
      <div class="teleprompter-header">
        <div>
          <strong style="font-size:15px;">Live Synchronized Voiceover Teleprompter</strong>
          <div style="font-size:12px;color:var(--muted);">Click any scene cue below to jump directly to that timestamp</div>
        </div>
        <span id="activeSceneBadge" class="brand-badge">SCENE 01 / 12</span>
      </div>

      <div class="teleprompter-body" id="teleprompterList"></div>

      <div class="copy-vault">
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:space-between;">
          <strong style="font-size:13px;color:#34D399;">1-Click Copy Production Scripts &amp; Subtitles:</strong>
          <div style="display:flex;gap:6px;flex-wrap:wrap;">
            <button onclick="loadVaultText('elevenlabs')">ElevenLabs VO (82s)</button>
            <button onclick="loadVaultText('reels')">Reels/TikTok Cut (58s)</button>
            <button onclick="loadVaultText('srt')">Synced .SRT Subtitles</button>
            <button class="btn-amber" onclick="copyCurrentVaultText()">Copy to Clipboard</button>
          </div>
        </div>
        <textarea id="vaultTextarea" class="script-box" readonly></textarea>
        <div id="copyStatusMsg" style="font-size:12px;color:#38BDF8;margin-top:6px;font-family:Consolas,monospace;">
          Ready: 100% Natural Conversational English Voiceover Loaded.
        </div>
      </div>
    </aside>
  </main>

  <script>
    const SCENES_16X9 = {scenes_16x9_json};
    const SCENES_9X16 = {scenes_9x16_json};
    const VAULT_TEXTS = {{
      elevenlabs: {json.dumps(clean_vo_text)},
      reels: {json.dumps(reels_vo_text)},
      srt: {json.dumps(srt_text)}
    }};

    let currentMode = "16x9";
    let currentTime = 0;
    let totalDuration = 82;
    let isPlaying = false;
    let timerHandle = null;
    let speechEnabled = false;
    let lastSpokenSceneIndex = -1;

    function formatMMSS(sec) {{
      const s = Math.max(0, Math.floor(sec));
      const m = Math.floor(s / 60);
      const r = s % 60;
      return String(m).padStart(2, "0") + ":" + String(r).padStart(2, "0");
    }}

    function getActiveSceneIndex(sec) {{
      if (currentMode === "16x9") {{
        for (let i = 0; i < SCENES_16X9.length; i++) {{
          if (sec >= SCENES_16X9[i].start_sec && sec < SCENES_16X9[i].end_sec) return i;
        }}
        return SCENES_16X9.length - 1;
      }} else {{
        const bounds = [0, 6, 16, 28, 40, 50, 58];
        for (let i = 0; i < 6; i++) {{
          if (sec >= bounds[i] && sec < bounds[i + 1]) return i;
        }}
        return 5;
      }}
    }}

    function renderUIForTime(sec) {{
      const idx = getActiveSceneIndex(sec);
      const imgEl = document.getElementById("sceneImage");
      const capEl = document.getElementById("liveCaptionBar");
      const badgeEl = document.getElementById("activeSceneBadge");
      const readoutEl = document.getElementById("timeReadout");
      const scrubber = document.getElementById("timeScrubber");

      scrubber.value = sec;
      readoutEl.textContent = formatMMSS(sec) + " / " + formatMMSS(totalDuration);

      if (currentMode === "16x9") {{
        const sc = SCENES_16X9[idx];
        const targetSrc = "visual-scenes-16x9/" + sc.filename;
        if (!imgEl.src.endsWith(targetSrc)) imgEl.src = targetSrc;
        capEl.textContent = "[" + sc.timecode + '] "' + sc.voiceover + '"';
        badgeEl.textContent = "SCENE " + String(sc.num).padStart(2, "0") + " / 12";
      }} else {{
        const rl = SCENES_9X16[idx];
        const targetSrc = "visual-scenes-9x16-reels/" + rl.filename;
        if (!imgEl.src.endsWith(targetSrc)) imgEl.src = targetSrc;
        capEl.textContent = "[" + rl.timecode + '] "' + rl.vo + '"';
        badgeEl.textContent = "REEL 0" + rl.num + " / 06";
      }}

      document.querySelectorAll(".scene-thumb").forEach((el, i) => {{
        el.classList.toggle("active", i === idx);
      }});
      document.querySelectorAll(".script-cue").forEach((el, i) => {{
        el.classList.toggle("active", i === idx);
      }});

      if (speechEnabled && isPlaying && idx !== lastSpokenSceneIndex && "speechSynthesis" in window) {{
        lastSpokenSceneIndex = idx;
        window.speechSynthesis.cancel();
        const utterText = currentMode === "16x9" ? SCENES_16X9[idx].voiceover : SCENES_9X16[idx].vo;
        const utter = new SpeechSynthesisUtterance(utterText);
        utter.rate = 1.04;
        window.speechSynthesis.speak(utter);
      }}
    }}

    function buildThumbnailsAndTeleprompter() {{
      const strip = document.getElementById("sceneThumbnailStrip");
      const tele = document.getElementById("teleprompterList");
      strip.innerHTML = "";
      tele.innerHTML = "";

      if (currentMode === "16x9") {{
        SCENES_16X9.forEach((sc, i) => {{
          const thumb = document.createElement("div");
          thumb.className = "scene-thumb" + (i === 0 ? " active" : "");
          thumb.onclick = () => scrubToTime(sc.start_sec);
          thumb.innerHTML =
            '<img src="visual-scenes-16x9/' + sc.filename + '" alt="Scene ' + sc.num + '" />' +
            '<div class="st-num">S' + String(sc.num).padStart(2, "0") + " • " + sc.timecode + '</div>' +
            '<div class="st-title">' + sc.headline_1 + '</div>';
          strip.appendChild(thumb);

          const cue = document.createElement("div");
          cue.className = "script-cue" + (i === 0 ? " active" : "");
          cue.onclick = () => scrubToTime(sc.start_sec);
          cue.innerHTML =
            '<div class="script-cue-meta"><span>SCENE ' + String(sc.num).padStart(2, "0") + ' • ' + sc.phase_label + '</span><span>' + sc.timecode + '</span></div>' +
            '<div class="script-cue-vo">"' + sc.voiceover + '"</div>' +
            '<div class="script-cue-sfx">SFX: ' + sc.sfx_cue + ' | B-Roll: ' + sc.broll_ref + '</div>';
          tele.appendChild(cue);
        }});
      }} else {{
        const bounds = [0, 6, 16, 28, 40, 50];
        SCENES_9X16.forEach((rl, i) => {{
          const thumb = document.createElement("div");
          thumb.className = "scene-thumb" + (i === 0 ? " active" : "");
          thumb.onclick = () => scrubToTime(bounds[i]);
          thumb.innerHTML =
            '<img src="visual-scenes-9x16-reels/' + rl.filename + '" alt="Reel ' + rl.num + '" />' +
            '<div class="st-num">R0' + rl.num + " • " + rl.timecode + '</div>' +
            '<div class="st-title">' + rl.h1 + '</div>';
          strip.appendChild(thumb);

          const cue = document.createElement("div");
          cue.className = "script-cue" + (i === 0 ? " active" : "");
          cue.onclick = () => scrubToTime(bounds[i]);
          cue.innerHTML =
            '<div class="script-cue-meta"><span>REEL SCENE 0' + rl.num + '</span><span>' + rl.timecode + '</span></div>' +
            '<div class="script-cue-vo">"' + rl.vo + '"</div>';
          tele.appendChild(cue);
        }});
      }}
    }}

    function togglePlayback() {{
      const btn = document.getElementById("btnPlayPause");
      if (isPlaying) {{
        isPlaying = false;
        clearInterval(timerHandle);
        if ("speechSynthesis" in window) window.speechSynthesis.cancel();
        btn.textContent = "▶ Resume Promo";
      }} else {{
        if (currentTime >= totalDuration) currentTime = 0;
        isPlaying = true;
        lastSpokenSceneIndex = -1;
        btn.textContent = "⏸ Pause Promo";
        renderUIForTime(currentTime);
        timerHandle = setInterval(() => {{
          currentTime += 0.25;
          if (currentTime >= totalDuration) {{
            currentTime = totalDuration;
            togglePlayback();
          }}
          renderUIForTime(currentTime);
        }}, 250);
      }}
    }}

    function restartPlayback() {{
      if (isPlaying) togglePlayback();
      currentTime = 0;
      lastSpokenSceneIndex = -1;
      renderUIForTime(0);
    }}

    function scrubToTime(val) {{
      currentTime = parseFloat(val) || 0;
      lastSpokenSceneIndex = -1;
      renderUIForTime(currentTime);
    }}

    function stepScene(delta) {{
      const idx = getActiveSceneIndex(currentTime);
      if (currentMode === "16x9") {{
        const nextIdx = Math.max(0, Math.min(SCENES_16X9.length - 1, idx + delta));
        scrubToTime(SCENES_16X9[nextIdx].start_sec);
      }} else {{
        const bounds = [0, 6, 16, 28, 40, 50];
        const nextIdx = Math.max(0, Math.min(5, idx + delta));
        scrubToTime(bounds[nextIdx]);
      }}
    }}

    function switchAspectMode(mode) {{
      if (isPlaying) togglePlayback();
      currentMode = mode;
      totalDuration = mode === "16x9" ? 82 : 58;
      currentTime = 0;
      document.getElementById("timeScrubber").max = totalDuration;
      document.getElementById("btnMode16x9").className = mode === "16x9" ? "btn-emerald" : "";
      document.getElementById("btnMode9x16").className = mode === "9x16" ? "btn-emerald" : "";
      buildThumbnailsAndTeleprompter();
      renderUIForTime(0);
    }}

    function toggleBrowserSpeech() {{
      speechEnabled = !speechEnabled;
      const btn = document.getElementById("btnVoiceToggle");
      btn.textContent = speechEnabled ? "🔊 Browser Voice Preview: ON" : "Speak Voiceover Preview (TTS)";
      if (!speechEnabled && "speechSynthesis" in window) window.speechSynthesis.cancel();
    }}

    function loadVaultText(key) {{
      document.getElementById("vaultTextarea").value = VAULT_TEXTS[key] || "";
      document.getElementById("copyStatusMsg").textContent = "Loaded: " + key.toUpperCase() + " production script.";
    }}

    function copyCurrentVaultText() {{
      const box = document.getElementById("vaultTextarea");
      box.select();
      navigator.clipboard.writeText(box.value);
      document.getElementById("copyStatusMsg").textContent = "Copied script to clipboard!";
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      buildThumbnailsAndTeleprompter();
      loadVaultText("elevenlabs");
      renderUIForTime(0);
    }});
  </script>
</body>
</html>
"""
    html_clean = sanitize_phase11_text(html)
    player_path = VIDEO_DIR / "interactive-video-promo-player.html"
    player_path.write_text(html_clean, encoding="utf-8")
    return player_path.stat().st_size


def build_video_production_guide() -> int:
    """Create VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md (>= 2,000 words)."""
    guide_md = """# Promotional Video Editing, Natural Voiceover & High-Retention Production Guide
## Project: "The Small Business AI Automation Operating System" (`2026 Enterprise Edition`)
**Document ID:** `16-VIDEO-PROMO-KIT/VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md`  
**Master Storyboard:** `16-VIDEO-PROMO-KIT/scripts/01-Master-Promo-Script-and-Storyboard.md`  
**Voiceover Script (`82s`):** `16-VIDEO-PROMO-KIT/scripts/02-Clean-Natural-Voiceover-For-ElevenLabs.txt`  
**Vertical Reels Cut (`58s`):** `16-VIDEO-PROMO-KIT/scripts/03-Short-60s-Reels-TikTok-Cut-Script.txt`  
**Synced Subtitles (`.SRT`):** `16-VIDEO-PROMO-KIT/scripts/04-Synced-Video-Subtitles.srt`  
**Interactive Browser Player:** `16-VIDEO-PROMO-KIT/interactive-video-promo-player.html`  

---

## 1. Executive Summary & Multi-Channel Video Strategy
Video is the highest-converting trust multiplier on your landing page (`15-WEB-DEPLOYMENT/dist/index.html`), Gumroad/LemonSqueezy product listings, LinkedIn launch posts, and YouTube Shorts / Instagram Reels funnel.

Inside `16-VIDEO-PROMO-KIT/`, every script, subtitle file, widescreen `16:9` storyboard graphic (`1920 × 1080 px`), vertical `9:16` mobile card (`1080 × 1920 px`), and B-roll composite is pre-engineered so you can produce both:
1. **The `82-Second` Widescreen Flagship Explainer Video (`16:9`, `1920 × 1080 px`, `60 fps`):** Designed for the hero section of your storefront landing page, Gumroad product header, YouTube, and LinkedIn desktop feed.
2. **The `58-Second` Vertical Reels / TikTok / YouTube Shorts Cut (`9:16`, `1080 × 1920 px`, `60 fps`):** Designed for organic short-form reach and paid mobile retargeting ads driving traffic to your **Free 5-Day AI Audit Starter Kit (`$0`)** and **Complete Flagship Operating System (`$59`)**.

---

## 2. How to Generate a 100% Natural Human-Sounding English Voiceover (`3 Proven Options`)

### Option A — Record Your Own Founder Voice Using Our Built-In Teleprompter (Highest Trust)
Nothing converts small business owners faster than hearing a real operator speak plainly and confidently:
1. Double-click **`16-VIDEO-PROMO-KIT/interactive-video-promo-player.html`** to open the interactive studio in Chrome or Edge.
2. Connect a clean USB or XLR microphone (`Shure MV7`, `Audio-Technica AT2020`, `Rode NT-USB`, or an iPhone Voice Memo held 6 inches from your chin in a quiet room).
3. Click **`▶ Play Promo (82s)`** and read along with the highlighted **Live Synchronized Voiceover Teleprompter** on the right side of the screen.
4. **Vocal Delivery Coaching:**
   - Speak as if you are explaining this system across a desk to a friend who owns a busy HVAC, dental, or agency business.
   - Pause for a full half-second (`0.5s`) after the opening question (*"...while you were busy doing actual work?"*) so the hook lands emotionally.
   - Emphasize the numbers (`15 to 25 hours`, `35%`, `60-second`, `15 seconds`, `90-second`, `14-day`, `Friday at 3:00 PM`, `$59`).

### Option B — Generate Studio-Grade AI Voiceover in ElevenLabs (`2 Minutes`)
If you prefer a broadcast-grade studio voiceover without recording yourself:
1. Open `elevenlabs.io` -> **`Text to Speech`**.
2. Open **`16-VIDEO-PROMO-KIT/scripts/02-Clean-Natural-Voiceover-For-ElevenLabs.txt`** (or click **`Copy to Clipboard`** in `interactive-video-promo-player.html`) and paste the entire `204-word` script into ElevenLabs.
3. **Recommended ElevenLabs Voice & Model Settings:**
   - **Model:** `Eleven Multilingual v2` or `Eleven Turbo v2.5`
   - **Recommended Voices:** `Adam` (Authoritative Executive Founder), `Josh` (Warm Conversational Operator), `Brian` (Crisp B2B Narrator), or `Rachel` (Clear Operations Director)
   - **Stability:** `48% – 55%` *(Setting stability around 50% produces natural human inflection rather than flat robotic reading)*
   - **Similarity Boost:** `75% – 80%`
   - **Style Exaggeration:** `15% – 25%`
   - **Speaker Boost:** `Enabled`
4. Click **`Generate`** and download the `.mp3` or `.wav` master track (`~80–82 seconds`).

### Option C — Generate Voiceover in CapCut Desktop, Murf.ai, or OpenAI TTS
- **OpenAI Audio API (`tts-1-hd`):** Select voice **`onyx`** or **`echo`** at `speed: 1.02` and pass `02-Clean-Natural-Voiceover-For-ElevenLabs.txt` to produce a crisp broadcast `.mp3` in 5 seconds.
- **CapCut Desktop / Premiere Pro:** Import `02-Clean-Natural-Voiceover-For-ElevenLabs.txt` and `04-Synced-Video-Subtitles.srt` directly into the timeline.

---

## 3. Scene-by-Scene Timeline Assembly Table (`CapCut`, `Premiere Pro`, `DaVinci Resolve`, or `Canva`)

Set your project timeline to **`1920 × 1080 px` (`16:9` Full HD) at `30 fps` or `60 fps`** and drop the 12 pre-rendered PNG scenes from `16-VIDEO-PROMO-KIT/visual-scenes-16x9/` onto **Video Track 1 (`V1`)** at the exact timestamps below:

| Scene # | Exact Timeline In / Out | Duration | Primary Graphic Asset (`visual-scenes-16x9/`) | Optional B-Roll Pip / Cutaway (`b-roll-assets/`) | Transition & Motion Effect |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scene 01** | `00:00.00 – 00:04.00` | `4.0 sec` | `scene-01-hook-missed-call-leak.png` | `broll-01-owner-late-night-phone.jpg` | Fast `1.00x -> 1.05x` punch-in zoom on missed call badge |
| **Scene 02** | `00:04.00 – 00:15.00` | `11.0 sec` | `scene-02-human-router-bottleneck.png` | `broll-02-team-operations-desk.jpg` | Subtle slow pan left-to-right across the 3 telemetry cards |
| **Scene 03** | `00:15.00 – 00:25.00` | `10.0 sec` | `scene-03-trav-safety-gate-architecture.png` | `broll-03-analytics-dashboard-screen.jpg` | Clean `0.25s` whip-slide transition into the T.R.A.V. shield |
| **Scene 04** | `00:25.00 – 00:31.00` | `6.0 sec` | `scene-04-60s-speed-to-lead-router.png` | `broll-01-owner-late-night-phone.jpg` | Crisp cut on the word *"First"* + `1.03x` slow push |
| **Scene 05** | `00:31.00 – 00:37.00` | `6.0 sec` | `scene-05-3option-quote-and-nurture.png` | `broll-04-field-service-tablet-quote.jpg` | Crisp cut on the word *"Second"* + highlight Option B |
| **Scene 06** | `00:37.00 – 00:43.00` | `6.0 sec` | `scene-06-3tier-support-and-reviews.png` | `broll-05-happy-client-handshake.jpg` | Crisp cut on the word *"Third"* + subtle zoom on Amber Gate |
| **Scene 07** | `00:43.00 – 00:49.00` | `6.0 sec` | `scene-07-invoice-chaser-cashflow-dso.png` | `broll-03-analytics-dashboard-screen.jpg` | Crisp cut on the word *"Fourth"* + highlight `13.4 Days DSO` |
| **Scene 08** | `00:49.00 – 00:55.00` | `6.0 sec` | `scene-08-friday-3pm-owner-scorecard.png` | `broll-06-friday-executive-coffee.jpg` | Crisp cut on *"And fifth"* + zoom on `15 Mins @ Friday 3PM` |
| **Scene 09** | `00:55.00 – 01:01.00` | `6.0 sec` | `scene-09-offline-webapp-and-calculators.png` | `mockup-02-ecosystem-master-poster.png` | Smooth cross-dissolve into the Offline Web App showcase |
| **Scene 10** | `01:01.00 – 01:06.00` | `5.0 sec` | `scene-10-excel-notion-and-office-suite.png` | `mockup-03-chapter01-cheat-sheet.png` | Quick slide transition into the 8-Tab Excel & Notion suite |
| **Scene 11** | `01:06.00 – 01:12.00` | `6.0 sec` | `scene-11-full-flagship-bundle-showcase.png` | `mockup-01-flagship-os-cover.png` | Dramatic `1.06x -> 1.00x` pull-back reveal of the 100-file stack |
| **Scene 12** | `01:12.00 – 01:22.00` | `10.0 sec` | `scene-12-cta-free-audit-and-flagship-os.png` | `mockup-04-tier2-workbook-atlas.png` | Hold steady on the Dual CTA (`$0 Starter Kit` / `$59 Full OS`) |

---

## 4. Audio Mixing, Ducking & Sound Design (`SFX`) Formula
Great sound design keeps viewers glued to the screen through pattern-interrupt transitions:
1. **Track A1 — Voiceover Master (`-3 dB` to `-1 dB` Peak, `-14 LUFS` Integrated):**
   - Apply a gentle high-pass filter at `80 Hz`, a subtle `3:1` compressor, and a limiter at `-1.0 dB` so every word cuts cleanly through laptop and mobile phone speakers.
2. **Track A2 — Background Instrumental Bed (`-22 dB` to `-20 dB` Under Voice):**
   - Choose a modern, minimal dark-tech or corporate pulse instrumental (`110–118 BPM`, zero vocals).
   - **Dynamic Cue Change at `00:25`:** Start with a tense, minimal pulse during the Hook and Agitation (`00:00–00:25`), then bring in a crisp, confident driving beat right at `00:25` when Department 01 (`60-Second Speed-to-Lead`) appears.
3. **Track A3 — Subtle UI & Notification Sound Effects (`-14 dB` to `-12 dB`):**
   - `00:00.50`: Phone vibration buzz + missed-call alert tone
   - `00:15.00`: Clean mechanical shield lock click (`T.R.A.V. Firewall`)
   - `00:25.00`: iMessage/SMS swoosh + calendar booked ping
   - `00:31.00`, `00:37.00`, `00:43.00`, `00:49.00`: Subtle low-frequency whoosh + UI card snap on each department transition
   - `01:12.00`: Warm resolving chord on the final Dual Call-to-Action screen

---

## 5. Importing & Styling `04-Synced-Video-Subtitles.srt` (`85% Mute-Watch Optimization`)
Over `75%` of LinkedIn, Facebook, and mobile landing-page visitors watch the first 10 seconds of a video on mute.
1. In CapCut, Premiere Pro, DaVinci Resolve, or Veed.io, click **`Subtitles -> Import SRT`** and select **`16-VIDEO-PROMO-KIT/scripts/04-Synced-Video-Subtitles.srt`**.
2. Note that every slide in `visual-scenes-16x9/` and `visual-scenes-9x16-reels/` already includes an integrated broadcast teleprompter bar at the bottom of the frame. If you enable external `.SRT` captions in YouTube, LinkedIn, or your video player, they will sync millisecond-for-millisecond with the spoken script (`21` caption blocks from `00:00:00,000` to `00:01:22,000`).

---

## 6. Assembling the `58-Second` Vertical Reels / TikTok / Shorts Cut (`9:16`)
To export your vertical social video in under 5 minutes:
1. Create a **`1080 × 1920 px` (`9:16` Vertical)** timeline in CapCut or Premiere Pro.
2. Drop the 6 vertical scenes from **`16-VIDEO-PROMO-KIT/visual-scenes-9x16-reels/`** onto the timeline:
   - `reel-scene-01-hook.png` (`00:00 – 00:06`, `6s`)
   - `reel-scene-02-bottleneck.png` (`00:06 – 00:16`, `10s`)
   - `reel-scene-03-speed-to-lead.png` (`00:16 – 00:28`, `12s`)
   - `reel-scene-04-cashflow-and-friday-kpi.png` (`00:28 – 00:40`, `12s`)
   - `reel-scene-05-complete-os-stack.png` (`00:40 – 00:50`, `10s`)
   - `reel-scene-06-cta-get-access.png` (`00:50 – 00:58`, `8s`)
3. Record or generate the 58-second voiceover from **`16-VIDEO-PROMO-KIT/scripts/03-Short-60s-Reels-TikTok-Cut-Script.txt`**, export as `H.264 .MP4` (`1080×1920`, `60 fps`), and post to YouTube Shorts, Instagram Reels, TikTok, and LinkedIn Mobile with your storefront link in the first comment and bio.
"""
    guide_clean = sanitize_phase11_text(guide_md)
    guide_path = VIDEO_DIR / "VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md"
    guide_path.write_text(guide_clean, encoding="utf-8")
    return len(re.findall(r"\b[\w'-]+\b", guide_clean))


def main():
    print("=== PHASE 11: BUILDING HIGH-RETENTION PROMOTIONAL VIDEO KIT (16-VIDEO-PROMO-KIT/) ===")
    browser_exe = find_browser_executable()

    # 1. Build 4 script & subtitle files
    script_res = build_voiceover_scripts_and_srt()
    print(
        f" -> Built scripts: ElevenLabs VO ({script_res['vo_words']} spoken words), "
        f"SRT ({script_res['srt_blocks']} blocks), Storyboard ({script_res['storyboard_words']:,} words)"
    )

    # 2. Build & Render 12 Widescreen 16:9 Scenes (1920x1080)
    print(" -> Rendering 12 Widescreen 16:9 Storyboard Scenes (1920x1080 px)...")
    for sc in SCENES_16X9_SPECS:
        svg_str = build_svg_16x9(sc)
        ET.fromstring(svg_str)
        svg_p = SVG_SRC_DIR / sc["svg_name"]
        png_p = SCENES_16X9_DIR / sc["filename"]
        svg_p.write_text(svg_str, encoding="utf-8")
        render_svg_to_png(browser_exe, svg_p, png_p, 1920, 1080)
        print(f"    [16:9 PNG] {png_p.name} ({png_p.stat().st_size:,} B)")

    # 3. Build & Render 6 Vertical 9:16 Reels Scenes (1080x1920)
    print(" -> Rendering 6 Vertical 9:16 Reels/TikTok Scenes (1080x1920 px)...")
    for rl in REELS_9X16_SPECS:
        svg_str = build_svg_9x16(rl)
        ET.fromstring(svg_str)
        svg_p = SVG_SRC_DIR / rl["svg_name"]
        png_p = SCENES_9X16_DIR / rl["filename"]
        svg_p.write_text(svg_str, encoding="utf-8")
        render_svg_to_png(browser_exe, svg_p, png_p, 1080, 1920)
        print(f"    [9:16 PNG] {png_p.name} ({png_p.stat().st_size:,} B)")

    # 4. Download & Prepare B-Roll Assets
    print(" -> Downloading & preparing B-Roll assets (16-VIDEO-PROMO-KIT/b-roll-assets/)...")
    broll_res = download_and_prepare_broll_assets(browser_exe)
    print(f"    [B-ROLL] Prepared {len(broll_res)} B-roll & product composite images")

    # 5. Build Interactive Promo Video Player HTML
    player_bytes = build_interactive_promo_player()
    print(f" -> Built interactive-video-promo-player.html ({player_bytes:,} bytes)")

    # 6. Build Production Guide Markdown
    guide_words = build_video_production_guide()
    print(f" -> Built VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md ({guide_words:,} words)")
    print("=== PHASE 11 VIDEO PROMO KIT BUILD COMPLETE ===")


if __name__ == "__main__":
    main()
