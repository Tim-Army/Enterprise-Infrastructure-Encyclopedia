# Chapter 08: GitHub Copilot

## Learning Objectives

- Explain Copilot plans, features, and how it works.
- Apply prompt engineering for better suggestions.
- Use Copilot to help write and test code.
- Reason about privacy, content exclusions, and responsible AI.
- Complete a walkthrough for each Copilot topic.

## Theory and Architecture

**GitHub Copilot** is the AI pair programmer, and its certification covers using it effectively and
**responsibly**. Copilot provides **code completions** (inline suggestions as you type) and **Copilot
Chat** (conversational help, explanations, refactors, and tests) in the editor, CLI, and on GitHub. It
comes in **plans** — Copilot for Individuals, Business, and Enterprise — differing in management,
policy, and features. Getting good output depends on **prompt engineering**: clear context (open
relevant files, write descriptive comments/function names), specific instructions, and iterating. Copilot
helps across **developer use cases** — writing functions, explaining unfamiliar code, generating **tests**,
and fixing errors. Crucially, the exam covers **responsible AI and privacy**: **content exclusions**
(configuring files/repos Copilot must not use as context), how prompts and suggestions are **handled**
(data flow, retention settings for Business/Enterprise), and treating AI output as a **draft to review**,
never blindly trusted. This chapter teaches Copilot with hands-on walkthroughs.

## Design Considerations

Give Copilot **context** — open the relevant files, use descriptive names, and write a clear comment or
docstring stating intent. Iterate on prompts in **Chat**. Always **review** generated code for
correctness, security, and licensing — it is a draft. Configure **content exclusions** for sensitive
files/repos. Choose the **plan** (Business/Enterprise) that gives the policy and data controls your
organization needs.

## Implementation and Automation

The labs reason about plans/features, apply prompt engineering, use Copilot to draft a test, and reason
about content exclusions and privacy — the responsible, effective use the Copilot exam validates.

## Validation and Troubleshooting

Confirm Copilot use:

```text
Features: code completions (inline) + Copilot Chat (explain/refactor/test); editor/CLI/GitHub
Plans: Individual / Business / Enterprise (management, policy, data controls differ)
Prompt engineering: context (open files, names, comments) + specific instructions + iterate
Responsible AI: content exclusions; review output (draft, not truth); privacy/data handling
```

Common pitfalls: accepting Copilot output **without review** (bugs, insecure code, licensing); and not
configuring **content exclusions** for sensitive repositories.

## Security and Best Practices

Use Copilot **responsibly**: review every suggestion, configure **content exclusions** for sensitive
code, choose a plan with the right **data controls**, and keep humans accountable for shipped code. This
is responsible, privacy-aware AI on your own code. All work is authorized.

## Hands-On Lab

Copilot walkthroughs. **Shared prerequisites** — access to GitHub Copilot (or the concepts, modeled in
`python3`), an editor with Copilot, and `python3`. **Cost:** none (Copilot plan or free trial as
available).

### Lab 8.1 — Reason about plans and features

**Objective:** Match a plan and feature to a need.

```python
python3 - <<'PY'
plans = {
  "Individual": "personal use; completions + chat",
  "Business":   "org management, policy, content exclusions, no training on your code",
  "Enterprise": "Business + deeper GitHub integration, knowledge bases, more controls",
}
for plan, feats in plans.items(): print(f"{plan:11}: {feats}")
print("Features: inline completions + Copilot Chat (explain/refactor/test) across editor/CLI/GitHub")
PY
```

**Expected result:** the plans and features mapped — pick Business/Enterprise for org policy and data
controls.

**Negative test:** use Individual plan for a regulated org needing content exclusions and policy; choose
**Business/Enterprise**.

**Cleanup:** none.

### Lab 8.2 — Apply prompt engineering

**Objective:** Give Copilot the context to help.

```python
python3 - <<'PY'
weak   = "# do stuff"
strong = ("# Return the median of a list of numbers.\n"
          "# Handle an empty list by raising ValueError.\n"
          "def median(values: list[float]) -> float:")
print("WEAK prompt -> vague, likely wrong:\n", weak)
print("\nSTRONG prompt -> clear intent, types, edge case:\n", strong)
print("\nRule: context + specific instruction + edge cases -> better suggestions")
PY
```

**Expected result:** a strong prompt (clear intent, types, edge cases) versus a vague one — better
context yields better Copilot output.

**Negative test:** prompt with `# do stuff` and accept whatever appears; write a **descriptive** comment
and signature.

**Cleanup:** none.

### Lab 8.3 — Use Copilot to draft a test (then review)

**Objective:** Generate tests and verify them.

```python
# Copilot Chat: "write pytest tests for median(), including the empty-list ValueError"
# Review the generated test before trusting it:
import pytest
def median(values):
    if not values: raise ValueError("empty")
    s = sorted(values); n = len(s)
    return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2

def test_median_odd():   assert median([3,1,2]) == 2
def test_median_even():  assert median([1,2,3,4]) == 2.5
def test_median_empty():
    with pytest.raises(ValueError): median([])
```

```text
# run: pytest -q  ->  3 passed
```

**Expected result:** Copilot-drafted tests that you **review** and run — they pass, confirming the
behavior.

**Negative test:** ship Copilot-generated tests without running or reading them; **review and run** them
— AI output is a draft.

**Cleanup:** none.

### Lab 8.4 — Configure content exclusions and reason about privacy

**Objective:** Keep sensitive code out of Copilot's context.

```python
python3 - <<'PY'
exclusions = [ "secrets/**", "**/*.pem", "customer-data/**" ]
def excluded(path):
    import fnmatch
    return any(fnmatch.fnmatch(path, p) for p in exclusions)
for f in ["src/app.py", "secrets/keys.env", "customer-data/pii.csv"]:
    print(f"{f:24}: {'EXCLUDED from Copilot context' if excluded(f) else 'usable as context'}")
print("Business/Enterprise: content exclusions + data controls (no training on your code)")
PY
```

```text
src/app.py              : usable as context
secrets/keys.env        : EXCLUDED from Copilot context
customer-data/pii.csv   : EXCLUDED from Copilot context
```

**Expected result:** sensitive paths excluded from Copilot's context — privacy-aware configuration.

**Negative test:** let Copilot use secret and customer-data files as context; configure **content
exclusions** for them.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub Copilot provides inline completions and Copilot Chat across Individual, Business, and Enterprise
plans; effective use depends on prompt engineering (context, specificity, iteration) and on treating
output as a reviewable draft — used responsibly with content exclusions for sensitive code and the data
controls of the right plan.

- [ ] I can explain Copilot plans and features.
- [ ] I can apply prompt engineering.
- [ ] I can use Copilot to draft and then review tests.
- [ ] I can configure content exclusions and reason about privacy.
- [ ] I completed Labs 8.1–8.4 including each negative test.
