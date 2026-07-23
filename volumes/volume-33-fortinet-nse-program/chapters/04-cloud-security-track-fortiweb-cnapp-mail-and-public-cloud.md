# Chapter 04: Cloud Security Track — FortiWeb, CNAPP, Mail, and Public Cloud

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
(verified 22 July 2026). NSE 4 (FortiGate/FortiOS, Volume XIX) remains
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

FortiWeb VM in front of a lab web app: tune a protection profile in
detection mode against real requests, then enable blocking with a
false-positive control. In a cloud account (or runbook against the
admin guides): insert a FortiGate VM with an SDN connector, prove
traffic is inspected (routing verified), and onboard the account to
FortiCNAPP with inventory verification.

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
