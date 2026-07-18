# Enterprise Infrastructure Encyclopedia

> A volume-first, documentation-as-code curriculum for designing, deploying, securing, automating, operating, and troubleshooting modern enterprise infrastructure.

<a href="https://derg20.github.io/Enterprise-Infrastructure-Encyclopedia-v2/" target="_blank" rel="noopener noreferrer">Read the HTML edition</a>

![Status](https://img.shields.io/badge/status-active%20development-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Markdown](https://img.shields.io/badge/documentation-Markdown-blue)

## Overview

The Enterprise Infrastructure Encyclopedia is a 24-volume technical curriculum for infrastructure engineers, architects, administrators, cloud engineers, automation engineers, security professionals, students, and instructors.

The series combines architecture and theory with implementation guidance, automation, validation, troubleshooting, security, best practices, knowledge checks, and hands-on labs. Sources are maintained in Markdown and organized by volume for multi-format publishing.

## Curriculum

24 volumes, 222 chapters. Each volume has a dedicated
[README](#volume-first-layout), index, and glossary.

| Volume | Title | Chapters |
| --- | --- | --- |
| I | [Enterprise Engineering Foundations](volumes/volume-01-enterprise-engineering-foundations/README.md) | 8 |
| II | [Network Engineering Foundations](volumes/volume-02-network-engineering-foundations/README.md) | 9 |
| III | [Cisco Enterprise Networking](volumes/volume-03-cisco-enterprise-networking/README.md) | 9 |
| IV | [Enterprise Systems Administration](volumes/volume-04-enterprise-systems-administration/README.md) | 9 |
| V | [VMware Virtualization](volumes/volume-05-vmware-virtualization/README.md) | 16 |
| VI | [Enterprise Storage and Data Protection](volumes/volume-06-enterprise-storage-data-protection/README.md) | 9 |
| VII | [Cloud Infrastructure](volumes/volume-07-cloud-infrastructure/README.md) | 9 |
| VIII | [Containers and Platform Engineering](volumes/volume-08-containers-platform-engineering/README.md) | 9 |
| IX | [Infrastructure Automation](volumes/volume-09-infrastructure-automation/README.md) | 9 |
| X | [Enterprise Cybersecurity](volumes/volume-10-enterprise-cybersecurity/README.md) | 9 |
| XI | [Observability and Enterprise Operations](volumes/volume-11-observability-enterprise-operations/README.md) | 9 |
| XII | [Resilience and Lifecycle Management](volumes/volume-12-resilience-lifecycle-management/README.md) | 9 |
| XIII | [Integrated Enterprise Labs](volumes/volume-13-integrated-enterprise-labs/README.md) | 9 |
| XIV | [Red Hat Enterprise Linux 10](volumes/volume-14-red-hat-enterprise-linux-10/README.md) | 9 |
| XV | [Forescout Platform and Certifications](volumes/volume-15-forescout-platform-certifications/README.md) | 9 |
| XVI | [Palo Alto Networks Security](volumes/volume-16-palo-alto-networks-security/README.md) | 9 |
| XVII | [AWS Architecture and Security](volumes/volume-17-aws-architecture-security/README.md) | 9 |
| XVIII | [Gigamon Network Visibility](volumes/volume-18-gigamon-network-visibility/README.md) | 9 |
| XIX | [Fortinet Network Security](volumes/volume-19-fortinet-network-security/README.md) | 9 |
| XX | [Wireshark and Packet Analysis](volumes/volume-20-wireshark-packet-analysis/README.md) | 9 |
| XXI | [Ubuntu Server and Cloud 26.04 LTS](volumes/volume-21-ubuntu-server-cloud-26-04-lts/README.md) | 9 |
| XXII | [Dell OpenManage Enterprise](volumes/volume-22-dell-openmanage-enterprise/README.md) | 9 |
| XXIII | [Dell iDRAC 9 and 10 Administration](volumes/volume-23-dell-idrac-9-10-administration/README.md) | 9 |
| C | [Reference Library](volumes/volume-24-reference-library/README.md) | 9 |

Technical review and lab-validation sign-off for all 222 chapters are
tracked in [PROJECT_STATUS.md](PROJECT_STATUS.md). The
[master index](INDEX.md) and [master glossary](GLOSSARY.md) cover all
volumes.

See the [24-volume roadmap](ROADMAP.md) for approved titles, stable slugs,
scope, dependencies, and ownership. [MASTER_TOC.md](MASTER_TOC.md) provides
full series navigation, and [PROJECT_STATUS.md](PROJECT_STATUS.md) records
current delivery progress.

## Volume-first layout

```text
Enterprise-Infrastructure-Encyclopedia/
├── .github/                 GitHub configuration and validation workflows
├── configs/                 Vendor and platform configuration examples
├── diagrams/                Architecture and topology diagrams
├── labs/                    Cross-volume lab assets
├── references/              Shared references
├── scripts/                 Repository and publishing automation
├── templates/               Reusable content templates
├── volumes/
│   ├── volume-01-enterprise-engineering-foundations/
│   │   ├── README.md
│   │   ├── INDEX.md
│   │   ├── GLOSSARY.md
│   │   └── chapters/
│   ├── volume-02-network-engineering-foundations/
│   │   ├── README.md
│   │   ├── INDEX.md
│   │   ├── GLOSSARY.md
│   │   └── chapters/
│   └── ... (24 volumes total, see MASTER_TOC.md)
├── INDEX.md
├── GLOSSARY.md
├── MASTER_TOC.md
├── ROADMAP.md
├── SOFTWARE_VERSIONS.md
├── SUMMARY.md
└── book.yml
```

Each chapter belongs to exactly one volume:

```text
volumes/volume-NN-volume-slug/chapters/NN-chapter-slug.md
```

The repository does not use a root-level `chapters/` directory. See [Structure.md](Structure.md) for the canonical path rules.

## Chapter framework

Chapters use a professional structure that includes:

- Learning objectives
- Theory and architecture
- Design considerations
- Implementation and automation
- Validation and troubleshooting
- Security and best practices
- References and knowledge checks
- Hands-on labs
- Summary and completion checklist

Use [templates/chapter.md](templates/chapter.md) when starting a manuscript.
Use the
[chapter-expansion instruction template](templates/chapter-expansion-instructions.md)
to bring an existing chapter to the complete topic-map and step-by-step lab
standard. Apply [EDITORIAL_STANDARDS.md](EDITORIAL_STANDARDS.md) and complete the
[technical-review checklist](templates/technical-review-checklist.md) before a
chapter advances to publication.

## Publishing sources

- [book.yml](book.yml) lists chapter sources and explicitly declares which
  volumes are complete and eligible for generated editions.
- [SUMMARY.md](SUMMARY.md) provides publishing navigation.
- [MASTER_TOC.md](MASTER_TOC.md) is the canonical series table of contents.
- [ROADMAP.md](ROADMAP.md) is the authoritative 24-volume curriculum plan.
- [SOFTWARE_VERSIONS.md](SOFTWARE_VERSIONS.md) defines the dated software
  baseline used by every chapter and volume.
- [CERTIFICATION_BLUEPRINTS.md](CERTIFICATION_BLUEPRINTS.md) maps every volume
  to relevant current vendor certifications, training paths, and controlling
  sources without reproducing proprietary assessment content.
- Each volume README is the authoritative table of contents for that volume.
- Each completed volume has its own index and glossary; the repository root has
  series-wide master versions.

Only existing, non-empty chapters from a completed volume are included in an
edition. A volume becomes build eligible only after its contiguous chapter
list, index, glossary, and declared chapter count pass repository validation.

## Validation

Install the locked Node dependencies once, then run the complete non-networked
validation and publication build before publishing changes:

```bash
corepack enable
corepack prepare pnpm@11.9.0 --activate
pnpm install --frozen-lockfile
scripts/bash/validate.sh
# Build the series from all completed volumes.
scripts/bash/build-book.sh --format all

# Or build one completed volume as a separate edition.
scripts/bash/build-book.sh --format all \
  --volume volume-02-network-engineering-foundations

# Or build a single published chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-02-network-engineering-foundations/chapters/01-network-models-and-protocol-architecture.md

# Build the complete reading and download portal.
scripts/bash/build-download-site.sh --output _site
```

Follow [SETUP.md](SETUP.md) for the pinned Node.js, pnpm, ShellCheck, Pandoc,
Typst, and Lychee installation. Complete-volume, series, and published-chapter
editions are generated only from volumes that passed the completed-volume gate.
Generated DOCX, self-contained HTML, offline website ZIP, tagged PDF/UA-1,
EPUB 3, and checksum-manifest files are written below `output/`.

## HTML edition build instructions

The HTML edition uses Pandoc with [publishing/web.css](publishing/web.css) and
the [theme switcher](publishing/theme-toggle.html). It opens in dark mode with
a black background and `#060` body text; the fixed upper-right control switches
to light mode and remembers the reader's choice in that browser. The generated
reading and download portal uses the same dark-first theme and its upper-right
control.

After completing the setup in [SETUP.md](SETUP.md), use the following commands
from the repository root:

```bash
# Validate all source and publishing prerequisites first.
scripts/bash/validate.sh

# Build the self-contained HTML edition for the complete encyclopedia.
scripts/bash/build-book.sh --format html

# Build the HTML edition for one completed volume.
scripts/bash/build-book.sh --format html \
  --volume volume-02-network-engineering-foundations

# Build the HTML edition for one published chapter.
scripts/bash/build-book.sh --format html \
  --chapter volumes/volume-02-network-engineering-foundations/chapters/01-network-models-and-protocol-architecture.md

# Build the offline website ZIP, which contains that scope's HTML edition.
scripts/bash/build-book.sh --format website-zip

# Build and validate the HTML reading and download portal.
scripts/bash/build-download-site.sh --output _site
```

HTML files are written to `output/html/`; offline website archives are written
to `output/website-zip/`. The portal build writes static pages, its CSS, and
theme script below `_site/`, verifies every catalog page and download link, and
is the artifact deployed by the Pages workflow. Do not manually edit generated
files in `output/` or `_site/`; change the Markdown source, publishing assets,
or build scripts and regenerate instead.

External references can be checked separately with:

```bash
scripts/bash/check-external-links.sh
```

GitHub Actions runs repository structure, editorial, Markdown, spelling,
internal-link, external-link, and multi-format publication checks on `main`.
The Pages workflow publishes an accessible portal with online reading and all
five download formats for the complete encyclopedia, every volume, and every
chapter. Version tags matching `v*` publish the verified complete-encyclopedia
artifacts to a GitHub release under the [release process](RELEASE_PROCESS.md).

## Encyclopedia operating instructions

The following rules govern ongoing creation and maintenance of this
encyclopedia. They consolidate the project workflow and editorial expectations
used for every volume and chapter.

### Repository workflow

- Work directly on `main`; do not create branches or pull requests for routine
  encyclopedia changes.
- Commit and push every completed change to the configured primary repository.
- Never force-push, reset `main`, bypass protections, or include unrelated
  changes in a commit.
- Treat credentials, license keys, personal data, and proprietary training or
  examination content as out of scope for commits.
- Report work only when it is complete or when user action is required to
  resolve a failure.

### Curriculum and chapter standards

- Maintain the volume-first structure and complete one volume to its declared
  standard before advancing to the next volume.
- Keep the root README, `MASTER_TOC.md`, `SUMMARY.md`, `book.yml`, volume
  README files, roadmap, and publication navigation synchronized when content
  changes.
- Keep a dedicated index and glossary for every volume, plus the master index
  and master glossary for the entire encyclopedia.
- Use the professional chapter framework: learning objectives, theory,
  architecture, design considerations, implementation, automation, validation,
  troubleshooting, security, best practices, references, knowledge checks,
  labs, summary, and completion checklist.
- Apply the chapter-expansion template and editorial standards before marking a
  chapter complete.

### Labs, certification, and technical accuracy

- Create hands-on labs as detailed walkthroughs with prerequisites, safe setup,
  numbered procedures, expected results, validation evidence, a negative test
  where appropriate, recovery guidance, and cleanup steps.
- Align vendor-focused volumes to relevant current certification blueprints and
  official training sources without reproducing protected exam questions or
  proprietary course material.
- Keep software, platform, and product version references aligned with
  `SOFTWARE_VERSIONS.md`; record dated baselines rather than implying that a
  version is timeless.
- Use accessible visuals where they materially improve learning, retain editable
  sources when possible, and provide meaningful text alternatives.

### Publishing and verification

- Document all build instructions in this `README.md` whenever a build,
  publishing workflow, format, dependency, or command is added or changed.
- Generate DOCX, HTML, PDF, EPUB, and offline website editions only after the
  entire applicable volume has passed its completed-volume gate; complete-series
  editions require every volume to pass.
- Maintain the download portal so readers can obtain the full encyclopedia,
  individual volumes, and individual chapters in each supported format.
- Run the relevant repository validation and publication checks before each
  commit, and resolve failures before publishing whenever possible.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for documentation standards,
[AUTOMATION.md](AUTOMATION.md) for safe repository operations, and
[SETUP.md](SETUP.md) for local dependencies.

## License

Released under the [MIT License](LICENSE).
