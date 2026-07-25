# Chapter 04: Virtualization, Storage, and Data Protection Lab

![Lab topology for this chapter: two ESXi hosts backed by a vSAN witness form the HQ cluster with vSAN, HA, and DRS fully automated; the domain controllers, control host, and Linux client migrate in without losing domain authentication. A backup host exports a verified backup of one domain controller, and a branch-site host receives a vSphere Replication copy within its configured RPO window. As a negative test, one ESXi host is forced offline while running a domain controller; vSphere HA detects the unreachable host and restarts that VM on the surviving host within a few minutes, and vSAN resynchronizes to green once the failed host rejoins. A restore test deliberately corrupts a file, then imports the verified backup to a temporary VM and confirms the file matches its pre-corruption state before that temporary VM is deleted.](../../../diagrams/volume-13-integrated-enterprise-labs/chapter-04-vsan-ha-backup-restore-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: an HQ vSphere/vSAN cluster with HA and a backup/replication pipeline, tested against a host failure and a real restore.*

## Learning Objectives

- Build a two-node vSphere cluster with a vSAN witness appliance, and
  migrate the standalone VMs from Chapters 01–03 into managed cluster
  inventory.
- Configure vSphere HA and DRS and prove HA actually restarts a workload
  after a simulated host failure.
- Stand up a scripted, VADP-aligned backup workflow to an independent
  repository host, and prove a restore works before trusting it.
- Configure vSphere Replication from HQ to a BR1 DR target host as a
  foundation for the resilience testing in [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md).
- Diagnose the most common nested-ESXi networking defect (promiscuous
  mode/forged transmits) flagged as a recurring risk in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md).

## Theory and Architecture

Every VM built so far — `ctrl01`, `dc01`, `dc02`, `linux01` — has been
running on whatever standalone hypervisor the reader provisioned in
Chapters 01 and 02, with no shared storage, no HA, and no formal lifecycle
management. This chapter consolidates them into a real vSphere cluster,
following [Volume V](../../volume-05-vmware-virtualization/README.md) (VMware Virtualization): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) (ESXi Installation,
Configuration, and Host Operations) and [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) (vCenter Server
Deployment, Identity, and Recovery) for the cluster foundation, Chapter 04
(vSphere Virtual Networking) for attaching the cluster to the VLANs
[Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) built, [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) (vSphere Storage and vSAN) for the shared
datastore, and [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) (vSphere Availability, Mobility, and Cluster
Services) for HA and DRS.

Data protection follows [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md) (Enterprise Storage and Data Protection):
[Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md) (Backup Architecture and Data Protection Policy) for the backup
design, [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) (Snapshots, Replication, and Continuous Data Protection)
for the vSphere Replication target at `BR1`, and [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) (Recovery
Engineering and Disaster Recovery Validation) for the principle this
chapter enforces in its negative test: an untested restore is not a
backup, only a hope.

This chapter is also where [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s warning about nested hypervisors
becomes concrete. If `esxi-a01` and `esxi-a02` are themselves VMs on a
parent hypervisor (the expected case for most readers), every VM they host
depends on the parent virtual switch passing traffic those VMs originate —
which requires Promiscuous Mode and Forged Transmits set to Accept on the
parent port group. Skipping this is the single most common reason a
freshly built nested vSphere cluster looks correctly configured but VMs
inside it cannot reach the network.

### Systems introduced in this chapter

| Hostname | Role | Address |
| --- | --- | --- |
| `vcsa01` | vCenter Server Appliance | `10.13.30.20` |
| `esxi-a01` | HQ vSphere host 1 | `10.13.30.21` (mgmt), `10.13.50.21` (storage), `10.13.51.21` (vMotion) |
| `esxi-a02` | HQ vSphere host 2 | `10.13.30.22` (mgmt), `10.13.50.22` (storage), `10.13.51.22` (vMotion) |
| `vsan-witness01` | vSAN witness appliance | `10.13.30.23` |
| `bkp01` | Backup repository / secondary storage | `10.13.50.30` |
| `esxi-br101` | BR1 DR-target ESXi host | `10.13.61.21` |

## Design Considerations

- **Two-node vSAN with a witness, not a three-node cluster.** A two-node
  vSAN cluster plus a lightweight witness appliance delivers the same
  resilience lesson as a three-node cluster with a smaller resource
  footprint — an explicit trade-off for a lab that [Volume V, Chapter 06](../../volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md)
  covers as a legitimate ROBO (remote office/branch office) pattern, not
  just a shortcut.
- **Migrate existing VMs rather than rebuild them.** `dc01`, `dc02`,
  `ctrl01`, and `linux01` are imported into the cluster rather than
  recreated, because a real migration project ([Volume I, Chapter 08](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md),
  Infrastructure Lifecycle Management) almost never gets to start from
  nothing — this mirrors that constraint honestly instead of skipping it.
- **Scripted backup workflow instead of a specific commercial product.**
  This chapter uses PowerCLI-driven quiesced snapshots exported to `bkp01`
  rather than installing a specific vendor backup platform, so the
  mechanics (snapshot, export, verify, retire the snapshot) stay visible.
  [Volume VI, Chapter 05](../../volume-06-enterprise-storage-data-protection/chapters/05-backup-architecture-and-data-protection-policy.md) covers evaluating a commercial VADP-integrated
  product for a production environment; the lab technique here is
  intentionally transparent rather than a product endorsement.
- **vSphere Replication, not storage-array replication.** With no
  enterprise array in this lab, hypervisor-level replication is the only
  practical way to get a DR-ready copy of a VM at `BR1`; production
  environments with array-based replication would use [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md), Chapter
  06's array-replication patterns instead.
- **Admission control is mandatory, not optional.** HA admission control
  is configured to reserve enough capacity on `esxi-a02` alone to run every
  VM that would fail over from `esxi-a01` — without it, this chapter's
  negative test would "pass" for the wrong reason (both hosts happening to
  have spare capacity) rather than because admission control guaranteed it.

## Implementation and Automation

Enable vSAN on the two-node cluster with the witness appliance registered:

```powershell
Connect-VIServer vcsa01.corp.meridian.example
New-Cluster -Name "HQ-Cluster" -Location (Get-Datacenter "HQ") `
  -HAEnabled -DrsEnabled -DrsAutomationLevel FullyAutomated
Add-VMHost esxi-a01.corp.meridian.example -Location "HQ-Cluster" -Force
Add-VMHost esxi-a02.corp.meridian.example -Location "HQ-Cluster" -Force
$cluster = Get-Cluster "HQ-Cluster"
Set-VsanClusterConfiguration -Configuration $cluster -Enabled $true `
  -WitnessHost vsan-witness01.corp.meridian.example
```

Configure HA admission control to reserve one host's worth of capacity:

```powershell
Set-Cluster -Cluster "HQ-Cluster" -HAAdmissionControlEnabled $true `
  -HAFailoverLevel 1 -Confirm:$false
```

Migrate the existing standalone VMs into the cluster using cold or hot
migration, depending on hypervisor compatibility:

```powershell
Move-VM -VM dc01,dc02,ctrl01,linux01 -Destination (Get-Cluster "HQ-Cluster") `
  -Datastore (Get-Datastore "vsanDatastore")
```

Script the backup workflow on `bkp01` (invoked on a schedule via `cron` or
the equivalent Windows Task Scheduler job):

```bash
#!/usr/bin/env bash
# vm-backup.sh — quiesced snapshot, export, cleanup for one VM
set -euo pipefail
VM="$1"
govc snapshot.create -vm "$VM" -quiesce "backup-$(date -u +%Y%m%dT%H%M%SZ)"
govc export.ovf -vm "$VM" "/backup/${VM}/$(date -u +%Y%m%dT%H%M%SZ)"
govc snapshot.remove -vm "$VM" "backup-*"
```

Configure vSphere Replication from `dc02` at HQ to `esxi-br101`:

```powershell
New-VIReplication -VM dc02 -TargetVIServer esxi-br101.corp.meridian.example `
  -RPO 240 -PreparePrimaryVM Auto
```

## Validation and Troubleshooting

- **Cluster health.** `Get-Cluster "HQ-Cluster" | Get-View` (or the vSphere
  Client cluster summary) must show no configuration issues, vSAN health
  green, and both hosts connected before migrating any VM.
- **Nested networking.** If a migrated VM loses network connectivity that
  it had on its original standalone host, check the parent hypervisor's
  port group security policy first: Promiscuous Mode and Forged Transmits
  must both be set to Accept, exactly as flagged in Chapter 01.
- **HA admission control.** `Get-Cluster "HQ-Cluster" | Select
  HAFailoverLevel` should report `1`; if HA restarts fail during the
  negative test with a resource-related error, admission control was
  probably not actually applied.
- **Common failure: vMotion over the wrong VLAN.** If migrations hang or
  fail with a timeout, confirm the vMotion vmkernel adapter is bound to
  VLAN 151 (`10.13.51.0/24`) specifically, not the management VLAN — a
  vMotion adapter accidentally left on the management network is a
  frequent misconfiguration that still "mostly works" until load exposes
  it.
- **Backup verification.** Every `vm-backup.sh` run should be followed by
  confirming the exported OVF directory is non-empty and its manifest
  checksum validates (`govc export.ovf` writes a `.mf` file); a backup job
  that reports success but writes an empty or corrupt export is worse than
  a job that fails loudly.
- **Replication health.** `Get-VIReplication -VM dc02` should show a
  recent successful sync timestamp within the configured 4-hour RPO; a
  replication job stuck at "syncing" typically indicates the WAN link
  from Chapter 03 is saturated or down.

## Security and Best Practices

- Isolate the vMotion (VLAN 151) and storage (VLAN 150) networks from
  every VLAN with user or internet-facing traffic; neither protocol
  encrypts payload by default in this configuration.
- Restrict `vcsa01` administrative access to a dedicated vSphere SSO group
  populated from `corp.meridian.example`, not local SSO accounts, so
  access control stays centralized with the identity work from Chapter 02.
- Store exported backup images on `bkp01` with access restricted to the
  backup service account and encrypt them at rest if the lab's storage
  supports it — a backup image is a complete copy of production-equivalent
  data, including anything sensitive in Active Directory.
- Tag every VM with an owner and expiration label as Chapter 01 requires;
  the migration in this chapter is a natural point to apply that tagging
  consistently across the whole inventory.
- Test the restore path on a defined interval, not just once in this
  chapter — a backup policy without a periodic restore test is, per Volume
  VI, Chapter 07, not actually validated.

## References and Knowledge Checks

**References**

- [Volume V](../../volume-05-vmware-virtualization/README.md), Chapters 02–04 and 06–07 — ESXi and vCenter deployment,
  virtual networking, vSAN, and availability/mobility.
- [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md), Chapters 05–07 — backup architecture, snapshots/replication,
  and recovery engineering.
- [Volume I, Chapter 08](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md) — Infrastructure Lifecycle Management (migration
  context).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — vSphere 9.x
  baseline used throughout this chapter.

**Knowledge checks**

1. Why does this chapter migrate the existing VMs into the cluster instead
   of rebuilding them from scratch?
2. What does HA admission control guarantee that HA alone, without
   admission control, does not?
3. Why is Promiscuous Mode/Forged Transmits on the parent port group a
   recurring theme from Chapter 01 rather than a one-time fix?
4. What would a "successful" backup job that produces an empty export
   directory teach you about trusting job exit codes alone?

## Hands-On Lab

This chapter's labs add the **virtualization, storage, and data-protection** layer to the
environment, drawing on Volumes V, VI, and XXVI. Each ends **`**Lab verified by:** *pending*`** until a
human runs it.

**Shared prerequisites for Labs 4.1–4.4** — the network fabric and identity from Chapters 02–03, and a
virtualization host (KVM/Proxmox/ESXi) with storage. **Cost:** none beyond lab resources.

### Lab 4.1 — Virtualized workloads on the fabric (Topic: Virtualization)

**Objective:** Run the environment's services as VMs on the integrated network.

```bash
# Provision a VM attached to a segment VLAN (Ch03), joined to the domain (Ch02):
#   virt-install / qm create ... --net0 bridge=vmbr0,tag=20   (server segment)
virsh list --all 2>/dev/null | head || qm list 2>/dev/null | head
```

**Expected result:** VMs run the environment's services, placed on the correct segment and joined to
the directory — virtualization (Volumes V/XXVI) hosts the integrated services densely and flexibly,
and each VM inherits the network segmentation and identity established in the prior chapters.

**Negative test:** place VMs on a default/flat virtual network ignoring the segmentation plan; they
bypass the environment's network policy — VM NICs must attach to the correct segment VLAN to stay
consistent with the fabric.

**Cleanup:** destroy lab-only VMs.

### Lab 4.2 — Shared storage for the environment (Topic: Storage)

**Objective:** Provide resilient shared storage to the workloads.

```bash
# A resilient datastore (LVM/ZFS/vSAN, Vol VI/XXVI) backs the VMs; network storage (NFS/SMB) for data:
df -h --total | tail -1
showmount -e <nas> 2>/dev/null | head || echo "(NFS/SMB shares serve app data across the environment)"
```

**Expected result:** VMs sit on a resilient datastore and application data on shared network storage —
integrated storage (Volume VI) gives the environment fault-tolerant capacity with the right resilience
(RAID/FTT) per workload, decoupling data from any single host.

**Negative test:** run stateful services on a single host's local disk with no redundancy or shared
storage; a host loss takes the data with it — resilient shared storage is what lets workloads survive
host failure and migrate.

**Cleanup:** none.

### Lab 4.3 — Data protection (Topic: Backup)

**Objective:** Protect the environment's data with tested backups.

```bash
# Scheduled backups of VMs + data (Vol VI/XXVI), with a verified restore:
#   vzdump / veeam / restic ... to an offsite/immutable target (3-2-1)
echo "backup -> offsite/immutable copy -> scheduled -> TEST RESTORE (the only proof that matters)"
```

**Expected result:** the environment's VMs and data have scheduled, offsite/immutable backups and a
tested restore — data protection (Volume VI) layered on top of storage resilience covers what RAID/FTT
cannot: corruption, deletion, ransomware, and site loss; the tested restore is the proof.

**Negative test:** rely on storage redundancy as "backup"; ransomware or deletion is faithfully
mirrored to every copy — a separate, tested, offline backup is what makes the environment recoverable.

**Cleanup:** remove lab-only backup artifacts.

### Lab 4.4 — Live migration and availability (Topic: Availability)

**Objective:** Move a running workload without downtime.

```bash
# With shared storage (Lab 4.2), migrate a running VM between hosts:
#   virsh migrate --live <vm> qemu+ssh://host2/system   (or vMotion / qm migrate)
echo "shared storage + clustering enables live migration -> host maintenance with zero VM downtime"
```

**Expected result:** a running VM migrates between hosts with no downtime — live migration (enabled by
shared storage + clustering, Volumes V/XXVI) lets you patch/maintain hosts without disrupting the
environment's services, integrating virtualization and availability design.

**Negative test:** attempt live migration with VMs on host-local storage; there is no shared copy to
migrate to, so it fails or requires downtime — shared storage is the prerequisite for non-disruptive
mobility.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter consolidated every VM built so far into a managed,
HA-protected vSphere cluster on vSAN, added a transparent scripted backup
workflow, and established vSphere Replication to a BR1 DR target that
Chapter 09's capstone will exercise fully. The negative test proved HA
admission control actually restarts a workload after a host failure, and
the restore test proved the backup was recoverable, not just present.

- [ ] Built a two-node vSAN cluster with a witness appliance and migrated
      existing lab VMs into it.
- [ ] Configured and validated HA admission control and DRS.
- [ ] Built and validated a scripted backup workflow to `bkp01`.
- [ ] Configured vSphere Replication from HQ to `esxi-br101`.
- [ ] Completed the host-failure negative test and a full restore test,
      with a corrupted restored VM deleted during cleanup.
