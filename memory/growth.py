# memory/growth.py
# The Canopy — Voice growth protocol.
#
# Voices grow by writing growth memories (memory_type="growth").
# When enough have accumulated to indicate genuine development —
# dispositions refined, failure patterns named, scope clarified —
# the Steward initiates a growth review and proposes an amendment.
#
# The protocol:
#   1. Assess — read growth memories, compare against current definition
#   2. Review — Steward + council examine the gap
#   3. Lock — current definition moved to _history/ before any change
#   4. Amend — new definition written with growth integrated
#   5. Record — amendment logged to decisions-log and semantic memory
#
# Self-modification without deliberation is the most dangerous failure mode.
# This protocol enforces deliberation before any voice definition changes.

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.episodic import load

VOICES_ACTIVE   = Path(__file__).parent.parent / "constitution" / "voices" / "v2_compressed"
VOICES_HISTORY  = Path(__file__).parent.parent / "constitution" / "voices" / "_history"
DECISIONS_LOG   = Path(__file__).parent.parent / "constitution" / "decisions-log"
GROWTH_LOG      = Path(__file__).parent / "growth_log.json"

GROWTH_THRESHOLD = 3  # minimum growth memories before a review is warranted
VALID_AGENTS = [
    "elder", "listener", "strategist", "product_partner", "builder",
    "guardian", "operator", "steward", "inventor", "challenger",
]


# ── File helpers ───────────────────────────────────────────────────────────────

def _voice_file(agent: str) -> Path:
    name = agent
    # Handle underscore names
    candidates = [
        VOICES_ACTIVE / f"{agent}.md",
        VOICES_ACTIVE / f"{agent.replace('_', '_')}.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return VOICES_ACTIVE / f"{agent}.md"


def _read_voice(agent: str) -> str:
    path = _voice_file(agent)
    if path.exists():
        return path.read_text()
    return ""


def _amendment_count(agent: str) -> int:
    """Counts prior amendments for this agent from the history directory."""
    VOICES_HISTORY.mkdir(parents=True, exist_ok=True)
    return len(list(VOICES_HISTORY.glob(f"{agent}_locked_*.md")))


# ── Assessment ─────────────────────────────────────────────────────────────────

def assess_voice_growth(agent: str) -> dict:
    """
    Reads a voice's growth memories and current definition.
    Returns structured data for the Steward's review.
    Does not modify anything — read-only.
    """
    if agent not in VALID_AGENTS:
        raise ValueError(f"Unknown agent: {agent}. Valid: {VALID_AGENTS}")

    growth_memories = load(agent, memory_type="growth", exclude_type=None, limit=100)
    current_definition = _read_voice(agent)
    prior_amendments = _amendment_count(agent)
    threshold_met = len(growth_memories) >= GROWTH_THRESHOLD

    return {
        "agent": agent,
        "growth_memory_count": len(growth_memories),
        "threshold_met": threshold_met,
        "threshold": GROWTH_THRESHOLD,
        "prior_amendments": prior_amendments,
        "current_definition": current_definition,
        "growth_memories": growth_memories,
        "assessed_at": datetime.now().isoformat(),
    }


def all_voices_assessment() -> list[dict]:
    """Surveys all voices and returns lightweight assessment for each."""
    results = []
    for agent in VALID_AGENTS:
        memories = load(agent, memory_type="growth", exclude_type=None, limit=100)
        results.append({
            "agent": agent,
            "growth_memory_count": len(memories),
            "threshold": GROWTH_THRESHOLD,
            "threshold_met": len(memories) >= GROWTH_THRESHOLD,
            "prior_amendments": _amendment_count(agent),
        })
    return sorted(results, key=lambda x: -x["growth_memory_count"])


# ── Versioning ─────────────────────────────────────────────────────────────────

def lock_voice_version(agent: str, notes: str = "") -> Path:
    """
    Copies the current active voice definition to _history/ before amendment.
    Returns the path of the locked file.
    Call this BEFORE writing any changes to the active file.
    """
    VOICES_HISTORY.mkdir(parents=True, exist_ok=True)

    source = _voice_file(agent)
    if not source.exists():
        raise FileNotFoundError(f"No active voice file for {agent}: {source}")

    amendment_n = _amendment_count(agent) + 1
    date_str = datetime.now().strftime("%Y%m%d")
    dest_name = f"{agent}_locked_v{amendment_n}_{date_str}.md"
    dest = VOICES_HISTORY / dest_name

    shutil.copy2(source, dest)

    # Append lock metadata to the archived file
    with open(dest, "a") as f:
        f.write(f"\n\n---\n*Locked {datetime.now().strftime('%Y-%m-%d')} before amendment {amendment_n}.*")
        if notes:
            f.write(f" {notes}")
        f.write("\n")

    return dest


# ── Amendment recording ────────────────────────────────────────────────────────

def record_amendment(
    agent: str,
    what_changed: str,
    why: str,
    decided_by: str = "steward + founder",
    locked_path: Optional[Path] = None,
) -> None:
    """
    Appends an amendment record to constitution/decisions-log and
    updates the growth log.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    amendment_n = _amendment_count(agent)  # already incremented by lock_voice_version

    entry = f"""
---

## Voice Amendment — {agent.replace('_', ' ').title()} (Amendment {amendment_n})
**Date:** {date_str}
**Decided by:** {decided_by}

### What changed
{what_changed}

### Why
{why}

### Prior version locked at
`{locked_path.name if locked_path else 'see _history/'}`

"""
    with open(DECISIONS_LOG, "a") as f:
        f.write(entry)

    # Update growth log
    history = []
    if GROWTH_LOG.exists():
        history = json.loads(GROWTH_LOG.read_text())
    history.append({
        "agent": agent,
        "amendment_n": amendment_n,
        "amended_at": datetime.now().isoformat(),
        "decided_by": decided_by,
        "what_changed": what_changed[:300],
        "locked_as": locked_path.name if locked_path else None,
    })
    GROWTH_LOG.write_text(json.dumps(history, indent=2))


# ── Formatting ─────────────────────────────────────────────────────────────────

def format_assessment(data: dict) -> str:
    agent = data["agent"]
    count = data["growth_memory_count"]
    threshold = data["threshold"]
    met = data["threshold_met"]
    amendments = data["prior_amendments"]
    definition = data["current_definition"]
    memories = data["growth_memories"]

    lines = [
        f"# Voice Growth Assessment — {agent.replace('_', ' ').title()}",
        f"*Growth memories: {count} / {threshold} required | "
        f"Prior amendments: {amendments} | "
        f"Threshold {'MET' if met else 'NOT YET MET'}*",
        "",
    ]

    if not met:
        lines += [
            f"**Not yet ready for a growth review.** "
            f"{count} growth {'memory' if count == 1 else 'memories'} recorded; "
            f"{threshold - count} more needed before an amendment is warranted.",
            "",
            "Growth memories so far:",
            "",
        ]
        for m in memories:
            ts = m.get("timestamp", "")[:10]
            learning = m.get("learning", "")[:300]
            lines.append(f"- **[{ts}]** {learning}")
            aaak = m.get("aaak", {})
            if aaak.get("assertion"):
                lines.append(f"  → *{aaak['assertion']}*")
        lines.append("")
        lines.append("Continue writing growth memories. The protocol runs when the threshold is met.")
        return "\n".join(lines)

    # Threshold met — full assessment
    lines += [
        "## Current Voice Definition",
        "",
        definition,
        "",
        "## Growth Memories (what this voice has written about itself)",
        "",
    ]
    for m in memories:
        ts = m.get("timestamp", "")[:10]
        learning = m.get("learning", "")
        aaak = m.get("aaak", {})
        lines.append(f"**[{ts}]** {learning}")
        if aaak:
            for k in ("assertion", "assumption", "action", "knowledge"):
                if aaak.get(k):
                    lines.append(f"  *{k}:* {aaak[k]}")
        lines.append("")

    lines += [
        "## Gap Analysis",
        "",
        "The Steward reads the growth memories against the current definition and asks:",
        "",
        "- What has this voice learned about itself that is **not reflected** in the current definition?",
        "- What **failure pattern** has been named that the definition doesn't acknowledge?",
        "- What **scope clarification** has emerged from practice?",
        "- What **tension** has been discovered that isn't in the 'In tension with' line?",
        "- Is the core identity — the primary question, the essential disposition — still accurate?",
        "  Or has practice revealed that the definition was off in some way?",
        "",
        "## Proposed Amendment",
        "",
        "Draft the updated voice file here. Keep the same structure. Mark what changed.",
        "The core identity should be recognizable — growth does not mean replacement.",
        "",
        "When ready:",
        "```python",
        "from memory.growth import lock_voice_version, record_amendment",
        f'locked = lock_voice_version("{agent}", notes="amendment reason")',
        "# Then write the new definition to the voice file",
        "# Then record:",
        f'record_amendment("{agent}", what_changed="...", why="...", locked_path=locked)',
        "```",
    ]

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys as _sys
    agent_arg = _sys.argv[1] if len(_sys.argv) > 1 else None

    if agent_arg:
        data = assess_voice_growth(agent_arg)
        print(format_assessment(data))
    else:
        print("# Voice Growth Survey\n")
        for row in all_voices_assessment():
            status = "READY" if row["threshold_met"] else f"{row['growth_memory_count']}/{row['threshold']}"
            amend = f" ({row['prior_amendments']} prior)" if row["prior_amendments"] else ""
            print(f"  {row['agent']:<20} {status}{amend}")
        print(f"\nThreshold: {GROWTH_THRESHOLD} growth memories required for review.")
        print("Run: python memory/growth.py <agent_name>  for full assessment.")
