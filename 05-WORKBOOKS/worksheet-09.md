# Worksheet 9: Team Delegation & SOP Standardization Canvas

**Companion to:** Chapter 9 — *Internal Team SOPs, Meeting Synthesis & Instant Staff Training Systems*  
**Framework Reference:** *The Living SOP & Voice-to-Checklist Delegation Engine (5-Minute Loom/Voice Capture -> 7-Block Living SOP Compiler -> Internal "Ask-the-SOP" Staff Assistant -> Zero-Drift Meeting Synthesis -> 7-Day New-Hire Certification)*  
**Department Engine:** `Dept 05 — Internal Team SOPs, Delegation & Training`  
**Estimated Completion Time:** 45 Minutes  
**Interactive Companion:** Pre-configured inside the Notion Small Business OS (`06-NOTION-TEMPLATES/`) and the Pro Web App Suite (`07-INTERACTIVE-TOOLS/index.html` — Access Code: `SMALLBIZ-OS-PRO-2026`).

---

## Instructions for the Owner & Operations Manager

The reason most small business owners work 55 to 65 hours a week is not because their employees are lazy—it is because **the company's operating manual lives exclusively inside the owner's head**. Every time a staff member has to knock on your door, call your cell phone from a job site, or message you on Slack to ask *"How do we handle a partial refund?"*, *"Where is the vendor login?"*, or *"What's the checklist for closing the clinic on Friday?"*, your deep-work focus is shattered. Worse, when you ask managers to "write SOPs," nothing gets written because sitting down at a blank document to type step-by-step manuals takes hours nobody has.

Chapter 9 solves this permanently: **you never type an SOP from scratch again**. You simply record a 3-minute screen share (Loom) or voice memo while performing the task once, and `Prompt 9.1` compiles it into a standardized **7-Block Living SOP** indexed inside your internal **"Ask-the-SOP" Staff Bot (`Prompt 9.4`)**. Use this 5-part workbook to prioritize the first 15 tasks you will extract from your head, standardize your 7-Block SOP format, structure voice-to-task delegations, index your staff Q&A vault, and certify new hires in 7 days.

---

## Part 1: Owner Task Delegation & SOP Priority Inventory

List the top 10 to 15 recurring operational tasks or staff questions that currently interrupt your week or require your personal intervention. Score each task to identify your **First 5 Recordings** this week (tasks that take 3 minutes to record and immediately save 1 to 3 hours every single week).

| SOP ID | Recurring Task or Frequent Staff Question | Dept (`01–05`) | Frequency (`Daily / Weekly / Monthly`) | Mins Per Occurrence | Weekly Owner/Lead Time Drained | Target Delegate Role | 3-Min Loom / Voice Recorded? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SOP-01-01` | **Missed-Call & Amber Lead Triage:** How front desk reviews and approves custom quote requests | `Dept 01` | Daily (`5x/wk`) | `15 mins` | `75 mins/wk` | Front Desk / Intake Coord | `[ ] Recorded [ ] Approved` |
| `SOP-02-01` | **3-Tier Proposal Setup & Margin Check:** Generating Core/Pro/Complete quotes from discovery notes | `Dept 02` | Daily (`5x/wk`) | `20 mins` | `100 mins/wk` | Sales Rep / Estimator | `[ ] Recorded [ ] Approved` |
| `SOP-03-01` | **New Client Kickoff & Folder Provisioning:** Verifying Gate A assets and posting the Delivery Brief | `Dept 03` | `3–5x / week` | `20 mins` | `80 mins/wk` | Project / Dispatch Coord | `[ ] Recorded [ ] Approved` |
| `SOP-03-02` | **Tier 2 Support Refund & Replacement Approval:** Reviewing photo proof and issuing replacements `< $75` | `Dept 03` | Daily (`5x/wk`) | `15 mins` | `75 mins/wk` | Support Specialist | `[ ] Recorded [ ] Approved` |
| `SOP-03-03` | **Opening / Closing Shop, Clinic, or Truck Inspection:** Daily readiness and safety sign-off checklist | `Dept 03` | Daily (`5–6x/wk`) | `15 mins` | `90 mins/wk` | Lead Tech / Shift Lead | `[ ] Recorded [ ] Approved` |
| `SOP-04-01` | **Completed Job Invoice Dispatch & AR Check:** Formatting job notes into QBO/Stripe invoice line items | `Dept 04` | Daily (`5x/wk`) | `15 mins` | `75 mins/wk` | Billing / Office Admin | `[ ] Recorded [ ] Approved` |
| `SOP-04-02` | **Vendor Bill OCR & Price-Creep Review:** Approving staged bills and flagging `> 5%` price hikes | `Dept 04` | Weekly (`Fri`) | `30 mins` | `30 mins/wk` | Bookkeeper / Office Mgr | `[ ] Recorded [ ] Approved` |
| `SOP-05-01` | **Friday 2:30 PM KPI Data Prep:** Checking exceptions before the 3:00 PM Owner Scorecard runs | `Dept 05` | Weekly (`Fri`) | `20 mins` | `20 mins/wk` | Operations Lead | `[ ] Recorded [ ] Approved` |
| `SOP-CUS-01` | `_______________________________________________________` | `Dept __` | `____________` | `____ mins` | `____ mins/wk` | `___________________` | `[ ] Recorded [ ] Approved` |
| `SOP-CUS-02` | `_______________________________________________________` | `Dept __` | `____________` | `____ mins` | `____ mins/wk` | `___________________` | `[ ] Recorded [ ] Approved` |
| `SOP-CUS-03` | `_______________________________________________________` | `Dept __` | `____________` | `____ mins` | `____ mins/wk` | `___________________` | `[ ] Recorded [ ] Approved` |
| `SOP-CUS-04` | `_______________________________________________________` | `Dept __` | `____________` | `____ mins` | `____ mins/wk` | `___________________` | `[ ] Recorded [ ] Approved` |

---

## Part 2: The 7-Block Living SOP Authoring Template (`Prompt 9.1`)

Whenever you or a senior team member record a 3-to-5-minute Loom screen share or voice memo explaining how to perform a task, pass the raw transcript into `Prompt 9.1`. Every SOP stored in your company vault (`06-NOTION-TEMPLATES/` or `12-EDITABLE-OFFICE-SUITE/Word-Docs/`) must conform to this exact **7-Block Living SOP Standard**:

```markdown
================================================================================
STANDARD OPERATING PROCEDURE (7-BLOCK LIVING SOP STANDARD)
SOP ID: {{sop_id}} | Title: {{sop_title}}
Department: {{department}} | Role Owner: {{assigned_role}}
Effective Date: {{date_iso}} | Version: {{version_number}} | Video Link: {{loom_url}}
================================================================================

BLOCK 1: PURPOSE & OPERATIONAL OUTCOME (WHY THIS MATTERS)
- Objective: {{one_sentence_objective}}
- Business Impact if Skipped: {{consequence_of_failure}}
- Target Completion Time: {{estimated_minutes}} Minutes

BLOCK 2: EXACT TRIGGER & TIMING SLA (WHEN TO RUN THIS)
- Trigger Event: {{exact_webhook_status_or_schedule_trigger}}
- Mandatory SLA Window: Must be completed within {{sla_window}} of trigger.

BLOCK 3: REQUIRED TOOLS, LOGINS & PRE-FLIGHT INPUTS
- Software / Systems Needed: {{systems_and_permission_level}}
- Required Inputs Before Starting:
  [ ] 1. {{prerequisite_input_1}}
  [ ] 2. {{prerequisite_input_2}}

BLOCK 4: STEP-BY-STEP EXECUTION CHECKLIST (HOW TO DO IT)
- [ ] Step 1 ({{action_verb_header_1}}): {{exact_clicks_fields_and_actions_1}}
- [ ] Step 2 ({{action_verb_header_2}}): {{exact_clicks_fields_and_actions_2}}
- [ ] Step 3 ({{action_verb_header_3}}): {{exact_clicks_fields_and_actions_3}}
- [ ] Step 4 ({{action_verb_header_4}}): {{exact_clicks_fields_and_actions_4}}
- [ ] Step 5 ({{action_verb_header_5}}): {{exact_clicks_fields_and_actions_5}}

BLOCK 5: QUANTIFIED "DEFINITION OF DONE" (QUALITY VERIFICATION GATE)
This task is NOT complete until all 3 verification checks below are true:
- [ ] QA Check 1: {{measurable_output_check_1}}
- [ ] QA Check 2: {{measurable_output_check_2}}
- [ ] QA Check 3: {{status_updated_and_logged_check_3}}

BLOCK 6: COMMON EDGE CASES & DECISION BOUNDARIES (IF X, DO Y)
- Scenario A ({{edge_case_a}}): {{exact_approved_handling_a}}
- Scenario B ({{edge_case_b}}): {{exact_approved_handling_b}}

BLOCK 7: AMBER / RED ESCALATION BOUNDARY (WHEN TO STOP & ASK)
- Escalate Immediately To: {{escalation_role_and_channel}}
- Hard Stop Conditions: Stop and escalate if dollar impact exceeds ${{dollar_cap}},
  customer sentiment is hostile, or required data is missing after 2 attempts.
================================================================================
```

---

## Part 3: Voice-to-Checklist Ad-Hoc Delegation Contract (`Prompt 9.2`)

Even with a complete SOP library, owners frequently need to delegate one-off projects or custom client requests on the fly. Instead of sending vague 1-line Slack messages (*"Hey Sam, can you take care of the Miller account update?"*) that result in misunderstandings, record a 45-second voice note and run it through `Prompt 9.2` to generate a **5-Point Delegation Contract**:

| Delegation Element | Bad Ad-Hoc Delegation (Causes Rework) | Studio Voice-to-Checklist Standard (`Prompt 9.2` Output) | Verified in Task Card? |
| :--- | :--- | :--- | :--- |
| **1. Single Named Owner** | *"Can somebody in the back check on the parts order?"* | **Assigned To:** `@Marcus_T` (One primary human owner per task—never a group) | `[ ] Yes` |
| **2. Binary Deliverable** | *"Work on the Q4 client renewal deck"* | **Deliverable:** 8-slide renewal PDF saved in `Drive/Client_X/04-Deliverables` | `[ ] Yes` |
| **3. Hard Deadline & Time** | *"Get this done soon / when you have a chance"* | **Due By:** `Thursday, Oct 29 at 2:00 PM CT` | `[ ] Yes` |
| **4. Decision Authority Tier** | Staff doesn't know if they should act or ask first | **Authority Level:** `[ ] Level 1: Research & Recommend` `[ ] Level 2: Draft & Amber Gate` `[ ] Level 3: Execute & Report` | `[ ] Yes` |
| **5. Definition of Done (QA)** | Staff says *"Done!"* when only half the steps are finished | **Definition of Done:** 3-item checkbox list that must be checked before marking complete | `[ ] Yes` |

---

## Part 4: Internal "Ask-the-SOP" Staff Bot Governance Rules (`Prompt 9.4`)

To cut internal staff interruptions by **70% to 80%**, establish the **"SOP Bot First" Cultural Rule** across your team. Before any team member messages the Owner or Operations Manager with a *"How do I...?"* question, they ask your internal `#ask-the-sop` Slack/Teams/Web assistant (`Prompt 9.4`):

- [ ] **Rule 1 — Closed-World SOP Grounding (`temperature: 0.0`):** The internal staff bot answers *exclusively* from your approved 7-Block Living SOP folder and Single-Source Policy KB. It must cite the exact `SOP-ID` and step number in every reply.
- [ ] **Rule 2 — Zero Guessing on Unindexed Questions:** If a staff member asks a question that is not covered in any existing SOP (`confidence < 0.90`), the bot is forbidden from improvising. Instead, it replies: *"No verified SOP covers this scenario yet. I have tagged `{{department_lead}}` to provide the official rule and auto-create a new SOP."*
- [ ] **Rule 3 — The 60-Second Voice-Note Self-Healing Loop:** When the bot tags the Owner or Manager on an unindexed question, the Owner replies right in the thread with a **60-second voice note**. The automation transcribes the voice note, runs `Prompt 9.1` to generate a new 7-Block SOP draft, and adds it to the vault—ensuring the owner **never answers the same staff question twice**.

---

## Part 5: 7-Day New-Hire Role Certification & Ramp-Up Tracker (`Prompt 9.5`)

When you hire a new front-desk coordinator, technician, support rep, or account manager, use `Prompt 9.5` to generate a structured **7-Day Role Certification Curriculum** from the 8 to 12 Living SOPs assigned to their role. Track their certification below:

| Onboarding Day | Assigned Living SOPs (`SOP-IDs`) | Loom Video + 7-Block SOP Studied? | `Prompt 9.5` Scenario Quiz Score (`Pass >= 90%`) | Supervised Shadow Execution (`3 Real Tasks Verified`) | Manager Sign-Off & Certification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Day 1: Core Systems & Safety** | `SOP-____`, `SOP-____` | `[ ] Complete` | `____ / 100%` | `[ ] Task 1 [ ] Task 2 [ ] Task 3` | Initials: `______` |
| **Day 2: Daily Frontline Tasks** | `SOP-____`, `SOP-____` | `[ ] Complete` | `____ / 100%` | `[ ] Task 1 [ ] Task 2 [ ] Task 3` | Initials: `______` |
| **Day 3: Customer Handoffs** | `SOP-____`, `SOP-____` | `[ ] Complete` | `____ / 100%` | `[ ] Task 1 [ ] Task 2 [ ] Task 3` | Initials: `______` |
| **Day 4: Exceptions & Amber Gates** | `SOP-____`, `SOP-____` | `[ ] Complete` | `____ / 100%` | `[ ] Task 1 [ ] Task 2 [ ] Task 3` | Initials: `______` |
| **Day 5: Back-Office & Reporting** | `SOP-____`, `SOP-____` | `[ ] Complete` | `____ / 100%` | `[ ] Task 1 [ ] Task 2 [ ] Task 3` | Initials: `______` |
| **Day 6–7: Full Solo Sprint & QA** | *All Role SOPs Combined* | `[ ] Complete` | `____ / 100%` | `10 Consecutive Tasks at 100% QA` | **Certified:** `[ ] YES` |

### Team SOP & Delegation Engine Sign-Off

- **Top 10 High-Drain Owner Tasks Recorded & Compiled via `Prompt 9.1`:** `[ ] Verified Live`
- **Internal `#ask-the-sop` Staff Assistant Deployed (`Prompt 9.4`):** `[ ] Verified Live`
- **Daily Huddle / Meeting Synthesis Connected to Task Board (`Prompt 9.3`):** `[ ] Verified Live`
- **Sign-Off Date:** `____ / ____ / 2026` | **Owner / Ops Manager Signature:** `___________________________`
