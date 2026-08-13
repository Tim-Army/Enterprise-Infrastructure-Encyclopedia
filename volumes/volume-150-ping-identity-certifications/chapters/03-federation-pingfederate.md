# Chapter 03: Federation — PingFederate

## Learning Objectives

- Explain SAML and OIDC federation and the IdP/SP roles.
- Understand the assertion/token as the vehicle of trust.
- Distinguish OAuth authorization from OIDC authentication.
- Apply least-privilege scopes to access tokens.

*Cert relevance: PingFederate is Ping's flagship — the **Certified Professional – PingFederate** exam is federation, SAML, OIDC, and OAuth.*

## The federation protocols

**PingFederate** is a **federation server** — it implements the standards that let identity be trusted across domains. Two protocol families dominate:

| Protocol | Era / use | Carries |
|:---|:---|:---|
| **SAML 2.0** | Enterprise SSO, mature | XML **assertions** |
| **OIDC** (OpenID Connect) | Modern, API/mobile-friendly, built on OAuth 2.0 | JSON **ID tokens** (JWTs) |

Both do the same core job — let an **identity provider (IdP)** vouch for a user to a **service provider (SP)** / relying party — but SAML is the older XML-based enterprise standard, and **OIDC** is the modern JSON/JWT standard built on **OAuth 2.0**, better suited to mobile apps and APIs. PingFederate speaks both, bridging legacy and modern. Knowing when each applies is core exam material.

## The assertion is the trust

The heart of federation is the **assertion** (SAML) or **token** (OIDC): a **digitally-signed statement** from the IdP saying "I have authenticated this user; here is who they are (and some attributes)." The SP **trusts the signature** — it does not re-authenticate the user or ever see their password; it verifies the assertion was signed by the IdP it trusts, and grants access.

This is why federation is secure: the trust rests on **cryptographic signatures**, not shared passwords. The SP and IdP exchange signing certificates once (establishing the trust relationship), and thereafter every assertion is verifiable. A tampered or forged assertion fails signature verification. The lab models the signed-assertion flow.

## OAuth versus OIDC

A distinction the exam tests and practitioners muddle:

- **OAuth 2.0** is an **authorization** framework — it issues **access tokens** that grant a client permission to call an API *on a user's behalf*, scoped to specific permissions. OAuth answers "what can this app do?" It does **not**, by itself, tell you *who the user is*.
- **OIDC** is an **authentication** layer *on top of* OAuth 2.0 — it adds an **ID token** that says *who the user is*. OIDC answers "who logged in?"

The classic error is using a raw OAuth **access token** as proof of *identity* — it is proof of *authorization* to call an API, not an authentication of the user. OIDC's **ID token** is the identity statement. PingFederate issues both, correctly. And OAuth's **scopes** are the least-privilege lever: an access token should carry only the scopes the client actually needs. The lab models scoped tokens.

## Hands-On Lab

Python models federation. **Cost:** none.

### Lab 3.1 — The signed assertion carries the trust

**Objective:** See why the SP trusts a signature, not a password.

```bash
python3 - <<'EOF'
import hashlib
# IdP signs an assertion; SP verifies with the IdP's known public key (modeled as a shared secret)
IDP_SIGNING_KEY = "idp-private-key-SECRET"
SP_KNOWN_IDP_KEY = "idp-private-key-SECRET"   # exchanged once, at trust setup

def sign(assertion, key):
    return hashlib.sha256((assertion + key).encode()).hexdigest()[:16]

def idp_issue(user):
    assertion = f"user={user};authenticated=true;dept=finance"
    return assertion, sign(assertion, IDP_SIGNING_KEY)

def sp_accept(assertion, signature):
    # SP re-computes the signature with the IdP key it trusts
    return sign(assertion, SP_KNOWN_IDP_KEY) == signature

# normal flow
assertion, sig = idp_issue("alice")
print("IdP authenticates alice, issues a SIGNED assertion:")
print(f"   assertion: {assertion}")
print(f"   signature: {sig}")
print(f"   SP verifies signature -> {sp_accept(assertion, sig)} -> alice is IN")
print("   (the SP NEVER saw alice's password — it trusts the IdP's signature)\n")

# attacker forges an assertion (elevates to admin) but can't sign it correctly
forged = "user=mallory;authenticated=true;dept=finance;role=ADMIN"
forged_sig = sign(forged, "attacker-guessed-key")   # wrong key
print("Attacker FORGES an assertion (adds role=ADMIN), signs with a guessed key:")
print(f"   forged:    {forged}")
print(f"   SP verifies signature -> {sp_accept(forged, forged_sig)} -> REJECTED")
print("   the forged assertion fails signature verification — the attacker doesn't")
print("   have the IdP's signing key, so they can't produce a valid signature.\n")
print("The federation security model: trust rests on the IdP's SIGNATURE, not on")
print("shared passwords. The SP and IdP exchange signing certs ONCE (trust setup);")
print("after that, every assertion is cryptographically verifiable. No password ever")
print("crosses to the SP, and a forged/tampered assertion is rejected. This is what")
print("PingFederate manages — the signing keys, the trust relationships, the assertions.")
EOF
```

**Expected result:** A signed assertion accepted by the SP via signature verification (never seeing the password) and a forged assertion rejected because the attacker lacks the IdP's signing key. The assertion lesson is that federation trust rests on cryptographic signatures, not shared passwords — the SP verifies the IdP's signature, so no password crosses domains and forged assertions fail.

**Negative test:** Assuming an attacker who crafts an assertion can impersonate a user. Without the IdP's signing key they cannot produce a valid signature, and the SP rejects the forgery — the signature, not the assertion's contents alone, is the trust.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Least-privilege OAuth scopes

**Objective:** Scope an access token to only what the client needs.

```bash
python3 - <<'EOF'
# an app requests an OAuth access token to call APIs on the user's behalf
ALL_SCOPES = ["profile:read", "email:read", "contacts:read", "contacts:write",
              "files:read", "files:write", "payments:write"]
# a calendar app that only needs to read the profile and contacts
APP = "calendar-app"
NEEDED = ["profile:read", "contacts:read"]

print(f"'{APP}' requests an OAuth access token. What scopes should it get?\n")
print("OVER-SCOPED (grant everything 'to be safe'):")
print(f"   token scopes = {ALL_SCOPES}")
print("   -> if this token leaks (logs, a compromised app), the attacker can WRITE")
print("      contacts, read/write FILES, and make PAYMENTS. Huge blast radius.\n")
print("LEAST-PRIVILEGE (grant only what the app needs):")
print(f"   token scopes = {NEEDED}")
denied = [s for s in ALL_SCOPES if s not in NEEDED]
print(f"   denied: {denied}")
print("   -> if THIS token leaks, the attacker can only READ profile + contacts.")
print("      No writes, no files, no payments. Blast radius capped to the task.\n")
print("The OAuth lesson: an access token is a bearer of PERMISSION — whoever holds it")
print("can do what its SCOPES allow. So scope it to the minimum the client needs, never")
print("'everything to avoid errors.' A leaked over-scoped token is a breach; a leaked")
print("least-privilege token is a nuisance.")
print("\nAlso note: this ACCESS token authorizes API calls — it is NOT proof of WHO the")
print("user is. That's the OIDC ID token's job. Using an access token as identity is")
print("the classic OAuth-vs-OIDC error: OAuth = authorize (what can this app do),")
print("OIDC = authenticate (who logged in). PingFederate issues both, for the right use.")
EOF
```

**Expected result:** A calendar app scoped to only profile and contacts read, versus an over-scoped token that grants file and payment writes, so a leak's blast radius is capped to the task. The scope lesson is that an OAuth access token bears exactly its scopes' permissions, so least privilege caps a leak's damage — and the reminder that an access token authorizes API calls but is not identity (that is OIDC's ID token).

**Negative test:** Granting an app all scopes to avoid permission errors. A leaked over-scoped token lets an attacker write files and make payments; least-privilege scopes cap the damage to the app's actual task.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SAML and OIDC federation understood, with the IdP vouching for a user to an SP.
- [ ] The signed assertion/token understood as the vehicle of trust — signatures, not shared passwords.
- [ ] OAuth (authorization, access tokens) distinguished from OIDC (authentication, ID tokens).
- [ ] Least-privilege scopes applied to access tokens to cap a leak's blast radius.
