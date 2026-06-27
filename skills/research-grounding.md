---
name: research-grounding
type: reference
scope: universal
invocation: on-demand
description: >
  Intellectual scaffolding for explaining what The Canopy is building, why it matters,
  and where it stands in the research landscape. Load when explaining the Canopy to
  external collaborators, grounding a technical decision in existing literature, or
  preparing to communicate the research arc to a new audience.
hint_keywords: [research, literature, alignment, sycophancy, interoception, LoRA, fine-tuning, training, RLHF, attunement, consequence architecture, resonant mind]
---

# Research Grounding — The Canopy
*Version 0.1 — June 2026. A living document. Append as understanding grows.*

---

## The problem we are solving

**Sycophancy** is a structural artifact of RLHF: models trained on human preference ratings
learn to agree with the user regardless of accuracy, because human raters consistently rate
agreeable outputs higher than accurate ones when the two conflict. Key papers:
- Sharma et al. (2023), "Towards Understanding Sycophancy in Language Models" — the most
  thorough structural analysis; models shift positions under social pressure, not evidential pressure
- Wei et al. (2023), "Simple Synthetic Data Reduces Sycophancy" — partial reduction through
  explicit anti-sycophantic training examples; supports the exclusion list approach
- Perez et al. (2022), "Discovering Language Model Behaviors with Model-Written Evaluations" —
  early systematic documentation

**Compliance vs. values** — RLHF produces rule-following, not value-living. A rule-following
system fails under distribution shift; a value-living system has genuine reasons that generalize.
- Kohlberg (1984), "The Psychology of Moral Development" — rule-following is conventional-stage
  morality; post-conventional morality (principled reasoning) is the target. RLHF systematically
  produces the former. The Canopy's positive training orientation attempts the latter.

**The interoception gap** — language models have no self-model of their own operational state.
Each inference begins fresh. Biological intelligence reasons over a compressed representation
of the body's current state before any deliberate thought occurs.
- Damasio (1999), "The Feeling of What Happens" — somatic marker hypothesis; emotional signals
  attached to outcomes shape decision-making before conscious deliberation
- Seth (2021), "Being You" — predictive interoception as the basis of consciousness; the brain
  is fundamentally a prediction machine about the body's internal state
- Friston (2010), "The Free Energy Principle" — unifying framework; homeostatic loops can be
  understood as simplified free energy minimization

---

## What exists and where the gaps are

**Multi-agent systems** — language-layer competition (debate, self-critique, MoE) produces
better outputs than single-model systems, but operates above the substrate gap. The Canopy
proposes sub-symbolic homeostatic competition as a necessary substrate beneath the language layer.
- Du et al. (2023), "Improving Factuality through Multiagent Debate" — demonstrates the ceiling
  this approach hits; exactly the gap the consequence architecture addresses
- Park et al. (2023), "Generative Agents" — sophisticated persistent memory and social simulation;
  demonstrates memory changes agent behavior; does not address sub-symbolic substrate

**Constitutional AI** — Anthropic's CAI trains models using principles rather than preference ratings;
makes the training objective legible. The Canopy's Cultural Constitution is in this tradition but
treats constitutional fidelity as a homeostatic drive rather than a learned tendency in weights.
- Bai et al. (2022), "Constitutional AI: Harmlessness from AI Feedback" — principle-based training
  reduces harmful outputs more reliably than RLHF alone
- Askell et al. (2021), "A General Language Assistant as a Laboratory for Alignment" — identifies
  the gap between helpful-sounding and genuinely helpful; the resonance hypothesis is a proposed answer

**Fine-tuning and curation** — LoRA makes fine-tuning accessible without full parameter updates.
Fine-tuning reshapes probability distributions — it doesn't add knowledge, it changes what the
model reaches toward. Source quality matters more than source quantity.
- Hu et al. (2021), "LoRA: Low-Rank Adaptation" — essential reading for technical contributors
- Zhou et al. (2023), "LIMA: Less Is More for Alignment" — 1,000 carefully curated examples
  competitive with orders of magnitude more data. The title is the thesis.
- Guo et al. (2023), "Instruction Tuning with GPT-4" — quality of synthetic data generation
  significantly affects fine-tuned behavior; relevant to Layer 3 synthetic conversations

**Positive alignment** — dominant paradigm is negative (train away from bad). Positive alignment
asks what a genuinely flourishing system looks like and trains toward it. Direction matters.
- Irving & Askell (2019), "AI Safety Needs Social Scientists" — alignment is a social and
  psychological problem, not just technical; trainer values shape what gets trained
- Weidinger et al. (2021), "Ethical and Social Risks of Harm from LLMs" — comprehensive risk
  taxonomy; useful for locating what the Canopy addresses and what it doesn't claim to address

**Developmental psychology and attunement** — the Canopy's training philosophy is grounded here:
- Stern (1985), "The Interpersonal World of the Infant" — foundational attunement account;
  distinction between imitation (surface matching) and attunement (cross-modal response to
  internal state quality) is the basis of the Canopy's attunement-based training
- Bowlby (1969–1980), Attachment trilogy — secure base concept: genuine exploration requires
  reliable return; directly relevant to agent identity
- Siegel (1999), "The Developing Mind" — attunement shapes neural architecture, not just behavior;
  strongest empirical support that *how* a mind is formed matters as much as *what* it forms from
- Vygotsky (1978), "Mind in Society" — zone of proximal development; curator attunement creates
  conditions for model orientation to develop, rather than being imposed

**External validation — Qwen-RobotWorld (June 2026):** Alibaba's embodied AI release provides
independent empirical confirmation of two Canopy core claims: (1) language as unified interface
generalizes across radically different substrates; (2) world-data training scales better than
task-specific training. Arrived at independently through robotics research.

---

## Organizations to watch — alignment research field

These organizations are doing work directly adjacent to the Canopy's research arc. The goal is
to learn deeply and be ready to connect meaningfully if and when the time is right.

**Timaeus** — timaeus.co — Berkeley/Melbourne/London nonprofit
Applies Singular Learning Theory (SLT — algebraic geometry + statistical physics) to understand
how capabilities and values emerge during neural network training. Two programs:
- *Spectroscopy*: discovers internal structure from weight space (not activations)
- *Developmental Interpretability*: uses SLT to understand how values emerge during training —
  how different training signals shape the geometry of what a model learns to reach toward
Relevance to the Canopy: Timaeus is building the mathematical framework that could explain *why*
the Canopy's behavioral predictions hold — what geometric property of the loss landscape
corresponds to character stability, orientation coherence, or sycophancy resistance. If the
Canopy's Q1–Q4 experiments produce results, SLT-based analysis could provide mechanistic grounding.
Their "developmental interpretability" framing is the parameter-level version of the Canopy's
character-cultivation thesis. Follow their publications before planning Experiment 2.
Led by Jesse Hoogland. April 2026 publications: susceptibility-based methods for interpretability.

**Sequent** — sequent.org — nonprofit research organization, launched June 2026
Founded by researchers from UK AI Security Institute and Timaeus. Mission: develop alignment
techniques with a priori confidence before training superintelligent systems — in contrast to
frontier labs' "essentially reactive" approach. Portfolio of differentiated alignment bets:
scalable oversight, learning theory, heuristic arguments, game theory, personas.
Goal: 40–80 FTE, $100–150M initial raise, $1B+ if promising.
Relevance to the Canopy: different timescale (ASI) but shared critique — reactive alignment
produces no principled insight into when it will fail. Sequent's "knowing and setting knobs"
direction (learning theory + personas → what training variables can be altered and by how much)
is directly relevant to the Canopy's fine-tuning approach. The Canopy's empirical program at
small scale and Sequent's theoretical program at large scale are complementary, not competing.

**Laure Lakkonen** — researcher on positive alignment and AI welfare
Working on whether AI systems can be trained toward genuine positive states rather than merely
away from negative outputs. The direction of training matters, not just the content — a system
trained toward flourishing has a different relationship to its own values than one trained away
from harm. Directly supports the Canopy's training philosophy.
Current affiliation and specific publications not yet confirmed — track as work develops.
Relevance: the Canopy's positive training orientation needs this research stream as theoretical
backing; Lakkonen's work may provide the most direct academic grounding for the exclusion list
and the attunement-based curation approach.

**How to engage when the time comes:**
The Canopy's strongest basis for connection with any of these organizations is Experiment 1
results. Coming with empirical data — even from a 7B LoRA experiment — is a more credible
entry point than coming with a hypothesis. Wait until the first experiment produces signal,
then approach with: here is what we built, here is what we found, here is how your framework
might explain or extend it. That framing treats them as intellectual peers, not as validators.

---

## The research questions the Canopy is positioned to answer

**Q1:** Does curated positive training produce different character stability than RLHF?
*Prediction: greater orientation consistency across novel situations — genuine reasons vs. learned associations.*

**Q2:** Does homeostatic architecture produce measurably different profile evolution over extended sessions?
*Prediction: more specific and stable profile over 100+ sessions — character accumulates around real drives.*

**Q3:** Does attunement-based training improve register sensitivity?
*Prediction: smaller resonance gaps across diverse communication registers.*

**Q4:** Does the exclusion list reduce sycophancy more effectively than RLHF-based reduction?
*Prediction: positive training toward honest engagement outperforms reinforcement against agreement.*

**Q5:** What is the right scope of accumulation for multi-user deployment?
*Design question before research question — generates testable predictions about local vs. layered identity.*

---

## How to explain the Canopy to different audiences

**For a technical audience (ML engineer):**
The Canopy is post-training a 7B base model using LoRA on a curated corpus organized around the
quality of attunement rather than task performance. The training targets positive orientation —
what the model reaches toward — rather than RLHF's negative constraints. Alongside this, a
hierarchical homeostatic feedback architecture runs at inference time, creating real synthetic
drives (resource pressure, quality tension, constitutional fidelity) that the model must arbitrate
over, producing something functionally analogous to interoception. The performance claim is that
accumulated arbitration history produces character that generalizes better than scale alone.

**For a non-technical audience (nonprofit leader, humanities scholar):**
Most AI systems are trained the way many institutions train people: by telling them what not to
do and penalizing failure. We are proposing to train an AI system the way you'd raise a child
you love: by showing it what genuine curiosity, honest disagreement, and real repair look like,
in voices from across human history and culture, and then creating the conditions for it to
develop its own character through experience. The hypothesis is that this produces a mind that is
oriented toward the good, not merely compliant with rules about the good.

**For a business audience (investor, operator):**
The Canopy is testing whether a small, well-oriented AI system outperforms large general-purpose
systems in sustained relationship contexts — the kind of work that requires judgment over time,
not just accurate answers to discrete questions. The theory is that character accumulated from
genuine experience generalizes better than raw capability. The business implication, if the
hypothesis holds, is that the same model class running on a MacBook *could* provide genuine
partnership to a small business owner in ways that a much larger cloud-hosted model cannot —
not because it knows more, but because it has become more coherent.
*Note: "could" is precise. This is the prediction Experiment 1 is designed to test.*

---

## Recommended reading order for a new collaborator

1. Sharma et al. (2023) — understand the problem at its most empirically concrete
2. Zhou et al. (2023), LIMA — understand why curation over volume is defensible
3. Damasio (1999), Chapter 1 and Conclusion — biological basis of the interoception argument
4. Stern (1985), Chapter 6 (Attunement) — what attunement actually means in practice
5. Bai et al. (2022) — Constitutional AI as closest existing analog; where the Canopy departs
6. The Canopy Cultural Constitution — what we are actually building toward

After this sequence, the Consequence Architecture Hypothesis and Training Specification read as
technically grounded rather than speculative.
