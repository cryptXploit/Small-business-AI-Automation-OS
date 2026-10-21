# Worksheet 6: Support Knowledge Base & Escalation Rules Matrix

**Companion to:** Chapter 6 — *24/7 AI Customer Support Triage, FAQ Resolution & Smart Escalation*  
**Framework Reference:** *The 3-Tier Support Shield (Grounded Single-Source Knowledge Base -> Tier 1 Green-Zone Autonomous Resolution -> Tier 2 Amber-Zone Assisted Drafts -> Tier 3 Red-Zone Urgent VIP & Safety Takeover)*  
**Department Engine:** `Dept 03 — Customer Experience & 24/7 Support Triage`  
**Estimated Completion Time:** 60 Minutes  
**Interactive Companion:** Pre-configured inside the Notion Small Business OS (`06-NOTION-TEMPLATES/`) and the Pro Web App Suite (`07-INTERACTIVE-TOOLS/index.html` — Access Code: `SMALLBIZ-OS-PRO-2026`).

---

## Instructions for the Owner & Support Manager

An AI customer support system is only as safe and accurate as the **Single-Source Knowledge Base** it reads from and the **Deterministic Escalation Boundaries** that govern when it must hand the conversation to a human. When small businesses deploy generic chatbots without strict policy grounding, they suffer two opposite failures: either the bot gives vague, unhelpful answers that frustrate buyers, or it invents unauthorized refund promises and scheduling exceptions.

Use this 5-part operational workbook to audit your **Top 25 Repetitive Customer Inquiries**, codify your **Single-Source Policy & Refund Boundary Sheet**, configure your **Tier 1 / Tier 2 / Tier 3 Routing Rules Matrix**, establish your **Red-Zone Escalation Trigger Keyword Registry**, and institute a **15-Minute Weekly AI Support Accuracy Audit Log**.

---

## Part 1: Top 25 Repetitive Customer Inquiry Audit Table (`Prompt 6.1`)

Export your last 90 days of sent emails, SMS replies, social DMs, and support tickets, and run them through `Prompt 6.1` (*Raw Ticket/Email History to Structured Support Knowledge-Base Compiler*). Record your highest-volume inquiry categories below to identify the 60% to 75% of tickets eligible for **Tier 1 Green-Zone Autonomous Resolution**.

| Policy Chunk ID | Inquiry Category & Exact Customer Question Pattern | Monthly Ticket Volume | Current Avg Human Time per Ticket | Required Live Data Lookup (Read-Only API) | Assigned Shield Tier (`Tier 1 / 2 / 3`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `KB-ORD-01` | **Order / Shipment Status:** *"Where is my order / When will my package arrive?"* | `______ / mo` | `4.5 mins` | Shopify / WooCommerce / ShipStation Tracking API | **Tier 1 (Green)** |
| `KB-SCH-01` | **Appointment Rescheduling (> 24h Notice):** *"Can I move my appointment to next week?"* | `______ / mo` | `6.0 mins` | Calendly / HighLevel / Jobber Booking Link | **Tier 1 (Green)** |
| `KB-HRS-01` | **Hours, Location, Parking & Service Area:** *"Are you open Saturday? Do you serve my ZIP?"* | `______ / mo` | `3.0 mins` | Static Policy Chunk `KB-HRS-01` + ZIP Table | **Tier 1 (Green)** |
| `KB-PRP-01` | **Pre-Visit / Product Usage Instructions:** *"How do I prepare for my visit / use this item?"* | `______ / mo` | `5.0 mins` | Static Policy Chunk `KB-PRP-01` | **Tier 1 (Green)** |
| `KB-INV-01` | **Duplicate Receipt / Invoice Copy Request:** *"Can you send me a paid receipt for tax/insurance?"* | `______ / mo` | `5.5 mins` | Stripe / QuickBooks / Xero Invoice PDF URL | **Tier 1 (Green)** |
| `KB-SIZ-01` | **Product Sizing / Compatibility / Spec Check:** *"Will part X fit model Y? Which size fits me?"* | `______ / mo` | `6.0 mins` | Approved Compatibility Matrix `KB-SIZ-01` | **Tier 1 (Green)** |
| `KB-RET-01` | **Standard Return / Exchange Within Policy Window:** *"How do I return an unopened item (< 30 days)?"* | `______ / mo` | `5.0 mins` | Order Date Check + Return Portal URL | **Tier 1 (Green)** |
| `KB-RET-02` | **Goodwill Credit / Late Return / Damaged Item (< `$75`):** *"Item arrived scratched / 5 days past window"* | `______ / mo` | `9.0 mins` | Order History + Photo Attachment Check | **Tier 2 (Amber)** |
| `KB-SCH-02` | **Late Cancellation / Same-Day Reschedule Fee Waiver:** *"Something came up today, can you waive the fee?"* | `______ / mo` | `8.0 mins` | CRM Customer LTV + Past Attendance Count | **Tier 2 (Amber)** |
| `KB-TEC-01` | **Multi-Step Technical Troubleshooting:** *"I followed the guide and still get error code E-04"* | `______ / mo` | `12.0 mins` | Technical SOP `KB-TEC-01` + Ticket History | **Tier 2 (Amber)** |
| `KB-BIL-01` | **Billing Dispute / Double Charge / High Refund (`>= $75`):** *"You charged my card twice / I want a full refund"* | `______ / mo` | `15.0 mins` | Stripe / QBO Ledger + CRM Timeline | **Tier 3 (Red)** |
| `KB-VIP-01` | **Angry Sentiment (`< -0.50`) / Legal / Safety / Property Damage:** *"Your crew broke my pipe / calling my lawyer"* | `______ / mo` | `25.0 mins` | Full Account Dossier + Immediate Bot Pause | **Tier 3 (Red)** |
| `KB-CUS-01` | `_______________________________________________________` | `______ / mo` | `____ mins` | `___________________________` | `Tier ___` |
| `KB-CUS-02` | `_______________________________________________________` | `______ / mo` | `____ mins` | `___________________________` | `Tier ___` |
| `KB-CUS-03` | `_______________________________________________________` | `______ / mo` | `____ mins` | `___________________________` | `Tier ___` |
| `KB-CUS-04` | `_______________________________________________________` | `______ / mo` | `____ mins` | `___________________________` | `Tier ___` |
| `KB-CUS-05` | `_______________________________________________________` | `______ / mo` | `____ mins` | `___________________________` | `Tier ___` |

---

## Part 2: Single-Source Policy & Refund Boundary Sheet

Fill in the exact numeric and operational rules below. These exact figures are injected into your **Single-Source Knowledge Base (`02-ARCHITECTURE/` / Notion KB)** so `Prompt 6.3` and `Prompt 6.4` never guess or improvise company policy.

### 2.1 Financial, Return & Cancellation Boundaries

| Policy Parameter | Exact Deterministic Rule / Numeric Boundary | Tier 1 Autonomous Authority | Tier 2 Staff One-Click Authority | Tier 3 Owner-Only Authority |
| :--- | :--- | :--- | :--- | :--- |
| **Standard Return / Refund Window** | `____` Calendar Days from delivery/purchase | Share return portal link if `< ____ days` & unopened | Approve up to `____` days grace period | Any exception beyond `____` days |
| **Monetary Refund / Credit Cap** | Max automated goodwill credit = `$0.00` | `$0.00` (Zero autonomous cash refunds) | `$0.01` to `$________` (e.g., `$75.00`) | Above `$________` (e.g., `> $75.00`) |
| **Replacement / Re-Ship Authority** | Verified carrier lost/damaged with photo | Collect photo & tracking number | One-click replacement up to `$________` COGS | Replacement above `$________` COGS |
| **Appointment Reschedule Notice** | Minimum `____` hours advance notice required | Self-serve reschedule link if `>= ____ hrs` | Waive late fee once if customer LTV `>= $______` | Repeat no-shows or VIP disputes |
| **Service Warranty / Redo Window** | Workmanship covered for `____` days post-service | Provide warranty terms & photo upload link | Schedule warranty tech check + draft reply | Third-party damage or cash claim |
| **Price-Match / Promo Retroactivity** | Within `____` days of purchase | Explain policy rules only | Issue store credit up to `$________` | Cash price adjustment |

### 2.2 Canonical Markdown Knowledge Chunk Template

Every entry in your Single-Source Knowledge Base must follow this exact 6-field structure so retrieval accuracy exceeds `98%`:

```markdown
### Policy Chunk ID: [KB-CATEGORY-NUMBER]
- **Title:** [Clear, specific policy name]
- **Last Verified Date:** [YYYY-MM-DD] | **Policy Owner:** [Role/Name]
- **Customer Question Triggers:** [3–5 common ways customers phrase this question]
- **Exact Approved Policy Answer:** [Crystal-clear, factual explanation with exact numbers, timeframes, and URLs]
- **Hard Exceptions & Boundaries:** [What is strictly NOT allowed under this policy]
- **Escalation Rule:** [When the AI must route this inquiry to Tier 2 Amber or Tier 3 Red]
```

---

## Part 3: The 3-Tier Support Shield Triage Rules Matrix (`Prompt 6.2`)

Configure your automation router (Make / Zapier / n8n / HelpScout / Gorgias / Front / HighLevel) using the deterministic conditions below:

| Routing Dimension | Tier 1: Green Zone (Autonomous Instant Reply) | Tier 2: Amber Zone (AI Draft + Staff 1-Click Approval) | Tier 3: Red Zone (Bot Suppression + Manager Alert) |
| :--- | :--- | :--- | :--- |
| **Target Share of Volume** | **60% – 75%** of all inbound messages | **20% – 30%** of all inbound messages | **5% – 10%** of all inbound messages |
| **Target Response SLA** | **`< 30 Seconds`** (24/7/365) | **`< 2 Business Hours`** | **`< 15 Minutes`** (Immediate SMS/Slack Alert) |
| **AI Confidence Score (`0.00–1.00`)** | `confidence_score >= 0.90` AND valid `policy_chunk_id` cited | `0.65 <= confidence_score < 0.90` OR multi-policy synthesis | Any confidence score when Red-Zone trigger is present |
| **Customer Sentiment Score (`-1.0` to `+1.0`)** | `sentiment_score >= -0.15` (Neutral to Positive) | `-0.50 <= sentiment_score < -0.15` (Mild frustration/urgency) | **`sentiment_score < -0.50`** (High anger/hostility) |
| **Financial / Refund Exposure** | **`$0.00`** (Informational / status / self-serve link only) | **`$0.01` to `$75.00`** (Or within Tier 2 staff cap) | **`> $75.00`**, chargeback threat, or disputed invoice |
| **AI Action Executed** | Sends grounded reply via `Prompt 6.3` + logs resolution in CRM | Posts internal Context Whisper + Draft Reply (`Prompt 6.4`) to Slack/Helpdesk | Immediately sets `ai_auto_reply = FALSE` + generates Executive Recovery Brief (`Prompt 6.5`) |
| **Human Escape Hatch** | Every Tier 1 message includes footer: *"Reply HUMAN anytime to speak with our team."* | Staff clicks `[Approve & Send]`, `[Edit Reply]`, or `[Escalate]` | Owner or Manager calls/emails customer directly using 3-option recovery brief |

---

## Part 4: Red-Zone Escalation Trigger Keyword & Pattern Registry

Your pre-AI deterministic router must scan every inbound email, SMS, chat message, and social DM against the **Red-Zone Keyword & Pattern Registry** below. If **any** pattern matches, the ticket bypasses Tier 1 and Tier 2 immediately and triggers **Tier 3 Red-Zone Takeover**.

### 4.1 Mandatory Universal Red-Zone Triggers

- [ ] **Category A — Legal, Regulatory & Chargeback Threats:**  
  `lawyer`, `attorney`, `lawsuit`, `small claims`, `sue`, `legal action`, `chargeback`, `dispute the charge`, `fraud`, `unauthorized charge`, `Better Business Bureau`, `BBB`, `Attorney General`, `FTC`, `trading standards`, `ombudsman`, `licensing board`, `health department`, `OSHA`.
- [ ] **Category B — Physical Safety, Injury, Illness & Property Damage:**  
  `injured`, `hurt`, `bleeding`, `hospital`, `urgent care`, `allergic reaction`, `rash`, `chemical burn`, `swelling`, `smoke`, `sparks`, `burning smell`, `gas leak`, `carbon monoxide`, `flooding`, `burst pipe`, `water damage`, `property damage`, `broke my`, `ruined my`.
- [ ] **Category C — Public Reputation & Viral Escalation Threats:**  
  `1-star`, `one star`, `worst company`, `scam`, `rip-off`, `posting on Google`, `Yelp review`, `Reddit`, `TikTok`, `local news`, `warn everyone`.
- [ ] **Category D — Human Override & Bot Frustration Signals:**  
  `HUMAN`, `AGENT`, `MANAGER`, `OWNER`, `SUPERVISOR`, `real person`, `stop messaging me`, `stupid bot`, `talk to a human`, or `>= 3` consecutive customer replies within 10 minutes without resolution.
- [ ] **Category E — VIP & High-Value Account Protection:**  
  `customer_lifetime_value >= $________` OR `account_tag == "VIP"` OR `open_deal_value >= $________` combined with any negative sentiment (`sentiment_score < 0.0`).

### 4.2 Custom Industry Red-Zone Keywords for Your Business

Write 5 to 10 industry-specific emergency or high-risk words that should immediately trigger Tier 3 human takeover in your business:
1. `___________________________` (e.g., *"no heat"*, *"website down"*, *"crown fell out"*, *"payroll failed"*)
2. `___________________________`
3. `___________________________`
4. `___________________________`
5. `___________________________`
6. `___________________________`

---

## Part 5: Weekly AI Support Accuracy Audit Log (15-Minute Friday Ritual)

Every Friday afternoon, the Support Lead or Owner spends 15 minutes reviewing a random sample of **10 Tier-1 Auto-Resolved Tickets** and **all Tier-2 Human-Edited Drafts** from the past 7 days. Every time a staff member had to edit a Tier-2 AI draft because a policy detail was missing from the Knowledge Base, add that missing rule to your Single-Source KB so the AI gets smarter every week.

| Week Ending Date | Total Inbound Tickets | Tier 1 Auto-Resolved (`#` / `%`) | Tier 2 Assisted (`#` / `%`) | Tier 3 Escalated (`#` / `%`) | Tier 1 Fact-Check Accuracy (`10-Ticket Audit`) | New / Updated KB Policy Chunks Added This Week | Support CSAT Score (`%` or `/5.0`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline (Pre-OS)** | `______` | `0 (0%)` | `0 (0%)` | `100% Manual` | `N/A` | `Initial 25 Chunks Compiled` | `______` |
| **Week 1:** `____/____` | `______` | `____ (___%)` | `____ (___%)` | `____ (___%)` | `____ / 10 (___%)` | `Chunk IDs: ___________________` | `______` |
| **Week 2:** `____/____` | `______` | `____ (___%)` | `____ (___%)` | `____ (___%)` | `____ / 10 (___%)` | `Chunk IDs: ___________________` | `______` |
| **Week 3:** `____/____` | `______` | `____ (___%)` | `____ (___%)` | `____ (___%)` | `____ / 10 (___%)` | `Chunk IDs: ___________________` | `______` |
| **Week 4:** `____/____` | `______` | `____ (___%)` | `____ (___%)` | `____ (___%)` | `____ / 10 (___%)` | `Chunk IDs: ___________________` | `______` |
| **Week 8:** `____/____` | `______` | `____ (___%)` | `____ (___%)` | `____ (___%)` | `____ / 10 (___%)` | `Chunk IDs: ___________________` | `______` |
| **Target Benchmark** | *All Channels* | **`60% – 75%`** | **`20% – 30%`** | **`5% – 10%`** | **`10 / 10 (100%)`** | *+2 to 4 Chunks / Week* | **`>= 95.0%`** |

### Support Shield Deployment Sign-Off

- **Single-Source Knowledge Base Populated (`>= 25` Verified Policy Chunks):** `[ ] Verified Live`
- **Red-Zone Keyword & Sentiment (`< -0.50`) Suppression Gate Active:** `[ ] Verified Live`
- **Prompts `6.1` through `6.5` Connected to Helpdesk / Inbox Router:** `[ ] Verified Live`
- **Sign-Off Date:** `____ / ____ / 2026` | **Owner / Support Lead Signature:** `___________________________`
