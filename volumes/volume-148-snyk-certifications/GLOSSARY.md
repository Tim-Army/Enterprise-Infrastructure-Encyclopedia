# Volume CXLVIII — Glossary

| Term | Definition |
|:---|:---|
| **ASPM** | Application Security Posture Management — a cross-cutting view of security across the whole SDLC and application portfolio: which apps exist, which are critical, where coverage gaps are, how risk trends. Answers "across all our apps, where is our risk?" |
| **Base-image recommendation** | Snyk Container's signature move: because most image vulnerabilities come from the shared base image, changing the base (to slim/alpine/newer) fixes many CVEs at once across every image that inherits it. The container form of fix-at-the-source. |
| **Certificate of Completion** | The credential Snyk Learn awards for finishing a learning path — a downloadable PDF, tracked by a free account. A learning credential, not a proctored-exam certification. |
| **DeepCode AI** | The AI engine behind Snyk Code, trained on millions of commits and fixes to raise SAST accuracy (cut false positives) and suggest fixes. |
| **Developer-first** | Delivering security to developers in their own workflow (IDE, CLI, PR, CI/CD) with actionable fixes, rather than a separate team's late report — because security developers actually use beats more-thorough security they ignore. |
| **Excessive agency** | The top agentic-AI risk: an AI agent given more tools/power than its task needs, which — combined with prompt injection — can be steered to act maliciously. Countered with least privilege on agent tools. |
| **False positive** | A finding flagged as vulnerable that is not. A security failure, not a nuisance: a noisy tool gets muted, and a muted tool secures nothing. Accuracy is therefore a security property. |
| **Learning path** | A sequence of interactive Snyk Learn lessons on a topic, ending in a Certificate of Completion (e.g. Security for Developers, OWASP Top 10, Secure AI Development). |
| **Policy-as-code** | Security rules ("no public buckets," "encryption required") expressed as code that runs in the pipeline and fails the pull request on violation — executable, versioned, consistently enforced. |
| **Prompt injection** | Untrusted input that manipulates an LLM's instructions — the source-to-sink data-flow problem in AI form, and a top OWASP LLM risk. |
| **Reachability** | Whether your code actually calls a vulnerable function. A critical vulnerability in a never-called function is dead weight, not live risk; reachability sharply reorders the priority queue. |
| **SAST** | Static Application Security Testing — analyzing your first-party source for insecure patterns (injection, XSS) via data-flow analysis (untrusted source → unsanitized → dangerous sink). Snyk Code. |
| **SCA** | Software Composition Analysis — inventorying open-source dependencies (including transitive ones) against a vulnerability database. Snyk Open Source. The largest attack surface in most apps. |
| **Snyk Learn** | Snyk's free, interactive developer-security education and product-training program — learning paths and lessons awarding certificates of completion. Not proctored exams. |
| **Transitive dependency** | A dependency of a dependency — a package you never directly chose but ship anyway. Most of an app's packages and dependency vulnerabilities are transitive, requiring full-tree analysis to find. |
