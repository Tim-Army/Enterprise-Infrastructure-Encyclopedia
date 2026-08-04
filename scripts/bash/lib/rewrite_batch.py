#!/usr/bin/env python3
"""Rewrite (and optionally demote) many files in a SINGLE process.

build-book.sh's EPUB build used to rewrite every volume README and chapter by
spawning rewrite_chapter_links.py and demote_headings.py once per file — on
the order of 2,600 short-lived Python processes for the whole encyclopedia.
That serial fork/exec churn cost ~50 s of interpreter startup and was the
most likely trigger of an intermittent hang in the EPUB step. This does the
whole batch in one interpreter, reusing the exact same rewrite/demote logic so
the output is identical.

Usage: rewrite_batch.py <manifest.tsv> <dest-root>

Each manifest line is tab-separated: ``<src>\\t<mode>\\t<current-volume>\\t<demote>``
  src             path to the source file (relative to the current directory)
  mode            html-flat | html-root | epub-absolute
  current-volume  volume slug for html-flat (empty otherwise)
  demote          "yes" to demote headings (chapters in combined editions), else "no"

For each job the rewritten content is written to ``<dest-root>/<src>``; when
demote is "yes" the demoted result is additionally written to
``<dest-root>/<src>.demoted.md`` — the same destination paths build-book.sh has
always used, so the pandoc argument list and resource paths are unchanged.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rewrite_chapter_links import rewrite  # noqa: E402
from demote_headings import demote_text  # noqa: E402


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: rewrite_batch.py <manifest.tsv> <dest-root>", file=sys.stderr)
        sys.exit(2)

    manifest_path, dest_root = sys.argv[1], sys.argv[2]

    with open(manifest_path, encoding="utf-8") as manifest:
        for lineno, raw in enumerate(manifest, 1):
            line = raw.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 4:
                print(
                    f"rewrite_batch.py: malformed manifest line {lineno}: {line!r}",
                    file=sys.stderr,
                )
                sys.exit(1)
            src, mode, current_volume, demote_flag = parts

            with open(src, encoding="utf-8") as source:
                content = source.read()
            rewritten = rewrite(content, src, mode, current_volume)

            dest = os.path.join(dest_root, src)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as out:
                out.write(rewritten)

            if demote_flag == "yes":
                with open(dest + ".demoted.md", "w", encoding="utf-8") as out:
                    out.write(demote_text(rewritten))


if __name__ == "__main__":
    main()
