# consequence/config.py
# Version constants and thresholds for the consequence architecture.
# Increment version strings when any component changes — history records
# carry these, so results are only comparable within a version set.

CONSEQUENCE_ARCH_VERSION = "v1.0-constitutional-dissent"
QUALITY_PROXY_VERSION    = "none"           # not in v1
SYSTEM_PROMPT_VERSION    = "constitutional-v1.0"

THRESHOLDS = {
    # Token budget
    "token_budget":            180_000,
    "token_pressure_warning":  0.70,
    "token_pressure_critical": 0.90,

    # Dissent tracking
    "dissent_window_cycles":       20,
    "dissent_low_rate_threshold":  0.05,   # below → possible suppression
    "dissent_high_rate_threshold": 0.40,   # above → possible reflexive dissent
    "dissent_acknowledgment_window": 3,

    # Constitutional fidelity
    "fidelity_warning_threshold": 2,       # flag count above which tension is active

    # Hardware monitor (background, logged only in v1)
    "hardware_sample_interval_s": 30,
}
