# Chapter 36: Appendix — Trellix Certifications and Course Access

The **Trellix** certification program — the credentials for administering, detecting, and
responding with Trellix's endpoint, network, data, and SecOps platform — organized by product, with
the lineage, the certification model, and the training and delivery model. The program was verified
on **28 July 2026** from **trellix.com** — the same source that anchors
[Volume LXX — Trellix Certification Tracks](../../volume-070-trellix-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** Trellix was formed in 2022 from **McAfee Enterprise + FireEye**, and its
**Trellix Education Services** (successor to McAfee's education organization) delivers
instructor-led and on-demand product courses with hands-on labs, plus **per-product Certified
Product Specialist** certifications. Exams have historically been delivered through Pearson VUE
(McAfee **MA0-###** codes). Practice happens on authorized product/lab instances, and the
**OpenDXL** automation SDK is free and open source.

> **Currency.** The program is **in transition** from McAfee to Trellix branding, and the portfolio
> is consolidating into the **XDR** platform (Helix + DXL). Course names and exam codes may differ
> from historical McAfee references. Confirm the current certification catalog and codes on
> trellix.com/services/education before registering.

## Free and low-cost resources and entry points

- **[Trellix Education Services](https://www.trellix.com/services/education/)** — the authoritative
  courses and certifications
- **Trellix product course descriptions** (trellix.com/assets/course-descriptions) — per-product
  course outlines
- **[OpenDXL](https://www.opendxl.com/)** — the free, open-source DXL client and Python SDK
- Authorized product/lab instances (ePO, ENS, EDR, Helix) for hands-on practice

## Fees, delivery, and renewal

- **Fees:** per-course and per-exam fees via Trellix Education Services / the exam provider; confirm
  current pricing on trellix.com.
- **Delivery:** instructor-led and on-demand courses with labs; certification exams via the exam
  provider (historically Pearson VUE for McAfee MA0-### exams).
- **Prerequisites:** ePO underpins the endpoint-managed products; product courses have their own
  recommended experience.
- **Validity and renewal:** certifications carry a validity period; renew per Trellix policy.

## The certification map

Verified against trellix.com on 28 July 2026. **Per-product Certified Product Specialist** model
(legacy McAfee exam codes shown where known; verify current codes on trellix.com).

| Product | Certification focus | Legacy exam code |
| --- | --- | --- |
| ePolicy Orchestrator (ePO) | Central management (System Tree, policy, tasks, reporting) | MA0-101 |
| Endpoint Security (ENS) | Endpoint protection (Threat Prevention, Firewall, Web Control, ATP) | MA0-100 |
| Endpoint Detection and Response (EDR) | Detection, hunting, investigation, response | — |
| Network Security (IPS) | Inline network detection/prevention | MA0-104 (IPS) |
| Advanced Threat Defense (ATD) | Malware sandboxing / verdicts | — |
| Data Loss Prevention (DLP) | Endpoint and network data protection | — |
| Helix | SecOps / SIEM / XDR | — |

## Product focus

- **ePO:** the central console most Trellix endpoint products manage through — the foundation.
- **ENS:** integrated endpoint protection with reputation-based Adaptive Threat Protection.
- **EDR:** real-time and historical hunting, process-story investigation, and reactions.
- **Network Security / ATD:** inline IPS plus sandboxing, with verdicts shared via DXL.
- **DLP:** data classification and channel-based protection with incident review.
- **Helix / XDR:** cross-domain correlation, case management, and playbook/SOAR response.

## Notes

- **McAfee → Trellix.** Verify current course names and exam codes on trellix.com; legacy McAfee
  MA0-### references are in transition.
- **ePO first.** Most endpoint products manage through ePO — it is the natural starting point.
- **OpenDXL is open source.** The DXL fabric's client and Python SDK are freely available for
  automation and integration.
- **Defensive scope.** The platforms are defensive; study and practice authorized administration,
  detection, and response only.
- **Related practice** in the encyclopedia: CrowdStrike in **Volume L**, Palo Alto Networks in
  **Volumes XVI and LXV**, Cisco Security in **Volume XXV**, and Enterprise Cybersecurity in
  **Volume X**.
