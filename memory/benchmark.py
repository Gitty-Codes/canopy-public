# memory/benchmark.py
# The Canopy — Self-awareness layer.
#
# Tracks every harness call: tokens, cache hits, memories, DISSENT rate.
# Tracks every test run: pass/fail counts, test-level results.
# The harness writes here automatically after every call.
# The test runner writes here after every suite run.
#
# Principle: the harness is the product. This is the product's metrics layer.
# Non-blocking: benchmark failures never crash the harness.
#
# CLI: python memory/benchmark.py

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BENCH_PATH = Path(__file__).parent / "benchmark.db"


# ── Internal ──────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now().isoformat()


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(BENCH_PATH)
    c.row_factory = sqlite3.Row
    return c


def _init() -> None:
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS calls (
                id                    INTEGER PRIMARY KEY AUTOINCREMENT,
                mode                  TEXT NOT NULL,
                model                 TEXT DEFAULT '',
                voice_set             TEXT DEFAULT '',
                input_tokens          INTEGER DEFAULT 0,
                output_tokens         INTEGER DEFAULT 0,
                cache_read_tokens     INTEGER DEFAULT 0,
                cache_creation_tokens INTEGER DEFAULT 0,
                memories_used         INTEGER DEFAULT 0,
                dissent_issued        INTEGER DEFAULT 0,
                synthesis_turn        INTEGER DEFAULT 0,
                project_id            TEXT DEFAULT '',
                created_at            TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS test_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                suite       TEXT NOT NULL,
                passed      INTEGER NOT NULL DEFAULT 0,
                failed      INTEGER NOT NULL DEFAULT 0,
                errors      INTEGER NOT NULL DEFAULT 0,
                total       INTEGER NOT NULL DEFAULT 0,
                duration_ms INTEGER DEFAULT 0,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS test_results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id      INTEGER NOT NULL,
                test_name   TEXT NOT NULL,
                status      TEXT NOT NULL,
                message     TEXT DEFAULT '',
                duration_ms INTEGER DEFAULT 0,
                FOREIGN KEY(run_id) REFERENCES test_runs(id)
            );
        """)


_init()


# ── Write API — all non-blocking ──────────────────────────────────────────────

def record_call(
    mode: str,
    model: str = "",
    voice_set: str = "",
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read_tokens: int = 0,
    cache_creation_tokens: int = 0,
    memories_used: int = 0,
    dissent_issued: bool = False,
    synthesis_turn: bool = False,
    project_id: str = "",
) -> None:
    """Records one harness call. Non-blocking — never raises."""
    try:
        with _conn() as c:
            c.execute(
                """INSERT INTO calls
                   (mode, model, voice_set, input_tokens, output_tokens,
                    cache_read_tokens, cache_creation_tokens, memories_used,
                    dissent_issued, synthesis_turn, project_id, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (mode, model, voice_set, input_tokens, output_tokens,
                 cache_read_tokens, cache_creation_tokens, memories_used,
                 int(dissent_issued), int(synthesis_turn), project_id, _now()),
            )
    except Exception:
        pass


def record_test_run(
    suite: str,
    passed: int,
    failed: int,
    errors: int,
    duration_ms: int = 0,
) -> int:
    """Records a test suite run. Returns run_id for linking individual results."""
    total = passed + failed + errors
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO test_runs (suite, passed, failed, errors, total, duration_ms, created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (suite, passed, failed, errors, total, duration_ms, _now()),
        )
        return cur.lastrowid


def record_test_result(
    run_id: int,
    test_name: str,
    status: str,
    message: str = "",
    duration_ms: int = 0,
) -> None:
    """Records one test result within a run. status: pass | fail | error"""
    try:
        with _conn() as c:
            c.execute(
                """INSERT INTO test_results (run_id, test_name, status, message, duration_ms)
                   VALUES (?,?,?,?,?)""",
                (run_id, test_name, status, message, duration_ms),
            )
    except Exception:
        pass


# ── Report ────────────────────────────────────────────────────────────────────

def report() -> str:
    with _conn() as c:
        total_calls = c.execute("SELECT COUNT(*) FROM calls").fetchone()[0]

        lines = [
            "=" * 60,
            "THE CANOPY — Self-Awareness Report",
            "=" * 60,
            "",
        ]

        # ── Harness calls ─────────────────────────────────────────────────────
        lines.append(f"Harness calls recorded:  {total_calls}")
        if total_calls > 0:
            avgs = c.execute("""
                SELECT AVG(input_tokens) ai, AVG(output_tokens) ao,
                       AVG(cache_read_tokens) ac, AVG(memories_used) am
                FROM calls
            """).fetchone()

            totals = c.execute("""
                SELECT SUM(input_tokens) ti, SUM(cache_read_tokens) tc
                FROM calls WHERE input_tokens > 0
            """).fetchone()

            cache_rate = (totals["tc"] / totals["ti"] * 100) if totals["ti"] else 0.0

            lines += [
                f"Cache hit rate:          {cache_rate:.1f}%",
                f"Avg input tokens:        {avgs['ai']:.0f}" if avgs["ai"] else "Avg input tokens:        —",
                f"Avg output tokens:       {avgs['ao']:.0f}" if avgs["ao"] else "Avg output tokens:       —",
                f"Avg memories used:       {avgs['am']:.1f}" if avgs["am"] else "Avg memories used:       —",
                "",
            ]

            modes = c.execute(
                "SELECT mode, COUNT(*) n FROM calls GROUP BY mode ORDER BY n DESC"
            ).fetchall()
            lines.append("Mode breakdown:")
            for m in modes:
                lines.append(f"  {m['mode']:<14} {m['n']} calls")
            lines.append("")

            council = c.execute("SELECT COUNT(*) FROM calls WHERE mode='council'").fetchone()[0]
            if council:
                dissent = c.execute("SELECT COUNT(*) FROM calls WHERE dissent_issued=1").fetchone()[0]
                lines.append(f"Council calls:           {council}")
                lines.append(f"DISSENT rate:            {dissent / council * 100:.1f}%")
                lines.append("")

            # Token trend: last 5 calls
            recent = c.execute("""
                SELECT created_at, mode, input_tokens, cache_read_tokens, memories_used
                FROM calls ORDER BY created_at DESC LIMIT 5
            """).fetchall()
            if recent:
                lines.append("Last 5 calls:")
                for r in reversed(recent):
                    date = r["created_at"][:16]
                    cached_pct = int(r["cache_read_tokens"] / r["input_tokens"] * 100) if r["input_tokens"] else 0
                    lines.append(
                        f"  {date}  {r['mode']:<10} "
                        f"in:{r['input_tokens']:>5}  cached:{cached_pct:>3}%  mem:{r['memories_used']}"
                    )
                lines.append("")

        # ── Test runs ─────────────────────────────────────────────────────────
        total_runs = c.execute("SELECT COUNT(*) FROM test_runs").fetchone()[0]
        lines.append(f"Test suite runs:         {total_runs}")
        if total_runs > 0:
            runs = c.execute("""
                SELECT suite, passed, failed, errors, total, duration_ms, created_at
                FROM test_runs ORDER BY created_at DESC LIMIT 8
            """).fetchall()
            lines.append("")
            lines.append("Recent test runs:")
            for r in runs:
                date     = r["created_at"][:16]
                ok       = r["failed"] == 0 and r["errors"] == 0
                mark     = "✓" if ok else "✗"
                ms       = f"{r['duration_ms']}ms" if r["duration_ms"] else ""
                lines.append(
                    f"  {mark} {date}  {r['suite']:<20}  {r['passed']}/{r['total']} passed  {ms}"
                )

            # Latest failures
            latest_run = c.execute(
                "SELECT id FROM test_runs ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
            if latest_run:
                failures = c.execute(
                    """SELECT test_name, message FROM test_results
                       WHERE run_id=? AND status != 'pass'""",
                    (latest_run["id"],),
                ).fetchall()
                if failures:
                    lines.append("")
                    lines.append("Failures in latest run:")
                    for f in failures:
                        lines.append(f"  ✗ {f['test_name']}")
                        if f["message"]:
                            lines.append(f"    {f['message'][:100]}")

        lines += ["", "=" * 60]
        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(report())
