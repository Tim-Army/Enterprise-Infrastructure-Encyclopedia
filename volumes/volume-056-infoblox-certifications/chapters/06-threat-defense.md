# Chapter 06: Threat Defense

## Learning Objectives

- Explain Infoblox Threat Defense and DNS-layer security.
- Identify the Threat Defense components.
- Configure DNS forwarding proxies and security policies.
- Integrate endpoints and use threat analytics.
- Complete a walkthrough for each Threat Defense topic.

## Theory and Architecture

**Infoblox Threat Defense** provides **DNS-layer security** — blocking access to
malicious domains and detecting DNS-based exfiltration before connections complete. Its
microcredential topic areas: **components** (the cloud service, on-prem enforcement),
**DNS forwarding proxies** (steer client DNS through Threat Defense), **security policy
configuration** (allow/block/redirect by category and threat feed), **endpoint
integration** (the endpoint agent for roaming users), and **threat analytics** including
**Threat Insight** (detecting DNS tunneling/DGA). It is a **defensive** control.

## Design Considerations

Steer DNS through **forwarding proxies** or the **endpoint agent** so all resolution is
inspected, apply **security policies** (threat feeds + categories) per group, and use
**Threat Insight** analytics to catch tunneling/exfiltration. This is protection at the
DNS control point every connection uses.

## Implementation and Automation

The labs use the Portal API for each Threat Defense topic — components, proxies, policy,
endpoints, and analytics.

## Validation and Troubleshooting

Confirm the topic areas:

```text
Threat Defense: components; DNS forwarding proxies; security policy config;
endpoint integration; threat analytics (Threat Insight — tunneling/DGA/exfil).
Defensive DNS-layer security.
```

Common pitfalls: DNS paths that bypass Threat Defense (uninspected resolution); and
policies with no threat feeds.

## Security and Best Practices

Route **all** DNS through Threat Defense (proxies + endpoint agent), apply **policies**
with current threat feeds, segment policy by **group**, and monitor **Threat Insight**
for tunneling/exfiltration. Authorized defensive use only.

## Hands-On Lab

Per-topic walkthroughs — Threat Defense. **Shared prerequisites** — an Infoblox Portal
tenant with Threat Defense and an API key. **Cost:** none beyond a trial tenant.

### Lab 6.1 — Components

**Objective:** Confirm the Threat Defense service is active.

```bash
curl -sS "https://csp.infoblox.com/api/atcfw/v1/security_policies" \
  -H "Authorization: Token $CSP_API_KEY" \
  | python3 -c "import sys,json;print('security policies:',len(json.load(sys.stdin).get('results',[])))"
```

**Expected result:** the configured **security policies** — confirming the Threat Defense
components are in place.

**Negative test:** assume DNS security is on by default; **verify the service/policies**
exist — it must be configured.

**Rollback:** none (read-only).

### Lab 6.2 — DNS forwarding proxies

**Objective:** List DNS forwarding proxies.

```bash
curl -sS "https://csp.infoblox.com/api/atcfw/v1/dns_forwarding_proxies" \
  -H "Authorization: Token $CSP_API_KEY" \
  | python3 -c "import sys,json;print('DFPs:',len(json.load(sys.stdin).get('results',[])))"
```

**Expected result:** the **DNS forwarding proxies** steering client DNS through Threat
Defense — the proxy topic.

**Negative test:** leave clients resolving directly to public DNS; a **forwarding proxy**
routes them through inspection — deploy it.

**Rollback:** none (read-only).

### Lab 6.3 — Security policy configuration

**Objective:** Review a policy's rules.

```bash
curl -sS "https://csp.infoblox.com/api/atcfw/v1/security_policies" \
  -H "Authorization: Token $CSP_API_KEY" \
  | python3 -c "import sys,json;r=json.load(sys.stdin)['results'];print('rules in policy 0:',len(r[0].get('rules',[])) if r else 0)"
```

**Expected result:** the **rules** (feeds/categories with allow/block/redirect) in a
policy — the policy-configuration topic.

**Negative test:** block-list a few domains by hand; **threat feeds** keep the policy
current automatically — use them.

**Rollback:** none (read-only).

### Lab 6.4 — Endpoint integration

**Objective:** Confirm endpoint agent coverage.

```text
# The Infoblox endpoint agent forwards roaming users' DNS to Threat Defense off-network.
# Verify enrolled endpoints in the Portal (Endpoints view / api).
"roaming endpoints enrolled -> DNS inspected on and off the corporate network"
```

**Expected result:** enrolled **endpoints** whose DNS is inspected anywhere — the
endpoint-integration topic.

**Negative test:** protect only on-network DNS; **endpoint agents** extend protection to
roaming users — enroll them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.5 — Threat analytics (Threat Insight)

**Objective:** Review DNS threat analytics.

```bash
curl -sS "https://csp.infoblox.com/api/dnsdata/v2/dns_event" \
  -H "Authorization: Token $CSP_API_KEY" 2>/dev/null \
  | python3 -c "import sys,json;print('DNS security events:',len(json.load(sys.stdin).get('result',[])))" 2>/dev/null \
  || echo "review: Threat Insight flags DNS tunneling/DGA/exfiltration in the Portal"
```

**Expected result:** DNS security **events** (or the Threat Insight view) — the analytics
topic (tunneling/DGA/exfiltration detection).

**Negative test:** watch only blocklist hits; **Threat Insight** detects behavioral
tunneling/exfil that lists miss — monitor it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Infoblox Threat Defense delivers DNS-layer security across its components, DNS forwarding
proxies, security-policy configuration (threat feeds/categories), endpoint integration
for roaming users, and Threat Insight analytics — a defensive control at the DNS choke
point.

- [ ] I can confirm the Threat Defense components/policies.
- [ ] I can list DNS forwarding proxies.
- [ ] I can review security-policy rules and feeds.
- [ ] I can describe endpoint integration and Threat Insight.
- [ ] I completed Labs 6.1–6.5 including each negative test.
