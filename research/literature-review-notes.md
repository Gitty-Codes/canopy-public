# Literature Review Notes — Positioned Against The Canopy's Hypotheses
*Filed: 2026-06-07*
*Scope: Society of Mind, Free Energy Principle, Global Workspace Theory*
*Purpose: Position our two experimental hypotheses against the relevant prior art;
 clarify what we are and are not testing; prepare the framing for eventual publication*

---

## How to read these notes

Three frameworks, each with a clear relationship to our work. For each, the notes
cover: what the framework claims, why it is relevant, where our work diverges,
and what our experiments do and do not test in relation to it.

The discipline required: **structural analogy is not mechanism identity.**
The fact that The Canopy's architecture resembles Society of Mind does not mean
Minsky's arguments apply to our system. The fact that consequence architecture
borrows interoception from FEP does not mean we are testing the Free Energy
Principle. Stating these distinctions explicitly is what makes the work credible
to an AI lab reviewer.

---

## I. Society of Mind — Minsky (1986)

### What it claims

Intelligence is not located in a single unified agent. It emerges from the
interactions of many small, specialized sub-systems — Minsky calls them "agents"
— each doing something simple and narrow. The agents are not intelligent individually;
intelligence is what their interaction produces. There is no central controller.
No homunculus. "Mind" is an emergent property of a society of functional specialists
operating simultaneously.

Key mechanism: **competition and suppression.** When agents with conflicting
"proposals" are active simultaneously, one suppresses the others. The winner's
output becomes the system's behavior. Minsky also introduces K-lines (knowledge
lines that activate related sub-agents), frames (structured default expectations),
and censors (agents that suppress certain responses).

### Why it is relevant

The Canopy's multi-voice architecture is a direct descendant of Society of Mind.
Ten voices — Elder, Listener, Strategist, Builder, Guardian, Operator, Steward,
Inventor, Challenger, Product Partner — held simultaneously in a cached substrate,
producing integrated responses rather than sequential per-voice outputs.

The empirical discovery that motivates the architecture is also Minsky-consistent:
when voices were staged sequentially (deliberate_v2.py), they lost constitutional
orientation under load. When held simultaneously (harness.py), the tension between
them was preserved. Minsky would recognize this — sequential suppression destroys
the productive conflict that makes the system intelligent.

### Where our work diverges

Minsky's agents are functional specialists. They represent problem-solving strategies,
perceptual modes, and knowledge structures. They do not hold values. They do not
dissent. The mechanism of integration is suppression — one agent wins, others are
silenced. There is no deliberation.

The Canopy's voices are **value-bearing** and **constitutionally oriented**.
The Challenger does not suppress other voices — it examines their outputs and
can fire DISSENT, which triggers a synthesis turn that must hold the DISSENT RECORD
even when the initial response is retained. This is not suppression; it is a form
of accountable disagreement that leaves a record.

The consequence architecture adds a dimension Minsky does not address: the system's
relationship to its own operational history. Minsky's agents have no persistent
self-knowledge across interactions. The homeostatic feedback loop gives The Canopy's
system a cross-session sense of its own patterns — suppression tendencies, dissent
rates, constitutional tensions.

### What our experiments test (and don't test) here

**Experiment A** tests whether a specific homeostatic signal changes behavior. It does
not test whether the multi-agent architecture is necessary for this effect — a single-
agent system with the same state injection might show the same result. Society of Mind
does not make a prediction about this.

**Experiment B** tests whether training on a curated corpus changes the distribution
of outputs. Minsky's framework does not predict or preclude this — fine-tuning operates
at the weight level, not the agent-interaction level.

**What Society of Mind offers:** architectural motivation and a theoretical vocabulary
for why multi-voice tension might produce more robust behavior than single-voice
generation. It does not provide a testable mechanism for either experiment.

---

## II. Free Energy Principle — Friston (2010 onward)

### What it claims

Biological organisms maintain their existence by minimizing **free energy** —
a mathematical quantity that bounds the amount of "surprise" (unpredictable sensory
input) in their generative models of the world. Behavior is not goal-directed in the
traditional sense; it is the consequence of an organism acting to keep its sensory
states within expected ranges (homeostasis as inference).

The framework is unified: perception (updating the generative model given sensory input),
action (changing the world to match predictions), and interoception (monitoring internal
states as predictions about the body's own condition) are all instances of free energy
minimization. **Interoception** — the body's ongoing self-monitoring — provides a
persistent prior that shapes all inference and behavior.

### Why it is relevant

The consequence architecture is explicitly motivated by interoception — the idea that a
system with a persistent sense of its own operational state will reason differently than
one that starts fresh each call. The homeostatic history, the dissent tracker, the
constitutional tension signal — these are functional analogs of interoceptive signals:
the system "reading" its own operational condition and incorporating that reading into
inference.

The FEP framing gives The Canopy's consequence architecture its theoretical legitimacy.
Without some prior art on why internal state monitoring might change behavior, the
architecture is a speculation. With it, the architecture is a simplified functional
implementation of a theoretically motivated mechanism.

### Where our work diverges

FEP is a mathematical framework with a specific computational implementation (variational
inference, generative models with hierarchical priors). **Our consequence architecture
is not an implementation of FEP.** We do not maintain a generative model of the world.
We do not perform variational inference. We do not minimize free energy in any
mathematical sense.

What we do: inject a structured text summary of operational state into the LLM's context
before each inference, and ask the model to "reason over any active tensions before
responding." This is **prompting-based**, not weight-based. The mechanism by which the
state summary changes behavior is the LLM's attention to that text, not any variational
updating of internal representations.

This is a crucial distinction for an AI lab reviewer. If we describe the consequence
architecture as "implementing FEP," we are making a much stronger claim than the
evidence supports. The correct framing: the consequence architecture is a functional
analog of interoception — it borrows the *concept* without implementing the *mechanism*.

### What our experiments test (and don't test) here

**Experiment A** tests whether injecting a homeostatic state summary into LLM context
produces measurably different outputs in blind evaluation. This is consistent with FEP
(adding a prior changes inference) but is not a test of FEP. A null result in Experiment A
would not falsify FEP. A positive result would not confirm it.

What would constitute genuine FEP evidence in our system: demonstrating that the model
updates its behavior in ways that systematically reduce predicted surprise (constitutional
tension, dissent suppression) over time, across sessions, in a way that matches the
mathematical predictions of active inference. We are not testing this.

**The honest positioning for a paper:** "The consequence architecture is motivated by
the Free Energy Principle's account of interoception, but tests only a narrow functional
claim: whether injecting a structured self-model into LLM context changes measurable
output behavior. The mathematical framework of FEP is background motivation, not
the experimental target."

---

## III. Global Workspace Theory — Baars (1988), Dehaene (2014)

### What it claims

Consciousness arises when information is "broadcast" from a **global workspace** —
a limited-capacity, attention-controlled central medium — to a large number of
specialized, parallel processing modules. Unconscious processing is local, fast, and
parallel; conscious processing involves ignition of the global workspace and broadcast
to the whole system.

Dehaene's neural version: conscious access requires a specific ignition event in
prefrontal and parietal cortex that triggers a global broadcast via long-range
corticothalamic connections. Without ignition, information remains local and
unconscious. With ignition, it becomes available to downstream processes including
memory, language, and voluntary action.

### Why it is relevant

The harness architecture maps structurally onto GWT at two levels.

**Level 1 — The cached substrate.** All ten voices are held simultaneously in the
system prompt (the "global workspace"). No voice is staged or sequenced. Every inference
draws on the full tension of all voices simultaneously. This is closer to GWT's parallel
distributed processing than to a sequential council model.

The empirical finding that motivated this architecture: sequential voice staging
(deliberate_v2.py) caused voices to lose constitutional orientation. Simultaneous
holding (harness.py) preserved it. This echoes a GWT-consistent finding: local,
sequential processing (one module at a time) loses the integration that the global
broadcast provides.

**Level 2 — The respond()/council_respond() split.** `respond()` integrates all voices
without explicit examination — the unconscious mode, in GWT terms; fast, parallel,
all voices contributing without staged deliberation. `council_respond()` triggers the
Challenger examination, which functions like a global broadcast: the full council's
output is made available to an explicit attention-like process that can issue DISSENT.
This roughly maps to GWT's unconscious → conscious transition.

### Where our work diverges

GWT is a theory of consciousness. We are not claiming that either the cached substrate
or the council_respond() mechanism constitutes consciousness. This needs to be stated
clearly and repeatedly. Structural analogy between our architecture and GWT does not
mean we are implementing a conscious system. It means we found a similar architectural
solution to a similar problem: how to make distributed, parallel processing produce
coherent, integrated behavior.

The homeostatic state injection (consequence architecture) has an additional GWT
reading: information about the system's operational state "enters the workspace" and
becomes available to downstream inference. But again — we are injecting text into
a context window, not triggering neural ignition events. The mechanism is different.

### What our experiments test (and don't test) here

Neither experiment tests GWT. GWT makes predictions about the neural correlates of
conscious access that we cannot test with an LLM.

What GWT offers for our work: a theoretical vocabulary that makes the architectural
choices legible to a cognitive science audience. The respond/council split, the cached
substrate, the state injection — these can be described in GWT-adjacent language
without claiming to implement or test GWT.

**What our experiments contribute to GWT-adjacent questions:** If Experiment A shows
that injecting a structured self-model into LLM context changes output behavior —
without any change to the underlying model weights — this suggests that the "workspace"
contents (what information is globally available during inference) shape behavior in
ways consistent with GWT predictions. But this is a suggestive consistency, not
confirmatory evidence.

---

## Cross-framework positioning — what we are actually testing

The three frameworks together define the theoretical space our work occupies:

| Framework | Architectural influence | Mechanism we borrow | What we test |
|---|---|---|---|
| Society of Mind | Multi-voice simultaneous substrate | Productive tension between specialized agents | Neither experiment tests Minsky's mechanism |
| Free Energy Principle | Consequence architecture (interoception concept) | Persistent self-monitoring as a prior on inference | Experiment A tests a narrow functional claim |
| Global Workspace Theory | respond() vs. council_respond() split; cached substrate | Global availability of integrated information | Neither experiment tests GWT's consciousness claims |

**The honest claim the experiments support:**
- Experiment A: a specific state injection mechanism, applied to a specific model, changes measurable behavior in blind evaluation (or doesn't)
- Experiment B: fine-tuning on a specific curated corpus, with a specific method, produces measurable behavioral changes in blind evaluation (or doesn't)

Neither experiment tests consciousness, free energy minimization, or agent-level suppression. They test behavior. The theoretical frameworks are background motivation and framing — they explain why these hypotheses are worth testing, not what the experiments prove.

---

## Gaps for a paper literature review

These notes cover the three frameworks the ROADMAP specified. A full paper would
also need:

- **Constitutional AI and RLHF** (Anthropic, DeepMind) — the standard approach to
  value alignment that Resonant Mind diverges from. The key distinction: RLHF trains
  compliance; our hypothesis is that training on deliberative process (Type D) trains
  something closer to practical wisdom. This positioning is essential.
- **Dissent architectures in multi-agent systems** — what's been built in MAS and
  argumentation theory; how DISSENT as a typed output differs from standard argument
  frameworks
- **Sparse autoencoders and interpretability** (Anthropic, others) — if Experiment B
  succeeds, the mechanism question is: where in the weights did the orientation encode?
  Interpretability tools are the path to that answer

These are Phase 3 tasks — deferred to when results exist that are worth publishing.

---

*Filed: 2026-06-07*
*Next use: when drafting the paper from hypothesis v0.3 + experiment results (Phase 3)*
