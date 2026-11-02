# FREE AUTOMATION 1-CLICK TEST GUIDE: 60-SECOND INSTANT LEAD ROUTER
**The Small Business AI Automation Operating System — Free Tier 0 Automation Pack**
**Author:** OMAR SUNNY

---

## 1. OVERVIEW: YOUR FIRST PRODUCTION AUTOMATION

Inside this folder is `01-60s-instant-lead-router-and-sms-intake.json`, an export-ready workflow blueprint designed to deploy on **Make.com**, **n8n**, or **Zapier**.

### Core Problem It Solves
The average small service business takes 42 minutes to respond to a new web inquiry. If response time exceeds 5 minutes, qualification likelihood drops by 80%. This automation receives any new web lead, enriches the contact, checks for VIP priority, triggers an instant SMS confirmation to the prospect, and pings the business owner in under 45 seconds.

---

## 2. 3-MINUTE IMPORT & DEPLOYMENT INSTRUCTIONS

### Option A: Import into Make.com (Recommended)
1. Log in to your [Make.com](https://make.com) account.
2. In your dashboard, click **`Create a new scenario`**.
3. In the canvas controls at the bottom, click the **`...` (More)** icon.
4. Select **`Import Blueprint`**.
5. Upload `01-60s-instant-lead-router-and-sms-intake.json` from this folder.
6. Make will immediately build out the complete 5-module scenario:
   - `Module 1: Custom Webhook Listener`
   - `Module 2: JSON Payload Parser & Data Validator`
   - `Module 3: CRM Record Creator (Google Sheets / Notion)`
   - `Module 4: Twilio / SMS First-Touch Dispatcher`
   - `Module 5: Slack / WhatsApp Executive Alert Router`
7. Click your Webhook module to copy your dedicated live Webhook URL.
8. Toggle scenario status to **`ON`**.

### Option B: Import into Self-Hosted n8n
1. Open your n8n workspace.
2. Click **`Add Workflow`** > **`... (Workflow Menu)`** > **`Import from File`**.
3. Select `01-60s-instant-lead-router-and-sms-intake.json`.
4. Connect your credential nodes for SMS and CRM.
5. Save and activate.

---

## 3. 1-CLICK WEBHOOK TESTING PROCEDURE

To test your new automation without changing your live website:

1. Copy your Webhook URL from Module 1.
2. Open your terminal or a browser testing tool (like Postman or curl):
   ```bash
   curl -X POST "YOUR_WEBHOOK_URL" \
     -H "Content-Type: application/json" \
     -d '{
       "lead_name": "Test Prospect",
       "phone": "+15550192834",
       "service_requested": "Emergency HVAC Repair",
       "urgency": "High"
     }'
   ```
3. Watch the scenario execute in real-time. Within 15 seconds, a formatted SMS and internal alert will fire.

---

## 4. ARCHITECTURE OVERVIEW: BLUEPRINT #1 FLOW

```
[Inbound Form / Ad Lead]
           |
           v
[Webhook Ingestion Node]
           |
    +------+------+
    |             |
    v             v
[Twilio SMS]  [CRM Logger]
    |             |
    +------+------+
           |
           v
[Owner Mobile Alert (<60s SLA)]
```

---

## 5. COMPLETE AUTOMATION SUITE: BLUEPRINTS #2–#5 (TIER 3 EXCLUSIVE)

In this Free Starter Pack, you have Blueprint #1. In the **Tier 3 Flagship OS ($59)**, you receive all 5 production automation blueprints with pre-built error handlers and fallback routes:

### Blueprint #2: AI Support Triage & Amber Approval Gate
- Automatically reads incoming support emails via OpenAI/Anthropic.
- Tags sentiment, urgency, and category.
- If confidence score > 90%, drafts professional response; if under 90%, routes to Amber Approval Queue for human sign-off.

### Blueprint #3: 3-Option Instant Quote & 14-Day Nurture Follow-up
- Receives scope variables and computes Good / Better / Best pricing tiers.
- Generates dynamic PDF proposal.
- Triggers 3-stage email/SMS follow-up sequence over 14 days until signed.

### Blueprint #4: Overdue Invoice 5-Stage Payment Chaser
- Syncs with QuickBooks / Xero / Stripe daily at 9:00 AM.
- Identifies overdue invoices past Day +1, Day +7, Day +14, Day +21, and Day +30.
- Automatically sends polite to firm escalation notices, reducing DSO by up to 35%.

### Blueprint #5: Friday 3:00 PM Owner KPI Executive Digest
- Gathers closed deals, cash collected, open support tickets, and system error rates.
- Synthesizes an executive markdown summary sent directly to the owner's mobile.

---

## 6. UPGRADE TO COMPLETE FLAGSHIP OS

Unlock all 5 production automation blueprints with plug-and-play JSON files, setup guides, and video walk-throughs:
- **Tier 3 Flagship OS ($59):** Instant access at your Gumroad portal or use code `STUDIO-PRO-OS-2026`.
