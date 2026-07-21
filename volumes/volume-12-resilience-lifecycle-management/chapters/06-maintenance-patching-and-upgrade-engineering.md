# Chapter 6: Maintenance, Patching, and Upgrade Engineering

![Lab flow for this chapter: a rolling patch script patches all five simulated cluster nodes one at a time (drain, patch, rejoin), reporting quorum preserved throughout and returning the cluster to full strength. As a negative test, the script's quorum calculation is hardcoded to a value well below true majority and the rolling patch re-run; the script now proceeds even when it should not, demonstrating that a quorum guard with an incorrect threshold provides false confidence rather than real protection — the formula itself must be verified, not merely present.](../../../diagrams/volume-12-resilience-lifecycle-management/chapter-06-quorum-rolling-patch-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: a rolling patch preserving cluster quorum throughout, contrasted with a deliberately broken quorum guard.*

## Learning Objectives

- Distinguish patching from upgrading and explain why each carries a different risk profile and testing requirement.
- Classify patches by severity and map each classification to a remediation SLA.
- Design a staged rollout (canary, rolling, blue-green) that patches or upgrades a Tier 0/1 service without violating its availability targets from [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md).
- Coordinate planned maintenance with HA quorum and disruption-budget constraints so voluntary disruption does not become an involuntary outage.
- Build automated patch-compliance reporting and a rollback-triggered staged deployment.
- Explain the exception process for a Tier 0 system that cannot be immediately patched, and the compensating controls it requires.

## Theory and Architecture

### Patching vs. Upgrading

Patching applies a vendor-supplied fix — typically a security fix, a bug fix, or a small functional change — within the same major version, and is usually designed by the vendor to be low-risk and backward-compatible. Upgrading moves a system to a new major or minor version, which may change behavior, deprecate features, or require a compatibility review. The two share mechanics (both are planned changes to running infrastructure, both benefit from staged rollout and rollback planning) but differ sharply in risk: a patch's blast radius is usually well understood and vendor-tested; an upgrade's blast radius depends heavily on how much the receiving system's specific configuration and integrations have drifted from the vendor's tested baseline. Treating a major-version upgrade with the same lightweight process used for a routine security patch is a common and costly mistake; treating every patch with the full rigor of a major upgrade is the opposite mistake, delaying critical security fixes for no proportionate benefit.

### The Patch Management Lifecycle

A mature patch management process runs the same cycle for every patch, with the depth of each stage varying by classification:

1. **Identify** — new patches are discovered through vendor advisories, subscribed CVE feeds, or automated inventory-scanning tools that compare installed versions against known-available updates.
2. **Classify** — the patch is scored by severity (see below) and cross-referenced against the systems it applies to, using the same asset inventory referenced in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md)'s lifecycle management chapter.
3. **Test** — the patch is applied in a non-production environment that mirrors production configuration closely enough to surface compatibility issues before they reach production.
4. **Approve** — the patch is scheduled through the organization's change management process (standard, normal, or emergency, per [Volume I, Chapter 8](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md)), with risk and rollback plan documented.
5. **Deploy** — the patch is applied using a staged rollout strategy matched to the service's criticality tier.
6. **Verify** — post-patch validation confirms the system is both patched and functioning correctly, not merely that the patch command exited successfully.

### Patch Severity Classification and SLAs

| Severity | Typical Criteria | Example Remediation SLA |
| --- | --- | --- |
| Critical | Actively exploited vulnerability, or CVSS 9.0+ with no mitigating control | 24–72 hours |
| High | CVSS 7.0–8.9, or a fix for a bug causing active production impact | 7–14 days |
| Moderate | CVSS 4.0–6.9, non-security functional fix | Next scheduled maintenance window |
| Low | CVSS below 4.0, cosmetic or minor fix | Bundled with the next routine upgrade cycle |

Remediation SLAs should be organization-defined and formally approved (often by the same body governing vulnerability management in [Volume X](../../volume-10-enterprise-cybersecurity/README.md)'s cybersecurity practices), not an engineering team's informal preference, because missed SLAs on critical vulnerabilities are frequently an audit and regulatory finding independent of whether an actual exploit occurred.

### Upgrade Types and Compatibility Policy

Following semantic versioning conventions broadly (even for platforms that do not strictly adhere to semver), upgrades fall into three categories with different compatibility expectations:

- **Patch-level** — bug and security fixes only, no intended behavior change; lowest risk.
- **Minor-version** — new functionality added in a backward-compatible way; low-to-moderate risk, occasional deprecation warnings.
- **Major-version** — may include breaking changes, removed features, or new default behaviors; highest risk, requires the most thorough compatibility testing.

Many platforms also publish an **N-1/N-2 support policy**, supporting only the current and one or two prior major versions with security fixes. A system running a version older than the vendor's supported window is, by definition, unable to receive patches at all — this is a forcing function that connects directly to [Chapter 7](07-technical-debt-modernization-and-platform-renewal.md)'s modernization discipline: a system that has fallen out of vendor support is technical debt with a hard deadline, not a soft preference to eventually address.

### Staged Rollout Strategies

Deploying a patch or upgrade to 100% of a fleet simultaneously maximizes blast radius if the change is bad; staged rollout strategies deliberately limit exposure while the change is validated against real traffic:

- **Canary** — the change is applied to a small subset (a single instance, or a low single-digit percentage of traffic) first, observed against defined success metrics, and only promoted to the full fleet if the canary is healthy.
- **Rolling** — instances are updated in sequential batches, each batch validated (often via the same health checks from [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md)) before the next batch proceeds, keeping the service available throughout because only a bounded fraction of capacity is ever offline at once.
- **Blue-green** — a complete parallel environment (green) is provisioned with the new version while the existing environment (blue) continues serving all traffic; traffic is cut over to green only after validation, and blue is retained briefly for instant rollback.

These strategies are not exclusive to application deployments — the same logic applies to OS patching, firmware updates, and database upgrades, though the mechanics differ (a rolling OS patch cycles nodes through a maintenance state; a blue-green database upgrade typically requires a parallel replica promoted after validation, closely resembling the DR failover pattern from [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md)).

## Design Considerations

### Test Environment Parity

A patch or upgrade tested in an environment that differs meaningfully from production — different data volume, different configuration, different traffic patterns, or simply staler than production due to configuration drift — provides a weaker signal than it appears to. Test environment parity should be treated as its own maintained property, verified periodically (a configuration-drift comparison between test and production, not just an assumption that they started identical and stayed that way).

### Patching Order and Progressive Exposure

A disciplined patching order limits the population exposed to an undiscovered bad patch at each stage: development, then staging, then a production canary, then a wider production rolling wave, then the full fleet — with a defined bake time at each stage before promotion. Skipping stages under time pressure (common with critical-severity security patches) is sometimes a legitimate risk trade-off, but it should be an explicit, approved exception with compensating monitoring during the accelerated rollout, not a routine practice adopted because the standard process feels slow.

### Coordinating Patching With HA Quorum and Disruption Budgets

Planned maintenance is a voluntary disruption, and [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md)'s Pod Disruption Budget example exists specifically to prevent voluntary disruptions (a node drain during patching) from taking more capacity offline than the service can tolerate. The same principle applies outside Kubernetes: patching nodes in a quorum-based cluster one at a time, always confirming the cluster retains quorum after each node is taken offline, is mandatory — a maintenance operation that drops a cluster below quorum has caused an outage indistinguishable, from the user's perspective, from an unplanned failure, except that it was entirely avoidable. Maintenance runbooks should explicitly state the maximum number of units that may be offline simultaneously, derived from the same redundancy math (N+1, 2N) established in [Chapter 1](01-resilience-engineering-and-critical-service-design.md).

### Rollback Strategy as a First-Class Design Decision

A rollback plan designed after a patch has already caused a problem is a rollback plan designed under pressure with incomplete information. Rollback strategy should be decided and validated before deployment begins: is the change reversible in place (uninstalling a patch), or does rollback require restoring from a pre-change snapshot or redeploying the prior version's artifact? For database schema changes in particular, forward-only migrations (additive changes that do not break the prior application version) are frequently safer than attempting to design a true rollback for a destructive schema change, and this distinction should inform how upgrades are sequenced relative to application deployments.

### Maintenance Window Sizing

A maintenance window must be sized against the actual time required for the staged rollout, including bake time at each stage and time reserved for a rollback if needed — not merely the time to apply the change to a single unit multiplied by unit count, which omits validation and buffer time entirely and is a common source of maintenance windows that run over and collide with business hours.

## Implementation and Automation

### Patch Compliance as Code

```yaml
# patch-policy.yaml
- system_class: production-linux-hosts
  tier: 0
  critical_sla_hours: 48
  high_sla_days: 7
  moderate_sla: "next maintenance window"
  rollout_strategy: rolling
  max_concurrent_offline_pct: 20
  bake_time_minutes: 30
  rollback_method: "snapshot restore"

- system_class: internal-reporting-batch
  tier: 3
  critical_sla_hours: 168
  high_sla_days: 30
  moderate_sla: "next scheduled release"
  rollout_strategy: all-at-once
  max_concurrent_offline_pct: 100
  bake_time_minutes: 0
  rollback_method: "redeploy prior artifact"
```

As with the criticality register and backup policy in earlier chapters, storing patch policy as structured data enables automated compliance checks: a scheduled job can compare each system's last-patched date and current version against its policy's SLA and flag violations before they become an audit finding.

### Example: Patch Compliance Scan

```python
from datetime import datetime, timedelta

def check_compliance(system: dict, policy: dict, now: datetime) -> list[str]:
    """Return a list of SLA violations for a system against its patch policy."""
    violations = []
    if system["severity"] == "critical":
        deadline = system["patch_available_date"] + timedelta(hours=policy["critical_sla_hours"])
    elif system["severity"] == "high":
        deadline = system["patch_available_date"] + timedelta(days=policy["high_sla_days"])
    else:
        return violations  # moderate/low tracked against maintenance calendar, not a hard SLA

    if now > deadline and not system.get("patched", False):
        overdue = (now - deadline).days
        violations.append(
            f"{system['system_id']}: {system['severity']} patch overdue by {overdue} day(s)"
        )
    return violations
```

Running this check on a schedule (daily for critical/high severities) and routing violations to the same paging system used for production incidents, rather than a report nobody reads, is what turns a compliance policy into an enforced control.

### Example: Canary Rollout with Automated Promotion Gate

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout-api-canary
spec:
  replicas: 1
  selector:
    matchLabels: { app: checkout-api, track: canary }
  template:
    metadata:
      labels: { app: checkout-api, track: canary }
    spec:
      containers:
        - name: checkout-api
          image: example.registry/checkout-api:2026.07.2
```

```bash
#!/usr/bin/env bash
# promote-canary.sh: promote a canary to full rollout only if its
# error rate stays within tolerance for the bake period.
set -euo pipefail

BAKE_SECONDS="${1:-1800}"
ERROR_RATE_THRESHOLD="${2:-1.0}"

echo "Observing canary for ${BAKE_SECONDS}s (threshold: ${ERROR_RATE_THRESHOLD}% errors)..."
START=$(date +%s)
while (( $(date +%s) - START < BAKE_SECONDS )); do
  CURRENT_ERROR_RATE=$(example-metrics-cli query --metric error_rate_pct --track canary)
  if (( $(echo "${CURRENT_ERROR_RATE} > ${ERROR_RATE_THRESHOLD}" | bc -l) )); then
    echo "FAIL: canary error rate ${CURRENT_ERROR_RATE}% exceeds threshold; rolling back"
    kubectl scale deployment/checkout-api-canary --replicas=0
    exit 1
  fi
  sleep 60
done

echo "PASS: canary healthy for full bake period; promoting to full rollout"
kubectl set image deployment/checkout-api checkout-api=example.registry/checkout-api:2026.07.2
kubectl scale deployment/checkout-api-canary --replicas=0
```

### Rolling Node Patching With Quorum Awareness

```bash
#!/usr/bin/env bash
# patch-cluster-rolling.sh: patch cluster nodes one at a time,
# confirming quorum is retained before proceeding to the next node.
set -euo pipefail

NODES=("$@")
MIN_QUORUM=$(( (${#NODES[@]} / 2) + 1 ))

for node in "${NODES[@]}"; do
  ACTIVE=$(example-cluster-cli active-node-count)
  if (( ACTIVE - 1 < MIN_QUORUM )); then
    echo "ABORT: taking ${node} offline would drop cluster below quorum (${MIN_QUORUM})" >&2
    exit 1
  fi
  echo "Draining and patching ${node}..."
  example-cluster-cli drain --node "${node}"
  example-cluster-cli patch --node "${node}"
  example-cluster-cli rejoin --node "${node}"
  example-cluster-cli wait-healthy --node "${node}" --timeout 300
done
echo "All nodes patched with quorum preserved throughout."
```

## Validation and Troubleshooting

### Post-Patch Validation

Validation must confirm both that the patch applied and that the system still functions correctly — the two are independent facts:

- Confirm the installed version matches the expected patched version through an independent query, not just the exit code of the patch command.
- Run an automated smoke test covering the service's critical transactions, not only a low-level health check (a service can report "healthy" while a specific patched code path is broken).
- Confirm dependent services and integrations still function; a patch that changes a default configuration value can silently break an integration that relied on the prior default.

### Common Failure Modes

| Symptom | Likely Cause |
| --- | --- |
| Patch applies cleanly but service fails to restart | Configuration file format changed by the patch, or a dependency version incompatibility not caught in test |
| Canary looks healthy but full rollout causes an incident | Canary's traffic sample was not representative (too small, or excluded a critical customer segment or code path) |
| Maintenance causes an unplanned outage despite following the runbook | Cluster quorum math was wrong, or a concurrent, unrelated node failure combined with the planned maintenance to exceed tolerance |
| Rollback fails to restore prior behavior | Rollback plan was never actually tested prior to the change; a database schema change was not designed to be forward-compatible with the prior application version |
| Patch compliance dashboard shows 100% but a real audit finds unpatched systems | Asset inventory used for compliance scanning is incomplete; unmanaged or shadow infrastructure is invisible to the scan |

### Troubleshooting a Failed Rollout Mid-Stage

When a staged rollout fails partway through (some units patched, some not), resist the urge to simply continue forward past the failure. Halt the rollout, assess whether the failed units should be rolled back individually or whether the entire in-flight batch should be reverted, and only resume forward progress once the root cause is understood — a rollout that "mostly succeeded" and is left in a mixed state is itself an unplanned, uncharacterized configuration-drift condition, and should be resolved to a known state (fully rolled back or fully forward) before being considered complete.

## Security and Best Practices

- Verify patch and package integrity (signature verification against a trusted vendor key) before installation; supply-chain compromise of a patch distribution channel is a realistic threat, and installing an unsigned or improperly signed patch defeats the purpose of a patch management program.
- Treat an approved, documented, time-bound exception — not silent non-compliance — as the correct path when a Tier 0 system genuinely cannot be patched within its SLA (a vendor has not yet certified compatibility, for example). The exception must specify compensating controls (increased monitoring, network segmentation, a compensating firewall rule) and an expiration date, and should be visible to the same governance body that owns the patch policy.
- Align critical and high-severity patch SLAs with the organization's broader vulnerability management program ([Volume X](../../volume-10-enterprise-cybersecurity/README.md)); patch management and vulnerability management are frequently the same underlying process viewed from two different chapters of this encyclopedia.
- Restrict who can approve deployment to production patch pipelines separately from who can author a change, mirroring plan/apply separation from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md)'s automation architecture guidance.
- Retain patch and rollback audit history for the retention period required by applicable compliance frameworks; "we patched it" claims without a verifiable record are difficult to defend during an audit or post-incident review.

## References and Knowledge Checks

### References

- [Chapter 1](01-resilience-engineering-and-critical-service-design.md) for the redundancy math (N+1, 2N) that determines safe maintenance concurrency.
- [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) for Pod Disruption Budgets and quorum concepts directly reused here for maintenance safety.
- [Volume I, Chapter 8](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md), *Infrastructure Lifecycle Management*, for the standard/normal/emergency change classification this chapter's approval stage relies on.
- NIST SP 800-40 Rev. 4, *Guide to Enterprise Patch Management Planning*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) for the Kubernetes baseline used in this chapter's rollout examples.

### Knowledge Checks

1. Explain the practical risk difference between applying a patch-level fix and performing a major-version upgrade, and why each warrants a different testing depth.
2. A five-node quorum-based cluster is being patched one node at a time. At what point, numerically, would taking the next node offline violate quorum, and how should the automation respond?
3. Why is a canary rollout's traffic sample representativeness as important as its size?
4. Describe the compensating-control exception process for a Tier 0 system that cannot meet its patch SLA, and explain why silent non-compliance is unacceptable even when the underlying reason is legitimate.
5. Why should rollback strategy be decided before deployment begins rather than designed reactively after a problem is discovered?

## Hands-On Lab

### Lab: Quorum-Aware Rolling Patch With Compliance Scan

**Objective:** Simulate a rolling patch across a small cluster that refuses to proceed if quorum would be violated, and run an automated patch-compliance scan that flags an overdue critical patch.

**Prerequisites:**

- `bash`, `python3` (3.11+).

**Procedure:**

1. Create a working directory and a stub cluster CLI simulating a 5-node cluster:

   ```bash
   mkdir -p ~/labs/resilience-ch6 && cd ~/labs/resilience-ch6
   echo 5 > active-nodes.txt
   cat <<'EOF' > example-cluster-cli
   #!/usr/bin/env bash
   case "$1" in
     active-node-count) cat active-nodes.txt ;;
     drain) N=$(cat active-nodes.txt); echo $((N - 1)) > active-nodes.txt ;;
     patch) sleep 1 ;;
     rejoin) N=$(cat active-nodes.txt); echo $((N + 1)) > active-nodes.txt ;;
     wait-healthy) sleep 1 ;;
   esac
   EOF
   chmod +x example-cluster-cli
   export PATH="$PWD:$PATH"
   ```

2. Save the `patch-cluster-rolling.sh` script from this chapter and run it against five simulated node names:

   ```bash
   bash patch-cluster-rolling.sh node-1 node-2 node-3 node-4 node-5
   ```

   **Expected Result:** All five nodes report as patched with the message `All nodes patched with quorum preserved throughout`, and `active-nodes.txt` returns to `5` at the end.

3. Save `check_compliance` from this chapter as `compliance.py` with a small driver:

   ```python
   from datetime import datetime, timedelta

   def check_compliance(system, policy, now):
       if system["severity"] == "critical":
           deadline = system["patch_available_date"] + timedelta(hours=policy["critical_sla_hours"])
       elif system["severity"] == "high":
           deadline = system["patch_available_date"] + timedelta(days=policy["high_sla_days"])
       else:
           return []
       if now > deadline and not system.get("patched", False):
           overdue = (now - deadline).days
           return [f"{system['system_id']}: {system['severity']} patch overdue by {overdue} day(s)"]
       return []

   policy = {"critical_sla_hours": 48, "high_sla_days": 7}
   system = {
       "system_id": "web-frontend-03",
       "severity": "critical",
       "patch_available_date": datetime(2026, 7, 10),
       "patched": False,
   }
   now = datetime(2026, 7, 18)
   for v in check_compliance(system, policy, now):
       print(v)
   ```

4. Run the scan:

   ```bash
   python3 compliance.py
   ```

**Expected Result:** Output reports `web-frontend-03: critical patch overdue by X day(s)`, correctly flagging a system that missed its 48-hour critical SLA.

**Negative Test:** Modify the rolling-patch script's `MIN_QUORUM` calculation to intentionally drop below true majority (for example, hardcode `MIN_QUORUM=1`) and rerun step 2. Confirm the script now proceeds even when it should not, demonstrating why the quorum-check formula itself must be verified, not merely present — a quorum guard with an incorrect threshold provides false confidence rather than real protection. Restore the correct formula afterward.

**Cleanup:**

```bash
cd ~ && rm -rf ~/labs/resilience-ch6
```

No shared or production systems were modified; the cluster and compliance data were entirely local simulations.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Maintenance, patching, and upgrade engineering apply the same staged-rollout, blast-radius, and rollback discipline introduced for chaos experiments in [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md) to routine, planned change — the difference being that here the "fault" is deliberately permanent (a new version) rather than deliberately temporary. Patch severity classification drives remediation SLAs; staged rollout strategies (canary, rolling, blue-green) limit exposure to a bad change; and quorum-aware maintenance sequencing prevents a voluntary disruption from becoming an involuntary outage. A system that consistently cannot meet its patch SLA, or has fallen outside vendor support entirely, is not a patching problem to keep deferring — it is the trigger condition for [Chapter 7](07-technical-debt-modernization-and-platform-renewal.md)'s modernization and technical-debt discipline.

**Completion checklist:**

- [ ] Can distinguish patching from upgrading and justify a different testing depth for each.
- [ ] Can classify a patch by severity and state its corresponding remediation SLA.
- [ ] Designed a staged rollout (canary, rolling, or blue-green) appropriate to a given service's criticality tier.
- [ ] Implemented quorum-aware rolling maintenance that refuses to proceed when quorum would be violated.
- [ ] Built an automated patch-compliance scan that flags an SLA violation.
- [ ] Can describe the compensating-control exception process for a system that cannot meet its patch SLA.
