# Chapter 07: Rules, Transforms, Workflows, and APIs

## Learning Objectives

- Write transforms that normalize and derive identity attribute values.
- Know when a rule is required instead of a transform — and why to prefer transforms.
- Build workflows driven by event triggers.
- Use the APIs for automation and reporting.

## The engineer's chapter

This is the material that separates the two Identity Security Cloud certifications. The **Administrator** exam covers operating the platform; the **Engineer** exam adds **Architecture** and **Rules and Transforms**. The **Identity Security Expert** knowledge credential covers the same ground — transforms, rules, workflows, event triggers, APIs, and connectivity.

Four extension mechanisms, in the order you should reach for them:

| Mechanism | Runs | Use it for |
|:---|:---|:---|
| **Transform** | In the cloud, declarative JSON | Deriving/normalizing an attribute value |
| **Rule** | Java/BeanShell, often on the VA | Logic transforms cannot express (external lookups, complex branching) |
| **Workflow** | In the cloud, triggered by events | Multi-step automation and orchestration |
| **API** | Anywhere | Automation, reporting, integration |

**Prefer a transform.** Transforms are configuration: declarative, cloud-executed, versionable, and reviewable. Rules are code that must be submitted, deployed, and maintained — and cloud rules require SailPoint review. Reaching for a rule when a transform would do is the most common design mistake this chapter exists to prevent.

## Transforms

A transform computes an attribute value from other values. Common operations: `lower`, `upper`, `concat`, `substring`, `replace`, `split`, `lookup`, `dateFormat`, `firstValid`, `static`, and conditionals.

Two patterns carry most real work:

- **`firstValid`** — take the first non-empty value from an ordered list of sources (Workday email, then AD mail, then a generated default). This is how you survive incomplete source data.
- **Uniqueness generation** — build a username, then handle collisions deterministically (`jdoe`, `jdoe2`, `jdoe3`).

## Rules

Rules are code, and they run in specific contexts (connector rules on the VA, cloud rules in the tenant). They are appropriate for logic transforms genuinely cannot express — an external system lookup, elaborate branching, complex data manipulation. The cost is real: development, testing, deployment, review, and long-term maintenance, plus a debugging story that is far worse than a transform's.

## Workflows and event triggers

A **workflow** is triggered automation: an **event trigger** fires (identity created, attribute changed, access requested, certification finished), and the workflow runs steps — notify, call an HTTP endpoint, apply logic, act. Typical uses: alert the security team when someone gains privileged access, open a ticket on a mover event, post to a channel when a campaign completes.

## APIs

ISC exposes REST APIs (v3/beta) for everything the UI does: query identities, launch campaigns, manage sources, extract data for reporting. Authentication is OAuth (personal access token or client credentials). Anything you do repeatedly in the UI should eventually be an API call.

## Hands-On Lab

Python models the extension mechanisms. **Cost:** none.

### Lab 7.1 — Build transforms for attribute derivation

**Objective:** Normalize and derive attributes declaratively.

```bash
python3 - <<'EOF'
def first_valid(*values):
    for v in values:
        if v not in (None, "", "null"): return v
    return None

def generate_username(first, last, existing):
    base = (first[0] + last).lower().replace(" ", "")
    candidate, n = base, 1
    while candidate in existing:          # deterministic collision handling
        n += 1; candidate = f"{base}{n}"
    return candidate

raw = [
  {"first":"Jane","last":"Doe","wd_email":"jane.doe@corp.com","ad_mail":None},
  {"first":"John","last":"Doe","wd_email":None,               "ad_mail":"j.doe2@corp.com"},
  {"first":"Jill","last":"Doe","wd_email":None,               "ad_mail":None},
]
existing = set()
for r in raw:
    email = first_valid(r["wd_email"], r["ad_mail"], f"{r['first'].lower()}.{r['last'].lower()}@corp.com")
    uname = generate_username(r["first"], r["last"], existing); existing.add(uname)
    print(f"{r['first']:5} {r['last']:4} -> username={uname:8} email={email}")
print("\nfirstValid survives incomplete source data; uniqueness generation is deterministic and repeatable.")
EOF
```

**Expected result:** All three identities get a username and an email even though only one has a Workday address — `firstValid` falls through Workday → AD → a generated default, and the three Does become `jdoe`, `jdoe2`, `jdoe3`. Determinism matters more than elegance here: the same input must always produce the same username, or re-running aggregation creates duplicate accounts.

**Negative test:** Deriving email from a single source with no fallback — identities missing that attribute get a null email, and every downstream notification and provisioning action for them fails.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Decide: transform or rule?

**Objective:** Apply the prefer-a-transform discipline.

```bash
python3 - <<'EOF'
def choose(requirement, needs_external_lookup, needs_complex_branching, expressible_declaratively):
    if expressible_declaratively and not needs_external_lookup:
        return "TRANSFORM — declarative, cloud-executed, no deployment or review overhead"
    if needs_external_lookup:
        return "RULE — must call an external system; accept the maintenance cost"
    if needs_complex_branching:
        return "RULE — logic exceeds what transforms express"
    return "TRANSFORM"

cases = [
  ("Lowercase the email domain",              False, False, True),
  ("Department code -> cost centre (static map)", False, False, True),
  ("Look up manager in an external HR API",   True,  False, False),
  ("15-way branch on 6 attributes",           False, True,  False),
]
for req, *flags in cases:
    print(f"{req:45} -> {choose(req, *flags)}")
print("\nDefault to a transform; justify every rule. Rules are code you must maintain forever.")
EOF
```

**Expected result:** The first two resolve to transforms (even the lookup table — that is a declarative `lookup` transform), while only the external API call and the genuinely complex branching justify rules. This decision is an exam favorite because it is a real architectural judgment: teams that reach for rules by habit accumulate a codebase inside their IGA platform that nobody wants to own three years later.

**Negative test:** Writing a rule for a static department-to-cost-centre map — you have converted a two-line configuration change into a code deployment with a review cycle.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Event-triggered workflows

**Objective:** Automate a response to an identity event.

```bash
python3 - <<'EOF'
PRIVILEGED = {"Domain Admins","Treasury Ops","Payments - Approve"}

def on_access_granted(identity, access):
    steps = []
    if access in PRIVILEGED:
        steps += [f"NOTIFY security-team: {identity} granted PRIVILEGED '{access}'",
                  f"CREATE ticket: verify business justification for {identity}",
                  f"SCHEDULE event-based certification in 30 days for {identity}/{access}"]
    else:
        steps.append(f"LOG: {identity} granted '{access}' (routine)")
    return steps

def on_identity_moved(identity, old_dept, new_dept):
    return [f"TRIGGER reconcile: recompute target access for {identity}",
            f"NOTIFY {old_dept} manager: confirm revocation of departing access",
            f"SCHEDULE event-based certification: review {identity} after move to {new_dept}"]

for step in on_access_granted("Jane Doe","Domain Admins"): print(step)
print()
for step in on_identity_moved("Jane Doe","Finance","Sales"): print(step)
EOF
```

**Expected result:** Privileged grants trigger notification, a verification ticket, and a **30-day event-based certification**, while routine grants only log. The mover event triggers reconciliation plus a targeted review. Event triggers are what make governance continuous rather than annual — the privileged grant is examined within a month of happening, not at next year's campaign.

**Negative test:** Treating every grant identically — either you alert on everything and the security team tunes it out, or you alert on nothing and privileged access is invisible until the annual review.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Transforms written for normalization, `firstValid` fallback, and deterministic uniqueness.
- [ ] Transform-vs-rule decision applied, defaulting to transforms.
- [ ] Event-triggered workflows built for privileged grants and mover events.
- [ ] API role in automation and reporting understood.
