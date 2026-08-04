#!/usr/bin/env python3
"""Demote every ATX heading in a Markdown file by one level — H1 to H2, H2 to
H3, and so on, capped at H6 — writing the result to stdout.

Used by build-book.sh when it concatenates chapters into the combined
editions (Enterprise-Infrastructure-Encyclopedia.html and the EPUB).
Each chapter file's title is a level-1 heading, the same level as its
volume README's "# Volume N" title, so in the concatenated table of contents
a chapter renders as a *sibling* of its volume rather than nesting beneath
it. Demoting the chapter's headings by one makes "Chapter N" a child of
"Volume N". Standalone per-chapter pages are built without this pass, so
their title stays H1.

Fenced code blocks are skipped. This matters: chapters are full of shell
snippets whose comment lines begin with "# ", which are not headings and
must not be demoted. The pass tracks ``` and ~~~ fences and only rewrites
heading lines outside them.

Usage: demote_headings.py <file.md>   (result on stdout)
"""
import re
import sys

FENCE = re.compile(r"^(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})(\s)")


def demote_text(text: str) -> str:
    """Demote every ATX heading in ``text`` by one level, outside code fences.

    Splitting and rejoining on ``\\n`` is lossless for the LF-only Markdown
    this project produces, so the result is byte-identical to reading the same
    text from a file and processing it line by line. Exposed as a function so
    build-book.sh can rewrite the whole EPUB body in one process (see
    rewrite_batch.py) instead of spawning this script once per chapter.
    """
    fence = None  # the fence marker that opened the current code block, or None
    out = []
    for line in text.split("\n"):
        stripped = line.lstrip()
        marker = FENCE.match(stripped)
        if marker:
            token = marker.group(1)[0] * 3
            if fence is None:
                fence = token
            elif stripped.startswith(fence):
                fence = None
            out.append(line)
            continue
        if fence is None:
            m = HEADING.match(line)
            if m and len(m.group(1)) < 6:
                line = "#" + line
        out.append(line)
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        print("usage: demote_headings.py <file.md>", file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1], encoding="utf-8") as handle:
        sys.stdout.write(demote_text(handle.read()))


if __name__ == "__main__":
    main()
