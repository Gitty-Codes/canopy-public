---
name: code-health
type: playbook
scope: meta
invocation: on-demand
description: Bidirectional build audit — spec coherence before building, structural quality and cross-artifact consistency after
---

# Code Health — Bidirectional Build Audit

Two moments, seven checks. Runs at the start of a build (forward-looking) and before any
significant push (backward-looking). Finds logical gaps in specs before they become code,
and finds decay before it becomes a rats nest.

**Before building:** Checks 0–1 (spec coherence, artifact consistency plan)
**After building / before push:** Checks 2–7 (structural quality, naming, security, consistency)

The checks below are the operational form of The Builder's five principles.
Each check has a pass condition and a fail action.

---

## Check 0 — Spec Coherence (run BEFORE building)

Before writing any code, read the spec or plan for the session. Ask:

- **Is the intent clear?** Could a careful stranger implement this without asking you questions?
- **Are the names decided?** Does the spec use the same names for the same concepts throughout, and do those names match what already exists in the codebase, README, and memory?
- **Is there a contradiction?** Does any part of the spec conflict with another part, or with a prior decision in the decisions-log?
- **Is the boundary defined?** Does the spec say what it will NOT do, not just what it will? An unbounded spec is an open invitation to scope creep.
- **Is there a test condition?** How will you know when this is done? What does correct look like?

- **Does this cross the irreversible consequence threshold?** Does this decision: (1) change behavior for users currently depending on the system without their prior knowledge, (2) introduce or materially change a third-party service that receives user data, (3) change how data is isolated between orgs, users, or sessions, (4) change how identity is established or validated, (5) make rollback non-trivial without manual intervention? If yes to any — stop. Bring to council before building.

**Pass:** all six answered, none blocked. Begin building.
**Fail:** resolve before writing code. A spec that can't answer these questions will produce code that can't answer them either.

For task profiles or agent specs specifically, also ask:
- Does this task duplicate something a skill already does?
- Does this task require a new file? If so, where does it live and why there?

---

## Check 1 — Cross-Artifact Consistency (run BEFORE and AFTER building)

Pick the primary name for every new concept introduced in this session (function, file, skill, agent, endpoint, screen, config key). That name must be consistent across:

| Artifact | Check |
|---|---|
| Code | function/class/variable name matches the concept name |
| File name | filename matches what the code inside it is called |
| README / docs | same name used, not a synonym or abbreviation |
| Git commit message | same name, not a paraphrase |
| Skills / task profiles | same name if the concept is referenced |
| Memory files | same name if logged |
| MANIFEST or index files | same name, description matches actual behavior |

**Pass:** one name, used everywhere, with no synonyms or abbreviations that would make a stranger guess.
**Fail:** rename before pushing. Inconsistent names are the most common source of "I thought X was Y" bugs.

For cross-language projects (Python + Flutter/Dart + markdown): check that the same concept doesn't have different names in different layers. A backend endpoint called `seed_test_plan` must not be called `seedPlan` in Flutter and `test-plan-seeder` in the README.

---

## Check 2 — Fresh Eyes Test

List every Python file in the project (excluding .venv, __pycache__, archive):

```bash
find . -name "*.py" -not -path "*/.venv/*" -not -path "*/__pycache__/*" -not -path "*/archive/*" | sort
```

For each file, read its first 10 lines. Ask:
- Does this file have a declared purpose in its header comment?
- Is that declared purpose still its actual purpose?
- Can a careful stranger understand why this file exists without reading the whole thing?

**Pass:** every file answers yes to all three.
**Fail:** rename, add a header, or schedule deletion. Do not leave the ambiguity.

---

## Check 3 — Zombie Check

For each file, ask:
- Is it imported anywhere in active code (not archive)?
- If not imported, is it a declared utility script (seeder, migration, one-off) with a header comment confirming its last-run date and future use case?
- If neither, it is a zombie.

```bash
# Find files with no imports from active code
grep -rn "import" . --include="*.py" | grep -v __pycache__ | grep -v archive
```

**Pass:** every file is either imported or declared as a utility with a dated header.
**Fail:** archive with a reason or delete. Name the decision and write it.

---

## Check 4 — Deep Module Check

For each module, ask (Ousterhout's test):
- What does the interface expose? (function signatures, parameters, return types)
- What does the implementation do?
- Is the interface simpler than the implementation?

A module whose interface is as complex as its implementation is shallow — it adds no abstraction value. It just moves complexity around.

Watch for:
- Functions with 5+ parameters (interface complexity leaking implementation complexity)
- Modules that re-export everything from another module without adding anything
- Wrappers that don't simplify

**Pass:** every module's interface is simpler than what it hides.
**Fail:** either simplify the interface, or question whether the module should exist.

---

## Check 5 — Name Check

Sample 10 function and variable names across the codebase. For each, ask:
- Does the name reveal what it IS or what it DOES, without a comment?
- If you removed the comment (if there is one), would the name still be clear?
- Is this name consistent with how the same concept is named elsewhere?

Rename candidates: anything with `tmp`, `data`, `result`, `thing`, `process_`, `handle_`, or a number suffix.

**Pass:** every sampled name is self-explaining and consistent.
**Fail:** rename in this session. Do not defer naming fixes.

---

## Check 6 — Security Scan (when code touches external inputs or APIs)

Only run this check when the session involved code that handles external input, API calls, or user data.

Ask The Guardian's OWASP questions:
- **Injection**: does any function pass external input to a command, query, or template without validation?
- **Authentication**: is the caller verified before any sensitive operation?
- **Exposure**: does any response return more data than the caller asked for?
- **Dependencies**: was anything new imported? What is its provenance?

**Pass:** all four questions answered cleanly.
**Fail:** name the specific exposure at the appropriate severity and resolve before pushing.

---

---

## Check 7 — Git hygiene (run before every push)

**Private repo (canopy, practice_buddy):** push at the end of every meaningful build session.
"Meaningful" means: a feature works, a version closes, a decision is committed, or a cleanup
pass completes. Do not let more than one session of work accumulate without a commit.

**Public repo (canopy public):** push when any of these are true:
- A version closes (Project Sprout done → Canopy v1 opens)
- A founding document is amended (Cultural Constitution, Agent Architecture, decisions-log entry)
- A skill is added or significantly changed
- A feature reaches a state worth showing

The public repo is a signal, not a mirror. It should always reflect the best current state,
not every intermediate step.

**Rollback readiness:** every commit must be rollback-safe.
- Never commit half-finished features without a branch
- Experimental work that might not hold: use a branch named `exp/[what-you're-trying]`
- When the experiment works: merge to main with a clear commit message
- When it doesn't: delete the branch; the attempt is not lost — it's in the decisions-log or memory if worth keeping

**Commit message discipline:**
- First line: `[type]: [what changed]` — type is `feat`, `fix`, `refactor`, `docs`, `chore`
- Second paragraph (if needed): why, not what — the what is in the diff
- If a version closes: `chore: close Project Sprout v0 — all done criteria met`

**Pass:** every session ends with a commit on the private repo. Public push when criteria above are met.
**Fail:** uncommitted work at session end — commit before closing, even if incomplete (use `wip:` prefix).

---

## Build rhythm — when each check runs

The discipline is bidirectional. Two moments in every build cycle:

### Before building (Checks 0–1)
Run at the start of any session that will produce new files, new functions, or new concepts.
- **Check 0 — Spec Coherence**: read the spec or plan; confirm intent, names, boundaries, test condition
- **Check 1 — Cross-Artifact Consistency**: identify the names to be used; confirm they match existing artifacts

If either check fails, resolve before writing code. A ten-minute spec review prevents a two-hour refactor.

### After building / before push (Checks 1–6)
Run before any `git push` that includes new or deleted files.
- **Check 1 — Cross-Artifact Consistency** (again): confirm what was built matches the names decided in Check 0
- **Check 2 — Fresh Eyes Test**: every file has a declared, accurate purpose
- **Check 3 — Zombie Check**: every file is imported or declared as a utility
- **Check 4 — Deep Module Check**: every module's interface is simpler than its implementation
- **Check 5 — Name Check**: every name is self-explaining and consistent
- **Check 6 — Security Scan**: run when session touched external inputs, APIs, or user data

**Target time:** fifteen minutes total. If it takes longer, the session produced more complexity than it should have.

---

## Language coverage

These checks apply to all languages in the project, not just Python.

| Language | Fresh Eyes | Zombie | Deep Module | Name | Cross-Artifact |
|---|---|---|---|---|---|
| Python | `find . -name "*.py"` | grep imports | function signatures | variable/function names | endpoint names, class names |
| Flutter/Dart | `find . -name "*.dart"` | check widget/service usage | widget interface vs. implementation | Provider/Service names | screen routes, API call names |
| Markdown (skills, README) | first paragraph describes purpose | is this file referenced anywhere? | N/A | heading names, concept labels | skill names match MANIFEST |

Cross-language rule: the same concept has exactly one canonical name. It does not have a Python name, a Dart name, and a README name. One name, used consistently across all layers.

---

## What to do with findings

Write findings to episodic memory as Builder growth memories:
```python
from memory.episodic import log
log('builder', 'Code health check [date]: [what was found and fixed]', memory_type='growth', tags=['code-health'])
```

When a finding recurs across two checks, it is a deficiency signal for the proposals layer.

When a finding reveals a naming inconsistency that exists in committed code, fix it in this session — do not defer. Naming debt compounds faster than technical debt because it lives in human memory, not just files.
