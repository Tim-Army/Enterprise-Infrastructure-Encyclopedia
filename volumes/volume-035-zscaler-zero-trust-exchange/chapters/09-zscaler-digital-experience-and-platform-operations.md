# Chapter 09: Zscaler Digital Experience (ZDX) and Platform Operations

## Learning Objectives

- Explain **Zscaler Digital Experience (ZDX)** as end-to-end monitoring of user
  experience across device, network, and application — the basis of the ZDXA
  certification.
- Describe the **ZDX Score** and the probe types (web/application, Cloud Path,
  device health) that feed it.
- Use **Cloud Path** and **deep tracing** to localize a problem to device,
  network, or application.
- Operate the platform: admin roles, log streaming (NSS/LSS), and API/Terraform
  automation.
- Validate a ZDX investigation and reason about score changes.

## Theory and Architecture

The first eight chapters secured and forwarded traffic. ZDX answers the
operational question that follows: *when a user says "the app is slow," where is
the problem?* Because Zscaler is already inline for every session, ZDX measures
the whole path — the endpoint, the network hop-by-hop, and the application
response — and scores it, so support can localize an issue instead of guessing.

### The ZDX Score and probes

The **ZDX Score** (0–100) summarizes experience for a user, application, or
location, blending signals from:

- **Web/application probes** — synthetic measurements of an app's availability
  and response time (page fetch, DNS, server response).
- **Cloud Path** — a hop-by-hop path trace (latency and loss per hop) from the
  endpoint through the network to the app, so a bad hop is visible.
- **Device health** — CPU, memory, Wi-Fi signal, and other endpoint metrics.

A falling score points to a layer: device (high CPU, weak Wi-Fi), network (loss
at a hop in Cloud Path), or application (slow server response) — which is
exactly the triage a help desk needs.

### Deep tracing

**Deep tracing** captures detailed diagnostics for a specific user/app over a
window — process-level and network detail — for the hard, intermittent problems
a single score cannot explain.

### Platform operations

- **Admin roles** scope which policies and which cloud an administrator can
  change (least privilege in the control plane).
- **Log streaming** — NSS (Nanolog Streaming Service) / LSS (Log Streaming
  Service) export logs to a SIEM in real time.
- **Automation** — ZIA, ZPA, and ZDX are API-driven, with a Terraform provider
  and SDKs, so configuration and reporting can be codified.

## Design Considerations

- **Probe the apps users care about.** A ZDX Score is only as useful as the
  probes configured — define web/app probes for the business-critical
  applications, not just a default.
- **Cloud Path localizes; the score alerts.** Use the score to notice
  degradation and Cloud Path/deep tracing to find *where* — they are alert vs.
  diagnosis.
- **Stream logs off-platform.** Send ZIA/ZPA logs to the SIEM via NSS/LSS so
  Zscaler telemetry joins the rest of security operations.

## Implementation and Automation

### Configuring monitoring (portal shape)

```text
# ZDX Portal: define an Application "M365" with web probe (URL) + Cloud Path;
#   enable device health; dashboards show ZDX Score by user/app/location.
```

### Modeling a ZDX score triage

```bash
python3 - <<'EOF'
def localize(device_cpu, worst_hop_loss, app_ms):
    if device_cpu > 90:        return "DEVICE (CPU)"
    if worst_hop_loss > 5:     return "NETWORK (Cloud Path hop loss)"
    if app_ms > 800:           return "APPLICATION (server response)"
    return "healthy"
for case in [(95,0,200),(20,12,200),(20,0,1200),(20,0,200)]:
    print(case, "->", localize(*case))
EOF
```

### Log streaming and API (shape)

```bash
# Stream logs to SIEM: ZIA NSS / LSS feeds (firewall, web, DNS, DLP) in real time.
# API/automation example (authenticate for your tenant/cloud first):
#   GET /zdx/v1/applications        -> monitored apps + scores
#   GET /zdx/v1/.../deep-traces     -> deep-trace results
echo "ZIA/ZPA/ZDX are API-driven; a Terraform provider codifies config"
```

## Validation and Troubleshooting

- **Score dropped, cause unknown.** Open Cloud Path (network) and device health
  (endpoint) for the affected users — the score says "degraded," the probes say
  "where."
- **No data for an app.** No probe is configured for it — ZDX measures what you
  tell it to probe.
- **SIEM missing Zscaler events.** NSS/LSS feed not configured or filtered —
  logs are streamed, not pulled.

## Security and Best Practices

- **Least privilege for admins** — scope roles to the policies and cloud each
  administrator needs; do not share a super-admin.
- **Stream logs to the SIEM** so Zscaler is part of detection and response, not
  a silo.
- **Codify configuration** with the API/Terraform provider so policy is
  reviewed, versioned, and reproducible (the discipline of Volume IX).

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Digital Experience Monitoring (ZDX): ZDX Score, Cloud
  Path, Deep Tracing* (`help.zscaler.com`).
- Zscaler Help Portal — *Nanolog Streaming Service (NSS) / Log Streaming
  Service (LSS)*; Zscaler API and Terraform provider documentation.

### Knowledge Checks

- What three signal types feed the ZDX Score, and which layer does each expose?
- How do Cloud Path and deep tracing differ in what they diagnose?
- Why does a ZDX Score require probes to be configured to be meaningful?
- How does NSS/LSS put Zscaler telemetry into security operations?

## Hands-On Lab

This chapter's labs cover ZDX triage and platform operations. The triage model
runs locally; ZDX/portal and API steps reference the tenant. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.3** — `python3`; a Zscaler tenant for
portal/API steps. **Cost:** none.

### Lab 9.1 — Triage a ZDX score to a layer (Topic: Digital experience)

**Objective:** Localize "the app is slow" to device, network, or app.

```bash
python3 - <<'EOF'
def localize(device_cpu, worst_hop_loss, app_ms):
    if device_cpu > 90:    return "DEVICE"
    if worst_hop_loss > 5: return "NETWORK"
    if app_ms > 800:       return "APPLICATION"
    return "healthy"
assert localize(95,0,200)=="DEVICE"
assert localize(20,12,200)=="NETWORK"
assert localize(20,0,1200)=="APPLICATION"
print("ZDX triage localizes to the right layer")
EOF
```

**Expected result:** each case localizes to device, network, or application —
the ZDX Score blends device health, Cloud Path (per-hop loss/latency), and
web/app probes, so a support engineer can point to the failing layer instead of
guessing.

**Negative test:** judge experience from the app's server-side metrics alone; a
weak-Wi-Fi or bad-hop problem is invisible there — ZDX measures the whole path
end to end for exactly that reason.

**Cleanup:** none.

### Lab 9.2 — Cloud Path and deep tracing (Topic: Diagnosis)

**Objective:** Find *where* a degradation is, not just that it exists.

```text
# ZDX Portal: open Cloud Path for the affected user->app (hop-by-hop latency/loss);
#   start a Deep Trace over the incident window for process + network detail.
```

**Expected result:** Cloud Path shows the hop where loss/latency spikes and deep
tracing captures endpoint/network detail over the window — the score alerts that
experience degraded; Cloud Path and deep tracing diagnose the exact layer and
hop, which is the difference between "it's slow" and a root cause.

**Negative test:** rely on the aggregate score alone to fix an intermittent
issue; it tells you *that* not *where* — diagnosis needs Cloud Path/deep
tracing.

**Cleanup:** stop the lab deep trace.

### Lab 9.3 — Operations: roles, logging, automation (Topic: Platform ops)

**Objective:** Operate the platform safely and reproducibly.

```text
# Admin Roles: scope an operator to ZIA web policy on the correct cloud only.
# NSS/LSS: stream firewall/web/DNS/DLP logs to the SIEM.
# API/Terraform: codify a URL-filtering rule so it is versioned and reviewed.
```

**Expected result:** admins hold least-privilege scoped roles, logs stream to
the SIEM in real time, and configuration is codified via API/Terraform — the
platform is operated with least privilege, integrated telemetry, and
reproducible config rather than click-ops on a shared super-admin.

**Negative test:** run everything as one shared super-admin with no log
streaming; a mistake is unattributable and Zscaler is a telemetry silo — roles
and NSS/LSS are what make operations accountable.

**Cleanup:** revert lab role/log/config changes.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ZDX turns the inline vantage point into operational visibility: the ZDX Score
blends device, network (Cloud Path), and application probes to localize a
problem, and deep tracing diagnoses the hard cases. Around it, platform
operations — least-privilege admin roles, NSS/LSS log streaming to the SIEM, and
API/Terraform automation — keep the deployment accountable and reproducible.
Together with the preceding chapters, this completes the operate-and-optimize
view of the Zero Trust Exchange that the ZDXA and ZDTE credentials assess.

- [ ] Can localize a ZDX score change to device, network, or application.
- [ ] Knows when to use Cloud Path vs. deep tracing.
- [ ] Can scope admin roles, stream logs to a SIEM, and codify config.
- [ ] Understands ZDX as the operational layer over the whole platform.
