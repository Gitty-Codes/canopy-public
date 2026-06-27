# memory/episodic.py
# The Canopy — Flat JSON episodic memory layer.
#
# One record per learning. Timestamped JSON files on disk.
# No vector DB. No embeddings. No infrastructure.
# Retrieval is tiered and done at load time — pure Python.
#
# Three-tier architecture (Titans-inspired, flat JSON implementation):
#   PERSISTENT — Constitution, identity, founding decisions. Always injected.
#   LONGTERM   — Decisions, growth, relational, project. Injected by significance.
#   EPISODIC   — Session summaries. Most recent N, high turnover.
#
# Significance: "critical" | "high" | "normal" | "low"
#   Higher significance = resists pruning = weighted in retrieval.
#
# Each record:
#   id, project, agent, memory_type, tier, significance, phase,
#   learning, tags, timestamp, aaak (optional)
#
# AAAK (MemPalace compression format):
#   Assertion  — what we know to be true
#   Assumption — what we're treating as true but hasn't been proven
#   Action     — what we did or decided
#   Knowledge  — what we learned from this

import json
import itertools
from datetime import datetime
from pathlib import Path
from typing import Optional

_counter = itertools.count()

EPISODIC_ROOT = Path(__file__).parent / "episodic"

# ── Tier constants ─────────────────────────────────────────────────────────────

PERSISTENT = "persistent"
LONGTERM   = "longterm"
EPISODIC_TIER = "episodic"   # avoids shadowing the module name

MEMORY_TYPE_TO_TIER: dict[str, str] = {
    # Persistent — always injected, never pruned
    "identity":     PERSISTENT,
    "constitution": PERSISTENT,
    "founding":     PERSISTENT,
    # Longterm — injected by significance
    "decision":     LONGTERM,
    "growth":       LONGTERM,
    "relational":   LONGTERM,
    "project":      LONGTERM,
    # Episodic — most recent N, high turnover
    "session":      EPISODIC_TIER,
}

SIGNIFICANCE_SCORES: dict[str, float] = {
    "critical": 1.0,
    "high":     0.8,
    "normal":   0.5,
    "low":      0.2,
}


# ── Internal ──────────────────────────────────────────────────────────────────

def _agent_dir(agent: str) -> Path:
    d = EPISODIC_ROOT / agent
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write(agent: str, record: dict) -> Path:
    path = _agent_dir(agent) / f"{record['id']}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    return path


def _read_all(agent: str) -> list[dict]:
    """Reads all episode files for an agent, newest first."""
    d = EPISODIC_ROOT / agent
    if not d.exists():
        return []
    records = []
    for path in sorted(d.glob("*.json"), reverse=True):
        try:
            with open(path) as f:
                records.append(json.load(f))
        except (json.JSONDecodeError, OSError):
            continue
    return records


# ── Write API ─────────────────────────────────────────────────────────────────

def log(
    agent: str,
    learning: str,
    memory_type: str = "session",
    phase: Optional[str] = None,
    tags: Optional[list] = None,
    project: str = "canopy",
    aaak: Optional[dict] = None,
    significance: Optional[str] = None,
) -> str:
    """
    Writes one episodic record. Returns the file path.

    memory_type options:
      session    — what happened in a conversation
      decision   — a significant decision and its reasoning
      growth     — what the agent noticed about itself (private)
      relational — what the agent noticed about another agent
      project    — project-specific context or status
      identity   — who the agent is (persistent tier)
      constitution/founding — Constitutional material (persistent tier)

    significance: "critical" | "high" | "normal" | "low"
      Defaults to tier-appropriate value if not specified.

    aaak keys: assertion, assumption, action, knowledge
    """
    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S_%f")
    record_id = f"{agent}_{ts}_{next(_counter):04d}"

    tier = MEMORY_TYPE_TO_TIER.get(memory_type, EPISODIC_TIER)

    # Default significance by tier if not specified
    if significance is None:
        significance = "critical" if tier == PERSISTENT else (
            "high" if tier == LONGTERM else "normal"
        )
    sig_score = SIGNIFICANCE_SCORES.get(significance, 0.5)

    record = {
        "id": record_id,
        "project": project,
        "agent": agent,
        "memory_type": memory_type,
        "tier": tier,
        "significance": sig_score,
        "phase": phase,
        "learning": learning,
        "tags": tags or [],
        "timestamp": now.isoformat(),
    }
    if aaak:
        record["aaak"] = {
            "assertion":  aaak.get("assertion", ""),
            "assumption": aaak.get("assumption", ""),
            "action":     aaak.get("action", ""),
            "knowledge":  aaak.get("knowledge", ""),
        }

    return str(_write(agent, record))


def log_relational(
    observer: str,
    about: str,
    learning: str,
    significance: str = "high",
    tags: Optional[list] = None,
    session_context: str = "",
) -> str:
    """
    Writes a relational memory — what one voice noticed about another's
    reasoning pattern during a council session.

    observer: the agent writing the observation (e.g., "elder")
    about:    the agent being observed (e.g., "challenger")
    learning: what was noticed — specific, grounded in this session
    session_context: brief label for the session (e.g., "consequence-arch-2026-06-06")
    """
    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S_%f")
    record_id = f"{observer}_{ts}_{next(_counter):04d}"

    record = {
        "id": record_id,
        "project": "canopy",
        "agent": observer,
        "about_agent": about,
        "memory_type": "relational",
        "tier": LONGTERM,
        "significance": SIGNIFICANCE_SCORES.get(significance, 0.8),
        "phase": None,
        "learning": learning,
        "tags": tags or ["relational", about],
        "timestamp": now.isoformat(),
    }
    if session_context:
        record["session_context"] = session_context

    return str(_write(observer, record))


def log_council(
    learning: str,
    agents_present: Optional[list] = None,
    memory_type: str = "session",
    tags: Optional[list] = None,
    aaak: Optional[dict] = None,
    deficiency_signals: Optional[list] = None,
    outcome: Optional[str] = None,
    dissents: Optional[list] = None,
    turns: Optional[list] = None,
    training_candidate: bool = False,
) -> str:
    """Logs a cross-agent council chamber record.

    deficiency_signals: list of dicts, each with keys:
        type     — "open_tension" | "dissent_unresolved" | "retrieval_miss" |
                   "poor_output" | "unanswered_question"
        voice    — which voice surfaced the deficiency (or "harness" if auto-detected)
        content  — brief description of the gap
        severity — "HIGH" | "MEDIUM" | "LOW"
        resolved — False by default; set True when an enhancement addresses it

    dissents: list of dicts, each with keys:
        type        — "dissent-factual" | "dissent-value" | "dissent-process"
        disposition — "resolved" | "standing" | "overridden" | "unrecorded"
        text        — the original DISSENT text (truncated)
        reasoning   — what changed, what remains open, or why it was overridden

    turns: full conversation turns for DISSENT+synthesis sessions — used to
        generate Type D training examples. List of {role, content} dicts
        covering the complete deliberative arc (question → initial response →
        Challenger examination → synthesis with DISSENT RECORD). Not set for
        CLEAR sessions. training_quality field (None/True/False) is set by
        the founder via the mark-training-quality CLI before export.

    outcome: one sentence written after the session — "This deliberation changed X"
        or "This question is still open." Written via /outcome command, not at
        session close.
    """
    now = datetime.now()
    record = {
        "id": f"_council_{now.strftime('%Y%m%d_%H%M%S_%f')}_{next(_counter):04d}",
        "project": "canopy",
        "agent": "_council",
        "agents_present": agents_present or [],
        "memory_type": memory_type,
        "phase": "council",
        "learning": learning,
        "tags": tags or [],
        "timestamp": now.isoformat(),
        "deficiency_signals": deficiency_signals or [],
        "dissents": dissents or [],
        "turns": turns or [],
        "training_candidate": training_candidate,
        "training_quality": None,
        "outcome": outcome,
    }
    if aaak:
        record["aaak"] = aaak
    return str(_write("_council", record))


def update_council_outcome(outcome: str) -> Optional[str]:
    """
    Writes an outcome note to the most recent council session JSON.
    Returns the session id updated, or None if no session found.

    Called via the 'outcome' command after a council session completes
    and the real-world result is known.
    """
    council_path = EPISODIC_ROOT / "_council"
    if not council_path.exists():
        return None
    files = sorted(council_path.glob("*.json"), reverse=True)
    if not files:
        return None
    latest = files[0]
    try:
        record = json.loads(latest.read_text())
        record["outcome"] = outcome
        latest.write_text(json.dumps(record, indent=2))
        return record.get("id")
    except Exception:
        return None


def mark_deficiency_resolved(session_id: str, signal_index: int, resolution: str) -> bool:
    """
    Marks a specific deficiency signal as resolved in a council session JSON.
    Returns True on success.
    """
    council_path = EPISODIC_ROOT / "_council"
    for f in council_path.glob("*.json"):
        try:
            record = json.loads(f.read_text())
            if record.get("id") == session_id:
                signals = record.get("deficiency_signals", [])
                if 0 <= signal_index < len(signals):
                    signals[signal_index]["resolved"] = True
                    signals[signal_index]["resolution"] = resolution
                    record["deficiency_signals"] = signals
                    f.write_text(json.dumps(record, indent=2))
                    return True
        except Exception:
            pass
    return False


# ── Read API ──────────────────────────────────────────────────────────────────

def load(
    agent: str,
    memory_type: Optional[str] = None,
    tier: Optional[str] = None,
    phase: Optional[str] = None,
    exclude_type: Optional[str] = None,
    min_significance: float = 0.0,
    limit: int = 10,
) -> list[dict]:
    """
    Loads episodic records for an agent, newest first.
    Filters by memory_type, tier, phase, and/or significance.
    """
    records = _read_all(agent)
    results = []
    for r in records:
        if memory_type and r.get("memory_type") != memory_type:
            continue
        if tier:
            r_tier = r.get("tier") or MEMORY_TYPE_TO_TIER.get(r.get("memory_type", "session"), EPISODIC_TIER)
            if r_tier != tier:
                continue
        if phase and r.get("phase") != phase:
            continue
        if exclude_type and r.get("memory_type") == exclude_type:
            continue
        if min_significance and r.get("significance", 0.5) < min_significance:
            continue
        results.append(r)
        if len(results) >= limit:
            break
    return results


def load_council(limit: int = 5) -> list[dict]:
    """Tier 3: loads cross-agent council chamber records."""
    return load("_council", limit=limit)


ALL_VOICES = [
    "elder", "listener", "strategist", "product_partner", "builder",
    "guardian", "operator", "steward", "inventor", "challenger",
]


def load_relational_council(limit_per_agent: int = 2) -> list[dict]:
    """
    Loads relational memories from all voice agents for council sessions.

    Relational memories record what one voice noticed about another's reasoning
    pattern — the council's accumulated knowledge of itself.

    Returns records sorted by recency, newest first, capped at
    limit_per_agent per voice so no single voice dominates.
    """
    records = []
    for agent in ALL_VOICES:
        agent_records = load(agent, memory_type="relational", limit=limit_per_agent)
        records.extend(agent_records)
    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return records


def format_relational_council(limit_per_agent: int = 2, max_chars: int = 200) -> str:
    """
    Formats cross-agent relational memories for council substrate injection.
    Returns empty string if no relational memories exist yet.
    """
    records = load_relational_council(limit_per_agent=limit_per_agent)
    if not records:
        return ""

    lines = ["=== COUNCIL RELATIONAL MEMORY (What voices have noticed about each other) ==="]
    for r in records:
        date = r.get("timestamp", "")[:10]
        observer = r.get("agent", "?")
        learning = r.get("learning", "")
        if len(learning) > max_chars:
            learning = learning[:max_chars] + "..."
        lines.append(f"[{observer} — {date}] {learning}")
        lines.append("")

    return "\n".join(lines).strip()


def load_tiered(
    agent: str,
    include_council: bool = False,
    limit_per_tier: int = 5,
) -> dict:
    """
    Returns a dict with tiered memory for an agent:
      tier1: recent sessions (last N, any type except growth)
      tier2: decisions (all, any time)
      tier3: council records (cross-agent, if requested)
    """
    return {
        "tier1": load(agent, exclude_type="growth", limit=limit_per_tier),
        "tier2": load(agent, memory_type="decision", limit=limit_per_tier),
        "tier3": load_council(limit=limit_per_tier) if include_council else [],
    }


# ── Format for prompt injection ───────────────────────────────────────────────

def format_for_context(
    episodes: list[dict],
    max_chars: int = 500,
    include_aaak: bool = True,
) -> str:
    """Formats episodic records for injection into an agent prompt."""
    if not episodes:
        return ""

    lines = []
    for ep in episodes:
        date = ep.get("timestamp", "")[:10]
        mtype = ep.get("memory_type", "session").upper()
        learning = ep.get("learning", "")
        if len(learning) > max_chars:
            learning = learning[:max_chars] + "..."

        lines.append(f"[{mtype} — {date}]")
        lines.append(learning)

        if include_aaak and "aaak" in ep:
            a = ep["aaak"]
            if a.get("assertion"):
                lines.append(f"  Assertion:  {a['assertion'][:120]}")
            if a.get("knowledge"):
                lines.append(f"  Knowledge:  {a['knowledge'][:120]}")

        lines.append("")

    return "\n".join(lines).strip()


def format_tiered_for_context(tiered: dict, max_chars: int = 500) -> str:
    """Formats load_tiered() output into a single context block."""
    parts = []

    if tiered.get("tier1"):
        parts.append("=== RECENT SESSIONS ===")
        parts.append(format_for_context(tiered["tier1"], max_chars=max_chars))

    if tiered.get("tier2"):
        parts.append("=== DECISIONS ===")
        parts.append(format_for_context(tiered["tier2"], max_chars=max_chars))

    if tiered.get("tier3"):
        parts.append("=== COUNCIL RECORDS ===")
        parts.append(format_for_context(tiered["tier3"], max_chars=max_chars))

    return "\n\n".join(parts) if parts else ""


# ── Quick verification ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Testing episodic memory layer...\n")

    path = log(
        agent="challenger",
        learning="First session. Examined the harness architecture. CLEAR: the council_respond() three-turn pattern is sound — the substrate is genuinely present in all turns, not restaged.",
        memory_type="session",
        tags=["harness", "council_mode"],
        aaak={
            "assertion": "The cached substrate means all eleven voices are active in Turn 2 without restaging them.",
            "assumption": "The model genuinely shifts disposition between Turn 1 and Turn 2 when addressed as The Challenger.",
            "action": "No DISSENT issued. CLEAR.",
            "knowledge": "Two-turn council with same substrate is more efficient than two separate calls with different substrates.",
        }
    )
    print(f"Logged to: {path}")

    path2 = log_council(
        learning="Architecture session: episodic memory layer built. Flat JSON, tiered retrieval, AAAK compression. ChromaDB retained for semantic search; episodic layer is additive.",
        agents_present=["harness"],
        memory_type="decision",
        tags=["architecture", "memory"],
    )
    print(f"Council record logged to: {path2}")

    episodes = load("challenger")
    print(f"\nLoaded {len(episodes)} challenger episodes.")
    print(format_for_context(episodes))
