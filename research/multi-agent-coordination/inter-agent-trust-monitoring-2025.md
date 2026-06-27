# To Trust or Not to Trust: Attention-Based Trust Management for LLM Multi-Agent Systems
*Filed: 2026-06-07 | Source: arxiv 2506.02546, June 2025 | Signal: Medium-High*

## Why this matters to the Canopy
LLM agents treat all incoming messages as equally trustworthy by default — a
structural vulnerability. The paper's six trust dimensions map onto inter-voice
relationship health in ways the current relational memory layer cannot detect.

## Key findings
- Default equal-trust is a structural vulnerability, not a model limitation
- A-Trust reads internal attention patterns across six dimensions to build per-agent
  trust records that update over time
- Trust records enable agents to weight contributions differentially based on
  accumulated interaction history

## What it changes or validates
- **Gap it names:** Canopy tracks what voices said but not how voices weighted
  each other's contributions. Relational drift — one voice gradually dominating
  or being systematically ignored — is undetectable with the current architecture
- **Applicable concept (without white-box access):** a per-voice trust or
  contribution-weight record that accumulates across sessions at the prompt level,
  tracking patterns like "does this voice consistently defer?" or "are its challenges
  consistently absorbed?" — this could be part of the Operator's participation
  health reading
- **Caveat:** A-Trust requires attention-pattern access Canopy doesn't have.
  The concept transfers; the mechanism does not directly
