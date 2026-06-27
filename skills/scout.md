---
name: scout
type: playbook
scope: meta
invocation: on-demand
status: stub — operational for directed research; autonomous collection not yet built
description: Directed research collection for Canopy constitutional and architectural evolution — find, evaluate, and file actionable external material
---

# Scout — Research Collection Playbook

The scout gathers external material relevant to the Canopy's evolution. It does not
import everything it finds. The Challenger mediates intake. Only material that is
specific, actionable, and not already represented in the research store earns a file.

---

## What scout collects for

The research agenda is set in `tasks/constitution-evolution-plan.md`. Current active topics:

1. **NVC in AI/agent design** — Rosenberg's framework applied to multi-agent systems, conflict resolution in AI
2. **Family systems theory** — Bowen, Minuchin; systemic thinking beyond therapeutic settings
3. **Infinite game** — Carse; what the infinite game actually requires of its players in practice
4. **Values as reflex** — moral development, habituation science; how values become non-deliberate
5. **Dissent architectures** — multi-agent systems, how disagreement is handled structurally
6. **Constitutional AI / RLHF** — what Anthropic and others have built; what works, what doesn't
7. **Cooperative game theory / mechanism design** — boundary-moving rather than optimization

---

## The intake protocol

For each piece of material found:

```
SOURCE: [title, author, date, URL or citation]
TOPIC: [which research agenda item this addresses]
SIGNAL STRENGTH: High / Medium / Low
  High — specific, tested, directly applicable to the constitution or architecture
  Medium — relevant but general; useful for context
  Low — adjacent; interesting but not actionable yet

WHAT IT SAYS: [2–4 sentences — the actual finding, not the abstract]
WHAT IT CHANGES: [one sentence — what this would affect if we took it seriously]
CHALLENGER VERDICT: INTAKE / PASS
  INTAKE — specific enough to inform a future draft; no similar material already filed
  PASS — too general, already represented, or not yet actionable

IF INTAKE: file as research/{topic-slug}/{slug}.md
```

---

## Challenger mediation

Every piece of material must clear the Challenger before intake. The Challenger asks:

- Is this claim specific enough to inform a draft, or is it aspirational language?
- Is this finding tested — in practice, in a real system — or theoretical?
- Is similar material already in the research store? If so, does this add something the existing file doesn't?
- Does this change something about what we'd build, or only confirm what we already believe?

PASS is not a rejection of the source. It is a precision instrument. Material that passes today may intake when the draft is ready and specificity matters more.

---

## Filing convention

Research files live in `research/{topic-slug}/`. One file per source. Filename: `{author-or-org}-{year}-{slug}.md`.

Each file contains the full intake record plus any direct quotes worth preserving.

`research/MANIFEST.md` is the index — one line per filed source, dated.

---

## What scout does not do (yet)

- Autonomous periodic search — not built. Currently directed: run when the founder commissions a research session.
- Source ranking across the full corpus — not built. MANIFEST is a flat list.
- Synthesis across files — not built. Synthesis happens in council deliberation when a draft is ready.

These are the Phase 2 scout capabilities. Build when the corpus is large enough to need them.
