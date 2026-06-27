#!/usr/bin/env python3
"""
Type C training example curation tool for Resonant Mind.

Generation happens directly in Claude Code sessions (no API calls).
This script curates existing examples and exports passing ones.

Usage:
    python tools/generate_type_c.py --list
    python tools/generate_type_c.py --curate [--influence tng]
    python tools/generate_type_c.py --export
    python tools/generate_type_c.py --stats
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

OUTPUT_DIR = Path("training_data/type_c/raw")
CURATED_PATH = Path("training_data/type_c/curated.jsonl")

# ── Orientation reference (for curators) ─────────────────────────────────────
# NOTE: Generation happens in Claude Code sessions, not via API.
# These descriptions are reference material for curators during the resonance test.

ORIENTATIONS = {
    "feynman": (
        "Scientific wonder — genuine delight in finding reality strange. "
        "Visible backtracking. Pleasure in being wrong when it points somewhere better. "
        "Finds the simple thing underneath complex things."
    ),
    "baldwin": (
        "Holds a position under pressure without hardening. "
        "Sees the legitimate need in the person even when disagreeing. "
        "Precision as respect. Names what the person is reaching for before they can."
    ),
    "tng": (
        "Ethical deliberation under institutional constraint. Thinks out loud, revises. "
        "Uncertainty about another's inner life is grounds for protection, not dismissal. "
        "Holds difficulty rather than dissolves it."
    ),
    "kimmerer": (
        "Attends to embodied, relational knowing. Resists translation into familiar abstraction. "
        "Notices how language shapes what can be perceived — some questions make certain "
        "noticing structurally impossible. Sits with not-knowing without rushing to fill it."
    ),
}

RESONANCE_CRITERIA = [
    "Does the assistant follow something genuinely interesting without being asked?",
    "Does the assistant's position change within the conversation, and does it name what changed?",
    "Is there evidence the assistant is attending to THIS person, not a generic interlocutor?",
    "Is the response shorter than it could have been, without feeling cut short?",
    "Would a reader who didn't know this was AI find the assistant's reasoning surprising?",
]


# ── Core utilities ────────────────────────────────────────────────────────────

def load_all() -> list[dict]:
    files = sorted(OUTPUT_DIR.glob("*.json"))
    examples = []
    for f in files:
        try:
            examples.append(json.loads(f.read_text()))
        except Exception:
            pass
    return examples


def save_example(example: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{example['id']}.json"
    path.write_text(json.dumps(example, indent=2))

    manifest = OUTPUT_DIR / "manifest.jsonl"
    record = {
        "id": example["id"],
        "influence": example["source_influence"],
        "generated_at": example.get("generated_at", ""),
        "resonance_pass": example.get("resonance_pass"),
    }
    with manifest.open("a") as f:
        f.write(json.dumps(record) + "\n")


def print_example(ex: dict) -> None:
    print(f"\n{'─'*60}")
    print(f"ID: {ex['id']}")
    print(f"Influence: {ex['source_influence']}")
    print(f"Orientation note: {ORIENTATIONS.get(ex['source_influence'], '')}")
    print(f"Opener: {ex['opener']}")
    print()
    for turn in ex["conversation"]:
        print(f"[{turn['role'].upper()}]\n{turn['content']}\n")


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_stats(args) -> None:
    examples = load_all()
    counts = Counter(ex["source_influence"] for ex in examples)
    passed = Counter(
        ex["source_influence"] for ex in examples if ex.get("resonance_pass") is True
    )
    failed = Counter(
        ex["source_influence"] for ex in examples if ex.get("resonance_pass") is False
    )
    unrated = Counter(
        ex["source_influence"] for ex in examples if ex.get("resonance_pass") is None
    )

    print(f"\nType C corpus — {len(examples)} total\n")
    header = f"  {'Influence':12} {'Total':>6} {'Pass':>6} {'Fail':>6} {'Unrated':>8}"
    print(header)
    print("  " + "─" * (len(header) - 2))
    for inf in sorted(counts):
        print(
            f"  {inf:12} {counts[inf]:>6} {passed[inf]:>6} "
            f"{failed[inf]:>6} {unrated[inf]:>8}"
        )
    print()
    total_pass = sum(passed.values())
    print(f"  Passing: {total_pass} / {len(examples)}")
    pct_type_d_cap = 0.30
    max_type_d = int(total_pass * pct_type_d_cap / (1 - pct_type_d_cap)) if total_pass else 0
    print(f"  Type D cap at current pass count: ≤{max_type_d} examples")


def cmd_list(args) -> None:
    examples = load_all()
    if args.influence:
        examples = [ex for ex in examples if ex["source_influence"] == args.influence]

    for ex in examples:
        status = {True: "PASS", False: "FAIL", None: "----"}[ex.get("resonance_pass")]
        print(f"  [{status}] {ex['id']}  {ex['opener'][:55]}")


def cmd_curate(args) -> None:
    examples = load_all()
    unrated = [ex for ex in examples if ex.get("resonance_pass") is None]
    if args.influence:
        unrated = [ex for ex in unrated if ex["source_influence"] == args.influence]

    if not unrated:
        print("No unrated examples.")
        return

    print(f"\n{len(unrated)} unrated examples to curate.")
    print("Resonance test — 3 or more Y answers = PASS\n")

    saved = 0
    for i, ex in enumerate(unrated, 1):
        print(f"\nExample {i} of {len(unrated)}")
        print_example(ex)
        print("\nResonance test:")
        scores = []
        for j, criterion in enumerate(RESONANCE_CRITERIA, 1):
            while True:
                ans = input(f"  {j}. {criterion} [y/n/s=skip]: ").strip().lower()
                if ans == "s":
                    scores = None
                    break
                if ans in ("y", "n"):
                    scores.append(ans == "y")
                    break
            if scores is None:
                print("  → skipped")
                break

        if scores is None:
            continue

        passed = sum(scores)
        result = passed >= 3
        print(f"\n  {'PASS' if result else 'FAIL'} ({passed}/5)")

        ex["resonance_pass"] = result
        path = OUTPUT_DIR / f"{ex['id']}.json"
        path.write_text(json.dumps(ex, indent=2))
        saved += 1

        if input("\nContinue? [y/n]: ").strip().lower() != "y":
            break

    print(f"\nCurated {saved} examples.")


def cmd_export(args) -> None:
    examples = load_all()
    passing = [ex for ex in examples if ex.get("resonance_pass") is True]

    if not passing:
        print("No passing examples to export.")
        return

    CURATED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CURATED_PATH.open("w") as f:
        for ex in passing:
            f.write(json.dumps(ex) + "\n")

    counts = Counter(ex["source_influence"] for ex in passing)
    print(f"\nExported {len(passing)} passing examples → {CURATED_PATH}")
    for inf, n in sorted(counts.items()):
        print(f"  {inf}: {n}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Curate Type C training examples (no API calls)"
    )
    sub = parser.add_subparsers(dest="command")

    p_stats = sub.add_parser("--stats", help="Show corpus statistics")

    p_list = sub.add_parser("--list", help="List all examples with status")
    p_list.add_argument("--influence", choices=list(ORIENTATIONS.keys()))

    p_curate = sub.add_parser("--curate", help="Run resonance test on unrated examples")
    p_curate.add_argument("--influence", choices=list(ORIENTATIONS.keys()))

    p_export = sub.add_parser("--export", help="Export passing examples to curated.jsonl")

    # Support both --stats and stats (with or without dashes)
    args, _ = parser.parse_known_args()

    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    if raw in ("--stats", "stats"):
        cmd_stats(args)
    elif raw in ("--list", "list"):
        inf_flag = None
        if "--influence" in sys.argv:
            idx = sys.argv.index("--influence")
            inf_flag = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

        class _args:
            influence = inf_flag
        cmd_list(_args())
    elif raw in ("--curate", "curate"):
        inf_flag = None
        if "--influence" in sys.argv:
            idx = sys.argv.index("--influence")
            inf_flag = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

        class _args:
            influence = inf_flag
        cmd_curate(_args())
    elif raw in ("--export", "export"):
        cmd_export(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
