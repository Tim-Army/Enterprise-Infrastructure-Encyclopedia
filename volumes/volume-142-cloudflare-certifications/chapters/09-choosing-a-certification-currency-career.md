# Chapter 09: Choosing a Certification, Currency, and Career

## Learning Objectives

- Choose between the two Associate exams by product family, not by guesswork.
- Prepare for a young program from what actually exists: the free tier and the documentation.
- Place Cloudflare among the encyclopedia's edge, SSE, and zero-trust volumes.
- Track a program that will look different at every currency check.

## Choosing

The two exams split cleanly along the product families:

| If your work is… | Take | This volume's chapters |
|:---|:---|:---|
| WAF, DDoS, bots, APIs — protecting *applications* | **Application Security Associate** | 02–04 |
| Access, Gateway, WARP, Tunnel — protecting *people and connectivity* | **Zero Trust Associate** | 05–06 |

Both exams sit on the same substrate (Chapter 02), and Cloudflare's own guidance is the published prerequisite: hands-on experience with the products is "highly recommended." For engineers doing both — common in smaller teams, where the same person runs the WAF and the Access policies — the Connect 2026 bundle's one-attempt-at-both structure is unusually well shaped, and its $495 price includes the training day.

**There is no Professional or Expert tier to plan a ladder around.** Two Associates is the entire certification catalog at verification. Treat any roadmap beyond that as speculation until Cloudflare publishes it.

## Preparing for a program this young

The honest preparation stack, in order of value:

1. **The free tier, with a real domain.** Nearly everything in Chapters 02–06 can be exercised on a free account: DNS and the proxy toggle, caching, WAF managed rules, rate limiting, Access for up to 50 users, Gateway DNS filtering, Tunnel, Workers. No other vendor on this shelf offers this much of the actual product for nothing — use it.
2. **The product documentation** (`developers.cloudflare.com`) — public, thorough, and the source this volume verified against. The reference architectures and learning paths are effectively the missing study guides.
3. **The exam portal** (`certifications.cloudflare.com`) for the domain outlines once you register — they exist behind the login, and they are the authoritative scope statement.
4. **Register interest.** For a program in rollout, the interest form is literally how you find out about availability.

And the standing caution, fourth vendor running: **duration, question count, passing score, validity, and standalone pricing are unpublished.** A practice-exam site quoting them for a program whose portal still says "Register Interest" is not guessing well — it is guessing conspicuously.

## Where Cloudflare sits in the encyclopedia

Three shelves intersect here:

| Shelf | Neighbors | The comparison |
|:---|:---|:---|
| **SSE / Zero Trust** | [XXXV Zscaler](../../volume-035-zscaler-zero-trust-exchange/README.md), [CXXVII Netskope](../../volume-127-netskope-certifications/README.md) | The direct rivals. Zscaler and Netskope built SSE first and retrofit developer platforms; Cloudflare built an edge network first and grew SSE onto it. Cloudflare's differentiator is the shared substrate — the same network fronts your apps (Ch 03–04), your users (Ch 05–06), and your code (Ch 07) |
| **Zero trust discipline** | [LXXXVII Microsegmentation Options](../../volume-087-microsegmentation-options/README.md) and the lab volumes XCIII–CXXI | Access/Tunnel is the *north-south* half of zero trust — user-to-app. The microsegmentation shelf is the *east-west* half — workload-to-workload. Doing one is not doing the other |
| **Edge and delivery** | [XVIII Gigamon](../../volume-018-gigamon-network-visibility/README.md), CDN material across the networking volumes | The traffic-path viewpoint |

The certification-posture comparison completes the Batch F arc: **Dynatrace** (CXL) publishes nothing; **New Relic** (CXLI) publishes everything; **Cloudflare** publishes *that the exams exist* and little else — the natural state of a program still being rolled out. Three consecutive vendors, three disclosure postures, one lesson: verify against what the vendor actually states today, because the defaults of the genre predict nothing.

## Currency

- **This volume will age faster than its neighbors.** A certification program showing "Register Interest" changes shape by the quarter: expect standalone registration, published mechanics, possibly more exams. Re-verify `certifications.cloudflare.com` and the Connect University page before relying on any program fact here.
- **The accreditation track moves too** — the Accredited Workers Developer was "in development" at verification.
- **The platform ships weekly.** Product capabilities in Chapters 02–08 are stable at the concept level; specific limits and tiers are perishable.
- **Verified 4 August 2026** from certifications.cloudflare.com (portal + exam-engine bundle), cloudflare.com/connect/cloudflare-university (Connect 2026: $495 University Pass, both exams, in-person proctored), and the Cloudflare partner-program blog (accreditations). Exam mechanics were not published and are not asserted anywhere in this volume.

## Hands-On Lab

### Lab 9.1 — Which exam, from the work

**Objective:** Map a real week onto the two exams.

```bash
python3 - <<'EOF'
WEEK = {                              # hours/week
  "WAF rules and tuning":                     6,
  "bot / fraud response":                     3,
  "API schema and shadow-endpoint work":      4,
  "Access policies and app onboarding":       7,
  "Gateway / egress policy":                  3,
  "tunnel deployment and VPN retirement":     5,
  "Workers development":                      2,
}
APPSEC = ["WAF rules and tuning", "bot / fraud response", "API schema and shadow-endpoint work"]
ZT     = ["Access policies and app onboarding", "Gateway / egress policy", "tunnel deployment and VPN retirement"]
total = sum(WEEK.values())
a = sum(WEEK[k] for k in APPSEC); z = sum(WEEK[k] for k in ZT)
print(f"{'activity':40}{'h/wk':>6}   exam")
for k, v in WEEK.items():
    tag = "AppSec" if k in APPSEC else ("ZeroTrust" if k in ZT else "(neither)")
    print(f"{k:40}{v:>6}   {tag}")
print(f"\nApplication Security-shaped: {a}/{total} ({a/total*100:.0f}%)")
print(f"Zero Trust-shaped:           {z}/{total} ({z/total*100:.0f}%)")
lead = "Zero Trust Associate" if z > a else "Application Security Associate"
print(f"\nThis week points at the {lead} first.")
print("With hours this balanced, the Connect bundle's one-attempt-at-both design")
print("is the honest answer — and either way, the 2 Workers hours count toward")
print("neither exam. That is not wasted study; it is just not CERTIFIED study,")
print("until the Workers accreditation ships.")
EOF
```

**Expected result:** A 15-vs-13-hour split pointing narrowly at Zero Trust, with the bundle flagged as the rational choice for balanced weeks. The Workers note keeps the map honest — some real work maps to no current credential, and pretending otherwise is how people study the wrong thing.

**Negative test:** Choosing by which exam sounds more senior. They are both Associates; there is nothing above them to optimize for yet.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — The free-tier practice syllabus

**Objective:** Turn the free account into the missing prep course.

```bash
python3 - <<'EOF'
plan = """
PRACTICE SYLLABUS — one free account, one spare domain, zero dollars

CH02  [ ] onboard the domain; flip a record proxied/DNS-only and observe both
      [ ] set a cache rule; measure hit ratio; purge ONE url and watch it re-fill
CH03  [ ] enable WAF managed rules in LOG mode; read a week of matches
      [ ] write one custom rule; deliberately order it wrong, observe, fix
      [ ] rate-limit a test endpoint at 3x your own measured usage
CH04  [ ] turn on bot fight mode; find your own automation in the logs
CH05  [ ] publish one app through Access; write a 2-signal policy
      [ ] issue a service token for a script; scope it; rotate it once
CH06  [ ] enable Gateway DNS filtering on one test device
      [ ] connect an origin via Tunnel; close its inbound port; verify by scanning
CH07  [ ] deploy one Worker; read a value from KV; observe propagation delay
CH08  [ ] export the zone config via API; diff it a week later

then: register interest at certifications.cloudflare.com, read the domain
outlines once registration opens, and book against what THEY say — this
syllabus is the hands-on experience the exam page recommends, not a scope map.
"""
print(plan)
print("Every box is free. The scan in CH06 is against YOUR OWN origin — verifying")
print("your own port closure is the only scanning this encyclopedia teaches.")
EOF
```

**Expected result:** A twelve-item hands-on syllabus costing nothing, explicitly framed as the recommended experience rather than a scope map. The closing note keeps the security framing exact: the one scan in the syllabus targets your own origin to verify your own closure.

**Negative test:** Substituting a third-party "Cloudflare certification course" for the free tier. The vendor gives you the actual product for nothing; a course *about* the product is a strictly worse use of the same hours.

**Rollback:** Keep the syllabus; it doubles as the practice log.

## Summary and Completion Checklist

- [ ] An exam chosen by product family, with the Connect bundle considered for balanced roles.
- [ ] Preparation built on the free tier and official documentation.
- [ ] The unpublished mechanics left unpublished — sourced from the portal after registration.
- [ ] Cloudflare placed against Zscaler/Netskope (SSE), the microsegmentation shelf (east-west), and the Batch F disclosure arc.
- [ ] A shorter re-verification cycle noted for this volume specifically.
