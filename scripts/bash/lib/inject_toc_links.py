#!/usr/bin/env python3
"""Insert up-navigation entries at the top of a generated HTML file's table
of contents, nesting the document's own entries beneath them.

Pandoc builds its table of contents purely from the headings of the document
it is converting, so an entry pointing at a *different* document (a chapter
linking up to its volume, or a volume linking up to the complete
encyclopedia) cannot be expressed in the source Markdown. Those entries are
therefore injected here, after Pandoc has run.

The injected entries are ancestors of the document, not siblings of its
headings, so the last one adopts everything Pandoc produced as its children.
A chapter page reads:

    Encyclopedia Table of Contents
    Volume Table of Contents
        Chapter 02: ...
            Learning Objectives
            Theory and Architecture

rather than placing the encyclopedia, the volume, and the chapter at one
flat level, which gave no sense of where the page sat in the series.

Links are given target="_blank" to match scripts/pandoc/open-links-new-tab.lua,
which does the same for every cross-document link in HTML output. EPUB gets
the equivalent navigation as links on its title page instead, because an
EPUB's nav document is only permitted to reference resources inside the book.

Usage: inject_toc_links.py <file.html> "Label|href" ["Label|href" ...]
"""
import html
import sys

TOC_OPEN = '<nav id="TOC" role="doc-toc">\n<ul>\n'
NAV_CLOSE = "</nav>"


def anchor(label, href):
    return '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>'.format(
        html.escape(href, quote=True), html.escape(label)
    )


def main():
    if len(sys.argv) < 3:
        print("usage: inject_toc_links.py <file.html> 'Label|href' ...",
              file=sys.stderr)
        sys.exit(2)

    path, pairs = sys.argv[1], sys.argv[2:]
    with open(path, encoding="utf-8") as handle:
        doc = handle.read()

    start = doc.find(TOC_OPEN)
    if start < 0:
        print(f"inject_toc_links.py: no table of contents found in {path}",
              file=sys.stderr)
        sys.exit(1)

    body_start = start + len(TOC_OPEN)

    # The outer <ul> is the last one closed before </nav>; nested lists close
    # earlier. Finding it this way avoids having to parse the nesting.
    nav_end = doc.find(NAV_CLOSE, body_start)
    if nav_end < 0:
        print(f"inject_toc_links.py: table of contents unterminated in {path}",
              file=sys.stderr)
        sys.exit(1)
    outer_close = doc.rfind("</ul>", body_start, nav_end)
    if outer_close < 0:
        print(f"inject_toc_links.py: no closing </ul> found in {path}",
              file=sys.stderr)
        sys.exit(1)

    own_entries = doc[body_start:outer_close]

    parsed = []
    for pair in pairs:
        if "|" not in pair:
            print(f"inject_toc_links.py: expected 'Label|href', got {pair!r}",
                  file=sys.stderr)
            sys.exit(2)
        label, href = pair.split("|", 1)
        parsed.append((label, href))

    # Every entry but the last is a plain sibling; the last one adopts the
    # document's own entries as its children.
    out = []
    for label, href in parsed[:-1]:
        out.append("<li>{}</li>\n".format(anchor(label, href)))

    last_label, last_href = parsed[-1]
    if own_entries.strip():
        out.append("<li>{}\n<ul>\n{}</ul>\n</li>\n".format(
            anchor(last_label, last_href), own_entries))
    else:
        out.append("<li>{}</li>\n".format(anchor(last_label, last_href)))

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(doc[:body_start] + "".join(out) + doc[outer_close:])


if __name__ == "__main__":
    main()
