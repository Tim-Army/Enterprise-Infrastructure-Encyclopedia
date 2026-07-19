#!/usr/bin/env python3
"""Rewrite links into working links in generated editions.

Two independent link classes are rewritten:

1. Links resolving to volumes/<slug>/chapters/<file>.md — the dominant
   case (chapter-to-chapter cross-references).
2. Links resolving to publishing/web.css or publishing/theme-toggle.html
   — these files are never copied into output/ as standalone files
   (Pandoc embeds their content directly via --embed-resources /
   --include-before-body), so a relative link to them has nothing local
   to point at. They're rewritten to the GitHub source instead.

Everything else (links to other root docs, volume/root README/INDEX/
GLOSSARY, external URLs) is left exactly as written in the source, since
those targets have no corresponding file in the generated output either
and there's no single sensible fallback for all of them the way there is
for these two specific, known asset paths.

Usage:
    rewrite_chapter_links.py <source-file> <mode> [<current-volume-slug>]

    mode:
      html-flat <current-volume-slug>
          Rewrite for a document that will live in output/html/<slug>/
          (a single chapter's own page, or that volume's combined page).
          Same-volume chapter links become a bare "NN-slug.html"; links
          to another volume's chapter become "../other-slug/NN-slug.html".

      html-root
          Rewrite for the complete-series document at output/html/. Every
          chapter link becomes "volume-slug/NN-slug.html".

      epub-absolute
          Rewrite for any EPUB build. A relative path inside an EPUB
          cannot address a separate output/html/ file, so links become
          absolute URLs at the deployed Pages portal.

    publishing/web.css and publishing/theme-toggle.html links are
    rewritten to the GitHub source the same way in every mode, since none
    of the three output contexts has a local copy of those files to
    point at instead.

Prints the transformed content to stdout.
"""
import os
import re
import sys

PORTAL_BASE_URL = "https://derg20.github.io/Enterprise-Infrastructure-Encyclopedia"
GITHUB_BLOB_BASE = "https://github.com/derg20/Enterprise-Infrastructure-Encyclopedia/blob/main"

LINK_RE = re.compile(r"\]\(([^)\s]+\.(?:md|css|html))((?:#[^)]*)?)\)")
CHAPTER_RE = re.compile(r"^volumes/([^/]+)/chapters/([^/]+)\.md$")
PUBLISHING_ASSETS = {"publishing/web.css", "publishing/theme-toggle.html"}


def resolve_chapter_target(source_file: str, target_path: str):
    source_dir = os.path.dirname(source_file)
    resolved = os.path.normpath(os.path.join(source_dir, target_path))
    match = CHAPTER_RE.match(resolved)
    if not match:
        return None
    return match.group(1), match.group(2)


def resolve_publishing_asset(source_file: str, target_path: str):
    source_dir = os.path.dirname(source_file)
    resolved = os.path.normpath(os.path.join(source_dir, target_path))
    return resolved if resolved in PUBLISHING_ASSETS else None


def rewrite(content: str, source_file: str, mode: str, current_volume: str) -> str:
    def replace(m: "re.Match[str]") -> str:
        target_path, fragment = m.group(1), m.group(2)

        asset = resolve_publishing_asset(source_file, target_path)
        if asset is not None:
            return f"]({GITHUB_BLOB_BASE}/{asset}{fragment})"

        target = resolve_chapter_target(source_file, target_path)
        if target is None:
            return m.group(0)
        target_volume, target_chapter = target

        if mode == "html-flat":
            if target_volume == current_volume:
                new_target = f"{target_chapter}.html"
            else:
                new_target = f"../{target_volume}/{target_chapter}.html"
        elif mode == "html-root":
            new_target = f"{target_volume}/{target_chapter}.html"
        elif mode == "epub-absolute":
            new_target = f"{PORTAL_BASE_URL}/html/{target_volume}/{target_chapter}.html"
        else:
            raise ValueError(f"unknown mode: {mode}")

        return f"]({new_target}{fragment})"

    return LINK_RE.sub(replace, content)


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    source_file = sys.argv[1]
    mode = sys.argv[2]
    current_volume = sys.argv[3] if len(sys.argv) > 3 else ""

    with open(source_file, encoding="utf-8") as fh:
        content = fh.read()

    sys.stdout.write(rewrite(content, source_file, mode, current_volume))


if __name__ == "__main__":
    main()
