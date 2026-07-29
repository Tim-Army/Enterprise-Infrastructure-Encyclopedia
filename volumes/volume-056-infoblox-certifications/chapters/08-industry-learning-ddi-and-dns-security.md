# Chapter 08: Industry Learning — DDI and DNS Security

## Learning Objectives

- Explain Infoblox's vendor-agnostic Industry Learning credentials.
- Summarize the DDI Associate/Professional scope.
- Summarize the DNS Security Associate/Professional scope.
- Apply the concepts with standard DNS/DHCP tooling.
- Complete a walkthrough for each Industry Learning credential.

## Theory and Architecture

Beyond product certifications, Infoblox offers **Industry Learning** — **vendor-agnostic**
credentials teaching portable fundamentals: **DDI Associate (DDIA)** and **DDI
Professional (DDIP)** cover DNS, DHCP, and IPAM from fundamentals through advanced design;
**DNS Security Associate (DSA)** and **DNS Security Professional (DSP)** cover DNS-based
threats and mitigation. These validate concepts that apply on any vendor's platform, so
the labs use **standard tooling** (`dig`, DNS/DHCP concepts) rather than Infoblox-specific
APIs.

## Design Considerations

Use the **Associate** tiers for fundamentals and the **Professional** tiers for advanced
design/analysis. The knowledge is portable — it underpins the product tracks (NIOS,
Universal DDI, Threat Defense) and any other DDI/DNS-security platform.

## Implementation and Automation

The labs use standard DNS tooling (`dig`) for each credential's scope.

## Validation and Troubleshooting

Confirm the credentials:

```text
Industry Learning (vendor-agnostic):
  DDIA / DDIP — DNS, DHCP, IPAM (fundamentals -> advanced)
  DSA / DSP — DNS-based threats + mitigation
```

Common pitfalls: treating these as product exams (they are **vendor-agnostic**); and
skipping fundamentals before the professional tier.

## Security and Best Practices

Build **portable fundamentals** first (DDIA/DSA) then advance (DDIP/DSP), and apply the
concepts across whatever DDI/DNS-security platform you operate. Understand DNS threats
(tunneling, cache poisoning, DGA) generically.

## Hands-On Lab

Per-credential walkthroughs — Industry Learning. **Shared prerequisites** — a shell with
`dig` (bind-utils/dnsutils). **Cost:** none.

### Lab 8.1 — DDI Associate (DNS fundamentals)

**Objective:** Resolve records to demonstrate DNS fundamentals.

```bash
dig +short example.com A
dig +short example.com NS
```

**Expected result:** the **A and NS** records — core DNS resolution (the DDIA
fundamentals).

**Negative test:** assume one record type suffices; DNS has **many types** (A/AAAA/NS/MX/
TXT/PTR) — know each.

**Cleanup:** none.

### Lab 8.2 — DDI Professional (advanced DNS/DHCP)

**Objective:** Inspect delegation and authority.

```bash
dig +norecurse @a.root-servers.net com. NS +short | head
dig example.com SOA +short
```

**Expected result:** the delegation chain and the zone **SOA** — advanced DNS behavior
(the DDIP scope).

**Negative test:** ignore the **SOA/serial** during zone changes; the serial drives
secondary transfers — track it.

**Cleanup:** none.

### Lab 8.3 — DNS Security Associate (threats)

**Objective:** Recognize a DNS-based threat pattern.

```bash
# Long, high-entropy subdomains under one domain suggest DNS tunneling/exfiltration:
dig +short $(python3 -c "print('a'*40)").tunnel.example TXT 2>/dev/null; echo "(pattern: oversized/encoded labels)"
```

**Expected result:** recognition that **oversized/encoded labels** signal tunneling — the
DSA threat-awareness scope.

**Negative test:** treat all DNS traffic as benign; **tunneling/exfiltration** hides in
DNS — inspect it.

**Cleanup:** none.

### Lab 8.4 — DNS Security Professional (mitigation)

**Objective:** Describe layered DNS mitigations.

```text
# Mitigations: DNSSEC (integrity), response policy zones (RPZ)/threat feeds (blocking),
#   rate limiting (RRL), and behavioral analytics for tunneling/DGA.
"defense-in-depth: DNSSEC + RPZ/feeds + RRL + analytics"
```

**Expected result:** a layered **mitigation** strategy — the DSP professional scope.

**Negative test:** rely on a single control (a blocklist); **layer** integrity, blocking,
rate-limiting, and analytics.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Infoblox Industry Learning provides vendor-agnostic credentials — DDI Associate/
Professional (DNS/DHCP/IPAM) and DNS Security Associate/Professional (threats and
mitigation) — teaching portable fundamentals that underpin the product tracks. This
chapter applied each with standard DNS tooling.

- [ ] I can demonstrate DNS resolution fundamentals.
- [ ] I can inspect delegation, authority, and SOA.
- [ ] I can recognize DNS-based threat patterns.
- [ ] I can describe layered DNS mitigations.
- [ ] I completed Labs 8.1–8.4 including each negative test.
