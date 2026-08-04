# Chapter 06: Log Collection and the Detection Pipeline

## Learning Objectives

- Identify the log sources a SIEM needs and why each matters.
- Explain parsing, normalization, and attribution of events to users and assets.
- Query log data effectively to investigate.
- Apply user behavior analytics without over-trusting it.

## What InsightIDR is

**InsightIDR** is Rapid7's SIEM and detection-and-response product, and the **Certified Specialist** exam covers log collection, the log query language, endpoint detection via Insight Agents, deception technology, alert framework tuning, threat intelligence correlation, and incident-response automation.

The pipeline underneath is the same in every SIEM: **collect → parse → normalize → attribute → detect → alert → investigate**. Understanding it as a pipeline matters because a failure at any stage degrades everything downstream, usually silently.

## Sources

| Source | Detects |
|:---|:---|
| **Active Directory / identity** | Authentication, privilege changes, account creation — the backbone |
| **Endpoint (Insight Agent)** | Process execution, local activity, on and off the corporate network |
| **Firewall / network** | Connections, egress, lateral movement |
| **VPN / remote access** | Where users connect from |
| **DHCP** | IP-to-host mapping over time — essential for attribution |
| **Cloud / SaaS** | Activity outside your perimeter entirely |
| **DNS** | Resolution behavior, including command-and-control patterns |

**Identity sources are the highest-value starting point**, because nearly every attack involves authentication somewhere, and because they enable the attribution that makes everything else readable.

## Attribution is the point

Raw logs describe **IP addresses and hostnames**. Investigations are about **people and machines**. A SIEM's central job is joining those: DHCP maps an IP to a host over a time window, identity data maps a session to a user, and the agent ties activity to a device wherever it is.

Without attribution, an alert reads "10.4.2.88 did something suspicious at 03:14" and the analyst starts a research project. With it, the same alert reads "j.doe's laptop did something suspicious at 03:14" and the investigation starts immediately. This is also why **DHCP logs matter far more than their dullness suggests** — without them, an IP in a log from last Tuesday cannot be resolved to the machine that held it.

## Parsing and normalization

**Parsing** extracts fields from raw text; **normalization** maps them into common names so a query can span sources. When a source's format changes — a vendor upgrade, a new log version — parsing silently breaks, and the detections built on those fields stop firing. Nothing errors. The alerts simply stop, which looks exactly like quiet.

## User behavior analytics, honestly

**UBA** baselines normal behavior per user and flags deviations: a first-time country, an unusual volume of access, activity at an unusual hour. It is genuinely useful for detecting compromised credentials, where the account is legitimate and only the *behavior* is wrong.

Its limits are equally real: baselines need time and stable behavior, genuinely novel activity produces false positives (a person's first business trip is anomalous), and an attacker who moves slowly stays inside the baseline. Treat UBA as a signal that raises priority, not as a verdict.

## Hands-On Lab

Python models the pipeline. **Cost:** none.

### Lab 6.1 — Attribution: from IP to person

**Objective:** Join network events to users through DHCP and identity data.

```bash
python3 - <<'EOF'
dhcp = [
  {"ip":"10.4.2.88","host":"laptop-hr-07","start":"2026-08-03T08:00","end":"2026-08-04T09:00"},
  {"ip":"10.4.2.88","host":"laptop-eng-12","start":"2026-08-04T09:30","end":None},
]
sessions = [
  {"host":"laptop-hr-07","user":"j.doe","start":"2026-08-03T08:05"},
  {"host":"laptop-eng-12","user":"r.patel","start":"2026-08-04T09:35"},
]
events = [
  {"ts":"2026-08-03T22:14","ip":"10.4.2.88","action":"connected to rare external host"},
  {"ts":"2026-08-04T11:02","ip":"10.4.2.88","action":"connected to rare external host"},
]
def attribute(ts, ip):
    for lease in dhcp:
        if lease["ip"] == ip and lease["start"] <= ts and (lease["end"] is None or ts <= lease["end"]):
            host = lease["host"]
            user = next((s["user"] for s in sessions if s["host"] == host), "unknown")
            return host, user
    return None, None

for e in events:
    host, user = attribute(e["ts"], e["ip"])
    print(f"{e['ts']}  {e['ip']}  {e['action']}")
    print(f"      -> {host} ({user})")
print("\nSAME IP, two different machines and two different people, one day apart.")
print("Without DHCP correlation both alerts read '10.4.2.88' and the analyst cannot tell")
print("whether this is one repeat offender or two unrelated events. Attribution IS the product.")
EOF
```

**Expected result:** The same IP resolves to `laptop-hr-07`/`j.doe` on one day and `laptop-eng-12`/`r.patel` the next. That reassignment is entirely routine on a DHCP network and completely invisible without lease data — which is why an unglamorous log source turns out to be a prerequisite for meaningful investigation.

**Negative test:** Investigating by IP address alone across a multi-day window — you will attribute one machine's behavior to another user's device and reach a confident wrong conclusion.

**Cleanup:** None.

### Lab 6.2 — Parsing breaks silently

**Objective:** Detect the failure mode that produces no error.

```bash
python3 - <<'EOF'
import re
PARSER = re.compile(r"user=(?P<user>\S+) src=(?P<src>\S+) result=(?P<result>\S+)")

old_format = "2026-08-01 auth user=j.doe src=10.4.2.88 result=success"
new_format = '2026-08-04 auth {"user":"j.doe","src":"10.4.2.88","result":"success"}'   # vendor upgrade

for label, line in (("before upgrade", old_format), ("after upgrade", new_format)):
    m = PARSER.search(line)
    if m:
        print(f"{label:15} PARSED  {m.groupdict()}")
    else:
        print(f"{label:15} NO MATCH — fields are empty; the event still INGESTS as raw text")

print("\nWhat happens next:")
print("  - the event volume dashboard looks NORMAL (events are still arriving)")
print("  - 'user' and 'result' are now empty, so every detection keyed on them stops firing")
print("  - no error is raised anywhere; the SIEM simply goes quiet on that source")
print("\nDetect it: alert on PER-SOURCE PARSE-SUCCESS RATE and on detections that stop firing,")
print("not just on ingest volume. Silence after a vendor upgrade is a symptom, not good news.")
EOF
```

**Expected result:** The parser matches the old format and fails on the new one, while events keep flowing. This is among the most dangerous SIEM failures precisely because every obvious health indicator stays green — volume is normal, ingestion succeeds, and only the *content* of the events has become unusable. Monitoring parse-success rate per source is the countermeasure.

**Negative test:** Monitoring only ingest volume — a parsing break shows no volume change at all, so the coverage loss is invisible until an incident review asks why nothing alerted.

**Cleanup:** None.

### Lab 6.3 — UBA baselines and their limits

**Objective:** Flag behavioral anomalies while respecting what they cannot tell you.

```bash
python3 - <<'EOF'
baseline = {"j.doe": {"countries":{"GB"}, "hours":set(range(8,19)), "avg_files":40}}
events = [
  {"user":"j.doe","country":"GB","hour":10,"files":45},
  {"user":"j.doe","country":"GB","hour":3, "files":38},
  {"user":"j.doe","country":"BR","hour":11,"files":42},
  {"user":"j.doe","country":"GB","hour":14,"files":900},
]
for e in events:
    b = baseline[e["user"]]
    flags = []
    if e["country"] not in b["countries"]: flags.append(f"new country {e['country']}")
    if e["hour"] not in b["hours"]:        flags.append(f"unusual hour {e['hour']:02d}:00")
    if e["files"] > b["avg_files"] * 5:    flags.append(f"volume {e['files']} vs baseline {b['avg_files']}")
    print(f"{e} -> {'ANOMALY: ' + '; '.join(flags) if flags else 'normal'}")

print("\nWhat UBA is good at: COMPROMISED CREDENTIALS — the account is legitimate, only the")
print("behavior is wrong, so signature-based detection sees nothing.")
print("\nWhat it cannot do:")
print("  - a first business trip is anomalous and benign (false positive)")
print("  - a NEW employee has no baseline for weeks")
print("  - an attacker who moves slowly stays INSIDE the baseline (false negative)")
print("Treat an anomaly as a priority signal to investigate, never as a verdict.")
EOF
```

**Expected result:** Three anomalies flagged — an unusual hour, a new country, and a 22x file-access spike — with the honest limits stated. The framing in the final line is what separates useful UBA from alert fatigue: anomaly scores are inputs to triage, and treating them as conclusions produces both wrongly-accused users and false confidence about the slow attacker who never trips a threshold.

**Negative test:** Auto-disabling accounts on UBA anomalies — the first employee to travel gets locked out mid-trip, and after two such incidents the detection is switched off entirely.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Log sources identified, with identity data recognized as the highest-value starting point.
- [ ] Attribution modeled through DHCP and session data, from IP to person.
- [ ] Silent parsing failure understood, and parse-success rate adopted as the monitor.
- [ ] UBA applied to compromised-credential detection, with its false positives and blind spots stated.
