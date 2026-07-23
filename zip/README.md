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

## Version log

Every archive this directory has held, with the local time of the commit
that created it and, once pruned under the retention rule above, the commit
that removed it. The three still present are marked *current*. Each file is
named `Enterprise-Infrastructure-Encyclopedia-website-vN.zip`.

| Version | Created | Deleted |
| --- | --- | --- |
| v1 | 2026-07-20 13:12 | 2026-07-20 19:08 |
| v2 | 2026-07-20 18:43 | 2026-07-20 19:15 |
| v3 | 2026-07-20 18:49 | 2026-07-20 20:15 |
| v4 | 2026-07-20 19:08 | 2026-07-20 20:22 |
| v5 | 2026-07-20 19:15 | 2026-07-20 20:47 |
| v6 | 2026-07-20 20:15 | 2026-07-20 20:59 |
| v7 | 2026-07-20 20:22 | 2026-07-20 21:05 |
| v8 | 2026-07-20 20:47 | 2026-07-20 21:14 |
| v9 | 2026-07-20 20:59 | 2026-07-20 21:26 |
| v10 | 2026-07-20 21:05 | 2026-07-20 21:34 |
| v11 | 2026-07-20 21:14 | 2026-07-20 21:43 |
| v12 | 2026-07-20 21:26 | 2026-07-20 21:52 |
| v13 | 2026-07-20 21:34 | 2026-07-20 22:19 |
| v14 | 2026-07-20 21:43 | 2026-07-20 22:28 |
| v15 | 2026-07-20 21:52 | 2026-07-20 22:37 |
| v16 | 2026-07-20 22:19 | 2026-07-20 22:53 |
| v17 | 2026-07-20 22:28 | 2026-07-20 23:16 |
| v18 | 2026-07-20 22:37 | 2026-07-20 23:16 |
| v19 | 2026-07-20 22:53 | 2026-07-20 23:30 |
| v20 | 2026-07-20 23:16 | 2026-07-20 23:38 |
| v21 | 2026-07-20 23:16 | 2026-07-20 23:50 |
| v22 | 2026-07-20 23:30 | 2026-07-21 00:08 |
| v23 | 2026-07-20 23:38 | 2026-07-21 01:05 |
| v24 | 2026-07-20 23:50 | 2026-07-21 07:52 |
| v25 | 2026-07-21 00:08 | 2026-07-21 08:06 |
| v26 | 2026-07-21 01:05 | 2026-07-21 08:18 |
| v27 | 2026-07-21 07:52 | 2026-07-21 08:31 |
| v28 | 2026-07-21 08:06 | 2026-07-21 13:25 |
| v29 | 2026-07-21 08:18 | 2026-07-21 13:39 |
| v30 | 2026-07-21 08:31 | 2026-07-21 14:08 |
| v31 | 2026-07-21 13:25 | 2026-07-21 14:27 |
| v32 | 2026-07-21 13:39 | 2026-07-21 14:37 |
| v33 | 2026-07-21 14:08 | 2026-07-21 15:21 |
| v34 | 2026-07-21 14:27 | 2026-07-21 16:08 |
| v35 | 2026-07-21 14:37 | 2026-07-21 16:23 |
| v36 | 2026-07-21 15:21 | 2026-07-21 17:14 |
| v37 | 2026-07-21 16:08 | 2026-07-21 17:42 |
| v38 | 2026-07-21 16:23 | 2026-07-21 19:01 |
| v39 | 2026-07-21 17:14 | 2026-07-21 19:53 |
| v40 | 2026-07-21 17:42 | 2026-07-21 21:24 |
| v41 | 2026-07-21 19:01 | 2026-07-21 22:39 |
| v42 | 2026-07-21 19:53 | 2026-07-21 23:04 |
| v43 | 2026-07-21 21:24 | 2026-07-21 23:19 |
| v44 | 2026-07-21 22:39 | 2026-07-21 23:29 |
| v45 | 2026-07-21 23:04 | 2026-07-21 23:57 |
| v46 | 2026-07-21 23:19 | 2026-07-22 00:20 |
| v47 | 2026-07-21 23:29 | 2026-07-22 00:48 |
| v48 | 2026-07-21 23:57 | 2026-07-22 05:20 |
| v49 | 2026-07-22 00:20 | 2026-07-22 05:55 |
| v50 | 2026-07-22 00:48 | 2026-07-22 06:30 |
| v51 | 2026-07-22 05:20 | 2026-07-22 07:07 |
| v52 | 2026-07-22 05:55 | 2026-07-22 07:39 |
| v53 | 2026-07-22 06:30 | 2026-07-22 08:03 |
| v54 | 2026-07-22 07:07 | 2026-07-22 08:47 |
| v55 | 2026-07-22 07:39 | 2026-07-22 09:02 |
| v56 | 2026-07-22 08:03 | 2026-07-22 13:58 |
| v57 | 2026-07-22 08:47 | 2026-07-22 15:04 |
| v58 | 2026-07-22 09:02 | 2026-07-22 15:37 |
| v59 | 2026-07-22 13:58 | 2026-07-22 16:13 |
| v60 | 2026-07-22 15:04 | 2026-07-22 16:47 |
| v61 | 2026-07-22 15:37 | 2026-07-22 17:06 |
| v62 | 2026-07-22 16:13 | 2026-07-22 17:23 |
| v63 | 2026-07-22 16:47 | 2026-07-22 17:50 |
| v64 | 2026-07-22 17:06 | 2026-07-22 18:16 |
| v65 | 2026-07-22 17:23 | 2026-07-22 18:36 |
| v66 | 2026-07-22 17:50 | 2026-07-22 19:19 |
| v67 | 2026-07-22 18:16 | 2026-07-22 19:32 |
| v68 | 2026-07-22 18:36 | 2026-07-22 20:24 |
| v69 | 2026-07-22 19:19 | 2026-07-22 20:41 |
| v70 | 2026-07-22 19:32 | *current* |
| v71 | 2026-07-22 20:24 | *current* |
| v72 | 2026-07-22 20:41 | *current* |

## Rebuilding

```bash
scripts/bash/build-book.sh --format all
scripts/bash/build-download-site.sh --output _site
```

Then stage `_site/` under a directory named for the new version, strip any
`.DS_Store` files, and zip it so it extracts into that one directory.
