# Worksheet 8: Receivables Automation & Monthly Close Checklist

**Companion to:** Chapter 8 — *Back-Office Autopilot: Invoicing, Payment Chasers, Bookkeeping Prep & Vendor Triage*  
**Framework Reference:** *The Cashflow Collection & Receipt Extraction Pipeline (Milestone Instant Invoicing -> 5-Stage Polite-to-Firm Payment Chaser Ladder -> OCR Receipt & Vendor Bill Triage -> 5-Day Monthly Bookkeeping Pre-Close)*  
**Department Engine:** `Dept 04 — Back-Office Billing, Cashflow & Bookkeeping Prep`  
**Estimated Completion Time:** 45 Minutes  
**Interactive Companion:** Pre-configured inside the Notion Small Business OS (`06-NOTION-TEMPLATES/`), the 8-Tab Excel Command Center (`06-NOTION-TEMPLATES/Spreadsheets/`), and the Pro Web App Suite (`07-INTERACTIVE-TOOLS/index.html` — Access Code: `SMALLBIZ-OS-PRO-2026`).

---

## Instructions for the Owner, Office Manager & Bookkeeper

Profit on an income statement does not pay Friday payroll—**collected cash in your operating bank account does**. In most 1–25 person businesses, cashflow crunches are caused by two preventable back-office habits:
1. **The "Friday/Sunday Billing Batch" Delay:** Waiting days or weeks after completing a job or milestone before generating and sending the customer invoice—and then feeling too awkward or busy to follow up systematically when an invoice goes past due.
2. **The "Month-End Shoebox" Scramble:** Letting field receipts, vendor PDF bills, and uncategorized credit card charges pile up for 30 days, resulting in hidden vendor price hikes, missed tax deductions, and financial statements that arrive three weeks too late to guide decisions.

Use this 5-part operational workbook to map your **Milestone Invoicing Triggers**, calculate your **Baseline Days Sales Outstanding (DSO) & Trapped Cash**, configure your **5-Stage Polite-to-Firm Payment Chaser Ladder**, standardize your **Vendor OCR & Chart-of-Accounts GL Mapping Grid**, and execute a **5-Day Monthly Bookkeeping Pre-Close**.

---

## Part 1: Invoicing Trigger & Billing SLA Audit Table (`Prompt 8.1`)

Eliminate manual batch invoicing by tying every revenue stream in your business to a deterministic **Completion or Milestone Webhook** that runs `Prompt 8.1` (*Completed-Job Notes to Itemized Customer Invoice Line-Item Formatter*) within 60 seconds of work sign-off.

| Revenue Stream / Billing Model | Exact Operational Trigger Event (POS / CRM / PM Tool) | Accounting Target (`QBO / Xero / Stripe / Square`) | Execution Gate (`Green Auto-Send` vs. `Amber 1-Click Approve`) | Target Billing SLA | Payment Methods Enabled on Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Fixed-Price Field / Service Jobs** *(HVAC, Electrical, Auto, Cleaning, Clinics)* | Technician/Clinician marks Work Order `Completed & Signed` | QuickBooks Online / Xero / Stripe Invoice | **Green Zone** *(If total matches signed estimate)* | **`< 60 Seconds`** post sign-off | `[ ] Card [ ] ACH [ ] Apple/Google Pay` |
| **2. Progress / Milestone Projects** *(Agencies, Construction, Custom Fabrication)* | Client signs off on Milestone Deliverable OR Project Board moves to `Milestone Complete` | QuickBooks / Xero Progress Invoice (`50% / 25% / 25%`) | **Amber Zone** *(1-Click PM Approval of `Prompt 8.1` memo)* | **`< 2 Hours`** of milestone completion | `[ ] ACH Bank Transfer [ ] Card` |
| **3. Recurring Monthly Retainers / Memberships** | Scheduled Cron on `1st` or `15th` of Month | Stripe Subscription / QBO Recurring Invoice | **Green Zone** *(Auto-charge stored payment method)* | **`08:00 AM`** on billing date | `[ ] Auto-Debit ACH [ ] Card on File` |
| **4. Time-and-Materials / Change Orders** | Approved Change Order or Weekly Logged Hours | QBO / Xero Itemized Invoice (`Prompt 8.1` translates tech notes) | **Amber Zone** *(Owner/Manager 1-Click review)* | **Every Friday by `12:00 PM`** | `[ ] ACH [ ] Card` |
| **Your Billing Stream #1:** `_____________________` | Trigger: `_____________________` | System: `_____________________` | `[ ] Green [ ] Amber` | SLA: `_________` | `[ ] ACH [ ] Card` |
| **Your Billing Stream #2:** `_____________________` | Trigger: `_____________________` | System: `_____________________` | `[ ] Green [ ] Amber` | SLA: `_________` | `[ ] ACH [ ] Card` |

---

## Part 2: Aged Receivables & Days Sales Outstanding (DSO) Calculator

Before activating your automated payment chasers, audit your current Accounts Receivable (AR) aging report from QuickBooks, Xero, Stripe, or FreshBooks to quantify how much working capital is currently trapped in unpaid customer invoices.

### 2.1 Current Accounts Receivable Aging Snapshot

| AR Aging Bucket | Number of Open Invoices (`#`) | Total Dollar Balance (`$`) | `%` of Total Open AR | Historical Collection Probability | Immediate Action Required (`Prompt 8.2`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Current (`0 – Due Date`)** | `______` | `$______________` | `____ %` | `98%+` | Enroll in Stage 1 (`Day -3` Courtesy Pre-Due Reminder) |
| **1 – 7 Days Past Due** | `______` | `$______________` | `____ %` | `94%` | Trigger Stage 2 (`Day +1`) & Stage 3 (`Day +7`) Chasers |
| **8 – 15 Days Past Due** | `______` | `$______________` | `____ %` | `85%` | Trigger Stage 3 (`Day +7`) + Offer 2-Part Split / Card Link |
| **16 – 30 Days Past Due** | `______` | `$______________` | `____ %` | `72%` | Route to Stage 4 (`Day +15` Amber Gate — Work Pause Notice) |
| **31 – 60 Days Past Due** | `______` | `$______________` | `____ %` | `51%` | Route to Stage 5 (`Day +30` Red Gate — Owner Call + Script 02) |
| **61+ Days Past Due** | `______` | `$______________` | `____ %` | `< 28%` | Final Demand Notice (`Emergency Script 02`) / Collections |
| **TOTAL OPEN RECEIVABLES** | **`______`** | **`$______________`** | **`100%`** | — | **Target 60-Day Recovery: `>= 75%` of Past-Due Balance** |

### 2.2 Days Sales Outstanding (DSO) & Trapped Working Capital Formula

Calculate your baseline DSO and the exact cash freed when the Chapter 8 pipeline reduces your DSO to your target (`14 Days`):

$$\text{Current DSO (Days)} = \left( \frac{\text{Total Open Accounts Receivable (\$)}}{\text{Total Credit/Invoiced Sales Over Last 90 Days (\$)}} \right) \times 90$$

$$\text{Working Capital Freed (\$)} = \left( \text{Current DSO} - \text{Target DSO} \right) \times \left( \frac{\text{Annual Invoiced Revenue (\$)}}{365} \right)$$

* **Your Total Open Accounts Receivable (`$`):** `$____________________`
* **Your Invoiced Sales Over Last 90 Days (`$`):** `$____________________`
* **Your Baseline DSO (`Days`):** `________ Days` *(Small Business Manual Average: `38 to 46 Days`)*
* **Your Target Automated DSO (`Days`):** `14 Days`
* **Your Average Daily Invoiced Revenue (`Annual / 365`):** `$____________ / day`
* **Total Trapped Cash Unlocked into Your Bank Account:** **`$____________________`**

---

## Part 3: 5-Stage Payment Chaser Cadence & Stop-Logic Checklist (`Prompt 8.2`)

Configure your 5-stage overdue invoice follow-up sequence in QuickBooks/Xero + Make/Zapier/n8n using `Prompt 8.2`. Verify that every guardrail and stop-condition below is active before turning on the workflow:

| Chaser Stage | Timing Trigger | Risk Gate Zone | Channel | Tone & Core Operational Hook (`Prompt 8.2`) | Mandatory Pre-Send Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Courtesy Pre-Due** | **3 Days Before Due Date** (`Day -3`) | **Green Zone** *(Auto-Send)* | Email | Warm heads-up that Invoice `#{{inv_num}}` (`${{amount}}`) is due on `{{due_date}}`; includes 1-click ACH/Card link and attached PDF for their AP team. | Confirm `invoice_balance > $0` and `open_dispute == false` |
| **Stage 2: Friendly Nudge** | **1 Day Past Due** (`Day +1`) | **Green Zone** *(Auto-Send)* | Email + SMS | Assumes honest oversight (*"Inboxes get busy—resending your 1-click payment link for Invoice #{{inv_num}}"*). Zero accusation or friction. | Confirm bank/Stripe webhook has not recorded payment in last 24h |
| **Stage 3: Helpful Check-In** | **7 Days Past Due** (`Day +7`) | **Green Zone** *(Auto-Send)* | Email + SMS | Asks if their accounting department needs a W-9, PO number update, or a 2-part payment split link to clear the balance today. | Confirm no pending ACH settlement (`status != "processing"`) |
| **Stage 4: Firm Work-Pause Warning** | **15 Days Past Due** (`Day +15`) | **Amber Zone** *(1-Click Owner/Mgr Approval)* | Email + SMS + Phone Task | Polite but firm executive notice: per service agreement terms, active work/deliveries/scheduling will pause in **48 hours** if balance remains unpaid. | **Human Approval Required:** Owner verifies no active handshake extension |
| **Stage 5: Final Pre-Collections** | **30 Days Past Due** (`Day +30`) | **Red Zone** *(Mandatory Owner Sign-Off)* | Certified Email + SMS (`Script 02`) | Formal notice of contractual late fee assessment (`{{late_fee_pct}}%`) and 7-day deadline before transferring file to collections/legal recovery. | **Owner Sign-Off Required:** Pause all recurring services immediately |

### Critical Stop-Logic Verification Checklist
- [ ] **Webhook Stop Condition 1 (`invoice.paid`):** Does the instant a payment is received in Stripe, Square, QuickBooks, or Xero set `invoice_balance = 0` and immediately terminate all scheduled Stage 1–5 chasers?
- [ ] **Webhook Stop Condition 2 (`payment.processing`):** If a B2B client initiates an ACH bank transfer on Day +2 (which takes 3–4 banking days to settle), does the router pause Stage 3 so the client is not nagged while their bank transfer is in flight?
- [ ] **Webhook Stop Condition 3 (`tier3_dispute_active`):** If the client has an open Tier 3 complaint ticket (`Chapter 6`), does the router route the overdue invoice to an Amber Manager Review instead of sending automated dunning texts?

---

## Part 4: Vendor Receipt OCR & Chart-of-Accounts GL Mapping Grid (`Prompts 8.3 & 8.4`)

Create a dedicated forwarding email alias (`receipts@yourcompany.com` or `ap@yourcompany.com`) and a shared field-staff SMS/Slack upload channel. Whenever a vendor PDF invoice or receipt photo arrives, `Prompt 8.3` extracts the structured JSON fields and maps the expense to your exact Chart of Accounts below, while `Prompt 8.4` checks for vendor unit-price increases `> 5%`.

| Standard GL Code | Account Category Name (`QBO / Xero`) | Common Vendor / Expense Examples | Required Job / Project Costing Tag? | Price-Creep Alert Threshold (`Prompt 8.4`) |
| :--- | :--- | :--- | :--- | :--- |
| `GL-5100` | **Cost of Goods Sold (COGS) — Materials & Parts** | Wholesale parts, lumber, clinical supplies, raw ingredients, packaging | **`[X] YES`** *(Require `Job_ID` or `Batch_ID`)* | Flag if unit price increases **`> 5.0%`** vs. 90-day baseline |
| `GL-5200` | **COGS — Subcontractors & Field Labor** | Specialty trade subcontractors, freelance production specialists | **`[X] YES`** *(Require `Job_ID` & Signed PO)* | Flag if total exceeds approved PO by **`> $0.00`** |
| `GL-6120` | **Vehicle, Fuel & Fleet Maintenance** | Gas station receipts, fleet oil/tire service, commercial auto insurance | `[ ] Optional` *(Tag `Truck_Number`)* | Flag single fuel receipt **`> $175.00`** |
| `GL-6240` | **Software, SaaS & Cloud Subscriptions** | CRM, OpenAI/Anthropic API, Make/Zapier, Adobe, Microsoft 365, Google | `[ ] No` *(Overhead)* | Flag any new recurring charge or tier jump **`> 5.0%`** |
| `GL-6310` | **Advertising & Lead Generation** | Google Local Service Ads, Meta Ads, print mailers, directory fees | `[ ] Optional` *(Tag `Campaign`)* | Reconcile monthly against `Dept 01` CAC scorecard |
| `GL-6450` | **Shop, Clinic & Office Supplies** | Small tools, cleaning supplies, printer paper, breakroom items | `[ ] No` *(Overhead)* | Flag single receipt **`> $250.00`** for Amber review |
| `GL-6999` | **Uncategorized / Suspense (Needs Review)** | Ambiguous vendor name or missing line-item detail | **`[X] YES`** *(Auto-chase staff member)* | Route to `Prompt 8.5` Monthly Pre-Close Chaser |

---

## Part 5: Monthly 5-Day Bookkeeping Pre-Close Checklist (`Prompt 8.5`)

Run this 5-day sequence on **Days 1 through 5 of every month** so your bookkeeper or CPA delivers finalized Profit & Loss, Balance Sheet, and Cashflow statements by the **5th business day**:

- [ ] **Day 1 (Automated Bank/Card Feed Audit — `Prompt 8.5`):** Export the prior month's bank and credit card transactions and match against uploaded receipts in `receipts@yourcompany.com`. Automatically generate the **Staff Missing-Receipt Chaser List** and **Duplicate/Zombie Subscription Report**.
- [ ] **Day 2 (Automated Staff Receipt Collection):** Dispatch individual Slack/SMS prompts to any cardholder with a missing receipt `>= $25.00` (*"Hi Carlos, please snap a photo of the Oct 19 Home Depot receipt for $142.80 and reply to this text"*).
- [ ] **Day 3 (Vendor Price-Creep & AP Reconciliation — `Prompt 8.4`):** Review all flagged Amber vendor bills where unit prices increased by `> 5%` or duplicate invoice numbers were detected before releasing vendor ACH payments.
- [ ] **Day 4 (AR Aging & Bad-Debt Review):** Reconcile all collected Stripe/Square payouts against QuickBooks/Xero invoices, accounting for merchant processing fees automatically.
- [ ] **Day 5 (Executive Financial Package Sign-Off):** Bookkeeper locks the prior month's ledger and delivers the 1-Page Monthly P&L, Gross Margin by Service Line, and 13-Week Cashflow Forecast to the Owner.

### Back-Office Autopilot Deployment Sign-Off

- **Milestone Invoice Trigger & `Prompt 8.1` Line-Item Formatter Live:** `[ ] Verified Live`
- **5-Stage Payment Chaser (`Prompt 8.2`) & Webhook Stop-Logic Tested:** `[ ] Verified Live`
- **Receipt OCR Inbox (`Prompt 8.3`) & Price-Creep Detector (`Prompt 8.4`) Active:** `[ ] Verified Live`
- **Sign-Off Date:** `____ / ____ / 2026` | **Owner / Finance Lead Signature:** `___________________________`
