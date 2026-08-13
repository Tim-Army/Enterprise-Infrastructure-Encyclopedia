# Chapter 06: Machine Learning on Viya

## Learning Objectives

- Describe the Machine Learning Specialist credential and Model Studio.
- Build a supervised ML pipeline — data, transform, model, assess.
- Compare models and understand assessment metrics.
- Explain model deployment and where ML fits the Data Scientist path.

*Cert relevance: this is the AI & Machine Learning category — Machine Learning Specialist Using SAS Viya.*

## Machine learning in SAS Viya

Machine learning extends statistics ([Ch 5](05-statistical-analysis.md)) into **predictive modeling at scale** — training algorithms on data to predict outcomes (churn, fraud, demand) and letting the model **learn patterns** rather than being fully specified by hand. SAS Viya runs ML on the **in-memory CAS engine** ([Ch 2](02-the-sas-platform.md)) so it scales to large data, and provides **Model Studio** — a **visual pipeline** environment — for building it. The **Machine Learning Specialist Using SAS Viya** credential validates creating **supervised** ML models with pipelines: preparing data sources, building models, and assessing and deploying them.

The shift from statistics to ML is one of emphasis: statistics prizes **interpretability and inference** (why); ML prizes **predictive accuracy** (how well), often with more complex algorithms. SAS supports both, and a data scientist uses each where it fits. The lab builds an ML pipeline.

## The Model Studio pipeline

**Model Studio** builds ML as a **pipeline** — a flow of **nodes** from data to a scored model:

- **Data node** — the input data and its **roles** (which variable is the **target** to predict, which are inputs).
- **Transform / preprocessing nodes** — impute missing values, encode categories, handle outliers, engineer features.
- **Model nodes** — the algorithms: **decision tree**, **random forest**, **gradient boosting**, **neural network**, **logistic regression**, and more — often several in one pipeline to compare.
- **Assessment / comparison node** — evaluate the models on held-out data and **pick the champion**.

This visual pipeline makes the ML workflow **explicit and repeatable**: the same flow can be rerun, tuned, and deployed. Understanding the node types and the flow is the core of the ML Specialist exam. The lab builds a pipeline: data → transform → model → assess.

## Comparing models and metrics

ML always involves **choosing among models**, which requires **metrics** on **held-out** data (to avoid overfitting):

- **Classification** — accuracy, **precision/recall**, **ROC/AUC** (how well the model separates classes), the confusion matrix.
- **Regression** — error metrics (RMSE, MAE), R².
- **Champion/challenger** — train several models, compare on a **validation** partition, and select the **champion** (best on the metric that matters for the business).

The key discipline is **honest evaluation on data the model did not train on** — a model that memorizes the training data but fails on new data is worthless. Choosing the right metric (precision vs recall matters for fraud vs marketing) is part of the skill. The lab compares two models by validation accuracy. *(This evaluation rigor is the same as statistical model assessment in [Ch 5](05-statistical-analysis.md), extended to ML.)*

## Deployment and the Data Scientist path

A model delivers value only when **deployed** — put into production to **score** new data. SAS Viya supports publishing models (as analytic stores, code, or via APIs) so applications and processes can call them. Managing models in production — monitoring for **drift** (accuracy decaying as the world changes), retraining, and governance — is part of the modern ML lifecycle.

Machine learning is one of the credentials that composes into the **SAS Certified Data Scientist** ([Ch 8](08-data-scientist-and-administration.md)), alongside data curation, programming, and advanced analytics — because a data scientist must **prepare data, model, assess, and deploy** end to end. The ML Specialist is the modeling pillar of that path. The lab notes deployment.

## Hands-On Lab

Python models a Model Studio pipeline — data, transform, two models, and champion selection. **Cost:** none.

### Lab 6.1 — Build and compare an ML pipeline

**Objective:** Run a supervised pipeline (data → transform → model → assess) and pick a champion.

```bash
python3 - <<'EOF'
# supervised ML pipeline (Model Studio style): predict churn (1) from tenure + support_calls
TRAIN = [ # (tenure, support_calls, churn)
  (1,5,1),(2,4,1),(10,0,0),(12,1,0),(3,3,1),(8,1,0),(1,4,1),(15,0,0)]
VALID = [(2,5,1),(11,0,0),(4,2,1),(9,1,0)]   # held-out validation partition

# transform node: simple standardize (here, pass-through + a derived feature)
def transform(rows): return [(t, c, t - c, y) for (t,c,y) in rows]  # feature: tenure - calls

# two model nodes: (A) threshold rule, (B) a simple scoring model
def model_A(t,c,tc): return 1 if tc < 2 else 0        # churn if tenure-calls small
def model_B(t,c,tc): return 1 if (c >= 3 or t <= 3) else 0

def assess(model, rows):  # accuracy on held-out data
    correct = sum(1 for (t,c,tc,y) in rows if model(t,c,tc)==y)
    return correct/len(rows)

print("MODEL STUDIO PIPELINE — data -> transform -> models -> assess:\n")
tr, va = transform(TRAIN), transform(VALID)
print(f"   data: {len(TRAIN)} train, {len(VALID)} validation; target=churn; feature=tenure-calls")
accA, accB = assess(model_A, va), assess(model_B, va)
print(f"   model A (tenure-calls < 2): validation accuracy = {accA:.2f}")
print(f"   model B (calls>=3 or tenure<=3): validation accuracy = {accB:.2f}")
champion = "A" if accA >= accB else "B"
print(f"\n   CHAMPION (best on VALIDATION): model {champion}")
print(f"   deploy: publish champion to score new customers (monitor for drift, retrain)")
print()
print("A supervised PIPELINE flows data -> TRANSFORM (feature engineering) -> MODEL nodes")
print("(compare algorithms) -> ASSESS on a HELD-OUT validation partition -> pick the CHAMPION.")
print("Honest evaluation on data the model didn't train on prevents overfitting; the champion is")
print("DEPLOYED to score new data and monitored for drift. Building this is the ML Specialist cert.")
EOF
```

**Expected result:** A supervised pipeline that transforms features, trains two candidate models, evaluates both on a held-out validation partition, selects the champion by accuracy, and notes deployment. The lesson is machine learning in SAS Viya: build a Model Studio pipeline (data → transform → model → assess), compare models honestly on held-out data, pick a champion, and deploy it — the competency the Machine Learning Specialist credential validates.

**Negative test:** Choosing the model by its accuracy on the training data. A model that memorizes training data scores perfectly there but fails on new customers; comparing on a held-out validation partition is what selects a model that actually generalizes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] ML on Viya understood — predictive modeling at scale on CAS, built in Model Studio.
- [ ] The pipeline understood — data → transform → model → assess, with node types.
- [ ] Model comparison understood — metrics on held-out data and champion selection.
- [ ] Deployment and the Data Scientist path understood — scoring, drift/retraining, and ML as a Data Scientist pillar.

## See also

- [Chapter 05 — Statistical Analysis](05-statistical-analysis.md) — the statistics ML extends, and shared assessment rigor.
- [Chapter 08 — The Data Scientist Path and Viya Administration](08-data-scientist-and-administration.md) — how ML composes into the Data Scientist credential.
- [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) — ML on another in-memory analytics platform.
