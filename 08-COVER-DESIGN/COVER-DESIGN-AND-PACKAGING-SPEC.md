# Commercial Cover & Amazon KDP Full-Wrap Print Packaging Specification

**Directory:** `08-COVER-DESIGN/`  
**Print Export Copy:** `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf`  
**Verified KDP Interior Page Count (`Phase 5`):** `242 pages` (`6.0" × 9.0"` US Trade Trim)  
**Calculated White-Paper Spine Width:** `0.545 inches` (`39.24 pt` / `163.5 px @ 300 DPI`)  
**Full-Wrap Bleed Canvas Dimensions:** `12.795" × 9.250"` (`921.24 pt × 666.0 pt`)  
**Visual Theme System:** Executive Emerald & Slate (`#0F172A`, `#059669`, `#0284C7`, `#D97706`, `#1E293B`, `#64748B`, `#FFFFFF`)  

---

## 1. Executive Visual Identity & Typography System

The commercial cover suite for **The Small Business AI Automation Operating System** (`2026 Enterprise Edition`) is engineered to project authoritative systems engineering credibility across Amazon KDP Kindle, Amazon KDP Print-on-Demand Paperback, Gumroad, LemonSqueezy, and enterprise B2B sales pages.

### 1.1 Color Architecture (Executive Emerald & Slate Palette)
Every vector cover asset (`.svg`), rasterized high-resolution preview (`.png`), and print-ready press sheet (`.pdf`) enforces the studio's seven-color specification:
1. **Primary Canvas (`#0F172A` — Deep Executive Navy/Slate):** Provides high-contrast authority that stands out dramatically at thumbnail scale on light-mode retail marketplaces (Amazon, Gumroad, Apple Books).
2. **Operations Emerald (`#059669` & `#34D399` Highlights):** Signifies **Green-Gate Autonomous Execution**, positive cashflow recovery, and verified operational health.
3. **System Cyan (`#0284C7` & `#38BDF8` Highlights):** Signifies deterministic webhook routing, API schema validation, and multi-department data synchronization.
4. **Amber Approval Gate (`#D97706` & `#FBBF24` Highlights):** Signifies **Human-in-the-Loop (HITL) Governance**, margin protection, and 15-second manager approval checkpoints.
5. **Secondary Surface Slate (`#1E293B` & `#334155` Borders):** Structural card containers, telemetry grids, and spine boundaries.
6. **Muted Telemetry Slate (`#64748B` & `#94A3B8`):** Technical sub-labels, trim callouts, and platform compatibility strips.
7. **Pure White (`#FFFFFF`):** Primary title display typography and the mandatory KDP ISBN barcode box (`2.00" × 1.20"`).

### 1.2 Typography Hierarchy
- **Primary Display Title:** `Inter` / `Segoe UI` Black (`font-weight: 900`), uppercase, tight tracking (`-1px`), engineered for instant legibility even when scaled down to a `120 × 192 px` mobile Amazon search result thumbnail.
- **Technical Telemetry & Badges:** `JetBrains Mono` / `Consolas` Bold (`font-weight: 700`), uppercase with wide tracking (`1.5px–3.0px`), reinforcing the deterministic code-and-prompt engineering foundation of the book.
- **Executive Subtitles & Back-Cover Copy:** `Inter` Medium/SemiBold (`font-weight: 500–700`), set with generous line height for rapid scanning by busy business owners.

---

## 2. Dynamic Amazon KDP Paperback Full-Wrap Geometry (`242 Pages`)

Amazon KDP Print-on-Demand requires exact mathematical alignment between the compiled interior PDF page count (`09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf`, verified at **`242 pages`** in Phase 5) and the full-wrap cover press file (`08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf`).

### 2.1 Official KDP White-Paper Spine & Full-Wrap Formulas
Using Amazon KDP's official multiplier for standard white interior paper (`0.002252 inches per page`):

1. **Spine Width (`S`):**
   - `S = 242 pages × 0.002252 in/page = 0.544984 in ≈ 0.545 inches` (`13.84 mm` / `39.24 pt` / `163.5 px @ 300 DPI`).
2. **Total Full-Wrap Width (`W_wrap`):**
   - `W_wrap = Left Bleed (0.125") + Back Cover Trim (6.000") + Spine Width (0.545") + Front Cover Trim (6.000") + Right Bleed (0.125")`
   - `W_wrap = 12.795 inches` (`324.99 mm` / `921.24 pt` / `3,838.5 px @ 300 DPI`).
3. **Total Full-Wrap Height (`H_wrap`):**
   - `H_wrap = Top Bleed (0.125") + Trim Height (9.000") + Bottom Bleed (0.125")`
   - `H_wrap = 9.250 inches` (`234.95 mm` / `666.00 pt` / `2,775.0 px @ 300 DPI`).

### 2.2 Horizontal Coordinate Map Across the `3838 × 2775` Master Canvas (`300 DPI`)
| Zone Name | Width (Inches) | Width (Points) | Pixel X-Range (`300 DPI`) | Engineering & Safe-Zone Rule |
| :--- | :--- | :--- | :--- | :--- |
| **1. Left Exterior Bleed** | `0.125"` | `9.00 pt` | `X: 0.0 -> 37.5 px` | Background gradient & grid extend to `X=0`; zero live text permitted. |
| **2. Back Cover Trim Panel** | `6.000"` | `432.00 pt` | `X: 37.5 -> 1837.5 px` | Safe text zone inset `0.25"` inside trim (`X: 115 -> 1760 px`). |
| **3. Center Spine Panel** | `0.545"` | `39.24 pt` | `X: 1837.5 -> 2001.0 px` | Spine centerline at `X = 1919.25 px`; rotated `90°` title with `0.0625"` (`18.75 px`) spine margin buffer on both sides. |
| **4. Front Cover Trim Panel** | `6.000"` | `432.00 pt` | `X: 2001.0 -> 3801.0 px` | Safe text zone inset `0.25"` inside trim (`X: 2075 -> 3720 px`). |
| **5. Right Exterior Bleed** | `0.125"` | `9.00 pt` | `X: 3801.0 -> 3838.0 px` | Background gradient & grid extend to `X=3838`; zero live text permitted. |

### 2.3 Mandatory ISBN Barcode Safe Zone (`Back Cover Bottom-Right`)
Per Amazon KDP Print specifications, a high-contrast solid white box (`#FFFFFF`) measuring **`2.00" × 1.20"` (`600 × 360 px @ 300 DPI`)** is positioned at `X: 1105 -> 1705 px`, `Y: 2160 -> 2520 px`. This placement sits `0.44"` (`132.5 px`) to the left of the spine fold and `0.85"` (`255 px`) above the bottom bleed edge, exceeding KDP's minimum `0.25"` barcode clearance rule so KDP's automated barcode stamper never overlaps back-cover copy.

---

## 3. Complete Inventory of the 6 Commercial Cover Suites (`SVG + PNG + PDF`)

### 3.1 `ebook-cover-kdp-kindle` (`.svg` & `.png`)
- **Target Platforms:** Amazon Kindle Direct Publishing (KDP eBook), Apple Books, Google Play Books, Kobo, and Draft2Digital.
- **Exact Dimensions:** `1600 × 2560 pixels` (Exact `1 : 1.6` Amazon KDP Ideal Height-to-Width Aspect Ratio).
- **Visual Composition:** Full-height vertical architecture showcasing the 3-word stacked title, the 5-Department Operating System radial node diagram (`Dept 01` Speed-to-Lead, `Dept 02` Sales & Quoting, `Dept 03` Delivery & Support, `Dept 04` Finance & A/R, `Dept 05` Owner Command), the `Green / Amber / Red` T.R.A.V. governance telemetry bar, and the 8-platform tool compatibility strip.

### 3.2 `kdp-paperback-full-wrap-cover` (`.svg`, `.png` & `.pdf`)
- **Target Platforms:** Amazon KDP Print Paperback (`6.0" × 9.0"` White Paper) and IngramSpark POD.
- **Exact Dimensions:**
  - Vector SVG Canvas: `viewBox="0 0 3838 2775"` (`300 DPI` equivalent of `12.795" × 9.25"`).
  - High-Resolution PNG Preview: `2559 × 1850 pixels` (or `3838 × 2775 pixels` proportional full-wrap raster).
  - Press-Ready PDF (`08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf` & `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf`): `12.795" × 9.25"` (`921.24 pt × 666.00 pt`), single page (`1 page`).

### 3.3 `gumroad-tier0-free-audit-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 0 (`$0 Free Lead Magnet`)** — *The 5-Day Small Business Time & Lead-Leak Audit Starter Kit*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape E-Commerce Hero Ratio for Gumroad, LemonSqueezy, and ConvertKit landing pages).
- **Visual Highlights:** Operations Cyan & Emerald theme highlighting the Free Chapter 1 + Worksheet 1 PDF (`32 pages`, `64 AcroForm fields`), the CMF ROI Calculator Web App (Free Diagnostic Mode), and the `sheet1-automation-roi-and-leak-calculator.csv` spreadsheet.

### 3.4 `gumroad-tier2-workbook-atlas-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 2 (`$29 Direct / Commercial Upgrade`)** — *The Complete Book, Fillable Action Workbooks (US Letter + A4), Landscape Tablet Planner & Visual Shortcut Atlas*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape).
- **Visual Highlights:** Highlights the `179-page` Master Digital Book PDF, Reflowable EPUB 3.0, `80-page` US Letter Fillable Workbook (`160 AcroForm fields`), `76-page` ISO A4 Fillable Workbook (`152 AcroForm fields`), `47-page` iPad/GoodNotes Landscape Planner, and Printable Laminated Desk Cards.

### 3.5 `gumroad-tier3-flagship-os-bundle-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 3 (`$59 Flagship Commercial Bundle` — Core Revenue Driver)** — *The Complete Small Business AI Automation Operating System*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape).
- **Visual Highlights:** Emphasizes the activated **Pro Web Companion App (`SMALLBIZ-OS-PRO-2026`)**, all **50 Tested AI Workflow Prompts**, all **12 Emergency Operations Scripts**, the **5-Database Minimalist Notion OS Kit**, the **8-Tab Charted Excel Command Center (`.xlsx`)**, and the **Importable Make.com / Zapier / n8n JSON Automation Blueprints**.

### 3.6 `gumroad-tier4-living-vault-membership-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 4 (`$12/mo or $59/yr Recurring Membership`)** — *The Living Small Business Automation Vault & Quarterly Governance Updates*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape).
- **Visual Highlights:** Executive Amber & Emerald prestige styling highlighting quarterly new Make/n8n/Zapier JSON blueprints, updated model prompt calibrations, Editable Office Suite (`.docx` SOPs + `.pptx` Training Decks), and Canva/Figma Editable Design Kits.

---

## 4. Automated Pre-Flight Quality Assurance Protocol (`verify_phase7.py`)

Every cover asset generated in `08-COVER-DESIGN/` is verified programmatically before release:
1. **XML Structural Integrity:** All 6 `.svg` files are parsed via Python's `xml.etree.ElementTree` to guarantee 100% well-formed XML tags, valid `viewBox` attributes, and presence of the Executive Emerald & Slate brand hex codes (`#0F172A`, `#059669`, `#0284C7`, `#D97706`).
2. **PNG Binary `IHDR` Verification:** All 6 `.png` files are inspected at the binary byte level (`\x89PNG\r\n\x1a\n` signature + `IHDR` big-endian unsigned integer width/height unpacking) to confirm exact pixel dimensions (`1600 × 2560` for Kindle, `1600 × 1200` for Gumroad Tiers 0/2/3/4, and full-wrap dimensions for KDP Paperback) and file sizes exceeding `> 40 KB`.
3. **PDF MediaBox & Page-Count Verification:** Both `08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf` and `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf` are validated with `pypdf.PdfReader` to confirm `1 page` and exact `921.24 pt × 666.00 pt` (`12.795" × 9.25"`) bleed dimensions.

---

## 5. Step-by-Step Amazon KDP, Draft2Digital & Gumroad Upload Guide

### 5.1 Uploading the Kindle eBook Edition (`Amazon KDP & Draft2Digital`)
1. Log into `https://kdp.amazon.com` and select **`Create -> Kindle eBook`**.
2. Enter the official metadata from `02-ARCHITECTURE/book-config.yaml`:
   - **Title:** *The Small Business AI Automation Operating System*
   - **Subtitle:** *A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff*
3. Under **Manuscript**, upload `09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub` (`376 KB`, validated EPUB 3.0).
4. Under **Kindle eBook Cover**, select **`Upload a cover you already have (JPG/TIFF/PNG)`** and upload `08-COVER-DESIGN/ebook-cover-kdp-kindle.png` (`1600 × 2560 px`).

### 5.2 Uploading the `6.0" × 9.0"` Print Paperback Edition (`Amazon KDP Print`)
1. In your KDP Bookshelf, click **`+ Create Paperback`** linked to your eBook title.
2. Under **Print Options**, select:
   - **Interior & Paper Type:** `Black & white interior with white paper` (or `Standard color interior with white paper`).
   - **Trim Size:** `6 × 9 in (15.24 × 22.86 cm)`.
   - **Bleed Settings:** `No Bleed` (for the interior manuscript PDF, which uses mirrored `0.75"` inside gutter margins and `0.625"` outside margins).
   - **Paperback Cover Finish:** `Matte` (recommended for deep `#0F172A` executive slate contrast) or `Glossy`.
3. Under **Manuscript**, upload `09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf` (`242 pages`).
4. Under **Book Cover**, select **`Upload a cover you already have (Print-ready PDF only)`** and upload `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf` (`12.795" × 9.25"`, `0.545"` spine).
5. Launch **KDP Print Previewer**: verify that the spine title sits centered within the `0.545"` spine fold guides and that KDP's automated ISBN barcode places cleanly inside the `2.00" × 1.20"` white box on the bottom-right of the back cover.

### 5.3 Configuring the 4 Gumroad / LemonSqueezy Commercial Product Tiers
When setting up your direct-to-founder digital storefront (`Chapters 1–10` commercial funnel):
- **Tier 0 Listing (`$0+ Free Audit Starter Kit`):** Upload `08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png` (`1600 × 1200 px`) as the product cover image and attach the Tier 0 ZIP bundle (`tier0-free-sample-chapter01-and-audit.pdf`, `smallbiz-automation-os-app.html`, and `sheet1-automation-roi-and-leak-calculator.csv`).
- **Tier 2 Listing (`$29 Action Workbooks, Tablet Planner & Atlas`):** Upload `08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png` (`1600 × 1200 px`) and attach the complete eBook + US Letter/A4/iPad fillable workbooks.
- **Tier 3 Listing (`$59 Flagship Small Business AI Automation OS Bundle`):** Upload `08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png` (`1600 × 1200 px`) and attach the complete Flagship Bundle including `PRO-ACCESS-LICENSE-KEY.txt` (`SMALLBIZ-OS-PRO-2026`), the 5-Database Notion OS Kit, the 8-Tab Excel Command Center, and the Make/Zapier/n8n JSON blueprints.
- **Tier 4 Listing (`$12/mo or $59/yr Living Automation Vault & Office Suite`):** Upload `08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png` (`1600 × 1200 px`) and enable recurring membership access to the Editable Office Suite (`.docx` + `.pptx`), Design Kit, and quarterly blueprint releases.

---

## 6. Customization & Re-Compilation Workflow (`build_phase7.py`)

If you ever add bonus appendices to the manuscript in a future edition that change `kdp_paperback_page_count` inside `PROJECT_STATE.json`:
1. Run `python build.py` first to re-compile the `6.0" × 9.0"` KDP interior PDF and update `kdp_paperback_page_count` in `PROJECT_STATE.json`.
2. Run `python build_phase7.py` to automatically recalculate the new spine width (`pages × 0.002252"`), regenerate `kdp-paperback-full-wrap-cover.svg`, re-render all 6 high-resolution `.png` files, and re-compile `kdp-paperback-full-wrap-cover.pdf`.
3. Run `python verify_phase7.py` to confirm `0 errors` across all XML, PNG `IHDR`, and PDF `MediaBox` checks.
