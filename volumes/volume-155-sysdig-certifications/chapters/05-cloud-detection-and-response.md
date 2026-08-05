# Chapter 05: Cloud Detection and Response (CDR)

## Learning Objectives

- Explain cloud detection and response and the speed imperative.
- Understand drift detection as a runtime-integrity signal.
- Describe the incident workflow with deep-visibility forensics.
- Recognize why cloud attacks demand fast, automated response.

*Cert relevance: CDR is a core Sysdig Secure capability and a major topic in the Sysdig accreditations.*

## The speed imperative

**Cloud Detection and Response (CDR)** is runtime threat detection *plus* the response to stop it — the [SentinelOne-style (CLI)](../../volume-151-sentinelone-certifications/chapters/02-autonomous-endpoint-protection.md) machine-speed idea, applied to cloud workloads. Sysdig emphasizes **5-second detection** — from a malicious action to an alert in ~5 seconds — because **cloud attacks move fast**: an attacker who lands in a container can escalate, move laterally, and exfiltrate in **minutes**, and against an [ephemeral container (Chapter 2)](02-runtime-first-cloud-security.md) that may only live for minutes, slow detection means detecting *nothing* (the container is gone).

Speed matters more in cloud than on traditional servers because the environment is faster: automation lets attackers act at machine speed, and workloads appear and vanish. Detection measured in *days* (typical for legacy SIEM correlation) is useless here; detection in *seconds* is the requirement, which the [Falco/eBPF (Chapters 3–4)](03-falco-open-source-runtime-security.md) real-time engine delivers. The lab models the speed imperative.

## Drift detection

A signature CDR capability is **drift detection** — catching when a *running* container **differs from the image it was built from.** The principle of **immutable infrastructure** is that a container should be exactly its image and never change at runtime: if a new binary appears in a running container that was *not* in the image, that is **drift**, and drift is almost always **malicious** (an attacker dropped a tool) or at least a policy violation.

Drift detection is powerful because it needs no signature — it does not ask "is this binary known-bad?" but "was this binary *supposed to be here*?" An attacker's dropped miner, backdoor, or tool is *by definition* drift (it was not in the image), so drift detection catches novel tooling that signatures miss. You can even **block execution of drifted binaries** — a strong runtime control. The lab models drift.

## Incident workflow with forensics

When CDR fires, the [deep visibility (Chapter 4)](04-ebpf-and-deep-visibility.md) provides **forensics** even for an ephemeral workload: because Sysdig captured the system-call activity, a responder can see **exactly what happened** — the full sequence of the attack (the [Storyline-like](../../volume-151-sentinelone-certifications/chapters/03-storyline-autonomous-correlation.md) narrative) — *even after the container is gone.* This solves the ephemeral-forensics problem: you get a recorded, replayable account of a container that lived for two minutes and no longer exists. Response actions (kill the pod, block the binary, isolate) then contain it. The lab is covered within the drift exercise.

## Hands-On Lab

Python models CDR. **Cost:** none.

### Lab 5.1 — Drift detection catches the dropped tool

**Objective:** See why comparing runtime to the image catches novel malware.

```bash
python3 - <<'EOF'
# the image's known binaries (immutable baseline) vs what's executed at RUNTIME
IMAGE_BINARIES = {"/usr/sbin/nginx", "/bin/sh", "/usr/bin/env"}   # what shipped in the image
RUNTIME_EXECS = [
  "/usr/sbin/nginx",        # in image - fine
  "/usr/bin/env",           # in image - fine
  "/tmp/xmrig",             # NOT in image -> DRIFT (dropped miner)
  "/usr/bin/nc",            # NOT in image -> DRIFT (netcat backdoor)
]
print("Immutable principle: a running container should be EXACTLY its image.\n")
print(f"image binaries (baseline): {sorted(IMAGE_BINARIES)}\n")
print("runtime executions:")
drift = []
for exe in RUNTIME_EXECS:
    is_drift = exe not in IMAGE_BINARIES
    if is_drift: drift.append(exe)
    print(f"   exec {exe:22} -> {'DRIFT! (not in image)' if is_drift else 'ok (in image)'}")
print(f"\n   drifted binaries: {drift}")
print("\nDrift detection asks NOT 'is this binary known-bad?' but 'was it SUPPOSED to be")
print("here?' /tmp/xmrig and /usr/bin/nc were NOT in the image, so they're DRIFT — an")
print("attacker dropped them at runtime. No signature needed: an attacker's tool is BY")
print("DEFINITION drift (it wasn't in the image), so drift detection catches NOVEL")
print("malware that signature scanning would miss.")
print("\nAnd you can BLOCK execution of drifted binaries — a strong runtime control:")
print("even if the attacker gets in, they can't RUN their dropped tools. This is the")
print("power of immutable infrastructure + runtime enforcement: the container can only")
print("do what its image intended, and any deviation is caught (or blocked) in seconds.")
print("Combined with eBPF forensics, you also get the full recorded attack sequence —")
print("even after an ephemeral container is gone. That's Sysdig CDR.")
EOF
```

**Expected result:** Runtime executions compared against the immutable image baseline, flagging binaries not in the image (a dropped miner, a netcat backdoor) as drift without needing signatures. The drift lesson is that comparing runtime to the image asks "was this supposed to be here?" — so an attacker's dropped tool is by definition drift and caught (or blocked) even though it is novel, with eBPF forensics providing the recorded attack sequence.

**Negative test:** Detecting dropped attacker tools by matching known-malware signatures. Novel or renamed tools evade signatures; drift detection catches them because they are not in the image — no signature required.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] CDR understood as runtime detection plus response, with 5-second detection required by fast, ephemeral cloud attacks.
- [ ] Drift detection understood as catching runtime deviation from the immutable image — signature-free novel-tool detection.
- [ ] The incident workflow understood — deep-visibility forensics provide the attack narrative even for gone containers.
- [ ] The speed imperative recognized — cloud attacks move at machine speed against short-lived workloads.
