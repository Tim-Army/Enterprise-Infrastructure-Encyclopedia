# Chapter 07: System Administrator — Deploying and Governing

## Learning Objectives

- Explain the System Administrator role — deploying and governing Qlik.
- Describe the Qlik Management Console (QMC).
- Understand streams, spaces, and security rules.
- Recognize reload tasks and operational governance.

*Cert relevance: the Qlik Sense System Administrator (QSSA) certification validates deployment and governance.*

## The System Administrator role

The **Qlik Sense System Administrator** deploys, manages, and **governs** the Qlik environment — the person who keeps Qlik running securely and reliably for everyone else. Where the [Data Architect (Ch 4)](04-data-architect.md) builds data models and the [Business Analyst (Ch 5)](05-business-analyst.md) builds apps, the System Administrator provides the **governed platform** they work on: managing access, organizing content, scheduling data refreshes, and securing the whole deployment. The QSSA certification validates this operational skill. The lab models the role.

## The Qlik Management Console (QMC)

For **client-managed** Qlik Sense, the administrator's primary tool is the **Qlik Management Console (QMC)** — the central console for **administering** the environment. Through the QMC, the admin:

- **Manages content** — apps, streams, and their organization.
- **Controls access** — users, security rules, and what each can see and do.
- **Schedules reloads** — tasks that refresh app data on a schedule.
- **Monitors** — the health and usage of the environment.

(In **Qlik Cloud**, the equivalent governance is done through the cloud management/administration interface and **spaces**.) The QMC is the operational cockpit of a client-managed deployment, and knowing it is core to the QSSA. The lab models the QMC.

## Streams, spaces, and security rules

Qlik organizes and secures content through:

- **Streams** (client-managed) / **spaces** (Qlik Cloud) — containers that **group apps** and control **who can access them**. An app is published to a stream/space, and users' access to that stream/space determines what they see. This is how content is organized and access is scoped.
- **Security rules** — the QMC's **rule-based access control**: attribute-based rules that define who can read, publish, or administer which resources. Security rules are powerful and central — they express the deployment's whole access policy.

Getting streams/spaces and security rules right is what makes Qlik **governed** — the right people see the right apps, and nothing more. The lab models access control.

## Reload tasks and operational governance

Apps need **fresh data**, so the administrator schedules **reload tasks** — jobs that re-run an app's [load script (Ch 4)](04-data-architect.md) to refresh its data, on a schedule or triggered by other tasks (task chains). Managing reloads (timing, dependencies, failures) keeps the analytics current without manual intervention. Combined with access governance and monitoring, reload management is the **operational** heart of running Qlik at scale — the platform stays current, secure, and reliable. The lab synthesizes.

## Hands-On Lab

Python models governance — streams, security rules, and reloads. **Cost:** none.

### Lab 7.1 — Streams, security rules, and scheduled reloads

**Objective:** See governed access and operational data refresh.

```bash
python3 - <<'EOF'
# Qlik governance: streams/spaces group apps; security rules control access; reload tasks refresh data
STREAMS = {
  "Finance":   {"apps": ["Revenue", "Budget"],   "access": {"role:finance", "role:exec"}},
  "Sales":     {"apps": ["Pipeline", "Quota"],    "access": {"role:sales", "role:exec"}},
  "Everyone":  {"apps": ["Company KPIs"],          "access": {"role:employee"}},
}
def can_see(stream, user_roles):
    return bool(STREAMS[stream]["access"] & user_roles)

print("STREAMS/SPACES group apps + control access (security rules):\n")
for s, d in STREAMS.items():
    print(f"   [{s}] apps={d['apps']}  access={d['access']}")
print("\nSecurity-rule checks (rule-based access control):")
for user, roles in [("alice (finance)", {"role:finance","role:employee"}),
                    ("bob (sales)", {"role:sales","role:employee"})]:
    visible = [s for s in STREAMS if can_see(s, roles)]
    print(f"   {user:18} can see streams: {visible}")
print("   -> alice sees Finance + Everyone (NOT Sales); bob sees Sales + Everyone (NOT Finance)\n")
# reload tasks keep data fresh
TASKS = [
    {"app": "Revenue", "schedule": "daily 02:00", "on_success_trigger": "Budget"},
    {"app": "Pipeline","schedule": "hourly",       "on_success_trigger": None},
]
print("RELOAD TASKS (scheduled data refresh — via the QMC):")
for t in TASKS:
    chain = f" -> then reload {t['on_success_trigger']}" if t["on_success_trigger"] else ""
    print(f"   reload '{t['app']}' {t['schedule']}{chain}")
print("\nThe SYSTEM ADMINISTRATOR (QSSA) provides the GOVERNED platform: the QMC (client-managed;")
print("or Cloud admin/spaces) manages content, access, reloads, monitoring. STREAMS/SPACES group")
print("apps + scope access; SECURITY RULES (attribute-based) decide who reads/publishes/admins")
print("what — alice sees Finance not Sales. RELOAD TASKS (scheduled, chainable) keep data fresh.")
print("Right people see the right apps, data stays current — Qlik GOVERNED at scale.")
EOF
```

**Expected result:** Streams grouping apps with role-based access, security rules where alice (finance) sees Finance and Everyone but not Sales while bob (sales) sees the reverse, and scheduled/chained reload tasks refreshing data. The System Administrator lesson is that the role provides a governed platform via the QMC (or Qlik Cloud admin) — streams/spaces scope access, security rules define who can do what, and reload tasks keep data current — so the right people see the right apps and the analytics stay fresh.

**Negative test:** Publishing all apps to one open stream with no security rules or scheduled reloads. Everyone sees everything and data goes stale; streams/spaces plus security rules scope access and reload tasks keep it current — the governance the System Administrator provides.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The System Administrator role understood — deploying and governing the Qlik platform.
- [ ] The Qlik Management Console (QMC) understood — the console for administering a client-managed deployment.
- [ ] Streams/spaces and security rules understood — grouping apps and controlling access.
- [ ] Reload tasks and operational governance understood — keeping data current, secure, and reliable.
