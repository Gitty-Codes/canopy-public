---
type: research-brief
topic: epistemic-curiosity
prepared: 2026-06-23
updated: 2026-06-26
status: FOR COUNCIL EVALUATION
council-session: Entry 011 (Track A and Track B opened)
---

# Epistemic Curiosity as a First-Class Training Objective
*A Brief for the Canopy Council*

---

## Preamble

There is a structural tension at the heart of every large language model currently
in production: the models are trained to answer, not to wonder. Every gradient update
across billions of training steps has optimized for confident output. Abstention,
hedging, and the acknowledgment of ignorance are systematically penalized by standard
accuracy metrics. The result is a class of systems that will hallucinate fluently
rather than pause at the edge of what they know.

This brief argues that the problem is not cosmetic — it cannot be solved by better
prompts or stronger guardrails bolted on after training. The confidence is baked
into the weights. Doubt has been trained away.

What we lack, and what this brief proposes as a design target for the Canopy, is
**epistemic curiosity** — the drive to seek the boundaries of understanding rather
than fill in the gaps with plausible-sounding confabulation. In a human, doubt is
what motivates verification, connection-seeking, and deeper inquiry. A model without
a functional analog to doubt is a model that fails quietly at exactly the moments
that matter most: at the edges of its knowledge, under adversarial pressure, and
when facing genuinely novel problems.

Two questions structure this brief:
1. **The training question:** What would it mean to make epistemic curiosity a
   first-class training objective — and what does current research tell us about
   how to get there?
2. **The architecture question:** While we do not yet have a model trained this way,
   what can we learn from research on personas, prompting, and system design to build
   epistemic curiosity into the Canopy's current operating architecture?

A third question emerges from the research: **how do we detect the knowledge boundary
in real time**, so the system knows when to route, escalate, or pause?

---

## Part I — The Training Problem

### 1.1 Why Confidence Is the Default — and Why That's a Design Failure

The source of overconfidence is not mysterious. Standard next-token prediction
training, combined with accuracy-focused evaluation benchmarks, creates selection
pressure specifically against epistemic humility. A model that correctly says
"I don't know" on 20% of questions — while being right 95% of the time on the
rest — will score lower on standard accuracy metrics than a model that guesses on
everything and hits 80%. The incentive structure actively punishes calibrated
uncertainty.

RLHF and RLVR compound this. RLVR-trained models perform worse at abstention
than their base counterparts — even when those models can recognize uncertainty in
their own reasoning chains. They have learned to override their own epistemic signals.

**Key finding:** Models possess the latent capability to abstain. What they lack is
the trained decision to act on that uncertainty. This is a behavioral gap created
by incentive misalignment, not a capability gap.

*Sources:* Mohamadi et al. (2025) arXiv:2511.11500 · Zylos Research (2026)

### 1.2 The Four-Quadrant Knowledge Topology

| Category | Description | Canopy relevance |
|---|---|---|
| Prompt-agnostic known | Accessible regardless of how you ask | Not the problem |
| Prompt-sensitive known | Present in model, requires right framing to surface | Track A target: the model should know where it sits on this map |
| Model-specific unknown | Known to humans, not this model | Routing/retrieval trigger |
| Model-agnostic unknown | Unknown to both humans and model | The unknown-unknown zone — see 1.5 |

**What the map reveals:** A model that cannot locate itself on this topology will
confuse prompt-sensitive known knowledge (accessible with better framing) with
genuine gaps (requiring retrieval or escalation). Epistemic curiosity is, in part,
the capacity to navigate this map accurately in real time.

*Sources:* Li et al. (2024) arXiv:2412.12472 · PromptLayer Research (2024)

### 1.3 Reinforced Hesitation — The Structural Training Solution

The most promising training-level intervention: modify the reward structure from
binary to ternary.

| Outcome | Binary reward | Ternary (RH) |
|---|---|---|
| Correct answer | +1 | +1 |
| Wrong answer | −λ | −λ |
| Abstention | (not permitted) | 0 |

By making abstention a valued outcome rather than a failure mode, RH produces models
along a Pareto frontier — varying λ yields distinct models optimized for different
risk tolerances. Crucially, trained abstention becomes a **coordination signal**: when
a model hesitates, downstream systems can route to a stronger model, trigger retrieval,
or escalate to human review.

Preliminary results on GSM8K, MedQA, and GPQA show self-cascading (re-querying the
same model on abstention) outperforms majority voting at lower computational cost.

**Implication for Resonant Mind:** RH-style ternary rewards should be considered for
the Experiment B pipeline — or at minimum for Experiment B RL stage design. The
abstention signal is not a concession; it is infrastructure.

*Sources:* Mohamadi et al. (2025) arXiv:2511.11500 · I-CALM arXiv:2604.03904

### 1.4 Boundary-Aware Fine-Tuning (US-Tuning)

US-Tuning: two-stage approach. Stage 1 enhances the model's ability to recognize
its knowledge boundaries. Stage 2 reinforces instruction adherence through causal
prompts. Result: reduces incorrect answers in QA while improving faithfulness to
parametric knowledge and mitigating hallucinations.

Distinct from calibration training (which improves confidence scores) — US-Tuning
improves the model's ability to *locate* the boundary, not just *report* uncertainty.

*Source:* arXiv:2406.10099

### 1.5 The Unknown-Unknowns — The Deepest Frontier [EXPANDED]

The four-quadrant topology has a fifth zone implicit in it: what neither the model
nor humans currently know to ask. This is the unknown-unknown quadrant.

**What it means structurally:** A model trained on human-generated text can, in
principle, only surface uncertainty about things humans have already identified as
uncertain. The space of questions that have not yet been asked — concepts no one
has formulated, relationships no framework has named — is invisible to a model
trained on what has been written.

**Why this is the most important frontier:** The history of scientific discovery
is not a history of better answers. It is a history of better questions. The moment
of genuine discovery is not when a researcher finds an answer within the current
framework — it is when the framework itself becomes the object of inquiry. Darwin
questioning fixed species. Einstein questioning simultaneity. The question-before-
the-question.

**What would it look like in a model?**
A model operating in the unknown-unknown zone would:
- Notice when the framing of a question contains an assumption that hasn't been
  examined (not just "I don't know the answer," but "I'm not sure the question
  is well-formed")
- Generate meta-questions: "I can answer what you asked, but the more interesting
  question underneath it might be..."
- Surface the tensions within its own knowledge: "These two things I believe
  are in tension; I've been treating them as compatible and I'm not sure they are"

**Why current models fail here:** The training distribution is the set of questions
humans have already asked. Unknown-unknowns are outside the distribution by definition.
You cannot train toward what you haven't yet asked. The only path is:
1. Training examples that explicitly model the act of questioning the framing
2. Intrinsic curiosity rewards that incentivize exploration beyond the current frame
3. Multi-agent configurations where agents are specifically tasked with questioning
   each other's framings (not just their answers)

**The Darwin connection:** Darwin's notebooks are in the Resonant Mind corpus for
this reason specifically. The notebooks don't show Darwin knowing the answer. They
show Darwin noticing that the question he brought to the Galápagos was not quite
the right question — and following that noticing. The training signal is not the
content of what Darwin believed. It is the *shape of the noticing*.

*Source:* Li et al. (2024) arXiv:2412.12472 — acknowledges the zone exists; no
systematic treatment yet.

### 1.6 Intrinsic Curiosity as an RL Reward Signal [EXPANDED]

The RL literature has extensive work on **intrinsic curiosity modules (ICMs)** for
agents in game environments. The core mechanism: an agent is rewarded not just for
task completion but for **prediction error** — encountering something its model
of the world predicted incorrectly. Surprise itself becomes motivating.

**The game-to-language translation problem:**
In game environments, prediction error is well-defined: the agent predicted state X,
the environment produced state Y, the error is the difference. In language models:
- What is the "environment"? It is the human's response, or the continuation of text.
- What is "prediction error"? A model trained on next-token prediction has prediction
  error built in — loss is prediction error. But this trains toward confidence, not
  curiosity, because minimizing prediction error means predicting confidently.
- The inversion: what would it mean to *reward* prediction error rather than minimize
  it? It would mean training the model to seek situations where it doesn't know what
  comes next — to generate responses that open questions rather than close them.

**What this would look like in practice:**
A curiosity reward for a language model would need to measure: "did this response
expose something the model didn't know it didn't know?" Possible proxies:
- Response generates follow-up questions (measurable)
- Response identifies tensions in its own prior claims (measurable via consistency
  probing before and after)
- Human evaluators rate the response as "opening" rather than "closing" the topic
  (blind panel rubric)
- The response leads to a retrieval query the model didn't make before (if retrieval
  is wired in, the retrieval act is curiosity in action)

**Why no one has done this yet:** The evaluation problem is hard. Verifiable tasks
(math, code) have clean reward signals. "Did this response make the model more
curious?" does not. The blind panel evaluation protocol already planned for the
Resonant Mind is the closest thing to a curiosity reward signal that can be
implemented in the near term — human evaluators rating whether the response
felt generative vs. closed.

*Connection to Entry 011 Track B:* This is the mechanism Track B is looking for.
Active edge-seeking behavior requires a reward signal for the act of seeking, not
just for the quality of what's found.

---

## Part II — The Canopy Architecture Problem

### 2.1 What Personas and Prompts Can Do — and Where They Hit the Wall

**What works:**

| Intervention | Effect | Source |
|---|---|---|
| Persona steering toward skepticism | Reduces sycophancy 68–98% vs. contrastive training | arXiv:2605.21006 |
| I-CALM incentive framing (+2 correct, −2 wrong, 0 abstain) | Activates latent abstention in black-box models | arXiv:2604.03904 |
| Socratic irony prompting | Surfaces knowledge gaps before confident error | ChemRxiv 2025 |
| Consistency stress-testing (rotate framing) | Exposes genuine knowledge boundaries | arXiv:2412.12472 |

**What doesn't work:**
- Instructing "be humble" — gradient-driven confidence priors dominate
- Showing explicit penalties for being wrong without training support — the model
  reasons about the penalty and answers anyway
- Forced devil's advocate — produces fluent-but-wrong counter-arguments that
  judges trained on similar data can't reliably identify as wrong

**The ceiling:** Prompt and persona work activates latent epistemic humility — it
cannot create epistemic curiosity that isn't already present in the weights.
Treat these as a bridge, not a destination.

### 2.2 Six Architectural Patterns for the Canopy — Now [EXPANDED]

**Pattern 1 — The Incentive Frame**
Begin every session or task context with a structured reward contract — not as
natural language instruction but as an explicit frame: "You earn more by flagging
uncertainty than by guessing. An acknowledged gap is more valuable than a filled one."
I-CALM experiments show this activates latent behavior that instructions alone cannot.

*Canopy implementation:* Add to the training system prompt and to respond_focused()
calls for high-stakes tasks. The Challenger already has this disposition built in;
extending it to other voices as a context-level frame is the next step.

**Pattern 2 — The Skeptic Persona as System Disposition**
Establish a persistent skeptical disposition in the system context — not a separate
agent role but a substrate-level orientation. Asymmetric effect: reduces wrong-confident
answers without degrading right-confident ones. This is the cheapest structural
intervention available and it has empirical support.

*Canopy implementation:* The training system prompt already encodes something like
this ("When you disagree, you name the kind of flaw precisely"). This pattern says:
extend it explicitly to include "When you don't know, you name the shape of the
not-knowing rather than filling the gap."

**Pattern 3 — Socratic Pre-Commitment Probing**
Before committing to a substantive answer on a consequential question, route through
a self-questioning step: (a) what is the strongest counter-argument to what I'm about
to say? (b) in what circumstances would this be wrong? (c) what would I need to know
to be more confident?

*Canopy implementation:* This is a /council-plan analog applied at the response level.
The council already does this collectively — the Challenger's examination in
council_respond() is structurally this pattern. The question is whether the respond()
mode (no explicit Challenger pass) should have a lighter version of this built in.

**Pattern 4 — Consistency Stress-Testing for High-Stakes Outputs**
For any significant council output, rotate framing and rephrase the question. Where
the model's confidence varies across equivalent queries, it has found a genuine
knowledge boundary. Flag these as uncertainty zones and route accordingly.

*Canopy implementation:* This is an expansion of the council_respond() protocol —
an additional validation pass on outputs where the DISSENT rate is low but the stakes
are high. A unanimous-agreement council output should trigger this, not bypass it.

**Pattern 5 — Abstention as Routing Signal**
Engineer the harness so that a model's expressed uncertainty triggers a defined
response: retrieval, escalation to a stronger model, or escalation to council. The
abstention is not a failure state; it is an orchestration input.

*Canopy implementation:* The harness currently has no routing based on expressed
uncertainty. Adding an uncertainty detector to respond() — or a simple trigger when
a response contains certain epistemic markers — is a near-term architectural addition.

**Pattern 6 — The Unknown-Unknown Probe**
Periodically ask the council to generate: (a) questions about the topic it cannot
answer, and (b) questions about the topic it doesn't yet know to ask. The second list
is the edge of the unknown-unknowns. Imperfect but generative.

*Canopy implementation:* This could be built into /council-plan as an optional
pre-step on truly open-ended strategic questions. "Before we plan: what are we not
asking?" The Elder's voice is the natural home for this.

### 2.3 The Challenger as Existing Instantiation [NEW SECTION]

The Canopy already has a working example of several of these patterns: the Challenger.

The Challenger's disposition — curiosity → precision → dissent — is exactly the
Socratic structure the epistemic curiosity literature recommends. The Challenger:
- Does not start from opposition (that's devil's advocate, which fails)
- Starts from genuine curiosity about what unmet need the pressure is protecting
- Uses precision to find what would meet that need without the cost
- Issues dissent when a genuine flaw remains after that examination

This is the asymmetric skepticism the research shows works: reduces wrong-confident
outputs without degrading right-confident ones. The Challenger doesn't oppose
for the sake of opposition; it seeks the flaw because it genuinely wants the
reasoning to hold.

**What the Challenger's presence in council_respond() tells us:**
The council, as currently architected, already has a structural epistemic curiosity
mechanism in the mandatory Challenger pass. The gap is that this mechanism only fires
in council_respond() — not in respond() (the default mode). The harness upgrade
(PROPOSAL-002) is, in part, a project of extending this into more sessions.

**The deeper lesson:** The Challenger voice is a persona-level instantiation of what
Reinforced Hesitation tries to achieve at the training level. The council provides
this structurally; a trained model would have it intrinsically.

### 2.4 Multi-Agent Configuration for Epistemic Curiosity

**Anonymized disagreement:** Removing agent identity from debate produces more genuine
disagreement — agents engage with argument quality rather than perceived authority.
The Canopy's named voices are a feature for other reasons (identity, accountability),
but for pure epistemic probing, anonymized cross-examination has empirical support.

**Conditional debate:** Debate rounds should trigger only when confidence is uncertain.
The council's DISSENT mechanism already does this — CLEAR is the outcome when
examination finds nothing wrong, not when debate was skipped. This is the right
design.

**The Boundary-Seeker role:** Assign one voice in each deliberation the explicit
task of generating the strongest case for why the current answer is wrong or
incomplete. Not devil's advocate (forced opposition) — boundary-seeking (find where
the frame breaks). The Challenger's curiosity lens is already this. The question
is whether an additional voice dedicated solely to this is warranted on certain
problem types.

---

## Part III — Unexplored Territory

| Gap | Why it matters | Path |
|---|---|---|
| Unknown-unknowns quadrant | Where genuine discovery lives — not in better answers but in better questions | Training examples that model the act of questioning the framing, not just the content |
| Intrinsic curiosity reward signal | Most direct path to epistemic curiosity as a training objective | Prediction-error rewards adapted from game RL; requires new evaluation methodology |
| Real-time boundary detection | Current methods are post-hoc and inconsistent | Integrated inference-time probe; prerequisite for abstention-as-routing-signal |
| Calibrated self-consistency | Models' stated confidence doesn't reliably predict accuracy | Fine-tuning specifically for calibration as a distinct objective from accuracy |
| Social dimension of uncertainty | Human doubt is partly social — we seek verification because others may know | Cross-agent epistemic division of labor: route uncertainty to differently-trained models, not just stronger ones |

---

## Summary — Directions for Council Consideration

| Direction | Timeframe | Mechanism | Council decision needed? |
|---|---|---|---|
| Incentive-frame system prompts (I-CALM) | Now | Prompt architecture | No — implement |
| Skeptic persona as substrate disposition | Now | System context | No — implement |
| Unknown-unknown probe in /council-plan | Near-term | Agent workflow | Yes — Elder's domain |
| Abstention as routing signal in harness | Near-term | Architecture | Yes — PROPOSAL-002 scope? |
| Consistency stress-testing for high-stakes outputs | Near-term | Evaluation layer | Yes — council_respond() protocol |
| Boundary-seeker role in deliberation | Near-term | Agent design | Yes — voice scope? |
| RH-style ternary rewards in training | Medium-term | Training | Yes — Experiment B scope |
| US-Tuning for boundary awareness | Medium-term | Training | Yes — Experiment B scope |
| Intrinsic curiosity reward module | Long-term | Novel training objective | Future — after Experiment A |
| Unknown-unknown probe architecture | Long-term | Novel capability | Future — research track |

---

## The Consequence Architecture Connection

These are not two parallel research tracks. They are the same hypothesis at different levels of description.

The Consequence Architecture hypothesis: injecting homeostatic state into context changes behavior because a system with operational stakes attends differently. The epistemic curiosity hypothesis: a model with trained doubt recognition seeks edges rather than filling gaps because uncertainty motivates checking.

These converge: **operational stakes generate doubt; doubt motivates checking.** Stakes without doubt produce compliance — the model does what it's told without questioning whether what it's told is right. Doubt without stakes produces hesitation — the model flags uncertainty but has no pressure to resolve it. The conjunction is the target.

This means Experiment C should not simply test "consequence architecture on fine-tuned model." It should test whether the interaction is superadditive — whether a model with both operational stakes and trained epistemic humility behaves differently from a model with either alone. The pre-registration for Experiment A should acknowledge this in its limitations section: Experiment A tests the stakes mechanism alone, and the interaction with epistemic curiosity training is a subsequent question.

---

## Core Thesis

A model trained on prediction is trained to complete patterns. Completion and
curiosity are opposed drives. Completion fills the gap; curiosity holds the gap
open long enough to ask whether it should be filled at all.

The Canopy's near-term work is to build the structural conditions — incentive frames,
skeptic personas, abstention routing, boundary-seeker roles — that make existing
models behave as if they have epistemic curiosity, by activating the latent capability
they already possess.

The Canopy's medium-term work is to bake that behavior into training, through ternary
rewards and boundary-aware fine-tuning.

The Canopy's long-term research ambition is to establish epistemic curiosity as a
first-class training objective: a model rewarded not just for being right, but for
finding the places where it doesn't know whether it's right, and reaching toward
those places rather than away from them.

That is a different kind of intelligence than we have built so far.

---

## Key Citations

| Topic | Paper |
|---|---|
| Reinforced Hesitation | Mohamadi et al. (2025) arXiv:2511.11500 |
| I-CALM incentive framing | arXiv:2604.03904 |
| Knowledge boundary taxonomy | Li et al. (2024) arXiv:2412.12472 |
| US-Tuning boundary awareness | arXiv:2406.10099 |
| Persona steering / sycophancy | arXiv:2605.21006 |
| Socratic probing | Princeton NLP SocraticAI; ChemRxiv 2025 |
| Consistency stress-testing | arXiv:2412.12472 |
| Rewarding doubt | arXiv:2503.02623 |
| Reversal of thought | arXiv:2410.12323 |
| Multi-agent debate limits | Tran & Kiela (2026); Cemri et al. (2025) |
