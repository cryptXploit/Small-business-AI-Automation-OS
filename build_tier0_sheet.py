import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter

STUDIO_ROOT = os.path.dirname(os.path.abspath(__file__))
SPREADSHEET_DIR = os.path.join(STUDIO_ROOT, "06-NOTION-TEMPLATES", "Spreadsheets")
os.makedirs(SPREADSHEET_DIR, exist_ok=True)
FILE_PATH = os.path.join(SPREADSHEET_DIR, "tier0-free-lite-command-sheet.xlsx")

wb = openpyxl.Workbook()

# Style definitions
NAVY_HEADER = "1E293B"      # Dark slate navy
EMERALD_ACCENT = "10B981"   # Emerald green
ACCENT_BLUE = "2563EB"      # Blue accent
LIGHT_GRAY = "F1F5F9"       # Row alternate
BORDER_COLOR = "CBD5E1"     # Light slate border
GOLD_ACCENT = "F59E0B"      # Amber gold

header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")

section_font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
section_fill = PatternFill(start_color=EMERALD_ACCENT, end_color=EMERALD_ACCENT, fill_type="solid")

bold_font = Font(name="Calibri", size=11, bold=True, color="0F172A")
normal_font = Font(name="Calibri", size=11, color="1E293B")
italic_font = Font(name="Calibri", size=10, italic=True, color="64748B")

thin_border = Border(
    left=Side(style='thin', color=BORDER_COLOR),
    right=Side(style='thin', color=BORDER_COLOR),
    top=Side(style='thin', color=BORDER_COLOR),
    bottom=Side(style='thin', color=BORDER_COLOR)
)

total_border = Border(
    left=Side(style='thin', color=BORDER_COLOR),
    right=Side(style='thin', color=BORDER_COLOR),
    top=Side(style='thin', color=BORDER_COLOR),
    bottom=Side(style='double', color="0F172A")
)

# ----------------------------------------------------------------------
# TAB 1: Chapter 1 Diagnostic & Core Allocation Calculator
# ----------------------------------------------------------------------
ws1 = wb.active
ws1.title = "Ch1-Diagnostic-Calculator"
ws1.views.sheetView[0].showGridLines = True

# Title block
ws1.merge_cells("A1:G1")
ws1["A1"] = "THE SMALL BUSINESS AI AUTOMATION OS — FREE TIER 0 DIAGNOSTIC CALCULATOR"
ws1["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
ws1["A1"].fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 35

ws1.merge_cells("A2:G2")
ws1["A2"] = "Author: OMAR SUNNY | System: Core Metric Framework (C.M.F.) & Speed-to-Lead ROI Model"
ws1["A2"].font = italic_font
ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[2].height = 20

# Instructions block
ws1.merge_cells("A4:G4")
ws1["A4"] = "DIAGNOSTIC WORKBENCH: Enter your weekly hours and hourly cost below to calculate annual operational leaks."
ws1["A4"].font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
ws1["A4"].fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
ws1["A4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws1.row_dimensions[4].height = 24

headers1 = [
    "Operational Bottleneck Area",
    "Current Process",
    "Weekly Manual Hours",
    "Hourly Rate ($/hr)",
    "Weekly Cost ($)",
    "Post-Automation Hours",
    "Annual Savings ($)"
]

ws1.row_dimensions[5].height = 26
for col_idx, h in enumerate(headers1, 1):
    cell = ws1.cell(row=5, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border

rows_data1 = [
    ("Speed-to-Lead Routing", "Manual lead copying & email alerts", 8, 35, 1),
    ("Customer Support Triage", "Repetitive FAQ inbox sorting", 12, 28, 2),
    ("Quote & Proposal Generation", "Manual PDF drafting & follow-up", 10, 45, 2),
    ("Invoice Chasing & AR Follow-up", "Manual reminder texting & logging", 6, 30, 1),
    ("Friday Reporting & Operations Sync", "Manual spreadsheet merging", 5, 50, 1),
    ("Data Sync & CRM Updating", "Re-typing customer contact records", 7, 25, 1)
]

for idx, (area, process, hours, rate, post_hrs) in enumerate(rows_data1, 6):
    ws1.cell(row=idx, column=1, value=area).font = bold_font
    ws1.cell(row=idx, column=2, value=process).font = normal_font
    
    c_hrs = ws1.cell(row=idx, column=3, value=hours)
    c_hrs.font = normal_font
    c_hrs.alignment = Alignment(horizontal="center")
    
    c_rate = ws1.cell(row=idx, column=4, value=rate)
    c_rate.font = normal_font
    c_rate.number_format = "$#,##0.00"
    c_rate.alignment = Alignment(horizontal="right")
    
    # Formula for Weekly Cost: Hours * Rate
    c_wk_cost = ws1.cell(row=idx, column=5, value=f"=C{idx}*D{idx}")
    c_wk_cost.font = bold_font
    c_wk_cost.number_format = "$#,##0.00"
    c_wk_cost.alignment = Alignment(horizontal="right")
    
    c_post = ws1.cell(row=idx, column=6, value=post_hrs)
    c_post.font = normal_font
    c_post.alignment = Alignment(horizontal="center")
    
    # Formula for Annual Savings: (Hours - PostHours) * Rate * 52
    c_sav = ws1.cell(row=idx, column=7, value=f"=ROUND((C{idx}-F{idx})*D{idx}*52, 2)")
    c_sav.font = Font(name="Calibri", size=11, bold=True, color="047857")
    c_sav.number_format = "$#,##0.00"
    c_sav.alignment = Alignment(horizontal="right")
    
    ws1.row_dimensions[idx].height = 22
    for c in range(1, 8):
        ws1.cell(row=idx, column=c).border = thin_border

# Totals row
tot_row = 12
ws1.cell(row=tot_row, column=1, value="TOTAL OPERATIONAL BENCHMARK").font = bold_font
ws1.cell(row=tot_row, column=2, value="Annual Cumulative Impact").font = italic_font
c_tot_hrs = ws1.cell(row=tot_row, column=3, value="=SUM(C6:C11)")
c_tot_hrs.font = bold_font
c_tot_hrs.alignment = Alignment(horizontal="center")

c_avg_rate = ws1.cell(row=tot_row, column=4, value="=AVERAGE(D6:D11)")
c_avg_rate.font = bold_font
c_avg_rate.number_format = "$#,##0.00"
c_avg_rate.alignment = Alignment(horizontal="right")

c_tot_wk = ws1.cell(row=tot_row, column=5, value="=SUM(E6:E11)")
c_tot_wk.font = bold_font
c_tot_wk.number_format = "$#,##0.00"
c_tot_wk.alignment = Alignment(horizontal="right")

c_tot_post = ws1.cell(row=tot_row, column=6, value="=SUM(F6:F11)")
c_tot_post.font = bold_font
c_tot_post.alignment = Alignment(horizontal="center")

c_tot_sav = ws1.cell(row=tot_row, column=7, value="=SUM(G6:G11)")
c_tot_sav.font = Font(name="Calibri", size=12, bold=True, color="065F46")
c_tot_sav.number_format = "$#,##0.00"
c_tot_sav.alignment = Alignment(horizontal="right")

ws1.row_dimensions[tot_row].height = 26
tot_fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
for c in range(1, 8):
    ws1.cell(row=tot_row, column=c).border = total_border
    ws1.cell(row=tot_row, column=c).fill = tot_fill

# Native OpenPyXL Chart: Manual Hours vs Post-Automation Hours
chart1 = BarChart()
chart1.type = "col"
chart1.style = 10
chart1.title = "Weekly Hours Comparison: Manual vs Post-Automation"
chart1.y_axis.title = "Weekly Hours"
chart1.x_axis.title = "Bottleneck Area"
chart1.width = 18
chart1.height = 10

data_ref = Reference(ws1, min_col=3, min_row=5, max_col=6, max_row=11)
cats_ref = Reference(ws1, min_col=1, min_row=6, max_row=11)
chart1.add_data(data_ref, titles_from_data=True)
chart1.set_categories(cats_ref)

ws1.add_chart(chart1, "A14")


# ----------------------------------------------------------------------
# TAB 2: Quick-Win 7-Day Action & ROI Tracker
# ----------------------------------------------------------------------
ws2 = wb.create_sheet(title="7-Day-Action-Tracker")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:G1")
ws2["A1"] = "7-DAY QUICK-WIN AUTOMATION AUDIT & IMPLEMENTATION TRACKER"
ws2["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
ws2["A1"].fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 35

ws2.merge_cells("A2:G2")
ws2["A2"] = "Complete 1 actionable automation step daily to unlock 10+ hours per week immediately."
ws2["A2"].font = italic_font
ws2["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[2].height = 20

headers2 = [
    "Sprint Day",
    "Focus Domain",
    "Specific Implementation Action",
    "Assigned Owner",
    "Status",
    "Expected Time Recovered (Hrs/Wk)",
    "Actual Impact Notes"
]

ws2.row_dimensions[4].height = 26
for col_idx, h in enumerate(headers2, 1):
    cell = ws2.cell(row=4, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border

tracker_tasks = [
    ("Day 1", "Diagnostic Audit", "Run Chapter 1 Diagnostic Calculator and establish baseline hourly cost", "Business Owner", "Completed", 2.0, "Identified $24k annual leak"),
    ("Day 2", "Inbound Speed-to-Lead", "Configure Google Form or Webhook to send instant SMS alert via Make.com", "Operations Lead", "In Progress", 4.0, "Sub-60s notification verified"),
    ("Day 3", "Support FAQ Caching", "Deploy Chapter 2 AI triage prompt with Amber approval guardrails", "Support Lead", "Ready", 3.5, "Deflects 45% repetitive inquiries"),
    ("Day 4", "Quote Standardization", "Implement 3-Option Instant Quote Generator formula sheet", "Sales Lead", "Ready", 3.0, "Faster proposal delivery"),
    ("Day 5", "AR Chaser Workflow", "Setup 5-stage automated overdue payment reminder sequence", "Finance Lead", "Ready", 2.5, "Shortens DSO by 9 days"),
    ("Day 6", "Team SOP Synchronization", "Import 01-Core-Starter-Database into Notion workspace", "Operations Lead", "Ready", 2.0, "Centralizes lead routing"),
    ("Day 7", "Friday Executive Review", "Generate 1st automated Friday 3:00 PM Owner KPI briefing", "Business Owner", "Ready", 3.0, "Replaces 2-hour manual sync")
]

for idx, (day, domain, action, owner, status, hrs, notes) in enumerate(tracker_tasks, 5):
    ws2.cell(row=idx, column=1, value=day).font = bold_font
    ws2.cell(row=idx, column=1).alignment = Alignment(horizontal="center")
    
    ws2.cell(row=idx, column=2, value=domain).font = bold_font
    ws2.cell(row=idx, column=3, value=action).font = normal_font
    
    c_owner = ws2.cell(row=idx, column=4, value=owner)
    c_owner.font = normal_font
    c_owner.alignment = Alignment(horizontal="center")
    
    c_status = ws2.cell(row=idx, column=5, value=status)
    c_status.font = bold_font
    c_status.alignment = Alignment(horizontal="center")
    if status == "Completed":
        c_status.fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    elif status == "In Progress":
        c_status.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    
    c_hrs = ws2.cell(row=idx, column=6, value=hrs)
    c_hrs.font = bold_font
    c_hrs.alignment = Alignment(horizontal="center")
    
    ws2.cell(row=idx, column=7, value=notes).font = normal_font
    
    ws2.row_dimensions[idx].height = 22
    for c in range(1, 8):
        ws2.cell(row=idx, column=c).border = thin_border

# Summary row
ws2.cell(row=12, column=1, value="TOTAL SPRINT WIN").font = bold_font
ws2.cell(row=12, column=2, value="Full 7-Day Sprint").font = italic_font
ws2.cell(row=12, column=5, value="Target Sum:").font = bold_font
ws2.cell(row=12, column=5).alignment = Alignment(horizontal="right")

c_tot_tracker = ws2.cell(row=12, column=6, value="=SUM(F5:F11)")
c_tot_tracker.font = Font(name="Calibri", size=12, bold=True, color="047857")
c_tot_tracker.alignment = Alignment(horizontal="center")

ws2.cell(row=12, column=7, value="Hours per week recovered permanently").font = bold_font

ws2.row_dimensions[12].height = 26
for c in range(1, 8):
    ws2.cell(row=12, column=c).border = total_border
    ws2.cell(row=12, column=c).fill = tot_fill


# ----------------------------------------------------------------------
# TAB 3: Teaser Roadmap Tab (Remaining 6 Pro Tabs Preview)
# ----------------------------------------------------------------------
ws3 = wb.create_sheet(title="Pro-OS-8Tab-Command-Center")
ws3.views.sheetView[0].showGridLines = True

ws3.merge_cells("A1:F1")
ws3["A1"] = "THE COMPLETE 8-TAB COMMERCIAL EXCEL COMMAND CENTER (TIER 3 / TIER 4)"
ws3["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
ws3["A1"].fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 35

ws3.merge_cells("A2:F2")
ws3["A2"] = "You are currently viewing the Tier 0 Free Lite Edition. Upgrade to Tier 3 Flagship ($59) to unlock all 8 tabs with live dynamic formulas."
ws3["A2"].font = Font(name="Calibri", size=11, bold=True, color="B45309")
ws3["A2"].fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
ws3["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[2].height = 25

headers3 = [
    "Sheet #",
    "Tab Title & Module",
    "Edition Status",
    "Key Capabilities & Built-in Formulas",
    "Target Outcome",
    "Unlock Level"
]

ws3.row_dimensions[4].height = 26
for col_idx, h in enumerate(headers3, 1):
    cell = ws3.cell(row=4, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

pro_tabs = [
    ("Tab 1", "Ch1 Automation ROI & Leak Calculator", "UNLOCKED (Free Tier 0)", "C.M.F. calculations, hourly leak benchmarks, 1 embedded chart", "Identify immediate $20k+ leaks", "Free Tier 0"),
    ("Tab 2", "5-Day Time & Task Forensic Audit", "UNLOCKED (Free Tier 0)", "7-day sprint tracker, recoverable hour formulas", "Recover 10+ hours in week one", "Free Tier 0"),
    ("Tab 3", "Speed-to-Lead Latency & Recovery Model", "LOCKED IN PRO OS", "Decay curve modeling, conversion multiplier formulas, sub-60s vs 24hr ROI", "Double inbound lead conversion", "Tier 3 Flagship ($59)"),
    ("Tab 4", "3-Option Quote & 14-Day Nurture ROI", "LOCKED IN PRO OS", "Decoy pricing matrix, margin simulator, follow-up touchpoint tracker", "Increase average deal size by 28%", "Tier 3 Flagship ($59)"),
    ("Tab 5", "Support Deflection & 90-Day Win-Back", "LOCKED IN PRO OS", "First-contact resolution formulas, CSAT metrics, churn prevention ROI", "Cut support ticket load by 60%", "Tier 3 Flagship ($59)"),
    ("Tab 6", "Invoicing, AR Chasers & DSO Cashflow", "LOCKED IN PRO OS", "5-tier automated aging bucket simulator, interest recovery formulas", "Reduce Days Sales Outstanding by 35%", "Tier 3 Flagship ($59)"),
    ("Tab 7", "Friday 16-Week Owner KPI Scorecard", "LOCKED IN PRO OS", "Automated weekly health index, amber risk triggers, rolling variance", "Reclaim entire weekends as owner", "Tier 3 Flagship ($59)"),
    ("Tab 8", "90-Day Rollout & Tool Stack Budget", "LOCKED IN PRO OS", "Zapier vs Make vs n8n cost calculator, self-funding automation tracker", "Full enterprise deployment plan", "Tier 3 Flagship ($59)")
]

for idx, (num, name, status, caps, outcome, level) in enumerate(pro_tabs, 5):
    ws3.cell(row=idx, column=1, value=num).font = bold_font
    ws3.cell(row=idx, column=1).alignment = Alignment(horizontal="center")
    
    ws3.cell(row=idx, column=2, value=name).font = bold_font
    
    c_stat = ws3.cell(row=idx, column=3, value=status)
    c_stat.font = bold_font
    c_stat.alignment = Alignment(horizontal="center")
    if "UNLOCKED" in status:
        c_stat.fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    else:
        c_stat.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
        c_stat.font = Font(name="Calibri", size=10, bold=True, color="991B1B")
        
    ws3.cell(row=idx, column=4, value=caps).font = normal_font
    ws3.cell(row=idx, column=5, value=outcome).font = normal_font
    
    c_lvl = ws3.cell(row=idx, column=6, value=level)
    c_lvl.font = bold_font
    c_lvl.alignment = Alignment(horizontal="center")
    if "Free" in level:
        c_lvl.fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    else:
        c_lvl.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
        c_lvl.font = Font(name="Calibri", size=11, bold=True, color="92400E")
        
    ws3.row_dimensions[idx].height = 24
    for c in range(1, 7):
        ws3.cell(row=idx, column=c).border = thin_border

# Upgrade CTA Banner at row 15
ws3.merge_cells("A14:F14")
ws3["A14"] = "⚡ READY TO UNLOCK THE COMPLETE 8-TAB FINANCIAL & ROI COMMAND CENTER?"
ws3["A14"].font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
ws3["A14"].fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
ws3["A14"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[14].height = 30

ws3.merge_cells("A15:F15")
ws3["A15"] = "Visit your Gumroad product portal or use code STUDIO-PRO-OS-2026 to activate Tier 3 Flagship ($59) instantly."
ws3["A15"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
ws3["A15"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[15].height = 25


# Auto-fit columns across all sheets
for ws in [ws1, ws2, ws3]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if '\n' in val_str:
                val_str = max(val_str.split('\n'), key=len)
            if len(val_str) > max_len and cell.row > 2:  # ignore merged title row
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

# Specific tweaks
ws1.column_dimensions['A'].width = 32
ws1.column_dimensions['B'].width = 38
ws1.column_dimensions['G'].width = 22

ws2.column_dimensions['A'].width = 14
ws2.column_dimensions['B'].width = 24
ws2.column_dimensions['C'].width = 46
ws2.column_dimensions['G'].width = 38

ws3.column_dimensions['B'].width = 38
ws3.column_dimensions['D'].width = 46
ws3.column_dimensions['E'].width = 36

wb.save(FILE_PATH)
print(f"Created Tier 0 Lite Command Sheet successfully at: {FILE_PATH}")
