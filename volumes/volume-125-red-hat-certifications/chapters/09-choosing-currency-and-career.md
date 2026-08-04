# Chapter 09: Choosing a Track, Currency, and Career

## Learning Objectives

- Choose a Red Hat track and sequence its exams to RHCA.
- Understand the 2026 renewal model: retake, level up, or advance.
- Keep certifications current through RHEL-version and track-structure changes.

## Choosing a track

All five tracks start at RHCSA-or-equivalent and climb the same five levels; pick by where your work lives:

| If your work is… | Track | Path to RHCA |
|:---|:---|:---|
| RHEL system administration | Enterprise Linux | RHCSA → EX342 → 3 EL Specialists |
| Automation at scale | Ansible | RHCSA → RHCE (EX294) → 3 Ansible Specialists |
| Container platform ops | OpenShift | EX180 → EX280 → EX380 → 3 OpenShift Specialists |
| Application development on OpenShift | Cloud-Native | EX188 → EX288 → in-track Specialists |
| AI/ML platforms | AI (provisional) | verify codes on redhat.com |

RHCSA is the near-universal foundation; RHCE (Ansible, EX294) is the most-recognized mid-tier credential; RHCA is the capstone — now **track-specific**.

## Study approach: everything is performance-based

Red Hat exams cannot be crammed as multiple choice — they are **live systems**. The study method is repetition on a real lab:

| Exam | Volume chapters | Lab |
|:---|:---|:---|
| RHCSA (EX200) | [02](02-rhcsa-users-storage-boot.md)–[03](03-rhcsa-services-networking-selinux-containers.md) | RHEL 10 / AlmaLinux / Rocky VM ([Volume XIV](../../volume-014-red-hat-enterprise-linux-10/README.md) for depth) |
| RHCE (EX294) | [05](05-ansible-track-ex294.md) | control + managed nodes ([Volume LIX](../../volume-059-ansible/README.md)) |
| Advanced EL (EX342) | [04](04-enterprise-linux-track-ex342.md) | RHEL VM |
| OpenShift (EX280) | [06](06-openshift-track-ex280.md) | CRC / kind / minikube ([Volume XLI](../../volume-041-cncf-kubernetes-certifications/README.md)) |
| Cloud-Native (EX188/288) | [07](07-cloud-native-and-ai-tracks.md) | Podman + local cluster |
| Specialists | [08](08-specialist-electives.md) | per-elective lab |

Free RHEL access: a **Red Hat Developer subscription** (no-cost for individual use) gives genuine RHEL; **AlmaLinux**/**Rocky Linux** are binary-compatible rebuilds; **CRC** runs OpenShift locally. Every lab in this volume runs on these.

## Currency (the 2026 model)

- **Three renewal paths** replaced the single retake: **retake** the same exam, **level up** (pass a higher exam in the track, which auto-renews lower credentials), or **advance** (broaden). Leveling up is the efficient path — one exam refreshes the chain.
- **RHEL-version rebasing.** RHCSA is on **RHEL 10**; RHEL 9 EX200 may linger briefly. Study the version the exam page names, and keep your lab at that major version.
- **Track-specific RHCA.** Three Specialists must share the track with your Administrator and Engineer exams — plan the three electives up front, not opportunistically.
- **Retirements move you forward.** EX318 (RHV virtualization) is gone; EX316 (OpenShift Virtualization) is its replacement. Verify a specialist still exists before committing study time.
- **The AI track is provisional.** Its exam codes were pending at verification; confirm on redhat.com before planning around it.

## Hands-On Lab

### Lab 9.1 — Build your Red Hat certification plan

**Objective:** Commit a track-aligned, RHCA-oriented plan.

```bash
cat > my-redhat-plan.md <<'EOF'
Work: sysadmin / automation / openshift / dev / ai
Track: Enterprise Linux / Ansible / OpenShift / Cloud-Native / AI
L2 exam: EX200 / EX280 / EX188      Target date: ___   Lab: RHEL10 / AlmaLinux / CRC
L3 exam: EX342 / EX294 / EX380      Target date: ___
RHCA electives (SAME track, pick 3): ___ , ___ , ___
Renewal plan: level up (higher exam auto-renews lower)   RHEL version check: ___
EOF
cat my-redhat-plan.md
```

**Expected result:** A plan naming exact exam codes, the RHEL/lab version, and three in-track electives chosen in advance — the discipline the track-specific RHCA rule demands.

**Negative test:** A plan with electives from mixed tracks — invalid for RHCA post-2026; catch it at planning time.

**Cleanup:** Keep the plan.

### Lab 9.2 — Verify exam currency before booking

**Objective:** Make the RHEL-version/track check routine.

```bash
cat <<'EOF'
Before booking, on redhat.com/en/services/certifications:
  [ ] exam code still current (not retired — cf. EX318)
  [ ] RHEL/product version the exam is based on (RHEL 10? OCP 4.18?)
  [ ] your lab matches that major version
  [ ] for AI track: confirm the code exists officially (was pending 3 Aug 2026)
EOF
echo "one check saves studying a retired or wrong-version exam"
```

**Expected result:** A four-point pre-booking check — the currency habit that catches rebases and retirements before they cost study time.

**Negative test:** Studying EX200 on RHEL 8 because a book said so — version drift; the exam page is the authority.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Track chosen and sequenced to a track-specific RHCA.
- [ ] Performance-based study method (real lab, repetition) adopted with a free RHEL-family environment.
- [ ] 2026 renewal model (retake/level-up/advance) and version/retirement currency habits installed.
