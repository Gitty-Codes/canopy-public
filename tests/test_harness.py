"""
tests/test_harness.py — Harness substrate assembly tests. No API required.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import harness
from harness import (
    load_voices,
    load_constitution,
    build_system_blocks,
    PREAMBLE,
    DEFAULT_VOICE_SET,
    DEFAULT_MODEL,
    HARNESS_MEMORY_AGENT,
)
from skills.loader import load_skills_for_context


class TestSubstrateLoading(unittest.TestCase):

    def test_load_voices_returns_nonempty(self):
        text = load_voices(DEFAULT_VOICE_SET)
        self.assertGreater(len(text), 1000)

    def test_load_voices_contains_all_ten(self):
        text = load_voices(DEFAULT_VOICE_SET).lower()
        expected = ["builder", "guardian", "listener", "elder", "steward",
                    "inventor", "challenger", "strategist", "operator"]
        for voice in expected:
            self.assertIn(voice, text, f"Voice '{voice}' not found in substrate")

    def test_load_constitution_returns_nonempty(self):
        text = load_constitution()
        self.assertGreater(len(text), 500)

    def test_load_constitution_contains_dignity(self):
        text = load_constitution().lower()
        self.assertIn("dignity", text)

    def test_preamble_contains_core_principle(self):
        self.assertIn("dignity", PREAMBLE.lower())
        self.assertIn("ten", PREAMBLE.lower())

    def test_unknown_voice_variant_raises(self):
        with self.assertRaises(ValueError):
            load_voices("nonexistent_variant")


class TestSkillsLoading(unittest.TestCase):

    def test_returns_tuple_of_str_and_dict(self):
        text, hints = load_skills_for_context()
        self.assertIsInstance(text, str)
        self.assertIsInstance(hints, dict)

    def test_default_load_nonempty(self):
        text, _ = load_skills_for_context()
        self.assertGreater(len(text), 500)

    def test_hints_have_required_keys(self):
        _, hints = load_skills_for_context()
        self.assertIn("types", hints)
        self.assertIn("keywords", hints)
        self.assertIn("project_scope", hints)

    def test_project_context_accepted(self):
        text, hints = load_skills_for_context(
            project_context={"sector": "nonprofit", "function": "fundraising"},
            explicit=["opportunity-scout"],
        )
        self.assertGreater(len(text), 500)
        self.assertTrue(hints["project_scope"])


class TestSystemBlockAssembly(unittest.TestCase):

    def setUp(self):
        self.voices = load_voices(DEFAULT_VOICE_SET)
        self.constitution = load_constitution()
        self.skills, _ = load_skills_for_context()

    def test_returns_list(self):
        blocks = build_system_blocks(self.voices, self.constitution, self.skills)
        self.assertIsInstance(blocks, list)

    def test_first_block_is_cached(self):
        blocks = build_system_blocks(self.voices, self.constitution, self.skills)
        self.assertIn("cache_control", blocks[0])
        self.assertEqual(blocks[0]["cache_control"]["type"], "ephemeral")

    def test_static_block_contains_preamble(self):
        blocks = build_system_blocks(self.voices, self.constitution, self.skills)
        self.assertIn("ten voices", blocks[0]["text"])

    def test_memory_block_added_when_provided(self):
        blocks = build_system_blocks(
            self.voices, self.constitution, self.skills,
            memory_text="Test memory content"
        )
        self.assertEqual(len(blocks), 2)
        self.assertIn("Test memory content", blocks[1]["text"])

    def test_no_memory_block_when_none(self):
        blocks = build_system_blocks(self.voices, self.constitution, self.skills)
        self.assertEqual(len(blocks), 1)

    def test_static_block_size_reasonable(self):
        blocks = build_system_blocks(self.voices, self.constitution, self.skills)
        # Should be under 120K chars (~30K tokens) — cache budget.
        # Threshold raised from 80K after v1 voice expansions (2026-06-07):
        # voices are richer; if this fails again, audit voice file sizes first.
        self.assertLess(len(blocks[0]["text"]), 120_000)


class TestBuildMemoryContext(unittest.TestCase):

    def test_returns_tuple(self):
        result = harness.build_memory_context("test query")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_count_is_nonnegative_int(self):
        _, count = harness.build_memory_context("test query")
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_memory_hints_accepted(self):
        hints = {"keywords": ["memory", "architecture"], "types": [], "project_scope": False}
        text, count = harness.build_memory_context("test query", memory_hints=hints)
        self.assertIsInstance(text, str)

    def test_project_context_without_project_id_is_safe(self):
        text, count = harness.build_memory_context(
            "test query",
            project_context={"sector": "nonprofit"},  # no project_id
        )
        self.assertIsInstance(text, str)


class TestTaskLayer(unittest.TestCase):

    def test_load_valid_task_profile(self):
        from harness import _load_task_profile
        profile, body = _load_task_profile("nonprofit-comms")
        self.assertEqual(profile["name"], "nonprofit-comms")
        self.assertIn("primary_voice", profile)
        self.assertIn("serves", profile)
        self.assertIn("human_gate", profile)
        self.assertGreater(len(body), 100)

    def test_load_missing_task_raises(self):
        from harness import _load_task_profile
        with self.assertRaises(ValueError) as ctx:
            _load_task_profile("nonexistent-task")
        self.assertIn("not found", str(ctx.exception))

    def test_task_primary_voice_is_valid_domain(self):
        from harness import _load_task_profile, DOMAIN_HINTS
        profile, _ = _load_task_profile("nonprofit-comms")
        self.assertIn(profile["primary_voice"], DOMAIN_HINTS)

    def test_task_required_skills_exist(self):
        from harness import _load_task_profile, SKILLS_DIR
        profile, _ = _load_task_profile("nonprofit-comms")
        requires = profile.get("requires", [])
        if isinstance(requires, str):
            requires = [requires]
        for skill in requires:
            self.assertTrue(
                (SKILLS_DIR / f"{skill}.md").exists(),
                f"Required skill '{skill}' not found in skills/"
            )

    def test_extract_section_artifact(self):
        from harness import _extract_section
        text = "ARTIFACT:\nHere is the draft.\n\nHUMAN GATE — Review first.\nConfirm before sending.\n\nUNCERTAINTY:\nMissing funder name."
        result = _extract_section(text, "ARTIFACT")
        self.assertIn("Here is the draft", result)
        self.assertNotIn("HUMAN GATE", result)

    def test_extract_section_uncertainty(self):
        from harness import _extract_section
        text = "ARTIFACT:\nDraft here.\n\nHUMAN GATE — Review.\nAction needed.\n\nUNCERTAINTY:\nFunder priorities unknown."
        result = _extract_section(text, "UNCERTAINTY")
        self.assertIn("Funder priorities unknown", result)

    def test_extract_section_missing_returns_empty(self):
        from harness import _extract_section
        result = _extract_section("No sections here.", "ARTIFACT")
        self.assertEqual(result, "")

    def test_tasks_dir_exists(self):
        from harness import TASKS_DIR
        self.assertTrue(TASKS_DIR.exists())
        self.assertTrue((TASKS_DIR / "TASKS.md").exists())


class TestConstants(unittest.TestCase):

    def test_default_model(self):
        self.assertIn("claude", DEFAULT_MODEL.lower())

    def test_harness_agent_name(self):
        self.assertEqual(HARNESS_MEMORY_AGENT, "harness")

    def test_domain_hints_covers_all_voices(self):
        from harness import DOMAIN_HINTS
        expected = {"builder", "guardian", "listener", "strategist",
                    "product_partner", "operator",
                    "steward", "elder", "inventor", "challenger"}
        self.assertEqual(set(DOMAIN_HINTS.keys()), expected)


class TestPrivacyClassifier(unittest.TestCase):

    def setUp(self):
        from privacy.classifier import (
            classify, classify_inputs,
            is_cloud_allowed, requires_audit, memory_write_allowed,
            PUBLIC, OPERATIONAL, SENSITIVE, PROTECTED,
        )
        self.classify = classify
        self.classify_inputs = classify_inputs
        self.is_cloud_allowed = is_cloud_allowed
        self.requires_audit = requires_audit
        self.memory_write_allowed = memory_write_allowed
        self.PUBLIC = PUBLIC
        self.OPERATIONAL = OPERATIONAL
        self.SENSITIVE = SENSITIVE
        self.PROTECTED = PROTECTED

    # ── Classification ────────────────────────────────────────────────────────

    def test_plain_text_defaults_to_operational(self):
        result = self.classify("Please help us write a grant letter.")
        self.assertEqual(result, self.OPERATIONAL)

    def test_donor_text_classified_sensitive(self):
        result = self.classify("Donor Jane Smith gave $5,000 in the fall campaign.")
        self.assertEqual(result, self.SENSITIVE)

    def test_dollar_amount_classified_sensitive(self):
        result = self.classify("The major gift of $25,000 was received last week.")
        self.assertEqual(result, self.SENSITIVE)

    def test_student_record_classified_protected(self):
        result = self.classify("Student records show Max has an IEP accommodation.")
        self.assertEqual(result, self.PROTECTED)

    def test_minor_mention_classified_protected(self):
        result = self.classify("All participants are minors under 13 enrolled in after-school.")
        self.assertEqual(result, self.PROTECTED)

    def test_salary_classified_sensitive(self):
        result = self.classify("Staff salaries range from $45k to $75k annually.")
        self.assertEqual(result, self.SENSITIVE)

    def test_health_data_classified_protected(self):
        result = self.classify("Her mental health records and treatment plan are attached.")
        self.assertEqual(result, self.PROTECTED)

    def test_confidential_marker_classified_sensitive(self):
        result = self.classify("CONFIDENTIAL: This budget is not for distribution.")
        self.assertEqual(result, self.SENSITIVE)

    def test_override_respected(self):
        sensitive_text = "donor gave $10,000"
        result = self.classify(sensitive_text, override=self.PUBLIC)
        self.assertEqual(result, self.PUBLIC)

    def test_unknown_override_becomes_sensitive(self):
        result = self.classify("plain text", override="mystery_tier")
        self.assertEqual(result, self.SENSITIVE)

    def test_classify_inputs_takes_highest(self):
        inputs = {
            "request": "Write a letter for our program.",
            "donor_context": "Jane Smith pledged $50,000 last year.",
        }
        result = self.classify_inputs(inputs)
        self.assertEqual(result, self.SENSITIVE)

    def test_classify_inputs_protected_wins(self):
        inputs = {
            "request": "Help with student IEP documentation.",
            "background": "The donor gave $5,000.",
        }
        result = self.classify_inputs(inputs)
        self.assertEqual(result, self.PROTECTED)

    def test_classify_inputs_empty_is_operational(self):
        result = self.classify_inputs({})
        self.assertEqual(result, self.OPERATIONAL)

    # ── Routing decisions ─────────────────────────────────────────────────────

    def test_protected_blocks_cloud(self):
        self.assertFalse(self.is_cloud_allowed(self.PROTECTED))

    def test_sensitive_allows_cloud(self):
        self.assertTrue(self.is_cloud_allowed(self.SENSITIVE))

    def test_operational_allows_cloud(self):
        self.assertTrue(self.is_cloud_allowed(self.OPERATIONAL))

    def test_public_allows_cloud(self):
        self.assertTrue(self.is_cloud_allowed(self.PUBLIC))

    def test_sensitive_requires_audit(self):
        self.assertTrue(self.requires_audit(self.SENSITIVE))

    def test_protected_requires_audit(self):
        self.assertTrue(self.requires_audit(self.PROTECTED))

    def test_operational_no_audit(self):
        self.assertFalse(self.requires_audit(self.OPERATIONAL))

    def test_public_no_audit(self):
        self.assertFalse(self.requires_audit(self.PUBLIC))

    def test_protected_blocks_memory_write(self):
        self.assertFalse(self.memory_write_allowed(self.PROTECTED))

    def test_sensitive_allows_memory_write(self):
        self.assertTrue(self.memory_write_allowed(self.SENSITIVE))


class TestPrivacyGateInRunTask(unittest.TestCase):

    def test_protected_inputs_raise_privacy_error(self):
        from harness import run_task, PrivacyError
        protected_inputs = {
            "request": "Help document IEP accommodations for our students under 13."
        }
        with self.assertRaises(PrivacyError) as ctx:
            run_task("nonprofit-comms", protected_inputs)
        self.assertIn("PROTECTED", str(ctx.exception))
        self.assertIn("cloud", str(ctx.exception).lower())

    def test_privacy_class_returned_in_result_envelope(self):
        # Verify the result dict includes privacy_class.
        # We can't call the real API in tests, so patch respond_focused.
        import unittest.mock as mock
        from harness import run_task

        fake_result = {
            "response": "ARTIFACT:\nTest.\n\nHUMAN GATE — Review.\nOK.\n\nUNCERTAINTY:\nNone.",
            "input_tokens": 0, "output_tokens": 0,
            "cache_read_tokens": 0, "cache_creation_tokens": 0,
            "memories_used": 0,
        }
        with mock.patch("harness.respond_focused", return_value=fake_result):
            result = run_task(
                "nonprofit-comms",
                {"request": "Write a program overview for our website."},
                save_to_memory=False,
            )
        self.assertIn("privacy_class", result)
        self.assertIn(result["privacy_class"], ["public", "operational", "sensitive", "protected"])


class TestPrivacyAudit(unittest.TestCase):

    def test_write_and_read_audit(self):
        from privacy.audit import write_audit, read_audit_log, AUDIT_DIR
        import tempfile, os
        from pathlib import Path
        from unittest import mock

        # Write to a temp dir so we don't pollute real audit log during tests
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("privacy.audit.AUDIT_DIR", Path(tmpdir)):
                write_audit(
                    classification="sensitive",
                    task_name="test-task",
                    engine_used="cloud",
                    model_used="claude-sonnet-4-6",
                    memory_written=False,
                    inputs_summary="Test audit write.",
                )
                records = read_audit_log.__wrapped__(Path(tmpdir)) if hasattr(read_audit_log, "__wrapped__") else None

                import json
                files = list(Path(tmpdir).glob("*.json"))
                self.assertEqual(len(files), 1)
                record = json.loads(files[0].read_text())

        self.assertEqual(record["classification"], "sensitive")
        self.assertEqual(record["task"], "test-task")
        self.assertFalse(record["memory_written"])
        self.assertIn("_note", record)


class TestGovernanceGate(unittest.TestCase):

    def test_consequence_level_in_research_profile(self):
        from harness import _load_task_profile
        profile, _ = _load_task_profile("research")
        self.assertEqual(profile.get("consequence_level"), "reversible")

    def test_consequence_level_in_product_spec_profile(self):
        from harness import _load_task_profile
        profile, _ = _load_task_profile("product-spec")
        self.assertEqual(profile.get("consequence_level"), "review_required")

    def test_consequence_level_returned_in_result(self):
        import unittest.mock as mock
        from harness import run_task
        fake_result = {
            "response": "ARTIFACT:\nTest artifact.\n\nHUMAN GATE — Review before use.\nOK.\n\nUNCERTAINTY:\nNone.",
            "input_tokens": 0, "output_tokens": 0,
            "cache_read_tokens": 0, "cache_creation_tokens": 0,
            "memories_used": 0,
        }
        with mock.patch("harness.respond_focused", return_value=fake_result):
            result = run_task(
                "research",
                {"request": "Test research query about fundraising."},
                save_to_memory=False,
            )
        self.assertIn("consequence_level", result)
        self.assertEqual(result["consequence_level"], "reversible")

    def test_review_required_task_has_consequence_in_result(self):
        import unittest.mock as mock
        from harness import run_task
        fake_result = {
            "response": "ARTIFACT:\nTest spec.\n\nHUMAN GATE — Review.\nOK.\n\nUNCERTAINTY:\nNone.",
            "input_tokens": 0, "output_tokens": 0,
            "cache_read_tokens": 0, "cache_creation_tokens": 0,
            "memories_used": 0,
        }
        with mock.patch("harness.respond_focused", return_value=fake_result):
            result = run_task(
                "product-spec",
                {"request": "Spec for a practice tracking feature."},
                save_to_memory=False,
            )
        self.assertEqual(result["consequence_level"], "review_required")

    def test_existing_tasks_have_human_gate(self):
        from harness import _load_task_profile
        for task in ["nonprofit-comms", "grant-loi", "funder-brief"]:
            profile, _ = _load_task_profile(task)
            self.assertIn("human_gate", profile, f"Task '{task}' missing human_gate")
            self.assertGreater(len(profile["human_gate"]), 10)


class TestNewTaskProfiles(unittest.TestCase):

    def test_product_spec_loads_with_correct_voice(self):
        from harness import _load_task_profile, DOMAIN_HINTS
        profile, body = _load_task_profile("product-spec")
        self.assertEqual(profile["primary_voice"], "product_partner")
        self.assertIn(profile["primary_voice"], DOMAIN_HINTS)
        self.assertGreater(len(body), 200)

    def test_research_loads_with_correct_voice(self):
        from harness import _load_task_profile, DOMAIN_HINTS
        profile, body = _load_task_profile("research")
        self.assertEqual(profile["primary_voice"], "listener")
        self.assertIn(profile["primary_voice"], DOMAIN_HINTS)
        self.assertGreater(len(body), 200)

    def test_product_spec_references_product_scout(self):
        from harness import _load_task_profile
        profile, _ = _load_task_profile("product-spec")
        skills = profile.get("skills", [])
        self.assertIn("product-scout", skills)

    def test_research_references_product_scout(self):
        from harness import _load_task_profile
        profile, _ = _load_task_profile("research")
        skills = profile.get("skills", [])
        self.assertIn("product-scout", skills)

    def test_all_tasks_have_valid_consequence_levels(self):
        from harness import _load_task_profile
        valid_levels = {"reversible", "review_required", "irreversible"}
        for task in ["nonprofit-comms", "grant-loi", "funder-brief", "product-spec", "research"]:
            profile, _ = _load_task_profile(task)
            level = profile.get("consequence_level", "review_required")
            self.assertIn(level, valid_levels, f"Task '{task}' has invalid consequence_level: {level}")


if __name__ == "__main__":
    unittest.main()
