# Chapter 02: NSE 2 Threat Landscape, Security Technologies, and Fortinet Portfolio

![Lab flow for this chapter: a technology-to-risk inventory for a scenario organization marks each security technology category deployed, partial, or not deployed, with each gap's uncovered kill-chain stage mapped against one current, real attack technique from public threat intelligence. As a negative test, one category is deliberately marked deployed with no corresponding real enforcement point; re-reading the inventory as an independent reviewer, the unsupported claim is identifiable from the coverage notes alone, proving coverage notes must describe actual enforcement, not just product ownership.](../../../diagrams/volume-19-fortinet-network-security/chapter-02-technology-risk-inventory-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: a technology-to-risk inventory validated against public threat intelligence, tested against a deliberately unsupported coverage claim.*

## Learning Objectives

- Describe the evolution of cybercrime from individual actors to organized,
  service-based criminal ecosystems, including ransomware-as-a-service.
- Explain the cyber kill chain and how it maps attacker objectives to
  defensive control points.
- Identify the major security technology categories an enterprise deploys
  and the specific gap each one closes.
- Map each technology category to the corresponding Fortinet Security
  Fabric product family.
- Build a technology-to-risk inventory usable as an organizational planning
  artifact.

## Theory and Architecture

### The evolution of cybercrime

Early network intrusion activity was dominated by individuals motivated by
curiosity or reputation — the "script kiddie" era, where attacks used
widely shared, unsophisticated tools against opportunistic targets.
Cybercrime has since restructured into a layered criminal economy with
specialization comparable to any legitimate service industry:

- **Access brokers** compromise and sell footholds (stolen VPN credentials,
  exposed RDP endpoints, exploited vulnerabilities) to other criminal
  actors rather than exploiting the access themselves.
- **Ransomware-as-a-service (RaaS)** operators develop and lease ransomware
  toolkits and negotiation infrastructure to affiliates, who carry out the
  actual intrusion and split extortion proceeds with the operator.
- **Malware-as-a-service** vendors sell or rent loaders, credential
  stealers, and botnets on a subscription basis, lowering the technical bar
  to entry.
- **Nation-state and state-aligned actors** pursue espionage, intellectual
  property theft, or critical infrastructure disruption with resourcing and
  persistence far beyond financially motivated crime.
- **Supply chain compromise** targets a trusted software vendor, update
  mechanism, or managed service provider once, gaining access to every
  downstream customer simultaneously — a force multiplier that has driven
  some of the highest-impact incidents of the last decade.

This shift matters architecturally: defending against a lone opportunistic
attacker and defending against a well-funded, patient affiliate using
purchased tooling and negotiated extortion playbooks are different
problems, and modern control design assumes the latter.

### The cyber kill chain

The kill chain (originally formalized by Lockheed Martin, and reflected in
similar form in the MITRE ATT&CK framework's tactic categories) models an
intrusion as a sequence of stages, each of which is an opportunity for
defensive interruption rather than a single point of failure:

| Stage | Attacker objective | Representative defensive control |
| --- | --- | --- |
| Reconnaissance | Identify targets, exposed services, personnel | Attack surface management, awareness training ([Chapter 01](01-nse-1-cybersecurity-awareness-and-digital-safety.md)) |
| Weaponization | Pair an exploit with a deliverable payload | Threat intelligence, patch management |
| Delivery | Get the payload to the target (email, web, USB, supply chain) | Secure email gateway, web filtering, sandboxing |
| Exploitation | Trigger the vulnerability or user action | IPS, endpoint protection, application control |
| Installation | Establish persistence on the compromised host | Endpoint detection and response (EDR), application allow-listing |
| Command and control (C2) | Establish outbound communication to attacker infrastructure | DNS filtering, botnet/C2 signature detection, egress firewall policy |
| Actions on objectives | Exfiltrate data, deploy ransomware, pivot laterally | Data loss prevention, network segmentation, backup/recovery |

No single technology interrupts every stage. Defense-in-depth architecture
deliberately layers controls so that a failure at one stage (a user who
clicks a malicious link) is still contained by a control at a later stage
(sandboxing the delivered file, or IPS blocking the resulting exploit
attempt). This chapter's technology survey is organized around exactly
which kill-chain stage(s) each category interrupts.

### Security technology categories

| Category | Kill-chain stage(s) addressed | Function |
| --- | --- | --- |
| Next-generation firewall (NGFW) | Delivery, exploitation, C2 | Stateful inspection plus application awareness, user identity, and integrated IPS at the network perimeter and internal segmentation points |
| Intrusion prevention system (IPS) | Exploitation | Signature- and behavior-based blocking of known exploit patterns against vulnerable services |
| VPN (site-to-site and remote access) | N/A (transport security) | Confidentiality and integrity for traffic crossing an untrusted network |
| Sandboxing | Delivery, exploitation | Detonates unknown files in an isolated environment to observe behavior before the payload reaches a real endpoint |
| Endpoint protection / EDR | Installation, actions on objectives | Detects and responds to malicious behavior on the host itself, independent of network visibility |
| SD-WAN | N/A (transport/performance) | Application-aware path selection across multiple WAN circuits; increasingly bundled with security enforcement ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)) |
| Secure email gateway | Delivery | Filters phishing, malware attachments, and business email compromise attempts before they reach a mailbox |
| Web application firewall (WAF) | Exploitation | Protects internet-facing applications against injection, request forgery, and other application-layer attacks |
| Cloud security (CASB/CNAPP) | Reconnaissance, actions on objectives | Visibility and policy enforcement over SaaS usage and cloud workload configuration/posture |
| Network access control (NAC) | Reconnaissance, installation | Identifies and controls what devices are permitted to join the network, including unmanaged and IoT/OT devices |
| SIEM / SOAR | All stages (detection and response) | Aggregates and correlates logs across the estate, and automates response playbooks |

### The Fortinet Security Fabric portfolio

Fortinet organizes its product portfolio as fabric components that share
telemetry and can be centrally orchestrated, rather than as independent
point products. The following mapping connects each technology category
above to its primary Fortinet product family; [Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md) covers the
Security Fabric's architectural integration in depth.

| Technology category | Fortinet product family |
| --- | --- |
| Next-generation firewall | FortiGate |
| Central firewall/VPN management | FortiManager |
| Security analytics and logging | FortiAnalyzer |
| Endpoint protection / EDR | FortiClient / FortiEDR |
| Endpoint fleet management | FortiClient EMS |
| Wireless access | FortiAP |
| Switching | FortiSwitch |
| Sandboxing | FortiSandbox |
| Secure email gateway | FortiMail |
| Web application firewall | FortiWeb |
| Network access control | FortiNAC |
| SOAR | FortiSOAR |
| SIEM | FortiSIEM |
| Cloud security posture / CNAPP | FortiCNP |
| Application delivery controller | FortiADC |
| Deception technology | FortiDeceptor |
| Managed service provider portal | FortiPortal |

Fortinet also maintains a **Fabric-Ready Partner** ecosystem: third-party
products (identity providers, SIEM platforms, cloud providers, ticketing
systems) integrate with the Security Fabric through published APIs and
Fabric Connectors rather than requiring an entirely closed, single-vendor
estate. This matters for enterprise architecture decisions: an
organization is not forced into an all-Fortinet stack to benefit from
Security Fabric telemetry sharing, though the deepest integration exists
between native fabric components.

## Design Considerations

- **Technology category coverage before product selection.** Before naming
  a vendor, an architect should confirm which kill-chain stages are
  currently uncovered for the organization's specific risk profile —
  buying a second NGFW does nothing for an organization whose actual gap is
  endpoint visibility or email filtering.
- **Best-of-breed vs. platform consolidation trade-off.** A best-of-breed
  approach (selecting the strongest independent product per category)
  maximizes per-category capability at the cost of integration effort and
  fragmented visibility; a platform approach (Fortinet Security Fabric,
  or an equivalent single-vendor fabric) trades some per-category
  best-in-class capability for shared telemetry, a single management plane,
  and faster automated response across products. Most mature enterprises
  land somewhere between the two, consolidating on a platform for the
  highest-volume, highest-integration-value categories (firewall, endpoint,
  SIEM/SOAR) while keeping best-of-breed products where a category has a
  dominant specialist.
- **RaaS-aware architecture.** Because ransomware affiliates now purchase
  rather than build their tooling, assume attacker technique is broadly
  known and commoditized; the organization's differentiator is detection
  speed and segmentation (limiting blast radius), not obscurity of its
  environment.
- **Supply chain exposure inventory.** Technology category planning should
  explicitly include the organization's own software supply chain and
  managed service provider relationships as an attack surface, not only its
  directly operated infrastructure.

## Implementation and Automation

NSE 2-level material precedes hands-on FortiOS configuration, which begins
in [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md). The practical deliverable at this stage is a structured
planning artifact: a technology-to-risk inventory that an organization (or
a student building a portfolio) can produce and keep under version control
alongside the rest of its infrastructure-as-code, consistent with this
encyclopedia's documentation-as-code approach ([Volume I](../../volume-01-enterprise-engineering-foundations/README.md)).

```yaml
# security-technology-inventory.yaml
# Maps recognized risk against deployed technology category and product.
organization: "NSE Lab Enterprises"
last_reviewed: "2026-07-18"
categories:
  - category: "Next-generation firewall"
    kill_chain_stage: ["delivery", "exploitation", "command-and-control"]
    deployed: true
    product: "FortiGate"
    coverage_notes: "HQ and branch perimeter; internal segmentation pending (Chapter 06)."
  - category: "Sandboxing"
    kill_chain_stage: ["delivery", "exploitation"]
    deployed: false
    product: "FortiSandbox (planned)"
    coverage_notes: "Currently relying on signature-based AV only; gap identified."
  - category: "Secure email gateway"
    kill_chain_stage: ["delivery"]
    deployed: false
    product: "FortiMail (evaluation in progress)"
    coverage_notes: "Primary phishing delivery vector remains uncovered by a dedicated gateway."
  - category: "Endpoint protection / EDR"
    kill_chain_stage: ["installation", "actions-on-objectives"]
    deployed: true
    product: "FortiClient / FortiEDR"
    coverage_notes: "Deployed to managed laptops; BYOD posture checking not yet enforced."
  - category: "Network access control"
    kill_chain_stage: ["reconnaissance", "installation"]
    deployed: false
    product: "FortiNAC (planned)"
    coverage_notes: "No automated control over unmanaged/IoT device onboarding today."
```

Maintaining this inventory as structured data (rather than a slide deck)
allows it to be diffed over time, reviewed in a pull request alongside
other architecture decisions, and referenced directly when justifying a
budget request against a named, unaddressed kill-chain stage.

## Validation and Troubleshooting

- **Coverage claimed but not enforced.** A product being "deployed" is not
  the same as a control being effective — confirm sandboxing is actually
  in the inspection path (not running in a monitor-only pilot mode
  indefinitely), and that secure email gateway rules are not bypassed by a
  legacy direct-to-mailbox mail route left over from a migration.
  Chapters 04–08 return to this distinction between configured and
  effective controls at the FortiGate policy level.
- **Stale inventory as a false sense of coverage.** An inventory that is
  not revisited after an acquisition, a new SaaS adoption, or a cloud
  migration will misrepresent current risk; treat `last_reviewed` staleness
  itself as a finding.
- **Kill-chain stage gaps hiding behind category-level completeness.** Two
  organizations can both claim "NGFW deployed" while one enforces
  east-west segmentation and the other does not — record coverage notes at
  the level of actual enforcement, not just product ownership.
- **Alert fatigue undermining SIEM/SOAR value.** A SIEM ingesting
  high-volume, low-fidelity logs without tuning produces so many alerts
  that real detections are missed in the noise; this is a technology
  category failure mode distinct from simply "not having a SIEM," and is
  covered operationally in [Volume XI](../../volume-11-observability-enterprise-operations/README.md).

## Security and Best Practices

- Prioritize closing kill-chain-stage gaps that address the delivery and
  exploitation stages first for most organizations — interrupting an
  attack early is cheaper than detecting it after installation or
  exfiltration.
- Do not evaluate a technology category purchase in isolation from the
  Security Fabric's existing telemetry-sharing capability; a product that
  cannot share detection context with the rest of the fabric loses much of
  its incremental value in a platform-consolidated architecture.
- Revisit the technology-to-risk inventory on a fixed cadence (at minimum
  annually, and after any material infrastructure or business change such
  as an acquisition or new cloud adoption).
- Treat ransomware-as-a-service commoditization as the current baseline
  threat capability when sizing controls — assume any organization,
  regardless of size or perceived obscurity, is a viable target for an
  affiliate operating at scale against many victims simultaneously.
- Cross-reference this chapter's category gaps against [Volume X](../../volume-10-enterprise-cybersecurity/README.md) (Enterprise
  Cybersecurity) for vendor-neutral control design principles that apply
  regardless of which product fills a given category.

## References and Knowledge Checks

**References**

- [Fortinet NSE Training Institute, *NSE 2: Network Security Associate*
  learning path (threat landscape and technology modules).](https://training.fortinet.com/local/staticpage/view.php?page=nse_2)
- [Lockheed Martin, *Cyber Kill Chain* framework.](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html)
- [MITRE ATT&CK, tactics and techniques matrix.](https://attack.mitre.org/)
- [Fortinet, *Security Fabric* architecture and product portfolio
  documentation.](https://docs.fortinet.com/security-fabric)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — encyclopedia-wide
  dated baseline reference.

**Knowledge checks**

1. Name two ways the ransomware-as-a-service model changes the assumed
   attacker profile compared to a lone opportunistic actor.
2. Which kill-chain stage does sandboxing primarily interrupt, and why is
   it complementary to signature-based antivirus rather than a
   replacement for it?
3. Give one example each of a technology category best suited to
   best-of-breed selection and one best suited to platform consolidation,
   with justification.
4. Which two Fortinet product families provide central management and
   centralized log analytics, respectively, across a fleet of FortiGate
   devices?

## Hands-On Lab

**Objective:** Build a technology-to-risk inventory for a defined scenario
organization and validate it against a public threat intelligence source —
no FortiGate hardware or lab appliance is required for this chapter.

**Prerequisites**

- A text editor and the ability to write YAML.
- Internet access to a public threat intelligence resource (for example, a
  vendor's published threat landscape report or a public threat map).

**Scenario:** A 400-employee organization with a single headquarters site,
two remote branch offices, a hybrid workforce, and a customer-facing web
application hosted in a public cloud provider.

**Steps**

1. List every technology category from the Theory and Architecture table
   and mark each as deployed, partially deployed, or not deployed for the
   scenario organization, using your own reasonable assumptions for a
   typical organization of this size.

2. For each category marked not deployed, identify which kill-chain
   stage(s) remain uncovered as a result.

3. Consult a current public threat intelligence source (a vendor threat
   landscape report or public threat map) and identify one currently
   prominent attack technique (for example, a specific initial-access
   vector or a specific ransomware family's delivery method).

4. Map that current technique against your inventory: does an existing
   deployed category interrupt it, or does it exploit one of the gaps
   identified in step 2?

5. Write the findings as a `security-technology-inventory.yaml` file
   following the format shown in Implementation and Automation, including
   a `coverage_notes` field that references the specific technique
   identified in step 3 for any category you mark as a gap.

6. **Negative test:** Deliberately mark the web application firewall
   category as "deployed: true" without a corresponding enforcement point
   in front of the scenario's public-cloud-hosted customer application
   (i.e., claim coverage that does not actually exist), then re-read your
   own inventory as if you were an independent reviewer — confirm you can
   identify the unsupported claim from the coverage notes alone. This
   demonstrates why coverage notes must describe actual enforcement, not
   just product ownership.

7. Correct the negative-test entry to accurately reflect the gap.

**Expected result:** A version-controllable YAML inventory with at least
eight technology categories, each with an accurate deployment status and a
coverage note tied to a real, current threat technique for at least one gap
entry.

**Cleanup**

- No system changes to revert; retain the inventory file as a reference
  artifact for [Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md)'s Security Fabric mapping exercise.

## Summary and Completion Checklist

This chapter traced cybercrime's evolution from individual actors to a
specialized criminal service economy, introduced the cyber kill chain as
the organizing model for where defensive technology categories intervene,
surveyed the major enterprise security technology categories, and mapped
each to its corresponding Fortinet Security Fabric product family. The
technology-to-risk inventory produced in the hands-on lab is a reusable
planning artifact that [Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md) extends into Security Fabric
architecture, and that Chapters 04–09 fill in with actual FortiGate
configuration.

- [ ] Can describe the shift from individual attackers to
      ransomware-as-a-service and supply chain compromise models.
- [ ] Can map at least six security technology categories to the
      kill-chain stage(s) each interrupts.
- [ ] Can name the Fortinet product family corresponding to each major
      technology category.
- [ ] Can articulate the best-of-breed vs. platform consolidation
      trade-off.
- [ ] Completed the hands-on lab, including the negative test.
