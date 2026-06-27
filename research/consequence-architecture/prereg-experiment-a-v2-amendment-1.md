# Pre-Registration Amendment — Experiment A-2, Amendment 1
**Date:** 2026-06-21
**Amends:** `prereg-experiment-a-v2.md` (signed 2026-06-09)
**Status:** DRAFT — requires founder sign-off before data collection resumes
**Author:** The Canopy (Steward review, Builder design, founder deliberation 2026-06-21)

---

## What this amendment changes

One thing only: **how the Operator state summary is generated and injected** in the
treatment condition.

The pre-registration describes the summary as written by the Operator at session open,
reading from episodic memory. This amendment replaces that manual process with an MCP
server (`consequence/mcp_server.py`) that generates and returns the summary automatically
when called at treatment session open.

**Everything else is unchanged:**
- Hypothesis — identical
- Signal source — identical (`memory/episodic/_council/`, dissent records, outcome notes)
- State summary format — identical (the same six fields; see v2 §Signal Source)
- Rubric — identical (Appendix A, five criteria)
- Sample size — identical (N=88 prompt pairs)
- Success criteria — identical (Cohen's d ≥ 0.3, 95% CI, p < 0.05, kappa ≥ 0.6)
- Control condition — identical (no summary injected)
- Evaluator protocol — identical (3–5 blind raters)

---

## Why this amendment

The pre-registration specifies that the Operator summary is "written by the Operator at
the start of each treatment session." In practice, this means manual composition from
episodic memory — a discipline-dependent process that introduces variability into the
treatment condition. If the summary is written inconsistently across sessions (different
fields selected, different depth), treatment fidelity degrades.

The MCP server removes that variability. The same code path generates the state summary
on every treatment session call, reading from the same memory sources, formatted
identically. This improves treatment condition reliability without changing what is
being injected or why.

**The honest argument for this change is ecological validity, not cost.** The Claude
Code session surface is where Canopy deliberation actually happens. The MCP server wires
the consequence architecture into that surface as a native tool rather than a manual
discipline overlay. Signal collected this way is more representative of real use.
Cost reduction is a secondary benefit, not the rationale.

---

## What the MCP server does

`consequence/mcp_server.py` exposes three tools:

**`get_homeostatic_state()`** — reads `memory/episodic/_council/`, dissent records,
and outcome notes; formats and returns the Operator state summary in the format
specified in v2. Called at the open of each treatment session. This replaces the
manual Operator summary step.

**`log_interoception_event(event_type, content, severity)`** — writes a structured
event to `data/homeostatic_history.jsonl` during a session. Called on named triggers:
Check 0 fires, DISSENT fires, irreversible consequence threshold crossed, kaizen runs.
This enriches the signal store between sessions.

**`close_session(summary)`** — writes a session record to the episodic store at session
close. This captures sessions that currently produce no episodic record (any Claude Code
session that does not explicitly run `/council`).

The data model for `homeostatic_history.jsonl` is unchanged. The MCP server writes to
the same format the consequence architecture already uses.

---

## Research integrity notes

**The treatment sessions write to the signal store.** Sessions in the treatment
condition will call `log_interoception_event()` and `close_session()`, adding records
to the same episodic store that `get_homeostatic_state()` reads for future sessions.
This is intentional — it is how signal accumulates — and it is not contamination. The
hypothesis claims that more signal produces better outcomes; the feedback loop is the
mechanism under test, not a confound.

What would be contamination: modifying the episodic records of prior sessions, or
generating artificial signal outside of real sessions. Neither occurs here.

**The control condition is unaffected.** Control sessions do not call
`get_homeostatic_state()` and do not receive the state summary. The MCP server's
existence does not change what the control condition experiences.

**Manual summary baseline.** If any treatment sessions were run under the manual
Operator summary protocol (v2 as written, before this amendment), those sessions
should be logged separately and excluded from the primary analysis. They may be
reported as an exploratory comparison: does MCP-generated summary show different
effect size than manually-composed summary? This is post-hoc and will be labeled as
such.

---

## What this amendment does not change

The pre-registration question — "does injecting structured session history change
measurable output behavior?" — is unchanged. The amendment affects how the injection
is delivered, not what is injected or what we're measuring.

The minimum signal threshold before data collection (≥ 20 council sessions, ≥ 5
DISSENT records, ≥ 3 outcome notes) is unchanged. The MCP server may accelerate
reaching that threshold by capturing sessions that previously produced no record, but
the threshold requirement stands.

---

## Founder sign-off

This amendment is complete when the founder reads it, confirms it accurately describes
the intended change, and signs off.

**This amendment must not be modified after founder sign-off.**
The original pre-registration (`prereg-experiment-a-v2.md`) remains the primary
document; this amendment specifies the single deviation from it.

Sign-off: ___________________ Date: ___________________
