# memory/project.py
# The Canopy — Project registry and project-scoped memory.
#
# Design principle (from The Elder, May 2026):
#   Identity is persistent — agent memory in memory/episodic/{agent}/ is global.
#   Context is scoped — project memory in memory/episodic/projects/{id}/{agent}/
#   is layered on top of identity, never replacing it.
#
# A project does not create a different Steward.
# It gives The Steward additional context about what they're working on.

import itertools
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

_counter = itertools.count()

CANOPY_ROOT  = Path(__file__).parent.parent
PROJECTS_DIR = CANOPY_ROOT / "projects"
EPISODIC_ROOT = Path(__file__).parent / "episodic"
PROJECT_EPISODIC_ROOT = EPISODIC_ROOT / "projects"


# ── YAML frontmatter parser (no dependency on PyYAML) ─────────────────────────

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parses --- frontmatter from markdown. Returns (metadata, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    front = text[3:end].strip()
    body  = text[end + 4:].strip()
    meta  = {}
    for line in front.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Parse lists: [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
            meta[key] = val
    return meta, body


# ── Project registry ───────────────────────────────────────────────────────────

def list_projects(status: Optional[str] = None) -> list[dict]:
    """
    Returns all projects from the projects/ directory.
    Optionally filter by status: "active", "paused", "completed", "archived".
    """
    projects = []
    for project_file in sorted(PROJECTS_DIR.rglob("project.md")):
        text = project_file.read_text()
        meta, body = _parse_frontmatter(text)
        if not meta.get("id"):
            continue
        if status and meta.get("status") != status:
            continue
        projects.append({
            "id":      meta.get("id"),
            "name":    meta.get("name", meta["id"]),
            "client":  meta.get("client", ""),
            "status":  meta.get("status", "active"),
            "agents":  meta.get("agents", []),
            "skills":  meta.get("skills", []),
            "created": meta.get("created", ""),
            "body":    body,
            "path":    project_file,
        })
    return projects


def load_project(project_id: str) -> Optional[dict]:
    """
    Loads a single project by ID (e.g. "clients/kic/practice-buddy").
    Returns None if not found.
    """
    project_file = PROJECTS_DIR / project_id / "project.md"
    if not project_file.exists():
        # Try searching
        for p in list_projects():
            if p["id"] == project_id:
                return p
        return None

    text = project_file.read_text()
    meta, body = _parse_frontmatter(text)
    return {
        "id":      meta.get("id", project_id),
        "name":    meta.get("name", project_id),
        "client":  meta.get("client", ""),
        "status":  meta.get("status", "active"),
        "agents":  meta.get("agents", []),
        "skills":  meta.get("skills", []),
        "created": meta.get("created", ""),
        "body":    body,
        "path":    project_file,
    }


def format_project_context(project: dict, max_chars: int = 1500) -> str:
    """
    Formats a project's context for injection into agent prompts.
    Agents load this alongside their identity and global memory.
    """
    lines = [
        f"=== PROJECT CONTEXT: {project['name']} ===",
        f"Client: {project['client']} | Status: {project['status']}",
        f"Active agents: {', '.join(project['agents']) if isinstance(project['agents'], list) else project['agents']}",
        "",
    ]
    body = project["body"]
    if len(body) > max_chars:
        body = body[:max_chars] + "..."
    lines.append(body)
    return "\n".join(lines)


# ── Project-scoped memory ──────────────────────────────────────────────────────

def _project_agent_dir(project_id: str, agent: str) -> Path:
    """
    Returns the path for project-scoped episodic memory.
    Creates the directory if it doesn't exist.
    """
    d = PROJECT_EPISODIC_ROOT / project_id / agent
    d.mkdir(parents=True, exist_ok=True)
    return d


def log_project(
    project_id: str,
    agent: str,
    learning: str,
    memory_type: str = "session",
    tags: Optional[list] = None,
    significance: Optional[str] = None,
    aaak: Optional[dict] = None,
) -> str:
    """
    Writes a project-scoped episodic record.

    This is a project context memory — it belongs to the intersection of
    this agent and this project. It does not replace the agent's global memory.
    Call memory.episodic.log() for agent-global memories.
    """
    from memory.episodic import MEMORY_TYPE_TO_TIER, EPISODIC_TIER, PERSISTENT, LONGTERM, SIGNIFICANCE_SCORES

    now = datetime.now()
    ts  = now.strftime("%Y%m%d_%H%M%S_%f")
    record_id = f"{agent}_{ts}_{next(_counter):04d}"

    tier = MEMORY_TYPE_TO_TIER.get(memory_type, EPISODIC_TIER)
    if significance is None:
        significance = "critical" if tier == PERSISTENT else ("high" if tier == LONGTERM else "normal")
    sig_score = SIGNIFICANCE_SCORES.get(significance, 0.5)

    record = {
        "id":          record_id,
        "project":     project_id,
        "agent":       agent,
        "memory_type": memory_type,
        "tier":        tier,
        "significance": sig_score,
        "learning":    learning,
        "tags":        tags or [],
        "timestamp":   now.isoformat(),
    }
    if aaak:
        record["aaak"] = {
            "assertion":  aaak.get("assertion", ""),
            "assumption": aaak.get("assumption", ""),
            "action":     aaak.get("action", ""),
            "knowledge":  aaak.get("knowledge", ""),
        }

    path = _project_agent_dir(project_id, agent) / f"{record_id}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    return str(path)


def load_project_episodes(
    project_id: str,
    agent: str,
    memory_type: Optional[str] = None,
    limit: int = 10,
) -> list[dict]:
    """Loads project-scoped episodic records for an agent, newest first."""
    agent_dir = PROJECT_EPISODIC_ROOT / project_id / agent
    if not agent_dir.exists():
        return []

    records = []
    for path in sorted(agent_dir.glob("*.json"), reverse=True):
        try:
            with open(path) as f:
                r = json.load(f)
            if memory_type and r.get("memory_type") != memory_type:
                continue
            records.append(r)
            if len(records) >= limit:
                break
        except Exception:
            continue
    return records


def build_project_memory_context(
    project_id: str,
    agent: str,
    max_chars: int = 1000,
) -> str:
    """
    Builds project-scoped memory context for an agent.
    This is layered on top of the agent's global memory — never replacing it.
    """
    from memory.episodic import MEMORY_TYPE_TO_TIER, LONGTERM, format_for_context

    records = load_project_episodes(project_id, agent, limit=20)
    if not records:
        return ""

    # Split into longterm (decisions/growth) and episodic (sessions)
    lt = [r for r in records if MEMORY_TYPE_TO_TIER.get(r.get("memory_type", "session")) == LONGTERM]
    ep = [r for r in records if MEMORY_TYPE_TO_TIER.get(r.get("memory_type", "session")) != LONGTERM]

    parts = []
    if lt:
        parts.append(f"=== PROJECT DECISIONS [{project_id}] ===")
        parts.append(format_for_context(lt[:5], max_chars=max_chars // 2))
    if ep:
        parts.append(f"=== PROJECT SESSIONS [{project_id}] ===")
        parts.append(format_for_context(ep[:3], max_chars=max_chars // 2))

    return "\n\n".join(parts) if parts else ""


# ── Institutional knowledge ────────────────────────────────────────────────────
# Cross-project learning lives at memory/episodic/projects/_institutional/
# Patterns extracted from client work that belong to The Canopy's growing wisdom.

INSTITUTIONAL_ID = "_institutional"


def log_institutional(
    agent: str,
    learning: str,
    memory_type: str = "decision",
    tags: Optional[list] = None,
    significance: str = "high",
) -> str:
    """
    Records a cross-project learning to institutional knowledge.
    Call after kaizen extracts a pattern that generalized across projects.
    """
    return log_project(
        project_id=INSTITUTIONAL_ID,
        agent=agent,
        learning=learning,
        memory_type=memory_type,
        tags=(tags or []) + ["institutional"],
        significance=significance,
    )
