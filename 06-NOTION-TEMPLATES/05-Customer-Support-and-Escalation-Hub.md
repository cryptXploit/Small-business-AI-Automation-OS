# Database 05: Customer Support, RAG Knowledge Base & Red-Gate Escalation Hub

**Database File:** `06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.csv`  
**Linked Chapters:** Chapter 2 (*T.R.A.V. Safety Architecture*), Chapter 6 (*24/7 AI Customer Support & Triage*), Chapter 7 (*Reputation & Retention*), and Back Matter Part II (*12 Emergency Scripts*)  
**Governance Standard:** Closed-World Grounded RAG (`temperature: 0.0–0.1` | Minimum Autonomous Confidence Floor: `0.85`)  

---

## 1. Architectural Purpose of the Support & Escalation Hub

In a 1-to-25 person business, customer support and exception handling typically suffer from two opposite failure modes:
1. **The Manual Bottleneck Trap:** The founder or front-desk coordinator personally types out repetitive answers to the same 25 routine questions (*"Where do I park?"*, *"Can I move my Tuesday appointment?"*, *"Can you resend Invoice #4418?"*, *"Do you take Delta Dental PPO?"*) 40 times a week, interrupting high-value fulfillment and sales work.
2. **The Reckless Bot Trap:** The business installs an ungrounded website widget that invents unauthorized discounts, quotes inaccurate service pricing, or replies cheerfully to a furious customer threatening a lawsuit or regulatory complaint.

**Database 05 (`05-Customer-Support-and-Escalation-Hub`)** eliminates both failure modes by acting as the **Single Source of Grounded Policy Truth** for your Make.com, n8n, or Zapier support triage pipeline (`Prompts 6.1` through `6.5`). Every row in this database defines:
- What the AI is explicitly permitted to state and execute autonomously in **Tier 1 (`Green Zone`)**.
- What the AI must draft and hold for a 15-second human thumb-approval in **Tier 2 (`Amber Zone`)**.
- What the system must immediately intercept, silence automation on (`client.automation_hold = TRUE`), and route to a human leader in **Tier 3 (`Red Zone`)**.

---

## 2. The 3-Tier Triage & Sentiment Routing Matrix

Every inbound customer email, SMS, WhatsApp message, web chat, or portal ticket processed by **Prompt 6.1 (*Multi-Channel Support Ticket Intent, Sentiment & Urgency Classifier*)** is scored along three deterministic axes before any reply is generated:

### Axis 1: Customer Sentiment Score (`1` to `5`)
- **Sentiment `5 / 5` (Delighted Advocate):** Customer expresses praise, gratitude, or satisfaction. Eligible for `Tier 1 Green Auto` resolution and automatic tagging for the **Chapter 7 5-Star Review Funnel (`Prompt 7.2`)**.
- **Sentiment `4 / 5` (Positive / Cooperative):** Polite routine inquiry. Eligible for `Tier 1 Green Auto` resolution when RAG confidence is `>= 0.85`.
- **Sentiment `3 / 5` (Neutral / Matter-of-Fact):** Standard transactional request (rescheduling, invoice copy, ETA check). Eligible for `Tier 1 Green Auto` resolution when grounded policy match is exact.
- **Sentiment `2 / 5` (Frustrated / Dissatisfied):** Customer expresses annoyance, repeated delay frustration, or disappointment. **Automatic Amber/Red Intercept:** Autonomous replies are blocked; `Prompt 6.4` compiles an immediate context brief for human review.
- **Sentiment `1 / 5` (Hostile / Escalation Threat):** Profanity, threats of chargeback, 1-star public review, legal counsel, regulatory board complaint, or safety/property damage report. **Mandatory Red-Gate Lock:** Fires `Emergency Script 01` containment protocol within 60 seconds.

### Axis 2: Hard Red-Zone Regex Intercept Filter (Pre-AI Code Gate)
Before passing any inbound message to an LLM, your router executes a deterministic regular expression scan across the raw message body. If any token matches the Red-Zone pattern below, the workflow bypasses `Prompt 6.2` completely and routes straight to `#red-alerts` in Slack:

```regex
\b(lawyer|attorney|sue|lawsuit|malpractice|board complaint|bbb|better business bureau|chargeback|dispute charge|fraud|scam|police|injured|bleeding|hospital|fire|flooded|damaged my|broke my|1 star|one star|worst company|report you)\b
```

### Axis 3: Grounded Policy Confidence & Financial Ceiling (`Max_Auto_Refund_USD`)
Even when customer sentiment is `4/5` or `5/5`, an automation workflow may only dispatch an unattended response (`Tier 1 Green Zone`) when:
1. `grounded_source_row_id` matches an active `Policy_ID` (`POL-01` through `POL-21`) in Database 05.
2. `confidence_score >= 0.85` (meaning 100% of the customer's question is answered by the approved policy text without outside guessing).
3. Any financial goodwill credit or fee waiver requested is strictly `<= Max_Auto_Refund_USD` (`$0` for general FAQs; `$50` maximum for verified minor delivery/consumable delays under `POL-07`).

---

## 3. Complete Grounded Knowledge Base & Escalation Policy Reference (`POL-01` – `POL-21`)

Use the structured policy blocks below inside your Notion Knowledge Base view and sync them to your vector store or Airtable/Notion lookup step for `Prompt 6.2`.

### 3.1 Tier 1 — Autonomous Green-Gate Policies (`< 60 Seconds` Unattended Resolution)

#### `POL-01`: Business Hours, Location, Parking & Accessibility FAQ
- **Approved Grounded Facts:**
  - Operating Hours: Monday through Friday, `8:00 AM – 5:30 PM` local time; Saturday urgent/on-call dispatch `9:00 AM – 1:00 PM`.
  - Physical Location & Parking: Validated street address and suite number from company profile, with complimentary customer parking in the dedicated front lot.
  - Guardrail: Never promise walk-in availability without checking the live calendar booking link.

#### `POL-02`: Standard Appointment Rescheduling (`> 24 Hours` Advance Notice)
- **Approved Grounded Facts:**
  - Customers providing more than 24 hours advance notice may reschedule any routine consultation, maintenance visit, or project review call at zero fee.
  - Execution Rule: Verify caller/sender identity via matching phone number or email in CRM, release the original slot only after the new slot is confirmed, and provide the direct 1-click rescheduling link.

#### `POL-04`: Order Status, Shipment Tracking & Technician ETA Lookup (`WISMO`)
- **Approved Grounded Facts:**
  - Trigger `Prompt 6.3` to query the live Field Service Management (`ServiceTitan` / `Jobber` / `Housecall Pro`) or e-commerce (`Shopify` / `ShipStation`) API using the customer's verified email or phone number.
  - Return the exact job status (`Scheduled`, `En Route`, `In Progress`, `Shipped`), carrier tracking URL, and 2-hour arrival window.

#### `POL-05`: Duplicate Invoice PDF, Paid Receipt, or Company W-9 Request
- **Approved Grounded Facts:**
  - Verify that the requester's email domain matches the billing contact on file in QuickBooks Online, Xero, or Stripe.
  - Dispatch the hosted invoice/receipt URL and attach the current signed Form W-9 / GST / VAT registration certificate.

#### `POL-07`: Minor Delivery Delay Courtesy Credit (`<= $50.00` Ceiling)
- **Approved Grounded Facts:**
  - If a shipment or routine visit is delayed by more than 24 hours due to internal scheduling or carrier transit and the customer inquiries politely (`Sentiment >= 3`), the system is authorized to apply a one-time `$25.00 to $50.00` courtesy credit memo (`GL-4910 Service Goodwill`) or ship a complimentary replacement consumable, limited to once per customer per 12-month period.

---

### 3.2 Tier 2 — Human-in-the-Loop Amber-Gate Policies (`< 15 to 60 Minutes` 1-Click Approval)

#### `POL-03`: Late Cancellation or Same-Day Reschedule (`< 24 Hours` Notice)
- **Operational Rule:** Standard service agreements specify a `$50.00` late-cancellation/trip fee when a slot is cancelled within 24 hours. However, automatically charging a loyal customer who had a genuine family emergency destroys lifetime value.
- **Amber Workflow:** The AI prepares a Slack approval card (`Prompt 2.3`) showing the customer's LTV, tenure, and cancellation reason, with two 1-click buttons for the manager:
  1. **`[Waive Fee & Send VIP Reschedule Link]`** (Recommended for first-time occurrence or high-LTV client)
  2. **`[Apply $50 Late Fee & Send Reschedule Link]`** (Used for repeat no-shows)

#### `POL-06`: Insurance Benefit, Warranty & Custom Specification Inquiries
- **Operational Rule:** AI may confirm whether an insurance payer or manufacturer brand is on the company's **Approved Carrier / Brand Truth Table**, but must never state a patient's exact out-of-pocket surgical copay or approve a warranty labor claim without human verification of the policy/serial number.
- **Amber Workflow:** AI sends an instant holding reply confirming whether the carrier/brand is supported and routes the pre-populated verification ticket to the Billing Coordinator.

#### `POL-08`: Service Adjustment, Credit Memo, or Refund Request (`$51.00 – $250.00`)
- **Operational Rule:** Any financial adjustment between `$51.00` and `$250.00` requires manager 1-click approval in `#amber-approvals` (`Prompt 2.3`).

#### `POL-12`: Mid-Project Scope Creep & Paid Change-Order Boundary (`Emergency Script 05`)
- **Operational Rule:** When a client asks for extra deliverables, additional rooms/units, or out-of-scope revisions, the AI drafts **Emergency Script 05**, pairing an enthusiastic *"Yes, we can add that!"* with **Option 1 (1-Click Paid Change Order `#CO-JobID-01`)** and **Option 2 (Log in Phase 2 Backlog at $0 change to current budget)**.

#### `POL-13` & `POL-20`: Proactive Supply Delay Rescheduling & Erroneous Message Correction
- **Operational Rule:** Governed by **Emergency Script 04** (backordered part/material notification with 2 pre-held VIP slots) and **Emergency Script 07** (immediate transparent correction of any mistaken automated quote or reminder).

---

### 3.3 Tier 3 — Immediate Red-Gate Containment Protocols (`< 5 to 15 Minutes` Human Takeover)

Whenever `POL-09`, `POL-10`, `POL-11`, `POL-14`, `POL-15`, `POL-16`, `POL-17`, `POL-18`, or `POL-19` triggers, the automation pipeline executes the **3-Step Red-Gate Containment Sequence**:

1. **Step 1 — Silence All Outbound Automation (`< 2 Seconds`):**
   - Set `client.automation_hold = TRUE` and `invoice.dispute_flag = TRUE` in the CRM and accounting database.
   - This guarantees that an angry client (`Emergency Script 01`), a chargeback account (`Emergency Script 09`), or a cancelling VIP (`Emergency Script 10`) never receives an automated "How was your visit? Leave us a 5-star review!" text or an automated overdue invoice reminder while the founder is resolving the situation.
2. **Step 2 — Assemble the 60-Second Executive Context Packet (`Prompt 6.4`):**
   - Query the customer's full history (lifetime spend, open invoices, assigned technician/specialist, last 5 messages, and signed work order PDF link) and post a high-priority alert to `#red-alerts` in Slack + SMS to the escalation owner.
3. **Step 3 — Dispatch the Verified Emergency Script (`Module 4` / `Database 03`):**
   - Open `07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html` (`Module 4: 12 Emergency Ops Scripts`) or `Database 03` in Notion, populate the bracketed variables (`[CUSTOMER_NAME]`, `[COMPANY_NAME]`, `[INVOICE_NUMBER]`, `[JOB_ID]`), and send the synchronized Email and SMS response within 15 minutes.

---

## 4. Weekly Knowledge-Base Self-Healing Loop (`Prompt 6.5`)

Every Friday at 2:30 PM (30 minutes prior to the **Friday 3:00 PM Owner KPI Scorecard** review), run **Prompt 6.5 (*Weekly Unanswered Support Ticket Auditor & Knowledge-Base Gap Patcher*)** across all tickets that fell below the `0.85` confidence threshold during the week:
1. Group all Amber-escalated questions by topic cluster.
2. Identify the top 1 to 3 recurring questions that lacked a grounded row in `Database 05`.
3. Approve the AI-drafted `Approved_Policy_Summary` row in 1 click to append `POL-22`, `POL-23`, etc. directly into this Notion database.
4. Over 90 days, your Tier-1 autonomous resolution rate climbs steadily from `30%` in Week 1 to `65%–75%+` by Week 12 with zero hallucination risk.
