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
from typing import Optional

COVER_HREF = "text/cover.xhtml"

# The contents entry cannot point at nav.xhtml. Readers consume the document
# carrying properties="nav" to build their own contents UI and never render
# it as a page, so a link to it lands nowhere -- in Apple Books the row is
# simply dead. The entry therefore points at an ordinary content document
# generated here, holding the same list.
#
# contents.xhtml sits beside nav.xhtml at the EPUB root rather than under
# text/, so every href copied out of the nav (text/chNNN.xhtml#...) and the
# stylesheet path resolve unchanged.
CONTENTS_ID = "contents_xhtml"
CONTENTS_HREF = "contents.xhtml"
CONTENTS_TITLE = "Table of Contents"
CONTENTS_ITEM = (
    f'<li id="toc-li-contents"><a href="{CONTENTS_HREF}">{CONTENTS_TITLE}</a></li>'
)
CONTENTS_DOC = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en-US" xml:lang="en-US">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <link rel="stylesheet" type="text/css" href="styles/stylesheet1.css" />
</head>
<body epub:type="frontmatter">
<section id="contents">
{body}
</section>
</body>
</html>
"""


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


def build_contents_doc(nav_xml: str) -> Optional[str]:
    """Render the nav's contents list as an ordinary, readable page."""
    match = re.search(r'<nav[^>]*epub:type="toc"[^>]*>(.*?)</nav>', nav_xml, re.S)
    if not match:
        return None
    return CONTENTS_DOC.format(title=CONTENTS_TITLE, body=match.group(1))


def add_contents_entry(xml: str) -> str:
    """Add an entry for the contents page at the head of the contents."""
    if CONTENTS_ITEM in xml:
        return xml

    match = re.search(r'<nav[^>]*epub:type="toc".*?<ol[^>]*>', xml, re.S)
    if not match:
        return xml

    return xml[: match.end()] + CONTENTS_ITEM + xml[match.end():]


def register_contents(xml: str) -> str:
    """Declare the contents page in the manifest and place it in the spine."""
    if f'id="{CONTENTS_ID}"' in xml:
        return xml

    item = (
        f'<item id="{CONTENTS_ID}" href="{CONTENTS_HREF}" '
        'media-type="application/xhtml+xml" />'
    )
    xml = xml.replace("</manifest>", f"  {item}\n  </manifest>", 1)

    # Sit ahead of nav.xhtml so a reader paging through the spine meets the
    # readable contents first; fall back to the head of the spine.
    itemref = f'<itemref idref="{CONTENTS_ID}" />'
    nav_ref = re.search(r'<itemref[^>]*idref="nav"[^>]*/>', xml)
    if nav_ref:
        return xml[: nav_ref.start()] + itemref + "\n    " + xml[nav_ref.start():]
    spine = re.search(r"<spine[^>]*>", xml)
    return xml[: spine.end()] + f"\n    {itemref}" + xml[spine.end():]


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
        # Build the readable page from the nav before the entry pointing at
        # that page is inserted, so the page does not list itself.
        contents = build_contents_doc(text)
        entries[nav] = add_contents_entry(text).encode("utf-8")

        if contents:
            root = nav[: -len("nav.xhtml")]
            name = f"{root}{CONTENTS_HREF}"
            if name not in entries:
                names.append(name)
            entries[name] = contents.encode("utf-8")
            entries[opf] = register_contents(
                entries[opf].decode("utf-8")
            ).encode("utf-8")

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
