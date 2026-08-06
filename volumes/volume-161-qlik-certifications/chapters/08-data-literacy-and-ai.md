# Chapter 08: Data Literacy and AI

## Learning Objectives

- Explain data literacy and the Data Literacy Qualification.
- Describe Insight Advisor and augmented analytics.
- Understand Qlik AutoML and Qlik Answers (generative AI).
- Recognize Qlik's AI direction and the data-integration side.

*Cert relevance: the Data Literacy Qualification and AI capabilities round out the Qlik program.*

## Data literacy

Qlik champions **data literacy** — the ability to **read, work with, analyze, and communicate with data** — as a discipline in its own right, and offers the **Data Literacy Qualification** ([Chapter 1](01-the-qlik-program.md)): a **non-technical, product-agnostic** credential (30 questions, 1 hour) measuring these fundamental skills, independent of any tool. The premise is that analytics technology only delivers value if people can **interpret and act on** data — a beautiful dashboard is useless to someone who cannot read it. Data literacy covers interpreting requirements, understanding and transforming data, reading visualizations, analyzing results, acting on them, and fostering a data-informed culture. It is Qlik's recognition that the human skill matters as much as the tool. The lab models data-literacy reasoning.

## Insight Advisor: augmented analytics

**Insight Advisor** is Qlik's **augmented-analytics** assistant — using AI to **help users find insights** without manually building every chart. It can **generate visualizations and insights automatically** from the data, answer **natural-language** questions ("show me sales by region"), and surface relationships and anomalies the user might miss. Augmented analytics lowers the barrier to analysis: a business user asks a question in plain language, and Insight Advisor produces the relevant chart. This complements the [Business Analyst's (Ch 5)](05-business-analyst.md) manual craft with AI assistance, broadening who can get value from data. The lab models augmented analytics.

## Qlik AutoML and Qlik Answers

Qlik extends into **AI/ML** and **generative AI**:

- **Qlik AutoML** — **no-code machine learning**: business teams build **predictive models** (e.g., predict customer churn, forecast sales) and generate predictions **without writing code**, then bring those predictions into Qlik analytics. It democratizes predictive analytics.
- **Qlik Answers** — a **generative-AI knowledge assistant**: ask questions in natural language and get AI-generated answers drawing on your organization's **unstructured** content (documents, knowledge bases), extending analytics beyond structured data into a conversational, GenAI experience.

Together these move Qlik from **descriptive** analytics (what happened) toward **predictive** (what will happen) and **generative** (ask anything) — the industry's AI direction. The lab models the AI progression.

## The data-integration side

Analytics needs **data**, and Qlik also provides **data integration and quality** capabilities — especially since Qlik's **acquisition of Talend (2023)**, giving it a full **data integration** portfolio (**Qlik Talend**) for moving, transforming, and governing data across sources into the analytics layer. This means Qlik spans the pipeline from **integrating and preparing** data through **analyzing** it — the [Data Architect's (Ch 4)](04-data-architect.md) loading is one part, and the broader Qlik Talend integration/quality tooling is the enterprise-scale extension. For a certification candidate, the takeaway is that Qlik is a **full data-to-insight platform**, not only visualization. The lab synthesizes.

## Hands-On Lab

Python models data literacy and the AI progression. **Cost:** none.

### Lab 8.1 — Data literacy and the descriptive→predictive→generative progression

**Objective:** See data-literacy reasoning and Qlik's AI capabilities.

```bash
python3 - <<'EOF'
# 1) data literacy: reading a visualization critically (not just accepting it)
print("DATA LITERACY — read/analyze/communicate with data (product-agnostic):\n")
observation = {"claim": "Sales up 200% this month!", "detail": "from 1 sale to 3 sales (tiny base)"}
print(f"   chart claims: '{observation['claim']}'")
print(f"   LITERATE reading: {observation['detail']} -> % is misleading on a tiny base; question it")
print("   -> data literacy = interpret requirements, question visualizations, act on VALID insight\n")

# 2) the AI progression: descriptive -> predictive -> generative
STAGES = [
  ("DESCRIPTIVE", "Qlik Sense + Insight Advisor", "what happened / what's related (augmented: NL query auto-builds charts)"),
  ("PREDICTIVE",  "Qlik AutoML (no-code ML)",     "what WILL happen (predict churn/forecast, no code)"),
  ("GENERATIVE",  "Qlik Answers (GenAI)",         "ask anything in NL over your unstructured content"),
]
print("Qlik's AI progression (descriptive -> predictive -> generative):")
for stage, tool, what in STAGES:
    print(f"   {stage:11} [{tool:28}] {what}")
print()
# 3) full data-to-insight platform (incl. integration via Talend acq. 2023)
print("Full data-to-insight platform:")
print("   INTEGRATE (Qlik Talend — data integration + quality, since 2023 Talend acquisition)")
print("   -> PREPARE (Data Architect load script) -> ANALYZE (Business Analyst apps + associative)")
print("   -> AUGMENT/PREDICT/GENERATE (Insight Advisor / AutoML / Qlik Answers)\n")
print("DATA LITERACY (the product-agnostic Qualification) = the human skill that makes analytics")
print("valuable: read, analyze, question, communicate, ACT. Qlik's AI moves from DESCRIPTIVE")
print("(Insight Advisor augmented analytics + NL) to PREDICTIVE (AutoML no-code ML) to GENERATIVE")
print("(Qlik Answers GenAI). And Qlik spans INTEGRATE->PREPARE->ANALYZE (Qlik Talend, acq. 2023)")
print("— a full data-to-insight platform, not just visualization.")
EOF
```

**Expected result:** A data-literacy reading that questions a misleading "+200%" claim (1→3 sales on a tiny base), and Qlik's AI progression from descriptive (Insight Advisor augmented analytics/NL) to predictive (AutoML no-code ML) to generative (Qlik Answers GenAI), plus the full integrate→prepare→analyze platform (Qlik Talend since 2023). The lesson is that data literacy is the human skill that makes analytics valuable, and Qlik extends from descriptive to predictive to generative AI while spanning data integration through insight — a full data-to-insight platform.

**Negative test:** Accepting a striking statistic (like +200%) at face value, or assuming Qlik is only visualization. Data literacy means questioning misleading numbers, and Qlik spans integration (Qlik Talend), prediction (AutoML), and generative AI (Qlik Answers) — not just charts.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Data literacy understood — reading, working with, analyzing, and communicating with data; the product-agnostic Qualification.
- [ ] Insight Advisor understood — augmented analytics with auto-generated insights and natural-language queries.
- [ ] Qlik AutoML and Qlik Answers understood — no-code ML and generative-AI knowledge assistance.
- [ ] Qlik's AI direction and the data-integration side (Qlik Talend) recognized — a full data-to-insight platform.
