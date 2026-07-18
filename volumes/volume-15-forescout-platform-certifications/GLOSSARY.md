# Volume XV Glossary

Definitions for terms introduced in **Volume XV — Forescout Platform and
Certifications**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Action history** — The host-level record of every automated and manual
action taken against a host, including policy-driven property changes,
control actions, and manual overrides. Introduced in Chapter 04.

**Active scanning** — Targeted, permission-gated network probes (banner
grabs, port scans, OS fingerprinting) an appliance performs against
discovered IP addresses to fill visibility gaps passive monitoring alone
cannot resolve. Introduced in Chapter 01.

**API governance** — The set of controls — least-privilege scoping, rate
limiting, credential rotation, and API-specific audit logging — applied
to programmatic access through the Forescout Web API. Introduced in
Chapter 07.

**Appliance (Forescout Appliance)** — A physical or virtual node running
a hardened, purpose-built operating system that performs traffic
monitoring, active discovery, plugin execution, and local policy
evaluation for the network segment(s) it is connected to. Introduced in
Chapter 01.

**Asset curation** — The ongoing discipline of merging, deduplicating,
enriching, and validating asset inventory records over the life of a
deployment, distinct from one-time baseline validation; particularly
important in OT/ICS environments where assets are long-lived and only
partially identifiable from network traffic alone. Introduced in
Chapter 09.

**Behavioral baselining** — Establishing what normal communication
patterns look like for a network zone (endpoints, protocol operations,
frequency, timing) so that material deviation can be flagged as a
potential threat-detection signal. Introduced in Chapter 09.

**Capability module** — A licensed layer of platform functionality
(eyeSight, eyeControl, eyeSegment, eyeExtend, eyeInspect) built on the
core appliance, each unlocking a distinct category of visibility,
control, segmentation, integration, or OT/ICS capability. Introduced in
Chapter 01.

**Clarification policy** — A policy type, commonly built from the
"Clarify" template, that targets hosts with missing, generic, or
low-confidence classification and resolves the ambiguity through
escalated discovery, directed end-user engagement, or manual review
queueing. Introduced in Chapter 03.

**Classification** — The process of deriving identity properties —
principally `Function` and `Operating System` — from raw fingerprinting
data, producing a result with an associated confidence level. Introduced
in Chapter 02.

**Classification confidence** — A measure of how much corroborating
evidence supports a classification result, used to gate whether
downstream compliance and control policies treat a host as
authoritatively classified. Introduced in Chapter 02.

**Compliance policy** — A policy type that evaluates whether a host's
current state matches a defined desired state and records the result as
a compliance status property, typically paired with a grace period and
remediation actions, without itself changing network access. Introduced
in Chapter 03.

**Console (Forescout Console)** — The management application
administrators use to configure policies, review the asset inventory,
manage plugins, and monitor platform health, connecting to one or more
appliances or to an Enterprise Manager. Introduced in Chapter 01 and
detailed in Chapter 02.

**Control policy** — A policy type that changes a host's actual network
state — VLAN reassignment, port restriction or block, endpoint isolation,
or an equivalent action driven through an eyeExtend integration.
Introduced in Chapter 03.

**Custom property** — An administrator-defined attribute on the host
record tracking an organization-specific fact no built-in property
covers, behaving identically to a built-in property everywhere it is used.
Introduced in Chapter 02.

**Discovery mechanisms** — The combined set of techniques (passive
traffic monitoring, active scanning, switch/wireless integration,
directory/infrastructure plugins, and optional endpoint-side access) the
platform uses to build device visibility without a single point of
failure. Introduced in Chapter 01.

**Dynamic group** — A property-driven collection of hosts whose
membership updates automatically as underlying property values change,
contrasted with a static group's manually maintained membership.
Introduced in Chapter 04.

**Enterprise Manager (EM)** — The aggregation and policy-distribution
node in a multi-appliance deployment, consolidating inventory data and
distributing policy configuration to managed appliances from a single
pane of glass. Introduced in Chapter 01.

**Exclusion group** — A documented group of hosts every control policy
checks against before acting, protecting sensitive or protected hosts
(isolated lab segments, medical devices, infrastructure management
interfaces) from unintended enforcement. Introduced in Chapter 03.

**eyeControl** — The capability module providing network access control
actions: VLAN assignment, port block/restrict, endpoint isolation, and
guest/BYOD onboarding workflows. Introduced in Chapter 01.

**eyeExtend** — Both the licensed integration-framework capability module
and the general term for the platform's catalog of bidirectional
third-party integration plugins (SIEM, SOAR, ITSM, vulnerability
management, EDR/UEM, firewall/NAC vendors). Introduced in Chapter 01 and
detailed in Chapter 05.

**eyeInspect** — The OT/ICS-specific capability module providing passive
deep packet inspection, industrial protocol dissection, and asset
visibility for industrial networks. Introduced in Chapter 01 and detailed
in Chapters 08–09.

**eyeSegment** — The capability module providing segmentation visibility
and policy modeling — mapping observed traffic flows and proposing or
enforcing segmentation policy across existing switches and firewalls
without requiring a physical network redesign. Introduced in Chapter 01
and detailed in Chapter 05.

**eyeSight** — The baseline visibility capability module (discovery,
classification, asset inventory) required as the foundation for every
other capability module. Introduced in Chapter 01.

**Grace period** — A defined window during which a newly non-compliant
host is flagged but not yet escalated to a control action, allowing
automated remediation or end-user self-correction time to resolve the
issue first. Introduced in Chapter 03.

**Host record** — The core data model entity, identified primarily by MAC
address, that every property collected about a device is attached to.
Introduced in Chapter 02.

**HPS Inspection Engine** — A plugin providing deep, credentialed
inspection of Windows endpoints (installed software, running processes,
registry/configuration state) via management interfaces such as WMI/RPC.
Introduced in Chapter 01.

**Idempotent automation** — Automation designed so that running an
operation multiple times produces the same end state as running it once,
allowing safe re-execution of scripts built on the Forescout Web API.
Introduced in Chapter 07.

**Industrial DMZ** — The Purdue model's Level 3.5 boundary zone between
enterprise IT and operational technology networks, and a common placement
point for OT visibility sensors. Introduced in Chapter 08.

**Layered diagnostic model** — A structured, top-down troubleshooting
method spanning network delivery, appliance health, plugin state,
property/policy state, and downstream/integration state. Introduced in
Chapter 06.

**Monitor mode** — A policy staging state in which a control or
enforcement policy logs the action it would take without actually
executing it, used to validate a policy's real-world behavior before
enabling live enforcement. Introduced in Chapter 03.

**Passive traffic monitoring** — Observing network traffic via a
SPAN/mirror port or tap without transmitting onto the monitored segment;
the default and, in OT/ICS environments, the primary visibility posture.
Introduced in Chapter 01 and reinforced for OT/ICS in Chapter 08.

**Plugin (module)** — A self-contained component that collects data
about hosts (writing it into properties), exposes an action a policy can
invoke, or both; plugins are licensed and scoped independently.
Introduced in Chapter 02.

**Policy engine** — The shared evaluation system underlying
classification, clarification, compliance, and control policies: an
ordered set of rules, each with conditions evaluated against host
properties and actions that fire on a match. Introduced in Chapter 01 and
formalized in Chapter 03.

**Purdue Enterprise Reference Architecture (PERA)** — The standard
reference model for layering an industrial network (Levels 0 through 5,
from physical process to enterprise IT), used to reason about OT/ICS
sensor placement and segmentation. Introduced in Chapter 08.

**RBAC (role-based access control)** — Console access control built
around roles scoped to job function and inventory/site boundaries,
typically integrated with a centralized identity provider. Introduced in
Chapter 04.

**Re-admission condition** — The explicitly defined property state that,
once restored, triggers a control policy to automatically reverse an
enforcement action such as a VLAN reassignment. Introduced in Chapter 03.

**Reconciliation job** — A scheduled, typically idempotent, API-driven
script that compares platform state against an authoritative external
source and either auto-corrects known-safe discrepancies or flags them
for human review. Introduced in Chapter 07.

**SecureConnector** — An optional dissolvable or persistent endpoint
client providing deeper, credentialed visibility into Windows and Linux
endpoints where agentless network-based fingerprinting is insufficient.
Introduced in Chapter 01.

**Static group** — A manually maintained collection of hosts, appropriate
for small, fixed populations that do not need to track the environment
automatically. Introduced in Chapter 04.

**Switch plugin** — A plugin performing SNMP/CLI reads against access
switches to provide physical port location, VLAN/802.1X state, and
control-action execution capability. Introduced in Chapter 01.

**Threat detection (OT/ICS)** — Detection logic combining behavioral
baselining, known-bad protocol behavior, and change-management
correlation to distinguish legitimate industrial control operations from
anomalous ones. Introduced in Chapter 09.

**Web API (Forescout)** — The RESTful programmatic interface exposing
host inventory queries, property reads/writes, policy and group
management, and administrative operations to external automation and
integrations. Introduced in Chapter 07.

**Wireless plugin** — A plugin integrating with WLAN controllers to
provide wireless session state and control-action execution capability
analogous to the Switch plugin's wired-network role. Introduced in
Chapter 01.

**Zone (cell/area zone)** — A Purdue-model network segment grouping
related industrial control assets, used as the unit of scope for OT/ICS
sensor placement, asset curation, and behavioral baselining. Introduced
in Chapter 08 and extended in Chapter 09.
