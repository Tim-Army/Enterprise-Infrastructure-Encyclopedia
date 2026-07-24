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

**Objective:** Build the core engineer objects, then prove that a
predefined role grants exactly what you expect — and that a missing API
fails differently from a missing permission.

**Cost note:** An `e2-micro` instance and a small bucket are minimal but
not free. Step 6 deletes the project, which removes everything.

**Prerequisites**

- The sandbox project and budget alert from Chapter 01.
- `gcloud` authenticated with rights to create resources and IAM bindings.

**Steps**

1. **Build (20 minutes).** Enable the Compute API, then create the VPC,
   subnet, a VM, and a bucket using the Implementation commands.

   **Expected result:** all four exist and appear in their `list`
   commands.

2. **Create and attach a service account (10 minutes).** Create
   `sa-ace-lab`, grant it `roles/storage.objectViewer`, and attach it to a
   VM.

   **Expected result:** the binding appears in the project IAM policy and
   the VM reports the service account.

3. **Test permissions directly (10 minutes).** Run
   `test-iam-permissions` for `storage.objects.get` and
   `storage.objects.delete`.

   **Expected result:** `get` returns as permitted, `delete` does not —
   demonstrating that the predefined role is genuinely scoped.

4. **Negative test — two different failures (15 minutes).** First, disable
   an API you have not used and attempt an operation needing it. Then, as
   the service account, attempt `storage.objects.delete`.

   **Expected result:** two distinguishable errors — one naming a disabled
   API and directing you to `gcloud services enable`, one naming a missing
   permission. Being able to tell them apart from the message alone is the
   point.

5. **Check inheritance (10 minutes).** In writing, state what would change
   if `roles/editor` were granted at the folder level above this project.

   **Expected result:** a correct account — the broad role would be
   inherited and would *not* be constrained by the narrow binding you
   made.

6. **Cleanup:**

   ```bash
   gcloud projects delete <PROJECT_ID>
   ```

   Confirm it shows `DELETE_REQUESTED`, and check the budget for
   unexpected spend.

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
