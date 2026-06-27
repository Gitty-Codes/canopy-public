# models/router.py
# The Canopy — Model router.
#
# Single source of truth for model selection and tier routing.
# Model choice is a cost/capability decision, not a values decision.
# The Constitutional substrate and dignity principles travel with every
# call regardless of which tier is selected.
#
# Three tiers:
#   HAIKU  — high-volume, structured, template-driven, retrieval-based tasks.
#             ~20x cheaper than Sonnet. Use when the output is deterministic
#             and full deliberation is not required.
#   SONNET — judgment-heavy, narrative, strategic, deliberative tasks.
#             Default tier. Use for council, respond, focused calls.
#   OPUS   — highest-stakes reasoning. Commission explicitly — never default.
#             Reserved for: irreversible decisions, Constitutional amendments,
#             founder-level governance questions.
#
# Routing rules (current):
#   council (all turns)    → SONNET  — deliberation requires full capability;
#                                       downgrading examination risks missing flaws
#   respond / focused      → SONNET
#   task profiles          → task declares tier in frontmatter (haiku|sonnet|opus);
#                            defaults to SONNET when absent — harness never silently
#                            downgrades without explicit task permission
#   future ambient/batch   → HAIKU candidates once those modes exist

import os

HAIKU  = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"
OPUS   = "claude-opus-4-7"

# CANOPY_DEV=1 forces all calls to Haiku (~20x cheaper than Sonnet).
# Set this in your local environment when testing. Never set in production.
_DEV_MODE = bool(os.environ.get("CANOPY_DEV"))

DEFAULT_MODEL = HAIKU if _DEV_MODE else SONNET

# Maps task profile frontmatter values → model strings.
# Task profiles declare:  model: haiku | sonnet | opus
TIER_MAP = {"haiku": HAIKU, "sonnet": SONNET, "opus": OPUS}


def select_model(mode: str, task_tier: str | None = None) -> str:
    """
    Returns the appropriate model string for a given call mode.

    mode options:
      "respond"             — default single-call respond()
      "council"             — council_respond() turns 1, 2, 3
      "focused"             — respond_focused() domain call
      "task"                — run_task(); task_tier from profile frontmatter
      "opus"                — explicit Opus commission (founder must pass this)

    task_tier: tier string from task profile ("haiku" | "sonnet" | "opus").
               Only consulted when mode="task". Ignored for all other modes.

    CANOPY_DEV=1 overrides all routing to Haiku.
    """
    if _DEV_MODE:
        return HAIKU
    if mode == "opus":
        return OPUS
    if mode == "task" and task_tier:
        return TIER_MAP.get(task_tier.lower(), SONNET)
    return SONNET
