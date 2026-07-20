# Offline Website Archives

Self-contained builds of the reading and download portal — the same site
published to GitHub Pages, packaged so it runs from a local filesystem
with no server, network access, or build toolchain.

## Using an archive

Extract it and open `index.html` in a browser. Each archive expands into a
single directory named for its version:

```text
Enterprise-Infrastructure-Encyclopedia-website-vN/
├── index.html   Portal: links to every volume, the complete edition, and the EPUB
├── web.css
├── html/         Per-chapter, per-volume, and complete-series editions
└── epub/         The complete edition as EPUB 3
```

Every page is generated with Pandoc's `--embed-resources`, so diagrams are
inlined as data URIs and there are no external script, stylesheet, or image
requests. The one outbound link is the footer's "on GitHub" reference,
which simply does not resolve when offline.

## Versioning and retention

Archives are numbered sequentially (`v1`, `v2`, …). Only the three most
recent are kept here; older ones are deleted when a new archive is added.

Note that pruning this directory bounds the working tree, not the
repository history — every archive committed remains in the history of
every clone.

## Rebuilding

```bash
scripts/bash/build-book.sh --format all
scripts/bash/build-download-site.sh --output _site
```

Then stage `_site/` under a directory named for the new version, strip any
`.DS_Store` files, and zip it so it extracts into that one directory.
