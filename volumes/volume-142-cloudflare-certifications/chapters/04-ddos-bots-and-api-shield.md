# Chapter 04: DDoS Protection, Bot Management, and API Shield

## Learning Objectives

- Distinguish network-layer from application-layer DDoS and how the edge handles each.
- Use bot scores as evidence, with thresholds set by consequence.
- Protect APIs with discovery, schema validation, and mutual TLS.
- Keep every enforcement decision measurable and reversible.

*Exam relevance: the remainder of Application Security Associate territory. **Defensive** throughout — absorbing, classifying, and validating; never generating attacks.*

## DDoS: two different problems sharing a name

| | **L3/4 (network)** | **L7 (application)** |
|:---|:---|:---|
| Looks like | SYN floods, UDP amplification — volume of *packets* | Floods of *valid-looking HTTP requests* |
| Defeated by | Anycast distribution + always-on packet filtering at the edge | Distinguishing malicious from legitimate *requests* |
| Cost asymmetry | Attacker cheap, absorption structural (Chapter 02's arithmetic) | Each request can be expensive at the origin (search, login, checkout) |

Network-layer floods never reach the origin on a proxied setup — they hit anycast addresses and die at the edge. The application layer is the harder half: a botnet sending plausible search queries is indistinguishable from users *per request*; classification needs signals across requests — which is exactly what Bot Management formalizes.

## Bot scores as evidence

Bot Management assigns each request a **score from 1 (definitely automated) to 99 (definitely human)**, computed from behavioral and fingerprinting signals. The score is not a verdict; it is evidence you act on in rules — and the acting is where judgment lives:

- **Consequence sets the threshold.** Checkout and login can afford to challenge aggressively — friction there is cheap relative to fraud. Public content pages cannot — challenging every marginal score on the blog costs real readers.
- **Not all bots are enemies.** Search crawlers, uptime monitors, and partner integrations are automated and welcome. Verified-bot allowances and explicit allow rules for known partners come *before* score-based enforcement, or you deindex yourself enforcing against Googlebot.
- **The challenge is the middle gear again.** Block at the confident-bot end, challenge the uncertain middle, and leave the human end alone — the same precision ladder as Chapter 03, driven by the same measurement.

## API Shield

APIs break assumptions the human-web protections rely on: no browser to challenge, no JavaScript to fingerprint, clients that are *supposed* to be automated. API Shield's answer is structural:

| Capability | Does |
|:---|:---|
| **API discovery** | Finds the API endpoints actually receiving traffic — including ones nobody documented |
| **Schema validation** | Enforces an OpenAPI schema at the edge: requests that do not match the contract never reach the origin |
| **Mutual TLS** | Only clients presenting a valid certificate connect at all |

Discovery deserves the emphasis: **you cannot validate a schema against an endpoint you do not know exists**, and shadow APIs — deployed, forgotten, unprotected — are the API equivalent of Chapter 02's gray-cloud DNS records. Same failure shape, one layer up.

## Hands-On Lab

Python models classification and validation. **Cost:** none. Defensive throughout.

### Lab 4.1 — Score thresholds by consequence

**Objective:** Set different enforcement on different endpoints from one score.

```bash
python3 - <<'EOF'
import random
random.seed(14)
def traffic(n):
    out = []
    for _ in range(n):
        if random.random() < 0.22:                      # automated share
            score = random.randint(1, 35)
            kind = "bot"
        else:
            score = random.randint(30, 99)              # humans; some look marginal
            kind = "human"
        out.append((score, kind))
    return out

POLICIES = {
  "/blog":     {"block_below": 3,  "challenge_below": 10},
  "/api/search":{"block_below": 10, "challenge_below": 30},
  "/checkout": {"block_below": 20, "challenge_below": 45},
}
t = traffic(30_000)
print(f"{'endpoint':14}{'blocked':>9}{'challenged':>12}{'humans challenged':>19}{'bots passed':>13}")
for ep, p in POLICIES.items():
    blocked    = sum(1 for s, k in t if s < p["block_below"])
    challenged = sum(1 for s, k in t if p["block_below"] <= s < p["challenge_below"])
    humans_challenged   = sum(1 for s, k in t if k == "human" and p["block_below"] <= s < p["challenge_below"])
    bots_pass  = sum(1 for s, k in t if k == "bot" and s >= p["challenge_below"])
    print(f"{ep:14}{blocked:>9,}{challenged:>12,}{humans_challenged:>19,}{bots_pass:>13,}")

print("\nOne score, three policies. /blog tolerates bots to avoid taxing readers;")
print("/checkout challenges deep into the uncertain range because friction there is")
print("cheaper than fraud. Neither policy is 'the right threshold' — each is a")
print("consequence decision made per endpoint.")
print("\nBoth error columns are visible: humans challenged (friction cost) and bots")
print("passed (leakage cost). A threshold change moves weight between them; the")
print("policy question is which cost this endpoint prefers. Watch both, always —")
print("a threshold tuned while watching only one column is optimizing half a trade.")
EOF
```

**Expected result:** Three policies with visibly different friction and leakage columns from the same score distribution. The instrument panel matters more than the numbers: every threshold buys enforcement with a mix of challenged humans and passed bots, and tuning while watching only one column is how teams "improve" into either fraud or churn.

**Negative test:** Setting one global threshold because the score is global. The score is global; the *consequences* are per-endpoint, and the policy encodes consequences.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Schema validation at the edge

**Objective:** Enforce the API contract before the origin sees the request.

```bash
python3 - <<'EOF'
SCHEMA = {   # the OpenAPI contract for POST /api/orders, abbreviated
  "required": ["item_id", "quantity"],
  "properties": {
    "item_id":  {"type": "str", "max_len": 24},
    "quantity": {"type": "int", "min": 1, "max": 100},
    "coupon":   {"type": "str", "max_len": 16},
  },
}
REQUESTS = [
  ("legit order",              {"item_id": "SKU-1142", "quantity": 2}),
  ("legit with coupon",        {"item_id": "SKU-0031", "quantity": 1, "coupon": "SUMMER26"}),
  ("negative quantity probe",  {"item_id": "SKU-1142", "quantity": -5}),
  ("oversized field probe",    {"item_id": "A"*4000, "quantity": 1}),
  ("unexpected field probe",   {"item_id": "SKU-1142", "quantity": 1, "role": "admin"}),
  ("missing required field",   {"quantity": 3}),
]
def validate(body):
    for f in SCHEMA["required"]:
        if f not in body: return f"REJECT: missing required '{f}'"
    for k, v in body.items():
        spec = SCHEMA["properties"].get(k)
        if not spec: return f"REJECT: unexpected field '{k}'"
        if spec["type"] == "int":
            if not isinstance(v, int): return f"REJECT: '{k}' wrong type"
            if not (spec["min"] <= v <= spec["max"]): return f"REJECT: '{k}'={v} out of range"
        if spec["type"] == "str":
            if not isinstance(v, str): return f"REJECT: '{k}' wrong type"
            if len(v) > spec["max_len"]: return f"REJECT: '{k}' exceeds {spec['max_len']} chars"
    return "PASS -> origin"

for name, body in REQUESTS:
    print(f"   {name:26} {validate(body)}")

print("\n4 of 6 requests never reach the origin, including the privilege-escalation")
print("probe ('role': 'admin') — rejected not because anything recognized an attack,")
print("but because the CONTRACT does not include that field. That inversion is the")
print("whole idea: enumerate what is valid and reject the rest, rather than trying")
print("to enumerate everything malicious.")
print("\nThe operational preconditions, in order:")
print("   1. DISCOVERY — you cannot validate endpoints you do not know exist")
print("   2. an accurate, current schema — a stale schema rejects legitimate new")
print("      fields, which is this feature's version of the false positive")
print("   3. the same log->enforce ladder as every other protection in this volume")
EOF
```

**Expected result:** Four probes rejected at the edge, including the `role: admin` field — refused as *outside the contract* rather than recognized as an attack. That is positive security's core trade: it needs no signature for novel probes, and it charges you an accurate schema, kept current, with the stale-schema false positive as the failure mode to manage.

**Negative test:** Enabling strict validation against a schema last updated two releases ago. The mobile app's new optional field gets rejected edge-wide, and the API team learns about schema drift from an outage.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Shadow API discovery

**Objective:** Reconcile documented endpoints against observed traffic.

```bash
python3 - <<'EOF'
DOCUMENTED = {"/api/orders", "/api/products", "/api/search", "/api/account"}
OBSERVED = {          # endpoint -> req/day seen at the edge
  "/api/orders":        48_000,
  "/api/products":     220_000,
  "/api/search":       310_000,
  "/api/account":       22_000,
  "/api/v1/orders":      1_800,   # the version nobody retired
  "/api/internal/sync":    950,   # "internal" — reachable from the internet
  "/api/debug/users":       12,   # someone's diagnostic endpoint
}
print(f"{'endpoint':22}{'req/day':>10}   status")
for ep, n in sorted(OBSERVED.items(), key=lambda kv: -kv[1]):
    if ep in DOCUMENTED:
        s = "documented, schema-validated"
    else:
        s = "*** SHADOW — receiving traffic, in no schema, no protection tuned"
    print(f"{ep:22}{n:>10,}   {s}")
shadow = [e for e in OBSERVED if e not in DOCUMENTED]
print(f"\n{len(shadow)} shadow endpoints. Each needs a decision, not a reflex:")
print("   /api/v1/orders     -> old version: migrate the 1,800 req/day, then retire")
print("   /api/internal/sync -> should never be public: Access policy or Tunnel-only")
print("                         (Chapters 05-06), then remove public exposure")
print("   /api/debug/users   -> 12 req/day of WHAT? Identify the caller before")
print("                         deleting — diagnostic endpoints have a way of being")
print("                         load-bearing for exactly one critical process")
print("\nSame failure shape as Chapter 02's gray-cloud DNS audit, one layer up:")
print("the inventory you enforce against must be DISCOVERED from reality, not")
print("copied from documentation — documentation records intentions, traffic")
print("records facts.")
EOF
```

**Expected result:** Three shadow endpoints surface, each with a different correct disposition — migration, access control, and investigation before removal. The closing parallel is the volume's recurring audit pattern: documentation-versus-reality reconciliation has now appeared for DNS records, service inventories (Vol CXL), and API surfaces, and it is the same discipline each time.

**Negative test:** Blocking all three shadow endpoints on discovery day. The 1,800 daily requests on `/api/v1/orders` belong to a paying integration that never migrated; discovery tells you what exists, not what is safe to break.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] L3/4 floods understood as structurally absorbed; L7 as a classification problem.
- [ ] Bot-score thresholds set per endpoint by consequence, watching both error columns.
- [ ] Schema validation deployed behind discovery, with stale schemas treated as the false-positive source.
- [ ] Shadow endpoints reconciled from observed traffic, with per-endpoint dispositions.
