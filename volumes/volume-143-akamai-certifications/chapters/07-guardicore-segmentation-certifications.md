# Chapter 07: Guardicore Segmentation Certifications

## Learning Objectives

- Navigate Akamai's deepest certification ladder: GCSA, GCSE, their variants, and GCSP.
- Explain the Centra architecture — collectors, the flow map, and label-based policy.
- Design segmentation policy from labels, not IP addresses.
- Connect this certification chapter to the hands-on Guardicore lab already in this encyclopedia.

*Cert relevance: the **Guardicore Certified Segmentation Administrator (GCSA)** and its **Advanced** variant, the **Certified Segmentation Engineer (GCSE)** and its **On-Premise** variant, and the partner-services **Certified Services Provider (GCSP) – Implementation / Support**. This is Akamai's most-developed exam ladder. **Defensive** throughout.*

## The ladder

Guardicore is the segmentation product Akamai acquired, and it carries the certification depth to match — the only Akamai family with a genuine multi-rung, role-split, exam-based ladder:

| Credential | Role | Level | Time band |
|:---|:---|:---|:---|
| **GCSA** | Administrator — day-to-day operation of the Centra platform | Intermediate | Hours |
| **GCSA Advanced** | Hands-on: labeling schemes, policy creation, ransomware mitigation, project planning | Advanced | Days |
| **GCSE** | Engineer — platform administration, CLI, cluster, integration, debugging | Intermediate | Hours |
| **GCSE – On Premise** | Engineer, self-hosted management deployment | Intermediate | Hours |
| **GCSP – Implementation** | Partner: deliver implementations | Advanced | Weeks |
| **GCSP – Support** | Partner: Day-2 operations and support | Advanced | Weeks |

The **administrator/engineer split** is the structural choice to understand: GCSA operates the platform (policy, visibility, day-to-day), GCSE runs the platform (deployment, cluster, integration, troubleshooting). It is the same deploy-versus-operate split [Dynatrace (CXL)](../../volume-140-dynatrace-certifications/README.md) draws between Implementation and Administration Professional — pick by which job is yours.

## Centra architecture

Guardicore's platform is **Centra**, and three pieces carry it:

| Component | Does |
|:---|:---|
| **Agents / collectors** | Sit on workloads, report flows and enforce policy locally |
| **Flow map** | The visualized, historical map of what actually talks to what |
| **Management (Centra)** | Policy authoring, the map, analysis — SaaS or on-premise (the GCSE variant) |

The flow map is the product's center of gravity, and its discipline is the one every segmentation volume on this shelf teaches: **you cannot segment what you have not mapped.** Policy written against assumptions breaks production; policy written against an observed flow map breaks nothing it did not intend to. This is the `monitor-first` rollout that [Volume LXXXVII (Microsegmentation Options)](../../volume-087-microsegmentation-options/README.md) makes its central rubric.

## Label-based policy

Guardicore's defining technique — and the reason it earns a certification ladder rather than a course badge — is **policy by label, not by address.** Workloads carry labels (environment, application, role, tier, compliance scope), applied by rule from orchestrator metadata, naming conventions, or integrations. Policy is written between *labels* ("Production Database may receive from Production App on 5432, nothing else"), and it applies automatically to every workload that carries those labels, including ones created next year.

The payoff is exactly the rule-based-versus-manual-tag lesson from [Volume CXL's tagging chapter](../../volume-140-dynatrace-certifications/chapters/04-entities-topology-and-management-zones.md), now load-bearing for enforcement: address-based policy rots the moment an IP changes; label-based policy holds as the estate churns. The GCSA Advanced credential's named skills — **labeling schema, policy creation, segmentation project planning** — are this discipline, examined.

## This chapter has a lab volume

Uniquely among this volume's chapters, the hands-on build already exists: **[Volume XCV — Akamai Guardicore Build-It-Yourself Lab](../../volume-095-akamai-guardicore-lab/README.md)** stands up a five-VM environment, proves lateral movement on a flat network, and contains it with segmentation — on two tracks (the real Centra console, or the native `nftables`/WFP equivalent). This certification chapter is the *why and what*; that volume is the *how*. A GCSA candidate should read this chapter and then do that lab.

## Hands-On Lab

Python models segmentation policy. **Cost:** none. Defensive throughout. (For the full build, use Volume XCV.)

### Lab 7.1 — Map before you segment

**Objective:** Show what the flow map reveals that assumptions miss.

```bash
python3 - <<'EOF'
ASSUMED = {   # the architecture diagram's flows
  ("web", "app"), ("app", "db"),
}
OBSERVED = {  # what the flow map actually recorded over 2 weeks
  ("web", "app"), ("app", "db"),
  ("app", "legacy-billing"),          # undocumented dependency
  ("backup-agent", "db"),             # backup reaches straight into the DB
  ("web", "db"),                       # a debug path someone left in
  ("monitoring", "web"), ("monitoring", "app"), ("monitoring", "db"),
  ("jump-host", "db"),                 # admin access, real and needed
}
print("Segmentation policy from the DIAGRAM (assumed flows):")
for s, d in sorted(ASSUMED): print(f"   allow {s} -> {d}")
print("   ...deny everything else.\n")
would_break = OBSERVED - ASSUMED
print(f"Flow map shows {len(OBSERVED)} real flows; the diagram knew {len(ASSUMED)}.")
print(f"Enforcing the diagram would BREAK {len(would_break)} real flows:")
for s, d in sorted(would_break):
    kind = {("web","db"): "  <- actually a debug path — CLOSE it, don't allow it",
            ("app","legacy-billing"): "  <- real dependency nobody documented",
            ("backup-agent","db"): "  <- backups die silently at 2am"}.get((s,d), "")
    print(f"   {s} -> {d}{kind}")
print("\nThe map turns segmentation from a risky guess into a reviewed decision:")
print("  most broken flows are LEGITIMATE-but-undocumented -> add to policy")
print("  some are findings -> web->db debug path gets CLOSED, not allowed")
print("The point is you now DECIDE each one, with evidence, instead of discovering")
print("them as 2am outages after enforcing a diagram that was always incomplete.")
EOF
```

**Expected result:** A two-flow diagram against an eight-flow reality, where enforcing the diagram breaks six real flows — most legitimate-but-undocumented, one an actual finding to close. The decision framing is the monitor-first rubric: the map converts every hidden dependency from a future outage into a present, evidence-backed choice.

**Negative test:** Segmenting from the architecture diagram. The backup path and the legacy-billing dependency were never on it, and both fail silently after enforcement.

**Cleanup:** None.

### Lab 7.2 — Labels outlive addresses

**Objective:** Watch address policy rot and label policy hold.

```bash
python3 - <<'EOF'
import random
random.seed(52)
# Address policy: allow 10.1.1.0/24 (app) -> 10.1.2.5 (db)
# Label policy:   allow role=app,env=prod -> role=db,env=prod
def gen_workloads(n, start_ip):
    out = []
    for i in range(n):
        out.append({"ip": f"10.1.{random.choice([1,3,7])}.{start_ip+i}",
                    "labels": {"role": random.choice(["app","app","worker"]), "env": "prod"}})
    return out

app_fleet = gen_workloads(6, 10)
new_app_nodes = gen_workloads(4, 40)   # autoscaled next month, new IPs, maybe new subnet

def addr_allowed(w):  return w["ip"].startswith("10.1.1.")
def label_allowed(w): return w["labels"]["role"] == "app" and w["labels"]["env"] == "prod"

print("Day 1 — 6 app nodes:")
print(f"   address policy covers: {sum(addr_allowed(w) for w in app_fleet)}/6")
print(f"   label policy covers  : {sum(label_allowed(w) for w in app_fleet if w['labels']['role']=='app')}/{sum(1 for w in app_fleet if w['labels']['role']=='app')} app nodes")

fleet = app_fleet + new_app_nodes
print(f"\nDay 30 — autoscaled to {len(fleet)} nodes (new IPs, some off the original subnet):")
app_nodes = [w for w in fleet if w["labels"]["role"] == "app"]
print(f"   address policy still covers: {sum(addr_allowed(w) for w in app_nodes)}/{len(app_nodes)} app nodes")
print(f"   label policy still covers  : {sum(label_allowed(w) for w in app_nodes)}/{len(app_nodes)} app nodes")
print("\nThe new app nodes came up on 10.1.3.x and 10.1.7.x. The ADDRESS policy")
print("does not cover them — they either can't reach the DB (broken) or someone")
print("widens the rule to a /16 (over-permissive). The LABEL policy covered them")
print("the instant they booted with role=app, because policy binds to the LABEL.")
print("\nThis is why Guardicore is a CERTIFICATION and not a course badge: the")
print("labeling SCHEMA is the actual skill. Bad labels = bad segmentation, applied")
print("automatically and confidently to everything. GCSA Advanced examines exactly this.")
EOF
```

**Expected result:** Address policy covers 6 of 6 nodes on day 1 and a fraction after autoscaling to new subnets, while label policy covers every `role=app` node throughout. The rot is the argument for label-based segmentation, and the closing line explains the certification depth — the labeling schema is a designed artifact whose quality determines whether enforcement helps or hurts.

**Negative test:** Widening the address rule to a `/16` when new nodes appear off-subnet. You restored connectivity by granting the whole range the database access that segmentation existed to remove.

**Cleanup:** None.

### Lab 7.3 — Ransomware containment as the GCSA Advanced scenario

**Objective:** Model the blast-radius reduction the credential names explicitly.

```bash
python3 - <<'EOF'
# A flat-ish network vs a segmented one; ransomware lands on one workload
WORKLOADS = ["web1","web2","app1","app2","db1","db2","backup","fileserver","dc","print"]
FLAT_REACHABLE = {w: [x for x in WORKLOADS if x != w] for w in WORKLOADS}  # everything talks to everything
SEGMENTED = {
  "web1": ["app1","app2"], "web2": ["app1","app2"],
  "app1": ["db1"], "app2": ["db1"],
  "db1": [], "db2": [], "backup": ["db1","db2","fileserver"],
  "fileserver": [], "dc": [], "print": [],
}
def spread(graph, patient_zero):
    seen, stack = set(), [patient_zero]
    while stack:
        n = stack.pop()
        if n in seen: continue
        seen.add(n)
        stack.extend(graph.get(n, []))
    return seen

pz = "web1"
flat = spread(FLAT_REACHABLE, pz)
seg = spread(SEGMENTED, pz)
print(f"Ransomware lands on {pz}.\n")
print(f"FLAT network:      reaches {len(flat)}/{len(WORKLOADS)} workloads — {', '.join(sorted(flat))}")
print(f"SEGMENTED network: reaches {len(seg)}/{len(WORKLOADS)} workloads — {', '.join(sorted(seg))}")
print(f"\nblast radius: {len(flat)} -> {len(seg)} ({(1-len(seg)/len(flat))*100:.0f}% reduction)")
print("\nweb1 can reach the app tier and, through it, ONE database — and stops.")
print("the domain controller, the file server, the backups, the second DB: all")
print("unreachable from a compromised web node, because no policy permits the flow.")
print("\nThis is the GCSA Advanced skill list made literal: 'ransomware mitigation'")
print("and 'east-west traffic control' are this containment. Segmentation does not")
print("PREVENT the initial compromise — it bounds what the compromise can become,")
print("which is the difference between an incident and a company-ending event.")
print("\n(Build this for real, five VMs, in Volume XCV — both the Centra console")
print("track and the native-firewall track prove exactly this reduction.)")
EOF
```

**Expected result:** A compromise reaching all 10 workloads on a flat network and 3 on a segmented one — a 70% blast-radius reduction. The literal mapping to the GCSA Advanced skill list ("ransomware mitigation," "east-west traffic control") is the point, and the closing pointer sends the reader to the real five-VM build in Volume XCV.

**Negative test:** Treating segmentation as prevention. It does not stop `web1` from being compromised; it stops `web1`'s compromise from reaching the domain controller and the backups — which is the whole value.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Guardicore ladder (GCSA/GCSE + variants, GCSP) navigated by role and level.
- [ ] Centra's collectors, flow map, and management placed.
- [ ] Policy designed from labels, with the schema understood as the examined skill.
- [ ] Segmentation understood as blast-radius containment, with Volume XCV as the hands-on build.
