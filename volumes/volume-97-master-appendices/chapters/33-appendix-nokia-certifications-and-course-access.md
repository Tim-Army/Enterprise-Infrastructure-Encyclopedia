# Chapter 33: Appendix — Nokia Certifications and Course Access

The **Nokia Service Routing Certification (SRC)** program — the credentials for designing and
operating IP/MPLS service-provider networks on **SR OS** — organized by level, with each
credential's exams and the training and delivery model. The program was verified on **28 July
2026** from **nokia.com** — the same source that anchors
[Volume LXVII — Nokia Certification Tracks](../../volume-67-nokia-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** Training is delivered through **Nokia's Service Routing Certification
program** (nokia.com/networks/training/src) as instructor-led and self-study courses; written exams
are delivered by **Pearson VUE**, and NRS II additionally requires a **hands-on practical lab**
(4A0-N01). Practice runs on **SR OS VSR** (virtual) in lab tools such as containerlab, EVE-NG, or
GNS3.

> **Currency.** Nokia evolves the SRC program with the platform and technologies (Segment Routing,
> SRv6, EVPN, MD-CLI). Confirm the current exams, variants, and recertification terms on
> nokia.com/networks/training/src before registering.

## Free and low-cost resources and entry points

- **[Nokia Service Routing Certification](https://www.nokia.com/networks/training/src/)** — the
  authoritative program, exams, and courses
- **Nokia SR OS documentation** — the platform, classic CLI, MD-CLI, and pySROS
- **SR OS VSR** in containerlab/EVE-NG/GNS3 — hands-on practice for the NRS II lab

## Fees, delivery, and renewal

- **Fees:** the NRS I (4A0-100) and NRS II composite-written exams are **US$125** each via Pearson
  VUE; the practical lab and SRA have their own fees. Confirm current pricing on nokia.com.
- **Delivery:** written exams at **Pearson VUE**; NRS II also requires the **4A0-N01 practical
  lab**.
- **Prerequisites:** **NRS I → NRS II → SRA**; SRA requires NRS II.
- **Validity and renewal:** certifications carry a validity period and are renewed per Nokia policy;
  confirm on the portal.

## The certification map

Verified against nokia.com on 28 July 2026.

| Credential | Level | Exams |
| --- | --- | --- |
| Network Routing Specialist I (NRS I) | Associate | 4A0-100 (IP Networks and Services Fundamentals) |
| Network Routing Specialist II (NRS II) | Professional | Composite Written 4A0-C03 (IS-IS) **or** 4A0-C04 (OSPF) + Practical Lab 4A0-N01 |
| Service Routing Architect (SRA) | Expert | 4A0-112 (requires NRS II) |

## Level focus

- **NRS I:** TCP/IP, IPv4 addressing, Ethernet, packet forwarding, routing-protocol and MPLS/VPN
  fundamentals, and base SR OS configuration (classic CLI and MD-CLI).
- **NRS II:** OSPF and IS-IS, BGP (IBGP/EBGP and policy), MPLS (LDP, RSVP-TE) and Segment Routing,
  and SR OS services (Epipe/VLL, VPLS, VPRN, EVPN) — plus the integrated practical lab.
- **SRA:** end-to-end service-provider design — scalable IGP/BGP, SR transport, and service
  architecture with redundancy and failure analysis.

## Notes

- **NRS II has two components.** A composite written exam (IS-IS or OSPF variant) **and** a 3.5-hour
  practical lab — plan for both.
- **Model-driven.** SR OS exposes a YANG model via MD-CLI, NETCONF, gRPC/gNMI, and pySROS for
  automation.
- **Verify variants.** Choose the composite-written variant (4A0-C03 IS-IS or 4A0-C04 OSPF) that
  matches your network.
- **Related practice** in the encyclopedia: Cisco Service Provider in **Volume XXIX**, Juniper in
  **Volume XXXI**, Arista in **Volume LXII**, and Python for network engineers in **Volume LVIII**.
