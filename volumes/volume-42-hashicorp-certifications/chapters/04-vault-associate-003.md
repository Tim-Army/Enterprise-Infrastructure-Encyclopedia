# Chapter 04: Vault Associate (003)

## Learning Objectives

- Explain what the Vault Associate (003) certifies and its exam mechanics.
- List the nine Vault Associate objectives.
- Operate Vault's core workflow with the CLI — auth, policies, tokens, leases, and secrets.
- Apply encryption-as-a-service and Vault's architecture concepts.
- Complete a per-objective walkthrough for each Vault Associate objective.

## Theory and Architecture

The **Vault Associate (003)** validates practical knowledge of **HashiCorp
Vault** — the secrets-management and data-protection platform. It covers how
clients **authenticate**, how **policies** authorize them, how **tokens** and
**leases** work, the **secrets engines** that generate or store secrets, and
**encryption as a service**, plus Vault's architecture. It is **one hour,
online-proctored, multiple-choice** (version 003 supersedes 002). Nine
objectives:

| # | Objective |
|---|-----------|
| 1 | Authentication methods |
| 2 | Vault policies |
| 3 | Vault tokens |
| 4 | Vault leases |
| 5 | Secrets engines |
| 6 | Encryption as a service |
| 7 | Vault architecture fundamentals |
| 8 | Vault deployment architecture |
| 9 | Access management architecture |

## Design Considerations

Vault's model is **authenticate → get a token → policy authorizes → access
secrets**, and most secrets are **dynamic and leased** (generated on demand,
revoked automatically). Master the CLI for each step, understand **policies** as
path-and-capability grants, and know the difference between **static** (KV) and
**dynamic** secrets engines, plus **transit** (encryption as a service, where
Vault never stores the data). Architecture objectives cover the **storage
backend**, **seal/unseal**, and **HA**. The labs below run against a local `vault
-dev` server.

## Implementation and Automation

Each lab exercises one objective with the real `vault` CLI against the dev server
from Chapter 01 — auth methods, policies, tokens, leases, secrets engines,
transit encryption, and the architecture concepts.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
developer.hashicorp.com/certifications > Vault Associate (003):
  - nine objectives, one hour, multiple-choice, online proctored
  - study 003 (002 is retired)
```

Common pitfalls: confusing **authentication** (proving identity → a token) with
**authorization** (policies on that token); leaving secrets **static** when a
**dynamic** engine is safer; and forgetting that **transit** encrypts without
storing — Vault is a crypto service there, not a vault of ciphertext.

## Security and Best Practices

Use least-privilege **policies** (deny by default, grant specific paths/
capabilities), prefer **dynamic secrets** with short **leases**, never use the
**root token** for routine work, and enable **audit devices**. Keep unseal keys
split (Shamir) or use auto-unseal.

## References and Knowledge Checks

- developer.hashicorp.com: *Vault Associate (003)* objectives and tutorials; Vault documentation.

**Knowledge checks**

1. What is the sequence from authentication to accessing a secret?
2. What is the difference between a static and a dynamic secret?
3. What does the transit engine do that a KV engine does not?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every Vault Associate objective**.

**Shared prerequisites** — the running `vault -dev` server from Chapter 01 with
`VAULT_ADDR` and `VAULT_TOKEN=root` exported. **Cost:** none.

### Lab 4.1 — Objective 1: Authentication methods

**Objective:** Enable an auth method and authenticate to get a token.

```bash
vault auth enable userpass
vault write auth/userpass/users/alice password=pw policies=default
vault login -method=userpass username=alice password=pw | grep -E 'token|policies'
```

**Expected result:** the `userpass` method enabled and a **login** returning a
token with the `default` policy — authentication producing a token (Objective 1).

**Negative test:** treat the root token as an auth method; **auth methods** issue
scoped tokens per identity — root is for setup only.

**Cleanup:** `vault login root >/dev/null`

### Lab 4.2 — Objective 2: Vault policies

**Objective:** Write and apply a least-privilege policy.

```bash
vault policy write app - <<'HCL'
path "secret/data/app/*" { capabilities = ["read", "list"] }
HCL
vault policy read app
```

**Expected result:** the `app` policy granting only `read`/`list` on
`secret/data/app/*` — path-and-capability authorization (Objective 2).

**Negative test:** grant `path "*" { capabilities = ["sudo","root"] }`; that is
full access — scope policies to the exact paths and capabilities needed.

**Cleanup:** none.

### Lab 4.3 — Objective 3: Vault tokens

**Objective:** Create a scoped token and inspect it.

```bash
vault token create -policy=app -ttl=15m -format=json | \
  python3 -c 'import sys,json; d=json.load(sys.stdin)["auth"]; print("ttl:",d["lease_duration"],"policies:",d["token_policies"])'
```

**Expected result:** a token with a 900-second TTL and the `app` policy — tokens
as the carrier of identity and authorization (Objective 3).

**Negative test:** issue long-lived, broadly-scoped tokens; short **TTLs** and
narrow policies limit blast radius — scope and expire tokens.

**Cleanup:** none.

### Lab 4.4 — Objective 4: Vault leases

**Objective:** Observe and revoke a lease.

```bash
vault secrets enable -path=kv kv-v2 2>/dev/null || true
vault kv put kv/demo value=s3cr3t >/dev/null
vault lease list sys/leases/lookup 2>/dev/null | head || \
  echo "Dynamic secrets (e.g., database creds) get a LEASE with a TTL and are auto-revoked."
```

**Expected result:** the leasing concept — dynamic secrets carry a **lease**
(TTL) and Vault revokes them automatically at expiry (Objective 4).

**Negative test:** issue credentials that never expire; **leases** ensure secrets
are short-lived and revocable — rely on them.

**Cleanup:** none.

### Lab 4.5 — Objective 5: Secrets engines

**Objective:** Use the KV v2 engine to store and version a secret.

```bash
vault kv put kv/app/db username=appuser password=pw1
vault kv put kv/app/db username=appuser password=pw2
vault kv get -field=password kv/app/db
vault kv get -version=1 -field=password kv/app/db
```

**Expected result:** the current password `pw2` and version 1's `pw1` — the KV v2
secrets engine with versioning (Objective 5).

**Negative test:** store long-lived cloud keys statically forever; prefer a
**dynamic** secrets engine that generates short-lived credentials on demand.

**Cleanup:** none.

### Lab 4.6 — Objective 6: Encryption as a service

**Objective:** Encrypt and decrypt data with the transit engine (Vault never
stores it).

```bash
vault secrets enable transit 2>/dev/null || true
vault write -f transit/keys/appkey >/dev/null
CT=$(vault write -field=ciphertext transit/encrypt/appkey \
      plaintext=$(printf 'card-1234' | base64))
echo "ciphertext: $CT"
vault write -field=plaintext transit/decrypt/appkey ciphertext="$CT" | base64 -d; echo
```

**Expected result:** a `vault:v1:...` ciphertext and, on decrypt, `card-1234` —
encryption as a service where Vault holds the key but not the data (Objective 6).

**Negative test:** ship encryption keys to every app; **transit** centralizes key
management — apps call Vault to encrypt/decrypt.

**Cleanup:** none.

### Lab 4.7 — Objective 7: Vault architecture fundamentals

**Objective:** Inspect seal status and the storage/token model.

```bash
vault status | grep -E 'Sealed|Storage|HA|Version'
echo "Barrier: Vault encrypts everything before the storage backend; unseal reconstructs the master key."
```

**Expected result:** `Sealed false`, the storage type, and version — the
seal/barrier model that protects data at rest (Objective 7).

**Negative test:** assume the storage backend can read secrets; Vault encrypts
**before** storage (the barrier) — the backend only sees ciphertext.

**Cleanup:** none.

### Lab 4.8 — Objective 8: Vault deployment architecture

**Objective:** Describe HA and unseal for production deployment.

```bash
python3 - <<'PY'
print("Production: Integrated Storage (Raft) or Consul backend; multiple nodes for HA (active/standby).")
print("Unseal: Shamir key shares (threshold) OR auto-unseal via a cloud KMS/HSM.")
print("Dev mode (this lab) is single-node, in-memory, auto-unsealed — never for production.")
PY
```

**Expected result:** the HA and unseal options for a real deployment (Raft/
Consul storage, Shamir or auto-unseal) — deployment architecture (Objective 8).

**Negative test:** run a single dev node in production; you need **HA storage**
and a real **unseal** strategy — dev mode is for learning only.

**Cleanup:** none.

### Lab 4.9 — Objective 9: Access management architecture

**Objective:** Relate identities, entities, and groups.

```bash
vault write identity/entity name=alice-entity policies=app -format=json 2>/dev/null | \
  python3 -c 'import sys,json; print("entity id:", json.load(sys.stdin)["data"]["id"])' 2>/dev/null \
  || echo "Identity: entities (a person/app) tie multiple auth aliases together; groups grant shared policies."
```

**Expected result:** an identity **entity** (or the concept) tying auth aliases to
policies, with **groups** for shared access — the identity/access-management
architecture (Objective 9).

**Negative test:** manage each auth method's users in isolation; the **identity**
system unifies them into entities and groups — model identity centrally.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Vault Associate (003) certifies practical Vault across nine objectives —
authentication, policies, tokens, leases, secrets engines, transit encryption,
and Vault's architecture, deployment, and identity model — in a one-hour
multiple-choice exam (study 003, not the retired 002). Its throughline is
authenticate → token → policy → leased secret.

- [ ] I can list the nine Vault Associate objectives.
- [ ] I can enable an auth method, write a policy, and issue a scoped token.
- [ ] I can use KV and transit engines and explain leases.
- [ ] I can describe seal/unseal, HA, and the identity model.
- [ ] I completed Labs 4.1–4.9 including each negative test.
