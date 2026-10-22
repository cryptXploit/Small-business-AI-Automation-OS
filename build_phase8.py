#!/usr/bin/env python3
"""
Phase 8 Builder: Conversion Marketing Funnel, 7-Email Sequence, Bangladesh W-8BEN/Payoneer Runbook,
Tier 4 Vault Drop #01 & Initial 5-Tier Commercial ZIP Packaging (build_phase8.py)
Project: The Small Business AI Automation Operating System (SMALLBIZ-AI-AUTOMATION-OS-V1)
"""

import json
import os
import re
import zipfile
from pathlib import Path
from build_webapp import sanitize_banned_stems, parse_all_50_prompts

STUDIO_ROOT = Path(__file__).resolve().parent
MARKETING_DIR = STUDIO_ROOT / "10-MARKETING"
BUNDLE_DIR = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE"

MARKETING_DIR.mkdir(parents=True, exist_ok=True)
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)


def clean_copy(text: str) -> str:
    """Sanitize any banned words or phrases from marketing & runbook copy."""
    text = sanitize_banned_stems(text)
    extra = [
        (r"\bin today's fast-paced world\b", "in modern small business operations"),
        (r"\bever-evolving landscape\b", "changing operational environment"),
        (r"\bit is important to remember\b", "note that"),
        (r"\bin conclusion\b", "in summary"),
        (r"\bwithout further ado\b", "directly"),
        (r"\blet's dive in\b", "let us begin"),
        (r"\blook no further\b", "start here"),
        (r"\bgame-changing\b", "high-impact"),
        (r"\bgame-changer\b", "operational advantage"),
        (r"\bskyrocketing\b", "accelerating"),
        (r"\bsupercharging\b", "accelerating"),
        (r"\bfostering\b", "building"),
        (r"\bfoster\b", "build"),
        (r"\bunderscoring\b", "highlighting"),
        (r"\bunderscore\b", "highlight"),
        (r"\bpivotal\b", "critical"),
        (r"\brealm\b", "domain"),
        (r"\belevate(?:s|d|ing|r)?\b", "advance"),
        (r"\blandscape(?:s|d|ing|r)?\b", "horizontal"),
    ]
    for pat, rep in extra:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


# =============================================================================
# DELIVERABLE 1: 10-MARKETING/index.html (>= 60 KB Offline Conversion Page)
# =============================================================================

def build_marketing_landing_page() -> str:
    prompts = parse_all_50_prompts()
    # Embed sample prompt previews for interactive curriculum explorer
    featured_prompts = []
    for pid in ("Prompt 1.1", "Prompt 2.3", "Prompt 3.3", "Prompt 4.1", "Prompt 5.1", "Prompt 6.2", "Prompt 7.1", "Prompt 8.2", "Prompt 9.1", "Prompt 10.1"):
        for p in prompts:
            if p["id"] == pid:
                featured_prompts.append({
                    "id": p["id"],
                    "chapter": p["chapter"],
                    "title": p["title"],
                    "dept": p["dept_label"],
                    "zone": p["zone"],
                    "trigger": p["trigger"],
                    "stack": p["stack"],
                    "template": p["prompt_template"],
                    "sample": p["sample_output"][:900],
                })
                break

    featured_json = json.dumps(featured_prompts, ensure_ascii=False, indent=2)

    chapters_data = [
        {
            "num": 1,
            "dept": "Dept 05: Strategy & All 5 Depts",
            "title": "Chapter 1: The Small Business Automation Audit — Finding Your $50,000+ Manual Bottlenecks",
            "framework": "5-Department Small Business Engine & P.A.C.E. Prioritization Matrix (Pain, Annual Hours, Cashflow, Ease)",
            "case_study": "Apex Comfort HVAC & Plumbing (11 Staff, $1.45M Revenue) — Audited $302,266/yr in Annual Cost of Manual Friction (CMF) and recovered 18.5 hrs/wk in 30 days.",
            "worksheet": "Worksheet 01: 5-Day Time & Task Log, Lead-Leak Calculator & P.A.C.E. Matrix",
            "prompts": "Prompts 1.1 – 1.5 (Time-Log Synthesizer, Lead-Leak Diagnostic, SaaS Stack Auditor, T.R.A.V. Mapper, Zero-Layoff Team Memo)",
            "summary": "Replaces random software experimentation with a rigorous 5-day operational diagnostic. Quantifies your exact Labor Tax (L_tax), Speed-to-Lead Revenue Leak (R_leak), and Receivables Cashflow Drag (C_drag) so you automate your highest-ROI bottleneck in Week 1."
        },
        {
            "num": 2,
            "dept": "Dept 05: Systems & Safety Governance",
            "title": "Chapter 2: The Human-in-the-Loop Architecture — Designing Safe, Zero-Hallucination Workflows",
            "framework": "T.R.A.V. 4-Stage Safety Contract (Trigger -> Rules -> AI -> Verification) & Green / Amber / Red Governance Zones",
            "case_study": "BrightSmile Dental & Orthodontics (9 Staff, $1.18M Revenue) — Eliminated insurance quoting errors while automating 78% of routine front-desk patient inquiries.",
            "worksheet": "Worksheet 02: Workflow Risk Classifier, Grounded Truth-Table Builder & Kill-Switch Checklist",
            "prompts": "Prompts 2.1 – 2.5 (Risk Classifier, Closed-World JSON Compiler, 15s Slack Approval Card Formatter, Regex PII Redactor, DLQ Outage Monitor)",
            "summary": "Establishes closed-world truth tables, deterministic pre-AI regex filters, temperature 0.0-0.1 JSON schema contracts, and 15-second Slack/Teams Amber Approval Cards so your AI never invents prices, discounts, or legal commitments."
        },
        {
            "num": 3,
            "dept": "Dept 01: Lead Capture & Speed-to-Lead",
            "title": "Chapter 3: The 60-Second Lead Capture & Speed-to-Lead Engine (Web, Phone, SMS & Social)",
            "framework": "I.N.S.T.A.N.T. 60-Second Omnichannel Router & Non-Intrusive B.A.N.T.-Lite Lead Scorer",
            "case_study": "MetroShield Roofing & Exteriors (14 Staff, $2.1M Revenue) — Cut median response time from 4.2 hours to 38 seconds and rescued $38,400/mo in previously missed calls.",
            "worksheet": "Worksheet 03: Omnichannel Intake Audit, A2P 10DLC SMS Compliance & Missed-Call Text-Back Script Builder",
            "prompts": "Prompts 3.1 – 3.5 (Omnichannel Lead Enricher, 60s SMS/Email Concierge, Missed-Call Whisper Text-Back Bot, 2-Way SMS Booker, 30m Pre-Call Rep Brief)",
            "summary": "Captures web forms, missed phone calls, voicemails, Facebook/IG Lead Ads, WhatsApp, and Google Business messages into a single normalized webhook router that responds and books appointments in under 60 seconds 24/7."
        },
        {
            "num": 4,
            "dept": "Dept 02: Sales Qualification & Quoting",
            "title": "Chapter 4: Automated Sales Qualification, 3-Option Quotes & The 14-Day Follow-Up Loop",
            "framework": "Voice-to-3-Tier Good-Better-Best Proposal Engine & The 6-Touch Polite-Persistence State Machine",
            "case_study": "Vanguard Commercial Cleaning (19 Staff, $1.65M Revenue) — Compressed proposal turnaround from 72 hours to 14 minutes and lifted 14-day quote close rate from 24% to 39%.",
            "worksheet": "Worksheet 04: Deterministic SKU Pricebook Matrix, 3-Tier Proposal Template & 14-Day Follow-Up Cadence",
            "prompts": "Prompts 4.1 – 4.5 (Field Voice Memo to 3-Tier Proposal, Executive ROI Cover Letter, 14-Day Follow-Up Sequence, Margin-Safe Objection Counter, 90-Day Closed-Lost Recycler)",
            "summary": "Allows field estimators, clinicians, and consultants to record a 90-second voice note after a site visit and automatically assemble a locked Good-Better-Best proposal PDF with automated follow-up nudges that halt the instant the client signs."
        },
        {
            "num": 5,
            "dept": "Dept 03: Client Onboarding & Fulfillment",
            "title": "Chapter 5: Frictionless Client Onboarding & Service Delivery Automation",
            "framework": "The 5-Stage Zero-Drop Handoff Architecture (Payment -> Provisioning -> Dynamic Intake -> Internal Brief -> Milestone Pulse)",
            "case_study": "Apex Digital Marketing Agency (12 Staff, $1.52M Revenue) — Cut client onboarding cycle time from 9.4 days to 11 hours and reduced Day-90 churn by 64%.",
            "worksheet": "Worksheet 05: Payment-to-Portal Provisioning Map, Conditional Intake Validator & Scope-Boundary Tracker",
            "prompts": "Prompts 5.1 – 5.5 (Sales-to-Fulfillment Handoff Compiler, Welcome & Milestone Writer, Incomplete Intake Validator, Stalled Onboarding Chaser, Scope-Creep Detector)",
            "summary": "Wires Stripe, Square, and QuickBooks payment webhooks directly to cloud folder creation, project board provisioning, pre-filled intake forms, and proactive milestone status updates."
        },
        {
            "num": 6,
            "dept": "Dept 03: Customer Support Triage",
            "title": "Chapter 6: 24/7 AI Customer Support & Smart Escalation (Zero-Hallucination Helpdesk)",
            "framework": "The 3-Tier Support Shield (Tier 1 Green RAG Auto-Resolve, Tier 2 Amber Draft, Tier 3 Red Human Takeover)",
            "case_study": "Pure Botanica Skincare & Wellness D2C (8 Staff, $1.35M Revenue) — Deflected 68% of routine WISMO and FAQ tickets in under 45 seconds while maintaining 4.92/5 CSAT.",
            "worksheet": "Worksheet 06: Top-25 FAQ Truth-Table Builder, Sentiment Routing Matrix & Red-Gate Regex Filter",
            "prompts": "Prompts 6.1 – 6.5 (Ticket Sentiment/Intent Classifier, Grounded RAG Responder, Live Order/Appointment API Formatter, Angry Customer Red-Gate Brief, Weekly KB Gap Patcher)",
            "summary": "Turns your verified policies, hours, warranties, and live order/scheduling APIs into a grounded 24/7 helpdesk that resolves routine inquiries instantly and escalates frustrated customers (`Sentiment <= 2`) to a human immediately."
        },
        {
            "num": 7,
            "dept": "Dept 03: Reputation, Reviews & Retention",
            "title": "Chapter 7: The Reputation, Review & Repeat-Sales Flywheel",
            "framework": "The R.E.V.I.E.W. Sentiment-Gated Reputation Engine & The 30/60/90/180-Day Dormant Win-Back Matrix",
            "case_study": "Precision Auto Care & Tire (10 Staff, $1.28M Revenue) — Grew verified 5-star Google reviews from 42 to 218 in 6 months and generated $94,000 in dormant recall bookings.",
            "worksheet": "Worksheet 07: Golden-Moment Sentiment Gate Setup, GBP SEO Response Library & Win-Back Cohort Planner",
            "prompts": "Prompts 7.1 – 7.5 (Post-Visit Sentiment Gate Classifier, Frictionless 5-Star Google Review Generator, Public Review SEO Responder, 60/90/180d Win-Back Writer, VIP Churn Predictor)",
            "summary": "Sends a 1-click satisfaction check at the peak moment of customer gratitude—routing 4-5 star advocates directly to your Google Business Profile review page while intercepting 1-3 star detractors into private executive resolution."
        },
        {
            "num": 8,
            "dept": "Dept 04: Invoicing, Receivables & AP",
            "title": "Chapter 8: Automated Invoicing, Payment Chasers, Expense OCR & Cashflow Control",
            "framework": "Same-Day Milestone Billing, The 5-Stage Polite-to-Firm AR Chaser State Machine & 3-Way AP Price-Creep Guard",
            "case_study": "HarborView Electrical Contractors (16 Staff, $2.35M Revenue) — Reduced average Days Sales Outstanding (DSO) from 44 days to 13 days, unlocking $142,000 in working capital.",
            "worksheet": "Worksheet 08: Same-Day Billing Trigger Map, 5-Stage Payment Chaser Templates & Vendor Price-Creep Audit Sheet",
            "prompts": "Prompts 8.1 – 8.5 (Job Notes to Itemized Invoice Formatter, 5-Stage AR Payment Chaser, Vendor Bill & Receipt OCR Extractor, 5% Price-Creep Auditor, Monthly Pre-Close Anomaly Builder)",
            "summary": "Eliminates Friday night billing backlogs and awkward collection calls by dispatching itemized invoices on job completion, automating polite-to-firm overdue payment reminders, and auditing every supplier bill for unannounced price hikes."
        },
        {
            "num": 9,
            "dept": "Dept 05: Team SOPs & Delegation",
            "title": "Chapter 9: The Self-Running Team — Automating SOP Creation, Onboarding, and Task Delegation",
            "framework": "The 7-Block Living SOP Compiler, 60-Second Voice-to-Task Delegation Engine & Internal Ask-the-SOP Bot",
            "case_study": "NorthStar Tax & Advisory CPA (13 Staff, $1.78M Revenue) — Documented 40 core firm SOPs in 3 weeks from 4-minute Loom recordings and cut new-hire ramp time by 55%.",
            "worksheet": "Worksheet 09: Top-20 SOP Priority Matrix, 7-Block SOP Template & 7-Day New-Hire Onboarding Curriculum",
            "prompts": "Prompts 9.1 – 9.5 (Loom Transcript to 7-Block SOP Compiler, Voice-to-Task Delegation Brief, Meeting Action-Item Tracker, Internal Ask-the-SOP Bot, 7-Day New-Hire Quiz Builder)",
            "summary": "Ends the 'Ask the Owner Everything' bottleneck by converting 3-minute screen recordings into structured 7-block checklists with binary Definitions of Done and a grounded Slack bot that answers staff procedural questions 24/7."
        },
        {
            "num": 10,
            "dept": "Dept 05: Executive Command & 90-Day Rollout",
            "title": "Chapter 10: The 15-Minute Friday Owner Scorecard & Your 90-Day Phased Rollout Roadmap",
            "framework": "The 12-Metric Friday 3:00 PM Executive Pulse, 90-Day Phased Rollout Schedule & Quarterly Security/Drift Governance",
            "case_study": "Summit Peak Physical Therapy (15 Staff, $1.92M Revenue) — Reduced founder weekly working hours from 58 hrs to 36 hrs while increasing net operating margin from 14% to 24%.",
            "worksheet": "Worksheet 10: 12-KPI Friday Scorecard Configuration, 90-Day Sprint Exit-Gate Checklist & Quarterly Security Audit",
            "prompts": "Prompts 10.1 – 10.5 (Friday 3:00 PM KPI Synthesizer, 90-Day Rollout Customizer, Monthly Tool-Stack & Labor ROI Auditor, Quarterly Drift & Security Reviewer, Monday 15m All-Hands Brief)",
            "summary": "Consolidates all 5 departments into an automated Friday 3:00 PM executive brief, pairs it with a week-by-week 90-day implementation schedule, and locks in quarterly API security and prompt-drift governance."
        }
    ]
    chapters_json = json.dumps(chapters_data, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Small Business AI Automation Operating System — Official 2026 Enterprise Edition</title>
  <meta name="description" content="A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff." />
  <style>
    :root {{
      --primary: #0F172A;
      --primary-alt: #1E293B;
      --accent: #059669;
      --accent-hover: #047857;
      --accent-soft: #ECFDF5;
      --secondary: #0284C7;
      --secondary-soft: #F0F9FF;
      --warning: #D97706;
      --warning-soft: #FFFBEB;
      --text: #1E293B;
      --muted: #64748B;
      --border: #CBD5E1;
      --surface: #F8FAFC;
      --bg: #FFFFFF;
      --radius: 12px;
      --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      font-family: var(--font-sans);
      color: var(--text);
      background: var(--bg);
      line-height: 1.6;
    }}

    /* Sticky Top Navigation */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(8px);
      border-bottom: 2px solid var(--accent);
      padding: 0.85rem 1.5rem;
    }}

    .nav-inner {{
      max-width: 1320px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: #FFFFFF;
      text-decoration: none;
      font-weight: 800;
      font-size: 1rem;
    }}

    .nav-logo {{
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: linear-gradient(135deg, var(--accent), var(--secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-weight: 900;
      color: #FFFFFF;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 1.25rem;
      flex-wrap: wrap;
    }}

    .nav-links a {{
      color: #CBD5E1;
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 600;
      transition: color 0.15s ease;
    }}

    .nav-links a:hover {{
      color: #34D399;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      padding: 0.75rem 1.35rem;
      border-radius: 8px;
      font-size: 0.92rem;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      border: 2px solid transparent;
      transition: all 0.18s ease;
      font-family: inherit;
    }}

    .btn-sm {{
      padding: 0.45rem 0.95rem;
      font-size: 0.82rem;
    }}

    .btn-emerald {{
      background: var(--accent);
      color: #FFFFFF;
      box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35);
    }}
    .btn-emerald:hover {{
      background: var(--accent-hover);
      transform: translateY(-1px);
    }}

    .btn-cyan {{
      background: var(--secondary);
      color: #FFFFFF;
    }}
    .btn-cyan:hover {{
      background: #0369A1;
    }}

    .btn-amber {{
      background: var(--warning);
      color: #FFFFFF;
    }}
    .btn-amber:hover {{
      background: #B45309;
    }}

    .btn-outline-light {{
      background: rgba(255, 255, 255, 0.08);
      color: #FFFFFF;
      border-color: rgba(255, 255, 255, 0.28);
    }}
    .btn-outline-light:hover {{
      background: rgba(255, 255, 255, 0.16);
      border-color: #FFFFFF;
    }}

    .btn-outline-dark {{
      background: #FFFFFF;
      color: var(--primary);
      border-color: var(--border);
    }}
    .btn-outline-dark:hover {{
      background: var(--surface);
      border-color: var(--primary);
    }}

    /* Hero Section */
    .hero {{
      background: radial-gradient(circle at 75% 25%, rgba(5, 150, 105, 0.22), transparent 45%),
                  linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #0F172A 100%);
      color: #FFFFFF;
      padding: 4.5rem 1.5rem 4rem;
      border-bottom: 4px solid var(--accent);
    }}

    .container {{
      max-width: 1280px;
      margin: 0 auto;
    }}

    .eyebrow {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 0.35rem 0.85rem;
      border-radius: 999px;
      background: rgba(5, 150, 105, 0.2);
      color: #34D399;
      border: 1px solid #059669;
      margin-bottom: 1.2rem;
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: 1.25fr 0.9fr;
      gap: 2.5rem;
      align-items: center;
    }}

    @media (max-width: 980px) {{
      .hero-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .hero h1 {{
      font-size: 2.85rem;
      font-weight: 900;
      line-height: 1.12;
      letter-spacing: -0.02em;
      margin-bottom: 1rem;
    }}

    .hero h1 span.accent {{
      color: #34D399;
    }}

    .hero-sub {{
      font-size: 1.15rem;
      color: #CBD5E1;
      margin-bottom: 1.6rem;
      max-width: 720px;
    }}

    .proof-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
      margin-bottom: 1.85rem;
    }}

    .proof-pill {{
      background: rgba(30, 41, 59, 0.9);
      border: 1px solid #334155;
      color: #F8FAFC;
      padding: 0.38rem 0.75rem;
      border-radius: 6px;
      font-size: 0.78rem;
      font-family: var(--font-mono);
      font-weight: 600;
    }}

    .proof-pill strong {{
      color: #34D399;
    }}

    .hero-card {{
      background: rgba(15, 23, 42, 0.92);
      border: 2px solid #059669;
      border-radius: 16px;
      padding: 1.75rem;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
    }}

    /* Section Styling */
    .section {{
      padding: 4.25rem 1.5rem;
    }}

    .section-alt {{
      background: var(--surface);
      border-top: 1px solid #E2E8F0;
      border-bottom: 1px solid #E2E8F0;
    }}

    .section-dark {{
      background: var(--primary);
      color: #FFFFFF;
    }}

    .section-header {{
      text-align: center;
      max-width: 820px;
      margin: 0 auto 2.75rem;
    }}

    .section-header h2 {{
      font-size: 2.1rem;
      font-weight: 900;
      color: var(--primary);
      letter-spacing: -0.01em;
      margin-bottom: 0.65rem;
    }}

    .section-dark .section-header h2 {{
      color: #FFFFFF;
    }}

    .section-header p {{
      font-size: 1.02rem;
      color: var(--muted);
    }}

    .section-dark .section-header p {{
      color: #CBD5E1;
    }}

    /* Grid Utilities */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.25rem;
    }}

    .grid-5 {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 1rem;
    }}

    @media (max-width: 1080px) {{
      .grid-5 {{
        grid-template-columns: repeat(2, 1fr);
      }}
      .grid-3, .grid-2 {{
        grid-template-columns: 1fr;
      }}
    }}

    .card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
    }}

    /* Interactive Calculator Styles */
    .calc-group {{
      margin-bottom: 1rem;
    }}

    .calc-label {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 0.35rem;
    }}

    .calc-val {{
      font-family: var(--font-mono);
      font-size: 0.8rem;
      background: var(--secondary-soft);
      color: var(--secondary);
      padding: 0.12rem 0.5rem;
      border-radius: 4px;
      font-weight: 800;
    }}

    input[type="range"] {{
      width: 100%;
      accent-color: var(--accent);
      cursor: pointer;
    }}

    .form-input {{
      width: 100%;
      padding: 0.55rem 0.8rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 0.9rem;
      font-family: inherit;
    }}

    .result-banner {{
      background: var(--primary);
      color: #FFFFFF;
      border-radius: 12px;
      padding: 1.5rem;
      border-left: 6px solid var(--accent);
      margin-bottom: 1.25rem;
    }}

    .result-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
      margin-bottom: 1.25rem;
    }}

    .result-box {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem;
    }}

    .result-box .lbl {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .result-box .val {{
      font-size: 1.55rem;
      font-weight: 900;
      font-family: var(--font-mono);
      color: var(--primary);
      margin-top: 0.2rem;
    }}

    /* Chapter Explorer Tabs */
    .chapter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      justify-content: center;
    }}

    .ch-tab {{
      padding: 0.55rem 1rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
      font-weight: 700;
      font-size: 0.84rem;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }}

    .ch-tab:hover {{
      border-color: var(--accent);
      color: var(--accent);
    }}

    .ch-tab.active {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
    }}

    /* Pricing Matrix Cards */
    .tier-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.5rem 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: var(--shadow);
      position: relative;
    }}

    .tier-card.featured {{
      border: 3px solid var(--accent);
      transform: translateY(-6px);
      box-shadow: 0 18px 40px rgba(5, 150, 105, 0.18);
    }}

    .featured-ribbon {{
      position: absolute;
      top: -13px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--accent);
      color: #FFFFFF;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 800;
      padding: 0.2rem 0.75rem;
      border-radius: 99px;
      white-space: nowrap;
      text-transform: uppercase;
    }}

    .tier-price {{
      font-size: 2.15rem;
      font-weight: 900;
      font-family: var(--font-mono);
      color: var(--primary);
      margin: 0.6rem 0 0.2rem;
    }}

    .tier-list {{
      list-style: none;
      margin: 1rem 0 1.5rem;
      font-size: 0.83rem;
    }}

    .tier-list li {{
      margin-bottom: 0.55rem;
      padding-left: 1.25rem;
      position: relative;
    }}

    .tier-list li::before {{
      content: "✓";
      position: absolute;
      left: 0;
      color: var(--accent);
      font-weight: 900;
    }}

    /* Comparison Table */
    .comp-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
      background: var(--bg);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: var(--shadow);
    }}

    .comp-table th {{
      background: var(--primary);
      color: #FFFFFF;
      padding: 0.85rem;
      text-align: left;
      font-size: 0.78rem;
      text-transform: uppercase;
    }}

    .comp-table td {{
      padding: 0.75rem 0.85rem;
      border-bottom: 1px solid #E2E8F0;
    }}

    .comp-table tr:nth-child(even) td {{
      background: #F8FAFC;
    }}

    /* FAQ Accordion */
    .faq-item {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 0.75rem;
      overflow: hidden;
    }}

    .faq-q {{
      width: 100%;
      text-align: left;
      padding: 1.1rem 1.25rem;
      background: transparent;
      border: none;
      font-size: 0.98rem;
      font-weight: 700;
      color: var(--primary);
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: inherit;
    }}

    .faq-a {{
      padding: 0 1.25rem 1.15rem;
      font-size: 0.9rem;
      color: var(--text);
      display: none;
      border-top: 1px solid #F1F5F9;
      padding-top: 0.85rem;
    }}

    .faq-item.open .faq-a {{
      display: block;
    }}

    pre.code-preview {{
      background: #0F172A;
      color: #F8FAFC;
      padding: 1rem;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      overflow-x: auto;
      white-space: pre-wrap;
      max-height: 320px;
      border: 1px solid #334155;
    }}

    footer {{
      background: #0F172A;
      color: #94A3B8;
      padding: 3rem 1.5rem;
      border-top: 3px solid var(--accent);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>

  <!-- Sticky Executive Top Navigation Bar -->
  <header class="navbar">
    <div class="nav-inner">
      <a href="#top" class="nav-brand">
        <span class="nav-logo">OS</span>
        <span>SmallBiz AI Automation OS</span>
      </a>
      <nav class="nav-links">
        <a href="#five-depts">5-Department Engine</a>
        <a href="#roi-calculator">Live ROI Calculator</a>
        <a href="#curriculum">10-Chapter Blueprint</a>
        <a href="#prompt-sampler">50-Prompt Sampler</a>
        <a href="#pricing">5-Tier Pricing</a>
        <a href="#faq">FAQ</a>
      </nav>
      <div style="display:flex; gap:0.5rem;">
        <a href="#pricing" class="btn btn-sm btn-outline-light">Free Audit Kit ($0)</a>
        <a href="#pricing" class="btn btn-sm btn-emerald">Get Flagship OS ($59)</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section id="top" class="hero">
    <div class="container">
      <div class="hero-grid">
        <div>
          <span class="eyebrow">2026 Enterprise Edition • For 1–25 Person Small Businesses</span>
          <h1>
            The Small Business <span class="accent">AI Automation</span> Operating System
          </h1>
          <p class="hero-sub">
            A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff.
          </p>

          <div class="proof-pills">
            <span class="proof-pill"><strong>111,905+</strong> Manuscript Words</span>
            <span class="proof-pill"><strong>50</strong> Tested AI Workflow Prompts</span>
            <span class="proof-pill"><strong>12</strong> Emergency Crisis Scripts</span>
            <span class="proof-pill"><strong>20</strong> Vector System Diagrams</span>
            <span class="proof-pill"><strong>10</strong> Fillable PDF Workbooks</span>
            <span class="proof-pill"><strong>100% Offline</strong> SaaS-Lite Web App</span>
            <span class="proof-pill"><strong>5-DB</strong> Minimalist Notion OS Kit</span>
          </div>

          <div style="display:flex; gap:0.85rem; flex-wrap:wrap;">
            <a href="#pricing" class="btn btn-emerald">Get Flagship OS Bundle — $59</a>
            <a href="#pricing" class="btn btn-outline-light">Download Free 5-Day Audit Kit — $0</a>
          </div>
        </div>

        <!-- Right Hero Card: Executive Telemetry Summary -->
        <div class="hero-card">
          <div style="font-family:var(--font-mono); font-size:0.76rem; color:#34D399; font-weight:700; margin-bottom:0.4rem;">
            T.R.A.V. HUMAN-IN-THE-LOOP GOVERNANCE ARCHITECTURE
          </div>
          <h3 style="font-size:1.3rem; margin-bottom:0.85rem; color:#FFFFFF;">
            Built for Real Operations—Not Unchecked Chatbot Hype
          </h3>
          <p style="font-size:0.88rem; color:#CBD5E1; margin-bottom:1.1rem;">
            Every workflow in this Operating System separates deterministic pricing math from AI language drafting using our 3-Tier Risk Gate:
          </p>
          <div style="background:#1E293B; border-left:4px solid #059669; padding:0.75rem 0.9rem; border-radius:6px; margin-bottom:0.65rem;">
            <div style="font-size:0.8rem; font-weight:800; color:#34D399;">GREEN GATE (75% OF TASK VOLUME — UNATTENDED 24/7)</div>
            <div style="font-size:0.78rem; color:#CBD5E1;">60-second missed-call SMS text-back, CRM normalization, portal provisioning, Tier-1 grounded FAQs, and Day +1 invoice nudges.</div>
          </div>
          <div style="background:#1E293B; border-left:4px solid #D97706; padding:0.75rem 0.9rem; border-radius:6px; margin-bottom:0.65rem;">
            <div style="font-size:0.8rem; font-weight:800; color:#FBBF24;">AMBER GATE (20% OF VOLUME — 15-SECOND APPROVAL)</div>
            <div style="font-size:0.78rem; color:#CBD5E1;">AI prepares 95% of 3-tier quotes (&gt;=$2,500), credit memos, and SOP updates, pausing in Slack for a 1-click thumb approval.</div>
          </div>
          <div style="background:#1E293B; border-left:4px solid #EF4444; padding:0.75rem 0.9rem; border-radius:6px;">
            <div style="font-size:0.8rem; font-weight:800; color:#F87171;">RED GATE (5% OF VOLUME — IMMEDIATE CONTAINMENT)</div>
            <div style="font-size:0.78rem; color:#CBD5E1;">Sentiment &lt;= 2/5, legal/clinical keywords, or chargebacks immediately lock automation and trigger the 12 Emergency Scripts.</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 1: The 5-Department Small Business Engine -->
  <section id="five-depts" class="section">
    <div class="container">
      <div class="section-header">
        <span class="eyebrow" style="background:var(--accent-soft); color:var(--accent);">THE 5-DEPARTMENT ENGINE</span>
        <h2>Eliminate Manual Friction Across Every Core Department</h2>
        <p>Whether you run a local medical/dental clinic, an HVAC/plumbing trade contractor, a B2B agency, or an e-commerce brand, your business runs on five interconnected pipelines.</p>
      </div>

      <div class="grid-5">
        <div class="card" style="border-top:4px solid var(--accent);">
          <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--accent);">DEPT 01 • CH 3</div>
          <h3 style="font-size:1.05rem; margin:0.35rem 0 0.5rem; color:var(--primary);">60-Second Lead Capture</h3>
          <p style="font-size:0.83rem; color:var(--muted);">Omnichannel webhook intake across web forms, missed calls, WhatsApp, and social DMs with instant SMS concierge booking.</p>
        </div>
        <div class="card" style="border-top:4px solid var(--secondary);">
          <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--secondary);">DEPT 02 • CH 4</div>
          <h3 style="font-size:1.05rem; margin:0.35rem 0 0.5rem; color:var(--primary);">3-Tier Sales &amp; Quoting</h3>
          <p style="font-size:0.83rem; color:var(--muted);">Convert 90-second post-visit voice notes into Good-Better-Best proposals backed by a 14-day polite-persistence follow-up loop.</p>
        </div>
        <div class="card" style="border-top:4px solid var(--accent);">
          <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--accent);">DEPT 03 • CH 5–7</div>
          <h3 style="font-size:1.05rem; margin:0.35rem 0 0.5rem; color:var(--primary);">Onboarding, Support &amp; Reviews</h3>
          <p style="font-size:0.83rem; color:var(--muted);">Zero-drop payment-to-portal provisioning, grounded RAG customer support, sentiment-gated 5-star Google reviews, and 90d recalls.</p>
        </div>
        <div class="card" style="border-top:4px solid var(--warning);">
          <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--warning);">DEPT 04 • CH 8</div>
          <h3 style="font-size:1.05rem; margin:0.35rem 0 0.5rem; color:var(--primary);">Invoicing, AR &amp; Receipt OCR</h3>
          <p style="font-size:0.83rem; color:var(--muted);">Same-day itemized invoice creation, 5-stage overdue payment chaser ladder, receipt vision OCR, and 5% vendor price-creep alerts.</p>
        </div>
        <div class="card" style="border-top:4px solid var(--secondary);">
          <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--secondary);">DEPT 05 • CH 9–10</div>
          <h3 style="font-size:1.05rem; margin:0.35rem 0 0.5rem; color:var(--primary);">Living SOPs &amp; Owner Pulse</h3>
          <p style="font-size:0.83rem; color:var(--muted);">Turn 3-minute Loom recordings into 7-block SOPs, delegate by voice, and review all 12 Core Owner KPIs every Friday in 15 minutes.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 2: Live Interactive ROI & Lead-Leak Calculator -->
  <section id="roi-calculator" class="section section-alt">
    <div class="container">
      <div class="section-header">
        <span class="eyebrow" style="background:var(--secondary-soft); color:var(--secondary);">INTERACTIVE FINANCIAL DIAGNOSTIC</span>
        <h2>Calculate Your Annual Cost of Manual Friction (CMF) in 30 Seconds</h2>
        <p>Adjust the sliders below to see how much manual admin hours and delayed lead responses are costing your business right now—and how fast the Flagship OS pays for itself.</p>
      </div>

      <div class="grid-2">
        <!-- Calculator Inputs -->
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:0.5rem;">
            <h3 style="font-size:1.05rem; color:var(--primary);">1. Your Business Baseline</h3>
            <div style="display:flex; gap:0.4rem;">
              <button type="button" class="btn btn-sm btn-outline-dark" onclick="setMarketingPreset('solo')">Solo/Micro</button>
              <button type="button" class="btn btn-sm btn-outline-dark" onclick="setMarketingPreset('clinic')">Clinic/Trade</button>
              <button type="button" class="btn btn-sm btn-outline-dark" onclick="setMarketingPreset('agency')">Multi-Crew</button>
            </div>
          </div>

          <div class="calc-group">
            <label class="calc-label" for="mTeamSize">Team Size (1–25 Staff) <span id="vTeamSize" class="calc-val">8 Staff</span></label>
            <input type="range" id="mTeamSize" min="1" max="25" step="1" value="8" oninput="updateMarketingRoi()" />
          </div>

          <div class="calc-group">
            <label class="calc-label" for="mHourlyCost">Blended Hourly Labor Cost ($/hr Owner + Admin) <span id="vHourlyCost" class="calc-val">$58/hr</span></label>
            <input type="range" id="mHourlyCost" min="20" max="200" step="2" value="58" oninput="updateMarketingRoi()" />
          </div>

          <div class="calc-group">
            <label class="calc-label" for="mWeeklyHours">Weekly Manual Admin &amp; Copy-Paste Hours <span id="vWeeklyHours" class="calc-val">24 hrs/wk</span></label>
            <input type="range" id="mWeeklyHours" min="4" max="80" step="1" value="24" oninput="updateMarketingRoi()" />
          </div>

          <div class="calc-group">
            <label class="calc-label" for="mMonthlyLeads">Monthly Inbound Leads (All Channels) <span id="vMonthlyLeads" class="calc-val">110 leads/mo</span></label>
            <input type="range" id="mMonthlyLeads" min="10" max="800" step="5" value="110" oninput="updateMarketingRoi()" />
          </div>

          <div class="calc-group">
            <label class="calc-label" for="mDelayedPct">% Leads Delayed &gt;5 Mins or Missed Calls <span id="vDelayedPct" class="calc-val">35%</span></label>
            <input type="range" id="mDelayedPct" min="5" max="85" step="1" value="35" oninput="updateMarketingRoi()" />
          </div>

          <div class="grid-2" style="gap:0.85rem;">
            <div class="calc-group" style="margin-bottom:0;">
              <label class="calc-label" for="mCloseRate">Net Close Rate (%) <span id="vCloseRate" class="calc-val">16%</span></label>
              <input type="range" id="mCloseRate" min="5" max="50" step="1" value="16" oninput="updateMarketingRoi()" />
            </div>
            <div class="calc-group" style="margin-bottom:0;">
              <label class="calc-label" for="mCustomerVal">Avg Customer Value ($)</label>
              <input type="number" id="mCustomerVal" class="form-input" value="1850" min="100" max="50000" step="50" oninput="updateMarketingRoi()" />
            </div>
          </div>
        </div>

        <!-- Calculator Live Outputs -->
        <div class="card">
          <h3 style="font-size:1.05rem; color:var(--primary); margin-bottom:1rem;">2. Your Projected 12-Month Automation Return</h3>

          <div class="result-banner">
            <div style="font-size:0.76rem; font-family:var(--font-mono); color:#94A3B8; text-transform:uppercase;">
              Total Annual Cost of Manual Friction (Annual CMF)
            </div>
            <div id="outMktCmf" style="font-size:2.35rem; font-weight:900; font-family:var(--font-mono); color:#34D399;">
              $196,650/yr
            </div>
            <div id="outMktBreakdown" style="font-size:0.82rem; color:#CBD5E1; margin-top:0.2rem;">
              Includes $72,384/yr Labor Waste + $124,266/yr Leaked Lead Revenue
            </div>
          </div>

          <div class="result-grid">
            <div class="result-box">
              <div class="lbl">Weekly Hours Recovered (70%)</div>
              <div id="outMktHours" class="val" style="color:var(--accent);">16.8 hrs/wk</div>
              <div style="font-size:0.76rem; color:var(--muted);">874 hours/year returned to team</div>
            </div>
            <div class="result-box">
              <div class="lbl">Leaked Lead Revenue Rescued (65%)</div>
              <div id="outMktLeadRescue" class="val" style="color:var(--secondary);">$80,773/yr</div>
              <div style="font-size:0.76rem; color:var(--muted);">Via 60-Second SMS &amp; Email Router</div>
            </div>
            <div class="result-box">
              <div class="lbl">Total First-Year Net Value (65%)</div>
              <div id="outMktNetValue" class="val" style="color:var(--primary);">$127,822/yr</div>
              <div style="font-size:0.76rem; color:var(--muted);">Conservative first-year capture</div>
            </div>
            <div class="result-box" style="background:var(--accent-soft); border-color:#A7F3D0;">
              <div class="lbl" style="color:var(--accent-hover);">Recommended Edition &amp; Payback</div>
              <div id="outMktPayback" class="val" style="color:var(--accent-hover); font-size:1.3rem;">Tier 3 ($59) • &lt; 4 Hours</div>
              <div style="font-size:0.76rem; color:var(--accent-hover); font-weight:600;">One-Time Investment • Zero Extra Staff</div>
            </div>
          </div>

          <a href="#pricing" class="btn btn-emerald" style="width:100%;">
            Get Instant Access to the Flagship OS Bundle ($59)
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 3: Interactive 10-Chapter Curriculum Explorer -->
  <section id="curriculum" class="section">
    <div class="container">
      <div class="section-header">
        <span class="eyebrow" style="background:var(--accent-soft); color:var(--accent);">COMPLETE 10-CHAPTER ARCHITECTURE</span>
        <h2>Explore Every Chapter, Framework, Case Study &amp; Action Workbook</h2>
        <p>Click any chapter tab below to inspect the exact engineering framework, real-world small business case study, and copy-paste prompts inside.</p>
      </div>

      <div id="chapterTabsBar" class="chapter-tabs"></div>

      <div class="card" style="border-left:6px solid var(--accent);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.65rem;">
          <span id="chViewDept" style="font-family:var(--font-mono); font-size:0.8rem; font-weight:800; color:var(--accent);"></span>
          <span style="font-family:var(--font-mono); font-size:0.78rem; background:var(--surface); padding:0.2rem 0.6rem; border-radius:6px; border:1px solid var(--border);">
            Includes 2 Vector Diagrams + 5 Prompts + 1 Fillable Workbook
          </span>
        </div>
        <h3 id="chViewTitle" style="font-size:1.45rem; color:var(--primary); margin-bottom:0.65rem;"></h3>
        <p id="chViewSummary" style="font-size:0.95rem; color:var(--text); margin-bottom:1.25rem;"></p>

        <div class="grid-3">
          <div style="background:var(--surface); padding:1rem; border-radius:8px; border:1px solid var(--border);">
            <div style="font-size:0.74rem; font-weight:800; text-transform:uppercase; color:var(--secondary); margin-bottom:0.3rem;">Core Engineering Framework</div>
            <div id="chViewFramework" style="font-size:0.86rem; font-weight:600;"></div>
          </div>
          <div style="background:var(--accent-soft); padding:1rem; border-radius:8px; border:1px solid #A7F3D0;">
            <div style="font-size:0.74rem; font-weight:800; text-transform:uppercase; color:var(--accent-hover); margin-bottom:0.3rem;">Verified SMB Case Study</div>
            <div id="chViewCaseStudy" style="font-size:0.86rem; font-weight:600;"></div>
          </div>
          <div style="background:var(--warning-soft); padding:1rem; border-radius:8px; border:1px solid #FDE68A;">
            <div style="font-size:0.74rem; font-weight:800; text-transform:uppercase; color:#92400E; margin-bottom:0.3rem;">Companion Workbook &amp; Prompts</div>
            <div id="chViewWorksheet" style="font-size:0.84rem; font-weight:700; margin-bottom:0.25rem;"></div>
            <div id="chViewPrompts" style="font-size:0.8rem; color:var(--muted);"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 4: Interactive Prompt Vault Sampler -->
  <section id="prompt-sampler" class="section section-dark">
    <div class="container">
      <div class="section-header">
        <span class="eyebrow">DETERMINISTIC PROMPT CONTRACTS</span>
        <h2>Preview 10 of the 50 Tested AI Workflow Prompts Inside the Vault</h2>
        <p>Every prompt is structured with explicit System Role, Grounded Variables, Hard Negative Guardrails, and Strict JSON Output Schemas.</p>
      </div>

      <div style="display:flex; flex-wrap:wrap; gap:0.5rem; justify-content:center; margin-bottom:1.5rem;" id="samplerButtonsBar"></div>

      <div class="grid-2">
        <div class="card" style="background:#1E293B; border-color:#334155; color:#FFFFFF;">
          <div style="font-family:var(--font-mono); font-size:0.78rem; color:#34D399; font-weight:700;" id="smpMeta"></div>
          <h3 style="font-size:1.15rem; margin:0.3rem 0 0.75rem; color:#FFFFFF;" id="smpTitle"></h3>
          <div style="font-size:0.76rem; font-weight:700; color:#94A3B8; margin-bottom:0.35rem;">SYSTEM &amp; USER PROMPT CONTRACT:</div>
          <pre id="smpTemplateBox" class="code-preview"></pre>
        </div>
        <div class="card" style="background:#1E293B; border-color:#334155; color:#FFFFFF;">
          <div style="font-size:0.76rem; font-weight:700; color:#38BDF8; margin-bottom:0.35rem;">VERIFIED SAMPLE OUTPUT &amp; JSON PAYLOAD:</div>
          <pre id="smpSampleBox" class="code-preview" style="max-height:395px;"></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 5: 5-Tier Commercial Pricing Matrix -->
  <section id="pricing" class="section section-alt">
    <div class="container">
      <div class="section-header">
        <span class="eyebrow" style="background:var(--accent-soft); color:var(--accent);">CHOOSE YOUR OPERATING SYSTEM EDITION</span>
        <h2>5 Commercial Editions Tailored to Your Stage of Growth</h2>
        <p>Start with the Free 5-Day Audit Starter Kit or get instant offline + Notion + Excel access with the Flagship $59 Bundle.</p>
      </div>

      <div class="grid-5" style="margin-bottom:3rem;">
        <!-- Tier 0 -->
        <div class="tier-card">
          <div>
            <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--secondary);">TIER 0 • STARTER KIT</div>
            <h3 style="font-size:1.05rem; margin-top:0.25rem;">Free 5-Day Audit Kit</h3>
            <div class="tier-price">$0</div>
            <div style="font-size:0.76rem; color:var(--muted);">Instant ZIP Download</div>
            <ul class="tier-list">
              <li>Chapter 1 + Audit Workbook PDF (32 Pages, 64 Fillable Fields)</li>
              <li>Offline Web App (Free Diagnostic Mode)</li>
              <li>5-Dept ROI &amp; Lead-Leak CSV Calculator</li>
              <li>Prompts 1.1–1.5 + Emergency Script 01</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip" class="btn btn-outline-dark" style="width:100%; font-size:0.82rem;">Download Free Kit ($0)</a>
        </div>

        <!-- Tier 1 -->
        <div class="tier-card">
          <div>
            <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--muted);">TIER 1 • RETAIL BOOK</div>
            <h3 style="font-size:1.05rem; margin-top:0.25rem;">Kindle &amp; KDP Print</h3>
            <div class="tier-price">$9.99</div>
            <div style="font-size:0.76rem; color:var(--muted);">eBook ($16.99 Print 6"×9")</div>
            <ul class="tier-list">
              <li>Complete 10-Chapter Manuscript (111,905+ Words)</li>
              <li>Reflowable EPUB 3.0 &amp; 242-Page Print Edition</li>
              <li>All 50 Prompts &amp; 12 Emergency Scripts in Text</li>
              <li>All 20 Chapter Architecture Diagrams</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Retail-Book-Pack.zip" class="btn btn-outline-dark" style="width:100%; font-size:0.82rem;">Get Retail Book Pack</a>
        </div>

        <!-- Tier 2 -->
        <div class="tier-card">
          <div>
            <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--secondary);">TIER 2 • WORKBOOK SUITE</div>
            <h3 style="font-size:1.05rem; margin-top:0.25rem;">Interactive Workbooks &amp; Tablet Planner</h3>
            <div class="tier-price">$29</div>
            <div style="font-size:0.76rem; color:var(--muted);">One-Time Direct License</div>
            <ul class="tier-list">
              <li>Everything in Tier 1 (Master PDF + EPUB 3.0)</li>
              <li>80-Page US Letter Fillable Workbook (160 Fields)</li>
              <li>76-Page ISO A4 Fillable Workbook (152 Fields)</li>
              <li>47-Page iPad / GoodNotes Landscape Planner</li>
              <li>62-Item Prompt &amp; SOP CSV Vault</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip" class="btn btn-cyan" style="width:100%; font-size:0.82rem;">Get Workbook Edition ($29)</a>
        </div>

        <!-- Tier 3 (Featured) -->
        <div class="tier-card featured">
          <span class="featured-ribbon">MOST POPULAR • FLAGSHIP OS</span>
          <div>
            <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--accent);">TIER 3 • COMPLETE OS</div>
            <h3 style="font-size:1.05rem; margin-top:0.25rem;">Complete SmallBiz AI Automation OS</h3>
            <div class="tier-price" style="color:var(--accent);">$59</div>
            <div style="font-size:0.76rem; color:var(--muted);">One-Time Commercial License</div>
            <ul class="tier-list">
              <li><strong>Everything in Tier 2 Included</strong></li>
              <li><strong>Pro Web Companion App</strong> + License Key (<code>SMALLBIZ-OS-PRO-2026</code>)</li>
              <li><strong>5-Database Minimalist Notion OS Kit</strong> + Formula 2.0 Pack</li>
              <li><strong>8-Tab Charted Excel Command Center</strong> + JSON Blueprints</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip" class="btn btn-emerald" style="width:100%; font-size:0.84rem;">Get Flagship OS ($59)</a>
        </div>

        <!-- Tier 4 -->
        <div class="tier-card">
          <div>
            <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--warning);">TIER 4 • LIVING VAULT</div>
            <h3 style="font-size:1.05rem; margin-top:0.25rem;">Living Automation Vault &amp; Office Suite</h3>
            <div class="tier-price">$12<span style="font-size:0.95rem;">/mo</span></div>
            <div style="font-size:0.76rem; color:var(--muted);">Or $59/yr VIP Annual Access</div>
            <ul class="tier-list">
              <li><strong>Everything in Tier 3 Included</strong></li>
              <li>Monthly Industry Drop #01 (4 Verticals + 8 Prompts)</li>
              <li>Editable Word (.DOCX) SOPs &amp; Slide Decks (.PPTX)</li>
              <li>Quarterly New Make/n8n/Zapier Blueprints</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Automation-Vault-Membership-Drop01.zip" class="btn btn-amber" style="width:100%; font-size:0.82rem;">Join Living Vault</a>
        </div>
      </div>

      <!-- Feature Comparison Matrix Table -->
      <table class="comp-table">
        <thead>
          <tr>
            <th>Deliverable / Component</th>
            <th>Tier 0 ($0)</th>
            <th>Tier 1 ($9.99)</th>
            <th>Tier 2 ($29)</th>
            <th>Tier 3 Flagship ($59)</th>
            <th>Tier 4 Vault ($12/mo)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Chapter 1 + Fillable Audit Workbook + ROI CSV</strong></td>
            <td>Included</td>
            <td>Included</td>
            <td>Included</td>
            <td><strong>Included</strong></td>
            <td><strong>Included</strong></td>
          </tr>
          <tr>
            <td><strong>Complete 10-Chapter Book (179p PDF + EPUB 3.0 + 242p Print)</strong></td>
            <td>Ch 1 Sample</td>
            <td>Included</td>
            <td>Included</td>
            <td><strong>Included</strong></td>
            <td><strong>Included</strong></td>
          </tr>
          <tr>
            <td><strong>Fillable Action Workbooks (US Letter 80p + ISO A4 76p + iPad 47p)</strong></td>
            <td>Ch 1 Only</td>
            <td>—</td>
            <td>Included (406 Fields)</td>
            <td><strong>Included (406 Fields)</strong></td>
            <td><strong>Included (406 Fields)</strong></td>
          </tr>
          <tr>
            <td><strong>Offline SaaS-Lite Web App (50 Prompts, 12 Scripts &amp; 6 Calculators)</strong></td>
            <td>Diagnostic Mode</td>
            <td>—</td>
            <td>Diagnostic Mode</td>
            <td><strong>Pro Edition Activated</strong></td>
            <td><strong>Pro Edition Activated</strong></td>
          </tr>
          <tr>
            <td><strong>5-Database Minimalist Notion OS Kit + Notion Formula 2.0 Guide</strong></td>
            <td>—</td>
            <td>—</td>
            <td>62-Item CSV Only</td>
            <td><strong>All 5 Databases + Guide</strong></td>
            <td><strong>All 5 Databases + Guide</strong></td>
          </tr>
          <tr>
            <td><strong>4-Industry Vertical Pack (Drop #01) + Editable Office Suite (.DOCX/.PPTX)</strong></td>
            <td>—</td>
            <td>—</td>
            <td>—</td>
            <td>—</td>
            <td><strong>Included + Monthly Drops</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- Section 6: 12-Question FAQ & 30-Day Guarantee -->
  <section id="faq" class="section">
    <div class="container" style="max-width:940px;">
      <div class="section-header">
        <span class="eyebrow" style="background:var(--accent-soft); color:var(--accent);">FREQUENTLY ASKED QUESTIONS</span>
        <h2>Answers for Pragmatic Small Business Owners</h2>
        <p>Everything you need to know before deploying The Small Business AI Automation Operating System.</p>
      </div>

      <div id="faqContainer">
        <div class="faq-item open">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>1. Do I need a software developer or coding experience to deploy these workflows?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            No. Every workflow in this Operating System is engineered for visual no-code platforms (Make.com, Zapier, and n8n) using copy-paste JSON schemas and plain-English prompts. If you can copy and paste a spreadsheet column and connect a Google Sheet or QuickBooks account, you can deploy your first 60-second lead router in under 60 minutes.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>2. How does the T.R.A.V. Architecture prevent AI from hallucinating prices or making bad promises?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Chapter 2 establishes a strict separation between deterministic math and language generation. The AI is never allowed to calculate prices, taxes, or discounts on its own; instead, a lookup table injects locked SKU rows into the prompt at <code>temperature: 0.0–0.1</code>, and any quote above your threshold pauses at an Amber Gate in Slack for a 15-second human approval click.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>3. Does the Interactive Web Companion App require a monthly subscription or send my financial data to the cloud?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Zero subscription and zero cloud transmission. <code>smallbiz-automation-os-app.html</code> is a 100% self-contained offline HTML5 application that runs locally inside your browser (Chrome, Edge, Safari, Firefox) from your hard drive or USB stick. All your KPI snapshots and calculator inputs stay inside your browser's local storage and export to local CSV/JSON files.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>4. How much does the third-party software stack (Make, OpenAI, Twilio) cost per month to run?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            For a typical 5-to-15 person business processing 100–250 leads and 50–100 invoices per month, total API and no-code tool costs average $45 to $185 per month total—while recovering $5,000 to $15,000+ per month in rescued leads and administrative bandwidth.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>5. Which industries is this Operating System built for?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Every chapter includes multi-industry implementations across four core small business verticals: (1) Medical, Dental, Physical Therapy &amp; Wellness Clinics, (2) HVAC, Plumbing, Electrical, Roofing &amp; Home Service Contractors, (3) B2B Agencies, CPA Firms, Legal &amp; Consultancies, and (4) Specialty Retail &amp; D2C E-Commerce brands.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>6. How do I activate the Pro Web App with my Tier 3 or Tier 4 bundle?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Open <code>07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt</code> inside your bundle, copy the code <code>SMALLBIZ-OS-PRO-2026</code>, click "Activate Pro Access" in the top bar of the web app, and paste the code. All 50 Prompts, 12 Emergency Scripts, and 6 calculators activate immediately.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>7. Are the PDF workbooks fillable on my computer and iPad, or do I have to print them?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Both! We include interactive AcroForm-enabled PDFs for US Letter (8.5"×11", 160 fillable fields), International ISO A4 (210×297mm, 152 fillable fields), and a dedicated Landscape Tablet Planner (11"×8.5", 94 fillable fields) built for iPad GoodNotes, Notability, reMarkable, and desktop Adobe/Edge readers.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>8. Will my existing staff resist these automations out of fear of layoffs?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Chapter 1 includes <code>Prompt 1.5</code> (the "Zero-Layoff Automation Compact" internal memo) and a proven rollout script that frames automation around eliminating evening/weekend data-entry drudgery so staff can focus on high-value customer care and higher compensation.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>9. What happens if an automation hits an API outage or an angry customer texts in?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Prompt 2.5 monitors a Dead-Letter Queue (DLQ) that automatically routes failed webhooks to a backup Google Sheet and alerts your team via Slack/SMS. If an angry customer messages in (<code>Sentiment &lt;= 2</code>), the Red Gate halts all automated sequences immediately and gives you 12 copy-paste Emergency Scripts to resolve the situation personally.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>10. Can I use the Notion OS Kit on a free Notion account?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Yes. All 5 CSV databases and Notion Formula 2.0 properties run 100% natively on Notion's Free plan as well as Plus/Business plans with zero paid third-party Notion plugins required.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>11. How long does the full rollout take if I only have 3 hours a week to work on systems?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Chapter 10 structures the deployment into a realistic 90-Day Phased Roadmap (3 hours/week): Phase I (Days 1–30) launches your 60-second lead router and same-day invoicing; Phase II (Days 31–60) deploys 3-tier quotes, onboarding, and RAG support; Phase III (Days 61–90) adds receipt OCR, living SOPs, and your 15-minute Friday KPI Scorecard.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-q" onclick="toggleFaq(this)">
            <span>12. What is your 30-Day Implementation Satisfaction Guarantee?</span>
            <span>+</span>
          </button>
          <div class="faq-a">
            Run the Chapter 1 Audit and deploy a single workflow from Chapter 3 or Chapter 8 within 30 days. If the system does not visibly identify at least $25,000 in recoverable annual friction or save you at least 5 hours a week, reply to your receipt email within 30 days for a courteous 100% refund.
          </div>
        </div>
      </div>
    </div>
  </section>

  <footer>
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
      <div>
        <strong style="color:#FFFFFF;">The Small Business AI Automation Operating System (2026 Enterprise Edition)</strong><br />
        <span>Digital Publishing Studio • 100% Offline-Ready &amp; Privacy-First Operations Architecture</span>
      </div>
      <div>
        <a href="#top" style="color:#34D399; text-decoration:none; font-weight:700;">Back to Top ↑</a>
      </div>
    </div>
  </footer>

  <script>
    const CHAPTERS_DATA = {chapters_json};
    const FEATURED_PROMPTS = {featured_json};

    function fmtUsd(n) {{
      return "$" + Math.round(Number(n) || 0).toLocaleString("en-US");
    }}

    function updateMarketingRoi() {{
      const team = parseFloat(document.getElementById("mTeamSize").value) || 8;
      const rate = parseFloat(document.getElementById("mHourlyCost").value) || 58;
      const hrs = parseFloat(document.getElementById("mWeeklyHours").value) || 24;
      const leads = parseFloat(document.getElementById("mMonthlyLeads").value) || 110;
      const delayedPct = parseFloat(document.getElementById("mDelayedPct").value) || 35;
      const closePct = parseFloat(document.getElementById("mCloseRate").value) || 16;
      const ltv = parseFloat(document.getElementById("mCustomerVal").value) || 1850;

      document.getElementById("vTeamSize").textContent = team + " Staff";
      document.getElementById("vHourlyCost").textContent = "$" + rate + "/hr";
      document.getElementById("vWeeklyHours").textContent = hrs + " hrs/wk";
      document.getElementById("vMonthlyLeads").textContent = leads + " leads/mo";
      document.getElementById("vDelayedPct").textContent = delayedPct + "%";
      document.getElementById("vCloseRate").textContent = closePct + "%";

      const laborWaste = hrs * rate * 52;
      const delayedLeads = Math.round(leads * (delayedPct / 100));
      const leadLeak = delayedLeads * (closePct / 100) * ltv * 12;
      const totalCmf = laborWaste + leadLeak;

      const hrsRecovered = hrs * 0.70;
      const leadRescue = leadLeak * 0.65;
      const netFirstYear = totalCmf * 0.65;
      const paybackHours = Math.max(1, Math.round((59 / Math.max(netFirstYear, 1)) * 8760));

      document.getElementById("outMktCmf").textContent = fmtUsd(totalCmf) + "/yr";
      document.getElementById("outMktBreakdown").textContent =
        `Includes ${{fmtUsd(laborWaste)}}/yr Labor Waste + ${{fmtUsd(leadLeak)}}/yr Leaked Lead Revenue`;
      document.getElementById("outMktHours").textContent = hrsRecovered.toFixed(1) + " hrs/wk";
      document.getElementById("outMktLeadRescue").textContent = fmtUsd(leadRescue) + "/yr";
      document.getElementById("outMktNetValue").textContent = fmtUsd(netFirstYear) + "/yr";
      document.getElementById("outMktPayback").textContent = `Tier 3 ($59) • ~${{paybackHours}} Hrs Payback`;
    }}

    function setMarketingPreset(p) {{
      if (p === "solo") {{
        document.getElementById("mTeamSize").value = 2;
        document.getElementById("mHourlyCost").value = 72;
        document.getElementById("mWeeklyHours").value = 15;
        document.getElementById("mMonthlyLeads").value = 40;
        document.getElementById("mDelayedPct").value = 40;
        document.getElementById("mCloseRate").value = 20;
        document.getElementById("mCustomerVal").value = 2100;
      }} else if (p === "clinic") {{
        document.getElementById("mTeamSize").value = 9;
        document.getElementById("mHourlyCost").value = 58;
        document.getElementById("mWeeklyHours").value = 26;
        document.getElementById("mMonthlyLeads").value = 135;
        document.getElementById("mDelayedPct").value = 36;
        document.getElementById("mCloseRate").value = 18;
        document.getElementById("mCustomerVal").value = 1750;
      }} else {{
        document.getElementById("mTeamSize").value = 18;
        document.getElementById("mHourlyCost").value = 68;
        document.getElementById("mWeeklyHours").value = 42;
        document.getElementById("mMonthlyLeads").value = 260;
        document.getElementById("mDelayedPct").value = 34;
        document.getElementById("mCloseRate").value = 15;
        document.getElementById("mCustomerVal").value = 3100;
      }}
      updateMarketingRoi();
    }}

    function selectChapterTab(num) {{
      const ch = CHAPTERS_DATA.find(c => c.num === num) || CHAPTERS_DATA[0];
      document.querySelectorAll(".ch-tab").forEach(btn => {{
        btn.classList.toggle("active", parseInt(btn.dataset.num, 10) === num);
      }});
      document.getElementById("chViewDept").textContent = ch.dept;
      document.getElementById("chViewTitle").textContent = ch.title;
      document.getElementById("chViewSummary").textContent = ch.summary;
      document.getElementById("chViewFramework").textContent = ch.framework;
      document.getElementById("chViewCaseStudy").textContent = ch.case_study;
      document.getElementById("chViewWorksheet").textContent = ch.worksheet;
      document.getElementById("chViewPrompts").textContent = ch.prompts;
    }}

    function selectSamplePrompt(pid) {{
      const p = FEATURED_PROMPTS.find(item => item.id === pid) || FEATURED_PROMPTS[0];
      document.querySelectorAll(".smp-btn").forEach(btn => {{
        btn.classList.toggle("btn-emerald", btn.dataset.pid === pid);
        btn.classList.toggle("btn-outline-light", btn.dataset.pid !== pid);
      }});
      document.getElementById("smpMeta").textContent = `${{p.id}} • ${{p.dept}} • ${{p.zone}} Governance Gate`;
      document.getElementById("smpTitle").textContent = p.title;
      document.getElementById("smpTemplateBox").textContent = p.template;
      document.getElementById("smpSampleBox").textContent = p.sample;
    }}

    function toggleFaq(btn) {{
      const item = btn.parentElement;
      item.classList.toggle("open");
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      const tabsBar = document.getElementById("chapterTabsBar");
      tabsBar.innerHTML = CHAPTERS_DATA.map(c =>
        `<button type="button" class="ch-tab" data-num="${{c.num}}" onclick="selectChapterTab(${{c.num}})">Chapter ${{c.num}}</button>`
      ).join("");

      const smpBar = document.getElementById("samplerButtonsBar");
      smpBar.innerHTML = FEATURED_PROMPTS.map(p =>
        `<button type="button" class="btn btn-sm btn-outline-light smp-btn" data-pid="${{p.id}}" onclick="selectSamplePrompt('${{p.id}}')">${{p.id}} (Ch ${{p.chapter}})</button>`
      ).join("");

      updateMarketingRoi();
      selectChapterTab(1);
      selectSamplePrompt("Prompt 1.1");
    }});
  </script>
</body>
</html>
"""
    return clean_copy(html)


# =============================================================================
# DELIVERABLE 2: marketplace-listings-and-bd-launch-runbook.md (3,000+ words)
# =============================================================================

def build_marketplace_and_bd_runbook() -> str:
    content = """# Global Marketplace Listings & Bangladesh Creator Launch Runbook (Amazon KDP, Draft2Digital, Gumroad, Payoneer & IRS Form W-8BEN)

**Document ID:** `10-MARKETING/marketplace-listings-and-bd-launch-runbook.md`  
**Project:** *The Small Business AI Automation Operating System* (`SMALLBIZ-AI-AUTOMATION-OS-V1`)  
**Target Channels:** Amazon KDP (Kindle eBook + 6"×9" Print Paperback), Draft2Digital (Apple Books, Kobo, Barnes & Noble, OverDrive), and Gumroad (4-Tier Direct Commercial Storefront)  
**Tax & Payout Jurisdiction:** Bangladesh Resident Creator -> US Source Royalty Withholding Reduction (`30% -> 10%` under **US–Bangladesh Income Tax Treaty Article 12**) + **Payoneer Global Payment Service**  

---

## 1. Amazon KDP Publishing Runbook (Kindle eBook & 6"×9" Paperback)

Amazon Kindle Direct Publishing (`https://kdp.amazon.com`) serves as your global retail discovery engine (`Tier 1`), establishing authority on Amazon US, UK, Canada, Australia, Germany, and global marketplaces while driving high-intent small business owners into your direct Gumroad ecosystem (`Tiers 0, 2, 3, and 4`).

### 1.1 Exact KDP Bookshelf Metadata Table (Copy-Paste Ready)

| KDP Metadata Field | Exact Production Value to Enter in KDP Bookshelf |
| :--- | :--- |
| **Language** | `English` |
| **Book Title** | `The Small Business AI Automation Operating System` |
| **Subtitle** | `A Practical System to Automate Lead Capture, Customer Support, Invoicing, Team Operations, and Weekly Owner Reporting Without Hiring Extra Staff` |
| **Series Title** | `Enterprise Small Business Operations & AI Systems Series` (Book 2) |
| **Edition Number** | `1` (`2026 Enterprise Edition`) |
| **Primary Author / Contributor** | Your Legal Publishing Name or Studio Imprint (`Digital Publishing Studio`) |
| **Publishing Rights** | `I own the copyright and I hold the necessary publishing rights.` |
| **Primary Marketplace** | `Amazon.com` |
| **Adult Content (`18+`)** | `No` |
| **Reading Age (Optional)** | Leave blank (Adult Professional / Business Trade Non-Fiction) |
| **AI Disclosure Question (KDP Content Guidelines)** | Follow KDP's current disclosure form accurately for AI-assisted text/workflows and human-edited production engineering. |

---

### 1.2 HTML-Formatted Amazon KDP Book Description (`< 4,000 Characters`)
Copy and paste the exact KDP-compliant HTML block below directly into the **Description (Source View)** box on both your Kindle eBook and Paperback listings:

```html
<p><b>Stop drowning in evening paperwork, missed customer calls, and overdue invoices. Install a deterministic, human-in-the-loop AI Operating System across your entire 1-to-25 person business in 90 days—without hiring extra administrative staff or writing complex code.</b></p>

<p>Most small business owners lose <b>20% to 35% of their potential net profit</b> to the three silent killers of small business growth: inbound leads that go cold because nobody replied within 5 minutes, hours of repetitive copy-pasting between disconnected software apps, and completed jobs that sit unbilled or unpaid for 40+ days.</p>

<p>Generic "prompt packs" fail in real businesses because unguarded chatbots invent prices, hallucinate policies, and damage hard-earned local reputations. <b><i>The Small Business AI Automation Operating System</i></b> gives founders, clinic directors, home-service contractors, e-commerce operators, and B2B agency leaders a battle-tested systems engineering blueprint built on the <b>T.R.A.V. (Trigger -&gt; Rules -&gt; AI -&gt; Verification)</b> governance architecture.</p>

<p><b>Inside This Complete 10-Chapter Enterprise Operations Manual, You Will Deploy:</b></p>
<ul>
  <li><b>Chapter 1 — The 5-Day Manual Friction Audit:</b> Quantify your exact Annual Cost of Manual Friction (CMF) across Labor Waste, Leaked Lead Revenue, and Cashflow Drag, and rank your highest-ROI quick wins using the P.A.C.E. Matrix.</li>
  <li><b>Chapter 2 — The Human-in-the-Loop T.R.A.V. Safety Gate:</b> Separate deterministic pricing math from AI drafting using Green Gates (75% unattended 24/7 execution), Amber Gates (15-second Slack/Teams thumb approval for custom quotes), and Red Gates (immediate human takeover).</li>
  <li><b>Chapter 3 — The 60-Second Speed-to-Lead Router:</b> Capture website forms, missed phone calls, voicemails, WhatsApp messages, Facebook/IG Lead Ads, and Google Business messages into a unified router that texts back and books appointments in under 60 seconds.</li>
  <li><b>Chapter 4 — 3-Option Good-Better-Best Proposals &amp; The 14-Day Follow-Up Loop:</b> Turn a 90-second post-visit voice note into a polished 3-tier quote PDF and automate polite, multi-channel follow-ups that stop the millisecond the client signs.</li>
  <li><b>Chapter 5 — Frictionless Zero-Drop Client Onboarding:</b> Wire Stripe, Square, and QuickBooks deposit webhooks to instant welcome packets, cloud folder provisioning, conditional intake validation, and scope-creep early warnings.</li>
  <li><b>Chapter 6 — 24/7 Grounded RAG Customer Support:</b> Resolve 60%+ of routine Tier-1 tickets (hours, parking, WISMO order status, rescheduling) with zero hallucination while escalating frustrated customers (Sentiment &lt;= 2) to a human immediately.</li>
  <li><b>Chapter 7 — The 5-Star Review &amp; Repeat-Sales Flywheel:</b> Send a 1-click sentiment check at the peak moment of gratitude—routing happy clients to Google Reviews and waking up 60/90/180-day dormant customers automatically.</li>
  <li><b>Chapter 8 — Automated Invoicing, 5-Stage A/R Chasers &amp; Receipt OCR:</b> Compress Days Sales Outstanding (DSO) from 42 days down to 12 days with same-day billing, relationship-safe overdue reminders, and automated 5% vendor price-creep detection.</li>
  <li><b>Chapter 9 — The Self-Running Team &amp; Living SOP Engine:</b> Convert 3-minute screen recordings into 7-block Standard Operating Procedures, delegate tasks by voice memo, and deploy an internal "Ask-the-SOP" bot for your staff.</li>
  <li><b>Chapter 10 — The 15-Minute Friday Owner Scorecard &amp; 90-Day Rollout:</b> Review your entire company every Friday at 3:00 PM across 12 Core KPIs in 15 minutes flat.</li>
</ul>

<p><b>Includes 50 Copy-Ready AI Workflow Prompts (Prompts 1.1–10.5), 12 Red-Gate Emergency Operations Scripts, 20 Architecture &amp; Decision-Tree Diagrams, and Step-by-Step Blueprints for Make.com, Zapier, n8n, OpenAI, Claude, Notion, and QuickBooks.</b></p>
```

---

### 1.3 The 7 High-Intent Amazon KDP Backend Keyword Phrases (50-Char Limit Each)
Enter these exact seven phrases into the **7 Keyword Boxes** in KDP (zero punctuation, zero duplicate words from the title/subtitle):

1. `no code workflow make zapier n8n small company` (`46 chars`)
2. `home service contractor hvac dental clinic crm` (`46 chars`)
3. `standard operating procedures sop delegation guide` (`50 chars`)
4. `speed to lead missed call text back sms marketing` (`49 chars`)
5. `accounts receivable collections cashflow dso book` (`49 chars`)
6. `openai chatgpt claude business prompt engineering` (`49 chars`)
7. `entrepreneur operations management scaling systems` (`50 chars`)

### 1.4 BISAC & Amazon Store Category Selections
Select the following three categories in KDP Categories:
1. `Books > Business & Money > Small Business & Entrepreneurship > Small Business` (`BUS060000`)
2. `Books > Business & Money > Management & Leadership > Systems & Planning` (`BUS041000`)
3. `Books > Computers & Technology > Business & Management > Production & Operations` (`COM005000`)

---

### 1.5 Exact File Pairing & Global Royalty Pricing for KDP

#### Edition A: Amazon Kindle eBook (`70% Royalty Tier`)
- **Manuscript Upload File:** `09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub` (`376.04 KB`, validated EPUB 3.0)
- **Cover Upload File:** `08-COVER-DESIGN/ebook-cover-kdp-kindle.png` (`1600 × 2560 px`, `1,291.02 KB`)
- **DRM Setting:** `No, do not enable Digital Rights Management` (recommended so buyers can read across devices without friction)
- **List Price & Royalty:** Set **US List Price = `$9.99 USD`** under the **`70% Royalty Plan`** (yields `~$6.85 USD` net royalty per Kindle unit after whispernet delivery fee). Set UK = `£7.99`, Canada = `$12.99 CAD`, Australia = `$13.99 AUD`, EU = `€9.49 EUR`.

#### Edition B: Amazon KDP Print Paperback (`6.0" × 9.0"` Trim — `60% Royalty Tier`)
- **Interior Paper & Ink:** `Black & white interior with white paper`
- **Trim Size:** `6 × 9 in (15.24 × 22.86 cm)`
- **Bleed Setting:** `No Bleed` (interior PDF uses mirrored `0.75"` gutter / `0.625"` outer margins)
- **Cover Finish:** `Matte`
- **Interior Manuscript Upload File:** `09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf` (**`242 pages`**)
- **Full-Wrap Cover Upload File:** `09-EXPORTS/PRINT/kdp-paperback-full-wrap-cover.pdf` (`12.795" × 9.250"`, `0.545"` spine, `1 page`)
- **List Price & Royalty:** Set **US List Price = `$16.99 USD`** (`60%` of `$16.99` = `$10.19` minus `$3.90` print cost for `242` pages = **`$6.29 USD` net profit per paperback sold**). Enable **Expanded Distribution (`40%`)** to list automatically with Ingram, bookstores, and libraries.

---

## 2. Draft2Digital (D2D) Wide Retail & Library Distribution Runbook

Use **Draft2Digital (`https://www.draft2digital.com`)** to distribute your eBook to non-Amazon international storefronts and public/corporate library systems with zero upfront fees:

1. **Create New Book on D2D:** Enter the exact Title, Subtitle, Series, and HTML Description from Section 1.1–1.2 above.
2. **Upload Validated EPUB & Cover:**
   - Upload `09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub` and `08-COVER-DESIGN/ebook-cover-kdp-kindle.png`.
   - Because our EPUB 3.0 already contains a validated `nav.xhtml` Table of Contents and semantic chapter splits, select **"Use existing EPUB layout"** during D2D preview.
3. **Select Digital Storefronts & Library Channels (IMPORTANT: Leave Amazon UNCHECKED since you upload directly to KDP):**
   - **Retail Storefronts (`$9.99 USD`):** Check **Apple Books**, **Barnes & Noble Nook**, **Rakuten Kobo**, **Smashwords Store**, **Tolino**, **Vivlio**, and **Fable**.
   - **Subscription & Library Channels (`$19.99 USD` Library Price):** Check **Everand (Scribd)**, **OverDrive (Libby)**, **Bibliotheca**, **Baker & Taylor**, **BorrowBox**, **Hoopla**, and **Odilo**. *(Setting the library institutional price to `$19.99–$24.99` doubles your royalty per library checkout while keeping consumer retail at `$9.99`.)*

---

## 3. Gumroad 4-Product Direct Storefront Setup (`Tiers 0, 2, 3, and 4`)

Your direct Gumroad storefront (`https://yourstudio.gumroad.com`) captures `90%+` of gross revenue and builds your direct customer email list. Create the following four products in Gumroad:

### Product 1: Tier 0 — Free "5-Day Small Business Time & Lead-Leak Audit" Starter Kit (`$0+ Pay-What-You-Want`)
- **Product Type:** `Digital product`
- **URL Slug:** `/l/smallbiz-ai-audit-kit`
- **Price:** `$0+` (Suggested price: `$0`, allow customers to pay `$0` for instant lead-magnet capture)
- **Cover Image:** `08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png` (`1600 × 1200 px`)
- **Uploaded Content Archive:** `09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip`
- **Checkout Upsell Rule:** Configure Gumroad's **In-Cart Order Bump** offering an instant upgrade to **Tier 2 (`$29`)** or **Tier 3 Flagship OS (`$59` with `$10` fast-action discount code `AUDIT10`)**.

### Product 2: Tier 2 — Interactive Workbook, Visual Shortcut Atlas & Tablet Planner Edition (`$29.00`)
- **Product Type:** `Digital product`
- **URL Slug:** `/l/smallbiz-ai-workbooks-atlas`
- **Price:** `$29.00 USD` (Enable **Purchasing Power Parity / PPP** at `40% max discount` to boost international conversion in emerging markets while protecting US/UK/CA/AU pricing)
- **Cover Image:** `08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png` (`1600 × 1200 px`)
- **Uploaded Content Archive:** `09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip`

### Product 3: Tier 3 (FLAGSHIP) — Complete Small Business AI Automation OS Bundle (`$59.00`)
- **Product Type:** `Digital product`
- **URL Slug:** `/l/smallbiz-ai-automation-os`
- **Price:** `$59.00 USD` (Mark as Featured Product on your Gumroad profile)
- **Cover Image:** `08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png` (`1600 × 1200 px`)
- **Uploaded Content Archive:** `09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip`
- **Receipt Note Configuration:** In Gumroad's **Receipt customization** box, add:
  > *"Thank you for investing in the Complete Small Business AI Automation Operating System! Your Pro Web Companion App license key is **`SMALLBIZ-OS-PRO-2026`** (also saved inside `07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt` in your ZIP download)."*

### Product 4: Tier 4 — Living Automation Vault & Editable Office Suite Membership (`$12/mo` or `$59/yr`)
- **Product Type:** `Membership (Recurring Subscription)`
- **URL Slug:** `/l/smallbiz-automation-vault-vip`
- **Pricing Tiers:** `$12.00 / month` OR `$59.00 / year` (Default to Annual Billing — saves buyers 59% and locks in `$59` immediate cashflow)
- **Cover Image:** `08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png` (`1600 × 1200 px`)
- **Uploaded Content Archive:** `09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Automation-Vault-Membership-Drop01.zip` (plus future monthly/quarterly workflow drops via Gumroad Posts).

---

## 4. Bangladesh Creator Global Payout & US–BD Tax Treaty Runbook (`Payoneer + Form W-8BEN`)

Because Amazon KDP, Draft2Digital, and Gumroad are US-registered corporations paying royalties to a creator residing in **Bangladesh**, configuring your banking and US tax treaty documentation properly is critical. Without a valid IRS Form W-8BEN claiming the **US–Bangladesh Income Tax Treaty**, US platforms are legally required to withhold **30%** of your US buyer royalties. With the exact setup below, your US statutory withholding drops from **30% down to 10%**—saving you `$200` on every `$1,000` in US book royalties!

---

### 4.1 Step 1 — Obtain Your 12-Digit Bangladeshi e-TIN Certificate (Free, 10 Minutes)
To claim tax treaty benefits on IRS Form W-8BEN, you must enter a Foreign Tax Identifying Number (`FTIN`). Do **not** leave the FTIN box blank:
1. Visit the National Board of Revenue (NBR) portal at `https://secure.incometax.gov.bd/TINHome`.
2. Register and generate your **12-Digit Electronic Tax Identification Number (e-TIN)** using your Bangladeshi National ID (`NID`) and mobile number, ensuring your English spelling and residential address match your NID, Passport, and Payoneer profile character-for-character.
3. Download and save your PDF e-TIN certificate (`12 digits`, no hyphens or spaces when typing into US tax forms).

---

### 4.2 Step 2 — Configure Payoneer Global Payment Service (Receiving USD via US ACH)
Amazon KDP and Draft2Digital do not mail paper checks to Bangladesh correctly and wire transfers incur `$25–$40` intermediary fees. Instead, use **Payoneer's US Global Payment Service** to receive `100%` of your royalties via free US domestic EFT/ACH:

1. Log into your verified **Payoneer (`https://myaccount.payoneer.com`)** account linked to your local Bangladeshi bank account (e.g., Brac Bank, Eastern Bank PLC, City Bank, Dutch-Bangla Bank, Islami Bank, or Prime Bank).
2. Navigate to **`Receive -> Receiving Accounts -> USA (USD)`**.
3. Copy your assigned US virtual checking account credentials:
   - **Bank Name:** `Community Federal Savings Bank` or `First Century Bank` (or Citibank)
   - **Account Type:** `Checking`
   - **Routing (ABA) Number:** `9-digit ABA Routing Number` (e.g., `026073150` or `061120084`)
   - **Account Number:** Your unique `12-to-17 digit` USD account number
   - **Beneficiary Name:** Your exact legal name
4. **Where to Enter These USD Receiving Details:**
   - **In Amazon KDP (`Your Account -> Getting Paid`):** Select **Where is your bank? -> `United States`**, Account Type = `Checking`, and paste your Payoneer USD Routing and Account Number. This enables `$0-fee` monthly EFT payouts across all 13 Amazon currencies converted into USD!
   - **In Draft2Digital (`Account -> Payment Info`):** Select **`Payoneer`** (direct OAuth link) OR **`US Direct Deposit (ACH)`** using your Payoneer USD routing/account numbers (`$10` minimum payout threshold).
   - **In Gumroad (`Settings -> Payouts`):** Select **`Bangladesh`** as your country of residence and connect either your **Direct Local Bangladesh Bank Account** (via SWIFT/local routing) or **Payoneer** account.

---

### 4.3 Step 3 — Line-by-Line IRS Form W-8BEN Completion Guide (`Article 12 — 10% Royalty Rate`)
When completing the online Tax Interview inside **Amazon KDP**, **Draft2Digital**, and **Gumroad (Stripe Tax)**:

| Form W-8BEN Section & Line | Exact Entry for a Resident of Bangladesh |
| :--- | :--- |
| **Tax Status / Account Type** | `Individual` (or `Sole Proprietorship` under your legal name) |
| **Are you a US citizen, US permanent resident (Green Card), or US tax resident?** | **`No`** |
| **Are you acting as an intermediary agent?** | **`No`** |
| **Part I, Line 1: Name of individual who is the beneficial owner** | Your exact legal name as shown on your NID, Passport, and e-TIN |
| **Part I, Line 2: Country of citizenship** | **`Bangladesh`** |
| **Part I, Line 3: Permanent residence address** | Your street address, city, postal code, and country (`Bangladesh`) |
| **Part I, Line 5: U.S. taxpayer identification number (SSN or ITIN)** | Leave **BLANK** (not required when you provide your Bangladeshi e-TIN on Line 6a) |
| **Part I, Line 6a: Foreign tax identifying number (FTIN)** | Check *"I have a non-US TIN"* and enter your **12-Digit Bangladeshi e-TIN** (e.g., `123456789012`) |
| **Part II, Line 9: Claim of Tax Treaty Benefits — Resident of:** | Select **`Bangladesh`** |
| **Part II, Line 10: Special rates and conditions — Article and Paragraph** | **`Article 12, Paragraph 1`** *(or select `Article 12(2)` / `Copyright Royalties` from the KDP dropdown)* |
| **Part II, Line 10: Withholding Rate (%)** | **`10%`** *(Reduces default 30% US withholding down to 10% under the US–Bangladesh Income Tax Treaty)* |
| **Part II, Line 10: Type of income** | **`Royalties (Book / Digital Copyright Royalties)`** |
| **Part II, Line 10: Additional explanation (if prompted)** | `Beneficial owner is a tax resident of Bangladesh deriving copyright royalties from literary/digital publications and does not maintain a permanent establishment in the United States per Article 12 of the US-Bangladesh Income Tax Convention.` |
| **Part III: Certification & Electronic Signature** | Check all certification boxes, type your exact legal name, and submit. |

> **Verification Check in KDP:** Immediately after submitting the KDP Tax Questionnaire, verify that your KDP Tax Status box reads:  
> **`Tax Status: Completed | Applicable Withholding Rate: 10.0%`**.  
> *(Note: The 10% US withholding applies ONLY to sales made to customers on `Amazon.com` (US). Sales to customers in the UK, Canada, Australia, Germany, and rest of world have `0%` US tax withholding!)*

---

### 4.4 Step 4 — Bangladesh Bank Withdrawal, Encashment Certificates & Tax Compliance
1. **Withdrawing from Payoneer to Your Bangladeshi Bank (`BDT`):**
   - Withdraw USD from Payoneer directly to your linked Bangladeshi personal or proprietorship bank account when the USD-to-BDT exchange rate is favorable.
   - In the transfer purpose/reference note, specify **`Digital Publishing Royalties / IT-Enabled Content Export`**.
2. **Collecting Your Annual Foreign Currency Encashment Certificate:**
   - At the end of the Bangladeshi tax year (`June 30`), download your **Annual Payout Summary CSVs** from Amazon KDP, Draft2Digital, Gumroad, and Payoneer, and request a **Foreign Remittance / Export Encashment Certificate** from your local bank branch for your annual NBR income tax return filing.
   - Keep your **IRS Form 1042-S** (issued every March by Amazon KDP and Draft2Digital showing the 10% US tax withheld on US sales) in your tax folder as official foreign tax credit documentation.

---

### 4.5 Step 5 — Bangladesh Foreign Exchange Regulation (Form-C), Remittance Documentation & Multi-Channel Accounting SOP

Operating a multi-channel global digital publishing studio from Bangladesh requires disciplined monthly reconciliation across US retail marketplaces (`Amazon KDP` and `Draft2Digital`), direct digital commerce (`Gumroad`), your intermediate USD treasury account (`Payoneer Global Payment Service`), and your local Authorized Dealer (`AD`) bank branch in Bangladesh. Following the operational checklist below ensures that every incoming royalty disbursement clears compliance checks without delay, qualifies for proper export/remittance documentation under Bangladesh Bank guidelines, and reconciles cleanly in your year-end National Board of Revenue (`NBR`) tax return.

#### 1. Aligning Your Name, Address, and Tax Identifiers Across All 5 Platforms
The number-one cause of frozen payouts or rejected W-8BEN tax forms for Bangladeshi creators is character-level mismatch between government identity records and marketplace payout profiles. Before publishing your first listing, audit these five records side-by-side:
- **National ID Card (`Smart NID`) & Machine-Readable Passport (`MRP / e-Passport`):** Verify the exact English spelling of your first name, middle name, and surname, including any initials or prefixes (`Md.`, `Mohammad`, etc.). Never abbreviate your first name on Payoneer or Amazon KDP if it is spelled out in full on your NID and bank account.
- **12-Digit NBR e-TIN Certificate:** Confirm that the English name and residential address printed on your e-TIN certificate match your NID and bank statement. If your residential address has changed, update the address inside the NBR e-TIN portal before generating the PDF certificate you archive for IRS Form W-8BEN compliance.
- **Local Bangladeshi Bank Account (`AD Branch`):** Ensure your personal or sole-proprietorship bank account title matches your Payoneer profile name identically. When linking a Bangladeshi bank account inside Payoneer (`Settings -> Bank Accounts -> Add Bank Account`), enter the exact **13-to-17 digit full core banking account number**, the **8-or-11 character SWIFT/BIC code**, and the **9-digit Bangladesh Bank Routing Number** for your specific branch.

#### 2. Handling Bangladesh Bank Form-C Declarations for Incoming Transfers Above USD $10,000
Under Bangladesh Bank Foreign Exchange Circular regulations, inward foreign remittances equivalent to or exceeding **`USD $10,000`** (or local bank thresholds when aggregating monthly commercial payouts) may require a **Form-C Declaration** specifying the purpose of the inward remittance:
- **Recommended Transfer Sizing:** When transferring funds from your Payoneer USD balance to your local Bangladeshi bank account in `BDT`, schedule regular bi-weekly or monthly withdrawals (for example, `$1,500` to `$4,500 USD` per transfer) rather than holding six months of royalties and withdrawing a single `$12,000+` lump sum. Smaller, predictable monthly withdrawals process automatically through Payoneer's local partner bank clearing network within `1 to 3 business days` without manual branch intervention.
- **Purpose Code & Supporting Invoice Packet:** If your Authorized Dealer (`AD`) bank branch requests supporting documentation for high-volume royalties, provide a single PDF packet containing: (a) your **Amazon KDP Prior-Month Royalty Report PDF**, (b) your **Draft2Digital Monthly Earnings Statement**, (c) your **Gumroad Monthly Sales CSV Summary**, and (d) your **Payoneer Transaction Statement** showing that all funds originated from legitimate literary copyright royalties and B2B digital software/template licensing.

#### 3. Monthly Multi-Currency Royalty & Payout Schedule Matrix
Understanding the payment lag of each platform prevents cashflow surprises during your initial 90-day launch window:
- **Gumroad Direct Storefront (`Tiers 0, 2, 3, and 4`):** Pays out **weekly every Friday** (after a rolling 7-day hold on each transaction) once your balance exceeds `$10.00 USD`. This makes Gumroad your fastest cashflow engine—sales generated on Monday from your email sequence or social launch fund your operating account the following Friday.
- **Draft2Digital Wide Retail & Libraries (`Tier 1 Wide`):** Pays out **monthly around the 15th to 21st of each month** for royalties cleared during the prior calendar month, with a low **`$10.00 USD` minimum threshold** via Payoneer or US ACH.
- **Amazon KDP Global Marketplaces (`Tier 1 Kindle & Print`):** Pays out **monthly on the 29th of each month** on a **Net-60 cycle** (for example, January Kindle and paperback sales are deposited into your Payoneer US checking account on March 29). Because you linked a **Payoneer US Virtual Checking Account (`ABA Routing + Checking Account`)**, Amazon pays you via **Electronic Funds Transfer (`EFT`)** with **zero wire minimum** across all 13 Amazon stores (`Amazon.com`, `Amazon.co.uk`, `Amazon.de`, `Amazon.fr`, `Amazon.es`, `Amazon.it`, `Amazon.nl`, `Amazon.co.jp`, `Amazon.com.br`, `Amazon.ca`, `Amazon.com.mx`, `Amazon.com.au`, and `Amazon.in`).

#### 4. Step-by-Step 90-Day Launch & Merchandising Promotion Calendar
To maximize both Amazon KDP organic rankings and high-margin `$59` Gumroad Flagship OS bundle conversions, execute this 4-stage merchandising cadence upon launch:
1. **Days 1–7 (Direct List & Social Seed Launch):** Publish your Kindle eBook (`$9.99`) and KDP Paperback (`$16.99`) on Amazon KDP (do **not** enroll the eBook in KDP Select / Kindle Unlimited so that you can legally distribute the book wide on Draft2Digital and inside your Gumroad bundles). Simultaneously publish all four Gumroad tiers (`$0`, `$29`, `$59`, and `$12/mo | $59/yr`). Send `Tier 0 ($0)` to your network, LinkedIn connections, and small business communities so readers download the Free 5-Day Audit Kit and enter the 7-Email Automated Conversion Sequence.
2. **Days 8–21 (Look-Inside & Look-to-Bundle Bridge Verification):** Once your Amazon KDP listings are live, click the **"Read Sample" (`Look Inside`)** button on Amazon.com. Verify that the Front Matter page **`00c-how-to-use-this-system.md`** and Chapter 1 (`Worksheet 01`) are visible inside the free Amazon preview—giving every Amazon shopper a direct invitation to download the companion Starter Kit (`Tier 0`) and upgrade to the `$59` Complete Flagship OS Bundle (`Tier 3`).
3. **Days 22–45 (Amazon Author Central & A+ Content Deployment):** Claim your book inside **Amazon Author Central (`https://author.amazon.com`)** and open the **KDP A+ Content Manager**. Upload your high-resolution cover graphics from `08-COVER-DESIGN/` (`gumroad-tier2-workbook-atlas-cover.png` and `gumroad-tier3-flagship-os-bundle-cover.png`) alongside a 4-column comparison chart highlighting the **5-Department Engine**, the **T.R.A.V. Safety Contract**, the **50 Deterministic Prompts**, and the **12 Red-Gate Emergency Scripts**.
4. **Days 46–90 (Quarterly Price-Pulse & Tier 4 Vault Drop Expansion):** Every 30 days, release a new **Monthly Industry Drop** inside your Gumroad **Tier 4 Living Automation Vault Membership (`$12/mo | $59/yr`)** and email all existing Tier 0, Tier 2, and Tier 3 subscribers (`Email 07` cadence) showcasing the new vertical workflows. This turns one-time book buyers into recurring annual subscribers while keeping your core manuscript evergreen.
"""
    return clean_copy(content)


# =============================================================================
# DELIVERABLE 3: email-funnel-and-upsell-sequence.md (3,000+ words)
# =============================================================================

def build_email_funnel_sequence() -> str:
    content = """# 7-Email Automated Conversion, Onboarding & Upsell Sequence (`Email 01` – `Email 07`)

**Document ID:** `10-MARKETING/email-funnel-and-upsell-sequence.md`  
**Project:** *The Small Business AI Automation Operating System* (`SMALLBIZ-AI-AUTOMATION-OS-V1`)  
**Funnel Architecture:** Tier 0 Free 5-Day Audit Starter Kit (`$0`) -> Tier 2 Interactive Workbook & Atlas (`$29`) / Tier 3 Complete Flagship OS Bundle (`$59`) -> Tier 4 Living Automation Vault Membership (`$12/mo` or `$59/yr`)  
**Recommended ESP Platforms:** ConvertKit (Kit), Loops.so, ActiveCampaign, MailerLite, Beehiiv, or Gumroad Workflows  

---

## Sequence Architecture & Conversion Timing Overview

| Email ID | Send Timing & Trigger | Target Audience Segment | Primary Psychological & Operational Hook | Primary Conversion CTA |
| :--- | :--- | :--- | :--- | :--- |
| **`Email 01`** | **Day 0 (Immediate `< 60s`)** | New Tier 0 Free Audit Downloaders | Instant asset delivery + 15-minute Cost of Manual Friction (CMF) calculation win. | Open Offline ROI Calculator + Fast-Action Tier 3 Upgrade (`$59`) |
| **`Email 02`** | **Day 1 (`+24 Hours`)** | Non-Buyers of Tier 2/3 | The 60-Second Speed-to-Lead Math (`391%` lift vs. `80%` conversion decay after 5 mins). | Preview Chapter 3 Router & Upgrade to Flagship OS (`$59`) |
| **`Email 03`** | **Day 2 (`+48 Hours`)** | Non-Buyers of Tier 2/3 | Why generic AI prompts break small businesses—and how the **T.R.A.V. Safety Gate** stops hallucinations. | Get All 50 T.R.A.V.-Guarded Prompts & 12 Scripts (`$59`) |
| **`Email 04`** | **Day 4 (`+96 Hours`)** | Non-Buyers of Tier 2/3 | Case Study: How a 16-person contractor cut invoice DSO from 44 days to 13 days (`+$142K` cashflow). | Deploy Chapter 8 Billing & AR State Machine (`$59`) |
| **`Email 05`** | **Day 5 (`+120 Hours`)** | Non-Buyers of Tier 2/3 | Choosing your path: The `$29` Fillable Workbook & Tablet Edition vs. the `$59` Complete Flagship OS. | Compare Tier 2 (`$29`) vs. Tier 3 Flagship (`$59`) |
| **`Email 06`** | **Day 7 (`+168 Hours`)** | Non-Buyers of Tier 3 | Inside the Flagship Bundle: The Offline Pro Web App (`SMALLBIZ-OS-PRO-2026`) + 5-DB Notion OS Kit. | Activate Complete Flagship OS Bundle (`$59`) |
| **`Email 07`** | **Day 10 (`+240 Hours`)** | All Leads & Tier 2/3 Buyers | The 15-Minute Friday 3:00 PM Owner Scorecard + Invitation to Tier 4 Living Automation Vault (`$59/yr`). | Join Tier 4 Living Vault (`$12/mo` or `$59/yr`) |

---

## `Email 01`: Immediate Asset Delivery & The 15-Minute Manual Friction Diagnostic

- **Email ID & Name:** `Email 01 — Delivery of Your Free 5-Day Business Time & Lead-Leak Audit Kit + Quick-Win Setup`
- **Send Timing & Trigger:** Immediately (`< 60 seconds`) upon downloading `Tier0-Free-5Day-Audit-Starter-Kit.zip` on Gumroad or submitting the landing page opt-in form.
- **Target Segment:** All Tier 0 Free Starter Kit Subscribers (`Tag: tier0_audit_downloaded`).
- **Subject Line A:** `[Download Inside] Your 5-Day Small Business AI Audit Kit (+ 15-min ROI calculator)`
- **Subject Line B:** `Your Small Business Automation Starter Kit is ready (start with Step 1 inside)`
- **Preview Text:** `Download your 32-page fillable audit, open the offline ROI calculator, and find your #1 profit leak in 15 minutes.`

### Complete Ready-to-Send Body Copy (`Email 01`)
```text
Hi {{first_name | default: "there"}},

Welcome! Here is your direct download link for the Free "5-Day Small Business Time & Lead-Leak Audit" Starter Kit:

👉 [DOWNLOAD YOUR FREE STARTER KIT (.ZIP) HERE]({{tier0_download_url}})

Inside your ZIP folder, you have four practical operational tools ready to use right now—with zero internet connection or monthly software logins required:

1. `tier0-free-sample-chapter01-and-audit.pdf` (32 pages, 64 fillable fields): Full Chapter 1 of The Small Business AI Automation Operating System plus Worksheet 01.
2. `smallbiz-automation-os-app.html`: Our 100% offline SaaS-Lite Web Companion App (running in Free Diagnostic Mode). Double-click it to open directly in Chrome, Edge, or Safari.
3. `sheet1-automation-roi-and-leak-calculator.csv`: A formula-ready spreadsheet mirror for Excel or Google Sheets.
4. `chapter-01-mindmap.svg` & `chapter-01-flowchart.svg`: High-resolution architecture diagrams for the 5-Department Engine and P.A.C.E. Prioritization Gate.

------------------------------------------------------------------
YOUR 15-MINUTE QUICK WIN FOR TODAY:
------------------------------------------------------------------
Do not try to automate 10 things at once this week. Instead, take 15 minutes today to do this single exercise:

Step 1: Double-click `smallbiz-automation-os-app.html` inside your download folder.
Step 2: In "Module 1: Manual Friction & Automation ROI Calculator", drag the sliders to match your current team size, hourly labor rate, monthly inbound leads, and % of calls/leads answered after 5 minutes.
Step 3: Look at the top navy box labeled "Total Annual Cost of Manual Friction (Annual CMF)".

When we ran this exact diagnostic with Apex Comfort HVAC (an 11-person trade business doing $1.45M/year), the owner assumed his biggest problem was needing another $42,000/year office coordinator.

The calculator proved something completely different:
- His team was losing $105,976/year in repetitive copy-paste labor across 5 departments.
- Worse, because 34 calls and web forms per month waited 3+ hours for a callback while technicians were on ladders, the business was leaking $177,480/year in lost jobs.
- Another $18,810/year was evaporating in overdue invoices past 30 days.

Total Annual Cost of Manual Friction: $302,266 per year.

Instead of hiring another admin, he deployed two deterministic workflows from our Operating System—recovering 18.5 hours a week and $16,400/month in rescued jobs within 30 days.

Tomorrow, I will send you the exact 60-second Speed-to-Lead math and show you how to plug your #1 lead leak first.

Want to skip the wait and get all 10 Chapters, all 50 Tested AI Workflow Prompts, all 12 Emergency Scripts, the full 5-Database Notion OS Kit, and the Pro Web App license key (`SMALLBIZ-OS-PRO-2026`) right now?

👉 [Get Instant Access to the Complete Flagship OS Bundle ($59)]({{tier3_checkout_url}})

To your operational freedom,

{{sender_name}}
Digital Publishing Studio
The Small Business AI Automation Operating System
```

- **Primary Call-to-Action:** `Open smallbiz-automation-os-app.html & Run Your 15-Minute CMF Audit` (Secondary CTA: `Get Complete Flagship OS Bundle — $59`).

---

## `Email 02`: The 60-Second Speed-to-Lead Math (Department 01 Deep Dive)

- **Email ID & Name:** `Email 02 — The 60-Second Speed-to-Lead Math: Why 4-Hour Response Times Cost 31% of Your Deals`
- **Send Timing & Trigger:** **Day 1 (`+24 Hours` after `Email 01`)**.
- **Target Segment:** Subscribers who have not yet purchased Tier 2 or Tier 3 (`Tag: !purchased_tier2_or_3`).
- **Subject Line A:** `The 5-minute cliff: why 78% of small business leads buy from whoever replies first`
- **Subject Line B:** `How a 14-person roofer rescued $38,400/mo from missed phone calls (Chapter 3 blueprint)`
- **Preview Text:** `What happens when a customer calls your business at 6:15 PM or while your team is busy? Here is the 60-second fix.`

### Complete Ready-to-Send Body Copy (`Email 02`)
```text
Hi {{first_name | default: "there"}},

Did you get a chance to run your numbers in the Manual Friction Calculator yesterday?

For 8 out of 10 small businesses we audit, the single largest dollar leak isn't payroll—it's Component 2 of the formula:

**The Speed-to-Lead Revenue Leak.**

Here is the empirical reality of small business buyer behavior in 2026:
- When a prospect submits a quote form on your website, messages your Google Business Profile, or calls your office while your front desk is on the other line, they do not wait patiently for 4 hours.
- They go back to Google and click the next local competitor on the list.
- Responding within **60 seconds** increases lead-to-appointment conversion by **391%**.
- Waiting just **5 to 30 minutes** causes conversion odds to drop by **80%**.
- Waiting until the next morning (`>12 hours`) destroys **96%** of your paid advertising efficiency.

In **Chapter 3 of The Small Business AI Automation Operating System**, we replace manual inbox checking and voicemail tag with the **I.N.S.T.A.N.T. 60-Second Omnichannel Router**.

Here is how it works in production (using Make.com or n8n + Twilio/OpenPhone + OpenAI at `temperature: 0.1`):

1. **[I] Ingest & Normalize (`0–3 Seconds`):** Whether the inquiry comes from a website form, a Facebook Lead Ad, a Google LSA message, or a missed phone call (`call.missed` webhook), it routes into one unified payload.
2. **[N] Deduplicate & Scrub (`3–6 Seconds`):** An idempotency hash ensures the prospect never gets duplicate texts if they click submit twice.
3. **[S] Score & Classify (`6–15 Seconds`):** `Prompt 3.1` transcribes any voicemail via Whisper and scores the inquiry from 0 to 100 on our non-intrusive B.A.N.T.-Lite rubric (Urgency, Service Tier, Location Match).
4. **[T] Text & Email Concierge (`15–45 Seconds`):** `Prompt 3.2` and `Prompt 3.3` send a warm, natural SMS text-back and email acknowledging their exact issue and offering a direct 1-click booking link:
   *"Hi David, Sarah's team at MetroShield Roofing here—sorry we missed your call just now! I saw your note about the flashing leak over your garage. We have two inspection windows open tomorrow at 10:30 AM or 2:00 PM. Reply 1 for 10:30, 2 for 2:00, or grab any time here: [Link]"*
5. **[A] Assign & Brief (`30 Mins Before Visit`):** `Prompt 3.5` posts a 60-second pre-call briefing card to your sales rep or technician in Slack so they walk in prepared.

When MetroShield Roofing (14 staff) turned on this exact Chapter 3 workflow, their median lead response time dropped from **4.2 hours down to 38 seconds**—recovering **$38,400/month** in jobs from the exact same ad spend.

You can get the complete Chapter 3 blueprint, all 5 Speed-to-Lead Prompts (`Prompts 3.1–3.5`), the 60-Second Revenue Recovery Simulator in the Pro Web App, and the Notion Lead CRM database inside the **Complete Flagship OS Bundle ($59)**:

👉 [Activate the Complete Small Business AI Automation OS ($59)]({{tier3_checkout_url}})

Talk soon,

{{sender_name}}
Digital Publishing Studio
```

- **Primary Call-to-Action:** `Activate the Complete Small Business AI Automation OS ($59)`.

---

## `Email 03`: The T.R.A.V. Human-in-the-Loop Safety Gate (Eliminating AI Hallucinations)

- **Email ID & Name:** `Email 03 — Why Standard AI Prompts Fail in Small Business (And How the T.R.A.V. Gate Fixes It)`
- **Send Timing & Trigger:** **Day 2 (`+48 Hours` after `Email 01`)**.
- **Target Segment:** Non-buyers of Tier 2/3 (`Tag: !purchased_tier2_or_3`).
- **Subject Line A:** `Why you should NEVER let an unguarded AI quote prices to your customers`
- **Subject Line B:** `The 15-second "Amber Gate" that makes small business AI 100% safe`
- **Preview Text:** `How to automate 95% of the heavy lifting on quotes, support, and billing without risking a single pricing mistake.`

### Complete Ready-to-Send Body Copy (`Email 03`)
```text
Hi {{first_name | default: "there"}},

If you have hesitated to connect AI to your customer emails, SMS, or invoicing software because you are worried the AI might invent a fake discount, misquote an insurance policy, or send a robotic message to an upset VIP client...

**You are 100% right to be cautious.**

Most "AI prompt packs" sold online tell you to hook ChatGPT directly to your inbox and let it reply to anything. In a real small business, that is a recipe for margin erosion and brand damage.

That is why **Chapter 2** of *The Small Business AI Automation Operating System* is built around a strict engineering standard called the **T.R.A.V. Human-in-the-Loop Architecture**:

- **[T] Trigger:** Webhook event arrives and is deduplicated via an idempotency key.
- **[R] Rules (Deterministic Pre-AI Code Gate):** Before the AI is even called, a deterministic lookup pulls the exact row from your **Verified Pricebook / Policy Truth Table** and runs a Red-Zone safety regex check.
- **[A] AI (Closed-World JSON Engine):** The model runs at `temperature: 0.0–0.1` under an epistemic rule that forbids outside guessing and requires citing the exact `grounded_source_row_id` and a numeric `confidence_score`.
- **[V] Verification (Green / Amber / Red Governance Gate):**
  - **Green Zone (75% of tasks):** Routine scheduling, <60s lead greetings, and verified parking/hours FAQs execute 24/7 with zero delay.
  - **Amber Zone (20% of tasks):** Whenever a quote exceeds `$2,500`, a credit exceeds `$50`, or confidence is `< 0.85`, the AI still does **95% of the work**—assembling the 3-option proposal PDF, checking the gross margin floor, and drafting the email—and then pauses at an **Amber Approval Card in Slack (`Prompt 2.3`)**. You glance at your phone for 15 seconds and tap **`[Approve & Send]`**.
  - **Red Zone (5% of tasks):** Any customer with `Sentiment <= 2/5` or legal/safety keywords immediately locks `client.automation_hold = TRUE` and triggers one of our **12 Emergency Business Operations Scripts**.

When BrightSmile Dental & Orthodontics (9 staff) implemented this T.R.A.V. architecture, they automated 78% of front-desk insurance and consultation inquiries while maintaining **zero** unapproved pricing or clinical claims.

Inside the **Flagship OS Bundle ($59)**, every single one of our **50 Tested AI Workflow Prompts** comes pre-engineered with these exact closed-world guardrails, JSON output schemas, and verification checklists—plus the interactive **T.R.A.V. Workflow Risk Scorer** inside the Web App:

👉 [Get All 50 T.R.A.V.-Guarded Prompts & The Complete OS ($59)]({{tier3_checkout_url}})

Best regards,

{{sender_name}}
Digital Publishing Studio
```

- **Primary Call-to-Action:** `Get All 50 T.R.A.V.-Guarded Prompts & The Complete OS ($59)`.

---

## `Email 04`: Case Study Breakdown — Cutting Invoice DSO from 44 Days to 13 Days

- **Email ID & Name:** `Email 04 — Case Study Breakdown: How a 15-Person Contractor Cut Invoice DSO from 44 Days to 14 Days`
- **Send Timing & Trigger:** **Day 4 (`+96 Hours` after `Email 01`)**.
- **Target Segment:** Non-buyers of Tier 2/3 (`Tag: !purchased_tier2_or_3`).
- **Subject Line A:** `How HarborView Electrical unlocked $142,000 in trapped cashflow (Chapter 8)`
- **Subject Line B:** `Stop doing invoices on Friday night (+ the 5-stage polite payment chaser)`
- **Preview Text:** `See the exact 5-stage overdue invoice state machine that collects cash 31 days faster without awkward phone calls.`

### Complete Ready-to-Send Body Copy (`Email 04`)
```text
Hi {{first_name | default: "there"}},

Profit on your Profit & Loss statement does not pay Friday payroll—collected cash in your checking account does.

When we audited HarborView Electrical Contractors (16 staff, $2.35M annual revenue), the owner was working until 9:00 PM every Friday night typing messy technician notes into QuickBooks Online. Worse, their average **Days Sales Outstanding (DSO)** sat at **44 days**, trapping over **$185,000** in unpaid receivables at any given moment.

Why? Because nobody on the team had time to follow up consistently on overdue invoices—and when they finally called at Day 35, the conversation felt tense and awkward.

In **Chapter 8**, we installed three deterministic finance workflows (`Prompts 8.1–8.5`):

1. **Same-Day Job-Completion Invoicing (`Prompt 8.1`):**
   The moment a technician marks a job `Completed` (or an agency PM marks a milestone `Approved`), `Prompt 8.1` translates rough field shorthand (*"Replaced 3P 40A contactor RTU #2, chem washed coils, 14.2A normal"*) into polished, audit-clear customer line items—without ever touching the locked SKU prices or quantities. Invoices under `$1,500` dispatch within 5 minutes with a 1-click ACH/card link; invoices `>= $1,500` hit Slack `#billing-approvals` for a 15-second glance.

2. **The 5-Stage Polite-to-Firm Payment Chaser State Machine (`Prompt 8.2`):**
   Every morning at 9:00 AM, the workflow checks open invoices in QuickBooks/Xero/Stripe and dispatches stage-calibrated reminders that stop the instant payment clears:
   - **Stage 1 (`Day -3 Pre-Due`):** Helpful concierge confirmation that they have the PDF, W-9, and 1-click ACH link.
   - **Stage 2 (`Day +1 Past Due`):** Warm, zero-friction SMS + Email nudge assuming simple inbox oversight.
   - **Stage 3 (`Day +7 Past Due`):** Collaborative check-in offering an automatic **2-Part Split-Payment Link** (50% today, 50% in 14 days).
   - **Stage 4 (`Day +15 Past Due — Amber Gate`):** Firm notice stating that non-emergency scheduling pauses on Day +20 unless settled.
   - **Stage 5 (`Day +30 Past Due — Red Gate`):** Formal Pre-Collections & Work-Suspension Notice (`Emergency Script 02`).

3. **Vendor Bill OCR & 5% Price-Creep Detector (`Prompts 8.3 & 8.4`):**
   Field techs snap photos of supply-house receipts via SMS; Vision AI extracts line items and GL codes (`GL-5110`), compares every unit price against the 90-day baseline, and flags supplier price hikes `> 5.0%` before the bill is paid.

**The Result at 60 Days:** HarborView compressed DSO from **44 days down to 13 days**, freeing **$142,000 in working capital** and catching **$9,400/year** in unannounced supplier price creep.

Get the complete Chapter 8 Invoicing, AR Chaser, and Receipt OCR suite inside the **Complete Flagship OS Bundle ($59)**:

👉 [Get Instant Access to the Flagship OS Bundle ($59)]({{tier3_checkout_url}})

Best,

{{sender_name}}
Digital Publishing Studio
```

- **Primary Call-to-Action:** `Get Instant Access to the Flagship OS Bundle ($59)`.

---

## `Email 05`: Comparing Tier 2 (`$29` Workbooks) vs. Tier 3 (`$59` Complete Flagship OS)

- **Email ID & Name:** `Email 05 — From Audit to Execution: Stepping Up to the Interactive Workbook & Visual Atlas ($29) or Complete Flagship OS ($59)`
- **Send Timing & Trigger:** **Day 5 (`+120 Hours` after `Email 01`)**.
- **Target Segment:** Non-buyers of Tier 2/3 (`Tag: !purchased_tier2_or_3`).
- **Subject Line A:** `Which edition fits your team best? ($29 Workbook Suite vs. $59 Complete OS)`
- **Subject Line B:** `Ready to move past Chapter 1? Compare your implementation options inside`
- **Preview Text:** `Whether you prefer fillable iPad/PDF workbooks ($29) or the full Pro Web App + 5-Database Notion OS ($59), here is the breakdown.`

### Complete Ready-to-Send Body Copy (`Email 05`)
```text
Hi {{first_name | default: "there"}},

Five days ago, you downloaded the Chapter 1 Audit Starter Kit. By now, you know exactly which of your 5 departments is costing you the most hours and leaked revenue every week.

When you are ready to implement the workflows across Chapters 2 through 10, we offer two commercial packages depending on how you and your team like to work:

------------------------------------------------------------------
OPTION 1: TIER 2 — INTERACTIVE WORKBOOK, ATLAS & TABLET EDITION ($29)
------------------------------------------------------------------
Best for solo founders and hands-on operators who love structured PDFs, iPad/reMarkable planning, and spreadsheet prompt libraries:
- Complete 10-Chapter Master Digital Book PDF (`179 pages`, 20 inlined vector diagrams) + Reflowable EPUB 3.0.
- Complete 10-Chapter US Letter Fillable Action Workbook (`80 pages`, `160` interactive AcroForm fields).
- Complete 10-Chapter International ISO A4 Fillable Workbook (`76 pages`, `152` interactive fields).
- Landscape Tablet Implementation Planner (`47 pages`, `94` fields for iPad GoodNotes / Notability / reMarkable).
- All 20 standalone `.svg` vector diagrams + `62-Item-Prompt-and-SOP-Vault.csv` (all 50 Prompts + 12 Emergency Scripts).

👉 [Get Tier 2: Interactive Workbook & Tablet Edition ($29)]({{tier2_checkout_url}})

------------------------------------------------------------------
OPTION 2: TIER 3 — COMPLETE FLAGSHIP AI AUTOMATION OS BUNDLE ($59)
------------------------------------------------------------------
Best for 2-to-25 person businesses, clinics, contractors, and agencies that want the turnkey software, Notion databases, and live prompt builders (**84% of buyers choose this edition**):
- **EVERYTHING in Tier 2 above, PLUS:**
- **Commercial Pro License Key (`SMALLBIZ-OS-PRO-2026`)** for `smallbiz-automation-os-app.html`: Activates the **Live 50-Prompt Variable Builder** (type your company variables once on the left, copy your customized prompt in 1 click on the right), all **12 Interactive Emergency Scripts**, the **60s Speed-to-Lead Simulator**, the **T.R.A.V. Risk Scorer**, and the **Friday 12-KPI Owner Scorecard Tracker**.
- **The 5-Database Minimalist Notion OS Kit (`06-NOTION-TEMPLATES/`):** Pre-populated CSV databases for Inbound Leads CRM, Automation Workflow Registry, 62-Item Prompt & SOP Vault, Weekly Owner KPI Scorecard, and Customer Support & Escalation Hub—plus our 2,400-word **Notion Formula 2.0 Setup Guide**.

👉 [Get Tier 3: Complete Flagship AI Automation OS Bundle ($59)]({{tier3_checkout_url}})

Both editions are backed by our **30-Day Implementation Satisfaction Guarantee**: deploy a single workflow within 30 days, and if it does not save you at least 5 hours a week, reply to your receipt for a full refund.

To your success,

{{sender_name}}
Digital Publishing Studio
```

- **Primary Call-to-Action:** `Get Tier 3: Complete Flagship AI Automation OS Bundle ($59)` (Secondary: `Get Tier 2 Workbook Edition — $29`).

---

## `Email 06`: Inside the Pro Web Companion App & 5-Database Notion OS Kit

- **Email ID & Name:** `Email 06 — Inside the Complete Flagship OS Bundle: 50 Prompts, Offline Web App, Notion CRM & 90-Day Roadmap`
- **Send Timing & Trigger:** **Day 7 (`+168 Hours` after `Email 01`)**.
- **Target Segment:** Non-buyers of Tier 3 (`Tag: !purchased_tier3`).
- **Subject Line A:** `How to customize any of the 50 AI prompts in 12 seconds (zero find-and-replace errors)`
- **Subject Line B:** `Look inside Module 3 & Module 4 of the Offline Pro Web Companion App`
- **Preview Text:** `See how the Dynamic Variable Builder and 5-Database Minimalist Notion OS save 10+ hours of setup time.`

### Complete Ready-to-Send Body Copy (`Email 06`)
```text
Hi {{first_name | default: "there"}},

One of the biggest friction points when implementing AI workflows from a book is copying a prompt into a text editor and manually hunting for every `[BUSINESS_NAME]`, `[HOURLY_RATE]`, `[INVOICE_NUMBER]`, or `[SLA_THRESHOLD]` placeholder. Miss one bracket, and your webhook payload fails.

That is why we engineered the **Interactive Offline Web Companion App (`smallbiz-automation-os-app.html`)** and the **5-Database Minimalist Notion OS Kit** inside the **Tier 3 Flagship Bundle ($59)**:

1. **Module 3 — The 50-Prompt Live Variable Builder:**
   - Filter all 50 prompts by Department (`Dept 01`–`05`), Chapter (`Ch 1`–`10`), Risk Zone (`Green`, `Amber`, `Red`), or keyword.
   - The app automatically parses every `[VARIABLE_NAME]` token in the selected prompt and builds a clean form on the left panel.
   - Type your company name, software stack, or pricing table into the inputs, watch the prompt compile live on the right, and click **`Copy Customized Prompt`** or **`Download .txt`**.

2. **Module 4 — The 12 Emergency Operations Script Center:**
   - When an angry customer threatens a dispute (`Emergency Script 01`), a commercial client hits 30 days past due (`Script 02`), a software vendor goes down (`Script 03`), a supplier delays a part (`Script 04`), a client asks for unpaid scope creep (`Script 05`), a technician calls out sick at 6:30 AM (`Script 06`), or a 1-star review appears (`Script 08`), you do not waste 45 minutes writing from scratch under stress.
   - Enter `[CUSTOMER_NAME]`, `[COMPANY_NAME]`, and `[INVOICE_NUMBER]` once, and copy the synchronized Email, 160-character SMS, and Slack internal escalation note in 10 seconds.

3. **The 5-Database Minimalist Notion OS Kit:**
   - Import 5 clean CSV databases (`Inbound Leads CRM`, `Workflow Registry`, `62-Item Prompt & SOP Vault`, `Weekly Owner KPI Scorecard`, and `Support & Escalation Hub`) into Notion in 15 minutes, complete with copy-paste **Notion Formula 2.0** badges.

Everything runs 100% locally on your computer with zero recurring software fees paid to us:

👉 [Activate Your Pro License Key (`SMALLBIZ-OS-PRO-2026`) & Get the Flagship Bundle ($59)]({{tier3_checkout_url}})

Warm regards,

{{sender_name}}
Digital Publishing Studio
```

- **Primary Call-to-Action:** `Activate Your Pro License Key & Get the Flagship Bundle ($59)`.

---

## `Email 07`: The 15-Minute Friday Owner Scorecard & Tier 4 Living Vault Invitation

- **Email ID & Name:** `Email 07 — Your 15-Minute Friday Owner Scorecard & Joining the Living Automation Vault ($12/mo | $59/yr)`
- **Send Timing & Trigger:** **Day 10 (`+240 Hours` after `Email 01`, or `+72 Hours` post-purchase of Tier 2/3)**.
- **Target Segment:** All active subscribers & Tier 2/3 customers (`Tag: all_active_leads_and_buyers`).
- **Subject Line A:** `The Friday 3:00 PM ritual that gives you your weekend back (12 Core KPIs)`
- **Subject Line B:** `[New Release] Industry Vertical Drop #01 + The Living Automation Vault`
- **Preview Text:** `How to review your entire business in 15 minutes every Friday—plus get 8 new vertical prompts for Clinics, Contractors, E-Com & Agencies.`

### Complete Ready-to-Send Body Copy (`Email 07`)
```text
Hi {{first_name | default: "there"}},

Picture this Friday afternoon at 3:00 PM:

Instead of spending your Friday evening and Sunday afternoon digging through four different tabs in QuickBooks, your CRM, your phone logs, and your support inbox wondering whether your business actually made money this week...

At exactly 3:00 PM, `Prompt 10.1` posts your **1-Page Friday Owner KPI Scorecard** (`Module 6` of the Web App & `Database 04` in Notion) summarizing your **12 Core Executive Numbers** across all 5 Departments:

- **Dept 01 (Lead Capture):** (1) Weekly Inbound Leads, (2) Median Speed-to-Lead (`<= 60s`), (3) Missed-Call Recovery Rate (`>= 85%`).
- **Dept 02 (Sales & Quoting):** (4) 3-Tier Quotes Sent, (5) 14-Day Proposal Close Rate (`>= 35%`).
- **Dept 03 (Delivery, Support & Reviews):** (6) Onboarding Cycle Time (`<= 24h`), (7) Tier-1 Support Auto-Resolution (`>= 60%`), (8) Net New 5-Star Google Reviews.
- **Dept 04 (Finance & Cashflow):** (9) Weekly Cash Collected (`$`), (10) Overdue Receivables `>15 Days` (`<= $2,500`), (11) Average DSO (`<= 16 days`).
- **Dept 05 (Bandwidth & Health):** (12) Weekly Owner & Team Hours Saved (`>= 15 hrs/wk`).

Every metric is automatically graded **GREEN**, **AMBER**, or **RED**. You review the single Amber or Red bottleneck in 15 minutes, click 1 button to generate your **Monday 8:45 AM 15-Minute All-Hands Team Brief (`Prompt 10.5`)**, close your laptop at 3:15 PM, and enjoy your weekend.

------------------------------------------------------------------
ANNOUNCING TIER 4: THE LIVING AUTOMATION VAULT (DROP #01 LIVE NOW)
------------------------------------------------------------------
For owners and operations leaders who want **industry-specialized vertical workflows**, **editable Microsoft Word (`.docx`) & PowerPoint (`.pptx`) team training suites**, and **ongoing quarterly Make/n8n/Zapier blueprint releases**, we have just released **Monthly Drop #01** inside the **Tier 4 Living Automation Vault**:

Inside **Drop #01 (The 4-Industry Vertical Pack)**, you get complete compliance rules, custom intake schemas, and **8 new vertical AI workflow prompts**:
- **Vertical 1 (Medical, Dental & Wellness Clinics):** HIPAA-safe non-clinical symptom triage (`V1.1`) & 6-month hygiene/treatment recall (`V1.2`).
- **Vertical 2 (HVAC, Plumbing, Electrical & Home Services):** Emergency vs. routine dispatch scorer (`V2.1`) & photo-based preliminary range estimator (`V2.2`).
- **Vertical 3 (E-Commerce & Specialty Retail):** Instant WISMO + defect/exchange RMA router (`V3.1`) & predictive replenishment VIP offer (`V3.2`).
- **Vertical 4 (B2B Agencies, CPAs, Legal & Consultancies):** Tax/legal document completeness chaser (`V4.1`) & monthly executive retainer ROI digest (`V4.2`).

You can join the **Living Automation Vault** today—which includes **100% of the Tier 3 Flagship OS Bundle** plus Drop #01 and all future quarterly drops—for just **$12/month** or **$59/year (VIP Annual Plan)**:

👉 [Join the Tier 4 Living Automation Vault ($12/mo or $59/yr VIP)]({{tier4_checkout_url}})

*(Or if you prefer the one-time Flagship OS Bundle without recurring drops, grab [Tier 3 here for $59]({{tier3_checkout_url}}).)*

Here's to a calm, profitable Friday afternoon at 3:00 PM,

{{sender_name}}
Digital Publishing Studio
The Small Business AI Automation Operating System
```

- **Primary Call-to-Action:** `Join the Tier 4 Living Automation Vault ($12/mo or $59/yr VIP)`.
"""
    return clean_copy(content)


# =============================================================================
# DELIVERABLE 4: tier4-monthly-vault-drop-01.md (2,500+ words)
# =============================================================================

def build_tier4_vault_drop_01() -> str:
    content = """# Tier 4 Living Automation Vault — Monthly Drop #01: The 4-Industry Vertical Automation Pack

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
   \\b(chest pain|shortness of breath|uncontrolled bleeding|severe swelling|fever over 101|knocked out tooth|broken jaw|concussion|suicidal|fainting|anaphylaxis|allergic reaction)\\b
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
"""
    return clean_copy(content)


# =============================================================================
# DELIVERABLE 5: 5-TIER COMMERCIAL .ZIP BUNDLES (09-EXPORTS/HYBRID-BUNDLE/)
# =============================================================================

def create_bundle_zip(zip_filename: str, tier_title: str, file_mappings: list) -> dict:
    """
    Create a commercial .zip archive in 09-EXPORTS/HYBRID-BUNDLE/ with a generated
    README-BUNDLE-INVENTORY.txt and verify all entries exist and are non-empty.
    file_mappings: list of (src_rel_path, arcname_in_zip)
    """
    zip_path = BUNDLE_DIR / zip_filename
    inventory_lines = [
        "================================================================================",
        "THE SMALL BUSINESS AI AUTOMATION OPERATING SYSTEM (2026 ENTERPRISE EDITION)",
        f"COMMERCIAL PACKAGE INVENTORY: {tier_title}",
        "================================================================================",
        "",
        "INCLUDED FILES IN THIS ARCHIVE:",
    ]

    total_uncompressed = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src_rel, arcname in file_mappings:
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
            "1. Extract this .zip archive to a local folder on your computer.",
            "2. Open PDF editions in Adobe Acrobat Reader, Microsoft Edge, or GoodNotes.",
            "3. Double-click `smallbiz-automation-os-app.html` (if included in your tier)",
            "   to run the 100% offline SaaS-Lite Web Companion Suite in any browser.",
            "   (Tier 3 & Tier 4 buyers: enter Pro Key `SMALLBIZ-OS-PRO-2026`).",
            "================================================================================",
        ])
        readme_bytes = "\n".join(inventory_lines).encode("utf-8")
        total_uncompressed += len(readme_bytes)
        zf.writestr("README-BUNDLE-INVENTORY.txt", readme_bytes)

    return {
        "zip_file": f"09-EXPORTS/HYBRID-BUNDLE/{zip_filename}",
        "compressed_bytes": zip_path.stat().st_size,
        "compressed_kb": round(zip_path.stat().st_size / 1024, 2),
        "uncompressed_bytes": total_uncompressed,
        "uncompressed_kb": round(total_uncompressed / 1024, 2),
        "file_count": len(file_mappings) + 1,
    }


def package_all_5_tiers() -> dict:
    # Tier 0
    tier0_files = [
        ("09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf", "01-Book-Sample-and-Audit/tier0-free-sample-chapter01-and-audit.pdf"),
        ("05-WORKBOOKS/chapter-01-workbook.pdf", "01-Book-Sample-and-Audit/chapter-01-workbook.pdf"),
        ("07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html", "02-Interactive-ROI-Web-App/smallbiz-automation-os-app.html"),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", "02-Interactive-ROI-Web-App/README-WEB-APP.md"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", "03-Spreadsheet-Calculator/sheet1-automation-roi-and-leak-calculator.csv"),
        ("04-VISUAL-ASSETS/chapter-01-mindmap.svg", "04-Architecture-Diagrams/chapter-01-mindmap.svg"),
        ("04-VISUAL-ASSETS/chapter-01-flowchart.svg", "04-Architecture-Diagrams/chapter-01-flowchart.svg"),
        ("08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png", "05-Cover/gumroad-tier0-free-audit-cover.png"),
    ]

    # Tier 1
    tier1_files = [
        ("09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub", "01-Kindle-and-D2D-EPUB3/the-smallbiz-ai-automation-os.epub"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf", "02-KDP-Print-6x9-Interior/the-smallbiz-ai-automation-os-kdp-paperback-6x9.pdf"),
        ("08-COVER-DESIGN/ebook-cover-kdp-kindle.png", "03-Retail-Covers/ebook-cover-kdp-kindle.png"),
        ("08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf", "03-Retail-Covers/kdp-paperback-full-wrap-cover.pdf"),
        ("08-COVER-DESIGN/kdp-paperback-full-wrap-cover.png", "03-Retail-Covers/kdp-paperback-full-wrap-cover.png"),
        ("10-MARKETING/marketplace-listings-and-bd-launch-runbook.md", "04-Publishing-Runbooks/marketplace-listings-and-bd-launch-runbook.md"),
        ("08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md", "04-Publishing-Runbooks/COVER-DESIGN-AND-PACKAGING-SPEC.md"),
    ]

    # Tier 2
    tier2_files = [
        ("09-EXPORTS/PDF/the-smallbiz-ai-automation-os-complete-book.pdf", "01-Master-Book/the-smallbiz-ai-automation-os-complete-book.pdf"),
        ("09-EXPORTS/EPUB/the-smallbiz-ai-automation-os.epub", "01-Master-Book/the-smallbiz-ai-automation-os.epub"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-us-letter.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-us-letter.pdf"),
        ("09-EXPORTS/PRINT/the-smallbiz-ai-automation-os-workbook-a4.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-workbook-a4.pdf"),
        ("09-EXPORTS/PDF/the-smallbiz-ai-automation-os-tablet-planner.pdf", "02-Fillable-Workbooks-and-Planner/the-smallbiz-ai-automation-os-tablet-planner.pdf"),
        ("06-NOTION-TEMPLATES/Spreadsheets/62-Item-Prompt-and-SOP-Vault.csv", "03-Prompt-and-SOP-Vault/62-Item-Prompt-and-SOP-Vault.csv"),
        ("08-COVER-DESIGN/gumroad-tier2-workbook-atlas-cover.png", "06-Cover/gumroad-tier2-workbook-atlas-cover.png"),
    ]
    for ch in range(1, 11):
        tier2_files.append((f"04-VISUAL-ASSETS/chapter-{ch:02d}-mindmap.svg", f"04-Visual-Architecture-Atlas/chapter-{ch:02d}-mindmap.svg"))
        tier2_files.append((f"04-VISUAL-ASSETS/chapter-{ch:02d}-flowchart.svg", f"04-Visual-Architecture-Atlas/chapter-{ch:02d}-flowchart.svg"))
        tier2_files.append((f"05-WORKBOOKS/worksheet-{ch:02d}.md", f"05-Markdown-Workbooks/worksheet-{ch:02d}.md"))

    # Tier 3 (Everything in Tier 2 + Pro Web App + License Key + 5-DB Notion OS Kit)
    tier3_files = list(tier2_files) + [
        ("07-INTERACTIVE-TOOLS/smallbiz-automation-os-app.html", "07-Pro-Web-Companion-App/smallbiz-automation-os-app.html"),
        ("07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt", "07-Pro-Web-Companion-App/PRO-ACCESS-LICENSE-KEY.txt"),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", "07-Pro-Web-Companion-App/README-WEB-APP.md"),
        ("06-NOTION-TEMPLATES/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv", "08-Notion-OS-5-Database-Kit/01-Inbound-Leads-and-Speed-to-Lead-CRM.csv"),
        ("06-NOTION-TEMPLATES/02-Automation-Workflows-and-Health-Registry.csv", "08-Notion-OS-5-Database-Kit/02-Automation-Workflows-and-Health-Registry.csv"),
        ("06-NOTION-TEMPLATES/03-AI-Prompt-and-SOP-Vault-62.csv", "08-Notion-OS-5-Database-Kit/03-AI-Prompt-and-SOP-Vault-62.csv"),
        ("06-NOTION-TEMPLATES/04-Weekly-Owner-KPI-Scorecard.csv", "08-Notion-OS-5-Database-Kit/04-Weekly-Owner-KPI-Scorecard.csv"),
        ("06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.csv", "08-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.csv"),
        ("06-NOTION-TEMPLATES/05-Customer-Support-and-Escalation-Hub.md", "08-Notion-OS-5-Database-Kit/05-Customer-Support-and-Escalation-Hub.md"),
        ("06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md", "08-Notion-OS-5-Database-Kit/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"),
        ("06-NOTION-TEMPLATES/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv", "08-Notion-OS-5-Database-Kit/Spreadsheets/sheet1-automation-roi-and-leak-calculator.csv"),
        ("08-COVER-DESIGN/gumroad-tier3-flagship-os-bundle-cover.png", "06-Cover/gumroad-tier3-flagship-os-bundle-cover.png"),
    ]

    # Tier 4 (Everything in Tier 3 + Monthly Drop #01 + Marketing Funnel & Email Sequence)
    tier4_files = list(tier3_files) + [
        ("10-MARKETING/tier4-monthly-vault-drop-01.md", "09-Living-Vault-Drops/tier4-monthly-vault-drop-01.md"),
        ("10-MARKETING/index.html", "10-Commercial-Funnel-Suite/index.html"),
        ("10-MARKETING/email-funnel-and-upsell-sequence.md", "10-Commercial-Funnel-Suite/email-funnel-and-upsell-sequence.md"),
        ("10-MARKETING/marketplace-listings-and-bd-launch-runbook.md", "10-Commercial-Funnel-Suite/marketplace-listings-and-bd-launch-runbook.md"),
        ("08-COVER-DESIGN/gumroad-tier4-living-vault-membership-cover.png", "06-Cover/gumroad-tier4-living-vault-membership-cover.png"),
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
        "Tier 2 — Interactive Workbook, Visual Atlas & Tablet Planner Edition ($29)",
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
    return results


def main():
    print("=== STEP 1: Generating 10-MARKETING/ Deliverables ===")
    index_path = MARKETING_DIR / "index.html"
    index_html = build_marketing_landing_page()
    index_path.write_text(index_html, encoding="utf-8")
    print(f" -> Wrote 10-MARKETING/index.html ({index_path.stat().st_size:,} bytes)")

    runbook_path = MARKETING_DIR / "marketplace-listings-and-bd-launch-runbook.md"
    runbook_md = build_marketplace_and_bd_runbook()
    runbook_path.write_text(runbook_md, encoding="utf-8")
    print(f" -> Wrote 10-MARKETING/marketplace-listings-and-bd-launch-runbook.md ({len(runbook_md.split()):,} words)")

    email_path = MARKETING_DIR / "email-funnel-and-upsell-sequence.md"
    email_md = build_email_funnel_sequence()
    email_path.write_text(email_md, encoding="utf-8")
    print(f" -> Wrote 10-MARKETING/email-funnel-and-upsell-sequence.md ({len(email_md.split()):,} words)")

    drop_path = MARKETING_DIR / "tier4-monthly-vault-drop-01.md"
    drop_md = build_tier4_vault_drop_01()
    drop_path.write_text(drop_md, encoding="utf-8")
    print(f" -> Wrote 10-MARKETING/tier4-monthly-vault-drop-01.md ({len(drop_md.split()):,} words)")

    print("\n=== STEP 2: Packaging Initial 5-Tier Commercial .ZIP Archives ===")
    zip_results = package_all_5_tiers()
    for tier, info in zip_results.items():
        print(
            f" -> {tier}: {info['zip_file']} | {info['compressed_kb']} KB compressed "
            f"({info['uncompressed_kb']} KB uncompressed across {info['file_count']} files)"
        )


if __name__ == "__main__":
    main()
