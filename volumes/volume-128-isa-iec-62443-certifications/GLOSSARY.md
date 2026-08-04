# Volume CXXVIII — Glossary

| Term | Definition |
|:---|:---|
| **Asset owner** | The organization that operates the IACS and owns its security program and accepted risk (IEC 62443-2-1). |
| **Compensating control** | A control that reduces risk *around* an asset that cannot itself be secured (e.g. MFA at a jump host in front of an unpatchable PLC) — central to OT design. |
| **Conduit** | A controlled communication path between zones; a specific, enumerated set of permitted flows, with everything else denied — the realization of FR5. |
| **CRS (Cybersecurity Requirements Specification)** | The design deliverable listing the system requirements each zone must meet, traceable to its SL-Target and the underlying risk. |
| **Expert (ISA/IEC 62443 Cybersecurity Expert)** | The designation conferred automatically on holders of all four certificates; no separate exam. |
| **Foundational Requirement (FR1–FR7)** | The seven capability categories every zone is measured against: IAC, UC, SI, DC, RDF, TRE, RA. |
| **IACS** | Industrial Automation and Control Systems — the OT estate (PLCs, SCADA, DCS, RTUs, HMIs) 62443 secures. |
| **IC32 / IC33 / IC34 / IC37** | The courses behind Certificates 1–4: Fundamentals, Risk Assessment, Design, Maintenance (each with V/E/M format variants). |
| **IEC 62443** | The standard series: 1-x general/concepts, 2-x policies/procedures, 3-x system, 4-x component. |
| **Priority inversion (OT)** | In IACS, availability and safety outrank confidentiality (A→I→C), reversing the IT C→I→A ordering — the driver of every 62443 control decision. |
| **Product supplier** | The vendor that builds components/systems; owns secure development (4-1) and component requirements (4-2). |
| **Purdue model** | The layered reference architecture (Levels 0–5) with the IT/OT DMZ between Levels 3 and 4, used to structure zones. |
| **Security Level (SL 0–4)** | A measure of protection strength, expressed as a vector across the seven FRs; SL-Target is required, SL-Achieved is delivered. |
| **Service provider (integration/maintenance)** | The organization that designs, integrates, and maintains the IACS; owns the requirements in 62443-2-4. |
| **SL-A / SL-T** | Security Level Achieved (what the deployed controls deliver) and Security Level Target (what risk requires); the gap drives design. |
| **SuC (System under Consideration)** | The boundary of what a risk assessment covers. |
| **System Requirement (SR)** | A specific security requirement in IEC 62443-3-3, grouped under an FR, with Requirement Enhancements that raise the achievable SL. |
| **Virtual patching** | Mitigating a vulnerability at the network/conduit (block or monitor the exploit path) without modifying the vulnerable asset — the OT answer to unpatchable devices. |
| **Zone** | A grouping of assets with common security requirements; the unit that carries an SL-Target and is protected by conduits (FR5). |
