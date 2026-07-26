# Chapter 05: Vault Operations Professional

## Learning Objectives

- Explain what the Vault Operations Professional certifies and its lab-based format.
- List the eight Vault Operations Professional objectives.
- Configure, monitor, secure, and scale a production Vault deployment.
- Build fault-tolerant Vault with HA and understand HSM integration and Vault Agent.
- Complete a per-objective walkthrough for each Professional objective.

## Theory and Architecture

The **Vault Operations Professional** is the hands-on, **lab-based** credential
for engineers who **deploy, operate, and scale Vault** in production. It is **four
hours, lab-based plus multiple-choice**: you configure real Vault servers, not
just answer questions. Eight objectives:

| # | Objective |
|---|-----------|
| 1 | Create a working Vault server configuration given a scenario |
| 2 | Monitor a Vault environment |
| 3 | Employ the Vault security model |
| 4 | Build fault-tolerant Vault environments |
| 5 | Understand hardware security module (HSM) integration |
| 6 | Scale Vault for performance |
| 7 | Configure access control |
| 8 | Configure Vault Agent |

## Design Considerations

This exam is about **running Vault well**: writing the server **HCL config**
(listener, storage, seal), enabling **telemetry** and **audit devices** for
monitoring, applying the **security model** (barrier, seal, least privilege),
achieving HA with **Integrated Storage (Raft)** and **performance/DR
replication** (Enterprise), understanding **auto-unseal/HSM** (seal type),
**performance standbys** and caching for scale, fine-grained **access control**,
and **Vault Agent** for auto-auth and secret templating. Prepare by operating a
multi-node Vault, since the exam is hands-on.

## Implementation and Automation

The labs below use Vault server **configuration files** and the `vault` CLI
(against the dev server where a full cluster is impractical) to exercise each
objective — config, monitoring, security model, HA, HSM/auto-unseal, scaling,
access control, and Vault Agent.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
developer.hashicorp.com/certifications > Vault Operations Professional:
  - eight objectives, four hours (incl. break), lab-based + multiple-choice
  - hands-on: operate a real (ideally multi-node) Vault to prepare
```

Common pitfalls: forgetting an **audit device** (no forensic trail); running a
single node and calling it HA; and confusing **auto-unseal** (a seal type using
KMS/HSM) with **replication** (Enterprise HA/DR).

## Security and Best Practices

Always enable an **audit device**; use **auto-unseal** (KMS/HSM) or carefully
managed Shamir shares; run **Raft** with an odd node count for quorum; separate
the **root token** (revoke after setup); rotate the encryption key and the
unseal keys; and monitor **telemetry** and seal status.

## References and Knowledge Checks

- developer.hashicorp.com: *Vault Operations Professional* objectives; Vault operations and reference-architecture docs.

**Knowledge checks**

1. What three stanzas make up a minimal Vault server config?
2. What is the difference between auto-unseal and replication?
3. What does Vault Agent's auto-auth do for an application?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every Professional objective**.

**Shared prerequisites** — the `vault` CLI; the dev server from Chapter 01 for
CLI labs; a text editor for config labs. **Cost:** none.

### Lab 5.1 — Objective 1: Create a working Vault server configuration

**Objective:** Write a minimal production-style server config (Raft storage).

```bash
cat > vault.hcl <<'HCL'
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "node1"
}
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = false
  tls_cert_file = "/etc/vault/tls/cert.pem"
  tls_key_file  = "/etc/vault/tls/key.pem"
}
seal "awskms" { kms_key_id = "alias/vault-unseal" }
api_addr     = "https://vault.example.com:8200"
cluster_addr = "https://node1.example.com:8201"
HCL
echo "storage + listener + seal = a working, auto-unsealed, TLS-enabled server config."
```

**Expected result:** a config with `raft` storage, a TLS `listener`, and an
`awskms` auto-unseal `seal` — the scenario-based server configuration of
Objective 1.

**Negative test:** set `tls_disable = true` in production; Vault traffic carries
secrets — always enable TLS.

**Cleanup:** `rm -f vault.hcl`

### Lab 5.2 — Objective 2: Monitor a Vault environment

**Objective:** Enable an audit device and read telemetry configuration.

```bash
vault audit enable file file_path=/tmp/vault-audit.log 2>/dev/null || true
vault audit list
echo "Telemetry: add a `telemetry { prometheus_retention_time = \"24h\" }` stanza; scrape /v1/sys/metrics."
```

**Expected result:** a `file` audit device listed and the telemetry concept — the
monitoring and forensic trail of Objective 2.

**Negative test:** operate without an **audit device**; you cannot investigate an
incident with no record — always enable auditing.

**Cleanup:** `vault audit disable file 2>/dev/null || true`

### Lab 5.3 — Objective 3: Employ the Vault security model

**Objective:** Demonstrate the barrier and least-privilege model.

```bash
vault status | grep -E 'Sealed|Seal Type'
vault token capabilities root secret/data/app 2>/dev/null || \
  echo "Barrier encrypts all data before storage; policies enforce least privilege on every path."
```

**Expected result:** the seal status/type and the barrier + least-privilege
concept — Vault's security model (Objective 3).

**Negative test:** grant broad policies for convenience; the security model is
**deny-by-default least privilege** — grant only what each path needs.

**Cleanup:** none.

### Lab 5.4 — Objective 4: Build fault-tolerant Vault environments

**Objective:** Describe Raft HA and quorum.

```bash
python3 - <<'PY'
print("Integrated Storage (Raft): 3 or 5 nodes; one active, others standby.")
print("Quorum = (N/2)+1: a 3-node cluster tolerates 1 failure; 5 tolerates 2.")
print("Enterprise adds performance + DR replication across clusters.")
PY
```

**Expected result:** the Raft HA model and quorum math (odd node counts) — fault
tolerance for Objective 4.

**Negative test:** run a 2-node cluster expecting HA; even counts risk split-
brain and can't form quorum after one loss — use **odd** counts (3/5).

**Cleanup:** none.

### Lab 5.5 — Objective 5: Understand HSM integration

**Objective:** Describe HSM/KMS auto-unseal (seal stanza).

```bash
cat <<'HCL'
seal "pkcs11" {
  lib      = "/usr/vault/lib/libCryptoki2_64.so"
  slot     = "0"
  key_label = "vault-hsm-key"
}
HCL
echo "HSM (PKCS#11) or cloud KMS provides auto-unseal + master-key protection (Enterprise for HSM)."
```

**Expected result:** a `pkcs11` seal stanza and the HSM auto-unseal/key-
protection role — HSM integration (Objective 5).

**Negative test:** store unseal keys in a wiki for convenience; an **HSM/KMS**
auto-unseal removes human-held keys from the loop — use it where required.

**Cleanup:** none.

### Lab 5.6 — Objective 6: Scale Vault for performance

**Objective:** Describe performance standbys and caching.

```bash
python3 - <<'PY'
print("Performance Standbys (Enterprise): standby nodes serve read-only requests -> horizontal read scale.")
print("Client-side caching via Vault Agent reduces load; batch tokens are lightweight (not persisted).")
print("Tune: lease TTLs, token type (batch vs service), and storage performance.")
PY
```

**Expected result:** performance standbys, caching, and batch tokens as scaling
levers — Objective 6.

**Negative test:** issue millions of long-lived **service** tokens; they persist
in storage — use **batch** tokens for high-volume, ephemeral workloads.

**Cleanup:** none.

### Lab 5.7 — Objective 7: Configure access control

**Objective:** Apply fine-grained policy with allowed parameters.

```bash
vault policy write ops - <<'HCL'
path "secret/data/prod/*" {
  capabilities = ["read"]
}
path "sys/leases/revoke" { capabilities = ["update"] }
HCL
vault policy read ops
```

**Expected result:** an `ops` policy granting read on prod secrets and lease
revocation only — fine-grained access control (Objective 7).

**Negative test:** grant `sys/*`; that includes dangerous endpoints — grant only
the specific `sys/` paths an operator needs.

**Cleanup:** none.

### Lab 5.8 — Objective 8: Configure Vault Agent

**Objective:** Write a Vault Agent auto-auth and template config.

```bash
cat > agent.hcl <<'HCL'
auto_auth {
  method "approle" {
    config = { role_id_file_path = "/etc/vault/role_id", secret_id_file_path = "/etc/vault/secret_id" }
  }
  sink "file" { config = { path = "/run/vault/token" } }
}
template {
  source      = "/etc/vault/db.tpl"
  destination = "/run/secrets/db.env"
}
HCL
echo "Vault Agent: auto-authenticates (AppRole), caches a token, and renders secrets into files for apps."
```

**Expected result:** an agent config with **auto-auth** (AppRole) and a
**template** rendering secrets to a file — Vault Agent for app integration
(Objective 8).

**Negative test:** hard-code a Vault token in every app; **Vault Agent**
auto-authenticates and renews so apps never handle raw tokens.

**Cleanup:** `rm -f agent.hcl`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Vault Operations Professional certifies production Vault operations across
eight objectives — server configuration, monitoring, the security model, fault
tolerance (Raft HA), HSM/auto-unseal, scaling, access control, and Vault Agent —
in a four-hour lab-based exam. It rewards operating a real, highly-available
Vault securely.

- [ ] I can list the eight Professional objectives.
- [ ] I can write a server config with storage, listener, and seal.
- [ ] I can enable auditing and explain Raft HA and quorum.
- [ ] I can describe HSM auto-unseal, scaling, and Vault Agent.
- [ ] I completed Labs 5.1–5.8 including each negative test.
