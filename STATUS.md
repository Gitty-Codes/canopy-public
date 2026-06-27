# Canopy — Project Status
*Updated: 2026-06-09 | Update this file at the end of every build session.*

---

## How to read this

**ROADMAP.md** (root) — version sequencing: Project Sprout → v1 → v2. Done criteria per version.
**research/ROADMAP.md** — research thread sequencing: Consequence Architecture, Resonant Mind, phases.
**STATUS.md** (this file) — right now: what's live, what's next, who owns what.

Owner key: **[M]** = machine does it in Claude Code | **[F]** = founder does it in the world

---

## Version Status

**Project Sprout v0** — CLOSED ✓ (2026-06-06)
**Canopy v1** — COMPLETE ✓ (2026-06-09)

v1 done criteria — all met:
- [x] `harness.py` single unambiguous entry point — archive contains deliberate_v2.py
- [x] NVC three-tier dissent live in challenger.md and constitutional-deliberation.md
- [x] Cultural context acknowledgment in cultural-constitution.md
- [x] Code-health Check 0 documented as required pre-build step in CLAUDE.md
- [x] research/ store active — 22+ sources filed
- [x] README repository layout accurate and complete

Architecture clarification (2026-06-09): harness.py API-calling functions
(`respond`, `council_respond`, `run_task`) are research/Practice-Buddy infrastructure,
not the day-to-day interface. Claude Code is the deliberation engine. `CANOPY_NO_API=1`
set in `.claude/settings.local.json` — prevents accidental API calls from within
Claude Code sessions. API reserved for: Practice Buddy, deliberate experimental runs.

---

## Active Threads

### Thread 1 — Consequence Architecture (Synthetic Interoception)
**Status:** Module built, tested. Signal accumulates from real Claude Code session work.

What's live:
- `consequence/` module: token budget, dissent tracking, constitutional fidelity,
  background hardware monitor, JSONL history, rolling profile
- `CANOPY_NO_API=1` guard in harness.py — prevents accidental API calls from Claude Code
- Pre-registration v2 filed: `research/consequence-architecture/prereg-experiment-a-v2.md`
  Revised design: measures Claude Code sessions (not API calls); signal from episodic
  memory; no artificial warm-up required

What's not done:
- [ ] Recruit blind evaluation panel (3–5 raters) **[F]** — gates experiment start
- [ ] Reach data collection readiness threshold: ≥20 council sessions, ≥5 DISSENT
  records, ≥3 outcome notes **[F+M — accumulates through normal work]**
- [ ] Founder sign-off on prereg-experiment-a-v2.md **[F]**

Files: `consequence/`, `data/homeostatic_history.jsonl`, `research/consequence-architecture/`

---

### Thread 2 — Resonant Mind Training
**Status:** Spec complete. Both pre-registrations signed (v1 2026-06-07). Corpus confirmed.
W&B replaced with local CSV logging. Colab Pro active.

What's not done:
- [ ] Send Kimmerer letter — verify SUNY-ESF email first **[F]**
- [ ] Read three ML onramp resources **[F]**
- [ ] Recruit blind evaluation panel (shared with Thread 1) **[F]**
- [ ] Generate and curate 50–100 synthetic Type C training examples **[M+F]**
- [ ] Curate Type D council sessions via export tool **[F]**

Files: `research/resonant-mind-training/`

---

### Thread 3 — Council Infrastructure
**Status:** Relational memories live. Council sessions run in Claude Code via /council skill.
Auto-write on DISSENT wired into council_respond() for API-path use. Claude Code path
writes to episodic memory manually via /reflect skill.

What's live:
- 10 relational memory entries across all 11 agent directories
- Orchestration rules formalized in `constitutional-deliberation.md`
- Listener voice tone fixed (tentative vs. declarative)
- Council sessions accumulating in `memory/episodic/_council/` via Claude Code

What's not done:
- [ ] Run /reflect after each council session to build relational memory **[F — ongoing discipline]**
- [ ] Reach Thread 1 signal threshold (≥20 sessions) for Experiment A-2 readiness **[accumulates naturally]**

Files: `memory/episodic/*/`, `skills/constitutional-deliberation.md`, `constitution/voices/v2_compressed/`

---

### Thread 4 — Practice Buddy
**Status:** Active pilot. Auth complete. One studio deployed.

Open questions (from project.md):
- Partnership pipeline: which studios are next?
- Revenue model: studio licensing vs. grant-funded vs. hybrid?
- COPPA formal legal review (consent flow attorney sign-off)
- Multi-teacher studio schema change

Next: **[F]** — founder drives studio outreach and funding direction.
Machine available for: product spec work, grant research, comms drafting.

Files: `projects/clients/[client]/practice-buddy/`, `tasks/`

---

### Thread 5 — Publishing
**Status:** Two documents ready. Venue decided: arXiv preprint → Show HN.
Publish after Experiment A-2 produces results.

What's not done:
- [ ] Recruit blind evaluation panel **[F]** — shared gate with Threads 1 and 2
- [ ] Literature review section for hypothesis paper (Society of Mind, FEP, GWT) **[M]**

Files: `research/consequence-architecture/hypothesis-v0.3.md`, `research/consequence-architecture/spec-v0.2.md`

---

## File Map — Where Everything Lives

| What you're looking for | Where it is |
|---|---|
| **Entry point** | `harness.py` |
| **Version roadmap** | `ROADMAP.md` (root) |
| **Research roadmap** | `research/ROADMAP.md` |
| **This file** | `STATUS.md` (root) |
| **Cultural Constitution** | `constitution/cultural-constitution.md` |
| **Agent Architecture** | `constitution/agent-architecture.md` |
| **Voice files** | `constitution/voices/v2_compressed/` |
| **Decisions log** | `constitution/decisions-log` |
| **Skills** | `skills/` — index at `skills/MANIFEST.md` |
| **Task agents** | `tasks/` — index at `tasks/TASKS.md` |
| **Episodic memory** | `memory/episodic/{agent}/` |
| **Semantic memory** | `memory/semantic/` |
| **Relational memory** | `memory/episodic/{agent}/*_relational_*.json` |
| **Council memory** | `memory/episodic/_council/` |
| **Interoception module** | `consequence/` |
| **Interoception history** | `data/homeostatic_history.jsonl` |
| **Consequence arch spec** | `research/consequence-architecture/` |
| **Resonant Mind spec** | `research/resonant-mind-training/` |
| **Other research** | `research/` — index at `research/MANIFEST.md` |
| **Practice Buddy project** | `projects/clients/[client]/practice-buddy/` |
| **Threshold project** | `projects/` (check projects index) |
| **Privacy layer** | `privacy/` |
| **Tests** | `tests/` |
| **Enhancement proposals** | `proposals/` |
| **Benchmark pipelines** | `archive/` (deliberate.py, deliberate_v2.py) |
| **Claude Code session memory** | `~/.claude/projects/-Users-r3k-canopy/memory/` |

---

## Session Discipline

**At the start of every session:** read this file to orient.

**At the end of every session (machine):**
1. Update thread statuses in this file
2. Move completed items to done, add new next actions
3. Commit: `git commit` with what changed

**At the end of every session (founder):**
1. Note any real-world actions taken (letters sent, accounts set up, etc.)
2. Tell Claude so STATUS.md stays current

---

## What Needs a Decision (Founder)

These are open founder decisions that are blocking or shaping next machine actions:

| Decision | Blocks |
|---|---|
| Publish venue (arXiv / workshop / HackerNews) | Literature review framing, paper format |
| Studio outreach priority for Practice Buddy | Product and market thread work |
| Whether to run a full council via harness now | Validating relational memory write end-to-end |
