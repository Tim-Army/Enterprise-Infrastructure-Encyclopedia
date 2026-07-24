# Chapter 05: Catalyst Wireless Architecture and Operations

![Lab topology for this chapter: WLC-01's wireless management interface is on Vlan100; an access point joins the controller and shows State Registered, tagged with CORP-POLICY-TAG/CAMPUS-SITE-TAG/CAMPUS-RF-TAG; CORP-WLAN (802.1X, CORP-POLICY) is applied to the AP, and a test client associates, authenticates against the RADIUS/ISE server, and lands on VLAN 20 in State: Run. As a negative test, a second client using an intentionally wrong 802.1X password never reaches Run state, and a failed-authentication event is logged.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-05-catalyst-9800-wlc-8021x-topology.svg)

*Figure 5-1. Topology used throughout this chapter's Hands-On Lab: a Catalyst 9800 WLC joining an access point and authenticating a client against an 802.1X WLAN backed by RADIUS/ISE.*

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
Access Points (CAPWAP)** protocol ([RFC 5415](https://www.rfc-editor.org/rfc/rfc5415)):

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
RESTCONF programmability ([Chapter 8](08-ios-xe-programmability-and-network-automation.md)), and high-availability constructs as
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
| Sniffer | Captures 802.11 frames on a channel and forwards them to a packet analyzer ([Volume XX](../../volume-20-wireshark-packet-analysis/README.md)) |
| Rogue Detector | Wired-side only; correlates rogue AP MAC addresses seen over the air with MAC addresses learned on the wired network |
| Bridge / Flex+Bridge | Forms a wireless mesh backhaul (Cisco Adaptive Wireless Path Protocol) between APs where a wired uplink to every AP is impractical |
| SE-Connect | Dedicates the AP as a spectrum analyzer client for Cisco Spectrum Expert |

FlexConnect is the standard choice for branch sites reachable only over a
WAN link ([Chapter 4](04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md)): APs continue to serve clients locally even if
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
that data into RRM and Assurance ([Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md)) so that interference is
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
  fail or degrade ([Chapter 4](04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md)), so clients keep working during a WAN
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
([Chapter 7](07-cisco-identity-access-control-and-segmentation.md)); most designs instead rely on the AP's certificate-based
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
(`VOICE`/user VLAN family) introduced in [Chapter 2](02-catalyst-campus-switching-and-resiliency.md); the WLC bridges
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
introduced in [Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md).

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
| Client authentication fails immediately on an 802.1X WLAN | RADIUS server unreachable, shared secret mismatch, or `authentication-list` pointing at the wrong AAA method list | `show wireless client mac-address <MAC> detail`, `test aaa group <group> <user> <pass> legacy` ([Chapter 7](07-cisco-identity-access-control-and-segmentation.md)) |
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
  from local-mode APs) and review rogue reports in Assurance ([Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md))
  rather than treating rogue detection as a set-and-forget feature.
- Terminate CAPWAP control traffic with DTLS (the default) and do not
  disable it; disabling DTLS exposes AP-to-WLC control traffic, including
  configuration pushes, in cleartext.
- Apply the same AAA hardening from [Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md) (dedicated management
  credentials, no shared accounts) to the WLC itself, since a compromised
  WLC compromises every WLAN it serves.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Catalyst 9800 Series Wireless Controller Software Configuration
  Guide*, IOS XE 17.x.
- Cisco, *Enterprise Mobility Design Guide*.
- IEEE 802.11-2020 and amendments 802.11r, 802.11k, 802.11v.
- [RFC 5415](https://www.rfc-editor.org/rfc/rfc5415), *Control and Provisioning of Wireless Access Points (CAPWAP)
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

This chapter carries a topic-level walkthrough lab for the wireless exam
topics that map here — the **CCNA Domain 2/5 wireless items** and **all of
ENWLSI (300-430 Wireless Implementation)** — mapped in the volume README's
coverage tables; the design exam **ENWLSD (300-425)** is covered by the
Design Exercise below. Each lab is a Catalyst 9800 (IOS XE) walkthrough and
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.35** — a Catalyst 9800/9800-CL WLC, a
joined AP, an ISE/RADIUS server and CMX/Cisco Spaces where noted, privileged
EXEC access. **Cost:** none beyond lab resources; each lab removes its
config.

### Lab 5.1 — Describe wireless principles (CCNA 1.11)

**Objective:** Read the RF/channel plan the AP advertises.

```text
WLC# show ap dot11 5ghz summary
WLC# show ap dot11 24ghz summary
```

**Expected result:** per-AP channel, channel width, and tx power — the RF
fundamentals (channels, non-overlapping 2.4 GHz, DFS on 5 GHz).

**Negative test:** two nearby APs on the same 2.4 GHz channel co-channel
interfere; the principle is why RRM assigns non-overlapping channels.

**Cleanup:** none (read-only).

### Lab 5.2 — Describe wireless architectures and AP modes (CCNA 2.6)

**Objective:** Read AP mode (local, FlexConnect, monitor, sniffer).

```text
WLC# show ap summary
WLC# show ap name AP1 config general | include AP Mode
```

**Expected result:** each AP's mode — local (centrally switched via the WLC)
vs FlexConnect (locally switched at the branch), the two dominant models.

**Negative test:** expecting local-mode APs to keep serving clients if the
WLC/WAN is down; they cannot — that is FlexConnect's job.

**Cleanup:** none (read-only).

### Lab 5.3 — Describe WLAN physical connections (CCNA 2.7)

**Objective:** Confirm the AP's uplink and PoE.

```text
WLC# show ap name AP1 config general | include Ethernet|POE
WLC# show wireless stats ap join summary
```

**Expected result:** the AP's switchport, PoE draw, and a successful CAPWAP
join — the physical connection between AP, switch, and WLC.

**Negative test:** an AP on a switchport delivering insufficient PoE runs in
reduced mode (radios disabled); check the power budget.

**Cleanup:** none (read-only).

### Lab 5.4 — Interpret the wireless LAN GUI configuration (CCNA 2.9)

**Objective:** Read a WLAN/policy profile the GUI builds.

```text
WLC# show wlan summary
WLC# show wlan id 1
```

**Expected result:** the WLAN's SSID, security, and policy-profile binding —
the config the Web UI's WLAN wizard produces.

**Negative test:** a WLAN with no policy profile mapped to a policy tag never
broadcasts; the 9800's tag model requires the binding.

**Cleanup:** none (read-only).

### Lab 5.5 — Describe wireless security protocols (CCNA 5.9)

**Objective:** Read the WLAN's Layer 2 security (WPA2/WPA3).

```text
WLC# show wlan id 1 | include Security|WPA|AKM
```

**Expected result:** the security type (WPA2-Enterprise, WPA3-SAE) and AKM —
the protocol protecting the air.

**Negative test:** an open or WEP WLAN is trivially intercepted; WPA2/WPA3 is
the baseline.

**Cleanup:** none (read-only).

### Lab 5.6 — Configure a WLAN with WPA2 PSK (CCNA 5.10)

**Objective:** Build a PSK WLAN on the 9800.

```text
WLC(config)# wlan LAB-PSK 2 LAB-PSK
WLC(config-wlan)# security wpa psk set-key ascii 0 <passphrase>
WLC(config-wlan)# no shutdown
WLC# show wlan name LAB-PSK
```

**Expected result:** the WLAN active with WPA2-PSK; a client with the
passphrase associates.

**Negative test:** a PSK under 8 characters is rejected; WPA2-PSK enforces a
minimum key length.

**Cleanup:** `no wlan LAB-PSK`.

### Lab 5.7 — Deploy FlexConnect switching and operating modes (ENWLSI 1.1)

**Objective:** Put an AP in FlexConnect with local switching.

```text
WLC(config)# ap name AP1 mode flexconnect
WLC(config)# wireless profile flex FLEX-BR
WLC# show ap name AP1 config general | include AP Mode|Switching
```

**Expected result:** AP1 in FlexConnect mode with local switching — branch
traffic stays local instead of tunneling to the WLC.

**Negative test:** a locally switched WLAN with no local VLAN mapping drops
client traffic; the flex profile must map the SSID to a branch VLAN.

**Cleanup:** `ap name AP1 mode local`.

### Lab 5.8 — Deploy FlexConnect capabilities (ENWLSI 1.2)

**Objective:** Enable local authentication for WAN-down survivability.

```text
WLC(config)# wireless profile flex FLEX-BR
WLC(config-wireless-flex-profile)# local-auth ap-auth
WLC# show wireless profile flex detailed FLEX-BR
```

**Expected result:** FlexConnect local auth configured — clients keep
authenticating at the branch if the WLC/WAN is unreachable.

**Negative test:** central auth only; a WAN outage blocks all new
associations at the branch — local auth is the survivability feature.

**Cleanup:** remove local-auth from the flex profile.

### Lab 5.9 — Implement OfficeExtend (ENWLSI 1.3)

**Objective:** Configure an OEAP for a teleworker.

```text
WLC(config)# ap name AP-OE mode flexconnect
WLC(config)# ap name AP-OE flexconnect office-extend
WLC# show ap name AP-OE config general | include Office
```

**Expected result:** the AP in OfficeExtend mode — a DTLS-secured CAPWAP
tunnel from the home to the WLC, delivering corporate SSIDs remotely.

**Negative test:** an OEAP without the split-tunnel/local-split ACL sends all
home traffic over the tunnel; scope the split.

**Cleanup:** remove office-extend from the AP.

### Lab 5.10 — Implement wired-to-wireless QoS (ENWLSI 2.1)

**Objective:** Map wired DSCP to wireless UP end to end.

```text
WLC(config)# wireless profile policy POL-VOICE
WLC(config-wireless-policy)# service-policy input platinum-up
WLC# show wireless profile policy detailed POL-VOICE | include QoS
```

**Expected result:** a QoS policy mapping DSCP to 802.11 user priority —
voice keeps its marking across the wired/wireless boundary.

**Negative test:** trusting client-marked UP without a trust boundary lets a
client mark bulk as voice; mark/trust at the WLC.

**Cleanup:** remove the service-policy.

### Lab 5.11 — Implement QoS for wireless clients (ENWLSI 2.2)

**Objective:** Apply per-client rate limiting.

```text
WLC(config-wireless-policy)# service-policy client input rate-limit-5m
WLC# show wireless client mac-address <mac> detail | include Rate|QoS
```

**Expected result:** per-client bandwidth limits applied — fair-use control
on the WLAN.

**Negative test:** no per-client limit lets one client saturate the AP;
rate-limiting bounds it.

**Cleanup:** remove the client service-policy.

### Lab 5.12 — Implement AVC and Fastlane (ENWLSI 2.3)

**Objective:** Enable Application Visibility and Control on the policy
profile.

```text
WLC(config-wireless-policy)# ip flow monitor wireless-avc input
WLC# show avc wlan LAB-PSK application
```

**Expected result:** per-application flow visibility on the WLAN, and (with
Fastlane) Apple devices auto-marking priority apps — application-aware
wireless QoS.

**Negative test:** AVC without NBAR protocol packs cannot classify newer
apps; keep the protocol pack current.

**Cleanup:** remove the flow monitor from the policy profile.

### Lab 5.13 — Implement multicast components (ENWLSI 3.1)

**Objective:** Enable multicast on the WLC.

```text
WLC(config)# wireless multicast
WLC(config)# ap capwap multicast 239.10.10.10
WLC# show wireless multicast
```

**Expected result:** multicast enabled with a CAPWAP multicast group —
efficient AP delivery of multicast streams.

**Negative test:** unicast multicast delivery replicates a stream per client
and overloads the WLC; multicast-multicast mode scales it.

**Cleanup:** `no wireless multicast`.

### Lab 5.14 — Describe multicast's effect on wireless (ENWLSI 3.2)

**Objective:** Read the multicast data rate on the air.

```text
WLC# show ap dot11 5ghz network | include Multicast|Mandatory
```

**Expected result:** the mandatory/multicast data rate — multicast is sent at
the lowest mandatory rate, consuming disproportionate airtime.

**Negative test:** a low mandatory rate (e.g. 6 Mbps) makes multicast crush
airtime; raise the basic rate to speed multicast (at coverage cost).

**Cleanup:** none (read-only).

### Lab 5.15 — Implement multicast on a WLAN (ENWLSI 3.3)

**Objective:** Enable multicast for a specific WLAN/policy.

```text
WLC(config-wireless-policy)# multicast
WLC# show wireless profile policy detailed POL-VOICE | include Multicast
```

**Expected result:** multicast enabled on the policy profile — the WLAN can
carry multicast streams to clients.

**Negative test:** multicast enabled globally but not on the policy profile
still blocks it on that WLAN; both scopes matter.

**Cleanup:** `no multicast` on the policy profile.

### Lab 5.16 — Implement mDNS (ENWLSI 3.4)

**Objective:** Configure an mDNS (Bonjour) service policy.

```text
WLC(config)# mdns-sd gateway
WLC(config)# mdns-sd-flex-profile MDNS-FLEX
WLC# show mdns-sd summary
```

**Expected result:** the mDNS gateway bridging Bonjour services across VLANs
— AirPrint/Chromecast discovery without flooding mDNS everywhere.

**Negative test:** mDNS flooded across all VLANs (no gateway) is both a
scaling and a security problem; the gateway scopes it.

**Cleanup:** `no mdns-sd gateway`.

### Lab 5.17 — Implement Multicast Direct (ENWLSI 3.5)

**Objective:** Enable Multicast Direct (media stream) for a WLAN.

```text
WLC(config)# wireless media-stream multicast-direct
WLC(config-wireless-policy)# media-stream multicast-direct
WLC# show wireless media-stream group summary
```

**Expected result:** Multicast Direct converts multicast to unicast at the AP
for reliable video — better reliability for streaming.

**Negative test:** enabling Multicast Direct without admission control can
exhaust AP resources under many streams; pair with call admission control.

**Cleanup:** disable media-stream on the policy and globally.

### Lab 5.18 — Deploy CMX and Cisco Spaces (ENWLSI 4.1)

**Objective:** Confirm the WLC's connection to CMX/Cisco Spaces.

```text
WLC# show nmsp status
WLC# show wireless client summary | include Location
```

**Expected result:** an NMSP connection to CMX/Spaces `Active` — the WLC
streaming client location/analytics data to the location engine.

**Negative test:** NMSP down means no location data reaches CMX/Spaces;
maps/analytics go stale.

**Cleanup:** none (read-only).

### Lab 5.19 — Implement location services (ENWLSI 4.2)

**Objective:** Read the WLC's location/RSSI reporting for a client.

```text
WLC# show wireless client mac-address <mac> detail | include RSSI|AP Name
```

**Expected result:** per-client RSSI from multiple APs — the multilateration
input CMX/Spaces uses to place a client on a map.

**Negative test:** a client heard by only one AP cannot be triangulated;
location needs 3+ APs above the RSSI cutoff.

**Cleanup:** none (read-only).

### Lab 5.20 — Implement CMX/Cisco Spaces components (ENWLSI 5.1)

**Objective:** Read the location hierarchy (campus/building/floor) synced to
the WLC.

```text
WLC# show wireless location summary
```

**Expected result:** the location configuration tying APs to a map hierarchy
— the components that make location analytics meaningful.

**Negative test:** APs not placed on a floor map produce location data with
no spatial context; the map hierarchy is required.

**Cleanup:** none (read-only).

### Lab 5.21 — Implement location-aware guest services (ENWLSI 5.2)

**Objective:** Confirm a custom guest portal / captive-portal redirect.

```text
WLC# show wlan id 3 | include Web Auth|Portal
WLC# show parameter-map type webauth summary
```

**Expected result:** a guest WLAN redirecting to a custom portal (with
location-based content via Spaces) — revenue-generating, location-aware guest
onboarding.

**Negative test:** a webauth parameter-map pointing at an unreachable portal
leaves guests stuck at redirect; verify the portal URL.

**Cleanup:** none (read-only).

### Lab 5.22 — Troubleshoot location accuracy with Hyperlocation (ENWLSI 5.3)

**Objective:** Read Hyperlocation (AoA) status where deployed.

```text
WLC# show ap name AP1 config general | include Hyperlocation|Antenna
```

**Expected result:** Hyperlocation antenna module status — angle-of-arrival
tightens accuracy to ~1 m versus RSSI's several meters.

**Negative test:** expecting 1 m accuracy from RSSI multilateration alone;
Hyperlocation hardware is required for that precision.

**Cleanup:** none (read-only).

### Lab 5.23 — Troubleshoot CMX high availability (ENWLSI 5.4)

**Objective:** Read the CMX/Spaces connector HA/state from the WLC.

```text
WLC# show nmsp subscription summary
```

**Expected result:** the NMSP subscriptions/services active — a primary/
secondary CMX ensures analytics continuity on failover.

**Negative test:** a single CMX node is a single point of failure for
location; HA pairs the engines.

**Cleanup:** none (read-only).

### Lab 5.24 — Implement wIPS using Cisco DNA Center (ENWLSI 5.5)

**Objective:** Read the wireless-threat/rogue posture.

```text
WLC# show wireless wps rogue ap summary
WLC# show wireless wps rogue client summary
```

**Expected result:** detected rogue APs/clients and wIPS signatures — the
adaptive wireless IPS surface (managed via Catalyst Center).

**Negative test:** wIPS in detect-only mode alerts but does not contain; rogue
containment must be explicitly enabled.

**Cleanup:** none (read-only).

### Lab 5.25 — Configure client profiling on WLC and ISE (ENWLSI 6.1)

**Objective:** Enable device profiling for policy decisions.

```text
WLC(config-wireless-policy)# dhcp-tlv-caching
WLC(config-wireless-policy)# http-tlv-caching
WLC# show wireless client mac-address <mac> detail | include Device Type
```

**Expected result:** the WLC caching DHCP/HTTP attributes and reporting a
device type to ISE — profiling that drives differentiated policy.

**Negative test:** without TLV caching, ISE cannot profile the endpoint and
falls back to a generic policy.

**Cleanup:** remove the TLV-caching options.

### Lab 5.26 — Implement BYOD and guest (ENWLSI 6.2)

**Objective:** Confirm the dual-SSID BYOD onboarding flow.

```text
WLC# show wlan summary | include BYOD|Guest|Provision
WLC# show wireless client summary | include Provision
```

**Expected result:** an onboarding (provisioning) SSID and a secured SSID —
the BYOD flow that moves a device from open onboarding to certificate-based
access.

**Negative test:** a single open SSID with no onboarding grants full access to
unmanaged devices; BYOD separates provisioning from production access.

**Cleanup:** none (read-only).

### Lab 5.27 — Implement 802.1X and AAA across architectures (ENWLSI 6.3)

**Objective:** Bind a WLAN to a RADIUS server for 802.1X.

```text
WLC(config)# wlan CORP 1 CORP
WLC(config-wlan)# security dot1x authentication-list ISE-AUTH
WLC# show wlan name CORP | include 802.1X|AAA
```

**Expected result:** the WLAN using 802.1X against the ISE auth list —
enterprise authentication on local, FlexConnect, and fabric architectures.

**Negative test:** a FlexConnect AP with central auth loses 802.1X on a WAN
outage unless local EAP is configured; architecture changes the auth path.

**Cleanup:** `no wlan CORP`.

### Lab 5.28 — Implement Identity-Based Networking (ENWLSI 6.4)

**Objective:** Apply a per-user policy (VLAN/ACL) from RADIUS.

```text
WLC# show wireless client mac-address <mac> detail | include VLAN|ACL|SGT
```

**Expected result:** RADIUS-assigned VLAN/ACL/SGT applied per client —
identity, not SSID, drives the access policy.

**Negative test:** a static WLAN-to-VLAN mapping ignores identity; IBNS lets
one SSID serve many policies by user.

**Cleanup:** none (read-only).

### Lab 5.29 — Utilize reports on Prime/Catalyst Center (ENWLSI 7.1)

**Objective:** Read a wireless report source.

```text
WLC# show wireless stats client detail
WLC# show wireless summary
```

**Expected result:** client/AP/WLAN counts and stats — the data Prime
Infrastructure / Catalyst Center reports aggregate.

**Negative test:** reading a single WLC misses a multi-controller estate;
Prime/Catalyst Center aggregate across controllers.

**Cleanup:** none (read-only).

### Lab 5.30 — Manage alarms and rogues (ENWLSI 7.2)

**Objective:** Triage rogue and interference alarms.

```text
WLC# show wireless wps rogue ap summary
WLC# show logging | include ROGUE|WIPS
```

**Expected result:** classified rogues (friendly/malicious/unclassified) and
alarm history — the queue a wireless operator works.

**Negative test:** auto-containing an unclassified rogue that is a neighbor's
legitimate AP is a legal/operational risk; classify before containing.

**Cleanup:** none (read-only).

### Lab 5.31 — Manage RF interferers (ENWLSI 7.3)

**Objective:** Read CleanAir/spectrum interference.

```text
WLC# show ap dot11 5ghz cleanair air-quality summary
WLC# show ap dot11 5ghz cleanair device type all
```

**Expected result:** air-quality index and classified non-Wi-Fi interferers
(microwave, Bluetooth) — the spectrum data RRM reacts to.

**Negative test:** blaming Wi-Fi contention for a problem CleanAir shows is a
microwave oven; the spectrum view finds non-Wi-Fi sources.

**Cleanup:** none (read-only).

### Lab 5.32 — Troubleshoot client connectivity (ENWLSI 7.4)

**Objective:** Trace a client's association/auth failure.

```text
WLC# show wireless client mac-address <mac> detail
WLC# show wireless client mac-address <mac> mobility history
```

**Expected result:** the client's state machine (assoc → 802.1X → DHCP →
RUN) and where it stalled — the exact failure phase.

**Negative test:** blaming RF for a client stuck at 802.1X (a RADIUS/cert
problem); the state machine localizes it.

**Cleanup:** none (read-only).

### Lab 5.33 — Implement device access controls (ENWLSI 8.1)

**Objective:** Secure WLC management with RADIUS/TACACS+.

```text
WLC(config)# aaa authentication login VTY-AUTH group ISE local
WLC(config)# line vty 0 15
WLC(config-line)# login authentication VTY-AUTH
WLC# show run aaa | include authentication login
```

**Expected result:** WLC admin logins authenticated against ISE with a local
fallback — centralized management-plane access control.

**Negative test:** external AAA with no local method locks admins out when
ISE is down; keep a local account.

**Cleanup:** revert to prior VTY auth (keep a local login).

### Lab 5.34 — Implement access point authentication (ENWLSI 8.2)

**Objective:** Require 802.1X for APs joining the switch fabric.

```text
WLC(config)# ap dot1x username <user> password 0 <pw>
WLC# show ap dot1x summary
```

**Expected result:** APs authenticating via 802.1X to the wired switchport —
only trusted APs join the network.

**Negative test:** an AP on an open switchport with no 802.1X can be swapped
for a rogue; AP 802.1X binds the AP to the port.

**Cleanup:** remove the AP dot1x credentials.

### Lab 5.35 — Implement control-plane ACLs on the controller (ENWLSI 8.3)

**Objective:** Restrict management access to the WLC control plane.

```text
WLC(config)# ip access-list extended MGMT-ONLY
WLC(config-ext-nacl)# permit tcp 10.0.0.0 0.0.0.255 any eq 443
WLC(config)# control-plane host
WLC(config-cp-host)# management-interface GigabitEthernet1 allow https ssh
WLC# show ip access-lists MGMT-ONLY
```

**Expected result:** management (HTTPS/SSH) restricted to the admin subnet on
the control plane — CPU-protecting the WLC.

**Negative test:** an unrestricted management interface accepts connections
from anywhere; the control-plane ACL scopes it.

**Cleanup:** remove the control-plane host management restriction and ACL.

### Lab 5.36 — Catalyst 9800 WLAN with 802.1X and fast roaming (integrative)

**Objective:** Bring up a Catalyst 9800 WLC (or CML/virtual 9800-CL node),
join an access point, build an 802.1X-secured WLAN with fast roaming
enabled, and validate client association.

**Prerequisites**

- One Catalyst 9800 controller (appliance, EWC, or 9800-CL virtual node)
  and at least one compatible Catalyst access point, or an equivalent CML
  topology with a 9800-CL controller node.
- Reachable DHCP scope for the AP's subnet with option 43 (or a DNS
  `CISCO-CAPWAP-CONTROLLER` record) pointing APs at the WLC.
- A RADIUS server (or the local AAA fallback introduced in [Chapter 7](07-cisco-identity-access-control-and-segmentation.md)) for
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

## Design Exercise

**ENWLSD (300-425 Wireless Design)** is a design exam: it rewards reasoning
from requirements to a wireless design, not configuration recall. The
implementation labs above (5.1–5.35) cover ENWLSI; this exercise covers
ENWLSD's design domains — predictive/site survey, high-density, location,
and security design — with no lab required.

**Scenario.** Design Wi-Fi for a three-story, 200,000-sq-ft hospital: dense
patient/staff/guest devices, real-time voice and medical telemetry, a
requirement for ~3 m asset-location accuracy, WPA3 for staff, an isolated
guest network, and no coverage holes in stairwells or basements.

**Produce, defending each choice against a rejected alternative:**

1. **Coverage and capacity design** — bands, channel width, and AP count/
   placement from a predictive survey, and why (capacity-driven vs
   coverage-driven). Justify the 2.4 GHz decision for a high-density site.
2. **High-density and roaming design** — 802.11r/k/v, band steering, and
   RRM (DCA/TPC) settings that keep voice/telemetry roaming seamless.
3. **Location design** — AP density and placement (perimeter + interior) and
   the technology (RSSI multilateration vs Hyperlocation AoA) needed to hit
   3 m accuracy, with its cost.
4. **Segmentation and security design** — SSID/VLAN/SGT plan separating
   staff (WPA3-Enterprise), medical devices (profiled, MAB/certificate), and
   guest (isolated, portal); and the wIPS/rogue posture.
5. **Resilience design** — WLC HA (SSO), FlexConnect vs local mode per site,
   and survivability if the WAN or a WLC fails.

**Success looks like:** every AP-count, band, and location decision traces to
a stated requirement (density, voice, 3 m accuracy), each with the
alternative rejected and why — the design standard ENWLSD applies.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

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
