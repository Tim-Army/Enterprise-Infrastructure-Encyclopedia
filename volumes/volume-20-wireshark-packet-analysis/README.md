# Volume XX — Wireshark and Packet Analysis

> Enterprise packet capture engineering and protocol analysis with
> Wireshark and `tshark`: capture placement, the analyst interface and
> workflow, protocol-by-protocol dissection from Ethernet through TLS,
> and security investigation and automation, mapped to the WCA-101
> certification blueprint.

## Overview

Volume XX teaches packet capture and analysis as an enterprise discipline,
not just a tool tutorial. It builds from installing Wireshark and `tshark`
with least-privilege capture access and evidentiary handling discipline,
through where and how to capture at scale, through the analyst interface
and filtering skills that make a large capture tractable, through
protocol-by-protocol dissection of the stack every other volume in this
encyclopedia assumes, to security investigation, command-line automation,
and certification-aligned readiness.

Per [ROADMAP.md](../../ROADMAP.md), this volume depends on Volume II
(Network Engineering Foundations) for OSI/TCP-IP model and protocol
fundamentals, and is itself the encyclopedia's dedicated deep-dive on
packet-level observation — the ground-truth analysis technique every other
volume's troubleshooting sections assume is available when logs and
metrics are insufficient.

The volume is organized in three parts:

- **Chapters 01–03** establish the foundation: installation and
  evidentiary handling, enterprise capture engineering (TAPs, mirrors,
  ring buffers), and the Wireshark interface, profiles, and filtering
  workflow every later chapter depends on.
- **Chapters 04–07** work bottom-up through the protocol stack: Ethernet/
  ARP/IPv4/ICMPv4, IPv6/ICMPv6/UDP/DHCP/DNS, TCP reliability and
  performance, and application-protocol/TLS analysis.
- **Chapters 08–09** apply that protocol knowledge to security
  investigation and `tshark`-based automation, then close with WCA-101
  certification domain mapping and an integrated enterprise capstone lab.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md). Each hands-on lab
is a reproducible, disposable exercise with a stated objective,
prerequisites, numbered steps, expected results, a negative test, and
cleanup instructions.

## Chapters

1. [Packet Analysis Foundations, Wireshark Installation, and Evidence](chapters/01-packet-analysis-foundations-wireshark-installation-and-evidence.md) — what packet analysis reveals, Wireshark's architecture, platform installation with non-administrative capture rights, pcap vs. pcapng, and evidentiary handling.
2. [Enterprise Capture Engineering, Taps, Mirrors, and Ring Buffers](chapters/02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md) — SPAN/mirror ports vs. TAPs, network packet brokers, capture filters, `dumpcap` ring-buffer rotation, and remote capture.
3. [Wireshark Interface, Profiles, Filters, and Analysis Workflows](chapters/03-wireshark-interface-profiles-filters-and-analysis-workflows.md) — the three-pane interface, display filter syntax, configuration profiles, coloring rules, custom columns, and core statistics workflows.
4. [Ethernet, ARP, IPv4, and ICMPv4 Analysis](chapters/04-ethernet-arp-ipv4-and-icmpv4-analysis.md) — Ethernet II framing, ARP and spoofing detection, IPv4 header fields, and ICMPv4 diagnostics and error reporting.
5. [IPv6, ICMPv6, UDP, DHCP, and DNS Analysis](chapters/05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) — IPv6 headers and extension headers, Neighbor Discovery Protocol, UDP, DHCP DORA/DHCPv6, and DNS query/response analysis.
6. [TCP Reliability, Flow Control, and Performance Analysis](chapters/06-tcp-reliability-flow-control-and-performance-analysis.md) — the TCP handshake, expert-analysis flags (retransmission, duplicate ACK, zero window), window scaling, and throughput/RTT graphing.
7. [Application Protocol, TLS, and Service-Response Analysis](chapters/07-application-protocol-tls-and-service-response-analysis.md) — HTTP/1.1 and HTTP/2 dissection, TLS 1.2/1.3 handshake analysis, TLS decryption with session-key logs, and service response-time measurement.
8. [Security Investigation, Command-Line Analysis, and Automation](chapters/08-security-investigation-command-line-analysis-and-automation.md) — `tshark` scripting, attack-pattern detection, `editcap`/`mergecap`/`capinfos`, structured export, and capture sanitization.
9. [WCA-101 Certification Readiness and Enterprise Capstone](chapters/09-wca-101-certification-readiness-and-enterprise-capstone.md) — certification domain mapping, a personal readiness checklist, and an integrated enterprise capstone lab spanning every prior chapter.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Wireshark 4.4.x
(2026-07). Update that file, not individual chapters, when the baseline
changes.

## Certification alignment

Per [CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md), this
volume maps to the Wireshark Certified Analyst Program's WCA-101
credential. Chapter 09 provides a domain-to-chapter mapping and readiness
checklist; always confirm the current official blueprint directly with the
certifying program before scheduling an exam.

### The exam

| Term | Detail |
| --- | --- |
| Questions | 50–60 |
| Duration | 120 minutes |
| Cost | $349 per attempt |
| Delivery | Kryterion Webassessor — test center or online with secure browser and live proctor |
| Retakes | One attempt every 15 days |
| Validity | Three years |

### Domain weights, mapped to this volume

Weights are from the published WCA-101 objectives; they total 100%.

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Utilize key features of Wireshark | 10% | 01, 03 |
| 2.0 Utilize different methods of capturing traffic | 10% | 02 |
| 3.0 Filter traffic using capture and display filters | 12% | 03 |
| 4.0 Configure, adapt, and use the interface for different scenarios | 5% | 03 |
| 5.0 Identify and explain common network protocols | **43%** | 04–07 |
| 6.0 Troubleshoot common issues with those protocols | 20% | 06–08 |

**Two numbers should drive the study plan.** Protocol identification at
43% is nearly half the exam, and within it **TCP alone is 17%, scored
separately** — more than any other single topic and more than domains 1,
2 and 4 combined. [Chapter 06](chapters/06-tcp-reliability-flow-control-and-performance-analysis.md)
is therefore the highest-value chapter in this volume for exam purposes,
with the remaining 27% of protocol content spread across
[Chapters 04](chapters/04-ethernet-arp-ipv4-and-icmpv4-analysis.md),
[05](chapters/05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) and
[07](chapters/07-application-protocol-tls-and-service-response-analysis.md).

Conversely, interface configuration is 5%. It is worth knowing and quick
to learn, but it is not worth extended study time.

### Practice: the tool is free, the captures are the constraint

Wireshark inverts the usual problem. Every other volume in this
encyclopedia needs licenses, trial windows, or hosted sandboxes to get
hands-on; here the software is free, open source, and installs in
minutes. What a candidate actually lacks is **interesting traffic** —
captures containing the retransmissions, resets, malformed headers, and
failure patterns the exam asks you to recognize.

| Source | What it gives you |
| --- | --- |
| [Wireshark sample captures wiki](https://wiki.wireshark.org/SampleCaptures) | The canonical library, organized by protocol — the first place to look for a specific protocol's normal and abnormal behavior |
| [malware-traffic-analysis.net](https://www.malware-traffic-analysis.net/) | Dated exercises with real infection traffic, each posed as a question with published answers — the closest thing to graded practice |
| [Netresec public PCAP list](https://www.netresec.com/?page=PcapFiles) | An aggregated index of publicly available capture repositories |
| Your own network | Irreplaceable for [Chapter 02](chapters/02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)'s capture engineering — placement, SPAN versus TAP, and ring buffers cannot be learned from someone else's file |

**Generate your own failures.** The most efficient practice is to break
something deliberately and capture it: block a port mid-transfer to
produce retransmissions, force a TLS version mismatch, point a resolver
at a dead server. Reading a clean capture teaches protocol structure;
capturing a broken one teaches the diagnostic reasoning domain 6 tests at
20%.

Note that the certification is delivered by the **Wireshark Foundation**,
the nonprofit steward of the tool, and its official training partners are
named on the certification page. Because the credential is comparatively
new, third-party practice material is thinner than for older
certifications — the published objectives PDF is the authoritative study
map, and it is more specific than most vendors publish.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-20-wireshark-packet-analysis

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-20-wireshark-packet-analysis/chapters/06-tcp-reliability-flow-control-and-performance-analysis.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
