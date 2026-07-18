#!/usr/bin/env bash
# Check external links across all Markdown files with Lychee. Requires network
# access; not part of the default (non-networked) validation gate.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

if ! command -v lychee >/dev/null 2>&1; then
  echo "check-external-links.sh: 'lychee' not found. See SETUP.md." >&2
  exit 1
fi

lychee --config lychee.toml "**/*.md"
