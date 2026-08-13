# Chapter 08: Akamai Cloud and Automation

## Learning Objectives

- Explain Akamai Cloud (the Linode lineage) and its edge-adjacent positioning.
- Read the Cloud Computing Foundations Certification's scope.
- Automate Akamai configuration with the API, CLI, Terraform, and Pipeline.
- Apply config-as-code discipline to an estate where config is enforcement.

*Cert/course relevance: **Akamai Cloud Computing Foundations Certification** (Foundational, Paid) and the **Akamai Automation and DevOps** course (Akamai API, CLI, Pipeline, workflow automation).*

## Akamai Cloud

Akamai acquired Linode and grew it into **Akamai Cloud** — a compute/storage cloud positioned as **distributed and edge-adjacent** rather than a hyperscaler clone. The pitch is proximity: compute in more, smaller locations, close to users and close to Akamai's delivery edge, for workloads that benefit from being near the request.

The **Cloud Computing Foundations Certification** — notably the one Akamai credential titled "Certification" at the foundational level, and marked Paid — scopes to "basic cloud computing concepts, exposure to Akamai's cloud computing platform, and knowledge around Akamai's cloud computing solutions." It is a concepts-and-platform-orientation credential, not a deep architecture exam; read the level band honestly and plan accordingly.

The realistic placement against the cloud volumes on this shelf ([AWS XVII](../../volume-017-aws-architecture-security/README.md), [Azure XXXIII](../../volume-033-microsoft-azure-certifications/README.md), [GCP XXXIV](../../volume-034-google-cloud-certifications/README.md), [Alibaba LXXXII](../../volume-082-alibaba-cloud-certifications/README.md)): Akamai Cloud is not competing to be your everything-cloud. It competes for the **latency-sensitive, distribution-heavy** slice — the workloads where being near the user beats being near the other services — which is the same edge-compute placement argument [Volume CXLII's Workers chapter](../../volume-142-cloudflare-certifications/chapters/07-workers-and-the-developer-platform.md) makes, at VM/container scale rather than isolate scale.

## Automation

The **Automation and DevOps** course names the toolchain: **Akamai API, Akamai CLI, Akamai Pipeline**, and workflow automation. The through-line is identical to [New Relic's fixtures chapter](../../volume-141-newrelic-certifications/chapters/08-service-levels-and-automation.md) and [Cloudflare's operations chapter](../../volume-142-cloudflare-certifications/chapters/08-operating-cloudflare-api-terraform-and-logs.md), and it lands with the same weight it did for Cloudflare: **on this platform, configuration is enforcement.** A drifted property rule is a security or availability change; a click-built config cannot be reviewed or reproduced across the staging/production networks Chapter 02 described.

Akamai's specific tools:

| Tool | For |
|:---|:---|
| **Akamai API** (OPEN APIs) | Everything programmatic — properties, security configs, GTM, purge |
| **Akamai CLI** | Command-line access to the APIs, scriptable |
| **Terraform provider** | Declarative property/security/GTM config as code |
| **Akamai Pipeline** | Promote a property config across environments (dev → staging → prod) systematically |

**Pipeline** is the Akamai-specific piece worth knowing: it formalizes promoting one property configuration through a chain of environments, which is config-as-code fitted to the property/version/activation model rather than bolted beside it.

## Hands-On Lab

Python models automation discipline. **Cost:** none.

### Lab 8.1 — Where Akamai Cloud fits

**Objective:** Place workloads by what they talk to most.

```bash
python3 - <<'EOF'
WORKLOADS = [
  # name,                          user_latency_critical, talks_to_hyperscaler_services, data_gravity
  ("image/video transform at edge",     True,  False, "none — stateless"),
  ("API gateway near users",            True,  False, "light"),
  ("real-time bidding responder",       True,  False, "in-memory"),
  ("data warehouse + BI",               False, True,  "huge — years of data in S3/BigQuery"),
  ("ML training",                       False, True,  "huge — on hyperscaler GPUs"),
  ("regional cache/compute tier",       True,  False, "cached"),
]
print(f"{'workload':34}{'user-latency':>13}{'ties to hyperscaler':>21}   fit")
for name, lat, hyper, gravity in WORKLOADS:
    if hyper: fit = "hyperscaler — data/service gravity wins"
    elif lat: fit = "AKAMAI CLOUD — near users, edge-adjacent"
    else:     fit = "either"
    print(f"{name:34}{'yes' if lat else 'no':>13}{'yes' if hyper else 'no':>21}   {fit}")
print("\nSame placement logic as edge COMPUTE (Vol CXLII ch07), one tier up at")
print("VM/container scale: put the workload near what it talks to MOST.")
print("  talks to USERS, stateless/cached  -> Akamai Cloud's distribution wins")
print("  talks to a hyperscaler's DATA/GPUs -> follow the data; distance to users")
print("     is the smaller cost")
print("\nAkamai Cloud is not the everything-cloud and the Foundations cert does not")
print("claim it is. It is the latency-and-distribution play. Placing the BI")
print("warehouse there — miles from its data lake — repeats the checkout-at-the-edge")
print("mistake from Vol CXLII: compute moved away from the data it lives on.")
EOF
```

**Expected result:** Latency-critical stateless workloads fit Akamai Cloud; data-gravity workloads stay on the hyperscaler holding their data. The placement rule is the same "compute next to what it talks to most" from the edge-compute chapter, one tier up — and the BI-warehouse counter-example is the same mistake in cloud clothing.

**Negative test:** Migrating everything to Akamai Cloud for "edge benefits." The workloads tied to hyperscaler data pay a distance tax for a proximity they do not use.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Pipeline promotion across environments

**Objective:** Model config promotion versus per-environment hand edits.

```bash
python3 - <<'EOF'
BASE_CONFIG = {
  "caching": "static 7d, html no-store",
  "waf": "AAP evaluate",
  "origin": "PLACEHOLDER",       # per-environment
  "gtm": "single-dc",
}
ENVIRONMENTS = {
  "dev":     {"origin": "dev-origin.internal",  "waf": "AAP evaluate"},
  "staging": {"origin": "stg-origin.internal",  "waf": "AAP evaluate"},
  "prod":    {"origin": "prod-origin.internal", "waf": "AAP enforce", "gtm": "multi-dc-failover"},
}
print("Akamai Pipeline: one BASE config, per-environment OVERRIDES only.\n")
for env, overrides in ENVIRONMENTS.items():
    cfg = dict(BASE_CONFIG); cfg.update(overrides)
    diffs = ", ".join(f"{k}={v}" for k, v in overrides.items())
    print(f"  {env:8}: {diffs}")
print("\nThe caching and base WAF rules are DEFINED ONCE and promoted. Only origin,")
print("enforce-mode, and GTM differ — and those differences are DECLARED, in code,")
print("reviewable in a diff.\n")
print("The hand-edited alternative, and why it drifts:")
print("  each environment configured separately in the UI -> caching rules diverge")
print("  as people tweak one and forget the others -> staging stops predicting prod")
print("  -> the whole point of staging (Chapter 02) quietly dies")
print("\nPipeline makes the environments PROVABLY the same except where declared")
print("different. That is what lets staging's green result mean prod will be green —")
print("config-as-code fitted to the property/version/activation model, not beside it.")
EOF
```

**Expected result:** One base config promoted across three environments with declared per-environment overrides, versus hand edits that let staging and production diverge. The staging-integrity link is the payoff — Chapter 02's staging gate only predicts production if the two are provably identical except where deliberately differing, which is exactly what Pipeline enforces.

**Negative test:** Configuring dev, staging, and prod independently in the UI. Within a quarter their caching rules differ in ways nobody tracked, and a staging pass no longer means anything about production.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Config-as-code because config is enforcement

**Objective:** Diff intended against live on an Akamai estate.

```bash
python3 - <<'EOF'
INTENDED = {
  "property:www / caching":      "static 7d",
  "property:www / waf":          "AAP enforce",
  "property:www / origin-lock":  "Site Shield ranges only",
  "gtm:checkout":                "multi-dc, 30s probe",
  "security:rate-login":         "10/min per ip+user",
}
LIVE = {
  "property:www / caching":      "static 7d",
  "property:www / waf":          "AAP EVALUATE",                 # dropped to eval during an incident
  "property:www / origin-lock":  "Site Shield + office /24",     # debug exception, still there
  "gtm:checkout":                "multi-dc, 120s probe",         # loosened during a flap
  "security:rate-login":         "10/min per ip+user",
  "property:legacy / waf":       "none",                          # unmanaged property, no protection
}
print("terraform plan (Akamai provider):\n")
findings = 0
for k in sorted(set(INTENDED) | set(LIVE)):
    i, l = INTENDED.get(k), LIVE.get(k)
    if i == l: continue
    findings += 1
    kind = "UNMANAGED" if i is None else ("MISSING" if l is None else "DRIFTED")
    print(f"  {kind:10} {k}")
    if i and l: print(f"             intended {i!r} -> live {l!r}")
RISK = {
  "property:www / waf": "WAF in evaluate = NOT ENFORCING; attacks pass, logged only",
  "property:www / origin-lock": "office /24 bypasses the whole edge for anyone on it",
  "gtm:checkout": "failover 4x slower than intended (Chapter 02's arithmetic)",
  "property:legacy / waf": "a live property with ZERO protection, in no code",
}
print(f"\n{findings} findings, each a security/availability change on a security platform:")
for k, r in RISK.items(): print(f"  - {k}: {r}")
print("\nThe evaluate-mode WAF is the sharp one: it LOOKS configured (rules present,")
print("logs flowing) and enforces NOTHING. A dashboard glance passes; only the diff")
print("against intended catches it. Apply the code and enforcement returns.")
print("\nScheduled `terraform plan` alerting on non-empty diffs is the whole control —")
print("identical to Vols CXLI/CXLII, and it matters MORE here because more of the")
print("config is directly a security boundary.")
EOF
```

**Expected result:** Four findings including a WAF silently in evaluate mode and an unmanaged legacy property with no protection at all. The evaluate-mode case is the sharpest — configured-looking but enforcing nothing — and it is invisible to everything except a diff against declared intent, which is why config-as-code matters most on a platform where config *is* the security boundary.

**Negative test:** Auditing the Akamai estate by clicking through the UI quarterly. The evaluate-mode WAF looks fully configured; only the diff reveals it stopped enforcing.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Akamai Cloud placed as the latency/distribution play, not an everything-cloud.
- [ ] The Cloud Computing Foundations Certification read at its foundational scope.
- [ ] The automation toolchain (API, CLI, Terraform, Pipeline) applied, with Pipeline promoting configs.
- [ ] Config-as-code and scheduled drift detection applied, because config is enforcement.
