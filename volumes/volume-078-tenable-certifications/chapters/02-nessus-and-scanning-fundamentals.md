# Chapter 02: Nessus and Scanning Fundamentals

## Learning Objectives

- Describe the Nessus scanner and plugin architecture.
- Configure scan policies and templates.
- Distinguish credentialed from uncredentialed scans.
- Interpret scan results and plugins.
- Complete a walkthrough for each scanning fundamental.

## Theory and Architecture

**Nessus** is Tenable's vulnerability scanner and the engine beneath the whole platform. It assesses
targets against a library of **plugins** — small programs (written in NASL, the Nessus Attack
Scripting Language) that each check for a specific vulnerability, misconfiguration, or piece of
information; Tenable publishes new plugins continuously as vulnerabilities emerge. A **scan** is
defined by a **policy/template** (what to check and how) plus **targets** (which assets). The most
important distinction is **credentialed vs uncredentialed** scanning: an **uncredentialed** scan sees
a target only from the network (like an outside attacker), while a **credentialed** (authenticated)
scan logs in and inspects installed software, patches, and configuration — far more accurate, with
fewer false positives. Results list **findings** with severity, and Nessus deduplicates and
categorizes them. Understanding the scanner, plugins, policies, and credentialed scanning is the
foundation for every Tenable product. This chapter teaches each with a hands-on defensive walkthrough
(policy logic, credentialed reasoning, and result interpretation).

## Design Considerations

Prefer **credentialed** scans for accuracy. Choose the right **template** (basic, advanced,
compliance) for the goal. **Schedule** regular scans and keep **plugins** updated. Scope targets to
**authorized** assets. Tune to reduce false positives. Protect **scan credentials** (store them in a
vault, least privilege).

## Implementation and Automation

The labs reason about plugins, build a scan policy, compare credentialed scans, and read results.

## Validation and Troubleshooting

Confirm the scanning fundamentals:

```text
Nessus = scanner; plugins (NASL) = per-vulnerability checks, continuously updated. Scan = policy/template + targets.
Credentialed (authenticated, accurate) vs uncredentialed (network-only, attacker view). Results = findings by severity.
```

Common pitfalls: **uncredentialed-only** scanning (misses patch-level detail, more false positives);
and scanning **unauthorized** targets.

## Security and Best Practices

Use **credentialed** scans, keep **plugins** current, scope to **authorized** assets, schedule
regularly, and protect **scan credentials**. Tune false positives. All work is defensive.

## Hands-On Lab

Scanning walkthroughs. **Shared prerequisites** — `python3`, and Nessus Essentials against
**authorized** lab targets only. **Cost:** none (Nessus Essentials is free).

### Lab 2.1 — Understand plugins and severity

**Objective:** Read what a plugin reports.

```python
python3 - <<'PY'
plugins=[{"id":19506,"name":"Nessus Scan Information","sev":"Info"},
         {"id":51192,"name":"SSL Certificate Cannot Be Trusted","sev":"Medium"},
         {"id":97833,"name":"Missing OS security update","sev":"Critical"}]
for p in plugins: print(f"plugin {p['id']:>6} [{p['sev']:8}] {p['name']}")
print("Nessus: each plugin checks one issue; severity guides attention")
PY
```

**Expected result:** plugins with **IDs and severities** — how Nessus reports findings.

**Negative test:** treat every Info plugin as a vulnerability; **Info** is context, not risk — focus
on real severities.

**Cleanup:** none.

### Lab 2.2 — Build a scan policy

**Objective:** Define what to scan and how.

```python
python3 - <<'PY'
policy={"template":"Advanced Network Scan","targets":"10.10.0.0/24 (authorized lab)",
        "port_scan":"common + service detection","credentials":"SSH/Windows (least-priv scan account)",
        "schedule":"weekly"}
for k,v in policy.items(): print(f"{k:12}: {v}")
PY
```

**Expected result:** a scan **policy** with authorized targets and credentials — the scan definition.

**Negative test:** point a scan at an address you're not authorized to assess; that's prohibited —
scope to **authorized** assets.

**Cleanup:** none.

### Lab 2.3 — Compare credentialed vs uncredentialed

**Objective:** See why authentication matters.

```python
python3 - <<'PY'
uncred={"open ports":["443","22"],"os_patch_detail":None,"false_positives":"higher"}
cred  ={"open ports":["443","22"],"os_patch_detail":"12 missing patches (CVE list)","false_positives":"lower"}
print("uncredentialed:", uncred)
print("credentialed  :", cred)
print("Credentialed scans see installed software/patches -> accurate, fewer false positives")
PY
```

**Expected result:** the credentialed scan reveals **patch-level detail** the uncredentialed misses —
the value of authentication.

**Negative test:** rely on uncredentialed scans for patch management; they can't see installed
patches — use **credentialed** scans.

**Cleanup:** none.

### Lab 2.4 — Interpret and triage results

**Objective:** Turn findings into action.

```python
python3 - <<'PY'
findings=[{"host":"web01","plugin":"missing patch","sev":"Critical","exploitable":True},
          {"host":"web01","plugin":"weak cipher","sev":"Medium","exploitable":False},
          {"host":"pc22","plugin":"info banner","sev":"Info","exploitable":False}]
actionable=[f for f in findings if f["sev"] in ("Critical","High") and f["exploitable"]]
print("triage -> fix first:", [(f["host"],f["plugin"]) for f in actionable])
PY
```

**Expected result:** the exploitable **Critical** finding surfaced for first action — result triage.

**Negative test:** work findings alphabetically; you fix info-level items before critical exploitable
ones — **triage by risk**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Nessus scans targets against continuously-updated plugins per a policy, and credentialed scanning
delivers accurate, low-false-positive results — the scanning foundation beneath every Tenable
product.

- [ ] I can explain plugins and severity.
- [ ] I can build a scan policy.
- [ ] I can compare credentialed vs uncredentialed scans.
- [ ] I can triage results by risk.
- [ ] I completed Labs 2.1–2.4 including each negative test.
