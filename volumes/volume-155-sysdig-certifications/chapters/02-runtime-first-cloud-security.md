# Chapter 02: Runtime-First Cloud Security

## Learning Objectives

- Explain the runtime-first philosophy and why it matters for cloud-native.
- Distinguish prevention/posture from detection/runtime.
- Understand the ephemeral, dynamic nature of containers.
- Recognize runtime and posture as complementary, not competing.

*Cert relevance: runtime-first is the philosophy behind every Sysdig credential — the "why" of the platform.*

## Prevention is necessary but not sufficient

Cloud-native security has two halves. **Prevention/posture** (shift-left) tries to stop problems *before* they run: scan container images for vulnerabilities, check configurations against best practice, enforce policy in CI/CD. This is essential and the [Wiz (CXLVII)](../../volume-147-wiz-certifications/README.md) and [Snyk (CXLVIII)](../../volume-148-snyk-certifications/README.md) volumes cover it well. But prevention is **necessary, not sufficient** — you cannot prevent everything: zero-days exist, misconfigurations slip through, insider actions happen, and a "clean" image can be exploited at runtime.

**Detection/runtime** is the other half: watching what workloads *actually do* while running, to catch the attacks prevention missed. **Sysdig's philosophy is runtime-first** — not because posture is unimportant, but because **the attack happens at runtime**, and a security platform that only checks static state is blind exactly when it matters. The lab quantifies the coverage gap.

## Containers are ephemeral

Runtime security is *especially* critical for cloud-native because **containers are ephemeral and dynamic**. A container may live for **seconds** (a serverless function, an autoscaled pod that spins up and down), and the fleet changes constantly. This breaks traditional security models built for long-lived servers you can scan on a schedule:

- By the time a periodic scan runs, the container that was attacked may be **gone** — no forensic trace, no host to inspect.
- You cannot install a heavyweight agent and reboot an ephemeral container.
- The *only* way to secure something that lives for seconds is to watch it **as it runs, in real time**, and capture what happened *before it disappears*.

This is why cloud-native security *demands* runtime detection with a **capture** of the activity — you get one chance, in real time, to see and record what a short-lived container did. The lab models the ephemeral-container problem.

## Complementary, not competing

The mature view — and what the certifications teach — is that **runtime and posture are complementary**. Posture *reduces the attack surface* (fewer vulns, better config, less to exploit); runtime *catches what gets through* (the exploit of the vuln you did not fix in time, the zero-day, the insider). A complete CNAPP does **both** — and Sysdig's *unification* of posture and runtime on one platform, **led by runtime**, is its pitch. Posture without runtime is blind to live attacks; runtime without posture is drowning in a larger attack surface than necessary. The lab makes the complement concrete.

## Hands-On Lab

Python models the runtime-versus-posture coverage. **Cost:** none.

### Lab 2.1 — The coverage gap posture leaves

**Objective:** Quantify what runtime detection adds over posture alone.

```bash
python3 - <<'EOF'
# categories of cloud-native incidents, and which half of security catches each
INCIDENTS = [
  # incident,                              posture_catches, runtime_catches
  ("known CVE in an image (pre-deploy)",   True,  True),
  ("misconfiguration caught in CI",        True,  True),
  ("ZERO-DAY exploited at runtime",        False, True),
  ("misconfig that slipped past scanning", False, True),
  ("compromised dependency runs malware",  False, True),
  ("insider spawns a shell in a container",False, True),
  ("crypto-miner deployed to a pod",       False, True),
  ("container drift (binary added live)",  False, True),
]
posture_only = sum(1 for _,p,r in INCIDENTS if p)
runtime_adds = sum(1 for _,p,r in INCIDENTS if r and not p)
print(f"{'incident':42}{'posture':>9}{'runtime':>9}")
for inc, p, r in INCIDENTS:
    print(f"{inc:42}{('catches' if p else 'BLIND'):>9}{('catches' if r else '-'):>9}")
print(f"\n   posture alone catches: {posture_only}/{len(INCIDENTS)}")
print(f"   runtime ADDS: {runtime_adds} incident types posture is BLIND to")
print("\nThe coverage gap: posture (image scanning + config checks) catches the KNOWN,")
print("PRE-DEPLOY problems — vulns and misconfigs you can find before running. But it's")
print("BLIND to everything that happens AT RUNTIME: zero-days, slipped-past misconfigs,")
print("compromised dependencies executing, insider shells, crypto-miners, drift.")
print("\nThose runtime incidents are exactly where real breaches happen — the attacker")
print("acts on a RUNNING workload. Prevention is necessary (shrink the attack surface)")
print("but NOT SUFFICIENT (you can't prevent a zero-day). Runtime detection catches what")
print("prevention missed. This is why Sysdig is runtime-FIRST: it covers the half of the")
print("problem posture-led tools leave blind. You need both — posture + runtime — and")
print("the attack lives at runtime.")
EOF
```

**Expected result:** Posture catching only the known pre-deploy incidents (CVEs, CI misconfigs) while runtime detection adds coverage for zero-days, slipped-past misconfigs, compromised dependencies, insider shells, crypto-miners, and drift. The coverage-gap lesson is that prevention is necessary but not sufficient — it is blind to what happens at runtime, which is where real breaches occur, so runtime-first security covers the half posture-led tools leave open.

**Negative test:** Securing cloud-native workloads with posture and image scanning alone. It catches known pre-deploy issues but is blind to zero-days, runtime drift, and insider actions — runtime detection is required to catch what prevention missed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The runtime-first philosophy understood — the attack happens at runtime, so static checks alone are blind when it matters.
- [ ] Prevention/posture distinguished from detection/runtime as the two necessary halves.
- [ ] The ephemeral, dynamic nature of containers understood as demanding real-time detection and capture.
- [ ] Runtime and posture recognized as complementary — posture shrinks the surface, runtime catches what gets through.
