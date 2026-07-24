# Offline Website Archives

Self-contained builds of the reading and download portal — the same site
published to GitHub Pages, packaged so it runs from a local filesystem
with no server, network access, or build toolchain.

## Using an archive

Extract it and open `index.html` in a browser. Each archive expands into a
single directory named for its version:

```text
Enterprise-Infrastructure-Encyclopedia-v1.0.1/
├── index.html    Portal: links to every volume and the EPUB
├── web.css
├── html/         Per-chapter and per-volume editions
├── interactive/  Self-contained interactive companions
└── epub/         The complete edition as EPUB 3
```

Every page is generated with Pandoc's `--embed-resources`, so diagrams are
inlined as data URIs and there are no external script, stylesheet, or image
requests. The one outbound link is the footer's "on GitHub" reference,
which simply does not resolve when offline.

## Versioning and retention

Each archive is named for a **release version** —
`Enterprise-Infrastructure-Encyclopedia-v1.0.1.zip` — matching a GitHub
release tag and its EPUB asset (`Enterprise-Infrastructure-Encyclopedia-v1.0.1.epub`).
Its internal top-level folder matches the filename.

Every build is a release: each content change bumps the **patch** version
(`v1.0.0` → `v1.0.1` → `v1.0.2`, …) and is tagged so a matching GitHub
release exists; larger version bumps (minor, major) are made deliberately.
**Only the three most recent builds are kept here**; older ones are deleted
when a new build is added, giving a short rolling history of recent
releases.

Note that pruning this directory bounds the working tree, not the
repository history — every archive committed remains in the history of
every clone.

## Version log

Every archive this directory has held, with the local time of the commit
that created it and, once pruned under the retention rule above, the commit
that removed it. The builds still present are marked *current*.

**Naming changed at v1.0.0.** Archives through v0082 used a bare four-digit
per-build counter (`Enterprise-Infrastructure-Encyclopedia-website-vNNNN.zip`);
a brief transition used a release version plus that counter
(`…-v1.0.0-0083.zip`). From v1.0.1, each archive is named for a release
version alone (`…-v1.0.1.zip`) — every build bumps the patch and is tagged
as a matching GitHub release. The historical rows below are kept for the
record.

| Version | Created | Deleted |
| --- | --- | --- |
| v0001 | 2026-07-20 13:12 | 2026-07-20 19:08 |
| v0002 | 2026-07-20 18:43 | 2026-07-20 19:15 |
| v0003 | 2026-07-20 18:49 | 2026-07-20 20:15 |
| v0004 | 2026-07-20 19:08 | 2026-07-20 20:22 |
| v0005 | 2026-07-20 19:15 | 2026-07-20 20:47 |
| v0006 | 2026-07-20 20:15 | 2026-07-20 20:59 |
| v0007 | 2026-07-20 20:22 | 2026-07-20 21:05 |
| v0008 | 2026-07-20 20:47 | 2026-07-20 21:14 |
| v0009 | 2026-07-20 20:59 | 2026-07-20 21:26 |
| v0010 | 2026-07-20 21:05 | 2026-07-20 21:34 |
| v0011 | 2026-07-20 21:14 | 2026-07-20 21:43 |
| v0012 | 2026-07-20 21:26 | 2026-07-20 21:52 |
| v0013 | 2026-07-20 21:34 | 2026-07-20 22:19 |
| v0014 | 2026-07-20 21:43 | 2026-07-20 22:28 |
| v0015 | 2026-07-20 21:52 | 2026-07-20 22:37 |
| v0016 | 2026-07-20 22:19 | 2026-07-20 22:53 |
| v0017 | 2026-07-20 22:28 | 2026-07-20 23:16 |
| v0018 | 2026-07-20 22:37 | 2026-07-20 23:16 |
| v0019 | 2026-07-20 22:53 | 2026-07-20 23:30 |
| v0020 | 2026-07-20 23:16 | 2026-07-20 23:38 |
| v0021 | 2026-07-20 23:16 | 2026-07-20 23:50 |
| v0022 | 2026-07-20 23:30 | 2026-07-21 00:08 |
| v0023 | 2026-07-20 23:38 | 2026-07-21 01:05 |
| v0024 | 2026-07-20 23:50 | 2026-07-21 07:52 |
| v0025 | 2026-07-21 00:08 | 2026-07-21 08:06 |
| v0026 | 2026-07-21 01:05 | 2026-07-21 08:18 |
| v0027 | 2026-07-21 07:52 | 2026-07-21 08:31 |
| v0028 | 2026-07-21 08:06 | 2026-07-21 13:25 |
| v0029 | 2026-07-21 08:18 | 2026-07-21 13:39 |
| v0030 | 2026-07-21 08:31 | 2026-07-21 14:08 |
| v0031 | 2026-07-21 13:25 | 2026-07-21 14:27 |
| v0032 | 2026-07-21 13:39 | 2026-07-21 14:37 |
| v0033 | 2026-07-21 14:08 | 2026-07-21 15:21 |
| v0034 | 2026-07-21 14:27 | 2026-07-21 16:08 |
| v0035 | 2026-07-21 14:37 | 2026-07-21 16:23 |
| v0036 | 2026-07-21 15:21 | 2026-07-21 17:14 |
| v0037 | 2026-07-21 16:08 | 2026-07-21 17:42 |
| v0038 | 2026-07-21 16:23 | 2026-07-21 19:01 |
| v0039 | 2026-07-21 17:14 | 2026-07-21 19:53 |
| v0040 | 2026-07-21 17:42 | 2026-07-21 21:24 |
| v0041 | 2026-07-21 19:01 | 2026-07-21 22:39 |
| v0042 | 2026-07-21 19:53 | 2026-07-21 23:04 |
| v0043 | 2026-07-21 21:24 | 2026-07-21 23:19 |
| v0044 | 2026-07-21 22:39 | 2026-07-21 23:29 |
| v0045 | 2026-07-21 23:04 | 2026-07-21 23:57 |
| v0046 | 2026-07-21 23:19 | 2026-07-22 00:20 |
| v0047 | 2026-07-21 23:29 | 2026-07-22 00:48 |
| v0048 | 2026-07-21 23:57 | 2026-07-22 05:20 |
| v0049 | 2026-07-22 00:20 | 2026-07-22 05:55 |
| v0050 | 2026-07-22 00:48 | 2026-07-22 06:30 |
| v0051 | 2026-07-22 05:20 | 2026-07-22 07:07 |
| v0052 | 2026-07-22 05:55 | 2026-07-22 07:39 |
| v0053 | 2026-07-22 06:30 | 2026-07-22 08:03 |
| v0054 | 2026-07-22 07:07 | 2026-07-22 08:47 |
| v0055 | 2026-07-22 07:39 | 2026-07-22 09:02 |
| v0056 | 2026-07-22 08:03 | 2026-07-22 13:58 |
| v0057 | 2026-07-22 08:47 | 2026-07-22 15:04 |
| v0058 | 2026-07-22 09:02 | 2026-07-22 15:37 |
| v0059 | 2026-07-22 13:58 | 2026-07-22 16:13 |
| v0060 | 2026-07-22 15:04 | 2026-07-22 16:47 |
| v0061 | 2026-07-22 15:37 | 2026-07-22 17:06 |
| v0062 | 2026-07-22 16:13 | 2026-07-22 17:23 |
| v0063 | 2026-07-22 16:47 | 2026-07-22 17:50 |
| v0064 | 2026-07-22 17:06 | 2026-07-22 18:16 |
| v0065 | 2026-07-22 17:23 | 2026-07-22 18:36 |
| v0066 | 2026-07-22 17:50 | 2026-07-22 19:19 |
| v0067 | 2026-07-22 18:16 | 2026-07-22 19:32 |
| v0068 | 2026-07-22 18:36 | 2026-07-22 20:24 |
| v0069 | 2026-07-22 19:19 | 2026-07-22 20:41 |
| v0070 | 2026-07-22 19:32 | 2026-07-22 21:43 |
| v0071 | 2026-07-22 20:24 | 2026-07-22 22:03 |
| v0072 | 2026-07-22 20:41 | 2026-07-22 22:50 |
| v0073 | 2026-07-22 21:43 | 2026-07-22 23:00 |
| v0074 | 2026-07-22 22:03 | 2026-07-22 23:20 |
| v0075 | 2026-07-22 22:50 | 2026-07-23 05:06 |
| v0076 | 2026-07-22 23:00 | 2026-07-23 05:45 |
| v0077 | 2026-07-22 23:20 | 2026-07-23 06:14 |
| v0078 | 2026-07-23 05:06 | 2026-07-23 07:03 |
| v0079 | 2026-07-23 05:45 | 2026-07-23 07:20 |
| v0080 | 2026-07-23 06:14 | 2026-07-23 07:47 |
| v0081 | 2026-07-23 07:03 | 2026-07-23 07:47 |
| v0082 | 2026-07-23 07:20 | 2026-07-23 07:47 |
| v1.0.0 | 2026-07-23 07:47 | 2026-07-23 08:01 |
| v1.0.0-0083 | 2026-07-23 08:01 | 2026-07-23 08:10 |
| v1.0.1 | 2026-07-23 08:10 | 2026-07-23 20:43 |
| v1.0.2 | 2026-07-23 18:56 | 2026-07-23 23:25 |
| v1.0.3 | 2026-07-23 19:22 | *current* |
| v1.1.0 | 2026-07-23 20:43 | *current* |
| v1.2.0 | 2026-07-23 23:25 | *current* |

## Rebuilding

```bash
scripts/bash/build-book.sh --format all
scripts/bash/build-download-site.sh --output _site
```

Then stage `_site/` under a directory named for the new version, strip any
`.DS_Store` files, and zip it so it extracts into that one directory.
