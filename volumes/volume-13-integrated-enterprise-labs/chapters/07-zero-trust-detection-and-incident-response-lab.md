# Chapter 07: Zero Trust, Detection, and Incident Response Lab

![Lab topology for this chapter: 802.1X and RADIUS authenticate access-switch ports, and a default-deny ACL between the user and core-services VLANs blocks an RDP probe while Kerberos authentication still succeeds. A SIEM ingests logs from every system built so far and runs a Kerberos pre-authentication brute-force detection rule tuned above the measured baseline. As a negative test, an attacker host on the user VLAN runs 15 rapid Kerberos pre-authentication attempts; the SIEM raises an alert naming the attacker's address within the rule's evaluation window. Containment shuts the attacker's switch port, immediately cutting all connectivity; eradication confirms no lateral movement occurred before the attacker host is removed from the network entirely.](../../../diagrams/volume-13-integrated-enterprise-labs/chapter-07-zero-trust-incident-response-topology.svg)

*Figure 7-1. Topology used throughout this chapter's Hands-On Lab: 802.1X and default-deny microsegmentation paired with SIEM detection, exercised through a full detect-contain-eradicate-recover cycle.*

## Learning Objectives

- Implement microsegmentation between the HQ user and core-services VLANs
  using an explicit allow-list, replacing the implicit trust the network
  has carried since [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md).
- Deploy 802.1X port authentication backed by the directory from Chapter
  02, and a SIEM that ingests telemetry from every system built so far.
- Write and tune a detection rule for a specific attack pattern rather
  than relying on a vendor default.
- Execute a full incident-response cycle — detect, contain, eradicate,
  recover — against a simulated intrusion, producing a defensible evidence
  timeline.
- Explain why containment through this chapter's segmentation model does
  not depend on the compromised host cooperating.

## Theory and Architecture

Every chapter so far has trusted the network to carry traffic wherever it
was addressed. This chapter removes that assumption, following [Volume X](../../volume-10-enterprise-cybersecurity/README.md)
(Enterprise Cybersecurity): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) (Enterprise Identity, Zero Trust,
and Privileged Access) for the segmentation and authentication model,
[Chapter 04](04-virtualization-storage-and-data-protection-lab.md) (Network Security Architecture and Infrastructure Defense) for
enforcing it on the Cisco infrastructure [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) built, [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md)
(Security Telemetry, Detection Engineering, and SOC Operations) for the
SIEM and detection rule this chapter deploys as `siem01`, and Chapter 07
(Cybersecurity Incident Response and Digital Evidence) for the response
process this chapter's negative test exercises directly.

The access-control piece draws specifically on [Volume III, Chapter 07](../../volume-03-cisco-enterprise-networking/chapters/07-cisco-identity-access-control-and-segmentation.md)
(Cisco Identity, Access Control, and Segmentation): 802.1X port
authentication against the directory [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) built, combined with VLAN
access control lists on the core switches from [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md), so that a host
must both authenticate to join a VLAN and stay within that VLAN's explicit
allow-list once connected. Neither control alone is zero trust; together
they mean a device cannot reach `corp.meridian.example`'s core services
merely by being physically plugged into a switch port on the right VLAN.

This chapter's evidence discipline is not new — it reuses `evidence.sh`
from [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) — but the stakes are different. An incident timeline
assembled after the fact from memory is not defensible; one assembled from
timestamped, checksummed command output during the response is.

### Systems introduced in this chapter

| Hostname | Role | Address |
| --- | --- | --- |
| `siem01` | SIEM and log aggregation | `10.13.99.11` |
| `atk01` | Attacker-simulation host (isolated by default) | `10.13.20.99` |

`dc01` gains a Network Policy Server (RADIUS) role in this chapter,
serving 802.1X authentication requests from the core switches — no new
host is required for it.

## Design Considerations

- **Deny-by-default between VLANs, not a blocklist.** The VLAN ACL between
  110 (core services) and 120 (user/endpoint) permits only the specific
  ports [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)'s services require (DNS 53, Kerberos 88, LDAP 389/636)
  and denies everything else, rather than blocking a list of known-bad
  ports. A blocklist only stops attacks someone already anticipated; a
  default-deny allow-list stops everything not explicitly justified.
- **802.1X authenticates the port, ACLs authorize the traffic.** These are
  deliberately two separate controls at two separate layers. An attacker
  who defeats 802.1X (for example, by cloning a MAC address) still faces
  the VLAN ACL; an attacker already on an authenticated port still cannot
  reach ports the ACL does not permit.
- **The attacker host starts isolated, not on the production VLAN.**
  `atk01` is provisioned on a dedicated, non-routed segment and only
  attached to VLAN 120 deliberately, for the duration of the negative
  test, then removed — a permanent "attacker" VM on a live VLAN is a
  standing risk this design does not accept even in a lab.
- **Detection rule is written for this environment's baseline, not
  imported wholesale.** A generic "brute force" rule tuned for a
  high-traffic production SOC would either miss this lab's much lower
  authentication volume or fire on normal patching-window activity. This
  chapter's rule threshold is derived from `dc01`/`dc02`'s actual baseline
  authentication rate, established before the detection rule is trusted.
- **Containment must not depend on attacker cooperation.** The chosen
  containment mechanism — administratively shutting the switch port
  `atk01` is connected to — works regardless of whether the compromised
  host's own agent or operating system is still responsive, unlike a
  purely host-based containment action.

## Implementation and Automation

Configure 802.1X on the access switch port(s) serving VLAN 120, with
`dc01` as the RADIUS server:

```text
! sw-acc01
aaa new-model
aaa authentication dot1x default group radius
radius server DC01
 address ipv4 10.13.10.11 auth-port 1812 acct-port 1813
 key <RADIUS_SHARED_SECRET>
interface GigabitEthernet1/0/10
 switchport mode access
 switchport access vlan 120
 authentication port-control auto
 dot1x pae authenticator
```

Apply the default-deny VLAN ACL between core services and user VLANs on
`sw-core01`/`sw-core02`:

```text
ip access-list extended VLAN120-TO-VLAN110
 permit udp 10.13.20.0 0.0.0.255 host 10.13.10.11 eq 53
 permit udp 10.13.20.0 0.0.0.255 host 10.13.10.12 eq 53
 permit tcp 10.13.20.0 0.0.0.255 host 10.13.10.11 eq 88
 permit tcp 10.13.20.0 0.0.0.255 host 10.13.10.11 eq 389
 permit tcp 10.13.20.0 0.0.0.255 host 10.13.10.11 eq 636
 deny   ip 10.13.20.0 0.0.0.255 10.13.10.0 0.0.0.255 log
 permit ip any any
interface Vlan120
 ip access-group VLAN120-TO-VLAN110 in
```

Deploy `siem01` and configure log forwarding from the systems built so
far: Windows Event Forwarding from `dc01`/`dc02`, syslog from
`sw-core01`, `sw-core02`, and `rtr-hq01`, and `rsyslog`/agent-based
forwarding from `ctrl01` and `linux01`.

Write the tuned detection rule for a Kerberos pre-authentication brute
force:

```yaml
# siem01 detection rule
rule: kerberos-preauth-bruteforce
condition: >
  event.code == 4771 AND
  count(event.target_account, window=5m) > 8
  # baseline observed peak: 2 failures/5m during normal operation
severity: high
action: alert
```

## Validation and Troubleshooting

- **802.1X and RADIUS.** `show authentication sessions interface
  GigabitEthernet1/0/10` on `sw-acc01` must show `Authz Success` for a
  legitimate domain-joined client; a client stuck in `Running` typically
  indicates the RADIUS shared secret does not match between the switch and
  `dc01`'s NPS configuration.
- **VLAN ACL enforcement.** From `linux01` (VLAN 120), confirm permitted
  traffic works (`kinit` still succeeds) and confirm denied traffic is
  actually blocked, not merely unrouted:

  ```bash
  nc -zv -w2 10.13.10.11 3389
  ```

  This must fail (RDP is not in the allow-list), and the switch's ACL
  `log` counter for the deny line must increment.
- **SIEM ingestion.** Before trusting any detection rule, confirm
  `siem01` is actually receiving events from every source — a rule that
  never fires because its data source silently stopped forwarding is a
  much more dangerous failure than a rule that never fires because nothing
  bad happened.
- **Common failure: RADIUS accounting port confusion.** If authentication
  succeeds but session accounting data never appears on `dc01`'s NPS
  logs, confirm UDP 1813 (accounting), not just 1812 (authentication), is
  open through any intervening ACL — the two are easy to conflate when
  troubleshooting under time pressure.
- **Common failure: detection rule threshold too low for legitimate
  activity.** If the rule fires during a routine password-expiry event
  (many users re-authenticating in a short window), the baseline
  measurement in Design Considerations was taken during an unrepresentative
  period — re-baseline and adjust the threshold rather than disabling the
  rule.

## Security and Best Practices

- Treat the VLAN ACL deny-log line as a detection source in its own right;
  feed it into `siem01` alongside the Kerberos rule so blocked lateral
  movement attempts are visible, not just successful ones.
- Store the RADIUS shared secret in `vault01` ([Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md)), referenced by
  the switch configuration management job rather than typed once and
  forgotten in a running configuration.
- Require multi-person authorization before disabling the VLAN ACL or the
  802.1X requirement for any troubleshooting purpose, and set a hard
  expiration on any temporary exception — a "temporary" segmentation
  bypass left in place is a permanent one.
- Apply the same chain-of-custody discipline to every artifact captured
  during the incident-response exercise in this chapter's lab as [Volume X](../../volume-10-enterprise-cybersecurity/README.md),
  Chapter 07 requires for a real incident: who captured it, when, and its
  checksum, all of which `evidence.sh` already provides.
- Review and update the detection rule's threshold on a defined interval,
  not only when it is observed to misfire — a static rule silently
  drifts out of tune as the environment's baseline traffic changes.

## References and Knowledge Checks

**References**

- [RFC 3579](https://www.rfc-editor.org/rfc/rfc3579) — *RADIUS Support for Extensible Authentication Protocol
  (EAP)*.
- [IEEE 802.1X](https://1.ieee802.org/security/802-1x/) — Port-Based Network Access Control.
- [Volume III, Chapter 07](../../volume-03-cisco-enterprise-networking/chapters/07-cisco-identity-access-control-and-segmentation.md) — Cisco Identity, Access Control, and
  Segmentation.
- [Volume X](../../volume-10-enterprise-cybersecurity/README.md), Chapters 02, 04, 06–07 — zero trust/privileged access, network
  security architecture, security telemetry/detection engineering, and
  incident response/digital evidence.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Cisco IOS XE
  17.x baseline used for the switch configuration in this chapter.

**Knowledge checks**

1. Why are 802.1X authentication and the VLAN ACL treated as two separate
   controls rather than one combined mechanism?
2. What specifically makes shutting the switch port a more reliable
   containment action than a host-based agent command?
3. Why was the detection rule's threshold derived from this environment's
   own baseline instead of a generic industry default?
4. What does a VLAN ACL's `deny ... log` line provide that a plain `deny`
   without logging does not, in the context of this chapter's SIEM?

## Hands-On Lab

**Objective:** Deploy 802.1X and default-deny microsegmentation between
HQ's user and core-services VLANs, stand up `siem01` with a tuned
detection rule, then run a full detect-contain-eradicate-recover cycle
against a simulated intrusion.

**Prerequisites**

- [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) complete, with the automation pipeline and `vault01`
  available for secret storage.
- A RADIUS-capable directory role (Windows NPS on `dc01`) and 802.1X
  support on the access switch from [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md).
- Familiarity with basic offensive tooling for controlled lab use only
  (this chapter simulates an attack against infrastructure you own; never
  point these techniques at anything outside this lab).

**Steps**

1. Restore or confirm the `ch06-baseline` state.

2. Configure the NPS/RADIUS role on `dc01` and 802.1X on `sw-acc01`'s
   client-facing ports per Implementation and Automation. Confirm
   `linux01` still authenticates successfully to the network port before
   proceeding.

3. Apply the default-deny VLAN ACL between VLAN 120 and VLAN 110 on
   `sw-core01`/`sw-core02`.

4. **Expected result — ACL enforcement.**

   ```bash
   ./evidence.sh "nc -zv -w2 10.13.10.11 3389 || true"
   ./evidence.sh "kinit svc-domainjoin"
   ```

   The RDP probe must fail; Kerberos authentication must still succeed.

5. Deploy `siem01`, configure log forwarding from `dc01`, `dc02`,
   `sw-core01`, `sw-core02`, `rtr-hq01`, `ctrl01`, and `linux01`.

6. Measure the baseline Kerberos authentication failure rate over a
   representative period, then deploy the detection rule from
   Implementation and Automation with a threshold above that baseline.

7. **Expected result — telemetry flowing.**

   ```bash
   ./evidence.sh "curl -s http://siem01:9200/_cat/indices?v | grep -E 'winlog|syslog'"
   ```

   Indices for both Windows and syslog sources must show recent event
   counts greater than zero.

8. Take a snapshot of `siem01`'s rule configuration and the switch/RADIUS
   configuration state, labeled `ch07-baseline`.

9. Provision `atk01` on its isolated segment, then attach it to VLAN 120
   for the negative test only.

10. **Negative test:** From `atk01`, simulate a Kerberos pre-authentication
    brute-force attempt against `dc01`:

    ```bash
    ./evidence.sh "for i in $(seq 1 15); do \
      kinit baduser@CORP.MERIDIAN.EXAMPLE 2>/dev/null; done || true"
    ```

    **Expected result — detection.** Within the rule's evaluation window,
    `siem01` raises a `kerberos-preauth-bruteforce` alert naming `atk01`'s
    address and the targeted account pattern:

    ```bash
    ./evidence.sh "curl -s http://siem01:9200/alerts/_search?q=rule:kerberos-preauth-bruteforce"
    ```

11. **Contain:** Administratively shut the switch port `atk01` is
    connected to:

    ```bash
    ./evidence.sh "ssh admin@sw-acc01 'interface GigabitEthernet1/0/15 ; shutdown'"
    ```

    **Expected result:** `atk01` immediately loses all network
    connectivity, including any connection an attacker might already have
    established — confirm with a failed ping from `ctrl01` to `atk01`.

12. **Eradicate and recover:** Confirm no lateral movement succeeded
    (`repadmin /replsummary` on `dc01`/`dc02` shows no unexpected changes,
    no new domain accounts were created), then remove `atk01` from the
    network entirely rather than merely leaving its port shut down.

13. Assemble the incident timeline from the evidence captured in steps
    10–12, in `~/lab-evidence/manifest.sha256` order, as the deliverable
    for this exercise.

14. **Cleanup:** Decommission `atk01` (delete the VM; it has no ongoing
    purpose in this volume). Re-enable the switch port for future use.
    Retain `siem01`, the 802.1X configuration, and the VLAN ACL for
    [Chapter 08](08-observability-operations-and-major-incident-lab.md). Commit the updated topology and detection rule:

    ```bash
    cd ~/vol13-lab
    git add topology.yml
    git commit -m "Chapter 07: zero trust, detection, and incident response"
    ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter replaced implicit VLAN trust with 802.1X authentication and a
default-deny allow-list, then proved the design with a real detection and
containment cycle rather than a tabletop description of one. The
detection rule fired on baseline-derived thresholds, containment worked
without depending on the compromised host's cooperation, and the resulting
evidence timeline is the kind of artifact [Volume X, Chapter 07](../../volume-10-enterprise-cybersecurity/chapters/07-cybersecurity-incident-response-and-digital-evidence.md) expects
from a defensible incident response.

- [ ] Deployed 802.1X port authentication backed by the [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)
      directory.
- [ ] Applied and validated a default-deny VLAN ACL between core services
      and user VLANs.
- [ ] Deployed `siem01` with verified telemetry ingestion from every
      system built so far.
- [ ] Tuned and validated a detection rule against this environment's own
      baseline.
- [ ] Completed the full detect-contain-eradicate-recover cycle and
      assembled a timestamped incident timeline.
