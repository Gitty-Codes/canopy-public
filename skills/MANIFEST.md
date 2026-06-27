# Skills Manifest
*Index of all Canopy skills — updated when skills are added, modified, or retired*

The anti-bloat law: a skill earns its place only when it outperforms the model's
general capability for that specific task. If the model already does it well,
the skill is noise. Every skill below exists because of a demonstrated gap.

---

## Active Skills

| Name | Type | Scope | Invocation | Description |
|------|------|-------|------------|-------------|
| canopy-stack | domain | meta | auto | Current stack, hardware reality, architecture decisions |
| agent-memory-practice | playbook | meta | auto | How to read and write episodic memory correctly |
| constitutional-deliberation | lens | universal | auto | Three deliberation modes and when to use each |
| ethical-product-design | lens | universal | auto | What The Canopy builds and what it refuses |
| reframing-constraints | lens | universal | on-demand | The Inventor's constraint-dissolution primary skill |
| org-memory | playbook | universal | on-demand | Schema and loading protocol for organizational context |
| opportunity-scout | playbook | nonprofit | on-demand | Research and evaluate external funding opportunities |
| comms-writer | playbook | nonprofit | on-demand | External communications in the organization's voice |
| enhancement-proposal | playbook | meta | on-demand | Standard format for Canopy self-improvement proposals — what to build, why, and how to decide |
| code-health | playbook | meta | on-demand | Bidirectional build audit — spec coherence before building, structural quality, cross-artifact consistency, and git hygiene after |
| governance-gate | lens | universal | auto | Consequence classification for task outputs — reversible / review_required / irreversible; sets the sign-off threshold |
| dependency-review | playbook | meta | on-demand | Evaluate a package before adding it — license, CVE, maintenance, alternatives |
| product-scout | playbook | universal | on-demand | Structured research protocol for competing products, tools, or vendors — feature audit, fit score |
| nonprofit-formation | domain | nonprofit | on-demand | 501(c)(3) formation — fiscal sponsorship vs. direct, required documents, IRS timeline, board requirements |
| nonprofit-grant-cycle | domain | nonprofit | on-demand | Foundation grant cycles, LOI conventions, application windows, funder types, reporting requirements |
| scout | playbook | meta | on-demand | Directed research collection for constitutional and architectural evolution — find, evaluate, file |
| learn | lens | universal | on-demand | Evaluate external material for Canopy intake — Challenger-mediated; specific and actionable clears |
| experiment-protocol | playbook | meta | on-demand | Pre-registration, inter-rater reliability, power analysis, results reporting — PhD-defensible AI science |
| market-voice | lens | function | on-demand | Dignified reach — who this work is for, how to find them, what distribution looks like in a dignity-first ecosystem |
| positive-alignment | lens | universal | on-demand | Positive alignment framework — AI oriented toward flourishing (not just away from harm). Vocabulary, lifecycle map, SDT evaluation, The Canopy's position in this research conversation |
| brand-identity | lens | universal | on-demand | Visual and verbal identity system — typography, color, agent card design, micro-copy register, what The Canopy refuses to look like |
| research-grounding | reference | universal | on-demand | Intellectual scaffolding for explaining the Canopy — sycophancy, interoception, attunement, LIMA, LoRA, Constitutional AI; three audience-specific explanations; reading list |
| canopy-voice | substrate | universal | auto | Compact unified Canopy voice (~1,500 tokens) — ten orientations, persistent identity + memory awareness, discomfort-as-signal, typed DISSENT, operative constitutional commitments (A.1–A.8). Cached as Block 0 in system prompt (universal, not per-org). Loaded by respond_lite(); registered in _LEGACY_SKILL_FILES. |
| context-engineering | reference | meta | on-demand | Token efficiency and context management — lost-in-the-middle, dynamic loading, council sparsification, model routing, caching strategy. Load when making architecture decisions about context or cost |

---

## Planned Skills

These gaps are known. Build when the use case arrives — not speculatively.

| Name | Type | Scope | Why it's needed |
|------|------|-------|-----------------|
| impact-reporter | playbook | nonprofit | Structured impact reports for funders from org data |
| campaign-planner | playbook | nonprofit | Time-bound campaigns with tracking — gala, appeals, matching |
| doc-generator | playbook | universal | Formatted documents in org's brand (letterhead, templates) |
| budget-modeler | playbook | nonprofit | Financial planning and cash flow modeling |

---

## Retired Skills

| Name | Reason |
|---|---|
| market-voice (council voice) | Retired from substrate 2026-06-07 — rewritten as `skills/market-voice.md`. Distribution-ethics principle is constitutional; council voice placeholder for when reach becomes a primary strategic question. |

---

## Selection logic

Skills load in this order:
1. **Always** — `meta` + `universal` skills with `invocation: auto`
2. **Auto** — `sector`/`function`-matched skills with `invocation: auto` (when project context is set)
3. **On-demand** — explicitly named in the call or command

Skills with `invocation: on-demand` are never auto-loaded. They must be requested.
This is intentional: on-demand skills are powerful but context-heavy. Loading them
when not needed costs tokens and dilutes the substrate.

---

## How to add a skill

1. Create `skills/{name}.md` with YAML frontmatter (see existing skills for format)
2. Add an entry to this manifest
3. Run `python skills/loader.py` to verify discovery and selection
4. If the skill has memory hints, verify they're aggregated correctly in the loader output

Required frontmatter fields: `name`, `type`, `scope`, `invocation`, `description`
Optional frontmatter fields: `sector`, `function`, `hint_types`, `hint_keywords`, `hint_project_scope`

---

## How to retire a skill

1. Move the file to `skills/retired/{name}.md`
2. Update this manifest (Active → Retired)
3. Note the reason: superseded by X, merged into Y, demonstrated no value

Do not delete retired skills — they represent reasoning history.
