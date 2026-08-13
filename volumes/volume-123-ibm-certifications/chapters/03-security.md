# Chapter 03: Security Certifications

## Learning Objectives

- Map the IBM Security portfolio: the QRadar SIEM V7.5 ladder, Guardium, Verify Access, and the Cloud Pak for Security combo.
- Understand the QRadar role ladder from Associate through Deployment Professional.
- Complete walkthrough labs on the defensive concepts these certifications test.

## The security portfolio

| Certification | Catalog code | Focus |
|:---|:---|:---|
| Certified Associate - Security QRadar SIEM V7.5 | Cert-C9006200 | QRadar fundamentals |
| Certified Analyst - Security QRadar SIEM V7.5 | Cert-C9005200 | Offense analysis, searching |
| Certified SOC Analyst - QRadar SIEM V7.5 Plus CompTIA Cybersecurity Analyst | Cert-F1000200 | SOC workflow (IBM + CompTIA CySA+) |
| Certified Administrator - Security QRadar SIEM V7.5 | Cert-C9004600 | QRadar administration |
| Certified Deployment Professional - Security QRadar SIEM V7.5 | Cert-C9005100 | QRadar deployment/architecture |
| Certified Guardium Data Protection v12.x Administrator - Professional | Cert-C9008300 | Database activity monitoring |
| Certified Deployment Professional - Security Verify Access V10.0 | Cert-C4008807 | Access management (IAM) |
| Certified Administrator - Cloud Pak for Security V1.10 PLUS Red Hat OpenShift Admin | Cert-F1000100 | Unified security + OpenShift |

QRadar anchors the portfolio with a genuine **role ladder** — Associate → Analyst → Administrator → Deployment Professional — plus the CompTIA-combined SOC Analyst. All of this is **defensive**: detection, monitoring, access control, and data protection.

## Hands-On Lab

Walkthroughs use free primitives (a local syslog pipeline, SQL, an IdP concept model) to exercise the defensive ideas; QRadar/Guardium/Verify Access themselves are commercial (labs are design-level where the product is required). **Cost:** none.

### Lab 3.1 — Think in offenses (QRadar Analyst)

**Objective:** Build the correlation an analyst reads: many events → one offense.

```bash
python3 - <<'EOF'
# Model QRadar's core: a rule that correlates repeated failures into one offense
events = [("10.0.0.9","auth_fail")]*8 + [("10.0.0.9","auth_success")]
from collections import Counter
fails = Counter(src for src,ev in events if ev=="auth_fail")
for src,n in fails.items():
    if n >= 5:
        print(f"OFFENSE: possible brute force from {src} ({n} failures) then success -> investigate")
EOF
```

**Expected result:** One offense raised for the source with ≥5 failures followed by a success — QRadar's building-block behavior: rules turn event floods into a small number of prioritized offenses. The Analyst exam is about reading and tuning that, not writing Python.

**Negative test:** Lower the threshold to 1 and every failed login becomes an "offense" — alert fatigue; tuning thresholds is the analyst's craft the exam tests.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Log source and normalization (QRadar Administrator)

**Objective:** Understand the admin's first job: get events in and parsed.

```bash
logger -p auth.info "sshd[1]: Failed password for invalid user admin from 10.0.0.9 port 22 ssh2"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -1 || echo "event present in the auth stream"
```

**Expected result:** A syslog auth event generated and visible — the raw material QRadar ingests via a **log source**, then a **DSM** normalizes into fields (source IP, username, event category). The admin exam centers on log sources, DSMs, and whether events parse.

**Negative test:** A log source with the wrong DSM leaves events unparsed ("stored" but not categorized) — rules never fire on them; the classic admin troubleshooting scenario.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Database activity monitoring (Guardium)

**Objective:** State what Guardium watches and why it sits outside the database.

```sql
-- The activity Guardium flags, independent of the DB's own logs:
SELECT * FROM payroll.salary;              -- privileged SELECT on sensitive data
GRANT SELECT ON payroll.* TO 'contractor'; -- privilege change
```

**Expected result:** Both statements are the kind Guardium captures — a **SELECT on sensitive data** and a **privilege grant** — via network/agent taps *outside* the database, so a DBA cannot disable the monitoring from inside. That separation-of-duties property is Guardium's reason to exist and the exam's theme.

**Negative test:** Relying on the database's own audit log — a privileged insider can alter it; Guardium's out-of-band capture is the control that survives that.

**Rollback:** None (illustrative SQL).

### Lab 3.4 — Access management concepts (Verify Access)

**Objective:** Model the reverse-proxy/policy-enforcement pattern Verify Access implements.

```text
verify access> WebSEAL reverse proxy in front of the app:
  unauthenticated request -> redirect to auth (MFA/federation)
  authenticated -> policy check (who, what resource, what context) -> allow/deny -> proxy to app
```

**Expected result:** The enforcement chain — reverse proxy, authenticate (with MFA/federation), authorize by policy, then proxy — the Verify Access deployment model the exam tests, conceptually identical to the Gateway/WAF patterns in the Citrix and NetScaler volumes.

**Negative test:** Placing policy enforcement in the app instead of at the proxy — every app re-implements auth, inconsistently; the centralized-enforcement argument is the point.

**Rollback:** None (design).

### Lab 3.5 — Cloud Pak for Security + OpenShift (combo)

**Objective:** Understand the PLUS combo's two halves.

```text
combo> IBM half: Cloud Pak for Security V1.10 — federated search/threat intel across tools without moving data
combo> Red Hat half: OpenShift Administration — the platform the Cloud Pak runs on (RH Certified Specialist exam)
```

**Expected result:** Why the certification bundles two exams: the Cloud Pak is a containerized security fabric, so the credential validates both the security product and the OpenShift platform under it. [Chapter 09](09-red-hat-combos-choosing-currency-career.md) covers the combo mechanics across all six.

**Negative test:** Studying only the IBM half — the Red Hat OpenShift exam is a separate sitting with its own objectives; both are required.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] QRadar role ladder (Associate→Deployment Professional) and the CompTIA SOC combo mapped.
- [ ] Offense correlation, log-source/DSM normalization drilled.
- [ ] Guardium out-of-band monitoring and Verify Access enforcement modeled.
- [ ] The Cloud Pak for Security + OpenShift combo understood.
