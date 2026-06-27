"""
tests/test_kg.py — Temporal knowledge graph tests. No API required.

Test isolation: setUpModule patches KG_PATH to a temp file so tests
never touch the live kg.db. tearDownModule restores the original path.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import memory.kg as _kg_module
from memory.kg import (
    add_entity,
    get_entity,
    add_relationship,
    invalidate_relationship,
    query_relationships,
    add_decision,
    supersede_decision,
    invalidate_decision,
    query_decisions,
    record_approach,
    query_approaches,
    failed_approaches,
    format_for_context,
    kg_status,
)

_tmpdb = None
_original_kg_path = None


def setUpModule():
    global _tmpdb, _original_kg_path
    _original_kg_path = _kg_module.KG_PATH
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    _tmpdb = tmp.name
    _kg_module.KG_PATH = Path(_tmpdb)
    _kg_module._init()


def tearDownModule():
    global _original_kg_path
    if _original_kg_path is not None:
        _kg_module.KG_PATH = _original_kg_path
    if _tmpdb:
        try:
            os.unlink(_tmpdb)
        except OSError:
            pass


class TestEntities(unittest.TestCase):

    def test_add_and_get(self):
        add_entity("_test:entity1", "concept", "Test Entity", "A test entity")
        e = get_entity("_test:entity1")
        self.assertIsNotNone(e)
        self.assertEqual(e["name"], "Test Entity")
        self.assertEqual(e["type"], "concept")

    def test_get_nonexistent_returns_none(self):
        self.assertIsNone(get_entity("_test:does_not_exist"))

    def test_upsert_updates_name(self):
        add_entity("_test:upsert", "concept", "Original Name")
        add_entity("_test:upsert", "concept", "Updated Name")
        e = get_entity("_test:upsert")
        self.assertEqual(e["name"], "Updated Name")


class TestRelationships(unittest.TestCase):

    def setUp(self):
        add_entity("_test:from", "agent", "Test From")
        add_entity("_test:to", "concept", "Test To")

    def test_add_returns_id(self):
        rid = add_relationship("_test:from", "relates_to", "_test:to")
        self.assertIsInstance(rid, int)
        self.assertGreater(rid, 0)

    def test_query_by_entity(self):
        add_relationship("_test:from", "test_rel", "_test:to", "test context")
        rows = query_relationships(entity="_test:from")
        self.assertTrue(any(r["relation"] == "test_rel" for r in rows))

    def test_invalidate_removes_from_active(self):
        rid = add_relationship("_test:from", "temp_rel", "_test:to")
        active_before = query_relationships(entity="_test:from", active_only=True)
        invalidate_relationship(rid)
        active_after = query_relationships(entity="_test:from", active_only=True)
        before_ids = {r["id"] for r in active_before}
        after_ids = {r["id"] for r in active_after}
        self.assertIn(rid, before_ids)
        self.assertNotIn(rid, after_ids)

    def test_inactive_visible_when_active_only_false(self):
        rid = add_relationship("_test:from", "archived_rel", "_test:to")
        invalidate_relationship(rid)
        all_rows = query_relationships(entity="_test:from", active_only=False)
        self.assertTrue(any(r["id"] == rid for r in all_rows))


class TestDecisions(unittest.TestCase):

    def test_add_returns_id(self):
        did = add_decision("Test decision content", by_whom="test", reasoning="test reason")
        self.assertIsInstance(did, int)
        self.assertGreater(did, 0)

    def test_decision_starts_active(self):
        did = add_decision("Active decision", by_whom="test")
        decisions = query_decisions(status="active")
        ids = [d["id"] for d in decisions]
        self.assertIn(did, ids)

    def test_supersede_changes_status(self):
        did = add_decision("Decision to supersede")
        supersede_decision(did)
        active = [d["id"] for d in query_decisions(status="active")]
        superseded = [d["id"] for d in query_decisions(status="superseded")]
        self.assertNotIn(did, active)
        self.assertIn(did, superseded)

    def test_invalidate_changes_status(self):
        did = add_decision("Decision to invalidate")
        invalidate_decision(did)
        active = [d["id"] for d in query_decisions(status="active")]
        self.assertNotIn(did, active)

    def test_project_filter(self):
        did = add_decision("Project-scoped decision", project="_test_project")
        results = query_decisions(project="_test_project")
        ids = [d["id"] for d in results]
        self.assertIn(did, ids)

    def test_canopy_decisions_appear_in_project_query(self):
        canopy_did = add_decision("Canopy-level founding decision", project="canopy")
        project_did = add_decision("Project-specific decision", project="_test_proj2")
        results = query_decisions(project="_test_proj2")
        ids = [d["id"] for d in results]
        self.assertIn(canopy_did, ids)
        self.assertIn(project_did, ids)

    def test_canopy_query_excludes_other_projects(self):
        canopy_did = add_decision("Canopy decision", project="canopy")
        other_did = add_decision("Other project decision", project="_other_project")
        results = query_decisions(project="canopy")
        ids = [d["id"] for d in results]
        self.assertIn(canopy_did, ids)
        self.assertNotIn(other_did, ids)


class TestApproaches(unittest.TestCase):

    def test_record_success(self):
        aid = record_approach(
            problem_domain="_test_domain",
            approach="Direct approach",
            outcome="success",
            what_learned="Direct approaches work here.",
        )
        self.assertIsInstance(aid, int)

    def test_record_failure(self):
        aid = record_approach(
            problem_domain="_test_domain",
            approach="Failed approach",
            outcome="failure",
            what_failed="It didn't converge",
            what_learned="This approach diverges under load.",
        )
        rows = query_approaches(problem_domain="_test_domain", outcome="failure")
        ids = [r["id"] for r in rows]
        self.assertIn(aid, ids)

    def test_what_learned_required(self):
        with self.assertRaises(ValueError):
            record_approach("_test", "approach", "failure", what_learned="")

    def test_invalid_outcome_raises(self):
        with self.assertRaises(ValueError):
            record_approach("_test", "approach", "maybe", what_learned="something")

    def test_failed_approaches_returns_failures_and_partials(self):
        record_approach("_test_domain2", "fail1", "failure", what_learned="learned from fail1")
        record_approach("_test_domain2", "partial1", "partial", what_learned="learned from partial1")
        record_approach("_test_domain2", "success1", "success", what_learned="learned from success1")
        failures = failed_approaches(problem_domain="_test_domain2")
        outcomes = {r["outcome"] for r in failures}
        self.assertIn("failure", outcomes)
        self.assertIn("partial", outcomes)
        self.assertNotIn("success", outcomes)


class TestFormatForContext(unittest.TestCase):

    def test_returns_string(self):
        add_decision("Context format test decision")
        result = format_for_context()
        self.assertIsInstance(result, str)

    def test_includes_decision_text(self):
        unique = "UniqueDecision_XYZ_12345"
        add_decision(unique)
        result = format_for_context()
        self.assertIn(unique, result)

    def test_project_scoped_returns_string(self):
        result = format_for_context(project="_nonexistent_project_xyz", include_failures=False)
        self.assertIsInstance(result, str)

    def test_canopy_decisions_appear_in_project_format(self):
        unique = "CanopyDecision_format_test_XYZ"
        add_decision(unique, project="canopy")
        result = format_for_context(project="_some_project")
        self.assertIn(unique, result)


class TestKGStatus(unittest.TestCase):

    def test_status_has_required_keys(self):
        status = kg_status()
        self.assertIn("entities", status)
        self.assertIn("active_relationships", status)
        self.assertIn("active_decisions", status)
        self.assertIn("total_approaches", status)
        self.assertIn("failures_logged", status)

    def test_status_values_are_integers(self):
        status = kg_status()
        for v in status.values():
            self.assertIsInstance(v, int)


if __name__ == "__main__":
    unittest.main()
