#!/usr/bin/env python
"""
tests/run.py — The Canopy test runner.

Runs all test suites, records results in benchmark.db, prints a report.
No API key required.

Usage:
  python tests/run.py              # run all suites
  python tests/run.py skills       # run one suite
  python tests/run.py --report     # show benchmark report only
"""
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

SUITES = {
    "skills":  "tests.test_skills",
    "memory":  "tests.test_memory",
    "kg":      "tests.test_kg",
    "harness": "tests.test_harness",
}


def run_suite(name: str, module_path: str) -> dict:
    """Runs one test suite. Returns result dict."""
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromName(module_path)

    stream = open("/dev/null", "w")  # suppress unittest output; we format our own
    runner = unittest.TextTestRunner(stream=stream, verbosity=0)

    t0     = time.time()
    result = runner.run(suite)
    ms     = int((time.time() - t0) * 1000)
    stream.close()

    passed = result.testsRun - len(result.failures) - len(result.errors)
    return {
        "name":     name,
        "passed":   passed,
        "failed":   len(result.failures),
        "errors":   len(result.errors),
        "total":    result.testsRun,
        "ms":       ms,
        "failures": [(t, msg) for t, msg in result.failures + result.errors],
    }


def print_suite_result(r: dict) -> None:
    ok   = r["failed"] == 0 and r["errors"] == 0
    mark = "✓" if ok else "✗"
    print(f"  {mark} {r['name']:<10}  {r['passed']}/{r['total']} passed  ({r['ms']}ms)")
    for test, msg in r["failures"]:
        # Extract just the test name and first line of error
        test_name = str(test).split(" ")[0]
        first_line = msg.strip().splitlines()[-1][:100]
        print(f"      ✗ {test_name}")
        print(f"        {first_line}")


def record_results(results: list[dict]) -> None:
    """Writes run results to benchmark.db."""
    try:
        from memory.benchmark import record_test_run, record_test_result
        for r in results:
            run_id = record_test_run(
                suite=r["name"],
                passed=r["passed"],
                failed=r["failed"],
                errors=r["errors"],
                duration_ms=r["ms"],
            )
            for test, msg in r["failures"]:
                test_name = str(test).split(" ")[0]
                record_test_result(run_id, test_name, "fail", msg[:300])
    except Exception as e:
        print(f"  (benchmark recording failed: {e})")


def main() -> int:
    args = sys.argv[1:]

    if "--report" in args:
        from memory.benchmark import report
        print(report())
        return 0

    # Determine which suites to run
    requested = [a for a in args if a in SUITES]
    to_run    = {k: v for k, v in SUITES.items() if not requested or k in requested}

    print(f"\nThe Canopy — Test Suite\n{'─' * 40}")

    results    = []
    total_pass = 0
    total_fail = 0
    t_start    = time.time()

    for name, module_path in to_run.items():
        r = run_suite(name, module_path)
        results.append(r)
        print_suite_result(r)
        total_pass += r["passed"]
        total_fail += r["failed"] + r["errors"]

    elapsed = int((time.time() - t_start) * 1000)
    print(f"\n{'─' * 40}")

    if total_fail == 0:
        print(f"✓ All {total_pass} tests passed  ({elapsed}ms)\n")
    else:
        print(f"✗ {total_fail} failed, {total_pass} passed  ({elapsed}ms)\n")

    record_results(results)
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
