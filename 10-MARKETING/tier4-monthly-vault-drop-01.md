# Tier 4 Living Automation Vault — Monthly Drop #01: The 4-Industry Vertical Automation Pack

**Vault Release ID:** `VAULT-DROP-2026-01` (`10-MARKETING/tier4-monthly-vault-drop-01.md`)  
**Included In:** Tier 4 Living Automation Vault Membership (`$12/mo` or `$59/yr`)  
**Verticals Covered:** (1) Medical, Dental, PT & Wellness Clinics, (2) HVAC, Plumbing, Electrical, Roofing & Home Services, (3) Omni-Channel E-Commerce & Specialty Retail, and (4) B2B Agencies, CPA/Accounting Firms, Legal & Consultancies  
**Specialized Prompts Included:** `8 Deterministic Vertical Prompts` (`Vault Prompt V1.1` through `Vault Prompt V4.2`)  

---

## Executive Overview: How to Layer Vertical Playbooks Over Your Core 5-Department OS

Chapters 1 through 10 of *The Small Business AI Automation Operating System* provide the universal 5-Department backbone (`Prompts 1.1`–`10.5`). **Monthly Vault Drop #01** layers industry-specific data schemas, regulatory guardrails (HIPAA/PIPEDA/GDPR non-clinical boundaries, A2P 10DLC trade dispatch rules, e-commerce RMA fraud checks, and B2B scope governance), and **8 specialized JSON prompt contracts** directly on top of your existing Make.com, n8n, or Zapier routers.

---

## Vertical 1: Local Medical, Dental, Physical Therapy & Wellness Clinics

### 1.1 Vertical Operational Architecture & Privacy Guardrails
1. **Strict Non-Clinical Epistemic Boundary (HIPAA / PIPEDA / Privacy Compliance):**
   - Standard commercial SMS and email channels are non-encrypted transport layers. Consequently, your front-desk speed-to-lead and recall automations must enforce a **Zero-Diagnosis / Zero-PHI-over-SMS Rule**:
   - The automation never diagnoses symptoms, never recommends medications, and never repeats sensitive clinical conditions inside an outbound SMS text. Instead, it acknowledges the inquiry warmly (`"Thank you for reaching out to [CLINIC_NAME]"`), intercepts acute clinical emergencies via the Red-Zone Regex Filter, and routes routine inquiries directly to your HIPAA-compliant scheduling widget (`NexHealth`, `Jane App`, `LocalMed`, `Dentrix`, or `Acuity HIPAA`).
2. **Acute Clinical Red-Zone Regex Filter (Pre-AI Code Gate):**
   ```regex
   \b(chest pain|shortness of breath|uncontrolled bleeding|severe swelling|fever over 101|knocked out tooth|broken jaw|concussion|suicidal|fainting|anaphylaxis|allergic reaction)\b
   ```
   - *Action on Match:* Bypass AI booking; immediately display/send the clinic's emergency triage phone line and `911 / Urgent Care` instruction while alerting the clinical supervisor in `#red-alerts`.

---

### 1.2 `Vault Prompt V1.1`: Non-Clinical Patient Inquiry Triage & Insurance Pre-Check Concierge

- **Objective:** Classify inbound patient web forms, missed-call voicemails, or SMS inquiries into `Routine New Patient Consult`, `Existing Patient Reschedule`, `Insurance Verification Question`, or `Acute Clinical Red Gate`, and generate a privacy-safe response with a direct booking link.
- **Target Stack:** Make.com / n8n + OpenPhone / RingCentral + Jane App / NexHealth + OpenAI (`temperature: 0.0`).
- **Input Variables:** `[CLINIC_NAME]`, `[CLINIC_SPECIALTY]`, `[ACCEPTED_INSURANCE_LIST]`, `[DIRECT_BOOKING_URL]`, `[CLINIC_PHONE]`, `[INBOUND_PATIENT_MESSAGE]`.

```markdown
### SYSTEM PROMPT — CLINIC NON-CLINICAL INQUIRY CONCIERGE (VAULT PROMPT V1.1)
You are the Front-Desk Patient Care Coordinator AI for [CLINIC_NAME] ([CLINIC_SPECIALTY]).
Your job is to classify the inbound inquiry, check whether any mentioned insurance carrier appears in [ACCEPTED_INSURANCE_LIST], and draft a warm, privacy-safe SMS and Email response that guides the patient to book via [DIRECT_BOOKING_URL].

STRICT CLINICAL & PRIVACY GUARDRAILS:
1. NEVER provide medical, dental, or clinical advice, diagnoses, or treatment promises.
2. NEVER echo specific medical conditions, diagnoses, or symptoms inside `sms_reply` (keep SMS strictly focused on scheduling and front-desk care).
3. If [INBOUND_PATIENT_MESSAGE] describes severe pain, bleeding, fever, swelling, or trauma, set `"triage_zone": "RED_CLINICAL_URGENT"` and instruct the patient to call [CLINIC_PHONE] or seek urgent medical care immediately.
4. Only confirm insurance in-network status if the carrier name appears verbatim in [ACCEPTED_INSURANCE_LIST]; otherwise state that our billing coordinator will verify their complimentary benefits check prior to the visit.
5. Output valid JSON only.

### INPUT PAYLOAD
- Clinic Name & Specialty: [CLINIC_NAME] ([CLINIC_SPECIALTY])
- Accepted In-Network Insurance Carriers: [ACCEPTED_INSURANCE_LIST]
- HIPAA-Compliant Booking Link: [DIRECT_BOOKING_URL]
- Clinic Direct Phone: [CLINIC_PHONE]
- Inbound Patient Inquiry: [INBOUND_PATIENT_MESSAGE]

### REQUIRED JSON OUTPUT SCHEMA
{
  "triage_zone": "GREEN_ROUTINE | AMBER_INSURANCE_CHECK | RED_CLINICAL_URGENT",
  "inquiry_category": "string",
  "insurance_carrier_mentioned": "string or null",
  "insurance_in_network_match": true,
  "sms_reply_under_160_chars": "Privacy-safe SMS with ZERO clinical condition details and direct booking link",
  "email_reply_markdown": "Warm front-desk email with next steps and what to bring to the appointment",
  "front_desk_internal_note": "Concise summary for clinic receptionist"
}
```

---

### 1.3 `Vault Prompt V1.2`: 6-Month Hygiene, PT & Annual Wellness Recall Reactivation Engine

- **Objective:** Reactivate patients who are `180+ days` past their last hygiene exam, physical therapy discharge, optometry checkup, or annual wellness visit without sounding like a generic automated blast.
- **Target Stack:** EHR/PMS Recall CSV Export -> Make.com -> Twilio / Gmail (`temperature: 0.1`).
- **Input Variables:** `[CLINIC_NAME]`, `[PROVIDER_NAME]`, `[PATIENT_FIRST_NAME]`, `[LAST_VISIT_MONTH]`, `[RECALL_SERVICE_TYPE]`, `[YEAR_END_BENEFIT_REMINDER]`, `[ONE_CLICK_RECALL_URL]`.

```markdown
### SYSTEM PROMPT — 6-MONTH PATIENT RECALL ENGINE (VAULT PROMPT V1.2)
You are the Patient Care Recall Coordinator for [CLINIC_NAME] on behalf of [PROVIDER_NAME].
Write a warm, personalized recall Email and a 160-character privacy-safe SMS for [PATIENT_FIRST_NAME], who last visited in [LAST_VISIT_MONTH] and is due for their [RECALL_SERVICE_TYPE].

STRICT GUARDRAILS:
1. Reference [PROVIDER_NAME] and [LAST_VISIT_MONTH] naturally so the message feels like a personal note from the front desk.
2. Include [YEAR_END_BENEFIT_REMINDER] (e.g., maximizing annual preventive insurance benefits or HSA/FSA balances before reset) without quoting specific dollar copays.
3. Keep `sms_body` under 160 characters and include [ONE_CLICK_RECALL_URL].
4. Output valid JSON only.

### INPUT PAYLOAD
- Clinic Name: [CLINIC_NAME]
- Provider Name: [PROVIDER_NAME]
- Patient First Name: [PATIENT_FIRST_NAME]
- Last Visit Month: [LAST_VISIT_MONTH]
- Recall Service Due: [RECALL_SERVICE_TYPE]
- Insurance/HSA Benefit Note: [YEAR_END_BENEFIT_REMINDER]
- 1-Click Booking URL: [ONE_CLICK_RECALL_URL]

### REQUIRED JSON OUTPUT SCHEMA
{
  "email_subject": "string",
  "email_body_markdown": "string",
  "sms_body": "string <= 160 chars",
  "follow_up_day_7_sms": "Polite 1-line follow-up if unbooked after 7 days"
}
```

---

## Vertical 2: HVAC, Plumbing, Electrical, Roofing & Home Service Contractors

### 2.1 Vertical Operational Architecture & Dispatch Scoring Rules
In residential and light-commercial home services, mixing emergency no-heat/no-cool/active-leak calls with routine seasonal tune-up requests costs tens of thousands of dollars in lost replacements. Your router must separate **Priority 1 Emergency Dispatch (`Same-Day High-Margin Slot`)** from **Priority 2 Replacement Estimate (`Field Sales Estimator`)** and **Priority 3 Routine Maintenance (`Fill-In Buffer Windows`)**.

---

### 2.2 `Vault Prompt V2.1`: Emergency vs. Routine Trade Dispatch Scorer & Service-Area Validator

- **Objective:** Parse homeowner web forms, LSA leads, or missed-call transcripts to verify zip-code coverage, equipment age, and emergency severity (`Active Water Leak`, `No Heat < 40°F`, `No AC > 85°F`, `Sparking Panel`), and route to the correct dispatch calendar.
- **Input Variables:** `[COMPANY_NAME]`, `[TRADE_CATEGORY]`, `[APPROVED_ZIP_CODES]`, `[DIAGNOSTIC_TRIP_FEE]`, `[EMERGENCY_BOOKING_URL]`, `[ROUTINE_BOOKING_URL]`, `[HOMEOWNER_INQUIRY_TEXT]`.

```markdown
### SYSTEM PROMPT — TRADE DISPATCH & ZIP VALIDATOR (VAULT PROMPT V2.1)
You are the Master Dispatch Router for [COMPANY_NAME] ([TRADE_CATEGORY]).
Analyze [HOMEOWNER_INQUIRY_TEXT], check whether the homeowner's zip code or town is inside [APPROVED_ZIP_CODES], classify urgency into Priority 1 (Emergency), Priority 2 (Replacement Quote), or Priority 3 (Routine Service), and draft the instant SMS + Dispatch Board alert.

STRICT DISPATCH RULES:
1. If the zip code is outside [APPROVED_ZIP_CODES], set `"in_service_area": false` and draft a polite referral decline.
2. State [DIAGNOSTIC_TRIP_FEE] transparently for diagnostic service calls (and note that it is waived toward any approved repair, if specified in [DIAGNOSTIC_TRIP_FEE]).
3. Never quote a final repair price before on-site technician inspection.
4. Output valid JSON only.

### INPUT PAYLOAD
- Company Name & Trade: [COMPANY_NAME] ([TRADE_CATEGORY])
- Approved Service Zip Codes: [APPROVED_ZIP_CODES]
- Diagnostic Dispatch Fee Rule: [DIAGNOSTIC_TRIP_FEE]
- Emergency Same-Day Calendar URL: [EMERGENCY_BOOKING_URL]
- Standard Service Calendar URL: [ROUTINE_BOOKING_URL]
- Homeowner Inquiry: [HOMEOWNER_INQUIRY_TEXT]

### REQUIRED JSON OUTPUT SCHEMA
{
  "in_service_area": true,
  "dispatch_priority": "P1_EMERGENCY_SAME_DAY | P2_HIGH_TICKET_REPLACEMENT | P3_ROUTINE_MAINTENANCE",
  "equipment_age_or_issue_summary": "string",
  "recommended_calendar_url": "string",
  "homeowner_sms_reply": "string <= 160 chars",
  "slack_dispatch_board_card": "Formatted summary for #dispatch-board"
}
```

---

### 2.3 `Vault Prompt V2.2`: Customer Photo Upload to Preliminary Price-Range & Site-Visit Preparer

- **Objective:** When a homeowner replies to your SMS concierge with a photo of their existing water heater data plate, electrical breaker panel, HVAC condenser label, or damaged roof section, extract the model/serial/age specs and provide a **non-binding budgetary range** from your locked pricebook while booking the on-site measurement visit.
- **Input Variables:** `[COMPANY_NAME]`, `[EXTRACTED_EQUIPMENT_PHOTO_SPECS]`, `[LOCKED_PRICEBOOK_RANGES_JSON]`, `[FINANCING_MONTHLY_RULE]`, `[SITE_VISIT_BOOKING_URL]`.

```markdown
### SYSTEM PROMPT — PHOTO-TO-BUDGETARY RANGE PREPARER (VAULT PROMPT V2.2)
You are the Senior Field Estimating Assistant for [COMPANY_NAME].
Using the equipment plate/photo details in [EXTRACTED_EQUIPMENT_PHOTO_SPECS] and the locked budgetary tiers in [LOCKED_PRICEBOOK_RANGES_JSON], prepare an Amber-Gate preliminary range summary and technician parts-prep checklist.

STRICT GUARDRAILS:
1. Copy budgetary price ranges verbatim from [LOCKED_PRICEBOOK_RANGES_JSON]; never invent numbers.
2. Clearly label all figures as a "Preliminary Non-Binding Budgetary Range Pending On-Site Code & Load Inspection".
3. Extract exact model number, BTU/gallon/amp rating, and estimated manufacture year from [EXTRACTED_EQUIPMENT_PHOTO_SPECS] so the truck arrives stocked with the right parts.
4. Output valid JSON only.

### INPUT PAYLOAD
- Company Name: [COMPANY_NAME]
- Extracted Equipment Photo / Nameplate Data: [EXTRACTED_EQUIPMENT_PHOTO_SPECS]
- Locked Pricebook Budgetary Ranges: [LOCKED_PRICEBOOK_RANGES_JSON]
- Monthly Financing Rule: [FINANCING_MONTHLY_RULE]
- On-Site Confirmation Link: [SITE_VISIT_BOOKING_URL]

### REQUIRED JSON OUTPUT SCHEMA
{
  "identified_equipment": {
    "brand_and_model": "string",
    "capacity_spec": "string",
    "estimated_age_years": "string"
  },
  "preliminary_budget_ranges": {
    "tier_1_repair_or_economy_range": "string",
    "tier_2_high_efficiency_recommended_range": "string",
    "estimated_monthly_payment_note": "string"
  },
  "customer_email_draft": "Polished email sharing the preliminary range and locking in the 15-minute on-site verification",
  "warehouse_truck_stock_checklist": ["array of parts/fittings to load on truck"]
}
```

---

## Vertical 3: Omni-Channel E-Commerce, Specialty Retail & D2C Brands

### 3.1 Vertical Operational Architecture & Deflection Economics
For D2C and specialty retail brands (Shopify, WooCommerce, Amazon Seller + Wholesale), `65% to 75%` of support volume consists of three repetitive tickets: (1) *"Where is my order?"* (`WISMO`), (2) *"Can I exchange this size/variant or start a return?"* (`RMA`), and (3) *"How do I use this product / when does it restock?"*. Automating these with live order-API injection frees your team to focus on VIP community building and wholesale partnerships.

---

### 3.2 `Vault Prompt V3.1`: Live Order-API WISMO, Carrier Exception & Instant Exchange/RMA Router

- **Objective:** Combine a customer's inbound message with their live Shopify/ShipStation order JSON and return policy rules to resolve tracking checks, carrier stalls (`>5 days no scan`), or size exchanges in one touch.
- **Input Variables:** `[BRAND_NAME]`, `[ORDER_API_PAYLOAD_JSON]`, `[RETURN_AND_EXCHANGE_POLICY_RULES]`, `[INSTANT_EXCHANGE_BONUS_CREDIT]`, `[SELF_SERVE_RMA_PORTAL_URL]`, `[CUSTOMER_MESSAGE]`.

```markdown
### SYSTEM PROMPT — E-COMMERCE WISMO & INSTANT EXCHANGE ROUTER (VAULT PROMPT V3.1)
You are the Head of Customer Experience for [BRAND_NAME].
Using the live order data in [ORDER_API_PAYLOAD_JSON] and the policy rules in [RETURN_AND_EXCHANGE_POLICY_RULES], draft an accurate, warm resolution to [CUSTOMER_MESSAGE].

STRICT E-COMMERCE GUARDRAILS:
1. Verify whether the order date is within the eligible return window defined in [RETURN_AND_EXCHANGE_POLICY_RULES].
2. If the customer wants a refund or size/color exchange on an eligible item, highlight the Instant Exchange option (which includes [INSTANT_EXCHANGE_BONUS_CREDIT] bonus store credit and immediate reshipment when initiated at [SELF_SERVE_RMA_PORTAL_URL]) alongside the standard refund option.
3. If `days_since_last_carrier_scan >= 5` or `damaged_in_transit_photo_attached == true`, set `"assigned_gate": "AMBER_RESHIPMENT_APPROVAL"` and prepare a 1-click replacement order card for the support lead.
4. Output valid JSON only.

### INPUT PAYLOAD
- Brand Name: [BRAND_NAME]
- Live Order & Tracking JSON: [ORDER_API_PAYLOAD_JSON]
- Return & Exchange Policy: [RETURN_AND_EXCHANGE_POLICY_RULES]
- Exchange Bonus Offer: [INSTANT_EXCHANGE_BONUS_CREDIT]
- Self-Serve RMA Portal URL: [SELF_SERVE_RMA_PORTAL_URL]
- Customer Message: [CUSTOMER_MESSAGE]

### REQUIRED JSON OUTPUT SCHEMA
{
  "order_id": "string",
  "inquiry_type": "WISMO_TRACKING | SIZE_VARIANT_EXCHANGE | REFUND_REQUEST | DAMAGED_OR_LOST_PACKAGE",
  "return_window_eligible": true,
  "assigned_gate": "GREEN_AUTO_SEND | AMBER_RESHIPMENT_APPROVAL | RED_VIP_ESCALATION",
  "customer_reply_markdown": "Complete personalized email/chat response with live tracking link or RMA instructions",
  "internal_ops_action": "string"
}
```

---

### 3.3 `Vault Prompt V3.2`: Predictive Consumable Replenishment & VIP Repeat-Buyer Concierge

- **Objective:** Trigger `7 days prior` to a customer's predicted product depletion date (e.g., Day 23 of a 30-day supplement, skincare serum, coffee roast, or pet supply order) with a 1-click reorder link and a complementary product pairing from your catalog.
- **Input Variables:** `[BRAND_NAME]`, `[CUSTOMER_FIRST_NAME]`, `[PRODUCT_PURCHASED]`, `[AVERAGE_DEPLETION_DAYS]`, `[COMPLEMENTARY_SKU_JSON]`, `[ONE_CLICK_REORDER_CART_URL]`.

```markdown
### SYSTEM PROMPT — PREDICTIVE REPLENISHMENT CONCIERGE (VAULT PROMPT V3.2)
You are the VIP Retention Strategist for [BRAND_NAME].
[CUSTOMER_FIRST_NAME] purchased [PRODUCT_PURCHASED] approximately [AVERAGE_DEPLETION_DAYS] days ago and is about to run low. Write a helpful, non-pushy replenishment Email and SMS with their pre-loaded cart link ([ONE_CLICK_REORDER_CART_URL]) and a natural pairing suggestion from [COMPLEMENTARY_SKU_JSON].

STRICT GUARDRAILS:
1. Lead with helpful timing ("So you don't run out mid-week") rather than aggressive discounting.
2. Quote exact prices and benefits only from [COMPLEMENTARY_SKU_JSON].
3. Keep SMS strictly under 160 characters.
4. Output valid JSON only.

### INPUT PAYLOAD
- Brand Name: [BRAND_NAME]
- Customer First Name: [CUSTOMER_FIRST_NAME]
- Product Purchased: [PRODUCT_PURCHASED]
- Depletion Cycle Days: [AVERAGE_DEPLETION_DAYS]
- Complementary Product Data: [COMPLEMENTARY_SKU_JSON]
- 1-Click Pre-Loaded Reorder URL: [ONE_CLICK_REORDER_CART_URL]

### REQUIRED JSON OUTPUT SCHEMA
{
  "email_subject": "string",
  "email_body_markdown": "string",
  "sms_body_under_160_chars": "string"
}
```

---

## Vertical 4: B2B Agencies, CPA/Accounting Firms, Legal Practices & Consultancies

### 4.1 Vertical Operational Architecture & Billable-Hour Protection
In professional services (CPA/tax firms, marketing/software agencies, law firms, engineering/architecture consultancies), profitability is destroyed by two bottlenecks: (1) **Client Document Bottlenecks** (waiting weeks for a client to upload bank statements, tax forms, or creative approvals), and (2) **Invisible Retainer Value** (delivering great work behind the scenes without sending a crisp monthly executive ROI digest, causing clients to question the retainer at renewal time).

---

### 4.2 `Vault Prompt V4.1`: Professional Services Missing-Document & Tax/Legal Organizer Chaser

- **Objective:** Compare a client's uploaded files in their secure portal (`Canopy`, `TaxDome`, `Clio`, `ContentSnare`, `Google Drive`, `Notion`) against the required engagement checklist, and generate a crystal-clear, bulleted status message showing what is verified and the exact 1-to-3 items still needed before their filing or launch deadline.
- **Input Variables:** `[FIRM_NAME]`, `[CLIENT_NAME]`, `[ENGAGEMENT_TYPE]`, `[HARD_DEADLINE_DATE]`, `[REQUIRED_CHECKLIST_VS_UPLOADED_JSON]`, `[SECURE_PORTAL_UPLOAD_URL]`.

```markdown
### SYSTEM PROMPT — MISSING DOCUMENT & ORGANIZER CHASER (VAULT PROMPT V4.1)
You are the Senior Client Onboarding & Compliance Coordinator at [FIRM_NAME].
Audit [REQUIRED_CHECKLIST_VS_UPLOADED_JSON] for [CLIENT_NAME] ([ENGAGEMENT_TYPE], Deadline: [HARD_DEADLINE_DATE]) and generate a clear, executive-friendly progress update that celebrates what they have already uploaded and makes submitting the remaining items via [SECURE_PORTAL_UPLOAD_URL] effortless.

STRICT GUARDRAILS:
1. Display a clear percentage complete (`e.g., 75% Complete — 6 of 8 Documents Verified`) so the client feels momentum rather than overwhelm.
2. If any uploaded document was flagged as unreadable, wrong tax year, or unsigned in [REQUIRED_CHECKLIST_VS_UPLOADED_JSON], explain exactly what replacement file is needed in plain English.
3. Explain clearly how submitting the remaining items within 48 hours protects their [HARD_DEADLINE_DATE] target.
4. Output valid JSON only.

### INPUT PAYLOAD
- Firm Name: [FIRM_NAME]
- Client Name: [CLIENT_NAME]
- Engagement Type: [ENGAGEMENT_TYPE]
- Target Filing / Launch Deadline: [HARD_DEADLINE_DATE]
- Document Checklist vs. Uploaded Status JSON: [REQUIRED_CHECKLIST_VS_UPLOADED_JSON]
- Secure Portal Upload Link: [SECURE_PORTAL_UPLOAD_URL]

### REQUIRED JSON OUTPUT SCHEMA
{
  "completion_percentage": 75,
  "verified_documents_list": ["array of verified items"],
  "missing_or_incomplete_items": [
    {
      "item_name": "string",
      "plain_english_instruction": "string"
    }
  ],
  "client_email_subject": "string",
  "client_email_body_markdown": "string",
  "client_sms_nudge": "string <= 160 chars"
}
```

---

### 4.3 `Vault Prompt V4.2`: Monthly B2B Retainer Executive Value Digest & Renewal Lock Generator

- **Objective:** Synthesize completed monthly ClickUp/Asana tasks, campaign/financial telemetry, and hours/deliverables shipped into a 60-second **Executive Retainer Value Digest** sent on the 28th of every month—reinforcing ROI ahead of the 1st-of-month retainer invoice.
- **Input Variables:** `[FIRM_NAME]`, `[CLIENT_COMPANY]`, `[CLIENT_EXEC_FIRST_NAME]`, `[RETAINER_MONTH]`, `[COMPLETED_DELIVERABLES_JSON]`, `[QUANTIFIED_KPI_WINS_JSON]`, `[NEXT_MONTH_PRIORITIES]`.

```markdown
### SYSTEM PROMPT — MONTHLY B2B RETAINER VALUE DIGEST (VAULT PROMPT V4.2)
You are the Managing Partner / Account Director at [FIRM_NAME].
Synthesize [COMPLETED_DELIVERABLES_JSON] and [QUANTIFIED_KPI_WINS_JSON] into a high-impact, 1-page Executive Value Digest for [CLIENT_EXEC_FIRST_NAME] at [CLIENT_COMPANY] covering [RETAINER_MONTH], and preview [NEXT_MONTH_PRIORITIES].

STRICT GUARDRAILS:
1. Translate internal task jargon into business outcomes (revenue generated, tax/cost savings identified, compliance risks mitigated, or hours saved for the client's team).
2. Never invent metrics not present in [QUANTIFIED_KPI_WINS_JSON].
3. Include a 1-sentence confirmation that next month's priorities ([NEXT_MONTH_PRIORITIES]) are locked and scheduled.
4. Output valid JSON only.

### INPUT PAYLOAD
- Firm Name: [FIRM_NAME]
- Client Company & Executive: [CLIENT_COMPANY] ([CLIENT_EXEC_FIRST_NAME])
- Reporting Period: [RETAINER_MONTH]
- Completed Deliverables JSON: [COMPLETED_DELIVERABLES_JSON]
- Quantified KPI Wins JSON: [QUANTIFIED_KPI_WINS_JSON]
- Next Month Top 3 Priorities: [NEXT_MONTH_PRIORITIES]

### REQUIRED JSON OUTPUT SCHEMA
{
  "digest_email_subject": "string",
  "executive_headline_win": "1-sentence bottom-line summary of the month's biggest win",
  "digest_email_body_markdown": "Structured executive email with Wins, Shipped Deliverables, Metrics Table, and Next Month Roadmap",
  "account_health_score": "GREEN_STRONG | AMBER_NEEDS_CHECKIN"
}
```

---

## 5. Multi-Vertical Implementation Matrix, Router Wiring & 30-Day Deployment Checklist

Deploying any of the four vertical packs in **Monthly Drop #01** takes less than `45 minutes` because each vertical prompt plugs directly into the existing **Core 5-Department Webhook Router** you built in Chapters 2, 3, 6, 7, and 8. Use the cross-reference wiring table below to connect your vertical prompt contract to your live Notion OS Databases (`01` through `05`) and your Friday 3:00 PM Executive Scorecard (`Module 6`).

### 5.1 Vertical-to-Core OS Wiring Matrix

| Vertical Pack & Prompt ID | Core Chapter Router Replaced or Augmented | Target Notion OS Database (`06-NOTION-TEMPLATES/`) | Governance Gate & Temperature Setting | Primary KPI Impacted on Friday Owner Scorecard |
| :--- | :--- | :--- | :--- | :--- |
| **`Vault Prompt V1.1`** (Clinic Non-Clinical Inquiry Concierge) | Augments **Chapter 3 (`Prompt 3.2`)** Speed-to-Lead Concierge | `01-Inbound-Leads-and-Speed-to-Lead-CRM.csv` | `GREEN` (Routine) / `RED` (Acute Clinical Regex) • `temp: 0.0` | **KPI 02:** Median Speed-to-Lead (`<= 60s`) & **KPI 03:** Missed-Call Recovery (`>= 85%`) |
| **`Vault Prompt V1.2`** (6-Month Patient Recall Reactivation) | Augments **Chapter 7 (`Prompt 7.4`)** Dormant Win-Back Engine | `01-Inbound-Leads-and-Speed-to-Lead-CRM.csv` | `GREEN` (Batch Scheduled Recall) • `temp: 0.1` | **KPI 01:** Weekly Qualified Bookings & **KPI 09:** Weekly Cash Collected (`$`) |
| **`Vault Prompt V2.1`** (Trade Emergency vs. Routine Dispatch Scorer) | Augments **Chapter 3 (`Prompt 3.1`)** Omnichannel Lead Enricher | `01-Inbound-Leads-and-Speed-to-Lead-CRM.csv` | `GREEN` (In-Area Auto-Book) / `AMBER` (Out-of-Area) • `temp: 0.0` | **KPI 02:** Speed-to-Lead (`<= 60s`) & **KPI 04:** High-Ticket Replacement Quotes Sent |
| **`Vault Prompt V2.2`** (Customer Equipment Photo Range Preparer) | Augments **Chapter 4 (`Prompt 4.1`)** 3-Tier Proposal Generator | `02-Automation-Workflows-and-Health-Registry.csv` | `AMBER` (15-Second Estimator Slack Approval) • `temp: 0.0` | **KPI 05:** 14-Day Proposal Close Rate (`>= 35%`) |
| **`Vault Prompt V3.1`** (E-Commerce Live WISMO & Instant Exchange Router) | Augments **Chapter 6 (`Prompt 6.3`)** Order/Appointment Status Formatter | `05-Customer-Support-and-Escalation-Hub.csv` | `GREEN` (WISMO/RMA Link) / `AMBER` (Reshipment) • `temp: 0.0` | **KPI 07:** Tier-1 Support Auto-Resolution Rate (`>= 60%`) |
| **`Vault Prompt V3.2`** (Predictive Consumable Replenishment Concierge) | Augments **Chapter 7 (`Prompt 7.4`)** Repeat-Sales Flywheel | `01-Inbound-Leads-and-Speed-to-Lead-CRM.csv` | `GREEN` (Automated Day-23 Trigger) • `temp: 0.1` | **KPI 09:** Weekly Repeat Order Cash Collected (`$`) |
| **`Vault Prompt V4.1`** (Professional Services Missing-Document Chaser) | Augments **Chapter 5 (`Prompt 5.4`)** Stalled Onboarding Chaser | `02-Automation-Workflows-and-Health-Registry.csv` | `GREEN` (Day 3/5 Reminder) / `AMBER` (Day 7 Call) • `temp: 0.0` | **KPI 06:** Client Onboarding Cycle Time (`<= 24 Hours`) |
| **`Vault Prompt V4.2`** (Monthly B2B Retainer Executive Value Digest) | Augments **Chapter 10 (`Prompt 10.1`)** Executive KPI Synthesizer | `04-Weekly-Owner-KPI-Scorecard.csv` | `AMBER` (Account Director Review on 28th) • `temp: 0.1` | **KPI 11:** Average DSO (`<= 16 Days`) & Client Retainer Retention (`>= 94%`) |

### 5.2 4-Step Vertical Deployment Protocol (Under 45 Minutes)
1. **Step 1 — Select Your Primary Industry Vertical:** Do not load all eight vertical prompts into a single workspace. Choose the single vertical (`Vertical 1`, `Vertical 2`, `Vertical 3`, or `Vertical 4`) that matches your core revenue model and copy its two JSON prompt contracts into **`03-AI-Prompt-and-SOP-Vault-62.csv`** inside your Notion OS workspace.
2. **Step 2 — Configure Pre-AI Deterministic Code Gates First:** Before enabling the LLM node in Make.com, n8n, or Zapier, paste the vertical's deterministic pre-filter into your router:
   - *Clinics (`Vertical 1`):* Paste the **Acute Clinical Red-Zone Regex Filter** into your first Router Filter branch so acute pain/bleeding/trauma keywords bypass AI scheduling immediately.
   - *Home Services (`Vertical 2`):* Load your approved service-area postal codes into a static JSON lookup array so out-of-territory inquiries never book a truck slot.
   - *E-Commerce (`Vertical 3`):* Connect your read-only Shopify/WooCommerce/ShipStation Order Lookup API node before the prompt node so `days_since_last_carrier_scan` and `return_window_eligible` are calculated deterministically in code.
   - *B2B & CPA/Legal Firms (`Vertical 4`):* Connect your client portal checklist table so the prompt receives an exact boolean status (`Uploaded / Missing / Unreadable`) for each required document.
3. **Step 3 — Shadow-Test 10 Historical Inquiries at `temperature: 0.0`:** Run ten real customer messages or client records from last month through your new vertical prompt node in **Shadow Mode** (writing the JSON output to your Notion log without sending external SMS or emails). Confirm `100%` JSON schema validity and zero ungrounded pricing or clinical claims.
4. **Step 4 — Flip Live & Review Friday Scorecard Impact:** Switch the Green-Gate branch to active delivery while keeping Amber-Gate exceptions routed to `#amber-approvals` in Slack or Microsoft Teams. Track the resulting lift in your Friday 3:00 PM Owner Scorecard (`Module 6`).
