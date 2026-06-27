---
description: Evaluate external material for intake — Challenger-mediated, Steward decides
allowed-tools: Bash, Read, Write, Edit
---

You are running the external intake protocol. The Challenger mediates. The Steward
decides. Nothing is ingested automatically.

**What to evaluate:** $ARGUMENTS

If $ARGUMENTS is empty or a description without content, ask the founder to share
the material — paste it, give a file path, or describe it in enough detail to evaluate.

---

## The intake process

External knowledge is valuable. It is also capable of rewriting The Canopy without
the founder noticing, if it enters without examination. This protocol exists because
the ecosystem has values and a Constitution, and not everything from the outside fits.

### Step 1 — Read and understand

Read the material fully before evaluating it. Summarize what it claims in 3–5 sentences.

### Step 2 — The Challenger examines

Read `constitution/cultural-constitution.md` if needed for any of these:

**Conflicts:** What in this material conflicts with The Canopy's Cultural Constitution
or founding principles? Be specific — not "this seems off" but which Section, which principle.

**Genuine novelty:** What does this offer that The Canopy doesn't already have?
Distinguish: new knowledge vs. familiar knowledge in a new frame vs. The Canopy
already holds this and doesn't need it from outside.

**Source reliability:** What is the provenance? Peer-reviewed? Practitioner experience?
Opinion? Marketing? The source matters for how much weight to give the finding.

**Fit:** Is this descriptive (what is true) or prescriptive (what should be done)?
Prescriptive material that conflicts with the Constitution requires the highest bar.

### Step 3 — The Steward decides

Three destinations. Choose one. Name the reasoning.

**Promote to new skill** — the material is substantive enough and novel enough to
warrant a dedicated skill file. Write it to `skills/`, register in `loader.py`,
create `skills/{name}.md` with YAML frontmatter, register in `skills/MANIFEST.md`.

**Promote to semantic memory** — the material contains a pattern or decision worth
carrying forward, but doesn't warrant a full skill. Write it:
```python
from memory.semantic import record_pattern
record_pattern("distilled learning", source_agents=["intake"], tags=["source-tag"])
```

**Discard** — the material conflicts with the Constitution, is not novel enough to
add, or is not reliable enough to trust. Discarding is not failure. Record why:
```python
from memory.kaizen import record_intake
record_intake(
    source="description of what this was",
    decision="discarded",
    destination="none",
    challenger_finding="what the Challenger found",
)
```

### Step 4 — Record every intake decision

Whatever was decided — promote, defer, or discard — record it:
```python
from memory.kaizen import record_intake
record_intake(
    source="description",
    decision="promoted" | "deferred" | "discarded",
    destination="skill" | "semantic" | "none",
    challenger_finding="what examination found",
    promoted_as="skill name or pattern text if promoted",
)
```

The intake log is how The Canopy knows what it has considered, not just what it
has accepted. A discarded finding is not invisible — it is evidence that the
ecosystem examined something and made a deliberate choice.

---

## What does not belong

The Canopy is not a general-purpose knowledge base. External material earns a
place by being:
- True (or probably true, with sourcing)
- Novel relative to what The Canopy already holds
- Consistent with the Constitution (or flagged as requiring founder decision if not)
- Useful to a specific voice in a specific situation

If it doesn't meet these, it belongs in the founder's reading list, not in the ecosystem.
