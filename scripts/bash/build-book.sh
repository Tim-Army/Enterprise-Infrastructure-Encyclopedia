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
# Known limitation: internal links between chapters/volumes point at the
# original .md paths and are not rewritten to .html targets, so
# cross-chapter links in the generated output are not clickable. Fixing
# that requires a link-rewriting pass and is not yet implemented.
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

first_line_title() {
  head -1 "$1" | sed -E 's/^# (Chapter [0-9]+: )?//'
}

build_chapter_html() {
  local chapter_file="$1" volume_slug="$2"
  local base title outdir
  base="$(basename "$chapter_file" .md)"
  title="$(first_line_title "$chapter_file")"
  outdir="output/html/$volume_slug"
  mkdir -p "$outdir"
  pandoc "$chapter_file" \
    --standalone --embed-resources \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --toc --toc-depth=2 \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "$outdir/$base.html"
}

build_chapter_epub() {
  local chapter_file="$1" volume_slug="$2"
  local base title outdir
  base="$(basename "$chapter_file" .md)"
  title="$(first_line_title "$chapter_file")"
  outdir="output/epub/$volume_slug"
  mkdir -p "$outdir"
  pandoc "$chapter_file" \
    --toc --toc-depth=2 \
    --css=publishing/web.css \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "$outdir/$base.epub"
}

build_volume_html() {
  local volume_dir="$1" volume_slug title chapters
  volume_dir="${1%/}"
  volume_slug="$(basename "$volume_dir")"
  title="$(first_line_title "$volume_dir/README.md")"
  mkdir -p "output/html/$volume_slug"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find "$volume_dir/chapters" -name "*.md" | sort)
  pandoc "$volume_dir/README.md" "${chapters[@]}" \
    --standalone --embed-resources \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --toc --toc-depth=2 \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "output/html/$volume_slug/complete-volume.html"
}

build_volume_epub() {
  local volume_dir="$1" volume_slug title chapters
  volume_dir="${1%/}"
  volume_slug="$(basename "$volume_dir")"
  title="$(first_line_title "$volume_dir/README.md")"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find "$volume_dir/chapters" -name "*.md" | sort)
  pandoc "$volume_dir/README.md" "${chapters[@]}" \
    --toc --toc-depth=2 \
    --css=publishing/web.css \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "output/epub/$volume_slug.epub"
}

build_series_html() {
  local chapters
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find volumes -path "*/chapters/*.md" | sort)
  pandoc README.md "${chapters[@]}" \
    --standalone --embed-resources \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --toc --toc-depth=2 \
    --metadata "title=$series_title — Complete Edition" \
    --metadata "author=$author" \
    -o "output/html/complete-encyclopedia.html"
}

build_series_epub() {
  local chapters
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find volumes -path "*/chapters/*.md" | sort)
  pandoc README.md "${chapters[@]}" \
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
