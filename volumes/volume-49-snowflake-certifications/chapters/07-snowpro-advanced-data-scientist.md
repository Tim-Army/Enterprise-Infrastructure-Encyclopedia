# Chapter 07: SnowPro Advanced — Data Scientist

## Learning Objectives

- Explain what the SnowPro Advanced: Data Scientist certifies and its prerequisite.
- Summarize the exam-guide domains.
- Apply the ML workflow on Snowflake with Snowpark ML and Cortex.
- Prepare data and features and deploy models in-platform.
- Complete a per-topic walkthrough for each Data Scientist domain.

## Theory and Architecture

The **SnowPro Advanced: Data Scientist (DSA-C03)** validates machine learning on
Snowflake. It **requires SnowPro Core**. Its exam guide covers **data preparation
and feature engineering**, **model development** with **Snowpark ML** and Python,
**model deployment/operationalization** in Snowflake, and using **Cortex ML/AI
functions** (built-in forecasting, classification, and LLM functions).

## Design Considerations

The data scientist prepares features in SQL/Snowpark, trains with **Snowpark ML**
(scikit-learn-style, pushed into Snowflake compute), registers/deploys models in
the **model registry**, and uses **Cortex** for built-in ML (forecast/anomaly/
classification) and LLM functions — keeping data and compute in Snowflake.

## Implementation and Automation

The labs below use Snowpark ML and Cortex patterns for each domain — feature prep,
training, deployment, and built-in ML functions.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Advanced: Data Scientist (DSA-C03):
  - data prep/feature engineering, model development (Snowpark ML), deployment, Cortex ML/AI
  - requires SnowPro Core
```

Common pitfalls: exporting data to train externally (keep it in **Snowpark**);
ignoring **Cortex** built-ins when they solve the task; and not registering models.

## Security and Best Practices

Keep data in-platform with **Snowpark ML** (no export), engineer features
reproducibly, register models in the **model registry**, and use **Cortex ML/AI**
functions for forecasting/anomaly/LLM tasks where they fit. Govern training data
with RBAC and masking.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Advanced: Data Scientist exam guide; Snowpark ML and Cortex docs.

**Knowledge checks**

1. What does the Data Scientist exam require as a prerequisite?
2. Why train with Snowpark ML instead of exporting data?
3. What tasks do Cortex ML functions handle out of the box?

## Hands-On Lab

Per-topic walkthroughs — Data Scientist domains. Snowpark/Cortex on a free trial.

**Shared prerequisites** — a free Snowflake trial; Snowpark enabled. **Cost:**
none.

### Lab 7.1 — Data preparation and feature engineering

**Objective:** Engineer features in-platform.

```sql
CREATE TABLE features AS
SELECT id,
       amount,
       amount / NULLIF(AVG(amount) OVER (), 0) AS amount_ratio,
       DAYOFWEEK(order_date) AS dow
FROM demo_db.sales.orders;
```

**Expected result:** engineered features (ratio, day-of-week) computed in Snowflake
— the feature-engineering domain.

**Negative test:** export to pandas to engineer features; do it **in Snowflake**
(SQL/Snowpark) to scale and avoid movement.

**Cleanup:** `DROP TABLE IF EXISTS features;`

### Lab 7.2 — Model development with Snowpark ML

**Objective:** Describe training with Snowpark ML.

```python
# Snowpark ML (Python), runs in Snowflake:
# from snowflake.ml.modeling.ensemble import RandomForestClassifier
# model = RandomForestClassifier(...).fit(snowpark_df)  # training pushed down
```

**Expected result:** a Snowpark ML training pattern (scikit-style, pushed down) —
the model-development domain.

**Negative test:** pull all data to a laptop to train; **Snowpark ML** trains in
Snowflake compute — keep it in-platform.

**Cleanup:** none.

### Lab 7.3 — Model deployment / registry

**Objective:** Register and use a model in-platform.

```python
# Snowflake Model Registry: register a model, then run inference as a SQL/Snowpark call
# reg.log_model(model, model_name="churn"); model.run(df)  -> predictions in Snowflake
```

**Expected result:** a registered model callable for in-Snowflake inference — the
deployment/operationalization domain.

**Negative test:** serve predictions from an external service by shipping data out;
in-platform **model registry** inference keeps data governed.

**Cleanup:** none.

### Lab 7.4 — Cortex ML/AI functions

**Objective:** Use a built-in Cortex ML function.

```sql
SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', 'Summarize: quarterly revenue rose 12%.') AS summary;
-- Cortex also offers FORECAST, ANOMALY_DETECTION, CLASSIFICATION as SQL functions.
```

**Expected result:** a Cortex LLM completion (and the built-in ML functions) — the
Cortex domain the exam emphasizes.

**Negative test:** build a forecasting model from scratch when **Cortex FORECAST**
fits; use the built-in for standard tasks.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SnowPro Advanced: Data Scientist (requires Core) certifies ML on Snowflake:
in-platform feature engineering, model development with Snowpark ML, deployment via
the model registry, and Cortex ML/AI functions (forecast, anomaly, classification,
LLM) — keeping data and compute in Snowflake.

- [ ] I can engineer features in-platform.
- [ ] I can describe Snowpark ML training and the model registry.
- [ ] I can use Cortex ML/AI functions for standard tasks.
- [ ] I can keep data governed and in-platform throughout.
- [ ] I completed Labs 7.1–7.4 including each negative test.
