# Chapter 04: Network Security Architecture and Infrastructure Defense

![Lab topology for this chapter: lab-segmentation.nft implements a default-drop inbound chain allowing only established/related traffic, loopback, TCP 22, and TCP 443, logging every other drop with prefix SEG-DENY; from a second host, a request to the permitted port succeeds. As a negative test, a request to an unlisted port times out or is refused, and dmesg shows the SEG-DENY log entry. Separately, the CI policy validator passes cleanly against a compliant policy but fails with 'no explicit default-deny egress rule' and a nonzero exit against a broken policy missing that rule — the same fail-closed CI gate pattern used for the OSCAP remediation review.](../../../diagrams/volume-010-enterprise-cybersecurity/chapter-04-nftables-segmentation-ci-validator-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: an nftables default-drop segmentation policy validated by permitted and denied connectivity, plus a CI policy check catching a missing default-deny rule.*

## Learning Objectives

- Explain how network security architecture has shifted from a
  perimeter-centric model to segmentation- and identity-aware defense in
  depth, and how that shift relates to the Zero Trust model from [Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md).
- Design network segmentation and microsegmentation strategies that limit
  east-west movement, not just north-south perimeter crossing.
- Compare next-generation firewall (NGFW), intrusion detection/prevention
  (IDS/IPS), and secure remote access (VPN vs. ZTNA) technologies and place
  each correctly in a layered architecture.
- Evaluate DNS security, DDoS protection, and SASE/SSE as complementary
  infrastructure-defense controls rather than substitutes for
  segmentation.
- Represent firewall and segmentation policy as version-controlled,
  reviewable configuration.
- Build and test a working host-based segmentation policy, including a
  negative test that proves a denied path is actually blocked.

## Theory and Architecture

### From perimeter to segmented, identity-aware defense

Classic enterprise network security assumed a hardened perimeter (a
firewall at the internet edge) protecting an implicitly trusted internal
network. That model fails against three realities of modern enterprise
environments: users and workloads routinely operate outside any single
perimeter (SaaS, remote work, multi-cloud), a single compromised host
inside the perimeter historically had broad reach to everything else
inside it, and encrypted traffic dominates both north-south (client-to-
server, crossing the perimeter) and east-west (server-to-server, internal)
flows, limiting what a perimeter device alone can inspect.

Network security architecture today layers three distinct control planes
on top of each other:

- **Perimeter controls** — the traditional edge: NGFW, DDoS scrubbing, DNS
  filtering, and secure remote access, governing north-south traffic
  between the enterprise and the internet.
- **Segmentation controls** — internal zone and microsegmentation
  boundaries that govern east-west traffic between workloads, independent
  of whether traffic ever crosses the perimeter.
- **Identity-aware enforcement** — the Policy Enforcement Point (PEP)
  pattern from [Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)'s Zero Trust Architecture discussion, applied at
  the network layer so that access decisions depend on verified identity
  and device posture, not just source IP and port.

None of these three planes replaces the others. A well-designed
architecture assumes the perimeter will eventually be crossed (via
phishing, a vulnerable internet-facing service, or a compromised
credential) and relies on segmentation and identity-aware enforcement to
contain the resulting blast radius — the same defense-in-depth principle
introduced in [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md), applied specifically to network infrastructure.

### Segmentation and microsegmentation

- **Zone-based segmentation** groups systems of similar trust and function
  (DMZ, internal user network, server/data-center network, OT/ICS network,
  management network) and enforces policy at the boundary between zones,
  typically with VLANs and a firewall or routing ACL at each boundary.
  Zone segmentation is coarse-grained: it stops lateral movement between
  zones but does nothing to stop movement between two hosts inside the
  same zone.
- **Microsegmentation** enforces policy between individual workloads or
  small workload groups, independent of network topology — commonly
  implemented with software-defined networking overlays, hypervisor-level
  distributed firewalls, or host-based policy agents. A compromised
  application server in a microsegmented data center can be restricted to
  only the specific ports and destination workloads its function requires
  (for example, only outbound `5432/tcp` to its specific database
  instance), even though it shares a subnet with dozens of unrelated
  hosts.
- **East-west vs. north-south enforcement.** Most legacy security
  investment concentrated on north-south (perimeter) inspection because
  that is where volumetric, internet-sourced threats appear. Ransomware
  and business-email-compromise incidents, however, spread primarily
  east-west after an initial foothold — which is why microsegmentation and
  internal traffic visibility have become as important as perimeter
  hardening, not a secondary concern.

### Next-generation firewalls and intrusion detection/prevention

**Next-generation firewalls (NGFW)** extend stateful packet inspection
with application awareness (identifying the actual application generating
traffic regardless of port), user awareness (binding policy to identity,
not just IP address, by integrating with the identity provider from
[Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)), and integrated intrusion prevention. This lets policy be
expressed as "allow the finance application group to reach the payment
processing API," which is both more precise and more auditable than a
port/protocol rule.

**Intrusion detection and prevention systems (IDS/IPS)** inspect traffic
for known-malicious patterns and protocol anomalies:

- **Signature-based detection** matches traffic against a database of
  known attack patterns — high precision against known threats, blind to
  novel ones.
- **Anomaly-based detection** models expected traffic behavior and flags
  deviations — can catch novel threats but requires tuning to avoid excess
  false positives.
- **Inline (IPS) vs. out-of-band (IDS) deployment.** Inline placement
  (in the traffic path) enables active blocking but adds latency and a
  failure point; out-of-band placement (fed by a SPAN port or network tap)
  only alerts, adding no latency or path risk, but cannot block in real
  time. Many architectures deploy IPS inline at chokepoints that justify
  the risk (perimeter, segmentation boundaries to sensitive zones) and IDS
  out-of-band elsewhere for broad visibility without inline risk.

### Secure remote access: VPN and ZTNA

Traditional remote-access VPN grants a connecting device an IP address on
(or routed into) the internal network, implicitly trusting it to reach
whatever that network segment permits — the same implicit-trust weakness
Zero Trust Architecture exists to eliminate. **Zero Trust Network Access
(ZTNA)** replaces network-level trust with per-application, identity- and
posture-verified access brokered by a proxy: the user authenticates
through the identity provider (with the conditional access and
phishing-resistant MFA controls from [Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)), and the ZTNA broker
grants a connection to the *specific application* requested, never placing
the client device onto the internal network itself. This is the
Policy Enforcement Point pattern applied to remote access: the ZTNA broker
is the PEP, and the identity provider's conditional access engine is the
Policy Engine.

VPN is not obsolete — site-to-site VPN remains standard for connecting
data centers, cloud VPCs, and branch offices — but user-facing remote
access is migrating toward ZTNA specifically because it eliminates the
network-level blast radius a compromised remote-access client historically
carried.

### DNS security and DDoS protection

- **DNS security** operates at a chokepoint nearly every attack technique
  eventually touches: command-and-control resolution, phishing domains,
  and data exfiltration via DNS tunneling all depend on DNS resolution.
  Protective DNS (filtering resolution against known-malicious domain
  reputation), DNSSEC (cryptographically validating DNS response
  integrity against spoofing), and DNS query logging (feeding the
  detection pipeline in [Chapter 6](06-security-telemetry-detection-engineering-and-soc-operations.md)) are complementary, not redundant,
  controls.
- **DDoS protection** distinguishes volumetric attacks (overwhelming
  network capacity, mitigated by upstream scrubbing and anycast
  distribution) from application-layer attacks (exhausting application
  resources with seemingly valid requests, mitigated by rate limiting, bot
  management, and NGFW/WAF-layer controls). Enterprises with
  internet-facing services typically contract upstream DDoS scrubbing
  capacity sized well beyond their own link capacity, since a volumetric
  attack targets the link itself, not just the destination server.

### SASE and SSE: converging network and security at the edge

**Secure Access Service Edge (SASE)** converges SD-WAN networking with a
cloud-delivered security stack — secure web gateway, cloud access security
broker (CASB), ZTNA, and firewall-as-a-service — into a single,
identity-aware edge enforced close to the user rather than backhauled
through a data center. **Security Service Edge (SSE)** is the
security-only subset of SASE for organizations that already have a
networking strategy and want the security stack without the SD-WAN
component. Both patterns exist because a workforce that is majority
remote/hybrid and majority SaaS-consuming makes the traditional
data-center-centric perimeter an increasingly poor enforcement point:
policy needs to travel with the user and the request, not wait for traffic
to reach a fixed location.

## Design Considerations

- **Segmentation granularity vs. operational complexity.** Fine-grained
  microsegmentation minimizes blast radius but multiplies the number of
  policies to author, test, and maintain. Start with coarse zone
  segmentation for all environments, then apply microsegmentation
  selectively to the highest-value zones (data-center application tiers,
  payment processing, OT/ICS) rather than attempting uniform
  microsegmentation everywhere on day one.
- **TLS inspection trade-offs.** Decrypting and inspecting TLS traffic at
  the NGFW gives visibility into threats that would otherwise be invisible
  in encrypted payloads, but it requires distributing a trusted
  interception certificate to every managed endpoint, adds latency, and
  raises privacy and compliance questions for certain traffic categories
  (healthcare, personal banking). Scope TLS inspection deliberately —
  many organizations exempt defined categories rather than inspecting all
  traffic universally — and document the exemption list as a reviewed
  policy, not an ad hoc exclusion.
- **VPN-to-ZTNA migration is incremental, not a cutover.** Most
  enterprises run VPN and ZTNA in parallel for an extended period,
  migrating application-by-application. Prioritize migrating access to the
  highest-risk applications (admin consoles, financial systems) first,
  since those carry the most benefit from eliminating network-level trust.
- **Inline IPS placement risk.** Every inline device is a potential
  availability failure point and a chokepoint for encrypted-traffic
  inspection cost. Reserve inline blocking for chokepoints where the
  security benefit clearly outweighs the availability risk, and design
  fail-open vs. fail-closed behavior deliberately per zone — a fail-closed
  posture in front of a life-safety OT system, for example, may be the
  wrong default.
- **East-west visibility is commonly the biggest blind spot.** Enterprises
  that have invested heavily in perimeter NGFW and DDoS protection often
  have far weaker visibility into internal, encrypted, server-to-server
  traffic. When budgeting network security investment, explicitly assess
  east-west telemetry coverage (NetFlow/IPFIX export, microsegmentation
  logging) rather than assuming perimeter coverage implies internal
  coverage.
- **DDoS scrubbing capacity sizing** should be based on the largest
  plausible attack against the organization's public profile (industry
  sector, prior incident history), not the organization's own peak
  legitimate traffic — the two are unrelated numbers.

## Implementation and Automation

### Firewall and segmentation policy as code

Represent segmentation policy as structured, version-controlled data so it
can be peer-reviewed and validated in CI before deployment, following the
same pattern used for the control crosswalk in [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md):

```yaml
# segmentation/payment-processing-zone.yaml
zone: payment-processing
default_action: deny
rules:
  - id: seg-pp-001
    description: "App tier may reach payment DB on Postgres port only"
    source: zone.app-tier
    destination: zone.payment-processing
    port: 5432/tcp
    action: allow
  - id: seg-pp-002
    description: "Payment processing zone has no direct internet egress"
    source: zone.payment-processing
    destination: any
    port: any
    action: deny
    log: true
  - id: seg-pp-003
    description: "Break-glass admin access requires PAM broker session (Ch. 2)"
    source: pam-broker.jump-host
    destination: zone.payment-processing
    port: 22/tcp
    action: allow
    require_mfa: true
```

### NGFW application- and identity-aware policy (vendor-neutral pattern)

```text
# Policy intent expressed the way most NGFW management planes model it
rule "finance-app-to-payment-api":
  source_identity_group = "finance-application-service-accounts"
  application = "internal-payment-api"
  action = allow
  log_at_session_end = true

rule "default-deny-app-tier-egress":
  source_zone = "app-tier"
  destination = any
  action = deny
  log = true
```

### IDS/IPS signature tuning (Suricata-style detection rule)

Detection rules describe traffic *patterns to alert on or block*; they are
defensive artifacts, not attack tooling. A tuned rule narrows a broad
category (unexpected outbound DNS-over-HTTPS from a server segment that
should never originate it) to reduce false positives:

```text
alert dns any any -> any 53 (msg:"Possible DNS tunneling - excessive TXT query length"; \
  dns.query; content:"TXT"; pcre:"/^.{100,}$/"; \
  classtype:policy-violation; sid:9000123; rev:2;)

# Narrowed variant scoped only to a segment that should never do this,
# reducing false positives from legitimate long TXT queries elsewhere
alert dns $SERVER_TIER any -> !$AUTHORIZED_DNS_TXT_HOSTS 53 \
  (msg:"Unexpected long TXT query from server tier"; \
  dns.query; pcre:"/^.{100,}$/"; \
  classtype:policy-violation; sid:9000124; rev:1;)
```

### Automated segmentation policy validation in CI

```python
#!/usr/bin/env python3
"""validate_segmentation.py — fail CI if a segmentation policy file
lacks an explicit default-deny rule or defines an unscoped allow-any rule.
"""
import sys
import yaml


def validate(path: str) -> list[str]:
    with open(path, encoding="utf-8") as fh:
        policy = yaml.safe_load(fh)

    errors = []
    rules = policy.get("rules", [])
    has_default_deny = any(
        r["destination"] == "any" and r["action"] == "deny" for r in rules
    )
    if not has_default_deny:
        errors.append(f"{policy['zone']}: no explicit default-deny egress rule")

    for r in rules:
        if r["action"] == "allow" and r.get("port") == "any" and r["source"] == "any":
            errors.append(f"{policy['zone']}: rule {r['id']} is an unscoped allow-any")

    return errors


if __name__ == "__main__":
    problems = validate(sys.argv[1] if len(sys.argv) > 1 else "policy.yaml")
    for p in problems:
        print(f"POLICY ERROR: {p}")
    sys.exit(1 if problems else 0)
```

## Validation and Troubleshooting

- **Validate segmentation with active testing, not policy review alone.**
  A segmentation rule that looks correct on paper can be defeated by
  asymmetric routing, an unmanaged secondary interface, or a
  misconfigured route table. Periodically test enforced boundaries with
  controlled, authorized connectivity checks (from an approved source, to
  an approved destination, logged as a change-managed activity) rather
  than trusting the policy document alone.
- **Common failure: shadow paths around the perimeter.** Direct internet
  circuits provisioned by a business unit outside the managed network
  (a rogue LTE/5G gateway, an unauthorized cloud VPC peering connection)
  bypass every perimeter and segmentation control simultaneously.
  Maintain and periodically reconcile an authoritative network topology
  inventory against discovered egress points ([Chapter 5](05-vulnerability-exposure-and-patch-risk-management.md) covers the
  broader exposure-management discipline this feeds into).
- **Common failure: asymmetric routing breaking stateful inspection.**
  A stateful firewall or IPS that sees only one direction of a
  connection's traffic will drop or fail to properly evaluate it. When
  a segmentation boundary intermittently blocks traffic that should be
  permitted, check routing symmetry before assuming the policy itself is
  wrong.
- **Common failure: TLS inspection certificate errors.** An expired or
  improperly trusted TLS interception certificate produces browser and
  application TLS errors that are easy to misdiagnose as an application
  problem. Confirm interception certificate validity and endpoint trust
  store deployment first when TLS errors appear fleet-wide rather than
  for a single host.
- **Diagnosing IPS false positives**: correlate blocked-session logs
  against the specific signature ID and review whether the traffic
  pattern is legitimate but unusual (a backup job generating large
  sequential transfers, for example) before broadening or disabling a
  signature — a narrowed, scoped exception is preferable to disabling
  detection coverage for an entire signature category.
- **Diagnosing DDoS scrubbing activation gaps**: confirm the trigger
  threshold and time-to-mitigate for the scrubbing provider are documented
  and tested; an untested activation path is a common reason mitigation
  takes far longer than expected during an actual event.

## Security and Best Practices

- Default to deny for every segmentation boundary and log denied traffic;
  an allow-list posture with logged denials gives both containment and
  investigative value.
- Treat firewall and segmentation policy changes as change-managed,
  peer-reviewed configuration, following the same version-control
  discipline as the control crosswalk in [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md) — never apply an
  emergency firewall exception without a tracked expiration and
  retrospective review.
- Prioritize migrating high-risk remote access (administrative consoles,
  financial and identity systems) from VPN to ZTNA first, applying the
  phishing-resistant MFA and conditional access controls from [Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md) at
  the access-broker layer.
- Instrument east-west traffic (NetFlow/IPFIX export, microsegmentation
  logs) with the same rigor as perimeter traffic, and forward both into
  the detection pipeline described in [Chapter 6](06-security-telemetry-detection-engineering-and-soc-operations.md) — a segmentation control
  with no visibility behind it can be bypassed silently.
- Size and test DDoS scrubbing activation before it is needed; an
  untested runbook discovered during a live volumetric attack routinely
  adds significant time to mitigation.
- Scope TLS inspection deliberately, document exemptions, and protect the
  interception CA's private key with the same rigor as any other
  root-of-trust material — compromise of that key would let an attacker
  transparently intercept any inspected session.
- Review firewall and segmentation rule sets on a fixed cadence (at
  minimum semi-annually) to remove stale, overly broad, or unused rules,
  cross-referencing the risk register from [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md) for any documented
  compensating-control exceptions.

## References and Knowledge Checks

**References**

- [NIST SP 800-41 Rev 1, *Guidelines on Firewalls and Firewall Policy*](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
- [NIST SP 800-207, *Zero Trust Architecture*](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-207 companion guidance and CISA, *Zero Trust Maturity
  Model*](https://www.cisa.gov/zero-trust-maturity-model)
- [CISA, *Guidance on Securing DNS and Protective DNS*](https://www.cisa.gov/resources-tools/services/protective-domain-name-system-dns-resolver)
- [MITRE ATT&CK Enterprise, techniques T1071 (Application Layer Protocol)
  and T1071.004 (DNS) as reference points for detection coverage, and
  T1498 (Network Denial of Service) for DDoS-related mitigations](https://attack.mitre.org/)
- [CIS Controls v8.1, Control 12 (Network Infrastructure Management) and
  Control 13 (Network Monitoring and Defense)](https://www.cisecurity.org/controls/v8-1)

**Knowledge Checks**

1. Why does modern network security architecture emphasize
   microsegmentation in addition to perimeter defense rather than
   relying on the perimeter alone?
2. What is the architectural difference between VPN-based remote access
   and ZTNA, and why does ZTNA reduce blast radius after a client
   compromise?
3. When is inline IPS placement justified despite its availability risk,
   and when is out-of-band IDS the better choice?
4. What trade-offs must be weighed before enabling TLS inspection at the
   perimeter?
5. Why is east-west traffic visibility commonly a bigger blind spot than
   north-south visibility in mature enterprises?
6. What distinguishes volumetric DDoS mitigation from application-layer
   DDoS mitigation?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each network-defense skill** — host
firewalling, segmentation and reconnaissance, intrusion detection, and intrusion traffic
analysis — the CyberOps "Network Intrusion Analysis" domain. Every step is runnable. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.4** — a Linux host with `sudo`, `nftables`/`iptables`,
`nmap`, `suricata` (or `snort`), and `tshark`. **Safety:** scan and probe only hosts you own.
**Cost:** none.

### Lab 4.1 — Default-deny host firewall (Topic: Infrastructure defense)

**Objective:** Permit only intended traffic and drop the rest.

```bash
sudo nft add table inet filter 2>/dev/null
sudo nft 'add chain inet filter input { type filter hook input priority 0 ; policy drop ; }'
sudo nft add rule inet filter input ct state established,related accept
sudo nft add rule inet filter input iif lo accept
sudo nft add rule inet filter input tcp dport 22 accept          # allow SSH only
sudo nft list chain inet filter input
```

**Expected result:** the input chain defaults to `drop`, allowing only loopback, established
flows, and SSH — a default-deny firewall inverts the trust model: nothing is allowed unless
explicitly permitted, which is the foundation of network defense at host and perimeter.

**Negative test:** run a default-allow firewall with a few block rules; any service you forget
to block is exposed — default-deny means a forgotten service is closed, not open, which is the
safer failure mode.

**Rollback:** `sudo nft delete table inet filter`.

### Lab 4.2 — Reconnaissance and attack-surface enumeration (Topic: Network analysis)

**Objective:** See your host the way an attacker's scanner does.

```bash
sudo nmap -sS -sV -O -p- 127.0.0.1 2>/dev/null | grep -E "open|OS details" | head
nmap --script vuln 127.0.0.1 2>/dev/null | grep -iE "VULNERABLE|CVE" | head
```

**Expected result:** the open ports, service versions, and any flagged vulnerabilities on the
target — reconnaissance (port/service/OS discovery) is both the attacker's first move and the
defender's attack-surface check; you cannot defend a service you did not know was exposed.

**Negative test:** assume a host only runs what you deployed; a forgotten dev service or default
daemon is listening — scanning reveals the *actual* attack surface, which usually exceeds the
intended one.

**Rollback:** none (read-only scan of your own host).

### Lab 4.3 — Intrusion detection with Suricata (Topic: IDS/IPS)

**Objective:** Alert on a matching signature.

```bash
cd ~ && cat > local.rules <<'EOF'
alert icmp any any -> any any (msg:"ICMP ping detected"; itype:8; sid:1000001; rev:1;)
EOF
sudo suricata -r /usr/share/doc/suricata/*.pcap -S local.rules -l /tmp/suri 2>/dev/null; \
  grep -o '"signature":"[^"]*"' /tmp/suri/eve.json 2>/dev/null | head || \
  echo "(install suricata) rule would alert on matching traffic; alerts land in eve.json"
```

**Expected result:** Suricata raises the signature alert (in `eve.json`) on matching traffic —
an IDS/IPS inspects traffic against signatures and behavioral rules (Suricata/Snort), alerting
(IDS) or blocking (IPS) known-bad patterns; rules encode the threats you watch for.

**Negative test:** rely on the firewall's port rules alone for detection; it permits legitimate
ports but cannot see a malicious payload riding an allowed port — the IDS inspects *content*,
which port filtering does not.

**Rollback:** `rm -f ~/local.rules; sudo rm -rf /tmp/suri`.

### Lab 4.4 — Intrusion traffic analysis (Topic: Network intrusion analysis)

**Objective:** Find a scan or beacon pattern in a capture.

```bash
# Detect a port scan: one source hitting many ports with SYNs
tshark -r capture.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -e ip.src -e tcp.dstport 2>/dev/null | sort | uniq -c | sort -rn | head
# Detect beaconing: regular-interval connections to one destination
tshark -r capture.pcapng -Y "tcp.flags.syn==1" -T fields -e ip.dst 2>/dev/null | sort | uniq -c | sort -rn | head
```

**Expected result:** one source touching many destination ports (a scan) or repeated
connections to one host (a beacon) stand out in the counts — network intrusion analysis reads
captures/flows for attack patterns (scanning, beaconing, exfiltration) that individual packets do
not reveal, which is the SOC's network-side detection skill.

**Negative test:** judge intrusion from a single packet; a scan or beacon is a *pattern* across
many packets — aggregating by source/destination/port over time is what exposes it.

**Rollback:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the network infrastructure defense layer that sits
between platform hardening ([Chapter 3](03-platform-hardening-configuration-and-endpoint-defense.md)) and the identity-aware access
model ([Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)): perimeter controls, internal segmentation and
microsegmentation, NGFW and IDS/IPS placement, the shift from VPN to
ZTNA for remote access, and the complementary roles of DNS security,
DDoS protection, and SASE/SSE. Segmentation and firewall policy were
represented as version-controlled, CI-validated configuration rather than
opaque device state. The hands-on lab enforced a real host-based
segmentation policy, validated both an allowed and a denied path with
evidence in the system log, and exercised an automated policy validator
against a deliberately broken configuration.

- [ ] I can explain why microsegmentation is necessary in addition to
      perimeter defense.
- [ ] I can compare VPN and ZTNA and explain why ZTNA reduces blast
      radius.
- [ ] I can distinguish inline IPS from out-of-band IDS deployment and
      choose correctly based on risk tolerance.
- [ ] I can describe the trade-offs of TLS inspection at the perimeter.
- [ ] I can identify east-west visibility gaps as distinct from
      perimeter visibility gaps.
- [ ] I implemented and tested a host-based segmentation policy in the
      hands-on lab, including a negative test with logged evidence of a
      blocked connection.
