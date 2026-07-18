# Chapter 03: Management Network, IPv4, IPv6, DNS, NTP, and Connectivity

## Learning Objectives

- Choose between dedicated NIC and shared LOM network modes for iDRAC and
  explain the operational trade-offs of each.
- Configure static and DHCP-based IPv4 addressing, VLAN tagging, and NIC
  failover for the iDRAC management interface.
- Configure IPv6 addressing and explain when it is required rather than
  optional in a given environment.
- Configure DNS registration and resolution, and NTP time
  synchronization, and explain why both are prerequisites for reliable
  certificate validation and log correlation covered in later chapters.
- Diagnose the most common iDRAC network connectivity failures using
  RACADM, Redfish, and physical-layer checks.

## Theory and Architecture

### Dedicated NIC vs. shared LOM

Rack and tower PowerEdge servers offer two fundamentally different network
topologies for iDRAC traffic:

- **Dedicated NIC** — a physical Ethernet port on the server (commonly
  labeled with a wrench icon) used exclusively for iDRAC management
  traffic. This port is not visible to the host OS at all; it exists
  purely on iDRAC's side of the hardware boundary. This is the
  architecturally cleanest separation between management and production
  traffic and is the default recommendation for any environment with a
  dedicated out-of-band management network.
- **Shared LOM (LAN on Motherboard)** — iDRAC traffic rides one of the
  server's onboard production NIC ports, multiplexed with host OS traffic
  at the hardware level before the port. This avoids consuming a switch
  port purely for management on servers with limited rack-side cabling
  budget, at the cost of iDRAC traffic sharing physical and (unless VLAN
  segmented) logical network exposure with production traffic.

Modular (sled) servers behave differently: their iDRAC traffic typically
routes through the chassis's Chassis Management Controller (CMC) fabric
rather than a per-sled dedicated port, which is why this volume's network
guidance is scoped primarily to rack and tower topology; modular
management topology is covered under OpenManage Enterprise-Modular in
Volume XXII's related discussion, not duplicated here.

### NIC selection and failover modes

iDRAC's `NIC.Selection` setting determines which physical port carries
iDRAC traffic: `Dedicated`, or one of the shared LOM ports (commonly
labeled `LOM1` through `LOM4` depending on onboard NIC count). A related
`NIC.Failover` setting allows iDRAC to fail over from the dedicated port
to a shared LOM port (or between LOM ports) if the primary path loses
link — useful where the dedicated management network itself might
experience an outage and continued reachability over the production
network is an acceptable fallback for a defined period. Failover changes
the operational meaning of "which port is iDRAC on" from a fixed answer to
a conditional one; document this explicitly wherever it's enabled so
troubleshooting doesn't start from a wrong assumption about which physical
path is active.

### VLAN tagging at the iDRAC level

iDRAC can apply an 802.1Q VLAN tag directly to its own management traffic,
independent of any VLAN configuration on the host OS side of a shared LOM
port. This lets a shared-LOM iDRAC land on a distinct VLAN from the host's
production VLAN even though they share a physical port — a common and
effective way to gain most of the isolation benefit of a dedicated NIC
without consuming a physical port, provided the upstream switch port is
configured as an appropriate trunk carrying both VLANs.

### IPv4, IPv6, and dual-stack operation

iDRAC supports IPv4, IPv6, or both simultaneously (dual-stack). IPv4 with
DHCP is the default out-of-box state on most platforms and is sufficient
for many environments. IPv6 becomes a requirement rather than an option
in environments with an IPv6-only or IPv6-preferred management network
policy, in some government and regulated environments with IPv6
mandates, and in larger address-space-constrained management networks
where IPv4 exhaustion has pushed infrastructure teams toward IPv6 for new
address allocations. iDRAC's IPv6 implementation supports both stateless
address autoconfiguration (SLAAC) and DHCPv6, plus static assignment.

### DNS and NTP as prerequisites, not conveniences

DNS registration (iDRAC registering its own hostname with a DNS server)
and correct forward/reverse resolution matter beyond simple convenience:
certificate validation in Chapter 4 depends on the hostname a client
resolves matching the name on iDRAC's TLS certificate, and fleet tools
(including OME, Volume XXII) that build inventory and alert records from
hostname rather than raw IP produce far more usable records when DNS is
correct from the start. NTP matters even more acutely: TLS handshakes
involve certificate validity-period checks that fail confusingly when
iDRAC's clock has drifted, and every timestamp in the SEL and Lifecycle
Log (Chapter 6) — the record you will eventually depend on to reconstruct
an incident timeline — is only as trustworthy as the clock that wrote it.
Configure NTP during initial network bring-up, not as a follow-up task
after other issues have already surfaced from clock drift.

## Design Considerations

- **Default to dedicated NIC where the cabling budget allows it.** The
  clean separation is worth the extra switch port in the majority of
  enterprise environments; reserve shared LOM for genuinely
  cable-constrained deployments (some edge and remote-office footprints)
  where the trade-off is deliberate.
- **If using shared LOM, always VLAN-isolate.** Running iDRAC
  unsegmented on the same VLAN as host production traffic on a shared
  port erodes most of the security value of having an out-of-band
  management plane at all. Tag iDRAC's shared-LOM traffic onto a distinct
  management VLAN even when a dedicated NIC isn't available.
  Confirm the upstream switch port is configured as a trunk carrying both
  VLANs before enabling the tag, since a mismatch here silently drops
  iDRAC traffic rather than producing an obvious error.
- **Decide static vs. DHCP-with-reservation deliberately, not by
  default.** DHCP without reservation is workable for a handful of lab
  units but becomes an operational liability at fleet scale — address
  changes on lease renewal or DHCP server failure break every credential
  profile, alert destination, and inventory record that references the
  old address. Static addressing, or DHCP with a MAC-keyed reservation, is
  the practical standard for anything beyond a small lab.
  - **Plan IPv6 policy explicitly, even if the answer is "disabled for
  now."** An iDRAC with both IPv4 and IPv6 enabled and only IPv4 actually
  managed is a common source of an unmonitored, ungoverned secondary
  access path. If IPv6 is not part of your management strategy yet,
  disable it rather than leaving it in an unmanaged default state.
- **Treat DNS and NTP server addresses as part of your management-network
  standard, not a per-server choice.** Every iDRAC in an environment
  should point at the same DNS and NTP infrastructure (or the same
  documented regional set) so troubleshooting one unit's network
  configuration generalizes to the next, rather than requiring
  rediscovery of the correct servers each time.
- **Plan firewall rules around the actual protocols iDRAC uses, not just
  HTTPS.** Beyond TCP 443 for the web console and Redfish, plan for SSH
  (TCP 22) for RACADM, SNMP (UDP 161/162) if used for alerting, and
  virtual media/console-related ports (Chapter 5) if remote KVM/media use
  is planned across a routed (not local L2) network path.

## Implementation and Automation

### Selecting dedicated vs. shared LOM

```bash
racadm set iDRAC.NIC.Selection Dedicated
```

To use a shared LOM port instead, with the failover destination if the
dedicated port later becomes preferred as a fallback:

```bash
racadm set iDRAC.NIC.Selection LOM1
racadm set iDRAC.NIC.Failover Dedicated
```

### Configuring IPv4

Static assignment:

```bash
racadm set iDRAC.IPv4.DHCPEnable Disabled
racadm set iDRAC.IPv4.Address 10.20.30.40
racadm set iDRAC.IPv4.Netmask 255.255.255.0
racadm set iDRAC.IPv4.Gateway 10.20.30.1
```

DHCP:

```bash
racadm set iDRAC.IPv4.DHCPEnable Enabled
```

### Configuring VLAN tagging

```bash
racadm set iDRAC.NIC.VLanEnable Enabled
racadm set iDRAC.NIC.VLanID 200
racadm set iDRAC.NIC.VLanPriority 0
```

### Configuring IPv6

```bash
racadm set iDRAC.IPv6.Enable Enabled
racadm set iDRAC.IPv6.Address1 2001:db8:20:30::40
racadm set iDRAC.IPv6.PrefixLength 64
racadm set iDRAC.IPv6.Gateway 2001:db8:20:30::1
```

For SLAAC/DHCPv6-based assignment instead of static:

```bash
racadm set iDRAC.IPv6.AutoConfig Enabled
```

### Configuring DNS

```bash
racadm set iDRAC.IPv4.DNSFromDHCP Disabled
racadm set iDRAC.IPv4.DNS1 10.0.0.53
racadm set iDRAC.IPv4.DNS2 10.0.0.54
racadm set iDRAC.NIC.DNSRegister Enabled
racadm set iDRAC.NIC.DNSRacName idrac-rack12-u20
racadm set iDRAC.NIC.DNSDomainFromDHCP Disabled
racadm set iDRAC.NIC.DNSDomainName lab.example.com
```

### Configuring NTP

```bash
racadm set iDRAC.NTPConfigGroup.NTPEnable Enabled
racadm set iDRAC.NTPConfigGroup.NTP1 ntp1.lab.example.com
racadm set iDRAC.NTPConfigGroup.NTP2 ntp2.lab.example.com
racadm set iDRAC.Time.Timezone CST6CDT
```

Confirm exact attribute group and property names for NTP and time zone
against the Attribute Registry for your specific firmware build
(`racadm get iDRAC.NTPConfigGroup -o` and `racadm get iDRAC.Time -o`
enumerate the live, authoritative set on a running unit) — attribute
naming for time-related settings has been one of the more consistently
stable areas across recent iDRAC9 and iDRAC10 releases, but confirming
against the running unit removes any doubt before scripting against it.

### Applying network settings over Redfish

Redfish network configuration is exposed through the `EthernetInterfaces`
resource under the `Manager`:

```bash
curl -s -k -u root:'<password>' -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
        "IPv4StaticAddresses": [
          {"Address": "10.20.30.40", "SubnetMask": "255.255.255.0", "Gateway": "10.20.30.1"}
        ],
        "DHCPv4": {"DHCPEnabled": false}
      }' \
  https://192.168.1.120/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/NIC.1
```

A Python helper that applies a full network baseline in one pass, useful
as the network-bring-up step of a larger provisioning pipeline:

```python
#!/usr/bin/env python3
"""idrac_network_bootstrap.py — apply static IPv4, DNS, and NTP settings
to a freshly racked iDRAC over Redfish, then confirm the settings took
effect.

Usage: python3 idrac_network_bootstrap.py <idrac-ip> <username> <password> \
    <new-static-ip> <netmask> <gateway>
"""
import sys
import time
import requests

requests.packages.urllib3.disable_warnings()


def main() -> None:
    host, user, password, ip, mask, gw = sys.argv[1:7]
    session = requests.Session()
    session.auth = (user, password)
    session.verify = False

    resp = session.patch(
        f"https://{host}/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/NIC.1",
        json={
            "DHCPv4": {"DHCPEnabled": False},
            "IPv4StaticAddresses": [
                {"Address": ip, "SubnetMask": mask, "Gateway": gw}
            ],
        },
        timeout=30,
    )
    resp.raise_for_status()
    print("Network settings submitted; iDRAC will apply and may drop this session.")
    print("Wait 60-120 seconds, then reconnect at the new address to confirm.")


if __name__ == "__main__":
    main()
```

Note that changing the active management IP address is inherently
self-disruptive to the very session making the change — this script
intentionally does not attempt to reconnect and verify at the new address
automatically; reconnect manually or from a separate validation step once
the address change has settled.

## Validation and Troubleshooting

- **No link at all on the expected port.** Confirm NIC selection
  (`racadm get iDRAC.NIC.Selection`) matches the physical port actually
  cabled — this remains the single most common iDRAC network issue,
  especially after a factory reset (Chapter 2), which resets NIC
  selection to its platform default.
- **Link present but no DHCP address obtained.** Confirm VLAN tagging
  configuration matches the upstream switch port's trunk/access
  configuration; a VLAN ID mismatch between iDRAC and the switch port
  causes traffic to be silently dropped rather than producing an explicit
  error on either side.
- **Static address configured but unreachable from a specific subnet.**
  Verify the gateway is correct and that any intermediate firewall
  permits the specific protocols in use (HTTPS, SSH) from the source
  subnet — a common gap is a management-network firewall that allows the
  data center's primary admin subnet but not a newer or secondary jump
  host subnet.
- **DNS registration doesn't appear in the zone.** Confirm
  `iDRAC.NIC.DNSRegister` is enabled and that the target DNS server
  accepts dynamic updates from iDRAC's source address/credentials — many
  enterprise DNS deployments require an explicit allow-list for dynamic
  update sources, which iDRAC's registration attempt does not bypass.
- **Certificate or authentication errors that seem unrelated to
  networking.** Check NTP sync status first
  (`racadm get iDRAC.NTPConfigGroup` and compare iDRAC's reported time
  against a trusted source) — clock drift produces TLS and Kerberos
  (Chapter 4) failures that read as credential or certificate problems
  but are actually time problems.
- **IPv6 address never appears despite `AutoConfig Enabled`.** Confirm the
  upstream network segment actually advertises IPv6 router
  advertisements (RAs); iDRAC's SLAAC behavior depends entirely on the
  network providing them, and a network with IPv6 enabled at the switch
  but no RA-issuing router will never produce an address this way.

## Security and Best Practices

- Isolate the iDRAC management network — whether via dedicated NIC or
  VLAN-tagged shared LOM — from general production and user-facing
  networks with explicit firewall rules, not implicit trust based on
  physical topology.
- Disable IPv6 explicitly if it is not part of your management strategy,
  rather than leaving it enabled-but-unmanaged; an unmanaged access path
  is a governance gap even if no immediate exploit is known against it.
- Restrict which source subnets can reach iDRAC's management ports at the
  firewall, and treat that allow-list with the same change control as any
  other security boundary — the management network is a high-value
  target precisely because of what it can do to every server behind it.
- Use authenticated, access-controlled DNS dynamic update sources rather
  than an open-update zone, since an iDRAC hostname pointed at the wrong
  address by a spoofed update is a credible attack path in an
  insufficiently hardened DNS environment.
- Standardize on internal, monitored NTP sources for iDRAC time sync
  rather than public internet NTP pools where policy allows, so time
  infrastructure availability isn't a dependency on external network
  reachability for a security-relevant control.

## References and Knowledge Checks

**References**

- Dell Technologies, *iDRAC9/iDRAC10 User's Guide* — Network settings
  chapter (NIC selection, VLAN, IPv4/IPv6, DNS)
- Dell Technologies, *iDRAC RACADM CLI Guide* — `iDRAC.NIC`, `iDRAC.IPv4`,
  `iDRAC.IPv6`, and `iDRAC.NTPConfigGroup` attribute groups
- Dell Technologies, *iDRAC Redfish API Guide* — `EthernetInterfaces`
  resource
- `SOFTWARE_VERSIONS.md` in this repository for the dated iDRAC9/iDRAC10
  baseline

**Knowledge Checks**

1. What is the architectural difference between dedicated NIC and shared
   LOM, and what does VLAN tagging restore when shared LOM is chosen?
2. Why does NIC failover change how you should interpret "which port is
   iDRAC currently on"?
3. Why are DNS and NTP treated as prerequisites for later chapters rather
   than independent, optional conveniences?
4. What is the most common root cause of "no link" or "no DHCP address"
   symptoms immediately after a factory reset?
5. Why does an IPv6 address sometimes fail to appear even when
   `AutoConfig` is enabled on iDRAC?

## Hands-On Lab

**Objective:** Configure static IPv4 addressing, VLAN tagging (if your lab
switch supports it), DNS registration, and NTP on a lab iDRAC, then
validate connectivity and time synchronization from both RACADM and
Redfish.

**Prerequisites**

- The lab iDRAC configured in Chapters 1 and 2, with the SCP baseline
  exported in Chapter 2's lab retained for rollback.
- A lab network segment with a known-good static IP range, a reachable
  DNS server accepting dynamic updates (or write access to a test zone),
  and a reachable NTP server.
- Optionally, a lab switch port configurable as an 802.1Q trunk, to
  exercise the VLAN tagging step; skip that step if unavailable and note
  it as skipped.
- An SSH client and `curl`.

**Steps**

1. Confirm current NIC selection and IPv4 addressing mode:

   ```bash
   racadm get iDRAC.NIC.Selection
   racadm get iDRAC.IPv4
   ```

2. Change to a static IPv4 address within your lab's designated static
   range:

   ```bash
   racadm set iDRAC.IPv4.DHCPEnable Disabled
   racadm set iDRAC.IPv4.Address 10.20.30.40
   racadm set iDRAC.IPv4.Netmask 255.255.255.0
   racadm set iDRAC.IPv4.Gateway 10.20.30.1
   ```

   **Expected result:** your current session drops as the address changes;
   reconnect at `10.20.30.40` to confirm the new address is active.
3. Configure DNS registration:

   ```bash
   racadm set iDRAC.NIC.DNSRegister Enabled
   racadm set iDRAC.NIC.DNSRacName idrac-lab-01
   racadm set iDRAC.NIC.DNSDomainFromDHCP Disabled
   racadm set iDRAC.NIC.DNSDomainName lab.example.com
   ```

   **Expected result:** within a few minutes, `idrac-lab-01.lab.example.com`
   resolves to `10.20.30.40` from your workstation
   (`dig idrac-lab-01.lab.example.com` or `nslookup`).
4. Configure NTP:

   ```bash
   racadm set iDRAC.NTPConfigGroup.NTPEnable Enabled
   racadm set iDRAC.NTPConfigGroup.NTP1 <your-lab-ntp-server>
   ```

   **Expected result:** `racadm get iDRAC.NTPConfigGroup` shows
   `NTPEnable` as `Enabled` and your NTP server recorded; allow a few
   minutes, then confirm iDRAC's reported time (visible on the GUI
   dashboard or via `racadm get iDRAC.Time`) matches current time within a
   few seconds.
5. If your lab switch port supports trunking, tag iDRAC traffic onto a
   test VLAN:

   ```bash
   racadm set iDRAC.NIC.VLanEnable Enabled
   racadm set iDRAC.NIC.VLanID 200
   ```

   **Expected result:** if the switch port is correctly configured as a
   trunk carrying VLAN 200, connectivity is retained (possibly requiring
   your workstation to also reach VLAN 200); if the switch port is not so
   configured, connectivity is lost, demonstrating the tagging/trunk
   dependency described in this chapter. Revert with
   `racadm set iDRAC.NIC.VLanEnable Disabled` if connectivity is lost and
   you need to recover.
6. Validate the full network state over Redfish:

   ```bash
   curl -s -k -u root:'<password>' \
     https://10.20.30.40/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/NIC.1 \
     | python3 -m json.tool
   ```

   **Expected result:** the response confirms the static IPv4 address,
   subnet mask, and gateway configured in step 2.
7. **Negative test:** intentionally set an incorrect gateway and confirm
   the effect is scoped to routed (off-subnet) reachability rather than
   local-subnet reachability:

   ```bash
   racadm set iDRAC.IPv4.Gateway 10.20.30.254
   ```

   **Expected result:** the iDRAC remains reachable from your workstation
   if it is on the same local subnet/VLAN, but any test from a different
   subnet (or a `traceroute`/`tracert` from your workstation if routed)
   shows failure, isolating the fault to the deliberately wrong gateway.
   Restore the correct gateway afterward:
   `racadm set iDRAC.IPv4.Gateway 10.20.30.1`.

**Cleanup**

- If continuing to later chapters' labs, leave the static IP, DNS
  registration, and NTP configuration in place — Chapter 4 builds on a
  network-reachable, time-synchronized baseline.
- If this lab environment is shared or temporary, restore the SCP
  baseline exported in Chapter 2 to return to prior network settings:

  ```bash
  racadm systemconfig import -t xml -f lab-baseline.xml \
    -l //<share-ip>/scp-share -u <svc-user> -p '<password>' \
    --target idrac
  ```

## Summary and Completion Checklist

This chapter covered the full management-network configuration surface:
choosing between dedicated NIC and shared LOM, VLAN-isolating shared-LOM
traffic, configuring static and DHCP-based IPv4 and IPv6 addressing, DNS
registration and resolution, and NTP time synchronization — establishing
why DNS and NTP in particular are prerequisites for the certificate and
logging work in later chapters rather than optional conveniences. The lab
produced a network-reachable, DNS-registered, time-synchronized iDRAC
ready for the identity, certificate, and security configuration in
Chapter 4.

- [ ] I can choose between dedicated NIC and shared LOM and explain the
      trade-offs, including when VLAN tagging is necessary.
- [ ] I can configure static and DHCP-based IPv4 and IPv6 addressing on
      iDRAC.
- [ ] I can configure DNS registration/resolution and NTP, and explain why
      both matter beyond basic connectivity.
- [ ] I diagnosed at least one connectivity issue using the RACADM/Redfish
      checks in this chapter's Validation and Troubleshooting section.
- [ ] I have a network-reachable, DNS-registered, time-synchronized lab
      iDRAC ready for Chapter 4.
