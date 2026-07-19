#!/usr/bin/env python3
"""Rewrite links to chapter .md files into working links in generated
editions.

Only links resolving to volumes/<slug>/chapters/<file>.md are touched;
everything else (links to root docs, volume/root README/INDEX/GLOSSARY,
external URLs) is left exactly as written in the source, since those
targets have no corresponding file in the generated output.

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

Prints the transformed content to stdout.
"""
import os
import re
import sys

PORTAL_BASE_URL = "https://derg20.github.io/Enterprise-Infrastructure-Encyclopedia"

LINK_RE = re.compile(r"\]\(([^)\s]+\.md)((?:#[^)]*)?)\)")
CHAPTER_RE = re.compile(r"^volumes/([^/]+)/chapters/([^/]+)\.md$")


def resolve_chapter_target(source_file: str, target_path: str):
    source_dir = os.path.dirname(source_file)
    resolved = os.path.normpath(os.path.join(source_dir, target_path))
    match = CHAPTER_RE.match(resolved)
    if not match:
        return None
    return match.group(1), match.group(2)


def rewrite(content: str, source_file: str, mode: str, current_volume: str) -> str:
    def replace(m: "re.Match[str]") -> str:
        target_path, fragment = m.group(1), m.group(2)
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
