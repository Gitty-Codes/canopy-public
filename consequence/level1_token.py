# consequence/level1_token.py
# Token budget monitoring — lightweight, no subprocess, no latency cost.
from typing import Optional
from .config import THRESHOLDS

# tiktoken is optional — only used in the fallback path when the API hasn't
# returned a token count yet. The primary path uses api_response.usage.input_tokens
# directly, which is always more accurate (includes system blocks).
try:
    import tiktoken as _tiktoken
    _enc = _tiktoken.get_encoding("cl100k_base")
    def _count_tokens(messages: list[dict]) -> int:
        return sum(len(_enc.encode(m.get("content", ""))) for m in messages)
except ImportError:
    # Fallback: ~4 chars per token — rough but sufficient for pressure detection.
    # Install tiktoken for precise fallback counts: pip install tiktoken
    def _count_tokens(messages: list[dict]) -> int:
        return sum(len(m.get("content", "")) // 4 for m in messages)

TOKEN_BUDGET = THRESHOLDS["token_budget"]


def assess_token_budget(
    messages: list[dict],
    total_tokens: Optional[int] = None,
) -> tuple[float, str]:
    """
    Returns (ratio, pressure_level).
    ratio: 0.0–1.0, where 1.0 = budget exhausted.
    pressure_level: 'nominal' | 'warning' | 'critical'

    When total_tokens is provided (e.g. from api_response.usage.input_tokens),
    it is used directly — this is the accurate path, since it includes system
    blocks (voices, constitution, skills, memory) that messages alone omit.
    Falling back to counting messages is a rough proxy only.
    """
    if total_tokens is not None:
        count = total_tokens
    else:
        count = _count_tokens(messages)
    ratio = min(count / TOKEN_BUDGET, 1.0)

    if ratio >= THRESHOLDS["token_pressure_critical"]:
        pressure = "critical"
    elif ratio >= THRESHOLDS["token_pressure_warning"]:
        pressure = "warning"
    else:
        pressure = "nominal"

    return round(ratio, 3), pressure
