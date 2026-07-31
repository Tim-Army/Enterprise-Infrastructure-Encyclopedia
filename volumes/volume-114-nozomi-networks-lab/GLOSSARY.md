# Volume CXIV Glossary

Definitions for terms introduced in **Volume CXIV — Nozomi Networks Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Assertion** — a Nozomi rule expressing intent about protocol or process ("no writes from this VLAN", "this variable must stay in range"), authored centrally in Vantage.
- **Behavioral (process) baseline** — the learned normal usage of functions and the normal range of a process variable, used to flag deviations even on permitted flows.
- **Function code** — the field in a Modbus (or other OT) message that identifies the operation (read holding registers = 3, write single register = 6, etc.); the granularity function-aware policy acts on.
- **Function-aware proxy** — the Track 2 enforcer that parses the Modbus function code, permits reads, denies writes and non-Modbus, and checks read values against the learned range.
- **Guardian** — Nozomi's passive network sensor that dissects OT protocols on a SPAN and builds the network graph and process baselines.
- **Network graph** — the learned map of OT nodes, links, and the protocols/functions on each link.
- **Process anomaly** — a process variable outside its learned range (or an unexpected function), detected even when the flow itself is allowed.
- **Vantage** — Nozomi's SaaS console that aggregates many Guardians, holds alerts, and manages assertions fleet-wide.
- **Track 1 / Track 2** — the two lab paths: the real Nozomi Guardian/Vantage at design level (Track 1) and a buildable protocol-aware model with a Python Modbus server and function-aware proxy (Track 2).
