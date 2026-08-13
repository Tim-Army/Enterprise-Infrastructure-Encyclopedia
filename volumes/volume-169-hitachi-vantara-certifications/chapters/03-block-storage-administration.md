# Chapter 03: Block Storage Administration

## Learning Objectives

- Provision block storage — pools, LDEVs, and host presentation.
- Apply efficiency features — thin provisioning and tiering.
- Monitor and manage capacity and performance.
- Recognize what the VSP 360 Storage Administration credential (HQT-6742) validates.

*Cert relevance: this is the Qualified Professional VSP 360 Storage Administration exam (HQT-6742).*

## Provisioning block storage

The core daily work of a storage administrator is **provisioning** — giving hosts the storage they need. On a VSP the flow is:

- **Pools** — aggregate physical capacity (drives, parity groups) into a **pool** of usable space.
- **LDEVs (logical devices) / LUNs** — carve **logical volumes** out of a pool. An LDEV is the unit of storage you present to a host.
- **Host groups and mapping** — define the **hosts** (by their WWNs/initiators), then **map** LDEVs to them over the SAN (Fibre Channel or iSCSI) so the host sees the volume.
- **Ports and paths** — present volumes on multiple **ports/paths** for redundancy and performance (multipathing).

So the chain is **pool → LDEV → map to host**. Getting it right — correct size, correct host, redundant paths — is the administrator's fundamental task, and exactly what the VSP 360 Storage Administration exam tests. The lab provisions an LDEV to a host.

## Thin provisioning and tiering

Modern arrays use **efficiency features** so you do not waste capacity:

- **Thin provisioning (Dynamic Provisioning)** — present a volume of a given **virtual** size but consume **physical** capacity only as data is written. You can **over-provision** (allocate more virtual than physical) and add physical capacity as usage grows — but you must **monitor** so the pool does not fill.
- **Tiering (Dynamic Tiering)** — automatically move **hot** (frequently accessed) data to **fast** media (flash) and **cold** data to slower/cheaper media, optimizing cost and performance without manual effort.
- **Data reduction** — compression and deduplication to store more in less.

These features make storage **efficient and self-optimizing**, but they require the administrator to **understand and monitor** them (an over-provisioned pool that fills causes an outage). Knowing how thin provisioning and tiering work is core competency. The lab models thin provisioning and tiering.

## Monitoring capacity and performance

Provisioning is not "set and forget"; administrators **monitor** the array's health:

- **Capacity** — pool utilization (especially with thin provisioning), growth trends, and **thresholds/alerts** before a pool fills.
- **Performance** — IOPS, throughput, and **latency** per volume/port; spotting bottlenecks and hot spots.
- **Health** — component status (controllers, drives, paths), and responding to failures (a failed drive triggers a RAID rebuild).

Proactive monitoring — catching a filling pool or a latency spike **before** it becomes an incident — is what separates a good storage admin from a reactive one. Hitachi Ops Center Analyzer ([Ch 6](06-hitachi-ops-center.md)) provides deep analytics for this. The lab monitors pool capacity against a threshold.

## The VSP 360 Storage Administration credential

The **Qualified Professional VSP 360 Storage Administration** credential (exam **HQT-6742**: 35 questions, 60 minutes, 65% to pass, $100) validates exactly this chapter's skills — **provisioning, monitoring, troubleshooting, and enterprise storage operations** on VSP using the VSP 360 management experience. It is a **Professional-level HQT (Qualification)** credential ([Ch 1](01-the-hitachi-vantara-program.md)) — a role-based competency exam, the mainstream target for a storage administrator. Deeper, hands-on mastery is validated by the **HCE Certification** credentials (Specialist/Expert). The lab exercises the administration workflow end to end.

## Hands-On Lab

Python models provisioning, thin provisioning, tiering, and capacity monitoring. **Cost:** none.

### Lab 3.1 — Provision and monitor block storage

**Objective:** Create a pool, provision a thin LDEV to a host, tier data, and monitor capacity.

```bash
python3 - <<'EOF'
# VSP block storage administration: pool -> LDEV -> map to host, thin + tiering + monitor
class Pool:
    def __init__(self, name, physical_gb):
        self.name=name; self.physical=physical_gb; self.virtual_allocated=0; self.used=0
        self.ldevs=[]
    def create_ldev(self, name, virtual_gb, host):   # thin provisioning
        self.virtual_allocated += virtual_gb
        self.ldevs.append({"name":name,"virtual":virtual_gb,"host":host,"written":0})
        over = self.virtual_allocated > self.physical
        return f"LDEV '{name}' ({virtual_gb}GB virtual) -> host '{host}'  [over-provisioned={over}]"
    def write(self, ldev_name, gb):   # physical consumed only as data is written
        for l in self.ldevs:
            if l["name"]==ldev_name: l["written"]+=gb; self.used+=gb
    def utilization(self): return round(100*self.used/self.physical,1)

pool = Pool("pool-1", physical_gb=1000)
print("BLOCK STORAGE ADMINISTRATION — pool -> LDEV -> host (thin provisioned):\n")
print("   " + pool.create_ldev("db-vol", 800, "db-server"))
print("   " + pool.create_ldev("vm-vol", 600, "esxi-01"))   # 800+600=1400 virtual > 1000 physical
print(f"   pool: {pool.physical}GB physical, {pool.virtual_allocated}GB virtual allocated (over-provisioned)")

# write data (consume physical), then monitor
pool.write("db-vol", 300); pool.write("vm-vol", 250)
print(f"\n   after writes: {pool.used}GB physical used -> utilization {pool.utilization()}%")

# TIERING: move hot data to flash, cold to slower media
print("\n   DYNAMIC TIERING: 'db-vol' hot -> FLASH tier; old snapshots cold -> HDD tier")

# MONITOR against threshold
THRESHOLD = 80
status = "ALERT: pool filling — add capacity" if pool.utilization() >= THRESHOLD else "OK"
print(f"\n   CAPACITY MONITOR: utilization {pool.utilization()}% vs threshold {THRESHOLD}% -> {status}")
print()
print("Provision by POOL -> LDEV -> map to HOST. THIN PROVISIONING allows over-provisioning")
print("(1400GB virtual on 1000GB physical) consuming physical only as data is written — so you")
print("MUST monitor utilization against a threshold (fill = outage). DYNAMIC TIERING moves hot")
print("data to flash automatically. Provision + monitor + troubleshoot is the VSP 360 Admin cert (HQT-6742).")
EOF
```

**Expected result:** A pool with two thin-provisioned LDEVs mapped to hosts (over-provisioned virtual capacity), data writes consuming physical capacity, tiering hot data to flash, and capacity monitoring against a threshold. The lesson is VSP block administration: provision pool→LDEV→host, use thin provisioning and tiering for efficiency, and monitor capacity so an over-provisioned pool never fills — the competency the VSP 360 Storage Administration credential (HQT-6742) validates.

**Negative test:** Over-provisioning thin volumes and never monitoring the pool. The pool fills as data is written, and all volumes on it fail at once; thin provisioning requires active capacity monitoring with thresholds and alerts to be safe.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Provisioning understood — pools, LDEVs/LUNs, host groups, mapping, and multipathing.
- [ ] Efficiency features understood — thin provisioning (with monitoring), tiering, and data reduction.
- [ ] Monitoring understood — capacity thresholds, performance (IOPS/latency), and health.
- [ ] The VSP 360 Storage Administration credential placed — HQT-6742, the Professional HQT storage exam.

## See also

- [Chapter 02 — Hitachi Storage and the VSP Platform](02-hitachi-storage-and-vsp.md) — the platform this administers.
- [Chapter 05 — Data Protection and Replication](05-data-protection-and-replication.md) — protecting the volumes provisioned here.
- [Chapter 06 — Hitachi Ops Center](06-hitachi-ops-center.md) — the management suite that automates and analyzes this.
