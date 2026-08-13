# Chapter 06: Secrets for DevOps and Machine Identity

## Learning Objectives

- Explain DevOps Secrets Vault and the machine-secrets problem.
- Describe high-speed, API-driven secret retrieval for automation.
- Understand short-lived, dynamic secrets over hardcoded ones.
- Recognize machine identity as a fast-growing privileged surface.

*Cert relevance: DevOps Secrets Vault extends PAM to non-human (machine) identities — a distinct Delinea product.*

## The machine-secrets problem

Privileged access is not only about **humans**. Modern environments are full of **machine identities** — applications, scripts, CI/CD pipelines, containers, and microservices — that need **secrets** (database passwords, API keys, cloud credentials) to talk to each other. There are now **far more machine identities than human ones**, and their secrets are a huge, often-neglected attack surface: hardcoded passwords in source code, credentials in config files and environment variables, and keys that never rotate. **DevOps Secrets Vault** addresses this: a **high-speed secrets-management** system built for machines and automation, so applications retrieve secrets **securely at runtime** instead of embedding them. The lab models the problem.

## High-speed, API-driven retrieval

Machine secret access has different requirements than human vault access: it must be **fast** (automation makes many requests per second), **API-driven** (no human clicking a UI), and **scalable**. DevOps Secrets Vault is designed for this — a **high-throughput, API-first** vault where a pipeline or application authenticates and **fetches a secret programmatically** at the moment it is needed. This lets teams **remove hardcoded credentials** from code and config entirely: the secret lives in the vault, and the application requests it at runtime with its own machine identity. The lab models runtime retrieval.

## Short-lived, dynamic secrets

The strongest pattern DevOps Secrets Vault enables is **short-lived, dynamic secrets**: rather than a long-lived credential that sits in the vault for years, the vault issues a **just-in-time secret** that is valid only briefly (or generated on demand for a single use) and then expires. A leaked short-lived secret is worthless minutes later. This applies the [just-in-time principle (BeyondTrust CLVI)](../../volume-156-beyondtrust-certifications/chapters/02-privileged-access-management.md) to machine secrets: minimize the window in which any credential is useful. Dynamic, ephemeral secrets are how modern DevOps eliminates the standing, hardcoded credentials that breaches so often exploit. The lab models short-lived secrets.

## Machine identity as a privileged surface

The broader point is that **machine identity** is now a first-class privileged-access concern. Every service account, pipeline token, and application credential is a privileged identity that can be stolen and abused — and there are vastly more of them than human admins, changing constantly as code deploys. Securing machine identities (vaulting their secrets, making them short-lived, governing them) is as important as securing human privileged access, and it connects to [service-account governance (Ch 7)](07-account-lifecycle-manager.md) and the [cloud-entitlement work of Sysdig (CLV)/Wiz (CXLVII)](../../volume-155-sysdig-certifications/README.md). PAM has expanded to cover machines, and Delinea's DevOps Secrets Vault is that expansion. The lab synthesizes.

## Hands-On Lab

Python models machine secrets and short-lived credentials. **Cost:** none.

### Lab 6.1 — Runtime retrieval and short-lived secrets beat hardcoding

**Objective:** Contrast hardcoded credentials with vaulted, short-lived, API-retrieved secrets.

```bash
python3 - <<'EOF'
import time
# BAD: hardcoded secret in code/config vs GOOD: runtime retrieval of a short-lived secret
print("SCENARIO A — hardcoded credential (the common anti-pattern):")
print('   config.py: DB_PASSWORD = "P@ssw0rd-since-2019"   # in source control forever')
print("   -> leaks via repo, logs, backups, insider; NEVER rotates; long-lived = high value\n")

print("SCENARIO B — DevOps Secrets Vault: runtime retrieval of a SHORT-LIVED secret:")
class DevOpsSecretsVault:
    def issue_dynamic_secret(self, machine_id, ttl_s=300):
        return {"secret": f"dyn-{machine_id}-{int(time.time())}", "ttl_s": ttl_s, "issued": int(time.time())}
    def valid(self, tok, now):
        return now < tok["issued"] + tok["ttl_s"]

v = DevOpsSecretsVault()
tok = v.issue_dynamic_secret("ci-pipeline-42", ttl_s=300)   # 5-minute secret, fetched via API at runtime
now = tok["issued"]
print(f"   pipeline authenticates (machine identity) -> vault issues: {tok['secret']} (TTL {tok['ttl_s']}s)")
print(f"   used immediately (t+10s):  valid? {v.valid(tok, now+10)}")
print(f"   leaked + reused (t+600s):  valid? {v.valid(tok, now+600)}  -> EXPIRED, worthless\n")
print("The machine-secrets problem: there are FAR more machine identities (apps, CI/CD,")
print("containers) than humans, and their secrets are often HARDCODED — in code, config, env")
print("vars — never rotating. DevOps Secrets Vault fixes this: HIGH-SPEED, API-DRIVEN retrieval")
print("at RUNTIME (remove hardcoded creds entirely) + ★ SHORT-LIVED / DYNAMIC secrets (JIT for")
print("machines) so a leaked secret is dead in minutes. Machine identity is now a first-class")
print("privileged surface — PAM expanded to cover it.")
EOF
```

**Expected result:** A hardcoded credential that lives in source control forever versus a DevOps Secrets Vault dynamic secret fetched at runtime with a 5-minute TTL — valid immediately but expired (worthless) when reused later. The lesson is that machine identities vastly outnumber humans and their hardcoded secrets are a major attack surface; DevOps Secrets Vault removes hardcoded credentials via high-speed API retrieval and issues short-lived dynamic secrets, applying just-in-time to machines.

**Negative test:** Hardcoding credentials in code or config "because it's just a service account." Those leak and never rotate; vaulting them and issuing short-lived dynamic secrets retrieved at runtime removes the standing, embedded credential attackers exploit.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] DevOps Secrets Vault understood — secrets management built for machines and automation.
- [ ] High-speed, API-driven runtime retrieval understood — removing hardcoded credentials.
- [ ] Short-lived, dynamic secrets understood — just-in-time applied to machine credentials.
- [ ] Machine identity recognized as a fast-growing, first-class privileged surface.
