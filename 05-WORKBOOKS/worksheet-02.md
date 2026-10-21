# Worksheet 2: Workflow Risk & Automation Readiness Scorecard

**Companion To:** Chapter 2 — *The "Human-in-the-Loop" Architecture: Designing Safe, Zero-Hallucination Workflows*  
**Document Code:** `WB-CH02-TRAV-V1`  
**Target Completion Time:** 30 Minutes per Department Rollout  
**Applicable Team Size:** Solo Operator to 25-Person Small Business  

---

## Executive Instructions: Enforcing the T.R.A.V. Gate Before Any Workflow Goes Live

The single greatest risk in small business automation is connecting a raw language model directly to a live customer communication channel without deterministic rules, grounding tables, and human verification boundaries. A single hallucinated discount, invented clinical instruction, or double-fired webhook can destroy years of local reputation in thirty seconds.

Every automated workflow in your company must pass through **The T.R.A.V. Safety Architecture** documented on this scorecard before switching from `Sandbox Test Mode` to `Live Production Mode`:

1. **`[T]` Trigger Standardization:** Deduplicate webhooks using an idempotency hash (`event_hash`), normalize phone numbers (`E.164`), validate timestamps (`ISO-8601`), and reject malformed payloads before calling any AI endpoint.
2. **`[R]` Rules & Deterministic Context Grounding:** Run hard-coded filters (blocklists, business hours, numeric margin floors, regex keyword triggers) *before* AI inference, and inject only verified company pricing tables and approved SOP snippets (`temperature: 0.0–0.2`).
3. **`[A]` AI Processing with Strict JSON Schema Enforcement:** Require the model to output a structured JSON payload containing `confidence_score`, `risk_tier`, `policy_check_passed`, `draft_response`, and `escalation_reason`.
4. **`[V]` Verification & 3-Zone Routing Gate:** Route every output deterministically into **Green Zone** (`Auto-Execute`), **Amber Zone** (`One-Click Staff Approval Card`), or **Red Zone** (`Immediate Human Takeover`), backed by a **Dead-Letter Fallback Queue**.

---

## Part A: The 3-Zone Risk Classification Matrix (15 Common SMB Workflows + Your Custom Rows)

### A.1 Reference Benchmark: How to Score Risk Across 15 Standard Small Business Workflows

Every workflow is evaluated across four risk factors on a `1–5` scale (`1 = Minimal Risk`, `5 = Severe Exposure`), producing a **Total Risk Score (`4–20 Points`)**:
* **Factor 1 — Financial Exposure (`1–5`):** Does the action commit pricing, discounts, refunds, or vendor payments? (`1 = $0 commitment`; `3 = Standard fixed-price SKU <$500`; `5 = Custom quote >$1,000, refund, or contract pricing`).
* **Factor 2 — Legal, Clinical & Regulatory Liability (`1–5`):** Could an error violate medical privacy, legal ethics, safety codes, or A2P SMS consent? (`1 = Internal operational note`; `3 = Standard customer scheduling`; `5 = Medical/legal advice, contract terms, or dispute`).
* **Factor 3 — Reputational & Brand Sensitivity (`1–5`):** What happens if the tone is slightly off? (`1 = Internal staff checklist`; `3 = Routine prospect intake`; `5 = Angry customer complaint, 1-star review threat, or VIP partner`).
* **Factor 4 — Input Ambiguity (`1–5`):** How structured is the incoming data? (`1 = Fixed web form dropdowns`; `3 = Short SMS inquiry`; `5 = Multi-page unstructured custom RFP or emotional email`).

**Deterministic Routing Thresholds:**
* **Total Risk Score `4–8` (and Financial Exposure `<= 2`):** **GREEN ZONE** (`100% Unattended Auto-Execution`).
* **Total Risk Score `9–14` (or Financial Exposure `3–4`):** **AMBER ZONE** (`AI Drafts 95% -> 1-Click Slack/SMS/Email Human Approval`).
* **Total Risk Score `15–20` (or Any Single Factor `== 5` on Legal/Dispute):** **RED ZONE** (`Lock Automated Reply -> Immediate Human Takeover Alert`).

| Ref # | Standard Small Business Workflow | Dept | Fin. (`1–5`) | Legal (`1–5`) | Brand (`1–5`) | Input (`1–5`) | Total Risk (`/20`) | Assigned T.R.A.V. Zone | Required Approval Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BM-01` | Missed-Call 60-Second SMS Intake Concierge | `01` | `1` | `1` | `2` | `2` | **`6 / 20`** | **GREEN ZONE** | Auto-Execute (A2P Opt-In Verified) |
| `BM-02` | Website Contact Form CRM Normalization & Dedup | `01` | `1` | `1` | `1` | `1` | **`4 / 20`** | **GREEN ZONE** | Auto-Execute (Internal DB Write) |
| `BM-03` | Standard Fixed-Fee Inspection / Consult Booking | `01` | `2` | `1` | `2` | `2` | **`7 / 20`** | **GREEN ZONE** | Auto-Execute (Calendar Buffer Locked) |
| `BM-04` | Custom 3-Tier Proposal / Estimate Generation | `02` | `4` | `3` | `3` | `3` | **`13 / 20`** | **AMBER ZONE** | 1-Click Owner/Estimator Slack Card |
| `BM-05` | 14-Day Pre-Approved Quote Follow-Up Sequence | `02` | `1` | `1` | `2` | `1` | **`5 / 20`** | **GREEN ZONE** | Auto-Execute (With Stop-on-Reply Hook) |
| `BM-06` | Prospect Price Objection & Scope Reduction Re-Quote | `02` | `4` | `2` | `3` | `4` | **`13 / 20`** | **AMBER ZONE** | 1-Click Approval of Revised Tier-1 Scope |
| `BM-07` | Signed Quote to Client Folder & Task Board Setup | `03` | `1` | `1` | `1` | `1` | **`4 / 20`** | **GREEN ZONE** | Auto-Execute (Internal Provisioning) |
| `BM-08` | Tier-1 FAQ Reply (Hours, Address, Parking, Status) | `03` | `1` | `1` | `2` | `2` | **`6 / 20`** | **GREEN ZONE** | Auto-Execute (`Confidence >= 0.90`) |
| `BM-09` | Customer Refund, Credit Memo, or Warranty Claim | `03` | `4` | `3` | `4` | `3` | **`14 / 20`** | **AMBER ZONE** | Manager 1-Click Approval (`<$250` cap) |
| `BM-10` | Angry Customer Threatening Chargeback / Lawsuit | `03` | `5` | `5` | `5` | `4` | **`19 / 20`** | **RED ZONE** | Halt Bot -> Instant Owner Phone/Slack Alert |
| `BM-11` | Post-Service Sentiment Check & 5-Star Review Ask | `03` | `1` | `1` | `2` | `1` | **`5 / 20`** | **GREEN ZONE** | Auto-Execute (Sub-4-Star Routes to Amber) |
| `BM-12` | Completed Milestone to Draft Invoice Line Items | `04` | `3` | `2` | `2` | `2` | **`9 / 20`** | **AMBER ZONE** | Bookkeeper/Owner 1-Click Batch Approve |
| `BM-13` | Standard Overdue Invoice Reminders (Day -3 to +14) | `04` | `2` | `1` | `2` | `1` | **`6 / 20`** | **GREEN ZONE** | Auto-Execute (Verified Unpaid Balance) |
| `BM-14` | Vendor PDF Invoice OCR Extraction to Staging Table | `04` | `2` | `2` | `1` | `2` | **`7 / 20`** | **GREEN ZONE** | Auto-Stage as `Draft Bill` (Human Pays) |
| `BM-15` | 5-Min Voice Memo to Internal Team SOP & Friday KPI | `05` | `1` | `1` | `1` | `2` | **`5 / 20`** | **GREEN ZONE** | Auto-Execute (Internal Workspace Only) |

---

### A.2 Your Custom Workflow Risk Scoring Grid

Score the specific workflows you selected in `Worksheet 1` before building them:

| Row # | Your Custom Workflow Name | Dept (`01–05`) | Fin. (`1–5`) | Legal (`1–5`) | Brand (`1–5`) | Input (`1–5`) | Total Score (`/20`) | Assigned Zone (`Green`/`Amber`/`Red`) | Designated Human Approver (If Amber/Red) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CW-01` | `[CUSTOM_WORKFLOW_NAME_01]` | `[D_01]` | `[F_01]` | `[L_01]` | `[B_01]` | `[I_01]` | **`[TOT_01]/20`** | `[ZONE_01]` | `[APPROVER_ROLE_01]` |
| `CW-02` | `[CUSTOM_WORKFLOW_NAME_02]` | `[D_02]` | `[F_02]` | `[L_02]` | `[B_02]` | `[I_02]` | **`[TOT_02]/20`** | `[ZONE_02]` | `[APPROVER_ROLE_02]` |
| `CW-03` | `[CUSTOM_WORKFLOW_NAME_03]` | `[D_03]` | `[F_03]` | `[L_03]` | `[B_03]` | `[I_03]` | **`[TOT_03]/20`** | `[ZONE_03]` | `[APPROVER_ROLE_03]` |
| `CW-04` | `[CUSTOM_WORKFLOW_NAME_04]` | `[D_04]` | `[F_04]` | `[L_04]` | `[B_04]` | `[I_04]` | **`[TOT_04]/20`** | `[ZONE_04]` | `[APPROVER_ROLE_04]` |
| `CW-05` | `[CUSTOM_WORKFLOW_NAME_05]` | `[D_05]` | `[F_05]` | `[L_05]` | `[B_05]` | `[I_05]` | **`[TOT_05]/20`** | `[ZONE_05]` | `[APPROVER_ROLE_05]` |
| `CW-06` | `[CUSTOM_WORKFLOW_NAME_06]` | `[D_06]` | `[F_06]` | `[L_06]` | `[B_06]` | `[I_06]` | **`[TOT_06]/20`** | `[ZONE_06]` | `[APPROVER_ROLE_06]` |
| `CW-07` | `[CUSTOM_WORKFLOW_NAME_07]` | `[D_07]` | `[F_07]` | `[L_07]` | `[B_07]` | `[I_07]` | **`[TOT_07]/20`** | `[ZONE_07]` | `[APPROVER_ROLE_07]` |
| `CW-08` | `[CUSTOM_WORKFLOW_NAME_08]` | `[D_08]` | `[F_08]` | `[L_08]` | `[B_08]` | `[I_08]` | **`[TOT_08]/20`** | `[ZONE_08]` | `[APPROVER_ROLE_08]` |

---

## Part B: The T.R.A.V. Gate Architecture Design Canvas

Complete one design canvas below for each of your **Top 3 Sprint-1 Workflows** before activating live customer webhooks:

| T.R.A.V. Architectural Layer | Specification Question | Your Production Configuration |
| :--- | :--- | :--- |
| **Workflow Header** | **Workflow ID & Name:** | `[WORKFLOW_ID_AND_NAME]` |
| **1. `[T]` Trigger Standardization** | **Source Webhook / App Trigger:** | `[SOURCE_WEBHOOK_APP]` |
| **1. `[T]` Idempotency Key Formula** | How do we block duplicate webhooks within 60 seconds? | `SHA256([CONTACT_PHONE_OR_EMAIL] + [EVENT_TYPE] + [MINUTE_BUCKET])` |
| **1. `[T]` Required Non-Null Fields** | Which fields must exist before proceeding? | `[REQUIRED_FIELDS_LIST]` *(e.g., `phone_e164` OR `email`, `timestamp_utc`)* |
| **2. `[R]` Deterministic Pre-Filters** | What code/regex filter runs *before* the AI prompt? | `[PRE_FILTER_RULES]` *(e.g., block `noreply@`, check Red-Zone keywords)* |
| **2. `[R]` Red-Zone Trigger Keywords** | Which exact words force an immediate Red-Zone stop? | `lawyer, attorney, lawsuit, sue, BBB, fraud, chargeback, emergency, injury, bleeding, gas leak, fire` |
| **2. `[R]` Grounded Reference Table** | Which exact pricebook or SOP table is injected? | `[GROUNDED_SOURCE_TABLE_ID]` |
| **2. `[R]` Model Temperature Setting** | What temperature is enforced on the API call? | `0.1` *(Strict factual determinism; never exceed `0.2`)* |
| **3. `[A]` Required JSON Output Keys** | Which JSON keys must the AI return? | `confidence_score`, `risk_tier`, `policy_check_passed`, `draft_response`, `escalation_reason` |
| **3. `[A]` Negative Prompt Guardrails** | What is the AI strictly forbidden from stating? | `Never invent discounts, never quote off-menu SKUs, never promise exact arrival times without calendar check, never give legal/medical advice.` |
| **4. `[V]` Green-Zone Auto Threshold** | When does this run 100% unattended? | `risk_tier == "GREEN" AND confidence_score >= 0.90 AND policy_check_passed == true` |
| **4. `[V]` Amber-Gate Channel & SLA** | Where does the 1-click approval card go, and what is the timeout? | Channel: `[SLACK_OR_SMS_CHANNEL]` \| Escalation if unapproved after: `[TIMEOUT_MINS]` mins |
| **4. `[V]` Dead-Letter Fallback Action** | What happens if the LLM API times out or returns invalid JSON? | Route payload to `[DEAD_LETTER_SHEET_OR_TABLE]`, send static safe acknowledgement, and alert `[OPS_LEAD_CONTACT]`. |

---

## Part C: Deterministic Pre-Flight Validator & Grounding Checklist

Before any AI-generated draft is sent to a customer (in Green Zone) or presented to staff (in Amber Zone), verify that your automation bridge enforces these **8 Pre-Flight Code Checks**:

- [ ] **Check 1 — Valid JSON Parse:** Does the automation bridge wrap the AI response in a JSON parser node with an error-routing branch to the Dead-Letter Queue?
- [ ] **Check 2 — Numeric Price & Discount Bounds:** If the workflow outputs a dollar amount, does a deterministic formula node verify that `quoted_total >= minimum_pricebook_floor` and `discount_pct <= max_allowed_discount` (`Prompt 2.4`)?
- [ ] **Check 3 — Competitor & Forbidden Word Filter:** Does a regex filter verify that the outbound draft contains zero competitor brand names, zero internal markup percentages, and zero banned AI clichés?
- [ ] **Check 4 — Placeholder Leakage Filter:** Does a regex filter (`\[[A-Z0-9_]+\]|\{\{.*?\}\}`) verify that no unreplaced template brackets (such as `Hi [FIRST_NAME]`) ever reach a customer?
- [ ] **Check 5 — Active Customer / Open Dispute Suppression:** For sales and follow-up sequences, does the workflow check CRM status to confirm the contact does not have an open support escalation or unpaid 60-day dispute?
- [ ] **Check 6 — Quiet Hours & Time-Zone Enforcement:** For non-inbound follow-up SMS messages, does the router verify that the recipient's local time is between **8:00 AM and 8:00 PM**?
- [ ] **Check 7 — Confidence Score Floor (`>= 0.90`):** Does any response with `confidence_score < 0.90` automatically downgrade from Green Zone to Amber Zone for human inspection?
- [ ] **Check 8 — Immutable Audit Log Write:** Does the final step write `event_id`, `timestamp_utc`, `input_summary`, `ai_json_output`, `risk_zone`, `approved_by`, and `execution_status` to your central Audit Log table?

---

## Part D: Fallback Queue, Dead-Letter Alert & Emergency Kill-Switch Protocol Log

Every resilient small business automation system includes a clear **Emergency Kill-Switch** so any front-desk coordinator or manager can pause an automation in under 10 seconds if a third-party software outage occurs.

### D.1 Active Workflow Kill-Switch & Fallback Directory

Fill in the operational directory below and pin a printed copy at the front desk and inside your Notion SOP Vault:

| Workflow ID & Name | Automation Bridge Scenario URL / ID | Single-Record Pause Toggle (CRM Field) | Global Kill-Switch Location | Static Fallback Message Sent During Outage | Accountable Owner & Backup Contact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`WF-01`: 60s Lead Concierge** | `[SCENARIO_URL_01]` | Set Contact `bot_pause = TRUE` | Toggle Scenario `OFF` in Make/Zapier | *"Thanks for reaching out to `[BUSINESS_NAME]`! We received your inquiry and our team will text/call you shortly."* | `[OWNER_01]` / `[BACKUP_01]` |
| **`WF-02`: 3-Tier Quote Builder** | `[SCENARIO_URL_02]` | Set Deal `auto_quote = FALSE` | Toggle Scenario `OFF` in Make/Zapier | Hold in Draft Queue; notify estimator in `#quotes-amber-gate`. | `[OWNER_02]` / `[BACKUP_02]` |
| **`WF-03`: 14-Day Quote Nurture** | `[SCENARIO_URL_03]` | Set Deal `nurture_status = PAUSED` | Toggle Scenario `OFF` in Make/Zapier | Pause scheduled touches; log status in CRM deal timeline. | `[OWNER_03]` / `[BACKUP_03]` |
| **`WF-04`: Tier-1 Support Shield** | `[SCENARIO_URL_04]` | Tag Ticket `human_takeover` | Toggle Scenario `OFF` in Make/Zapier | *"We have logged your support request (Ticket `#[ID]`) and a specialist is reviewing it now."* | `[OWNER_04]` / `[BACKUP_04]` |
| **`WF-05`: Overdue AR Chaser** | `[SCENARIO_URL_05]` | Set Invoice `pause_reminders = TRUE` | Toggle Scenario `OFF` in Make/Zapier | Hold automated reminder; flag invoice on Friday AR Exception Report. | `[OWNER_05]` / `[BACKUP_05]` |

---

## Part E: Chapter 2 Safety Readiness Sign-Off

| Governance Verification Metric | Target Studio Standard | Your Current Status | Verified Date |
| :--- | :--- | :--- | :--- |
| **1. % of Live Workflows Mapped to Green/Amber/Red Zones** | `100%` | `[YOUR_ZONE_PCT]%` | `[DATE_01]` |
| **2. LLM API Temperature Across All Operational Prompts** | `0.0 to 0.2 Max` | `[YOUR_TEMP_SETTING]` | `[DATE_02]` |
| **3. Pre-Flight Placeholder & Price-Bound Regex Active** | `Active on 100% of Customer Outputs` | `[YOUR_REGEX_STATUS]` | `[DATE_03]` |
| **4. Dead-Letter Queue & Staff Alert Channel Tested** | `Simulated Failure Verified` | `[YOUR_DLQ_STATUS]` | `[DATE_04]` |

**Safety Architecture Approved By:** `[OWNER_OR_COMPLIANCE_LEAD]`  
**Business Name:** `[BUSINESS_NAME]`  
**Sign-Off Date:** `[SIGN_OFF_DATE]`  
