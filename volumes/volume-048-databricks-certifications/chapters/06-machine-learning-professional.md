# Chapter 06: Machine Learning Professional

## Learning Objectives

- Explain what the Machine Learning Professional certifies and how it extends the Associate.
- Summarize the exam-guide sections.
- Apply MLOps: experimentation, the model lifecycle, and deployment patterns.
- Monitor models for drift and manage the production lifecycle.
- Complete a per-topic walkthrough for each ML Professional area.

## Theory and Architecture

The **Databricks Certified Machine Learning Professional** validates **MLOps** —
taking models to production and operating them. Its exam guide covers
**experimentation** (advanced MLflow, reproducibility), **model lifecycle
management** (the registry, aliases, webhooks/automation), **model deployment**
(**batch**, **streaming**, and **real-time serving**), and **model monitoring**
(inference tables, **drift** detection, retraining). It assumes the Associate
foundation.

## Design Considerations

The professional owns the model **lifecycle**: rigorous experiment tracking,
promoting models through registry **aliases** (e.g., champion/challenger),
deploying via the right pattern (batch scoring, Structured Streaming, or **Model
Serving** endpoints), and **monitoring** for drift with inference tables and
Lakehouse Monitoring — triggering retraining when quality degrades. This is the
production discipline on top of the Associate's workflow.

## Implementation and Automation

The labs below use **MLflow registry**, **Model Serving**, and monitoring patterns
for each area — experimentation, lifecycle, the three deployment modes, and drift
monitoring.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
databricks.com/learn/certification > Machine Learning Professional > exam guide:
  - experimentation, model lifecycle management, deployment (batch/streaming/real-time),
    model monitoring (drift, inference tables)
```

Common pitfalls: promoting models by copying instead of **registry aliases**;
choosing the wrong **deployment mode** (real-time vs batch); and deploying without
**drift monitoring**.

## Security and Best Practices

Manage promotion with **registry aliases** and automation; pick the deployment mode
by latency need (batch for bulk, streaming for continuous, **Model Serving** for
real-time/low-latency); log predictions to **inference tables**; monitor **drift**
with Lakehouse Monitoring; and automate **retraining** on degradation. Govern
models in Unity Catalog.

## References and Knowledge Checks

- databricks.com: Machine Learning Professional exam guide; MLflow Model Registry, Model Serving, and Lakehouse Monitoring docs.

**Knowledge checks**

1. How do registry aliases support the model lifecycle?
2. When do you choose real-time serving vs batch scoring?
3. How do you detect and respond to model drift?

## Hands-On Lab

Per-topic walkthroughs — ML Professional areas. Run on the Databricks ML runtime.

**Shared prerequisites** — a Databricks ML workspace; `mlflow`; a registered model
(from Chapter 05). **Cost:** none (Free Edition where available).

### Lab 6.1 — Experimentation: compare and reproduce runs

**Objective:** Compare MLflow runs to select the best.

```python
import mlflow
runs = mlflow.search_runs(order_by=["metrics.auc DESC"])
best = runs.iloc[0]
print("best run:", best.run_id, "auc:", best["metrics.auc"])
```

**Expected result:** the best run by AUC from tracked experiments — the
experimentation rigor the Professional exam expects (comparable, reproducible).

**Negative test:** eyeball notebook outputs to pick a model; **search tracked
runs** for objective, reproducible selection.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Lifecycle: registry aliases (champion/challenger)

**Objective:** Promote a model version with an alias.

```python
from mlflow import MlflowClient
c = MlflowClient()
c.set_registered_model_alias("main.ml.churn_model", "champion", version=3)
# load for inference by alias:  models:/main.ml.churn_model@champion
```

**Expected result:** version 3 aliased `@champion`, loadable by alias — the
lifecycle-management pattern the exam tests.

**Negative test:** hard-code a version number in serving; use an **alias** so you
can promote without changing consumers.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Deployment: batch scoring

**Objective:** Score a batch with a registered model.

```python
import mlflow
model = mlflow.pyfunc.load_model("models:/main.ml.churn_model@champion")
scored = batch_df.withColumn("pred", model_udf(*feature_cols))  # or model.predict
```

**Expected result:** batch predictions written back to a table — the batch
deployment mode.

**Negative test:** stand up a real-time endpoint for a nightly bulk job; **batch
scoring** is cheaper for bulk — match the mode to the workload.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Deployment: real-time Model Serving

**Objective:** Describe a real-time serving endpoint.

```python
# Databricks Model Serving: a scalable REST endpoint for a registered model
# POST /serving-endpoints/churn/invocations  {"dataframe_records":[{...}]}
# Autoscaling, versioned, with request logging to inference tables.
```

**Expected result:** a real-time serving endpoint concept with request logging —
the low-latency deployment mode of the Professional exam.

**Negative test:** serve real-time predictions from a nightly batch table; use a
**Model Serving** endpoint for low-latency online inference.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.5 — Monitoring: inference tables and drift

**Objective:** Monitor a deployed model for drift.

```python
# Log inference to an inference table, then use Lakehouse Monitoring:
# - data drift (input distribution change) and prediction drift
# - quality metrics vs a baseline; alert when thresholds breach
```

**Expected result:** drift/quality monitoring over an inference table with alerts —
the monitoring area of the Professional exam.

**Negative test:** deploy and never monitor; models **drift** as data changes —
monitor and alert.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.6 — Automated retraining

**Objective:** Trigger retraining on drift.

```python
# Job pipeline: monitor -> if drift/quality breach -> retrain -> evaluate ->
#   register new version -> (if better) promote alias @champion. Automate via Jobs/webhooks.
```

**Expected result:** an automated retrain-and-promote loop — closing the MLOps
lifecycle the Professional exam certifies.

**Negative test:** retrain on a fixed schedule regardless of drift; **event-driven**
retraining (on degradation) is more efficient and timely.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Machine Learning Professional certifies MLOps on Databricks: rigorous
experimentation, model-lifecycle management with registry aliases, deployment
across batch/streaming/real-time serving, and drift monitoring with automated
retraining. It operationalizes what the Associate builds.

- [ ] I can summarize the ML Professional exam-guide areas.
- [ ] I can compare runs and promote models by alias.
- [ ] I can choose and describe batch, streaming, and real-time deployment.
- [ ] I can monitor drift and automate retraining.
- [ ] I completed Labs 6.1–6.6 including each negative test.
