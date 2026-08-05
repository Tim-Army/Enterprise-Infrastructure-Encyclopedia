# Volume CLIII — Glossary

| Term | Definition |
|:---|:---|
| **Active-active links** | Using all of a site's internet links simultaneously (not one as cold standby), with application-aware routing sending each app over the best link and failing over sub-second when one degrades. |
| **Backhaul** | Routing traffic back to a central data-center appliance stack for security before sending it to its destination — absurdly inefficient when the app is in the cloud and the user is remote. SASE eliminates it by inspecting at a PoP near the user. |
| **CASB** | Cloud Access Security Broker — discovers, assesses, and governs cloud/SaaS application usage, notably solving shadow IT by surfacing unsanctioned apps from the traffic and controlling what data flows to them. |
| **Convergence** | The core SASE idea: delivering networking (SD-WAN) and all security functions as one natively-integrated cloud service with one policy and one console, versus a stack of separate point products with seams between them. |
| **FWaaS** | Firewall-as-a-Service — the firewall delivered from the cloud rather than as an appliance, enforcing network security policy for all traffic through the PoPs, everywhere. |
| **Global backbone** | Cato's worldwide network of PoPs connected by optimized, SLA-backed private links — providing presence near every user and faster-than-internet routing between regions. |
| **Point-product stack** | The traditional approach of assembling separate appliances (SD-WAN, firewall, SWG, CASB, VPN, IPS), each with its own console and policy, integrated by the customer — with complexity, latency, and gaps at the seams. |
| **SASE** | Secure Access Service Edge (Gartner, 2019) — the convergence of networking and network security into one cloud-delivered, identity-driven service at the edge, near the user. |
| **SD-WAN** | Software-Defined WAN — using commodity internet links intelligently (active-active, application-aware) to connect sites, delivering MPLS-grade reliability at internet cost. The networking half of SASE. |
| **Shadow IT** | Cloud/SaaS apps employees adopt without IT's knowledge or approval — a data-leak and compliance risk that CASB discovers and governs from the full traffic. |
| **Single-pass architecture** | Decrypting and parsing traffic once, then applying every security function against that one representation — versus service chaining, which re-inspects per function. What makes converging many functions performant. |
| **SSE** | Security Service Edge — the security subset of SASE (SWG, CASB, ZTNA, FWaaS) without the networking; "SASE minus the WAN," for organizations adopting the security transformation without changing their network. |
| **SWG** | Secure Web Gateway — inspects and secures users' web/internet access (blocking malware, phishing, forbidden categories), protecting users wherever they are from the PoP near them. |
| **ZTNA** | Zero Trust Network Access — the VPN replacement: connects a verified identity to only the specific applications it is authorized for (least privilege), with everything else invisible (dark), eliminating lateral movement. |
| **Zero trust** | "Never trust, always verify" — no user or device is trusted by network location; every access request is authenticated, authorized, and continuously verified, at least privilege. |
