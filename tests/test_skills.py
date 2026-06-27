"""
tests/test_skills.py — Skill loader tests. No API required.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.loader import (
    _parse_frontmatter,
    _discover_skills,
    _select_skills,
    _aggregate_hints,
    load_skills_for_context,
    load_skill,
    load_skills_for_agent,
)


class TestFrontmatterParsing(unittest.TestCase):

    def test_parses_string_values(self):
        text = "---\nname: test-skill\nscope: meta\n---\nBody here."
        meta, body = _parse_frontmatter(text)
        self.assertEqual(meta["name"], "test-skill")
        self.assertEqual(meta["scope"], "meta")
        self.assertIn("Body here", body)

    def test_parses_list_values(self):
        text = "---\nhint_keywords: [funder, grant, application]\n---\nBody."
        meta, body = _parse_frontmatter(text)
        self.assertEqual(meta["hint_keywords"], ["funder", "grant", "application"])

    def test_parses_booleans(self):
        text = "---\nhint_project_scope: true\nother: false\n---\n"
        meta, _ = _parse_frontmatter(text)
        self.assertIs(meta["hint_project_scope"], True)
        self.assertIs(meta["other"], False)

    def test_no_frontmatter_returns_empty_meta(self):
        text = "# Just a markdown file\nNo frontmatter."
        meta, body = _parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertIn("Just a markdown", body)

    def test_body_stripped_correctly(self):
        text = "---\nname: x\n---\n\n# Title\nContent."
        _, body = _parse_frontmatter(text)
        self.assertTrue(body.startswith("# Title"))


class TestSkillDiscovery(unittest.TestCase):

    def test_discovers_twenty_skills(self):
        skills = _discover_skills()
        self.assertEqual(len(skills), 25)

    def test_all_skills_have_required_fields(self):
        for skill in _discover_skills():
            self.assertIn("name", skill, f"Missing name in {skill.get('_path')}")
            self.assertIn("scope", skill)
            self.assertIn("type", skill)
            self.assertIn("invocation", skill)

    def test_manifest_not_included(self):
        names = [s["name"] for s in _discover_skills()]
        self.assertNotIn("MANIFEST", names)

    def test_known_skills_present(self):
        names = {s["name"] for s in _discover_skills()}
        expected = {
            # Meta / universal — original
            "canopy-stack", "agent-memory-practice",
            "constitutional-deliberation", "ethical-product-design",
            "reframing-constraints", "org-memory",
            # Nonprofit — original
            "opportunity-scout", "comms-writer",
            # Nonprofit — added v0.3
            "el-sistema-model", "nonprofit-formation", "nonprofit-grant-cycle",
            # Meta — added v0.3
            "enhancement-proposal", "code-health", "dependency-review",
            # Universal — added v0.3
            "governance-gate", "product-scout",
            # Meta / universal — added v0.4 (Project Sprout close)
            "scout", "learn",
            # Added v1
            "experiment-protocol", "market-voice",
            # Added v1.1 — brand, research
            "brand-identity", "positive-alignment", "research-grounding",
            # Added v1.2 — unified voice, context engineering
            "canopy-voice", "context-engineering",
        }
        self.assertEqual(names, expected)


class TestSkillSelection(unittest.TestCase):

    def setUp(self):
        self.all_skills = _discover_skills()

    def test_default_loads_five_auto_skills(self):
        selected = _select_skills(self.all_skills, project_context=None, explicit=None)
        names = {s["name"] for s in selected}
        # meta/auto and universal/auto
        self.assertIn("canopy-stack", names)
        self.assertIn("agent-memory-practice", names)
        self.assertIn("constitutional-deliberation", names)
        self.assertIn("ethical-product-design", names)
        self.assertIn("governance-gate", names)
        # on-demand not loaded without explicit
        self.assertNotIn("reframing-constraints", names)
        self.assertNotIn("opportunity-scout", names)
        self.assertNotIn("nonprofit-formation", names)

    def test_governance_gate_auto_loaded(self):
        selected = _select_skills(self.all_skills, project_context=None, explicit=None)
        names = {s["name"] for s in selected}
        self.assertIn("governance-gate", names)

    def test_explicit_forces_on_demand_skill(self):
        selected = _select_skills(
            self.all_skills, project_context=None, explicit=["reframing-constraints"]
        )
        names = {s["name"] for s in selected}
        self.assertIn("reframing-constraints", names)

    def test_explicit_forces_fungible_skill(self):
        selected = _select_skills(
            self.all_skills, project_context=None, explicit=["opportunity-scout"]
        )
        names = {s["name"] for s in selected}
        self.assertIn("opportunity-scout", names)
        self.assertIn("canopy-stack", names)  # auto skills still load

    def test_no_duplicates(self):
        selected = _select_skills(
            self.all_skills,
            project_context=None,
            explicit=["canopy-stack"],  # already auto-loaded
        )
        names = [s["name"] for s in selected]
        self.assertEqual(len(names), len(set(names)))


class TestMemoryHintAggregation(unittest.TestCase):

    def test_empty_hints_from_auto_skills(self):
        all_skills = _discover_skills()
        active = _select_skills(all_skills, project_context=None, explicit=None)
        hints = _aggregate_hints(active)
        # auto-loaded skills don't declare hints
        self.assertEqual(hints["keywords"], [])
        self.assertFalse(hints["project_scope"])

    def test_hints_populated_from_opportunity_scout(self):
        all_skills = _discover_skills()
        active = _select_skills(all_skills, project_context=None, explicit=["opportunity-scout"])
        hints = _aggregate_hints(active)
        self.assertIn("funder", hints["keywords"])
        self.assertIn("grant", hints["keywords"])
        self.assertTrue(hints["project_scope"])

    def test_hints_merge_from_multiple_skills(self):
        all_skills = _discover_skills()
        active = _select_skills(
            all_skills, project_context=None,
            explicit=["opportunity-scout", "comms-writer"]
        )
        hints = _aggregate_hints(active)
        # comms-writer adds language/voice keywords
        self.assertIn("donor", hints["keywords"])
        # opportunity-scout adds funder keywords
        self.assertIn("funder", hints["keywords"])


class TestLoadSkillsForContext(unittest.TestCase):

    def test_returns_tuple(self):
        result = load_skills_for_context()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_default_skill_text_nonempty(self):
        text, _ = load_skills_for_context()
        self.assertGreater(len(text), 100)

    def test_explicit_adds_skill(self):
        default_text, _ = load_skills_for_context()
        explicit_text, _ = load_skills_for_context(explicit=["opportunity-scout"])
        self.assertGreater(len(explicit_text), len(default_text))
        self.assertIn("opportunity-scout".upper().replace("-", " "), explicit_text.upper())


class TestLegacyAPI(unittest.TestCase):

    def test_load_skill_strips_frontmatter(self):
        content = load_skill("canopy_stack")
        self.assertNotIn("---", content.split("\n")[0])
        self.assertGreater(len(content), 50)

    def test_load_skill_unknown_returns_empty(self):
        self.assertEqual(load_skill("nonexistent_skill"), "")

    def test_load_skills_for_agent_builder(self):
        result = load_skills_for_agent("builder")
        self.assertGreater(len(result), 0)
        self.assertIn("CANOPY STACK", result.upper())

    def test_load_skills_for_agent_unknown_returns_empty(self):
        result = load_skills_for_agent("nobody")
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
