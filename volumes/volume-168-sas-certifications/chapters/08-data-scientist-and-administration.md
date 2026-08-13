# Chapter 08: The Data Scientist Path and Viya Administration

## Learning Objectives

- Explain the composite SAS Certified Data Scientist credential and its components.
- Understand how curation, programming, analytics, and ML combine end to end.
- Describe SAS Viya Administration and what platform admins do.
- Recognize the two career poles — building analytics versus running the platform.

*Cert relevance: this chapter covers the SAS Certified Data Scientist composite and the Viya Administration credential.*

## The composite Data Scientist credential

The **SAS Certified Data Scientist** is the program's **capstone** — not a single exam but a **composite** credential earned by **combining several credentials** across the discipline. Its logic is that a real data scientist must be competent **end to end**, so the composite typically draws from:

- **Data Curation** ([Ch 4](04-preparing-and-curating-data.md)) — prepare and combine trustworthy data.
- **Programming** (Advanced Programming, [Ch 3](03-sas-programming-foundations.md)) — the SAS language to do the work at depth.
- **AI & Machine Learning** ([Ch 6](06-machine-learning-on-viya.md)) — build and assess predictive models.
- **Advanced Analytics / Statistics** ([Ch 5](05-statistical-analysis.md)) — sound statistical method.

Earning the component credentials **and** the composite proves you can take a problem **from raw data to a deployed, assessed model** — the full data-science lifecycle. *(The Data Scientist path was updated 30 June 2025, so confirm the current required components.)* The lab assembles the composite. The point is that data science is a **combination** of skills, not one.

## End to end

The Data Scientist credential reflects the **end-to-end workflow** the earlier chapters build:

1. **Curate** — combine, format, clean, and validate the data ([Ch 4](04-preparing-and-curating-data.md)).
2. **Explore and describe** — descriptive statistics and visualization ([Ch 5](05-statistical-analysis.md), [Ch 7](07-visual-analytics-and-bi.md)).
3. **Model** — statistical and machine-learning models ([Ch 5](05-statistical-analysis.md), [Ch 6](06-machine-learning-on-viya.md)).
4. **Assess** — fit, significance, validation on held-out data.
5. **Deploy and monitor** — score new data, watch for drift, retrain.

No single step is "data science" alone; the discipline is doing **all** of them well, with rigor at each. That is why the credential is composite — it certifies the **whole pipeline**, not a fragment. A data scientist who can only model, but not curate or assess, delivers unreliable results. The lab traces the end-to-end flow.

## SAS Viya Administration

Someone must **run the platform** the data scientists use, and that is the **administrator**. **SAS Viya Administration** (A00-451) validates operating SAS Viya:

- **Deployment and environment** — Viya runs on **Kubernetes**; admins manage the deployment, resources, and the CAS server.
- **Users, groups, and security** — authentication, authorization, and access to data and content.
- **Content and data governance** — organize folders, manage data connections, and control who can see and do what.
- **Monitoring and maintenance** — keep the environment healthy, manage capacity, and troubleshoot.

Administration is a **distinct career pole** from analytics: the admin does not build models but makes it possible for many people to, reliably and securely. It is the operational counterpart to the analytic credentials. The lab models an admin task. *(Platform administration parallels admin tracks across the encyclopedia's platforms.)*

## Two career poles

SAS certification points to **two complementary directions**:

- **Building analytics** — programmer → statistician / analyst → data scientist. You **use** SAS to analyze data and build models. Most credentials live here.
- **Running the platform** — administrator. You **operate** SAS Viya so others can use it.

Both are valuable and they depend on each other: admins provide a stable, governed platform; analysts and data scientists deliver insight on it. Knowing which pole you are on — and that the certifications serve both — helps you choose a path ([Ch 9](09-choosing-your-sas-path.md)). The lab contrasts the poles.

## Hands-On Lab

Python models the composite Data Scientist credential, the end-to-end flow, and an admin task. **Cost:** none.

### Lab 8.1 — Assemble the Data Scientist path and an admin task

**Objective:** Combine component credentials into the composite, trace the lifecycle, and model administration.

```bash
python3 - <<'EOF'
# SAS Certified Data Scientist = COMPOSITE of component credentials
COMPONENTS = ["Data Curation", "Advanced Programming", "Machine Learning (Viya)", "Advanced Analytics/Statistics"]
earned = set(COMPONENTS)   # a candidate who has earned all components
data_scientist = earned.issuperset(COMPONENTS)
print("SAS CERTIFIED DATA SCIENTIST — composite credential:")
for c in COMPONENTS:
    print(f"   [{'x' if c in earned else ' '}] {c}")
print(f"   -> Data Scientist earned: {data_scientist} (combine all components)\n")

# end-to-end lifecycle the composite certifies
lifecycle = ["curate data", "explore/describe", "model (stats + ML)", "assess (held-out)", "deploy + monitor drift"]
print("END-TO-END (what the composite proves):")
print("   " + " -> ".join(lifecycle))

# Viya Administration: a platform admin task (grant a group access to a CAS library)
print("\nSAS VIYA ADMINISTRATION (the other career pole):")
def admin_grant(group, resource, perm):
    return f"admin: granted '{group}' {perm} on '{resource}' (Kubernetes-hosted Viya, governed)"
print("   " + admin_grant("data-scientists", "CAS lib PRODUCTION", "read"))
print()
print("The DATA SCIENTIST credential is COMPOSITE — combine Data Curation + Advanced Programming")
print("+ Machine Learning + Advanced Analytics — proving the WHOLE lifecycle (curate -> explore ->")
print("model -> assess -> deploy), not one skill. The ADMINISTRATOR is the other pole: they RUN")
print("Viya (on Kubernetes) — users, security, data governance — so others can build analytics.")
EOF
```

**Expected result:** The composite Data Scientist assembled from its component credentials, the end-to-end lifecycle it certifies, and an administrator task granting access on the Kubernetes-hosted platform. The lesson is the two poles of SAS certification: the Data Scientist path composes curation, programming, ML, and statistics into end-to-end competency, while Viya Administration is the operational pole that runs the platform others build on.

**Negative test:** Calling someone a "data scientist" who can only build models but cannot curate data or assess results. The models are unreliable because the surrounding lifecycle is missing; the composite credential exists precisely to certify the whole pipeline, not one fragment.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The composite Data Scientist credential understood — combining curation, programming, ML, and analytics.
- [ ] The end-to-end workflow understood — curate → explore → model → assess → deploy/monitor.
- [ ] SAS Viya Administration understood — running Viya on Kubernetes: users, security, governance, monitoring.
- [ ] The two career poles understood — building analytics versus running the platform.

## See also

- [Chapter 04 — Preparing and Curating Data](04-preparing-and-curating-data.md), [Chapter 05 — Statistical Analysis](05-statistical-analysis.md), and [Chapter 06 — Machine Learning on Viya](06-machine-learning-on-viya.md) — the components that compose into Data Scientist.
- [Chapter 09 — Choosing Your SAS Path](09-choosing-your-sas-path.md) — turning these into a personal plan.
