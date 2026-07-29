# Volume LXXVII Glossary

Definitions for terms introduced in **Volume LXXVII — CyberArk Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Conjur** — CyberArk's secrets-management platform for DevOps and cloud-native workloads, using policy-as-code to control machine-identity access to secrets.
- **CPM (Central Policy Manager)** — the CyberArk component that automatically verifies, changes/rotates, and reconciles managed passwords per policy.
- **Credential Provider** — an agent on an application host that fetches secrets from the Vault at runtime so they are never stored in the app.
- **Defender** — the CyberArk certification level validating daily maintenance and operation of the PAM solution.
- **Digital Vault** — CyberArk's hardened, encrypted store of privileged credentials and secrets — the core of the platform.
- **Dynamic secret** — a short-lived credential created on demand and revoked after use, limiting the value of a leak.
- **EPM (Endpoint Privilege Manager)** — CyberArk's product that removes standing local-admin rights and grants just-in-time, per-application privilege elevation with application control.
- **Guardian** — CyberArk's highest certification, validating enterprise Identity Security architecture and strategy across the platform.
- **Idira** — the name toward which CyberArk's platform is progressively rebranding under Palo Alto Networks (2026); architecture and credential names are unchanged.
- **JIT (just-in-time) access** — time-boxed privilege granted only when needed and automatically revoked, replacing standing access.
- **PAM (Privileged Access Management)** — the discipline of securing, controlling, and monitoring privileged accounts and secrets.
- **PSM (Privileged Session Manager)** — the component that proxies privileged sessions (credential injected server-side), isolates them from the endpoint, and records them.
- **PTA (Privileged Threat Analytics)** — the component that detects and responds to anomalous privileged activity.
- **PVWA (Password Vault Web Access)** — the CyberArk web interface and REST API for users and administrators.
- **Safe** — a logical container in the Vault with its own permissions, the primary access-control boundary for stored accounts.
- **Secretless** — a pattern where an application connects through a broker that injects the credential, so the app never sees the secret.
- **Secure Cloud Access** — CyberArk's capability that eliminates standing cloud entitlements using just-in-time, zero-standing-privilege access.
- **Sentry** — the CyberArk certification level validating deployment, installation, and configuration of the solution (prerequisite: Defender).
- **Trustee** — the foundational CyberArk certification level covering privileged-access concepts and platform basics.
- **ZSP (zero standing privileges)** — a model where users hold no permanent privileged access, requesting time-boxed elevation only when needed.
