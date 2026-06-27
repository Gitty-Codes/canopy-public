# memory/proposals.py
# The Canopy — Enhancement proposal detection and surfacing.
#
# Reads deficiency signals across council sessions.
# When a gap recurs 3+ times, writes a proposal stub to proposals/.
# Stubs are surfaced to the founder at the next session open — quiet
# inbox, not an alarm. The founder commissions; the system detects.

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROPOSALS_DIR = Path(__file__).parent.parent / "proposals"
EPISODIC_ROOT = Path(__file__).parent / "episodic"
COUNCIL_DIR = EPISODIC_ROOT / "_council"
THRESHOLD = 3  # occurrences before a proposal stub is written


def _load_all_signals() -> list[dict]:
    """Reads every deficiency signal from every council session."""
    if not COUNCIL_DIR.exists():
        return []
    signals = []
    for f in sorted(COUNCIL_DIR.glob("*.json"), reverse=True)[:200]:
        try:
            ep = json.loads(f.read_text())
            session_id = ep.get("id", "")
            session_time = ep.get("timestamp", "")
            for sig in ep.get("deficiency_signals", []):
                signals.append({
                    **sig,
                    "session_id": session_id,
                    "session_time": session_time,
                })
        except Exception:
            pass
    return signals


def _existing_proposals() -> set[str]:
    """Returns the set of gap types that already have a proposal file."""
    if not PROPOSALS_DIR.exists():
        return set()
    covered = set()
    for f in PROPOSALS_DIR.glob("*.md"):
        try:
            text = f.read_text()
            # Look for "Deficiency addressed:" line and extract type
            for line in text.splitlines():
                if "deficiency addressed" in line.lower():
                    covered.add(f.stem)
        except Exception:
            pass
    # Also check the metadata file
    meta_file = PROPOSALS_DIR / "_index.json"
    if meta_file.exists():
        try:
            index = json.loads(meta_file.read_text())
            for entry in index:
                covered.add(entry.get("gap_type", ""))
        except Exception:
            pass
    return covered


def _next_proposal_number() -> str:
    if not PROPOSALS_DIR.exists():
        return "001"
    existing = list(PROPOSALS_DIR.glob("PROPOSAL-*.md"))
    return f"{len(existing) + 1:03d}"


def _update_index(entry: dict) -> None:
    meta_file = PROPOSALS_DIR / "_index.json"
    index = []
    if meta_file.exists():
        try:
            index = json.loads(meta_file.read_text())
        except Exception:
            pass
    index.append(entry)
    meta_file.write_text(json.dumps(index, indent=2))


def detect_and_stage() -> list[dict]:
    """
    Reads all council deficiency signals. For gap types that appear THRESHOLD+
    times and don't already have a proposal, writes a stub to proposals/.

    Returns a list of newly created proposal stubs (may be empty).
    """
    signals = _load_all_signals()
    unresolved = [s for s in signals if not s.get("resolved")]

    by_type: dict[str, list] = defaultdict(list)
    for sig in unresolved:
        by_type[sig.get("type", "unknown")].append(sig)

    existing = _existing_proposals()
    PROPOSALS_DIR.mkdir(exist_ok=True)

    new_proposals = []
    for gap_type, occurrences in by_type.items():
        if len(occurrences) < THRESHOLD:
            continue
        if gap_type in existing:
            continue

        num = _next_proposal_number()
        voices = sorted({s.get("voice", "?") for s in occurrences})
        severities = [s.get("severity", "LOW") for s in occurrences]
        severity = "HIGH" if "HIGH" in severities else ("MEDIUM" if "MEDIUM" in severities else "LOW")
        sample_content = occurrences[0].get("content", "")[:200]
        first_seen = min(s.get("session_time", "") for s in occurrences)[:10]

        stub = f"""---
proposal_id: PROPOSAL-{num}
gap_type: {gap_type}
status: PENDING
occurrences: {len(occurrences)}
severity: {severity}
voices: {', '.join(voices)}
first_seen: {first_seen}
created: {datetime.now().date()}
---

# [PROPOSAL-{num}] — Address recurring `{gap_type}` gap

**Deficiency addressed:**
Gap type `{gap_type}` has appeared {len(occurrences)} times in council sessions
since {first_seen}. Voices surfacing it: {', '.join(voices)}.

Sample signal: "{sample_content}"

**What this enhancement should do:**
*(To be completed by Listener + Inventor session)*

**What it does NOT do (scope boundary):**
*(To be completed)*

**Build cost:**
- Estimated hours: TBD
- Files touched: TBD
- Architectural risk: TBD
- Reversible: TBD

**Constitutional check:**
*(To be completed)*

**Proposed by:** auto-detected by proposals.py threshold trigger
**Status:** PENDING — awaiting founder commission

---
*This is a stub. A Listener + Inventor session fills in the "What this does" and
"Build cost" sections before the founder reviews.*
"""

        proposal_file = PROPOSALS_DIR / f"PROPOSAL-{num}.md"
        proposal_file.write_text(stub)

        entry = {
            "proposal_id": f"PROPOSAL-{num}",
            "gap_type": gap_type,
            "occurrences": len(occurrences),
            "severity": severity,
            "status": "PENDING",
            "created": datetime.now().isoformat(),
        }
        _update_index(entry)
        new_proposals.append(entry)

    return new_proposals


def pending_proposals() -> list[dict]:
    """Returns all PENDING proposals from the index."""
    meta_file = PROPOSALS_DIR / "_index.json"
    if not meta_file.exists():
        return []
    try:
        index = json.loads(meta_file.read_text())
        return [e for e in index if e.get("status") == "PENDING"]
    except Exception:
        return []


def format_pending_summary() -> str:
    """One-line summary of pending proposals for session-open display."""
    pending = pending_proposals()
    if not pending:
        return ""
    lines = [f"\n{'─' * 60}"]
    lines.append(f"  {len(pending)} enhancement proposal(s) pending your review:")
    for p in pending:
        lines.append(
            f"    [{p['proposal_id']}] {p['gap_type']} — "
            f"{p['occurrences']} occurrences, severity {p['severity']}"
        )
    lines.append(f"  See proposals/ directory to review and commission.")
    lines.append(f"{'─' * 60}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    print("Scanning for recurring deficiency gaps...\n")
    new = detect_and_stage()
    if new:
        for p in new:
            print(f"  ✓ Created {p['proposal_id']} — {p['gap_type']} ({p['occurrences']} occurrences)")
    else:
        print("  No new gaps reached the threshold. Nothing staged.")

    pending = pending_proposals()
    if pending:
        print(f"\n  {len(pending)} proposal(s) currently pending founder review.")
