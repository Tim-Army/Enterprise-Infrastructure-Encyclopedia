# Volume LX — Rust for Systems and Infrastructure

> Rust for infrastructure engineers, end to end — Cargo, ownership/borrowing, types and
> pattern matching, error handling, traits/generics/collections, CLI tools, concurrency
> and async, systems and network programming, and testing/packaging — with hands-on,
> compilable labs targeting Rust 1.97.x.

## Overview

Volume LX is a hands-on guide to **Rust for systems and infrastructure** — the language
chosen when infrastructure software needs a **fast, correct, self-contained binary**
(agents, CLIs, network services, runtime tooling). It complements the Python volumes
(LVII–LVIII): where Python is the glue, Rust is the performance-and-reliability choice.

Like the other tool/skills volumes, this is a **product/skills** volume — organized by
capability, with a **compilable walkthrough lab for every major functional area**. It
targets **Rust 1.97.x** and the **2024 edition** (verified on github.com/rust-lang/rust on
27 July 2026); every code lab compiles and runs with a stock `cargo`, so the volume is
reproducible for free.

Chapters are organized by capability:

- **Chapter 01** covers the toolchain and Cargo.
- **Chapter 02** covers ownership, borrowing, and lifetimes.
- **Chapter 03** covers types, structs, enums, and pattern matching.
- **Chapter 04** covers error handling (Result, `?`, anyhow/thiserror).
- **Chapter 05** covers traits, generics, and collections.
- **Chapter 06** covers building CLI tools (clap).
- **Chapter 07** covers concurrency and async (threads, channels, tokio).
- **Chapter 08** covers systems and network programming (Command, reqwest, serde).
- **Chapter 09** covers testing, packaging, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Rust for Systems and Infrastructure — Setup and Cargo](chapters/01-rust-for-systems-and-infrastructure-setup-and-cargo.md) — toolchain, Cargo, crates, editions.
2. [Ownership, Borrowing, and Lifetimes](chapters/02-ownership-borrowing-and-lifetimes.md) — the memory-safety model.
3. [Types, Structs, Enums, and Pattern Matching](chapters/03-types-structs-enums-and-pattern-matching.md) — modeling with the type system.
4. [Error Handling](chapters/04-error-handling.md) — Result, `?`, anyhow/thiserror.
5. [Traits, Generics, and Collections](chapters/05-traits-generics-and-collections.md) — abstraction and data structures.
6. [Building CLI Tools](chapters/06-building-cli-tools.md) — clap, subcommands, logging, release builds.
7. [Concurrency and Async](chapters/07-concurrency-and-async.md) — fearless concurrency and tokio.
8. [Working with the System and Networks](chapters/08-working-with-the-system-and-networks.md) — Command, files, reqwest, serde.
9. [Testing, Packaging, and Keeping Current](chapters/09-testing-packaging-and-keeping-current.md) — cargo test, clippy/fmt, crates.io, editions.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **compilable walkthrough lab for every major functional area** — **35 labs**
across the nine chapters. The walkthroughs use the real toolchain — **`cargo`**, the
standard library, and mainstream crates (**`clap`**, **`serde`**, **`tokio`**, **`anyhow`/
`thiserror`**, **`reqwest`**) — all buildable with a stock Rust install; several labs
include deliberate compile-error negative tests that demonstrate the borrow checker. Each
lab states an objective, code, expected results, a negative test, and cleanup, and ends
with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **doc.rust-lang.org** and **github.com/rust-lang** (the language and
docs), **Rust 1.97.x** with the **2024 edition**, and mainstream crates from **crates.io**.
Rust ships stable releases every six weeks, so keep the toolchain current — the 1.97.x
baseline was verified on 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-060-rust-systems-infrastructure
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
