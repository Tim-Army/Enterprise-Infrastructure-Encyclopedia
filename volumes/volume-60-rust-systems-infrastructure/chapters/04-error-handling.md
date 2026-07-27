# Chapter 04: Error Handling

## Learning Objectives

- Use Result for recoverable errors.
- Propagate errors with the `?` operator.
- Distinguish panic from recoverable errors.
- Use anyhow and thiserror for ergonomic errors.
- Complete a walkthrough for each error-handling skill.

## Theory and Architecture

Rust has **no exceptions**; fallible operations return **`Result<T, E>`** (`Ok`/`Err`), so
error handling is explicit and checked by the compiler. The **`?` operator** propagates an
`Err` up the call stack (returning early) while unwrapping `Ok`, making error-forwarding
concise. **`panic!`** (and `.unwrap()`/`.expect()`) is for **unrecoverable** bugs/invariant
violations — it aborts the thread — not for normal error flow. Two crates smooth real code:
**`thiserror`** derives custom error enums for libraries, and **`anyhow`** provides a
convenient `Result` with context for applications.

## Design Considerations

Return **`Result`** for anything that can fail, propagate with **`?`**, and reserve
**`panic`/`unwrap`** for truly-impossible cases or fast prototypes. Use **`thiserror`** to
define library error types and **`anyhow`** with **`.context(...)`** in binaries for helpful
messages.

## Implementation and Automation

The labs use Result, `?`, a custom error, and anyhow context.

## Validation and Troubleshooting

Confirm the model:

```text
Result<T,E> (Ok/Err). ? propagates Err (early return). panic!/unwrap = unrecoverable.
thiserror: derive library error enums. anyhow: app-level Result + .context(...).
```

Common pitfalls: **`.unwrap()`** in production paths (crashes on error); and swallowing
errors instead of propagating.

## Security and Best Practices

Return **`Result`** and propagate with **`?`**, avoid **`unwrap`** on fallible paths,
add **context** with anyhow, and define typed errors with **thiserror**. Handle or forward
every error — never ignore.

## Hands-On Lab

Error-handling walkthroughs. **Shared prerequisites** — cargo (`cargo new errs && cd
errs`; `cargo add anyhow thiserror` for later labs). **Cost:** none.

### Lab 4.1 — Return a Result

**Objective:** Model a fallible parse.

```rust
fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> {
    s.parse::<u16>()
}
fn main() {
    match parse_port("443") { Ok(p) => println!("port {p}"), Err(e) => println!("err {e}") }
}
```

**Expected result:** `port 443` — a checked, fallible operation.

**Negative test:** return a bare `u16` and use 0 for failure; **`Result`** makes failure
explicit and unignorable.

**Cleanup:** none.

### Lab 4.2 — Propagate with ?

**Objective:** Forward errors concisely.

```rust
use std::num::ParseIntError;
fn add_ports(a: &str, b: &str) -> Result<u16, ParseIntError> {
    Ok(a.parse::<u16>()? + b.parse::<u16>()?)   // ? returns early on Err
}
fn main() { println!("{:?}", add_ports("80", "x")); }
```

**Expected result:** an `Err(...)` for the bad input — `?` propagated the failure.

**Negative test:** match each parse manually and nest the handling; **`?`** forwards errors
without the boilerplate.

**Cleanup:** none.

### Lab 4.3 — Custom error with thiserror

**Objective:** Define a typed library error.

```rust
use thiserror::Error;
#[derive(Error, Debug)]
enum ConfigError {
    #[error("missing field: {0}")]
    Missing(String),
}
fn main() { println!("{}", ConfigError::Missing("host".into())); }
```

**Expected result:** `missing field: host` — a typed, descriptive error.

**Negative test:** return `String` errors everywhere; **typed errors** (thiserror) let
callers match on the cause.

**Cleanup:** none.

### Lab 4.4 — App errors with anyhow context

**Objective:** Add context in a binary.

```rust
use anyhow::{Context, Result};
fn load() -> Result<String> {
    std::fs::read_to_string("/no/such/file").context("reading config")
}
fn main() { if let Err(e) = load() { println!("{e:#}"); } }
```

**Expected result:** an error message including **"reading config"** — contextualized
failure.

**Negative test:** surface a bare OS error with no context; **`.context(...)`** tells the
operator *what* failed.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust error handling is explicit: `Result` for recoverable errors, `?` to propagate,
`panic`/`unwrap` only for the unrecoverable, and thiserror/anyhow for typed and
contextualized errors. This chapter returned Results, propagated with `?`, and used both
crates.

- [ ] I can return and match on Result.
- [ ] I can propagate errors with `?`.
- [ ] I can define typed errors with thiserror.
- [ ] I can add context with anyhow.
- [ ] I completed Labs 4.1–4.4 including each negative test.
