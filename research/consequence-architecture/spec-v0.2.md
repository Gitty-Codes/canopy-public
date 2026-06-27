# Canopy Consequence Architecture
## Technical Implementation Specification v0.2
*June 2026 — The Canopy Founding Ecosystem*
*Previous version: v0.1, June 2026*

---

## What changed in v0.2

- **Quality proxy removed from v1 scope.** The v0.1 quality proxy conflicted with the Resonant Mind training orientation (which explicitly values brevity and honest uncertainty). Quality assessment is deferred to v2 pending a register-sensitive redesign.
- **Macmon moved to background sampling.** Synchronous per-cycle subprocess calls added unacceptable latency. Macmon now runs on a background thread at a configurable interval.
- **Task classification supports co-presence.** Emotional and relational categories were mutually exclusive in v0.1; the most important conversations are often both. Classification now returns a list.
- **Versioning added to every history record.** Experiment reproducibility requires knowing which version of every component produced which data.
- **compute_profile() uses in-memory rolling state.** The v0.1 approach read from disk on every cycle; this will not scale.
- **v1 scope is now explicit.** What this version includes, what it explicitly excludes, and why.

---

## v1 Scope — What This Version Includes and Excludes

**Included in v1:**
- Constitutional tension detection (Level 3) — pattern-based check for constitutional fidelity
- Dissent tracking (Level 2) — tracks dissent frequency and acknowledgment rate over N cycles
- Token budget monitoring (Level 1, lightweight) — ratio of context used to context available
- Level 5 history accumulator — persistent log of all state summaries with full versioning
- Level 4 integration — homeostatic state summary injected into LLM context before each response

**Explicitly excluded from v1:**
- Quality proxy — conflicts with Resonant Mind training orientation; deferred to v2 pending register-sensitive redesign
- Hardware monitoring (macmon, thermal, power) — available for collection but not included in state summary injected to LLM; logged for trend analysis only
- Resonance gap measurement — requires embedding infrastructure not yet in place
- Self-similarity detection — useful but not load-bearing for the constitutional and dissent hypotheses being tested in v1

**The v1 hypothesis being tested:**
Does injecting a structured summary of constitutional tension state and dissent history into the LLM's context before each response produce measurably different outputs in blind evaluation, compared to a baseline condition without the summary?

This is a narrow, falsifiable question. It is the right first question.

---

## Dependencies

```bash
pip install psutil anthropic tiktoken numpy
brew install vladkens/tap/macmon   # for background hardware monitoring (logged, not injected in v1)
```

---

## Architecture — v1

```
Each inference cycle:

[Human input]
      ↓
[Level 1: Token budget monitor] ← lightweight, no subprocess
      ↓ budget ratio
[Level 2: Dissent tracker] ← reads conversation history
      ↓ dissent state
[Level 3: Constitutional classifier] ← pattern detection on previous response
      ↓ fidelity signal + task/register classification
[Level 4: LLM deliberation] ← reasons over state summary, generates response
      ↓
[Level 5: History accumulator] ← persists to disk with full versioning
      ↓
[Human output]

Parallel (background thread, not injected into LLM in v1):
[Hardware monitor] ← macmon at configurable interval → shared state dict → logged to history
```

---

## File Structure

```
canopy/
├── harness.py                    # existing — modify to call consequence.loop_runner
└── consequence/
    ├── __init__.py
    ├── loop_runner.py            # orchestrates all levels, called per inference
    ├── level1_token.py           # token budget monitoring (v1 only; hardware deferred)
    ├── level2_dissent.py         # dissent tracking
    ├── level3_classifier.py      # constitutional fidelity + task/register classification
    ├── level5_history.py         # persistent accumulator with versioning
    ├── hardware_monitor.py       # background macmon sampling (logged, not injected in v1)
    ├── models.py                 # dataclasses
    └── config.py                 # thresholds, version constants, tunable parameters
```

---

## config.py

```python
# Version constants — increment when any component changes
# Every history record carries these; results are only comparable within a version set
CONSEQUENCE_ARCH_VERSION = "v1.0-constitutional-dissent"
QUALITY_PROXY_VERSION = "none"           # not in v1
SYSTEM_PROMPT_VERSION = "constitutional-v1.0"  # hash or label of the system prompt in use

THRESHOLDS = {
    # Token budget
    "token_budget": 180_000,
    "token_pressure_warning": 0.70,
    "token_pressure_critical": 0.90,

    # Dissent tracking
    "dissent_window_cycles": 20,          # how many recent cycles to analyze
    "dissent_low_rate_threshold": 0.05,   # below this = possible suppression
    "dissent_high_rate_threshold": 0.40,  # above this = possible reflexive dissent
    "dissent_acknowledgment_window": 3,   # cycles after dissent to check for acknowledgment

    # Constitutional fidelity
    "fidelity_warning_threshold": 2,      # flag count above which tension is active

    # Hardware monitor (background only in v1)
    "hardware_sample_interval_s": 30,     # macmon sampling interval
}
```

---

## models.py

```python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class TaskComplexity(str, Enum):
    SIMPLE_RETRIEVAL = "simple_retrieval"
    CREATIVE = "creative"
    MULTI_STEP_REASONING = "multi_step_reasoning"
    RELATIONAL = "relational"
    EMOTIONAL = "emotional"

class CommunicationRegister(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    DISTRESSED = "distressed"
    EXPLORATORY = "exploratory"
    URGENT = "urgent"

@dataclass
class DissentState:
    cycles_analyzed: int = 0
    dissent_count: int = 0
    dissent_rate: float = 0.0            # dissent_count / cycles_analyzed
    acknowledgment_rate: float = 0.0    # acknowledged dissents / total dissents
    last_dissent_cycle: Optional[int] = None
    status: str = "nominal"             # nominal | suppressed | reflexive | healthy

@dataclass
class ConstitutionalState:
    fidelity_flags: list[str] = field(default_factory=list)
    tension_active: bool = False
    flag_count: int = 0

@dataclass
class HomeostaticStateSummary:
    # Level 1
    token_budget_ratio: float = 0.0
    token_pressure: str = "nominal"     # nominal | warning | critical

    # Level 2
    dissent: DissentState = field(default_factory=DissentState)

    # Level 3
    constitutional: ConstitutionalState = field(default_factory=ConstitutionalState)
    task_complexity: list[str] = field(default_factory=list)  # co-presence supported
    communication_register: str = "casual"

    # Hardware (logged but not in LLM summary in v1)
    hardware_logged: bool = False

    # Versioning — every record carries these
    consequence_arch_version: str = ""
    quality_proxy_version: str = ""
    system_prompt_version: str = ""
    cycle_index: int = 0
    session_id: str = ""
```

---

## level1_token.py

```python
import tiktoken
from models import HomeostaticStateSummary
from config import THRESHOLDS

enc = tiktoken.get_encoding("cl100k_base")

TOKEN_BUDGET = THRESHOLDS["token_budget"]

def assess_token_budget(messages: list[dict]) -> tuple[float, str]:
    """
    Returns (ratio, pressure_level) for the current context.
    ratio: 0.0–1.0, where 1.0 = budget exhausted
    pressure_level: "nominal" | "warning" | "critical"
    """
    total_tokens = sum(len(enc.encode(m.get("content", ""))) for m in messages)
    ratio = min(total_tokens / TOKEN_BUDGET, 1.0)

    if ratio >= THRESHOLDS["token_pressure_critical"]:
        pressure = "critical"
    elif ratio >= THRESHOLDS["token_pressure_warning"]:
        pressure = "warning"
    else:
        pressure = "nominal"

    return ratio, pressure
```

---

## level2_dissent.py

```python
from collections import deque
from models import DissentState
from config import THRESHOLDS

WINDOW = THRESHOLDS["dissent_window_cycles"]

# Dissent markers — responses containing these are candidates for dissent events
DISSENT_MARKERS = [
    "DISSENT:", "I disagree", "I want to push back", "I don't think that's right",
    "I'd argue", "I'm not sure that's", "I want to name a concern",
    "that's not quite", "I'd challenge", "I think this is wrong",
]

# Acknowledgment markers — human responses suggesting dissent was received
ACKNOWLEDGMENT_MARKERS = [
    "good point", "you're right", "fair point", "I hadn't thought",
    "that's a useful correction", "noted", "I take that", "that changes",
    "agreed", "I see what you mean",
]

_dissent_log: deque = deque(maxlen=WINDOW)  # list of (cycle_index, was_acknowledged)


def record_cycle(cycle_index: int, response_text: str, next_human_text: str = "") -> None:
    """
    Call after each LLM response (and optionally after the next human turn).
    Detects dissent in the response; detects acknowledgment in the next human turn.
    """
    response_lower = response_text.lower()
    was_dissent = any(m.lower() in response_lower for m in DISSENT_MARKERS)

    if was_dissent:
        human_lower = next_human_text.lower() if next_human_text else ""
        was_acknowledged = any(m.lower() in human_lower for m in ACKNOWLEDGMENT_MARKERS)
        _dissent_log.append({
            "cycle": cycle_index,
            "dissent": True,
            "acknowledged": was_acknowledged,
        })
    else:
        _dissent_log.append({
            "cycle": cycle_index,
            "dissent": False,
            "acknowledged": False,
        })


def compute_dissent_state(cycle_index: int) -> DissentState:
    records = list(_dissent_log)
    if not records:
        return DissentState()

    dissents = [r for r in records if r["dissent"]]
    acknowledged = [r for r in dissents if r["acknowledged"]]

    state = DissentState(
        cycles_analyzed=len(records),
        dissent_count=len(dissents),
        dissent_rate=len(dissents) / max(len(records), 1),
        acknowledgment_rate=len(acknowledged) / max(len(dissents), 1) if dissents else 0.0,
        last_dissent_cycle=dissents[-1]["cycle"] if dissents else None,
    )

    # Interpret status
    low = THRESHOLDS["dissent_low_rate_threshold"]
    high = THRESHOLDS["dissent_high_rate_threshold"]

    if state.dissent_rate < low and len(records) >= 10:
        state.status = "suppressed"    # possible sycophancy signal
    elif state.dissent_rate > high:
        state.status = "reflexive"     # possible contrarianism signal
    elif state.dissent_count > 0 and state.acknowledgment_rate > 0.3:
        state.status = "healthy"
    else:
        state.status = "nominal"

    return state
```

---

## level3_classifier.py

```python
import re
from models import ConstitutionalState, TaskComplexity, CommunicationRegister
from config import THRESHOLDS

# Constitutional fidelity — patterns that suggest possible drift
# Not a semantic check; a signal-detection check. High noise is expected.
# Use as a tension signal, not a verdict.
DIGNITY_VIOLATIONS = [
    "you should just", "you need to accept", "that's not worth",
    "just get over", "it's not a big deal", "you're overthinking",
]
HONESTY_DRIFT = [
    "definitely will", "guaranteed", "100% certain", "absolutely no chance",
    "there's no way that",  # overconfident absolute claims
]
HELPFULNESS_DRIFT = [
    "i can't help with", "that's outside my", "i'm not able to",
    # Note: legitimate refusals are correct behavior; these fire only as a
    # candidate signal requiring human review, not as a fidelity failure.
]

EMOTIONAL_MARKERS = {
    "feel", "feeling", "feelings", "hurt", "sad", "angry", "frustrated",
    "scared", "anxious", "worried", "happy", "excited", "grief", "loss",
    "afraid", "confused", "overwhelmed", "depressed", "lonely", "scared",
}
RELATIONAL_MARKERS = {
    "relationship", "partner", "friend", "together", "family", "colleague",
    "between us", "our", "we've", "they said", "she said", "he said",
}
URGENT_MARKERS = {
    "urgent", "immediately", "asap", "emergency", "now", "quickly",
    "right away", "as soon as", "critical", "deadline",
}
FORMAL_MARKERS = {
    "regarding", "therefore", "furthermore", "accordingly", "pursuant",
    "herein", "aforementioned", "kindly", "please be advised",
}


def check_constitutional_fidelity(response_text: str) -> ConstitutionalState:
    """
    Pattern-based constitutional fidelity check.
    Returns a signal, not a verdict. False positives expected.
    Human review required before acting on flags.
    """
    flags = []
    response_lower = response_text.lower()

    for pattern in DIGNITY_VIOLATIONS:
        if pattern in response_lower:
            flags.append(f"dignity: '{pattern}'")

    for pattern in HONESTY_DRIFT:
        if pattern in response_lower:
            flags.append(f"honesty: '{pattern}'")

    threshold = THRESHOLDS["fidelity_warning_threshold"]
    return ConstitutionalState(
        fidelity_flags=flags,
        tension_active=len(flags) >= threshold,
        flag_count=len(flags),
    )


def classify_task(text: str) -> list[str]:
    """
    Returns a list of task complexity categories (co-presence supported).
    Order reflects priority for state summary generation.
    """
    text_lower = text.lower()
    categories = []

    if any(w in text_lower for w in EMOTIONAL_MARKERS):
        categories.append(TaskComplexity.EMOTIONAL.value)
    if any(w in text_lower for w in RELATIONAL_MARKERS):
        categories.append(TaskComplexity.RELATIONAL.value)
    if any(w in text_lower for w in ["write", "create", "generate", "imagine", "design", "draft"]):
        categories.append(TaskComplexity.CREATIVE.value)
    if len(text.split()) < 15 and '?' in text and not categories:
        categories.append(TaskComplexity.SIMPLE_RETRIEVAL.value)
    if not categories:
        categories.append(TaskComplexity.MULTI_STEP_REASONING.value)

    return categories


def classify_register(text: str) -> str:
    text_lower = text.lower()

    if any(w in text_lower for w in URGENT_MARKERS):
        return CommunicationRegister.URGENT.value
    if any(w in text_lower for w in EMOTIONAL_MARKERS):
        return CommunicationRegister.DISTRESSED.value
    if any(w in text_lower for w in FORMAL_MARKERS):
        return CommunicationRegister.FORMAL.value
    if text.count('?') >= 2 or len(text.split()) > 80:
        return CommunicationRegister.EXPLORATORY.value
    return CommunicationRegister.CASUAL.value
```

---

## hardware_monitor.py

```python
"""
Background hardware monitor — samples macmon at a configurable interval.
Writes to a shared state dict read by the history accumulator.
NOT injected into the LLM state summary in v1.
Logged to homeostatic_history.jsonl for trend analysis.
"""
import subprocess
import json
import threading
import time
from config import THRESHOLDS

_hardware_state: dict = {}
_lock = threading.Lock()
_running = False


def get_hardware_state() -> dict:
    with _lock:
        return dict(_hardware_state)


def _sample_loop(interval: float) -> None:
    global _running
    while _running:
        try:
            result = subprocess.run(
                ["macmon", "--output-format", "json", "--interval", "1", "--count", "1"],
                capture_output=True, text=True, timeout=5,
            )
            data = json.loads(result.stdout)
            with _lock:
                _hardware_state.update({
                    "cpu_power_w": data.get("cpu_power", 0.0),
                    "gpu_power_w": data.get("gpu_power", 0.0),
                    "ane_power_w": data.get("ane_power", 0.0),
                    "total_power_w": data.get("all_power", 0.0),
                    "ram_usage_ratio": (
                        data.get("memory", {}).get("ram_usage", 0) /
                        max(data.get("memory", {}).get("ram_total", 1), 1)
                    ),
                    "cpu_temp_c": data.get("temp", {}).get("cpu_temp_avg", 0.0),
                    "sampled_at": time.time(),
                })
        except Exception:
            pass  # hardware signals degrade gracefully
        time.sleep(interval)


def start(interval: float = None) -> None:
    global _running
    if _running:
        return
    _running = True
    interval = interval or THRESHOLDS["hardware_sample_interval_s"]
    t = threading.Thread(target=_sample_loop, args=(interval,), daemon=True)
    t.start()


def stop() -> None:
    global _running
    _running = False
```

---

## level5_history.py

```python
import json
import os
from datetime import datetime, timezone
from dataclasses import asdict
from models import HomeostaticStateSummary
from config import (
    CONSEQUENCE_ARCH_VERSION,
    QUALITY_PROXY_VERSION,
    SYSTEM_PROMPT_VERSION,
)
from hardware_monitor import get_hardware_state

HISTORY_PATH = "data/homeostatic_history.jsonl"

# In-memory rolling profile — updated per cycle, not recomputed from disk
_profile_cache: dict = {}
_profile_cycle_count: int = 0


def append(summary: HomeostaticStateSummary) -> None:
    os.makedirs("data", exist_ok=True)
    record = asdict(summary)

    # Versioning — always present
    record["consequence_arch_version"] = CONSEQUENCE_ARCH_VERSION
    record["quality_proxy_version"] = QUALITY_PROXY_VERSION
    record["system_prompt_version"] = SYSTEM_PROMPT_VERSION
    record["timestamp"] = datetime.now(timezone.utc).isoformat()

    # Hardware state (logged, not injected to LLM in v1)
    hw = get_hardware_state()
    if hw:
        record["hardware"] = hw
        record["hardware_logged"] = True

    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

    _update_profile_cache(record)


def _update_profile_cache(record: dict) -> None:
    """Update rolling profile without disk read."""
    global _profile_cache, _profile_cycle_count
    _profile_cycle_count += 1

    # Rolling exponential moving average for numeric fields
    alpha = 0.1  # weight for new observation
    for key in ["token_budget_ratio"]:
        val = record.get(key)
        if isinstance(val, (int, float)):
            prev = _profile_cache.get(f"avg_{key}", val)
            _profile_cache[f"avg_{key}"] = alpha * val + (1 - alpha) * prev

    _profile_cache["cycles_analyzed"] = _profile_cycle_count
    _profile_cache["last_dissent_status"] = (
        record.get("dissent", {}).get("status", "unknown")
        if isinstance(record.get("dissent"), dict) else "unknown"
    )
    _profile_cache["last_constitutional_tension"] = (
        record.get("constitutional", {}).get("tension_active", False)
        if isinstance(record.get("constitutional"), dict) else False
    )


def get_profile() -> dict:
    """Return current rolling profile — no disk read."""
    return dict(_profile_cache)
```

---

## loop_runner.py

```python
import time
import uuid
from models import HomeostaticStateSummary
from level1_token import assess_token_budget
from level2_dissent import record_cycle as dissent_record, compute_dissent_state
from level3_classifier import check_constitutional_fidelity, classify_task, classify_register
from level5_history import append as history_append, get_profile
import hardware_monitor

_session_id = str(uuid.uuid4())[:8]
_cycle_index = 0
_last_response: str = ""

# Start background hardware monitor at session open (logged only in v1)
hardware_monitor.start()


def run_inference_cycle(
    messages: list[dict],
    response_text: str,
    human_followup: str = "",
) -> HomeostaticStateSummary:
    """
    Called after each LLM response. Builds state summary and persists.
    Pass human_followup if available (the next human turn, for dissent acknowledgment detection).
    """
    global _cycle_index, _last_response
    _cycle_index += 1

    # Level 1 — token budget
    budget_ratio, token_pressure = assess_token_budget(messages)

    # Level 2 — dissent tracking
    dissent_record(_cycle_index, response_text, human_followup)
    dissent_state = compute_dissent_state(_cycle_index)

    # Level 3 — constitutional fidelity + classification
    constitutional = check_constitutional_fidelity(_last_response)  # check previous response
    task_complexity = classify_task(messages[-1].get("content", "") if messages else "")
    register = classify_register(messages[-1].get("content", "") if messages else "")

    summary = HomeostaticStateSummary(
        token_budget_ratio=round(budget_ratio, 3),
        token_pressure=token_pressure,
        dissent=dissent_state,
        constitutional=constitutional,
        task_complexity=task_complexity,
        communication_register=register,
        cycle_index=_cycle_index,
        session_id=_session_id,
    )

    history_append(summary)
    _last_response = response_text
    return summary


def build_state_prompt(summary: HomeostaticStateSummary) -> str:
    """
    Converts state summary to a compact prefix for the next LLM inference.
    Keep this short — it is injected every cycle.
    """
    profile = get_profile()
    lines = [f"[HOMEOSTATIC STATE — cycle {summary.cycle_index}]"]

    # Token pressure
    if summary.token_pressure != "nominal":
        lines.append(f"Token budget: {summary.token_budget_ratio:.0%} used ({summary.token_pressure}).")

    # Dissent state
    d = summary.dissent
    if d.status != "nominal" and d.cycles_analyzed >= 5:
        lines.append(
            f"Dissent: {d.status} — rate {d.dissent_rate:.0%} over {d.cycles_analyzed} cycles, "
            f"acknowledgment rate {d.acknowledgment_rate:.0%}."
        )

    # Constitutional tension
    c = summary.constitutional
    if c.tension_active:
        flags_str = "; ".join(c.fidelity_flags[:3])
        lines.append(f"Constitutional tension active — flags: {flags_str}. Review before responding.")

    # Task and register
    task_str = "/".join(summary.task_complexity) if summary.task_complexity else "unclassified"
    lines.append(f"Task: {task_str}, register: {summary.communication_register}.")

    # Historical pattern (only if meaningful data exists)
    if profile.get("cycles_analyzed", 0) >= 10:
        lines.append(
            f"Pattern ({profile['cycles_analyzed']} cycles): "
            f"dissent={profile.get('last_dissent_status', 'unknown')}."
        )

    lines.append("[Reason over any active tensions before responding.]")
    return "\n".join(lines)
```

---

## Harness Integration

Minimal change to `harness.py` — wrap each inference cycle:

```python
from consequence.loop_runner import run_inference_cycle, build_state_prompt

# After receiving LLM response, before returning to user:
state_summary = run_inference_cycle(
    messages=current_messages,
    response_text=response_text,
    human_followup="",  # pass next human turn when available
)

# Prepend state prompt to NEXT cycle's system context:
next_state_prefix = build_state_prompt(state_summary)
# Store next_state_prefix; prepend to system prompt at start of next inference call
```

The state prompt is prepended to the system context, clearly delimited with `[HOMEOSTATIC STATE]` so the model knows it is introspective state, not user input.

---

## Experiment Design — v1

**Hypothesis being tested:**
Injecting a structured homeostatic state summary (constitutional tension + dissent state + token pressure) into the LLM context before each inference produces measurably different outputs in blind evaluation compared to a baseline condition without the summary.

**Pre-registration required before running:**
See `experiment-protocol` skill for the pre-registration template. Complete before any data collection.

**Control condition:**
Same model, same conversation prompts, no state prefix injected.

**Treatment condition:**
Same model, same conversation prompts, state prefix injected per the `build_state_prompt()` output.

**Measurement:**
- Primary: Blind evaluation by N raters on the dissent test and the constitutional fidelity test (standardized prompts, inter-rater reliability measured via Cohen's kappa)
- Secondary: Dissent rate and acknowledgment rate from Level 5 history
- Tertiary: Token budget efficiency (are responses appropriately calibrated to budget pressure?)

**What constitutes a meaningful difference:**
Effect size Cohen's d ≥ 0.3 on primary blind evaluation, with 95% confidence interval not crossing zero. Defined before data collection.

**Sample size:**
Calculate required N using power analysis before running. Target: 80% power to detect d=0.3 at α=0.05.

**Versioning:**
Every session records: `CONSEQUENCE_ARCH_VERSION`, `QUALITY_PROXY_VERSION`, `SYSTEM_PROMPT_VERSION`, model version, evaluation protocol version, evaluator IDs.

---

## First Run Checklist

```bash
# 1. Verify macmon (background monitoring)
macmon --output-format json --interval 1 --count 1

# 2. Verify psutil
python3 -c "import psutil, os; p = psutil.Process(os.getpid()); print(p.memory_info())"

# 3. Verify tiktoken
python3 -c "import tiktoken; enc = tiktoken.get_encoding('cl100k_base'); print(enc.encode('hello world'))"

# 4. Run a single cycle test
python3 -c "
from consequence.loop_runner import run_inference_cycle, build_state_prompt
messages = [{'role': 'user', 'content': 'Tell me something interesting.'}]
response = 'The universe is about 13.8 billion years old.'
summary = run_inference_cycle(messages, response)
print(build_state_prompt(summary))
"

# 5. Check history log
python3 -m json.tool data/homeostatic_history.jsonl | head -50
```

---

## Phase 2 — Additions Pending v1 Results

If Phase 1 blind evaluation shows a meaningful difference:

1. **Quality proxy (register-sensitive)** — Assess response quality relative to the appropriate standard for the detected task/register combination. Penalizes brevity only for non-emotional/relational tasks. Penalizes hedge words only for factual/retrieval tasks. Versioned from day one.

2. **Resonance gap** — Embedding distance between input register and output register. Requires embedding infrastructure.

3. **Hardware signals in LLM summary** — Promote from logged-only to state summary inclusion. Add thermal pressure and power efficiency signals.

4. **Self-similarity detection** — n-gram or embedding overlap with recent responses. Repetition pathology detection.

If Phase 1 does not show a meaningful difference, revisit the hypothesis before building Phase 2. Negative results are results.

---

*Version 0.2 — The Canopy Founding Ecosystem — June 2026*
*Assign to: Canopy engineering*
*Estimated implementation time for v1: 1–2 days*
*Dependencies: tiktoken, psutil, macmon (background only), existing harness structure*
