# privacy/__init__.py
# The Canopy — Privacy module public surface.
#
# Four-tier classification: Public → Operational → Sensitive → Protected.
# Classification sits above task routing — happens before any model call.
# Protected data never leaves the local machine. No exceptions.

from .classifier import (
    classify,
    classify_inputs,
    is_cloud_allowed,
    requires_audit,
    memory_write_allowed,
    cloud_requires_explicit_consent,
    max_tier,
    tier_rank,
    PUBLIC,
    OPERATIONAL,
    SENSITIVE,
    PROTECTED,
    TIER_DESCRIPTIONS,
)
from .audit import write_audit, read_audit_log, audit_summary
