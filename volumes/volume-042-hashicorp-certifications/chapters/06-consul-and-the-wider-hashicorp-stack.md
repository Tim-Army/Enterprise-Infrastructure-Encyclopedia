# Chapter 06: Consul and the Wider HashiCorp Stack

## Learning Objectives

- Explain the retirement of the Consul Associate exam and what it means for the program.
- Describe Consul's core capabilities: service discovery, service mesh, and KV.
- Map the wider HashiCorp stack (Nomad, Packer, Boundary, Waypoint) and its certification status.
- Practice Consul fundamentals hands-on despite the absence of a current exam.
- Complete walkthroughs for Consul's core capability areas.

## Theory and Architecture

**Consul** is HashiCorp's **service networking** platform — service discovery, a
**service mesh** (Connect), health checking, and a distributed **key/value**
store. It remains a widely deployed product, but its certification changed: the
**Consul Associate (003) exam was retired on 15 July 2026** (the last day to
schedule was 13 July 2026). There is currently **no active Consul certification**,
so Consul is covered here as an important **skill area** rather than an exam
track — the four active HashiCorp exams are Terraform and Vault only (Chapters
02–05).

This chapter also maps the **wider HashiCorp stack** so the program's shape is
clear:

- **Consul** — service discovery and mesh (this chapter; cert retired).
- **Nomad** — a scheduler and orchestrator for containers and non-container
  workloads (no current certification).
- **Packer** — machine-image building (no current certification).
- **Boundary** — identity-based secure remote access (no current certification).
- **Waypoint / Vagrant** — developer workflow and environments (no current
  certification).

Only **Terraform** and **Vault** currently carry certifications, at Associate and
Professional levels.

## Design Considerations

Even without an exam, Consul skills matter wherever services must **find and
securely reach each other** — it complements Kubernetes (Volume XLI), Nomad, and
VM fleets. Learn its three pillars: **service discovery** (register services, DNS/
HTTP lookup), **service mesh** (mTLS between services with **intentions** as
authorization), and the **KV store** (dynamic configuration). For the stack, know
which tool solves which problem — Terraform provisions, Vault secures secrets,
Consul connects services, Nomad schedules workloads.

## Implementation and Automation

The walkthroughs below run a local `consul agent -dev` and exercise Consul's core
capabilities — agent/catalog, service registration and discovery, the KV store,
and service-mesh intentions — plus a stack-mapping exercise.

## Validation and Troubleshooting

Confirm the program's current shape:

```text
developer.hashicorp.com/certifications:
  - active certifications: Terraform (Associate 004, Professional) and Vault (Associate 003, Professional)
  - Consul Associate: RETIRED 15 July 2026 (no replacement announced)
Check the site for any new Consul/Nomad certification before assuming one exists.
```

Common pitfalls: studying for a **Consul Associate exam that no longer exists**;
and assuming Nomad/Packer/Boundary have certifications — they do not (as of this
snapshot).

## Security and Best Practices

Run Consul with **ACLs enabled** and **TLS** in production (dev mode disables
both); use **intentions** to default-deny service-to-service traffic in the mesh;
and keep the **gossip encryption** key secret. For the wider stack, pair Consul
with **Vault** for certificate and secret management.

## References and Knowledge Checks

- developer.hashicorp.com: Consul documentation; the certification catalog (for current status); Nomad/Packer/Boundary docs.

**Knowledge checks**

1. What happened to the Consul Associate exam, and when?
2. What are Consul's three core capabilities?
3. Which two HashiCorp products currently carry certifications?

## Hands-On Lab

Walkthroughs for Consul's core capabilities and the stack. These build real
skills even though the Consul exam has retired.

**Shared prerequisites** — a Linux shell with `consul` installed; a second shell
for the foreground agent. **Cost:** none.

### Lab 6.1 — Consul: run the agent and read the catalog (service discovery core)

**Objective:** Start a dev agent and inspect its members and catalog.

```bash
consul agent -dev >/tmp/consul-dev.log 2>&1 &
sleep 2
consul members
consul catalog services
```

**Expected result:** the agent listed as `alive` in `consul members` and
`consul` in the service catalog — a running Consul with a service catalog, the
basis of discovery.

**Negative test:** run a dev agent in production; it disables **ACLs and TLS** —
dev mode is for learning only.

**Rollback:** keep the agent running for the next labs.

### Lab 6.2 — Consul: register and discover a service

**Objective:** Register a service and resolve it via Consul DNS.

```bash
consul services register -name=web -port=8080
consul catalog services | grep web
dig @127.0.0.1 -p 8600 web.service.consul +short 2>/dev/null || \
  consul catalog nodes -service=web
```

**Expected result:** `web` in the catalog and resolvable via Consul DNS
(`web.service.consul`) or `catalog nodes` — service registration and discovery.

**Negative test:** hard-code a service's IP:port in clients; services move —
resolve through **Consul** so clients follow the catalog.

**Rollback:** `consul services deregister -id=web 2>/dev/null || true`

### Lab 6.3 — Consul: the key/value store (dynamic configuration)

**Objective:** Store and read dynamic configuration in the KV store.

```bash
consul kv put app/config/log_level debug
consul kv get app/config/log_level
consul kv get -recurse app/
```

**Expected result:** `debug` returned for `app/config/log_level` and the recursive
listing under `app/` — the KV store for dynamic, centralized configuration.

**Negative test:** bake config into each service's image; the **KV store** lets
you change config centrally without a rebuild.

**Rollback:** `consul kv delete -recurse app/`

### Lab 6.4 — Consul: service mesh intentions (authorization)

**Objective:** Express service-to-service authorization with intentions.

```bash
consul intention create -allow web db 2>/dev/null \
  || echo "Intention: allow 'web' -> 'db'; default-deny everything else in the mesh (Connect + mTLS)."
consul intention list 2>/dev/null | head || echo "(intentions authorize mesh traffic by service identity)"
```

**Expected result:** an intention allowing `web → db` (or the concept) — the
service-mesh authorization model where identity, not IP, governs traffic.

**Negative test:** allow all mesh traffic by default; **intentions** should
default-deny and allow only required service pairs.

**Rollback:** `consul intention delete web db 2>/dev/null || true; pkill -f 'consul agent -dev' 2>/dev/null || true`

### Lab 6.5 — The wider stack: map tools to problems

**Objective:** Match each HashiCorp tool to the problem it solves and its cert
status.

```bash
python3 - <<'PY'
stack = {"Terraform":"provision infrastructure (IaC)  [CERT: Assoc 004 + Pro]",
         "Vault":"secrets + encryption           [CERT: Assoc 003 + Pro]",
         "Consul":"service discovery + mesh       [CERT: retired 15 Jul 2026]",
         "Nomad":"workload scheduling/orchestration [CERT: none]",
         "Packer":"build machine images           [CERT: none]",
         "Boundary":"identity-based remote access  [CERT: none]"}
for tool,desc in stack.items(): print(f"{tool:10} -> {desc}")
PY
```

**Expected result:** each tool mapped to its purpose and certification status —
only Terraform and Vault currently certify.

**Negative test:** assume every HashiCorp tool has a certification; only
**Terraform** and **Vault** do today — verify before planning a path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Consul provides service discovery, a service mesh, and a KV store, but its
Associate exam **retired on 15 July 2026**, leaving **Terraform and Vault** as
the only currently certified HashiCorp products. Consul remains a valuable skill,
and the wider stack (Nomad, Packer, Boundary) solves adjacent problems without
current certifications.

- [ ] I can explain the Consul Associate retirement and its date.
- [ ] I can run a Consul agent and register/discover a service.
- [ ] I can use the KV store and describe mesh intentions.
- [ ] I can map each HashiCorp tool to its purpose and cert status.
- [ ] I completed Labs 6.1–6.5 including each negative test.
