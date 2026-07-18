# Chapter 05: Catalyst Wireless Architecture and Operations

## Learning Objectives

- Explain the split-MAC CAPWAP architecture and the role of the Catalyst
  9800 Wireless Controller in current Cisco enterprise wireless designs.
- Compare Catalyst 9800 deployment models (appliance, embedded wireless on
  a Catalyst 9000 switch, and cloud-hosted) and the access point modes
  available in each.
- Describe RF fundamentals — bands, channel width, and Radio Resource
  Management (RRM) — well enough to reason about a site's design.
- Configure a WLAN, policy profile, and the site/policy/RF tag model used
  to join an access point on IOS XE wireless.
- Explain 802.11r/k/v fast-roaming mechanisms and WPA3 authentication
  options.
- Validate AP join state and client association, and diagnose the most
  common join and authentication failures.

## Theory and Architecture

### Split-MAC CAPWAP architecture

Cisco enterprise wireless separates access point functions into two
cooperating roles connected by the **Control and Provisioning of Wireless
Access Points (CAPWAP)** protocol (RFC 5415):

- **Access points (APs)** in the default local mode handle only the
  time-sensitive, per-packet 802.11 MAC functions — beaconing, probe
  response, and encryption/decryption of the wireless frame — before
  forwarding client traffic.
- **The Wireless LAN Controller (WLC)** owns everything else: association
  and authentication state, mobility (roaming) management, RF Resource
  Management (RRM), and the WLAN/policy configuration that every joined AP
  receives.

CAPWAP tunnels carry two logically separate streams between an AP and its
WLC: a **control tunnel** (encrypted with DTLS by default, carrying join,
configuration, and management traffic) and a **data tunnel** (client
traffic, optionally DTLS-encrypted). This split-MAC model is what lets a
single WLC centrally manage RF behavior, security policy, and roaming
across hundreds of APs without each AP needing local policy configuration.

### Catalyst 9800 deployment models

Cisco's current-generation WLC, the **Catalyst 9800**, runs IOS XE rather
than the legacy AireOS used on older controllers — which means it shares
the same install-mode packaging, Smart Licensing Using Policy, NETCONF/
RESTCONF programmability (Chapter 8), and high-availability constructs as
the rest of the Catalyst 9000 family covered in this volume. Three
deployment models cover most enterprise designs:

| Model | Platform | Typical fit |
| --- | --- | --- |
| Appliance | Catalyst 9800-40, 9800-80, 9800-L | Dedicated on-premises controller for campus or large branch scale |
| Embedded Wireless Controller (EWC) | Catalyst 9800 software running on a Catalyst 9300/9400 switch | Small/medium campus or branch that wants to avoid a standalone appliance |
| Cloud-delivered | Catalyst 9800-CL (virtual, private cloud or Cisco-hosted) | Data-center-hosted or cloud-hosted control plane, including Meraki-style cloud management via Catalyst Center Cloud Monitoring |

Regardless of model, the controller terminates CAPWAP from every joined AP
and applies the same WLAN/policy configuration model described below.

### Access point modes

An AP's mode determines what role it plays once joined:

| Mode | Function |
| --- | --- |
| Local | Default mode; serves WLANs and forwards client data normally |
| FlexConnect | Switches client traffic locally at the branch instead of tunneling it back to the WLC over the WAN; can still tunnel select WLANs centrally |
| Monitor | Radios dedicated to RF scanning — rogue detection, location, and spectrum data — with no client service |
| Sniffer | Captures 802.11 frames on a channel and forwards them to a packet analyzer (Volume XX) |
| Rogue Detector | Wired-side only; correlates rogue AP MAC addresses seen over the air with MAC addresses learned on the wired network |
| Bridge / Flex+Bridge | Forms a wireless mesh backhaul (Cisco Adaptive Wireless Path Protocol) between APs where a wired uplink to every AP is impractical |
| SE-Connect | Dedicates the AP as a spectrum analyzer client for Cisco Spectrum Expert |

FlexConnect is the standard choice for branch sites reachable only over a
WAN link (Chapter 4): APs continue to serve clients locally even if
connectivity to the central WLC is lost, and only rejoin/reconfiguration
traffic depends on the WAN path being up.

### RF fundamentals

Enterprise Wi-Fi in the current Catalyst portfolio operates across three
bands, each with distinct trade-offs:

- **2.4 GHz** — longest range and best wall penetration, but only three
  non-overlapping 20 MHz channels (1/6/11) in most regulatory domains and
  heavy contention from legacy and non-Wi-Fi devices (Bluetooth,
  microwave ovens). Increasingly reserved for IoT and legacy clients only.
- **5 GHz** — far more non-overlapping channels and higher throughput per
  channel width (20/40/80/160 MHz), the primary band for client
  performance in most current designs.
- **6 GHz (Wi-Fi 6E / Wi-Fi 7)** — an entirely new, far less congested
  band with no legacy device compatibility burden, gated to WPA3-only
  security by the Wi-Fi Alliance specification (no WEP/WPA2 fallback is
  permitted).

**Radio Resource Management (RRM)** runs on the WLC and continuously
tunes three RF variables across every joined AP so that a design does not
need static, per-AP channel/power planning:

- **Dynamic Channel Assignment (DCA)** — selects each AP's channel to
  minimize co-channel and adjacent-channel interference.
- **Transmit Power Control (TPC)** — adjusts each AP's transmit power to
  balance coverage against cell overlap.
- **Coverage Hole Detection and Mitigation (CHDM)** — raises power on APs
  neighboring a detected low-SNR coverage hole.

**CleanAir**-capable APs additionally classify non-Wi-Fi RF interference
sources (microwave ovens, Bluetooth, DECT phones, video bridges) and feed
that data into RRM and Assurance (Chapter 9) so that interference is
visible and, where possible, automatically avoided.

### Fast roaming: 802.11r, 802.11k, and 802.11v

A client roaming between APs re-authenticates against every new AP unless
a fast-roaming mechanism is enabled — full 802.1X/EAP re-authentication on
every roam is disruptive enough to break real-time applications such as
voice:

- **802.11r (Fast BSS Transition)** — caches key material derived from the
  original authentication so a roam only requires a four-way handshake
  with the new AP, not a full EAP exchange.
- **802.11k (Radio Resource Management)** — lets a client request a
  neighbor report from its current AP so it can evaluate roam candidates
  without scanning every channel blind.
- **802.11v (BSS Transition Management)** — lets the infrastructure
  suggest (or, in some deployments, direct) a client to a better AP based
  on RF conditions the client cannot see itself.

All three are independent, additive, and configured per WLAN; a WLAN
serving latency-sensitive voice/video traffic should enable all three
where client support allows.

## Design Considerations

- **Controller placement and sizing** — size the Catalyst 9800 appliance
  or EWC platform against expected AP count and client count headroom, not
  just current AP count; controller replacement/upgrade is far more
  disruptive than adding APs to headroom already provisioned.
- **Local vs. FlexConnect** — use local mode where the WLC is reachable
  over low-latency, high-bandwidth campus links; use FlexConnect for any
  site whose WLC reachability depends on a WAN path that can legitimately
  fail or degrade (Chapter 4), so clients keep working during a WAN
  outage.
- **Band and SSID strategy** — prefer a small number of SSIDs (typically
  one per major traffic class: corporate/802.1X, guest, IoT) rather than
  one SSID per department, since every additional SSID adds airtime
  overhead from beacon frames on every AP radio.
- **6 GHz rollout** — plan 6 GHz as an additive, WPA3-only band alongside
  2.4/5 GHz rather than a replacement, since many existing client devices
  do not support 6 GHz at all.
- **High availability** — pair Catalyst 9800 appliances in an N+1 (AP
  primary/secondary/tertiary controller assignment, stateless failover) or
  SSO (Stateful Switchover over a dedicated redundancy port, near-zero
  client impact) configuration depending on whether the design can
  tolerate APs re-joining a backup controller after a primary failure.
- **RRM tuning scope** — let RRM run in its default automatic mode for
  channel and power in the overwhelming majority of designs; only
  override to static channel/power on a specific AP when a documented,
  measured RF problem (not a guess) justifies the exception, since manual
  overrides silently opt that AP out of ongoing RRM optimization.
- **Site survey requirement** — do not size AP count and placement from a
  coverage-only estimate for any design with meaningful client density
  (open-plan offices, auditoriums, warehouses); commission a predictive
  and, for high-density sites, an active on-site survey.

## Implementation and Automation

### Wireless management interface and AP join basics

```text
WLC-01(config)# wireless management interface Vlan100
WLC-01(config)# ap dot1x-user-name lab-ap-user password 0 <STRONG_AP_PASSWORD>
```

The AP dot1x credentials above are only required if 802.1X port
authentication is enforced on the switchport an AP connects to
(Chapter 7); most designs instead rely on the AP's certificate-based
CAPWAP join process without per-port 802.1X.

### AP join profile, RF profile, and tags

```text
WLC-01(config)# ap profile CAMPUS-AP-PROFILE
WLC-01(config-ap-profile)# mgmtuser username netadmin password 0 <STRONG_PASSWORD> secret 0 <STRONG_SECRET>
WLC-01(config-ap-profile)# exit

WLC-01(config)# ap dot11 5ghz rf-profile CAMPUS-5GHZ-RF
WLC-01(config-rf-profile)# description "Campus 5 GHz RRM profile"
WLC-01(config-rf-profile)# exit

WLC-01(config)# wireless tag rf CAMPUS-RF-TAG
WLC-01(config-rf-tag)# 5ghz-rf-policy CAMPUS-5GHZ-RF
WLC-01(config-rf-tag)# 24ghz-rf-policy default-rf-policy
WLC-01(config-rf-tag)# exit

WLC-01(config)# wireless tag site CAMPUS-SITE-TAG
WLC-01(config-site-tag)# ap-join-profile CAMPUS-AP-PROFILE
WLC-01(config-site-tag)# exit
```

### WLAN and policy profile

```text
WLC-01(config)# wlan CORP-WLAN 1 CORP-SSID
WLC-01(config-wlan)# security wpa akm dot1x
WLC-01(config-wlan)# security wpa wpa2 ciphers aes
WLC-01(config-wlan)# security dot1x authentication-list default
WLC-01(config-wlan)# no shutdown
WLC-01(config-wlan)# exit

WLC-01(config)# wireless profile policy CORP-POLICY
WLC-01(config-wireless-policy)# vlan 20
WLC-01(config-wireless-policy)# no shutdown
WLC-01(config-wireless-policy)# exit

WLC-01(config)# wireless tag policy CORP-POLICY-TAG
WLC-01(config-policy-tag)# wlan CORP-WLAN policy CORP-POLICY
WLC-01(config-policy-tag)# exit
```

`vlan 20` in the policy profile is the client VLAN — the same VLAN 20
(`VOICE`/user VLAN family) introduced in Chapter 2; the WLC bridges
wireless clients into the existing VLAN structure rather than requiring a
separate wireless-only VLAN plan.

### WPA3 with SAE

```text
WLC-01(config)# wlan SECURE-WLAN 2 SECURE-SSID
WLC-01(config-wlan)# security wpa akm sae
WLC-01(config-wlan)# security wpa wpa3
WLC-01(config-wlan)# no security wpa wpa2 ciphers aes
WLC-01(config-wlan)# no shutdown
```

### Fast roaming

```text
WLC-01(config)# wlan CORP-WLAN
WLC-01(config-wlan)# security ft over-the-ds
WLC-01(config-wlan)# neighbor-list
WLC-01(config-wlan)# exit
```

`security ft over-the-ds` enables 802.11r using the over-the-DS transition
mechanism (broadest client compatibility); `neighbor-list` enables 802.11k
neighbor reports. 802.11v BSS Transition Management is enabled per WLAN
with `bss-transition` under the same `config-wlan` submode on platforms
where client compatibility has been validated.

### Assigning tags to an AP

```text
WLC-01(config)# ap F4CF.E2XX.0001
WLC-01(config-ap-tag)# policy-tag CORP-POLICY-TAG
WLC-01(config-ap-tag)# site-tag CAMPUS-SITE-TAG
WLC-01(config-ap-tag)# rf-tag CAMPUS-RF-TAG
WLC-01(config-ap-tag)# exit
```

Tags can also be pre-staged before an AP ever joins (by MAC address) so
that a newly cabled AP receives its full configuration automatically on
first join — the wireless equivalent of the day-0 provisioning pattern
introduced in Chapter 1.

### FlexConnect for a branch site

```text
WLC-01(config)# wireless profile flex BRANCH-FLEX-PROFILE
WLC-01(config-wireless-flex-profile)# acl-policy BRANCH-LOCAL-ACL
WLC-01(config-wireless-flex-profile)# exit
WLC-01(config)# ap profile BRANCH-AP-PROFILE
WLC-01(config-ap-profile)# exit
WLC-01(config)# wireless tag site BRANCH-SITE-TAG
WLC-01(config-site-tag)# ap-join-profile BRANCH-AP-PROFILE
WLC-01(config-site-tag)# flex-profile BRANCH-FLEX-PROFILE
WLC-01(config-site-tag)# no local-site
WLC-01(config-site-tag)# exit
```

`no local-site` is what marks this a remote (FlexConnect) site instead of
a local-mode site — every AP tagged with `BRANCH-SITE-TAG` switches
client traffic locally at the branch rather than tunneling it to
`WLC-01`.

## Validation and Troubleshooting

```text
WLC-01# show ap summary
WLC-01# show ap name AP-CAMPUS-01 config general
WLC-01# show wlan summary
WLC-01# show wireless tag policy summary
WLC-01# show wireless client summary
WLC-01# show wireless client mac-address <CLIENT_MAC> detail
WLC-01# show ap dot11 5ghz summary
WLC-01# show ap rf-profile summary
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| AP never appears in `show ap summary` | CAPWAP discovery failure (DHCP option 43/DNS `CISCO-CAPWAP-CONTROLLER` not resolving, or an ACL blocking UDP 5246/5247) | Confirm AP obtained an IP and can resolve/reach the WLC; check DHCP option 43 or the discovery DNS record |
| AP joins then immediately reboots/rejoins in a loop | Certificate validation failure or a software image mismatch between AP and controller | `show ap join-stats summary`, check for a Predownload mismatch requiring an AP image update |
| Client associates but never gets an IP address | Client VLAN in the policy profile not trunked to the AP's switchport, or DHCP relay/scope missing for that VLAN | `show wireless client mac-address <MAC> detail`, verify VLAN and confirm DHCP relay/scope on that VLAN |
| Client authentication fails immediately on an 802.1X WLAN | RADIUS server unreachable, shared secret mismatch, or `authentication-list` pointing at the wrong AAA method list | `show wireless client mac-address <MAC> detail`, `test aaa group <group> <user> <pass> legacy` (Chapter 7) |
| Clients roam but experience a voice/video glitch on every roam | 802.11r/k/v not enabled, or client driver doesn't support fast transition | `show wlan id <id>` to confirm `11r`/`neighbor-list` status; confirm client capability |
| Coverage hole reported repeatedly in the same area | Genuine RF coverage gap, or an AP administratively down/offline | `show ap summary` for AP state, review CleanAir/interference data before assuming it's a coverage design issue |

## Security and Best Practices

- Use WPA3 (SAE, or WPA3-Enterprise with 192-bit security for
  high-assurance environments) on every new SSID; retain WPA2 only where a
  documented legacy client population requires it, and plan its removal.
- Enable **Protected Management Frames (PMF/802.11w)** wherever client
  support allows — required outright by WPA3 — to prevent deauthentication
  and disassociation spoofing attacks against associated clients.
- Never rely on a hidden SSID or MAC filtering as a security control; both
  are trivially bypassed and only add operational friction for legitimate
  clients.
- Segment guest traffic onto its own WLAN, VLAN, and (if the design uses
  it) a dedicated DMZ/anchor path, never bridged onto the same VLAN as
  corporate wired or wireless traffic.
- Run Rogue Detector-mode APs (or rely on Monitor-mode/CleanAir scanning
  from local-mode APs) and review rogue reports in Assurance (Chapter 9)
  rather than treating rogue detection as a set-and-forget feature.
- Terminate CAPWAP control traffic with DTLS (the default) and do not
  disable it; disabling DTLS exposes AP-to-WLC control traffic, including
  configuration pushes, in cleartext.
- Apply the same AAA hardening from Chapter 1 (dedicated management
  credentials, no shared accounts) to the WLC itself, since a compromised
  WLC compromises every WLAN it serves.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Catalyst 9800 Series Wireless Controller Software Configuration
  Guide*, IOS XE 17.x.
- Cisco, *Enterprise Mobility Design Guide*.
- IEEE 802.11-2020 and amendments 802.11r, 802.11k, 802.11v.
- RFC 5415, *Control and Provisioning of Wireless Access Points (CAPWAP)
  Protocol Specification*.

**Knowledge checks**

1. What functions remain on the AP versus the WLC in the split-MAC CAPWAP
   model?
2. When should a site use FlexConnect mode instead of local mode, and what
   changes for clients if the WAN link to the WLC fails?
3. Name the three RRM functions and what each one optimizes.
4. What problem does 802.11r solve, and what are 802.11k and 802.11v each
   responsible for?
5. Why does the Wi-Fi Alliance require WPA3-only security on the 6 GHz
   band?

## Hands-On Lab

**Objective:** Bring up a Catalyst 9800 WLC (or CML/virtual 9800-CL node),
join an access point, build an 802.1X-secured WLAN with fast roaming
enabled, and validate client association.

**Prerequisites**

- One Catalyst 9800 controller (appliance, EWC, or 9800-CL virtual node)
  and at least one compatible Catalyst access point, or an equivalent CML
  topology with a 9800-CL controller node.
- Reachable DHCP scope for the AP's subnet with option 43 (or a DNS
  `CISCO-CAPWAP-CONTROLLER` record) pointing APs at the WLC.
- A RADIUS server (or the local AAA fallback introduced in Chapter 7) for
  802.1X authentication, plus a test client capable of WPA2/WPA3-Enterprise.

**Procedure**

1. Configure the wireless management interface and confirm the controller
   is reachable:

   ```text
   WLC-01(config)# wireless management interface Vlan100
   WLC-01# show wireless management interface
   ```

2. Create the AP join profile, RF tag, and site tag, then confirm the AP
   receives an address and appears as joined:

   ```text
   WLC-01# show ap summary
   ```

   **Expected result:** the AP shows `Country`, `IP Address`, and a
   `State` of `Registered` (or `Joined`).

3. Build `CORP-WLAN`, `CORP-POLICY`, and `CORP-POLICY-TAG` as shown in
   Implementation, and apply the policy tag to the joined AP.

4. Verify the WLAN is broadcast and the AP has the expected tags:

   ```text
   WLC-01# show wlan summary
   WLC-01# show ap name <AP_NAME> tag detail
   ```

   **Expected result:** `CORP-WLAN` shows `Enabled`, and the AP's tag
   detail output shows `CORP-POLICY-TAG`/`CAMPUS-SITE-TAG`/
   `CAMPUS-RF-TAG`.

5. From the test client, associate to `CORP-SSID`, authenticate with valid
   802.1X credentials, and confirm the client received an address on
   VLAN 20:

   ```text
   WLC-01# show wireless client summary
   WLC-01# show wireless client mac-address <CLIENT_MAC> detail
   ```

   **Expected result:** the client shows `State: Run` and the correct
   VLAN and IP address.

6. **Negative test:** attempt to associate a second test client using an
   intentionally wrong 802.1X password.

   ```text
   WLC-01# show wireless client summary
   WLC-01# show logging | include 802.1X|dot1x
   ```

   **Expected result:** the client does not reach `Run` state, and a
   failed-authentication event is logged, confirming invalid credentials
   are rejected rather than silently admitted.

**Cleanup**

- Remove the test WLAN, policy profile, and policy tag if this is a
  shared lab controller:

  ```text
  WLC-01(config)# no wlan CORP-WLAN
  WLC-01(config)# no wireless profile policy CORP-POLICY
  WLC-01(config)# no wireless tag policy CORP-POLICY-TAG
  ```

- Reset the AP's tags to the controller's default tags before returning it
  to a shared pool.

## Summary and Completion Checklist

Catalyst wireless design centers on the split-MAC CAPWAP relationship
between lightweight APs and a Catalyst 9800 controller: the controller
owns policy, RRM, and mobility state, while the AP handles only real-time
802.11 MAC processing. The site/policy/RF tag model is how that policy is
assigned to physical APs at scale, and WPA3, 802.11w, and 802.11r/k/v are
the current security and roaming baseline for any new WLAN design.

- [ ] Can explain the split-MAC CAPWAP architecture and AP mode options.
- [ ] Can compare Catalyst 9800 appliance, EWC, and cloud-hosted
      deployment models.
- [ ] Can configure a WLAN, policy profile, and site/policy/RF tags to
      join an AP and serve clients.
- [ ] Can explain 802.11r/k/v roaming and WPA3/PMF security options.
- [ ] Completed the hands-on lab, including the failed-authentication
      negative test and cleanup.
