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
4. [Appendix — Dell Technologies Certifications and Course Access](chapters/04-appendix-dell-technologies-certifications-and-course-access.md) — all 77 current Dell exams with official pages and the program's training-access model; snapshot dated 22 July 2026.
5. [Appendix — Palo Alto Networks Certifications and Course Access](chapters/05-appendix-palo-alto-networks-certifications-and-course-access.md) — the 17 role-based Palo Alto Networks certifications with official pages and the Beacon free / ILT paid access model; snapshot dated 22 July 2026.
6. [Appendix — Fortinet NSE Certifications and Course Access](chapters/06-appendix-fortinet-nse-certifications-and-course-access.md) — the restored NSE 1–8 program by track and level with the free-self-paced / paid-ILT access model; snapshot dated 22 July 2026.
7. [Appendix — VMware and Broadcom Certifications and Course Access](chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) — the whole Broadcom/VMware program by tier (VCP, VCAP, Distinguished Expert, Telco Cloud) with exam codes, exam end dates, and the Learning@Broadcom paid-ILT / free Hands-on Labs access model; snapshot dated 23 July 2026.
8. [Appendix — AWS Certifications and Course Access](chapters/08-appendix-aws-certifications-and-course-access.md) — all twelve current AWS certifications by level with exam codes, exam end dates, and the free Skill Builder exam-prep / paid classroom access model; snapshot dated 23 July 2026.
9. [Appendix — Microsoft Azure Certifications and Course Access](chapters/09-appendix-microsoft-azure-certifications-and-course-access.md) — every current Azure certification by level with exam codes, exam end dates, the retired list, and the free Microsoft Learn training / annual free renewal model; snapshot dated 23 July 2026.
10. [Appendix — Google Cloud Certifications and Course Access](chapters/10-appendix-google-cloud-certifications-and-course-access.md) — all fourteen Google Cloud certifications by level with format, fee, validity, the free Google Skills training, and why the exam-code column reads "none"; snapshot dated 23 July 2026.

## Appendix catalog

| Appendix | Serves | Chapter |
| --- | --- | --- |
| Cisco U. Learning Paths and CE credits | The Cisco certification tracks (Volumes III, XXV, XXVII–XXX) | [01](chapters/01-appendix-cisco-u-learning-paths-and-continuing-education-credits.md) |
| Appendix A: IPv4 Table (R640 lab, as built) | [Volume XXVI](../volume-26-proxmox-lab-poweredge-r640/README.md) | [02](chapters/02-appendix-proxmox-lab-ipv4-and-ipv6-address-tables.md) |
| Appendix B: IPv6 Table (R640 lab, template) | [Volume XXVI](../volume-26-proxmox-lab-poweredge-r640/README.md) | [02](chapters/02-appendix-proxmox-lab-ipv4-and-ipv6-address-tables.md) |
| Juniper courses and certification alignment | [Volume XXXI](../volume-31-juniper-networks-certifications/README.md) | [03](chapters/03-appendix-juniper-courses-and-certification-alignment.md) |
| Dell certifications and course access | [Volume XXXII](../volume-32-dell-technologies-certifications/README.md) | [04](chapters/04-appendix-dell-technologies-certifications-and-course-access.md) |
| Palo Alto Networks certifications and course access | [Volume XVI](../volume-16-palo-alto-networks-security/README.md) | [05](chapters/05-appendix-palo-alto-networks-certifications-and-course-access.md) |
| Fortinet NSE certifications and course access | [Volume XIX](../volume-19-fortinet-network-security/README.md) | [06](chapters/06-appendix-fortinet-nse-certifications-and-course-access.md) |
| VMware and Broadcom certifications and course access | [Volume V](../volume-05-vmware-virtualization/README.md) | [07](chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) |
| AWS certifications and course access | [Volume XVII](../volume-17-aws-architecture-security/README.md) | [08](chapters/08-appendix-aws-certifications-and-course-access.md) |
| Microsoft Azure certifications and course access | [Volume XXXIII](../volume-33-microsoft-azure-certifications/README.md) | [09](chapters/09-appendix-microsoft-azure-certifications-and-course-access.md) |
| Google Cloud certifications and course access | [Volume XXXIV](../volume-34-google-cloud-certifications/README.md) | [10](chapters/10-appendix-google-cloud-certifications-and-course-access.md) |

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
