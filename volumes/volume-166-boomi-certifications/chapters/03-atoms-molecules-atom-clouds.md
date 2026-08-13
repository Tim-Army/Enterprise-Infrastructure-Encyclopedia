# Chapter 03: Atoms, Molecules, and Atom Clouds

## Learning Objectives

- Describe the Atom — Boomi's lightweight runtime engine.
- Distinguish Atom, Molecule, and Atom Cloud and when to use each.
- Explain "design once in the cloud, deploy the runtime anywhere."
- Understand runtime placement — data residency, high availability, and hybrid.

*Cert relevance: the runtime model is core to the Runtime Architect certification and every deployment decision.*

## The Atom

The **Atom** is Boomi's signature: a **lightweight, self-contained runtime engine** that **executes your integration processes**. You design a process in the cloud on the visual canvas ([Ch 2](02-the-boomi-platform.md)), then **deploy** it to an Atom, and the Atom **runs** it — reading sources, transforming data, writing targets. The crucial property is **placement**: an Atom can run **wherever you install it** — in your own data center, in your cloud VPC, at the edge, or on a Boomi-hosted cloud. So sensitive data can be processed **close to where it lives**, while you still design and manage everything from the central cloud platform.

This split — **design centrally, execute locally** — is what makes Boomi work for enterprises with data spread across on-premises systems, multiple clouds, and regions. The Atom is the unit of runtime, and understanding it is the foundation of Boomi architecture. The lab models the Atom and design/execute split.

## Atom, Molecule, and Atom Cloud

Boomi offers **three runtime forms** to match scale and control needs:

- **Atom** — a **single-node runtime** on one server. Simple; suitable for development, smaller workloads, or a single integration server. If that node goes down, its integrations stop.
- **Molecule** — a **clustered, multi-node runtime**: several nodes act as **one logical runtime** with **load balancing and high availability**. If one node fails, the others carry the load. Use a Molecule for **production** workloads that need HA and horizontal scale, running on **your own** infrastructure.
- **Atom Cloud** — a **Boomi-hosted, multi-tenant runtime**. Boomi runs and maintains the runtime; you just deploy your processes to it. No infrastructure to manage — ideal for **cloud-to-cloud** integrations where you do not need the runtime on your own network.

The decision is a trade-off of **control vs convenience** and **scale vs simplicity**: Atom (simple, self-managed), Molecule (HA/scale, self-managed), Atom Cloud (managed, no infra). The **Runtime Architect** certification ([Ch 8](08-administration-and-architecture.md)) is precisely about choosing correctly. The lab selects a runtime per requirement.

## Design once, deploy anywhere

The Atom model delivers **"design once, deploy the runtime anywhere"**:

- You **build a process one time** in the cloud platform.
- You **deploy** it to **any Atom, Molecule, or Atom Cloud** — the **same process** runs on any of them.
- You can move or add runtimes without rebuilding integrations — deploy the same process to a Molecule in the EU and another in the US for data residency, for example.

Because the runtime is **decoupled** from the design, Boomi covers **cloud, on-premises, and hybrid** with one design surface. This portability is a major reason enterprises pick an iPaaS: the integration logic is an asset independent of where it runs. The lab deploys one process to multiple runtimes.

## Runtime placement

Choosing **where** an Atom runs is an architecture decision driven by real constraints:

- **Data residency** — if data must stay in a region or on-premises (regulation, privacy), place the runtime **there** so data is processed locally and never leaves.
- **High availability** — production integrations that cannot go down need a **Molecule** (multi-node) rather than a single Atom.
- **Connectivity** — to reach an on-premises database behind a firewall, run the Atom **inside** that network rather than routing data out to the cloud.
- **Managed vs self-managed** — pure cloud-to-cloud flows with no residency constraints are simplest on an **Atom Cloud**.

Good runtime placement balances **compliance, availability, connectivity, and operational burden**. This is the essence of Boomi runtime architecture and a frequent exam theme. The lab places runtimes against requirements. *(Runtime placement here parallels the Secure-Agent placement in [Informatica IDMC (CLXV Ch 2)](../../volume-165-informatica-certifications/chapters/02-idmc-platform.md) — the same design-in-cloud, execute-near-data idea.)*

## Hands-On Lab

Python models the runtime forms, one-design-many-runtimes portability, and placement decisions. **Cost:** none.

### Lab 3.1 — Choose and place Boomi runtimes

**Objective:** Select Atom / Molecule / Atom Cloud per requirements and deploy one process to many.

```bash
python3 - <<'EOF'
RUNTIMES = {
  "Atom":       {"nodes": 1,   "ha": False, "hosting": "self-managed", "use": "dev / small / single server"},
  "Molecule":   {"nodes": "N", "ha": True,  "hosting": "self-managed", "use": "production HA + horizontal scale"},
  "Atom Cloud": {"nodes": "N", "ha": True,  "hosting": "Boomi-hosted", "use": "cloud-to-cloud, no infra to manage"},
}
def choose(req):
    if req.get("data_residency") == "on-prem" or req.get("reach_onprem"):
        return "Molecule" if req.get("ha") else "Atom"     # must run inside the network
    if req.get("ha"):
        return "Molecule"                                   # self-managed HA
    return "Atom Cloud"                                     # managed, cloud-to-cloud

print("BOOMI RUNTIME FORMS:\n")
for r, d in RUNTIMES.items():
    print(f"   {r:11} nodes={str(d['nodes']):2} HA={str(d['ha']):5} {d['hosting']:13} — {d['use']}")

print("\nRUNTIME SELECTION per requirement:")
REQS = {
  "EU customer data must stay on-prem, production": {"data_residency": "on-prem", "ha": True},
  "Salesforce <-> NetSuite, cloud only":            {},
  "Read on-prem Oracle DB behind firewall":         {"reach_onprem": True},
  "Dev sandbox, single integration":                {},
}
for name, req in REQS.items():
    print(f"   {choose(req):11} <- {name}")

print("\nDESIGN ONCE, DEPLOY ANYWHERE:")
process = "p_sync_customers"
for target in ["Molecule-EU", "Molecule-US", "AtomCloud-Global"]:
    print(f"   deploy {process} -> {target}  (same process, different runtime)")
print()
print("An ATOM is a lightweight runtime you place where the data lives; a MOLECULE clusters")
print("Atoms for production HA/scale; an ATOM CLOUD is Boomi-hosted for cloud-to-cloud with no")
print("infra. Design a process ONCE in the cloud and deploy it to ANY runtime — placement is")
print("driven by data residency, HA, and connectivity. Choosing well is the Runtime Architect cert.")
EOF
```

**Expected result:** A runtime comparison (Atom single-node, Molecule clustered HA, Atom Cloud Boomi-hosted) and a selector that picks a Molecule for on-prem production data, an Atom Cloud for cloud-only flows, and an Atom to reach an on-prem database — then deploys one process to multiple runtimes. The lesson is Boomi's runtime model: design once in the cloud and deploy the same process to Atom, Molecule, or Atom Cloud, with placement driven by data residency, high availability, and connectivity — the core of the Runtime Architect certification.

**Negative test:** Forcing every integration onto a single Atom in one region. On-prem data behind a firewall is unreachable, production has no HA, and EU data-residency rules are violated; matching the runtime form and placement to each requirement is what the runtime model is for.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Atom understood — a lightweight runtime engine that executes processes wherever placed.
- [ ] Atom / Molecule / Atom Cloud distinguished — single-node, clustered HA, and Boomi-hosted.
- [ ] Design once, deploy anywhere understood — the same process runs on any runtime.
- [ ] Runtime placement understood — driven by data residency, HA, connectivity, and management burden.

## See also

- [Chapter 02 — The Boomi Enterprise Platform](02-the-boomi-platform.md) — the design surface the runtime executes.
- [Chapter 08 — Administration and Architecture](08-administration-and-architecture.md) — the Administrator and Runtime Architect tracks.
- [Volume CLXV — Informatica IDMC](../../volume-165-informatica-certifications/README.md) — the parallel Secure-Agent design-in-cloud/execute-near-data model.
