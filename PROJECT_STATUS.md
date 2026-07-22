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
| V — VMware Virtualization | 16 | Drafted |
| VI — Enterprise Storage and Data Protection | 9 | Drafted |
| VII — Cloud Infrastructure | 9 | Drafted |
| VIII — Containers and Platform Engineering | 9 | Drafted |
| IX — Infrastructure Automation | 9 | Drafted |
| X — Enterprise Cybersecurity | 9 | Drafted |
| XI — Observability and Enterprise Operations | 9 | Drafted |
| XII — Resilience and Lifecycle Management | 9 | Drafted |
| XIII — Integrated Enterprise Labs | 9 | Drafted |
| XIV — Red Hat Enterprise Linux 10 | 9 | Drafted |
| XV — Forescout Platform and Certifications | 9 | Drafted |
| XVI — Palo Alto Networks Security | 9 | Drafted |
| XVII — AWS Architecture and Security | 9 | Drafted |
| XVIII — Gigamon Network Visibility | 9 | Drafted |
| XIX — Fortinet Network Security | 9 | Drafted |
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
| XCVII — Master Appendices | 2 | Drafted |
| XCIX — Reference Library | 9 | Drafted |

**Total declared chapters:** 287 of 287 drafted (100%). Every volume has a
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
