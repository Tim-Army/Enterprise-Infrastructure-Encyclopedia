# Chapter 03: Administrator — SSO and App Integration

## Learning Objectives

- Integrate applications with SAML and OIDC.
- Use SWA for apps without federation.
- Configure the OIN and custom app integrations.
- Troubleshoot SSO failures.
- Complete a walkthrough for each SSO integration topic.

## Theory and Architecture

The **Okta Certified Administrator** deepens single sign-on. Okta acts as the **identity provider
(IdP)**, and applications are **service providers (SPs)** that trust it. The two federation
standards: **SAML 2.0** (XML assertions — long the enterprise standard) and **OpenID Connect (OIDC)**
(JSON/JWT on top of OAuth 2.0 — the modern default for new apps). For apps that support neither,
**SWA (Secure Web Authentication)** securely stores and replays credentials. Administrators integrate
apps from the **OIN** catalog (pre-built) or configure **custom** SAML/OIDC integrations, mapping
Okta user attributes into the assertion/token (e.g., email, groups) so the app knows who the user is
and what they can do. Troubleshooting SSO means reading the **SAML assertion or ID token**, checking
the **audience/entity ID**, certificates, and attribute mappings, and using the **System Log**. This
chapter teaches each with a hands-on defensive walkthrough (decoding tokens, mapping attributes,
diagnosing failures).

## Design Considerations

Prefer **OIDC** for new apps, **SAML** for enterprise apps that require it, and **SWA** only when
neither is available. Map the **minimum attributes** the app needs. Match **entity ID/audience** and
**ACS/redirect URIs** exactly. Rotate signing **certificates** before expiry. Use the **System Log**
for diagnosis.

## Implementation and Automation

The labs decode an assertion/token, map attributes, and troubleshoot an SSO failure.

## Validation and Troubleshooting

Confirm the SSO model:

```text
Okta = IdP; app = SP. SAML 2.0 (XML assertion) vs OIDC (JWT on OAuth 2.0). SWA = credential replay (no federation).
Integrate via OIN (pre-built) or custom. Map attributes into assertion/token. Troubleshoot: audience/entityID, certs, ACS/redirect, System Log.
```

Common pitfalls: mismatched **audience/entity ID** or **ACS URL** (assertion rejected); and an
**expired signing certificate** (SSO breaks).

## Security and Best Practices

Prefer modern **OIDC**, map **least attributes**, match endpoints/audiences exactly, rotate
**certificates** on time, and diagnose with the **System Log**. All work is defensive.

## Hands-On Lab

SSO walkthroughs. **Shared prerequisites** — `python3`, `base64`, a developer org. **Cost:** none.

### Lab 3.1 — Decode an OIDC ID token

**Objective:** Read what the app receives.

```bash
# A sample unsigned JWT payload (header.payload.signature); decode the payload:
JWT='eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIwMHUxMjMiLCJlbWFpbCI6ImFteUBleC5jb20iLCJncm91cHMiOlsiRmluYW5jZSJdfQ.sig'
echo "$JWT" | cut -d. -f2 | tr '_-' '/+' | base64 -d 2>/dev/null; echo
echo "OIDC: the ID token (JWT) carries claims (sub, email, groups) the app trusts"
```

**Expected result:** the decoded **claims** (`sub`, `email`, `groups`) — what an OIDC app receives
from Okta.

**Negative test:** trust a token without checking its **signature/issuer/audience**; a forged token
would pass — always validate them.

**Cleanup:** none.

### Lab 3.2 — Map attributes into the assertion

**Objective:** Give the app what it needs.

```python
python3 - <<'PY'
okta_user={"email":"amy@ex.com","firstName":"Amy","groups":["Finance"],"employeeId":"E123"}
app_needs=["email","groups"]     # least privilege: only what the app requires
assertion={k:okta_user[k] for k in app_needs}
print("SAML/OIDC attribute mapping ->", assertion)
print("Administrator: map only the attributes the app needs")
PY
```

**Expected result:** an assertion carrying **only email and groups** — least-attribute mapping.

**Negative test:** map every attribute including `employeeId`/PII the app doesn't need; that
over-shares — map the **minimum**.

**Cleanup:** none.

### Lab 3.3 — Troubleshoot an SSO failure

**Objective:** Diagnose a rejected assertion.

```python
python3 - <<'PY'
idp={"audience":"https://app.example.com","acs":"https://app.example.com/acs"}
sp ={"audience":"https://app.example.com","acs":"https://app.example.com/saml/consume"}  # mismatch!
issues=[]
if idp["audience"]!=sp["audience"]: issues.append("audience/entityID mismatch")
if idp["acs"]!=sp["acs"]: issues.append("ACS URL mismatch")
print("SSO failure causes:", issues or "none")
print("Administrator: check System Log; align audience + ACS/redirect URLs + certs")
PY
```

**Expected result:** the **ACS URL mismatch** identified — SSO troubleshooting.

**Negative test:** blame the user's password for an SSO failure; SSO issues are usually **config**
(audience/ACS/cert) — check the assertion and System Log.

**Cleanup:** none.

### Lab 3.4 — Choose the right integration method

**Objective:** Match method to app.

```python
python3 - <<'PY'
apps={"modern SaaS (new)":"OIDC","enterprise app requiring SAML":"SAML 2.0","legacy form-login app":"SWA"}
for app,method in apps.items(): print(f"{app:30}: {method}")
print("Administrator: OIDC first, SAML when required, SWA only as last resort")
PY
```

**Expected result:** each app matched to **OIDC/SAML/SWA** — correct integration choice.

**Negative test:** force SWA credential replay where **OIDC** is supported; that's less secure — use
federation when available.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Administrator SSO skills cover Okta as IdP integrating apps via SAML, OIDC, and SWA, mapping
least attributes into assertions/tokens, and troubleshooting via audience/ACS/certs and the System
Log.

- [ ] I can decode an OIDC ID token.
- [ ] I can map least attributes into an assertion.
- [ ] I can troubleshoot an SSO failure.
- [ ] I can choose the right integration method.
- [ ] I completed Labs 3.1–3.4 including each negative test.
