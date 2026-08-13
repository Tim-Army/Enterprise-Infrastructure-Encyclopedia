# Chapter 07: Puppet Enterprise Administration

## Learning Objectives

- Explain the Puppet Enterprise architecture (primary server, agents, Puppet Server).
- Explain PuppetDB and its role.
- Reason about certificates and agent enrollment.
- Read reports and run status.
- Complete a walkthrough for each administration topic.

## Theory and Architecture

The **Administration** domain covers running the platform. **Puppet Enterprise (PE)** architecture: the
**primary server** runs **Puppet Server** (which **compiles catalogs** for agents), the **console** (web
UI), an orchestration service, and **PuppetDB**; **agents** run on managed nodes (via **pxp-agent** for
orchestration) and pull catalogs on a schedule (default every **30 minutes**). Communication is secured
by a built-in **Certificate Authority**: a new agent submits a **certificate signing request**, an admin
**signs** it, and thereafter agent↔server traffic is mutually authenticated over TLS. **PuppetDB** is the
data warehouse — it stores each node's **facts**, last **catalog**, and **reports**, and enables
**exported resources** (one node collecting resources another node exported) and rich queries (via
**PQL**). **Reports** capture each run's outcome — resources changed, failed, corrective vs intentional
changes — surfaced in the console for compliance and troubleshooting. Understanding the components,
certificates, PuppetDB, and reporting is core to administering Puppet. This chapter teaches PE
administration with hands-on walkthroughs (open-source components mirror PE's).

## Design Considerations

Size the **primary server** for the number of agents (catalog compilation is CPU-bound); scale with
**compilers** for large fleets. Guard the **CA** and sign only trusted **CSRs**. Rely on **PuppetDB** for
facts/reports/exported resources and query it with **PQL**. Monitor **reports** for failed runs and
unexpected corrective changes (drift). Keep the run interval and `--noop` policy deliberate.

## Implementation and Automation

The labs reason about the architecture, inspect agent certificate state, and read a run report — the
administration the domain validates.

## Validation and Troubleshooting

Confirm PE administration:

```text
Architecture: primary server (Puppet Server = catalog compilation + console + PuppetDB) <- agents (pxp-agent)
Agents pull catalogs on a schedule (default 30 min); secured by the built-in CA (CSR -> sign -> mutual TLS)
PuppetDB: stores facts + catalogs + reports; enables exported resources + PQL queries
Reports: resources changed/failed; corrective vs intentional changes -> compliance + troubleshooting
```

Common pitfalls: auto-signing **any** CSR (a rogue node could enroll) — sign only trusted requests; and
undersizing the **primary server** so catalog compilation lags.

## Security and Best Practices

Protect the **CA** and sign CSRs deliberately, secure PuppetDB, and review **reports** for drift and
failures. The certificate-based mutual TLS and idempotent reporting are defensive controls. All work is
authorized administration of your own infrastructure.

## Hands-On Lab

PE-administration walkthroughs. **Shared prerequisites** — a Puppet primary/agent (or open-source
`puppetserver`/`puppet`), and `python3`. **Cost:** none.

### Lab 7.1 — Reason about the architecture

**Objective:** Map the components.

```python
python3 - <<'PY'
components = {
  "Primary server": "Puppet Server (compiles catalogs) + console + orchestrator + PuppetDB + CA",
  "Agent":          "pxp-agent; pulls catalog every ~30 min; applies + reports",
  "PuppetDB":       "facts + catalogs + reports; exported resources; PQL queries",
  "CA":             "signs agent CSRs -> mutual TLS between agent and server",
}
for c, role in components.items(): print(f"{c:16}: {role}")
PY
```

**Expected result:** the PE components and their roles — the platform you administer.

**Negative test:** expect agents to compile their own catalogs; the **primary server** compiles them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Inspect agent certificate state

**Objective:** Manage enrollment via the CA.

```bash
# on the primary server: list pending/signed agent certificates
puppetserver ca list --all
```

```text
Signed Certificates:
    web1.example.com   (SHA256) ...
Requested Certificates:
    db1.example.com    (SHA256) ...   # pending CSR -> sign to enroll
```

**Expected result:** a signed agent and a pending CSR — the certificate lifecycle the CA manages.

**Negative test:** enable **autosign `*`** to save time; a rogue node could enroll — sign trusted CSRs
explicitly (`puppetserver ca sign --certname db1.example.com`).

**Rollback:** none (read-only).

### Lab 7.3 — Read a run report

**Objective:** See what changed.

```python
python3 - <<'PY'
report = {
  "node": "web1", "status": "changed", "resources_total": 142,
  "changed": 3, "failed": 0,
  "corrective": 1,   # a resource had drifted and was fixed
  "intentional": 2,  # new declared changes applied
}
for k, v in report.items(): print(f"{k:16}: {v}")
print("Corrective change = drift Puppet fixed; failed>0 -> investigate")
PY
```

**Expected result:** a run report distinguishing corrective (drift) from intentional changes with zero
failures — the compliance/troubleshooting view.

**Negative test:** ignore reports and assume nodes are compliant; **read reports** for failed runs and
unexpected corrective changes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Reason about PuppetDB and exported resources

**Objective:** Use the data warehouse.

```python
python3 - <<'PY'
# node A exports its backend info; the load balancer collects all exported backends
print("web1: @@haproxy::balancermember { 'web1': ip => '10.0.0.11' }  # exported (@@)")
print("web2: @@haproxy::balancermember { 'web2': ip => '10.0.0.12' }  # exported")
print("lb1 : Haproxy::Balancermember <<| |>>  # collects all exported members from PuppetDB")
print("PQL: inventory[certname]{ facts.os.family = 'Debian' } -> query nodes")
PY
```

**Expected result:** exported resources collected via PuppetDB to build a load balancer from each web
node — PuppetDB's cross-node value.

**Negative test:** hardcode every backend in the LB config; **export/collect** via PuppetDB so it updates
as nodes change.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Puppet Enterprise runs a primary server (Puppet Server compiling catalogs, plus console, orchestrator,
CA, and PuppetDB) serving agents that pull catalogs on a schedule over CA-signed mutual TLS; PuppetDB
warehouses facts, catalogs, and reports and powers exported resources and PQL; and run reports
distinguish corrective (drift) from intentional changes for compliance and troubleshooting.

- [ ] I can explain the PE architecture and Puppet Server.
- [ ] I can inspect and manage agent certificates.
- [ ] I can read a run report.
- [ ] I can reason about PuppetDB and exported resources.
- [ ] I completed Labs 7.1–7.4 including each negative test.
