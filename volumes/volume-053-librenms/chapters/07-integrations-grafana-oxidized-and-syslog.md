# Chapter 07: Integrations — Grafana, Oxidized, and Syslog

## Learning Objectives

- Visualize LibreNMS data in Grafana.
- Back up device configs with Oxidized.
- Ingest syslog and SNMP traps.
- Sync device inventory with NetBox.
- Complete a walkthrough for each integration.

## Theory and Architecture

LibreNMS integrates with the wider ops ecosystem. **Grafana** reads LibreNMS metrics
(via the datasource/plugin or a shared time-series backend) for advanced dashboards.
**Oxidized** is a config-backup tool LibreNMS drives — pulling and versioning device
configs, surfaced in the UI. **Syslog** and **SNMP traps** feed event data into
LibreNMS (`syslog-ng`/`snmptrapd` → LibreNMS). And **NetBox** (Volume LII) can be the
source of truth that seeds LibreNMS device inventory.

## Design Considerations

Use **Grafana** when you outgrow built-in dashboards, **Oxidized** to add config
backup/diff to monitoring, **syslog/traps** to correlate events with metrics, and
**NetBox** as the authoritative device list feeding LibreNMS. Each integration keeps its
own tool doing what it does best.

## Implementation and Automation

The labs describe/configure Grafana, Oxidized, syslog, and a NetBox sync.

## Validation and Troubleshooting

Confirm the integrations:

```text
Grafana: dashboards over LibreNMS metrics. Oxidized: config backup/diff in the UI.
Syslog/traps: syslog-ng/snmptrapd -> LibreNMS events. NetBox: source of truth -> device list.
```

Common pitfalls: duplicating dashboards in two tools; and Oxidized without device
credentials (no backups).

## Security and Best Practices

Secure the **Grafana** datasource, store **Oxidized** device credentials safely, filter
and rate-limit **syslog/traps**, and let **NetBox** own the device list so both tools
agree. Keep integration credentials least-privilege.

## Hands-On Lab

Integration walkthroughs. **Shared prerequisites** — a running LibreNMS; optional
Grafana/Oxidized/NetBox. **Cost:** none.

### Lab 7.1 — Grafana dashboard over LibreNMS

**Objective:** Describe wiring Grafana to LibreNMS data.

```text
# Grafana: add the LibreNMS data source (or the shared TS backend), then a panel:
#   query device port in/out rates -> time-series panel.
"grafana panel: LibreNMS port rates over 24h"
```

**Expected result:** a Grafana panel rendering LibreNMS metrics — advanced
visualization beyond built-in graphs.

**Negative test:** rebuild every graph in both tools; **Grafana** reads the same data —
avoid duplication.

**Cleanup:** remove the panel if it was for the lab.

### Lab 7.2 — Oxidized config backup

**Objective:** Enable Oxidized-backed config backup.

```text
# config.php: $config['oxidized']['enabled'] = true; url = 'http://oxidized:8888';
# Oxidized pulls device configs on a schedule; LibreNMS shows config + diffs per device.
"oxidized enabled -> device 'Config' tab shows current config + version diffs"
```

**Expected result:** device **config backups with diffs** in the LibreNMS UI — monitoring
plus config history.

**Negative test:** rely on manual config saves; **Oxidized** versions them automatically
— enable it.

**Cleanup:** disable Oxidized if it was for the lab.

### Lab 7.3 — Ingest syslog

**Objective:** Route device syslog into LibreNMS.

```text
# Point devices' syslog at the LibreNMS host; syslog-ng writes to the LibreNMS DB.
# Verify in the UI: device > Logs > Syslog shows incoming messages.
logging host <librenms-ip>       # example device config line
```

**Expected result:** device syslog messages appearing under the device's **Syslog** —
event correlation with metrics.

**Negative test:** troubleshoot from metrics alone; **syslog** adds the device's own
event narrative — ingest it.

**Cleanup:** remove the logging host line if it was for the lab.

### Lab 7.4 — Seed inventory from NetBox

**Objective:** Add LibreNMS devices from NetBox data.

```bash
# Pull devices from NetBox (Volume LII) and add each to LibreNMS:
# for host in $(pynetbox devices with primary_ip): POST /api/v0/devices
echo "sync: NetBox devices -> LibreNMS (source of truth drives monitoring inventory)"
```

**Expected result:** LibreNMS device list **sourced from NetBox** — intended state
driving monitoring.

**Negative test:** maintain two device lists by hand; let the **source of truth** feed
LibreNMS to keep them aligned.

**Cleanup:** remove any devices added for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

LibreNMS integrates with Grafana (advanced dashboards), Oxidized (config backup/diff),
syslog/traps (event correlation), and NetBox (source of truth for inventory). This
chapter wired each integration conceptually and by config.

- [ ] I can visualize LibreNMS data in Grafana.
- [ ] I can enable Oxidized config backup.
- [ ] I can ingest syslog for event correlation.
- [ ] I can seed inventory from NetBox.
- [ ] I completed Labs 7.1–7.4 including each negative test.
