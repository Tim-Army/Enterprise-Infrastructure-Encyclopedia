# Chapter 07: Deploying and Managing APIs

## Learning Objectives

- Explain deployment options — CloudHub and Runtime Fabric.
- Describe API Manager and applying policies.
- Understand monitoring and the operational view.
- Recognize governance across the application network.

*Cert relevance: deployment, API management, and monitoring are core Architect and Developer II domains.*

## Deployment: CloudHub and Runtime Fabric

Once a Mule application is built, it must **run** somewhere. Anypoint offers deployment targets:

- **CloudHub** — MuleSoft's **iPaaS** (integration platform as a service): a fully-managed cloud where Mule apps run without you managing infrastructure. You deploy an app, choose worker size and number, and CloudHub runs, scales, and monitors it. The **simplest** path — deploy to the cloud, done.
- **Runtime Fabric** — for **hybrid/on-premises/private-cloud** deployment: run the Mule runtime on your own infrastructure (including **Kubernetes**), for data-residency, latency, or regulatory reasons, while still managing it through Anypoint.

The choice reflects where the workload must run — CloudHub for cloud-managed simplicity, Runtime Fabric for control and on-prem/hybrid needs. The **Platform Architect** exam weights *Deploying to CloudHub* explicitly. The lab models deployment choices.

## API Manager and policies

Running an API is not enough — it must be **governed**. **API Manager** applies **policies** to APIs through an **API gateway**, controlling how they are consumed:

- **Rate limiting / throttling** — cap requests per consumer to protect backends.
- **Security** — enforce **OAuth 2.0**, client ID/secret, JWT validation, IP allow-lists.
- **SLA tiers** — different limits for different consumer tiers.
- **Other policies** — caching, header injection, logging.

Policies are applied **without changing the API's code** — the gateway enforces them at the edge. This lets a platform team govern the whole application network **consistently**: every API rate-limited, secured, and monitored by policy. API management is a core architect responsibility. The lab models policy enforcement.

## Monitoring and the operational view

**Anypoint Monitoring** (and **Visualizer**) provide the **operational view** of the running application network: dashboards of API traffic, response times, error rates, and health; **Visualizer** maps the network of APIs and their dependencies visually. This observability is essential for **meeting quality goals** (an explicit Platform Architect domain) and for operating at scale — you cannot manage what you cannot see. Monitoring closes the lifecycle loop: design, build, deploy, and now **observe and improve**. The lab models the operational view.

## Governance across the application network

The architect's job is **governance at the network level**: consistent policies, standards, monitoring, and reuse across **all** the APIs, not just one. This is where the [Platform Architect and Integration Architect (Ch 1)](01-the-mulesoft-program.md) certifications focus — establishing the organizational and platform foundations (the heaviest exam domain), applying integration patterns, managing APIs, and monitoring the network. Governance is what keeps the application network **healthy, secure, and reusable** as it grows. The lab synthesizes.

## Hands-On Lab

Python models deployment, policies, and monitoring. **Cost:** none.

### Lab 7.1 — Deploy, govern with policies, and monitor

**Objective:** Model deployment targets, API policies, and the operational view.

```bash
python3 - <<'EOF'
# 1) deployment target choice
def choose_target(needs_onprem, needs_managed_simplicity):
    if needs_onprem: return "Runtime Fabric (hybrid/on-prem/K8s — data residency/latency)"
    return "CloudHub (managed iPaaS — deploy + scale, no infra to run)"
print("DEPLOY:")
print("   cloud-native API   ->", choose_target(False, True))
print("   data-residency API ->", choose_target(True, False), "\n")

# 2) API Manager applies policies at the gateway (no code change)
POLICIES = {"rate_limit": "1000 req/min per client", "security": "OAuth 2.0 required",
            "sla_tier": "gold=5000/min, standard=500/min"}
def gateway(request):
    if not request.get("oauth_token"): return "401 (security policy: OAuth required)"
    if request.get("rpm", 0) > 1000:   return "429 (rate-limit policy exceeded)"
    return "200 (policies passed) -> forwarded to Mule app"
print("API MANAGER — policies enforced at the GATEWAY (no code change):")
for k, v in POLICIES.items(): print(f"   {k:10}: {v}")
print("   request no token      ->", gateway({"rpm": 10}))
print("   request 5000 rpm      ->", gateway({"oauth_token": "x", "rpm": 5000}))
print("   request valid         ->", gateway({"oauth_token": "x", "rpm": 10}), "\n")

# 3) monitoring / operational view
metrics = {"api": "Customers-Experience-API", "rps": 240, "p95_ms": 180, "error_rate": "0.3%"}
print("ANYPOINT MONITORING — operational view:")
print(f"   {metrics}")
print("\nDEPLOY to CloudHub (managed iPaaS) or Runtime Fabric (hybrid/on-prem/K8s). GOVERN with")
print("API MANAGER: apply POLICIES (rate limit, OAuth security, SLA tiers) at the GATEWAY without")
print("changing code. OBSERVE with Anypoint Monitoring/Visualizer (traffic, latency, errors, the")
print("network map). The ARCHITECT governs at the NETWORK level — consistent policies + standards")
print("+ monitoring across ALL APIs — keeping the application network healthy, secure, reusable.")
EOF
```

**Expected result:** A cloud-native API deployed to CloudHub and a data-residency API to Runtime Fabric; API Manager's gateway rejecting an unauthenticated request (401) and a rate-limit-exceeding request (429) while passing a valid one; and a monitoring view of traffic, latency, and errors. The lesson is that Anypoint deploys to CloudHub (managed) or Runtime Fabric (hybrid/on-prem), governs APIs with gateway policies applied without code changes, and observes the network via monitoring — the architect governing the whole application network.

**Negative test:** Deploying APIs with no gateway policies or monitoring. They are unprotected (no rate limiting or auth) and unobservable; API Manager policies and Anypoint Monitoring are what govern and operate the application network safely at scale.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Deployment options understood — CloudHub (managed iPaaS) and Runtime Fabric (hybrid/on-prem/K8s).
- [ ] API Manager and policies understood — rate limiting, OAuth security, SLA tiers at the gateway.
- [ ] Monitoring and the operational view understood — traffic, latency, errors, and the network map.
- [ ] Governance across the application network recognized as the architect's core responsibility.
