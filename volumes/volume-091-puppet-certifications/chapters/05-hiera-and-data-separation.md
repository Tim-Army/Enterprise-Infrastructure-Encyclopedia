# Chapter 05: Hiera and Data Separation

## Learning Objectives

- Explain the Hiera hierarchy and data separation.
- Look up data with `lookup`.
- Use automatic parameter lookup for class parameters.
- Reason about external data and encrypted secrets.
- Complete a walkthrough for each Hiera topic.

## Theory and Architecture

**Data separation** keeps configuration **data** out of Puppet **code**, and **Hiera** is Puppet's
built-in hierarchical key/value lookup system that provides it. A **`hiera.yaml`** defines a **hierarchy**
of data sources, ordered from most specific to most general — e.g., per-node (`nodes/%{facts.hostname}`),
per-OS (`os/%{facts.os.family}`), then `common`. When Puppet needs a value, it walks the hierarchy and
returns the **first match** (or, for hashes/arrays, can merge). **Automatic parameter lookup** ties this
to classes: when you `include ntp`, Puppet automatically looks up `ntp::server` in Hiera to fill the
class parameter — so the same code gets different data per node/environment without editing manifests.
Hiera backends read **YAML/JSON** files or **external data** (a database, an ENC, a custom backend via
`hiera-eyaml` for **encrypted secrets**). Separating data from code is what makes Puppet modules reusable
across environments. This chapter teaches Hiera with hands-on walkthroughs.

## Design Considerations

Design the **hierarchy** from specific (node) to general (common) so overrides work naturally. Put
**data** in Hiera and keep **code** generic — parameterize classes (Chapter 03) and let **automatic
parameter lookup** fill them. Encrypt secrets with **hiera-eyaml** (never plain-text passwords in data).
Use **external data** (an ENC or database) where the source of truth lives elsewhere. Keep the hierarchy
shallow enough to reason about.

## Implementation and Automation

The labs define a hierarchy, look up a value, and reason about automatic parameter lookup and encrypted
secrets — the data separation the domain validates.

## Validation and Troubleshooting

Confirm Hiera:

```text
hiera.yaml: ordered hierarchy (specific -> general): node -> os -> common; first match wins (or merge)
lookup('key') resolves down the hierarchy; automatic parameter lookup fills class params (ntp::server)
Backends: YAML/JSON files; external data (ENC/DB); hiera-eyaml for ENCRYPTED secrets
Data separation: data in Hiera, code stays generic -> reusable across environments
```

Common pitfalls: a hierarchy ordered **general before specific** (overrides never take effect); and
**secrets in plain-text** Hiera — use **hiera-eyaml**.

## Security and Best Practices

Encrypt secrets with **hiera-eyaml**, never commit plain-text passwords, and scope data by environment.
Data separation keeps secrets out of code. All work is authorized administration.

## Hands-On Lab

Hiera walkthroughs. **Shared prerequisites** — open-source Puppet 8 with a Hiera data directory, and
`puppet lookup`. **Cost:** none.

### Lab 5.1 — Define a hierarchy

**Objective:** Order data sources specific → general.

```bash
mkdir -p /tmp/hdemo/data
cat > /tmp/hdemo/hiera.yaml <<'YAML'
---
version: 5
defaults:
  datadir: data
  data_hash: yaml_data
hierarchy:
  - name: "Per-node"
    path: "nodes/%{facts.networking.hostname}.yaml"
  - name: "Per-OS"
    path: "os/%{facts.os.family}.yaml"
  - name: "Common"
    path: "common.yaml"
YAML
echo "---" && cat /tmp/hdemo/hiera.yaml | grep -A1 "name:"
```

```text
  - name: "Per-node"   (most specific, checked first)
  - name: "Per-OS"
  - name: "Common"     (most general, checked last)
```

**Expected result:** a hierarchy from per-node down to common — the lookup order.

**Negative test:** list `common` first; its values would win over per-node overrides — order **specific
first**.

**Rollback:**

```bash
rm -rf /tmp/hdemo
```

### Lab 5.2 — Look up a value

**Objective:** Resolve a key down the hierarchy.

```bash
mkdir -p /tmp/hdemo/data/os
cat > /tmp/hdemo/data/common.yaml <<'YAML'
ntp::server: pool.ntp.org
YAML
cat > /tmp/hdemo/data/os/Debian.yaml <<'YAML'
ntp::server: debian.pool.ntp.org
YAML
puppet lookup ntp::server --hiera_config /tmp/hdemo/hiera.yaml \
  --facts <(echo '{"os":{"family":"Debian"},"networking":{"hostname":"web1"}}')
```

```text
--- debian.pool.ntp.org
```

**Expected result:** the Debian-specific value overriding the common value — first-match resolution.

**Negative test:** expect `common.yaml` to win when an OS-specific file exists; the **more specific**
match wins.

**Rollback:**

```bash
rm -rf /tmp/hdemo
```

### Lab 5.3 — Reason about automatic parameter lookup

**Objective:** Fill class parameters from Hiera.

```python
python3 - <<'PY'
# class ntp (String $server) { ... } ; include ntp
# Puppet automatically looks up 'ntp::server' in Hiera to fill $server
print("include ntp -> APL looks up 'ntp::server' -> value from Hiera fills the class parameter")
print("Result: same code, different data per node/env -> no manifest edits")
PY
```

**Expected result:** the class parameter filled automatically from Hiera — data-driven, code stays
generic.

**Negative test:** hardcode the server in the class or pass it in every manifest; use **automatic
parameter lookup** from Hiera.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Reason about encrypted secrets

**Objective:** Keep secrets out of plain-text data.

```python
python3 - <<'PY'
plain  = "db_password: SuperSecret123"           # BAD: plain text in Hiera
eyaml  = "db_password: ENC[PKCS7,MIIBiQ...==]"    # GOOD: hiera-eyaml encrypted
print("Plain YAML :", plain, "  <- committed secret, exposed")
print("hiera-eyaml:", eyaml, "  <- encrypted at rest, decrypted at catalog compile")
print("Rule: encrypt secrets with hiera-eyaml; never commit plain-text passwords")
PY
```

**Expected result:** the encrypted (`ENC[...]`) form versus the plain-text form — secrets protected with
hiera-eyaml.

**Negative test:** store a database password as plain YAML in the repo; use **hiera-eyaml** encryption.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Hiera separates data from code through an ordered hierarchy (specific to general) resolved by first match,
filling class parameters automatically via automatic parameter lookup so generic code gets per-node data,
reading YAML/JSON or external backends, and protecting secrets with hiera-eyaml encryption.

- [ ] I can define a Hiera hierarchy.
- [ ] I can look up a value down the hierarchy.
- [ ] I can reason about automatic parameter lookup.
- [ ] I can reason about encrypted secrets with hiera-eyaml.
- [ ] I completed Labs 5.1–5.4 including each negative test.
