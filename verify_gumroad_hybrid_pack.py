#!/usr/bin/env python3
"""
Verification Gate for Gumroad Hybrid Master Setup Pack & 600x600 Square Thumbnails
Project: The Small Business AI Automation Operating System by OMAR SUNNY
"""
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

STUDIO = Path(__file__).resolve().parent
COVER_DIR = STUDIO / "08-COVER-DESIGN"
GUMROAD_DIR = STUDIO / "10-MARKETING" / "Gumroad-Hybrid-Master-Setup"
THUMBS_COPY_DIR = GUMROAD_DIR / "Thumbnails-and-Covers"

BANNED_WORDS = ["TBD", "TODO", "placeholder", "coming soon", "lorem ipsum", "[insert"]

def get_png_dimensions(png_path: Path):
    with open(png_path, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a valid PNG: {png_path}")
    w, h = struct.unpack(">II", header[16:24])
    return w, h

def main():
    errors = 0
    print("=" * 72)
    print("VERIFYING GUMROAD HYBRID MASTER SETUP PACK (OMAR SUNNY)")
    print("=" * 72)

    # 1. Check 3 Square SVGs and PNGs in 08-COVER-DESIGN and Thumbnails-and-Covers
    thumb_bases = [
        "11-gumroad-square-thumb-listing1-free-audit-600x600",
        "12-gumroad-square-thumb-listing2-flagship-os-600x600",
        "13-gumroad-square-thumb-listing3-vip-membership-600x600",
    ]
    for base in thumb_bases:
        for folder in [COVER_DIR, THUMBS_COPY_DIR]:
            svg_p = folder / f"{base}.svg"
            png_p = folder / f"{base}.png"
            if not svg_p.exists() or svg_p.stat().st_size < 1500:
                print(f"[FAIL] Missing or small SVG: {svg_p}")
                errors += 1
            else:
                try:
                    tree = ET.parse(svg_p)
                    root = tree.getroot()
                    vb = root.attrib.get("viewBox", "")
                    txt = svg_p.read_text(encoding="utf-8")
                    if vb != "0 0 600 600":
                        print(f"[FAIL] SVG viewBox != '0 0 600 600' in {svg_p}: {vb}")
                        errors += 1
                    elif "OMAR SUNNY" not in txt:
                        print(f"[FAIL] 'OMAR SUNNY' missing in {svg_p}")
                        errors += 1
                    else:
                        print(f"[PASS] SVG valid (viewBox=0 0 600 600, OMAR SUNNY): {svg_p.relative_to(STUDIO)}")
                except Exception as e:
                    print(f"[FAIL] Invalid XML in {svg_p}: {e}")
                    errors += 1

            if not png_p.exists() or png_p.stat().st_size < 10240:
                print(f"[FAIL] Missing or small PNG (<10KB): {png_p}")
                errors += 1
            else:
                try:
                    w, h = get_png_dimensions(png_p)
                    if (w, h) != (600, 600):
                        print(f"[FAIL] PNG dimensions {w}x{h} != 600x600: {png_p}")
                        errors += 1
                    else:
                        print(f"[PASS] PNG valid (600x600 px, {png_p.stat().st_size:,} bytes): {png_p.relative_to(STUDIO)}")
                except Exception as e:
                    print(f"[FAIL] PNG read error {png_p}: {e}")
                    errors += 1

    # 2. Check 6 Master Markdown Playbooks and Word Count Gates
    md_specs = [
        ("00-UNIFIED-2-LINK-MASTER-STRATEGY-AND-LOCKED-SETUP.md", 800),
        ("01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md", 1500),
        ("02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md", 2500),
        ("03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md", 1800),
        ("04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md", 1800),
        ("05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md", 1800),
    ]
    for fname, min_words in md_specs:
        md_p = GUMROAD_DIR / fname
        if not md_p.exists():
            print(f"[FAIL] Missing Markdown guide: {md_p}")
            errors += 1
            continue
        text = md_p.read_text(encoding="utf-8")
        words = len(text.split())
        if words < min_words:
            print(f"[FAIL] Word count {words} < {min_words} in {fname}")
            errors += 1
        else:
            print(f"[PASS] {fname}: {words:,} words (gate >= {min_words:,})")

        low = text.lower()
        for bw in BANNED_WORDS:
            if bw.lower() in low:
                print(f"[FAIL] Banned phrase '{bw}' found in {fname}")
                errors += 1

    print("=" * 72)
    print(f"VERIFICATION COMPLETE: {errors} errors")
    print("=" * 72)
    if errors > 0:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
