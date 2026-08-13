# Chapter 05: Zero Trust Access

## Learning Objectives

- Explain ZTNA and how Cloudflare Access replaces VPN-style network access.
- Write Access policies over identity, device, and context signals.
- Use service tokens for non-human access without weakening the human path.
- Compare blast radii: what a stolen credential buys under each model.

*Exam relevance: the first half of Zero Trust Associate territory. **Defensive** throughout. The zero-trust discipline itself is covered vendor-neutrally in [Volume LXXXVII](../../volume-087-microsegmentation-options/README.md) and product-by-product across the microsegmentation lab volumes; this chapter is Cloudflare's implementation of it.*

## The model change

A VPN answers one question — *are you allowed onto the network?* — once, at connect time. Everything reachable from that network is then reachable from you. **Access** answers a different question — *may this identity, on this device, reach this application, right now?* — and answers it **per application, per request**.

| | **VPN** | **Access (ZTNA)** |
|:---|:---|:---|
| Decision | Once, at connect | Per application, continuously |
| Grants | A network position | An application session |
| A stolen credential buys | Everything routable from the VPN subnet | The applications that identity's policies allow |
| The application's exposure | Open to the internal network | Not directly reachable at all — fronted by the edge |
| Visibility | Flow logs, if collected | Per-application, per-identity access logs by construction |

The blast-radius row is the argument, and Lab 5.2 does its arithmetic. The visibility row matters almost as much in practice: "who accessed the finance app last month" is a *query* under Access and an archaeology project under VPN flow logs.

## Policies

An Access policy binds an application to requirements over signals:

- **Identity** — the user, their groups, from one or more configured identity providers.
- **Device posture** — WARP-enrolled, managed, disk-encrypted, running required software (via the client, Chapter 06).
- **Context** — country, network, time, multifactor method used.

Policy design inherits every lesson this shelf has taught about rules: **specific before broad, deny stated explicitly, and every exception named and owned.** An Access policy of "everyone in the company may reach the admin panel" is a VPN with better logging — the value arrives when policy granularity matches application sensitivity.

## Service tokens

Automation cannot complete an identity-provider login. **Service tokens** — a client ID and secret issued per service — let non-human clients authenticate to Access-protected applications without carving humans-style exceptions.

The disciplines are familiar from [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md) territory: one token per consumer (never shared), scoped to the applications that consumer needs, rotated on schedule, and revoked when the consumer retires. A service token in a repository is a credential leak like any other. What tokens prevent is the worse pattern they replace: "just IP-allowlist the office and let the script skip auth" — an unauthenticated hole punched for one script's convenience.

## Hands-On Lab

Python models access control. **Cost:** none — and Access's free tier covers 50 users, so the real thing is also free at lab scale.

### Lab 5.1 — Policy evaluation

**Objective:** Trace who reaches what, and why.

```bash
python3 - <<'EOF'
APPS = {
  "wiki":      [{"require": {"group": "employees"}}],
  "finance":   [{"require": {"group": "finance-team", "posture": "managed", "mfa": "hardware-key"}}],
  "admin":     [{"require": {"group": "platform-admins", "posture": "managed", "country": "trusted"}}],
  "grafana":   [{"require": {"group": "engineering", "posture": "managed"}}],
}
USERS = [
  ("ana (finance, managed laptop, hardware key)",
   {"group": {"employees","finance-team"}, "posture": "managed", "mfa": "hardware-key", "country": "trusted"}),
  ("ben (engineering, personal tablet)",
   {"group": {"employees","engineering"}, "posture": "unmanaged", "mfa": "totp", "country": "trusted"}),
  ("attacker with ana's PASSWORD only",
   {"group": {"employees","finance-team"}, "posture": "unmanaged", "mfa": "none", "country": "other"}),
  ("cal (platform-admin, managed, traveling)",
   {"group": {"employees","platform-admins"}, "posture": "managed", "mfa": "hardware-key", "country": "other"}),
]
def allowed(app, u):
    for pol in APPS[app]:
        r = pol["require"]
        ok = True
        if "group" in r and r["group"] not in u["group"]: ok = False
        if "posture" in r and u["posture"] != r["posture"]: ok = False
        if "mfa" in r and u["mfa"] != r["mfa"]: ok = False
        if "country" in r and u["country"] != r["country"]: ok = False
        if ok: return True
    return False

print(f"{'user':46}" + "".join(f"{a:>9}" for a in APPS))
for name, u in USERS:
    row = "".join(f"{'ALLOW' if allowed(a, u) else '--':>9}" for a in APPS)
    print(f"{name:46}{row}")

print("\nRead the attacker's row: ana's stolen password buys NOTHING. The finance")
print("policy also demands managed posture and a hardware key — signals a password")
print("thief does not have. Under a VPN, that same password was the whole game.")
print("\nRead cal's row: an admin, correctly equipped, denied ONE app while traveling")
print("because the admin policy pins country. That is policy working — and it is")
print("also a support ticket, which is why context requirements belong on the")
print("highest-consequence apps rather than everywhere.")
EOF
```

**Expected result:** The password-only attacker reaches nothing despite holding valid group membership, and the traveling admin loses exactly one application to the country pin. Both rows teach: layered signals make single-credential theft insufficient, and every added signal is also a legitimate-user denial waiting for the right circumstances — spend context requirements where consequence justifies the tickets.

**Negative test:** Requiring hardware keys and managed posture on the lunch-menu wiki. Security indistinguishable from obstruction trains users to route around the system that is supposed to protect the finance app.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Blast radius: VPN versus per-app access

**Objective:** Compute what one stolen credential reaches.

```bash
python3 - <<'EOF'
NETWORK = {          # what is routable once you are "on the network"
  "wiki": 1, "finance": 1, "admin": 1, "grafana": 1, "jenkins": 1,
  "postgres-prod": 1, "redis-prod": 1, "k8s-api": 1, "nas": 1,
  "printer-vlan": 1, "legacy-erp": 1, "dev-jumphost": 1,
}
ACCESS_POLICIES = {  # apps published through Access, per-identity
  "sales-user":    ["wiki"],
  "engineer":      ["wiki", "grafana", "jenkins"],
  "finance-user":  ["wiki", "finance"],
  "platform-admin":["wiki", "grafana", "jenkins", "admin", "k8s-api"],
}
print("Stolen credential: a SALES user's password + a session on their unmanaged laptop\n")
print(f"   VPN model    : attacker lands on the network -> {len(NETWORK)} reachable systems,")
print("                  including postgres-prod and k8s-api, none of which a sales")
print("                  role ever needed. Lateral movement is now a scanning exercise.")
n = len(ACCESS_POLICIES["sales-user"])
print(f"   Access model : the identity's policies allow {n} application: wiki.")
print("                  postgres-prod is not merely denied — it is NOT PUBLISHED;")
print("                  there is no route to attempt.\n")
print(f"{'stolen identity':18}{'VPN reach':>11}{'Access reach':>14}")
for role, apps in ACCESS_POLICIES.items():
    print(f"{role:18}{len(NETWORK):>11}{len(apps):>14}")
print("\nTwo different claims hide in that table:")
print("  SMALLER  — least privilege shrinks each identity's reach (rows differ)")
print("  BOUNDED  — even the admin's worst case is the apps published to admins,")
print("             not 'everything routable'. The database was never on the menu.")
print("\nThe honest caveats: Access covers what you PUBLISH through it. The legacy")
print("ERP still reached over VPN is the perimeter you have not retired — hybrid")
print("estates hold both risk profiles at once, and the migration order should be")
print("highest-consequence apps first, not easiest first.")
EOF
```

**Expected result:** A sales credential reaches 12 systems under VPN and one under Access, with even the admin's worst case bounded to five published applications. The two-claims framing is the analytical content — least privilege shrinks reach per identity, while publication as the only path bounds reach for *every* identity — and the caveat names the real-world condition: hybrid estates carry both models' risk until migration completes.

**Negative test:** Declaring zero trust achieved because Access fronts six apps while the VPN still routes to everything. The attacker reads the same architecture diagram you do and takes the old road.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Service tokens without human-path holes

**Objective:** Authenticate automation properly.

```bash
python3 - <<'EOF'
from datetime import date
TOKENS = [
  # name,                  apps,                  created,      rotated,      owner
  ("ci-deploy",           ["jenkins"],           "2026-01-10", "2026-07-10", "platform"),
  ("uptime-checker",      ["wiki","grafana"],    "2025-03-02", "2025-03-02", "sre"),
  ("etl-finance",         ["finance"],           "2026-02-20", "2026-06-20", "data-eng"),
  ("old-slack-bot",       ["wiki","admin"],      "2024-08-15", "2024-08-15", "(nobody current)"),
]
today = date(2026, 8, 4)
ROTATE_DAYS = 180
print(f"{'token':16}{'apps':24}{'age(d)':>7}{'since rotate':>13}   finding")
for name, apps, created, rotated, owner in TOKENS:
    age = (today - date.fromisoformat(created)).days
    rot = (today - date.fromisoformat(rotated)).days
    finds = []
    if rot > ROTATE_DAYS: finds.append("ROTATION OVERDUE")
    if owner.startswith("("): finds.append("NO OWNER — revoke or adopt")
    if "admin" in apps: finds.append("scope check: why does a bot reach 'admin'?")
    print(f"{name:16}{','.join(apps):24}{age:>7}{rot:>13}   {'; '.join(finds) or 'healthy'}")

print("\nThe audit questions for every token, quarterly:")
print("   WHO owns it (a team, not a departed person)")
print("   WHAT it reaches (minimum scope; 'admin' in a bot's list is a finding)")
print("   WHEN it last rotated (calendar-enforced, not memory-enforced)")
print("\nold-slack-bot fails all three at once — unowned for two years, unrotated,")
print("scoped to an admin surface. Tokens rot exactly like Vol CXL's manual tags")
print("and Chapter 02's forgotten DNS records: silently, and in proportion to how")
print("long ago someone stopped being responsible for them.")
EOF
```

**Expected result:** Two tokens healthy, one rotation-overdue, and one failing every audit dimension simultaneously. The pattern named at the end is this volume's connective tissue — unowned artifacts (tokens, tags, DNS records, shadow APIs) decay silently, and the countermeasure is always the same: an owner, a scope, and a calendar.

**Negative test:** Solving automation access by IP-allowlisting the CI runner around Access entirely. That is an unauthenticated hole with a comment saying it is temporary, and it will outlive everyone who remembers why.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Access understood as per-application, per-request decisions over layered signals.
- [ ] Policies granular in proportion to application sensitivity, with exceptions owned.
- [ ] Blast radius bounded by publication, with hybrid-estate caveats stated.
- [ ] Service tokens scoped, owned, rotated — and never replaced by allowlist holes.
