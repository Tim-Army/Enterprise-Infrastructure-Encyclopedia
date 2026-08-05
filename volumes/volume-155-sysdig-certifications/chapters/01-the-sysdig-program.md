# Chapter 01: The Sysdig Program

![The Sysdig learning and accreditation program and the runtime-first platform beneath it. Sysdig's program is delivered through its enablement portal and issues Credly digital badges. Its signature named accreditation, Kraken Hunter, validates using Sysdig tooling for cloud and container security through a workshop of hands-on labs and presentations followed by an exam; a Partner Technical Accreditation Program awards badges per level to partner teams. Separately, Falco, the open-source runtime security engine that Sysdig created and donated to the Cloud Native Computing Foundation, has its own training path: the twenty-hour Detecting Cloud Runtime Threats with Falco course, LFS254, built by CNCF, the Linux Foundation, and Sysdig. The platform beneath is runtime-first. Sysdig Secure is an enterprise cloud-native application protection platform that unifies cloud detection and response, cloud workload protection, cloud security posture management, cloud infrastructure entitlement management, and vulnerability management, with Falco-powered runtime threat detection achieving five-second detection. Sysdig Monitor adds Prometheus-based observability. The unifying idea is runtime-first security built on eBPF kernel instrumentation for deep visibility into what is actually running, complementing agentless posture with what is happening right now.](../../../diagrams/volume-155-sysdig-certifications/chapter-01-program.svg)

*Figure 1-1. Credly-badged accreditations and the Falco open-source path over the runtime-first platform.*

## Learning Objectives

- Describe the Sysdig program — Credly-badged accreditations and the Falco training path.
- Distinguish Sysdig's product accreditations from the open-source Falco course.
- Place the runtime-first CNAPP and its signature technologies.
- Recognize Sysdig's position in cloud-native security.

> **Defensive framing.** This volume is about *defending* cloud-native workloads — detecting threats at runtime, prioritizing real vulnerabilities, and enforcing posture. The mechanisms (Falco rules, runtime detection, drift detection) are the tools a cloud-security team uses to protect containers and cloud. Nothing here is about attacking systems.

## What Sysdig is

Sysdig is a leader in **cloud-native and container security** — its platform, **Sysdig Secure**, is a **runtime-first CNAPP** (Cloud-Native Application Protection Platform) that secures containers, Kubernetes, and cloud by watching what is **actually running**. Sysdig also *created* **Falco** — the open-source **runtime security engine** now stewarded by the [CNCF (XLI)](../../volume-041-cncf-kubernetes-certifications/README.md) — which is the foundation of its runtime detection. Where the [Wiz volume (CXLVII)](../../volume-147-wiz-certifications/README.md) leads with *agentless posture* (what *could* be wrong), **Sysdig leads with *runtime* — what *is* happening right now** on your workloads, via deep [eBPF (Chapter 4)](04-ebpf-and-deep-visibility.md) instrumentation.

## The program

Sysdig's credentialing has two distinct strands — and it is worth being precise about what they are:

> **A badged-accreditation program plus the open-source Falco path.** Sysdig's own credentials are **Credly digital badges** earned through its **enablement portal** — most notably the **Kraken Hunter** accreditation (a hands-on workshop of labs and presentations plus an exam, validating Sysdig-tooling skill for cloud & container security) and a **Partner Technical Accreditation** program. Separately, **Falco** (the open-source engine Sysdig created) has a **Linux Foundation / CNCF** course, **LFS254 "Detecting Cloud Runtime Threats with Falco"** (~20 hours). This is a *badges-and-training* program, stated plainly — hands-on and current — not a proctored vendor-exam gate.

| Strand | Is |
|:---|:---|
| **Kraken Hunter** (Credly) | Sysdig-tooling accreditation — workshop (labs) + exam |
| **Partner Technical Accreditation** | Partner-team badges per level |
| **Falco LFS254** (CNCF/LF) | Open-source runtime-security course (~20h) |

The two strands reflect Sysdig's dual identity: a **commercial platform** (Sysdig Secure) *and* the **steward of open-source Falco**. Learning Sysdig means learning both the product and the Falco engine beneath it.

## The runtime-first platform

Every credential sits on the **runtime-first** platform:

| Capability | Is |
|:---|:---|
| **Falco-powered CDR** | Runtime threat detection & response (5-second detection) ([Chapter 5](05-cloud-detection-and-response.md)) |
| **Vulnerability management** | Prioritized by *in-use* runtime context ([Chapter 6](06-vulnerability-management-runtime-prioritization.md)) |
| **CSPM / CIEM** | Posture and entitlements ([Chapter 7](07-posture-permissions-and-compliance.md)) |
| **Sysdig Monitor** | Prometheus-based observability ([Chapter 8](08-the-unified-cnapp-and-monitor.md)) |

The unifying idea is **runtime-first**: static posture (CSPM) tells you what *could* be exploited; runtime tells you what *is* being exploited *now*. Sysdig's signature is deep runtime visibility (via [eBPF](04-ebpf-and-deep-visibility.md) and [Falco](03-falco-open-source-runtime-security.md)) that other CNAPPs, leading with posture, do not match. The lab reads the program and the runtime-first idea.

## Hands-On Lab

The labs in this volume model cloud-native-security concepts in Python at no cost. **Falco is free and open-source**, and Sysdig offers a **free trial** — so the runtime-detection concepts can genuinely be explored at no cost.

### Lab 1.1 — Read the two-strand program

**Objective:** Place a credential by strand and what it validates.

```bash
python3 - <<'EOF'
CREDS = [
  # credential,               strand,                  validates
  ("Kraken Hunter",           "Sysdig (Credly badge)", "using Sysdig tooling for cloud & container security"),
  ("Partner Technical Accreditation","Sysdig (Credly badge)", "partner-team skill per accreditation level"),
  ("Falco LFS254",            "CNCF / Linux Foundation","open-source runtime threat detection (~20h)"),
]
print(f"{'credential':28}{'strand':26}validates")
for cred, strand, val in CREDS:
    print(f"{cred:28}{strand:26}{val}")
print("\nTWO strands, reflecting Sysdig's dual identity:")
print("  SYSDIG PRODUCT accreditations (Credly badges via the enablement portal) —")
print("     Kraken Hunter (a workshop of LABS + an EXAM) proves you can USE Sysdig")
print("     tooling; Partner Technical Accreditation is the partner-team track.")
print("  FALCO (CNCF/LF) — Sysdig CREATED Falco and donated it to the CNCF, so the")
print("     open-source engine has its OWN Linux Foundation course (LFS254).")
print("\nWhat KIND of program: badges + hands-on training, NOT proctored vendor exams.")
print("Genuine, current, lab-based. Learning Sysdig means learning BOTH the commercial")
print("platform (Sysdig Secure) AND the open-source Falco engine beneath it — that dual")
print("identity (product + open-source steward) is central to Sysdig.")
EOF
```

**Expected result:** The credentials placed across two strands — Sysdig's Credly-badged product accreditations (Kraken Hunter, Partner Technical) and the open-source Falco LFS254 course from CNCF/Linux Foundation. The program lesson is Sysdig's dual identity: a commercial platform and the steward of open-source Falco, so learning it means both the product and the engine beneath, via a badges-and-training model rather than proctored exams.

**Negative test:** Expecting a single proctored Sysdig certification like AWS's. Sysdig's program is Credly-badged accreditations plus the open-source Falco training path — hands-on and current, but a different, badge-based model.

**Cleanup:** None.

### Lab 1.2 — Runtime-first: what posture alone misses

**Objective:** See why runtime security catches what static posture cannot.

```bash
python3 - <<'EOF'
# a container: its static posture is clean, but at RUNTIME something happens
events = [
  # time, what,                                          posture_sees, runtime_sees
  ("t0", "image scanned: no critical vulns, config OK",  True,  True),
  ("t1", "container deployed, running normally",         True,  True),
  ("t2", "attacker exploits a 0-day, spawns /bin/bash",  False, True),   # posture is BLIND to this
  ("t3", "shell reads /etc/shadow, curls to evil.com",   False, True),   # runtime behavior
  ("t4", "new binary dropped + executed (drift)",        False, True),
]
print("A container that passed STATIC posture checks — then gets attacked at RUNTIME:\n")
print(f"   {'time':5}{'event':50}{'posture?':>9}{'runtime?':>10}")
for t, what, ps, rt in events:
    print(f"   {t:5}{what:50}{('sees' if ps else 'BLIND'):>9}{('DETECTS' if rt else '-'):>10}")
print("\nPosture (CSPM) checked the image + config at BUILD/DEPLOY time — all clean.")
print("But at RUNTIME an attacker exploited a 0-day, spawned a shell, read /etc/shadow,")
print("called out to a C2, and dropped a new binary. POSTURE IS BLIND to all of it —")
print("it only knows the static state, not what's HAPPENING.")
print("\nRUNTIME security (Falco/Sysdig) DETECTS each behavior: 'a shell spawned in a")
print("container', 'a sensitive file read', 'unexpected outbound', 'binary drift' — the")
print("signs of an attack in progress. This is why Sysdig is RUNTIME-FIRST: posture")
print("tells you what COULD be wrong (fix it — Wiz CXLVII does this well); runtime tells")
print("you what IS wrong RIGHT NOW. You need both, but the ATTACK happens at runtime, and")
print("that's where Sysdig leads. A clean scan doesn't mean a safe running container.")
EOF
```

**Expected result:** A container passing all static posture checks but then exploited at runtime (shell spawn, sensitive-file read, C2 callout, binary drift) — all invisible to posture but detected by runtime security. The runtime-first lesson is that posture knows the static state while runtime knows what is happening now, and since the attack happens at runtime, that is where Sysdig leads — a clean scan does not mean a safe running container.

**Negative test:** Relying on posture/image scanning alone for cloud-native security. A container can pass every static check and still be exploited at runtime via a 0-day; only runtime detection sees the shell spawn, the drift, and the C2 callout as they happen.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Sysdig program understood as Credly-badged accreditations (Kraken Hunter) plus the open-source Falco LFS254 path.
- [ ] Sysdig's dual identity (commercial platform + Falco steward) recognized.
- [ ] The runtime-first CNAPP and its capabilities (Falco CDR, in-use vuln mgmt, CSPM/CIEM) placed.
- [ ] Runtime-first understood — posture knows the static state, runtime knows what is happening now.
