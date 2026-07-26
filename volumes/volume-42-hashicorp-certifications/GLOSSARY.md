# Volume XLII Glossary

Definitions for terms used in **Volume XLII — HashiCorp Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Auto-unseal** — A Vault seal type that uses a cloud KMS or an HSM to unseal
automatically, removing human-held unseal keys from the process. Used in Chapter
05.

**Barrier** — Vault's cryptographic boundary: all data is encrypted before it
reaches the storage backend, so the backend only ever holds ciphertext. Used in
Chapters 04 and 05.

**Consul** — HashiCorp's service-networking product (service discovery, service
mesh via Connect, and a KV store); its Associate exam retired 15 July 2026. Used
in Chapter 06.

**Dynamic secret** — A secret Vault generates on demand with a lease and revokes
automatically, as opposed to a long-lived static secret. Used in Chapter 04.

**`for_each`** — A Terraform meta-argument that creates one instance per key in a
map/set, giving stable addressing (preferred over `count` for that reason). Used
in Chapter 03.

**HCP Terraform** — HashiCorp's hosted platform (formerly Terraform Cloud) for
remote state, remote runs, RBAC, and policy — the collaborative Terraform
workflow. Used in Chapters 02 and 03.

**Lease** — The TTL Vault attaches to a dynamic secret or token, after which it
is automatically revoked. Used in Chapter 04.

**Lifecycle meta-arguments** — Terraform arguments (`create_before_destroy`,
`prevent_destroy`, `ignore_changes`) that control how a resource is replaced or
protected. Used in Chapter 03.

**Module (Terraform)** — A reusable, parameterized package of Terraform
configuration with inputs and outputs. Used in Chapters 02 and 03.

**Policy (Vault)** — A set of path-and-capability grants that authorize what a
token may do; least privilege is deny-by-default. Used in Chapters 04 and 05.

**Raft (Integrated Storage)** — Vault's built-in HA storage backend; an odd node
count forms quorum and tolerates minority failures. Used in Chapter 05.

**Recertification** — Renewing a HashiCorp credential (valid two years) by passing
an exam for the same product at the same level or higher; there is no
continuing-education model. Used in Chapters 01 and 07.

**Secrets engine** — A Vault component that stores or generates secrets (KV,
transit, database, cloud); static engines store, dynamic engines generate. Used
in Chapter 04.

**State (Terraform)** — The file mapping configuration to real resources; it can
contain secrets and must be protected and manipulated with `terraform state`
subcommands. Used in Chapter 02.

**Transit engine** — Vault's encryption-as-a-service engine: it encrypts and
decrypts data with a managed key without storing the data. Used in Chapter 04.

**Vault Agent** — A client-side Vault process that auto-authenticates, caches a
token, and renders secrets into files for applications. Used in Chapter 05.

**Workspace (Terraform)** — A named, isolated state within a configuration, used
to separate environments. Used in Chapter 03.
