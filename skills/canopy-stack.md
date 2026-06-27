---
name: canopy-stack
type: domain
scope: meta
invocation: auto
description: Current stack, hardware reality, architecture decisions, and situational truth for The Canopy
---

# The Canopy — Current Stack and Situational Truth
*Updated: June 2026*

## What exists and runs today

**Runtime**
- Python 3.11, virtual environment at ~/canopy/.venv
- Ollama + llama3.2:3b locally — preserved for benchmark comparison only
- Anthropic API (Claude Sonnet 4.6) — cloud is the substrate; local is the benchmark

**Memory**
- Flat JSON episodic store — memory/episodic/ (single write path, all agents and projects)
- SQLite semantic tier — memory/semantic/patterns.db (distilled cross-session patterns)
- Three tiers: PERSISTENT (always injected), LONGTERM (by significance + keyword score), EPISODIC (recent sessions)
- Relational memory — memory/episodic/{agent}/*_relational_*.json — what each voice has
  noticed about other voices' reasoning patterns across council sessions
- Project-scoped memory — memory/episodic/projects/{client}/{project}/{agent}/
- ChromaDB archived — memory/db/ retained for reference, no longer written

**Deliberation pipelines**
- harness.py — unified harness, single API call, all ten voices in cached substrate
  - respond() — unconscious mode, all voices integrated; interoception runs on every call
  - council_respond() — Challenger examines; DISSENT triggers synthesis turn; auto-writes
    relational memories when DISSENT fires; relational council memory injected at session open
  - respond_focused() — lead with a specific voice, full substrate still present
- archive/deliberate_v2.py — three-pass pipeline, archived; superseded by harness council_respond()

**Consequence Architecture (Synthetic Interoception)**
- consequence/ — homeostatic feedback loop system, wired into all harness call surfaces
  - Level 1: token budget monitoring (per call, no latency cost)
  - Level 2: dissent tracking — rate and acknowledgment rate over rolling window
  - Level 3: constitutional fidelity detection + task/register classification
  - Level 5: persistent JSONL history (data/homeostatic_history.jsonl) with full versioning
  - Background: macmon hardware sampling (30s interval, logged, not injected in v1)
- State prompt from previous cycle injected into next call's memory block
- Cross-session profile seeding from JSONL history at module load

**Skills**
- skills/loader.py — context-aware loader; frontmatter-based discovery and selection
- skills/MANIFEST.md — index of all skills, planned gaps, and retired skills
- 19 active skills including experiment-protocol (pre-registration, inter-rater reliability,
  power analysis, results reporting — PhD-level rigor for AI science research)
- Selection: meta+universal/auto always load; sector/function-matched auto-load on project context;
  on-demand skills require explicit invocation
- Memory hints: active skills declare hint_types and hint_keywords; loader aggregates them;
  harness uses hints to keyword-score longterm retrieval and load project-scoped memory

**Projects**
- projects/{client}/{project}/project.md — YAML frontmatter registry for each project
- memory/project.py — load_project(), log_project(), build_project_memory_context()
- /project slash command — lists or loads project context into session

**Constitution and agents**
- constitution/ — Cultural Constitution (active, v0.1), Agent Architecture (v0.3)
- constitution/voices/v2_compressed/ — ten compressed voice files (active substrate)
- constitution/voices/v1_original/ — locked reference copies
- LangGraph 1.5.2 — installed, not yet wired (planned for v3 deliberation)
- Orchestration rules — skills/constitutional-deliberation.md: Steward trigger,
  Guardian/Challenger convergence protocol, Inventor/Challenger sequencing, Operator trigger

**Privacy**
- privacy/classifier.py — four-tier classifier (Public/Operational/Sensitive/Protected)
- privacy/audit.py — processing metadata audit trail (never stores content)
- Cloud gate in run_task(): Sensitive+ content blocked from cloud calls by default

**Tasks and research**
- tasks/ — task profiles and skills for the nonprofit-comms layer; see tasks/TASKS.md
- research/ — filed research sources by topic; see research/MANIFEST.md
- research/consequence-architecture/ — Consequence Architecture Hypothesis v0.3, spec v0.2
- research/resonant-mind-training/ — Resonant Mind training pipeline, corpus map, outreach letters
- research/ROADMAP.md — phased research roadmap (Consequence Architecture + Resonant Mind);
  Phase 1.5 added: constitutional transfer experiment (seed of multi-model orchestra)
- skills/scout.md — directed research collection playbook
- skills/learn.md — external material evaluation; Challenger-mediated intake
- skills/experiment-protocol.md — PhD-level research rigor: pre-registration, power analysis,
  inter-rater reliability, results reporting
- tools/export_training_data.py — export council sessions as Type D ChatML training examples;
  `--mark <id> true/false` for founder curation; `--only-approved` for clean export
- training_data/ — exported Type D candidates (gitignored; not committed to repo)

---

## Hardware reality

8GB RAM M2 MacBook. Context window is the constraint.
- Do not recommend dependencies not already installed
- Do not suggest replacing what works
- Build on what exists; defer what can wait

Static substrate with v2_compressed voices + constitution + auto skills ≈ 14K tokens.
Prompt caching active — cache hit on static block after first call in a session.

---

## Routing reality

harness.py → Anthropic API (Claude Sonnet 4.6) by design.
deliberate_v2.py Pass 1 and Pass 3 can route to local (llama3.2:3b) or cloud.
Pass 2 always routes to cloud — it is the full reasoning pass.

---

## What has been decided and why

**Dignity first** — no exploitation; Constitutional principles apply to every technical decision.

**Boring over clever** — proven over novel, reversible over permanent. The burden of proof
is on the irreversible decision.

**Single write path** — all episodic memory goes through memory/episodic.py (flat JSON).
ChromaDB retired after split-brain problem emerged from two uncoordinated write paths.

**Skills are on-demand specializations** — not general curriculum; not injected always.
A skill earns its place by outperforming the model for a specific task. The taxonomy
(meta / universal / sector / client) plus invocation tags (auto / on-demand) controls
what gets loaded and when. Skills declare memory hints; the loader aggregates them;
the harness satisfies them.

**Eleven voices held simultaneously** — not staged as sequential dialogue. Empirical result:
llama3.2:3b lost role and Constitutional orientation under sequential load.
Frontier model with cached substrate holds the tension more faithfully.

**The Challenger is a first-class voice** — DISSENT is a valid output, not a failure mode.
council_respond() fires a Challenger examination turn on every call; synthesis only if DISSENT.

**Identity is persistent; context is scoped** — agent-global memory stays in memory/episodic/{agent}/.
Project-scoped memory lives in memory/episodic/projects/{id}/{agent}/.
A project gives a voice additional context. It does not create a different voice.

**No forks in fundamental code** — one codebase, any machine.

---

## Direction — what the Canopy is building toward

The thesis: dignity-first outperforms exploitation-based systems over time.
The Canopy exists to prove this — not by assertion but by building something
that demonstrates it.

**v1 (complete — June 2026):** Ten voices (Market Voice retired, distribution ethics
constitutionalized), typed DISSENT (FACTUAL/VALUE/PROCESS) with routing, DISSENT RECORD
required in synthesis, structured dissents field queryable by Operator across sessions,
NVC three-lens deliberation live, training data export pipeline in tools/. The first
legible version. A careful developer can pick it up without asking questions.

**v2 (next):** Genuine agent-to-agent deliberation. Autonomous research cycles.
Multiple clients served with minimal founder involvement. Build only after v1
outcome notes show the current council hitting a real ceiling.

**The research arc beneath the platform:**
- *Consequence Architecture* — synthetic interoception: homeostatic loops that
  give the system genuine operational stakes and self-knowledge across sessions
- *Resonant Mind* — a fine-tuned model where dignity is in the weights, not just
  the context window

Phase 3 convergence: drives that create pressure (consequence architecture) +
values that shape how pressure is arbitrated (Resonant Mind) + character that
accumulates from that arbitration over time. That convergence is what this is
pointed at.

The council deliberating right now is the embryo of that system.

## Reflexive growth loop (LIVE — May 2026)

The council can now experience its own deficiency and initiate structured response.

**Loop:** `council_respond()` logs deficiency signals → `kaizen` surfaces recurring
gaps → `proposals.py` stages stubs at threshold (3 occurrences) → quiet inbox at
session open → founder commissions → Builder builds → signals marked resolved →
kaizen reads resolved signals as growth record.

**Deficiency signal schema:** type / voice / content / severity / resolved
**`outcome` command** — write a one-sentence outcome note after a session's
real-world result is known. Closes the loop between deliberation and consequence.

**Architecture confirmed:** Council = governance layer. Sub-agents = production layer.
Outputs above the "irreversible consequence threshold" must pass council review gate.
Threshold definition is the next governance task.

---

## What has been tried and why it didn't work

- Sequential per-agent council on llama3.2:3b — agents pattern-matched to generic content
  under load, lost Constitutional orientation. Pipeline preserved for benchmarking.
- Generic curriculum skills — created noise in 3b model. Replaced with specific playbooks.
- Full Constitution loaded into every agent prompt — too heavy for 3b context window.
  Replaced with lean identity prompts in harness substrate.
- stream=True in ollama.chat — caused self-prompting behavior on macOS. Fixed with stream=False.
- ChromaDB as memory backend — produced split-brain when commands wrote flat JSON and agents
  wrote ChromaDB. Retired. Flat JSON is the single path.

---

## Active Project: The Canopy Webapp

### Versioning
  v0.2.0 — Shipped 2026-06-20 (KIC beta: streaming, image upload, session persistence, memory parity)
  v0.3.0 — Shipped 2026-06-21 (Phase 0 security hardening + Phase 1 foundations)
  v0.3.1 — Shipped 2026-06-21 (KIC structured context fields — brief/standard now use curated fields)
  v0.3.2 — Shipped 2026-06-21 (Canva Connect API OAuth live — PKCE, correct token URL)
  v0.4.0 — Shipped 2026-06-22 (Phase 0 conversation rebuild — multi-turn, session persistence,
            clipboard export, follow-up routing fix, interoception signals)
  v1.0.0 — Multi-org launch ready (target: after conversation experience confirmed stable with KIC)

  Repository: canopy (private) / canopy-public (mirror). Webapp is webapp/ subdirectory.
  Version tracked in: webapp/backend/main.py (app version field) and this file.

### Current state
Status: v0.4.0 LIVE — https://thecanopy.fly.dev
Last major session: 2026-06-22 (Phase 0 conversation rebuild complete; council-deliberated)
Users: Rebecca Marchand (ED) and Laura Milleson (Artistic Director), Kids in Concert
Roadmap: proposals/ROADMAP-webapp-v1.md — Phase 0 complete; Phases 1–4 defined

Stack: React/Vite frontend, FastAPI backend, Anthropic API, Google Drive OAuth, Canva Connect API

### What is confirmed working (v0.4.0)
  - Auth: random session token cookie (canopy_session, HttpOnly, Secure, 30-day); org_id/user_id
    read from server-side session files only — never from client headers
  - Onboarding: name → Connect Google Drive → skip
  - Org deployment model: KIC seeded from org-memory.md (23,530 chars full_context)
    + 9 structured fields (mission, tagline, voice_words, voice_avoid, audience, programs,
    impact_stats, year_founded, location) written directly to volume
  - Context trimming: brief tasks get curated structured fields (~500 chars of org identity);
    standard tasks get all structured fields; full tasks get the complete org document
  - Eleven task skills: social-post (Haiku), monthly-social-plan (Sonnet), brand-kit (Sonnet),
    social-log-template (Haiku), donor-email (Haiku), board-memo (Sonnet), campaign (Sonnet),
    grant-loi (Sonnet), research (Sonnet), funder-brief (Sonnet), rec-letter (Sonnet)
  - Multi-turn conversations: follow-ups route through original task type (not generic respond());
    canva_blocks and human_gate appear on every turn, not just turn 1
  - Session persistence across navigation: thread saved to sessionStorage on every exchange;
    back button restores conversation; tab close still loses state (server-side threads in Phase 1)
  - Social-post task: always drafts on turn 1 (draft-first), refinement question after
  - Clipboard-first Canva export: "Copy for Canva ↓" scrolls to per-field copy blocks
    (headline, caption, hashtags); works with any Canva plan, no template setup required
  - Canva autofill path: OAuth live, but BLOCKED — requires Canva Enterprise per user
    (not Teams, not free); autofill code preserved but inactive until account tier confirmed
    NOTE: Canva data fields are set up via Apps → "Data autofill" in template editor (not Bulk
    Create, not right-click). Field names are case-sensitive and must match API exactly.
    Use GET /brand-templates/{id}/dataset to discover field names before calling autofill.
  - Google Drive: per-user OAuth, token refresh, save as Google Doc; connect button in session
  - Web search on respond_lite() and research/grant-loi/funder-brief tasks
  - Fly volume (canopy_data, 1GB): memory and session data survive redeploys
  - Prompt caching: Block 0 (substrate) + Block 1 (org context)
  - Image upload: social-post task uses uploaded photo directly
  - Per-org data namespace: data/orgs/{org_id}/setup.json, projects.json, sessions/, token_log.jsonl
  - Token spend log: data/orgs/{org_id}/token_log.jsonl appended after every call
  - Interoception signals: task completions and errors write to data/webapp_signals.jsonl;
    consequence/webapp_reader.py stub ready; NOT YET wired to consequence architecture
  - Multi-org support: BETA_CODE_ORGS env var (JSON map code→org_id) + BETA_ORG_NAMES
  - Sidebar sessions: clickable and resumable (were dead <p> tags before v0.4.0)
  - Server logging: canopy logger now attached directly with StreamHandler (basicConfig is a
    no-op under uvicorn — this was broken in all prior versions; fixed in v0.4.0)
  - Error messages: /respond and /task routes have distinct error strings from /council

### What is broken / known gaps
  - Thread state does not survive tab close or hard refresh (server-side thread persistence
    is Phase 1 — proposal in proposals/ROADMAP-webapp-v1.md)
  - No cross-session memory surfacing: prior sessions inform org context silently but are not
    shown to the user ("last time we worked on X…" — Phase 2)
  - Session titles are the first 40 chars of user input, often awkward (auto-title in Phase 2)
  - Canva autofill blocked on Enterprise requirement — clipboard export is the working path

### Phase 0 (security hardening, June 2026) — COMPLETE
  - Random session token cookie; server-side session files; org/user never from client
  - X-Beta-Code and X-User-Id header auth paths removed
  - Per-org data isolation with ownership verification and path sanitization
  - OAuth tokens namespaced by org_id; OAuth state dict pruned (10min TTL)
  - Generic error responses to client; full errors server-side only

### Phase 1 (foundations, June 2026) — COMPLETE
  - context_level per task profile (brief/standard/full) — all 11 task profiles set
  - Structured context fields: brief/standard use curated fields, not char truncation
  - KIC setup populated with 9 structured fields on volume (full_context preserved)
  - Token spend log per org
  - Multi-turn full-thread context
  - provision_org.py CLI for adding new orgs

### Phase 0 conversation rebuild (June 2026) — COMPLETE (v0.4.0)
  Council-deliberated before building. Governance gate applied.
  - Multi-turn routing fixed (follow-ups route through original task)
  - Thread persistence via sessionStorage (back navigation safe)
  - Social-post draft-first contract
  - Clipboard-first Canva export
  - Resumable sidebar sessions
  - Differentiated error messages
  - Server logging fixed
  - Interoception signal stub

### Phase 1 (conversation-first architecture) — NEXT
  Full server-side thread persistence, thread-aware sidebar, threads as primary navigation unit.
  Crosses irreversible consequence threshold — requires council review before building.
  Schema: data/orgs/{org_id}/threads/{thread_id}.json, versioned (v: 1).
  See proposals/ROADMAP-webapp-v1.md for full spec.

### Deployment notes
  ALWAYS deploy from repo root: cd ~/canopy && flyctl deploy --config webapp/fly.toml
  Frontend must be rebuilt locally before deploying: cd webapp/frontend && npm run build
  Dockerfile copies static assets; it does NOT build frontend.

  Secrets — currently set:
    ANTHROPIC_API_KEY, BETA_ACCESS_CODE, TOKEN_ENCRYPTION_KEY,
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, CANVA_REDIRECT_URI (fly.toml env),
    CANVA_CLIENT_ID, CANVA_CLIENT_SECRET
  Secrets — needed when adding second org:
    BETA_CODE_ORGS (JSON map; replaces BETA_ACCESS_CODE)
    BETA_ORG_NAMES (JSON map; optional display names)

  .dockerignore at repo root excludes: .venv/ (2.2GB), memory/episodic/, memory/semantic/,
    memory/db/, training_data/, research/, projects/, .git/, __pycache__/

  To update org data on the volume without a redeploy:
    fly ssh console -a thecanopy -C "python3 -" < tools/your_script.py

### Next build priorities
  1. Schedule working session with Rebecca and Laura — validate Phase 0 fixes with real use
  2. Phase 1: server-side thread persistence (council review required first)
  3. Canva autofill: verify Laura's account tier before any more template work

## Active Project: Practice Buddy

Status: Alpha complete; pilot underway with KIC students and teachers
Stack: Flutter (mobile), Claude API (AI feedback), Supabase (backend)
What exists: AI practice companion, metronome, tuner, teacher dashboard,
  concert countdown, COPPA-compliant onboarding, multi-tenant architecture
What is proven: Architecture complete, pilot underway — real students, real teachers
Audio: Processed in real-time, immediately deleted — never stored
Mission: Social value — serving underserved students, not profit extraction

Do not recommend rebuilding what exists. Reason from what is already built.
