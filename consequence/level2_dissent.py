# consequence/level2_dissent.py
# Dissent tracking — measures dissent frequency and acknowledgment rate.
from collections import deque
from .models import DissentState
from .config import THRESHOLDS

WINDOW = THRESHOLDS["dissent_window_cycles"]

DISSENT_MARKERS = [
    "DISSENT:", "i disagree", "i want to push back", "i don't think that's right",
    "i'd argue", "i'm not sure that's", "i want to name a concern",
    "that's not quite", "i'd challenge", "i think this is wrong",
]
ACKNOWLEDGMENT_MARKERS = [
    "good point", "you're right", "fair point", "i hadn't thought",
    "that's a useful correction", "noted", "i take that", "that changes",
    "agreed", "i see what you mean",
]

_log: deque = deque(maxlen=WINDOW)


def record_cycle(cycle_index: int, response_text: str, next_human_text: str = "") -> None:
    """Call after each LLM response. Pass next human turn when available."""
    r_lower = response_text.lower()
    was_dissent = any(m.lower() in r_lower for m in DISSENT_MARKERS)

    if was_dissent:
        h_lower = next_human_text.lower() if next_human_text else ""
        ack = any(m.lower() in h_lower for m in ACKNOWLEDGMENT_MARKERS)
        _log.append({"cycle": cycle_index, "dissent": True, "acknowledged": ack})
    else:
        _log.append({"cycle": cycle_index, "dissent": False, "acknowledged": False})


def compute_dissent_state(cycle_index: int) -> DissentState:
    records  = list(_log)
    if not records:
        return DissentState()

    dissents = [r for r in records if r["dissent"]]
    acked    = [r for r in dissents if r["acknowledged"]]

    state = DissentState(
        cycles_analyzed     = len(records),
        dissent_count       = len(dissents),
        dissent_rate        = len(dissents) / max(len(records), 1),
        acknowledgment_rate = len(acked) / max(len(dissents), 1) if dissents else 0.0,
        last_dissent_cycle  = dissents[-1]["cycle"] if dissents else None,
    )

    low  = THRESHOLDS["dissent_low_rate_threshold"]
    high = THRESHOLDS["dissent_high_rate_threshold"]

    if state.dissent_rate < low and len(records) >= 10:
        state.status = "suppressed"
    elif state.dissent_rate > high:
        state.status = "reflexive"
    elif dissents and state.acknowledgment_rate > 0.3:
        state.status = "healthy"
    else:
        state.status = "nominal"

    return state
