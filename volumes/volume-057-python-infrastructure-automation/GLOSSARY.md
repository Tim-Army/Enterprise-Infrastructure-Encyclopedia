# Volume LVII Glossary

Definitions for terms used in **Volume LVII — Python for Infrastructure and Automation**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**argparse** — The standard-library command-line argument parser. Used in Chapter 06.

**asyncio** — Python's standard-library framework for single-threaded cooperative
concurrency (`async`/`await`). Used in Chapter 07.

**click** — A third-party library for building ergonomic CLIs with decorators. Used in
Chapter 06.

**Comprehension** — A concise expression to build a list/dict/set by transforming/
filtering an iterable. Used in Chapter 02.

**concurrent.futures** — A standard-library high-level interface for thread/process pools
(`ThreadPoolExecutor`). Used in Chapter 07.

**Entry point (console script)** — A `pyproject.toml` mapping that installs a Python
function as a shell command. Used in Chapters 06 and 09.

**Fixture** — A pytest construct providing reusable setup/teardown to tests. Used in
Chapter 08.

**GIL (Global Interpreter Lock)** — The lock that serializes Python bytecode execution;
released during I/O, so threads help I/O-bound but not CPU-bound work. Used in Chapter 07.

**Mocking** — Replacing an external dependency with a controllable stand-in in tests
(`unittest.mock`). Used in Chapter 08.

**mypy** — A static type checker for Python. Used in Chapter 08.

**pathlib** — The standard-library object-oriented path/file API (`Path`). Used in
Chapter 03.

**pip** — Python's package installer. Used in Chapters 01 and 09.

**pipx** — A tool that installs Python CLI applications each in an isolated environment.
Used in Chapter 09.

**pyproject.toml** — The standard project metadata/build/dependency configuration file.
Used in Chapters 01, 06, 09.

**pytest** — The standard testing framework (assert-based tests, fixtures,
parametrization). Used in Chapter 08.

**requests** — The de-facto HTTP client library for calling APIs. Used in Chapter 05.

**ruff** — A fast Python linter/formatter. Used in Chapter 08.

**subprocess** — The standard-library module for running external commands
(`subprocess.run`). Used in Chapter 04.

**Type hint** — An annotation declaring the expected type of a variable/parameter/return.
Used in Chapter 02.

**venv** — A standard-library virtual environment isolating a project's dependencies.
Used in Chapter 01.

**Wheel** — A built, installable Python package artifact (`.whl`). Used in Chapter 09.
