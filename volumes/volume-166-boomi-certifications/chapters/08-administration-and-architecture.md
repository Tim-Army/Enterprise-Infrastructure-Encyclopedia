# Chapter 08: Administration and Architecture

## Learning Objectives

- Describe the Administrator role — environments, deployment, and monitoring.
- Distinguish the Administrator certifications (Associate, Windows/Linux Operational).
- Explain the Architect role — integration and runtime architecture.
- Understand Boomi AI — Companion, Agentstudio, and Boomi GPT.

*Cert relevance: this chapter covers the Administrator and Architect tracks, plus Boomi AI (training only).*

## The Administrator role

Someone has to **run** the platform — deploy integrations, manage runtimes, and keep everything healthy. That is the **Administrator**. Where developers build processes ([Ch 4](04-building-integrations.md)), administrators handle **operations**:

- **Environments** — logical targets like **Dev**, **Test**, and **Production**, each mapped to runtimes ([Ch 3](03-atoms-molecules-atom-clouds.md)). Administrators manage promoting processes through environments.
- **Deployment** — packaging processes and **deploying** them to the right environment/runtime, managing versions and rollbacks.
- **Monitoring** — watching **process executions**, catching failures, viewing logs, and setting up **alerts** so problems are seen early.
- **Runtime operations** — installing, patching, and maintaining **Atoms and Molecules**, including the underlying **Windows or Linux** hosts.

The **Administrator** track has three certifications reflecting this operational depth. The lab models environments, deployment, and monitoring.

## The Administrator certifications

- **Associate Administrator** — validates **foundational** administration: environments, deployment, user/role management, and monitoring in the platform.
- **Professional Windows Operational Administrator** — validates operating Boomi runtimes on **Windows** hosts — installation, services, patching, and OS-level runtime management.
- **Professional Linux Operational Administrator** — the same for **Linux** hosts.

The split into Windows and Linux Operational Administrator credentials reflects that a **Molecule** runs on real servers you must operate at the OS level — a genuinely different skill from building integrations. The lab covers deployment and monitoring operations.

## The Architect role

**Architects** design **how** integrations and runtimes are structured at scale — the decisions that make a Boomi implementation robust, performant, and governable. Boomi has two Associate Architect credentials:

- **Associate Integration Architect** — validates designing **integration solutions**: patterns, reuse, error handling, and how many processes fit together into a coherent architecture rather than a sprawl of one-off flows.
- **Associate Runtime Architect** — validates designing the **runtime topology** ([Ch 3](03-atoms-molecules-atom-clouds.md)): choosing Atom vs Molecule vs Atom Cloud, sizing and clustering for load and HA, and **placing runtimes** for data residency and connectivity.

Architecture is where the earlier chapters come together: an architect decides the **process design patterns** (Integration Architect) and the **runtime deployment topology** (Runtime Architect) for the whole implementation. The lab makes an architecture decision.

## Boomi AI

**Boomi AI** brings generative AI into the platform. It is **training-based** today (no dedicated certification yet), but it is central to how modern Boomi work is done:

- **Boomi Companion** — an **AI-assisted build** helper that suggests mappings, next steps, and configurations as you build, and helps you **co-plan and validate** integrations.
- **Agentstudio** — a capability to **build AI agents** that act within your integrations and processes.
- **Boomi GPT** — a **conversational** interface to the platform — describe what you want and get help building it.

The pattern mirrors AI across the industry: the platform's metadata and your intent feed AI that **accelerates building**. The course *Co-Creating with Boomi Companion* teaches durable habits for working with an AI build assistant. The lab models AI-assisted suggestions. *(This parallels AI engines elsewhere — e.g. [CLAIRE in Informatica (Vol CLXV Ch 8)](../../volume-165-informatica-certifications/chapters/08-governance-and-catalog.md) and GenAI in [Pega (Vol CLXIV Ch 7)](../../volume-164-pega-certifications/README.md).)*

## Hands-On Lab

Python models administration (environments, deployment, monitoring), an architecture decision, and AI-assisted build. **Cost:** none.

### Lab 8.1 — Operate and architect the platform

**Objective:** Promote through environments, monitor executions, choose an architecture, and use AI suggestions.

```bash
python3 - <<'EOF'
# --- ADMINISTRATOR: environments + deployment + monitoring ---
ENVIRONMENTS = {"Dev": "Atom-dev", "Test": "Atom-test", "Prod": "Molecule-prod-cluster"}
print("1) ADMINISTRATOR — environments (env -> runtime):")
for env, rt in ENVIRONMENTS.items():
    print(f"      {env:5} -> {rt}")
process = "p_sync_customers v3"
print(f"\n   deploy '{process}': Dev -> Test -> Prod (promote through environments)")
executions = [{"id": 1, "status": "COMPLETE"}, {"id": 2, "status": "ERROR"}, {"id": 3, "status": "COMPLETE"}]
errs = [e for e in executions if e["status"] == "ERROR"]
print(f"   MONITOR: {len(executions)} executions, {len(errs)} error(s) -> ALERT on execution {errs[0]['id']}")

# --- ARCHITECT: choose runtime topology for a requirement ---
def runtime_arch(req):
    if req["prod"] and req["ha"]: return "Molecule (multi-node HA) — Runtime Architect"
    if req["cloud_only"]:         return "Atom Cloud (managed) — Runtime Architect"
    return "Atom (single node)"
print("\n2) ARCHITECT — runtime topology decision:")
req = {"prod": True, "ha": True, "cloud_only": False}
print(f"      requirement={req}")
print(f"      -> {runtime_arch(req)}")

# --- BOOMI AI: Companion suggests as you build ---
def companion_suggest(source_field):
    KB = {"cust_name": "map -> CustomerName (upper-case)", "email": "map -> Email (validate format)",
          "order_amt": "map -> Amount (convert to number)"}
    return KB.get(source_field, "no suggestion")
print("\n3) BOOMI AI — Companion suggestions while building a map:")
for f in ["cust_name", "email", "order_amt"]:
    print(f"      source '{f}' -> Companion suggests: {companion_suggest(f)}")
print()
print("ADMINISTRATORS promote processes Dev->Test->Prod across ENVIRONMENTS (each mapped to a")
print("runtime), MONITOR executions, and ALERT on errors (Associate + Windows/Linux Operational")
print("Admin). ARCHITECTS choose the runtime topology — a Molecule for prod HA (Runtime Architect)")
print("— and integration patterns (Integration Architect). BOOMI AI (Companion/Agentstudio/GPT)")
print("suggests mappings as you build — training today, accelerating the whole platform.")
EOF
```

**Expected result:** An administration model promoting a process through Dev/Test/Prod environments (each mapped to a runtime), monitoring executions and alerting on an error; an architecture decision selecting a Molecule for a production HA requirement; and Boomi Companion suggesting field mappings. The lesson is the operate-and-architect side of Boomi — Administrators manage environments, deployment, and monitoring (with Windows/Linux Operational credentials for OS-level runtime work), Architects design integration patterns and runtime topology, and Boomi AI accelerates building.

**Negative test:** Developing straight in production with no environments, monitoring, or architecture review. A bad deploy takes down live integrations with no test gate, failures go unnoticed, and the runtime is undersized; environments, monitoring, and architecture are what make Boomi production-grade.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Administrator role understood — environments, deployment, monitoring, and runtime operations.
- [ ] The Administrator certifications placed — Associate, and Windows/Linux Operational Administrator.
- [ ] The Architect role understood — Integration Architect (patterns) and Runtime Architect (topology).
- [ ] Boomi AI understood — Companion, Agentstudio, and Boomi GPT (training, no cert yet).

## See also

- [Chapter 03 — Atoms, Molecules, and Atom Clouds](03-atoms-molecules-atom-clouds.md) — the runtime topology architects design and admins operate.
- [Chapter 09 — Choosing Your Boomi Path](09-choosing-your-boomi-path.md) — sequencing these tracks into a career.
- [Volume CLXV — Informatica](../../volume-165-informatica-certifications/README.md) — CLAIRE, a parallel AI engine on a data platform.
