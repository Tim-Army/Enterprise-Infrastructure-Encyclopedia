# Chapter 06: Consultant and API Access Management

## Learning Objectives

- Approach complex, multi-environment Okta deployments (Consultant).
- Design a custom authorization server and OAuth 2.0 scopes.
- Protect APIs with access tokens and scopes.
- Handle migrations and integrations at scale.
- Complete a walkthrough for each Consultant/API topic.

## Theory and Architecture

The **Okta Certified Consultant** validates implementing Okta in **complex, real-world**
environments — multiple orgs, migrations, deep integrations, and edge cases beyond standard admin
work. A core Consultant skill is **API Access Management** — Okta as an **OAuth 2.0 authorization
server** protecting APIs. Here Okta issues **access tokens** to clients (apps/services), scoped by
**OAuth scopes** (fine-grained permissions like `read:orders`) and shaped by **claims** and
**access policies** on a **custom authorization server**. APIs validate the token's **signature,
issuer, audience, expiry, and scopes** before serving a request. Consultants also handle
**tenant-to-tenant migrations**, **coexistence** with legacy IdPs, and **automation** of
configuration. The theme is **designing identity for scale and edge cases** while keeping tokens
least-privilege and short-lived. This chapter teaches each with a hands-on defensive walkthrough
(authorization-server design, scope enforcement, token validation).

## Design Considerations

Use a **custom authorization server** per API domain with least-privilege **scopes**. Keep access
tokens **short-lived** and validate all claims (iss/aud/exp/scope) at the API. Plan **migrations**
with coexistence and rollback. Automate config for **repeatability** across environments. Document
edge cases.

## Implementation and Automation

The labs design scopes, enforce them at an API, and validate a token.

## Validation and Troubleshooting

Confirm the API-access model:

```text
Consultant = complex deployments (multi-org, migrations, integrations, automation).
API Access Management: Okta = OAuth 2.0 auth server -> access tokens scoped by OAuth scopes + shaped by claims/policies on a custom auth server.
API validates: signature + iss + aud + exp + scope. Tokens least-privilege + short-lived.
```

Common pitfalls: **over-scoped** or long-lived tokens; and APIs that skip **audience/scope**
validation (accept any token).

## Security and Best Practices

Least-privilege **scopes**, **short-lived** tokens, full **claim validation** at the API, and
repeatable automated config. Plan migrations with rollback. All work is defensive.

## Hands-On Lab

Consultant/API walkthroughs. **Shared prerequisites** — `python3`, a developer org. **Cost:** none.

### Lab 6.1 — Design least-privilege OAuth scopes

**Objective:** Fine-grained API permissions.

```python
python3 - <<'PY'
api_scopes={"orders-api":["read:orders","write:orders"],"reports-api":["read:reports"]}
client={"name":"mobile-app","granted":["read:orders"]}   # only what it needs
for api,scopes in api_scopes.items(): print(f"{api}: available {scopes}")
print(f"client '{client['name']}' granted:", client["granted"], "(least privilege)")
PY
```

**Expected result:** the client granted only **read:orders** — least-privilege scoping (API Access
Management).

**Negative test:** grant the mobile app **write:orders** it never uses; that widens blast radius —
grant the **minimum** scope.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Enforce scope at the API

**Objective:** Check the token before serving.

```python
python3 - <<'PY'
def handle(request_scope_needed, token_scopes):
    return "200 OK" if request_scope_needed in token_scopes else "403 Forbidden (missing scope)"
print("GET /orders  ->", handle("read:orders", ["read:orders"]))
print("DELETE /orders ->", handle("delete:orders", ["read:orders"]))
print("API enforces the required scope on every request")
PY
```

**Expected result:** the read allowed, the delete **403** for missing scope — API-side enforcement.

**Negative test:** trust that the client only calls what it should; a compromised client will try
more — **enforce scope at the API**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Validate an access token

**Objective:** Verify before trusting.

```python
python3 - <<'PY'
import time
token={"iss":"https://org.okta.com/oauth2/aus1","aud":"orders-api","exp":time.time()-10,"scope":"read:orders"}
expected={"iss":"https://org.okta.com/oauth2/aus1","aud":"orders-api"}
checks={"issuer":token["iss"]==expected["iss"],"audience":token["aud"]==expected["aud"],
        "not expired":token["exp"]>time.time()}
print("validation:",checks)
print("verdict:", "REJECT" if not all(checks.values()) else "ACCEPT")
PY
```

**Expected result:** the token **REJECTED** (expired) despite correct issuer/audience — full token
validation.

**Negative test:** validate only the signature and skip **exp/aud**; an expired or wrong-audience
token passes — check **all** claims.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Plan a migration with coexistence

**Objective:** Move without downtime.

```python
python3 - <<'PY'
plan=["Stand up new Okta org + integrations","Coexist: route new apps to Okta, legacy to old IdP",
      "Migrate users in waves (with rollback)","Cut over remaining apps","Decommission legacy IdP"]
for i,step in enumerate(plan,1): print(f"{i}. {step}")
print("Consultant: phased migration with coexistence + rollback (no big-bang)")
PY
```

**Expected result:** a phased **coexistence** migration with rollback — the Consultant approach.

**Negative test:** big-bang cut over everything at once; one failure breaks all logins — migrate in
**waves**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Consultant handles complex deployments and API Access Management — Okta as an OAuth 2.0
authorization server issuing least-privilege, short-lived, fully-validated scoped tokens — plus
phased migrations with coexistence and rollback.

- [ ] I can design least-privilege OAuth scopes.
- [ ] I can enforce scope at the API.
- [ ] I can validate an access token fully.
- [ ] I can plan a coexistence migration.
- [ ] I completed Labs 6.1–6.4 including each negative test.
