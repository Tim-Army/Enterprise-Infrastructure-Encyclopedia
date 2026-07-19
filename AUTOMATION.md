# Automation

This document describes the repository's own automation — validation,
publishing builds, and link checking — and the safety rules for running it.

## Validation

`scripts/bash/validate.sh` runs without network access and checks:

- Every volume has a `README.md`, `INDEX.md`, `GLOSSARY.md`, and a
  contiguous, gap-free `chapters/` sequence.
- Every chapter declared in [book.yml](book.yml) exists on disk and every
  chapter file on disk is declared in `book.yml`.
- Markdown lint (`markdownlint-cli2`) and spelling (`cspell`) pass.
- Internal links resolve (no dangling relative links between Markdown files).

## Publishing builds

`scripts/bash/build-book.sh` generates self-contained HTML and EPUB 3
editions from Markdown sources using Pandoc. It accepts `--format`
(`all`, `html`, or `epub`), `--volume`, and `--chapter` scoping flags.
Chapter and volume order comes directly from the `volumes/` directory
structure. With no scoping flag it builds every chapter, every volume
(combined into one document), and the complete-series edition.

`scripts/bash/build-download-site.sh` builds the combined reading and
download portal (`_site/`) that the Pages workflow deploys.

## External link checking

`scripts/bash/check-external-links.sh` runs Lychee against every Markdown
file. It requires network access and is not part of the default validation
gate, so a flaky external site cannot block a local commit.

## Safe repository automation rules

- Automation must never force-push, rewrite history, or bypass branch
  protection.
- Generated output (`output/`, `_site/`) is gitignored; regenerate it from
  source rather than editing it directly.
- CI workflows in `.github/workflows/` run validation on every push to
  `main` and publish the Pages portal only after validation passes.
- Release automation only triggers on `v*` tags and only publishes artifacts
  that passed the full validation and build gate.
