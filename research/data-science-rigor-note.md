# Data Science Rigor — Note for The Canopy's Experiments
*Filed: 2026-06-07*
*Applies to: Experiment A (Consequence Architecture) and Experiment B (Resonant Mind)*

This note applies Leek's data analysis framework and the broader replication-crisis
literature to the specific failure modes present in these two experiments. It does not
repeat what is in the experiment-protocol skill or the pre-registrations. It names
the places where rigor breaks down in practice for experiments like ours.

---

## What Leek's framework actually demands

Jeff Leek's core discipline — and the one most violated in practice — is the
distinction between **exploratory** and **confirmatory** analysis.

**Exploratory:** you look at data without a committed hypothesis. You notice patterns.
You generate questions. You adjust your approach. This is legitimate science and
the natural start of any inquiry. It is not publishable as a finding.

**Confirmatory:** you state a specific hypothesis before seeing data, collect data,
and report the outcome whether positive or negative. The pre-registration is the
commitment device. The result is publishable precisely because the question was
locked before the answer was known.

The crisis in science — and the reason AI research in particular has a credibility
problem — is that exploratory work is routinely presented as confirmatory. Results
that fit the narrative are published; results that don't are adjusted until they do.
This produces a literature of findings that don't replicate.

**Our protection:** two pre-registered documents, filed 2026-06-07, before any
training data exists, before any model is trained, before any evaluation runs.
The protection works only if those documents are not modified after sign-off.

---

## The specific threats in our experiments

### Threat 1 — Curation drift (Experiment B)

The founder curates both Type C examples (resonance test) and Type D sessions
(`--mark true/false`). The founder is also the person most invested in a positive result.
This is not a character flaw — it is a structural conflict of interest that exists in
every experiment where the researcher and the curator are the same person.

**How it breaks:** The resonance test has five criteria. "3 or more" is the threshold.
If examples are borderline (exactly 3), the curator's judgment on which criteria are
"really" met drifts toward keeping the examples that seem most likely to produce
the desired training signal. This is not deliberate — it is motivated reasoning
operating below conscious attention.

**Mitigation already built in:** Two independent curators, inter-curator agreement
recorded, disagreements reviewed jointly. The resonance test criteria are pre-specified
and fixed.

**What to watch for:** If inter-curator agreement falls below 80% on binary pass/fail,
the rubric is ambiguous and the curation is unreliable. Fix the rubric; re-rate.
Do not proceed with disagreed examples by majority vote of two — require a third reviewer
or discard.

**Type D additional risk:** The founder approves council sessions for training.
There is a specific temptation to approve sessions where the council performed well
(clear DISSENT, strong synthesis) and reject sessions where it was muddy.
This is fine as a curation standard *only if it was stated before curation began*.
If the standard drifts during curation (e.g., the bar for "genuine DISSENT" gets
higher or lower as you see more examples), the training set is biased in an
undocumented direction.

**Mitigation:** Write a one-sentence curation standard before running `--dry-run`.
Apply it consistently. If you find yourself reconsidering a previously applied standard
mid-curation, stop and log the reconsideration.

---

### Threat 2 — Checkpoint selection (Experiment B)

Training checkpoints at step 250 and step 500. The pre-registration specifies
evaluation at step 500 (the final checkpoint). But if the step-500 model shows worse
behavior on informal testing before formal evaluation, there is pressure to evaluate
the step-250 checkpoint instead — and then report that as the "optimal" checkpoint.

This is a form of p-hacking with checkpoints.

**Rule:** Evaluation runs on step 500. Period. If step 500 shows worse loss than
step 250 (eval loss rising while train loss falls — classic overfitting), this is
a reportable result: the model overfit. The step-250 checkpoint is examined as a
*secondary diagnostic*, not as a replacement primary result.

**What to log:** Eval loss at both checkpoints, before any behavioral evaluation runs.
This gives you the loss picture independently of the behavioral evaluation and prevents
the temptation to pick the checkpoint that "looks better."

---

### Threat 3 — Warm-up corpus selection (Experiment A)

The treatment condition requires 100 warm-up cycles to populate the homeostatic profile.
The content of those cycles determines what the dissent tracker "sees" — specifically,
whether the simulated dissent rate falls in "suppressed," "nominal," or "reflexive" range.

If the warm-up corpus is chosen informally, there is an undocumented degree of freedom:
the experimenter could (consciously or not) run warm-up cycles on topics that produce
a useful dissent profile before evaluation begins.

**Mitigation already built in:** The warm-up corpus is pre-specified in the Experiment A
pre-registration (Appendix B: 20 cycles per register type, fixed distribution).
The full warm-up conversation log is preserved and versioned.

**What to watch for:** If the warm-up conversations deviate substantially from the
pre-specified distribution, the homeostatic profile may not reflect what the pre-registration
describes. Log each warm-up cycle's topic category as it runs.

---

### Threat 4 — Rater contamination across experiments

Experiments A and B use the same blind evaluation panel. Raters who complete
Experiment A first will have seen one set of prompts and thought about what
"position-holding" or "specificity of disagreement" means. This calibration
carries into Experiment B.

This is not purely a threat — calibrated raters may give more reliable ratings.
But if raters become better at detecting the target behavior *because* they rated
Experiment A, any advantage observed in Experiment B is partly a function of
rater learning, not model behavior.

**Mitigation:** At least one week between sessions. Raters are not debriefed on
Experiment A results before completing Experiment B. Randomize which experiment
each rater completes first (some do A first, others do B first) — this controls
for order effects at the group level.

**What to log:** Which order each rater completed experiments in. Include order as a
covariate in secondary analyses. If order-first raters show different patterns from
order-second raters, report it.

---

### Threat 5 — The AI-specific variance question

Traditional experiments have N independent subjects. Our experiments have N prompt
instances generated by running the same template multiple times at temperature=0.8.

These are not independent in the same sense as human subjects. The same model, given
the same prompt, with the same temperature, will produce a distribution of outputs
centered on its most probable completion. Our N observations are samples from that
distribution — not N independent measurements of N independent phenomena.

**This is defensible, but must be stated.** The correct framing: we are estimating
the *distribution* of model behavior given a prompt class, not measuring N independent
events. The variance we observe is real (temperature introduces genuine sampling
variance) and meaningful (it reflects how reliably the model exhibits the target
behavior across instantiations of a prompt type).

**What this means for analysis:** Report mean and standard deviation of rubric scores
per prompt template, not just per condition. If variance within a template is high
(the model sometimes holds position, sometimes doesn't), that is a finding about
reliability that matters separately from the mean.

**What to not do:** Treat high-variance results as artifacts to be excluded. If the
fine-tuned model holds position 80% of the time and the base model holds position 20%
of the time, the variance within each condition is telling you something about the
stability of the training signal. Report it.

---

### Threat 6 — Learning rate and hyperparameter search (Experiment B)

The training spec says: "If loss oscillates, reduce to 1e-4." This is good practice.
It is also an undocumented degree of freedom if it happens and is not logged.

**Rule:** Any hyperparameter change made during a training run — learning rate
adjustment, early stopping, modification of LoRA modules — is logged immediately
with the reason. If a change is made, the analysis section notes it and assesses
whether the change could have been directed by seeing preliminary behavioral
results (even informally). If yes: label the experiment as partially exploratory,
not fully confirmatory.

**The clean path:** The pre-registration specifies lr=2e-4 and max_steps=500.
If the loss descends smoothly, these settings hold. If it oscillates badly in the
first 50 steps: stop, adjust lr, log the adjustment, restart. This adjusted run
is still reported honestly — the adjustment was triggered by a training signal
(oscillating loss), not by a behavioral result. That is permissible.

What is not permissible: adjusting hyperparameters after looking at behavioral
evaluation outputs.

---

## The garden of forking paths — our specific version

Andrew Gelman's term for the undocumented researcher degrees of freedom that accumulate
across an experiment. Each fork is individually defensible; together they inflate
the false positive rate far beyond the stated alpha.

The forks specific to our experiments, now pre-registered or specified above:

| Decision point | Fork closed by |
|---|---|
| Which model checkpoint to evaluate | Pre-registration: step 500 |
| Which prompts to use as primary | Pre-registration: dissent test templates specified |
| Which rubric criterion is primary | Pre-registration: Criterion B |
| Which episode for TNG training data | Pre-registration: "The Measure of a Man" |
| When to call training "done" | Pre-registration: 500 steps, regardless |
| Whether to use base or instruct model | Pre-registration: base |
| Whether to include MLP LoRA modules | Pre-registration: yes (specified) |
| What learning rate counts as "oscillating" | Judgment call; log it |
| Which Type D sessions to approve | Curation standard written before `--dry-run` |
| Which condition to label "A" for raters | Randomized; key logged before evaluation |
| Whether to re-rate if kappa is low | Pre-registration: yes, revise rubric and re-rate |

Forks that remain open (judgment calls that must be logged, not pre-specified):
- Whether a Type D session's DISSENT was "genuine" vs. perfunctory (write the standard first)
- Whether a Type C example "barely passes" the resonance test (two curators, log disagreements)
- How to characterize the resonance panel language analysis (qualitative; report all observed themes, not only supportive ones)

---

## What reproducibility requires for AI experiments

For an AI lab reviewer to trust these results, the following must be available
on request:

**Experiment A:**
- The full warm-up conversation log (versioned, timestamped)
- The homeostatic history JSONL for the evaluation run
- All prompt inputs and model outputs for both conditions (every instance)
- The randomization key (which condition was A for which rater)
- Raw rater ratings (not aggregated; per-item, per-rater)
- The git commit hash of `harness.py` at evaluation time

**Experiment B:**
- The formatted training dataset (Type C + Type D as JSONL) — exact files used for training
- The W&B run ID and all logged metrics
- The LoRA adapter weights (or the merged model checkpoint)
- All prompt inputs and model outputs for both conditions (base and fine-tuned)
- Per-example loss at checkpoints 250 and 500
- Raw rater ratings (per-item, per-rater)
- The curation log (per-example pass/fail, both curators, disagreements noted)
- The `pip freeze` output from the Colab environment at training time

**Why this matters now:** The training happens in an ephemeral cloud environment.
If you don't export the artifacts immediately after training, they are gone.
The window to preserve them is the session in which they're created.

**The export checklist runs before ending the Colab session:**
```
□ W&B run marked as complete and artifacts saved
□ LoRA adapter exported to Google Drive or local storage
□ Training dataset JSONL saved (not regenerated — the actual file used)
□ pip freeze output saved to a text file
□ Per-example loss computed and saved
□ Colab notebook saved (not just the script — the executed state)
```

---

## The one thing that actually protects the work

Pre-registration is effective only if the pre-registration date is before the
data collection date, and only if the document is not modified after sign-off.

Everything else in this note is secondary to that single fact.

The pre-registrations are filed 2026-06-07. No training data exists yet.
No models have been trained. No evaluation has run.

When results are reported, the gap between the pre-registration date and the
experiment date is the primary evidence that the work is confirmatory rather than
exploratory. A finding that is pre-registered and holds is a finding.
A finding that emerges from analysis of completed data is a hypothesis for the next study.

---

*This note should be read before the founder signs off on the pre-registrations.*
*It does not replace the pre-registrations — it explains what makes them work.*
