# Chapter 02: AI, watsonx, and Quantum Certifications

## Learning Objectives

- Map the AI portfolio: seven watsonx/AI certifications plus the Qiskit quantum developer credential.
- Understand what each watsonx product does — the certifications differ by product, not by buzzword.
- Complete walkthrough labs, including runnable Qiskit and prompt-engineering exercises.

## The AI portfolio

| Certification | Catalog code | Product focus |
|:---|:---|:---|
| Certified Artificial Intelligence v1 - Associate | Cert-C9008700 | Cross-product AI foundations |
| Certified watsonx Generative AI Engineer - Associate | Cert-C9007000 | watsonx.ai: selecting, customizing, prompting LLMs |
| Certified watsonx AI Assistant Engineer v1 - Professional | Cert-C9006900 | watsonx Assistant (conversational AI) |
| Certified watsonx Orchestrate AI Engineer v1 - Associate | Cert-C9009400 | watsonx Orchestrate (agentic skills/automation) |
| Certified watsonx Data Scientist - Associate | Cert-C9006400 | ML/DS workflows on watsonx |
| Certified watsonx Data Lakehouse Engineer v1 - Associate | Cert-C9007300 | watsonx.data (lakehouse, Presto/Iceberg) |
| Certified watsonx Governance Lifecycle Advisor v1 - Associate | Cert-C9008000 | watsonx.governance (model lifecycle/risk) |
| Certified Quantum Computation using Qiskit v2.X Developer - Associate | Cert-C9008400 | Qiskit circuits and execution |
| *Retiring soon:* watsonx Mainframe Modernization Architect v1 - Associate | Cert-C9007600 | watsonx Code Assistant for Z |

The grammar: **watsonx.ai** builds and prompts models, **watsonx.data** feeds them governed data, **watsonx.governance** audits them, **Assistant** and **Orchestrate** productize them. Exam questions test which product owns which job.

## Hands-On Lab

**Shared prerequisites** — Python 3.11+ with `pip`; free tiers/trials for watsonx where noted. **Cost:** none for the runnable labs.

### Lab 2.1 — Qiskit: a real circuit (Qiskit Developer)

**Objective:** Build and run the exam's bread-and-butter object — a Bell-state circuit.

```bash
pip install -q qiskit qiskit-aer
python3 - <<'EOF'
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
result = AerSimulator().run(transpile(qc, AerSimulator()), shots=1000).result()
print(result.get_counts())
EOF
```

**Expected result:** Counts split ~50/50 between `00` and `11` (e.g. `{'00': 507, '11': 493}`) — entanglement, measured; the Hadamard + CNOT + measure pattern the Qiskit exam drills, on the free local simulator.

**Negative test:** Remove the `cx` gate: counts spread across `00`/`01`/`10`/`11` — superposition without entanglement; the difference is exam material.

**Cleanup:** None.

### Lab 2.2 — Prompt engineering discipline (Generative AI Engineer)

**Objective:** Exercise the parameter vocabulary the watsonx.ai exam uses.

```text
watsonx.ai> Prompt Lab (trial): model=granite; try the same prompt at:
  temperature 0    -> deterministic, repeatable output
  temperature 1.2  -> varied, creative output
  max_new_tokens 20 vs 200 -> truncation vs full answer
  + a system prompt constraining format ("answer in one JSON object")
```

**Expected result:** Observable behavior change per parameter — decoding (greedy vs sampling), temperature, token limits, and system prompts are the exam's core vocabulary, and Prompt Lab makes each visible in isolation.

**Negative test:** Temperature 0 with a sampling-dependent instruction ("give me three different options") — the model repeats itself; parameters and prompts must agree.

**Cleanup:** Trial project cleanup as desired.

### Lab 2.3 — RAG shape (Generative AI Engineer / Data Scientist)

**Objective:** Build the retrieval-augmented pattern the exams describe, locally and free.

```bash
pip install -q sentence-transformers
python3 - <<'EOF'
from sentence_transformers import SentenceTransformer, util
docs = ["MQ channels connect queue managers.", "Qiskit builds quantum circuits.", "Db2 is a relational database."]
m = SentenceTransformer("all-MiniLM-L6-v2")
q = "How do I link two queue managers?"
scores = util.cos_sim(m.encode(q), m.encode(docs))[0]
best = docs[int(scores.argmax())]
print("retrieved:", best)
print("prompt to LLM: Answer using only this context:", best, "| Q:", q)
EOF
```

**Expected result:** The MQ document retrieved (highest cosine score) and a grounded prompt assembled — embed, retrieve, ground: the RAG loop watsonx.ai productizes with vector indexes, reduced to its testable essence.

**Negative test:** Ask a question none of the documents cover — the top score is low and the grounded answer should be "not in context"; retrieval quality gates generation quality.

**Cleanup:** None.

### Lab 2.4 — Lakehouse and governance concepts (Data Lakehouse / Governance Advisor)

**Objective:** Anchor the two data-side watsonx certifications.

```text
watsonx.data> engine: Presto queries over Iceberg tables on object storage; one catalog, many engines
watsonx.governance> register a model use case; track: owner, risk tier, evaluation metrics, approvals
```

**Expected result:** The lakehouse claim (open table format + interchangeable engines + cheap storage) and the governance claim (models tracked like change-controlled assets, with drift/quality monitors) stated concretely — each exam is its product's mental model plus operations.

**Negative test:** Try to place "prompt a model" in watsonx.data or "query Iceberg" in watsonx.governance — wrong product; the portfolio grammar assigns each job one home.

**Cleanup:** None (design).

### Lab 2.5 — Assistant vs Orchestrate (AI Assistant / Orchestrate Engineer)

**Objective:** Separate the two productized-AI certifications.

```text
assistant> build: dialog/actions answering user questions (conversational AI; intents, entities, actions)
orchestrate> build: skills that DO things (run an API, chain apps into an automation, agentic flows)
```

**Expected result:** The split: **Assistant converses, Orchestrate acts.** Exam scenarios hand you a requirement ("answer HR questions" vs "file the HR request across three systems") and expect the right product.

**Negative test:** Building a multi-system automation as a dialog tree — the wrong tool's exam will tell you why.

**Cleanup:** None (design).

## Summary and Completion Checklist

- [ ] Eight-credential AI portfolio mapped to products.
- [ ] Qiskit circuit built and run locally; RAG loop built locally.
- [ ] Prompt-parameter vocabulary exercised.
- [ ] watsonx product grammar (ai/data/governance/Assistant/Orchestrate) internalized.
