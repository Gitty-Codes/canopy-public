# memory/kaizen.py
# The Canopy — Growth cycle (kaizen distillation).
#
# Steward-owned process that reads episodic memories since the last cycle
# and surfaces candidates for semantic promotion.
#
# Semi-automated by design: infrastructure finds candidates, the Steward
# makes promotion decisions. Self-modification without deliberation is
# the most dangerous failure mode.
#
# Run:  python memory/kaizen.py
# Or invoke via /kaizen command in Claude Code.

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Ensure project root is on the path when run as a script
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.episodic import load

KAIZEN_LOG = Path(__file__).parent / "kaizen_log.json"
EPISODIC_ROOT = Path(__file__).parent / "episodic"

ALL_AGENTS = [
    "elder", "listener", "strategist", "product_partner",
    "builder", "guardian", "operator",
    "steward", "inventor", "challenger",
]


# ── Cycle tracking ─────────────────────────────────────────────────────────────

def last_run_time() -> datetime:
    if KAIZEN_LOG.exists():
        data = json.loads(KAIZEN_LOG.read_text())
        return datetime.fromisoformat(data.get("last_run", "2000-01-01T00:00:00"))
    return datetime.fromisoformat("2000-01-01T00:00:00")


def record_run(patterns_promoted: int = 0, decisions_promoted: int = 0) -> None:
    history = []
    if KAIZEN_LOG.exists():
        data = json.loads(KAIZEN_LOG.read_text())
        history = data.get("history", [])

    history.append({
        "run_at": datetime.now().isoformat(),
        "patterns_promoted": patterns_promoted,
        "decisions_promoted": decisions_promoted,
    })

    KAIZEN_LOG.write_text(json.dumps({
        "last_run": datetime.now().isoformat(),
        "cycles_completed": len(history),
        "history": history,
    }, indent=2))


# ── Episode collection ─────────────────────────────────────────────────────────

def _load_council_episodes(since: datetime) -> list[dict]:
    council_path = EPISODIC_ROOT / "_council"
    if not council_path.exists():
        return []
    episodes = []
    for f in sorted(council_path.glob("*.json"), reverse=True)[:50]:
        try:
            ep = json.loads(f.read_text())
            ep_time = datetime.fromisoformat(ep.get("timestamp", "2000-01-01"))
            if ep_time > since:
                episodes.append(ep)
        except Exception:
            pass
    return episodes


def gather_deficiency_gaps(since: Optional[datetime] = None) -> dict:
    """
    Reads deficiency_signals from all council sessions since last cycle.
    Returns recurring gaps — signals of the same type appearing 2+ times.
    Also returns resolved signals as growth evidence.
    """
    if since is None:
        since = last_run_time()

    council_path = EPISODIC_ROOT / "_council"
    if not council_path.exists():
        return {"recurring": {}, "resolved": [], "all_signals": []}

    all_signals = []
    resolved = []

    for f in sorted(council_path.glob("*.json"), reverse=True)[:100]:
        try:
            ep = json.loads(f.read_text())
            ep_time = datetime.fromisoformat(ep.get("timestamp", "2000-01-01"))
            if ep_time <= since:
                continue
            session_id = ep.get("id", "")
            for sig in ep.get("deficiency_signals", []):
                sig = {**sig, "session_id": session_id, "session_time": ep.get("timestamp", "")}
                if sig.get("resolved"):
                    resolved.append(sig)
                else:
                    all_signals.append(sig)
        except Exception:
            pass

    # Group unresolved by type
    by_type: dict[str, list] = defaultdict(list)
    for sig in all_signals:
        by_type[sig.get("type", "unknown")].append(sig)

    recurring = {t: sigs for t, sigs in by_type.items() if len(sigs) >= 2}

    return {"recurring": recurring, "resolved": resolved, "all_signals": all_signals}


def gather_candidates(since: Optional[datetime] = None) -> dict:
    """
    Reads all episodic memories since the last cycle (or since `since`)
    and clusters them into pattern candidates for the Steward's review.
    """
    if since is None:
        since = last_run_time()

    episodes = []
    for agent in ALL_AGENTS:
        for ep in load(agent, memory_type=None, exclude_type=None, limit=100):
            try:
                ep_time = datetime.fromisoformat(ep.get("timestamp", "2000-01-01"))
                if ep_time > since:
                    episodes.append(ep)
            except Exception:
                pass

    episodes += _load_council_episodes(since)

    # Cluster by tag
    tag_groups: dict[str, list] = defaultdict(list)
    for ep in episodes:
        for tag in ep.get("tags", []):
            tag_groups[tag].append(ep)

    # A candidate is a tag cluster with 2+ episodes from different agents or sessions
    candidates = {}
    for tag, eps in tag_groups.items():
        agents_seen = {ep.get("agent", "") for ep in eps}
        if len(eps) >= 2 or len(agents_seen) >= 2:
            candidates[tag] = eps

    return {
        "since": since.isoformat(),
        "total_episodes": len(episodes),
        "candidates": candidates,
        "all_episodes": sorted(episodes, key=lambda e: e.get("timestamp", ""), reverse=True),
    }


# ── Formatting ─────────────────────────────────────────────────────────────────

def format_for_review(result: dict) -> str:
    since = result["since"][:10]
    total = result["total_episodes"]
    candidates = result["candidates"]
    all_episodes = result["all_episodes"]

    lines = [
        "# Growth Cycle — Candidates for Semantic Promotion",
        f"*Since: {since} | Episodes reviewed: {total}*",
        "",
    ]

    # ── Deficiency gap report ─────────────────────────────────────────────────
    deficiency = gather_deficiency_gaps(datetime.fromisoformat(result["since"]))
    recurring = deficiency["recurring"]
    resolved = deficiency["resolved"]

    if recurring:
        lines += [
            "## Recurring Gaps",
            "*Deficiency signals appearing 2+ times — candidates for enhancement proposals.*",
            "",
        ]
        for gap_type, signals in sorted(recurring.items(), key=lambda x: -len(x[1])):
            voices = sorted({s.get("voice", "?") for s in signals})
            lines.append(f"### `{gap_type}` — {len(signals)} occurrences, voices: {', '.join(voices)}")
            for sig in signals:
                ts = sig.get("session_time", "")[:10]
                severity = sig.get("severity", "?")
                content = sig.get("content", "")[:150]
                lines.append(f"- **[{ts}] [{severity}]** {content}")
            lines.append("")
    else:
        lines += [
            "## Recurring Gaps",
            "*No deficiency signals appearing 2+ times yet.*",
            "",
        ]

    if resolved:
        lines += [
            "## Growth Record — Resolved Deficiencies",
            "*Deficiencies that have been addressed — evidence of the council's growth.*",
            "",
        ]
        for sig in resolved:
            ts = sig.get("session_time", "")[:10]
            gap_type = sig.get("type", "?")
            resolution = sig.get("resolution", "(no resolution note)")
            lines.append(f"- **[{ts}] {gap_type}**: {resolution}")
        lines.append("")

    if not all_episodes:
        lines.append("No new episodic memories since the last cycle.")
        lines.append("")
        lines.append("The ecosystem has not written since last distillation. Run sessions, then cycle.")
        return "\n".join(lines)

    if candidates:
        lines += [
            "## Pattern Candidates",
            "*These tags appear in 2+ episodes — potential stable patterns.*",
            "",
        ]
        for tag, eps in sorted(candidates.items(), key=lambda x: -len(x[1])):
            agents = sorted({ep.get("agent", "?") for ep in eps})
            lines.append(f"### `{tag}` — {len(eps)} episodes, agents: {', '.join(agents)}")
            for ep in eps:
                agent = ep.get("agent", "?")
                ts = ep.get("timestamp", "")[:10]
                mtype = ep.get("memory_type", "")
                learning = ep.get("learning", "")[:200]
                lines.append(f"- **[{ts}] {agent} ({mtype})**: {learning}")
                aaak = ep.get("aaak", {})
                if aaak.get("assertion"):
                    lines.append(f"  → *assertion: {aaak['assertion']}*")
            lines.append("")
    else:
        lines += [
            "## Pattern Candidates",
            "*No tag clusters with 2+ episodes yet — too early for pattern promotion.*",
            "",
        ]

    lines += [
        "## All Recent Episodes",
        "",
    ]
    for ep in all_episodes:
        agent = ep.get("agent", "?")
        ts = ep.get("timestamp", "")[:10]
        mtype = ep.get("memory_type", "")
        learning = ep.get("learning", "")[:250]
        lines.append(f"**[{ts}] {agent} ({mtype})**: {learning}")
        aaak = ep.get("aaak", {})
        if aaak.get("assertion"):
            lines.append(f"  → *{aaak['assertion']}*")
        lines.append("")

    lines += [
        "---",
        "",
        "## Steward Actions",
        "",
        "To promote a pattern to semantic memory:",
        "```python",
        "from memory.semantic import record_pattern",
        'record_pattern("what has been learned", source_agents=["agent"], tags=["tag"])',
        "```",
        "",
        "To record this cycle as complete:",
        "```python",
        "from memory.kaizen import record_run",
        "record_run(patterns_promoted=N, decisions_promoted=M)",
        "```",
    ]

    return "\n".join(lines)


# ── External intake tracking ───────────────────────────────────────────────────

INTAKE_LOG = Path(__file__).parent / "intake_log.json"


def record_intake(
    source: str,
    decision: str,
    destination: str,
    challenger_finding: str = "",
    promoted_as: str = "",
) -> None:
    """
    Records that an external learning was evaluated.
    Decision: 'promoted' | 'deferred' | 'discarded'
    Destination: 'skill' | 'semantic' | 'none'
    """
    entries = []
    if INTAKE_LOG.exists():
        entries = json.loads(INTAKE_LOG.read_text())

    entries.append({
        "evaluated_at": datetime.now().isoformat(),
        "source": source,
        "decision": decision,
        "destination": destination,
        "challenger_finding": challenger_finding,
        "promoted_as": promoted_as,
    })

    INTAKE_LOG.write_text(json.dumps(entries, indent=2))


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Running growth cycle...\n")
    result = gather_candidates()
    print(format_for_review(result))

    last = last_run_time()
    cycles = 0
    if KAIZEN_LOG.exists():
        data = json.loads(KAIZEN_LOG.read_text())
        cycles = data.get("cycles_completed", 0)
    print(f"\n---\nLast cycle: {last.date()} | Cycles completed: {cycles}")
