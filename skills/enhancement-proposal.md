---
name: enhancement-proposal
type: playbook
scope: meta
invocation: on-demand
description: Standard format for Canopy self-improvement proposals — what to build, why, and how to decide
---

# Enhancement Proposal — Standard Format

Every enhancement proposal uses this format. The format makes the consideration step
fast and the incorporation step unambiguous. Short is better than complete.

---

## [PROPOSAL-XXX] — {one-line title}

**Deficiency addressed:** link to the pattern in semantic memory or recurring gap report
*(e.g., "open_tension appearing 3x since May 2026 — council finishes sessions with unresolved questions")*

**What this enhancement does:**
One paragraph. Specific capability added or gap closed. No hedging.

**What it does NOT do (scope boundary):**
One sentence. What is explicitly out of scope. Prevents scope creep at review time.

**Build cost:**
- Estimated hours: X
- Files touched: list them
- Architectural risk: LOW / MEDIUM / HIGH
- Reversible: yes / no

**Constitutional check:**
Does this proposal conflict with any Constitutional principle?
If yes: name the conflict and justify the exception (highest bar).
If no: CLEAR — state which principle it serves.

**Proposed by:** {voice that surfaced the deficiency} via {session id or kaizen cycle date}

**Status:** PENDING / APPROVED / BUILDING / RESOLVED

---

## How proposals enter the system

1. Kaizen cycle surfaces recurring deficiency signal (2+ occurrences)
2. Listener + Inventor session produces a proposal using this format
3. Proposal saved to `proposals/{PROPOSAL-XXX}.md`
4. Surfaced to founder at next session open (quiet inbox — not an alarm)
5. Founder approves / modifies / defers
6. Builder builds
7. Deficiency signals marked `resolved: true` with link to proposal
8. Next kaizen cycle reads resolved signals as growth record

## What makes a good proposal

- Names one thing. Not three things dressed as one.
- Has a scope boundary. "Does X but not Y" is better than "Does X (and maybe Y later)."
- Passes the Constitutional check. If it doesn't, it doesn't go forward without
  founder deliberation at the highest bar.
- Is reversible if possible. Reversible over permanent — the burden of proof is
  on the irreversible decision.

## What does NOT belong in a proposal

- Speculative enhancements without a deficiency signal driving them
- Architecture changes that touch the Constitutional substrate without council review
- Anything that removes the founder's governance role at the commissioning step
