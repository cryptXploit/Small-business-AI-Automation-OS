# Worksheet 5: Customer Onboarding & Handoff Verification Checklist

**Companion to:** Chapter 5 — *Frictionless Customer Onboarding, Scheduling & Order Handoffs*  
**Framework Reference:** *The Zero-Drop Handoff Protocol (Stage 1 Payment Trigger -> Stage 2 Welcome Sequence -> Stage 3 Intake Verification & Chaser Loop -> Stage 4 AI Delivery Brief & Task Provisioning)*  
**Department Engine:** `Dept 03 — Customer Onboarding & Fulfillment Handoff`  
**Estimated Completion Time:** 45 Minutes  
**Interactive Companion:** Pre-configured inside the Notion Small Business OS (`06-NOTION-TEMPLATES/`) and the Pro Web App Suite (`07-INTERACTIVE-TOOLS/index.html` — Access Code: `SMALLBIZ-OS-PRO-2026`).

---

## Instructions for the Owner & Operations Lead

The most expensive operational breakdown in a small business occurs during the **post-deposit handoff gap**—the critical window between the moment a customer signs an agreement or pays an invoice (`Dept 02`) and the moment your fulfillment crew, clinical provider, or project team begins executing the work (`Dept 03`). When sales notes remain trapped inside scattered phone transcripts, email threads, or a salesperson's memory, your delivery team starts blind, customers experience post-purchase silence, and field technicians or designers waste billable hours on preventable rework.

Use this 5-part operational workbook to standardize your **Sales-to-Fulfillment Data Contract**, configure your **Instant Welcome Packet**, automate your **Day 1 / Day 3 / Day 5 Missing-Asset Chaser Loop**, deploy the **AI-Compiled Internal Staff Delivery Brief**, and track your **First-7-Day Onboarding Service-Level Agreement (SLA)**.

---

## Part 1: Sales-to-Fulfillment Required Data Contract Table

Before a deal in your CRM is permitted to move from `Closed-Won / Deposit Paid` to `Scheduled for Kickoff / Dispatch`, every mandatory field in the **Sales-to-Fulfillment Data Contract** must be populated and validated. Define your non-negotiable intake fields across your primary service lines below.

### 1.1 Universal Deal & Billing Verification Fields (Stage 1 Webhook Gate)

| Field ID | Data Contract Field Name | Source System (Stripe / QBO / CRM / E-Sign) | Validation Rule (Deterministic Check) | Fallback Action if Missing |
| :--- | :--- | :--- | :--- | :--- |
| `ONB-01` | **Verified Payment Event ID** | `[ ] Stripe [ ] Square [ ] QBO [ ] Xero` | `payment_status == "paid"` AND `amount_paid >= required_deposit` | Hold onboarding; alert billing channel `#finance-alerts` |
| `ONB-02` | **Countersigned Proposal / SOW URL** | `[ ] PandaDoc [ ] DocuSign [ ] HighLevel` | Signed PDF URL returns HTTP `200 OK` and non-empty file size | Re-send signature link automatically via SMS/email |
| `ONB-03` | **Selected Package Tier** | `[ ] Core [ ] Pro [ ] Complete` | Exact match against approved SKU code in Pricebook | Flag account manager in `#onboarding-exceptions` |
| `ONB-04` | **Primary Decision-Maker Contact** | CRM Contact Record | Valid mobile E.164 phone + deliverable email address | Prompt sales rep to complete contact record |
| `ONB-05` | **On-Site / Day-of-Service Contact** | Intake Form / CRM Record | Name, mobile number, and role (if different from payer) | Request inside Stage 2 Welcome Intake Form |
| `ONB-06` | **Promised Delivery / Target Window** | Signed SOW / Estimate Record | Valid ISO date (`YYYY-MM-DD`) >= `today + minimum_lead_time_days` | Flag scheduling conflict before confirming slot |

### 1.2 Vertical-Specific Prerequisite & Asset Checklist (Stage 3 Gate A)

Complete the row that matches your business model and add your custom technical prerequisites:

| Business Archetype | Mandatory Customer Assets / Photos / Prerequisites Required Before Dispatch or Kickoff | File / Data Validation Criteria (Checked by `Prompt 5.3`) | Who Reviews Amber Flags? |
| :--- | :--- | :--- | :--- |
| **Home & Field Services** *(HVAC, Plumbing, Electrical, Solar, Remodeling, Landscaping)* | 1. Wide-angle photo of existing unit/panel/install area<br>2. Close-up photo of manufacturer model/serial plate<br>3. Gate/lockbox access code & pet containment confirmation<br>4. HOA or municipal permit approval (if required) | Minimum `1080p` image resolution; serial plate legible via OCR; gate code populated (`!= "N/A"`) | Dispatch Coordinator: `___________________` |
| **B2B Agencies & Professional Studios** *(Web, Marketing, Accounting, Legal, IT/MSP)* | 1. Completed brand/technical questionnaire<br>2. High-resolution vector logo (`.svg` or `.eps`) & brand guide<br>3. Verified admin/delegated access to DNS, CMS, Ad Accounts, or Books<br>4. Approved point-of-contact for weekly milestone sign-offs | Access tokens verified active; vector file format confirmed; questionnaire `100%` of required fields answered | Account Manager: `___________________` |
| **Clinical, Medical, Dental & Wellness Practices** | 1. Completed HIPAA/privacy consent & medical history form<br>2. Front and back photos of active insurance card + photo ID<br>3. Prior imaging/records release or current medication list<br>4. Signed financial responsibility & cancellation policy | Insurance member ID & group number legible; consent signature timestamped; zero blank mandatory health screening questions | Patient Coordinator: `___________________` |
| **Custom Retail, Manufacturing & Specialty E-Commerce** | 1. Exact measurements / sizing specification sheet<br>2. Custom artwork / engraving proof sign-off<br>3. Commercial loading-dock or residential delivery window confirmation<br>4. Tax-exempt resale certificate (for wholesale buyers) | Proof approval checkbox = `TRUE`; dimensions within machine tolerances (`min/max` bounds) | Fulfillment Lead: `___________________` |
| **Your Custom Prerequisite #1:** | `_______________________________________________________` | `_______________________________________________________` | Owner/Lead: `___________________` |
| **Your Custom Prerequisite #2:** | `_______________________________________________________` | `_______________________________________________________` | Owner/Lead: `___________________` |

---

## Part 2: Customer Welcome Packet & Expectation-Setting Checklist (`Prompt 5.2`)

Within **60 seconds** of payment confirmation, Stage 2 of the Zero-Drop Handoff Protocol dispatches a personalized Welcome Email and concise SMS confirmation. Audit your Welcome Packet against the 10 mandatory trust elements below:

- [ ] **Element 1 — Immediate Gratitude & Deposit Receipt Confirmation:** Explicitly confirms the exact dollar amount received (`$________`) and the package tier selected (`Core / Pro / Complete`) so the customer knows their transaction succeeded.
- [ ] **Element 2 — Named Human Point of Contact:** Introduces the specific Project Manager, Field Supervisor, or Care Coordinator (`Name: ____________________`, `Direct Role: ____________________`) so the customer never feels handed off to a faceless queue.
- [ ] **Element 3 — The "What Happens Next" 3-Step Visual Timeline:** Lists the exact chronological milestones (e.g., *Step 1: Complete 4-Minute Intake Form within 24 Hours -> Step 2: Technical Spec Verification & Calendar Release -> Step 3: Kickoff / Installation Day*).
- [ ] **Element 4 — Single Pre-Filled Dynamic Intake Link:** Provides a one-click URL (`https://____________________________________`) with the customer's name, email, phone, and package ID already pre-populated via URL query parameters (`?deal_id={{deal_id}}&email={{email}}`).
- [ ] **Element 5 — Exact Time Estimate for Intake Completion:** States clearly how long the intake takes (e.g., *"Takes 4 minutes on your phone"*) and why completing it immediately protects their target delivery date.
- [ ] **Element 6 — Communication Boundaries & SLA Rules:** Defines your normal response window (e.g., *"Same-day response for all messages received between 8:00 AM and 5:00 PM"*), official communication channels, and emergency contact rules.
- [ ] **Element 7 — Scope-Protection Reminder:** Gently reinforces what is included in their selected tier and how optional add-ons or change requests are handled transparently.
- [ ] **Element 8 — Automated Client Folder / Portal Provisioning:** Automatically creates a dedicated Google Drive, SharePoint, Notion, or Client Portal folder (`[Client Name] - [Deal ID] - Onboarding`) and logs the folder URL back into the CRM deal record.
- [ ] **Element 9 — Stop-Logic on Sales Nurture Sequences:** Immediately removes the customer from all open-quote chasers (`Chapter 4`) so they never receive an embarrassing *"Still thinking about your quote?"* text after paying.
- [ ] **Element 10 — Companion SMS Notification:** Sends a short, high-deliverability SMS within 60 seconds of payment:  
  > *"Hi {{first_name}}, thank you! Your deposit for {{package_name}} at {{company_name}} is confirmed. We just emailed your Welcome Packet & 4-minute setup link to {{email}}. Complete that today to lock in your kickoff slot! — {{coordinator_name}}"*

---

## Part 3: Automated Missing-Asset Chaser Schedule (`Prompt 5.3`)

Never allow a highly paid technician, clinician, designer, or account manager to spend hours manually chasing clients for missing photos, forms, or logins. Configure your automated **3-Touch Missing-Asset Chaser Loop** below. The automation runs `Prompt 5.3` every time an intake form is partially submitted or remains incomplete after 24 hours.

### 3.1 Chaser Timing, Channel & Escalation Matrix

| Chaser Stage | Trigger Timing & Condition | Delivery Channel | Core Message Angle (`Prompt 5.3` Dynamic Output) | Stop Condition | Escalation Action if Unresolved |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Touch 1: Helpful Specificity** | **+24 Hours** post-deposit if `intake_completeness_score < 100%` | **SMS + Email** *(8:00 AM–8:00 PM Local)* | Thanks client for completed items (`{{completed_items}}`), lists the exact 1–2 missing/blurry items (`{{missing_items}}`), and provides direct mobile upload link. | Stops immediately when `completeness == 100%` | Logs `Chaser_1_Sent` in CRM |
| **Touch 2: Timeline Protection** | **+72 Hours (Day 3)** post-deposit if still `< 100%` | **Email + SMS** | Explains how providing the remaining item (`{{missing_items}}`) today keeps their target kickoff/installation date (`{{target_date}}`) on schedule; offers 1-reply help if stuck. | Stops immediately when `completeness == 100%` | Updates deal status to `Onboarding - Awaiting Client Assets` |
| **Touch 3: Provisional Hold Warning** | **+120 Hours (Day 5)** post-deposit if still `< 100%` | **Email + Priority Staff Task** | Polite notice that their provisional calendar slot is held for 24 more hours pending `{{missing_items}}`; creates a 5-minute phone walkthrough task for the coordinator. | Stops immediately when `completeness == 100%` | Posts Amber Alert in `#onboarding-ops` for human call |

### 3.2 Pre-Appointment / Pre-Installation Readiness Sequence (`Prompt 5.4`)

Once `intake_completeness_score == 100%` and the calendar slot is confirmed, configure your automated no-show and site-readiness reminders:

| Reminder Window | Channel | Required Customer Action / Readiness Verification | Configured in Tool? |
| :--- | :--- | :--- | :--- |
| **72 Hours Prior** | Email + SMS | Site/meeting preparation checklist (clear workspace, pet containment, decision-maker attendance, required materials ready) | `[ ] Yes [ ] No` |
| **24 Hours Prior** | SMS (Interactive) | *"Reply `1` to Confirm or `2` to Reschedule"* — `1` marks appointment `Confirmed` in CRM; `2` triggers Amber Alert to backfill the slot | `[ ] Yes [ ] No` |
| **2 Hours Prior** | SMS | Technician En-Route GPS link + photo bio OR Virtual Kickoff Zoom/Meet URL + 3-bullet agenda | `[ ] Yes [ ] No` |

---

## Part 4: Internal Staff Delivery Brief Template (`Prompt 5.1` & `Prompt 5.5`)

Your fulfillment team should never have to read a 40-message sales email chain or listen to a 30-minute discovery call recording to figure out what was sold. Configure your automation bridge (Make / Zapier / n8n) to pass the **Signed SOW + Sales Discovery Notes + Validated Customer Intake Data** into `Prompt 5.1` and `Prompt 5.5`, generating the standardized **1-Page Internal Staff Delivery Brief** below.

```markdown
================================================================================
INTERNAL STAFF DELIVERY BRIEF — ZERO-DROP HANDOFF PACKET
Generated Automatically via Dept 03 Onboarding Engine | Deal ID: {{deal_id}}
================================================================================

1. CLIENT & PROJECT SNAPSHOT
   - Client / Account Name:      {{client_name}} ({{company_name}})
   - Selected Package Tier:      {{package_tier}} (Total Value: {{contract_value}})
   - Deposit Verified:           {{deposit_amount}} (Paid via {{payment_method}} on {{paid_at}})
   - Assigned Fulfillment Lead:  {{assigned_lead_name}}
   - Target Kickoff / Dispatch:  {{scheduled_kickoff_datetime}}
   - Client Assets Folder URL:   {{cloud_folder_url}}

2. PRIMARY OBJECTIVE & DEFINITION OF DONE (IN PLAIN ENGLISH)
   - Core Customer Goal:         {{synthesized_primary_goal}}
   - Quantitative Success Metric:{{success_criteria_metric}}
   - Must-Have Deliverables:
     [ ] 1. {{deliverable_1}} (Spec: {{deliverable_1_spec}})
     [ ] 2. {{deliverable_2}} (Spec: {{deliverable_2_spec}})
     [ ] 3. {{deliverable_3}} (Spec: {{deliverable_3_spec}})

3. VERIFIED TECHNICAL SPECS, ACCESS & SITE LOGISTICS (FROM GATE A)
   - Equipment / Environment:    {{verified_equipment_or_tech_stack}}
   - Uploaded Photos / Files:    {{verified_asset_links_and_ocr_notes}}
   - Site Access / Constraints:  {{parking_gate_pets_or_login_notes}}
   - On-Site / Day-Of Contact:   {{onsite_contact_name}} ({{onsite_contact_phone}})

4. CUSTOMER PREFERENCES, SENSITIVITIES & SALES PROMISES
   - Explicit Sales Commitments: {{special_promises_from_sales_notes}}
   - Communication Preference:   {{preferred_channel_and_cadence}}
   - Known Sensitivities:        {{past_bad_experiences_or_concerns}}

5. SCOPE-BOUNDARY & CHANGE-ORDER WATCHLIST (PROMPT 5.5 AUDIT)
   - Explicit SOW Exclusions:    {{explicitly_excluded_items}}
   - Detected Scope-Drift Risk:  {{amber_flag_unquoted_client_requests}}
   - Pre-Calculated Change Order:{{recommended_upsell_or_change_order_amount}}

6. AUTO-PROVISIONED TASK BOARD CHECKLIST
   - Task Board Link:            {{asana_clickup_jobber_board_url}}
   - Milestone 1 Due Date:       {{milestone_1_date}}
   - Final QA Sign-Off Date:     {{final_qa_date}}
================================================================================
```

---

## Part 5: First-7-Day Onboarding SLA & Bottleneck Tracker

Review these five onboarding metrics every Friday during your 15-Minute Owner Scorecard review (`Chapter 10`). Track your baseline performance before automation alongside your Week 4 and Week 8 automated performance.

| Metric ID | Onboarding KPI Name | Formula / Measurement Definition | Baseline (Manual) | Target Benchmark (Automated OS) | Week 4 Actual | Week 8 Actual |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `KPI-5.1` | **Payment-to-Welcome Latency** | Median seconds from `invoice.paid` webhook to Welcome Packet + SMS delivery | `______ hrs` | **`< 60 seconds`** | `______ sec` | `______ sec` |
| `KPI-5.2` | **48-Hour Intake Completion Rate** | `%` of new customers who submit `100%` of required assets within 48 hours of deposit | `______ %` | **`>= 85.0%`** | `______ %` | `______ %` |
| `KPI-5.3` | **Payment-to-Kickoff Cycle Time** | Average hours from deposit payment to verified, ready-to-execute kickoff/dispatch | `______ days` | **`< 36 hours`** | `______ hrs` | `______ hrs` |
| `KPI-5.4` | **First-Time Spec Accuracy Rate** | `%` of jobs/projects that require zero mid-job delays due to missing specs or wrong parts | `______ %` | **`>= 96.0%`** | `______ %` | `______ %` |
| `KPI-5.5` | **Appointment / Kickoff No-Show Rate** | `%` of scheduled kickoffs or field visits missed or cancelled within `< 24 hours` | `______ %` | **`<= 3.5%`** | `______ %` | `______ %` |

### Owner Sign-Off & Deployment Verification

- **Webhook Trigger Connected (`Stripe / Square / QBO / E-Sign`):** `[ ] Verified Live`
- **Dynamic Intake Form & Cloud Folder Provisioning Tested:** `[ ] Verified Live`
- **Prompts `5.1` through `5.5` Deployed with JSON Schema Validation:** `[ ] Verified Live`
- **Sign-Off Date:** `____ / ____ / 2026` | **Owner / Ops Lead Signature:** `___________________________`
