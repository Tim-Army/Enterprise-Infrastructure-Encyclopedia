# Chapter 02: Ownership, Borrowing, and Lifetimes

## Learning Objectives

- Explain Rust's ownership model and why it guarantees memory safety.
- Move and clone values correctly.
- Borrow with shared and mutable references.
- Understand lifetimes at a working level.
- Complete a walkthrough for each ownership concept.

## Theory and Architecture

Rust's defining feature is **ownership** — a compile-time discipline that eliminates whole
classes of bugs (use-after-free, double-free, data races) without a garbage collector.
The rules: every value has one **owner**; when the owner goes out of scope the value is
**dropped** (freed); assigning or passing a non-`Copy` value **moves** ownership (the old
binding becomes invalid). To use a value without taking ownership you **borrow** it: a
shared reference **`&T`** (many allowed, read-only) or a mutable reference **`&mut T`**
(exclusive, read-write) — the compiler enforces that you never have a mutable reference
alongside any other reference. **Lifetimes** are the compiler's way of ensuring references
never outlive the data they point to; most are inferred.

## Design Considerations

Prefer **borrowing** (`&`/`&mut`) over moving or **cloning** — cloning is explicit and can
be costly. Design functions to take references when they only need to read. Let the
compiler's ownership errors guide you toward correct, safe designs rather than fighting
them.

## Implementation and Automation

The labs demonstrate move, clone, shared/mutable borrows, and a borrow-checker error.

## Validation and Troubleshooting

Confirm the model:

```text
One owner; drop at scope end. Move on assign/pass (non-Copy). Borrow: &T (shared, many) / &mut T (exclusive).
No &mut alongside any other ref. Lifetimes ensure refs don't outlive data (mostly inferred).
```

Common pitfalls: using a value after it was **moved**; and holding a `&mut` while another
reference exists.

## Security and Best Practices

Borrow instead of move/clone where possible, keep **mutable borrows** short and exclusive,
and treat borrow-checker errors as design feedback. Ownership is what makes Rust safe —
work with it, not against it.

## Hands-On Lab

Ownership walkthroughs. **Shared prerequisites** — cargo (`cargo new own && cd own`, edit
`src/main.rs`, `cargo run`). **Cost:** none.

### Lab 2.1 — Move semantics

**Objective:** Observe a move invalidating the source.

```rust
fn main() {
    let a = String::from("config");
    let b = a;                 // ownership moves to b
    println!("{b}");           // ok
    // println!("{a}");        // compile error: value borrowed after move
}
```

**Expected result:** it prints `config`; uncommenting the `a` line **fails to compile** —
move semantics.

**Negative test:** expect `a` to still be usable after `let b = a`; non-`Copy` types
**move** — clone or borrow if you need both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Clone when you need a copy

**Objective:** Keep both bindings with an explicit clone.

```rust
fn main() {
    let a = String::from("config");
    let b = a.clone();         // deep copy
    println!("{a} {b}");       // both valid
}
```

**Expected result:** `config config` — both usable after an **explicit clone**.

**Negative test:** clone large data on a hot path to dodge the borrow checker; **borrow**
instead — cloning has a cost.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Shared borrows

**Objective:** Read a value without taking ownership.

```rust
fn len_of(s: &String) -> usize { s.len() }   // borrows, doesn't own
fn main() {
    let s = String::from("infra");
    println!("{}", len_of(&s));               // s still owned by main
    println!("{s}");
}
```

**Expected result:** the length then `infra` — a shared borrow leaves the owner intact.

**Negative test:** pass `s` by value to a helper that only reads it; **borrow with `&`** so
the caller keeps ownership.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Mutable borrow exclusivity

**Objective:** See the exclusive-mutable-borrow rule.

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let m = &mut v;            // exclusive mutable borrow
    m.push(4);
    // let r = &v;             // compile error: cannot borrow while &mut exists
    println!("{:?}", v);
}
```

**Expected result:** `[1, 2, 3, 4]`; uncommenting `&v` **fails to compile** — exclusive
mutability.

**Negative test:** hold a `&mut` and a `&` at once; the compiler **rejects** it — that rule
prevents data races.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ownership gives Rust memory safety without a GC: one owner, move on assignment, borrow with
`&`/`&mut` under exclusivity rules, and lifetimes ensuring references stay valid. This
chapter demonstrated moves, clones, and shared/mutable borrows.

- [ ] I can explain ownership and drops.
- [ ] I can reason about move vs clone.
- [ ] I can borrow with shared references.
- [ ] I can apply the exclusive-mutable-borrow rule.
- [ ] I completed Labs 2.1–2.4 including each negative test.
