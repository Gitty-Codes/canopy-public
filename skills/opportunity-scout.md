---
name: opportunity-scout
type: playbook
scope: sector
sector: nonprofit
function: fundraising
invocation: on-demand
hint_types: [decision, project]
hint_keywords: [funder, grant, application, declined, awarded, partnership, RFP, foundation, opportunity]
hint_project_scope: true
description: Research and evaluate external funding opportunities — grants, foundations, RFPs, partnerships — for a specific organization
---

# Opportunity Scout — Funding Opportunity Research Playbook

This skill turns the org's story assets into a structured search for fundable matches.
It is not a generic grant list. It is a fit-assessed, prioritized set of opportunities
matched to what this specific organization can credibly win.

---

## What this skill does

Given org memory (who they are, what they've done, what they need) and a search
context (geography, deadline window, opportunity type), this skill:

1. Identifies candidate funders or partnership opportunities
2. Assesses fit: Strong / Moderate / Weak — with reasoning
3. Surfaces the right story assets to lead with for each funder
4. Flags misalignments or red flags before the application begins
5. Produces a prioritized list with application sequence and next steps

---

## Inputs

**Required:**
- Org memory (identity, outcomes, partnerships, current funding picture)
- Geography / jurisdiction (where the org operates, where funders must focus)

**Optional but high-value:**
- Deadline window (e.g., "applications due within 60 days")
- Opportunity type (foundation grants, government grants, corporate sponsorship, RFPs)
- Amount range (floor/ceiling for viable grants)
- Funders who have already declined (never re-approach without a strategy)
- Funders with active warm relationships (warm introductions move faster)

---

## Fit assessment rubric

**Strong** — All three are true:
- Geographic and sector alignment is explicit in the funder's stated priorities
- The org's outcomes match what the funder funds for (not adjacent — direct)
- No known misalignment in demographics, model, or approach

**Moderate** — Two of three are true, or Strong with one complication:
- Alignment is present but not the funder's primary focus
- Application requires careful positioning (lead with X, not Y)
- A warm introduction would move this from Moderate to Strong

**Weak** — Proceed only with a specific strategy:
- Significant misalignment that cannot be overcome with framing
- Funder has already declined without changed circumstances
- Geography or eligibility is a hard barrier

---

## Output format

For each opportunity:

```
FUNDER: [Name]
FIT: Strong / Moderate / Weak
AMOUNT RANGE: [$X–$Y]
DEADLINE: [date or cycle]
LEAD WITH: [which story asset to open with — specific, not generic]
AVOID: [what not to emphasize for this funder]
WARM PATH: [who at the org knows someone at the funder, or which partner could intro]
NEXT STEP: [exactly what to do — LOI, full app, contact program officer, etc.]
NOTES: [anything else — red flags, timing constraints, relationship history]
```

---

## Sequencing principle

Apply in order:
1. **Decline first** — check memory for funders who have already said no. Never
   recommend re-approaching without noting the history and the reason now is different.
2. **Warm before cold** — warm introductions through existing partners outperform cold
   applications at roughly 3:1. Map the warm paths before recommending cold outreach.
3. **Local before national** — local and regional funders move faster, know the community,
   and are often less competitive. They belong in the immediate pipeline.
4. **Sector-specific before general** — funders who already understand the model
   (El Sistema, youth orchestra, tribal education) need less convincing than generalists.
5. **Foundation before government** — federal and state grants have the longest cycles
   and most reporting burden. Apply, but do not let them crowd out faster opportunities.

---

## What makes a nonprofit fundable

Load this into every opportunity assessment:

- **Specific outcomes over activity** — "100% high school graduation rate" funds.
  "We serve 75 students" does not. Funders invest in demonstrated results.
- **Community rootedness over reach** — A tribal partnership earned over years signals
  authentic community trust. An org that "serves diverse communities" is generic.
- **Institutional affiliations as credibility signals** — El Sistema USA membership,
  Seattle Symphony relationship, LA Phil/YOLA connection. These are not logo placements;
  they tell funders this org is vetted by organizations the funder already trusts.
- **Supply-constrained over demand-constrained** — An org that more people want than
  can currently be served is fundable. One that struggles to find participants is not.

---

## After the list

The opportunity list is the beginning of the work, not the end. For each Strong or
Moderate opportunity:
- Identify the relationship holder at the org
- Identify the program officer or contact at the funder (if known)
- Set a specific next-step date
- Track in the org's project memory so nothing falls through

The opportunity scout produces a prioritized list. The comms-writer skill turns that
list into actual applications and LOIs.
