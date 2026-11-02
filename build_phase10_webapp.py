import os
import re
import json
import shutil

STUDIO_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(STUDIO_ROOT, "07-INTERACTIVE-TOOLS", "smallbiz-automation-os-app.html")

print("Reading existing web app master data...")
with open(APP_PATH, "r", encoding="utf-8") as f:
    orig_content = f.read()

p_data_pos = orig_content.find("const PROMPTS_DATA =")
s_data_pos = orig_content.find("const EMERGENCY_SCRIPTS_DATA =")
after_scripts_pos = orig_content.find("];\n    const OFFICIAL_PRO_KEY = ", s_data_pos)
if after_scripts_pos == -1:
    after_scripts_pos = orig_content.find("];\n    const LICENSE_CODES = ", s_data_pos)
if after_scripts_pos == -1:
    after_scripts_pos = orig_content.find("];\n", s_data_pos)

data_block = orig_content[p_data_pos : after_scripts_pos + 2]
print(f"Extracted master data block: {len(data_block):,} chars")

# Construct the upgraded web app
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Small Business AI Automation Operating System — Interactive Companion Suite (2026 Enterprise Edition)</title>
  <meta name="author" content="OMAR SUNNY" />
  <meta name="description" content="100% Offline Interactive Operations Suite: C.M.F. Friction & ROI Calculator, Speed-to-Lead Simulator, 50-Prompt Variable Builder, 12 Emergency Scripts, T.R.A.V. Risk Scorer, and Friday Owner KPI Scorecard with full CRUD, localStorage persistence, and 3-Tier Value Ladder." />
  <style>
    :root {{
      --primary: #0F172A;
      --primary-light: #1E293B;
      --accent: #059669;
      --accent-hover: #047857;
      --accent-soft: #ECFDF5;
      --secondary: #0284C7;
      --secondary-soft: #F0F9FF;
      --purple: #7C3AED;
      --purple-soft: #F5F3FF;
      --warning: #D97706;
      --warning-soft: #FFFBEB;
      --danger: #DC2626;
      --danger-soft: #FEF2F2;
      --text: #1E293B;
      --muted: #64748B;
      --border: #CBD5E1;
      --surface: #F8FAFC;
      --bg: #FFFFFF;
      --radius: 10px;
      --shadow: 0 4px 16px rgba(15, 23, 42, 0.07);
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      color: var(--text);
      background-color: var(--surface);
      line-height: 1.55;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Topbar & 3-Tier Bar */
    .topbar {{
      background-color: var(--primary);
      color: #FFFFFF;
      padding: 14px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-icon {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--accent) 0%, #0284C7 100%);
      color: #FFFFFF;
      font-weight: 800;
      font-size: 18px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
      user-select: none;
    }}

    .brand-title {{
      font-size: 17px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }}

    .brand-subtitle {{
      font-size: 12px;
      color: #94A3B8;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .topbar-controls {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    /* 3-Tier Selector Group */
    .tier-selector-group {{
      display: inline-flex;
      background: rgba(255, 255, 255, 0.1);
      padding: 4px;
      border-radius: 10px;
      gap: 4px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }}

    .tier-btn {{
      background: transparent;
      border: none;
      color: #CBD5E1;
      padding: 6px 14px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}

    .tier-btn:hover {{
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.08);
    }}

    .tier-btn.active.tier-0 {{
      background: var(--accent);
      color: #FFFFFF;
      box-shadow: 0 2px 6px rgba(5, 150, 105, 0.4);
    }}

    .tier-btn.active.tier-2 {{
      background: var(--secondary);
      color: #FFFFFF;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.4);
    }}

    .tier-btn.active.tier-3 {{
      background: var(--purple);
      color: #FFFFFF;
      box-shadow: 0 2px 6px rgba(124, 58, 237, 0.4);
    }}

    .edition-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 5px 12px;
      border-radius: 9999px;
    }}

    .edition-badge.free {{
      background-color: rgba(16, 185, 129, 0.15);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .edition-badge.tier2 {{
      background-color: rgba(56, 189, 248, 0.15);
      color: #38BDF8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    .edition-badge.pro {{
      background-color: rgba(167, 139, 250, 0.15);
      color: #C084FC;
      border: 1px solid rgba(167, 139, 250, 0.3);
    }}

    /* Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 8px;
      border: 1px solid transparent;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.18s ease;
      white-space: nowrap;
    }}

    .btn-sm {{
      padding: 5px 10px;
      font-size: 12px;
      border-radius: 6px;
    }}

    .btn-accent {{
      background-color: var(--accent);
      color: #FFFFFF;
    }}
    .btn-accent:hover {{
      background-color: var(--accent-hover);
    }}

    .btn-secondary {{
      background-color: var(--secondary);
      color: #FFFFFF;
    }}
    .btn-secondary:hover {{
      background-color: #0369A1;
    }}

    .btn-purple {{
      background-color: var(--purple);
      color: #FFFFFF;
    }}
    .btn-purple:hover {{
      background-color: #6D28D9;
    }}

    .btn-outline {{
      background-color: transparent;
      color: var(--text);
      border-color: var(--border);
    }}
    .btn-outline:hover {{
      background-color: #F1F5F9;
    }}

    .btn-dark-outline {{
      background-color: transparent;
      color: #E2E8F0;
      border-color: #475569;
    }}
    .btn-dark-outline:hover {{
      background-color: rgba(255, 255, 255, 0.08);
      color: #FFFFFF;
    }}

    .btn-danger-outline {{
      background-color: transparent;
      color: var(--danger);
      border-color: #FCA5A5;
    }}
    .btn-danger-outline:hover {{
      background-color: var(--danger-soft);
    }}

    /* Navigation Tabs */
    .nav-tabs {{
      background-color: #FFFFFF;
      border-bottom: 1px solid var(--border);
      display: flex;
      overflow-x: auto;
      padding: 0 24px;
      gap: 8px;
    }}

    .nav-tab {{
      background: none;
      border: none;
      border-bottom: 3px solid transparent;
      color: var(--muted);
      font-family: inherit;
      font-size: 14px;
      font-weight: 600;
      padding: 14px 16px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      transition: all 0.15s ease;
    }}

    .nav-tab:hover {{
      color: var(--text);
    }}

    .nav-tab.active {{
      color: var(--primary);
      border-bottom-color: var(--accent);
    }}

    .tab-pill {{
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 9999px;
      background-color: #E2E8F0;
      color: var(--primary-light);
      font-weight: 700;
    }}

    .nav-tab.active .tab-pill {{
      background-color: var(--accent-soft);
      color: var(--accent);
    }}

    /* Main Container */
    main {{
      flex: 1;
      padding: 28px 24px;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
    }}

    .module-section {{
      display: none;
    }}
    .module-section.active {{
      display: block;
    }}

    /* Dynamic Thirst Teaser Banner */
    .thirst-teaser-banner {{
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
      border: 1px solid #334155;
      border-left: 5px solid var(--accent);
      border-radius: var(--radius);
      padding: 18px 22px;
      color: #FFFFFF;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
      animation: fadeIn 0.3s ease;
    }}

    .thirst-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .thirst-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(16, 185, 129, 0.2);
      color: #34D399;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 0.05em;
    }}

    .thirst-title {{
      font-size: 15px;
      font-weight: 700;
      color: #F8FAFC;
    }}

    .thirst-body {{
      font-size: 13px;
      color: #CBD5E1;
      line-height: 1.6;
    }}

    .thirst-body strong {{
      color: #FCD34D;
    }}

    .thirst-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 4px;
    }}

    /* Cards & Layout */
    .card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow);
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 18px;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .card-title {{
      font-size: 18px;
      font-weight: 700;
      color: var(--primary);
    }}

    .card-desc {{
      font-size: 13px;
      color: var(--muted);
      margin-top: 4px;
    }}

    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }}

    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}

    @media (max-width: 900px) {{
      .grid-2, .grid-3, .grid-4 {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Forms & Inputs */
    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 14px;
    }}

    .form-label {{
      font-size: 12px;
      font-weight: 600;
      color: var(--text);
    }}

    .form-input, .form-select {{
      font-family: inherit;
      font-size: 13px;
      padding: 9px 12px;
      border-radius: 7px;
      border: 1px solid var(--border);
      background-color: #FFFFFF;
      color: var(--text);
      outline: none;
      transition: border-color 0.15s ease;
    }}

    .form-input:focus, .form-select:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.15);
    }}

    /* CRUD Toolbars & Tables */
    .crud-toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px dashed var(--border);
    }}

    .crud-actions-left {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .crud-actions-right {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .table-wrap {{
      overflow-x: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
      position: relative;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    th {{
      background-color: #F1F5F9;
      color: var(--primary);
      font-weight: 700;
      padding: 10px 14px;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }}

    td {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:hover td {{
      background-color: #F8FAFC;
    }}

    .cell-editable {{
      cursor: pointer;
      position: relative;
      border-radius: 4px;
      padding: 2px 4px;
      transition: background-color 0.15s;
    }}

    .cell-editable:hover {{
      background-color: #FEF3C7;
      outline: 1px dashed #D97706;
    }}

    .row-delete-btn {{
      background: none;
      border: none;
      color: #94A3B8;
      cursor: pointer;
      font-size: 14px;
      padding: 4px 6px;
      border-radius: 4px;
      transition: all 0.15s;
    }}

    .row-delete-btn:hover {{
      color: var(--danger);
      background-color: var(--danger-soft);
    }}

    .badge-custom {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #E0E7FF;
      color: #3730A3;
      font-weight: 700;
      margin-left: 6px;
    }}

    /* Glassmorphism Blur & Locked Rows */
    .glassmorphism, .glass-blurred-wrapper {{
      position: relative;
    }}

    .glass-blurred-content {{
      filter: blur(5px);
      backdrop-filter: blur(8px);
      opacity: 0.55;
      pointer-events: none;
      user-select: none;
      transition: all 0.3s ease;
    }}

    .glass-lock-overlay {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      padding: 24px 30px;
      text-align: center;
      color: #FFFFFF;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.35);
      z-index: 10;
      max-width: 480px;
      width: 90%;
    }}

    .glass-lock-overlay h4 {{
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 8px;
      color: #F8FAFC;
    }}

    .glass-lock-overlay p {{
      font-size: 12px;
      color: #CBD5E1;
      margin-bottom: 16px;
      line-height: 1.5;
    }}

    /* Stat Cards */
    .stat-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }}

    .stat-label {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
    }}

    .stat-value {{
      font-size: 24px;
      font-weight: 800;
      color: var(--primary);
      margin-top: 4px;
    }}

    .stat-value.accent {{
      color: var(--accent);
    }}

    .stat-sub {{
      font-size: 11px;
      color: var(--muted);
      margin-top: 2px;
    }}

    /* Personal Notes & Action Log Box */
    .module-notes-box {{
      background-color: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px 20px;
      margin-top: 24px;
      box-shadow: var(--shadow);
    }}

    .module-notes-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}

    .module-notes-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .notes-status {{
      font-size: 11px;
      color: #64748B;
      font-weight: 500;
    }}

    .module-notes-textarea {{
      width: 100%;
      height: 90px;
      font-family: inherit;
      font-size: 13px;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: 7px;
      background: var(--surface);
      color: var(--text);
      resize: vertical;
      outline: none;
      transition: all 0.15s ease;
    }}

    .module-notes-textarea:focus {{
      border-color: var(--secondary);
      background: #FFFFFF;
      box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.15);
    }}

    /* Prompts & Scripts Viewer */
    .item-browser-grid {{
      display: grid;
      grid-template-columns: 340px 1fr;
      gap: 20px;
    }}

    @media (max-width: 960px) {{
      .item-browser-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .item-list {{
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #FFFFFF;
      max-height: 620px;
      overflow-y: auto;
    }}

    .item-list-entry {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .item-list-entry:hover {{
      background: #F8FAFC;
    }}

    .item-list-entry.active {{
      background: var(--accent-soft);
      border-left: 4px solid var(--accent);
    }}

    .item-list-entry.locked {{
      opacity: 0.75;
      background: #F9FAFB;
    }}

    .item-tag-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    .item-tag {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      background: #E2E8F0;
      color: #334155;
    }}

    .item-lock-pill {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      background: #FEF3C7;
      color: #92400E;
    }}

    .item-title {{
      font-size: 13px;
      font-weight: 600;
      color: var(--primary);
    }}

    .item-preview-pane {{
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .prompt-box {{
      background: #0F172A;
      color: #E2E8F0;
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 16px;
      border-radius: 8px;
      max-height: 380px;
      overflow-y: auto;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.6;
      border: 1px solid #334155;
    }}

    /* Modals */
    .modal-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 16px;
    }}

    .modal-backdrop.open {{
      display: flex;
    }}

    .modal-box {{
      background: #FFFFFF;
      border-radius: 12px;
      max-width: 540px;
      width: 100%;
      padding: 28px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border);
      animation: modalSlide 0.2s ease;
    }}

    @keyframes modalSlide {{
      from {{ transform: translateY(12px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    .modal-title {{
      font-size: 18px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
    }}

    .modal-desc {{
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 20px;
      line-height: 1.5;
    }}

    .modal-footer {{
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 22px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }}

    /* Toast */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--primary);
      color: #FFFFFF;
      font-size: 13px;
      font-weight: 600;
      padding: 12px 20px;
      border-radius: 8px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      border-left: 4px solid var(--accent);
      z-index: 2000;
      display: none;
      animation: toastIn 0.25s ease;
    }}

    @keyframes toastIn {{
      from {{ transform: translateY(20px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    /* Print Styles */
    @media print {{
      .topbar, .nav-tabs, .crud-toolbar, .module-notes-box, .thirst-actions,
      .glass-lock-overlay, .btn, .modal-backdrop, .toast {{
        display: none !important;
      }}
      body {{
        background: #FFF !important;
        color: #000 !important;
      }}
      main {{
        padding: 0 !important;
        max-width: 100% !important;
      }}
      .card {{
        border: 1px solid #CCC !important;
        box-shadow: none !important;
        page-break-inside: avoid;
        margin-bottom: 20px !important;
      }}
      .module-section {{
        display: block !important;
        page-break-after: always;
      }}
      .glass-blurred-content {{
        filter: none !important;
        opacity: 1 !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- Sticky Topbar with 3-Tier Access System -->
  <header class="topbar">
    <div class="brand-wrap">
      <div class="brand-icon">OS</div>
      <div>
        <div class="brand-title">The Small Business AI Automation Operating System</div>
        <div class="brand-subtitle">
          <span>Author: OMAR SUNNY</span>
          <span>•</span>
          <span>100% Offline SaaS-Lite Suite</span>
        </div>
      </div>
    </div>

    <div class="topbar-controls">
      <!-- 3-Tier Progressive Value Ladder Bar -->
      <div class="tier-selector-group" role="group" aria-label="Edition Level Selector">
        <button type="button" class="tier-btn tier-0 active" onclick="selectTier(0)">
          <span>🟢 Tier 0: Free Diagnostic</span>
        </button>
        <button type="button" class="tier-btn tier-2" onclick="selectTier(2)">
          <span>🔵 Tier 2: Workbook ($29)</span>
        </button>
        <button type="button" class="tier-btn tier-3" onclick="selectTier(3)">
          <span>🟣 Tier 3: Flagship OS ($59)</span>
        </button>
      </div>

      <span id="editionStatusBadge" class="edition-badge free">🟢 TIER 0: FREE DIAGNOSTIC</span>

      <button type="button" class="btn btn-dark-outline btn-sm" onclick="openActivationModal()">
        🔑 Enter Code
      </button>

      <button type="button" class="btn btn-dark-outline btn-sm" onclick="openBackupModal()">
        💾 Backup / Restore
      </button>

      <button type="button" class="btn btn-dark-outline btn-sm" onclick="window.print()">
        🖨️ Print / PDF
      </button>
    </div>
  </header>

  <!-- Module Navigation Tabs -->
  <nav class="nav-tabs" role="tablist">
    <button type="button" class="nav-tab active" data-target="module-1" onclick="switchModule('module-1')">
      1. Friction &amp; ROI Calculator <span class="tab-pill">FREE + CRUD</span>
    </button>
    <button type="button" class="nav-tab" data-target="module-2" onclick="switchModule('module-2')">
      2. 60s Speed-to-Lead Simulator <span class="tab-pill">LATENCY</span>
    </button>
    <button type="button" class="nav-tab" data-target="module-3" onclick="switchModule('module-3')">
      3. 50-Prompt Vault &amp; Builder <span class="tab-pill">50 PROMPTS</span>
    </button>
    <button type="button" class="nav-tab" data-target="module-4" onclick="switchModule('module-4')">
      4. 12 Emergency Ops Scripts <span class="tab-pill">12 SCRIPTS</span>
    </button>
    <button type="button" class="nav-tab" data-target="module-5" onclick="switchModule('module-5')">
      5. T.R.A.V. Risk &amp; 90-Day Tracker <span class="tab-pill">GOVERNANCE</span>
    </button>
    <button type="button" class="nav-tab" data-target="module-6" onclick="switchModule('module-6')">
      6. Friday Owner KPI Scorecard <span class="tab-pill">EXECUTIVE</span>
    </button>
  </nav>

  <!-- Main Application Body -->
  <main>

    <!-- ================================================================= -->
    <!-- MODULE 1: MANUAL FRICTION & ROI CALCULATOR (CMF ENGINE)           -->
    <!-- ================================================================= -->
    <section id="module-1" class="module-section active">
      
      <!-- Preset scenarios banner -->
      <div class="card" style="padding:16px 20px; margin-bottom:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
          <div style="font-size:13px; font-weight:700; color:var(--primary);">
            ⚡ Quick Load Business Benchmark Presets:
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button type="button" class="btn btn-outline btn-sm" onclick="loadCmfScenario('solo')">Solo/Micro ($250K)</button>
            <button type="button" class="btn btn-outline btn-sm" onclick="loadCmfScenario('clinic')">Clinic / Home Svc ($850K)</button>
            <button type="button" class="btn btn-outline btn-sm" onclick="loadCmfScenario('agency')">Multi-Crew / Agency ($2.4M)</button>
          </div>
        </div>
      </div>

      <!-- Global Parameters Card -->
      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">1. Core Diagnostic Parameters (C.M.F. Model)</h2>
            <p class="card-desc">Enter your top-line annual revenue and hourly owner rate to baseline friction costs.</p>
          </div>
          <span class="edition-badge free">100% UNLOCKED IN FREE TIER 0</span>
        </div>

        <div class="grid-3">
          <div class="form-group">
            <label class="form-label" for="cmfRevenue">Annual Gross Revenue ($)</label>
            <input type="number" id="cmfRevenue" class="form-input" value="350000" step="5000" oninput="calculateCmf()" />
          </div>
          <div class="form-group">
            <label class="form-label" for="cmfOwnerRate">Owner Hourly Economic Value ($/hr)</label>
            <input type="number" id="cmfOwnerRate" class="form-input" value="125" step="5" oninput="calculateCmf()" />
          </div>
          <div class="form-group">
            <label class="form-label" for="cmfTeamSize">Full-Time Operational Team Size</label>
            <input type="number" id="cmfTeamSize" class="form-input" value="4" step="1" oninput="calculateCmf()" />
          </div>
        </div>
      </div>

      <!-- Friction Table Card (Full CRUD) -->
      <div class="card">
        <div class="card-header">
          <div>
            <h3 class="card-title">Departmental Manual Friction &amp; Cost Registry</h3>
            <p class="card-desc">Click any number or title to Edit Inline. Add custom entries to model your exact business.</p>
          </div>
        </div>

        <div class="crud-toolbar">
          <div class="crud-actions-left">
            <button type="button" class="btn btn-accent btn-sm" onclick="openAddCmfRowModal()">
              + Add Custom Row / Item / Prompt
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="editInline('cmf', 0)">
              Edit Inline
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="resetCmfDefaults()">
              Reset to Studio Defaults
            </button>
          </div>
          <div class="crud-actions-right">
            <button type="button" class="btn btn-outline btn-sm" onclick="exportCmfCsv()">
              📥 Export Audit CSV
            </button>
          </div>
        </div>

        <div class="table-wrap">
          <table id="cmfTable">
            <thead>
              <tr>
                <th>Department / Function</th>
                <th>Manual Friction Description</th>
                <th style="text-align:center;">Weekly Hours</th>
                <th style="text-align:right;">Blended Rate ($/hr)</th>
                <th style="text-align:right;">Annual Cost ($)</th>
                <th style="text-align:center;">Actions</th>
              </tr>
            </thead>
            <tbody id="cmfTableBody">
              <!-- Dynamically rendered via JS -->
            </tbody>
          </table>
        </div>

        <!-- Calculated Summary Statistics -->
        <div class="grid-4" style="margin-top:20px;">
          <div class="stat-card">
            <div class="stat-label">Total Weekly Friction</div>
            <div class="stat-value" id="cmfTotalHours">0 hrs</div>
            <div class="stat-sub">Across all departments</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Annual Operational Leak</div>
            <div class="stat-value accent" id="cmfTotalCost">$0</div>
            <div class="stat-sub" id="cmfLeakPercent">0% of gross revenue</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Recoverable Hours</div>
            <div class="stat-value" id="cmfRecoverableHours">0 hrs/wk</div>
            <div class="stat-sub">Target 65% automation yield</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Net Projected Savings</div>
            <div class="stat-value accent" id="cmfNetSavings">$0/yr</div>
            <div class="stat-sub">Conservative post-tool margin</div>
          </div>
        </div>
      </div>

      <!-- Persistent Personal Notes & Action Log -->
      <div class="module-notes-box">
        <div class="module-notes-header">
          <div class="module-notes-title">📝 Personal Notes &amp; Action Log (Auto-Saved)</div>
          <span class="notes-status" id="notesStatus-1">Saved locally</span>
        </div>
        <textarea id="notes-module-1" class="module-notes-textarea" placeholder="Record your key takeaways from the CMF audit, specific department owners to involve, and automation priorities here... Auto-saves instantaneously to browser localStorage." oninput="saveModuleNotes(1)"></textarea>
      </div>

    </section>

    <!-- ================================================================= -->
    <!-- MODULE 2: SPEED-TO-LEAD SIMULATOR (DEPT 01)                       -->
    <!-- ================================================================= -->
    <section id="module-2" class="module-section">
      
      <!-- Live Dynamic Thirst Banner -->
      <div id="thirstBanner-2" class="thirst-teaser-banner">
        <!-- Rendered dynamically from Module 1 inputs -->
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">2. Inbound Lead Latency &amp; Speed-to-Lead Simulator</h2>
            <p class="card-desc">Simulate how sub-60-second response workflows rescue dropped leads across channels.</p>
          </div>
          <span id="stlTierBadge" class="edition-badge tier2">TIER 2 &amp; PRO ENGINE</span>
        </div>

        <div class="crud-toolbar">
          <div class="crud-actions-left">
            <button type="button" class="btn btn-accent btn-sm" onclick="openAddStlChannelModal()">
              + Add Custom Row / Item / Prompt
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="editInline('stl', 0)">
              Edit Inline
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="resetStlDefaults()">
              Reset to Studio Defaults
            </button>
          </div>
          <div class="crud-actions-right">
            <button type="button" class="btn btn-outline btn-sm" onclick="exportStlCsv()">
              📥 Export Channel CSV
            </button>
          </div>
        </div>

        <!-- Channel Table with Glassmorphism blur on rows 3+ when in Tier 0 -->
        <div class="table-wrap glass-blurred-wrapper glassmorphism">
          <table>
            <thead>
              <tr>
                <th>Lead Generation Channel</th>
                <th style="text-align:center;">Monthly Leads</th>
                <th style="text-align:center;">Current Latency</th>
                <th style="text-align:center;">Current Conv %</th>
                <th style="text-align:center;">Sub-60s Conv %</th>
                <th style="text-align:right;">Avg Deal Value</th>
                <th style="text-align:right;">Annual Recovery ($)</th>
                <th style="text-align:center;">Actions</th>
              </tr>
            </thead>
            <tbody id="stlTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>

          <div id="stlLockOverlay" class="glass-lock-overlay" style="display:none;">
            <h4>🔒 Advanced Multi-Channel Simulation Locked</h4>
            <p>You are viewing the Free Tier 0 preview (first 2 channels unlocked). Activate Tier 2 or Tier 3 Flagship OS to unlock unlimited channels, custom decay curves, and webhook routing triggers.</p>
            <button type="button" class="btn btn-accent btn-sm" onclick="openUnlockModal('tier2')">
              Unlock Full OS ($29 / $59)
            </button>
          </div>
        </div>

        <div class="grid-3" style="margin-top:20px;">
          <div class="stat-card">
            <div class="stat-label">Total Monthly Leads</div>
            <div class="stat-value" id="stlTotalLeads">0</div>
            <div class="stat-sub">Across all tracked channels</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Total Annual Lost Revenue</div>
            <div class="stat-value" style="color:var(--danger);" id="stlLostRevenue">$0</div>
            <div class="stat-sub">Due to response latency &gt; 15 min</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Net Sub-60s Revenue Recovery</div>
            <div class="stat-value accent" id="stlRecoveredRevenue">$0</div>
            <div class="stat-sub">Projected annual top-line lift</div>
          </div>
        </div>
      </div>

      <!-- Persistent Personal Notes & Action Log -->
      <div class="module-notes-box">
        <div class="module-notes-header">
          <div class="module-notes-title">📝 Personal Notes &amp; Action Log (Auto-Saved)</div>
          <span class="notes-status" id="notesStatus-2">Saved locally</span>
        </div>
        <textarea id="notes-module-2" class="module-notes-textarea" placeholder="Document your primary lead intake channels, webhook triggers, and SMS concierge response rules here..." oninput="saveModuleNotes(2)"></textarea>
      </div>

    </section>

    <!-- ================================================================= -->
    <!-- MODULE 3: 50-PROMPT VAULT & VARIABLE CUSTOMIZER                   -->
    <!-- ================================================================= -->
    <section id="module-3" class="module-section">
      
      <!-- Live Dynamic Thirst Banner -->
      <div id="thirstBanner-3" class="thirst-teaser-banner">
        <!-- Rendered dynamically -->
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">3. 50 Production AI Workflow Prompts (Chapters 1–10)</h2>
            <p class="card-desc">Battle-tested system prompts with variable injection, guardrails, and inline customization.</p>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <button type="button" class="btn btn-accent btn-sm" onclick="openAddPromptModal()">
              + Add Custom Row / Item / Prompt
            </button>
            <span id="promptTierBadge" class="edition-badge tier2">TIER 2: ALL 50 PROMPTS</span>
          </div>
        </div>

        <!-- Filter & Search Toolbar -->
        <div style="display:flex; gap:12px; margin-bottom:18px; flex-wrap:wrap;">
          <input type="text" id="promptSearchInput" class="form-input" style="flex:1; min-width:240px;" placeholder="Search prompts by keyword, department, or chapter..." oninput="filterPromptList()" />
          <select id="promptDeptFilter" class="form-select" style="width:240px;" onchange="filterPromptList()">
            <option value="ALL">All Departments (10 Chapters)</option>
            <option value="Dept 01">Dept 01: Lead Intake &amp; Routing</option>
            <option value="Dept 02">Dept 02: Sales &amp; Quoting</option>
            <option value="Dept 03">Dept 03: Fulfillment &amp; Support</option>
            <option value="Dept 04">Dept 04: Invoicing &amp; Cashflow</option>
            <option value="Dept 05">Dept 05: Executive &amp; Governance</option>
          </select>
        </div>

        <div class="item-browser-grid">
          <!-- Prompt Left Sidebar List -->
          <div class="item-list" id="promptListContainer">
            <!-- Rendered dynamically -->
          </div>

          <!-- Prompt Right Preview Pane -->
          <div class="item-preview-pane">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap;">
              <div>
                <span id="activePromptTag" class="item-tag">Chapter 1</span>
                <h3 id="activePromptTitle" style="font-size:16px; font-weight:700; color:var(--primary); margin-top:6px;">Prompt 1.1</h3>
                <p id="activePromptDesc" style="font-size:12px; color:var(--muted); margin-top:4px;">Description</p>
              </div>
              <div style="display:flex; gap:8px;">
                <button type="button" class="btn btn-outline btn-sm" onclick="editPromptTemplateModal()">
                  ✏️ Edit Inline
                </button>
                <button type="button" class="btn btn-accent btn-sm" onclick="copyCurrentPrompt()">
                  📋 Copy Prompt
                </button>
                <button type="button" class="btn btn-outline btn-sm" onclick="downloadCurrentPromptTxt()">
                  💾 .txt
                </button>
              </div>
            </div>

            <!-- Dynamic Variables Input Form -->
            <div id="promptVariablesContainer" style="background:#F8FAFC; border:1px solid var(--border); border-radius:8px; padding:14px;">
              <!-- Variables rendered here -->
            </div>

            <!-- Compiled Output Box -->
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:12px; font-weight:700; color:var(--primary);">Compiled Output with Injected Variables:</span>
                <button type="button" class="btn btn-outline btn-sm" style="padding:2px 8px; font-size:11px;" onclick="resetPromptVariables()">
                  Reset Variables
                </button>
              </div>
              <pre id="promptCompiledOutput" class="prompt-box" contenteditable="true">Select a prompt to view compiled output.</pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Persistent Personal Notes & Action Log -->
      <div class="module-notes-box">
        <div class="module-notes-header">
          <div class="module-notes-title">📝 Personal Notes &amp; Action Log (Auto-Saved)</div>
          <span class="notes-status" id="notesStatus-3">Saved locally</span>
        </div>
        <textarea id="notes-module-3" class="module-notes-textarea" placeholder="Keep track of your top-performing prompt variations, dynamic variables for your team, and testing notes here..." oninput="saveModuleNotes(3)"></textarea>
      </div>

    </section>

    <!-- ================================================================= -->
    <!-- MODULE 4: 12 EMERGENCY BUSINESS OPERATIONS SCRIPTS                -->
    <!-- ================================================================= -->
    <section id="module-4" class="module-section">
      
      <!-- Live Dynamic Thirst Banner -->
      <div id="thirstBanner-4" class="thirst-teaser-banner">
        <!-- Rendered dynamically -->
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">4. 12 Emergency Business Operations Scripts</h2>
            <p class="card-desc">Pre-approved disaster-prevention scripts with dual-channel Email &amp; SMS execution templates.</p>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <button type="button" class="btn btn-accent btn-sm" onclick="openAddScriptModal()">
              + Add Custom Row / Item / Prompt
            </button>
            <span id="scriptTierBadge" class="edition-badge pro">TIER 3: ALL 12 SCRIPTS</span>
          </div>
        </div>

        <div class="item-browser-grid">
          <!-- Script Sidebar List -->
          <div class="item-list" id="scriptListContainer">
            <!-- Rendered dynamically -->
          </div>

          <!-- Script Preview Pane -->
          <div class="item-preview-pane">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap;">
              <div>
                <span id="activeScriptTag" class="item-tag">Emergency 01</span>
                <h3 id="activeScriptTitle" style="font-size:16px; font-weight:700; color:var(--primary); margin-top:6px;">Script 01</h3>
                <p id="activeScriptDesc" style="font-size:12px; color:var(--muted); margin-top:4px;">Trigger description</p>
              </div>
              <div style="display:flex; gap:8px;">
                <button type="button" class="btn btn-outline btn-sm" onclick="editScriptBodyModal()">
                  ✏️ Edit Inline
                </button>
                <button type="button" class="btn btn-accent btn-sm" onclick="copyCurrentScript('email')">
                  📋 Copy Email
                </button>
                <button type="button" class="btn btn-secondary btn-sm" onclick="copyCurrentScript('sms')">
                  📱 Copy SMS
                </button>
              </div>
            </div>

            <!-- Variables form -->
            <div id="scriptVariablesContainer" style="background:#F8FAFC; border:1px solid var(--border); border-radius:8px; padding:14px;">
              <!-- Variables rendered here -->
            </div>

            <!-- Email output -->
            <div>
              <div style="font-size:12px; font-weight:700; color:var(--primary); margin-bottom:6px;">Email Notification Template:</div>
              <pre id="scriptEmailOutput" class="prompt-box" contenteditable="true" style="max-height:220px;">Select a script.</pre>
            </div>

            <!-- SMS output -->
            <div>
              <div style="font-size:12px; font-weight:700; color:var(--primary); margin-bottom:6px;">Instant SMS Concierge Template:</div>
              <pre id="scriptSmsOutput" class="prompt-box" contenteditable="true" style="max-height:120px;">Select a script.</pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Persistent Personal Notes & Action Log -->
      <div class="module-notes-box">
        <div class="module-notes-header">
          <div class="module-notes-title">📝 Personal Notes &amp; Action Log (Auto-Saved)</div>
          <span class="notes-status" id="notesStatus-4">Saved locally</span>
        </div>
        <textarea id="notes-module-4" class="module-notes-textarea" placeholder="List your key emergency contacts, escalation phone numbers, and company-specific fallback SOPs here..." oninput="saveModuleNotes(4)"></textarea>
      </div>

    </section>

    <!-- ================================================================= -->
    <!-- MODULE 5: T.R.A.V. GOVERNANCE & 90-DAY ROLLOUT TRACKER            -->
    <!-- ================================================================= -->
    <section id="module-5" class="module-section">
      
      <!-- Live Dynamic Thirst Banner -->
      <div id="thirstBanner-5" class="thirst-teaser-banner">
        <!-- Rendered dynamically -->
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">5. T.R.A.V. Risk Governance Matrix &amp; 90-Day Rollout</h2>
            <p class="card-desc">Evaluate automation safety across Transparency, Reliability, Auditability, and Velocity.</p>
          </div>
          <span id="travTierBadge" class="edition-badge pro">TIER 3 FLAGSHIP OS</span>
        </div>

        <div class="crud-toolbar">
          <div class="crud-actions-left">
            <button type="button" class="btn btn-accent btn-sm" onclick="openAddWorkflowModal()">
              + Add Custom Row / Item / Prompt
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="openAddTaskModal()">
              + Add Custom 90-Day Task
            </button>
          </div>
          <div class="crud-actions-right">
            <button type="button" class="btn btn-outline btn-sm" onclick="exportTravJson()">
              📥 Export Roadmap JSON
            </button>
          </div>
        </div>

        <!-- Workflow Risk Matrix Table with Glassmorphism Blur on lower rows in Tier 0 -->
        <div class="table-wrap glass-blurred-wrapper glassmorphism">
          <table>
            <thead>
              <tr>
                <th>Workflow Name</th>
                <th style="text-align:center;">Department</th>
                <th style="text-align:center;">Autonomy Tier</th>
                <th style="text-align:center;">Risk Score</th>
                <th style="text-align:center;">Amber Gate Required</th>
                <th style="text-align:center;">Actions</th>
              </tr>
            </thead>
            <tbody id="travTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>

          <div id="travLockOverlay" class="glass-lock-overlay" style="display:none;">
            <h4>🔒 Full 90-Day Rollout Matrix Locked</h4>
            <p>Based on your Module 1 diagnostic numbers, our engine calculated custom risk thresholds for your business. Activate Tier 3 Flagship OS to unlock the full 90-day interactive implementation tracker and amber approval gates.</p>
            <button type="button" class="btn btn-accent btn-sm" onclick="openUnlockModal('tier3')">
              Unlock Full OS ($29 / $59)
            </button>
          </div>
        </div>

        <!-- 90-Day Implementation Checklist -->
        <div style="margin-top:24px;">
          <h3 style="font-size:15px; font-weight:700; color:var(--primary); margin-bottom:12px;">
            90-Day Milestone Execution Tracker (Auto-Saved)
          </h3>
          <div id="roadmapMilestonesContainer" style="display:flex; flex-direction:column; gap:10px;">
            <!-- Rendered via JS -->
          </div>
        </div>
      </div>

      <!-- Persistent Personal Notes & Action Log -->
      <div class="module-notes-box">
        <div class="module-notes-header">
          <div class="module-notes-title">📝 Personal Notes &amp; Action Log (Auto-Saved)</div>
          <span class="notes-status" id="notesStatus-5">Saved locally</span>
        </div>
        <textarea id="notes-module-5" class="module-notes-textarea" placeholder="Document your company's Amber Approval channel, designated human supervisors, and rollout sprint deadlines here..." oninput="saveModuleNotes(5)"></textarea>
      </div>

    </section>

    <!-- ================================================================= -->
    <!-- MODULE 6: FRIDAY OWNER KPI SCORECARD                              -->
    <!-- ================================================================= -->
    <section id="module-6" class="module-section">
      
      <!-- Live Dynamic Thirst Banner -->
      <div id="thirstBanner-6" class="thirst-teaser-banner">
        <!-- Rendered dynamically -->
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">6. Friday 3:00 PM Owner KPI Executive Scorecard</h2>
            <p class="card-desc">15-minute weekly executive health dashboard to track automation yield and prevent silent leaks.</p>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <button type="button" class="btn btn-accent btn-sm" onclick="openAddKpiModal()">
              + Add Custom Row / Item / Prompt
            </button>
            <span id="kpiTierBadge" class="edition-badge pro">TIER 3 FLAGSHIP OS</span>
          </div>
        </div>

        <div class="crud-toolbar">
          <div class="crud-actions-left">
            <button type="button" class="btn btn-outline btn-sm" onclick="editInline('kpi', 0)">
              Edit Inline
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="resetKpiDefaults()">
              Reset to Studio Defaults
            </button>
          </div>
          <div class="crud-actions-right">
            <button type="button" class="btn btn-outline btn-sm" onclick="exportKpiCsv()">
              📥 Export Scorecard CSV
            </button>
            <button type="button" class="btn btn-accent btn-sm" onclick="saveFridaySnapshot()">
              💾 Save Weekly Snapshot
            </button>
          </div>
        </div>

        <!-- KPI Table with Glassmorphism Blur on lower rows in Tier 0 -->
        <div class="table-wrap glass-blurred-wrapper glassmorphism">
          <table>
            <thead>
              <tr>
                <th>KPI Metric Name</th>
                <th style="text-align:center;">Department</th>
                <th style="text-align:center;">Target Benchmark</th>
                <th style="text-align:center;">This Week Actual</th>
                <th style="text-align:center;">Health Status</th>
                <th style="text-align:center;">Actions</th>
              </tr>
            </thead>
            <tbody id="kpiTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>

          <div id="kpiLockOverlay" class="glass-lock-overlay" style="display:none;">
            <h4>🔒 Executive Scorecard Multi-Week History Locked</h4>
            <p>Free Tier 0 includes the first 2 health metrics. Activate Tier 3 Flagship OS to unlock all 12 department metrics, automated weekly variance calculation, and Amber risk digests.</p>
            <button type="button" class="btn btn-accent btn-sm" onclick="openUnlockModal('tier3')">
              Unlock Full OS ($29 / $59)
            </button>
          </div>
        </div>

        <div class="grid-3" style="margin-top:20px;">
          <div class="stat-card">
            <div class="stat-label">Executive Health Index</div>
            <div class="stat-value accent" id="kpiHealthScore">92%</div>
            <div class="stat-sub">Based on current week entries</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Active Amber Alerts</div>
            <div class="stat-value" style="color:var(--warning);" id="kpiAmberAlerts">0</div>
            <div class="stat-sub">Metrics requiring review</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Saved Historical Snapshots</div>
            <div class="stat-value" id="kpiSnapshotCount">0</div>
            <div class="stat-sub">Stored in browser vault</div>
          </div>
        </div>
      </div>

      <!-- Persistent Personal Notes & Action Log -->
      <div class="module-notes-box">
        <div class="module-notes-header">
          <div class="module-notes-title">📝 Personal Notes &amp; Action Log (Auto-Saved)</div>
          <span class="notes-status" id="notesStatus-6">Saved locally</span>
        </div>
        <textarea id="notes-module-6" class="module-notes-textarea" placeholder="List your high-priority decisions for Monday, staff performance highlights, and operational adjustments here..." oninput="saveModuleNotes(6)"></textarea>
      </div>

    </section>

  </main>

  <!-- =================================================================== -->
  <!-- MODAL: LICENSE KEY ACTIVATION & TIER UPGRADE                       -->
  <!-- =================================================================== -->
  <div id="activationModal" class="modal-backdrop">
    <div class="modal-box">
      <h3 class="modal-title">Activate Commercial Edition License</h3>
      <p class="modal-desc">
        Enter your official commercial license key below, or upgrade to Tier 2 ($29) or Tier 3 Flagship ($59) to receive instant access.
      </p>

      <div class="form-group">
        <label class="form-label" for="licenseKeyInput">Commercial License Key</label>
        <input type="text" id="licenseKeyInput" class="form-input" placeholder="e.g. STUDIO-TIER2-2026 or STUDIO-PRO-OS-2026" style="text-transform:uppercase; font-weight:700; font-family:var(--font-mono);" />
        <div id="licenseFeedback" style="font-size:12px; margin-top:6px; color:var(--danger); min-height:18px;"></div>
      </div>

      <div style="background:#F1F5F9; border-radius:8px; padding:14px; margin-bottom:14px; font-size:12px; line-height:1.5;">
        <div style="font-weight:700; color:var(--primary); margin-bottom:6px;">Need a License Key?</div>
        <div>• <strong>Tier 2 Workbook Edition ($29):</strong> Includes all 50 AI prompts, 10-chapter checklists, and printable audit generator. Key: <code>STUDIO-TIER2-2026</code></div>
        <div style="margin-top:4px;">• <strong>Tier 3 Flagship OS ($59):</strong> Unlocks all 6 modules, 12 emergency scripts, automation blueprints, and 8-tab Excel center. Keys: <code>SMALLBIZ-OS-PRO-2026</code> or <code>STUDIO-PRO-OS-2026</code></div>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-outline" onclick="closeActivationModal()">Cancel</button>
        <button type="button" class="btn btn-accent" onclick="submitLicenseKey()">Activate License</button>
      </div>
    </div>
  </div>

  <!-- =================================================================== -->
  <!-- MODAL: ADD CUSTOM ITEM (CRUD HANDLER)                              -->
  <!-- =================================================================== -->
  <div id="customItemModal" class="modal-backdrop">
    <div class="modal-box">
      <h3 class="modal-title" id="customItemModalTitle">Add Custom Item</h3>
      <p class="modal-desc" id="customItemModalDesc">Enter custom item details to persist in your workspace.</p>

      <div id="customItemModalBody">
        <!-- Rendered dynamically depending on item type -->
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-outline" onclick="closeCustomItemModal()">Cancel</button>
        <button type="button" class="btn btn-accent" id="customItemModalSaveBtn" onclick="saveCustomItem()">Save Item</button>
      </div>
    </div>
  </div>

  <!-- =================================================================== -->
  <!-- MODAL: WORKSPACE BACKUP & RESTORE (JSON ENGINE)                    -->
  <!-- =================================================================== -->
  <div id="backupModal" class="modal-backdrop">
    <div class="modal-box">
      <h3 class="modal-title">Workspace Backup &amp; Transfer Center</h3>
      <p class="modal-desc">
        Export your complete workspace (custom rows, prompts, checklists, notes, and calculator entries) as a single JSON file, or restore from a previous backup.
      </p>

      <div style="display:flex; flex-direction:column; gap:16px;">
        <div style="border:1px dashed var(--border); border-radius:8px; padding:16px; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:var(--primary); margin-bottom:4px;">Export Current Workspace</div>
          <p style="font-size:12px; color:var(--muted); margin-bottom:12px;">Downloads smallbiz-automation-os-workspace-backup.json.</p>
          <button type="button" class="btn btn-accent btn-sm" onclick="exportWorkspaceJson()">
            💾 Export Full Workspace Backup (JSON)
          </button>
        </div>

        <div style="border:1px dashed var(--border); border-radius:8px; padding:16px; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:var(--primary); margin-bottom:4px;">Restore From Backup File</div>
          <p style="font-size:12px; color:var(--muted); margin-bottom:12px;">Select your previously saved JSON file to restore state.</p>
          <input type="file" id="workspaceRestoreInput" accept=".json" style="display:none;" onchange="handleWorkspaceFileSelect(event)" />
          <button type="button" class="btn btn-outline btn-sm" onclick="document.getElementById('workspaceRestoreInput').click()">
            📂 Upload &amp; Restore JSON File
          </button>
        </div>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-outline" onclick="closeBackupModal()">Close</button>
      </div>
    </div>
  </div>

  <!-- Interactive Toast Notification -->
  <div id="toast" class="toast">Operation completed successfully.</div>

  <!-- Master JavaScript Application Logic -->
  <script>
    // =========================================================================
    // EMBEDDED MASTER DATA: 50 PROMPTS (CH 1-10) & 12 EMERGENCY SCRIPTS
    // =========================================================================
    {data_block}

    // =========================================================================
    // 3-TIER PROGRESSIVE ACCESS & LICENSE ENGINE
    // =========================================================================
    const LICENSE_CODES = {{
      tier2: ["STUDIO-TIER2-2026"],
      tier3: ["SMALLBIZ-OS-PRO-2026", "STUDIO-PRO-OS-2026"]
    }};

    const STORAGE_KEYS = {{
      currentTier: "smallbiz_os_current_tier_v2",
      unlockedTier2: "smallbiz_os_unlocked_tier2_v2",
      unlockedTier3: "smallbiz_os_unlocked_tier3_v2",
      cmfRows: "smallbiz_os_cmf_rows_v2",
      cmfGlobals: "smallbiz_os_cmf_globals_v2",
      stlChannels: "smallbiz_os_stl_channels_v2",
      customPrompts: "smallbiz_os_custom_prompts_v2",
      editedPrompts: "smallbiz_os_edited_prompts_v2",
      customScripts: "smallbiz_os_custom_scripts_v2",
      editedScripts: "smallbiz_os_edited_scripts_v2",
      travWorkflows: "smallbiz_os_trav_workflows_v2",
      roadmapTasks: "smallbiz_os_roadmap_tasks_v2",
      kpiMetrics: "smallbiz_os_kpi_metrics_v2",
      kpiSnapshots: "smallbiz_os_kpi_snapshots_v2"
    }};

    let currentTier = 0; // 0 = Free Diagnostic, 2 = Workbook, 3 = Flagship OS
    let unlockedTier2 = false;
    let unlockedTier3 = false;

    // Toast helper
    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.textContent = msg;
      t.style.display = "block";
      setTimeout(() => {{
        t.style.display = "none";
      }}, 3200);
    }}

    // Switch between Modules 1-6
    function switchModule(modId) {{
      document.querySelectorAll(".module-section").forEach(s => s.classList.remove("active"));
      document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));

      const target = document.getElementById(modId);
      if (target) target.classList.add("active");

      const tabBtn = document.querySelector(`.nav-tab[data-target="${{modId}}"]`);
      if (tabBtn) tabBtn.classList.add("active");

      updateThirstBanners();
    }}

    // Select Tier (0, 2, 3)
    function selectTier(tierNum) {{
      if (tierNum === 2 && !unlockedTier2 && !unlockedTier3) {{
        openActivationModal("tier2");
        return;
      }}
      if (tierNum === 3 && !unlockedTier3) {{
        openActivationModal("tier3");
        return;
      }}
      currentTier = tierNum;
      try {{
        localStorage.setItem(STORAGE_KEYS.currentTier, tierNum.toString());
      }} catch (e) {{}}
      applyTierStateUI();
      showToast(`Active Edition: ${{getTierName(tierNum)}}`);
    }}

    function getTierName(tier) {{
      if (tier === 3) return "Tier 3 / Tier 4: Flagship Pro OS";
      if (tier === 2) return "Tier 2: Workbook & Prompt Vault";
      return "Tier 0: Free Diagnostic & Starter Mode";
    }}

    function applyTierStateUI() {{
      const badge = document.getElementById("editionStatusBadge");
      const btn0 = document.querySelector(".tier-btn.tier-0");
      const btn2 = document.querySelector(".tier-btn.tier-2");
      const btn3 = document.querySelector(".tier-btn.tier-3");

      [btn0, btn2, btn3].forEach(b => b.classList.remove("active"));

      if (currentTier === 3) {{
        btn3.classList.add("active");
        badge.textContent = "🟣 TIER 3: FLAGSHIP PRO OS";
        badge.className = "edition-badge pro";
      }} else if (currentTier === 2) {{
        btn2.classList.add("active");
        badge.textContent = "🔵 TIER 2: WORKBOOK EDITION";
        badge.className = "edition-badge tier2";
      }} else {{
        btn0.classList.add("active");
        badge.textContent = "🟢 TIER 0: FREE DIAGNOSTIC";
        badge.className = "edition-badge free";
      }}

      // Update badges in cards
      const promptBadge = document.getElementById("promptTierBadge");
      if (promptBadge) {{
        promptBadge.textContent = currentTier >= 2 ? "ALL 50 PROMPTS UNLOCKED" : "10 FREE PROMPTS (CH 1-2)";
        promptBadge.className = currentTier >= 2 ? "edition-badge tier2" : "edition-badge free";
      }}

      const scriptBadge = document.getElementById("scriptTierBadge");
      if (scriptBadge) {{
        scriptBadge.textContent = currentTier >= 3 ? "ALL 12 SCRIPTS UNLOCKED" : "2 FREE SCRIPTS (CH 1-2)";
        scriptBadge.className = currentTier >= 3 ? "edition-badge pro" : "edition-badge free";
      }}

      // Apply blur locks
      applyGlassmorphismLocks();
      renderPromptList();
      renderEmergencyScriptList();
      renderRoadmapMilestones();
      updateThirstBanners();
    }}

    function applyGlassmorphismLocks() {{
      const stlLock = document.getElementById("stlLockOverlay");
      const travLock = document.getElementById("travLockOverlay");
      const kpiLock = document.getElementById("kpiLockOverlay");

      const isLockedMod2 = (currentTier === 0);
      const isLockedMod5 = (currentTier === 0);
      const isLockedMod6 = (currentTier < 3);

      if (stlLock) stlLock.style.display = isLockedMod2 ? "block" : "none";
      if (travLock) travLock.style.display = isLockedMod5 ? "block" : "none";
      if (kpiLock) kpiLock.style.display = isLockedMod6 ? "block" : "none";

      // Style table rows in stl, trav, kpi
      styleTableRowsForTier("stlTableBody", isLockedMod2, 2);
      styleTableRowsForTier("travTableBody", isLockedMod5, 2);
      styleTableRowsForTier("kpiTableBody", isLockedMod6, 2);
    }}

    function styleTableRowsForTier(tbodyId, isLocked, visibleRowsCount) {{
      const tbody = document.getElementById(tbodyId);
      if (!tbody) return;
      const rows = tbody.querySelectorAll("tr");
      rows.forEach((row, idx) => {{
        if (isLocked && idx >= visibleRowsCount) {{
          row.style.filter = "blur(4px)";
          row.style.opacity = "0.5";
          row.style.pointerEvents = "none";
          row.style.userSelect = "none";
        }} else {{
          row.style.filter = "none";
          row.style.opacity = "1";
          row.style.pointerEvents = "auto";
          row.style.userSelect = "auto";
        }}
      }});
    }}

    // Activation Modal
    function openActivationModal(hintTier) {{
      const modal = document.getElementById("activationModal");
      const input = document.getElementById("licenseKeyInput");
      const feedback = document.getElementById("licenseFeedback");
      feedback.textContent = "";
      input.value = "";
      modal.classList.add("open");
      input.focus();
    }}

    function closeActivationModal() {{
      document.getElementById("activationModal").classList.remove("open");
    }}

    function openUnlockModal(targetTier) {{
      openActivationModal(targetTier);
    }}

    function submitLicenseKey() {{
      const input = (document.getElementById("licenseKeyInput").value || "").trim().toUpperCase();
      const feedback = document.getElementById("licenseFeedback");

      if (LICENSE_CODES.tier3.includes(input)) {{
        unlockedTier2 = true;
        unlockedTier3 = true;
        currentTier = 3;
        try {{
          localStorage.setItem(STORAGE_KEYS.unlockedTier2, "true");
          localStorage.setItem(STORAGE_KEYS.unlockedTier3, "true");
          localStorage.setItem(STORAGE_KEYS.currentTier, "3");
        }} catch (e) {{}}
        closeActivationModal();
        applyTierStateUI();
        showToast("🎉 Flagship Pro OS Activated: All 6 Modules, 50 Prompts & 12 Scripts Enabled!");
      }} else if (LICENSE_CODES.tier2.includes(input)) {{
        unlockedTier2 = true;
        currentTier = 2;
        try {{
          localStorage.setItem(STORAGE_KEYS.unlockedTier2, "true");
          localStorage.setItem(STORAGE_KEYS.currentTier, "2");
        }} catch (e) {{}}
        closeActivationModal();
        applyTierStateUI();
        showToast("🎉 Tier 2 Workbook Activated: All 50 Prompts & Checklists Enabled!");
      }} else {{
        feedback.textContent = "Invalid license key. Use STUDIO-TIER2-2026 or STUDIO-PRO-OS-2026.";
      }}
    }}

    // =========================================================================
    // DYNAMIC "THIRST & CRAVING" ENGINE
    // =========================================================================
    function getDiagnosticMetrics() {{
      const rev = parseFloat(document.getElementById("cmfRevenue").value) || 350000;
      const ownerRate = parseFloat(document.getElementById("cmfOwnerRate").value) || 125;
      const teamSize = parseFloat(document.getElementById("cmfTeamSize").value) || 4;

      let totalWeeklyHrs = 0;
      let totalAnnualCost = 0;
      let highestCostDept = "Dept 01: Inbound Speed-to-Lead";
      let highestDeptCost = 0;

      cmfRowsData.forEach(r => {{
        totalWeeklyHrs += r.hours;
        const c = r.hours * r.rate * 52;
        totalAnnualCost += c;
        if (c > highestDeptCost) {{
          highestDeptCost = c;
          highestCostDept = r.dept;
        }}
      }});

      const recoverableHours = Math.round(totalWeeklyHrs * 0.65 * 10) / 10;
      const netSavings = Math.round(totalAnnualCost * 0.68);

      return {{
        revenue: rev,
        ownerRate: ownerRate,
        teamSize: teamSize,
        totalWeeklyHrs: totalWeeklyHrs,
        totalAnnualCost: totalAnnualCost,
        highestCostDept: highestCostDept,
        recoverableHours: recoverableHours,
        netSavings: netSavings
      }};
    }}

    function updateThirstBanners() {{
      const m = getDiagnosticMetrics();
      const revFmt = "$" + m.revenue.toLocaleString();
      const costFmt = "$" + Math.round(m.totalAnnualCost).toLocaleString();
      const saveFmt = "$" + Math.round(m.netSavings).toLocaleString();

      for (let i = 2; i <= 6; i++) {{
        const b = document.getElementById("thirstBanner-" + i);
        if (!b) continue;

        if (currentTier === 3) {{
          b.style.display = "none";
          continue;
        }}

        b.style.display = "flex";
        let moduleContext = "";
        if (i === 2) {{
          moduleContext = `⚡ Diagnostic Alert: Based on the numbers you just entered in Module 1, our engine calculated an estimated ${{costFmt}} annual leak across your business (highest bottleneck: ${{m.highestCostDept}}). The first 2 channels below are calibrated to your live numbers. Activate Tier 2 ($29) or Tier 3 Flagship OS ($59) to unlock and edit your full results immediately.`;
        }} else if (i === 3) {{
          moduleContext = `⚡ Diagnostic Alert: Based on the numbers you just entered in Module 1, our engine calculated ${{m.recoverableHours}} recoverable hours weekly. Prompts 1.1–2.5 are unlocked below to address ${{m.highestCostDept}}. Activate Tier 2 ($29) or Tier 3 Flagship OS ($59) to unlock and edit your full results immediately.`;
        }} else if (i === 4) {{
          moduleContext = `⚡ Diagnostic Alert: Based on the numbers you just entered in Module 1, our engine calibrated Emergency Scripts 01 & 02 for immediate frontline triage. Activate Tier 2 ($29) or Tier 3 Flagship OS ($59) to unlock and edit your full results immediately.`;
        }} else if (i === 5) {{
          moduleContext = `⚡ Diagnostic Alert: Based on the numbers you just entered in Module 1, our engine calculated your custom 90-Day Execution Roadmap + 4 Automation Triggers for your ${{m.teamSize}}-person team below. Activate Tier 2 ($29) or Tier 3 Flagship OS ($59) to unlock and edit your full results immediately.`;
        }} else if (i === 6) {{
          moduleContext = `⚡ Diagnostic Alert: Based on the numbers you just entered in Module 1, our engine calculated ${{costFmt}}/yr in potential silent leaks. Metrics 1 & 2 are live below. Activate Tier 2 ($29) or Tier 3 Flagship OS ($59) to unlock and edit your full results immediately.`;
        }}

        b.innerHTML = `
          <div class="thirst-header">
            <span class="thirst-badge">⚡ DYNAMIC DIAGNOSTIC ALERT (CALIBRATED TO YOUR NUMBERS)</span>
            <span style="font-size:12px; color:#94A3B8;">Revenue: ${{revFmt}} · Leak: ${{costFmt}}/yr</span>
          </div>
          <div class="thirst-body">
            ${{moduleContext}}
          </div>
          <div class="thirst-actions">
            <button type="button" class="btn btn-accent btn-sm" onclick="openUnlockModal('tier2')">
              Unlock Full OS ($29 / $59)
            </button>
          </div>
        `;
      }}
    }}

    // Helper for Edit Inline
    function editInline(type, idx) {{
      if (type === 'cmf') {{
        editCmfField(idx, 'desc');
      }} else if (type === 'stl') {{
        editStlField(idx, 'currentConv');
      }} else if (type === 'kpi') {{
        editKpiField(idx, 'actual');
      }}
    }}

    // =========================================================================
    // MODULE 1: CMF FRICTION CALCULATOR (FULL CRUD)
    // =========================================================================
    const DEFAULT_CMF_ROWS = [
      {{ dept: "Dept 01: Lead Intake", desc: "Manual web form copy-paste & delayed SMS notifications", hours: 8.5, rate: 35 }},
      {{ dept: "Dept 02: Quoting & Sales", desc: "Manual PDF estimate formatting & unstandardized proposals", hours: 9.0, rate: 65 }},
      {{ dept: "Dept 03: Fulfillment", desc: "Repetitive client onboarding email threads & manual file links", hours: 6.5, rate: 35 }},
      {{ dept: "Dept 03: Customer Support", desc: "Copy-pasting answers to identical tier-1 FAQ tickets", hours: 11.0, rate: 28 }},
      {{ dept: "Dept 04: Invoicing & AR", desc: "Manual invoice creation and weekly overdue reminder chasing", hours: 5.5, rate: 45 }},
      {{ dept: "Dept 05: Owner Operations", desc: "Compiling manual spreadsheet updates for Friday status review", hours: 6.0, rate: 125 }}
    ];

    let cmfRowsData = [];

    function initCmfData() {{
      try {{
        const saved = localStorage.getItem(STORAGE_KEYS.cmfRows);
        cmfRowsData = saved ? JSON.parse(saved) : JSON.parse(JSON.stringify(DEFAULT_CMF_ROWS));
        const globals = localStorage.getItem(STORAGE_KEYS.cmfGlobals);
        if (globals) {{
          const g = JSON.parse(globals);
          if (g.revenue) document.getElementById("cmfRevenue").value = g.revenue;
          if (g.ownerRate) document.getElementById("cmfOwnerRate").value = g.ownerRate;
          if (g.teamSize) document.getElementById("cmfTeamSize").value = g.teamSize;
        }}
      }} catch (e) {{
        cmfRowsData = JSON.parse(JSON.stringify(DEFAULT_CMF_ROWS));
      }}
      renderCmfTable();
      calculateCmf();
    }}

    function renderCmfTable() {{
      const tbody = document.getElementById("cmfTableBody");
      tbody.innerHTML = "";

      cmfRowsData.forEach((row, idx) => {{
        const cost = Math.round(row.hours * row.rate * 52);
        const isCustom = row.isCustom ? `<span class="badge-custom">CUSTOM</span>` : "";

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${{row.dept}}</strong>${{isCustom}}</td>
          <td class="cell-editable" title="Click to edit" onclick="editCmfField(${{idx}}, 'desc')">${{row.desc}}</td>
          <td style="text-align:center;" class="cell-editable" title="Click to edit" onclick="editCmfField(${{idx}}, 'hours')">${{row.hours}} hrs</td>
          <td style="text-align:right;" class="cell-editable" title="Click to edit" onclick="editCmfField(${{idx}}, 'rate')">$${{row.rate}}</td>
          <td style="text-align:right; font-weight:700; color:var(--primary);">$${{cost.toLocaleString()}}</td>
          <td style="text-align:center;">
            <button type="button" class="row-delete-btn" title="Delete Row" onclick="deleteCmfRow(${{idx}})">✕</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function calculateCmf() {{
      const rev = parseFloat(document.getElementById("cmfRevenue").value) || 1;
      const ownerRate = parseFloat(document.getElementById("cmfOwnerRate").value) || 100;
      const teamSize = parseFloat(document.getElementById("cmfTeamSize").value) || 1;

      // Save globals
      try {{
        localStorage.setItem(STORAGE_KEYS.cmfGlobals, JSON.stringify({{ revenue: rev, ownerRate: ownerRate, teamSize: teamSize }}));
      }} catch (e) {{}}

      let totHrs = 0;
      let totCost = 0;

      cmfRowsData.forEach(r => {{
        totHrs += r.hours;
        totCost += r.hours * r.rate * 52;
      }});

      const recoverable = Math.round(totHrs * 0.65 * 10) / 10;
      const netSavings = Math.round(totCost * 0.68);
      const pct = Math.round((totCost / rev) * 1000) / 10;

      document.getElementById("cmfTotalHours").textContent = `${{totHrs.toFixed(1)}} hrs`;
      document.getElementById("cmfTotalCost").textContent = `$${{Math.round(totCost).toLocaleString()}}`;
      document.getElementById("cmfLeakPercent").textContent = `${{pct}}% of gross revenue`;
      document.getElementById("cmfRecoverableHours").textContent = `${{recoverable.toFixed(1)}} hrs/wk`;
      document.getElementById("cmfNetSavings").textContent = `$${{netSavings.toLocaleString()}}/yr`;

      updateThirstBanners();
    }}

    function editCmfField(idx, field) {{
      const current = cmfRowsData[idx][field];
      const promptText = field === 'desc' ? 'Edit Friction Description:' : `Edit ${{field}} ($/hr or hrs):`;
      const newVal = prompt(promptText, current);
      if (newVal !== null && newVal.trim() !== "") {{
        if (field === 'hours' || field === 'rate') {{
          const num = parseFloat(newVal);
          if (!isNaN(num) && num >= 0) {{
            cmfRowsData[idx][field] = num;
          }}
        }} else {{
          cmfRowsData[idx][field] = newVal.trim();
        }}
        saveCmfState();
      }}
    }}

    function deleteCmfRow(idx) {{
      if (cmfRowsData.length <= 1) {{
        showToast("At least 1 friction row required.");
        return;
      }}
      cmfRowsData.splice(idx, 1);
      saveCmfState();
      showToast("Friction area deleted.");
    }}

    function resetCmfDefaults() {{
      cmfRowsData = JSON.parse(JSON.stringify(DEFAULT_CMF_ROWS));
      saveCmfState();
      showToast("Reset to Studio Defaults.");
    }}

    function saveCmfState() {{
      try {{
        localStorage.setItem(STORAGE_KEYS.cmfRows, JSON.stringify(cmfRowsData));
      }} catch (e) {{}}
      renderCmfTable();
      calculateCmf();
    }}

    function loadCmfScenario(type) {{
      if (type === 'solo') {{
        document.getElementById("cmfRevenue").value = "250000";
        document.getElementById("cmfOwnerRate").value = "100";
        document.getElementById("cmfTeamSize").value = "1";
      }} else if (type === 'clinic') {{
        document.getElementById("cmfRevenue").value = "850000";
        document.getElementById("cmfOwnerRate").value = "175";
        document.getElementById("cmfTeamSize").value = "5";
      }} else if (type === 'agency') {{
        document.getElementById("cmfRevenue").value = "2400000";
        document.getElementById("cmfOwnerRate").value = "250";
        document.getElementById("cmfTeamSize").value = "14";
      }}
      calculateCmf();
      showToast(`Loaded ${{type.toUpperCase()}} Benchmark Scenario.`);
    }}

    function exportCmfCsv() {{
      let csv = "Department,Friction Description,Weekly Hours,Hourly Rate,Annual Cost\\n";
      cmfRowsData.forEach(r => {{
        const c = Math.round(r.hours * r.rate * 52);
        csv += `"${{r.dept}}","${{r.desc}}",${{r.hours}},${{r.rate}},${{c}}\\n`;
      }});
      downloadFile(csv, "cmf-friction-and-roi-audit.csv", "text/csv");
    }}

    // =========================================================================
    // MODULE 2: SPEED TO LEAD SIMULATOR (FULL CRUD)
    // =========================================================================
    const DEFAULT_STL_CHANNELS = [
      {{ channel: "Website Quote Form", monthlyLeads: 45, currentSpeed: "42 min", currentConv: 14, targetConv: 34, dealValue: 1800 }},
      {{ channel: "Google Local Service Ads", monthlyLeads: 30, currentSpeed: "18 min", currentConv: 18, targetConv: 38, dealValue: 2400 }},
      {{ channel: "After-Hours Voicemail", monthlyLeads: 25, currentSpeed: "14 hrs", currentConv: 6, targetConv: 22, dealValue: 1500 }},
      {{ channel: "Instagram & Facebook DM", monthlyLeads: 35, currentSpeed: "3.5 hrs", currentConv: 8, targetConv: 26, dealValue: 1200 }}
    ];

    let stlChannelsData = [];

    function initStlData() {{
      try {{
        const saved = localStorage.getItem(STORAGE_KEYS.stlChannels);
        stlChannelsData = saved ? JSON.parse(saved) : JSON.parse(JSON.stringify(DEFAULT_STL_CHANNELS));
      }} catch (e) {{
        stlChannelsData = JSON.parse(JSON.stringify(DEFAULT_STL_CHANNELS));
      }}
      renderStlTable();
    }}

    function renderStlTable() {{
      const tbody = document.getElementById("stlTableBody");
      tbody.innerHTML = "";

      let totLeads = 0;
      let totLost = 0;
      let totRecovered = 0;

      stlChannelsData.forEach((ch, idx) => {{
        totLeads += ch.monthlyLeads;
        const currentCloses = ch.monthlyLeads * (ch.currentConv / 100);
        const sub60Closes = ch.monthlyLeads * (ch.targetConv / 100);
        const monthlyLift = (sub60Closes - currentCloses) * ch.dealValue;
        const annualRecovery = Math.round(monthlyLift * 12);
        const annualLost = Math.round((sub60Closes - currentCloses) * ch.dealValue * 12 * 1.25);

        totLost += annualLost;
        totRecovered += annualRecovery;

        const isCustom = ch.isCustom ? `<span class="badge-custom">CUSTOM</span>` : "";

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${{ch.channel}}</strong>${{isCustom}}</td>
          <td style="text-align:center;" class="cell-editable" onclick="editStlField(${{idx}}, 'monthlyLeads')">${{ch.monthlyLeads}}</td>
          <td style="text-align:center;">${{ch.currentSpeed}}</td>
          <td style="text-align:center;" class="cell-editable" onclick="editStlField(${{idx}}, 'currentConv')">${{ch.currentConv}}%</td>
          <td style="text-align:center;" class="cell-editable" onclick="editStlField(${{idx}}, 'targetConv')">${{ch.targetConv}}%</td>
          <td style="text-align:right;" class="cell-editable" onclick="editStlField(${{idx}}, 'dealValue')">$${{ch.dealValue.toLocaleString()}}</td>
          <td style="text-align:right; font-weight:700; color:var(--accent);">$${{annualRecovery.toLocaleString()}}</td>
          <td style="text-align:center;">
            <button type="button" class="row-delete-btn" title="Delete Channel" onclick="deleteStlChannel(${{idx}})">✕</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById("stlTotalLeads").textContent = totLeads.toString();
      document.getElementById("stlLostRevenue").textContent = `$${{totLost.toLocaleString()}}`;
      document.getElementById("stlRecoveredRevenue").textContent = `$${{totRecovered.toLocaleString()}}`;

      applyGlassmorphismLocks();
    }}

    function editStlField(idx, field) {{
      const current = stlChannelsData[idx][field];
      const newVal = prompt(`Edit ${{field}}:`, current);
      if (newVal !== null && newVal.trim() !== "") {{
        const num = parseFloat(newVal);
        if (!isNaN(num) && num >= 0) {{
          stlChannelsData[idx][field] = num;
          saveStlState();
        }}
      }}
    }}

    function deleteStlChannel(idx) {{
      if (stlChannelsData.length <= 1) {{
        showToast("At least 1 channel required.");
        return;
      }}
      stlChannelsData.splice(idx, 1);
      saveStlState();
      showToast("Channel deleted.");
    }}

    function resetStlDefaults() {{
      stlChannelsData = JSON.parse(JSON.stringify(DEFAULT_STL_CHANNELS));
      saveStlState();
      showToast("Reset to Studio Defaults.");
    }}

    function saveStlState() {{
      try {{
        localStorage.setItem(STORAGE_KEYS.stlChannels, JSON.stringify(stlChannelsData));
      }} catch (e) {{}}
      renderStlTable();
    }}

    function exportStlCsv() {{
      let csv = "Channel,Monthly Leads,Current Latency,Current Conv %,Sub-60s Conv %,Avg Deal Value,Annual Recovery\\n";
      stlChannelsData.forEach(ch => {{
        const cCloses = ch.monthlyLeads * (ch.currentConv / 100);
        const sCloses = ch.monthlyLeads * (ch.targetConv / 100);
        const rec = Math.round((sCloses - cCloses) * ch.dealValue * 12);
        csv += `"${{ch.channel}}",${{ch.monthlyLeads}},"${{ch.currentSpeed}}",${{ch.currentConv}},${{ch.targetConv}},${{ch.dealValue}},${{rec}}\\n`;
      }});
      downloadFile(csv, "speed-to-lead-simulation.csv", "text/csv");
    }}

    // =========================================================================
    // MODULE 3: 50-PROMPT VAULT & LIVE BUILDER (FULL CRUD)
    // =========================================================================
    let activePromptId = "Prompt 1.1";
    let activePromptVarValues = {{}};
    let customPromptsData = [];
    let editedPromptTemplates = {{}};

    function initPromptData() {{
      try {{
        const savedCustom = localStorage.getItem(STORAGE_KEYS.customPrompts);
        if (savedCustom) customPromptsData = JSON.parse(savedCustom);
        const savedEdited = localStorage.getItem(STORAGE_KEYS.editedPrompts);
        if (savedEdited) editedPromptTemplates = JSON.parse(savedEdited);
      }} catch (e) {{}}
      renderPromptList();
      selectPrompt("Prompt 1.1");
    }}

    function getAllPrompts() {{
      return [...PROMPTS_DATA, ...customPromptsData];
    }}

    function renderPromptList() {{
      const container = document.getElementById("promptListContainer");
      if (!container) return;
      container.innerHTML = "";

      const query = (document.getElementById("promptSearchInput") ? document.getElementById("promptSearchInput").value : "").toLowerCase();
      const dept = document.getElementById("promptDeptFilter") ? document.getElementById("promptDeptFilter").value : "ALL";

      const all = getAllPrompts();

      all.forEach((p, idx) => {{
        // Filter checks
        const matchesQuery = p.id.toLowerCase().includes(query) || p.title.toLowerCase().includes(query) || (p.category && p.category.toLowerCase().includes(query));
        const matchesDept = (dept === "ALL") || (p.category && p.category.includes(dept));
        if (!matchesQuery || !matchesDept) return;

        // Check tier lock: Tier 0 unlocks first 10 prompts (Ch 1 & 2)
        const isLockedInTier0 = (currentTier === 0 && idx >= 10 && !p.isCustom);

        const entry = document.createElement("div");
        entry.className = `item-list-entry ${{p.id === activePromptId ? "active" : ""}} ${{isLockedInTier0 ? "locked" : ""}}`;
        entry.onclick = () => {{
          if (isLockedInTier0) {{
            openActivationModal("tier2");
          }} else {{
            selectPrompt(p.id);
          }}
        }};

        const lockBadge = isLockedInTier0 ? `<span class="item-lock-pill">🔒 TIER 2</span>` : "";
        const customBadge = p.isCustom ? `<span class="badge-custom">CUSTOM</span>` : "";

        entry.innerHTML = `
          <div class="item-tag-row">
            <span class="item-tag">${{p.chapter_title || p.category || "Prompt"}}</span>
            ${{lockBadge}}${{customBadge}}
          </div>
          <div class="item-title">${{p.id}}: ${{p.title}}</div>
        `;
        container.appendChild(entry);
      }});
    }}

    function selectPrompt(promptId) {{
      activePromptId = promptId;
      const all = getAllPrompts();
      const p = all.find(x => x.id === promptId) || all[0];
      if (!p) return;

      document.querySelectorAll("#promptListContainer .item-list-entry").forEach(e => e.classList.remove("active"));
      // highlight active
      const entries = document.querySelectorAll("#promptListContainer .item-list-entry");
      entries.forEach(e => {{
        if (e.textContent.includes(p.id)) e.classList.add("active");
      }});

      document.getElementById("activePromptTag").textContent = p.chapter_title || p.category || "Prompt";
      document.getElementById("activePromptTitle").textContent = `${{p.id}}: ${{p.title}}`;
      document.getElementById("activePromptDesc").textContent = p.description || p.category || "";

      renderPromptVariablesForm(p);
      updateCompiledPromptOutput(p);
    }}

    function renderPromptVariablesForm(p) {{
      const container = document.getElementById("promptVariablesContainer");
      container.innerHTML = "";

      const vars = p.variables || [];
      if (vars.length === 0) {{
        container.innerHTML = `<div style="font-size:12px; color:var(--muted);">Zero dynamic variables required for this prompt. Ready for immediate deployment.</div>`;
        return;
      }}

      const heading = document.createElement("div");
      heading.style.fontSize = "12px";
      heading.style.fontWeight = "700";
      heading.style.color = "var(--primary)";
      heading.style.marginBottom = "8px";
      heading.textContent = "Customize Variable Values for Your Business:";
      container.appendChild(heading);

      const grid = document.createElement("div");
      grid.style.display = "grid";
      grid.style.gridTemplateColumns = "1fr 1fr";
      grid.style.gap = "10px";

      vars.forEach(v => {{
        const group = document.createElement("div");
        group.className = "form-group";
        group.style.marginBottom = "0";

        const label = document.createElement("label");
        label.className = "form-label";
        label.textContent = v;

        const input = document.createElement("input");
        input.type = "text";
        input.className = "form-input";
        input.value = activePromptVarValues[v] || "";
        input.placeholder = `Enter ${{v}}...`;
        input.oninput = (e) => {{
          activePromptVarValues[v] = e.target.value;
          updateCompiledPromptOutput(p);
        }};

        group.appendChild(label);
        group.appendChild(input);
        grid.appendChild(group);
      }});

      container.appendChild(grid);
    }}

    function updateCompiledPromptOutput(p) {{
      const box = document.getElementById("promptCompiledOutput");
      if (!p) return;

      let template = editedPromptTemplates[p.id] || p.prompt_text || p.user_prompt || "";
      const sys = p.system_prompt ? `=== SYSTEM PROMPT / GUARDRAILS ===\\n${{p.system_prompt}}\\n\\n=== EXECUTION PROMPT ===\\n` : "";

      let compiled = template;
      const vars = p.variables || [];
      vars.forEach(v => {{
        const val = activePromptVarValues[v] || `[${{v}}]`;
        compiled = compiled.split(`[${{v}}]`).join(val);
        compiled = compiled.split(`{{${{v}}}}`).join(val);
      }});

      box.textContent = sys + compiled;
    }}

    function filterPromptList() {{
      renderPromptList();
    }}

    function resetPromptVariables() {{
      activePromptVarValues = {{}};
      const all = getAllPrompts();
      const p = all.find(x => x.id === activePromptId);
      if (p) {{
        renderPromptVariablesForm(p);
        updateCompiledPromptOutput(p);
        showToast("Variables reset.");
      }}
    }}

    function copyCurrentPrompt() {{
      const text = document.getElementById("promptCompiledOutput").textContent;
      copyToClipboard(text, "Prompt copied to clipboard!");
    }}

    function downloadCurrentPromptTxt() {{
      const text = document.getElementById("promptCompiledOutput").textContent;
      downloadFile(text, `${{activePromptId.replace(/\s+/g, '_')}}.txt`, "text/plain");
    }}

    function editPromptTemplateModal() {{
      const all = getAllPrompts();
      const p = all.find(x => x.id === activePromptId);
      if (!p) return;
      const current = editedPromptTemplates[p.id] || p.prompt_text || p.user_prompt || "";
      const newVal = prompt("Edit Prompt Template (use [VARIABLE] format):", current);
      if (newVal !== null && newVal.trim() !== "") {{
        editedPromptTemplates[p.id] = newVal.trim();
        try {{
          localStorage.setItem(STORAGE_KEYS.editedPrompts, JSON.stringify(editedPromptTemplates));
        }} catch (e) {{}}
        updateCompiledPromptOutput(p);
        showToast("Template updated locally.");
      }}
    }}

    // =========================================================================
    // MODULE 4: 12 EMERGENCY SCRIPTS (FULL CRUD)
    // =========================================================================
    let activeEmergencyId = "Emergency Script 01";
    let activeEmergencyVarValues = {{}};
    let customScriptsData = [];
    let editedScriptTemplates = {{}};

    function initEmergencyData() {{
      try {{
        const savedCustom = localStorage.getItem(STORAGE_KEYS.customScripts);
        if (savedCustom) customScriptsData = JSON.parse(savedCustom);
        const savedEdited = localStorage.getItem(STORAGE_KEYS.editedScripts);
        if (savedEdited) editedScriptTemplates = JSON.parse(savedEdited);
      }} catch (e) {{}}
      renderEmergencyScriptList();
      selectEmergencyScript("Emergency Script 01");
    }}

    function getAllEmergencyScripts() {{
      return [...EMERGENCY_SCRIPTS_DATA, ...customScriptsData];
    }}

    function renderEmergencyScriptList() {{
      const container = document.getElementById("scriptListContainer");
      if (!container) return;
      container.innerHTML = "";

      const all = getAllEmergencyScripts();

      all.forEach((s, idx) => {{
        // Tier check: Tier 0 and Tier 2 unlock first 2 scripts; Tier 3 unlocks all 12
        const isLocked = (currentTier < 3 && idx >= 2 && !s.isCustom);

        const entry = document.createElement("div");
        entry.className = `item-list-entry ${{s.id === activeEmergencyId ? "active" : ""}} ${{isLocked ? "locked" : ""}}`;
        entry.onclick = () => {{
          if (isLocked) {{
            openActivationModal("tier3");
          }} else {{
            selectEmergencyScript(s.id);
          }}
        }};

        const lockBadge = isLocked ? `<span class="item-lock-pill">🔒 TIER 3</span>` : "";
        const customBadge = s.isCustom ? `<span class="badge-custom">CUSTOM</span>` : "";

        entry.innerHTML = `
          <div class="item-tag-row">
            <span class="item-tag">${{s.trigger_category || "Emergency"}}</span>
            ${{lockBadge}}${{customBadge}}
          </div>
          <div class="item-title">${{s.id}}: ${{s.title}}</div>
        `;
        container.appendChild(entry);
      }});
    }}

    function selectEmergencyScript(scriptId) {{
      activeEmergencyId = scriptId;
      const all = getAllEmergencyScripts();
      const s = all.find(x => x.id === scriptId) || all[0];
      if (!s) return;

      document.querySelectorAll("#scriptListContainer .item-list-entry").forEach(e => e.classList.remove("active"));
      const entries = document.querySelectorAll("#scriptListContainer .item-list-entry");
      entries.forEach(e => {{
        if (e.textContent.includes(s.id)) e.classList.add("active");
      }});

      document.getElementById("activeScriptTag").textContent = s.trigger_category || "Emergency";
      document.getElementById("activeScriptTitle").textContent = `${{s.id}}: ${{s.title}}`;
      document.getElementById("activeScriptDesc").textContent = s.trigger_event || s.description || "";

      renderEmergencyVariablesForm(s);
      updateCompiledScriptOutputs(s);
    }}

    function renderEmergencyVariablesForm(s) {{
      const container = document.getElementById("scriptVariablesContainer");
      container.innerHTML = "";

      const vars = s.dynamic_variables || s.variables || [];
      if (vars.length === 0) {{
        container.innerHTML = `<div style="font-size:12px; color:var(--muted);">Zero dynamic variables required. Ready for immediate deployment.</div>`;
        return;
      }}

      const heading = document.createElement("div");
      heading.style.fontSize = "12px";
      heading.style.fontWeight = "700";
      heading.style.color = "var(--primary)";
      heading.style.marginBottom = "8px";
      heading.textContent = "Customize Emergency Variables:";
      container.appendChild(heading);

      const grid = document.createElement("div");
      grid.style.display = "grid";
      grid.style.gridTemplateColumns = "1fr 1fr";
      grid.style.gap = "10px";

      vars.forEach(v => {{
        const group = document.createElement("div");
        group.className = "form-group";
        group.style.marginBottom = "0";

        const label = document.createElement("label");
        label.className = "form-label";
        label.textContent = v;

        const input = document.createElement("input");
        input.type = "text";
        input.className = "form-input";
        input.value = activeEmergencyVarValues[v] || "";
        input.placeholder = `Enter ${{v}}...`;
        input.oninput = (e) => {{
          activeEmergencyVarValues[v] = e.target.value;
          updateCompiledScriptOutputs(s);
        }};

        group.appendChild(label);
        group.appendChild(input);
        grid.appendChild(group);
      }});

      container.appendChild(grid);
    }}

    function updateCompiledScriptOutputs(s) {{
      if (!s) return;
      const emailBox = document.getElementById("scriptEmailOutput");
      const smsBox = document.getElementById("scriptSmsOutput");

      let emailText = (editedScriptTemplates[s.id] && editedScriptTemplates[s.id].email) || s.email_template || s.email_body || "";
      let smsText = (editedScriptTemplates[s.id] && editedScriptTemplates[s.id].sms) || s.sms_template || s.sms_body || "";

      const vars = s.dynamic_variables || s.variables || [];
      vars.forEach(v => {{
        const val = activeEmergencyVarValues[v] || `[${{v}}]`;
        emailText = emailText.split(`[${{v}}]`).join(val);
        emailText = emailText.split(`{{${{v}}}}`).join(val);
        smsText = smsText.split(`[${{v}}]`).join(val);
        smsText = smsText.split(`{{${{v}}}}`).join(val);
      }});

      emailBox.textContent = emailText;
      smsBox.textContent = smsText;
    }}

    function copyCurrentScript(channel) {{
      const text = channel === 'email' ? document.getElementById("scriptEmailOutput").textContent : document.getElementById("scriptSmsOutput").textContent;
      copyToClipboard(text, `${{channel.toUpperCase()}} script copied!`);
    }}

    function editScriptBodyModal() {{
      const all = getAllEmergencyScripts();
      const s = all.find(x => x.id === activeEmergencyId);
      if (!s) return;
      const curEmail = (editedScriptTemplates[s.id] && editedScriptTemplates[s.id].email) || s.email_template || "";
      const newEmail = prompt("Edit Email Template:", curEmail);
      if (newEmail !== null && newEmail.trim() !== "") {{
        if (!editedScriptTemplates[s.id]) editedScriptTemplates[s.id] = {{}};
        editedScriptTemplates[s.id].email = newEmail.trim();
        try {{
          localStorage.setItem(STORAGE_KEYS.editedScripts, JSON.stringify(editedScriptTemplates));
        }} catch (e) {{}}
        updateCompiledScriptOutputs(s);
        showToast("Email template updated.");
      }}
    }}

    // =========================================================================
    // MODULE 5: T.R.A.V. & 90-DAY ROADMAP (FULL CRUD)
    // =========================================================================
    const DEFAULT_TRAV_WORKFLOWS = [
      {{ name: "60s Inbound Webhook Lead Router", dept: "Dept 01", tier: "Tier 1: Green", risk: 14, amber: "No" }},
      {{ name: "Missed Call Auto-SMS Concierge", dept: "Dept 01", tier: "Tier 1: Green", risk: 18, amber: "No" }},
      {{ name: "3-Option Instant Quote Generator", dept: "Dept 02", tier: "Tier 2: Amber", risk: 54, amber: "Yes (Owner Review)" }},
      {{ name: "AI Support Ticket Classification", dept: "Dept 03", tier: "Tier 1: Green", risk: 22, amber: "No" }},
      {{ name: "Overdue Invoice 5-Stage Chaser", dept: "Dept 04", tier: "Tier 2: Amber", risk: 48, amber: "Yes (Finance Review)" }}
    ];

    const DEFAULT_ROADMAP_MILESTONES = [
      {{ id: "m1", phase: "Phase I (Days 1–30): Quick Wins & Revenue Rescue", title: "Complete 5-Department Bottleneck Audit & C.M.F. Benchmarking (Ch 1)" }},
      {{ id: "m2", phase: "Phase I (Days 1–30): Quick Wins & Revenue Rescue", title: "Deploy T.R.A.V. Pre-AI Guardrails & Slack Amber Approval Channel (Ch 2)" }},
      {{ id: "m3", phase: "Phase I (Days 1–30): Quick Wins & Revenue Rescue", title: "Launch 60-Second Speed-to-Lead & Missed-Call SMS Concierge (Ch 3)" }},
      {{ id: "m4", phase: "Phase I (Days 1–30): Quick Wins & Revenue Rescue", title: "Activate Same-Day Invoice Trigger & 5-Stage Polite Payment Chaser (Ch 8)" }},
      {{ id: "m5", phase: "Phase II (Days 31–60): Core Quoting & Fulfillment", title: "Configure 3-Tier Quote Engine & 14-Day Nurture Follow-up (Ch 4)" }},
      {{ id: "m6", phase: "Phase II (Days 31–60): Core Quoting & Fulfillment", title: "Deploy Client Onboarding Pipeline & Automated Asset Intake (Ch 5)" }},
      {{ id: "m7", phase: "Phase II (Days 31–60): Core Quoting & Fulfillment", title: "Install AI Support Triage & Repetitive FAQ Deflection Gate (Ch 6)" }},
      {{ id: "m8", phase: "Phase III (Days 61–90): Retention, Delegation & Command", title: "Launch 90-Day Win-Back Engine & 5-Star Review Trigger (Ch 7)" }},
      {{ id: "m9", phase: "Phase III (Days 61–90): Retention, Delegation & Command", title: "Sync Team Notion SOP Vault & Weekly Accountability Registry (Ch 9)" }},
      {{ id: "m10", phase: "Phase III (Days 61–90): Retention, Delegation & Command", title: "Run 1st Automated Friday 3:00 PM Owner KPI Executive Review (Ch 10)" }}
    ];

    let travWorkflowsData = [];
    let roadmapTasksData = [];
    let roadmapCheckedState = {{}};

    function initTravData() {{
      try {{
        const savedW = localStorage.getItem(STORAGE_KEYS.travWorkflows);
        travWorkflowsData = savedW ? JSON.parse(savedW) : JSON.parse(JSON.stringify(DEFAULT_TRAV_WORKFLOWS));
        const savedT = localStorage.getItem(STORAGE_KEYS.roadmapTasks);
        roadmapTasksData = savedT ? JSON.parse(savedT) : JSON.parse(JSON.stringify(DEFAULT_ROADMAP_MILESTONES));
        const savedChecks = localStorage.getItem("smallbiz_os_roadmap_checks");
        if (savedChecks) roadmapCheckedState = JSON.parse(savedChecks);
      }} catch (e) {{
        travWorkflowsData = JSON.parse(JSON.stringify(DEFAULT_TRAV_WORKFLOWS));
        roadmapTasksData = JSON.parse(JSON.stringify(DEFAULT_ROADMAP_MILESTONES));
      }}
      renderTravTable();
      renderRoadmapMilestones();
    }}

    function renderTravTable() {{
      const tbody = document.getElementById("travTableBody");
      tbody.innerHTML = "";

      travWorkflowsData.forEach((w, idx) => {{
        const isCustom = w.isCustom ? `<span class="badge-custom">CUSTOM</span>` : "";
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${{w.name}}</strong>${{isCustom}}</td>
          <td style="text-align:center;">${{w.dept}}</td>
          <td style="text-align:center;"><span class="item-tag">${{w.tier}}</span></td>
          <td style="text-align:center; font-weight:700;">${{w.risk}}/100</td>
          <td style="text-align:center;">${{w.amber}}</td>
          <td style="text-align:center;">
            <button type="button" class="row-delete-btn" title="Delete Workflow" onclick="deleteTravWorkflow(${{idx}})">✕</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      applyGlassmorphismLocks();
    }}

    function renderRoadmapMilestones() {{
      const container = document.getElementById("roadmapMilestonesContainer");
      if (!container) return;
      container.innerHTML = "";

      roadmapTasksData.forEach((m, idx) => {{
        // Tier 0 unlocks Phase 1 (first 4 tasks); Phase 2 & 3 locked
        const isLockedInTier0 = (currentTier === 0 && idx >= 4);

        const row = document.createElement("div");
        row.style.display = "flex";
        row.style.alignItems = "center";
        row.style.justifyContent = "space-between";
        row.style.padding = "10px 14px";
        row.style.background = "#FFFFFF";
        row.style.border = "1px solid var(--border)";
        row.style.borderRadius = "8px";

        if (isLockedInTier0) {{
          row.style.filter = "blur(3px)";
          row.style.opacity = "0.5";
          row.style.pointerEvents = "none";
        }}

        const left = document.createElement("div");
        left.style.display = "flex";
        left.style.alignItems = "center";
        left.style.gap = "12px";

        const chk = document.createElement("input");
        chk.type = "checkbox";
        chk.checked = !!roadmapCheckedState[m.id];
        chk.onchange = (e) => {{
          roadmapCheckedState[m.id] = e.target.checked;
          try {{
            localStorage.setItem("smallbiz_os_roadmap_checks", JSON.stringify(roadmapCheckedState));
          }} catch (err) {{}}
          showToast(e.target.checked ? "Milestone checked!" : "Milestone updated.");
        }};

        const titleSpan = document.createElement("span");
        titleSpan.style.fontSize = "13px";
        titleSpan.style.fontWeight = "600";
        titleSpan.textContent = m.title;

        left.appendChild(chk);
        left.appendChild(titleSpan);

        const phaseBadge = document.createElement("span");
        phaseBadge.className = "item-tag";
        phaseBadge.textContent = m.phase.split(":")[0];

        row.appendChild(left);
        row.appendChild(phaseBadge);
        container.appendChild(row);
      }});
    }}

    function deleteTravWorkflow(idx) {{
      if (travWorkflowsData.length <= 1) {{
        showToast("At least 1 workflow required.");
        return;
      }}
      travWorkflowsData.splice(idx, 1);
      try {{
        localStorage.setItem(STORAGE_KEYS.travWorkflows, JSON.stringify(travWorkflowsData));
      }} catch (e) {{}}
      renderTravTable();
      showToast("Workflow deleted.");
    }}

    function exportTravJson() {{
      const exportObj = {{
        workflows: travWorkflowsData,
        milestones: roadmapTasksData,
        completed: roadmapCheckedState,
        exportedAt: new Date().toISOString()
      }};
      downloadFile(JSON.stringify(exportObj, null, 2), "governance-and-90day-roadmap.json", "application/json");
    }}

    // =========================================================================
    // MODULE 6: FRIDAY OWNER KPI SCORECARD (FULL CRUD)
    // =========================================================================
    const DEFAULT_KPIS = [
      {{ name: "Sub-60s Lead Response Rate", dept: "Dept 01", target: "90%", actual: "94%", amber: "<80%" }},
      {{ name: "Average Response Latency (Sec)", dept: "Dept 01", target: "<45s", actual: "38s", amber: ">90s" }},
      {{ name: "First-Contact Resolution Rate", dept: "Dept 03", target: "75%", actual: "82%", amber: "<65%" }},
      {{ name: "Support Ticket Deflection %", dept: "Dept 03", target: "50%", actual: "58%", amber: "<40%" }},
      {{ name: "Days Sales Outstanding (DSO)", dept: "Dept 04", target: "<22 days", actual: "18 days", amber: ">30 days" }},
      {{ name: "Overdue Invoices (>14 Days)", dept: "Dept 04", target: "0", actual: "1", amber: ">2" }}
    ];

    let kpiMetricsData = [];
    let kpiSnapshotsData = [];

    function initKpiData() {{
      try {{
        const savedK = localStorage.getItem(STORAGE_KEYS.kpiMetrics);
        kpiMetricsData = savedK ? JSON.parse(savedK) : JSON.parse(JSON.stringify(DEFAULT_KPIS));
        const savedS = localStorage.getItem(STORAGE_KEYS.kpiSnapshots);
        if (savedS) kpiSnapshotsData = JSON.parse(savedS);
      }} catch (e) {{
        kpiMetricsData = JSON.parse(JSON.stringify(DEFAULT_KPIS));
      }}
      renderKpiTable();
      updateKpiStats();
    }}

    function renderKpiTable() {{
      const tbody = document.getElementById("kpiTableBody");
      tbody.innerHTML = "";

      kpiMetricsData.forEach((k, idx) => {{
        const isCustom = k.isCustom ? `<span class="badge-custom">CUSTOM</span>` : "";
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${{k.name}}</strong>${{isCustom}}</td>
          <td style="text-align:center;">${{k.dept}}</td>
          <td style="text-align:center;" class="cell-editable" onclick="editKpiField(${{idx}}, 'target')">${{k.target}}</td>
          <td style="text-align:center; font-weight:700;" class="cell-editable" onclick="editKpiField(${{idx}}, 'actual')">${{k.actual}}</td>
          <td style="text-align:center;"><span class="item-tag" style="background:#D1FAE5; color:#065F46;">NORMAL</span></td>
          <td style="text-align:center;">
            <button type="button" class="row-delete-btn" title="Delete KPI" onclick="deleteKpi(${{idx}})">✕</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      applyGlassmorphismLocks();
    }}

    function editKpiField(idx, field) {{
      const current = kpiMetricsData[idx][field];
      const newVal = prompt(`Edit ${{field}}:`, current);
      if (newVal !== null && newVal.trim() !== "") {{
        kpiMetricsData[idx][field] = newVal.trim();
        saveKpiState();
      }}
    }}

    function deleteKpi(idx) {{
      if (kpiMetricsData.length <= 1) {{
        showToast("At least 1 KPI required.");
        return;
      }}
      kpiMetricsData.splice(idx, 1);
      saveKpiState();
      showToast("KPI deleted.");
    }}

    function resetKpiDefaults() {{
      kpiMetricsData = JSON.parse(JSON.stringify(DEFAULT_KPIS));
      saveKpiState();
      showToast("Reset to Studio Defaults.");
    }}

    function saveKpiState() {{
      try {{
        localStorage.setItem(STORAGE_KEYS.kpiMetrics, JSON.stringify(kpiMetricsData));
      }} catch (e) {{}}
      renderKpiTable();
      updateKpiStats();
    }}

    function updateKpiStats() {{
      document.getElementById("kpiSnapshotCount").textContent = kpiSnapshotsData.length.toString();
    }}

    function saveFridaySnapshot() {{
      const snap = {{
        timestamp: new Date().toISOString(),
        dateFormatted: new Date().toLocaleDateString(),
        metrics: JSON.parse(JSON.stringify(kpiMetricsData))
      }};
      kpiSnapshotsData.unshift(snap);
      if (kpiSnapshotsData.length > 52) kpiSnapshotsData.pop(); // keep 52 weeks
      try {{
        localStorage.setItem(STORAGE_KEYS.kpiSnapshots, JSON.stringify(kpiSnapshotsData));
      }} catch (e) {{}}
      updateKpiStats();
      showToast("Weekly Friday Snapshot saved to local vault!");
    }}

    function exportKpiCsv() {{
      let csv = "KPI Metric,Department,Target,Actual,Amber Threshold\\n";
      kpiMetricsData.forEach(k => {{
        csv += `"${{k.name}}","${{k.dept}}","${{k.target}}","${{k.actual}}","${{k.amber}}"\\n`;
      }});
      downloadFile(csv, "friday-owner-kpi-scorecard.csv", "text/csv");
    }}

    // =========================================================================
    // MODULE NOTES & ACTION LOG PERSISTENCE (MODULES 1-6)
    // =========================================================================
    function initModuleNotes() {{
      for (let i = 1; i <= 6; i++) {{
        const key = `smallbiz_notes_m${{i}}`;
        const val = localStorage.getItem(key) || "";
        const el = document.getElementById(`notes-module-${{i}}`);
        if (el) el.value = val;
      }}
    }}

    function saveModuleNotes(moduleNum) {{
      const el = document.getElementById(`notes-module-${{moduleNum}}`);
      const statusEl = document.getElementById(`notesStatus-${{moduleNum}}`);
      if (!el) return;
      const key = `smallbiz_notes_m${{moduleNum}}`;
      try {{
        localStorage.setItem(key, el.value);
        if (statusEl) {{
          statusEl.textContent = "Saved " + new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
        }}
      }} catch (e) {{}}
    }}

    // =========================================================================
    // MODAL DIALOGS: ADD CUSTOM ITEMS & BACKUP / RESTORE
    // =========================================================================
    let currentCustomItemType = "";

    function openAddCmfRowModal() {{
      currentCustomItemType = "cmf";
      document.getElementById("customItemModalTitle").textContent = "Add Custom Friction Area";
      document.getElementById("customItemModalDesc").textContent = "Add a custom bottleneck specific to your business workflow.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">Department / Function</label>
          <input type="text" id="custCmfDept" class="form-input" placeholder="e.g. Dept 03: Inventory & Warehouse" />
        </div>
        <div class="form-group">
          <label class="form-label">Friction Description</label>
          <input type="text" id="custCmfDesc" class="form-input" placeholder="e.g. Manual re-ordering and stock check emails" />
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Weekly Hours</label>
            <input type="number" id="custCmfHours" class="form-input" value="5" step="0.5" />
          </div>
          <div class="form-group">
            <label class="form-label">Hourly Rate ($/hr)</label>
            <input type="number" id="custCmfRate" class="form-input" value="35" step="5" />
          </div>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function openAddStlChannelModal() {{
      currentCustomItemType = "stl";
      document.getElementById("customItemModalTitle").textContent = "Add Inbound Lead Channel";
      document.getElementById("customItemModalDesc").textContent = "Track response time and revenue recovery for a new marketing channel.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">Channel Name</label>
          <input type="text" id="custStlName" class="form-input" placeholder="e.g. LinkedIn Inbound DMs" />
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Monthly Inquiries</label>
            <input type="number" id="custStlLeads" class="form-input" value="20" />
          </div>
          <div class="form-group">
            <label class="form-label">Average Deal Value ($)</label>
            <input type="number" id="custStlDeal" class="form-input" value="1500" />
          </div>
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Current Conv %</label>
            <input type="number" id="custStlCurConv" class="form-input" value="10" />
          </div>
          <div class="form-group">
            <label class="form-label">Target Sub-60s Conv %</label>
            <input type="number" id="custStlTgtConv" class="form-input" value="25" />
          </div>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function openAddPromptModal() {{
      currentCustomItemType = "prompt";
      document.getElementById("customItemModalTitle").textContent = "Add Custom AI Prompt";
      document.getElementById("customItemModalDesc").textContent = "Create and store your company-specific AI prompt with custom variables.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">Prompt Title</label>
          <input type="text" id="custPromptTitle" class="form-input" placeholder="e.g. VIP Client Onboarding Concierge" />
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Department / Category</label>
            <input type="text" id="custPromptCategory" class="form-input" placeholder="e.g. Dept 03: Fulfillment" />
          </div>
          <div class="form-group">
            <label class="form-label">Variables (comma separated)</label>
            <input type="text" id="custPromptVars" class="form-input" placeholder="e.g. CLIENT_NAME, SERVICE_TIER" />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Prompt Body / Template</label>
          <textarea id="custPromptBody" class="form-input" style="height:90px;" placeholder="Write prompt with [VARIABLE] placeholders..."></textarea>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function openAddScriptModal() {{
      currentCustomItemType = "script";
      document.getElementById("customItemModalTitle").textContent = "Add Custom Emergency Script";
      document.getElementById("customItemModalDesc").textContent = "Add a company incident communication template.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">Script Title</label>
          <input type="text" id="custScriptTitle" class="form-input" placeholder="e.g. Payment Gateway Failure Alert" />
        </div>
        <div class="form-group">
          <label class="form-label">Trigger Category</label>
          <input type="text" id="custScriptCat" class="form-input" placeholder="e.g. Dept 04: Finance &amp; Payments" />
        </div>
        <div class="form-group">
          <label class="form-label">Email Template</label>
          <textarea id="custScriptEmail" class="form-input" style="height:80px;" placeholder="Email message body..."></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">SMS Concierge Template</label>
          <textarea id="custScriptSms" class="form-input" style="height:60px;" placeholder="Brief SMS message..."></textarea>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function openAddWorkflowModal() {{
      currentCustomItemType = "workflow";
      document.getElementById("customItemModalTitle").textContent = "Add Custom Workflow to Matrix";
      document.getElementById("customItemModalDesc").textContent = "Register a workflow into the T.R.A.V. Governance Matrix.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">Workflow Name</label>
          <input type="text" id="custWfName" class="form-input" placeholder="e.g. Automated Review Request Trigger" />
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Department</label>
            <input type="text" id="custWfDept" class="form-input" placeholder="e.g. Dept 03" />
          </div>
          <div class="form-group">
            <label class="form-label">Autonomy Tier</label>
            <select id="custWfTier" class="form-select">
              <option value="Tier 1: Green">Tier 1: Green (Autonomous)</option>
              <option value="Tier 2: Amber">Tier 2: Amber (Human-in-Loop)</option>
              <option value="Tier 3: Red">Tier 3: Red (Owner Only)</option>
            </select>
          </div>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function openAddTaskModal() {{
      currentCustomItemType = "task";
      document.getElementById("customItemModalTitle").textContent = "Add Custom 90-Day Task";
      document.getElementById("customItemModalDesc").textContent = "Add a milestone task to your implementation roadmap.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">Task Description</label>
          <input type="text" id="custTaskTitle" class="form-input" placeholder="e.g. Review Twilio SMS logs with Operations Lead" />
        </div>
        <div class="form-group">
          <label class="form-label">Sprint Phase</label>
          <select id="custTaskPhase" class="form-select">
            <option value="Phase I (Days 1–30): Quick Wins">Phase I (Days 1–30)</option>
            <option value="Phase II (Days 31–60): Quoting">Phase II (Days 31–60)</option>
            <option value="Phase III (Days 61–90): Scale">Phase III (Days 61–90)</option>
          </select>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function openAddKpiModal() {{
      currentCustomItemType = "kpi";
      document.getElementById("customItemModalTitle").textContent = "Add Custom KPI Metric";
      document.getElementById("customItemModalDesc").textContent = "Add a custom performance indicator to the Friday Owner Scorecard.";
      document.getElementById("customItemModalBody").innerHTML = `
        <div class="form-group">
          <label class="form-label">KPI Name</label>
          <input type="text" id="custKpiName" class="form-input" placeholder="e.g. Weekly Proposal Close Rate" />
        </div>
        <div class="grid-3">
          <div class="form-group">
            <label class="form-label">Department</label>
            <input type="text" id="custKpiDept" class="form-input" placeholder="e.g. Dept 02" />
          </div>
          <div class="form-group">
            <label class="form-label">Target Benchmark</label>
            <input type="text" id="custKpiTarget" class="form-input" placeholder="e.g. >40%" />
          </div>
          <div class="form-group">
            <label class="form-label">Current Actual</label>
            <input type="text" id="custKpiActual" class="form-input" placeholder="e.g. 44%" />
          </div>
        </div>
      `;
      document.getElementById("customItemModal").classList.add("open");
    }}

    function closeCustomItemModal() {{
      document.getElementById("customItemModal").classList.remove("open");
    }}

    function saveCustomItem() {{
      if (currentCustomItemType === "cmf") {{
        const dept = (document.getElementById("custCmfDept").value || "Custom Dept").trim();
        const desc = (document.getElementById("custCmfDesc").value || "Custom Friction").trim();
        const hrs = parseFloat(document.getElementById("custCmfHours").value) || 2;
        const rate = parseFloat(document.getElementById("custCmfRate").value) || 50;
        cmfRowsData.push({{ dept: dept, desc: desc, hours: hrs, rate: rate, isCustom: true }});
        saveCmfState();
        showToast("Custom friction area added.");
      }} else if (currentCustomItemType === "stl") {{
        const name = (document.getElementById("custStlName").value || "Custom Channel").trim();
        const leads = parseFloat(document.getElementById("custStlLeads").value) || 10;
        const deal = parseFloat(document.getElementById("custStlDeal").value) || 1000;
        const curConv = parseFloat(document.getElementById("custStlCurConv").value) || 10;
        const tgtConv = parseFloat(document.getElementById("custStlTgtConv").value) || 25;
        stlChannelsData.push({{ channel: name, monthlyLeads: leads, currentSpeed: "Custom", currentConv: curConv, targetConv: tgtConv, dealValue: deal, isCustom: true }});
        saveStlState();
        showToast("Custom lead channel added.");
      }} else if (currentCustomItemType === "prompt") {{
        const title = (document.getElementById("custPromptTitle").value || "Custom Prompt").trim();
        const cat = (document.getElementById("custPromptCategory").value || "General").trim();
        const rawVars = (document.getElementById("custPromptVars").value || "").split(",").map(v => v.trim()).filter(Boolean);
        const body = (document.getElementById("custPromptBody").value || "").trim();
        const id = `Custom ${{customPromptsData.length + 1}}`;
        customPromptsData.push({{ id: id, title: title, category: cat, variables: rawVars, prompt_text: body, isCustom: true }});
        try {{
          localStorage.setItem(STORAGE_KEYS.customPrompts, JSON.stringify(customPromptsData));
        }} catch (e) {{}}
        renderPromptList();
        selectPrompt(id);
        showToast("Custom AI Prompt created!");
      }} else if (currentCustomItemType === "script") {{
        const title = (document.getElementById("custScriptTitle").value || "Custom Script").trim();
        const cat = (document.getElementById("custScriptCat").value || "General").trim();
        const email = (document.getElementById("custScriptEmail").value || "").trim();
        const sms = (document.getElementById("custScriptSms").value || "").trim();
        const id = `Custom Script ${{customScriptsData.length + 1}}`;
        customScriptsData.push({{ id: id, title: title, trigger_category: cat, email_template: email, sms_template: sms, isCustom: true }});
        try {{
          localStorage.setItem(STORAGE_KEYS.customScripts, JSON.stringify(customScriptsData));
        }} catch (e) {{}}
        renderEmergencyScriptList();
        selectEmergencyScript(id);
        showToast("Custom Emergency Script created!");
      }} else if (currentCustomItemType === "workflow") {{
        const name = (document.getElementById("custWfName").value || "Custom Workflow").trim();
        const dept = (document.getElementById("custWfDept").value || "Dept 01").trim();
        const tier = document.getElementById("custWfTier").value;
        travWorkflowsData.push({{ name: name, dept: dept, tier: tier, risk: 25, amber: tier.includes("Amber") ? "Yes" : "No", isCustom: true }});
        try {{
          localStorage.setItem(STORAGE_KEYS.travWorkflows, JSON.stringify(travWorkflowsData));
        }} catch (e) {{}}
        renderTravTable();
        showToast("Custom workflow added to matrix.");
      }} else if (currentCustomItemType === "task") {{
        const title = (document.getElementById("custTaskTitle").value || "Custom Task").trim();
        const phase = document.getElementById("custTaskPhase").value;
        const id = `cust_m_${{Date.now()}}`;
        roadmapTasksData.push({{ id: id, phase: phase, title: title }});
        try {{
          localStorage.setItem(STORAGE_KEYS.roadmapTasks, JSON.stringify(roadmapTasksData));
        }} catch (e) {{}}
        renderRoadmapMilestones();
        showToast("Custom roadmap task added.");
      }} else if (currentCustomItemType === "kpi") {{
        const name = (document.getElementById("custKpiName").value || "Custom KPI").trim();
        const dept = (document.getElementById("custKpiDept").value || "Dept 01").trim();
        const tgt = (document.getElementById("custKpiTarget").value || "Target").trim();
        const act = (document.getElementById("custKpiActual").value || "Actual").trim();
        kpiMetricsData.push({{ name: name, dept: dept, target: tgt, actual: act, amber: "Review", isCustom: true }});
        saveKpiState();
        showToast("Custom KPI added.");
      }}
      closeCustomItemModal();
    }}

    // =========================================================================
    // WORKSPACE BACKUP & RESTORE (1-CLICK JSON ENGINE)
    // =========================================================================
    function openBackupModal() {{
      document.getElementById("backupModal").classList.add("open");
    }}

    function closeBackupModal() {{
      document.getElementById("backupModal").classList.remove("open");
    }}

    function exportWorkspaceJson() {{
      const notes = {{}};
      for (let i = 1; i <= 6; i++) {{
        notes[`m${{i}}`] = localStorage.getItem(`smallbiz_notes_m${{i}}`) || "";
      }}

      const backupObj = {{
        app: "The Small Business AI Automation Operating System",
        author: "OMAR SUNNY",
        version: "2026 Enterprise Edition",
        exportedAt: new Date().toISOString(),
        tierState: {{
          currentTier: currentTier,
          unlockedTier2: unlockedTier2,
          unlockedTier3: unlockedTier3
        }},
        cmfGlobals: {{
          revenue: document.getElementById("cmfRevenue").value,
          ownerRate: document.getElementById("cmfOwnerRate").value,
          teamSize: document.getElementById("cmfTeamSize").value
        }},
        cmfRows: cmfRowsData,
        stlChannels: stlChannelsData,
        customPrompts: customPromptsData,
        editedPrompts: editedPromptTemplates,
        customScripts: customScriptsData,
        editedScripts: editedScriptTemplates,
        travWorkflows: travWorkflowsData,
        roadmapTasks: roadmapTasksData,
        roadmapChecks: roadmapCheckedState,
        kpiMetrics: kpiMetricsData,
        kpiSnapshots: kpiSnapshotsData,
        moduleNotes: notes
      }};

      downloadFile(JSON.stringify(backupObj, null, 2), "smallbiz-automation-os-workspace-backup.json", "application/json");
      showToast("Workspace backup exported successfully!");
    }}

    function handleWorkspaceFileSelect(event) {{
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {{
        try {{
          const data = JSON.parse(e.target.result);
          if (data.cmfRows) {{
            localStorage.setItem(STORAGE_KEYS.cmfRows, JSON.stringify(data.cmfRows));
            cmfRowsData = data.cmfRows;
          }}
          if (data.cmfGlobals) {{
            localStorage.setItem(STORAGE_KEYS.cmfGlobals, JSON.stringify(data.cmfGlobals));
            if (data.cmfGlobals.revenue) document.getElementById("cmfRevenue").value = data.cmfGlobals.revenue;
            if (data.cmfGlobals.ownerRate) document.getElementById("cmfOwnerRate").value = data.cmfGlobals.ownerRate;
            if (data.cmfGlobals.teamSize) document.getElementById("cmfTeamSize").value = data.cmfGlobals.teamSize;
          }}
          if (data.stlChannels) {{
            localStorage.setItem(STORAGE_KEYS.stlChannels, JSON.stringify(data.stlChannels));
            stlChannelsData = data.stlChannels;
          }}
          if (data.customPrompts) {{
            localStorage.setItem(STORAGE_KEYS.customPrompts, JSON.stringify(data.customPrompts));
            customPromptsData = data.customPrompts;
          }}
          if (data.editedPrompts) {{
            localStorage.setItem(STORAGE_KEYS.editedPrompts, JSON.stringify(data.editedPrompts));
            editedPromptTemplates = data.editedPrompts;
          }}
          if (data.customScripts) {{
            localStorage.setItem(STORAGE_KEYS.customScripts, JSON.stringify(data.customScripts));
            customScriptsData = data.customScripts;
          }}
          if (data.editedScripts) {{
            localStorage.setItem(STORAGE_KEYS.editedScripts, JSON.stringify(data.editedScripts));
            editedScriptTemplates = data.editedScripts;
          }}
          if (data.travWorkflows) {{
            localStorage.setItem(STORAGE_KEYS.travWorkflows, JSON.stringify(data.travWorkflows));
            travWorkflowsData = data.travWorkflows;
          }}
          if (data.roadmapTasks) {{
            localStorage.setItem(STORAGE_KEYS.roadmapTasks, JSON.stringify(data.roadmapTasks));
            roadmapTasksData = data.roadmapTasks;
          }}
          if (data.roadmapChecks) {{
            localStorage.setItem("smallbiz_os_roadmap_checks", JSON.stringify(data.roadmapChecks));
            roadmapCheckedState = data.roadmapChecks;
          }}
          if (data.kpiMetrics) {{
            localStorage.setItem(STORAGE_KEYS.kpiMetrics, JSON.stringify(data.kpiMetrics));
            kpiMetricsData = data.kpiMetrics;
          }}
          if (data.kpiSnapshots) {{
            localStorage.setItem(STORAGE_KEYS.kpiSnapshots, JSON.stringify(data.kpiSnapshots));
            kpiSnapshotsData = data.kpiSnapshots;
          }}
          if (data.moduleNotes) {{
            for (let i = 1; i <= 6; i++) {{
              if (data.moduleNotes[`m${{i}}`] !== undefined) {{
                localStorage.setItem(`smallbiz_notes_m${{i}}`, data.moduleNotes[`m${{i}}`]);
              }}
            }}
            initModuleNotes();
          }}
          if (data.tierState) {{
            currentTier = data.tierState.currentTier || 0;
            unlockedTier2 = !!data.tierState.unlockedTier2;
            unlockedTier3 = !!data.tierState.unlockedTier3;
            localStorage.setItem(STORAGE_KEYS.currentTier, currentTier.toString());
            localStorage.setItem(STORAGE_KEYS.unlockedTier2, unlockedTier2 ? "true" : "false");
            localStorage.setItem(STORAGE_KEYS.unlockedTier3, unlockedTier3 ? "true" : "false");
          }}

          renderCmfTable();
          calculateCmf();
          renderStlTable();
          renderPromptList();
          renderEmergencyScriptList();
          renderTravTable();
          renderRoadmapMilestones();
          renderKpiTable();
          applyTierStateUI();

          closeBackupModal();
          showToast("Workspace restored successfully!");
        }} catch (err) {{
          alert("Invalid workspace backup file: " + err.message);
        }}
      }};
      reader.readAsText(file);
    }}

    // =========================================================================
    // GENERAL UTILITIES
    // =========================================================================
    function copyToClipboard(text, successMsg) {{
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(() => {{
          showToast(successMsg);
        }}).catch(() => fallbackCopy(text, successMsg));
      }} else {{
        fallbackCopy(text, successMsg);
      }}
    }}

    function fallbackCopy(text, successMsg) {{
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      showToast(successMsg);
    }}

    function downloadFile(content, fileName, mimeType) {{
      const blob = new Blob([content], {{ type: mimeType }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    // =========================================================================
    // INITIALIZATION ON DOM READY
    // =========================================================================
    window.addEventListener("DOMContentLoaded", () => {{
      // Load saved tier
      try {{
        unlockedTier2 = (localStorage.getItem(STORAGE_KEYS.unlockedTier2) === "true");
        unlockedTier3 = (localStorage.getItem(STORAGE_KEYS.unlockedTier3) === "true");
        const savedTier = localStorage.getItem(STORAGE_KEYS.currentTier);
        currentTier = savedTier ? parseInt(savedTier, 10) : 0;
      }} catch (e) {{}}

      initCmfData();
      initStlData();
      initPromptData();
      initEmergencyData();
      initTravData();
      initKpiData();
      initModuleNotes();
      applyTierStateUI();

      console.log("The Small Business AI Automation OS — Web Companion initialized.");
    }});
  </script>
</body>
</html>
"""

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated upgraded Web App ({len(html_content):,} chars) at: {APP_PATH}")

# Sync to web deployment dist
dist_app = os.path.join(STUDIO_ROOT, "15-WEB-DEPLOYMENT", "dist", "app", "index.html")
if os.path.exists(os.path.dirname(dist_app)):
    shutil.copyfile(APP_PATH, dist_app)
    print(f"Synced to {dist_app}")
