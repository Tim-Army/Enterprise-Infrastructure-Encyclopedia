# Volume CXLVI — Glossary

| Term | Definition |
|:---|:---|
| **ABM / ASM** | Apple Business Manager / Apple School Manager — the Apple portals that link purchased devices and apps to your MDM. The supply chain for zero-touch enrollment (ADE) *and* for VPP app licensing. |
| **ADE** | Automated Device Enrollment — zero-touch enrollment where a device whose serial is assigned to your organization in ABM enrolls into Jamf automatically on first power-on, configured before the user logs in. |
| **CIS macOS Benchmark** | The Center for Internet Security's consensus set of macOS hardening settings (FileVault on, firewall on, secure screen-lock, guest off, and more) — the baseline Jamf enforces with profiles and measures continuously. |
| **Configuration profile** | A declarative bundle of Apple settings (Wi-Fi, VPN, restrictions, FileVault, passcode) that the device applies and *maintains* — reverting when the profile is removed. Profiles for settings, policies for actions. |
| **Cooperative, not coercive** | The defining property of Apple management: Jamf implements Apple's MDM framework and can only do what Apple permits — you send Apple-defined commands and profiles, not arbitrary Group-Policy-style force. |
| **DDM** | Declarative Device Management — Apple's modern model where the server declares a desired state and the *device itself* works to reach and maintain it, reporting changes without being polled. The Kubernetes/Terraform desired-state model, applied to Apple. |
| **Endpoint Security framework** | Apple's supported system-extension API for security software to observe system events, replacing the deprecated kernel-extension (kext) approach. Jamf Protect is built on it — deep visibility that endures across macOS updates. |
| **Extension attribute** | A custom inventory field populated by a script (agent status, FileVault state, a file's presence). Lets you build Smart Groups and scope on facts beyond Apple/Jamf's built-in inventory. |
| **Jamf Connect** | The identity product: brings cloud IdP (Okta/Entra/Google) login to the Mac login window and synchronizes the local macOS password with the cloud one — closing password drift and the local-account offboarding gap. |
| **Jamf Pro** | The flagship device-management product — enrollment, Smart Groups, configuration profiles, policies, patch management, Self Service — implementing Apple's MDM framework. Certification ladder 100/200/300/400. |
| **Jamf Protect** | Apple-native endpoint security — telemetry, threat prevention, and continuous compliance monitoring, built on Apple's Endpoint Security framework. A distinct product with its own ladder (170/270/370). Defensive. |
| **Jamf School** | Education-tailored management (shared iPad carts, classroom workflows, student/teacher roles) on the same Apple foundation — its own ladder (140/240). A different sector, not a different difficulty. |
| **Policy** | An imperative action Jamf runs at a trigger (enrollment, check-in, schedule) — install a package, run a script. Done once; not maintained and not reverted by removing the policy. |
| **Self Service** | The app-store-like catalog on managed devices where users *choose* to install optional software and run workflows on demand — the pull half of the push-versus-offer decision. |
| **Smart Group** | A dynamic set of devices defined by inventory criteria, with automatic, live membership — devices join and leave as they match. The scaling discipline over hand-maintained static groups; everything scopes through it. |
| **Scope** | How a policy or profile targets devices — usually Smart Groups, refined by exclusions and limitations. A live query: destructive actions must be pre-flighted against current membership before deploying. |
| **Supervision** | The elevated management state (typically ADE-enrolled, org-owned hardware) that unlocks the fuller MDM capability set — restrictions, silent install, stronger update enforcement — that user-enrolled BYOD does not permit. |
| **VPP** | Volume Purchase Program — buying and assigning App Store apps through ABM so Jamf installs and manages them centrally, without an Apple ID on the device, as licensed, updatable, removable managed apps. |
| **Zero-touch** | Deployment where a device ships from Apple/reseller straight to the user and self-enrolls on first boot via ADE — no IT depot, no imaging. Depends on the serial being in ABM. |
