# memory/semantic.py
# The Canopy — SQLite semantic/pattern tier.
#
# Distilled cross-run learnings. The Elder's arc in a database.
# SQLite because: still just a file, no server, enables structured
# queries that flat JSON can't do efficiently at scale.
#
# Two tables:
#   patterns  — distilled insights that hold across multiple runs
#   decisions — what was decided, when, by whom, and whether it still stands
#
# The Steward is the primary writer.
# All agents are readers.
# History is not rewritten — records are invalidated, not deleted.

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

SEMANTIC_DIR = Path(__file__).parent / "semantic"
SEMANTIC_DB = SEMANTIC_DIR / "patterns.db"
SEMANTIC_SUMMARY = SEMANTIC_DIR / "summary.md"


# ── Connection ────────────────────────────────────────────────────────────────

def _conn() -> sqlite3.Connection:
    SEMANTIC_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(SEMANTIC_DB))
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE IF NOT EXISTS patterns (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern      TEXT NOT NULL,
            source_agents TEXT DEFAULT '[]',
            tags         TEXT DEFAULT '[]',
            project      TEXT DEFAULT 'canopy',
            recorded_at  TEXT NOT NULL,
            valid        INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS decisions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            decision     TEXT NOT NULL,
            reasoning    TEXT DEFAULT '',
            decided_by   TEXT DEFAULT 'council',
            project      TEXT DEFAULT 'canopy',
            decided_at   TEXT NOT NULL,
            status       TEXT DEFAULT 'active'
        );
    """)
    db.commit()
    return db


# ── Write API ─────────────────────────────────────────────────────────────────

def record_pattern(
    pattern: str,
    source_agents: Optional[list] = None,
    tags: Optional[list] = None,
    project: str = "canopy",
) -> int:
    """
    Records a distilled pattern — something learned across multiple runs
    that is stable enough to carry forward as semantic knowledge.
    Returns the record ID.
    """
    db = _conn()
    cur = db.execute(
        "INSERT INTO patterns (pattern, source_agents, tags, project, recorded_at) VALUES (?,?,?,?,?)",
        (
            pattern,
            json.dumps(source_agents or []),
            json.dumps(tags or []),
            project,
            datetime.now().isoformat(),
        ),
    )
    db.commit()
    _refresh_summary(project)
    return cur.lastrowid


def record_decision(
    decision: str,
    reasoning: str = "",
    decided_by: str = "council",
    project: str = "canopy",
) -> int:
    """
    Records a significant decision with its reasoning.
    Use invalidate_decision() to supersede — never delete.
    Returns the record ID.
    """
    db = _conn()
    cur = db.execute(
        "INSERT INTO decisions (decision, reasoning, decided_by, project, decided_at) VALUES (?,?,?,?,?)",
        (decision, reasoning, decided_by, project, datetime.now().isoformat()),
    )
    db.commit()
    _refresh_summary(project)
    return cur.lastrowid


def invalidate_decision(decision_id: int, reason: str = "") -> None:
    """
    Marks a decision as superseded. Does not delete — history is not rewritten.
    """
    db = _conn()
    db.execute(
        "UPDATE decisions SET status=? WHERE id=?",
        (f"superseded: {reason}" if reason else "superseded", decision_id),
    )
    db.commit()


def invalidate_pattern(pattern_id: int) -> None:
    """Marks a pattern as invalid (no longer holds)."""
    db = _conn()
    db.execute("UPDATE patterns SET valid=0 WHERE id=?", (pattern_id,))
    db.commit()


# ── Read API ──────────────────────────────────────────────────────────────────

def query_patterns(project: str = "canopy", limit: int = 10) -> list[dict]:
    """Returns active patterns, newest first."""
    db = _conn()
    rows = db.execute(
        "SELECT id, pattern, source_agents, tags, recorded_at FROM patterns "
        "WHERE valid=1 AND project=? ORDER BY id DESC LIMIT ?",
        (project, limit),
    ).fetchall()
    return [
        {
            "id": r["id"],
            "pattern": r["pattern"],
            "source_agents": json.loads(r["source_agents"] or "[]"),
            "tags": json.loads(r["tags"] or "[]"),
            "recorded_at": r["recorded_at"],
        }
        for r in rows
    ]


def query_decisions(
    project: str = "canopy",
    status: str = "active",
    limit: int = 20,
) -> list[dict]:
    """Returns decisions filtered by status ('active', 'superseded', or 'all')."""
    db = _conn()
    if status == "all":
        rows = db.execute(
            "SELECT id, decision, reasoning, decided_by, decided_at, status FROM decisions "
            "WHERE project=? ORDER BY id DESC LIMIT ?",
            (project, limit),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT id, decision, reasoning, decided_by, decided_at, status FROM decisions "
            "WHERE project=? AND status=? ORDER BY id DESC LIMIT ?",
            (project, status, limit),
        ).fetchall()
    return [
        {
            "id": r["id"],
            "decision": r["decision"],
            "reasoning": r["reasoning"],
            "decided_by": r["decided_by"],
            "decided_at": r["decided_at"],
            "status": r["status"],
        }
        for r in rows
    ]


def format_for_context(project: str = "canopy") -> str:
    """Formats active patterns and decisions for prompt injection."""
    patterns = query_patterns(project)
    decisions = query_decisions(project, status="active")

    if not patterns and not decisions:
        return ""

    lines = []
    if patterns:
        lines.append("=== PATTERNS ===")
        for p in patterns:
            agents = ", ".join(p["source_agents"]) if p["source_agents"] else "council"
            lines.append(f"[{p['recorded_at'][:10]} | {agents}] {p['pattern']}")

    if decisions:
        lines.append("\n=== ACTIVE DECISIONS ===")
        for d in decisions:
            lines.append(f"[{d['decided_at'][:10]} | {d['decided_by']}] {d['decision']}")
            if d["reasoning"]:
                lines.append(f"  → {d['reasoning'][:200]}")

    return "\n".join(lines)


# ── Summary refresh ───────────────────────────────────────────────────────────

def _refresh_summary(project: str = "canopy") -> None:
    """Regenerates the human-readable summary.md after any write."""
    patterns = query_patterns(project, limit=50)
    decisions = query_decisions(project, status="all", limit=50)

    lines = [
        f"# The Canopy — Semantic Memory",
        f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## Active Patterns",
        "",
    ]
    if patterns:
        for p in patterns:
            agents = ", ".join(p["source_agents"]) if p["source_agents"] else "council"
            lines.append(f"- **[{p['recorded_at'][:10]}]** {p['pattern']}")
            lines.append(f"  *(sources: {agents})*")
    else:
        lines.append("*(none yet)*")

    lines += ["", "## Decisions", ""]
    active = [d for d in decisions if d["status"] == "active"]
    superseded = [d for d in decisions if d["status"] != "active"]

    if active:
        lines.append("### Active")
        for d in active:
            lines.append(f"- **[{d['decided_at'][:10]}]** {d['decision']}")
            if d["reasoning"]:
                lines.append(f"  → {d['reasoning']}")
    if superseded:
        lines.append("\n### Superseded")
        for d in superseded:
            lines.append(f"- ~~[{d['decided_at'][:10]}] {d['decision']}~~ ({d['status']})")

    SEMANTIC_SUMMARY.write_text("\n".join(lines))


# ── Quick verification ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Testing semantic memory layer...\n")

    pid = record_pattern(
        "Sequential per-agent council on small models (llama3.2:3b) causes role drift — agents pattern-match to generic content under load. Frontier model with cached substrate holds voice tension more faithfully.",
        source_agents=["steward", "builder"],
        tags=["architecture", "model_selection"],
    )
    print(f"Pattern recorded: id={pid}")

    did = record_decision(
        "Frontier API (Claude Sonnet 4.6) is the primary substrate. Local model (llama3.2:3b) is retained for benchmarking only.",
        reasoning="Empirical test showed sequential council on 3b loses Constitutional orientation under load. Frontier holds the tension.",
        decided_by="founder + council",
    )
    print(f"Decision recorded: id={did}")

    print("\n" + format_for_context())
    print(f"\nSummary written to: {SEMANTIC_SUMMARY}")
