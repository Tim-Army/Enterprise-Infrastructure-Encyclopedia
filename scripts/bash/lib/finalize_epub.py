#!/usr/bin/env python3
"""Make a Pandoc-built EPUB open on its cover.

Pandoc puts the cover first in the spine, which is enough for readers that
simply start at the beginning. Readers that instead consult the navigation
metadata do not land there, because Pandoc emits:

  * a <guide> whose first entry is the table of contents, and which carries
    no `text` reference -- the EPUB 2 marker for "start reading here"; and
  * a landmarks nav that lists `titlepage` ahead of `cover`, with no
    `bodymatter` entry.

This rewrites both so the cover is the declared starting point: the guide
gains a `text` reference pointing at the cover and lists the cover first,
and the landmarks nav is reordered to lead with the cover.

It also adds a "Table of Contents" entry at the head of the table of
contents itself. Pandoc's nav lists only the body matter, so the nav
document -- which sits in the spine and is a readable page -- is the one
page in the book with no way to reach it from the contents. Readers that
render the nav as a panel rather than a page gain nothing from the entry
but are not harmed by it; readers that page through the spine get a way
back.

The archive is rebuilt rather than patched in place, because an EPUB
requires `mimetype` to be the first entry and stored uncompressed; a naive
rewrite loses that and produces a file some readers reject.

Usage: finalize_epub.py <book.epub>
"""
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

COVER_HREF = "text/cover.xhtml"
NAV_HREF = "nav.xhtml"
NAV_TITLE = "Table of Contents"
NAV_ITEM = f'<li id="toc-li-contents"><a href="{NAV_HREF}">{NAV_TITLE}</a></li>'


def fix_opf(xml: str) -> str:
    """Lead the guide with the cover and declare it the start of reading."""
    match = re.search(r"<guide>(.*?)</guide>", xml, re.S)
    if not match:
        return xml

    body = match.group(1)
    refs = re.findall(r"<reference\b[^>]*/>", body)
    cover_ref = next((r for r in refs if 'type="cover"' in r), None)
    if cover_ref is None:
        return xml

    others = [r for r in refs if r is not cover_ref and 'type="text"' not in r]
    text_ref = f'<reference type="text" title="Cover" href="{COVER_HREF}" />'
    rebuilt = "\n    ".join([cover_ref, text_ref] + others)
    return xml[: match.start()] + f"<guide>\n    {rebuilt}\n  </guide>" + xml[match.end():]


def fix_nav(xml: str) -> str:
    """Reorder the landmarks nav so the cover is listed first."""
    match = re.search(
        r'(<nav[^>]*epub:type="landmarks".*?<ol>)(.*?)(</ol>)', xml, re.S
    )
    if not match:
        return xml

    items = re.findall(r"<li>.*?</li>", match.group(2), re.S)
    cover = [i for i in items if 'epub:type="cover"' in i]
    if not cover:
        return xml

    rest = [i for i in items if i not in cover]
    inner = "\n    " + "\n    ".join(cover + rest) + "\n  "
    return xml[: match.start(2)] + inner + xml[match.end(2):]


def add_contents_entry(xml: str) -> str:
    """Add a self-referencing entry at the head of the table of contents."""
    if NAV_ITEM in xml:
        return xml

    match = re.search(r'<nav[^>]*epub:type="toc".*?<ol[^>]*>', xml, re.S)
    if not match:
        return xml

    return xml[: match.end()] + NAV_ITEM + xml[match.end():]


def main():
    if len(sys.argv) != 2:
        print("usage: finalize_epub.py <book.epub>", file=sys.stderr)
        sys.exit(2)

    src = Path(sys.argv[1])
    with zipfile.ZipFile(src) as book:
        names = book.namelist()
        entries = {name: book.read(name) for name in names}

    opf = next((n for n in names if n.endswith(".opf")), None)
    nav = next((n for n in names if n.endswith("nav.xhtml")), None)
    if opf is None:
        print(f"finalize_epub.py: no .opf found in {src}", file=sys.stderr)
        sys.exit(1)

    entries[opf] = fix_opf(entries[opf].decode("utf-8")).encode("utf-8")
    if nav:
        text = fix_nav(entries[nav].decode("utf-8"))
        entries[nav] = add_contents_entry(text).encode("utf-8")

    tmp = Path(tempfile.mkstemp(suffix=".epub")[1])
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        # mimetype must come first and be stored, not deflated.
        if "mimetype" in entries:
            out.writestr(
                zipfile.ZipInfo("mimetype"), entries["mimetype"], zipfile.ZIP_STORED
            )
        for name in names:
            if name != "mimetype":
                out.writestr(name, entries[name])

    shutil.move(str(tmp), str(src))


if __name__ == "__main__":
    main()
