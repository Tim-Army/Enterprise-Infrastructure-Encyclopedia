# Chapter 01: The DoD Hardening Framework — Where SRGs and STIGs Come From

## Learning Objectives

- Explain what a Security Requirements Guide (SRG) and a Security Technical
  Implementation Guide (STIG) are, and how they differ.
- Trace the chain from a NIST SP 800-53 control, through a Control Correlation
  Identifier (CCI) and an SRG requirement, down to a product STIG rule.
- Identify the DoD policies that make STIG compliance mandatory and the
  organization (DISA) that publishes the content.
- Distinguish the technology SRGs from the Cloud Computing SRG, which serves a
  different purpose.
- Locate, download, and unpack the official STIG and SRG content.

## Theory and Architecture

A **Security Technical Implementation Guide (STIG)** is a configuration
standard for one specific product: a particular operating system release, a
network operating system, a database engine, a web server, or an application.
Each STIG is a list of rules. Every rule says what secure configuration looks
like, how to check for it, and how to fix it. A **Security Requirements Guide
(SRG)** is the layer above: a product-neutral list of requirements for a whole
*class* of technology, such as "general purpose operating system" or "network
device management." STIGs are written to implement SRGs.

Both are published by the **Defense Information Systems Agency (DISA)**, the
U.S. Department of Defense (DoD) combat support agency responsible for DoD
information technology and networks. DISA distributes them free of charge
through the **DoD Cyber Exchange** website. Most content is public; a small
number of STIGs are restricted to DoD PKI (Common Access Card) holders.

### Why STIGs are mandatory in DoD

STIG compliance is not a best practice inside DoD; it is policy:

| Policy | What it establishes |
| --- | --- |
| **DoDI 8500.01**, *Cybersecurity* | DoD IT must be configured in accordance with applicable SRGs and STIGs, and DISA develops and maintains them. |
| **DoDI 8510.01**, *Risk Management Framework (RMF) for DoD Systems* | Systems are authorized to operate through RMF, which uses NIST SP 800-53 controls; STIG results are core assessment evidence. |
| **NIST SP 800-53 Rev. 5** | The catalog of security and privacy controls that every requirement ultimately traces back to. |
| **CNSSI 1253** | How national security systems are categorized and which 800-53 control baselines and overlays apply. |

The practical consequence is that a system cannot reach an **Authorization to
Operate (ATO)** with open, unmitigated STIG findings that its Authorizing
Official (AO) has not accepted. Chapter 09 covers that process.

Outside DoD, STIGs are widely used as a hardening reference by federal civilian
agencies, defense contractors, and commercial organizations that want a
detailed, auditable baseline. For that audience they compete with the **Center
for Internet Security (CIS) Benchmarks**; Chapter 09 compares the two.

### The requirements chain

The most important idea in this volume is that every STIG rule sits at the
bottom of a traceable chain:

```text
NIST SP 800-53 control        AC-7  Unsuccessful Logon Attempts
        │
        ▼
CCI (Control Correlation ID)  CCI-000044  "enforce the organization-defined limit
        │                                  of consecutive invalid logon attempts"
        ▼
SRG requirement               General Purpose Operating System SRG:
        │                     "The operating system must enforce the limit of
        │                      three consecutive invalid logon attempts..."
        ▼
STIG rule                     RHEL 9 STIG: configure pam_faillock with
                              deny = 3, plus the check command and fix text
```

Each layer adds specificity:

- **800-53 controls** say *what* must be protected, in policy terms. They leave
  values ("organization-defined") to the organization.
- **CCIs** break each control into single, testable statements. DISA maintains
  the CCI list and its mapping to 800-53. One control usually maps to several
  CCIs.
- **SRG requirements** apply a CCI to a technology class and set DoD's value
  (here, three attempts).
- **STIG rules** apply the SRG requirement to one product, with the exact file,
  setting, command, or GUI path to check and fix.

Because the chain is preserved in the content itself (every STIG rule lists its
SRG ID and CCI), a single STIG finding can be traced all the way back to the
800-53 control it supports. That traceability is what makes STIG results usable
as RMF evidence.

### SRG versus STIG

| | SRG | STIG |
| --- | --- | --- |
| Scope | A technology class (all operating systems, all routers) | One product and version (RHEL 9, a vendor firewall) |
| Content | Requirements, with rationale | Requirements plus check procedure and fix text |
| Who writes it | DISA | DISA, or the product vendor under DISA's process |
| When you use it directly | When no STIG exists for your product | Whenever a STIG exists |

When a product has no STIG, the applicable SRG still applies. You assess the
product against the SRG requirements and document how each one is met. Chapter
03 covers this.

### The Cloud Computing SRG is different

One SRG does not fit the pattern above. The **Cloud Computing SRG** sets
requirements for *cloud service offerings* used by DoD. It defines **impact
levels** (IL2, IL4, IL5, IL6) based on the sensitivity of the data, and it
governs how commercial clouds obtain DoD provisional authorizations, building
on FedRAMP. It is a program-level document about providers and data, not a
configuration checklist. Chapter 08 places it alongside the technology STIGs.

## Design Considerations

- **Decide the baseline early.** Choosing STIG as your hardening standard
  affects image builds, change management, and how you write runbooks. It is
  far cheaper to build STIG-compliant from the start than to retrofit.
- **STIGs follow the product version.** A STIG applies to a specific release
  (for example, Windows Server 2022, not "Windows Server"). Platform upgrades
  require moving to the matching STIG, which can change many rules.
- **Expect friction with operations.** STIGs favor security over convenience:
  short session timeouts, strict password and lockout policy, FIPS-validated
  cryptography, extensive audit logging, and removal of anything not needed.
  Budget time to test each change against the workload.
- **Not every rule is achievable.** Some rules conflict with how an application
  works. The answer is a documented deviation with a mitigation and risk
  acceptance, never a silent skip.
- **Outside DoD, adopt deliberately.** Commercial users are free to tailor.
  Record which rules you exclude and why, so the baseline stays auditable.

## Implementation and Automation

The content is distributed as ZIP files from the DoD Cyber Exchange STIG pages
(`https://www.cyber.mil/stigs/downloads`; the files themselves are served from
`dl.dod.cyber.mil`, and DoD has moved this site before, so confirm the address). Three downloads matter most:

| Download | What it contains |
| --- | --- |
| **Individual STIG or SRG** | One product's ZIP: the XCCDF XML file, a PDF or text overview, and sometimes supplementary documents |
| **STIG Library Compilation** | Every public STIG and SRG in one large ZIP (for example `U_SRG-STIG_Library_October_2026.zip`, about 375 MB), refreshed each quarterly release |
| **SCAP benchmarks** | Automatable versions of selected STIGs for scanners such as the SCAP Compliance Checker (Chapter 04) |

Unpacking a single STIG on a Linux workstation:

```bash
mkdir -p ~/stig && cd ~/stig
unzip <STIG_ZIP_FILE>.zip -d <product>-stig
find <product>-stig -type f | sort
```

Typical contents:

```text
<product>-stig/<Product>_STIG_V<version>R<release>_Manual-xccdf.xml
<product>-stig/<Product>_STIG_Overview.pdf
<product>-stig/<Product>_Revision_History.pdf
```

The `*-xccdf.xml` file is the STIG itself, in the **Extensible Configuration
Checklist Description Format (XCCDF)**. Every tool in this volume, from STIG
Viewer to a SCAP scanner, reads that file. Chapter 02 takes it apart.

To see which STIGs exist for your environment, list the library compilation
instead of downloading products one at a time:

```bash
unzip -l <STIG_LIBRARY_COMPILATION>.zip | grep -i -E "windows|rhel|cisco" | head -40
```

## Validation and Troubleshooting

- **Confirm you have the current release.** The file name carries the version
  and release (`V2R1` means version 2, release 1). Compare it with the release
  listed on the Cyber Exchange page. Assessing against a superseded release is a
  common audit finding.
- **Check that the STIG matches the product version.** Using the RHEL 8 STIG on
  RHEL 9, or a Windows 10 STIG on Windows 11, produces wrong results.
- **Nested ZIPs are normal.** The library compilation contains ZIPs inside ZIPs.
  Extract the inner archive for the product you need.
- **A download that requires a certificate prompt** is one of the PKI-restricted
  STIGs; it needs a DoD Common Access Card or other DoD PKI certificate.
- **Missing STIG for your product** does not mean no requirements apply. Use the
  matching SRG (Chapter 03).

## Security and Best Practices

- Download content only from the official DoD Cyber Exchange site, and verify
  any published checksums. Third-party mirrors may be stale or altered.
- Keep a dated archive of the exact STIG releases you assessed against. Auditors
  ask which release produced a given result.
- Subscribe to DISA's release announcements and plan a quarterly review. STIGs
  change every quarter, and new rules can turn a compliant system non-compliant.
- Treat the STIG as the floor for DoD systems, not the ceiling. It does not
  replace vulnerability patching, which is tracked separately (for example,
  through IAVM notices in DoD).

## References and Knowledge Checks

**References:**

- DoD Cyber Exchange, STIGs Document Library (`www.cyber.mil/stigs/downloads`).
- DoDI 8500.01, *Cybersecurity*; DoDI 8510.01, *Risk Management Framework for
  DoD Systems*.
- NIST SP 800-53 Rev. 5, *Security and Privacy Controls for Information Systems
  and Organizations* (`csrc.nist.gov`).
- CNSSI 1253, *Security Categorization and Control Selection for National
  Security Systems*.
- DISA Control Correlation Identifier (CCI) list, published on the DoD Cyber
  Exchange.

**Knowledge checks:**

1. What is the difference between an SRG and a STIG, and which one do you use
   when a product has no STIG?
2. List the four layers of the requirements chain, from the most general to the
   most specific.
3. What does a CCI add between an 800-53 control and an SRG requirement?
4. Why is the Cloud Computing SRG not used the same way as the operating system
   or network device SRGs?
5. Which DoD instruction requires DoD IT to be configured according to STIGs and
   SRGs?

## Summary and Completion Checklist

SRGs set product-neutral requirements for a class of technology, and STIGs
implement them for specific products with exact check and fix procedures. Both
come from DISA, and DoD policy makes them mandatory. Every STIG rule traces back
through an SRG requirement and a CCI to a NIST SP 800-53 control, which is what
makes STIG results usable as RMF evidence. The Cloud Computing SRG is the
exception: it governs cloud providers and data impact levels rather than
product configuration.

- [ ] Can explain the difference between an SRG and a STIG.
- [ ] Can describe the chain from 800-53 control to CCI, SRG requirement, and
      STIG rule.
- [ ] Can name the DoD policies that make STIGs mandatory.
- [ ] Can explain how the Cloud Computing SRG differs from technology SRGs.
