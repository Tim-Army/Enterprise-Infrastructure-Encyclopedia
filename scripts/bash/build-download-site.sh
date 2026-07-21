#!/usr/bin/env bash
# Build the combined reading and download portal deployed by the Pages
# workflow. Requires scripts/bash/build-book.sh to have already populated
# output/html/ and output/epub/ — this script copies that output into the
# portal directory and generates the index pages that tie it together.
#
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

if [[ ! -d output/html || ! -d output/epub ]]; then
  echo "build-download-site.sh: output/html or output/epub not found." >&2
  echo "build-download-site.sh: run scripts/bash/build-book.sh first." >&2
  exit 1
fi

rm -rf "$output"
mkdir -p "$output"
cp publishing/web.css "$output/web.css"
cp -R output/html "$output/html"
cp -R output/epub "$output/epub"

page_head() {
  # $1 = <title> text
  # $2 = relative prefix from this page back to the site root, e.g. "../../"
  #      Defaults to "" for pages written at the root. Volume index pages sit
  #      two levels down under html/<slug>/, so a bare "web.css" resolves
  #      against their own directory and 404s, leaving the page unstyled and
  #      the theme toggle inert.
  local prefix="${2-}"
  cat <<HTML
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>$1</title>
<link rel="stylesheet" href="${prefix}web.css" />
</head>
<body>
HTML
}

page_tail() {
  cat publishing/repo-link.html
  cat publishing/theme-toggle.html
  echo "</body></html>"
}

volume_title() {
  head -1 "volumes/$1/README.md" | sed -E 's/^# //'
}

# --- root index.html ---
{
  page_head "Enterprise Infrastructure Encyclopedia"
  echo "<h1>Enterprise Infrastructure Encyclopedia</h1>"
  echo "<p>A volume-first, documentation-as-code curriculum for enterprise infrastructure.</p>"
  echo "<h2>Complete edition</h2>"
  echo "<ul>"
  echo "<li><a href=\"html/complete-encyclopedia.html\">Read online (HTML)</a></li>"
  echo "<li><a href=\"epub/Enterprise-Infrastructure-Encyclopedia.epub\">Download (EPUB)</a></li>"
  echo "</ul>"
  echo "<h2>Volumes</h2>"
  echo "<ul>"
  for volume_dir in volumes/*/; do
    slug="$(basename "${volume_dir%/}")"
    title="$(volume_title "$slug")"
    echo "<li><a href=\"html/$slug/index.html\">$title</a></li>"
  done
  echo "</ul>"
  page_tail
} > "$output/index.html"

# --- per-volume index.html ---
for volume_dir in volumes/*/; do
  slug="$(basename "${volume_dir%/}")"
  title="$(volume_title "$slug")"
  {
    page_head "$title" "../../"
    echo "<p><a href=\"../../index.html\">&larr; All volumes</a></p>"
    echo "<h1>$title</h1>"
    echo "<h2>Complete volume</h2>"
    echo "<ul>"
    echo "<li><a href=\"complete-volume.html\">Read online (HTML)</a></li>"
    echo "<li><a href=\"../../epub/Enterprise-Infrastructure-Encyclopedia.epub\">Download the complete encyclopedia (EPUB)</a></li>"
    echo "</ul>"
    echo "<h2>Chapters</h2>"
    echo "<ul>"
    for chapter in "$volume_dir"chapters/*.md; do
      base="$(basename "$chapter" .md)"
      chtitle="$(head -1 "$chapter" | sed -E 's/^# //')"
      echo "<li><a href=\"$base.html\">$chtitle</a></li>"
    done
    echo "</ul>"
    page_tail
  } > "$output/html/$slug/index.html"
done

# --- verify every generated link resolves ---
broken=0
while IFS= read -r -d '' html_file; do
  dir="$(dirname "$html_file")"
  while IFS= read -r href; do
    target="${href%%#*}"
    [[ -z "$target" ]] && continue
    case "$target" in http://*|https://*|mailto:*) continue ;; esac
    if [[ ! -e "$dir/$target" ]]; then
      echo "build-download-site.sh: BROKEN LINK in $html_file -> $target" >&2
      broken=1
    fi
  done < <(grep -oE 'href="[^"]+"' "$html_file" | sed -E 's/href="([^"]+)"/\1/')
done < <(find "$output" -name "index.html" -print0)

if [[ "$broken" -ne 0 ]]; then
  echo "build-download-site.sh: FAILED — portal has broken links" >&2
  exit 1
fi

echo "build-download-site.sh: wrote portal to $output/ (all catalog links verified)"
