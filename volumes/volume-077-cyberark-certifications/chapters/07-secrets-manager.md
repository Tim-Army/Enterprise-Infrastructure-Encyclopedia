# Chapter 07: Secrets Manager

## Learning Objectives

- Describe CyberArk Secrets Manager (Conjur and Credential Providers).
- Remove hardcoded secrets from applications and pipelines.
- Apply policy-as-code for machine identities.
- Understand secretless and dynamic secrets.
- Complete a walkthrough for each Secrets Manager topic.

## Theory and Architecture

**Secrets Manager** extends privileged access to **non-human identities** — applications, scripts,
containers, and CI/CD pipelines that need credentials (database passwords, API keys, cloud keys).
Hardcoding these secrets in code, config files, or pipeline variables is a top source of breaches.
CyberArk addresses it two ways: **Credential Providers** (agents on the app host that fetch secrets
from the Vault at runtime so they're never stored in the app), and **Conjur** (a
secrets-management platform for **DevOps and cloud-native** workloads, with **policy-as-code** — you
declare which machine identities can access which secrets, versioned in Git). Advanced patterns
include **dynamic secrets** (short-lived credentials created on demand and revoked after use) and
**secretless** (the app connects through a broker that injects the credential, so the app never sees
it at all). The goal: **no secret in source, config, or image** — machine identities authenticate and
retrieve secrets securely at runtime. This chapter teaches each with a hands-on defensive walkthrough
(removing a hardcoded secret, policy-as-code, and dynamic/secretless patterns).

## Design Considerations

Never store secrets in **code, config, images, or pipeline logs**. Use **Credential Providers** for
traditional apps and **Conjur** for cloud-native/DevOps. Declare access with **policy-as-code**
(least privilege per machine identity). Prefer **dynamic, short-lived** secrets and **secretless**
where possible. Rotate and audit.

## Implementation and Automation

The labs remove a hardcoded secret, write access policy, and use dynamic/secretless retrieval.

## Validation and Troubleshooting

Confirm the Secrets Manager model:

```text
Secrets Manager: secure secrets for non-human identities (apps/CI-CD/containers). Credential Providers (agent fetches from Vault) + Conjur (DevOps/cloud, policy-as-code).
Patterns: dynamic secrets (short-lived, on-demand) + secretless (broker injects; app never sees the secret). Goal: no secret in source/config/image.
```

Common pitfalls: secrets in **environment variables / pipeline logs**; and one **shared** static
secret for all services.

## Security and Best Practices

Remove secrets from **code/config/images**, retrieve at runtime via **Credential Providers/Conjur**,
declare **least-privilege policy-as-code**, and prefer **dynamic/secretless**. Rotate and audit. All
work is defensive.

## Hands-On Lab

Secrets Manager walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 7.1 — Remove a hardcoded secret

**Objective:** Fetch at runtime instead.

```python
python3 - <<'PY'
# BEFORE (bad): secret in source
bad = 'db_password = "P@ssw0rd123"'
# AFTER (good): fetch from Secrets Manager at runtime
good = 'db_password = secrets_client.get("db/prod/password")   # Credential Provider / Conjur'
print("bad :", bad)
print("good:", good)
print("Secrets Manager: no secret in source; retrieved securely at runtime")
PY
```

**Expected result:** the hardcoded secret replaced by a **runtime fetch** — the core Secrets Manager
pattern.

**Negative test:** commit the password to Git "temporarily"; it lives in history forever — **never**
hardcode it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Write access policy-as-code (Conjur)

**Objective:** Least privilege for a machine identity.

```python
python3 - <<'PY'
# Conjur-style policy (declarative, versioned in Git)
policy="""
- !host web-app-prod
- !variable db/prod/password
- !permit
    role: !host web-app-prod
    privileges: [ read, execute ]
    resource: !variable db/prod/password
"""
print(policy.strip())
print("Conjur: web-app-prod may read ONLY db/prod/password (least privilege, in Git)")
PY
```

**Expected result:** a **policy-as-code** grant scoping one host to one secret — Conjur least
privilege.

**Negative test:** grant every host access to every secret; one compromised app leaks all — scope
**per identity per secret**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Use a dynamic (short-lived) secret

**Objective:** Reduce the value of a leak.

```python
python3 - <<'PY'
import time
def issue_dynamic_secret(ttl=300):
    return {"cred":"temp-abc123","expires_in_s":ttl,"revoke_after_use":True}
s=issue_dynamic_secret()
print("dynamic secret:", s)
print("Dynamic secrets: created on demand, auto-expire (a leaked one is soon useless)")
PY
```

**Expected result:** a **short-lived** credential that auto-expires — dynamic secrets.

**Negative test:** hand out a long-lived static key to a pipeline; if leaked it's valid for months —
use **dynamic** secrets.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Apply the secretless pattern

**Objective:** Keep the secret from the app entirely.

```python
python3 - <<'PY'
def app_connect(mode):
    if mode=="secretless":
        return "app connects via broker; broker injects credential; app never sees it"
    return "app reads secret into memory (still better than hardcoding, but app holds it)"
print("secretless:", app_connect("secretless"))
print("fetch     :", app_connect("fetch"))
PY
```

**Expected result:** the **secretless** broker path where the app never holds the credential — the
strongest pattern.

**Negative test:** assume fetching at runtime is the only option; **secretless** removes the secret
from the app entirely where supported — prefer it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Secrets Manager secures machine-identity secrets via Credential Providers and Conjur, removing
hardcoded secrets, declaring least-privilege policy-as-code, and using dynamic and secretless patterns
— no secret in source, config, or image.

- [ ] I can remove a hardcoded secret.
- [ ] I can write access policy-as-code (Conjur).
- [ ] I can use a dynamic secret.
- [ ] I can apply the secretless pattern.
- [ ] I completed Labs 7.1–7.4 including each negative test.
