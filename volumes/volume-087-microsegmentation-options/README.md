# Volume LXXXVII — Microsegmentation Options

> A vendor-neutral decision guide to microsegmentation — the enforcement models and the leading
> platforms (VMware NSX, Cisco, Illumio, Akamai Guardicore, Zero Networks, TrueFort, ColorTokens
> Xshield, cloud-native, and Kubernetes) — with the **pros, cons, compatibility, and requirements** of
> each, so you can choose the right approach for your environment.

## Overview

Volume LXXXVII is a **comparison and decision volume** for **microsegmentation** — the practice of
containing east-west (lateral) movement inside a network by wrapping each workload, asset, or
application in its own least-privilege policy. There is no single "best" microsegmentation product; the
right choice depends on what you must protect (Windows, Linux, legacy, OT/IoT, cloud, Kubernetes,
network gear), how you can enforce (agent, agentless, hypervisor, EDR, appliance, cloud-native), and
what you can operate. This volume lays out the **enforcement models**, then walks each major option with
its **pros, cons, compatibility, and requirements**, and closes with a weighted decision framework and a
phased rollout plan.

This is a **product-and-skills** volume (like the vSphere and open-source tooling volumes), not a
certification-tracks volume: it maps a technology space and teaches it with hands-on walkthroughs. Every
platform's facts — architecture, coverage, and requirements — were **verified against the vendors'
official sources on 29 July 2026**; the comparison is a fair decision guide, not an endorsement of any
one product.

Chapters move from concepts to options to decision:

- **Chapter 01** covers the fundamentals — east-west traffic, lateral movement, zero trust, and segmentation granularity.
- **Chapter 02** lays out the **enforcement models** and a **selection framework** (the rubric used throughout).
- **Chapter 03** covers **network- and hypervisor-based** options — VMware NSX DFW and Cisco ACI.
- **Chapter 04** covers **workload/agent-based** platforms — Illumio, Cisco Secure Workload, and Akamai Guardicore.
- **Chapter 05** covers **Zero Networks** — agentless, MFA-based segmentation.
- **Chapter 06** covers **TrueFort** — EDR-leveraged, application- and identity-centric segmentation.
- **Chapter 07** covers **ColorTokens Xshield** — hybrid enforcement with an agentless Gatekeeper.
- **Chapter 08** covers **cloud-native and Kubernetes** — security groups/NSGs and NetworkPolicy/Calico/Cilium.
- **Chapter 09** is the **decision guide** — a weighted matrix, PoC, migration, and day-2 operations.
- **Chapter 10** covers **network-fabric and NAC-based** options — Cisco ISE/TrustSec, Arista MSS, HPE Aruba, Juniper, Fortinet, Check Point.
- **Chapter 11** covers **DPU-accelerated and platform-native** options — HPE Aruba CX 10000 with AMD Pensando, NVIDIA BlueField, Nutanix Flow.
- **Chapter 12** covers **service mesh and workload identity** — Istio, Linkerd, Consul, SPIFFE/SPIRE.
- **Chapter 13** covers the **identity-based and overlay independents** — Elisity and Tempered Airwall, plus the vendors that are no longer viable.
- **Chapter 14** covers **OT and cyber-physical** segmentation — Xage, Claroty xDome, Nozomi, TXOne, Zscaler/Airgap.
- **Chapter 15** is the **comparison matrix** — cost, implementation time, system requirements, FIPS 140-3, FedRAMP, air-gap, and vendor links.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs, and every
option chapter carries an explicit **Pros / Cons / Compatibility / Requirements** breakdown.

> **Scope.** Microsegmentation is a **defensive** control: it contains lateral movement and enforces
> least privilege inside **your own** network. All policy design, enforcement, and testing in this
> volume is authorized administration of environments you operate.

## Chapters

1. [Microsegmentation Fundamentals](chapters/01-microsegmentation-fundamentals.md) — east-west traffic, lateral movement, zero trust, granularity.
2. [Enforcement Models and a Selection Framework](chapters/02-enforcement-models-and-selection.md) — the eleven enforcement models and the evaluation rubric.
3. [Network and Hypervisor-Based Options](chapters/03-network-and-hypervisor-based.md) — VMware NSX DFW, Cisco ACI.
4. [Workload and Agent-Based Platforms](chapters/04-workload-agent-based-platforms.md) — Illumio, Cisco Secure Workload, Akamai Guardicore.
5. [Zero Networks](chapters/05-zero-networks.md) — agentless, MFA-based segmentation.
6. [TrueFort](chapters/06-truefort.md) — EDR-leveraged, application- and identity-centric segmentation.
7. [ColorTokens Xshield](chapters/07-colortokens-xshield.md) — hybrid enforcement and the agentless Gatekeeper.
8. [Cloud-Native and Kubernetes Microsegmentation](chapters/08-cloud-native-and-kubernetes.md) — security groups/NSGs, NetworkPolicy, Calico, Cilium.
9. [Choosing and Rolling Out Microsegmentation](chapters/09-choosing-and-rolling-out.md) — weighted matrix, PoC, migration, day-2 operations.
10. [Network-Fabric and NAC-Based Segmentation](chapters/10-network-fabric-and-nac-based.md) — Cisco ISE/TrustSec, Arista MSS-Group, HPE Aruba, Juniper, Fortinet, Check Point.
11. [DPU-Accelerated and Platform-Native Segmentation](chapters/11-dpu-and-platform-native.md) — AMD Pensando/CX 10000, NVIDIA BlueField, Nutanix Flow.
12. [Service Mesh and Workload-Identity Segmentation](chapters/12-service-mesh-and-workload-identity.md) — Istio, Linkerd, Consul, SPIFFE/SPIRE.
13. [Identity-Based and Overlay Independents](chapters/13-identity-based-and-overlay-independents.md) — Elisity, Tempered Airwall; the status of vArmour and Unisys Stealth.
14. [OT and Cyber-Physical Segmentation](chapters/14-ot-and-cyber-physical-segmentation.md) — Xage, Claroty xDome, Nozomi, TXOne, Zscaler/Airgap.
15. [Comparison Matrix, Compliance, and Sources](chapters/15-comparison-matrix-and-sources.md) — cost, implementation time, system requirements, FIPS 140-3, FedRAMP, air-gap, vendor links.

## Compliance and currency

Chapters 10–15 record, for every option, a cost model, an implementation-time estimate, system
requirements, FIPS 140-3 status, FedRAMP status, and air-gap capability.

Three cautions govern how those fields should be read. **FIPS 140-3 means a CMVP certificate for a
specific module and version** — "FIPS-compliant" is a marketing phrase, not a validation. **FedRAMP
"In Process" is not authorization** and permits no federal use. And **implementation times are
estimates derived from the deployment model**, never vendor commitments. Compliance entries were
verified against the
[NIST CMVP registry](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search)
and the [FedRAMP Marketplace](https://marketplace.fedramp.gov/) on **30 July 2026**; re-verify before
relying on any of them.

Chapter 13 also records vendors that are **no longer viable** — vArmour was discontinued and its IP sold
in January 2025, and Unisys Stealth no longer exists as a named product — because both still appear in
older comparisons and incumbent proposals.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## How to use this volume

Read Chapters 01–02 for the mental model and the rubric, then read the option chapters (03–08) that
match your environment, scoring each against the rubric. Chapter 09 turns those scores into a decision
and a rollout plan. Related coverage: Zscaler (**XXXV**) and Palo Alto (**XVI**, **LXV**) for
zero-trust access, VMware (**V**, **LXXI**, **LXXII**) for the NSX/vSphere platform, CNCF/Kubernetes
(**XLI**) and Containers (**VIII**) for the cluster context, and Enterprise Cybersecurity (**X**) for
the broader defense program.
