# Chapter 8: Network Validation and Observability

## Learning Objectives

- Distinguish monitoring, observability, and validation as related but
  distinct disciplines, and explain when each applies.
- Explain SNMP polling architecture, including MIBs, OIDs, and the
  security difference between SNMPv2c and SNMPv3.
- Explain centralized syslog architecture, including severity levels and
  the role of accurate time synchronization from [Chapter 5](05-core-network-services.md).
- Compare flow-based telemetry (NetFlow, IPFIX, sFlow) and model-driven
  streaming telemetry as complementary data sources.
- Explain the purpose of a network baseline and how it changes what counts
  as an anomaly.
- Design an alerting strategy that avoids alert fatigue through thresholds
  and correlation.
- Build and interpret a basic centralized logging pipeline.

## Theory and Architecture

Every mechanism in Chapters 1 through 7 — addressing, switching, routing,
core services, wireless, and resilient design — eventually needs a way to
answer three operational questions: is it working right now, has it always
worked this way, and did a specific change make it better or worse. This
chapter is about the instrumentation that answers those questions, which
becomes the direct input to [Chapter 9](09-network-troubleshooting-and-operations.md)'s troubleshooting methodology.

### Monitoring, Observability, and Validation

These three terms are often used interchangeably but describe distinct
activities:

| Term | Question Answered | Typical Data |
| --- | --- | --- |
| Monitoring | "Is this specific, known thing healthy right now?" | Threshold-based checks against predefined metrics (interface up/down, CPU %, reachability) |
| Observability | "Given the data available, can I understand *any* internal state from the outside, including states no one predicted in advance?" | Rich, correlatable telemetry — metrics, logs, flow data, and traces considered together |
| Validation | "Does the network's actual, current state match the intended state?" | Structured comparison of configuration or operational state against a defined intent ("golden config," expected route table, expected neighbor adjacency) |

Monitoring answers questions you thought to ask in advance (an alert rule
that already exists); observability is what lets an engineer answer a
question they did not anticipate needing to ask, using data that was
already being collected for other purposes. Validation is narrower than
both: it is a pass/fail comparison against a defined intent, most often run
immediately before and after a change (developed further in [Chapter 9](09-network-troubleshooting-and-operations.md)'s
change-lifecycle discussion).

### SNMP: Polling Architecture

Simple Network Management Protocol (SNMP) is the long-standing standard for
polling device state. A **Management Information Base (MIB)** defines a
hierarchical namespace of **Object Identifiers (OIDs)**, each representing
one measurable value (interface octet counters, CPU utilization, chassis
temperature). A network management station polls devices for specific OIDs
on an interval, or receives an unsolicited **trap** when a device detects a
condition worth reporting immediately (such as a link-down event) rather
than waiting for the next poll.

| SNMP Version | Authentication | Encryption | Status |
| --- | --- | --- | --- |
| SNMPv1 | Community string (cleartext) | None | Obsolete; avoid |
| SNMPv2c | Community string (cleartext) | None | Still common; cleartext community string is a real weakness |
| SNMPv3 | User-based (MD5/SHA) | Optional (DES/AES) | Current standard; use `authPriv` mode for both authentication and encryption |

```text
Poller ---(GET request: OID 1.3.6.1.2.1.2.2.1.10.1, "ifInOctets" for interface 1)--> Device
Device ---(response: 4839201823)-----------------------------------------------------> Poller
```

Polling-based SNMP scales adequately for moderate device counts and polling
intervals (commonly 60–300 seconds), but has known limitations: it cannot
report a metric faster than the polling interval, and its pull-based model
places query load on every device polled — considerations that motivated
the push-based, model-driven streaming telemetry model discussed below.

### Syslog: Centralized Logging Architecture

Syslog, standardized in [RFC 5424](https://www.rfc-editor.org/rfc/rfc5424), transports log messages from a device
(the sender) to a centralized collector, tagged with a **facility** (the
subsystem generating the message — kernel, local application, and so on)
and a **severity**:

| Severity | Level | Example |
| --- | --- | --- |
| 0 | Emergency | System unusable |
| 1 | Alert | Immediate action required |
| 2 | Critical | Critical condition |
| 3 | Error | Error condition |
| 4 | Warning | Warning condition |
| 5 | Notice | Normal but significant condition |
| 6 | Informational | Informational message |
| 7 | Debug | Debug-level detail |

Syslog is most commonly transported over UDP, which is fast and simple but
provides no delivery guarantee — a collector outage or network congestion
silently drops messages with no retransmission. [RFC 5425](https://www.rfc-editor.org/rfc/rfc5425) defines syslog
over TLS for both confidentiality and reliable, connection-oriented
delivery, which enterprises increasingly require for security-relevant log
sources. Centralizing logs from every network device onto one (or a
redundant pair of) collector gives operations a single place to search
across devices during an incident — impossible when logs remain scattered
across each device's local buffer, which typically wraps and overwrites
after a short period.

### Flow-Based Telemetry: NetFlow, IPFIX, and sFlow

Flow telemetry summarizes traffic as **flow records** — one record per
conversation (source/destination IP, ports, protocol, byte/packet counts,
timestamps) — instead of exporting full packet captures, which do not scale
to continuous, always-on collection.

| Technology | Origin | Export Model | Notes |
| --- | --- | --- | --- |
| NetFlow (v5/v9) | Cisco-originated | Device exports flow records after flow expiration or timeout | v9 introduced flexible, template-based fields |
| IPFIX | IETF standardization of NetFlow v9's model ([RFC 7011](https://www.rfc-editor.org/rfc/rfc7011)) | Same template-based export model | Vendor-neutral standard; the modern default to design for |
| sFlow | Independent standard, packet-sampled | Exports a statistical sample of packets (e.g., 1-in-1000) plus interface counters | Lower device overhead than full flow accounting; statistical rather than exact |

Flow data answers "who talked to whom, how much, and when" — invaluable
for capacity planning, unexpected-traffic investigation, and confirming
that traffic actually follows the path a design ([Chapter 7](07-enterprise-network-design-and-resilience.md)) intended,
without the storage and processing cost of full packet capture.

### Model-Driven Streaming Telemetry

Where SNMP polls a fixed OID tree on an interval, modern streaming
telemetry inverts the model: a device continuously pushes state changes to
a collector as they happen, structured against a YANG data model (the same
modeling language used by NETCONF/RESTCONF configuration management) rather
than SNMP's separate MIB hierarchy. **gNMI** (gRPC Network Management
Interface) is the common transport for this pattern, supporting both a
collector-initiated subscription ("dial-in") and a device-initiated push to
a configured collector ("dial-out"). The practical advantage over SNMP
polling is latency and efficiency: a state change is reported as it occurs
rather than waiting up to a full polling interval, and only changed data
needs to be transmitted rather than a full periodic sweep.

### Establishing a Network Baseline

A baseline is a recorded profile of *normal* — typical interface
utilization by time of day, typical route table size, typical CPU load,
typical flow volume between known endpoint pairs — captured over a
representative period (commonly at least one full business cycle,
including peak periods). Without a baseline, "is this value abnormal"
cannot actually be answered; a threshold-based alert set from a guess
("alert if interface utilization exceeds 80%") on a link whose normal peak
is 85% either fires constantly and gets ignored, or a link whose normal
peak is 20% gets no warning until utilization has already tripled.
Baselines are re-established after any significant topology or capacity
change, since the previous "normal" is no longer a valid comparison point.

## Design Considerations

- **Choose the right telemetry source for the question, not a single
  universal tool.** SNMP/streaming telemetry answers device-state
  questions; flow data answers traffic-pattern questions; syslog answers
  event/condition questions; no single source answers all three well.
- **Scale collector infrastructure and retention to the actual data
  volume**, particularly for flow and streaming telemetry, which produce
  orders of magnitude more data than SNMP polling or syslog — undersized
  collector storage silently truncates the retention window an incident
  investigation may need.
- **Design alerting around correlated conditions, not single metrics in
  isolation**, to control alert fatigue: an interface utilization spike
  correlated with a known maintenance window is informational; the same
  spike correlated with an unexpected BGP session flap is actionable.
  Alerting on every raw threshold crossing independently produces a volume
  of noise that trains operators to ignore alerts.
- **Place collectors and pollers with redundancy and independent power/path
  where the network being monitored could itself be the thing that fails**
  — a monitoring system that shares fate with the infrastructure it
  monitors cannot alert on that infrastructure's own outage.
- **Decide push (streaming telemetry) vs. pull (SNMP polling) based on
  latency requirements and device support**, not habit; SNMP polling
  remains adequate and simpler to operate for many device classes, while
  streaming telemetry matters most where sub-second detection of state
  change is operationally significant.
- **Re-baseline after every significant change**, and record the baseline
  itself as a version-controlled artifact (consistent with the docs-as-code
  approach established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md)) rather than tribal knowledge held by
  one engineer.

## Implementation and Automation

### Enabling SNMPv3 and Syslog (Vendor-Neutral Pseudo-CLI)

```text
device(config)# snmp-server group MONITORS v3 priv
device(config)# snmp-server user netmon MONITORS v3 auth sha <AUTH_KEY> priv aes 128 <PRIV_KEY>
device(config)# snmp-server host 10.10.2.10 version 3 priv netmon

device(config)# logging host 10.10.2.11 transport tcp port 6514 tls
device(config)# logging trap warning
device(config)# logging source-interface loopback0
```

### Enabling IPFIX Export (Vendor-Neutral Pseudo-CLI)

```text
device(config)# flow exporter LAB-EXPORTER
device(config-flow-exporter)# destination 10.10.2.12
device(config-flow-exporter)# transport udp 4739
device(config-flow-exporter)# export-protocol ipfix

device(config)# flow monitor LAB-MONITOR
device(config-flow-monitor)# exporter LAB-EXPORTER
device(config)# interface gigabitethernet0/1
device(config-if)# ip flow monitor LAB-MONITOR input
```

### Querying SNMP Programmatically

```python
from pysnmp.hlapi import (
    getCmd, SnmpEngine, UsmUserData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity, usmAesCfb128Protocol, usmHMACSHAAuthProtocol,
)

iterator = getCmd(
    SnmpEngine(),
    UsmUserData("netmon", "authKeyPlaceholder", "privKeyPlaceholder",
                authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb128Protocol),
    UdpTransportTarget(("10.10.5.1", 161)),
    ContextData(),
    ObjectType(ObjectIdentity("IF-MIB", "ifInOctets", 1)),
)
errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
if not errorIndication and not errorStatus:
    for varBind in varBinds:
        print(" = ".join(str(x) for x in varBind))
```

### Compliance-Style Monitoring Validation with Ansible

```yaml
- name: Confirm monitoring configuration is present on all devices
  hosts: all_network_devices
  tasks:
    - name: Gather running configuration
      network.device.command:
        commands: "show running-config | include logging|snmp-server"
      register: config_output

    - name: Assert centralized syslog host is configured
      ansible.builtin.assert:
        that:
          - "'logging host 10.10.2.11' in config_output.stdout[0]"
        fail_msg: "Device is missing the centralized syslog destination."
```

Configuration for monitoring itself should be managed and validated the
same way as any other network configuration — drift in monitoring
configuration (a device silently missing its syslog or SNMP destination)
is a blind spot that is only discovered during an incident unless it is
actively checked for, as this playbook does.

## Validation and Troubleshooting

```bash
# Confirm a device answers SNMP before assuming a monitoring platform issue
snmpget -v3 -u netmon -l authPriv -a SHA -A <AUTH_KEY> -x AES -X <PRIV_KEY> \
  10.10.5.1 1.3.6.1.2.1.1.3.0

# Confirm syslog reachability from the collector's perspective
sudo tcpdump -i eth0 -nn 'host 10.10.5.1 and port 6514'

# Confirm flow export is actually arriving at the collector
sudo tcpdump -i eth0 -nn 'udp port 4739'
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Monitoring platform shows a device as down, but it responds to `ping` | SNMP community string/user mismatch, ACL blocking SNMP, or trap destination misconfigured | `snmpget` directly from the poller; check device SNMP ACL |
| Logs from a device stop appearing with no error | Collector reachability lost (often over UDP, silently) or device logging configuration removed by an untracked change | Confirm reachability with a packet capture at the collector; diff current config against the intended baseline |
| Two devices' logs appear out of order for the same event | Clock skew between devices | Cross-reference against [Chapter 5](05-core-network-services.md)'s `chronyc tracking` on both devices |
| Flow collector shows a large, unexplained traffic spike | Could be a genuine incident, a legitimate but unannounced bulk transfer, or a monitoring artifact (e.g., a sampling/export misconfiguration) | Compare against the established baseline before treating as an incident |
| Alert volume is high enough that real incidents get missed | Thresholds set without a baseline, or alerts not correlated before paging | Re-baseline the metric; implement correlation/deduplication logic |
| Streaming telemetry subscription silently stops updating | gNMI session dropped without automatic resubscription, or device resource limit hit | Check collector logs for subscription state; confirm device telemetry process health |

The clock-skew symptom above is a direct, practical consequence of
[Chapter 5](05-core-network-services.md)'s point that accurate time is a prerequisite for troubleshooting:
without synchronized clocks, "what happened first" during a multi-device
incident cannot be reliably determined from logs alone.

## Security and Best Practices

- **Use SNMPv3 with `authPriv`**, never SNMPv1/v2c community strings, on
  any network reachable outside a tightly controlled management segment —
  a cleartext community string observed on the wire grants read (and, if
  misconfigured, write) access to device state.
- **Transport syslog over TLS ([RFC 5425](https://www.rfc-editor.org/rfc/rfc5425))** for security-relevant log
  sources, both to protect log content in transit and to gain reliable,
  connection-oriented delivery that plain UDP syslog cannot provide.
- **Restrict management-plane access to monitoring infrastructure itself**
  with the same rigor as any other management-plane control — a compromised
  monitoring collector or poller often has broad read access (and
  sometimes write access, via SNMP `authPriv` or an automation credential)
  across the entire managed fleet.
- **Treat flow and packet-capture data as potentially sensitive**,
  consistent with [Chapter 1](01-network-models-and-protocol-architecture.md)'s guidance — flow records reveal traffic
  patterns and communicating parties even without payload, which is itself
  sensitive operational and sometimes regulated information.
- **Alert on monitoring infrastructure health itself**, not only on the
  infrastructure it observes; a silently failed collector or poller
  produces a false sense of security that is worse than no monitoring at
  all, because its absence of alerts is indistinguishable from genuine
  health.

## References and Knowledge Checks

**References**

- [RFC 3411 — An Architecture for Describing SNMP Management Frameworks](https://www.rfc-editor.org/rfc/rfc3411)
- [RFC 3414 — User-based Security Model (USM) for SNMPv3](https://www.rfc-editor.org/rfc/rfc3414)
- [RFC 5424 — The Syslog Protocol](https://www.rfc-editor.org/rfc/rfc5424)
- [RFC 5425 — TLS Transport Mapping for Syslog](https://www.rfc-editor.org/rfc/rfc5425)
- [RFC 7011 — Specification of the IP Flow Information Export (IPFIX) Protocol](https://www.rfc-editor.org/rfc/rfc7011)
- [OpenConfig / gNMI Specification](https://github.com/openconfig/reference/tree/master/rpc/gnmi)

**Knowledge Checks**

1. Explain the difference between monitoring and observability using an
   example of a question each can and cannot answer.
2. Why is SNMPv2c considered insecure for use outside a tightly controlled
   management network, specifically?
3. What problem does a network baseline solve that a fixed, guessed
   alert threshold does not?
4. Compare NetFlow/IPFIX and sFlow's export models, and explain when
   sFlow's sampling approach is an acceptable trade-off.
5. Why does UDP-transported syslog risk silent message loss, and what does
   [RFC 5425](https://www.rfc-editor.org/rfc/rfc5425) change about that?
6. A multi-device incident's log timeline does not match the order
   engineers believe events actually occurred in. What should be checked
   first, and why?

## Hands-On Lab

**Objective.** Build a minimal [RFC 5424](https://www.rfc-editor.org/rfc/rfc5424) syslog receiver, generate tagged
log messages at varying severities, and implement a simple alert
correlation rule — demonstrating the centralized logging and alert-fatigue
concepts from this chapter end to end.

**Prerequisites**

- A Linux host with `python3` (standard library only — no external
  packages required).
- The `logger` utility (part of `util-linux`/`bsdutils`, present on
  virtually all Linux distributions) with [RFC 5424](https://www.rfc-editor.org/rfc/rfc5424) and UDP support.
  Confirm support first:

  ```bash
  logger --help 2>&1 | grep -E "rfc5424|udp" || echo "Fallback sender required — see step 2 note."
  ```

**Lab Steps**

1. Write a minimal UDP syslog receiver that parses the [RFC 5424](https://www.rfc-editor.org/rfc/rfc5424) PRI field
   (facility/severity) and prints a human-readable summary:

   ```bash
   cat <<'PYEOF' > /tmp/syslog_receiver.py
   import re
   import socket
   import sys
   from datetime import datetime

   SEVERITY_NAMES = ["Emergency", "Alert", "Critical", "Error",
                      "Warning", "Notice", "Informational", "Debug"]

   PRI_RE = re.compile(r"^<(\d+)>")

   def parse(message: str):
       match = PRI_RE.match(message)
       if not match:
           return None
       pri = int(match.group(1))
       facility, severity = divmod(pri, 8)
       return facility, severity, message[match.end():].strip()

   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind(("127.0.0.1", 1514))
   print("Syslog receiver listening on 127.0.0.1:1514 (Ctrl+C to stop)")

   recent_errors = []
   while True:
       data, _ = sock.recvfrom(4096)
       text = data.decode(errors="replace")
       parsed = parse(text)
       now = datetime.now()
       if parsed is None:
           print(f"[UNPARSEABLE] raw message: {text!r}")
           continue
       facility, severity, body = parsed
       sev_name = SEVERITY_NAMES[severity] if severity < 8 else "Unknown"
       print(f"[{sev_name}] facility={facility} :: {body}")
       if severity <= 3:  # Error or more severe
           recent_errors.append(now)
           recent_errors[:] = [t for t in recent_errors if (now - t).total_seconds() <= 10]
           if len(recent_errors) >= 3:
               print(f"  !! ALERT: {len(recent_errors)} error-or-higher messages within 10 seconds")
   PYEOF
   python3 /tmp/syslog_receiver.py &
   RECEIVER_PID=$!
   sleep 1
   ```

2. Send a single tagged message and confirm the receiver decodes severity
   and facility correctly:

   ```bash
   logger -n 127.0.0.1 -P 1514 -d --rfc5424 -p local0.warning "lab: interface Gi0/1 flapping"
   sleep 1
   ```

   If `logger` does not support `--rfc5424`/`-d` on this system, use the
   fallback sender instead:

   ```bash
   python3 -c "
   import socket
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.sendto(b'<132>lab: interface Gi0/1 flapping', ('127.0.0.1', 1514))
   "
   ```

   **Expected result:** the receiver prints `[Warning] facility=16 ::
   lab: interface Gi0/1 flapping` — facility 16 is `local0`, severity 4 is
   `Warning`, matching the severity table in this chapter's theory section.

3. Generate a burst of three error-severity messages within a few seconds
   to trigger the correlation rule implemented in the receiver:

   ```bash
   for i in 1 2 3; do
     logger -n 127.0.0.1 -P 1514 -d --rfc5424 -p local0.err "lab: BGP neighbor $i down" \
       || python3 -c "import socket; socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'<131>lab: BGP neighbor $i down', ('127.0.0.1', 1514))"
     sleep 1
   done
   ```

   **Expected result:** after the third message, the receiver prints an
   `ALERT` line — demonstrating, in miniature, the correlation-over-raw-
   threshold alerting principle from the Design Considerations section:
   one error is noted individually, but three within ten seconds triggers a
   distinct, actionable alert.

**Negative Test**

Send a deliberately malformed message with no valid PRI field and confirm
the receiver flags it rather than crashing:

```bash
python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'this is not a valid syslog message', ('127.0.0.1', 1514))
"
sleep 1
```

**Expected result:** the receiver prints `[UNPARSEABLE] raw message: ...`
and continues running rather than throwing an unhandled exception —
demonstrating why production log pipelines need defensive parsing:
malformed or non-conforming messages are a routine occurrence, not an edge
case, and a pipeline that crashes on one loses every subsequent message
until restarted.

**Cleanup**

```bash
kill "$RECEIVER_PID" 2>/dev/null || true
rm -f /tmp/syslog_receiver.py
```

## Summary and Completion Checklist

This chapter distinguished monitoring, observability, and validation, and
covered the four primary telemetry sources an enterprise network relies on:
SNMP polling, centralized syslog, flow-based telemetry, and model-driven
streaming telemetry — along with why a recorded baseline is what makes any
of that data interpretable as normal or abnormal. The hands-on lab built a
working syslog pipeline from scratch, including a simple but genuine
alert-correlation rule, and confirmed defensive handling of malformed
input — the same operational instrumentation this chapter's theory
describes, built rather than merely read about.

**Completion Checklist**

- [ ] Can distinguish monitoring, observability, and validation with an
      example question each answers.
- [ ] Can explain SNMP's MIB/OID model and why SNMPv3 `authPriv` is
      required over v1/v2c.
- [ ] Can explain syslog severity levels and the reliability trade-off of
      UDP vs. TLS transport.
- [ ] Can compare NetFlow/IPFIX and sFlow's export models.
- [ ] Understands why a network baseline is required before threshold-based
      alerting is meaningful.
- [ ] Built a working syslog receiver, validated severity/facility parsing,
      and implemented a basic alert-correlation rule.
