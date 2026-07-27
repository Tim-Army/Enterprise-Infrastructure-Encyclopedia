# Chapter 07: Concurrency and Async

## Learning Objectives

- Explain Rust's "fearless concurrency".
- Spawn threads and share work.
- Communicate with channels.
- Write async I/O with tokio.
- Complete a walkthrough for each concurrency skill.

## Theory and Architecture

Rust's ownership rules extend to concurrency, giving **"fearless concurrency"**: the
compiler prevents **data races** at compile time via the **`Send`** (safe to move between
threads) and **`Sync`** (safe to share by reference) marker traits. For CPU parallelism you
**spawn threads** (`std::thread`) and coordinate with **channels** (`std::sync::mpsc`) or
shared state behind **`Arc<Mutex<T>>`**. For high-concurrency **I/O** (network services,
many connections) the ecosystem uses **async/await** on a runtime — most commonly
**`tokio`** — which multiplexes thousands of tasks on a few threads. Because the compiler
enforces thread-safety, concurrent Rust that compiles is free of data races.

## Design Considerations

Use **threads + channels** for CPU-parallel work and message passing; use **`Arc<Mutex>`**
for shared mutable state. For I/O-bound, high-fan-out work (an agent polling many endpoints)
use **async/tokio**. Let `Send`/`Sync` errors guide you to safe sharing.

## Implementation and Automation

The labs spawn threads, use a channel, share state, and run an async task.

## Validation and Troubleshooting

Confirm the model:

```text
Fearless concurrency via Send/Sync (compile-time race prevention).
Threads: std::thread::spawn. Channels: mpsc. Shared state: Arc<Mutex<T>>.
Async I/O: async/await on tokio (#[tokio::main]).
```

Common pitfalls: sharing mutable state without `Arc<Mutex>` (won't compile — good); and
using threads for massive I/O fan-out where **async** scales better.

## Security and Best Practices

Pass messages with **channels** where possible, guard shared state with **`Arc<Mutex>`**,
use **async/tokio** for high-concurrency I/O, and trust the compiler's **Send/Sync**
checks. Keep locked sections short.

## Hands-On Lab

Concurrency walkthroughs. **Shared prerequisites** — cargo (`cargo new conc && cd conc`;
`cargo add tokio --features full` for the async lab). **Cost:** none.

### Lab 7.1 — Spawn threads

**Objective:** Run work on multiple threads.

```rust
fn main() {
    let handles: Vec<_> = (0..4).map(|i| std::thread::spawn(move || i * 10)).collect();
    let sums: Vec<i32> = handles.into_iter().map(|h| h.join().unwrap()).collect();
    println!("{:?}", sums);   // [0, 10, 20, 30]
}
```

**Expected result:** `[0, 10, 20, 30]` — parallel thread results joined.

**Negative test:** capture a non-`Send` value in a thread closure; the compiler **rejects**
it — that prevents races.

**Cleanup:** none.

### Lab 7.2 — Channels

**Objective:** Send results over a channel.

```rust
use std::sync::mpsc;
fn main() {
    let (tx, rx) = mpsc::channel();
    for i in 0..3 { let tx = tx.clone(); std::thread::spawn(move || tx.send(i).unwrap()); }
    drop(tx);
    let mut got: Vec<i32> = rx.iter().collect(); got.sort();
    println!("{:?}", got);   // [0, 1, 2]
}
```

**Expected result:** `[0, 1, 2]` — worker results collected via a channel.

**Negative test:** share a `Vec` across threads without synchronization; **channels** (or
`Arc<Mutex>`) are required — the compiler enforces it.

**Cleanup:** none.

### Lab 7.3 — Shared state with Arc<Mutex>

**Objective:** Safely mutate shared state.

```rust
use std::sync::{Arc, Mutex};
fn main() {
    let counter = Arc::new(Mutex::new(0));
    let handles: Vec<_> = (0..5).map(|_| {
        let c = Arc::clone(&counter);
        std::thread::spawn(move || { *c.lock().unwrap() += 1; })
    }).collect();
    for h in handles { h.join().unwrap(); }
    println!("{}", *counter.lock().unwrap());   // 5
}
```

**Expected result:** `5` — safe concurrent increment.

**Negative test:** increment a plain `i32` from many threads; it **won't compile** without
`Arc<Mutex>` — no data races.

**Cleanup:** none.

### Lab 7.4 — Async with tokio

**Objective:** Run concurrent async tasks.

```rust
#[tokio::main]
async fn main() {
    let tasks: Vec<_> = (0..3).map(|i| tokio::spawn(async move {
        tokio::time::sleep(std::time::Duration::from_millis(50)).await; i
    })).collect();
    for t in tasks { println!("done {}", t.await.unwrap()); }
}
```

**Expected result:** three `done` lines from **concurrent async tasks** — the async model.

**Negative test:** block the async runtime with a synchronous `std::thread::sleep`; use
**`tokio::time::sleep().await`** so the runtime stays cooperative.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust's compiler prevents data races (Send/Sync) for fearless concurrency: threads +
channels and `Arc<Mutex>` for CPU/shared work, and async/tokio for high-concurrency I/O.
This chapter spawned threads, used a channel, shared state safely, and ran async tasks.

- [ ] I can explain fearless concurrency (Send/Sync).
- [ ] I can spawn threads and use channels.
- [ ] I can share state with Arc<Mutex>.
- [ ] I can run async tasks with tokio.
- [ ] I completed Labs 7.1–7.4 including each negative test.
