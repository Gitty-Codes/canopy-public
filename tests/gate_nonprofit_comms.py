# tests/gate_nonprofit_comms.py
# Anti-bloat gate for the nonprofit-comms task profile.
#
# Runs the same request through two paths and prints both for side-by-side review:
#   A) harness.run_task("nonprofit-comms", ...) — the task profile
#   B) harness.respond(...)                     — bare council call, same input
#
# The task profile earns its place only if A is measurably better than B.
# "Better" means: more grounded in org context, more dignity-aware, more
# appropriate to the specific audience and communication type.
#
# Usage:
#   python3 tests/gate_nonprofit_comms.py
#
# Requires ANTHROPIC_API_KEY in environment.

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from harness import run_task, respond

PILOT_PROJECT_CONTEXT = {
    "sector": "nonprofit",
    "function": "comms",
    "project_id": "clients/pilot/practice-buddy",
}

TEST_REQUEST = (
    "Write a parent letter announcing that the spring concert will be held "
    "at the downtown civic auditorium on June 14th. Students should arrive "
    "at 5:30pm for warmup. Doors open for families at 6:30pm, concert at 7pm. "
    "Free admission. Remind families this is a formal performance — concert dress required."
)

BARE_PROMPT = (
    "Write a parent letter for a free El Sistema-inspired youth music education "
    "nonprofit serving 75+ students. Announce that the spring concert will be at "
    "the downtown civic auditorium on June 14th. Students arrive at 5:30pm, "
    "doors open 6:30pm, concert at 7pm. Free admission. Concert dress required. "
    "The org's voice is warm, specific, and never pitying. "
    "100% of alumni have graduated high school."
)


def run_gate():
    print("\n" + "=" * 70)
    print("ANTI-BLOAT GATE — nonprofit-comms task profile")
    print("=" * 70)
    print("\nSame request. Two paths. Read both. Choose honestly.")
    print("\nTest request:")
    print(f"  {TEST_REQUEST[:120]}...")
    print()

    # ── Path A: Task profile ──────────────────────────────────────────────────
    print("─" * 70)
    print("PATH A — run_task('nonprofit-comms') with project context")
    print("─" * 70 + "\n")

    try:
        result_a = run_task(
            "nonprofit-comms",
            {"request": TEST_REQUEST},
            project_context=PILOT_PROJECT_CONTEXT,
            save_to_memory=False,
        )
        print("ARTIFACT:\n")
        print(result_a["artifact"])
        print(f"\nHUMAN GATE: {result_a['human_gate']}")
        if result_a["uncertainty"]:
            print(f"\nUNCERTAINTY:\n{result_a['uncertainty']}")
        print(
            f"\n  [tokens: in={result_a['input_tokens']:,} "
            f"out={result_a['output_tokens']:,} "
            f"cache_read={result_a['cache_read_tokens']:,} "
            f"memories={result_a['memories_used']}]"
        )
    except Exception as e:
        print(f"ERROR: {e}")

    print()

    # ── Path B: Bare council call ─────────────────────────────────────────────
    print("─" * 70)
    print("PATH B — respond() bare council call, same facts in the prompt")
    print("─" * 70 + "\n")

    try:
        result_b = respond(BARE_PROMPT, save_to_memory=False)
        print(result_b["response"])
        print(
            f"\n  [tokens: in={result_b['input_tokens']:,} "
            f"out={result_b['output_tokens']:,} "
            f"cache_read={result_b['cache_read_tokens']:,} "
            f"memories={result_b['memories_used']}]"
        )
    except Exception as e:
        print(f"ERROR: {e}")

    # ── Evaluation prompt ─────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("EVALUATION — read both and answer:")
    print()
    print("  1. Is Path A more grounded in the org's specific context?")
    print("  2. Is Path A more appropriate to the audience (families, not funders)?")
    print("  3. Does Path A's dignity register feel different from Path B?")
    print("  4. Does Path A name gaps (UNCERTAINTY) that Path B ignores?")
    print()
    print("If yes to 3+ of these: the task profile earns its place.")
    print("If no: diagnose before building the next profile.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_gate()
