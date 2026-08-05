# Chapter 06: Wiz Code — Shift-Left

## Learning Objectives

- Explain shift-left security and the ASPM idea.
- Understand scanning code, IaC, and secrets before deployment.
- Describe code-to-cloud tracing — connecting a cloud risk back to its source line.
- Recognize why fixing at the source beats fixing in production.

*Cert relevance: Wiz Code is the shift-left pillar — the developer/DevSecOps side of the code-to-cloud-to-runtime story.*

## Shift-left and ASPM

**Shift-left** means moving security *earlier* — from production (right) back toward development (left): catch the misconfiguration in the Terraform pull request, not in the running cloud; catch the vulnerable dependency in the build, not in the breach. **Wiz Code** is Wiz's shift-left pillar, an **ASPM** (Application Security Posture Management) capability that scans what developers produce *before* it becomes cloud:

- **Code** — application source and its dependencies (vulnerable libraries, insecure patterns).
- **IaC** — infrastructure-as-code (Terraform, CloudFormation, Kubernetes manifests) for the *same* misconfigurations CSPM would later find in the cloud, but while they are still a diff.
- **Secrets** — hardcoded credentials, API keys, and tokens committed to repositories.

The economics are the whole argument: a misconfiguration caught in a pull request is a two-minute review comment; the same misconfiguration in production is an exposure, a remediation ticket, and possibly a breach. The lab models that cost curve.

## Code-to-cloud tracing

Because Wiz Code and Wiz Cloud share the **Security Graph** (Chapter 2), Wiz can do something single-purpose scanners cannot: **trace a cloud risk back to the exact code that caused it**. A public S3 bucket in production is not just a cloud finding — Wiz can link it to the **Terraform module** and the **line** that declared `acl = "public-read"`, and to the **pull request** and **developer** that merged it. Remediation stops being "someone go fix the cloud" and becomes "fix line 42 of this module, and every environment it deploys inherits the fix."

This is the deep value of one graph over stitched-together tools: the runtime alert (Defend), the cloud posture issue (Cloud), and the source line (Code) are the same object, so you can always move from *symptom* to *root cause* to *the fix that prevents recurrence*. The lab models tracing a cloud finding to its source.

## Why source-fixing wins

Fixing in production is **whack-a-mole**: you fix the public bucket, and next week the same Terraform module spins up another public bucket, because the *source* still says public. Fixing at the source is **permanent and multiplying**: fix the module once, and every current and future deployment of it is corrected. Shift-left is not just "cheaper because earlier" — it is "durable because it fixes the *cause*, not the *instance*." The lab makes that multiplication concrete.

## Hands-On Lab

Python models shift-left economics and code-to-cloud tracing. **Cost:** none.

### Lab 6.1 — The cost curve of catching risk early

**Objective:** Quantify why catching risk left is dramatically cheaper.

```bash
python3 - <<'EOF'
# cost to remediate the SAME issue at each stage (relative effort units)
STAGES = [
  ("code review (PR)",     1,    "a review comment; fixed before merge"),
  ("CI build",             3,    "a failed check; fixed before deploy"),
  ("cloud posture (prod)", 20,   "a ticket, a change window, a re-deploy"),
  ("runtime incident",     100,  "detection, IR, possible breach + disclosure"),
]
print("SAME misconfiguration (public bucket in a Terraform module), cost by stage:\n")
print(f"   {'stage':24}{'rel. cost':>10}   what it takes")
for stage, cost, what in STAGES:
    bar = "#" * cost if cost <= 20 else "#"*20 + f" x{cost//20*5}"
    print(f"   {stage:24}{cost:>10}   {what}")
print("\n   caught in the PR:        1 unit")
print("   caught in production:   20 units  (20x)")
print("   caught as an incident: 100 units  (100x) + reputational cost")
print("\nShift-LEFT means catching it at the CODE/IaC stage — a diff, a comment, done —")
print("instead of at the CLOUD or RUNTIME stage where it's a ticket, a change window,")
print("or a breach. Wiz Code scans the Terraform/code/secrets in the pull request, so")
print("the public bucket never SHIPS. The earlier the catch, the cheaper by orders of")
print("magnitude — and the cheapest bug is the one that never reached production.")
EOF
```

**Expected result:** The same misconfiguration costing 1 unit to fix in a pull request versus 20 in production and 100 as a runtime incident. The shift-left economics are the lesson — catching risk at the code/IaC stage is orders of magnitude cheaper than in the cloud or at runtime, because Wiz Code stops the misconfiguration before it ever ships.

**Negative test:** Relying only on production CSPM to catch misconfigurations. It works, but at 20× the cost of the pull-request catch and after the exposure already existed — shift-left prevents the shipment rather than cleaning up after it.

**Cleanup:** None.

### Lab 6.2 — Code-to-cloud: trace the finding to its source

**Objective:** Connect a production cloud risk back to the line that caused it, and fix once.

```bash
python3 - <<'EOF'
# cloud findings, each linked back through the graph to its IaC source
CLOUD_FINDINGS = [
  # cloud resource,      source module,          line,  deploys_to
  ("prod-bucket-public", "modules/storage/main.tf", 42, ["prod","staging","dev"]),
  ("stage-bucket-public","modules/storage/main.tf", 42, ["prod","staging","dev"]),
  ("dev-bucket-public",  "modules/storage/main.tf", 42, ["prod","staging","dev"]),
]
print("THREE cloud findings (public buckets in prod, staging, dev):")
for res, mod, line, _ in CLOUD_FINDINGS:
    print(f"   {res:20} <- {mod}:{line}")
print("\nWhack-a-mole (fix in the cloud): fix 3 buckets by hand today...")
print("   ...and next deploy, the module spins up public buckets AGAIN. The SOURCE")
print("   still says acl = \"public-read\". You'll be back next week.\n")

# code-to-cloud: all three trace to ONE line
sources = {(m, l) for _, m, l, _ in CLOUD_FINDINGS}
print(f"Code-to-cloud tracing: all 3 findings trace to {len(sources)} source line:")
for mod, line in sources:
    envs = CLOUD_FINDINGS[0][3]
    print(f"   {mod}:{line}  ->  deploys to {envs}")
print("\nFix acl = \"public-read\" -> \"private\" on that ONE line, and:")
print("   - all 3 existing buckets get corrected on next apply")
print("   - every FUTURE environment from this module is born correct")
print("   - the fix is code-reviewed, versioned, and permanent")
print("\nThis is what ONE Security Graph buys: the cloud finding, the IaC line, and the")
print("developer who merged it are the SAME object. You move from symptom (public")
print("bucket) to ROOT CAUSE (line 42) to the fix that prevents RECURRENCE. Fixing the")
print("source is permanent and multiplies; fixing instances in the cloud is forever.")
EOF
```

**Expected result:** Three separate cloud findings all tracing to a single IaC line, so one source fix corrects every current and future deployment rather than three manual cloud fixes that regenerate next apply. The code-to-cloud lesson is that one Security Graph makes the cloud finding, the source line, and the developer the same object — enabling a permanent root-cause fix instead of whack-a-mole on instances.

**Negative test:** Fixing the three public buckets directly in the cloud. They are correct until the next `terraform apply`, when the unchanged module recreates them public — only fixing the source line stops the recurrence.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Shift-left and ASPM understood — scanning code, IaC, and secrets before they become cloud.
- [ ] Code-to-cloud tracing understood as connecting a cloud risk to its exact source line via the shared graph.
- [ ] The cost curve internalized — catching risk in a pull request is orders of magnitude cheaper than in production or at runtime.
- [ ] Source-fixing recognized as permanent and multiplying, versus whack-a-mole on cloud instances.
