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

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs, and every
option chapter carries an explicit **Pros / Cons / Compatibility / Requirements** breakdown.

> **Scope.** Microsegmentation is a **defensive** control: it contains lateral movement and enforces
> least privilege inside **your own** network. All policy design, enforcement, and testing in this
> volume is authorized administration of environments you operate.

## Chapters

1. [Microsegmentation Fundamentals](chapters/01-microsegmentation-fundamentals.md) — east-west traffic, lateral movement, zero trust, granularity.
2. [Enforcement Models and a Selection Framework](chapters/02-enforcement-models-and-selection.md) — the eight enforcement models and the evaluation rubric.
3. [Network and Hypervisor-Based Options](chapters/03-network-and-hypervisor-based.md) — VMware NSX DFW, Cisco ACI.
4. [Workload and Agent-Based Platforms](chapters/04-workload-agent-based-platforms.md) — Illumio, Cisco Secure Workload, Akamai Guardicore.
5. [Zero Networks](chapters/05-zero-networks.md) — agentless, MFA-based segmentation.
6. [TrueFort](chapters/06-truefort.md) — EDR-leveraged, application- and identity-centric segmentation.
7. [ColorTokens Xshield](chapters/07-colortokens-xshield.md) — hybrid enforcement and the agentless Gatekeeper.
8. [Cloud-Native and Kubernetes Microsegmentation](chapters/08-cloud-native-and-kubernetes.md) — security groups/NSGs, NetworkPolicy, Calico, Cilium.
9. [Choosing and Rolling Out Microsegmentation](chapters/09-choosing-and-rolling-out.md) — weighted matrix, PoC, migration, day-2 operations.

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
