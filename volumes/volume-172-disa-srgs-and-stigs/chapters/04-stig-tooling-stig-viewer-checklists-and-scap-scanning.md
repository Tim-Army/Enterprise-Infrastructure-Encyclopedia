# Chapter 04: STIG Tooling — STIG Viewer, Checklists, and SCAP Scanning

## Learning Objectives

- Create, complete, and export a STIG checklist in STIG Viewer, using the four
  finding statuses correctly.
- Explain the difference between the CKL and CKLB checklist formats.
- Run a SCAP scan with the SCAP Compliance Checker or OpenSCAP and explain what
  a SCAP scan can and cannot tell you.
- Distinguish DISA's SCAP benchmarks from the community ComplianceAsCode
  content, and know why their results do not import the same way.
- Describe the tools used to automate manual checks and manage assessments at
  scale: Evaluate-STIG, STIG Manager, and eMASS.

## Theory and Architecture

A STIG assessment produces one artifact above all others: a **checklist**. A
checklist is a copy of one or more STIGs for a specific **asset** (a host,
device, or application instance), with a status, finding details, and comments
recorded against every rule. Tools either help you fill in the checklist or
help you manage many of them.

### The finding statuses

Every rule in a checklist ends in exactly one of four states:

| Status | Use it when | Required evidence |
| --- | --- | --- |
| **Open** | The asset does not meet the rule | What you observed, and the plan to fix or mitigate |
| **Not a Finding** | The asset meets the rule | How you verified it (command output, setting, screenshot) |
| **Not Applicable** | The rule cannot apply to this asset | Why, specific to the asset (for example, "no wireless hardware present") |
| **Not Reviewed** | Nobody has assessed it yet | None; an assessment is not complete while any rule is Not Reviewed |

Severity can be changed on an individual finding (a *severity override*), but
only with a written justification, typically a documented mitigation. Chapter 09
covers when that is allowed.

### Checklist formats

| Format | Extension | Structure | Produced by |
| --- | --- | --- | --- |
| **CKL** | `.ckl` | XML | STIG Viewer 2.x and many older tools |
| **CKLB** | `.cklb` | JSON | STIG Viewer 3.x and newer tools |

**STIG Viewer** is DISA's free desktop application for reading STIGs and
completing checklists. Version 3 introduced the JSON-based CKLB format and a
redesigned interface; version 2 used XML-based CKL files. Most current tools
read both. Confirm which format your organization's repository and eMASS
workflow expect before standardizing.

### SCAP scanning

A **SCAP scanner** evaluates the automatable part of a STIG by running OVAL
checks against a live system and writing XCCDF results. Two families of content
exist, and the difference matters:

| | DISA SCAP benchmarks | ComplianceAsCode (SCAP Security Guide) |
| --- | --- | --- |
| Published by | DISA, on the DoD Cyber Exchange | The open-source ComplianceAsCode project, shipped by Linux vendors |
| Rule identifiers | DISA rule IDs (match the STIG's Group IDs) | ComplianceAsCode rule names (for example `accounts_passwords_pam_faillock_deny`) |
| Typical scanner | SCAP Compliance Checker (SCC) | OpenSCAP (`oscap`) |
| Imports into a STIG checklist | Directly | Not directly; IDs do not match |
| Remediation content | None | Bash, Ansible, and other fix scripts |

The **SCAP Compliance Checker (SCC)**, developed by Naval Information Warfare
Center (NIWC) Atlantic and distributed through the DoD Cyber Exchange, runs
DISA's SCAP benchmarks on Windows, Linux, and macOS. **OpenSCAP** is the
open-source scanner shipped with RHEL and other distributions. It runs the
ComplianceAsCode content, which includes a `stig` profile aligned with the DISA
STIG and can also generate remediation scripts. OpenSCAP can usually evaluate
DISA's SCAP benchmarks too, which produces results with DISA identifiers.

Whatever the scanner, remember the limit: **a SCAP scan covers only the
automatable rules.** A clean SCAP report is not a clean STIG. The manual rules
still need review.

### Automating manual checks and managing at scale

| Tool | Purpose | Availability |
| --- | --- | --- |
| **Evaluate-STIG** | A PowerShell-based tool that automates many manual STIG checks across Windows, Linux, and supported applications, and writes completed checklists | Developed by NAVSEA; distributed to DoD users through the DoD Cyber Exchange |
| **STIG Manager** | An open-source web application for managing STIG assessments across many assets: import checklists and scan results, review, track, and report | Open source, from Naval Undersea Warfare Center Division Newport (NUWCDIVNPT) |
| **eMASS** | The Enterprise Mission Assurance Support Service, DoD's RMF system of record, where checklists and scan results become authorization evidence | DoD only |

## Design Considerations

- **Decide the system of record.** Small teams can keep CKLB files in a
  repository. Anything larger needs STIG Manager or an equivalent, or results
  scatter across laptops.
- **Use DISA SCAP benchmarks for evidence, ComplianceAsCode for remediation.**
  DISA benchmark results map straight into checklists. ComplianceAsCode is
  better at fixing things and at scanning in pipelines (Chapters 05 and 09).
- **Budget for the manual remainder.** Plan reviewer time for the rules SCAP
  does not cover, or use Evaluate-STIG where you are eligible to.
- **Standardize asset data.** Checklists carry host name, IP address, role, and
  technology area. Inconsistent asset data makes reporting across hundreds of
  checklists painful.
- **Keep the scanner and content current.** A new STIG release needs the
  matching SCAP benchmark and, often, a scanner update.

## Implementation and Automation

### STIG Viewer

Download STIG Viewer from the DoD Cyber Exchange (it is distributed as a ZIP for
Windows and Linux), unpack it, and run the executable. The basic workflow:

1. **Load the STIG.** Import the STIG ZIP or XCCDF file into the library.
2. **Create a checklist.** Create a checklist from one or more STIGs for an
   asset (an operating system STIG plus application STIGs for the same host is
   common).
3. **Enter asset information.** Host name, IP, MAC, FQDN, role, and technology
   area.
4. **Assess each rule.** Set the status, and record finding details (what you
   saw) and comments (context, ticket numbers, mitigations).
5. **Import automated results.** Where available, import XCCDF results from a
   SCAP scan so automatable rules fill in, then review the remainder by hand.
6. **Export.** Save the checklist as CKLB (or CKL where required).

### OpenSCAP with ComplianceAsCode content (RHEL family)

```bash
sudo dnf install -y openscap-scanner scap-security-guide
ls /usr/share/xml/scap/ssg/content/            # one data stream per platform
oscap info /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml | grep -i stig
```

Scan against the STIG profile and produce an HTML report and machine-readable
results:

```bash
sudo oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_stig \
  --results-arf /tmp/stig-arf.xml \
  --report /tmp/stig-report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```

`oscap` returns exit code `2` when at least one rule fails. That is normal for
a first scan and not an error in the command.

### OpenSCAP with a DISA SCAP benchmark

Download the DISA SCAP benchmark for the platform, unzip it, find the DISA
profile names, and evaluate:

```bash
unzip <DISA_SCAP_BENCHMARK_ZIP>.zip -d disa-scap
oscap info disa-scap/<BENCHMARK_FILE>.xml | grep -i profile
sudo oscap xccdf eval \
  --profile <DISA_PROFILE_ID> \
  --results /tmp/disa-xccdf-results.xml \
  --report /tmp/disa-report.html \
  disa-scap/<BENCHMARK_FILE>.xml
```

The `--results` file uses DISA rule identifiers, so STIG Viewer and STIG
Manager can import it into a checklist for that host.

## Validation and Troubleshooting

- **`oscap` exits with code 2.** At least one rule failed. Code `1` is a real
  error (bad profile name, unreadable file).
- **"Profile not found."** List profiles with `oscap info <file>` and copy the
  ID exactly. DISA and ComplianceAsCode profile IDs look different.
- **Importing scan results changes nothing in the checklist.** The results were
  produced from ComplianceAsCode content, whose rule IDs do not match the DISA
  STIG. Use a DISA SCAP benchmark for checklist evidence.
- **Results show "notchecked" for many rules.** Those are manual rules, or rules
  whose OVAL could not run. Review them by hand.
- **A checklist opens in one tool but not another.** Check whether it is CKL or
  CKLB, and whether the tool supports that format.
- **Scan results differ from last quarter with no system change.** The STIG or
  benchmark release changed. Compare release numbers before investigating the
  host.

## Security and Best Practices

- Run scanners with the least privilege that produces accurate results.
  Unprivileged scans miss settings that only root or an administrator can read,
  which produces false Open findings.
- Protect checklists and scan results. They are a map of every weakness on the
  system and may themselves be sensitive or controlled.
- Record evidence in Finding Details for every Not a Finding, not just for Open
  items. An assessor should be able to verify the status without logging in.
- Never mark a rule Not a Finding based only on a SCAP pass if the rule's check
  text includes manual steps the OVAL does not cover.

## References and Knowledge Checks

**References:**

- DISA STIG Viewer and its user guide, on the DoD Cyber Exchange.
- SCAP Compliance Checker (SCC), on the DoD Cyber Exchange SCAP tools page.
- OpenSCAP project (`open-scap.org`) and the `oscap` manual page.
- ComplianceAsCode content project (`github.com/ComplianceAsCode/content`).
- STIG Manager (`github.com/NUWCDIVNPT/stig-manager`).

**Knowledge checks:**

1. Name the four checklist statuses and the evidence each requires.
2. What is the practical difference between CKL and CKLB?
3. Why can results from a ComplianceAsCode STIG-profile scan not be imported
   directly into a DISA STIG checklist?
4. What does a clean SCAP report not tell you?
5. What does Evaluate-STIG add on top of a SCAP scan?

## Summary and Completion Checklist

A STIG assessment produces checklists: one per asset, with every rule set to
Open, Not a Finding, Not Applicable, or Not Reviewed, plus evidence. STIG Viewer
creates and edits them, in CKL (XML) or CKLB (JSON) format. SCAP scanners fill
in the automatable rules. DISA's SCAP benchmarks produce results that import
into checklists, while ComplianceAsCode content is better for remediation and
pipelines. Manual rules remain, which Evaluate-STIG helps with in DoD, and STIG
Manager and eMASS manage results at scale.

- [ ] Can use the four finding statuses correctly, with evidence.
- [ ] Can explain CKL versus CKLB.
- [ ] Can run an OpenSCAP scan with both content types.
- [ ] Can explain why ComplianceAsCode results do not import into a DISA
      checklist.
