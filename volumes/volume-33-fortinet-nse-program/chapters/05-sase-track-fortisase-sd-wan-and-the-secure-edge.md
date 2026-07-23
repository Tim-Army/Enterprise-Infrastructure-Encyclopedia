# Chapter 05: SASE Track — FortiSASE, SD-WAN, and the Secure Edge

## Learning Objectives

- Deploy FortiSASE and SD-WAN as an integrated secure-access edge (the
  NSE 5 SASE Core exam)
- Operate the SASE product estate: FortiClient EMS, FortiDLP,
  FortiEDR, and SD-WAN at NSE 6
- Design enterprise SASE and SD-WAN fabrics at NSE 7 (FortiSASE and
  FortiSASE Enterprise Administrator)
- Map the SASE NSE 5–7 ladder and its overlap with the Secure
  Networking and Cloud tracks

## Theory and Architecture

### The track in one sentence

The SASE track certifies Fortinet's convergence of networking and
security at the edge: **FortiSASE** (cloud-delivered SWG, ZTNA, CASB,
FWaaS) meeting **Secure SD-WAN** (application-aware WAN over any
transport) so branch and remote users reach applications securely
without backhauling. The ladder runs **FortiSASE and SD-WAN Core
Administrator** at **NSE 5**; the endpoint-and-edge estate
(FortiClient EMS, FortiDLP, FortiEDR, SD-WAN Architect, SD-WAN
Enterprise Administrator) at **NSE 6**; and **FortiSASE
Administrator** and **FortiSASE Enterprise Administrator** at **NSE 7**
(verified 22 July 2026). NSE 4 remains the shared foundation.

### SD-WAN and SASE, two halves of one edge

Secure SD-WAN (introduced in Volume XIX, Chapter 08) steers
application traffic across links by SLA; FortiSASE extends the same
security stack to users who are nowhere near a branch — the
cloud-delivered POP inspects their traffic and applies ZTNA before
they reach the app. Together they are the modern edge: the branch gets
SD-WAN with on-box security, the roamer gets FortiSASE, and both
enforce one policy. The NSE 7 exams reward designing this as one
system, with FortiClient EMS as the shared endpoint control point.

### ZTNA and DLP at the edge

FortiClient EMS manages the endpoint agent that powers ZTNA (identity-
and posture-aware application access, replacing broad VPN) and feeds
FortiSASE. FortiDLP adds data-loss controls at the same edge, and
FortiEDR the endpoint detection/response that the SASE and SecOps
tracks share. The overlap is intentional — the edge is where
networking, access, and endpoint security converge.

## Design Considerations

- SD-WAN for the branch WAN, FortiSASE for users off the branch — most
  enterprises need both, enforcing one policy set
- ZTNA over legacy VPN wherever the endpoint is managed (FortiClient
  EMS): least-privilege, posture-gated app access (Volume X Zero Trust)
- SASE POP selection and SD-WAN underlay design decide user
  experience; measure it (Volume XI) rather than assume it
- FortiClient EMS is a shared control point across SASE, Secure
  Networking, and SecOps — design its role once

## Implementation and Automation

```text
# Secure SD-WAN member + SLA-based steering (NSE 5, from Volume XIX ch08)
config system sdwan
  set status enable
  config members
    edit 1
      set interface "wan1"
  config health-check
    edit "app-sla"
      set server "app.example.com"
      set members 1 2
# FortiSASE: ZTNA application + posture tag via FortiClient EMS (NSE 6/7)
#   - define the private application and its ZTNA policy
#   - require posture (AV on, disk encrypted) before access
#   - roamer traffic transits the FortiSASE POP; one policy, branch or not
```

## Validation and Troubleshooting

- SD-WAN: `diagnose sys sdwan health-check` and member SLA status
  before any steering theory; asymmetric routing is the recurring fault
- FortiSASE: user → POP → application path; verify the endpoint reached
  the right POP and posture evaluated as intended
- ZTNA denials: posture-tag evaluation first (a failed check reads as a
  block), then policy match, then the application connector
- FortiClient EMS: agent registration and profile assignment before
  endpoint-behavior guesses

## Security and Best Practices

- ZTNA default-deny with posture requirements; VPN retired where ZTNA
  reaches
- DLP policies (FortiDLP) at the edge for the data classes that matter,
  logged for audit
- SASE and SD-WAN policy authored once and enforced everywhere; no
  branch-local exceptions outside change control

## References and Knowledge Checks

- Fortinet Training Institute exam pages: FortiSASE and SD-WAN Core,
  FortiClient EMS, FortiDLP, FortiEDR, SD-WAN Architect/Enterprise,
  FortiSASE and FortiSASE Enterprise Administrator (NSE 5–7 SASE)
- FortiSASE and Secure SD-WAN admin guides; Volumes X, XI, XIX

Knowledge checks:

1. Which half of the edge serves the branch and which serves the
   roamer, and what makes them one system?
2. Why does ZTNA replace VPN where the endpoint is managed, and what
   gates access?
3. A ZTNA app is unreachable for one user only. Name the first thing
   you check and why.

## Hands-On Lab

Extend Volume XIX's SD-WAN lab: add SLA-based steering across two
links and prove failover; then (FortiSASE trial / free NSE labs, else
runbook) define a ZTNA application with a posture requirement in
FortiClient EMS, prove a compliant endpoint reaches it and a
non-compliant one is denied, and confirm a roaming user transits the
POP under the same policy.

## Lab Verification

Verification means SD-WAN steered and failed over by SLA with
evidence, the ZTNA app admitted the compliant endpoint and denied the
non-compliant one at the posture gate, and one policy governed both
branch and roaming paths.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Secure SD-WAN SLA steering and failover demonstrated (NSE 5)
- [ ] ZTNA with posture gating via FortiClient EMS shown (NSE 6/7)
- [ ] SASE POP path and one-policy enforcement understood
- [ ] SASE NSE 5–7 ladder recorded from verified sources
