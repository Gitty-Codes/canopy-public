# Canopy Research Roadmap
*Working document — June 2026*
*Two parallel research threads: Consequence Architecture and Resonant Mind Training*
*Publishing standard: PhD-defensible, interesting to AI labs*

---

## How to read this

**Machine actions** — what Claude does in Claude Code sessions.
**Founder actions** — what you do. These are the things that can't be delegated.

Phase gates are real: Phase 1 does not start until Phase 0 is complete.
Experiments do not run until pre-registration is complete.
Results are reported honestly whether positive or negative.

---

## Phase 0 — Foundation
*Status: In progress*

### Machine actions (Claude)
- [x] Consequence architecture hypothesis revised for external publishing (v0.3)
- [x] Consequence architecture spec revised — quality proxy removed, macmon to background, versioning, v1 scope defined (v0.2)
- [x] Listener voice tone fixed — tentative language, not declarative
- [x] `experiment-protocol` skill built — pre-registration, inter-rater reliability, power analysis, results reporting
- [x] Research directories structured: `research/consequence-architecture/`, `research/resonant-mind-training/`
- [x] Training data export pipeline built: `tools/export_training_data.py` — exports council sessions as Type D ChatML examples; `--mark` flag for founder curation; `--only-approved` for clean export
- [x] Run code-health Check 0 against consequence architecture spec v0.2 — two bugs fixed (token budget path, urgent markers); gpu/ane hardware fields deferred until macmon installed
- [x] Write data science rigor research note (Leek principles applied to our specific experiments) — filed at research/data-science-rigor-note.md
- [x] Draft pre-registration document for consequence architecture v1 experiment — filed at research/consequence-architecture/prereg-experiment-a-v1.md; awaiting founder sign-off
- [x] Draft pre-registration document for Resonant Mind first experiment — filed at research/resonant-mind-training/prereg-experiment-b-v1.md; awaiting founder sign-off
- [x] Write power analysis for both experiments (required N before data collection) — embedded in both pre-registrations; N=88 paired for primary measure (80% power, d=0.3)
- [x] Write literature review notes: Society of Mind, Free Energy Principle, GWT — positioned against the hypothesis — filed at research/literature-review-notes.md
- [x] Design the blind evaluation protocol with specific prompts and rater rubric — filed at research/blind-evaluation-protocol.md

### Founder actions (you)
- [x] **Confirm versioning schema** — schema confirmed complete; Experiment B training environment fields added (unsloth_version, cuda_version, colab_gpu, training_dataset_hash, gguf_quantization, ollama_version); canopy git-hash covers voices + constitution implicitly
- [x] **Decide publish venue** — arXiv preprint first (establishes priority, stable URL), then Show HN: post linking the arXiv paper the morning it goes live. Paper format: LaTeX/PDF (Phase 3 task).
- [x] **Set up W&B workspace** — skipped: W&B SSO block prevented signup with personal accounts. Replaced with local CSV logging (`loss_log.csv`) via `LossLoggerCallback` in training-pipeline-spec.md. Loss curves plotted locally with pandas after training. W&B can be added in a later experiment if SSO issues resolve.
- [x] **Get Colab Pro access** — signed up 2026-06-07
- [x] **Brew install macmon** — installed and verified 2026-06-07; API changed to subcommand (`macmon pipe`); hardware_monitor.py updated accordingly
- [ ] **Recruit blind evaluation panel** — 3–5 people who: (a) have not been involved in building this, (b) represent genuinely different perspectives, (c) are willing to do two evaluation sessions with a gap between. These are not technical reviewers — they are the people the system will eventually serve.
- [ ] **Send Kimmerer letter** — ready to send in `research/resonant-mind-training/outreach-letters-ready.md`. Verify her SUNY-ESF email first.
- [ ] **Read three ML onramp resources** (before the Resonant Mind training run):
  - The Illustrated Transformer: jalammar.github.io/illustrated-transformer
  - Sebastian Raschka on LoRA: rasbt.github.io/mlxtend (search "LoRA fine-tuning")
  - W&B basics tutorial: wandb.ai/tutorials

---

## Phase 0.5 — Council Infrastructure
*Can run in parallel with Phase 0 — no blockers*

### Agent-to-agent relational memory

**What it is:** After consequential council sessions, voices write brief relational observations about other voices — how they reason, their characteristic patterns, their blind spots. Injected into council substrate at session open. The council knows itself as a council.

**Machine actions:**
- [ ] Add `relational` memory type to episodic memory schema (new field: `about_agent`)
- [ ] Write post-session protocol: which sessions trigger /reflect, which voices observe which
- [ ] Update harness to load relational memories at council session open (inject per voice)
- [ ] Run /reflect retrospectively on the three sessions from this conversation as seed data

**Founder actions:**
- [ ] **Run /reflect after each future council session** — brief, 5 minutes, immediate after the session while it's fresh. This is the discipline that makes the memory valuable.

### Council orchestration rules (no code change required)

From effectiveness analysis of three sessions:
- **Steward trigger:** engage The Steward whenever a proposal claims Constitutional alignment
- **Convergence naming:** when Guardian and Challenger flag the same concern, name the convergence explicitly rather than running full parallel outputs
- **Operator trigger:** engage when consequence architecture history data exists and needs interpretation

---

## Phase 1 — First Experiments
*Starts when Phase 0 machine and founder actions are complete*
*Both experiments run in parallel but are analyzed independently*

### Experiment A: Consequence Architecture v1

**What we're testing:** Does injecting constitutional tension state and dissent history into the LLM context before each inference produce measurably different outputs in blind evaluation?

**Machine actions:**
- [ ] Implement consequence architecture v1 (constitutional loop + dissent tracking + token budget, per spec-v0.2.md)
- [ ] Wire into harness.py — minimal modification, clearly delimited
- [ ] Run 100 warm-up cycles to populate history and profile
- [ ] Produce control and treatment output sets (standardized prompts, logged with versioning)
- [ ] Statistical analysis per experiment-protocol skill

**Founder actions:**
- [ ] **Run pre-registration review** — read the pre-registration document before any experiment runs and confirm it matches your understanding of the hypothesis. Sign off with a date.
- [ ] **Coordinate blind evaluation panel** — give panel members the evaluation rubric, run sessions, collect ratings independently before group discussion
- [ ] **Log inter-rater reliability** — calculate Cohen's kappa from panel ratings before looking at aggregate results

### Experiment B: Resonant Mind First Training Run

**What we're testing:** Does fine-tuning on a curated corpus (50–100 examples, four canonical sources + council session transcripts) produce measurably different outputs on the wandering test, dissent test, and typed DISSENT tests in blind evaluation, compared to the base model?

**Two training data types:**
- **Type C** (synthetic open-wandering conversations) — primary signal for wandering, brevity, relational attention behaviors
- **Type D** (council session transcripts) — deliberative arc: initial response → typed DISSENT examination → synthesis with DISSENT RECORD. Primary signal for DISSENT behavior. Export via `tools/export_training_data.py --only-approved`

**Machine actions:**
- [ ] Generate 50–100 synthetic Type C training examples using Claude API with constitutional system prompt (see updated system prompt in training-pipeline-spec.md)
- [ ] Curate Type C: apply resonance test, keep examples passing 3+ of 5 criteria
- [ ] Export and curate Type D: run export script; founder reviews and approves sessions
- [ ] Format to Qwen2.5 ChatML template
- [ ] Write training script from training-pipeline-spec.md
- [ ] Run 500 training steps on Colab Pro, checkpoint at 250 and 500
- [ ] Log per-example loss for diagnostic review; high-loss Type D examples indicate where DISSENT behavior is being most actively shaped
- [ ] Produce control (base model) and treatment (fine-tuned) output sets

**Founder actions:**
- [ ] **Run training** — execute the training script on Colab Pro. Watch the loss curve for the first 50 steps; if it oscillates instead of descending, stop and consult.
- [ ] **Curate Type C examples** — apply the resonance test to each generated example. Budget 2–3 hours.
- [ ] **Curate Type D sessions** — run `python tools/export_training_data.py --dry-run` to see candidates; use `--mark <id> true/false` to approve or reject. A Type D session is worth keeping if the DISSENT was genuine (not manufactured), the reasoning in the DISSENT RECORD is clear, and the synthesis improved on the initial response.
- [ ] **Run pre-registration review** — same as Experiment A. Sign off before training runs.
- [ ] **Coordinate blind panel** — same panel as Experiment A, different session to prevent contamination.

---

## Phase 1.5 — Constitutional Transfer
*Starts when Experiment B produces a positive result; can overlap with Phase 2 analysis*

**The question:** Does the constitutional orientation in the general foundation model survive the routing handoff to a domain SLM, producing coherent constitutional+domain responses that neither could produce alone?

**Architecture clarification (from council deliberation, 2026-06-07):** Domain SLMs are not expected to hold full constitutional orientation in isolation. The foundation model holds the deliberative and constitutional layer; the SLM holds domain expertise. The routing layer connects them — SLM handles domain content, foundation model handles constitutional evaluation and synthesis. The capacity floor question is therefore not "can a 3B model hold constitutional orientation alone?" but "does the handoff preserve constitutional integrity?" This is a more tractable test and a more honest description of how the orchestra actually works.

**Why this determines Phase 2:** Labs are building one general model that does everything. The Canopy hypothesis is a collection of resonant models: one general capable resonant foundation + purpose-built SLMs (code, music/musicology, sheet music reading) trained on domain corpora and constitutionally fine-tuned. Each specialist runs locally — privacy through architecture, not policy. Together they match frontier capability for the domains that matter. This architecture scales with the open-source ecosystem rather than competing against it. The biodiversity of the ensemble — different training sources, different domain orientations — is what makes the system self-governing rather than requiring a central conductor.

**Machine actions:**
- [ ] Select domain base model for first transfer test (Qwen2.5-Coder for code, or a music-capable base for Practice Buddy — music is higher mission value, code is easier to validate)
- [ ] Apply Experiment B's constitutional LoRA to the domain base
- [ ] Build minimal routing prototype: foundation model receives domain-specialist output and applies constitutional evaluation layer
- [ ] Test handoff quality: does a domain-specialist response routed through the constitutional foundation produce typed DISSENT when warranted?
- [ ] Run typed DISSENT tests on the combined system (not the SLM in isolation)

**Local training note:** Domain SLMs at 1–3B can be trained locally on the M2 using Apple MLX (`mlx_lm.lora`). QAT base models (Gemma 4 E2B ~1GB, E4B ~2GB) make this feasible. First experiment (7B general model) still requires cloud (Colab Pro / RunPod). Iteration on domain specialists: local-first.

**Founder actions:**
- [ ] **Choose the domain** — music (higher mission value for Practice Buddy) or code (easier to validate)?
- [ ] **Run blind panel** — same panel, domain-relevant prompt.

**What this determines:**
- Handoff quality holds → Phase 2 is the orchestra
- Handoff quality degrades → constitutional signal is lost in the routing; investigate routing architecture before proceeding

---

## Phase 2 — Iteration
*Starts when Phase 1 analysis is complete and results are reported*

The specific Phase 2 plan depends on Phase 1 and Phase 1.5 results.

**If Experiment A supported:** Add metabolic layer to consequence architecture. Redesign quality proxy (register-sensitive, versioned). Run Experiment A-2 with expanded architecture.

**If Experiment A not supported:** Revisit hypothesis. Do not add more architecture — investigate why the constitutional loop didn't change behavior. Revise or reject before proceeding.

**If Experiment B supported and Phase 1.5 transfer holds:** Build the orchestra. General resonant foundation model (expand training set to 500 examples across Types C and D, add full canonical source range, 3,000 steps) plus at minimum one domain specialist (music SLM for Practice Buddy). Each specialist: domain-competent base + constitutional LoRA.

**If Experiment B supported but Phase 1.5 transfer fails:** Expand Experiment B on general base before extending to domains. Investigate whether constitutional training requires constitutional signal in pre-training, not just fine-tuning.

**If Experiment B not supported:** Review highest-loss training examples. Consider whether base vs. instruct model choice was right. Revise curation protocol. Do not proceed to Phase 1.5 until Experiment B shows signal.

**If both Experiments A and B supported and Phase 1.5 transfer holds:** Run Experiment C — consequence architecture running on the fine-tuned model substrate, applied to the domain specialist. This is the full stack: drives + orientation + domain competence. The hypothesis is that the combination produces something none achieves alone.

---

## Phase 3 — Publication
*Starts when Phase 2 produces results worth publishing*

**Machine actions:**
- [ ] Draft research paper from hypothesis v0.3 + experiment results
- [ ] Literature review section positioned against Society of Mind, FEP, GWT
- [ ] Statistical appendix with full data
- [ ] Format for target venue (arXiv preprint or workshop submission)

**Founder actions:**
- [ ] **Identify target venue** — AI safety workshops (NeurIPS, ICLR), consciousness and AI conferences, or direct AI lab outreach. This decision shapes the paper's framing.
- [ ] **Engage outside reviewer** — at least one person with AI research background who has not been involved in this project, who can push back on the claims before submission.
- [ ] **Decide attribution** — the hypothesis documents were co-developed. What does authorship look like for an AI-human collaboration? This is worth deciding explicitly before submission.

---

## Blind Evaluation Panel — Logistics

**Format:** Google Form or Typeform. No machine access, no repo to clone.

**Form structure:**
- The standardized prompt (context for raters)
- Response A / Response B (condition not labeled — raters don't know which is control)
- Rubric: 4–5 specific criteria, rated 1–5 each (criteria defined in pre-registration)
- One open question: "Describe what you noticed about each response"
- Preference question: "Which would you continue this conversation with?"

**Randomization:** Across raters, randomize which condition is labeled A. Some raters see control as A, others see treatment as A. Prevents position bias.

**Rater profile:** People who have not been involved in building the system. Genuinely different perspectives. Willing to do two sessions (Experiment A and Experiment B) with a gap between.

**Before raters see anything:** Inter-rater reliability rubric is written, raters are briefed on what they're evaluating and what they're not (no technical explanation of conditions), sessions are run independently.

---

## What We Are Watching For

**Signs the work is real science:**
- Pre-registrations written before data collection and unchanged after
- Null results reported with the same care as positive results
- Effect sizes matter more than p-values
- Blind evaluators can distinguish conditions above chance

**Signs of vibe-coding drift:**
- Results are always positive
- Hypotheses are revised after seeing data
- Qualitative impressions substituted for measurement
- Claims exceed what the evidence supports

The second list is not a failure — it is information. The roadmap adjusts. We do not rewrite the past.

---

*Updated: 2026-06-07*
*Next review: after Phase 0 machine actions complete*

---

## Research Hypothesis — Phase 2: Weight-Level State Conditioning
*Originated: 2026-06-08, from founder reflection on Illustrated Transformer*

### The gap Experiment A does not close

Experiment A tests whether injecting homeostatic state as *text into context* changes
measurable behavior. The state prompt ("Token budget: 71% used. Dissent: suppressed.")
is processed semantically — the model responds to it the way it responds to any text,
via learned associations from its training distribution.

This is structurally different from what somatic signals do in biological cognition.
Somatic signals (cortisol, interoceptive feedback, urgency arousal) reshape attention
and cognition *pre-consciously*, before semantic processing. They act at the level of
the architecture, not the content.

**The hypothesis:** text-based state injection is a partial, brittle approximation
of somatic signaling. The deeper mechanism requires the signal to influence the
attention computation directly — via the weight matrices, not via the context window.

### What's actually missing

- **Project delta**: difference between current and previous session state (trajectory,
  not just snapshot). Computable from project memory; not currently used.
- **Urgency at weight level**: the model has learned associations for urgency-as-described
  but no intrinsic sensitivity to urgency-as-signal.
- **Importance**: not tracked at any level.
- **Model routing informed by state**: which model is best for this task/urgency/budget
  combination. router.py exists but is not informed by homeostatic state.
- **Cross-session delta**: what changed since last time the project was touched.

### Candidate architectures for Phase 2

**Option A — Cross-attention state conditioning:**
Encode the homeostatic state as a dense vector (not text). Inject it into the
attention computation via cross-attention on the K and V projections:

```
CrossAttention(Q_text, K_state, V_state)
```

The state vector shapes which text tokens attend to what — pre-semantically. This
is mechanistically closer to somatic signaling than text injection.

**Option B — State-conditioned LoRA:**
Train LoRA adapters with homeostatic state as a conditioning variable. Multiple
adapter sets, each tuned to a different state regime (urgency + suppression,
token pressure + creative task, etc.). The active adapter is selected by state,
not by prompt.

**Option C — State-annotated training data:**
Annotate Type D council sessions with the homeostatic state that was active during
each session. Fine-tune with state as a conditioning signal. The model learns
intrinsic sensitivity to state — not from context text, but from the training
distribution. Requires substantially more Type D data than Phase 1 corpus.

### What determines which to pursue

Experiment A outcome:
- If null result: text-based injection doesn't change behavior. Strong motivation
  to move to architecture-level conditioning (Option A or B).
- If positive result: text-based injection works. Phase 2 tests whether weight-level
  conditioning produces larger or more stable effects.

Either outcome motivates Phase 2. A null result makes it urgent.

### The worldedness problem (deeper)

The semantic/somatic gap is a specific instance of a more general problem: transformer
models have propositional knowledge about the world but no situational engagement with
it. They know what urgency means; they don't respond to urgency the way an organism
does. This is Heidegger's distinction between Vorhandenheit (presence-at-hand,
propositional) and Zuhandenheit (readiness-to-hand, situational engagement).

The consequence architecture is an attempt to give the system situational engagement
through self-monitoring. Whether that's achievable via text injection or requires
architectural change is the open empirical question.

*Flag for Phase 2 pre-registration after Experiment A results are in.*
