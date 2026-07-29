# Chapter 07: Developer and Auth0 Customer Identity

## Learning Objectives

- Build secure sign-in with Okta/OIDC flows (Developer).
- Choose the right OAuth 2.0 grant for each app type.
- Extend identity with hooks and Auth0 Actions.
- Implement customer identity (B2C/B2B) with Auth0.
- Complete a walkthrough for each Developer/CIC topic.

## Theory and Architecture

The **Okta Certified Developer** and **Auth0 Certified Developer** validate building secure
authentication into applications. Developers integrate login using **OpenID Connect (OIDC)** on top
of **OAuth 2.0**, choosing the correct **grant/flow** for the app type: **Authorization Code with
PKCE** for single-page and mobile apps (public clients), **Authorization Code** for server-side web
apps (confidential clients), and **Client Credentials** for machine-to-machine. Okta issues **ID
tokens** (who the user is) and **access tokens** (what they can call), which apps validate. Identity
can be **extended** with **Okta hooks** (inline/event hooks that call your code during sign-in/
registration) and, on the **Customer Identity Cloud (Auth0)**, **Actions** (serverless functions in
the login pipeline) and **Organizations** (B2B multi-tenant). Auth0 focuses on **customer**
scenarios — B2C signup/login, social connections, and B2B SaaS — where user experience and
extensibility matter. This chapter teaches each with a hands-on defensive walkthrough (flow
selection, token handling, hooks/Actions).

## Design Considerations

Use **Authorization Code + PKCE** for public clients; never the deprecated **implicit** flow. Keep
**client secrets** server-side only. Validate **ID/access tokens** properly. Extend with **hooks/
Actions** for custom logic (MFA enrichment, risk checks) without weakening the flow. For Auth0, use
**Organizations** for B2B and secure **social/database** connections.

## Implementation and Automation

The labs select flows, validate tokens, and add an Action/hook.

## Validation and Troubleshooting

Confirm the developer model:

```text
OIDC on OAuth 2.0. Flows: Auth Code + PKCE (SPA/mobile public), Auth Code (server confidential), Client Credentials (M2M).
Tokens: ID (identity) + access (authorization). Extend: Okta hooks; Auth0 Actions (login pipeline) + Organizations (B2B). Never implicit flow.
```

Common pitfalls: using the **implicit** flow or embedding **secrets** in a SPA; and not validating
tokens in the app.

## Security and Best Practices

Use **Auth Code + PKCE** for public clients, keep **secrets** server-side, validate tokens, and add
logic via **hooks/Actions** without weakening security. For B2B, use Auth0 **Organizations**. All
work is defensive.

## Hands-On Lab

Developer/CIC walkthroughs. **Shared prerequisites** — `python3`, a free Okta/Auth0 developer org.
**Cost:** none.

### Lab 7.1 — Choose the right OAuth flow

**Objective:** Match grant to app type.

```python
python3 - <<'PY'
apps={"single-page app (browser)":"Authorization Code + PKCE","mobile app":"Authorization Code + PKCE",
      "server-side web app":"Authorization Code (confidential client)","backend service (no user)":"Client Credentials"}
for app,flow in apps.items(): print(f"{app:28}: {flow}")
print("Developer: PKCE for public clients; never the deprecated implicit flow")
PY
```

**Expected result:** each app matched to the correct **OAuth flow** — secure flow selection.

**Negative test:** use the **implicit** flow for a SPA; tokens leak in the URL — use **Auth Code +
PKCE**.

**Cleanup:** none.

### Lab 7.2 — Handle tokens safely in a public client

**Objective:** Protect tokens.

```python
python3 - <<'PY'
practices={"store":"in-memory (not localStorage) for access tokens",
           "client secret":"NONE in a public client (PKCE instead)",
           "refresh":"rotating refresh tokens","validate":"verify iss/aud/exp/signature"}
for k,v in practices.items(): print(f"{k:14}: {v}")
print("Developer: PKCE + no secret + rotating refresh + validation")
PY
```

**Expected result:** safe token handling (in-memory, PKCE, rotating refresh, validation) — public-
client security.

**Negative test:** embed a **client secret** in the SPA; anyone can read it — public clients use
**PKCE**, no secret.

**Cleanup:** none.

### Lab 7.3 — Add an Auth0 Action / Okta hook

**Objective:** Extend the login pipeline safely.

```python
python3 - <<'PY'
# Pseudo Auth0 Action (login pipeline): enforce email verification + add a claim
def on_login(event, api):
    if not event["user"]["email_verified"]:
        return api.access.deny("email not verified")
    api.id_token.set_custom_claim("tenant", event["organization"]["name"])
    return "allow"
print(on_login({"user":{"email_verified":True},"organization":{"name":"acme"}}, type("A",(),{
    "access":type("x",(),{"deny":staticmethod(lambda m:f'deny: {m}')}),
    "id_token":type("y",(),{"set_custom_claim":staticmethod(lambda k,v:None)})})()))
print("Auth0 Action / Okta hook: custom logic in the pipeline (verify + enrich) without weakening the flow")
PY
```

**Expected result:** the Action **allows** a verified user and could deny unverified — pipeline
extension.

**Negative test:** put trust decisions only in the client app; bypass the client and they're gone —
enforce in the **Action/hook** (server side).

**Cleanup:** none.

### Lab 7.4 — Model an Auth0 B2B organization

**Objective:** Multi-tenant customer identity.

```python
python3 - <<'PY'
orgs={"acme":{"connection":"acme-saml","branding":"Acme logo"},
      "globex":{"connection":"globex-google","branding":"Globex logo"}}
def login(org,user): return f"{user} -> {orgs[org]['connection']} (branded: {orgs[org]['branding']})"
print(login("acme","alice@acme.com"))
print(login("globex","bob@globex.com"))
print("Auth0 Organizations: each B2B tenant gets its own connection + branding")
PY
```

**Expected result:** each B2B org routed to its **own connection and branding** — Auth0
Organizations.

**Negative test:** force all B2B customers through one shared connection; they can't use their own
IdP — use **Organizations**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Developer tracks build secure OIDC/OAuth login — Auth Code + PKCE for public clients, proper
token handling, and extension via Okta hooks and Auth0 Actions/Organizations for customer (B2C/B2B)
identity.

- [ ] I can choose the right OAuth flow.
- [ ] I can handle tokens safely in a public client.
- [ ] I can add an Auth0 Action / Okta hook.
- [ ] I can model an Auth0 B2B organization.
- [ ] I completed Labs 7.1–7.4 including each negative test.
