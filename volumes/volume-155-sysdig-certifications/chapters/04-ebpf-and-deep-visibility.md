# Chapter 04: eBPF and Deep Visibility

## Learning Objectives

- Explain eBPF and why it enables deep, safe runtime visibility.
- Understand system-call instrumentation as the source of truth.
- Recognize the low-overhead, no-code-change advantage.
- Place deep visibility as the foundation of runtime detection and forensics.

*Cert relevance: eBPF and system-call visibility are the technical foundation of Sysdig and Falco — how they see everything at runtime.*

## What eBPF is

**eBPF** (extended Berkeley Packet Filter) is a Linux kernel technology that lets programs run **safely inside the kernel** to observe (and act on) system events — without modifying the kernel or loading risky kernel modules. It is the technology that revolutionized cloud-native observability and security, because it provides **deep visibility into everything the system does** with **low overhead** and **safety** (eBPF programs are verified before they run, so they cannot crash the kernel).

Sysdig and Falco use eBPF to instrument the kernel and capture the **stream of system calls** — the fundamental operations every process performs. This is the technical foundation of everything: you cannot detect a runtime attack you cannot *see*, and eBPF is *how* Sysdig sees. The lab illustrates the visibility.

## System calls: the source of truth

Every meaningful thing a program does — open a file, spawn a process, make a network connection, read memory — happens through a **system call** to the kernel. This makes the system-call stream the **ground truth** of what is *actually happening* on a host: not what a log says happened (logs can be incomplete or forged), but what the kernel *actually did*.

By instrumenting system calls via eBPF, Sysdig/Falco see **everything, at the source** — every process launch, every file access, every network connection, across every container on the host, from *one* vantage point in the kernel (no per-application agents). This is why the visibility is "deep": it is at the lowest, most complete layer, where nothing can hide. An attacker's shell, file read, or network callout *is* a sequence of system calls, and the kernel sees them all. The lab models system-call-level detection.

## Low overhead, no code changes

The practical advantages that make this deployable at scale:

- **Low overhead** — eBPF is efficient; instrumenting system calls adds minimal performance cost, so it runs on production workloads without slowing them.
- **No code changes** — you do not instrument your applications; eBPF observes them from the kernel, so *any* workload (in any language, including ones you did not write) is covered automatically.
- **One agent per host** — a single eBPF-based sensor per node sees every container on it, rather than an agent per container.

Together these make deep runtime visibility *practical* — comprehensive, safe, cheap, and universal. The lab is covered within the visibility exercise.

## Hands-On Lab

Python models system-call visibility. **Cost:** none.

### Lab 4.1 — System calls are the ground truth

**Objective:** See why instrumenting syscalls reveals what logs miss.

```bash
python3 - <<'EOF'
# an attack, as the APPLICATION LOG sees it vs as the SYSCALL stream (eBPF) sees it
APP_LOG = [
  "INFO  request handled: GET /api/status 200",
  "INFO  request handled: POST /api/upload 200",
  # ...the attack leaves NO application log entry...
]
SYSCALL_STREAM = [
  ("execve", "nginx -> /bin/sh"),                        # shell spawned (the exploit)
  ("open",   "/etc/shadow (read)"),                      # sensitive file
  ("execve", "/bin/sh -> curl"),                         # tooling
  ("connect","curl -> 45.9.evil.xyz:443"),               # C2 / exfil
  ("open",   "/usr/bin/xmrig (write+exec)"),             # dropped miner
]
print("Same attack, two views:\n")
print("APPLICATION LOG (what the app chose to log):")
for line in APP_LOG:
    print(f"   {line}")
print("   ...and NOTHING about the attack. The app didn't log the exploit — why would")
print("   it? The attacker didn't go through the app's logging. The log is BLIND.\n")
print("SYSCALL STREAM via eBPF (what the KERNEL actually did):")
for sc, detail in SYSCALL_STREAM:
    print(f"   syscall {sc:9} {detail}")
print("   -> the ENTIRE attack is visible: shell spawn, /etc/shadow read, C2 connect,")
print("      miner dropped. Every action IS a system call, and the kernel saw them all.\n")
print("The insight: application LOGS show what the app CHOSE to record — incomplete, and")
print("an attacker operating BELOW the app leaves no trace. But every meaningful action")
print("(open a file, spawn a process, make a connection) is a SYSTEM CALL to the kernel.")
print("The syscall stream is GROUND TRUTH: what ACTUALLY happened, not what got logged.")
print("\neBPF instruments syscalls SAFELY in the kernel, so Sysdig/Falco see EVERYTHING")
print("at the source — every container, one vantage point, low overhead, no app changes.")
print("You can't detect what you can't see; eBPF is HOW Sysdig sees. Deep visibility at")
print("the lowest layer, where nothing can hide, is the foundation of runtime security.")
EOF
```

**Expected result:** An attack invisible in the application log (which only records what the app chose to) but fully visible in the eBPF system-call stream — shell spawn, sensitive-file read, C2 connect, dropped miner. The eBPF lesson is that system calls are the ground truth of what actually happened, and instrumenting them safely in the kernel gives deep, complete visibility that logs miss — the foundation of runtime detection.

**Negative test:** Relying on application logs to detect a runtime attack. An attacker operating below the application leaves no log entry; the system-call stream captured by eBPF sees every action because every action is a syscall.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] eBPF understood as safe, in-kernel instrumentation providing deep runtime visibility with low overhead.
- [ ] System calls understood as the ground truth of what actually happens, more complete than application logs.
- [ ] The low-overhead, no-code-change, one-agent-per-host advantages recognized as making deep visibility practical.
- [ ] Deep visibility placed as the foundation of runtime detection and forensics — you cannot detect what you cannot see.
