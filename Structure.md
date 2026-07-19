# Repository Structure

## Canonical chapter path

```text
volumes/volume-NN-volume-slug/chapters/NN-chapter-slug.md
```

The repository does not use a root-level `chapters/` directory. Every chapter
belongs to exactly one volume and is numbered sequentially within that
volume's `chapters/` folder.

## Volume layout

Each volume directory follows the same shape:

```text
volumes/volume-NN-volume-slug/
├── README.md      Volume overview and chapter table of contents
├── INDEX.md        Topical index for the volume
├── GLOSSARY.md      Volume-specific term definitions
└── chapters/
    ├── 01-chapter-slug.md
    ├── 02-chapter-slug.md
    └── ...
```

## Top-level layout

```text
Enterprise-Infrastructure-Encyclopedia/
├── .github/          GitHub configuration and validation workflows
├── configs/          Vendor and platform configuration examples
├── diagrams/         Architecture and topology diagrams
├── labs/             Cross-volume lab assets
├── publishing/        Publishing assets (CSS, theme toggle)
├── references/        Shared references
├── scripts/          Repository and publishing automation
├── templates/         Reusable content templates
├── tests/            Repository and content validation tests
├── volumes/           All 24 volumes (see above)
├── INDEX.md           Master index across all volumes
├── GLOSSARY.md         Master glossary across all volumes
├── MASTER_TOC.md        Canonical series table of contents
├── ROADMAP.md          Authoritative 24-volume curriculum plan
├── SOFTWARE_VERSIONS.md  Dated software/platform baseline
└── book.yml            Chapter sources and build eligibility
```

## Naming rules

- Volume slugs are zero-padded two-digit numbers followed by a short
  kebab-case name: `volume-01-enterprise-engineering-foundations`.
- Chapter slugs are zero-padded two-digit numbers followed by a short
  kebab-case title: `01-network-models-and-protocol-architecture.md`.
- The 24th volume's title uses **Volume C** (the Roman numeral for 100,
  not 24) rather than continuing the sequential I–XXIII numbering used by
  every other volume; it still keeps the `volume-24-` directory slug for
  filesystem ordering, so the slug and the display title intentionally
  don't match for this one volume.
