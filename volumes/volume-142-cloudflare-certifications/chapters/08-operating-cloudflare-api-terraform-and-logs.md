# Chapter 08: Operating Cloudflare — API, Terraform, and Logs

## Learning Objectives

- Manage zones and Zero Trust configuration as code with the API and Terraform provider.
- Detect and resolve drift between intended and live configuration.
- Get security and traffic logs out of the edge and into your analysis stack.
- Monitor the moving parts you now depend on — tunnels above all.

*Exam relevance: operational threads from both exams — configuration hygiene underlies every Application Security control in Chapters 03–04, and tunnel/client health underlies everything in Chapters 05–06.*

## Configuration as code

Everything the dashboard does, the **API** does, and the official **Terraform provider** wraps: DNS records, WAF custom rules, rate limits, Access applications and policies, tunnels, Workers routes. The argument was made in [Volume CXLI's fixtures chapter](../../volume-141-newrelic-certifications/chapters/08-service-levels-and-automation.md) and transfers whole — click-built configuration drifts, cannot be reviewed, and cannot be reproduced.

It lands harder here for one reason: **this configuration is security enforcement.** A drifted dashboard is a wrong chart; a drifted WAF rule, Access policy, or DNS record is an open door. The v1.2.155-class incident for a Cloudflare estate is someone "temporarily" loosening a rule mid-incident and the loosening becoming permanent because nothing diffed it.

Two practices carry the weight:

1. **The audit trail is your friend.** Cloudflare logs configuration changes with actor and timestamp; alert on changes to security-critical objects that did not come from the pipeline's service token.
2. **Drift detection on a schedule.** `terraform plan` in a cron job, alerting on non-empty diffs, is the entire mechanism. Lab 8.1 models the findings a first run typically produces.

## Logs out of the edge

The edge sees every request; the question is where that evidence goes. Options scale with plan and need — from the dashboard's analytics, through **Logpush** delivering request/firewall/Access/Gateway logs to your storage (R2, S3, a SIEM), to instant tailing for live debugging.

The design decision is the one [Volume XLV (Splunk)](../../volume-045-splunk-certifications/README.md) and [Volume LXXXVI (Elastic)](../../volume-086-elastic-certifications/README.md) exist for: the edge is a *source*, your SIEM is the *destination*, and the WAF events from Chapter 03's log-mode rollout are only measurable if they actually land somewhere queryable. A protection you cannot measure is a protection you cannot tune — the whole log-first ladder assumes the logs arrive.

## Monitoring the new dependencies

Chapter 06 traded open inbound ports for tunnel daemons, and the trade included a monitoring obligation:

| Component | Failure looks like | Watch |
|:---|:---|:---|
| **Tunnel (`cloudflared`)** | The app behind it is *down* — cleanly, totally | Tunnel health/heartbeat; run replicas |
| **WARP client fleet** | Users lose posture signals → lose posture-gated apps | Enrollment coverage, client version health |
| **Service tokens** | Expiry = automation suddenly 403s | Expiry dates, on a calendar |
| **Certificates (universal/origin)** | Renewal failure = TLS errors edge-wide | Expiry and renewal status |

The tunnel row is the one that pages you: a single-replica tunnel is a single point of failure for everything published through it, which is why `cloudflared` runs with replicas and why its heartbeat belongs in the same alerting estate as the applications it fronts.

## Hands-On Lab

Python models operations. **Cost:** none.

### Lab 8.1 — Drift detection on security configuration

**Objective:** Diff intended against live, and read each finding as a risk.

```bash
python3 - <<'EOF'
INTENDED = {
  "dns:www":                {"proxied": True},
  "dns:staging":            {"proxied": True},
  "waf:sqli-managed":       {"action": "block"},
  "waf:anomaly-managed":    {"action": "challenge"},
  "ratelimit:/login":       {"threshold": 12, "key": "ip+username"},
  "access:finance":         {"require": "finance-team+managed+hardware-key"},
  "tunnel:erp":             {"replicas": 2},
}
LIVE = {
  "dns:www":                {"proxied": True},
  "dns:staging":            {"proxied": False},                          # <- flipped during "testing"
  "waf:sqli-managed":       {"action": "block"},
  "waf:anomaly-managed":    {"action": "log"},                           # <- loosened mid-incident
  "ratelimit:/login":       {"threshold": 500, "key": "ip"},             # <- raised for a load test
  "access:finance":         {"require": "finance-team+managed+hardware-key"},
  "tunnel:erp":             {"replicas": 1},                             # <- second replica never restored
  "waf:tmp-allow-vendor":   {"action": "allow", "expr": "ip 198.51.100.9"},  # <- unmanaged
}
RISK = {
  "dns:staging":          "ORIGIN EXPOSED — the Chapter 02 leak, reintroduced by hand",
  "waf:anomaly-managed":  "protection silently reduced to observation",
  "ratelimit:/login":     "credential-stuffing limit 40x looser, actor key discarded",
  "tunnel:erp":           "single point of failure for everything behind it",
  "waf:tmp-allow-vendor": "unmanaged ALLOW — an inspection hole with no owner",
}
print("terraform plan (conceptually):\n")
findings = 0
for k in sorted(set(INTENDED) | set(LIVE)):
    i, l = INTENDED.get(k), LIVE.get(k)
    if i == l: continue
    findings += 1
    kind = "UNMANAGED" if i is None else ("MISSING" if l is None else "DRIFTED")
    print(f"  {kind:10} {k}")
    if i and l:
        for f in i:
            if i[f] != l[f]: print(f"             {f}: intended {i[f]!r}, live {l[f]!r}")
    print(f"             risk: {RISK.get(k, '-')}")
print(f"\n{findings} findings, every one a hand edit that made sense in a moment and")
print("was never reverted. None of them errored; none of them alerted; all of them")
print("are security posture, not preference.")
print("\nApply the code and all five heal at once. The deeper fix is the loop:")
print("   scheduled plan -> alert on non-empty diff -> the hand edit is discovered")
print("   in HOURS (as a finding) instead of MONTHS (as an incident).")
EOF
```

**Expected result:** Five findings — a re-exposed origin, a silently observational WAF rule, a 40x-loosened login limit, a de-redundant tunnel, and an ownerless allow. Each traces to a reasonable moment; the loop at the end is the operational content, because discovery latency is the difference between a finding and an incident report.

**Negative test:** Running the drift check only after incidents. That converts it from prevention into archaeology — accurate, and late.

**Cleanup:** None.

### Lab 8.2 — Are the logs actually arriving?

**Objective:** Monitor the pipeline that everything else's measurability depends on.

```bash
python3 - <<'EOF'
from datetime import datetime, timedelta
now = datetime(2026, 8, 4, 21, 0)
JOBS = [
  # logpush job,          destination,     last_delivery,          expected_interval_min
  ("http_requests",       "r2://logs",     now - timedelta(minutes=4),   5),
  ("firewall_events",     "siem://main",   now - timedelta(minutes=3),   5),
  ("access_requests",     "siem://main",   now - timedelta(hours=26),    5),
  ("gateway_dns",         "r2://logs",     now - timedelta(minutes=2),   5),
]
print(f"{'job':18}{'destination':>14}{'last delivery':>16}{'status'}")
for job, dest, last, interval in JOBS:
    age = (now - last).total_seconds() / 60
    if age <= interval * 3: s = "   healthy"
    else: s = f"   *** SILENT for {age/60:.0f}h — investigate the JOB, not just the source"
    print(f"{job:18}{dest:>14}{f'{age:.0f}m ago':>16}{s}")

print("\naccess_requests has delivered nothing for 26 hours. Two very different")
print("explanations, indistinguishable from the dashboard:")
print("   1. nobody used any Access app for 26 hours (possible on a holiday)")
print("   2. the logpush job broke (credential expiry, destination full, config)")
print("\nThe monitoring rule from Vol CXLI's collection chapter, verbatim:")
print("SILENCE FROM A TELEMETRY PIPELINE IS INDISTINGUISHABLE FROM A QUIET SYSTEM.")
print("Alert on delivery-job health (last success age), not only on log contents —")
print("and remember what is downstream: the Chapter 03 log-mode measurements, the")
print("SIEM detections, and the incident timeline you will want NEXT month are all")
print("silently incomplete for as long as that job is down.")
EOF
```

**Expected result:** Three healthy jobs and one 26 hours silent, with the ambiguity stated: quiet system and broken pipeline look identical from below. The downstream inventory is why this is a page and not a ticket — every measurement this volume has built assumes the logs land, and a dead delivery job invalidates them retroactively and invisibly.

**Negative test:** Alerting only on what the logs contain. A dead pipeline produces no logs, hence no alerts, hence green dashboards over a 26-hour evidence gap.

**Cleanup:** None.

### Lab 8.3 — The tunnel is infrastructure now

**Objective:** Treat `cloudflared` with the seriousness of the apps behind it.

```bash
python3 - <<'EOF'
TUNNELS = [
  # tunnel,        replicas, hosts,                    apps_behind, heartbeat_alert
  ("prod-web",     3,        ["web-1","web-2","web-3"], 4,          True),
  ("erp",          1,        ["erp-host"],              1,          False),
  ("internal-ops", 2,        ["ops-1","ops-2"],         6,          True),
]
print(f"{'tunnel':14}{'replicas':>9}{'apps behind':>13}{'heartbeat alert':>17}   assessment")
for name, reps, hosts, apps, hb in TUNNELS:
    problems = []
    if reps < 2: problems.append("SINGLE REPLICA — one daemon restart = total outage for what it fronts")
    if not hb:   problems.append("no heartbeat alert — the outage announces itself via users")
    if len(set(hosts)) < reps: problems.append("replicas share a host — redundancy in name only")
    print(f"{name:14}{reps:>9}{apps:>13}{'yes' if hb else 'NO':>17}   {'; '.join(problems) or 'healthy'}")

print("\nThe erp tunnel fails both checks at once — and note what it fronts: the one")
print("application whose outage generates an executive email. The pattern is common")
print("because tunnels get set up in migration order (Chapter 06's lab), and the")
print("legacy app migrated last inherits the least-finished operational setup.")
print("\nThe checklist per tunnel: >=2 replicas, on DIFFERENT hosts, heartbeat")
print("alerting wired to the same channel as the apps behind it. Chapter 06 said")
print("the trade was good, not free. This is the fee, and it is small — pay it.")
EOF
```

**Expected result:** Two tunnels healthy and the ERP tunnel failing every check while fronting the least-tolerable outage. The migration-order observation explains how this happens without negligence — last-migrated apps inherit least-finished operations — and the three-item checklist is the whole fee for Chapter 06's trade.

**Negative test:** Running a second replica on the same host as the first. Host reboot takes both; the redundancy existed only in the replica count.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Zones, WAF, and Zero Trust configuration managed as code, with scheduled drift detection.
- [ ] Configuration changes audited; out-of-pipeline edits alerting.
- [ ] Log delivery monitored by job health, not only content.
- [ ] Tunnels run redundantly across hosts, with heartbeats in the paging path.
