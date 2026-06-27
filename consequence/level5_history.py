# consequence/level5_history.py
# Persistent accumulator — append-only JSONL, in-memory rolling profile.
import hashlib
import json
import os
from datetime import datetime, timezone
from dataclasses import asdict
from .models import HomeostaticStateSummary
from .config import CONSEQUENCE_ARCH_VERSION, QUALITY_PROXY_VERSION, SYSTEM_PROMPT_VERSION
from .hardware_monitor import get as hw_get

HISTORY_PATH = "data/homeostatic_history.jsonl"


def _compute_constitution_hash() -> str:
    """Short hash of the active constitution — changes when the document changes."""
    try:
        with open("constitution/cultural-constitution.md", "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:8]
    except Exception:
        return "unknown"


_CONSTITUTION_HASH = _compute_constitution_hash()

_profile: dict = {}
_cycle_count: int = 0


def append(summary: HomeostaticStateSummary, curator_note: str = "") -> None:
    os.makedirs("data", exist_ok=True)
    record = asdict(summary)

    # Versioning — always present so results stay comparable across experiments
    record["consequence_arch_version"] = CONSEQUENCE_ARCH_VERSION
    record["quality_proxy_version"]    = QUALITY_PROXY_VERSION
    record["system_prompt_version"]    = SYSTEM_PROMPT_VERSION
    record["timestamp"]                = datetime.now(timezone.utc).isoformat()

    # T4: experiment-level tags — makes history interpretable across checkpoints
    record["training_checkpoint"] = os.getenv("CANOPY_TRAINING_CHECKPOINT", "")
    record["constitution_hash"]   = _CONSTITUTION_HASH
    record["curator_note"]        = curator_note or os.getenv("CANOPY_CURATOR_NOTE", "")

    hw = hw_get()
    if hw:
        record["hardware"]        = hw
        record["hardware_logged"] = True

    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

    _update_profile(record)


def update_profile(record: dict) -> None:   # public alias for cross-session seeding
    _update_profile(record)


def _update_profile(record: dict) -> None:
    global _cycle_count
    _cycle_count += 1
    alpha = 0.1   # exponential moving average weight for new observation

    for key in ["token_budget_ratio"]:
        val = record.get(key)
        if isinstance(val, (int, float)):
            prev = _profile.get(f"avg_{key}", val)
            _profile[f"avg_{key}"] = alpha * val + (1 - alpha) * prev

    _profile["cycles_analyzed"] = _cycle_count
    _profile["last_dissent_status"] = (
        record.get("dissent", {}).get("status", "unknown")
        if isinstance(record.get("dissent"), dict) else "unknown"
    )
    _profile["last_constitutional_tension"] = (
        record.get("constitutional", {}).get("tension_active", False)
        if isinstance(record.get("constitutional"), dict) else False
    )


def get_profile() -> dict:
    return dict(_profile)
