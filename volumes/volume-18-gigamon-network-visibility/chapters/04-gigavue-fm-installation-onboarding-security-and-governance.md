# Chapter 04: GigaVUE-FM Installation, Onboarding, Security, and Governance

![Lab flow for this chapter: a lab GigaVUE node onboards into one fabric group, appearing healthy in GigaVUE-FM's inventory; a read-only role is denied when attempting to create a Flow Map, while a flow-author role successfully creates one on the same fabric group. As a negative test, the flow-author user attempts to access a second, unrelated fabric group not included in that role's scope; access is denied, confirming role scoping is enforced per fabric group and not merely per capability — write permission on one fabric group does not imply write permission on another.](../../../diagrams/volume-18-gigamon-network-visibility/chapter-04-gigavue-fm-rbac-scope-flow.svg)

*Figure 4-1. Flow used throughout this chapter's Hands-On Lab: GigaVUE-FM onboarding and scoped RBAC roles, tested against a role's access to a fabric group outside its scope.*

## Learning Objectives

- Explain GigaVUE-FM's role as the centralized control plane for a
  physical-and-virtual GigaVUE fabric, distinct from per-node GigaVUE-OS
  CLI administration.
- Deploy GigaVUE-FM and complete initial setup, including high-availability
  considerations for the management plane itself.
- Onboard physical and virtual GigaVUE nodes into GigaVUE-FM and organize
  them into a manageable inventory.
- Configure role-based access control (RBAC), directory integration, and
  audit logging to govern who can change fabric configuration.
- Explain licensing, backup/restore, and upgrade workflow considerations
  for GigaVUE-FM as a production management system in its own right.

## Theory and Architecture

### GigaVUE-FM as the fabric's control plane

Chapters 02 and 03 configured individual nodes directly through
GigaVUE-OS CLI — a necessary skill for first-touch bring-up and
node-local troubleshooting, but not how a production fabric of more than
a handful of nodes is operated day to day. **GigaVUE-FM** (Fabric
Manager) is Gigamon's centralized, web-based management application:
every physical and virtual node registers with GigaVUE-FM, which then
becomes the single place an operator authors Flow Mapping, configures
GigaSMART applications, monitors fabric health, manages licensing, and
exposes the REST API that automation ([Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md)) depends on.

This mirrors a pattern already familiar from other volumes in this
encyclopedia — a per-device CLI/data-plane layer paired with a
centralized management plane (compare, for example, Panorama's
relationship to individual PAN-OS firewalls in [Volume XVI](../../volume-16-palo-alto-networks-security/README.md), or a wireless
LAN controller's relationship to individual access points). The same
operational lesson applies here: GigaVUE-FM does not replace node-local
administration, but production changes should flow through it so that
Flow Mapping, licensing, and audit history remain consistent and
centrally visible rather than fragmented across dozens of independently
managed node CLIs.

### Deployment models

GigaVUE-FM is deployed as a virtual appliance (OVA/qcow2-style image for
VMware or KVM-based private cloud) or as a cloud-hosted instance in public
cloud, sized according to the number of managed nodes and the volume of
statistics/log retention required. A small lab or pilot deployment can run
GigaVUE-FM as a single instance; a production fabric managing a
meaningful physical and virtual node count should plan for a
**high-availability GigaVUE-FM deployment** (an active instance with a
standby, or a clustered management deployment depending on the release's
supported HA model), because GigaVUE-FM's unavailability does not stop
already-configured Flow Mapping from forwarding traffic, but it does
remove the ability to make fabric changes, view consolidated health, or
respond to a fabric-wide incident until it is restored.

### Node onboarding and inventory organization

Once GigaVUE-FM is reachable, physical nodes ([Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md)) and virtual
nodes ([Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)) are onboarded by registering each node's management
address and credentials (or, for cloud-deployed virtual nodes, through
automated self-registration at first boot, per [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)). GigaVUE-FM
then presents a unified inventory of every node — physical and virtual —
as members of one or more logical fabrics, typically organized to reflect
the organization's own structure: by data center, by region, by business
unit, or by security zone, depending on how administrative and Flow
Mapping responsibility should be scoped.

### Governance: RBAC, directory integration, and audit

Because GigaVUE-FM is the single point of control for what traffic goes
to which tool, its own access control is a governance-critical surface —
equivalent in sensitivity to a SIEM's administrative console or a
firewall manager. GigaVUE-FM supports:

- **Role-based access control (RBAC).** Administrative roles are scoped to
  specific capabilities (view-only, Flow Mapping authoring, full
  administration, licensing management) and can be scoped to specific
  node groups or fabrics rather than granting fabric-wide access to every
  administrator by default.
- **Directory integration.** Authentication against an existing enterprise
  identity provider (LDAP/Active Directory, or SAML-based single sign-on)
  rather than relying solely on locally defined GigaVUE-FM accounts,
  consistent with centralized identity governance practices covered
  throughout this encyclopedia's security-focused volumes.
- **Audit logging.** Every configuration change — a new Flow Map, a
  modified GigaSMART application, a licensing change, an administrator
  added or removed — is recorded with the responsible identity and
  timestamp, forming the audit trail a security or compliance review will
  expect for a system that controls access to sensitive network traffic.
- **Multi-tenancy.** Larger and service-provider deployments can scope
  administrative visibility and Flow Mapping authority to defined tenant
  boundaries, so that one business unit's administrators cannot see or
  modify another's traffic policy — directly relevant to the
  multi-tenant cloud considerations raised in [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md).

### Licensing model

GigaVUE-FM itself, individual node platforms, and specific GigaSMART
applications ([Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md)) are licensed both for base functionality and for
advanced feature tiers (extended map-rule capacity, specific GigaSMART
applications, cloud node counts). GigaVUE-FM centralizes license
visibility and, in most deployments, license application — an operator
should be able to answer "which features are licensed on which node" from
GigaVUE-FM's licensing view without cross-referencing individual node
CLIs.

## Design Considerations

- **Treat GigaVUE-FM's own availability as a production management-plane
  requirement, not an afterthought.** Size and deploy it with the same HA
  rigor applied to any other centralized control plane in this
  encyclopedia (compare vCenter in [Volume V](../../volume-05-vmware-virtualization/README.md) or Panorama in [Volume XVI](../../volume-16-palo-alto-networks-security/README.md));
  a fabric that cannot be reconfigured during an incident because its
  manager is a single point of failure is a design gap, not an acceptable
  trade-off.
- **Decide inventory organization before onboarding at scale.** Retrofitting
  a logical grouping structure (by data center, region, or business unit)
  after dozens of nodes are already onboarded flat is disruptive; agree on
  the grouping model in the same design pass as the tap inventory from
  [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md).
- **Scope RBAC to the principle of least privilege from day one.**
  Granting every administrator full fabric-wide access because the fabric
  is small today creates governance debt that is painful to unwind once
  the fabric — and the number of administrators — grows. Design role
  scopes around actual job function (Flow Mapping author versus read-only
  auditor versus licensing administrator) even in a small initial
  deployment.
- **Plan directory integration alongside identity infrastructure changes,
  not independently.** GigaVUE-FM's SAML/LDAP integration should be
  reviewed whenever the organization's identity provider changes (a
  migration, a new conditional access policy) rather than treated as a
  one-time setup step forgotten after initial configuration.
- **Back up GigaVUE-FM configuration on a defined schedule, separate from
  individual node configuration backups.** GigaVUE-FM holds the
  fabric-wide Flow Mapping definitions, RBAC structure, and license
  associations that would otherwise need to be painstakingly
  reconstructed node by node after a catastrophic loss.

## Implementation and Automation

### Initial GigaVUE-FM setup

1. Deploy the GigaVUE-FM virtual appliance image to the target hypervisor
   or cloud platform, sized per the vendor's guidance for the expected
   managed-node count.
2. Complete first-boot console configuration: management IP addressing,
   DNS, and NTP (accurate time is essential for audit-log integrity and
   for correlating fabric events with tool-side telemetry).
3. Access the GigaVUE-FM web UI over HTTPS using the initial administrative
   credential, and change that credential immediately.
4. Install the base license and confirm the license inventory reflects
   the entitlements purchased before onboarding nodes.

### Onboarding a physical or virtual node

```text
GigaVUE-FM UI (representative workflow; menu paths vary by release):
Physical > Nodes > Add Node
  Management IP: 10.20.10.5
  Credentials: <node admin credential>
  Fabric group: dc1-visibility-fabric
```

For nodes deployed with self-registration configured at first boot
(common for cloud-hosted V Series nodes, per [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)), onboarding is
largely automatic: the node contacts GigaVUE-FM's registration endpoint
and appears in the pending-approval queue, where an administrator confirms
it belongs to the expected fabric before it is fully trusted.

```text
GigaVUE-FM UI:
Physical > Nodes > Pending Registrations
  Approve: v-series-aws-use1-01  ->  Fabric group: cloud-visibility-use1
```

### Configuring RBAC and directory integration

```text
GigaVUE-FM UI:
Administration > Authentication > External Authentication
  Type: LDAP / SAML
  Server: idp.example.com
  Base DN / Metadata: <organization-specific>

Administration > Roles
  Role: flow-mapping-author
    Permissions: Flow Mapping (read/write), Node inventory (read-only)
    Scope: dc1-visibility-fabric

Administration > Users
  User: jsmith@example.com  ->  Role: flow-mapping-author
```

### Backup and restore

```text
GigaVUE-FM UI or API:
Administration > Backup
  Schedule: daily, 02:00 local
  Retention: 30 days
  Destination: <organization SFTP or object storage target>
```

A scheduled, off-box backup destination is essential — a backup stored
only on the GigaVUE-FM instance itself does not survive the loss of that
instance.

### Upgrade workflow

GigaVUE-FM and managed GigaVUE-OS nodes are versioned together against a
supported compatibility matrix; an upgrade generally follows: review the
release notes and compatibility matrix for the target GigaVUE-FM version
against currently deployed node firmware, back up GigaVUE-FM
configuration, upgrade GigaVUE-FM itself, then stage and apply node
firmware upgrades in a controlled sequence (non-disruptively where
clustering and redundant paths allow, per [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md)'s inline resiliency
model for nodes carrying inline traffic).

> Exact menu paths, backup destinations supported, and upgrade sequencing
> options vary by GigaVUE-FM release; confirm against the release notes
> for the specific version in use, consistent with the 6.x baseline in
> [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).

## Validation and Troubleshooting

- **A node will not onboard.** Confirm network reachability between
  GigaVUE-FM and the node's management interface (a firewall or
  security-group rule blocking the registration/heartbeat port is the
  most common cause), and confirm the credential supplied matches the
  node's current administrative credential.
- **A node onboards but shows degraded or unknown health.** Confirm time
  synchronization between GigaVUE-FM and the node — significant clock
  drift can cause heartbeat or certificate-validation failures that
  present as a health problem rather than an obvious time-sync error.
- **An administrator cannot see or modify a fabric they should have
  access to.** Review the RBAC role scope assigned to that administrator's
  account; a role correctly granting Flow Mapping authoring rights but
  scoped to the wrong fabric group is a common misconfiguration,
  distinguishable from an authentication failure because the
  administrator can log in successfully.
- **Directory-integrated login fails after an identity provider change.**
  Confirm the SAML metadata or LDAP bind configuration in GigaVUE-FM was
  updated to match; identity provider certificate rotations and endpoint
  changes are a common, easily missed cause of a sudden authentication
  outage.
- **A restored backup does not fully reflect the expected fabric state.**
  Confirm the backup being restored is recent relative to the last
  configuration change, and confirm node firmware versions at restore time
  are compatible with the GigaVUE-FM version the backup was taken from —
  restoring a configuration backup onto a materially different node
  firmware baseline than it was created against can produce partial or
  rejected configuration application.

## Security and Best Practices

- Require directory-integrated authentication with multi-factor
  authentication for GigaVUE-FM administrative access wherever the
  organization's identity infrastructure supports it; treat GigaVUE-FM
  credentials as tier-0, on par with SIEM and firewall-manager access.
- Scope every administrative role to the minimum fabric group and
  capability set the individual's job function requires; avoid a
  default "full administrator for everyone" posture even in small
  deployments.
- Restrict GigaVUE-FM's own web UI and API reachability to an
  access-controlled administrative network segment, never expose it
  directly to the general corporate network or the internet.
- Enable and regularly review audit logging; export audit events to a
  centralized SIEM ([Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md) covers integration patterns) rather than
  relying solely on GigaVUE-FM's local log retention.
- Rotate the initial and any locally defined administrative credentials on
  a defined cadence, and remove local accounts once directory integration
  is fully validated, keeping only a documented emergency-access local
  account.
- Validate backups periodically with an actual restore test in a lab
  environment; an untested backup is not a reliable recovery capability.

## References and Knowledge Checks

**References**

- [Gigamon, *GigaVUE-FM Fabric Manager Data Sheet*](https://www.gigamon.com/content/dam/resource-library/english/data-sheet/ds-gigavue-fm-fabric-manager.pdf) — capability overview
  and deployment models.
- [Gigamon, *GigaVUE Fabric Management* documentation library](https://docs.gigamon.com/doclib/Content/GigaVUE_Fabric_Manager-allDocIntro.html) — onboarding,
  RBAC, and licensing workflows.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline.

**Knowledge checks**

1. Why should production Flow Mapping changes flow through GigaVUE-FM
   rather than being made independently on individual node CLIs?
2. What is the practical operational consequence of GigaVUE-FM becoming
   unavailable, given that it is a management plane rather than a
   traffic-forwarding data plane?
3. Name two governance controls GigaVUE-FM provides beyond simple
   username/password authentication, and explain why each matters for a
   system that controls access to sensitive network traffic.
4. Why is a GigaVUE-FM configuration backup insufficient on its own if
   never tested with an actual restore?

## Hands-On Lab

**Objective:** Deploy a lab GigaVUE-FM instance, onboard a lab GigaVUE
node (physical or virtual, from [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) or 03), configure a scoped
administrative role, and validate both successful and denied access
paths.

**Prerequisites**

- A lab GigaVUE-FM virtual appliance deployable to an available
  hypervisor or cloud environment.
- At least one lab GigaVUE node (physical or virtual) with known
  management credentials, from the [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) or [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) labs.
- Two lab user identities (or the ability to create two local GigaVUE-FM
  accounts) to demonstrate scoped access.
- Isolated lab network segment — do not perform this lab against
  production management infrastructure.

**Steps**

1. Deploy the GigaVUE-FM appliance and complete first-boot configuration
   (management IP, DNS, NTP).
2. Log in to the GigaVUE-FM web UI with the initial credential and
   immediately change it to a strong, lab-documented password.
3. Onboard the lab GigaVUE node by registering its management IP and
   credentials under a new fabric group named `lab-fabric-01`.
   **Expected result:** the node appears in the GigaVUE-FM inventory with
   a healthy status within a few minutes of onboarding.
4. Create a scoped role `lab-read-only` granting read-only access to
   `lab-fabric-01` only, and a second role `lab-flow-author` granting Flow
   Mapping read/write access to the same fabric group.
5. Create two local user accounts (or map two test directory identities),
   assigning `lab-read-only` to the first and `lab-flow-author` to the
   second.
6. Log in as the `lab-read-only` user and attempt to create a new Flow
   Map on `lab-fabric-01`.
   **Expected result:** the action is denied or the relevant controls are
   unavailable/read-only in the UI, confirming the scoped role correctly
   restricts write access.
7. Log in as the `lab-flow-author` user and create a minimal test Flow Map
   on the onboarded node.
   **Expected result:** the map is created successfully, confirming the
   role's granted permissions function as intended.
8. **Negative test:** attempt to log in as the `lab-flow-author` user and
   access or modify a different fabric group not included in that role's
   scope (create a second empty fabric group, `lab-fabric-02`, if none
   exists).
   **Expected result:** access to `lab-fabric-02` is denied, confirming
   role scoping is enforced per fabric group and not merely per
   capability.
9. Review the audit log and confirm every action above — the login
   attempts, the denied write, the successful map creation — is recorded
   with the correct user identity and timestamp.
10. **Cleanup:** remove the test Flow Map, the two lab user accounts (or
    role assignments), and the `lab-fabric-02` empty group if it was
    created solely for this lab, and note whether `lab-fabric-01` and the
    onboarded node should be retained for later chapters' exercises.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GigaVUE-FM is the centralized control plane that turns individually
configured GigaVUE nodes into one governed, auditable fabric — it is
where Flow Mapping is authored at scale, where RBAC and directory
integration enforce who can change traffic policy, and where licensing,
backup, and upgrade are managed fabric-wide rather than node by node.
Treating GigaVUE-FM's own availability, access control, and backup
posture with production rigor is a prerequisite for everything the
remaining chapters in this volume build on top of it.

- [ ] Can explain GigaVUE-FM's role as a centralized control plane
      distinct from per-node CLI administration.
- [ ] Can onboard a physical or virtual node into GigaVUE-FM and organize
      it into a logical fabric group.
- [ ] Can configure a scoped administrative role and explain why
      least-privilege RBAC matters for a fabric manager.
- [ ] Can describe GigaVUE-FM's licensing, backup, and upgrade
      considerations as production management-plane concerns.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
