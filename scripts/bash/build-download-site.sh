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

# macOS Finder/Spotlight recreate .DS_Store files asynchronously, which can
# make a plain `rm -rf` race and abort under `set -e` with "Directory not
# empty". Strip them from the sources we are about to copy, then retry the
# removal of any prior portal directory so the build is deterministic.
find output publishing -name '.DS_Store' -type f -delete 2>/dev/null || true
for _ in 1 2 3 4 5; do
  if [[ -e "$output" ]]; then
    find "$output" -name '.DS_Store' -type f -delete 2>/dev/null || true
  fi
  rm -rf "$output" 2>/dev/null && break
  sleep 1
done
mkdir -p "$output"
cp publishing/web.css "$output/web.css"
cp -R output/html "$output/html"
cp -R output/epub "$output/epub"

# Whole-volume Word and PDF copies, written by build-book.sh for the volumes
# it lists in download_volumes. Published at downloads/<volume>/<volume>.docx
# and .pdf, linked from the volume's README and its portal index page.
if [[ -d output/downloads ]]; then
  cp -R output/downloads "$output/downloads"
fi

# Lab automation scripts. A volume that keeps a lab-scripts folder gets it
# published as plain files plus one zip at
# downloads/<volume>/lab-scripts/ and downloads/<volume>/<volume>-lab-scripts.zip.
# The folder of the Lab Selector (the one with common/lab-catalog.json) also gets
# the lab diagram of the shared lab as diagrams/lab-topology.svg, with a PNG copy
# when rsvg-convert is installed, and the lab chapters that the catalog names as
# walkthroughs/<short name>, so the Lab Selector can put them in its zip.
# scripts/python/sync_lab_selector.py --package-args lists those files.
# set_links holds one line for each lab set of the Lab Selector (the folder of its
# volume, its id, and its name), for the links on the portal pages of those volumes.
set_links=""
for scripts_dir in volumes/*/lab-scripts; do
  [[ -d "$scripts_dir" ]] || continue
  # A folder with no file in it is skipped: git does not track an empty folder.
  [[ -n "$(find "$scripts_dir" -type f -print -quit)" ]] || continue
  vol="$(basename "$(dirname "$scripts_dir")")"
  mkdir -p "$output/downloads/$vol"
  extra_args=()
  if [[ -f "$scripts_dir/common/lab-catalog.json" ]]; then
    package_args="$(python3 scripts/python/sync_lab_selector.py --package-args)"
    while IFS= read -r spec; do
      spec="${spec%$'\r'}"
      [[ -z "$spec" ]] && continue
      extra_args+=(--add "$spec")
    done <<< "$package_args"
    set_links="$(python3 scripts/python/sync_lab_selector.py --set-links)"
  else
    topology="diagrams/$vol/chapter-999-shared-lab-topology.svg"
    if [[ -f "$topology" ]]; then
      extra_args+=(--add "$topology=diagrams/lab-topology.svg")
    fi
  fi
  python3 scripts/python/package_lab_scripts.py "$scripts_dir" "$output/downloads/$vol" "$vol-lab-scripts.zip" ${extra_args[@]+"${extra_args[@]}"}
done

# The Lab Selector was the Lab Builder of volume 201 until 2026-11-20. A page at
# the old address sends a reader on to the new one.
selector_page="downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html"
if [[ -f "$output/$selector_page" ]]; then
  old_dir="$output/downloads/volume-201-fortiswitch-stig-and-srg-mapping/lab-scripts/builder"
  mkdir -p "$old_dir"
  cat > "$old_dir/lab-builder.html" <<HTML
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta http-equiv="refresh" content="0; url=../../../volume-901-lab-selector/lab-scripts/selector/lab-selector.html" />
<title>Lab Selector</title>
</head>
<body>
<p>The Lab Builder is now the <a href="../../../volume-901-lab-selector/lab-scripts/selector/lab-selector.html">Lab Selector</a>, in Volume CMI.</p>
</body>
</html>
HTML
fi

# Self-contained interactive companion pages (searchable/sortable catalogs
# and the like). These are hand-authored, fully offline HTML — served as-is
# alongside the Pandoc output and linked from the portal and their volume.
if [[ -d publishing/interactive ]]; then
  cp -R publishing/interactive "$output/interactive"
fi

# Downloadable data files (CSV exports of chapter tables, written by
# scripts/python/export_srg_tables.py). Chapters link to them at
# data/<volume>/<file>.csv on the portal.
for data_dir in volumes/*/data; do
  [[ -d "$data_dir" ]] || continue
  vol="$(basename "$(dirname "$data_dir")")"
  mkdir -p "$output/data/$vol"
  cp "$data_dir"/*.csv "$output/data/$vol/"
done

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
  echo "<p>The whole encyclopedia in one file is published as an EPUB. Read online by volume or chapter below.</p>"
  echo "<ul>"
  echo "<li><a href=\"epub/Enterprise-Infrastructure-Encyclopedia.epub\">Download (EPUB)</a></li>"
  echo "</ul>"
  if [[ -f "$output/interactive/cisco-u-learning-paths.html" ]]; then
    echo "<h2>Interactive companions</h2>"
    echo "<ul>"
    echo "<li><a href=\"interactive/cisco-u-learning-paths.html\">Cisco U. Learning Paths &mdash; searchable CE-credit &amp; access catalog</a> (companion to <a href=\"html/volume-997-master-appendices/Enterprise-Infrastructure-Encyclopedia.html#c01\">Master Appendices, Chapter 01</a>)</li>"
    if [[ -f "$output/interactive/fortigate-operator-quiz.html" ]]; then
      echo "<li><a href=\"interactive/fortigate-operator-quiz.html\">FortiGate 7.6 Operator Practice Exam &mdash; interactive self-check</a> (companion to <a href=\"html/volume-019-fortinet-network-security/Enterprise-Infrastructure-Encyclopedia.html#c16\">Fortinet NSE, Chapter 16</a>)</li>"
    fi
    if [[ -f "$output/interactive/fortigate-administrator-quiz.html" ]]; then
      echo "<li><a href=\"interactive/fortigate-administrator-quiz.html\">FortiGate 7.6 Administrator (NSE 4) Study Quiz &mdash; interactive self-check</a> (companion to <a href=\"html/volume-019-fortinet-network-security/Enterprise-Infrastructure-Encyclopedia.html#c16\">Fortinet NSE, Chapter 16</a>)</li>"
    fi
    if [[ -f "$output/$selector_page" ]]; then
      echo "<li><a href=\"$selector_page\">Lab Selector &mdash; choose certification, learning, or SRG labs and get the build for them</a> (companion to <a href=\"html/volume-901-lab-selector/Enterprise-Infrastructure-Encyclopedia.html\">Lab Selector, Volume CMI</a>)</li>"
    fi
    if [[ -f "$output/interactive/fortiswitch-srg-crosswalk.html" ]]; then
      echo "<li><a href=\"interactive/fortiswitch-srg-crosswalk.html\">FortiSwitch SRG Crosswalk &mdash; searchable, sortable table with CSV downloads</a> (companion to <a href=\"html/volume-201-fortiswitch-stig-and-srg-mapping/Enterprise-Infrastructure-Encyclopedia.html\">FortiSwitch STIG and SRG Mapping, Volume CCI</a>)</li>"
    fi
    echo "</ul>"
  fi
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
    echo "<li><a href=\"Enterprise-Infrastructure-Encyclopedia.html\">Read online (HTML)</a></li>"
    echo "<li><a href=\"../../epub/Enterprise-Infrastructure-Encyclopedia.epub\">Download the complete encyclopedia (EPUB)</a></li>"
    if [[ -f "$output/downloads/$slug/$slug.docx" ]]; then
      echo "<li><a href=\"../../downloads/$slug/$slug.docx\">Download this volume (Word, .docx)</a></li>"
    fi
    if [[ -f "$output/downloads/$slug/$slug.pdf" ]]; then
      echo "<li><a href=\"../../downloads/$slug/$slug.pdf\">Download this volume (PDF)</a></li>"
    fi
    if [[ -f "$output/downloads/$slug/$slug-lab-scripts.zip" ]]; then
      echo "<li><a href=\"../../downloads/$slug/$slug-lab-scripts.zip\">Download the lab automation scripts (.zip)</a></li>"
    fi
    if [[ -f "$output/downloads/$slug/lab-scripts/selector/lab-selector.html" ]]; then
      echo "<li><a href=\"../../downloads/$slug/lab-scripts/selector/lab-selector.html\">Lab Selector: choose the labs, a platform, and options, and get the manifest, the commands, the checklist, and the walkthroughs</a></li>"
    fi
    # A volume whose labs the Lab Selector offers gets a link that opens the page with those labs ticked.
    if [[ -n "$set_links" && -f "$output/$selector_page" ]]; then
      while IFS=$'\t' read -r set_volume set_id set_name; do
        set_name="${set_name%$'\r'}"
        [[ "$set_volume" == "$slug" ]] || continue
        echo "<li><a href=\"../../$selector_page?sets=$set_id\">Lab Selector: plan a lab build for the $set_name labs of this volume</a></li>"
      done <<< "$set_links"
    fi
    echo "</ul>"
    echo "<h2>Chapters</h2>"
    echo "<ul>"
    for chapter in "$volume_dir"chapters/*.md; do
      base="$(basename "$chapter" .md)"
      num="${base%%-*}"
      chtitle="$(head -1 "$chapter" | sed -E 's/^# //')"
      echo "<li><a href=\"Enterprise-Infrastructure-Encyclopedia.html#c$num\">$chtitle</a></li>"
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
    # A link can carry choices for its page after a question mark. The file is what has to exist.
    target="${target%%\?*}"
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

# Final sweep: no .DS_Store may reach the portal (and thus the offline zip).
find "$output" -name '.DS_Store' -type f -delete 2>/dev/null || true

echo "build-download-site.sh: wrote portal to $output/ (all catalog links verified)"
