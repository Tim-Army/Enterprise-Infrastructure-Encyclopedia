# Chapter 09: Running a STIG Compliance Program

## Learning Objectives

- Place STIG work in the steps of the Risk Management Framework, from
  implementation through continuous monitoring.
- Choose the right disposition for a finding: remediate, mitigate, accept the
  risk, or justify it as Not Applicable.
- Write a Plan of Action and Milestones (POA&M) entry for an open finding.
- Keep systems compliant over time with golden images, pipeline scanning,
  quarterly updates, and drift detection.
- Compare STIGs with CIS Benchmarks and tailor a baseline outside DoD.

## Theory and Architecture

Hardening a system once is a project. Keeping hundreds of systems compliant
while STIGs change every quarter is a program. This chapter covers the program.

### STIGs in the Risk Management Framework

DoD authorizes systems through the RMF (DoDI 8510.01, built on NIST SP 800-37).
STIG work shows up in most of its steps:

| RMF step | STIG work |
| --- | --- |
| **Prepare / Categorize** | Identify the system boundary and every product in it, so you know which STIGs apply |
| **Select** | Controls are selected from 800-53 baselines; the applicable STIGs implement many of them |
| **Implement** | Build and configure systems to the STIGs; record deviations |
| **Assess** | The assessor reviews checklists, scan results, and evidence; findings are recorded against controls through their CCIs |
| **Authorize** | The Authorizing Official (AO) weighs residual risk, including open findings and their POA&M entries, and decides on an ATO |
| **Monitor** | Rescan and reassess as systems change and STIGs update; keep the POA&M current |

STIG results flow into the authorization package as evidence. In DoD, that
package lives in eMASS, and the CCIs on each finding tie it to the 800-53
controls it affects.

### Finding dispositions

Every Open finding needs a decision. There are only a few legitimate ones:

| Disposition | When to use it | What you document |
| --- | --- | --- |
| **Remediate** | The fix is feasible | The change, and evidence it worked; status becomes Not a Finding |
| **Mitigate** | The fix is not feasible, but other controls reduce the risk | The compensating controls and evidence; this may support a reduced severity, subject to the assessor and AO |
| **Accept the risk** | Neither fix nor adequate mitigation is available now | A POA&M entry with milestones, or a formal risk acceptance by the AO |
| **Not Applicable** | The rule cannot apply to this asset | An asset-specific reason; the status is Not Applicable rather than Open |
| **False positive** | The scanner was wrong | Evidence that the system meets the rule; status becomes Not a Finding |

Two traps are common. A **product limitation** (the product cannot do what the
rule asks) is a finding to mitigate or accept, not Not Applicable. And a
**severity override** is not a way to make findings go away; it needs a
documented mitigation, and the assessor and AO decide whether it stands.

### The POA&M

A **Plan of Action and Milestones (POA&M)** records each weakness that is not
yet resolved and the plan to resolve it. A useful entry contains:

| Field | Example |
| --- | --- |
| Weakness | Session idle timeout exceeds the required limit on the reporting application |
| Source | Application STIG, Group ID and STIG ID |
| Severity | CAT II |
| Affected assets | Host names or the asset group |
| Point of contact | The responsible engineer or team |
| Resources required | Vendor upgrade to a release that supports configurable timeouts |
| Milestones | Vendor upgrade tested by a date; deployed by a later date |
| Scheduled completion | A realistic date the AO agrees to |
| Mitigation in place | Network access to the application restricted to the admin VLAN |
| Status | Ongoing, completed, or risk accepted |

### Keeping compliance over time

Compliance decays unless the process enforces it:

```text
          ┌───────────── quarterly STIG release ─────────────┐
          ▼                                                  │
  Golden image ──► Deploy ──► Scheduled scans ──► Drift?─────┤
  (STIG applied,                 │                 yes │     │
   scanned in CI)                ▼                     ▼     │
                           Checklists in        Remediate or │
                           STIG Manager/eMASS   update POA&M─┘
```

- **Golden images.** Build machine images with the STIG applied (Packer plus
  Ansible is common), scan them in the pipeline, and deploy only images that
  pass. New systems start compliant.
- **Pipeline gates.** Fail a build when a scan finds a new CAT I, or when the
  compliance score drops below the agreed threshold.
- **Scheduled scans.** Rescan running systems on a fixed cadence to catch drift,
  and always after patching.
- **Configuration management.** Group Policy, DSC, or Ansible runs that
  reassert the baseline correct drift automatically.
- **Quarterly updates.** When DISA releases new content, review the revision
  history, update the content in your tools, rescan, and plan remediation for
  newly added rules.

### Measuring the program

A few metrics show whether the program works:

- Open CAT I findings across the estate (the target is zero, or zero not under
  an approved POA&M).
- Compliance percentage by severity and by system.
- Mean time to remediate new findings, by severity.
- POA&M items past their scheduled completion date.
- Assets with a checklist older than the current STIG release.

### STIGs and CIS Benchmarks

Outside DoD, the main alternative to STIGs is the CIS Benchmarks. Both are
listed in NIST's National Checklist Program (NIST SP 800-70).

| | DISA STIGs | CIS Benchmarks |
| --- | --- | --- |
| Publisher | DISA (U.S. DoD) | Center for Internet Security (consensus process) |
| Cost | Free | Benchmarks free as PDFs; some tooling and build kits require membership |
| Profiles | One baseline per STIG, all rules expected | Level 1 (practical baseline) and Level 2 (defense in depth) |
| Traceability | CCI to NIST SP 800-53 | Mapped to CIS Controls and other frameworks |
| Required for | DoD systems | Not mandated by DoD; common in commercial and regulated sectors |
| Strictness | Generally stricter, with DoD-specific items | Generally more tunable, especially Level 1 |

Commercial organizations often use STIGs as a stricter reference while
operating to CIS Level 1, or tailor the STIG by documenting excluded rules.
Either way, the baseline should be written down and its exceptions recorded.

## Design Considerations

- **Pick one system of record** for checklists and findings (STIG Manager,
  eMASS, or a GRC tool), and make every team use it.
- **Assign owners by system, not by STIG.** One owner per system who answers for
  all its findings is clearer than one owner per STIG across many systems.
- **Set dispositions with the assessor early.** Agree which mitigations support
  a severity reduction and what evidence satisfies process-heavy rules before
  assessment, not during it.
- **Keep POA&M dates honest.** An entry that rolls its date every quarter erodes
  the AO's trust in the whole package.
- **Automate the boring parts.** Scanning, checklist import, and reporting
  should be automated, so people spend their time on manual rules and decisions.

## Implementation and Automation

Scan results become much more useful as a findings register. This script reads
an XCCDF results file or an ARF file from OpenSCAP or SCC and writes every
failed rule to CSV. It matches elements by local name, so it works with
XCCDF 1.1 and 1.2 output:

```python
#!/usr/bin/env python3
"""Write failed rules from an XCCDF or ARF results file to CSV."""
import csv
import sys
import xml.etree.ElementTree as ET

def local(tag):
    return tag.rsplit("}", 1)[-1]

tree = ET.parse(sys.argv[1])
rules = {}
for el in tree.iter():
    if local(el.tag) == "Rule":
        title = next((c.text for c in el if local(c.tag) == "title"), "")
        rules[el.get("id")] = (el.get("severity", ""), (title or "").strip())

out = csv.writer(sys.stdout)
out.writerow(["rule_id", "severity", "title", "disposition", "owner", "due_date"])
for el in tree.iter():
    if local(el.tag) != "rule-result":
        continue
    result = next((c.text for c in el if local(c.tag) == "result"), "")
    if result == "fail":
        sev, title = rules.get(el.get("idref"), (el.get("severity", ""), ""))
        out.writerow([el.get("idref"), el.get("severity") or sev, title, "", "", ""])
```

```bash
python3 findings2csv.py /tmp/disa-xccdf-results.xml > findings.csv
```

Open `findings.csv` in a spreadsheet, fill in the disposition, owner, and due
date for each row, and move anything not remediated into the POA&M.

## Validation and Troubleshooting

- **The register is empty.** The file may contain only passes, or the results
  use a different structure. Check that `rule-result` elements exist
  (`grep -c rule-result <file>`).
- **Severity is blank for some rows.** Some content records severity only on the
  rule definition. The script falls back to the rule; if that is missing too,
  look the rule up in the STIG.
- **POA&M items keep slipping.** Look for missing resources or ownership. A
  slipping date is a planning problem, not a reporting one.
- **Compliance dropped with no system change.** A new quarterly release added
  rules. Compare release numbers and the revision history before investigating
  the systems.
- **Two tools disagree on compliance.** Check that both use the same STIG
  release and the same content type (DISA benchmark or ComplianceAsCode).

## Security and Best Practices

- Treat open CAT I findings as incidents waiting to happen. Remediate or
  formally accept them quickly, and never leave one without an owner.
- Keep evidence with every disposition. A mitigation or Not Applicable without
  evidence will not survive assessment.
- Protect findings registers and POA&Ms; they list every known weakness.
- Revisit risk acceptances on a schedule. Conditions change, and an accepted
  risk may become fixable or more serious.
- Rescan after every significant change, not only on the schedule.

## References and Knowledge Checks

**References:**

- NIST SP 800-37 Rev. 2, *Risk Management Framework for Information Systems and
  Organizations*; DoDI 8510.01, *RMF for DoD Systems*.
- NIST SP 800-70, *National Checklist Program for IT Products*, and the
  National Checklist Program repository (`ncp.nist.gov`).
- Center for Internet Security, CIS Benchmarks (`cisecurity.org`).
- STIG Manager documentation (`github.com/NUWCDIVNPT/stig-manager`).

**Knowledge checks:**

1. In which RMF steps does STIG work appear, and what does it contribute to
   each?
2. What is the difference between mitigating a finding and accepting its risk?
3. Why is a product limitation not Not Applicable?
4. List the fields a useful POA&M entry contains.
5. Give three ways to keep systems compliant as STIGs change each quarter.
6. How do STIGs and CIS Benchmarks differ in profiles and traceability?

## Summary and Completion Checklist

A STIG program keeps systems compliant over time. Within the RMF, STIGs are
implemented in builds, assessed as evidence through their CCIs, weighed by the
AO at authorization, and monitored continuously. Every open finding gets a real
disposition, and unresolved ones go into a POA&M with honest milestones. Golden
images, pipeline gates, scheduled scans, configuration management, and a
quarterly update routine keep compliance from decaying. Outside DoD, STIGs and
CIS Benchmarks are both valid baselines, as long as the choice and its
exceptions are documented.

- [ ] Can place STIG work in each RMF step.
- [ ] Can choose and justify finding dispositions.
- [ ] Can write a complete POA&M entry.
- [ ] Can describe how to keep compliance over time and measure it.
