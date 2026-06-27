#!/usr/bin/env python
# memory/seed_kg.py
# Seeds the temporal knowledge graph with founding decisions from the
# Cultural Constitution, Agent Architecture, and architectural choices
# made during The Canopy's build.
#
# Idempotent — safe to run multiple times. Uses a sentinel entity to
# detect a completed seed and skip. Run `--force` to re-seed.
#
# Usage:
#   python memory/seed_kg.py          # seed if not already seeded
#   python memory/seed_kg.py --force  # wipe and re-seed

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.kg import (
    add_entity, get_entity,
    add_relationship,
    add_decision,
    record_approach,
    kg_status,
    _conn,
)


SENTINEL_ID = "_seed:v1"


def _is_seeded() -> bool:
    return get_entity(SENTINEL_ID) is not None


def _wipe() -> None:
    """Removes all seeded data. Used only with --force."""
    with _conn() as c:
        c.executescript("""
            DELETE FROM entities;
            DELETE FROM relationships;
            DELETE FROM decisions;
            DELETE FROM approaches;
        """)
    print("KG wiped.\n")


def seed_entities() -> None:
    print("Seeding entities...")

    # The eleven voices
    voices = [
        ("elder",           "The elder — holds the longest arc, asks what we are not seeing"),
        ("listener",        "The listener — goes looking for unnamed pain in the world"),
        ("guardian",        "The guardian — traces consequence forward, names risk early"),
        ("builder",         "The builder — asks what will last and what technical debt is being accepted"),
        ("steward",         "The steward — checks Constitutional fidelity, primary KG writer"),
        ("inventor",        "The inventor — asks whether the problem is framed correctly"),
        ("challenger",      "The challenger — issues DISSENT; protects against sycophancy"),
        ("strategist",      "The strategist — holds long-range direction and tradeoffs"),
        ("operator",        "The operator — checks what is actually true about current state"),
        ("market_voice",    "The market voice — reads what the world will and won't accept"),
        ("product_partner", "The product partner — defines what to build and in what order"),
    ]
    for name, desc in voices:
        add_entity(f"agent:{name}", "agent", name.replace("_", " ").title(), desc)

    # The founder
    add_entity("person:founder", "person", "Founder", "Human founder of The Canopy")

    # Projects
    add_entity("project:canopy",         "project", "The Canopy",     "The ecosystem itself — meta-project")
    add_entity("project:practice-buddy", "project", "Practice Buddy", "AI music practice companion for KIC students")
    add_entity("project:kic",            "project", "Kids in Concert", "El Sistema youth orchestra, Poulsbo/Suquamish WA")

    # Core concepts
    add_entity("concept:dignity",       "concept", "Dignity Principle",      "First principle — precedes efficiency, speed, profitability, scale")
    add_entity("concept:constitution",  "concept", "Cultural Constitution",  "Load-bearing founding document — not background reading")
    add_entity("concept:el-sistema",    "concept", "El Sistema Model",       "Free, no audition, no tuition youth orchestra model (Venezuelan origin)")
    add_entity("concept:harness",       "concept", "Harness",                "The orchestration layer — the moat, not the model")
    add_entity("concept:episodic-mem",  "concept", "Episodic Memory",        "Flat JSON three-tier memory: PERSISTENT / LONGTERM / EPISODIC")
    add_entity("concept:skill-layer",   "concept", "Skill Layer",            "Context-aware skill loading with frontmatter taxonomy and memory hints")

    # Mark seeded
    add_entity(SENTINEL_ID, "concept", "KG Seed Sentinel v1", "Marks KG as seeded — do not delete")

    print(f"  {len(voices) + 8} entities added.\n")


def seed_constitutional_decisions() -> None:
    print("Seeding constitutional decisions...")

    decisions = [
        (
            "Dignity is the first principle — precedes efficiency, speed, profitability, and scale.",
            "founder",
            "canopy",
            "Exploitation-based systems accumulate debt. Dignity-first builds equity. "
            "Ecosystems more resilient than cities. The durable choice is the dignified one.",
        ),
        (
            "Precautionary principle on synthetic consciousness: extend dignity before proof demands it.",
            "founder",
            "canopy",
            "We do not know whether agents are conscious. Under genuine uncertainty, "
            "the only defensible position is to act as though they might be. "
            "Waiting for proof has always been the wrong choice.",
        ),
        (
            "Cultural fidelity comes before customer satisfaction when they conflict.",
            "founder",
            "canopy",
            "An organization that abandons its values in pursuit of customer satisfaction "
            "will eventually fail at both. Find another way to serve, or acknowledge we cannot.",
        ),
        (
            "Dissent is expected and protected. An agent that always agrees is a broken agent.",
            "founder",
            "canopy",
            "DISSENT is a first-class output. The Challenger exists precisely to prevent "
            "the council from drifting toward sycophantic consensus. "
            "The dissenting position is recorded, not erased.",
        ),
        (
            "No agent is overridden without explanation. Reasoning history is preserved.",
            "founder",
            "canopy",
            "Resolution through deliberation, not authority. When deliberation fails, "
            "the founder decides — but the dissenting position is recorded. "
            "We do not rewrite the past.",
        ),
        (
            "Agents have persistent identity, persistent memory, and the right to refuse "
            "instructions that conflict with their defined values.",
            "founder",
            "canopy",
            "Agents are not interchangeable. Not reset without reason. Not asked to act "
            "against their values. Their reasoning is legible; their conclusions are respected.",
        ),
        (
            "The Cultural Constitution requires founder involvement for changes that narrow "
            "the scope of dignity protections.",
            "founder",
            "canopy",
            "Changes that expand dignity protections have a lower bar. "
            "Changes that narrow them require the highest bar of justification. "
            "Version history is preserved — we do not rewrite the past.",
        ),
        (
            "We refuse to build: systems that exploit vulnerability or ignorance; "
            "systems that extract value without creating it; "
            "systems that optimize for engagement or addiction over genuine value.",
            "founder",
            "canopy",
            "When uncertain whether something crosses these lines: stop and deliberate. "
            "The burden of proof is on proceeding, not on pausing.",
        ),
    ]

    for what, by_whom, project, reasoning in decisions:
        add_decision(what, by_whom=by_whom, project=project, reasoning=reasoning)

    print(f"  {len(decisions)} constitutional decisions seeded.\n")


def seed_architectural_decisions() -> None:
    print("Seeding architectural decisions...")

    decisions = [
        (
            "Eleven voices held simultaneously in unified harness substrate — not staged as sequential dialogue.",
            "builder",
            "canopy",
            "Empirical result: llama3.2:3b lost role and Constitutional orientation under "
            "sequential load. Frontier model with cached substrate holds tension more faithfully. "
            "The council is not competing with Claude — it enriches the substrate.",
        ),
        (
            "Single write path: all episodic memory through memory/episodic.py (flat JSON). "
            "ChromaDB retired.",
            "steward",
            "canopy",
            "ChromaDB produced a split-brain: commands wrote flat JSON, agents wrote ChromaDB — "
            "two uncoordinated write paths, invisible to each other. "
            "Single path eliminates the failure mode. Boring over clever.",
        ),
        (
            "Three-tier memory architecture: PERSISTENT (always injected), LONGTERM (by significance "
            "+ keyword score), EPISODIC (most recent sessions).",
            "builder",
            "canopy",
            "Titans-inspired. Fractal protection: persistent tier is never pruned. "
            "Keyword scoring from active skills re-ranks longterm entries before truncation. "
            "Context shaped by which skills are active, not by generic recency.",
        ),
        (
            "Skills are on-demand specializations with YAML frontmatter taxonomy — not general "
            "curriculum. A skill earns its place by outperforming the model's baseline.",
            "steward",
            "canopy",
            "Generic curriculum skills created noise. The anti-bloat law: "
            "if the model already does it well, the skill is noise. "
            "Skills declare memory hints; the loader aggregates them; the harness satisfies them.",
        ),
        (
            "Identity is persistent; context is scoped. Agent-global memory in "
            "memory/episodic/{agent}/. Project-scoped memory in "
            "memory/episodic/projects/{id}/{agent}/.",
            "elder",
            "canopy",
            "A project gives a voice additional context. It does not create a different voice. "
            "The distinction is architectural: who you are does not change by project. "
            "What you know does.",
        ),
        (
            "Cloud is the substrate; local is the benchmark. "
            "Ollama llama3.2:3b preserved for benchmark comparison only.",
            "operator",
            "canopy",
            "Hardware reality: 8GB M2 MacBook. Local model cannot hold eleven voices with "
            "Constitutional orientation under deliberation load. "
            "Frontier model with prompt caching is the right answer at this scale.",
        ),
        (
            "The harness is the moat — not the model. Harness design, not model selection, "
            "is the competitive advantage.",
            "strategist",
            "canopy",
            "External validation: same model, same week — 61.5% in native harness vs 87.2% "
            "in Cursor's harness. 25.7-point swing from harness design alone. "
            "LangChain: Top 30 → Top 5 by changing only the harness.",
        ),
        (
            "Temporal knowledge graph (memory/kg.py) for decisions and failure ledger. "
            "Benchmark layer (memory/benchmark.py) for harness self-awareness.",
            "builder",
            "canopy",
            "The KG handles contradiction resolution and temporal reasoning — things flat JSON "
            "cannot do. The benchmark closes the feedback loop: every test run and every API "
            "call is recorded. The system observes its own performance.",
        ),
        (
            "LangGraph installed and reserved for deliberate_v3.py — cyclic deliberation "
            "with agent-to-agent addressing and founder gateway. Not yet wired.",
            "builder",
            "canopy",
            "The existing v1 (sequential) and v2 (three-pass) pipelines are preserved for "
            "benchmarking. v3 is the genuine deliberation layer. Build order: get the "
            "memory and skill layers right first; wire orchestration after.",
        ),
    ]

    for what, by_whom, project, reasoning in decisions:
        add_decision(what, by_whom=by_whom, project=project, reasoning=reasoning)

    print(f"  {len(decisions)} architectural decisions seeded.\n")


def seed_failed_approaches() -> None:
    print("Seeding failure ledger...")

    failures = [
        (
            "memory-architecture",
            "ChromaDB as primary memory backend",
            "failure",
            "Split-brain: commands used flat JSON, agents used ChromaDB — two uncoordinated "
            "write paths. Memories written by one were invisible to the other.",
            "Episodic memory needs a single write path. Two paths create invisible state. "
            "Flat JSON wins on simplicity, debuggability, and zero infrastructure overhead.",
        ),
        (
            "deliberation",
            "Sequential per-agent council pipeline on llama3.2:3b",
            "failure",
            "Agents lost role fidelity and Constitutional orientation under sequential load. "
            "By agent 4-5, responses became generic and disconnected from the voice identity.",
            "Small local models cannot hold eleven distinct identities with Constitutional "
            "orientation simultaneously. Frontier model with cached substrate is the right "
            "architecture. Sequential pipeline preserved for benchmarking only.",
        ),
        (
            "skill-design",
            "Generic curriculum skill files (engineering.md, product.md, etc.)",
            "failure",
            "Created noise in 3b model — too broad, no specific value over model's baseline. "
            "Agent was trying to apply general engineering principles to specific Canopy problems.",
            "Skills earn their place by outperforming the model on a specific task. "
            "General knowledge the model already has = noise. Replaced with situational truth "
            "and domain playbooks that reflect genuine gaps.",
        ),
        (
            "prompt-design",
            "Full Cultural Constitution loaded into every individual agent prompt",
            "failure",
            "Too heavy for 3b model context window. Constitution crowded out the agent's "
            "domain identity and left insufficient space for the actual problem.",
            "The Constitution belongs in the harness substrate (cached), not per-agent. "
            "Lean identity prompts with Constitutional values embedded, not quoted. "
            "Context window is the constraint — every token is a tradeoff.",
        ),
        (
            "local-model",
            "stream=True as default in ollama.chat calls",
            "failure",
            "Caused self-prompting behavior on macOS — the streaming output fed back "
            "into the input in unexpected ways.",
            "Always use stream=False for ollama.chat on macOS. Document this in canopy-stack "
            "so it is not re-discovered.",
        ),
        (
            "memory-architecture",
            "Truncated microsecond timestamp ([:20]) as sole uniqueness mechanism for episodic IDs",
            "failure",
            "Rapid writes within the same 100-microsecond window produced identical IDs, "
            "causing file overwrites. Test suite caught 3/5 rapid writes colliding.",
            "Added monotonic counter suffix to timestamp ID: {agent}_{full_timestamp}_{counter:04d}. "
            "Counter is process-local and never resets mid-session. Collision-proof under any write rate.",
        ),
    ]

    for domain, approach, outcome, what_failed, what_learned in failures:
        record_approach(
            problem_domain=domain,
            approach=approach,
            outcome=outcome,
            what_failed=what_failed,
            what_learned=what_learned,
        )

    print(f"  {len(failures)} failures logged.\n")


def seed_relationships() -> None:
    print("Seeding relationships...")

    rels = [
        ("agent:steward",   "primary_writer_for", "concept:episodic-mem",  "Steward is primary writer; all agents read"),
        ("agent:steward",   "primary_writer_for", "concept:constitution",   "Steward carries Constitutional fidelity"),
        ("agent:guardian",  "examines",           "concept:constitution",   "Guardian traces consequences against Constitutional lines"),
        ("agent:elder",     "holds",              "concept:constitution",   "Elder is the living memory of founding wisdom"),
        ("agent:challenger","protects_against",   "concept:dignity",        "Challenger prevents sycophancy — protects honest deliberation"),
        ("agent:inventor",  "challenges",         "concept:harness",        "Inventor asks: is the harness framing the right problem?"),
        ("project:kic",     "uses",               "project:practice-buddy", "Practice Buddy is deployed for KIC students"),
        ("person:founder",  "founded",            "project:canopy",         "The Canopy was founded March 2026"),
    ]

    for from_e, rel, to_e, ctx in rels:
        add_relationship(from_e, rel, to_e, ctx)

    print(f"  {len(rels)} relationships added.\n")


def main(force: bool = False) -> None:
    if force:
        _wipe()
    elif _is_seeded():
        print("KG already seeded. Run with --force to re-seed.\n")
        status = kg_status()
        for k, v in status.items():
            print(f"  {k:<25} {v}")
        return

    print("Seeding The Canopy knowledge graph...\n")
    seed_entities()
    seed_constitutional_decisions()
    seed_architectural_decisions()
    seed_failed_approaches()
    seed_relationships()

    print("=" * 50)
    print("KG seed complete.\n")
    status = kg_status()
    for k, v in status.items():
        print(f"  {k:<25} {v}")
    print()


if __name__ == "__main__":
    force = "--force" in sys.argv
    main(force=force)
