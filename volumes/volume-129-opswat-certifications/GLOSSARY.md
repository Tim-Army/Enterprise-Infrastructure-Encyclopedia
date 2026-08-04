# Volume CXXIX — Glossary

| Term | Definition |
|:---|:---|
| **CIP (Critical Infrastructure Protection)** | Defending the systems society depends on (energy, water, manufacturing, healthcare, government) where attacks threaten safety and continuity, not just data. |
| **CyberOps** | The OPSWAT Academy track of hands-on, authorized defensive/analysis skills — protocol analysis, PLC security, OSINT, red/blue fundamentals. |
| **Deep CDR (Content Disarm and Reconstruction)** | OPSWAT's flagship technique: rebuild a file without any active/abnormal content, removing the threat vector whether or not it was detected — zero-day-resistant. |
| **ICAP** | The protocol web proxies use to offload content inspection; MetaDefender ICAP applies CDR/multiscan/DLP to web downloads and uploads inline. |
| **ICIP** | Introduction to Critical Infrastructure Protection — OPSWAT's free entry certification on CIP concepts. |
| **Kiosk (MetaDefender Kiosk)** | A media-scanning station at the OT perimeter: removable media is multiscanned + sanitized (CDR) before any vetted copy crosses into the network — vital for air-gapped OT. |
| **MetaAccess** | OPSWAT's endpoint compliance / network access control — admits only devices meeting posture policy. |
| **MetaDefender Core** | The platform's scanning hub (multiscanning + Deep CDR + Proactive DLP + sandbox) that the edge products feed files through. |
| **MetaDefender Vault** | Secure, scanned file storage with access control and approval-gated, audited release across trust zones. |
| **Multiscanning** | Running many anti-malware engines in parallel so the union of their detections catches far more known malware than any single engine. |
| **NAC (Network Access Control)** | Controlling which devices join the network and what they may reach, by identity and posture; enforced at layer 2 (802.1X, blocks before an IP) or layer 3 (filters routing after admission). |
| **OCFA / OECA / OFSA / ONSA / OSSA** | OPSWAT Associate certifications: Cybersecurity Fundamentals, Endpoint Compliance, File Security, Network Security, Secure Storage. |
| **OT Security Expert** | OPSWAT's expert designation for end-to-end critical-infrastructure defense (boundary architecture, MetaDefender deployment, OT operations, 62443 alignment). |
| **Posture** | A device's security state (patching, AV, encryption, configuration) evaluated before network admission. |
| **Proactive DLP** | Finding and redacting/blocking sensitive data (PII/PHI/secrets) inside files before they cross a boundary. |
| **Static vs dynamic analysis** | Inspecting a file without executing it (structure, true file type, metadata) versus detonating it in a sandbox to observe behavior. |
| **Trust no file, no device** | OPSWAT's CIP premise: every file may be weaponized and every device may be a carrier, so inspect and sanitize at every boundary. |
| **True file type** | The actual format of a file determined by its content, not its extension — a core file-security check against extension spoofing. |
