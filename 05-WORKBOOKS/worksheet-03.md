# Worksheet 3: Multi-Channel Lead Capture & Qualification Blueprint

**Companion To:** Chapter 3 — *The 60-Second Speed-to-Lead & Multi-Channel Intake System*  
**Document Code:** `WB-CH03-INSTANT-V1`  
**Target Completion Time:** 35 Minutes  
**Applicable Team Size:** Solo Operator to 25-Person Small Business  

---

## Executive Instructions: Building Your 60-Second Frontline Funnel

Responding to an inbound prospect within **60 seconds** yields a **391% higher conversion rate** than responding at the 5-minute mark, and more than **21x higher qualification rates** than waiting 30 minutes. Yet in most small businesses, leads arrive across six disconnected doors—missed phone calls, website forms, emails, Instagram/Facebook DMs, WhatsApp messages, and Google Business Profile chats—and sit unnoticed for hours.

Use this blueprint to wire all inbound lead channels into **The I.N.S.T.A.N.T. Lead Router** (`Dept 01`) so that 100% of genuine prospects receive a personalized, compliant response and booking path in under 60 seconds, 24 hours a day, 365 days a year.

---

## Part A: Omni-Channel Intake Inventory & Webhook Mapping

Audit every entry door where a prospective customer, patient, or B2B client can contact your business today, and map each channel to your central automation bridge (Make, Zapier, or n8n):

| Channel ID | Inbound Lead Channel | Current Software / Platform | Monthly Inquiry Volume | Webhook / Trigger Event Type | Target Response Channel(s) | Target SLA (Seconds) | Connected to Router? (`Yes`/`No`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`CH-01`** | **Inbound Phone — Missed / Busy / After-Hours** | `[VOIP_PROVIDER]` *(e.g., OpenPhone, RingCentral, Twilio)* | `[VOL_01]` | `call.missed` / `voicemail.created` (after 20s ring) | Instant SMS (`Prompt 3.3`) + CRM Deal | `< 35 sec` | `[STATUS_01]` |
| **`CH-02`** | **Website Contact / Estimate Request Form** | `[WEB_FORM_APP]` *(e.g., WPForms, Typeform, HubSpot, Webflow)* | `[VOL_02]` | `form.submission.webhook` | Instant SMS + Personalized Email (`Prompt 3.2`) | `< 45 sec` | `[STATUS_02]` |
| **`CH-03`** | **Google Local Service Ads / Google Business Chat** | `[GOOGLE_GBP_ACCOUNT]` | `[VOL_03]` | `gbp.message.received` / `lsa.lead.created` | GBP Reply + SMS Follow-Up | `< 45 sec` | `[STATUS_03]` |
| **`CH-04`** | **Meta Lead Ads & Instagram / Facebook DMs** | `[META_BUSINESS_SUITE]` | `[VOL_04]` | `leadgen.webhook` / `instagram.dm.received` | Instant DM Reply + SMS/Email | `< 45 sec` | `[STATUS_04]` |
| **`CH-05`** | **Direct SMS / WhatsApp Business Inbound** | `[SMS_WHATSAPP_NUMBER]` | `[VOL_05]` | `message.incoming.webhook` | Conversational SMS/WhatsApp (`Prompt 3.3`) | `< 30 sec` | `[STATUS_05]` |
| **`CH-06`** | **Direct Email Inquiries (`info@` / `sales@` / Portals)** | `[EMAIL_PROVIDER]` *(e.g., Google Workspace, M365)* | `[VOL_06]` | `email.arrived` (Filtered by Subject/Parser) | Threaded Email Reply + SMS Alert | `< 60 sec` | `[STATUS_06]` |
| **TOTAL** | **All Inbound Doors Combined** | **Unified into 1 Webhook Bus** | **`[SUM_VOL]`** | **Normalized JSON Event** | **Multi-Channel 60s First Touch** | **`< 60 sec`** | **Goal: 100%** |

---

## Part B: Standard CRM Field Mapping & Normalization Contract

To prevent duplicate contacts and broken downstream automations in `Dept 02` (Quoting) and `Dept 04` (Invoicing), every inbound channel in **Part A** must map its raw fields into the **12 Canonical Lead Fields** below before saving to your CRM:

| # | Canonical CRM Field Key | Data Type | Normalization & Formatting Rule (`[N]` Step) | Fallback Value if Missing from Raw Inquiry | Your CRM Custom Property Name |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01` | `contact_first_name` | `String` | Title-case first token; strip emojis and titles (`Dr.`, `Mr.`) | `"there"` *(so greeting reads `"Hi there,"`)* | `[CRM_FIELD_01]` |
| `02` | `contact_last_name` | `String` | Title-case remaining name tokens | `""` (Blank until slot-filled via `Prompt 3.4`) | `[CRM_FIELD_02]` |
| `03` | `phone_e164` | `String` | Strip spaces/dashes/parens; prefix country code (e.g., `+15125550199`, `+447700900077`) | `null` (Route to Email-Only First Touch) | `[CRM_FIELD_03]` |
| `04` | `email_clean` | `String` | Lowercase, trim whitespace, validate `@` domain syntax | `null` (Route to SMS-Only First Touch) | `[CRM_FIELD_04]` |
| `05` | `postal_or_zip_code` | `String` | Extract 5-digit US Zip or UK/CA/AU postcode via regex | `"UNKNOWN_GEO"` (Trigger `Prompt 3.4` ask) | `[CRM_FIELD_05]` |
| `06` | `source_channel` | `Enum` | `MISSED_CALL`, `WEB_FORM`, `GOOGLE_GBP`, `META_DM`, `SMS_DIRECT`, `EMAIL_PORTAL` | `"DIRECT_UNKNOWN"` | `[CRM_FIELD_06]` |
| `07` | `utm_campaign_source` | `String` | Capture `utm_source` + `utm_campaign` or referring URL | `"organic_or_direct"` | `[CRM_FIELD_07]` |
| `08` | `service_category` | `Enum` | Classify via `Prompt 3.1` into your official service/product lines | `"GENERAL_INQUIRY"` | `[CRM_FIELD_08]` |
| `09` | `urgency_tier` | `Enum` | `EMERGENCY_SAME_DAY`, `HIGH_THIS_WEEK`, `STANDARD_PLANNING`, `LOW_EXPLORATORY` | `"STANDARD_PLANNING"` | `[CRM_FIELD_09]` |
| `10` | `lead_intent_score` | `Integer` | Calculated `0–100` score from `Prompt 3.1` | `50` | `[CRM_FIELD_10]` |
| `11` | `sms_opt_in_status` | `Boolean` | `true` if web checkbox checked OR inbound call/SMS initiated by prospect | `false` (Do not send promotional SMS) | `[CRM_FIELD_11]` |
| `12` | `response_sla_seconds` | `Integer` | `UNIX_TIMESTAMP(first_reply_sent_at) - UNIX_TIMESTAMP(lead_created_at)` | `null` (Alert on Friday Scorecard if `>60`) | `[CRM_FIELD_12]` |

### Deduplication Lookup Order (`3-Second Upsert Rule`)
1. **Primary Lookup:** Search CRM Contacts by exact `phone_e164`.
2. **Secondary Lookup (if phone is null or not found):** Search CRM Contacts by exact `email_clean`.
3. **Upsert Action:** If a matching contact is found, **update** the existing contact record, append the new inquiry note to their activity timeline, and create/update their active Deal in `Dept 01`. Never create a duplicate contact row.

---

## Part C: The 5-Question Qualification, Scoring & Disqualification Matrix

Define the exact business rules that **Prompt 3.1** and **Prompt 3.3** will use to score your inbound leads (`0–100 points`), ask 1–2 frictionless qualifying questions, and filter out spam or out-of-scope inquiries:

### C.1 Your Custom Qualification Criteria Table

| Qualification Dimension | Ideal High-Intent Fit (`+20 to +30 Pts`) | Standard Acceptable Fit (`+10 to +15 Pts`) | Disqualified / Out-of-Scope (`Route to Referral / Redirect`) | Your Exact Business Rule / Values |
| :--- | :--- | :--- | :--- | :--- |
| **1. Geographic Territory / Delivery Zone** | Inside primary zip/postal codes or target B2B countries | Secondary zone (travel fee or minimum order applies) | Outside service area or restricted shipping country | **Approved Zips/Regions:** `[YOUR_APPROVED_GEO_ZONES]` |
| **2. Service / Product Category Requested** | Core high-margin service, treatment plan, or retainer | Standard repair, consult, or catalog order | Services you do not perform (e.g., warranty on competitor gear) | **Core Services:** `[YOUR_CORE_SERVICES_LIST]` |
| **3. Timeline & Urgency** | Immediate / Emergency / Within 7 days | Within 14 to 30 days | "Just browsing for next year" / Student research | **Emergency Keywords:** `[YOUR_URGENT_KEYWORDS]` |
| **4. Estimated Budget / Deal Size Minimum** | Exceeds target anchor package (`>$[VIP_THRESHOLD]`) | Meets minimum job/order floor (`>$[MIN_ORDER_FLOOR]`) | Below minimum dispatch/project floor (`<$[MIN_ORDER_FLOOR]`) | **Min Floor:** `$[MIN_ORDER_FLOOR]` \| **VIP:** `$[VIP_THRESHOLD]` |
| **5. Decision-Maker Authority** | Homeowner, Practice Owner, Company Founder, Authorized Buyer | Vetted Operations Manager or Spouse | Cold SEO/marketing vendor, job applicant, robocaller | **Spam Filter Keywords:** `SEO, backlinks, virtual assistant, merchant cash advance` |

### C.2 Your 2 Frictionless SMS Qualifying Questions

When a prospect calls and misses you—or submits a short inquiry—never send a link to a 15-question survey. Write the **two simple questions** your 60-second SMS concierge (`Prompt 3.2` / `Prompt 3.3`) will ask so the prospect can reply in 10 seconds with a thumb tap:

* **Qualifying Question 1 (Service Category / Core Need):**  
  *"Hi `{{contact_first_name}}`, this is the automated desk at `[BUSINESS_NAME]`. Sorry we missed your call! So we can get you taken care of right away, are you looking for: **(1) `[OPTION_1_CORE_SERVICE]`**, **(2) `[OPTION_2_SERVICE]`**, or **(3) `[OPTION_3_EMERGENCY_OR_CUSTOM]`**?"*
* **Qualifying Question 2 (Location / Urgency + Booking Link):**  
  *"Got it! What is your **zip/postal code** (or project timeline), and would you like to grab our next open slot right here? `[DIRECT_CALENDAR_BOOKING_LINK]`"*

---

## Part D: Telecommunications & Privacy Compliance Checklist (A2P 10DLC / TCPA / GDPR / CASL)

Before turning on automated SMS or WhatsApp replies in `Dept 01`, complete and verify these six mandatory compliance safeguards:

- [ ] **1. Carrier Brand & Campaign Registration (US/CA A2P 10DLC / UK & AU Sender ID):** Our business EIN/registration number and conversational customer-care use case are registered and approved inside our VoIP/SMS provider (Twilio, OpenPhone, HighLevel, or RingCentral).
- [ ] **2. Website Form Explicit SMS Opt-In Disclosure:** Every website quote/contact form includes an explicit consent checkbox beneath the phone field reading:  
  `[ ] By providing your phone number, you agree to receive automated and human text messages from [BUSINESS_NAME] regarding your inquiry, scheduling, and service updates. Msg & data rates may apply. Reply STOP to opt out.`
- [ ] **3. Clear Sender Identification in First Message:** Every automated first-touch SMS clearly states our business name (`[BUSINESS_NAME]`) in the first sentence.
- [ ] **4. Automated `STOP` / `UNSUBSCRIBE` Webhook Listener:** If any recipient replies `STOP`, `UNSUBSCRIBE`, `CANCEL`, or `QUIT`, our VoIP carrier and CRM immediately set `sms_opt_in_status = false` and block all future automated texts.
- [ ] **5. Spam / Robocall Pre-Filter Active (`Prompt 3.1`):** Automated SMS replies are suppressed whenever the inbound message is flagged as a vendor solicitation, automated bot, or `noreply@` address.
- [ ] **6. Direct Human Escalation Keyword (`HUMAN` / `AGENT` / `0`):** If a prospect replies `HUMAN`, `CALL ME`, or expresses frustration, the bot immediately halts conversational slot-filling and triggers a live staff callback alert (`Prompt 3.5`).

---

## Part E: 60-Second Speed-to-Lead Live Verification & SLA Test Log

Before marking Chapter 3 complete, run **five live end-to-end tests** from a personal mobile phone and external email account (including at least one test after 6:00 PM) and log the exact stopwatch timestamps below:

| Test # | Simulated Inbound Scenario | Test Timestamp (`lead_created_at`) | First Reply Received (`first_reply_at`) | Measured Latency (Seconds) | CRM Contact Upserted & Scored? | Booking Link / VIP Alert Verified? | Pass / Fail (`< 60s SLA`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Test 1** | Call business number from mobile & hang up at voicemail | `[T1_START]` | `[T1_END]` | `[T1_SEC] sec` | `[YES / NO]` | `[YES / NO]` | `[PASS / FAIL]` |
| **Test 2** | Submit website quote form with high-ticket VIP scope | `[T2_START]` | `[T2_END]` | `[T2_SEC] sec` | `[YES / NO]` | `[YES / NO]` | `[PASS / FAIL]` |
| **Test 3** | Send incomplete inquiry missing zip code / service type | `[T3_START]` | `[T3_END]` | `[T3_SEC] sec` | `[YES / NO]` | `[YES / NO]` | `[PASS / FAIL]` |
| **Test 4** | Submit simulated cold SEO spam solicitation form | `[T4_START]` | `Suppressed` | `0 SMS Sent` | `Tagged Spam` | `Suppressed` | `[PASS / FAIL]` |
| **Test 5** | After-hours / weekend inquiry via Social DM or Web Form | `[T5_START]` | `[T5_END]` | `[T5_SEC] sec` | `[YES / NO]` | `[YES / NO]` | `[PASS / FAIL]` |

**Speed-to-Lead Architecture Verified By:** `[OWNER_OR_REVOPS_LEAD]`  
**Business Name:** `[BUSINESS_NAME]`  
**Median Verified Response SLA:** `[MEDIAN_SLA_SECONDS] seconds` *(Target: `< 45 seconds`)*  
**Sign-Off Date:** `[SIGN_OFF_DATE]`  
