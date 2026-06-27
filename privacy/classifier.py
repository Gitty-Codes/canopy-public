# privacy/classifier.py
# The Canopy — Data Classification
#
# Four tiers: Public, Operational, Sensitive, Protected.
# Classification happens before any model call — it is a gate, not a suggestion.
#
# Conservative by design: when uncertain, errs toward higher sensitivity.
# Org-supplied data is almost never truly Public until explicitly confirmed.
#
# Pattern libraries are a starting point. Real classifications require
# a conversation with each organization — see PRIVACY_MANIFEST.md.

import re
from typing import Optional

# ── Classification tiers ──────────────────────────────────────────────────────

PUBLIC      = "public"
OPERATIONAL = "operational"
SENSITIVE   = "sensitive"
PROTECTED   = "protected"

# Ordered lowest → highest sensitivity. Do not reorder.
TIER_ORDER = [PUBLIC, OPERATIONAL, SENSITIVE, PROTECTED]

TIER_DESCRIPTIONS = {
    PUBLIC:      "Information the org has already made public or would freely share.",
    OPERATIONAL: "Internal working info that is not sensitive but is not public.",
    SENSITIVE:   "Information about identifiable individuals or confidential org matters.",
    PROTECTED:   "Legally regulated or highest-sensitivity data — minors, health, financial identity.",
}


def tier_rank(tier: str) -> int:
    """Integer rank for comparison. Higher = more sensitive."""
    try:
        return TIER_ORDER.index(tier)
    except ValueError:
        return TIER_ORDER.index(SENSITIVE)  # unknown string → treat as Sensitive


def max_tier(*tiers: str) -> str:
    """Returns the most sensitive tier from a set."""
    return max(tiers, key=tier_rank)


# ── Pattern libraries ─────────────────────────────────────────────────────────
#
# Protected: minors, student records, health information, financial identity.
# Legal frameworks: COPPA (minors under 13), FERPA (student records), HIPAA (health).

_PROTECTED_PATTERNS = [
    # Minors and student records
    r"\bIEP\b", r"\b504\s+plan\b", r"\bspecial\s+education\b",
    r"\bunder\s+13\b", r"\bunder\s+thirteen\b",
    r"\bstudent\s+record", r"\bstudent\s+information\b", r"\bstudent\s+data\b",
    r"\bchild\s+record", r"\bCOPPA\b", r"\bFERPA\b",
    r"\bminor\b(?!\s+issue)",  # "minor" but not "minor issue"

    # Health and HIPAA adjacent
    r"\bHIPAA\b", r"\bhealth\s+record", r"\bmedical\s+record",
    r"\bdiagnosis\b", r"\bprescription\b", r"\btreatment\s+plan",
    r"\bmental\s+health\b", r"\btherapist\b", r"\bcounselor\b",
    r"\bdisability\b", r"\baccommodation\b", r"\b504\b",

    # Financial identity
    r"\bSSN\b", r"\bsocial\s+security\s+number",
    r"\baccount\s+number\b", r"\brouting\s+number\b",
    r"\bcredit\s+card\b", r"\bbank\s+account\b",
    r"\bEIN\b",
]

# Sensitive: named individuals, donor specifics, staff data, org confidential.
# These require explicit org awareness before cloud processing.

_SENSITIVE_PATTERNS = [
    # Donor information
    r"\bdonor\b", r"\bgiving\s+history\b", r"\bgift\s+amount\b",
    r"\bpledge\b", r"\bmajor\s+gift\b", r"\bplanned\s+giving\b",
    r"\bDAF\b", r"\bdonor[- ]advised\b",
    r"\$\s*\d[\d,]*",  # dollar amounts

    # Staff and employment
    r"\bsalary\b", r"\bwage\b", r"\bcompensation\b",
    r"\bstaff\b.{0,30}\bpersonal\b", r"\bemployment\s+record",
    r"\bperformance\s+review", r"\bPTO\b", r"\bbenefits\s+package\b",
    r"\btermination\b", r"\bresignation\b", r"\bpayroll\b",

    # Financial records (non-identity)
    r"\bfinancial\s+statement", r"\baudited\s+financials",
    r"\bbudget\b.{0,30}\bconfidential\b", r"\bdeficit\b",
    r"\bcash\s+flow\b",

    # Grant pre-disclosure
    r"\bgrant\s+application\b", r"\bLOI\b.{0,30}\bdraft\b",
    r"\bpending\s+grant\b", r"\bgrant\s+pending\b",
    r"\bunannounced\s+grant\b",

    # Board personal
    r"\bboard\s+member\b.{0,30}\bpersonal\b",
    r"\bdirector\b.{0,30}\baddress\b", r"\bdirector\b.{0,30}\bphone\b",

    # Explicit confidentiality markers
    r"\bconfidential\b", r"\bnot\s+for\s+distribution\b",
    r"\binternal\s+only\b", r"\bdo\s+not\s+share\b",
    r"\bprivate\b.{0,30}\bstrategy\b",
]

# Operational: internal working information — not sensitive, not public.
# Fine for cloud with standard protections.

_OPERATIONAL_PATTERNS = [
    r"\bgrant\s+deadline\b", r"\bsubmission\s+deadline\b",
    r"\bmeeting\s+notes\b", r"\bboard\s+agenda\b",
    r"\bcampaign\s+plan\b", r"\bworkplan\b",
    r"\bstaff\s+meeting\b", r"\bplanning\s+session\b",
    r"\binternal\b", r"\bdraft\b",
]


def _matches_any(text: str, patterns: list) -> bool:
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False


def classify(text: str, override: Optional[str] = None) -> str:
    """
    Classifies a text string into: public, operational, sensitive, protected.

    Conservative: errs toward higher sensitivity when uncertain.
    Default for unclassified text is OPERATIONAL — org data is almost never
    truly Public without explicit confirmation.

    override: caller-asserted classification. Validated against known tiers;
              unknown values default to SENSITIVE.
    """
    if override is not None:
        return override if override in TIER_ORDER else SENSITIVE

    if _matches_any(text, _PROTECTED_PATTERNS):
        return PROTECTED

    if _matches_any(text, _SENSITIVE_PATTERNS):
        return SENSITIVE

    if _matches_any(text, _OPERATIONAL_PATTERNS):
        return OPERATIONAL

    return OPERATIONAL  # Unclassified org content defaults to Operational


def classify_inputs(inputs: dict, override: Optional[str] = None) -> str:
    """
    Classifies the combined user-supplied inputs for a run_task() call.
    Returns the highest tier found across all string values.
    """
    if override is not None:
        return classify("", override=override)

    tiers = [classify(str(v)) for v in inputs.values() if v is not None]
    if not tiers:
        return OPERATIONAL

    return max(tiers, key=tier_rank)


# ── Routing decisions ─────────────────────────────────────────────────────────

def is_cloud_allowed(tier: str) -> bool:
    """
    Protected data must never leave the local machine.
    All other tiers may use cloud with appropriate handling.
    """
    return tier_rank(tier) < tier_rank(PROTECTED)


def requires_audit(tier: str) -> bool:
    """Sensitive and Protected requests require an audit record."""
    return tier_rank(tier) >= tier_rank(SENSITIVE)


def memory_write_allowed(tier: str) -> bool:
    """
    Protected data must not be written to persistent memory.
    Sensitive: allowed but caller should confirm intent.
    """
    return tier_rank(tier) < tier_rank(PROTECTED)


def cloud_requires_explicit_consent(tier: str) -> bool:
    """
    Sensitive data requires the caller to explicitly acknowledge that
    cloud processing is appropriate (e.g., by setting privacy_class="sensitive"
    rather than relying on auto-classification).
    """
    return tier == SENSITIVE
