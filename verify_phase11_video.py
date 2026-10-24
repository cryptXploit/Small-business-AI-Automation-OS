#!/usr/bin/env python3
"""
Phase 11 Promotional Video Kit QA Verification Script (`verify_phase11_video.py`)
Project: "The Small Business AI Automation Operating System" (Flagship Product #2)

Verifies:
1. Voiceover word count in `02-Clean-Natural-Voiceover-For-ElevenLabs.txt` is strictly 185-215 spoken words.
2. Natural conversational contractions present and zero banned words/phrases across all scripts and guides.
3. Valid `.srt` timecode syntax (`HH:MM:SS,mmm --> HH:MM:SS,mmm`) in `04-Synced-Video-Subtitles.srt`.
4. All 12 widescreen `16:9` PNGs in `visual-scenes-16x9/` are exact `1920x1080` valid PNGs.
5. All 6 vertical `9:16` PNGs in `visual-scenes-9x16-reels/` are exact `1080x1920` valid PNGs.
6. All 18 SVG sources in `svg-sources/` parse as valid XML.
7. All B-roll assets in `b-roll-assets/` exist and are >= 15 KB.
8. `interactive-video-promo-player.html` and `VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md` exist and pass QA.
9. Writes `11-QA-REPORTS/phase11-qa-report.json` & `.md` and updates `PROJECT_STATE.json`.
"""

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "16-VIDEO-PROMO-KIT"
SCRIPTS_DIR = VIDEO_DIR / "scripts"
SCENES_16X9_DIR = VIDEO_DIR / "visual-scenes-16x9"
SCENES_9X16_DIR = VIDEO_DIR / "visual-scenes-9x16-reels"
BROLL_DIR = VIDEO_DIR / "b-roll-assets"
SVG_SRC_DIR = VIDEO_DIR / "svg-sources"
QA_DIR = ROOT / "11-QA-REPORTS"

BANNED_WORDS = [
    "delve", "tapestry", "testament", "beacon", "symphony", "unlock", "unleash",
    "skyrocket", "supercharge", "game-changer", "pivotal", "realm", "foster",
    "underscore", "utilize", "leverage",
]
BANNED_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further",
]
PLACEHOLDERS = [r"\bTODO\b", r"\bTBD\b", r"Lorem ipsum", r"\[XX\]"]


def audit_lexical(text: str) -> list:
    hits = []
    for bw in BANNED_WORDS:
        if re.search(rf"\b{re.escape(bw)}\b", text, flags=re.IGNORECASE):
            hits.append(f"banned_word:{bw}")
    for bp in BANNED_PHRASES:
        if bp.lower() in text.lower():
            hits.append(f"banned_phrase:{bp}")
    for pat in PLACEHOLDERS:
        if re.search(pat, text, flags=re.IGNORECASE):
            hits.append(f"placeholder:{pat}")
    return hits


def read_png_dimensions(png_path: Path):
    raw = png_path.read_bytes()
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", raw[16:24])
    return w, h, len(raw)


def main():
    errors = []
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": "Phase 11 — High-Retention Promotional Video Script, Subtitles & Visual B-Roll Kit",
        "scripts": {},
        "scenes_16x9": {},
        "scenes_9x16": {},
        "broll_assets": {},
        "player_and_guide": {},
    }

    # 1. Verify 4 Scripts & Subtitles
    vo_p = SCRIPTS_DIR / "02-Clean-Natural-Voiceover-For-ElevenLabs.txt"
    if not vo_p.exists():
        errors.append("Missing 02-Clean-Natural-Voiceover-For-ElevenLabs.txt")
    else:
        vo_txt = vo_p.read_text(encoding="utf-8")
        vo_words = len(re.findall(r"\b[\w'-]+\b", vo_txt))
        if not (185 <= vo_words <= 215):
            errors.append(f"Voiceover word count {vo_words} outside required 185–215 range")
        if not any(c in vo_txt.lower() for c in ["you're", "doesn't", "that's", "isn't"]):
            errors.append("Voiceover missing natural conversational contractions")
        lex = audit_lexical(vo_txt)
        if lex:
            errors.append(f"Lexical violations in 02-Clean-Natural-Voiceover-For-ElevenLabs.txt: {lex}")
        report["scripts"]["02-Clean-Natural-Voiceover-For-ElevenLabs.txt"] = {
            "spoken_words": vo_words,
            "bytes": vo_p.stat().st_size,
            "lexical_violations": len(lex),
        }

    for sname in ["01-Master-Promo-Script-and-Storyboard.md", "03-Short-60s-Reels-TikTok-Cut-Script.txt"]:
        sp = SCRIPTS_DIR / sname
        if not sp.exists():
            errors.append(f"Missing {sname}")
        else:
            stxt = sp.read_text(encoding="utf-8")
            swords = len(re.findall(r"\b[\w']+\b", stxt))
            lex = audit_lexical(stxt)
            if lex:
                errors.append(f"Lexical violations in {sname}: {lex}")
            report["scripts"][sname] = {"words": swords, "bytes": sp.stat().st_size}

    srt_p = SCRIPTS_DIR / "04-Synced-Video-Subtitles.srt"
    if not srt_p.exists():
        errors.append("Missing 04-Synced-Video-Subtitles.srt")
    else:
        srt_txt = srt_p.read_text(encoding="utf-8")
        tc_matches = re.findall(r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}", srt_txt)
        if len(tc_matches) < 15:
            errors.append(f"SRT has only {len(tc_matches)} timecode blocks (< 15 required)")
        lex = audit_lexical(srt_txt)
        if lex:
            errors.append(f"Lexical violations in 04-Synced-Video-Subtitles.srt: {lex}")
        report["scripts"]["04-Synced-Video-Subtitles.srt"] = {
            "caption_blocks": len(tc_matches),
            "bytes": srt_p.stat().st_size,
        }

    # 2. Verify 12 Widescreen 16:9 PNGs (1920x1080)
    expected_16x9 = [
        "scene-01-hook-missed-call-leak.png",
        "scene-02-human-router-bottleneck.png",
        "scene-03-trav-safety-gate-architecture.png",
        "scene-04-60s-speed-to-lead-router.png",
        "scene-05-3option-quote-and-nurture.png",
        "scene-06-3tier-support-and-reviews.png",
        "scene-07-invoice-chaser-cashflow-dso.png",
        "scene-08-friday-3pm-owner-scorecard.png",
        "scene-09-offline-webapp-and-calculators.png",
        "scene-10-excel-notion-and-office-suite.png",
        "scene-11-full-flagship-bundle-showcase.png",
        "scene-12-cta-free-audit-and-flagship-os.png",
    ]
    for fname in expected_16x9:
        p = SCENES_16X9_DIR / fname
        if not p.exists():
            errors.append(f"Missing 16:9 scene: {fname}")
            continue
        dims = read_png_dimensions(p)
        if not dims or dims[0] != 1920 or dims[1] != 1080:
            errors.append(f"Invalid dimensions for {fname}: {dims}")
        else:
            report["scenes_16x9"][fname] = {"width": dims[0], "height": dims[1], "bytes": dims[2]}

    # 3. Verify 6 Vertical 9:16 PNGs (1080x1920)
    expected_9x16 = [
        "reel-scene-01-hook.png",
        "reel-scene-02-bottleneck.png",
        "reel-scene-03-speed-to-lead.png",
        "reel-scene-04-cashflow-and-friday-kpi.png",
        "reel-scene-05-complete-os-stack.png",
        "reel-scene-06-cta-get-access.png",
    ]
    for fname in expected_9x16:
        p = SCENES_9X16_DIR / fname
        if not p.exists():
            errors.append(f"Missing 9:16 reel scene: {fname}")
            continue
        dims = read_png_dimensions(p)
        if not dims or dims[0] != 1080 or dims[1] != 1920:
            errors.append(f"Invalid dimensions for {fname}: {dims}")
        else:
            report["scenes_9x16"][fname] = {"width": dims[0], "height": dims[1], "bytes": dims[2]}

    # 4. Verify 18 SVG sources
    svg_files = sorted(SVG_SRC_DIR.glob("*.svg"))
    if len(svg_files) < 18:
        errors.append(f"Expected 18 SVG files in svg-sources/, found {len(svg_files)}")
    for sp in svg_files:
        try:
            ET.fromstring(sp.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"Invalid XML in {sp.name}: {e}")

    # 5. Verify B-Roll assets
    broll_files = sorted(BROLL_DIR.glob("*.*"))
    if len(broll_files) < 8:
        errors.append(f"Expected >= 8 B-roll files in b-roll-assets/, found {len(broll_files)}")
    for bp in broll_files:
        sz = bp.stat().st_size
        if sz < 15_000:
            errors.append(f"B-roll file too small: {bp.name} ({sz} B)")
        report["broll_assets"][bp.name] = sz

    # 6. Verify Interactive Promo Player & Production Guide
    player_p = VIDEO_DIR / "interactive-video-promo-player.html"
    if not player_p.exists() or player_p.stat().st_size < 15_000:
        errors.append("Missing or undersized interactive-video-promo-player.html")
    else:
        ptxt = player_p.read_text(encoding="utf-8")
        lex = audit_lexical(ptxt)
        if lex:
            errors.append(f"Lexical violations in interactive-video-promo-player.html: {lex}")
        report["player_and_guide"]["interactive-video-promo-player.html_bytes"] = player_p.stat().st_size

    guide_p = VIDEO_DIR / "VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md"
    if not guide_p.exists():
        errors.append("Missing VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md")
    else:
        gtxt = guide_p.read_text(encoding="utf-8")
        gwords = len(re.findall(r"\b[\w']+\b", gtxt))
        if gwords < 1_000:
            errors.append(f"VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md has {gwords} words (< 1,000 required)")
        lex = audit_lexical(gtxt)
        if lex:
            errors.append(f"Lexical violations in VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md: {lex}")
        report["player_and_guide"]["VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md_words"] = gwords

    report["total_errors"] = len(errors)
    report["errors"] = errors
    report["status"] = "PASS" if len(errors) == 0 else "FAIL"

    (QA_DIR / "phase11-qa-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Phase 11 Promotional Video Script, Subtitles & Visual B-Roll Kit QA Report",
        "",
        f"- **Timestamp:** `{report['timestamp']}`",
        f"- **Status:** `{report['status']}`",
        f"- **Total QA Errors:** `{report['total_errors']}`",
        "",
        "## 1. Voiceover Scripts & Synced `.SRT` Subtitles (`16-VIDEO-PROMO-KIT/scripts/`)",
        f"- **`02-Clean-Natural-Voiceover-For-ElevenLabs.txt`:** `{report['scripts'].get('02-Clean-Natural-Voiceover-For-ElevenLabs.txt', {}).get('spoken_words', 0)} spoken words` (Target: `185–215 words` at `~145 WPM` = `82 seconds`)",
        f"- **`04-Synced-Video-Subtitles.srt`:** `{report['scripts'].get('04-Synced-Video-Subtitles.srt', {}).get('caption_blocks', 0)} synced timecode blocks` (`00:00:00,000` -> `00:01:22,000`)",
        f"- **`01-Master-Promo-Script-and-Storyboard.md`:** `{report['scripts'].get('01-Master-Promo-Script-and-Storyboard.md', {}).get('words', 0):,} words`",
        f"- **`03-Short-60s-Reels-TikTok-Cut-Script.txt`:** `{report['scripts'].get('03-Short-60s-Reels-TikTok-Cut-Script.txt', {}).get('words', 0)} words`",
        "",
        "## 2. Rendered Storyboard Scenes & B-Roll Assets",
        f"- **Widescreen `16:9` Scenes (`1920 × 1080 px`):** `{len(report['scenes_16x9'])}/12` verified",
        f"- **Vertical `9:16` Reels/TikTok Scenes (`1080 × 1920 px`):** `{len(report['scenes_9x16'])}/6` verified",
        f"- **Vector SVG Source Files (`svg-sources/`):** `{len(svg_files)}/18` verified XML",
        f"- **B-Roll & Product Composite Assets (`b-roll-assets/`):** `{len(report['broll_assets'])}/10` verified",
        f"- **Interactive Video Promo Player (`interactive-video-promo-player.html`):** `{report['player_and_guide'].get('interactive-video-promo-player.html_bytes', 0):,} bytes`",
        f"- **Video Production Guide (`VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md`):** `{report['player_and_guide'].get('VIDEO-EDITING-AND-VOICEOVER-PRODUCTION-GUIDE.md_words', 0):,} words`",
    ]
    (QA_DIR / "phase11-qa-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    state_path = ROOT / "PROJECT_STATE.json"
    if state_path.exists() and len(errors) == 0:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["current_phase"] = "PHASE_11_COMPLETE_VIDEO_PROMO_KIT_LOCKED"
        state["last_updated"] = report["timestamp"]
        state["phase_11_video_promo_kit"] = {
            "directory": "16-VIDEO-PROMO-KIT",
            "voiceover_spoken_words": report["scripts"]["02-Clean-Natural-Voiceover-For-ElevenLabs.txt"]["spoken_words"],
            "srt_caption_blocks": report["scripts"]["04-Synced-Video-Subtitles.srt"]["caption_blocks"],
            "widescreen_16x9_scenes": len(report["scenes_16x9"]),
            "vertical_9x16_scenes": len(report["scenes_9x16"]),
            "broll_assets": len(report["broll_assets"]),
            "qa_errors": 0,
        }
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print("=" * 72)
    print(f"PHASE 11 VIDEO PROMO KIT QA STATUS: {report['status']} (Total Errors: {report['total_errors']})")
    print("=" * 72)
    if errors:
        for e in errors:
            print(f" [ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
