# Chapter 06: Hitachi Ops Center

## Learning Objectives

- Describe Hitachi Ops Center as the unified storage-management suite.
- Distinguish the modules — Administrator, Automator, Protector, and Analyzer.
- Explain automation and analytics for storage operations.
- Understand infrastructure-as-a-service and self-service storage.

*Cert relevance: this is the Hitachi Ops Center track (Administration, Automation, Protection, Analyzer).*

## The unified management suite

Managing a fleet of storage arrays by hand does not scale, so Hitachi provides **Hitachi Ops Center** — a **unified software suite** for **managing, automating, protecting, and analyzing** Hitachi storage from one place. Where the previous chapters covered administering a **single** array, Ops Center is how you operate **many** arrays as a governed, automated, observable **estate**. It turns storage from a set of boxes into a **managed service**.

Ops Center is a distinct certification track because managing at scale — with automation and analytics — is a different competency from configuring one array. The suite is **modular**; you learn the modules relevant to your role. The lab models the suite.

## The modules

Hitachi Ops Center has four core modules:

- **Ops Center Administrator** — the **management** interface: provision, configure, and monitor storage across arrays from one console (the modern successor to element managers).
- **Ops Center Automator** — **automation** of storage tasks via **templates and service catalogs**: define a "provision 500GB gold-tier volume" service once, and let it run consistently (and via self-service). This is **infrastructure-as-code** for storage.
- **Ops Center Protector** — **data-protection orchestration**: manage snapshots and replication ([Ch 5](05-data-protection-and-replication.md)) through policies rather than manual commands, coordinating local and remote protection.
- **Ops Center Analyzer** — **performance and capacity analytics**: monitor health, spot bottlenecks, forecast capacity, and troubleshoot across the estate with deep telemetry.

Each module maps to an operational need — **manage** (Administrator), **automate** (Automator), **protect** (Protector), **analyze** (Analyzer) — and to certification content. The lab maps the modules to tasks.

## Automation and analytics

The two modules that most transform storage operations are **Automator** and **Analyzer**:

- **Automation (Automator)** — replaces error-prone manual provisioning with **repeatable service templates**. Benefits: **consistency** (every volume built to standard), **speed** (minutes not tickets), and **self-service** (users request storage from a catalog, approved and fulfilled automatically). This is how storage keeps up with cloud-like expectations.
- **Analytics (Analyzer)** — replaces reactive firefighting with **proactive insight**: which volume is the latency hot spot, when will a pool fill, is a host's performance problem actually the storage? Deep analytics turn raw metrics into **answers and forecasts**.

Together they move storage operations from **manual and reactive** to **automated and proactive** — the modern operating model. Understanding what automation and analytics deliver is central to the Ops Center certifications. The lab runs an automation template and an analytics forecast. *(Automation and analytics for infrastructure parallel the observability and automation themes across the encyclopedia.)*

## Self-service and infrastructure-as-a-service

Ops Center Automator enables **storage-as-a-service**: a **service catalog** where consumers **request** storage (a database volume, a file share) and the request is **fulfilled automatically** to standard, with approvals and guardrails. This delivers the **cloud experience on-premises** — self-service, fast, consistent — while keeping enterprise **governance**. For the enterprise it means storage teams spend less time on repetitive provisioning and more on architecture, and consumers get what they need quickly. Recognizing this **IaaS/self-service** model — and that Automator is how Hitachi delivers it — rounds out the operational picture. The lab models a self-service request.

## Hands-On Lab

Python models the Ops Center modules, an automation template, analytics, and self-service. **Cost:** none.

### Lab 6.1 — Manage, automate, protect, and analyze

**Objective:** Map the modules, run an Automator service template, forecast capacity (Analyzer), and fulfill a self-service request.

```bash
python3 - <<'EOF'
MODULES = {
  "Administrator": "manage/provision/monitor across arrays (one console)",
  "Automator":     "automate via templates + service catalog (storage-as-code)",
  "Protector":     "orchestrate snapshots + replication by policy",
  "Analyzer":      "performance + capacity analytics, forecasting, troubleshooting",
}
print("HITACHI OPS CENTER — modules:")
for m, d in MODULES.items(): print(f"   {m:14} {d}")

# AUTOMATOR: a service template provisions consistently
def automator_service(tier, size_gb, host):
    specs = {"gold":{"media":"flash","raid":"RAID-6","protect":"Thin Image + Universal Replicator"}}
    s = specs[tier]
    return f"provisioned {size_gb}GB {tier} volume ({s['media']}, {s['raid']}, protection={s['protect']}) -> {host}"
print("\nAUTOMATOR (service template — consistent, repeatable):")
print(f"   {automator_service('gold', 500, 'db-server')}")

# ANALYZER: forecast when a pool fills (proactive)
used, capacity, growth_per_day = 700, 1000, 10   # GB
days_to_full = (capacity - used) / growth_per_day
print(f"\nANALYZER (forecast): pool {used}/{capacity}GB, +{growth_per_day}GB/day -> full in {days_to_full:.0f} days -> plan capacity now")

# SELF-SERVICE (Automator catalog): a user requests storage, fulfilled automatically
print("\nSELF-SERVICE (storage-as-a-service):")
print("   user requests 'gold 500GB' from catalog -> approved -> Automator fulfills to standard -> ready in minutes")
print()
print("OPS CENTER manages a storage ESTATE, not one array: ADMINISTRATOR (manage), AUTOMATOR")
print("(templates/self-service = storage-as-code), PROTECTOR (policy-driven snapshots+replication),")
print("ANALYZER (analytics + capacity FORECAST -> proactive). Automation + analytics move storage ops")
print("from manual/reactive to automated/proactive — the cloud experience on-prem, governed. The Ops Center certs.")
EOF
```

**Expected result:** The four Ops Center modules mapped to their roles, an Automator service template provisioning a gold volume consistently, an Analyzer forecast of when a pool will fill, and a self-service catalog request fulfilled automatically. The lesson is Hitachi Ops Center: it manages a storage estate through Administrator (manage), Automator (automate/self-service), Protector (policy-driven protection), and Analyzer (analytics/forecasting) — moving storage operations from manual and reactive to automated and proactive.

**Negative test:** Provisioning every volume by hand and reacting to capacity problems only when a pool fills. Volumes drift from standard, provisioning is slow, and outages surprise you; Automator's templates/self-service and Analyzer's forecasting are what make storage operations consistent and proactive at scale.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Ops Center understood — the unified suite for managing a storage estate at scale.
- [ ] The modules understood — Administrator (manage), Automator (automate), Protector (protect), Analyzer (analyze).
- [ ] Automation and analytics understood — templates/self-service and proactive performance/capacity insight.
- [ ] Self-service/IaaS understood — a governed storage-as-a-service catalog, the cloud experience on-premises.

## See also

- [Chapter 03 — Block Storage Administration](03-block-storage-administration.md) — the per-array administration Ops Center scales up.
- [Chapter 05 — Data Protection and Replication](05-data-protection-and-replication.md) — what Ops Center Protector orchestrates.
- [Chapter 08 — Converged, Hyperconverged, and Hybrid Cloud](08-converged-and-cloud.md) — the infrastructure Ops Center helps operate.
