# Chapter 07: Security, Hardening, Incident Response, and Risk Reference

## Learning Objectives

- Apply the CIA triad and defense-in-depth as consolidated decision
  frameworks when evaluating a control across any platform in this
  encyclopedia.
- Locate the appropriate hardening baseline (CIS Benchmark or vendor
  guide) for a given platform and explain the CIS Benchmark profile
  levels.
- Execute the NIST SP 800-61 incident response lifecycle phases in order
  and know what evidence each phase requires.
- Score and prioritize a vulnerability using CVSS severity bands and a
  likelihood-times-impact risk matrix.
- Classify data and incidents consistently enough to select the correct
  retention, disclosure, and escalation path.

## Theory and Architecture

Security across every volume in this encyclopedia rests on the same small
set of frameworks, restated per platform but never fundamentally
different:

- **The CIA triad** — Confidentiality (only authorized parties can read
  data), Integrity (data and systems are not altered without
  authorization or detection), Availability (authorized parties can
  access data and systems when needed) — is the lens every control in
  this chapter is ultimately justified through. A control that improves
  one leg of the triad at severe, unexamined cost to another (for
  example, logging so verbose it degrades availability) is not
  automatically a good trade.
- **Defense in depth** layers independent controls so that a single
  control's failure does not equal a breach: network segmentation
  ([Chapter 02](02-ports-protocols-services-and-traffic-flows.md)), host hardening (this chapter), identity and access
  management ([Chapter 03](03-addressing-subnetting-naming-time-and-identity-reference.md), [Volume X](../../volume-10-enterprise-cybersecurity/README.md)), logging and detection ([Volume XI](../../volume-11-observability-enterprise-operations/README.md)),
  and incident response (this chapter) are deliberately redundant rather
  than each covering a unique, non-overlapping slice of risk.
- **Hardening baselines** (CIS Benchmarks, DISA STIGs, vendor security
  guides) translate defense-in-depth principles into specific,
  checkable settings per platform — the same baseline concept introduced
  generically in [Chapter 04](04-configuration-templates-baselines-and-change-records.md), applied specifically to security posture
  here.
- **Incident response** is a lifecycle, not a single action: NIST SP
  800-61 defines Preparation, Detection and Analysis, Containment,
  Eradication and Recovery, and Post-Incident Activity as sequential
  phases, each with distinct objectives and each dependent on the
  troubleshooting groundwork from [Chapter 06](06-troubleshooting-decision-aids-and-escalation.md) but requiring additional
  evidence-preservation discipline that routine troubleshooting does not.
- **Risk** is formally the product of likelihood and impact, not either
  alone; a high-impact, near-zero-likelihood event and a low-impact,
  frequent event can land at the same risk score, and treating them
  identically (or ignoring the low-impact/high-frequency category
  entirely) is a common risk-management failure.

## Design Considerations

- **Select a CIS Benchmark profile level deliberately, not by default.**
  CIS Benchmarks publish Level 1 (broadly applicable, minimal operational
  impact) and Level 2 (defense-in-depth, higher operational impact,
  intended for higher-security environments) profiles per platform;
  applying Level 2 everywhere without assessing operational impact is as
  much a design failure as applying no hardening at all.
- **Map every control back to a specific risk it mitigates.** A control
  applied because "it's in the benchmark" without a stated rationale is
  hard to defend during an exception request and hard to prioritize
  during a resource-constrained hardening effort; tie each control to a
  CIA-triad impact and, where possible, a specific threat.
- **Design incident response roles before an incident, not during one.**
  Incident Commander, Communications Lead, and technical responders are
  roles, not necessarily fixed individuals, and should be assignable from
  an on-call rotation consistent with the escalation matrix in [Chapter 06](06-troubleshooting-decision-aids-and-escalation.md).
- **Decide data classification tiers before they are needed for a
  disclosure or retention decision.** A simple three- or four-tier model
  (Public, Internal, Confidential, Restricted) applied consistently is
  more useful under time pressure than a granular scheme few people
  remember correctly.
- **Pre-authorize emergency/break-glass access with mandatory
  post-use review**, rather than either requiring full change approval
  during an active Sev 1 security incident (too slow) or leaving
  emergency access entirely unaudited (too risky).
- **Budget for the eradication and recovery phases explicitly**, not just
  detection and containment; an incident response plan that stops at
  "contained" leaves the actual return to a known-good, hardened state
  ([Chapter 04](04-configuration-templates-baselines-and-change-records.md)'s baseline) undone.

## Implementation and Automation

### CIS Benchmark profile levels

| Profile | Description | Typical Application |
| --- | --- | --- |
| Level 1 | Foundational, minimal operational impact, broadly applicable | Default baseline for nearly all systems |
| Level 2 | Defense-in-depth, may reduce functionality or increase operational overhead | Higher-security zones, regulated workloads, systems handling Restricted-tier data |
| STIG (DISA) | Department of Defense Security Technical Implementation Guide, generally at least as strict as CIS Level 2 | US federal/defense-adjacent environments; often required contractually |

### NIST SP 800-61 incident response lifecycle

| Phase | Objective | Key Evidence/Output |
| --- | --- | --- |
| Preparation | Establish tools, access, playbooks, and communication paths before an incident occurs | IR plan, contact list, pre-provisioned forensic/response tooling |
| Detection and Analysis | Identify a candidate incident, confirm scope and severity, distinguish false positives | Alert source, initial timeline ([Chapter 06](06-troubleshooting-decision-aids-and-escalation.md) format), affected-system list, severity classification |
| Containment | Limit further damage/spread while preserving evidence — short-term (isolate) and long-term (patch/segment) containment are distinct steps | Network isolation records, credential revocation log, forensic images/snapshots taken before remediation |
| Eradication and Recovery | Remove the root cause (malware, unauthorized access, vulnerability) and restore systems to a validated, hardened baseline ([Chapter 04](04-configuration-templates-baselines-and-change-records.md)) | Baseline validation evidence ([Chapter 05](05-validation-evidence-checklists-and-acceptance.md)), patch/rebuild records |
| Post-Incident Activity | Blameless review, root-cause documentation, corrective action tracking | Post-incident report, updated decision tree/baseline/runbook, corrective action tickets |

### CVSS v3.1/v4.0 severity bands

| CVSS Score | Severity | Typical Enterprise Response Expectation |
| --- | --- | --- |
| 0.1 – 3.9 | Low | Scheduled remediation within standard patch cycle |
| 4.0 – 6.9 | Medium | Remediation within a defined SLA (commonly 30–90 days), sooner if internet-facing |
| 7.0 – 8.9 | High | Expedited remediation (commonly 7–14 days), compensating controls if remediation is delayed |
| 9.0 – 10.0 | Critical | Emergency change process; remediation or compensating control within days, immediate for actively exploited/internet-facing findings |

CVSS score alone is a starting point, not a final priority; combine it
with exploitability in the wild (known exploited vulnerability catalogs),
asset criticality, and exposure (internet-facing vs. internal-only) before
setting a final remediation SLA.

### Risk matrix (likelihood × impact)

| | Impact: Low | Impact: Medium | Impact: High | Impact: Critical |
| --- | --- | --- | --- | --- |
| **Likelihood: Rare** | Low | Low | Medium | High |
| **Likelihood: Unlikely** | Low | Medium | High | High |
| **Likelihood: Possible** | Medium | Medium | High | Critical |
| **Likelihood: Likely** | Medium | High | Critical | Critical |
| **Likelihood: Almost Certain** | High | Critical | Critical | Critical |

Resulting risk rating drives action: Low risks are tracked and
periodically reviewed; Medium risks require a documented mitigation plan
and owner; High risks require active mitigation with a target date and
management visibility; Critical risks require immediate action and, in
most organizations, executive/board-level visibility.

### Data classification reference

| Tier | Definition | Example | Handling Baseline |
| --- | --- | --- | --- |
| Public | Approved for unrestricted release | Marketing material, published documentation (like this encyclopedia) | No special handling |
| Internal | Not for external release, low individual sensitivity | Internal wiki content, non-sensitive configuration | Access limited to employees/contractors |
| Confidential | Sensitive business or personal data | Customer PII, financial reports, source code | Access limited to a defined need-to-know group; encryption at rest and in transit |
| Restricted | Highest sensitivity; regulatory, legal, or severe business impact if disclosed | Authentication secrets, cardholder data, protected health information | Strict access control, mandatory encryption, enhanced logging and retention per [Chapter 09](09-standards-certifications-vendor-documentation-and-reference-governance.md)'s governing standards |

### Common enterprise hardening actions by platform (cross-reference)

| Platform | Representative Hardening Actions | Primary Baseline Source |
| --- | --- | --- |
| RHEL 10 / Ubuntu 26.04 | SELinux/AppArmor enforcing mode, disable unused services, `auditd` enabled, SSH key-only auth | CIS Benchmark for the respective distribution |
| Windows Server | LAPS or equivalent for local admin credentials, disable legacy SMBv1, enforce Credential Guard where supported | CIS Benchmark for Windows Server; Microsoft Security Baselines |
| Cisco IOS XE | `service password-encryption`, disable unused management protocols, AAA via TACACS+ ([Chapter 01](01-command-quick-reference-and-safe-administration.md)) | Cisco hardening guide; CIS Benchmark for Cisco IOS |
| PAN-OS / FortiOS | Disable default admin account, enforce MFA for administrative access, minimize management-plane exposure | Vendor hardening guide; CIS Benchmark where published |
| VMware vSphere | Enable lockdown mode, disable SSH/ESXi Shell by default, enforce certificate-based host management | VMware vSphere Security Configuration Guide |
| Kubernetes | Disable anonymous kubelet access ([Chapter 02](02-ports-protocols-services-and-traffic-flows.md)), Pod Security Standards enforcement, network policies default-deny | CIS Kubernetes Benchmark |
| AWS | Root account MFA and disuse for daily operations, IAM least privilege, GuardDuty/Security Hub enabled | CIS AWS Foundations Benchmark |

## Validation and Troubleshooting

- **Verify hardening controls are actually applied, not merely
  documented as applied.** A CIS Benchmark checklist item marked complete
  should be backed by the same evidence discipline established in Chapter
  05 — a scan output or configuration query, not a memory of having done
  it.
- **Reconcile a vulnerability scanner's finding against actual
  exploitability before escalating blindly.** A Critical CVSS score on a
  component that is present but not reachable/enabled may warrant a lower
  practical priority than a Medium score on an internet-facing,
  actively-exploited component; document the reasoning either way.
- **During containment, confirm isolation actually holds** (re-test the
  five-field flow statement from [Chapter 02](02-ports-protocols-services-and-traffic-flows.md) for the isolated system)
  rather than assuming a firewall rule or network access control change
  took effect as intended.
- **Distinguish a detection false positive from a true negative during
  the Detection and Analysis phase**, and document which was concluded
  and why; an unexplained "false positive" dismissal without evidence is
  a common way real incidents get missed.
- **Re-run the acceptance checklist ([Chapter 05](05-validation-evidence-checklists-and-acceptance.md)) against the recovery
  baseline before declaring Eradication and Recovery complete**; a system
  restored from backup or rebuilt must be validated against the current
  hardened baseline, not simply returned to its pre-incident state, which
  may reintroduce the same vulnerability.

## Security and Best Practices

- Apply the principle of least privilege to every identity, service
  account, and network path referenced throughout this encyclopedia;
  most controls in the hardening table above are specific expressions of
  this one principle.
- Treat logging and alerting as a control in its own right, not an
  afterthought — an incident that cannot be detected cannot be responded
  to, regardless of how strong preventive controls are ([Volume XI](../../volume-11-observability-enterprise-operations/README.md)).
- Test incident response plans with tabletop exercises on a recurring
  cadence, not only when a real incident forces the first execution;
  an untested plan reliably surfaces gaps at the worst possible time.
- Preserve forensic evidence (memory captures, disk images, log exports)
  before remediating a suspected compromised system wherever feasible;
  premature remediation is a common, avoidable cause of lost root-cause
  evidence.
- Review and update hardening baselines whenever the platform's
  `SOFTWARE_VERSIONS.md` baseline changes; CIS Benchmarks and vendor
  guides are versioned to specific platform releases and drift from the
  running baseline over time.
- Report suspected security incidents through the defined escalation path
  ([Chapter 06](06-troubleshooting-decision-aids-and-escalation.md)) immediately, even with incomplete information; delay while
  gathering more certainty before reporting is a common and costly
  anti-pattern.

## References and Knowledge Checks

**References**

- NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide.
- NIST SP 800-53 — Security and Privacy Controls for Information Systems
  and Organizations.
- CIS Benchmarks (`cisecurity.org/cis-benchmarks`) — per-platform
  hardening guides referenced throughout this table.
- FIRST CVSS v3.1/v4.0 specification (`first.org/cvss`).
- DISA STIGs (`public.cyber.mil/stigs`).
- [Chapter 04](04-configuration-templates-baselines-and-change-records.md) of this volume — baselines that incident recovery restores
  systems to.
- [Chapter 05](05-validation-evidence-checklists-and-acceptance.md) of this volume — evidence and acceptance discipline applied
  to hardening and recovery validation.
- [Volume X](../../volume-10-enterprise-cybersecurity/README.md) — Enterprise Cybersecurity (full architectural and control
  treatment).

**Knowledge checks**

1. Explain the difference between CIS Benchmark Level 1 and Level 2
   profiles, and give a scenario where Level 2 is appropriate.
2. Why does a high CVSS score not automatically imply the highest
   practical remediation priority?
3. List the five NIST SP 800-61 incident response phases in order and
   name one required evidence artifact from each.
4. A likelihood-times-impact assessment places a finding at "Possible ×
   High." What risk rating results, and what organizational response does
   that rating typically require?

## Hands-On Lab

**Objective:** Build a security and incident-response quick-reference
card covering a hardening baseline lookup, a risk-scoring exercise, and a
simulated incident walked through the NIST 800-61 lifecycle.

**Prerequisites:** A lab or work system you can evaluate against a public
hardening benchmark; internet access to retrieve the relevant CIS
Benchmark or vendor guide (or a locally cached copy); a Markdown editor.

1. Identify the correct CIS Benchmark (or vendor hardening guide) for one
   platform in your environment and record its title, version, and
   profile level chosen (Level 1 or 2), with a one-line justification for
   the level chosen. **Expected result:** a correctly identified,
   version-dated baseline reference.
2. Select five hardening controls from that benchmark and check each
   against your lab system, recording Pass/Fail evidence in the format
   from [Chapter 05](05-validation-evidence-checklists-and-acceptance.md). **Expected result:** five controls checked with
   linked evidence.
3. For any Fail, assign a CVSS-style severity band (Low/Medium/High/
   Critical) using your best-effort assessment of impact and
   exploitability, and record the reasoning. **Expected result:** each
   Fail has a documented severity and rationale.
4. Plot each Fail on the risk matrix in this chapter using an assessed
   likelihood, and record the resulting risk rating. **Expected result:**
   a completed risk rating per finding.
5. Simulate a minor incident (for example, an unauthorized local account
   creation on a lab VM) and walk it through all five NIST 800-61 phases,
   recording at least one action and one piece of evidence per phase.
   **Expected result:** a phase-by-phase incident record covering
   Preparation through Post-Incident Activity.
6. Negative test: attempt to skip directly to Eradication without
   completing Containment, and note what evidence-preservation step would
   be lost by doing so. **Expected result:** a documented explanation of
   why phase order matters, based on a concrete example from the lab.
7. Remediate the highest-risk Fail from step 4 and re-validate it against
   the same control checked in step 2. **Expected result:** the control
   now passes, with before/after evidence retained.

**Cleanup:** Remove the unauthorized account created for the simulated
incident, revert any hardening control changed only for lab purposes if
it is not intended to persist, and confirm the lab system returns to its
baseline state from [Chapter 04](04-configuration-templates-baselines-and-change-records.md).

## Summary and Completion Checklist

This chapter consolidated the CIA triad and defense-in-depth as the
underlying justification for every control referenced across this
encyclopedia, mapped CIS Benchmark profile levels and CVSS severity bands
to concrete remediation expectations, provided a likelihood-times-impact
risk matrix, and walked the NIST SP 800-61 incident response lifecycle
with the evidence each phase requires.

- [ ] I can explain the CIA triad and defense-in-depth as they apply to a
      control in my own environment.
- [ ] I can locate and apply the correct hardening baseline and profile
      level for a given platform.
- [ ] I can score a finding's severity and plot it on the risk matrix to
      derive a risk rating.
- [ ] I can walk a simulated incident through all five NIST 800-61
      phases with evidence at each phase.
- [ ] I understand why evidence preservation must precede remediation
      wherever feasible.
