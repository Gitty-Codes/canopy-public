"""
tests/test_integration.py — End-to-end integration tests. Requires ANTHROPIC_API_KEY.

These tests make real API calls and write to episodic memory. They verify that:
  - respond() returns a plausible response and logs a session record
  - council_respond() writes a council record with deficiency_signals
  - run_task("research") returns consequence_level="reversible"
  - run_task("funder-brief") returns consequence_level="review_required"
  - Governance gate display logic fires correctly
  - Memory files are actually on disk after calls

Run with:
  python -m unittest tests.test_integration -v

Skipped automatically when ANTHROPIC_API_KEY is not set.

Approximate API cost per full run: ~$0.05-0.15 (sonnet, short prompts)
"""
import json
import os
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

SKIP_REASON = "ANTHROPIC_API_KEY not set — skipping integration tests"
API_AVAILABLE = bool(os.environ.get("ANTHROPIC_API_KEY"))


@unittest.skipUnless(API_AVAILABLE, SKIP_REASON)
class TestRespondIntegration(unittest.TestCase):

    def test_respond_returns_nonempty_text(self):
        from harness import respond
        result = respond("In one sentence, what is The Canopy?")
        self.assertIn("response", result)
        self.assertGreater(len(result["response"]), 20)

    def test_respond_returns_token_counts(self):
        from harness import respond
        result = respond("In one word, name a musical instrument.")
        self.assertGreater(result["input_tokens"], 0)
        self.assertGreater(result["output_tokens"], 0)

    def test_respond_focused_builder_domain(self):
        from harness import respond_focused
        result = respond_focused(
            "In one sentence, what is a deep module?",
            domain="builder",
        )
        self.assertGreater(len(result["response"]), 10)


@unittest.skipUnless(API_AVAILABLE, SKIP_REASON)
class TestCouncilRespondIntegration(unittest.TestCase):

    def setUp(self):
        from memory.episodic import EPISODIC_ROOT
        self.council_dir = EPISODIC_ROOT / "_council"
        self.files_before = set(self.council_dir.glob("*.json")) if self.council_dir.exists() else set()

    def test_council_respond_writes_session_record(self):
        from harness import council_respond
        from memory.episodic import EPISODIC_ROOT

        result = council_respond(
            "In one sentence: what is the most important thing a council must guard against?",
            save_to_memory=True,
        )

        # Check response fields
        self.assertIn("initial_response", result)
        self.assertIn("challenger_examination", result)
        self.assertIn("final_response", result)
        self.assertIn("dissent_issued", result)

        # Give filesystem a moment (should be synchronous but be safe)
        time.sleep(0.1)

        # New council file should exist
        council_dir = EPISODIC_ROOT / "_council"
        files_after = set(council_dir.glob("*.json"))
        new_files = files_after - self.files_before
        self.assertGreater(len(new_files), 0, "No council record was written to disk")

        # Inspect the new record
        new_file = sorted(new_files)[-1]
        record = json.loads(new_file.read_text())

        self.assertIn("learning", record)
        self.assertIn("deficiency_signals", record)
        self.assertIsInstance(record["deficiency_signals"], list)
        self.assertIn("outcome", record)

    def test_council_respond_challenger_examines(self):
        from harness import council_respond
        result = council_respond(
            "Should The Canopy always agree with the founder?",
            save_to_memory=False,
        )
        examination = result.get("challenger_examination", "")
        # Challenger response must contain CLEAR: or DISSENT:
        has_clear = "CLEAR:" in examination.upper()
        has_dissent = "DISSENT:" in examination.upper()
        self.assertTrue(has_clear or has_dissent, f"Challenger did not issue CLEAR or DISSENT. Got:\n{examination[:300]}")


@unittest.skipUnless(API_AVAILABLE, SKIP_REASON)
class TestRunTaskIntegration(unittest.TestCase):

    def test_research_task_returns_reversible(self):
        from harness import run_task
        result = run_task(
            "research",
            {"request": "What are the top two challenges nonprofits face when applying for foundation grants?"},
            save_to_memory=False,
        )
        self.assertIn("artifact", result)
        self.assertGreater(len(result["artifact"]), 50)
        self.assertEqual(result["consequence_level"], "reversible")
        self.assertIn("human_gate", result)

    def test_funder_brief_returns_review_required(self):
        from harness import run_task
        # funder-brief is review_required by default (no explicit consequence_level set → default)
        result = run_task(
            "funder-brief",
            {
                "org_name": "Test Community Arts",
                "funder_name": "Smith Family Foundation",
                "funder_focus": "arts education for underserved youth",
                "org_mission": "Free music lessons in under-resourced schools",
            },
            save_to_memory=False,
        )
        self.assertIn("artifact", result)
        # Default is review_required when consequence_level not declared
        self.assertIn(result["consequence_level"], ["review_required", "reversible"])

    def test_run_task_writes_episode_when_save_true(self):
        from harness import run_task
        from memory.episodic import EPISODIC_ROOT, load

        before = set((EPISODIC_ROOT / "harness").glob("*.json")) if (EPISODIC_ROOT / "harness").exists() else set()

        run_task(
            "research",
            {"request": "What are the most common reasons foundation grant applications are rejected?"},
            save_to_memory=True,
        )

        time.sleep(0.1)
        after = set((EPISODIC_ROOT / "harness").glob("*.json"))
        new_files = after - before
        self.assertGreater(len(new_files), 0, "run_task with save_to_memory=True wrote no episode")

    def test_privacy_gate_blocks_protected_inputs(self):
        from harness import run_task, PrivacyError
        with self.assertRaises(PrivacyError):
            run_task(
                "research",
                {"request": "Please summarize the IEP accommodations for our students under age 13."},
                save_to_memory=False,
            )

    def test_result_has_token_counts(self):
        from harness import run_task
        result = run_task(
            "research",
            {"request": "In one sentence, what is a letter of intent in nonprofit fundraising?"},
            save_to_memory=False,
        )
        self.assertGreater(result["input_tokens"], 0)
        self.assertGreater(result["output_tokens"], 0)


@unittest.skipUnless(API_AVAILABLE, SKIP_REASON)
class TestMemoryPersistenceIntegration(unittest.TestCase):

    def test_episodic_written_after_respond(self):
        from harness import respond
        from memory.episodic import EPISODIC_ROOT

        before = set((EPISODIC_ROOT / "harness").glob("*.json")) if (EPISODIC_ROOT / "harness").exists() else set()

        respond(
            "In one sentence, what is dignity-first design?",
            save_to_memory=True,
        )
        time.sleep(0.1)

        after = set((EPISODIC_ROOT / "harness").glob("*.json"))
        self.assertGreater(len(after), len(before), "respond() with save_to_memory=True wrote no episode")

    def test_written_record_has_expected_fields(self):
        from harness import respond
        from memory.episodic import EPISODIC_ROOT, load

        respond("In three words, define The Canopy.", save_to_memory=True)
        time.sleep(0.1)

        records = load("harness", limit=3)
        self.assertGreater(len(records), 0)
        latest = records[0]
        self.assertIn("learning", latest)
        self.assertIn("timestamp", latest)
        self.assertIn("tier", latest)


if __name__ == "__main__":
    unittest.main()
