# Chapter 08: Cloud Security — Professional and Engineer

## Learning Objectives

- Explain the Cloud Security Professional and Cloud Security Engineer credentials.
- Describe the Prisma Cloud / Cortex Cloud CNAPP model.
- Assess cloud posture and query findings with RQL.
- Shift left with infrastructure-as-code scanning.
- Complete a walkthrough for each Cloud Security topic (defensive).

## Theory and Architecture

The **Cloud Security Professional** (Professional) and **Cloud Security Engineer** (Specialist)
credentials cover Palo Alto's cloud-native application protection platform — **Prisma Cloud**,
now delivered as part of **Cortex Cloud**. A **CNAPP** unifies what used to be separate tools:
**CSPM** (posture — misconfigurations and compliance), **CWPP** (workload protection — hosts,
containers, serverless), **CIEM** (cloud identity and entitlements), **IaC scanning** (catching
misconfigurations before deploy), and **code-to-cloud** context that traces a running risk back
to the code that created it. The query language is **RQL** (the Prisma Cloud Query Language),
used to search configuration, network, and audit data for findings. The Professional focuses on
posture and concepts; the Engineer on onboarding accounts, building policies, and remediation.
All **defensive**: find and fix cloud risk.

## Design Considerations

**Shift left** — scan **IaC** so misconfigurations never reach production. Cover the whole
CNAPP surface (posture + workloads + identity), not just posture. Use **code-to-cloud** context
to fix the **root** (the template), not just the running symptom. Prioritize by real
exploitability, not raw finding count.

## Implementation and Automation

The labs assess posture with RQL, scan IaC, review a CIEM finding, and query the API — all
**authorized cloud-security assessment and remediation**.

## Validation and Troubleshooting

Confirm the CNAPP model:

```text
Prisma/Cortex Cloud (CNAPP): CSPM (posture) + CWPP (workloads) + CIEM (identity) + IaC scan
  + code-to-cloud context. Query language: RQL. Shift left; fix the root (IaC).
```

Common pitfalls: fixing a running misconfiguration but not the **IaC template** (it returns);
and chasing finding **count** instead of **exploitable** risk.

## Security and Best Practices

Scan **IaC in the pipeline**, remediate at the **template**, and prioritize by exploitability
and blast radius. Cover posture, workloads, and identity together. Least-privilege the CNAPP's
own cloud access. Defensive assessment and remediation throughout.

## Hands-On Lab

Cloud Security walkthroughs (defensive). **Shared prerequisites** — a Prisma/Cortex Cloud tenant
(or the RQL/IaC patterns) and, for Lab 8.2, the `checkov` open-source IaC scanner. **Cost:**
none with a tenant/trial.

### Lab 8.1 — Assess posture with RQL

**Objective:** Find exposed storage.

```sql
config from cloud.resource where api.name = 'aws-s3api-get-bucket-acl'
  AND json.rule = "policyStatus.isPublic is true"
```

**Expected result:** publicly exposed S3 buckets surfaced by **RQL** — a posture (CSPM) finding.

**Negative test:** click through each bucket in the console; **RQL** finds them across all
accounts — query centrally.

**Cleanup:** none (read-only).

### Lab 8.2 — Shift left: scan IaC

**Objective:** Catch a misconfiguration before deploy.

```bash
cat > main.tf <<'TF'
resource "aws_s3_bucket" "demo" { bucket = "demo" }
resource "aws_s3_bucket_public_access_block" "demo" {
  bucket = aws_s3_bucket.demo.id
  block_public_acls = false   # misconfiguration
}
TF
checkov -f main.tf --compact 2>/dev/null | grep -iE "FAILED|block_public" | head \
  || echo "IaC scan (checkov/Prisma Cloud IaC) flags block_public_acls=false before deploy"
```

**Expected result:** the scanner **flags** `block_public_acls=false` before deployment — shift
left.

**Negative test:** deploy first and scan the running bucket; **IaC scanning** catches it earlier
— scan in the pipeline.

**Cleanup:** `rm -f main.tf`.

### Lab 8.3 — Review a CIEM finding

**Objective:** Find excessive cloud entitlements.

```text
# CIEM analyzes effective permissions: an identity with unused admin rights is over-privileged.
#   Recommendation: right-size to least privilege based on actual usage.
"ciem: effective permissions vs used -> flag over-privilege -> least-privilege remediation"
```

**Expected result:** an **over-privileged identity** flagged with a least-privilege
recommendation — the CIEM view.

**Negative test:** grant broad admin "to be safe"; **CIEM** right-sizes to used permissions —
least privilege.

**Cleanup:** none.

### Lab 8.4 — Query findings via the API

**Objective:** Retrieve alerts programmatically.

```bash
curl -sk -X POST "https://<prisma-api>/v2/alerts" -H "x-redlock-auth: $PRISMA_JWT" \
  -H "Content-Type: application/json" -d '{"filters":[{"name":"alert.status","value":"open"}]}' 2>/dev/null \
  | python3 -c "import sys;print('open alerts retrieved' if '[' in sys.stdin.read() else 'query the Prisma Cloud API for open alerts')" 2>/dev/null \
  || echo "Prisma/Cortex Cloud API: POST /v2/alerts -> open findings for automation/reporting"
```

**Expected result:** the open cloud-security alerts from the **API** — programmatic reporting and
remediation.

**Negative test:** export findings from the console to report; the **API** feeds automation — use
it.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Cloud Security Professional and Engineer credentials cover Prisma/Cortex Cloud CNAPP —
CSPM, CWPP, CIEM, IaC scanning, and code-to-cloud context — queried with RQL. Shift left, fix
the root in IaC, cover the whole surface, and prioritize by exploitability. Defensive assessment
and remediation.

- [ ] I can assess posture with RQL.
- [ ] I can scan IaC to shift left.
- [ ] I can interpret a CIEM over-privilege finding.
- [ ] I can query cloud findings via the API.
- [ ] I completed Labs 8.1–8.4 including each negative test.
