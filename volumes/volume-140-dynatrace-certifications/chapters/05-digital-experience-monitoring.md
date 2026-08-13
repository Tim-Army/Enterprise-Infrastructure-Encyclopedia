# Chapter 05: Digital Experience Monitoring

## Learning Objectives

- Distinguish Real User Monitoring from Synthetic Monitoring and use each for its purpose.
- Apply user action naming rules so that sessions aggregate meaningfully.
- Use Session Replay and business events without mishandling personal data.
- Explain why DEM is its own Specialist certification.

*Exam relevance: **Digital Experience Management** is one of the six Associate domains, and the whole of the **DEM and Business Analytics Specialist** skill list: RUM (web and mobile), Session Replay, Synthetics, business events, data privacy, USQL, action/session properties, user action naming rules.*

## RUM and Synthetics

Two ways to know how the application feels to use, answering different questions:

| | **Real User Monitoring** | **Synthetic Monitoring** |
|:---|:---|:---|
| Source | Actual users, via injected JS agent or mobile SDK | Scripted checks from chosen locations |
| Answers | What is *really* happening, to whom | Is it up and correct, on a schedule |
| Coverage | Only paths users actually take | Exactly the paths you script |
| At 3 a.m. with no traffic | Silent | Still reporting |
| Detects | Real-world device, network, geography effects | Regressions in critical journeys, from outside |

Neither replaces the other, and the reason is structural: **RUM cannot tell you about an outage nobody has hit yet, and Synthetics cannot tell you about a problem you did not think to script.** A checkout flow broken for Safari-on-iOS users in Germany will be invisible to a synthetic monitor running Chrome from Virginia, and a total outage at 4 a.m. will be invisible to RUM because no real user is there to be monitored.

Private synthetic monitors run from an **ActiveGate** inside your network (Chapter 02), which is how you monitor internal applications that have no public path.

## User action naming

RUM captures **user actions** — clicks, loads, custom events. By default their names come from what happened in the browser, which produces exactly the problem you would expect:

```text
Loading of page /orders/88213/detail
Loading of page /orders/88214/detail
Loading of page /orders/88215/detail
```

Three names for one action. Aggregate across a day and you get tens of thousands of unique action names, each with a handful of samples — statistically useless and expensive.

**User action naming rules** collapse these into `Loading of page /orders/{id}/detail`. This is the same cardinality discipline that governs Prometheus labels and Loki streams, arriving from a different direction: **identifiers belong in properties, not in names.**

## Session Replay and privacy

Session Replay reconstructs what the user saw. It is the fastest way to understand a defect report and the fastest way to create a data-protection incident, and both facts are true at once.

Dynatrace's masking model offers a choice that should be made deliberately:

| Mode | Behavior | When |
|:---|:---|:---|
| **Mask all** | Everything masked unless explicitly allowed | Default; the safe starting point, especially under GDPR/HIPAA/PCI |
| **Mask user input** | Typed input masked; page content visible | Lower-sensitivity applications |

The rule worth stating without hedging: **start from mask-all and unmask deliberately.** The opposite order — start permissive, tighten after an incident — means the sensitive data has already been recorded and retained. Masking is not retroactive.

**Business events** carry business meaning (order placed, value, payment method) into Grail for analysis alongside technical telemetry. They are powerful for exactly the reason they are risky: they are the path by which commercially and personally sensitive fields enter the observability platform.

## Hands-On Lab

Python models DEM. **Cost:** none.

### Lab 5.1 — What each monitoring type can and cannot see

**Objective:** Show the complementary blind spots.

```bash
python3 - <<'EOF'
INCIDENTS = [
  # description,                                   hour, has_real_traffic, segment,            scripted
  ("checkout JS error, Safari/iOS, Germany only",    14, True,  "safari-ios-de", False),
  ("total outage, all users",                         4, False, "all",           True),
  ("payment API 500s during business hours",         11, True,  "all",           True),
  ("new signup flow broken (feature-flagged, 2%)",   15, True,  "beta-cohort",   False),
  ("TLS cert expired on the admin portal",            2, False, "internal",      True),
  ("slow images for users on mobile networks",       19, True,  "mobile-3g",     False),
]
print(f"{'incident':46}{'RUM':>6}{'SYN':>6}   why")
rum_only = syn_only = both = neither = 0
for desc, hour, traffic, seg, scripted in INCIDENTS:
    rum = traffic
    syn = scripted
    why = []
    if not traffic: why.append("no live users at that hour")
    if not scripted: why.append("segment not scripted")
    if rum and syn: both += 1
    elif rum: rum_only += 1
    elif syn: syn_only += 1
    else: neither += 1
    print(f"{desc:46}{'YES' if rum else '--':>6}{'YES' if syn else '--':>6}   {'; '.join(why) or 'both cover it'}")

print(f"\nRUM only: {rum_only}   Synthetic only: {syn_only}   Both: {both}   Neither: {neither}")
print("\nThe two failure classes are structurally different:")
print("  synthetics MISS what you did not think to script (narrow segments, new flows)")
print("  RUM MISSES what no user has hit yet (overnight outages, expired certs)")
print("\nNeither gap is closable from inside the other tool. Running only one is")
print("choosing which class of incident you would rather find out about from a customer.")
EOF
```

**Expected result:** Three incidents are RUM-only, two synthetic-only, one covered by both. The framing matters more than the tally: these are not overlapping tools with different coverage percentages but tools with *categorically* different blind spots, so the choice to run one is a choice about which incidents reach you by complaint.

**Negative test:** Dropping synthetics because "we have real user data now." The 4 a.m. outage and the expired certificate both go undetected until morning.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — User action naming and cardinality

**Objective:** Collapse per-record action names into analyzable ones.

```bash
python3 - <<'EOF'
import re, collections, random
random.seed(5)
raw = []
for _ in range(20000):
    r = random.random()
    if r < .45:  raw.append(f"Loading of page /orders/{random.randint(10000,99999)}/detail")
    elif r < .70: raw.append(f"Loading of page /users/{random.randint(1000,9999)}/profile")
    elif r < .85: raw.append(f"click on 'Add to cart' on /product/{random.randint(100,999)}")
    elif r < .95: raw.append("Loading of page /checkout")
    else:         raw.append(f"Loading of page /search?q={random.choice(['shoes','hat','bag','x'])}&p={random.randint(1,50)}")

RULES = [
  (re.compile(r"/orders/\d+/detail"),  "/orders/{id}/detail"),
  (re.compile(r"/users/\d+/profile"),  "/users/{id}/profile"),
  (re.compile(r"/product/\d+"),        "/product/{id}"),
  (re.compile(r"/search\?.*"),         "/search"),
]
def apply_rules(name):
    for rx, repl in RULES: name = rx.sub(repl, name)
    return name

before = collections.Counter(raw)
after  = collections.Counter(apply_rules(r) for r in raw)
print(f"user actions captured      : {len(raw):,}")
print(f"unique names BEFORE rules  : {len(before):,}")
print(f"unique names AFTER  rules  : {len(after):,}")
print(f"reduction                  : {(1-len(after)/len(before))*100:.2f}%\n")
print("top actions after naming rules:")
for name, n in after.most_common():
    print(f"   {n:>6,}  {name}")
thin_before = sum(1 for n in before.values() if n < 5)
thin_after  = sum(1 for n in after.values()  if n < 5)
print(f"\nBefore: {thin_before:,} of {len(before):,} names have fewer than 5 samples")
print(f"        ({thin_before/len(before)*100:.1f}%) — no percentile is meaningful on those,")
print("        and the action list is thousands of rows long and unreadable.")
print(f"After:  {thin_after} of {len(after)} names are thin; the smallest has "
      f"{min(after.values()):,} samples.")
print("\nNote /checkout survived both ways: it carries no id, so it never fragmented.")
print("The damage is confined to the PARAMETERIZED paths — which is exactly where")
print("naming rules apply, and why the fix is targeted rather than global.")
print("\nSame rule as Prometheus labels and Loki streams, from another direction:")
print("IDENTIFIERS BELONG IN PROPERTIES, NOT IN NAMES. Keep the order id as a")
print("session/action property so you can still filter to one order when you need to.")
EOF
```

**Expected result:** 20,000 raw actions collapse from 13,427 unique names to five, with essentially all of the pre-rule names holding fewer than five samples. Two details are worth noticing: `/checkout` was never fragmented because it carries no identifier, which shows the damage is confined to parameterized paths — and the closing line is the part people skip, since naming rules are not about discarding the identifier. The order ID stays available as a property, so single-order investigation still works.

**Negative test:** Solving the cardinality problem by dropping the identifier entirely. You fix the statistics and lose the ability to answer "what happened to *this* order?"

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Session Replay masking

**Objective:** Compare mask-all with permissive capture.

```bash
python3 - <<'EOF'
FIELDS = [
  # field,               sensitive, category
  ("product name",        False, "content"),
  ("search box text",     False, "input"),
  ("email address",       True,  "PII"),
  ("full name",           True,  "PII"),
  ("password field",      True,  "credential"),
  ("credit card number",  True,  "PCI"),
  ("CVV",                 True,  "PCI"),
  ("date of birth",       True,  "PII"),
  ("diagnosis notes",     True,  "PHI"),
  ("order total",         False, "content"),
  ("shipping address",    True,  "PII"),
  ("session id (cookie)", True,  "credential"),
]
def capture(mode, allowlist=()):
    rows = []
    for f, sens, cat in FIELDS:
        if mode == "mask-all":
            recorded = f in allowlist
        else:                                  # mask user input only
            recorded = cat != "input"
        rows.append((f, sens, cat, recorded))
    return rows

for mode, allow in (("mask-all", ("product name", "order total")),
                    ("mask-user-input", ())):
    rows = capture(mode, allow)
    leaked = [r for r in rows if r[1] and r[3]]
    print(f"\n=== {mode} ===")
    for f, sens, cat, rec in rows:
        mark = "RECORDED" if rec else "masked"
        warn = "   <-- SENSITIVE DATA CAPTURED" if (sens and rec) else ""
        print(f"   {f:20} {cat:11} {mark:9}{warn}")
    print(f"   sensitive fields recorded: {len(leaked)}")

print("\nmask-all records 2 harmless fields you explicitly allowed.")
print("mask-user-input records 6 sensitive fields you never decided to record —")
print("including PCI and PHI data, because they are page CONTENT rather than typed input.")
print("\nThat is the trap: 'mask user input' sounds comprehensive and is not. Sensitive")
print("data is frequently DISPLAYED, not typed — an order confirmation screen shows the")
print("address and card suffix without the user entering anything.")
print("\nAnd masking is NOT RETROACTIVE. Starting permissive and tightening later means")
print("the data was already captured and retained. Start from mask-all; unmask on purpose.")
EOF
```

**Expected result:** Mask-all records two deliberately allowed fields; mask-user-input silently records six sensitive ones including PCI and PHI. The reason is the part worth internalizing — sensitive data is frequently *displayed* rather than typed, so a mode that masks input only feels safe while capturing confirmation screens in full.

**Negative test:** Enabling Session Replay with input masking on a healthcare or payments application and assuming compliance. The diagnosis notes and the card summary were both page content.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] RUM and Synthetic monitoring matched to their structurally different blind spots.
- [ ] User action naming rules applied, with identifiers kept as properties.
- [ ] Session Replay configured mask-all first, unmasked deliberately.
- [ ] Business events understood as both powerful and a sensitive-data pathway.
