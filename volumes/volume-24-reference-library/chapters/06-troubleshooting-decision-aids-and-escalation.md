# Chapter 06: Troubleshooting Decision Aids and Escalation

## Learning Objectives

- Apply a structured troubleshooting methodology (bottom-up, top-down, or
  divide-and-conquer) appropriate to a given symptom instead of defaulting
  to unstructured trial and error.
- Work through text-based decision trees for the four most common
  enterprise incident categories: no connectivity, degraded performance,
  authentication failure, and service unavailable.
- Distinguish a closed port, a filtered/dropped port, and an
  application-layer failure using observable evidence, building on
  Chapter 02.
- Apply a severity classification and escalation matrix consistently
  across platforms, and know when to escalate rather than continue
  independent diagnosis.
- Produce an incident timeline sufficient to support both a fix and a
  later root-cause/post-incident review (Chapter 07).

## Theory and Architecture

Troubleshooting methodology exists to convert an unstructured symptom
report ("it's slow," "it doesn't work") into a bounded, falsifiable
hypothesis that can be tested. Three complementary methodologies cover
nearly every situation in this encyclopedia:

- **Bottom-up (layered) troubleshooting** starts at the physical/link
  layer and works up the OSI stack (Volume II): cable/link state, then
  IP reachability, then transport (port open?), then application. This is
  the right default for "no connectivity" symptoms because each layer's
  failure has a distinct, checkable signature and lower layers are
  cheaper to rule out first.
- **Top-down troubleshooting** starts at the application/user-visible
  symptom and works downward, useful when the symptom is specific to one
  application while other traffic on the same path is known-good — it
  avoids re-verifying infrastructure that other evidence already confirms
  is working.
- **Divide-and-conquer** starts at a midpoint in the path or stack (often
  the load balancer, the default gateway, or the API gateway) and
  branches up or down based on the result, minimizing the number of
  checks needed when the failing component is unknown and the path is
  long.

A **decision tree** formalizes one of these methodologies into a
repeatable sequence: a yes/no or small-multiple-choice question at each
node, with each branch leading to either the next question or a specific
next action. The value of a written decision tree is not that it replaces
engineering judgment — it is that it prevents an engineer under time
pressure from skipping a cheap, high-signal check in favor of an
expensive, low-signal one, and it lets a less experienced responder reach
a competent first triage before an escalation is needed.

**Escalation** is the deliberate handoff of an incident to broader
expertise, higher authority, or additional resources when the current
responder's tools, access, or knowledge are insufficient to continue
safely or quickly enough. Escalation is not failure; treating escalation
as a last resort after independent effort has been exhausted is the most
common reason mean time to resolution (MTTR) exceeds an organization's
target.

## Design Considerations

- **Write decision trees for the symptom categories that recur most
  often in your environment**, not for every possible failure; a short
  tree used consistently outperforms a comprehensive tree no one has time
  to read during an incident.
- **Anchor each decision tree node to a specific, runnable check**, not
  to a vague question. "Is the network okay?" is not a decision tree
  node; "Does `ping <default gateway>` succeed?" is.
- **Define severity independent of root cause**, since root cause is
  often unknown when severity must first be assigned; base severity on
  observed business/user impact and scope (Chapter 07 formalizes this for
  security incidents specifically).
- **Set an explicit time-box for independent diagnosis before
  escalation**, calibrated to severity — a Sev 1 with unknown cause after
  15 minutes of structured diagnosis should escalate; a Sev 4 may
  reasonably run for hours before escalation is warranted.
- **Design the escalation path to name a role, not only a person** (on-call
  rotation, secondary on-call, platform owner, vendor TAC), so that
  escalation does not stall when a specific individual is unavailable.
- **Capture the incident timeline as you go, not retroactively.** A
  timeline reconstructed after resolution loses the sequence and timing
  precision that root-cause analysis (Chapter 07) depends on.

## Implementation and Automation

### Decision tree 1 — No connectivity (host or service unreachable)

```text
START: Host/service X is unreachable from host/location Y.

1. Can Y reach its own default gateway? (ping/traceroute first hop)
   NO  -> Local link/interface/VLAN problem on Y.
          Check: link state, IP config, VLAN assignment, cable/vNIC.
          -> STOP (local fix) or escalate to site/network team.
   YES -> continue to 2.

2. Can Y reach X's IP address (ping, or TCP SYN test if ICMP is filtered)?
   NO  -> Routing or ACL/firewall problem between Y and X.
          Check: traceroute to find the last responding hop;
          check firewall rule set against the five-field flow
          statement (Chapter 02) at each hop between Y and X.
          -> STOP (routing/ACL fix) or escalate to network/security team.
   YES -> continue to 3.

3. Is the target port open on X? (nc -zv X <port> / Test-NetConnection)
   NO (RST received)     -> Port is closed or the service is down on X.
                             Check: is the service process/listener
                             running on X? (ss -tulpn / Get-NetTCPConnection)
                             -> If not running, this is a service problem,
                                not a network problem; go to Decision
                                tree 3 (service unavailable).
   NO (timeout, no RST)  -> Port is filtered/dropped somewhere in the path.
                             Check: firewall rule sets on X, on any
                             security appliance in the path, and on any
                             host-based firewall (nftables/firewalld/
                             Windows Firewall) on X itself.
                             -> STOP (firewall fix) or escalate.
   YES                    -> Port is open; this is an application-layer
                              problem, not a network problem.
                              -> Proceed to application-specific
                                 diagnostics (logs, application health
                                 checks) or Decision tree 3.
```

### Decision tree 2 — Degraded performance (slow, not down)

```text
START: Users report X is "slow."

1. Is the degradation confirmed with a metric, not only a report?
   NO  -> Obtain a concrete measurement first (latency, response time,
          throughput) before proceeding; "slow" without a number cannot
          be diagnosed or later confirmed as resolved.
   YES -> continue to 2.

2. Is the degradation isolated to one path/user/location, or is it
   global to all consumers of X?
   ISOLATED -> Check the specific path: client-side resource
               (CPU/memory/network on the client), the specific network
               segment between that client and X, or a per-tenant
               rate limit.
   GLOBAL   -> continue to 3.

3. Is a resource utilization threshold exceeded on X or its immediate
   dependencies? (CPU, memory, disk I/O, connection pool, queue depth)
   YES -> Resource saturation. Identify which resource, and whether it
          is a capacity problem (scale) or a runaway consumer (a specific
          process, query, or client) driving the saturation.
   NO  -> continue to 4.

4. Has a recent change been made to X or a direct dependency (deploy,
   configuration change, upstream/downstream service, DNS, certificate
   rotation)? Check the change record log (Chapter 04).
   YES -> Correlate the change timestamp with the onset of degradation;
          if they align, treat the change as the primary hypothesis and
          consider a rollback per that change's recorded rollback plan.
   NO  -> Escalate for deeper analysis: distributed tracing (Volume XI),
          dependency health (upstream API/database latency), or an
          external factor (DDoS, upstream provider incident).
```

### Decision tree 3 — Service unavailable (process/service down)

```text
START: A service is confirmed down (port closed, process not found, or
health check failing).

1. Did the service crash, or was it never started / intentionally
   stopped? Check process manager state (systemctl status,
   Get-Service, Kubernetes pod status).
   CRASHED       -> Check the service's own logs for the failure reason
                     (journalctl -u <unit>, kubectl logs --previous,
                     Windows Event Viewer Application log) immediately
                     before the crash timestamp.
   NEVER STARTED -> Check for a failed dependency (a required mount,
                     network interface, or upstream service not ready
                     at boot/start time) or a configuration error
                     preventing startup.
   STOPPED       -> Check the change record log (Chapter 04) for an
                     intentional stop; if none exists, treat as
                     unauthorized/unexpected and consider Chapter 07.

2. Does restarting the service resolve the symptom?
   YES (and root cause is understood) -> Restart per the safe-
        administration gates (Chapter 01), document as a Tier 1/2
        change, and schedule root-cause follow-up if the underlying
        trigger (resource exhaustion, bad input, dependency flake) is
        not yet fixed.
   YES (but root cause is NOT understood) -> Restart to restore
        service if impact warrants it, but open a follow-up
        investigation; an unexplained fix is a latent recurring risk.
   NO -> Escalate; a service that will not stay up after a clean
         restart typically indicates a deeper dependency, resource, or
         configuration problem beyond first-line remediation.
```

### Severity classification matrix

| Severity | Definition | Example | Target Initial Response |
| --- | --- | --- | --- |
| Sev 1 (Critical) | Complete loss of a business-critical service, or an active security incident with confirmed impact | Production database cluster down; active data exfiltration confirmed | Immediate (minutes); page on-call, engage incident commander |
| Sev 2 (High) | Significant degradation or partial outage of a business-critical service, no acceptable workaround | Primary site down but DR failover functional; 50% error rate on a core API | Within 30 minutes |
| Sev 3 (Moderate) | Degraded non-critical service, or a critical service issue with an acceptable workaround | Reporting dashboard unavailable; one of N redundant nodes down | Within business hours |
| Sev 4 (Low) | Minor issue, cosmetic defect, or a single non-critical user affected | Broken link in an internal wiki; single workstation issue | Standard queue/backlog |

### Escalation matrix

| Trigger | Escalate To | When |
| --- | --- | --- |
| Sev 1/2 unresolved after time-box (organization-defined, commonly 15–30 minutes) | Secondary on-call / incident commander | Immediately at time-box expiry, not "just a bit longer" |
| Diagnosis requires access/privilege the responder does not hold | Platform/system owner with required access | As soon as the access gap is identified |
| Suspected security incident at any point in the tree above | Security/incident response team (Chapter 07) | Immediately; do not continue routine troubleshooting on a system suspected to be compromised without IR involvement |
| Root cause points to a vendor-controlled component (hardware, SaaS, cloud provider) | Vendor TAC / cloud provider support, with case number logged | Once internal diagnosis rules out the customer-controlled path |
| Multiple systems/teams affected simultaneously | Incident commander coordinating a bridge/war room | As soon as cross-team scope is recognized |

### Incident timeline format

```markdown
## Incident Timeline: <incident ID>

| Time (UTC) | Actor | Action / Observation | Evidence |
| --- | --- | --- | --- |
| 14:02 | Monitoring | Alert fired: API error rate > 5% | alert-14:02.png |
| 14:05 | J. Rivera | Confirmed with `curl` against health endpoint | curl-14:05.txt |
| 14:07 | J. Rivera | Ran Decision tree 1; port open, app-layer 500 errors | ss-output-14:07.txt |
| 14:10 | J. Rivera | Escalated to Sev 2 per matrix; paged secondary on-call | — |
| 14:18 | M. Chen | Identified recent deploy at 13:55 as correlated change | change-record-4471.md |
| 14:22 | M. Chen | Rolled back deploy per change record's rollback plan | rollback-log-14:22.txt |
| 14:26 | Monitoring | Error rate returned to baseline | dashboard-14:26.png |
```

## Validation and Troubleshooting

- **Confirm the fix against the same metric or check that first
  identified the problem**, not a different, looser check; if degraded
  latency triggered the incident, confirm resolution with latency, not
  simply "users say it feels fine."
- **Re-run the decision tree from its starting point after a fix** to
  confirm the entire path now resolves cleanly, not only the specific
  node believed to be the root cause; a partial fix can leave an earlier
  node newly failing in a way that was previously masked.
- **Watch for a fix that resolves the symptom but not the trigger.** A
  service restart (Decision tree 3) that clears an immediate outage
  without understanding what caused the crash is validated for the
  incident but not validated as a durable fix; track the follow-up
  separately.
- **Distinguish flapping from resolved.** A service or link that recovers
  and then fails again within a short window should not be marked
  resolved; extend observation before closing a Sev 1/2 incident.

## Security and Best Practices

- Treat any troubleshooting path that surfaces evidence of unauthorized
  access, unexpected privilege use, or unexplained configuration change as
  a potential security incident and route to Chapter 07's process rather
  than continuing routine troubleshooting alone.
- Avoid running state-changing commands (restarts, configuration
  rollbacks) on a system that may be compromised before incident response
  has had the opportunity to preserve forensic evidence (Chapter 07);
  a routine "fix it and move on" reflex can destroy the evidence needed
  to determine scope.
- Record who accessed what during an incident, not only what was
  changed; incident timelines are themselves security-relevant records
  and should be retained per the same policy as change and acceptance
  evidence (Chapter 05).
- Do not bypass authentication, disable logging, or use shared/emergency
  credentials to speed up diagnosis without following the organization's
  break-glass procedure and its required post-use review.
- After any Sev 1/2 incident, hold a blameless post-incident review and
  feed corrective actions back into the relevant baseline, template, or
  decision tree (Chapters 04–06) so the same failure is faster to
  diagnose or does not recur.

## References and Knowledge Checks

**References**

- Chapter 02 of this volume — five-field flow statements referenced in
  Decision tree 1.
- Chapter 04 of this volume — change records referenced in Decision trees
  2 and 3.
- Chapter 05 of this volume — evidence capture for incident timelines.
- Chapter 07 of this volume — incident response process for
  security-relevant findings surfaced during troubleshooting.
- Volume XI — Observability and Enterprise Operations (metrics, tracing,
  and alerting that supply Decision tree 2's inputs).
- Volume XX — Wireshark and Packet Analysis (packet-level evidence for
  Decision tree 1).

**Knowledge checks**

1. Explain when bottom-up troubleshooting is preferable to top-down, and
   give an example symptom for each.
2. In Decision tree 1, what is the diagnostic difference between a TCP
   RST and a timeout at the port-check step, and what does each imply
   about where to look next?
3. Why is severity defined by observed impact rather than by suspected
   root cause?
4. A troubleshooting session on Decision tree 3 uncovers an unexpected
   configuration change with no matching change record. What should
   happen next, and why should routine remediation not simply proceed?

## Hands-On Lab

**Objective:** Apply the decision trees in this chapter to a real or
simulated incident, produce a timeline, and correctly classify severity
and escalation.

**Prerequisites:** A lab environment where a service can be safely broken
and restored (for example, a Linux VM running a simple web service); a
Markdown editor; a way to induce at least one of: a network-layer block, a
port-level block, and a service crash.

1. Establish a working baseline: confirm a lab service is reachable end
   to end and record the baseline response time. **Expected result:** a
   documented, working baseline.
2. Simulate a failure by inducing exactly one condition (for example,
   block the service port with a host firewall rule, or stop the
   service process) without documenting in advance which one you chose.
   **Expected result:** the service becomes unreachable or degraded in an
   observable way.
3. Starting from Decision tree 1 or 3 as appropriate, work through each
   node in order, recording the check run and its result at each step.
   **Expected result:** a written record of the path taken through the
   tree, ending at a specific, correct diagnosis.
4. Classify the simulated incident's severity using the matrix in this
   chapter, and state which escalation trigger would apply if the
   time-box were exceeded. **Expected result:** a severity level and
   escalation trigger, both justified by the matrix criteria, not by
   intuition alone.
5. Produce an incident timeline in the format shown in this chapter,
   covering detection through resolution. **Expected result:** a
   timestamped timeline with at least four entries and linked evidence
   for each.
6. Resolve the simulated failure and re-run the same check that first
   detected it, confirming against the original baseline from step 1.
   **Expected result:** the service matches its original baseline
   behavior, not just "appears to work."
7. Negative test: re-introduce the same failure condition and confirm the
   decision tree reaches the same diagnosis a second time. **Expected
   result:** the tree is repeatable, not a one-time coincidence.

**Cleanup:** Remove any temporary firewall rules or induced failure
conditions, confirm the lab service is restored to its normal running
state, and delete lab-only incident records if they reference
non-representative test data.

## Summary and Completion Checklist

This chapter provided three text-based decision trees covering the
majority of first-line troubleshooting scenarios — no connectivity,
degraded performance, and service unavailable — built on the bottom-up,
top-down, and divide-and-conquer methodologies, along with a severity
classification matrix, an escalation matrix, and an incident timeline
format that feeds directly into the post-incident review process in
Chapter 07.

- [ ] I can select the appropriate troubleshooting methodology
      (bottom-up, top-down, divide-and-conquer) for a given symptom.
- [ ] I can work through all three decision trees in this chapter using
      real diagnostic commands.
- [ ] I can classify an incident's severity using observed impact, not
      assumed root cause.
- [ ] I know the escalation triggers in the matrix and when independent
      diagnosis should stop.
- [ ] I produced a timestamped, evidence-linked incident timeline for a
      simulated incident.
