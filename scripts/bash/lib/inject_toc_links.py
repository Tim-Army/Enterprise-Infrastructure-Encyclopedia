#!/usr/bin/env python3
"""Insert up-navigation entries at the top of a generated HTML file's table
of contents.

Pandoc builds its table of contents purely from the headings of the document
it is converting, so an entry pointing at a *different* document (a chapter
linking up to its volume, or a volume linking up to the complete
encyclopedia) cannot be expressed in the source Markdown. Those entries are
therefore injected here, after Pandoc has run.

Links are given target="_blank" to match scripts/pandoc/open-links-new-tab.lua,
which does the same for every cross-document link in HTML output. EPUB gets
the equivalent navigation as links on its title page instead, because an
EPUB's nav document is only permitted to reference resources inside the book.

Usage: inject_toc_links.py <file.html> "Label|href" ["Label|href" ...]
"""
import html
import sys

TOC_OPEN = '<nav id="TOC" role="doc-toc">\n<ul>\n'


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

    items = []
    for pair in pairs:
        if "|" not in pair:
            print(f"inject_toc_links.py: expected 'Label|href', got {pair!r}",
                  file=sys.stderr)
            sys.exit(2)
        label, href = pair.split("|", 1)
        items.append(
            '<li><a href="{}" target="_blank" rel="noopener noreferrer">'
            "{}</a></li>\n".format(
                html.escape(href, quote=True), html.escape(label)
            )
        )

    at = start + len(TOC_OPEN)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(doc[:at] + "".join(items) + doc[at:])


if __name__ == "__main__":
    main()
