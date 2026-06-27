# memory/store.py
# The Canopy — Memory façade.
#
# Single write path: all memory goes through episodic.py (flat JSON).
# ChromaDB is no longer a write target. Legacy data was migrated.
#
# Three-tier context injection (v2 concepts, flat JSON implementation):
#   PERSISTENT  — Constitution, identity, founding. Always fully injected.
#   LONGTERM    — Decisions, growth, relational, project. Injected by significance.
#   EPISODIC    — Session summaries. Most recent N, high turnover.
#
# API surface is unchanged from v1 — existing agent imports continue to work.
# New callers should use build_memory_context() instead of format_memories_for_context().
#
# Research foundation:
#   Titans three-tier model: https://arxiv.org/abs/2501.00663
#   Fractal protection principle: context fields that must never be pruned

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.episodic import (
    log as _log,
    load as _load,
    load_tiered as _load_tiered,
    format_for_context,
    format_tiered_for_context,
    MEMORY_TYPE_TO_TIER,
    PERSISTENT,
    LONGTERM,
    EPISODIC_TIER,
    SIGNIFICANCE_SCORES,
)
from typing import Optional


# ── Constants ──────────────────────────────────────────────────────────────────

# Context budget fractions (of max_chars, after persistent is set aside)
_LONGTERM_BUDGET  = 0.35
_EPISODIC_BUDGET  = 0.25


# ── Retrieval helpers ──────────────────────────────────────────────────────────

def _keyword_score(record: dict, keywords: list) -> float:
    """
    Returns 0.0–1.0: fraction of hint keywords found in the record's text + tags.
    Used to re-rank longterm entries when a skill declares memory appetites.
    Zero keywords → always returns 0.0 (no effect on sort).
    """
    if not keywords:
        return 0.0
    text = (
        record.get("learning", "") + " " + " ".join(record.get("tags", []))
    ).lower()
    return sum(1.0 for kw in keywords if kw.lower() in text) / len(keywords)


# ── Write API ──────────────────────────────────────────────────────────────────

def save_memory(
    agent_name: str,
    content: str,
    memory_type: str = "session",
    metadata: dict = None,      # accepted, unused — legacy compat
    significance: str = "normal",
) -> str:
    """
    Saves a memory for an agent.

    Routes to episodic.log(). The `metadata` kwarg is accepted for
    backward compatibility but not stored (it was ChromaDB metadata).

    memory_type options: session, decision, growth, relational, project,
                         identity, constitution, founding
    significance: critical | high | normal | low
    """
    return _log(
        agent=agent_name,
        learning=content,
        memory_type=memory_type,
        significance=significance,
    )


def save_persistent_memory(
    agent_name: str,
    content: str,
    memory_type: str = "identity",
) -> str:
    """Stores a persistent-tier memory (Constitutional or identity). Never pruned."""
    return save_memory(
        agent_name=agent_name,
        content=content,
        memory_type=memory_type,
        significance="critical",
    )


def save_session_summary(agent_name: str, summary: str) -> str:
    """Legacy convenience wrapper."""
    return save_memory(agent_name, summary, memory_type="session", significance="normal")


# ── Read API ───────────────────────────────────────────────────────────────────

def retrieve_memories(
    agent_name: str,
    query: str = "",            # kept for API compat; not used for filtering
    memory_type: Optional[str] = None,
    tier: Optional[str] = None,
    n_results: int = 5,
    min_significance: float = 0.0,
) -> list[dict]:
    """
    Retrieves memories from the flat JSON store.

    Retrieval is by metadata filter (type, tier, significance, recency).
    Semantic/vector search is deferred to v3 deliberation layer.

    Returns records in the legacy shape expected by agent files:
      {"content", "type", "tier", "date", "timestamp", "significance"}
    """
    records = _load(
        agent=agent_name,
        memory_type=memory_type,
        tier=tier,
        min_significance=min_significance,
        limit=n_results * 2,    # over-fetch before significance sort
    )

    # Sort: significance desc, then recency desc
    records.sort(
        key=lambda r: (r.get("significance", 0.5), r.get("timestamp", "")),
        reverse=True,
    )

    result = []
    for r in records[:n_results]:
        result.append({
            "content":     r.get("learning", ""),
            "type":        r.get("memory_type", "session"),
            "tier":        r.get("tier") or MEMORY_TYPE_TO_TIER.get(r.get("memory_type", "session"), EPISODIC_TIER),
            "date":        r.get("timestamp", "")[:10],
            "timestamp":   r.get("timestamp", ""),
            "significance": r.get("significance", 0.5),
        })
    return result


def retrieve_persistent_memories(agent_name: str) -> list[dict]:
    """
    Returns all persistent-tier memories for an agent, fully — no truncation.
    Fractal protection: these fields must never be pruned from context.
    """
    records = _load(agent=agent_name, tier=PERSISTENT, limit=100)
    result = []
    for r in sorted(records, key=lambda x: x.get("timestamp", "")):
        result.append({
            "content":     r.get("learning", ""),
            "type":        r.get("memory_type", "identity"),
            "tier":        PERSISTENT,
            "date":        r.get("timestamp", "")[:10],
            "timestamp":   r.get("timestamp", ""),
            "significance": r.get("significance", 1.0),
        })
    return result


# ── Context injection ──────────────────────────────────────────────────────────

def build_memory_context(
    agent_name: str,
    query: str = "",
    max_chars: int = 3000,
    memory_hints: Optional[dict] = None,
) -> tuple[str, int]:
    """
    Builds a complete three-tier memory context block for prompt injection.

    Persistent tier: always fully included (fractal protection — no char limit).
    Longterm tier:   up to 35% of max_chars, sorted by significance + keyword score.
    Episodic tier:   most recent sessions, up to 25% of max_chars.

    memory_hints: optional dict from skill loader, keys:
      keywords     — terms to score against longterm content (boosts relevant entries)
      types        — memory types to prefer in longterm retrieval
      project_scope — handled by the harness, not here

    Returns (context_string, entries_injected).
    Use this instead of format_memories_for_context() for new code.
    """
    sections = []
    entries_injected = 0

    # ── Tier 1: PERSISTENT — always present, no budget limit ──────────────────
    persistent = retrieve_persistent_memories(agent_name)
    if persistent:
        lines = ["=== PERSISTENT MEMORY (Constitutional / Identity) ==="]
        for m in persistent:
            lines.append(f"[{m['type'].upper()}]")
            lines.append(m["content"])
            lines.append("")
        sections.append("\n".join(lines))
        entries_injected += len(persistent)

    # ── Tier 2: LONGTERM — decisions, growth, relational, project ─────────────
    longterm_budget = int(max_chars * _LONGTERM_BUDGET)
    hints = memory_hints or {}
    keywords = hints.get("keywords", [])
    lt_records = _load(agent=agent_name, tier=LONGTERM, limit=20)
    # Sort by significance + keyword bonus — hints from active skills surface relevant context
    lt_records.sort(
        key=lambda r: r.get("significance", 0.5) + _keyword_score(r, keywords),
        reverse=True,
    )

    if lt_records:
        lines = ["=== LONG-TERM MEMORY (Decisions / Growth / Projects) ==="]
        chars_used = 0
        added = 0
        for r in lt_records:
            content = r.get("learning", "")
            date    = r.get("timestamp", "")[:10]
            mtype   = r.get("memory_type", "").upper()
            sig     = r.get("significance", 0.5)
            entry   = f"[{mtype} — {date} — sig:{sig:.1f}]\n{content}"
            if chars_used + len(entry) > longterm_budget:
                break
            lines.append(entry)
            lines.append("")
            chars_used += len(entry)
            added += 1
        if added:
            sections.append("\n".join(lines))
            entries_injected += added

    # ── Tier 3: EPISODIC — recent sessions ────────────────────────────────────
    episodic_budget = int(max_chars * _EPISODIC_BUDGET)
    ep_records = _load(agent=agent_name, memory_type="session", limit=5)

    if ep_records:
        lines = ["=== EPISODIC MEMORY (Recent Sessions) ==="]
        chars_used = 0
        added = 0
        for r in ep_records:
            content = r.get("learning", "")
            date    = r.get("timestamp", "")[:10]
            entry   = f"[{date}]\n{content}"
            if chars_used + len(entry) > episodic_budget:
                break
            lines.append(entry)
            lines.append("")
            chars_used += len(entry)
            added += 1
        if added:
            sections.append("\n".join(lines))
            entries_injected += added

    return "\n\n".join(sections) if sections else "", entries_injected


def format_memories_for_context(
    memories: list,
    max_chars_per_memory: int = 200,
) -> str:
    """
    Legacy format function. Maintained for existing agent code.
    New code should use build_memory_context() for tier-aware injection.
    """
    if not memories:
        return "No relevant memories found for this context."

    formatted = ["=== MEMORY CONTEXT ==="]
    for m in memories:
        content = m.get("content", "")
        if len(content) > max_chars_per_memory:
            content = content[:max_chars_per_memory] + "..."
        mtype = m.get("type", "session").upper()
        date  = m.get("date", "")
        formatted.append(f"[{mtype} — {date}]")
        formatted.append(content)
        formatted.append("")
    return "\n".join(formatted)


# ── Maintenance ────────────────────────────────────────────────────────────────

def prune_episodic_memories(agent_name: str, keep_n: int = 10) -> int:
    """
    Removes oldest session-type episodic entries beyond keep_n.
    Never touches persistent or longterm tier records.
    Returns count of pruned files.
    """
    import json
    from pathlib import Path

    ep_dir = Path(__file__).parent / "episodic" / agent_name
    if not ep_dir.exists():
        return 0

    session_files = []
    for f in sorted(ep_dir.glob("*.json")):
        try:
            d = json.loads(f.read_text())
            if d.get("memory_type") == "session":
                session_files.append((f, d.get("timestamp", "")))
        except Exception:
            continue

    session_files.sort(key=lambda x: x[1])
    to_delete = session_files[:-keep_n] if len(session_files) > keep_n else []
    for f, _ in to_delete:
        f.unlink()
    return len(to_delete)


def memory_status(agent_name: str) -> dict:
    """Returns memory count per tier for an agent. Useful for diagnostics."""
    records = _load(agent=agent_name, limit=1000)
    status: dict = {PERSISTENT: 0, LONGTERM: 0, EPISODIC_TIER: 0}
    for r in records:
        t = r.get("tier") or MEMORY_TYPE_TO_TIER.get(r.get("memory_type", "session"), EPISODIC_TIER)
        status[t] = status.get(t, 0) + 1
    status["total"] = sum(status[k] for k in [PERSISTENT, LONGTERM, EPISODIC_TIER])
    return status


# ── Verification ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Testing three-tier memory store (flat JSON)...\n")

    print("1. Saving persistent memory (Constitutional)...")
    save_persistent_memory(
        "steward",
        "The Canopy Cultural Constitution: dignity is the first principle. "
        "Ecosystems not cities. Precautionary principle on synthetic consciousness.",
        memory_type="constitution",
    )
    print("   ✓\n")

    print("2. Saving longterm memory (significant decision)...")
    save_memory(
        "steward",
        "Decision: store.py rewritten as façade over flat JSON episodic layer. "
        "ChromaDB removed from write path. Single source of truth established.",
        memory_type="decision",
        significance="high",
    )
    print("   ✓\n")

    print("3. Saving episodic memory (session)...")
    save_memory(
        "steward",
        "Memory architecture cleanup session. Three tiers implemented in flat JSON.",
        memory_type="session",
        significance="normal",
    )
    print("   ✓\n")

    print("4. Building complete memory context...")
    ctx, count = build_memory_context("steward", query="architecture decisions", max_chars=3000)
    print(f"   Context length: {len(ctx)} chars, {count} entries injected")
    print(f"   Preview:\n{ctx[:400]}...\n")

    print("5. Memory status:")
    for tier, count in memory_status("steward").items():
        print(f"   {tier}: {count}")

    print("\n✓ Three-tier flat JSON memory verified.")
