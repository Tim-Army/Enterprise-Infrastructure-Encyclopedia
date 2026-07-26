# Chapter 03: ZIA Threat Prevention — Cloud Firewall, DNS Control, IPS, and Sandbox

## Learning Objectives

- Configure the **ZIA Cloud Firewall** (FWaaS) with network-service and
  application rules, and explain how it complements the SWG.
- Apply **DNS Control** and DNS security to filter and inspect name resolution.
- Explain **Advanced Threat Protection (ATP)** and the inline **IPS**, and how
  known-threat signatures block malicious content.
- Describe the **Cloud Sandbox** for detonating unknown files, and the choice
  between patient-zero blocking and quarantine.
- Validate protection safely using the industry-standard **EICAR** test file.

## Theory and Architecture

The Secure Web Gateway (Chapter 02) controls *where* users go; ZIA's threat
prevention controls *what* comes back and *what is happening at other layers*.
Because all traffic is already inline at the exchange, ZIA layers several
engines on the same session: a cloud firewall for non-web ports and
applications, DNS control for name resolution, signature-based IPS/ATP for
known threats, and a sandbox for unknown files. One pass, many verdicts.

### Cloud Firewall (FWaaS)

The ZIA **Cloud Firewall** applies stateful policy to all ports and protocols,
not just 80/443 — rules match by network service (port/protocol), network
application, source/destination, user, and location. It replaces branch
firewalls for internet-bound traffic, so a site can forward everything to
Zscaler and let cloud policy decide, rather than maintaining per-site firewall
rules.

### DNS Control

**DNS Control** governs resolution: it can block or redirect categories of
domains, enforce a specific resolver, detect DNS tunneling, and stop
resolution of known-malicious domains before a connection is even attempted.
Because so many attacks begin with a DNS lookup, filtering here stops threats
early and cheaply.

### ATP, IPS, and the Cloud Sandbox

- **Advanced Threat Protection (ATP)** blocks known malicious content —
  botnet callbacks, phishing, malicious active content — by reputation and
  signature.
- The inline **IPS** matches traffic against threat signatures in real time.
- The **Cloud Sandbox** handles the *unknown*: a file not seen before is
  detonated in an isolated environment and its behavior scored. Policy chooses
  between **AI Instant Verdict / patient-zero blocking** (hold the file until a
  verdict is returned, so even the first user is protected) and quarantine or
  allow-and-monitor for lower-risk categories.

## Design Considerations

- **Blocking unknown files has a latency/UX cost.** Patient-zero (hold-for-
  verdict) is the strongest posture but adds delay on first download of a new
  file; scope it to risky file types and untrusted categories.
- **DNS control is the cheapest chokepoint.** Blocking malicious domains at
  resolution prevents the connection entirely — apply it broadly.
- **Firewall + SWG are complementary.** Web policy lives in the SWG; non-web
  ports, DNS, and application control live in the firewall. Both run on the same
  forwarded session.

## Implementation and Automation

### A cloud-firewall rule (portal shape)

```text
# ZIA Portal > Policy > Firewall Control:
#   Rule "Block outbound SMB": Network Services = SMB (TCP/445); Action = Block
#   Rule "Allow DNS to Zscaler only": Network Services = DNS; Dest = Zscaler resolvers; Action = Allow
```

### DNS control and sandbox policy (portal shape)

```text
# ZIA Portal > Policy > DNS Control: block "Malware/Command & Control" domain categories
# ZIA Portal > Policy > Sandbox: file types = executables/archives; on unknown => "Quarantine (block until verdict)"
```

### Verifying with EICAR (safe test)

```bash
# EICAR is the industry-standard harmless antivirus test string. On a
# ZIA-forwarded host, downloading it should be blocked by ZIA's malware engine:
curl -s -o /dev/null -w "%{http_code}\n" https://secure.eicar.org/eicar.com.txt
```

## Validation and Troubleshooting

- **EICAR download succeeds unexpectedly.** Malware protection or SSL
  inspection is off for that host/category — the engine can only block what it
  inspects.
- **Legitimate file held too long.** Patient-zero blocking is holding for a
  sandbox verdict; verify the sandbox policy's scope and the file type rules.
- **DNS bypass.** A client using its own DoH resolver can evade DNS control —
  enforce DNS through Zscaler and block alternative resolvers in the firewall.

## Security and Best Practices

- **Turn on SSL inspection for the threat engines to matter** — encrypted
  malware is invisible without it (Chapter 02).
- **Prefer patient-zero blocking for high-risk file types**; the point of a
  cloud sandbox is that even the first victim is protected.
- **Close the DNS side door**: force Zscaler DNS and block public DoH/DoT
  resolvers so DNS Control cannot be bypassed.

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Cloud Firewall*, *DNS Control*, *Advanced Threat
  Protection*, and *Cloud Sandbox* (`help.zscaler.com`).
- EICAR anti-malware test file (`eicar.org`) — safe validation standard.

### Knowledge Checks

- How does the ZIA Cloud Firewall complement the Secure Web Gateway?
- Why is DNS control described as the cheapest chokepoint for stopping threats?
- What does patient-zero (hold-for-verdict) sandboxing protect against that
  allow-and-monitor does not?
- Why must SSL inspection be enabled for the threat engines to inspect most
  traffic?

## Hands-On Lab

This chapter's labs cover the threat-prevention engines — firewall, DNS
control, and sandbox/malware — validated with the safe EICAR standard. Portal
steps reference a ZIA tenant; the verification is a local `curl`. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.3** — `curl`; a ZIA-forwarded host for
the live block test. **Cost:** none.

### Lab 3.1 — A cloud-firewall rule (Topic: FWaaS)

**Objective:** Block a non-web service at the cloud firewall.

```text
# ZIA Portal > Policy > Firewall Control:
#   Rule "Block SMB egress": Network Services = SMB (TCP/445); Users = All; Action = Block
```

**Expected result:** outbound TCP/445 is blocked for forwarded users — the ZIA
Cloud Firewall applies stateful policy to all ports and protocols, not just
web, so a site can forward everything to Zscaler instead of maintaining
per-branch firewall rules.

**Negative test:** rely on the SWG alone to stop non-web threats; it governs
web traffic — non-web ports and applications need the cloud firewall.

**Cleanup:** disable the lab rule.

### Lab 3.2 — Malware/sandbox protection with EICAR (Topic: Threat prevention)

**Objective:** Prove malware download is blocked, safely.

```bash
# EICAR is a harmless standard test file that every AV/sandbox recognizes:
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://secure.eicar.org/eicar.com.txt
```

**Expected result:** on a ZIA-forwarded, SSL-inspected host the download is
**blocked** (a Zscaler block/notification instead of the file) — ZIA's malware
engine and sandbox detonate/score content inline, and EICAR is the safe,
industry-standard way to confirm protection without real malware.

**Negative test:** run the same request off Zscaler (or with inspection off);
the harmless EICAR file downloads — the engines can only act on inspected
traffic.

**Cleanup:** none.

### Lab 3.3 — DNS control (Topic: DNS security)

**Objective:** Filter resolution of a malicious-domain category.

```text
# ZIA Portal > Policy > DNS Control: block "Command & Control / Malware" domain categories;
# force clients to Zscaler DNS; block alternative public DoH resolvers in Firewall Control.
```

**Expected result:** lookups for malicious-category domains are blocked/redirected
before any connection is attempted — DNS Control is the earliest, cheapest
chokepoint: stopping resolution stops the attack before a session exists.

**Negative test:** allow clients to use their own DoH resolver; DNS Control is
bypassed — resolution must be forced through Zscaler for the control to hold.

**Cleanup:** revert lab DNS policy.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

On the same inline session, ZIA layers a cloud firewall for all ports, DNS
control at resolution, signature-based ATP/IPS for known threats, and a sandbox
for the unknown — with patient-zero blocking protecting even the first user.
The engines only see what SSL inspection decrypts, and DNS control is the
cheapest place to stop an attack. EICAR is the safe way to prove it all works.

- [ ] Can write a cloud-firewall rule for a non-web service.
- [ ] Has confirmed malware/sandbox blocking with EICAR.
- [ ] Can filter a malicious-domain category with DNS Control.
- [ ] Understands why SSL inspection and forced DNS are prerequisites.
