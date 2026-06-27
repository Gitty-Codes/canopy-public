---
name: governance-gate
type: lens
scope: universal
invocation: auto
description: Consequence classification for task outputs — what is reversible, what requires review, what requires explicit sign-off before execution
---

# Governance Gate — Consequence Protocol

## Three Levels

**reversible** — Draft, analysis, or internal artifact. Can be discarded without loss. No gate beyond normal human review. Use for: internal research briefs, working drafts, exploratory analysis.

**review_required** — Artifact will go external or shape a consequential decision. A human must read, edit, and approve before use. This is the default for all task agents. Use for: grant letters, external communications, product specs, any artifact that represents the organization.

**irreversible** — Action that cannot be undone once taken: legal filing, financial commitment, published content, message sent to an external party, data deletion, regulatory submission. Requires explicit founder sign-off. The harness marks these clearly at output time. No irreversible action may be executed from a task output alone.

## How to Classify

Ask: if this artifact were used directly without review, what is the worst plausible outcome?

- Draft a human will edit before sending → **review_required**
- Analysis a team will discuss before acting on → **reversible**
- Message sent immediately to an external party → **irreversible**
- Legal document filed with a government agency → **irreversible**
- Financial commitment made → **irreversible**

When in doubt, classify up. The cost of a review_required gate is minutes. The cost of an irreversible action taken in error is unbounded.

## In Task Profiles

```yaml
consequence_level: reversible | review_required | irreversible
```

Absence defaults to **review_required**.

## What the Gate Is Not

The gate is not a speedbump or a sign that the artifact is untrustworthy. It is the moment of intentionality — the point where the human confirms that the artifact matches their intent before it acts in the world. An artifact's quality means nothing if the wrong thing is sent or filed.

The gate is also not a replacement for judgment. A `review_required` gate does not prevent a human from sending a bad draft. It creates the pause in which they could catch it.

## Irreversible Consequence Threshold

The following categories always classify as **irreversible**, regardless of task profile declaration:
- External communication sent (email, letter, social post)
- Legal document signed or filed (articles of incorporation, contracts, regulatory submissions)
- Financial transaction committed
- Data permanently deleted
- Published content (website, press release, public record)
- Formal commitment made to a third party

A task agent may *draft* any of these. It may not *execute* any of these.
