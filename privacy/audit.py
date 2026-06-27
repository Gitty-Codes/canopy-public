# privacy/audit.py
# The Canopy — Privacy Audit Trail
#
# Writes a local record for every Sensitive or Protected request.
# Records only processing metadata — never the request content.
# Stored in memory/privacy_audit/ as JSON. Never sent to external services.
#
# Purpose: support the organization's own compliance needs.
# This trail exists for the org, not for The Canopy.

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

AUDIT_DIR = Path(__file__).parent.parent / "memory" / "privacy_audit"


def write_audit(
    classification: str,
    task_name: str,
    engine_used: str,
    model_used: str,
    memory_written: bool,
    inputs_summary: Optional[str] = None,
) -> Path:
    """
    Writes an audit record for a Sensitive or Protected request.

    inputs_summary: brief description of what was processed — not actual content.
                    The actual request text is never stored here.
    Returns path to the written record.
    """
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).isoformat()
    ts_slug = ts[:19].replace(":", "-").replace("T", "_")

    summary = (inputs_summary or "")[:200]

    record = {
        "timestamp":      ts,
        "classification": classification,
        "task":           task_name,
        "engine":         engine_used,
        "model":          model_used,
        "memory_written": memory_written,
        "inputs_summary": summary,
        "_note": (
            "Audit record only. Request content is not stored here. "
            "This file supports the organization's compliance record-keeping."
        ),
    }

    fname = f"{ts_slug}_{classification}_{task_name}.json"
    fpath = AUDIT_DIR / fname
    fpath.write_text(json.dumps(record, indent=2))
    return fpath


def read_audit_log(limit: int = 20) -> list[dict]:
    """Returns the most recent audit records, newest first."""
    if not AUDIT_DIR.exists():
        return []

    records = []
    for f in sorted(AUDIT_DIR.glob("*.json"), reverse=True)[:limit]:
        try:
            records.append(json.loads(f.read_text()))
        except Exception:
            continue
    return records


def audit_summary() -> dict:
    """Returns counts per classification tier for a quick status view."""
    records = read_audit_log(limit=1000)
    counts: dict = {}
    for r in records:
        c = r.get("classification", "unknown")
        counts[c] = counts.get(c, 0) + 1
    counts["total"] = len(records)
    return counts
