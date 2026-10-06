# Chapter 08: Applications, Databases, Web Servers, Containers, and Cloud

## Learning Objectives

- Explain what the Application Security and Development STIG requires and why
  much of its evidence is about process rather than settings.
- Describe how database and web server STIGs split instance-level and
  object-level (database or site) requirements.
- Apply STIG thinking to containers: the Container Platform SRG, orchestrator
  STIGs, hardened images, and why many operating system rules do not apply
  inside a container.
- Explain the Cloud Computing SRG impact levels and how they relate to FedRAMP.
- Scan a container image against a STIG-aligned profile.

## Theory and Architecture

The operating system and network chapters dealt with settings. Higher up the
stack, STIGs increasingly ask for evidence about **how software is built,
configured, and operated**, and the line between product configuration and
organizational process blurs.

### The Application Security and Development STIG

The **Application Security and Development (ASD) STIG** applies to software DoD
develops, or acquires and deploys, when no more specific STIG covers it. It is
one of the largest STIGs and spans the whole software lifecycle:

| Area | Examples of what it asks for |
| --- | --- |
| **Authentication and sessions** | Strong authentication, DoD PKI or MFA support, session timeouts, secure session identifiers |
| **Input and output handling** | Protection against injection, cross-site scripting, and other input validation flaws |
| **Cryptography** | FIPS-validated modules for protecting data in transit and at rest |
| **Error handling and logging** | No sensitive data in error messages; audit records for security-relevant events |
| **Secrets** | No credentials embedded in code or configuration files |
| **Development process** | Secure design, code review, static and dynamic analysis, vulnerability testing before release |
| **Supportability** | Supported frameworks and components, with a process for patching them |

Many ASD rules cannot be checked by reading a configuration file. Their
evidence is a code review record, a scan report, a threat model, or a written
procedure. Embedded credentials, injection flaws, and unsupported software are
typical CAT I findings.

### Databases and web servers: instance and object

Database and web server STIGs usually come in two parts, mirroring the product:

| Product | Instance-level STIG covers | Object-level STIG covers |
| --- | --- | --- |
| **Database** (for example Microsoft SQL Server) | The database engine: authentication modes, auditing, encryption, services, patch level | Each database: permissions, ownership, encryption, auditing of database objects |
| **Web server** (for example IIS 10.0, Apache HTTP Server) | The server: modules, logging, TLS, service account, directory permissions | Each site: authentication, directory browsing, error pages, request filtering |

One database server with five databases, or one web server with three sites,
therefore produces one instance checklist plus one object checklist per
database or site. DISA publishes STIGs for the major database engines and web
servers; confirm which exist for your products and versions in the library.

### Containers

Containers change which rules make sense. A container shares the host kernel and
usually runs one process, so operating system rules about the boot loader,
kernel parameters, `auditd`, or the login console do not apply inside it. STIG
content for containers works at three layers:

```text
Container platform (orchestrator)   Container Platform SRG, Kubernetes and
                                    vendor platform STIGs (for example
                                    OpenShift, RKE2)
Container host                      The host operating system STIG (Chapter 05)
Container image                     A hardened base image; the OS STIG rules
                                    that make sense inside a container
```

DoD's answer to the image layer is **Iron Bank**, the hardened container image
repository run by Platform One. Images in Iron Bank are rebuilt from hardened
bases, scanned continuously, and published with justifications for remaining
findings, so programs can start from an accredited image rather than hardening
their own from scratch.

### The Cloud Computing SRG

The **Cloud Computing SRG** is not a configuration checklist. It sets the
security requirements a cloud service offering must meet to host DoD data, and
defines **impact levels** by data sensitivity:

| Impact level | Data | Notes |
| --- | --- | --- |
| **IL2** | Public and non-controlled unclassified information | Aligns closely with FedRAMP Moderate |
| **IL4** | Controlled Unclassified Information (CUI) | FedRAMP baseline plus DoD-specific controls |
| **IL5** | Higher-sensitivity CUI and unclassified national security systems | Adds stronger separation and personnel requirements |
| **IL6** | Classified information up to SECRET | Requires classified environments |

DISA issues **provisional authorizations** to cloud offerings at a given level,
largely by reusing FedRAMP authorizations and adding DoD controls. A DoD program
using an authorized offering still owns its part of the shared responsibility
model. The operating systems, databases, and applications it deploys in the
cloud must meet their own STIGs, and connections for IL4 and IL5 workloads go
through DoD's Secure Cloud Computing Architecture.

## Design Considerations

- **Bring the ASD STIG into the development process early.** Retrofitting
  logging, session handling, or FIPS cryptography into a finished application is
  expensive. Map ASD requirements to user stories and pipeline gates.
- **Plan checklist volume for databases and web servers.** Instance plus
  per-object checklists multiply quickly. Automate collection where you can.
- **Harden images, not running containers.** Fix findings in the image build and
  redeploy. Patching a running container is lost on the next restart.
- **Start from hardened images.** Iron Bank (for DoD) or vendor-hardened minimal
  images reduce findings before you add your application.
- **Know the impact level before choosing a cloud service.** The impact level of
  your data decides which cloud offerings and regions you can use at all.

## Implementation and Automation

### Scan a container image

OpenSCAP can scan container images and containers with `oscap-podman`, using
the ComplianceAsCode content. Rules that cannot apply inside a container are
reported as not applicable rather than failing:

```bash
sudo dnf install -y openscap-utils scap-security-guide podman
sudo podman pull registry.access.redhat.com/ubi9/ubi:latest
sudo oscap-podman registry.access.redhat.com/ubi9/ubi:latest xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_stig \
  --report ~/ubi9-stig.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```

Feed the findings back into the image build (a `Containerfile` or `Dockerfile`)
and rescan the new image.

### Check database settings

Many database rules come down to a handful of server settings. For PostgreSQL,
for example, the settings that STIG rules commonly check can be read directly:

```bash
sudo -u postgres psql -c "SHOW ssl;" -c "SHOW password_encryption;" \
  -c "SHOW log_connections;" -c "SHOW log_disconnections;"
```

Compare each value with the check text in the database STIG for your engine and
version, and record the output as evidence.

### Organize ASD STIG evidence

For process-heavy rules, keep an evidence register that points each rule to the
artifact that satisfies it:

| ASD rule topic | Evidence artifact | Owner |
| --- | --- | --- |
| Code review before release | Pull request reviews or review reports | Development lead |
| Static analysis | SAST pipeline report for each release | DevSecOps |
| Vulnerability testing | DAST or penetration test report | Security testing |
| No embedded credentials | Secret-scanning results and the secrets-management design | Development lead |
| Supported components | Software bill of materials with end-of-support check | Product owner |

## Validation and Troubleshooting

- **The container scan shows many "notapplicable" results.** Expected. Kernel,
  boot, and host-service rules cannot apply inside a container. Judge the image
  on the rules that remain.
- **`oscap-podman` cannot find the image.** Pull it first, and run as the same
  user (root or rootless) that owns the image.
- **The application team says a rule "is not a setting."** Many ASD rules need
  process evidence. Agree the evidence artifact with the assessor instead of
  arguing the rule away.
- **A database checklist covers only the instance.** Create the object-level
  checklists for each database too.
- **The cloud provider is authorized, so the team assumes the workload is.**
  Provider authorization covers the provider's responsibilities only. The
  workload's own STIGs still apply.

## Security and Best Practices

- Use secret scanning in every repository and pipeline. Embedded credentials
  are among the most common CAT I application findings.
- Use FIPS-validated cryptographic modules in applications that handle DoD data,
  not merely FIPS-approved algorithms.
- Rebuild container images regularly from updated bases, and rescan them on
  every build.
- Keep databases and web servers on vendor-supported versions, and remove sample
  databases, default sites, and demo content.
- Document the shared responsibility split for every cloud service you use, so
  no requirement falls between provider and program.

## References and Knowledge Checks

**References:**

- DISA Application Security and Development STIG (DoD Cyber Exchange).
- DISA database and web server STIGs for your products (DoD Cyber Exchange).
- DISA Container Platform SRG and Kubernetes STIG.
- DoD Cloud Computing SRG (DoD Cyber Exchange).
- Iron Bank, part of DoD Platform One.
- OpenSCAP `oscap-podman` documentation.

**Knowledge checks:**

1. Why is much of the evidence for the ASD STIG about process rather than
   configuration?
2. How many checklists does a SQL Server instance with three databases need,
   and why?
3. Name three operating system STIG rules that do not apply inside a container.
4. What data does each Cloud Computing SRG impact level cover?
5. Does a provider's DoD provisional authorization make your cloud workload
   compliant? Explain.

## Summary and Completion Checklist

Above the operating system, STIGs ask for more process evidence. The
Application Security and Development STIG covers secure design, coding,
testing, and supportability for custom and acquired software. Database and web
server STIGs split instance-level and per-database or per-site requirements.
Containers need STIG content at the platform, host, and image layers, with
hardened images such as Iron Bank as the starting point. The Cloud Computing SRG
governs cloud offerings by impact level, while workloads in the cloud still
carry their own STIGs.

- [ ] Can explain the scope and evidence types of the ASD STIG.
- [ ] Can explain instance and object-level database and web server STIGs.
- [ ] Can describe STIG content for containers at each layer.
- [ ] Can explain the Cloud Computing SRG impact levels.
