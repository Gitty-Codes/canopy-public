# skills/loader.py
# The Canopy — Context-aware skill injection layer.
#
# Skills are on-demand specializations: injected when relevant, ignored when not.
# A skill earns its place by outperforming the model's general capability for a
# specific task. If the model already does it well, the skill is noise.
#
# Three-layer selection:
#   Always:    meta + universal skills with invocation: auto
#   Auto:      sector/function-matched skills when project_context is set
#   On-demand: explicitly named in the call
#
# Memory appetites (frontmatter keys):
#   hint_types        — memory types to prioritize in retrieval (e.g. [decision, project])
#   hint_keywords     — terms to score against episodic content (e.g. [funder, grant])
#   hint_project_scope — if true, also load project-scoped episodic memory
#
# The loader aggregates hints from all active skills and returns them alongside
# skill text. The harness uses hints to sharpen retrieval — pulling memories
# relevant to the active task rather than generic recent context.
#
# Backward compatibility:
#   load_skill(), load_skills_for_agent(), inject_skills() preserved for agent files.
#   New harness code uses load_skills_for_context() exclusively.

from pathlib import Path
from typing import Optional

SKILLS_DIR = Path(__file__).parent


# ── Frontmatter parsing ────────────────────────────────────────────────────────

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Extracts YAML frontmatter from between --- markers.
    Returns (meta_dict, body_text). No PyYAML dependency.
    Supports: string values, list values [a, b, c], booleans.
    """
    meta: dict = {}
    stripped = text.lstrip()

    if not stripped.startswith("---"):
        return meta, text

    end = stripped.find("\n---", 3)
    if end == -1:
        return meta, text

    fm_block = stripped[3:end].strip()
    body = stripped[end + 4:].lstrip()

    for line in fm_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()

        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            meta[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        elif val.lower() == "true":
            meta[key] = True
        elif val.lower() == "false":
            meta[key] = False
        else:
            meta[key] = val

    return meta, body


# ── Skill discovery ────────────────────────────────────────────────────────────

def _discover_skills() -> list[dict]:
    """
    Scans skills/ for .md files with YAML frontmatter.
    Files without frontmatter are not skills and are skipped.
    """
    skills = []
    for path in sorted(SKILLS_DIR.glob("*.md")):
        if path.name.startswith("_") or path.name.upper() == "MANIFEST.MD":
            continue
        try:
            text = path.read_text()
        except OSError:
            continue
        meta, body = _parse_frontmatter(text)
        if not meta:
            continue  # not a skill file
        meta["_path"] = str(path)
        meta["_body"] = body
        if "name" not in meta:
            meta["name"] = path.stem
        skills.append(meta)
    return skills


# ── Selection logic ────────────────────────────────────────────────────────────

def _select_skills(
    all_skills: list[dict],
    project_context: Optional[dict],
    explicit: Optional[list],
) -> list[dict]:
    """
    Selects active skills based on scope, invocation, and project context.

    Evaluation order:
      1. Named in explicit → always included
      2. scope: meta|universal + invocation: auto → always included
      3. invocation: auto + project context matches sector/function → included
      4. Everything else → excluded unless explicitly named
    """
    selected = []
    seen: set = set()
    explicit_names = set(explicit or [])

    def _add(skill: dict) -> None:
        name = skill.get("name", skill["_path"])
        if name not in seen:
            seen.add(name)
            selected.append(skill)

    for skill in all_skills:
        name       = skill.get("name", "")
        scope      = skill.get("scope", "universal")
        invocation = skill.get("invocation", "on-demand")

        # Rule 1 — explicit override
        if name in explicit_names:
            _add(skill)
            continue

        # Rule 2 — always-on
        if scope in ("meta", "universal") and invocation == "auto":
            _add(skill)
            continue

        # Rule 3 — auto-load when project context matches
        if invocation == "auto" and project_context:
            skill_sector   = skill.get("sector")
            skill_function = skill.get("function")
            ctx_sector     = project_context.get("sector")
            ctx_function   = project_context.get("function")

            sector_match   = not skill_sector   or (ctx_sector   and skill_sector   == ctx_sector)
            function_match = not skill_function or (ctx_function and skill_function == ctx_function)

            if sector_match and function_match:
                _add(skill)

    return selected


# ── Memory hint aggregation ────────────────────────────────────────────────────

def _aggregate_hints(active_skills: list[dict]) -> dict:
    """
    Merges memory hints from all active skills into a single retrieval guide.

    Returns:
      types         — memory types to prefer in longterm retrieval
      keywords      — terms to score against episodic content
      project_scope — if True, also load project-scoped memory
    """
    types_set: set = set()
    keywords_set: set = set()
    project_scope = False

    for skill in active_skills:
        hint_types    = skill.get("hint_types", [])
        hint_keywords = skill.get("hint_keywords", [])

        if isinstance(hint_types, list):
            types_set.update(hint_types)
        if isinstance(hint_keywords, list):
            keywords_set.update(hint_keywords)
        if skill.get("hint_project_scope"):
            project_scope = True

    return {
        "types":         sorted(types_set),
        "keywords":      sorted(keywords_set),
        "project_scope": project_scope,
    }


# ── Primary API ───────────────────────────────────────────────────────────────

def load_skills_for_context(
    project_context: Optional[dict] = None,
    explicit: Optional[list] = None,
) -> tuple[str, dict]:
    """
    Loads skills appropriate for the current context.

    project_context keys (all optional):
      sector     — e.g. "nonprofit", "healthcare", "arts"
      function   — e.g. "fundraising", "comms", "operations"
      project_id — e.g. "clients/my-org/my-project"

    explicit: list of skill names to force-include regardless of invocation tag.

    Returns: (skill_text, memory_hints)
      skill_text   — formatted content block for prompt injection
      memory_hints — aggregated retrieval hints from all active skills
    """
    all_skills = _discover_skills()
    active = _select_skills(all_skills, project_context, explicit)

    if not active:
        return "", {}

    parts = []
    for skill in active:
        name  = skill.get("name", "unknown")
        label = name.upper().replace("-", " ")
        body  = skill.get("_body", "").strip()
        parts.append(f"=== SKILL: {label} ===\n\n{body}")

    memory_hints = _aggregate_hints(active)
    return "\n\n".join(parts), memory_hints


# ── Backward-compat shims ─────────────────────────────────────────────────────
# Preserved for agent files (builder.py, guardian.py, etc.). Do not use in new code.

_LEGACY_SKILL_FILES = {
    "canopy-voice":                "canopy-voice.md",
    "canopy_stack":                "canopy-stack.md",
    "constitutional_deliberation": "constitutional-deliberation.md",
    "agent_memory_practice":       "agent-memory-practice.md",
    "ethical_product_design":      "ethical-product-design.md",
    "reframing_constraints":       "reframing-constraints.md",
}

_CANOPY_CORE = ["constitutional_deliberation", "agent_memory_practice"]

AGENT_SKILLS = {
    "builder":         ["canopy_stack"] + _CANOPY_CORE,
    "product_partner": ["canopy_stack"] + _CANOPY_CORE,
    "guardian":        ["canopy_stack", "ethical_product_design"] + _CANOPY_CORE,
    "operator":        ["canopy_stack"] + _CANOPY_CORE,
    "strategist":      ["canopy_stack"] + _CANOPY_CORE,
    "listener":        _CANOPY_CORE,
    "elder":           _CANOPY_CORE,
    "steward":         ["ethical_product_design"] + _CANOPY_CORE,
    "inventor":        ["reframing_constraints"] + _CANOPY_CORE,
    "challenger":      ["canopy_stack"] + _CANOPY_CORE,
}


def load_skill(skill_name: str) -> str:
    """Loads a single skill by legacy name. Strips frontmatter."""
    filename = _LEGACY_SKILL_FILES.get(skill_name)
    if not filename:
        return ""
    path = SKILLS_DIR / filename
    if not path.exists():
        return ""
    _, body = _parse_frontmatter(path.read_text())
    return body


def load_skills_for_agent(agent_name: str, additional: list = None) -> str:
    """Loads skills for a specific agent using the legacy per-agent map."""
    skill_names = AGENT_SKILLS.get(agent_name, []).copy()
    if additional:
        for s in additional:
            if s not in skill_names:
                skill_names.append(s)
    if not skill_names:
        return ""
    loaded = []
    for name in skill_names:
        content = load_skill(name)
        if content:
            label = name.upper().replace("_", " ")
            loaded.append(f"=== SKILL: {label} ===\n\n{content}")
    return "\n\n".join(loaded) if loaded else ""


def inject_skills(base_prompt: str, agent_name: str, additional: list = None) -> str:
    """Injects skills into a system prompt. Legacy API for agent files."""
    skills_context = load_skills_for_agent(agent_name, additional)
    if not skills_context:
        return base_prompt
    return f"""{base_prompt}

=== YOUR CONTEXT ===
What is true about this project right now.
Use this to stay grounded in what exists and what has been decided.

{skills_context}

=== END CONTEXT ==="""


# ── Verification ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Skill loader verification\n")

    all_skills = _discover_skills()
    print(f"Skills discovered: {len(all_skills)}\n")
    for s in all_skills:
        scope = s.get("scope", "?")
        stype = s.get("type", "?")
        inv   = s.get("invocation", "?")
        hints = "hints" if (s.get("hint_keywords") or s.get("hint_project_scope")) else "-"
        print(f"  {s['name']:<38} scope:{scope:<12} type:{stype:<16} inv:{inv:<12} {hints}")

    print()
    ctx_text, hints = load_skills_for_context()
    print(f"Default load (no context):          {len(ctx_text):>6,} chars | hints: {hints}")

    print()
    ctx_text, hints = load_skills_for_context(
        project_context={"sector": "nonprofit", "function": "fundraising"},
        explicit=["opportunity-scout"],
    )
    print(f"Nonprofit/fundraising + explicit:   {len(ctx_text):>6,} chars")
    print(f"Memory hints: {hints}")
