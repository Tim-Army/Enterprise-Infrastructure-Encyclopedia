# Chapter 5: Resilience Testing, Exercises, and Chaos Engineering

## Learning Objectives

- Explain why declared resilience (redundancy, HA design, backups, DR runbooks) is unverified until it has been exercised, and connect that principle back to Chapters 1–4.
- Distinguish exercise types (tabletop, walkthrough, simulation, parallel test, full interruption test) and select an appropriate type and cadence from a service's criticality tier.
- Apply the principles of chaos engineering: steady-state hypothesis, blast-radius control, and hypothesis-driven experimentation.
- Design a chaos experiment with explicit abort criteria and a controlled blast radius appropriate to production or pre-production environments.
- Run a game day exercising a specific failure mode end to end, including human response, not only automated failover.
- Build a resilience-testing program with a cadence tied to criticality tier rather than ad hoc, opportunistic testing.

## Theory and Architecture

### Untested Resilience Is a Hypothesis

Every prior chapter in this volume has said some version of the same thing: redundancy is a hypothesis until tested ([Chapter 1](01-resilience-engineering-and-critical-service-design.md)), a continuity plan untested for years is a common finding ([Chapter 2](02-business-impact-analysis-and-continuity-planning.md)), untested failover is the most common cause of an HA design underperforming during a real incident ([Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md)), and a backup that has not been restore-tested is not a verified control ([Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md)). This chapter formalizes the practice that turns "should work" into "verified to work": resilience testing, exercises, and chaos engineering. These are complementary, not interchangeable — exercises validate human procedure and coordination; chaos engineering validates system behavior under injected failure; both are necessary, and an organization that only does one has a real, uncharacterized gap in the other.

### The Exercise Maturity Ladder

Continuity and DR exercises increase in realism, cost, and risk together, and a mature resilience-testing program uses all of them at a cadence matched to criticality:

| Exercise Type | Description | Realism | Typical Cadence (Tier 0/1) |
| --- | --- | --- | --- |
| Tabletop | Discussion-based walkthrough of a scenario with the response team, no systems touched | Low | Quarterly |
| Walkthrough | Team steps through the actual runbook procedure verbally or on a non-production copy, checking each step is current and executable | Low–Moderate | Quarterly to semi-annually |
| Simulation | A realistic scenario is simulated (often with injected synthetic alerts) and the team responds as if it were real, without touching production | Moderate | Semi-annually |
| Parallel test | The DR environment is actually brought up and validated while production continues to run unaffected | High | Annually, more often for Tier 0 |
| Full interruption test | Production traffic is actually cut over to the DR environment (or a real component is actually failed) | Highest | At most annually for Tier 0; carries real business risk and requires explicit sign-off |

Each rung exercises something the rung below cannot: a tabletop finds gaps in the plan's logic and team knowledge; a parallel test finds gaps in whether the DR environment can actually absorb real-scale data and load; only a full interruption test proves the complete path, including the parts of the cutover (DNS propagation, client reconnection behavior, downstream partner systems) that are difficult to simulate convincingly. The ladder exists because the top rung is expensive and risky enough that it cannot be the only rung — running exclusively full interruption tests is operationally reckless, and running exclusively tabletops is operationally naive.

### Chaos Engineering Principles

Chaos engineering is the discipline of running controlled experiments against a system to build confidence in its ability to withstand turbulent, real-world conditions. It is distinguished from undirected "break things and see" testing by four principles, drawn from the discipline's founding practice at scale-out internet operators and now broadly adopted:

1. **Define a steady-state hypothesis** — establish a measurable definition of normal system behavior (a specific latency percentile, an error rate, a throughput figure) before injecting any failure, so a deviation can be detected objectively rather than judged by feel.
2. **Vary real-world events** — inject failures that reflect actual production risks: instance termination, network latency or partition, dependency failure, resource exhaustion, clock skew, region or AZ loss — rather than arbitrary or unrealistic faults.
3. **Run experiments in production, or as close to it as possible** — pre-production environments frequently lack production's scale, traffic patterns, and configuration drift, and a resilience gap that only appears at production scale will not be found anywhere else. This principle is also the one that most requires the blast-radius and safety controls covered in Design Considerations below.
4. **Automate experiments to run continuously** — a one-time chaos experiment proves the system was resilient to that fault on that day; continuous or regularly scheduled experiments catch resilience regressions introduced by later changes, the same way automated tests catch functional regressions.

### Failure Injection Categories

Chaos experiments typically inject one of several failure categories, each exercising a different resilience mechanism from earlier chapters:

- **Resource-level faults** — terminating an instance or container, exhausting CPU/memory/disk, killing a process — exercises the redundancy and self-healing mechanisms from Chapters 1 and 3.
- **Network faults** — added latency, packet loss, full partition between components — exercises timeouts, retries, circuit breakers, and quorum/split-brain handling from [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md).
- **Dependency faults** — a downstream service returns errors, times out, or degrades — exercises circuit breakers, bulkheads, and graceful degradation from [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md).
- **Zonal or regional faults** — simulated loss of an entire availability zone or region — exercises the multi-AZ/multi-region HA and DR patterns from Chapters 3 and 4.
- **State and data faults** — clock skew, corrupted or delayed replication, a stale cache — exercises data-consistency assumptions that are otherwise rarely tested outside of chaos experiments.

## Design Considerations

### Blast Radius Control

Running experiments in or near production is valuable precisely because it is realistic, which is also what makes an uncontrolled experiment dangerous. Blast radius control is the set of deliberate constraints that make production experimentation acceptably safe:

- **Scope the experiment to the smallest population that still produces a valid result** — a single instance or a single percentage of traffic, not "all instances" on a first run of a new experiment type.
- **Define explicit, automated abort criteria** — a steady-state metric crossing a defined threshold should automatically halt the experiment and revert the injected fault, without waiting for a human to notice and react.
- **Run during a window with adequate operational coverage** — an experiment run when the on-call team is least able to respond defeats the purpose of learning how the system and team behave together.
- **Have a verified, fast rollback for the injected fault itself** — the ability to stop injecting latency or to restart a terminated instance must be at least as reliable as the experiment tooling that started the fault.

### Notified vs. Surprise Exercises

Both notified (scheduled, announced) and unannounced exercises have a place, and they test different things. A notified exercise, run with the team aware in advance, primarily validates the technical mechanism and the runbook's correctness under low-stress conditions. An unannounced exercise additionally validates real-world detection and response — whether monitoring actually pages the right people, whether the runbook is findable and current under time pressure, and whether the team's actual behavior matches the documented procedure. Unannounced exercises carry materially higher risk of confusion, wasted incident-response cycles, or unintended escalation, and should be reserved for mature programs that have already validated the mechanism through notified testing first; introducing surprise before the underlying mechanism is proven conflates "the system failed the experiment" with "the team was caught off guard," which are different findings requiring different fixes.

### Game Day Format

A game day is a scheduled, facilitated exercise combining a chaos experiment (or a simulated equivalent) with active human response, run against a specific hypothesis about a specific failure mode. An effective game day has:

- A single, clearly stated hypothesis (for example: "the checkout service will maintain a 99.9% success rate when the inventory-service dependency becomes fully unavailable for 10 minutes").
- A facilitator who is not also a responder, responsible for injecting the fault, tracking the timeline, and enforcing abort criteria.
- Observers capturing what actually happened — timeline, decisions made, tooling gaps found — independent of the responders' own after-action recollection, which is reliably incomplete under the stress of an active exercise.
- A blameless retrospective producing specific, owned follow-up actions, not a general sense that "it went fine" or "it went badly."

### Cadence Tied to Criticality Tier

Exercise and chaos-experiment cadence should scale with the criticality tiers established in [Chapter 1](01-resilience-engineering-and-critical-service-design.md), mirroring the same logic already applied to backup verification cadence in [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md):

| Tier | Tabletop/Walkthrough | Simulation/Parallel Test | Chaos Experiments |
| --- | --- | --- | --- |
| Tier 0 | Quarterly | Semi-annually to annually | Continuous, automated, low blast radius |
| Tier 1 | Semi-annually | Annually | Regularly scheduled, moderate blast radius |
| Tier 2 | Annually | As feasible | Opportunistic |
| Tier 3/4 | As feasible | Rarely required | Not typically required |

A Tier 0 service with no chaos-experiment history and a Tier 3 batch job exercised quarterly represents the same category of mismatch flagged in [Chapter 1](01-resilience-engineering-and-critical-service-design.md)'s discussion of aligning architecture to business criticality — testing investment, like redundancy investment, should trace back to the criticality register.

## Implementation and Automation

### Chaos Experiment Specification as Code

```yaml
# chaos-experiment.yaml
experiment_id: inventory-service-dependency-failure
target_service: checkout-api
hypothesis:
  steady_state_metric: "checkout_success_rate_pct"
  steady_state_threshold: 99.5
method:
  fault_type: dependency_failure
  target_dependency: inventory-service
  failure_mode: "return HTTP 503 for all requests"
  duration_minutes: 10
blast_radius:
  environment: production
  traffic_percentage: 5
  excluded_customer_segments: ["enterprise-priority"]
abort_conditions:
  - metric: checkout_success_rate_pct
    operator: "<"
    threshold: 95.0
  - metric: checkout_error_rate_pct
    operator: ">"
    threshold: 10.0
rollback: "restore inventory-service to normal responses immediately on abort or completion"
schedule: "weekly, Tuesday 10:00, business-hours coverage window"
owner: checkout-team
```

Treating the experiment as structured, version-controlled data — following the same pattern used for the criticality register, backup policy, and BIA records in earlier chapters — makes the blast radius, hypothesis, and abort conditions explicit and reviewable before the experiment runs, rather than left as tribal knowledge in whoever is operating the chaos tooling that day.

### Example: Network Fault Injection

A representative, tool-agnostic approach to injecting latency using traffic-control primitives available on most Linux hosts:

```bash
#!/usr/bin/env bash
# inject-latency.sh: add artificial network latency to a target
# interface for a bounded duration, with automatic rollback.
set -euo pipefail

INTERFACE="$1"
LATENCY_MS="${2:-300}"
DURATION_S="${3:-600}"

echo "Injecting ${LATENCY_MS}ms latency on ${INTERFACE} for ${DURATION_S}s..."
tc qdisc add dev "${INTERFACE}" root netem delay "${LATENCY_MS}ms"

cleanup() {
  echo "Rolling back latency injection on ${INTERFACE}..."
  tc qdisc del dev "${INTERFACE}" root netem || true
}
trap cleanup EXIT

sleep "${DURATION_S}"
```

The `trap cleanup EXIT` line is deliberate: rollback must execute whether the script completes normally, is interrupted, or fails partway through, so that an aborted experiment cannot leave a fault injected indefinitely — the single most important safety property of any fault-injection tool.

### Example: Steady-State Monitor with Automated Abort

```python
import time
import sys

def steady_state_ok(get_metric_fn, threshold: float, comparison: str = "gte") -> bool:
    """Poll a metric source and return False the moment steady state
    is violated, so the caller can trigger an immediate abort."""
    value = get_metric_fn()
    if comparison == "gte":
        return value >= threshold
    return value <= threshold

def run_experiment(get_metric_fn, inject_fn, rollback_fn,
                    threshold: float, duration_s: int, poll_interval_s: int = 5):
    inject_fn()
    elapsed = 0
    try:
        while elapsed < duration_s:
            if not steady_state_ok(get_metric_fn, threshold):
                print(f"ABORT: steady state violated at {elapsed}s", file=sys.stderr)
                return False
            time.sleep(poll_interval_s)
            elapsed += poll_interval_s
        print("Experiment completed without violating steady state")
        return True
    finally:
        rollback_fn()
```

Wrapping `rollback_fn()` in a `finally` block mirrors the `trap cleanup EXIT` pattern above — abort logic and rollback logic must be structurally guaranteed to run, not merely present in the code's happy path.

### Game Day Facilitation Checklist

```markdown
# Game Day: <hypothesis-id>

## Pre-Exercise
- [ ] Hypothesis and steady-state metric agreed and documented.
- [ ] Blast radius and abort criteria reviewed and approved.
- [ ] Facilitator and independent observer assigned (neither is a responder).
- [ ] Rollback mechanism tested in isolation before the exercise.

## During Exercise
- [ ] Facilitator injects fault at the scheduled time and starts the timeline log.
- [ ] Observer records decisions, tool gaps, and communication in real time.
- [ ] Abort criteria monitored continuously; facilitator has sole authority to abort.

## Post-Exercise
- [ ] Fault confirmed fully rolled back and steady state confirmed restored.
- [ ] Blameless retrospective scheduled within 5 business days.
- [ ] Follow-up actions assigned owners and due dates, tracked to closure.
```

## Validation and Troubleshooting

### Validating a Resilience-Testing Program

- Confirm every Tier 0/1 service has exercise and chaos-experiment history matching the cadence table above, not just a plan stating that it should.
- Confirm abort criteria have actually been exercised at least once — an abort path that has never been triggered in practice is itself an untested control, subject to the same "declared but unverified" risk as everything else in this volume.
- Confirm retrospective follow-up actions are tracked to closure; a resilience-testing program that surfaces findings but never resolves them accumulates the same kind of technical debt covered in [Chapter 7](07-technical-debt-modernization-and-platform-renewal.md).

### Common Failure Modes

| Symptom | Likely Cause |
| --- | --- |
| Chaos experiment causes a real, unintended outage | Blast radius scoped too broadly, or abort criteria threshold set too loosely to trigger before real damage |
| Steady-state metric never crosses threshold despite an apparent failure | The chosen metric does not actually reflect the failure mode being tested (measuring the wrong thing) |
| Game day "succeeds" but the same failure mode causes a real incident weeks later | Exercise used synthetic conditions unrepresentative of real production load or configuration, or follow-up actions from the retrospective were never completed |
| Team cannot execute the runbook under exercise conditions despite it existing | Runbook untested since last significant architecture change; walkthrough/tabletop cadence too infrequent to catch drift |
| Rollback fails to fully restore steady state after experiment | Rollback logic tested only against the specific fault duration used in prior runs, not against edge cases like an aborted mid-experiment run |

### Troubleshooting an Escalating Experiment

If an experiment's abort criteria trigger, or if steady state does not recover promptly after rollback, treat it as an active incident, not merely a failed test: engage the same incident response process used for real outages, because at that point the chaos experiment has become one. Capture the full timeline regardless of outcome — a chaos experiment that required manual incident response is a highly valuable finding, not a failed test to be quietly rerun until it "passes."

## Security and Best Practices

- Restrict access to fault-injection tooling as tightly as access to production infrastructure itself; the same capability that lets an authorized engineer inject a controlled failure could let an attacker cause an unauthorized denial of service, and this tooling should never share credentials with lower-privilege systems.
- Chaos engineering is not a substitute for adversarial security testing (red-teaming, penetration testing); it validates resilience to accidental and infrastructure-level failure, not to a deliberate, intelligent adversary adapting to defenses in real time. Coordinate with [Volume X](../../volume-10-enterprise-cybersecurity/README.md)'s cybersecurity practices for that distinct discipline, and do not conflate the two in program reporting.
- Require documented, revocable authorization for every production chaos experiment and every full interruption DR test, mirroring the dual-authorization practice for Tier 0 continuity-plan activation established in [Chapter 2](02-business-impact-analysis-and-continuity-planning.md).
- Log all fault-injection activity to the same audit trail as production changes; an unexplained latency spike or dependency failure that turns out to be an untracked chaos experiment wastes significant incident-response effort and erodes trust in monitoring data.
- Ensure experiment tooling itself has no standing write access beyond what the specific fault requires, following the bulkhead/least-privilege principle from [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) applied to the testing tooling rather than only to production services.

## References and Knowledge Checks

### References

- [Chapter 1](01-resilience-engineering-and-critical-service-design.md) for the criticality tiers this chapter's exercise cadence table is built on.
- [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) and [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md) for the HA and DR mechanisms chaos experiments and exercises validate.
- Principles of Chaos Engineering (principlesofchaos.org), the foundational public reference for the four principles summarized in this chapter.
- NIST SP 800-34 Rev. 1, *Contingency Planning Guide for Federal Information Systems*, for exercise-type definitions (tabletop through full interruption).

### Knowledge Checks

1. Explain the difference between an exercise (tabletop, walkthrough, simulation) and a chaos experiment, and why both are necessary rather than either alone.
2. Why does chaos engineering favor running experiments in or near production over pre-production environments, and what mitigates the risk of doing so?
3. A chaos experiment's rollback logic is written in the "happy path" of a script with no `trap`/`finally` equivalent. What specific failure mode does this leave unprotected against?
4. Explain why an unannounced (surprise) exercise should generally follow, not precede, a notified exercise of the same failure mode.
5. A game day "succeeds" with no abort triggered, but the retrospective produces no follow-up actions. Is this a healthy outcome? Why or why not?

## Hands-On Lab

### Lab: Hypothesis-Driven Fault Injection with Automated Abort

**Objective:** Run a scripted chaos-style experiment against a simulated dependency, observe a steady-state monitor detect a violation, trigger an automated abort and rollback, and confirm the rollback executes even when the experiment is interrupted.

**Prerequisites:**

- `python3` (3.11+).
- `bash`.

**Procedure:**

1. Create a working directory:

   ```bash
   mkdir -p ~/labs/resilience-ch5 && cd ~/labs/resilience-ch5
   ```

2. Save the `run_experiment` function from this chapter as `experiment.py`, and add a driver simulating a dependency that degrades partway through the experiment:

   ```python
   import time
   import random

   state = {"degraded": False, "injected": False}

   def get_metric():
       # Simulated checkout success rate: healthy at 99.8%, degraded at 80%.
       return 80.0 if state["degraded"] else 99.8

   def inject_fn():
       print("Injecting fault: inventory-service returning errors")
       state["injected"] = True

   def rollback_fn():
       print("Rolling back fault: inventory-service restored")
       state["degraded"] = False
       state["injected"] = False

   def run_experiment(get_metric_fn, inject_fn, rollback_fn, threshold, duration_s, poll_interval_s=1):
       inject_fn()
       elapsed = 0
       try:
           while elapsed < duration_s:
               value = get_metric_fn()
               if value < threshold:
                   print(f"ABORT: steady state violated at {elapsed}s (value={value})")
                   return False
               # Simulate the dependency actually degrading at the 3-second mark.
               if elapsed == 3:
                   state["degraded"] = True
               time.sleep(poll_interval_s)
               elapsed += poll_interval_s
           print("Experiment completed without violating steady state")
           return True
       finally:
           rollback_fn()

   result = run_experiment(get_metric, inject_fn, rollback_fn, threshold=95.0, duration_s=10)
   print(f"Experiment result: {'PASS' if result else 'ABORTED'}")
   print(f"Post-rollback state confirms fault cleared: degraded={state['degraded']}")
   ```

3. Run the experiment:

   ```bash
   python3 experiment.py
   ```

**Expected Result:** Output shows the fault injected, the steady-state metric dropping below the 95.0 threshold at approximately the 3–4 second mark, an `ABORT` message, and confirmation that rollback executed (`degraded=False`) even though the experiment exited early rather than running its full 10-second duration.

4. Modify the threshold to `70.0` and rerun. **Expected Result:** The experiment now completes its full duration without aborting, because the simulated degraded value (80.0) no longer violates the (now looser) steady-state threshold — demonstrating why threshold selection materially changes experiment outcomes and must reflect a genuine business-relevant steady state, not an arbitrary number.

**Negative Test:** Introduce a deliberate bug by editing `run_experiment` so `rollback_fn()` is called only after the `while` loop completes normally (move it below the loop, after the "Experiment completed" print, and remove the `try`/`finally` wrapper entirely) rather than being structurally guaranteed to run on every exit path. Rerun the original step-3 scenario (`threshold=95.0`, `duration_s=10`) unchanged. Confirm the script still reports the same `ABORT` message at the same elapsed time as before, but now `state["degraded"]` remains `True` after the script exits, because the early `return False` on the abort path no longer passes through any rollback call. Contrast this with step 3's original result, where `finally` guaranteed rollback ran even on the aborted path — demonstrating exactly the unprotected rollback failure mode described in this chapter's Knowledge Checks, and why rollback must be structurally guaranteed rather than merely present in the normal-completion path.

**Cleanup:**

```bash
cd ~ && rm -rf ~/labs/resilience-ch5
```

No shared or production systems were modified; the experiment was entirely simulated in local Python state.

## Summary and Completion Checklist

Resilience testing closes the loop this volume has been building since [Chapter 1](01-resilience-engineering-and-critical-service-design.md): every architectural and procedural control — redundancy, HA failover, backup, DR — is a hypothesis until it is exercised under conditions that resemble reality. Exercises (tabletop through full interruption) validate human procedure and coordination at increasing realism and cost; chaos engineering validates system behavior against a defined steady-state hypothesis with a controlled, reversible blast radius. Neither substitutes for the other, and both require a cadence tied to the criticality tiers established in [Chapter 1](01-resilience-engineering-and-critical-service-design.md). [Chapter 6](06-maintenance-patching-and-upgrade-engineering.md) shifts from testing resilience under injected failure to maintaining it under routine, planned change — patching and upgrades — where many of the same safety disciplines (staged rollout, abort criteria, rollback) reappear in a different context.

**Completion checklist:**

- [ ] Can place a given testing activity on the exercise maturity ladder (tabletop through full interruption) and justify its position.
- [ ] Can state the four principles of chaos engineering and apply them to design a specific experiment.
- [ ] Designed a chaos experiment specification with an explicit steady-state hypothesis, blast radius, and abort criteria.
- [ ] Implemented fault injection with a rollback mechanism structurally guaranteed to execute, including on abort or interruption.
- [ ] Ran a scripted experiment and observed an automated abort triggered by a steady-state violation.
- [ ] Can explain why chaos engineering and exercises are necessary complements, not substitutes for each other.
