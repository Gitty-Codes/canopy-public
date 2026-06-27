# Canopy — Master Schedule
*Updated: 2026-06-14 | Check boxes in GitHub UI or tell Claude "done: X"*
*Owner key: **[F]** founder action (no machine substitute) | **[M]** machine | **[F+M]** both*

---

## Critical Path

```
Visual brand [F: today] → digital strategy decisions [F] → content/comms build [M] → go public

Evaluation panel recruited [F: today] ─┬→ Experiment A-2 (Consequence Architecture)
                                        └→ Experiment B evaluation (Resonant Mind)

Resonant Mind data ready [M] ──────────→ Experiment B training run → results → publishing
Pre-reg sign-off [F] ──────────────────→ (same)

Fly.io deploy [F: tomorrow] ───────────→ KIC beta live → brand setup with Laura → real use
```

**The single most load-bearing founder action right now: recruit the evaluation panel.**
It is blocking two research threads simultaneously. Everything else can move around it.

---

## TODAY — June 14

- [ ] Bring brand input (feel words, visual references, logo thinking, color instincts) **[F]**
- [x] AI stance check: Google "@bryankonietzko AI" and "@mike_dima AI" — 10 min **[F]**
- [x] Send Avatar letter — sent to studioinfo@nick.com 2026-06-14 **[F]**
- [x] Send KIPO letter — sent to radsechrist@hotmail.com 2026-06-14 **[F]**
- [ ] Begin evaluation panel recruitment (3–5 raters, blind) **[F]**

---

## Thread 1 — KIC Beta (The Canopy Web App)

**Status:** Built. Not deployed. Visual brand pending.

- [ ] Fly.io deploy — set secrets + `fly deploy` from `/webapp` **[F: tomorrow, you have the guide]**
- [ ] Brand session with Laura — populate KIC org memory via Brand Setup screen **[F+M: after deploy]**
- [ ] First real council session on a live KIC task (grant LOI or donor email) **[F: after deploy]**
- [ ] Visual brand build **[M: after brand input today]**
- [ ] Share beta URL + code with Laura **[F: after visual brand]**

*Dependencies: deploy → brand session → real use → visual iterations → beta users 2 + 3*

---

## Thread 2 — Practice Buddy

**Status:** Auth complete. One studio (KIC). Backend localhost only.

- [ ] Railway deploy — env vars: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_JWT_SECRET`, `ANTHROPIC_API_KEY`, `ENVIRONMENT=production`, `FRONTEND_URL` **[F]**
- [ ] Real device test — iPhone, TTS + mic + full session flow **[F: after Railway deploy]**
- [ ] COPPA confirmation email — wire to Resend or Postmark **[M: before real under-13 students]**
- [ ] `music_xml_content` DB migration in Supabase **[M]**
- [ ] Teacher dashboard (plan builder, session summaries, practice logs) **[M: Phase 2]**

*Dependencies: Railway deploy → device test → COPPA fix → second studio outreach*

---

## Thread 3 — Resonant Mind

**Status:** Spec + pre-reg complete. Export tool built. No training data prepared. No Colab notebook built. Phase gate: pre-reg signed off → experiments run.

**Outreach — sending today:**
- [ ] AI stance check for DiMartino, Konietzko, Sechrist **[F: 10 min today]**
- [x] Send Avatar letter — sent to studioinfo@nick.com 2026-06-14 **[F]**
- [x] Send KIPO letter — sent to radsechrist@hotmail.com 2026-06-14 **[F]**
- [x] Kimmerer letter — sent 2026-06-14 **[F]**
- [ ] Baldwin estate — jamesbaldwin.com/contact or Wylie Agency **[F: this week]**

**Data:**
- [ ] Run `tools/export_training_data.py --only-approved` to see current Type D count **[M: anytime]**
- [ ] Generate Type C synthetic examples (target: 50–100, curate via resonance test) **[M]**
- [ ] Founder sign-off on Experiment B pre-registration **[F]**

**Training:**
- [ ] Build Colab training notebook from pipeline spec (can do today — spec has all code) **[M]**
- [ ] Pilot run: 10–20 examples, 100 steps — "does the pipeline work" proof-of-concept **[F+M: decision — this is separate from Experiment B, not bound by pre-reg gate]**
- [ ] Experiment B full run (500 steps, 50+ examples) **[F+M: after pre-reg + data ready + panel recruited]**

**ML onramp (founder):**
- [ ] Read three ML onramp resources (in `founder-ml-onramp.md`) **[F: ongoing]**

*Dependencies: pre-reg sign-off + panel + data → Experiment B → results → publishing*

---

## Thread 4 — Consequence Architecture

**Status:** Module live. Signal accumulating. Pre-reg signed (A-2). Waiting on data threshold + evaluation panel.

Data threshold (accumulates through normal council use — no action needed):
- Current: unknown count. Need ≥20 council sessions, ≥5 DISSENT records, ≥3 outcome notes
- [ ] Check current count: `ls memory/episodic/_council/ | wc -l` **[M: anytime]**

Gated actions:
- [ ] Evaluation panel recruited (3–5 raters) **[F: TODAY — this is critical path]**
- [ ] Founder sign-off on pre-reg A-2 **[F: already signed — confirm]**
- [ ] Run Experiment A-2 when threshold met **[M+F]**

---

## Thread 5 — Project Threshold (Psychiatrist client)

**Status:** VOC complete. Direction set (pre-session consultation tool). Challenger's dissent stands: need working agreement before any build.

- [ ] Schedule working agreement conversation **[F]**
- [ ] Confirm HIPAA anonymized case presentation model with client **[F: in that conversation]**
- [ ] Build pending working agreement **[M: after above]**

---

## Thread 6 — Visual Brand + Identity

**Status:** Placeholder system (green, Lora, warm neutrals). Not decided.

- [ ] Bring brand input today (feel words, references, logo thinking, color instincts) **[F: TODAY]**
- [ ] Brand build — Tailwind tokens, typography, color, spacing, logo direction **[M: after input]**
- [ ] Decision: does The Canopy need a logo/mark for beta, or wordmark only? **[F]**

---

## Thread 7 — Digital Strategy

**Status:** No decisions made. Blocking all public-facing work.

- [ ] Domain: thecanopy.ai / canopy.ai / other — check availability, decide **[F]**
- [ ] Access model for non-beta users: hosted waitlist? public GitHub? download? **[F]**
- [ ] Public presence form: standalone site? GitHub page? Substack? **[F]**

*Dependencies: these three decisions → content/comms strategy → any public work*

---

## Thread 8 — Content + Communications

**Status:** Not started. Gated on: visual brand + digital strategy + experiment results.

When gates clear, the sequence is:
1. Website / landing page **[M]**
2. GitHub public repo polish **[M]**
3. First LinkedIn posts (what The Canopy is + why) **[F+M: drafts by M, posted by F]**
4. Blog / Substack cadence (published deliberations as proof artifact) **[F+M]**
5. HN post: Show HN after Experiment A-2 results **[F+M]**

*Nothing here until digital strategy is decided.*

---

## Parking Lot — Decided but not scheduled

- **Studio outreach for Practice Buddy** — next studio after KIC is working well **[F: drives]**
- **Resonant Mind Phase 1.5** — multi-model orchestra, after Experiment B results
- **Canva integration** — Phase 2 of web app, after KIC beta validates
- **Teacher dashboard** — Practice Buddy Phase 2
- **Ensemble listening** — Practice Buddy Phase 2
- **Desktop app (Tauri)** — when Resonant Mind is production-ready
- **Subscription billing** — after beta validates value

---

## How to use this

- Check boxes in the GitHub UI (pencil icon, check the box, commit) or tell Claude "done: X"
- Claude reads this at the start of any session where it's relevant
- Update the "Updated" date and thread status when things change
- Add new threads as they emerge; move completed threads to Parking Lot
