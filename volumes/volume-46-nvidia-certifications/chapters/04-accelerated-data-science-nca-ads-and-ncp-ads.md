# Chapter 04: Accelerated Data Science (NCA-ADS and NCP-ADS)

## Learning Objectives

- Explain the Accelerated Data Science credentials (Associate and Professional).
- Describe the RAPIDS ecosystem: cuDF, cuML, cuGraph, and Dask.
- Apply GPU-accelerated data processing and machine learning concepts.
- Understand scaling data science to multiple GPUs.
- Complete a per-topic walkthrough for each Accelerated Data Science area.

## Theory and Architecture

The **Accelerated Data Science** credentials validate using **GPUs to accelerate
the data-science workflow** — ETL, analytics, and machine learning — primarily
through **RAPIDS**:

- **NCA-ADS (Associate)** — foundational understanding of GPU-accelerated data
  science (RAPIDS, GPU dataframes, when acceleration helps). 50 questions / 60
  minutes.
- **NCP-ADS (Professional)** — deeper, applied acceleration: building and scaling
  accelerated pipelines and ML.

Key ecosystem: **cuDF** (GPU dataframes, pandas-like), **cuML** (GPU machine
learning, scikit-learn-like), **cuGraph** (graph analytics), and **Dask** for
multi-GPU/multi-node scaling.

## Design Considerations

The credentials reward knowing **when and how** GPU acceleration helps: large
dataframe operations, ML training/inference, and graph analytics benefit; tiny
datasets may not (transfer overhead). Learn the **pandas → cuDF** and
**scikit-learn → cuML** parallels (near drop-in APIs), and **Dask** for scaling
beyond one GPU's memory. The Professional adds pipeline design and optimization.

## Implementation and Automation

The labs below use the RAPIDS **API parallels** (shown as code you can run on a
GPU host with RAPIDS installed; the concepts apply anywhere) — cuDF, cuML,
cuGraph, and Dask scaling.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
nvidia.com/learn/certification > NCA-ADS / NCP-ADS:
  - RAPIDS (cuDF, cuML, cuGraph), GPU dataframes, when acceleration helps, scaling (Dask)
  - NCA associate (50 Q / 60 min); NCP professional (applied)
```

Common pitfalls: GPU-accelerating tiny datasets (transfer overhead dominates);
forgetting **GPU memory limits** (use Dask to spill/scale); and assuming every
pandas op has a cuDF equivalent (most, not all).

## Security and Best Practices

Accelerate where it pays (large data, heavy compute); keep data on the GPU across
steps to avoid transfer overhead; use **Dask-cuDF/Dask-cuML** to scale beyond one
GPU's memory; and validate that accelerated results match the CPU baseline.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCA-ADS and NCP-ADS blueprints; RAPIDS documentation (rapids.ai).

**Knowledge checks**

1. What are cuDF and cuML the GPU equivalents of?
2. When does GPU acceleration *not* help a data-science task?
3. How do you scale accelerated data science beyond one GPU?

## Hands-On Lab

Per-topic walkthroughs — RAPIDS API parallels. Run on a GPU host with RAPIDS
(concepts apply anywhere).

**Shared prerequisites** — a shell with `python3`; RAPIDS on a GPU host for
execution. **Cost:** none (concepts run without a GPU).

### Lab 4.1 — NCA-ADS: GPU dataframes with cuDF

**Objective:** See the pandas → cuDF parallel.

```python
# CPU (pandas)                 # GPU (cuDF) — near drop-in
import pandas as pd            # import cudf
df = pd.read_csv("big.csv")    # df = cudf.read_csv("big.csv")
df.groupby("k")["v"].mean()    # df.groupby("k")["v"].mean()   # runs on the GPU
```

**Expected result:** an identical groupby that runs on the GPU with cuDF — the
GPU-dataframe acceleration NCA-ADS tests.

**Negative test:** accelerate a 100-row CSV; transfer/setup overhead outweighs the
gain — accelerate **large** data.

**Cleanup:** none.

### Lab 4.2 — NCA-ADS: GPU machine learning with cuML

**Objective:** See the scikit-learn → cuML parallel.

```python
# CPU: from sklearn.cluster import KMeans
from cuml.cluster import KMeans          # GPU
km = KMeans(n_clusters=8).fit(X)         # trains on the GPU
labels = km.predict(X)
```

**Expected result:** a KMeans fit/predict on the GPU via cuML — the accelerated
ML NCA-ADS covers (near-identical API to scikit-learn).

**Negative test:** expect every sklearn estimator in cuML; most common ones exist,
not all — check cuML coverage.

**Cleanup:** none.

### Lab 4.3 — NCA-ADS: when acceleration helps

**Objective:** Decide whether to accelerate.

```bash
python3 - <<'PY'
def worth_gpu(rows, op_cost):
    return "YES" if rows > 1_000_000 and op_cost=="heavy" else "MAYBE/NO (overhead)"
for rows,op in [(50_000_000,"heavy"),(500,"heavy"),(2_000_000,"light")]:
    print(f"{rows:>12,} rows, {op:6} -> {worth_gpu(rows,op)}")
PY
```

**Expected result:** large + heavy → YES; small → overhead — the acceleration
decision NCA-ADS tests.

**Negative test:** GPU-accelerate everything reflexively; small/light tasks lose to
**transfer overhead** — decide by size and cost.

**Cleanup:** none.

### Lab 4.4 — NCP-ADS: scaling with Dask

**Objective:** Scale beyond one GPU's memory with Dask-cuDF.

```python
from dask_cuda import LocalCUDACluster
from dask.distributed import Client
import dask_cudf
client = Client(LocalCUDACluster())          # one worker per GPU
ddf = dask_cudf.read_csv("huge/*.csv")       # partitioned across GPUs
ddf.groupby("k")["v"].mean().compute()
```

**Expected result:** a multi-GPU groupby via Dask-cuDF — the scaling technique
NCP-ADS certifies.

**Negative test:** load a dataset larger than one GPU's memory into plain cuDF; it
OOMs — **Dask** partitions across GPUs/nodes.

**Cleanup:** none.

### Lab 4.5 — NCP-ADS: pipeline optimization

**Objective:** Keep data on the GPU across pipeline steps.

```bash
python3 - <<'PY'
print("Optimize: read -> transform (cuDF) -> train (cuML) all on GPU; avoid CPU round-trips.")
print("Each host<->device transfer costs time; chain GPU steps to keep data resident.")
PY
```

**Expected result:** the keep-data-on-GPU optimization — the pipeline design of
NCP-ADS.

**Negative test:** move data to CPU between every step; **transfers** dominate —
chain GPU operations.

**Cleanup:** none.

### Lab 4.6 — NCP-ADS: graph analytics (cuGraph)

**Objective:** Run a GPU graph algorithm.

```python
import cugraph, cudf
edges = cudf.DataFrame({"src":[0,1,2], "dst":[1,2,0]})
G = cugraph.Graph(); G.from_cudf_edgelist(edges, source="src", destination="dst")
cugraph.pagerank(G)     # GPU-accelerated PageRank
```

**Expected result:** a GPU PageRank via cuGraph — accelerated graph analytics in
the ADS ecosystem.

**Negative test:** run large-graph analytics on CPU NetworkX; **cuGraph** is
orders of magnitude faster for big graphs.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Accelerated Data Science credentials certify GPU-accelerated data science with
RAPIDS: **NCA-ADS** (foundational — cuDF, cuML, when acceleration helps) and
**NCP-ADS** (applied — pipeline optimization, cuGraph, and scaling with Dask). The
throughline is keeping large data on the GPU and scaling beyond one GPU.

- [ ] I can name the RAPIDS components and their CPU equivalents.
- [ ] I can decide when GPU acceleration is worthwhile.
- [ ] I can scale with Dask-cuDF and optimize GPU pipelines.
- [ ] I can run GPU graph analytics with cuGraph.
- [ ] I completed Labs 4.1–4.6 including each negative test.
