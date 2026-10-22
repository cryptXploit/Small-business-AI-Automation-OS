# The Small Business AI Automation OS — 5-Database Notion Setup, Relations & Formula 2.0 Engineering Guide

**Kit Directory:** `06-NOTION-TEMPLATES/`  
**Companion Web App:** `07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html`  
**Target Setup Time:** 15 Minutes (Zero Paid Notion Add-Ons Required — Works on Free & Plus Plans)  

---

## 1. Architecture of the 5-Database Minimalist Notion OS

Most small business owners abandon Notion templates because they are over-engineered with 25 nested sub-pages, aesthetic widgets that break on mobile phones, and complex relational mazes that staff refuse to update.

The **Small Business AI Automation Operating System Notion Kit** follows a strict **5-Database Minimalist Architecture**. Every single operational event across your 5 core departments lives inside one of five clean, flat, webhook-ready databases:

| Database # | CSV File Name | Core Operational Role | Primary Chapter Link | Pre-Loaded Rows |
| :--- | :--- | :--- | :--- | :--- |
| **DB 01** | `01-Inbound-Leads-and-Speed-to-Lead-CRM.csv` | Omnichannel lead intake, 60-second SLA timer, B.A.N.T.-Lite score, 3-tier quote status, and 14-day follow-up tracker. | Chapters 3 & 4 | `26 rows` |
| **DB 02** | `02-Automation-Workflows-and-Health-Registry.csv` | Master registry of active Make/n8n/Zapier pipelines, T.R.A.V. governance zones, error rates, kill-switches, and net ROI. | Chapters 1, 2 & 10 | `27 rows` |
| **DB 03** | `03-AI-Prompt-and-SOP-Vault-62.csv` | Complete 62-item production library containing all **50 Tested AI Workflow Prompts (`1.1–10.5`)** and **12 Emergency Scripts (`01–12`)**. | Chapters 1–10 + Back Matter | `62 rows` |
| **DB 04** | `04-Weekly-Owner-KPI-Scorecard.csv` | Longitudinal Friday 3:00 PM Executive Command Center tracking the 12 Core KPIs across 12 weeks of rollout. | Chapters 8, 9 & 10 | `12 rows` |
| **DB 05** | `05-Customer-Support-and-Escalation-Hub.csv` | Grounded RAG Knowledge Base truth table (`POL-01`–`POL-21`), refund ceilings, sentiment floors, and Red-Gate escalation rules. | Chapters 2, 5, 6 & 7 | `21 rows` |

---

## 2. Step-by-Step 15-Minute Notion Import & Workspace Assembly

Follow these exact steps to deploy all five databases into your Notion workspace with 100% preserved columns, status badges, and sample operational records:

### Step 1: Create Your Top-Level Command Page (Minutes 1–2)
1. Open Notion (Desktop or Web) and click **`+ New Page`** in your left sidebar.
2. Title the page: **`Small Business AI Automation OS — Executive Command Center`**.
3. Choose **`Full Width`** from the top-right three-dot menu (`... -> Full width` toggle ON) so multi-column tables and KPI dashboards display without horizontal scrolling.
4. Create two side-by-side callout blocks at the top of the page:
   - **Left Callout (Operations Emerald `#059669`):** Quick links to your active Make.com/n8n dashboard, Slack `#amber-approvals` channel, and local [`smallbiz-automation-os-app.html`](../07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html).
   - **Right Callout (Amber Gate `#D97706`):** Your team's **Zero-Hallucination & Red-Gate Compact** (*"1. Never alter deterministic SKU prices; 2. Approve Amber cards within 15 minutes; 3. Flip `automation_hold = TRUE` on any Sentiment <= 2 ticket"*).

### Step 2: Import All 5 CSV Databases (Minutes 3–8)
For each of the five CSV files in `06-NOTION-TEMPLATES/` (`01-Inbound-Leads...` through `05-Customer-Support...`):
1. Type `/table view` on your Command Center page and select **`New database`** (or click **`Import -> CSV`** from the page menu).
2. Select the CSV file from `06-NOTION-TEMPLATES/`.
3. Once imported, configure the column property types as follows so Notion formulas and Make.com/n8n API modules read numeric and date fields cleanly:
   - **In `DB 01 (Inbound Leads & Speed-to-Lead CRM)`:**
     - Set `Speed_To_Lead_Seconds`, `Qualification_Score`, and `Estimated_Deal_Value_USD` to **`Number`** (`Estimated_Deal_Value_USD` formatted as `US Dollar`).
     - Set `Inbound_Channel`, `SLA_60s_Status`, `Urgency_Tier`, `Pipeline_Stage`, and `Recommended_Quote_Tier` to **`Select`**.
     - Set `Next_Action_Date` to **`Date`**.
   - **In `DB 02 (Automation Workflows & Health Registry)`:**
     - Set `Department`, `Chapter_Ref`, `No_Code_Platform`, `TRAV_Risk_Zone`, and `Operational_Status` to **`Select`**.
     - Set `Weekly_Run_Volume`, `Weekly_Hours_Saved`, `Monthly_Tool_Cost_USD`, and `Annualized_Net_ROI_USD` to **`Number`**.
   - **In `DB 03 (AI Prompt & SOP Vault — 62 Items)`:**
     - Set `Asset_Type`, `Department`, `Chapter_Ref`, and `TRAV_Risk_Zone` to **`Select`**.
     - Keep `Full_Prompt_Or_Script_Body`, `Input_Variables`, `Expected_Output_Schema`, and `Verification_Gate_Checklist` as **`Text`** (enable `Wrap cells` on the full prompt view or open row pages in `Side Peek` mode).
   - **In `DB 04 (Weekly Owner KPI Scorecard)`:**
     - Set `Friday_Date` to **`Date`**.
     - Set `Inbound_Leads_Count`, `Median_Speed_To_Lead_Sec`, `Quotes_Sent_Count`, `Onboarding_Cycle_Hours`, `Net_New_5Star_Reviews`, `Weekly_Cash_Collected_USD`, `Overdue_AR_Over_15Days_USD`, `Average_DSO_Days`, `Owner_Hours_Worked`, `Weekly_Team_Hours_Saved`, and `Automation_Exceptions_Count` to **`Number`**.
   - **In `DB 05 (Customer Support & Escalation Hub)`:**
     - Set `Inquiry_Category`, `Tier_Level`, `Sentiment_Floor`, and `SLA_Response_Target` to **`Select`**.
     - Set `Max_Auto_Refund_USD` to **`Number`** (`US Dollar`).
4. Paste the contents of [`05-Customer-Support-and-Escalation-Hub.md`](05-Customer-Support-and-Escalation-Hub.md) into a sub-page above `DB 05` so your support staff and RAG vector indexer have both the structured policy table and the full narrative escalation playbook in one place.

---

## 3. Relational Wiring Across the 5 Databases (Minutes 9–11)

While each database works standalone out of the box, connecting three lightweight **Notion Relation & Rollup properties** turns your workspace into an interconnected operating system:

```text
+-----------------------------------------------------------------------+
| DB 03: AI Prompt & SOP Vault (50 Prompts + 12 Emergency Scripts)      |
+-----------------------------------+-----------------------------------+
                                    |
         +--------------------------+--------------------------+
         | Relation: Prompt_ID_Used                            | Relation: Linked_Prompt_Or_Script
         v                                                     v
+-----------------------------------+       +-----------------------------------+
| DB 02: Automation Workflows       |       | DB 05: Support & Escalation Hub   |
| (27 Active Pipelines & ROI)       |       | (21 Grounded Policies & Ceilings) |
+-----------------+-----------------+       +-----------------------------------+
                  |
                  | Relation: Workflow_Blueprint_Ref / Rollup: Weekly Hours Saved
                  v
+-----------------------------------+       +-----------------------------------+
| DB 01: Inbound Leads & CRM        | ----> | DB 04: Weekly Owner KPI Scorecard |
| (26 Leads, <60s SLA & Pipeline)   |       | (12-Week Friday 3:00 PM Pulse)    |
+-----------------------------------+       +-----------------------------------+
```

### How to Add the 3 Core Relations in Notion:
1. **Link `DB 02 (Workflows)` <-> `DB 03 (Prompt & SOP Vault)`:**
   - In `DB 02`, click `+` to add a column, choose **`Relation`**, select **`03-AI-Prompt-and-SOP-Vault-62`**, and toggle **`Show on 03-AI-Prompt-and-SOP-Vault-62`**.
   - Now every workflow in `DB 02` points directly to its live System Prompt in `DB 03`. When you update a prompt variable in `DB 03`, you immediately see which active Make.com/n8n scenarios use it.
2. **Link `DB 05 (Support Hub)` <-> `DB 03 (Prompt & SOP Vault)`:**
   - In `DB 05`, add a **`Relation`** column pointing to **`03-AI-Prompt-and-SOP-Vault-62`**.
   - Link `POL-01..POL-21` to their corresponding support prompts (`Prompt 6.1`–`6.5`) and Red-Gate crisis scripts (`Emergency Script 01`–`12`).
3. **Link `DB 02 (Workflows)` -> `DB 04 (Weekly Owner KPI Scorecard)`:**
   - In `DB 04`, add a **`Rollup`** property pulling `Sum of Weekly_Hours_Saved` and `Sum of Annualized_Net_ROI_USD` from `DB 02` so your Friday Scorecard automatically displays total hours recovered across all active workflows.

---

## 4. Copy-Paste Notion Formula 2.0 Code Blocks (Minutes 12–15)

Notion Formula 2.0 allows you to embed automatic Green / Amber / Red status badges and financial calculations directly inside your database rows. Create a **`Formula`** column in the respective database below and paste the exact code block:

### Formula 1: 60-Second Speed-to-Lead SLA Status Badge (`Add to DB 01`)
**Formula Column Name:** `Live_SLA_Grade`  
**Purpose:** Automatically grades each lead based on `Speed_To_Lead_Seconds` against the Chapter 3 `60-Second` benchmark.

```javascript
lets(
  sec, prop("Speed_To_Lead_Seconds"),
  ifs(
    empty(sec), "⏳ PENDING FIRST TOUCH",
    sec <= 60, "🟢 PASS (<60s Instant SLA): " + format(sec) + "s",
    sec <= 300, "🟡 AMBER (1-5 Min Delay — 22% Decay Risk): " + format(sec) + "s",
    "🔴 BREACH (>5 Min Delay — High Leak Risk): " + format(sec) + "s"
  )
)
```

### Formula 2: Weighted Pipeline Expected Value Calculator (`Add to DB 01`)
**Formula Column Name:** `Weighted_Pipeline_USD`  
**Purpose:** Multiplies `Estimated_Deal_Value_USD` by the stage probability (`Closed Won = 100%`, `Quote Sent = 45%`, `Booked Consult = 30%`, `Active Follow-Up = 20%`).

```javascript
lets(
  val, prop("Estimated_Deal_Value_USD"),
  stg, prop("Pipeline_Stage"),
  prob, ifs(
    stg == "Closed Won", 1.00,
    contains(stg, "Quote Sent"), 0.45,
    stg == "Booked Consult", 0.30,
    stg == "Active Follow-Up", 0.20,
    0.10
  ),
  round(val * prob)
)
```

### Formula 3: Workflow Annualized Net Labor & Cashflow ROI (`Add to DB 02`)
**Formula Column Name:** `Calculated_Annual_Labor_Savings_USD`  
**Purpose:** Computes annual labor value recovered at a blended `$58/hr` rate minus annual tool-stack subscription cost (`Monthly_Tool_Cost_USD * 12`).

```javascript
lets(
  hrsWk, prop("Weekly_Hours_Saved"),
  toolMo, prop("Monthly_Tool_Cost_USD"),
  blendedRate, 58,
  grossAnnual, hrsWk * blendedRate * 52,
  netAnnual, grossAnnual - (toolMo * 12),
  "$" + format(round(netAnnual)) + "/yr (" + format(round(hrsWk * 52)) + " hrs saved)"
)
```

### Formula 4: T.R.A.V. Governance & Error-Rate Safety Monitor (`Add to DB 02`)
**Formula Column Name:** `Governance_Health_Alert`  
**Purpose:** Flags any workflow whose `TRAV_Risk_Zone` is Red or Amber so operators never disable human approval gates prematurely.

```javascript
lets(
  zone, prop("TRAV_Risk_Zone"),
  status, prop("Operational_Status"),
  ifs(
    status != "Active Production", "⚪ PAUSED / SANDBOX",
    contains(zone, "Red"), "🔴 RED GATE: Immediate Human Takeover Required",
    contains(zone, "Amber"), "🟡 AMBER GATE: 15s Slack Approval Required Before Send",
    "🟢 GREEN GATE: 100% Autonomous 24/7 Execution"
  )
)
```

### Formula 5: Friday 3:00 PM Owner Scorecard Composite Health Badge (`Add to DB 04`)
**Formula Column Name:** `Composite_OS_Grade`  
**Purpose:** Evaluates weekly `Median_Speed_To_Lead_Sec`, `Average_DSO_Days`, `Overdue_AR_Over_15Days_USD`, and `Weekly_Team_Hours_Saved` to produce an instant Friday executive status.

```javascript
lets(
  stl, prop("Median_Speed_To_Lead_Sec"),
  dso, prop("Average_DSO_Days"),
  overdue, prop("Overdue_AR_Over_15Days_USD"),
  hrsSaved, prop("Weekly_Team_Hours_Saved"),
  ifs(
    stl <= 60 and dso <= 16 and overdue <= 2500 and hrsSaved >= 15,
    "🟢 ELITE OS HEALTH (All 4 Core Pillars Passing)",
    stl <= 120 and dso <= 25 and overdue <= 6000,
    "🟡 AMBER WATCH (Review Variance Bottleneck in Prompt 10.1)",
    "🔴 ACTION REQUIRED (Check Speed-to-Lead or Overdue AR Ladder)"
  )
)
```

---

## 5. Recommended Saved Views for Daily & Weekly Execution

To keep your team focused without visual clutter, create these three filtered **Saved Views** at the top of your Notion Command Center:

1. **View 1 — Daily Frontline Speed-to-Lead & Follow-Up Board (`DB 01 — Board View`):**
   - **Group By:** `Pipeline_Stage` (`Booked Consult` -> `Quote Sent` -> `Active Follow-Up` -> `Closed Won`).
   - **Sort By:** `Qualification_Score` (`Descending`) and `Next_Action_Date` (`Ascending`).
   - **Who Uses It:** Front-desk coordinators and sales reps for 10 minutes each morning at 8:30 AM.
2. **View 2 — Amber Gate & Emergency Script Quick-Reference Gallery (`DB 03 — Gallery View`):**
   - **Filter:** `TRAV_Risk_Zone` contains `Amber` OR `Asset_Type` equals `Emergency Operations Script (Red Gate)`.
   - **Card Preview:** Show `Vault_ID`, `Title`, `Trigger_Condition`, and `Input_Variables`.
   - **Who Uses It:** Operations leads and managers whenever a high-stakes client exception occurs.
3. **View 3 — Friday 3:00 PM Founder 15-Minute Pulse (`DB 04 — Table + Chart View`):**
   - **Sort By:** `Friday_Date` (`Descending`).
   - **Summary Row Calculations:** Set bottom column summaries to `Average` on `Median_Speed_To_Lead_Sec` and `Average_DSO_Days`, and `Sum` on `Weekly_Cash_Collected_USD` and `Weekly_Team_Hours_Saved`.
   - **Who Uses It:** The business owner every Friday afternoon at 3:00 PM (`Chapter 10`) before closing the laptop for the weekend.

---

## 6. Connecting Make.com, Zapier & n8n to Your 5 Notion Databases via Internal Integration Token

To allow your automation workflows (`Chapter 3` Lead Router, `Chapter 5` Onboarding Provisioner, `Chapter 6` Support Triage, `Chapter 8` Invoice & Price-Creep Auditor, and `Chapter 10` Friday KPI Synthesizer) to create and update rows automatically inside `DB 01` through `DB 05`:

### Step 1: Create Your Dedicated Service Integration in Notion (`2 Minutes`)
1. Navigate to `https://www.notion.so/my-integrations` while signed in with your company workspace admin account.
2. Click **`+ New integration`** and name it **`SmallBiz-AI-Automation-OS-Engine`**.
3. Under **Capabilities**, enable **`Read content`**, **`Update content`**, and **`Insert content`**. Under **User Capabilities**, select **`No user information`** if you want strict minimal-privilege privacy, or **`Read user information without email addresses`** if assigning owners by Notion User ID.
4. Copy the generated **`Internal Integration Secret`** (`ntn_...` or `secret_...`) and store it inside your Make.com, n8n, or Zapier encrypted connection vault.

### Step 2: Grant Database-Level Access to Your 5 OS Databases (`1 Minute`)
In Notion, integrations cannot read or write to any page unless explicitly invited to that page:
1. Open your top-level **`Small Business AI Automation OS — Executive Command Center`** page (which holds `DB 01` through `DB 05` as child databases).
2. Click the top-right **`...`** menu, scroll down to **`Connections` -> `Connect to`**, and select **`SmallBiz-AI-Automation-OS-Engine`**.
3. Because child databases inherit parent page permissions in Notion, connecting the parent Command Center page automatically grants your Make.com/n8n workflows secure read/write access to all five databases simultaneously while keeping the rest of your private company pages completely isolated.

### Step 3: Copy Your 32-Character Notion Database IDs for Webhook Mapping
Each of your five imported databases has a unique 32-character hexadecimal `Database_ID` found in its browser URL (`https://www.notion.so/yourworkspace/<32_CHAR_DATABASE_ID>?v=...`):
- **Database 01 ID (`NOTION_DB01_LEADS_ID`):** Paste into **Blueprint 01 (`Lead Capture & 60s SMS Router`)** and **Blueprint 02 (`3-Tier Quote & 14-Day Follow-Up`)** so every new inbound inquiry creates a row with `Lead_Received_Timestamp`, `First_Touch_Timestamp`, `Speed_To_Lead_Seconds`, and `Qualification_Score`.
- **Database 02 ID (`NOTION_DB02_WORKFLOWS_ID`):** Used by the **Dead-Letter Queue Monitor (`Prompt 2.5`)** and **Quarterly Governance Auditor (`Prompt 10.4`)** to log weekly execution counts and error rates.
- **Database 03 ID (`NOTION_DB03_VAULT_ID`):** Used by **Prompt 9.1 (`7-Block Living SOP Compiler`)** whenever a new Loom video is dropped into `#sop-capture`, automatically creating a structured SOP row ready for a 15-second owner review.
- **Database 04 ID (`NOTION_DB04_SCORECARD_ID`):** Used every Friday at 2:55 PM by **Prompt 10.1 (`Friday Executive KPI Synthesizer`)** to write the week's 12 aggregated metrics and generate the Slack executive brief.
- **Database 05 ID (`NOTION_DB05_SUPPORT_ID`):** Queried in real time by **Prompt 6.2 (`Grounded RAG Support Responder`)** to fetch the verified `Approved_Policy_Summary` and `Max_Auto_Refund_USD` ceiling before drafting any customer reply.

---

## 7. Team Role Permissions, Mobile App Pinning & Weekly CSV Backup Protocol

### 7.1 Role-Based Access Control (RBAC) for 1-to-25 Person Teams
- **Founder / Operations Director (`Full Access`):** Can edit database schemas, modify `Approved_Policy_Summary` rows in `DB 05`, adjust `Max_Auto_Refund_USD` ceilings, and sign off on `DB 04` Friday Scorecards.
- **Sales Reps, Front-Desk & Fulfillment Staff (`Can Edit Content` — Schema Locked):** Click **`Lock database`** on `DB 01`, `DB 02`, `DB 03`, `DB 04`, and `DB 05` once imported! In Notion, locking a database prevents staff from accidentally deleting a column or breaking a Formula 2.0 block while still allowing them to add leads, update pipeline stages, and check off tasks normally.
- **External Bookkeepers or Contractors (`Can View` or Filtered Page Share):** Share only the specific filtered view required for their role.

### 7.2 Pinning the Mobile Quick-Capture Views (`iOS & Android`)
Install the Notion mobile app on your phone and add two home-screen shortcuts:
1. **`#amber-approvals` & `DB 01` Active Today View:** Allows you to inspect high-ticket leads on the go in 15 seconds.
2. **`DB 04` Friday 3:00 PM Scorecard View:** Lets you review all 12 core business metrics from your phone on Friday afternoon in under 5 minutes.

### 7.3 Monthly Offline CSV Snapshot Protocol (`30 Seconds`)
On the first Friday of each month (alongside `Prompt 10.3`), click **`... -> Export -> Markdown & CSV`** on your top-level Command Center page and save the `.zip` archive to your local company backup drive alongside your Web Companion App JSON backup (`smallbiz-automation-os-backup.json`). This ensures 100% offline disaster recovery and audit readiness year-round.
