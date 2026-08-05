# Chapter 04: Endpoint Privilege Management

## Learning Objectives

- Explain endpoint privilege management (EPM) and removing local admin rights.
- Describe privilege elevation per-application rather than per-user.
- Understand application control (allow/deny/elevate).
- Recognize EPM across Windows, Mac, and Linux.

*Cert relevance: EPM has three Certified Administrator credentials (Windows, Mac, Linux) — the endpoint least-privilege pillar.*

## Removing local admin rights

**Endpoint Privilege Management (EPM)** enforces **least privilege on endpoints and servers** — workstations, laptops, and servers running Windows, Mac, and Linux. The core move is to **remove local administrator rights** from users. Standing local admin is dangerous: it lets malware install itself, disable security tools, and tamper with the system, and it is the privilege attackers escalate to first. But users still occasionally need elevated actions (install an approved app, change a setting). EPM resolves the tension: **users run as standard users**, and **specific actions are elevated on demand** under policy — the user is never a standing admin, but is never blocked from legitimate work either. The lab models this.

## Privilege elevation per-application

The key idea is elevating **the application, not the user.** Traditional admin rights make the *whole session* privileged; EPM instead grants elevation to **a specific application or task**, based on policy, while the user account stays unprivileged. An approved installer runs elevated; the user's shell does not. This is far safer: even if the user is tricked into running malware, the malware inherits the **standard-user** context, not admin — it cannot install drivers, tamper with protected areas, or disable defenses. Per-application elevation gives users what they need for approved tasks while denying attackers the blanket privilege they seek. The lab models per-app elevation.

## Application control

EPM pairs elevation with **application control** — deciding which applications may run at all, on a policy of **allow / deny / elevate**:

- **Allow** — known-good applications run normally (as standard user).
- **Elevate** — approved applications that need it run with elevated rights, automatically.
- **Deny** — unknown or forbidden applications are blocked.

This combines least privilege with allow-listing: not only is the user not an admin, but only sanctioned software runs, and only sanctioned software gets elevation. It is a strong control against ransomware and unknown malware, which rely on both running freely and escalating. The lab models application control.

## EPM across Windows, Mac, and Linux

EPM spans the estate — and BeyondTrust certifies each platform separately (**EPM for Windows**, **EPM for Mac**, **EPM for Linux**) because the mechanisms differ: Windows (UAC, tokens, installers), macOS (the Apple security model — complementary to the management [Jamf (CXLVI)](../../volume-146-jamf-certifications/README.md) provides), and Linux/Unix (**sudo** replacement — fine-grained, logged privilege elevation instead of broad sudo rights). The principle is uniform; the implementation is platform-specific, which is why there are three credentials. The lab covers the shared model.

## Hands-On Lab

Python models endpoint least privilege. **Cost:** none.

### Lab 4.1 — Per-application elevation beats standing admin

**Objective:** See why elevating the app, not the user, contains malware.

```bash
python3 - <<'EOF'
# EPM policy: users are STANDARD; specific apps are allowed/elevated/denied
POLICY = {
  "approved-installer.msi": "elevate",   # sanctioned, needs admin -> auto-elevate
  "chrome.exe":             "allow",     # known-good, runs as standard user
  "notepad.exe":            "allow",
  "ransomware.exe":         "deny",      # unknown/forbidden -> blocked
  "cryptolocker.tmp":       "deny",
}
def run(app, user_is_admin):
    action = POLICY.get(app, "deny")     # default-deny unknown apps
    if action == "deny":
        return f"BLOCKED (app control: not allowed)"
    ctx = "ELEVATED" if action == "elevate" else ("admin" if user_is_admin else "standard-user")
    return f"runs as {ctx}"

print("SCENARIO A — traditional STANDING LOCAL ADMIN (no EPM):")
for app in ["approved-installer.msi", "ransomware.exe"]:
    # without EPM everything the user runs inherits ADMIN
    ctx = "admin" if app != "___" else ""
    print(f"   {app:24} runs as {ctx}   <-- ransomware ALSO gets admin!")
print("   -> malware inherits ADMIN: installs drivers, disables AV, encrypts everything\n")

print("SCENARIO B — EPM: standard user + per-app policy:")
for app in POLICY:
    print(f"   {app:24} {run(app, user_is_admin=False)}")
print("   -> the approved installer elevates; ransomware is DENIED; everything else runs")
print("      as STANDARD USER with no admin to inherit\n")
print("The insight: elevate the APPLICATION, not the USER. Standing local admin makes the")
print("WHOLE session privileged, so anything the user is tricked into running gets admin.")
print("EPM keeps the user unprivileged and elevates only sanctioned apps -> malware runs")
print("(if at all) as a standard user: no driver installs, no AV tampering, contained.")
print("Least privilege on the endpoint is the escalation step (Ch 2) removed at the source.")
EOF
```

**Expected result:** Under standing local admin, ransomware inherits admin alongside the approved installer; under EPM, the approved installer auto-elevates, ransomware is denied, and everything else runs as a standard user with no admin to inherit. The EPM lesson is that elevating the application rather than the user keeps the user unprivileged, so malware runs (if at all) in a standard-user context — no driver installs, no security-tool tampering — removing the escalation step at its source.

**Negative test:** Giving users standing local admin "so they can install things." That makes the entire session privileged, so any malware they run inherits admin; per-application elevation grants only sanctioned apps elevation while the user stays a standard user.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] EPM understood — least privilege on endpoints by removing standing local admin rights.
- [ ] Per-application elevation understood — elevate the app, not the user, so malware can't inherit admin.
- [ ] Application control understood — allow / deny / elevate policy, least privilege plus allow-listing.
- [ ] EPM's three platforms (Windows, Mac, Linux) recognized, each a separate Certified Administrator credential.
