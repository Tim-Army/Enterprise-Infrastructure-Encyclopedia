# Chapter 03: Falco — Open-Source Runtime Security

## Learning Objectives

- Explain what Falco is and its role as the runtime detection engine.
- Understand Falco rules as detection-as-code.
- Describe the kinds of runtime behavior Falco detects.
- Recognize Falco's CNCF/open-source significance.

*Cert relevance: Falco is the subject of **LFS254** and the engine beneath Sysdig Secure — central to every Sysdig credential.*

## What Falco is

**Falco** is an **open-source runtime security engine** — created by Sysdig, donated to and stewarded by the [CNCF (XLI)](../../volume-041-cncf-kubernetes-certifications/README.md), and the de-facto standard for **Kubernetes/container runtime threat detection**. Falco watches the **behavior** of running workloads (via [eBPF/system-call instrumentation, Chapter 4](04-ebpf-and-deep-visibility.md)) and **alerts in real time** when it sees something suspicious — a shell spawning in a container, a sensitive file being read, an unexpected network connection, a privilege escalation.

Falco is significant beyond Sysdig: as a **CNCF project**, it is the open standard many organizations and other tools build on, and it is *free*. Understanding Falco is understanding the engine at the heart of cloud-native runtime detection — which is why it has its own [Linux Foundation course (Chapter 1)](01-the-sysdig-program.md) and why it anchors Sysdig Secure's CDR. The lab models Falco detection.

## Falco rules: detection-as-code

Falco's detections are **rules** — written as **code** (YAML), version-controlled, and testable, exactly like the [policy-as-code](../../volume-148-snyk-certifications/chapters/06-snyk-infrastructure-as-code.md) and [detection-engineering](../../volume-045-splunk-certifications/README.md) disciplines the shelf teaches. A Falco rule describes a **condition** on runtime events and an **output** when it matches:

```text
rule: Terminal shell in container
condition: spawned_process and container and shell_procs
output: "A shell was spawned in a container (user=%user.name container=%container.name)"
priority: WARNING
```

Falco ships a large set of **default rules** (community-maintained, covering common attack techniques and mapped to MITRE ATT&CK), and teams **write custom rules** for their own environment. Because rules are code, they are shareable, reviewable, and improvable — detection knowledge as a versioned artifact. The lab models rule evaluation.

## What Falco detects

Falco detects the **behavioral signs of an attack** — the actions an attacker takes that differ from normal workload behavior:

| Category | Example detection |
|:---|:---|
| **Shell/exec** | An interactive shell spawned in a container (containers rarely need one) |
| **File access** | Reading `/etc/shadow` or writing to a system binary directory |
| **Network** | An unexpected outbound connection (possible C2 or exfiltration) |
| **Privilege** | A process escalating privileges or a container running as root doing suspicious things |
| **Drift** | A new binary executed that was not in the original image ([Chapter 5](05-cloud-detection-and-response.md)) |

The insight: **containers have narrow, predictable behavior** (a web server serves HTTP; it does not spawn a shell or read `/etc/shadow`), so *deviation from that norm is a strong signal.* Falco encodes "normal for a container" and alerts on the anomalies. The lab models this.

## Hands-On Lab

Python models Falco rule detection. **Cost:** none.

### Lab 3.1 — Falco rules detect anomalous runtime behavior

**Objective:** Evaluate runtime events against detection-as-code rules.

```bash
python3 - <<'EOF'
# a stream of runtime events (from eBPF); Falco-style rules flag the suspicious ones
RULES = [
  # name,                       matches(event) -> bool,                             priority
  ("Terminal shell in container", lambda e: e["proc"] in ("bash","sh","zsh") and e["in_container"], "WARNING"),
  ("Read sensitive file",         lambda e: e.get("file") in ("/etc/shadow","/etc/sudoers"),        "ERROR"),
  ("Unexpected outbound conn",    lambda e: e.get("net") and e["net"]["dst"] not in ("registry","db"), "NOTICE"),
  ("Write below binary dir",      lambda e: (e.get("file") or "").startswith("/usr/bin/") and e.get("write"), "ERROR"),
]
EVENTS = [
  {"proc": "nginx",  "in_container": True, "file": "/var/www/index.html"},          # normal
  {"proc": "bash",   "in_container": True, "file": None},                            # shell in container!
  {"proc": "cat",    "in_container": True, "file": "/etc/shadow"},                    # sensitive read!
  {"proc": "app",    "in_container": True, "net": {"dst": "evil-c2.xyz"}},            # C2 callout!
  {"proc": "app",    "in_container": True, "net": {"dst": "db"}},                     # normal db conn
  {"proc": "dropper","in_container": True, "file": "/usr/bin/xmrig", "write": True},  # write to /usr/bin!
]
print("Runtime event stream evaluated against Falco-style rules:\n")
alerts = 0
for e in EVENTS:
    matched = [(name, pri) for name, cond, pri in RULES if cond(e)]
    label = f"proc={e['proc']}"
    if matched:
        alerts += 1
        for name, pri in matched:
            print(f"   [{pri:7}] {name}  ({label})")
    else:
        print(f"   [ok     ] no rule matched  ({label})")
print(f"\n   {alerts} alerts from {len(EVENTS)} events")
print("\nFalco rules are DETECTION-AS-CODE: each is a CONDITION on runtime events + an")
print("OUTPUT when it matches, written as versioned YAML (shareable, reviewable, mapped")
print("to MITRE ATT&CK). Here they flagged: a SHELL in a container, a read of")
print("/etc/shadow, a C2 callout, and a write to /usr/bin (a dropped miner) — while")
print("passing normal nginx serving + a legit db connection.")
print("\nThe key insight: containers have NARROW, PREDICTABLE behavior (nginx serves HTTP;")
print("it never spawns bash or reads /etc/shadow). So DEVIATION from that norm is a")
print("strong attack signal. Falco encodes 'normal for a container' as rules and alerts")
print("on the anomalies — the open-source engine (CNCF) at the heart of cloud-native")
print("runtime detection, and what Sysdig Secure's CDR is built on.")
EOF
```

**Expected result:** Runtime events evaluated against Falco-style detection-as-code rules, flagging a shell in a container, a sensitive-file read, a C2 callout, and a write to a binary directory while passing normal behavior. The Falco lesson is that rules are versioned, reviewable detection-as-code encoding "normal for a container," so deviations (which are strong attack signals given containers' narrow behavior) are caught in real time — the open-source CNCF engine beneath Sysdig's CDR.

**Negative test:** Trying to detect runtime attacks with static signatures of known malware. Attackers use novel tools and living-off-the-land techniques; Falco's behavioral rules ("a shell spawned in a container") catch the *actions* regardless of the specific tool.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Falco understood as the open-source (CNCF) runtime detection engine created by Sysdig.
- [ ] Falco rules understood as detection-as-code — versioned, reviewable conditions on runtime events.
- [ ] The behavioral categories Falco detects (shell, file, network, privilege, drift) understood.
- [ ] The narrow-container-behavior insight internalized — deviation from the norm is a strong attack signal.
