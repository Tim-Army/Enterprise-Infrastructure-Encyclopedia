# Chapter 02: Console, Plugins, Properties, and Asset Classification

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

**Objective.** Configure a custom property, author a basic classification
policy, and validate classification coverage using an inventory view.

**Prerequisites**

- The lab appliance and Console from [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)'s lab, with passive
  visibility already validated.
- At least one test endpoint whose `Function` property is currently
  unclassified or generic.
- Console access with permission to create properties and policies.

**Procedure**

1. In the Console, review the current property set on your unclassified
   test endpoint and note which properties are already populated (MAC, IP,
   open ports, DHCP data) versus empty.
2. Create a custom property named `Lab Asset Owner` (string type, manually
   editable) and set its value on the test endpoint to your name or team,
   confirming it appears alongside built-in properties on the host record.
3. Author a classification policy rule that sets `Function` based on a
   condition your test endpoint matches (for example, an open-port or
   DHCP-vendor-class condition specific to that device type).
4. Apply the policy and trigger re-evaluation (many deployments
   re-evaluate on a schedule or on demand from the policy view); confirm
   the test endpoint's `Function` property updates to the value your rule
   set.
5. Build an inventory view/group filtered to `Function` equals the value
   you set, and confirm the test endpoint appears while unrelated hosts do
   not.
6. **Negative test.** Temporarily broaden your classification rule's
   condition to something deliberately too generic (for example, matching
   only on a single common open port with no other condition), reapply it,
   and observe that it now incorrectly matches at least one other host on
   the segment. This demonstrates why rule specificity and ordering matter.
   Revert the rule to its specific form afterward.

**Expected Results**

- The custom property is visible and correctly scoped to the test
  endpoint.
- The classification policy correctly sets `Function` on the intended
  endpoint under the specific rule, and the inventory view correctly
  filters on it.
- The negative test visibly demonstrates over-broad-rule misclassification
  and is reverted cleanly.

**Cleanup**

- Delete or disable the lab classification policy rule if it should not
  persist beyond the lab.
- Remove the `Lab Asset Owner` custom property and its value, or leave it
  in place if subsequent chapter labs will reuse it (later labs in this
  volume assume it may still exist but do not require it).
- Remove the temporary inventory view if it was created only for this
  exercise.

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
