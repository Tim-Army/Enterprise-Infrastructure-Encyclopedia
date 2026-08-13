# Chapter 07: Cloudera Machine Learning Engineer

## Learning Objectives

- Explain the ML Engineer role — building and operationalizing models on CDP.
- Describe Cloudera AI (formerly Cloudera Machine Learning).
- Understand MLOps — the lifecycle from development to production.
- Recognize the advantage of ML on the data platform.

*Cert relevance: the Cloudera Machine Learning Engineer certification validates designing, building, and operationalizing models with MLOps.*

## The ML engineer role

The **Cloudera Machine Learning Engineer** designs, develops, and **operationalizes machine-learning models** on the platform — not just training a model in a notebook, but taking it all the way to **production** where it delivers predictions reliably. The role centers on **MLOps** (machine-learning operations) using **Cloudera AI** (formerly **Cloudera Machine Learning / CML**). The distinguishing skill is not only building models but making them **production-grade**: deployed, monitored, versioned, and maintained. The lab models the ML lifecycle.

## Cloudera AI

**Cloudera AI** (formerly CML) is CDP's **machine-learning platform** — a workspace where data scientists and ML engineers **develop, train, deploy, and serve** models. It provides:

- **Collaborative notebooks** (Python, R, etc.) for exploration and model development, on the platform's compute.
- **Model training** at scale, using the cluster's resources.
- **Model deployment and serving** — publishing models as **REST endpoints** for applications to call.
- **Access to governed platform data** — models train on the same [SDX-governed data (Chapter 2)](02-the-cloudera-data-platform.md) the rest of the platform uses.

Because it runs **on CDP**, Cloudera AI puts ML **next to the data** — no copying datasets to a separate ML environment, and with the platform's security and governance intact. The lab models the platform advantage.

## MLOps: development to production

**MLOps** applies DevOps discipline to machine learning — the lifecycle from experiment to reliable production service:

1. **Develop** — build and train a model in notebooks.
2. **Version** — track model versions, data, and experiments for reproducibility.
3. **Deploy** — publish the model as a served endpoint.
4. **Monitor** — watch the model in production for performance and **drift** (when real-world data diverges from training data and accuracy degrades).
5. **Retrain** — update the model as data and patterns change.

The gap MLOps closes is between a model that *works in a notebook* and one that *works reliably in production* — most ML value is lost in that gap, and MLOps is how the ML engineer closes it. Model **monitoring and drift detection** are especially critical: a deployed model silently degrades as the world changes. The lab models MLOps.

## The data-platform advantage

Doing ML **on the data platform** is the strategic point. Models need data — lots of it, governed and current. Running Cloudera AI on CDP means models **train and serve next to the governed data**, with SDX security applied, and with the data engineering and operations that feed them on the same platform. Compared to exporting data to a separate ML tool (losing governance, adding copies and latency), platform-native ML is more secure, more current, and more maintainable. This is Cloudera's ML thesis, and it pairs with the broader [AI-infrastructure skills (NVIDIA XLVI)](../../volume-046-nvidia-certifications/README.md) the shelf covers. The lab synthesizes.

## Hands-On Lab

Python models the MLOps lifecycle and drift. **Cost:** none.

### Lab 7.1 — MLOps: deploy, monitor for drift, retrain

**Objective:** Model the production ML lifecycle on the platform.

```bash
python3 - <<'EOF'
# an ML model's lifecycle on Cloudera AI, with production drift monitoring
STAGES = ["develop (notebook)", "version (track model+data)", "deploy (REST endpoint)",
          "monitor (accuracy + drift)", "retrain (as data shifts)"]
print("MLOps lifecycle on Cloudera AI (ML next to GOVERNED platform data):\n")
for i, s in enumerate(STAGES, 1):
    print(f"   {i}. {s}")
print()
# production monitoring: model accuracy degrades as data drifts
weeks = [("wk1", 0.94), ("wk4", 0.93), ("wk8", 0.88), ("wk12", 0.79)]
THRESHOLD = 0.85
print("Production monitoring — accuracy over time (data drift creeping in):")
for wk, acc in weeks:
    flag = "  <-- DRIFT: below threshold -> RETRAIN" if acc < THRESHOLD else ""
    print(f"   {wk:5} accuracy={acc:.2f}{flag}")
print(f"\n   threshold {THRESHOLD}: crossed at wk12 -> retrain on recent data, redeploy\n")
print("The ML Engineer OPERATIONALIZES models — not just training in a notebook, but the")
print("full MLOps lifecycle on CLOUDERA AI: develop -> version -> deploy (REST) -> MONITOR")
print("-> retrain. The critical part is PRODUCTION: a deployed model SILENTLY DEGRADES as")
print("real-world data drifts from training data (0.94 -> 0.79 here). Monitoring + drift")
print("detection catch it; retraining fixes it. Most ML value is lost in the notebook->")
print("production gap — MLOps closes it. And doing it ON CDP puts ML next to GOVERNED data")
print("(SDX intact, no copies), the Cloudera advantage over a separate ML tool.")
EOF
```

**Expected result:** The MLOps lifecycle (develop → version → deploy → monitor → retrain) and a production model whose accuracy drifts from 0.94 to 0.79, crossing the 0.85 threshold and triggering retraining. The ML-engineer lesson is that the role operationalizes models through the full MLOps lifecycle on Cloudera AI — the critical part being production monitoring for drift and retraining, since deployed models silently degrade — and doing ML on CDP keeps it next to governed data (SDX intact), the platform advantage.

**Negative test:** Deploying a model and assuming it stays accurate. Data drift degrades it silently; MLOps monitoring and drift detection with retraining are what keep a production model reliable, and running on the platform keeps governance and data current.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The ML-engineer role understood — designing, building, and operationalizing models on CDP.
- [ ] Cloudera AI (formerly CML) understood — notebooks, training, deployment, and serving on the platform.
- [ ] MLOps understood — the develop-to-production lifecycle, with monitoring and drift detection.
- [ ] The advantage of ML on the data platform recognized — next to governed data, with SDX intact.
