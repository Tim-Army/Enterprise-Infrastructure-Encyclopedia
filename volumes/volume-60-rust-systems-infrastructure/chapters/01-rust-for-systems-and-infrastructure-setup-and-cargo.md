# Chapter 01: Rust for Systems and Infrastructure — Setup and Cargo

## Learning Objectives

- Explain why Rust suits systems and infrastructure software.
- Install the toolchain with rustup.
- Create and run a project with Cargo.
- Manage dependencies and editions.
- Verify the toolchain version.

## Theory and Architecture

**Rust** is a systems programming language that delivers **memory safety without a
garbage collector** and **C-comparable performance**, enforced at compile time by its
ownership model. For infrastructure that means reliable, fast, small-footprint binaries —
increasingly used for CLIs (ripgrep, bat), container/runtime tooling, network services,
and eBPF/agents where correctness and performance both matter. Where Python (Volumes
LVII–LVIII) is the glue language, Rust is chosen when you need a **fast, dependable
binary**.

The toolchain is managed by **rustup** (installs the compiler `rustc`, `cargo`, and
components like `clippy`/`rustfmt`) and centered on **Cargo** — the build system and
package manager that handles builds, dependencies (**crates** from crates.io declared in
**`Cargo.toml`**), testing, and publishing. Rust evolves through **editions** (2015, 2018,
2021, **2024**) that opt into language changes without breaking old code; the current
stable release is **1.97.x**.

## Design Considerations

Reach for Rust when a task needs a **fast, correct, self-contained binary** (performance-
critical agents, CLIs, services) rather than a quick script. Use **Cargo** for everything
(build/test/deps), pin dependencies for reproducibility, and target the current stable
release and the **2024 edition** for new projects.

## Implementation and Automation

Create and run a project with Cargo:

```bash
cargo new infra-tool && cd infra-tool
cargo run
```

## Validation and Troubleshooting

Confirm the fundamentals:

```text
Toolchain via rustup (rustc, cargo, clippy, rustfmt). Cargo: build/test/deps/publish.
Deps: crates from crates.io in Cargo.toml. Editions: 2015/2018/2021/2024. Stable: 1.97.x.
```

Common pitfalls: fighting the borrow checker instead of learning ownership (Chapter 02);
and mixing editions/toolchains unexpectedly.

## Security and Best Practices

Install via **rustup**, use **Cargo** for reproducible builds, pin dependency versions,
keep the toolchain current, and audit dependencies (`cargo audit`). Prefer Rust where
memory-safety and performance both matter.

## References and Knowledge Checks

- doc.rust-lang.org: The Rust Programming Language ("the book"), Cargo, and std docs.

**Knowledge checks**

1. What does Rust provide that C lacks and Python provides differently?
2. What does Cargo manage?
3. What is a Rust edition?

## Hands-On Lab

Setup walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — rustup/cargo installed
(`rustup` from rustup.rs). **Cost:** none.

### Lab 1.1 — Create and run a project

**Objective:** Scaffold a Cargo project.

```bash
cargo new infra-tool && cd infra-tool
cargo run
```

**Expected result:** **`Hello, world!`** — a compiled, running binary.

**Negative test:** compile a `.rs` file by hand with `rustc` for a multi-file project;
**Cargo** manages builds/deps — use it beyond single files.

**Cleanup:** `cd .. && rm -rf infra-tool`.

### Lab 1.2 — Add a dependency

**Objective:** Declare a crate and use it.

```bash
cargo new dep-demo && cd dep-demo
cargo add serde_json
grep serde_json Cargo.toml
```

**Expected result:** a **`serde_json`** dependency line in `Cargo.toml` — a managed
dependency.

**Negative test:** vendor a crate's source by copy-paste; **`cargo add`** + crates.io
handles versions/updates — declare it.

**Cleanup:** `cd .. && rm -rf dep-demo`.

### Lab 1.3 — Verify the toolchain

**Objective:** Confirm the compiler version.

```bash
rustc --version
cargo --version
```

**Expected result:** a **1.97.x** rustc/cargo version — the running toolchain.

**Negative test:** assume language features exist regardless of version; **check
`--version`** — features stabilize per release/edition.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust delivers memory safety without a GC and high performance, making it ideal for fast,
reliable infrastructure binaries; the toolchain is rustup-managed and centered on Cargo,
with crates from crates.io and editions for language evolution. This chapter created a
project, added a dependency, and checked the version.

- [ ] I can explain why Rust suits systems/infra software.
- [ ] I can create and run a Cargo project.
- [ ] I can add a dependency.
- [ ] I can verify the toolchain version.
- [ ] I completed Labs 1.1–1.3 including each negative test.
