# Chapter 04: Privilege Manager — Endpoint Privilege Management

## Learning Objectives

- Explain Privilege Manager as Delinea's endpoint privilege management.
- Describe application control — allow, deny, and elevate policies.
- Understand removing local admin rights while preserving productivity.
- Recognize least privilege on the endpoint as attack-surface reduction.

*Cert relevance: Privilege Manager is Delinea's EPM product, covered in the certifications alongside Secret Server.*

## What Privilege Manager is

**Privilege Manager** (Thycotic heritage) is Delinea's **endpoint privilege management (EPM)** product — enforcing **least privilege** on endpoints and servers by **removing standing local administrator rights** and controlling which applications may run and with what privilege. Where [Secret Server (Ch 3)](03-secret-server.md) secures **credentials**, Privilege Manager secures the **endpoint itself** — ensuring users run as standard users and only sanctioned applications get elevation. This is the same EPM discipline the [BeyondTrust volume covers (CLVI, Ch 4)](../../volume-156-beyondtrust-certifications/chapters/04-endpoint-privilege-management.md); Delinea implements it via Privilege Manager. The lab models endpoint least privilege.

## Application control: allow, deny, elevate

Privilege Manager works through **application control policies** that decide, for each application, one of three outcomes:

- **Allow** — known-good applications run normally (as a standard user).
- **Elevate** — approved applications that require admin rights are **elevated automatically** under policy, without making the user an admin.
- **Deny** — unknown or forbidden applications are **blocked** (or handled by a default policy).

The key move is elevating the **application, not the user**: the account stays unprivileged, and elevation is granted per-application by policy. So even if a user is tricked into running malware, it inherits the **standard-user** context — it cannot install drivers, disable defenses, or tamper with the system. The lab models the policy.

## Removing local admin without breaking productivity

The hard part of endpoint least privilege is doing it **without blocking legitimate work**. Users occasionally need to install an approved application or run a tool that needs elevation. Privilege Manager resolves the tension: **remove standing local admin** (so nothing runs privileged by default), but **elevate specific approved actions on demand** — silently for sanctioned software, or with a justification/approval workflow for edge cases. Users keep working; attackers lose the blanket privilege they rely on. Balancing security and productivity is what makes EPM deployable rather than merely theoretical. The lab models the balance.

## Least privilege as attack-surface reduction

Removing local admin is one of the **highest-impact** security controls: standing local admin is what malware needs to install itself, disable security tools, and persist, and it is the privilege attackers escalate to first. Enforcing least privilege on the endpoint **shrinks the attack surface** at the source — a compromised standard user is far less dangerous than a compromised admin. Combined with the vault ([Secret Server](03-secret-server.md)) and server privilege ([Server PAM, Ch 5](05-server-pam.md)), Privilege Manager completes Delinea's least-privilege coverage from endpoint to server. The lab models the impact.

## Hands-On Lab

Python models endpoint application control. **Cost:** none.

### Lab 4.1 — Application control contains malware while preserving work

**Objective:** See allow/deny/elevate keep users productive and unprivileged.

```bash
python3 - <<'EOF'
# Privilege Manager application-control policy: users are STANDARD; apps get allow/elevate/deny
POLICY = {
  "approved-tool.msi":   ("elevate", "sanctioned installer -> auto-elevate (user stays standard)"),
  "chrome.exe":          ("allow",   "known-good -> runs as standard user"),
  "internal-app.exe":    ("allow",   "known-good line-of-business app"),
  "unknown-miner.exe":   ("deny",    "unknown/forbidden -> BLOCKED"),
  "ransomware.tmp":      ("deny",    "unknown -> BLOCKED (default-deny)"),
}
def run(app):
    action, why = POLICY.get(app, ("deny", "unknown -> default-deny"))
    if action == "deny": return f"BLOCKED            ({why})"
    ctx = "ELEVATED (app only)" if action == "elevate" else "standard-user"
    return f"runs as {ctx:18} ({why})"

print("Privilege Manager — endpoint application control (user = STANDARD, no local admin):\n")
for app in POLICY:
    print(f"   {app:20} {run(app)}")
print()
print("The insight (same as all EPM): elevate the APPLICATION, not the USER. Users run as")
print("STANDARD users with NO standing local admin; only sanctioned apps get elevation, per")
print("policy. So work continues (approved installer auto-elevates, LOB apps run) while:")
print("  - malware runs (if at all) as a STANDARD user -> no driver installs, no AV tamper")
print("  - unknown/forbidden apps are DENIED outright")
print("Removing standing local admin is one of the highest-impact controls — it removes the")
print("privilege-escalation step at the source. Privilege Manager (Thycotic heritage) does it")
print("without breaking productivity: security AND usability, the requirement for deployable EPM.")
EOF
```

**Expected result:** A policy where the approved installer auto-elevates, known-good apps run as standard user, and unknown/ransomware apps are denied — users unprivileged throughout. The Privilege Manager lesson is that elevating the application rather than the user keeps accounts unprivileged (so malware can't inherit admin), while approved software still elevates on demand — removing standing local admin at the source without breaking productivity.

**Negative test:** Leaving users with standing local admin to avoid support friction. That makes the whole session privileged, so any malware inherits admin; per-application elevation preserves productivity while removing the blanket privilege attackers exploit.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Privilege Manager understood as Delinea's endpoint privilege management (Thycotic heritage).
- [ ] Application control understood — allow / elevate / deny, elevating the app not the user.
- [ ] Removing local admin without breaking productivity understood — on-demand elevation of approved actions.
- [ ] Endpoint least privilege recognized as high-impact attack-surface reduction.
