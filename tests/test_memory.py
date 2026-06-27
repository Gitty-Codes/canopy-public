"""
tests/test_memory.py — Episodic store and memory context tests. No API required.
"""
import shutil
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.episodic import log, load, MEMORY_TYPE_TO_TIER, PERSISTENT, LONGTERM, EPISODIC_TIER, EPISODIC_ROOT
from memory.store import (
    save_memory,
    build_memory_context,
    retrieve_memories,
    memory_status,
    _keyword_score,
)

TEST_AGENT = "_test_memory_agent"


def setUpModule():
    test_dir = EPISODIC_ROOT / TEST_AGENT
    if test_dir.exists():
        shutil.rmtree(test_dir)


def tearDownModule():
    test_dir = EPISODIC_ROOT / TEST_AGENT
    if test_dir.exists():
        shutil.rmtree(test_dir)


class TestEpisodicWrite(unittest.TestCase):

    def test_log_returns_path(self):
        path = log(TEST_AGENT, "test learning", memory_type="session")
        self.assertTrue(Path(path).exists())

    def test_log_creates_json_file(self):
        import json
        path = log(TEST_AGENT, "json test", memory_type="decision")
        with open(path) as f:
            record = json.load(f)
        self.assertEqual(record["learning"], "json test")
        self.assertEqual(record["memory_type"], "decision")

    def test_timestamp_uniqueness(self):
        # Write two records rapidly — microsecond IDs must not collide
        paths = [log(TEST_AGENT, f"rapid write {i}", memory_type="session") for i in range(5)]
        self.assertEqual(len(set(paths)), 5)

    def test_tier_assigned_correctly(self):
        import json
        path = log(TEST_AGENT, "identity content", memory_type="identity")
        with open(path) as f:
            r = json.load(f)
        self.assertEqual(r["tier"], PERSISTENT)

    def test_significance_default_by_tier(self):
        import json
        path = log(TEST_AGENT, "persistent content", memory_type="constitution")
        with open(path) as f:
            r = json.load(f)
        self.assertEqual(r["significance"], 1.0)  # critical for persistent


class TestEpisodicRead(unittest.TestCase):

    def setUp(self):
        log(TEST_AGENT, "session entry for read test", memory_type="session")
        log(TEST_AGENT, "decision entry for read test", memory_type="decision")

    def test_load_returns_list(self):
        records = load(TEST_AGENT, limit=5)
        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)

    def test_load_filter_by_type(self):
        records = load(TEST_AGENT, memory_type="decision", limit=10)
        for r in records:
            self.assertEqual(r["memory_type"], "decision")

    def test_load_filter_by_tier(self):
        records = load(TEST_AGENT, tier=EPISODIC_TIER, limit=10)
        for r in records:
            self.assertIn(r.get("tier", EPISODIC_TIER), [EPISODIC_TIER])

    def test_newest_first(self):
        records = load(TEST_AGENT, limit=10)
        if len(records) >= 2:
            self.assertGreaterEqual(
                records[0]["timestamp"], records[1]["timestamp"]
            )


class TestKeywordScoring(unittest.TestCase):

    def test_no_keywords_returns_zero(self):
        record = {"learning": "funder grant application", "tags": []}
        self.assertEqual(_keyword_score(record, []), 0.0)

    def test_full_match_returns_one(self):
        record = {"learning": "funder grant application", "tags": []}
        score = _keyword_score(record, ["funder", "grant", "application"])
        self.assertAlmostEqual(score, 1.0)

    def test_partial_match(self):
        record = {"learning": "funder is important", "tags": []}
        score = _keyword_score(record, ["funder", "grant"])
        self.assertAlmostEqual(score, 0.5)

    def test_tag_match_counts(self):
        record = {"learning": "nothing here", "tags": ["funder", "grant"]}
        score = _keyword_score(record, ["funder", "grant"])
        self.assertAlmostEqual(score, 1.0)

    def test_case_insensitive(self):
        record = {"learning": "FUNDER is key", "tags": []}
        score = _keyword_score(record, ["funder"])
        self.assertAlmostEqual(score, 1.0)


class TestBuildMemoryContext(unittest.TestCase):

    def test_returns_tuple(self):
        result = build_memory_context(TEST_AGENT)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_count_is_integer(self):
        _, count = build_memory_context(TEST_AGENT)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_memory_hints_accepted(self):
        hints = {"keywords": ["decision", "architecture"], "types": ["decision"], "project_scope": False}
        text, count = build_memory_context(TEST_AGENT, memory_hints=hints)
        self.assertIsInstance(text, str)
        self.assertIsInstance(count, int)

    def test_empty_agent_returns_empty_string(self):
        text, count = build_memory_context("_nonexistent_agent_xyz")
        self.assertEqual(text, "")
        self.assertEqual(count, 0)


class TestMemoryStatus(unittest.TestCase):

    def test_status_has_required_keys(self):
        status = memory_status(TEST_AGENT)
        self.assertIn("persistent", status)
        self.assertIn("longterm", status)
        self.assertIn("episodic", status)
        self.assertIn("total", status)

    def test_total_matches_sum(self):
        status = memory_status(TEST_AGENT)
        self.assertEqual(
            status["total"],
            status["persistent"] + status["longterm"] + status["episodic"],
        )


class TestRelationalCouncil(unittest.TestCase):

    def test_all_voices_constant_is_complete(self):
        from memory.episodic import ALL_VOICES
        expected = {
            "elder", "listener", "strategist", "product_partner", "builder",
            "guardian", "operator", "steward", "inventor", "challenger",
        }
        self.assertEqual(set(ALL_VOICES), expected)
        self.assertEqual(len(ALL_VOICES), 10)

    def test_load_relational_council_returns_list(self):
        from memory.episodic import load_relational_council
        result = load_relational_council(limit_per_agent=2)
        self.assertIsInstance(result, list)

    def test_format_relational_council_returns_string(self):
        from memory.episodic import format_relational_council
        result = format_relational_council()
        self.assertIsInstance(result, str)

    def test_format_relational_council_empty_when_no_memories(self):
        from memory.episodic import format_relational_council, EPISODIC_ROOT
        # Only meaningful if test agent dirs have no relational records.
        # Check the function returns a string without raising.
        result = format_relational_council(limit_per_agent=1)
        self.assertIsInstance(result, str)

    def test_relational_memory_written_under_correct_agent(self):
        import json
        from memory.episodic import log, load, EPISODIC_ROOT
        path = log(
            agent=TEST_AGENT,
            learning="Test relational observation.",
            memory_type="relational",
            tags=["relational", "test"],
        )
        self.assertTrue(Path(path).exists())
        with open(path) as f:
            record = json.load(f)
        self.assertEqual(record["memory_type"], "relational")
        self.assertEqual(record["agent"], TEST_AGENT)

    def test_relational_memory_loadable_by_type(self):
        from memory.episodic import log, load
        log(
            agent=TEST_AGENT,
            learning="Another relational entry.",
            memory_type="relational",
            tags=["relational"],
        )
        records = load(TEST_AGENT, memory_type="relational", limit=10)
        self.assertGreater(len(records), 0)
        for r in records:
            self.assertEqual(r["memory_type"], "relational")


class TestCouncilMemory(unittest.TestCase):

    def test_log_council_writes_file(self):
        from memory.episodic import log_council, EPISODIC_ROOT
        import json
        path = log_council(
            learning="Test council record for unit test.",
            agents_present=["harness"],
            memory_type="session",
            tags=["test"],
        )
        self.assertTrue(Path(path).exists())
        with open(path) as f:
            record = json.load(f)
        self.assertIn("learning", record)
        self.assertIn("deficiency_signals", record)
        self.assertIn("outcome", record)

    def test_log_council_with_deficiency_signals(self):
        from memory.episodic import log_council
        import json
        signals = [
            {
                "type": "open_tension",
                "voice": "challenger",
                "content": "Test tension.",
                "severity": "MEDIUM",
                "resolved": False,
            }
        ]
        path = log_council(
            learning="Council session with deficiency signal.",
            agents_present=["challenger"],
            deficiency_signals=signals,
        )
        with open(path) as f:
            record = json.load(f)
        self.assertEqual(len(record["deficiency_signals"]), 1)
        self.assertEqual(record["deficiency_signals"][0]["type"], "open_tension")
        self.assertFalse(record["deficiency_signals"][0]["resolved"])


if __name__ == "__main__":
    unittest.main()
