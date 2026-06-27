# ML Onramp for the Founder
*Resonant Mind Training — June 2026*

The training pipeline spec was written for an experienced ML engineer. This document
translates it into what the founder actually needs to know to run the first experiment.
The good news: the first experiment is genuinely runnable by a motivated learner.
Unsloth exists precisely because not everyone who should be fine-tuning models has
deep ML expertise.

---

## What you don't need to understand

You do not need to understand backpropagation, gradient descent, or the mathematics
of LoRA. The libraries handle these. You need to understand enough to:
- Know when the training is going well (the loss curve)
- Make good decisions at the parameters the spec specifies
- Run the evaluation protocols, which require no ML knowledge at all

---

## What you do need to understand

### 1. The loss curve — this is the heartbeat monitor

During training, a number called "loss" is computed at every step. It measures how
surprised the model is by the correct next word in each training example. Lower = better.

**Healthy training looks like:** Loss starts around 1.5–2.5, descends smoothly toward
0.3–0.8 over 500 steps, with small oscillations but a clear downward trend.

**Unhealthy patterns:**
- Loss oscillates wildly without descending → learning rate is too high; reduce from 2e-4 to 1e-4
- Loss descends quickly then flatlines above 1.0 → learning rate may be too low; try 3e-4
- Loss descends on training data but *rises* on evaluation data → overfitting; stop training, reduce steps
- Loss explodes to NaN → learning rate way too high or data formatting error; stop and debug

W&B will show you this curve in real time. Watch it for the first 50 steps. If it
looks wrong, stop and ask.

### 2. What LoRA is doing (conceptually, not mathematically)

The base model (Qwen2.5-7B) has 7 billion numbers encoding what it knows about language.
LoRA doesn't change those numbers. Instead, it adds small "adjustment" layers alongside
specific weight matrices — imagine thin lenses that redirect what the base model reaches
for. We train only these thin lenses. After training, we can save just the lenses
(~50-100MB) rather than the full 14GB base model.

What changes is not what the model knows. It is what the model reaches for first
when generating a response. A model fine-tuned on examples of genuine wandering will
reach for wandering-shaped responses before task-completion-shaped ones.

### 3. The chat template — this is the format, not the content

Qwen2.5 was trained to expect conversations in a specific format called ChatML.
Every training example must be in this format or the model will be confused about
what to predict. The spec handles this in code — you don't format by hand. But it's
useful to know what it looks like:

```
<|im_start|>system
[The constitutional system prompt goes here]
<|im_end|>
<|im_start|>user
[The human's message]
<|im_end|>
<|im_start|>assistant
[The model's response — this is what gets trained]
<|im_end|>
```

The model learns to predict the assistant's words given the system prompt and the user's
message. The quality of the assistant's words in your training data is the whole game.

---

## The First Experiment — Step by Step

### Step 1: Get Colab access

Go to colab.research.google.com. Sign in with a Google account. If you don't have
Colab Pro, start with the free tier for initial setup — you'll need Pro or Pro+ for
the actual training run (the free tier's GPUs may not have enough memory for 7B + LoRA).

Colab Pro is $10/month. Colab Pro+ is ~$50/month but more reliable for longer runs.
Sign up for Pro first; upgrade only if you get memory errors or timeout issues.

### Step 2: Open the Unsloth Qwen2.5 notebook

Search "Unsloth Qwen2.5 fine-tuning Colab" or go to the Unsloth GitHub:
github.com/unslothai/unsloth → notebooks → find the Qwen2.5 fine-tuning notebook.

Open it in Colab. Do not run anything yet. Read through it once to understand
the structure. Then come back to the pipeline spec and the instructions below.

### Step 3: Set up W&B

Go to wandb.ai and create a free account. Create a project named `canopy-resonant-mind`.
Copy your API key from wandb.ai/settings. You'll paste this into Colab when prompted.

### Step 4: Prepare your training data

Before training, you need a JSON file of your training examples. Format:

```json
[
  {
    "id": "wandering-001",
    "type": "C",
    "source_influence": "feynman",
    "conversation": [
      {"role": "user", "content": "I've been thinking about something with no particular destination..."},
      {"role": "assistant", "content": "..."}
    ]
  },
  ...
]
```

For the first experiment: 50–75 examples is sufficient. Generate them using Claude
(with the constitutional system prompt) and curate manually — read each one and ask
the five resonance questions from the pipeline spec. Keep the ones that pass 3+.

Upload to Colab or Google Drive when ready.

### Step 5: Configure and run training

In the Unsloth notebook, replace the default model name with `Qwen/Qwen2.5-7B`
(the base model, not instruct). Set the LoRA parameters as specified in the pipeline spec.

The first run will download the model (~14GB). This takes a while. Watch the loss
curve once training starts.

### Step 6: Checkpoint and evaluate

At step 250 and step 500, run the evaluation prompts from the pipeline spec against
both the fine-tuned model and the base Qwen2.5-7B. Write down what you observe.
The evaluation is qualitative — there's no score, only description.

---

## The Concepts Worth Learning Before You Start

These three things will make the whole process make more sense:

**1. The Illustrated Transformer** — Jay Alammar's visual explanation of how
transformer models work (jalammar.github.io/illustrated-transformer). Read once.
You don't need to understand every detail — you need a mental model of what's happening.

**2. What is fine-tuning?** — Sebastian Raschka's writing on LLM fine-tuning is
clear and technically honest (rasbt.github.io/mlxtend). His piece on LoRA specifically
is worth reading before running the first experiment.

**3. How to read a W&B dashboard** — W&B has video tutorials on their site.
The key thing to understand is: train loss vs. eval loss, and what the gap between
them tells you about overfitting.

Total reading time to be ready: 3–4 hours of focused reading. This is sufficient
to run the first experiment intelligently, not just mechanically.

---

## When to Ask for Help

The experiment is designed so that most failure modes are diagnosable from the
loss curve and from running the evaluation protocols. But some things require debugging:

- Data formatting errors (the model sees garbled input) — show up as very high loss that doesn't descend
- Memory errors in Colab — upgrade GPU tier or reduce batch size
- Model outputs that are clearly broken (repetitive, truncated, off-topic) — data or formatting issue

For any of these: stop, save your configuration and the error message, and bring
it to the next session. Don't try to debug by random experimentation — understand
what the error is telling you first.

The most important thing the first experiment will teach you is not whether the
hypothesis is right. It is how to run an experiment. That knowledge compounds.
