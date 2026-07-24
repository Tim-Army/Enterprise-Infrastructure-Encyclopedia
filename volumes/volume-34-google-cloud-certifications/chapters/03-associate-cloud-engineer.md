# Chapter 03: Associate Cloud Engineer

## Learning Objectives

- Place Associate Cloud Engineer as the working anchor of the Google Cloud
  program and the usual real starting point for infrastructure engineers
- Describe the engineer's domain: setting up a cloud solution environment,
  planning and configuring, deploying and implementing, ensuring
  successful operation, and configuring access and security
- Configure and verify the core objects from `gcloud` — projects, compute,
  networking, storage, and IAM bindings
- Apply Google Cloud IAM correctly, including the additive-roles model and
  the difference between basic, predefined, and custom roles
- Build a study plan anchored in a sandbox project rather than in reading

## Theory and Architecture

### The working anchor

**Associate Cloud Engineer** is the Google Cloud certification most
infrastructure engineers should hold first. It is **2 hours, $125, 50–60
multiple choice and multiple select questions**, valid **three years**,
with no prerequisites and a recommended six months or more of hands-on
Google Cloud experience (verified 23 July 2026).

It plays the role AZ-104 plays on Azure and Solutions Architect –
Associate plays on AWS: the credential that certifies you can actually
operate the platform, and the substrate every professional certification
assumes.

### What the engineer owns

Google's exam guide organizes the role into five areas, and they map onto
daily work:

- **Setting up a cloud solution environment** — projects, billing
  accounts, IAM for users and service accounts, and enabling APIs.
- **Planning and configuring** — computing resources, data storage
  options, and network resources sized against requirements.
- **Deploying and implementing** — Compute Engine, Google Kubernetes
  Engine, Cloud Run, App Engine, data solutions, and networking resources.
- **Ensuring successful operation** — managing those same resources,
  plus Cloud Monitoring, Cloud Logging, and diagnostics.
- **Configuring access and security** — IAM roles, service accounts, and
  audit logs.

### IAM: additive roles, and the three role types

The conceptual core of this certification, and the place engineers from
other clouds most often carry a wrong mental model.

Google Cloud IAM grants **roles** to **principals** at a **scope**
(organization, folder, project, or an individual resource). Two properties
matter:

- **Roles are additive.** Effective permissions are the union of every
  role a principal holds at every scope above and including the resource.
  Granting a narrow role does not constrain a broad one granted elsewhere;
  there is no ordinary "deny wins" evaluation at the role level. To
  actually remove access you remove the binding, or use an explicit **IAM
  deny policy**, which is a separate mechanism.
- **Inheritance flows down.** A role granted at the organization or folder
  level applies to everything beneath it.

Three role types, in increasing precision:

| Type | Examples | When |
| --- | --- | --- |
| Basic | Owner, Editor, Viewer | Legacy and very broad — avoid in production |
| Predefined | `roles/compute.instanceAdmin`, `roles/storage.objectViewer` | The normal choice; curated per service |
| Custom | Your own permission set | Only when no predefined role fits |

Basic roles predate IAM's finer grain and remain dangerously wide —
Editor in particular grants far more than most people assume. Reaching for
a predefined role first is both examinable and simply correct.

### Service accounts

A **service account** is an identity for a workload rather than a person.
It is both a *principal* (it can be granted roles) and a *resource*
(principals can be granted roles **on** it, such as the ability to
impersonate it). That dual nature is a reliable source of confusion and a
reliable source of exam questions.

Prefer attaching a service account to a resource and using the metadata
server or Workload Identity over creating and distributing service account
**keys**, which are long-lived credentials that leak.

## Design Considerations

- **Start here, not at Cloud Digital Leader.** For anyone already
  administering infrastructure, this is the certification that changes how
  you are read professionally.
- **Grant predefined roles, not basic ones.** If you find yourself
  granting Editor, stop and find the predefined role that actually fits.
- **Grant at the smallest correct scope.** Inheritance flows down, so a
  role granted at the organization level is almost never what you meant.
- **Avoid service account keys.** Attach service accounts to resources.
  A key file in a repository is the most common serious Google Cloud
  security failure, and the exam reflects that.
- **Practice in a project you can delete.** Deleting a project removes
  everything in it, which makes cleanup trivially reliable — a genuine
  advantage over per-resource teardown.

## Implementation and Automation

### Project, API, and compute

```bash
gcloud config set project <PROJECT_ID>
gcloud services enable compute.googleapis.com
```

```bash
gcloud compute instances create vm-ace-lab \
  --zone=us-central1-a --machine-type=e2-micro \
  --image-family=debian-12 --image-project=debian-cloud
```

### Networking and storage

```bash
gcloud compute networks create vpc-ace-lab --subnet-mode=custom
gcloud compute networks subnets create snet-ace \
  --network=vpc-ace-lab --range=10.20.0.0/24 --region=us-central1
```

```bash
gcloud storage buckets create gs://ace-lab-$RANDOM --location=us-central1 \
  --uniform-bucket-level-access
```

### IAM: predefined role at project scope, and a service account

```bash
# A predefined role, not a basic one
gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:<SA_EMAIL>" \
  --role="roles/storage.objectViewer"
```

```bash
# Create a service account and attach it to a VM rather than issuing keys
gcloud iam service-accounts create sa-ace-lab --display-name="ACE lab"
gcloud compute instances create vm-with-sa --zone=us-central1-a \
  --machine-type=e2-micro \
  --service-account="sa-ace-lab@<PROJECT_ID>.iam.gserviceaccount.com" \
  --scopes=cloud-platform
```

## Validation and Troubleshooting

- **Read effective permissions, not intent.** `gcloud projects
  get-iam-policy` flattened by member shows what a principal actually
  holds at that scope; roles inherited from a folder or organization sit
  above it and will not appear there.
- **Test a permission directly** rather than reasoning about it:

  ```bash
  gcloud projects test-iam-permissions <PROJECT_ID> \
    --permissions=storage.objects.get,compute.instances.create
  ```

- **Distinguish "API not enabled" from "permission denied."** Both fail a
  command; the first is fixed with `gcloud services enable`, the second
  with an IAM binding. The error text names which, and telling them apart
  quickly is a real engineer skill.
- **Check the scope when a role seems ineffective.** A binding at project
  scope does not grant access to a resource in a *different* project, and
  a binding on a bucket does not grant project-wide storage rights.
- **Prove cleanup.** Deleting the project is the reliable teardown; verify
  with `gcloud projects list` that it is in `DELETE_REQUESTED`.

## Security and Best Practices

- Never grant basic roles (Owner, Editor, Viewer) in anything resembling
  production. Editor in particular is far broader than its name suggests.
- Do not create service account keys unless there is no alternative.
  Attach service accounts to resources, or use Workload Identity
  Federation for external workloads.
- Enable uniform bucket-level access on new buckets, as in the command
  above; per-object ACLs are legacy and make effective access hard to
  reason about.
- Audit logs are examinable and operationally essential — Admin Activity
  logs are on by default; Data Access logs generally are not, and enabling
  them is a deliberate decision with cost implications.
- Run every lab in the sandbox project with the budget alert from
  Chapter 01, and delete the project when done.

## References and Knowledge Checks

**References**

- [Associate Cloud Engineer](https://cloud.google.com/certification/cloud-engineer) —
  2 hours, $125, three-year validity, with the exam guide.
- [Google Cloud IAM documentation](https://cloud.google.com/iam/docs)
- [Google Skills](https://cloud.google.com/learn) — the free learning path
  for this certification.
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 05](05-professional-cloud-architect.md) for the design
  credential this leads to.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Explain what "IAM roles are additive" means and how you actually remove
   access.
2. Distinguish basic, predefined, and custom roles, and say which to reach
   for first.
3. Why is a service account both a principal and a resource, and what does
   that enable?
4. A command fails. How do you tell "API not enabled" from "permission
   denied," and what fixes each?
5. Why is deleting the project a more reliable cleanup than deleting
   resources individually?

## Hands-On Lab

These labs cover **every topic in the Associate Cloud Engineer exam
guide**, section by section. Each is a walkthrough: run the command shown
and compare against the stated expected result. The topic-to-lab mapping
is in the [volume README](../README.md#lab-coverage--associate-cloud-engineer).

**Cost note:** `e2-micro` instances, a small bucket, one Cloud SQL
instance, and a single-node GKE Autopilot cluster are minimal but **not
free**. GKE and Cloud SQL are the expensive items — Lab 3.7 deletes the
whole project, which stops everything.

**Prerequisites**

- The sandbox project and budget alert from
  [Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md).
- `gcloud` authenticated. Set your project once:

  ```bash
  export PROJECT_ID="$(gcloud config get-value project)"
  echo "$PROJECT_ID"
  ```

  **Expected result:** your sandbox project ID, not `(unset)`.

### Lab 3.1 — Setting up cloud projects and accounts *(guide topic 1.1)*

```bash
gcloud projects describe "$PROJECT_ID" \
  --format='table(projectId, name, lifecycleState, parent.type)'
```

**Expected result:** one row, `lifecycleState: ACTIVE`. `parent.type`
reads `folder` or `organization` if the project sits in a hierarchy, and
is blank for a standalone project — which is itself the answer to "is
this project governed from above?"

### Lab 3.2 — Managing billing configuration *(guide topic 1.2)*

```bash
gcloud billing projects describe "$PROJECT_ID" \
  --format='value(billingAccountName, billingEnabled)'
```

**Expected result:** `billingAccounts/XXXXXX-XXXXXX-XXXXXX True`. If
`billingEnabled` is `False`, every later lab fails at resource creation —
fix it before continuing. Note the billing account is a *separate* object
from the project, which is why budgets attach to it.

### Lab 3.3 — Planning and configuring compute resources *(guide topic 2.1)*

```bash
gcloud compute machine-types list --filter="zone:us-central1-a AND name~'^e2-'" \
  --format='table(name, guestCpus, memoryMb)' --limit=5
```

**Expected result:** a short table including `e2-micro` with `guestCpus: 2`
and `memoryMb: 1024`. Sizing is a selection problem before it is a
provisioning problem — this is the catalogue you select from.

### Lab 3.4 — Planning and configuring data storage options *(guide topic 2.2)*

```bash
gcloud storage buckets create "gs://ace-lab-${PROJECT_ID}" \
  --location=us-central1 --uniform-bucket-level-access
gcloud storage buckets describe "gs://ace-lab-${PROJECT_ID}" \
  --format='value(location, storageClass, uniformBucketLevelAccess.enabled)'
```

**Expected result:** `US-CENTRAL1 STANDARD True`. Uniform bucket-level
access being `True` matters: it disables per-object ACLs, which is the
configuration that makes effective access reasonable to audit.

### Lab 3.5 — Planning and configuring network resources *(guide topic 2.3)*

```bash
gcloud compute networks create vpc-ace --subnet-mode=custom
gcloud compute networks subnets create snet-ace \
  --network=vpc-ace --range=10.40.0.0/24 --region=us-central1
gcloud compute networks subnets list --network=vpc-ace \
  --format='table(name, region, ipCidrRange)'
```

**Expected result:** one row — `snet-ace us-central1 10.40.0.0/24`. The
VPC itself is global; only the subnet carries a region, which is the
Google Cloud networking fact Chapter 06 builds on.

### Lab 3.6 — Deploying Compute Engine resources *(guide topic 3.1)*

```bash
gcloud compute instances create vm-ace --zone=us-central1-a \
  --machine-type=e2-micro --subnet=snet-ace --no-address \
  --image-family=debian-12 --image-project=debian-cloud
gcloud compute instances describe vm-ace --zone=us-central1-a \
  --format='value(status, machineType.basename(), networkInterfaces[0].networkIP)'
```

**Expected result:** `RUNNING e2-micro 10.40.0.2`. `--no-address` means no
external IP — the instance is reachable only inside the VPC, which is the
posture the security chapters assume.

### Lab 3.7 — Deploying Google Kubernetes Engine resources *(guide topic 3.2)*

```bash
gcloud container clusters create-auto gke-ace \
  --region=us-central1 --network=vpc-ace --subnetwork=snet-ace
gcloud container clusters describe gke-ace --region=us-central1 \
  --format='value(status, currentMasterVersion)'
```

**Expected result:** `RUNNING` and a version string. This takes several
minutes and is the most expensive resource in the chapter — if you are
watching cost, read the expected result here and skip to Lab 3.9.

### Lab 3.8 — Deploying Cloud Run and Cloud Functions *(guide topic 3.3)*

```bash
gcloud run deploy svc-ace \
  --image=us-docker.pkg.dev/cloudrun/container/hello \
  --region=us-central1 --allow-unauthenticated
gcloud run services describe svc-ace --region=us-central1 \
  --format='value(status.url, status.conditions[0].status)'
```

**Expected result:** an `https://svc-ace-...run.app` URL and `True`.
`curl` that URL and you should get the sample page — Cloud Run scales to
zero, so the first request is measurably slower than the second.

### Lab 3.9 — Deploying data solutions *(guide topic 3.4)*

```bash
bq mk --dataset --location=us-central1 "${PROJECT_ID}:ace_lab"
bq ls --format=pretty "${PROJECT_ID}:"
```

**Expected result:** a table listing `ace_lab`. Creating a dataset is
free; queries against it are not, which is why Chapter 04's dry-run habit
exists.

### Lab 3.10 — Deploying networking resources *(guide topic 3.5)*

```bash
gcloud compute firewall-rules create allow-ace-internal \
  --network=vpc-ace --allow=tcp:22,icmp --source-ranges=10.40.0.0/24
gcloud compute firewall-rules list --filter="network:vpc-ace" \
  --format='table(name, direction, sourceRanges.list(), allowed[].map().firewall_rule().list())'
```

**Expected result:** one INGRESS rule for `10.40.0.0/24` allowing
`tcp:22` and `icmp`. Google Cloud denies ingress by default, so without
this rule the instance from Lab 3.6 is unreachable even from inside the
subnet.

### Lab 3.11 — Implementing resources through infrastructure as code *(guide topic 3.6)*

```bash
cat > /tmp/ace.tf <<'TF'
resource "google_storage_bucket" "iac" {
  name                        = "ace-iac-${var.project_id}"
  location                    = "US-CENTRAL1"
  uniform_bucket_level_access = true
}
variable "project_id" { type = string }
TF
cd /tmp && terraform init -input=false >/dev/null && \
  terraform plan -input=false -var="project_id=$PROJECT_ID" | tail -5
```

**Expected result:** `Plan: 1 to add, 0 to change, 0 to destroy.` The
plan is the deliverable here — infrastructure as code is examined as a
declarative workflow, and reading a plan before applying is the habit.

### Lab 3.12 — Managing Compute Engine resources *(guide topic 4.1)*

```bash
gcloud compute instances stop vm-ace --zone=us-central1-a
gcloud compute instances describe vm-ace --zone=us-central1-a --format='value(status)'
gcloud compute instances start vm-ace --zone=us-central1-a
gcloud compute instances describe vm-ace --zone=us-central1-a --format='value(status)'
```

**Expected result:** `TERMINATED` then `RUNNING`. A stopped instance still
bills for its persistent disk — stopping is not deleting, and the exam
tests that distinction.

### Lab 3.13 — Managing Google Kubernetes Engine resources *(guide topic 4.2)*

```bash
gcloud container clusters get-credentials gke-ace --region=us-central1
kubectl create deployment web --image=us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0
kubectl get deployment web -o wide
```

**Expected result:** `web  1/1  1  1` once the pod is scheduled. On
Autopilot the node appears on demand, so `READY` may take a minute —
`kubectl get pods -w` shows the transition.

### Lab 3.14 — Managing Cloud Run resources *(guide topic 4.3)*

```bash
gcloud run services update svc-ace --region=us-central1 --max-instances=3
gcloud run services describe svc-ace --region=us-central1 \
  --format='value(spec.template.metadata.annotations["autoscaling.knative.dev/maxScale"])'
```

**Expected result:** `3`. Capping max instances is the standard guard
against a traffic spike turning into a bill spike.

### Lab 3.15 — Managing storage and database solutions *(guide topic 4.4)*

```bash
echo "ace lab object" > /tmp/ace.txt
gcloud storage cp /tmp/ace.txt "gs://ace-lab-${PROJECT_ID}/"
gcloud storage ls -L "gs://ace-lab-${PROJECT_ID}/ace.txt" | grep -E 'Storage class|Content-Length'
```

**Expected result:** `Storage class: STANDARD` and a byte count. Then set
a lifecycle rule and confirm it is recorded:

```bash
printf '{"lifecycle":{"rule":[{"action":{"type":"Delete"},"condition":{"age":1}}]}}' > /tmp/lc.json
gcloud storage buckets update "gs://ace-lab-${PROJECT_ID}" --lifecycle-file=/tmp/lc.json
gcloud storage buckets describe "gs://ace-lab-${PROJECT_ID}" --format='value(lifecycle)'
```

**Expected result:** the rule echoed back with `age: 1`.

### Lab 3.16 — Managing networking resources *(guide topic 4.5)*

```bash
gcloud compute networks subnets expand-ip-range snet-ace \
  --region=us-central1 --prefix-length=23
gcloud compute networks subnets describe snet-ace --region=us-central1 \
  --format='value(ipCidrRange)'
```

**Expected result:** `10.40.0.0/23` — the range widened in place.
Subnet ranges can be expanded but **never shrunk**, which is why initial
CIDR planning (Lab 3.5) matters.

### Lab 3.17 — Monitoring and logging *(guide topic 4.6)*

```bash
gcloud logging read \
  'resource.type="gce_instance" AND protoPayload.methodName:"compute.instances.start"' \
  --limit=3 --format='table(timestamp, protoPayload.authenticationInfo.principalEmail)'
```

**Expected result:** at least one row showing your own account and the
time you ran Lab 3.12 — Admin Activity audit logs are on by default and
answer "who did this?" without configuration.

### Lab 3.18 — Managing IAM *(guide topic 5.1)*

```bash
gcloud projects get-iam-policy "$PROJECT_ID" \
  --flatten='bindings[].members' \
  --format='table(bindings.role, bindings.members)' | head -10
```

**Expected result:** your account against one or more roles. Now test a
specific permission rather than inferring it:

```bash
gcloud projects test-iam-permissions "$PROJECT_ID" \
  --permissions=compute.instances.create,resourcemanager.projects.delete
```

**Expected result:** the permissions you actually hold are echoed back;
any you lack are simply absent from the response.

### Lab 3.19 — Managing service accounts *(guide topic 5.2)*

```bash
gcloud iam service-accounts create sa-ace --display-name="ACE lab"
SA="sa-ace@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA}" --role="roles/storage.objectViewer" \
  --condition=None --format='value(bindings.role)' | tail -1
```

**Expected result:** `roles/storage.objectViewer` in the updated policy —
a *predefined* role, not a basic one.

### Lab 3.20 — Negative test: prove the role is genuinely scoped

```bash
gcloud iam service-accounts add-iam-policy-binding "$SA" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/iam.serviceAccountTokenCreator"
gcloud storage rm "gs://ace-lab-${PROJECT_ID}/ace.txt" \
  --impersonate-service-account="$SA"
```

**Expected result:** the delete **fails** with
`403 ... does not have storage.objects.delete access`. That is the point:
`objectViewer` grants read and not delete, and impersonating the service
account proves it against the real identity rather than by reading the
policy. Confirm the object survived:

```bash
gcloud storage ls "gs://ace-lab-${PROJECT_ID}/"
```

**Expected result:** `ace.txt` still listed.

### Lab 3.21 — Cleanup

```bash
gcloud projects delete "$PROJECT_ID" --quiet
gcloud projects describe "$PROJECT_ID" --format='value(lifecycleState)'
```

**Expected result:** `DELETE_REQUESTED`. Deleting the project removes the
cluster, instance, bucket, dataset, and service account together — which
is why the sandbox project is the unit of teardown. Confirm in the billing
console that GKE and Cloud Run stop accruing.

## Lab Verification

Complete this sign-off once both failure modes have been distinguished and
the project deleted. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Associate Cloud Engineer is the working anchor of the Google Cloud program
— 2 hours, $125, three-year validity, no prerequisites — and the right
first certification for most infrastructure engineers. Its conceptual core
is IAM: roles are **additive** and inherited **downward**, so effective
access is the union of everything granted at and above a resource, and
removing access means removing bindings rather than adding narrower ones.
Prefer predefined roles over the dangerously broad basic roles, grant at
the smallest correct scope, and attach service accounts to resources
instead of issuing long-lived keys. Readiness comes from building and
deleting a sandbox project repeatedly, which is also the most reliable
cleanup the program offers.

- [ ] Can explain additive roles and downward inheritance.
- [ ] Can distinguish basic, predefined, and custom roles.
- [ ] Can explain a service account's dual nature.
- [ ] Can tell an API-not-enabled failure from a permission denial.
- [ ] Has tested permissions directly rather than inferring them.
- [ ] Completed the hands-on lab, including both negative tests and
      project deletion.
