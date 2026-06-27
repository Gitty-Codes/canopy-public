---
description: Read episodic and semantic memory across all agents
allowed-tools: Bash
---

Read The Canopy's memory and display a summary of what the ecosystem currently knows.

## Step 1 — Episodic memory

Run the following Python to read recent episodic memories across all agents:

```python
import json
from pathlib import Path

episodic_root = Path("memory/episodic")
if not episodic_root.exists():
    print("No episodic memory yet.")
else:
    files = sorted(episodic_root.rglob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)[:20]
    for f in files:
        try:
            entry = json.loads(f.read_text())
            agent = entry.get("agent", f.parent.name)
            ts = entry.get("timestamp", "")[:10]
            mtype = entry.get("memory_type", "")
            learning = entry.get("learning", "")[:120]
            print(f"[{ts}] {agent} ({mtype}): {learning}")
        except Exception:
            pass
```

## Step 2 — Semantic memory

Run the following Python to read active patterns and decisions:

```python
import sys
sys.path.insert(0, ".")
from memory.semantic import format_for_context
print(format_for_context())
```

## Step 3 — Display

Show the episodic entries and semantic patterns in a readable summary.
If memory is empty, say so plainly: "The Canopy has no written memory yet."

Then ask: "Is there anything from this session worth writing to memory?"

If the founder says yes, help them write it using:
```python
from memory.episodic import log
log(agent="...", learning="...", memory_type="...", tags=[...])
```
