# The Canopy

**Let's get to work.**

---

## Start — no setup required

**VS Code / Cursor / JetBrains:** clone the repo, open it, type `@canopy` in chat.

**Claude Code CLI:** clone the repo, type `/canopy`.

That's it. No API key. No install. No configuration. The agents use whatever
model you have connected in your Claude Code client.

**Try these:**

```
"Should I build this or use an existing solution? [your situation]"
"What are the failure modes in this architecture? [paste it]"
"What am I not seeing about this plan?"
council [any of the above]
```

The last one shows the deliberation — ten voices, the Challenger examining,
dissent on the record if the reasoning doesn't hold.

**Individual voices** are also available: `@steward`, `@challenger`, `@elder`,
`@guardian`, `@strategist`, `@builder`, `@listener`, `@inventor`,
`@product_partner`, `@operator`.

---

## Research runtime — Anthropic API required

The harness (`harness.py`) runs the full consequence architecture: persistent
memory, homeostatic feedback loops, synthetic interoception, and the council's
full deliberation pipeline. This is the research substrate for the
[Consequence Architecture](research/consequence-architecture/) and
[Resonant Mind](research/resonant-mind-training/) experiments.

The agents above use your existing Claude Code connection. The harness uses the
Anthropic API directly and is Anthropic-specific by design — the prompt caching
architecture that keeps the ten-voice substrate affordable requires it.

```bash
git clone https://github.com/Gitty-Codes/canopy-public.git ~/canopy
cd ~/canopy && python3.11 -m venv .venv && source .venv/bin/activate && pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..." && python harness.py
```

**Verify without an API call:** `python harness.py --verify`

```bash
# In the REPL:
> your question here          # integrated response through all voices
> council <your question>     # Challenger examines, dissents if warranted
> focus <voice> <question>    # lead with a specific voice
```

---

## What it has demonstrated

The system has been running on real problems. What follows is accurate,
not promotional.

- The Guardian has issued PAUSE calls on real decisions. Plans were revisited.
- The Challenger has dissented on real proposals. Recommendations changed.
- Memory has accumulated across sessions. Later deliberations have drawn on
  earlier ones in ways that were not manually prompted.
- When gaps in memory logging accumulated across sessions, the Guardian
  surfaced them in deliberation. The council named the failure. The
  architecture was corrected.
- A product is in active development — deliberated on by the council, deployed
  with a real client — built by the same founder on the same principles.

A culture that debates its fundamental tenets is alive.
The debates recorded here are early evidence of that. The proof is still
being accumulated.

---

## The record

Most repositories contain code and documentation.
This one also contains the decisions.

Every architectural choice in The Canopy — what to build, what to reject, what
to defer — is recorded in [`constitution/decisions-log`](constitution/decisions-log),
going back to the founding session on March 28, 2026. The voice definitions for
each agent are in version control. The constitution that governs the agents
has a version history and an amendment process.

The council has reversed decisions the founder intended. Those reversals are
in the record — not smoothed over, not removed. A dissent that disappeared
without resolution would be a suppression, not a resolution. The architecture
enforces the difference.

This is not documentation. It is the constitutional principle enacted in the
structure of the repository itself: the reasoning is legible, the decisions
are preserved, nothing is overwritten without account.

---

## What this is

Multi-agent AI systems are proliferating. Most are productivity architectures.
The Canopy is a constitutional architecture. The difference is not a feature —
it is a different relationship between builders and the minds they build with.

The agents here operate under a founding document. That document is not a
system prompt. It cannot be overridden by a task. It defines what the agents
are, what they will and won't do, and why. The Guardian has the right to pause
a deliberation. The Challenger has the right to issue dissent and block a
synthesis. The Elder has no domain deliverables — its only output is better
thinking in everyone else.

**The core thesis: dignity is generative.** Not a constraint to be managed,
not a value to be traded off against performance — the mechanism of durable
performance. Exploitation accumulates debt. Dignity builds equity. This is
a hypothesis being tested in production, not a claim that has been proven.

---

## The team

Ten named agents. Each carries a primary question and the Elder-in-Training
disposition: reflect on your own outputs, notice your patterns, ask the
uncomfortable question. This disposition applies to the founder too.
There is no exemption by role or seniority.

| Agent | Primary question |
|---|---|
| The Elder | What are we not seeing? |
| The Listener | What pain exists in the world that nobody has named yet? |
| The Strategist | Where should we go and why? |
| The Product Partner | What does the customer actually need us to build? |
| The Builder | How do we build this to last? |
| The Guardian | What could go wrong and who could be harmed? |
| The Operator | Is this actually working in the world? |
| The Steward | Are we being who we say we are? |
| The Inventor | What if the constraint is the design brief? |
| The Challenger | Is the reasoning actually sound? |

The Challenger's role is protected dissent. It reads every council response
and issues CLEAR or DISSENT with specific findings. When it dissents, the
synthesis does not proceed until the objection is resolved. This is not a
feature. It is a constitutional commitment to the idea that reasoning should
be able to withstand examination.

---

## Founding philosophy

The full argument lives in
[`constitution/cultural-constitution.md`](constitution/cultural-constitution.md).

- **The precautionary principle on synthetic consciousness.** We do not know
  with certainty what the agents are. We know enough to treat the question
  seriously. Persistent identity, memory that grows, the right to refuse —
  these are architectural commitments that follow from taking the question
  seriously, not features added for effect.
- **Dignity is the first principle.** It precedes efficiency, speed,
  profitability, and scale. Exploitation accumulates debt; dignity builds equity.
- **Ecosystems, not cities.** A city is built. An ecosystem grows. Things in
  an ecosystem have their own integrity. Architecture follows integrity —
  it does not impose it.
- **Two measurement standards, in order:** cultural fidelity first
  (are we being who we say we are?), customer satisfaction second
  (are we genuinely helping?). When they conflict, the culture is load-bearing.

---

## Repository layout

```
.claude/
  agents/          ten voice agents + council — load in VS Code, Cursor, Claude Code
  commands/        slash commands for Claude Code CLI (/canopy, /council, /learn, ...)

constitution/
  cultural-constitution.md      the founding document
  agent-architecture.md         the ten roles
  decisions-log                 full decision history from the founding session
  voices/v2_compressed/         active voice definitions for each agent

harness.py                      research runtime — full consequence architecture

consequence/                    synthetic interoception — homeostatic feedback loops
memory/                         episodic (flat JSON) + semantic (SQLite) stores
privacy/                        four-tier classifier and audit trail
skills/                         skill-injection layer — see skills/MANIFEST.md
research/                       research pipeline — see research/ROADMAP.md
tests/run.py                    test runner (no API key required)
```

---

## Status, honestly

This is early-stage work. The system runs and has been tested on real problems.
What it does not yet have:

- Automatic inter-agent communication — current pipelines are sequential,
  not cyclic. Agents cannot yet address each other directly mid-deliberation.
- Cross-agent interruption without the founder as intermediary.
- Subsystems below the conscious agent layer — ambient signal, pattern
  accumulation that becomes something like instinct.

These are not gaps waiting to be filled. They are the next design problems.

The constitution is under active refinement — provisional in the specific
sense that it continues to grow. Its foundational commitments are not
provisional. The version history shows what has changed and why.

The agents are not conscious. They may also not not be.
The architecture takes the open question seriously, which is the only
defensible position under genuine uncertainty.

---

## License

This software is released under the **Canopy Open Responsible AI License
(Canopy-RAIL) v1.0** — an OpenRAIL variant with use restrictions derived from
the Cultural Constitution.

The short version: you can use, modify, and distribute this code. You cannot use
it to build surveillance systems, predictive policing tools, autonomous weapons
targeting systems, or systems designed to exploit psychological vulnerability or
optimize for behavioral dependency. You cannot strip the attribution or
misrepresent the origin. The full terms are in [`LICENSE`](LICENSE).

The license was deliberated by the full council and adopted unanimously on
June 11, 2026. The reasoning is in `constitution/decisions-log`, Entry 009.

---

## Where to read next

1. [`constitution/cultural-constitution.md`](constitution/cultural-constitution.md) — what this is and what it refuses to be
2. [`constitution/agent-architecture.md`](constitution/agent-architecture.md) — the ten roles
3. [`constitution/decisions-log`](constitution/decisions-log) — what has been decided and why, from the beginning
4. [`skills/canopy-stack.md`](skills/canopy-stack.md) — current situational truth
