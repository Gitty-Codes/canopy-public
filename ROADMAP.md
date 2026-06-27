# The Canopy — Technology Roadmap

The Canopy is the platform. Products (Practice Buddy, Threshold, others) are built on it.
This roadmap covers the platform only. Each product has its own roadmap.

Version names: Project Sprout → Canopy v1 → Canopy v2.
A version is done when its done criteria are met, not when a date arrives.

---

## Project Sprout — v0
**Status: CURRENT — closing**

Project Sprout is the experimental prototype. It proved the thesis: eleven voices held
simultaneously on a cached substrate, capable of genuine deliberation, constitutional
orientation under load. The Guardian has issued real PAUSEs. The Challenger has issued
real DRESSENTs. Memory has accumulated across sessions and informed subsequent work.

The code works. It is not yet legible to a stranger.

### Done criteria (must all pass before v1 starts)
- [ ] Code-health pass complete — Checks 0–6 across all Python files
- [ ] `deliberate.py` examine-mode bug fixed or clearly documented in file header
- [ ] `deliberate.py` and `deliberate_v2.py` archived with headers marking them benchmark-only
- [ ] Constitution label updated — remove "Draft for Founder Review" (it has been load-bearing since founding)
- [ ] `canopy-stack.md` updated to reflect research store, scout/learn skills, new code-health checks
- [ ] README repository layout section accurate (agents/, research/, tasks/ not listed)
- [ ] All skills in MANIFEST match their actual files and descriptions

### What Project Sprout contains
- `harness.py` — primary entry point; all 11 voices as cached substrate; `respond()`, `council_respond()`, `respond_focused()`
- `deliberate.py` — original sequential pipeline (benchmark only)
- `deliberate_v2.py` — three-pass architecture (benchmark only)
- Skill system: 17 skills, auto/on-demand, frontmatter discovery via `skills/loader.py`
- Memory: flat JSON episodic store + SQLite semantic store + temporal knowledge graph
- Privacy layer: four-tier classifier, cloud gate in `run_task()`, audit trail
- Research store: `research/` — 7 topics, 10 sources filed, MANIFEST indexed
- Constitution: 11 compressed voices, decisions-log, Cultural Constitution, Agent Architecture
- Practice Buddy: first product, active alpha deployment

### What Project Sprout does not contain
- NVC three-tier dissent (logged in decisions-log, awaiting research accumulation)
- Signal detection / context-reading meta-layer (spec not yet written)
- Cultural context acknowledgment in Cultural Constitution
- Autonomous scout capability
- LangGraph integration

---

## Canopy v1
**Status: NEXT — starts after Project Sprout done criteria are committed**

Canopy v1 is the first legible version. A careful developer can pick it up and understand
it without asking questions. The constitutional amendments logged in Entry 007 are live.
The platform is ready to onboard a second client with minimal founder involvement.

### Done criteria
- [x] `harness.py` is the single, unambiguous primary entry point — `deliberate.py` and `deliberate_v2.py` are in `archive/` with clear headers (2026-06-07)
- [x] NVC three-tier dissent amendment live in `challenger.md` and `constitutional-deliberation.md` — council deliberation session completed, founder approved, prior version locked (2026-06-07)
- [x] Cultural context acknowledgment added to `cultural-constitution.md` — explicit statement of the constitution's origins and commitment to periodic interrogation (2026-06-07)
- [ ] Code-health Check 0 (spec coherence) documented as a required pre-build step in CLAUDE.md
- [x] `research/` store active — 22 sources filed across 9 topics (2026-06-07)
- [ ] `README.md` repository layout accurate and complete for this version

### What Canopy v1 contains
- `harness.py` — sole primary entry point; benchmark pipelines archived
- NVC three-lens Challenger: curiosity → precision → dissent
- Ten-voice council: all tensions symmetric; Operator as proactive session historian;
  Product Partner as HOW voice; full tension network established
- Constitutional amendments: NVC tier (Challenger), distribution ethics (Section V),
  interrogation obligation (Section VII)
- Research store: active and growing via `scout` and `learn` skills
- Code-health: full seven-check bidirectional build discipline
- All Project Sprout capabilities, cleaned and legible

### What Canopy v1 does not contain
- Signal detection meta-layer spec — deferred to v2; orchestration work done today
  (Operator probe, Steward trigger, Product Partner routing) partially addresses
  what signal detection was meant to solve; full spec will be grounded in v1
  outcome notes before being written
- Voice skills (founding-commitment, stakeholder-brief, constraint-map, etc.) — v2
- Product Partner/Builder sequencing turn in orchestration — v2
- Autonomous scout (periodic search without commission) — v2
- LangGraph-based deliberate_v3 (genuine agent-to-agent dialogue) — v2
- Relational memories as primary architecture — v2
- Wider WRE stakeholders beyond founder + council — v2

---

## Canopy v2
**Status: PLANNED — details emerge from v1 outcomes**

Canopy v2 is the generative platform. Multiple clients can deploy on it. The council
can initiate research cycles autonomously. Agent-to-agent deliberation is real.

### Likely contains (subject to v1 outcome notes)
- Signal detection meta-layer — context-reading that loads skills reflexively; spec
  grounded in v1 outcome notes and research before being written
- Voice skills — founding-commitment, stakeholder-brief, guardian-security,
  constraint-map, capability-map, sequencing-tool; each earns its place
- Product Partner/Builder sequencing turn — orchestration update for generative
  questions; invention → path → foundation → examination → execution
- Guardian voice narrowing — move OWASP lens to guardian-security skill
- `deliberate_v3.py` — LangGraph-based genuine deliberation: cyclic, agent-to-agent addressing, Guardian-Inventor cycle, founder gateway for Constitutional pauses
- Relational memories as primary architecture — agents log what they noticed during deliberation; shared council chamber collection
- Autonomous scout — periodic research collection without founder commission
- Wider WRE — clients and affected communities participate in equilibration process
- Multi-client deployment — second client onboarded with documented process

### Build only after
v1 outcome notes show the current council hitting a real ceiling that v2 addresses.
Do not build v2 features speculatively.

---

## What belongs in a version and what doesn't

A feature belongs in the current version if:
- It is needed to meet the current version's done criteria, OR
- It unblocks the next version's first done criterion

Everything else goes in the next version's "likely contains" section and does not get built until that version opens.

When in doubt: add it to the roadmap, not to the current sprint.

---

## The Canopy Webapp — KIC Beta
**Status: LIVE — https://thecanopy.fly.dev**
*Updated: 2026-06-20*

The webapp is the first customer-facing surface for The Canopy. KIC beta (Rebecca Marchand + Laura Milleson) is the first real deployment. The org deployment model — seeded context, per-user private projects, shared org layer — is the architecture for all future orgs.

First real user feedback (Laura, 2026-06-20): "I love the post. And I like the Canopy because it feels opinionated." First successful full session: pride post for Instagram; she iterated with follow-ups.

### What is live and confirmed working
- Auth: server-side session cookie (canopy_session, HttpOnly, Secure, 30-day); /api/login sets cookie; /api/verify checks it
- Onboarding: name → Connect Google Drive → skip
- Org deployment model: KIC seeded from org-memory.md (23,530 chars); org context cached as Block 1
- User/org layer: private projects per user (X-User-Id), org context from org_id
- Eleven task skills in QUICK_ACTIONS: social-post (Haiku), monthly-social-plan (Sonnet), brand-kit (Sonnet), social-log-template (Haiku), donor-email (Haiku), board-memo (Sonnet), campaign (Sonnet), grant-loi (Sonnet), research (Sonnet), funder-brief (Sonnet), rec-letter (Sonnet)
- Google Drive: per-user OAuth, token refresh, save as Google Doc; connect button in session
- Web search: enabled on free-form chat and research/grant-loi/funder-brief tasks
- Persistent thread: follow-ups run in-place, no navigation
- URL privacy: question text in sessionStorage, never in URL
- Session sidebar: skills rail always visible
- Cache-Control: no-cache on index.html — browser always picks up new bundle after deploy
- Project-scoped episodic memory: every session writes to memory/episodic/projects/clients/kids-in-concert/
- Fly volume (canopy_data, 1GB): memory and session data survive redeploys
- Machine always warm: min_machines_running=1
- Prompt caching: Block 0 (substrate) + Block 1 (org context)

---

### Webapp backlog — prioritized by value to KIC beta, in build order

**#1 — Image upload for social posts** *(HIGH — directly unblocks Laura's social workflow)*
- What: File input (images only: jpg/png/webp) in compose area on Home and Workspace
- Backend: read uploaded image, encode as base64, include as image block in the Anthropic API call
- The social-post task already knows what to do with a photo; this lets Laura show it instead of describe it
- Estimate: ~3-4 hours
- Signal confirmed: her first session was a social post; she's describing photos in text now

**#2 — Streaming responses** *(MEDIUM — watch for signal)*
- What: SSE streaming on all API calls; tokens appear as they arrive
- Backend: `stream=True` on Anthropic calls, FastAPI `StreamingResponse`; Frontend: progressive text reveal
- Estimate: ~4 hours
- Build when: Rebecca or Laura says the wait feels too long (grant LOIs and board memos can run 20-30s blank-screen)

**#3 — Persistent session storage** *(MEDIUM — watch for signal)*
- What: Move session content from sessionStorage to server-side records on the Fly volume
- Impact: Past outputs survive tab close and device switches; Recent list restores content, not just titles
- Google Drive save is the intended path — this is the fallback
- Estimate: ~4 hours
- Build when: a user reports lost work

**Canva Connect API — blocked on founder action, not build time**
- Code is complete. Blocked on: (a) founder registers Canva developer app and gets credentials,
  (b) Laura creates KIC brand templates with named data fields in Canva,
  (c) CANVA_CLIENT_ID + CANVA_CLIENT_SECRET set as Fly secrets
- Once unblocked: ~2 hours to verify and activate

**Phase 2 — after KIC beta learnings confirm need:**
- Shared workspace: build when Rebecca or Laura asks "can we see what the other person worked on?" (see decisions-log Entry 2026-06-20)
- Session export as PDF/DOCX: build when Drive-save-then-download feels like too many steps
- OpenRouter integration: route social posts / donor emails to cheaper models at scale; negligible cost for 2 users now; worth doing at 20+ orgs

**Phase 3 — multi-org:**
- Self-serve BrandSetup: onboarding flow for new orgs (currently KIC is hand-seeded by founder)
- Per-org beta codes: unique code per org instead of shared code
- Usage dashboard: tokens consumed, cost per org, task breakdown — build when there are enough orgs to need it

---

## How to use this roadmap

- **Before building anything:** check which version is current. Does this feature belong here or in the next version?
- **Before opening a new version:** confirm all done criteria for the current version are committed to git.
- **After shipping a version:** run a brief council session — what surprised us? What should move from "likely" to "certain" in the next version?
- **When the plan changes:** update this file in the same commit as the decision that changed it.
