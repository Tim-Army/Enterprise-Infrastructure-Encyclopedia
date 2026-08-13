# Chapter 06: Snyk Infrastructure as Code

## Learning Objectives

- Explain IaC scanning and why the manifest is the right place to fix.
- Understand policy-as-code — security rules that live with the pipeline.
- Distinguish configuration drift from IaC-defined state.
- Recognize IaC as the fourth engine completing the supply chain.

*Cert relevance: Snyk IaC is the infrastructure engine — catching cloud misconfiguration while it is still a code diff.*

## Scanning the blueprint

**Infrastructure as Code (IaC)** declares your cloud infrastructure in files — Terraform, CloudFormation, Kubernetes manifests, ARM/Bicep — that a pipeline applies to create real resources. This means the *security posture of your cloud* is, first, the *content of these files*: an S3 bucket is public because a Terraform resource says `acl = "public-read"`; a security group is open because a rule says `0.0.0.0/0`.

**Snyk IaC** scans these files for misconfigurations **before they are applied** — the same insecure settings a cloud posture tool (CSPM) would later flag in the running cloud, but caught while they are still a **code diff in a pull request**. This is the fourth Snyk engine, completing the supply chain: [SAST (your code)](04-snyk-code-sast.md), [SCA (dependencies)](03-snyk-open-source-sca.md), [Container (the image)](05-snyk-container-and-kubernetes.md), and IaC (the infrastructure).

## Fix the blueprint, not the building

The reason to scan IaC rather than only the running cloud is the [fix-at-the-source principle](../../volume-147-wiz-certifications/chapters/06-wiz-code-shift-left.md) again: if you fix a public bucket *in the cloud console* but the Terraform still says public, the next `apply` **recreates it public**. The IaC file is the **source of truth**; fixing the running resource without fixing the file is temporary, and the drift will be "corrected" back to insecure by the next deploy.

So Snyk IaC fixes at the blueprint: change `acl = "public-read"` to `"private"` in the module, and every environment the module deploys is born correct and *stays* correct. Fixing the building while the blueprint still says otherwise is a losing game. The lab models this drift.

## Policy-as-code

The governance layer is **policy-as-code**: your organization's security rules ("no public buckets," "encryption required," "no `0.0.0.0/0` ingress except on the load balancer") expressed as **code** that runs in the pipeline, versioned alongside the infrastructure. Instead of a wiki page of standards nobody reads, the standard is a **check that fails the pull request** when violated. Policy-as-code makes security rules **executable and consistent** — the same rule enforced identically on every change, by every developer, automatically. The lab is covered within the drift exercise below.

## Hands-On Lab

Python models IaC scanning and drift. **Cost:** none.

### Lab 6.1 — Fix the blueprint or fight the drift

**Objective:** See why fixing the running cloud without fixing the IaC loses.

```bash
python3 - <<'EOF'
# the IaC file is the source of truth; the cloud is what it deploys
iac_says_public = True     # terraform: acl = "public-read"
print("Terraform module says: acl = \"public-read\"  (INSECURE)\n")

print("APPROACH A — fix the running cloud only (console: make bucket private):")
cloud_state = "private"    # you fixed it by hand
print(f"   cloud is now: {cloud_state}  ... looks fixed!")
# next deploy re-applies the IaC, which STILL says public
print("   next 'terraform apply' re-reads the file (still says public):")
cloud_state = "public" if iac_says_public else "private"
print(f"   cloud is now: {cloud_state}  <-- DRIFT CORRECTED BACK TO INSECURE")
print("   you'll fix it again, and it'll break again, forever.\n")

print("APPROACH B — fix the blueprint (Snyk IaC flags it in the PR):")
iac_says_public = False    # change the module: acl = "private"
print("   change module: acl = \"public-read\" -> \"private\", merged via PR")
cloud_state = "public" if iac_says_public else "private"
print(f"   next apply deploys: {cloud_state}  <-- and STAYS private")
print("   every environment from this module is born correct, permanently.\n")

print("The IaC file is the SOURCE OF TRUTH. Fixing the running resource while the file")
print("still says 'public' is temporary — the next deploy 'corrects' your fix back to")
print("insecure (drift). Snyk IaC catches the bad setting IN THE PULL REQUEST, so you")
print("fix the BLUEPRINT before it ever deploys. Fix the blueprint, not the building —")
print("otherwise you're re-fixing the same misconfig every release.")
print("\nAnd via POLICY-AS-CODE, 'no public buckets' is a CHECK that FAILS the PR, not a")
print("wiki page nobody reads — the same rule enforced on every change, automatically.")
EOF
```

**Expected result:** A hand-fix in the cloud console reverting to insecure on the next apply because the IaC still declares it public, versus a blueprint fix that deploys correct and stays correct. The fix-the-blueprint lesson is that the IaC file is the source of truth — fixing the running resource without fixing the file is drift waiting to be re-applied, so Snyk IaC catches the misconfiguration in the pull request.

**Negative test:** Fixing a misconfiguration in the cloud console while the Terraform still declares it insecure. The next `apply` reverts your fix — only changing the IaC source makes the fix durable, and policy-as-code makes the rule fail the PR automatically.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] IaC scanning understood as catching cloud misconfiguration in the manifest before it deploys.
- [ ] Fix-the-blueprint understood — the IaC file is the source of truth, and console fixes drift back to insecure.
- [ ] Policy-as-code understood as executable, versioned security rules that fail the pull request on violation.
- [ ] IaC recognized as the fourth engine completing the code-dependency-container-infrastructure supply chain.
