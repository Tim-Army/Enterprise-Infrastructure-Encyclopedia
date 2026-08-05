# Chapter 05: Attended vs Unattended and Orchestrator

## Learning Objectives

- Distinguish attended from unattended robots and when to use each.
- Understand queues and transactions — distributing work at scale.
- Place the REFramework as the standard robust template.
- Recognize credential and asset management as a governance necessity.

*Cert relevance: attended/unattended design, queues, and Orchestrator governance run through the **Developer** and **Solution Architect** certifications.*

## Attended versus unattended

The most consequential deployment decision is **attended versus unattended**:

| | **Attended** | **Unattended** |
|:---|:---|:---|
| Runs on | A person's desktop | A server, headless |
| Triggered by | The user (a button, a hotkey) | A schedule or event, automatically |
| Works alongside | The human, in real time | No human present |
| Best for | Assisting a worker (a call-center agent's helper) | High-volume back-office batches |

**Attended** robots *assist a person* — a call-center agent clicks a button and the robot pulls up the customer's records across five systems while they talk. **Unattended** robots *replace the manual running entirely* — at 2 a.m., with nobody watching, robots process the day's invoices. The choice follows the work: is a human in the loop (attended) or is this lights-out volume (unattended)? Getting it wrong — building an unattended batch as an attended robot that needs someone to click go — caps the automation's value. The lab models the choice.

## Queues and transactions

Unattended automation at scale runs on **queues**. Instead of one robot chewing through 10,000 invoices sequentially, Orchestrator puts the invoices in a **queue** as **transaction items**, and a *pool of robots* pulls items off the queue in parallel — ten robots processing the queue finish roughly ten times faster. Queues also provide **reliability**: each item's status (new, in-progress, successful, failed) is tracked, failed items can be retried, and the work survives a robot crash (another robot picks up where it left off).

This is the scaling pattern for volume automation: **decouple the work (queue) from the workers (robots)**, and add robots to go faster. The lab models queue throughput.

## The REFramework

UiPath provides the **REFramework** (Robotic Enterprise Framework) — a standard, battle-tested **template** for building robust unattended transaction-processing automations. It bakes in the hard-won best practices: a state machine (initialize → get transaction → process → end), automatic **retry** of failed transactions, **exception handling** that distinguishes business from application errors ([Chapter 4](04-building-automations-studio-and-workflows.md)), logging, and graceful recovery. Developers are expected to know it because it encodes the reliability patterns every serious unattended automation needs — starting from REFramework is starting from "does the right thing under failure."

## Credentials and assets

Unattended robots need to **log into systems** — which means handling **credentials** without a human to type them. Orchestrator manages this through **assets** (shared configuration) and **credential stores** (secure, often integrated with a vault), so a robot retrieves the password it needs at runtime without it ever being hardcoded in the automation. This is a **governance necessity**: a fleet of unattended robots with system access is a security surface, and centralizing credentials (never in the code, least privilege, audited) is essential — the same discipline the [identity and security volumes](../../volume-147-wiz-certifications/chapters/05-ciem-and-dspm-identity-and-data.md) teach. The lab touches this within the queue exercise.

## Hands-On Lab

Python models deployment and scaling. **Cost:** none.

### Lab 5.1 — Choose attended or unattended

**Objective:** Match the robot type to the work.

```bash
python3 - <<'EOF'
SCENARIOS = [
  # scenario,                                     best,        why
  ("call-center agent needs customer data pulled","attended",  "assists a person in real time, they trigger it"),
  ("process 10k invoices overnight",              "unattended","high-volume, lights-out, no human present"),
  ("employee clicks to auto-fill a form",         "attended",  "on-demand help at the user's desk"),
  ("nightly reconciliation of two ledgers",       "unattended","scheduled batch, no human, runs headless"),
  ("generate month-end reports at 3am",           "unattended","scheduled, unattended by definition"),
]
print(f"{'scenario':46}{'type':>12}   why")
for scen, typ, why in SCENARIOS:
    print(f"{scen:46}{typ:>12}   {why}")
print("\nThe deciding question: IS A HUMAN IN THE LOOP, in real time?")
print("  ATTENDED   — a person triggers it and works ALONGSIDE it (a helper at their")
print("               desk). Value = augmenting a worker, on demand.")
print("  UNATTENDED — runs on a schedule/event, HEADLESS, nobody present. Value =")
print("               lights-out processing of volume.")
print("\nGet it wrong and you cap the value: building an overnight 10k-invoice batch as")
print("an ATTENDED robot means someone has to be at a desk to start it — you've thrown")
print("away the 'lights-out' benefit. Match the robot type to whether a human is in")
print("the loop, and unattended + queues (next lab) is how volume actually scales.")
EOF
```

**Expected result:** Real-time human-assist scenarios assigned to attended robots and scheduled lights-out volume assigned to unattended, on the question of whether a human is in the loop. The attended-versus-unattended lesson is to match the robot type to the work — building lights-out volume as an attended robot throws away the unattended benefit by requiring someone at a desk.

**Negative test:** Building an overnight high-volume batch as an attended robot. It requires a human to trigger it, defeating the lights-out purpose — high-volume, no-human-present work is unattended by definition.

**Cleanup:** None.

### Lab 5.2 — Queue throughput: decouple work from workers

**Objective:** See how a queue plus a robot pool scales volume automation.

```bash
python3 - <<'EOF'
ITEMS = 10000
SECONDS_PER_ITEM = 18
def duration(robots):
    total_robot_seconds = ITEMS * SECONDS_PER_ITEM
    return total_robot_seconds / robots / 3600   # hours, parallel across robots
print(f"{ITEMS} invoices, {SECONDS_PER_ITEM}s each. Queue + a pool of unattended robots:\n")
print(f"   {'robots':>8}{'hours':>10}")
for r in [1, 2, 5, 10, 20]:
    print(f"   {r:>8}{duration(r):>10.1f}")
print("\n   1 robot:  50 hours (over two days — misses the overnight window)")
print("   10 robots: 5 hours (fits comfortably in the overnight batch)")
print("   20 robots: 2.5 hours\n")
print("The pattern: put the 10k invoices in a QUEUE as transaction items; a POOL of")
print("robots pulls items off in PARALLEL. Throughput scales ~linearly with robots —")
print("need it faster, add robots, no code change. That's DECOUPLING the work (queue)")
print("from the workers (robots).")
print("\nAnd the queue gives RELIABILITY for free: each item's status is tracked (new/")
print("in-progress/success/failed), failed items retry, and if a robot CRASHES mid-")
print("batch another robot picks up the remaining items — the work survives. Sequential")
print("processing on one robot has none of that: it's slow AND a crash loses the run.")
print("\n(The robots pull credentials from Orchestrator ASSETS/credential store at")
print("runtime — never hardcoded — so a 20-robot fleet stays governed and auditable.)")
EOF
```

**Expected result:** Queue-based processing scaling roughly linearly with the robot pool (50 hours on one robot down to a few on ten or twenty), with per-item status tracking and crash recovery. The queue lesson is to decouple the work (queue) from the workers (robots) so throughput scales by adding robots with no code change, while item-status tracking gives reliability a single sequential robot cannot.

**Negative test:** Processing a large batch sequentially on a single robot. At 50 hours it misses the overnight window, and a crash midway loses the whole run — a queue with a robot pool scales the throughput and survives crashes by tracking each item.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Attended and unattended robots distinguished by whether a human is in the loop, and matched to the work.
- [ ] Queues and transactions understood as decoupling work from workers for parallel scale and reliability.
- [ ] The REFramework recognized as the standard robust template encoding retry, exception handling, and recovery.
- [ ] Credential and asset management understood as a governance necessity for unattended robot fleets.
