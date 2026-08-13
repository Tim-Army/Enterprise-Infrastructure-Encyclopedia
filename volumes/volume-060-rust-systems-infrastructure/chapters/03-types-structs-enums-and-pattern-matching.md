# Chapter 03: Types, Structs, Enums, and Pattern Matching

## Learning Objectives

- Model data with structs and enums.
- Handle absence with Option.
- Match exhaustively with pattern matching.
- Use methods with impl blocks.
- Complete a walkthrough for each modeling concept.

## Theory and Architecture

Rust's type system makes **invalid states unrepresentable**. **Structs** group related
fields; **enums** model a value that is one of several **variants** (and can carry data),
which — combined with **pattern matching** (`match`) — express state machines and
alternatives precisely. Two enums are foundational: **`Option<T>`** (`Some(T)` or `None`)
replaces null, forcing you to handle absence; and **`Result<T, E>`** (`Ok`/`Err`) for
fallible operations (Chapter 04). `match` is **exhaustive** — the compiler ensures every
variant is handled. Behavior attaches to types via **`impl`** blocks (methods).

## Design Considerations

Model domains with **structs + enums** so illegal combinations can't exist. Use
**`Option`** instead of sentinel/null values, and **exhaustive `match`** so adding a
variant forces you to handle it everywhere. Attach behavior with **methods** on the type.

## Implementation and Automation

The labs define a struct, an enum, Option handling, and methods.

## Validation and Troubleshooting

Confirm the model:

```text
struct { fields }. enum { Variant, Variant(data) }. Option<T> = Some(T) | None.
match is exhaustive (all variants). impl Type { fn method(&self) ... }.
```

Common pitfalls: modeling states with booleans/flags (illegal combos possible); and
non-exhaustive handling that breaks when a variant is added.

## Security and Best Practices

Make **invalid states unrepresentable** with enums, replace null with **`Option`**, keep
`match` **exhaustive**, and attach behavior via **methods**. Let the type system enforce
your invariants.

## Hands-On Lab

Modeling walkthroughs. **Shared prerequisites** — cargo (`cargo new model && cd model`).
**Cost:** none.

### Lab 3.1 — Define a struct

**Objective:** Model a host record.

```rust
struct Host { name: String, port: u16, active: bool }
fn main() {
    let h = Host { name: "web1".into(), port: 443, active: true };
    println!("{}:{} active={}", h.name, h.port, h.active);
}
```

**Expected result:** `web1:443 active=true` — a structured record.

**Negative test:** pass loose parallel variables (name, port, active) everywhere; a
**struct** keeps them together and typed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Enum with data

**Objective:** Model a connection state machine.

```rust
enum State { Down, Connecting, Up { since: u64 } }
fn describe(s: &State) -> String {
    match s {
        State::Down => "down".into(),
        State::Connecting => "connecting".into(),
        State::Up { since } => format!("up since {since}"),
    }
}
fn main() { println!("{}", describe(&State::Up { since: 1000 })); }
```

**Expected result:** `up since 1000` — an enum + exhaustive match.

**Negative test:** represent state with two booleans; **enum variants** make impossible
states (e.g., down-and-up) unrepresentable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Option and match

**Objective:** Handle a possibly-missing value.

```rust
fn find_port(name: &str) -> Option<u16> {
    if name == "web1" { Some(443) } else { None }
}
fn main() {
    match find_port("db1") {
        Some(p) => println!("port {p}"),
        None => println!("no port for that host"),
    }
}
```

**Expected result:** `no port for that host` — absence handled explicitly.

**Negative test:** return `-1`/0 as a "not found" sentinel; **`Option`** forces the caller
to handle `None` — no silent sentinels.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Methods with impl

**Objective:** Attach behavior to a type.

```rust
struct Host { name: String, port: u16 }
impl Host {
    fn endpoint(&self) -> String { format!("{}:{}", self.name, self.port) }
}
fn main() {
    let h = Host { name: "web1".into(), port: 443 };
    println!("{}", h.endpoint());
}
```

**Expected result:** `web1:443` — behavior via a method.

**Negative test:** scatter free functions taking the struct everywhere; **methods** keep
behavior with the data.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust's types make invalid states unrepresentable: structs group data, enums model
alternatives (with data), Option replaces null, exhaustive match handles every case, and
impl blocks attach behavior. This chapter modeled a host, a state enum, Option, and
methods.

- [ ] I can model data with structs.
- [ ] I can model alternatives with enums.
- [ ] I can handle absence with Option and match.
- [ ] I can attach methods with impl.
- [ ] I completed Labs 3.1–3.4 including each negative test.
