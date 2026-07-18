# Volume XVIII Glossary

Definitions for terms introduced in **Volume XVIII — Gigamon Network
Visibility**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Adaptive Packet Filtering / Application Session Filtering (ASF)** — A
GigaSMART capability that filters traffic based on identified application
or session characteristics rather than static header fields alone,
allowing a map to select traffic by application even when it cannot be
distinguished by IP address or port. Introduced in Chapter 06.

**Application Metadata Intelligence (AMI)** — A GigaSMART application that
inspects sessions, identifies the application in use, and exports
IPFIX-based metadata records describing session attributes to a
consuming tool, without requiring full packet payload delivery.
Introduced in Chapter 06.

**Box/slot/port addressing** — GigaVUE-OS's convention for identifying a
physical port (for example, `1/1/x1`), used consistently across CLI
commands, Flow Mapping definitions, and GigaVUE-FM's node inventory.
Introduced in Chapter 02.

**Cluster (GigaVUE)** — A group of GigaVUE nodes interconnected over stack
ports and jointly managed as one logical fabric, allowing Flow Mapping to
span node boundaries. Introduced in Chapter 02.

**De-duplication** — A GigaSMART application that identifies and drops
duplicate copies of the same packet, commonly produced by overlapping TAP
or SPAN coverage, reducing tool load without discarding unique traffic.
Introduced in Chapter 06.

**Fail-closed** — An inline tool group's configured behavior on heartbeat
failure in which traffic is blocked rather than allowed to pass
uninspected, prioritizing inspection assurance over availability.
Introduced in Chapter 07.

**Fail-open (bypass)** — An inline tool group's configured behavior on
heartbeat failure in which traffic is routed around the failed tool,
restoring connectivity at the cost of losing that tool's inspection for
the outage's duration. Introduced in Chapter 07.

**First-level map / second-level map** — The two-stage Flow Mapping
pattern in which a first-level map performs initial filtering close to
the acquisition point, and a second-level map takes GigaSMART-processed
output and delivers it to final tool destinations. Introduced in Chapter
05.

**Flow Mapping** — GigaVUE-OS's packet-forwarding rule engine, which binds
source ports to destination ports through an ordered set of pass/drop
rules, authored node-by-node through the CLI or fabric-wide through
GigaVUE-FM. Introduced in Chapter 01 and detailed in Chapter 05.

**Gigamon Certified Professional (GCP)** — Gigamon's vendor certification
program validating hands-on competence implementing Gigamon products,
commonly paired with the Gigamon Certified Professional Bootcamp (GCPB)
training course. Introduced in Chapter 09.

**GigaSMART** — The traffic-intelligence processing engine hosted on
GigaSMART-capable node platforms, performing packet slicing, masking,
deduplication, header stripping, SSL/TLS decryption, and Application
Metadata Intelligence generation. Introduced in Chapter 01 and detailed in
Chapter 06.

**GigaStream** — A logical, load-balanced bundle of tool ports that
distributes flows across member ports using a consistent hashing method,
solving tool-port oversubscription without requiring the Flow Map itself
to be re-authored as capacity is added. Introduced in Chapter 01 and
detailed in Chapter 05.

**GigaVUE Cloud Suite** — Gigamon's collective term for cloud-native and
virtualization-platform visibility products, spanning AWS, Azure, GCP,
OpenStack, VMware, and Kubernetes acquisition and processing. Introduced
in Chapter 03.

**GigaVUE-FM (Fabric Manager)** — The centralized, web-based management
application that onboards physical and virtual GigaVUE nodes, provides
fabric-wide Flow Mapping authoring, RBAC and directory integration,
licensing, monitoring, and the REST API automation depends on. Introduced
in Chapter 01 and detailed in Chapter 04.

**GigaVUE HC Series** — The family of GigaSMART-capable physical GigaVUE
node platforms (HCT, HC1, HC1-Plus, HC3), ranging from compact,
low-size/weight/power edge platforms to high-capacity, high-port-density
chassis. Introduced in Chapter 02.

**GigaVUE-OS** — The operating system running on every physical and
virtual GigaVUE node, exposing a CLI for port management, Flow Mapping,
GigaSMART configuration, and clustering. Introduced in Chapter 02.

**GigaVUE TA Series** — The family of fixed-configuration,
COTS-switch-based GigaVUE physical node platforms optimized for
high-density traffic aggregation at the acquisition edge; does not host
GigaSMART processing engines. Introduced in Chapter 02.

**GigaVUE V Series** — The virtual/cloud-native equivalent of a physical
GigaVUE node, deployed as a VM or cloud instance, terminating tunneled
traffic from virtual taps and performing Flow Mapping and GigaSMART-
equivalent processing. Introduced in Chapter 03.

**G-vTAP agent** — A lightweight virtual tap component deployed inside a
hypervisor guest or private-cloud instance to capture east-west traffic
and tunnel it to a GigaVUE V Series node. Introduced in Chapter 03.

**Heartbeat (inline)** — A periodic health probe GigaVUE-OS sends through
an inline tool to detect failure, triggering fail-open or fail-closed
behavior if the probe does not return within the configured interval.
Introduced in Chapter 07.

**Hybrid port** — A physical GigaVUE port configurable as either a
network port or a tool port, adding deployment flexibility on
fixed-port-count platforms. Introduced in Chapter 02.

**Inline bypass** — The set of resiliency mechanisms — heartbeat,
fail-open/fail-closed configuration, and maintenance mode — that keep an
inline deployment safe for production traffic when an in-path tool fails
or requires servicing. Introduced in Chapter 07.

**Inline map** — A Flow Mapping construct governing which traffic from an
inline network group is directed to which inline tool group, with
inspected (and potentially modified or blocked) traffic returned to the
production link. Introduced in Chapter 07.

**Inline network group** — A representation of a production link the
fabric has been physically inserted into, bridging both sides of the link
through dedicated inline network ports. Introduced in Chapter 07.

**Inline tool group** — One or more inline (in-path) tools attached to an
inline network group through dedicated inline tool ports, arranged in
series (sequential inspection stages) or parallel (load-balanced
capacity). Introduced in Chapter 07.

**Maintenance mode (inline)** — A deliberate, operator-invoked bypass of
an inline tool group for planned maintenance, independent of heartbeat
failure detection. Introduced in Chapter 07.

**map-passall** — A Flow Mapping type that forwards all traffic from its
source unconditionally, bypassing rule evaluation; used for first-touch
validation or where a tool genuinely requires an unfiltered copy.
Introduced in Chapter 05.

**map-scollector (shared collector)** — A Flow Mapping type whose
destination is shared across multiple source maps, commonly used to funnel
several filtered sources into one common GigaSMART processing stage
without duplicating destination configuration. Introduced in Chapter 05.

**Masking** — A GigaSMART application that overwrites specific packet
fields with a fixed pattern before delivery, permanently obscuring
sensitive data from every downstream tool that receives the traffic.
Introduced in Chapter 06.

**Negative heartbeat** — An inline heartbeat variant designed to detect a
tool that is technically forwarding traffic but has failed in a way basic
link-state monitoring would miss. Introduced in Chapter 07.

**Network port** — A GigaVUE port role receiving traffic entering the
fabric from a TAP or SPAN destination. Introduced in Chapter 01 and
formalized in Chapter 02.

**Oversubscription (tool port)** — The condition in which aggregated
network traffic destined for a tool port or GigaStream group exceeds its
available capacity, addressed through filtering, GigaStream load
balancing, or GigaSMART traffic reduction. Introduced in Chapter 01.

**Packet slicing** — A GigaSMART application that truncates each packet
after a specified point (commonly after a named protocol header) while
preserving headers needed for analysis, reducing tool storage and
processing load. Introduced in Chapter 06.

**Precryption** — Gigamon's host-based plaintext-visibility technology,
using eBPF to capture traffic before encryption or after decryption
inside the application/OS stack without intercepting or managing keys,
effective against TLS 1.3 and perfect-forward-secrecy traffic. Introduced
in Chapter 07.

**Role-based access control (RBAC), GigaVUE-FM** — GigaVUE-FM's
administrative access model, scoping capabilities (view-only, Flow
Mapping authoring, full administration, licensing) to specific roles and,
optionally, specific fabric groups. Introduced in Chapter 04.

**Replication, 1:N** — The Flow Mapping pattern of forwarding a single
acquisition point's traffic to multiple tool destinations simultaneously,
each receiving an identical copy. Introduced in Chapter 01.

**SPAN / mirror port** — A switch-native traffic-copy mechanism that
mirrors one or more source interfaces or VLANs to a destination port,
used for Gigamon acquisition where physical TAP insertion is impractical.
Introduced in Chapter 01.

**SSL/TLS decryption (GigaSMART)** — A GigaSMART application that
decrypts TLS-protected traffic centrally using configured server
certificates and keys, delivering plaintext to out-of-band tools (or, in
an inline deployment, to an in-path tool) that cannot decrypt
independently. Introduced in Chapter 06 and extended to the inline path
in Chapter 07.

**Stack port** — A GigaVUE port role interconnecting two or more nodes so
they can operate as a single logical cluster. Introduced in Chapter 02.

**Tap inventory** — A version-controlled record mapping every acquisition
point to its GigaVUE network port, acquisition method, and subscribed
tools, maintained as the source of truth for fabric acquisition coverage.
Introduced in Chapter 01.

**TAP (network Test Access Point)** — A passive or active physical device
inserted in-line with a production link that copies traffic to one or two
monitor ports without altering the original path, providing full-fidelity
acquisition independent of switch mirroring capacity. Introduced in
Chapter 01.

**Tool chaining** — Forwarding traffic from one inline or out-of-band
tool to the next in a defined sequence, where one tool's output is a
precondition for a downstream tool's input. Introduced in Chapter 01.

**Tool port** — A GigaVUE port role delivering traffic out of the fabric
toward a connected monitoring or security tool. Introduced in Chapter 01
and formalized in Chapter 02.

**Universal Cloud Tap (UCT)** — Gigamon's lightweight, agentless or
light-agent cloud tapping mechanism that pre-filters traffic at the
source instance before tunneling it to a GigaVUE V Series node, reducing
egress cost and downstream processing load. Introduced in Chapter 03.

**Visibility fabric** — The dedicated layer of GigaVUE nodes and
GigaVUE-FM management sitting between traffic acquisition points and the
tool ecosystem, responsible for filtering, transforming, and delivering
traffic without adding load or risk to the production network. Introduced
in Chapter 01.
