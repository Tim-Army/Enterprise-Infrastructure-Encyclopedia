# 27-Volume Curriculum Roadmap

This roadmap is the authoritative plan for the Enterprise Infrastructure
Encyclopedia: approved titles, stable slugs, scope, and chapter counts for
all 27 volumes. Dependencies are noted where a volume assumes prior volumes
as prerequisite reading.

| # | Volume | Slug | Chapters | Primary Dependency |
| --- | --- | --- | --- | --- |
| 1 | I — Enterprise Engineering Foundations | `volume-01-enterprise-engineering-foundations` | 8 | None (series entry point) |
| 2 | II — Network Engineering Foundations | `volume-02-network-engineering-foundations` | 9 | Volume I |
| 3 | III — Cisco Enterprise Networking | `volume-03-cisco-enterprise-networking` | 9 | Volume II |
| 4 | IV — Enterprise Systems Administration | `volume-04-enterprise-systems-administration` | 9 | Volume I |
| 5 | V — VMware Virtualization | `volume-05-vmware-virtualization` | 16 | Volumes I, IV |
| 6 | VI — Enterprise Storage and Data Protection | `volume-06-enterprise-storage-data-protection` | 9 | Volumes I, IV |
| 7 | VII — Cloud Infrastructure | `volume-07-cloud-infrastructure` | 9 | Volumes I, II, IV |
| 8 | VIII — Containers and Platform Engineering | `volume-08-containers-platform-engineering` | 9 | Volumes IV, VII |
| 9 | IX — Infrastructure Automation | `volume-09-infrastructure-automation` | 9 | Volumes I, IV |
| 10 | X — Enterprise Cybersecurity | `volume-10-enterprise-cybersecurity` | 9 | Volumes II, IV |
| 11 | XI — Observability and Enterprise Operations | `volume-11-observability-enterprise-operations` | 9 | Volumes IV, VII, VIII |
| 12 | XII — Resilience and Lifecycle Management | `volume-12-resilience-lifecycle-management` | 9 | Volumes IV, VI, VII |
| 13 | XIII — Integrated Enterprise Labs | `volume-13-integrated-enterprise-labs` | 9 | Volumes I–XII |
| 14 | XIV — Red Hat Enterprise Linux 10 | `volume-14-red-hat-enterprise-linux-10` | 9 | Volume IV |
| 15 | XV — Forescout Platform and Certifications | `volume-15-forescout-platform-certifications` | 9 | Volume II |
| 16 | XVI — Palo Alto Networks Security | `volume-16-palo-alto-networks-security` | 9 | Volume II |
| 17 | XVII — AWS Architecture and Security | `volume-17-aws-architecture-security` | 9 | Volume VII |
| 18 | XVIII — Gigamon Network Visibility | `volume-18-gigamon-network-visibility` | 9 | Volume II |
| 19 | XIX — Fortinet Network Security | `volume-19-fortinet-network-security` | 9 | Volume II |
| 20 | XX — Wireshark and Packet Analysis | `volume-20-wireshark-packet-analysis` | 9 | Volume II |
| 21 | XXI — Ubuntu Server and Cloud 26.04 LTS | `volume-21-ubuntu-server-cloud-26-04-lts` | 9 | Volume IV |
| 22 | XXII — Dell OpenManage Enterprise | `volume-22-dell-openmanage-enterprise` | 9 | Volume IV |
| 23 | XXIII — Dell iDRAC 9 and 10 Administration | `volume-23-dell-idrac-9-10-administration` | 9 | Volume IV |
| 24 | XXIV — Dell VxRail Hyperconverged Infrastructure | `volume-24-dell-vxrail-hci` | 9 | Volume V |
| 25 | XXV — Cisco Security | `volume-25-cisco-security` | 9 | Volumes III, X |
| 26 | XXVI — Proxmox Virtualization Lab on Dell PowerEdge R640 | `volume-26-proxmox-lab-poweredge-r640` | 9 | Volumes XXII, XXIII |
| 27 | XCIX — Reference Library | `volume-99-reference-library` | 9 | Volumes I–XXVI |

## Ownership and scope control

- Each volume advances only after the prior volume in its dependency chain
  has passed the completed-volume gate defined in `book.yml`.
- Vendor-specific volumes (III, V, XIV–XXIII) are scoped to the dated baseline
  in [SOFTWARE_VERSIONS.md](SOFTWARE_VERSIONS.md) and must be revisited when that
  baseline changes materially.
- [PROJECT_STATUS.md](PROJECT_STATUS.md) tracks technical review and
  lab-validation sign-off against this roadmap.
