---
description: Load a project context or list active projects
allowed-tools: Bash, Read
---

Load a project context into the session: $ARGUMENTS

---

## What project context does

A project gives The Canopy's voices additional context — who the client is,
what is built, what is not yet proven, which agents are on the roster, which
skills apply. It does not change who the voices are. It changes what they know.

Identity is persistent. Context is scoped.

---

## Step 1 — List or load

If $ARGUMENTS is empty, list all projects:

```python
import sys; sys.path.insert(0, ".")
from memory.project import list_projects

projects = list_projects()
print(f"Active projects: {len([p for p in projects if p['status'] == 'active'])}\n")
for p in projects:
    status_mark = "●" if p["status"] == "active" else "○"
    roster = ", ".join(p["agents"][:4]) if isinstance(p["agents"], list) else p["agents"]
    if isinstance(p["agents"], list) and len(p["agents"]) > 4:
        roster += f" +{len(p['agents'])-4} more"
    print(f"  {status_mark} {p['id']:<40} {p['name']}")
    print(f"    Client: {p['client']} | Agents: {roster}")
    print()
```

Then ask: "Which project would you like to load?"

If $ARGUMENTS is provided, load that project (e.g. `clients/kic/practice-buddy`).

---

## Step 2 — Load and display

```python
import sys; sys.path.insert(0, ".")
from memory.project import load_project, format_project_context, build_project_memory_context

project = load_project("PROJECT_ID")
if not project:
    print(f"Project not found: PROJECT_ID")
    print("Run /project with no arguments to see available projects.")
else:
    print(format_project_context(project))
    print()
    
    # Show any existing project-scoped memories
    mem = build_project_memory_context("PROJECT_ID", "steward")
    if mem:
        print("--- Project Memory ---")
        print(mem)
```

---

## Step 3 — Confirm and orient

After loading the project, state clearly:

> "Project loaded: [name]. Working in context of [client]. Active agents for
> this project: [roster]. I'll carry this context through the session.
> What would you like to work on?"

When working in a project context:
- Load project.md context alongside agent skills
- Write project-scoped memories with `log_project()` for project-specific decisions
- Write agent-global memories with `log()` for learnings that belong to the voice itself
- The distinction: "we decided X for Practice Buddy" → project memory.
  "I noticed I default to listing when asked values questions" → agent memory.

---

## Writing project-scoped memory

```python
from memory.project import log_project
log_project(
    project_id="clients/kic/practice-buddy",
    agent="steward",
    learning="Decided to prioritize teacher onboarding over student-facing features for Q2.",
    memory_type="decision",
    significance="high",
)
```

## Writing institutional knowledge (cross-project learning)

```python
from memory.project import log_institutional
log_institutional(
    agent="steward",
    learning="Nonprofit clients require explicit grant-funding pathway in product strategy before studio outreach.",
    tags=["nonprofit", "go-to-market"],
)
```
