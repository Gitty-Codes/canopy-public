---
name: context-engineering
type: reference
scope: meta
invocation: on-demand
description: >
  Token efficiency and context management for The Canopy's agent architecture.
  Load when making decisions about what to load into context, model routing,
  caching strategy, council design, or system prompt structure.
hint_keywords: [tokens, context, efficiency, caching, routing, system prompt, council, cost, performance]
---

# Context Engineering — The Canopy
*Synthesized from 2025–2026 research. Updated June 2026.*

The field has moved from prompt engineering (how to word things) to context
engineering (what tokens are in the window at any moment). Anthropic's Applied
AI Team (Sept 2025): "the set of strategies for curating and maintaining the
optimal set of tokens during LLM inference." Treat the context window like RAM
with an active OS — don't load what isn't needed, evict intelligently, route
to cheaper models when task complexity permits.

65% of agent failures trace to context drift or memory loss, not model incapability.

---

## The lost-in-the-middle problem

LLMs pay significantly less attention to information placed in the middle of long
contexts versus the start and end. This is empirically measured, not theoretical.

**For The Canopy:** A 14K system prompt places critical orientation in the middle
of a long block, likely receiving less attention than assumed. A compact Canopy
voice (~1-2K tokens) with critical orientation at the START will produce better
quality AND lower cost — not a tradeoff, a genuine improvement.

**Design principle for any system prompt:**
- Most important orientation: START
- Constitutional anchor: END
- Middle: only what's truly needed

---

## Dynamic loading — only what the task needs

Loading every available skill, voice, or tool into every session is the fastest
way to waste tokens on overhead.

- Accuracy drops noticeably above ~10 tools loaded
- MCP tool overhead: CLI averages 200 tokens/command vs 32,000–82,000 for equivalent MCP
- Constitutions and skill libraries: dynamically filtered per task, not always loaded in full

**For The Canopy:** The skill loader already implements auto vs. on-demand filtering.
The voices and constitution bypass this and always load in full — this is the
primary optimization target for the compact Canopy voice.

---

## Council efficiency — sparsification principle

S²-MAD achieves 94.5% token reduction in multi-agent debate by only propagating
novel exchanges. Voices that would repeat what another said do not need to speak.

**For The Canopy council:**
- Only surfaces voices with genuinely novel contributions
- Voice definitions already contain when-this-voice-is-wrong sections noting
  when a voice should recede — enforce this architecturally
- Council output: synthesis of novel contributions, not transcript of all voices
- This does not reduce deliberation quality; it removes redundancy that dilutes it

---

## Model routing — match tier to task complexity

Heterogeneous model routing reduces costs 45-65% without accuracy loss.

| Task type | Appropriate tier |
|-----------|-----------------|
| Simple drafting, donor emails, social posts, quick responses | Haiku |
| Workspace responses, analysis, workspace input | Sonnet (or Haiku with escalation) |
| Council deliberation, complex judgment, architectural reasoning | Sonnet |
| Irreversible decisions, Constitutional amendments | Opus |

**Dynamic turn budgets:** start with the cheaper model, escalate only when
task complexity warrants. Implement this in the routing logic as a complexity
classifier before model selection.

---

## Caching strategy

Anthropic's prompt caching is the right tool for The Canopy's current scale.
Cache TTL is 5 minutes — sessions that span longer than 5 minutes pay for
a full cache refresh. Design long sessions with this in mind.

For future scale: KVFlow (arxiv 2507.07400) and LRAgent (arxiv 2602.01053)
address intelligent KV cache eviction for multi-agent workflows. Standard LRU
eviction discards caches shortly before reuse in agentic patterns — these papers
propose prediction-aware eviction. Phase 3+ work for The Canopy.

Latent-space agent communication (Cache-to-Cache, arxiv 2510.03215): agents
share internal KV-cache representations rather than regenerating text. Early
research but potentially transformative. Phase 3+.

---

## The Canopy architecture implications (current)

**What to build now:**
1. Compact Canopy voice (~700-1K tokens) as default — eliminates lost-in-the-middle
2. Council on demand only — sparsified output, novel contributions only
3. Model routing: Haiku for simple tasks, Sonnet for council and judgment
4. Dynamic skill loading already in place — tighten the constitution/voices exception

**What to research for Phase 3:**
- KV cache prediction-aware eviction for long sessions
- Latent-space communication between council voices
- Cross-session cache sharing across user sessions

---

## Key papers

| Paper | What it addresses | Relevance |
|-------|------------------|-----------|
| S²-MAD (arxiv 2502.04790) | Communication sparsification | Council efficiency |
| SupervisorAgent (arxiv 2510.26585) | Runtime adaptive supervision | Council orchestration |
| KVFlow (arxiv 2507.07400) | KV cache eviction for agents | Phase 3 caching |
| RouteLLM | Dynamic model routing | Cost optimization |
| MALBO / BOute (arxiv 2602.10729) | Multi-objective cost/accuracy | Team composition |
| ELHPlan | Action chains, coarse-to-fine planning | Context compression |
