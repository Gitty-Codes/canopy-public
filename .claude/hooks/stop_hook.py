#!/usr/bin/env python3
"""
Stop hook — council review gate for founder mode.
Silently exits if CANOPY_MODE != founder.
If session queue is non-empty, surfaces flagged files and prompts /council-review.
"""
import os
import sys
import json

if os.environ.get("CANOPY_MODE") != "founder":
    sys.exit(0)


def main():
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    session_id = hook_input.get("session_id", "default")
    queue_file = f"/tmp/canopy_review_queue_{session_id}.txt"

    if not os.path.exists(queue_file):
        sys.exit(0)

    with open(queue_file) as f:
        queued = [line.strip() for line in f if line.strip()]

    os.remove(queue_file)

    if not queued:
        sys.exit(0)

    unique = list(dict.fromkeys(queued))
    files_list = "\n".join(f"  • {p}" for p in unique)

    print(
        f"\n[CANOPY] Council review has not run this session.\n"
        f"Significant files changed:\n{files_list}\n\n"
        f"Run /council-review before closing, or acknowledge explicitly.\n",
        flush=True,
    )


if __name__ == "__main__":
    main()
