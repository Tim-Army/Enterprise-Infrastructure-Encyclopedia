# Setup

Pinned local tooling for validation and publishing builds.

## Requirements

| Tool | Version | Purpose |
| --- | --- | --- |
| Node.js | 22.x LTS (see `.node-version`) | Validation and lint tooling |
| pnpm | 11.9.0 | Package management (via Corepack) |
| ShellCheck | latest stable | Lint `scripts/bash/*.sh` |
| Pandoc | 3.x | DOCX, HTML, and EPUB generation |
| Typst | latest stable | Tagged PDF/UA-1 generation |
| Lychee | latest stable | External link checking |

## Install

```bash
corepack enable
corepack prepare pnpm@11.9.0 --activate
pnpm install --frozen-lockfile
```

Install ShellCheck, Pandoc, Typst, and Lychee with your platform's package
manager (for example `brew install shellcheck pandoc typst lychee` on
macOS, or the equivalent `apt`/`dnf` packages on Linux).

## Verify

```bash
scripts/bash/validate.sh
```

This runs the full non-networked validation suite described in
[AUTOMATION.md](AUTOMATION.md). Resolve any failures before committing.

## Build a local edition

```bash
scripts/bash/build-book.sh --format html
```

See the [README build instructions](README.md#validation) for the complete
set of build and portal commands.
