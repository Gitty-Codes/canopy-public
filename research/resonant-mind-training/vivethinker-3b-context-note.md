---
type: research-context
source: arXiv:2606.16140v1
filed: 2026-06-26
status: CONTEXT ONLY — not cited in pre-registration until RL reward model designed
---

# VibeThinker-3B — Research Context Note

**Citation:** "VibeThinker-3B: Exploring the Frontier of Verifiable Reasoning in
Small Language Models" — Xu et al., Alibaba/DAMO, 2026. arXiv:2606.16140v1

---

## What it shows

A 3B parameter model achieves near-frontier reasoning on verifiable tasks through
multi-stage post-training, challenging the assumption that reasoning scales linearly
with parameters.

**Key results:**
- AIME 2026: 94.3 (97.1 with test-time scaling)
- LiveCodeBench v6: 80.2 Pass@1
- IFEval (instruction following): 93.4 — reasoning gains did not hurt alignment
- GPQA-Diamond (knowledge-heavy): 70.2 — underperformed as expected

**Pipeline (five stages):**
1. Curriculum SFT with multi-path distillation
2. Multi-domain RL via MaxEnt-Guided Policy Optimization (math/code/STEM)
3. Long2Short efficiency optimization
4. Offline self-distillation
5. Instruction RL alignment

---

## What transfers to Resonant Mind work

**Reasoning-Knowledge Decoupling Paradigm:**
Compact models can excel at structured reasoning while lacking broad world knowledge.
This is architectural support for the orchestra hypothesis: SLMs hold reasoning +
constitutional orientation; larger models or retrieval supply domain knowledge.
Neither alone is sufficient; the handoff is the test.

**MaxEnt-Guided Policy Optimization:**
Rewards entropy alongside correctness — the policy explores multiple reasoning paths
before converging. This is structurally a doubt-encourager: the model is incentivized
to not take the first answer. Candidate mechanism for:
- Track B (active edge-seeking) — if uncertainty can be made behaviorally generative
- A future Resonant Mind RL stage (Experiment B extension or C)

**Validates Qwen2.5-7B target:**
If 3B achieves this, 7B has room for the behaviors we need. The parameter budget
is sufficient; the question is training signal design, not scale.

---

## What does NOT transfer

**The reward signal.** VibeThinker uses verifiable rewards: math answers are right
or wrong; code either runs or doesn't. Resonant Mind targets — genuine curiosity,
relational attention, calibrated uncertainty, typed DISSENT — have no equivalent
automated verifiability. An RL stage for the Resonant Mind requires:
- A reward model trained from human blind panel ratings
- An inter-rater reliability protocol (Cohen's kappa, pre-established rubric)
- Anti-gaming design (what prevents the model from producing superficially resonant outputs without the underlying orientation?)

Until that reward model design document exists, RL stays out of pre-registration.

---

## Status

- **Filed as:** research context for Resonant Mind training decisions
- **Do NOT cite in pre-registration** until reward model specification is written
- **Revisit for:** Experiment B RL stage design, Track B (active edge-seeking) mechanism
- **Council decision:** Entry 011 — DISSENT-FACTUAL resolved by filing as context only
