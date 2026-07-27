# Chapter 07: CCIS — Certified Identity Specialist

## Learning Objectives

- Explain what the CCIS certifies and its target role.
- Summarize the twelve exam-guide domains.
- Apply Falcon Identity Protection: assessment, policy, connectors, MFA/IDaaS.
- Hunt identity threats and query the Identity Protection GraphQL API.
- Complete a per-domain walkthrough for each CCIS domain.

## Theory and Architecture

The **CrowdStrike Certified Identity Specialist (CCIS)** validates managing
**Falcon Identity Protection** — the IAM/identity-threat credential. Its exam guide
(90 minutes, 60 questions) covers **twelve domains**: **Zero Trust Architecture**,
**Identity Protection Tenets**, **Falcon Identity Protection Fundamentals**, **Domain
Security Assessment**, **Risk Assessment**, **User Assessment**, **Threat Hunting and
Investigation**, **Risk Management with Policy Rules**, **Configuration and
Connectors**, **MFA and IDaaS**, **Falcon Fusion SOAR for Identity Protection**, and
the **GraphQL API**.

## Design Considerations

Identity Protection enforces **Zero Trust** on authentication: it ingests directory
and auth telemetry via **connectors**, scores **domain**, **user**, and **entity**
risk, enforces **policy rules** (allow/deny/step-up MFA), integrates **third-party
MFA/IDaaS**, supports **threat hunting**, automates response with **Fusion SOAR**, and
exposes everything through a **GraphQL API**. Policy rules that trigger step-up MFA are
the core control.

## Implementation and Automation

The labs use Identity Protection configuration and the **GraphQL API** for each of the
twelve domains.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CCIS exam guide (12 domains):
  Zero Trust Architecture; Identity Protection Tenets; Fundamentals;
  Domain Security Assessment; Risk Assessment; User Assessment;
  Threat Hunting and Investigation; Risk Management with Policy Rules;
  Configuration and Connectors; MFA and IDaaS; Fusion SOAR; GraphQL API
```

Common pitfalls: connectors not covering all domain controllers (blind spots); and
policy rules that block instead of **stepping up** authentication.

## Security and Best Practices

Extend **Zero Trust** to identity, cover **every DC/IdP** with connectors, act on
**risk scores** for domains/users/entities, prefer **step-up MFA** over hard blocks,
integrate existing **MFA/IDaaS**, hunt identity threats (e.g., Kerberoasting,
lateral movement), automate with **Fusion SOAR**, and drive it all via the
**GraphQL API**.

## References and Knowledge Checks

- crowdstrike.com: CCIS exam guide; Falcon Identity Protection and GraphQL API docs.

**Knowledge checks**

1. Why prefer step-up MFA over blocking?
2. What do domain/user/entity risk scores drive?
3. How does the GraphQL API expose Identity Protection data?

## Hands-On Lab

Per-domain walkthroughs — CCIS. **Shared prerequisites** — a Falcon tenant with
Identity Protection, a domain connector, and API access. GraphQL is shown as runnable
query text against the Identity Protection endpoint. **Cost:** none beyond the tenant.

### Lab 7.1 — Zero Trust Architecture

**Objective:** State how Identity Protection enforces Zero Trust at auth time.

```text
# Zero Trust: verify every authentication, evaluate risk, enforce least privilege.
# Identity Protection sits inline with Kerberos/NTLM/LDAP + IdP flows to score & gate.
"model: every auth is verified and risk-scored before access"
```

**Expected result:** the inline **verify-every-auth** model — the Zero Trust
Architecture domain.

**Negative test:** trust an authenticated session forever; Zero Trust **re-verifies**
continuously — never implicitly trust.

**Cleanup:** none.

### Lab 7.2 — Identity Protection Tenets

**Objective:** List the protection tenets.

```text
# Tenets: full visibility of all identities (human + service),
#         real-time risk scoring, and adaptive/conditional enforcement.
"tenets: visibility, risk scoring, adaptive enforcement"
```

**Expected result:** the three tenets — visibility, risk scoring, adaptive
enforcement (the Identity Protection Tenets domain).

**Negative test:** protect human users only; **service accounts** are prime targets —
cover all identities.

**Cleanup:** none.

### Lab 7.3 — Falcon Identity Protection Fundamentals

**Objective:** Confirm the product is receiving identity telemetry.

```text
query { entities(first: 1) { nodes { primaryDisplayName riskScore } } }
```

**Expected result:** at least one **entity** with a risk score — proof the
fundamentals (telemetry + scoring) are working.

**Negative test:** assume it's active after install; **query an entity** — no data
means the connector isn't feeding it.

**Cleanup:** none (read-only).

### Lab 7.4 — Domain Security Assessment

**Objective:** Review domain-level security findings.

```text
query { domainSecurityAssessment { findings { name severity affectedEntities } } }
```

**Expected result:** domain findings (e.g., weak crypto, stale accounts) with
severity — the Domain Security Assessment domain.

**Negative test:** assess users only; the **domain** posture (protocols, policies)
is a distinct assessment — run it.

**Cleanup:** none (read-only).

### Lab 7.5 — Risk Assessment

**Objective:** Rank entities by risk score.

```text
query { entities(sortKey: RISK_SCORE, sortOrder: DESCENDING, first: 10)
        { nodes { primaryDisplayName riskScore riskFactors { type } } } }
```

**Expected result:** the top-10 riskiest entities with **risk factors** — the Risk
Assessment domain.

**Negative test:** treat all entities equally; **risk-rank** to focus remediation.

**Cleanup:** none (read-only).

### Lab 7.6 — User Assessment

**Objective:** Inspect a single user's risk detail.

```text
query { entities(primaryDisplayNames: ["jdoe"]) 
        { nodes { riskScore riskFactors { type severity } accounts { ... on ActiveDirectoryAccount { samAccountName } } } } }
```

**Expected result:** the user's **risk factors** and linked accounts — the User
Assessment domain.

**Negative test:** judge a user by title; the **risk factors** (stale password,
privileged, exposed) are what matter.

**Cleanup:** none (read-only).

### Lab 7.7 — Threat Hunting and Investigation

**Objective:** Hunt anomalous authentications.

```text
query { timeline(types: [FAILED_AUTHENTICATION], first: 20)
        { nodes { timestamp sourceEntity { primaryDisplayName } targetEndpoint { hostName } } } }
```

**Expected result:** recent failed-auth events for hunting lateral movement/spray —
the Threat Hunting and Investigation domain.

**Negative test:** wait for an alert; **hunt** the auth timeline for patterns before
they escalate.

**Cleanup:** none (read-only).

### Lab 7.8 — Risk Management with Policy Rules

**Objective:** Define a step-up MFA policy rule.

```text
# Policy rule: IF risk >= HIGH AND access to privileged resource THEN require MFA.
mutation { createPolicyRule(input:{ name:"stepup-high-risk",
  condition:"riskScore>=HIGH", action: ENFORCE_MFA }) { id } }
```

**Expected result:** a rule that **enforces MFA** on high-risk access — the Risk
Management with Policy Rules domain (the core control).

**Negative test:** hard-block high risk; **step-up MFA** preserves productivity while
containing risk.

**Cleanup:** delete the rule if it was for the lab.

### Lab 7.9 — Configuration and Connectors

**Objective:** Verify connector health.

```text
query { connectors { nodes { name type status lastSyncTime } } }
```

**Expected result:** each connector's **status/last sync** — the Configuration and
Connectors domain (coverage of DCs/IdPs).

**Negative test:** deploy one connector for many DCs; **cover every DC** or you have
identity blind spots.

**Cleanup:** none (read-only).

### Lab 7.10 — MFA and IDaaS

**Objective:** Confirm a third-party IDaaS/MFA integration.

```text
query { identityProviders { nodes { name type enabled } } }
```

**Expected result:** the connected **IdP/MFA providers** and enabled state — the MFA
and IDaaS domain.

**Negative test:** rely on native MFA only; **integrate existing IDaaS** (Okta, Entra
ID, Ping) for consistent enforcement.

**Cleanup:** none (read-only).

### Lab 7.11 — Falcon Fusion SOAR for Identity Protection

**Objective:** Automate a response to an identity detection.

```text
# Fusion SOAR: on identity detection (e.g., Kerberoasting) -> disable account + notify.
"workflow: trigger=identity detection -> action=step-up MFA / disable / notify"
```

**Expected result:** a Fusion workflow linking an identity detection to an **automated
action** — the Fusion SOAR domain.

**Negative test:** respond to identity threats by hand; **SOAR** contains them at
machine speed.

**Cleanup:** disable the workflow if it was for the lab.

### Lab 7.12 — GraphQL API

**Objective:** Call the Identity Protection GraphQL endpoint.

```bash
curl -sS -X POST "https://api.crowdstrike.com/identity-protection/combined/graphql/v1" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"query":"{ entities(first:1){ nodes{ primaryDisplayName riskScore } } }"}'
```

**Expected result:** a JSON response with an entity and risk score — the GraphQL API
domain (programmatic access to Identity Protection).

**Negative test:** scrape the console UI; the **GraphQL API** is the supported,
scriptable interface — use it.

**Cleanup:** let the token expire.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCIS certifies Falcon Identity Protection across twelve domains: Zero Trust and
tenets, fundamentals, domain/risk/user assessment, threat hunting, policy rules
(step-up MFA), connectors, MFA/IDaaS, Fusion SOAR, and the GraphQL API.

- [ ] I can explain Zero Trust for identity and the protection tenets.
- [ ] I can run domain/risk/user assessments and hunt auth anomalies.
- [ ] I can build a step-up-MFA policy rule and verify connectors.
- [ ] I can integrate MFA/IDaaS, automate with SOAR, and call GraphQL.
- [ ] I completed Labs 7.1–7.12 including each negative test.
