# Chapter 09: WCA-101 Certification Readiness and Enterprise Capstone

![Lab flow for this chapter: a bounded ring-buffer capture on the lab host records a reproduced DHCP renewal, DNS resolution, and HTTPS request alongside an authorized port scan simulating the reported symptom; DHCP, DNS, and TLS all confirm working as expected, leaving the scan as the explanation once the detection one-liner identifies the scanning host by its high distinct-port count. As a negative test, the scanning host's traffic is filtered out entirely and the detection command re-run against what remains; no high-count scan signature remains, confirming the original detection was correctly attributable to the scanning host specifically.](../../../diagrams/volume-20-wireshark-packet-analysis/chapter-09-capstone-investigation-report-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: an integrated investigation combining capture engineering, protocol analysis, and scan detection against one realistic 'slow and occasionally unreachable' scenario.*

## Learning Objectives

- Map this volume's eight technical chapters to the general skill domains
  a foundational packet-analysis certification such as WCA-101 evaluates.
- Identify study and practice priorities for each domain using the
  chapters, filters, and labs already completed in this volume.
- Plan and execute an integrated capstone investigation that combines
  capture engineering, interface workflows, protocol analysis, TCP
  performance analysis, TLS/application analysis, and command-line
  security investigation in a single exercise.
- Produce a professional-quality analysis report from a capstone capture,
  suitable as a work sample for an enterprise packet-analysis role.

## Theory and Architecture

This chapter closes the volume in two parts. The first maps the technical
material from Chapters 01–08 to the general domain structure a
foundational, vendor-neutral packet-analysis certification program is
built around, so that certification preparation becomes a matter of
targeted review rather than re-reading the volume linearly. The second is
a capstone lab that requires applying skills from every prior chapter
against a single, realistic capture scenario — the same kind of integrated
problem an enterprise analyst encounters in practice, where a single
investigation rarely stays inside one protocol layer.

### About WCA-101 and this chapter's scope

[CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) maps
this volume to the Wireshark Certified Analyst Program's WCA-101
credential as the relevant current certification for packet-analysis
practitioners. Consistent with this encyclopedia's editorial standards
(EDITORIAL_STANDARDS.md), this chapter describes general blueprint
*domains* — the broad skill areas any competent foundational
packet-analysis certification would reasonably evaluate, and which this
volume's chapters were organized to build toward — without reproducing
any proprietary exam questions or licensed courseware. **Always confirm
the current official blueprint, exam objectives, and registration details
directly from the Wireshark Certified Analyst Program before scheduling an
exam**; certification content and structure change independently of this
encyclopedia's release cycle.

### Domain-to-chapter mapping

| Domain | What it evaluates | Primary chapters |
| --- | --- | --- |
| Capture fundamentals and tooling | Installing and permissioning Wireshark/`tshark`, capture file formats, evidentiary handling | [Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md) |
| Capture engineering | TAPs, SPAN/mirror ports, capture filters, ring buffers, remote capture | [Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md) |
| Analyst workflow and interface proficiency | Panes, profiles, display filters, coloring rules, statistics views | [Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md) |
| Core protocol analysis (IPv4 family) | Ethernet, ARP, IPv4, ICMPv4 | [Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md) |
| Core protocol analysis (IPv6 family and name/address services) | IPv6, ICMPv6/NDP, UDP, DHCP, DNS | [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) |
| Transport-layer reliability and performance | TCP handshake, retransmission/duplicate-ACK/zero-window analysis, window scaling, throughput | [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md) |
| Application-layer and encrypted-traffic analysis | HTTP/HTTP2, TLS handshake analysis, TLS decryption, service response time | [Chapter 07](07-application-protocol-tls-and-service-response-analysis.md) |
| Security investigation and automation | Attack-pattern recognition, `tshark` scripting, file utilities, sanitization | [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md) |

### Preparation priorities by domain

- **Capture fundamentals and engineering (Chapters 01–02).** Be able to
  explain, without notes, the difference between `dumpcap`, `tshark`, and
  the GUI; pcap vs. pcapng; and why an oversubscribed SPAN port or
  aggregating TAP drops packets silently. These are conceptual questions
  more than syntax questions, and are frequently under-reviewed by
  candidates who focus only on filter syntax.
- **Filter syntax fluency ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md) onward).** Practice writing display
  filters from a plain-language description without autocomplete — the
  ability to construct `tcp.flags.syn==1 && tcp.flags.ack==0` from memory,
  not just recognize it, is the single most transferable exam-readiness
  skill this volume builds.
- **Field-name recall for core protocols (Chapters 04–07).** Build a
  personal quick-reference of the field names used most often in this
  volume's labs (`ip.ttl`, `icmp.type`, `dns.flags.rcode`,
  `tcp.analysis.retransmission`, `tls.handshake.type`) and drill until
  recall is immediate.
- **Expert-flag interpretation ([Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md)).** Be able to distinguish a
  retransmission from a duplicate ACK from a zero-window condition purely
  from a description of the symptom, and state which side of the
  connection each points an investigation toward.
- **Command-line equivalence ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)).** For every GUI workflow
  practiced in this volume, be able to state the `tshark` equivalent — many
  foundational packet-analysis assessments test whether a candidate
  understands that the GUI and CLI share the same dissection engine, not
  just GUI menu navigation.

## Design Considerations

- **Study plan sequencing should mirror investigative order, not chapter
  order, in review.** In practice, an analyst starts with capture
  placement and scope ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)), moves to interface/workflow setup
  ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)), then protocol analysis (Chapters 04–07), then
  security/automation ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)) — reviewing in this investigative
  sequence during final preparation reinforces how the domains connect
  rather than treating them as isolated topics.
- **Practice against real captures, not just field-name flashcards.**
  Recognizing `tcp.analysis.zero_window` in a list is a different skill
  from noticing a zero-window condition while scanning an unfamiliar
  capture under time pressure; the capstone lab below is designed to
  exercise the latter.
- **Time management during hands-on assessment mirrors time management
  during a real investigation.** Triage with Protocol Hierarchy and
  Conversations ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)) before drilling into individual packets,
  exactly as recommended for a first pass on any unfamiliar capture.
- **Certification currency has a shelf life independent of this
  volume.** Because [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md)
  records this volume's Wireshark 4.4.x baseline as of 2026-07, and
  certification blueprints revise independently, re-verify the current
  blueprint before an exam attempt scheduled well after that date.

## Implementation and Automation

### Building a personal domain checklist

Convert the domain table above into a tracked checklist, marking each
sub-skill only after demonstrating it without reference material:

```text
[ ] Explain dumpcap/tshark/GUI separation and why it is a security boundary
[ ] State pcap vs. pcapng differences from memory
[ ] Explain SPAN oversubscription and aggregating-TAP drop behavior
[ ] Write five display filters from plain-language descriptions, unaided
[ ] Create a configuration profile and a coloring rule from a cold start
[ ] Decode an ARP exchange and state the ARP-spoofing signature
[ ] Decode IPv4 TTL/fragmentation fields and explain traceroute's ICMP mechanism
[ ] Decode an NDP exchange and relate it to ARP
[ ] Trace a DHCP DORA exchange and identify a rogue-server signature
[ ] Interpret DNS response codes and state when DNS uses TCP
[ ] Read a TCP handshake's negotiated options
[ ] Identify retransmission, duplicate ACK, and zero-window from a description
[ ] Compute a bandwidth-delay product and explain window-limited throughput
[ ] Read a TLS 1.2 vs. TLS 1.3 handshake and count round trips
[ ] Configure and validate TLS decryption with a session-key log
[ ] Write a tshark one-liner to extract fields to CSV
[ ] Detect a port scan and a SYN flood pattern from a capture
```

### Rapid protocol-field drill script

```bash
# Present a random field name from this volume's core set and self-test
# recall of its meaning before checking the chapter reference.
fields=(ip.ttl ip.flags.mf icmp.type arp.opcode ipv6.nxt icmpv6.type
        dhcp.option.dhcp dns.flags.rcode tcp.analysis.retransmission
        tcp.analysis.zero_window tls.handshake.type http.time)
echo "${fields[$RANDOM % ${#fields[@]}]}"
```

## Validation and Troubleshooting

- **Confident on filter syntax but slow identifying which filter to
  write.** This is a triage-skill gap, not a syntax gap — practice starting
  from Statistics views ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)) before writing any filter, so filter
  construction follows a hypothesis rather than searching blindly.
- **Strong on individual protocol chapters but weak on cross-layer
  scenarios.** Revisit the capstone lab below and any multi-chapter labs;
  real investigations, and well-designed assessments, rarely stay inside
  one protocol layer.
- **Comfortable in the GUI but unable to produce the `tshark`
  equivalent.** Deliberately re-do at least one lab from each of Chapters
  04–08 command-line-only, with the GUI closed, to confirm the
  equivalence is internalized rather than assumed.
- **Uncertain which domain a weak area belongs to.** Use the domain table
  above to locate the owning chapter, then re-run that chapter's Hands-On
  Lab rather than only re-reading the Theory and Architecture section —
  this volume's labs are designed to be the retention mechanism.

## Security and Best Practices

- **Do not seek out or use leaked or reproduced exam questions from any
  source.** Beyond the integrity issue, they are an unreliable and
  frequently outdated proxy for the actual current blueprint; the domain
  review and capstone approach in this chapter is designed to build the
  underlying skill instead.
- **Practice only against captures you are authorized to generate or
  possess.** Every lab in this volume uses traffic the analyst generates
  in their own lab or captures with explicit authorization — apply the
  same standard to any additional self-directed practice.
- **Maintain the evidentiary and sanitization discipline from Chapters 01
  and 08 even in practice captures**, so the habit is automatic before it
  matters in a real investigation.
- **Treat certification as a checkpoint, not the end state.** The
  underlying skill — reading a capture accurately under time pressure and
  reasoning from observed bytes rather than assumption — is what an
  enterprise role actually requires; keep practicing against real
  production and lab captures after certification.

## References and Knowledge Checks

**References**

- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this encyclopedia's mapping of Volume XX to the WCA-101 credential and
  pointer to the controlling vendor source.
- [Wireshark Certified Analyst Program](https://www.wireshark.org/certifications/) — official current blueprint,
  exam objectives, and registration (verify directly with the program
  before scheduling an exam).
- Chapters 01–08 of this volume, and their individual References and
  Knowledge Checks sections, for domain-specific source material.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. Which two chapters primarily map to the "capture engineering" domain,
   and what is the single concept from that domain most often
   under-reviewed by candidates who focus only on filter syntax?
2. Why does practicing filter construction from Statistics-view triage
   produce better exam and real-investigation performance than memorizing
   filters in isolation?
3. Why should a candidate re-verify the official WCA-101 blueprint before
   an exam attempt rather than relying solely on this chapter's domain
   table?
4. Name one command-line equivalence a candidate should be able to state
   for a GUI workflow practiced in [Chapter 07](07-application-protocol-tls-and-service-response-analysis.md).

## Hands-On Lab

This chapter closes the volume with **WCA-101 readiness and a capstone** — a domain-weighted
self-check, an integrative investigation that exercises every domain, and a written
**Analysis Exercise** that captures a repeatable methodology. All steps are runnable
`tshark` work. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.3** — `tshark` and a rich, realistic capture that
contains a genuine problem (a throttled/broken transfer or an infection capture from
malware-traffic-analysis.net). **Cost:** none.

### Lab 9.1 — Domain-weighted readiness self-check (Topic: Exam readiness)

**Objective:** Prove hands-on coverage of each WCA-101 domain, weighted by exam value.

```bash
# 5.0 Protocols 43% (TCP 17%) — the highest-value skills:
tshark -r cap.pcapng -q -z io,phs                                 # protocols present (D5)
tshark -r cap.pcapng -Y "tcp.analysis.flags" -q -z expert         # TCP problems (D5 TCP + D6)
# 3.0 Filters 12% / 2.0 Capture 10% / 1.0 Features 10% / 4.0 Interface 5%:
tshark -r cap.pcapng -Y "tcp.port in {80 443}" -c 5               # display filter (D3)
capinfos cap.pcapng                                               # capture features/metadata (D1/D2)
```

**Expected result:** you can demonstrate each domain against a real capture — protocol
identification and TCP analysis (the 43%/17% core), filtering, capture handling, and file
features — confirming your practice is weighted the way the exam is, not spread evenly.

**Negative test:** study all six domains equally; you under-invest in TCP (17% alone) and
protocols (43%) while over-investing in the 5% interface domain — the weights are an
instruction about where to spend time.

**Cleanup:** none (read-only).

### Lab 9.2 — Capstone investigation: triage a real problem (Topic: Integrative analysis)

**Objective:** Work one capture end-to-end, from profile to root cause, using every layer.

```bash
# 1. Profile the capture:
tshark -r case.pcapng -q -z io,phs
tshark -r case.pcapng -q -z conv,ip | sort -k7 -rn | head
# 2. Follow the suspect conversation down the stack:
tshark -r case.pcapng -q -z expert                                # protocol-level problems
tshark -r case.pcapng -Y "tcp.analysis.retransmission || tcp.analysis.zero_window" | head
tshark -r case.pcapng -Y "tls.handshake.type==1" -T fields -e tls.handshake.extensions_server_name | head
tshark -r case.pcapng -Y "dns.flags.rcode != 0 && dns.flags.response==1" | head
```

**Expected result:** you localize the fault — e.g. retransmissions pointing to loss, a
zero-window pointing to a stalled receiver, a DNS ServFail pointing to resolution, or an
anomalous SNI/beacon pointing to compromise — by working top statistics → conversation →
protocol layers in order, which is exactly the reasoning the WCA-101 troubleshooting domain
rewards.

**Negative test:** jump straight to the packet you suspect without profiling; you anchor on a
guess and miss the dominant problem the protocol-hierarchy and expert views would have named
first — profile before you dive.

**Cleanup:** none (read-only).

### Lab 9.3 — Analysis Exercise: a repeatable methodology (Topic: Synthesis)

**Objective:** Write down the method so any capture yields a defensible conclusion — the
analyst's real deliverable, not a single command.

> **Scenario.** A user reports "the application is slow and sometimes fails." You are handed a
> capture from a TAP near the client and asked for a root-cause answer, not a guess.

Work through and **write down** your method:

1. **Establish the capture's validity** — capture point, time window, drops (`capinfos`), and
   an evidence hash (Chapter 01).
2. **Profile** — protocol hierarchy, top conversations, expert summary (what dominates,
   what is broken).
3. **Isolate** — filter to the affected client/server conversation.
4. **Descend the stack** — DNS resolved? TCP handshake clean? Retransmissions / zero window /
   resets? TLS negotiated? `http.time` vs TCP RTT (network vs server)?
5. **Attribute** — assign the delay/failure to a specific layer and party (network loss,
   receiver flow control, server think-time, name resolution, or security event).
6. **Report** — the evidence (filters + counts + RTT/throughput numbers) that supports the
   conclusion, so it is reproducible by someone else.

**Expected result:** a written methodology that turns any capture into a layered,
evidence-backed root cause — the difference between an analyst who *guesses* and one who
*proves*, which is what both the exam and real incident response reward.

**Negative test:** conclude "it's the network" without descending the stack; if `http.time`
shows server think-time and TCP RTT is a millisecond, that conclusion is wrong and the method
would have caught it — the discipline of the method is what prevents the confident wrong
answer.

**Cleanup:** none (methodology artifact).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This volume built from installation and evidentiary handling ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md))
through capture engineering ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)), interface and filter fluency
([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)), core protocol analysis across the IPv4 and IPv6 families
(Chapters 04–05), transport-layer reliability and performance (Chapter
06), application and encrypted-traffic analysis ([Chapter 07](07-application-protocol-tls-and-service-response-analysis.md)), and
security investigation and automation ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)). Certification
readiness for a foundational credential such as WCA-101 is a matter of
targeted review against the domain table above and repeated practice
against real captures — this chapter's capstone is deliberately built to
require every domain at once, because that is how packet-analysis problems
actually present in enterprise practice.

- [ ] Can map each of Chapters 01–08 to a general certification domain.
- [ ] Completed a personal domain checklist and can demonstrate each item
      without reference material.
- [ ] Can state the command-line (`tshark`) equivalent for GUI workflows
      practiced throughout the volume.
- [ ] Completed the integrated capstone lab, including the negative test
      and cleanup.
- [ ] Produced a professional-quality analysis report from the capstone
      capture.
- [ ] Confirmed the current official WCA-101 blueprint independently
      before treating this chapter as exam preparation.
