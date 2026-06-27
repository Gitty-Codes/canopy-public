# memory/kg.py
# The Canopy — Temporal knowledge graph.
#
# SQLite-backed. Four tables:
#   entities     — things the system knows about (agents, projects, concepts)
#   relationships — how entities relate, with validity windows
#   decisions    — significant decisions with status (active/superseded/invalidated)
#   approaches   — what was tried and what was learned (the failure ledger)
#
# "Invalidate" marks records superseded without deleting them.
# History is preserved. Only the present changes.
#
# The Steward is primary writer. All agents and the harness can read.
# format_for_context() injects active decisions into the prompt.

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

KG_PATH = Path(__file__).parent / "kg.db"


# ── Internal ──────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now().isoformat()


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(KG_PATH)
    c.row_factory = sqlite3.Row
    return c


def _init() -> None:
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS entities (
                id          TEXT PRIMARY KEY,
                type        TEXT NOT NULL,
                name        TEXT NOT NULL,
                description TEXT DEFAULT '',
                created_at  TEXT NOT NULL,
                valid_until TEXT
            );

            CREATE TABLE IF NOT EXISTS relationships (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                from_entity  TEXT NOT NULL,
                relation     TEXT NOT NULL,
                to_entity    TEXT NOT NULL,
                context      TEXT DEFAULT '',
                created_at   TEXT NOT NULL,
                valid_until  TEXT
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                what          TEXT NOT NULL,
                by_whom       TEXT DEFAULT '',
                project       TEXT DEFAULT '',
                reasoning     TEXT DEFAULT '',
                status        TEXT NOT NULL DEFAULT 'active',
                created_at    TEXT NOT NULL,
                superseded_at TEXT
            );

            CREATE TABLE IF NOT EXISTS approaches (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_domain TEXT NOT NULL,
                approach       TEXT NOT NULL,
                outcome        TEXT NOT NULL,
                what_failed    TEXT DEFAULT '',
                what_learned   TEXT NOT NULL,
                created_at     TEXT NOT NULL
            );
        """)


_init()


# ── Entity API ────────────────────────────────────────────────────────────────

def add_entity(
    entity_id: str,
    entity_type: str,
    name: str,
    description: str = "",
) -> None:
    """
    Adds or updates an entity. Types: agent, project, concept, person, product.
    Use namespaced IDs: "agent:guardian", "project:kic-practice-buddy".
    """
    with _conn() as c:
        c.execute(
            """INSERT INTO entities (id, type, name, description, created_at)
               VALUES (?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
                 name=excluded.name,
                 description=excluded.description""",
            (entity_id, entity_type, name, description, _now()),
        )


def get_entity(entity_id: str) -> Optional[dict]:
    with _conn() as c:
        row = c.execute("SELECT * FROM entities WHERE id=?", (entity_id,)).fetchone()
        return dict(row) if row else None


# ── Relationship API ──────────────────────────────────────────────────────────

def add_relationship(
    from_entity: str,
    relation: str,
    to_entity: str,
    context: str = "",
) -> int:
    """
    Records a relationship between two entities. Returns the relationship ID.
    Example: add_relationship("agent:guardian", "has_flagged", "concept:coppa")
    """
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO relationships
               (from_entity, relation, to_entity, context, created_at)
               VALUES (?,?,?,?,?)""",
            (from_entity, relation, to_entity, context, _now()),
        )
        return cur.lastrowid


def invalidate_relationship(relationship_id: int) -> None:
    """Marks a relationship as no longer valid (without deleting it)."""
    with _conn() as c:
        c.execute(
            "UPDATE relationships SET valid_until=? WHERE id=?",
            (_now(), relationship_id),
        )


def query_relationships(
    entity: Optional[str] = None,
    relation: Optional[str] = None,
    active_only: bool = True,
) -> list[dict]:
    with _conn() as c:
        filters, params = [], []
        if entity:
            filters.append("(from_entity=? OR to_entity=?)")
            params.extend([entity, entity])
        if relation:
            filters.append("relation=?")
            params.append(relation)
        if active_only:
            filters.append("valid_until IS NULL")
        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        rows = c.execute(
            f"SELECT * FROM relationships {where} ORDER BY created_at DESC", params
        ).fetchall()
        return [dict(r) for r in rows]


# ── Decision API ──────────────────────────────────────────────────────────────

def add_decision(
    what: str,
    by_whom: str = "",
    project: str = "",
    reasoning: str = "",
) -> int:
    """
    Records a significant decision. Returns the decision ID.
    Decisions are active until explicitly superseded or invalidated.
    """
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO decisions (what, by_whom, project, reasoning, created_at)
               VALUES (?,?,?,?,?)""",
            (what, by_whom, project, reasoning, _now()),
        )
        return cur.lastrowid


def supersede_decision(decision_id: int, replacement_id: Optional[int] = None) -> None:
    """
    Marks a decision as superseded. The record is preserved; status changes.
    Pass replacement_id to link to the decision that replaces it.
    """
    with _conn() as c:
        c.execute(
            "UPDATE decisions SET status='superseded', superseded_at=? WHERE id=?",
            (_now(), decision_id),
        )


def invalidate_decision(decision_id: int) -> None:
    """Marks a decision as invalidated (found to be wrong, not just replaced)."""
    with _conn() as c:
        c.execute(
            "UPDATE decisions SET status='invalidated', superseded_at=? WHERE id=?",
            (_now(), decision_id),
        )


def query_decisions(
    project: Optional[str] = None,
    status: str = "active",
    limit: int = 20,
) -> list[dict]:
    with _conn() as c:
        filters = ["status=?"]
        params: list = [status]
        if project:
            if project == "canopy":
                filters.append("(project=? OR project='')")
            else:
                # Include canopy-level decisions as universal parent
                filters.append("(project=? OR project='' OR project='canopy')")
            params.append(project)
        where = f"WHERE {' AND '.join(filters)}"
        rows = c.execute(
            f"SELECT * FROM decisions {where} ORDER BY created_at DESC LIMIT ?",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]


# ── Approach / Failure Ledger API ─────────────────────────────────────────────

def record_approach(
    problem_domain: str,
    approach: str,
    outcome: str,
    what_learned: str,
    what_failed: str = "",
) -> int:
    """
    Records an approach tried, its outcome, and what was learned.
    outcome: "success" | "failure" | "partial"

    This is the failure ledger — explicit record of what was tried and why
    it worked or didn't. Prevents re-trying failed approaches without reason.
    Required: what_learned. Even failures must teach something.
    """
    if outcome not in ("success", "failure", "partial"):
        raise ValueError(f"outcome must be success/failure/partial, got: {outcome}")
    if not what_learned.strip():
        raise ValueError("what_learned is required — even failures must teach something")

    with _conn() as c:
        cur = c.execute(
            """INSERT INTO approaches
               (problem_domain, approach, outcome, what_failed, what_learned, created_at)
               VALUES (?,?,?,?,?,?)""",
            (problem_domain, approach, outcome, what_failed, what_learned, _now()),
        )
        return cur.lastrowid


def query_approaches(
    problem_domain: Optional[str] = None,
    outcome: Optional[str] = None,
    limit: int = 20,
) -> list[dict]:
    with _conn() as c:
        filters, params = [], []
        if problem_domain:
            filters.append("problem_domain=?")
            params.append(problem_domain)
        if outcome:
            filters.append("outcome=?")
            params.append(outcome)
        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        rows = c.execute(
            f"SELECT * FROM approaches {where} ORDER BY created_at DESC LIMIT ?",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]


def failed_approaches(problem_domain: Optional[str] = None) -> list[dict]:
    """Returns all failed or partial approaches — what not to try again."""
    rows = query_approaches(problem_domain=problem_domain, outcome="failure")
    rows += query_approaches(problem_domain=problem_domain, outcome="partial")
    rows.sort(key=lambda r: r["created_at"], reverse=True)
    return rows


# ── Context injection ─────────────────────────────────────────────────────────

def format_for_context(
    project: Optional[str] = None,
    max_decisions: int = 5,
    include_failures: bool = True,
) -> str:
    """
    Returns a formatted block of active decisions (and notable failures) for
    injection into a prompt. Called by the harness alongside episodic memory.
    """
    parts = []

    decisions = query_decisions(project=project, status="active", limit=max_decisions)
    if decisions:
        lines = ["=== TEMPORAL KNOWLEDGE (Active Decisions) ==="]
        for d in decisions:
            date   = d["created_at"][:10]
            by     = f" — {d['by_whom']}" if d.get("by_whom") else ""
            proj   = f" [{d['project']}]" if d.get("project") else ""
            lines.append(f"[{date}{by}{proj}] {d['what']}")
            if d.get("reasoning"):
                lines.append(f"  Why: {d['reasoning'][:150]}")
        parts.append("\n".join(lines))

    if include_failures:
        failures = failed_approaches()[:3]
        if failures:
            lines = ["=== FAILURE LEDGER (Do Not Re-try Without Reason) ==="]
            for f in failures:
                date = f["created_at"][:10]
                lines.append(f"[{date} — {f['problem_domain']}] Tried: {f['approach'][:80]}")
                if f.get("what_failed"):
                    lines.append(f"  Failed: {f['what_failed'][:100]}")
                lines.append(f"  Learned: {f['what_learned'][:120]}")
            parts.append("\n".join(lines))

    return "\n\n".join(parts)


# ── Status ────────────────────────────────────────────────────────────────────

def kg_status() -> dict:
    with _conn() as c:
        return {
            "entities":             c.execute("SELECT COUNT(*) FROM entities").fetchone()[0],
            "active_relationships": c.execute("SELECT COUNT(*) FROM relationships WHERE valid_until IS NULL").fetchone()[0],
            "active_decisions":     c.execute("SELECT COUNT(*) FROM decisions WHERE status='active'").fetchone()[0],
            "total_approaches":     c.execute("SELECT COUNT(*) FROM approaches").fetchone()[0],
            "failures_logged":      c.execute("SELECT COUNT(*) FROM approaches WHERE outcome='failure'").fetchone()[0],
        }


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Knowledge Graph Status\n")
    s = kg_status()
    for k, v in s.items():
        print(f"  {k:<25} {v}")

    print("\nActive decisions:")
    for d in query_decisions(status="active", limit=10):
        print(f"  [{d['created_at'][:10]}] {d['what'][:80]}")

    print("\nFailure ledger:")
    for f in failed_approaches():
        print(f"  [{f['created_at'][:10]}] {f['problem_domain']}: {f['approach'][:60]}")
        print(f"    Learned: {f['what_learned'][:80]}")
