# Chapter 3: High Availability, Fault Tolerance, and Graceful Degradation

![Lab flow for this chapter: breaker_demo.py wraps a deliberately failing dependency in a circuit breaker; the first three calls fail with RuntimeError as the breaker's state progresses toward open, and from the fourth call onward, calls are rejected immediately with CircuitBreakerError rather than waiting for the dependency to fail again. Separately, a failover-verification script run against a load-balancer stub with a generous RTO budget reports PASS. As a negative test, rerunning with an artificially tight zero-second RTO budget reports FAIL, proving the RTO-enforcement branch is reachable and correctly triggers, not just the success path.](../../../diagrams/volume-12-resilience-lifecycle-management/chapter-03-circuit-breaker-failover-flow.svg)

*Figure 3-1. Flow used throughout this chapter's Hands-On Lab: a circuit breaker's fail-fast transition after repeated failures, and a failover-verification script enforcing an RTO budget.*

## Learning Objectives

- Distinguish active-active, active-passive, and clustered HA topologies and select among them based on RTO/RPO from [Chapter 2](02-business-impact-analysis-and-continuity-planning.md).
- Explain quorum, split-brain, and the mechanisms that prevent it in clustered systems.
- Implement circuit breakers, retries with backoff, timeouts, and bulkheads as fault-tolerance primitives.
- Design graceful degradation modes, including load shedding and feature-flag-driven fallback, for a Tier 0/1 service.
- Calculate compound availability across redundant layers (compute, network, storage, power) and identify the weakest link.
- Validate an HA design through controlled failover testing rather than architecture review alone.

## Theory and Architecture

### HA Topologies

High availability is the operational implementation of the absorption property introduced in [Chapter 1](01-resilience-engineering-and-critical-service-design.md): the capacity to lose a component without losing service. Three topologies cover the majority of production systems:

- **Active-passive** — one instance (or site) serves traffic while a standby remains ready to take over. Failover requires detecting the primary's failure and promoting the standby, which introduces a failover time greater than zero. Data must be replicated to the standby, synchronously or asynchronously (see the RPO trade-off below).
- **Active-active** — two or more instances serve traffic simultaneously, and a failure of any one instance is absorbed by the remaining capacity with no promotion step. Active-active requires the application to tolerate concurrent writes to shared state (or to partition state so writes never conflict) and typically delivers the lowest RTO, approaching zero for stateless tiers.
- **Clustering** — a set of nodes cooperate under a shared identity (a virtual IP, a cluster resource manager, or a distributed consensus protocol) to present a single logical service, with the cluster itself handling leader election and failover. Clustering is common for stateful systems — databases, message brokers, and coordination services — where active-active writes are not safe without a coordination layer.

The choice among these is a direct consequence of the [Chapter 2](02-business-impact-analysis-and-continuity-planning.md) RTO/RPO targets: sub-second RTO effectively requires active-active or a fast-electing cluster; an RTO measured in minutes can be met with active-passive; nothing here removes the need for the backup-and-restore patterns in [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md) for RTOs measured in hours.

### Quorum and Split-Brain

A cluster's core problem is agreeing, during a network partition, which side (if any) is authoritative. **Split-brain** occurs when a partition causes two sides of a cluster to independently believe they are the primary and both accept writes, producing divergent, unreconcilable state. **Quorum** — requiring a strict majority of cluster members to agree before accepting a write or promoting a new leader — is the standard defense: a partition can produce at most one side with a majority, so at most one side can proceed.

Quorum has direct sizing consequences: a three-node cluster tolerates the loss of one node (quorum = 2 of 3); a five-node cluster tolerates the loss of two. A two-node cluster cannot achieve quorum-based split-brain protection on its own and requires an external tie-breaker (a witness node, a quorum disk, or an arbitration service) — a common design mistake is deploying a two-node "HA pair" with no witness and assuming quorum semantics that do not actually exist. Consensus protocols such as Raft and Paxos formalize this leader-election and log-replication problem and underpin most modern distributed coordination systems (etcd, Kubernetes' control plane state store, and many distributed databases); this volume treats them at the level of operational consequence (odd-numbered cluster sizes, witness nodes, quorum loss behavior) rather than protocol internals, which belong to a distributed-systems text.

### Fault-Tolerance Primitives

Beyond redundancy at the infrastructure layer, resilient services implement fault tolerance in the request path itself:

- **Timeouts** — every synchronous call to a dependency must have an explicit upper bound; a call with no timeout turns a slow dependency into an unbounded resource leak in the caller.
- **Retries with backoff** — a failed call may be retried, but naive immediate retries under load amplify the failure (a "retry storm"). Exponential backoff with jitter spaces retries out and avoids synchronized retry waves across many callers.
- **Circuit breakers** — after a failure-rate threshold is crossed, a circuit breaker stops sending requests to a failing dependency for a cooldown period, failing fast instead of waiting for calls to time out, and periodically allows a trial request through to detect recovery.
- **Bulkheads** — isolating resource pools (threads, connections, queue capacity) per dependency so that one saturated or slow dependency cannot exhaust resources needed to serve calls to healthy dependencies.

These four primitives compose: a call is protected by a bulkhead (isolated pool), bounded by a timeout, retried with backoff on transient failure, and wrapped by a circuit breaker that stops the retries entirely once the dependency is clearly down.

### Graceful Degradation

Graceful degradation defines what a service does when it cannot deliver full functionality, rather than failing the entire request. Techniques include:

- **Load shedding** — deliberately rejecting a fraction of incoming requests (typically the lowest-priority ones, identified by a request classification scheme) to protect the ability to serve the remainder, rather than allowing the whole system to degrade under overload.
- **Feature-flag-driven fallback** — disabling non-essential features (personalized recommendations, non-critical analytics calls) under load or dependency failure while preserving the critical path (for example, checkout continues to function without a recommendation carousel).
- **Cached or default responses** — serving a slightly stale cached value, or a safe default, instead of a hard failure when a non-critical dependency is unavailable.
- **Read-only mode** — for systems where writes are riskier to accept during partial failure than reads are to serve stale, falling back to read-only operation preserves partial value rather than none.

## Design Considerations

### Availability Across Layers

Redundancy at only one layer of the stack does not protect the whole system. A realistic HA design accounts for compute, network, storage, and power independently, and the system's real availability is bounded by the layer with the weakest redundancy:

| Layer | Redundancy Mechanism | Common Gap |
| --- | --- | --- |
| Compute | Multiple instances across hosts/AZs | Autoscaling group spans AZs but minimum size is 1 |
| Network | Redundant paths, multiple uplinks, BGP failover | Single top-of-rack switch per rack with no MLAG/redundant uplink |
| Storage | RAID/erasure coding, replicated volumes | Replicated database but backups stored on the same storage array |
| Power | Dual feeds, UPS, generator | Redundant servers on a single, unredundant PDU |

A design review should explicitly walk every layer for every Tier 0/1 service; it is common to find rigorous compute redundancy paired with a completely unredundant storage or power dependency underneath it, silently capping the achievable availability regardless of how well the compute layer is engineered.

### Synchronous vs. Asynchronous Replication

Data replication for HA/failover involves a direct trade-off:

- **Synchronous replication** guarantees zero data loss on failover (RPO = 0) because a write is not acknowledged until it is durable on both sides, but it adds the round-trip latency between sites to every write, and it stalls writes entirely if the replica is unreachable — availability and consistency are in tension.
- **Asynchronous replication** acknowledges writes locally and ships them to the replica afterward, preserving low write latency and availability, but risks losing the most recent, unreplicated writes on failover (RPO > 0, bounded by replication lag).

The acceptable choice is dictated by the RPO derived in [Chapter 2](02-business-impact-analysis-and-continuity-planning.md), not by which option is operationally simpler. A financial ledger with an RPO of zero cannot use asynchronous replication regardless of the latency cost; a metrics ingestion pipeline with an RPO of minutes can, and should, prefer the availability and performance of asynchronous replication.

### Sizing Circuit Breakers and Bulkheads

Circuit-breaker thresholds and bulkhead pool sizes are not "set and forget" defaults — they require tuning against observed traffic and dependency behavior. Thresholds set too sensitively cause a circuit to trip on ordinary variance, itself becoming an availability problem; thresholds set too loosely fail to protect the caller before a slow dependency exhausts its resources. Bulkhead pool sizes should be derived from the dependency's observed p99 latency and the caller's acceptable concurrency, not an arbitrary round number, and revisited whenever call volume or dependency performance characteristics change materially.

### Geographic Distribution Trade-offs

Multi-AZ deployment protects against a data-center-level failure at moderate cost and complexity; multi-region deployment protects against a regional-scale event (a cloud provider region outage, a natural disaster, or a regional network failure) but multiplies both cost and complexity, particularly for stateful systems that must now reconcile the CAP-theorem trade-off (consistency vs. availability under partition) across a much higher-latency link. Not every Tier 0 service needs multi-region; the decision should trace back to the BIA's regional-failure scenario and its associated impact, not be adopted reflexively because "more redundancy is always better."

## Implementation and Automation

### Example: Circuit Breaker and Timeout Configuration

A representative configuration for an HTTP client library's resilience policy (illustrative, vendor-neutral pseudo-config applicable to most modern resilience libraries):

```yaml
# resilience-policy.yaml
dependency: inventory-service
timeout_ms: 800
retry:
  max_attempts: 3
  backoff: exponential
  base_delay_ms: 100
  jitter: true
circuit_breaker:
  failure_rate_threshold_pct: 50
  minimum_calls: 20
  wait_duration_open_state_s: 30
  half_open_trial_calls: 5
bulkhead:
  max_concurrent_calls: 40
  max_queue_size: 10
```

### Example: Kubernetes-Native Availability Controls

Against the Kubernetes 1.31.x baseline in [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md), pod-level availability guarantees are expressed with anti-affinity and disruption budgets:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout-api
spec:
  replicas: 6
  selector:
    matchLabels: { app: checkout-api }
  template:
    metadata:
      labels: { app: checkout-api }
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels: { app: checkout-api }
      containers:
        - name: checkout-api
          image: example.registry/checkout-api:2026.07.1
          readinessProbe:
            httpGet: { path: /healthz/ready, port: 8080 }
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /healthz/live, port: 8080 }
            periodSeconds: 10
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: checkout-api-pdb
spec:
  minAvailable: 4
  selector:
    matchLabels: { app: checkout-api }
```

The `topologySpreadConstraints` block enforces the multi-AZ redundancy from the design section; the `PodDisruptionBudget` prevents voluntary disruptions (node drains during patching, covered in [Chapter 6](06-maintenance-patching-and-upgrade-engineering.md)) from taking more capacity offline than the service can tolerate.

### Example: Load-Shedding Middleware Logic

```python
def should_shed(request, current_load_pct: float, threshold_pct: float = 90.0) -> bool:
    """Shed low-priority requests first as load approaches capacity."""
    if current_load_pct < threshold_pct:
        return False
    priority = request.headers.get("X-Request-Priority", "standard")
    # Shed standard-priority traffic before critical traffic.
    return priority != "critical"
```

Deploy this logic at the ingress or API-gateway layer so shedding decisions happen before request processing consumes downstream resources, and expose the shed rate as a metric — an unmonitored load-shedding path can silently drop a growing fraction of traffic without triggering alerts.

### Automating Failover Verification

```bash
#!/usr/bin/env bash
# verify-failover.sh: confirm a load balancer removes an unhealthy target
# within the configured RTO window.
set -euo pipefail

TARGET_ID="$1"
RTO_SECONDS="${2:-30}"

echo "Marking target $TARGET_ID unhealthy..."
example-lb-cli mark-unhealthy --target "$TARGET_ID"

START=$(date +%s)
while example-lb-cli target-status --target "$TARGET_ID" | grep -q "InService"; do
  ELAPSED=$(( $(date +%s) - START ))
  if (( ELAPSED > RTO_SECONDS )); then
    echo "FAIL: target still in service after ${ELAPSED}s (RTO=${RTO_SECONDS}s)"
    exit 1
  fi
  sleep 1
done
echo "PASS: target removed from rotation within $(( $(date +%s) - START ))s"
```

## Validation and Troubleshooting

### Validating HA Designs

- Confirm quorum configuration matches the documented cluster size and tolerance — an odd number of voting members for majority-quorum systems, or an explicit witness for two-node configurations.
- Confirm health checks reflect actual service health, not just process liveness: a readiness probe that only checks "is the process running" will not detect a service that is up but unable to reach its database, and traffic will continue to route to a functionally dead instance.
- Confirm replication lag is monitored continuously for asynchronous replication topologies, with alerting tied to the RPO budget established in [Chapter 2](02-business-impact-analysis-and-continuity-planning.md).

### Common Failure Modes

| Symptom | Likely Cause |
| --- | --- |
| Failover takes far longer than designed RTO | Health check interval/threshold too lenient, or DNS TTL too high for DNS-based failover |
| Cluster becomes unavailable when it should have tolerated a node loss | Quorum miscalculated, or a maintenance operation dropped the cluster below quorum without accounting for the concurrent voluntary loss |
| Circuit breaker never opens despite clear dependency failure | `minimum_calls` threshold not reached because call volume is too low for the configured window |
| Retries make an outage worse | No backoff/jitter, causing synchronized retry storms; or retries applied to non-idempotent operations, causing duplicate side effects |
| Graceful degradation path itself fails under load | Fallback/default path was never load-tested and has its own uncharacterized capacity limit |

### Troubleshooting Split-Brain Symptoms

Divergent data between cluster nodes after a network event, or duplicate leader election log entries, are the primary symptoms. Resolution requires identifying the authoritative side (typically the side that retained quorum), reconciling or discarding divergent writes from the non-authoritative side per the application's conflict-resolution policy, and reviewing why the quorum/witness configuration failed to prevent the condition in the first place — split-brain occurring at all, even if survived, indicates a design gap that must be corrected before the next partition event.

## Security and Best Practices

- Health-check and failover-control endpoints are high-value targets: an attacker who can mark healthy targets unhealthy can trigger a denial-of-service through the resilience mechanism itself. Authenticate and restrict access to these control paths.
- Retry logic must be idempotency-aware; retrying a non-idempotent write (a payment charge, an inventory decrement) without an idempotency key can convert a resilience mechanism into a data-integrity or financial-correctness bug.
- Do not let graceful-degradation fallback paths bypass authorization or data-validation checks for the sake of availability; a "fail open" security control under load is rarely an acceptable trade-off and should be an explicit, reviewed exception, not a default.
- Test failover regularly (see [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md)) rather than relying on architecture review; untested failover is the single most common cause of an HA design not performing as expected during a real incident.
- Document and rehearse the human procedures around automated failover (who is paged, what the expected automated behavior is, when to intervene manually) so that operators do not fight an automated failover in progress under the false assumption that it has failed.

## References and Knowledge Checks

### References

- [Chapter 1](01-resilience-engineering-and-critical-service-design.md) and [Chapter 2](02-business-impact-analysis-and-continuity-planning.md) for the criticality tiers and RTO/RPO values that drive HA topology selection.
- Kubernetes documentation on topology spread constraints and pod disruption budgets, current to the 1.31.x baseline in [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Raft consensus algorithm reference material (raft.github.io) for the leader-election and quorum concepts summarized in this chapter.
- [Volume VII](../../volume-07-cloud-infrastructure/README.md), Cloud Infrastructure, for cloud-provider-specific multi-AZ and multi-region networking patterns referenced here at a vendor-neutral level.

### Knowledge Checks

1. A two-node database cluster has no witness node configured. Explain the specific failure scenario this leaves unprotected and how to correct it.
2. Why does adding retries with no backoff or jitter risk making an outage worse rather than better?
3. Given a service with RPO = 0 requirement, justify why asynchronous replication cannot be used regardless of its latency benefits.
4. Explain the difference between a liveness probe and a readiness probe, and describe a scenario where a service is "alive" but should not be "ready."
5. Why must a redundancy review examine compute, network, storage, and power layers independently rather than assuming redundancy at one layer implies it at the others?

## Hands-On Lab

### Lab: Circuit Breaker Behavior and Load-Balancer Failover Timing

**Objective:** Observe circuit-breaker state transitions under simulated dependency failure, and measure actual failover time against a target RTO using the failover-verification script from this chapter.

**Prerequisites:**

- `python3` (3.11+) with `pip install pybreaker` (or an equivalent circuit-breaker library available in your environment).
- `bash`, `curl`.
- Optional: access to a lab load balancer CLI matching the `example-lb-cli` interface used in this chapter's script; if unavailable, the failover portion can be simulated with the provided stub described in step 4.

**Procedure:**

1. Create a working directory:

   ```bash
   mkdir -p ~/labs/resilience-ch3 && cd ~/labs/resilience-ch3
   ```

2. Write `breaker_demo.py` wrapping a deliberately failing function in a circuit breaker configured with `fail_max=3` and `reset_timeout=10`:

   ```python
   import pybreaker
   import time

   breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)

   def flaky_dependency(succeed: bool):
       if not succeed:
           raise RuntimeError("simulated dependency failure")
       return "ok"

   for i in range(6):
       try:
           result = breaker.call(flaky_dependency, False)
           print(f"call {i}: {result}")
       except pybreaker.CircuitBreakerError:
           print(f"call {i}: circuit OPEN, call rejected")
       except RuntimeError as e:
           print(f"call {i}: dependency failed ({e}), breaker state={breaker.current_state}")
       time.sleep(1)
   ```

3. Run the script:

   ```bash
   python3 breaker_demo.py
   ```

**Expected Result:** The first three calls fail with `RuntimeError` and the breaker's state progresses toward `open`; from the fourth call onward, calls are rejected immediately with `CircuitBreakerError` rather than waiting for the simulated dependency to fail again — demonstrating the fail-fast behavior described in this chapter's theory section.

4. If a lab load balancer is unavailable, create a stub `example-lb-cli` shell function to exercise the verification script's logic locally:

   ```bash
   cat <<'EOF' > example-lb-cli
   #!/usr/bin/env bash
   STATE_FILE="/tmp/lb-target-state"
   case "$1" in
     mark-unhealthy) echo "Draining" > "$STATE_FILE" ;;
     target-status) sleep 5; echo "Draining" > "$STATE_FILE"; cat "$STATE_FILE" ;;
   esac
   EOF
   chmod +x example-lb-cli
   export PATH="$PWD:$PATH"
   ```

5. Save the `verify-failover.sh` script from this chapter and run it against the stub with a generous RTO budget:

   ```bash
   bash verify-failover.sh demo-target 60
   ```

**Expected Result:** The script reports `PASS` once the stub's status output no longer contains `InService` (immediately, in this simplified stub), confirming the timing-loop logic functions correctly.

**Negative Test:** Rerun the verification script with an artificially tight RTO budget of 0 seconds (`bash verify-failover.sh demo-target 0`). Confirm the script now reports `FAIL`, proving the RTO enforcement branch is reachable and correctly triggers, not just the success path.

**Cleanup:**

```bash
cd ~ && rm -f /tmp/lb-target-state && rm -rf ~/labs/resilience-ch3
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

High availability and fault tolerance translate the RTO/RPO targets from the BIA into concrete architecture: topology choice (active-active, active-passive, clustered), quorum-safe failover, and request-path resilience primitives (timeouts, retries, circuit breakers, bulkheads), backed by graceful-degradation modes for conditions that exceed absorption capacity. None of these mechanisms are self-verifying — the chapter's emphasis on failover testing sets up [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md)'s resilience testing and chaos engineering practice, which turns "should fail over correctly" into "verified to fail over correctly."

**Completion checklist:**

- [ ] Can select an HA topology (active-active, active-passive, cluster) from a given RTO/RPO target.
- [ ] Can explain quorum and split-brain and correctly size a cluster or specify a witness for even-numbered/two-node configurations.
- [ ] Implemented and tested a circuit breaker showing the closed-to-open state transition under simulated failure.
- [ ] Can articulate the synchronous-vs-asynchronous replication trade-off in terms of RPO and latency.
- [ ] Designed at least one graceful-degradation mode (load shedding, feature fallback, or read-only mode) for a sample service.
- [ ] Measured actual failover time against a target RTO using an automated verification script.
