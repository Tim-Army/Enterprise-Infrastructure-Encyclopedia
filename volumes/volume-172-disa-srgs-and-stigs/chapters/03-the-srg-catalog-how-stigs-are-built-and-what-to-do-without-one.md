# Chapter 03: The SRG Catalog, How STIGs Are Built, and What to Do Without One

## Learning Objectives

- Name the main technology SRGs and the kinds of products each one governs.
- Explain how one product can fall under several SRGs at once, and why network
  devices usually have more than one STIG.
- Describe how STIGs are produced from SRGs, including the vendor-developed
  STIG process.
- Explain the quarterly release cycle and what happens when a STIG is sunset.
- Assess a product that has no STIG directly against the applicable SRG.

## Theory and Architecture

An SRG captures what DoD requires of a whole technology class. DISA maintains a
set of them, and every product STIG is written against one or more. The exact
list changes over time as DISA adds, merges, and retires SRGs, so treat the
table below as orientation and confirm current names and releases in the SRG
section of the DoD Cyber Exchange library.

| SRG (commonly used) | Governs | Example products with STIGs |
| --- | --- | --- |
| **General Purpose Operating System (GPOS)** | Server and desktop operating systems | Windows, RHEL, Ubuntu, other Linux distributions |
| **Network Device Management (NDM)** | The management plane of any network device | Routers, switches, firewalls, load balancers |
| **Router** | Routing and forwarding functions | Router STIGs for major vendors |
| **Firewall** | Traffic filtering functions | Firewall STIGs for major vendors |
| **Application Layer Gateway (ALG)** | Proxies and application-aware inspection | Next-generation firewall and proxy STIGs |
| **Intrusion Detection and Prevention Systems (IDPS)** | Network intrusion detection and prevention | IPS functions of security appliances |
| **Virtual Private Network (VPN)** | VPN gateways and remote access | VPN STIGs for gateways and firewalls |
| **Application Server** | Middleware that hosts applications | Java application servers, other middleware |
| **Database** | Database management systems | Relational database STIGs |
| **Web Server** | HTTP servers | Web server STIGs |
| **Container Platform** | Container orchestration platforms | Kubernetes distribution STIGs |
| **Cloud Computing** | Cloud service offerings and impact levels | Not configuration STIGs; see Chapter 08 |

Alongside the SRGs, DISA publishes a few **cross-cutting STIGs** that are not
tied to a single product. The most important is the **Application Security and
Development STIG**, which applies to custom software DoD develops or acquires
(Chapter 08).

### One product, several SRGs

SRGs are written per *function*, and many products perform several functions.
A next-generation firewall, for example, has a management plane, filters
traffic, inspects applications, detects intrusions, and terminates VPNs. Each
function maps to a different SRG, so the vendor's STIG content is usually split
along the same lines:

```text
Next-generation firewall
├── NDM STIG    management access, accounts, logging, banners, time
├── Firewall / ALG STIG   traffic filtering and application inspection
├── IDPS STIG   intrusion prevention settings
└── VPN STIG    tunnels and remote access (if the feature is used)
```

You assess every STIG that matches a function you have **enabled**. If the VPN
feature is not licensed or not configured, the VPN STIG rules are typically
recorded as Not Applicable, with that justification.

### How STIGs are made

STIGs reach the library in two ways:

1. **DISA-developed.** DISA writes the STIG itself, translating each applicable
   SRG requirement into product-specific checks and fixes.
2. **Vendor-developed.** The vendor writes the STIG against the SRG under DISA's
   vendor STIG development process. DISA provides the SRG and templates, the
   vendor maps each requirement to its product and writes the check and fix
   text, and DISA reviews and validates the content before publishing it under
   DISA's name. Vendors do this because having a published STIG matters for
   selling into DoD.

Either way, the result is checked against the SRG. Each SRG requirement ends up
in the STIG in one of three forms: as a rule with check and fix text; as a rule
the product meets by design; or, where the product cannot meet it, as a
documented gap that becomes a permanent finding the customer must mitigate.

### The release cycle

DISA releases STIG and SRG updates on a quarterly schedule, typically early in
January, April, July, and October, with out-of-cycle releases when urgent. Each
quarterly release refreshes the library compilation. Over a product's life, a
STIG moves through these states:

- **Draft.** Published for public comment before the first release.
- **Released.** The current authoritative content.
- **Sunset.** The product reached end of support or the STIG was replaced. DISA
  stops maintaining a sunset STIG; running a product whose STIG is sunset
  generally means running unsupported software, which is itself a finding.

## Design Considerations

- **Inventory functions, not boxes.** List each device's enabled functions and
  map them to SRGs. That tells you which STIGs apply before you open a single
  checklist.
- **Prefer products with a published STIG.** A product with a vendor STIG has a
  known compliance path. A product without one means you write and defend your
  own SRG assessment, which costs more effort and invites more scrutiny.
- **Ask vendors about STIG status during procurement.** Whether a STIG exists,
  is in development, or is planned should be part of the evaluation.
- **Watch the sunset list.** Plan platform refreshes before a product's STIG is
  sunset, not after.
- **Align upgrade timing with STIG releases.** A major product upgrade may wait
  on DISA or the vendor publishing the matching STIG.

## Implementation and Automation

### Find which STIGs implement an SRG requirement

Because every STIG rule records its SRG ID, you can search the whole library
for every product rule that implements a given requirement. Extract the library
compilation once, then search across all XCCDF files:

```bash
mkdir -p ~/stig/library && cd ~/stig/library
unzip -q ~/Downloads/<STIG_LIBRARY_COMPILATION>.zip
# The compilation contains nested ZIPs; extract them all
find . -name "*.zip" -exec sh -c 'unzip -q -o "$1" -d "${1%.zip}"' _ {} \;
grep -rl --include="*xccdf.xml" "<SRG_ID>" . | sort
```

Replace `<SRG_ID>` with an identifier copied from a STIG rule, such as the
`SRG-OS-...` ID behind the failed logon rule traced in Chapter 01. The output lists every STIG, across vendors and products, that implements
that requirement.

### Assess a product that has no STIG

When no STIG exists, assess against the applicable SRG directly:

1. Identify the SRGs that match the product's functions (for an appliance, at
   least NDM plus one per traffic function).
2. Download the SRG and open it in STIG Viewer (Chapter 04) or convert it to a
   spreadsheet with the Chapter 02 script.
3. For each requirement, work out how the product meets it, using vendor
   documentation and testing. Record the product-specific setting or evidence.
4. Give every requirement a status: met (Not a Finding), not met (Open), or not
   applicable, with a justification for anything that is not met or not
   applicable.
5. Treat the result as your own product-specific checklist. Keep it with the
   system's authorization package and review it each quarter.

This is the same work a vendor does to create a STIG, without DISA's validation.
Expect assessors to look at it more closely than a published STIG.

## Validation and Troubleshooting

- **The search returns nothing for an SRG ID.** Check you extracted the nested
  ZIPs, and that the ID is copied exactly. Some IDs exist only in the SRG
  because no product STIG implements them yet.
- **Two STIGs both seem to cover a device.** That is normal for multi-function
  products. Assess each STIG for the functions you use.
- **A rule says the product "does not support" the requirement.** That is a
  documented product gap. It stays a finding and needs a mitigation or risk
  acceptance; it is not Not Applicable.
- **You cannot find a STIG you used last year.** It may have been sunset or
  renamed. Check the Cyber Exchange's sunset list.

## Security and Best Practices

- Never mark an SRG requirement Not Applicable just because there is no STIG.
  The requirement still applies to the product.
- Document the functions you rely on and the STIGs that cover them, so an
  assessor can see the scope at a glance.
- Disable functions you do not use. Fewer enabled functions means fewer STIGs,
  fewer rules, and less attack surface.
- Retire products before their STIGs are sunset, or plan the risk acceptance
  well before the date.

## References and Knowledge Checks

**References:**

- DoD Cyber Exchange SRG and STIG library, including the sunset STIG list.
- DISA guidance on the vendor STIG development process, published on the DoD
  Cyber Exchange.
- The Application Security and Development STIG.

**Knowledge checks:**

1. Why does a next-generation firewall usually have more than one STIG?
2. Which SRG covers the management plane of every network device?
3. Describe the two ways STIGs are produced, and who validates both.
4. What should you do with a product that has no STIG?
5. Why is a "product does not support" rule not the same as Not Applicable?

## Summary and Completion Checklist

DISA maintains SRGs per technology function: operating systems, network device
management, routing, filtering, application gateways, intrusion prevention,
VPN, application servers, databases, web servers, and container platforms.
Multi-function products fall under several SRGs and so carry several STIGs.
STIGs come from DISA or from vendors under DISA's validation process, are
updated quarterly, and are eventually sunset. When no STIG exists, the SRG still
applies and you assess the product against it directly.

- [ ] Can name the main technology SRGs and what each governs.
- [ ] Can explain why multi-function devices carry several STIGs.
- [ ] Can describe the DISA-developed and vendor-developed STIG paths.
- [ ] Can assess a product against an SRG when no STIG exists.
