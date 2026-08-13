# Chapter 07: Architect — Application and System

## Learning Objectives

- Understand the Architect pyramid and the CTA.
- Design a scalable data and sharing architecture.
- Design integrations and identity/access.
- Plan development lifecycle and deployment.
- Complete a walkthrough for each architect domain.

## Theory and Architecture

The **Architect** track is a pyramid of specialist exams building to the elite **Certified Technical
Architect (CTA)**. Two capstones sit below it: the **Application Architect** (earned via Platform App
Builder, Platform Developer I, **Data Architect**, and **Sharing and Visibility Architect**) — mastery
of the data model, large-data-volume design, and the sharing model at scale; and the **System
Architect** (earned via **Integration Architecture**, **Identity and Access Management Architect**,
and **Development Lifecycle and Deployment Architect**) — mastery of integrating Salesforce with other
systems (REST/SOAP, integration patterns, middleware), identity/SSO, and the release process
(sandboxes, version control, CI/CD, change management). The **CTA** is assessed by a **board review**
where the candidate designs and defends an end-to-end solution to a complex scenario. Architecture is
about **trade-offs at scale** — data volume, sharing performance, integration reliability, and
deployment safety — justified against requirements. This chapter teaches each with a hands-on
walkthrough (data/sharing scale, integration patterns, and lifecycle design).

## Design Considerations

Design the **data model** for large data volumes (skinny tables, indexing, archiving). Ensure the
**sharing model** performs at scale (avoid ownership skew). Choose the right **integration pattern**
(request-reply, fire-and-forget, batch, pub/sub) and secure it. Design **identity/SSO** (SAML/OIDC).
Use **sandboxes + version control + CI/CD** for safe deployment. Justify **trade-offs** for the CTA
board.

## Implementation and Automation

The labs reason about data/sharing scale, integration patterns, and deployment.

## Validation and Troubleshooting

Confirm the architect model:

```text
Application Architect (App Builder + PD1 + Data Architect + Sharing & Visibility): data model at scale (LDV) + sharing performance. System Architect (Integration + Identity & Access Mgmt + Dev Lifecycle & Deployment): integration patterns + SSO + release process.
CTA: board review defending an end-to-end design. Architecture = trade-offs at scale justified to requirements.
```

Common pitfalls: a sharing model that doesn't scale (**ownership skew**, deep hierarchies); and manual
deployment with no **version control/CI-CD**.

## Security and Best Practices

Design for **large data volumes**, a **scalable sharing** model, the right **integration patterns**
with security, **identity/SSO**, and safe **CI/CD deployment** — justifying trade-offs. All work is
authorized architecture.

## Hands-On Lab

Architect walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 7.1 — Design for large data volumes

**Objective:** Keep performance at scale.

```python
python3 - <<'PY'
ldv={"problem":"50M records on a custom object","techniques":["selective indexed SOQL filters","skinny tables",
     "archive old data off-platform / to Big Objects","avoid non-selective queries in triggers"]}
print("problem:",ldv["problem"])
for t in ldv["techniques"]: print("  -",t)
print("Data Architect: LDV design keeps queries + sharing performant at scale")
PY
```

**Expected result:** **large-data-volume** techniques (indexing, skinny tables, archiving) — scalable
data design.

**Negative test:** run non-selective SOQL against 50M records in a trigger; it times out — use
**selective, indexed** queries.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Avoid ownership skew

**Objective:** Keep sharing performant.

```python
python3 - <<'PY'
scenario={"issue":"one integration user owns 2M records (ownership skew)","impact":"sharing recalculation locks + slow",
          "fix":"distribute ownership / use 'public' OWD where sharing isn't needed / role placement"}
for k,v in scenario.items(): print(f"{k:8}: {v}")
print("Sharing & Visibility Architect: avoid ownership/lookup skew to keep sharing performant")
PY
```

**Expected result:** the **ownership skew** problem and fix — scalable sharing architecture.

**Negative test:** assign millions of records to one owner; sharing recalculation degrades — **distribute
ownership**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Choose an integration pattern

**Objective:** Connect systems reliably.

```python
python3 - <<'PY'
patterns={"real-time lookup from another system":"Request-Reply (synchronous callout)",
          "notify external system of a change":"Fire-and-Forget (async / platform event)",
          "nightly bulk sync":"Batch Data Synchronization","event-driven many consumers":"Publish/Subscribe (Platform Events)"}
for need,pattern in patterns.items(): print(f"{need:40}: {pattern}")
PY
```

**Expected result:** each need matched to an **integration pattern** — System Architect integration
design.

**Negative test:** make a **synchronous** callout for a nightly bulk sync; it blocks and hits limits —
use a **batch** pattern.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Plan the deployment lifecycle

**Objective:** Deploy safely.

```python
python3 - <<'PY'
lifecycle=["develop in a Developer/scratch sandbox","version control (Git) as source of truth",
           "CI: run Apex tests on pull request","deploy to a UAT sandbox for validation","release to production via CI/CD (DevOps Center / sf CLI)"]
for i,s in enumerate(lifecycle,1): print(f"{i}. {s}")
print("Dev Lifecycle & Deployment Architect: sandboxes + Git + CI/CD -> safe, repeatable releases")
PY
```

**Expected result:** a **sandbox → Git → CI/CD** deployment lifecycle — safe release management.

**Negative test:** make changes directly in **production**; there's no test/rollback — deploy through
**sandboxes + CI/CD**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Architect track masters data and sharing at scale (Application Architect) and integration, identity,
and deployment (System Architect), culminating in the CTA board — designing and defending scalable,
reliable, safely-deployed solutions.

- [ ] I can design for large data volumes.
- [ ] I can avoid ownership skew.
- [ ] I can choose an integration pattern.
- [ ] I can plan the deployment lifecycle.
- [ ] I completed Labs 7.1–7.4 including each negative test.
