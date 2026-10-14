#!/usr/bin/env bash
# Usage: bash .claude/skills/srg-mapping-for/check.sh <chapter-file>   (run from the repo root)
# Regenerates the CSV downloads, then runs markdownlint, cspell, the internal
# link check, and the book.yml check for a new Volume CLXXII chapter.
set -u
V=volumes/volume-172-disa-srgs-and-stigs
F=$V/chapters/$1
[[ -f "$F" ]] || { echo "check.sh: no such chapter: $F" >&2; exit 1; }
echo "== csv"; PYTHONIOENCODING=utf-8 python scripts/python/export_srg_tables.py | grep -F "${1%.md}" || echo "(no map tables in this chapter)"
echo "== markdownlint"; npx --yes markdownlint-cli2 "$F" $V/*.md README.md PROJECT_STATUS.md 2>&1 | grep -E "^(volumes|README|PROJECT)" || echo "clean"
echo "== cspell"; npx --yes cspell --no-progress "$F" $V/*.md 2>&1 | tail -3
echo "== links"; python scripts/python/check_internal_links.py 2>&1 | tail -1
echo "== book"; python scripts/python/check_book_yml.py 2>&1 | tail -1
git status --short
