# Chapter 09: Testing, Packaging, and Keeping Current

## Learning Objectives

- Write and run tests with Cargo.
- Enforce quality with clippy and rustfmt.
- Package and publish crates.
- Track Rust releases and editions.
- Complete a walkthrough for each quality/release skill.

## Theory and Architecture

Rust has **built-in testing**: functions annotated `#[test]` run with **`cargo test`**
(unit tests live alongside code, integration tests in `tests/`, and doctests in
documentation examples). Quality tooling ships with the toolchain: **`clippy`** (a rich
linter catching common mistakes and non-idiomatic code) and **`rustfmt`** (canonical
formatting). Libraries are packaged as **crates** and published to **crates.io** (`cargo
publish`), with semantic versioning. Rust ships a **new stable release every six weeks**
(current **1.97.x**) with strong backward-compatibility guarantees, and **editions** (2024)
gate opt-in language changes. Track releases and run **`cargo audit`** for vulnerable
dependencies.

## Design Considerations

Write **`#[test]`** unit tests and doctests, gate CI on **`clippy` + `rustfmt --check`**,
version crates with **semver**, and stay on a **recent stable** release. Use **editions**
per project and run **`cargo audit`** for dependency CVEs.

## Implementation and Automation

The labs write a test, run clippy/fmt, and check the version.

## Validation and Troubleshooting

Confirm the toolchain:

```text
Tests: #[test] + cargo test (unit/integration/doc). Lint: cargo clippy. Format: cargo fmt.
Publish: cargo publish to crates.io (semver). Releases: 6-week stable cadence (1.97.x); editions (2024). cargo audit.
```

Common pitfalls: no **clippy** in CI (non-idiomatic code slips in); and running an old
toolchain that lacks fixes.

## Security and Best Practices

Test with **`cargo test`** (incl. doctests), gate CI on **clippy + rustfmt**, **`cargo
audit`** dependencies, version with **semver**, and keep the toolchain **current**. Prefer
the latest edition for new projects.

## Hands-On Lab

Quality/release walkthroughs. **Shared prerequisites** — cargo, clippy, rustfmt (`rustup
component add clippy rustfmt`). **Cost:** none.

### Lab 9.1 — Write and run a test

**Objective:** Add a unit test.

```rust
// src/lib.rs
pub fn to_cents(dollars: f64) -> u64 { (dollars * 100.0).round() as u64 }
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rounds() { assert_eq!(to_cents(19.99), 1999); }
}
```

```bash
cargo test
```

**Expected result:** **`test result: ok. 1 passed`** — a verified function.

**Negative test:** ship logic with no test; a regression **breaks silently** — test it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Lint with clippy

**Objective:** Catch non-idiomatic code.

```bash
cargo clippy 2>&1 | tail -5
```

**Expected result:** clippy reporting clean (or actionable lints) — enforced idioms.

**Negative test:** rely on review for idiom/bug lints; **clippy** catches them
mechanically — gate CI on it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Format check

**Objective:** Enforce canonical formatting.

```bash
cargo fmt --check || echo "(would reformat; run 'cargo fmt' to fix)"
```

**Expected result:** a clean format check (or a list of files to reformat) — consistent
style.

**Negative test:** argue about brace style in review; **rustfmt** is canonical — run it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.4 — Check the version

**Objective:** Confirm a current toolchain.

```bash
rustc --version
```

**Expected result:** a **1.97.x** version — a current, supported toolchain.

**Negative test:** run a long-outdated toolchain; Rust's **6-week cadence** ships fixes —
update with `rustup update`.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust ships built-in testing (`cargo test`, doctests), clippy/rustfmt for quality, crates.io
for distribution, and a fast stable cadence with editions — plus `cargo audit` for
dependency security. This chapter wrote a test, ran clippy/fmt, and checked the version.

- [ ] I can write and run tests with cargo test.
- [ ] I can lint with clippy.
- [ ] I can enforce formatting with rustfmt.
- [ ] I can confirm a current toolchain and understand editions.
- [ ] I completed Labs 9.1–9.4 including each negative test.
