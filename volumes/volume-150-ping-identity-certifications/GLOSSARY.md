# Volume CL — Glossary

| Term | Definition |
|:---|:---|
| **Access certification** | A periodic governance review where managers re-attest that their reports still need the access they hold, revoking what is no longer justified — the control against privilege creep. |
| **Adaptive authentication** | Risk-based authentication that adjusts the challenge to signals (device, location, velocity, anomalies) — stepping up MFA for risky logins while letting low-risk logins through with less friction. PingOne Protect scores the risk. |
| **Assertion / token** | The digitally-signed statement an identity provider issues to vouch for an authenticated user — a SAML assertion or an OIDC ID token. The service provider trusts the signature, never the password. |
| **Authentication (AuthN)** | Proving who you are (password, MFA, biometric). Distinct from and prior to authorization. |
| **Authorization (AuthZ)** | Determining what an authenticated identity may do (roles, policies, scopes). A separate gate — a known identity can still be denied. |
| **CIAM** | Customer Identity and Access Management — identity for customers (unbounded, self-registering, experience-sensitive), as opposed to workforce identity. |
| **Federation** | Extending SSO across organizational/domain boundaries so an identity from one domain's IdP is trusted by an app in another, via SAML/OIDC. PingFederate's core function. |
| **IDaaS** | Identity-as-a-Service — identity (SSO, MFA, directory) delivered from the cloud rather than self-hosted. PingOne is Ping's IDaaS. |
| **IdP / SP** | Identity Provider (authenticates the user and issues assertions) and Service Provider / relying party (trusts the IdP and grants access). |
| **OAuth 2.0** | An authorization framework issuing scoped access tokens that let a client call an API on a user's behalf. Answers "what can this app do?" — not "who is the user?" |
| **OIDC** | OpenID Connect — an authentication layer on top of OAuth 2.0 that adds an ID token stating who the user is. Answers "who logged in?" |
| **PingFederate** | Ping's flagship federation server — SAML, OIDC, and OAuth SSO, bridging enterprise and modern standards. The most transferable Ping skill. |
| **PingOne DaVinci** | Ping's no-code identity orchestration — designing identity journeys as visual, branching flows glued across a multi-vendor estate by connectors. |
| **PingOne Protect** | Ping's threat/fraud protection — scoring each authentication for risk from device, location, velocity, and behavioral signals, feeding adaptive authentication. |
| **Passwordless** | Authentication without a password, using FIDO2/WebAuthn keys or platform authenticators — more secure (phishing-resistant, nothing to steal) and more usable. |
| **Privilege creep** | The accumulation of access as people change roles and keep old permissions, leaving users with far more access than they need — the standing risk access certification exists to catch. |
| **Product-specific program** | Ping's certification model — each exam certifies you on one product (PingFederate, PingAccess, PingOne, PingAM…) at Professional/Advanced/Expert level, reflecting the broad merged portfolio. |
| **Identity governance** | The discipline of what a user *should* access (versus access management's *can*) — access certification, joiner-mover-leaver lifecycle, and segregation of duties. PingOne Identity Governance. |
