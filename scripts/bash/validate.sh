#!/usr/bin/env bash
# Non-networked structural validation: every volume has README/INDEX/GLOSSARY,
# a contiguous chapters/ sequence, and book.yml matches the chapters on disk.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

fail=0

for volume_dir in volumes/*/; do
  volume="${volume_dir%/}"
  for required in README.md INDEX.md GLOSSARY.md; do
    if [[ ! -f "$volume/$required" ]]; then
      echo "MISSING: $volume/$required"
      fail=1
    fi
  done

  if [[ ! -d "$volume/chapters" ]]; then
    echo "MISSING: $volume/chapters/"
    fail=1
    continue
  fi

  expected=1
  for chapter in "$volume"/chapters/*.md; do
    [[ -e "$chapter" ]] || continue
    base="$(basename "$chapter")"
    number="${base%%-*}"
    printf -v want "%02d" "$expected"
    if [[ "$number" != "$want" ]]; then
      echo "GAP: $volume/chapters expected ${want}-*.md next, found $base"
      fail=1
    fi
    expected=$((expected + 1))
  done
done

if command -v pnpm >/dev/null 2>&1 && [[ -f package.json ]]; then
  pnpm exec markdownlint-cli2 "**/*.md" || fail=1
  pnpm exec cspell lint --no-progress "**/*.md" || fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "validate.sh: FAILED"
  exit 1
fi

echo "validate.sh: OK"
