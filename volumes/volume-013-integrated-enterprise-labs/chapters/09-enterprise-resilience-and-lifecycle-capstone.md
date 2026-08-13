# Chapter 09: Enterprise Resilience and Lifecycle Capstone

![Lab flow for this chapter: a simulated HQ outage takes the WAN peer unreachable and drops OSPF from the branch site's view, confirming a directory write against the read-only domain controller alone fails as the expected limitation. The replicated domain controller image at the branch site is recovered and seizes all five FSMO roles; the branch's DHCP relay and replication partner repoint to it, and a minimal Kubernetes control plane is rebuilt there, with elapsed time recorded as the measured RTO. On failback, the original domain controller is checked for a USN rollback condition before rejoining replication, and a metadata cleanup removes its stale FSMO claims. The volume then tears down every system built, in strict reverse-dependency order, with disk sanitization and a final verified evidence manifest.](../../../diagrams/volume-013-integrated-enterprise-labs/chapter-09-capstone-dr-failback-decommission-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: the volume's capstone chaos exercise — HQ outage, disaster recovery failover, measured RTO/RPO, failback, and full reverse-dependency decommission.*

## Learning Objectives

- Translate a business impact analysis of every service built in this
  volume into explicit RTO/RPO targets, then measure actual performance
  against them.
- Execute a full HQ site-failure chaos exercise and follow the resulting
  disaster-recovery failover through to a functioning `BR1`-based
  identity plane.
- Diagnose two genuine architectural limitations this volume deliberately
  left in place — the `BR1` RODC's write dependency from [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) and
  the on-premises-only Kubernetes control plane from [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md) — and
  resolve the identity limitation using the vSphere-replicated domain
  controller from [Chapter 04](04-virtualization-storage-and-data-protection-lab.md).
- Fail back to HQ cleanly, including Active Directory metadata cleanup,
  without introducing directory inconsistency.
- Execute a complete, evidence-backed decommissioning of every system this
  volume built, in dependency order, with secure data sanitization.

## Theory and Architecture

This chapter is the integration point for the entire volume and draws
directly on [Volume XII](../../volume-012-resilience-lifecycle-management/README.md) (Resilience and Lifecycle Management): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)
(Business Impact Analysis and Continuity Planning) for the RTO/RPO
exercise this chapter opens with, [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) (High Availability, Fault
Tolerance, and Graceful Degradation) and [Chapter 04](04-virtualization-storage-and-data-protection-lab.md) (Backup, Recovery, and
Disaster-Recovery Engineering) for the failover mechanics, [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md)
(Resilience Testing, Exercises, and Chaos Engineering) for how the outage
is safely simulated and bounded, and Chapter 09 (Retirement,
Decommissioning, and Lifecycle Governance) for the teardown that closes
the volume. [Volume I, Chapter 08](../../volume-001-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md) (Infrastructure Lifecycle Management)
supplies the broader lifecycle frame this chapter's decommissioning phase
follows.

Every earlier chapter in this volume left at least one deliberate scope
boundary rather than building a fully redundant system from the start:
[Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) placed a read-only, not writable, domain controller at `BR1`;
[Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md) kept the Kubernetes control plane entirely on-premises so a
hybrid link failure would degrade scheduling rather than take down the
cluster, at the cost of the whole platform depending on HQ's survival.
[Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md)'s negative test exercised a VPN failure, not a full HQ outage —
this chapter is where that untested boundary finally gets exercised. A
resilience program that only ever tests the failures it already knows how
to survive is not testing anything; [Volume XII, Chapter 05](../../volume-012-resilience-lifecycle-management/chapters/05-resilience-testing-exercises-and-chaos-engineering.md) calls this out
directly, and this capstone is built to surface exactly that kind of gap
rather than avoid it.

The chapter has three phases: a bounded chaos exercise simulating total
loss of the `HQ` site, a disaster-recovery failover and later failback
using the assets [Chapter 04](04-virtualization-storage-and-data-protection-lab.md) specifically built for this moment, and a
full, ordered decommissioning of every system in the reference lab.

### Service tiers and recovery targets

Established from a business impact analysis across everything this volume
built, before the chaos exercise runs:

| Tier | Services | RTO target | RPO target |
| --- | --- | --- | --- |
| 0 | Identity, DNS, time (`dc01`/`dc02`, [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)) | 15 min | 0 (synchronous AD replication) |
| 0 | Core network, WAN ([Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)) | 15 min | N/A (stateless) |
| 1 | Virtualization/storage/backup ([Chapter 04](04-virtualization-storage-and-data-protection-lab.md)) | 1 hr | 4 hr (replication RPO set in Ch. 04) |
| 1 | Hybrid platform (`meridian-web`, Kubernetes, [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md)) | 4 hr | 1 hr |
| 1 | Security telemetry (`siem01`, [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md)) | 4 hr | 15 min |
| 2 | Automation/CI (`git01`, `vault01`, [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md)) | 8 hr | 24 hr |
| 2 | Observability (`obs01`, [Chapter 08](08-observability-operations-and-major-incident-lab.md)) | 8 hr | 24 hr |

## Design Considerations

- **Simulate a full site loss, not another single-component failure.**
  Every prior negative test in this volume failed exactly one thing — a
  domain controller, a core switch, a VPN tunnel, a Kubernetes node. This
  chapter fails the entire `HQ` site at once, which is the only way to
  find an assumption that held only because two things never failed
  together.
- **The blast radius is bounded and reversible before it starts.** Per
  [Volume XII, Chapter 05](../../volume-012-resilience-lifecycle-management/chapters/05-resilience-testing-exercises-and-chaos-engineering.md)'s chaos engineering discipline, this exercise
  runs against systems already known to be disposable lab infrastructure,
  every affected system has a snapshot taken immediately beforehand, and
  the exercise has a defined stop condition (an unrecoverable state) that
  triggers an immediate abort to restore from snapshot rather than
  pressing forward.
- **Recover through the asset built for this, not through improvisation.**
  [Chapter 04](04-virtualization-storage-and-data-protection-lab.md)'s decision to replicate `dc02` — not `dc01` — to `esxi-br101`
  was made specifically so this chapter would have a writable domain
  controller image available at `BR1` without depending on the RODC
  [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) placed there. This chapter is the payoff for that earlier
  design decision, not a new one.
- **Failback happens after HQ is verified stable, never concurrently with
  the emergency response.** Running the failback procedure while HQ
  systems are still being brought back online risks a second simultaneous
  change during an already elevated-risk period — a classic change
  management anti-pattern [Volume XI, Chapter 07](../../volume-011-observability-enterprise-operations/chapters/07-service-management-incident-problem-and-change-operations.md) and [Volume XII, Chapter 06](../../volume-012-resilience-lifecycle-management/chapters/06-maintenance-patching-and-upgrade-engineering.md)
  both warn against.
- **Decommission in reverse-dependency order.** Workloads come down
  before the platform hosting them; the platform comes down before the
  network; identity comes down last, because every other system in this
  volume depends on it and almost nothing depends on removing it first.
- **Sanitize, don't just delete.** Every disk that held `corp.meridian.example`
  data — even lab data — is sanitized per NIST SP 800-88 categories
  (Clear, Purge, or Destroy) rather than simply released back to the
  hypervisor's free pool, per the security note established in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md).

## Implementation and Automation

Simulate the full `HQ` outage as a single scripted action, so the exercise
starts at a known instant and its blast radius is exactly the systems
listed:

```bash
#!/usr/bin/env bash
# simulate-hq-outage.sh — power off every HQ system at once
set -euo pipefail
HQ_HOSTS=(sw-core01 sw-core02 rtr-hq01 dc01 dc02 ctrl01 \
          esxi-a01 esxi-a02 vcsa01 k8s-cp01 k8s-wk01 \
          git01 vault01 siem01 obs01)
for h in "${HQ_HOSTS[@]}"; do
  govc vm.power -off "$h" 2>/dev/null || ssh "admin@${h}" 'shutdown -h now' || true
done
echo "HQ outage simulated at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Recover the replicated `dc02` image at `BR1` and seize FSMO roles onto it,
since an RODC cannot hold or be promoted directly into FSMO ownership:

```powershell
# On esxi-br101, recover the replicated VM
Start-VIRReplicationRecovery -VM dc02 -RecoveryPoint Latest

# On the recovered dc02 copy, once network-isolated verification passes
ntdsutil
: roles
fsmo maintenance: seize schema master
fsmo maintenance: seize domain naming master
fsmo maintenance: seize pdc
fsmo maintenance: seize rid master
fsmo maintenance: seize infrastructure master
fsmo maintenance: quit
: quit
```

Repoint `BR1`'s DHCP relay and `dc-br101`'s replication partner to the
recovered writable DC, then rebuild a minimal control plane at `BR1` using
[Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md)'s automation rather than manual steps:

```bash
cd ~/vol13-lab
terraform apply -var-file=environments/br1-emergency.tfvars \
  -target=module.k8s_control_plane_br1
ansible-playbook site.yml --limit br1 --tags emergency-rebuild
```

After HQ is verified stable during failback, clean up the stale FSMO
claims the original `dc01` still believes it holds:

```text
ntdsutil
: metadata cleanup
metadata cleanup: connections
server connections: connect to server dc01.corp.meridian.example
server connections: quit
metadata cleanup: select operation target
select operation target: list domains
select operation target: select domain 0
select operation target: list sites
select operation target: select site 0
select operation target: list servers in site
select operation target: select server <stale-dc01-object-number>
select operation target: quit
metadata cleanup: remove selected server
metadata cleanup: quit
```

Tear the environment down in reverse-dependency order using the same
pipeline [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) built for creation:

```bash
terraform destroy -target=module.k8s_workloads
terraform destroy -target=module.k8s_cluster
terraform destroy -target=module.cloud1_landing_zone
terraform destroy -target=module.hq_vsphere_cluster
ansible-playbook decommission.yml --tags network,security,observability,identity
```

## Validation and Troubleshooting

- **Confirm the outage before recovering from it.** From `BR1`, confirm
  HQ is genuinely unreachable (`ping`, OSPF neighbor down) before starting
  recovery — recovering against a partially failed simulation produces
  results that do not reflect a real full-site loss.
- **Expect the RODC write attempt to fail, and document it.** A password
  reset or new-account creation attempted against `dc-br101` alone should
  fail or redirect toward a writable DC that no longer exists — this is
  the exact limitation the chapter's design flagged, not a bug in this
  chapter's build.
- **Verify FSMO seizure completed on all five roles**, not just the PDC
  emulator most guides emphasize: `netdom query fsmo` against the
  recovered `dc02` copy must show all five roles held there before BR1
  identity is considered fully recovered.
- **Watch for a USN rollback warning during failback.** If the original
  `dc01` is powered back on without first checking whether its
  invocation ID or USN state conflicts with changes made during the
  emergency, the directory service will detect and halt on a USN
  rollback condition — check `dcdiag /test:CheckSDRefDom` and the
  directory service event log before allowing `dc01` back into
  replication, and if in doubt, treat it as compromised metadata and
  re-add it as a fresh DC rather than forcing it back in.
- **Confirm Terraform destroy actually removed cloud-billed resources.**
  A `terraform destroy` that exits successfully can still leave orphaned
  resources it never had in state (created manually outside Terraform at
  some point in Chapters 04–06) — cross-check against the cloud
  provider's resource inventory directly, not just Terraform's own state
  file.
- **Confirm sanitization, not just deletion.** A deleted VM's underlying
  storage is not necessarily overwritten; run the sanitization step
  explicitly and verify its completion status per host before considering
  that host decommissioned.

## Security and Best Practices

- Revoke every credential and secret issued anywhere in this volume as an
  explicit decommissioning step — `vault01`'s leases, the DHCP failover
  secret, both IPsec pre-shared keys, RADIUS shared secrets, and any cloud
  IAM roles — rather than assuming deleting the systems that used them is
  sufficient.
- Apply NIST SP 800-88 Clear, Purge, or Destroy sanitization to every disk
  that held domain, security, or configuration data, matching the
  category to the storage medium and the sensitivity of what it held, per
  the standard [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) committed this volume to.
- Confirm no stale DNS records, computer objects, or certificate issuances
  remain in `corp.meridian.example` after every domain controller is
  decommissioned — an orphaned DNS record pointing at a deleted host is a
  small but real attack-surface leftover.
- Preserve the evidence bundle itself beyond the infrastructure's own
  teardown; the record of what was built, tested, and decommissioned has
  value independent of whether the lab environment still exists.
- Document both architectural limitations this chapter surfaced — the
  RODC write dependency and the on-premises-only Kubernetes control plane
  — as findings with a recommended remediation, even though remediating
  them is out of this volume's scope; [Volume XII, Chapter 07](../../volume-012-resilience-lifecycle-management/chapters/07-technical-debt-modernization-and-platform-renewal.md) (Technical
  Debt, Modernization, and Platform Renewal) is where that kind of finding
  is meant to go next.

## References and Knowledge Checks

**References**

- [Volume I, Chapter 08](../../volume-001-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md) — Infrastructure Lifecycle Management.
- [Volume XII](../../volume-012-resilience-lifecycle-management/README.md), Chapters 02–07 and 09 — business impact analysis, high
  availability, backup/DR engineering, resilience testing/chaos
  engineering, maintenance/patching, technical debt/modernization, and
  retirement/decommissioning.
- [NIST SP 800-88 Rev. 1](https://csrc.nist.gov/pubs/sp/800/88/r1/final) — *Guidelines for Media Sanitization*.
- [Microsoft's Active Directory Forest Recovery guidance (FSMO seizure and
  USN rollback detection).](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-guide)
- Every chapter of this volume — this capstone assumes Chapters 01–08 are
  complete and their environments healthy.

**Knowledge checks**

1. Why does this chapter simulate a full site failure instead of another
   single-component failure, given how many single-component failures
   this volume already tested?
2. Why was `dc02`, specifically, the domain controller [Chapter 04](04-virtualization-storage-and-data-protection-lab.md)
   replicated to `BR1`, and how does that decision pay off in this
   chapter?
3. What could go wrong if `dc01` were powered back on and allowed to
   replicate immediately during failback, without checking for a USN
   rollback condition first?
4. Why does decommissioning proceed in reverse-dependency order, and what
   would go wrong if identity were decommissioned first?
5. Name the two architectural limitations this chapter deliberately
   surfaces rather than fixes, and where in the encyclopedia's structure
   the remediation for each belongs.

## Hands-On Lab

This chapter is the **enterprise-resilience and lifecycle capstone** — it exercises the entire
integrated environment (Volumes I–XII) against disaster and through its full lifecycle. It closes with
a synthesis **Design Exercise**. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.4** — the complete integrated environment from Chapters 02–08.
**Cost:** none beyond lab resources.

### Lab 9.1 — Resilience validation (Topic: Resilience)

**Objective:** Prove the environment survives component failures.

```text
# Inject failures and confirm the environment keeps serving (chaos-style, controlled):
#   - kill a redundant service instance -> load balancer/HA keeps the service up (Ch04, Ch05)
#   - fail a network path -> routing/redundancy reconverges (Ch03)
#   - fail a storage node -> RAID/FTT rebuilds, no data loss (Ch04)
# Confirm SLOs hold (Ch08) throughout.
```

**Expected result:** each single-component failure is absorbed with the service staying within SLO —
resilience is a property of the *whole* design (redundancy at network, compute, storage, and service
layers, Volumes II–VI), and validating it with controlled failures proves the integration actually
tolerates faults rather than assuming it.

**Negative test:** assume redundancy works without testing; a misconfigured HA pair or insufficient
capacity only reveals itself in a real outage — controlled failure injection proves resilience in
advance.

**Rollback:** restore failed components; confirm health returns to green.

### Lab 9.2 — Disaster recovery (Topic: DR)

**Objective:** Recover the environment at a second site.

```text
# Execute a DR scenario (Vol VI/XII): "primary site lost." Recover using:
#   - backups/replication (Ch04) restored at the DR site
#   - the environment rebuilt from IaC (Ch06) where faster than restore
#   - identity/DNS/network re-established (Ch02-03)
# Measure against RPO (data loss) and RTO (time) targets.
```

**Expected result:** the environment is recovered at the DR site within the RTO, with data loss within
the RPO — disaster recovery integrates backups (Chapter 04), IaC rebuild (Chapter 06), and the core
services (Chapters 02–03); a tested DR run measured against RPO/RTO is the only proof the organization
can actually recover.

**Negative test:** have a DR *plan* on paper that has never been executed; the first real disaster
finds the gaps (missing backups, un-coded infrastructure, stale runbooks) — a tested DR run is what makes
recovery real.

**Rollback:** tear down the DR-test environment.

### Lab 9.3 — Lifecycle operations (Topic: Lifecycle)

**Objective:** Operate the environment through change over time.

```text
# Run the ongoing lifecycle (Vol XII): patch/upgrade a component through the pipeline (Ch06) with
#   progressive delivery and SLO gates (Ch08); decommission a retired service cleanly (Ch06);
#   right-size capacity from observability data (Ch08).
echo "provision -> operate/patch (gated) -> scale/right-size -> decommission -- all as code"
```

**Expected result:** components are patched through gated progressive delivery, retired services
decommissioned cleanly as code, and capacity right-sized from data — lifecycle management (Volume XII)
keeps the integrated environment current, correctly-sized, and free of orphaned resources across its
whole life, not just at build time.

**Negative test:** build the environment and then operate it ad-hoc (manual patches, no
decommissioning, guessed capacity); it degrades, drifts, and accretes orphaned resources — managed
lifecycle keeps it healthy over time.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.4 — Capstone Design Exercise: the whole environment (Topic: Synthesis)

**Objective:** Present and defend the complete integrated design — the volume's culminating deliverable.

> **Scenario.** Present the reference environment you built (Chapters 01–09) as a coherent enterprise
> platform to a review board, and defend it end to end.

Work through and **write down**, tracing each to its source volume: lab-engineering discipline (Ch01);
identity/DNS/time core services (Ch02); the segmented, routed, wireless network fabric (Ch03);
virtualization, storage, and data protection (Ch04); hybrid cloud and Kubernetes platform (Ch05);
infrastructure-as-code and automated delivery (Ch06); zero-trust security, detection, and IR (Ch07);
unified observability and incident operations (Ch08); and resilience, DR, and lifecycle (Ch09). For
each layer, state the requirement it serves and the trade-offs made.

**Expected result:** a defensible, coherent design where every layer integrates with the others —
identity underpins security, networking carries segmentation, IaC rebuilds everything, observability
drives operations, and resilience/DR/lifecycle keep it running — demonstrating mastery of the whole
encyclopedia, which is exactly what this capstone volume exists to prove.

**Negative test:** present the environment as a pile of independently-configured technologies with no
integration story; it is not a *platform*, just tools — the integration (each layer serving and
depending on the others) is the deliverable this volume assesses.

**Rollback:** none (the capstone design is the artifact); tear down the reference environment when the
exercise is complete.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This capstone tested the whole reference lab against a failure no earlier
chapter attempted — total loss of the `HQ` site — and followed the
recovery through to a working `BR1`-based identity plane using the
vSphere-replicated domain controller [Chapter 04](04-virtualization-storage-and-data-protection-lab.md) built specifically for
this moment. It surfaced two real architectural limitations rather than
concealing them, executed a clean failback with proper Active Directory
metadata hygiene, and closed the volume with a complete, sanitized,
evidence-backed decommissioning of everything built since [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md).

- [ ] Completed the business impact analysis and recorded RTO/RPO
      targets for every tier.
- [ ] Executed the full HQ site-failure chaos exercise from a
      pre-recorded, reversible starting point.
- [ ] Recovered BR1 identity through the replicated `dc02` image and
      confirmed FSMO seizure on all five roles.
- [ ] Failed back to HQ cleanly, including AD metadata cleanup and a USN
      rollback check.
- [ ] Decommissioned every system in the volume in reverse-dependency
      order, with sanitization verified and every credential revoked.
- [ ] Verified the complete evidence manifest from [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) through
      this capstone.
