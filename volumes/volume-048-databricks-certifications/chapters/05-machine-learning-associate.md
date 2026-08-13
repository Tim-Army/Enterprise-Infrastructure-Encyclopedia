# Chapter 05: Machine Learning Associate

## Learning Objectives

- Explain what the Machine Learning Associate certifies and its exam format.
- Summarize the exam-guide sections.
- Apply the ML workflow on Databricks: MLflow, AutoML, and the Feature Store.
- Scale ML with Spark ML and distributed training.
- Complete a per-topic walkthrough for each ML Associate area.

## Theory and Architecture

The **Databricks Certified Machine Learning Associate** validates using Databricks
for the ML workflow: **Databricks ML** and clusters, **MLflow** (experiment
tracking and the model registry), **AutoML**, the **Feature Store / Feature
Engineering in Unity Catalog**, and **Spark ML** for scaling. Its exam guide covers
Databricks Machine Learning basics, ML workflows (data prep, training, evaluation),
Spark ML, and scaling/deployment fundamentals.

## Design Considerations

The associate ML practitioner runs the end-to-end workflow on Databricks: prepare
features (Feature Store), train and **track with MLflow**, use **AutoML** for
baselines, evaluate, and register models. Master MLflow tracking/registry, the
Feature Store, and when to use **Spark ML** (distributed) vs single-node
libraries. This is the foundation for the ML Professional exam.

## Implementation and Automation

The labs below use **MLflow**, **AutoML**, the **Feature Store**, and **Spark ML**
patterns you can run on Free/Community Edition (with the ML runtime).

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
databricks.com/learn/certification > Machine Learning Associate > exam guide:
  - Databricks ML, ML workflows, MLflow, AutoML, Feature Store, Spark ML, scaling
```

Common pitfalls: not **tracking** runs with MLflow (you can't compare/reproduce);
confusing the **Feature Store** with a plain table; and using single-node libs when
data needs **Spark ML**.

## Security and Best Practices

Track every experiment with **MLflow** (params, metrics, artifacts); register
models in the **MLflow Model Registry / Unity Catalog**; centralize features in the
**Feature Store** for reuse and consistency (avoid training/serving skew); and use
**Spark ML** or distributed training when data exceeds one node.

## References and Knowledge Checks

- databricks.com: Machine Learning Associate exam guide; MLflow, AutoML, and Feature Engineering docs.

**Knowledge checks**

1. What does MLflow tracking record, and why?
2. What problem does the Feature Store solve?
3. When do you use Spark ML instead of a single-node library?

## Hands-On Lab

Per-topic walkthroughs — ML Associate areas. Run on the Databricks ML runtime
(Free/Community Edition).

**Shared prerequisites** — a Databricks ML cluster; `mlflow`, `scikit-learn`,
PySpark. **Cost:** none (Free Edition).

### Lab 5.1 — ML workflow: train and track with MLflow

**Objective:** Train a model and log it with MLflow.

```python
import mlflow, mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", model.score(X_test, y_test))
    mlflow.sklearn.log_model(model, "model")
```

**Expected result:** a tracked MLflow run with params, a metric, and a logged model
— the reproducible ML workflow the exam centers on.

**Negative test:** train without logging; you cannot compare or reproduce runs —
always track with **MLflow**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — AutoML: baseline model

**Objective:** Generate a baseline with AutoML.

```python
from databricks import automl
summary = automl.classify(dataset=train_df, target_col="churn", timeout_minutes=10)
# AutoML produces trials, a best model, and an editable notebook
```

**Expected result:** an AutoML run yielding a best model and a reproducible
notebook — the AutoML area of the exam.

**Negative test:** hand-tune from scratch before a baseline; **AutoML** gives a
fast, reproducible baseline to beat.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Feature Store / Feature Engineering

**Objective:** Create and use a feature table.

```python
from databricks.feature_engineering import FeatureEngineeringClient
fe = FeatureEngineeringClient()
fe.create_table(name="main.ml.customer_features", primary_keys=["id"], df=features_df)
# Reuse the same features for training AND serving -> no skew
```

**Expected result:** a governed feature table reusable for training and serving —
the Feature Store area (prevents training/serving skew).

**Negative test:** compute features differently in training vs serving; the
**Feature Store** guarantees consistency — use it for both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Spark ML: scale training

**Objective:** Train a distributed model with Spark ML.

```python
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
va = VectorAssembler(inputCols=["f1","f2","f3"], outputCol="features")
train = va.transform(spark_df)
model = LogisticRegression(labelCol="label").fit(train)
```

**Expected result:** a Spark ML model trained on a Spark DataFrame — distributed
training for data beyond one node (the scaling area).

**Negative test:** `collect()` a huge dataset to pandas for training; it OOMs —
use **Spark ML** to train in a distributed way.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.5 — Model evaluation

**Objective:** Evaluate with appropriate metrics.

```python
from pyspark.ml.evaluation import BinaryClassificationEvaluator
auc = BinaryClassificationEvaluator(labelCol="label").evaluate(model.transform(test))
print("AUC:", auc)
```

**Expected result:** an AUC (or task-appropriate metric) — the evaluation the exam
expects (choose the metric for the problem).

**Negative test:** use accuracy on an imbalanced dataset; prefer **AUC/precision/
recall** — match the metric to the problem.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.6 — Register and stage a model

**Objective:** Register a model for lifecycle management.

```python
mlflow.register_model("runs:/<run_id>/model", "main.ml.churn_model")
# Manage versions/aliases (e.g., @champion) in Unity Catalog Model Registry
```

**Expected result:** a registered, versioned model in the Unity Catalog Model
Registry — the model-management area of the exam.

**Negative test:** copy model files around by hand; the **Model Registry** versions
and governs them — register instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Machine Learning Associate certifies the ML workflow on Databricks: MLflow
tracking and the registry, AutoML baselines, the Feature Store (no training/serving
skew), Spark ML for scale, and evaluation. It is the foundation for the ML
Professional exam.

- [ ] I can summarize the ML Associate exam-guide areas.
- [ ] I can train and track a model with MLflow.
- [ ] I can use AutoML and the Feature Store.
- [ ] I can scale with Spark ML and register a model.
- [ ] I completed Labs 5.1–5.6 including each negative test.
