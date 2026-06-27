---
name: dependency-review
type: playbook
scope: meta
invocation: on-demand
description: Evaluate a package or dependency before adding it — license, security, maintenance, and alternatives check
---

# Dependency Review — Operational Protocol

Every dependency added is an attack surface added. A library that saves two hours today can cost two weeks when a CVE drops or the maintainer disappears. This protocol runs before any new package is added to the project.

## The Five Checks

### 1. License

| License | Status | Notes |
|---------|--------|-------|
| MIT, Apache 2.0, BSD | Green | Standard permissive — use freely |
| ISC, Unlicense | Green | Permissive |
| LGPL | Yellow | Linking is usually fine; embedding is not |
| GPL v2/v3 | Red for proprietary | Copyleft propagates to your code |
| AGPL | Red for SaaS | Network use triggers copyleft |
| No license | Red | No rights granted; cannot legally use |

If the license requires investigation, stop before installing.

### 2. Security Audit

Run before adding, and in CI after adding:

```bash
# Python
pip-audit --requirement requirements.txt

# JavaScript / Node
npm audit
npm audit --audit-level=moderate  # fail CI on moderate+
```

Check the CVE database for the package name: https://nvd.nist.gov

If any HIGH or CRITICAL CVE is open and unpatched: reject unless no alternative exists. If accepted under constraint, document it as TECH DEBT ACCEPTED — [CVE number] [when it must be resolved].

### 3. Maintenance Status

A package is at risk if:
- Last commit was more than 12 months ago
- Maintainer count is 1 (bus factor = 1)
- More than 50 open issues with no response pattern
- No releases in 18 months for an active-use library

Check: package repository commit history, release page, open issue response time.

### 4. Usage Signals

- Weekly downloads / install count (npm, PyPI stats)
- GitHub stars, but more importantly: stars *trend* (growing or plateauing?)
- Fork count and fork activity (are others maintaining it independently?)
- Are major projects using it? Named dependents?

High download counts signal that the CVE community watches it. A low-download package with a critical CVE may have no fix coming.

### 5. Alternatives Comparison

Before committing to a package, answer: is this the best available option, or the first one found?

- Search for 2-3 alternatives
- Compare on: feature fit, license, maintenance, size (smaller is safer)
- If you're wrapping a simple standard library function: write it yourself instead

The best dependency is often no dependency.

## Documentation

When a dependency passes review, record the decision:

```python
# requirements.txt or pyproject.toml comment
# [DEPENDENCY REVIEW: YYYY-MM-DD] requests 2.31.0 — MIT, CVE clean, well-maintained. Replaces manual urllib calls.
```

For any accepted risk, use the debt label:
```
# TECH DEBT ACCEPTED — AGPL license risk acknowledged, isolated in cli-only module, revisit if SaaS exposure changes.
```

## Rejection Protocol

If a dependency is rejected:
1. Note why in the PR description or commit message
2. Name the alternative used or the reason to build in-house
3. Do not leave the rejected package in requirements files

A rejected dependency decision is worth recording in episodic memory (`memory_type="decision"`) if it was a close call with significant tradeoffs.
