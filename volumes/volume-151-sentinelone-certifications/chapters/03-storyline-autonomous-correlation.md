# Chapter 03: Storyline — Autonomous Correlation

## Learning Objectives

- Explain the alert-correlation problem in a SOC.
- Understand how Storyline auto-correlates events into an attack narrative.
- Describe how correlation cuts mean-time-to-respond and analyst fatigue.
- Recognize the attack story as the unit of investigation.

*Cert relevance: Storyline is a signature SentinelOne concept — **SIREN** and **THP** both assume you investigate stories, not isolated alerts.*

## The correlation problem

A single attack generates *hundreds* of low-level events across an endpoint: a process starts, reads a file, opens a network connection, spawns a child, writes to the registry, injects into another process. Traditional EDR emits these as **separate alerts**, and a human analyst must **manually stitch them together** — "is this PowerShell alert related to that network alert and this file-write alert?" — reconstructing the attack by hand from a flood of disconnected signals.

This is slow, error-prone, and the primary source of **analyst fatigue and alert overload**: a SOC drowning in thousands of individual alerts cannot tell which twenty are one attack and which are noise. Correlation — connecting related events into a coherent picture — is the hardest, most time-consuming part of the job, and doing it manually does not scale.

## Storyline: automatic correlation

**Storyline** is SentinelOne's answer: the agent **automatically correlates** all the related events on an endpoint into a single **attack narrative** — one "story" that shows the full sequence from the initial entry through every action to the impact, with the causal relationships already drawn. Instead of 200 alerts, the analyst sees **one story**: "this Word document spawned PowerShell, which downloaded a payload, which injected into a process, which began encrypting files."

The mechanism is that the agent tracks the **relationships between events in real time** (which process spawned which, which process touched which file), assigning related activity a common **Storyline ID**. The correlation is done *by the agent, automatically, as it happens* — not reconstructed later by an analyst. This is the same **autonomy** principle as the response model ([Chapter 2](02-autonomous-endpoint-protection.md)): the machine does the tedious, machine-scale work (correlating hundreds of events), leaving the human to *judge the story*. The lab models it.

## The story as the unit of work

The consequence reframes the SOC workflow: the **unit of investigation is the attack story, not the individual alert.** An analyst triaging a Storyline sees the whole attack at once — entry, spread, impact — and can respond to the *entire* story with one action (kill the whole process tree, not one process). This slashes **mean-time-to-respond (MTTR)** and lets a smaller team handle more, because they reason about *attacks* rather than drowning in *events*. The [SIREN](01-the-sentinelone-university-program.md) certification is built around investigating stories. The lab quantifies the reduction.

## Hands-On Lab

Python models event correlation. **Cost:** none.

### Lab 3.1 — From raw events to one attack story

**Objective:** Correlate scattered events into a single narrative by their relationships.

```bash
python3 - <<'EOF'
# raw endpoint events: (id, parent_id, action) — a flood a legacy tool alerts on separately
EVENTS = [
  (1, None, "winword.exe opens invoice.doc"),
  (2, 1,    "winword.exe spawns powershell.exe"),          # child of 1
  (3, 2,    "powershell downloads payload.exe from evil.com"),
  (4, 3,    "payload.exe injects into explorer.exe"),
  (5, 4,    "explorer.exe connects to C2 45.9.x.x"),
  (6, 4,    "explorer.exe begins encrypting *.docx"),      # the impact
  (7, None, "chrome.exe loads a web page"),                # UNRELATED benign
]
# correlate: walk parent links to assign a common storyline id
def root(eid, byid):
    e = byid[eid]
    return root(e[1], byid) if e[1] is not None else eid
byid = {e[0]: e for e in EVENTS}
from collections import defaultdict
stories = defaultdict(list)
for e in EVENTS:
    stories[root(e[0], byid)].append(e[2])

print("LEGACY EDR: 7 separate alerts, analyst must stitch them by hand:")
for e in EVENTS:
    print(f"   ALERT: {e[2]}")
print("   -> which are related? which are one attack? Manual, slow, error-prone.\n")

print("STORYLINE: auto-correlated into stories by event relationships:")
for sid, actions in stories.items():
    kind = "ATTACK STORY" if len(actions) > 1 else "(benign, single event)"
    print(f"   Storyline {sid} [{kind}]:")
    for a in actions:
        print(f"      -> {a}")
print("\nThe agent tracked WHO SPAWNED WHOM in real time and assigned related events a")
print("common Storyline ID. The 6-step attack (doc -> powershell -> payload -> inject")
print("-> C2 -> encrypt) collapses into ONE story showing entry to impact, causal")
print("chain drawn. The unrelated chrome event is its own (benign) story.")
print("\nInstead of 7 alerts to stitch, the analyst sees ONE attack narrative and one")
print("benign event. This is Storyline: automatic correlation into the ATTACK STORY —")
print("the machine does the tedious event-stitching, the human judges the story.")
EOF
```

**Expected result:** Seven scattered raw events auto-correlated by their parent-child relationships into one six-step attack story (document to PowerShell to payload to injection to C2 to encryption) plus one separate benign event. The Storyline lesson is that the agent tracks event relationships in real time and collapses a flood of alerts into a single readable attack narrative, so the analyst judges one story instead of stitching hundreds of events.

**Negative test:** Triaging each event as a separate alert. The analyst must manually determine which of the seven are related — slow and error-prone — where Storyline has already drawn the causal chain into one story.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Correlation cuts MTTR and alert load

**Objective:** Quantify the analyst-time reduction from story-level investigation.

```bash
python3 - <<'EOF'
DAILY_EVENTS = 8000          # raw security events across the fleet
EVENTS_PER_ATTACK = 40       # a real attack spans ~40 events
NOISE_FRACTION = 0.95        # 95% of events are benign noise

real_attack_events = int(DAILY_EVENTS * (1 - NOISE_FRACTION))
attacks = max(1, real_attack_events // EVENTS_PER_ATTACK)

print(f"{DAILY_EVENTS} raw events/day. {NOISE_FRACTION:.0%} are benign noise.\n")
print("WITHOUT correlation (alert per event):")
MIN_PER_ALERT = 3
alerts = DAILY_EVENTS  # every event a potential alert
hours = alerts * MIN_PER_ALERT / 60
print(f"   ~{alerts} alerts to triage at {MIN_PER_ALERT} min each = {hours:,.0f} analyst-hours/day")
print(f"   -> IMPOSSIBLE. The SOC drowns; real attacks hide in the flood (alert fatigue).\n")

print("WITH Storyline (investigate stories, not events):")
# events collapse into stories; benign events into benign stories, attacks into ~N stories
benign_stories = int(DAILY_EVENTS*NOISE_FRACTION / 20)   # benign events also group
total_stories = benign_stories + attacks
MIN_PER_STORY = 8   # a story takes longer each, but there are FAR fewer
hours2 = total_stories * MIN_PER_STORY / 60
print(f"   {DAILY_EVENTS} events collapse into ~{total_stories} stories ({attacks} are real attacks)")
print(f"   ~{total_stories} stories at {MIN_PER_STORY} min each = {hours2:,.1f} analyst-hours/day")
print(f"\n   analyst-hours: {hours:,.0f} -> {hours2:,.1f}  ({hours/hours2:.0f}x less work)")
print("\nThe reduction isn't just fewer clicks — it's a different UNIT of work. You")
print("investigate ~dozens of STORIES, not thousands of EVENTS, and each story is a")
print("whole attack you can respond to at once (kill the whole tree). MTTR drops")
print("because you see entry-to-impact immediately; alert fatigue drops because the")
print("machine did the correlation. A small team can defend a large fleet — the whole")
print("economic argument for autonomous correlation.")
EOF
```

**Expected result:** Thousands of daily events being impossible to triage per-alert but collapsing into a few dozen stories that a team can actually investigate, an order-of-magnitude reduction in analyst hours. The correlation-economics lesson is that Storyline changes the unit of work from events to attack stories, dropping MTTR and alert fatigue so a small team can defend a large fleet.

**Negative test:** Staffing a SOC to triage every raw event as an alert. The volume is impossible and real attacks hide in the noise; correlating into stories makes the workload tractable and surfaces the real attacks.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The correlation problem understood — attacks generate hundreds of events that legacy EDR emits as separate alerts to stitch by hand.
- [ ] Storyline understood as automatic, real-time correlation of related events into one attack narrative.
- [ ] The MTTR and alert-fatigue reduction understood — the machine correlates, the human judges the story.
- [ ] The attack story recognized as the unit of investigation and response, not the individual alert.
