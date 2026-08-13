# Chapter 08: The Unified CNAPP and Sysdig Monitor

## Learning Objectives

- Explain how Sysdig unifies the security capabilities into one CNAPP.
- Understand the shared-visibility advantage of one platform.
- Place Sysdig Monitor and observability alongside security.
- Recognize the convergence of security and observability on runtime data.

*Cert relevance: the unified platform is the synthesis the accreditations validate — how the pieces compose.*

## The unified CNAPP

The previous chapters each covered one capability; **Sysdig Secure unifies them** into one CNAPP: [CDR](05-cloud-detection-and-response.md), [vulnerability management](06-vulnerability-management-runtime-prioritization.md), [CSPM, CIEM, and compliance](07-posture-permissions-and-compliance.md) — all on **one platform, sharing the same deep [runtime data (Chapter 4)](04-ebpf-and-deep-visibility.md).** This is the [convergence lesson](../../volume-153-cato-networks-certifications/chapters/03-traditional-stack-vs-converged-sase.md) applied to cloud-native security: instead of separate tools for scanning, posture, entitlements, and runtime (each with its own console and blind spots), one platform does all of it, and — crucially — the capabilities **inform each other.**

The shared-data advantage is Sysdig's real pitch: because **the same runtime observation** feeds vulnerability prioritization (*in-use* packages), posture (which misconfig is on a *running, exposed* workload), entitlements (which permissions are *actually used*), and detection (Falco on the *live* syscalls), each capability is *sharper* than it would be alone. Runtime is the **connective tissue** — the one source of truth that makes the whole CNAPP more than the sum of its parts. The lab models the shared-context advantage.

## From shift-left to runtime, unified

A complete cloud-native security program spans the lifecycle: **shift-left** (scan images and IaC before deploy) *and* **runtime** (detect and respond in production). Sysdig covers the span but, true to its identity, **anchors it in runtime** — and the runtime data flows *back* to improve the shift-left side (e.g., which image vulnerabilities to prioritize based on what actually runs). The lifecycle is a loop, not a line: runtime informs prevention, prevention reduces runtime risk. The lab is covered within the shared-context exercise.

## Sysdig Monitor: observability

Sysdig's origin is **observability** (monitoring), and **Sysdig Monitor** — Prometheus-compatible monitoring for cloud, containers, and Kubernetes — sits alongside Sysdig Secure. This reflects a deep truth: **security and observability draw on the same deep runtime data.** The system-call and metrics stream that reveals a performance problem also reveals an attack; the same eBPF instrumentation serves both. Sysdig's coverage of *both* security and observability from one data foundation is distinctive, and it mirrors the industry convergence of the two disciplines (the [observability shelf — Datadog, Dynatrace, Grafana](../../volume-140-dynatrace-certifications/README.md) — increasingly touches security too). The lab is covered within the exercises above.

## Hands-On Lab

Python models the shared-data advantage. **Cost:** none.

### Lab 8.1 — Shared runtime data makes every capability sharper

**Objective:** See how one runtime source improves the whole CNAPP.

```bash
python3 - <<'EOF'
# a workload; runtime observation feeds MULTIPLE security capabilities at once
runtime_facts = {
    "workload": "payments-api",
    "running": True,
    "internet_exposed": True,
    "loaded_packages": {"openssl", "libc", "app-code"},   # what's actually in use
    "used_permissions": {"db:read", "secrets:read"},       # what's actually exercised
    "behavior_baseline": "serves HTTPS, reads db",
}
# each capability, WITHOUT vs WITH the shared runtime context
print(f"Workload '{runtime_facts['workload']}' — ONE runtime observation feeds ALL:\n")
print("VULNERABILITY MGMT:")
print("   without runtime: 900 image CVEs, all 'to fix'")
print(f"   WITH runtime: prioritize CVEs in {runtime_facts['loaded_packages']} (actually loaded)")
print("      + it's INTERNET-EXPOSED -> those are top priority\n")
print("POSTURE (CSPM):")
print("   without runtime: a list of misconfigs across all resources")
print(f"   WITH runtime: this workload is RUNNING + EXPOSED -> its misconfigs jump the queue\n")
print("ENTITLEMENTS (CIEM):")
print(f"   without runtime: guess what permissions to keep")
print(f"   WITH runtime: used = {runtime_facts['used_permissions']} -> remove the rest\n")
print("DETECTION (CDR):")
print(f"   baseline: '{runtime_facts['behavior_baseline']}' -> anything else = anomaly to alert\n")
print("The unifying advantage: ONE runtime observation of this workload makes EVERY")
print("capability sharper — vuln prioritization (in-use packages), posture (running +")
print("exposed), entitlements (used permissions), detection (behavior baseline). Runtime")
print("is the CONNECTIVE TISSUE that ties the CNAPP together.")
print("\nSeparate point tools each see a slice and miss the connections; ONE platform on")
print("SHARED runtime data makes the whole more than the sum of its parts. And the SAME")
print("data powers OBSERVABILITY (Sysdig Monitor) — because a perf problem and an attack")
print("are both visible in the same deep runtime stream. Security + observability, one")
print("foundation. That convergence, anchored in runtime, is Sysdig's whole thesis.")
EOF
```

**Expected result:** One runtime observation of a workload sharpening vulnerability prioritization (in-use packages), posture (running and exposed), entitlements (used permissions), and detection (behavior baseline) simultaneously. The unified-CNAPP lesson is that runtime is the connective tissue tying the capabilities together — shared data makes each sharper than standalone tools, and the same foundation powers observability, converging security and observability.

**Negative test:** Assembling cloud-native security from separate scanning, posture, entitlement, and runtime tools. Each sees a slice and misses the connections; one platform on shared runtime data lets the capabilities inform each other, and the same data also serves observability.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The unified CNAPP understood — CDR, vulnerability management, CSPM, CIEM, and compliance on one platform.
- [ ] The shared-visibility advantage understood — the same runtime data makes every capability sharper.
- [ ] Sysdig Monitor placed as Prometheus-based observability on the same deep runtime foundation.
- [ ] The convergence of security and observability on runtime data recognized as Sysdig's distinctive position.
