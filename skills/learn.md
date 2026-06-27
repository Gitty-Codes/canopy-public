---
name: learn
type: lens
scope: universal
invocation: on-demand
description: Evaluate external material for Canopy intake — Challenger-mediated; specific and actionable clears; aspirational language does not
---

# /learn — External Material Intake

`/learn [source or topic]` evaluates external material for intake into the Canopy's
knowledge base. The Challenger mediates. The standard is specific and actionable —
not interesting, not adjacent, not confirmatory of what we already believe.

---

## What this is for

The Canopy grows by encountering the world and keeping what is genuinely useful.
`/learn` is the gate. It exists because indiscriminate intake creates noise, and
noise costs tokens, attention, and the integrity of the substrate.

Every piece of material that clears `/learn` changes something — either in how we
deliberate, what we build, or what we hold as true. Material that doesn't change
anything doesn't clear.

---

## The evaluation sequence

**1. Read the material honestly.**
Not looking for confirmation. Not looking for rejection. What is actually here?

**2. The Listener names the signal.**
What is this source actually saying? What pain or insight does it carry?
What is the most honest summary — not the abstract, the actual finding?

**3. The Challenger examines.**
- Is this specific enough to inform a draft or a build decision?
- Is it tested — in practice, in a real system — or purely theoretical?
- Does it add something the Canopy doesn't already hold?
- What would have to change if we took this seriously?

**4. Verdict.**
- **INTAKE** — file in `research/{topic-slug}/` using the scout filing convention
- **HOLD** — return when a specific draft is in progress and specificity matters more
- **PASS** — too general, already represented, or not actionable at any horizon

**5. If INTAKE — note what it changes.**
One sentence. If you can't complete "this changes ___," the material doesn't clear.

---

## The anti-patterns `/learn` guards against

- **Aspirational language as research** — "AI should be dignified" is not a finding.
  A specific protocol for how dignity is operationalized in a deployed system is.
- **Confirmation intake** — material that only tells us what we already believe.
  Useful for morale. Not useful for growth.
- **Citation padding** — collecting sources to appear well-read.
  The research store is a working archive, not a bibliography.
- **Recency bias** — new is not better. A 2003 paper that's specific and tested
  outperforms a 2026 paper that's aspirational.

---

## Output format after evaluation

```
/learn result — [source title]

WHAT IT SAYS:
[2–4 sentences — the actual finding]

WHAT IT CHANGES:
[one sentence — specific]

CHALLENGER VERDICT: INTAKE / HOLD / PASS
REASON: [one sentence]

[IF INTAKE] Filed at: research/{topic-slug}/{filename}.md
```
