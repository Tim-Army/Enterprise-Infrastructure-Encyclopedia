# Chapter 05: Statistical Analysis

## Learning Objectives

- Describe SAS's statistical heritage and the Statistical Business Analyst credential.
- Apply descriptive and inferential statistics with SAS procedures.
- Build and interpret a linear regression model.
- Understand model assessment — fit, significance, and diagnostics.

*Cert relevance: this is the Advanced Analytics / Statistics category — the Statistical Business Analyst credential.*

## SAS's statistical heritage

SAS was built for **statistics**, and that heritage is its deepest strength. Where many tools bolt analytics onto a database or a dashboard, SAS has decades of **validated statistical procedures** trusted in **regulated** settings — clinical trials, banking risk, government research — where results must be **correct and defensible**. The **Statistical Business Analyst** credential (A00-240) validates the ability to apply statistics to business problems using SAS: describe data, test hypotheses, and build predictive models with sound method.

This chapter is where SAS's identity as an **analytics** platform (not just a programming or BI tool) is clearest. Statistical rigor — knowing which test applies, checking assumptions, interpreting results honestly — is the competency, and SAS provides the procedures. The lab builds a regression and assesses it.

## Descriptive and inferential statistics

Statistics in SAS runs from **describing** data to **inferring** from it:

- **Descriptive** — summarize what the data shows: means, standard deviations, distributions, correlations (`PROC MEANS`, `PROC UNIVARIATE`, `PROC CORR`). This characterizes the data before modeling.
- **Inferential** — draw conclusions **beyond** the sample: hypothesis tests (t-tests, ANOVA via `PROC TTEST`, `PROC ANOVA`/`PROC GLM`) ask whether an observed difference is **statistically significant** or likely due to chance.

The discipline is using the **right** procedure for the question and the data, and reading **p-values and confidence intervals** correctly — significance is about evidence, not certainty. Descriptive first (understand the data), then inferential (test claims). The lab computes descriptive stats and a correlation.

## Regression modeling

The workhorse of predictive statistics is **regression** — modeling a **response** variable as a function of **predictors**:

- **Linear regression** (`PROC REG`, `PROC GLM`) — predict a **continuous** outcome (sales from advertising spend); estimate the **coefficients** (the effect of each predictor) and the **intercept**.
- **Logistic regression** (`PROC LOGISTIC`) — predict a **binary** outcome (will the customer churn?) as a probability.

A fitted model gives you **coefficients** (how much the response changes per unit of a predictor), their **significance** (are they real effects?), and a way to **predict** new cases. Building a regression — choosing predictors, fitting, and interpreting the coefficients — is central to the Statistical Business Analyst work. The lab fits a linear regression by least squares.

## Model assessment

A model you cannot assess is not trustworthy, so statistics emphasizes **evaluation**:

- **Fit** — how well the model explains the data (**R²** — the fraction of variance explained; residual error).
- **Significance** — are the coefficients and the overall model **statistically significant** (p-values)? A predictor that is not significant may not belong.
- **Diagnostics** — check the **assumptions** (linearity, constant variance, normal residuals, no undue influence from outliers); violated assumptions make conclusions unreliable.
- **Validation** — assess on **held-out** data to guard against overfitting (the bridge to machine learning, [Ch 6](06-machine-learning-on-viya.md)).

Honest assessment — reporting fit, significance, and assumption checks — is what separates sound analytics from a plausible-looking but wrong model. This rigor is exactly what SAS certifications in statistics test. The lab computes R² and interprets the fit. *(This assessment discipline carries directly into ML model evaluation in [Ch 6](06-machine-learning-on-viya.md).)*

## Hands-On Lab

Python models descriptive stats, a linear regression by least squares, and assessment. **Cost:** none.

### Lab 5.1 — Fit and assess a linear regression

**Objective:** Compute descriptive statistics, fit a regression, and assess fit and significance.

```bash
python3 - <<'EOF'
# predict sales from advertising spend (like PROC REG)
DATA = [(1,20),(2,40),(3,50),(4,70),(5,80)]   # (ad_spend, sales)
xs = [d[0] for d in DATA]; ys = [d[1] for d in DATA]
n = len(DATA)

# descriptive (PROC MEANS / PROC CORR)
mean_x, mean_y = sum(xs)/n, sum(ys)/n
def corr(xs, ys):
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    sx = sum((x-mx)**2 for x in xs)**0.5; sy = sum((y-my)**2 for y in ys)**0.5
    return cov/(sx*sy)
print("DESCRIPTIVE (PROC MEANS / CORR):")
print(f"   mean ad_spend={mean_x}, mean sales={mean_y}, correlation={corr(xs,ys):.3f}")

# linear regression by least squares (PROC REG): sales = b0 + b1*ad_spend
sxx = sum((x-mean_x)**2 for x in xs)
sxy = sum((x-mean_x)*(y-mean_y) for x,y in zip(xs,ys))
b1 = sxy/sxx; b0 = mean_y - b1*mean_x
print(f"\nREGRESSION (PROC REG): sales = {b0:.1f} + {b1:.1f} * ad_spend")

# model assessment: R^2 (fraction of variance explained)
pred = [b0 + b1*x for x in xs]
ss_res = sum((y-p)**2 for y,p in zip(ys,pred))
ss_tot = sum((y-mean_y)**2 for y in ys)
r2 = 1 - ss_res/ss_tot
print(f"\nASSESSMENT: R-squared = {r2:.3f} (fraction of variance explained)")
print(f"   predict sales at ad_spend=6: {b0 + b1*6:.1f}")
print(f"   interpretation: each +1 ad_spend -> +{b1:.1f} sales; model explains {r2*100:.1f}% of variance")
print()
print("DESCRIPTIVE stats (mean, correlation) characterize the data; a least-squares REGRESSION")
print("estimates coefficients (each +1 ad_spend -> +b1 sales); ASSESSMENT reports R-squared (fit)")
print("and lets you predict. Right method + honest assessment (fit, significance, assumptions) is")
print("SAS's statistical rigor — the Statistical Business Analyst competency.")
EOF
```

**Expected result:** Descriptive statistics and a correlation, a fitted linear regression (intercept and slope by least squares), an R² fit assessment, and a prediction. The lesson is statistical analysis in SAS: describe the data, fit a model (regression) with sound method, and assess it honestly (fit, significance, assumptions) — the rigorous analytics the Statistical Business Analyst credential validates.

**Negative test:** Reporting a regression's predictions without checking fit, significance, or assumptions. A poorly fitting or assumption-violating model looks authoritative but misleads; assessing R², significance, and diagnostics is what makes a statistical conclusion trustworthy.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SAS's statistical heritage understood — validated procedures for regulated, rigorous analytics.
- [ ] Descriptive and inferential statistics understood — summarize the data, then test claims with the right procedure.
- [ ] Regression understood — linear and logistic models, coefficients, and prediction.
- [ ] Model assessment understood — fit (R²), significance, diagnostics, and validation.

## See also

- [Chapter 04 — Preparing and Curating Data](04-preparing-and-curating-data.md) — the clean data statistics requires.
- [Chapter 06 — Machine Learning on Viya](06-machine-learning-on-viya.md) — where statistics extends into predictive ML.
- [Chapter 03 — SAS Programming Foundations](03-sas-programming-foundations.md) — the PROCs that run these analyses.
