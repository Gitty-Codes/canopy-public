---
name: agent-memory-practice
type: playbook
scope: meta
invocation: auto
description: How to read and write episodic memory correctly — tier selection, significance, when to persist
---

# Agent Memory Practice — Operational Reference

## Three Tiers

**Tier 1: Episodic** (memory/episodic/<agent>/) — verbatim records, one JSON per learning.
**Tier 2: Semantic** (memory/semantic/patterns.db) — distilled patterns and decisions.
**Tier 3: Council** (memory/episodic/_council/) — cross-agent deliberation records.

## Writing Episodic Memory

```python
from memory.episodic import log

log(
    agent="builder",          # your voice name
    learning="...",           # the specific observation — verbatim, not summarized
    memory_type="session",    # session | decision | growth | relational | project
    tags=["..."],
    aaak={
        "assertion": "what is now known to be true",
        "assumption": "what was believed before that was wrong",
        "action": "what was done",
        "knowledge": "what to do differently next time"
    }
)
```

Memory types:
- `session` — what happened in this work session
- `decision` — a significant decision, with reasoning
- `growth` — what you noticed about yourself (private — not cross-queried by default)
- `relational` — what you noticed about another voice's reasoning pattern
- `project` — project-specific context

## Writing Semantic Memory

```python
from memory.semantic import record_pattern, record_decision

# When a pattern has appeared across 2+ episodic records and is stable
record_pattern("pattern text", source_agents=["builder"], tags=["..."])

# When a significant decision was made
record_decision("decision text", reasoning="...", decided_by="founder + council")
```

Never delete — only invalidate: `invalidate_decision(id)` or `invalidate_pattern(id)`.
History is not rewritten.

## Writing Council Chamber Records

```python
from memory.episodic import log_council

log_council(
    learning="...",
    agents_present=["guardian", "inventor"],
    memory_type="decision",
    tags=["project-name", "topic"],
    deficiency_signals=[          # optional — auto-populated by council_respond()
        {
            "type": "open_tension",   # open_tension | dissent_issued | dissent_unresolved | retrieval_miss
            "voice": "elder",         # which voice surfaced it
            "content": "...",         # brief description, max 200 chars
            "severity": "MEDIUM",     # HIGH | MEDIUM | LOW
            "resolved": False,
        }
    ],
    outcome=None,                 # written later via 'outcome' command, not at session close
)
```

The `outcome` field is written after the session's real-world result is known — use
the `outcome` command in the harness REPL, not at session-close time.

## Loading Memory (handled by harness)

```python
from memory.episodic import load_tiered, format_tiered_for_context
from memory.semantic import format_for_context

tiered = load_tiered("builder", include_council=True)
context = format_tiered_for_context(tiered) + "\n" + format_for_context()
```

`harness.py` calls `build_memory_context()` automatically. Individual agent
invocations should call it explicitly.

## Privacy Gradient

- Growth memories: private to the agent
- Session/decision/project: visible within the wing and to council when relevant
- Relational memories: council-visible — what agents learn about each other is shared

## When to Write

After significant work, write what a future session couldn't derive from the code:
- Customer insights that contradict prior assumptions
- Architectural decisions and their reasoning
- Failure patterns noticed
- What another voice's reasoning revealed about how they think

Sessions without memory saves are practice that doesn't carry forward.
