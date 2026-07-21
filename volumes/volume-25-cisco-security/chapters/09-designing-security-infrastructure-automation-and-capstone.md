# Chapter 09: Designing Security Infrastructure, Automation, and Capstone

## Learning Objectives

- Approach security as a design discipline: requirements, risk, and
  trade-offs before configuration.
- Design secure infrastructure across edge, transit, cloud, and
  application layers.
- Align a security design to a risk framework and to stated requirements.
- Apply automation, DevSecOps, and the role of AI to security operations.
- Compose the whole CCNP Security track into one reference design as a
  capstone.

## Theory and Architecture

### The SDSI concentration is a design exam

This chapter is the **SDSI (300-745)** concentration —
*Designing Cisco Security Infrastructure* — and it is different in kind
from the others. SVPN and SISE test whether you can configure and
troubleshoot a product; SDSI tests whether you can *design a security
architecture*, which is judgment rather than CLI. Its weights:

| SDSI domain | Weight |
| --- | --- |
| Secure Infrastructure | **30%** |
| Risk, Events, and Requirements | **30%** |
| Applications | 25% |
| Artificial Intelligence, Automation, and DevSecOps | 15% |

Note there is **no dominant configuration domain** and two 30% domains —
one on infrastructure design, one on risk and requirements. A candidate
who prepares by configuring devices has misread it: SDSI rewards the
ability to justify a design against requirements and risk, which is the
architect's skill, not the operator's. This chapter is written that way,
and it also serves as the volume's capstone.

### Design starts with requirements and risk, not products

The central SDSI discipline, and the one the two 30% domains encode:
**a security design begins with what must be protected and against what,
not with which product to deploy.** The order is:

1. **Requirements** — what the business needs the design to achieve:
   compliance obligations, availability targets, the data to protect, the
   users and locations to serve.
2. **Risk** — what threatens those requirements, at what likelihood and
   impact, framed against a recognized model (the threat classes from
   [Chapter 01](01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md),
   organized by a risk framework).
3. **Design** — the controls that meet the requirements and mitigate the
   risk, chosen and placed deliberately.
4. **Products** — last, selected to implement the design, not to drive it.

A design that starts from a product ("we have firewalls, where do they
go") inverts this and is the anti-pattern SDSI tests against. The
Risk, Events, and Requirements domain (30%) is precisely this reasoning
made examinable.

### Secure infrastructure across the layers

The Secure Infrastructure domain (30%) is designing the enforcement points
this volume has covered as a coherent whole rather than in isolation:

- **Secure edge and transit** — the firewall and IPS boundary
  ([Chapter 02](02-network-security-with-cisco-secure-firewall-and-ips.md)),
  the VPN and secure-connectivity fabric
  ([Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md)),
  placed to protect the flows that matter.
- **Secure access** — identity-based network access and segmentation
  ([Chapters 05](05-secure-network-access-visibility-and-enforcement.md)
  and [06](06-identity-services-engine-deployment-policy-and-services.md)).
- **Secure cloud and service edge** — cloud-delivered controls and
  zero-trust access
  ([Chapters 03](03-cloud-security-and-the-secure-service-edge.md) and
  [08](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)).
- **Hybrid-work architecture** — the reality that users and workloads are
  everywhere, which is why the perimeter model gave way to zero trust and
  the service edge.

The design skill is composition: how these layers reinforce one another,
where they overlap deliberately for defense in depth, and where a gap
between them is the exposure an attacker uses.

### Application security

The Applications domain (25%) extends security into how applications are
built and run: securing containerized cloud workloads, API security, and
the application-and-data controls from
[Chapter 08](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md).
As applications moved to containers and cloud, the security boundary moved
with them — securing the workload and its pipeline, not only the network
around it.

### Automation, DevSecOps, and AI

The AI, Automation, and DevSecOps domain (15%) is the SCOR automation
thread carried into design:

- **Security automation** — the read-first, gate-writes API discipline
  the volume has applied to FMC (Chapter 02), Secure Endpoint (Chapter 04),
  and ISE (Chapter 06), designed in as a first-class capability rather than
  bolted on.
- **DevSecOps** — building security into the delivery pipeline:
  policy-as-code, automated security testing, and scanning
  infrastructure-as-code before it deploys (the shift-left idea that
  parallels the Palo Alto Cortex Cloud material in
  [Volume XVI, Chapter 09](../../volume-16-palo-alto-networks-security/chapters/09-cortex-cloud-security-professional.md)).
- **AI in security** — its emerging role in detection and response, and,
  even-handedly, as a capability attackers use too. The design question is
  where AI-assisted analytics genuinely improve detection versus where they
  add opacity.

## Design Considerations

- **Write requirements down before drawing a topology.** An unstated
  requirement is an ungoverned design; the requirements domain exists
  because most security failures are requirements failures in disguise.
- **Frame risk explicitly and proportionally.** Not every risk warrants
  the same control; a design applies effort where likelihood and impact
  justify it. A design that treats all risk equally wastes budget on the
  trivial and underfunds the severe.
- **Design defense in depth, not defense in duplicate.** Layers should
  cover different failure modes, not the same one repeatedly. Know why each
  layer is present and what it catches that the others do not.
- **Design for operability and change.** A secure design that cannot be
  operated, monitored, or evolved is insecure over time. Automation and
  observability are design requirements, not afterthoughts.
- **Choose products to serve the design.** Product selection is the last
  step and the servant of the requirements — the discipline that keeps a
  design from being a vendor catalog.

## Implementation and Automation

SDSI is a design exam, so "implementation" here is producing design
artifacts and the automation that operationalizes them.

### 1. A requirements-to-controls design record

The artifact SDSI's reasoning produces:

```text
# security-design-record.md
Requirement:  Remote staff must reach the finance app; data must not leave.
Risk:         Credential theft (high likelihood), data exfiltration (high impact).
Controls:     ZTNA per-app access (Ch08) + Duo phishing-resistant MFA (Ch08)
              + device posture gate (Ch06) + DLP on the app's data (Ch08).
Products:     Secure Access / Duo / ISE — selected to implement the above.
Assurance:    Access logs answer who/what/device/posture (Ch08 visibility).
```

The record makes the reasoning auditable: each control traces to a risk,
each risk to a requirement. This is what an SDSI answer looks like when it
is right.

### 2. Policy-as-code, the DevSecOps expression

```bash
# Scan infrastructure-as-code for security misconfiguration before deploy —
# the shift-left control, catching the exposed-bucket class (Ch03) in the
# pipeline rather than in production.
checkov -d ./infrastructure --compact

# Gate the deployment: a failing scan blocks the merge.
# (In CI: non-zero exit fails the pipeline.)
```

### 3. Cross-portfolio automation via pxGrid and APIs

```bash
# The design-level automation goal: shared context across the portfolio.
# ISE publishes who-is-on-the-network via pxGrid; other tools subscribe.
# Read-only context retrieval is the safe, high-value integration.
curl -sk "https://ise.example.com:8910/pxgrid/..." --cert client.pem \
  # subscribe to session context; consumed by firewall/analytics policy
```

## Validation and Troubleshooting

### Validating a design, not a device

SDSI validation is design review, and the questions are architectural:

- **Does every control trace to a risk, and every risk to a requirement?**
  A control with no risk behind it is cost; a risk with no control is
  exposure. The design record above makes both visible.
- **Is there defense in depth without wasteful duplication?** Each layer
  should catch something the others do not.
- **Can the design be operated and observed?** A design with no assurance
  story cannot be run safely.
- **Does product selection follow the design or drive it?** If the design
  reads as a product list, the reasoning ran backwards.

### The requirements-gap failure

The characteristic design failure — and the one the 30% requirements
domain targets — is a technically strong design that does not meet a stated
requirement, because the requirement was never written down. A design that
elegantly secures the wrong thing is the architect's version of Chapter
02's shadowing rule: correct-looking, and wrong where it counts. The
defense is the requirements-first discipline.

## Security and Best Practices

- **Make risk acceptance explicit and owned.** Where a risk is not fully
  mitigated, the residual risk should be named and accepted by someone
  accountable, not left implicit. Silent residual risk is how designs fail
  audits and incidents alike.
- **Design least privilege and assume-breach into the architecture.** The
  Chapter 01 and Chapter 08 principles are design inputs, not operational
  add-ons; segment to contain, and grant minimally by default.
- **Automate the security controls, and secure the automation.** The
  pipelines and APIs that operate security are themselves tier-0; a
  compromised deployment pipeline compromises everything it deploys.
- **Design assurance in.** Visibility and logging are what make a design
  auditable and an incident answerable; a design without them is
  unfalsifiable, which is not a compliment.
- **Keep the design current with the threat and the platform.** A security
  architecture decays as threats and products evolve; designing for change
  is designing for security over time.

## References and Knowledge Checks

**References**

- [Cisco 300-745 SDSI exam topics](https://learningnetwork.cisco.com/s/sdsi-exam-topics)
  — the design concentration's domains and subtopics.
- [Volume X — Enterprise Cybersecurity](../../volume-10-enterprise-cybersecurity/README.md)
  — vendor-neutral risk frameworks and security architecture the design
  reasoning draws on.
- [Volume XII, Chapter 01](../../volume-12-resilience-lifecycle-management/chapters/01-resilience-engineering-and-critical-service-design.md)
  — critical-service and resilience design that complements security
  design.
- All prior chapters of this volume — the enforcement points SDSI composes.

**Knowledge checks**

1. Why does a security design begin with requirements and risk rather than
   products, and what anti-pattern does starting from products create?
2. Name the layers of secure infrastructure and explain what "composition"
   means as a design skill.
3. What distinguishes defense in depth from defense in duplicate?
4. What is DevSecOps, and how does shift-left scanning apply the
   Chapter 03 cloud-posture idea to the pipeline?
5. Give the characteristic SDSI design failure and the discipline that
   prevents it.

## Hands-On Lab

**Objective:** Produce a complete security design record for a stated
scenario — the capstone that composes the whole volume — and implement a
shift-left automation control.

**Prerequisites:** The knowledge from Chapters 01–08; a machine with
`checkov` (or an equivalent IaC scanner) for the automation portion. No
licensed Cisco products — this is a design capstone.

**This capstone is design work, reproducible without licensed products.**
It exercises the SDSI reasoning and the DevSecOps automation, which is
where the exam's weight and the role's value both sit.

**Procedure — the capstone design**

1. **Requirements (SDSI 30%).** Take a scenario: a hybrid-work company with
   remote staff, a cloud-hosted finance application holding regulated data,
   and branch sites. Write down its security requirements — who must reach
   what, what data must be protected, what compliance applies.
2. **Risk (SDSI 30%).** For each requirement, name the threats (Chapter 01)
   and rate likelihood and impact.
3. **Design across the layers.** Select controls composing this volume:
   - Firewall and IPS at the edge ([Chapter 02](02-network-security-with-cisco-secure-firewall-and-ips.md)).
   - Site connectivity via VPN ([Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md)).
   - Identity-based access and segmentation (Chapters [05](05-secure-network-access-visibility-and-enforcement.md)–[06](06-identity-services-engine-deployment-policy-and-services.md)).
   - Cloud and service-edge controls ([Chapter 03](03-cloud-security-and-the-secure-service-edge.md)).
   - Zero-trust application access for remote staff ([Chapter 08](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)).
   - Endpoint protection ([Chapter 04](04-content-security-and-endpoint-protection.md)).
4. **Trace and record.** Produce the design record so each control traces
   to a risk and each risk to a requirement. Name any residual risk.
5. **Assurance.** State how the design is monitored and how an incident
   would be answered.

**Procedure — the automation**

6. Write an infrastructure-as-code file with a deliberate misconfiguration
   (an open security group, an unencrypted store) and scan it with
   `checkov`. Confirm it fails.
7. Remediate and re-scan; confirm it passes. Wire it as a pipeline gate
   (a non-zero exit fails the build) — shift-left security in practice.

**Negative test**

8. Review your design record and remove one requirement, then check
   whether any control is now unjustified — demonstrating that controls
   without requirements are cost, and that the requirements-first
   discipline is what keeps a design honest. Restore it.

**Expected results**

- A complete design record composing every enforcement point in the
  volume, with controls traced to risks and risks to requirements.
- A named, owned residual risk and an assurance story.
- A working shift-left scan that gates a deployment on security.

**Cleanup**

9. This capstone produces design artifacts and a scan pipeline; retain
   them. They are the deliverable, and together they demonstrate the whole
   CCNP Security track applied to one scenario.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SDSI is a design exam, and design is judgment: it begins with requirements
and risk, not products, and its two 30% domains encode exactly that
reasoning. Secure infrastructure design is the composition of everything
this volume covered — firewall and IPS, VPN and secure connectivity,
identity-based access, cloud and service-edge controls, and zero-trust
application access — into layers that reinforce one another for defense in
depth without wasteful duplication. Application security extends the
boundary to workloads and pipelines, and automation, DevSecOps, and AI
operationalize the design and shift security left into the delivery
process. The capstone composes the whole CCNP Security track into one
requirements-driven reference design, which is both the SDSI skill and the
truest picture of the role the certification represents: not configuring a
product, but architecting security that meets stated requirements against
real risk.

- [ ] Can explain why design starts with requirements and risk, not
      products.
- [ ] Can compose the volume's enforcement points into a layered design.
- [ ] Can distinguish defense in depth from duplication.
- [ ] Can apply DevSecOps shift-left scanning as a pipeline gate.
- [ ] Has produced a capstone design record tracing controls to risks to
      requirements.
