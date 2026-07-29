# Chapter 08: Working with the System and Networks

## Learning Objectives

- Run external commands and read their output.
- Read and write files and environment.
- Call HTTP APIs with reqwest.
- Serialize/deserialize JSON with serde.
- Complete a walkthrough for each systems skill.

## Theory and Architecture

Infrastructure tools interact with the OS and network. Rust's standard library covers
**`std::process::Command`** (run external programs, capture output, check status),
**`std::fs`** (files) and **`std::env`** (environment/args). For networking, the ecosystem
provides **`reqwest`** — an ergonomic HTTP client (built on tokio/hyper) for calling REST
APIs — and **`serde`** with **`serde_json`**, the near-universal (de)serialization framework
that maps JSON to typed structs via `#[derive(Serialize, Deserialize)]`. Together these let
Rust do the same API-and-config work as Python, but as a fast, typed binary.

## Design Considerations

Run commands with **`Command`** (argument lists, checked status), read config from **`env`/
files**, call APIs with **`reqwest`**, and map payloads to **typed structs with serde**
(compile-time-checked shapes) rather than untyped maps. Handle every `Result`.

## Implementation and Automation

The labs run a command, read a file, and (de)serialize JSON with serde.

## Validation and Troubleshooting

Confirm the tools:

```text
std::process::Command::new("cmd").args([...]).output() -> stdout/status.
std::fs read/write; std::env::var. reqwest for HTTP. serde + serde_json: #[derive(Serialize, Deserialize)].
```

Common pitfalls: ignoring a command's **exit status**; and parsing JSON into untyped
`Value` where a **typed struct** is clearer/safer.

## Security and Best Practices

Run commands as **argument lists** (no shell string building), check **exit status**, read
secrets from **env**, and deserialize into **typed structs** so malformed data fails
loudly. Handle all `Result`s.

## Hands-On Lab

Systems walkthroughs. **Shared prerequisites** — cargo (`cargo new sys && cd sys`; `cargo
add serde --features derive serde_json`). **Cost:** none.

### Lab 8.1 — Run a command

**Objective:** Execute a program and capture output.

```rust
use std::process::Command;
fn main() {
    let out = Command::new("echo").arg("hello infra").output().unwrap();
    println!("out: {}", String::from_utf8_lossy(&out.stdout).trim());
    println!("ok: {}", out.status.success());
}
```

**Expected result:** `out: hello infra` and `ok: true` — captured output and status.

**Negative test:** build a shell string from input and run it; pass **argument lists** to
`Command` — avoid injection.

**Cleanup:** none.

### Lab 8.2 — Read a file and env

**Objective:** Read config from disk/environment.

```rust
fn main() {
    std::fs::write("/tmp/rust_cfg.txt", "port=443\n").unwrap();
    let cfg = std::fs::read_to_string("/tmp/rust_cfg.txt").unwrap();
    let home = std::env::var("HOME").unwrap_or_else(|_| "?".into());
    println!("cfg={} home_set={}", cfg.trim(), home != "?");
}
```

**Expected result:** `cfg=port=443 home_set=true` — file + env access.

**Negative test:** hard-code config in the binary; read it from **files/env** so it's
changeable without recompiling.

**Cleanup:** `rm -f /tmp/rust_cfg.txt`.

### Lab 8.3 — Deserialize JSON with serde

**Objective:** Map JSON to a typed struct.

```rust
use serde::Deserialize;
#[derive(Deserialize, Debug)]
struct Host { name: String, port: u16 }
fn main() {
    let h: Host = serde_json::from_str(r#"{"name":"web1","port":443}"#).unwrap();
    println!("{}:{}", h.name, h.port);   // web1:443
}
```

**Expected result:** `web1:443` — JSON parsed into a typed struct.

**Negative test:** dig through an untyped `serde_json::Value` by string keys; a **typed
struct** validates the shape at deserialize time.

**Cleanup:** none.

### Lab 8.4 — HTTP with reqwest (pattern)

**Objective:** Call a REST API.

```rust
// cargo add reqwest --features json ; cargo add tokio --features full
// #[tokio::main] async fn main() -> Result<(), reqwest::Error> {
//     let body: serde_json::Value = reqwest::get("https://httpbin.org/json").await?.json().await?;
//     println!("keys: {:?}", body.as_object().map(|m| m.keys().len()));
//     Ok(())
// }
println!("reqwest: async GET -> .json() into serde types (typed API access)");
```

**Expected result:** the reqwest **async GET → JSON** pattern — typed API access.

**Negative test:** hand-roll HTTP over TCP sockets; **reqwest** handles TLS/redirects/JSON —
use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rust interacts with the system via `Command`, `fs`, and `env`, and with networks via
reqwest (HTTP) and serde (typed JSON) — doing Python-style glue work as a fast, typed
binary. This chapter ran a command, read file/env, and deserialized JSON.

- [ ] I can run commands and check status.
- [ ] I can read files and environment.
- [ ] I can deserialize JSON into typed structs.
- [ ] I can describe HTTP access with reqwest.
- [ ] I completed Labs 8.1–8.4 including each negative test.
