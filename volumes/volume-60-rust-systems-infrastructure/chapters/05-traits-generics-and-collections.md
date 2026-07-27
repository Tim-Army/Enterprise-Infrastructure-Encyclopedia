# Chapter 05: Traits, Generics, and Collections

## Learning Objectives

- Define shared behavior with traits.
- Write generic, reusable functions.
- Use core collections (Vec, HashMap).
- Transform data with iterators.
- Complete a walkthrough for each abstraction skill.

## Theory and Architecture

Rust's abstraction tools are **traits** and **generics**. A **trait** defines shared
behavior (like an interface) that types can implement; functions can accept "any type that
implements trait X" via **generics** with **trait bounds** (`fn f<T: Display>(x: T)`),
resolved at compile time with no runtime cost (monomorphization). The standard
**collections** — **`Vec<T>`** (growable array) and **`HashMap<K, V>`** — cover most needs,
and **iterators** provide lazy, composable transforms (`.iter().map().filter().collect()`)
that are both expressive and efficient. Together they give Python-like expressiveness with
compile-time safety and speed.

## Design Considerations

Program against **traits** (behavior) rather than concrete types for flexibility. Use
**generics + bounds** for reusable code. Reach for **`HashMap`** to index and **`Vec`** for
sequences, and prefer **iterator chains** over manual loops for clarity and performance.

## Implementation and Automation

The labs define a trait, a generic function, use collections, and chain iterators.

## Validation and Troubleshooting

Confirm the tools:

```text
trait T { fn m(&self); } impl T for Type {}. Generics: fn f<T: Bound>(x: T).
Vec<T> (sequence), HashMap<K,V> (index). Iterators: iter().map().filter().collect().
```

Common pitfalls: over-cloning in iterator chains; and manual index loops where an iterator
is clearer/safer.

## Security and Best Practices

Abstract with **traits**, reuse with **generics + bounds**, index with **`HashMap`**, and
prefer **iterator adapters** over manual loops (fewer off-by-one/bounds bugs). Keep trait
bounds minimal and meaningful.

## Hands-On Lab

Abstraction walkthroughs. **Shared prerequisites** — cargo (`cargo new abstr && cd
abstr`). **Cost:** none.

### Lab 5.1 — Define and implement a trait

**Objective:** Share behavior across types.

```rust
trait Endpoint { fn addr(&self) -> String; }
struct Host { name: String, port: u16 }
impl Endpoint for Host { fn addr(&self) -> String { format!("{}:{}", self.name, self.port) } }
fn main() { println!("{}", Host { name: "web1".into(), port: 443 }.addr()); }
```

**Expected result:** `web1:443` — behavior via a trait.

**Negative test:** duplicate an `addr` function for each type; a **trait** unifies the
behavior — implement it.

**Cleanup:** none.

### Lab 5.2 — Generic function with a bound

**Objective:** Accept any type implementing a trait.

```rust
use std::fmt::Display;
fn announce<T: Display>(x: T) { println!("ready: {x}"); }
fn main() { announce("web1"); announce(443); }
```

**Expected result:** two `ready:` lines for a string and an int — one generic function.

**Negative test:** write `announce_str` and `announce_int` separately; **generics + a
bound** cover both.

**Cleanup:** none.

### Lab 5.3 — HashMap indexing

**Objective:** Index records by key.

```rust
use std::collections::HashMap;
fn main() {
    let mut ports = HashMap::new();
    ports.insert("web1", 443u16);
    ports.insert("db1", 5432);
    println!("{:?}", ports.get("db1"));   // Some(5432)
}
```

**Expected result:** `Some(5432)` — O(1) keyed lookup.

**Negative test:** scan a `Vec` of pairs for each lookup; a **HashMap** is O(1) — index
with it.

**Cleanup:** none.

### Lab 5.4 — Iterator chain

**Objective:** Transform a collection functionally.

```rust
fn main() {
    let ports = vec![22, 80, 443, 8080];
    let secure: Vec<u16> = ports.iter().copied().filter(|&p| p == 443 || p == 8443).collect();
    println!("{:?}", secure);   // [443]
}
```

**Expected result:** `[443]` — a filtered, collected result.

**Negative test:** build the result with a manual index loop + push; an **iterator chain**
is clearer and bounds-safe.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Traits define shared behavior, generics with bounds give zero-cost reuse, Vec/HashMap cover
core data needs, and iterators transform data expressively and efficiently. This chapter
defined a trait, a generic function, used a HashMap, and chained iterators.

- [ ] I can define and implement traits.
- [ ] I can write generic functions with bounds.
- [ ] I can index with HashMap.
- [ ] I can transform data with iterators.
- [ ] I completed Labs 5.1–5.4 including each negative test.
