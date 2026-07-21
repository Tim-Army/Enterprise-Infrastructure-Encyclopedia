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
├── volumes/           All 25 volumes (see above)
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
- The 24th volume's title uses **Volume XCIX** (the Roman numeral for 99)
  rather than continuing the sequential I–XXIII numbering used by every
  other volume. Its directory slug is `volume-99-reference-library` —
  99 written in Arabic numerals, matching XCIX's value rather than the
  volume's ordinal position in the series — so it still sorts correctly
  after `volume-23-...` in a plain lexicographic directory listing.
