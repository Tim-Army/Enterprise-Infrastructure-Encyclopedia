# Volume CLIX — Glossary

| Term | Definition |
|:---|:---|
| **Account Lifecycle Manager (ALM)** | Delinea's service-account governance product — discovers service accounts across the estate, maps their dependencies, onboards them into the vault with owners and rotation, and manages them through decommissioning; closes the service-account-sprawl gap. |
| **Active Directory bridging** | Extending Active Directory authentication and policy to Linux and Unix servers (via Kerberos), part of Server PAM, so servers authenticate against one governed AD identity per user instead of scattered local accounts. |
| **Associate** | The entry Delinea Security Academy tier — self-paced, online-only, e-learning coursework plus an online certification exam, building technical understanding toward the Engineer tier. |
| **Consultant** | The advanced Delinea tier (by invitation, for partners) — customizations, integrations, and extensibility, validated through coursework, an online exam, and hands-on technical labs. |
| **Delinea Platform** | The unified, cloud-native SaaS control plane tying the Delinea portfolio together (vaulting, sessions, policy, analytics, identity security) and extending PAM into ITDR and ISPM. |
| **DevOps Secrets Vault** | Delinea's high-speed, API-driven secrets-management product for machines and automation (apps, CI/CD, containers), enabling runtime retrieval and short-lived dynamic secrets instead of hardcoded credentials. |
| **Engineer** | The hands-on Delinea tier — validates the ability to install, configure, and manage to best practice through lab challenges assessed by a live Delinea Security Academy expert, including break-fix troubleshooting. |
| **ISPM** | Identity Security Posture Management — continuously finding and reducing identity risk (over-privileged accounts, unmanaged service accounts, excessive standing access); the identity-security parallel to cloud posture management. |
| **ITDR** | Identity Threat Detection and Response — detecting and responding to identity-based attacks (credential theft, privilege escalation, suspicious authentication) across the identity fabric; the identity counterpart to endpoint detection. |
| **PEDM** | Privilege Elevation and Delegation Management — granting specific privileged commands (e.g., via Centrify's audited `dzdo`) instead of blanket root/sudo, with every command attributable and logged; least privilege on servers. |
| **Privilege Manager** | Delinea's endpoint privilege management product (Thycotic heritage) — removes standing local admin rights and enforces application control (allow/elevate/deny), elevating the application rather than the user. |
| **Privileged Behavior Analytics (PBA)** | Delinea's behavioral analytics on privileged activity — detecting anomalies (unusual time, location, or access pattern) that signal a compromised or misused privileged account. |
| **Rule-based passwords** | Secret Server's automatic generation of strong, policy-compliant passwords (length, complexity, character sets), so rotated credentials always meet security requirements. |
| **Secret policy** | A Secret Server policy governing how a class of secrets behaves — rotation frequency, access, check-out requirement, session recording — applied consistently rather than configured per secret. |
| **Secret Server** | Delinea's flagship privileged credential vault (Thycotic heritage) — credential vaulting, secret policies, rule-based passwords, automatic rotation, check-out, and session monitoring/recording with keystroke logging. |
| **Server PAM** | Delinea's server privilege product (Centrify heritage) — granular privilege elevation (PEDM) on Linux/Unix/Windows servers, Active Directory bridging, and MFA at the server; identity-centric least privilege on infrastructure. |
| **Short-lived (dynamic) secret** | A secret issued just-in-time by DevOps Secrets Vault that is valid only briefly (or for a single use) and then expires, so a leaked machine credential is worthless minutes later. |
| **Thycotic / Centrify** | The two PAM vendors merged in 2021 to form Delinea — Thycotic contributed Secret Server and Privilege Manager (secrets and endpoints), Centrify contributed Server PAM and AD bridging (servers and identity). |
