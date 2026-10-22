# Static Web Deployment, Live Demo Hub & Global Launch Runbook
## Project: "The Small Business AI Automation Operating System" (`2026 Enterprise Edition`)
**Document ID:** `15-WEB-DEPLOYMENT/STATIC-WEB-DEPLOYMENT-AND-LAUNCH-GUIDE.md`  
**Deployment Root:** `15-WEB-DEPLOYMENT/dist/`  
**Drag-and-Drop Archive:** `15-WEB-DEPLOYMENT/SmallBiz-AI-OS-Cloudflare-Netlify-Dist.zip`  
**Target Hosting Platforms:** Cloudflare Pages (`$0/mo`), GitHub Pages (`$0/mo`), Netlify (`$0/mo`), Vercel (`$0/mo`)  

---

## 1. Executive Architecture Overview (`Zero Monthly Hosting Overhead`)
`15-WEB-DEPLOYMENT/dist/` is a **100% self-contained, zero-dependency static production web bundle**. Every HTML application, stylesheet, SVG diagram, commercial cover graphic, and Tier 0 lead-magnet file is pre-compiled and linked with clean relative paths so you can deploy your high-converting storefront, live SaaS-Lite web companion app, and interactive design customizer studio to global edge CDNs in **under 3 minutes at `$0.00/month` hosting cost**.

### 1.1 Complete Route Map Inside `15-WEB-DEPLOYMENT/dist/`
| Production URL Route | Physical File in `dist/` | Primary Commercial & Operational Function |
| :--- | :--- | :--- |
| **`/` (`index.html`)** | `dist/index.html` | Flagship conversion sales page with Interactive Monthly Leak Calculator, 5-Department Tabs, 12-Accordion Curriculum, Live Demo Hub, Pricing Comparison Matrix, and Lead Magnet Capture. |
| **`/app/` (`app/index.html`)** | `dist/app/index.html` | Live Interactive SaaS-Lite Web Companion Application (Free Preview Mode enabled by default; Pro Tier 3/Tier 4 features gated by license key `SBAO-PRO-2026-EXEC-OS99`). |
| **`/studio/` (`studio/index.html`)** | `dist/studio/index.html` | Live Interactive Cover, SOP Binder & Social Graphic Customizer Studio with 5 canvas presets, 5 corporate color palettes, 80 quick-load templates, local `FileReader` logo upload, and high-res `.PNG` / `.SVG` export. |
| **`/404.html`** | `dist/404.html` | Branded Executive Emerald & Slate custom 404 recovery gate routing visitors back to `/`, `/app/`, `/studio/`, or the free `.zip` download. |
| **`/downloads/Tier0-Free-5Day-Audit-Starter-Kit.zip`** | `dist/downloads/Tier0-Free-5Day-Audit-Starter-Kit.zip` | Instant 1-click download of the complete Tier 0 Free Lead Magnet bundle (`3.13 MB`). |
| **`/downloads/tier0-free-sample-chapter01-and-audit.pdf`** | `dist/downloads/tier0-free-sample-chapter01-and-audit.pdf` | Direct browser preview/download of the 23-page Chapter 1 + 5-Day AI Audit Sample PDF. |
| **`/downloads/chapter-01-workbook.pdf`** | `dist/downloads/chapter-01-workbook.pdf` | Direct browser preview/download of the 15-page Fillable AcroForm Chapter 1 Action Workbook PDF. |
| **`/downloads/sheet1-automation-roi-and-leak-calculator.csv`** | `dist/downloads/sheet1-automation-roi-and-leak-calculator.csv` | Direct download of the Sheet 1 Executive ROI & Monthly Profit-Leak Calculator CSV. |
| **`/downloads/00-ECOSYSTEM-MASTER-MAP-POSTER.png`** | `dist/downloads/00-ECOSYSTEM-MASTER-MAP-POSTER.png` | High-resolution `1600 × 1000 px` Master 5-Department Ecosystem Wall Poster PNG. |
| **`/downloads/cheat-sheet-ch01.png`** | `dist/downloads/cheat-sheet-ch01.png` | High-resolution `1600 × 1000 px` Chapter 01 Executive Cheat Sheet Poster PNG. |

---

## 2. Option A: 60-Second Deployment to Cloudflare Pages (Recommended — Unlimited Bandwidth, `$0/mo`)
Cloudflare Pages is the #1 recommended production host for digital publishing studios because its free tier includes **unlimited static bandwidth**, **300+ global edge locations** (including Dhaka, Singapore, London, New York, and Frankfurt), automatic **SSL/TLS (`HTTPS`)**, and native support for `_headers` and `_redirects`.

### Method A1 — 10-Second Drag-and-Drop Upload (No CLI Required)
1. Log into your free Cloudflare account at `dash.cloudflare.com` and select **`Compute (Workers & Pages) -> Pages`**.
2. Click **`Create application -> Pages -> Upload assets`**.
3. Enter your project name (for example: `smallbiz-ai-automation-os`) and click **`Create project`**.
4. Drag and drop either the **`15-WEB-DEPLOYMENT/dist/`** folder OR the pre-packaged archive **`15-WEB-DEPLOYMENT/SmallBiz-AI-OS-Cloudflare-Netlify-Dist.zip`** directly into the upload box.
5. Click **`Deploy site`**. Within 15 seconds your live storefront is online at `https://smallbiz-ai-automation-os.pages.dev` with `/app/`, `/studio/`, and `/downloads/` all active.

### Method A2 — Automated Git Deployment via Wrangler CLI or GitHub Integration
If you push this repository to a private GitHub or GitLab repository:
1. In Cloudflare Pages, click **`Connect to Git`** and select your repository.
2. Configure the build settings:
   - **Framework preset:** `None`
   - **Build command:** *(Leave blank — files are pre-compiled)*
   - **Build output directory:** `15-WEB-DEPLOYMENT/dist`
3. Or deploy directly from your Windows PowerShell terminal using the Cloudflare Wrangler CLI:
   ```powershell
   npx wrangler pages deploy "15-WEB-DEPLOYMENT/dist" --project-name="smallbiz-ai-automation-os"
   ```

---

## 3. Option B: Zero-Cost Deployment to GitHub Pages (`deploy-github-pages.yml`)
We have included a complete GitHub Actions workflow at `15-WEB-DEPLOYMENT/deploy-github-pages.yml`.

### Step-by-Step GitHub Pages Activation
1. Copy `15-WEB-DEPLOYMENT/deploy-github-pages.yml` into `.github/workflows/deploy-github-pages.yml` in your repository root:
   ```powershell
   New-Item -ItemType Directory -Force -Path ".github/workflows"
   Copy-Item "15-WEB-DEPLOYMENT/deploy-github-pages.yml" ".github/workflows/deploy-github-pages.yml"
   ```
2. Push your repository to GitHub (`git push origin master --tags`).
3. In your GitHub repository dashboard, navigate to **`Settings -> Pages`**.
4. Under **Build and deployment -> Source**, select **`GitHub Actions`**.
5. Every push to `master` (or manual click on `Run workflow` in the Actions tab) automatically uploads `15-WEB-DEPLOYMENT/dist/` and publishes your live site.

---

## 4. Option C: 1-Click Deployment to Netlify (`netlify.toml`)
`15-WEB-DEPLOYMENT/netlify.toml` pre-configures the publish directory (`dist`), security headers, immutable asset caching, and clean route redirects (`/companion`, `/customizer`, `/free-audit`).

### Method C1 — Netlify Drop (Drag-and-Drop)
1. Open `app.netlify.com/drop` in your browser.
2. Drag the **`15-WEB-DEPLOYMENT/dist/`** folder onto the page. Your site is live immediately.

### Method C2 — Netlify CLI or Git Connection
1. Connect your Git repository in Netlify and set **Base directory** to `15-WEB-DEPLOYMENT` (Netlify will automatically read `netlify.toml` and publish `dist/`).
2. Or deploy from PowerShell:
   ```powershell
   npx netlify-cli deploy --dir="15-WEB-DEPLOYMENT/dist" --prod
   ```

---

## 5. Option D: Deployment to Vercel (`vercel.json`)
`15-WEB-DEPLOYMENT/vercel.json` configures `outputDirectory: "dist"`, `cleanUrls: true`, security headers, and route redirects.

### Deploying to Vercel in 30 Seconds
1. Open PowerShell inside `15-WEB-DEPLOYMENT/` (or pass the path argument) and run:
   ```powershell
   npx vercel --cwd "15-WEB-DEPLOYMENT" --prod
   ```
2. Or import your Git repository at `vercel.com/new`, set **Root Directory** to `15-WEB-DEPLOYMENT`, and click **Deploy**.

---

## 6. Wiring Live Gumroad / LemonSqueezy Checkout Links Into `dist/index.html`
Once you upload your 5 commercial `.zip` bundles from `09-EXPORTS/HYBRID-BUNDLE/` into your Gumroad (`gumroad.com`) or LemonSqueezy (`lemonsqueezy.com`) dashboard (following the step-by-step Bangladesh W-8BEN & Payoneer payout setup in `10-MARKETING/marketplace-listings-and-bd-launch-runbook.md`):

### 6.1 Your 5 Commercial Product Bundles & Pricing Tiers
| Tier | Archive File to Upload in Gumroad / LemonSqueezy (`09-EXPORTS/HYBRID-BUNDLE/`) | Retail Price | Recommended Gumroad Custom Permalink |
| :--- | :--- | :--- | :--- |
| **Tier 0** | `Tier0-Free-5Day-Audit-Starter-Kit.zip` (`3.13 MB`, 11 files) | **`$0+`** (Pay-What-You-Want Lead Magnet) | `https://yourstore.gumroad.com/l/smallbiz-ai-audit` |
| **Tier 1** | `Tier1-KDP-and-D2D-Retail-Book-Pack.zip` (`8.35 MB`, 8 files) | **`$9.99`** (Digital Book & Executive Read Edition) | `https://yourstore.gumroad.com/l/smallbiz-ai-ebook` |
| **Tier 2** | `Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip` (`17.15 MB`, 62 files) | **`$29.00`** (Interactive Workbook & Visual Shortcut Atlas) | `https://yourstore.gumroad.com/l/smallbiz-ai-workbook` |
| **Tier 3** | `Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip` (`18.96 MB`, 100 files) | **`$59.00`** (Complete Flagship Operating System Bundle) | `https://yourstore.gumroad.com/l/smallbiz-ai-os` |
| **Tier 4** | `Tier4-Living-Automation-Vault-Membership-Drop01.zip` (`19.76 MB`, 105 files) | **`$99.00 / yr`** (All-Access Living Vault + Monthly Drops) | `https://yourstore.gumroad.com/l/smallbiz-ai-vault` |

### 6.2 Enabling the Gumroad Overlay Checkout Drawer (Optional 1-Line Upgrade)
If you want buyers to complete their purchase directly on your custom domain without leaving `index.html`:
1. Add Gumroad's lightweight overlay script right before `</body>` in `15-WEB-DEPLOYMENT/dist/index.html`:
   ```html
   <script src="https://gumroad.com/js/gumroad.js"></script>
   ```
2. Update the Tier 1, Tier 2, Tier 3, and Tier 4 CTA button `href` attributes to your Gumroad product URLs (`https://yourstore.gumroad.com/l/smallbiz-ai-os?wanted=true`). Adding `?wanted=true` opens the instant checkout drawer in a single click.

---

## 7. How the Pro License Key Gate Works in `/app/` (`smallbiz-automation-os-app.html`)
When visitors click **`Launch Live Web Companion App →`** on your storefront (`/` -> `/app/index.html`), the application opens in **Free Preview Mode**:
- **activate in Free Preview Mode (`Tier 0 Lead Magnet Experience`):**
  - **Module 1 (`5-Day Time & Monthly Profit-Leak Calculator`):** Interactive sliders calculate the visitor's weekly hours saved and annual recovered profit in real time, building immediate urgency to upgrade to Tier 3 (`$59`).
  - **Module 2 (`5-Department Automation Readiness Scorecard`):** Interactive 25-point assessment with live radar/bar scoring.
  - **Module 4 (`Prompt & Script Vault — Chapter 1 Sample`):** Visitors can test and copy the 5 Chapter 1 prompts (`Prompts 1.1–1.5`) and Emergency Script #01.
- **Gated Behind the Pro License Modal (`activate for Tier 3 $59 & Tier 4 $99/yr Buyers`):**
  - Chapters 2 through 10 in the Interactive Prompt Vault (`45` additional Prompt Contracts + `11` additional Emergency Scripts), full 90-Day Kanban export, and Friday 3:00 PM Executive Scorecard JSON backup/restore.
  - Inside `Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip` and `Tier4-Living-Automation-Vault-Membership-Drop01.zip`, buyers receive `08-Pro-Web-Companion-App/PRO-ACCESS-LICENSE-KEY.txt` containing the master activation key:
    ```text
    SBAO-PRO-2026-EXEC-OS99
    ```
  - Entering `SBAO-PRO-2026-EXEC-OS99` (or its SHA-256 verification digest) activate 100% of the application permanently in `localStorage`.

---

## 8. Post-Deployment Verification & Pre-Launch Flight Checklist
Before announcing your launch on LinkedIn, Facebook Groups, YouTube, or your email list (`10-MARKETING/email-funnel-and-upsell-sequence.md`), run this 6-point verification check on your live URL:
1. **Main Storefront (`/`) Loads in `< 1.2 Seconds`:** Confirm that all 5 commercial product covers (`assets/ebook-cover-kdp-kindle.png` and `assets/gumroad-tier0..4.png`) and the 2 cheat-sheet posters (`assets/00-ECOSYSTEM-MASTER-MAP-POSTER.png` and `assets/cheat-sheet-ch01.png`) render crisp with zero broken image icons.
2. **Interactive ROI Sliders Respond Live:** Drag the 4 sliders in the Monthly Profit-Leak Calculator on `/` and confirm that `Monthly Recovered Value ($)` and `Annual ROI (%)` update immediately.
3. **Companion Web App Route (`/app/index.html`) Works End-to-End:** Click `Launch Live Web Companion App`, test the Free Preview tabs, click `activate Pro OS`, paste `SBAO-PRO-2026-EXEC-OS99`, and verify all 50 Prompts and 12 Emergency Scripts activate cleanly.
4. **Design Customizer Studio Route (`/studio/index.html`) Exports PNG & SVG:** Click `Open Live Design Customizer Studio`, select any of the 80 presets in Section 0, click `Download High-Res .PNG`, and verify that the downloaded PNG matches the selected canvas resolution (`1600×2560`, `1600×2200`, `1600×1200`, `1200×630`, or `1080×1080`).
5. **Direct Lead Magnet Downloads (`/downloads/`) Succeed:** Click `Download Full Tier 0 Starter Kit (.ZIP)` and verify that `Tier0-Free-5Day-Audit-Starter-Kit.zip` (`3.13 MB`) downloads and extracts cleanly.
6. **Custom 404 Recovery Gate (`/404.html`) Active:** Visit a non-existent URL (e.g., `/non-existent-route`) and confirm that your branded Executive Emerald & Slate 404 card routes visitors back to `/` or `/app/`.

---

## 9. Custom Domain DNS, SSL/TLS & Subdomain Routing (`Cloudflare / Namecheap / Porkbun`)
Binding a branded domain name (such as `smallbizautomationos.com` or `automation.yourcompany.com`) increases buyer trust and conversion rates on Tier 3 (`$59`) and Tier 4 (`$99/yr`) orders:
1. **Connecting a Custom Domain on Cloudflare Pages:**
   - Inside your Cloudflare Pages project (`smallbiz-ai-automation-os`), click the **`Custom domains`** tab -> **`Set up a custom domain`**.
   - Enter `smallbizautomationos.com` (and optionally `www.smallbizautomationos.com`).
   - If your domain's DNS is already managed in Cloudflare, click **`Activate domain`**—Cloudflare automatically creates the proxied `CNAME` record and issues an edge SSL/TLS certificate (`Full (Strict)`) within 60 seconds.
2. **Connecting an External Domain (`Namecheap`, `Porkbun`, `GoDaddy`) to Netlify or Vercel:**
   - Add a **`CNAME` record** for `www` pointing to your Netlify (`your-site.netlify.app`) or Vercel (`cname.vercel-dns.com`) target.
   - Add an **`ALIAS` / `ANAME` / `A` record** for the apex root (`@`) pointing to your host's load balancer IP (`76.76.21.21` for Vercel; `75.2.60.5` for Netlify).
   - Enable **`Force HTTPS / Automatic TLS`** so all HTTP requests redirect (`301`) to `https://`.
3. **Updating `robots.txt` and `sitemap.xml` After Custom Domain Activation:**
   - Open `15-WEB-DEPLOYMENT/dist/robots.txt` and `15-WEB-DEPLOYMENT/dist/sitemap.xml` in any text editor and replace `https://smallbiz-automation-os.example.com` with your live custom domain URL, then re-run `python build_phase10_deploy.py` or re-upload `dist/` so Google Search Console and Bing Webmaster Tools index your canonical URLs immediately.

---

## 10. Bangladesh Global Payout, W-8BEN Tax Treaty & Multi-Marketplace Synchronization
For digital publishing studios and founders operating from **Bangladesh** (selling globally in USD/EUR/GBP to buyers in the US, UK, Canada, Australia, and EU):
1. **Merchant-of-Record Storefronts (`Gumroad` & `LemonSqueezy`):**
   - Upload the 5 `.zip` bundles from `09-EXPORTS/HYBRID-BUNDLE/` to Gumroad and/or LemonSqueezy. Both platforms act as the global **Merchant of Record (MoR)**—automatically calculating, collecting, and remitting EU/UK VAT and US state sales tax on every digital order so you have zero foreign sales-tax filing burden.
   - Connect your **Payoneer USD Receiving Account** (Community Federal Savings Bank / Citibank / First Century Bank routing + account number) or direct Bangladesh bank SWIFT account in your payout settings, and transfer Payoneer USD funds to your local Bangladesh bank account or bKash wallet at competitive interbank rates.
2. **Amazon KDP & Draft2Digital (`US–Bangladesh Income Tax Treaty Article 12`):**
   - When publishing `Tier1-KDP-and-D2D-Retail-Book-Pack.zip` (`the-smallbiz-ai-automation-os.epub`, `the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf`, and `kdp-paperback-full-wrap-cover.pdf` with `0.5445 in` spine for `242` pages) on Amazon KDP and Draft2Digital, complete the online **IRS Form W-8BEN** tax interview.
   - Select **`Bangladesh`** as your country of tax residence, enter your **12-digit Bangladesh e-TIN (`Taxpayer Identification Number`)** in the `Foreign Tax Identifying Number (FTIN)` field, and claim **Article 12 (Royalties)** treaty benefits to reduce US statutory royalty withholding from **`30%` down to `10%`**.

---

## 11. 7-Day Organic & Email Traffic Launch Sequence (Connecting Your Web Hub to the 7-Email Funnel)
Once `15-WEB-DEPLOYMENT/dist/` is live on your public URL, execute this 7-day launch sequence using the copy-paste templates in `10-MARKETING/email-funnel-and-upsell-sequence.md`:
- **Day 1 (`Launch Announcement & Free Audit Magnet`):** Post your live storefront URL (`/`) and the direct interactive Web Companion App sandbox link (`/app/`) on LinkedIn, X/Twitter, and small-business operator communities. Invite readers to run the **60-Second Monthly Profit-Leak Calculator** on your homepage and download `Tier0-Free-5Day-Audit-Starter-Kit.zip` (`$0`).
- **Day 2 (`Email 01 & 02 — The 5-Day Time Audit & 60-Second Speed-to-Lead Proof`):** Every subscriber who downloads the Tier 0 Starter Kit receives `Email 01` (instant delivery) followed 24 hours later by `Email 02` demonstrating how the 60-second lead router recovers `$3,500–$12,000/month` in missed calls.
- **Day 3 (`Live Design Studio Showcase`):** Share a 60-second screen recording of `/studio/` (`design-customizer-studio.html`) showing how an HVAC company, dental clinic, or B2B agency can generate a white-labeled **Company AI & SOP Operations Binder Cover** in 30 seconds.
- **Day 4 (`Email 03 & 04 — The T-R-A-V Firewall & 3-Option Proposal Engine`):** Highlight the difference between fragile one-line prompts and the **50 Grounded 7-Part Prompt Contracts + 12 Emergency Scripts** inside the **Tier 3 Complete OS Bundle (`$59`)**.
- **Day 5 (`8-Tab Excel Command Center Walkthrough`):** Post a screenshot of `01_Executive_ROI_Command` and `07_Friday_Owner_Scorecard` from `the-smallbiz-ai-automation-os-financial-and-roi-matrix.xlsx` (`340` live formulas + `4` embedded charts), showing how an owner manages all 5 departments in 15 minutes every Friday at 3:00 PM.
- **Day 6 & Day 7 (`Email 05, 06 & 07 — Fast-Action Tier 3 $59 Close & Tier 4 $99/yr Vault Upgrade`):** Send the case-study breakdown, objection-handling FAQ, and final 48-hour bonus reminder driving buyers directly to your Tier 3 (`$59`) and Tier 4 (`$99/yr`) checkout links on `/` (`#pricing`).
