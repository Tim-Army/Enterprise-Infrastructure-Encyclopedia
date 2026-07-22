# Chapter 07: Security Design

## Learning Objectives

- Integrate security into network design rather than appending it
- Design zero-trust and segmentation architectures to requirements
- Design the security enforcement topology: where inspection,
  identity, and policy live
- Design for compliance and for the threat model the business faces
- Reason about the trade-offs security imposes — latency, cost,
  operational effort — and size them

## Theory and Architecture

### Security is designed in, not bolted on

CCDE Domain 5 (15%) tests security as an architectural property. The
expert-level principle: security integrated into the design from the
start — trust boundaries, segmentation, identity, and enforcement
placement decided alongside topology and routing — is coherent and
operable, while security appended afterward is full of gaps and
friction. Every other chapter's designs have already touched security
(segmentation in 06, management-plane protection in 05, edge in 03);
this chapter makes it the explicit lens.

### Zero trust as a design model

**Zero trust** replaces "trusted inside, untrusted outside" with
"never trust, always verify": identity- and posture-based access,
least privilege, and continuous verification regardless of location.
As a *design*, zero trust means:

- **Identity as the perimeter** — access decisions from authenticated
  identity and device posture (ISE, SASE identity), not IP address or
  network location.
- **Microsegmentation** — fine-grained policy between workloads/users
  (SGT/group-based policy, Chapter 06), so a compromise is contained.
- **Continuous verification** — posture and behavior checked over
  time, not just at connect.

The design decides how far to take it — full microsegmentation is
powerful and operationally heavy; the depth is set by the threat model
and the data's sensitivity, not by fashion.

### Enforcement topology

A security design places enforcement deliberately:

- **Perimeter and edge** — firewalls and IPS at internet and partner
  boundaries (Volume XVI, XXV); the design decides how many boundaries
  and where.
- **Segmentation enforcement** — between segments/groups, in the
  fabric (SGT) or at firewalls (service graphs/PBR steering,
  Volume XXVII).
- **Identity and access** — where authentication, authorization, and
  posture assessment happen (ISE, SASE), and how they scale.
- **Cloud and SASE** — enforcement following users and workloads to
  the cloud edge rather than hairpinning through a data center
  (the Workforce Mobility elective, Chapter 08).

The recurring design question: **does traffic have to traverse the
enforcement point, and at what latency/cost** — an inspection point
users hairpin across the world to reach is a design failure.

### Compliance and threat modeling

The business's regulatory obligations (PCI, HIPAA, GDPR, sector rules)
and threat model drive concrete design requirements: segmentation
scope (PCI's cardholder-data environment), data residency (GDPR),
logging and audit retention, and encryption in transit. The CCDE
designs to the actual obligations and threats — not a generic maximum,
which over-constrains, and not a generic minimum, which under-protects.

### AI and security (v3.1)

The v3.1 AI additions cut both ways in security design: AI/ML for
detection and assurance (behavioral anomaly detection on the telemetry
Chapter 05 produces), and AI infrastructure as a new asset to protect
(training data and models are high-value — Volume XXVII, Chapter 07).
Both are now design considerations.

## Design Considerations

- **Design security with the topology, not after.** Trust boundaries
  and segmentation decided alongside the network are coherent;
  appended ones leak.
- **Zero-trust depth to the threat model.** Full microsegmentation
  where data sensitivity and threat justify its operational weight;
  coarser segmentation where they do not — a stated decision.
- **Enforcement where traffic naturally flows.** Place inspection and
  identity so protected traffic passes them without pathological
  hairpins; SASE exists precisely to avoid backhaul.
- **Compliance scope precisely.** Design segmentation to contain the
  compliance scope (shrink the PCI CDE), reducing audit burden — a
  design decision with direct business value.
- **Name the security trade-off.** Every control costs latency, money,
  or operational effort; size it to the requirement and state it, as
  with every other domain.

## Applied Design Reasoning

Brief fragment — *"A financial-services firm is adopting cloud and
hybrid work; regulators require data-in-transit protection and
segmentation of trading systems; users work from anywhere; the
security team wants consistent policy for on-prem, cloud, and remote
without backhauling everyone through HQ."* — reasoned:

```text
Requirements: protect data in transit (regulatory); segment trading
  systems; consistent policy across on-prem/cloud/remote; no backhaul.
Constraints: hybrid/remote workforce; multi-environment; regulator.
Design decisions:
  - Zero-trust with identity-based access (ISE + SASE identity),
    because users work from anywhere and location-based trust cannot
    meet the requirement.
  - Microsegmentation of trading systems specifically (highest
    sensitivity), coarser segmentation elsewhere, because full
    microsegmentation everywhere would exceed the operational need outside the
    regulated core -> depth sized to the threat model.
  - SASE for enforcement at the cloud edge, because "no backhaul" +
    consistent policy across environments is an explicit requirement;
    inspection follows the user rather than hairpinning through HQ.
  - Encryption in transit end to end (regulatory), designed into the
    transport, not appended.
  Trade-off: SASE + zero trust adds subscription cost and a new policy
  plane -> accepted, because anywhere-work with regulatory data
  protection and no backhaul cannot be met by a perimeter model.
```

## Verification and Design Review

Security design is verified by confirming security was designed with
the topology (not appended); zero-trust depth matches the threat model
and data sensitivity; enforcement is placed so protected traffic
passes it without pathological hairpins; compliance scope is contained
by segmentation; encryption/audit meet the actual obligations; and
every control's cost is sized and stated. The distinctive review
question: **can a user or workload reach what they need while every
required control is unavoidably in the path, without backhaul pain** —
security that is either bypassable or unbearable is a failed design.

## References and Knowledge Checks

- CCDE v3.1 Security Design domain (15%)
- Volume X (enterprise cybersecurity), Volume XVI (Palo Alto / NGFW,
  SASE), Volume XXV (Cisco security), Volume XXVII (AI-asset security)

Knowledge checks:

1. Why does security designed with the topology outperform security
   appended to it? Give one concrete gap the appended approach
   creates.
2. What sets the appropriate depth of microsegmentation, and what is
   the cost of taking it too far?
3. What problem does SASE solve that a hub-and-spoke inspection model
   creates for a hybrid workforce?
4. How does segmentation design reduce compliance audit burden?

## Design Exercise

Take the financial-services brief (or a security-design scenario from
your experience) and produce a security HLD: the trust model
(zero-trust vs zoned) with justification; the segmentation design and
where microsegmentation depth is/ isn't applied (tied to sensitivity);
the enforcement topology (perimeter, fabric, identity, SASE) placed so
protected traffic passes controls without hairpins; the compliance
mapping (obligation → design element); and the encryption/audit design.
State each as a decision-with-driver-and-cost and review both ways.

## Lab Verification

The exercise is verified when security is integrated with the
topology, zero-trust depth matches the threat model, enforcement is
unavoidable-yet-not-pathological for protected traffic, compliance
obligations map to design elements, and each control's cost is sized
and stated. Until a reviewer confirms that, the exercise is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Security design integrates protection into the architecture from the
start: zero trust with identity as the perimeter, microsegmentation
sized to the threat model, enforcement placed where protected traffic
naturally flows (SASE to avoid backhaul), and compliance scope
contained by segmentation. Every control's latency, cost, and
operational weight is sized and named — security that is bypassable or
unbearable both fail the design.

- [ ] I design security with the topology, not after it
- [ ] I size microsegmentation depth to the threat model
- [ ] My enforcement is unavoidable for protected traffic without
      backhaul pain
- [ ] I contain compliance scope by design and state each control's
      cost
