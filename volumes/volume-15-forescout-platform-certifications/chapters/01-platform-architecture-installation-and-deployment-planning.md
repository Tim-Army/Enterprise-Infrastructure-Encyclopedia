# Chapter 01: Platform Architecture, Installation, and Deployment Planning

![Lab topology for this chapter: a lab switch mirrors three test endpoints of distinct device types to the Forescout appliance's monitor interface; within minutes all three appear in the inventory with MAC, IP, and a provisional classification, and enabling scoped active scanning adds more specific detail. As a negative test, the SPAN destination interface is shut down on the switch; the Console reports the monitor interface down and no new host activity registers at all, demonstrating the platform's total dependency on a correctly delivered mirror feed. Re-enabling the interface resumes host updates immediately.](../../../diagrams/volume-15-forescout-platform-certifications/chapter-01-passive-visibility-span-topology.svg)

*Figure 1-1. Topology used throughout this chapter's Hands-On Lab: passive host discovery over a SPAN session, tested against an interrupted mirror feed.*

## Learning Objectives

- Describe the core components of the Forescout Platform architecture:
  Console, Enterprise Manager, appliances, plugins, and the policy engine.
- Differentiate physical appliance, virtual appliance, and cloud-hosted
  deployment models, and identify when each is appropriate.
- Explain how the platform achieves agentless device visibility, and the
  trade-offs of adding SecureConnector or credentialed access.
- Plan appliance placement relative to SPAN/mirror ports, network taps, and
  switch infrastructure for a given topology.
- Identify the licensed capability modules (eyeSight, eyeControl, eyeSegment,
  eyeExtend, eyeInspect) and map them to platform functionality.
- Apply pre-installation planning steps — network prerequisites, sizing, and
  high-availability posture — before a Forescout deployment begins.

## Theory and Architecture

The Forescout Platform (the current name for the product line historically
shipped as CounterACT) is a network-based visibility and control system. Its
central design premise is that an organization can discover, classify, and
govern every device that touches its network — managed endpoints, unmanaged
and IoT devices, OT/ICS assets, and transient guest devices — without
requiring a software agent to be pre-installed on the endpoint. This
distinguishes it from endpoint-agent-first approaches to asset management and
makes it a foundational control point for Network Access Control (NAC) and
Zero Trust network segmentation programs. This volume uses the
Forescout eyeSight/eyeControl Console baseline recorded in
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) (8.5.x, dated 2026-07);
menu paths and workflow details can shift between releases, so always confirm
against the release notes for the version in your environment.

### Architectural components

- **Forescout Appliance.** The workhorse of the platform. An appliance is a
  physical rack-mounted device or a virtual machine that performs traffic
  monitoring, active discovery, plugin execution, and local policy
  evaluation for the segment(s) of the network it is connected to. Each
  appliance runs a hardened Linux-based operating system purpose-built for
  the platform; administrators do not manage it as a general-purpose server.
- **Forescout Console.** The management application administrators use to
  configure policies, review the asset inventory, manage plugins, and
  monitor platform health. The Console is typically installed as a
  standalone management application (historically a Windows-hosted thick
  client, with browser-based administration expanding release over release)
  that connects to one or more appliances or to an Enterprise Manager.
- **Enterprise Manager (EM).** In multi-appliance deployments, the Enterprise
  Manager aggregates data from every managed appliance into a single pane of
  glass, distributes policy configuration to appliances, and provides a
  consolidated asset inventory. The EM is itself deployed as an appliance
  (physical or virtual) dedicated to that aggregation role rather than to
  direct traffic monitoring, though small deployments sometimes combine EM
  and appliance duties on one node.
- **Policy engine.** Every appliance runs a local instance of the policy
  engine, which evaluates classification, compliance, and control policies
  against the properties known for each host. Policies propagate from the
  Console/EM to appliances, but evaluation happens locally so that control
  actions are not dependent on a live link to central management.
- **Plugins (modules).** Plugins extend what the core appliance can see and
  do. Examples include the Switch plugin (SNMP/CLI reads from switching
  infrastructure for port-level location and 802.1X status), the Wireless
  plugin (WLAN controller integration), the HPS Inspection Engine (Windows
  management interfaces such as WMI/RPC for deep endpoint inspection), a
  Linux/Unix plugin (SSH-based inspection), and a large catalog of
  eyeExtend integration modules for third-party systems. Plugins are
  licensed and enabled independently, and each appliance loads only the
  plugins relevant to its role.
- **Asset inventory / properties store.** The classification and compliance
  data collected about every observed device is stored as a set of
  properties (built-in and custom) against a host record. This inventory is
  the shared substrate that classification, compliance, and control policies
  all read from and write to.

### Capability modules and licensing

Forescout licenses platform capability in named modules layered on the core
appliance:

| Module | Function |
| --- | --- |
| eyeSight | Baseline visibility: discovery, classification, and asset inventory. Required foundation for every other module. |
| eyeControl | Network access control actions: VLAN assignment, port block/restrict, endpoint isolation, guest/BYOD onboarding workflows. |
| eyeSegment | Segmentation visibility and policy modeling — maps traffic flows and proposes/enforces segmentation policy across switches and firewalls without requiring a redesign of the physical network. |
| eyeExtend | The integration framework and the individual connectors it ships (SIEM, SOAR, ITSM, vulnerability management, EDR/UEM, firewalls). |
| eyeInspect | OT/ICS-specific deep packet inspection, protocol dissection, and asset visibility for industrial networks (covered in depth in Chapters 8 and 9). |

A given deployment typically starts with eyeSight for visibility, then adds
eyeControl once the organization is confident classification and compliance
data are accurate enough to drive network actions safely.

### Discovery mechanisms

The platform combines several discovery techniques so that no single blind
spot determines visibility:

1. **Passive traffic monitoring.** An appliance interface connected to a
   SPAN/mirror port or a network tap observes traffic without being inline,
   fingerprinting devices from DHCP requests, ARP, HTTP headers, TLS
   handshakes, and other protocol chatter.
2. **Active scanning.** Where permitted, the appliance performs targeted
   probes (banner grabs, port scans, OS fingerprinting) against discovered
   IP addresses to fill gaps passive monitoring cannot resolve, using
   configurable scan intensity to avoid disrupting sensitive devices.
3. **Switch and wireless integration.** SNMP reads (and, on supported
   platforms, CLI or NETCONF integration) against access switches and WLAN
   controllers provide physical port location, CDP/LLDP neighbor data, and
   802.1X session state — the data eyeControl needs to act at the correct
   port.
4. **Infrastructure and directory plugins.** Integrations with DHCP servers,
   NetFlow/IPFIX exporters, Active Directory, MDM/UEM platforms, and cloud
   provider APIs enrich the inventory with data the network path alone
   cannot provide (owner, managed/unmanaged status, compliance posture).
5. **Endpoint-side access (optional).** SecureConnector — a small, dissolvable
   or persistent client — and the HPS Inspection Engine provide deeper,
   credentialed visibility into Windows and Linux endpoints (installed
   software, running processes, registry/configuration state) where
   agentless network-based fingerprinting is insufficient for a compliance
   check.

## Design Considerations

- **Physical vs. virtual vs. cloud appliances.** Physical appliances are
  sized and certified for a maximum sustained traffic rate and are the
  default choice for core-switch SPAN aggregation in a data center or campus
  core. Virtual appliances (deployable on common hypervisors) suit branch
  offices, smaller sites, or environments standardized on a virtualization
  platform, at the cost of depending on the host's network I/O path for
  SPAN/tap traffic delivery. Cloud-hosted appliance form factors extend
  visibility to workloads and virtual networks running in public cloud,
  typically consuming cloud-native traffic mirroring or API-based telemetry
  rather than a physical SPAN port.
- **In-band vs. out-of-band placement.** Most Forescout deployments are
  out-of-band: the appliance observes and reports on traffic it is not in
  the direct forwarding path of, reducing the platform's own availability
  requirements. Control actions (VLAN change, port shutdown, ACL push) are
  then executed indirectly against switches, wireless controllers, or
  firewalls via their management interfaces rather than by inserting the
  appliance inline. Inline enforcement is possible for select choke points
  but adds availability and failover requirements the architect must plan
  for explicitly.
- **SPAN/mirror capacity planning.** A SPAN or mirror port can typically
  aggregate only a fraction of the total bandwidth of the source ports
  feeding it before it drops frames under load. Where full campus- or
  data-center-wide visibility is required, plan for a dedicated
  aggregation/tap fabric (see the Gigamon-focused volume of this
  encyclopedia for detail on visibility fabrics) rather than a single
  oversubscribed SPAN session.
- **Sizing to host count and event rate**, not just link speed. Appliance
  sizing guidance is driven primarily by the number of concurrent hosts
  visible on the monitored segments and by the churn rate (DHCP
  lease/roaming rate on wireless and guest networks), because those numbers
  drive property update volume and policy re-evaluation frequency more than
  raw packet throughput does.
- **Enterprise Manager placement and redundancy.** In multi-site
  deployments, decide whether each site's appliance reports to a single
  central EM (simpler operations, single pane of glass, but a
  wide-area-network dependency for cross-site correlation) or whether
  regional EMs are used with a summary rollup. Plan EM sizing around total
  managed host count and appliance count, not local traffic volume.
- **High availability.** Determine which appliances are single points of
  failure for a compliance-critical control action (e.g., the only
  appliance able to quarantine a segment) and plan HA appliance pairs or
  compensating manual procedures accordingly.
- **Change control for control actions.** Because eyeControl can actively
  change a device's network state, plan a staged rollout: visibility-only
  (eyeSight) first, compliance policies in monitor/report mode next, and
  control (enforcement) actions last, gated by a defined change-management
  and rollback process.

## Implementation and Automation

The following sequence reflects a typical greenfield deployment plan. Exact
menu paths vary by release; consult the installation guide shipped with your
licensed 8.5.x build.

1. **Confirm prerequisites.** DNS resolution (forward and reverse) for the
   Console/EM and every appliance, NTP synchronization across all
   components, and a management-network path between the Console, the EM,
   and every appliance on the ports documented in the installation guide.
2. **Deploy the Enterprise Manager and appliance(s).** For physical
   appliances, rack, cable management and monitor interfaces, and power on;
   for virtual appliances, deploy the vendor-supplied OVA/template with the
   documented vCPU, memory, and disk allocations for the target host-count
   tier.
3. **Run initial setup.** Each appliance and the EM expose a console-based
   (serial/KVM or virtual console) initial configuration wizard for
   hostname, management IP, DNS, NTP, and the initial administrative
   credential. Change default credentials immediately as part of this step.
4. **Register appliances to the Enterprise Manager** (multi-appliance
   deployments) so that policy and inventory data centralize correctly.
5. **License the deployment.** Apply the license file(s) covering the
   purchased capability modules (eyeSight at minimum) and the licensed host
   count.
6. **Connect monitor interfaces.** Cable each appliance's monitor
   interface(s) to the planned SPAN/mirror session or tap, and confirm the
   switch-side SPAN configuration matches the intended source VLANs/ports.
   Example Cisco IOS SPAN configuration mirroring a VLAN to the appliance's
   monitor port:

   ```text
   monitor session 1 source vlan 100
   monitor session 1 destination interface GigabitEthernet1/0/24
   ```

7. **Verify passive visibility.** From the Console, confirm hosts on the
   monitored segment begin appearing in the asset inventory within a few
   minutes, with basic properties (MAC, IP, DHCP fingerprint) populated.
8. **Enable targeted active scanning** for the discovered IP ranges, tuned
   to a scan intensity appropriate for the segment (production data center
   ranges typically use a lighter touch than office/campus ranges).
9. **Add switch and wireless plugins** with read-only SNMP/API credentials
   scoped to the access layer, and validate that port-location properties
   populate for a sample of known hosts.
10. **Layer in directory and infrastructure plugins** (Active Directory,
    DHCP, MDM/UEM) to enrich classification confidence before any
    compliance or control policy is authored.
11. **Baseline in monitor-only mode** for an agreed observation period
    before authoring any compliance or control policy that takes action, so
    that classification accuracy can be validated against known assets
    first.

## Validation and Troubleshooting

- **No hosts appearing after cabling a SPAN port.** Confirm the switch SPAN
  session is active and sourcing the intended VLAN/ports (`show monitor
  session 1` on Cisco IOS), that the appliance's monitor interface is
  administratively up, and that the interface is bound to the correct
  monitor role in the appliance configuration (a monitor interface
  misconfigured as a management interface, or vice versa, is the most
  common first-deployment error).
- **Appliance not registering to the Enterprise Manager.** Verify DNS
  resolution in both directions, that the required management ports are open
  between appliance and EM, and that system clocks are within tolerance —
  certificate-based trust between appliance and EM commonly fails silently
  when clocks drift.
- **Partial or stale properties.** Cross-check which plugin is expected to
  supply a given property; a stale switch-port-location property usually
  traces back to an SNMP credential that changed on the switch side without
  a corresponding update in the plugin configuration.
- **Active scan not returning OS fingerprint data.** Confirm that any
  intermediate firewall or ACL between the appliance and the target segment
  is not blocking the scan traffic, and that the scan policy's IP range
  actually includes the target subnet.
- **Console/EM performance degradation.** Check appliance and EM resource
  utilization (CPU, memory, disk) against the sizing guidance for the
  current host count; a common root cause is host count growth (new
  IoT/guest segments monitored) outpacing the original sizing exercise.

## Security and Best Practices

- Change all default administrative credentials during initial setup, and
  integrate Console administrative accounts with centralized
  authentication (RADIUS/LDAP/SAML, per the current release's supported
  identity provider list) rather than relying on local accounts long-term.
- Scope plugin credentials (switch SNMP, AD service accounts, HPS/WMI
  credentials) to least privilege — read-only where the plugin's function
  permits it, and dedicated service accounts rather than reused
  administrative credentials.
- Treat the appliance's monitor interfaces as a data-diode-style
  receive-only path: monitor ports should not also serve as production
  management or data interfaces.
- Encrypt and restrict management-plane access to the Console and EM (a
  dedicated out-of-band management VLAN is standard practice) since
  compromise of the Console would expose the full asset inventory and
  policy/control capability of the platform.
- Stage control-capable policies through monitor/report mode before
  enabling live enforcement, and maintain a documented rollback plan
  (disable policy, or set to report-only) that on-call staff can execute
  without deep platform expertise during an incident.
- Keep appliance firmware/OS and plugin versions current against vendor
  advisories; because the platform has privileged read access into
  switches, directories, and endpoints, it is a high-value target if
  compromised.

## References and Knowledge Checks

**References**

- [Forescout Technologies official product documentation portal (Forescout
  Platform / Console administration and installation guides for the 8.5.x
  release).](https://docs.forescout.com/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  dated baseline (Forescout eyeSight/eyeControl Console 8.5.x, 2026-07).
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA/FSCP/FSCE blueprint domain mapping for this volume.
- [Forescout Technologies certification and training catalog (official
  source for current FSCA/FSCP/FSCE blueprint domains and exam
  registration).](https://www.forescout.com/support-hub/training/)

**Knowledge Checks**

1. What is the functional difference between the Forescout Console and an
   Enterprise Manager, and when does a deployment need both?
2. Name three discovery mechanisms the platform combines to build device
   visibility, and describe one blind spot each mechanism alone would leave.
3. Why do most production deployments place the appliance out-of-band
   relative to the traffic it monitors, and what does that imply for how
   control actions are executed?
4. Which capability module must be licensed before eyeControl,
   eyeSegment, or eyeInspect data becomes meaningful, and why?
5. List two sizing inputs besides raw link bandwidth that determine
   appliance capacity requirements.

## Hands-On Lab

**Objective.** Stand up passive visibility on a lab appliance and validate
that host discovery and basic classification work end to end before any
control policy is introduced.

**Prerequisites**

- A lab or trial Forescout virtual appliance already deployed and licensed
  for eyeSight, with Console/EM access.
- A lab switch capable of configuring a SPAN/mirror session (or a hub/tap if
  no manageable switch is available).
- At least three test endpoints on the mirrored segment with distinct
  device types (for example, a Windows VM, a Linux VM, and a phone or IoT
  simulator) so classification differences are observable.
- Administrative access to the lab switch CLI.

**Procedure**

1. On the lab switch, configure a SPAN session sourcing the VLAN or ports
   the test endpoints live on, destined to the appliance's monitor
   interface:

   ```text
   monitor session 1 source interface GigabitEthernet1/0/1 - 3
   monitor session 1 destination interface GigabitEthernet1/0/10
   ```

2. In the Console, confirm the appliance's monitor interface is enabled and
   bound correctly, then open the asset inventory view.
3. Generate traffic from each test endpoint (a DHCP renewal, a web browse,
   a ping to another host on the segment) to accelerate fingerprinting.
4. Within a few minutes, confirm all three test endpoints appear in the
   inventory with at minimum a MAC address, an IP address, and a
   provisional classification (function/OS guess).
5. Open one endpoint's host record and review which plugin/data source
   populated each property — this confirms you understand the
   property-to-source mapping used throughout later chapters.
6. Enable active scanning scoped only to the lab subnet, and re-observe the
   same three hosts; note which properties become more specific (for
   example, OS version detail) after the active scan runs.
7. **Negative test.** Temporarily shut down the SPAN destination interface
   on the switch (`shutdown` on the destination interface configuration) and
   confirm in the Console that the appliance reports the monitor interface
   as down and that no new host activity registers, demonstrating the
   platform's dependency on a correctly delivered mirror feed. Re-enable
   the interface afterward and confirm hosts resume updating.

**Expected Results**

- All three test endpoints are visible in the inventory with populated MAC,
  IP, and provisional classification properties.
- Property source attribution is visible and matches the plugins enabled in
  this lab (passive fingerprinting and, after step 6, active scan).
- The negative test clearly demonstrates loss of visibility when the SPAN
  feed is interrupted, and recovery once it is restored.

**Cleanup**

- Disable active scanning if the lab subnet will be reused for a shared
  purpose, to avoid unexpected scan traffic later.
- Remove the SPAN session from the switch if the interfaces are needed for
  another lab (`no monitor session 1`).
- Leave the appliance's base configuration in place; it is reused in later
  chapters' labs.

## Summary and Completion Checklist

This chapter established the architectural vocabulary used throughout the
rest of the volume: appliances, the Enterprise Manager, the Console, the
policy engine, and the plugin model that extends visibility and control. It
covered the capability modules (eyeSight, eyeControl, eyeSegment, eyeExtend,
eyeInspect) and the discovery mechanisms — passive monitoring, active
scanning, switch/wireless integration, directory/infrastructure plugins, and
optional endpoint-side access — that together build the asset inventory
every later policy type depends on. It also covered deployment planning
decisions (physical/virtual/cloud appliance choice, in-band vs. out-of-band
placement, SPAN capacity, sizing, and HA) and walked through an installation
and validation sequence.

**Completion checklist**

- [ ] Can name and describe the role of the Console, Enterprise Manager,
      appliance, policy engine, and plugin architecture.
- [ ] Can map each capability module (eyeSight/eyeControl/eyeSegment/
      eyeExtend/eyeInspect) to the functionality it unlocks.
- [ ] Can explain the difference between passive, active, and
      infrastructure-plugin discovery.
- [ ] Completed the hands-on lab and observed both successful discovery and
      the negative-test loss of visibility.
- [ ] Understands why control-capable policies are staged through
      monitor/report mode before enforcement.
