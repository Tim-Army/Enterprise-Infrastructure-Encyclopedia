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

These labs cover **every topic in the Professional Cloud Security Engineer
exam guide**, section by section, and touch the Security Operations
Engineer surface (detection and response) where it adjoins. Mapping is in
the [volume README](../README.md#lab-coverage--security-professionals).

**Cost note:** IAM, org policy, and audit-log reads are free. One KMS key
(a small monthly per-version charge) and one bucket are the only billable
items. Lab 7.16 disables the key and deletes the project.

**Prerequisites**

```bash
export PROJECT_ID="$(gcloud config get-value project)"; echo "$PROJECT_ID"
```

**Expected result:** your sandbox project ID.

### Lab 7.1 — Managing Cloud Identity *(topic 1.1)*

```bash
gcloud organizations list --format='table(displayName, id)' 2>&1 | head -3
```

**Expected result:** your organization, or none for a standalone project.
Cloud Identity is where users and groups originate before IAM ever grants
them anything — the identity layer beneath access.

### Lab 7.2 — Managing service accounts *(topic 1.2)*

```bash
gcloud iam service-accounts create sa-sec --display-name="sec lab"
SA="sa-sec@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud iam service-accounts describe "$SA" --format='value(email, disabled)'
```

**Expected result:** the email and `disabled:` blank (= enabled). Note
**no key was created** — that is the secure default this exam rewards.

### Lab 7.3 — Managing authentication *(topic 1.3)*

```bash
gcloud iam service-accounts keys list --iam-account="$SA" \
  --format='table(name.basename(), keyType)'
```

**Expected result:** one `SYSTEM_MANAGED` key and **no** `USER_MANAGED`
keys. User-managed keys are the leak risk; their absence is the finding
you want.

### Lab 7.4 — Managing authorization controls *(topic 1.4)*

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA}" --role="roles/storage.objectViewer" \
  --condition=None
gcloud projects get-iam-policy "$PROJECT_ID" --flatten='bindings[].members' \
  --filter="bindings.members:${SA}" --format='value(bindings.role)'
```

**Expected result:** `roles/storage.objectViewer` — a predefined role, not
a basic one. Authorization is additive and inherited downward.

### Lab 7.5 — Defining the resource hierarchy *(topic 1.5)*

```bash
gcloud projects describe "$PROJECT_ID" --format='value(parent.type, parent.id)'
```

**Expected result:** `folder` or `organization` with an ID, or blank for a
standalone project. The hierarchy is where inherited IAM and policy
originate — security design starts here.

### Lab 7.6 — Designing perimeter security *(topic 2.1)*

```bash
gcloud access-context-manager policies list --organization="$(gcloud projects describe "$PROJECT_ID" --format='value(parent.id)')" \
  --format='value(name)' 2>&1 | head -3
```

**Expected result:** an access policy name, or a message that none exists
/ no org. VPC Service Controls perimeters live under an access policy —
the control that answers *where data may go*.

### Lab 7.7 — Configuring boundary segmentation *(topic 2.2)*

```bash
gcloud compute networks create vpc-sec --subnet-mode=custom
gcloud compute firewall-rules create deny-all-ingress \
  --network=vpc-sec --action=deny --rules=all --direction=INGRESS --priority=65534
gcloud compute firewall-rules describe deny-all-ingress \
  --format='value(denied[].IPProtocol.list(), priority)'
```

**Expected result:** `all 65534`. An explicit low-priority deny makes the
default-deny posture readable rather than implicit — segmentation as
written intent.

### Lab 7.8 — Establishing private connectivity *(topic 2.3)*

```bash
gcloud compute networks subnets create snet-sec \
  --network=vpc-sec --range=10.70.0.0/24 --region=us-central1 \
  --enable-private-ip-google-access
gcloud compute networks subnets describe snet-sec --region=us-central1 \
  --format='value(privateIpGoogleAccess)'
```

**Expected result:** `True`. Private Google Access lets workloads reach
Google APIs with no external IP — the private-connectivity building block.

### Lab 7.9 — Preventing data loss *(topic 3.1)*

```bash
gcloud services list --available --filter="name:dlp" --format='value(name)'
```

**Expected result:** `dlp.googleapis.com` available. Sensitive Data
Protection (DLP) discovers and de-identifies sensitive data — the topic-3.1
control, applied before data spreads.

### Lab 7.10 — Managing encryption *(topic 3.2)*

```bash
gcloud kms keyrings create kr-sec --location=us-central1
gcloud kms keys create key-sec --location=us-central1 --keyring=kr-sec \
  --purpose=encryption
gcloud storage buckets create "gs://sec-lab-${PROJECT_ID}" --location=us-central1 \
  --uniform-bucket-level-access \
  --default-encryption-key="projects/${PROJECT_ID}/locations/us-central1/keyRings/kr-sec/cryptoKeys/key-sec"
gcloud storage buckets describe "gs://sec-lab-${PROJECT_ID}" --format='value(default_kms_key)'
```

**Expected result:** the key's full resource name — CMEK is in force.
Reading it back is the verification; the create command alone is not
evidence.

### Lab 7.11 — Securing AI workloads *(topic 3.3)*

```bash
gcloud services list --available --filter="name:aiplatform" --format='value(name)'
```

**Expected result:** `aiplatform.googleapis.com` available. Securing AI
workloads (a recent guide addition) means the same controls — IAM, CMEK,
VPC-SC — applied to Vertex AI resources; confirm current guide wording.

### Lab 7.12 — Automating infrastructure security *(topic 4.1)*

```bash
gcloud resource-manager org-policies deny compute.vmExternalIpAccess all \
  --project="$PROJECT_ID"
gcloud resource-manager org-policies list --project="$PROJECT_ID" \
  --format='value(constraint)' | grep vmExternalIpAccess
```

**Expected result:** `constraints/compute.vmExternalIpAccess`. Org policy
is security automation — a guardrail that enforces itself on every future
resource without a human in the loop.

### Lab 7.13 — Logging, monitoring, and detection *(topic 4.2)*

```bash
gcloud logging read 'protoPayload.methodName:"SetIamPolicy"' --limit=3 \
  --format='table(timestamp, protoPayload.authenticationInfo.principalEmail)'
gcloud scc findings list "$(gcloud projects describe "$PROJECT_ID" --format='value(parent.id)')" \
  --filter='state="ACTIVE"' --format='value(category)' 2>&1 | head -3
```

**Expected result:** IAM-change log lines, and either Security Command
Center findings or an access message. This is the Security Operations
Engineer overlap — detection is built on these two surfaces.

### Lab 7.14 — Supporting compliance requirements *(topic 5.1)*

```bash
gcloud resource-manager org-policies describe constraints/gcp.resourceLocations \
  --project="$PROJECT_ID" --effective 2>&1 | head -5
```

**Expected result:** a location allow-list, or a "not currently enforced"
result. Data-residency compliance is expressed as this constraint — a
regulatory requirement made technical.

### Lab 7.15 — Data Access audit logs *(operations, cross-topic)*

```bash
gcloud projects get-iam-policy "$PROJECT_ID" --format=json > /tmp/pol.json
grep -c auditConfigs /tmp/pol.json || echo "no Data Access audit logs configured"
```

**Expected result:** `no Data Access audit logs configured` on a fresh
project. Admin Activity logs are always on; Data Access logs are **not**,
so "who read this object?" has no answer unless enabled in advance — the
lesson that surfaces only during an investigation.

### Lab 7.16 — Negative test and cleanup

Prove CMEK is genuinely in the data path — disable the key and try to
write:

```bash
gcloud kms keys versions disable 1 --key=key-sec --keyring=kr-sec --location=us-central1
echo test > /tmp/t.txt
gcloud storage cp /tmp/t.txt "gs://sec-lab-${PROJECT_ID}/" 2>&1 | tail -2
```

**Expected result:** the write **fails**, the error naming the disabled
key (`KMS key ... is not enabled`). That failure is the proof CMEK sits in
the write path — and that key management is an availability risk, not only
a confidentiality one.

```bash
gcloud kms keys versions enable 1 --key=key-sec --keyring=kr-sec --location=us-central1
gcloud projects delete "$PROJECT_ID" --quiet
gcloud projects describe "$PROJECT_ID" --format='value(lifecycleState)'
```

**Expected result:** `DELETE_REQUESTED`. Re-enabling the key first avoids
leaving a disabled-key alert behind; project deletion removes the key
ring, bucket, VPC, and policies together.

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
