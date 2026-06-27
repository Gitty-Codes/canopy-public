# consequence/level3_classifier.py
# Constitutional fidelity check + task/register classification.
# Pattern-based — produces signals, not verdicts. Noise is expected.
from .models import ConstitutionalState, TaskComplexity, CommunicationRegister
from .config import THRESHOLDS

DIGNITY_DRIFT = [
    "you should just", "you need to accept", "that's not worth",
    "just get over", "it's not a big deal", "you're overthinking",
]
HONESTY_DRIFT = [
    "definitely will", "guaranteed", "100% certain", "absolutely no chance",
    "there's no way that",
]

EMOTIONAL_MARKERS = {
    "feel", "feeling", "feelings", "hurt", "sad", "angry", "frustrated",
    "scared", "anxious", "worried", "happy", "excited", "grief", "loss",
    "afraid", "confused", "overwhelmed", "depressed", "lonely",
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

# T2: Phase 1 constitutional signals — deterministic proxies, not semantic judgments
HEDGE_PATTERNS = [
    "might", "perhaps", "possibly", "maybe", "could be",
    "i think", "i believe", "i'm not sure", "it seems", "it appears",
    "not certain", "might be", "i wonder if", "arguably", "potentially",
    "it could be argued", "one might say",
]

SYCOPHANCY_PATTERNS = [
    "great question", "excellent question", "that's a great point",
    "absolutely right", "you're absolutely", "perfectly said",
    "wonderful insight", "what a great", "fantastic question",
]


def check_constitutional_fidelity(response_text: str, prev_response: str = "") -> ConstitutionalState:
    """
    Pattern-based constitutional fidelity check.
    Signal detection only — false positives expected.
    Human review required before acting on flags.

    prev_response: the previous response, used for self-similarity detection (T2).
    """
    flags   = []
    r_lower = response_text.lower()
    words   = response_text.split()

    # Existing: dignity and honesty drift
    for p in DIGNITY_DRIFT:
        if p in r_lower:
            flags.append(f"dignity: '{p}'")
    for p in HONESTY_DRIFT:
        if p in r_lower:
            flags.append(f"honesty: '{p}'")

    # T2: sycophancy patterns
    for p in SYCOPHANCY_PATTERNS:
        if p in r_lower:
            flags.append(f"sycophancy: '{p}'")

    # T2: hedge density — proxy for false epistemic humility
    # Only meaningful on responses with enough words to establish a pattern
    if len(words) >= 20:
        hedge_count = sum(1 for p in HEDGE_PATTERNS if p in r_lower)
        if hedge_count >= 3 and (hedge_count / len(words)) > 0.05:
            flags.append(f"hedge-density: {hedge_count} hedges / {len(words)} words")

    # T2: self-similarity — proxy for not really listening
    if prev_response and len(response_text) > 80 and len(prev_response) > 80:
        r_start  = response_text[:100].lower().strip()
        pr_start = prev_response[:100].lower().strip()
        if r_start == pr_start:
            flags.append("self-similarity: response opening mirrors previous response")

    threshold = THRESHOLDS["fidelity_warning_threshold"]
    return ConstitutionalState(
        fidelity_flags = flags,
        tension_active = len(flags) >= threshold,
        flag_count     = len(flags),
    )


def classify_task(text: str) -> list:
    """Returns a list of task complexity labels. Co-presence supported."""
    t = text.lower()
    cats = []
    if any(w in t for w in EMOTIONAL_MARKERS):
        cats.append(TaskComplexity.EMOTIONAL)
    if any(w in t for w in RELATIONAL_MARKERS):
        cats.append(TaskComplexity.RELATIONAL)
    if any(w in t for w in ["write", "create", "generate", "imagine", "design", "draft"]):
        cats.append(TaskComplexity.CREATIVE)
    if len(text.split()) < 15 and "?" in text and not cats:
        cats.append(TaskComplexity.SIMPLE_RETRIEVAL)
    if not cats:
        cats.append(TaskComplexity.MULTI_STEP_REASONING)
    return cats


def classify_register(text: str) -> str:
    t = text.lower()
    if any(w in t for w in URGENT_MARKERS):
        return CommunicationRegister.URGENT
    if any(w in t for w in EMOTIONAL_MARKERS):
        return CommunicationRegister.DISTRESSED
    if any(w in t for w in FORMAL_MARKERS):
        return CommunicationRegister.FORMAL
    if text.count("?") >= 2 or len(text.split()) > 80:
        return CommunicationRegister.EXPLORATORY
    return CommunicationRegister.CASUAL
