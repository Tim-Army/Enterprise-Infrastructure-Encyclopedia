# Volume XXII Glossary

Definitions for terms introduced in **Volume XXII — Dell OpenManage
Enterprise**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Account lockout policy** — An appliance-wide security control that
locks a local account after a configured number of consecutive failed
login attempts, requiring an Administrator-role account to unlock it
before the timer expires. Introduced in Chapter 02.

**Alert action** — The delivery mechanism an alert policy invokes when it
matches an event: console display, email, SNMP trap forwarding, syslog
forwarding, or webhook invocation in supported releases. Introduced in
Chapter 04.

**Alert policy** — An administrator-defined rule matching alerts by
source device or group, category, and severity, and associating matches
with one or more alert actions. Introduced in Chapter 04.

**Appliance backup** — An export of OME's application state (inventory,
job history, alert policies, templates, credentials, accounts) to a
network-accessible location, distinct from any backup of the managed
device fleet's own data. Introduced in Chapter 09.

**Baseline** — A named association between a firmware/driver catalog (or
a specific version of one) and a target scope of devices or a device
group, evaluated to produce a compliance report. Introduced in Chapter
05.

**Compliance report (configuration)** — The result of comparing a
device's current configuration against a template without applying any
change, expressed as per-attribute drift. Introduced in Chapter 08.

**Compliance report (firmware)** — The result of evaluating a baseline:
for each in-scope device and component, whether the currently inventoried
version matches, exceeds ("ahead of baseline"), or falls behind ("behind
baseline") what the catalog specifies. Introduced in Chapter 05.

**Connected (online) repository** — A catalog source pointed at Dell's
hosted repository at `downloads.dell.com`, refreshed automatically or on
a schedule, requiring appliance outbound connectivity. Introduced in
Chapter 06.

**Custom catalog** — A catalog source registered from a locally or
network-hosted location (a network share or internal HTTP endpoint)
rather than Dell's connected online source, the mechanism used to consume
an offline/air-gapped repository export. Introduced in Chapter 07.

**Dell Repository Manager (DRM)** — A separate Windows-based Dell tool
used to build custom and offline-exportable firmware/driver catalogs
outside of a live OME appliance, typically run on an internet-connected
workstation distinct from an air-gapped OME instance. Introduced in
Chapter 07.

**Dell Update Package (DUP)** — A self-contained, model- and
component-aware installer for a single firmware or driver update,
referenced by catalog metadata and applied through iDRAC's Lifecycle
Controller. Introduced in Chapter 05.

**Deployment template** — A configuration template used to push captured
or defined configuration onto one or more target devices, as opposed to
compliance-only evaluation of the same template. Introduced in Chapter
08.

**Device control** — Actions performed directly against a managed
device's out-of-band interface, most commonly power operations (on, off,
cycle, graceful/non-graceful shutdown) and chassis identification.
Introduced in Chapter 03.

**Directory service authentication** — OME's integration with Active
Directory or a generic LDAP directory, mapping directory security groups
to OME roles so console logins use existing enterprise credentials rather
than appliance-local accounts. Introduced in Chapter 02.

**Discovery** — The process of probing a set of network targets with one
or more protocols and credential profiles to determine what is reachable
and identifiable, the first stage of OME's discovery-to-onboarding-to-
inventory pipeline. Introduced in Chapter 03.

**Discovery credential profile** — A named, reusable, protocol-scoped
set of credentials referenced by one or more discovery jobs, separating
credential storage and rotation from individual job definitions.
Introduced in Chapter 03.

**Downgrade (firmware)** — Applying a firmware or driver version older
than what is currently installed on a device, a higher-risk operation
than a forward update and disabled by default in most baseline
configurations. Introduced in Chapter 05.

**Dynamic (query-based) group** — A device group whose membership is
defined by a filter expression evaluated against device attributes,
updating automatically as devices are onboarded, retired, or change
state. Introduced in Chapter 03.

**Firmware/driver catalog** — A versioned metadata index describing
available update packages, the models and components they apply to, and
their severity classification, sourced either from Dell's connected
repository or an offline/custom repository. Introduced in Chapter 05.

**Health status roll-up** — The mechanism by which a device's health
status (Normal, Warning, Critical, Unknown) is computed from individual
component conditions, and by which a group's dashboard status reflects
the worst status among its member devices. Introduced in Chapter 04.

**Identity pool** — A managed pool of unique values (IP addresses, IQNs,
and similar per-device-unique identifiers) that OME can assign
automatically during template deployment, avoiding manual per-device
attribute overrides. Introduced in Chapter 08.

**Inventory collection** — The scheduled or on-demand process of pulling
detailed hardware, firmware, driver, and warranty facts from a managed
device, the data source for compliance reporting and dashboards.
Introduced in Chapter 03.

**iDRAC (Integrated Dell Remote Access Controller)** — The per-server,
out-of-band management controller OME discovers, inventories, and
orchestrates updates against; covered in administrative depth in Volume
XXIII. Introduced in Chapter 01.

**Job engine** — The appliance subsystem that queues, schedules, retries,
and tracks execution history for every asynchronous OME operation,
including discovery, inventory refresh, update orchestration, template
deployment, and report generation. Introduced in Chapter 01 and
formalized in Chapter 04.

**Lifecycle Controller** — The embedded management firmware on a
PowerEdge server, accessed through iDRAC, that OME's update jobs use as
the execution engine to actually apply firmware and driver packages.
Introduced in Chapter 05.

**OpenManage Enterprise (OME)** — Dell's virtual appliance-based,
one-to-many systems management console for PowerEdge rack and tower
servers, the subject of this volume. Introduced in Chapter 01.

**OpenManage Enterprise-Modular (OME-M)** — A related but distinct Dell
product running on a PowerEdge MX7000 chassis's Chassis Management
Controller, managing sleds and fabric within that chassis, commonly run
alongside OME rather than in place of it. Introduced in Chapter 01.

**OData pagination (`@odata.nextLink`)** — The mechanism OME's REST API
uses to page large result sets; fleet-scale automation must follow this
link rather than assuming a single response page is complete. Introduced
in Chapter 08.

**Onboarding** — The stage after discovery in which a positively
identified, credentialed endpoint is committed into OME's managed device
inventory, gaining access to monitoring, compliance, and template
functionality. Introduced in Chapter 03.

**Plugin framework** — The OME subsystem allowing optional capability
modules (Power Manager, the SupportAssist integration) to be installed
and licensed independently of the base appliance. Introduced in Chapter
01.

**Power Manager** — An optional OME plugin extending monitoring to
rack/row-level power and thermal telemetry beyond individual server
health. Introduced in Chapter 01.

**Proxy configuration (catalog egress)** — The appliance setting
governing how OME reaches `downloads.dell.com` for connected catalog
operations, either directly or through an explicitly configured web
proxy. Introduced in Chapter 06.

**Recovery time objective (RTO)** — The maximum acceptable duration of
OME console/API unavailability during an unplanned outage before a
restore-to-new-appliance process must begin, an explicit design decision
that drives backup currency and restore rehearsal frequency. Introduced
in Chapter 09.

**Redfish** — An industry-standard, HTTPS-based out-of-band management
protocol OME uses (alongside WS-Management) to discover and manage iDRAC
and other Redfish-compliant targets. Introduced in Chapter 01.

**Role (RBAC)** — A named bundle of permissions (device management,
template operations, user administration, and similar) assigned to an
OME identity, combined with scope to bound what an account can do.
Introduced in Chapter 02.

**Scope** — An assignment restricting a role to one or more device
groups, the primary mechanism for delegated, least-privilege
administration in OME. Introduced in Chapter 02.

**Server Configuration Profile (SCP)** — The underlying iDRAC mechanism
for exporting and importing server configuration state, which OME
configuration templates wrap with fleet-scale capture, comparison, and
deployment tooling. Introduced in Chapter 08.

**Session token (`X-Auth-Token`)** — The authentication token returned
by a successful `POST` to `SessionService/Sessions`, required on every
subsequent OME REST API request until the session expires or is deleted.
Introduced in Chapter 01.

**Severity classification (firmware)** — The urgency rating (commonly
Critical, Recommended, and Optional) Dell assigns to a catalog-referenced
update, used to prioritize remediation. Introduced in Chapter 05.

**SNMP discovery** — Discovery of third-party network, storage, or
generic devices over SNMP, yielding basic identification and health
polling but not the deep component-level inventory available from native
iDRAC discovery. Introduced in Chapter 03.

**Static group** — A device group with an explicitly assigned membership
list that changes only when an administrator or automation adds or
removes a device. Introduced in Chapter 03.

**SupportAssist Enterprise** — Dell's automated support-case and
telemetry pipeline, integrated with but distinct from OME, covered as an
operational integration in this volume. Introduced in Chapter 01.

**Transfer integrity verification** — A checksum-based validation step
performed on offline repository content after it crosses an air gap,
confirming it was not corrupted or tampered with before it is registered
as a trusted catalog source. Introduced in Chapter 07.

**Update job** — The orchestrated OME operation that applies one or more
non-compliant firmware or driver packages to target devices through each
device's iDRAC and Lifecycle Controller. Introduced in Chapter 05.

**WS-Management (WS-Man)** — A SOAP-based, HTTPS-transported management
protocol OME historically used (alongside the increasingly favored
Redfish) for native iDRAC discovery and orchestration. Introduced in
Chapter 01.
