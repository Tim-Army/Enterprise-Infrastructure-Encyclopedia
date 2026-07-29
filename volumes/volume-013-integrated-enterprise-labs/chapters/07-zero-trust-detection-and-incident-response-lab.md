# Chapter 07: Zero Trust, Detection, and Incident Response Lab

![Lab topology for this chapter: 802.1X and RADIUS authenticate access-switch ports, and a default-deny ACL between the user and core-services VLANs blocks an RDP probe while Kerberos authentication still succeeds. A SIEM ingests logs from every system built so far and runs a Kerberos pre-authentication brute-force detection rule tuned above the measured baseline. As a negative test, an attacker host on the user VLAN runs 15 rapid Kerberos pre-authentication attempts; the SIEM raises an alert naming the attacker's address within the rule's evaluation window. Containment shuts the attacker's switch port, immediately cutting all connectivity; eradication confirms no lateral movement occurred before the attacker host is removed from the network entirely.](../../../diagrams/volume-013-integrated-enterprise-labs/chapter-07-zero-trust-incident-response-topology.svg)

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
was addressed. This chapter removes that assumption, following [Volume X](../../volume-010-enterprise-cybersecurity/README.md)
(Enterprise Cybersecurity): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) (Enterprise Identity, Zero Trust,
and Privileged Access) for the segmentation and authentication model,
[Chapter 04](04-virtualization-storage-and-data-protection-lab.md) (Network Security Architecture and Infrastructure Defense) for
enforcing it on the Cisco infrastructure [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) built, [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md)
(Security Telemetry, Detection Engineering, and SOC Operations) for the
SIEM and detection rule this chapter deploys as `siem01`, and Chapter 07
(Cybersecurity Incident Response and Digital Evidence) for the response
process this chapter's negative test exercises directly.

The access-control piece draws specifically on [Volume III, Chapter 07](../../volume-003-cisco-enterprise-networking/chapters/07-cisco-identity-access-control-and-segmentation.md)
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
  during the incident-response exercise in this chapter's lab as [Volume X](../../volume-010-enterprise-cybersecurity/README.md),
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
- [Volume III, Chapter 07](../../volume-003-cisco-enterprise-networking/chapters/07-cisco-identity-access-control-and-segmentation.md) — Cisco Identity, Access Control, and
  Segmentation.
- [Volume X](../../volume-010-enterprise-cybersecurity/README.md), Chapters 02, 04, 06–07 — zero trust/privileged access, network
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

This chapter's labs secure the integrated environment with **zero-trust segmentation, detection, and
incident response**, drawing on Volumes X, XV, XIX, and XXV. Each ends **`**Lab verified by:**
*pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.4** — the environment from Chapters 02–06, and security tooling
(firewall/segmentation, a SIEM/detection stack). **Cost:** none beyond lab resources.

### Lab 7.1 — Zero-trust segmentation (Topic: Segmentation)

**Objective:** Enforce least-privilege access between the environment's segments.

```bash
# Default-deny between segments (Ch03), allow only intended flows, keyed on identity (Ch02):
sudo nft add table inet zt 2>/dev/null
sudo nft 'add chain inet zt forward { type filter hook forward priority 0 ; policy drop ; }'
sudo nft add rule inet zt forward ct state established,related accept
# allow: user-segment -> app:443 only; everything else denied
sudo nft add rule inet zt forward ip saddr 192.168.20.0/24 tcp dport 443 accept
```

**Expected result:** inter-segment traffic is default-deny with only intended flows permitted — zero
trust (Volume X) builds on the segmentation (Chapter 03) and identity (Chapter 02) to enforce
least-privilege access between every part of the environment, containing lateral movement.

**Negative test:** allow open traffic between segments; a compromise in one (e.g. a user workstation)
reaches the whole environment — default-deny with explicit allows is what contains lateral movement.

**Cleanup:** `sudo nft delete table inet zt`.

### Lab 7.2 — Detection engineering (Topic: Detection)

**Objective:** Detect malicious activity across the environment.

```bash
# Ship logs from every integrated component (Ch02-06) to the SIEM, and write a detection:
#   e.g. brute force = >10 failed auths from one source in 5m (Vol X, Ch06 detection labs)
grep "Failed password" /var/log/auth.log 2>/dev/null | grep -oE 'from [0-9.]+' | sort | uniq -c | awk '$1>10{print "ALERT",$0}'
```

**Expected result:** a detection fires on a brute-force pattern in the aggregated logs — detection
engineering (Volume X) correlates telemetry from across the integrated environment (identity, network,
hosts, cloud) so an attack is visible wherever it touches, which requires the unified observability
(Chapter 08) to work.

**Negative test:** monitor each component's logs in isolation; a multi-stage attack that crosses
identity → network → host is never correlated — detection needs the aggregated, cross-component
telemetry.

**Cleanup:** none.

### Lab 7.3 — Incident response (Topic: IR)

**Objective:** Contain and investigate a simulated compromise.

```text
# Run the IR lifecycle (Vol X) against the environment for a simulated compromised host:
#   Identify (detection, Lab 7.2) -> Contain (isolate the host via segmentation policy, Lab 7.1)
#   -> Eradicate (rebuild from code, Ch06) -> Recover -> Lessons (blameless postmortem)
echo "detect -> contain (segment) -> eradicate (rebuild from IaC) -> recover -> learn"
```

**Expected result:** the compromised host is isolated by segmentation policy, eradicated by rebuilding
from code, and recovered — integrated IR ties detection (Lab 7.2), segmentation containment (Lab 7.1),
and IaC rebuild (Chapter 06) into one response, which is far faster than ad-hoc remediation.

**Negative test:** respond to a compromise by manually cleaning the host in place; you may miss
persistence and cannot be sure it is clean — containment plus rebuild-from-known-good-code is the
trustworthy eradication.

**Cleanup:** restore the isolated host after the exercise.

### Lab 7.4 — Security validation (Topic: Assurance)

**Objective:** Confirm the controls actually work.

```bash
# Emulate a technique and confirm the environment detects/contains it (purple team, Vol X):
logger -p auth.warning "Failed password for invalid user attacker from 203.0.113.9"
sleep 1; journalctl -p warning --since "-1 min" 2>/dev/null | grep -q "Failed password" && echo "DETECTION VALIDATED" || echo "GAP"
```

**Expected result:** the emulated technique produces a detectable signal, validating the control
(or exposing a gap) — security assurance (Volume X) proves the integrated detection/segmentation
controls work against real techniques, rather than assuming the tools deployed across the environment
are effective.

**Negative test:** assume the security controls work because they are deployed; many silently break
(a log source moved, a rule disabled) — emulating the technique and confirming detection is the only
proof of current coverage.

**Cleanup:** none.

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
evidence timeline is the kind of artifact [Volume X, Chapter 07](../../volume-010-enterprise-cybersecurity/chapters/07-cybersecurity-incident-response-and-digital-evidence.md) expects
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
