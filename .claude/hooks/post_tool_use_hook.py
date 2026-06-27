#!/usr/bin/env python3
"""
PostToolUse hook — significance filter for council review queue.
Fires after Write/Edit. Silently exits if CANOPY_MODE != founder.
Appends significant files to a session-scoped queue for stop_hook.py.
"""
import os
import sys
import json

if os.environ.get("CANOPY_MODE") != "founder":
    sys.exit(0)

CORE_PATHS = [
    "agents/",
    "constitution/",
    "skills/",
    ".claude/commands/",
    ".claude/agents/",
]
ALWAYS_TRIGGER = [
    "harness.py",
    "constitution/decisions-log",
    "constitution/cultural-constitution.md",
]
LINE_THRESHOLD = 15


def is_significant(tool_name, tool_input):
    if tool_name not in ("Write", "Edit"):
        return False

    file_path = tool_input.get("file_path", "")
    rel_path = file_path.lstrip("/")

    if any(rel_path.endswith(t) or rel_path == t for t in ALWAYS_TRIGGER):
        return True

    in_core = any(
        ("/" + rel_path + "/").find("/" + p) >= 0 or rel_path.startswith(p)
        for p in CORE_PATHS
    )
    if not in_core:
        return False

    if tool_name == "Write":
        return True

    old = tool_input.get("old_string", "")
    new = tool_input.get("new_string", "")
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    changed = abs(len(new_lines) - len(old_lines)) + sum(
        1 for a, b in zip(old_lines, new_lines) if a != b
    )
    return changed >= LINE_THRESHOLD


def main():
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})
    session_id = hook_input.get("session_id", "default")

    if not is_significant(tool_name, tool_input):
        sys.exit(0)

    file_path = tool_input.get("file_path", "unknown")
    queue_file = f"/tmp/canopy_review_queue_{session_id}.txt"
    with open(queue_file, "a") as f:
        f.write(f"{file_path}\n")

    print(f"[COUNCIL QUEUE] {file_path} — flagged for /council-review", flush=True)


if __name__ == "__main__":
    main()
