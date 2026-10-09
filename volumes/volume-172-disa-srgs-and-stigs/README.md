# Volume CLXXII — DISA SRGs and STIGs

> A practitioner's guide to **DISA Security Requirements Guides (SRGs)** and
> **Security Technical Implementation Guides (STIGs)**: where they come from,
> how the content is structured, how to assess and harden Linux, Windows,
> network devices, applications, containers, and the Fortinet portfolio against
> them, and how to run a compliance program that keeps systems compliant as STIGs
> change every quarter.

## Overview

Volume CLXXII is a **vendor-neutral standards volume** on the configuration
baselines the U.S. Department of Defense requires for its systems. **SRGs**
set requirements for a class of technology, such as general purpose operating
systems or network device management. **STIGs** implement those requirements
for specific products, with exact check and fix procedures. Both are published
by the Defense Information Systems Agency (DISA), and DoD policy makes them
mandatory. Outside DoD they are widely used as a detailed, auditable hardening
reference.

The volume's central idea is the **requirements chain**: every STIG rule traces
back through an SRG requirement and a Control Correlation Identifier (CCI) to a
NIST SP 800-53 control. That chain is what turns a configuration setting into
evidence for a Risk Management Framework authorization, and it runs through
every chapter.

STIG material appears throughout the encyclopedia as hardening advice inside
product volumes. This volume explains the framework itself, so those product
chapters can be read in context.

Chapters move from the framework to the content, the tools, the platforms, and
finally the program:

- **Chapter 01** explains what SRGs and STIGs are, the DoD policies behind
  them, and the chain from 800-53 to STIG rule.
- **Chapter 02** takes a STIG apart: XCCDF structure, the five rule
  identifiers, CAT I/II/III severity, and versioning.
- **Chapter 03** surveys the SRG catalog, explains how STIGs are produced
  (including vendor-developed STIGs), and shows how to assess a product that
  has no STIG.
- **Chapter 04** covers the tools: STIG Viewer and checklists (CKL and CKLB),
  the SCAP Compliance Checker, OpenSCAP, Evaluate-STIG, STIG Manager, and
  eMASS.
- **Chapter 05** hardens Linux to the STIG, with RHEL 9 as the main example and
  the Ubuntu Security Guide for Ubuntu.
- **Chapter 06** hardens Windows to the STIG with DISA's GPO package, LGPO,
  PowerSTIG, and SCC.
- **Chapter 07** covers network device STIGs: the NDM and traffic-plane split,
  common requirements, and manual assessment.
- **Chapter 08** moves up the stack to applications, databases, web servers,
  containers, and the Cloud Computing SRG.
- **Chapter 09** runs the program: RMF, finding dispositions, POA&Ms,
  continuous monitoring, metrics, and STIGs compared with CIS Benchmarks.
- **Chapter 10** covers the Fortinet portfolio: the two FortiGate STIGs and
  how to meet them on FortiOS, and the SRGs that apply to every other Fortinet
  product.
- **Chapter 11** maps every FortiSwitch feature to the FortiSwitchOS releases
  that support it and to the SRG requirement it implements or must meet.
- **Chapter 12** does the same for FortiAnalyzer, against the Central Log
  Server SRG, with the command or GUI location that meets each requirement.
- **Chapter 13** maps every FortiManager feature to its release, the NDM SRG
  requirement it meets, and the command that meets it, with emphasis on access
  control, auditing, and configuration-change control.
- **Chapter 14** maps every FortiAP feature to its release, the Network WLAN
  STIG or NDM SRG requirement it meets, and the FortiGate wireless-controller
  or FortiAP command that meets it.
- **Chapter 15** maps every FortiExtender feature to its release, the NDM,
  Router, or VPN SRG requirement it meets, and the FortiGate or FortiExtender
  command that meets it.
- **Chapter 16** maps every FortiWeb feature to its release, the ALG or NDM
  SRG requirement it meets, and the FortiWeb command that meets it.
- **Chapter 17** maps every FortiMail feature to its release, the ALG or NDM
  SRG requirement it meets, and the FortiMail command that meets it.
- **Chapter 18** maps every FortiProxy feature to its release, the ALG or NDM
  SRG requirement it meets, and the FortiProxy command that meets it.
- **Chapter 19** maps every FortiADC feature to its release, the ALG, NDM,
  or VPN SRG requirement it meets, and the FortiADC command that meets it.
- **Chapter 20** maps every FortiDDoS-F feature to its release, the NDM SRG or
  Firewall SRG denial-of-service requirement it meets, and the command or web
  UI pane that meets it.
- **Chapter 21** maps every FortiSandbox feature to its release, the NDM or
  IDPS SRG requirement it meets, and the command or web UI pane that meets it.
- **Chapter 22** maps every FortiVoice feature to its release, the EVVM or NDM
  SRG requirement it meets, and the web UI pane or command that meets it.
- **Chapter 23** maps every FortiAuthenticator feature to its release, the AAA
  Services or NDM SRG requirement it meets, and the web UI pane that meets it.
- **Chapter 24** maps every FortiPAM feature to its release, the NDM SRG
  requirement or Application Security and Development STIG rule it meets, and
  the web UI pane or command that meets it.
- **Chapter 25** maps every FortiNAC-F feature to its release, the NDM or AAA
  Services SRG requirement or Cisco ISE NAC STIG pattern rule it relates to,
  and the command or web UI pane that meets it.
- **Chapter 26** maps every FortiSIEM feature to its release, the Central Log
  Server, NDM, or GPOS SRG requirement it meets, and the web UI pane or command
  that meets it.
- **Chapter 27** maps every FortiClient and FortiClient EMS feature to its
  release, the UEM Server, UEM Agent, or VPN SRG requirement it meets, and the
  EMS pane, FortiClient XML setting, or command that meets it.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), with knowledge checks,
except that this volume has no hands-on labs (see
[Lab coverage](#lab-coverage)).

## Chapters

1. [The DoD Hardening Framework — Where SRGs and STIGs Come From](chapters/01-the-dod-hardening-framework-where-srgs-and-stigs-come-from.md) — SRG versus STIG, DISA, DoD policy, the requirements chain, and the Cloud Computing SRG.
2. [Anatomy of a STIG — XCCDF, Identifiers, Severity, and Versioning](chapters/02-anatomy-of-a-stig-xccdf-identifiers-severity-and-versioning.md) — XCCDF structure, Group/Rule/STIG/SRG IDs and CCIs, CAT I/II/III, releases, and manual versus SCAP content.
3. [The SRG Catalog, How STIGs Are Built, and What to Do Without One](chapters/03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md) — technology SRGs, multi-function devices, vendor STIGs, the quarterly cycle, and SRG-based assessment.
4. [STIG Tooling — STIG Viewer, Checklists, and SCAP Scanning](chapters/04-stig-tooling-stig-viewer-checklists-and-scap-scanning.md) — finding statuses, CKL and CKLB, SCC, OpenSCAP, DISA versus ComplianceAsCode content, and tools at scale.
5. [Hardening Linux to the STIG](chapters/05-hardening-linux-to-the-stig.md) — RHEL 9 STIG coverage, install-time hardening, Ansible remediation, and the Ubuntu Security Guide.
6. [Hardening Windows to the STIG](chapters/06-hardening-windows-to-the-stig.md) — the Windows STIG family, STIG IDs, DISA GPOs with GPMC and LGPO, PowerSTIG, and SCC.
7. [Network Device STIGs — Management, Routing, and Filtering](chapters/07-network-device-stigs-management-routing-and-filtering.md) — NDM and traffic-plane STIGs, common requirements, and manual assessment with evidence.
8. [Applications, Databases, Web Servers, Containers, and Cloud](chapters/08-applications-databases-web-servers-containers-and-cloud.md) — the ASD STIG, instance and object STIGs, containers and Iron Bank, and Cloud Computing SRG impact levels.
9. [Running a STIG Compliance Program](chapters/09-running-a-stig-compliance-program.md) — RMF, dispositions, POA&Ms, continuous monitoring, metrics, and STIGs versus CIS Benchmarks.
10. [Fortinet Products — STIGs and SRG Mapping](chapters/10-fortinet-products-stigs-and-srg-mapping.md) — the FortiGate NDM and Firewall STIGs on FortiOS, uncovered FortiGate functions, and SRG mapping for every other Fortinet product.
11. [FortiSwitch Feature, Version, and SRG Map](chapters/11-fortiswitch-feature-version-and-srg-map.md) — all 235 FortiSwitchOS 8.0.0 features with the releases that list them and the Layer 2 Switch, NDM, Router, or AAA Services SRG requirement each maps to.
12. [FortiAnalyzer Feature, Version, and SRG Map](chapters/12-fortianalyzer-feature-version-and-srg-map.md) — 349 FortiAnalyzer features (53 core platform features and every feature in the 7.0 to 8.0 New Features Guides) with the release that introduced each, the Central Log Server or NDM SRG requirement it maps to, and the command that meets it.
13. [FortiManager Feature, Version, and SRG Map](chapters/13-fortimanager-feature-version-and-srg-map.md) — 487 FortiManager features (52 core platform features and every feature in the 7.0 to 8.0 New Features Guides) with the release that introduced each, the NDM SRG requirement it maps to, and the command that meets it.
14. [FortiAP Feature, Version, and SRG Map](chapters/14-fortiap-feature-version-and-srg-map.md) — 186 FortiAP features (39 core platform features and every feature in the FortiAP 7.0.0 to 8.0.0 release notes) with the release that introduced each, the Network WLAN STIG or NDM SRG requirement it maps to, and the FortiGate or FortiAP command that meets it.
15. [FortiExtender Feature, Version, and SRG Map](chapters/15-fortiextender-feature-version-and-srg-map.md) — 154 FortiExtender features (43 core platform features and every feature in the FortiExtender 7.0.0 to 8.0.0 release notes) with the release that introduced each, the NDM, Router, or VPN SRG requirement it maps to, and the FortiGate or FortiExtender command that meets it.
16. [FortiWeb Feature, Version, and SRG Map](chapters/16-fortiweb-feature-version-and-srg-map.md) — 480 FortiWeb features (76 core platform features and every feature in the FortiWeb 7.0.0 to 8.0.8 "What's new" lists) with the release that introduced each, the ALG or NDM SRG requirement it maps to, and the FortiWeb CLI command that meets it.
17. [FortiMail Feature, Version, and SRG Map](chapters/17-fortimail-feature-version-and-srg-map.md) — 331 FortiMail features (84 core platform features and every feature in the FortiMail 7.0.0 to 8.0.2 release notes "What's new" tables) with the release that introduced each, the ALG or NDM SRG requirement it maps to, and the FortiMail CLI command that meets it.
18. [FortiProxy Feature, Version, and SRG Map](chapters/18-fortiproxy-feature-version-and-srg-map.md) — 425 FortiProxy features (89 core platform features and every feature in the FortiProxy 7.0.0 to 7.6.7 release notes "What's new" sections) with the release that introduced each, the ALG or NDM SRG requirement it maps to, and the FortiProxy CLI command that meets it.
19. [FortiADC Feature, Version, and SRG Map](chapters/19-fortiadc-feature-version-and-srg-map.md) — 327 FortiADC features (80 core platform features and every feature in the FortiADC 7.0.0 to 8.0.4 release notes and New Features guides) with the release that introduced each, the ALG, NDM, or VPN SRG requirement it maps to, and the FortiADC CLI command that meets it.
20. [FortiDDoS Feature, Version, and SRG Map](chapters/20-fortiddos-feature-version-and-srg-map.md) — 292 FortiDDoS-F features (51 core platform features and every feature in the 6.1.0 to 8.0.1 release notes) with the release that introduced each, the NDM SRG or Firewall SRG denial-of-service, filtering, and logging requirement it maps to, and the command or web UI pane that meets it.
21. [FortiSandbox Feature, Version, and SRG Map](chapters/21-fortisandbox-feature-version-and-srg-map.md) — 518 FortiSandbox features (62 core platform features and every feature in the 4.0.0 to 5.2.2 release notes) with the release that introduced each, the NDM or IDPS SRG requirement it maps to, and the CLI command or web UI pane that meets it.
22. [FortiVoice Feature, Version, and SRG Map](chapters/22-fortivoice-feature-version-and-srg-map.md) — 172 FortiVoice features (86 core platform features and every feature in the 7.0.0 to 8.0.1 release notes) with the release that introduced each, the EVVM Session Management, Endpoint, or Policy SRG or NDM SRG requirement it maps to, and the web UI pane or command that meets it.
23. [FortiAuthenticator Feature, Version, and SRG Map](chapters/23-fortiauthenticator-feature-version-and-srg-map.md) — 198 FortiAuthenticator features (102 core platform features and every feature in the 6.6.0 to 8.0.3 release notes) with the release that introduced each, the AAA Services or NDM SRG requirement it maps to, and the web UI pane or command that meets it.
24. [FortiPAM Feature, Version, and SRG Map](chapters/24-fortipam-feature-version-and-srg-map.md) — 366 FortiPAM features (85 core platform features and every feature in the 1.0.0 to 7.0.0 release notes) with the release that introduced each, the NDM SRG requirement or administrator-configurable Application Security and Development STIG rule it maps to, and the web UI pane or command that meets it.
25. [FortiNAC Feature, Version, and SRG Map](chapters/25-fortinac-feature-version-and-srg-map.md) — 172 FortiNAC-F features (53 core platform features and every feature in the 7.2.0 to 7.6.7 release notes) with the release that introduced each, the NDM or AAA Services SRG requirement or Cisco ISE NAC STIG pattern rule it maps to, and the FortiNAC CLI command or web UI pane that meets it.
26. [FortiSIEM Feature, Version, and SRG Map](chapters/26-fortisiem-feature-version-and-srg-map.md) — 153 FortiSIEM features (63 core platform features and every feature in the 7.0.0 to 7.6.0 release notes) with the release that introduced each, the Central Log Server, NDM, or GPOS SRG requirement it maps to, and the web UI pane or command that meets it.
27. [FortiClient and EMS Feature, Version, and SRG Map](chapters/27-forticlient-and-ems-feature-version-and-srg-map.md) — 185 FortiClient and FortiClient EMS features (63 core platform features and every feature in the 7.0 to 8.0 New Features Guides) with the FortiClient or EMS release that introduced each, the UEM Server, UEM Agent, or VPN SRG requirement it maps to, and the EMS GUI pane, FortiClient XML setting, or emscli command that meets it.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all twenty-seven chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Related volumes

This is a vendor-neutral standards volume, not a certification-tracks volume,
and it is not mapped to a single exam blueprint. It connects to the product
volumes where STIGs are applied:
[Red Hat Enterprise Linux 10 (XIV)](../volume-014-red-hat-enterprise-linux-10/README.md),
[Ubuntu Server and Cloud 26.04 LTS (XXI)](../volume-021-ubuntu-server-cloud-26-04-lts/README.md),
[Windows Server 2025 and Active Directory (XXXVI)](../volume-036-windows-server-2025-active-directory/README.md),
[Fortinet Network Security (XIX)](../volume-019-fortinet-network-security/README.md),
[Palo Alto Networks Security (XVI)](../volume-016-palo-alto-networks-security/README.md),
and [Containers and Platform Engineering (VIII)](../volume-008-containers-platform-engineering/README.md).
For the wider security program, see
[Enterprise Cybersecurity (X)](../volume-010-enterprise-cybersecurity/README.md)
and [Public Sector Data Governance (LXIII)](../volume-063-public-sector-data-governance/README.md).

## Lab coverage

This volume has **no hands-on labs**, by design. It is a reference to the
SRG and STIG framework, content, tools, and program. Each chapter keeps its
implementation examples (commands, scripts, and configuration snippets) and its
knowledge checks, but omits the Hands-On Lab and Lab Verification sections of
the standard chapter template. For hands-on practice applying STIG settings,
see the hardening labs in the product volumes listed under
[Related volumes](#related-volumes).

## Software and platform baseline

This volume references the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): **DISA STIG and SRG content
as of the 2026-10 quarterly release**, with STIG Viewer 3.x, the SCAP
Compliance Checker 5.x, OpenSCAP 1.3 or later, and ComplianceAsCode content
current in RHEL 9. STIGs change every quarter, and identifiers, values, and
tool versions change with them. Confirm the current release of any STIG on the
DoD Cyber Exchange before assessing against it, and update that file, not
individual chapters, when the baseline changes.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-172-disa-srgs-and-stigs
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
