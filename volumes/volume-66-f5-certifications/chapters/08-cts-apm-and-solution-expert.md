# Chapter 08: Technology Specialist — APM and Solution Expert

## Learning Objectives

- Explain the CTS APM specialization (exam 304) and the CSE Security expert level (401).
- Build an access policy with the Visual Policy Editor.
- Configure authentication, SSO, and per-request policy.
- Understand how the Solution Expert ties the security modules together.
- Complete a walkthrough for each APM and expert topic.

## Theory and Architecture

The **F5 Certified Technology Specialist, APM** (exam **304**) covers **BIG-IP Access Policy
Manager** — F5's access and identity gateway. APM authenticates and authorizes users before they
reach applications, delivering **secure web gateway**, **identity-aware proxy / ZTNA**,
**VPN** (network access), and **SSO** to backend apps. Access is defined in the **Visual Policy
Editor (VPE)** — a flow of checks (authentication against AD/LDAP/RADIUS/SAML/OAuth, endpoint
posture, group logic) that ends in **allow** (assign a session and resources) or **deny**.
**Per-request policy** re-evaluates each request for continuous authorization. The **F5 Certified
Solution Expert, Security** (exam **401**) is the capstone, requiring the F5-CA and all four CTS
specializations; it tests designing **integrated** solutions across LTM, DNS, Advanced WAF, and
APM — for example, an application published through LTM, protected by Advanced WAF, with access
gated by APM. All of this is **defensive**: controlling and protecting access.

## Design Considerations

Build access as an **explicit policy flow** in the VPE — authenticate, check posture, authorize,
then grant least-privilege resources. Prefer **identity-aware, per-app access (ZTNA)** over broad
network VPN. Use **SSO** to reduce credential handling. At the expert level, **combine** modules
(LTM + Advanced WAF + APM) into one coherent, defended service.

## Implementation and Automation

The labs build an access policy, add authentication and SSO, apply per-request policy, and reason
about an integrated Solution Expert design.

## Validation and Troubleshooting

Confirm the APM/CSE model:

```text
APM: authenticate (AD/LDAP/RADIUS/SAML/OAuth) + posture + authorize -> allow/deny; SSO; VPN; ZTNA.
Visual Policy Editor (VPE): the access flow. Per-request policy: continuous authorization.
CSE Security (401): integrate LTM + DNS + Advanced WAF + APM. Requires F5-CA + 4 CTS.
```

Common pitfalls: broad **network VPN** where **per-app ZTNA** fits; and a policy that authorizes
once but never **re-evaluates** (add per-request policy).

## Security and Best Practices

Authenticate and **authorize before access**, check **posture**, grant **least privilege**, and
use **SSO**. Re-evaluate with **per-request policy**. At the expert level, layer **APM + Advanced
WAF + LTM** so access, application security, and delivery reinforce each other. Defensive access
control throughout.

## Hands-On Lab

APM and expert walkthroughs. **Shared prerequisites** — a BIG-IP VE with APM provisioned (Labs
8.1–8.3); Lab 8.4 is design reasoning. In an authorized lab. **Cost:** none.

### Lab 8.1 — Create an access profile and policy

**Objective:** Gate the app behind an access policy.

```bash
tmsh create apm profile access web_access accept-languages add { en } 
# Then build the policy flow in the Visual Policy Editor: Start -> Logon Page -> AD Auth -> Allow.
tmsh modify ltm virtual web_vs profiles add { web_access }
tmsh list apm profile access web_access
```

**Expected result:** an **access profile** on `web_vs` with a VPE flow — users must pass the
policy before reaching the app.

**Negative test:** publish the app with no access profile; unauthenticated users reach it
directly — gate it with APM.

**Cleanup:** detach and delete the access profile.

### Lab 8.2 — Add authentication and SSO

**Objective:** Authenticate users and sign them into the backend.

```text
# VPE: Logon Page -> AD/LDAP (or SAML/OAuth) Auth -> on success, SSO credentials to the backend app.
"access flow: authenticate (AD/SAML) -> SSO to app -> single sign-on, no re-prompt"
```

**Expected result:** users **authenticate once** and are **SSO'd** into the application — secure,
seamless access.

**Negative test:** prompt for credentials at both APM and the app; **SSO** passes them once —
configure it.

**Cleanup:** none.

### Lab 8.3 — Per-request policy

**Objective:** Re-evaluate authorization continuously.

```text
# Per-request policy runs on each request (not just at logon): re-check group/URL/posture ->
#   allow or block that request. Enables continuous, Zero-Trust authorization.
"per-request: re-authorize every request -> continuous Zero Trust"
```

**Expected result:** **continuous authorization** per request — access decisions that don't stop
at logon.

**Negative test:** authorize only at logon; **per-request policy** re-checks each request — add it
for Zero Trust.

**Cleanup:** none.

### Lab 8.4 — Solution Expert integration (401)

**Objective:** Design a combined, defended service.

```python
python3 - <<'PY'
service={"delivery":"LTM virtual server + pool (load balance, SSL offload)",
         "app_security":"Advanced WAF policy (signatures + positive model + bot defense)",
         "access":"APM access policy (authenticate + ZTNA + SSO)",
         "global":"BIG-IP DNS wide IP (multi-site failover)"}
for layer,detail in service.items(): print(f"{layer:12}: {detail}")
print("CSE Security (401): integrate all four into one coherent design")
PY
```

**Expected result:** an **integrated** design — LTM delivery, Advanced WAF protection, APM access,
DNS global availability — the Solution Expert deliverable.

**Negative test:** deploy the modules in isolation; the **expert** design integrates them into one
defended service.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CTS APM specialization (304) covers access policy in the VPE — authentication, SSO, ZTNA, VPN,
and per-request continuous authorization — and the CSE Security expert (401) integrates LTM, DNS,
Advanced WAF, and APM into one defended service. Authorize before access, prefer per-app ZTNA, and
combine modules at the expert level.

- [ ] I can build an access profile and policy.
- [ ] I can add authentication and SSO.
- [ ] I can apply a per-request policy.
- [ ] I can design an integrated Solution Expert service.
- [ ] I completed Labs 8.1–8.4 including each negative test.
