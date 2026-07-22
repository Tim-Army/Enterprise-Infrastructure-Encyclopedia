# Volume XCVII — Master Appendices

The single home for every appendix in the encyclopedia. When a volume's
material calls for an appendix — a data table, a catalog, an as-built
record — the appendix lives here as a chapter, and the source volume
links to it, so supplementary reference tables are always findable in
one place instead of scattered through volume READMEs.

## Chapters

1. [Appendix — Cisco U. Learning Paths and Continuing Education Credits](chapters/01-appendix-cisco-u-learning-paths-and-continuing-education-credits.md) — every Cisco U. Learning Path with the exam it prepares for, its Continuing Education credit value, and whether it is free or needs a subscription; snapshot dated 22 July 2026.
2. [Appendix — Proxmox Lab IPv4 and IPv6 Address Tables](chapters/02-appendix-proxmox-lab-ipv4-and-ipv6-address-tables.md) — the as-built IPv4 addressing and the IPv6 template for the Volume XXVI Dell PowerEdge R640 Proxmox lab.
3. [Appendix — Juniper Courses and Certification Alignment](chapters/03-appendix-juniper-courses-and-certification-alignment.md) — every official Juniper course with the exam it prepares for and whether it is free; snapshot dated 22 July 2026.

## Appendix catalog

| Appendix | Serves | Chapter |
| --- | --- | --- |
| Cisco U. Learning Paths and CE credits | The Cisco certification tracks (Volumes III, XXV, XXVII–XXX) | [01](chapters/01-appendix-cisco-u-learning-paths-and-continuing-education-credits.md) |
| Appendix A: IPv4 Table (R640 lab, as built) | [Volume XXVI](../volume-26-proxmox-lab-poweredge-r640/README.md) | [02](chapters/02-appendix-proxmox-lab-ipv4-and-ipv6-address-tables.md) |
| Appendix B: IPv6 Table (R640 lab, template) | [Volume XXVI](../volume-26-proxmox-lab-poweredge-r640/README.md) | [02](chapters/02-appendix-proxmox-lab-ipv4-and-ipv6-address-tables.md) |
| Juniper courses and certification alignment | [Volume XXXI](../volume-31-juniper-networks-certifications/README.md) | [03](chapters/03-appendix-juniper-courses-and-certification-alignment.md) |

## Conventions

- An appendix keeps its original lettering (Appendix A, Appendix B) from
  its source volume, so cross-references in that volume's chapters stay
  meaningful.
- The source volume keeps a short pointer section linking here; the data
  itself is not duplicated.
- Volume XCVII sorts just before the Reference Library (XCIX) at the end
  of the shelf: appendices, then reference.

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
  --volume volume-97-master-appendices
```
