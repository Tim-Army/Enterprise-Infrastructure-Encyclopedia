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
# With no --volume/--chapter, builds every chapter and every volume
# (combined), plus the complete-encyclopedia EPUB. --volume scopes to one
# volume (its chapters plus the combined volume edition). --chapter builds
# only that one chapter.
#
# HTML is produced per chapter and per volume. EPUB is produced only as a
# single Enterprise-Infrastructure-Encyclopedia.epub: the whole work is one
# book, so --volume/--chapter scoping affects HTML alone. (The single-page
# complete-encyclopedia HTML edition was retired; the EPUB is the one-file
# edition.)
#
# Links to other chapters (volumes/*/chapters/*.md) and to volume READMEs
# (volumes/*/README.md) are rewritten by
# scripts/bash/lib/rewrite_chapter_links.py before each Pandoc invocation:
# in HTML output they become relative links to that chapter's own .html
# file (or that volume's Enterprise-Infrastructure-Encyclopedia.html); in EPUB output (which
# cannot address a separate output/html/ file) they become absolute links
# to the deployed Pages portal. Links to anything else (root docs,
# volume/root INDEX, GLOSSARY) are left as-is, since those have no
# generated-output equivalent to point at.
#
# Every link in HTML output (internal and external alike) opens in a new
# tab via scripts/pandoc/open-links-new-tab.lua, applied at Pandoc
# conversion time — not used for EPUB, since e-readers have no tab concept.
#
# implicit_figures is disabled. Left on, Pandoc wraps every image in a
# <figure> and repeats its alt text as a visible <figcaption>, so each
# diagram rendered its whole accessibility description as prose on the page
# before its real "Figure N-1" caption. The alt text stays on the <img>
# where assistive technology reads it; only the duplicated visible copy is
# gone.
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

# The project's creation date is a fixed constant (not derived from git log)
# because CI checks out a shallow clone, under which "earliest commit" would
# incorrectly resolve to whatever commit triggered the build. "Last updated"
# is the actual build date, which is accurate in any environment.
title_page_created="2026-07-18"
title_page_updated="$(date +%Y-%m-%d)"

# The EPUB's dc:identifier. Pandoc mints a fresh random UUID whenever one is
# not supplied, which makes every rebuild a different publication: readers
# stack the builds up as separate books rather than replacing the previous
# one, and the reader's position is lost each time. Pinning it keeps a
# rebuild an update to the same book. dcterms:modified still carries the
# build timestamp, so revisions remain distinguishable.
#
# Do not regenerate this value.
epub_identifier="https://github.com/Tim-Army/Enterprise-Infrastructure-Encyclopedia"

link_tmp="$(mktemp -d)"
trap 'rm -rf "$link_tmp"' EXIT

# Mirror diagrams/ into the rewrite workspace so relative image references
# in chapter Markdown (for example "../../../diagrams/...") resolve to a
# real local file, the same way they do in the repo itself. Pandoc then
# embeds the image directly (HTML via --embed-resources, EPUB by packaging
# it) instead of needing network access.
if [[ -d diagrams ]]; then
  mkdir -p "$link_tmp/diagrams"
  cp -r diagrams/. "$link_tmp/diagrams/"
fi

# The cover image is referenced from the rendered title page, so it needs to
# resolve inside the rewrite workspace too. $link_tmp is on the resource path
# for the series build, which is the only build the title page appears in.
mkdir -p "$link_tmp/publishing"
cp publishing/cover.png "$link_tmp/publishing/cover.png"

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

# Like rewrite_file, but then demotes every heading one level (see
# lib/demote_headings.py). Used for chapters in the concatenated editions so
# each chapter's "# Chapter N" title nests under its volume's "# Volume N" in
# the table of contents instead of sitting beside it. Standalone chapter
# pages call rewrite_file directly and keep their H1 title.
rewrite_and_demote() {
  local rewritten demoted
  rewritten="$(rewrite_file "$@")"
  demoted="${rewritten}.demoted.md"
  python3 "$repo_root/scripts/bash/lib/demote_headings.py" "$rewritten" > "$demoted"
  printf '%s' "$demoted"
}

# Single-page variants (lib/singlepage_rewrite.py): for the combined
# whole-volume page, rewrite cross-chapter/README links to in-page anchors and
# inject per-chapter namespaced heading ids (#cNN-...) so every reference
# resolves on the one page. Writes to the same $link_tmp/<src> location as
# rewrite_file so "../../../diagrams/..." still resolves.
rewrite_single() {
  local src="$1" vol="$2" dest
  dest="$link_tmp/$src"
  mkdir -p "$(dirname "$dest")"
  python3 "$repo_root/scripts/bash/lib/singlepage_rewrite.py" "$src" "$vol" > "$dest"
  printf '%s' "$dest"
}
rewrite_single_and_demote() {
  local rewritten demoted
  rewritten="$(rewrite_single "$@")"
  demoted="${rewritten}.demoted.md"
  python3 "$repo_root/scripts/bash/lib/demote_headings.py" "$rewritten" > "$demoted"
  printf '%s' "$demoted"
}

first_line_title() {
  head -1 "$1" | sed -E 's/^# (Chapter [0-9]+: )?//'
}

# Renders the footer shared by every generated page and prints its path.
#
# The "Volume contents" link points at the page's sibling index.html — the
# volume's chapter list on the portal — so the footer is identical for every
# page and takes no arguments.
footer_for() {
  local dest links
  dest="$link_tmp/footer.html"
  links="<li><a href=\"index.html\">Volume contents</a></li>"
  links+="<li><a href=\"#\">Back to top</a></li>"
  {
    printf '<nav id="page-nav" aria-label="Page navigation"><ul>%s</ul></nav>\n' "$links"
    cat publishing/repo-link.html
  } > "$dest"
  printf '%s' "$dest"
}

# Renders publishing/title-page.md and prints the path to the rendered copy.
#
# This is the cover page of the encyclopedia as a whole, so it is built into
# the complete-encyclopedia EPUB only. Per-chapter and per-volume HTML pages
# do not carry a copy of any title page.
title_page_for() {
  local dest="$link_tmp/title-page.md"
  python3 "$repo_root/scripts/bash/lib/render_template.py" \
    publishing/title-page.md \
    "CREATED_DATE=$title_page_created" \
    "UPDATED_DATE=$title_page_updated" > "$dest"
  # EPUB supplies the cover through --epub-cover-image, which produces a real
  # cover document. Leaving the image in the title page as well would package
  # the same 2.6 MB file twice and show the artwork twice on opening.
  if [[ "${1:-}" == "--no-cover" ]]; then
    grep -v '^!\[' "$dest" > "$dest.stripped" && mv "$dest.stripped" "$dest"
  fi
  printf '%s' "$dest"
}

# Renders the title page for a single volume, given that volume's title, and
# prints the path to the rendered copy. Each volume edition opens with its
# own title page; chapters of that volume link up to it.
volume_title_page_for() {
  local vol_title="$1" dest="$link_tmp/volume-title-page.md"
  python3 "$repo_root/scripts/bash/lib/render_template.py" \
    publishing/volume-title-page.md \
    "VOLUME_TITLE=$vol_title" \
    "CREATED_DATE=$title_page_created" \
    "UPDATED_DATE=$title_page_updated" > "$dest"
  printf '%s' "$dest"
}

# Adds up-navigation entries to the top of a generated HTML file's table of
# contents. No-op when given no link pairs.
inject_toc_links() {
  local file="$1"
  shift
  [[ $# -eq 0 ]] && return 0
  python3 "$repo_root/scripts/bash/lib/inject_toc_links.py" "$file" "$@"
}

# Pandoc resolves an image's relative path against its own working
# directory, not against the source file's directory -- so a chapter's
# "../../../diagrams/..." reference needs each rewritten file's own
# directory on the search path. Prints a colon-joined --resource-path
# value covering every directory in $@ (deduplicated), for input files
# that may live at different depths (a volume README.md plus its
# chapters/*.md).
resource_path_for() {
  local dirs=() f d already
  for f in "$@"; do
    d="$(dirname "$f")"
    already=0
    for existing in "${dirs[@]:-}"; do
      [[ "$existing" == "$d" ]] && { already=1; break; }
    done
    [[ "$already" -eq 0 ]] && dirs+=("$d")
  done
  local IFS=:
  printf '%s' "${dirs[*]}"
}

# --- Bounding the EPUB step so a hang fails fast ------------------------------
#
# The EPUB is one long serial step at the tail of the build; an intermittent
# wedge there (observed once, most likely in the pre-Pandoc rewrite churn)
# would otherwise block the whole build forever. run_bounded caps each
# sub-step's wall-clock time and turns a hang into a clean, fast failure.
#
# It prefers coreutils `timeout`/`gtimeout` (present in CI); where neither
# exists — notably macOS's stock bash 3.2 — it falls back to a portable
# watchdog that polls the child and SIGTERMs (then SIGKILLs) it past the limit.
timeout_bin=""
if command -v timeout >/dev/null 2>&1; then
  timeout_bin="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
  timeout_bin="gtimeout"
fi

# Generous caps (seconds) — well above normal runtimes, so they only trip on a
# genuine wedge, never on a merely slow machine.
rewrite_timeout=300     # the batched link rewrite: normally well under a minute
pandoc_timeout=1800     # the whole-encyclopedia EPUB conversion: minutes
finalize_timeout=300    # the in-memory EPUB repackage: seconds

run_bounded() {
  local secs="$1"; shift
  local rc=0
  if [[ -n "$timeout_bin" ]]; then
    "$timeout_bin" -k 10 "$secs" "$@" || rc=$?
  else
    # Portable fallback for hosts without timeout/gtimeout (e.g. bash 3.2).
    "$@" &
    local cmd_pid=$!
    (
      waited=0
      while kill -0 "$cmd_pid" 2>/dev/null; do
        if [[ "$waited" -ge "$secs" ]]; then
          kill -TERM "$cmd_pid" 2>/dev/null
          sleep 10
          kill -KILL "$cmd_pid" 2>/dev/null
          break
        fi
        sleep 5
        waited=$((waited + 5))
      done
    ) &
    local watch_pid=$!
    wait "$cmd_pid" || rc=$?
    # The command has ended; stop the watchdog (it may still be mid-poll).
    kill "$watch_pid" 2>/dev/null || true
    wait "$watch_pid" 2>/dev/null || true
  fi
  case "$rc" in
    124|137|143)
      echo "build-book.sh: ERROR — step exceeded ${secs}s and was terminated (likely a hang): $*" >&2
      ;;
  esac
  return "$rc"
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
    -f markdown-implicit_figures \
    --standalone --embed-resources \
    --resource-path="$(resource_path_for "$rewritten")" \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --include-after-body="$(footer_for)" \
    --lua-filter=scripts/pandoc/open-links-new-tab.lua \
    --toc --toc-depth=2 \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "$outdir/$base.html"
  inject_toc_links "$outdir/$base.html" \
    "Volume Table of Contents|Enterprise-Infrastructure-Encyclopedia.html#TOC"
}

build_volume_html() {
  local volume_dir="$1" volume_slug title chapters ch rewritten_readme rewritten_chapters rewritten_title_page
  volume_dir="${1%/}"
  volume_slug="$(basename "$volume_dir")"
  title="$(first_line_title "$volume_dir/README.md")"
  mkdir -p "output/html/$volume_slug"
  rewritten_readme="$(rewrite_single "$volume_dir/README.md" "$volume_slug")"
  chapters=()
  while IFS= read -r f; do chapters+=("$f"); done < <(find "$volume_dir/chapters" -name "*.md" | sort)
  rewritten_chapters=()
  for ch in "${chapters[@]}"; do
    rewritten_chapters+=("$(rewrite_single_and_demote "$ch" "$volume_slug")")
  done
  rewritten_title_page="$(volume_title_page_for "$title")"
  # toc-depth 3: with chapters demoted, the volume is H1, chapters are H2, and
  # chapter sections are H3 — depth 3 keeps the section detail visible while
  # nesting chapters under their volume.
  pandoc "$rewritten_title_page" "$rewritten_readme" "${rewritten_chapters[@]}" \
    -f markdown-implicit_figures \
    --standalone --embed-resources \
    --resource-path="$(resource_path_for "$rewritten_readme" "${rewritten_chapters[@]}")" \
    --css=publishing/web.css \
    --include-before-body=publishing/theme-toggle.html \
    --include-after-body="$(footer_for)" \
    --include-after-body=publishing/toc-freeze.html \
    --lua-filter=scripts/pandoc/open-links-new-tab.lua \
    --toc --toc-depth=3 \
    --metadata "title=$title" \
    --metadata "author=$author" \
    -o "output/html/$volume_slug/Enterprise-Infrastructure-Encyclopedia.html"
}

build_series_epub() {
  local volume_dir ch rewritten_readme rewritten_body rewritten_colophon rewritten_title_page
  local manifest="$link_tmp/epub-rewrite-manifest.tsv"
  : > "$manifest"

  # Rewrite every file for the EPUB in ONE python process (lib/rewrite_batch.py)
  # rather than spawning the per-file rewrite/demote scripts ~2,600 times. The
  # loop below only records each job in the manifest and the dest path it will
  # produce; those dest paths are exactly the ones this script has always used
  # ($link_tmp/<src>, plus a .demoted.md sibling for demoted chapters), so the
  # Pandoc argument list and resource paths further down are unchanged.
  #
  # Same volume-by-volume walk as the HTML edition, for the same reason: the
  # volume READMEs carry the "Volume N" headings the table of contents needs.
  printf '%s\tepub-absolute\t\tno\n' "README.md" >> "$manifest"
  rewritten_readme="$link_tmp/README.md"
  rewritten_body=()
  for volume_dir in volumes/*/; do
    printf '%s\tepub-absolute\t\tno\n' "${volume_dir}README.md" >> "$manifest"
    rewritten_body+=("$link_tmp/${volume_dir}README.md")
    for ch in "${volume_dir}"chapters/*.md; do
      printf '%s\tepub-absolute\t\tyes\n' "$ch" >> "$manifest"
      rewritten_body+=("$link_tmp/${ch}.demoted.md")
    done
  done
  printf '%s\tepub-absolute\t\tno\n' "publishing/colophon.md" >> "$manifest"
  rewritten_colophon="$link_tmp/publishing/colophon.md"

  run_bounded "$rewrite_timeout" \
    python3 "$repo_root/scripts/bash/lib/rewrite_batch.py" "$manifest" "$link_tmp"

  rewritten_title_page="$(title_page_for --no-cover)"
  run_bounded "$pandoc_timeout" \
    pandoc "$rewritten_title_page" "$rewritten_readme" "${rewritten_body[@]}" "$rewritten_colophon" \
    -f markdown-implicit_figures \
    --epub-cover-image=publishing/cover.png \
    --toc --toc-depth=2 \
    --resource-path="$(resource_path_for "$rewritten_readme" "${rewritten_body[@]}")" \
    --css=publishing/web.css \
    --metadata "title=$series_title — Complete Edition" \
    --metadata "author=$author" \
    --metadata "identifier=$epub_identifier" \
    -o "output/epub/Enterprise-Infrastructure-Encyclopedia.epub"
  # Pandoc leaves the cover first in the spine but not in the navigation
  # metadata, so readers that consult the guide or landmarks open elsewhere.
  run_bounded "$finalize_timeout" \
    python3 "$repo_root/scripts/bash/lib/finalize_epub.py" \
    "output/epub/Enterprise-Infrastructure-Encyclopedia.epub"
}

# The EPUB edition is the encyclopedia as a single book, so it is only ever
# produced by an unscoped build. Say so rather than silently emitting nothing.
if [[ "$want_epub" -eq 1 && ( -n "$chapter" || -n "$volume" ) ]]; then
  echo "build-book.sh: note — EPUB is built only for the complete encyclopedia;" >&2
  echo "build-book.sh:        --volume/--chapter affects HTML output only." >&2
fi

if [[ -n "$chapter" ]]; then
  volume_slug="$(basename "$(dirname "$(dirname "$chapter")")")"
  echo "build-book.sh: building chapter $chapter"
  [[ "$want_html" -eq 1 ]] && build_chapter_html "$chapter" "$volume_slug"
elif [[ -n "$volume" ]]; then
  volume_dir="volumes/$volume"
  if [[ ! -d "$volume_dir" ]]; then
    echo "build-book.sh: no such volume '$volume'" >&2
    exit 1
  fi
  echo "build-book.sh: building volume $volume"
  [[ "$want_html" -eq 1 ]] && build_volume_html "$volume_dir"
else
  volume_count="$(find volumes -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  echo "build-book.sh: building all $volume_count volumes and the complete series"
  for volume_dir in volumes/*/; do
    volume_slug="$(basename "${volume_dir%/}")"
    [[ "$want_html" -eq 1 ]] && build_volume_html "$volume_dir"
    echo "build-book.sh: built $volume_slug"
  done
  [[ "$want_epub" -eq 1 ]] && build_series_epub
fi

echo "build-book.sh: done — output under output/html/ and output/epub/"
