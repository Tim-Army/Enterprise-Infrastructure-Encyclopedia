# Chapter 01: The SUSE Certification Program

## Learning Objectives

- Explain SUSE's portfolio (SLES, Rancher, NeuVector, SUSE Manager).
- Describe the SCA / SCDS / SCE certification levels.
- Understand the Questionmark exam model and product tracks.
- Map credentials to roles and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**SUSE** is an enterprise open-source vendor whose portfolio spans **SUSE Linux Enterprise Server
(SLES)** — a hardened enterprise Linux — and a cloud-native stack: **Rancher** (Kubernetes
management, with the **RKE2** and **K3s** distributions), **Longhorn** (Kubernetes storage),
**NeuVector** (container security), and **SUSE Manager** (patch and configuration management at
scale). Its certification program has three levels: **SUSE Certified Administrator (SCA)** for
day-to-day administration, **SUSE Certified Deployment Specialist (SCDS)** for deploying and
configuring, and **SUSE Certified Engineer (SCE)** for advanced engineering — each tied to a
**product** (SLES, Rancher, NeuVector, Longhorn, and more). Exams are delivered remotely through
**Questionmark**. The flagship is **SCA in SUSE Linux Enterprise (SLES 15)**, whose domains cover the
platform overview, filesystem, command line, system initialization, process management, security,
software management, network management, storage management, and administration/monitoring. SUSE sits
naturally beside the encyclopedia's other Linux volumes (RHEL 10 XIV, Ubuntu XXI) and its cloud-native
volumes (CNCF/Kubernetes XLI, Containers VIII). This volume teaches each with hands-on labs.

> **Scope.** SUSE administration is authorized systems work. The NeuVector container-security content
> is **defensive** — securing and monitoring authorized clusters, never an attack.

## Design Considerations

Start with the **SCA in SUSE Linux Enterprise** — it grounds the platform. Add **Rancher/Kubernetes**
for cloud-native, **SUSE Manager** for fleet management, and **NeuVector** for container security.
Choose the **level** (SCA/SCDS/SCE) that matches your role. Verify current product versions (SLES 15
vs newer) and exams on suse.com — SUSE refreshes exams with product releases.

## Implementation and Automation

Confirm your practice toolset (SLES concepts run on any Linux; SUSE-specific tools noted):

```bash
for t in zypper systemctl kubectl; do command -v "$t" >/dev/null && echo "$t: ok" || echo "$t: SUSE/K8s tool (use a SLES/openSUSE VM or lab)"; done
echo "Practice on a free openSUSE Leap / SLES trial VM and a Rancher/RKE2 lab cluster"
```

## Validation and Troubleshooting

The verified program facts (suse.com/training/certification, 29 July 2026):

```text
Levels: SCA (Administrator), SCDS (Deployment Specialist), SCE (Engineer) — per product. Delivery: Questionmark (remote proctored).
Products: SUSE Linux Enterprise Server (SLES 15 + updates), Enterprise Linux, Rancher (RKE2/K3s), NeuVector, Longhorn, SUSE Manager.
Flagship: SCA in SUSE Linux Enterprise (domains: overview/filesystem/CLI/init/process/security/software/network/storage/admin+monitoring).
```

Common pitfalls: assuming SUSE is only SLES (it spans **Rancher/Kubernetes and container security**);
and studying an old **product version** (verify SLES 15 vs newer on suse.com).

## Security and Best Practices

Learn the **current** levels and products on suse.com, ground yourself in **SLES**, and practice on a
free openSUSE/SLES VM and a Rancher lab. Treat NeuVector content as **defensive**. Verify product
versions before studying.

## References and Knowledge Checks

- suse.com/training/certification: the levels, products, and exams.
- documentation.suse.com: SLES, Rancher, SUSE Manager, and NeuVector docs.

**Knowledge checks**

1. Name three SUSE products with certifications.
2. What are the three SUSE certification levels?
3. What is the flagship SCA certification?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a Linux workstation (openSUSE/
SLES ideal) with `python3`, in a lab. **Cost:** none.

### Lab 1.1 — Map the SUSE portfolio

**Objective:** Learn the products.

```python
python3 - <<'PY'
portfolio={"SLES":"enterprise Linux (SCA/SCDS/SCE)","Rancher":"Kubernetes mgmt (RKE2/K3s)",
           "NeuVector":"container security (defensive)","Longhorn":"Kubernetes storage",
           "SUSE Manager":"patch/config at scale (Salt)"}
for p,scope in portfolio.items(): print(f"{p:13}: {scope}")
PY
```

**Expected result:** the SUSE **product map** — the tracks this volume follows.

**Negative test:** think SUSE is only SLES; it spans **Kubernetes and security** — use the full map.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map levels to roles

**Objective:** Record the level structure.

```python
python3 - <<'PY'
levels={"SCA":"Certified Administrator — day-to-day operation",
        "SCDS":"Certified Deployment Specialist — deploy/configure",
        "SCE":"Certified Engineer — advanced engineering"}
for lvl,scope in levels.items(): print(f"{lvl:5}: {scope}")
print("Each level applies to a product (e.g., SCA in SUSE Linux Enterprise)")
PY
```

**Expected result:** the **SCA/SCDS/SCE** levels and their scope — your scheduling reference.

**Negative test:** treat SCA and SCE as interchangeable; **SCE** is advanced engineering — pick by
role.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Linux admin":"SCA in SUSE Linux Enterprise -> SCE","Cloud-native":"SCA Rancher/RKE2",
       "Container security":"NeuVector (SCA)","Fleet management":"SUSE Manager"}
for role,path in paths.items(): print(f"{role:18}: {path}")
PY
```

**Expected result:** role-to-path sequences — the tracks this volume follows.

**Negative test:** jump to a Rancher cert with no Linux base; **SLES** grounds it — build up.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SUSE certifies its open-source portfolio across SCA/SCDS/SCE levels — SUSE Linux Enterprise Server plus
Rancher/Kubernetes, NeuVector, Longhorn, and SUSE Manager — delivered via Questionmark, taught here as
authorized administration with defensive container security.

- [ ] I can name three SUSE products with certifications.
- [ ] I can describe the SCA/SCDS/SCE levels.
- [ ] I can name the flagship SCA certification.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
