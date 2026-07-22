# Enterprise Infrastructure Encyclopedia

> A volume-first, documentation-as-code curriculum for designing, deploying, securing, automating, operating, and troubleshooting modern enterprise infrastructure.

<a href="https://derg20.github.io/Enterprise-Infrastructure-Encyclopedia/" target="_blank" rel="noopener noreferrer">Read the HTML edition</a>

Also mirrored at [github.com/Tim-Army/Enterprise-Infrastructure-Encyclopedia](https://github.com/Tim-Army/Enterprise-Infrastructure-Encyclopedia), with its own [HTML edition](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/).

![Status](https://img.shields.io/badge/status-active%20development-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Markdown](https://img.shields.io/badge/documentation-Markdown-blue)

## Overview

The Enterprise Infrastructure Encyclopedia is a 33-volume technical curriculum for infrastructure engineers, architects, administrators, cloud engineers, automation engineers, security professionals, students, and instructors.

The series combines architecture and theory with implementation guidance, automation, validation, troubleshooting, security, best practices, knowledge checks, and hands-on labs. Sources are maintained in Markdown and organized by volume for multi-format publishing.

## Curriculum

33 volumes, 291 chapters. Each volume has a dedicated
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
| XXIV | [Dell VxRail Hyperconverged Infrastructure](volumes/volume-24-dell-vxrail-hci/README.md) | 9 |
| XXV | [Cisco Security](volumes/volume-25-cisco-security/README.md) | 9 |
| XXVI | [Proxmox Virtualization Lab on Dell PowerEdge R640](volumes/volume-26-proxmox-lab-poweredge-r640/README.md) | 9 |
| XXVII | [Cisco Data Center](volumes/volume-27-cisco-data-center/README.md) | 9 |
| XXVIII | [Cisco Collaboration](volumes/volume-28-cisco-collaboration/README.md) | 9 |
| XXIX | [Cisco Service Provider](volumes/volume-29-cisco-service-provider/README.md) | 9 |
| XXX | [Cisco CCDE Network Design](volumes/volume-30-cisco-ccde-network-design/README.md) | 9 |
| XCVII | [Master Appendices](volumes/volume-97-master-appendices/README.md) | 2 |
| XCVIII | [Acronyms](volumes/volume-98-acronyms/README.md) | 4 |
| XCIX | [Reference Library](volumes/volume-99-reference-library/README.md) | 9 |

Technical review and lab-validation sign-off for all 286 chapters are
tracked in [PROJECT_STATUS.md](PROJECT_STATUS.md). The
[master index](INDEX.md) and [master glossary](GLOSSARY.md) cover all
volumes.

See the [24-volume roadmap](ROADMAP.md) for approved titles, stable slugs,
scope, dependencies, and ownership. [MASTER_TOC.md](MASTER_TOC.md) provides
full series navigation, and [PROJECT_STATUS.md](PROJECT_STATUS.md) records
current delivery progress.

## Tracks

A volume's number records the order it joined the series and never changes —
it is a stable identifier, not a shelf position — so related volumes are not
always adjacent. The reading paths below group them thematically. A volume
can appear in more than one track, and each path lists its volumes in
ascending order.

| Track | Reading path |
| --- | --- |
| Core curriculum | Volumes [I](volumes/volume-01-enterprise-engineering-foundations/README.md)–[XIII](volumes/volume-13-integrated-enterprise-labs/README.md) in numbered order — foundations through integrated labs |
| Cisco | [III Enterprise Networking](volumes/volume-03-cisco-enterprise-networking/README.md) → [XXV Security](volumes/volume-25-cisco-security/README.md) → [XXVII Data Center](volumes/volume-27-cisco-data-center/README.md) → [XXVIII Collaboration](volumes/volume-28-cisco-collaboration/README.md) → [XXIX Service Provider](volumes/volume-29-cisco-service-provider/README.md) → [XXX CCDE Network Design](volumes/volume-30-cisco-ccde-network-design/README.md) |
| Dell | [XXII OpenManage Enterprise](volumes/volume-22-dell-openmanage-enterprise/README.md) → [XXIII iDRAC 9 and 10](volumes/volume-23-dell-idrac-9-10-administration/README.md) → [XXIV VxRail](volumes/volume-24-dell-vxrail-hci/README.md) → [XXVI Proxmox lab on PowerEdge R640](volumes/volume-26-proxmox-lab-poweredge-r640/README.md) |
| Security | [X Enterprise Cybersecurity](volumes/volume-10-enterprise-cybersecurity/README.md) → [XV Forescout](volumes/volume-15-forescout-platform-certifications/README.md) → [XVI Palo Alto Networks](volumes/volume-16-palo-alto-networks-security/README.md) → [XIX Fortinet](volumes/volume-19-fortinet-network-security/README.md) → [XXV Cisco Security](volumes/volume-25-cisco-security/README.md) |
| Visibility and analysis | [XI Observability and Enterprise Operations](volumes/volume-11-observability-enterprise-operations/README.md) → [XVIII Gigamon](volumes/volume-18-gigamon-network-visibility/README.md) → [XX Wireshark and Packet Analysis](volumes/volume-20-wireshark-packet-analysis/README.md) |
| Operating systems | [XIV Red Hat Enterprise Linux 10](volumes/volume-14-red-hat-enterprise-linux-10/README.md) → [XXI Ubuntu Server and Cloud 26.04 LTS](volumes/volume-21-ubuntu-server-cloud-26-04-lts/README.md) |
| Virtualization | [V VMware](volumes/volume-05-vmware-virtualization/README.md) → [XXIV VxRail](volumes/volume-24-dell-vxrail-hci/README.md) → [XXVI Proxmox lab on PowerEdge R640](volumes/volume-26-proxmox-lab-poweredge-r640/README.md) |
| Cloud | [VII Cloud Infrastructure](volumes/volume-07-cloud-infrastructure/README.md) → [XVII AWS Architecture and Security](volumes/volume-17-aws-architecture-security/README.md) |
| Reference | [XCVII Master Appendices](volumes/volume-97-master-appendices/README.md), [XCVIII Acronyms](volumes/volume-98-acronyms/README.md), and [XCIX Reference Library](volumes/volume-99-reference-library/README.md) — appendices, the acronym dictionary, and cross-volume reference material, always last |

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
│   └── ... (27 volumes total, see MASTER_TOC.md)
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

# Build the complete reading and download portal (requires build-book.sh
# to have run first, since it copies output/html/ and output/epub/).
scripts/bash/build-download-site.sh --output _site
```

Follow [SETUP.md](SETUP.md) for the pinned Node.js, pnpm, ShellCheck, Pandoc,
and Lychee installation. Generated self-contained HTML and EPUB 3 files are
written below `output/`.

## HTML edition build instructions

The HTML edition uses Pandoc with [publishing/web.css](publishing/web.css) and
the [theme switcher](publishing/theme-toggle.html). It opens in dark mode with
a `#1e1e1e` background and `#76d40b` body text, mirroring the mindthedark
template on tim.army; the fixed upper-right control switches
to light mode and remembers the reader's choice in that browser. The generated
reading and download portal uses the same dark-first theme and its upper-right
control.

After completing the setup in [SETUP.md](SETUP.md), use the following commands
from the repository root:

```bash
# Validate all source and publishing prerequisites first.
scripts/bash/validate.sh

# Build self-contained HTML and EPUB for the complete encyclopedia, every
# volume, and every chapter — output/html/ and output/epub/.
scripts/bash/build-book.sh --format all

# Or scope to one completed volume.
scripts/bash/build-book.sh --format all \
  --volume volume-02-network-engineering-foundations

# Or scope to one published chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-02-network-engineering-foundations/chapters/01-network-models-and-protocol-architecture.md

# Build and verify the HTML reading and download portal (run build-book.sh
# first — this copies its output/ into _site/ and adds navigation pages).
scripts/bash/build-download-site.sh --output _site
```

HTML files are written to `output/html/`; EPUB files are written to
`output/epub/`. The portal build copies both into `_site/`, generates a root
index and a per-volume index page linking every chapter and download, and
verifies every generated link resolves before it succeeds — this is the
artifact deployed by the Pages workflow. Do not manually edit generated files
in `output/` or `_site/`; change the Markdown source, publishing assets, or
build scripts and regenerate instead.

Links between chapters (same-volume or cross-volume) are rewritten by
[scripts/bash/lib/rewrite_chapter_links.py](scripts/bash/lib/rewrite_chapter_links.py)
before each Pandoc invocation: in HTML output they become relative links to
that chapter's own page; in EPUB output — which cannot address a separate
`output/html/` file — they become absolute links to the deployed Pages
portal. Links to anything other than a chapter file (root docs, volume or
root README/INDEX/GLOSSARY) are left pointing at their `.md` path, since
those don't have a generated-output page to point at instead.

External references can be checked separately with:

```bash
scripts/bash/check-external-links.sh
```

GitHub Actions runs repository structure, editorial, Markdown, spelling,
internal-link, and external-link checks on `main`. The Pages workflow
publishes an accessible portal with online reading and EPUB download for the
complete encyclopedia, every volume, and every chapter. Version tags matching
`v*` publish the complete-encyclopedia HTML and EPUB to a GitHub release under
the [release process](RELEASE_PROCESS.md).

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
- Generate HTML and EPUB editions for a volume once it has a complete
  chapter set plus README, INDEX, and GLOSSARY; complete-series editions
  cover every volume.
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
