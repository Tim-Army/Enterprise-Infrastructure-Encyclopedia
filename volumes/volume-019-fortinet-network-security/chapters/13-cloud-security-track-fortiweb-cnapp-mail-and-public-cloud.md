# Chapter 13: Cloud Security Track — FortiWeb, CNAPP, Mail, and Public Cloud

## Learning Objectives

- Operate the Cloud Security product estate: FortiWeb (WAF), FortiADC
  (delivery), FortiAppSec, FortiMail, FortiDDoS, and FortiCNAPP
- Deploy FortiGate-based security in AWS, Azure, and GCP (the public
  cloud administrator exams)
- Design cloud-native application protection with FortiCNAPP and the
  Public Cloud Security Architect apex
- Map the Cloud Security NSE 5–7 ladder atop the shared NSE 4 foundation

## Theory and Architecture

### The track in one sentence

Cloud Security certifies protecting applications and workloads in and
in front of the cloud: **NSE 5** covers application-delivery and web
protection (FortiWeb, FortiADC, FortiAppSec Administrators); **NSE 6**
the cloud-workload and messaging estate (AWS/Azure/GCP Cloud Security
Administrators, FortiMail, FortiMail Workspace, FortiDDoS, and
FortiCNAPP Analyst); **NSE 7** is the Public Cloud Security Architect
(verified 22 July 2026). NSE 4 (FortiGate/FortiOS, Chapter 09) remains
the shared prerequisite — the cloud track secures workloads a FortiGate
often fronts.

### Two problem shapes: front-door and in-cloud

The **front-door** products protect applications regardless of where
they run: FortiWeb inspects HTTP(S) for the OWASP-class attacks a
network firewall misses; FortiADC load-balances and offloads;
FortiDDoS absorbs volumetric attacks; FortiMail secures the email
channel. The **in-cloud** products live in the provider: FortiGate VM
as the cloud network firewall (the AWS/Azure/GCP administrator exams —
VPC/VNet insertion, routing, auto-scaling, native integration), and
**FortiCNAPP** as the cloud-native application protection platform
(posture, workload, IaC, and runtime — the CSPM/CWPP model Volume VII
and the Palo Alto CNAPP chapter also teach).

### The Architect apex

Public Cloud Security Architect (NSE 7) designs across both shapes and
all three providers: hub-and-spoke security VPCs, auto-scaling
inspection, native-service integration, and CNAPP-driven posture — the
Volume VII landing-zone doctrine expressed in Fortinet products.

## Design Considerations

- FortiWeb in front of every internet-facing app the network firewall
  cannot inspect at layer 7; FortiADC where delivery and offload
  matter
- Cloud network firewall insertion is a routing-and-scale design:
  gateway load balancer / native integration, auto-scaling groups,
  and the failure domain of the security VPC (Volume VII rules)
- FortiCNAPP posture is only as good as account coverage — onboard
  every account before trusting a single finding
- Choose AWS vs. Azure vs. GCP exam by the estate; the architecture
  patterns rhyme, the native services differ

## Implementation and Automation

```text
# FortiWeb: a protection profile in front of an app (NSE 5)
config waf profile
  edit "app1-waf"
    set signature "high"
    set threat-weight enable
# FortiGate in AWS (NSE 6): SDN connector for dynamic address groups
config system sdn-connector
  edit "aws1"
    set type aws
    set region "us-east-1"
# FortiCNAPP (NSE 6): onboard account, then verify coverage before tuning
#   1. connect cloud account (agentless + agent)
#   2. confirm asset inventory completeness
#   3. tune posture policy to the compliance baseline
```

## Validation and Troubleshooting

- FortiWeb: false positives are the WAF tax — tune in detection mode
  against real traffic before blocking; the NSE 5 exam's judgment core
- Cloud firewall: verify the SDN connector resolves dynamic objects and
  that routing actually steers traffic through inspection (asymmetric
  routing is the classic cloud-insertion failure)
- FortiCNAPP: coverage gaps masquerade as clean posture — inventory
  completeness first, findings second
- FortiMail: mailflow and policy order before spam/AV theories

## Security and Best Practices

- Least-privilege cloud roles for FortiGate SDN connectors and
  FortiCNAPP onboarding; the security tool does not need broad write
- WAF in blocking mode only after a tuning window; DDoS thresholds
  sized to real baselines
- Findings routed into the SOC (Chapter 03) — one incident queue, not
  a per-product silo

## References and Knowledge Checks

- Fortinet Training Institute exam pages: FortiWeb, FortiADC,
  FortiAppSec, FortiMail, FortiDDoS, FortiCNAPP, AWS/Azure/GCP Cloud
  Security, Public Cloud Security Architect (NSE 5–7 Cloud Security)
- Product admin guides; Volume VII (cloud) of this encyclopedia

Knowledge checks:

1. Separate the front-door products from the in-cloud products and give
   each one's job in a sentence.
2. Name the classic cloud network-firewall insertion failure and how
   you prove it.
3. Why does FortiCNAPP posture require account-coverage verification
   before finding-level tuning?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each key product of the Cloud
Security track (NSE 5–7)** — FortiWeb, FortiMail, FortiADC, FortiGate-VM in public cloud,
and FortiCNAPP/FortiDDoS — mapped in the volume README's coverage tables. Every lab gives
concrete, verifiable steps and ends **`**Lab verified by:** *pending*`** until a human runs
it.

**Shared prerequisites for Labs 13.1–13.5** — the relevant product (FortiWeb, FortiMail,
FortiADC as VM or hardware; a cloud account for FortiGate-VM), a web/mail backend to
protect, and a client. **Cost:** cloud-marketplace BYOL/PAYG charges apply only to Lab
13.4 if you deploy in a real cloud account — the on-prem labs are free.

### Lab 13.1 — FortiWeb WAF policy (Topic: FortiWeb)

**Objective:** Front a web app with a WAF in reverse-proxy mode.

```text
# On FortiWeb: create a Server Pool -> Virtual Server -> Server Policy, then verify:
diagnose policy total-detail-list 2>/dev/null | head
# From a client, send a benign request and an obvious SQLi probe:
#   curl "http://<vip>/product?id=1"
#   curl "http://<vip>/product?id=1' OR '1'='1"
```

**Expected result:** the benign request passes; the SQL-injection probe is blocked and
logged by the WAF signature/anomaly engine — FortiWeb protects web apps against OWASP
Top-10 attacks, bots, and API abuse that a network firewall does not inspect at layer 7.

**Negative test:** deploy FortiWeb in pass-through with the policy in "alert only"; the
SQLi is logged but delivered to the app — the policy action must be `block`/`deny` to
enforce.

**Rollback:** remove the lab server policy.

### Lab 13.2 — FortiMail antispam and antimalware (Topic: FortiMail)

**Objective:** Filter inbound mail in gateway mode.

```text
# On FortiMail (gateway mode): set the protected domain and an inbound recipient policy
#   with antispam + antivirus profiles, then send a test message.
diagnose system top 2>/dev/null | head
# Send an EICAR attachment and a GTUBE spam-test message; confirm both are caught.
```

**Expected result:** the GTUBE spam-test string is quarantined/rejected and the EICAR
attachment is stripped — FortiMail secures the email vector (spam, phishing, malware, and
outbound DLP) that is the top initial-access route for attackers.

**Negative test:** MX-route mail straight to the server, bypassing FortiMail; none of the
filtering applies — FortiMail must sit in the mail flow (MX/relay) to inspect.

**Rollback:** remove the lab protected-domain and policy.

### Lab 13.3 — FortiADC application delivery (Topic: FortiADC)

**Objective:** Load-balance a web pool with a health check.

```text
# On FortiADC: create Real Servers -> Real Server Pool (with an HTTP health check)
#   -> Virtual Server, then verify:
diagnose load-balance real-server list 2>/dev/null | head
# Stop one backend and confirm traffic shifts to the healthy member.
```

**Expected result:** requests distribute across healthy backends by the chosen algorithm,
and a failed backend is removed from rotation by the health check — FortiADC delivers
availability, SSL offload, and L7 optimization alongside security.

**Negative test:** configure the pool with no health check; when a backend dies the ADC
keeps sending it traffic and users get errors — the health check is what makes load
balancing resilient.

**Rollback:** remove the lab virtual server and pool.

### Lab 13.4 — FortiGate-VM in public cloud (Topic: Cloud FortiGate — AWS/Azure/GCP)

**Objective:** Confirm a cloud-deployed FortiGate-VM's licensing and SDN connector.

```text
get system status | grep -iE "License|VM"
config system sdn-connector
    edit aws-sdn
        set type aws
        set use-metadata-iam enable
    next
end
diagnose sys sdn-connector status 2>/dev/null | head
```

**Expected result:** the FortiGate-VM reports a valid cloud license (BYOL or PAYG) and the
SDN connector pulls dynamic address objects from the cloud (instances by tag/security
group) — cloud FortiGate secures north-south and east-west traffic with objects that track
cloud changes automatically.

**Negative test:** write static IP policies for auto-scaling cloud workloads; addresses
churn and policies break — SDN-connector dynamic objects are what keep policy correct as
the cloud changes.

**Rollback:** delete the `aws-sdn` connector if lab-only.

### Lab 13.5 — Cloud posture and DDoS: FortiCNAPP and FortiDDoS (Topic: FortiCNAPP / FortiDDoS)

**Objective:** Read a cloud posture finding and a DDoS mitigation baseline.

```text
# FortiCNAPP (Lacework FortiCNAPP): review a compliance finding
#   (e.g. a public S3 bucket / over-permissive IAM) and its remediation guidance.
# FortiDDoS: confirm the appliance has learned a traffic baseline, then:
diagnose ddos setting 2>/dev/null | head
```

**Expected result:** FortiCNAPP surfaces misconfigurations and risky IAM across cloud
accounts (CSPM/CWPP), and FortiDDoS shows a learned per-service baseline it uses to
distinguish attack floods from legitimate spikes — cloud security spans posture and
volumetric defense, not just the firewall.

**Negative test:** set FortiDDoS thresholds manually without letting it learn a baseline;
it either misses attacks or blocks legitimate bursts — behavioral baselining is what makes
mitigation accurate.

**Rollback:** none (read-only review).

## Lab Verification

Verification means the WAF blocked attacks without blocking the
control, cloud inspection was proven by routing evidence (not
assumption), and the CNAPP onboarding showed complete inventory before
any policy tuning.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Front-door protection (FortiWeb) tuned and enforced (NSE 5)
- [ ] Cloud firewall insertion proven with routing evidence (NSE 6)
- [ ] FortiCNAPP onboarding with coverage verification (NSE 6)
- [ ] Cloud Security NSE 5–7 ladder recorded from verified sources
