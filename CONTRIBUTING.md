# Contributing

Thank you for improving the Enterprise Infrastructure Encyclopedia.

## Documentation standards

- Follow [EDITORIAL_STANDARDS.md](EDITORIAL_STANDARDS.md) for tone,
  structure, and Markdown conventions.
- Start new chapters from [templates/chapter.md](templates/chapter.md) and
  bring them to publication standard with the
  [chapter-expansion instructions](templates/chapter-expansion-instructions.md).
- Complete the [technical-review checklist](templates/technical-review-checklist.md)
  before marking a chapter published.
- Keep the volume-first path convention in [Structure.md](Structure.md).

## Workflow

- Work directly on `main` for routine content changes; open a pull request
  for structural or build-tooling changes so they can be reviewed.
- Keep the root README, `MASTER_TOC.md`, `SUMMARY.md`, `book.yml`, the
  affected volume README, and `PROJECT_STATUS.md` synchronized with any
  content change.
- Run `scripts/bash/validate.sh` before committing.

## Scope boundaries

- Do not commit credentials, license keys, personal data, or proprietary
  exam/training content.
- Vendor guidance should reflect the dated baseline in
  [SOFTWARE_VERSIONS.md](SOFTWARE_VERSIONS.md); update that file in the same
  change if you write against a newer release.

## Getting help

See [SETUP.md](SETUP.md) for local tooling and [AUTOMATION.md](AUTOMATION.md)
for safe repository automation practices.
