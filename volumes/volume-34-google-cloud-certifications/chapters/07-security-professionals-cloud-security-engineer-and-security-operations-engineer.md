# Chapter 07: Security Professionals — Cloud Security Engineer and Security Operations Engineer

## Learning Objectives

- Distinguish the two professional security certifications and the
  different jobs they certify
- Describe the Cloud Security Engineer's domain: identity, network
  security, data protection, and compliance on Google Cloud
- Explain what Security Operations Engineer covers and why its arrival
  reflects Google's security-operations portfolio
- Apply Google Cloud's data-protection controls — CMEK, VPC Service
  Controls, and Sensitive Data Protection — to stated requirements
- Choose between the two certifications, and recognize when both are
  justified

## Theory and Architecture

### Two security certifications, two jobs

| Certification | The job |
| --- | --- |
| Professional Cloud Security Engineer | Designs and implements secure infrastructure on Google Cloud |
| Professional Security Operations Engineer | Detects, investigates, and responds to threats |

Both are **2 hours, $200, 50–60 multiple choice and multiple select
questions**, valid **two years**, no prerequisites (verified
23 July 2026).

The split mirrors a real organizational division — the engineer who builds
the controls versus the analyst who works the alerts — and it is the same
split Microsoft draws between its identity/platform security
certifications and SC-200 Security Operations Analyst
([Volume XXXIII](../../volume-33-microsoft-azure-certifications/README.md),
Chapter 09).

**Security Operations Engineer is the newer of the two**, and its
existence reflects Google's investment in a security-operations portfolio
following the Mandiant acquisition and the Google Security Operations
platform. A reader working an alert queue should note it exists; older
certification maps do not show it.

### Cloud Security Engineer: building the controls

Four areas, and each has a control that repays knowing well:

- **Identity and access** — IAM design, service accounts, Workload
  Identity Federation, and the additive-roles model from
  [Chapter 03](03-associate-cloud-engineer.md). Prefer Workload Identity
  Federation over service account keys for external workloads; key files
  are the most-leaked Google Cloud credential.
- **Network security** — VPC firewall rules, Cloud Armor for edge
  protection and WAF, Private Google Access, and the elimination of
  external IPs via organization policy
  ([Chapter 05](05-professional-cloud-architect.md)).
- **Data protection** — encryption everywhere by default, with
  **CMEK** (customer-managed encryption keys in Cloud KMS) when a
  requirement demands key control, and **Sensitive Data Protection** for
  discovering and de-identifying sensitive data at rest and in flight.
- **Compliance and monitoring** — Security Command Center as the posture
  and threat surface, audit logs, and Assured Workloads where regulatory
  regimes require it.

### VPC Service Controls: the control that is genuinely distinctive

The Google Cloud security control most worth understanding, and the one
most likely to decide an exam scenario:

**VPC Service Controls** define a *service perimeter* around Google-managed
services — BigQuery, Cloud Storage, and others — so that data cannot be
read out of the perimeter even by an identity that holds valid IAM
permissions. It mitigates **exfiltration**, which IAM by itself cannot:
a compromised credential with legitimate `storage.objects.get` rights can
still be blocked from copying data to an external project.

Hold the distinction clearly:

- **IAM** answers *who may access this resource*.
- **Organization policy** answers *what may be configured*.
- **VPC Service Controls** answers *where data may go*.

A requirement phrased as "even an authorized user must not be able to copy
this data outside our organization" is a VPC Service Controls requirement,
and neither of the other two mechanisms satisfies it.

### Security Operations Engineer: working the queue

This certification covers the detection-and-response side: ingesting and
normalizing telemetry, writing and tuning detection rules, triaging and
investigating alerts, threat hunting, and orchestrating response. Google
Security Operations (with its SIEM and SOAR capabilities) is the platform,
and Security Command Center supplies cloud posture and threat findings.

The skills are analytical rather than architectural — reducing false
positives, reconstructing a timeline, deciding what a detection should
actually fire on — and they do not follow from the Cloud Security Engineer
material.

## Design Considerations

- **Choose by whether you build controls or work alerts.** Cloud Security
  Engineer designs and implements; Security Operations Engineer detects
  and responds. Both is justified only for a genuinely dual role.
- **Reach for VPC Service Controls on exfiltration requirements.** If the
  requirement survives the sentence "assume the credential is valid," IAM
  is not the answer.
- **Use CMEK when the requirement names key control.** Google-managed
  encryption is on by default and satisfies most requirements; CMEK adds
  operational burden and is justified by a stated need to hold or rotate
  keys yourself.
- **Eliminate service account keys.** Workload Identity Federation for
  external workloads, attached service accounts for internal ones.
- **Treat Security Command Center as the posture source.** Scenarios about
  "how would you know" usually resolve to it rather than to a bespoke
  pipeline.

## Implementation and Automation

### CMEK on a storage bucket

```bash
gcloud kms keyrings create kr-lab --location=us-central1
gcloud kms keys create key-lab --location=us-central1 \
  --keyring=kr-lab --purpose=encryption
```

```bash
gcloud storage buckets create gs://sec-lab-$RANDOM --location=us-central1 \
  --uniform-bucket-level-access \
  --default-encryption-key=projects/<PROJECT_ID>/locations/us-central1/keyRings/kr-lab/cryptoKeys/key-lab
```

### Inspecting a service perimeter

```bash
# Perimeters live at organization scope under an access policy
gcloud access-context-manager policies list --organization=<ORG_ID>
gcloud access-context-manager perimeters list --policy=<POLICY_ID>
```

### Reading Security Command Center findings

```bash
gcloud scc findings list <ORG_ID> \
  --filter='state="ACTIVE" AND severity="HIGH"' \
  --format='table(category, resourceName, severity)' | head -20
```

### Audit logs: the investigator's raw material

```bash
# Admin Activity logs are on by default and are where "who did this"
# questions are answered
gcloud logging read \
  'logName:"cloudaudit.googleapis.com%2Factivity" AND protoPayload.methodName:"storage.buckets"' \
  --limit=10 --format='table(timestamp, protoPayload.authenticationInfo.principalEmail, protoPayload.methodName)'
```

## Validation and Troubleshooting

- **Prove a perimeter blocks exfiltration**, not merely that it exists.
  A VPC Service Controls perimeter that has never denied a cross-perimeter
  read is unverified configuration.
- **Distinguish three denial types.** An IAM failure names a missing
  permission; an organization policy violation names a constraint; a VPC
  Service Controls denial names the perimeter and is often reported as a
  request-violates-perimeter error. Telling them apart is the diagnostic
  skill.
- **Verify CMEK is actually in force** by reading the bucket's default
  encryption key rather than trusting the creation command:

  ```bash
  gcloud storage buckets describe gs://<BUCKET> --format='value(default_kms_key)'
  ```

- **Confirm Data Access logs before an investigation depends on them.**
  Admin Activity is on by default; Data Access generally is not, so the
  "who read this object" question may have no answer unless enabled in
  advance.
- **Tune detections against false positives.** A rule that fires
  constantly is worse than no rule; the operations certification tests
  that judgment directly.

## Security and Best Practices

- Never grant basic roles in a security design, and never distribute
  service account keys — both are examinable failures and real-world
  incident causes.
- Enable Data Access audit logs deliberately on sensitive resources,
  accepting the cost, because their absence is discovered only during an
  investigation when it is too late.
- Apply VPC Service Controls in dry-run mode first. A perimeter applied
  directly to production will break legitimate access paths you did not
  know existed, and dry-run reports what *would* have been denied.
- Rotate CMEK keys on a schedule and understand that destroying a key
  renders data unrecoverable — key management is a availability risk as
  much as a confidentiality control.
- Run all lab work in the sandbox project; perimeter and organization
  policy changes are disruptive by design.

## References and Knowledge Checks

**References**

- [Professional Cloud Security Engineer](https://cloud.google.com/certification/cloud-security-engineer)
- [Professional Security Operations Engineer](https://cloud.google.com/learn/certification/security-operations-engineer)
- [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs)
- [Security Command Center](https://cloud.google.com/security-command-center/docs)
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 03](03-associate-cloud-engineer.md) for the IAM model and
  [Chapter 05](05-professional-cloud-architect.md) for organization policy.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Distinguish the two security certifications by the job each certifies.
2. State what IAM, organization policy, and VPC Service Controls each
   answer, and give a requirement only the third satisfies.
3. When is CMEK justified over Google-managed encryption?
4. Why might "who read this object?" be unanswerable during an
   investigation, and what prevents that?
5. Why apply a service perimeter in dry-run mode first?

## Hands-On Lab

**Objective:** Apply a customer-managed encryption key and prove it is in
force, then distinguish the three denial types Google Cloud produces.

**Cost note:** KMS keys carry a small monthly charge per key version; the
bucket is negligible. Step 6 deletes the project, which stops both.

**Prerequisites**

- The sandbox project and budget alert from Chapter 01.
- `gcloud` authenticated with rights to create KMS keys and buckets.

**Steps**

1. **Create the key (10 minutes).** Create the key ring and key from the
   Implementation section.

   **Expected result:** the key exists and is `ENABLED`.

2. **Create a CMEK bucket (10 minutes).** Create a bucket with the key as
   its default encryption key.

   **Expected result:** the bucket exists.

3. **Verify CMEK is in force (5 minutes).**

   ```bash
   gcloud storage buckets describe gs://<BUCKET> --format='value(default_kms_key)'
   ```

   **Expected result:** your key's full resource name — not empty.
   Trusting the create command without this check is the mistake.

4. **Negative test — break the key (15 minutes).** Disable the key
   version, then attempt to write an object:

   ```bash
   gcloud kms keys versions disable 1 --key=key-lab --keyring=kr-lab --location=us-central1
   echo test > /tmp/t.txt && gcloud storage cp /tmp/t.txt gs://<BUCKET>/
   ```

   **Expected result:** the write **fails**, naming the key. This proves
   CMEK is genuinely in the data path — and demonstrates that key
   management is an availability risk. Re-enable the version afterward.

5. **Distinguish denials (15 minutes).** Produce and compare three errors:
   an IAM denial (act outside your roles), an organization policy denial
   (reuse the external-IP constraint from
   [Chapter 05](05-professional-cloud-architect.md)), and the key failure
   above.

   **Expected result:** you can name the mechanism from each message
   alone.

6. **Cleanup:** re-enable the key version, then delete the project:

   ```bash
   gcloud projects delete <PROJECT_ID>
   ```

   Confirm no KMS key versions remain billable.

## Lab Verification

Complete this sign-off once CMEK has been proven in the data path and the
three denial types distinguished. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Google Cloud's two professional security certifications split along a real
organizational line: **Cloud Security Engineer** builds the controls —
identity, network security, data protection, and compliance — while the
newer **Security Operations Engineer** detects, investigates, and responds
on Google Security Operations and Security Command Center. Both are $200,
two hours, and valid two years. The distinctive control is **VPC Service
Controls**, which answers *where data may go* and mitigates exfiltration
that IAM cannot — completing the trio with IAM (*who may act*) and
organization policy (*what may be configured*). CMEK is justified when a
requirement names key control, and it puts key availability into the data
path, which the lab proves directly.

- [ ] Can distinguish the two security certifications by job.
- [ ] Can state what IAM, org policy, and VPC Service Controls each
      answer.
- [ ] Knows when CMEK is justified and what risk it introduces.
- [ ] Knows Data Access logs must be enabled before they are needed.
- [ ] Has proven CMEK is in the data path and distinguished three denial
      types.
- [ ] Completed the hands-on lab, including re-enabling the key and
      cleanup.
