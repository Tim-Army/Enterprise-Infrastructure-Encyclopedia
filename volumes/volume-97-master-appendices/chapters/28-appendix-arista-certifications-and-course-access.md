# Chapter 28: Appendix — Arista Certifications and Course Access

The **Arista Certified Engineer (ACE)** program — the credentials for operating,
engineering, and automating **Arista EOS** networks managed by **CloudVision** — organized
by track and tier, with each credential's focus, topic areas, and the training and delivery
model. The program was **revised on 1 June 2025** into a Learning Track model and was
verified on **27 July 2026** from **training.arista.com** — the same source that anchors
[Volume LXII — Arista Certification Tracks](../../volume-62-arista-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works at Arista.** Training and certification are delivered through **Arista
Academy** (training.arista.com) as **self-paced** learning tracks with **hands-on labs** and
proctored exams. Each track combines self-study hours with lab time; practice also runs free
on **cEOS/vEOS** images (containerlab) or **Arista Test Drive**. The **All-Access Pass**
bundles every track for an annual fee with one free exam attempt per subtrack.

> **Currency.** The ACE program was **revised on 1 June 2025** (a post-cutoff change — verify
> against the source, do not trust model memory) and Arista continues to revise it as EOS and
> CloudVision evolve. Confirm the current tracks, blueprints, and recertification policy on
> training.arista.com before registering.

## Free resources and entry points

- **[Arista Academy](https://www.training.arista.com/)** (training.arista.com) — the
  authoritative catalog: learning tracks, blueprints, and exams
- **[arista.com](https://www.arista.com/)** — EOS and CloudVision product documentation
- **cEOS / vEOS** images (containerlab) and **Arista Test Drive** — free hands-on practice
- **Blueprints** — published per track (e.g., an ACEL1 blueprint) as the study scope

## Fees, delivery, and renewal

- **Fees:** approximately **$495** (Network Foundations) and **$1,995** per Specialist/
  Automation track; **All-Access Pass** approximately **$4,995/year** (all tracks, lab hours
  per subtrack, one free exam attempt). Confirm current pricing on training.arista.com.
- **Delivery:** **self-paced** through Arista Academy — self-study hours plus **hands-on
  labs** — with proctored exams. Blueprints are published per track.
- **Prerequisites:** everyone starts with **Network Foundations (Associate)**; Specialist and
  Automation tracks build on that base.
- **Validity and renewal:** an **ACE recertification policy** took effect **1 June 2025** —
  confirm the current terms before you certify.

## The certification map

Verified against training.arista.com on 27 July 2026. Tiers: **Associate (L1) → Specialist
(L3) → Professional (L4)**.

| Track | Tier(s) | Specialization(s) | Focus |
| --- | --- | --- | --- |
| Network Foundations | Associate (L1) | — | EOS fundamentals, switching, routing, protocols |
| Data Center | Specialist (L3) | Operations, Engineering | Leaf-spine, MLAG, EVPN/VXLAN |
| Campus | Specialist (L3) | Operations, Engineering | Campus fabric, PoE, 802.1X, CloudVision |
| WAN Routing | Specialist (L3) | MPLS Core | MPLS/LDP, L3VPN |
| Automation | Specialist → Professional (L4) | Foundations, Advanced | eAPI/pyeapi, Ansible, AVD, CloudVision, Git |

Passing all **Automation** Specialist specializations (Foundations + Advanced) earns the
**Professional (Automation)** accreditation.

## Topic areas

- **Network Foundations (Associate):** EOS architecture and CLI; VLANs and trunking; MLAG
  basics; IP routing (static, OSPF, BGP); spanning tree; management and eAPI.
- **Data Center — Operations:** leaf-spine operation; MLAG; interface/port-channel
  management; streaming telemetry; monitoring and troubleshooting of an EVPN/VXLAN fabric.
- **Data Center — Engineering:** underlay (eBGP/OSPF) design; VXLAN VTEP/VNI; BGP EVPN
  control plane; anycast gateway (IRB); multi-tenancy and fabric design.
- **Campus — Operations and Engineering:** campus fabric; PoE; 802.1X/authentication;
  wired/wireless; CloudVision provisioning; MSS segmentation.
- **WAN Routing — MPLS Core:** MPLS forwarding and LDP; MP-BGP L3VPN (VPNv4) and VRFs;
  provider/core routing design.
- **Automation — Foundations and Advanced:** eAPI (JSON-RPC) and pyeapi; Ansible
  `arista.eos`; Jinja templates and Git config-as-code; **AVD** fabric generation;
  CloudVision-governed deployment.

## Notes

- **Start with Network Foundations.** It is the Associate base for every Specialist and
  Automation track.
- **Blueprints are the study scope.** Follow the matching Arista Academy track and blueprint.
- **Practice is free** on cEOS/vEOS (containerlab) or Arista Test Drive.
- **Recertify** per the 1 June 2025 policy; track new tracks as Arista launches them.
- **Related practice** in the encyclopedia: Cisco in **Volumes III, XXV, XXVII–XXX**, Juniper
  in **Volume XXXI**, NetBox in **Volume LII**, Python for network engineers in **Volume
  LVIII**, and Ansible in **Volume LIX**.
