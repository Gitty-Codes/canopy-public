# consequence/webapp_reader.py
# Stub — reads webapp interoception signals into the consequence architecture.
#
# NOT YET WIRED. Wire when:
#   - webapp_signals.jsonl has accumulated enough data to inform homeostatic
#     feedback (suggested: after 50+ task_complete signals from real KIC use)
#   - The consequence architecture has a defined intake format for external surfaces
#
# When wired, this module should:
#   1. Read data/webapp_signals.jsonl (appended by harness_wrapper._log_webapp_signal)
#   2. Aggregate: task completion rates, error rates per task type, per-org patterns
#   3. Emit homeostatic signals to level2_dissent or level5_history as appropriate
#   4. Mark processed entries so it doesn't re-read the full file on every call
#
# Signal schema (from harness_wrapper._log_webapp_signal):
#   {
#     "ts": "ISO 8601",
#     "surface": "webapp",
#     "org_id": "str",
#     "task": "str",          # e.g. "social-post", "grant-loi"
#     "signal": "str",        # "task_complete" | "task_error" | "follow_up" | "session_start"
#     "detail": {}            # optional — output_tokens, error_type, etc.
#   }

from pathlib import Path

SIGNALS_FILE = Path(__file__).parent.parent / "webapp" / "backend" / "data" / "webapp_signals.jsonl"


def read_signals(since_ts: str | None = None) -> list[dict]:
    """Read webapp signals, optionally filtered by timestamp. Not yet called."""
    import json
    if not SIGNALS_FILE.exists():
        return []
    signals = []
    with open(SIGNALS_FILE) as f:
        for line in f:
            try:
                record = json.loads(line)
                if since_ts is None or record.get("ts", "") >= since_ts:
                    signals.append(record)
            except json.JSONDecodeError:
                pass
    return signals
