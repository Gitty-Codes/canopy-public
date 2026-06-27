---
name: experiment-protocol
type: playbook
scope: meta
invocation: on-demand
description: Pre-registration, inter-rater reliability, power analysis, and results reporting for Canopy research experiments — PhD-defensible rigor for AI science
---

# Experiment Protocol — Research Rigor Playbook

The Canopy is building things that may be interesting to AI labs and to the field.
That means the work must be defensible: pre-registered hypotheses, honest reporting,
reproducible methods, and results that include null findings.

This skill runs at two moments: before an experiment (pre-registration) and after
(results reporting). Do not skip pre-registration. A hypothesis written after seeing
the data is not a hypothesis — it is a narrative.

---

## Before the Experiment — Pre-Registration

Complete this document before any data collection. Store it in the experiment directory
with a datestamp. Do not modify it after data collection begins.

```markdown
# Experiment Pre-Registration
Date: [YYYY-MM-DD]
Experiment: [name]
Versions: [consequence_arch_version, model_version, eval_protocol_version, etc.]

## Hypothesis
[One specific, falsifiable statement. What does the architecture predict?
 Not "we expect improvement" — what kind, how large, on what measure?]

## Control condition
[Exactly what the control group sees/does. Enough detail to reproduce.]

## Treatment condition
[Exactly what the treatment group sees/does. Enough detail to reproduce.]

## Primary outcome measure
[The single number or rating that determines whether the hypothesis is supported.
 How is it computed? By whom?]

## Secondary outcome measures
[Other things being measured. Must be declared before data collection.]

## Success criterion
[What constitutes a meaningful difference? State effect size and confidence interval
 threshold before seeing data. e.g., Cohen's d ≥ 0.3, 95% CI not crossing zero.]

## Sample size
[N determined by power analysis. See power analysis section below.
 Do not adjust N after seeing preliminary results.]

## Evaluator protocol
[How evaluators are recruited. What they are told and not told.
 How inter-rater reliability is measured.]

## What constitutes a null result
[Be specific. If the data looks like X, the hypothesis is not supported.]
```

---

## Power Analysis — Before You Collect Data

Power analysis answers: how many observations do we need to detect a real difference?

Run before data collection. The standard settings for most Canopy experiments:

- **Target effect size:** Cohen's d = 0.3 (small-medium; meaningful but conservative)
- **Power:** 0.80 (80% chance of detecting the effect if it's real)
- **Alpha:** 0.05 (5% chance of false positive)

```python
# Minimal power analysis — install scipy first
from scipy import stats
import numpy as np

def required_n(effect_size_d=0.3, power=0.80, alpha=0.05):
    """
    Returns required N per group for a two-sample t-test.
    For paired designs, N is total pairs needed.
    """
    from scipy.stats import norm
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    n = ((z_alpha + z_beta) / effect_size_d) ** 2
    return int(np.ceil(n))

n = required_n()
print(f"Required N per condition: {n}")
# For d=0.3, power=0.80, alpha=0.05: ~88 per condition
```

For blind evaluation studies (human raters):

```python
# For inter-rater agreement target kappa >= 0.6 (substantial agreement):
# Minimum 30 items per rater, minimum 2 raters, minimum 2 independent rating passes.
# Rule of thumb: 50 items per rater gives reliable kappa estimates.
```

If you cannot reach the required N, either:
- Accept lower power and report it honestly (note this limits conclusions)
- Reduce the target effect size (weakens the claim you can support)
- Report the study as exploratory (no confirmatory claims)

Never adjust N upward after looking at preliminary results. That inflates false positive rate.

---

## Inter-Rater Reliability Protocol

For qualitative evaluations (wandering test, dissent test, blind resonance panel):

**Setup:**
1. Write standardized prompts before recruiting evaluators
2. Recruit evaluators who have not seen the outputs they will rate
3. Provide evaluators with a rubric (specific criteria, not just "which is better")
4. Have each evaluator rate independently before comparing

**Rubric format:**
```
Item: [output to evaluate]
Rate each criterion 1–5:
  Criterion A: [specific observable behavior]
  Criterion B: [specific observable behavior]
  Criterion C: [specific observable behavior]
Notes: [anything the rating doesn't capture]
```

**Measure agreement:**
```python
from sklearn.metrics import cohen_kappa_score
import numpy as np

rater_1 = [3, 4, 2, 5, 3, ...]   # ratings from rater 1
rater_2 = [3, 4, 3, 4, 2, ...]   # ratings from rater 2

kappa = cohen_kappa_score(rater_1, rater_2)
print(f"Cohen's kappa: {kappa:.3f}")
# Interpretation: < 0.2 = poor, 0.2–0.4 = fair, 0.4–0.6 = moderate,
#                 0.6–0.8 = substantial, > 0.8 = almost perfect
# Target: kappa >= 0.6 before treating the evaluation as reliable
```

If kappa < 0.4: the rubric is unclear, or the phenomenon being rated is too ambiguous.
Revise the rubric and re-rate before proceeding. Do not average low-agreement ratings.

---

## Statistical Analysis — After Data Collection

```python
import numpy as np
from scipy import stats

def analyze_two_conditions(control: list, treatment: list, label: str = "outcome"):
    """
    Basic analysis for two conditions. Report all of these, not just p-value.
    """
    c = np.array(control)
    t = np.array(treatment)

    # Descriptive
    print(f"\n{label}")
    print(f"  Control:   mean={c.mean():.3f}, SD={c.std():.3f}, N={len(c)}")
    print(f"  Treatment: mean={t.mean():.3f}, SD={t.std():.3f}, N={len(t)}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((c.std()**2 + t.std()**2) / 2)
    d = (t.mean() - c.mean()) / max(pooled_std, 0.001)
    print(f"  Cohen's d: {d:.3f}")

    # Statistical test
    # Use Wilcoxon signed-rank for paired; Mann-Whitney for independent
    stat, p = stats.mannwhitneyu(t, c, alternative='two-sided')
    print(f"  Mann-Whitney U: p={p:.4f}")

    # Confidence interval on the difference
    diff = t.mean() - c.mean()
    se = np.sqrt(c.var()/len(c) + t.var()/len(t))
    ci_low = diff - 1.96 * se
    ci_high = diff + 1.96 * se
    print(f"  95% CI on difference: [{ci_low:.3f}, {ci_high:.3f}]")

    # Interpretation
    if p < 0.05 and abs(d) >= 0.3 and ci_low * ci_high > 0:
        print(f"  Conclusion: SUPPORTED — effect is statistically significant and meets pre-registered threshold")
    elif p < 0.05:
        print(f"  Conclusion: PARTIAL — statistically significant but effect size below threshold (d={d:.3f})")
    else:
        print(f"  Conclusion: NOT SUPPORTED — null result")
```

---

## Results Reporting Template

```markdown
# Experiment Results
Date: [YYYY-MM-DD]
Pre-registration: [link to pre-registration document]
Versions: [same as pre-registration — must match]

## What we predicted
[Copy hypothesis from pre-registration verbatim]

## What we measured
[Control N=X, Treatment N=Y. Primary measure: [description].]

## What we found
[Paste analysis output. State effect size, confidence interval, p-value.
 Do not state p < 0.05 without also stating the effect size.]

## Conclusion
[Supported / Partially supported / Not supported — match to the pre-registered criterion]

## What this changes
[If supported: what does this mean for the next phase?
 If not supported: what does this mean for the hypothesis? What would we change?]

## Limitations
[What this study cannot tell us. What alternative explanations exist for the result?]

## Open questions
[What would we want to know next?]
```

**Mandatory rule:** Null results get the same reporting template as positive results.
If we only publish positive results, the work is not science.

---

## Versioning Discipline

Every experiment record must carry:

```python
# Experiment A (Consequence Architecture)
EXPERIMENT_RECORD_A = {
    "experiment_id": "consequence-arch-v1-001",
    "date": "YYYY-MM-DD",
    "pre_registration_date": "2026-06-07",   # must be BEFORE data collection
    "versions": {
        "canopy": "main@[git-hash]",         # covers voices + constitution implicitly
        "consequence_arch": "v1.0-constitutional-dissent",
        "quality_proxy": "none",
        "model": "claude-sonnet-4-6",
        "system_prompt": "constitutional-v1.0",
        "eval_protocol": "v1.0-blind-dissent",
        "hardware": "m2-8gb-macos14",
    },
    "evaluators": ["evaluator-a", "evaluator-b"],   # anonymized IDs
    "rater_order": {"evaluator-a": "exp-a-first", "evaluator-b": "exp-b-first"},
    "kappa_criterion_b": 0.0,   # fill before analysis
    "N_control": 88,
    "N_treatment": 88,
    "primary_outcome": {},
    "secondary_outcomes": {},
    "conclusion": "supported | partial | not supported",
}

# Experiment B (Resonant Mind) — adds training environment fields
EXPERIMENT_RECORD_B = {
    "experiment_id": "resonant-mind-v1-001",
    "date": "YYYY-MM-DD",
    "pre_registration_date": "2026-06-07",
    "versions": {
        "canopy": "main@[git-hash]",
        "base_model": "Qwen/Qwen2.5-7B",
        "unsloth_version": "[from pip freeze]",
        "cuda_version": "[from Colab runtime]",
        "colab_gpu": "A100-40GB",
        "training_steps": 500,
        "lora_rank": 16,
        "lora_alpha": 32,
        "learning_rate": "2e-4",
        "training_dataset_hash": "[sha256 of training JSONL]",
        "n_examples_type_c": 0,   # fill at curation time
        "n_examples_type_d": 0,
        "checkpoint_evaluated": "step-500",
        "gguf_quantization": "Q4_K_M",
        "ollama_version": "[from ollama --version]",
        "system_prompt": "constitutional-v1.0",
        "eval_protocol": "v1.0-resonant-mind",
        "hardware_inference": "m2-8gb-macos14",
    },
    "evaluators": ["evaluator-a", "evaluator-b"],
    "rater_order": {"evaluator-a": "exp-a-first", "evaluator-b": "exp-b-first"},
    "kappa_criterion_b": 0.0,
    "N_control": 88,
    "N_treatment": 88,
    "primary_outcome": {},
    "secondary_outcomes": {},
    "conclusion": "supported | partial | not supported",
}
```

Results from different versions are not comparable without explicit version-alignment.
When a component version changes, start a new experiment series.

---

## What Rigor Looks Like to an AI Lab

AI labs review work against these standards:
- Falsifiable hypothesis stated before results are known
- Control condition that isolates the variable being tested
- Blind evaluation (raters don't know which condition is which)
- Effect sizes reported (not just p-values)
- Null results published, not suppressed
- Methods sufficient to reproduce the experiment
- Claims scoped to what the evidence supports (functional language, not phenomenal)

The Canopy adds one more: version control on every component so the conditions
that produced the result can be precisely reconstructed.
