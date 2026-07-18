#!/usr/bin/env bash
# Build DOCX, self-contained HTML, offline website ZIP, tagged PDF/UA-1, and
# EPUB 3 editions from Markdown sources using Pandoc and Typst.
#
# Usage:
#   build-book.sh --format all|html|docx|pdf|epub|website-zip
#                  [--volume <volume-slug>] [--chapter <path/to/chapter.md>]
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

format="all"
volume=""
chapter=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --format) format="$2"; shift 2 ;;
    --volume) volume="$2"; shift 2 ;;
    --chapter) chapter="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

for cmd in pandoc typst; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "build-book.sh: '$cmd' not found. See SETUP.md." >&2
    exit 1
  fi
done

mkdir -p output/html output/docx output/pdf output/epub output/website-zip

echo "build-book.sh: format=$format volume=${volume:-<all>} chapter=${chapter:-<none>}"
echo "build-book.sh: this is a scaffold entry point — wire per-format Pandoc/Typst" \
     "invocations here as each volume passes its completed-volume gate in book.yml."
