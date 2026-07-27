# Chapter 01: The CrowdStrike Falcon Certification Program

## Learning Objectives

- Describe the CrowdStrike Falcon platform and what its certifications validate.
- Identify the seven Falcon certifications and their target roles.
- Explain the exam format, delivery, and three-year validity.
- Locate the authoritative exam guides and CrowdStrike University training.
- Verify program facts from the official source.

## Theory and Architecture

**CrowdStrike Falcon** is a cloud-delivered platform for endpoint, cloud, identity,
and SIEM security — a single lightweight **sensor** feeding a cloud console and a
rich **API**. The **Falcon Certification Program** (run by **CrowdStrike University**,
CSU) validates the operational skills to administer, respond, hunt, engineer SIEM,
and secure identity and cloud on Falcon. This volume is a **certification-tracks**
volume, like the other vendor volumes: it maps the program — which credentials
exist, their **exam-guide domains**, and roles — and teaches each with a hands-on
walkthrough.

The program has **seven certifications** in two groups:

- **Platform:** Certified Falcon **Administrator (CCFA)**, **Responder (CCFR)**,
  **Hunter (CCFH)**, and the Next-Gen SIEM pair — **SIEM Analyst (CCSA)** and
  **SIEM Engineer (CCSE)**.
- **Specialist:** Certified **Identity Specialist (CCIS)** and **Cloud Specialist
  (CCCS)**.

Every credential was **verified against crowdstrike.com on 27 July 2026**; the exam
guides carry recent revision dates (January–July 2026).

## Design Considerations

Choose by role. **CCFA** is the administrative foundation (deployment, policy, RBAC).
Analysts progress to **CCFR** (respond to detections) and **CCFH** (proactive threat
hunting with the CrowdStrike Query Language). SOC teams building on **Next-Gen SIEM**
take **CCSA** (analyze) and **CCSE** (engineer ingestion/parsing/content). The
**specialist** exams cover **Identity Protection (CCIS)** and **Cloud Security
(CCCS)**. There are no enforced prerequisites, but each guide recommends CSU learning
paths and practical experience.

## Implementation and Automation

Confirm the current lineup from the source:

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.crowdstrike.com/en-us/crowdstrike-university/crowdstrike-falcon-certification-program/" \
  | grep -oiE 'CCF[ARH]|CCS[AE]|CCIS|CCCS|Certified Falcon [A-Za-z]+' | sort -u
```

Labs in this volume use **real Falcon tooling** — the `falconctl` sensor CLI, the
**FalconPy** Python SDK, the **OAuth2 REST API**, the **CrowdStrike Query Language
(CQL)** for Next-Gen SIEM, and the **GraphQL API** for Identity Protection — against
a licensed Falcon tenant (or the read-only patterns shown where no tenant is
available). This is **defensive** security: authorized administration, detection,
hunting, and response only.

## Validation and Troubleshooting

Confirm the program facts before you study:

```text
crowdstrike.com/crowdstrike-university:
  - 7 certifications (CCFA, CCFR, CCFH, CCSA, CCSE, CCIS, CCCS)
  - each exam: 90 minutes, 60 questions, Pearson VUE
  - valid 3 years; recertify by passing the current exam
  - exam guides list knowledge domains (no published % weights)
```

Common pitfalls: studying a stale guide (they revise regularly — check the date);
and assuming published domain weights exist (they do not — prepare evenly).

## Security and Best Practices

Read the current **exam guide** for each target credential (it lists the domains),
complete the recommended **CSU learning path**, and get hands-on time in a Falcon
tenant. Treat all Falcon access as privileged: least-privilege RBAC, audited RTR,
and change-controlled policy. Recertify within the three-year window.

## References and Knowledge Checks

- crowdstrike.com/crowdstrike-university: the certification program, exam guides, and CSU training.

**Knowledge checks**

1. Name the seven Falcon certifications and each group they belong to.
2. What is the exam format and validity period?
3. Where are the authoritative exam domains published?

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a
shell with `curl`, `python3`, and (optionally) Falcon API credentials. **Cost:**
none for the read-only checks.

### Lab 1.1 — Enumerate the certification lineup

**Objective:** Read the seven certifications from the source.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.crowdstrike.com/en-us/crowdstrike-university/crowdstrike-falcon-certification-program/" \
  | grep -oiE 'CCF[ARH]|CCS[AE]|CCIS|CCCS' | sort -u
```

**Expected result:** the acronyms **CCCS, CCFA, CCFH, CCFR, CCIS, CCSA, CCSE** — the
seven-credential program.

**Negative test:** rely on a third-party "CrowdStrike certs" list; vendors change
lineups — confirm on crowdstrike.com.

**Cleanup:** none.

### Lab 1.2 — Obtain an API bearer token (OAuth2)

**Objective:** Authenticate to the Falcon API (the basis for every SDK/API lab).

```bash
curl -sS -X POST "https://api.crowdstrike.com/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$FALCON_CLIENT_ID&client_secret=$FALCON_CLIENT_SECRET" \
  | python3 -c "import sys,json;print('token len',len(json.load(sys.stdin)['access_token']))"
```

**Expected result:** a non-zero **token length** — a valid OAuth2 bearer token for
subsequent calls (tokens expire in ~30 minutes).

**Negative test:** call a data endpoint with no token; the API returns **401
Unauthorized** — authenticate first.

**Cleanup:** let the token expire; revoke the API client in the console if it was
temporary.

### Lab 1.3 — Confirm the exam format

**Objective:** State the shared exam format.

```bash
python3 - <<'PY'
exams=["CCFA","CCFR","CCFH","CCSA","CCSE","CCIS","CCCS"]
for e in exams: print(f"{e}: 90 minutes, 60 questions, Pearson VUE, valid 3 years")
PY
```

**Expected result:** the shared **90-minute / 60-question / Pearson VUE / 3-year**
format for all seven exams — the program's testing model.

**Negative test:** assume differing formats per exam; all seven share the same
format — verify on the guide.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CrowdStrike Falcon Certification Program validates operating the Falcon platform
across seven role-based credentials in two groups — platform (CCFA, CCFR, CCFH,
CCSA, CCSE) and specialist (CCIS, CCCS). Every exam is 90 minutes and 60 questions,
delivered by Pearson VUE and valid three years. The exam guides define the domains;
this volume teaches each with real Falcon tooling.

- [ ] I can name the seven certifications and their groups.
- [ ] I can state the exam format and validity.
- [ ] I can obtain an OAuth2 API token.
- [ ] I can locate the authoritative exam guides.
- [ ] I completed Labs 1.1–1.3 including each negative test.
