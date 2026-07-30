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
├── volumes/           All 96 volumes (see above)
├── INDEX.md           Master index across all volumes
├── GLOSSARY.md         Master glossary across all volumes
├── MASTER_TOC.md        Canonical series table of contents
├── ROADMAP.md          Authoritative 24-volume curriculum plan
├── SOFTWARE_VERSIONS.md  Dated software/platform baseline
└── book.yml            Chapter sources and build eligibility
```

## Naming rules

- Volume slugs are zero-padded **three-digit** numbers followed by a short
  kebab-case name: `volume-001-enterprise-engineering-foundations`. Three
  digits is a deliberate width choice: it keeps a plain lexicographic listing
  (and therefore the build's `volumes/*/` glob) in true series order all the
  way to volume 999, which two-digit padding cannot do — under the old scheme
  a hypothetical `volume-100-...` sorted between `volume-10-...` and
  `volume-11-...`.
- Chapter slugs are zero-padded two-digit numbers followed by a short
  kebab-case title: `01-network-models-and-protocol-architecture.md`.
- The three **reference volumes** at the end of the series are numbered out
  of sequence, in a reserved high block rather than continuing the ordinal
  numbering used by every instructional volume:

  | Volume | Slug | Content |
  | --- | --- | --- |
  | **CMXCVII** | `volume-997-master-appendices` | Course-catalog appendices |
  | **CMXCVIII** | `volume-998-acronyms` | Acronym dictionary |
  | **CMXCIX** | `volume-999-reference-library` | Cross-volume reference material |

  In every case the slug's Arabic number matches the Roman numeral's value
  (997 = CMXCVII, 998 = CMXCVIII, 999 = CMXCIX) rather than the volume's
  ordinal position in the series. Because every volume slug is padded to the
  same three-digit width, the reference block sorts last in a plain
  lexicographic directory listing purely on its numeric value —
  `volume-997-...` follows `volume-092-...` — which is what keeps the build's
  `volumes/*/` glob emitting them at the end of the series.
- The reserved block was renumbered from 97/98/99 to 997/998/999 so the
  instructional sequence can grow past 92 without colliding with it. The
  instructional volumes were subsequently widened from two digits to three so
  that the whole series shares one width and stays correctly ordered past
  volume 99.
