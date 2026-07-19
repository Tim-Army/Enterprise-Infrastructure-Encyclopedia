# Chapter 07: Cisco Identity, Access Control, and Segmentation

![Lab topology for this chapter: CLI administration on DIST-01 authenticates via TACACS+, confirmed by incrementing request/response counters after an SSH login; ACCESS-01 has three identically configured open-mode 802.1X/MAB ports — Gi1/0/1 with an 802.1X-capable client authenticates via dot1x with a RADIUS/ISE-returned VLAN and dACL, Gi1/0/2 with a non-802.1X device falls back to MAB after the dot1x timeout, and Gi1/0/3 is the negative test. As a negative test, RADIUS reachability is removed and a new client on Gi1/0/3 either lands in the critical-authentication VLAN or stays unauthenticated per the port's server-dead action, rather than being silently granted access.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-07-8021x-mab-tacacs-topology.svg)

*Figure 7-1. Topology used throughout this chapter's Hands-On Lab: TACACS+-authenticated device administration alongside three access ports demonstrating 802.1X success, MAB fallback, and RADIUS-dead behavior.*

## Learning Objectives

- Explain AAA architecture and compare TACACS+ and RADIUS for device
  administration and network access respectively.
- Configure 802.1X port-based authentication with MAC Authentication
  Bypass (MAB) fallback for non-802.1X-capable endpoints.
- Explain Cisco Identity Services Engine (ISE)'s role as policy decision
  point and describe closed, open, and monitor 802.1X deployment modes.
- Describe Cisco TrustSec Security Group Tag (SGT) micro-segmentation and
  how it complements VRF-lite macro-segmentation from [Chapter 3](03-cisco-enterprise-routing-and-path-control.md).
- Configure downloadable ACLs (dACLs) and static SGT-to-VLAN mappings, and
  validate an authentication session end to end.
- Apply device-administration and network-access hardening consistent
  with the rest of this volume's security guidance.

## Theory and Architecture

### AAA architecture

**Authentication, Authorization, and Accounting (AAA)** is the framework
IOS XE uses to control who can manage a device and what a user or
endpoint is allowed to do once connected to the network. Two protocols
implement AAA against an external server, each suited to a different job:

| Protocol | Primary use | Transport | Key trait |
| --- | --- | --- | --- |
| TACACS+ | Device administration (CLI/console/VTY access) | TCP 49, fully encrypted body | Separates authentication, authorization, and accounting into distinct exchanges; can authorize individual commands |
| RADIUS | Network access (802.1X, VPN, MAB) | UDP 1812/1813 (or legacy 1645/1646), encrypts only the password attribute | Combines authentication and authorization in one exchange; the IETF standard for network access control, including EAP transport |

Cisco networks typically run **both**: TACACS+ against a AAA server (or
ISE's device-administration service) for administrator CLI access with
per-command authorization, and RADIUS against ISE for 802.1X/MAB network
access control — using the same identity source for both wherever
possible so that access decisions stay consistent.

### 802.1X and MAC Authentication Bypass

**802.1X** is the IEEE port-based network access control standard. Three
roles participate:

- **Supplicant** — the endpoint requesting access (a built-in OS 802.1X
  client, or dedicated supplicant software).
- **Authenticator** — the switch port, which blocks all traffic except
  EAP-over-LAN (EAPoL) frames until authentication succeeds.
- **Authentication server** — RADIUS (ISE), which validates credentials
  and returns an authorization result (VLAN, dACL, SGT).

Not every endpoint can run an 802.1X supplicant — printers, IP cameras,
and many IoT devices cannot. **MAC Authentication Bypass (MAB)** lets the
switch fall back to authenticating the endpoint's MAC address against
RADIUS when no 802.1X response arrives within a timeout, giving these
devices a policy-driven (if weaker) path onto the network instead of
requiring a manually configured static exception per port.

### Deployment modes

802.1X is rarely turned on network-wide in enforcing mode on day one; a
phased rollout uses three modes:

- **Monitor mode** — every authentication attempt is logged to RADIUS
  accounting, but the port is never actually blocked regardless of
  success or failure (`authentication open`). This exposes exactly which
  endpoints would fail authentication before any port is ever closed.
- **Open (low-impact) mode** — the port stays open by default
  (`authentication open`) so DHCP/basic traffic flows immediately, but a
  dynamic ACL is still applied pre-authentication to limit what an
  unauthenticated device can reach, and full access/VLAN/dACL policy is
  applied once authentication succeeds.
- **Closed mode** — the port blocks all traffic except EAPoL/MAB exchanges
  until authentication succeeds; this is the end-state most production
  designs converge to after monitor mode confirms endpoint readiness.

### Cisco ISE as policy decision point

**Cisco Identity Services Engine (ISE)** is the policy server most
current Cisco identity designs authenticate against. ISE combines several
roles that can be deployed on one appliance (small sites) or distributed
across dedicated persona nodes (large/HA deployments):

- **Policy Administration Node (PAN)** — the management/configuration
  point for policy authors.
- **Policy Service Node (PSN)** — the node that actually processes
  RADIUS/TACACS+ requests from switches (the policy decision point in the
  data path).
- **Monitoring and Troubleshooting (MnT) Node** — collects logs and
  authentication events for reporting and live session troubleshooting.

ISE evaluates authentication and authorization policy per request and can
return more than accept/reject — it can return a **VLAN assignment**, a
**downloadable ACL (dACL)**, a **Security Group Tag (SGT)**, or a
**Change of Authorization (CoA)** later in the session (for example, to
quarantine a device after a posture or threat-intelligence signal changes
without waiting for the endpoint to re-authenticate on its own).

### Cisco TrustSec and Security Group Tags

[Chapter 3](03-cisco-enterprise-routing-and-path-control.md) covered **VRF-lite** as a macro-segmentation tool — separate
routing tables for coarse-grained isolation (for example, a guest VRF
fully separated from the corporate VRF). **Cisco TrustSec** adds
**micro-segmentation** on top of that: instead of writing and maintaining
IP-address-based ACLs everywhere a policy boundary exists, TrustSec tags
traffic with a **Security Group Tag (SGT)** at its ingress point (assigned
by 802.1X/MAB authorization, or statically per VLAN/subnet/interface) and
then enforces policy based on that tag anywhere downstream, using a
**Security Group ACL (SGACL)** matrix keyed on source-SGT/destination-SGT
pairs instead of source-IP/destination-IP pairs.

Two mechanisms carry SGT information across the network:

- **Inline tagging** — the SGT is carried directly in a Cisco Meta Data
  (CMD) field inside the Ethernet frame on links between
  TrustSec-capable devices.
- **SGT Exchange Protocol (SXP)** — propagates IP-address-to-SGT bindings
  over a TCP session to devices that cannot inline-tag (for example, an
  older switch or a firewall consuming the binding for its own policy),
  decoupling tag propagation from every hop needing hardware inline-
  tagging support.

The practical benefit: an SGACL policy written as "Quarantine cannot talk
to Corporate_Servers" stays correct even as devices move between ports,
VLANs, and IP subnets, because enforcement follows the tag the endpoint
was assigned at authentication, not a static address.

## Design Considerations

- **Rollout sequencing** — always stage 802.1X as monitor mode, then open
  mode, then closed mode, per site or per switch block, rather than
  enabling closed-mode enforcement network-wide on day one; monitor mode
  is what surfaces devices that will fail authentication before that
  failure actually blocks a port.
- **MAB scope discipline** — treat MAB as a bridge for genuinely
  non-802.1X-capable devices, not a default fallback for every device that
  is merely inconvenient to configure; every MAB-authenticated device
  should still be inventoried and profiled (ISE profiling) rather than
  trusted purely by MAC address.
- **AAA server redundancy** — configure at least two RADIUS/TACACS+
  servers (or ISE PSNs) per site with an appropriate `deadtime`/failover
  timer, and define a documented **critical-authentication VLAN** or
  fallback behavior for what happens to new connections if every AAA
  server becomes unreachable — an all-server-down event should have a
  deliberate, tested outcome, not an accidental full lockout or full
  bypass.
- **VLAN vs. SGT segmentation** — use VLAN assignment where broadcast-
  domain-level separation is genuinely required (for example, isolating
  IoT traffic at Layer 2 for its own DHCP scope); use SGT/SGACL
  micro-segmentation where the goal is policy between groups of endpoints
  that otherwise share the same VLAN/subnet, since re-architecting VLANs
  for every new segmentation requirement does not scale operationally.
- **dACL vs. SGACL** — dACLs are simple, per-session, IP-based ACLs pushed
  to a single switch at authentication time; SGACLs are centrally
  authored once in the SGT matrix and enforced consistently everywhere
  that tag appears. Prefer SGACLs for policy that should apply
  network-wide; reserve dACLs for narrow, session-specific exceptions.
- **TACACS+ command authorization scope** — start with privilege-level
  authorization (view vs. full-admin) before investing in granular
  per-command TACACS+ authorization, and only add per-command granularity
  where a specific compliance or operational-risk requirement justifies
  the added policy maintenance.

## Implementation and Automation

### AAA and TACACS+ for device administration

```text
DIST-01(config)# aaa new-model
DIST-01(config)# tacacs server ISE-TACACS-01
DIST-01(config-server-tacacs)# address ipv4 10.10.99.20
DIST-01(config-server-tacacs)# key 0 <STRONG_TACACS_KEY>
DIST-01(config-server-tacacs)# exit
DIST-01(config)# aaa group server tacacs+ ISE-ADMIN
DIST-01(config-sg-tacacs+)# server name ISE-TACACS-01
DIST-01(config-sg-tacacs+)# exit
DIST-01(config)# aaa authentication login default group ISE-ADMIN local
DIST-01(config)# aaa authorization exec default group ISE-ADMIN local
DIST-01(config)# aaa authorization commands 15 default group ISE-ADMIN local
DIST-01(config)# aaa accounting exec default start-stop group ISE-ADMIN
DIST-01(config)# aaa accounting commands 15 default start-stop group ISE-ADMIN
```

The trailing `local` method in each `aaa authentication`/`aaa
authorization` line is the fallback used only if every TACACS+ server in
`ISE-ADMIN` is unreachable, so local emergency access still works during
an AAA outage.

### RADIUS for 802.1X/MAB

```text
DIST-01(config)# radius server ISE-PSN-01
DIST-01(config-radius-server)# address ipv4 10.10.99.21 auth-port 1812 acct-port 1813
DIST-01(config-radius-server)# key 0 <STRONG_RADIUS_KEY>
DIST-01(config-radius-server)# exit
DIST-01(config)# aaa group server radius ISE-NAC
DIST-01(config-sg-radius)# server name ISE-PSN-01
DIST-01(config-sg-radius)# exit
DIST-01(config)# aaa authentication dot1x default group ISE-NAC
DIST-01(config)# aaa authorization network default group ISE-NAC
DIST-01(config)# aaa accounting dot1x default start-stop group ISE-NAC
DIST-01(config)# dot1x system-auth-control
```

### 802.1X with MAB fallback in open (monitor-transitioning) mode

```text
ACCESS-01(config)# interface GigabitEthernet1/0/1
ACCESS-01(config-if)# switchport mode access
ACCESS-01(config-if)# switchport access vlan 10
ACCESS-01(config-if)# switchport voice vlan 20
ACCESS-01(config-if)# authentication host-mode multi-domain
ACCESS-01(config-if)# authentication open
ACCESS-01(config-if)# authentication order dot1x mab
ACCESS-01(config-if)# authentication priority dot1x mab
ACCESS-01(config-if)# authentication port-control auto
ACCESS-01(config-if)# mab
ACCESS-01(config-if)# dot1x pae authenticator
ACCESS-01(config-if)# dot1x timeout tx-period 5
ACCESS-01(config-if)# spanning-tree portfast edge
```

`authentication order dot1x mab` tries 802.1X first and falls back to MAB
only if no EAPoL response arrives; `authentication open` keeps this port
in open/low-impact mode. Removing that single line (and confirming
monitor-mode logs show clean results first) is the entire mechanism for
moving a port from open to closed mode.

### Static SGT and SGACL policy

```text
DIST-01(config)# cts role-based enforcement
DIST-01(config)# cts role-based sgt-map vlan-list 30 sgt 20
DIST-01(config)# cts sxp enable
DIST-01(config)# cts sxp default password 0 <STRONG_SXP_PASSWORD>
DIST-01(config)# cts sxp connection peer 10.10.99.30 source 10.10.99.2 password default mode local speaker
```

The SGACL matrix itself (which SGT pairs are permitted/denied, and which
ACL applies) is centrally authored in ISE's TrustSec policy matrix and
pushed to enforcing devices; the CLI above only establishes the local
enforcement point and SXP propagation. Dynamically assigned SGTs (from
802.1X/MAB authorization) require no local `sgt-map` configuration at
all — ISE returns the SGT as part of the RADIUS Access-Accept.

### RADIUS Change of Authorization (CoA)

```text
DIST-01(config)# aaa server radius dynamic-author
DIST-01(config-locsvr-da-radius)# client 10.10.99.21 server-key 0 <STRONG_RADIUS_KEY>
DIST-01(config-locsvr-da-radius)# port 1700
```

This allows ISE to push a CoA (for example, re-authenticate, or move a
session to a quarantine SGT/dACL) to an already-authenticated session
without waiting for the endpoint's own re-authentication timer.

## Validation and Troubleshooting

```text
DIST-01# show aaa servers
DIST-01# test aaa group ISE-ADMIN netadmin <PASSWORD> legacy
ACCESS-01# show authentication sessions
ACCESS-01# show authentication sessions interface GigabitEthernet1/0/1 details
ACCESS-01# show dot1x all
ACCESS-01# show mab all
DIST-01# show cts role-based sgt-map all
DIST-01# show cts sxp connections
DIST-01# show cts role-based permissions
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| CLI login fails even with correct credentials | TACACS+ server unreachable and local fallback account doesn't exist/mismatched password | `show aaa servers`, `test aaa group`, confirm a local emergency account is configured |
| Endpoint stuck in `AUTHENTICATING` indefinitely | RADIUS server unreachable, shared secret mismatch, or EAP type not supported by ISE policy | `show authentication sessions interface <intf> details`, `show aaa servers`, confirm shared key matches on both switch and ISE |
| Device that should MAB never gets network access | `authentication order` doesn't include `mab`, or `mab` not enabled on the interface | `show mab all`, confirm `authentication order`/`authentication priority` includes MAB and interface has `mab` configured |
| Session authenticates but wrong VLAN/dACL applied | ISE authorization policy rule matching an unintended condition, or dACL name mismatch between ISE and switch expectations | `show authentication sessions interface <intf> details`, cross-check the ISE live log for the same session |
| SGT not applied to dynamically authenticated session | RADIUS Access-Accept missing the SGT attribute (ISE authorization profile not configured to return one) | `show authentication sessions interface <intf> details` (look for `Security Group Tag`), verify the ISE authorization profile |
| SXP peer never reaches `On` state | SXP password mismatch, or TCP 64999/reachability issue between peers | `show cts sxp connections`, confirm password and IP reachability between the two SXP peers |

## Security and Best Practices

- Never leave a production access port in open mode indefinitely; open
  mode is a rollout stage, and every port should have a target date to
  reach closed mode once monitor-mode data confirms readiness.
- Configure a distinct **critical-authentication VLAN**
  (`authentication event server dead action authorize vlan <id>`) so
  endpoints have a defined, restricted fallback path if every RADIUS
  server becomes unreachable, instead of either full lockout or an
  undocumented full-access fallback.
- Rotate TACACS+/RADIUS shared secrets on a defined schedule and store
  them in a managed secrets store rather than plaintext configuration
  backups ([Volume IX](../../volume-09-infrastructure-automation/README.md)).
- Use per-command TACACS+ authorization for privilege-15 administrators
  where regulatory or change-control requirements justify the additional
  policy maintenance; at minimum, separate read-only (privilege 1–14) from
  full-admin (privilege 15) roles.
- Prefer EAP-TLS (certificate-based) 802.1X over PEAP/MSCHAPv2 for
  managed corporate endpoints wherever a certificate deployment pipeline
  ([Volume IV](../../volume-04-enterprise-systems-administration/README.md), [Volume IX](../../volume-09-infrastructure-automation/README.md)) exists; certificate-based authentication removes
  password-based credential theft as a network-access attack vector.
- Treat the SGACL matrix as a change-controlled artifact, not an
  ad hoc set of rules; because SGACL policy applies wherever an SGT
  appears, an overly permissive matrix entry has network-wide
  consequences, unlike a single mis-scoped VLAN ACL.
- Enable RADIUS CoA (`aaa server radius dynamic-author`) so ISE can
  actively quarantine a session in response to a posture, threat, or
  policy change, rather than only reactively at the endpoint's own
  re-authentication interval.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Identity Services Engine Administrator Guide*, current release.
- Cisco, *TrustSec Configuration Guide* for IOS XE Catalyst 9000 switches.
- IEEE 802.1X-2020, *Port-Based Network Access Control*.
- [RFC 2865](https://www.rfc-editor.org/rfc/rfc2865)/2866 (RADIUS), [RFC 8907](https://www.rfc-editor.org/rfc/rfc8907) (TACACS+ protocol specification).

**Knowledge checks**

1. Why do most Cisco designs use TACACS+ for device administration and
   RADIUS for network access, rather than one protocol for both?
2. What problem does MAB solve, and why should its use still be limited
   and profiled rather than applied broadly?
3. Describe the progression from monitor mode to open mode to closed mode
   and why a rollout follows that order.
4. How does SGACL micro-segmentation differ operationally from writing
   IP-address-based ACLs at every enforcement point?
5. What is the functional difference between inline SGT tagging and SXP?

## Hands-On Lab

**Objective:** Deploy 802.1X with MAB fallback on an access port in open
mode, confirm authorization results (VLAN/dACL) from a RADIUS/ISE policy
server, and validate CLI administrator access uses TACACS+.

**Prerequisites**

- The access/distribution topology from [Chapter 2](02-catalyst-campus-switching-and-resiliency.md)'s lab (or equivalent
  CML topology).
- A RADIUS/TACACS+-capable AAA server or ISE instance (physical, virtual,
  or the ISE Personal Developer VM) reachable from the lab switches, with
  a test user account and a device-authorization policy configured.
- One 802.1X-capable test client and one non-802.1X device (or a device
  simulator) for the MAB path.

**Procedure**

1. Configure `aaa new-model`, the TACACS+ server/group, and the
   authentication/authorization/accounting method lists for device
   administration as shown in Implementation.

2. Confirm CLI login now authenticates via TACACS+:

   ```text
   DIST-01# show aaa servers
   ```

   **Expected result:** the TACACS+ server shows request/response
   counters incrementing after a fresh SSH login attempt.

3. Configure the RADIUS server/group and enable `dot1x
   system-auth-control` globally, then apply the open-mode 802.1X/MAB
   interface configuration from Implementation to a test access port.

4. Connect the 802.1X-capable test client and confirm it authenticates:

   ```text
   ACCESS-01# show authentication sessions interface GigabitEthernet1/0/1 details
   ```

   **Expected result:** the session shows `Authc Success`, method
   `dot1x`, and the VLAN/dACL returned by the policy server.

5. Connect the non-802.1X device (or simulator) to a second port
   configured identically, and confirm it falls back to MAB:

   ```text
   ACCESS-01# show authentication sessions interface GigabitEthernet1/0/2 details
   ```

   **Expected result:** the session shows `Authc Success`, method `mab`,
   after the configured `dot1x timeout tx-period` elapses with no EAPoL
   response.

6. **Negative test:** disconnect the RADIUS server (shut down the server
   interface, or remove IP reachability in the lab) and attempt a new
   client authentication on a third, identically configured port.

   ```text
   ACCESS-01# show authentication sessions interface GigabitEthernet1/0/3 details
   ACCESS-01# show aaa servers
   ```

   **Expected result:** `show aaa servers` shows the RADIUS server as
   dead, and the new session either falls into the critical-authentication
   VLAN (if configured) or remains unauthenticated per the port's
   `authentication event server dead action` policy — confirming the
   fallback behaves as designed rather than silently granting full
   access.

7. Restore RADIUS reachability and confirm normal authentication resumes.

**Cleanup**

- Remove the lab-only 802.1X/MAB interface configuration if the switch is
  shared:

  ```text
  ACCESS-01(config)# interface range GigabitEthernet1/0/1-3
  ACCESS-01(config-if-range)# no authentication port-control auto
  ACCESS-01(config-if-range)# no mab
  ACCESS-01(config-if-range)# no dot1x pae authenticator
  ```

- Clear any test sessions:

  ```text
  ACCESS-01# clear authentication sessions interface GigabitEthernet1/0/1
  ```

## Summary and Completion Checklist

Identity-based access control replaces static, address-based trust with
policy evaluated at connection time: TACACS+ governs who can administer
the device itself, while 802.1X and MAB (backed by RADIUS/ISE) govern
what an endpoint can do once connected — down to a dynamic VLAN, dACL, or
Security Group Tag. TrustSec's SGT/SGACL model then lets that identity
follow the endpoint for micro-segmentation, complementing the VRF-lite
macro-segmentation introduced in [Chapter 3](03-cisco-enterprise-routing-and-path-control.md) without requiring an
IP-address-based ACL at every enforcement point.

- [ ] Can configure TACACS+ device administration with a local fallback.
- [ ] Can configure 802.1X with MAB fallback and explain the monitor/open/
      closed mode progression.
- [ ] Can explain ISE's PAN/PSN/MnT roles and what an authorization policy
      can return to the switch.
- [ ] Can explain SGT/SGACL micro-segmentation and the difference between
      inline tagging and SXP.
- [ ] Completed the hands-on lab, including the RADIUS-server-down
      negative test and cleanup.
