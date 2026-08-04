# Chapter 05: Server and Application Monitoring

## Learning Objectives

- Build application monitors from component monitors and templates.
- Roll component health up into a meaningful application status.
- Monitor the full stack: hardware, operating system, service, and user experience.
- Distinguish "the process is running" from "the service works."

## The SAM discipline

This is the **SolarWinds Server and Application Monitor (SAM)** exam's territory. Its core insight is compositional: an application's health is not one metric but a **rollup of component checks**, and the design work is choosing components that actually reflect whether users can do their job.

| Layer | Example checks |
|:---|:---|
| **Hardware** | Fans, PSU, temperature, RAID/disk health, predictive failure |
| **Operating system** | CPU, memory, disk space, disk latency, page/swap |
| **Service/process** | Process running, service state, port listening |
| **Application** | HTTP response and content, query returns expected result, queue depth, error rate |
| **User experience** | Synthetic transaction — log in, search, check out |

## The critical distinction

**"The process is running" is not "the service works."** A web server process can be alive while returning 500 errors to every request; a database service can be up while every query times out; a queue consumer can be running while the queue grows without bound.

This is why **component monitors that test behavior** — fetch a URL and check the content, run a query and check the result, measure queue depth — are worth far more than process checks. The exam-relevant framing: monitor the **outcome the user cares about**, then add lower-level checks to explain *why* it broke.

## Templates

A **template** is a reusable set of component monitors for an application type (IIS, SQL Server, Exchange, Apache). Apply it to a node and you get the whole check set consistently. Templates matter for the same reason plans mattered in data protection and roles mattered in identity: **consistency across scale**, and the ability to improve every instance at once by improving the template.

## Rollup logic

When components have different importance, health rollup must reflect it. A failed hardware fan and a failed login transaction are not equally urgent, and a single degraded component out of twelve should not necessarily mark an application "down." Sensible rollup weights components by criticality and distinguishes **degraded** from **down** — otherwise every dashboard is red and nobody looks at it.

## Hands-On Lab

Python models application monitoring. **Cost:** none.

### Lab 5.1 — Compose an application template

**Objective:** Build a template from component monitors across the stack.

```bash
python3 - <<'EOF'
template = {
  "name":"Web Application (3-tier)",
  "components":[
    {"name":"HTTP 200 + content match","layer":"application","critical":True},
    {"name":"login synthetic transaction","layer":"experience","critical":True},
    {"name":"app service running","layer":"service","critical":True},
    {"name":"SQL query returns rows","layer":"application","critical":True},
    {"name":"CPU < 90%","layer":"os","critical":False},
    {"name":"free disk > 10%","layer":"os","critical":False},
    {"name":"RAID healthy","layer":"hardware","critical":False},
  ],
}
print(f"TEMPLATE: {template['name']}  ({len(template['components'])} component monitors)\n")
for layer in ["experience","application","service","os","hardware"]:
    for c in template["components"]:
        if c["layer"] == layer:
            print(f"  [{layer:11}] {c['name']:32} {'CRITICAL' if c['critical'] else 'supporting'}")
print("\nApply this template to every web server: consistent checks, and improving the template")
print("improves every instance at once.")
EOF
```

**Expected result:** Seven component monitors spanning experience down to hardware, with the user-facing checks marked critical and the resource checks supporting. The layering is deliberate — the **critical** checks answer "can users work?", while the supporting checks explain *why* when the answer is no.

**Negative test:** Building bespoke monitors per server — every host checks slightly different things, coverage gaps are invisible, and improving a check means editing dozens of nodes.

**Cleanup:** None.

### Lab 5.2 — Process running versus service working

**Objective:** Demonstrate why process checks mislead.

```bash
python3 - <<'EOF'
scenarios = [
  {"host":"web-01","process_running":True, "http_status":200,"content_ok":True, "response_ms":180},
  {"host":"web-02","process_running":True, "http_status":500,"content_ok":False,"response_ms":90},
  {"host":"web-03","process_running":True, "http_status":200,"content_ok":True, "response_ms":9500},
  {"host":"web-04","process_running":False,"http_status":None,"content_ok":False,"response_ms":None},
]
for s in scenarios:
    proc = "UP" if s["process_running"] else "DOWN"
    if not s["process_running"]:
        verdict = "DOWN — process check and service check agree"
    elif s["http_status"] != 200 or not s["content_ok"]:
        verdict = f"BROKEN — process is UP but HTTP {s['http_status']} / content mismatch <-- PROCESS CHECK LIES"
    elif s["response_ms"] > 5000:
        verdict = f"DEGRADED — works but {s['response_ms']}ms; users experience this as broken"
    else:
        verdict = "HEALTHY"
    print(f"{s['host']}  process={proc:4}  -> {verdict}")
print("\nTwo of four hosts would be reported HEALTHY by a process-only monitor while failing users.")
EOF
```

**Expected result:** `web-02` returns HTTP 500 and `web-03` takes 9.5 seconds — both with a **running process**, so a process-only monitor calls them healthy while users experience an outage and a timeout respectively. This is the chapter's central lesson, and it generalizes: monitor the behavior users depend on, not the existence of a process.

**Negative test:** Alerting on "service stopped" as the primary application check — you catch only the cleanest failure mode and miss error responses, hangs, and slow degradation, which are the common ones.

**Cleanup:** None.

### Lab 5.3 — Weighted health rollup

**Objective:** Roll components up into a status that means something.

```bash
python3 - <<'EOF'
def rollup(components):
    crit = [c for c in components if c["critical"]]
    sup  = [c for c in components if not c["critical"]]
    crit_down = [c for c in crit if not c["ok"]]
    sup_down  = [c for c in sup if not c["ok"]]
    if crit_down:
        return "DOWN", f"critical component(s) failed: {[c['name'] for c in crit_down]}"
    if len(sup_down) >= 2:
        return "WARNING", f"multiple supporting components degraded: {[c['name'] for c in sup_down]}"
    if sup_down:
        return "DEGRADED", f"supporting component degraded: {[c['name'] for c in sup_down]}"
    return "UP", "all components healthy"

states = {
 "app-A":[{"name":"login txn","critical":True,"ok":True},{"name":"HTTP","critical":True,"ok":True},
          {"name":"CPU","critical":False,"ok":True},{"name":"disk","critical":False,"ok":True}],
 "app-B":[{"name":"login txn","critical":True,"ok":True},{"name":"HTTP","critical":True,"ok":True},
          {"name":"CPU","critical":False,"ok":False},{"name":"disk","critical":False,"ok":True}],
 "app-C":[{"name":"login txn","critical":True,"ok":False},{"name":"HTTP","critical":True,"ok":True},
          {"name":"CPU","critical":False,"ok":True},{"name":"disk","critical":False,"ok":True}],
}
for app, comps in states.items():
    status, why = rollup(comps)
    print(f"{app}: {status:9} — {why}")
print("\nWithout weighting, app-B (high CPU, users fine) would look as bad as app-C (login broken).")
EOF
```

**Expected result:** `app-A` is UP, `app-B` is **DEGRADED** (high CPU, users unaffected), and `app-C` is **DOWN** because the login transaction failed. The closing line names the failure this design prevents: unweighted rollup makes a busy CPU look as serious as a broken login, and once every dashboard is red, the dashboard stops being consulted.

**Negative test:** Treating any failed component as "application down" — you generate alerts for conditions users never notice, and the resulting fatigue means the real outage is treated as one more false alarm.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Templates built from component monitors across hardware, OS, service, application, and experience.
- [ ] Behavior-testing monitors preferred over process-existence checks.
- [ ] The "process running ≠ service working" failure modes demonstrated.
- [ ] Health rolled up with criticality weighting to distinguish degraded from down.
