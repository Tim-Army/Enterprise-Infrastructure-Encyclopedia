#!/usr/bin/env bash
# Build self-contained HTML and EPUB 3 editions from Markdown sources using
# Pandoc. Chapter and volume order comes directly from the volumes/
# directory structure (zero-padded volume and chapter numbers), which
# scripts/bash/validate.sh already confirms is contiguous and gap-free.
#
# Usage:
#   build-book.sh --format all|html|epub
#                  [--volume <volume-slug>] [--chapter <path/to/chapter.md>]
#
# With no --volume/--chapter, builds every chapter, every volume (combined),
# and the complete-series edition. --volume scopes to one volume (its
# chapters plus the combined volume edition). --chapter builds only that
# one chapter.
#
# Links to other chapters (volumes/*/chapters/*.md) are rewritten by
# scripts/bash/lib/rewrite_chapter_links.py before each Pandoc invocation:
# in HTML output they become relative links to that chapter's own .html
# file; in EPUB output (which cannot address a separate output/html/ file)
# they become absolute links to the deployed Pages portal. Links to
# anything other than a chapter file (root docs, volume/root README,
# INDEX, GLOSSARY) are left as-is, since those have no generated-output
# equivalent to point at.
#
# Every link in HTML output (internal and external alike) opens in a new
# tab via scripts/pandoc/open-links-new-tab.lua, applied at Pandoc
# conversion time — not used for EPUB, since e-readers have no tab concept.
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

if ! command -v pandoc >/dev/null 2>&1; then
  echo "build-book.sh: 'pandoc' not found. See SETUP.md." >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "build-book.sh: 'python3' not found (needed for chapter-link rewriting)." >&2
  exit 1
fi

want_html=0
want_epub=0
case "$format" in
  all) want_html=1; want_epub=1 ;;
  html) want_html=1 ;;
  epub) want_epub=1 ;;
  *) echo "build-book.sh: unknown --format '$format' (want all|html|epub)" >&2; exit 1 ;;
esac

mkdir -p output/html output/epub

series_title="Enterprise Infrastructure Encyclopedia"
author="Enterprise Infrastructure Encyclopedia Project"

link_tmp="$(mktemp -d)"
trap 'rm -rf "$link_tmp"' EXIT

# Rewrite chapter links in $1 for $2 (html-flat|html-root|epub-absolute),
# optionally scoped to volume $3 for html-flat. Prints the path to a
# rewritten temp copy of the file.
rewrite_file() {
  local src="$1" mode="$2" vol="${3:-}" dest
  dest="$link_tmp/$src"
  mkdir -p "$(dirname "$dest")"
  python3 "$repo_root/scripts/bash/lib/rewrite_chapter_links.py" "$src" "$mode" "$vol" > "$dest"
  printf '%s' "$dest"
}

first_line_title() {
  head -1 "$1" | sed -E 's/^# (Chapter [0-9]+: )?//'
}

build_chapter_html() {
  local chapter_file="$1" volume_slug="$2"
  local base title outdir rewritten
  base="$(basename "$chapter_file" .md)"
  title="$(first_line_title "$chapter_file")"
  outdir="output/html/$volume_slug"
  mkdir -p "$outdir"
  rewritten="$(rewrite_file "$chapter_file" html-flat "$volume_slug")"
  pandoc "$rewritten" \
    --standalone --embed-resources \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --lua-filter=scripts/pandoc/open-links-new-tab.lua \
    --toc --toc-depth=2 \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "$outdir/$base.html"
}

build_chapter_epub() {
  local chapter_file="$1" volume_slug="$2"
  local base title outdir rewritten
  base="$(basename "$chapter_file" .md)"
  title="$(first_line_title "$chapter_file")"
  outdir="output/epub/$volume_slug"
  mkdir -p "$outdir"
  rewritten="$(rewrite_file "$chapter_file" epub-absolute)"
  pandoc "$rewritten" \
    --toc --toc-depth=2 \
    --css=publishing/web.css \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "$outdir/$base.epub"
}

build_volume_html() {
  local volume_dir="$1" volume_slug title chapters ch rewritten_readme rewritten_chapters
  volume_dir="${1%/}"
  volume_slug="$(basename "$volume_dir")"
  title="$(first_line_title "$volume_dir/README.md")"
  mkdir -p "output/html/$volume_slug"
  rewritten_readme="$(rewrite_file "$volume_dir/README.md" html-flat "$volume_slug")"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find "$volume_dir/chapters" -name "*.md" | sort)
  rewritten_chapters=()
  for ch in "${chapters[@]}"; do
    rewritten_chapters+=("$(rewrite_file "$ch" html-flat "$volume_slug")")
  done
  pandoc "$rewritten_readme" "${rewritten_chapters[@]}" \
    --standalone --embed-resources \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --lua-filter=scripts/pandoc/open-links-new-tab.lua \
    --toc --toc-depth=2 \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "output/html/$volume_slug/complete-volume.html"
}

build_volume_epub() {
  local volume_dir="$1" volume_slug title chapters ch rewritten_readme rewritten_chapters
  volume_dir="${1%/}"
  volume_slug="$(basename "$volume_dir")"
  title="$(first_line_title "$volume_dir/README.md")"
  rewritten_readme="$(rewrite_file "$volume_dir/README.md" epub-absolute)"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find "$volume_dir/chapters" -name "*.md" | sort)
  rewritten_chapters=()
  for ch in "${chapters[@]}"; do
    rewritten_chapters+=("$(rewrite_file "$ch" epub-absolute)")
  done
  pandoc "$rewritten_readme" "${rewritten_chapters[@]}" \
    --toc --toc-depth=2 \
    --css=publishing/web.css \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "output/epub/$volume_slug.epub"
}

build_series_html() {
  local chapters ch rewritten_readme rewritten_chapters
  rewritten_readme="$(rewrite_file "README.md" html-root)"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find volumes -path "*/chapters/*.md" | sort)
  rewritten_chapters=()
  for ch in "${chapters[@]}"; do
    rewritten_chapters+=("$(rewrite_file "$ch" html-root)")
  done
  pandoc "$rewritten_readme" "${rewritten_chapters[@]}" \
    --standalone --embed-resources \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --lua-filter=scripts/pandoc/open-links-new-tab.lua \
    --toc --toc-depth=2 \
    --metadata "title=$series_title — Complete Edition" \
    --metadata "author=$author" \
    -o "output/html/complete-encyclopedia.html"
}

build_series_epub() {
  local chapters ch rewritten_readme rewritten_chapters
  rewritten_readme="$(rewrite_file "README.md" epub-absolute)"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find volumes -path "*/chapters/*.md" | sort)
  rewritten_chapters=()
  for ch in "${chapters[@]}"; do
    rewritten_chapters+=("$(rewrite_file "$ch" epub-absolute)")
  done
  pandoc "$rewritten_readme" "${rewritten_chapters[@]}" \
    --toc --toc-depth=2 \
    --css=publishing/web.css \
    --metadata "title=$series_title — Complete Edition" \
    --metadata "author=$author" \
    -o "output/epub/complete-encyclopedia.epub"
}

if [[ -n "$chapter" ]]; then
  volume_slug="$(basename "$(dirname "$(dirname "$chapter")")")"
  echo "build-book.sh: building chapter $chapter"
  [[ "$want_html" -eq 1 ]] && build_chapter_html "$chapter" "$volume_slug"
  [[ "$want_epub" -eq 1 ]] && build_chapter_epub "$chapter" "$volume_slug"
elif [[ -n "$volume" ]]; then
  volume_dir="volumes/$volume"
  if [[ ! -d "$volume_dir" ]]; then
    echo "build-book.sh: no such volume '$volume'" >&2
    exit 1
  fi
  echo "build-book.sh: building volume $volume"
  for ch in "$volume_dir"/chapters/*.md; do
    [[ "$want_html" -eq 1 ]] && build_chapter_html "$ch" "$volume"
    [[ "$want_epub" -eq 1 ]] && build_chapter_epub "$ch" "$volume"
  done
  [[ "$want_html" -eq 1 ]] && build_volume_html "$volume_dir"
  [[ "$want_epub" -eq 1 ]] && build_volume_epub "$volume_dir"
else
  echo "build-book.sh: building all 24 volumes and the complete series"
  for volume_dir in volumes/*/; do
    volume_slug="$(basename "${volume_dir%/}")"
    for ch in "$volume_dir"chapters/*.md; do
      [[ "$want_html" -eq 1 ]] && build_chapter_html "$ch" "$volume_slug"
      [[ "$want_epub" -eq 1 ]] && build_chapter_epub "$ch" "$volume_slug"
    done
    [[ "$want_html" -eq 1 ]] && build_volume_html "$volume_dir"
    [[ "$want_epub" -eq 1 ]] && build_volume_epub "$volume_dir"
    echo "build-book.sh: built $volume_slug"
  done
  [[ "$want_html" -eq 1 ]] && build_series_html
  [[ "$want_epub" -eq 1 ]] && build_series_epub
fi

echo "build-book.sh: done — output under output/html/ and output/epub/"
