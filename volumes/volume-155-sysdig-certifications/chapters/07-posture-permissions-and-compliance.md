# Chapter 07: Posture, Permissions, and Compliance

## Learning Objectives

- Explain CSPM — cloud security posture management.
- Understand CIEM — cloud entitlements, informed by runtime usage.
- Place compliance monitoring against benchmarks.
- Recognize how runtime data sharpens posture and permissions.

*Cert relevance: CSPM, CIEM, and compliance are the posture pillars of the Sysdig CNAPP — tested across the accreditations.*

## CSPM: posture

**Cloud Security Posture Management (CSPM)** is the posture pillar — continuously checking cloud and Kubernetes **configurations** against best practice and finding misconfigurations (a public storage bucket, an over-permissive security group, a container running as root, a missing network policy). This is the same [CSPM the Wiz volume (CXLVII)](../../volume-147-wiz-certifications/chapters/04-agentless-posture-and-vulnerabilities.md) covers, and it is essential prevention — reducing the attack surface *before* runtime.

Sysdig delivers CSPM as *part of the unified CNAPP*, so posture findings sit alongside runtime detections — and, distinctively, posture can be **prioritized by runtime context**: a misconfiguration on a workload that is *actually running and exposed* matters more than one on a dormant resource. Runtime data sharpens posture just as it sharpens vulnerabilities ([Chapter 6](06-vulnerability-management-runtime-prioritization.md)). The lab is covered within the CIEM exercise.

## CIEM: entitlements informed by runtime

**Cloud Infrastructure Entitlement Management (CIEM)** manages **who and what can do what** in the cloud — the [effective-permissions problem the Wiz volume teaches](../../volume-147-wiz-certifications/chapters/05-ciem-and-dspm-identity-and-data.md). Cloud identities (users, roles, service accounts) accumulate **over-broad permissions**, and excessive entitlements are a major attack surface (a compromised identity can do everything it *can*, not just what it *should*).

Sysdig's distinctive angle, again, is **runtime**: it observes which permissions are **actually used** and recommends **right-sizing** entitlements to match — removing permissions **granted but never exercised.** The insight parallels in-use vulnerabilities: of the permissions an identity *has*, only some are *used*, and the unused ones are pure risk with no benefit. Recommending least-privilege from *observed* usage is stronger than guessing, because it is grounded in what the workload actually needs. The lab models this.

## Compliance

**Compliance** monitoring checks the environment against **regulatory and industry benchmarks** — CIS Kubernetes/Docker benchmarks, PCI DSS, SOC 2, NIST, HIPAA. Because Sysdig continuously assesses both posture *and* runtime, it can report compliance as a **live, evidence-backed** state — not only "is the configuration compliant?" but "is the *running* environment behaving compliantly?" — and produce the reports auditors require. Continuous compliance (the [live-number discipline](../../volume-146-jamf-certifications/chapters/08-jamf-school-and-compliance.md) from across the shelf) applied to cloud-native. The lab is covered within the CIEM exercise.

## Hands-On Lab

Python models runtime-informed entitlements. **Cost:** none.

### Lab 7.1 — Right-size entitlements from observed usage

**Objective:** See how runtime usage data drives least privilege.

```bash
python3 - <<'EOF'
# a service account's GRANTED permissions vs what it ACTUALLY USES at runtime
GRANTED = {"s3:read", "s3:write", "s3:delete", "ec2:start", "ec2:terminate",
           "iam:createuser", "iam:attachpolicy", "logs:write", "secrets:read"}
# runtime observation over 30 days: which were ever actually invoked?
USED = {"s3:read", "s3:write", "logs:write", "secrets:read"}

print("Service account 'app-svc' — GRANTED vs ACTUALLY USED (observed over 30 days):\n")
print(f"   granted ({len(GRANTED)}): {sorted(GRANTED)}")
print(f"   used    ({len(USED)}): {sorted(USED)}")
unused = GRANTED - USED
print(f"\n   GRANTED BUT NEVER USED ({len(unused)}): {sorted(unused)}")
print("\n   These unused permissions are PURE RISK with zero benefit:")
for p in sorted(unused):
    risk = "  <-- HIGH (destructive/privilege)" if p in ("s3:delete","ec2:terminate","iam:createuser","iam:attachpolicy") else ""
    print(f"      {p}{risk}")
reduction = 100*len(unused)/len(GRANTED)
print(f"\n   right-sizing to observed usage removes {len(unused)}/{len(GRANTED)} permissions ({reduction:.0f}%)")
print("   -> incl. s3:delete, ec2:terminate, iam:createuser/attachpolicy — the exact")
print("      permissions an attacker who compromised this account would abuse.")
print("\nThe CIEM insight (runtime-informed): of the permissions an identity HAS, only")
print("some are ever USED. The unused ones are attack surface with NO operational")
print("benefit — a compromised account can do everything it CAN, not just what it")
print("SHOULD. Sysdig OBSERVES actual usage and recommends right-sizing to match —")
print("least privilege grounded in MEASURED need, not guesswork. Same 'in-use' idea as")
print("runtime vuln prioritization (Ch 6): runtime data sharpens the whole CNAPP —")
print("vulnerabilities, posture, AND entitlements — by grounding it in what's real.")
EOF
```

**Expected result:** A service account's granted permissions compared to those actually used at runtime, flagging the unused ones (including destructive and privilege-granting permissions) as pure risk to remove. The CIEM lesson is that only some granted permissions are ever used, so right-sizing to observed usage removes attack surface with no operational cost — runtime data grounding least privilege in measured need, the same in-use principle that sharpens vulnerabilities and posture.

**Negative test:** Right-sizing permissions by guessing what an identity needs. You either leave excess (risk) or break the workload (removed a needed permission); observing actual runtime usage grounds least privilege in what is genuinely required.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CSPM understood as continuous configuration posture, able to be prioritized by runtime context in the unified CNAPP.
- [ ] CIEM understood as entitlement management, with Sysdig's runtime angle right-sizing permissions from observed usage.
- [ ] Compliance understood as live, evidence-backed monitoring against benchmarks (CIS, PCI, SOC 2).
- [ ] Runtime data recognized as sharpening the whole CNAPP — vulnerabilities, posture, and entitlements alike.
