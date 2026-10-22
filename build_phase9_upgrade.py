#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 9 Master Upgrade & Final 5-Tier Bundle Packaging Builder (build_phase9_upgrade.py)
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)

Executes:
  1. Upgrade 1: 11 High-Res Vector SVG & PNG Cheat Sheets + 12-Page Landscape Visual Shortcut Atlas PDF
  2. Upgrades 2-6 via phase9_office_and_studio.build_all_office_and_studio_upgrades()
  3. Rebuilds all 5 Commercial .ZIP Bundles in 09-EXPORTS/HYBRID-BUNDLE/ with full Phase 1-9 inventory
"""

import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from pypdf import PdfReader

from phase9_office_and_studio import (
    build_all_office_and_studio_upgrades,
    sanitize_phase9_text,
)

STUDIO_ROOT = Path(__file__).resolve().parent
CHEAT_DIR = STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS"
EXPORT_PDF_DIR = STUDIO_ROOT / "09-EXPORTS" / "PDF"
BUNDLE_DIR = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE"

for d in (CHEAT_DIR, EXPORT_PDF_DIR, BUNDLE_DIR):
    d.mkdir(parents=True, exist_ok=True)


def find_browser_executable() -> str:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    raise FileNotFoundError("Neither Microsoft Edge nor Google Chrome was found on this system.")


def esc_xml(text: str) -> str:
    s = sanitize_phase9_text(str(text or ""))
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# =============================================================================
# UPGRADE 1: 11 VECTOR CHEAT SHEETS (.SVG + .PNG) & 12-PAGE ATLAS PDF
# =============================================================================

CHAPTER_CHEAT_SPECS = [
    {
        "num": 1,
        "dept": "DEPT 05 • STRATEGY & ALL 5 DEPTS",
        "title": "Chapter 1: The Small Business Automation Audit",
        "subtitle": "Finding Your $50,000+ Manual Bottlenecks via the 5-Day Task & Lead-Leak Diagnostic",
        "framework": "The 5-Department Engine & P.A.C.E. Prioritization Matrix (Pain, Annual Hours, Cashflow, Ease)",
        "formula": "Annual CMF = L_tax (Hrs × Rate × 52) + R_leak (Delayed Leads × Close% × LTV × 12) + C_drag",
        "sla": "Audit 100% of recurring tasks over 5 days; Automate #1 P.A.C.E. Quick-Win (>= 16/20) in Week 1",
        "green": "Read-only time-log synthesis, SaaS stack overlap audit, and internal CMF calculation.",
        "amber": "Publishing the Zero-Layoff Team Reallocation Memo & locking the 90-day sprint queue.",
        "red": "Never automate a broken or undocumented process before establishing a manual baseline.",
        "prompts": [
            "Prompt 1.1: 5-Day Time & Task Friction Synthesizer",
            "Prompt 1.2: Speed-to-Lead & Revenue-Leak Diagnostic",
            "Prompt 1.3: Redundant SaaS & Tool-Stack Cost Auditor",
            "Prompt 1.4: Workflow-to-T.R.A.V. Blueprint Mapper",
            "Prompt 1.5: Zero-Layoff Staff Reallocation Memo Writer"
        ],
        "actions": [
            "1. Log all recurring manual tasks across 5 days in Worksheet 01 (or Excel Tab 02).",
            "2. Run the Offline ROI Calculator to quantify your exact Annual CMF ($).",
            "3. Score top bottlenecks on the 20-point P.A.C.E. Matrix and select your Week-1 workflow."
        ],
        "kpi": "Friday KPI 12: Reclaim >= 18.0 Team & Owner Manual Admin Hours Per Week"
    },
    {
        "num": 2,
        "dept": "DEPT 05 • SYSTEMS & SAFETY GOVERNANCE",
        "title": "Chapter 2: The Human-in-the-Loop T.R.A.V. Architecture",
        "subtitle": "Designing Safe, Zero-Hallucination Workflows with Green, Amber, and Red Governance Gates",
        "framework": "T.R.A.V. 4-Stage Safety Contract (Trigger -> Rules -> AI -> Verification)",
        "formula": "Hallucination Risk = 0 when Price/Math = Deterministic Lookup & AI Temp <= 0.1 (JSON Mode)",
        "sla": "100% of LLM nodes wrapped in JSON Schema + Pre-AI Regex Filter + 60-Second Manual Kill Switch",
        "green": "75% of volume: Routine acknowledgments, booking links, and verified FAQ lookups run 24/7.",
        "amber": "20% of volume: Quotes > $1,500 & credits <= $100 pause for a 15-second Slack approval click.",
        "red": "5% of volume: Sentiment <= 2, legal/safety regex matches, or disputes > $100 mute bot immediately.",
        "prompts": [
            "Prompt 2.1: Workflow Risk & Governance Zone Classifier",
            "Prompt 2.2: Closed-World Truth-Table JSON Compiler",
            "Prompt 2.3: 15-Second Slack Amber Approval Card Builder",
            "Prompt 2.4: Pre-AI Regex PII & Payment Card Scrubber",
            "Prompt 2.5: Dead-Letter Queue (DLQ) & Outage Alert Monitor"
        ],
        "actions": [
            "1. Build your Locked Pricing & Policy Truth Table before connecting any LLM prompt node.",
            "2. Paste the Pre-AI Red-Zone Regex & PII Scrubber into Node 02 of Make.com / n8n.",
            "3. Register every active workflow and its 1-click Kill Switch URL in Notion Database 02."
        ],
        "kpi": "Safety SLA: 0% Unverified Price/Policy Hallucinations; < 60s Kill-Switch Execution"
    },
    {
        "num": 3,
        "dept": "DEPT 01 • LEAD CAPTURE & SPEED-TO-LEAD",
        "title": "Chapter 3: The 60-Second Lead Capture & Speed-to-Lead Engine",
        "subtitle": "Omnichannel Web, Phone, Missed-Call SMS, and Social Lead Routing 24/7",
        "framework": "I.N.S.T.A.N.T. 60-Second Router & Non-Intrusive B.A.N.T.-Lite Lead Scorer",
        "formula": "Rescued Lead Revenue = Delayed Leads/Mo × (60s Close% - Baseline Close%) × Avg LTV × 12",
        "sla": "Median Speed-to-Lead <= 60 seconds; Missed-Call Text-Back <= 15 seconds; Recovery >= 85%",
        "green": "In-territory routine service/consultation inquiries receive instant SMS + booking link.",
        "amber": "High-ticket commercial or multi-site inquiries trigger an instant rep brief in #inbound-leads.",
        "red": "Emergency hazards (gas leak, sparking, acute clinical pain) bypass AI and alert on-call lead.",
        "prompts": [
            "Prompt 3.1: Omnichannel Lead Normalizer & B.A.N.T.-Lite Scorer",
            "Prompt 3.2: 60-Second Personalized SMS & Email Concierge",
            "Prompt 3.3: Missed-Call Whisper Transcript & Text-Back Bot",
            "Prompt 3.4: Conversational 2-Way SMS Calendar Booker",
            "Prompt 3.5: 30-Minute Pre-Call Sales Rep Executive Brief"
        ],
        "actions": [
            "1. Connect website forms, OpenPhone/Twilio missed calls, and Meta Lead Ads to Blueprint 01.",
            "2. Configure E.164 phone normalization and postal-code territory verification in Node 02.",
            "3. Enable 30-minute pre-call rep briefings so reps enter every consultation prepared."
        ],
        "kpi": "Friday KPIs 01–03: Qualified Leads, Speed-to-Lead <= 60s, Missed-Call Recovery >= 85%"
    },
    {
        "num": 4,
        "dept": "DEPT 02 • SALES QUALIFICATION & QUOTING",
        "title": "Chapter 4: 3-Option Quotes & The 14-Day Follow-Up Loop",
        "subtitle": "Turning 90-Second Field Voice Memos into Good-Better-Best Proposals with Automated Nurture",
        "framework": "Voice-to-3-Tier Proposal Engine & 6-Touch Polite-Persistence State Machine",
        "formula": "Proposal Lift = Monthly Quotes × (Loop Close% - Baseline Close%) × Blended 3-Tier Ticket ($)",
        "sla": "90%+ of proposals dispatched within 15 minutes of site visit; 14-day close rate >= 35%",
        "green": "Standard diagnostic/tune-up quotes < $1,500 using locked SKU codes.",
        "amber": "All multi-option proposals >= $1,500 require a 15-second estimator click in #amber-approvals.",
        "red": "Any quote with gross margin < 42% floor or custom legal terms escalates to Owner.",
        "prompts": [
            "Prompt 4.1: 90s Field Voice Memo to 3-Tier Proposal Compiler",
            "Prompt 4.2: Executive ROI Proposal Cover Letter Writer",
            "Prompt 4.3: 14-Day 6-Touch Polite-Persistence Follow-Up Engine",
            "Prompt 4.4: Margin-Safe Price Objection Counter-Offer Builder",
            "Prompt 4.5: 90-Day Closed-Lost Estimate Seasonal Recycler"
        ],
        "actions": [
            "1. Lock your deterministic SKU Pricebook (Option A Essential, Option B Recommended, Option C VIP).",
            "2. Wire Blueprint 03 so estimators record a 90s voice memo immediately after every site visit.",
            "3. Configure the 14-day follow-up state machine to halt the instant Proposal_Status != Sent."
        ],
        "kpi": "Friday KPIs 04–05: >= 90% Quotes Sent < 15 Mins; >= 35% 14-Day Proposal Close Rate"
    },
    {
        "num": 5,
        "dept": "DEPT 03 • CLIENT ONBOARDING & FULFILLMENT",
        "title": "Chapter 5: Frictionless Zero-Drop Client Onboarding",
        "subtitle": "Wiring Payment Webhooks to Instant Portal Provisioning, Smart Intake & Scope Protection",
        "framework": "The 5-Stage Zero-Drop Handoff Architecture (Payment -> Provision -> Intake -> Brief -> Pulse)",
        "formula": "Onboarding Velocity Gain = Baseline Cycle Hours - Automated Payment-to-Kickoff Hours (<= 24h)",
        "sla": "Welcome packet & portal provisioned < 60s after deposit; Onboarding cycle time <= 24 hours",
        "green": "Folder creation, project board provisioning, welcome email, and milestone status pulses.",
        "amber": "Scope-creep detection alerts (Prompt 5.5) draft a polite Change Order for PM review.",
        "red": "Payment webhook signature failure or stalled onboarding > 7 days pages Account Director.",
        "prompts": [
            "Prompt 5.1: Sales-to-Fulfillment Handoff Brief Compiler",
            "Prompt 5.2: Instant Welcome Packet & Milestone Roadmap Writer",
            "Prompt 5.3: Incomplete Intake Document & Photo Validator",
            "Prompt 5.4: Polite Stalled-Onboarding Chaser Sequence",
            "Prompt 5.5: Scope-Creep Detector & Change-Order Draftsman"
        ],
        "actions": [
            "1. Connect Stripe/Square/QuickBooks Paid webhooks to automatic folder and board creation.",
            "2. Pre-fill client intake forms with discovery data so clients never type anything twice.",
            "3. Run Prompt 5.3 on uploaded files to verify completeness before unlocking the kickoff call."
        ],
        "kpi": "Friday KPI 06: Payment-to-Kickoff Client Onboarding Cycle Time <= 24.0 Hours"
    },
    {
        "num": 6,
        "dept": "DEPT 03 • CUSTOMER SUPPORT TRIAGE",
        "title": "Chapter 6: 24/7 AI Customer Support & Smart Escalation",
        "subtitle": "Deflecting 60%+ of Routine Tickets with Grounded RAG While Protecting Frustrated Clients",
        "framework": "The 3-Tier Support Shield (Tier 1 Green Auto-Resolve, Tier 2 Amber Draft, Tier 3 Red Takeover)",
        "formula": "Support Labor Saved = Monthly Tickets × Tier-1 Deflection% × (Avg Mins/Ticket ÷ 60) × Hourly Rate",
        "sla": ">= 60% Tier-1 tickets resolved in < 45 seconds; < 15m human response on Tier-3 Red alerts",
        "green": "Sentiment >= 3 AND KB Confidence >= 0.88 AND $0 refund -> Auto-resolve via Database 05.",
        "amber": "Sentiment == 3 AND courtesy credit <= $100 -> Post 1-click approval card in #amber-support.",
        "red": "Sentiment <= 2 OR Red-Zone Regex match OR refund > $100 -> Mute bot & page manager.",
        "prompts": [
            "Prompt 6.1: Ticket Sentiment, Intent & Urgency Classifier",
            "Prompt 6.2: Grounded RAG Tier-1 Knowledge Base Responder",
            "Prompt 6.3: Live Order / Appointment Status API Formatter",
            "Prompt 6.4: Angry Customer Red-Gate Brief & De-Escalation Draft",
            "Prompt 6.5: Weekly Unanswered Ticket & KB Gap Patcher"
        ],
        "actions": [
            "1. Populate Notion Database 05 with your Top 25 verified FAQs, policies, and escalation rules.",
            "2. Deploy Blueprint 02 with the Pre-AI Red-Zone Regex Filter active ahead of the LLM node.",
            "3. Run Prompt 6.5 every Friday at 2:00 PM to patch knowledge base gaps from escalated tickets."
        ],
        "kpi": "Friday KPI 07: Tier-1 Support Auto-Resolution Rate >= 60.0% with >= 4.8/5 CSAT"
    },
    {
        "num": 7,
        "dept": "DEPT 03 • REPUTATION, REVIEWS & RETENTION",
        "title": "Chapter 7: The Reputation, Review & Repeat-Sales Flywheel",
        "subtitle": "Sentiment-Gated 5-Star Google Reviews and Automated 60/90/180-Day Dormant Win-Backs",
        "framework": "The R.E.V.I.E.W. Sentiment-Gated Engine & 60/90/180-Day Win-Back Cohort Matrix",
        "formula": "Repeat Cohort Revenue = Dormant Contacts × Win-Back Booking% × Avg Repeat Order Value ($)",
        "sla": "Sentiment check sent 2h post-completion; >= 3 net new 5-star reviews/wk; 100% review replies < 24h",
        "green": "4–5 Star sentiment clicks route to Google Review page; public 4–5 star reviews get SEO reply.",
        "amber": "60/90/180-day batch recall campaigns previewed by marketing coordinator before dispatch.",
        "red": "1–3 Star sentiment clicks or negative public reviews route privately to Owner in #red-alerts.",
        "prompts": [
            "Prompt 7.1: Golden-Moment Post-Visit Sentiment Gate Classifier",
            "Prompt 7.2: Frictionless 5-Star Review Memory-Jogger Helper",
            "Prompt 7.3: Local SEO Public Google Review Responder",
            "Prompt 7.4: 60/90/180-Day Dormant Client Win-Back Writer",
            "Prompt 7.5: VIP Repeat-Buyer Churn Risk Early-Warning Scorer"
        ],
        "actions": [
            "1. Trigger a 1-click satisfaction pulse 2 hours after every completed job or delivered order.",
            "2. Route 4–5 star advocates to your direct Google review link and intercept 1–3 star feedback privately.",
            "3. Schedule monthly 60/90/180-day recall sequences to fill shoulder-season calendar capacity."
        ],
        "kpi": "Friday KPI 08: >= 3 Net New 5-Star Public Google Reviews Added Every Week"
    },
    {
        "num": 8,
        "dept": "DEPT 04 • INVOICING, RECEIVABLES & AP",
        "title": "Chapter 8: Automated Invoicing, AR Chasers & Expense OCR",
        "subtitle": "Same-Day Milestone Billing, 5-Stage Overdue Recovery, and 5% Supplier Price-Creep Protection",
        "framework": "Same-Day Billing Trigger, 5-Stage Polite-to-Firm AR State Machine & 3-Way AP Guard",
        "formula": "Working Capital Freed = (Baseline DSO - Automated DSO) × (Annual Credit Revenue ÷ 365)",
        "sla": "100% completed jobs billed same day; Average DSO <= 16 days; Overdue > 15d <= $2,500",
        "green": "Same-day invoices and Stages 1–3 reminders (Day -3, +1, +7) when open_support_dispute == false.",
        "amber": "Stage 4 (Day +15 Firm Notice) and supplier unit-price hikes > 5% require Slack approval.",
        "red": "Stage 5 (Day +30 Final Demand) or invoices linked to an open support dispute halt automation.",
        "prompts": [
            "Prompt 8.1: Field Job Notes to Itemized Invoice Formatter",
            "Prompt 8.2: 5-Stage Polite-to-Firm AR Payment Chaser Engine",
            "Prompt 8.3: Supplier Bill & Receipt Mobile OCR Extractor",
            "Prompt 8.4: 5% Vendor Unit-Price Creep & Overcharge Auditor",
            "Prompt 8.5: Monthly Pre-Close Reconciliation Anomaly Finder"
        ],
        "actions": [
            "1. Wire job completion sign-offs to Prompt 8.1 so itemized invoices + ACH links go out same day.",
            "2. Activate Blueprint 04 with the Dispute-Check Interlock so frustrated clients never get chased.",
            "3. Route vendor bills through Prompt 8.3 & 8.4 to flag unannounced supplier price hikes > 5%."
        ],
        "kpi": "Friday KPIs 09–11: Weekly Cash Collected, Overdue >15d <= $2,500, Avg DSO <= 16 Days"
    },
    {
        "num": 9,
        "dept": "DEPT 05 • TEAM SOPS & DELEGATION",
        "title": "Chapter 9: The Self-Running Team & Living SOP Engine",
        "subtitle": "Converting 3-Minute Loom Recordings into 7-Block Checklists & Voice-to-Task Delegation",
        "framework": "The 7-Block Living SOP Compiler, 60s Voice Delegation & Internal Ask-the-SOP Bot",
        "formula": "Delegation Leverage = (Owner Hours Saved/Wk × Owner Hourly Value) ÷ 3-Min Loom Recording Time",
        "sla": "Top 20 company SOPs documented in 7-Block format; New-hire ramp time reduced by >= 50%",
        "green": "Internal #ask-the-sop Slack bot answers staff procedural questions from Notion Database 03.",
        "amber": "Newly compiled 7-Block SOPs and 7-day onboarding quizzes reviewed by Dept Lead before publishing.",
        "red": "Safety-critical, clinical, or financial-signoff procedures require human supervisor sign-off.",
        "prompts": [
            "Prompt 9.1: 3-Minute Loom Transcript to 7-Block SOP Compiler",
            "Prompt 9.2: 60-Second Owner Voice Memo to Delegated Task Brief",
            "Prompt 9.3: Weekly Meeting Action-Item & Owner Extractor",
            "Prompt 9.4: Grounded Internal 'Ask-the-SOP' Staff Helper Bot",
            "Prompt 9.5: 7-Day New-Hire Onboarding Curriculum & Quiz Builder"
        ],
        "actions": [
            "1. Identify your Top 20 recurring tasks and record a 3-minute screen walkthrough the next time you do each.",
            "2. Run transcripts through Prompt 9.1 and store all 7-Block SOPs in Notion Database 03.",
            "3. Require staff to query #ask-the-sop before interrupting the owner with routine process questions."
        ],
        "kpi": "Friday KPI 12: 20+ Living SOPs Active; 80%+ Reduction in Routine Owner Interruptions"
    },
    {
        "num": 10,
        "dept": "DEPT 05 • EXECUTIVE COMMAND & 90-DAY ROLLOUT",
        "title": "Chapter 10: The 15-Minute Friday Owner Scorecard & Rollout",
        "subtitle": "Running Your Entire Business on 12 Weekly KPIs Across Sprints 1, 2, and 3",
        "framework": "The Friday 3:00 PM 12-Metric Executive Pulse & Quarterly Security/Drift Governance",
        "formula": "Net Automation ROI Multiple = Annualized CMF Recovered ($) ÷ Annual Tool-Stack Spend ($)",
        "sla": "Scorecard delivered Friday 3:00 PM; Owner review <= 15m; Monday All-Hands Huddle <= 15m",
        "green": "Weekly KPI aggregation (Blueprint 05) and Monday 8:45 AM team agenda generation.",
        "amber": "Any KPI in AMBER variance triggers a 7-day root-cause fix assigned to the metric owner.",
        "red": "Any KPI in RED variance for 2 consecutive weeks or DLQ errors > 0 triggers immediate audit.",
        "prompts": [
            "Prompt 10.1: Friday 3:00 PM 12-KPI Executive Scorecard Synthesizer",
            "Prompt 10.2: Custom 90-Day Phased Rollout Schedule Generator",
            "Prompt 10.3: Monthly Tool-Stack Spend vs. Labor ROI Auditor",
            "Prompt 10.4: Quarterly Prompt-Drift & API Security Reviewer",
            "Prompt 10.5: Monday 8:45 AM 15-Minute All-Hands Team Brief"
        ],
        "actions": [
            "1. Schedule Blueprint 05 to populate Notion Database 04 every Friday at 3:00 PM sharp.",
            "2. Spend 15 minutes reviewing the 12 KPIs and pick ONE Amber/Red bottleneck to solve next week.",
            "3. Run the Quarterly API Key Rotation & 50-Sample Drift Audit every 90 days."
        ],
        "kpi": "Master OS Target: All 12 Friday KPIs GREEN; 15–25+ Hours/Week Permanently Reclaimed"
    }
]


def generate_master_ecosystem_poster_svg() -> str:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000">
  <defs>
    <linearGradient id="bgMaster" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#1E293B" />
    </linearGradient>
  </defs>
  <rect width="1600" height="1000" fill="url(#bgMaster)" />
  <rect x="0" y="0" width="1600" height="12" fill="#059669" />
  <rect x="0" y="988" width="1600" height="12" fill="#0284C7" />

  <!-- Header Banner -->
  <rect x="36" y="28" width="1528" height="108" rx="14" fill="#1E293B" stroke="#059669" stroke-width="2.5" />
  <text x="64" y="64" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" letter-spacing="1.5">MASTER ARCHITECTURE POSTER • THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM (2026 EDITION)</text>
  <text x="64" y="102" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="30" font-weight="900">End-to-End 5-Department Engine, T.R.A.V. Safety Gate &amp; 90-Day Rollout Map</text>
  <rect x="1250" y="48" width="290" height="68" rx="10" fill="#0F172A" stroke="#0284C7" stroke-width="2" />
  <text x="1395" y="76" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" text-anchor="middle">50 PROMPTS • 12 SCRIPTS</text>
  <text x="1395" y="100" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="13" font-weight="700" text-anchor="middle">10 Chapters • 5 Notion DBs • 12 KPIs</text>

  <!-- Row 1: The T.R.A.V. 4-Stage Safety Contract Bar -->
  <rect x="36" y="154" width="1528" height="132" rx="12" fill="#0F172A" stroke="#334155" stroke-width="2" />
  <text x="60" y="182" fill="#F59E0B" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">LAYER 1: THE T.R.A.V. HUMAN-IN-THE-LOOP SAFETY CONTRACT (CHAPTER 2 FOUNDATION)</text>

  <rect x="60" y="196" width="350" height="74" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="78" y="222" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">1. TRIGGER (T)</text>
  <text x="78" y="244" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="12">Webhook, Missed Call, Paid Invoice, or Cron</text>
  <text x="78" y="261" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11">Deduplicated via unique event_id check</text>

  <rect x="434" y="196" width="360" height="74" rx="8" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="452" y="222" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">2. DETERMINISTIC RULES (R)</text>
  <text x="452" y="244" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="12">Pre-AI Regex Red Gate + PII Masking</text>
  <text x="452" y="261" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11">Locked SKU Pricebook &amp; FAQ Truth-Table Lookup</text>

  <rect x="818" y="196" width="350" height="74" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="836" y="222" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">3. GROUNDED AI (A)</text>
  <text x="836" y="244" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="12">Temperature 0.0–0.1 • Strict JSON Mode</text>
  <text x="836" y="261" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11">Zero math or ungrounded claims permitted</text>

  <rect x="1192" y="196" width="348" height="74" rx="8" fill="#1E293B" stroke="#D97706" stroke-width="2" />
  <text x="1210" y="222" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">4. VERIFICATION GATE (V)</text>
  <text x="1210" y="244" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="12">Green (75% Auto) • Amber (20% 15s Slack)</text>
  <text x="1210" y="261" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11">Red (5% Bot Mute + Human Takeover &lt;15m)</text>

  <!-- Row 2: The 5 Core Operating Departments (5 Vertical Pillars) -->
  <text x="44" y="316" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">LAYER 2: THE 5 CORE SMALL BUSINESS OPERATING DEPARTMENTS (CHAPTERS 1–10)</text>

  <!-- Dept 01 -->
  <rect x="36" y="330" width="292" height="390" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2.5" />
  <rect x="36" y="330" width="292" height="44" rx="10" fill="#059669" />
  <text x="182" y="358" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="15" font-weight="900" text-anchor="middle">DEPT 01: LEAD CAPTURE (CH 3)</text>
  <text x="54" y="400" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">SLA: &lt; 60s Speed-to-Lead 24/7</text>
  <text x="54" y="426" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Web, Phone, SMS &amp; Social Intake</text>
  <text x="54" y="448" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 15s Missed-Call Text-Back Bot</text>
  <text x="54" y="470" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Non-Intrusive B.A.N.T.-Lite Scorer</text>
  <text x="54" y="492" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 2-Way SMS Calendar Booking</text>
  <text x="54" y="514" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 30m Pre-Call Sales Rep Brief</text>
  <rect x="54" y="540" width="256" height="82" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="68" y="564" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700">PROMPTS 3.1 – 3.5 + BP-01</text>
  <text x="68" y="584" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="11">Notion DB 01: Inbound Leads CRM</text>
  <text x="68" y="604" fill="#34D399" font-family="Inter, Segoe UI, sans-serif" font-size="11" font-weight="700">KPIs 01, 02, 03 (&gt;=85% Call Rescue)</text>
  <rect x="54" y="636" width="256" height="64" rx="8" fill="#0F172A" stroke="#059669" />
  <text x="182" y="662" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="12" font-weight="800" text-anchor="middle">SPRINT 1 PRIORITY (DAYS 1–30)</text>
  <text x="182" y="684" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="11" text-anchor="middle">Rescues $3,000–$12,000/mo</text>

  <!-- Dept 02 -->
  <rect x="345" y="330" width="292" height="390" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2.5" />
  <rect x="345" y="330" width="292" height="44" rx="10" fill="#0284C7" />
  <text x="491" y="358" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="15" font-weight="900" text-anchor="middle">DEPT 02: QUOTING &amp; SALES (CH 4)</text>
  <text x="363" y="400" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">SLA: &lt; 15m 3-Tier Quote Turnaround</text>
  <text x="363" y="426" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 90s Field Voice Memo to Quote</text>
  <text x="363" y="448" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Locked SKU Pricebook Lookup</text>
  <text x="363" y="470" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Good / Better / Best Options</text>
  <text x="363" y="492" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 14-Day 6-Touch Follow-Up Loop</text>
  <text x="363" y="514" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Auto-Stop on Signature/Reply</text>
  <rect x="363" y="540" width="256" height="82" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="377" y="564" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700">PROMPTS 4.1 – 4.5 + BP-03</text>
  <text x="377" y="584" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="11">Amber Gate: 15s Estimator Click</text>
  <text x="377" y="604" fill="#34D399" font-family="Inter, Segoe UI, sans-serif" font-size="11" font-weight="700">KPIs 04, 05 (&gt;=35% 14d Close Rate)</text>
  <rect x="363" y="636" width="256" height="64" rx="8" fill="#0F172A" stroke="#0284C7" />
  <text x="491" y="662" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="12" font-weight="800" text-anchor="middle">SPRINT 2 PRIORITY (DAYS 31–45)</text>
  <text x="491" y="684" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="11" text-anchor="middle">+24% Average Order Value Lift</text>

  <!-- Dept 03 -->
  <rect x="654" y="330" width="292" height="390" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2.5" />
  <rect x="654" y="330" width="292" height="44" rx="10" fill="#059669" />
  <text x="800" y="358" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="15" font-weight="900" text-anchor="middle">DEPT 03: OPS, SUPPORT &amp; REVIEWS</text>
  <text x="672" y="400" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">SLA: &gt;=60% Support Deflection (Ch 5–7)</text>
  <text x="672" y="426" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Ch 5: Zero-Drop Client Onboarding</text>
  <text x="672" y="448" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Ch 5: Scope-Creep Early Warning</text>
  <text x="672" y="470" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Ch 6: 3-Tier Support Shield RAG</text>
  <text x="672" y="492" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Ch 7: Golden-Moment Review Gate</text>
  <text x="672" y="514" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Ch 7: 60/90/180d Dormant Recall</text>
  <rect x="672" y="540" width="256" height="82" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="686" y="564" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700">PROMPTS 5.1 – 7.5 + BP-02</text>
  <text x="686" y="584" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="11">Notion DB 05: Support &amp; FAQ Hub</text>
  <text x="686" y="604" fill="#34D399" font-family="Inter, Segoe UI, sans-serif" font-size="11" font-weight="700">KPIs 06, 07, 08 (&gt;=3 New 5★/Wk)</text>
  <rect x="672" y="636" width="256" height="64" rx="8" fill="#0F172A" stroke="#059669" />
  <text x="800" y="662" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="12" font-weight="800" text-anchor="middle">SPRINT 2 PRIORITY (DAYS 45–60)</text>
  <text x="800" y="684" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="11" text-anchor="middle">&lt;15m Human Red-Gate Takeover</text>

  <!-- Dept 04 -->
  <rect x="963" y="330" width="292" height="390" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2.5" />
  <rect x="963" y="330" width="292" height="44" rx="10" fill="#0284C7" />
  <text x="1109" y="358" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="15" font-weight="900" text-anchor="middle">DEPT 04: FINANCE &amp; AR (CH 8)</text>
  <text x="981" y="400" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">SLA: Avg DSO &lt;= 16 Days</text>
  <text x="981" y="426" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Same-Day Job Completion Billing</text>
  <text x="981" y="448" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 5-Stage Polite-to-Firm AR Chasers</text>
  <text x="981" y="470" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Support Dispute Interlock Check</text>
  <text x="981" y="492" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Mobile Vendor Bill &amp; Receipt OCR</text>
  <text x="981" y="514" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 5% Supplier Price-Creep Guard</text>
  <rect x="981" y="540" width="256" height="82" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="995" y="564" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700">PROMPTS 8.1 – 8.5 + BP-04</text>
  <text x="995" y="584" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="11">1-Click Stripe / QBO ACH Links</text>
  <text x="995" y="604" fill="#34D399" font-family="Inter, Segoe UI, sans-serif" font-size="11" font-weight="700">KPIs 09, 10, 11 (Overdue &lt;=$2.5K)</text>
  <rect x="981" y="636" width="256" height="64" rx="8" fill="#0F172A" stroke="#0284C7" />
  <text x="1109" y="662" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="12" font-weight="800" text-anchor="middle">SPRINT 3 PRIORITY (DAYS 61–75)</text>
  <text x="1109" y="684" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="11" text-anchor="middle">Unlocks Working Capital Fast</text>

  <!-- Dept 05 -->
  <rect x="1272" y="330" width="292" height="390" rx="12" fill="#1E293B" stroke="#D97706" stroke-width="2.5" />
  <rect x="1272" y="330" width="292" height="44" rx="10" fill="#D97706" />
  <text x="1418" y="358" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="15" font-weight="900" text-anchor="middle">DEPT 05: SOPS &amp; COMMAND (CH 9–10)</text>
  <text x="1290" y="400" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">SLA: 15m Friday Owner Scorecard</text>
  <text x="1290" y="426" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 3m Loom Video to 7-Block SOP</text>
  <text x="1290" y="448" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• 60s Voice-to-Task Delegation</text>
  <text x="1290" y="470" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Internal #ask-the-sop Slack Bot</text>
  <text x="1290" y="492" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Friday 3:00 PM 12-KPI Digest</text>
  <text x="1290" y="514" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• Monday 8:45 AM 15m Team Brief</text>
  <rect x="1290" y="540" width="256" height="82" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="1304" y="564" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700">PROMPTS 9.1 – 10.5 + BP-05</text>
  <text x="1304" y="584" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="11">Notion DBs 02, 03 &amp; 04</text>
  <text x="1304" y="604" fill="#34D399" font-family="Inter, Segoe UI, sans-serif" font-size="11" font-weight="700">KPI 12: &gt;=18 Hrs/Wk Reclaimed</text>
  <rect x="1290" y="636" width="256" height="64" rx="8" fill="#0F172A" stroke="#D97706" />
  <text x="1418" y="662" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="12" font-weight="800" text-anchor="middle">SPRINT 3 PRIORITY (DAYS 76–90)</text>
  <text x="1418" y="684" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="11" text-anchor="middle">Quarterly Drift &amp; Security Lock</text>

  <!-- Row 3: The 12 Friday Owner Scorecard KPIs & 90-Day Rollout Bar -->
  <rect x="36" y="742" width="1528" height="222" rx="14" fill="#0F172A" stroke="#059669" stroke-width="2" />
  <text x="60" y="772" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">LAYER 3: THE 15-MINUTE FRIDAY 3:00 PM OWNER SCORECARD (12 CORE EXECUTIVE KPIS) &amp; 5-DATABASE NOTION OS</text>

  <rect x="60" y="788" width="480" height="154" rx="10" fill="#1E293B" stroke="#334155" />
  <text x="80" y="814" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800">REVENUE &amp; SALES KPIS (01–05)</text>
  <text x="80" y="838" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 01: Weekly Qualified Inbound Leads (&gt;=25/wk)</text>
  <text x="80" y="860" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 02: Median Speed-to-Lead (&lt;=60 seconds)</text>
  <text x="80" y="882" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 03: Missed-Call Text-Back Recovery (&gt;=85%)</text>
  <text x="80" y="904" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 04: 3-Option Quotes Sent &lt;15m (&gt;=90%)</text>
  <text x="80" y="926" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 05: 14-Day Proposal Close Rate (&gt;=35%)</text>

  <rect x="560" y="788" width="480" height="154" rx="10" fill="#1E293B" stroke="#334155" />
  <text x="580" y="814" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800">DELIVERY, SUPPORT &amp; REVIEWS (06–08)</text>
  <text x="580" y="838" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 06: Payment-to-Onboarding Cycle (&lt;=24 hours)</text>
  <text x="580" y="860" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 07: Tier-1 Support Auto-Resolution (&gt;=60%)</text>
  <text x="580" y="882" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 08: Net New 5-Star Google Reviews (&gt;=3/wk)</text>
  <text x="580" y="908" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">12 RED-GATE EMERGENCY SCRIPTS (01–12)</text>
  <text x="580" y="928" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11">Ready-to-send fallback templates for outages &amp; VIP care</text>

  <rect x="1060" y="788" width="480" height="154" rx="10" fill="#1E293B" stroke="#334155" />
  <text x="1080" y="814" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800">CASHFLOW &amp; TEAM BANDWIDTH (09–12)</text>
  <text x="1080" y="838" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 09: Weekly Gross Cash Collected ($ Target)</text>
  <text x="1080" y="860" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 10: Overdue Receivables &gt;15 Days (&lt;=$2,500)</text>
  <text x="1080" y="882" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 11: Average Days Sales Outstanding (&lt;=16d)</text>
  <text x="1080" y="904" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="12">• KPI 12: Weekly Team &amp; Owner Hours Saved (&gt;=18h)</text>
  <text x="1080" y="928" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700">PRO WEB APP KEY: SMALLBIZ-OS-PRO-2026</text>
</svg>"""
    return sanitize_phase9_text(svg)


def generate_chapter_cheat_sheet_svg(spec: dict) -> str:
    ch = spec["num"]
    dept = esc_xml(spec["dept"])
    title = esc_xml(spec["title"])
    subtitle = esc_xml(spec["subtitle"])
    framework = esc_xml(spec["framework"])
    formula = esc_xml(spec["formula"])
    sla = esc_xml(spec["sla"])
    green = esc_xml(spec["green"])
    amber = esc_xml(spec["amber"])
    red = esc_xml(spec["red"])
    kpi = esc_xml(spec["kpi"])

    prompts_svg = ""
    for idx, p in enumerate(spec["prompts"]):
        py = 528 + idx * 38
        prompts_svg += f"""
        <rect x="60" y="{py}" width="700" height="30" rx="6" fill="#0F172A" stroke="#334155" stroke-width="1.2" />
        <text x="76" y="{py + 20}" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700">{esc_xml(p)}</text>
        """

    actions_svg = ""
    for idx, act in enumerate(spec["actions"]):
        ay = 532 + idx * 56
        actions_svg += f"""
        <rect x="820" y="{ay}" width="720" height="46" rx="8" fill="#0F172A" stroke="#059669" stroke-width="1.5" />
        <text x="838" y="{ay + 28}" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="13.5" font-weight="600">{esc_xml(act)}</text>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000">
  <defs>
    <linearGradient id="bgCh{ch:02d}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#1E293B" />
    </linearGradient>
  </defs>
  <rect width="1600" height="1000" fill="url(#bgCh{ch:02d})" />
  <rect x="0" y="0" width="1600" height="12" fill="#059669" />
  <rect x="0" y="988" width="1600" height="12" fill="#0284C7" />

  <!-- Top Header Card -->
  <rect x="36" y="28" width="1528" height="114" rx="14" fill="#1E293B" stroke="#059669" stroke-width="2.5" />
  <text x="64" y="62" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" letter-spacing="1.5">ONE-PAGE EXECUTIVE CHEAT SHEET • CHAPTER {ch:02d} OF 10 • {dept}</text>
  <text x="64" y="100" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="30" font-weight="900">{title}</text>
  <text x="64" y="128" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="15" font-weight="500">{subtitle}</text>

  <rect x="1310" y="46" width="230" height="78" rx="10" fill="#0F172A" stroke="#0284C7" stroke-width="2" />
  <text x="1425" y="78" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" text-anchor="middle">WORKSHEET {ch:02d}</text>
  <text x="1425" y="104" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Prompts {ch}.1 – {ch}.5</text>

  <!-- Row 1: Core Engineering Framework, Formula & SLA Target -->
  <rect x="36" y="160" width="750" height="130" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="60" y="190" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">1. CORE NAMED ENGINEERING FRAMEWORK</text>
  <text x="60" y="222" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="16" font-weight="800">{framework}</text>
  <text x="60" y="256" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700">SLA BENCHMARK: {sla}</text>

  <rect x="814" y="160" width="750" height="130" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="838" y="190" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">2. DETERMINISTIC FINANCIAL &amp; OPERATIONAL FORMULA</text>
  <rect x="838" y="206" width="702" height="64" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="1189" y="244" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" text-anchor="middle">{formula}</text>

  <!-- Row 2: T.R.A.V. Green / Amber / Red Governance Zones -->
  <rect x="36" y="308" width="1528" height="156" rx="12" fill="#0F172A" stroke="#334155" stroke-width="2" />
  <text x="60" y="338" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">3. CHAPTER {ch:02d} T.R.A.V. HUMAN-IN-THE-LOOP GOVERNANCE RULES (GREEN / AMBER / RED ZONES)</text>

  <rect x="60" y="354" width="480" height="92" rx="10" fill="#1E293B" stroke="#059669" stroke-width="2.5" />
  <text x="80" y="382" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">GREEN ZONE (UNATTENDED 24/7 AUTO)</text>
  <text x="80" y="412" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="13">{green}</text>

  <rect x="560" y="354" width="480" height="92" rx="10" fill="#1E293B" stroke="#D97706" stroke-width="2.5" />
  <text x="580" y="382" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">AMBER ZONE (15s SLACK APPROVAL CLICK)</text>
  <text x="580" y="412" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="13">{amber}</text>

  <rect x="1060" y="354" width="480" height="92" rx="10" fill="#1E293B" stroke="#EF4444" stroke-width="2.5" />
  <text x="1080" y="382" fill="#F87171" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">RED ZONE (BOT MUTE &amp; HUMAN TAKEOVER)</text>
  <text x="1080" y="412" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="13">{red}</text>

  <!-- Row 3: Left = 5 Prompts Index | Right = Top 3 Implementation Actions -->
  <rect x="36" y="482" width="750" height="260" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="60" y="512" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">4. CHAPTER {ch:02d} DETERMINISTIC AI PROMPT VAULT (PROMPTS {ch}.1 – {ch}.5)</text>
  {prompts_svg}

  <rect x="814" y="482" width="750" height="260" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="838" y="512" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800">5. TOP 3 IMPLEMENTATION ACTION STEPS THIS WEEK</text>
  {actions_svg}

  <!-- Row 4: Friday Owner Scorecard KPI Target & Kill-Switch Footer -->
  <rect x="36" y="762" width="1528" height="202" rx="14" fill="#1E293B" stroke="#059669" stroke-width="2.5" />
  <text x="64" y="796" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800">6. FRIDAY 3:00 PM OWNER SCORECARD TARGET &amp; COMPANION TOOLS</text>

  <rect x="64" y="814" width="920" height="64" rx="10" fill="#0F172A" stroke="#059669" stroke-width="2" />
  <text x="88" y="852" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="18" font-weight="800">{kpi}</text>

  <rect x="1008" y="814" width="528" height="64" rx="10" fill="#0F172A" stroke="#0284C7" stroke-width="2" />
  <text x="1272" y="842" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" text-anchor="middle">COMPANION ASSETS IN YOUR BUNDLE</text>
  <text x="1272" y="864" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="12" text-anchor="middle">Worksheet {ch:02d} • Mindmap &amp; Flowchart {ch:02d} • Notion OS Kit</text>

  <rect x="64" y="894" width="1472" height="50" rx="8" fill="#0F172A" stroke="#334155" />
  <text x="88" y="924" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700">60-SECOND KILL SWITCH RULE: If any schema error or unexpected customer reply occurs, pause workflow in Notion DB 02 &amp; activate Emergency Script.</text>
</svg>"""
    return sanitize_phase9_text(svg)


def render_svg_to_png(browser_exe: str, svg_path: Path, png_path: Path, width: int = 1600, height: int = 1000):
    svg_content = svg_path.read_text(encoding="utf-8")
    html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {width}px; height: {height}px; overflow: hidden; background: #0F172A; }}
  svg {{ display: block; width: {width}px; height: {height}px; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_wrapper)
        temp_html = Path(tf.name)
    try:
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={str(png_path)}",
            temp_html.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    finally:
        if temp_html.exists():
            temp_html.unlink()


def compile_12_page_visual_atlas_pdf(browser_exe: str, svg_paths: list) -> dict:
    """
    Compile 12-Page Landscape Visual Shortcut Atlas PDF (11in x 8.5in = 792 x 612 pt):
      - Page 1: Executive Visual Shortcut Atlas Cover & Governance Key
      - Page 2: 00-ECOSYSTEM-MASTER-MAP-POSTER.svg
      - Pages 3-12: cheat-sheet-ch01.svg .. cheat-sheet-ch10.svg
    """
    cover_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000">
      <rect width="1600" height="1000" fill="#0F172A" />
      <rect x="0" y="0" width="1600" height="18" fill="#059669" />
      <rect x="0" y="982" width="1600" height="18" fill="#0284C7" />
      <rect x="60" y="60" width="1480" height="880" rx="20" fill="#1E293B" stroke="#059669" stroke-width="3" />
      <rect x="120" y="120" width="1360" height="56" rx="10" fill="#0F172A" stroke="#0284C7" stroke-width="2" />
      <text x="800" y="156" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="18" font-weight="800" text-anchor="middle" letter-spacing="2">2026 ENTERPRISE EDITION • 12-PAGE EXECUTIVE VISUAL SHORTCUT ATLAS</text>

      <text x="800" y="290" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="56" font-weight="900" text-anchor="middle">THE SMALL BUSINESS AI AUTOMATION</text>
      <text x="800" y="362" fill="#059669" font-family="Inter, Segoe UI, sans-serif" font-size="56" font-weight="900" text-anchor="middle">VISUAL SHORTCUT ATLAS</text>
      <text x="800" y="425" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="22" font-weight="500" text-anchor="middle">Master Ecosystem Wall Poster + All 10 Chapter One-Page Executive Reference Sheets</text>

      <rect x="120" y="485" width="1360" height="310" rx="14" fill="#0F172A" stroke="#334155" stroke-width="2" />
      <text x="160" y="530" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="18" font-weight="800">HOW TO USE THIS 12-PAGE LANDSCAPE ATLAS WITH YOUR TEAM:</text>
      <text x="160" y="575" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="18">• Page 02 (Master Ecosystem Map): Print in US Letter/Tabloid Landscape and pin above your operations desk.</text>
      <text x="160" y="615" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="18">• Pages 03–12 (Chapter 01–10 Cheat Sheets): Hand the relevant 1-page sheet to each department owner during rollout.</text>
      <text x="160" y="655" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="18">• Color Governance Key: Emerald (#059669) = Unattended Green Gate • Amber (#D97706) = 15s Slack Approval • Red (#EF4444) = Human Takeover.</text>
      <text x="160" y="695" fill="#E2E8F0" font-family="Inter, Segoe UI, sans-serif" font-size="18">• Paired Interactive Tools: Use alongside smallbiz-automation-os-app.html (Pro Key: SMALLBIZ-OS-PRO-2026) &amp; Notion OS Kit.</text>
      <text x="160" y="745" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="700">INCLUDES: 10 Core Frameworks • 10 Deterministic Formulas • 50 Prompt References • 12 Friday Scorecard KPIs</text>

      <text x="800" y="885" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="700" text-anchor="middle">DIGITAL PUBLISHING STUDIO • PAGE 01 OF 12 • LANDSCAPE EXECUTIVE ATLAS EDITION</text>
    </svg>"""

    pages_html = [f'<div class="atlas-page">{cover_svg}</div>']
    for idx, sp in enumerate(svg_paths):
        svg_raw = sp.read_text(encoding="utf-8")
        is_last = idx == len(svg_paths) - 1
        cls = "atlas-page last-page" if is_last else "atlas-page"
        pages_html.append(f'<div class="{cls}">{svg_raw}</div>')

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: 11in 8.5in;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  html, body {{
    width: 11in;
    margin: 0;
    padding: 0;
    background: #0F172A;
  }}
  .atlas-page {{
    width: 11in;
    height: 8.48in;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0F172A;
  }}
  .atlas-page.last-page {{
    page-break-after: auto;
    break-after: auto;
  }}
  .atlas-page svg {{
    width: 11in;
    height: 8.48in;
    display: block;
  }}
</style>
</head>
<body>
{"".join(pages_html)}
</body>
</html>"""

    atlas_pdf_1 = CHEAT_DIR / "the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf"
    atlas_pdf_2 = EXPORT_PDF_DIR / "the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf"

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(full_html)
        temp_html = Path(tf.name)
    try:
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={str(atlas_pdf_1)}",
            temp_html.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=90)
    finally:
        if temp_html.exists():
            temp_html.unlink()

    shutil.copy2(atlas_pdf_1, atlas_pdf_2)
    reader = PdfReader(str(atlas_pdf_1))
    page_count = len(reader.pages)
    w_pt = float(reader.pages[0].mediabox.width)
    h_pt = float(reader.pages[0].mediabox.height)
    return {
        "pdf_path": str(atlas_pdf_1.relative_to(STUDIO_ROOT)),
        "export_copy_path": str(atlas_pdf_2.relative_to(STUDIO_ROOT)),
        "pages": page_count,
        "dimensions_pt": f"{w_pt:.1f} x {h_pt:.1f}",
        "bytes": atlas_pdf_1.stat().st_size,
    }


def build_upgrade_1_visual_cheat_sheets() -> dict:
    print("=== UPGRADE 1: Generating 11 Cheat Sheet SVGs, 11 PNGs & 12-Page Visual Shortcut Atlas PDF ===")
    browser_exe = find_browser_executable()
    svg_paths = []

    # 1. Master Ecosystem Poster
    master_svg_path = CHEAT_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.svg"
    master_png_path = CHEAT_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.png"
    master_svg = generate_master_ecosystem_poster_svg()
    ET.fromstring(master_svg)  # Validate XML
    master_svg_path.write_text(master_svg, encoding="utf-8")
    render_svg_to_png(browser_exe, master_svg_path, master_png_path, 1600, 1000)
    svg_paths.append(master_svg_path)
    print(f" -> Rendered {master_png_path.name} ({master_png_path.stat().st_size:,} bytes)")

    # 2. 10 Chapter Cheat Sheets
    for spec in CHAPTER_CHEAT_SPECS:
        ch = spec["num"]
        s_path = CHEAT_DIR / f"cheat-sheet-ch{ch:02d}.svg"
        p_path = CHEAT_DIR / f"cheat-sheet-ch{ch:02d}.png"
        svg_str = generate_chapter_cheat_sheet_svg(spec)
        ET.fromstring(svg_str)  # Validate XML
        s_path.write_text(svg_str, encoding="utf-8")
        render_svg_to_png(browser_exe, s_path, p_path, 1600, 1000)
        svg_paths.append(s_path)
        print(f" -> Rendered {p_path.name} ({p_path.stat().st_size:,} bytes)")

    # 3. 12-Page Landscape Visual Shortcut Atlas PDF
    atlas_info = compile_12_page_visual_atlas_pdf(browser_exe, svg_paths)
    print(
        f" -> Compiled 12-Page Visual Shortcut Atlas PDF: {atlas_info['pages']} pages "
        f"({atlas_info['dimensions_pt']} pt, {atlas_info['bytes']:,} bytes)"
    )
    return {
        "svg_count": len(svg_paths),
        "png_count": len(svg_paths),
        "atlas_pdf": atlas_info,
    }


# =============================================================================
# STEP 2: REBUILD ALL 5 COMMERCIAL .ZIP BUNDLES (09-EXPORTS/HYBRID-BUNDLE/)
# =============================================================================

def create_bundle_zip(zip_filename: str, tier_title: str, file_mappings: list) -> dict:
    zip_path = BUNDLE_DIR / zip_filename
    inventory_lines = [
        "================================================================================",
        "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM (2026 ENTERPRISE EDITION)",
        f"FINAL PRODUCTION PACKAGE INVENTORY: {tier_title}",
        "================================================================================",
        "",
        "INCLUDED FILES IN THIS ARCHIVE:",
    ]

    total_uncompressed = 0
    seen_arcnames = set()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src_rel, arcname in file_mappings:
            if arcname in seen_arcnames:
                continue
            seen_arcnames.add(arcname)
            src_path = STUDIO_ROOT / src_rel
            if not src_path.is_file():
                raise FileNotFoundError(f"Missing source file for {zip_filename}: {src_rel}")
            fsize = src_path.stat().st_size
            total_uncompressed += fsize
            zf.write(src_path, arcname=arcname)
            inventory_lines.append(f"  - {arcname} ({fsize:,} bytes)")

        inventory_lines.extend([
            "",
            "--------------------------------------------------------------------------------",
            "QUICK-START LAUNCH INSTRUCTIONS:",
            "1. Extract this .zip archive to a local folder on your workstation.",
            "2. Open PDF editions in Adobe Acrobat Reader, Microsoft Edge, or GoodNotes.",
            "3. Double-click `smallbiz-automation-os-app.html` (if included in your tier)",
            "   to launch the 100% offline SaaS-Lite Web Companion Suite in any browser.",
            "   (Tier 3 & Tier 4 buyers: enter Pro Key `SMALLBIZ-OS-PRO-2026`).",
            "4. Double-click `design-customizer-studio.html` (Tier 3 & Tier 4) to customize",
            "   and export high-resolution PNG/SVG covers, SOP binder covers, and social cards.",
            "================================================================================",
        ])
        readme_bytes = "\n".join(inventory_lines).encode("utf-8")
        total_uncompressed += len(readme_bytes)
        zf.writestr("README-BUNDLE-INVENTORY.txt", readme_bytes)

    return {
        "zip_file": f"09-EXPORTS/HYBRID-BUNDLE/{zip_filename}",
        "compressed_bytes": zip_path.stat().st_size,
        "compressed_mb": round(zip_path.stat().st_size / (1024 * 1024), 2),
        "uncompressed_bytes": total_uncompressed,
        "uncompressed_mb": round(total_uncompressed / (1024 * 1024), 2),
        "file_count": len(seen_arcnames) + 1,
    }


def rebuild_all_5_commercial_bundles() -> dict:
    print("\n=== STEP 2: Rebuilding All 5 Commercial .ZIP Bundles (Phase 9 Final Lock) ===")

    # 1. Tier 0: Free 5-Day Audit Starter Kit ($0)
    tier0_files = [
        ("09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf", "01-Book-Sample-and-Audit/tier0-free-sample-chapter01-and-audit.pdf"),
        ("05-WORKBOOKS/chapter-01-workbook.pdf", "01-Book-Sample-and-Audit/chapter-01-workbook.pdf"),
        ("07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html", "02-Interactive-ROI-Web-App/smallbiz-automation-os-app.html"),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", "02-Interactive-ROI-Web-App/README-WEB-APP.md"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", "03-Spreadsheet-Calculator/sheet1-automation-roi-and-leak-calculator.csv"),
        ("13-VISUAL-CHEAT-SHEETS/00-ECOSYSTEM-MASTER-MAP-POSTER.png", "04-Visual-Cheat-Sheets/00-ECOSYSTEM-MASTER-MAP-POSTER.png"),
        ("13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch01.png", "04-Visual-Cheat-Sheets/cheat-sheet-ch01.png"),
        ("04-VISUAL-ASSETS/chapter-01-mindmap.svg", "05-Architecture-Diagrams/chapter-01-mindmap.svg"),
        ("04-VISUAL-ASSETS/chapter-01-flowchart.svg", "05-Architecture-Diagrams/chapter-01-flowchart.svg"),
        ("08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png", "06-Cover/gumroad-tier0-free-audit-cover.png"),
    ]

    # 2. Tier 1: KDP & D2D Retail Book Pack ($9.99 / $16.99)
    tier1_files = [
        ("09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub", "01-Kindle-and-D2D-EPUB3/the-smallbiz-ai-automation-os.epub"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf", "02-KDP-Print-6x9-Interior/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf"),
        ("08-COVER-DESIGN/ebook-cover-kdp-kindle.png", "03-Retail-Covers/ebook-cover-kdp-kindle.png"),
        ("08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf", "03-Retail-Covers/kdp-paperback-full-wrap-cover.pdf"),
        ("08-COVER-DESIGN/kdp-paperback-full-wrap-cover.png", "03-Retail-Covers/kdp-paperback-full-wrap-cover.png"),
        ("10-MARKETING/marketplace-listings-and-bd-launch-runbook.md", "04-Publishing-Runbooks/marketplace-listings-and-bd-launch-runbook.md"),
        ("08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md", "04-Publishing-Runbooks/COVER-DESIGN-AND-PACKAGING-SPEC.md"),
    ]

    # 3. Tier 2: Interactive Workbook, Visual Shortcut Atlas & Tablet Planner Edition ($29)
    tier2_files = [
        ("09-EXPORTS/PDF/the-smallbiz-ai-automation-os-complete-book.pdf", "01-Master-Book/the-smallbiz-ai-automation-os-complete-book.pdf"),
        ("09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub", "01-Master-Book/the-smallbiz-ai-automation-os.epub"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-us-letter.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-us-letter.pdf"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-a4.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-a4.pdf"),
        ("09-EXPORTS/PDF/the-smallbiz-ai-automation-os-tablet-planner.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-tablet-planner.pdf"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/02-Editable-10-Chapter-Action-Workbook.docx", "02-Fillable-Workbooks-and-Planner/02-Editable-10-Chapter-Action-Workbook.docx"),
        ("13-VISUAL-CHEAT-SHEETS/the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf", "03-Visual-Shortcut-Atlas-and-Posters/the-smallbiz-ai-automation-os-visual-shortcut-atlas.pdf"),
        ("13-VISUAL-CHEAT-SHEETS/00-ECOSYSTEM-MASTER-MAP-POSTER.svg", "03-Visual-Shortcut-Atlas-and-Posters/00-ECOSYSTEM-MASTER-MAP-POSTER.svg"),
        ("13-VISUAL-CHEAT-SHEETS/00-ECOSYSTEM-MASTER-MAP-POSTER.png", "03-Visual-Shortcut-Atlas-and-Posters/00-ECOSYSTEM-MASTER-MAP-POSTER.png"),
        ("06-NOTION-TEMPLATES/Spreadsheets/62-Item-Prompt-and-SOP-Vault.csv", "04-Prompt-and-SOP-Vault/62-Item-Prompt-and-SOP-Vault.csv"),
        ("08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png", "07-Covers/gumroad-tier2-workbook-atlas-cover.png"),
    ]
    for ch in range(1, 11):
        tier2_files.append((f"13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch{ch:02d}.svg", f"03-Visual-Shortcut-Atlas-and-Posters/cheat-sheet-ch{ch:02d}.svg"))
        tier2_files.append((f"13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch{ch:02d}.png", f"03-Visual-Shortcut-Atlas-and-Posters/cheat-sheet-ch{ch:02d}.png"))
        tier2_files.append((f"04-VISUAL-ASSETS/chapter-{ch:02d}-mindmap.svg", f"05-Chapter-Architecture-Diagrams/chapter-{ch:02d}-mindmap.svg"))
        tier2_files.append((f"04-VISUAL-ASSETS/chapter-{ch:02d}-flowchart.svg", f"05-Chapter-Architecture-Diagrams/chapter-{ch:02d}-flowchart.svg"))
        tier2_files.append((f"05-WORKBOOKS/worksheet-{ch:02d}.md", f"06-Markdown-Workbooks/worksheet-{ch:02d}.md"))

    # 4. Tier 3: Complete Small Business AI Automation OS Flagship Bundle ($59)
    tier3_files = list(tier2_files) + [
        ("07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html", "08-Pro-Web-Companion-App/smallbiz-automation-os-app.html"),
        ("07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt", "08-Pro-Web-Companion-App/PRO-ACCESS-LICENSE-KEY.txt"),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", "08-Pro-Web-Companion-App/README-WEB-APP.md"),
        ("06-NOTION-TEMPLATES/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv", "09-Notion-OS-5-Database-Kit/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv"),
        ("06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv", "09-Notion-OS-5-Database-Kit/02-Automation-Workflows-and-Health-Registry.csv"),
        ("06-NOTION-TEMPLATES/03-AI-Prompt-and-SOP-Vault-62.csv", "09-Notion-OS-5-Database-Kit/03-AI-Prompt-and-SOP-Vault-62.csv"),
        ("06-NOTION-TEMPLATES/04-Weekly-Owner-KPI-Scorecard.csv", "09-Notion-OS-5-Database-Kit/04-Weekly-Owner-KPI-Scorecard.csv"),
        ("06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.csv", "09-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.csv"),
        ("06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.md", "09-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.md"),
        ("06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md", "09-Notion-OS-5-Database-Kit/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"),
        ("06-NOTION-TEMPLATES/Spreadsheets/the-smallbiz-ai-automation-os-financial-and-roi-matrix.xlsx", "10-Excel-8Tab-Command-Center/the-smallbiz-ai-automation-os-financial-and-roi-matrix.xlsx"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", "10-Excel-8Tab-Command-Center/sheet1-automation-roi-and-leak-calculator.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet2-5day-time-and-task-audit.csv", "10-Excel-8Tab-Command-Center/sheet2-5day-time-and-task-audit.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet3-speed-to-lead-latency-and-recovery-model.csv", "10-Excel-8Tab-Command-Center/sheet3-speed-to-lead-latency-and-recovery-model.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet4-3option-quote-and-14day-nurture-roi.csv", "10-Excel-8Tab-Command-Center/sheet4-3option-quote-and-14day-nurture-roi.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet5-support-deflection-and-90day-winback.csv", "10-Excel-8Tab-Command-Center/sheet5-support-deflection-and-90day-winback.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet6-invoicing-ar-chasers-and-dso-cashflow.csv", "10-Excel-8Tab-Command-Center/sheet6-invoicing-ar-chasers-and-dso-cashflow.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet7-friday-16week-owner-kpi-scorecard.csv", "10-Excel-8Tab-Command-Center/sheet7-friday-16week-owner-kpi-scorecard.csv"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet8-90day-rollout-and-tool-stack-budget.csv", "10-Excel-8Tab-Command-Center/sheet8-90day-rollout-and-tool-stack-budget.csv"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/01-Full-Editable-Book-Manuscript.docx", "11-Editable-Word-SOP-Suite/01-Full-Editable-Book-Manuscript.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/02-Editable-10-Chapter-Action-Workbook.docx", "11-Editable-Word-SOP-Suite/02-Editable-10-Chapter-Action-Workbook.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/03-AI-Automation-Rollout-Proposal-and-Charter.docx", "11-Editable-Word-SOP-Suite/03-AI-Automation-Rollout-Proposal-and-Charter.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/04-Customer-Escalation-and-Refund-SOP-Matrix.docx", "11-Editable-Word-SOP-Suite/04-Customer-Escalation-and-Refund-SOP-Matrix.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/05-Staff-AI-Usage-and-Data-Privacy-Policy.docx", "11-Editable-Word-SOP-Suite/05-Staff-AI-Usage-and-Data-Privacy-Policy.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/06-Vendor-and-Tool-Stack-Onboarding-Checklist.docx", "11-Editable-Word-SOP-Suite/06-Vendor-and-Tool-Stack-Onboarding-Checklist.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Word-Docs/07-Weekly-Owner-Executive-Brief-Template.docx", "11-Editable-Word-SOP-Suite/07-Weekly-Owner-Executive-Brief-Template.docx"),
        ("12-EDITABLE-OFFICE-SUITE/Slide-Decks/01-Team-AI-Automation-Onboarding-and-SOP-Deck.pptx", "12-Executive-Slide-Decks/01-Team-AI-Automation-Onboarding-and-SOP-Deck.pptx"),
        ("12-EDITABLE-OFFICE-SUITE/Slide-Decks/02-Quarterly-Automation-ROI-and-KPI-Review-Deck.pptx", "12-Executive-Slide-Decks/02-Quarterly-Automation-ROI-and-KPI-Review-Deck.pptx"),
        ("12-EDITABLE-OFFICE-SUITE/Slide-Decks/03-Client-and-Partner-Operational-Excellence-Pitch-Deck.pptx", "12-Executive-Slide-Decks/03-Client-and-Partner-Operational-Excellence-Pitch-Deck.pptx"),
        ("08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html", "13-Design-Customizer-Studio/design-customizer-studio.html"),
        ("08-COVER-DESIGN/Editable-Design-Kit/README-DESIGN-KIT.md", "13-Design-Customizer-Studio/README-DESIGN-KIT.md"),
        ("14-AUTOMATION-BLUEPRINTS/01-60s-instant-lead-router-and-sms-intake.json", "14-Make-n8n-Zapier-Blueprints/01-60s-instant-lead-router-and-sms-intake.json"),
        ("14-AUTOMATION-BLUEPRINTS/02-ai-support-triage-and-amber-approval-gate.json", "14-Make-n8n-Zapier-Blueprints/02-ai-support-triage-and-amber-approval-gate.json"),
        ("14-AUTOMATION-BLUEPRINTS/03-3option-instant-quote-and-14day-followup.json", "14-Make-n8n-Zapier-Blueprints/03-3option-instant-quote-and-14day-followup.json"),
        ("14-AUTOMATION-BLUEPRINTS/04-overdue-invoice-5stage-payment-chaser.json", "14-Make-n8n-Zapier-Blueprints/04-overdue-invoice-5stage-payment-chaser.json"),
        ("14-AUTOMATION-BLUEPRINTS/05-friday-3pm-owner-kpi-executive-digest.json", "14-Make-n8n-Zapier-Blueprints/05-friday-3pm-owner-kpi-executive-digest.json"),
        ("14-AUTOMATION-BLUEPRINTS/NO-CODE-AUTOMATION-SETUP-GUIDE.md", "14-Make-n8n-Zapier-Blueprints/NO-CODE-AUTOMATION-SETUP-GUIDE.md"),
        ("08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png", "07-Covers/gumroad-tier3-flagship-os-bundle-cover.png"),
    ]

    # 5. Tier 4: Living Automation Vault Membership + Monthly Drop #01 ($12/mo | $59/yr)
    tier4_files = list(tier3_files) + [
        ("10-MARKETING/tier4-monthly-vault-drop-01.md", "15-Living-Vault-Drops/tier4-monthly-vault-drop-01.md"),
        ("10-MARKETING/index.html", "16-Commercial-Funnel-Suite/index.html"),
        ("10-MARKETING/email-funnel-and-upsell-sequence.md", "16-Commercial-Funnel-Suite/email-funnel-and-upsell-sequence.md"),
        ("10-MARKETING/marketplace-listings-and-bd-launch-runbook.md", "16-Commercial-Funnel-Suite/marketplace-listings-and-bd-launch-runbook.md"),
        ("08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png", "07-Covers/gumroad-tier4-living-vault-membership-cover.png"),
    ]

    results = {}
    results["Tier 0"] = create_bundle_zip(
        "Tier0-Free-5Day-Audit-Starter-Kit.zip",
        "Tier 0 — Free 5-Day Small Business Time & Lead-Leak Audit Starter Kit ($0)",
        tier0_files,
    )
    results["Tier 1"] = create_bundle_zip(
        "Tier1-KDP-and-D2D-Retail-Book-Pack.zip",
        "Tier 1 — Amazon KDP & Draft2Digital Retail Book Pack ($9.99 Digital / $16.99 Print)",
        tier1_files,
    )
    results["Tier 2"] = create_bundle_zip(
        "Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip",
        "Tier 2 — Interactive Workbook, Visual Shortcut Atlas & Tablet Planner Edition ($29)",
        tier2_files,
    )
    results["Tier 3"] = create_bundle_zip(
        "Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip",
        "Tier 3 — Complete Small Business AI Automation Operating System Flagship Bundle ($59)",
        tier3_files,
    )
    results["Tier 4"] = create_bundle_zip(
        "Tier4-Living-Automation-Vault-Membership-Drop01.zip",
        "Tier 4 — Living Automation Vault Membership + Monthly Drop #01 ($12/mo | $59/yr)",
        tier4_files,
    )

    for tier, info in results.items():
        print(
            f" -> {tier}: {info['zip_file']} | {info['compressed_mb']} MB compressed "
            f"({info['uncompressed_mb']} MB uncompressed across {info['file_count']} files)"
        )
    return results


def main():
    u1 = build_upgrade_1_visual_cheat_sheets()
    u2_to_6 = build_all_office_and_studio_upgrades()
    bundles = rebuild_all_5_commercial_bundles()
    print("\n=== PHASE 9 BUILD COMPLETE ===")
    return {"upgrade1": u1, **u2_to_6, "bundles": bundles}


if __name__ == "__main__":
    main()
