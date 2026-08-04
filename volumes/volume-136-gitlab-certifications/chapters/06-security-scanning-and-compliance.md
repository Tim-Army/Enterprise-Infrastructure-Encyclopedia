# Chapter 06: Security Scanning and Compliance

## Learning Objectives

- Configure the scanner set: SAST, DAST, secret detection, dependency, and container scanning.
- Read findings in the merge request and manage the vulnerability lifecycle.
- Enforce security policies and merge-request approval rules.
- Apply license compliance to dependencies.

## Shift left, concretely

This is the **Certified Security Associate** material, and GitLab's premise is that security scanning belongs **in the pipeline**, surfacing findings in the merge request where the author can still fix them cheaply — rather than in a quarterly report that arrives after release.

| Scanner | Finds | Runs against |
|:---|:---|:---|
| **SAST** (static) | Vulnerable patterns in your source | Source code, no execution |
| **DAST** (dynamic) | Vulnerabilities in a running application | A deployed instance |
| **Secret detection** | Credentials and tokens committed to the repository | Repository history and diffs |
| **Dependency scanning** | Known CVEs in the libraries you depend on | Lock files and manifests |
| **Container scanning** | Known CVEs in image layers and OS packages | Built container images |
| **License compliance** | Dependency licenses violating policy | Dependency metadata |

Two distinctions the exams probe:

- **SAST vs DAST** — static reads code without running it (broad coverage, more false positives, finds issues DAST cannot see); dynamic exercises a running app (fewer false positives, but only covers paths it actually reaches). They are complementary, not alternatives.
- **Dependency vs container scanning** — dependency scanning covers *your application's* libraries; container scanning covers the *image*, including base-OS packages you never chose explicitly. Most real CVE counts come from base images.

## Secret detection deserves special handling

A leaked credential is different from other findings in one crucial way: **removing it from the code does not fix it.** Git history retains the secret, and anyone who cloned or forked the repository already has it.

The correct response order is: **rotate the credential first**, then remove it from the code, then consider history rewriting. Teams routinely do this backwards — deleting the line, closing the finding, and leaving a live credential in the history of a repository with fifty forks.

## The vulnerability lifecycle

Findings are not simply "fix or ignore." GitLab tracks a state: **Detected → Confirmed / Dismissed → Resolved**, where dismissal requires a reason (false positive, acceptable risk, mitigating control). The audit value comes from the dismissal reason being recorded and attributable, not from the count reaching zero.

## Policies and approvals

Two enforcement mechanisms:

- **Scan execution policies** — require particular scanners to run on particular projects, enforced at group level so a project cannot simply delete them from its CI file.
- **Merge request approval rules / scan result policies** — require approval from a named group (say, AppSec) when a scan finds issues above a severity threshold.

The reason policies live at group level is precisely that a project-level CI file can be edited by anyone who can push. A control that the controlled party can switch off is not a control.

## Hands-On Lab

Python models security scanning. **Cost:** none.

### Lab 6.1 — Route findings from the right scanner

**Objective:** Map a vulnerability class to the scanner that detects it.

```bash
python3 - <<'EOF'
findings = [
  {"issue":"SQL built by string concatenation",   "where":"src/db.py",             "detector":"SAST"},
  {"issue":"Reflected XSS on /search",            "where":"running app",           "detector":"DAST"},
  {"issue":"AWS key committed in config",         "where":"config/settings.yml",   "detector":"Secret detection"},
  {"issue":"CVE-2025-1234 in requests 2.19",      "where":"requirements.txt",      "detector":"Dependency scanning"},
  {"issue":"CVE-2024-9999 in base image openssl", "where":"debian:11 base layer",  "detector":"Container scanning"},
  {"issue":"GPL-3.0 dependency in proprietary product","where":"package-lock.json","detector":"License compliance"},
]
for f in findings:
    print(f"{f['detector']:20} {f['issue']:44} [{f['where']}]")

print("\nWhy you need more than one:")
print("  SAST reads code without running it   -> finds the SQL pattern; cannot confirm exploitability")
print("  DAST exercises the running app       -> confirms the XSS; blind to code paths it never reaches")
print("  Dependency  = YOUR libraries         |  Container = the IMAGE incl. base-OS packages")
print("  Most raw CVE counts come from BASE IMAGES, not from code you wrote —")
print("  which is why 'update the base image' is usually the highest-yield single fix.")
EOF
```

**Expected result:** Each finding maps to exactly one detector, and the notes explain the complementarity. The base-image observation is the practically valuable one: teams confronted with hundreds of container CVEs often start triaging individually when rebuilding on a current base image resolves most of them at once.

**Negative test:** Running SAST only and declaring the application scanned — you have no coverage of runtime behavior, dependency CVEs, committed secrets, or the base image, which between them account for most real incidents.

**Cleanup:** None.

### Lab 6.2 — Secret detection: rotate before you delete

**Objective:** Get the remediation order right.

```bash
python3 - <<'EOF'
def remediate(steps_taken):
    correct = ["rotate", "remove", "history"]
    print(f"steps in order: {steps_taken}")
    if not steps_taken or steps_taken[0] != "rotate":
        print("   WRONG ORDER — the credential is STILL VALID.")
        print("   Git history retains it, and every existing clone/fork already has a copy.")
        print("   Deleting the line closes the finding while the secret keeps working.\n")
        return False
    print("   CORRECT — credential invalidated first, so the copies in history are worthless.\n")
    return True

remediate(["remove", "history", "rotate"])
remediate(["remove"])
remediate(["rotate", "remove", "history"])

print("Secret findings differ from every other class: removal does NOT remediate.")
print("Order: 1) ROTATE the credential  2) remove from code  3) consider history rewrite")
print("   ...and treat the secret as compromised from the moment it was pushed, not from detection.")
EOF
```

**Expected result:** Only the rotate-first sequence is correct. The final line is the part people resist: the exposure window began at **push time**, not at detection, so a secret found six months later has been readable by anyone with repository access for six months and must be treated as compromised regardless of whether you can prove misuse.

**Negative test:** Rewriting history to purge the secret without rotating — an expensive, disruptive operation (every collaborator must re-clone) that leaves the credential fully valid in every fork and local copy made beforehand.

**Cleanup:** None.

### Lab 6.3 — Approval policy gates on scan results

**Objective:** Gate merges on severity, and see why the policy belongs at group level.

```bash
python3 - <<'EOF'
POLICY = {"block_severities": ["critical","high"], "approver_group": "AppSec", "min_approvals": 1}

def merge_decision(findings, approvals, policy_level):
    blocking = [f for f in findings if f["severity"] in POLICY["block_severities"] and f["state"] == "Detected"]
    if policy_level == "project":
        note = "  (policy defined in the project's .gitlab-ci.yml — anyone who can push can delete it)"
    else:
        note = "  (policy enforced at GROUP level — the project cannot switch it off)"
    if not blocking:
        return "MERGE ALLOWED — no open critical/high findings" + note
    if approvals.get(POLICY["approver_group"], 0) >= POLICY["min_approvals"]:
        return (f"MERGE ALLOWED — {len(blocking)} blocking finding(s), but {POLICY['approver_group']} "
                f"approved (accepted risk, recorded)") + note
    return (f"MERGE BLOCKED — {len(blocking)} finding(s) at {POLICY['block_severities']} "
            f"require {POLICY['approver_group']} approval") + note

f_clean = [{"severity":"low","state":"Detected"}]
f_bad   = [{"severity":"critical","state":"Detected"}, {"severity":"medium","state":"Detected"}]
f_dismissed = [{"severity":"critical","state":"Dismissed"}]

print(merge_decision(f_clean, {}, "group"), "\n")
print(merge_decision(f_bad, {}, "group"), "\n")
print(merge_decision(f_bad, {"AppSec":1}, "group"), "\n")
print(merge_decision(f_dismissed, {}, "group"), "\n")
print(merge_decision(f_bad, {}, "project"))
print("\nA control the controlled party can edit is not a control — which is exactly why scan")
print("execution and scan result policies are defined at GROUP level, above the project's CI file.")
EOF
```

**Expected result:** Clean and dismissed findings merge; open critical findings block until AppSec approves, which records an accepted risk rather than silently allowing it. The final case makes the governance point — a project-level policy is advisory, because the same people it constrains can remove it in the file they already control.

**Negative test:** Blocking on *all* severities including informational — merges stall on findings nobody intends to fix, teams demand exceptions, and the exception becomes the norm, which is how security gates get switched off entirely.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The scanner set configured, with SAST/DAST and dependency/container distinctions clear.
- [ ] Base images recognized as the usual source of container CVE volume.
- [ ] Secret findings remediated rotate-first, with exposure dated from push not detection.
- [ ] Vulnerability lifecycle states used, with dismissal reasons recorded.
- [ ] Approval and scan policies enforced at group level, above the project's own CI file.
