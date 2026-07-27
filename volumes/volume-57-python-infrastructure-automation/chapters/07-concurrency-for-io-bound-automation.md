# Chapter 07: Concurrency for I/O-bound Automation

## Learning Objectives

- Explain why infra automation is I/O-bound and how concurrency helps.
- Parallelize with `concurrent.futures`.
- Write async I/O with `asyncio`.
- Bound concurrency to avoid overwhelming targets.
- Complete a walkthrough for each concurrency skill.

## Theory and Architecture

Infrastructure automation is overwhelmingly **I/O-bound** — waiting on API calls, SSH
sessions, and file operations, not CPU. Running these **concurrently** collapses total
time (100 hosts polled in parallel finish in about the time of the slowest one). Python
offers **`concurrent.futures.ThreadPoolExecutor`** (simple thread-based fan-out, ideal
for I/O despite the GIL, since threads release it while waiting) and **`asyncio`**
(single-threaded cooperative concurrency with `async`/`await`, scaling to thousands of
connections). For **CPU-bound** work you'd use processes, but that is rare in ops.

## Design Considerations

Use a **ThreadPoolExecutor** for straightforward parallel I/O over a bounded worker
count; use **`asyncio`** when a library is async-native or you need very high fan-out.
Always **bound concurrency** (pool size / semaphore) so you don't overwhelm the target or
hit rate limits.

## Implementation and Automation

The labs use ThreadPoolExecutor, asyncio, and a concurrency bound.

## Validation and Troubleshooting

Confirm the tools:

```text
Threads: concurrent.futures.ThreadPoolExecutor(max_workers=N).map(fn, items).
Async: async def + await; asyncio.run(main()); asyncio.gather(*tasks).
Bound: pool size or asyncio.Semaphore(N) to cap in-flight work.
```

Common pitfalls: unbounded fan-out (rate-limit/overload); and using threads for
**CPU-bound** work (the GIL serializes it — use processes).

## Security and Best Practices

Parallelize **I/O** with a **bounded** pool/semaphore, keep worker functions
**thread-safe** (no shared mutable state without locks), and respect target **rate
limits**. Reserve processes for genuinely CPU-bound tasks.

## Hands-On Lab

Concurrency walkthroughs. **Shared prerequisites** — Python 3.12+. **Cost:** none.

### Lab 7.1 — Parallel with ThreadPoolExecutor

**Objective:** Fan out an I/O task across threads.

```python
import concurrent.futures, time
def poll(host):
    time.sleep(0.2)   # simulate I/O
    return f"{host}:ok"
hosts = [f"h{i}" for i in range(10)]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(poll, hosts))
print(len(results))   # 10 (in ~0.4s, not 2s)
```

**Expected result:** **10** results in roughly the time of two batches — parallel I/O.

**Negative test:** poll hosts in a serial loop; 10 × 0.2s = **2s** vs ~0.4s parallel —
fan out I/O.

**Cleanup:** none.

### Lab 7.2 — Async I/O with asyncio

**Objective:** Run coroutines concurrently.

```python
import asyncio
async def poll(host):
    await asyncio.sleep(0.2)
    return f"{host}:ok"
async def main():
    return await asyncio.gather(*(poll(f"h{i}") for i in range(10)))
print(len(asyncio.run(main())))   # 10
```

**Expected result:** **10** results via cooperative concurrency — the async model.

**Negative test:** call `await` outside an event loop; async code needs
**`asyncio.run`**/a loop — run it properly.

**Cleanup:** none.

### Lab 7.3 — Bound concurrency with a semaphore

**Objective:** Cap in-flight async work.

```python
import asyncio
sem = asyncio.Semaphore(3)
async def poll(host):
    async with sem:                 # at most 3 concurrent
        await asyncio.sleep(0.2)
        return host
async def main():
    return await asyncio.gather(*(poll(f"h{i}") for i in range(9)))
print(len(asyncio.run(main())))     # 9, max 3 at a time
```

**Expected result:** **9** results with at most **3 concurrent** — a bounded fan-out.

**Negative test:** launch 1000 requests unbounded; you **hit rate limits/overload** — cap
with a semaphore/pool.

**Cleanup:** none.

### Lab 7.4 — Choose threads vs processes

**Objective:** State the right tool per workload.

```python
# I/O-bound (API/SSH/file waits): threads or asyncio (GIL released during I/O).
# CPU-bound (hashing/parsing huge data): ProcessPoolExecutor (bypass the GIL).
print("I/O -> threads/asyncio ; CPU -> processes")
```

**Expected result:** the correct mapping — the right concurrency model per workload.

**Negative test:** use threads for CPU-bound work; the **GIL** serializes it — use
**processes** for CPU.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Infra automation is I/O-bound, so concurrency (ThreadPoolExecutor or asyncio) collapses
total time — bounded to respect targets. Threads/asyncio suit I/O; processes suit
CPU-bound work. This chapter fanned out with threads and asyncio and bounded it.

- [ ] I can parallelize I/O with ThreadPoolExecutor.
- [ ] I can run coroutines with asyncio.
- [ ] I can bound concurrency with a semaphore.
- [ ] I can choose threads vs processes correctly.
- [ ] I completed Labs 7.1–7.4 including each negative test.
