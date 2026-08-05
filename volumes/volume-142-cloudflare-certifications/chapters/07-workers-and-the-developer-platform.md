# Chapter 07: Workers and the Developer Platform

## Learning Objectives

- Explain the Workers execution model and how isolates differ from containers.
- Choose among the platform's storage options by consistency and access pattern.
- Recognize when edge compute fits — and when it does not.
- Connect the developer platform to the announced Accredited Workers Developer track.

*Exam relevance: peripheral to both current Associate exams but foundational context — Workers appear wherever edge logic does (custom security responses, request rewriting), and the **Accredited Workers Developer** partner track was announced as in development at verification. This chapter positions the platform; it is not a JavaScript course.*

## The Workers model

**Workers** run your code in every edge location, in **V8 isolates** rather than containers:

| | Container/function (typical serverless) | **Workers isolate** |
|:---|:---|:---|
| Cold start | Tens to hundreds of ms — a runtime boots | **Milliseconds** — the runtime is already resident; only your isolate is created |
| Deployed to | A region you choose | **Every edge location**, automatically |
| State | Local disk, memory per instance | Stateless; state lives in platform services |
| Scaling unit | Instances | Requests |

The two consequences worth internalizing: **there is no region to pick** (the deployment question from Chapter 02 stays answered), and **the cold-start class of problem largely disappears** — an isolate spins up in less time than a TLS handshake, which is why per-request edge logic is affordable at all.

The constraint that pays for this: Workers are **stateless and short-lived**. Long computations, large memory, and local persistence are the wrong shape. Edge compute complements origin compute; it does not replace it.

## Storage on the platform

| Service | Model | Right for | Wrong for |
|:---|:---|:---|:---|
| **KV** | Key-value, **eventually consistent**, read-optimized | Config, feature flags, cached lookups read everywhere | Anything needing read-after-write guarantees |
| **R2** | Object storage, S3-compatible API | Assets, backups, large blobs — with **no egress fees** as its headline economics | Queryable structured data |
| **D1** | SQLite-based relational | Structured data with real queries | Massive write concurrency |
| **Durable Objects** | Single-instance coordination points with storage | Counters, locks, sessions — when *one* authoritative copy must exist | Fan-out read scale |

The KV row carries the exam-grade concept: **eventual consistency is a contract, not a defect.** A feature flag flipped in KV propagates over seconds; code that writes a value and immediately reads it back may see the old one. Durable Objects exist precisely for the cases where that is unacceptable — they trade global replication for a single authoritative instance.

## Where edge compute fits

Good fits share a shape — small logic, per-request, benefiting from running *before* traffic crosses the ocean: header and cookie manipulation, A/B assignment, auth token verification, custom security responses, API composition, serving from KV/R2 without an origin at all.

Poor fits share the opposite shape: long-running jobs, heavy computation, large working sets, chatty transactions against a distant single-region database — the last being the classic trap, where moving compute to the edge *adds* a hundred round trips to the region the data never left.

## Hands-On Lab

Python models the platform's trade-offs. **Cost:** none. (The Workers free tier is generous; the real thing is an afternoon.)

### Lab 7.1 — Isolates and the cold-start budget

**Objective:** Compare startup economics at request scale.

```bash
python3 - <<'EOF'
import random
random.seed(7)
REQ = 100_000
COLD_SHARE = 0.03                      # 3% of requests land on a cold instance
MODELS = {
  "regional function (container)": {"cold_ms": 250, "warm_ms": 3, "extra_rtt_ms": 90},
  "edge worker (isolate)":         {"cold_ms": 5,   "warm_ms": 0.5, "extra_rtt_ms": 0},
}
print(f"{'model':32}{'p50 overhead':>13}{'p99 overhead':>13}   note")
for name, m in MODELS.items():
    samples = []
    for _ in range(REQ):
        cold = random.random() < COLD_SHARE
        samples.append((m["cold_ms"] if cold else m["warm_ms"]) + m["extra_rtt_ms"])
    samples.sort()
    p50, p99 = samples[REQ//2], samples[int(REQ*.99)]
    note = "cold starts live in the tail; distance lives everywhere" if "container" in name else \
           "runtime resident at every edge; nothing to boot, nowhere to travel"
    print(f"{name:32}{p50:>11.1f}ms{p99:>11.1f}ms   {note}")

print("\nTwo separate wins are conflated in 'edge is fast':")
print("  1. COLD STARTS: isolate creation is ~ms, so the 3% cold tail costs almost")
print("     nothing — the container model's p99 is dominated by boots.")
print("  2. DISTANCE: the worker runs where the request ARRIVED. The container adds")
print("     a fixed ~90ms round trip to its region for every request, cold or warm.")
print("\nFor auth-check-sized logic the second win is usually the bigger one — and")
print("it is also the one that reverses (Lab 7.3) when the DATA stays regional.")
EOF
```

**Expected result:** The container model's p99 is boot-dominated while its p50 is distance-dominated; the isolate model shows near-zero for both. The decomposition is the takeaway — "edge is fast" bundles a cold-start win and a proximity win, and Lab 7.3 shows the proximity win turning into a penalty the moment the data does not move with the compute.

**Negative test:** Quoting the isolate numbers for a workload that then calls a single-region database four times. The compute moved; the latency stayed with the data.

**Cleanup:** None.

### Lab 7.2 — KV's eventual consistency, observed

**Objective:** See what the consistency contract actually permits.

```bash
python3 - <<'EOF'
import random
random.seed(3)
PROPAGATION_S = 12                     # value settles globally within ~seconds
flag_writes = [(0, "checkout_v2", "off"), (300, "checkout_v2", "ON")]

def read_at(t, location_offset):
    """Each edge location sees the new value after its own propagation delay."""
    current = "off"
    for wt, k, v in flag_writes:
        if t >= wt + location_offset:
            current = v
    return current

print("t=300s: operator flips checkout_v2 to ON in KV\n")
print(f"{'t (s)':>7}{'edge A (+2s)':>14}{'edge B (+7s)':>14}{'edge C (+11s)':>15}   world state")
for t in (299, 301, 304, 308, 312):
    a, b, c = read_at(t, 2), read_at(t, 7), read_at(t, 11)
    state = "consistent" if a == b == c else "MIXED — both versions live simultaneously"
    print(f"{t:>7}{a:>14}{b:>14}{c:>15}   {state}")

print("\nFor a FEATURE FLAG the mixed window is harmless: some users get the new")
print("checkout a few seconds early. That is the contract working as designed.")
print("\nWhere the same window is NOT harmless:")
print("   - a kill switch for a security rule (seconds of partial enforcement)")
print("   - anything read-after-write ('create then immediately fetch')")
print("   - a counter (concurrent increments at two edges lose updates)")
print("\nThose cases are what Durable Objects are FOR: one authoritative instance,")
print("strongly consistent, at the cost of every request traveling to it. Choose")
print("per datum: flags in KV, locks and counters in Durable Objects — the wrong")
print("choice in either direction is either a correctness bug or a latency tax.")
EOF
```

**Expected result:** A ~10-second window where three edges disagree about the flag, labeled explicitly as the contract rather than a malfunction. The three not-harmless cases are the judgment content — the same propagation window that is fine for a flag is a correctness bug for a counter, and the storage choice is made per datum, not per application.

**Negative test:** Implementing a distributed rate-limit counter in KV. Two edges increment concurrently, one update wins, and the limit quietly under-counts — the failure leaves no error, only a limit that does not limit.

**Cleanup:** None.

### Lab 7.3 — When edge compute helps, and when it backfires

**Objective:** Decide placement by where the data lives.

```bash
python3 - <<'EOF'
USER_TO_EDGE_MS = 15
EDGE_TO_REGION_MS = 90
WORKLOADS = [
  # name,                          db_calls, data_at_edge
  ("verify JWT + route",                 0,  True),
  ("serve config from KV",               0,  True),
  ("A/B assign + rewrite",               0,  True),
  ("product page (1 DB read, cached)",   1,  False),
  ("checkout (4 sequential DB calls)",   4,  False),
]
print(f"{'workload':34}{'at edge (ms)':>13}{'at origin (ms)':>15}   verdict")
for name, calls, local in WORKLOADS:
    edge   = USER_TO_EDGE_MS + (0 if local else calls * 2 * EDGE_TO_REGION_MS)
    origin = USER_TO_EDGE_MS + EDGE_TO_REGION_MS + calls * 2 * 2   # db is ~2ms away locally
    v = "EDGE — logic travels well" if edge < origin else "ORIGIN — the data did not move; follow it"
    print(f"{name:34}{edge:>13}{origin:>15}   {v}")

print("\ncheckout at the edge: 4 sequential DB calls x 180ms round trip = 735ms of")
print("pure geography, versus ~121ms running NEXT TO the database. Moving compute")
print("to the edge moved it AWAY from the data — the proximity win from Lab 7.1")
print("ran in reverse.")
print("\nThe placement rule in one line: put compute next to what it talks to most.")
print("Talks to the USER (headers, auth, flags)     -> edge.")
print("Talks to the DATABASE (transactions, joins)  -> origin.")
print("Talks to both -> split it: the edge half handles the user-facing part and")
print("makes ONE call to the origin half, not four.")
EOF
```

**Expected result:** The three data-local workloads win at the edge decisively; the four-call checkout is roughly six times *slower* there. The one-line rule — compute next to what it talks to most — resolves every row, and the split pattern in the last lines is how real applications get both halves right.

**Negative test:** Moving an API to Workers for the latency win without moving or caching its data. The benchmark from one region away improves; users across the ocean from the database get the geography bill fourfold.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Isolate economics understood as two separate wins: cold starts and proximity.
- [ ] Storage chosen per datum: KV for propagation-tolerant reads, Durable Objects for authority, R2 for objects, D1 for queries.
- [ ] Eventual consistency treated as a contract with named unacceptable cases.
- [ ] Compute placed next to what it talks to most — split when it talks to both.
