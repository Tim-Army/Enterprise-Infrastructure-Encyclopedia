# Chapter 03: WAF, Rules, and Rate Limiting

## Learning Objectives

- Deploy the WAF's managed rulesets and know what tuning them means.
- Write custom rules and reason about evaluation order and actions.
- Configure rate limiting that stops abuse without rationing real users.
- Roll out enforcement the defensible way: log first, measure, then block.

*Exam relevance: core Application Security Associate territory. This chapter is **defensive** throughout — configuring protections, measuring their precision, and remediating; never crafting attacks.*

## The WAF

Cloudflare's WAF inspects proxied HTTP requests at the edge and applies three layers, in evaluation order:

| Layer | What it is | You tune by |
|:---|:---|:---|
| **Managed rulesets** | Cloudflare-maintained rules for known attack classes (injection, XSS, RCE patterns) plus emergency rules pushed during active campaigns | Enabling/disabling rules, overriding actions per rule |
| **Custom rules** | Your expressions over request fields — path, method, headers, country, bot score | Writing them; ordering them |
| **Rate limiting rules** | Thresholds per key (IP, header, cookie) over a window | Choosing the key, threshold, window, and action |

Actions escalate: **log** (count it), **challenge** (interactive or managed challenge), **block**. The action ladder is the rollout mechanism, and the discipline from [Volume CXL's blocking chapter](../../volume-140-dynatrace-certifications/chapters/07-application-security.md) transfers whole: **a false positive in log mode is a line in a report; in block mode it is a customer turned away.** Measure precision on real traffic before enforcing.

## Custom rules: order and first match

Custom rules evaluate in order, and the first matching **terminating** action wins. The failure mode is the same one [GitLab's `rules:` model](../../volume-136-gitlab-certifications/README.md) exhibits in CI: **a broad early rule shadows a precise later one.** An `allow` for "our office IP range" placed above a block for "requests with attack-pattern payloads" exempts the office from the WAF — including the day a laptop on the office network is compromised. Order allows narrow-and-specific first, broad-and-permissive last, and audit any allow that precedes a block.

## Rate limiting

Rate limiting counts requests per **key** within a **window** and acts past a **threshold**. Every design choice is a trade:

- **Key on IP** is simple and collapses under CGNAT and corporate egress, where one IP is thousands of users — threshold too low and you ration an office; too high and a single-source scraper never trips it.
- **Key on something identity-shaped** (session cookie, API token) tracks actual actors but only exists after authentication.
- **The window shapes burst tolerance.** 600/minute admits a 600-request burst in one second; 10/second smooths it but punishes legitimate bursts like a page loading forty assets.

The right configuration starts from the question "what does *legitimate* peak usage look like for this endpoint?" — measured, not guessed — and sets thresholds above it with margin. Login and password-reset endpoints get their own, much stricter rules, because their abuse case (credential stuffing) is high-value and their legitimate rate is tiny.

## Hands-On Lab

Python models WAF behavior. **Cost:** none. All labs are defensive.

### Lab 3.1 — Rule order: the shadowing audit

**Objective:** Find the allow that swallows the block.

```bash
python3 - <<'EOF'
RULES = [
  # order, expression,                                action,     terminating
  (1, "ip.src in OFFICE_RANGE",                       "allow",    True),
  (2, "uri.path contains '/admin'",                   "block",    True),
  (3, "cf.threat_score > 40",                         "challenge",True),
  (4, "uri.path contains '/api/' and not has_token",  "block",    True),
]
REQUESTS = [
  ("attacker probing /admin from botnet",     {"office": False, "path": "/admin", "threat": 60, "token": False}),
  ("employee reaching /admin from office",    {"office": True,  "path": "/admin", "threat": 5,  "token": True}),
  ("compromised office laptop hitting /admin",{"office": True,  "path": "/admin", "threat": 70, "token": False}),
  ("tokenless scraper on /api/products",      {"office": False, "path": "/api/products", "threat": 20, "token": False}),
]
def evaluate(req):
    for order, expr, action, term in RULES:
        hit = (("OFFICE_RANGE" in expr and req["office"]) or
               ("/admin" in expr and "/admin" in req["path"]) or
               ("threat_score" in expr and req["threat"] > 40) or
               ("/api/" in expr and "/api/" in req["path"] and not req["token"]))
        if hit and term:
            return order, expr, action
    return None, "(no match)", "default allow"

print(f"{'request':44}{'rule':>5}{'action':>11}")
for name, req in REQUESTS:
    order, expr, action = evaluate(req)
    flag = "   <-- PROBLEM" if "compromised" in name and action == "allow" else ""
    print(f"{name:44}{str(order):>5}{action:>11}{flag}")

print("\nRule 1 allows ALL office traffic before any inspection. The compromised")
print("laptop inherits the exemption: threat score 70, no token, hitting /admin —")
print("allowed, because first terminating match wins and rule 1 fired first.")
print("\nThe fix is ordering AND narrowing:")
print("   - move specific blocks ABOVE broad allows")
print("   - or narrow the allow: office range AND path in the two endpoints that")
print("     actually need the exemption — an allow is a hole; size it to its purpose")
print("\nAudit rule for any WAF: list every allow, and for each, name what it is")
print("exempting from inspection and why that is acceptable. 'It was easier' is")
print("the most common answer and never an acceptable one.")
EOF
```

**Expected result:** The compromised office laptop reaches `/admin` with a threat score of 70 because the broad allow at position 1 terminates evaluation. The audit rule at the end is the reusable tool: every `allow` is a documented hole or an undocumented one, and the difference is whether anyone can answer "exempting what, from what, why?"

**Negative test:** Fixing this by deleting the allow entirely and breaking a legitimate internal tool that needed it. The answer is narrowing, not oscillating between too-broad and absent.

**Cleanup:** None.

### Lab 3.2 — Log, measure, then block

**Objective:** Run the enforcement rollout with numbers.

```bash
python3 - <<'EOF'
import random
random.seed(17)
DAILY = 1_500_000
# Managed ruleset in LOG mode for two weeks; each rule's matches examined
RULES_OBSERVED = [
  # rule,                          matches/day, true_positive_rate
  ("SQLi patterns (core)",              2200,   0.96),
  ("XSS patterns (core)",               1400,   0.93),
  ("RCE / code injection",               310,   0.98),
  ("generic anomaly scoring",           9800,   0.31),
  ("legacy app rule (old CVE)",           45,   0.99),
]
print("Two weeks in LOG mode produced this evidence:\n")
print(f"{'rule':28}{'matches/day':>12}{'precision':>11}   decision at go-live")
for rule, m, tp in RULES_OBSERVED:
    fp_day = m * (1 - tp)
    if tp >= 0.95:      d = "BLOCK — precision earned it"
    elif tp >= 0.90:    d = f"CHALLENGE — {fp_day:,.0f} FPs/day get a challenge, not a wall"
    else:               d = f"keep LOGGING — {fp_day:,.0f} FPs/day would be turned-away users"
    print(f"{rule:28}{m:>12,}{tp*100:>10.0f}%   {d}")

anomaly_fp = 9800 * (1 - 0.31)
print(f"\nThe anomaly rule alone would have rejected ~{anomaly_fp:,.0f} legitimate requests")
print("per day if enabled in block mode on day one — invisible in log mode, an")
print("incident channel full of angry tickets in block mode.")
print("\nThe ladder: LOG (measure) -> CHALLENGE (friction for the uncertain) ->")
print("BLOCK (only where precision is proven). Challenges are the WAF's middle gear:")
print("a real user passes one in seconds; most automation does not.")
EOF
```

**Expected result:** Three rules earn block mode, one earns a challenge, and the anomaly rule — which *sounds* most protective — would have rejected ~6,800 legitimate requests daily. The challenge action is the underused middle: it converts "not sure" from a blocking decision into a friction decision, which is a much cheaper mistake to make.

**Negative test:** Enabling the full managed ruleset in block mode at go-live because "it's vendor-maintained." The rules are well-maintained; their fit to *your* traffic is what log mode measures, and nobody can measure it for you.

**Cleanup:** None.

### Lab 3.3 — Rate limit keys and windows

**Objective:** Set thresholds from measured legitimate behavior.

```bash
python3 - <<'EOF'
MEASURED = {                       # p99 of legitimate per-actor request rates
  "/api/search":        {"p99_per_min": 40,  "burst": "typing produces bursts"},
  "/login":             {"p99_per_min": 4,   "burst": "humans type passwords slowly"},
  "/api/products":      {"p99_per_min": 90,  "burst": "page loads fan out"},
  "/password-reset":    {"p99_per_min": 2,   "burst": "rare by nature"},
}
MARGIN = 3
print(f"{'endpoint':18}{'p99 legit/min':>14}{'limit (x3)':>12}   key + notes")
for ep, d in MEASURED.items():
    limit = d["p99_per_min"] * MARGIN
    strict = ep in ("/login", "/password-reset")
    key = "IP + session where available" if not strict else "IP AND username tried"
    note = "STRICT — abuse here is credential stuffing" if strict else d["burst"]
    print(f"{ep:18}{d['p99_per_min']:>14}{limit:>12}   {key} — {note}")

print("\nWhy margin x3 instead of setting the limit AT p99: legitimate behavior has")
print("tails the measurement window did not see — a sale, a crawler you invited, a")
print("mobile app retrying. The limit exists to stop ABUSE, which operates orders of")
print("magnitude above legitimate rates; nothing is gained by shaving the margin.")
print("\nThe CGNAT caveat: keying /api/search on IP alone at 120/min rations a")
print("thousand-employee office sharing one egress IP to 120 searches a minute")
print("TOTAL. Key on session/token where one exists; treat IP-only limits on")
print("authenticated endpoints as a smell.")
print("\nLogin is the exception in every direction: tiny legitimate rate, high-value")
print("abuse, and the right key is (IP AND the username being tried) so a spray")
print("across many accounts from one IP trips it while one user's fumbled retries")
print("do not.")
EOF
```

**Expected result:** Limits set at 3x measured p99 per endpoint, with login and password-reset governed strictly and keyed on IP-plus-username. Three ideas do the work: margin over measurement rather than guessing, keys that identify actors rather than networks, and the recognition that authentication endpoints are a different threat model wearing the same URL shape.

**Negative test:** One global rate limit "to keep things simple." It is simultaneously too loose for `/login` and too tight for `/api/products`, which is the predictable result of one number describing four behaviors.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Managed rulesets deployed through the log → challenge → block ladder, with measured precision.
- [ ] Custom rule order audited: every allow named, narrowed, and justified.
- [ ] Rate limits derived from measured legitimate p99 with margin, keyed on actors.
- [ ] Login and password-reset endpoints governed by their own strict rules.
