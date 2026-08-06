# Chapter 06: Decisioning and Next-Best-Action

## Learning Objectives

- Explain Pega decisioning and the Customer Decision Hub.
- Describe Next-Best-Action — real-time, AI-driven decisions.
- Understand balancing customer relevance and business priority.
- Recognize the Decisioning Consultant and Data Scientist roles.

*Cert relevance: decisioning is a distinct Pega track (CPDC, Data Scientist, Lead Decisioning Architect).*

## Pega decisioning

Beyond case management, Pega has a powerful **decisioning** capability — **real-time, AI-driven decisions** about **customer engagement**. The **Customer Decision Hub (CDH)** is Pega's decisioning engine: for **every customer interaction** (a website visit, a call, an app session, an email), it decides — **in real time** — the **single best action** to take with that customer. This is Pega's **CRM/customer-engagement** crown jewel, distinct from the [case-management/BPM side (Ch 3)](03-case-management.md), and it has its own certification track: **Decisioning Consultant (CPDC)**, **Data Scientist**, and **Lead Decisioning Architect**. The lab models decisioning.

## Next-Best-Action

The core paradigm is **Next-Best-Action (NBA)** — for each customer, at each moment, determine the **next best action**: the offer, message, retention play, or service that is **best** for **both** the customer and the business, **right now**. NBA runs **in real time** across **all channels** (web, mobile, call center, email), so a customer gets a **consistent, relevant** experience wherever they interact. Instead of blasting everyone with the same campaign, NBA makes a **1:1** decision per customer per interaction. Next-Best-Action is Pega's signature decisioning concept. The lab models NBA.

## Balancing relevance and priority

The intelligence of NBA is **balancing multiple factors** to pick the best action:

- **Customer relevance / propensity** — how likely is the customer to want/accept this action? (predicted by **AI/ML models** — the [Data Scientist's, Ch 1](01-the-pega-program.md) work: adaptive and predictive models learning from behavior).
- **Business priority / value** — how valuable is this action to the business?
- **Eligibility and suitability** — is the customer **eligible** (rules), and is it **suitable/appropriate** (don't offer a loan to someone in hardship)?
- **Context** — the customer's current situation and channel.

NBA combines these — **arbitration** — to choose the one action that best serves the customer **and** the business, ethically. This balance (not just "sell the most") is what makes decisioning effective and responsible. The lab models arbitration.

## The Decisioning roles

The decisioning track has distinct roles:

- **Data Scientist** — builds the **predictive and adaptive models** (propensity, churn) that power NBA.
- **Decisioning Consultant (CPDC)** — designs the **Customer Decision Hub** strategy: the actions, eligibility, arbitration, and channels.
- **Lead Decisioning Architect** — the expert who architects enterprise decisioning (earned via [interview, Ch 1](01-the-pega-program.md), requiring both CPDC and Data Scientist).

Together they deliver **1:1 real-time customer engagement** at scale — a sophisticated capability that sets Pega apart in customer engagement. The lab synthesizes.

## Hands-On Lab

Python models Next-Best-Action arbitration. **Cost:** none.

### Lab 6.1 — Next-Best-Action arbitration per customer

**Objective:** See NBA balance relevance, priority, eligibility, and suitability.

```bash
python3 - <<'EOF'
# for a customer interaction, pick the NEXT BEST ACTION by arbitration
CUSTOMER = {"name": "Ana", "segment": "premium", "in_hardship": False, "channel": "mobile app"}
ACTIONS = [
  {"action": "premium-card-offer", "biz_value": 90, "propensity": 0.7, "eligible": True,  "suitable": True},
  {"action": "personal-loan",      "biz_value": 80, "propensity": 0.2, "eligible": True,  "suitable": True},
  {"action": "high-risk-invest",   "biz_value": 95, "propensity": 0.6, "eligible": True,  "suitable": False},  # unsuitable
  {"action": "savings-tips",       "biz_value": 10, "propensity": 0.8, "eligible": True,  "suitable": True},
]
def arbitrate(actions):
    scored = []
    for a in actions:
        if not (a["eligible"] and a["suitable"]):   # gate: must be eligible AND suitable
            continue
        # arbitration = propensity (customer relevance) x business value
        score = round(a["propensity"] * a["biz_value"], 1)
        scored.append((score, a["action"]))
    return sorted(scored, reverse=True)

print(f"Customer interaction: {CUSTOMER['name']} ({CUSTOMER['segment']}) on {CUSTOMER['channel']}\n")
print("Candidate actions -> arbitrate (relevance x business value, gated by eligibility + suitability):")
ranked = arbitrate(ACTIONS)
for score, action in ranked:
    print(f"   score {score:>5}  {action}")
print(f"   (high-risk-invest EXCLUDED: not SUITABLE — ethical guardrail)\n")
print(f"   NEXT BEST ACTION for {CUSTOMER['name']}: {ranked[0][1]}  -> deliver in real time, this channel\n")
print("NEXT-BEST-ACTION: for EACH customer, EACH interaction, pick the single BEST action in REAL")
print("TIME across ALL channels. Arbitration balances CUSTOMER RELEVANCE (propensity, from AI/ML")
print("models — the Data Scientist's work) x BUSINESS VALUE, GATED by ELIGIBILITY (rules) +")
print("SUITABILITY (don't push unsuitable/harmful actions — the high-risk-invest is excluded). It's")
print("1:1 engagement, not one-size-fits-all campaigns — and balancing customer + business (not just")
print("'sell the most') is what makes it effective + responsible. Pega's decisioning crown jewel (CDH).")
EOF
```

**Expected result:** For customer Ana, candidate actions arbitrated by propensity × business value and gated by eligibility and suitability — the high-risk investment excluded as unsuitable, and the premium-card offer chosen as the next best action delivered in real time. The decisioning lesson is that Next-Best-Action picks the single best action per customer per interaction in real time across all channels, balancing customer relevance (AI/ML propensity) with business value while enforcing eligibility and suitability — 1:1 responsible engagement, Pega's Customer Decision Hub crown jewel.

**Negative test:** Blasting every customer with the highest-business-value offer regardless of relevance or suitability. That ignores propensity (irrelevant offers) and suitability (pushing harmful products); NBA arbitrates relevance and value gated by eligibility and suitability, delivering the responsible 1:1 next best action.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Pega decisioning and the Customer Decision Hub understood — real-time decisions on customer engagement.
- [ ] Next-Best-Action understood — the single best action per customer per interaction across channels.
- [ ] Balancing customer relevance and business priority understood — arbitration gated by eligibility and suitability.
- [ ] The Decisioning roles understood — Data Scientist (models), Decisioning Consultant (strategy), Lead Decisioning Architect.
