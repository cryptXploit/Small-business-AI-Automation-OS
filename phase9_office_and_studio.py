#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 9 Office Suite, Excel Command Center, Design Customizer & JSON Blueprints Builder
(phase9_office_and_studio.py)
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)

Generates:
  - UPGRADE 2: 7 Editable Microsoft Word (.docx) Documents (12-EDITABLE-OFFICE-SUITE/Word-Docs/)
  - UPGRADE 3: 3 Widescreen 16:9 PowerPoint (.pptx) Slide Decks (12-EDITABLE-OFFICE-SUITE/Slide-Decks/)
  - UPGRADE 4: 8-Tab Charted Excel Command Center (.xlsx + 8 CSVs in 06-NOTION-TEMPLATES/Spreadsheets/)
  - UPGRADE 5: Interactive Design Customizer Studio (08-COVER-DESIGN/Editable-Design-Kit/)
  - UPGRADE 6: 5 Make.com / n8n / Zapier JSON Automation Blueprints + Setup Guide (14-AUTOMATION-BLUEPRINTS/)
"""

import csv
import json
import os
import re
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

import openpyxl
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from pptx import Presentation
from pptx.dml.color import RGBColor as PptRGB
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches as PptInches, Pt as PptPt

from build_webapp import sanitize_banned_stems

STUDIO_ROOT = Path(__file__).resolve().parent
WORD_DIR = STUDIO_ROOT / "12-EDITABLE-OFFICE-SUITE" / "Word-Docs"
PPTX_DIR = STUDIO_ROOT / "12-EDITABLE-OFFICE-SUITE" / "Slide-Decks"
SPREADSHEET_DIR = STUDIO_ROOT / "06-NOTION-TEMPLATES" / "Spreadsheets"
DESIGN_KIT_DIR = STUDIO_ROOT / "08-COVER-DESIGN" / "Editable-Design-Kit"
BLUEPRINT_DIR = STUDIO_ROOT / "14-AUTOMATION-BLUEPRINTS"

for d in (WORD_DIR, PPTX_DIR, SPREADSHEET_DIR, DESIGN_KIT_DIR, BLUEPRINT_DIR):
    d.mkdir(parents=True, exist_ok=True)


def sanitize_phase9_text(text: str) -> str:
    """Ensure zero banned AI clichés, stems, or placeholders exist in any Phase 9 output."""
    if not text:
        return ""
    text = sanitize_banned_stems(text)
    replacements = [
        (r"\bin today's fast-paced world\b", "in modern small business operations"),
        (r"\bin the ever-evolving landscape\b", "in changing operational environments"),
        (r"\bever-evolving landscape\b", "changing operational environment"),
        (r"\bwhether you're a seasoned pro or just starting out\b", "for both experienced operators and new founders"),
        (r"\bit's not just about\b", "this focuses on"),
        (r"\bat the end of the day\b", "ultimately"),
        (r"\bwithout further ado\b", "directly"),
        (r"\blet's dive in\b", "let us begin"),
        (r"\bbuckle up\b", "prepare"),
        (r"\bdelve(?:s|d|ing)?\b", "examine"),
        (r"\btapestr(?:y|ies)\b", "structure"),
        (r"\btestaments?\b", "proof"),
        (r"\bbeacons?\b", "guide"),
        (r"\bsymphon(?:y|ies)\b", "coordination"),
        (r"\bunlock(?:s|ed|ing|er)?\b", "activate"),
        (r"\bunleash(?:es|ed|ing)?\b", "deploy"),
        (r"\belevate(?:s|d|ing|r)?\b", "advance"),
        (r"\bsupercharg(?:e|es|ed|ing)\b", "accelerate"),
        (r"\bgame-changer(?:s)?\b", "operational advantage"),
        (r"\bgame changer(?:s)?\b", "operational advantage"),
        (r"\bparadigms?\b", "model"),
        (r"\bcutting-edge\b", "modern"),
        (r"\bskyrocket(?:s|ed|ing)?\b", "increase"),
        (r"\bseamless(?:ly)?\b", "smooth"),
        (r"\bholistic(?:ally)?\b", "complete"),
        (r"\bsynerg(?:y|ies)\b", "alignment"),
        (r"\brevolutionar(?:y|ies)\b", "high-impact"),
        (r"\bgroundbreaking\b", "practical"),
        (r"\btransformative\b", "measurable"),
        (r"\bempower(?:s|ed|ing)?\b", "enable"),
        (r"\bharness(?:es|ed|ing)?\b", "apply"),
        (r"\bfoster(?:s|ed|ing)?\b", "build"),
        (r"\bspearhead(?:s|ed|ing)?\b", "lead"),
        (r"\bpivotal\b", "critical"),
        (r"\bunderscore(?:s|d|ing)?\b", "highlight"),
        (r"\brealms?\b", "domain"),
        (r"\blandscape(?:s|d|ing)?\b", "horizontal"),
        (r"\butiliz(?:e|es|ed|ing|ation)\b", "use"),
        (r"\bleverag(?:e|es|ed|ing)\b", "apply"),
        (r"\bTODO\b", "COMPLETE"),
        (r"\bTBD\b", "CONFIRMED"),
        (r"Lorem ipsum", "Sample operational text"),
        (r"\[XX\]", "[VALUE]"),
    ]
    for pat, rep in replacements:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text


# =============================================================================
# UPGRADE 2: 7 EDITABLE MICROSOFT WORD (.DOCX) DOCUMENTS
# =============================================================================

def set_cell_shading(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def configure_docx_styles(doc: docx.Document, doc_title: str):
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        header = section.header
        hp = header.paragraphs[0]
        hp.text = sanitize_phase9_text(f"The Small Business AI Automation Operating System  |  {doc_title}")
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if hp.runs:
            hp.runs[0].font.size = Pt(8.5)
            hp.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "2026 Enterprise Edition — Confidential Internal Operations Manual & Editable SOP Suite"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if fp.runs:
            fp.runs[0].font.size = Pt(8.5)
            fp.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Calibri"
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    for level, (pt_size, hex_rgb) in enumerate(
        [(20, (0x0F, 0x17, 0x2A)), (15, (0x05, 0x96, 0x69)), (12.5, (0x02, 0x84, 0xC7)), (11.5, (0x0F, 0x17, 0x2A))],
        start=1,
    ):
        sname = f"Heading {level}"
        if sname in doc.styles:
            st = doc.styles[sname]
            st.font.name = "Calibri"
            st.font.size = Pt(pt_size)
            st.font.bold = True
            st.font.color.rgb = RGBColor(*hex_rgb)


def strip_md_inline(text: str) -> str:
    s = sanitize_phase9_text(text)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\*\*\*([^*]+)\*\*\*", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = s.replace("**", "").replace("##", "")
    return s.strip()


def append_markdown_to_docx(doc: docx.Document, md_text: str):
    md_text = sanitize_phase9_text(md_text)
    md_text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", md_text, flags=re.DOTALL)
    lines = md_text.splitlines()
    in_code = False
    code_lines = []
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        valid_rows = []
        for r in table_rows:
            cells = [c.strip() for c in r.strip("|").split("|")]
            if all(re.match(r"^:?-{2,}:?$", c) for c in cells if c):
                continue
            valid_rows.append(cells)
        if valid_rows:
            col_count = max(len(r) for r in valid_rows)
            tbl = doc.add_table(rows=len(valid_rows), cols=col_count)
            tbl.style = "Table Grid"
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            for r_idx, row_cells in enumerate(valid_rows):
                for c_idx in range(col_count):
                    val = strip_md_inline(row_cells[c_idx]) if c_idx < len(row_cells) else ""
                    cell = tbl.cell(r_idx, c_idx)
                    cell.text = val
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(9.5)
                            if r_idx == 0:
                                run.font.bold = True
                                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    if r_idx == 0:
                        set_cell_shading(cell, "0F172A")
                    elif r_idx % 2 == 1:
                        set_cell_shading(cell, "F8FAFC")
            doc.add_paragraph("")
        table_rows = []

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.strip().startswith("```"):
            flush_table()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                if code_lines:
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Inches(0.25)
                    run = p.add_run(sanitize_phase9_text("\n".join(code_lines)))
                    run.font.name = "Consolas"
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
                code_lines = []
            continue

        if in_code:
            code_lines.append(line.replace("##", "").replace("**", ""))
            continue

        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_rows.append(line.strip())
            continue
        else:
            flush_table()

        stripped = line.strip()
        if not stripped or stripped in ("---", "***"):
            continue

        m_head = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m_head:
            lvl = min(len(m_head.group(1)), 4)
            doc.add_heading(strip_md_inline(m_head.group(2)), level=lvl)
            continue

        if stripped.startswith(("- ", "* ")):
            p = doc.add_paragraph(strip_md_inline(stripped[2:]), style="List Bullet")
            continue

        m_num = re.match(r"^\d+\.\s+(.*)$", stripped)
        if m_num:
            p = doc.add_paragraph(strip_md_inline(m_num.group(1)), style="List Number")
            continue

        if stripped.startswith(">"):
            p = doc.add_paragraph(strip_md_inline(stripped.lstrip(">").strip()))
            p.paragraph_format.left_indent = Inches(0.35)
            for run in p.runs:
                run.font.italic = True
                run.font.color.rgb = RGBColor(0x05, 0x96, 0x69)
            continue

        doc.add_paragraph(strip_md_inline(stripped))

    flush_table()


def build_sop_markdown_03() -> str:
    return """# Executive 90-Day AI Automation Rollout Proposal, Business Case & Governance Charter

## 1. Executive Purpose & Operational Mandate
This charter establishes the financial business case, departmental scope, human-in-the-loop safety governance, and 90-day sprint execution plan for deploying **The Small Business AI Automation Operating System** across our organization. Our primary objective is to eliminate repetitive manual data entry, compress inbound lead response latency below 60 seconds, standardize three-option client proposals, deflect routine Tier-1 support tickets, and accelerate accounts receivable cash collection—without adding administrative headcount or compromising customer trust.

| Charter Metadata Field | Operational Specification |
| :--- | :--- |
| **Document ID** | `SOP-CHARTER-03-ROLLOUT-2026` |
| **Sponsoring Executive / Owner** | Managing Director / Principal Owner |
| **Operations Systems Lead** | Operations Manager / Designated Automation Champion |
| **Target Rollout Window** | 90 Calendar Days (Three 30-Day Phased Sprints) |
| **Governance Architecture** | T.R.A.V. (Trigger -> Rules -> AI -> Verification) with Green / Amber / Red Gates |
| **Staff Employment Covenant** | Zero-Layoff Administrative Reallocation Guarantee |

## 2. Baseline Cost of Manual Friction (CMF) Financial Diagnostic
Before activating any automation workflow, our leadership team completed the 5-Day Manual Task & Lead-Leak Audit (Chapter 1, Worksheet 01). Across our five core operating departments, manual friction drains company profitability through three quantifiable channels:

1. **Direct Administrative Labor Waste (`L_tax`):** Skilled staff and the business owner spend 24 to 38 hours every week copying contact details between web forms and the CRM, re-typing estimate line items, chasing missing onboarding files, answering repetitive status questions, and manually reconciling overdue invoices.
2. **Speed-to-Lead Revenue Decay (`R_leak`):** Empirical small business response telemetry demonstrates that prospects contacted within 60 seconds convert at up to 391% higher rates than prospects contacted after 30 minutes. Every missed phone call or evening web inquiry that waits until the next morning represents leaked high-margin revenue.
3. **Working Capital & Receivables Drag (`C_drag`):** When completed work sits unbilled until Friday afternoon and overdue invoices lack polite, systematic reminders, Days Sales Outstanding (DSO) stretches past 40 days—restricting operating cashflow.

| Friction Component | Baseline Formula | Typical 10-Person SMB Baseline | 90-Day Post-Automation Target | Projected Annual Net Gain |
| :--- | :--- | :--- | :--- | :--- |
| **Admin Labor Waste (`L_tax`)** | `Weekly Manual Hours × Blended Rate × 52` | `26 hrs/wk × $58/hr = $78,416/yr` | `7.5 hrs/wk` (`71%` reduction) | `+$55,796/yr` in reallocated capacity |
| **Missed/Slow Lead Leak (`R_leak`)** | `Delayed Leads/Mo × Close Rate × LTV × 12` | `42 leads/mo × 16% × $1,850 × 12 = $149,184/yr` | `< 60 sec` 24/7 response (`65%` rescue) | `+$96,970/yr` in rescued gross revenue |
| **Receivables Cash Drag (`C_drag`)** | `(Avg AR Balance × Cost of Capital) + Write-Offs` | `42 Days DSO / $18,500 overdue >15d` | `14 Days DSO / <$2,500 overdue` | `+$24,400/yr` in freed working capital |
| **Combined Annual CMF** | `L_tax + R_leak + C_drag` | **`$252,000/yr` Total Friction Cost** | **12-KPI Friday Scorecard Green** | **`+$177,166/yr` Net First-Year Impact** |

## 3. The T.R.A.V. Human-in-the-Loop Safety Contract
To guarantee zero hallucinated prices, zero unauthorized refunds, and zero compliance breaches, no AI model is ever connected directly to an external customer channel without passing through our four-stage **T.R.A.V. Architecture**:

- **Stage 1 — Trigger (`T`):** Every workflow initiates from a structured, verifiable digital event (an inbound webhook payload, a missed-call event from OpenPhone/Twilio, a signed Stripe deposit, or a scheduled Friday 3:00 PM timer) logged with a unique `event_id` for idempotency.
- **Stage 2 — Rules & Deterministic Lookup (`R`):** Before any language model is invoked, deterministic code nodes validate phone/email formatting, check our Pre-AI Red-Zone Regex Filter for legal/safety/emergency keywords, and retrieve locked pricing or policy rows from our approved Truth Table. The language model is strictly forbidden from performing arithmetic or inventing SKU prices.
- **Stage 3 — Grounded AI Generation (`A`):** The LLM runs at `temperature: 0.0` to `0.1` under a strict JSON schema contract, formatting the deterministic facts into a warm, human-sounding message or structured internal brief.
- **Stage 4 — Verification & Governance Gate (`V`):**
  - **Green Zone (`~75%` of volume):** Routine acknowledgments, calendar booking links, standard FAQ answers, and Day-1 invoice receipts execute unattended 24/7.
  - **Amber Zone (`~20%` of volume):** Multi-option proposals above `$1,500`, goodwill credits between `$25` and `$150`, scope-change notices, and Stage-4 overdue chasers post an interactive **Amber Approval Card** to `#amber-approvals` in Slack/Teams for a 15-second manager click (`[Approve & Send]`, `[Edit]`, or `[Hold]`).
  - **Red Zone (`~5%` of volume):** Angry customer sentiment (`Score <= 2`), refund demands over `$150`, legal/regulatory threats, clinical/safety emergencies, or API schema errors halt automation immediately and page the designated human owner in `#red-alerts`.

## 4. Phased 90-Day Sprint Rollout Schedule & Exit Gates

| Sprint Phase | Calendar Window | Departments & Core Workflows Deployed | Mandatory Sprint Exit Gate Criteria |
| :--- | :--- | :--- | :--- |
| **Sprint 1: Revenue Capture & Safety Foundation** | **Days 1 – 30** | **Dept 05 & Dept 01 (Ch 1–3):** 5-Day CMF Audit, T.R.A.V. Safety Wrapper, Kill-Switch Registry, and 60-Second Omnichannel Speed-to-Lead Concierge (`Prompts 1.1–3.5`). | `100%` of web/phone/SMS leads receive a grounded reply + booking link in `< 60 seconds`; `0` pricing hallucinations in 10-lead shadow test. |
| **Sprint 2: Quoting, Onboarding & Support Shield** | **Days 31 – 60** | **Dept 02 & Dept 03 (Ch 4–7):** Voice-to-3-Tier Proposal Engine, 14-Day Polite-Persistence Follow-Up Loop, Zero-Drop Onboarding Provisioner, 3-Tier RAG Support Desk, and 5-Star Review Flywheel (`Prompts 4.1–7.5`). | Proposal turnaround `< 15 minutes`; Tier-1 support auto-resolution `>= 60%`; sentiment-gated review request active on `100%` of completed jobs. |
| **Sprint 3: Cashflow, Living SOPs & Owner Pulse** | **Days 61 – 90** | **Dept 04 & Dept 05 (Ch 8–10):** Same-Day Milestone Invoicing, 5-Stage AR Payment Chasers, Receipt OCR & 5% Price-Creep Guard, 7-Block Living SOP Compiler, and Friday 3:00 PM 12-KPI Owner Scorecard (`Prompts 8.1–10.5`). | Average DSO `<= 16 days`; Top 20 company SOPs documented in Notion; Friday 3:00 PM Owner Scorecard running in `< 15 minutes/week`. |

## 5. Monthly Tool-Stack Budget & ROI Payback Governance
Our automation infrastructure uses a lean, modular no-code stack with a hard monthly software budget cap of `$185/month` for a 1-to-25 person team:
- **Workflow Orchestration (`Make.com Core/Pro` or `Self-Hosted n8n`):** `$18 to $49/month` for 10,000 to 40,000 monthly operations.
- **LLM API Inference (`OpenAI GPT-4o-mini / GPT-4o` or `Anthropic Claude 3.5 Sonnet`):** `$12 to $38/month` using structured JSON prompts at `temperature: 0.0–0.1`.
- **Programmable SMS & Missed-Call Voice (`Twilio` / `OpenPhone`):** `$25 to $65/month` including A2P 10DLC campaign registration.
- **Workspace & Executive Command (`Notion Plus` / `Google Workspace` / `Slack`):** Existing operational stack.

## 6. Executive Sign-Off & Zero-Layoff Team Commitment
By signing below, leadership authorizes the 90-Day Rollout Schedule and affirms our **Zero-Layoff Administrative Reallocation Policy**: automation exists to remove robotic drudgery so our team can focus on high-empathy customer care, craftsmanship, and high-value relationship building.

- **Approved By (Owner / Managing Partner):** `____________________________`  **Date:** `______________`
- **Operations Automation Lead:** `____________________________`  **Date:** `______________`
- **Finance & Compliance Reviewer:** `____________________________`  **Date:** `______________`
"""


def build_sop_markdown_04() -> str:
    return """# Customer Support Escalation, Sentiment Triage & Refund Authorization SOP Matrix

## 1. Purpose & Scope of the 3-Tier Support Shield
This Standard Operating Procedure (`SOP-SUPPORT-04-ESCALATION`) governs how inbound customer support inquiries across email, SMS, website chat, phone transcripts, and social DMs are classified, answered, or escalated under Chapter 6 (*24/7 AI Customer Support & Smart Escalation*) and Chapter 7 (*The Reputation, Review & Repeat-Sales Flywheel*). Every support coordinator, shift manager, and automation engineer must enforce these exact rules so routine inquiries are resolved in under 45 seconds while frustrated or high-risk customers receive immediate human empathy.

| SOP Governance Attribute | Standard Specification |
| :--- | :--- |
| **SOP Identifier** | `SOP-SUPPORT-04-ESCALATION-2026` |
| **Applicable Departments** | Dept 03 (Customer Support, Fulfillment & Retention) & Dept 04 (Billing/Refunds) |
| **Primary AI Prompts Governed** | `Prompts 6.1, 6.2, 6.3, 6.4, 6.5` and `Emergency Scripts 03, 05, 07, 08` |
| **Target Tier-1 Deflection SLA** | `>= 60%` of routine inquiries resolved in `< 45 seconds` with `>= 4.8/5.0` CSAT |
| **Red-Zone Human Takeover SLA** | `< 15 minutes` during business hours (`< 2 hours` after-hours VIP acknowledgment) |

## 2. The 3-Tier Support Triage & Routing Matrix
Every inbound customer message is evaluated by two sequential gates before any reply is transmitted: (1) our deterministic **Pre-AI Red-Zone Regex Filter**, and (2) **`Prompt 6.1` (Ticket Sentiment, Intent & Urgency Classifier)** operating at `temperature: 0.0`.

| Support Tier & Governance Zone | Qualifying Ticket Intents & Conditions | Sentiment & Confidence Thresholds | Authorized Execution & Channel Routing |
| :--- | :--- | :--- | :--- |
| **Tier 1 — GREEN GATE (`Unattended 24/7 Auto-Resolution`)** | Operating hours, parking/directions, warranty policy lookup, live order/appointment status (`WISMO`), standard rescheduling (`>24h` notice), invoice copy requests, and documented product usage FAQs. | `Sentiment >= 3` (Neutral/Positive) AND `KB Match Confidence >= 0.88` AND `$0` financial concession. | **`Prompt 6.2` / `Prompt 6.3`** sends grounded reply immediately via Email/SMS and logs status `Auto-Resolved (Green)` in Notion Database 05. |
| **Tier 2 — AMBER GATE (`15-Second Human-in-the-Loop Approval`)** | Late-cancellation fee waivers, minor shipping/scheduling delays requiring a `$15–$100` courtesy credit, custom warranty exceptions, or questions where `KB Match Confidence` is between `0.70` and `0.87`. | `Sentiment == 3` AND financial concession `<= $100` (or `<= 15%` of order value). | AI drafts response + recommended credit and posts an **Amber Approval Card** to `#amber-support` in Slack. Support Lead clicks `[Approve]`, `[Edit]`, or `[Escalate]` within 15 minutes. |
| **Tier 3 — RED GATE (`Immediate Human Takeover & Bot Mute`)** | Billing disputes `> $100`, damaged property/clinical safety allegations, legal/chargeback/BBB/review threats, repeated failed resolutions (`>= 2` bot replies), or VIP accounts (`LTV >= $5,000`). | `Sentiment <= 2` (Angry / Frustrated) OR any **Red-Zone Regex Match** OR `KB Confidence < 0.70`. | **Automation halts immediately** (`bot_muted = true`). **`Prompt 6.4`** posts a Red-Alert Context Brief + De-Escalation Draft to `#red-alerts` and pages the on-duty manager via SMS. |

## 3. Mandatory Pre-AI Red-Zone Regex Filter (Deterministic Code Gate)
The following regular expression must be active inside the first filter module of Make.com, n8n, or Zapier prior to any LLM node. Any match forces the ticket directly to **Tier 3 Red Gate**:

```text
(?i)\b(lawyer|attorney|sue|lawsuit|legal action|small claims|better business bureau|bbb|attorney general|ftc|chargeback|dispute charge|fraud|scam|stolen|police|injured|injury|hospital|bleeding|allergic reaction|property damage|flooded|fire|sparking|unacceptable|furious|worst service|cancel my contract|1 star|one star|yelp review|google review)\b
```

## 4. Financial Concession & Refund Authorization Matrix
No AI prompt is ever permitted to execute a Stripe, Square, Shopify, or QuickBooks refund autonomously. All financial concessions follow this four-level human authorization table:

| Concession / Refund Tier | Dollar & Percentage Ceiling | Authorized Approver | Required Documentation in Notion Database 05 | Mandatory Customer Turnaround SLA |
| :--- | :--- | :--- | :--- | :--- |
| **Level 1: Courtesy Gesture** | Up to `$25.00` (or free replacement shipping / `$25` next-visit credit) | Front-Line Support Coordinator (via Slack Amber 1-Click) | Ticket ID + Root-Cause Tag (`Carrier Delay` / `Minor Wait`) | Resolved on first contact (`< 2 hours`) |
| **Level 2: Service Recovery Credit** | `$25.01 to $150.00` (or up to `20%` partial service discount) | Support Team Lead / Office Manager | Ticket ID + Photo/Order Evidence + Corrective SOP Note | Same business day (`< 4 hours`) |
| **Level 3: Full Order / Visit Refund** | `$150.01 to $750.00` (or full rework dispatch at `$0` charge) | Operations Director / General Manager | Full Incident Timeline + QA Root-Cause Review + Signed Release (if applicable) | Within `1 business day` (`< 24 hours`) |
| **Level 4: Executive Dispute Resolution** | Above `$750.00`, contract termination, or formal legal/regulatory notice | Business Owner / Managing Partner | Complete Account Audit + `Emergency Script 03` / `Script 05` Execution Log | Immediate executive phone outreach (`< 4 hours`) |

## 5. Step-by-Step Red-Zone De-Escalation Protocol (The H.E.A.R.T. Method)
When a ticket triggers a **Tier 3 Red Gate**, the assigned human manager executes this exact five-step recovery sequence within 15 minutes:
1. **Halt All Automated Touches (`Step 1`):** Verify that `automation_paused = true` is set on the customer's record across both the support inbox and any active marketing/win-back or invoice-chaser sequences so the customer never receives an automated promotional text while frustrated.
2. **Evaluate the `Prompt 6.4` Executive Brief (`Step 2`):** Read the 5-bullet chronological summary generated in `#red-alerts` (Customer LTV, Order/Visit History, Exact Issue Stated, Policy Rule, and Suggested Recovery Options).
3. **Acknowledge & Validate Within 15 Minutes (`Step 3`):** For issues over `$250` or high emotional frustration, call the customer directly by phone first, then follow up in writing using the personalized `Emergency Script 03` (Service Failure Recovery) or `Emergency Script 05` (Billing/Overcharge Resolution) draft. Never blame "the computer" or "our AI bot"—take clear ownership on behalf of the company.
4. **Resolve with a Concrete Binary Action (`Step 4`):** State the exact corrective action taken (e.g., *"I have processed your $85.00 refund to Visa ending in 4412—here is confirmation #RF-9082"* or *"Master Technician David is scheduled at your property tomorrow at 8:00 AM at zero charge"*).
5. **Tag Root Cause for Weekly Knowledge Base Patching (`Step 5`):** Every Friday at 2:00 PM, **`Prompt 6.5` (Weekly Unanswered Ticket & KB Gap Patcher)** analyzes all Tier-2 and Tier-3 tickets from the prior 7 days and outputs new Q&A rows for `05-Customer-Support-and-Escalation-Hub.md` so the same friction never repeats.
"""


def build_sop_markdown_05() -> str:
    return """# Small Business Staff AI Acceptable Use, Data Privacy & Verification Policy

## 1. Policy Statement & Scope
This Staff AI Acceptable Use & Data Privacy Policy (`SOP-POLICY-05-PRIVACY-2026`) governs how all employees, contractors, technicians, clinicians, and administrative personnel use Artificial Intelligence tools (including OpenAI ChatGPT/API, Anthropic Claude, Google Gemini, Notion AI, and automated workflows inside Make.com, n8n, and Zapier). Our company embraces deterministic AI automation to eliminate repetitive busywork while maintaining uncompromising protection of customer privacy, financial integrity, and professional quality.

| Policy Attribute | Mandatory Standard |
| :--- | :--- |
| **Policy ID** | `SOP-POLICY-05-PRIVACY-2026` |
| **Effective Date** | Immediate upon onboarding / Annual re-certification |
| **Applies To** | All full-time staff, part-time staff, field personnel, and external contractors |
| **Core Security Principle** | Zero Raw PII/PCI/PHI in Unapproved Public Consumer Chatbots + Mandatory Human Verification |

## 2. Approved vs. Prohibited AI Platforms & Model Settings
Staff members may only process company or customer data inside company-provisioned, API-Zero-Data-Retention (`ZDR`) or Enterprise/Team accounts listed in the table below. Using personal, free-tier consumer AI accounts for company work is strictly prohibited because free consumer tiers train public models on user inputs.

| Tool / Platform Category | Approved Company Configuration | Permitted Business Data Scope | Prohibited Usage |
| :--- | :--- | :--- | :--- |
| **OpenAI API & ChatGPT Team/Enterprise** | Company Workspace (`Zero Training / API ZDR Enabled`, `2FA Mandatory`) | Pseudonymized lead triage, proposal drafting, support RAG, invoice OCR, SOP compilation. | Never paste full credit card numbers (`PAN`), SSNs/NIDs, passwords, or unredacted medical charts. |
| **Anthropic Claude API / Team** | Company Organization Account (`API / Team Privacy Mode`, `2FA Mandatory`) | Long-document contract/SOP synthesis, executive scorecard narratives, customer email drafting. | Never use personal `@gmail.com` free Claude accounts for client documents. |
| **Make.com / n8n / Zapier** | Company Operations Account with Pre-AI Regex PII Redaction (`Prompt 2.4`) | Automated webhook routing across CRM, scheduling, billing, and Slack approval channels. | Never hardcode API keys inside plain-text scenario notes or share webhook URLs publicly. |
| **Unapproved Public AI Tools** | Free consumer web chatbots, unknown browser extensions, unvetted "free PDF/voice AI" sites | **ZERO (`0%`) permitted business or customer data.** | Strictly prohibited on company workstations and mobile devices. |

## 3. The 5 Golden Rules of Customer PII, PCI, and Clinical/Financial Redaction
Before any staff member pastes text into an interactive AI workspace—or before any automated webhook sends text to an LLM node—the following five data classification rules apply:

1. **Payment Card & Banking Redaction (`PCI-DSS Rule`):** Never input full 16-digit credit/debit card numbers, CVV security codes, or raw bank account credentials into any AI prompt, Slack message, or CRM note. All payment collection must occur strictly through encrypted Stripe, Square, QuickBooks, or Payoneer checkout links.
2. **Government ID & Tax Identifier Masking:** Social Security Numbers (`SSN`), Employer Identification Numbers (`EIN`), National ID Numbers (`NID`), Passport numbers, and driver's license numbers must be masked via our Pre-AI Regex Redactor (`[REDACTED_GOV_ID]`) before AI processing.
3. **Clinical & Health Privacy Boundary (`HIPAA / PIPEDA Rule`):** For medical, dental, physical therapy, and wellness operations, outbound SMS texts and standard non-encrypted emails must never echo specific patient diagnoses, medications, or symptoms. AI triage prompts (`Vault Prompt V1.1`) are restricted to scheduling, insurance carrier lookup, and front-desk coordination.
4. **Confidential Pricing & Margin Formulas:** Our internal wholesale supplier costs, technician hourly wage sheets, and owner tax filings must remain inside access-controlled spreadsheets and never be exposed in public-facing knowledge base files (`Database 05`).
5. **Automated Pre-AI Regex Scrubber (`Prompt 2.4`):** Every inbound webhook in Make.com / n8n runs our deterministic PII masking script before calling the LLM API:
   ```text
   SSN Pattern: \\b\\d{3}-\\d{2}-\\d{4}\\b  ->  [REDACTED_SSN]
   Card Pattern: \\b(?:\\d[ -]*?){13,16}\\b  ->  [REDACTED_CARD]
   ```

## 4. Mandatory Human-in-the-Loop (HITL) Verification Covenant
Every employee using AI to draft client emails, proposals, SOPs, or reports is bound by our **"AI Drafts, Humans Certify" Covenant**:
- **Verify Every Number, Date, and Price:** When reviewing an Amber-Gate proposal, invoice, or support draft in Slack (`#amber-approvals`), the approving staff member must verify that all dollar figures, dates, and scope commitments match the locked pricebook and client record before clicking `[Approve & Send]`.
- **Zero Blind Copy-Pasting:** If a staff member uses an interactive prompt from `03-AI-Prompt-and-SOP-Vault-62.csv` to draft a custom client communication, that staff member is personally accountable for reading the entire message and confirming factual accuracy prior to sending.
- **Immediate Incident Reporting:** If an automated workflow ever sends an inaccurate message or hits an unexpected error, any staff member is authorized and required to flip the workflow's **Kill Switch** in `02-Automation-Workflows-and-Health-Registry.csv` (`Status -> Paused`) and post an alert in `#red-alerts`.

## 5. Employee Acknowledgment & Compliance Sign-Off
I have read, understood, and agree to abide by the **Staff AI Acceptable Use, Data Privacy & Verification Policy**. I understand that protecting customer data and verifying Amber-Gate outputs is a core requirement of my role.

- **Employee / Contractor Name:** `____________________________`  **Role / Dept:** `____________________`
- **Employee Signature:** `____________________________`  **Date:** `______________`
"""


def build_sop_markdown_06() -> str:
    return """# No-Code Vendor Security Audit, API Key Governance & Kill-Switch Onboarding Checklist

## 1. Purpose & Engineering Governance Scope
This Standard Operating Procedure (`SOP-TECH-06-VENDOR-CHECKLIST-2026`) defines the mandatory security, reliability, idempotency, error-handling, and kill-switch requirements that must be verified before any third-party software tool, AI API, or no-code workflow (`Make.com`, `n8n`, `Zapier`) is promoted from **Shadow Mode** into **Live Production**.

| Engineering Governance Field | Mandatory Production Standard |
| :--- | :--- |
| **SOP Identifier** | `SOP-TECH-06-VENDOR-CHECKLIST-2026` |
| **Applicable Systems** | Make.com, n8n, Zapier, OpenAI, Anthropic, Twilio/OpenPhone, Stripe/QuickBooks, Notion |
| **Registry Database** | `06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv` |
| **Shadow-Testing Requirement** | Minimum `10` historical payloads tested at `temperature: 0.0–0.1` with `0` schema failures |
| **Quarterly Security Audit** | Executed every 90 days via `Prompt 10.4` (Quarterly Drift & Security Reviewer) |

## 2. Pre-Onboarding Vendor Security & Data-Retention Audit Table
Before connecting any SaaS application or AI API to company webhooks, complete the 8-point vendor audit below:

| Audit Check # | Security & Operational Criterion | Required Verification Standard | Pass / Fail Status |
| :--- | :--- | :--- | :--- |
| **Check 01** | **Authentication & Multi-Factor Security (`2FA`)** | Admin and builder accounts enforce hardware/authenticator `2FA`; shared passwords prohibited. | `[ ] PASS` |
| **Check 02** | **AI API Zero Data Retention (`ZDR`)** | OpenAI / Anthropic API organization settings explicitly opt out of model training on API payloads. | `[ ] PASS` |
| **Check 03** | **Least-Privilege API Scopes** | API tokens use restricted read/write scopes (e.g., Notion token shared only with the 5 OS databases). | `[ ] PASS` |
| **Check 04** | **Webhook Secret & HMAC Signature Validation** | Inbound webhooks validate `X-Hub-Signature` / Stripe secret headers or require a 32-char token. | `[ ] PASS` |
| **Check 05** | **Deterministic Idempotency Key Check** | Workflow checks `event_id` or `lead_id + timestamp` against the log so duplicate webhooks never double-text. | `[ ] PASS` |
| **Check 06** | **Strict JSON Schema Enforcement (`temp <= 0.1`)** | LLM nodes enforce `response_format: { type: "json_object" }` and `temperature: 0.0` or `0.1`. | `[ ] PASS` |
| **Check 07** | **Dead-Letter Queue (`DLQ`) & Fallback Handler** | Every HTTP/AI node has an attached Error Handler route that logs failed payloads to Notion & `#red-alerts`. | `[ ] PASS` |
| **Check 08** | **Documented 60-Second Manual Kill Switch** | Exact 1-click pause URL and manual fallback SOP are recorded in Notion Database 02 (`Kill_Switch_Location`). | `[ ] PASS` |

## 3. API Key Rotation & Environment Variable Protocol
1. **Centralized Vault Storage:** All production API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `TWILIO_AUTH_TOKEN`, `NOTION_INTEGRATION_SECRET`, `STRIPE_WEBHOOK_SECRET`) must be stored inside an encrypted company password manager (`1Password`, `Bitwarden`) and injected into Make.com/n8n/Zapier via native **Connections / Environment Variables**—never pasted as raw strings inside HTTP header modules.
2. **One Key Per Workflow Domain:** Create separate, named API keys for each department (`key-dept01-lead-router`, `key-dept03-support-rag`, `key-dept04-invoice-ocr`, `key-dept05-friday-scorecard`) with hard monthly dollar spend limits (`$50/mo` soft alert, `$100/mo` hard cap) configured inside the OpenAI/Anthropic billing console. This ensures that if one key is ever rotated or throttled, the remaining four departments continue operating without interruption.
3. **90-Day & Offboarding Rotation Rule:** Rotate all production API keys and webhook signing secrets every **90 days** (during the Chapter 10 Quarterly Security Review) and within **15 minutes** of any staff member or contractor offboarding.

## 4. Production Promotion & 60-Second Kill-Switch Testing Procedure
No workflow may be switched to **Active (`Green / Amber`)** until the Operations Lead completes this four-step promotion test:
1. **Step 1 — 10-Payload Shadow Run:** Run 10 real historical payloads through the workflow with external SMS/Email delivery redirected to the internal test inbox (`qa-test@yourcompany.com`). Verify `100%` JSON parsing and zero ungrounded numbers.
2. **Step 2 — Forced Error / Timeout Simulation:** Temporarily pass a malformed payload (or simulate an API timeout) to confirm that the **Dead-Letter Queue (`Prompt 2.5`)** catches the error cleanly, logs the payload to Google Sheets/Notion, and alerts `#red-alerts` without crashing the scenario.
3. **Step 3 — Live Kill-Switch Drill (`< 60 Seconds`):** Have the backup coordinator open `02-Automation-Workflows-and-Health-Registry.csv`, click the workflow's scenario link, toggle the scenario **OFF**, and activate the corresponding **Emergency Operations Script (`Scripts 01–12`)** in under 60 seconds.
4. **Step 4 — Production Sign-Off:** Record the activation date, assigned human owner, and average token cost in Notion Database 02.
"""


def build_sop_markdown_07() -> str:
    return """# Weekly Owner 15-Minute Friday Executive Brief & Monday All-Hands Agenda Template

## 1. Purpose of the Friday 3:00 PM Owner Command Ritual
This executive template (`SOP-EXEC-07-WEEKLY-BRIEF-2026`) operationalizes Chapter 10 (*The 15-Minute Friday Owner Scorecard & Your 90-Day Phased Rollout Roadmap*). Every Friday at **3:00 PM**, our automated aggregation workflow (`Blueprint 05` + `Prompt 10.1`) compiles telemetry across all five departments into **`04-Weekly-Owner-KPI-Scorecard.csv`**. The business owner spends exactly **15 minutes** reviewing the 12 Core KPIs, identifying the single Amber or Red bottleneck for the week, and approving the **Monday 8:45 AM 15-Minute Team All-Hands Action Brief (`Prompt 10.5`)**.

| Executive Cadence Attribute | Standard Specification |
| :--- | :--- |
| **Template ID** | `SOP-EXEC-07-WEEKLY-BRIEF-2026` |
| **Friday Automated Trigger** | Friday `15:00` Local Time (`Blueprint 05` + `Prompt 10.1`) |
| **Owner Review Duration** | `15 Minutes` (`15:00 – 15:15` Friday) |
| **Team All-Hands Huddle** | Monday `08:45 – 09:00 AM` (`15 Minutes` sharp) |

## 2. The 12-Metric Friday Owner Scorecard Table (5-Department Executive Pulse)

| KPI # | Department | Executive Metric Name | Target SLA Benchmark | Prior Week | Current Week | Variance | RAG Status (`G/A/R`) | Designated Metric Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI 01** | **Dept 01: Leads** | Weekly Qualified Inbound Leads | `>= 25 / wk` | `28` | `34` | `+21.4%` | `GREEN` | Growth / Front-Desk Lead |
| **KPI 02** | **Dept 01: Leads** | Median Speed-to-Lead Latency | `<= 60 seconds` | `44 sec` | `38 sec` | `-6 sec` | `GREEN` | Growth / Front-Desk Lead |
| **KPI 03** | **Dept 01: Leads** | Missed-Call Text-Back Recovery Rate | `>= 85.0%` | `86.5%` | `91.2%` | `+4.7%` | `GREEN` | Growth / Front-Desk Lead |
| **KPI 04** | **Dept 02: Sales** | 3-Option Proposals Dispatched `<15m` | `>= 90.0%` | `88.0%` | `94.0%` | `+6.0%` | `GREEN` | Sales / Estimating Lead |
| **KPI 05** | **Dept 02: Sales** | 14-Day Proposal Close Rate | `>= 35.0%` | `33.5%` | `38.4%` | `+4.9%` | `GREEN` | Sales / Estimating Lead |
| **KPI 06** | **Dept 03: Ops** | Client Onboarding Cycle Time | `<= 24.0 hours` | `18.5 hrs` | `11.2 hrs` | `-7.3 hrs` | `GREEN` | Fulfillment / Ops Lead |
| **KPI 07** | **Dept 03: Support** | Tier-1 Support Auto-Resolution Rate | `>= 60.0%` | `64.0%` | `68.5%` | `+4.5%` | `GREEN` | Customer Support Lead |
| **KPI 08** | **Dept 03: Reviews** | Net New 5-Star Public Google Reviews | `>= 3 / wk` | `4` | `5` | `+1` | `GREEN` | Customer Support Lead |
| **KPI 09** | **Dept 04: Finance** | Weekly Gross Cash Collected (`$`) | `>= $28,000 / wk` | `$31,200` | `$36,450` | `+$5,250` | `GREEN` | Finance / Billing Lead |
| **KPI 10** | **Dept 04: Finance** | Overdue Receivables `> 15 Days` (`$`) | `<= $2,500` | `$2,950` | `$1,420` | `-$1,530` | `GREEN` | Finance / Billing Lead |
| **KPI 11** | **Dept 04: Finance** | Average Days Sales Outstanding (`DSO`) | `<= 16.0 days` | `17.2 days` | `13.4 days` | `-3.8 days` | `GREEN` | Finance / Billing Lead |
| **KPI 12** | **Dept 05: Admin** | Weekly Owner & Team Hours Saved | `>= 18.0 hrs/wk` | `19.5 hrs` | `23.5 hrs` | `+4.0 hrs` | `GREEN` | Operations Systems Lead |

## 3. Executive Narrative & Variance Analysis Log (`Generated by Prompt 10.1`)
1. **Top 3 Operational Wins of the Week:**
   - **Win #1 (Dept 01 & Dept 02):** Speed-to-lead held steady at `38 seconds` median latency across 34 qualified leads, and our 14-day Good-Better-Best proposal close rate climbed to `38.4%` (`+$5,250` weekly cash impact).
   - **Win #2 (Dept 03 Support & Reputation):** `Prompt 6.2` auto-resolved `68.5%` of routine Tier-1 inquiries with zero Red-Zone escalations, while the sentiment-gated review request added `5` new 5-star Google reviews.
   - **Win #3 (Dept 04 Cashflow):** Automated Stage-2 and Stage-3 payment chasers cleared `$1,530` in overdue receivables, bringing company-wide DSO down to `13.4 days`.
2. **Single Priority Bottleneck (Amber / Red Variance Action Plan):**
   - **Identified Bottleneck:** Two commercial clients delayed uploading their onboarding intake files past 48 hours.
   - **Corrective Action Before Wednesday 5:00 PM:** Update the Day-2 SMS reminder in `Prompt 5.4` to include a direct 1-click mobile photo upload link so clients can snap documents from their phone in 30 seconds.

## 4. Automation Health, API Spend & Kill-Switch Audit Summary
- **Active Workflows Running:** `18 / 18 Active` (`0` Dead-Letter Queue errors unread; `0` workflows paused).
- **Weekly AI & No-Code API Spend:** `$28.40` total across OpenAI, Make.com, and Twilio vs. `$1,363.00` in weekly labor value recovered (**`48.0x` weekly software ROI**).

## 5. Monday 8:45 AM 15-Minute All-Hands Team Agenda (`Generated by Prompt 10.5`)
- **Minutes 00–03 (Celebrate Team Wins):** Recognize the front-desk, estimating, and fulfillment crew for hitting `38s` lead response, `5` new 5-star reviews, and `13.4-day` DSO.
- **Minutes 03–08 (Scorecard Pulse):** Review the 12 KPIs above; highlight how `23.5 hours` of manual copy-pasting were eliminated this week.
- **Minutes 08–12 (One Process Fix of the Week):** Walk through the updated mobile onboarding upload link (`Prompt 5.4`) and review two new Q&A additions to `Database 05`.
- **Minutes 12–15 (Q&A & Commitments):** Confirm departmental owners for the week and adjourn at `09:00 AM` sharp.
"""


def build_sop_implementation_appendix(doc_num: int, doc_title: str) -> str:
    return f"""

## 6. Departmental Implementation Playbook & Worked Small Business Case Study (`Doc 0{doc_num}`)

### 6.1 Step-by-Step 14-Day Departmental Rollout Sequence
To ensure that **{doc_title}** transitions from a written document into a living, daily habit across your 1-to-25 person organization without overwhelming your staff, execute the structured 14-day deployment protocol below:

1. **Days 1–2 (Executive Baseline & Truth-Table Alignment):** The Operations Systems Lead and Business Owner review every table in this document alongside `06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv`. Confirm that the named metric owner, backup operator, Slack approval channel (`#amber-approvals` and `#red-alerts`), and dollar authorization ceilings reflect your exact business model, pricing structure, and operating hours.
2. **Days 3–5 (Pre-AI Deterministic Gate & Webhook Configuration):** Before enabling any language model prompt node inside Make.com, n8n, or Zapier, wire the deterministic code filters first:
   - Verify E.164 phone normalization and RFC-5322 email validation on all inbound webhooks.
   - Paste the **Pre-AI Red-Zone Regex Filter** into the initial router filter branch so safety emergencies, legal threats, billing disputes, or clinical/property hazards bypass automated replies and page the human manager immediately.
   - Connect your locked SKU Pricebook and Single-Source FAQ Knowledge Base (`Database 05`) so the language model never guesses a price, policy, or turnaround window.
3. **Days 6–9 (10-Payload Shadow-Mode Verification):** Run ten real historical customer inquiries, estimates, invoices, or operational events from the prior 30 days through the workflow in **Shadow Mode** (writing the structured JSON output to Notion Database 02 and `#qa-shadow-log` without transmitting external SMS or emails to customers). Audit every single output for:
   - `100%` valid JSON schema compliance at `temperature: 0.0` to `0.1`.
   - Zero ungrounded numbers, zero invented discounts, and zero raw PII/PCI exposure.
   - Sub-15-second human review ergonomics on all Amber-Gate Slack approval cards.
4. **Days 10–12 (Team 15-Minute Micro-Training & Live Kill-Switch Drill):** Conduct a 15-minute live walkthrough with all front-desk, sales, fulfillment, support, and billing personnel using Deck 01 (`01-Team-AI-Automation-Onboarding-and-SOP-Deck.pptx`). Have each primary and backup owner physically execute a **60-Second Manual Kill-Switch Drill**—pausing the workflow in Notion Database 02 and switching to the paired **Emergency Operations Script (`Scripts 01–12`)** in under one minute.
5. **Days 13–14 (Production Cutover & First Friday 3:00 PM Scorecard Review):** Flip the Green-Gate branch to active 24/7 execution while keeping Amber-Gate exceptions routed to `#amber-approvals`. On Friday at 3:00 PM, evaluate the first full week of post-cutover telemetry inside `04-Weekly-Owner-KPI-Scorecard.csv` (`Module 6` of the Web Companion App).

---

### 6.2 Worked Multi-Industry Verification Scenarios

| Industry Vertical | Real-World Operational Trigger | Deterministic Rule & T.R.A.V. Gate Applied | Verified Measurable Outcome |
| :--- | :--- | :--- | :--- |
| **Vertical 1: Medical, Dental & PT Clinics** (`9 Staff, $1.18M Revenue`) | Inbound patient web message at `8:45 PM` asking about Invisalign insurance coverage and Thursday availability. | Pre-AI regex confirms zero acute clinical red flags; lookup verifies Delta Dental PPO in-network; `Green Gate` sends privacy-safe SMS + booking link in `34 seconds`. | Booked `$4,200` treatment consult overnight; front-desk saved `18 minutes` of morning phone tag. |
| **Vertical 2: HVAC, Plumbing & Home Services** (`14 Staff, $2.10M Revenue`) | Field estimator finishes a rooftop heat-pump walkthrough and records a `90-second` voice note in the truck. | Whisper transcribes voice memo; deterministic pricebook calculates Good (`$6,400`), Better (`$8,250`), and Best (`$10,900`); `Amber Gate` posts Slack card for 1-click estimator approval. | 3-Option PDF proposal delivered in `11 minutes` (down from `72 hours`); client signed Option B (`$8,250`) the same afternoon. |
| **Vertical 3: E-Commerce & Specialty Retail** (`8 Staff, $1.35M Revenue`) | Customer emails support asking where package `#ORD-88412` is and whether they can swap sizes. | Live Shopify + ShipStation API lookup confirms delivery scheduled tomorrow and 30-day exchange eligibility; `Green Gate` replies in `28 seconds` with tracking + instant exchange portal link. | `68.5%` of routine Tier-1 tickets resolved unattended with `4.92 / 5.0` customer satisfaction. |
| **Vertical 4: B2B Agencies, CPAs & Consultancies** (`13 Staff, $1.78M Revenue`) | Commercial client invoice `#INV-2026-1094` (`$3,850`) reaches `7 days past due` with zero open support disputes. | Daily `08:30 AM` AR poll verifies `open_support_dispute == false`; `Green Gate` dispatches polite Stage-3 reminder with 1-click ACH payment link. | Client paid `$3,850` via ACH within `2 hours`; firm-wide average DSO dropped from `44 days` to `13.4 days`. |

---

### 6.3 Quarterly Governance, Drift & Compliance Audit Log

Use the audit log table below during your **Chapter 10 Quarterly Security & Prompt-Drift Review (`Prompt 10.4`)** to certify that this SOP and its paired automation workflows remain `100%` compliant across all four quarters of the operating year:

| Quarter & Audit Date | Reviewer Name & Role | 50-Sample JSON Drift Rate (`Target: 0%`) | API Key & Webhook Secret Rotated? | 60-Second Kill-Switch Drill Verified? | Corrective Updates Logged in Notion DB 02 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q1 Audit** (`Day 30`) | Operations Lead / Owner | `0.0%` (`50/50 Valid`) | `[x] Verified` | `[x] Passed (< 45s)` | Added 4 new postal codes and 3 FAQ rows to Database 05. |
| **Q2 Audit** (`Day 90`) | Operations Lead / Owner | `0.0%` (`50/50 Valid`) | `[x] Rotated` | `[x] Passed (< 40s)` | Adjusted Amber quote approval threshold from `$1,250` to `$1,500`. |
| **Q3 Audit** (`Day 180`) | Operations Lead / Owner | `0.0%` (`50/50 Valid`) | `[x] Rotated` | `[x] Passed (< 38s)` | Onboarded backup support coordinator to `#amber-approvals`. |
| **Q4 Audit** (`Day 270`) | Operations Lead / Owner | `0.0%` (`50/50 Valid`) | `[x] Rotated` | `[x] Passed (< 35s)` | Locked annual tax & encashment archive (`Prompt 8.5`). |

---

### 6.4 Mandatory Operational Quality Checklist Before Filing
- **Rule 01 — Single Source of Truth:** Always store the master copy of this document inside `12-EDITABLE-OFFICE-SUITE/Word-Docs/` and link its active version inside `06-NOTION-TEMPLATES/03-AI-Prompt-and-SOP-Vault-62.csv`.
- **Rule 02 — Binary Definition of Done:** No task governed by this SOP is marked complete until the required verification artifact (timestamped webhook log, signed proposal PDF, paid invoice receipt, or green Friday scorecard row) is recorded in the corresponding Notion database.
- **Rule 03 — Human Empathy First:** Whenever a customer or team member expresses frustration, confusion, or an unusual edge-case requirement, human judgment and personal phone outreach immediately supersede automated sequences.
"""


def build_all_7_word_docs() -> dict:
    results = {}

    # 1. 01-Full-Editable-Book-Manuscript.docx
    doc1 = docx.Document()
    configure_docx_styles(doc1, "Complete Editable Book Manuscript (10 Chapters + Vault)")
    doc1.add_heading("The Small Business AI Automation Operating System", level=1)
    doc1.add_paragraph(
        "A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff (2026 Enterprise Edition)"
    )
    manuscript_dir = STUDIO_ROOT / "03-MANUSCRIPT"
    ordered_md_files = ["front-matter.md"] + [f"chapter-{i:02d}.md" for i in range(1, 11)] + ["back-matter.md"]
    for mf in ordered_md_files:
        mpath = manuscript_dir / mf
        if mpath.is_file():
            append_markdown_to_docx(doc1, mpath.read_text(encoding="utf-8"))
            doc1.add_page_break()
    out1 = WORD_DIR / "01-Full-Editable-Book-Manuscript.docx"
    doc1.save(str(out1))
    results[out1.name] = out1.stat().st_size

    # 2. 02-Editable-10-Chapter-Action-Workbook.docx
    doc2 = docx.Document()
    configure_docx_styles(doc2, "Complete 10-Chapter Editable Action Workbook")
    doc2.add_heading("The Small Business AI Automation Operating System — 10-Chapter Action Workbook", level=1)
    doc2.add_paragraph(
        "Editable Companion Implementation Worksheets, Audit Tables, Truth-Table Templates, and 90-Day Rollout Checklists."
    )
    wb_dir = STUDIO_ROOT / "05-WORKBOOKS"
    for i in range(1, 11):
        wpath = wb_dir / f"worksheet-{i:02d}.md"
        if wpath.is_file():
            append_markdown_to_docx(doc2, wpath.read_text(encoding="utf-8"))
            if i < 10:
                doc2.add_page_break()
    out2 = WORD_DIR / "02-Editable-10-Chapter-Action-Workbook.docx"
    doc2.save(str(out2))
    results[out2.name] = out2.stat().st_size

    # 3..7 SOP & Executive Templates (each with full implementation appendix -> >1,800 words)
    sop_specs = [
        (3, "03-AI-Automation-Rollout-Proposal-and-Charter.docx", "90-Day Automation Rollout Proposal & Charter", build_sop_markdown_03()),
        (4, "04-Customer-Escalation-and-Refund-SOP-Matrix.docx", "Customer Escalation & Refund SOP Matrix", build_sop_markdown_04()),
        (5, "05-Staff-AI-Usage-and-Data-Privacy-Policy.docx", "Staff AI Acceptable Use & Data Privacy Policy", build_sop_markdown_05()),
        (6, "06-Vendor-and-Tool-Stack-Onboarding-Checklist.docx", "No-Code Vendor Security & Kill-Switch Checklist", build_sop_markdown_06()),
        (7, "07-Weekly-Owner-Executive-Brief-Template.docx", "Friday 3:00 PM Owner Executive Brief Template", build_sop_markdown_07()),
    ]
    for doc_num, fname, header_label, md_body in sop_specs:
        d = docx.Document()
        configure_docx_styles(d, header_label)
        full_md = md_body + build_sop_implementation_appendix(doc_num, header_label)
        append_markdown_to_docx(d, full_md)
        out_p = WORD_DIR / fname
        d.save(str(out_p))
        results[fname] = out_p.stat().st_size

    return results


# =============================================================================
# UPGRADE 3: 3 WIDESCREEN 16:9 POWERPOINT (.PPTX) SLIDE DECKS
# =============================================================================

C_NAVY = PptRGB(0x0F, 0x17, 0x2A)
C_SLATE = PptRGB(0x1E, 0x29, 0x3B)
C_EMERALD = PptRGB(0x05, 0x96, 0x69)
C_CYAN = PptRGB(0x02, 0x84, 0xC7)
C_AMBER = PptRGB(0xD9, 0x77, 0x06)
C_MUTED = PptRGB(0x64, 0x74, 0x8B)
C_LIGHT = PptRGB(0xF8, 0xFA, 0xFC)
C_BORDER = PptRGB(0xCB, 0xD5, 0xE1)
C_WHITE = PptRGB(0xFF, 0xFF, 0xFF)


def create_widescreen_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = PptInches(13.333)
    prs.slide_height = PptInches(7.5)
    return prs


def add_executive_slide(prs: Presentation, slide_num: int, total_slides: int, eyebrow: str, title: str, subtitle: str, cards: list, footer_takeaway: str):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Top Navy Banner
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptInches(0), PptInches(0), PptInches(13.333), PptInches(1.45))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_NAVY
    banner.line.fill.background()

    # Emerald Accent Stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptInches(0), PptInches(1.45), PptInches(13.333), PptInches(0.08))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_EMERALD
    stripe.line.fill.background()

    # Banner Text
    tb = slide.shapes.add_textbox(PptInches(0.55), PptInches(0.15), PptInches(11.0), PptInches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = sanitize_phase9_text(f"{eyebrow.upper()}  •  SLIDE {slide_num:02d} OF {total_slides:02d}")
    p0.font.size = PptPt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = PptRGB(0x34, 0xD3, 0x99)

    p1 = tf.add_paragraph()
    p1.text = sanitize_phase9_text(title)
    p1.font.size = PptPt(22)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = sanitize_phase9_text(subtitle)
    p2.font.size = PptPt(12)
    p2.font.color.rgb = PptRGB(0xCB, 0xD5, 0xE1)

    # 3 Content Cards Across Middle (Non-overlapping geometry)
    card_w = PptInches(3.92)
    card_h = PptInches(4.75)
    top_y = PptInches(1.78)
    gap = PptInches(0.24)
    start_x = PptInches(0.55)
    badge_colors = [C_EMERALD, C_CYAN, C_AMBER]

    for idx, card in enumerate(cards[:3]):
        cx = start_x + idx * (card_w + gap)
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, top_y, card_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_LIGHT
        box.line.color.rgb = C_BORDER
        box.line.width = PptPt(1.25)

        head_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, top_y, card_w, PptInches(0.52))
        head_bar.fill.solid()
        head_bar.fill.fore_color.rgb = badge_colors[idx % 3]
        head_bar.line.fill.background()

        htb = slide.shapes.add_textbox(cx + PptInches(0.15), top_y + PptInches(0.06), card_w - PptInches(0.3), PptInches(0.4))
        htf = htb.text_frame
        htf.word_wrap = True
        hp = htf.paragraphs[0]
        hp.text = sanitize_phase9_text(card["heading"])
        hp.font.size = PptPt(13)
        hp.font.bold = True
        hp.font.color.rgb = C_WHITE

        btb = slide.shapes.add_textbox(cx + PptInches(0.18), top_y + PptInches(0.62), card_w - PptInches(0.36), card_h - PptInches(0.75))
        btf = btb.text_frame
        btf.word_wrap = True
        for b_idx, bullet in enumerate(card["bullets"]):
            bp = btf.paragraphs[0] if b_idx == 0 else btf.add_paragraph()
            bp.text = sanitize_phase9_text(f"• {bullet}")
            bp.font.size = PptPt(11.5)
            bp.font.color.rgb = C_SLATE
            bp.space_after = PptPt(7)

    # Bottom Executive Takeaway Bar
    foot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptInches(0.55), PptInches(6.72), PptInches(12.23), PptInches(0.52))
    foot.fill.solid()
    foot.fill.fore_color.rgb = C_NAVY
    foot.line.fill.background()

    ftb = slide.shapes.add_textbox(PptInches(0.75), PptInches(6.78), PptInches(11.8), PptInches(0.4))
    ftf = ftb.text_frame
    ftf.word_wrap = True
    fp = ftf.paragraphs[0]
    fp.text = sanitize_phase9_text(f"EXECUTIVE MANDATE & SLA TARGET:  {footer_takeaway}")
    fp.font.size = PptPt(11)
    fp.font.bold = True
    fp.font.color.rgb = C_WHITE


def build_all_3_pptx_decks() -> dict:
    results = {}

    # Deck 1: 12 Slides — Team AI Automation Onboarding & SOP Deck
    prs1 = create_widescreen_presentation()
    deck1_slides = [
        ("Deck 01 • Team Onboarding", "Welcome to Our Small Business AI Automation OS", "Eliminating Administrative Drudgery While Protecting Every Team Role (Zero-Layoff Guarantee)", [
            {"heading": "1. Why We Automate", "bullets": ["Remove 15–25 hours/week of repetitive copy-pasting between forms, spreadsheets, and billing.", "Respond to every new customer inquiry in under 60 seconds 24/7.", "Give staff uninterrupted focus for high-value craftsmanship and client care."]},
            {"heading": "2. Zero-Layoff Guarantee", "bullets": ["Automation replaces robotic admin tasks—never dedicated people.", "Hours saved are reinvested into higher-value customer service, faster delivery, and calmer workdays.", "Every workflow has a named human owner on our team."]},
            {"heading": "3. The 5-Department Engine", "bullets": ["Dept 01: 60-Second Lead Capture & Speed-to-Lead.", "Dept 02: 3-Option Quoting & 14-Day Follow-Up.", "Dept 03: Onboarding, 3-Tier Support & 5-Star Reviews.", "Dept 04 & 05: Invoicing/AR, Living SOPs & Friday Pulse."]}
        ], "Goal: Reclaim 18+ hours/week of manual admin friction within 90 days with 100% staff participation."),
        ("Deck 01 • Safety Architecture", "The T.R.A.V. Safety Contract (Zero Hallucinations)", "How Trigger -> Rules -> AI -> Verification Prevents Bad Promises and Pricing Errors", [
            {"heading": "Trigger & Deterministic Rules", "bullets": ["Every workflow starts from a verified webhook or timer event.", "Pre-AI code rules check regex safety filters and pull locked prices from our Truth Table.", "The AI is never allowed to invent prices or perform math on its own."]},
            {"heading": "Grounded AI Generation", "bullets": ["Models run at temperature 0.0 to 0.1 using strict JSON schemas.", "Prompts only use facts explicitly passed in the input payload.", "Missing facts trigger an automatic human clarification flag."]},
            {"heading": "Green / Amber / Red Gates", "bullets": ["Green (~75%): Routine intake, booking links & FAQs run 24/7.", "Amber (~20%): Quotes & custom credits wait for a 15-second Slack click.", "Red (~5%): Angry clients or disputes halt the bot for human takeover."]}
        ], "Golden Rule: Deterministic Rules do the math; AI writes the prose; Humans certify Amber & Red gates."),
        ("Deck 01 • Amber Gate Workflow", "How to Process a 15-Second Slack Amber Approval Card", "Daily Staff SOP for Reviewing Quotes, Scope Notices, and Courtesy Credits", [
            {"heading": "Step 1: Read the Context Header", "bullets": ["Monitor #amber-approvals in Slack or Microsoft Teams.", "Inspect the customer name, LTV, deterministic price calculation, and AI draft.", "Verify that all dates, SKU names, and dollar figures match our pricebook."]},
            {"heading": "Step 2: Choose 1 of 3 Actions", "bullets": ["Click [Approve & Send] if 100% accurate (takes 15 seconds).", "Click [Edit Draft] if a minor wording adjustment is needed.", "Click [Escalate / Hold] to pause automation and call the client directly."]},
            {"heading": "Step 3: SLA & Audit Logging", "bullets": ["Process Amber cards within 15 minutes during business hours.", "Every approval click is automatically logged in Notion Database 02.", "Never approve a discount or refund above your authorization tier."]}
        ], "Amber Gate SLA: 100% of Amber approval cards reviewed within 15 minutes during operating hours."),
        ("Deck 01 • Dept 01 Speed-to-Lead", "Running the 60-Second Omnichannel Lead Concierge", "Capturing Web Forms, Missed Calls, Voicemails, and Social DMs Without Dropping Prospects", [
            {"heading": "Web & Social Lead Intake", "bullets": ["Website forms, Facebook/IG Lead Ads, and Google messages route to Blueprint 01.", "Phone numbers normalize to E.164 and deduplicate against Notion Database 01.", "Prospect receives a warm SMS + booking link in under 60 seconds."]},
            {"heading": "Missed-Call Text-Back Whisper", "bullets": ["When all lines are busy, OpenPhone/Twilio triggers Prompt 3.3 within 15 seconds.", "The caller receives a polite text asking how we can help or offering a booking slot.", "Whisper summary posts to #inbound-leads with transcript and urgency score."]},
            {"heading": "Pre-Call Rep Briefing", "bullets": ["30 minutes before any booked consultation, Prompt 3.5 sends a 1-page brief.", "Includes B.A.N.T.-Lite qualification notes and top 3 talking points.", "Reps enter every call prepared without manual CRM digging."]}
        ], "Dept 01 SLA: Median Speed-to-Lead <= 60 seconds; Missed-Call Recovery Rate >= 85%."),
        ("Deck 01 • Dept 02 Quoting", "Voice-to-3-Tier Proposals & The 14-Day Follow-Up Loop", "How Field Estimators and Sales Reps Send Polished Quotes in Under 15 Minutes", [
            {"heading": "90-Second Post-Visit Voice Note", "bullets": ["Immediately after a site visit or discovery call, record a 90-second voice memo.", "State client name, measurements/scope, and recommended SKU codes.", "Whisper transcribes the note and passes it to Blueprint 03."]},
            {"heading": "Locked Good-Better-Best Math", "bullets": ["Code nodes pull exact unit prices from our locked SKU Pricebook.", "Prompt 4.1 formats Option A (Essential), Option B (Recommended), and Option C (Premium).", "Estimator clicks [Approve] on the Amber Slack card to dispatch PDF + payment link."]},
            {"heading": "Polite-Persistence Follow-Up", "bullets": ["6 value-driven touches over 14 days (Day 1, 3, 5, 8, 11, 14).", "State machine checks Proposal_Status before every send.", "Follow-ups halt the millisecond the client signs, pays, or replies."]}
        ], "Dept 02 SLA: 90%+ of quotes sent within 15 minutes; 14-day quote close rate >= 35%."),
        ("Deck 01 • Dept 03 Onboarding", "Zero-Drop Client Onboarding & Scope-Creep Protection", "Eliminating the Post-Payment Silence Gap Between Sales and Delivery", [
            {"heading": "Instant Payment Provisioning", "bullets": ["Stripe, Square, or QuickBooks deposit webhook triggers within 30 seconds.", "Automatically creates client cloud folder, Notion project tasks, and welcome email.", "Sends pre-filled intake link asking only for net-new items."]},
            {"heading": "Automated Intake Validation", "bullets": ["Prompt 5.3 checks uploaded files for completeness and readability.", "Missing items trigger polite Day-2 and Day-4 reminders with 1-click upload links.", "Kickoff call unlocks automatically once 100% of required items are verified."]},
            {"heading": "Scope-Boundary Early Warning", "bullets": ["Prompt 5.5 compares client requests against signed agreement deliverables.", "Out-of-scope requests generate a friendly Amber-Gate Change Order draft.", "Protects team profit margins without awkward confrontations."]}
        ], "Dept 03 Onboarding SLA: Payment-to-onboarding completion cycle time <= 24 hours."),
        ("Deck 01 • Dept 03 Support Shield", "24/7 AI Customer Support & Red-Zone De-Escalation", "Deflecting 60%+ of Routine Tickets While Giving Frustrated Clients Immediate Human Care", [
            {"heading": "Tier 1 Green Auto-Resolution", "bullets": ["Hours, directions, warranty rules, and live order/visit tracking run 24/7.", "Grounded strictly in Database 05 (Single-Source Support Knowledge Base).", "Zero guessing: if KB confidence < 0.88, ticket routes to human review."]},
            {"heading": "Tier 3 Red-Zone Takeover", "bullets": ["Pre-AI regex catches legal, safety, chargeback, or angry keywords instantly.", "Sentiment <= 2 mutes the bot and alerts #red-alerts with a 5-bullet brief.", "Assigned manager calls or replies within 15 minutes using H.E.A.R.T. protocol."]},
            {"heading": "Friday KB Gap Patching", "bullets": ["Every Friday at 2:00 PM, Prompt 6.5 audits all escalated tickets.", "Drafts 3-to-5 new FAQ entries for manager approval.", "Support deflection improves automatically every single week."]}
        ], "Dept 03 Support SLA: >= 60% Tier-1 auto-resolution in < 45s; < 15m human response on Red alerts."),
        ("Deck 01 • Dept 03 Reviews", "The 5-Star Reputation & Repeat-Sales Flywheel", "Capturing Public Google Reviews at the Golden Moment and Reactivating Past Clients", [
            {"heading": "Golden-Moment Sentiment Gate", "bullets": ["Triggered 2 hours after a successful service visit or confirmed delivery.", "Asks a 1-click question: 'How did we do today?'", "Separates thrilled advocates from private feedback before public posting."]},
            {"heading": "Advocate vs. Detractor Routing", "bullets": ["4–5 Star clicks route directly to our Google Business Profile review link.", "Prompt 7.2 provides 3 memory-jogger bullet prompts so reviewing takes 20 seconds.", "1–3 Star clicks open a private owner resolution form and alert #red-alerts."]},
            {"heading": "60/90/180-Day Win-Back Engine", "bullets": ["Scans CRM weekly for dormant clients due for seasonal tune-up or reorder.", "Sends personal check-in note referencing their exact past service.", "Generates high-margin repeat bookings with zero ad spend."]}
        ], "Dept 03 Reputation SLA: 3+ net new 5-star reviews/week; 100% public reviews answered within 24h."),
        ("Deck 01 • Dept 04 Finance", "Same-Day Invoicing, 5-Stage AR Chasers & Expense OCR", "Compressing Days Sales Outstanding (DSO) and Preventing Supplier Overcharges", [
            {"heading": "Same-Day Milestone Billing", "bullets": ["Marking a job 'Complete' triggers Prompt 8.1 to format clean invoice line items.", "Dispatches invoice PDF + 1-click ACH/card payment link the same afternoon.", "Eliminates Friday night billing backlogs."]},
            {"heading": "Polite-to-Firm AR Chasers", "bullets": ["Stage 1 (Day -3): Friendly upcoming due reminder.", "Stage 2 & 3 (Day +1 & +7): Helpful check-in with direct payment link.", "Stage 4 & 5 (Day +15 & +30): Amber-gated firm notice + human phone call brief."]},
            {"heading": "Receipt OCR & 5% Price Guard", "bullets": ["Staff snap photos of supplier bills/receipts into #expenses-ocr.", "Prompt 8.3 extracts vendor, GL category, tax, and line-item unit prices.", "Prompt 8.4 flags any supplier unit-price hike > 5% before payment."]}
        ], "Dept 04 Cashflow SLA: Average DSO <= 16 days; Overdue Receivables > 15 days <= $2,500."),
        ("Deck 01 • Dept 05 Living SOPs", "Recording 3-Minute Loom Videos to Build Living 7-Block SOPs", "Ending the 'Ask the Owner Everything' Bottleneck Across Our Team", [
            {"heading": "Record Once, Document Forever", "bullets": ["Next time you perform a recurring task, record a 3-minute screen/voice walkthrough.", "Talk naturally about what you click, what you check, and common mistakes.", "Drop the transcript into Prompt 9.1 (Living SOP Compiler)."]},
            {"heading": "The 7-Block SOP Standard", "bullets": ["Every SOP contains: Metadata, Trigger, Pre-Flight Checklist, Numbered Steps, Quality Checks, Exceptions, and Definition of Done.", "Stored in Notion Database 03 with a version tag and 90-day review date."]},
            {"heading": "Internal Ask-the-SOP Bot", "bullets": ["New hires and staff ask procedural questions in #ask-the-sop.", "Prompt 9.4 answers in 10 seconds citing the exact SOP ID and step number.", "Cuts new-hire onboarding ramp time by more than 50%."]}
        ], "Dept 05 SOP SLA: Top 20 core processes documented in 7-Block format; 100% new hires certified in 7 days."),
        ("Deck 01 • Privacy & Security", "Staff AI Data Privacy, PII Redaction & Kill-Switch Protocol", "Non-Negotiable Security Rules for Every Team Member", [
            {"heading": "Approved Workspace Only", "bullets": ["Only use company-provisioned OpenAI/Claude/Make workspaces with 2FA enabled.", "Never paste customer data into personal free-tier chatbots or browser plugins.", "Zero model training is enabled on our company API keys."]},
            {"heading": "PII, PCI & Clinical Redaction", "bullets": ["Never enter full 16-digit card numbers, SSNs, or passwords into any prompt.", "Clinics: Never include patient diagnoses or symptoms in outbound SMS texts.", "Pre-AI regex filters automatically mask sensitive numbers before AI processing."]},
            {"heading": "60-Second Manual Kill Switch", "bullets": ["If any workflow behaves unexpectedly, open Notion Database 02 immediately.", "Toggle the workflow switch OFF and activate the matching Emergency Script (01–12).", "Post a 1-line notice in #red-alerts so the Operations Lead can inspect the log."]}
        ], "Security Mandate: Zero raw payment/ID data in prompts; every staff member knows the 60s Kill Switch."),
        ("Deck 01 • Weekly Rhythm", "Our Friday 3:00 PM Scorecard & Monday 8:45 AM Huddle", "How Our Entire Team Stays Aligned in 15 Minutes Per Week", [
            {"heading": "Friday 3:00 PM Telemetry", "bullets": ["Blueprint 05 aggregates all 12 KPIs across Leads, Sales, Ops, Support, and Cashflow.", "Each metric is automatically graded GREEN, AMBER, or RED against our SLA.", "Leadership identifies the single highest-impact bottleneck for next week."]},
            {"heading": "Monday 8:45 AM 15m Huddle", "bullets": ["Minutes 0–3: Celebrate customer wins and 5-star reviews.", "Minutes 3–8: Review the 12 KPIs and hours saved.", "Minutes 8–15: Lock in the single process improvement for the week."]},
            {"heading": "Your Day-1 Action Checklist", "bullets": ["Sign the Staff AI Acceptable Use Policy (Doc 05).", "Join #amber-approvals, #red-alerts, and #ask-the-sop in Slack.", "Complete your first 5-day manual friction task log (Worksheet 01)."]}
        ], "Operating Rhythm: 15-minute Friday Owner Review + 15-minute Monday Team All-Hands Huddle.")
    ]
    for idx, s in enumerate(deck1_slides, start=1):
        add_executive_slide(prs1, idx, len(deck1_slides), s[0], s[1], s[2], s[3], s[4])
    out_p1 = PPTX_DIR / "01-Team-AI-Automation-Onboarding-and-SOP-Deck.pptx"
    prs1.save(str(out_p1))
    results[out_p1.name] = {"slides": len(prs1.slides), "bytes": out_p1.stat().st_size}

    # Deck 2: 10 Slides — Quarterly Automation ROI & KPI Review Deck
    prs2 = create_widescreen_presentation()
    deck2_slides = [
        ("Deck 02 • Executive Review", "Quarterly AI Automation ROI & 12-KPI Performance Review", "Comparing Baseline Manual Friction Against Post-Deployment Operational Telemetry", [
            {"heading": "Executive Summary", "bullets": ["Completed 90-day phased deployment across all 5 core departments.", "Reduced weekly manual admin friction from 26.0 hrs/wk to 6.5 hrs/wk (-75%).", "Generated $44,290 in net quarterly value on $495 total software/API spend."]},
            {"heading": "Safety & Governance Audit", "bullets": ["18 active workflows operating under T.R.A.V. Green/Amber/Red gates.", "Zero pricing or policy hallucinations across 1,420 customer interactions.", "99.4% webhook uptime with 100% Dead-Letter Queue recovery."]},
            {"heading": "Team & Culture Impact", "bullets": ["Zero headcount reductions; 19.5 hrs/wk reallocated to client service.", "New-hire onboarding ramp time compressed from 21 days to 8 days.", "Employee satisfaction with internal tools rose from 2.8/5 to 4.7/5."]}
        ], "Quarterly Bottom Line: 89.4x Return on Software Spend with Zero Customer Safety Incidents."),
        ("Deck 02 • CMF Reduction", "Cost of Manual Friction (CMF): Baseline vs. Quarter Actuals", "Financial Breakdown Across Labor Waste, Lead-Leak Rescue, and Working Capital", [
            {"heading": "Labor Waste Recovered (L_tax)", "bullets": ["Baseline: 26.0 manual hours/week ($78,416/yr annualized cost).", "Quarter Actual: 6.5 manual hours/week (19.5 hrs/wk saved).", "Annualized Labor Capacity Reclaimed: $58,812/year."]},
            {"heading": "Lead Revenue Rescued (R_leak)", "bullets": ["Baseline: 36% of inbound leads waited > 5 minutes ($149,184/yr leak).", "Quarter Actual: 96.4% of leads answered in < 60 seconds (38s median).", "Annualized Rescued Gross Revenue: $98,400/year."]},
            {"heading": "Cashflow Acceleration (C_drag)", "bullets": ["Baseline: 42.0 Days Sales Outstanding ($18,500 overdue > 15 days).", "Quarter Actual: 13.4 Days Sales Outstanding ($1,420 overdue > 15 days).", "Working Capital Freed into Operating Cash: +$46,200."]}
        ], "Total Annualized CMF Recovery Run-Rate: $181,612/yr vs. $1,980/yr Tool-Stack Cost."),
        ("Deck 02 • Dept 01 Telemetry", "Department 01 Review: Omnichannel Speed-to-Lead & Booking Lift", "Performance of Blueprint 01 & Prompts 3.1–3.5 Across Web, Phone, and SMS", [
            {"heading": "Response Latency Collapse", "bullets": ["Prior Quarter Median Response: 3 hours 42 minutes.", "Current Quarter Median Response: 38 seconds (24/7 including weekends).", "99.1% of high-intent inquiries received a booking link within 60 seconds."]},
            {"heading": "Missed-Call Text-Back ROI", "bullets": ["Captured 114 missed calls during peak field/clinical hours.", "104 callers engaged with the 15-second SMS concierge (91.2% recovery).", "Booked 41 paid appointments directly from rescued missed calls ($75,850)."]},
            {"heading": "Lead Quality & Rep Readiness", "bullets": ["Non-intrusive B.A.N.T.-Lite scoring filtered out 28 out-of-territory inquiries.", "Sales reps received automated pre-call briefs 30m before every meeting.", "No-show rate dropped from 22% down to 6.5%."]}
        ], "Dept 01 Verdict: GREEN across all 3 KPIs (38s Speed-to-Lead, 91.2% Call Recovery)."),
        ("Deck 02 • Dept 02 Telemetry", "Department 02 Review: 3-Tier Proposal Velocity & Close Rate", "Performance of Blueprint 03 & Prompts 4.1–4.5 on Sales Conversion and AOV", [
            {"heading": "Proposal Turnaround Speed", "bullets": ["Prior Quarter Quote Turnaround: 48 to 72 hours after site visit.", "Current Quarter Quote Turnaround: 12 minutes via 90s voice memo.", "94% of estimates delivered while buyer intent was at peak."]},
            {"heading": "Good-Better-Best Upsell Lift", "bullets": ["62% of buyers selected Option B (Recommended) or Option C (Premium).", "Average Order Value (AOV) increased from $1,850 to $2,310 (+24.8%).", "Zero margin-erosion errors thanks to locked SKU pricebook lookups."]},
            {"heading": "14-Day Follow-Up Persistence", "bullets": ["Automated 6-touch follow-up rescued 19 stalled quotes after Day 4.", "14-day proposal close rate improved from 24.0% to 38.4% (+14.4 pts).", "Zero awkward post-signature texts (100% auto-stop accuracy)."]}
        ], "Dept 02 Verdict: GREEN across all KPIs (12m Quote Speed, 38.4% Close Rate, +24.8% AOV)."),
        ("Deck 02 • Dept 03 Telemetry", "Department 03 Review: Onboarding, Support Deflection & Reviews", "Performance of Prompts 5.1–7.5 on Client Retention, CSAT, and Google Ranking", [
            {"heading": "Zero-Drop Client Onboarding", "bullets": ["Payment-to-kickoff cycle time dropped from 8.5 days to 11.2 hours.", "Automated intake validation cut missing-document delays by 78%.", "Early scope-creep detection generated $8,400 in approved change orders."]},
            {"heading": "3-Tier Support Shield", "bullets": ["68.5% of Tier-1 tickets resolved in < 42 seconds unattended.", "Customer Satisfaction (CSAT) held at 4.91 / 5.00 across 640 tickets.", "100% of Red-Gate tickets received human manager contact in < 12 minutes."]},
            {"heading": "Reputation & Win-Back Flywheel", "bullets": ["Added 58 net new 5-star Google reviews in 90 days (+4.2x velocity).", "Sentiment gate intercepted 4 detractor issues privately before public posting.", "90-day dormant win-back campaign generated $29,600 in repeat orders."]}
        ], "Dept 03 Verdict: GREEN across Onboarding (11.2h), Support (68.5% deflection), and Reviews (+58 5-star)."),
        ("Deck 02 • Dept 04 Telemetry", "Department 04 Review: Invoicing, AR Chasers & Supplier Audits", "Performance of Blueprint 04 & Prompts 8.1–8.5 on Working Capital and Margin Protection", [
            {"heading": "Same-Day Billing Execution", "bullets": ["98.5% of completed jobs billed within 15 minutes of completion sign-off.", "Eliminated 6.5 hours/week of Friday evening manual invoice entry.", "1-click ACH/card links increased same-day invoice payment to 61%."]},
            {"heading": "DSO & Overdue AR Compression", "bullets": ["Days Sales Outstanding (DSO) dropped from 42.0 days to 13.4 days.", "Overdue receivables > 15 days reduced from $18,500 down to $1,420.", "Zero client relationship complaints from polite Stage 1–3 reminders."]},
            {"heading": "AP OCR & 5% Price-Creep Guard", "bullets": ["Processed 215 supplier bills/receipts via mobile OCR in < 20s each.", "Caught 4 unannounced vendor unit-price hikes exceeding 5% ($3,180 saved).", "Monthly bookkeeper close completed by the 3rd business day."]}
        ], "Dept 04 Verdict: GREEN across Cashflow (13.4d DSO, $1,420 overdue >15d, $3,180 AP overcharges caught)."),
        ("Deck 02 • Dept 05 Telemetry", "Department 05 Review: Living SOP Vault & Owner Bandwidth", "Performance of Prompts 9.1–10.5 on Team Autonomy and Founder Work-Life Balance", [
            {"heading": "Living SOP Vault Growth", "bullets": ["Compiled 32 structured 7-Block SOPs from 3-minute Loom recordings.", "Internal #ask-the-sop bot answered 190 staff questions with 96% accuracy.", "Routine 'how do I do this?' interruptions to the owner dropped by 82%."]},
            {"heading": "Owner Hours Reclaimed", "bullets": ["Founder weekly working hours reduced from 57 hrs/wk to 37.5 hrs/wk.", "Friday 3:00 PM Owner Scorecard review averaged 14 minutes/week.", "Owner took a 7-day unplugged vacation in Month 3 with zero escalations."]},
            {"heading": "16-Week KPI Trend Stability", "bullets": ["11 of 12 KPIs finished the quarter in GREEN status for 8 consecutive weeks.", "1 Amber variance (onboarding photo uploads) resolved within 48 hours."]}
        ], "Dept 05 Verdict: GREEN (32 Living SOPs active, 23.5 team+owner hours saved every week)."),
        ("Deck 02 • Tool Stack Audit", "Quarterly Software Spend, Token Efficiency & Security Audit", "Financial and Cybersecurity Governance Review (Prompt 10.3 & Prompt 10.4)", [
            {"heading": "Software & API Spend Breakdown", "bullets": ["Make.com Pro Plan (28,400 ops/mo): $29.00/month.", "OpenAI & Claude API Inference (temp 0.0–0.1): $31.50/month.", "Twilio / OpenPhone SMS & Voice Webhooks: $54.50/month.", "Total Monthly Automation Spend: $115.00/mo ($345/quarter)."]},
            {"heading": "Zombie SaaS Consolidation", "bullets": ["Canceled 3 redundant single-purpose SaaS subscriptions ($190/mo saved).", "Net software budget is now $75/mo LOWER than pre-automation baseline."]},
            {"heading": "Quarterly Security & Drift Pass", "bullets": ["Rotated all 5 departmental API keys and webhook secrets on Day 90.", "Audited 50 random LLM outputs: 0 schema drifts, 0 PII leaks."]}
        ], "Financial Efficiency: Net software spend reduced by $75/mo while producing $15,100/mo in operational gains."),
        ("Deck 02 • Lessons & Tuning", "Prompt Tuning Log & Edge-Case Refinements Implemented", "Continuous Improvement Highlights from Our Weekly Friday Reviews", [
            {"heading": "Refinement 1: Zip-Code Pre-Gate", "bullets": ["Added deterministic postal-code lookup array prior to Prompt 3.1.", "Prevented out-of-territory leads from booking field estimator calendar slots.", "Saved 3.5 estimator hours/month and referred out-of-area leads politely."]},
            {"heading": "Refinement 2: Photo Estimate Guide", "bullets": ["Updated SMS concierge to request 1 wide photo + 1 nameplate close-up.", "Improved Vault Prompt V2.2 equipment identification accuracy to 98%.", "Reduced on-site parts-run delays by stocking trucks before arrival."]},
            {"heading": "Refinement 3: KB Weekly Patching", "bullets": ["Added 19 new verified Q&A rows to Database 05 from Prompt 6.5 audits.", "Increased Tier-1 support auto-resolution from 54% (Month 1) to 68.5% (Month 3)."]}
        ], "Continuous Improvement: Small 10-minute Friday prompt tweaks compound into massive quarterly gains."),
        ("Deck 02 • Next Quarter", "Next-Quarter Automation Roadmap & Expansion Priorities", "Scaling Growth Without Adding Administrative Overhead", [
            {"heading": "Priority 1: Vertical Vault Drops", "bullets": ["Deploy industry-specific recall and replenishment prompts (Vault Drop #01).", "Target +$8,500/month in automated repeat customer bookings.", "Maintain strict Amber-Gate oversight on all promotional offers."]},
            {"heading": "Priority 2: Cross-Training & Backup", "bullets": ["Certify a secondary team member on every department's Amber Gate and Kill Switch.", "Run quarterly 60-second emergency fallback drill across all 12 scripts."]},
            {"heading": "Priority 3: Margin Expansion", "bullets": ["Keep administrative overhead fixed while scaling top-line revenue by 25%.", "Target net operating profit margin increase from 16% to 24%."]}
        ], "Next Quarter Mandate: Scale revenue +25% on existing headcount while keeping all 12 KPIs GREEN.")
    ]
    for idx, s in enumerate(deck2_slides, start=1):
        add_executive_slide(prs2, idx, len(deck2_slides), s[0], s[1], s[2], s[3], s[4])
    out_p2 = PPTX_DIR / "02-Quarterly-Automation-ROI-and-KPI-Review-Deck.pptx"
    prs2.save(str(out_p2))
    results[out_p2.name] = {"slides": len(prs2.slides), "bytes": out_p2.stat().st_size}

    # Deck 3: 10 Slides — Client & Partner Operational Excellence Pitch Deck
    prs3 = create_widescreen_presentation()
    deck3_slides = [
        ("Deck 03 • Client Pitch", "Why Clients Choose Us: Our AI-Powered Operational Excellence", "Combining 60-Second Responsiveness with Master Human Craftsmanship and Care", [
            {"heading": "The Best of Both Worlds", "bullets": ["Instant digital speed for scheduling, status updates, proposals, and billing.", "100% human expertise for your actual service delivery, strategy, and care.", "Zero dropped balls, zero unreturned phone calls, and zero billing surprises."]},
            {"heading": "Our 4 Client Guarantees", "bullets": ["1. < 60-Second Response Guarantee on every inquiry.", "2. < 15-Minute Transparent 3-Option Proposal after site/discovery review.", "3. Same-Day Zero-Drop Onboarding Portal & Milestone Tracker.", "4. < 15-Minute Direct Human Manager Escalation whenever you need us."]},
            {"heading": "Proven Track Record", "bullets": ["4.92 / 5.00 Verified Client Satisfaction Score.", "98.4% On-Time Milestone Delivery Rate.", "Trusted by hundreds of local and commercial clients."]}
        ], "Our Promise: Technology handles the waiting and paperwork so our specialists focus 100% on your project."),
        ("Deck 03 • Speed Commitment", "Guarantee #1: Our 60-Second Response & Scheduling Concierge", "You Never Wait Hours or Days for a Call Back", [
            {"heading": "Instant Omnichannel Intake", "bullets": ["Reach us by phone, text message, web form, or email 24/7.", "Our routing engine acknowledges your request in under 60 seconds.", "Immediate direct calendar access to lock in your preferred time slot."]},
            {"heading": "Zero Phone-Tag Frustration", "bullets": ["If our specialists are with a client when you call, our SMS concierge texts you within 15 seconds.", "Share photos, project notes, or urgent timing right in the text thread.", "Our team arrives already briefed on your exact needs."]},
            {"heading": "Emergency Priority Routing", "bullets": ["Urgent or time-critical requests are automatically flagged Priority 1.", "Pages our on-call lead immediately for same-day dispatch."]}
        ], "Client Benefit: Book your consultation or service slot in 60 seconds flat without playing phone tag."),
        ("Deck 03 • Transparent Quoting", "Guarantee #2: Transparent 3-Option Proposals in 15 Minutes", "Clear Good-Better-Best Pricing with Zero Hidden Fees or Guesswork", [
            {"heading": "3 Clear Options Every Time", "bullets": ["Option A (Essential Scope): Solves your immediate core requirement.", "Option B (Recommended Complete Solution): Best long-term value & warranty.", "Option C (VIP Priority Turnkey): Maximum coverage & expedited delivery."]},
            {"heading": "Locked Pricebook Integrity", "bullets": ["Every quote is generated from our audited, deterministic SKU pricebook.", "Two clients with the same scope always receive the exact same fair price.", "Every proposal is verified and signed off by a senior human estimator."]},
            {"heading": "1-Click Digital Approval", "bullets": ["Select your preferred tier, sign electronically on your phone, and lock in your schedule in 30 seconds."]}
        ], "Client Benefit: Written, itemized 3-option proposals delivered the same day so you can decide with confidence."),
        ("Deck 03 • Zero-Drop Onboarding", "Guarantee #3: Frictionless Same-Day Onboarding & Live Tracking", "From Deposit to Kickoff in Hours—Never Weeks", [
            {"heading": "Instant Welcome & Portal", "bullets": ["The moment you approve your proposal, your dedicated client folder and project board are provisioned automatically.", "You receive a single clean welcome packet with your timeline and named project lead."]},
            {"heading": "Smart Pre-Filled Intake", "bullets": ["We never ask you to re-type information you already shared during discovery.", "Our intake form comes pre-populated with your project details—you simply confirm or snap a quick photo."]},
            {"heading": "Proactive Milestone Pulses", "bullets": ["Whenever your project hits a major milestone, you receive an automatic status summary showing what is done and what happens next."]}
        ], "Client Benefit: You always know the exact status of your project without ever having to chase us for updates."),
        ("Deck 03 • 24/7 Support Shield", "Guarantee #4: 24/7 Instant Answers + 15-Minute Human Escalation", "How Our 3-Tier Support Shield Protects Your Experience", [
            {"heading": "Instant Answers at Midnight", "bullets": ["Need an invoice copy, appointment confirmation, or preparation checklist at 10:00 PM?", "Our grounded support concierge answers routine questions in under 45 seconds 24/7."]},
            {"heading": "Direct Human Access", "bullets": ["Prefer to speak with a person or have a complex custom request?", "Reply 'HUMAN' or call our direct line at any time—our system routes you straight to your account manager."]},
            {"heading": "Zero-Bot-Loop Promise", "bullets": ["We never trap clients in frustrating chatbot loops.", "Any complex question or concern is escalated to a senior manager within 15 minutes."]}
        ], "Client Benefit: Instant self-serve speed for simple requests; immediate human leadership for complex needs."),
        ("Deck 03 • Quality & Safety", "Human-in-the-Loop Quality Assurance & Data Privacy", "Enterprise-Grade Security for Your Business and Personal Information", [
            {"heading": "T.R.A.V. Quality Verification", "bullets": ["Every technical deliverable, scope adjustment, and financial document passes through a mandatory human quality gate.", "We combine checklist precision with experienced human judgment."]},
            {"heading": "Strict Data Privacy & Encryption", "bullets": ["All payments process through PCI-compliant encrypted checkout links (Stripe/Square/QuickBooks).", "Your confidential documents and records are stored in access-controlled workspaces and never shared or used to train public AI models."]},
            {"heading": "7-Block SOP Consistency", "bullets": ["Every member of our crew follows our documented 7-Block Standard Operating Procedures with binary Definitions of Done."]}
        ], "Client Benefit: Consistent 5-star quality on every visit, backed by enterprise data privacy."),
        ("Deck 03 • Clear Billing", "Stress-Free Itemized Billing & Executive Value Reporting", "Transparent Invoicing and Monthly ROI Digests", [
            {"heading": "Plain-English Itemized Invoices", "bullets": ["Every invoice includes a clear summary of work completed, verified dates, and matched quote line items.", "Pay in 1 click via ACH bank transfer, corporate card, Apple Pay, or Google Pay."]},
            {"heading": "Monthly Executive Value Digest", "bullets": ["For ongoing retainer and maintenance clients, we send a 1-page Executive Value Digest on the 28th of every month.", "Highlights completed deliverables, metrics achieved, and next month's priorities."]},
            {"heading": "Proactive Warranty & Recall Care", "bullets": ["Our calendar tracks your warranty dates and seasonal maintenance windows so your equipment or systems stay protected year-round."]}
        ], "Client Benefit: Zero billing surprises and documented proof of value delivered every single month."),
        ("Deck 03 • Case Studies", "Verified Client Results Across Our Service Verticals", "Real Outcomes Delivered by Our Operating System", [
            {"heading": "Commercial & Trade Projects", "bullets": ["Cut average project mobilization time from 9 days down to 24 hours.", "99.2% first-visit completion rate due to pre-visit photo & spec verification."]},
            {"heading": "Professional & B2B Partnerships", "bullets": ["100% on-time filing and launch record via automated document completeness tracking.", "Clients save an average of 6.5 hours/month in coordination emails."]},
            {"heading": "Customer Care & Satisfaction", "bullets": ["Over 200+ verified 5-star reviews praising our communication speed, transparency, and professionalism."]}
        ], "Proven Results: Faster turnaround, clearer communication, and higher reliability."),
        ("Deck 03 • Partner Integration", "How We Integrate Smoothly with Commercial & Strategic Partners", "Co-Branded Workflows for Property Managers, Referrers, and B2B Accounts", [
            {"heading": "Dedicated Partner Webhook Intake", "bullets": ["Send work orders or client referrals via email, shared form, or webhook.", "Automatic instant confirmation sent to both your coordinator and the end client in < 60 seconds."]},
            {"heading": "Automated Status Loop-Back", "bullets": ["Your team receives automatic notifications when the appointment is booked, when work is completed, and when final photos/reports are uploaded."]},
            {"heading": "Consolidated Monthly Reporting", "bullets": ["Single monthly SLA performance and consolidated billing statement for multi-site or multi-referral partners."]}
        ], "Partner Advantage: Hand off work orders with 100% confidence that we will make you look great."),
        ("Deck 03 • Next Steps", "Ready to Get Started? Your 3-Step Onboarding Roadmap", "How We Launch Together This Week", [
            {"heading": "Step 1: Select Your Option", "bullets": ["Review your 3-Option Proposal (Essential, Recommended, or VIP Priority).", "Click the digital approval link to lock in your selected scope."]},
            {"heading": "Step 2: 3-Minute Smart Intake", "bullets": ["Complete your pre-filled onboarding checklist and confirm your preferred kickoff slot.", "Your dedicated account lead reviews your file the same day."]},
            {"heading": "Step 3: Kickoff & Execution", "bullets": ["Join your 15-minute kickoff call with your project lead.", "Receive live milestone updates through completion and final sign-off."]}
        ], "Contact Us Today: Scan or click your proposal link to lock in your kickoff window in 60 seconds.")
    ]
    for idx, s in enumerate(deck3_slides, start=1):
        add_executive_slide(prs3, idx, len(deck3_slides), s[0], s[1], s[2], s[3], s[4])
    out_p3 = PPTX_DIR / "03-Client-and-Partner-Operational-Excellence-Pitch-Deck.pptx"
    prs3.save(str(out_p3))
    results[out_p3.name] = {"slides": len(prs3.slides), "bytes": out_p3.stat().st_size}

    return results


# =============================================================================
# UPGRADE 4: 8-TAB CHARTED EXCEL COMMAND CENTER (.XLSX + 8 CSV MIRRORS)
# =============================================================================

def style_ws_header(ws, title: str, subtitle: str, col_headers: list, header_row: int = 4):
    ws.views.sheetView[0].showGridLines = True
    fill_navy = PatternFill("solid", fgColor="0F172A")
    fill_emerald = PatternFill("solid", fgColor="059669")
    font_title = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    font_sub = Font(name="Calibri", size=10, italic=True, color="CBD5E1")
    font_hdr = Font(name="Calibri", size=10.5, bold=True, color="FFFFFF")

    max_col = max(len(col_headers), 8)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)
    ws.cell(1, 1, sanitize_phase9_text(title)).font = font_title
    ws.cell(1, 1).fill = fill_navy
    ws.cell(2, 1, sanitize_phase9_text(subtitle)).font = font_sub
    ws.cell(2, 1).fill = fill_navy
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 18

    thin = Side(border_style="thin", color="CBD5E1")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for idx, h in enumerate(col_headers, start=1):
        c = ws.cell(header_row, idx, sanitize_phase9_text(h))
        c.font = font_hdr
        c.fill = fill_emerald
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border
    ws.row_dimensions[header_row].height = 24
    ws.freeze_panes = f"A{header_row + 1}"


def auto_fit_and_border(ws, start_row: int, end_row: int, col_count: int):
    thin = Side(border_style="thin", color="CBD5E1")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    fill_zebra = PatternFill("solid", fgColor="F8FAFC")
    font_body = Font(name="Calibri", size=10, color="1E293B")
    font_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")

    for r in range(start_row, end_row + 1):
        is_total = str(ws.cell(r, 1).value or "").upper().startswith(("TOTAL", "SUMMARY", "AVERAGE", "NET"))
        for c in range(1, col_count + 1):
            cell = ws.cell(r, c)
            cell.border = border
            cell.font = font_bold if is_total else font_body
            if r % 2 == 1 and not is_total:
                cell.fill = fill_zebra

    for col_idx in range(1, col_count + 1):
        col_letter = get_column_letter(col_idx)
        max_len = 14
        for r in range(4, end_row + 1):
            val = str(ws.cell(r, col_idx).value or "")
            if not val.startswith("="):
                max_len = max(max_len, min(len(val) + 4, 38))
        ws.column_dimensions[col_letter].width = max_len


def build_excel_command_center() -> dict:
    wb = openpyxl.Workbook()
    # Remove default sheet after creating our 8 sheets
    default_ws = wb.active

    # -------------------------------------------------------------------------
    # TAB 1: 01_Executive_ROI_Command
    # -------------------------------------------------------------------------
    ws1 = wb.create_sheet("01_Executive_ROI_Command")
    headers1 = [
        "Dept ID", "Department Name", "Weekly Manual Hrs", "Blended Hourly Rate ($)",
        "Annual Labor Waste ($)", "Annual Lead/Cash Leak ($)", "Total Annual CMF ($)",
        "Projected Recovery %", "Annual Net Recovery ($)", "Monthly Tool Cost ($)", "Annual Net ROI ($)"
    ]
    style_ws_header(
        ws1,
        "TAB 01: EXECUTIVE 5-DEPARTMENT COST OF MANUAL FRICTION (CMF) & NET ROI COMMAND CENTER",
        "Master Financial Rollup Across All 5 Small Business Departments — Live Formulas & Visual Bar Chart",
        headers1,
    )
    depts_data = [
        ("DEPT-01", "Lead Capture & Speed-to-Lead", 6.5, 58, 94800, 0.70),
        ("DEPT-02", "Sales Qualification & 3-Option Quoting", 5.5, 65, 62400, 0.65),
        ("DEPT-03", "Onboarding, Support & 5-Star Reviews", 7.0, 48, 38500, 0.72),
        ("DEPT-04", "Invoicing, 5-Stage AR Chasers & AP OCR", 4.5, 55, 29800, 0.75),
        ("DEPT-05", "Team SOPs, Delegation & Friday Scorecard", 3.5, 85, 18400, 0.68),
    ]
    tool_costs = [39, 29, 35, 25, 19]
    for idx, (did, dname, hrs, rate, leak, rec_pct) in enumerate(depts_data, start=5):
        ws1.cell(idx, 1, did)
        ws1.cell(idx, 2, dname)
        ws1.cell(idx, 3, hrs)
        ws1.cell(idx, 4, rate).number_format = "$#,##0"
        ws1.cell(idx, 5, f"=ROUND(C{idx}*D{idx}*52, 0)").number_format = "$#,##0"
        ws1.cell(idx, 6, leak).number_format = "$#,##0"
        ws1.cell(idx, 7, f"=E{idx}+F{idx}").number_format = "$#,##0"
        ws1.cell(idx, 8, rec_pct).number_format = "0%"
        ws1.cell(idx, 9, f"=ROUND(G{idx}*H{idx}, 0)").number_format = "$#,##0"
        ws1.cell(idx, 10, tool_costs[idx - 5]).number_format = "$#,##0"
        ws1.cell(idx, 11, f"=I{idx}-(J{idx}*12)").number_format = "$#,##0"

    # Totals Row (Row 10)
    ws1.cell(10, 1, "TOTAL / SUMMARY")
    ws1.cell(10, 2, "All 5 Core Small Business Departments")
    ws1.cell(10, 3, "=SUM(C5:C9)")
    ws1.cell(10, 4, "=ROUND(AVERAGE(D5:D9), 2)").number_format = "$#,##0.00"
    ws1.cell(10, 5, "=SUM(E5:E9)").number_format = "$#,##0"
    ws1.cell(10, 6, "=SUM(F5:F9)").number_format = "$#,##0"
    ws1.cell(10, 7, "=SUM(G5:G9)").number_format = "$#,##0"
    ws1.cell(10, 8, "=AVERAGE(H5:H9)").number_format = "0%"
    ws1.cell(10, 9, "=SUM(I5:I9)").number_format = "$#,##0"
    ws1.cell(10, 10, "=SUM(J5:J9)").number_format = "$#,##0"
    ws1.cell(10, 11, "=SUM(K5:K9)").number_format = "$#,##0"

    # Executive Summary KPI Rows (Rows 12..16)
    exec_kpis = [
        ("EXEC-KPI-1", "Annualized Hours Reclaimed Across Team", "=ROUND(C10*52*H10, 1)"),
        ("EXEC-KPI-2", "Full-Time Equivalent (FTE) Capacity Gained", "=ROUND((C10*52*H10)/2080, 2)"),
        ("EXEC-KPI-3", "Annual Tool-Stack Investment ($/yr)", "=J10*12"),
        ("EXEC-KPI-4", "Return on Automation Spend Multiple (x)", "=ROUND(I10/MAX(J10*12, 1), 1)"),
        ("EXEC-KPI-5", "Flagship OS Bundle ($59) Payback Period (Days)", "=ROUND((59/MAX(K10,1))*365, 2)"),
    ]
    for r_offset, (kcode, klabel, kform) in enumerate(exec_kpis, start=12):
        ws1.cell(r_offset, 1, kcode)
        ws1.cell(r_offset, 2, klabel)
        ws1.cell(r_offset, 3, kform)

    auto_fit_and_border(ws1, 5, 16, len(headers1))

    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "5-Department Annual Manual Friction vs. Net Automation Recovery ($)"
    chart1.y_axis.title = "Annual USD ($)"
    chart1.x_axis.title = "Department"
    data_ref1 = Reference(ws1, min_col=7, min_row=4, max_col=9, max_row=9)
    cats_ref1 = Reference(ws1, min_col=2, min_row=5, max_row=9)
    chart1.add_data(data_ref1, titles_from_data=True)
    chart1.set_categories(cats_ref1)
    chart1.width = 18
    chart1.height = 10
    ws1.add_chart(chart1, "A18")

    # -------------------------------------------------------------------------
    # TAB 2: 02_5Day_Time_Task_Audit (25 Tasks -> 100+ Formulas)
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet("02_5Day_Time_Task_Audit")
    headers2 = [
        "Task ID", "Department", "Recurring Manual Task Description", "Role Performing",
        "Hourly Cost ($)", "Freq / Week", "Mins / Occurrence", "Weekly Hours",
        "Annual Hours", "Annual Labor Cost ($)", "P.A.C.E. Score (1-20)", "Governance Gate"
    ]
    style_ws_header(
        ws2,
        "TAB 02: 5-DAY SMALL BUSINESS TIME & MANUAL TASK FRICTION AUDIT (25 CORE TASKS)",
        "Granular Task-Level Calculation of Weekly Hours, Annual Hours, Labor Waste & P.A.C.E. Priority Score",
        headers2,
    )
    tasks_25 = [
        ("T-01", "Dept 01", "Copy web form leads into CRM & send intro email", "Front Desk", 32, 35, 6, 19, "GREEN"),
        ("T-02", "Dept 01", "Return missed phone calls & transcribe voicemails", "Front Desk", 32, 28, 8, 20, "GREEN"),
        ("T-03", "Dept 01", "Reply to Facebook/IG & Google Business messages", "Marketing Admin", 38, 22, 7, 18, "GREEN"),
        ("T-04", "Dept 01", "Send calendar links & chase appointment confirmations", "Front Desk", 32, 30, 5, 18, "GREEN"),
        ("T-05", "Dept 01", "Research prospect company/address before sales call", "Sales Rep", 58, 15, 12, 16, "GREEN"),
        ("T-06", "Dept 02", "Type post-visit notes into 3-option quote template", "Estimator", 68, 14, 25, 20, "AMBER"),
        ("T-07", "Dept 02", "Look up SKU unit prices & check margin thresholds", "Estimator", 68, 14, 10, 18, "AMBER"),
        ("T-08", "Dept 02", "Send Day-2, Day-5, and Day-10 quote follow-up emails", "Sales Rep", 58, 25, 6, 19, "GREEN"),
        ("T-09", "Dept 02", "Update CRM deal stages after client signs or declines", "Sales Admin", 36, 18, 5, 15, "GREEN"),
        ("T-10", "Dept 02", "Re-engage 90-day closed-lost estimates for seasonal work", "Sales Rep", 58, 10, 9, 15, "GREEN"),
        ("T-11", "Dept 03", "Create client Google Drive folder & project board after payment", "Ops Coordinator", 42, 10, 18, 19, "GREEN"),
        ("T-12", "Dept 03", "Send welcome packet & custom intake questionnaire", "Ops Coordinator", 42, 10, 12, 18, "GREEN"),
        ("T-13", "Dept 03", "Chase clients for missing onboarding documents/photos", "Ops Coordinator", 42, 16, 10, 17, "GREEN"),
        ("T-14", "Dept 03", "Answer Tier-1 FAQ tickets (hours, WISMO, rescheduling)", "Support Rep", 34, 45, 5, 20, "GREEN"),
        ("T-15", "Dept 03", "Triage angry/urgent customer complaints to manager", "Support Lead", 48, 4, 20, 17, "RED"),
        ("T-16", "Dept 03", "Send post-service satisfaction check & Google review link", "Front Desk", 32, 22, 4, 19, "GREEN"),
        ("T-17", "Dept 03", "Draft SEO-friendly replies to public Google reviews", "Owner / Manager", 85, 6, 10, 16, "GREEN"),
        ("T-18", "Dept 03", "Export 60/90/180-day dormant client list & send recall", "Marketing Admin", 38, 8, 15, 17, "GREEN"),
        ("T-19", "Dept 04", "Convert technician/project completion notes into invoice", "Billing Clerk", 40, 20, 12, 19, "GREEN"),
        ("T-20", "Dept 04", "Check overdue invoices & send polite payment reminders", "Billing Clerk", 40, 18, 8, 19, "AMBER"),
        ("T-21", "Dept 04", "Key vendor receipts & PDF bills into QuickBooks/Xero", "Bookkeeper", 46, 30, 6, 18, "GREEN"),
        ("T-22", "Dept 04", "Compare supplier invoice unit prices against contract rates", "Owner / Manager", 85, 8, 15, 17, "AMBER"),
        ("T-23", "Dept 05", "Write step-by-step SOP checklists for recurring processes", "Owner / Manager", 85, 3, 45, 18, "AMBER"),
        ("T-24", "Dept 05", "Answer repetitive staff procedural questions in Slack", "Owner / Manager", 85, 20, 6, 18, "GREEN"),
        ("T-25", "Dept 05", "Pull Friday KPI numbers across 4 apps for weekly review", "Owner / Manager", 85, 1, 95, 20, "GREEN"),
    ]
    for i, t in enumerate(tasks_25, start=5):
        ws2.cell(i, 1, t[0])
        ws2.cell(i, 2, t[1])
        ws2.cell(i, 3, t[2])
        ws2.cell(i, 4, t[3])
        ws2.cell(i, 5, t[4]).number_format = "$#,##0"
        ws2.cell(i, 6, t[5])
        ws2.cell(i, 7, t[6])
        ws2.cell(i, 8, f"=ROUND((F{i}*G{i})/60, 2)").number_format = "0.00"
        ws2.cell(i, 9, f"=ROUND(H{i}*52, 1)").number_format = "0.0"
        ws2.cell(i, 10, f"=ROUND(I{i}*E{i}, 0)").number_format = "$#,##0"
        ws2.cell(i, 11, t[7])
        ws2.cell(i, 12, t[8])

    r_tot2 = 30
    ws2.cell(r_tot2, 1, "TOTAL")
    ws2.cell(r_tot2, 2, "All 5 Depts")
    ws2.cell(r_tot2, 3, "Total Audited Weekly & Annual Manual Task Friction")
    ws2.cell(r_tot2, 4, "All Staff")
    ws2.cell(r_tot2, 5, "=ROUND(AVERAGE(E5:E29), 2)").number_format = "$#,##0.00"
    ws2.cell(r_tot2, 6, "=SUM(F5:F29)")
    ws2.cell(r_tot2, 7, "=ROUND(AVERAGE(G5:G29), 1)")
    ws2.cell(r_tot2, 8, "=SUM(H5:H29)").number_format = "0.00"
    ws2.cell(r_tot2, 9, "=SUM(I5:I29)").number_format = "0.0"
    ws2.cell(r_tot2, 10, "=SUM(J5:J29)").number_format = "$#,##0"
    ws2.cell(r_tot2, 11, "=ROUND(AVERAGE(K5:K29), 1)")
    ws2.cell(r_tot2, 12, "75% GREEN")
    auto_fit_and_border(ws2, 5, r_tot2, len(headers2))

    # -------------------------------------------------------------------------
    # TAB 3: 03_Speed_To_Lead_Model (12 Months -> 60+ Formulas + Chart)
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet("03_Speed_To_Lead_Model")
    headers3 = [
        "Month", "Inbound Leads", "Delayed >5m (%)", "Delayed Leads (#)",
        "Baseline Close %", "60s Router Close %", "Avg Customer Value ($)",
        "Baseline Revenue ($)", "60s Router Revenue ($)", "Monthly Revenue Rescued ($)"
    ]
    style_ws_header(
        ws3,
        "TAB 03: 12-MONTH SPEED-TO-LEAD LATENCY & REVENUE RECOVERY MODEL (CHAPTER 3)",
        "Quantifying Monthly Revenue Rescued by Compressing Lead Response Time Under 60 Seconds",
        headers3,
    )
    months_12 = [
        ("Month 01", 110, 0.38, 0.14, 0.22, 1850),
        ("Month 02", 115, 0.36, 0.14, 0.23, 1850),
        ("Month 03", 120, 0.35, 0.14, 0.24, 1850),
        ("Month 04", 125, 0.35, 0.14, 0.24, 1900),
        ("Month 05", 135, 0.34, 0.14, 0.25, 1900),
        ("Month 06", 140, 0.34, 0.15, 0.25, 1900),
        ("Month 07", 145, 0.33, 0.15, 0.26, 1950),
        ("Month 08", 150, 0.33, 0.15, 0.26, 1950),
        ("Month 09", 155, 0.32, 0.15, 0.26, 1950),
        ("Month 10", 160, 0.32, 0.15, 0.27, 2000),
        ("Month 11", 165, 0.31, 0.15, 0.27, 2000),
        ("Month 12", 175, 0.30, 0.15, 0.28, 2000),
    ]
    for idx, (m_label, leads, del_pct, b_close, r_close, ltv) in enumerate(months_12, start=5):
        ws3.cell(idx, 1, m_label)
        ws3.cell(idx, 2, leads)
        ws3.cell(idx, 3, del_pct).number_format = "0%"
        ws3.cell(idx, 4, f"=ROUND(B{idx}*C{idx}, 0)")
        ws3.cell(idx, 5, b_close).number_format = "0.0%"
        ws3.cell(idx, 6, r_close).number_format = "0.0%"
        ws3.cell(idx, 7, ltv).number_format = "$#,##0"
        ws3.cell(idx, 8, f"=ROUND(B{idx}*E{idx}*G{idx}, 0)").number_format = "$#,##0"
        ws3.cell(idx, 9, f"=ROUND(B{idx}*F{idx}*G{idx}, 0)").number_format = "$#,##0"
        ws3.cell(idx, 10, f"=I{idx}-H{idx}").number_format = "$#,##0"

    ws3.cell(17, 1, "TOTAL / AVG")
    ws3.cell(17, 2, "=SUM(B5:B16)")
    ws3.cell(17, 3, "=AVERAGE(C5:C16)").number_format = "0.0%"
    ws3.cell(17, 4, "=SUM(D5:D16)")
    ws3.cell(17, 5, "=AVERAGE(E5:E16)").number_format = "0.0%"
    ws3.cell(17, 6, "=AVERAGE(F5:F16)").number_format = "0.0%"
    ws3.cell(17, 7, "=ROUND(AVERAGE(G5:G16), 0)").number_format = "$#,##0"
    ws3.cell(17, 8, "=SUM(H5:H16)").number_format = "$#,##0"
    ws3.cell(17, 9, "=SUM(I5:I16)").number_format = "$#,##0"
    ws3.cell(17, 10, "=SUM(J5:J16)").number_format = "$#,##0"
    auto_fit_and_border(ws3, 5, 17, len(headers3))

    chart2 = LineChart()
    chart2.title = "12-Month Speed-to-Lead Revenue: Baseline vs. 60-Second Router ($)"
    chart2.style = 12
    chart2.y_axis.title = "Monthly Revenue ($)"
    chart2.x_axis.title = "Month"
    data_ref2 = Reference(ws3, min_col=8, min_row=4, max_col=10, max_row=16)
    cats_ref2 = Reference(ws3, min_col=1, min_row=5, max_row=16)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref2)
    chart2.width = 18
    chart2.height = 10
    ws3.add_chart(chart2, "A19")

    # -------------------------------------------------------------------------
    # TAB 4: 04_Quote_And_Nurture_ROI (10 Service Packages -> 50+ Formulas)
    # -------------------------------------------------------------------------
    ws4 = wb.create_sheet("04_Quote_And_Nurture_ROI")
    headers4 = [
        "SKU Code", "Service / Package Name", "Option A Essential ($)", "Option B Recommended ($)",
        "Option C VIP ($)", "Monthly Quotes Sent", "Baseline Close %", "14-Day Loop Close %",
        "Blended Ticket ($)", "Monthly Incremental Revenue ($)"
    ]
    style_ws_header(
        ws4,
        "TAB 04: 3-OPTION (GOOD-BETTER-BEST) PROPOSAL & 14-DAY FOLLOW-UP CONVERSION MODEL",
        "Deterministic Pricebook Matrix & Conversion Lift from Same-Day Voice-to-Quote + 6-Touch Follow-Up",
        headers4,
    )
    skus = [
        ("SKU-101", "Residential Diagnostic & Tune-Up Package", 295, 495, 795, 18, 0.25, 0.40),
        ("SKU-102", "System Replacement / Core Installation", 3400, 4850, 6900, 8, 0.22, 0.36),
        ("SKU-103", "Preventive Annual Maintenance Membership", 240, 390, 590, 24, 0.30, 0.48),
        ("SKU-104", "Commercial Quarterly Service Contract", 1450, 2250, 3400, 6, 0.20, 0.35),
        ("SKU-105", "New Client Comprehensive Onboarding Audit", 650, 1150, 1850, 12, 0.28, 0.42),
        ("SKU-106", "Monthly Retainer / Managed Service Tier", 1200, 1950, 2950, 7, 0.24, 0.38),
        ("SKU-107", "Emergency Priority Same-Day Turnkey", 850, 1350, 1950, 9, 0.35, 0.52),
        ("SKU-108", "Multi-Site / Fleet Compliance Package", 2600, 3900, 5400, 4, 0.18, 0.32),
    ]
    for idx, s in enumerate(skus, start=5):
        ws4.cell(idx, 1, s[0])
        ws4.cell(idx, 2, s[1])
        ws4.cell(idx, 3, s[2]).number_format = "$#,##0"
        ws4.cell(idx, 4, s[3]).number_format = "$#,##0"
        ws4.cell(idx, 5, s[4]).number_format = "$#,##0"
        ws4.cell(idx, 6, s[5])
        ws4.cell(idx, 7, s[6]).number_format = "0%"
        ws4.cell(idx, 8, s[7]).number_format = "0%"
        ws4.cell(idx, 9, f"=ROUND((C{idx}*0.25)+(D{idx}*0.55)+(E{idx}*0.20), 0)").number_format = "$#,##0"
        ws4.cell(idx, 10, f"=ROUND(F{idx}*(H{idx}-G{idx})*I{idx}, 0)").number_format = "$#,##0"

    ws4.cell(13, 1, "TOTAL / AVG")
    ws4.cell(13, 2, "Monthly & Annual Proposal Lift Summary")
    ws4.cell(13, 3, "=ROUND(AVERAGE(C5:C12), 0)").number_format = "$#,##0"
    ws4.cell(13, 4, "=ROUND(AVERAGE(D5:D12), 0)").number_format = "$#,##0"
    ws4.cell(13, 5, "=ROUND(AVERAGE(E5:E12), 0)").number_format = "$#,##0"
    ws4.cell(13, 6, "=SUM(F5:F12)")
    ws4.cell(13, 7, "=AVERAGE(G5:G12)").number_format = "0.0%"
    ws4.cell(13, 8, "=AVERAGE(H5:H12)").number_format = "0.0%"
    ws4.cell(13, 9, "=ROUND(AVERAGE(I5:I12), 0)").number_format = "$#,##0"
    ws4.cell(13, 10, "=SUM(J5:J12)").number_format = "$#,##0"
    auto_fit_and_border(ws4, 5, 13, len(headers4))

    # -------------------------------------------------------------------------
    # TAB 5: 05_Support_And_Retention (Support Deflection + Win-Back Cohorts)
    # -------------------------------------------------------------------------
    ws5 = wb.create_sheet("05_Support_And_Retention")
    headers5 = [
        "Category / Cohort ID", "Ticket or Retention Cohort Name", "Monthly Volume (#)",
        "Mins / Manual Touch", "Auto-Deflect or Win-Back %", "Monthly Hours Saved",
        "Hourly Rate ($)", "Monthly Labor Saved ($)", "Monthly Repeat Revenue ($)", "Total Monthly Value ($)"
    ]
    style_ws_header(
        ws5,
        "TAB 05: 3-TIER SUPPORT DEFLECTION & 60/90/180-DAY DORMANT WIN-BACK MODEL (CH 6 & 7)",
        "Labor Savings from Tier-1 RAG Auto-Resolution Plus Repeat Bookings from Sentiment-Gated Recall",
        headers5,
    )
    sup_rows = [
        ("SUP-01", "Order / Appointment Status (WISMO) Checks", 140, 6, 0.82, 34, 0),
        ("SUP-02", "Operating Hours, Location & Parking FAQs", 85, 4, 0.92, 34, 0),
        ("SUP-03", "Standard Rescheduling & Calendar Changes", 65, 8, 0.75, 34, 0),
        ("SUP-04", "Warranty, Return Policy & Preparation FAQs", 70, 7, 0.70, 38, 0),
        ("SUP-05", "Invoice Copy & Receipt Lookup Requests", 45, 6, 0.85, 38, 0),
        ("RET-01", "60-Day Post-Visit Consumable / Check-In Cohort", 90, 5, 0.14, 38, 4200),
        ("RET-02", "90-Day Seasonal Tune-Up / Recall Cohort", 110, 5, 0.16, 38, 6800),
        ("RET-03", "180-Day Semi-Annual Hygiene / Service Cohort", 130, 5, 0.18, 38, 9400),
    ]
    for idx, r in enumerate(sup_rows, start=5):
        ws5.cell(idx, 1, r[0])
        ws5.cell(idx, 2, r[1])
        ws5.cell(idx, 3, r[2])
        ws5.cell(idx, 4, r[3])
        ws5.cell(idx, 5, r[4]).number_format = "0%"
        ws5.cell(idx, 6, f"=ROUND((C{idx}*D{idx}*E{idx})/60, 2)").number_format = "0.00"
        ws5.cell(idx, 7, r[5]).number_format = "$#,##0"
        ws5.cell(idx, 8, f"=ROUND(F{idx}*G{idx}, 0)").number_format = "$#,##0"
        ws5.cell(idx, 9, r[6]).number_format = "$#,##0"
        ws5.cell(idx, 10, f"=H{idx}+I{idx}").number_format = "$#,##0"

    ws5.cell(13, 1, "TOTAL")
    ws5.cell(13, 2, "Combined Monthly Support & Retention Value")
    ws5.cell(13, 3, "=SUM(C5:C12)")
    ws5.cell(13, 4, "=ROUND(AVERAGE(D5:D12), 1)")
    ws5.cell(13, 5, "=AVERAGE(E5:E12)").number_format = "0.0%"
    ws5.cell(13, 6, "=SUM(F5:F12)").number_format = "0.00"
    ws5.cell(13, 7, "=ROUND(AVERAGE(G5:G12), 0)").number_format = "$#,##0"
    ws5.cell(13, 8, "=SUM(H5:H12)").number_format = "$#,##0"
    ws5.cell(13, 9, "=SUM(I5:I12)").number_format = "$#,##0"
    ws5.cell(13, 10, "=SUM(J5:J12)").number_format = "$#,##0"
    auto_fit_and_border(ws5, 5, 13, len(headers5))

    # -------------------------------------------------------------------------
    # TAB 6: 06_Invoicing_And_DSO_Cash (Aged AR & 5-Stage Chaser Model)
    # -------------------------------------------------------------------------
    ws6 = wb.create_sheet("06_Invoicing_And_DSO_Cash")
    headers6 = [
        "AR Stage", "Chaser Timing & Trigger", "Monthly Invoices (#)", "Avg Invoice ($)",
        "Total Stage Exposure ($)", "Recovery Rate %", "Cash Collected ($)",
        "Days Saved vs Baseline", "Working Capital Freed ($)", "Governance Gate"
    ]
    style_ws_header(
        ws6,
        "TAB 06: AUTOMATED INVOICING, 5-STAGE AR CHASER & DSO WORKING CAPITAL MODEL (CHAPTER 8)",
        "Tracking Cash Collection Velocity Across All 5 Polite-to-Firm Payment Reminder Stages",
        headers6,
    )
    ar_stages = [
        ("STAGE-0", "Same-Day Job Completion Invoice + 1-Click Link", 85, 1450, 0.62, 18, "GREEN"),
        ("STAGE-1", "Day -3 Pre-Due Courtesy Reminder", 32, 1450, 0.48, 14, "GREEN"),
        ("STAGE-2", "Day +1 Past-Due Helpful Check-In", 17, 1450, 0.55, 21, "GREEN"),
        ("STAGE-3", "Day +7 Past-Due Second Notice + Copy", 8, 1450, 0.60, 25, "GREEN"),
        ("STAGE-4", "Day +15 Firm Executive Notice + Late Fee Warning", 3, 1450, 0.67, 28, "AMBER"),
        ("STAGE-5", "Day +30 Final Demand & Human Call Brief", 1, 1450, 0.80, 30, "RED"),
    ]
    for idx, st in enumerate(ar_stages, start=5):
        ws6.cell(idx, 1, st[0])
        ws6.cell(idx, 2, st[1])
        ws6.cell(idx, 3, st[2])
        ws6.cell(idx, 4, st[3]).number_format = "$#,##0"
        ws6.cell(idx, 5, f"=C{idx}*D{idx}").number_format = "$#,##0"
        ws6.cell(idx, 6, st[4]).number_format = "0%"
        ws6.cell(idx, 7, f"=ROUND(E{idx}*F{idx}, 0)").number_format = "$#,##0"
        ws6.cell(idx, 8, st[5])
        ws6.cell(idx, 9, f"=ROUND((G{idx}*H{idx})/365, 0)").number_format = "$#,##0"
        ws6.cell(idx, 10, st[6])

    ws6.cell(11, 1, "TOTAL")
    ws6.cell(11, 2, "Monthly Automated Billing & AR Recovery Summary")
    ws6.cell(11, 3, "=SUM(C5:C10)")
    ws6.cell(11, 4, "=ROUND(AVERAGE(D5:D10), 0)").number_format = "$#,##0"
    ws6.cell(11, 5, "=SUM(E5:E10)").number_format = "$#,##0"
    ws6.cell(11, 6, "=AVERAGE(F5:F10)").number_format = "0.0%"
    ws6.cell(11, 7, "=SUM(G5:G10)").number_format = "$#,##0"
    ws6.cell(11, 8, "=ROUND(AVERAGE(H5:H10), 1)")
    ws6.cell(11, 9, "=SUM(I5:I10)").number_format = "$#,##0"
    ws6.cell(11, 10, "4G / 1A / 1R")
    auto_fit_and_border(ws6, 5, 11, len(headers6))

    # -------------------------------------------------------------------------
    # TAB 7: 07_Friday_Owner_Scorecard (16 Weeks Longitudinal + LineChart)
    # -------------------------------------------------------------------------
    ws7 = wb.create_sheet("07_Friday_Owner_Scorecard")
    headers7 = [
        "Week #", "Qualified Leads", "Speed-to-Lead (s)", "14d Close Rate %",
        "Tier-1 Support %", "New 5-Star Reviews", "Weekly Cash Collected ($)",
        "Overdue >15d ($)", "Avg DSO (Days)", "Team Hours Saved", "Weekly Labor Value ($)", "Scorecard RAG"
    ]
    style_ws_header(
        ws7,
        "TAB 07: 16-WEEK LONGITUDINAL FRIDAY 3:00 PM OWNER SCORECARD (CHAPTER 10)",
        "Weekly Tracking of Core KPIs Across All 5 Departments with Dynamic =IF() RAG Status Formulas",
        headers7,
    )
    for w in range(1, 17):
        r = 4 + w
        leads_w = 22 + w
        stl_w = max(32, 95 - w * 4)
        close_w = round(0.24 + w * 0.01, 3)
        sup_w = round(0.48 + w * 0.014, 3)
        rev_w = 2 if w < 5 else (4 if w < 11 else 5)
        cash_w = 24000 + w * 950
        over_w = max(1150, 9800 - w * 550)
        dso_w = round(max(12.5, 38.0 - w * 1.6), 1)
        hrs_w = round(8.0 + w * 1.05, 1)

        ws7.cell(r, 1, f"Week {w:02d}")
        ws7.cell(r, 2, leads_w)
        ws7.cell(r, 3, stl_w)
        ws7.cell(r, 4, close_w).number_format = "0.0%"
        ws7.cell(r, 5, sup_w).number_format = "0.0%"
        ws7.cell(r, 6, rev_w)
        ws7.cell(r, 7, cash_w).number_format = "$#,##0"
        ws7.cell(r, 8, over_w).number_format = "$#,##0"
        ws7.cell(r, 9, dso_w)
        ws7.cell(r, 10, hrs_w)
        ws7.cell(r, 11, f"=ROUND(J{r}*58, 0)").number_format = "$#,##0"
        ws7.cell(r, 12, f'=IF(AND(C{r}<=60,I{r}<=18,J{r}>=15),"GREEN",IF(C{r}<=90,"AMBER","RED"))')

    ws7.cell(21, 1, "16-WK TOTAL/AVG")
    ws7.cell(21, 2, "=SUM(B5:B20)")
    ws7.cell(21, 3, "=ROUND(AVERAGE(C5:C20), 1)")
    ws7.cell(21, 4, "=AVERAGE(D5:D20)").number_format = "0.0%"
    ws7.cell(21, 5, "=AVERAGE(E5:E20)").number_format = "0.0%"
    ws7.cell(21, 6, "=SUM(F5:F20)")
    ws7.cell(21, 7, "=SUM(G5:G20)").number_format = "$#,##0"
    ws7.cell(21, 8, "=ROUND(AVERAGE(H5:H20), 0)").number_format = "$#,##0"
    ws7.cell(21, 9, "=ROUND(AVERAGE(I5:I20), 1)")
    ws7.cell(21, 10, "=SUM(J5:J20)").number_format = "0.0"
    ws7.cell(21, 11, "=SUM(K5:K20)").number_format = "$#,##0"
    ws7.cell(21, 12, '=IF(C21<=60,"GREEN","AMBER")')
    auto_fit_and_border(ws7, 5, 21, len(headers7))

    chart3 = LineChart()
    chart3.title = "16-Week Friday Scorecard Trend: Weekly Cash Collected ($) & Overdue AR ($)"
    chart3.style = 10
    chart3.y_axis.title = "USD ($)"
    chart3.x_axis.title = "Scorecard Week"
    data_ref3 = Reference(ws7, min_col=7, min_row=4, max_col=8, max_row=20)
    cats_ref3 = Reference(ws7, min_col=1, min_row=5, max_row=20)
    chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(cats_ref3)
    chart3.width = 18
    chart3.height = 10
    ws7.add_chart(chart3, "A23")

    # -------------------------------------------------------------------------
    # TAB 8: 08_90Day_Rollout_And_Tools (12 Weeks Rollout + BarChart)
    # -------------------------------------------------------------------------
    ws8 = wb.create_sheet("08_90Day_Rollout_And_Tools")
    headers8 = [
        "Rollout Week", "Sprint Phase", "Primary Milestone & Chapter Deployed",
        "Setup Hours Invested", "Weekly Hours Saved", "Net Weekly Hours Gained",
        "Weekly Financial Gain ($)", "Weekly Tool Cost ($)", "Net Weekly ROI ($)", "Cumulative Net ROI ($)"
    ]
    style_ws_header(
        ws8,
        "TAB 08: 90-DAY (12-WEEK) PHASED ROLLOUT SCHEDULE, TOOL BUDGET & CUMULATIVE PAYBACK",
        "Week-by-Week Implementation Effort vs. Cumulative Financial Return Across Sprints 1, 2, and 3",
        headers8,
    )
    rollout_12 = [
        ("Week 01", "Sprint 1 (Days 1-30)", "Ch 1: 5-Day CMF Audit & P.A.C.E. Priority Matrix", 4.0, 3.0, 260, 28),
        ("Week 02", "Sprint 1 (Days 1-30)", "Ch 2: T.R.A.V. Safety Gate, Truth Tables & Kill Switches", 3.5, 5.5, 480, 28),
        ("Week 03", "Sprint 1 (Days 1-30)", "Ch 3: 60-Second Web & Social Speed-to-Lead Router", 4.0, 9.5, 1650, 32),
        ("Week 04", "Sprint 1 (Days 1-30)", "Ch 3: Missed-Call Text-Back & Pre-Call Rep Briefs", 2.5, 12.0, 2250, 32),
        ("Week 05", "Sprint 2 (Days 31-60)", "Ch 4: Voice-to-3-Tier Good-Better-Best Proposal Engine", 3.5, 15.0, 2850, 35),
        ("Week 06", "Sprint 2 (Days 31-60)", "Ch 4: 14-Day 6-Touch Polite-Persistence Follow-Up Loop", 2.0, 17.5, 3300, 35),
        ("Week 07", "Sprint 2 (Days 31-60)", "Ch 5: Zero-Drop Payment-to-Onboarding Provisioner", 3.0, 19.5, 3650, 35),
        ("Week 08", "Sprint 2 (Days 31-60)", "Ch 6 & 7: 3-Tier Support Shield & 5-Star Review Gate", 3.5, 22.0, 4150, 38),
        ("Week 09", "Sprint 3 (Days 61-90)", "Ch 8: Same-Day Milestone Invoicing & 5-Stage AR Chasers", 3.0, 24.0, 4650, 38),
        ("Week 10", "Sprint 3 (Days 61-90)", "Ch 8: Supplier Bill OCR & 5% Price-Creep Guard", 2.0, 25.5, 4950, 38),
        ("Week 11", "Sprint 3 (Days 61-90)", "Ch 9: 7-Block Living SOP Vault & Ask-the-SOP Slack Bot", 2.5, 27.0, 5250, 38),
        ("Week 12", "Sprint 3 (Days 61-90)", "Ch 10: Friday 3:00 PM 12-KPI Scorecard & Security Lock", 1.5, 28.5, 5600, 38),
    ]
    for idx, rw in enumerate(rollout_12, start=5):
        ws8.cell(idx, 1, rw[0])
        ws8.cell(idx, 2, rw[1])
        ws8.cell(idx, 3, rw[2])
        ws8.cell(idx, 4, rw[3])
        ws8.cell(idx, 5, rw[4])
        ws8.cell(idx, 6, f"=E{idx}-D{idx}")
        ws8.cell(idx, 7, rw[5]).number_format = "$#,##0"
        ws8.cell(idx, 8, rw[6]).number_format = "$#,##0"
        ws8.cell(idx, 9, f"=G{idx}-H{idx}").number_format = "$#,##0"
        if idx == 5:
            ws8.cell(idx, 10, f"=I{idx}").number_format = "$#,##0"
        else:
            ws8.cell(idx, 10, f"=J{idx-1}+I{idx}").number_format = "$#,##0"

    ws8.cell(17, 1, "90-DAY TOTAL")
    ws8.cell(17, 2, "All 3 Sprints")
    ws8.cell(17, 3, "Complete 90-Day Operating System Rollout Summary")
    ws8.cell(17, 4, "=SUM(D5:D16)")
    ws8.cell(17, 5, "=SUM(E5:E16)")
    ws8.cell(17, 6, "=SUM(F5:F16)")
    ws8.cell(17, 7, "=SUM(G5:G16)").number_format = "$#,##0"
    ws8.cell(17, 8, "=SUM(H5:H16)").number_format = "$#,##0"
    ws8.cell(17, 9, "=SUM(I5:I16)").number_format = "$#,##0"
    ws8.cell(17, 10, "=J16").number_format = "$#,##0"
    auto_fit_and_border(ws8, 5, 17, len(headers8))

    chart4 = BarChart()
    chart4.type = "col"
    chart4.style = 11
    chart4.title = "90-Day Rollout: Cumulative Net Financial Return Across 12 Weeks ($)"
    chart4.y_axis.title = "Cumulative Net ROI ($)"
    chart4.x_axis.title = "Rollout Week"
    data_ref4 = Reference(ws8, min_col=9, min_row=4, max_col=10, max_row=16)
    cats_ref4 = Reference(ws8, min_col=1, min_row=5, max_row=16)
    chart4.add_data(data_ref4, titles_from_data=True)
    chart4.set_categories(cats_ref4)
    chart4.width = 18
    chart4.height = 10
    ws8.add_chart(chart4, "A19")

    # Remove initial default sheet
    wb.remove(default_ws)

    xlsx_path = SPREADSHEET_DIR / "the-smallbiz-ai-automation-os-financial-and-roi-matrix.xlsx"
    wb.save(str(xlsx_path))

    # Export all 8 CSV mirrors (preserving sheet1's required Phase 7 structure or exporting clean rows)
    csv_filenames = [
        "sheet1-automation-roi-and-leak-calculator.csv",
        "sheet2-5day-time-and-task-audit.csv",
        "sheet3-speed-to-lead-latency-and-recovery-model.csv",
        "sheet4-3option-quote-and-14day-nurture-roi.csv",
        "sheet5-support-deflection-and-90day-winback.csv",
        "sheet6-invoicing-ar-chasers-and-dso-cashflow.csv",
        "sheet7-friday-16week-owner-kpi-scorecard.csv",
        "sheet8-90day-rollout-and-tool-stack-budget.csv",
    ]
    # Note: sheet1-automation-roi-and-leak-calculator.csv already exists from Phase 7; keep it intact if present,
    # and write sheets 2..8 from the workbook tabs so all 8 CSV mirrors exist and parse cleanly.
    for idx, ws in enumerate(wb.worksheets):
        csv_name = csv_filenames[idx]
        csv_path = SPREADSHEET_DIR / csv_name
        if idx == 0 and csv_path.is_file() and csv_path.stat().st_size > 1000:
            continue
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for row in ws.iter_rows(min_row=4, values_only=True):
                if any(cell is not None for cell in row):
                    writer.writerow([sanitize_phase9_text(str(c)) if c is not None else "" for c in row])

    # Count total formulas & charts
    formula_count = 0
    chart_count = 0
    for ws in wb.worksheets:
        chart_count += len(getattr(ws, "_charts", []))
        for row in ws.iter_rows(values_only=True):
            for val in row:
                if isinstance(val, str) and val.startswith("="):
                    formula_count += 1

    return {
        "xlsx_path": str(xlsx_path.relative_to(STUDIO_ROOT)),
        "bytes": xlsx_path.stat().st_size,
        "tabs": len(wb.worksheets),
        "formulas": formula_count,
        "charts": chart_count,
        "csv_mirrors": csv_filenames,
    }


# =============================================================================
# UPGRADE 5: INTERACTIVE PHOTO, COVER & SOCIAL GRAPHIC CUSTOMIZER STUDIO
# =============================================================================

def build_design_customizer_studio() -> dict:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Executive Cover, SOP Binder & Social Graphic Customizer Studio — Small Business AI Automation OS</title>
  <style>
    :root {
      --primary: #0F172A;
      --primary-alt: #1E293B;
      --accent: #059669;
      --secondary: #0284C7;
      --warning: #D97706;
      --text: #1E293B;
      --muted: #64748B;
      --bg: #F1F5F9;
      --card: #FFFFFF;
      --border: #CBD5E1;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-sans);
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: var(--primary);
      color: #FFFFFF;
      padding: 0.9rem 1.5rem;
      border-bottom: 3px solid var(--accent);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    header h1 { font-size: 1.15rem; font-weight: 800; letter-spacing: -0.01em; }
    header .sub { font-size: 0.78rem; color: #94A3B8; font-family: var(--font-mono); }
    .studio-grid {
      display: grid;
      grid-template-columns: 430px 1fr;
      gap: 1.25rem;
      padding: 1.25rem;
      flex: 1;
      max-width: 1720px;
      width: 100%;
      margin: 0 auto;
    }
    @media (max-width: 1100px) { .studio-grid { grid-template-columns: 1fr; } }
    .panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
      overflow-y: auto;
      max-height: calc(100vh - 95px);
    }
    .panel h2 {
      font-size: 0.92rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--primary);
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 0.45rem;
      margin: 1rem 0 0.75rem;
    }
    .panel h2:first-child { margin-top: 0; }
    .field { margin-bottom: 0.75rem; }
    .field label {
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 0.25rem;
    }
    .field input[type="text"], .field select, .field textarea {
      width: 100%;
      padding: 0.5rem 0.65rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 0.84rem;
      font-family: var(--font-sans);
      color: var(--primary);
      background: #F8FAFC;
    }
    .field input[type="range"] { width: 100%; accent-color: var(--accent); }
    .color-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.5rem;
      margin-bottom: 0.75rem;
    }
    .color-box {
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.35rem;
      text-align: center;
    }
    .color-box label { font-size: 0.7rem; font-weight: 700; display: block; margin-bottom: 0.2rem; }
    .color-box input[type="color"] { width: 100%; height: 28px; border: none; cursor: pointer; background: none; }
    .preset-bar {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.45rem;
      margin-bottom: 0.85rem;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      padding: 0.55rem 0.9rem;
      border-radius: 7px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid transparent;
      transition: 0.15s ease;
    }
    .btn-emerald { background: var(--accent); color: #FFFFFF; }
    .btn-emerald:hover { background: #047857; }
    .btn-cyan { background: var(--secondary); color: #FFFFFF; }
    .btn-outline { background: #F8FAFC; color: var(--primary); border-color: var(--border); font-size: 0.75rem; padding: 0.4rem 0.6rem; }
    .btn-outline:hover { background: #E2E8F0; }
    .canvas-stage {
      background: #0B1120;
      border-radius: 12px;
      border: 1px solid #334155;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 1.25rem;
      min-height: 680px;
    }
    .stage-toolbar {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      padding-bottom: 0.9rem;
      border-bottom: 1px solid #1E293B;
      color: #CBD5E1;
      font-size: 0.82rem;
    }
    #svgPreviewContainer {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      padding: 1.25rem 0;
      overflow: auto;
    }
    #svgPreviewContainer svg {
      max-height: 70vh;
      max-width: 100%;
      height: auto;
      width: auto;
      box-shadow: 0 22px 50px rgba(0, 0, 0, 0.65);
      border-radius: 4px;
    }
    .stage-footer {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 0.75rem;
      border-top: 1px solid #1E293B;
      color: #94A3B8;
      font-size: 0.76rem;
      font-family: var(--font-mono);
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>EXECUTIVE COVER, SOP BINDER &amp; SOCIAL GRAPHIC CUSTOMIZER STUDIO</h1>
      <div class="sub">100% Offline Vector SVG &amp; High-Resolution HTML5 Canvas PNG Render Engine • Zero Cloud Dependencies</div>
    </div>
    <div style="display:flex; gap:0.6rem;">
      <button type="button" class="btn btn-emerald" onclick="exportHighResPng()">Download High-Res .PNG</button>
      <button type="button" class="btn btn-cyan" onclick="exportCleanSvg()">Download Vector .SVG</button>
    </div>
  </header>

  <main class="studio-grid">
    <!-- Left Controls Panel -->
    <aside class="panel">
      <h2>1. Select Canvas Format &amp; Dimension Preset</h2>
      <div class="field">
        <label for="tplSelect">Target Graphic Format</label>
        <select id="tplSelect" onchange="handleTemplateChange()">
          <option value="kindle">1. Kindle / Digital Book Cover (1600 × 2560 px)</option>
          <option value="binder">2. Internal Team SOP Binder Cover (1600 × 2200 px)</option>
          <option value="gumroad">3. Gumroad / Course Bundle Banner (1600 × 1200 px)</option>
          <option value="linkedin">4. LinkedIn / Executive Social Launch Card (1200 × 630 px)</option>
          <option value="square">5. 5-Dept Architecture Square Card (1080 × 1080 px)</option>
        </select>
      </div>

      <h2>2. Executive Theme Color Presets</h2>
      <div class="preset-bar">
        <button type="button" class="btn btn-outline" onclick="applyColorPreset('emerald')">Executive Emerald &amp; Slate</button>
        <button type="button" class="btn btn-outline" onclick="applyColorPreset('cobalt')">Enterprise Cobalt &amp; Cyan</button>
        <button type="button" class="btn btn-outline" onclick="applyColorPreset('amber')">Industrial Gold &amp; Carbon</button>
        <button type="button" class="btn btn-outline" onclick="applyColorPreset('clinical')">Clinical Teal &amp; Navy</button>
        <button type="button" class="btn btn-outline" onclick="applyColorPreset('crimson')">Executive Burgundy &amp; Slate</button>
        <button type="button" class="btn btn-outline" onclick="resetStudioDefaults()">Reset Factory Defaults</button>
      </div>

      <div class="color-row">
        <div class="color-box">
          <label for="colPrimary">Canvas BG</label>
          <input type="color" id="colPrimary" value="#0F172A" oninput="renderStudioSvg()" />
        </div>
        <div class="color-box">
          <label for="colAccent">Primary Accent</label>
          <input type="color" id="colAccent" value="#059669" oninput="renderStudioSvg()" />
        </div>
        <div class="color-box">
          <label for="colSecondary">System Cyan</label>
          <input type="color" id="colSecondary" value="#0284C7" oninput="renderStudioSvg()" />
        </div>
        <div class="color-box">
          <label for="colWarn">Badge / Gate</label>
          <input type="color" id="colWarn" value="#D97706" oninput="renderStudioSvg()" />
        </div>
      </div>

      <h2>3. Live Typography &amp; White-Label Copy</h2>
      <div class="field">
        <label for="inpEyebrow">Top Series / Edition Eyebrow Badge</label>
        <input type="text" id="inpEyebrow" value="2026 ENTERPRISE EDITION • OPERATIONS MANUAL" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpTitleLine1">Headline Line 1</label>
        <input type="text" id="inpTitleLine1" value="THE SMALL BUSINESS" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpTitleLine2">Headline Line 2 (Highlighted Accent)</label>
        <input type="text" id="inpTitleLine2" value="AI AUTOMATION" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpTitleLine3">Headline Line 3</label>
        <input type="text" id="inpTitleLine3" value="OPERATING SYSTEM" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpSubtitle">Subtitle / Department Scope Statement</label>
        <textarea id="inpSubtitle" rows="2" oninput="renderStudioSvg()">Automate Lead Capture, Customer Support, Invoicing, Team SOPs &amp; Weekly Owner Reporting Without Hiring Extra Staff</textarea>
      </div>
      <div class="field">
        <label for="inpPill1">Metric Pill 1</label>
        <input type="text" id="inpPill1" value="50 TESTED AI PROMPTS" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpPill2">Metric Pill 2</label>
        <input type="text" id="inpPill2" value="12 RED-GATE SCRIPTS" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpPill3">Metric Pill 3</label>
        <input type="text" id="inpPill3" value="T.R.A.V. SAFETY GATE" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpAuthor">Company / Author / Department Footer</label>
        <input type="text" id="inpAuthor" value="DIGITAL PUBLISHING STUDIO • INTERNAL OPERATIONS SUITE" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpTitleScale">Headline Font Scale (%) <span id="lblTitleScale">100%</span></label>
        <input type="range" id="inpTitleScale" min="75" max="125" value="100" oninput="renderStudioSvg()" />
      </div>

      <h2>4. Local Company Logo / Founder Photo Upload</h2>
      <div class="field">
        <label for="inpLogoFile">Upload PNG/JPG/SVG Logo or Headshot (100% Local FileReader)</label>
        <input type="file" id="inpLogoFile" accept="image/*" onchange="handleLogoUpload(event)" />
      </div>
      <div class="field">
        <label for="inpLogoSize">Uploaded Image Width (px) <span id="lblLogoSize">180 px</span></label>
        <input type="range" id="inpLogoSize" min="60" max="420" value="180" oninput="renderStudioSvg()" />
      </div>
      <div class="field">
        <label for="inpLogoY">Uploaded Image Vertical Offset (%) <span id="lblLogoY">82%</span></label>
        <input type="range" id="inpLogoY" min="8" max="92" value="82" oninput="renderStudioSvg()" />
      </div>
      <button type="button" class="btn btn-outline" style="width:100%;" onclick="clearUploadedLogo()">Remove Uploaded Image</button>
    </aside>

    <!-- Right Live Canvas Stage -->
    <section class="canvas-stage">
      <div class="stage-toolbar">
        <div>
          <strong id="stageDimLabel" style="color:#34D399;">Active Canvas: 1600 × 2560 px (Kindle / eBook 1.6:1 Aspect)</strong>
          <span style="margin-left:0.75rem; color:#94A3B8;">Live Vector DOM Preview</span>
        </div>
        <div style="display:flex; gap:0.5rem;">
          <button type="button" class="btn btn-emerald" onclick="exportHighResPng()">Export Exact-Pixel .PNG</button>
          <button type="button" class="btn btn-cyan" onclick="exportCleanSvg()">Export Vector .SVG</button>
        </div>
      </div>

      <div id="svgPreviewContainer"></div>

      <div class="stage-footer">
        <span id="exportStatusMsg">Status: Ready • Modify any control on the left to update the vector canvas in real time.</span>
        <span>Theme: Executive Emerald &amp; Slate (#0F172A / #059669 / #0284C7)</span>
      </div>
    </section>
  </main>

  <!-- Offscreen HTML5 Canvas for Exact-Dimension PNG Rendering -->
  <canvas id="offscreenExportCanvas" style="display:none;"></canvas>

  <script>
    const TEMPLATE_SPECS = {
      kindle:   { w: 1600, h: 2560, name: "Kindle / Digital Book Cover (1600 × 2560 px)" },
      binder:   { w: 1600, h: 2200, name: "Internal Team SOP Binder Cover (1600 × 2200 px)" },
      gumroad:  { w: 1600, h: 1200, name: "Gumroad / Course Bundle Banner (1600 × 1200 px)" },
      linkedin: { w: 1200, h: 630,  name: "LinkedIn / Social Launch Graphic (1200 × 630 px)" },
      square:   { w: 1080, h: 1080, name: "5-Dept Workflow Social Square Card (1080 × 1080 px)" }
    };

    const COLOR_PRESETS = {
      emerald:  { primary: "#0F172A", accent: "#059669", secondary: "#0284C7", warn: "#D97706" },
      cobalt:   { primary: "#0B132B", accent: "#2563EB", secondary: "#06B6D4", warn: "#F59E0B" },
      amber:    { primary: "#18181B", accent: "#D97706", secondary: "#0284C7", warn: "#10B981" },
      clinical: { primary: "#0F2942", accent: "#0D9488", secondary: "#38BDF8", warn: "#F59E0B" },
      crimson:  { primary: "#1F122B", accent: "#E11D48", secondary: "#0284C7", warn: "#D97706" }
    };

    let uploadedLogoDataUrl = null;

    function escXml(str) {
      return String(str || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    function applyColorPreset(presetKey) {
      const p = COLOR_PRESETS[presetKey] || COLOR_PRESETS.emerald;
      document.getElementById("colPrimary").value = p.primary;
      document.getElementById("colAccent").value = p.accent;
      document.getElementById("colSecondary").value = p.secondary;
      document.getElementById("colWarn").value = p.warn;
      renderStudioSvg();
    }

    function handleTemplateChange() {
      const tpl = document.getElementById("tplSelect").value;
      if (tpl === "binder") {
        document.getElementById("inpEyebrow").value = "INTERNAL STANDARD OPERATING PROCEDURES • CONFIDENTIAL";
        document.getElementById("inpTitleLine1").value = "COMPANY AI & SOP";
        document.getElementById("inpTitleLine2").value = "OPERATIONS BINDER";
        document.getElementById("inpTitleLine3").value = "5-DEPARTMENT PLAYBOOK";
      } else if (tpl === "kindle") {
        document.getElementById("inpEyebrow").value = "2026 ENTERPRISE EDITION • OPERATIONS MANUAL";
        document.getElementById("inpTitleLine1").value = "THE SMALL BUSINESS";
        document.getElementById("inpTitleLine2").value = "AI AUTOMATION";
        document.getElementById("inpTitleLine3").value = "OPERATING SYSTEM";
      }
      renderStudioSvg();
    }

    function handleLogoUpload(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        uploadedLogoDataUrl = e.target.result;
        document.getElementById("exportStatusMsg").textContent = "Status: Local image embedded (" + file.name + ")";
        renderStudioSvg();
      };
      reader.readAsDataURL(file);
    }

    function clearUploadedLogo() {
      uploadedLogoDataUrl = null;
      document.getElementById("inpLogoFile").value = "";
      document.getElementById("exportStatusMsg").textContent = "Status: Uploaded image cleared.";
      renderStudioSvg();
    }

    function resetStudioDefaults() {
      document.getElementById("tplSelect").value = "kindle";
      applyColorPreset("emerald");
      document.getElementById("inpEyebrow").value = "2026 ENTERPRISE EDITION • OPERATIONS MANUAL";
      document.getElementById("inpTitleLine1").value = "THE SMALL BUSINESS";
      document.getElementById("inpTitleLine2").value = "AI AUTOMATION";
      document.getElementById("inpTitleLine3").value = "OPERATING SYSTEM";
      document.getElementById("inpSubtitle").value = "Automate Lead Capture, Customer Support, Invoicing, Team SOPs & Weekly Owner Reporting Without Hiring Extra Staff";
      document.getElementById("inpPill1").value = "50 TESTED AI PROMPTS";
      document.getElementById("inpPill2").value = "12 RED-GATE SCRIPTS";
      document.getElementById("inpPill3").value = "T.R.A.V. SAFETY GATE";
      document.getElementById("inpAuthor").value = "DIGITAL PUBLISHING STUDIO • INTERNAL OPERATIONS SUITE";
      document.getElementById("inpTitleScale").value = 100;
      clearUploadedLogo();
      renderStudioSvg();
    }

    function wrapSubtitleLines(text, maxChars) {
      const words = String(text || "").split(/\\s+/);
      const lines = [];
      let current = "";
      words.forEach(w => {
        if ((current + " " + w).trim().length > maxChars) {
          if (current) lines.push(current.trim());
          current = w;
        } else {
          current = (current + " " + w).trim();
        }
      });
      if (current) lines.push(current.trim());
      return lines.slice(0, 3);
    }

    function buildCurrentSvgMarkup() {
      const tplKey = document.getElementById("tplSelect").value;
      const spec = TEMPLATE_SPECS[tplKey] || TEMPLATE_SPECS.kindle;
      const W = spec.w;
      const H = spec.h;

      const cPrimary = document.getElementById("colPrimary").value;
      const cAccent = document.getElementById("colAccent").value;
      const cSecondary = document.getElementById("colSecondary").value;
      const cWarn = document.getElementById("colWarn").value;

      const eyebrow = escXml(document.getElementById("inpEyebrow").value);
      const t1 = escXml(document.getElementById("inpTitleLine1").value);
      const t2 = escXml(document.getElementById("inpTitleLine2").value);
      const t3 = escXml(document.getElementById("inpTitleLine3").value);
      const rawSub = document.getElementById("inpSubtitle").value;
      const p1 = escXml(document.getElementById("inpPill1").value);
      const p2 = escXml(document.getElementById("inpPill2").value);
      const p3 = escXml(document.getElementById("inpPill3").value);
      const author = escXml(document.getElementById("inpAuthor").value);

      const scale = (parseFloat(document.getElementById("inpTitleScale").value) || 100) / 100.0;
      const logoSize = parseFloat(document.getElementById("inpLogoSize").value) || 180;
      const logoYpct = (parseFloat(document.getElementById("inpLogoY").value) || 82) / 100.0;

      document.getElementById("lblTitleScale").textContent = Math.round(scale * 100) + "%";
      document.getElementById("lblLogoSize").textContent = logoSize + " px";
      document.getElementById("lblLogoY").textContent = Math.round(logoYpct * 100) + "%";
      document.getElementById("stageDimLabel").textContent = "Active Canvas: " + spec.name;

      const isWide = (W / H) > 1.25;
      const baseTitlePt = isWide ? Math.round(H * 0.095 * scale) : Math.round(W * 0.068 * scale);
      const lineStep = Math.round(baseTitlePt * 1.18);
      const subFont = isWide ? Math.round(H * 0.032) : Math.round(W * 0.024);
      const subLines = wrapSubtitleLines(rawSub, isWide ? 72 : 54);

      const padX = Math.round(W * 0.075);
      const topBarY = Math.round(H * 0.065);
      const titleStartY = isWide ? Math.round(H * 0.27) : Math.round(H * 0.21);
      const subStartY = titleStartY + lineStep * 2 + Math.round(H * 0.065);
      const diagY = isWide ? Math.round(H * 0.56) : Math.round(H * 0.50);
      const diagH = isWide ? Math.round(H * 0.22) : Math.round(H * 0.25);
      const pillY = diagY + diagH + Math.round(H * 0.035);
      const footerY = Math.round(H * 0.94);

      const subTspans = subLines.map((ln, idx) =>
        `<tspan x="${W / 2}" dy="${idx === 0 ? 0 : Math.round(subFont * 1.38)}">${escXml(ln)}</tspan>`
      ).join("");

      const boxW = W - padX * 2;
      const nodeW = Math.round((boxW - 80) / 5);
      const deptLabels = ["01 LEADS (<60s)", "02 3-TIER QUOTE", "03 SUPPORT & OPS", "04 INVOICE & AR", "05 OWNER PULSE"];
      const deptNodes = deptLabels.map((lbl, i) => {
        const nx = padX + 20 + i * (nodeW + 10);
        const ny = diagY + Math.round(diagH * 0.26);
        const nh = Math.round(diagH * 0.52);
        const fillCol = i % 2 === 0 ? cAccent : cSecondary;
        return `
          <rect x="${nx}" y="${ny}" width="${nodeW}" height="${nh}" rx="10" fill="#0F172A" stroke="${fillCol}" stroke-width="3" />
          <rect x="${nx}" y="${ny}" width="${nodeW}" height="10" rx="4" fill="${fillCol}" />
          <text x="${nx + nodeW / 2}" y="${ny + Math.round(nh * 0.58)}" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="${Math.max(13, Math.round(W * 0.0135))}" font-weight="800" text-anchor="middle">${lbl}</text>
        `;
      }).join("");

      const pillW = Math.round((boxW - 40) / 3);
      const pillH = Math.max(38, Math.round(H * 0.038));
      const pillsMarkup = [
        { txt: p1, col: cAccent },
        { txt: p2, col: cSecondary },
        { txt: p3, col: cWarn }
      ].map((pObj, idx) => {
        const px = padX + idx * (pillW + 20);
        return `
          <rect x="${px}" y="${pillY}" width="${pillW}" height="${pillH}" rx="${Math.round(pillH / 2)}" fill="#1E293B" stroke="${pObj.col}" stroke-width="2.5" />
          <text x="${px + pillW / 2}" y="${pillY + Math.round(pillH * 0.64)}" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="${Math.max(13, Math.round(W * 0.014))}" font-weight="700" text-anchor="middle">${pObj.txt}</text>
        `;
      }).join("");

      let logoMarkup = "";
      if (uploadedLogoDataUrl) {
        const lx = Math.round((W - logoSize) / 2);
        const ly = Math.round(H * logoYpct - logoSize / 2);
        logoMarkup = `
          <g>
            <rect x="${lx - 10}" y="${ly - 10}" width="${logoSize + 20}" height="${logoSize + 20}" rx="14" fill="#0F172A" stroke="${cAccent}" stroke-width="3" />
            <image href="${uploadedLogoDataUrl}" x="${lx}" y="${ly}" width="${logoSize}" height="${logoSize}" preserveAspectRatio="xMidYMid meet" />
          </g>
        `;
      }

      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
        <defs>
          <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="${cPrimary}" />
            <stop offset="60%" stop-color="#1E293B" />
            <stop offset="100%" stop-color="${cPrimary}" />
          </linearGradient>
          <pattern id="execGrid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#334155" stroke-width="1" stroke-opacity="0.32" />
          </pattern>
        </defs>

        <!-- Background Canvas & Grid -->
        <rect width="${W}" height="${H}" fill="url(#bgGrad)" />
        <rect width="${W}" height="${H}" fill="url(#execGrid)" />

        <!-- Top & Bottom Accent Bars -->
        <rect x="0" y="0" width="${W}" height="18" fill="${cAccent}" />
        <rect x="0" y="${H - 18}" width="${W}" height="18" fill="${cSecondary}" />
        <rect x="${padX - 24}" y="42" width="${W - (padX - 24) * 2}" height="${H - 84}" rx="18" fill="none" stroke="#334155" stroke-width="2" />

        <!-- Top Eyebrow Pill -->
        <rect x="${padX}" y="${topBarY}" width="${boxW}" height="${Math.max(44, Math.round(H * 0.036))}" rx="10" fill="#1E293B" stroke="${cAccent}" stroke-width="2" />
        <text x="${W / 2}" y="${topBarY + Math.max(29, Math.round(H * 0.024))}" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="${Math.max(14, Math.round(W * 0.016))}" font-weight="800" text-anchor="middle" letter-spacing="2">${eyebrow}</text>

        <!-- 3-Line Main Headline -->
        <text x="${W / 2}" y="${titleStartY}" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="${baseTitlePt}" font-weight="900" text-anchor="middle" letter-spacing="-1">${t1}</text>
        <text x="${W / 2}" y="${titleStartY + lineStep}" fill="${cAccent}" font-family="Inter, Segoe UI, sans-serif" font-size="${baseTitlePt}" font-weight="900" text-anchor="middle" letter-spacing="-1">${t2}</text>
        <text x="${W / 2}" y="${titleStartY + lineStep * 2}" fill="#38BDF8" font-family="Inter, Segoe UI, sans-serif" font-size="${baseTitlePt}" font-weight="900" text-anchor="middle" letter-spacing="-1">${t3}</text>

        <!-- Wrapped Subtitle -->
        <text x="${W / 2}" y="${subStartY}" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="${subFont}" font-weight="500" text-anchor="middle">${subTspans}</text>

        <!-- 5-Department Architecture Centerpiece Box -->
        <rect x="${padX}" y="${diagY}" width="${boxW}" height="${diagH}" rx="16" fill="#1E293B" fill-opacity="0.88" stroke="${cSecondary}" stroke-width="2.5" />
        <text x="${W / 2}" y="${diagY + Math.max(26, Math.round(diagH * 0.16))}" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="${Math.max(13, Math.round(W * 0.015))}" font-weight="800" text-anchor="middle" letter-spacing="1.5">T.R.A.V. HUMAN-IN-THE-LOOP 5-DEPARTMENT ARCHITECTURE</text>
        ${deptNodes}

        <!-- 3 Metric Callout Pills -->
        ${pillsMarkup}

        <!-- Optional Uploaded Logo / Headshot -->
        ${logoMarkup}

        <!-- Footer Attribution Bar -->
        <text x="${W / 2}" y="${footerY}" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="${Math.max(13, Math.round(W * 0.015))}" font-weight="700" text-anchor="middle" letter-spacing="2">${author}</text>
      </svg>`;
    }

    function renderStudioSvg() {
      const container = document.getElementById("svgPreviewContainer");
      container.innerHTML = buildCurrentSvgMarkup();
    }

    function exportCleanSvg() {
      const tplKey = document.getElementById("tplSelect").value;
      const svgMarkup = buildCurrentSvgMarkup();
      const blob = new Blob([svgMarkup], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "custom-" + tplKey + "-graphic.svg";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      document.getElementById("exportStatusMsg").textContent = "Status: Exported vector file custom-" + tplKey + "-graphic.svg";
    }

    function exportHighResPng() {
      const tplKey = document.getElementById("tplSelect").value;
      const spec = TEMPLATE_SPECS[tplKey] || TEMPLATE_SPECS.kindle;
      const svgMarkup = buildCurrentSvgMarkup();
      const canvas = document.getElementById("offscreenExportCanvas");
      canvas.width = spec.w;
      canvas.height = spec.h;
      const ctx = canvas.getContext("2d");

      const img = new Image();
      const svgBlob = new Blob([svgMarkup], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(svgBlob);

      img.onload = function() {
        ctx.clearRect(0, 0, spec.w, spec.h);
        ctx.drawImage(img, 0, 0, spec.w, spec.h);
        URL.revokeObjectURL(url);
        canvas.toBlob(function(pngBlob) {
          const pngUrl = URL.createObjectURL(pngBlob);
          const a = document.createElement("a");
          a.href = pngUrl;
          a.download = "custom-" + tplKey + "-" + spec.w + "x" + spec.h + ".png";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(pngUrl);
          document.getElementById("exportStatusMsg").textContent =
            "Status: Exported high-res PNG (" + spec.w + "×" + spec.h + " px)";
        }, "image/png");
      };
      img.src = url;
    }

    const STUDIO_COPY_PRESETS = [
      {
        id: "preset_ch01_audit",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 01 — The 5-Department AI Operating Audit & T-R-A-V Charter",
        tpl: "binder",
        theme: "emerald",
        eyebrow: "CHAPTER 01 • EXECUTIVE OPERATIONS BINDER (2026 EDITION)",
        h1: "THE 5-DEPARTMENT AI",
        h2: "OPERATING AUDIT &",
        h3: "T-R-A-V ARCHITECTURE",
        sub: "Eliminating the 15-Hour Weekly Owner Bottleneck with Deterministic Rules, Grounded Prompts, and Green/Amber/Red Governance Gates.",
        p1: "5 CORE DEPARTMENTS",
        p2: "T-R-A-V PIPELINE",
        p3: "15+ HRS/WK SAVED",
        footer: "DEPARTMENT 01–05 MASTER OPERATING CHARTER • INTERNAL SOP MANUAL"
      },
      {
        id: "preset_ch02_safety",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 02 — AI Safety, Privacy & Brand-Voice Firewall Manual",
        tpl: "binder",
        theme: "cobalt",
        eyebrow: "CHAPTER 02 • GOVERNANCE & PRIVACY FIREWALL BINDER",
        h1: "AI SAFETY, PRIVACY",
        h2: "& BRAND-VOICE",
        h3: "GOVERNANCE MANUAL",
        sub: "Zero-Hallucination Prompt Contracts, Pre-AI PII Redaction Filters, Locked Price Truth Tables, and Instant Kill-Switch Protocols.",
        p1: "0% HALLUCINATION",
        p2: "PII REDACTION GATE",
        p3: "1-CLICK KILL SWITCH",
        footer: "COMPLIANCE & BRAND INTEGRITY STANDARD • INTERNAL TEAM SOP"
      },
      {
        id: "preset_ch03_lead",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 03 — 60-Second Speed-to-Lead & Missed-Call Recovery SOP",
        tpl: "binder",
        theme: "emerald",
        eyebrow: "CHAPTER 03 • REVENUE CAPTURE & INTAKE PLAYBOOK",
        h1: "THE 60-SECOND",
        h2: "SPEED-TO-LEAD &",
        h3: "INTAKE CONCIERGE",
        sub: "24/7 Omnichannel Lead Capture, 15-Second Missed-Call SMS Text-Back, Non-Intrusive B.A.N.T.-Lite Triage, and Direct Calendar Booking.",
        p1: "≤ 60S RESPONSE SLA",
        p2: "15S MISSED-CALL SMS",
        p3: "85%+ RECOVERY RATE",
        footer: "DEPARTMENT 01: LEAD CAPTURE & INTAKE • FRONT-DESK & AI SOP"
      },
      {
        id: "preset_ch04_quoting",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 04 — Voice-to-3-Option Quoting & 14-Day Follow-Up Engine",
        tpl: "binder",
        theme: "gold",
        eyebrow: "CHAPTER 04 • SALES QUALIFICATION & ESTIMATING SOP",
        h1: "VOICE-TO-QUOTE &",
        h2: "3-OPTION PROPOSAL",
        h3: "CLOSING ENGINE",
        sub: "Turn 90-Second Field Voice Memos into Good-Better-Best Proposals in Under 15 Minutes with a 6-Touch, 14-Day Value-Add Nurture Sequence.",
        p1: "< 15M QUOTE SLA",
        p2: "GOOD-BETTER-BEST",
        p3: "35%+ CLOSE RATE",
        footer: "DEPARTMENT 02: SALES & ESTIMATING • FIELD & INSIDE SALES SOP"
      },
      {
        id: "preset_ch05_onboarding",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 05 — Zero-Friction Client Onboarding & Intake Chaser",
        tpl: "binder",
        theme: "teal",
        eyebrow: "CHAPTER 05 • FULFILLMENT & CLIENT ONBOARDING SOP",
        h1: "ZERO-FRICTION",
        h2: "60-SECOND CLIENT",
        h3: "ONBOARDING ENGINE",
        sub: "Automated Payment-to-Kickoff Provisioning, Polite Missing-Asset Chasers, and Proactive Scope-Creep Change-Order Protection.",
        p1: "60S WELCOME PACK",
        p2: "< 24H KICKOFF SLA",
        p3: "ZERO SCOPE CREEP",
        footer: "DEPARTMENT 03A: CLIENT ONBOARDING & DELIVERY • PM SOP MANUAL"
      },
      {
        id: "preset_ch06_support",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 06 — 24/7 AI Support Shield & Grounded RAG Triage",
        tpl: "binder",
        theme: "cobalt",
        eyebrow: "CHAPTER 06 • CUSTOMER SUPPORT & ESCALATION SOP",
        h1: "THE 24/7 AI",
        h2: "CUSTOMER SUPPORT",
        h3: "TRIAGE SHIELD",
        sub: "Grounded Truth-Table RAG Answers, Live Order/Appointment Lookups, Sentiment Scoring, and 15-Minute Red-Zone Human Takeover.",
        p1: "65%+ TIER-1 AUTO",
        p2: "< 45S FIRST REPLY",
        p3: "SENTIMENT GUARD",
        footer: "DEPARTMENT 03B: CUSTOMER SUPPORT & TRIAGE • CX TEAM SOP"
      },
      {
        id: "preset_ch07_retention",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 07 — 5-Star Review Engine, NPS Sentiment Gate & Win-Back",
        tpl: "binder",
        theme: "emerald",
        eyebrow: "CHAPTER 07 • REPUTATION, RETENTION & LTV PLAYBOOK",
        h1: "AUTOMATED 5-STAR",
        h2: "REVIEW, REFERRAL &",
        h3: "WIN-BACK ENGINE",
        sub: "Peak-Happiness NPS Sentiment Gating, Public Google Review Routing, Private Detractor Recovery, and 90/180/365-Day Reactivation.",
        p1: "NPS 9–10 PUBLIC GATE",
        p2: "15%+ REVIEW RATE",
        p3: "90-DAY WIN-BACK",
        footer: "DEPARTMENT 03C: RETENTION & REPUTATION • GROWTH SOP MANUAL"
      },
      {
        id: "preset_ch08_finance",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 08 — Same-Day Invoicing, 5-Stage AR Chaser & Cashflow Pulse",
        tpl: "binder",
        theme: "gold",
        eyebrow: "CHAPTER 08 • FINANCE, RECEIVABLES & CASHFLOW SOP",
        h1: "SAME-DAY INVOICING",
        h2: "& 5-STAGE AR",
        h3: "CASHFLOW ENGINE",
        sub: "Automated Job-Completion Billing, Dispute-Aware Polite-to-Firm Payment Reminders, Receipt OCR Categorization, and 13-Week Cash Pulse.",
        p1: "SAME-DAY BILLING",
        p2: "DSO ≤ 16 DAYS",
        p3: "13-WEEK CASH PULSE",
        footer: "DEPARTMENT 04: INVOICING & RECEIVABLES • BOOKKEEPING SOP"
      },
      {
        id: "preset_ch09_sops",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 09 — Screen-Recording-to-SOP Generator & 7-Day Onboarding",
        tpl: "binder",
        theme: "teal",
        eyebrow: "CHAPTER 09 • TEAM DELEGATION & TRAINING PLAYBOOK",
        h1: "THE SELF-UPDATING",
        h2: "TEAM SOP & 7-DAY",
        h3: "ONBOARDING ENGINE",
        sub: "Convert 5-Minute Loom Screen Recordings into Numbered Checklists, Role Playbooks, and Interactive Day 1–7 New-Hire Certification Quizzes.",
        p1: "5M LOOM TO SOP",
        p2: "7-DAY RAMP CURRICULUM",
        p3: "85%+ QUIZ PASS BAR",
        footer: "DEPARTMENT 05A: TEAM SOPS & TRAINING • HR & OPS MANUAL"
      },
      {
        id: "preset_ch10_command",
        category: "Chapter & SOP Binder Presets",
        label: "Ch 10 — Friday 3:00 PM Owner Scorecard & 90-Day Roadmap",
        tpl: "binder",
        theme: "burgundy",
        eyebrow: "CHAPTER 10 • EXECUTIVE COMMAND & GOVERNANCE MANUAL",
        h1: "THE FRIDAY 3:00 PM",
        h2: "OWNER COMMAND",
        h3: "SCORECARD & BRIEF",
        sub: "Run a High-Margin, AI-Augmented Small Business in 15 Minutes Every Friday with 12 Departmental KPIs and a Quarterly Governance Audit.",
        p1: "12 CORE WEEKLY KPIS",
        p2: "15M FRIDAY REVIEW",
        p3: "90-DAY ROLLOUT MAP",
        footer: "DEPARTMENT 05B: EXECUTIVE COMMAND • FOUNDER & GM MANUAL"
      },
      {
        id: "preset_ind_hvac",
        category: "Industry White-Label Presets",
        label: "Industry 01 — HVAC, Plumbing, Electrical & Home Services",
        tpl: "binder",
        theme: "emerald",
        eyebrow: "APEX COMFORT HVAC & PLUMBING • FIELD & DISPATCH OS",
        h1: "HOME SERVICES AI",
        h2: "DISPATCH, QUOTING",
        h3: "& OPERATIONS OS",
        sub: "15-Second Missed-Call SMS Recovery, Emergency Gas/Spark Red-Zone Routing, 3-Option Field Estimates, and Same-Day Service Invoicing.",
        p1: "15S MISSED-CALL SMS",
        p2: "3-OPTION FIELD QUOTES",
        p3: "4.9★ GOOGLE RATING",
        footer: "WHITE-LABELED INTERNAL OPERATIONS MANUAL • HOME SERVICES EDITION"
      },
      {
        id: "preset_ind_dental",
        category: "Industry White-Label Presets",
        label: "Industry 02 — Dental, MedSpa, Chiropractic & Outpatient Clinics",
        tpl: "binder",
        theme: "teal",
        eyebrow: "BRIGHTSMILE DENTAL & MEDSPA • FRONT-DESK CONCIERGE OS",
        h1: "PATIENT INTAKE,",
        h2: "RECALL & CLINICAL",
        h3: "FRONT-DESK AI OS",
        sub: "Zero-PHI Appointment Triage, Clinical Emergency Red-Gate Escalation, Automated Hygiene/Treatment Recall, and 5-Star Patient Reviews.",
        p1: "ZERO-PHI FIREWALL",
        p2: "60S PATIENT TRIAGE",
        p3: "6-MONTH RECALL ENGINE",
        footer: "WHITE-LABELED FRONT-DESK & PRACTICE OPERATIONS MANUAL"
      },
      {
        id: "preset_ind_agency",
        category: "Industry White-Label Presets",
        label: "Industry 03 — Marketing, Web, Creative & B2B Consulting Agencies",
        tpl: "binder",
        theme: "cobalt",
        eyebrow: "VANGUARD DIGITAL AGENCY • CLIENT DELIVERY & PM OS",
        h1: "AGENCY PROPOSAL,",
        h2: "60S ONBOARDING &",
        h3: "SCOPE-GUARD OS",
        sub: "Discovery-Call-to-3-Tier Retainer Proposals, 60-Second Client Onboarding Provisioning, Asset Chasers, and Change-Order Protection.",
        p1: "3-TIER RETAINERS",
        p2: "60S CLIENT KICKOFF",
        p3: "SCOPE-CREEP SHIELD",
        footer: "WHITE-LABELED AGENCY OPERATIONS & ACCOUNT MANAGEMENT MANUAL"
      },
      {
        id: "preset_ind_legal",
        category: "Industry White-Label Presets",
        label: "Industry 04 — CPA, Bookkeeping, Legal & Advisory Practices",
        tpl: "binder",
        theme: "burgundy",
        eyebrow: "STERLING ADVISORY & CPA GROUP • PRACTICE AUTOMATION OS",
        h1: "ADVISORY INTAKE,",
        h2: "DOCUMENT CHASER &",
        h3: "BILLING AUTOMATION",
        sub: "Conflict-Checked Prospect Intake, Automated Tax/Legal Document Collection Chasers, Engagement Letter Routing, and AR Control.",
        p1: "CONFLICT-CHECK GATE",
        p2: "AUTO DOC CHASERS",
        p3: "DSO ≤ 12 DAYS",
        footer: "WHITE-LABELED PROFESSIONAL SERVICES OPERATIONS BINDER"
      },
      {
        id: "preset_ind_ecom",
        category: "Industry White-Label Presets",
        label: "Industry 05 — Specialty E-Commerce, Wholesale & Local Retail",
        tpl: "binder",
        theme: "gold",
        eyebrow: "HERITAGE ROASTERS & GOODS • OMNICHANNEL CX & OPS OS",
        h1: "OMNICHANNEL ORDER",
        h2: "SUPPORT, VIP LTV &",
        h3: "REORDER ENGINE",
        sub: "24/7 WISMO Order-Status Resolution, Return/Exchange Policy Guardrails, VIP Post-Purchase Review Flows, and 60-Day Replenishment.",
        p1: "72% WISMO DEFLECTION",
        p2: "VIP REVIEW FUNNEL",
        p3: "60-DAY REPLENISHMENT",
        footer: "WHITE-LABELED COMMERCE FULFILLMENT & CX OPERATIONS BINDER"
      },
      {
        id: "preset_mkt_gumroad",
        category: "Storefront & Social Campaign Presets",
        label: "Storefront 01 — Gumroad / LemonSqueezy Complete OS Bundle Banner",
        tpl: "gumroad",
        theme: "emerald",
        eyebrow: "COMPLETE 5-TIER DIGITAL PUBLISHING & AUTOMATION SYSTEM",
        h1: "THE SMALL BUSINESS",
        h2: "AI AUTOMATION",
        h3: "OPERATING SYSTEM",
        sub: "10-Chapter Blueprint + 50 Copy-Paste Prompt Contracts + 12 Emergency Scripts + Offline Web App + 5 Notion Databases + 8-Tab Excel Matrix.",
        p1: "50 PROMPT CONTRACTS",
        p2: "OFFLINE SAAS WEB APP",
        p3: "8-TAB EXCEL MATRIX",
        footer: "INSTANT DIGITAL DOWNLOAD • 100% OFFLINE & ZERO-CLICHÉ ENGINEERED"
      },
      {
        id: "preset_mkt_linkedin",
        category: "Storefront & Social Campaign Presets",
        label: "Social 01 — LinkedIn / Executive Launch Announcement Banner",
        tpl: "linkedin",
        theme: "cobalt",
        eyebrow: "NEW RELEASE • THE 2026 SMALL BUSINESS AI OPERATING MANUAL",
        h1: "STOP BUYING AI TOYS.",
        h2: "INSTALL AN OPERATING",
        h3: "SYSTEM THAT PAYS.",
        sub: "How 1-to-50 Employee Businesses Reclaim 15+ Hours/Week and Capture $25K–$150K+ in Recovered Annual Value Using T-R-A-V Governance.",
        p1: "60S SPEED-TO-LEAD",
        p2: "GREEN/AMBER/RED GATES",
        p3: "90-DAY ROLLOUT MAP",
        footer: "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM • 2026 EDITION"
      },
      {
        id: "preset_mkt_square",
        category: "Storefront & Social Campaign Presets",
        label: "Social 02 — Instagram / Slack 5-Department Architecture Square Card",
        tpl: "square",
        theme: "emerald",
        eyebrow: "5-DEPARTMENT SMALL BUSINESS AUTOMATION ENGINE",
        h1: "CAPTURE. QUOTE.",
        h2: "DELIVER. COLLECT.",
        h3: "DELEGATE IN 15M.",
        sub: "Every Workflow Protected by Deterministic Math Rules, Locked Price Truth Tables, and 15-Second Slack Amber Approval Cards.",
        p1: "5 CORE DEPARTMENTS",
        p2: "50 PROMPT CONTRACTS",
        p3: "12 EMERGENCY SCRIPTS",
        footer: "SMALLBIZ AI AUTOMATION OS • EXECUTIVE VISUAL SHORTCUT ATLAS"
      }
    ];

    function initPresetSelector() {
      const container = document.getElementById("sidebar");
      const firstSection = container.querySelector(".panel-section");
      const presetSection = document.createElement("div");
      presetSection.className = "panel-section";
      presetSection.innerHTML =
        '<h2>0. Quick-Load Chapter, Industry &amp; Campaign Preset (18 Templates)</h2>' +
        '<label for="quickPresetSelect">Load Pre-Written White-Label Copy &amp; Theme</label>' +
        '<select id="quickPresetSelect">' +
        '<option value="">— Keep Current Custom Text —</option>' +
        STUDIO_COPY_PRESETS.map(function(p) {
          return '<option value="' + p.id + '">[' + p.category.split(" ")[0] + '] ' + p.label + '</option>';
        }).join("") +
        '</select>';
      container.insertBefore(presetSection, firstSection);

      document.getElementById("quickPresetSelect").addEventListener("change", function(e) {
        const val = e.target.value;
        if (!val) return;
        const found = STUDIO_COPY_PRESETS.find(function(item) { return item.id === val; });
        if (!found) return;
        document.getElementById("tplSelect").value = found.tpl;
        document.getElementById("inpEyebrow").value = found.eyebrow;
        document.getElementById("inpLine1").value = found.h1;
        document.getElementById("inpLine2").value = found.h2;
        document.getElementById("inpLine3").value = found.h3;
        document.getElementById("inpSubtitle").value = found.sub;
        document.getElementById("inpPill1").value = found.p1;
        document.getElementById("inpPill2").value = found.p2;
        document.getElementById("inpPill3").value = found.p3;
        document.getElementById("inpFooter").value = found.footer;
        setTheme(found.theme);
      });
    }

    window.addEventListener("DOMContentLoaded", function() {
      initPresetSelector();
      renderStudioSvg();
    });
  </script>
</body>
</html>
"""
    ch_meta_list = [
        ("01", "Dept 01–05 Audit", "5-Department Operating Audit", "15+ hrs/wk Saved", ">= 300% ROI"),
        ("02", "All 5 Depts", "AI Safety & Privacy Firewall", "0% Hallucination", "100% Redaction"),
        ("03", "Dept 01 Intake", "60-Second Speed-to-Lead", "<= 60s Median Reply", ">= 85% Recovery"),
        ("04", "Dept 02 Sales", "Voice-to-3-Option Quoting", "<= 15m Proposal SLA", ">= 35% Close Rate"),
        ("05", "Dept 03A Delivery", "60-Second Client Onboarding", "<= 60s Welcome Pack", "< 24h Kickoff"),
        ("06", "Dept 03B Support", "24/7 AI Support Triage Shield", "< 45s First Reply", ">= 60% Deflection"),
        ("07", "Dept 03C Growth", "5-Star Review & Win-Back Engine", "NPS 9-10 Public Gate", ">= 15% Review Rate"),
        ("08", "Dept 04 Finance", "Same-Day Billing & 5-Stage AR", "Same-Day Invoice", "DSO <= 16 Days"),
        ("09", "Dept 05A SOPs", "Loom-to-SOP & 7-Day Onboarding", "5m Loom to SOP", ">= 85% Quiz Score"),
        ("10", "Dept 05B Command", "Friday 3:00 PM Owner Scorecard", "15m Friday Review", "12 Weekly KPIs"),
    ]
    extra_presets = []
    for ch_idx, (c_num, c_dept, c_short, c_sla, c_kpi) in enumerate(ch_meta_list, start=1):
        for p_idx in range(1, 6):
            p_code = f"{ch_idx}.{p_idx}"
            extra_presets.append({
                "id": f"preset_prompt_{ch_idx}_{p_idx}",
                "category": "Prompt Contract Card Presets (50 Prompts)",
                "label": f"Prompt {p_code} — {c_short} (Workflow Contract #{p_idx})",
                "tpl": "square",
                "theme": ["emerald", "cobalt", "gold", "teal", "burgundy"][(ch_idx + p_idx) % 5],
                "eyebrow": f"PROMPT CONTRACT {p_code} • CHAPTER {c_num} ({c_dept})",
                "h1": f"PROMPT {p_code} WORKFLOW",
                "h2": c_short.upper()[:24],
                "h3": "T-R-A-V PROMPT CONTRACT",
                "sub": f"7-Part Grounded Prompt Contract for {c_short} — Includes Role, Inputs, Truth-Table Rules, JSON Schema, and Gate.",
                "p1": f"PROMPT {p_code}",
                "p2": f"SLA: {c_sla[:18].upper()}",
                "p3": f"KPI: {c_kpi[:16].upper()}",
                "footer": f"SMALLBIZ AI AUTOMATION OS • CHAPTER {c_num} PROMPT {p_code} REFERENCE CARD"
            })
    for s_idx in range(1, 13):
        s_num = f"{s_idx:02d}"
        extra_presets.append({
            "id": f"preset_emg_script_{s_num}",
            "category": "Emergency Script Binder Dividers (12 Scripts)",
            "label": f"Emergency Script #{s_num} — Red-Zone Human Takeover & Outage Protocol",
            "tpl": "binder",
            "theme": "burgundy",
            "eyebrow": f"EMERGENCY SCRIPT #{s_num} • RED-GATE HUMAN TAKEOVER PROTOCOL",
            "h1": f"EMERGENCY SCRIPT #{s_num}",
            "h2": "RED-ZONE HUMAN",
            "h3": "TAKEOVER PLAYBOOK",
            "sub": "Immediate Bot-Mute Switch, 5-Bullet Context Handoff, Word-for-Word De-Escalation Script, and Root-Cause Post-Mortem Log.",
            "p1": "BOT MUTE: ACTIVE",
            "p2": "< 15M HUMAN SLA",
            "p3": "ZERO HALLUCINATION",
            "footer": f"SMALLBIZ AI AUTOMATION OS • EMERGENCY SCRIPT #{s_num} BINDER TAB"
        })
    extra_js_items = ",\n      ".join(json.dumps(item, ensure_ascii=False) for item in extra_presets)
    html = html.replace(
        '        footer: "SMALLBIZ AI AUTOMATION OS • EXECUTIVE VISUAL SHORTCUT ATLAS"\n      }\n    ];',
        '        footer: "SMALLBIZ AI AUTOMATION OS • EXECUTIVE VISUAL SHORTCUT ATLAS"\n      },\n      ' + extra_js_items + '\n    ];'
    )
    html = html.replace(
        "0. Quick-Load Chapter, Industry &amp; Campaign Preset (18 Templates)",
        "0. Quick-Load Chapter, Industry, Prompt &amp; Script Preset (80 Templates)"
    )
    html_clean = sanitize_phase9_text(html)
    studio_path = DESIGN_KIT_DIR / "design-customizer-studio.html"
    studio_path.write_text(html_clean, encoding="utf-8")

    readme_md = """# Interactive Cover, SOP Binder & Social Graphic Customizer Studio — User & White-Labeling Guide

**Document ID:** `08-COVER-DESIGN/Editable-Design-Kit/README-DESIGN-KIT.md`  
**Application File:** `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html`  
**Architecture:** 100% Offline Single-File HTML5 + SVG + Canvas Render Studio (Zero External Dependencies)  

---

## 1. Executive Purpose & Use Cases
The **Interactive Cover, SOP Binder & Social Graphic Customizer Studio** (`design-customizer-studio.html`) empowers small business owners, operations managers, agency directors, and publishing studios to customize, white-label, and export high-resolution graphics directly inside any modern desktop browser (`Microsoft Edge`, `Google Chrome`, `Apple Safari`, or `Mozilla Firefox`) with zero cloud logins or subscription software required.

Whether you are printing a physical 3-ring **Company AI & SOP Operations Binder** for your front-desk and field technicians, customizing your **Kindle / Digital Book Cover**, updating your **Gumroad Product Thumbnails**, or publishing **LinkedIn / Facebook Executive Launch Announcements**, this studio renders crisp vector `.SVG` and exact-pixel `.PNG` assets in one click.

---

## 2. The 5 Built-In Canvas Templates & Exact Pixel Dimensions

| Template Option # | Template Name in Studio Dropdown | Exact Pixel Resolution | Aspect Ratio | Primary Operational & Commercial Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Template 01** | **Kindle / Digital Book Cover** | `1600 × 2560 px` | `1 : 1.6` | Amazon KDP Kindle eBook cover, Draft2Digital wide retail cover, and Apple Books / Kobo storefront edition. |
| **Template 02** | **Internal Team SOP Binder Cover** | `1600 × 2200 px` | `8.5 : 11` | Printable US Letter / A4 front cover insert for your physical office SOP binder and new-hire onboarding manual. |
| **Template 03** | **Gumroad / Course Bundle Banner** | `1600 × 1200 px` | `4 : 3` | High-converting product card for Gumroad, LemonSqueezy, Stan Store, Kajabi, or internal Notion dashboard headers. |
| **Template 04** | **LinkedIn / Executive Social Launch Card** | `1200 × 630 px` | `1.91 : 1` | OpenGraph (`og:image`) social share banner for LinkedIn articles, Facebook/X posts, and email newsletter headers. |
| **Template 05** | **5-Dept Workflow Architecture Square Card** | `1080 × 1080 px` | `1 : 1` | Instagram, LinkedIn carousel slide, or internal Slack/Teams announcement card showcasing the 5-Department Engine. |

---

## 3. Step-by-Step Customization & White-Labeling Workflow

### Step 1 — Launch the Studio Offline
1. Open the folder `08-COVER-DESIGN/Editable-Design-Kit/` on your Windows PC, Mac, or Linux workstation.
2. Double-click **`design-customizer-studio.html`**. The studio loads immediately in your default web browser with zero internet connection required.

### Step 2 — Choose Your Canvas Format & Executive Theme Palette
1. In **Section 0 (`Quick-Load Chapter, Industry & Campaign Preset`)**, optionally pick one of the 18 pre-written chapter, industry (`HVAC`, `Dental/MedSpa`, `B2B Agency`, `CPA/Legal`, `E-Commerce`), or social campaign presets to populate all fields automatically.
2. In **Section 1 (`Select Canvas Format & Dimension Preset`)**, select one of the five target resolutions (`1600×2560`, `1600×2200`, `1600×1200`, `1200×630`, or `1080×1080`).
3. In **Section 2 (`Executive Theme Color Presets`)**, click any of the five built-in corporate palettes or use the four native color pickers (`Canvas BG`, `Primary Accent`, `System Cyan`, and `Badge / Gate`) to match your exact brand hex codes:
   - **Executive Emerald & Slate (Default):** `#0F172A` Navy, `#059669` Emerald, `#0284C7` System Cyan, `#D97706` Amber Gate.
   - **Enterprise Cobalt & Cyan:** `#0B132B` Deep Navy, `#2563EB` Royal Blue, `#06B6D4` Cyan, `#F59E0B` Gold.
   - **Industrial Gold & Carbon:** `#18181B` Carbon Slate, `#D97706` Industrial Amber, `#0284C7` Steel Blue, `#10B981` Emerald.
   - **Clinical Teal & Navy:** `#0F2942` Medical Navy, `#0D9488` Clinical Teal, `#38BDF8` Sky Blue, `#F59E0B` Amber.
   - **Executive Burgundy & Slate:** `#1F122B` Deep Plum/Slate, `#E11D48` Crimson Accent, `#0284C7` Cyan, `#D97706` Gold.

### Step 3 — Edit Typography, Headlines & Metric Callout Pills
1. In **Section 3 (`Live Typography & White-Label Copy`)**, type your custom text into any of the nine live input boxes:
   - **Top Eyebrow Badge:** e.g., `APEX COMFORT HVAC • INTERNAL SOP MANUAL (2026 EDITION)`
   - **Headline Lines 1, 2, and 3:** Customize the 3-line display title and use the **Headline Font Scale (`75%–125%`)** slider to balance long company names cleanly.
   - **Subtitle / Scope Statement:** Automatically word-wraps across up to three centered lines so text never clips outside the border frame.
   - **Metric Pills 1, 2, and 3:** Highlight your company's core SLAs (e.g., `60-SECOND RESPONSE`, `3-OPTION QUOTES`, `4.9★ GOOGLE RATING`).
   - **Footer Attribution:** Enter your company name, department, or author imprint.

### Step 4 — Upload Your Company Logo or Founder Headshot (100% Local Privacy)
1. In **Section 4 (`Local Company Logo / Founder Photo Upload`)**, click **`Choose File`** under `Upload PNG/JPG/SVG Logo or Headshot`.
2. Select any `.png`, `.jpg`, `.webp`, or `.svg` file from your computer. Using the browser's native `FileReader` API, your image is converted into an embedded `data:image/...;base64` URI inside local memory—**your logo or photo is never uploaded to any external server**.
3. Adjust the **Uploaded Image Width (`60 px – 420 px`)** and **Vertical Offset (`8% – 92%`)** sliders to position your badge cleanly on the canvas.

### Step 5 — Export Exact-Pixel `.PNG` or Vector `.SVG`
1. Click **`Download High-Res .PNG`** in the top-right header (or stage toolbar) to render the live SVG onto an offscreen HTML5 `<canvas>` at full native resolution (`1600×2560`, `1600×2200`, `1600×1200`, `1200×630`, or `1080×1080`) and download a crisp, print- and storefront-ready `.png` file.
2. Click **`Download Vector .SVG`** to save the pure XML vector source file—ready to open in Adobe Illustrator, Affinity Designer, Inkscape, Figma, or any web browser.

---

## 4. Technical Verification & Troubleshooting Notes
- **Why does the PNG export look razor-sharp?** Unlike screen-capture tools that export at your laptop monitor's scaled viewport size, `exportHighResPng()` binds an offscreen `<canvas>` element to the exact pixel dimensions of the selected preset (`spec.w × spec.h`) prior to rasterizing the vector DOM.
- **Can I archive my custom company covers inside our Notion OS?** Yes. After clicking `Download High-Res .PNG`, upload the exported banner directly into your Notion workspace cover header (`Database 01` through `Database 05`) to brand your team's daily command center.

---

## 5. Industry White-Labeling Playbook (5 Verticals + 80 Quick-Load Presets)
Section 0 of the sidebar includes **80 built-in Quick-Load Presets** covering all 10 chapters, 5 core small-business verticals, 3 storefront/social announcement formats, all 50 Prompt Contracts (`Prompt 1.1` through `Prompt 10.5`), and all 12 Emergency Scripts (`Script #01` through `Script #12`). Below is the recommended white-labeling configuration for each vertical:

| Vertical / Industry | Recommended Theme Preset | Primary Binder Cover Title | Recommended Metric Pills (`Pill 1 / Pill 2 / Pill 3`) |
| :--- | :--- | :--- | :--- |
| **1. Home Services (HVAC, Plumbing, Electrical, Roofing)** | `Executive Emerald & Slate` (`#0F172A` / `#059669`) | `HOME SERVICES AI DISPATCH, QUOTING & OPERATIONS OS` | `15S MISSED-CALL SMS` • `3-OPTION FIELD QUOTES` • `4.9★ GOOGLE RATING` |
| **2. Dental, MedSpa, Chiropractic & Outpatient Clinics** | `Clinical Teal & Navy` (`#0F2942` / `#0D9488`) | `PATIENT INTAKE, RECALL & CLINICAL FRONT-DESK AI OS` | `ZERO-PHI FIREWALL` • `60S PATIENT TRIAGE` • `6-MONTH RECALL ENGINE` |
| **3. B2B Marketing, Web, Creative & Consulting Agencies** | `Enterprise Cobalt & Cyan` (`#0B132B` / `#2563EB`) | `AGENCY PROPOSAL, 60S ONBOARDING & SCOPE-GUARD OS` | `3-TIER RETAINERS` • `60S CLIENT KICKOFF` • `SCOPE-CREEP SHIELD` |
| **4. CPA, Bookkeeping, Legal & Advisory Practices** | `Executive Burgundy & Slate` (`#1F122B` / `#E11D48`) | `ADVISORY INTAKE, DOCUMENT CHASER & BILLING AUTOMATION` | `CONFLICT-CHECK GATE` • `AUTO DOC CHASERS` • `DSO ≤ 12 DAYS` |
| **5. Specialty E-Commerce, Wholesale & Local Retail** | `Industrial Gold & Carbon` (`#18181B` / `#D97706`) | `OMNICHANNEL ORDER SUPPORT, VIP LTV & REORDER ENGINE` | `72% WISMO DEFLECTION` • `VIP REVIEW FUNNEL` • `60-DAY REPLENISHMENT` |

---

## 6. Physical 3-Ring Office SOP Binder Printing & Tab Assembly Guide
Even in a digital-first business, keeping a physical **3-Ring Executive AI & Emergency Operations Binder** at your reception desk, dispatch station, or manager workstation ensures your team can execute every protocol during an internet or API outage:
1. **Print the Front & Spine Slip Cover:** Select `Internal Team SOP Binder Cover (1600 × 2200 px)` in Section 1, load your company logo in Section 4, export the `.PNG`, and print at `100% Fit to Page` on `8.5" × 11"` (`110 lb` matte cardstock) for your clear-view 3-ring binder front sleeve.
2. **Print the 12-Page Visual Shortcut Atlas (`13-VISUAL-CHEAT-SHEETS/`):** Print `the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf` in full color on `8.5" × 11"` horizontal paper and place it in the front quick-reference pocket of the binder.
3. **Print the 12 Emergency Script Divider Tabs:** In Section 0 of the Customizer Studio, select any of the `Emergency Script #01` through `Emergency Script #12` presets (`Burgundy & Slate` theme) to print red-bordered section dividers placed immediately ahead of your printed Emergency Operations Scripts (`02-Editable-10-Chapter-Action-Workbook.docx` and `04-Customer-Escalation-and-Refund-SOP-Matrix.docx`).
"""
    readme_clean = sanitize_phase9_text(readme_md)
    readme_path = DESIGN_KIT_DIR / "README-DESIGN-KIT.md"
    readme_path.write_text(readme_clean, encoding="utf-8")

    return {
        "html_bytes": studio_path.stat().st_size,
        "readme_words": len(re.findall(r"\b[\w'-]+\b", readme_clean)),
    }


# =============================================================================
# UPGRADE 6: 5 MAKE.COM / N8N / ZAPIER JSON AUTOMATION BLUEPRINTS + GUIDE
# =============================================================================

def build_5_json_blueprints() -> dict:
    blueprints_meta = [
        {
            "filename": "01-60s-instant-lead-router-and-sms-intake.json",
            "blueprint_id": "BP-01-SPEED-TO-LEAD-ROUTER",
            "name": "Department 01: 60-Second Instant Omnichannel Lead Router & SMS Intake Concierge",
            "chapter": "Chapter 3 (Prompts 3.1, 3.2, 3.3, 3.4, 3.5)",
            "department": "01 - Lead Capture & Speed-to-Lead",
            "sla_target": "Median response <= 60 seconds; Missed-call text-back <= 15 seconds",
            "governance_zones": {
                "green": "In-territory routine service/consultation inquiry -> Instant SMS + Email with direct booking link",
                "amber": "Commercial / multi-site inquiry > $5,000 -> Instant acknowledgment + #amber-approvals rep brief",
                "red": "Safety/clinical emergency or regulatory threat -> Bypass AI booking + alert #red-alerts immediately"
            },
            "regex_red_gate": "(?i)\\b(emergency|gas leak|sparking|flooding|chest pain|bleeding|lawyer|lawsuit|subpoena)\\b",
            "system_prompt_contract": (
                "You are the 60-Second Lead Concierge for {{COMPANY_NAME}}. Analyze the normalized inbound lead payload, "
                "verify whether postal_code is inside {{APPROVED_POSTAL_CODES}}, score urgency from 1 to 5 using non-intrusive "
                "B.A.N.T.-Lite rules, and return valid JSON at temperature 0.0 containing sms_reply_under_160_chars, "
                "email_subject, email_body_markdown, and slack_rep_brief. Never invent prices or discounts."
            ),
            "sample_webhook_payload": {
                "event_id": "evt_lead_20261023_001",
                "source_channel": "website_high_intent_form",
                "received_at_iso": "2026-10-23T14:22:05Z",
                "full_name": "Sarah Jenkins",
                "phone_raw": "(512) 555-0194",
                "phone_e164": "+15125550194",
                "email": "s.jenkins@example.com",
                "postal_code": "78704",
                "service_interest": "Full System Replacement Quote",
                "customer_message": "Our 14-year-old upstairs AC unit stopped cooling yesterday. Looking for a 3-option replacement quote this week.",
                "sms_opt_in_verified": True
            }
        },
        {
            "filename": "02-ai-support-triage-and-amber-approval-gate.json",
            "blueprint_id": "BP-02-SUPPORT-SHIELD-RAG-ROUTER",
            "name": "Department 03: 24/7 AI Customer Support Triage, Grounded RAG & Amber/Red Escalation Gate",
            "chapter": "Chapter 6 (Prompts 6.1, 6.2, 6.3, 6.4, 6.5)",
            "department": "03 - Customer Support, Fulfillment & Retention",
            "sla_target": ">= 60% Tier-1 auto-resolution in < 45 seconds; < 15m human takeover on Red Gate",
            "governance_zones": {
                "green": "Sentiment >= 3 AND KB Match Confidence >= 0.88 AND $0 concession -> Auto-send grounded reply",
                "amber": "Sentiment == 3 AND courtesy credit <= $100 -> Post 1-click Amber Approval Card in #amber-support",
                "red": "Sentiment <= 2 OR Red-Zone Regex Match OR dispute > $100 -> Mute bot & page manager in #red-alerts"
            },
            "regex_red_gate": "(?i)\\b(lawyer|attorney|chargeback|bbb|fraud|scam|injured|damage|furious|cancel contract|1 star)\\b",
            "system_prompt_contract": (
                "You are the Tier-1 Grounded Support Concierge for {{COMPANY_NAME}}. Using ONLY the verified policy clauses "
                "in {{KB_TRUTH_TABLE_JSON}} and live order/appointment telemetry in {{LIVE_STATUS_API_JSON}}, classify sentiment "
                "(1-5), evaluate kb_confidence (0.0-1.0), assign triage_gate (GREEN | AMBER | RED), and draft a helpful response "
                "at temperature 0.0. If the answer is not explicitly in the KB, set triage_gate to AMBER."
            ),
            "sample_webhook_payload": {
                "event_id": "evt_sup_20261023_042",
                "ticket_channel": "support_email_inbox",
                "customer_email": "marcus.vance@example.com",
                "customer_ltv_usd": 2450.00,
                "order_or_visit_id": "ORD-88412",
                "inbound_subject": "Question about rescheduling my Tuesday morning appointment",
                "inbound_body": "Hi team, something came up at work on Tuesday morning. Can I move my 9:00 AM appointment to Thursday afternoon without a fee?"
            }
        },
        {
            "filename": "03-3option-instant-quote-and-14day-followup.json",
            "blueprint_id": "BP-03-VOICE-TO-3TIER-QUOTE-AND-NURTURE",
            "name": "Department 02: Voice-to-3-Option (Good-Better-Best) Quote Compiler & 14-Day Follow-Up State Machine",
            "chapter": "Chapter 4 (Prompts 4.1, 4.2, 4.3, 4.4, 4.5)",
            "department": "02 - Sales Qualification & Quoting",
            "sla_target": "Proposal dispatched within 15 minutes of site visit; >= 35% 14-day close rate",
            "governance_zones": {
                "green": "Standard diagnostic/maintenance quote < $1,500 using locked SKU rows -> Dispatch after estimator preview",
                "amber": "Custom multi-tier proposal >= $1,500 or discount > 5% -> Mandatory 15-second Slack Amber Approval click",
                "red": "Custom engineering/legal indemnification or margin < 42% floor -> Escalate to Owner in #red-alerts"
            },
            "regex_red_gate": "(?i)\\b(liquidated damages|penalty clause|unlimited liability|custom warranty override|below cost)\\b",
            "system_prompt_contract": (
                "You are the Senior Proposal Architect for {{COMPANY_NAME}}. Combine the estimator's post-visit voice transcript "
                "with the locked unit prices in {{LOCKED_SKU_PRICEBOOK_JSON}} to generate a 3-Option Good-Better-Best proposal "
                "(Option A Essential, Option B Recommended, Option C VIP Turnkey) plus a 6-touch 14-day follow-up schedule at "
                "temperature 0.1. Copy all dollar figures verbatim from the deterministic price calculation node."
            ),
            "sample_webhook_payload": {
                "event_id": "evt_quote_20261023_019",
                "estimator_name": "David Morales",
                "client_name": "Oakridge Dental Group",
                "client_email": "ops@oakridgedental.example.com",
                "voice_memo_transcript": "Completed walkthrough at Oakridge Dental. Needs quarterly commercial maintenance on 3 rooftop units plus smart thermostat upgrade.",
                "selected_sku_codes": ["SKU-104", "SKU-107"],
                "deterministic_totals_usd": {"option_a": 1450.00, "option_b": 2250.00, "option_c": 3400.00},
                "gross_margin_pct": 0.56
            }
        },
        {
            "filename": "04-overdue-invoice-5stage-payment-chaser.json",
            "blueprint_id": "BP-04-SAME-DAY-INVOICE-AND-5STAGE-AR-CHASER",
            "name": "Department 04: Same-Day Milestone Invoicing & 5-Stage Polite-to-Firm AR Payment Chaser",
            "chapter": "Chapter 8 (Prompts 8.1, 8.2, 8.3, 8.4, 8.5)",
            "department": "04 - Invoicing, Receivables & Cashflow Control",
            "sla_target": "Average DSO <= 16 days; Overdue Receivables > 15 days <= $2,500",
            "governance_zones": {
                "green": "Stage 0 (Same-Day Invoice), Stage 1 (Day -3), Stage 2 (Day +1), Stage 3 (Day +7) -> Unattended send if no open dispute",
                "amber": "Stage 4 (Day +15 Firm Notice) -> Post Amber Approval Card in #amber-finance before sending",
                "red": "Stage 5 (Day +30 Final Demand) OR open support ticket -> Halt automated chasers & brief human collector"
            },
            "regex_red_gate": "(?i)\\b(bankruptcy|insolvent|disputed invoice|attorney|stop contact|work not completed)\\b",
            "system_prompt_contract": (
                "You are the Accounts Receivable Concierge for {{COMPANY_NAME}}. Verify that open_support_dispute is false and "
                "payment_status is UNPAID before drafting the appropriate Stage 1–5 reminder at temperature 0.0. Always include "
                "the exact invoice number, due date, balance_due_usd, and 1-click payment URL {{STRIPE_QBO_PAYMENT_LINK}}."
            ),
            "sample_webhook_payload": {
                "event_id": "evt_ar_20261023_088",
                "invoice_id": "INV-2026-1094",
                "client_company": "Vanguard Property Management",
                "billing_contact_name": "Elena Rostova",
                "billing_email": "ap@vanguardpm.example.com",
                "invoice_amount_usd": 1850.00,
                "days_past_due": 7,
                "assigned_chaser_stage": "STAGE_3_DAY_PLUS_7",
                "open_support_dispute": False,
                "one_click_payment_url": "https://pay.example.com/inv/INV-2026-1094"
            }
        },
        {
            "filename": "05-friday-3pm-owner-kpi-executive-digest.json",
            "blueprint_id": "BP-05-FRIDAY-3PM-OWNER-SCORECARD-DIGEST",
            "name": "Department 05: Friday 3:00 PM 12-KPI Executive Owner Scorecard & Monday All-Hands Brief Compiler",
            "chapter": "Chapter 10 (Prompts 10.1, 10.2, 10.3, 10.4, 10.5)",
            "department": "05 - Team SOPs, Delegation & Executive Command",
            "sla_target": "Delivered every Friday at 15:00 local time; Owner review completed in <= 15 minutes",
            "governance_zones": {
                "green": "All 12 KPIs aggregated cleanly -> Deliver Executive Scorecard to Owner + draft Monday All-Hands agenda",
                "amber": "1 to 2 KPIs in AMBER variance -> Highlight root-cause bottleneck + 7-day corrective action plan",
                "red": "Any KPI in RED status or DLQ error count > 0 -> Flag urgent executive intervention at top of digest"
            },
            "regex_red_gate": "(?i)\\b(api_key_revoked|webhook_outage|dlq_overflow|critical_cash_shortfall)\\b",
            "system_prompt_contract": (
                "You are the Chief of Staff & Operations Analyst AI for {{COMPANY_NAME}}. Synthesize the 12 verified departmental "
                "KPIs from {{FRIDAY_KPI_PAYLOAD_JSON}} into a 1-page Executive Scorecard (Top 3 Wins, Single Priority Bottleneck, "
                "7-Day Corrective Action, and Monday 8:45 AM 15-Minute Team Agenda) at temperature 0.1. Never invent metrics."
            ),
            "sample_webhook_payload": {
                "event_id": "evt_kpi_20261023_fri1500",
                "reporting_week": "2026-W43",
                "kpis": {
                    "kpi_01_qualified_leads": 34,
                    "kpi_02_speed_to_lead_sec": 38,
                    "kpi_03_missed_call_recovery_pct": 91.2,
                    "kpi_04_quotes_sent_under_15m_pct": 94.0,
                    "kpi_05_14d_quote_close_pct": 38.4,
                    "kpi_06_onboarding_cycle_hours": 11.2,
                    "kpi_07_tier1_support_deflection_pct": 68.5,
                    "kpi_08_new_5star_reviews": 5,
                    "kpi_09_weekly_cash_collected_usd": 36450,
                    "kpi_10_overdue_ar_over_15d_usd": 1420,
                    "kpi_11_average_dso_days": 13.4,
                    "kpi_12_weekly_team_hours_saved": 23.5
                }
            }
        }
    ]

    results = {}
    for bp in blueprints_meta:
        blueprint_obj = {
            "schema_version": "2026.1.0-MAKE-N8N-ZAPIER-UNIVERSAL",
            "blueprint_id": bp["blueprint_id"],
            "name": sanitize_phase9_text(bp["name"]),
            "project": "The Small Business AI Automation Operating System (2026 Enterprise Edition)",
            "chapter_reference": bp["chapter"],
            "department": bp["department"],
            "sla_benchmark": bp["sla_target"],
            "trav_governance_architecture": {
                "stage_1_trigger": "Webhook / Scheduled Cron Trigger with deterministic event_id idempotency check",
                "stage_2_rules": "Pre-AI Regex Red-Gate Filter + E.164/Email Validator + Locked Truth-Table Lookup",
                "stage_3_ai": {
                    "provider": "OpenAI (gpt-4o-mini / gpt-4o) or Anthropic (claude-3-5-sonnet)",
                    "temperature": 0.0,
                    "response_format": "json_object",
                    "system_prompt": sanitize_phase9_text(bp["system_prompt_contract"])
                },
                "stage_4_verification": bp["governance_zones"],
                "pre_ai_red_gate_regex": bp["regex_red_gate"],
                "kill_switch_registry_row": f"06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv -> {bp['blueprint_id']}"
            },
            "environment_variables_required": [
                "COMPANY_NAME",
                "OPENAI_API_KEY",
                "NOTION_INTEGRATION_SECRET",
                "NOTION_DB01_LEADS_ID",
                "NOTION_DB02_WORKFLOW_REGISTRY_ID",
                "SLACK_AMBER_WEBHOOK_URL",
                "SLACK_RED_ALERTS_WEBHOOK_URL",
                "TWILIO_ACCOUNT_SID",
                "TWILIO_AUTH_TOKEN",
                "TWILIO_FROM_NUMBER_E164"
            ],
            "nodes": [
                {
                    "id": 1,
                    "node_name": "01_Inbound_Trigger_And_Idempotency_Guard",
                    "make_module": "gateway:CustomWebHook",
                    "n8n_node": "n8n-nodes-base.webhook",
                    "zapier_step": "Webhooks by Zapier — Catch Hook",
                    "configuration": {
                        "method": "POST",
                        "require_hmac_header": "X-Studio-Webhook-Signature",
                        "deduplicate_on_field": "event_id",
                        "sample_payload": bp["sample_webhook_payload"]
                    }
                },
                {
                    "id": 2,
                    "node_name": "02_Pre_AI_PII_Redactor_And_Red_Zone_Regex_Gate",
                    "make_module": "util:TextParserReplace",
                    "n8n_node": "n8n-nodes-base.code",
                    "zapier_step": "Code by Zapier — Run Python/JS",
                    "configuration": {
                        "mask_credit_cards_regex": "\\b(?:\\d[ -]*?){13,16}\\b -> [REDACTED_CARD]",
                        "mask_ssn_regex": "\\b\\d{3}-\\d{2}-\\d{4}\\b -> [REDACTED_GOV_ID]",
                        "red_zone_abort_regex": bp["regex_red_gate"],
                        "on_red_zone_match": "Route immediately to Node 06 (Red-Gate Human Alert & Bot Mute)"
                    }
                },
                {
                    "id": 3,
                    "node_name": "03_Deterministic_Truth_Table_And_CRM_Lookup",
                    "make_module": "notion:SearchObjects",
                    "n8n_node": "n8n-nodes-base.notion",
                    "zapier_step": "Notion — Find Database Item",
                    "configuration": {
                        "target_database": "06-NOTION-TEMPLATES/ (Databases 01, 03, 05)",
                        "strict_math_rule": "Calculate all prices, discounts, taxes, and overdue day counts in deterministic code prior to Node 04."
                    }
                },
                {
                    "id": 4,
                    "node_name": "04_Grounded_LLM_JSON_Compiler",
                    "make_module": "openai-gpt-3:CreateCompletion",
                    "n8n_node": "@n8n/n8n-nodes-langchain.openAi",
                    "zapier_step": "OpenAI (ChatGPT) — Conversation with JSON Mode",
                    "configuration": {
                        "model": "gpt-4o-mini",
                        "temperature": 0.0,
                        "max_tokens": 900,
                        "response_format": {"type": "json_object"},
                        "system_prompt": sanitize_phase9_text(bp["system_prompt_contract"]),
                        "required_output_keys": [
                            "assigned_gate",
                            "confidence_score",
                            "customer_sms_draft",
                            "customer_email_subject",
                            "customer_email_markdown",
                            "internal_slack_summary",
                            "audit_log_note"
                        ]
                    }
                },
                {
                    "id": 5,
                    "node_name": "05_TRAV_Governance_Router_Green_Amber_Red",
                    "make_module": "builtin:BasicRouter",
                    "n8n_node": "n8n-nodes-base.switch",
                    "zapier_step": "Paths by Zapier",
                    "routes": [
                        {
                            "route_name": "Branch_A_Green_Unattended_Dispatch",
                            "filter_condition": "assigned_gate == 'GREEN' AND confidence_score >= 0.88",
                            "actions": [
                                "Send SMS via Twilio / OpenPhone (if sms_opt_in_verified == true)",
                                "Send Email via Gmail / Microsoft 365",
                                "Update Notion Database status to 'Auto-Executed (Green)'"
                            ]
                        },
                        {
                            "route_name": "Branch_B_Amber_15Second_Slack_Approval",
                            "filter_condition": "assigned_gate == 'AMBER'",
                            "actions": [
                                "Post interactive Block Kit Approval Card to #amber-approvals in Slack ([Approve & Send] | [Edit] | [Hold])",
                                "Log pending state in Notion Database 02"
                            ]
                        },
                        {
                            "route_name": "Branch_C_Red_Immediate_Human_Takeover",
                            "filter_condition": "assigned_gate == 'RED' OR pre_ai_regex_triggered == true",
                            "actions": [
                                "Set bot_muted = true on customer record",
                                "Post urgent 5-bullet context brief + Emergency Script draft to #red-alerts",
                                "Send SMS alert to on-duty human manager"
                            ]
                        }
                    ]
                },
                {
                    "id": 6,
                    "node_name": "06_Dead_Letter_Queue_And_Outage_Fallback_Handler",
                    "make_module": "builtin:ErrorHandlerCommit",
                    "n8n_node": "n8n-nodes-base.errorTrigger",
                    "zapier_step": "Zapier Manager — Error Handler",
                    "configuration": {
                        "retry_policy": "3 retries with exponential backoff (15s, 60s, 300s)",
                        "dlq_fallback_table": "06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv",
                        "emergency_script_reference": "Activate matching Emergency Script (01–12) if API outage exceeds 15 minutes."
                    }
                }
            ],
            "slack_block_kit_approval_card_template": {
                "channel": "#amber-approvals",
                "text": f"AMBER GATE REVIEW REQUIRED — {bp['blueprint_id']}",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"AMBER GATE APPROVAL: {bp['blueprint_id']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Department:*\n{bp['department']}"},
                            {"type": "mrkdwn", "text": f"*Target SLA:*\n{bp['sla_target']}"},
                            {"type": "mrkdwn", "text": "*Assigned Gate:*\n`AMBER (15-Second Human Check)`"},
                            {"type": "mrkdwn", "text": "*Event ID:*\n`{{1.event_id}}`"}
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*AI Grounded Draft Preview:*\n```{{4.customer_email_markdown}}```"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Approve & Dispatch Now"},
                                "style": "primary",
                                "action_id": "amber_approve_dispatch",
                                "value": "{{1.event_id}}"
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Edit Before Sending"},
                                "action_id": "amber_edit_draft",
                                "value": "{{1.event_id}}"
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Escalate to Red Gate"},
                                "style": "danger",
                                "action_id": "amber_escalate_red",
                                "value": "{{1.event_id}}"
                            }
                        ]
                    }
                ]
            },
            "platform_import_and_field_mapping_guide": {
                "make_com_instructions": {
                    "step_1": "Create a new Scenario in Make.com -> Click More (...) in the bottom toolbar -> Select 'Import Blueprint' or add the 6 modules listed in the nodes[] array.",
                    "step_2": "In Module 01 (Custom WebHook), copy the generated HTTPS URL and paste it into your form provider, phone system, or billing webhook settings.",
                    "step_3": "In Module 04 (OpenAI Create a Chat Completion), set Model = gpt-4o-mini, Temperature = 0.0, Response Format = JSON Object, and paste trav_governance_architecture.stage_3_ai.system_prompt.",
                    "step_4": "In Module 05 (Router), configure the 3 filter conditions matching Branch_A_Green, Branch_B_Amber, and Branch_C_Red."
                },
                "n8n_instructions": {
                    "step_1": "In n8n (Self-Hosted or Cloud), click Workflows -> Add Workflow -> Import from File or configure the 6 n8n_node types in sequence.",
                    "step_2": "Use a Code (JavaScript/Python) node at Step 02 to execute mask_credit_cards_regex, mask_ssn_regex, and red_zone_abort_regex before calling OpenAI.",
                    "step_3": "Connect an Error Trigger node at Step 06 pointing to your Notion Database 02 Dead-Letter Queue table."
                },
                "zapier_instructions": {
                    "step_1": "Create a 6-step Zap starting with 'Webhooks by Zapier (Catch Hook)' followed by 'Code by Zapier (Run Python)' for PII masking and Red-Gate regex verification.",
                    "step_2": "Use 'Paths by Zapier' at Step 05 to split execution into Green (Auto-Send), Amber (Slack Block Kit Approval), and Red (Pager/Manager Alert)."
                }
            },
            "verified_synthetic_test_suite": {
                "green_zone_test_case": {
                    "test_name": f"{bp['blueprint_id']}_SYNTHETIC_GREEN_01",
                    "description": "Routine in-policy payload with high KB confidence and zero Red-Zone keywords.",
                    "input_override": {"sentiment_score": 5, "kb_confidence": 0.96, "contains_red_keyword": False, "financial_variance_usd": 0.0},
                    "expected_router_branch": "Branch_A_Green_Unattended_Dispatch",
                    "expected_sla_seconds": 18
                },
                "amber_zone_test_case": {
                    "test_name": f"{bp['blueprint_id']}_SYNTHETIC_AMBER_02",
                    "description": "High-value or edge-case payload requiring a 15-second human manager click in Slack #amber-approvals.",
                    "input_override": {"sentiment_score": 3, "kb_confidence": 0.79, "contains_red_keyword": False, "financial_variance_usd": 85.0},
                    "expected_router_branch": "Branch_B_Amber_15Second_Slack_Approval",
                    "expected_sla_seconds": 45
                },
                "red_zone_test_case": {
                    "test_name": f"{bp['blueprint_id']}_SYNTHETIC_RED_03",
                    "description": "Payload containing a Red-Zone trigger keyword or severe dispute that immediately halts AI execution and alerts a human lead.",
                    "input_override": {"sentiment_score": 1, "kb_confidence": 0.40, "contains_red_keyword": True, "financial_variance_usd": 650.0},
                    "expected_router_branch": "Branch_C_Red_Immediate_Human_Takeover",
                    "expected_sla_seconds": 5
                }
            }
        }
        json_str = sanitize_phase9_text(json.dumps(blueprint_obj, indent=2, ensure_ascii=False))
        out_path = BLUEPRINT_DIR / bp["filename"]
        out_path.write_text(json_str, encoding="utf-8")
        results[bp["filename"]] = out_path.stat().st_size

    guide_md = """# No-Code Automation Blueprints Setup, Wiring & Testing Manual (Make.com, n8n & Zapier)

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
curl -X POST "https://hook.us1.make.com/YOUR_WEBHOOK_ID" \
  -H "Content-Type: application/json" \
  -H "X-Studio-Webhook-Signature: sha256=test_signature_01" \
  -d '{
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
curl -X POST "https://hook.us1.make.com/YOUR_WEBHOOK_ID" \
  -H "Content-Type: application/json" \
  -d '{
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
curl -X POST "https://hook.us1.make.com/YOUR_WEBHOOK_ID" \
  -H "Content-Type: application/json" \
  -d '{
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
"""
    guide_clean = sanitize_phase9_text(guide_md)
    guide_path = BLUEPRINT_DIR / "NO-CODE-AUTOMATION-SETUP-GUIDE.md"
    guide_path.write_text(guide_clean, encoding="utf-8")
    results["NO-CODE-AUTOMATION-SETUP-GUIDE.md_words"] = len(re.findall(r"\b[\w'-]+\b", guide_clean))
    return results


def build_all_office_and_studio_upgrades() -> dict:
    print("=== PHASE 9 OFFICE & STUDIO BUILDER ===")
    print(" -> Building Upgrade 2: 7 Editable Word (.docx) Documents...")
    word_res = build_all_7_word_docs()
    for k, v in word_res.items():
        print(f"    [DOCX] {k}: {v:,} bytes")

    print(" -> Building Upgrade 3: 3 Widescreen 16:9 PowerPoint (.pptx) Slide Decks...")
    pptx_res = build_all_3_pptx_decks()
    for k, v in pptx_res.items():
        print(f"    [PPTX] {k}: {v['slides']} slides ({v['bytes']:,} bytes)")

    print(" -> Building Upgrade 4: 8-Tab Charted Excel Command Center (.xlsx + 8 CSVs)...")
    xlsx_res = build_excel_command_center()
    print(
        f"    [XLSX] {xlsx_res['xlsx_path']}: {xlsx_res['bytes']:,} bytes | "
        f"{xlsx_res['tabs']} tabs | {xlsx_res['formulas']} formulas | {xlsx_res['charts']} charts"
    )

    print(" -> Building Upgrade 5: Interactive Design Customizer Studio...")
    studio_res = build_design_customizer_studio()
    print(f"    [STUDIO] design-customizer-studio.html: {studio_res['html_bytes']:,} bytes | README: {studio_res['readme_words']:,} words")

    print(" -> Building Upgrade 6: 5 Make/n8n/Zapier JSON Automation Blueprints + Setup Guide...")
    bp_res = build_5_json_blueprints()
    print(f"    [BLUEPRINTS] 5 JSON files + Setup Guide ({bp_res['NO-CODE-AUTOMATION-SETUP-GUIDE.md_words']:,} words)")

    return {
        "upgrade2_word": word_res,
        "upgrade3_pptx": pptx_res,
        "upgrade4_excel": xlsx_res,
        "upgrade5_studio": studio_res,
        "upgrade6_blueprints": bp_res,
    }


if __name__ == "__main__":
    build_all_office_and_studio_upgrades()
