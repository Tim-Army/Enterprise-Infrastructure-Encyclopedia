# Chapter 11: Secure Networking Upper Levels — Switching, Wireless, and Management

## Learning Objectives

- Deploy FortiSwitch and Secure Wireless LAN under FortiGate control
  (FortiLink), the NSE 5 Secure Networking exams
- Operate the Secure Networking NSE 6 product estate: FortiManager,
  FortiAnalyzer, FortiAuthenticator, FortiNAC, FortiClient EMS,
  FortiVoice
- Design and troubleshoot enterprise firewall estates at NSE 7
  (Enterprise Firewall Administrator) and the LAN Edge / OT / SD-WAN
  architect exams
- Map the Secure Networking NSE 5–7 ladder atop the NSE 1–4 foundation

## Theory and Architecture

### The track in one sentence

Secure Networking extends the FortiGate foundation (Chapters 03–09) across
the campus and branch fabric: **NSE 5** certifies FortiSwitch
Administration and Secure Wireless LAN Administration; **NSE 6** the
management-and-services layer (FortiManager, FortiAnalyzer,
FortiAuthenticator, FortiNAC, FortiClient EMS, FortiVoice) plus
architect roles (LAN Edge Architect, OT Security Architect, SD-WAN
Architect, SD-WAN Enterprise Administrator, Secure Networking Support
Engineer); **NSE 7** is the Enterprise Firewall Administrator — the
multi-FortiGate, policy-at-scale apex (verified 22 July 2026).

### FortiLink: the switch and AP as fabric extensions

FortiSwitch and FortiAP managed over **FortiLink** turn the FortiGate
into the single management and policy point for wired and wireless
access — VLANs, 802.1X, and security policy authored once and enforced
at the edge. The NSE 5 exams live in this integration: FortiLink
provisioning, VLAN and port policy, wireless SSIDs and security, and
the troubleshooting that follows when the fabric link misbehaves.

### Management scales the estate

At NSE 6, **FortiManager** centralizes configuration (ADOMs, policy
packages, provisioning) and **FortiAnalyzer** centralizes logging and
reporting — the Fortinet equivalents of the fleet-management discipline
Volume IX teaches. **FortiAuthenticator** and **FortiNAC** own
identity and access control at the edge (the Volume XV Forescout
patterns apply). The Enterprise Firewall NSE 7 ties it together:
consistent policy across many FortiGates, managed from FortiManager,
with the automation and troubleshooting depth an enterprise demands.

## Design Considerations

- FortiLink-managed access is a consolidation win and a blast-radius
  decision: the FortiGate becomes the access fabric's control plane —
  draw it as one failure domain (Volume II doctrine)
- FortiManager ADOM and policy-package design before the tenth device;
  retrofitting central management onto drifted firewalls is the
  classic pain the NSE 7 exam probes
- SD-WAN appears in both Secure Networking and SASE tracks — choose the
  track by the estate's center of gravity (branch WAN vs. cloud edge)

## Implementation and Automation

```text
# FortiLink + a secured access VLAN (the NSE 5 shape)
config system interface
  edit "fortilink"
    set fortilink enable
config switch-controller managed-switch
  edit "S148-lab"
    config ports
      edit "port1"
        set vlan "users"
        set port-security-policy "dot1x-users"

# FortiManager-driven policy (NSE 6/7): install a package to an ADOM
execute fmgr install-config package "Enterprise" adom "Campus"
diagnose dvm device list          # managed-device inventory + sync state
```

## Validation and Troubleshooting

- FortiLink first: `diagnose switch-controller switch-info status` —
  a switch that will not join is a fabric-link or auth problem, not a
  policy one
- Wireless: client association → auth → DHCP timeline; `diagnose
  wireless-controller wlac -c sta` for the station view
- FortiManager: device sync status and policy-package install logs
  before any "config not applying" theory
- NSE 7 Enterprise Firewall: policy consistency across FortiGates is a
  FortiManager question first, a per-box question second

## Security and Best Practices

- 802.1X / MAC-auth on access ports via FortiNAC/FortiAuthenticator;
  BPDU/loop protection on the wired edge
- Central logging to FortiAnalyzer as the audit substrate; management
  on a dedicated plane (Volume IV/X discipline)
- FortiManager as the single source of truth for policy — no per-box
  edits outside change control

## References and Knowledge Checks

- Fortinet Training Institute exam pages: FortiSwitch, Secure Wireless
  LAN, FortiManager, FortiAnalyzer, FortiAuthenticator, FortiNAC,
  Enterprise Firewall (NSE 5–7 Secure Networking)
- FortiOS, FortiSwitch, FortiManager admin guides; Volumes XV, XIX

Knowledge checks:

1. What does FortiLink centralize, and what failure domain does it
   create?
2. Order the tables you inspect when a FortiSwitch will not join the
   FortiGate.
3. Why is enterprise-firewall consistency a FortiManager problem before
   it is a FortiGate problem?

## Hands-On Lab

On a FortiGate VM lab (the platform from Chapters 03–09): FortiLink-manage a
FortiSwitch VM (or emulate), place a client on a secured VLAN with
802.1X, and prove policy enforcement; onboard the FortiGate into a
FortiManager ADOM and install a policy package; induce a FortiLink
auth failure and capture its signature before repair.

## Lab Verification

Verification means the managed switch joined and enforced port policy,
the FortiManager package installed with a clean sync, and the induced
FortiLink failure showed its distinct signature and was repaired.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] FortiLink switch/wireless management operated (NSE 5)
- [ ] FortiManager/FortiAnalyzer central management exercised (NSE 6)
- [ ] Enterprise Firewall consistency demonstrated (NSE 7)
- [ ] Secure Networking NSE 5–7 ladder mapped atop the NSE 1–4 foundation
