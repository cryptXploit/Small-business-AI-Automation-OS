# Editorial & Architectural Style Guide: The Small Business AI Automation Operating System

**Document ID:** `SMALLBIZ-AI-AUTOMATION-OS-STYLE-GUIDE`  
**Enforcement Level:** Automated Hard-Gate Verification (`verify_phase1.py` .. `verify_phase9.py`)  
**Target Audience:** Small Business Owners, Managing Partners, Practice Managers, and Operations Leads (1–25 Employees)

---

## 1. Editorial Voice & Operational Tone

Every page of *The Small Business AI Automation Operating System* is written from the perspective of an experienced **Chief Operating Officer and Systems Architect** who has personally audited, standardized, and automated hundreds of 1–25 person companies across North America, the UK, Europe, and Australia.

1. **Direct, Numerate, and Concrete:** Every claim must be anchored in operational metrics (minutes per task, response-time windows in seconds, close-rate percentages, hourly labor rates, and monthly cashflow impact).
2. **Multi-Vertical Inclusivity:** Every chapter must include concrete operational examples across three core small business archetypes:
   * **Archetype A — Local Field & Clinical Services:** HVAC/plumbing/electrical, dental/medical/wellness clinics, legal/accounting firms.
   * **Archetype B — B2B Agencies & Professional Studios:** Marketing/web agencies, consulting practices, recruiting firms, architectural studios.
   * **Archetype C — Specialized Retail & Omni-Channel E-Commerce:** Custom DTC brands, wholesale/distribution operators, specialty manufacturing shops.
3. **Tool-Agnostic Systems First:** Explain the exact trigger, payload structure, AI prompt contract, human approval gate, and destination database write so the reader can implement the workflow in Make, Zapier, n8n, HighLevel, HubSpot, QuickBooks, Xero, Notion, or Google Workspace.

---

## 2. Mandatory 14-Part Studio Chapter Schema

Every manuscript chapter (`03-MANUSCRIPT/chapter-01.md` through `03-MANUSCRIPT/chapter-10.md`) MUST contain at least **6,500 words** and follow this exact 14-part structural hierarchy:

1. **H1 Title:** `# Chapter X: [Chapter Title]` (plus optional operational subtitle/metadata block)
2. `## 1. Learning Objectives` — 6 measurable, action-oriented operational outcomes the owner will achieve by completing the chapter.
3. `## 2. The Real-World Friction Point` — Granular diagnostic of how the manual bottleneck manifests on a Monday morning, including hidden labor costs and revenue leaks.
4. `## 3. Why Standard Approaches Fail` — Analysis of why cheap unmanaged labor, disconnected SaaS subscriptions ("App Sprawl"), or naive one-line chat prompts break in production.
5. `## 4. Core Framework: [Named Chapter Framework]` — Complete architectural specification, mathematical formulas, worked financial tables across 3 business sizes, and data contracts.
6. `## 5. Visual Architecture: System Mindmap` — Must embed `![Chapter X Mindmap](../04-VISUAL-ASSETS/chapter-XX-mindmap.svg)` and provide a node-by-node architectural walkthrough.
7. `## 6. Step-by-Step Implementation Protocol` — A 7-step operational runbook with exact field mappings, webhook payload schemas, and staff handoff rules.
8. `## 7. Operational Decision Tree` — Must embed `![Chapter X Flowchart](../04-VISUAL-ASSETS/chapter-XX-flowchart.svg)` and walk through every conditional gate and routing rule.
9. `## 8. Tested AI Workflow Prompts` — Exactly **5 production-tested prompts** (`Prompt X.1` through `Prompt X.5`), each following the 7-part Prompt Engineering Contract below.
10. `## 9. Real-World Implementation Case Study` — Named small business case study with employee count, annual revenue, implementation timeline, and a **Before vs. After Operational Metrics** Markdown table.
11. `## 10. Common Operational Pitfalls & Fixes` — Structured Markdown table detailing 8 production failure modes, root causes, and exact operational fixes.
12. `## 11. Chapter Action Worksheet` — Guided action plan linking directly to `05-WORKBOOKS/worksheet-XX.md`.
13. `## 12. Executive Summary & Implementation Checklist` — 10-point verification checklist (`[ ]`) that must be signed off before advancing to the next chapter.
14. `## 13. Sources & Operational References` — Empirical studies, industry benchmarks, and standards cited in the chapter.

---

## 3. Mandatory 7-Part Prompt Engineering Contract

Each of the 50 prompts across the book (`Prompt 1.1` through `Prompt 10.5`) must be formatted as a production-ready operational asset containing all seven components:

1. **Header:** `### Prompt X.Y: [Descriptive Operational Name]`
2. **Objective:** What specific operational bottleneck this prompt resolves and what measurable output it generates.
3. **Department & Trigger:** Which of the 5 Departments (`Dept 01`–`Dept 05`) owns the prompt and what event triggers it (manual audit, webhook, email arrival, form submission, Friday cron).
4. **Input Variables:** Explicit list of bracketed uppercase variables required (e.g., `[BUSINESS_NAME]`, `[INDUSTRY_VERTICAL]`, `[BLENDED_HOURLY_RATE]`, `[RAW_TASK_LOG]`).
5. **Copy-Ready System & User Prompt Block:** Enclosed in a fenced code block (`text` or `markdown`) containing Role Definition, Context Injection, Task Instructions, Execution Rules & Negative Guardrails, and Output Format Specification.
6. **Expected Output Schema:** Structural specification (JSON schema or Markdown table columns) so downstream automation bridges can parse the response deterministically.
7. **Realistic Sample Output:** A complete, filled-in example output demonstrating how the prompt performs on realistic small business data.

---

## 4. Visual Asset & Typography Standards

### 4.1 Executive Emerald & Slate Color Palette
All SVGs, PDF exports, web applications, spreadsheets, slide decks, and Word documents must strictly enforce these hex tokens:
* **Primary (`#0F172A`):** Deep Executive Navy/Slate — Main structural headers, central hub nodes, primary backgrounds.
* **Accent (`#059669`):** Operations Emerald — Active automation nodes, revenue recovery highlights, positive KPI badges.
* **Secondary (`#0284C7`):** System Cyan/Blue — Data routing bridges, secondary department modules, webhook connectors.
* **Warning (`#D97706`):** Amber Approval Gate — Human-in-the-loop verification gates, exception escalations, risk thresholds.
* **Text (`#1E293B`):** High-Contrast Slate Body — Main readable prose and dark text inside light cards.
* **Muted (`#64748B`):** Slate Muted — Captions, footers, axis labels, secondary annotations.
* **Canvas (`#FFFFFF`):** Pure White — Document page canvas and card interiors.

### 4.2 Vector SVG Diagram Rules
* Every SVG file in `04-VISUAL-ASSETS/` must parse cleanly via `xml.etree.ElementTree`.
* Required root attribute: `viewBox="0 0 900 480"`, `width="900"`, `height="480"`.
* Typography: `font-family="Inter, 'Segoe UI', Arial, sans-serif"`, minimum label size `10px` so text remains crisp at both 100% digital zoom and `6"×9"` print reduction.
* Every diagram must remain legible when converted to 300-DPI grayscale for Amazon KDP print (use distinct border weights, badge shapes, and high-contrast text rather than relying on color hue alone).

---

## 5. Strict Banned AI Cliché & Placeholder Policy (Zero Tolerance)

Automated verification scripts scan all manuscript, research, architecture (`toc.md`, `sources.md`), and workbook files. Any match triggers an immediate build failure.

### 5.1 Banned Single Words (Case-Insensitive Whole-Word Match)
Never use any of the following words in prose, headings, prompts, or UI labels:
* `delve`
* `tapestry`
* `testament`
* `beacon`
* `symphony`
* `unlock` *(Replacement: use "Activate", "Access", "Enable", or "Open")*
* `unleash` *(Replacement: use "Deploy", "Launch", or "Execute")*
* `skyrocket` *(Replacement: use "Increase", "Compound", or "Accelerate")*
* `supercharge` *(Replacement: use "Optimize", "Accelerate", or "Upgrade")*
* `game-changer` *(Replacement: use "Structural advantage" or "Operational upgrade")*
* `pivotal` *(Replacement: use "Critical", "Core", or "Decisive")*
* `realm` *(Replacement: use "Domain", "Department", or "Environment")*
* `foster` *(Replacement: use "Build", "Support", or "Maintain")*
* `underscore` *(Replacement: use "Highlight", "Demonstrate", or "Confirm")*
* `utilize` *(Replacement: always use "use")*
* `leverage` *(Replacement: always use "apply", "use", or "deploy")*

### 5.2 Banned Phrases (Case-Insensitive Substring Match)
* `in today's fast-paced world`
* `ever-evolving landscape`
* `it is important to remember`
* `in conclusion`
* `without further ado`
* `let's dive in`
* `look no further`

### 5.3 Banned Placeholders (Zero Tolerance)
* `TODO`
* `TBD`
* `Lorem ipsum`
* `[XX]`

*(Note: Descriptive uppercase prompt input variables such as `[BUSINESS_NAME]`, `[SERVICE_CATEGORY]`, `[HOURLY_LABOR_COST]`, and `[CRM_PLATFORM]` inside AI prompt templates and worksheets are explicitly permitted and required.)*
