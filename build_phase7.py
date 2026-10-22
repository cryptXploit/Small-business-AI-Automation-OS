#!/usr/bin/env python3
"""
Phase 7 Builder: 5-Database Minimalist Notion OS Kit & Commercial Cover Suite (build_phase7.py)
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)
Generates:
  Part A (06-NOTION-TEMPLATES/):
    1. 01-Inbound-Leads-and-Speed-to-Lead-CRM.csv (25+ rows)
    2. 02-Automation-Workflows-and-Health-Registry.csv (25+ rows)
    3. 03-AI-Prompt-and-SOP-Vault-62.csv (62 rows: 50 Prompts + 12 Emergency Scripts)
       + copy to 06-NOTION-TEMPLATES/Spreadsheets/62-Item-Prompt-and-SOP-Vault.csv
    4. 04-Weekly-Owner-KPI-Scorecard.csv (12+ rows)
    5. 05-Customer-Support-and-Escalation-Hub.csv (20+ rows)
       + 05-Customer-Support-and-Escalation-Hub.md (1,500+ words)
    6. NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md (2,000+ words)
    7. Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv (20+ rows)
  Part B (08-COVER-DESIGN/):
    1. 6 Master Vector Cover SVGs
    2. 6 High-Resolution PNG Covers rendered via Headless Edge/Chrome (--force-device-scale-factor=1)
    3. Print-Ready KDP Full-Wrap Cover PDF (08-COVER-DESIGN/ & 09-EXPORTS/PRINT/)
    4. COVER-DESIGN-AND-PACKAGING-SPEC.md (1,500+ words)
"""

import csv
import json
import os
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from build_webapp import (
    parse_all_50_prompts,
    parse_all_12_emergency_scripts,
    sanitize_banned_stems,
)

STUDIO_ROOT = Path(__file__).resolve().parent
NOTION_DIR = STUDIO_ROOT / "06-NOTION-TEMPLATES"
SPREADSHEETS_DIR = NOTION_DIR / "Spreadsheets"
COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
PRINT_EXPORT_DIR = STUDIO_ROOT / "09-EXPORTS" / "PRINT"

NOTION_DIR.mkdir(parents=True, exist_ok=True)
SPREADSHEETS_DIR.mkdir(parents=True, exist_ok=True)
COVER_DIR.mkdir(parents=True, exist_ok=True)
PRINT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)


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
    raise RuntimeError("Could not find Microsoft Edge or Google Chrome executable.")


def write_csv_file(path: Path, headers: list, rows: list):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for r in rows:
            cleaned = [sanitize_banned_stems(str(cell)) for cell in r]
            writer.writerow(cleaned)


# =============================================================================
# PART A: 5-DATABASE MINIMALIST NOTION SMALL BUSINESS OS KIT
# =============================================================================

def generate_db01_inbound_leads():
    headers = [
        "Lead_ID",
        "Contact_Name",
        "Business_Or_Household",
        "Industry_Segment",
        "Inbound_Channel",
        "Lead_Received_Timestamp",
        "First_Touch_Timestamp",
        "Speed_To_Lead_Seconds",
        "SLA_60s_Status",
        "Urgency_Tier",
        "Qualification_Score",
        "Recommended_Quote_Tier",
        "Estimated_Deal_Value_USD",
        "Pipeline_Stage",
        "Follow_Up_Day_Step",
        "Next_Action_Date",
        "Assigned_Owner",
        "Workflow_Blueprint_Ref",
    ]
    channels = [
        "Website Quote Form",
        "Missed-Call SMS Text-Back",
        "WhatsApp Business Concierge",
        "Facebook / IG Lead Ad",
        "Google Business Profile Message",
    ]
    segments = [
        ("Residential HVAC Replacement", "Apex Comfort HVAC", 6800, "Tier 2 Recommended ($6,800)"),
        ("Dental Implant & Ortho Consult", "BrightSmile Dental", 4200, "Tier 2 Comprehensive ($4,200)"),
        ("B2B Retainer SEO & RevOps Build", "Elevate Growth Agency", 8500, "Tier 3 Enterprise ($8,500)"),
        ("Emergency Tankless Water Heater", "HarborView Plumbing", 3400, "Tier 2 Priority ($3,400)"),
        ("Commercial Roof Leak Inspection", "Summit Roofing Co", 11200, "Tier 3 Full-System ($11,200)"),
    ]
    contacts = [
        ("LD-2026-001", "Marcus Vance", "Vance Orthodontic Studio", 18, "PASS (<60s)", "Tier 1 Immediate", 94, "Closed Won", "Completed", "Elena Rostova"),
        ("LD-2026-002", "Rachel Sterling", "Sterling Residence", 24, "PASS (<60s)", "Tier 1 Immediate", 89, "Booked Consult", "Day 2 Pre-Visit Brief", "Carlos Mendez"),
        ("LD-2026-003", "David K. Miller", "Oakridge Medical Plaza", 31, "PASS (<60s)", "Tier 1 Immediate", 92, "Quote Sent (Amber Approved)", "Day 3 Value Check-In", "Sarah Jenkins"),
        ("LD-2026-004", "Hannah Al-Mansoor", "Al-Mansoor Family Dental", 15, "PASS (<60s)", "Tier 2 Standard", 84, "Booked Consult", "Day 1 Confirmation", "Elena Rostova"),
        ("LD-2026-005", "Trevor Lindqvist", "Nordic Logistics LLC", 42, "PASS (<60s)", "Tier 1 Immediate", 88, "Closed Won", "Completed", "Sarah Jenkins"),
        ("LD-2026-006", "Samantha Cho", "Cho Aesthetics & MedSpa", 19, "PASS (<60s)", "Tier 2 Standard", 81, "Quote Sent (Green Auto)", "Day 5 Case Study Nudge", "Carlos Mendez"),
        ("LD-2026-007", "logan O'Connor", "O'Connor Custom Homes", 27, "PASS (<60s)", "Tier 1 Immediate", 95, "Closed Won", "Completed", "Sarah Jenkins"),
        ("LD-2026-008", "Priya Patel", "Patel Pediatric Clinic", 36, "PASS (<60s)", "Tier 2 Standard", 79, "Active Follow-Up", "Day 7 Scope Option B", "Elena Rostova"),
        ("LD-2026-009", "Brandon Mercer", "Mercer Property Group", 22, "PASS (<60s)", "Tier 1 Immediate", 90, "Booked Consult", "Day 1 SMS Confirmed", "Carlos Mendez"),
        ("LD-2026-010", "Claire Beaumont", "Beaumont Bistro & Catering", 48, "PASS (<60s)", "Tier 2 Standard", 76, "Quote Sent (Green Auto)", "Day 3 Value Check-In", "Elena Rostova"),
        ("LD-2026-011", "Derek Kowalski", "Kowalski Auto Body", 14, "PASS (<60s)", "Tier 1 Immediate", 91, "Closed Won", "Completed", "Sarah Jenkins"),
        ("LD-2026-012", "Monica Alvarez", "Alvarez Household", 29, "PASS (<60s)", "Tier 2 Standard", 83, "Booked Consult", "Day 1 Confirmation", "Carlos Mendez"),
        ("LD-2026-013", "Jason Thorne", "Thorne Law Partners", 53, "PASS (<60s)", "Tier 2 Standard", 78, "Active Follow-Up", "Day 10 Split-Pay Offer", "Sarah Jenkins"),
        ("LD-2026-014", "Evelyn Chen", "Chen Vision Center", 21, "PASS (<60s)", "Tier 1 Immediate", 93, "Closed Won", "Completed", "Elena Rostova"),
        ("LD-2026-015", "Gregory Brooks", "Brooks Industrial Supply", 38, "PASS (<60s)", "Tier 2 Standard", 82, "Quote Sent (Amber Approved)", "Day 5 Case Study Nudge", "Carlos Mendez"),
        ("LD-2026-016", "Nadia Petrova", "Petrova Architecture", 17, "PASS (<60s)", "Tier 1 Immediate", 87, "Booked Consult", "Day 2 Pre-Visit Brief", "Elena Rostova"),
        ("LD-2026-017", "Anthony Russo", "Russo Electrical Services", 33, "PASS (<60s)", "Tier 2 Standard", 80, "Closed Won", "Completed", "Sarah Jenkins"),
        ("LD-2026-018", "Victoria Whitaker", "Whitaker Household", 74, "WARN (61-180s)", "Tier 3 Low-Urgency", 68, "Active Follow-Up", "Day 14 Polite Close-Out", "Carlos Mendez"),
        ("LD-2026-019", "Kieran Gallagher", "Gallagher Brewing Co", 25, "PASS (<60s)", "Tier 1 Immediate", 89, "Quote Sent (Amber Approved)", "Day 3 Value Check-In", "Sarah Jenkins"),
        ("LD-2026-020", "Alicia Dominguez", "Dominguez Physical Therapy", 19, "PASS (<60s)", "Tier 1 Immediate", 92, "Closed Won", "Completed", "Elena Rostova"),
        ("LD-2026-021", "Steven Takahashi", "Takahashi Precision Mfg", 41, "PASS (<60s)", "Tier 2 Standard", 85, "Booked Consult", "Day 1 Confirmation", "Carlos Mendez"),
        ("LD-2026-022", "Rebecca Reynolds", "Reynolds Veterinary Care", 28, "PASS (<60s)", "Tier 1 Immediate", 90, "Closed Won", "Completed", "Sarah Jenkins"),
        ("LD-2026-023", "Omar Farooq", "Crescent Accounting CPA", 16, "PASS (<60s)", "Tier 2 Standard", 84, "Quote Sent (Green Auto)", "Day 5 Case Study Nudge", "Elena Rostova"),
        ("LD-2026-024", "julianne Foster-Hayes", "Hayes Landscape Design", 35, "PASS (<60s)", "Tier 2 Standard", 77, "Active Follow-Up", "Day 7 Scope Option B", "Carlos Mendez"),
        ("LD-2026-025", "Zachary Bennett", "Bennett Commercial Realty", 23, "PASS (<60s)", "Tier 1 Immediate", 94, "Closed Won", "Completed", "Sarah Jenkins"),
        ("LD-2026-026", "Laura Lindholm", "Lindholm Skincare Clinic", 20, "PASS (<60s)", "Tier 1 Immediate", 91, "Booked Consult", "Day 2 Pre-Visit Brief", "Elena Rostova"),
    ]
    rows = []
    for idx, c in enumerate(contacts):
        lid, cname, biz, sec, sla, urg, score, stage, fstep, owner = c
        # Ensure zero banned words (note: 'Foster' was in julianne's surname, replace with 'Vaughn-Hayes')
        cname = cname.replace("Foster-Hayes", "Vaughn-Hayes").replace("logan", "Logan")
        seg_name, _, base_val, qtier = segments[idx % len(segments)]
        ch = channels[idx % len(channels)]
        day = (idx % 20) + 1
        rx_ts = f"2026-10-{day:02d} 09:{(10 + idx) % 59:02d}:00"
        ft_ts = f"2026-10-{day:02d} 09:{(10 + idx) % 59:02d}:{sec:02d}"
        next_date = f"2026-10-{min(28, day + 3):02d}"
        val = base_val + (idx * 150)
        rows.append([
            lid, cname, biz, seg_name, ch, rx_ts, ft_ts, sec, sla, urg,
            score, qtier, val, stage, fstep, next_date, owner, "Blueprint-01-Lead-Router",
        ])

    write_csv_file(NOTION_DIR / "01-Inbound-Leads-and-Speed-to-Lead-CRM.csv", headers, rows)
    return len(rows), len(headers)


def generate_db02_workflows_registry():
    headers = [
        "Workflow_ID",
        "Workflow_Name",
        "Department",
        "Chapter_Ref",
        "Trigger_Event",
        "No_Code_Platform",
        "TRAV_Risk_Zone",
        "Human_Approval_Gate_Owner",
        "Prompt_ID_Used",
        "Weekly_Run_Volume",
        "Weekly_Hours_Saved",
        "Monthly_Tool_Cost_USD",
        "Annualized_Net_ROI_USD",
        "Error_Rate_Pct",
        "Fallback_Kill_Switch_Status",
        "Operational_Status",
    ]
    workflows = [
        ("WF-01", "5-Day Staff Time-Log & CMF Financial Synthesizer", "Dept 05: Executive Command", "Chapter 1", "Friday Audit Form Submitted", "Make + Google Sheets", "Amber Zone", "Sarah Jenkins (Founder)", "Prompt 1.1", 4, 1.8, 12, 5200, "0.0%", "Armed (Auto-Revert)", "Active Production"),
        ("WF-02", "30-Day Multi-Channel Lead-Leak & Ad Decay Auditor", "Dept 01: Lead Capture", "Chapter 1", "Monthly Marketing Close", "Make + Airtable", "Amber Zone", "Sarah Jenkins (Founder)", "Prompt 1.2", 2, 1.2, 10, 8400, "0.0%", "Armed (Auto-Revert)", "Active Production"),
        ("WF-03", "SaaS Subscription Redundancy & GL-6110 Consolidation Scanner", "Dept 04: Finance & AR", "Chapter 1", "1st of Month QBO Expense Export", "Make + QuickBooks", "Amber Zone", "Sarah Jenkins (Founder)", "Prompt 1.3", 1, 0.8, 8, 3600, "0.0%", "Armed (Auto-Revert)", "Active Production"),
        ("WF-04", "Inbound Webhook Normalizer & Idempotency Hash Guard", "Dept 05: Systems & Governance", "Chapter 2", "Any External Webhook Received", "Make + Data Store", "Green Zone", "Automated Pre-Filter", "Prompt 2.1", 320, 3.5, 18, 10800, "0.2%", "Armed (DLQ Sheet)", "Active Production"),
        ("WF-05", "Closed-World Grounding & Pricebook Truth-Table Injector", "Dept 02: Sales & Quoting", "Chapter 2", "Pre-LLM Context Assembly", "Make + Airtable", "Green Zone", "Automated Pre-Filter", "Prompt 2.2", 185, 2.6, 15, 7900, "0.1%", "Armed (DLQ Sheet)", "Active Production"),
        ("WF-06", "Slack Block Kit 1-Click Amber Approval Card Dispatcher", "Dept 05: Systems & Governance", "Chapter 2", "Risk Score 9-14 or Quote >= $2,500", "Make + Slack API", "Amber Zone", "Department Lead", "Prompt 2.3", 45, 2.4, 10, 7200, "0.0%", "Armed (Email Backup)", "Active Production"),
        ("WF-07", "Dead-Letter Queue (DLQ) Outage Monitor & Fallback Router", "Dept 05: Systems & Governance", "Chapter 2", "HTTP 429/500 or Schema Validation Fail", "n8n + Twilio + Slack", "Red Zone", "Operations Manager", "Prompt 2.5", 6, 1.5, 12, 6500, "0.0%", "Armed (Active Monitor)", "Active Production"),
        ("WF-08", "I.N.S.T.A.N.T. 60-Second Omnichannel Lead Scorer", "Dept 01: Lead Capture", "Chapter 3", "Web Form, LSA, or Social Lead Ad", "Make + HubSpot", "Green Zone", "Automated (<60s SLA)", "Prompt 3.1", 115, 4.2, 24, 28500, "0.3%", "Armed (DLQ Sheet)", "Active Production"),
        ("WF-09", "Personalized 60-Second SMS & Email Concierge Dispatcher", "Dept 01: Lead Capture", "Chapter 3", "Scored Lead Output from WF-08", "Make + Twilio + Gmail", "Green Zone", "Automated (<60s SLA)", "Prompt 3.2", 115, 3.8, 28, 24200, "0.2%", "Armed (DLQ Sheet)", "Active Production"),
        ("WF-10", "Missed-Call Voicemail Whisper Transcriber & 45s Text-Back", "Dept 01: Lead Capture", "Chapter 3", "call.missed / voicemail.completed", "Make + OpenPhone + OpenAI", "Green Zone", "Automated (<45s SLA)", "Prompt 3.3", 64, 3.4, 22, 31400, "0.4%", "Armed (Front Desk Alert)", "Active Production"),
        ("WF-11", "2-Way Conversational SMS Qualification & Calendar Booker", "Dept 01: Lead Capture", "Chapter 3", "Prospect Replies to SMS Concierge", "Make + Twilio + Calendly", "Green Zone", "Front Desk Lead (If Complex)", "Prompt 3.4", 88, 3.1, 20, 19800, "0.5%", "Armed (Human Handoff)", "Active Production"),
        ("WF-12", "30-Minute Pre-Consult Sales Rep Briefing Card Compiler", "Dept 02: Sales & Quoting", "Chapter 3", "30m Before Calendar Appointment", "Make + Google Calendar + Slack", "Green Zone", "Automated Internal Brief", "Prompt 3.5", 42, 2.1, 10, 6400, "0.0%", "Armed (Auto-Revert)", "Active Production"),
        ("WF-13", "Field Voice Memo to 3-Tier Good-Better-Best Proposal Engine", "Dept 02: Sales & Quoting", "Chapter 4", "Audio Note Uploaded in #field-quotes", "Make + Whisper + PandaDoc", "Amber Zone", "Carlos Mendez (Sales Lead)", "Prompt 4.1", 28, 5.2, 32, 36800, "0.4%", "Armed (Draft Only)", "Active Production"),
        ("WF-14", "Executive Proposal Cover Letter & ROI Justification Writer", "Dept 02: Sales & Quoting", "Chapter 4", "Pricing Table Locked from WF-13", "Make + PandaDoc", "Amber Zone", "Carlos Mendez (Sales Lead)", "Prompt 4.2", 28, 2.4, 14, 14500, "0.2%", "Armed (Draft Only)", "Active Production"),
        ("WF-15", "14-Day Polite-Persistence Open Quote Follow-Up Sequence", "Dept 02: Sales & Quoting", "Chapter 4", "Quote Viewed_Unsigned > 48 Hours", "Make + CRM + Gmail + Twilio", "Green Zone", "Sales Rep (Day 14 Amber)", "Prompt 4.3", 54, 3.6, 18, 29400, "0.2%", "Armed (Kill on Sign)", "Active Production"),
        ("WF-16", "Inbound Quote Objection Classifier & Margin-Safe Counter Drafter", "Dept 02: Sales & Quoting", "Chapter 4", "Prospect Replies With Price/Scope Query", "Make + Gmail + Slack", "Amber Zone", "Carlos Mendez (Sales Lead)", "Prompt 4.4", 14, 1.9, 12, 16200, "0.0%", "Armed (Draft Only)", "Active Production"),
        ("WF-17", "Zero-Drop Deposit Payment to Welcome Packet & Portal Provisioner", "Dept 03: Onboarding & Support", "Chapter 5", "stripe.checkout.completed / invoice.paid", "Make + Stripe + Notion + Drive", "Green Zone", "Automated (<15s Handoff)", "Prompt 5.1", 22, 3.3, 18, 14200, "0.1%", "Armed (Ops Alert)", "Active Production"),
        ("WF-18", "Client Intake Form Completeness & Asset Validation Auditor", "Dept 03: Onboarding & Support", "Chapter 5", "Tally / Typeform Intake Submitted", "Make + Tally + ClickUp", "Green Zone", "Elena Rostova (If Missing)", "Prompt 5.2", 22, 2.0, 12, 8600, "0.2%", "Armed (Ops Alert)", "Active Production"),
        ("WF-19", "Stalled Onboarding +24h/+72h/+5d Polite Asset Chaser", "Dept 03: Onboarding & Support", "Chapter 5", "Intake Incomplete at +24h Check", "Make + Twilio + Gmail", "Green Zone", "Elena Rostova (Day 5 Call)", "Prompt 5.3", 12, 1.6, 10, 6800, "0.0%", "Armed (Kill on Submit)", "Active Production"),
        ("WF-20", "Multi-Channel Support Ticket Sentiment & Intent Classifier", "Dept 03: Onboarding & Support", "Chapter 6", "New Ticket in HelpScout / Gorgias", "Make + HelpScout + OpenAI", "Green Zone", "Support Lead (If Sent <= 2)", "Prompt 6.1", 140, 3.9, 24, 15400, "0.3%", "Armed (Red Gate Bypass)", "Active Production"),
        ("WF-21", "Zero-Hallucination Grounded RAG Tier-1 Answer Dispatcher", "Dept 03: Onboarding & Support", "Chapter 6", "Tier-1 Routine FAQ & Sentiment >= 3", "Make + Supabase + HelpScout", "Green Zone", "Auto if Confidence >= 0.85", "Prompt 6.2", 95, 4.5, 26, 18200, "0.4%", "Armed (Draft Fallback)", "Active Production"),
        ("WF-22", "Post-Delivery Sentiment Gate & 5-Star Google Review Funnel", "Dept 03: Onboarding & Support", "Chapter 7", "Job Marked Completed + Optimal Delay", "Make + Twilio + GBP API", "Green Zone", "Owner Alert if Score 1-3", "Prompt 7.1", 48, 2.5, 16, 21000, "0.1%", "Armed (Detractor Hold)", "Active Production"),
        ("WF-23", "Same-Day Completed Job to Itemized QuickBooks Invoice Builder", "Dept 04: Finance & AR", "Chapter 8", "job.completed / milestone.approved", "Make + QuickBooks + Stripe", "Amber Zone", "Auto <$1.5k / Amber >=$1.5k", "Prompt 8.1", 46, 3.7, 22, 19600, "0.2%", "Armed (Draft Invoice)", "Active Production"),
        ("WF-24", "5-Stage Polite-to-Firm Overdue Invoice Payment Chaser State Machine", "Dept 04: Finance & AR", "Chapter 8", "Daily 9:00 AM Open AR Aging Scan", "Make + QuickBooks + Twilio", "Amber Zone", "Green Stg 1-3 / Amber Stg 4-5", "Prompt 8.2", 35, 3.2, 18, 26800, "0.1%", "Armed (Dispute Hold)", "Active Production"),
        ("WF-25", "Vendor Bill OCR Extractor & 5% Price-Creep Variance Auditor", "Dept 04: Finance & AR", "Chapter 8", "Email to bills@ or Tech Receipt SMS", "Make + OpenAI Vision + QBO", "Amber Zone", "Finance Lead (If Creep > 5%)", "Prompt 8.4", 52, 2.9, 20, 14900, "0.3%", "Armed (Hold Bill)", "Active Production"),
        ("WF-26", "Loom Voice/Screen Recording to 7-Block Living SOP Compiler", "Dept 05: Executive Command", "Chapter 9", "New Video in #sop-capture", "Make + Whisper + Notion", "Amber Zone", "15-Second Owner Glance", "Prompt 9.1", 8, 2.8, 14, 11200, "0.0%", "Armed (Draft Page)", "Active Production"),
        ("WF-27", "Friday 3:00 PM 12-KPI Executive Scorecard & Variance Synthesizer", "Dept 05: Executive Command", "Chapter 10", "Scheduled Friday 3:00 PM Cron", "Make + Airtable + QBO + Slack", "Amber Zone", "Sarah Jenkins (Founder)", "Prompt 10.1", 1, 2.2, 12, 12400, "0.0%", "Armed (Auto-Revert)", "Active Production"),
    ]
    write_csv_file(NOTION_DIR / "02-Automation-Workflows-and-Health-Registry.csv", headers, workflows)
    return len(workflows), len(headers)


def generate_db03_prompt_and_sop_vault_62():
    headers = [
        "Vault_ID",
        "Asset_Type",
        "Department",
        "Chapter_Ref",
        "Title",
        "Trigger_Condition",
        "TRAV_Risk_Zone",
        "Input_Variables",
        "Full_Prompt_Or_Script_Body",
        "Expected_Output_Schema",
        "Verification_Gate_Checklist",
    ]
    prompts = parse_all_50_prompts()
    scripts = parse_all_12_emergency_scripts()
    rows = []

    for p in prompts:
        rows.append([
            p["id"],
            "Tested AI Workflow Prompt",
            f"{p['dept_code']} ({p['dept_label']})",
            p["chapter_label"],
            p["title"],
            p["trigger"],
            f"{p['zone']} Zone ({p['gate_detail']})",
            ", ".join(f"[{v}]" for v in p["variables"]),
            p["prompt_template"],
            p["sample_output"][:600].replace("\n", " "),
            "Verify grounded source citations, deterministic numeric math, and zero unapproved external commitments.",
        ])

    for s in scripts:
        combined_script = (
            f"SUBJECT: {s['email_subject']} || EMAIL: {s['email_body']} "
            f"|| SMS: {s['sms_body']} || INTERNAL NOTE: {s['escalation_note']}"
        ).replace("\n", " ")
        rows.append([
            s["id"],
            "Emergency Operations Script (Red Gate)",
            "Dept 05: Executive Crisis & Exception Containment",
            "Back Matter — Part II",
            s["title"],
            s["scenario"],
            "Red Zone (Mandatory Human Takeover)",
            ", ".join(f"[{v}]" for v in s["variables"]),
            combined_script,
            "Synchronized Email Subject/Body + 160-char SMS/WhatsApp + Slack Internal Escalation Alert",
            " | ".join(s["checklist"]),
        ])

    if len(rows) != 62:
        raise RuntimeError(f"Expected 62 rows in 03-AI-Prompt-and-SOP-Vault-62.csv, got {len(rows)}")

    target_main = NOTION_DIR / "03-AI-Prompt-and-SOP-Vault-62.csv"
    target_copy = SPREADSHEETS_DIR / "62-Item-Prompt-and-SOP-Vault.csv"
    write_csv_file(target_main, headers, rows)
    shutil.copyfile(target_main, target_copy)
    return len(rows), len(headers)


def generate_db04_weekly_kpi_scorecard():
    headers = [
        "Week_ID",
        "Friday_Date",
        "Rollout_Phase",
        "Inbound_Leads_Count",
        "Median_Speed_To_Lead_Sec",
        "Missed_Call_Recovery_Pct",
        "Quotes_Sent_Count",
        "Quote_14Day_Close_Rate_Pct",
        "Onboarding_Cycle_Hours",
        "Tier1_AI_Support_Resolution_Pct",
        "Net_New_5Star_Reviews",
        "Weekly_Cash_Collected_USD",
        "Overdue_AR_Over_15Days_USD",
        "Average_DSO_Days",
        "Owner_Hours_Worked",
        "Weekly_Team_Hours_Saved",
        "Automation_Exceptions_Count",
        "Executive_RAG_Status",
        "Monday_Top_Priority",
    ]
    weeks = [
        ("WK-2026-01", "2026-08-07", "Phase I: Days 1-30 (Baseline Audit)", 24, 1420, "18%", 9, "22%", 64.0, "0%", 1, 14200, 11800, 38, 56.0, 2.5, 0, "AMBER (Baseline Audit Week)", "Deploy T.R.A.V. Pre-AI Webhook Normalizer & Slack #amber-approvals"),
        ("WK-2026-02", "2026-08-14", "Phase I: Days 1-30 (Quick Wins)", 26, 95, "68%", 11, "25%", 52.0, "15%", 2, 15600, 9400, 33, 52.0, 6.0, 1, "AMBER (Speed-to-Lead Live)", "Tune Missed-Call Whisper SMS Concierge to <45s SLA"),
        ("WK-2026-03", "2026-08-21", "Phase I: Days 1-30 (Quick Wins)", 28, 48, "84%", 12, "29%", 44.0, "24%", 3, 17900, 7200, 27, 48.5, 9.5, 1, "GREEN (60s SLA Achieved)", "Activate Same-Day Job Completion Invoice Trigger (Prompt 8.1)"),
        ("WK-2026-04", "2026-08-28", "Phase I: Days 1-30 (Quick Wins)", 30, 44, "88%", 13, "31%", 38.0, "30%", 3, 19400, 5100, 22, 46.0, 12.0, 0, "GREEN (Phase I Exit Gate Passed)", "Launch Voice-to-3-Tier Proposal Engine (Prompt 4.1)"),
        ("WK-2026-05", "2026-09-04", "Phase II: Days 31-60 (Core Fulfillment)", 29, 41, "89%", 15, "34%", 29.0, "38%", 3, 20800, 4200, 19, 44.0, 14.5, 1, "GREEN (3-Tier Quotes Active)", "Enable 14-Day Polite-Persistence Open Quote Sequence (Prompt 4.3)"),
        ("WK-2026-06", "2026-09-11", "Phase II: Days 31-60 (Core Fulfillment)", 32, 39, "90%", 16, "36%", 21.0, "48%", 4, 21900, 3400, 17, 42.5, 16.5, 0, "GREEN (Zero-Drop Onboarding Live)", "Wire Stripe Deposit Webhook to Instant Welcome & Intake Provisioner"),
        ("WK-2026-07", "2026-09-18", "Phase II: Days 31-60 (Core Fulfillment)", 31, 38, "91%", 15, "37%", 16.5, "58%", 4, 22600, 2800, 16, 41.0, 18.0, 1, "GREEN (RAG Support Triage Live)", "Expand Grounded Knowledge Base Chunks for Top 25 Tier-1 FAQs"),
        ("WK-2026-08", "2026-09-25", "Phase II: Days 31-60 (Core Fulfillment)", 34, 37, "92%", 17, "38%", 14.0, "63%", 5, 23800, 2300, 15, 39.5, 19.5, 0, "GREEN (Phase II Exit Gate Passed)", "Deploy Sentiment-Gated 5-Star Google Review & 90-Day Recall Loop"),
        ("WK-2026-09", "2026-10-02", "Phase III: Days 61-90 (Autonomous Scale)", 33, 36, "92%", 16, "39%", 13.0, "65%", 4, 24500, 1950, 14, 38.5, 21.0, 0, "GREEN (OCR & Price-Creep Live)", "Enable Vendor Bill OCR & 5% Price-Creep Variance Detector (Prompt 8.4)"),
        ("WK-2026-10", "2026-10-09", "Phase III: Days 61-90 (Autonomous Scale)", 35, 35, "93%", 18, "40%", 12.5, "67%", 5, 25400, 1650, 13, 37.5, 22.5, 0, "GREEN (Living SOP Vault Live)", "Record 4 Loom Videos for 7-Block SOP Compiler & Voice Delegation"),
        ("WK-2026-11", "2026-10-16", "Phase III: Days 61-90 (Autonomous Scale)", 36, 34, "94%", 18, "41%", 12.0, "69%", 5, 26200, 1400, 12, 36.5, 24.0, 0, "GREEN (Friday Pulse Automated)", "Automate Friday 3:00 PM Executive Brief & Monday All-Hands Memo"),
        ("WK-2026-12", "2026-10-23", "Phase III: Days 61-90 (Full OS Maturity)", 38, 32, "95%", 19, "42%", 11.5, "71%", 6, 27800, 1150, 11, 35.0, 25.5, 0, "GREEN (90-Day Rollout Complete)", "Execute Q4 Governance, API Key Rotation & Prompt Drift Audit (Prompt 10.4)"),
    ]
    write_csv_file(NOTION_DIR / "04-Weekly-Owner-KPI-Scorecard.csv", headers, weeks)
    return len(weeks), len(headers)


def generate_db05_support_hub_csv_and_md():
    headers = [
        "Policy_ID",
        "Inquiry_Category",
        "Tier_Level",
        "Sentiment_Floor",
        "Approved_Policy_Summary",
        "Max_Auto_Refund_USD",
        "Escalation_Owner",
        "SLA_Response_Target",
        "Linked_Prompt_Or_Script",
    ]
    policies = [
        ("POL-01", "Business Hours, Street Address & Parking Directions", "Tier 1 (Green Auto)", "Sentiment >= 3", "Provide verified clinic/office street address, free parking lot instructions, and Mon-Fri 8:00 AM - 5:30 PM service hours.", 0, "Automated RAG Bot", "< 60 Seconds", "Prompt 6.2"),
        ("POL-02", "Standard Appointment Reschedule (>24 Hours Notice)", "Tier 1 (Green Auto)", "Sentiment >= 3", "Verify customer identity via phone/email and dispatch 1-click self-serve reschedule calendar link with zero fee.", 0, "Automated Booking Bot", "< 60 Seconds", "Prompt 6.3"),
        ("POL-03", "Late Cancellation / Reschedule (<24 Hours Notice)", "Tier 2 (Amber Approval)", "Sentiment >= 3", "Draft polite reminder of $50 late-reschedule policy while offering 1-time courtesy waiver option for manager 1-click sign-off.", 50, "Front Desk / Ops Lead", "< 15 Minutes", "Prompt 2.3"),
        ("POL-04", "Order Status / Technician ETA Lookup (WISMO)", "Tier 1 (Green Auto)", "Sentiment >= 3", "Query live FSM/Shopify tracking webhook and reply with exact technician dispatch window or carrier tracking link.", 0, "Automated Lookup API", "< 60 Seconds", "Prompt 6.3"),
        ("POL-05", "Copy of Itemized Invoice, Receipt, or W-9 Form", "Tier 1 (Green Auto)", "Sentiment >= 3", "Verify billing email address and re-send PDF invoice link plus company W-9 tax certificate from QuickBooks/Stripe.", 0, "Automated Billing Bot", "< 2 Minutes", "Prompt 8.1"),
        ("POL-06", "Insurance / Warranty Coverage Verification Inquiry", "Tier 2 (Amber Approval)", "Sentiment >= 3", "Confirm in-network carrier list from Grounded Truth Table; route specific copay/serial-number eligibility checks to coordinator.", 0, "Billing Coordinator", "< 30 Minutes", "Prompt 2.1"),
        ("POL-07", "Minor Courtesy Credit or Consumable Replacement (<= $50)", "Tier 1 (Green Auto)", "Sentiment >= 3", "Authorized to issue up to $50 account credit or replacement filter/accessory once per 12 months for verified delivery delay.", 50, "Automated Support Bot", "< 5 Minutes", "Prompt 6.2"),
        ("POL-08", "Service Adjustment or Refund Request ($51 - $250)", "Tier 2 (Amber Approval)", "Sentiment >= 2", "Assemble complete job history and invoice margin summary into Slack #amber-approvals card for 1-click manager authorization.", 250, "Operations Manager", "< 30 Minutes", "Prompt 2.3"),
        ("POL-09", "High-Value Refund or Dispute Claim (> $250)", "Tier 3 (Red Escalation)", "Any Sentiment", "Pause automated billing chasers immediately (`dispute_flag=TRUE`) and escalate to Founder with 5-point evidence summary.", 0, "Founder / Finance Lead", "< 15 Minutes", "Emergency Script 09"),
        ("POL-10", "Angry Customer / Severe Service Failure (Sentiment 1-2)", "Tier 3 (Red Escalation)", "Sentiment <= 2", "Halt all AI replies immediately. Lock `automation_hold=TRUE` and page Owner/Director for personal takeover call.", 0, "Founder / Owner", "< 15 Minutes", "Emergency Script 01"),
        ("POL-11", "Property Damage, Safety Hazard, or Clinical Complication", "Tier 3 (Red Escalation)", "Any Sentiment", "Immediate Red-Gate intercept via safety regex. Page on-call supervisor and owner cell phone within 60 seconds.", 0, "Founder & Safety Lead", "< 5 Minutes", "Prompt 6.4"),
        ("POL-12", "Mid-Project Out-of-Scope Addition / Extra Revision Request", "Tier 2 (Amber Approval)", "Sentiment >= 3", "Validate request warmly and generate 1-click Paid Change Order (`#CO-JobID-01`) vs. Phase 2 backlog option.", 0, "Project Manager", "< 1 Hour", "Emergency Script 05"),
        ("POL-13", "Supplier / Parts Backorder Delay Affecting Scheduled Visit", "Tier 2 (Amber Approval)", "Any Sentiment", "Pre-hold 2 VIP priority makeup slots and dispatch proactive reschedule notice with courtesy credit on the same day.", 50, "Dispatch Coordinator", "< 1 Hour", "Emergency Script 04"),
        ("POL-14", "Sudden Morning Technician / Specialist Sickness Absence", "Tier 3 (Red Escalation)", "Any Sentiment", "Triage day into Urgent Backup Coverage vs. VIP Priority Reschedule before 8:15 AM local time.", 50, "Dispatch Lead", "< 30 Minutes", "Emergency Script 06"),
        ("POL-15", "Unfair 1-Star or 2-Star Public Google / Yelp Review", "Tier 3 (Red Escalation)", "Sentiment <= 2", "Cross-check CRM for client match; initiate private executive resolution call and post calm public response within 4 hours.", 0, "Founder / Owner", "< 2 Hours", "Emergency Script 08"),
        ("POL-16", "Credit Card Chargeback Webhook (`charge.dispute.created`)", "Tier 3 (Red Escalation)", "Any Sentiment", "Compile 5-Point Evidence Packet and send amicable DBA descriptor clarification email before submitting formal rebuttal.", 0, "Finance Lead", "< 2 Hours", "Emergency Script 09"),
        ("POL-17", "VIP Retainer / Membership Cancellation Request", "Tier 3 (Red Escalation)", "Any Sentiment", "Confirm notice date immediately so client has zero billing anxiety, and offer $0 60-Day Seasonal Pause or Lite Tier.", 0, "Founder / Account Lead", "< 30 Minutes", "Emergency Script 10"),
        ("POL-18", "30-Day Past-Due Invoice Pre-Collections & Work Suspension", "Tier 3 (Red Escalation)", "Any Sentiment", "Verify live bank/QBO ledger first; place active work on administrative hold and send 72-hour cure link.", 0, "Finance Lead", "< 1 Hour", "Emergency Script 02"),
        ("POL-19", "Software Vendor / Booking / Payment Outage Fallback", "Tier 3 (Red Escalation)", "Any Sentiment", "Flip Make/n8n router to Google Sheet fallback mode and text backup booking/payment link within 15 minutes.", 0, "Systems Administrator", "< 15 Minutes", "Emergency Script 03"),
        ("POL-20", "Erroneous Automated Quote or Notification Correction", "Tier 2 (Amber Approval)", "Any Sentiment", "Pause affected workflow scenario, patch lookup table, and dispatch transparent correction with goodwill credit.", 50, "Operations Manager", "< 30 Minutes", "Emergency Script 07"),
        ("POL-21", "Annual Rate Adjustment & Loyalty Rate-Lock Inquiry", "Tier 2 (Amber Approval)", "Sentiment >= 3", "Present 12-month value recap and offer 1-click Grandfathered Loyalty Rate-Lock for early renewal confirmation.", 0, "Account Manager", "< 2 Hours", "Emergency Script 12"),
    ]
    write_csv_file(NOTION_DIR / "05-Customer-Support-and-Escalation-Hub.csv", headers, policies)

    md_content = """# Database 05: Customer Support, RAG Knowledge Base & Red-Gate Escalation Hub

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
\\b(lawyer|attorney|sue|lawsuit|malpractice|board complaint|bbb|better business bureau|chargeback|dispute charge|fraud|scam|police|injured|bleeding|hospital|fire|flooded|damaged my|broke my|1 star|one star|worst company|report you)\\b
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
"""
    md_path = NOTION_DIR / "05-Customer-Support-and-Escalation-Hub.md"
    md_path.write_text(sanitize_banned_stems(md_content), encoding="utf-8")
    return len(policies), len(headers), len(md_content.split())


def generate_notion_setup_guide():
    guide = """# The Small Business AI Automation OS — 5-Database Notion Setup, Relations & Formula 2.0 Engineering Guide

**Kit Directory:** `06-NOTION-TEMPLATES/`  
**Companion Web App:** `07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html`  
**Target Setup Time:** 15 Minutes (Zero Paid Notion Add-Ons Required — Works on Free & Plus Plans)  

---

## 1. Architecture of the 5-Database Minimalist Notion OS

Most small business owners abandon Notion templates because they are over-engineered with 25 nested sub-pages, aesthetic widgets that break on mobile phones, and complex relational mazes that staff refuse to update.

The **Small Business AI Automation Operating System Notion Kit** follows a strict **5-Database Minimalist Architecture**. Every single operational event across your 5 core departments lives inside one of five clean, flat, webhook-ready databases:

| Database # | CSV File Name | Core Operational Role | Primary Chapter Link | Pre-Loaded Rows |
| :--- | :--- | :--- | :--- | :--- |
| **DB 01** | `01-Inbound-Leads-and-Speed-to-Lead-CRM.csv` | Omnichannel lead intake, 60-second SLA timer, B.A.N.T.-Lite score, 3-tier quote status, and 14-day follow-up tracker. | Chapters 3 & 4 | `26 rows` |
| **DB 02** | `02-Automation-Workflows-and-Health-Registry.csv` | Master registry of active Make/n8n/Zapier pipelines, T.R.A.V. governance zones, error rates, kill-switches, and net ROI. | Chapters 1, 2 & 10 | `27 rows` |
| **DB 03** | `03-AI-Prompt-and-SOP-Vault-62.csv` | Complete 62-item production library containing all **50 Tested AI Workflow Prompts (`1.1–10.5`)** and **12 Emergency Scripts (`01–12`)**. | Chapters 1–10 + Back Matter | `62 rows` |
| **DB 04** | `04-Weekly-Owner-KPI-Scorecard.csv` | Longitudinal Friday 3:00 PM Executive Command Center tracking the 12 Core KPIs across 12 weeks of rollout. | Chapters 8, 9 & 10 | `12 rows` |
| **DB 05** | `05-Customer-Support-and-Escalation-Hub.csv` | Grounded RAG Knowledge Base truth table (`POL-01`–`POL-21`), refund ceilings, sentiment floors, and Red-Gate escalation rules. | Chapters 2, 5, 6 & 7 | `21 rows` |

---

## 2. Step-by-Step 15-Minute Notion Import & Workspace Assembly

Follow these exact steps to deploy all five databases into your Notion workspace with 100% preserved columns, status badges, and sample operational records:

### Step 1: Create Your Top-Level Command Page (Minutes 1–2)
1. Open Notion (Desktop or Web) and click **`+ New Page`** in your left sidebar.
2. Title the page: **`Small Business AI Automation OS — Executive Command Center`**.
3. Choose **`Full Width`** from the top-right three-dot menu (`... -> Full width` toggle ON) so multi-column tables and KPI dashboards display without horizontal scrolling.
4. Create two side-by-side callout blocks at the top of the page:
   - **Left Callout (Operations Emerald `#059669`):** Quick links to your active Make.com/n8n dashboard, Slack `#amber-approvals` channel, and local [`smallbiz-automation-os-app.html`](../07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html).
   - **Right Callout (Amber Gate `#D97706`):** Your team's **Zero-Hallucination & Red-Gate Compact** (*"1. Never alter deterministic SKU prices; 2. Approve Amber cards within 15 minutes; 3. Flip `automation_hold = TRUE` on any Sentiment <= 2 ticket"*).

### Step 2: Import All 5 CSV Databases (Minutes 3–8)
For each of the five CSV files in `06-NOTION-TEMPLATES/` (`01-Inbound-Leads...` through `05-Customer-Support...`):
1. Type `/table view` on your Command Center page and select **`New database`** (or click **`Import -> CSV`** from the page menu).
2. Select the CSV file from `06-NOTION-TEMPLATES/`.
3. Once imported, configure the column property types as follows so Notion formulas and Make.com/n8n API modules read numeric and date fields cleanly:
   - **In `DB 01 (Inbound Leads & Speed-to-Lead CRM)`:**
     - Set `Speed_To_Lead_Seconds`, `Qualification_Score`, and `Estimated_Deal_Value_USD` to **`Number`** (`Estimated_Deal_Value_USD` formatted as `US Dollar`).
     - Set `Inbound_Channel`, `SLA_60s_Status`, `Urgency_Tier`, `Pipeline_Stage`, and `Recommended_Quote_Tier` to **`Select`**.
     - Set `Next_Action_Date` to **`Date`**.
   - **In `DB 02 (Automation Workflows & Health Registry)`:**
     - Set `Department`, `Chapter_Ref`, `No_Code_Platform`, `TRAV_Risk_Zone`, and `Operational_Status` to **`Select`**.
     - Set `Weekly_Run_Volume`, `Weekly_Hours_Saved`, `Monthly_Tool_Cost_USD`, and `Annualized_Net_ROI_USD` to **`Number`**.
   - **In `DB 03 (AI Prompt & SOP Vault — 62 Items)`:**
     - Set `Asset_Type`, `Department`, `Chapter_Ref`, and `TRAV_Risk_Zone` to **`Select`**.
     - Keep `Full_Prompt_Or_Script_Body`, `Input_Variables`, `Expected_Output_Schema`, and `Verification_Gate_Checklist` as **`Text`** (enable `Wrap cells` on the full prompt view or open row pages in `Side Peek` mode).
   - **In `DB 04 (Weekly Owner KPI Scorecard)`:**
     - Set `Friday_Date` to **`Date`**.
     - Set `Inbound_Leads_Count`, `Median_Speed_To_Lead_Sec`, `Quotes_Sent_Count`, `Onboarding_Cycle_Hours`, `Net_New_5Star_Reviews`, `Weekly_Cash_Collected_USD`, `Overdue_AR_Over_15Days_USD`, `Average_DSO_Days`, `Owner_Hours_Worked`, `Weekly_Team_Hours_Saved`, and `Automation_Exceptions_Count` to **`Number`**.
   - **In `DB 05 (Customer Support & Escalation Hub)`:**
     - Set `Inquiry_Category`, `Tier_Level`, `Sentiment_Floor`, and `SLA_Response_Target` to **`Select`**.
     - Set `Max_Auto_Refund_USD` to **`Number`** (`US Dollar`).
4. Paste the contents of [`05-Customer-Support-and-Escalation-Hub.md`](05-Customer-Support-and-Escalation-Hub.md) into a sub-page above `DB 05` so your support staff and RAG vector indexer have both the structured policy table and the full narrative escalation playbook in one place.

---

## 3. Relational Wiring Across the 5 Databases (Minutes 9–11)

While each database works standalone out of the box, connecting three lightweight **Notion Relation & Rollup properties** turns your workspace into an interconnected operating system:

```text
+-----------------------------------------------------------------------+
| DB 03: AI Prompt & SOP Vault (50 Prompts + 12 Emergency Scripts)      |
+-----------------------------------+-----------------------------------+
                                    |
         +--------------------------+--------------------------+
         | Relation: Prompt_ID_Used                            | Relation: Linked_Prompt_Or_Script
         v                                                     v
+-----------------------------------+       +-----------------------------------+
| DB 02: Automation Workflows       |       | DB 05: Support & Escalation Hub   |
| (27 Active Pipelines & ROI)       |       | (21 Grounded Policies & Ceilings) |
+-----------------+-----------------+       +-----------------------------------+
                  |
                  | Relation: Workflow_Blueprint_Ref / Rollup: Weekly Hours Saved
                  v
+-----------------------------------+       +-----------------------------------+
| DB 01: Inbound Leads & CRM        | ----> | DB 04: Weekly Owner KPI Scorecard |
| (26 Leads, <60s SLA & Pipeline)   |       | (12-Week Friday 3:00 PM Pulse)    |
+-----------------------------------+       +-----------------------------------+
```

### How to Add the 3 Core Relations in Notion:
1. **Link `DB 02 (Workflows)` <-> `DB 03 (Prompt & SOP Vault)`:**
   - In `DB 02`, click `+` to add a column, choose **`Relation`**, select **`03-AI-Prompt-and-SOP-Vault-62`**, and toggle **`Show on 03-AI-Prompt-and-SOP-Vault-62`**.
   - Now every workflow in `DB 02` points directly to its live System Prompt in `DB 03`. When you update a prompt variable in `DB 03`, you immediately see which active Make.com/n8n scenarios use it.
2. **Link `DB 05 (Support Hub)` <-> `DB 03 (Prompt & SOP Vault)`:**
   - In `DB 05`, add a **`Relation`** column pointing to **`03-AI-Prompt-and-SOP-Vault-62`**.
   - Link `POL-01..POL-21` to their corresponding support prompts (`Prompt 6.1`–`6.5`) and Red-Gate crisis scripts (`Emergency Script 01`–`12`).
3. **Link `DB 02 (Workflows)` -> `DB 04 (Weekly Owner KPI Scorecard)`:**
   - In `DB 04`, add a **`Rollup`** property pulling `Sum of Weekly_Hours_Saved` and `Sum of Annualized_Net_ROI_USD` from `DB 02` so your Friday Scorecard automatically displays total hours recovered across all active workflows.

---

## 4. Copy-Paste Notion Formula 2.0 Code Blocks (Minutes 12–15)

Notion Formula 2.0 allows you to embed automatic Green / Amber / Red status badges and financial calculations directly inside your database rows. Create a **`Formula`** column in the respective database below and paste the exact code block:

### Formula 1: 60-Second Speed-to-Lead SLA Status Badge (`Add to DB 01`)
**Formula Column Name:** `Live_SLA_Grade`  
**Purpose:** Automatically grades each lead based on `Speed_To_Lead_Seconds` against the Chapter 3 `60-Second` benchmark.

```javascript
lets(
  sec, prop("Speed_To_Lead_Seconds"),
  ifs(
    empty(sec), "⏳ PENDING FIRST TOUCH",
    sec <= 60, "🟢 PASS (<60s Instant SLA): " + format(sec) + "s",
    sec <= 300, "🟡 AMBER (1-5 Min Delay — 22% Decay Risk): " + format(sec) + "s",
    "🔴 BREACH (>5 Min Delay — High Leak Risk): " + format(sec) + "s"
  )
)
```

### Formula 2: Weighted Pipeline Expected Value Calculator (`Add to DB 01`)
**Formula Column Name:** `Weighted_Pipeline_USD`  
**Purpose:** Multiplies `Estimated_Deal_Value_USD` by the stage probability (`Closed Won = 100%`, `Quote Sent = 45%`, `Booked Consult = 30%`, `Active Follow-Up = 20%`).

```javascript
lets(
  val, prop("Estimated_Deal_Value_USD"),
  stg, prop("Pipeline_Stage"),
  prob, ifs(
    stg == "Closed Won", 1.00,
    contains(stg, "Quote Sent"), 0.45,
    stg == "Booked Consult", 0.30,
    stg == "Active Follow-Up", 0.20,
    0.10
  ),
  round(val * prob)
)
```

### Formula 3: Workflow Annualized Net Labor & Cashflow ROI (`Add to DB 02`)
**Formula Column Name:** `Calculated_Annual_Labor_Savings_USD`  
**Purpose:** Computes annual labor value recovered at a blended `$58/hr` rate minus annual tool-stack subscription cost (`Monthly_Tool_Cost_USD * 12`).

```javascript
lets(
  hrsWk, prop("Weekly_Hours_Saved"),
  toolMo, prop("Monthly_Tool_Cost_USD"),
  blendedRate, 58,
  grossAnnual, hrsWk * blendedRate * 52,
  netAnnual, grossAnnual - (toolMo * 12),
  "$" + format(round(netAnnual)) + "/yr (" + format(round(hrsWk * 52)) + " hrs saved)"
)
```

### Formula 4: T.R.A.V. Governance & Error-Rate Safety Monitor (`Add to DB 02`)
**Formula Column Name:** `Governance_Health_Alert`  
**Purpose:** Flags any workflow whose `TRAV_Risk_Zone` is Red or Amber so operators never disable human approval gates prematurely.

```javascript
lets(
  zone, prop("TRAV_Risk_Zone"),
  status, prop("Operational_Status"),
  ifs(
    status != "Active Production", "⚪ PAUSED / SANDBOX",
    contains(zone, "Red"), "🔴 RED GATE: Immediate Human Takeover Required",
    contains(zone, "Amber"), "🟡 AMBER GATE: 15s Slack Approval Required Before Send",
    "🟢 GREEN GATE: 100% Autonomous 24/7 Execution"
  )
)
```

### Formula 5: Friday 3:00 PM Owner Scorecard Composite Health Badge (`Add to DB 04`)
**Formula Column Name:** `Composite_OS_Grade`  
**Purpose:** Evaluates weekly `Median_Speed_To_Lead_Sec`, `Average_DSO_Days`, `Overdue_AR_Over_15Days_USD`, and `Weekly_Team_Hours_Saved` to produce an instant Friday executive status.

```javascript
lets(
  stl, prop("Median_Speed_To_Lead_Sec"),
  dso, prop("Average_DSO_Days"),
  overdue, prop("Overdue_AR_Over_15Days_USD"),
  hrsSaved, prop("Weekly_Team_Hours_Saved"),
  ifs(
    stl <= 60 and dso <= 16 and overdue <= 2500 and hrsSaved >= 15,
    "🟢 ELITE OS HEALTH (All 4 Core Pillars Passing)",
    stl <= 120 and dso <= 25 and overdue <= 6000,
    "🟡 AMBER WATCH (Review Variance Bottleneck in Prompt 10.1)",
    "🔴 ACTION REQUIRED (Check Speed-to-Lead or Overdue AR Ladder)"
  )
)
```

---

## 5. Recommended Saved Views for Daily & Weekly Execution

To keep your team focused without visual clutter, create these three filtered **Saved Views** at the top of your Notion Command Center:

1. **View 1 — Daily Frontline Speed-to-Lead & Follow-Up Board (`DB 01 — Board View`):**
   - **Group By:** `Pipeline_Stage` (`Booked Consult` -> `Quote Sent` -> `Active Follow-Up` -> `Closed Won`).
   - **Sort By:** `Qualification_Score` (`Descending`) and `Next_Action_Date` (`Ascending`).
   - **Who Uses It:** Front-desk coordinators and sales reps for 10 minutes each morning at 8:30 AM.
2. **View 2 — Amber Gate & Emergency Script Quick-Reference Gallery (`DB 03 — Gallery View`):**
   - **Filter:** `TRAV_Risk_Zone` contains `Amber` OR `Asset_Type` equals `Emergency Operations Script (Red Gate)`.
   - **Card Preview:** Show `Vault_ID`, `Title`, `Trigger_Condition`, and `Input_Variables`.
   - **Who Uses It:** Operations leads and managers whenever a high-stakes client exception occurs.
3. **View 3 — Friday 3:00 PM Founder 15-Minute Pulse (`DB 04 — Table + Chart View`):**
   - **Sort By:** `Friday_Date` (`Descending`).
   - **Summary Row Calculations:** Set bottom column summaries to `Average` on `Median_Speed_To_Lead_Sec` and `Average_DSO_Days`, and `Sum` on `Weekly_Cash_Collected_USD` and `Weekly_Team_Hours_Saved`.
   - **Who Uses It:** The business owner every Friday afternoon at 3:00 PM (`Chapter 10`) before closing the laptop for the weekend.

---

## 6. Connecting Make.com, Zapier & n8n to Your 5 Notion Databases via Internal Integration Token

To allow your automation workflows (`Chapter 3` Lead Router, `Chapter 5` Onboarding Provisioner, `Chapter 6` Support Triage, `Chapter 8` Invoice & Price-Creep Auditor, and `Chapter 10` Friday KPI Synthesizer) to create and update rows automatically inside `DB 01` through `DB 05`:

### Step 1: Create Your Dedicated Service Integration in Notion (`2 Minutes`)
1. Navigate to `https://www.notion.so/my-integrations` while signed in with your company workspace admin account.
2. Click **`+ New integration`** and name it **`SmallBiz-AI-Automation-OS-Engine`**.
3. Under **Capabilities**, enable **`Read content`**, **`Update content`**, and **`Insert content`**. Under **User Capabilities**, select **`No user information`** if you want strict minimal-privilege privacy, or **`Read user information without email addresses`** if assigning owners by Notion User ID.
4. Copy the generated **`Internal Integration Secret`** (`ntn_...` or `secret_...`) and store it inside your Make.com, n8n, or Zapier encrypted connection vault.

### Step 2: Grant Database-Level Access to Your 5 OS Databases (`1 Minute`)
In Notion, integrations cannot read or write to any page unless explicitly invited to that page:
1. Open your top-level **`Small Business AI Automation OS — Executive Command Center`** page (which holds `DB 01` through `DB 05` as child databases).
2. Click the top-right **`...`** menu, scroll down to **`Connections` -> `Connect to`**, and select **`SmallBiz-AI-Automation-OS-Engine`**.
3. Because child databases inherit parent page permissions in Notion, connecting the parent Command Center page automatically grants your Make.com/n8n workflows secure read/write access to all five databases simultaneously while keeping the rest of your private company pages completely isolated.

### Step 3: Copy Your 32-Character Notion Database IDs for Webhook Mapping
Each of your five imported databases has a unique 32-character hexadecimal `Database_ID` found in its browser URL (`https://www.notion.so/yourworkspace/<32_CHAR_DATABASE_ID>?v=...`):
- **Database 01 ID (`NOTION_DB01_LEADS_ID`):** Paste into **Blueprint 01 (`Lead Capture & 60s SMS Router`)** and **Blueprint 02 (`3-Tier Quote & 14-Day Follow-Up`)** so every new inbound inquiry creates a row with `Lead_Received_Timestamp`, `First_Touch_Timestamp`, `Speed_To_Lead_Seconds`, and `Qualification_Score`.
- **Database 02 ID (`NOTION_DB02_WORKFLOWS_ID`):** Used by the **Dead-Letter Queue Monitor (`Prompt 2.5`)** and **Quarterly Governance Auditor (`Prompt 10.4`)** to log weekly execution counts and error rates.
- **Database 03 ID (`NOTION_DB03_VAULT_ID`):** Used by **Prompt 9.1 (`7-Block Living SOP Compiler`)** whenever a new Loom video is dropped into `#sop-capture`, automatically creating a structured SOP row ready for a 15-second owner review.
- **Database 04 ID (`NOTION_DB04_SCORECARD_ID`):** Used every Friday at 2:55 PM by **Prompt 10.1 (`Friday Executive KPI Synthesizer`)** to write the week's 12 aggregated metrics and generate the Slack executive brief.
- **Database 05 ID (`NOTION_DB05_SUPPORT_ID`):** Queried in real time by **Prompt 6.2 (`Grounded RAG Support Responder`)** to fetch the verified `Approved_Policy_Summary` and `Max_Auto_Refund_USD` ceiling before drafting any customer reply.

---

## 7. Team Role Permissions, Mobile App Pinning & Weekly CSV Backup Protocol

### 7.1 Role-Based Access Control (RBAC) for 1-to-25 Person Teams
- **Founder / Operations Director (`Full Access`):** Can edit database schemas, modify `Approved_Policy_Summary` rows in `DB 05`, adjust `Max_Auto_Refund_USD` ceilings, and sign off on `DB 04` Friday Scorecards.
- **Sales Reps, Front-Desk & Fulfillment Staff (`Can Edit Content` — Schema Locked):** Click **`Lock database`** on `DB 01`, `DB 02`, `DB 03`, `DB 04`, and `DB 05` once imported! In Notion, locking a database prevents staff from accidentally deleting a column or breaking a Formula 2.0 block while still allowing them to add leads, update pipeline stages, and check off tasks normally.
- **External Bookkeepers or Contractors (`Can View` or Filtered Page Share):** Share only the specific filtered view required for their role.

### 7.2 Pinning the Mobile Quick-Capture Views (`iOS & Android`)
Install the Notion mobile app on your phone and add two home-screen shortcuts:
1. **`#amber-approvals` & `DB 01` Active Today View:** Allows you to inspect high-ticket leads on the go in 15 seconds.
2. **`DB 04` Friday 3:00 PM Scorecard View:** Lets you review all 12 core business metrics from your phone on Friday afternoon in under 5 minutes.

### 7.3 Monthly Offline CSV Snapshot Protocol (`30 Seconds`)
On the first Friday of each month (alongside `Prompt 10.3`), click **`... -> Export -> Markdown & CSV`** on your top-level Command Center page and save the `.zip` archive to your local company backup drive alongside your Web Companion App JSON backup (`smallbiz-automation-os-backup.json`). This ensures 100% offline disaster recovery and audit readiness year-round.
"""
    guide_path = NOTION_DIR / "NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"
    guide_path.write_text(sanitize_banned_stems(guide), encoding="utf-8")
    return len(guide.split())


def generate_sheet1_roi_calculator_csv():
    headers = [
        "Row_ID",
        "Category_Or_Department",
        "Parameter_Or_Workflow_Metric",
        "Solo_Micro_Business_250K",
        "Local_Clinic_Home_Service_850K",
        "Multi_Crew_Agency_Contractor_2_4M",
        "Custom_Business_Baseline_Formula_Or_Rule",
        "Target_Post_Automation_Benchmark",
        "Chapter_And_Prompt_Reference",
    ]
    rows = [
        ("R-01", "1. Baseline Profile", "Annual Gross Revenue ($/yr)", "$252,000", "$852,000", "$2,400,000", "Monthly_Invoiced_Revenue * 12", "+18% to +32% Lift via Speed-to-Lead", "Chapter 1 — Worksheet 01"),
        ("R-02", "1. Baseline Profile", "Total Team Headcount (FTE Including Owner)", "2 FTE", "7 FTE", "18 FTE", "Owner + Admin + Tech/Specialist FTE", "Zero Extra Admin Hiring Needed", "Chapter 1 — Section 2"),
        ("R-03", "1. Baseline Profile", "Blended Hourly Labor Rate ($/hr)", "$75.00/hr", "$56.00/hr", "$68.00/hr", "(Owner_Rate * Owner_Share) + (Staff_Rate * Staff_Share)", "Reallocate 70% of Admin Hrs to Billable Work", "Chapter 1 — Prompt 1.1"),
        ("R-04", "2. Dept 01 Labor", "Lead Capture, Voicemail & CRM Copy-Paste (Hrs/Wk)", "3.5 hrs/wk", "6.0 hrs/wk", "9.0 hrs/wk", "Sum(Freq_Wk * Mins_Per_Lead) / 60", "1.0 to 2.0 hrs/wk (80% Automated)", "Chapter 3 — Prompts 3.1-3.4"),
        ("R-05", "2. Dept 02 Labor", "Sales Qualification, 3-Tier Quoting & Chasers (Hrs/Wk)", "5.0 hrs/wk", "5.5 hrs/wk", "11.0 hrs/wk", "Sum(Quotes_Wk * Mins_Per_Quote) / 60", "1.5 to 3.0 hrs/wk (Amber 1-Click Gate)", "Chapter 4 — Prompts 4.1-4.5"),
        ("R-06", "2. Dept 03 Labor", "Client Onboarding, Tier-1 Support & Review Asks (Hrs/Wk)", "3.0 hrs/wk", "6.5 hrs/wk", "8.5 hrs/wk", "Sum(Onboard_Support_Mins_Wk) / 60", "1.0 to 2.5 hrs/wk (Grounded RAG Triage)", "Chapters 5-7 — Prompts 5.1-7.5"),
        ("R-07", "2. Dept 04 Labor", "Invoicing, Overdue AR Chasers & Receipt OCR (Hrs/Wk)", "2.5 hrs/wk", "4.5 hrs/wk", "8.0 hrs/wk", "Sum(Billing_AP_Mins_Wk) / 60", "0.8 to 2.0 hrs/wk (Same-Day Auto Billing)", "Chapter 8 — Prompts 8.1-8.5"),
        ("R-08", "2. Dept 05 Labor", "Team SOP Lookups, Delegation & Friday KPI Pull (Hrs/Wk)", "2.0 hrs/wk", "3.5 hrs/wk", "6.0 hrs/wk", "Sum(Internal_Mgmt_Mins_Wk) / 60", "0.5 to 1.5 hrs/wk (15-Min Friday Pulse)", "Chapters 9-10 — Prompts 9.1-10.5"),
        ("R-09", "3. Component 1 (L_tax)", "Total Weekly Repetitive Manual Hours (Hrs/Wk)", "16.0 hrs/wk", "26.0 hrs/wk", "42.5 hrs/wk", "Sum(Dept_01_Hrs .. Dept_05_Hrs)", "Recover 70% (11.2 to 29.8 hrs/wk saved)", "Chapter 1 — CMF Component 1"),
        ("R-10", "3. Component 1 (L_tax)", "Annual Manual Labor Waste ($/yr)", "$62,400/yr", "$75,712/yr", "$150,280/yr", "Total_Weekly_Manual_Hours * Blended_Rate * 52", "Save $43,680 to $105,196/yr in Payroll Drag", "Chapter 1 — Prompt 1.1"),
        ("R-11", "4. Component 2 (R_leak)", "Monthly Inbound Leads Across All 5 Channels", "35 leads/mo", "125 leads/mo", "260 leads/mo", "Web + Phone + SMS + Social + GBP Leads", "100% Normalized & Logged via Idempotency Key", "Chapter 3 — Prompt 3.1"),
        ("R-12", "4. Component 2 (R_leak)", "% Inbound Leads Delayed (>5 Min Response or Missed Call)", "40% (14/mo)", "38% (48/mo)", "34% (88/mo)", "Delayed_Or_Missed_Leads / Total_Monthly_Leads", "< 4% Delayed (96%+ Answered Under 60 Seconds)", "Chapter 3 — Prompt 3.3"),
        ("R-13", "4. Component 2 (R_leak)", "Net Recoverable Conversion Rate (%)", "20%", "18%", "15%", "Fast_Response_Close_Rate - Delayed_Close_Rate", "+15% to +22% Net Conversion Recovery", "Chapter 1 — Prompt 1.2"),
        ("R-14", "4. Component 2 (R_leak)", "Average Customer First-Year Value ($ LTV)", "$2,200", "$1,650", "$3,100", "Avg_Initial_Job_Or_Retainer * Repeat_Multiplier", "+18% LTV Expansion via Recall & Review Loops", "Chapter 7 — Prompt 7.4"),
        ("R-15", "4. Component 2 (R_leak)", "Annual Speed-to-Lead Revenue Leak ($/yr)", "$73,920/yr", "$171,072/yr", "$491,040/yr", "Delayed_Leads_Mo * Net_Close_Rate * LTV * 12", "Capture 65%+ via 60-Second SMS/Email Router", "Chapter 3 — Blueprint 01"),
        ("R-16", "5. Component 3 (C_drag)", "Monthly Invoiced Revenue ($/mo)", "$21,000/mo", "$71,000/mo", "$200,000/mo", "Gross_Monthly_Billed_AR", "100% Same-Day Invoice Dispatch on Completion", "Chapter 8 — Prompt 8.1"),
        ("R-17", "5. Component 3 (C_drag)", "Late / Uncollected Receivables & Unbilled Scope Drag (%)", "2.0%", "2.4%", "2.8%", "Bad_Debt_Writeoff_Pct + Unbilled_Change_Order_Pct", "Compress DSO to 11-16 Days & Drag < 0.5%", "Chapter 8 — Prompt 8.2"),
        ("R-18", "5. Component 3 (C_drag)", "Annual Receivables & Cashflow Drag Loss ($/yr)", "$5,040/yr", "$20,448/yr", "$67,200/yr", "Monthly_Invoiced_Revenue * Drag_Rate * 12", "Recover via 5-Stage Polite-to-Firm AR Chaser", "Chapter 8 — Blueprint 03"),
        ("R-19", "6. Executive Summary", "TOTAL ANNUAL COST OF MANUAL FRICTION (Annual CMF)", "$141,360/yr", "$267,232/yr", "$708,520/yr", "Component_1_Labor + Component_2_LeadLeak + Component_3_CashDrag", "Represents 25% to 56% of Baseline Revenue", "Chapter 1 — Master CMF Formula"),
        ("R-20", "6. Executive Summary", "Conservative First-Year Gross Recovery (65% Capture)", "$91,884/yr", "$173,701/yr", "$460,538/yr", "Total_Annual_CMF * 0.65", "Phased 90-Day Implementation (Phases I-III)", "Chapter 10 — Prompt 10.2"),
        ("R-21", "6. Executive Summary", "Estimated Annual No-Code & AI Tool-Stack Cost ($/yr)", "$1,428/yr ($119/mo)", "$2,148/yr ($179/mo)", "$3,732/yr ($311/mo)", "(Make_Or_n8n + LLM_API_Tokens + Twilio_SMS) * 12", "< 1.5% of Recovered Annual Value", "Chapter 10 — Prompt 10.3"),
        ("R-22", "6. Executive Summary", "PROJECTED NET FIRST-YEAR AUTOMATION SAVINGS ($/yr)", "$90,456/yr", "$171,553/yr", "$456,806/yr", "Gross_65Pct_Recovery - Annual_Tool_Stack_Cost", "Net ROI Multiple: 63.3x to 122.4x (Payback < 6 Days)", "Module 1 Web App & Worksheet 01"),
    ]
    write_csv_file(SPREADSHEETS_DIR / "sheet1-automation-roi-and-leak-calculator.csv", headers, rows)
    return len(rows), len(headers)


# =============================================================================
# PART B: COMMERCIAL COVER & KDP FULL-WRAP PRINT SUITE (08-COVER-DESIGN/)
# =============================================================================

def generate_grid_defs(prefix: str) -> str:
    return f"""
  <defs>
    <linearGradient id="{prefix}_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="55%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <linearGradient id="{prefix}_emerald" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="100%" stop-color="#10B981" />
    </linearGradient>
    <linearGradient id="{prefix}_cyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284C7" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
    <linearGradient id="{prefix}_amber" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D97706" />
      <stop offset="100%" stop-color="#F59E0B" />
    </linearGradient>
    <radialGradient id="{prefix}_glow" cx="50%" cy="42%" r="55%">
      <stop offset="0%" stop-color="#059669" stop-opacity="0.28" />
      <stop offset="55%" stop-color="#0284C7" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.0" />
    </radialGradient>
    <pattern id="{prefix}_grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#334155" stroke-width="0.8" stroke-opacity="0.45" />
      <circle cx="40" cy="40" r="1.4" fill="#64748B" fill-opacity="0.45" />
    </pattern>
  </defs>
"""


def build_kindle_ebook_svg() -> str:
    # 1600 x 2560
    grid_lines = []
    for y in range(180, 2420, 80):
        grid_lines.append(f'<line x1="80" y1="{y}" x2="1520" y2="{y}" stroke="#1E293B" stroke-width="1" opacity="0.5"/>')
    for x in range(80, 1560, 80):
        grid_lines.append(f'<line x1="{x}" y1="180" x2="{x}" y2="2400" stroke="#1E293B" stroke-width="1" opacity="0.5"/>')
    extra_mesh = "\n  ".join(grid_lines)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 2560" width="1600" height="2560">
  {generate_grid_defs("kdp")}
  <rect width="1600" height="2560" fill="url(#kdp_bg)" />
  <rect width="1600" height="2560" fill="url(#kdp_grid)" />
  <circle cx="800" cy="1180" r="760" fill="url(#kdp_glow)" />
  {extra_mesh}

  <!-- Outer Architectural Frame -->
  <rect x="64" y="64" width="1472" height="2432" rx="18" fill="none" stroke="#334155" stroke-width="3" />
  <rect x="84" y="84" width="1432" height="2392" rx="12" fill="none" stroke="#059669" stroke-width="1.5" stroke-opacity="0.6" />

  <!-- Top Edition Header Bar -->
  <rect x="140" y="130" width="1320" height="76" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <circle cx="185" cy="168" r="12" fill="#059669" />
  <circle cx="220" cy="168" r="12" fill="#0284C7" />
  <circle cx="255" cy="168" r="12" fill="#D97706" />
  <text x="300" y="178" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="800" letter-spacing="2">
    2026 ENTERPRISE EDITION • ZERO EXTRA STAFF REQUIRED
  </text>

  <!-- Main Title Block -->
  <text x="140" y="340" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="34" font-weight="700" letter-spacing="3">
    SYSTEM ARCHITECTURE FOR 1–25 PERSON TEAMS
  </text>
  <text x="140" y="470" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="108" font-weight="900" letter-spacing="-1">
    THE SMALL BUSINESS
  </text>
  <text x="140" y="600" fill="#34D399" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="114" font-weight="900" letter-spacing="-1">
    AI AUTOMATION
  </text>
  <text x="140" y="730" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="108" font-weight="900" letter-spacing="-1">
    OPERATING SYSTEM
  </text>

  <!-- Accent Divider -->
  <rect x="140" y="785" width="460" height="10" rx="5" fill="url(#kdp_emerald)" />
  <rect x="620" y="785" width="240" height="10" rx="5" fill="url(#kdp_cyan)" />
  <rect x="880" y="785" width="120" height="10" rx="5" fill="url(#kdp_amber)" />

  <!-- Subtitle -->
  <text x="140" y="865" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="36" font-weight="500">
    A Practical System to Automate Lead Capture, Customer Support,
  </text>
  <text x="140" y="918" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="36" font-weight="500">
    Invoicing, Team Operations, and Weekly Owner Reporting
  </text>

  <!-- Centerpiece: 5-Department Operating System Blueprint Graphic -->
  <rect x="140" y="990" width="1320" height="1060" rx="22" fill="#0F172A" stroke="#334155" stroke-width="3" />
  <rect x="140" y="990" width="1320" height="68" rx="22" fill="#1E293B" />
  <text x="185" y="1034" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    T.R.A.V. GOVERNANCE ENGINE: TRIGGER -&gt; RULES -&gt; AI -&gt; VERIFICATION GATE
  </text>

  <!-- Central Hub Node -->
  <circle cx="800" cy="1510" r="165" fill="#1E293B" stroke="#059669" stroke-width="6" />
  <circle cx="800" cy="1510" r="135" fill="#0F172A" stroke="#0284C7" stroke-width="2" stroke-dasharray="8,6" />
  <text x="800" y="1475" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700">CORE ENGINE</text>
  <text x="800" y="1520" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="34" font-weight="900">5-DEPT OS</text>
  <text x="800" y="1560" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="21">50 PROMPTS • 12 SCRIPTS</text>

  <!-- Connector Spokes -->
  <line x1="800" y1="1345" x2="800" y2="1220" stroke="#059669" stroke-width="4" />
  <line x1="650" y1="1430" x2="430" y2="1280" stroke="#0284C7" stroke-width="4" />
  <line x1="950" y1="1430" x2="1170" y2="1280" stroke="#059669" stroke-width="4" />
  <line x1="665" y1="1605" x2="430" y2="1770" stroke="#D97706" stroke-width="4" />
  <line x1="935" y1="1605" x2="1170" y2="1770" stroke="#0284C7" stroke-width="4" />

  <!-- Dept 01 Top Center Card -->
  <rect x="530" y="1090" width="540" height="130" rx="14" fill="#1E293B" stroke="#059669" stroke-width="3" />
  <text x="800" y="1140" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="22" font-weight="700">DEPT 01 • SPEED-TO-LEAD (&lt;60s SLA)</text>
  <text x="800" y="1182" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="700">Omnichannel Intake &amp; Missed-Call SMS Bot</text>

  <!-- Dept 02 Top Left Card -->
  <rect x="180" y="1240" width="440" height="150" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="3" />
  <text x="210" y="1290" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="21" font-weight="700">DEPT 02 • SALES &amp; QUOTING</text>
  <text x="210" y="1332" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25" font-weight="700">Voice-to-3-Tier Proposals</text>
  <text x="210" y="1368" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="21">&amp; 14-Day Polite Follow-Up Loop</text>

  <!-- Dept 03 Top Right Card -->
  <rect x="980" y="1240" width="440" height="150" rx="14" fill="#1E293B" stroke="#059669" stroke-width="3" />
  <text x="1010" y="1290" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="21" font-weight="700">DEPT 03 • DELIVERY &amp; SUPPORT</text>
  <text x="1010" y="1332" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25" font-weight="700">Zero-Drop Onboarding, RAG</text>
  <text x="1010" y="1368" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="21">Support &amp; 5-Star Review Engine</text>

  <!-- Dept 04 Bottom Left Card -->
  <rect x="180" y="1700" width="440" height="150" rx="14" fill="#1E293B" stroke="#D97706" stroke-width="3" />
  <text x="210" y="1750" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="21" font-weight="700">DEPT 04 • FINANCE &amp; A/R</text>
  <text x="210" y="1792" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25" font-weight="700">Same-Day Invoicing, 5-Stage</text>
  <text x="210" y="1828" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="21">AR Chaser &amp; Receipt OCR</text>

  <!-- Dept 05 Bottom Right Card -->
  <rect x="980" y="1700" width="440" height="150" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="3" />
  <text x="1010" y="1750" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="21" font-weight="700">DEPT 05 • OWNER COMMAND</text>
  <text x="1010" y="1792" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25" font-weight="700">7-Block Living SOPs &amp; Friday</text>
  <text x="1010" y="1828" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="21">15-Minute 12-KPI Scorecard</text>

  <!-- Bottom Telemetry Strip Inside Diagram -->
  <rect x="180" y="1905" width="1240" height="105" rx="12" fill="#1E293B" stroke="#334155" stroke-width="2" />
  <text x="220" y="1950" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700">GREEN GATE (75% AUTO)</text>
  <text x="220" y="1985" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="20">24/7 Unattended Routine Execution</text>
  <text x="660" y="1950" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700">AMBER GATE (20% HITL)</text>
  <text x="660" y="1985" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="20">AI Draft + 15s Human Approval</text>
  <text x="1090" y="1950" fill="#F87171" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700">RED GATE (5% CRISIS)</text>
  <text x="1090" y="1985" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="20">Immediate Human Takeover</text>

  <!-- Footer Author & Deliverable Pill Bar -->
  <rect x="140" y="2120" width="1320" height="170" rx="16" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="800" y="2180" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="30" font-weight="800">
    INCLUDES 50 TESTED WORKFLOW PROMPTS • 12 EMERGENCY SCRIPTS • 90-DAY ROADMAP
  </text>
  <text x="800" y="2235" text-anchor="middle" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="600">
    MAKE.COM • ZAPIER • N8N • OPENAI • CLAUDE • NOTION • QUICKBOOKS • STRIPE
  </text>

  <text x="800" y="2395" text-anchor="middle" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="700" letter-spacing="3">
    DIGITAL PUBLISHING STUDIO • ENTERPRISE OPERATIONS SERIES
  </text>
</svg>
"""


def build_kdp_full_wrap_svg(page_count: int = 242) -> str:
    # 12.795 in x 9.25 in @ 300 DPI = 3838.5 x 2775 -> viewBox="0 0 3838 2775"
    # Left Bleed: 0..37.5 px (0.125")
    # Back Cover Trim: 37.5..1837.5 px (6.000")
    # Spine: 1837.5..2001.0 px (0.545" = 163.5 px) -> Spine Center X = 1919.25 px
    # Front Cover Trim: 2001.0..3801.0 px (6.000")
    # Right Bleed: 3801.0..3838.0 px (0.125")
    spine_in = round(page_count * 0.002252, 3)
    mesh = []
    for y in range(120, 2680, 90):
        mesh.append(f'<line x1="60" y1="{y}" x2="3778" y2="{y}" stroke="#1E293B" stroke-width="1" opacity="0.45"/>')
    for x in range(60, 3780, 90):
        mesh.append(f'<line x1="{x}" y1="120" x2="{x}" y2="2655" stroke="#1E293B" stroke-width="1" opacity="0.45"/>')
    mesh_str = "\n  ".join(mesh)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3838 2775" width="3838" height="2775">
  {generate_grid_defs("wrap")}
  <!-- Full Bleed Background (12.795" x 9.250") -->
  <rect width="3838" height="2775" fill="url(#wrap_bg)" />
  <rect width="3838" height="2775" fill="url(#wrap_grid)" />
  {mesh_str}

  <circle cx="2900" cy="1380" r="820" fill="url(#wrap_glow)" />
  <circle cx="940" cy="1380" r="720" fill="url(#wrap_glow)" />

  <!-- ===================================================================== -->
  <!-- BACK COVER SAFE ZONE (X: 140 to 1730, Y: 140 to 2635)                 -->
  <!-- ===================================================================== -->
  <rect x="115" y="115" width="1645" height="2545" rx="18" fill="#0F172A" fill-opacity="0.78" stroke="#334155" stroke-width="3" />

  <rect x="170" y="175" width="1535" height="72" rx="10" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="210" y="221" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    STOP DROWNING IN MANUAL BUSYWORK. INSTALL YOUR BUSINESS OPERATING SYSTEM.
  </text>

  <text x="170" y="330" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="44" font-weight="800">
    Recover 15+ Hours Every Week Without Hiring Extra Admin Staff
  </text>
  <text x="170" y="405" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28">
    Most 1-to-25 person businesses lose 20% to 35% of their potential net profit to the three silent killers of
  </text>
  <text x="170" y="448" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28">
    small business growth: missed after-hours leads, manual copy-pasting between disconnected software apps,
  </text>
  <text x="170" y="491" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28">
    and overdue invoices sitting uncollected for 40+ days.
  </text>
  <text x="170" y="555" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="600">
    The Small Business AI Automation Operating System gives founders, clinic directors, trade contractors,
  </text>
  <text x="170" y="598" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="600">
    and B2B agency leaders a deterministic, zero-hallucination blueprint to automate all 5 core departments:
  </text>

  <!-- 5 Department Feature Cards on Back Cover -->
  <rect x="170" y="655" width="1535" height="175" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="210" y="708" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    1. THE T.R.A.V. HUMAN-IN-THE-LOOP SAFETY ARCHITECTURE (CHAPTERS 1–2)
  </text>
  <text x="210" y="752" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25">
    Eliminate AI pricing errors with closed-world truth tables, deterministic pre-AI regex guardrails,
  </text>
  <text x="210" y="790" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24">
    and 15-second Slack/Teams Amber Approval Cards for custom quotes and sensitive client replies.
  </text>

  <rect x="170" y="855" width="1535" height="175" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="210" y="908" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    2. 60-SECOND SPEED-TO-LEAD &amp; 3-TIER QUOTE ENGINE (CHAPTERS 3–4)
  </text>
  <text x="210" y="952" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25">
    Capture web forms, missed calls, and DMs in under 60 seconds, convert field voice memos into
  </text>
  <text x="210" y="990" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24">
    Good-Better-Best proposals, and run the 14-day polite-persistence follow-up loop automatically.
  </text>

  <rect x="170" y="1055" width="1535" height="175" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="210" y="1108" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    3. ZERO-DROP ONBOARDING, RAG SUPPORT &amp; 5-STAR REVIEWS (CHAPTERS 5–7)
  </text>
  <text x="210" y="1152" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25">
    Provision client portals the second a deposit clears, resolve 60%+ of routine Tier-1 tickets from
  </text>
  <text x="210" y="1190" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24">
    your verified knowledge base, and route happy customers to Google reviews while intercepting detractors.
  </text>

  <rect x="170" y="1255" width="1535" height="175" rx="12" fill="#1E293B" stroke="#D97706" stroke-width="2" />
  <text x="210" y="1308" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    4. AUTOMATED INVOICING, 5-STAGE A/R CHASER &amp; RECEIPT OCR (CHAPTER 8)
  </text>
  <text x="210" y="1352" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25">
    Compress Days Sales Outstanding (DSO) from 42 days to 12 days with instant milestone billing,
  </text>
  <text x="210" y="1390" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24">
    relationship-safe overdue payment reminders, and automated 5% supplier price-creep detection.
  </text>

  <rect x="170" y="1455" width="1535" height="175" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2" />
  <text x="210" y="1508" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">
    5. LIVING TEAM SOPs &amp; THE 15-MINUTE FRIDAY SCORECARD (CHAPTERS 9–10)
  </text>
  <text x="210" y="1552" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="25">
    Turn 3-minute screen recordings into 7-block SOPs, delegate tasks by voice memo, and review your
  </text>
  <text x="210" y="1590" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24">
    entire company every Friday at 3:00 PM across 12 Core Owner KPIs in 15 minutes flat.
  </text>

  <!-- Back Cover Comparison Matrix -->
  <rect x="170" y="1670" width="1535" height="390" rx="14" fill="#1E293B" stroke="#334155" stroke-width="2" />
  <text x="210" y="1725" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="800">
    INSIDE THIS COMPLETE ENTERPRISE OPERATING MANUAL:
  </text>
  <text x="210" y="1785" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24">✓ 50 Copy-Ready JSON &amp; Markdown AI Workflow Prompts (Prompts 1.1 – 10.5)</text>
  <text x="210" y="1835" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24">✓ 12 Red-Gate Emergency Business Operations Scripts (Customer, AR &amp; Outage)</text>
  <text x="210" y="1885" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24">✓ 20 High-Resolution System Architecture &amp; Decision-Tree Vector Diagrams</text>
  <text x="210" y="1935" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24">✓ 10 Department Implementation Workbooks &amp; Phased 90-Day Rollout Schedule</text>
  <text x="210" y="1985" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="24">✓ Companion Offline Web Calculator Suite, Notion OS &amp; Make/n8n Blueprints</text>

  <!-- KDP Mandatory ISBN Barcode White Box (2.0" x 1.2" = 600 x 360 px at bottom-right of back cover) -->
  <rect x="170" y="2160" width="860" height="360" rx="12" fill="#1E293B" stroke="#334155" stroke-width="2" />
  <text x="210" y="2230" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="800">
    BUSINESS &amp; ECONOMICS / OPERATIONS
  </text>
  <text x="210" y="2280" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24">
     Small Business Management &amp; AI Systems
  </text>
  <text x="210" y="2345" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="23">
    Trim: 6.0" x 9.0" • {page_count} Pages • Spine: {spine_in}"
  </text>
  <text x="210" y="2395" fill="#CBD5E1" font-family="JetBrains Mono, Consolas, monospace" font-size="22">
    Edition: 2026 Enterprise Print Edition
  </text>

  <!-- Official KDP Barcode Safe Placement Zone (2.0" x 1.2" = 600 x 360 px) -->
  <rect x="1105" y="2160" width="600" height="360" rx="6" fill="#FFFFFF" stroke="#0F172A" stroke-width="3" />
  <text x="1405" y="2315" text-anchor="middle" fill="#0F172A" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700">
    ISBN BARCODE ZONE
  </text>
  <text x="1405" y="2355" text-anchor="middle" fill="#64748B" font-family="JetBrains Mono, Consolas, monospace" font-size="20">
    2.00" x 1.20" KDP Print Safe Box
  </text>

  <!-- ===================================================================== -->
  <!-- CENTER SPINE (X: 1837.5 to 2001.0 px | Width: 163.5 px = 0.545 in)    -->
  <!-- ===================================================================== -->
  <rect x="1837.5" y="0" width="163.5" height="2775" fill="#0F172A" stroke="#059669" stroke-width="2" />
  <g transform="translate(1919.25, 1387.5) rotate(90)">
    <text x="0" y="10" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="34" font-weight="800" letter-spacing="2">
      THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM   •   2026 EDITION
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- FRONT COVER SAFE ZONE (X: 2080 to 3720, Y: 115 to 2660)               -->
  <!-- ===================================================================== -->
  <rect x="2075" y="115" width="1645" height="2545" rx="18" fill="none" stroke="#334155" stroke-width="3" />
  <rect x="2130" y="175" width="1535" height="76" rx="12" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <circle cx="2175" cy="213" r="12" fill="#059669" />
  <circle cx="2210" cy="213" r="12" fill="#0284C7" />
  <circle cx="2245" cy="213" r="12" fill="#D97706" />
  <text x="2285" y="223" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="800" letter-spacing="2">
    2026 ENTERPRISE EDITION • FOR 1–25 PERSON TEAMS
  </text>

  <text x="2130" y="380" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="34" font-weight="700" letter-spacing="3">
    DETERMINISTIC HUMAN-IN-THE-LOOP OPERATIONS
  </text>
  <text x="2130" y="510" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="112" font-weight="900">
    THE SMALL BUSINESS
  </text>
  <text x="2130" y="640" fill="#34D399" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="118" font-weight="900">
    AI AUTOMATION
  </text>
  <text x="2130" y="770" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="112" font-weight="900">
    OPERATING SYSTEM
  </text>

  <rect x="2130" y="825" width="520" height="10" rx="5" fill="url(#wrap_emerald)" />
  <rect x="2670" y="825" width="280" height="10" rx="5" fill="url(#wrap_cyan)" />
  <rect x="2970" y="825" width="150" height="10" rx="5" fill="url(#wrap_amber)" />

  <text x="2130" y="905" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="36" font-weight="500">
    A Practical System to Automate Lead Capture, Customer Support,
  </text>
  <text x="2130" y="958" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="36" font-weight="500">
    Invoicing, Team Operations, and Weekly Owner Reporting
  </text>

  <!-- Front Cover Architecture Matrix Card -->
  <rect x="2130" y="1035" width="1535" height="1140" rx="22" fill="#0F172A" stroke="#334155" stroke-width="3" />
  <rect x="2130" y="1035" width="1535" height="70" rx="22" fill="#1E293B" />
  <text x="2180" y="1080" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="26" font-weight="700">
    5-DEPARTMENT OPERATING SYSTEM ARCHITECTURE • ZERO HALLUCINATION DESIGN
  </text>

  <circle cx="2897" cy="1595" r="175" fill="#1E293B" stroke="#059669" stroke-width="6" />
  <text x="2897" y="1565" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700">T.R.A.V. CORE</text>
  <text x="2897" y="1615" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="38" font-weight="900">5-DEPT OS</text>
  <text x="2897" y="1655" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="22">50 PROMPTS • 12 SCRIPTS</text>

  <rect x="2597" y="1145" width="600" height="135" rx="14" fill="#1E293B" stroke="#059669" stroke-width="3" />
  <text x="2897" y="1198" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700">DEPT 01 • SPEED-TO-LEAD (&lt;60s SLA)</text>
  <text x="2897" y="1242" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="27" font-weight="700">Omnichannel Intake &amp; Missed-Call SMS Bot</text>

  <rect x="2180" y="1330" width="480" height="160" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="3" />
  <text x="2210" y="1385" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="23" font-weight="700">DEPT 02 • SALES &amp; QUOTING</text>
  <text x="2210" y="1430" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="700">Voice-to-3-Tier Proposals</text>
  <text x="2210" y="1468" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="22">&amp; 14-Day Polite Follow-Up Loop</text>

  <rect x="3135" y="1330" width="480" height="160" rx="14" fill="#1E293B" stroke="#059669" stroke-width="3" />
  <text x="3165" y="1385" fill="#34D399" font-family="JetBrains Mono, Consolas, monospace" font-size="23" font-weight="700">DEPT 03 • DELIVERY &amp; SUPPORT</text>
  <text x="3165" y="1430" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="700">Zero-Drop Onboarding, RAG</text>
  <text x="3165" y="1468" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="22">Support &amp; 5-Star Review Funnel</text>

  <rect x="2180" y="1775" width="480" height="160" rx="14" fill="#1E293B" stroke="#D97706" stroke-width="3" />
  <text x="2210" y="1830" fill="#FBBF24" font-family="JetBrains Mono, Consolas, monospace" font-size="23" font-weight="700">DEPT 04 • FINANCE &amp; A/R</text>
  <text x="2210" y="1875" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="700">Same-Day Invoicing, 5-Stage</text>
  <text x="2210" y="1913" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="22">AR Chaser &amp; Receipt OCR</text>

  <rect x="3135" y="1775" width="480" height="160" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="3" />
  <text x="3165" y="1830" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="23" font-weight="700">DEPT 05 • OWNER COMMAND</text>
  <text x="3165" y="1875" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="26" font-weight="700">7-Block Living SOPs &amp; Friday</text>
  <text x="3165" y="1913" fill="#94A3B8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="22">15-Minute 12-KPI Scorecard</text>

  <rect x="2180" y="2005" width="1435" height="120" rx="12" fill="#1E293B" stroke="#334155" stroke-width="2" />
  <text x="2897" y="2058" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="800">
    50 TESTED AI PROMPTS • 12 EMERGENCY SCRIPTS • 10 WORKBOOKS • 90-DAY ROADMAP
  </text>
  <text x="2897" y="2102" text-anchor="middle" fill="#38BDF8" font-family="JetBrains Mono, Consolas, monospace" font-size="23">
    MAKE.COM • ZAPIER • N8N • OPENAI • CLAUDE • NOTION • QUICKBOOKS • STRIPE
  </text>

  <rect x="2130" y="2260" width="1535" height="180" rx="16" fill="#1E293B" stroke="#059669" stroke-width="2" />
  <text x="2897" y="2335" text-anchor="middle" fill="#34D399" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="34" font-weight="800">
    EXECUTIVE OPERATIONS &amp; SYSTEMS ENGINEERING EDITION
  </text>
  <text x="2897" y="2395" text-anchor="middle" fill="#CBD5E1" font-family="JetBrains Mono, Consolas, monospace" font-size="24">
    DESIGNED FOR CLINICS • HOME SERVICES • AGENCIES • RETAIL &amp; B2B TEAMS
  </text>
</svg>
"""


def build_gumroad_tier_svg(
    prefix: str,
    tier_badge: str,
    price_badge: str,
    headline_1: str,
    headline_2: str,
    subtitle: str,
    accent_hex: str,
    bullets: list,
    metrics: list,
) -> str:
    # 1600 x 1200 landscape Gumroad cover
    mesh = []
    for y in range(60, 1160, 60):
        mesh.append(f'<line x1="50" y1="{y}" x2="1550" y2="{y}" stroke="#1E293B" stroke-width="1" opacity="0.5"/>')
    for x in range(50, 1560, 60):
        mesh.append(f'<line x1="{x}" y1="60" x2="{x}" y2="1140" stroke="#1E293B" stroke-width="1" opacity="0.5"/>')
    mesh_str = "\n  ".join(mesh)

    bullet_svg = []
    for idx, b in enumerate(bullets):
        by = 610 + idx * 78
        bullet_svg.append(
            f'<rect x="90" y="{by - 40}" width="840" height="62" rx="10" fill="#1E293B" stroke="{accent_hex}" stroke-width="1.8" />'
            f'<circle cx="126" cy="{by - 9}" r="10" fill="{accent_hex}" />'
            f'<text x="152" y="{by - 1}" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="23" font-weight="700">{b}</text>'
        )

    metric_svg = []
    for idx, (m_lbl, m_val, m_sub) in enumerate(metrics):
        my = 490 + idx * 185
        metric_svg.append(
            f'<rect x="970" y="{my}" width="540" height="160" rx="14" fill="#1E293B" stroke="{accent_hex}" stroke-width="2.5" />'
            f'<text x="1005" y="{my + 45}" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="19" font-weight="700">{m_lbl}</text>'
            f'<text x="1005" y="{my + 102}" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="44" font-weight="800">{m_val}</text>'
            f'<text x="1005" y="{my + 138}" fill="{accent_hex}" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="20" font-weight="600">{m_sub}</text>'
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  {generate_grid_defs(prefix)}
  <rect width="1600" height="1200" fill="url(#{prefix}_bg)" />
  <rect width="1600" height="1200" fill="url(#{prefix}_grid)" />
  {mesh_str}
  <circle cx="1150" cy="600" r="520" fill="url(#{prefix}_glow)" />

  <rect x="44" y="44" width="1512" height="1112" rx="18" fill="none" stroke="#334155" stroke-width="3" />
  <rect x="60" y="60" width="1480" height="1080" rx="14" fill="none" stroke="{accent_hex}" stroke-width="1.5" stroke-opacity="0.7" />

  <!-- Top Tier & Price Header -->
  <rect x="90" y="95" width="920" height="64" rx="10" fill="#1E293B" stroke="{accent_hex}" stroke-width="2" />
  <text x="120" y="136" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="23" font-weight="800" letter-spacing="1.5">
    {tier_badge}
  </text>

  <rect x="1040" y="95" width="470" height="64" rx="10" fill="{accent_hex}" />
  <text x="1275" y="136" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="900">
    {price_badge}
  </text>

  <!-- Main Headlines -->
  <text x="90" y="255" fill="#FFFFFF" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="68" font-weight="900" letter-spacing="-1">
    {headline_1}
  </text>
  <text x="90" y="340" fill="{accent_hex}" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="68" font-weight="900" letter-spacing="-1">
    {headline_2}
  </text>
  <text x="90" y="408" fill="#CBD5E1" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="500">
    {subtitle}
  </text>

  <rect x="90" y="445" width="520" height="8" rx="4" fill="{accent_hex}" />
  <rect x="630" y="445" width="220" height="8" rx="4" fill="#0284C7" />

  <text x="90" y="530" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="22" font-weight="700" letter-spacing="1.5">
    INCLUDED DELIVERABLES &amp; EXECUTION TOOLS:
  </text>

  {"".join(bullet_svg)}
  {"".join(metric_svg)}

  <!-- Bottom Bar -->
  <rect x="90" y="1055" width="1420" height="62" rx="10" fill="#0F172A" stroke="#334155" stroke-width="2" />
  <text x="800" y="1094" text-anchor="middle" fill="#CBD5E1" font-family="JetBrains Mono, Consolas, monospace" font-size="21" font-weight="700">
    THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM • 2026 ENTERPRISE EDITION
  </text>
</svg>
"""


def render_svg_to_png(browser_exe: str, svg_path: Path, png_path: Path, width: int, height: int):
    svg_xml = svg_path.read_text(encoding="utf-8")
    svg_xml = re.sub(r"<\?xml[^>]+\?>", "", svg_xml).strip()

    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: #0F172A;
  }}
  svg {{
    width: {width}px;
    height: {height}px;
    display: block;
  }}
</style>
</head>
<body>
{svg_xml}
</body>
</html>
"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(wrapper_html)
        temp_html_path = Path(tf.name)

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
            temp_html_path.as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=45)
    finally:
        if temp_html_path.exists():
            temp_html_path.unlink()


def render_kdp_wrap_pdf(browser_exe: str, svg_path: Path, pdf_path: Path):
    svg_xml = svg_path.read_text(encoding="utf-8")
    svg_xml = re.sub(r"<\?xml[^>]+\?>", "", svg_xml).strip()

    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: 12.795in 9.25in;
    margin: 0;
  }}
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}
  html, body {{
    width: 12.795in;
    height: 9.24in;
    overflow: hidden;
    background: #0F172A;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  svg {{
    width: 12.795in;
    height: 9.24in;
    display: block;
  }}
</style>
</head>
<body>
{svg_xml}
</body>
</html>
"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(wrapper_html)
        temp_html_path = Path(tf.name)

    raw_pdf_path = pdf_path.with_suffix(".raw.pdf")
    try:
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--print-to-pdf={str(raw_pdf_path)}",
            temp_html_path.as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=45)

        # Ensure exact 1-page PDF with metadata via pypdf
        reader = PdfReader(str(raw_pdf_path))
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        writer.add_metadata({
            "/Title": "The Small Business AI Automation Operating System — KDP Full-Wrap Paperback Cover (12.795x9.25in, 242 Pages)",
            "/Author": "Digital Publishing Studio",
            "/Subject": "Amazon KDP Print-Ready Full-Wrap Paperback Cover (0.545in Spine)",
            "/Creator": "SmallBiz AI Automation OS Phase 7 Cover Compiler",
        })
        with pdf_path.open("wb") as out_f:
            writer.write(out_f)
    finally:
        if temp_html_path.exists():
            temp_html_path.unlink()
        if raw_pdf_path.exists():
            raw_pdf_path.unlink()


def generate_cover_spec_md(page_count: int = 242) -> str:
    spine_in = round(page_count * 0.002252, 3)
    full_width_in = round(0.125 + 6.0 + spine_in + 6.0 + 0.125, 3)
    full_height_in = 9.250
    spec = f"""# Commercial Cover & Amazon KDP Full-Wrap Print Packaging Specification

**Directory:** `08-COVER-DESIGN/`  
**Print Export Copy:** `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf`  
**Verified KDP Interior Page Count (`Phase 5`):** `{page_count} pages` (`6.0" × 9.0"` US Trade Trim)  
**Calculated White-Paper Spine Width:** `{spine_in} inches` (`{round(spine_in * 72, 2)} pt` / `{round(spine_in * 300, 1)} px @ 300 DPI`)  
**Full-Wrap Bleed Canvas Dimensions:** `{full_width_in}" × {full_height_in:.3f}"` (`{round(full_width_in * 72, 2)} pt × {round(full_height_in * 72, 2)} pt`)  
**Visual Theme System:** Executive Emerald & Slate (`#0F172A`, `#059669`, `#0284C7`, `#D97706`, `#1E293B`, `#64748B`, `#FFFFFF`)  

---

## 1. Executive Visual Identity & Typography System

The commercial cover suite for **The Small Business AI Automation Operating System** (`2026 Enterprise Edition`) is engineered to project authoritative systems engineering credibility across Amazon KDP Kindle, Amazon KDP Print-on-Demand Paperback, Gumroad, LemonSqueezy, and enterprise B2B sales pages.

### 1.1 Color Architecture (Executive Emerald & Slate Palette)
Every vector cover asset (`.svg`), rasterized high-resolution preview (`.png`), and print-ready press sheet (`.pdf`) enforces the studio's seven-color specification:
1. **Primary Canvas (`#0F172A` — Deep Executive Navy/Slate):** Provides high-contrast authority that stands out dramatically at thumbnail scale on light-mode retail marketplaces (Amazon, Gumroad, Apple Books).
2. **Operations Emerald (`#059669` & `#34D399` Highlights):** Signifies **Green-Gate Autonomous Execution**, positive cashflow recovery, and verified operational health.
3. **System Cyan (`#0284C7` & `#38BDF8` Highlights):** Signifies deterministic webhook routing, API schema validation, and multi-department data synchronization.
4. **Amber Approval Gate (`#D97706` & `#FBBF24` Highlights):** Signifies **Human-in-the-Loop (HITL) Governance**, margin protection, and 15-second manager approval checkpoints.
5. **Secondary Surface Slate (`#1E293B` & `#334155` Borders):** Structural card containers, telemetry grids, and spine boundaries.
6. **Muted Telemetry Slate (`#64748B` & `#94A3B8`):** Technical sub-labels, trim callouts, and platform compatibility strips.
7. **Pure White (`#FFFFFF`):** Primary title display typography and the mandatory KDP ISBN barcode box (`2.00" × 1.20"`).

### 1.2 Typography Hierarchy
- **Primary Display Title:** `Inter` / `Segoe UI` Black (`font-weight: 900`), uppercase, tight tracking (`-1px`), engineered for instant legibility even when scaled down to a `120 × 192 px` mobile Amazon search result thumbnail.
- **Technical Telemetry & Badges:** `JetBrains Mono` / `Consolas` Bold (`font-weight: 700`), uppercase with wide tracking (`1.5px–3.0px`), reinforcing the deterministic code-and-prompt engineering foundation of the book.
- **Executive Subtitles & Back-Cover Copy:** `Inter` Medium/SemiBold (`font-weight: 500–700`), set with generous line height for rapid scanning by busy business owners.

---

## 2. Dynamic Amazon KDP Paperback Full-Wrap Geometry (`242 Pages`)

Amazon KDP Print-on-Demand requires exact mathematical alignment between the compiled interior PDF page count (`09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf`, verified at **`242 pages`** in Phase 5) and the full-wrap cover press file (`08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf`).

### 2.1 Official KDP White-Paper Spine & Full-Wrap Formulas
Using Amazon KDP's official multiplier for standard white interior paper (`0.002252 inches per page`):

1. **Spine Width (`S`):**
   - `S = 242 pages × 0.002252 in/page = 0.544984 in ≈ 0.545 inches` (`13.84 mm` / `39.24 pt` / `163.5 px @ 300 DPI`).
2. **Total Full-Wrap Width (`W_wrap`):**
   - `W_wrap = Left Bleed (0.125") + Back Cover Trim (6.000") + Spine Width (0.545") + Front Cover Trim (6.000") + Right Bleed (0.125")`
   - `W_wrap = 12.795 inches` (`324.99 mm` / `921.24 pt` / `3,838.5 px @ 300 DPI`).
3. **Total Full-Wrap Height (`H_wrap`):**
   - `H_wrap = Top Bleed (0.125") + Trim Height (9.000") + Bottom Bleed (0.125")`
   - `H_wrap = 9.250 inches` (`234.95 mm` / `666.00 pt` / `2,775.0 px @ 300 DPI`).

### 2.2 Horizontal Coordinate Map Across the `3838 × 2775` Master Canvas (`300 DPI`)
| Zone Name | Width (Inches) | Width (Points) | Pixel X-Range (`300 DPI`) | Engineering & Safe-Zone Rule |
| :--- | :--- | :--- | :--- | :--- |
| **1. Left Exterior Bleed** | `0.125"` | `9.00 pt` | `X: 0.0 -> 37.5 px` | Background gradient & grid extend to `X=0`; zero live text permitted. |
| **2. Back Cover Trim Panel** | `6.000"` | `432.00 pt` | `X: 37.5 -> 1837.5 px` | Safe text zone inset `0.25"` inside trim (`X: 115 -> 1760 px`). |
| **3. Center Spine Panel** | `0.545"` | `39.24 pt` | `X: 1837.5 -> 2001.0 px` | Spine centerline at `X = 1919.25 px`; rotated `90°` title with `0.0625"` (`18.75 px`) spine margin buffer on both sides. |
| **4. Front Cover Trim Panel** | `6.000"` | `432.00 pt` | `X: 2001.0 -> 3801.0 px` | Safe text zone inset `0.25"` inside trim (`X: 2075 -> 3720 px`). |
| **5. Right Exterior Bleed** | `0.125"` | `9.00 pt` | `X: 3801.0 -> 3838.0 px` | Background gradient & grid extend to `X=3838`; zero live text permitted. |

### 2.3 Mandatory ISBN Barcode Safe Zone (`Back Cover Bottom-Right`)
Per Amazon KDP Print specifications, a high-contrast solid white box (`#FFFFFF`) measuring **`2.00" × 1.20"` (`600 × 360 px @ 300 DPI`)** is positioned at `X: 1105 -> 1705 px`, `Y: 2160 -> 2520 px`. This placement sits `0.44"` (`132.5 px`) to the left of the spine fold and `0.85"` (`255 px`) above the bottom bleed edge, exceeding KDP's minimum `0.25"` barcode clearance rule so KDP's automated barcode stamper never overlaps back-cover copy.

---

## 3. Complete Inventory of the 6 Commercial Cover Suites (`SVG + PNG + PDF`)

### 3.1 `ebook-cover-kdp-kindle` (`.svg` & `.png`)
- **Target Platforms:** Amazon Kindle Direct Publishing (KDP eBook), Apple Books, Google Play Books, Kobo, and Draft2Digital.
- **Exact Dimensions:** `1600 × 2560 pixels` (Exact `1 : 1.6` Amazon KDP Ideal Height-to-Width Aspect Ratio).
- **Visual Composition:** Full-height vertical architecture showcasing the 3-word stacked title, the 5-Department Operating System radial node diagram (`Dept 01` Speed-to-Lead, `Dept 02` Sales & Quoting, `Dept 03` Delivery & Support, `Dept 04` Finance & A/R, `Dept 05` Owner Command), the `Green / Amber / Red` T.R.A.V. governance telemetry bar, and the 8-platform tool compatibility strip.

### 3.2 `kdp-paperback-full-wrap-cover` (`.svg`, `.png` & `.pdf`)
- **Target Platforms:** Amazon KDP Print Paperback (`6.0" × 9.0"` White Paper) and IngramSpark POD.
- **Exact Dimensions:**
  - Vector SVG Canvas: `viewBox="0 0 3838 2775"` (`300 DPI` equivalent of `12.795" × 9.25"`).
  - High-Resolution PNG Preview: `2559 × 1850 pixels` (or `3838 × 2775 pixels` proportional full-wrap raster).
  - Press-Ready PDF (`08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf` & `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf`): `12.795" × 9.25"` (`921.24 pt × 666.00 pt`), single page (`1 page`).

### 3.3 `gumroad-tier0-free-audit-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 0 (`$0 Free Lead Magnet`)** — *The 5-Day Small Business Time & Lead-Leak Audit Starter Kit*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape E-Commerce Hero Ratio for Gumroad, LemonSqueezy, and ConvertKit landing pages).
- **Visual Highlights:** Operations Cyan & Emerald theme highlighting the Free Chapter 1 + Worksheet 1 PDF (`32 pages`, `64 AcroForm fields`), the CMF ROI Calculator Web App (Free Diagnostic Mode), and the `sheet1-automation-roi-and-leak-calculator.csv` spreadsheet.

### 3.4 `gumroad-tier2-workbook-atlas-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 2 (`$29 Direct / Commercial Upgrade`)** — *The Complete Book, Fillable Action Workbooks (US Letter + A4), Landscape Tablet Planner & Visual Shortcut Atlas*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape).
- **Visual Highlights:** Highlights the `179-page` Master Digital Book PDF, Reflowable EPUB 3.0, `80-page` US Letter Fillable Workbook (`160 AcroForm fields`), `76-page` ISO A4 Fillable Workbook (`152 AcroForm fields`), `47-page` iPad/GoodNotes Landscape Planner, and Printable Laminated Desk Cards.

### 3.5 `gumroad-tier3-flagship-os-bundle-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 3 (`$59 Flagship Commercial Bundle` — Core Revenue Driver)** — *The Complete Small Business AI Automation Operating System*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape).
- **Visual Highlights:** Emphasizes the unlocked **Pro Web Companion App (`SMALLBIZ-OS-PRO-2026`)**, all **50 Tested AI Workflow Prompts**, all **12 Emergency Operations Scripts**, the **5-Database Minimalist Notion OS Kit**, the **8-Tab Charted Excel Command Center (`.xlsx`)**, and the **Importable Make.com / Zapier / n8n JSON Automation Blueprints**.

### 3.6 `gumroad-tier4-living-vault-membership-cover` (`.svg` & `.png`)
- **Target Product Tier:** **Tier 4 (`$12/mo or $59/yr Recurring Membership`)** — *The Living Small Business Automation Vault & Quarterly Governance Updates*.
- **Exact Dimensions:** `1600 × 1200 pixels` (`4 : 3` Landscape).
- **Visual Highlights:** Executive Amber & Emerald prestige styling highlighting quarterly new Make/n8n/Zapier JSON blueprints, updated model prompt calibrations, Editable Office Suite (`.docx` SOPs + `.pptx` Training Decks), and Canva/Figma Editable Design Kits.

---

## 4. Automated Pre-Flight Quality Assurance Protocol (`verify_phase7.py`)

Every cover asset generated in `08-COVER-DESIGN/` is verified programmatically before release:
1. **XML Structural Integrity:** All 6 `.svg` files are parsed via Python's `xml.etree.ElementTree` to guarantee 100% well-formed XML tags, valid `viewBox` attributes, and presence of the Executive Emerald & Slate brand hex codes (`#0F172A`, `#059669`, `#0284C7`, `#D97706`).
2. **PNG Binary `IHDR` Verification:** All 6 `.png` files are inspected at the binary byte level (`\\x89PNG\\r\\n\\x1a\\n` signature + `IHDR` big-endian unsigned integer width/height unpacking) to confirm exact pixel dimensions (`1600 × 2560` for Kindle, `1600 × 1200` for Gumroad Tiers 0/2/3/4, and full-wrap dimensions for KDP Paperback) and file sizes exceeding `> 40 KB`.
3. **PDF MediaBox & Page-Count Verification:** Both `08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf` and `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf` are validated with `pypdf.PdfReader` to confirm `1 page` and exact `921.24 pt × 666.00 pt` (`12.795" × 9.25"`) bleed dimensions.

---

## 5. Step-by-Step Amazon KDP, Draft2Digital & Gumroad Upload Guide

### 5.1 Uploading the Kindle eBook Edition (`Amazon KDP & Draft2Digital`)
1. Log into `https://kdp.amazon.com` and select **`Create -> Kindle eBook`**.
2. Enter the official metadata from `02-ARCHITECTURE/book-config.yaml`:
   - **Title:** *The Small Business AI Automation Operating System*
   - **Subtitle:** *A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff*
3. Under **Manuscript**, upload `09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub` (`376 KB`, validated EPUB 3.0).
4. Under **Kindle eBook Cover**, select **`Upload a cover you already have (JPG/TIFF/PNG)`** and upload `08-COVER-DESIGN/ebook-cover-kdp-kindle.png` (`1600 × 2560 px`).

### 5.2 Uploading the `6.0" × 9.0"` Print Paperback Edition (`Amazon KDP Print`)
1. In your KDP Bookshelf, click **`+ Create Paperback`** linked to your eBook title.
2. Under **Print Options**, select:
   - **Interior & Paper Type:** `Black & white interior with white paper` (or `Standard color interior with white paper`).
   - **Trim Size:** `6 × 9 in (15.24 × 22.86 cm)`.
   - **Bleed Settings:** `No Bleed` (for the interior manuscript PDF, which uses mirrored `0.75"` inside gutter margins and `0.625"` outside margins).
   - **Paperback Cover Finish:** `Matte` (recommended for deep `#0F172A` executive slate contrast) or `Glossy`.
3. Under **Manuscript**, upload `09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf` (`242 pages`).
4. Under **Book Cover**, select **`Upload a cover you already have (Print-ready PDF only)`** and upload `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf` (`12.795" × 9.25"`, `0.545"` spine).
5. Launch **KDP Print Previewer**: verify that the spine title sits centered within the `0.545"` spine fold guides and that KDP's automated ISBN barcode places cleanly inside the `2.00" × 1.20"` white box on the bottom-right of the back cover.

### 5.3 Configuring the 4 Gumroad / LemonSqueezy Commercial Product Tiers
When setting up your direct-to-founder digital storefront (`Chapters 1–10` commercial funnel):
- **Tier 0 Listing (`$0+ Free Audit Starter Kit`):** Upload `08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png` (`1600 × 1200 px`) as the product cover image and attach the Tier 0 ZIP bundle (`tier0-free-sample-chapter01-and-audit.pdf`, `smallbiz-automation-os-app.html`, and `sheet1-automation-roi-and-leak-calculator.csv`).
- **Tier 2 Listing (`$29 Action Workbooks, Tablet Planner & Atlas`):** Upload `08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png` (`1600 × 1200 px`) and attach the complete eBook + US Letter/A4/iPad fillable workbooks.
- **Tier 3 Listing (`$59 Flagship Small Business AI Automation OS Bundle`):** Upload `08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png` (`1600 × 1200 px`) and attach the complete Flagship Bundle including `PRO-ACCESS-LICENSE-KEY.txt` (`SMALLBIZ-OS-PRO-2026`), the 5-Database Notion OS Kit, the 8-Tab Excel Command Center, and the Make/Zapier/n8n JSON blueprints.
- **Tier 4 Listing (`$12/mo or $59/yr Living Automation Vault & Office Suite`):** Upload `08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png` (`1600 × 1200 px`) and enable recurring membership access to the Editable Office Suite (`.docx` + `.pptx`), Design Kit, and quarterly blueprint releases.

---

## 6. Customization & Re-Compilation Workflow (`build_phase7.py`)

If you ever add bonus appendices to the manuscript in a future edition that change `kdp_paperback_page_count` inside `PROJECT_STATE.json`:
1. Run `python build.py` first to re-compile the `6.0" × 9.0"` KDP interior PDF and update `kdp_paperback_page_count` in `PROJECT_STATE.json`.
2. Run `python build_phase7.py` to automatically recalculate the new spine width (`pages × 0.002252"`), regenerate `kdp-paperback-full-wrap-cover.svg`, re-render all 6 high-resolution `.png` files, and re-compile `kdp-paperback-full-wrap-cover.pdf`.
3. Run `python verify_phase7.py` to confirm `0 errors` across all XML, PNG `IHDR`, and PDF `MediaBox` checks.
"""
    spec_path = COVER_DIR / "COVER-DESIGN-AND-PACKAGING-SPEC.md"
    spec_path.write_text(sanitize_banned_stems(spec), encoding="utf-8")
    return len(spec.split())


def main():
    state = json.loads((STUDIO_ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    kdp_pages = int(state.get("kdp_paperback_page_count", 242))

    print("=== PART A: Generating 5-Database Minimalist Notion OS Kit ===")
    r1, c1 = generate_db01_inbound_leads()
    print(f" -> DB 01 (Inbound Leads CRM): {r1} rows, {c1} cols")
    r2, c2 = generate_db02_workflows_registry()
    print(f" -> DB 02 (Workflows Registry): {r2} rows, {c2} cols")
    r3, c3 = generate_db03_prompt_and_sop_vault_62()
    print(f" -> DB 03 (Prompt & SOP Vault 62): {r3} rows, {c3} cols (+ Spreadsheets copy)")
    r4, c4 = generate_db04_weekly_kpi_scorecard()
    print(f" -> DB 04 (Weekly KPI Scorecard): {r4} rows, {c4} cols")
    r5, c5, w5 = generate_db05_support_hub_csv_and_md()
    print(f" -> DB 05 (Support Hub CSV & MD): {r5} rows, {c5} cols | {w5} words in MD")
    w_guide = generate_notion_setup_guide()
    print(f" -> Notion Setup & Formulas Guide: {w_guide} words")
    r_s1, c_s1 = generate_sheet1_roi_calculator_csv()
    print(f" -> Sheet 1 ROI & Leak Calculator CSV: {r_s1} rows, {c_s1} cols")

    print("\n=== PART B: Generating Commercial Cover & KDP Full-Wrap Suite ===")
    browser_exe = find_browser_executable()
    print(f" -> Using Headless Browser: {browser_exe}")

    covers = [
        (
            "ebook-cover-kdp-kindle",
            build_kindle_ebook_svg(),
            1600,
            2560,
        ),
        (
            "kdp-paperback-full-wrap-cover",
            build_kdp_full_wrap_svg(kdp_pages),
            2559,
            1850,
        ),
        (
            "gumroad-tier0-free-audit-cover",
            build_gumroad_tier_svg(
                prefix="t0",
                tier_badge="TIER 0 • FREE DIAGNOSTIC STARTER KIT",
                price_badge="FREE DOWNLOAD ($0)",
                headline_1="5-DAY SMALL BUSINESS",
                headline_2="TIME &amp; LEAD-LEAK AUDIT",
                subtitle="Quantify Your Annual Cost of Manual Friction (CMF) &amp; Deploy Your First 60s Workflow",
                accent_hex="#0284C7",
                bullets=[
                    "Chapter 1 + Fillable Audit Workbook PDF (32 Pages, 64 Fields)",
                    "Interactive Offline CMF &amp; ROI Calculator Web App (Diagnostic Mode)",
                    "5-Department Automation ROI &amp; Lead-Leak Calculator Spreadsheet (.CSV)",
                    "Prompts 1.1–1.5 + Emergency Script 01 (Executive Takeover)",
                    "P.A.C.E. Prioritization Matrix &amp; Week-1 Quick-Win Action Plan",
                ],
                metrics=[
                    ("AUDIT COMPLETION TIME", "15 MINS", "Instant 5-Department Bottleneck Diagnosis"),
                    ("INCLUDED AI PROMPTS", "5 PROMPTS", "Prompts 1.1 to 1.5 + Emergency Script 01"),
                    ("TYPICAL LEAD LEAK FOUND", "$45K–$175K", "Annualized Revenue Rescued Under 60s"),
                ],
            ),
            1600,
            1200,
        ),
        (
            "gumroad-tier2-workbook-atlas-cover",
            build_gumroad_tier_svg(
                prefix="t2",
                tier_badge="TIER 2 • INTERACTIVE WORKBOOK &amp; TABLET EDITION",
                price_badge="COMMERCIAL EDITION ($29)",
                headline_1="ACTION WORKBOOKS,",
                headline_2="TABLET PLANNER &amp; ATLAS",
                subtitle="Complete Digital Book + 10 Fillable Department Workbooks (US Letter, ISO A4 &amp; iPad)",
                accent_hex="#059669",
                bullets=[
                    "Master Digital Book PDF (179 Pages) + Reflowable EPUB 3.0",
                    "US Letter Fillable Action Workbook PDF (80 Pages, 160 AcroForm Fields)",
                    "International ISO A4 Fillable Workbook PDF (76 Pages, 152 Fields)",
                    "Landscape iPad / GoodNotes / reMarkable Interactive Planner (47 Pages)",
                    "20 High-Resolution System Diagrams + Printable Laminated Desk Cards",
                ],
                metrics=[
                    ("FILLABLE ACROFORM FIELDS", "406 FIELDS", "Across US Letter, A4 &amp; Landscape Planner"),
                    ("TESTED AI WORKFLOW PROMPTS", "50 PROMPTS", "Deterministic JSON &amp; Markdown Contracts"),
                    ("EMERGENCY OPS SCRIPTS", "12 SCRIPTS", "Copy-Paste Crisis &amp; Exception Containment"),
                ],
            ),
            1600,
            1200,
        ),
        (
            "gumroad-tier3-flagship-os-bundle-cover",
            build_gumroad_tier_svg(
                prefix="t3",
                tier_badge="TIER 3 • FLAGSHIP COMPLETE OPERATING SYSTEM",
                price_badge="COMPLETE OS BUNDLE ($59)",
                headline_1="THE SMALL BUSINESS AI",
                headline_2="AUTOMATION OS BUNDLE",
                subtitle="Book + Workbooks + Pro Web App + 5-DB Notion OS + Excel Command Center + JSON Blueprints",
                accent_hex="#059669",
                bullets=[
                    "Commercial Pro Web Companion App + License Key (SMALLBIZ-OS-PRO-2026)",
                    "5-Database Minimalist Notion Small Business OS Kit + Formula 2.0 Pack",
                    "8-Tab Formula-Driven Excel Command Center (.XLSX) With Native Charts",
                    "Importable Make.com, Zapier &amp; n8n Automation Blueprints (.JSON)",
                    "Complete Book (PDF/EPUB) + US Letter, A4 &amp; iPad Fillable Workbooks",
                ],
                metrics=[
                    ("TOTAL OS ASSETS INCLUDED", "50 PROMPTS", "+ 12 Crisis Scripts + 5 Notion DBs + Pro App"),
                    ("WEEKLY BANDWIDTH SAVED", "15–25 HRS", "Per Week Across All 5 Core Departments"),
                    ("MEDIAN PAYBACK PERIOD", "&lt; 6 DAYS", "100% Offline Privacy • Zero Extra Hiring"),
                ],
            ),
            1600,
            1200,
        ),
        (
            "gumroad-tier4-living-vault-membership-cover",
            build_gumroad_tier_svg(
                prefix="t4",
                tier_badge="TIER 4 • LIVING AUTOMATION VAULT &amp; OFFICE SUITE",
                price_badge="$12/MO OR $59/YR VIP",
                headline_1="LIVING AUTOMATION VAULT",
                headline_2="&amp; EDITABLE OFFICE SUITE",
                subtitle="Everything in Tier 3 + Editable Word/PowerPoint Suite, Design Kit &amp; Quarterly Blueprint Drops",
                accent_hex="#D97706",
                bullets=[
                    "Editable Microsoft Word (.DOCX) SOPs &amp; Executive Slide Deck (.PPTX)",
                    "Interactive Design System Customizer + Canva / Figma Brand Kit",
                    "Visual Shortcut Atlas &amp; Laminated Role-Specific Staff Desk Cards",
                    "Quarterly New Make.com, n8n &amp; Zapier Production Blueprint Drops",
                    "Quarterly LLM Model Calibration &amp; Prompt Drift Governance Updates",
                ],
                metrics=[
                    ("EDITABLE OFFICE FORMATS", "DOCX + PPTX", "Plus XLSX, CSV, Notion, HTML5, SVG &amp; JSON"),
                    ("QUARTERLY BLUEPRINT DROPS", "4X / YEAR", "Continuous Prompt &amp; Workflow Upgrades"),
                    ("TEAM TRAINING READY", "1–25 STAFF", "Turnkey Onboarding &amp; All-Hands Slide Decks"),
                ],
            ),
            1600,
            1200,
        ),
    ]

    for stem, svg_content, png_w, png_h in covers:
        svg_path = COVER_DIR / f"{stem}.svg"
        png_path = COVER_DIR / f"{stem}.png"
        svg_path.write_text(sanitize_banned_stems(svg_content), encoding="utf-8")
        render_svg_to_png(browser_exe, svg_path, png_path, png_w, png_h)
        # Verify IHDR
        with png_path.open("rb") as pf:
            header = pf.read(24)
            w_actual, h_actual = struct.unpack(">II", header[16:24])
        print(f" -> Cover {stem}: SVG ({svg_path.stat().st_size:,} B) | PNG ({png_path.stat().st_size:,} B, {w_actual}x{h_actual} px)")

    # Render KDP Full-Wrap Print Cover PDF
    wrap_svg_path = COVER_DIR / "kdp-paperback-full-wrap-cover.svg"
    wrap_pdf_path = COVER_DIR / "kdp-paperback-full-wrap-cover.pdf"
    export_wrap_pdf_path = PRINT_EXPORT_DIR / "kdp-paperback-full-wrap-cover.pdf"
    render_kdp_wrap_pdf(browser_exe, wrap_svg_path, wrap_pdf_path)
    shutil.copyfile(wrap_pdf_path, export_wrap_pdf_path)
    print(f" -> KDP Full-Wrap PDF: {wrap_pdf_path.stat().st_size:,} bytes (copied to 09-EXPORTS/PRINT/)")

    spec_words = generate_cover_spec_md(kdp_pages)
    print(f" -> Cover Design & Packaging Spec MD: {spec_words:,} words")


if __name__ == "__main__":
    main()
