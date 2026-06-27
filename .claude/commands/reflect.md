---
description: Write a relational memory — what you noticed about another voice's reasoning pattern during a council session
allowed-tools: Bash
---

You are writing a relational memory on behalf of a council voice. This is not a session summary — it is what one voice noticed about another voice's *reasoning pattern*: a tendency, a blindspot, a consistent framing, a way of entering a problem. These observations accumulate into the council's knowledge of itself.

## What a relational memory captures

- A recurring pattern in how a voice approaches problems ("The Inventor consistently anchors on mechanism before checking user need")
- A blindspot revealed under examination ("The Strategist rarely names the harm case; surface it explicitly next time")
- An emergent dynamic between two voices ("When the Guardian raises risk, the Elder tends to hold rather than resolve — this is structural, not personal")
- A voice that was absent when it should have spoken

Relational memories are not judgments. They are observations. Write what you actually noticed, not what seems polite.

## Format

Ask the founder:
1. Which voice is writing this observation?
2. Which voice (or dynamic) is being observed?
3. What did you notice?

Then write:

```python
import sys
sys.path.insert(0, ".")
from memory.episodic import log

log(
    agent="<observer_voice>",
    learning="<what was noticed — specific, not generic>",
    memory_type="relational",
    tags=["relational", "<observed_voice>"],
    aaak={
        "assertion": "<what is now known about this voice's pattern>",
        "assumption": "<what was assumed before this observation>",
        "action": "<nothing yet, or: named this explicitly to council>",
        "knowledge": "<what to do with this knowledge in future sessions>",
    }
)
```

Run the script and confirm the path written.

## Privacy note

Relational memories are council-visible — they are loaded into every council session via `format_relational_council()`. Write what should be part of the council's self-knowledge, not private critique. If an observation is too raw to share with the full council, it belongs in a growth memory instead.

## When to use

After any council session where you noticed something non-obvious about how a voice reasoned — not after every session. If nothing was genuinely surprising, don't write one.
