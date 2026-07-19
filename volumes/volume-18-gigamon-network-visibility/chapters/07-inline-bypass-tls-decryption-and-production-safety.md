# Chapter 07: Inline Bypass, TLS Decryption, and Production Safety

## Learning Objectives

- Explain how inline deployment differs from the out-of-band model used in
  every prior chapter, and why it introduces availability risk that
  out-of-band delivery does not.
- Describe inline network groups, inline tool groups, and the difference
  between series and parallel inline tool arrangements.
- Explain heartbeat monitoring, fail-open versus fail-closed behavior, and
  maintenance mode as the mechanisms that keep an inline path safe.
- Compare centralized GigaSMART SSL/TLS decryption, inline decryption
  ahead of an in-path tool, and Precryption's host-based plaintext capture
  model.
- Design and validate an inline bypass deployment, including a controlled
  inline tool failure, without causing a production outage.

## Theory and Architecture

### Out-of-band versus inline: a different risk model

Every chapter so far has described **out-of-band (OOB)** delivery: the
fabric forwards a *copy* of traffic to a tool, and the tool's failure —
crash, overload, misconfiguration — has no effect on the original
traffic's path. Some security functions cannot work this way. An
intrusion prevention system (IPS) that only sees a copy of a malicious
packet cannot block it — by the time the copy arrives, the original has
already been delivered. Functions that must **block, delay, or modify**
traffic in real time — IPS, inline data-loss-prevention enforcement, and
inline decryption ahead of such tools — must sit directly **in the
path**, receiving the original traffic and deciding whether it continues.

This single requirement changes the risk model completely. An
out-of-band tool failing affects only that tool's visibility. An inline
tool failing can affect the production traffic flowing through it —
which is why inline deployment is a deliberate, narrowly scoped design
decision (as stated in [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md)'s design considerations) and why
Gigamon builds specific resiliency mechanisms — inline bypass — around
every inline deployment.

### Inline network groups and inline tool groups

An **inline network group** represents a production link the fabric has
been inserted into — conceptually similar to the TAP insertion pattern
from [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md), except that instead of splitting off a passive copy, the
fabric now sits directly in the traffic's path, bridging the two sides of
the link through its own inline network ports.

An **inline tool group** represents one or more inline tools (IPS
appliances, for example) attached to that inline network group through
dedicated inline tool ports. Two arrangements are common:

- **Series.** Traffic passes through multiple inline tools one after
  another (for example, an inline decryption stage followed by an IPS),
  each tool seeing the previous tool's output.
- **Parallel.** Traffic is load-balanced across multiple instances of the
  same tool type for capacity scaling, similar in spirit to GigaStream
  load balancing ([Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md)) but applied to inline, bidirectional
  traffic rather than one-way tool delivery.

An **inline map** governs which traffic from an inline network group is
sent to which inline tool group — the same Flow Mapping concepts from
[Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md) apply, but the destination is a bidirectional inline tool group
rather than a one-way tool port, and packets returned from the inline
tool (after inspection, and potentially after modification or blocking)
are forwarded back onto the production link rather than simply
disappearing into a tool's ingest pipeline.

### Heartbeat, fail-open, and fail-closed

Because production traffic depends on the inline tool being healthy,
GigaVUE-OS actively monitors each inline tool's health with a
**heartbeat** — a periodic probe sent through the tool and expected back
within a defined interval. If the heartbeat fails to return (the tool has
crashed, hung, or is otherwise not forwarding traffic), the fabric must
decide what happens to production traffic next, and this decision is
configured explicitly per inline tool group:

- **Fail-open (bypass).** On heartbeat failure, the fabric routes traffic
  around the failed tool, restoring connectivity for the production link
  at the cost of losing that tool's inspection for the duration of the
  outage. This is the common choice for availability-prioritized
  deployments, where a security tool outage should not become a network
  outage.
- **Fail-closed.** On heartbeat failure, the fabric blocks traffic on that
  path rather than allowing it through uninspected. This is the choice
  for deployments where uninspected traffic is a greater risk than a
  service interruption (for example, a segment carrying traffic subject
  to a compliance mandate requiring continuous inspection).

A **negative heartbeat** variant, where the health probe is designed to
detect a tool that is technically forwarding traffic but has failed in a
way that basic link-state monitoring would miss, provides a more rigorous
health signal than link state alone for tools whose failure mode is
"passes traffic through but has stopped actually inspecting it."

**Maintenance mode** allows an operator to deliberately bypass an inline
tool group for planned tool maintenance (a software upgrade, a hardware
swap) without waiting for or relying on heartbeat failure detection —
a controlled, intentional bypass rather than a reactive one.

### SSL/TLS decryption: three models compared

| Model | Where decryption happens | Key handling | Typical use |
| --- | --- | --- | --- |
| Centralized GigaSMART decryption ([Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md)) | On the GigaSMART engine, out-of-band, before delivery to OOB tools | Requires configuring server certificates/keys (or session-key forwarding) on the fabric | Feeding plaintext to out-of-band tools that cannot decrypt independently |
| Inline decryption | On the GigaSMART engine, inline, ahead of an in-path tool such as an IPS | Same key-handling requirement as centralized decryption, but on the inline path, with the associated availability considerations of any inline stage | Allowing an inline security tool to inspect (and potentially block) plaintext content in real time |
| Precryption | On the monitored host itself, using eBPF to capture plaintext before encryption or after decryption inside the application/OS stack | No keys are intercepted, sniffed, or centrally managed at all — nothing is actually decrypted by the fabric | Modern hosts (particularly cloud-native and containerized workloads) where centralized key management is undesirable or infeasible, and where TLS 1.3 / perfect-forward-secrecy traffic would otherwise defeat traditional key-based decryption |

Precryption represents a materially different approach from the other two
models: rather than obtaining and using the server's private key (or a
forwarded session key) to mathematically decrypt captured ciphertext, it
sits between the application and the host's encryption library and
captures traffic in the moment it is still plaintext — before the
encryption library processes it outbound, or after the library processes
it inbound. Because it never touches a key or performs decryption itself,
it works against TLS 1.3 and perfect-forward-secrecy configurations that
make traditional key-based decryption impossible without cooperation from
the endpoint, and it removes centralized key custody as a security
concern entirely. Its trade-off is that it requires a host-based sensor
component, so it applies to hosts the organization can instrument (owned
servers, container hosts) rather than arbitrary network segments a TAP or
SPAN can passively observe.

## Design Considerations

- **Justify every inline placement individually.** [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md) established
  this principle; it is worth restating here because inline design is
  where the consequence of skipping it is most severe. A tool placed
  inline "for convenience" (to simplify some other part of the topology)
  rather than because it must block or modify traffic in real time adds a
  permanent availability dependency the organization did not need to
  accept.
- **Choose fail-open versus fail-closed per segment, not fabric-wide.** A
  single default applied uniformly across every inline tool group ignores
  the fact that different segments carry different risk profiles — an
  internet-edge IPS protecting general corporate traffic may reasonably
  fail open, while a segment subject to a regulatory continuous-inspection
  requirement may need to fail closed even at the cost of availability.
- **Plan capacity for series chains realistically.** Each additional
  inline tool in a series arrangement adds latency and an additional
  potential point of failure; validate that the cumulative latency budget
  and the cumulative availability risk of the full chain (not just each
  individual tool) remains acceptable for the traffic it serves.
- **Decide the decryption model based on the tool's deployment mode and
  the traffic's TLS characteristics, not habit.** An organization already
  running centralized GigaSMART decryption for out-of-band tools should
  not assume the same key-management approach is appropriate for a new
  inline IPS deployment, and should evaluate Precryption specifically for
  TLS 1.3/PFS-heavy environments where key-based decryption is
  increasingly difficult to sustain.
- **Schedule and rehearse maintenance-mode procedures before they are
  needed under pressure.** An operator invoking maintenance mode for the
  first time during an active incident, rather than as a rehearsed
  procedure, is far more likely to make an error that turns a tool
  maintenance event into a broader outage.

## Implementation and Automation

### Configuring an inline network group

```text
(admin) (config) # port 1/1/c1 params admin enable
(admin) (config) # port 1/1/c1 type inline-network
(admin) (config) # port 1/1/c2 params admin enable
(admin) (config) # port 1/1/c2 type inline-network

(admin) (config) # inline-network alias edge-link-01
(admin) (config inline-network alias edge-link-01) # port-list 1/1/c1,1/1/c2
(admin) (config inline-network alias edge-link-01) # traffic-path to-inline-tool
(admin) (config inline-network alias edge-link-01) # exit
```

### Configuring an inline tool group with heartbeat

```text
(admin) (config) # port 1/1/c3 params admin enable
(admin) (config) # port 1/1/c3 type inline-tool
(admin) (config) # port 1/1/c4 params admin enable
(admin) (config) # port 1/1/c4 type inline-tool

(admin) (config) # inline-tool alias ips-primary
(admin) (config inline-tool alias ips-primary) # port-list 1/1/c3,1/1/c4
(admin) (config inline-tool alias ips-primary) # heartbeat enable
(admin) (config inline-tool alias ips-primary) # heartbeat interval 500
(admin) (config inline-tool alias ips-primary) # failover-action tool-inline-failover
(admin) (config inline-tool alias ips-primary) # fail-mode open
(admin) (config inline-tool alias ips-primary) # exit
```

### Binding the inline network to the inline tool group

```text
(admin) (config) # inline-map alias edge-to-ips
(admin) (config inline-map alias edge-to-ips) # inline-network edge-link-01
(admin) (config inline-map alias edge-to-ips) # inline-tool ips-primary
(admin) (config inline-map alias edge-to-ips) # rule add priority 10 pass any
(admin) (config inline-map alias edge-to-ips) # exit
(admin) (config) # write memory
```

### Invoking maintenance mode

```text
(admin) # inline-tool alias ips-primary maintenance-mode enable
# ... perform tool maintenance ...
(admin) # inline-tool alias ips-primary maintenance-mode disable
```

### Configuring inline decryption ahead of the inline tool group

```text
(admin) (config) # gsgroup alias gs-inline-decrypt
(admin) (config gsgroup alias gs-inline-decrypt) # gsop alias inline-ssl-decrypt
(admin) (config gsgroup gsop alias inline-ssl-decrypt) # type ssl-decrypt
(admin) (config gsgroup gsop alias inline-ssl-decrypt) # cert-key-profile edge-tls-profile
(admin) (config gsgroup gsop alias inline-ssl-decrypt) # exit
(admin) (config gsgroup alias gs-inline-decrypt) # exit
```

> As with prior chapters, exact inline-network, inline-tool, and
> inline-map keyword syntax, default fail-mode behavior, and heartbeat
> parameters vary by GigaVUE-OS release and platform; confirm against the
> release documentation before deploying to a production inline path, and
> validate fail-mode behavior in a lab before relying on it in production
> (see Hands-On Lab).

## Validation and Troubleshooting

- **Traffic drops entirely as soon as an inline tool group is
  activated.** Confirm inline network port cabling matches the intended
  A/B link orientation, and confirm the inline map's rule set is not
  inadvertently narrower than the traffic actually traversing the link —
  unlike an out-of-band map, an inline map with an unintentionally
  restrictive rule set blocks unmatched traffic rather than merely
  failing to deliver a copy of it.
- **An inline tool failure does not trigger the expected bypass.**
  Confirm heartbeat is actually enabled and the interval/timeout is
  appropriate for the tool's expected response characteristics; a
  heartbeat interval set too long can leave production traffic blocked
  (in fail-closed mode) or degraded far longer than intended before
  failover triggers.
- **Traffic continues flowing through a tool believed to have failed.**
  If only link-state monitoring is configured (no heartbeat, or a
  heartbeat that only checks basic reachability), a tool that is up but
  has stopped meaningfully inspecting traffic can appear healthy; this is
  the scenario negative heartbeat is designed to catch, and its absence is
  a common gap in early inline deployments.
- **Latency complaints after adding a series inline tool.** Measure
  per-hop latency contribution across the full inline chain, not just the
  newly added tool in isolation — a chain of individually low-latency
  tools can still accumulate to a latency budget that affects
  latency-sensitive applications.
- **Maintenance mode was invoked but traffic still routes through the
  tool being serviced.** Confirm maintenance mode was invoked on the
  correct inline tool group alias — in a fabric with several inline tool
  groups, invoking maintenance mode against the wrong alias produces this
  exact symptom and is a common operator error under time pressure.

## Security and Best Practices

- Require a documented, approved justification for every new inline tool
  placement, referencing the specific blocking or real-time-modification
  requirement that makes out-of-band delivery insufficient.
- Set fail-mode deliberately per inline tool group based on a documented
  risk decision for that specific segment, not a fabric-wide default
  applied without review.
- Rehearse inline tool failure and maintenance-mode procedures in a lab
  environment (see Hands-On Lab) before an engineer is expected to perform
  them under production incident pressure.
- Protect decryption key material (for centralized or inline GigaSMART
  decryption) with the same custody discipline as any other private key
  in the organization's PKI, and evaluate Precryption specifically as a
  way to remove centralized key custody as a risk in eligible
  environments.
- Monitor and alert on inline tool group health and fail-mode transitions
  in real time — a fail-open event that goes unnoticed for an extended
  period is a silent loss of security coverage, not merely an
  availability event.
- Review series inline tool ordering periodically; placing a
  higher-failure-rate tool earlier in a chain compounds availability risk
  for every tool downstream of it.

## References and Knowledge Checks

**References**

- [Gigamon, *Configure Inline Bypass Solutions* documentation](https://docs.gigamon.com/doclib/Content/GV-FM-UG/Configure_Inline_Bypass_Solutions.html) — inline
  network, inline tool, and inline map configuration model.
- [Gigamon, *GigaSMART SSL/TLS Decryption* product page](https://www.gigamon.com/products/optimize-traffic/traffic-intelligence/gigasmart/ssl-tls-decryption.html) — centralized and
  inline decryption architecture.
- [Gigamon, *Precryption Technology* announcement and product materials](https://www.gigamon.com/campaigns/precryption.html) —
  eBPF-based plaintext capture without key handling.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline.

**Knowledge checks**

1. Why can an IPS not be deployed purely out-of-band, and what
   availability risk does moving it inline introduce that out-of-band
   delivery does not have?
2. Explain the difference between fail-open and fail-closed, and describe
   one segment characteristic that would justify each choice.
3. What does a negative heartbeat detect that basic link-state monitoring
   does not?
4. How does Precryption's approach to obtaining plaintext visibility
   differ fundamentally from both centralized and inline GigaSMART
   decryption, and why does that difference matter for TLS 1.3 traffic?

## Hands-On Lab

**Objective:** Build a lab inline bypass deployment with heartbeat-based
failover configured fail-open, validate that production traffic continues
to flow when the inline tool is deliberately failed, and validate
maintenance mode as a controlled alternative — entirely in an isolated lab
segment.

**Prerequisites**

- A lab GigaVUE HC Series node (or lab-equivalent) with inline-capable
  ports, continuing from prior chapters' lab node where practical.
- A lab inline tool — a simple bump-in-the-wire device or a VM configured
  to bridge two interfaces is sufficient to stand in for a production IPS
  for this lab's purposes.
- Two lab hosts positioned on either side of the inline link to generate
  and receive test traffic.
- An isolated lab network segment — this lab deliberately fails a device
  in the traffic path and must never be performed against a production
  link.

**Steps**

1. Cable the lab inline network group between the two lab hosts' link,
   and cable the lab inline tool to the inline tool ports, following the
   pattern in Implementation and Automation.
2. Configure the inline network group, inline tool group with heartbeat
   enabled at a short interval, and an inline map binding them with a
   `pass any` rule.
3. Set the inline tool group's fail-mode to open (bypass).
4. From one lab host, start a continuous ping (or equivalent continuous
   traffic) to the other lab host across the inline link.
   **Expected result:** traffic flows normally, passing through the
   healthy inline tool.
5. Confirm heartbeat status shows healthy for the inline tool group
   (`show inline-tool` or the equivalent status command).
6. **Controlled failure test:** power off, disconnect, or otherwise fail
   the lab inline tool while the continuous traffic test from step 4 is
   still running.
   **Expected result:** a brief interruption occurs while the heartbeat
   failure is detected, after which traffic resumes flowing (now bypassing
   the failed tool) because fail-mode is set to open — confirming
   fail-open behavior protects production connectivity when an inline
   tool fails.
7. Restore the lab inline tool and confirm the inline tool group returns
   to healthy status and traffic resumes routing through it rather than
   remaining in bypass.
8. **Negative test:** change the inline tool group's fail-mode to closed,
   repeat the controlled failure test from step 6, and observe the
   result.

   ```text
   (admin) (config inline-tool alias ips-primary) # fail-mode closed
   ```

   **Expected result:** this time, traffic stops entirely when the tool
   fails and does not resume until the tool is restored, demonstrating
   the fail-closed trade-off described in Theory and Architecture — a
   security-availability trade-off made deliberately, not by default.
9. Restore fail-mode to the value appropriate for this lab's intended
   later use, and invoke maintenance mode manually, confirming traffic
   bypasses the tool without waiting for a heartbeat failure:

   ```text
   (admin) # inline-tool alias ips-primary maintenance-mode enable
   ```

   **Expected result:** traffic continues flowing (bypassing the tool)
   immediately upon invoking maintenance mode, confirming the controlled
   bypass path works independently of heartbeat detection.
10. **Cleanup:** disable maintenance mode, restore the inline tool group
    and inline map to a known-good baseline configuration (or remove them
    entirely if the lab topology will be reused for [Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md) or 09),
    and stop the continuous traffic test.

## Summary and Completion Checklist

Inline deployment trades the safety of out-of-band delivery for the
ability to block or modify traffic in real time, and that trade must be
made deliberately, tool by tool. Inline bypass — heartbeat monitoring,
configurable fail-open/fail-closed behavior, and maintenance mode — is
what makes accepting that trade survivable in production, and every
inline tool group's fail-mode should reflect a documented decision about
that specific segment's risk profile. Decryption for inline (and
out-of-band) tools has matured beyond a single centralized-key model:
centralized GigaSMART decryption, inline decryption, and the newer
Precryption approach each fit different deployment modes and TLS
characteristics, and choosing among them is itself a design decision, not
a default.

- [ ] Can explain why some security functions require inline placement
      and what risk that placement introduces.
- [ ] Can describe inline network groups, inline tool groups, and series
      versus parallel arrangements.
- [ ] Can explain heartbeat, fail-open/fail-closed, and maintenance mode
      and when each fail-mode is appropriate.
- [ ] Can compare centralized decryption, inline decryption, and
      Precryption and state a scenario favoring each.
- [ ] Completed the hands-on lab, including the controlled failure test,
      the negative test, and cleanup.
