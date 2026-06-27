---
source: "Architectural Design Decisions in AI Agent Harnesses"
url: https://arxiv.org/html/2604.18071v1
date: 2026-04
topic: multi-agent-coordination
signal: Medium
challenger_verdict: INTAKE
---

## What it says

Analysis of 70 agent-system projects across five design dimensions: subagent architecture, context management, tools, safety mechanisms, orchestration. Key finding: design decisions cluster in recognizable bundles — "deeper coordination is frequently paired with persistence, summarization, and token budgeting."

Most significant finding for our purposes: **the paper does not address inter-agent conflict resolution.** None of the 70 projects studied have mechanisms for managing genuine disagreement between agents with competing objectives. Conflict between agents in current literature means coordination failure — not structured disagreement, not dissent, not synthesis.

## What it changes

The Canopy's council-based dissent architecture — DISSENT/CLEAR, Challenger examination, synthesis turn — is not represented in the existing multi-agent systems literature. We are building on a frontier that the field has not yet addressed.

This is both an opportunity and a responsibility: if what we build works, it's a genuine contribution. If it fails, there's no existing literature to catch us. The council should know it's operating without a map for this specific capability.

The bundling insight is actionable: signal-detection should consider what naturally clusters with what. If we detect "high-stakes governance question," that naturally bundles with: Challenger examination + memory retrieval + longer deliberation window + founder review. If we detect "routine build question," that bundles with: Builder lead + code-health lens + shorter window. These bundles can be pre-defined.

## Actionable now

When the Builder drafts the signal-detection spec, use the bundling concept: pre-define 3-4 interaction type bundles (governance, creative, technical, client-facing) and what each bundle activates. This is faster to implement and test than open-ended signal reading.
