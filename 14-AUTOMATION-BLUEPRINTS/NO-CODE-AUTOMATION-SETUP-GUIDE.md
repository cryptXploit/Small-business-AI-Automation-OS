# No-Code Automation Blueprints Setup, Wiring & Testing Manual (Make.com, n8n & Zapier)

**Document ID:** `14-AUTOMATION-BLUEPRINTS/NO-CODE-AUTOMATION-SETUP-GUIDE.md`  
**Project:** *The Small Business AI Automation Operating System* (`2026 Enterprise Edition`)  
**Included Blueprints:** `01` through `05` (Universal Make.com / n8n / Zapier JSON Workflow Specifications)  

---

## 1. Overview of the 5 Production Automation Blueprints
The `14-AUTOMATION-BLUEPRINTS/` directory contains five production-grade JSON workflow blueprints covering every department of the **5-Department Small Business AI Automation Engine**. Each blueprint implements our **T.R.A.V. (Trigger -> Rules -> AI -> Verification)** safety contract so that deterministic rules calculate every dollar figure, Pre-AI regex gates intercept emergencies and PII, and Amber/Red Slack gates keep a human in command of high-stakes decisions.

| Blueprint File | Department & Chapter | Primary Trigger Event | Governance Gate Split | Core SLA Target |
| :--- | :--- | :--- | :--- | :--- |
| **`01-60s-instant-lead-router-and-sms-intake.json`** | **Dept 01 (Ch 3)** | Inbound Web Form, Missed Call, or Social Lead Ad Webhook | `80% Green` / `15% Amber` / `5% Red` | `< 60 sec` response; `< 15 sec` missed-call text-back |
| **`02-ai-support-triage-and-amber-approval-gate.json`** | **Dept 03 (Ch 6)** | Inbound Customer Email, SMS, or Chat Support Ticket | `68% Green` / `24% Amber` / `8% Red` | `< 45 sec` Tier-1 auto-resolution; `< 15m` Red takeover |
| **`03-3option-instant-quote-and-14day-followup.json`** | **Dept 02 (Ch 4)** | Estimator 90-Second Voice Memo or Discovery Form Submission | `20% Green` / `75% Amber` / `5% Red` | `< 15 min` 3-option quote dispatch; `>= 35%` close rate |
| **`04-overdue-invoice-5stage-payment-chaser.json`** | **Dept 04 (Ch 8)** | Job Completion Webhook & Daily `08:30 AM` AR Aging Poll | `75% Green` / `20% Amber` / `5% Red` | Average DSO `<= 16 days`; Overdue `>15d <= $2,500` |
| **`05-friday-3pm-owner-kpi-executive-digest.json`** | **Dept 05 (Ch 10)** | Scheduled Weekly Cron (`Friday 15:00` Local Time) | `100% Executive Summary` | Delivered Friday `3:00 PM`; `< 15 min` Owner review |

---

## 2. Step-by-Step Import & Wiring Instructions by Platform

### 2.1 Importing & Wiring in Make.com (Recommended Visual Orchestrator)
1. **Create a Dedicated Folder in Make.com:** Log into Make.com (`Core` or `Pro` plan, `$9–$29/mo`), navigate to **`Scenarios`**, and create a folder named **`SmallBiz-AI-Automation-OS-2026`**.
2. **Import Blueprint Structure:** Click **`Create a new scenario -> More (...) -> Import Blueprint`** or use the 6-node architecture defined inside each `.json` file (`Node 01` through `Node 06`) to wire your Connections:
   - **Node 01 (`Custom Webhook`):** Copy the generated Make.com webhook URL and paste it into your website form plugin (WPForms, Gravity Forms, Typeform, Webflow, Tally) and your phone system (`OpenPhone` or `Twilio` Missed-Call Webhook).
   - **Node 02 (`Pre-AI Regex & PII Scrubber`):** Paste the exact `red_zone_abort_regex` and `mask_credit_cards_regex` strings from the JSON blueprint into a Make `Text Parser -> Replace` and `Router Filter` before your OpenAI module.
   - **Node 03 (`Notion / Google Sheets Truth-Table Lookup`):** Connect your Notion workspace (`06-NOTION-TEMPLATES/`) or Excel/Google Sheet (`06-NOTION-TEMPLATES/Spreadsheets/`) so locked SKU prices and FAQ policy clauses are injected deterministically.
   - **Node 04 (`OpenAI / Anthropic JSON Module`):** Select model **`gpt-4o-mini`** (for high-speed routing in Blueprints 01, 02, 04) or **`gpt-4o` / `claude-3-5-sonnet`** (for 3-tier proposals in Blueprint 03 and executive synthesis in Blueprint 05). Set **`Temperature = 0.0` (or `0.1`)** and **`Response Format = JSON Object`**.
   - **Node 05 (`Basic Router — Green / Amber / Red`):** Configure the three filter branches (`assigned_gate == "GREEN"`, `assigned_gate == "AMBER"`, `assigned_gate == "RED"`).
   - **Node 06 (`Error Handler — Dead-Letter Queue`):** Right-click the OpenAI and HTTP modules, select **`Add error handler`**, and connect a Notion/Google Sheets row logger plus a `#red-alerts` Slack notification node.

### 2.2 Importing & Wiring in n8n (Cloud or Self-Hosted Docker Edition)
1. **Open Your n8n Canvas:** In n8n (`Workflows -> Add Workflow`), click the top-right menu (`... -> Import from File`) or copy the node parameters from the `.json` specification.
2. **Configure Credentials in n8n:**
   - Add your **OpenAI API Credential**, **Notion API Integration Secret**, **Slack OAuth/Webhook Credential**, and **Twilio Account SID/Auth Token** inside n8n's encrypted Credentials vault.
   - In the **Code Node (`Node 02`)**, run the JavaScript/Python E.164 phone normalization and Regex PII scrubber so zero raw card numbers or SSNs ever leave your n8n instance.
   - Attach an **Error Trigger (`Node 06`)** workflow that writes any failed execution ID and payload to `02-Automation-Workflows-and-Health-Registry.csv`.

### 2.3 Wiring in Zapier (Multi-Step Zaps with Paths)
1. Create a new Zap starting with **Webhooks by Zapier (`Catch Hook`)** (for Blueprints 01–03) or **Schedule by Zapier** (for Blueprints 04–05).
2. Add **Code by Zapier (`Run Python`)** as Step 2 to execute the Pre-AI Regex Red-Zone check and PII masking.
3. Add **Notion (`Find Database Item`)** as Step 3, **ChatGPT (`Conversation` with `temperature: 0.0`)** as Step 4, and **Paths by Zapier** (`Path A: Green`, `Path B: Amber Slack Approval`, `Path C: Red Escalation`) as Step 5.

---

## 3. Environment Variables & Credential Security Checklist
Before turning any scenario from `OFF` to `ON`, configure these ten environment variables in your platform's encrypted variable store:

| Variable Name | Example / Format | Purpose & Security Rule |
| :--- | :--- | :--- |
| `COMPANY_NAME` | `"Apex Comfort HVAC & Plumbing"` | Injected into system prompts and SMS footers. |
| `OPENAI_API_KEY` | `sk-proj-...` (Zero Data Retention enabled) | Dedicated departmental API key with `$50/mo` spend cap. |
| `NOTION_INTEGRATION_SECRET` | `ntn_...` | Scoped strictly to the 5 Notion OS databases. |
| `NOTION_DB01_LEADS_ID` | `32-char UUID` | Target database for Blueprint 01 & 03 lead logging. |
| `NOTION_DB02_WORKFLOW_REGISTRY_ID` | `32-char UUID` | Target database for execution health & Dead-Letter Queue logs. |
| `SLACK_AMBER_WEBHOOK_URL` | `https://hooks.slack.com/services/...` | Posts 15-second interactive approval cards to `#amber-approvals`. |
| `SLACK_RED_ALERTS_WEBHOOK_URL` | `https://hooks.slack.com/services/...` | Pages on-call manager in `#red-alerts` on Red-Gate triggers. |
| `TWILIO_ACCOUNT_SID` | `AC...` | Programmable SMS & Missed-Call Voice webhook authentication. |
| `TWILIO_AUTH_TOKEN` | `32-char secret` | Stored in encrypted connection vault; rotate every 90 days. |
| `TWILIO_FROM_NUMBER_E164` | `+15125550100` | Registered A2P 10DLC business SMS number. |

---

## 4. Copy-Paste `curl` Webhook Testing Commands (Shadow-Mode Verification)
Never test a newly wired workflow on live customers first. Open PowerShell, Terminal, or Postman and run the three test payloads below against your webhook URL while your SMS/Email nodes are pointed at your internal test address (`qa-test@yourcompany.com`):

### Test 1: Routine Green-Gate Lead Intake (`Should Auto-Reply in < 60s`)
```bash
curl -X POST "https://hook.us1.make.com/YOUR_WEBHOOK_ID"   -H "Content-Type: application/json"   -H "X-Studio-Webhook-Signature: sha256=test_signature_01"   -d '{
    "event_id": "test_green_001",
    "source_channel": "website_form",
    "full_name": "Alex Rivera",
    "phone_e164": "+15125550199",
    "email": "qa-test@yourcompany.com",
    "postal_code": "78704",
    "customer_message": "Hi, I would like to book a standard seasonal tune-up next week.",
    "sms_opt_in_verified": true
  }'
```

### Test 2: High-Ticket Amber-Gate Quote Request (`Should Post Approval Card to #amber-approvals`)
```bash
curl -X POST "https://hook.us1.make.com/YOUR_WEBHOOK_ID"   -H "Content-Type: application/json"   -d '{
    "event_id": "test_amber_002",
    "estimator_name": "David Morales",
    "client_name": "Metro Commercial Properties",
    "client_email": "qa-test@yourcompany.com",
    "voice_memo_transcript": "Walked 4-unit commercial building. Quote SKU-102 and SKU-104 with 3 options.",
    "selected_sku_codes": ["SKU-102", "SKU-104"],
    "deterministic_totals_usd": {"option_a": 4850, "option_b": 7100, "option_c": 10300},
    "gross_margin_pct": 0.54
  }'
```

### Test 3: Urgent Red-Gate Escalation (`Should Mute Bot & Page #red-alerts Immediately`)
```bash
curl -X POST "https://hook.us1.make.com/YOUR_WEBHOOK_ID"   -H "Content-Type: application/json"   -d '{
    "event_id": "test_red_003",
    "ticket_channel": "support_email",
    "customer_email": "qa-test@yourcompany.com",
    "inbound_subject": "Unacceptable billing error - disputing charge",
    "inbound_body": "You charged my card twice and nobody called me back. Fix this today or I am filing a chargeback and leaving a 1 star Google review."
  }'
```

---

## 5. A2P 10DLC SMS Compliance & 60-Second Kill-Switch Drill
1. **Mandatory SMS Compliance Rules (US TCPA / A2P 10DLC, Canada CASL, UK/EU GDPR):**
   - Only send automated SMS messages to leads or customers where `sms_opt_in_verified == true` (via web form consent checkbox or inbound customer call/text).
   - Every initial outbound SMS must identify your business name clearly and honor native carrier `STOP` / `UNSUBSCRIBE` keywords immediately.
2. **Executing the 60-Second Kill-Switch Drill:**
   - Open `06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv`.
   - Click the direct scenario URL for any blueprint (`BP-01` through `BP-05`), toggle the master scenario switch **OFF**, and open the paired **Emergency Operations Script (`Scripts 01–12`)** from `03-AI-Prompt-and-SOP-Vault-62.csv`. Verify that any coordinator on your team can complete this fallback switch in under 60 seconds.

---

## 6. Blueprint-by-Blueprint Node Wiring & Field Mapping Walkthrough (`01` through `05`)

### 6.1 Blueprint 01 — `01-60s-instant-lead-router-and-sms-intake.json` (Department 01: Speed-to-Lead)
- **Trigger (`Node 01`):** Fires within `1–3 seconds` whenever a prospect submits your website inquiry form, clicks a Google Local Services / Meta Lead Ad, or hangs up after an unanswered inbound phone call (`OpenPhone` / `Twilio` `call.ringing.unanswered` webhook).
- **Rules & Pre-AI Filter (`Node 02`):** Normalizes `phone_raw` to strict `E.164` format (`+15125550194`), checks whether `event_id` has already been processed in the last 24 hours (idempotency guard), and runs the Pre-AI Emergency Regex (`gas leak|sparking|flooding|chest pain|bleeding|lawyer`). Any regex match bypasses AI booking and routes straight to `Branch_C_Red_Immediate_Human_Takeover`.
- **Truth-Table Lookup (`Node 03`):** Queries `Database 01 (Leads & Quotes Pipeline)` to detect returning customers and checks whether `postal_code` is inside your approved service territory list (`{{APPROVED_POSTAL_CODES}}`).
- **Grounded AI Compiler (`Node 04`):** Runs `Prompt 3.1 / 3.3` at `temperature: 0.0` in JSON Object mode to produce a `< 160 character` SMS reply with your live Calendly / Cal.com booking link, a multi-paragraph confirmation email, and a 4-bullet rep brief.
- **T-R-A-V Router (`Node 05`):**
  - **Green Branch (`80% of volume`):** Standard in-territory service/consultation inquiries (`Urgency 1–3`) dispatch the SMS and email immediately without waiting for human review.
  - **Amber Branch (`15% of volume`):** Commercial or multi-unit inquiries (`> $5,000` estimated value) send an instant polite acknowledgment to the prospect and post a 1-click Amber Approval Card to `#amber-approvals` so a senior rep can claim the account within 15 minutes.
  - **Red Branch (`5% of volume`):** Safety/clinical emergencies mute automated follow-up and page the on-duty manager in `#red-alerts`.

### 6.2 Blueprint 02 — `02-ai-support-triage-and-amber-approval-gate.json` (Department 03: Support Shield)
- **Trigger (`Node 01`):** Fires on every new inbound support email, website chat message, or customer SMS question.
- **Rules & Pre-AI Filter (`Node 02`):** Scrubs payment card numbers (`[REDACTED_CARD]`) and government IDs (`[REDACTED_GOV_ID]`), then checks the Red-Zone Legal/Chargeback Regex (`lawyer|attorney|chargeback|bbb|fraud|scam|injured|damage|furious|1 star`).
- **Truth-Table Lookup (`Node 03`):** Fetches the customer's live order/appointment status (`ORD-...`) and retrieves matching verified clauses from `05-Company-Knowledge-Base-and-SOP-Tracker.csv` (`Database 05`).
- **Grounded AI Compiler (`Node 04`):** Runs `Prompt 6.1 / 6.2` at `temperature: 0.0`. If the answer is explicitly present in `Database 05` (`kb_confidence >= 0.88`) and `sentiment_score >= 3` with `$0` financial concession, the ticket is marked `GREEN`. If the customer requests a one-time courtesy fee waiver (`<= $100`) or asks an unindexed question, the ticket is marked `AMBER`.
- **T-R-A-V Router (`Node 05`):** Auto-resolves `60%–70%` of routine Tier-1 inquiries (`WISMO`, rescheduling, policy FAQs) in under 45 seconds while routing Amber credit approvals to `#amber-support` and Red escalations to `#red-alerts` with **Emergency Script #07** pre-populated.

### 6.3 Blueprint 03 — `03-3option-instant-quote-and-14day-followup.json` (Department 02: Sales & Quoting)
- **Trigger (`Node 01`):** Fires when a field estimator or sales consultant submits a 90-second voice memo or mobile web form after completing a site visit or discovery call.
- **Deterministic Math Engine (`Node 03`):** Looks up the selected SKU codes (`SKU-101` through `SKU-112`) in `Sheet 4: 3-Option Quote Calculator` (`06-NOTION-TEMPLATES/Spreadsheets/sheet4-3option-quote-and-margin-calculator.csv`) and calculates exact dollar totals, labor hours, tax, and gross margin (`>= 42%` floor) in deterministic code **before** calling the LLM.
- **Grounded AI Compiler (`Node 04`):** Runs `Prompt 4.1 & 4.2` at `temperature: 0.1` to format the **Option A (Essential)**, **Option B (Recommended Most Popular)**, and **Option C (VIP Turnkey)** scope descriptions alongside the 6-touch, 14-day value-add follow-up sequence (`Day 1, Day 2, Day 4, Day 7, Day 10, Day 14`).
- **Amber Approval Gate (`Node 05`):** Posts the compiled 3-option quote preview to `#amber-approvals` in Slack. Once the estimator clicks **`[Approve & Dispatch Now]`**, the proposal PDF/link is emailed and texted to the prospect and the 14-day follow-up state machine begins—automatically halting within 3 seconds the moment the prospect signs or replies (`Prompt 4.4`).

### 6.4 Blueprint 04 — `04-overdue-invoice-5stage-payment-chaser.json` (Department 04: Finance & AR)
- **Trigger (`Node 01`):** Dual trigger—fires immediately on `job.completed` (Stage 0 Same-Day Invoice) and runs a daily `08:30 AM` scheduled poll of unpaid invoices in QuickBooks Online, Xero, FreshBooks, or Stripe.
- **Dispute & Freeze Verification (`Node 02 & Node 03`):** Cross-checks `Database 01` and your support inbox to verify that `open_support_dispute == false`. If a client has an active warranty or quality complaint (`open_support_dispute == true`), automated AR reminders are frozen immediately (`Emergency Script #10`) so the bot never chases a disputed bill.
- **5-Stage Polite-to-Firm Cadence (`Node 04 & Node 05`):**
  - `Stage 1 (Day -3 Pre-Due Courtesy)` -> **Green Gate** (Unattended Email)
  - `Stage 2 (Day +1 Helpful Link Resend)` -> **Green Gate** (Unattended Email + SMS)
  - `Stage 3 (Day +7 Account Coordinator Check-In)` -> **Green Gate** (Unattended Email + SMS)
  - `Stage 4 (Day +15 Formal Late Fee Warning)` -> **Amber Gate** (Requires 15-second manager approval click in `#amber-finance`)
  - `Stage 5 (Day +30 Service Pause & Final Demand)` -> **Red Gate** (Halts automation and briefs human finance lead for personal phone call)

### 6.5 Blueprint 05 — `05-friday-3pm-owner-kpi-executive-digest.json` (Department 05: Owner Command)
- **Trigger (`Node 01`):** Scheduled cron trigger firing every Friday at `15:00` (`3:00 PM`) local business time.
- **12-KPI Aggregation (`Node 03`):** Reads the weekly totals from `Database 01` through `Database 05` and `Sheet 2: 52-Week KPI Tracker` (`qualified_leads`, `speed_to_lead_sec`, `missed_call_recovery_pct`, `quotes_sent_under_15m_pct`, `14d_quote_close_pct`, `onboarding_cycle_hours`, `tier1_support_deflection_pct`, `new_5star_reviews`, `weekly_cash_collected_usd`, `overdue_ar_over_15d_usd`, `average_dso_days`, and `weekly_team_hours_saved`).
- **Executive Scorecard Compiler (`Node 04`):** Runs `Prompt 10.1 & 10.2` at `temperature: 0.1` to deliver a 1-page Executive Brief to the Owner's Slack DM and inbox containing:
  1. Red/Amber/Green status across all 12 KPIs,
  2. Top 3 Departmental Wins of the Week,
  3. The #1 Root-Cause Operational Bottleneck + 7-Day Corrective Action Plan, and
  4. A ready-to-read **Monday 8:45 AM 15-Minute All-Hands Team Agenda**.

---

## 7. Configuring Interactive Slack Block Kit 15-Second Amber Approval Cards
Each JSON blueprint includes a ready-to-use `slack_block_kit_approval_card_template` object. To wire interactive 1-click approvals (`[Approve & Dispatch Now]`, `[Edit Before Sending]`, `[Escalate to Red Gate]`) in Slack:
1. Create a free internal Slack App at `api.slack.com/apps` -> Enable **Incoming Webhooks** for `#amber-approvals`, `#amber-support`, `#amber-finance`, and `#red-alerts`.
2. In the **Interactivity & Shortcuts** tab of your Slack App, toggle **Interactivity `ON`** and paste the webhook URL of a lightweight Make.com / n8n **"Amber Action Listener"** scenario into the `Request URL` box.
3. When a manager taps **`[Approve & Dispatch Now]`** from their phone or desktop, Slack sends the `event_id` payload to your listener scenario, which immediately releases the held email/SMS and updates the row in `02-Automation-Workflows-and-Health-Registry.csv` from `Pending Amber` to `Approved & Sent` with the approver's timestamp.

---

## 8. Dead-Letter Queue (DLQ) Recovery & Monthly Governance Audit Checklist
- **Automated Retry & Dead-Letter Queue (`Node 06`):** Every external API call (OpenAI, Twilio, Gmail/M365, Notion, Stripe/QBO) is wrapped in a 3-attempt exponential backoff policy (`15s -> 60s -> 300s`). If an upstream provider experiences a sustained outage, `Node 06` writes the full raw JSON payload to your **Dead-Letter Queue** (`Database 02`) and alerts `#red-alerts` so zero customer inquiries are ever lost.
- **Monthly 15-Minute Governance Audit (First Monday of Every Month):**
  1. Review the previous 30 days of Amber-Gate edits in `#amber-approvals` and add any recurring corrections as permanent policy rows in `05-Company-Knowledge-Base-and-SOP-Tracker.csv` (`Prompt 10.3`).
  2. Verify that OpenAI / Anthropic monthly API spend remains within budget (`$12–$45/mo` typical for 1–50 employee businesses) and rotate any API keys older than 90 days.
  3. Run the three synthetic `curl` test cases (`test_green_001`, `test_amber_002`, `test_red_003`) to certify that all Green, Amber, and Red routing branches remain 100% operational.
