# Chapter 02: Adding and Discovering Devices

## Learning Objectives

- Configure SNMP so LibreNMS can monitor a device.
- Add a device via the CLI and the API.
- Run and understand auto-discovery.
- Group devices dynamically for scale.
- Complete a walkthrough for each onboarding step.

## Theory and Architecture

Monitoring starts by **adding a device** with its SNMP credentials; LibreNMS then runs
**discovery** to learn what the device exposes — interfaces, sensors, VLANs, neighbors
(via LLDP/CDP), OS, and modules — and the **poller** begins collecting metrics.
**Device groups** classify devices by dynamic rules (e.g., OS, type, location) so
alerting and views scale without manual tagging.

## Design Considerations

Standardize **SNMPv3** credentials so onboarding is uniform. Let **discovery** populate
the model (don't hand-enter interfaces). Use **dynamic device groups** so a new switch
automatically joins the right alerting scope.

## Implementation and Automation

The labs use `snmpget`, the `lnms` CLI, the REST API, and discovery to onboard a device
and group it.

## Validation and Troubleshooting

Confirm the flow:

```text
Device (SNMP creds) -> discovery (interfaces/sensors/neighbors/OS) -> poller (metrics).
Device groups: dynamic rules classify devices for alerting/views.
```

Common pitfalls: wrong SNMP community/creds (device unreachable); and static grouping
that misses new devices.

## Security and Best Practices

Prefer **SNMPv3** with auth+priv, restrict SNMP with device ACLs, verify reachability
with `snmpget` before adding, and use **dynamic groups** so classification stays
current. Feed device lists from a source of truth where possible.

## Hands-On Lab

Onboarding walkthroughs. **Shared prerequisites** — a running LibreNMS (`$LNMS`,
`$TOKEN`); a reachable SNMP device (or the LibreNMS host itself with snmpd). **Cost:**
none.

### Lab 2.1 — Verify SNMP reachability

**Objective:** Confirm SNMP responds before adding.

```bash
snmpget -v2c -c public 127.0.0.1 sysName.0
# or SNMPv3: snmpget -v3 -l authPriv -u user -a SHA -A authpass -x AES -X privpass 127.0.0.1 sysName.0
```

**Expected result:** the device's **sysName** — proof SNMP is reachable and the creds
work.

**Negative test:** add a device whose SNMP is unreachable; discovery fails — **test
with `snmpget` first**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Add a device (CLI)

**Objective:** Add a device with `lnms`.

```bash
docker compose exec librenms lnms device:add 127.0.0.1 \
  --v2c --community public
docker compose exec librenms lnms device:list | head
```

**Expected result:** the device added and listed — onboarding via CLI.

**Negative test:** add the same device twice; LibreNMS rejects the **duplicate** by
hostname/IP.

**Rollback:** `lnms device:remove 127.0.0.1`.

### Lab 2.3 — Add a device (API) and discover

**Objective:** Add via the API and trigger discovery.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -X POST "$LNMS/api/v0/devices" \
  -d '{"hostname":"127.0.0.1","version":"v2c","community":"public"}' \
  | python3 -c "import sys,json;print('status:',json.load(sys.stdin).get('status'))"
docker compose exec librenms lnms device:poll 127.0.0.1
```

**Expected result:** an **ok** status and a poll run — programmatic onboarding plus
discovery/poll.

**Negative test:** rely on the next cron cycle for urgent data; **trigger discovery/
poll** manually to see results now.

**Rollback:** delete the device via the API.

### Lab 2.4 — Create a dynamic device group

**Objective:** Group devices by a rule.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -X POST "$LNMS/api/v0/devicegroups" \
  -d '{"name":"linux","type":"dynamic","rules":{"condition":"AND","rules":[{"field":"devices.os","operator":"equal","value":"linux"}]}}'
```

**Expected result:** a **dynamic group "linux"** that auto-includes matching devices —
scalable classification.

**Negative test:** hand-add devices to a static group; a **dynamic rule** self-populates
as devices are discovered.

**Rollback:** delete the device group.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Onboarding is: configure SNMP, verify reachability, add the device (CLI or API), let
discovery learn its capabilities, and group it dynamically. This chapter onboarded a
device both ways and built a dynamic group.

- [ ] I can verify SNMP with `snmpget`.
- [ ] I can add a device via CLI and API.
- [ ] I can trigger discovery/poll on demand.
- [ ] I can build dynamic device groups.
- [ ] I completed Labs 2.1–2.4 including each negative test.
