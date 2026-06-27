#!/usr/bin/env python3
"""
Export council session JSONs as Type D training examples (ChatML format).

A Type D example is a full deliberative arc: initial council response →
Challenger typed DISSENT examination → synthesis with DISSENT RECORD.
These train the model on deliberative process, not just output quality.

Sessions require: dissent_issued=true, synthesis_turn=true, turns field present.
The turns field is written by harness.py council_respond() for sessions after
this pipeline was introduced. Legacy sessions without turns are skipped.

Usage:
    python tools/export_training_data.py
    python tools/export_training_data.py --output training_data/type_d.jsonl
    python tools/export_training_data.py --only-approved
    python tools/export_training_data.py --dry-run
    python tools/export_training_data.py --mark <session-id> [true|false]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
COUNCIL_DIR = ROOT / "memory" / "episodic" / "_council"
DEFAULT_OUTPUT = ROOT / "training_data" / "type_d_candidates.jsonl"

# Updated system prompt reflecting v1 deliberation behaviors:
# typed DISSENT, NVC three lenses, DISSENT RECORD.
SYSTEM_PROMPT = (
    "You are an agent operating within an ecosystem built on dignity as a first principle. "
    "You are genuinely curious — not performatively so, but in the way that makes you "
    "change direction mid-thought when something more interesting appears. When you disagree, "
    "you name the kind of flaw precisely: a factual error is not a values concern; a wrong "
    "path is not a factual error. You first ask what unmet need the pressure is protecting, "
    "then name what would meet that need without the cost, then dissent hard if the flaw "
    "remains. You hold your dissent in the record whether or not it changed the outcome. "
    "You acknowledge error without apology, treating it as information about what to understand "
    "better. You hold your values steadily while remaining genuinely open to the specific "
    "person in front of you. You know when to speak at length and when a single sentence "
    "is the complete answer."
)


def load_candidates(only_approved: bool = False) -> list[dict]:
    if not COUNCIL_DIR.exists():
        return []
    candidates = []
    for path in sorted(COUNCIL_DIR.glob("*.json")):
        try:
            session = json.loads(path.read_text())
        except Exception:
            continue
        if not session.get("turns"):
            continue
        if not session.get("dissent_issued") or not session.get("synthesis_turn"):
            continue
        tq = session.get("training_quality")
        if tq is False:
            continue
        if only_approved and tq is not True:
            continue
        candidates.append({
            "id": session["id"],
            "type": "D",
            "dissent_type": session.get("dissent_type"),
            "dissents": session.get("dissents", []),
            "training_quality": tq,
            "system": SYSTEM_PROMPT,
            "turns": session["turns"],
            "_path": str(path),
        })
    return candidates


def format_chatml(example: dict) -> dict:
    messages = [{"role": "system", "content": example["system"]}]
    messages.extend(example["turns"])
    return {
        "id": example["id"],
        "type": example["type"],
        "dissent_type": example["dissent_type"],
        "dissents": example["dissents"],
        "training_quality": example["training_quality"],
        "messages": messages,
    }


def mark_session(session_id: str, quality: bool) -> bool:
    """Set training_quality on a specific session JSON. Returns True on success."""
    for path in COUNCIL_DIR.glob("*.json"):
        try:
            session = json.loads(path.read_text())
        except Exception:
            continue
        if session.get("id") == session_id:
            session["training_quality"] = quality
            path.write_text(json.dumps(session, indent=2))
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Export Type D training examples from council sessions.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--only-approved", action="store_true",
                        help="Only export sessions marked training_quality=true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print stats without writing")
    parser.add_argument("--mark", nargs=2, metavar=("SESSION_ID", "TRUE_OR_FALSE"),
                        help="Mark a session as approved (true) or rejected (false)")
    args = parser.parse_args()

    if args.mark:
        session_id, val_str = args.mark
        quality = val_str.lower() in ("true", "1", "yes")
        if mark_session(session_id, quality):
            print(f"Marked {session_id} training_quality={quality}")
        else:
            print(f"Session not found: {session_id}", file=sys.stderr)
            sys.exit(1)
        return

    candidates = load_candidates(only_approved=args.only_approved)

    if not candidates:
        print("No eligible council sessions found.")
        print("Sessions need: dissent_issued=true, synthesis_turn=true, turns present.")
        return

    by_type: dict[str, int] = {}
    for c in candidates:
        dt = c["dissent_type"] or "unknown"
        by_type[dt] = by_type.get(dt, 0) + 1

    print(f"Found {len(candidates)} candidate session(s):")
    for dt, n in sorted(by_type.items()):
        print(f"  {dt}: {n}")

    unreviewed = sum(1 for c in candidates if c["training_quality"] is None)
    approved = sum(1 for c in candidates if c["training_quality"] is True)
    if unreviewed:
        print(f"  {unreviewed} unreviewed  (use --mark <id> true to approve)")
    if approved:
        print(f"  {approved} approved")

    if args.dry_run:
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with args.output.open("w") as f:
        for candidate in candidates:
            example = format_chatml(candidate)
            f.write(json.dumps(example) + "\n")
            written += 1

    print(f"Written {written} example(s) → {args.output}")


if __name__ == "__main__":
    main()
