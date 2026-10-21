# Worksheet 4: Automated Quote Matrix & Follow-Up Cadence Planner

**Companion To:** Chapter 4 — *Automated Estimating, Quotes & Follow-Up Sequences That Close*  
**Document Code:** `WB-CH04-QUOTES-V1`  
**Target Completion Time:** 40 Minutes  
**Applicable Team Size:** Solo Operator to 25-Person Small Business  

---

## Executive Instructions: Eliminating "Gut-Feel" Quoting & Silent Proposal Decay

Small businesses lose up to 40% of their qualified sales pipeline inside **Department 02 (Quoting & Follow-Up)** due to three structural flaws:
1. **The Owner-Only Pricing Bottleneck:** Because pricing rules live inside the owner's head ("gut-feel quoting"), estimates wait 24 to 72 hours until the owner has a quiet evening to type them up.
2. **Single-Option "Take-It-or-Leave-It" Quotes:** Sending a single price forces the buyer to compare your single number against a cheaper competitor, rather than choosing *which level of value* they want from you.
3. **Abandoning Follow-Up After One Email:** Over 80% of B2B and local service deals close between Touch #5 and Touch #8, yet 44% of small businesses stop following up after sending a single PDF.

Use this workbook to convert your pricing into a **Deterministic 3-Tier Price Matrix** (`Part A` & `Part B`), enforce your **Amber-Gate Gross Margin Floor** (`Part C`), and map your **14-Day 6-Touch Follow-Up Loop** (`Part D` & `Part E`).

---

## Part A: Good-Better-Best (3-Tier) Package & Gross Margin Matrix

Whenever a prospect requests a quote, your AI Estimating Engine (`Prompt 4.1` & `Prompt 4.2`) should present **three structured options** on a single page:
* **Option 1 — Essential / Core Compliance (`1.00x Baseline`):** Solves the immediate mandatory problem with standard turnaround and zero non-essential add-ons. Protects your price floor for budget-sensitive buyers.
* **Option 2 — Complete Recommended Solution (`1.30x–1.45x Anchor`):** Includes the core scope plus extended warranty, preventative maintenance, or optimization reporting. Engineered as the highest-value anchor (**selected by 55% to 65% of buyers**).
* **Option 3 — Priority Turnkey / VIP Package (`1.65x–1.90x Premium`):** Includes everything in Option 2 plus expedited scheduling, dedicated senior technician/partner oversight, and multi-quarter protection. Makes Option 2 look moderately priced while capturing 15% to 20% of buyers who value speed and certainty above all else.

### A.1 Your Core Service Lines — 3-Tier Pricing & Margin Table

Complete the matrix below for your top three revenue-generating services or product categories:

| Service Line & Option Tier | Included Scope & Deliverables (`3–4 Bullet Points`) | Direct Labor Hours (`H`) | Burdened Labor Cost (`$`) | Direct Materials / COGS (`$`) | Total Direct Cost (`C`) | Target Price (`P`) | Gross Margin `$` (`P - C`) | Gross Margin `%` (`(P-C)÷P`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Service Line 1:** `[SERVICE_LINE_1_NAME]` | **Base Unit Metric:** `[BASE_UNIT_1]` *(e.g., per SqFt, per Ton, per Monthly Retainer)* | — | — | — | — | — | — | **Floor: `>=48%`** |
| **• Tier 1: Essential** | `[S1_TIER1_DELIVERABLES]` | `[S1_T1_HRS]` | `$[S1_T1_LAB]` | `$[S1_T1_MAT]` | `$[S1_T1_COST]` | **`$[S1_T1_PRICE]`** | `$[S1_T1_GM]` | `[S1_T1_PCT]%` |
| **• Tier 2: Complete (Anchor)** | `[S1_TIER2_DELIVERABLES]` | `[S1_T2_HRS]` | `$[S1_T2_LAB]` | `$[S1_T2_MAT]` | `$[S1_T2_COST]` | **`$[S1_T2_PRICE]`** | `$[S1_T2_GM]` | `[S1_T2_PCT]%` |
| **• Tier 3: Priority VIP** | `[S1_TIER3_DELIVERABLES]` | `[S1_T3_HRS]` | `$[S1_T3_LAB]` | `$[S1_T3_MAT]` | `$[S1_T3_COST]` | **`$[S1_T3_PRICE]`** | `$[S1_T3_GM]` | `[S1_T3_PCT]%` |
| **Service Line 2:** `[SERVICE_LINE_2_NAME]` | **Base Unit Metric:** `[BASE_UNIT_2]` | — | — | — | — | — | — | **Floor: `>=48%`** |
| **• Tier 1: Essential** | `[S2_TIER1_DELIVERABLES]` | `[S2_T1_HRS]` | `$[S2_T1_LAB]` | `$[S2_T1_MAT]` | `$[S2_T1_COST]` | **`$[S2_T1_PRICE]`** | `$[S2_T1_GM]` | `[S2_T1_PCT]%` |
| **• Tier 2: Complete (Anchor)** | `[S2_TIER2_DELIVERABLES]` | `[S2_T2_HRS]` | `$[S2_T2_LAB]` | `$[S2_T2_MAT]` | `$[S2_T2_COST]` | **`$[S2_T2_PRICE]`** | `$[S2_T2_GM]` | `[S2_T2_PCT]%` |
| **• Tier 3: Priority VIP** | `[S2_TIER3_DELIVERABLES]` | `[S2_T3_HRS]` | `$[S2_T3_LAB]` | `$[S2_T3_MAT]` | `$[S2_T3_COST]` | **`$[S2_T3_PRICE]`** | `$[S2_T3_GM]` | `[S2_T3_PCT]%` |
| **Service Line 3:** `[SERVICE_LINE_3_NAME]` | **Base Unit Metric:** `[BASE_UNIT_3]` | — | — | — | — | — | — | **Floor: `>=48%`** |
| **• Tier 1: Essential** | `[S3_TIER1_DELIVERABLES]` | `[S3_T1_HRS]` | `$[S3_T1_LAB]` | `$[S3_T1_MAT]` | `$[S3_T1_COST]` | **`$[S3_T1_PRICE]`** | `$[S3_T1_GM]` | `[S3_T1_PCT]%` |
| **• Tier 2: Complete (Anchor)** | `[S3_TIER2_DELIVERABLES]` | `[S3_T2_HRS]` | `$[S3_T2_LAB]` | `$[S3_T2_MAT]` | `$[S3_T2_COST]` | **`$[S3_T2_PRICE]`** | `$[S3_T2_GM]` | `[S3_T2_PCT]%` |
| **• Tier 3: Priority VIP** | `[S3_TIER3_DELIVERABLES]` | `[S3_T3_HRS]` | `$[S3_T3_LAB]` | `$[S3_T3_MAT]` | `$[S3_T3_COST]` | **`$[S3_T3_PRICE]`** | `$[S3_T3_GM]` | `[S3_T3_PCT]%` |

---

## Part B: Deterministic Complexity Multipliers & Add-On SKU Registry

How do you get "owner intuition" out of your head and into a table that `Prompt 4.1` can apply with 100% mathematical accuracy? You define **Complexity Multipliers** (for difficult access, legacy data migration, rush timelines, or multi-location coordination) and **Fixed Add-On SKUs**.

### B.1 Complexity Multiplier Rules

$$\text{Calculated Option Price} = \left(\text{Base Tier Price} \times \text{Complexity Multiplier}\right) + \sum \text{Selected Add-On SKUs}$$

| Multiplier Code | Operational Condition / Trigger in Discovery Notes | Multiplier Factor | Automatic Labor Buffer Added | Your Specific Condition Definition |
| :--- | :--- | :--- | :--- | :--- |
| **`MULT-STD`** | **Standard Access / Clean Baseline:** Normal business hours, standard layout/data, 1 decision-maker | `1.00x` | `+0% hrs` | `[YOUR_STD_CONDITION]` |
| **`MULT-MOD`** | **Moderate Complexity:** Tight attic/crawlspace, 2–3 software integrations, older building/code, 2 locations | `1.20x` | `+20% hrs` | `[YOUR_MOD_CONDITION]` |
| **`MULT-HIGH`** | **High Complexity / Heavy Remediation:** Historic/commercial code, messy legacy database cleanup, custom fabrication | `1.45x` | `+45% hrs` | `[YOUR_HIGH_CONDITION]` |
| **`MULT-RUSH`** | **Expedited / Weekend / 48-Hour Rush Turnaround:** Customer requests immediate priority jump ahead of queue | `1.30x` | Overtime rate | `[YOUR_RUSH_CONDITION]` |

### B.2 Approved Add-On SKU Table (Grounded Reference for `Prompt 4.1`)

| Add-On SKU ID | Add-On Name & Customer-Facing Description | Unit Basis | Direct Cost (`$`) | Retail Price (`$`) | Auto-Included in Which Tier? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ADD-01` | `[ADDON_01_NAME]` *(e.g., 2-Year Preventative Maintenance / Monthly Analytics Pack)* | `[UNIT_01]` | `$[COST_01]` | `$[PRICE_01]` | `Tier 2 & Tier 3` |
| `ADD-02` | `[ADDON_02_NAME]` *(e.g., Priority 4-Hour SLA / Dedicated Account Slack Channel)* | `[UNIT_02]` | `$[COST_02]` | `$[PRICE_02]` | `Tier 3 Only` |
| `ADD-03` | `[ADDON_03_NAME]` *(e.g., Extended 5-Year Parts & Labor Protection / Annual Audit)* | `[UNIT_03]` | `$[COST_03]` | `$[PRICE_03]` | `Tier 3 Only` |
| `ADD-04` | `[ADDON_04_NAME]` *(e.g., Old Equipment Haul-Away / Legacy Data Archive Migration)* | `[UNIT_04]` | `$[COST_04]` | `$[PRICE_04]` | `Optional Line Item` |
| `ADD-05` | `[ADDON_05_NAME]` *(e.g., Staff On-Site Training Session / Custom Brand Kit)* | `[UNIT_05]` | `$[COST_05]` | `$[PRICE_05]` | `Tier 2 & Tier 3` |

---

## Part C: Amber-Gate Margin Floor & Discount Guardrail Rules

Lock in the hard financial boundaries that your pre-flight validator (`Prompt 2.4` / `Prompt 4.1`) and your **Amber Approval Card** enforce before any proposal reaches a prospect:

1. **Minimum Acceptable Gross Margin Floor (`GM_FLOOR`):** `[MIN_GROSS_MARGIN_PCT]%` *(Studio Recommended Floor: `48.0%` for services/clinics/agencies; `38.0%` for retail/equipment installation).* Any quote draft that calculates below this margin is automatically blocked and flagged in red on the owner's Slack card.
2. **Maximum Pre-Approved Paid-in-Full Incentive (`MAX_PIF_INCENTIVE`):** `[MAX_PIF_PCT]%` *(e.g., `3% to 5%` maximum savings only when the customer pays 100% upfront via ACH/bank transfer instead of credit card stages).*
3. **The Iron Rule of Price Objections (`Prompt 4.4`):** Staff and AI prompts are **strictly forbidden** from reducing the price of `Tier 2` or `Tier 3` while keeping the scope identical. If a prospect states that `Tier 2` exceeds their budget, the system must either:
   * Pivot the buyer to **`Tier 1 (Essential Scope)`**, OR
   * Split `Tier 2` into **Phase 1 (Immediate Core)** and **Phase 2 (60 Days Later)**.
4. **Proposal Expiration Window:** Every generated quote includes a deterministic validity date set to **`[VALIDITY_DAYS]` calendar days** from dispatch *(Recommended: `14 days` to align with the 14-day nurture loop)*.

---

## Part D: The 14-Day 6-Touch Multi-Channel Follow-Up Cadence Grid

Once you tap **`[Approve & Send]`** on an Amber Quote Card, the prospect enters your automated **14-Day Multi-Touch Nurture Loop (`Prompt 4.3`)**. Unlike nagging *"Just checking in on my quote"* emails, every touch delivers a distinct piece of decision-making value:

| Touch # & Day | Timing Offset | Channel | Core Strategic Angle & Value Delivered | Subject Line / SMS Preview Template | Automated Stop Condition Checked Before Firing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Touch 1 (Day 1)** | `Immediate (0m)` | **Email + SMS** | **Interactive 3-Option Proposal Delivery + Heads-Up:** Delivers the 3-tier quote link/PDF and sends a 1-sentence SMS confirming arrival. | *Email:* `Your 3 Options for [PROJECT_OR_SERVICE] — [BUSINESS_NAME]` \| *SMS:* `Hi {{first_name}}, just emailed your 3 custom options...` | Verify `amber_approved == true` |
| **Touch 2 (Day 2)** | `+28 Hours` | **Email** | **Top 3 Process & Implementation FAQs:** Proactively answers the 3 questions prospects hesitate to ask (timeline, disruption, warranty/guarantee). | `Quick question on your [SERVICE_CATEGORY] plan (+ how we prevent delays)` | Stop if `Quote_Status == Signed` OR `Prospect_Replied == true` |
| **Touch 3 (Day 4)** | `+96 Hours` | **SMS + Email** | **Matched Case Study / Before-After Social Proof:** Shares a 4-sentence story of a similar customer who chose `Tier 2` and the measurable result they achieved. | `How [SIMILAR_CLIENT_TYPE] solved [PAIN_POINT] in [TIMEFRAME]` | Stop if `Quote_Status == Signed` OR `Prospect_Replied == true` |
| **Touch 4 (Day 7)** | `+7 Days` | **SMS** | **Frictionless Timeline & Question Check:** Short conversational text asking if they are still targeting their stated start date. | `Hi {{first_name}}, are you still aiming to have [OUTCOME] wrapped up by [TARGET_DATE]?` | Stop if `Quote_Status == Signed` OR `Prospect_Replied == true` |
| **Touch 5 (Day 10)** | `+10 Days` | **Email** | **Scope Adjustment / Tier-1 Pivot Offer (`Prompt 4.4`):** Reminds them that if budget or timing shifted, we can start with `Option 1 (Essential)` first. | `Want to adjust the scope or start with Option 1 for [BUSINESS_OR_HOME]?` | Stop if `Quote_Status == Signed` OR `Prospect_Replied == true` |
| **Touch 6 (Day 14)** | `+14 Days` | **Email + SMS** | **Polite "Close-the-File" Trigger (`Prompt 4.5`):** Politely informs them their quote reservation expires today and asks if we should close their file or hold their slot. | `Should I close out your [SERVICE_CATEGORY] file for now, {{first_name}}?` | Stop if `Quote_Status == Signed`; if no reply by Day 21, move to `90-Day Win-Back` |

---

## Part E: Stop-on-Reply & Stop-on-Deposit Webhook Verification Checklist

Before activating your 14-day quote follow-up sequence, verify that your automation bridge enforces these five **Kill-Switch Triggers** so a paying or actively replying client never receives an automated chaser:

- [ ] **1. E-Signature Webhook Listener (`PandaDoc` / `Qwilr` / `ServiceTitan` / `HubSpot Quotes`):** The instant `document.completed` or `quote.accepted` fires, the bridge updates CRM Deal Stage to `CLOSED_WON`, cancels all pending Day 2–14 scheduled touches, and triggers `Dept 03` Onboarding.
- [ ] **2. Deposit Payment Webhook Listener (`Stripe` / `QuickBooks` / `Square`):** If a customer pays a deposit invoice directly via bank link before signing the form, the payment webhook immediately halts the quote follow-up loop.
- [ ] **3. Inbound Email Reply Detection:** Before sending Touch 2, 3, 5, or 6, the workflow queries the email thread (`thread_id`) to confirm zero unread or newer inbound replies from `{{email_clean}}`.
- [ ] **4. Inbound SMS Reply Detection:** If the prospect replies via SMS to Touch 1, 3, or 4 (e.g., *"Can we talk Thursday?"* or *"How much without the warranty?"*), the sequence pauses automatically and routes the reply to `Prompt 4.4` (Amber Gate).
- [ ] **5. Live Pre-Send CRM Stage Re-Check:** Never rely solely on a 14-day sleep timer. Before every single touch executes, perform a live `GET /deals/{{deal_id}}` API read and verify `deal_stage == "QUOTE_SENT_OPEN"`.

**Quoting & Nurture Engine Approved By:** `[OWNER_OR_SALES_LEAD]`  
**Business Name:** `[BUSINESS_NAME]`  
**Verified Margin Floor:** `[MIN_GROSS_MARGIN_PCT]%` \| **Sign-Off Date:** `[SIGN_OFF_DATE]`  
