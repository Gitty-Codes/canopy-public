#!/bin/bash
# Push a clean mirror of main to the public repo.
# Uses an orphan branch so the public repo has no commit history containing
# private data — every push produces a single clean initial commit.
#
# The public repo contains ONLY the CLI harness:
#   harness.py, constitution/, skills/, tasks/ (general), privacy/,
#   consequence/, memory/ (code only), models/, tests/, research/, tools/
#
# NEVER add client files, product code, session data, or strategy docs.
# When in doubt about a new file: add it to PRIVATE_PATHS before running.
#
# Usage: bash tools/push-public.sh
# Run from the repo root.

set -e

PRIVATE_PATHS=(
    # ── Product (not the harness) ─────────────────────────────────────────────
    "webapp"

    # ── Client project files ──────────────────────────────────────────────────
    "projects/clients"
    "projects/internal"

    # ── Internal strategy and governance ─────────────────────────────────────
    "proposals"

    # ── Session and runtime data ──────────────────────────────────────────────
    "memory/episodic"
    "memory/privacy_audit"
    "memory/kaizen_log.json"
    "memory/growth_log.json"
    "memory/semantic/patterns.db"
    "memory/semantic/summary.md"

    # ── Client-specific task profiles ─────────────────────────────────────────
    "tasks/grant-loi.md"
    "tasks/funder-brief.md"
    "tasks/constitution-evolution-plan.md"
    "tasks/threshold"
    "tasks/threshold-alpha-brief.md"
    "tasks/threshold-client-guide.md"
    "tasks/threshold-developer-spec.md"

    # ── Client-specific skills ────────────────────────────────────────────────
    "skills/el-sistema-model.md"

    # ── Private constitution content ──────────────────────────────────────────
    "constitution/founding-conversation-2026-03-28"

    # ── Proprietary research ──────────────────────────────────────────────────
    "research/resonant-mind-training/outreach-letters-ready.md"
    "research/resonant-mind-training/rights-holder-outreach.md"

    # ── Client provisioning tools ─────────────────────────────────────────────
    "tools/provision_org.py"
)

echo "=== Canopy public mirror push ==="
echo ""
echo "Private paths to exclude:"
for p in "${PRIVATE_PATHS[@]}"; do
    echo "  - $p"
done
echo ""

# Verify we're on main and it's clean
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
    echo "ERROR: must be on main branch (currently on $BRANCH)"
    exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERROR: uncommitted changes present. Commit or stash before pushing public."
    exit 1
fi

# Clean up any leftover temp branch from a previous failed run
git branch -D _public_push 2>/dev/null || true

# Orphan branch: no history, working tree and index populated from current HEAD
echo "Creating orphan branch from main (clean history — no prior commits in public remote)..."
git checkout --orphan _public_push

# Remove private paths from the index
REMOVED=0
for p in "${PRIVATE_PATHS[@]}"; do
    if git ls-files --error-unmatch "$p" > /dev/null 2>&1; then
        git rm -r --cached "$p" --quiet
        echo "  Removed: $p"
        REMOVED=$((REMOVED + 1))
    fi
done

echo ""
echo "Removed $REMOVED private path(s) from index."
echo ""

git commit -m "chore: public mirror — private paths excluded [ci skip]"
echo "Committed clean state."

echo ""
echo "Pushing to public remote (force — replaces full history with single clean commit)..."
git push public _public_push:main --force

# Return to main, clean up temp branch
git checkout -f main
git branch -D _public_push

echo ""
echo "Done. Public repo updated."
echo "Verify at: https://github.com/Gitty-Codes/canopy-public"
