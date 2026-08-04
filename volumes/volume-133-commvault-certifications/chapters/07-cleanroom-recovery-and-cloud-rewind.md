# Chapter 07: Cleanroom Recovery and Cloud Rewind

## Learning Objectives

- Explain Cleanroom Recovery: isolated, on-demand recovery into a known-clean environment.
- Use a cleanroom for both incident recovery and non-disruptive recovery testing.
- Describe Cloud Rewind: rebuilding cloud applications and their dependencies.
- Sequence a recovery so infrastructure comes back in dependency order.

## Why a cleanroom exists

These two capabilities define the **Professional** tier of the Readiverse program (which requires Cloud Rewind or Cleanroom Recovery coursework) and reappear in the **Expert** tier. They exist because of a problem Chapter 06 exposes: you have identified a clean recovery point, but **where do you restore it to?**

After a ransomware incident the production environment is a crime scene. It may still harbor the attacker, the malware, or the vulnerability that let them in. Restoring clean data into a compromised environment simply re-exposes it — and restoring into an environment still under investigation can destroy forensic evidence.

A **cleanroom** is an isolated, on-demand recovery environment — typically stood up in cloud infrastructure — that is:

| Property | Why it matters |
|:---|:---|
| **Isolated** | No network path to the compromised production estate |
| **Clean** | Built fresh from known-good images, not from the infected environment |
| **On-demand** | Provisioned when needed; you do not pay for a standing duplicate data center |
| **Complete** | Includes the identity, network, and dependencies the application needs to actually run |

The last property is the one people underestimate. Restoring an application server into an empty network gets you a machine that boots and does nothing, because it cannot authenticate, resolve names, or reach its database.

## The cleanroom serves two purposes

1. **Incident recovery** — recover for real, into an environment the attacker does not control, while forensics proceeds on production undisturbed.
2. **Recovery testing** — rehearse recovery routinely without touching production. This is verification **level 5** from Chapter 05, and the cleanroom is what makes it practical: previously, proving a full recovery required either a standing duplicate environment or an outage.

That second use is the quiet transformation. Recovery rehearsal stops being an annual fire drill nobody schedules and becomes a repeatable, non-disruptive test.

## Cloud Rewind

**Cloud Rewind** addresses cloud-native applications, where "restore the VM" is not sufficient. A cloud application is a *composition*: compute, managed databases, storage buckets, networks and security groups, IAM roles, load balancers, and the infrastructure-as-code that defines them. Losing it means losing the whole assembly.

Cloud Rewind rebuilds cloud applications and their **dependencies**, in the right **order**, so the application comes back as a working system rather than a pile of restored components. The exam-relevant concept is **dependency-ordered recovery**: network before compute, identity before applications, databases before app tiers.

## Hands-On Lab

Python models cleanroom and dependency-ordered recovery. **Cost:** none.

### Lab 7.1 — Orchestrate a cleanroom recovery

**Objective:** Recover into isolation from a verified-clean point.

```bash
python3 - <<'EOF'
def cleanroom_recovery(recovery_point, scan_status, isolated, clean_images, includes_identity):
    steps, blockers = [], []
    if scan_status != "clean":
        blockers.append(f"recovery point {recovery_point} is '{scan_status}' — pick an earlier clean point")
    if not isolated:
        blockers.append("cleanroom has a network path to production — isolation is the whole point")
    if not clean_images:
        blockers.append("environment built from production images — may carry the compromise")
    if not includes_identity:
        blockers.append("no identity services — restored apps cannot authenticate anyone")
    if blockers:
        return ["BLOCKED"] + [f"   - {b}" for b in blockers]
    steps = ["provision isolated cleanroom (fresh, known-good images)",
             "restore identity + DNS first",
             f"restore data from {recovery_point} (Threat Scan: clean)",
             "restore application tiers",
             "validate: applications start, authenticate, and serve",
             "forensics continues on production, undisturbed"]
    return ["PROCEED"] + [f"   {i+1}. {s}" for i, s in enumerate(steps)]

print("--- attempt 1 ---")
for line in cleanroom_recovery("2026-07-31","infected", True,  True,  True):  print(line)
print("\n--- attempt 2 ---")
for line in cleanroom_recovery("2026-07-29","clean",   False, True,  True):  print(line)
print("\n--- attempt 3 ---")
for line in cleanroom_recovery("2026-07-29","clean",   True,  True,  True):  print(line)
EOF
```

**Expected result:** The first attempt is blocked on an infected recovery point, the second on a cleanroom that is not actually isolated, and the third proceeds through the full sequence. Note the ordering inside the successful run — **identity and DNS come before data and applications**, because an application restored without them is a machine that boots and cannot serve anyone. The final step matters too: production is left alone for forensics rather than being rebuilt over.

**Negative test:** Recovering into production "because it is faster" — you restore clean data into an environment that may still contain the attacker, and you destroy the evidence needed to find out how they got in.

**Cleanup:** None.

### Lab 7.2 — Dependency-ordered cloud recovery (Cloud Rewind)

**Objective:** Rebuild a cloud application in the correct order.

```bash
python3 - <<'EOF'
resources = {
  "vpc-network":      [],
  "iam-roles":        [],
  "security-groups":  ["vpc-network"],
  "rds-database":     ["vpc-network","security-groups","iam-roles"],
  "s3-buckets":       ["iam-roles"],
  "app-servers":      ["vpc-network","security-groups","iam-roles","rds-database","s3-buckets"],
  "load-balancer":    ["vpc-network","security-groups","app-servers"],
  "dns-records":      ["load-balancer"],
}
done, order = set(), []
while len(done) < len(resources):
    progressed = False
    for name, deps in resources.items():
        if name not in done and all(d in done for d in deps):
            done.add(name); order.append(name); progressed = True
    if not progressed:
        print("CIRCULAR DEPENDENCY — cannot resolve"); break

print("Dependency-ordered rebuild:")
for i, r in enumerate(order, 1):
    print(f"  {i}. {r:18} (needs: {', '.join(resources[r]) or 'nothing'})")
print("\nRestoring app-servers first would fail: no network, no identity, no database to connect to.")
EOF
```

**Expected result:** A topological order — network and IAM first, then security groups, then data services, then application servers, load balancer, and finally DNS. Cloud Rewind's value is exactly this: a cloud application is a dependency graph, and recovering it means **resolving that graph**, not restoring a list of resources alphabetically or by size.

**Negative test:** Restoring the highest-value resource first (the database, or the app servers) — each fails or comes up misconfigured because its prerequisites do not exist yet, and you spend the outage rebuilding in an order you discover by trial and error.

**Cleanup:** None.

### Lab 7.3 — Non-disruptive recovery rehearsal

**Objective:** Use the cleanroom to reach verification level 5.

```bash
python3 - <<'EOF'
def rehearsal(system, restored, app_starts, authenticates, data_current, rto_target_h, actual_h):
    checks = {"data restored":restored, "application starts":app_starts,
              "authentication works":authenticates, "data is current":data_current}
    passed = all(checks.values()) and actual_h <= rto_target_h
    print(f"\n{system}")
    for c, ok in checks.items():
        print(f"   [{'PASS' if ok else 'FAIL'}] {c}")
    print(f"   [{'PASS' if actual_h <= rto_target_h else 'FAIL'}] RTO: {actual_h}h vs {rto_target_h}h target")
    print(f"   => {'RECOVERABILITY PROVEN (level 5)' if passed else 'GAP FOUND — fix before you need it'}")

rehearsal("ERP (quarterly rehearsal)", True, True, True, True, rto_target_h=4, actual_h=3.2)
rehearsal("CRM (first rehearsal)",     True, True, False, True, rto_target_h=4, actual_h=6.5)
print("\nThe CRM rehearsal FOUND TWO REAL GAPS in a test — not during an incident. That is the point.")
EOF
```

**Expected result:** The ERP passes every check inside its RTO; the CRM fails authentication and overruns its RTO by 2.5 hours. Both outcomes are successes *of the rehearsal* — the CRM's gaps were discovered on a Tuesday afternoon in an isolated environment rather than at 3 a.m. during a real incident. Because the cleanroom is isolated and on-demand, this test costs no production downtime, which is what turns recovery rehearsal from an aspiration into a routine.

**Negative test:** Never rehearsing because "it would disrupt production" — the first real test is then the actual disaster, when the authentication gap is discovered with the business watching.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Cleanroom Recovery explained: isolated, clean, on-demand, complete.
- [ ] Recovery orchestrated from a Threat Scan-verified clean point, identity first.
- [ ] Cloud Rewind's dependency-ordered rebuild modeled with a topological sort.
- [ ] Non-disruptive rehearsal used to reach proven recoverability and surface gaps early.
