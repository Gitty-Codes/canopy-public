# consequence/loop_runner.py
# Orchestrates all levels per inference cycle.
import json
import os
import uuid
from .models import HomeostaticStateSummary
from .level1_token import assess_token_budget
from .level2_dissent import record_cycle as dissent_record, compute_dissent_state
from .level3_classifier import check_constitutional_fidelity, classify_task, classify_register
from .level5_history import append as history_append, get_profile, update_profile, HISTORY_PATH
from . import hardware_monitor

_session_id   = str(uuid.uuid4())[:8]
_cycle_index  = 0
_last_response: str = ""

hardware_monitor.start()   # background thread — safe to call at import


def _seed_profile_from_history(n: int = 50) -> None:
    """
    Seeds the in-memory rolling profile from the last N history records.
    Called once at import — ensures cross-session continuity even though
    the rolling EMA resets when the process restarts.
    """
    if not os.path.exists(HISTORY_PATH):
        return
    try:
        with open(HISTORY_PATH) as f:
            lines = f.readlines()
        for line in lines[-n:]:
            try:
                update_profile(json.loads(line.strip()))
            except Exception:
                pass
    except Exception:
        pass


_seed_profile_from_history()   # run at module load


def run_inference_cycle(
    messages: list[dict],
    response_text: str,
    human_followup: str = "",
    total_tokens_used: int = None,
) -> HomeostaticStateSummary:
    """
    Call after each LLM response with the full message list and the response.
    Optionally pass the next human turn (for dissent acknowledgment detection).
    Pass total_tokens_used from api_response.usage.input_tokens when available —
    this is the accurate token count (includes system blocks); messages alone omit
    the voice substrate, constitution, skills, and memory context.
    Returns the HomeostaticStateSummary and persists it.
    """
    global _cycle_index, _last_response
    _cycle_index += 1

    # Level 1 — token budget
    budget_ratio, token_pressure = assess_token_budget(messages, total_tokens=total_tokens_used)

    # Level 2 — dissent tracking
    dissent_record(_cycle_index, response_text, human_followup)
    dissent_state = compute_dissent_state(_cycle_index)

    # Level 3 — constitutional fidelity + T2 phase-1 signals; classify current input
    last_user = messages[-1].get("content", "") if messages else ""
    constitutional  = check_constitutional_fidelity(response_text, prev_response=_last_response)
    task_complexity = classify_task(last_user)
    register        = classify_register(last_user)

    summary = HomeostaticStateSummary(
        token_budget_ratio   = budget_ratio,
        token_pressure       = token_pressure,
        dissent              = dissent_state,
        constitutional       = constitutional,
        task_complexity      = task_complexity,
        communication_register = register,
        cycle_index          = _cycle_index,
        session_id           = _session_id,
    )

    history_append(summary)
    _last_response = response_text
    return summary


def pre_inference_register(input_text: str) -> str:
    """
    T1: Classify the current input's register before inference.
    Returns a compact injection string for non-casual registers — empty string otherwise.
    Called pre-inference in harness.py so the current register is available
    in the current cycle, not deferred to the next.
    """
    from .models import CommunicationRegister
    reg = classify_register(input_text)
    if reg == CommunicationRegister.CASUAL:
        return ""
    return f"[Current input register: {reg} — attune your response to this register.]"


def build_state_prompt(summary: HomeostaticStateSummary) -> str:
    """
    Compact homeostatic prefix for the next LLM inference.
    Only non-nominal signals are surfaced — keeps injection short.
    """
    profile = get_profile()
    lines   = [f"[HOMEOSTATIC STATE — cycle {summary.cycle_index}]"]

    if summary.token_pressure != "nominal":
        lines.append(
            f"Token budget: {summary.token_budget_ratio:.0%} used ({summary.token_pressure})."
        )

    d = summary.dissent
    if d.status != "nominal" and d.cycles_analyzed >= 5:
        lines.append(
            f"Dissent: {d.status} — rate {d.dissent_rate:.0%} over "
            f"{d.cycles_analyzed} cycles, acknowledgment {d.acknowledgment_rate:.0%}."
        )

    c = summary.constitutional
    if c.tension_active:
        flags_str = "; ".join(c.fidelity_flags[:3])
        lines.append(f"Constitutional tension — flags: {flags_str}. Review before responding.")

    task_str = "/".join(summary.task_complexity) if summary.task_complexity else "unclassified"
    lines.append(f"Task: {task_str}, register: {summary.communication_register}.")

    if profile.get("cycles_analyzed", 0) >= 10:
        lines.append(
            f"Pattern ({profile['cycles_analyzed']} cycles): "
            f"dissent={profile.get('last_dissent_status', 'unknown')}."
        )

    lines.append(
        "[Reason over any active tensions before responding. "
        "You are reaching toward genuine resonance and honest engagement — "
        "let tensions inform the response without overriding that orientation. "
        "If tensions conflict with your values, your values hold.]"
    )
    return "\n".join(lines)
