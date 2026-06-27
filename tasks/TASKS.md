# Tasks Manifest
*Index of all Canopy task agents — updated when tasks are added, modified, or retired*

A task agent is a named context profile: primary voice, skill context, org memory,
output contract, and the people it serves. The harness runs them. Character travels
in the profile definition, not in Python code.

The anti-bloat law applies here too: a task earns its place by producing a
demonstrably better artifact than a bare council call. The first task must prove
this before the second is built.

---

## Active Tasks

| Name | Primary Voice | Serves | Description |
|------|---------------|--------|-------------|
| nonprofit-comms | listener | students, families, community partners, funders | External communications in a nonprofit's voice. Webapp aliases: `social-post` (Haiku), `donor-email` (Haiku), `board-memo` (Sonnet) |
| grant-loi | strategist | funders, foundation program officers, corporate giving staff | Letters of intent to private foundations and corporate funders. Webapp alias: `grant-loi` (Sonnet) |
| campaign | strategist | nonprofit development staff, executive directors, communications leads | Campaign plan — fundraising, awareness, advocacy, or program launch. Produces CANVA COPY BLOCKS structured output. Webapp alias: `campaign` (Sonnet) |
| funder-brief | strategist | executive directors, development officers | Pre-LOI research brief — fit score, recommended language, proceed/don't decision |
| product-spec | product_partner | founders, product teams, engineers | PRD with dignity considerations — user stories, acceptance criteria, tradeoffs named explicitly |
| research | listener | founders, product teams, investors, development staff | Structured research brief — customer discovery, competitive analysis, opportunity assessment, benchmarking. Webapp alias: `research` (Sonnet) |

---

## Planned Tasks

These are known gaps. Build when a real project demands them, not speculatively.
Prove outperformance before moving to Active.

| Name | Primary Voice | Serves | Why it's needed |
|------|---------------|--------|-----------------|
| impact-report | strategist | funders, board | Impact reporting structured for nonprofit funders — honest about gaps, not inflated |
| grant-research | listener + strategist | programs, students | Funder research and opportunity assessment — landscape scan, fit scoring, priority list |
| ~~product-spec~~ | — | — | Built and moved to Active. |
| ~~research~~ | — | — | Built and moved to Active. |

---

## Retired Tasks

None yet.

---

## How to add a task

1. Create `tasks/{name}.md` with YAML frontmatter (see schema below)
2. Call `harness.run_task(name, inputs)` and compare to `harness.respond()`
3. Only promote to Active after demonstrating the output is measurably better
4. Add an entry to this manifest

**Required frontmatter fields:** `name`, `description`, `primary_voice`, `serves`, `human_gate`
**Optional frontmatter fields:** `requires`, `skills`, `output_contract`, `consequence_level`, `hint_types`, `hint_keywords`, `hint_project_scope`

```yaml
---
name: task-name
description: One-line description of what this task produces
primary_voice: listener          # maps to a voice in DOMAIN_HINTS
serves: who is downstream        # the people at the end of this artifact
requires: [skill-name]           # skills that must exist; fails fast if missing
skills: [skill-a, skill-b]       # skills to load for this task
human_gate: Review before sending. This draft requires human approval.
consequence_level: review_required  # reversible | review_required | irreversible; see governance-gate skill
hint_types: [session, decision]
hint_keywords: [relevant, terms]
hint_project_scope: true
---
```

---

## How to retire a task

1. Move to `tasks/retired/{name}.md`
2. Update this manifest (Active → Retired)
3. Note the reason: superseded by X, demonstrated no value, merged into Y

Do not delete retired tasks — they represent reasoning history.

---

## The anti-bloat check

Before promoting a task to Active:

```bash
python harness.py
# Default mode: ask the same question bare
# Then: task <name> with the same inputs
# Compare outputs honestly
```

If the task output is not meaningfully better — clearer, more grounded in org context,
more dignity-aware — do not add it. The general model with a good prompt may be enough.
