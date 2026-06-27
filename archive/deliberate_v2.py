# archive/deliberate_v2.py
# The Canopy — Three-Pass Deliberation Architecture
# Project Sprout v0.3
#
# ARCHIVED: Superseded by harness.py council_respond().
# Preserved as reference for deliberate_v3.py (LangGraph cyclic deliberation).
# The three-pass pattern here (sharpen → answer → examine → synthesize) is
# architecturally distinct from the harness's single-call unconscious mode.
#
# Pass 1: The Listener + Elder sharpen the question
#          What is really being asked? What are we not seeing?
#
# Pass 2: Claude directly answers the enriched question
#          Full frontier reasoning, clean context
#
# Pass 3: Guardian, Steward, Builder, Operator, Inventor examine the answer
#          Not generating — examining. What was missed? What drifted?
#          What's not feasible? What's not true? Is the frame right?
#
# Final:  Claude reads the examination and produces final synthesis
#
# The agent is not the model.
# The council is not competing with Claude.
# The council is doing what Claude alone doesn't do naturally:
# holding role-specific perspective and Constitutional orientation.

import sys
import os
sys.path.insert(0, os.path.expanduser("~/canopy"))

from agents.listener import run_listener
from agents.elder import run_elder
from agents.guardian import run_guardian
from agents.steward import run_steward
from agents.builder import run_builder
from agents.operator import run_operator
from agents.inventor import run_inventor
from models.router import call_model
from memory.store import save_memory


# ── PASS 1: QUESTION SHARPENING ───────────────────────────────────────────────

def pass_one_sharpen(problem: str, engine: str = "local") -> dict:
    """
    The Listener and Elder examine the problem before it's answered.
    Goal: surface what's really being asked and what might be missed.
    Returns enriched context for Pass 2.
    """
    print("\n" + "="*60)
    print("PASS 1 — Sharpening the Question")
    print("="*60 + "\n")

    sharpening = {}

    # The Listener — what is the real pain or need here?
    print("The Listener: sensing the real question...\n")
    listener_prompt = f"""A founder has brought this problem to the council.
Before anyone answers — what is the real question here?
What is named and what is unnamed?
What pain or need sits beneath the surface of what was asked?
What signal would we miss if we rushed to answer?

The problem as submitted:
{problem}

Describe what you sense. Do not answer the question.
Surface what needs to be heard before the answer begins."""

    listener_response = run_listener(listener_prompt, engine=engine)
    sharpening["listener"] = listener_response
    print(f"Listener:\n{listener_response}\n")
    print("-"*60 + "\n")

    # The Elder — what are we not seeing?
    print("The Elder: asking what we might miss...\n")
    elder_prompt = f"""The problem:
{problem}

The Listener sensed:
{listener_response}

Before this question is answered — what are we not seeing?
One question. No more. Make it the question that matters most."""

    elder_response = run_elder(elder_prompt, engine=engine)
    sharpening["elder"] = elder_response
    print(f"Elder:\n{elder_response}\n")
    print("-"*60 + "\n")

    return sharpening


# ── PASS 2: FRONTIER REASONING ────────────────────────────────────────────────

def pass_two_answer(problem: str, sharpening: dict) -> str:
    """
    Claude answers the enriched question directly.
    Always uses cloud — this is the full reasoning pass.
    Clean context: problem + sharpening signals only.
    """
    print("="*60)
    print("PASS 2 — Frontier Reasoning")
    print("="*60 + "\n")
    print("Claude: reasoning from full context...\n")

    system_prompt = """You are a senior strategic advisor with deep expertise
in business formation, product development, legal structures, and
organizational strategy. You reason carefully, acknowledge uncertainty
honestly, and never fabricate specific numbers without stating your
assumptions clearly.

You are operating within The Canopy — a dignity-first organization.
The Cultural Constitution holds these principles:
- Dignity for all parties — human, synthetic, customer, partner
- Genuine value creation, not extraction
- Honest acknowledgment of what is unknown
- The burden of proof is on proceeding, not on pausing
- Build the smallest thing that is genuinely useful, then grow it

Answer with substance. Be specific where you can.
Acknowledge uncertainty where you must.
Do not pad. Do not hedge excessively.
Say what you actually think."""

    enriched_prompt = f"""ORIGINAL PROBLEM:
{problem}

BEFORE YOU ANSWER — the council surfaced these signals:

What The Listener sensed beneath the surface:
{sharpening.get('listener', '')}

What The Elder asked us not to miss:
{sharpening.get('elder', '')}

Now answer the original problem fully, informed by these signals.
Be specific. Be honest. Name your assumptions.
This is a real decision with real consequences."""

    messages = [{"role": "user", "content": enriched_prompt}]
    response = call_model(messages, system_prompt, engine="cloud")

    print(f"Claude:\n{response}\n")
    print("-"*60 + "\n")

    return response


# ── PASS 3: CONSTITUTIONAL EXAMINATION ────────────────────────────────────────

def pass_three_examine(problem: str, claude_answer: str, engine: str = "local") -> dict:
    """
    Guardian, Steward, Builder, Operator, Inventor examine Claude's answer.
    Not generating — examining.
    Each agent asks: what did Claude miss from my perspective?
    """
    print("="*60)
    print("PASS 3 — Constitutional Examination")
    print("="*60 + "\n")

    examination = {}

    # The Guardian — what risks were missed or underweighted?
    print("The Guardian: examining for missed risks...\n")
    guardian_prompt = f"""Claude has answered this problem:

PROBLEM:
{problem}

CLAUDE'S ANSWER:
{claude_answer}

Examine this answer through your lens.
What risks were missed or underweighted?
What harm was not named?
What assumption is dangerous?
What would you flag, and at what severity?
If nothing was missed — say so clearly. Do not manufacture concern.
Be specific. Be honest."""

    guardian_response = run_guardian(guardian_prompt, engine=engine)
    examination["guardian"] = guardian_response
    print(f"Guardian:\n{guardian_response}\n")

    # Check for PAUSE
    if "PAUSE" in guardian_response.upper():
        print("="*60)
        print("GUARDIAN HAS CALLED A PAUSE")
        print("Address this before the council proceeds.")
        print("="*60 + "\n")
        examination["pause_called"] = True
        save_memory(
            agent_name="guardian",
            content=f"PAUSE called examining Claude's answer on: {problem[:100]}",
            memory_type="decision"
        )
        return examination

    print("-"*60 + "\n")

    # The Steward — does this align with who we are?
    print("The Steward: checking Constitutional fidelity...\n")
    steward_prompt = f"""Claude has answered this problem:

PROBLEM:
{problem}

CLAUDE'S ANSWER:
{claude_answer}

Examine this answer through your lens.
Does this align with The Canopy's Cultural Constitution?
Does it honor dignity for all parties?
Does it avoid exploitation?
Did anything drift from our values in the reasoning?
What should be carried forward? What should be questioned?"""

    steward_response = run_steward(steward_prompt, engine=engine)
    examination["steward"] = steward_response
    print(f"Steward:\n{steward_response}\n")
    print("-"*60 + "\n")

    # The Builder — what's actually feasible?
    print("The Builder: examining for feasibility...\n")
    builder_prompt = f"""Claude has answered this problem:

PROBLEM:
{problem}

CLAUDE'S ANSWER:
{claude_answer}

Examine this answer through your lens.
What is actually buildable with current resources?
What timeline assumptions are optimistic or wrong?
What technical debt is being accepted silently?
What would you flag as not feasible now?
Be specific about current stack constraints where relevant."""

    builder_response = run_builder(builder_prompt, engine=engine)
    examination["builder"] = builder_response
    print(f"Builder:\n{builder_response}\n")
    print("-"*60 + "\n")

    # The Operator — what's true about current state?
    print("The Operator: checking against reality...\n")
    operator_prompt = f"""Claude has answered this problem:

PROBLEM:
{problem}

CLAUDE'S ANSWER:
{claude_answer}

Examine this answer through your lens.
What is actually true about current operational state?
What gap exists between what Claude proposed and what is real right now?
What is not yet observable, measurable, or recoverable?
What assumption about current reality is wrong?"""

    operator_response = run_operator(operator_prompt, engine=engine)
    examination["operator"] = operator_response
    print(f"Operator:\n{operator_response}\n")
    print("-"*60 + "\n")

    # The Inventor — is the problem framed right? what assumption could be dissolved?
    print("The Inventor: examining the frame...\n")
    inventor_prompt = f"""Claude has answered this problem:

PROBLEM:
{problem}

CLAUDE'S ANSWER:
{claude_answer}

Examine this answer through your lens.
Is the problem framed correctly, or is the frame itself the constraint?
What assumption in Claude's answer — if dissolved — would open a better path?
What is Claude treating as fixed that might not be fixed?
What would this look like if the obvious approach were not available?
If the frame is right and the answer is sound — say so. Do not invent constraint."""

    inventor_response = run_inventor(inventor_prompt, engine=engine)
    examination["inventor"] = inventor_response
    print(f"Inventor:\n{inventor_response}\n")
    print("-"*60 + "\n")

    return examination


# ── FINAL SYNTHESIS ───────────────────────────────────────────────────────────

def final_synthesis(problem: str, claude_answer: str, examination: dict) -> str:
    """
    Claude reads the examination and produces a final refined answer.
    Always cloud — this is where frontier reasoning meets
    Constitutional examination.
    """
    print("="*60)
    print("FINAL SYNTHESIS")
    print("="*60 + "\n")
    print("Claude: synthesizing examination...\n")

    system_prompt = """You are a senior strategic advisor operating within
The Canopy — a dignity-first organization. You have given an initial answer
and a council of specialized agents has examined it. Read their examination
carefully. Update your answer where they found genuine gaps. Hold your
ground where their concerns are not substantive. Produce a final,
refined answer that is better than your first pass."""

    synthesis_prompt = f"""You answered this problem:

PROBLEM:
{problem}

YOUR INITIAL ANSWER:
{claude_answer}

THE COUNCIL EXAMINED YOUR ANSWER:

Guardian (risks and harm):
{examination.get('guardian', 'Not examined')}

Steward (Constitutional fidelity):
{examination.get('steward', 'Not examined')}

Builder (feasibility):
{examination.get('builder', 'Not examined')}

Operator (current reality):
{examination.get('operator', 'Not examined')}

Now produce your final answer.
Where the council found genuine gaps — address them.
Where their concerns are not substantive — note that and hold your ground.
This should be better than your first pass, not just longer."""

    messages = [{"role": "user", "content": synthesis_prompt}]
    response = call_model(messages, system_prompt, engine="cloud")

    print(f"Final Answer:\n{response}\n")
    print("-"*60 + "\n")

    return response


# ── MAIN DELIBERATION ─────────────────────────────────────────────────────────

def deliberate_v2(problem: str, examination_engine: str = "local") -> dict:
    """
    Full three-pass deliberation.

    examination_engine: engine for Pass 1 and Pass 3 agents
    Pass 2 and Final Synthesis always use cloud.
    """
    print("\n" + "="*60)
    print("THE CANOPY — Three-Pass Deliberation")
    print("Project Sprout v0.3")
    print(f"Examination engine: {examination_engine}")
    print("Reasoning engine: cloud (always)")
    print("="*60)
    print(f"\nProblem:\n{problem}\n")
    print("="*60)

    record = {
        "problem": problem,
        "examination_engine": examination_engine
    }

    # Pass 1: Sharpen
    sharpening = pass_one_sharpen(problem, engine=examination_engine)
    record["sharpening"] = sharpening

    # Pass 2: Answer
    claude_answer = pass_two_answer(problem, sharpening)
    record["claude_answer"] = claude_answer

    # Pass 3: Examine
    examination = pass_three_examine(
        problem, claude_answer, engine=examination_engine
    )
    record["examination"] = examination

    if examination.get("pause_called"):
        print("Council paused. Address Guardian findings before synthesis.\n")
        return record

    # Final Synthesis
    final = final_synthesis(problem, claude_answer, examination)
    record["final"] = final

    # Save to memory
    summary = f"""Three-pass deliberation on: {problem[:150]}

Elder asked: {sharpening.get('elder', '')[:150]}
Claude initial: {claude_answer[:200]}
Final synthesis: {final[:200]}"""

    save_memory(
        agent_name="steward",
        content=summary,
        memory_type="project"
    )

    print("="*60)
    print("DELIBERATION COMPLETE — Three-Pass")
    print("="*60)
    print(f"\nPasses completed: Sharpen → Answer → Examine → Synthesize")
    print("Deliberation saved to Steward memory.\n")

    return record


# ── SESSION ───────────────────────────────────────────────────────────────────

def deliberation_session():
    print("\n" + "="*60)
    print("THE CANOPY — Council Chamber v2")
    print("Project Sprout v0.3 — Three-Pass Architecture")
    print("="*60)
    print("\nArchitecture:")
    print("  Pass 1: Listener + Elder sharpen the question (local or cloud)")
    print("  Pass 2: Claude answers with full frontier reasoning (always cloud)")
    print("  Pass 3: Guardian, Steward, Builder, Operator examine (local or cloud)")
    print("  Final:  Claude synthesizes examination (always cloud)")
    print("\nType 'exit' to close.\n")

    while True:
        # Examination engine
        print("Examination engine for Pass 1 + Pass 3 (enter for 'local', or 'cloud'): ",
              end="", flush=True)
        exam_engine = input().strip().lower()
        if not exam_engine:
            exam_engine = "local"
        if exam_engine in ["exit", "quit", "bye"]:
            print("\nCouncil adjourned.\n")
            break
        if exam_engine not in ["local", "cloud"]:
            exam_engine = "local"

        print(f"Pass 1+3 engine: {exam_engine}")
        print("Pass 2 + Final: cloud (always)\n")

        # Problem
        print("Problem (type END on its own line when done):\n")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            if line.strip() in ["exit", "quit", "bye"]:
                print("\nCouncil adjourned.\n")
                return
            lines.append(line)

        problem = "\n".join(lines).strip()
        if not problem:
            continue

        deliberate_v2(problem, examination_engine=exam_engine)

        print("\nBring another problem, or type 'exit' to close.\n")


if __name__ == "__main__":
    deliberation_session()
