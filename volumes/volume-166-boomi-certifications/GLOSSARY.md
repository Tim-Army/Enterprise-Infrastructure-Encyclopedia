# Volume CLXVI — Glossary

| Term | Definition |
|:---|:---|
| **API Control Plane** | Boomi's federated API governance across gateways and teams — discovering, managing, and securing the whole API estate to fight API sprawl and retire "zombie APIs" (undocumented, unused endpoints). |
| **API Management (APIM)** | The Boomi service for publishing integration processes as governed APIs behind a gateway that enforces authentication, rate limiting, and observability. Certified as Professional API Design and Professional API Management. |
| **Atom** | Boomi's signature lightweight runtime engine that executes integration processes. Designed centrally in the cloud and deployed wherever the data lives (data center, cloud VPC, edge) — design centrally, execute locally. |
| **Atom Cloud** | A Boomi-hosted, multi-tenant runtime — Boomi runs and maintains it; you just deploy processes. Ideal for cloud-to-cloud integration with no infrastructure to manage. |
| **Boomi AI** | Boomi's generative-AI capabilities: Boomi Companion (AI-assisted build/co-creation), Agentstudio (build AI agents), and Boomi GPT (conversational interface). Training exists; no dedicated certification yet. |
| **Boomi Enterprise Platform** | Boomi's unified, low-code, cloud-native iPaaS (formerly AtomSphere) — one platform of services (Integration, APIM, B2B/EDI, Flow, Data Hub, Event Streams, Boomi AI, and more) to connect apps, data, people, and devices. |
| **Connector** | Pre-built connectivity to an application or technology (Salesforce, SAP, databases, HTTP). A connection holds endpoint + credentials; an operation defines the action — configure rather than code a client. |
| **Contribute and publish** | Data Hub's two-way sync — sources contribute records into the hub (matched into golden records), and the hub publishes updated golden records back to connected systems so a fix made once propagates everywhere. |
| **Data Hub** | Boomi's master data management service — models (domains), sources, and match rules produce golden records synchronized across systems. Certified as Associate Data Hub and Professional Data Hub Developer. |
| **Flow** | Boomi's low-code service for building workflow applications and user-facing apps with people in the loop — human steps, generated UIs, and orchestration of integrations. Certified as Associate Flow Essentials. |
| **Golden record** | The single trusted version of an entity (customer, product) that Data Hub builds by matching and merging contributed source records with survivorship, keeping links back to each source. |
| **Integration process** | The core Boomi artifact — a visual, left-to-right flow of documents through shapes (Connector, Map, Decision, Branch, Try/Catch) from a source to a target. Certified as Associate/Professional Integration Developer. |
| **Map** | The shape that transforms one data structure into another — connecting a source profile to a target profile field by field, with functions (upper-case, convert, look up) in between. |
| **Molecule** | A clustered, multi-node Atom acting as one logical runtime with load balancing and high availability — the production runtime form, run on your own infrastructure. |
| **Profile** | A definition of a data structure (XML, JSON, database, flat file, EDI) — how Boomi knows the fields on the source and target sides of a map. |
| **Runtime placement** | The architecture decision of where to run an Atom/Molecule/Atom Cloud, driven by data residency, high availability, and connectivity (e.g. inside a firewall to reach an on-prem database). The Runtime Architect focus. |
| **Shape** | A building block placed on the process canvas — Connector, Map, Decision, Branch, Route, Data Process, Try/Catch, Stop — wired together to define an integration's logic visually. |
| **Trading Partner** | A Boomi component representing one external partner and its communication + document standards, used with the Trading Partner step to send/receive EDI (X12, EDIFACT) documents. |
| **X12** | The dominant North American EDI standard; documents are identified by numeric transaction sets — 850 (Purchase Order), 810 (Invoice), 856 (Advance Ship Notice), 997 (Functional Acknowledgement). Certified as Associate EDI for X12. |
| **Open-book / open-platform exam** | Boomi's exam format — you may consult documentation and the live Boomi platform during the exam, with no time limit, mixing multiple-choice/multiple-response with a hands-on practical section. |
