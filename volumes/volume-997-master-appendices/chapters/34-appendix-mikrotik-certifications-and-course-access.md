# Chapter 34: Appendix — MikroTik Certifications and Course Access

The **MikroTik** certification program — the credentials for deploying **RouterOS** on
RouterBOARD, CHR, and x86 — organized around the MTCNA foundation and the specialist certificates,
with the prerequisite structure and the training and delivery model. The program was verified on
**28 July 2026** from **mikrotik.com** — the same source that anchors
[Volume LXVIII — MikroTik Certification Tracks](../../volume-68-mikrotik-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** Training is delivered by **MikroTik Certified Trainers** at authorized
training centers (instructor-led and online), and the **exam is taken online** at mikrotik.com
after the course. Certificates are **valid three years**. Passing grants a **License Level 4/P1**
for RouterBOARD, CHR, or x86, and practice runs free on the **CHR (Cloud Hosted Router)** virtual
machine.

> **Currency.** RouterOS **v7** changed routing syntax (OSPF, BGP) from v6, and MikroTik has added
> newer certificates (**MTCSWE**, **MTCIPv6E**, **MTCEWE**). Confirm the current certificates,
> prerequisites, and RouterOS version on mikrotik.com/training before registering.

## Free and low-cost resources and entry points

- **[MikroTik Training](https://mikrotik.com/training)** — the authoritative certificate program,
  schedule, and trainers
- **[MikroTik documentation](https://help.mikrotik.com/)** — RouterOS v7, the CLI, the REST API,
  and scripting
- **CHR (Cloud Hosted Router)** — a free RouterOS VM for hands-on practice in GNS3/EVE-NG
- **WinBox / WebFig** — the RouterOS GUIs

## Fees, delivery, and renewal

- **Fees:** set by the training center/trainer (course + exam); confirm with the provider.
- **Delivery:** instructor-led by **MikroTik Certified Trainers**, with the **online exam** at
  mikrotik.com after the course.
- **Prerequisites:** **MTCNA is required for every other certificate**; **MTCINE additionally
  requires MTCRE**.
- **Validity and renewal:** certificates are **valid three years**; renew by re-examination.

## The certification map

Verified against mikrotik.com on 28 July 2026. **MTCNA is the prerequisite for all specialist
certificates.**

| Certificate | Focus | Prerequisite |
| --- | --- | --- |
| MTCNA — Network Associate | RouterOS basics: addressing, DHCP, NAT, firewall, wireless basics, bridging | — |
| MTCRE — Routing Engineer | Static/dynamic routing (OSPF), PTP addressing, tunnels (EoIP/GRE/IPIP) | MTCNA |
| MTCTCE — Traffic Control Engineer | Packet flow, firewall/mangle, NAT, QoS/queues, web proxy | MTCNA |
| MTCWE — Wireless Engineer | 802.11 wireless, CAPsMAN, wireless security | MTCNA |
| MTCEWE — Enterprise Wireless Engineer | Enterprise/CAPsMAN wireless | MTCNA |
| MTCUME — User Management Engineer | PPP/PPPoE, hotspot, RADIUS/User Manager | MTCNA |
| MTCINE — Inter-networking Engineer | BGP, MPLS, VPLS, traffic engineering | MTCNA + MTCRE |
| MTCSE — Security Engineer | Hardening, firewall, IPsec/tunnels | MTCNA |
| MTCSWE — Switching Engineer | VLANs, bridge VLAN filtering, spanning tree, switch-chip | MTCNA |
| MTCIPv6E — IPv6 Engineer | IPv6 addressing, SLAAC/DHCPv6, ND, IPv6 firewall | MTCNA |

## Certificate focus

- **MTCNA:** the RouterOS foundation — the prerequisite that gates all specialist certificates.
- **MTCRE / MTCINE:** the routing path — IGP and tunnels (MTCRE) up to BGP/MPLS/VPLS (MTCINE).
- **MTCTCE:** firewall, NAT, and QoS traffic control.
- **MTCWE / MTCEWE:** wireless and CAPsMAN.
- **MTCUME:** subscriber and guest access (PPPoE, hotspot, RADIUS).
- **MTCSE / MTCSWE / MTCIPv6E:** focused security, switching, and IPv6 add-ons.

## Notes

- **MTCNA first.** Every specialist certificate requires it; MTCINE also requires MTCRE.
- **RouterOS v7.** Routing syntax changed from v6 — study the current version.
- **Practice free on CHR.** The Cloud Hosted Router VM is ideal for labbing the certificates.
- **Automation.** RouterOS v7 adds a REST API alongside scripting and the Ansible
  `community.routeros` collection.
- **Related practice** in the encyclopedia: Cisco in **Volumes XXV and XXIX**, Juniper in **Volume
  XXXI**, Nokia in **Volume LXVII**, and Python for network engineers in **Volume LVIII**.
