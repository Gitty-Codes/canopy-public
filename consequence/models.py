# consequence/models.py
from dataclasses import dataclass, field
from typing import Optional


class TaskComplexity:
    SIMPLE_RETRIEVAL    = "simple_retrieval"
    CREATIVE            = "creative"
    MULTI_STEP_REASONING = "multi_step_reasoning"
    RELATIONAL          = "relational"
    EMOTIONAL           = "emotional"


class CommunicationRegister:
    FORMAL      = "formal"
    CASUAL      = "casual"
    DISTRESSED  = "distressed"
    EXPLORATORY = "exploratory"
    URGENT      = "urgent"


@dataclass
class DissentState:
    cycles_analyzed:      int   = 0
    dissent_count:        int   = 0
    dissent_rate:         float = 0.0
    acknowledgment_rate:  float = 0.0
    last_dissent_cycle:   Optional[int] = None
    status: str = "nominal"   # nominal | suppressed | reflexive | healthy


@dataclass
class ConstitutionalState:
    fidelity_flags: list = field(default_factory=list)
    tension_active: bool = False
    flag_count:     int  = 0


@dataclass
class HomeostaticStateSummary:
    # Level 1 — token budget
    token_budget_ratio: float = 0.0
    token_pressure:     str   = "nominal"   # nominal | warning | critical

    # Level 2 — dissent
    dissent: DissentState = field(default_factory=DissentState)

    # Level 3 — constitutional + classification
    constitutional:        ConstitutionalState = field(default_factory=ConstitutionalState)
    task_complexity:       list = field(default_factory=list)   # co-presence supported
    communication_register: str = "casual"

    # Hardware — logged but not injected into LLM in v1
    hardware_logged: bool = False

    # Versioning — every record carries these
    consequence_arch_version: str = ""
    quality_proxy_version:    str = ""
    system_prompt_version:    str = ""
    cycle_index: int = 0
    session_id:  str = ""
