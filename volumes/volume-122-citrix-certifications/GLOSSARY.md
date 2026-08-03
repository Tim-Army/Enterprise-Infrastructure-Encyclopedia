# Volume CXXII — Glossary

| Term | Definition |
|:---|:---|
| **AppDS** | App Delivery and Security — the NetScaler certification track (CCA-AppDS, CCP-AppDS). |
| **AppFlow** | NetScaler's per-transaction telemetry export (IPFIX) to a collector such as NetScaler Console. |
| **App Protection** | CVAD policies enforcing anti-keylogging and anti-screen-capture at brokering time for a delivery group. |
| **CCA-AppDS** | Citrix Certified Associate — App Delivery and Security: one credential earned by either the Gateway exam or the Traffic Management exam. |
| **CCA-V** | Citrix Certified Associate — Virtualization; its exam (*Citrix Virtual Apps and Desktops Administration*) replaced the retired 1Y0-204. |
| **CCE-V / CCE-N** | The discontinued Citrix Certified Expert credentials; the current ladder tops out at Professional. |
| **CCP-AppDS** | Citrix Certified Professional — App Delivery and Security; exam 1Y0-342 (*NetScaler Advanced Topics — Security, Management and Optimization*). |
| **CCP-V** | Citrix Certified Professional — Virtualization; prerequisite CCA-V. |
| **Cloud Connector** | The outbound-only agent pair that joins an on-premises resource location to the Citrix Cloud control plane, replacing local Delivery Controllers. |
| **Cloud Software Group (CSG)** | The company (Citrix + TIBCO) that runs the Citrix and NetScaler products and certification programs. |
| **Content switching** | One NetScaler VIP steering requests to different virtual servers by policy; precedence is priority order, lowest number first. |
| **CPX Express** | The free containerized NetScaler — the lab target for this volume's AppDS CLI walkthroughs. |
| **Delivery Controller** | The CVAD site's broker; sessions, power, and configuration flow through it (or through Cloud Connectors in Citrix Cloud). |
| **Delivery group** | The CVAD entitlement object: which users get which catalog machines, apps, and desktops. |
| **Director** | The CVAD monitoring and help-desk console; Trends holds the historical views. |
| **GSLB** | Global Server Load Balancing — DNS-based multi-site distribution; sites exchange health via the Metric Exchange Protocol (MEP). |
| **ICA proxy** | The Gateway mode that proxies HDX sessions through 443 to a StoreFront-fronted CVAD site — the classic remote-access deployment. |
| **Local Host Cache** | The controller-side fallback that keeps brokering alive when the site database is unreachable. |
| **Machine catalog** | The CVAD machine pool (MCS- or PVS-provisioned) that delivery groups draw from. |
| **MCS / PVS** | Machine Creation Services (differencing-disk clones) and Provisioning (streamed vDisk) — CVAD's two provisioning models. |
| **NetScaler Console** | The fleet management plane (formerly Citrix ADM): inventory, security/SSL dashboards, events, Stylebooks, configuration audit. |
| **nFactor** | NetScaler's chained authentication framework: login schemas collect, policies validate, policy labels chain the next factor. |
| **NSIP / SNIP / VIP** | NetScaler's three address roles: management, back-end source, and client-facing service. |
| **nstrace** | NetScaler's on-box packet capture; filter at capture time. |
| **Performance-based items** | Hands-on exam items (~10% of AppDS forms; CLI simulations on the TM exam) — the reason lab hours are non-negotiable. |
| **STA** | Secure Ticket Authority — controllers issue launch tickets that Gateway validates; mismatched STA lists break launches while enumeration still works. |
| **StoreFront** | The on-premises store users authenticate to and launch from; Workspace is its cloud counterpart. |
| **Stylebook** | A NetScaler Console configuration-as-code template; deployments are versioned and auditable. |
| **URL transform** | The NetScaler feature translating whole URLs bidirectionally — the third rewriting tool beside rewrite and responder. |
| **Web App Firewall (WAF)** | NetScaler's application firewall: profiles hold checks (Start URL, SQL injection, XSS, bot), policies select traffic; learn-then-block is the deployment discipline. |
| **Webassessor** | The Kryterion exam platform where Citrix and NetScaler exams are delivered and credentials are recovered. |
| **WEM** | Workspace Environment Management — agent-side actions and resource optimization that offload logon work from GPO/scripts. |
