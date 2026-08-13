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

This chapter carries a topic-level walkthrough lab for **each key product of the Secure
Networking track (NSE 5–7)** — FortiSwitch, FortiAP/wireless, FortiManager,
FortiAuthenticator/FortiNAC, and Enterprise Firewall (the NSE 7 track exam) — mapped in
the volume README's coverage tables. Every command is a real FortiOS/product CLI action;
each lab ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 11.1–11.5** — a FortiGate on FortiOS 7.6 plus, per lab,
a FortiSwitch, a FortiAP, FortiManager, and FortiAuthenticator (VM or hardware). **Cost:**
none beyond lab resources.

### Lab 11.1 — FortiSwitch managed over FortiLink (Topic: FortiSwitch)

**Objective:** Adopt a FortiSwitch through FortiLink and push a VLAN.

```text
config system interface
    edit fortilink
        set fortilink enable
    next
end
execute switch-controller get-conn-status
config switch-controller managed-switch
    edit S1234567890
        config ports
            edit port5
                set vlan quarantine
            next
        end
    next
end
diagnose switch-controller switch-info list
```

**Expected result:** the FortiSwitch shows `Authorized/Up` and its ports are managed from
the FortiGate; a port reassigned to a VLAN takes effect centrally — FortiLink makes the
switch an extension of the FortiGate's security fabric.

**Negative test:** cable the switch but never authorize it in the switch controller; it
stays offline to management — adoption is an explicit authorization step.

**Rollback:** remove the lab switch's authorization and restore its port VLANs.

### Lab 11.2 — FortiAP managed wireless (Topic: Secure wireless)

**Objective:** Provision an SSID and push it to a managed FortiAP.

```text
config wireless-controller vap
    edit corp-wifi
        set ssid "LAB-CORP"
        set security wpa2-only-enterprise
        set auth usergroup
        set usergroup staff
    next
end
config wireless-controller wtp-profile
    edit lab-ap
        config radio-1
            set vap-all disable
            set vaps corp-wifi
        end
    next
end
diagnose wireless-controller wlac -c wtp
```

**Expected result:** the FortiAP broadcasts `LAB-CORP` with WPA2-Enterprise, and clients
authenticate against the `staff` group; `diagnose wireless-controller` lists the AP as
connected — the FortiGate is the wireless controller, unifying wired and wireless policy.

**Negative test:** define the VAP but never bind it to the AP's WTP profile radio; the
SSID never airs — the profile-to-radio binding is what activates it.

**Rollback:** remove the VAP from the profile and delete `corp-wifi`.

### Lab 11.3 — FortiManager central policy (Topic: Central management)

**Objective:** Manage the FortiGate's policy from FortiManager.

```text
# On FortiManager CLI:
config system admin setting
    set gui-theme blue
end
diagnose dvm device list
# Install a policy package to the managed FortiGate:
execute securityconsole install package "default" "LAB-FGT-01"
```

**Expected result:** the FortiGate appears under Device Manager, and a policy package
installs down to it; `diagnose dvm device list` shows it in sync — FortiManager gives
single-pane policy, object, and firmware management across many FortiGates.

**Negative test:** edit policy directly on the FortiGate while it is FortiManager-managed;
the next install overwrites the local change and flags the device out-of-sync — managed
devices are edited centrally.

**Rollback:** remove the lab device from FortiManager if temporary.

### Lab 11.4 — Identity and NAC with FortiAuthenticator (Topic: FortiAuthenticator / FortiNAC)

**Objective:** Use FortiAuthenticator as a RADIUS server for FortiGate auth.

```text
# On FortiAuthenticator: create a RADIUS client for the FortiGate, then on FortiGate:
config user radius
    edit FAC
        set server 10.0.0.241
        set secret <radius-secret>
    next
end
config user group
    edit radius-staff
        set member FAC
    next
end
diagnose test authserver radius FAC pap alice <password>
```

**Expected result:** `diagnose test authserver` returns `authentication succeeded` and
the user's group membership — FortiAuthenticator centralizes identity (RADIUS, 802.1X,
MFA, certificates), and FortiNAC extends this to device profiling and network access
control.

**Negative test:** point the FortiGate at the RADIUS server with the wrong shared secret;
every auth fails with a timeout — the secret must match on both ends.

**Rollback:** delete the `radius-staff` group and the `FAC` server.

### Lab 11.5 — Enterprise Firewall: advanced routing & troubleshooting (Topic: NSE 7 Enterprise Firewall)

**Objective:** Verify OSPF adjacency and inspect the FIB — NSE 7 Enterprise Firewall
territory.

```text
config router ospf
    set router-id 10.10.10.1
    config area
        edit 0.0.0.0
        next
    end
    config network
        edit 1
            set prefix 10.10.10.0 255.255.255.0
            set area 0.0.0.0
        next
    end
end
get router info ospf neighbor
get router info routing-table ospf
diagnose ip route list | head
```

**Expected result:** an OSPF neighbor in `Full` state and OSPF-learned routes in the
table — the NSE 7 Enterprise Firewall exam expects dynamic routing, ADVPN, and deep
troubleshooting across a multi-FortiGate estate.

**Negative test:** mismatch the OSPF area or network statement between neighbors; the
adjacency stalls in `ExStart/Exchange` — area and network agreement is required to peer.

**Rollback:**

```text
config router ospf
    unset router-id
end
```

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
