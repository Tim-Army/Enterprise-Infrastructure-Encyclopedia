# Chapter 08: Role-Based Certification Portfolio and Enterprise Capstone

![Lab topology for this chapter: a data-center HA pair and a branch firewall bootstrap into Panorama-defined device groups and template stacks under a Global-Baseline hierarchy; a Shared pre-rule blocks known-malicious categories globally while device-group-scoped allow rules with attached inspection profiles permit legitimate traffic at each site, a phased decryption rule pair excludes financial-services, centralized logging confirms traffic from all three firewalls, and a bulk API script creates address objects on the branch firewall. As a negative test, a local rule added directly on the branch firewall attempts to permit the category the Shared pre-rule blocks; the policy match still reports the Shared pre-rule as the matching rule, not the local override, confirming Shared pre-rules evaluate ahead of local firewall rules and cannot be bypassed by local configuration.](../../../diagrams/volume-16-palo-alto-networks-security/chapter-08-capstone-panorama-prerule-override-topology.svg)

*Figure 8-1. Topology used throughout this chapter's Hands-On Lab: the full Panorama-governed capstone — data-center HA pair and branch firewall — validated end to end, tested against a local policy-override attempt.*

## Learning Objectives

- Map the role-based certification portfolio — Network Security Analyst,
  Next-Generation Firewall Engineer, and the Professional and Architect
  tiers — to the chapters and hands-on labs in this volume.
- Plan a study path from Cybersecurity Apprentice/Practitioner (Chapters
  01–02) through role-based, hands-on certification, sequenced against
  actual configuration repetition rather than passive review alone.
- Design an integrated, multi-firewall PAN-OS deployment that combines
  VM-Series, networking/HA, security policy, and Panorama management into
  a single coherent architecture.
- Build and validate that integrated deployment end to end in a capstone
  lab, demonstrating the full skill set developed across Chapters 03–07.
- Self-assess readiness against the role-based blueprint domains using a
  structured checklist rather than exam-question rehearsal.

## Theory and Architecture

[Chapter 01](01-cybersecurity-apprentice-foundations.md) introduced the Cybersecurity Apprentice credential as
vendor-adjacent and portfolio-wide; [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md) built Cybersecurity
Practitioner depth across Strata, Prisma, and Cortex. This chapter closes
the loop: the **role-based certification portfolio** — anchored at the
Specialist tier by Network Security Analyst and Next-Generation Firewall
Engineer — assumes exactly the hands-on configuration skill this volume's
Chapters 03 through 07 were built to develop, and requires demonstrable
muscle memory with the CLI and Web UI rather than conceptual recall alone.

### The role-based certification portfolio

Palo Alto Networks **retired its product-centric exams during 2025** —
PCNSA on 31 January and PCNSE on 31 July, along with PCCET, PCDRA, PCCSE,
PCSAE, and PCSFE. They were replaced by a role-based portfolio of four
levels across three tracks. A reader holding PCNSA or PCNSE still holds a
valid credential; there is simply no longer an exam by that name to sit,
and the material below is where that knowledge now maps.

The Network Security track, which this volume covers:

| Level | Certification | Chapters |
| --- | --- | --- |
| Foundational | Cybersecurity Apprentice | 01 |
| Foundational | Cybersecurity Practitioner | 02 |
| Professional | Network Security Professional | 02–05 |
| Specialist | Network Security Analyst | 05 |
| Specialist | Next-Generation Firewall Engineer | 03, 04, 06, 07 |
| Specialist | SD-WAN Engineer | 04 |
| Specialist | Security Service Edge Engineer | 02 |
| Architect | Network Security Architect | 08 |

The Security Operations and Cloud Security tracks sit outside this
volume's scope, except where
[Chapter 09](09-cortex-cloud-security-professional.md) reaches into
Cortex.

**Where the retired exams went.** Network Security Analyst is the closest
successor to PCNSA — policy and object creation, day-to-day operations.
Next-Generation Firewall Engineer is the closest successor to PCNSE, and
is the exam most readers of Chapters 03–07 will be aiming at.

### Blueprint domains and weights

Weights below come from each certification's official datasheet; each set
totals 100%. Datasheets are revised — the dates given are the versions
these tables were taken from.

**Next-Generation Firewall Engineer** (datasheet dated November 2025).
Recommended experience: 2–3 years in IT security, 2 years with Palo Alto
Networks NGFW. Recommended prior certifications: Network Security
Professional and Network Security Analyst.

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1. PAN-OS Networking Configuration | 40% | 04 |
| 2. PAN-OS Device Setting Configuration | 40% | 03, 05, 06 |
| 3. Integration and Automation | 20% | 03, 06, 07 |

Two domains at 40% each make this overwhelmingly a configuration exam.
Domain 1 is interfaces, zones, HA, routing, GlobalProtect, and tunnels;
Domain 2 is authentication, VSYS, logging, updates, certificates,
User-ID, and web proxy. Automation is real but is the smallest slice.

**Network Security Analyst** (datasheet dated August 2025).

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1. Object Configuration Creation and Application | 30% | 05 |
| 2. Policy Creation and Application | 30% | 05 |
| 3. Management and Operations | 26% | 06, 07 |
| 4. Troubleshooting | 14% | 07 |

**Network Security Professional** (datasheet dated June 2026).

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1. Network Security Fundamentals | 17% | 01 |
| 2. NGFW and SASE Solution Functionality | 13% | 02 |
| 3. Platform Solutions, Services, and Tools | 30% | 02 |
| 4. NGFW and SASE Solution Maintenance and Configuration | 10% | 03, 07 |
| 5. Infrastructure Management and CDSS | 17% | 02, 06 |
| 6. Connectivity and Security | 13% | 04, 05 |

**Cybersecurity Practitioner** (datasheet dated December 2025).

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1. Cybersecurity | 19% | 02 |
| 2. Network Security | 19% | 02 |
| 3. Secure Access | 14% | 02 |
| 4. Cloud Security | 20% | 02, 09 |
| 5. Endpoint Security | 15% | 02 |
| 6. Security Operations | 13% | 02 |

**Cybersecurity Apprentice** (datasheet dated May 2026).

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1. Cybersecurity | 16% | 01 |
| 2. Network Fundamentals | 16% | 01 |
| 3. Network Security | 14% | 01 |
| 4. Endpoint Security | 10% | 01 |
| 5. Cloud Security | 13% | 01 |
| 6. Security Operations | 13% | 01 |
| 7. Identity Security | 18% | 01 |

The remaining Specialist and Architect exams are outside most readers'
immediate path but are covered by this volume in part: **SD-WAN Engineer**
(August 2025) weights Planning and Design 24%, Deployment and
Configuration 24%, Troubleshooting 20%, Operations and Monitoring 18%,
Unified SASE 14%. **Security Service Edge Engineer** (March 2026) weights
Prisma Access Planning and Deployment, Prisma Access Services, and Prisma
Browser at 22% each, Troubleshooting 18%, Administration and Operation
16%. **Network Security Architect** (October 2025) spreads across ten
domains, none above 13%, which is itself the point: it tests breadth of
design judgment rather than depth in any one product.

All exams are delivered in English worldwide, with a 30-minute extension
provided by default in non-English-speaking countries.

### Certification sequencing and study path

The recommended progression for an engineer working through this volume:

1. **Cybersecurity Apprentice** ([Chapter 01](01-cybersecurity-apprentice-foundations.md)) — portfolio-wide conceptual
   foundation, no hands-on PAN-OS prerequisite.
2. **Cybersecurity Practitioner** ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)) — licensing, subscription,
   and platform-portfolio depth (Strata, Prisma, Cortex).
3. **Network Security Professional** — the Professional-level exam, and
   the one whose 30% Platform Solutions domain rewards Chapter 02's
   portfolio breadth most directly.
4. **Network Security Analyst** — after completing Chapters 03–05's
   hands-on labs at least once, ideally repeated on a second,
   independently built lab environment to confirm the configuration steps
   are retained rather than copy-pasted.
5. **Next-Generation Firewall Engineer** — after Chapters 06–07 and this
   chapter's capstone lab, which exercises the fleet-scale,
   troubleshooting, and automation skills its blueprint assumes.

Do not attempt NGFW Engineer without the Analyst-level hands-on repetition
first. Its own datasheet recommends both Network Security Professional and
Network Security Analyst beforehand, and gaps at the operational level
compound into larger gaps at the engineering level.

### The remaining paths, and how far this volume takes you

The sequence above covers five of the nine certifications in this
volume's blueprint row. Of the remaining four, one is covered elsewhere
in this volume and three are not — stated here so a reader planning a
path does not discover the gap after committing to it.

| Certification | Tier | Scope | Coverage here |
| --- | --- | --- | --- |
| **Cloud Security Professional** | Professional | Cortex Cloud platform, Cloud Runtime Security, Application Security, Cloud Posture Security, and SOC processes | **Covered** — [Chapter 09](09-cortex-cloud-security-professional.md) treats CNAPP architecture, agentless versus agent-based visibility, CIEM, and shift-left IaC scanning, and maps to the blueprint directly |
| **SD-WAN Engineer** | Specialist | Plan, deploy, configure, operate, monitor, and troubleshoot SD-WAN environments | Partial — [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md) covers routing and [Chapter 06](06-panorama-installation-central-management-and-logging.md) central management, but SD-WAN as a product is not developed |
| **Security Service Edge Engineer** | Specialist | Deploy, configure, manage, and troubleshoot SSE environments | Minimal — SSE is Prisma Access territory, named in [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)'s portfolio survey and not built on |
| **Network Security Architect** | Architect | Architecting secure, highly available, scalable systems across the network security portfolio | Partial — this volume builds the components an architect composes, but design judgment at architect tier is beyond its scope |

**Cortex Cloud is a genuine second track within this volume, not an
appendix to the network security one.** Chapter 09 stands apart from
Chapters 03–08 deliberately: it is a different platform, a different
console, and a different problem — securing workloads, configurations,
and identities *inside* public cloud rather than enforcing at the network
perimeter. A reader pursuing Cloud Security Professional can work
Chapters 01–02 for portfolio context and then go straight to Chapter 09,
skipping the PAN-OS chapters entirely. That path is roughly four to six
weeks rather than the six-to-nine months the network security sequence
takes, and [Volume VII](../../volume-07-cloud-infrastructure/README.md)
is the useful companion for the cloud-side fundamentals it assumes.

**The architect tier is a different kind of exam, not a harder one.** It
tests design judgment and trade-off reasoning across a portfolio rather
than configuration fluency on a product, which is why more lab repetition
does not prepare for it. Approach it after production design experience,
not after more study.

Palo Alto publishes no prerequisites for any of these — the
certification pages state tiers, not pathways — so sequencing is a matter
of judgment rather than a rule. The recommendation from the datasheets
that Network Security Professional and Network Security Analyst precede
NGFW Engineer is the only explicit ordering the vendor gives.

### Timelines for the first four exams

The NGFW Engineer plan below is the detailed one because it is where this
volume's material concentrates. The four exams preceding it in the
sequence are shorter propositions, and a reader working the volume in
order can reasonably slot them in as they arrive:

| Exam | Realistic preparation | Prerequisite reading |
| --- | --- | --- |
| Cybersecurity Apprentice | 1–2 weeks | [Chapter 01](01-cybersecurity-apprentice-foundations.md); no hands-on PAN-OS needed |
| Cybersecurity Practitioner | 2–3 weeks | [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md); portfolio and licensing breadth |
| Network Security Professional | 3–4 weeks | Chapters 01–03, with Chapter 02 carrying the 30% Platform Solutions domain |
| Network Security Analyst | 4–6 weeks | Chapters 03–05 worked hands-on at least twice, on independently built labs |

Taken end to end alongside the ten-week NGFW Engineer plan, the full
sequence is realistically a six-to-nine month undertaking rather than
something to compress into a quarter.

### A study plan for NGFW Engineer

Eight to ten weeks at **8–10 hours per week**, for a reader who has worked
through Chapters 01–07. Weighted toward configuration, because 80% of the
exam is.

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Interfaces, zones, virtual wire, aggregate Ethernet | 04 |
| 2 | High availability: active/active, active/passive, link and path monitoring | 04 |
| 3 | Routing, redistribution, and the Advanced Routing Engine | 04 |
| 4 | GlobalProtect portals, gateways, authentication, split tunneling; IPSec and GRE tunnels | 04 |
| 5 | Authentication profiles and sequences, VSYS, certificates and decryption | 05 |
| 6 | Logging, Strata Logging Service, log collectors, software updates | 06 |
| 7 | User-ID and Cloud Identity Engine, web proxy | 05 |
| 8 | Deployment options (PA-, VM-, CN-Series, Cloud NGFW), APIs, Terraform and Ansible | 03, 07 |
| 9 | Panorama, templates, device groups, pre- and post-rulesets, ACC dashboards | 06, 07 |
| 10 | Capstone lab, then timed configuration drills against the blueprint tasks | 08 |

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | The certification datasheet for your exam | Authority on domains, weights, and tasks; each lists subtopics far more specific than the domain titles |
| Official training | [Palo Alto Networks Education](https://www.paloaltonetworks.com/services/education) digital learning paths | Free digital learning and instructor-led courses aligned to each certification |
| Reference | Palo Alto Networks TechDocs | PAN-OS and Panorama administrator guides; the datasheets explicitly point at product documentation as the source exam items are written against |
| Community | [LIVEcommunity](https://live.paloaltonetworks.com/) | Practitioner answers on behavior the documentation does not cover |
| Lab | VM-Series in a hypervisor or public cloud trial | The exam is configuration-weighted; console repetition is the preparation |
| Practice exams | Third-party banks exist for the retired exams and are appearing for the new ones | Useful for exam stamina, but verify any bank targets the current exam and not PCNSE |

Note the last row carefully. Because the portfolio changed in 2025, a
large amount of PCNSA and PCNSE study material remains in circulation and
still sells. It is not worthless — the underlying PAN-OS knowledge
overlaps heavily — but it is not written to the current blueprints, and
anything claiming to be exam-accurate for PCNSE is by definition
describing an exam that no longer exists.

## Design Considerations

This chapter's capstone synthesizes every prior chapter's constructs into
one integrated architecture. The design below is deliberately
representative of a small-to-mid-size enterprise perimeter and branch
topology — the scale a Specialist-tier engineer is expected to reason about:

- **Topology.** A data-center HA pair (VM-Series, active/passive,
  [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md))
  fronting a DMZ and internal trust zone, managed by a Panorama
  instance ([Chapter 06](06-panorama-installation-central-management-and-logging.md)) that also manages a branch-office firewall
  onboarded via bootstrap ([Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md)).
- **Device group hierarchy.** A `Global-Baseline` parent device group
  carrying Shared/parent pre-rules for non-negotiable controls (known-
  malicious category blocks, DNS Security enforcement), with `DataCenter`
  and `Branch-Offices` child device groups carrying site-appropriate
  policy — directly reusing the hierarchy pattern from [Chapter 06](06-panorama-installation-central-management-and-logging.md).
- **Template stack layering.** A shared `Base-Network` template (NTP, DNS,
  logging/Collector Group assignment) combined with role-specific
  templates (`DataCenter-Network`, `Branch-Network`) into two template
  stacks — reusing the layering pattern from [Chapter 06](06-panorama-installation-central-management-and-logging.md).
- **Policy and inspection baseline.** App-ID/User-ID-based rules with a
  standard security profile group attached fleet-wide, plus a phased SSL
  Forward Proxy decryption rollout scoped to lower-risk URL categories
  first — directly reusing [Chapter 05](05-application-identity-threat-and-data-security-policy.md)'s design guidance.
- **Operational lifecycle.** Panorama-scheduled, staged content updates and
  a documented HA-aware software upgrade ring — reusing [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md)'s
  guidance — so the capstone environment is not just built once but
  designed to be operated indefinitely.
- **Automation touchpoint.** At least one configuration task (for example,
  bulk address-object creation) performed via the XML or REST API rather
  than manual entry, demonstrating the automation surface from [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md)
  integrated into a real build rather than treated as a standalone
  exercise.

## Implementation and Automation

The capstone build sequences prior chapters' implementation steps into one
coherent deployment; this section outlines the sequence and the
cross-chapter dependencies. The Hands-On Lab below executes it concretely.

### Build sequence

1. **Provision and bootstrap.** Deploy the data-center HA pair and the
   branch firewall as VM-Series instances ([Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md)), each with a
   tailored `init-cfg.txt` binding it to the correct Panorama device group
   and template stack from first boot.
2. **Establish Panorama governance.** Build the device group hierarchy and
   template stacks ([Chapter 06](06-panorama-installation-central-management-and-logging.md)) before pushing any site-specific policy,
   so every subsequent change flows through centralized management rather
   than local configuration.
3. **Configure networking and HA.** Push interface, zone, virtual router,
   and HA configuration via templates ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)), then verify HA state
   independently on the data-center pair before layering policy on top.
4. **Layer security policy.** Push Shared/parent pre-rules first (global,
   non-negotiable controls), then device-group-specific rules with
   attached security profile groups ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)).
5. **Enable decryption in scope.** Apply the phased SSL Forward Proxy
   policy with documented category exclusions ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)), verified
   against a client with the decryption CA distributed.
6. **Configure log forwarding.** Bind the Collector Group assignment into
   the shared template ([Chapter 06](06-panorama-installation-central-management-and-logging.md)) so every managed firewall's logs
   consolidate centrally from first push.
7. **Validate operational readiness.** Confirm content update scheduling,
   document the HA-aware upgrade sequence for this pair, and perform at
   least one API-driven configuration change against the fleet (Chapter
   07).

### Illustrative capstone automation snippet

```bash
# Bulk-create branch server address objects via the REST API, rather than
# manual entry for each object — representative of the automation
# integration expected at Specialist-tier maturity.
for host in app-server-01:10.10.20.50 db-server-01:10.10.20.60; do
  name="${host%%:*}"
  ip="${host##*:}"
  curl -sk -X POST \
    "https://pa-branch-01.acme.local/restapi/v11.1/Objects/Addresses?location=vsys&vsys=vsys1" \
    -H "X-PAN-KEY: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"entry\": [{\"@name\": \"${name}\", \"ip-netmask\": \"${ip}/32\"}]}"
done
```

## Validation and Troubleshooting

Apply a capstone-level validation pass across every layer built, using the
diagnostic commands introduced in earlier chapters as a single consolidated
checklist:

- **Bootstrap and licensing.** `show system bootstrap` and `request
  license info` on every instance confirm a clean first-boot state before
  troubleshooting anything downstream ([Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md)).
- **HA state.** `show high-availability state` on the data-center pair
  confirms one `active` and one `passive` member with synchronized
  configuration before assuming any policy or NAT issue is
  policy-related rather than an underlying HA sync problem ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)).
- **Routing and NAT.** `show routing route` and `test nat-policy-match`
  confirm the network layer independently of security policy before
  troubleshooting a "traffic is blocked" report as a policy problem
  ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)).
- **Policy match.** `test security-policy-match` isolates which rule
  (Shared, parent device group, local device group, or an unexpected local
  firewall rule) actually governs a given flow (Chapters 05–06).
- **Panorama push state.** Per-device push job status confirms every
  managed firewall actually received the intended configuration, rather
  than assuming a successful Panorama-local commit implies a successful
  fleet-wide push ([Chapter 06](06-panorama-installation-central-management-and-logging.md)).
- **Global counters and packet capture.** Reserved for problems that
  survive the checks above — used last, not first, consistent with
  [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md)'s layered troubleshooting guidance.

A capstone-level engineer works this checklist top-down rather than
reaching for packet capture as a first step; most real-world "the firewall
is blocking something" reports resolve at the routing, NAT, or policy-match
layer before any packet-level inspection is needed.

## Security and Best Practices

This chapter's capstone is also the point to audit the environment against
every prior chapter's security guidance as a single consolidated review,
rather than trusting that each chapter's guidance was independently
retained:

- Administrator RBAC and MFA on every management surface — firewall,
  Panorama, and API service accounts (Chapters 01, 06, 07).
- CDSS subscription currency and scheduled, staggered content updates
  across the fleet ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)).
- HA link isolation and path monitoring for both the data-center pair and
  any future branch HA expansion ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)).
- Least-privilege, App-ID/User-ID-scoped security rules with an attached
  profile group on every allow rule, and a documented, reviewed decryption
  exclusion list ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)).
- Access-domain-scoped Panorama administration and non-bypassable
  Shared/parent pre-rules for global controls ([Chapter 06](06-panorama-installation-central-management-and-logging.md)).
- Secrets-managed automation credentials with scoped roles and a rotation
  schedule ([Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md)).

Treat this consolidated review as the capstone's actual security
deliverable — a design is not complete when it passes functional
validation alone; it is complete when it also passes this cross-chapter
security review.

## References and Knowledge Checks

**References**

- [Palo Alto Networks, *Next-Generation Firewall Engineer* datasheet.](https://www.paloaltonetworks.com/content/dam/pan/en_US/assets/pdf/datasheets/education/ngfw-engineer-datasheet.pdf)
- [Palo Alto Networks, *Network Security Analyst* datasheet.](https://www.paloaltonetworks.com/content/dam/pan/en_US/assets/pdf/datasheets/education/netsec-analyst-datasheet.pdf)
- [Palo Alto Networks, *Network Security Professional* datasheet.](https://www.paloaltonetworks.com/content/dam/pan/en_US/assets/pdf/datasheets/education/netsec-professional-datasheet.pdf)
- [Palo Alto Networks certification portfolio.](https://www.paloaltonetworks.com/services/education/certification) — the current four-level, three-track program
- [Palo Alto Networks Beacon (training.paloaltonetworks.com)](https://beacon.paloaltonetworks.com/) — role-based
  learning paths and hands-on units.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this volume's certification mapping.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — PAN-OS 11.x /
  Panorama 11.x baseline used throughout this volume.

**Knowledge checks**

1. Which chapters map most directly to Network Security Analyst's
   blueprint scope, and which extend that scope to NGFW Engineer?
2. Why does the recommended study path require Analyst-level hands-on
   repetition before attempting NGFW Engineer, rather than proceeding
   directly there after [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)?
3. In the capstone's validation checklist, why are HA state and
   routing/NAT checks positioned before policy-match testing, and policy-
   match testing before packet capture?
4. Name two of the capstone's cross-chapter security review items that
   would not be caught by functional validation (traffic passes/fails)
   alone.

## Hands-On Lab

**Objective:** Build and validate the integrated capstone architecture
described in Design Considerations — a Panorama-managed data-center HA
pair and branch firewall with layered device-group policy, template-based
networking, phased decryption, centralized logging, and at least one
API-driven configuration change — then perform a full cross-chapter
validation pass, including a negative test that confirms the non-
negotiable global policy layer cannot be bypassed by local device-group
configuration.

**Prerequisites**

- Completion of Chapters 03–07's individual labs, ideally on environments
  that can be consolidated or rebuilt into the capstone topology (a
  data-center HA pair plus one branch firewall, all Panorama-managed).
- A lab Panorama instance with connectivity to all managed firewalls.
- A test client for decryption and policy validation, with the ability to
  trust the lab decryption CA.
- Estimated duration: this is the volume's longest lab and may reasonably
  span multiple working sessions; complete each numbered phase fully
  before proceeding to the next.

**Steps**

1. **Provisioning phase.** Confirm or (re)bootstrap the data-center HA
   pair and branch firewall with `init-cfg.txt` files binding each to the
   correct device group and template stack names planned for this
   capstone ([Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md)). Verify:

   ```text
   admin@pa-dc-01> show system bootstrap
   admin@pa-branch-01> show system bootstrap
   ```

2. **Panorama governance phase.** On Panorama, build the hierarchy and
   stacks:

   ```text
   admin@panorama01# set devicegroups Global-Baseline
   admin@panorama01# set devicegroups DataCenter parent Global-Baseline
   admin@panorama01# set devicegroups Branch-Offices parent Global-Baseline
   admin@panorama01# set template Base-Network config deviceconfig system dns-setting servers primary 10.10.10.2
   admin@panorama01# set template-stack DataCenter-Stack templates Base-Network
   admin@panorama01# set template-stack Branch-Stack templates Base-Network
   admin@panorama01# commit
   ```

3. Onboard all three firewalls into the correct device group and template
   stack assignments, then push:

   ```text
   admin@panorama01# set devicegroups DataCenter devices [ <DC_SERIAL_A> <DC_SERIAL_B> ]
   admin@panorama01# set devicegroups Branch-Offices devices <BRANCH_SERIAL>
   admin@panorama01# set template-stack DataCenter-Stack devices [ <DC_SERIAL_A> <DC_SERIAL_B> ]
   admin@panorama01# set template-stack Branch-Stack devices <BRANCH_SERIAL>
   admin@panorama01# commit
   admin@panorama01> request batch-push device-group Global-Baseline
   admin@panorama01> request batch-push template-stack DataCenter-Stack
   admin@panorama01> request batch-push template-stack Branch-Stack
   ```

4. **Networking and HA phase.** Confirm HA state on the data-center pair:

   ```text
   admin@pa-dc-01> show high-availability state
   ```

   **Expected result:** One `active`, one `passive`, both `Running` on
   HA1/HA2.

5. **Policy phase.** Add a Shared pre-rule and device-group-specific rules
   with an attached profile group, then push:

   ```text
   admin@panorama01# set shared pre-rulebase security rules Block-Known-Malicious from any to any source any destination any application any category [ malware phishing command-and-control ] action deny
   admin@panorama01# set devicegroups DataCenter pre-rulebase security rules DC-Outbound-Web from trust to untrust source any destination any application [ web-browsing ssl ] service application-default action allow
   admin@panorama01# set devicegroups DataCenter pre-rulebase security rules DC-Outbound-Web profile-setting group Standard-Inspection
   admin@panorama01# set devicegroups Branch-Offices pre-rulebase security rules Branch-Outbound-Web from trust to untrust source any destination any application [ web-browsing ssl ] service application-default action allow
   admin@panorama01# set devicegroups Branch-Offices pre-rulebase security rules Branch-Outbound-Web profile-setting group Standard-Inspection
   admin@panorama01# commit
   admin@panorama01> request batch-push device-group Global-Baseline
   ```

6. **Decryption phase.** On the `DataCenter-Network` template (create if
   not already present), push a scoped decrypt rule with a category
   exclusion, consistent with [Chapter 05](05-application-identity-threat-and-data-security-policy.md):

   ```text
   admin@panorama01# set devicegroups DataCenter pre-rulebase decryption rules Decrypt-Exclude-Financial from trust to untrust source any destination any category financial-services action no-decrypt
   admin@panorama01# set devicegroups DataCenter pre-rulebase decryption rules Decrypt-Outbound from trust to untrust source any destination any category any action decrypt type ssl-forward-proxy
   admin@panorama01# commit
   admin@panorama01> request batch-push device-group DataCenter
   ```

7. **Logging phase.** Confirm the Collector Group assignment is present in
   `Base-Network` and that traffic logs from all three firewalls appear in
   Panorama's log viewer after generating test traffic from each site.

8. **Automation phase.** Run the illustrative bulk address-object script
   from Implementation and Automation (adjusted for lab credentials)
   against the branch firewall, and confirm the objects exist:

   ```text
   admin@pa-branch-01> show object address app-server-01
   admin@pa-branch-01> show object address db-server-01
   ```

9. **Full validation pass.** Work the Validation and Troubleshooting
   checklist top-down (bootstrap/license, HA, routing/NAT, policy match,
   Panorama push state) across all three firewalls, recording the result
   of each check.

10. **Negative test.** From the branch firewall's *local* CLI (not
    Panorama), attempt to add a local rule permitting one of the
    categories the Shared pre-rule blocks, and confirm the Shared
    pre-rule — evaluated before local firewall rules — still governs the
    outcome for matching traffic:

    ```text
    admin@pa-branch-01# set rulebase security rules Local-Override-Attempt from trust to untrust source any destination any application any category malware action allow
    admin@pa-branch-01# commit
    ```

    ```text
    admin@pa-branch-01> test security-policy-match from trust to untrust source 10.10.20.15 destination 93.184.216.34 destination-port 443 protocol 6 application ssl category malware
    ```

    **Expected result:** `Block-Known-Malicious` (the Shared pre-rule) is
    reported as the matching rule, not `Local-Override-Attempt` —
    confirming pre-rules evaluate ahead of locally defined firewall rules
    and cannot be bypassed by local configuration. Remove the test rule:

    ```text
    admin@pa-branch-01# delete rulebase security rules Local-Override-Attempt
    admin@pa-branch-01# commit
    ```

11. **Cleanup:** Decide whether to retain the capstone environment for
    [Chapter 09](09-cortex-cloud-security-professional.md)'s Cortex Cloud material (recommended, if lab capacity
    allows) or decommission it. If decommissioning, remove pushed policy
    from Panorama, detach devices from their device groups and template
    stacks, and power off/delete the VM-Series instances:

    ```text
    admin@panorama01# delete devicegroups DataCenter
    admin@panorama01# delete devicegroups Branch-Offices
    admin@panorama01# delete devicegroups Global-Baseline
    admin@panorama01# commit
    ```

## Design Exercise

The **Network Security Architect** exam is a design credential — its ten
blueprint domains, none weighted above 13%, test breadth of design judgment
rather than depth in any one product. The capstone lab above is the *build*
half; this exercise is the *design* half, covering the Architect domains by
reasoning from requirements to a defensible architecture (no lab required).

**Scenario.** A retailer with 300 branches, two data centers, and a
mobile/remote workforce is consolidating onto the Palo Alto Networks
platform. Requirements: segment cardholder-data (PCI) traffic end to end;
give remote users the same policy as on-site; centralize policy and logging
for a 24×7 SOC; tolerate the loss of any one firewall or data center with no
security gap; and keep the branch hardware footprint minimal.

**Produce, defending each choice against a rejected alternative:**

1. **Requirements register** — classify each requirement as a requirement,
   constraint, assumption, or risk, each with a measurable acceptance test.
2. **Platform architecture** — where Strata NGFW, Prisma Access (SASE),
   Panorama, and Cortex (XSIAM/XSOAR) each sit, and why; the branch model
   (hardware NGFW vs Prisma Access) traded against the minimal-footprint
   constraint.
3. **Segmentation design** — zones, decryption, and User-ID strategy that
   keeps PCI traffic isolated and inspected end to end.
4. **Resilience design** — HA at each tier (firewall HA, Panorama HA,
   multi-DC) meeting the "lose any one" requirement, with the failure modes
   each covers and does not.
5. **Operations design** — centralized logging/Collector Groups feeding the
   SOC, and where XSOAR automation replaces manual response.
6. **Decision log** — at least five decisions as {decision, justification,
   rejected alternative, impact}.

**Success looks like:** every product placement traces to a requirement, each
resilience claim names the failure it survives, and no requirement is left
unaddressed — the breadth-of-judgment standard the Architect exam applies.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The role-based certification portfolio validates exactly the skill
progression this volume was built to develop: Analyst-level operational
fluency across initial configuration, networking, and policy (Chapters
01–05), extended by NGFW Engineer depth across Panorama, advanced
troubleshooting, and automation (Chapters 06–07). This chapter's capstone
lab is the volume's proof point — a single integrated build that exercises
every prior chapter's constructs together, validated with the same
layered troubleshooting discipline expected of a practicing Specialist-tier
engineer. [Chapter 09](09-cortex-cloud-security-professional.md) extends this same enterprise into Cortex Cloud
Security Professional territory, applying cloud-native application
protection to the workloads this capstone's firewalls protect.

- [ ] Can map this volume's chapters to the current blueprint domains and
      their weights.
- [ ] Can articulate and follow the recommended certification study
      sequence.
- [ ] Designed an integrated, multi-firewall, Panorama-managed architecture
      combining networking, HA, policy, decryption, and logging.
- [ ] Built and fully validated that architecture using a top-down,
      layered troubleshooting checklist.
- [ ] Completed the capstone hands-on lab, including the negative test and
      a documented cleanup or retention decision.
