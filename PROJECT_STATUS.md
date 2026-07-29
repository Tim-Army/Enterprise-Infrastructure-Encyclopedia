# Project Status

Tracks technical review and lab-validation sign-off against
[ROADMAP.md](ROADMAP.md). A volume is **Drafted** once every chapter is
written and its index and glossary are current. A volume only moves to
**Complete** after it has separately passed the
[technical-review checklist](templates/technical-review-checklist.md) —
drafting and technical review are distinct gates, and drafting a chapter
does not by itself verify every technical claim in it.

| Volume | Chapters | Status |
| --- | --- | --- |
| I — Enterprise Engineering Foundations | 8 | Drafted |
| II — Network Engineering Foundations | 9 | Drafted |
| III — Cisco Enterprise Networking | 9 | Drafted |
| IV — Enterprise Systems Administration | 9 | Drafted |
| V — VMware Virtualization | 20 | Drafted |
| VI — Enterprise Storage and Data Protection | 9 | Drafted |
| VII — Cloud Infrastructure | 9 | Drafted |
| VIII — Containers and Platform Engineering | 9 | Drafted |
| IX — Infrastructure Automation | 10 | Drafted |
| X — Enterprise Cybersecurity | 9 | Drafted |
| XI — Observability and Enterprise Operations | 9 | Drafted |
| XII — Resilience and Lifecycle Management | 9 | Drafted |
| XIII — Integrated Enterprise Labs | 9 | Drafted |
| XIV — Red Hat Enterprise Linux 10 | 9 | Drafted |
| XV — Forescout Platform and Certifications | 9 | Drafted |
| XVI — Palo Alto Networks Security | 12 | Drafted |
| XVII — AWS Architecture and Security | 13 | Drafted |
| XVIII — Gigamon Network Visibility | 9 | Drafted |
| XIX — Fortinet NSE Certification Program | 15 | Drafted |
| XX — Wireshark and Packet Analysis | 9 | Drafted |
| XXI — Ubuntu Server and Cloud 26.04 LTS | 9 | Drafted |
| XXII — Dell OpenManage Enterprise | 9 | Drafted |
| XXIII — Dell iDRAC 9 and 10 Administration | 9 | Drafted |
| XXIV — Dell VxRail | 9 | Drafted |
| XXV — Cisco Security | 9 | Drafted |
| XXVI — Proxmox Virtualization Lab on Dell PowerEdge R640 | 9 | Drafted |
| XXVII — Cisco Data Center | 9 | Drafted |
| XXVIII — Cisco Collaboration | 9 | Drafted |
| XXIX — Cisco Service Provider | 9 | Drafted |
| XXX — Cisco CCDE Network Design | 9 | Drafted |
| XXXI — Juniper Networks Certification Tracks | 9 | Drafted |
| XXXII — Dell Technologies Certification Tracks | 9 | Drafted |
| XXXIII — Microsoft Azure Certification Tracks | 9 | Drafted |
| XXXIV — Google Cloud Certification Tracks | 9 | Drafted |
| XXXV — Zscaler Zero Trust Exchange | 9 | Drafted |
| XXXVI — Windows Server 2025 and Active Directory | 11 | Drafted |
| XXXVII — Microsoft 365 and Modern Work | 11 | Drafted |
| XXXVIII — Microsoft Certifications Beyond Azure | 9 | Drafted |
| XXXIX — CompTIA Certification Tracks | 9 | Drafted |
| XL — ISC2 Certification Tracks | 9 | Drafted |
| XLI — CNCF and Kubernetes Certification Tracks | 9 | Drafted |
| XLII — HashiCorp Certification Tracks | 7 | Drafted |
| XLIII — Offensive Security (OffSec) Certification Tracks | 9 | Drafted |
| XLIV — ISACA Certification Tracks | 9 | Drafted |
| XLV — Splunk Certification Tracks | 9 | Drafted |
| XLVI — NVIDIA Certification Tracks | 9 | Drafted |
| XLVII — Oracle Certification Tracks | 9 | Drafted |
| XLVIII — Databricks Certification Tracks | 9 | Drafted |
| XLIX — Snowflake Certification Tracks | 9 | Drafted |
| L — CrowdStrike Certification Tracks | 9 | Drafted |
| LI — Nutanix Certification Tracks | 10 | Drafted |
| LII — NetBox Community Edition | 9 | Drafted |
| LIII — LibreNMS | 9 | Drafted |
| LIV — OpenTelemetry | 9 | Drafted |
| LV — Prometheus | 9 | Drafted |
| LVI — Infoblox Certification Tracks | 9 | Drafted |
| LVII — Python for Infrastructure and Automation | 9 | Drafted |
| LVIII — Python for Network Engineers | 9 | Drafted |
| LIX — Ansible | 9 | Drafted |
| LX — Rust for Systems and Infrastructure | 9 | Drafted |
| LXI — Cribl Certification Tracks | 9 | Drafted |
| LXII — Arista Certification Tracks | 9 | Drafted |
| LXIII — Public Sector Data Governance (PSDGP) | 9 | Drafted |
| LXIV — HPE Aruba Networking Certification Tracks | 9 | Drafted |
| LXV — Palo Alto Networks Certification Tracks | 9 | Drafted |
| LXVI — F5 Certification Tracks | 9 | Drafted |
| LXVII — Nokia Certification Tracks | 9 | Drafted |
| LXVIII — MikroTik Certification Tracks | 9 | Drafted |
| LXIX — CWNP Certification Tracks | 9 | Drafted |
| LXX — Trellix Certification Tracks | 9 | Drafted |
| LXXI — VMware vSphere 7 | 9 | Drafted |
| LXXII — VMware vSphere 8 | 9 | Drafted |
| LXXIII — Check Point Certification Tracks | 9 | Drafted |
| LXXIV — GIAC (SANS) Certification Tracks | 9 | Drafted |
| LXXV — EC-Council Certification Tracks | 9 | Drafted |
| LXXVI — Okta Certification Tracks | 9 | Drafted |
| LXXVII — CyberArk Certification Tracks | 9 | Drafted |
| LXXVIII — Tenable Certification Tracks | 9 | Drafted |
| LXXIX — Qualys Certification Tracks | 9 | Drafted |
| LXXX — ServiceNow Certification Tracks | 9 | Drafted |
| LXXXI — SUSE Certification Tracks | 9 | Drafted |
| XCVII — Master Appendices | 45 | Drafted |
| XCVIII — Acronyms | 4 | Drafted |
| XCIX — Reference Library | 9 | Drafted |

**Total declared chapters:** 814 of 814 drafted (100%). Every volume has a
full chapter set plus README, INDEX, and GLOSSARY.

## Known issues found during drafting

Authoring agents were instructed to actually execute every hands-on-lab
script rather than only reviewing it, which surfaced and fixed real bugs
before this pass ended. Two additional bugs were found and fixed after
initial drafting, both via the same extract-the-script-and-run-it method:

- Volume X, Chapter 1 (`compute_risk.py`): a validation guard was appended
  after the `if __name__ == "__main__":` call site, causing `NameError`
  instead of the documented output. Fixed by patching the function in
  before `main()` via a `content.replace()` script.
- Volume XII, Chapter 1 (`find_spofs`): removing the graph's entry node
  during SPOF analysis raised `NodeNotFound`, and the documented example
  claimed the wrong node as the single point of failure. Fixed with an
  entry-point guard and a corrected narrative, both re-verified by running
  the exact extracted code.

No volume has undergone a full technical-review-checklist pass yet — that
review (fact-checking version-sensitive claims, running the remaining
labs end-to-end, confirming CLI/API syntax against current vendor
documentation) is the next gate before any volume can be marked
**Complete** or included in a tagged release per
[RELEASE_PROCESS.md](RELEASE_PROCESS.md).
