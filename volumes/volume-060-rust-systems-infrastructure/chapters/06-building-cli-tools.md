# Chapter 06: Building CLI Tools

## Learning Objectives

- Parse arguments with clap.
- Structure a CLI with subcommands.
- Add structured logging.
- Build a release binary.
- Complete a walkthrough for each CLI skill.

## Theory and Architecture

Rust excels at **fast, single-binary CLI tools** (ripgrep, fd, bat). The standard argument
parser is **`clap`**, used most ergonomically via its **derive** API: annotate a struct
with `#[derive(Parser)]` and fields become options/arguments with auto-generated help,
validation, and types. **Subcommands** model tool verbs (via a `#[derive(Subcommand)]`
enum). Production tools add **structured logging** with the **`tracing`** (or `log` + `env_logger`)
ecosystem, and ship as an optimized **release binary** (`cargo build --release`) that runs
anywhere with no runtime.

## Design Considerations

Define the CLI as a **typed struct** with clap derive (free help/validation), use
**subcommands** for verbs, log with **`tracing`**/levels (not `println!`), and distribute
the **`--release`** binary (small, fast, dependency-free).

## Implementation and Automation

The labs build a clap CLI, add a subcommand, add logging, and produce a release build.

## Validation and Troubleshooting

Confirm the model:

```text
clap derive: #[derive(Parser)] struct Cli { #[arg(...)] field }. Subcommands: #[derive(Subcommand)] enum.
Logging: tracing/log + levels. Release: cargo build --release -> target/release/<bin>.
```

Common pitfalls: hand-parsing `std::env::args()` (no help/validation); and `println!`
instead of leveled logging.

## Security and Best Practices

Use **clap derive** for typed args and free help, model verbs with **subcommands**, log at
**levels** with `tracing`, and ship the optimized **release** binary. Validate inputs via
clap's types/validators.

## Hands-On Lab

CLI walkthroughs. **Shared prerequisites** — cargo (`cargo new cli && cd cli`; `cargo add
clap --features derive`). **Cost:** none.

### Lab 6.1 — Parse arguments with clap

**Objective:** Define a typed CLI.

```rust
use clap::Parser;
#[derive(Parser)]
struct Cli { host: String, #[arg(long, default_value_t = 3)] count: u8 }
fn main() { let c = Cli::parse(); println!("ping {} x{}", c.host, c.count); }
```

```bash
cargo run -- web1 --count 5
```

**Expected result:** `ping web1 x5` — parsed args with a typed option and default.

**Negative test:** index `std::env::args()` by position; **clap** gives help, validation,
and types — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Subcommands

**Objective:** Model tool verbs.

```rust
use clap::{Parser, Subcommand};
#[derive(Parser)]
struct Cli { #[command(subcommand)] cmd: Cmd }
#[derive(Subcommand)]
enum Cmd { Ping { host: String }, Version }
fn main() {
    match Cli::parse().cmd {
        Cmd::Ping { host } => println!("ping {host}"),
        Cmd::Version => println!("v0.1.0"),
    }
}
```

**Expected result:** `ping web1` (with `run -- ping web1`) — verb-based CLI.

**Negative test:** cram every mode into flags on one command; **subcommands** organize a
multi-verb tool.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Structured logging

**Objective:** Log at levels.

```rust
// cargo add tracing tracing-subscriber
fn main() {
    tracing_subscriber::fmt::init();
    tracing::info!("starting");
    tracing::debug!("hidden unless RUST_LOG=debug");
}
```

**Expected result:** the **info** line shown (debug filtered unless `RUST_LOG=debug`) —
leveled logging.

**Negative test:** `println!` everything; **tracing** filters by level and adds structure —
use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Release build

**Objective:** Produce an optimized binary.

```bash
cargo build --release
ls -lh target/release/cli 2>/dev/null | awk '{print $5, $9}'
```

**Expected result:** an optimized **`target/release/cli`** binary — a fast, distributable
artifact.

**Negative test:** ship the **debug** build; `--release` is optimized and smaller — build
release for distribution.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust CLIs use clap (derive) for typed args and subcommands, tracing for leveled logging,
and `--release` for an optimized single binary. This chapter built a CLI with subcommands,
logging, and a release build.

- [ ] I can parse args with clap derive.
- [ ] I can model verbs with subcommands.
- [ ] I can log at levels with tracing.
- [ ] I can build an optimized release binary.
- [ ] I completed Labs 6.1–6.4 including each negative test.
