# Chapter 09: Enterprise Resilience and Lifecycle Capstone

## Learning Objectives

- Translate a business impact analysis of every service built in this
  volume into explicit RTO/RPO targets, then measure actual performance
  against them.
- Execute a full HQ site-failure chaos exercise and follow the resulting
  disaster-recovery failover through to a functioning `BR1`-based
  identity plane.
- Diagnose two genuine architectural limitations this volume deliberately
  left in place — the `BR1` RODC's write dependency from Chapter 03 and
  the on-premises-only Kubernetes control plane from Chapter 05 — and
  resolve the identity limitation using the vSphere-replicated domain
  controller from Chapter 04.
- Fail back to HQ cleanly, including Active Directory metadata cleanup,
  without introducing directory inconsistency.
- Execute a complete, evidence-backed decommissioning of every system this
  volume built, in dependency order, with secure data sanitization.

## Theory and Architecture

This chapter is the integration point for the entire volume and draws
directly on Volume XII (Resilience and Lifecycle Management): Chapter 02
(Business Impact Analysis and Continuity Planning) for the RTO/RPO
exercise this chapter opens with, Chapter 03 (High Availability, Fault
Tolerance, and Graceful Degradation) and Chapter 04 (Backup, Recovery, and
Disaster-Recovery Engineering) for the failover mechanics, Chapter 05
(Resilience Testing, Exercises, and Chaos Engineering) for how the outage
is safely simulated and bounded, and Chapter 09 (Retirement,
Decommissioning, and Lifecycle Governance) for the teardown that closes
the volume. Volume I, Chapter 08 (Infrastructure Lifecycle Management)
supplies the broader lifecycle frame this chapter's decommissioning phase
follows.

Every earlier chapter in this volume left at least one deliberate scope
boundary rather than building a fully redundant system from the start:
Chapter 03 placed a read-only, not writable, domain controller at `BR1`;
Chapter 05 kept the Kubernetes control plane entirely on-premises so a
hybrid link failure would degrade scheduling rather than take down the
cluster, at the cost of the whole platform depending on HQ's survival.
Chapter 05's negative test exercised a VPN failure, not a full HQ outage —
this chapter is where that untested boundary finally gets exercised. A
resilience program that only ever tests the failures it already knows how
to survive is not testing anything; Volume XII, Chapter 05 calls this out
directly, and this capstone is built to surface exactly that kind of gap
rather than avoid it.

The chapter has three phases: a bounded chaos exercise simulating total
loss of the `HQ` site, a disaster-recovery failover and later failback
using the assets Chapter 04 specifically built for this moment, and a
full, ordered decommissioning of every system in the reference lab.

### Service tiers and recovery targets

Established from a business impact analysis across everything this volume
built, before the chaos exercise runs:

| Tier | Services | RTO target | RPO target |
| --- | --- | --- | --- |
| 0 | Identity, DNS, time (`dc01`/`dc02`, Chapter 02) | 15 min | 0 (synchronous AD replication) |
| 0 | Core network, WAN (Chapter 03) | 15 min | N/A (stateless) |
| 1 | Virtualization/storage/backup (Chapter 04) | 1 hr | 4 hr (replication RPO set in Ch. 04) |
| 1 | Hybrid platform (`meridian-web`, Kubernetes, Chapter 05) | 4 hr | 1 hr |
| 1 | Security telemetry (`siem01`, Chapter 07) | 4 hr | 15 min |
| 2 | Automation/CI (`git01`, `vault01`, Chapter 06) | 8 hr | 24 hr |
| 2 | Observability (`obs01`, Chapter 08) | 8 hr | 24 hr |

## Design Considerations

- **Simulate a full site loss, not another single-component failure.**
  Every prior negative test in this volume failed exactly one thing — a
  domain controller, a core switch, a VPN tunnel, a Kubernetes node. This
  chapter fails the entire `HQ` site at once, which is the only way to
  find an assumption that held only because two things never failed
  together.
- **The blast radius is bounded and reversible before it starts.** Per
  Volume XII, Chapter 05's chaos engineering discipline, this exercise
  runs against systems already known to be disposable lab infrastructure,
  every affected system has a snapshot taken immediately beforehand, and
  the exercise has a defined stop condition (an unrecoverable state) that
  triggers an immediate abort to restore from snapshot rather than
  pressing forward.
- **Recover through the asset built for this, not through improvisation.**
  Chapter 04's decision to replicate `dc02` — not `dc01` — to `esxi-br101`
  was made specifically so this chapter would have a writable domain
  controller image available at `BR1` without depending on the RODC
  Chapter 03 placed there. This chapter is the payoff for that earlier
  design decision, not a new one.
- **Failback happens after HQ is verified stable, never concurrently with
  the emergency response.** Running the failback procedure while HQ
  systems are still being brought back online risks a second simultaneous
  change during an already elevated-risk period — a classic change
  management anti-pattern Volume XI, Chapter 07 and Volume XII, Chapter 06
  both warn against.
- **Decommission in reverse-dependency order.** Workloads come down
  before the platform hosting them; the platform comes down before the
  network; identity comes down last, because every other system in this
  volume depends on it and almost nothing depends on removing it first.
- **Sanitize, don't just delete.** Every disk that held `corp.meridian.example`
  data — even lab data — is sanitized per NIST SP 800-88 categories
  (Clear, Purge, or Destroy) rather than simply released back to the
  hypervisor's free pool, per the security note established in Chapter 01.

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
Chapter 06's automation rather than manual steps:

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
pipeline Chapter 06 built for creation:

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
  the standard Chapter 01 committed this volume to.
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
  them is out of this volume's scope; Volume XII, Chapter 07 (Technical
  Debt, Modernization, and Platform Renewal) is where that kind of finding
  is meant to go next.

## References and Knowledge Checks

**References**

- Volume I, Chapter 08 — Infrastructure Lifecycle Management.
- Volume XII, Chapters 02–07 and 09 — business impact analysis, high
  availability, backup/DR engineering, resilience testing/chaos
  engineering, maintenance/patching, technical debt/modernization, and
  retirement/decommissioning.
- NIST SP 800-88 Rev. 1 — *Guidelines for Media Sanitization*.
- Microsoft's Active Directory Forest Recovery guidance (FSMO seizure and
  USN rollback detection).
- Every chapter of this volume — this capstone assumes Chapters 01–08 are
  complete and their environments healthy.

**Knowledge checks**

1. Why does this chapter simulate a full site failure instead of another
   single-component failure, given how many single-component failures
   this volume already tested?
2. Why was `dc02`, specifically, the domain controller Chapter 04
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

**Objective:** Run a full HQ site-failure chaos exercise against the
complete reference lab, execute disaster recovery through the
BR1-replicated domain controller, fail back cleanly, and then
decommission every system this volume built, in dependency order, with
verified data sanitization.

**Prerequisites**

- Chapters 01–08 complete, with every system healthy and each chapter's
  own completion checklist satisfied.
- Full administrative access to every system in the reference lab —
  this is the only chapter that touches the entire environment at once.
- A block of uninterrupted lab time; unlike earlier chapters, this
  exercise should not be run in fragments, since the mid-exercise state
  (HQ down, BR1 carrying the load) is not one you want to leave
  unattended.

**Steps**

1. Confirm the `ch08-baseline` state across every system in the
   environment.

2. Complete the business impact analysis table in Theory and Architecture
   for this specific environment if any tier or target has drifted since
   the table above was drafted, and record it in
   `~/vol13-lab/bia.yml`.

3. Take a full-environment snapshot or backup, labeled `ch09-pre-chaos`,
   across every host and network device — this is the point every phase
   of this exercise can roll back to if the abort condition is triggered.

4. **Chaos exercise:** Run the outage simulation:

   ```bash
   ./evidence.sh "./simulate-hq-outage.sh"
   ```

5. **Expected result — confirmed outage.** From `BR1`:

   ```bash
   ./evidence.sh "ssh admin@rtr-br101 'ping -c 3 10.13.70.1; show ip ospf neighbor'"
   ```

   The HQ-side WAN peer must be unreachable and the OSPF neighbor must be
   down before proceeding to recovery.

6. **Confirm the known limitation.** Attempt a directory write against
   the `BR1` RODC alone:

   ```bash
   ./evidence.sh "ssh administrator@dc-br101.corp.meridian.example \
     'Set-ADAccountPassword -Identity testuser -Reset' || true"
   ```

   **Expected result:** The operation fails or refers to a writable DC
   that is currently unreachable — document this as the confirmed
   limitation, not a step to work around in place.

7. **Disaster recovery failover:** Recover the replicated `dc02` image at
   `esxi-br101` and seize FSMO roles onto it, using the commands in
   Implementation and Automation.

8. **Expected result — FSMO seizure complete.**

   ```bash
   ./evidence.sh "ssh administrator@dc02.corp.meridian.example 'netdom query fsmo'"
   ```

   All five FSMO roles must show as held by the recovered `dc02` copy.

9. Repoint `BR1`'s DHCP relay and `dc-br101`'s replication partner to the
   recovered `dc02`, then confirm BR1-only identity operations now
   succeed:

   ```bash
   ./evidence.sh "ssh administrator@dc02.corp.meridian.example \
     'Set-ADAccountPassword -Identity testuser -Reset'"
   ```

10. Rebuild a minimal Kubernetes control plane at `BR1` using Chapter 06's
    automation, and record the elapsed time from step 4 to a working
    control plane as this exercise's measured RTO:

    ```bash
    ./evidence.sh "terraform apply -var-file=environments/br1-emergency.tfvars \
      -target=module.k8s_control_plane_br1"
    ```

11. **Expected result — RTO/RPO measured.** Compare the elapsed recovery
    time and the age of the last good replication point against the
    targets in the BIA table, and record both, including any tier that
    missed its target.

12. **Failback:** Once satisfied the exercise's findings are fully
    captured, power `HQ` systems back on. Before allowing `dc01` back into
    replication, check for a USN rollback condition per Validation and
    Troubleshooting:

    ```bash
    ./evidence.sh "ssh administrator@dc01.corp.meridian.example \
      'dcdiag /test:CheckSDRefDom'"
    ```

13. Run the metadata cleanup procedure from Implementation and Automation
    to remove `dc01`'s stale FSMO claims, then confirm a single,
    consistent view of role ownership:

    ```bash
    ./evidence.sh "ssh administrator@dc02.corp.meridian.example 'netdom query fsmo'"
    ```

    **Expected result:** Exactly one authoritative answer, with no
    conflicting claims from `dc01`.

14. Decommission the emergency `BR1` control plane rebuilt in step 10 now
    that HQ's original platform is available again, and confirm
    `meridian-web` and the hybrid cluster are healthy against the
    original topology.

15. **Full lifecycle decommission.** Working in reverse-dependency order,
    tear down every system this volume built:

    | Order | Scope | Mechanism |
    | --- | --- | --- |
    | 1 | Kubernetes workloads and cluster (Ch. 05) | `terraform destroy -target=module.k8s_cluster` |
    | 2 | `CLOUD1` landing zone (Ch. 05) | `terraform destroy -target=module.cloud1_landing_zone` |
    | 3 | vSphere VMs, cluster, ESXi hosts, `bkp01` (Ch. 04) | `terraform destroy -target=module.hq_vsphere_cluster` |
    | 4 | WAN, campus, wireless devices (Ch. 03) | `ansible-playbook decommission.yml --tags network` |
    | 5 | Security and observability tooling: `siem01`, `obs01` (Ch. 07–08) | `ansible-playbook decommission.yml --tags security,observability` |
    | 6 | Automation/CI: `git01`, `vault01` (Ch. 06) | `ansible-playbook decommission.yml --tags automation` |
    | 7 | Identity: `dc-br101`, `dc02`, `dc01` (Ch. 02–03) | Domain controller demotion, last |

    ```bash
    ./evidence.sh "terraform destroy -target=module.k8s_cluster -auto-approve"
    ./evidence.sh "terraform destroy -target=module.cloud1_landing_zone -auto-approve"
    ./evidence.sh "terraform destroy -target=module.hq_vsphere_cluster -auto-approve"
    ./evidence.sh "ansible-playbook decommission.yml --tags network,security,observability,automation"
    ./evidence.sh "ssh administrator@dc-br101.corp.meridian.example \
      'Uninstall-ADDSDomainController -Force -RemoveDnsDelegation'"
    ./evidence.sh "ssh administrator@dc02.corp.meridian.example \
      'Uninstall-ADDSDomainController -Force -LastDomainControllerInDomain -RemoveDnsDelegation'"
    ```

16. **Expected result — clean removal.** After the last domain controller
    is demoted, confirm no residual DNS records or computer objects
    remain:

    ```bash
    ./evidence.sh "nslookup corp.meridian.example || echo 'domain retired as expected'"
    ```

17. Sanitize every disk that held domain, security, or configuration data
    per NIST SP 800-88, matching the category to the medium (for example,
    a cryptographic erase or full-disk overwrite for VM storage before the
    underlying datastore or cloud volume is released).

18. **Cleanup:** Confirm the cloud provider's own resource inventory shows
    nothing remaining from `CLOUD1` (checking directly, not only via
    Terraform state), revoke every credential and secret issued across
    this volume, and finalize the evidence bundle:

    ```bash
    ./evidence.sh "sha256sum -c ~/lab-evidence/manifest.sha256"
    cd ~/vol13-lab
    git add topology.yml bia.yml
    git commit -m "Chapter 09: resilience exercise, DR failover, and full decommission"
    ```

    **Expected result:** Every checksum in the manifest verifies, giving
    a complete, tamper-evident record of every chapter's evidence from
    Chapter 01 through this capstone.

## Summary and Completion Checklist

This capstone tested the whole reference lab against a failure no earlier
chapter attempted — total loss of the `HQ` site — and followed the
recovery through to a working `BR1`-based identity plane using the
vSphere-replicated domain controller Chapter 04 built specifically for
this moment. It surfaced two real architectural limitations rather than
concealing them, executed a clean failback with proper Active Directory
metadata hygiene, and closed the volume with a complete, sanitized,
evidence-backed decommissioning of everything built since Chapter 01.

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
- [ ] Verified the complete evidence manifest from Chapter 01 through
      this capstone.
