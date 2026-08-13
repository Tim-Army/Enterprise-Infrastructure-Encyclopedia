# Chapter 08: Converged, Hyperconverged, and Hybrid Cloud

## Learning Objectives

- Distinguish converged (UCP) from hyperconverged infrastructure.
- Explain how Hitachi integrates compute, storage, and networking.
- Describe hybrid-cloud data infrastructure and cloud tiering.
- Understand infrastructure as a managed platform.

*Cert relevance: this is the Infrastructure / converged (UCP) track and hybrid-cloud content.*

## Converged infrastructure (UCP)

Storage does not stand alone — it is part of a stack with **compute** and **networking**. **Converged infrastructure** packages these together as a **pre-integrated, validated system**, and Hitachi's is **UCP (Unified Compute Platform)**. Instead of assembling and certifying servers, switches, and storage yourself, you get an **engineered system** where the components are **pre-tested to work together**, with a **single support** relationship.

The benefit is **speed and reduced risk**: deploy a validated stack quickly rather than integrating parts and debugging interoperability. UCP often underpins **VMware or database** environments where a known-good, supported platform matters. Converged infrastructure keeps the components **distinct** (separate storage arrays, servers, switches) but **integrated and validated** together. The lab models a converged stack.

## Converged versus hyperconverged

The two integration models differ in **architecture**:

- **Converged (UCP)** — compute, storage, and networking are **separate components** integrated and validated together; storage is a **shared array** (VSP). You can **scale each layer independently** (add storage without adding servers).
- **Hyperconverged (HCI)** — compute and storage are **combined in the same nodes**, with storage **software-defined** across the nodes' local disks; you scale by **adding nodes** (compute + storage together).

The trade-off: **converged** suits workloads needing **independent scaling** and **enterprise shared storage** (large databases, mixed workloads); **hyperconverged** suits **simplicity and node-based growth** (VDI, general virtualization). Knowing which model fits which need — and that UCP is Hitachi's converged offering — is the infrastructure competency. The lab contrasts the models.

## Hybrid-cloud data infrastructure

Modern infrastructure spans **on-premises and public cloud**, and Hitachi Vantara positions itself as a **hybrid-cloud data infrastructure** company:

- **Cloud tiering** — move **cold** data from on-premises storage to **public-cloud object storage** (S3) automatically, keeping hot data fast on-premises and cold data cheap in the cloud, in one managed namespace ([Ch 4](04-file-and-object-storage.md)).
- **Data mobility** — replicate and move data between on-premises and cloud for DR, migration, or bursting.
- **Consistent management** — manage on-premises and cloud-resident data through common tooling (Ops Center, [Ch 6](06-hitachi-ops-center.md)).

The goal is one **data fabric** spanning locations, so data lives in the **right place** for cost and performance without being trapped. This hybrid positioning is increasingly central to storage certifications as pure on-premises gives way to hybrid. The lab models cloud tiering. *(Hybrid-cloud data mobility parallels the multi-cloud themes across the encyclopedia's cloud volumes.)*

## Infrastructure as a managed platform

The through-line of this chapter is that Hitachi Vantara sells **infrastructure as a managed platform**, not just parts: **UCP** delivers a validated stack, **Ops Center** operates it with automation and analytics, and **hybrid-cloud** capabilities extend it beyond the data center. For the enterprise, this means less time integrating and operating infrastructure and more time on the applications and data that matter — infrastructure becomes a **reliable, managed foundation** rather than a project. Recognizing this platform framing — and where converged, hyperconverged, and cloud fit — completes the infrastructure picture and helps you place the certification tracks. The lab synthesizes the platform view.

## Hands-On Lab

Python models converged vs hyperconverged, a UCP stack, and hybrid-cloud tiering. **Cost:** none.

### Lab 8.1 — Converged, hyperconverged, and cloud tiering

**Objective:** Contrast converged and hyperconverged, model a UCP stack, and tier data to cloud.

```bash
python3 - <<'EOF'
# converged (UCP) vs hyperconverged (HCI)
MODELS = {
  "Converged (UCP)":      {"storage":"shared array (VSP)","scale":"each layer independently","fits":"large DBs, shared storage, independent scaling"},
  "Hyperconverged (HCI)": {"storage":"software-defined in nodes","scale":"add nodes (compute+storage)","fits":"VDI, general virtualization, simplicity"},
}
print("CONVERGED vs HYPERCONVERGED:")
for m, d in MODELS.items():
    print(f"   {m:22} storage={d['storage']:26} scale={d['scale']}")
    print(f"   {'':22} fits: {d['fits']}")

# a UCP converged stack: pre-integrated, validated
print("\nUCP (Unified Compute Platform) — validated converged stack:")
for layer in ["compute (servers)","networking (switches)","storage (VSP array)"]:
    print(f"   [{layer}] pre-integrated + validated + single support")

# hybrid cloud: tier cold data to public cloud object storage
data = [("db-hot", "flash on-prem", 5), ("archive-cold", "on-prem", 400)]   # (name, location, days_since_access)
print("\nHYBRID-CLOUD TIERING:")
for name, loc, idle in data:
    if idle > 90:
        print(f"   '{name}' (idle {idle}d) -> TIER to public-cloud object storage (S3, cheaper) — one namespace")
    else:
        print(f"   '{name}' (idle {idle}d) -> keep HOT on-prem (fast)")
print()
print("CONVERGED (UCP) integrates separate compute/network/storage as a VALIDATED stack (scale")
print("each layer independently, shared VSP); HYPERCONVERGED combines compute+storage in nodes")
print("(scale by adding nodes). HYBRID-CLOUD tiers cold data to public-cloud object storage while")
print("hot stays on-prem — one data fabric. Infrastructure as a managed platform — the UCP/cloud track.")
EOF
```

**Expected result:** A contrast of converged (UCP, separate validated components, independent scaling, shared VSP) versus hyperconverged (combined nodes, software-defined, node-based scaling), a UCP validated stack, and hybrid-cloud tiering of cold data to cloud object storage. The lesson is Hitachi infrastructure: converged UCP delivers a pre-integrated validated stack scaled per layer, hyperconverged combines compute and storage in nodes, and hybrid-cloud tiering moves cold data to the cloud in one namespace — infrastructure as a managed platform.

**Negative test:** Choosing hyperconverged for a workload that needs a large, independently scaled shared storage array, or keeping all cold archive data on expensive on-premises flash. The architecture fights the workload, or cost balloons; matching converged vs hyperconverged to the need and tiering cold data to cloud is the point.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Converged infrastructure (UCP) understood — a pre-integrated, validated compute/storage/network stack.
- [ ] Converged vs hyperconverged understood — separate validated components (independent scaling) vs combined nodes.
- [ ] Hybrid-cloud data infrastructure understood — cloud tiering, data mobility, and consistent management.
- [ ] Infrastructure as a managed platform understood — a reliable managed foundation, not just parts.

## See also

- [Chapter 06 — Hitachi Ops Center](06-hitachi-ops-center.md) — operating the infrastructure platform.
- [Chapter 04 — File and Object Storage](04-file-and-object-storage.md) — object storage and cloud tiering.
- [Chapter 09 — Choosing Your Hitachi Vantara Path](09-choosing-your-hitachi-vantara-path.md) — placing the infrastructure track.
