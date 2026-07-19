# Chapter 6: Wireless Network Foundations

## Learning Objectives

- Explain RF fundamentals — frequency bands, channels, channel width, and
  signal power measured in dBm — well enough to reason about coverage and
  interference trade-offs.
- Describe the evolution of IEEE 802.11 standards and how they map to
  consumer-facing Wi-Fi generation numbers.
- Distinguish autonomous and controller-based WLAN architectures, and
  explain the role of a tunneling protocol like CAPWAP in a split-MAC
  design.
- Explain the BSS/ESS model, the client association process, and the role
  of 802.11r/k/v in enterprise roaming.
- Explain the evolution of WLAN security from WEP through WPA3 and describe
  enterprise 802.1X/EAP authentication.
- Plan channel and power settings for a multi-access-point deployment that
  avoids co-channel interference.
- Diagnose common wireless client connectivity failures using layered
  reasoning consistent with earlier chapters.

## Theory and Architecture

Wireless LANs extend the Layer 2 domain introduced in [Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md) onto a
shared, unbounded medium — every other concept in this chapter exists
because radio frequency (RF) does not behave like a switched cable. This
chapter is deliberately vendor-neutral; [Volume III](../../volume-03-cisco-enterprise-networking/README.md)'s "Catalyst Wireless
Architecture and Operations" chapter covers Cisco-specific controller and
access-point configuration in depth.

### RF Fundamentals: Frequency, Channels, and Power

Enterprise Wi-Fi operates in three unlicensed frequency bands, each with
different propagation and capacity characteristics:

| Band | Approx. Range | Channel Width Options | Characteristics |
| --- | --- | --- | --- |
| 2.4 GHz | 2.400–2.4835 GHz | 20 MHz (22 MHz spacing) | Longest range, most interference (Bluetooth, microwaves, other Wi-Fi), only 3 non-overlapping 20 MHz channels (1, 6, 11 in most regions) |
| 5 GHz | 5.150–5.895 GHz | 20/40/80/160 MHz | Shorter range than 2.4 GHz, far more channels, many require Dynamic Frequency Selection (DFS) to avoid radar interference |
| 6 GHz | 5.925–7.125 GHz | 20/40/80/160 MHz | Shortest range, cleanest spectrum (Wi-Fi 6E/7 only, no legacy device support), largest channel count |

A **channel** is a slice of a band's spectrum; **channel width** determines
how much of that spectrum a single transmission uses. Wider channels
(80/160 MHz) increase throughput but leave fewer non-overlapping channels
available for reuse across nearby access points — a direct trade-off
between per-client speed and multi-AP capacity that must be decided during
design (see Design Considerations).

**Signal power** is expressed in dBm (decibel-milliwatts), a logarithmic
scale where +3 dBm is roughly double the power and −3 dBm is roughly half.
Key measurements:

| Term | Meaning |
| --- | --- |
| EIRP (Equivalent Isotropically Radiated Power) | Transmitter power plus antenna gain minus cable loss — the effective power radiated, often regulatorily capped |
| RSSI (Received Signal Strength Indicator) | The signal power a receiver measures from a given transmitter, typically −30 dBm (excellent, very close) to −90 dBm (unusable) |
| SNR (Signal-to-Noise Ratio) | The difference between signal power and the noise floor; a strong RSSI with a high noise floor can still perform poorly |
| Free Space Path Loss (FSPL) | Signal attenuation over distance, which increases with frequency — this is *why* 6 GHz has shorter range than 2.4 GHz at equal transmit power |

### 802.11 Standard Evolution

| IEEE Amendment | Wi-Fi Generation | Band(s) | Max PHY Rate (typical) | Key Feature |
| --- | --- | --- | --- | --- |
| 802.11a | — | 5 GHz | 54 Mbps | First 5 GHz standard |
| 802.11b | — | 2.4 GHz | 11 Mbps | First mass-market Wi-Fi |
| 802.11g | — | 2.4 GHz | 54 Mbps | OFDM brought to 2.4 GHz |
| 802.11n | Wi-Fi 4 | 2.4/5 GHz | 600 Mbps | MIMO (multiple spatial streams), channel bonding to 40 MHz |
| 802.11ac | Wi-Fi 5 | 5 GHz | ~3.5 Gbps | MU-MIMO (downlink), wider channels to 160 MHz |
| 802.11ax | Wi-Fi 6 / 6E | 2.4/5 GHz (6E adds 6 GHz) | ~9.6 Gbps | OFDMA (sub-channel scheduling), bidirectional MU-MIMO, Target Wake Time for power efficiency |
| 802.11be | Wi-Fi 7 | 2.4/5/6 GHz | ~46 Gbps (theoretical) | Multi-Link Operation (simultaneous multi-band association), 320 MHz channels |

The generational naming (Wi-Fi 4 through 7) was introduced by the Wi-Fi
Alliance to make the underlying IEEE amendment numbers meaningful to a
non-technical audience; enterprise engineers should know both, since
procurement and marketing materials use the generation number while device
capability negotiation and RF planning tools use the IEEE designation.

### WLAN Architecture: Autonomous vs. Controller-Based

**Autonomous access points** operate as fully independent devices — each AP
handles its own RF management, client authentication, and forwarding
decisions, with configuration applied and managed per device. This scales
poorly past a handful of APs: channel/power coordination, consistent SSID
and security policy, and roaming all require manual synchronization across
every AP.

**Controller-based (lightweight) architecture** splits the AP's function
between the AP itself and a central Wireless LAN Controller (WLC), a
pattern known as **split MAC**:

| Function | Location |
| --- | --- |
| Real-time 802.11 MAC operations (beacons, ACKs, retransmission) | Access point |
| RF management (channel/power assignment, interference detection) | Controller (with AP telemetry) |
| Client authentication and policy enforcement | Controller |
| Roaming coordination across APs | Controller |
| Client traffic forwarding | Either local (at the AP) or centralized (tunneled to the controller), depending on the deployment mode |

The AP and controller communicate over the **Control and Provisioning of
Wireless Access Points (CAPWAP)** protocol, which tunnels both control
traffic (RF management, configuration) and, in centralized-forwarding
deployments, client data traffic back to the controller. Controller-based
architecture is the dominant enterprise pattern because it centralizes RF
optimization and security policy across potentially hundreds of APs from a
single management point — the specific vendor implementation (Cisco
Catalyst wireless architecture) is covered in [Volume III](../../volume-03-cisco-enterprise-networking/README.md).

### BSS, ESS, and the Client Association Process

A **Basic Service Set (BSS)** is one access point (or radio) and the
clients associated with it, identified by a **BSSID** (the radio's MAC
address). An **Extended Service Set (ESS)** is a group of BSSs sharing the
same SSID, allowing a client to roam between physical APs while appearing
to remain on one logical network.

Association is a three-stage exchange before a client can pass data:

```text
Client                                          Access Point
  |--- Probe Request (or passive: listen for Beacon) --->|
  |<-- Probe Response (SSID, supported rates, security) --|
  |--- Authentication Request ---------------------------->|
  |<-- Authentication Response ----------------------------|
  |--- Association Request --------------------------------->|
  |<-- Association Response (client is now on the BSS) ------|
  |=== WPA2/WPA3 4-way handshake (session key derivation) ===|
```

For enterprise (WPA2/WPA3-Enterprise) networks, association is followed by
an 802.1X/EAP exchange with a RADIUS server before the 4-way handshake
completes — covered in the security section below.

### Enterprise Roaming: 802.11r, 802.11k, and 802.11v

As a client moves and signal from its current AP weakens, it must roam to
a stronger AP in the same ESS without dropping active sessions (a
particular concern for VoIP and video). Three amendments make this fast and
deterministic instead of client-guesswork:

- **802.11k (Radio Resource Management)** lets an AP provide a client with
  a neighbor report — a list of nearby APs and their channels — so the
  client does not have to scan every channel blindly before roaming.
- **802.11v (BSS Transition Management)** lets the infrastructure suggest a
  specific AP for a client to roam to, based on load and RF conditions the
  client cannot see on its own.
- **802.11r (Fast BSS Transition)** pre-negotiates encryption keys with
  candidate APs before the roam happens, cutting the re-authentication
  delay from hundreds of milliseconds (unacceptable for an active VoIP
  call) to under 50 ms.

### Wireless Security Evolution

| Standard | Encryption | Status |
| --- | --- | --- |
| WEP | RC4, static key | Broken; must not be used |
| WPA (TKIP) | RC4-based TKIP | Deprecated transitional standard; must not be used |
| WPA2 (CCMP/AES) | AES-CCMP | Baseline acceptable standard; Personal (PSK) or Enterprise (802.1X) |
| WPA3 | AES-CCMP (Enterprise), SAE replaces PSK (Personal) | Current standard; adds forward secrecy and resistance to offline dictionary attacks |

**WPA2/WPA3-Personal** uses a Pre-Shared Key (PSK) shared by all clients —
appropriate for guest or small-office networks but unsuitable for
enterprise use because the key cannot be revoked per-user and is difficult
to rotate without disrupting every connected device.

**WPA2/WPA3-Enterprise** uses **802.1X** port-based access control with the
**Extensible Authentication Protocol (EAP)**: the AP acts as an 802.1X
authenticator, relaying the client's (supplicant's) credentials to a
**RADIUS** server (the authentication server) defined in RFC 2865. Common
EAP methods:

| EAP Method | Credential | Notes |
| --- | --- | --- |
| EAP-TLS | Client certificate | Strongest option; requires client certificate distribution (PKI) |
| PEAP-MSCHAPv2 | Username/password inside a TLS tunnel | Common where certificate deployment is impractical |
| EAP-TTLS | Username/password or other inner method inside a TLS tunnel | Similar to PEAP, broader inner-method support |

This is the same 802.1X framework used for wired port authentication,
which is why enterprise identity architecture ([Volume X](../../volume-10-enterprise-cybersecurity/README.md)) treats wired and
wireless access control as a single policy domain rather than two separate
systems.

## Design Considerations

- **Design for capacity, not just coverage.** A signal that reaches every
  corner of a floor at −80 dBm satisfies "coverage" but fails under real
  client density; enterprise WLAN design targets a minimum RSSI (commonly
  −67 dBm for data, tighter for VoIP) with enough AP density to keep
  client counts per radio within the deployment's target.
- **Plan channel reuse to minimize co-channel interference.** With only
  three non-overlapping 2.4 GHz channels, dense deployments frequently
  disable 2.4 GHz for data SSIDs entirely and rely on 5/6 GHz, which offer
  far more usable channels for a 1-3-6-11-style reuse pattern (or its 5/6
  GHz equivalent) across adjacent APs.
- **Choose channel width as a capacity/range trade-off.** Wider channels
  (80/160 MHz) raise per-client throughput but reduce the number of
  non-overlapping channels available for reuse in a dense AP deployment —
  favor narrower channels in high-AP-density environments and wider
  channels where AP density is low and per-client throughput matters more.
- **Decide whether legacy client support is required before enabling a
  6 GHz-only SSID.** Wi-Fi 6E/7 devices only; older clients simply will not
  see the network, which is sometimes the intent (a clean, interference-free
  SSID for modern devices) and sometimes an unplanned access gap.
- **Size the WLAN controller deployment for redundancy**, not just AP
  count — controller failure (in a centralized-forwarding design)
  can affect every AP it manages, so controller high availability is a
  first-order design decision, not an afterthought.
- **Plan RF for worst-case client posture, not best-case.** A laptop with
  a strong antenna performs very differently from a handheld scanner or IoT
  sensor at the edge of a cell; site surveys should validate against the
  actual client device mix in use, not a single reference device.

## Implementation and Automation

### WLAN Profile Configuration (Vendor-Neutral Pseudo-CLI)

```text
wlc(config)# wlan create CORP-DATA ssid CORP-DATA
wlc(config-wlan)# security wpa wpa3 aes 802.1x
wlc(config-wlan)# security 802.1x radius-server 10.10.1.30 key <RADIUS_SHARED_SECRET>
wlc(config-wlan)# security pmf required
wlc(config-wlan)# radio-policy 5ghz-6ghz-only
wlc(config-wlan)# no shutdown

wlc(config)# ap-group FLOOR2-EAST
wlc(config-ap-group)# wlan CORP-DATA
wlc(config-ap-group)# rf-profile HIGH-DENSITY
```

### RF Profile: Channel and Power Assignment

```text
wlc(config)# rf-profile HIGH-DENSITY
wlc(config-rf-profile)# band 5ghz
wlc(config-rf-profile)# channel-width 40
wlc(config-rf-profile)# tx-power-control auto min -10 max 17
wlc(config-rf-profile)# dca-channel-list 36,40,44,48,149,153,157,161
```

Most enterprise controllers run automatic RF management (dynamic channel
assignment and transmit power control) that continuously adjusts channel
and power per AP based on neighboring AP RF telemetry — the configuration
above defines the *boundaries* the automatic algorithm operates within,
rather than fixing every AP's channel and power manually, which does not
scale past a handful of access points.

### Automating WLAN Configuration Consistency

```python
import requests

def get_ap_channel_power(wlc_url, token, ap_name):
    """Query a controller's REST API for an AP's current channel and power
    (illustrative — endpoint and auth scheme vary by vendor)."""
    resp = requests.get(
        f"{wlc_url}/api/v1/aps/{ap_name}/radios",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()

def audit_dfs_events(radios):
    """Flag any radio that recently switched channel due to radar
    detection (DFS), which silently drops all clients on that radio."""
    return [r for r in radios if r.get("last_channel_change_reason") == "radar"]
```

Configuration drift audits like this matter operationally: a controller's
automatic RF management can and does change a live AP's channel in response
to detected radar on a DFS channel, which is correct behavior but produces
a brief, real client disruption that should be visible in monitoring
([Chapter 8](08-network-validation-and-observability.md)) rather than discovered only through a user complaint.

## Validation and Troubleshooting

```bash
# Linux client: show current association details
iw dev wlan0 link

# Linux client: scan for visible SSIDs, channels, and signal strength
sudo iw dev wlan0 scan | grep -E "SSID|freq|signal"

# Controller pseudo-CLI: show a connected client's negotiated rate and RSSI
wlc# show wireless client mac aabb.ccdd.eeff detail
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Client sees the SSID but never associates | Authentication failure (wrong PSK, EAP/certificate issue) | Check RADIUS/controller authentication logs |
| Client associates but never gets an IP address | DHCP failure on the wireless VLAN (see [Chapter 5](05-core-network-services.md)), not a wireless fault | Confirm DHCP scope/relay on the client VLAN |
| Client connects near the AP but disconnects farther away | RSSI dropped below the client's roaming or the AP's minimum-RSSI threshold | Check RSSI/SNR at the point of disconnection with a site survey tool |
| Voice/video quality degrades despite strong signal | High channel utilization or co-channel interference, not weak signal | Check channel utilization and neighboring AP channel overlap |
| Client "sticks" to a distant AP instead of roaming to a closer one | Client-driven roaming decision with no 802.11k/v assistance, or minimum-RSSI/band-steering not enforced | Verify 802.11k/v/r are enabled and supported by the client |
| All clients on one radio drop simultaneously | DFS radar detection forced a channel change | Check controller/AP event log for a radar-triggered channel change |
| New Wi-Fi 6E/7 devices cannot see an expected SSID | SSID is 6 GHz-only and the device lacks 6 GHz support | Confirm device capability and intended radio policy |

Wireless troubleshooting benefits from the same layered discipline used
throughout this volume: confirm RF association first (Layer 1/2), then
DHCP/IP addressing (Layer 3, [Chapter 5](05-core-network-services.md)), before assuming an application
issue — a very common false diagnosis is treating a DHCP failure on the
wireless VLAN as a "Wi-Fi problem" when the RF association itself is
healthy.

## Security and Best Practices

- Disable WEP and WPA-TKIP entirely; they should not exist anywhere in an
  enterprise WLAN configuration, including legacy or guest SSIDs.
- Prefer WPA3-Enterprise with EAP-TLS where certificate distribution is
  feasible; PEAP-MSCHAPv2 remains an acceptable fallback but is weaker
  against credential-based attacks than certificate-based EAP-TLS.
- Enable **Protected Management Frames (PMF / 802.11w)**, which prevents
  forged deauthentication and disassociation frames — a common and
  otherwise trivial denial-of-service and rogue-AP technique against
  unprotected management frames.
- Deploy a Wireless Intrusion Prevention System (WIPS) or controller-native
  rogue detection to identify unauthorized APs broadcasting the
  enterprise's SSID (evil-twin attacks) or unauthorized APs physically
  connected to the wired network.
- Isolate guest and IoT SSIDs from corporate VLANs entirely (client
  isolation, separate VLAN and firewall policy), and require captive
  portal or WPA3-Personal (SAE) rather than open authentication for guest
  networks.
- Protect the RADIUS shared secret and certificate infrastructure backing
  802.1X authentication with the same rigor as any other credential store;
  a compromised RADIUS server or CA undermines every wireless (and wired
  802.1X) client relying on it.

## References and Knowledge Checks

**References**

- [IEEE 802.11-2020 — Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications](https://standards.ieee.org/ieee/802.11/7028/)
- [IEEE 802.11r-2008 — Fast BSS Transition](https://standards.ieee.org/standard/802_11r-2008.html)
- [RFC 2865 — Remote Authentication Dial In User Service (RADIUS)](https://www.rfc-editor.org/rfc/rfc2865)
- [RFC 3748 — Extensible Authentication Protocol (EAP)](https://www.rfc-editor.org/rfc/rfc3748)
- [RFC 5415 — Control and Provisioning of Wireless Access Points (CAPWAP) Protocol Specification](https://www.rfc-editor.org/rfc/rfc5415)
- [Wi-Fi Alliance — WPA3 Specification](https://www.wi-fi.org/discover-wi-fi/security)

**Knowledge Checks**

1. Explain why 6 GHz Wi-Fi has shorter effective range than 2.4 GHz at the
   same transmit power, in terms of free space path loss.
2. What problem does split-MAC controller-based architecture solve that
   autonomous access points cannot solve at scale?
3. Walk through the client association sequence, and identify where the
   WPA2/WPA3 4-way handshake occurs relative to 802.1X/EAP authentication.
4. Why is WPA2/WPA3-Personal (PSK) unsuitable for a typical enterprise
   deployment, independent of the strength of the encryption itself?
5. A user reports their laptop connects to Wi-Fi but nothing loads in a
   browser. Which layer should be checked first, and why?
6. What does Protected Management Frames (802.11w) specifically prevent,
   and why does that matter even on a network already using WPA3?

## Hands-On Lab

**Objective.** Construct and decode synthetic 802.11 management frames to
observe the beacon/probe/association sequence directly, and calculate free
space path loss to quantify the coverage trade-off between 2.4 GHz, 5 GHz,
and 6 GHz — reproducible entirely in software, without wireless hardware.

**Prerequisites**

- A Linux, macOS, or Windows host with `python3`.
- `scapy` and `tshark` (Wireshark CLI) installed:

  ```bash
  python3 -m venv ~/wifi-lab-venv
  source ~/wifi-lab-venv/bin/activate
  pip install scapy
  # tshark: sudo apt-get install -y tshark   (Debian/Ubuntu)
  ```

**Lab Steps**

1. Craft a synthetic Beacon frame advertising a lab SSID on channel 6
   (2.4 GHz) and write it to a pcap file:

   ```bash
   python3 - <<'PYEOF'
   from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, wrpcap

   frame = (
       RadioTap()
       / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff",
               addr2="02:00:00:00:00:01", addr3="02:00:00:00:00:01")
       / Dot11Beacon(cap="ESS")
       / Dot11Elt(ID="SSID", info="LAB-WLAN")
       / Dot11Elt(ID="DSset", info=bytes([6]))
   )
   wrpcap("/tmp/wifi-lab.pcap", [frame])
   print("Beacon frame written to /tmp/wifi-lab.pcap")
   PYEOF
   ```

2. Decode the frame with `tshark` and confirm it is recognized as a
   management-type beacon on the expected channel:

   ```bash
   tshark -r /tmp/wifi-lab.pcap -V | grep -E "SSID|Type/Subtype|DS Parameter"
   ```

   **Expected result:** the decode shows `Type/Subtype: Beacon frame
   (0x0008)`, `SSID parameter set: LAB-WLAN`, and `Current Channel: 6` —
   confirming the frame matches the management-frame structure described
   in this chapter's theory section.

3. Extend the capture with a Probe Request, Probe Response, Association
   Request, and Association Response to reproduce the full association
   sequence from the chapter:

   ```bash
   python3 - <<'PYEOF'
   from scapy.all import (RadioTap, Dot11, Dot11ProbeReq, Dot11ProbeResp,
                           Dot11AssoReq, Dot11AssoResp, Dot11Elt, rdpcap, wrpcap)

   client = "02:00:00:00:00:02"
   ap = "02:00:00:00:00:01"

   probe_req = (RadioTap() / Dot11(type=0, subtype=4, addr1=ap, addr2=client, addr3=ap)
                / Dot11ProbeReq() / Dot11Elt(ID="SSID", info="LAB-WLAN"))
   probe_resp = (RadioTap() / Dot11(type=0, subtype=5, addr1=client, addr2=ap, addr3=ap)
                 / Dot11ProbeResp(cap="ESS") / Dot11Elt(ID="SSID", info="LAB-WLAN"))
   assoc_req = (RadioTap() / Dot11(type=0, subtype=0, addr1=ap, addr2=client, addr3=ap)
                / Dot11AssoReq() / Dot11Elt(ID="SSID", info="LAB-WLAN"))
   assoc_resp = (RadioTap() / Dot11(type=0, subtype=1, addr1=client, addr2=ap, addr3=ap)
                 / Dot11AssoResp(status=0))

   existing = rdpcap("/tmp/wifi-lab.pcap")
   wrpcap("/tmp/wifi-lab.pcap", existing + [probe_req, probe_resp, assoc_req, assoc_resp])
   print("Association sequence appended.")
   PYEOF

   tshark -r /tmp/wifi-lab.pcap -T fields -e frame.number -e wlan.fc.type_subtype
   ```

   **Expected result:** five frames in order — subtype `0x08` (Beacon),
   `0x04` (Probe Request), `0x05` (Probe Response), `0x00` (Association
   Request), `0x01` (Association Response) — matching the theory section's
   association sequence.

4. Calculate free space path loss and estimated RSSI at increasing
   distances for 2.4 GHz, 5 GHz, and 6 GHz to quantify the coverage
   trade-off from this chapter's RF fundamentals section:

   ```bash
   python3 - <<'PYEOF'
   import math

   def fspl_db(distance_m, freq_mhz):
       # FSPL(dB) = 20*log10(d_km) + 20*log10(f_MHz) + 32.44
       d_km = distance_m / 1000
       return 20 * math.log10(d_km) + 20 * math.log10(freq_mhz) + 32.44

   TX_EIRP_DBM = 20  # typical enterprise AP EIRP
   bands = {"2.4 GHz": 2437, "5 GHz": 5200, "6 GHz": 6115}

   for distance in (10, 30, 60):
       print(f"--- Distance: {distance} m ---")
       for band, freq in bands.items():
           loss = fspl_db(distance, freq)
           rssi = TX_EIRP_DBM - loss
           print(f"  {band}: FSPL={loss:.1f} dB  estimated RSSI={rssi:.1f} dBm")
   PYEOF
   ```

   **Expected result:** at every distance, 6 GHz shows the highest path
   loss (weakest estimated RSSI) and 2.4 GHz the lowest, confirming that
   higher-frequency bands attenuate faster over distance — the physical
   reason 6 GHz deployments require higher AP density than 2.4/5 GHz for
   equivalent coverage.

**Negative Test**

Recompute step 4 at 100 meters and compare the 6 GHz result against a
typical enterprise receiver sensitivity threshold of −70 dBm for reliable
data throughput:

```bash
python3 -c "
import math
d_km = 100/1000
loss = 20*math.log10(d_km) + 20*math.log10(6115) + 32.44
rssi = 20 - loss
print(f'6 GHz RSSI at 100m: {rssi:.1f} dBm')
print('Link viable for data' if rssi > -70 else 'Link budget deficit: below reliable threshold')
"
```

**Expected result:** the estimated RSSI falls below −70 dBm, printing
"Link budget deficit" — demonstrating in calculation what the design
section states in prose: 6 GHz cells must be smaller (denser AP placement)
than 2.4/5 GHz cells to deliver the same reliability at range.

**Cleanup**

```bash
rm -f /tmp/wifi-lab.pcap
deactivate
rm -rf ~/wifi-lab-venv
```

## Summary and Completion Checklist

This chapter covered RF fundamentals, the 802.11 standard evolution, the
controller-based (split-MAC) WLAN architecture that dominates enterprise
deployments, the client association and roaming sequence, and the security
evolution from WEP through WPA3-Enterprise with 802.1X/EAP. The hands-on
lab built and decoded a synthetic association sequence and quantified, with
an actual free space path loss calculation, why higher-frequency bands
require denser AP placement — connecting the chapter's RF theory to a
concrete design consequence rather than leaving it abstract.

**Completion Checklist**

- [ ] Can explain the coverage/capacity trade-off between 2.4 GHz, 5 GHz,
      and 6 GHz.
- [ ] Can describe split-MAC controller-based architecture and CAPWAP's
      role in it.
- [ ] Can walk through the beacon/probe/association/4-way-handshake
      sequence.
- [ ] Understands the purpose of 802.11k/v/r in enterprise roaming.
- [ ] Can explain the WPA2/WPA3-Enterprise 802.1X/EAP/RADIUS
      authentication chain and why WPA3-Personal PSK is unsuitable for
      enterprise use.
- [ ] Constructed and decoded a synthetic 802.11 association sequence and
      calculated free space path loss across three frequency bands.
