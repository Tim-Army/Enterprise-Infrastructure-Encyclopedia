# Chapter 15: Comparison Matrix, Compliance, and Sources

## Learning Objectives

- Compare every option in this volume on one page: model, cost, effort, and requirements.
- Read the compliance columns correctly, including the distinctions vendors blur.
- Verify FIPS 140-3 and FedRAMP status yourself against the authoritative registries.
- Judge which options survive an air-gapped deployment.
- Complete a walkthrough for each comparison topic.

## How to read these tables

Four warnings, because a comparison table is the artifact in this volume most easily misused.

1. **Cost is quote-required almost everywhere.** Enterprise microsegmentation vendors do not publish
   list pricing. Where a real published figure exists, it is named. Everything else says *quote
   required*, which is a fact about the market, not a gap in this research.
2. **Implementation times are estimates, not vendor commitments.** They are derived from what the
   deployment model requires — agent rollout, hardware procurement, or plant change control — and are
   stated as ranges. No vendor here contractually commits to a timeline.
3. **FIPS 140-3 means a CMVP certificate.** "FIPS-compliant", "uses FIPS-approved algorithms", and
   "FIPS-ready" are marketing phrases that do not mean validated. Only a certificate number in the NIST
   registry counts, and validation is granted to a **specific module, version, and firmware** — never to
   a company.
4. **FedRAMP "In Process" is not authorization.** It appears on the same Marketplace and reads
   similarly. Only *Authorized* with at least one ATO/ATU permits federal use.

Compliance status changes continuously. Every entry below was checked on **30 July 2026**; verify before
relying on any of it.

## Table 1 — Options, models, and current status

| Option | Enforcement model | Chapter | Status | Vendor home |
| --- | --- | --- | --- | --- |
| VMware NSX (DFW) | Hypervisor | 03 | Current | [broadcom.com](https://www.broadcom.com/products/vmware-cloud-foundation/networking) |
| Cisco ACI | Network/fabric | 03 | Current | [cisco.com](https://www.cisco.com/site/us/en/products/networking/cloud-networking/application-centric-infrastructure/index.html) |
| Cisco Secure Workload | Host agent | 04 | Current | [cisco.com](https://www.cisco.com/site/us/en/products/security/secure-workload/index.html) |
| Cisco ISE + TrustSec | NAC group tag | 10 | Current | [cisco.com](https://www.cisco.com/site/us/en/products/security/identity-services-engine/index.html) |
| Arista MSS-Group | Network/fabric | 10 | Current | [arista.com](https://www.arista.com/en/products/multi-domain-segmentation) |
| HPE Aruba CX 10000 | DPU/SmartNIC | 11 | Current | [hpe.com](https://www.hpe.com/us/en/aruba-networking-cx-10000-switch-series.html) |
| Juniper Connected Security | Network/fabric | 10 | Current | [juniper.net](https://www.juniper.net/us/en/security.html) |
| Fortinet ISFW / VDOM | Network/fabric | 10 | Current | [fortinet.com](https://www.fortinet.com/) |
| Check Point CloudGuard | Network/fabric | 10 | Current | [checkpoint.com](https://www.checkpoint.com/cloudguard/) |
| Nutanix Flow Network Security | Hypervisor | 11 | Current | [nutanix.com](https://www.nutanix.com/products/flow-network-security) |
| NVIDIA BlueField | DPU/SmartNIC | 11 | Current | [nvidia.com](https://www.nvidia.com/en-us/networking/products/data-processing-unit/) |
| Illumio | Host agent | 04 | Current | [illumio.com](https://www.illumio.com/) |
| Akamai Guardicore | Host agent | 04 | Current | [akamai.com](https://www.akamai.com/products/akamai-guardicore-segmentation) |
| Zero Networks | Agentless OS-firewall | 05 | Current | [zeronetworks.com](https://zeronetworks.com/) |
| TrueFort | Host agent / EDR-leveraged | 06 | Current | [truefort.com](https://truefort.com/) |
| ColorTokens Xshield | Multi-mode + Gatekeeper | 07 | Current | [colortokens.com](https://colortokens.com/) |
| Elisity | Identity via existing switching | 13 | Current | [elisity.com](https://www.elisity.com/) |
| Tempered Airwall | HIP encrypted overlay | 13 | Current (Johnson Controls) | [temperednetworks.com](https://www.temperednetworks.com/) |
| **vArmour** | Host agent | 13 | **Discontinued** — IP to Fenix24, Jan 2025 | — |
| **Unisys Stealth** | Identity overlay | 13 | **Absorbed** into a managed service | [unisys.com](https://www.unisys.com/solutions/cybersecurity-solutions/) |
| AWS / Azure / GCP native | Cloud-native | 08 | Current | provider consoles |
| Calico | Container/eBPF | 08 | Current | [tigera.io](https://www.tigera.io/project-calico/) |
| Cilium | Container/eBPF | 08 | Current (Cisco/Isovalent) | [cilium.io](https://cilium.io/) |
| Istio | Service mesh | 12 | Current | [istio.io](https://istio.io/) |
| Linkerd | Service mesh | 12 | Current | [linkerd.io](https://linkerd.io/) |
| HashiCorp Consul | Service mesh (+VMs) | 12 | Current (IBM) | [consul.io](https://www.consul.io/) |
| Xage Security | OT identity broker | 14 | Current | [xage.com](https://xage.com/) |
| Claroty xDome | OT visibility (+integrated enforcement) | 14 | Current | [claroty.com](https://claroty.com/) |
| Nozomi Networks | OT visibility (+integrated enforcement) | 14 | Current | [nozominetworks.com](https://www.nozominetworks.com/) |
| TXOne Networks | OT endpoint/network | 14 | Current | [txone.com](https://www.txone.com/) |
| Zscaler / Airgap | Agentless DHCP-proxy isolation | 14 | Current | [zscaler.com](https://www.zscaler.com/) |

## Table 2 — Cost, effort, and system requirements

Implementation times are **estimates derived from the deployment model**, assuming an estate with a
usable asset inventory. They are not vendor commitments.

| Option | Cost model | Impl. time (est.) | Key system requirements |
| --- | --- | --- | --- |
| VMware NSX | Quote required; part of VCF licensing | 2–6 months | vSphere; NSX managers; supported hardware |
| Cisco ACI | Quote required; fabric purchase | 6–18 months | Nexus 9000 fabric; APIC cluster |
| Cisco Secure Workload | Quote required | 3–9 months | Agents on workloads; on-prem or SaaS control plane |
| Cisco ISE + TrustSec | **ISE Advantage, per endpoint** (concurrent active sessions) | 3–9 months | ISE; 802.1X/MAB; inline tagging on Catalyst 9200/9300/9400/9500 or Nexus 9000, else SXP (ISE 3595 caps at **20,000 SXP bindings**) |
| Arista MSS-Group | Quote required (CloudVision subscription) | 6–12 weeks | EOS switches; CloudVision; identity source (AGNI, vCenter, ServiceNow, Infoblox, CSV) |
| HPE Aruba CX 10000 | **Published list price on the HPE Store** | 3–6 months (procurement-gated) | CX 10000 series; AOS-CX; AMD Pensando DPU; CX 10040 = 8 Tbps switching / **1.6 Tbps L4 stateful** |
| Juniper Connected Security | Quote required | 3–9 months | SRX/cSRX; Apstra for fabric intent |
| Fortinet ISFW / VDOM | Quote required | 2–6 months | FortiGate; FortiManager; FortiNAC for identity |
| Check Point CloudGuard | Quote required | 2–6 months | CloudGuard gateways; Security Management |
| Nutanix Flow | **Per-node annual subscription, 1–5 yr terms**; licenses for **every node** in a protected cluster | 2–6 weeks | AHV only; Prism Central (Starter+); policy **does not replicate between Prism Central instances** |
| NVIDIA BlueField | Per-adapter, via server vendors | 3–6 months | Supported servers; DPU-side enforcement stack |
| Illumio | Quote required | 3–9 months | Agents (VEN); PCE control plane |
| Akamai Guardicore | Quote required | 3–9 months | Agents; management plane |
| Zero Networks | Quote required | 4–12 weeks | Windows/Linux host firewalls; privileged access to manage them |
| TrueFort | Quote required | 2–8 weeks (faster where EDR exists) | Existing EDR telemetry or agent |
| ColorTokens Xshield | Quote required | 4–12 weeks | SaaS console; agent, EDR, cloud, K8s, or Gatekeeper per asset |
| Elisity | Quote required (endpoints/term) | 4–10 weeks | Supported access switching; identity sources for IdentityGraph |
| Tempered Airwall | Quote required (incl. gateways) | 6–16 weeks | Airwall gateways in path; Conductor console |
| Cloud-native | **Included** in cloud subscription | 1–4 weeks per account | Provider IAM and network constructs |
| Calico / Cilium | **Open source, free**; paid enterprise tiers | 2–8 weeks | Kubernetes; CNI replacement or overlay |
| Istio / Linkerd / Consul | **Open source, free**; optional commercial support | 4–10 weeks to mTLS-everywhere | Kubernetes (Consul also VMs); CA or SPIRE; control plane |
| Xage Security | Quote required | 3–9 months | Fabric nodes near assets; identity sources |
| Claroty xDome | Quote required + services | 2–6 weeks visibility; 6–18 months enforcement | Span/tap collection; site surveys |
| Nozomi Networks | Quote required + services | 2–6 weeks visibility; 6–18 months enforcement | Span/tap collection; sensors per site |
| TXOne | Quote required | 2–6 months | OT-appropriate endpoints/network points |
| Zscaler / Airgap | Quote required | 4–12 weeks | **Control of DHCP** (proxy architecture); Zscaler tenancy |

## Table 3 — FIPS 140-3, FedRAMP, and air-gap

*Verified 30 July 2026.* "Verify" means no determination was made in this pass and you must check the
registry yourself — it does not mean absent.

| Option | FIPS 140-3 (CMVP) | FedRAMP | Air-gap capable |
| --- | --- | --- | --- |
| **Xage Security** | **Validated — cert #5229**, FIPS 140-3, 07 Apr 2026 (prior #4620, 140-2) | Verify | Yes — on-prem |
| **Illumio** | No CMVP results under vendor name | **Authorized — Moderate**, 21 Aug 2024, 1 ATO ([listing](https://www.fedramp.gov/marketplace/products/FR2230244107/)) | Yes — on-prem PCE |
| **Claroty xDome** | Verify | **In Process — High**, 0 ATOs, as of 20 Feb 2026 ([listing](https://www.fedramp.gov/marketplace/products/FR2323961436/)) — **not usable for federal data yet** | Yes — on-prem |
| **Zscaler / Airgap** | Verify | Authorized government offerings incl. ZPA-Gov ([listing](https://www.fedramp.gov/marketplace/products/FR1719759604/)); confirm the segmentation service is in scope | Cloud-delivered — confirm on-prem enforcement |
| **Nozomi Networks** | No CMVP results under vendor name | Verify | Yes — on-prem, confirm content update path |
| **Elisity** | No CMVP results under vendor name | No listing found | Cloud control plane — **confirm with vendor** |
| Tempered Airwall | Verify | Verify | Yes — Conductor on-prem |
| Cisco (ACI, ISE, Secure Workload) | Vendor holds validations; **verify per platform and firmware** | Verify per service | Yes — on-prem |
| Arista MSS | Verify per platform | Verify (CloudVision-as-a-Service) | Yes — CloudVision on-prem |
| HPE Aruba CX 10000 | Verify per platform/firmware | N/A (on-prem product) | Yes |
| Juniper / Fortinet / Check Point | Vendor holds validations; verify per model | Verify per cloud service | Yes — on-prem management |
| Nutanix Flow | Verify | N/A (on-prem product) | Yes — Prism Central on-prem |
| NVIDIA BlueField | Verify per firmware | N/A | Yes |
| VMware NSX | Verify per version | N/A (on-prem product) | Yes |
| Akamai Guardicore / TrueFort / ColorTokens | Verify | ColorTokens: FedRAMP Moderate (Ch. 07); others verify | Verify per control plane |
| Zero Networks | Verify | Verify | Verify — control plane dependency |
| Cloud-native (AWS/Azure/GCP) | Provider modules validated; verify per service | Provider services authorized at various levels | No — cloud only |
| Calico / Cilium | Verify build; upstream community builds generally **not** validated | N/A (software you run) | Yes — mirror images |
| Istio / Linkerd / Consul | FIPS-mode builds exist; **upstream builds generally not validated** | N/A (software you run) | Yes — fully self-hosted |
| TXOne | Verify | Verify | Yes — on-prem |

**Authoritative registries.** Check FIPS in the
[NIST CMVP validated modules search](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search)
and FedRAMP in the [FedRAMP Marketplace](https://marketplace.fedramp.gov/).

## Hands-On Lab

### Lab 15.1 — Filter the matrix by hard constraints

**Objective.** Reduce 30-plus options to a shortlist using disqualifying constraints, not preferences.

```python
options = {
    "istio":        {"agentless": False, "air_gap": True,  "fedramp": False},
    "elisity":      {"agentless": True,  "air_gap": False, "fedramp": False},
    "xage":         {"agentless": True,  "air_gap": True,  "fedramp": False},
    "illumio":      {"agentless": False, "air_gap": True,  "fedramp": True},
    "cx10000":      {"agentless": True,  "air_gap": True,  "fedramp": False},
}
need = {"agentless": True, "air_gap": True}          # disconnected OT site
for name, o in options.items():
    ok = all(o[k] == v for k, v in need.items())
    print(f"{name:<12}{'SHORTLIST' if ok else 'excluded'}")
```

**Expected result.** `xage` and `cx10000` survive; the rest are excluded by a hard constraint.

**Negative test.** Filter on preferences (vendor familiarity, analyst ranking) instead of constraints.
Options that cannot physically work in a disconnected, agent-hostile site stay on the list and waste a
procurement cycle.

**Cleanup.** None.

### Lab 15.2 — Distinguish validated from claimed FIPS

**Objective.** Apply the only test that matters.

```python
claims = {
    "Xage":    {"marketing": "FIPS 140-3 certified", "cmvp_cert": 5229},
    "VendorA": {"marketing": "FIPS-compliant encryption", "cmvp_cert": None},
    "VendorB": {"marketing": "uses FIPS-approved algorithms", "cmvp_cert": None},
}
for v, c in claims.items():
    print(f"{v:<10}{c['marketing']:<34}"
          f"{'VALIDATED cert #' + str(c['cmvp_cert']) if c['cmvp_cert'] else 'NOT VALIDATED'}")
```

**Expected result.** Only Xage is validated; the other two phrasings carry no validation.

**Negative test.** Accept "FIPS-compliant" in a requirements matrix. It commonly means the product calls
approved algorithms from an unvalidated implementation — which fails a FIPS control.

**Cleanup.** None.

### Lab 15.3 — Build a weighted shortlist from the matrix

**Objective.** Rank the survivors of Lab 15.1 rather than the whole market.

```python
weights = {"granularity": 0.35, "effort": 0.30, "coverage": 0.20, "cost_clarity": 0.15}
shortlist = {
    "xage":    {"granularity": 4, "effort": 2, "coverage": 4, "cost_clarity": 1},
    "cx10000": {"granularity": 4, "effort": 2, "coverage": 3, "cost_clarity": 5},
}
for name, s in shortlist.items():
    print(f"{name:<10}{sum(weights[k] * s[k] for k in weights):.2f} / 5.00")
```

**Expected result.** cx10000 3.35, xage 3.05 — published pricing is the differentiator once the hard
constraints are met.

**Negative test.** Remove `cost_clarity`. The two tie, and you lose the only column where one option
gives you a number without a sales cycle.

**Cleanup.** None.

### Lab 15.4 — Re-verify a compliance claim

**Objective.** Practice the check this chapter asks you to repeat.

```text
1. Open the NIST CMVP search and query the vendor name exactly.
2. Match the module name AND the version/firmware you will deploy.
3. Confirm the certificate is Active, not Historical.
4. Open the FedRAMP Marketplace and read the status field, impact level, and ATO count.
5. Record the date you checked beside the finding.
```

**Expected result.** A dated, sourced compliance statement you can defend in an audit.

**Negative test.** Cite a vendor datasheet instead. Datasheets routinely claim validation held by a
different module version, or by an OEM component rather than the product.

**Cleanup.** None.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This matrix compares every option in the volume on model, cost, effort, requirements, and compliance —
and its most important lesson is how to read it: pricing is quote-required across almost the whole
market, implementation timelines are estimates governed by deployment model rather than vendor promises,
FIPS means a CMVP certificate for a specific version, and FedRAMP "In Process" is not authorization.

- [ ] I can filter the matrix by hard constraints before preferences.
- [ ] I can tell a CMVP-validated module from a FIPS marketing claim.
- [ ] I can read a FedRAMP listing correctly, including In Process.
- [ ] I completed Labs 15.1–15.4 including each negative test.
