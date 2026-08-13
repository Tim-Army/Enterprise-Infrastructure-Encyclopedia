# Chapter 10: Software Versions and Download Sources

![Flow diagram showing the version-provenance chain used in this chapter: the repository's SOFTWARE_VERSIONS.md baseline is the single source of truth for pinned versions, this chapter adds an official download or source column and an access class per product, and a verification step confirms each source is the vendor's own authoritative location and each access class is correct before the table is relied upon.](../../../diagrams/volume-999-reference-library/chapter-10-software-inventory-download-provenance-flow.svg)

*Figure 10-1. The software-inventory provenance flow exercised in this chapter's lab: baseline version → official source → access class → verification.*

## Learning Objectives

- Locate the pinned baseline version of every platform this encyclopedia
  builds on, and understand that `SOFTWARE_VERSIONS.md` at the repository
  root is the single authoritative source for those versions.
- Find the **official** download or acquisition source for each product,
  and classify it as freely downloadable, entitlement/contract-gated, or a
  cloud service with nothing to download.
- Distinguish a version *baseline* (what a chapter was written against)
  from the *latest* release, and know why the encyclopedia pins the former.
- Apply the reproduction and provenance discipline from
  [Chapter 09](09-standards-certifications-vendor-documentation-and-reference-governance.md)
  to this inventory so it does not drift into stale or misleading links.

## Theory and Architecture

This chapter consolidates, in one place, **what software the encyclopedia
references, at what version, and where to get it**. It exists because two
questions recur constantly during real work: "which version is this written
against?" and "where do I actually download that?"

Two design rules govern the tables below.

- **Versions are not owned here.** The authoritative version baseline is
  [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) at the repository
  root, which every chapter already references. This chapter **mirrors** that
  baseline and adds a **download/source** column and an **access class**; it
  does not invent a second, competing version list. When a version changes,
  it changes in `SOFTWARE_VERSIONS.md` first, and this table follows.
- **Sources are official and access-classified.** Each source is the
  **vendor's own** distribution point — not a third-party mirror, reseller,
  or "download crack" site. Because much enterprise software is not publicly
  downloadable, every row is tagged with an **access class**:
  - **Free** — publicly downloadable at no cost (open source, community
    editions, free tools).
  - **Entitlement** — the download itself requires a subscription, support
    contract, or account login. Because the vendor's download portal is
    login-walled, the source given here is the vendor's **public parent page**
    (the openable product/support page above the gated download), not the
    login portal or a specific file.
  - **Cloud** — a SaaS or cloud service with **nothing to download**; you
    consume it via a console or API.

The distinction matters operationally: a lab that needs a *Free* tool can be
reproduced by anyone, while an *Entitlement* platform requires a license the
reader must already hold, and a *Cloud* service requires an account, not an
installer. The lab at the end audits these classifications.

## Design Considerations

- **Pin the baseline, link the source, never hardcode a deep file URL.**
  Vendor download URLs to specific build files rot quickly; the tables link
  to the **download portal or project releases page**, which stays stable as
  new builds appear. The version says *what* to fetch there.
- **Prefer the vendor's own domain, and its public parent page when the
  download is gated.** For every entitlement product the source is the
  vendor's **public** product/support page (`cisco.com`, `broadcom.com`,
  `paloaltonetworks.com`, and so on) — openable by any reader — rather than
  the login-walled download portal or a redistribution site. This is both a
  correctness and a security control.
- **Mark cloud services as non-downloadable rather than omitting them.** AWS,
  Webex/Control Hub, and Intersight SaaS have no installer; recording them as
  *Cloud* prevents a reader from hunting for a download that does not exist.
- **Keep this chapter in lockstep with `SOFTWARE_VERSIONS.md`.** If the two
  disagree, `SOFTWARE_VERSIONS.md` wins and this chapter is corrected in the
  same change — the governance rule from
  [Chapter 09](09-standards-certifications-vendor-documentation-and-reference-governance.md).

## Implementation and Automation

Baseline versions mirror [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md)
(baseline date **2026-07** unless noted); the **Official source** and
**Access** columns are added here.

### Operating systems and hypervisors

| Product | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Red Hat Enterprise Linux | RHEL 10 | `redhat.com` (free developer download at `developers.redhat.com`) | Entitlement / Free (dev) |
| Ubuntu Server / Cloud | 26.04 LTS | `ubuntu.com/download` | Free |
| Proxmox VE | 9.x | `proxmox.com/en/downloads` | Free |
| VMware vSphere / ESXi / vCenter | vSphere 9.x | `broadcom.com` (VMware by Broadcom) | Entitlement |
| VMware NSX | NSX 4.x | `broadcom.com` | Entitlement |

### Cisco platforms

| Product | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Cisco IOS XE | 17.x (Catalyst 9000) | `cisco.com` | Entitlement |
| Cisco Catalyst Center | Current SD-Access release | `cisco.com` | Entitlement |
| Cisco IOS XR (ASR 9000 / NCS) | 7.x | `cisco.com` | Entitlement |
| Cisco NX-OS (Nexus 9000) | 10.x | `cisco.com` | Entitlement |
| Cisco ACI | 6.x | `cisco.com` | Entitlement |
| Cisco UCS Manager / Intersight | 4.x / current SaaS | `cisco.com` / `intersight.com` | Entitlement / Cloud |
| Cisco Secure Firewall (FTD/FMC) | 7.x | `cisco.com` | Entitlement |
| Cisco Identity Services Engine (ISE) | 3.x | `cisco.com` | Entitlement |
| Cisco Unified CM / IM&P / Unity Connection | 15.x | `cisco.com` | Entitlement |
| Cisco Expressway | Current release | `cisco.com` | Entitlement |
| Cisco Webex / Control Hub | Continuous cloud delivery | `admin.webex.com` (console) | Cloud |

### Automation, orchestration, and cloud

| Product | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Kubernetes | 1.31.x | `kubernetes.io/releases/download` / `github.com/kubernetes/kubernetes/releases` | Free |
| Terraform | 1.9.x | `developer.hashicorp.com/terraform/install` | Free |
| Ansible | core 2.17 / ansible 10.x | `pypi.org/project/ansible` / `docs.ansible.com` | Free |
| AWS services | Current GA surface | `aws.amazon.com` (console/API; no download) | Cloud |

### Security and network operations

| Product | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Palo Alto Networks PAN-OS | 11.x | `paloaltonetworks.com` | Entitlement |
| Palo Alto Networks Panorama | 11.x | `paloaltonetworks.com` | Entitlement |
| Fortinet FortiOS | 7.6.x | `fortinet.com` | Entitlement |
| Forescout eyeSight / eyeControl | 8.5.x | `forescout.com` | Entitlement |
| Gigamon GigaVUE-FM | 6.x | `gigamon.com` | Entitlement |
| Wireshark | 4.4.x | `wireshark.org/download.html` | Free |

### Dell infrastructure management

| Product | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Dell OpenManage Enterprise | 4.7.x | `dell.com/support` | Free (firmware/driver) |
| Dell iDRAC | iDRAC9 / iDRAC10 | `dell.com/support` (per-service-tag firmware) | Free (firmware) |
| Dell VxRail | Version-locked to its vSphere bundle | `dell.com/support` (confirm the vSphere pairing in VxRail release notes) | Entitlement |

### Publishing toolchain (this encyclopedia's own build)

| Product | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Node.js | 22.x LTS | `nodejs.org/en/download` | Free |
| pnpm | 11.9.0 | `pnpm.io/installation` | Free |
| Pandoc | 3.10 (pinned by checksum in the build workflows) | `pandoc.org/installing.html` / `github.com/jgm/pandoc/releases` | Free |

### Additional open-source lab tools

These are not pinned in `SOFTWARE_VERSIONS.md` (labs use the current release);
they are the major freely downloadable tools the hands-on labs across the
encyclopedia rely on, listed with their official source.

| Tool | Baseline | Official source | Access |
| --- | --- | --- | --- |
| Python 3 | Current release | `python.org/downloads` | Free |
| Git | Current release | `git-scm.com/downloads` | Free |
| Docker / containerd | Current release | `docs.docker.com/get-docker` / `containerd.io` | Free |
| Helm | Current release | `helm.sh` | Free |
| HashiCorp Vault | Current release | `developer.hashicorp.com/vault/install` | Free |
| HashiCorp Consul | Current release | `developer.hashicorp.com/consul/install` | Free |
| Istio | Current release | `istio.io/latest/docs/setup/getting-started` | Free |
| Cilium | Current release | `cilium.io` / `github.com/cilium/cilium/releases` | Free |
| Calico | Current release | `docs.tigera.io` / `github.com/projectcalico/calico/releases` | Free |
| Grafana | Current release | `grafana.com/grafana/download` | Free |
| Prometheus | Current release | `prometheus.io/download` | Free |

## Validation and Troubleshooting

| State | Check | Failure means |
| --- | --- | --- |
| Version matches the baseline | Row version equals its `SOFTWARE_VERSIONS.md` entry | This chapter drifted from the authoritative baseline; correct it |
| Source is the vendor's own | The domain is the vendor/project, not a mirror or reseller | A row points at an unofficial (and possibly unsafe) source |
| Access class is correct | Free links resolve to a public download; Entitlement links reach the vendor's public product/support page (the download behind it needs a license/login); Cloud rows have no installer | The reader is sent hunting for a download that needs a license, or that does not exist |
| No pinned version is orphaned | Every `SOFTWARE_VERSIONS.md` row appears here | A referenced platform has no recorded download source |

- **A "download" link asks me to log in.** That is expected for an
  *Entitlement* row — the source is the vendor portal, and the license or
  support contract is the reader's to hold. It is not a broken link.
- **A row here disagrees with `SOFTWARE_VERSIONS.md`.** The root file wins.
  Correct this chapter in the same change, per the governance rule.
- **A vendor moved its download portal.** Update the source domain here and,
  if the same portal is referenced elsewhere, in the vendor-documentation
  table in [Chapter 09](09-standards-certifications-vendor-documentation-and-reference-governance.md).

## Security and Best Practices

- **Download only from the vendor's own domain.** Every source in this
  chapter is the vendor or project's authoritative distribution point.
  Third-party "free download" mirrors of enterprise software are a common
  malware vector; treat any source not listed here with suspicion.
- **Verify integrity where the vendor provides it.** Prefer checksums and
  signatures (the build toolchain pins **Pandoc by SHA-256** for exactly this
  reason). Open-source releases publish checksums on their releases pages.
- **Respect licensing and entitlement.** *Entitlement* rows require a valid
  license or support contract; downloading them presumes you hold one. This
  encyclopedia points at official sources and does not host or redistribute
  any vendor software.
- **Do not paste credentials into anything but the vendor's own portal.** The
  *Entitlement* links go to the vendor's own **public** product/support page;
  the gated download behind it authenticates on the vendor's portal — never
  enter portal credentials into a site reached from an unofficial link.

## References and Knowledge Checks

**References**

- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) — the authoritative
  version baseline this chapter mirrors.
- [Chapter 09](09-standards-certifications-vendor-documentation-and-reference-governance.md)
  — vendor documentation portals and the reference-governance discipline
  applied here.
- [Chapter 04](04-configuration-templates-baselines-and-change-records.md)
  — baselines and change records, of which the version baseline is one.

**Knowledge checks**

1. Why does this chapter mirror `SOFTWARE_VERSIONS.md` rather than maintain
   its own version numbers, and which file wins if they disagree?
2. What are the three access classes, and how does a reader's next action
   differ for a *Free*, an *Entitlement*, and a *Cloud* row?
3. Why do the tables link to a download **portal or releases page** rather
   than to a specific build's file URL?
4. A colleague sends you a link to "VMware vSphere 9 ISO — free download" on
   a file-sharing site. Why is that not the source in this chapter, and what
   is the risk?
5. Which products in the tables have **nothing to download**, and how should
   they be acquired instead?

## Hands-On Lab

**Objective:** Audit a slice of this chapter's inventory against the live
authoritative sources and the repository baseline, and produce a
governance-ready findings record.

**Prerequisites:** Internet access; access to the repository root files
[`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) and this chapter; a
Markdown editor. **Cost:** none (all official sources consulted are either
free or a portal/login you already hold; download nothing for this lab).

1. Pick **five** rows spanning all three access classes (at least one *Free*,
   one *Entitlement*, one *Cloud*). Record each product's **baseline version**
   from this chapter. **Expected result:** five version claims recorded.
2. For each of the five, open [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md)
   and confirm the version here **matches** the root baseline (or, for the
   *additional open-source tools* that are not pinned there, note that they
   are intentionally "current release"). **Expected result:** five
   match/no-pin determinations. **Negative test:** if any row disagrees with
   `SOFTWARE_VERSIONS.md`, draft the corrected row — the root file wins.
3. Visit each of the five **official sources** and confirm (a) the domain is
   the vendor/project's own, and (b) the **access class** is correct — a
   *Free* source offers a public download, an *Entitlement* source is the
   vendor's public product/support page (the download behind it requires a
   license/login), a *Cloud* row has no installer. **Expected result:** five
   verified `Product / Source / Access / As-of` rows.
4. For any source that has **moved** (a changed portal domain or releases
   URL), draft the exact corrected table row as it should appear here.
   **Expected result:** a ready-to-apply correction, or a note that all five
   are current.
5. Negative test: attempt to locate a **non-vendor** "free download" of one
   *Entitlement* product (e.g. an enterprise firewall image on a file-sharing
   site) and confirm this chapter does **not** link to any such source, only
   the vendor portal. **Expected result:** a confirmed compliance check that
   the inventory sources only official, vendor-owned locations.
6. Write a one-paragraph recommendation: what event should trigger an
   out-of-cycle review of this table (for example a vendor acquisition moving
   a download portal, as with VMware to Broadcom), and how it should stay in
   lockstep with `SOFTWARE_VERSIONS.md`. **Expected result:** a concrete,
   justified review-trigger recommendation.

**Rollback:** None; this lab is read-only against external sources and
downloads nothing.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter is the encyclopedia's single lookup for **what software it uses,
at what version, and where to get it**. Versions mirror the authoritative
`SOFTWARE_VERSIONS.md` baseline; this chapter adds, for each product, the
**official** download or acquisition source and an **access class** — *Free*
(publicly downloadable), *Entitlement* (vendor portal, license/contract
required), or *Cloud* (a service with nothing to download). Every source is
the vendor or project's own distribution point, never a third-party mirror,
which is both a correctness and a security control. When a version changes it
changes in `SOFTWARE_VERSIONS.md` first and this table follows, keeping the
two in lockstep per the reference-governance discipline of Chapter 09.

- [ ] The version baseline located and understood as owned by `SOFTWARE_VERSIONS.md`.
- [ ] The official source and access class found for each product in use.
- [ ] Free, Entitlement, and Cloud rows distinguished, and the reader's next action for each understood.
- [ ] The inventory confirmed to source only official, vendor-owned locations.
