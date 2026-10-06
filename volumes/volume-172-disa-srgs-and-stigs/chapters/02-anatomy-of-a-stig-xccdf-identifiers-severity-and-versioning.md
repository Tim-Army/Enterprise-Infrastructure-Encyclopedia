# Chapter 02: Anatomy of a STIG — XCCDF, Identifiers, Severity, and Versioning

## Learning Objectives

- Read a DISA STIG XCCDF file and identify the benchmark, profiles, groups, and
  rules it contains.
- Explain each identifier attached to a rule: Group ID, Rule ID, STIG ID, SRG
  ID, and CCI, and which ones stay stable across releases.
- Map XCCDF severity values to the CAT I, CAT II, and CAT III categories and
  explain what each category means for risk.
- Interpret the version and release numbering of a STIG and its benchmark date.
- Distinguish a manual STIG from a SCAP benchmark, and parse a STIG with a short
  script.

## Theory and Architecture

Every STIG is an **XCCDF** document. XCCDF, the Extensible Configuration
Checklist Description Format, is a NIST-maintained XML language for security
checklists and part of the Security Content Automation Protocol (SCAP). DISA's
manual STIGs use XCCDF 1.1; the SCAP benchmarks use XCCDF 1.2 inside SCAP data
streams. The structure is the same idea in both.

### Document structure

```text
Benchmark                      the STIG: title, version, release, date
├── Profile (×9)               MAC-1/2/3 × Classified/Sensitive/Public
└── Group  id="V-######"       one per requirement
    ├── title                  the SRG ID (SRG-OS-000480-GPOS-00227)
    └── Rule id="SV-######r######_rule"  severity="medium"
        ├── version            the STIG ID (RHEL-09-######)
        ├── title              a one-line statement of the requirement
        ├── description        VulnDiscussion: why the rule matters
        ├── ident              CCI-###### (one or more)
        ├── fixtext            how to remediate
        └── check/check-content   how to verify
```

A few elements deserve attention:

- **Profiles.** Manual STIGs carry nine profiles named for the old DoD **Mission
  Assurance Category (MAC)** levels (I, II, III) crossed with confidentiality
  levels (Classified, Sensitive, Public). In current STIGs nearly all rules
  appear in every profile, so most teams ignore the profile and assess every
  rule. The profiles are a holdover from the DIACAP era that preceded RMF.
- **Groups and rules.** Each requirement is a `Group` holding exactly one
  `Rule`. Tools treat the pair as a single item usually called a "vulnerability"
  or "finding."
- **Descriptions.** The rule's `description` contains escaped markup. The useful
  part is the `VulnDiscussion` block, which explains the risk the rule
  addresses. Read it before deviating from a rule.

### The identifiers

A single rule carries five identifiers. Knowing which ones change between
releases matters, because checklists and findings are tracked by them.

| Identifier | Example form | Meaning | Stability |
| --- | --- | --- | --- |
| **Group ID** (Vuln ID) | `V-257777` | The requirement within this STIG | Stable across releases; the primary key most tools use |
| **Rule ID** | `SV-257777r925318_rule` | A specific revision of the rule | The `r` suffix changes when the rule text changes |
| **STIG ID** | `RHEL-09-211010` | Human-readable product rule number | Generally stable; carried in the rule's `version` element |
| **SRG ID** | `SRG-OS-000480-GPOS-00227` | The SRG requirement this rule implements | Stable; shared by every STIG that implements it |
| **CCI** | `CCI-000366` | The atomic control statement, mapped to 800-53 | Stable |

Two practical rules follow. When you compare results between two releases of
the same STIG, join on the **Group ID**. When you compare across products (for
example, "how does every OS STIG handle lockout?"), join on the **SRG ID** or
**CCI**.

The specific numbers above illustrate the formats. Always read real values
from the current STIG rather than copying them from documentation, because
numbers are reassigned when products and releases change.

### Severity categories

XCCDF uses `severity="high|medium|low"`. DoD expresses the same thing as a
**Category (CAT)**:

| XCCDF severity | Category | Meaning |
| --- | --- | --- |
| `high` | **CAT I** | Any vulnerability whose exploitation will directly and immediately result in loss of confidentiality, availability, or integrity |
| `medium` | **CAT II** | Any vulnerability whose exploitation has a potential to result in loss of confidentiality, availability, or integrity |
| `low` | **CAT III** | Any vulnerability whose existence degrades measures to protect against loss of confidentiality, availability, or integrity |

CAT I findings are the ones that block an authorization. Typical examples are
remote access without authentication, unencrypted administrative protocols,
default passwords, and unsupported software. Most rules in an operating system
STIG are CAT II.

### Version, release, and date

A STIG's identity is its product, **version**, and **release**, written
`V<version>R<release>`:

- A new **release** (V1R3 to V1R4) is a maintenance update: rules added, edited,
  or removed within the same product baseline.
- A new **version** (V1R5 to V2R1) is a major revision, often a restructure or
  a large rewrite.
- The **benchmark date** in the release information marks when that release
  was published.

DISA has started naming some *download packages* by date rather than by
release. A package such as `U_FN_FortiGate_Firewall_Y26M10_STIG.zip` (year 2026,
month 10) can bundle several STIGs, each still carrying its own
`V<version>R<release>` inside: that one holds the FortiGate NDM STIG V1R6 and the
FortiGate Firewall STIG V1R5. Record the release of each STIG, not just the
package name.

DISA publishes STIG updates on a quarterly cycle. The revision history document
in each ZIP lists what changed, rule by rule. Read it before moving a system to
a new release.

### Manual STIGs and SCAP benchmarks

| | Manual STIG | SCAP benchmark |
| --- | --- | --- |
| File | `*_Manual-xccdf.xml` | A SCAP data stream with XCCDF 1.2 and OVAL |
| Checks | Human-readable `check-content` | Machine-executable OVAL definitions |
| Coverage | Every rule | Only the rules that can be automated |
| Used by | STIG Viewer and manual review | The SCAP Compliance Checker and other SCAP scanners |

The **Open Vulnerability and Assessment Language (OVAL)** is the SCAP language
that expresses a check as tests a scanner can run, such as "this registry value
equals 1" or "this file contains this line." Where a SCAP benchmark exists, it
covers part of the STIG automatically. The rest still needs manual review or a
tool that automates manual checks (Chapter 04).

## Design Considerations

- **Pick a primary key and keep it.** Track findings by Group ID within a STIG.
  Spreadsheets keyed on Rule ID break every time a rule revision suffix changes.
- **Do not filter by profile unless policy tells you to.** Assess the full
  rule set; filtering by MAC profile can silently drop rules.
- **Plan for manual work.** Even with SCAP benchmarks, a meaningful share of
  most STIGs is manual. Size assessment effort on the full rule count.
- **Keep the release with the result.** A result means nothing without the
  STIG name, version, and release it was produced against.

## Implementation and Automation

You rarely need to read XCCDF by hand, but a short script turns a STIG into a
spreadsheet, a severity summary, or a diff between releases. This Python script
reads any DISA manual STIG and prints one row per rule. It detects the XCCDF
namespace instead of hard-coding it:

```python
#!/usr/bin/env python3
"""List the rules in a DISA STIG XCCDF file as CSV."""
import csv
import re
import sys
import xml.etree.ElementTree as ET

CAT = {"high": "CAT I", "medium": "CAT II", "low": "CAT III"}

tree = ET.parse(sys.argv[1])
root = tree.getroot()
ns = {"x": root.tag.split("}")[0].strip("{")}

out = csv.writer(sys.stdout)
out.writerow(["group_id", "stig_id", "srg_id", "severity", "cat", "ccis", "title"])
for group in root.findall("x:Group", ns):
    rule = group.find("x:Rule", ns)
    ccis = [i.text for i in rule.findall("x:ident", ns) if i.text and i.text.startswith("CCI-")]
    sev = rule.get("severity", "")
    out.writerow([
        group.get("id"),
        rule.findtext("x:version", default="", namespaces=ns),
        group.findtext("x:title", default="", namespaces=ns),
        sev,
        CAT.get(sev, ""),
        " ".join(ccis),
        re.sub(r"\s+", " ", rule.findtext("x:title", default="", namespaces=ns)),
    ])
```

Save it as `stig2csv.py` and run it against a STIG:

```bash
python3 stig2csv.py <Product>_STIG_V<v>R<r>_Manual-xccdf.xml > rules.csv
```

The release information sits in a `plain-text` element of the benchmark. Print
it with:

```bash
grep -o 'Release: [0-9]* Benchmark Date: [^<]*' <Product>_STIG_*_Manual-xccdf.xml
```

## Validation and Troubleshooting

- **The script finds no groups.** Check that you pointed it at the
  `*_Manual-xccdf.xml` file, not a SCAP data stream. SCAP content nests the
  benchmark inside a data stream and uses XCCDF 1.2.
- **Descriptions are full of `&lt;` sequences.** That is escaped markup inside
  the description field. Unescape it (Python's `html.unescape`) and extract the
  `VulnDiscussion` text if you need it.
- **Counts differ between two tools.** One tool may be reading the SCAP
  benchmark (automatable rules only) and the other the manual STIG (all rules).
- **A Group ID disappeared in the new release.** The rule was removed or merged.
  The revision history document says which.

## Security and Best Practices

- Read the `VulnDiscussion` for every rule you plan to deviate from. It states
  the risk you are accepting.
- Treat CAT I findings as release blockers. Agree up front that no system goes
  to production with an open, unaccepted CAT I.
- Keep STIG files under version control or in a dated archive alongside
  results, so any past assessment can be reproduced.
- Never edit a STIG file to make findings disappear. Record tailoring and
  deviations separately (Chapter 09).

## References and Knowledge Checks

**References:**

- NIST, *Specification for the Extensible Configuration Checklist Description
  Format (XCCDF)* (NIST IR 7275).
- NIST Security Content Automation Protocol (SCAP) project pages
  (`csrc.nist.gov/projects/security-content-automation-protocol`).
- DISA STIG revision history documents, included in each STIG ZIP.
- DISA CCI list and its 800-53 mapping, published on the DoD Cyber Exchange.

**Knowledge checks:**

1. Which identifier should you use to match the same requirement across two
   releases of a STIG, and why not the Rule ID?
2. Where in the XCCDF does the STIG ID live, and where does the SRG ID live?
3. Map `high`, `medium`, and `low` severity to DoD categories.
4. What is the difference between a new release and a new version of a STIG?
5. Why can a SCAP benchmark never replace the manual STIG completely?

## Summary and Completion Checklist

A STIG is an XCCDF benchmark made of groups, each holding one rule with a
severity, an explanation, check text, fix text, and five identifiers. The Group
ID is the stable key within a STIG; the SRG ID and CCI link rules across
products and back to 800-53. Severity maps to CAT I, II, and III, and CAT I
findings block authorization. STIGs carry a version and release, update
quarterly, and come in manual form (every rule) and SCAP form (automatable
rules only).

- [ ] Can name and locate all five rule identifiers.
- [ ] Can explain which identifier to use for tracking across releases.
- [ ] Can map XCCDF severity to CAT I, II, and III.
- [ ] Can explain the difference between a manual STIG and a SCAP benchmark.
