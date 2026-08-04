# Chapter 07: Detections, Alerts, and Deception Technology

## Learning Objectives

- Tune the alert framework so analysts can trust it.
- Deploy deception technology: honeypots, honey users, honey credentials, and honey files.
- Correlate threat intelligence without drowning in indicators.
- Measure detection quality with precision and recall rather than volume.

## The alert framework

The InsightIDR alert framework is explicitly on the Certified Specialist syllabus, and the discipline it teaches generalizes: **an alert nobody trusts is worse than no alert**, because it consumes attention and trains people to dismiss the category.

Tuning levers:

| Lever | Use |
|:---|:---|
| **Threshold** | How much of the behavior is needed to fire |
| **Exceptions** | Known-good actors and systems (the vulnerability scanner will always look like an attacker) |
| **Suppression window** | Prevent one condition generating hundreds of alerts |
| **Priority** | Route by severity so not everything pages |
| **Enrichment** | Attach the asset, user, and threat context the analyst would otherwise look up |

Enrichment is the underrated one: an alert carrying its own context is triaged in a minute, while a bare alert becomes a ten-minute investigation before the analyst even knows whether it matters.

## Deception technology

Deception is the most distinctive part of this syllabus, and its appeal is a signal-to-noise property no other detection shares: **a legitimate user has no reason to touch a decoy, so an interaction is almost by definition suspicious.**

| Decoy | What it is | What tripping it means |
|:---|:---|:---|
| **Honeypot** | A fake system on the network | Something is scanning or moving laterally |
| **Honey user** | A fake account, never used, often attractively named (`svc_backup_admin`) | Someone is enumerating or spraying accounts |
| **Honey credential** | Fake credentials planted on real hosts | Someone is harvesting credentials from memory or files |
| **Honey file** | An attractive fake document (`passwords.xlsx`) | Someone is browsing for sensitive data |

Two properties make this powerful. First, **near-zero false positives** — nobody legitimately authenticates as an account that does not correspond to a person. Second, decoys catch attackers at the *reconnaissance and lateral-movement* stage, which is early, and they are indifferent to whether the technique is novel: a brand-new attack tool trips a honey credential exactly as reliably as an old one.

The caveats are honest ones: deception detects an attacker who **interacts** with a decoy, so it is a complement to other detection rather than a replacement, and decoys need to be plausible — a honey user named `honeypot_test` catches nobody.

## Threat intelligence

Indicator feeds correlate observed activity against known-bad infrastructure. The practical problem is volume and staleness: feeds contain millions of indicators, many long dead, and matching everything produces noise. Value comes from **relevant, current, contextualized** intelligence — and from remembering that indicator matching detects *known* badness only.

## Measuring detection quality

Volume is not quality. The measures that matter:

- **Precision** — of the alerts fired, how many were real? Low precision means fatigue.
- **Recall** — of the real incidents, how many did we alert on? Low recall means blindness.

They trade off, and the honest goal is to state where you have chosen to sit on that curve rather than pretending you have maximized both.

## Hands-On Lab

Python models detection tuning. **Cost:** none.

### Lab 7.1 — Deception trip-wires

**Objective:** Show the signal-to-noise advantage of decoys.

```bash
python3 - <<'EOF'
decoys = {
  "svc_backup_admin":  "honey user (never used by anyone)",
  "10.4.9.250":        "honeypot host (no legitimate service)",
  "passwords.xlsx":    "honey file on the finance share",
  "SQLSvc/backup2019": "honey credential planted in memory",
}
events = [
  {"actor":"j.doe","target":"fileserver/reports.xlsx","kind":"normal"},
  {"actor":"unknown","target":"svc_backup_admin","kind":"auth attempt"},
  {"actor":"laptop-11","target":"10.4.9.250","kind":"port scan"},
  {"actor":"r.patel","target":"crm.internal","kind":"normal"},
  {"actor":"srv-app-02","target":"passwords.xlsx","kind":"file open"},
]
alerts = 0
for e in events:
    if e["target"] in decoys:
        alerts += 1
        print(f"HIGH-CONFIDENCE ALERT: {e['actor']} -> {e['target']}")
        print(f"   {decoys[e['target']]} — no legitimate reason to touch this")
    else:
        print(f"(normal) {e['actor']} -> {e['target']}")
print(f"\n{alerts} alerts from {len(events)} events — and every one is worth investigating.")
print("\nWhy deception is different: most detections ask 'is this behavior unusual?' and get")
print("false positives from unusual-but-legitimate activity. A decoy asks 'did anyone touch a")
print("thing nobody should touch?' — so a hit is suspicious BY CONSTRUCTION.")
print("Caveat: it only catches an attacker who INTERACTS with a decoy, and decoys must be")
print("plausible. A honey user named 'honeypot_test' catches nobody.")
EOF
```

**Expected result:** Three high-confidence alerts and two normal events, with no false positives. The structural explanation in the closing lines is the exam-relevant insight: deception's advantage is not better analytics but a **better question** — interaction with a decoy is inherently anomalous, so the detection does not need to model normal behavior at all.

**Negative test:** Deploying obviously-named decoys — an attacker who recognizes `honeypot-01` avoids it and you have detection theater.

**Cleanup:** None.

### Lab 7.2 — Tune an alert nobody trusts

**Objective:** Raise precision without destroying recall.

```bash
python3 - <<'EOF'
def evaluate(name, true_positives, false_positives, missed):
    fired = true_positives + false_positives
    precision = true_positives / fired * 100 if fired else 0
    recall = true_positives / (true_positives + missed) * 100 if (true_positives + missed) else 0
    if precision < 10:
        verdict = "IGNORED IN PRACTICE — analysts learn this alert means nothing"
    elif precision < 50:
        verdict = "noisy but survivable"
    else:
        verdict = "trusted"
    print(f"{name:34} fired {fired:>4}  precision {precision:5.1f}%  recall {recall:5.1f}%  -> {verdict}")

print("Detection: 'impossible travel'\n")
evaluate("untuned",                     tp=8,  fp=412, missed=1)
evaluate("+ VPN/proxy exceptions",      tp=8,  fp=95,  missed=1)
evaluate("+ known-good travel patterns",tp=7,  fp=18,  missed=2)
evaluate("over-tuned (threshold too high)", tp=2, fp=1, missed=7)

print("\nUntuned: 420 alerts to find 8 real ones (2% precision) — analysts stop reading it,")
print("which converts 8 true positives into 0 investigated ones.")
print("Well tuned: 25 alerts, 7 real (28%), one incident missed — a deliberate, stated trade.")
print("OVER-tuned: beautiful 67% precision and it now MISSES 7 of 9 real incidents.")
print("\nAlways report precision AND recall. Optimizing precision alone produces a quiet,")
print("blind detection that looks excellent on a dashboard.")
EOF
```

**Expected result:** Precision climbs from 2% to 28% across sensible tuning steps, then the over-tuned version reaches 67% precision while missing seven of nine real incidents. That last row is the trap the lab exists to show — precision alone is a metric you can improve by detecting less, and it looks like progress.

**Negative test:** Tuning until the alert is quiet and declaring success — silence is indistinguishable from blindness unless you measure recall against known incidents.

**Cleanup:** None.

### Lab 7.3 — Threat intelligence without the noise

**Objective:** Filter indicators to the relevant and current.

```bash
python3 - <<'EOF'
import datetime
today = datetime.date(2026, 8, 4)
indicators = [
  {"ioc":"185.220.101.5","type":"ip","first_seen":datetime.date(2026,7,30),"confidence":"high","relevant_sector":True},
  {"ioc":"malware.example","type":"domain","first_seen":datetime.date(2023,1,10),"confidence":"low","relevant_sector":False},
  {"ioc":"d41d8cd9...","type":"hash","first_seen":datetime.date(2026,8,1),"confidence":"high","relevant_sector":True},
  {"ioc":"91.219.29.8","type":"ip","first_seen":datetime.date(2024,5,2),"confidence":"medium","relevant_sector":False},
]
def keep(i):
    age = (today - i["first_seen"]).days
    if age > 365:                 return False, f"stale ({age}d old) — IPs and domains recycle"
    if i["confidence"] == "low":  return False, "low confidence — matching it costs more than it finds"
    return True, f"current ({age}d), {i['confidence']} confidence" + (", sector-relevant" if i["relevant_sector"] else "")

kept = 0
for i in indicators:
    ok, why = keep(i)
    kept += ok
    print(f"{'USE  ' if ok else 'DROP '} {i['ioc']:16} [{i['type']:6}] {why}")
print(f"\n{kept}/{len(indicators)} indicators retained.")
print("\nFeeds contain millions of indicators, many long dead. Matching everything generates")
print("noise and false attribution — a recycled IP now belongs to someone innocent.")
print("And remember the ceiling: indicator matching detects KNOWN badness only. It cannot")
print("see a novel campaign, which is exactly what behavioral detection and deception are for.")
EOF
```

**Expected result:** Two of four indicators retained, with staleness and low confidence filtered out. The closing caveat frames the whole technique honestly: threat intelligence is a cheap way to catch known-bad infrastructure and is structurally incapable of catching anything new — which is why it belongs alongside the behavioral and deception detections rather than in place of them.

**Negative test:** Ingesting every available feed at full volume — you generate matches against recycled infrastructure and spend investigation time on innocent third parties.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Alert framework tuned with thresholds, exceptions, suppression, priority, and enrichment.
- [ ] Deception deployed across honeypots, honey users, credentials, and files, with plausibility required.
- [ ] Precision *and* recall measured, with over-tuning recognized as disguised blindness.
- [ ] Threat intelligence filtered for currency and confidence, and understood as known-badness only.
