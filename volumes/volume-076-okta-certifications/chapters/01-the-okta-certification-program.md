# Chapter 01: The Okta Certification Program

## Learning Objectives

- Explain Okta's platform (Workforce Identity Cloud and Customer Identity Cloud/Auth0).
- Describe the certification ladder and specialties.
- Understand the ProctorU exam model, cost, and validity.
- Map credentials to roles and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**Okta** is a leading **identity and access management (IAM)** platform, spanning the **Workforce
Identity Cloud (WIC)** — securing employee access with directory, single sign-on, multi-factor
authentication, and lifecycle management — and the **Customer Identity Cloud (CIC, built on Auth0)**
— securing customer-facing applications. Okta's certification program validates the people who
deploy and operate this platform. The **role ladder** runs **Certified Professional → Certified
Administrator → Certified Consultant → Certified Technical Architect**, with **Certified Developer**
for those building on Okta's APIs and SDKs, plus specialties (**Certified Workflows**, **Certified
Access Gateway**) and the **Auth0 Certified Developer** for customer identity. Exams are **proctored
online via ProctorU** (Guardian Browser), cost **$250** (first attempt), and are valid **two years**
(the **Technical Architect** is valid three years and includes a **board-defense** component).
Because IAM is the control plane for who can access what, this entire volume is **defensive** — every
lab secures identity, authentication, and access.

> **Scope.** Identity and access management is a defensive discipline. Every lab is **authorized
> administration** — configuring directories, SSO, MFA, policies, lifecycle, and governance to
> protect access — never an attack on an identity system.

## Design Considerations

Climb **Professional → Administrator → Consultant** for administration depth; add **Developer** for
API work and **Architect** for design. Pursue **Workflows/Access Gateway** specialties as your
environment needs. Note the **prerequisites** (Architect requires Professional, Administrator,
Consultant, and WIC Developer). Budget for the **two-year** renewal. Verify current exams on
okta.com — the program evolves with the platform.

## Implementation and Automation

Confirm your practice environment (a free Okta developer org and `python3`, used throughout):

```bash
command -v python3 >/dev/null && echo "python3: ok" || echo "python3: install for labs"
echo "Sign up for a free Okta Integrator/Developer org at developer.okta.com for hands-on labs"
```

## Validation and Troubleshooting

The verified program facts (okta.com/services/certification, 28 July 2026):

```text
Platform: Workforce Identity Cloud (WIC) + Customer Identity Cloud (CIC/Auth0).
Ladder: Professional -> Administrator -> Consultant -> Technical Architect (board defense, 3yr). Also: Developer, Workflows, Access Gateway, Auth0 Developer.
Exams: proctored via ProctorU (Guardian Browser); $250 first attempt; valid 2 years (Architect 3yr).
```

Common pitfalls: skipping **prerequisites** (Consultant needs Professional + Administrator); and
conflating **WIC** (workforce) with **CIC/Auth0** (customer) — they are distinct clouds.

## Security and Best Practices

Learn the **current** ladder and platform on okta.com, respect **prerequisites**, and renew before
the two-year expiry. Practice on a **free developer org**, never a production tenant. All work is
defensive identity administration.

## References and Knowledge Checks

- okta.com/services/certification: the ladder, specialties, and exam model.
- developer.okta.com: free developer org and API documentation.

**Knowledge checks**

1. What are Okta's two identity clouds?
2. Name the role ladder in order.
3. How long is a standard Okta certification valid?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a workstation with `python3`,
and (optionally) a free Okta developer org, in a lab. **Cost:** none.

### Lab 1.1 — Map the platform

**Objective:** Distinguish WIC and CIC.

```python
python3 - <<'PY'
platform={"Workforce Identity Cloud (WIC)":"employee access: Universal Directory, SSO, MFA, Lifecycle Mgmt, API Access, Governance",
          "Customer Identity Cloud (CIC/Auth0)":"customer apps: B2C/B2B login, Actions, Organizations"}
for cloud,scope in platform.items(): print(f"{cloud}\n   -> {scope}")
PY
```

**Expected result:** the **two clouds** and their scope — the platform map this volume follows.

**Negative test:** use a WIC feature for a customer-facing app; **CIC/Auth0** is built for that —
match the cloud to the use case.

**Cleanup:** none.

### Lab 1.2 — Map credentials to the ladder

**Objective:** Record the certification ladder.

```python
python3 - <<'PY'
ladder=[("Professional","no prereq — core"),("Administrator","prereq: Professional"),
        ("Consultant","prereq: Professional + Administrator"),
        ("Technical Architect","prereq: Prof+Admin+Consultant+WIC Developer; board defense; 3yr")]
extras=["Developer (APIs/SDKs)","Workflows (automation)","Access Gateway (on-prem apps)","Auth0 Developer (CIC)"]
for name,note in ladder: print(f"{name:20}: {note}")
print("Specialties:", ", ".join(extras))
PY
```

**Expected result:** the ladder with **prerequisites** and specialties — your scheduling reference.

**Negative test:** book the **Architect** first; its prerequisites gate it — climb the ladder.

**Cleanup:** none.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Okta admin":"Professional -> Administrator","Implementation consultant":"Professional -> Administrator -> Consultant",
       "App developer":"Developer (+ Auth0 Developer for CIC)","Identity architect":"...-> Consultant -> Technical Architect",
       "Automation specialist":"Administrator -> Workflows"}
for role,path in paths.items(): print(f"{role:24}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** pursue the Consultant with no Administrator; prerequisites block it — build up in
order.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Okta certifies IAM practitioners across a role ladder (Professional → Administrator → Consultant →
Technical Architect) plus Developer and specialty tracks, on the Workforce and Customer (Auth0)
identity clouds, via ProctorU with two-year validity — taught here as defensive identity
administration.

- [ ] I can explain WIC vs CIC/Auth0.
- [ ] I can name the ladder and prerequisites.
- [ ] I can describe the exam model and validity.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
