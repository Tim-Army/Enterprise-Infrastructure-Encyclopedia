# Volume LX Glossary

Definitions for terms used in **Volume LX — Rust for Systems and Infrastructure**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**anyhow** — An application-level error crate providing a convenient `Result` with
context. Used in Chapter 04.

**Arc<Mutex<T>>** — A thread-safe reference-counted pointer around a mutex for shared
mutable state. Used in Chapter 07.

**Borrowing** — Accessing a value by reference (`&T` shared, `&mut T` exclusive) without
taking ownership. Used in Chapter 02.

**Cargo** — Rust's build system and package manager (build/test/deps/publish). Used in
Chapters 01 and 09.

**Crate** — A Rust package/library, distributed via crates.io. Used in Chapters 01 and 09.

**Edition** — An opt-in set of language changes (2015/2018/2021/2024) that doesn't break
older code. Used in Chapters 01 and 09.

**Enum** — A type that is one of several variants, optionally carrying data; matched
exhaustively. Used in Chapter 03.

**Generics** — Type parameters (with trait bounds) enabling zero-cost reusable code. Used
in Chapter 05.

**Lifetime** — A compile-time guarantee that references never outlive the data they point
to. Used in Chapter 02.

**Option<T>** — An enum (`Some`/`None`) replacing null, forcing explicit absence handling.
Used in Chapter 03.

**Ownership** — Rust's rule that each value has one owner and is dropped at scope end; the
basis of memory safety. Used in Chapter 02.

**reqwest** — An ergonomic HTTP client crate. Used in Chapter 08.

**Result<T, E>** — An enum (`Ok`/`Err`) for recoverable errors; propagated with `?`. Used
in Chapter 04.

**serde** — The Rust (de)serialization framework (with serde_json for JSON). Used in
Chapter 08.

**Send / Sync** — Marker traits the compiler uses to guarantee thread-safety (no data
races). Used in Chapter 07.

**thiserror** — A crate to derive typed library error enums. Used in Chapter 04.

**tokio** — The async runtime for high-concurrency I/O. Used in Chapter 07.

**Trait** — A definition of shared behavior a type can implement (like an interface). Used
in Chapter 05.

**clippy / rustfmt** — The Rust linter and canonical formatter. Used in Chapter 09.
