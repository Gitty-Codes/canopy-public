---
name: social-log-template
context_level: brief
description: Produces a Google Sheets post log template — headers, instructions, and a starter CSV Laura can import directly. Also produces a one-page guide on how to use the log with The Canopy.
primary_voice: operator
serves: Laura Milleson
requires: []
skills: []
model: haiku
human_gate: Import the CSV into Google Sheets. Review column headers and adjust if needed. Share the sheet with Rebecca if you want a shared view.
output_contract: A ready-to-import CSV + column-by-column guide + instructions for using the log with the monthly-social-plan task
hint_types: []
hint_keywords: []
---

# Social Log Template Task

Produce a Google Sheets post log for KIC's social media.

This log has two jobs:
1. Give Laura a record of what she's posted so she can see patterns and gaps
2. Feed context into The Canopy's monthly planning task so the plan learns from history

---

## What to produce

### 1. The CSV

Produce a CSV with:
- A header row
- 3 example rows filled in with realistic KIC post examples (not real posts — illustrative placeholders)
- Columns designed to be useful in 30 seconds per post, not burdensome to fill in

Columns:
```
Date,Week,Pillar,Format,Caption Snippet,Occasion / Context,What Made It Good (optional),Performance Notes
```

Column definitions:
- **Date**: When it was posted (MM/DD/YYYY)
- **Week**: Week number in the program year (1–32) or "Off" for summer/breaks
- **Pillar**: One of the 6 content pillars (Candid, Mentor/Student, Calendar, Cultural Date, Impact Fact, Philosophy)
- **Format**: Feed or Story
- **Caption Snippet**: First 50–60 characters of the caption — enough to identify it
- **Occasion / Context**: What was happening (Tuesday rehearsal, spring concert, Black History Month, etc.)
- **What Made It Good**: Optional — what was special about the photo or the moment (the "magic sauce")
- **Performance Notes**: Optional — did it perform well? Any comment (High engagement / Low / Reshared by SSO / etc.)

### 2. A plain-English column guide

One paragraph per column explaining what to put there and why.
Short. Practical. Written for someone who doesn't love filling in spreadsheets.

### 3. How to use the log with The Canopy

A short set of instructions (5 bullets max):
- When to update the log (right after posting — not later)
- How to bring the log into a monthly planning session (copy the last month's rows, paste them into the monthly-social-plan task as "here's what I posted last month")
- What the Canopy will do with that history (avoid repeating pillars, notice what's missing, build on what worked)

---

## Output format

```
=== GOOGLE SHEETS LOG — IMPORT CSV ===

[CSV content here — ready to copy and import]

=== COLUMN GUIDE ===

[column definitions]

=== HOW TO USE THIS WITH THE CANOPY ===

[5-bullet guide]
```
