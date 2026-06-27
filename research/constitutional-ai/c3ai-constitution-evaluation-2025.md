# C3AI: Crafting and Evaluating Constitutions for Constitutional AI
*Filed: 2026-06-07 | Source: arxiv 2502.15861 / ACM WWW 2025 | Signal: Medium-High*

## Why this matters to the Canopy
Treats the constitution as something that can be interrogated, refined, and tested
against empirical behavior — a rigorous framework for what the Canopy's interrogation
obligation in Section VII aspires to.

## Key findings
- Systematic methodology for both constructing constitutions and evaluating whether
  fine-tuned models actually follow them — constitution as testable artifact
- Graph-based principle selection allows iterative refinement of existing constitutions
- Key empirical finding: fine-tuned CAI models adhere well to negatively-framed
  principles ("don't do X") but struggle with positively-framed ones ("do Y"),
  while human preference goes the other direction
- Gap between what humans want constitutions to say and what models can actually
  internalize — a concrete amendment problem

## What it changes or validates
- **Validates:** the Canopy's interrogation obligation (Section VII) — periodic
  examination of what the Constitution has made invisible is the right posture;
  this paper shows how to make it rigorous
- **Framing insight for Resonant Mind:** principle framing (positive vs. negative,
  behavior-based vs. trait-based) measurably affects whether a model internalizes
  it. When writing training prompts or fine-tuning objectives, framing is not
  cosmetic — it is architectural
- **Distinction worth preserving:** principle selection (what goes in) vs.
  constitution evaluation (whether it's working) — two-phase structure the Canopy
  should adopt for its own amendment process
- **Caveat:** RLHF/fine-tuning centric; principle-framing findings transfer to
  prompt-based agents; graph-selection algorithm does not directly
