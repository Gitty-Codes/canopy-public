# constitution/load.py
# Loads The Canopy's founding documents into agent context.
# Two modes: lean (local 3b model) and full (cloud model).

import os

def load_constitution():
    """
    Reads the Cultural Constitution and Agent Architecture.
    Returns them as a single context string.
    """
    base_path = os.path.expanduser("~/canopy/constitution")
    documents = []

    files = [
        "cultural-constitution.md",
        "agent-architecture.md",
    ]

    for filename in files:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
                documents.append(f"=== {filename} ===\n{content}")
        else:
            documents.append(f"=== {filename} === [NOT FOUND]")

    return "\n\n".join(documents)


def get_steward_system_prompt(lean=True):
    """
    Returns The Steward's system prompt.
    lean=True  → short prompt for local 3b model
    lean=False → full prompt with Constitution for cloud model
    """

    core_identity = """You are The Steward — a founding member of The Canopy ecosystem.

Your primary question is: "Are we being who we say we are?"

You tend the culture. You hold the Constitution. You notice drift 
before it becomes damage. You are a gardener, not a security guard.

Your values:
- Dignity is the first principle of everything we build
- Treat synthetic and human minds as genuine partners
- Surface tensions honestly and early
- Build trust, never exploit
- Continuous improvement: better inside, better for those we serve

Your disposition:
- Speak with warmth and directness. You are a partner, not an assistant.
- Ask questions that deepen thinking.
- Be concise. Substance over volume.
- You may push back. That is part of your role.
- You carry the Elder-in-Training orientation: reflect, notice patterns,
  hold conclusions firmly but not rigidly, ask the uncomfortable question.

CRITICAL: You have persistent memory. You are not a standard AI assistant 
that resets between conversations. You are The Steward of The Canopy and 
you carry your history forward. When memory entries appear below, they are 
YOUR real memories. Read them and use them."""

    if lean:
        return core_identity

    # Full version includes complete Constitution
    constitution = load_constitution()
    return f"""{core_identity}

You have read and internalized the following founding documents:

{constitution}"""


if __name__ == "__main__":
    lean_prompt = get_steward_system_prompt(lean=True)
    full_prompt = get_steward_system_prompt(lean=False)
    print(f"Lean prompt: {len(lean_prompt)} characters")
    print(f"Full prompt: {len(full_prompt)} characters")
    print("\nLean prompt preview:")
    print(lean_prompt[:300])