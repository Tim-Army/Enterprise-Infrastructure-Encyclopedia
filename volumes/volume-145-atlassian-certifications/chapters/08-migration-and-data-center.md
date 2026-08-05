# Chapter 08: Migration and Data Center

## Learning Objectives

- Explain the Data Center deployment and where it still fits after Server's end of life.
- Plan a Data-Center-to-Cloud migration — the skill Atlassian's catalog now emphasizes.
- Understand what migrates cleanly and what does not.
- Recognize migration as a project with the same discipline as an SAP conversion.

*Cert relevance: **Jira Administration for Data Center** and the **Confluence Administration for Data Center** certifications, plus the Data-Center-to-Cloud migration learning path prominent in Atlassian's catalog.*

## Data Center after Server's end of life

With **Server end-of-support in February 2024** (Chapter 01), Atlassian's self-hosted story is now **Data Center only** — the clustered, self-managed deployment for organizations that cannot or will not move to Cloud:

| Reason to stay on Data Center | Why |
|:---|:---|
| **Data residency / sovereignty** | Regulatory requirement to control where data physically lives |
| **Deep customization** | Apps, integrations, or configurations Cloud does not support |
| **Existing investment** | Large, complex instances where migration is a major project |
| **Network isolation** | Air-gapped or restricted environments |

Data Center is the enterprise self-hosted path, and its administration adds **clustering, load balancing, and infrastructure** to the Jira/Confluence admin skills from earlier chapters — which is why the Data Center certifications are distinct exams testing that infrastructure surface.

But the direction of travel is unmistakable, and the certifications reflect it: **Cloud is where Atlassian invests, and Data-Center-to-Cloud migration is a first-class skill area.**

## Migration is a project

Moving from Data Center to Cloud is not a copy — it is a **migration project**, with the same discipline as an [SAP ECC→S/4HANA conversion (CXLIV)](../../volume-144-sap-certifications/chapters/02-s4hana-and-the-rise-context.md): the target is not identical to the source, so things must be mapped, transformed, and sometimes rebuilt.

What migrates and what does not:

| Migrates cleanly | Needs work | May not migrate |
|:---|:---|:---|
| Projects, issues, history | User accounts (identity remapping) | Some Data Center-only apps |
| Spaces, pages, attachments | Permission schemes (model differs) | Deep customizations Cloud disallows |
| Workflows (mostly) | Marketplace apps (Cloud versions differ) | Custom code/scripts against DC internals |

The **app gap** is the one that surprises people: a Marketplace app on Data Center may have a different Cloud version, a different feature set, or no Cloud version at all — and a workflow depending on a DC-only app cannot simply move. This is exactly the [clean-core lesson](../../volume-144-sap-certifications/chapters/04-btp-and-abap-cloud-development.md) from SAP: the more you customized against the platform's internals, the harder the migration, because the customizations do not port.

## The migration approach

Atlassian's tooling (the Cloud Migration Assistant) handles the bulk mechanically, but the *planning* is the skill:

1. **Assess.** Inventory projects, apps, customizations, and integrations; identify what will not migrate cleanly (the app gap especially).
2. **Clean up first.** Migrate less: archive dead projects, remove unused apps, consolidate schemes (Chapter 02). A migration is the best possible forcing function for the tidying you have been deferring — you do not want to carry sprawl to the new platform.
3. **Pilot.** Migrate a subset, verify, learn.
4. **Migrate in waves.** Not everything at once; by team or product, with validation between waves.
5. **Validate and cut over.** Confirm data integrity, remap what needs it, switch users.

The recurring discipline: **clean up before you migrate**, because migrating sprawl just moves the problem, and **stage it in waves**, because a big-bang migration of a large instance is how you discover the app gap in production.

## Hands-On Lab

Python models migration planning. **Cost:** none.

### Lab 8.1 — Assess what will not migrate cleanly

**Objective:** Inventory the migration risks before starting.

```bash
python3 - <<'EOF'
INVENTORY = {
  "projects":              {"count": 340, "migrates": "clean",   "note": "projects/issues/history port"},
  "confluence spaces":     {"count": 45,  "migrates": "clean",   "note": "pages/attachments port"},
  "permission schemes":    {"count": 120, "migrates": "remap",   "note": "Cloud permission model differs"},
  "marketplace apps":      {"count": 22,  "migrates": "gap",     "note": "some have no Cloud version"},
  "custom scripts (DC)":   {"count": 15,  "migrates": "rebuild", "note": "written against DC internals"},
  "integrations":          {"count": 8,   "migrates": "remap",   "note": "re-point to Cloud APIs"},
}
print(f"{'item':22}{'count':>7}{'migration':>10}   risk")
clean = remap = gap = rebuild = 0
for item, d in INVENTORY.items():
    m = d["migrates"]
    risk = {"clean":"low", "remap":"MEDIUM — manual work", "gap":"HIGH — may not exist on Cloud",
            "rebuild":"HIGH — must rebuild"}[m]
    exec(f"{m} = {m} + d['count']" if m in ('clean','remap','gap','rebuild') else "None")
    print(f"{item:22}{d['count']:>7}{m:>10}   {risk}")
print(f"\nThe HIGH-risk items are the migration's real work, not the projects:")
print("  22 marketplace apps: check EACH for a Cloud version. Any DC-only app that a")
print("     workflow depends on blocks that workflow's migration until you find a")
print("     replacement or drop the dependency.")
print("  15 custom scripts against DC internals: these do NOT port — Cloud has no")
print("     equivalent internal access (same as SAP's ABAP-Cloud restriction). They")
print("     must be rebuilt as Cloud automation, Forge apps, or dropped.")
print("\nThe projects/issues/pages migrate mechanically. The APPS, SCRIPTS, and")
print("PERMISSION REMAPPING are where migrations slip — and where an honest ASSESS")
print("phase saves you from discovering them at cutover.")
print("\nAssess reveals the true scope: '340 projects' sounds like the job; the 37")
print("apps+scripts that don't port ARE the job.")
EOF
```

**Expected result:** The bulk (projects, pages) migrating clean while apps, custom scripts, and permission schemes carry the real risk. The assess-phase lesson is that the visible scale (340 projects) is not the work — the app gap and non-porting custom scripts are, and finding them early prevents cutover surprises.

**Negative test:** Scoping the migration by project count. The 340 projects migrate mechanically; the 22 apps and 15 DC-internal scripts are the effort, and skipping assessment discovers them in production.

**Cleanup:** None.

### Lab 8.2 — Clean up before you migrate

**Objective:** Quantify migrating less.

```bash
python3 - <<'EOF'
BEFORE = {"projects": 340, "active_projects": 210, "apps": 22, "used_apps": 12,
          "schemes": 180, "needed_schemes": 25}
print("The instance as-is vs after pre-migration cleanup:\n")
print(f"{'item':18}{'as-is':>8}{'after cleanup':>15}{'reduction':>11}")
for item, key_active in [("projects","active_projects"),("apps","used_apps"),("schemes","needed_schemes")]:
    before = BEFORE[item]; after = BEFORE[key_active]
    print(f"{item:18}{before:>8}{after:>15}{f'{(1-after/before)*100:.0f}%':>11}")
print("\nCleaning up FIRST — archiving dead projects, removing unused apps,")
print("consolidating schemes — shrinks the migration by a lot:")
print(f"  {BEFORE['projects']-BEFORE['active_projects']} dead projects: ARCHIVE them, don't migrate them.")
print(f"  {BEFORE['apps']-BEFORE['used_apps']} unused apps: REMOVE before migrating — every one you")
print(f"     carry is a Cloud-compatibility check you did not need to do.")
print(f"  {BEFORE['schemes']-BEFORE['needed_schemes']} redundant schemes (Chapter 02's sprawl): CONSOLIDATE, so you")
print(f"     migrate 25 well-designed schemes instead of 180 tangled ones.")
print("\nThe principle: a migration is the best FORCING FUNCTION you will ever get")
print("for the cleanup you have been deferring. Migrating sprawl just relocates the")
print("mess to a fresh platform — and now the fresh platform is already messy on")
print("day one. Clean up, THEN migrate; the target deserves better than the debt.")
print("\n(This is why Atlassian's migration learning paths spend so long on")
print("preparation — the mechanical move is easy; the cleanup is the value.)")
EOF
```

**Expected result:** Substantial reductions in projects, apps, and schemes from pre-migration cleanup. The forcing-function framing is the discipline — a migration is the ideal opportunity to shed the sprawl covered in Chapter 02, and migrating it instead just moves the mess to a fresh platform.

**Negative test:** Migrating the instance as-is to "sort it out later." The dead projects, unused apps, and sprawled schemes land on the new platform, which is now messy from day one and harder to clean in Cloud.

**Cleanup:** None.

### Lab 8.3 — Wave migration versus big bang

**Objective:** Model why migrations stage in waves.

```bash
python3 - <<'EOF'
TEAMS = 12
ISSUES_PER_TEAM = 8000
print("BIG BANG: migrate all 12 teams / 96,000 issues in one weekend cutover:")
print("   - if the app gap or a permission-remap bug surfaces, it hits ALL teams")
print("   - rollback means reverting EVERYONE; the whole company is blocked Monday")
print("   - you learn about problems at maximum blast radius\n")
print("WAVE MIGRATION: 3 waves of 4 teams, one week apart:")
waves = [("wave 1 (pilot: 2 low-risk teams)", 2), ("wave 2 (4 teams)", 4),
         ("wave 3 (6 teams incl. complex)", 6)]
migrated = 0
for name, n in waves:
    migrated += n
    print(f"   {name:34} -> {migrated}/{TEAMS} teams migrated, VALIDATE before next wave")
print("\nWhat waves buy you:")
print("  - the PILOT (wave 1) surfaces the app gap and remap issues on 2 low-risk")
print("    teams, where a problem is recoverable — not on all 12 at once")
print("  - each wave's lessons improve the next (a broken app found in wave 1 is")
print("    fixed before waves 2-3 hit it)")
print("  - rollback, if needed, is scoped to one wave's teams, not the company")
print("  - the complex teams go LAST, after the process is proven on simpler ones")
print("\nSame discipline as every staged rollout on this shelf (Akamai staging,")
print("Cloudflare log-then-enforce): prove it on a small blast radius, learn, widen.")
print("A big-bang migration of a large instance is how you discover the app gap with")
print("the whole company watching on Monday morning.")
EOF
```

**Expected result:** Wave migration surfacing problems on a low-risk pilot and scoping rollback per-wave, versus big-bang's company-wide blast radius. The staged-rollout discipline is the transferable lesson — the same prove-on-a-small-radius-then-widen pattern as Akamai staging and Cloudflare's enforcement ladder, applied to migration.

**Negative test:** A single big-bang weekend cutover for a 12-team instance. The app gap surfaces Monday morning for everyone at once, and rollback blocks the entire company.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Data Center placed as the enterprise self-hosted path after Server's Feb 2024 end of life.
- [ ] Migration understood as a project, with the app gap and DC-internal scripts as the real risk.
- [ ] Pre-migration cleanup treated as the forcing function to shed sprawl, not migrate it.
- [ ] Migration staged in waves, piloting on low-risk teams before the complex ones.
