# Interactive Cover, SOP Binder & Social Graphic Customizer Studio — User & White-Labeling Guide

**Document ID:** `08-COVER-DESIGN/Editable-Design-Kit/README-DESIGN-KIT.md`  
**Application File:** `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html`  
**Architecture:** 100% Offline Single-File HTML5 + SVG + Canvas Render Studio (Zero External Dependencies)  

---

## 1. Executive Purpose & Use Cases
The **Interactive Cover, SOP Binder & Social Graphic Customizer Studio** (`design-customizer-studio.html`) enable small business owners, operations managers, agency directors, and publishing studios to customize, white-label, and export high-resolution graphics directly inside any modern desktop browser (`Microsoft Edge`, `Google Chrome`, `Apple Safari`, or `Mozilla Firefox`) with zero cloud logins or subscription software required.

Whether you are printing a physical 3-ring **Company AI & SOP Operations Binder** for your front-desk and field technicians, customizing your **Kindle / Digital Book Cover**, updating your **Gumroad Product Thumbnails**, or publishing **LinkedIn / Facebook Executive Launch Announcements**, this studio renders crisp vector `.SVG` and exact-pixel `.PNG` assets in one click.

---

## 2. The 5 Built-In Canvas Templates & Exact Pixel Dimensions

| Template Option # | Template Name in Studio Dropdown | Exact Pixel Resolution | Aspect Ratio | Primary Operational & Commercial Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Template 01** | **Kindle / Digital Book Cover** | `1600 × 2560 px` | `1 : 1.6` | Amazon KDP Kindle eBook cover, Draft2Digital wide retail cover, and Apple Books / Kobo storefront edition. |
| **Template 02** | **Internal Team SOP Binder Cover** | `1600 × 2200 px` | `8.5 : 11` | Printable US Letter / A4 front cover insert for your physical office SOP binder and new-hire onboarding manual. |
| **Template 03** | **Gumroad / Course Bundle Banner** | `1600 × 1200 px` | `4 : 3` | High-converting product card for Gumroad, LemonSqueezy, Stan Store, Kajabi, or internal Notion dashboard headers. |
| **Template 04** | **LinkedIn / Executive Social Launch Card** | `1200 × 630 px` | `1.91 : 1` | OpenGraph (`og:image`) social share banner for LinkedIn articles, Facebook/X posts, and email newsletter headers. |
| **Template 05** | **5-Dept Workflow Architecture Square Card** | `1080 × 1080 px` | `1 : 1` | Instagram, LinkedIn carousel slide, or internal Slack/Teams announcement card showcasing the 5-Department Engine. |

---

## 3. Step-by-Step Customization & White-Labeling Workflow

### Step 1 — Launch the Studio Offline
1. Open the folder `08-COVER-DESIGN/Editable-Design-Kit/` on your Windows PC, Mac, or Linux workstation.
2. Double-click **`design-customizer-studio.html`**. The studio loads immediately in your default web browser with zero internet connection required.

### Step 2 — Choose Your Canvas Format & Executive Theme Palette
1. In **Section 0 (`Quick-Load Chapter, Industry & Campaign Preset`)**, optionally pick one of the 18 pre-written chapter, industry (`HVAC`, `Dental/MedSpa`, `B2B Agency`, `CPA/Legal`, `E-Commerce`), or social campaign presets to populate all fields automatically.
2. In **Section 1 (`Select Canvas Format & Dimension Preset`)**, select one of the five target resolutions (`1600×2560`, `1600×2200`, `1600×1200`, `1200×630`, or `1080×1080`).
3. In **Section 2 (`Executive Theme Color Presets`)**, click any of the five built-in corporate palettes or use the four native color pickers (`Canvas BG`, `Primary Accent`, `System Cyan`, and `Badge / Gate`) to match your exact brand hex codes:
   - **Executive Emerald & Slate (Default):** `#0F172A` Navy, `#059669` Emerald, `#0284C7` System Cyan, `#D97706` Amber Gate.
   - **Enterprise Cobalt & Cyan:** `#0B132B` Deep Navy, `#2563EB` Royal Blue, `#06B6D4` Cyan, `#F59E0B` Gold.
   - **Industrial Gold & Carbon:** `#18181B` Carbon Slate, `#D97706` Industrial Amber, `#0284C7` Steel Blue, `#10B981` Emerald.
   - **Clinical Teal & Navy:** `#0F2942` Medical Navy, `#0D9488` Clinical Teal, `#38BDF8` Sky Blue, `#F59E0B` Amber.
   - **Executive Burgundy & Slate:** `#1F122B` Deep Plum/Slate, `#E11D48` Crimson Accent, `#0284C7` Cyan, `#D97706` Gold.

### Step 3 — Edit Typography, Headlines & Metric Callout Pills
1. In **Section 3 (`Live Typography & White-Label Copy`)**, type your custom text into any of the nine live input boxes:
   - **Top Eyebrow Badge:** e.g., `APEX COMFORT HVAC • INTERNAL SOP MANUAL (2026 EDITION)`
   - **Headline Lines 1, 2, and 3:** Customize the 3-line display title and use the **Headline Font Scale (`75%–125%`)** slider to balance long company names cleanly.
   - **Subtitle / Scope Statement:** Automatically word-wraps across up to three centered lines so text never clips outside the border frame.
   - **Metric Pills 1, 2, and 3:** Highlight your company's core SLAs (e.g., `60-SECOND RESPONSE`, `3-OPTION QUOTES`, `4.9★ GOOGLE RATING`).
   - **Footer Attribution:** Enter your company name, department, or author imprint.

### Step 4 — Upload Your Company Logo or Founder Headshot (100% Local Privacy)
1. In **Section 4 (`Local Company Logo / Founder Photo Upload`)**, click **`Choose File`** under `Upload PNG/JPG/SVG Logo or Headshot`.
2. Select any `.png`, `.jpg`, `.webp`, or `.svg` file from your computer. Using the browser's native `FileReader` API, your image is converted into an embedded `data:image/...;base64` URI inside local memory—**your logo or photo is never uploaded to any external server**.
3. Adjust the **Uploaded Image Width (`60 px – 420 px`)** and **Vertical Offset (`8% – 92%`)** sliders to position your badge cleanly on the canvas.

### Step 5 — Export Exact-Pixel `.PNG` or Vector `.SVG`
1. Click **`Download High-Res .PNG`** in the top-right header (or stage toolbar) to render the live SVG onto an offscreen HTML5 `<canvas>` at full native resolution (`1600×2560`, `1600×2200`, `1600×1200`, `1200×630`, or `1080×1080`) and download a crisp, print- and storefront-ready `.png` file.
2. Click **`Download Vector .SVG`** to save the pure XML vector source file—ready to open in Adobe Illustrator, Affinity Designer, Inkscape, Figma, or any web browser.

---

## 4. Technical Verification & Troubleshooting Notes
- **Why does the PNG export look razor-sharp?** Unlike screen-capture tools that export at your laptop monitor's scaled viewport size, `exportHighResPng()` binds an offscreen `<canvas>` element to the exact pixel dimensions of the selected preset (`spec.w × spec.h`) prior to rasterizing the vector DOM.
- **Can I archive my custom company covers inside our Notion OS?** Yes. After clicking `Download High-Res .PNG`, upload the exported banner directly into your Notion workspace cover header (`Database 01` through `Database 05`) to brand your team's daily command center.

---

## 5. Industry White-Labeling Playbook (5 Verticals + 80 Quick-Load Presets)
Section 0 of the sidebar includes **80 built-in Quick-Load Presets** covering all 10 chapters, 5 core small-business verticals, 3 storefront/social announcement formats, all 50 Prompt Contracts (`Prompt 1.1` through `Prompt 10.5`), and all 12 Emergency Scripts (`Script #01` through `Script #12`). Below is the recommended white-labeling configuration for each vertical:

| Vertical / Industry | Recommended Theme Preset | Primary Binder Cover Title | Recommended Metric Pills (`Pill 1 / Pill 2 / Pill 3`) |
| :--- | :--- | :--- | :--- |
| **1. Home Services (HVAC, Plumbing, Electrical, Roofing)** | `Executive Emerald & Slate` (`#0F172A` / `#059669`) | `HOME SERVICES AI DISPATCH, QUOTING & OPERATIONS OS` | `15S MISSED-CALL SMS` • `3-OPTION FIELD QUOTES` • `4.9★ GOOGLE RATING` |
| **2. Dental, MedSpa, Chiropractic & Outpatient Clinics** | `Clinical Teal & Navy` (`#0F2942` / `#0D9488`) | `PATIENT INTAKE, RECALL & CLINICAL FRONT-DESK AI OS` | `ZERO-PHI FIREWALL` • `60S PATIENT TRIAGE` • `6-MONTH RECALL ENGINE` |
| **3. B2B Marketing, Web, Creative & Consulting Agencies** | `Enterprise Cobalt & Cyan` (`#0B132B` / `#2563EB`) | `AGENCY PROPOSAL, 60S ONBOARDING & SCOPE-GUARD OS` | `3-TIER RETAINERS` • `60S CLIENT KICKOFF` • `SCOPE-CREEP SHIELD` |
| **4. CPA, Bookkeeping, Legal & Advisory Practices** | `Executive Burgundy & Slate` (`#1F122B` / `#E11D48`) | `ADVISORY INTAKE, DOCUMENT CHASER & BILLING AUTOMATION` | `CONFLICT-CHECK GATE` • `AUTO DOC CHASERS` • `DSO ≤ 12 DAYS` |
| **5. Specialty E-Commerce, Wholesale & Local Retail** | `Industrial Gold & Carbon` (`#18181B` / `#D97706`) | `OMNICHANNEL ORDER SUPPORT, VIP LTV & REORDER ENGINE` | `72% WISMO DEFLECTION` • `VIP REVIEW FUNNEL` • `60-DAY REPLENISHMENT` |

---

## 6. Physical 3-Ring Office SOP Binder Printing & Tab Assembly Guide
Even in a digital-first business, keeping a physical **3-Ring Executive AI & Emergency Operations Binder** at your reception desk, dispatch station, or manager workstation ensures your team can execute every protocol during an internet or API outage:
1. **Print the Front & Spine Slip Cover:** Select `Internal Team SOP Binder Cover (1600 × 2200 px)` in Section 1, load your company logo in Section 4, export the `.PNG`, and print at `100% Fit to Page` on `8.5" × 11"` (`110 lb` matte cardstock) for your clear-view 3-ring binder front sleeve.
2. **Print the 12-Page Visual Shortcut Atlas (`13-VISUAL-CHEAT-SHEETS/`):** Print `the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf` in full color on `8.5" × 11"` horizontal paper and place it in the front quick-reference pocket of the binder.
3. **Print the 12 Emergency Script Divider Tabs:** In Section 0 of the Customizer Studio, select any of the `Emergency Script #01` through `Emergency Script #12` presets (`Burgundy & Slate` theme) to print red-bordered section dividers placed immediately ahead of your printed Emergency Operations Scripts (`02-Editable-10-Chapter-Action-Workbook.docx` and `04-Customer-Escalation-and-Refund-SOP-Matrix.docx`).
