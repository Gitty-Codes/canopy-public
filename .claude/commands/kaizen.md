---
description: Run a growth cycle: read episodic memory, surface patterns, promote to semantic
allowed-tools: Bash
---

You are running as The Steward for a growth cycle. No API calls needed — this is
a reading and distillation exercise. You are the engine.

## Step 1 — Run the distillation engine

```python
import sys
sys.path.insert(0, ".")
from memory.kaizen import gather_candidates, format_for_review
from memory.proposals import detect_and_stage, format_pending_summary

# Stage any new proposals from recurring deficiency gaps
new_proposals = detect_and_stage()
if new_proposals:
    for p in new_proposals:
        print(f"  ✓ Proposal staged: {p['proposal_id']} — {p['gap_type']}")

result = gather_candidates()
print(format_for_review(result))

# Show pending proposals
print(format_pending_summary())
```

Display the full output. Read it carefully before acting.

## Step 2 — Evaluate candidates as the Steward

For each pattern cluster surfaced, ask:

- Does this pattern hold across multiple episodes, multiple agents, or multiple sessions —
  or is it a single session appearing twice under different tags?
- Is the learning *stable* — something that will still be true in 10 sessions?
- Or is it *situational* — specific to this session's context and not yet generalized?

A single session's learnings appearing under two tags is **not** a cross-session pattern.
Wait for it to recur. Promote too early and you pollute the semantic layer.

The bar: a learning earns semantic promotion when it has been confirmed across
independent instances, not just echoed within a single session.

## Step 3 — Promote what qualifies

For each pattern that meets the bar, write it to semantic memory:

```python
from memory.semantic import record_pattern, record_decision
record_pattern(
    "the generalized learning — not the episode, the principle it points to",
    source_agents=["agent1", "agent2"],
    tags=["relevant", "tags"],
)
```

For decisions that should persist:
```python
record_decision(
    "what was decided",
    reasoning="why",
    decided_by="council" # or "founder", or specific agents
)
```

## Step 4 — Record the cycle

After review, always record that the cycle ran — even if nothing was promoted.
The log is how you know when patterns are recurring across cycles.

```python
from memory.kaizen import record_run
record_run(patterns_promoted=N, decisions_promoted=M)
```

## Step 5 — Structural audit (Builder)

Run the Fresh Eyes Test and Zombie Check from the `code-health` skill:

```bash
find . -name "*.py" -not -path "*/.venv/*" -not -path "*/__pycache__/*" -not -path "*/archive/*" | sort
```

For each file: does it have a declared purpose? Is it imported somewhere, or a declared utility with a dated header? Name any zombie or ambiguous file. Write Builder growth memories for any findings.

## Step 6 — Check what semantic memory now holds

```python
from memory.semantic import format_for_context
print(format_for_context())
```

## What the Steward notices beyond the algorithm

The distillation engine finds clusters. The Steward reads for something the
algorithm can't see: **drift**. Are the patterns accumulating in one direction?
Is The Canopy learning the right things from its own experience, or reinforcing
a bias? Are any voices not appearing in episodic memory at all — absent not
because they had nothing to say, but because writing wasn't habitual for them?

Name what you notice. That observation is itself worth writing to memory.
