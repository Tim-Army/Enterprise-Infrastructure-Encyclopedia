# Chapter 02: Console, Plugins, Properties, and Asset Classification

![Lab flow for this chapter: a custom property is created and set on a test endpoint, and a classification rule with a condition specific to that device type correctly updates its Function property, with an inventory view filtered on that value showing only the intended endpoint. As a negative test, the rule's condition is deliberately broadened to match only a single common open port with no other qualifier; reapplying it now incorrectly matches at least one other host on the segment, demonstrating why rule specificity and ordering matter before the rule is reverted to its specific form.](../../../diagrams/volume-015-forescout-platform-certifications/chapter-02-classification-rule-specificity-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: a custom property and classification policy validated for precision, then deliberately over-broadened.*

## Learning Objectives

- Navigate the major functional areas of the Forescout Console at a
  conceptual level: asset inventory, policy management, plugin
  configuration, and platform administration.
- Explain the plugin (module) architecture and how plugins contribute
  properties to the shared asset inventory.
- Distinguish built-in properties from custom properties, and describe when
  a custom property is the correct design choice.
- Describe how the classification engine derives function, operating
  system, and vendor/model properties, and what a classification confidence
  level means operationally.
- Build and tune a basic classification policy using property-based
  conditions.
- Organize the asset inventory using groups, views, and tags for
  operational use by NOC/SOC staff.

## Theory and Architecture

Every capability in the Forescout Platform — compliance checking, control
actions, segmentation policy, reporting — is built on top of a single shared
data model: the **host record**, identified primarily by MAC address, and
the collection of **properties** attached to it. The Console is the
administrative surface over that data model; plugins are the data sources
that populate it; and classification is the specific process of deriving
identity properties (what kind of device this is) from the raw data plugins
collect.

### Console functional areas

At a conceptual level, the Console organizes administrative work into a
small number of functional areas, though exact navigation labels vary by
release:

- **Asset inventory / Console view.** The primary operational screen: a
  filterable, sortable table (and associated dashboards) of every known
  host and its properties. Security operations and NAC administrators
  spend most of their time here.
- **Policy management.** The authoring surface for classification,
  compliance, and control policies (the policy engine covered in depth in
  [Chapter 3](03-clarification-compliance-and-control-policies.md)).
- **Plugin/module configuration.** Where each installed plugin is
  configured — credentials, scan/poll intervals, scope (which appliances
  run it, which IP ranges or switches it applies to).
- **Platform administration.** Appliance and Enterprise Manager health,
  user/role management, licensing, backup, and update management (covered
  in depth in [Chapter 4](04-host-management-administration-inventory-and-reporting.md)).
- **Reporting and dashboards.** Scheduled and ad hoc reports built from
  inventory and policy data (covered in depth in [Chapter 4](04-host-management-administration-inventory-and-reporting.md)).

### The plugin architecture

A plugin is a self-contained module that either (a) collects data about
hosts and writes it into properties, (b) exposes an action a control policy
can invoke, or (c) both. Plugins fall into rough categories useful for
exam-style domain mapping:

| Category | Examples | Primary contribution |
| --- | --- | --- |
| Network infrastructure | Switch, Wireless | Physical port location, VLAN/802.1X state, and the ability to execute VLAN/port control actions. |
| Endpoint inspection | HPS Inspection Engine (Windows), Linux/Unix plugin | Deep, credentialed endpoint state: installed software, running services, local configuration. |
| Directory and identity | Active Directory, LDAP | User/owner association, domain membership, group policy context. |
| Infrastructure telemetry | DHCP, NetFlow/IPFIX, DNS | Enrichment data that improves fingerprinting accuracy and fills gaps between active scan cycles. |
| Endpoint agent | SecureConnector | Optional lightweight client for environments where agentless visibility cannot answer a required compliance question. |
| eyeExtend integrations | SIEM, SOAR, ITSM, vulnerability management, MDM/UEM, EDR, firewall/NAC vendors | Bidirectional data exchange with third-party security and IT systems (covered in [Chapter 5](05-advanced-policy-integrations-and-business-outcomes.md)). |
| OT/ICS | eyeInspect sensor integration | Passive deep packet inspection of industrial protocols (covered in Chapters 8 and 9). |

Each plugin is licensed and enabled independently, is scoped to run on
specific appliances, and typically exposes its own configuration pane for
credentials and polling behavior. Because plugins run with elevated
credentials against switches, directories, or endpoints, plugin
configuration is itself a security-sensitive administrative activity — see
Security and Best Practices below.

### Properties: built-in and custom

A property is a single named attribute of a host record — for example, `IP
Address`, `Function`, `Operating System`, `Compliance Status`, or `Switch
Port`. The platform ships a large catalog of built-in properties populated
automatically by the discovery mechanisms and plugins described in
[Chapter 1](01-platform-architecture-installation-and-deployment-planning.md). Administrators can also define **custom properties** to track
organization-specific facts that no built-in property covers — for example,
an internally assigned asset-criticality tier, a business-unit owner tag
sourced from a CMDB integration, or a flag indicating a device is part of a
scoped compliance program (PCI DSS, for example). Custom properties behave
identically to built-in properties everywhere they are used: as policy
conditions, as inventory columns, and as report fields.

Design guidance: prefer a built-in property wherever one already captures
the fact you need, because built-in properties are maintained by the vendor
across releases and are automatically populated by existing plugins. Reach
for a custom property only when the fact is genuinely organization-specific
or must be sourced from a system the platform does not natively integrate
with (commonly resolved via a script or the Web API — see [Chapter 7](07-expert-automation-api-governance-and-capstone.md)).

### Classification

Classification is the process of deriving identity properties — most
importantly `Function` (for example, workstation, server, printer, IP
phone, IoT device, network infrastructure) and `Operating System` — from
the raw fingerprinting data plugins collect. The platform assigns
classification results a **confidence level**, reflecting how much
corroborating evidence supports the conclusion: a device fingerprinted by
DHCP options alone carries lower confidence than one corroborated by an
active scan banner and a directory lookup. Confidence level matters
operationally because compliance and control policies commonly gate
enforcement actions on a minimum classification confidence, so that a
device the platform is still unsure about is not misclassified into an
enforcement action it does not warrant (see [Chapter 3](03-clarification-compliance-and-control-policies.md) for the "clarification"
workflow that resolves low-confidence classifications).

## Design Considerations

- **Built-in vs. custom property strategy.** Establish a naming and
  documentation convention for custom properties before more than one
  administrator starts creating them; an undocumented sprawl of
  overlapping custom properties is a common source of policy logic errors
  in mature deployments.
- **Plugin credential scope.** Decide, per plugin, the minimum access level
  that satisfies the plugin's function (read-only SNMP community/user for
  Switch; a service account scoped to specific OUs for Active Directory;
  a least-privilege domain account for HPS). This is a security decision as
  much as a functional one.
- **Classification confidence thresholds.** Decide, per use case, what
  confidence level is acceptable before a device is treated as
  authoritatively classified for compliance or control purposes.
  Guest/BYOD onboarding may tolerate lower confidence than a policy gating
  access to a PCI-scoped VLAN.
- **Grouping and view design.** Design inventory groups and saved views
  around how operations staff will actually triage — by site, by function,
  by compliance status — rather than mirroring the raw property list.
  Overly granular groups increase maintenance burden without adding
  operational value.
- **Plugin scope vs. appliance load.** Running every plugin on every
  appliance is rarely correct; scope plugins (particularly endpoint
  inspection plugins) to the appliances actually responsible for the
  relevant IP ranges to avoid unnecessary load and redundant credentialed
  connections to the same endpoints from multiple appliances.
- **Tagging vs. properties.** Use lightweight tags for ad hoc,
  human-driven triage state (for example, "under investigation") and
  reserve formal custom properties for facts that policies need to
  evaluate programmatically.

## Implementation and Automation

1. **Review the built-in property catalog** before creating anything custom;
   most classification and compliance needs are covered by properties the
   platform already populates from installed plugins.
2. **Define a custom property** only after confirming no built-in property
   fits. Typical steps: name the property, choose its data type (string,
   list, boolean, numeric), decide whether it is manually editable, scriptable
   via the Web API, or populated by a specific plugin, and document its
   intended source of truth.
3. **Configure a new plugin** by supplying the credentials and scope it
   needs (for example, an SNMPv3 read-only user for the Switch plugin
   restricted to the access-layer switch IP range), then validate
   connectivity from the plugin's test/status view before saving.
4. **Build a basic classification policy.** Classification policies use the
   same condition/action structure as compliance and control policies
   (detailed in [Chapter 3](03-clarification-compliance-and-control-policies.md)): a set of conditions evaluated against host
   properties, and an action that sets a property (commonly `Function` or a
   custom classification tag) when the conditions match. A simple example in
   pseudocode form:

   ```text
   IF  Function is unknown/unclassified
   AND DHCP Vendor Class contains "MSFT"
   AND Open Ports includes 3389
   THEN set Function = "Windows Workstation"
   ```

5. **Order policy rules by specificity.** Classification policies evaluate
   rules top-down within a policy; place highly specific rules (matching a
   narrow, well-corroborated signature) above broad catch-all rules so a
   general rule does not pre-empt a more accurate specific one.
6. **Build inventory groups and views** that filter on the classification
   and compliance properties operations staff need daily — for example, a
   view of all hosts classified as `IoT` with a compliance status other
   than `Compliant`.
7. **Validate classification coverage** periodically by reviewing the
   percentage of hosts left in an unclassified or low-confidence state, and
   iterate on classification policy rules or add plugins to close the gap.

## Validation and Troubleshooting

- **A device is misclassified.** Open its host record and review the
  contributing properties and their source plugin; misclassification
  usually traces to a rule matching on an insufficiently specific
  condition (for example, matching purely on an open port that many device
  types share). Tighten the rule or add a corroborating condition.
- **A custom property never populates.** Confirm which mechanism was
  supposed to populate it (manual entry, script/API write, or a specific
  plugin) and verify that mechanism is actually configured and has run;
  a custom property with no defined source will simply stay empty
  indefinitely.
- **Plugin shows a credential or connectivity error.** Check the plugin's
  status/diagnostic pane for the specific failure reported (authentication
  failure, timeout, unreachable host) before assuming a broader network
  problem; most plugin failures are credential or ACL related rather than
  routing problems.
- **Classification confidence stays low across many hosts.** This usually
  indicates a missing corroborating data source — commonly that active
  scanning is disabled or too narrowly scoped, or that a directory plugin
  covering the affected segment is not yet configured.
- **Inventory view performance degrades** as host count grows. Prefer
  indexed/built-in property filters over complex custom-property text
  searches in high-host-count views, and confirm Console/EM sizing still
  matches current host count (see [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)).

## Security and Best Practices

- Apply least-privilege credentials to every plugin, and rotate
  plugin-owned service account credentials on the same cadence as other
  privileged service accounts in the environment.
- Restrict who can create or modify custom properties and classification
  policies; because classification results feed compliance and control
  decisions downstream, an incorrect classification rule can silently
  create false compliance or false control outcomes at scale.
- Document the intended source of truth for every custom property so a
  future administrator does not assume it is vendor-maintained.
- Avoid classification rules that rely solely on spoofable signals (a
  user-agent string or a DHCP vendor class alone) for any classification
  outcome that gates a control action; require corroboration from a
  harder-to-spoof source (switch port type, directory membership, or an
  active scan banner) before enforcement-sensitive classifications.
- Periodically audit unclassified and low-confidence hosts as a security
  hygiene task — an unusually large or growing unclassified population is
  itself a visibility gap worth investigating.

## References and Knowledge Checks

**References**

- [Forescout Technologies Console administration and plugin/module
  configuration guides for the 8.5.x release.](https://docs.forescout.com/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md) of this volume for the underlying appliance and discovery
  architecture that plugins depend on.
- [Forescout Technologies eyeExtend module catalog (official source for the
  current list of available integration plugins).](https://compatibility.forescout.com/eyeextend-products/)

**Knowledge Checks**

1. What is the relationship between a plugin, a property, and a host
   record?
2. Give one example each of a built-in property and a scenario that
   justifies creating a custom property instead.
3. Why does classification confidence matter when a compliance or control
   policy references a classification result?
4. Name two categories of plugin and one property each typically
   contributes.
5. Why should classification rules avoid relying solely on
   easily spoofed signals when the rule feeds an enforcement action?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each theme of the Console,
plugins, properties, and classification** — mapped in the volume README's chapter
outline. The Console is Forescout's primary interface, so these labs are Console
walkthroughs with CLI verification. Each ends **`**Lab verified by:** *pending*`** until
a human runs it.

**Shared prerequisites for Labs 2.1–2.4** — a Forescout deployment with the Console
connected and at least a handful of discovered hosts in the Asset Inventory. **Cost:**
none beyond lab resources.

### Lab 2.1 — Navigate the Console functional areas (Topic: Console layout)

**Objective:** Locate the four working areas an operator uses daily.

```text
# In the Console, open in turn:
#   - Asset Inventory   (hosts and their resolved properties)
#   - Policy            (Policy Manager: policies, rules, actions)
#   - Dashboard         (visualizations and NAC status)
#   - Reports           (scheduled/on-demand reporting)
```

**Expected result:** each area opens and reflects live deployment data — the Asset
Inventory is where visibility lands, the Policy Manager is where logic is built, and
Dashboards/Reports are where outcomes are communicated; fluency here is the foundation
the FSCE lab exam assumes.

**Negative test:** try to change enforcement from the Asset Inventory; actions are
authored in the Policy Manager — the inventory shows state, policies change it.

**Cleanup:** none (read-only navigation).

### Lab 2.2 — Manage a plugin (Topic: Plugin architecture)

**Objective:** Confirm a plugin is installed, running, and configured.

```text
# Console: Options > Plugins (Modules). Select a plugin (e.g. HPS Inspection Engine,
#   Switch, or a specific integration), confirm Status = Running/Installed, open its
#   configuration, and Apply.
fsctl status        # verify the platform service is up so plugins are active
```

**Expected result:** the plugin shows Running and its configuration is editable — plugins
are how Forescout resolves properties and takes actions (endpoint inspection, switch
control, integrations); the set of installed plugins defines what the platform can see
and do.

**Negative test:** write a policy that depends on a property resolved by a plugin that is
stopped or not installed; the property never resolves and the policy cannot match — the
plugin must be running for its properties to exist.

**Cleanup:** revert any plugin config changed only for the lab.

### Lab 2.3 — Read built-in versus custom properties (Topic: Properties)

**Objective:** Inspect a host's properties and note their source.

```text
# Console: Asset Inventory > select a host > Profile/Details. Review resolved
#   properties (e.g. Network Function, Operating System, Switch Port, Compliance).
#   Note which are built-in (plugin-resolved) vs custom (defined in your deployment).
```

**Expected result:** the host shows a mix of built-in properties (resolved by plugins)
and any custom properties your deployment defines — properties are the atoms policies
evaluate; understanding a property's source explains why it did (or did not) resolve.

**Negative test:** build policy logic on a property that only resolves after an active
scan, for hosts you only see passively; the property is blank and the rule misfires — a
property's resolution method must match how you actually see the host.

**Cleanup:** none (read-only).

### Lab 2.4 — Read the classification engine and confidence (Topic: Classification)

**Objective:** Confirm how a device is classified and with what confidence.

```text
# Console: Asset Inventory > select a device > review Function / OS / Vendor and Model.
#   Open the classification details to see the confidence level and the evidence
#   (properties) that drove the classification.
```

**Expected result:** the device carries a Function/OS/Vendor-Model classification with a
confidence indicator and the supporting evidence — the Device Classification Engine
fuses many properties into an identity, and confidence tells you how much to trust an
automated decision made on it.

**Negative test:** enforce a strict control on devices classified with low confidence;
you risk acting on a misidentified device — gate strong actions on high-confidence
classification (or add clarification first, Chapter 03).

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter mapped the Console's functional areas to the underlying data
model that every other Forescout capability builds on: plugins collect
data, properties store it on a host record, and classification derives
identity from it with an associated confidence level. It covered
built-in vs. custom property design, plugin categories and credential
scoping, and how to author and validate a basic classification policy rule.

**Completion checklist**

- [ ] Can describe the relationship between plugins, properties, and host
      records.
- [ ] Can articulate when a custom property is justified versus a built-in
      property.
- [ ] Understands classification confidence and why enforcement-sensitive
      rules should avoid easily spoofed signals.
- [ ] Completed the hands-on lab, including the negative test showing
      over-broad rule misclassification.
- [ ] Can design an inventory view/group aligned to an operational triage
      workflow.
