#!/usr/bin/env bash
# Build the combined reading and download portal deployed by the Pages workflow.
# Usage: build-download-site.sh --output _site
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

output="_site"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) output="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$output"
cp publishing/web.css "$output/web.css"
cp publishing/theme-toggle.html "$output/theme-toggle.html"

echo "build-download-site.sh: wrote portal scaffold to $output/"
echo "build-download-site.sh: run build-book.sh first so per-volume/per-chapter" \
     "editions exist under output/ for this script to catalog."
