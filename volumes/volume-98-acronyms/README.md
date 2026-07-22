# Volume XCVIII — Acronyms

The encyclopedia's acronym dictionary: every acronym and initialism the
shelf uses, defined in one place. Volume glossaries define the concepts
behind their own terms; this volume answers the quicker question — what
do the letters stand for — across all volumes at once.

## Inclusion criteria

- The acronym appears at least three times across the shelf.
- Its expansion is copied from the volume that introduces it, or is the
  standard, unambiguous industry expansion. Nothing is guessed: tokens
  that could not be expanded from either source are left out rather
  than defined loosely.
- Acronyms with more than one meaning on this shelf list each meaning
  in a single entry (for example, CE and DR).
- Lab hostnames, product model numbers, and document names are not
  acronyms and are excluded.

## Chapters

1. [Acronyms A through D](chapters/01-acronyms-a-through-d.md)
2. [Acronyms E through L](chapters/02-acronyms-e-through-l.md)
3. [Acronyms M through R](chapters/03-acronyms-m-through-r.md)
4. [Acronyms S through Z](chapters/04-acronyms-s-through-z.md)

## Conventions

- Entries are alphabetized case-insensitively, so `iDRAC` sorts under I
  and `vPC` under V.
- The dictionary defines expansions only; for the concept behind a
  term, follow it into the glossary of the volume that introduces it.
- Volume XCVIII sits between the Master Appendices (XCVII) and the
  Reference Library (XCIX) at the end of the shelf.

## Volume resources

- [Volume index](INDEX.md)
- [Volume glossary](GLOSSARY.md)
- [Master table of contents](../../MASTER_TOC.md)

## Building and validating this volume

```bash
# Full validation and repo-wide link checks.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-98-acronyms
```
