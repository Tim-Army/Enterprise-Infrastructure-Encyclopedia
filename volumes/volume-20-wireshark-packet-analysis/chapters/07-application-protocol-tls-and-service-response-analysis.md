# Chapter 07: Application Protocol, TLS, and Service-Response Analysis

![Lab flow for this chapter: with a TLS session-key log enabled, an HTTPS request populates a key log file, and pointing Wireshark's TLS pre-master-secret log preference at that file reveals decrypted HTTP request/response frames with a populated response-time value. As a negative test, the TLS key log preference is cleared and the capture reloaded; the same HTTP filter now matches nothing, since the identical records dissect only as encrypted TLS — confirming decryption genuinely depended on the configured key log rather than some other mechanism.](../../../diagrams/volume-20-wireshark-packet-analysis/chapter-07-tls-decryption-keylog-flow.svg)

*Figure 7-1. Flow used throughout this chapter's Hands-On Lab: an HTTPS session decrypted in Wireshark via a session-key log, tested against a cleared key log preference.*

## Learning Objectives

- Decode an HTTP/1.1 request/response exchange and identify the HTTP/2
  framing differences that change how Wireshark presents equivalent
  traffic.
- Read a TLS 1.2 and TLS 1.3 handshake, including the Client Hello, Server
  Hello, SNI extension, and cipher suite negotiation.
- Decrypt TLS traffic in Wireshark using a captured pre-master-secret/
  session-key log, and explain the prerequisites that make decryption
  possible.
- Measure application-layer service response time directly from a capture
  using Wireshark's built-in timing fields.
- Recognize the packet-level signature of common service-response
  failures: slow backend, TLS handshake failure, and HTTP error responses.

## Theory and Architecture

[Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md) established how TCP delivers a reliable byte stream; this
chapter analyzes what rides inside that stream — HTTP and TLS specifically,
as the application protocols an enterprise analyst encounters most — and
how to measure how quickly a service actually responded once the
transport-layer handshake behavior from [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md) is no longer the
bottleneck.

### HTTP/1.1 and HTTP/2 in Wireshark

HTTP/1.1 request and response messages dissect as a familiar, mostly
plain-text structure:

```text
Hypertext Transfer Protocol
    GET /index.html HTTP/1.1\r\n
    Host: www.example.com\r\n
    User-Agent: ...\r\n
    [Full request URI: http://www.example.com/index.html]
    [Response in frame: 48]
```

Wireshark automatically links each request to its matching response
(`[Response in frame: N]` / `[Request in frame: N]`), computes the elapsed
time between them, and exposes it as `http.time` — the single most useful
field for HTTP-layer response measurement.

HTTP/2, in contrast, multiplexes many logical streams over one TCP (or
QUIC, for HTTP/3) connection using a binary framing layer. Wireshark
dissects HTTP/2 as a sequence of frames (`HEADERS`, `DATA`, `SETTINGS`,
`WINDOW_UPDATE`) tagged with a stream identifier, reassembling and
displaying header fields similarly to HTTP/1.1 but keyed by
`http2.streamid` rather than one request/response pair per TCP segment.
Because HTTP/2 traffic is almost always also TLS-encrypted in enterprise
use (commonly negotiated via the TLS ALPN extension), inspecting it in
Wireshark requires the same decryption prerequisite covered below for TLS
generally.

### TLS handshake structure

TLS establishes a secure channel before any application data is
exchanged. The handshake differs meaningfully between TLS 1.2 and TLS 1.3:

```text
TLS 1.2 handshake (simplified):
    Client Hello        (client → server: supported versions, cipher suites, SNI)
    Server Hello        (server → client: chosen version, cipher suite)
    Certificate
    Server Key Exchange
    Server Hello Done
    Client Key Exchange
    Change Cipher Spec, Finished   (both directions)

TLS 1.3 handshake (simplified):
    Client Hello        (includes key_share — key exchange starts immediately)
    Server Hello, {Certificate, Finished}   (encrypted after Server Hello)
    Client: Finished
    [Application Data may begin after this single round trip]
```

TLS 1.3 collapses the handshake to one round trip by having the client
send its key share in the initial Client Hello, which is the primary
reason TLS 1.3 connections establish measurably faster than TLS 1.2 —
directly observable in Wireshark by counting handshake round trips before
the first `Application Data` record.

The **Server Name Indication (SNI)** extension in the Client Hello
(`tls.handshake.extensions_server_name`) is unencrypted in TLS 1.2 and,
absent Encrypted Client Hello (ECH) deployment, typically remains visible
in TLS 1.3 as well — it is what allows Wireshark (and any on-path
observer) to identify the requested hostname even though the rest of the
conversation is encrypted, and it is the field most security monitoring
tools key on for TLS-encrypted traffic they cannot otherwise inspect.

### Service response time

Beyond `http.time`, Wireshark computes protocol-appropriate elapsed-time
fields for several application dissectors (for example, `smb2.time` for
SMB2). Where no dissector-native timing field exists, the general-purpose
approach is measuring the delta between the last byte of a request and the
first byte of the corresponding response using `tcp.time_delta` (Chapter
03) on the relevant stream, combined with Follow Stream to confirm which
segments constitute the request and response boundaries.

## Design Considerations

- **Decryption requires a secret captured at the time of the session, not
  after.** TLS decryption in Wireshark depends on either a session-key log
  file generated by the client/server at connection time
  (`SSLKEYLOGFILE`) or the server's static RSA private key for the narrow
  set of legacy cipher suites that still permit it — modern cipher suites
  using ephemeral (forward-secret) key exchange cannot be decrypted after
  the fact from the private key alone, even with full server access.
- **Decrypting production traffic is a policy decision, not just a
  technical one.** Enabling `SSLKEYLOGFILE` on a production browser or
  service, or extracting a private key, both have real security
  implications; confirm authorization and scope before configuring
  decryption outside a lab or an authorized investigation ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)'s
  evidentiary-handling guidance applies directly).
- **Multiplexed HTTP/2 streams complicate simple request/response
  timing.** Because many logical HTTP/2 streams share one TCP connection,
  a slow single stream does not necessarily mean the connection or server
  is generally slow; filter by `http2.streamid` before drawing a
  conclusion from aggregate connection timing.
- **SNI-based visibility has limits.** An analyst relying on SNI alone to
  identify traffic should account for Encrypted Client Hello deployments
  and for TLS connections that omit SNI (some non-browser clients),
  neither of which will expose a plaintext hostname.
- **Response time measured in a capture reflects the capture point.**
  `http.time` measured at the client reflects the full round trip
  including network latency; the same measurement taken from a capture at
  the server reflects server processing time much more directly —
  choose (or duplicate) the capture point deliberately based on which
  question is being asked.

## Implementation and Automation

### HTTP filters and timing

```text
http                                    # all HTTP traffic
http.request.method == "GET"
http.response.code >= 400               # client/server error responses
http.time > 1.0                         # responses slower than 1 second
```

```bash
# List every HTTP request path with its response time, slowest first.
tshark -r capture.pcapng -Y "http.time" -T fields \
  -e frame.time -e http.request.full_uri -e http.time \
  | sort -k3 -rn | head -20
```

### HTTP/2 filters

```text
http2
http2.type == 1                         # HEADERS frame
http2.streamid == 5                     # one logical stream
http2.flags.end_stream == 1             # stream completion
```

### TLS handshake filters

```text
tls.handshake.type == 1                 # Client Hello
tls.handshake.type == 2                 # Server Hello
tls.handshake.extensions_server_name == "www.example.com"
tls.handshake.type == 11                # Certificate
tls.alert_message                       # any TLS alert (handshake or session failure)
tls.record.version == 0x0304            # TLS 1.3 record
```

Extract negotiated cipher suites across a capture to audit for weak
suites still in use:

```bash
tshark -r capture.pcapng -Y "tls.handshake.type==2" -T fields \
  -e ip.dst -e tls.handshake.ciphersuite
```

### Decrypting TLS with a session-key log

1. Set the environment variable before starting the client application (a
   browser, `curl`, or any TLS library that honors it) so it logs
   per-session secrets as connections are made:

   ```bash
   export SSLKEYLOGFILE=~/tls-keys.log
   ```

2. Capture traffic normally while the instrumented client runs.
3. In Wireshark, configure the key log file:
   **Edit > Preferences > Protocols > TLS > (Pre)-Master-Secret log
   filename**, point it at `~/tls-keys.log`.
4. Reload or re-open the capture. Decrypted `Application Data` records now
   dissect as their underlying protocol (commonly HTTP or HTTP/2) instead
   of opaque encrypted bytes, and Follow Stream ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)) works on the
   decrypted content directly.

`tshark` performs the same decryption non-interactively for scripted
extraction:

```bash
tshark -r capture.pcapng -o "tls.keylog_file:tls-keys.log" \
  -Y "http" -T fields -e http.request.full_uri
```

## Validation and Troubleshooting

- **TLS handshake completes but Application Data stays encrypted after
  configuring the key log.** Confirm the key log file actually contains
  entries with a `CLIENT_RANDOM` (TLS ≤1.2) or the TLS 1.3 secret labels
  matching the captured session's Client Hello random value — a key log
  generated by a different process instance, or after the session
  started, will not match.
- **Handshake fails with a TLS Alert before Application Data.** Filter
  `tls.alert_message` and read the alert's description field — common
  causes include certificate validation failure (`certificate_unknown`,
  `unknown_ca`), protocol version mismatch, or no shared cipher suite
  between client and server.
- **HTTP request shows no matching response.** Confirm the TCP stream did
  not reset or time out before a response was sent
  (`tcp.stream==<N> && tcp.flags.reset==1`, [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md)); a genuinely
  missing response is a server- or path-level failure, not an HTTP
  dissection issue.
- **`http.time` reports an implausibly large value.** Confirm the request
  and matched response are actually on the same TCP stream and not an
  artifact of HTTP pipelining or connection reuse matching the wrong pair;
  cross-check against `tcp.stream` and the raw frame numbers in
  `[Response in frame: N]`.
- **HTTP/2 stream appears incomplete.** Confirm
  `http2.flags.end_stream==1` was reached for that `http2.streamid`; a
  stream lacking this flag was still open when the capture ended, which is
  expected for long-lived streams (server push, ongoing downloads) rather
  than necessarily a fault.

## Security and Best Practices

- **Never commit a `SSLKEYLOGFILE` or a captured private key to a
  repository or share it outside the authorized investigation.** Both
  fully compromise the confidentiality of any traffic they can decrypt,
  including traffic beyond the specific session under investigation if
  the key is long-lived.
- **Confirm authorization before enabling TLS decryption on any traffic
  the analyst is not personally the client for.** Organizational policy,
  legal, and privacy requirements govern decrypting other users' traffic
  even on organization-owned infrastructure; this is a governance
  decision, not solely a technical capability.
- **Audit negotiated cipher suites and TLS versions periodically**, using
  the extraction pattern shown above, to catch legacy TLS 1.0/1.1 or weak
  cipher suite usage that should have been disabled per organizational
  policy.
- **Watch for TLS handshakes with anomalous SNI-to-certificate
  mismatches** or self-signed certificates presented for well-known
  hostnames — both are signatures worth escalating, especially combined
  with the security investigation techniques in [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md).
- **Redact decrypted Follow Stream output aggressively before sharing.**
  Once TLS is decrypted, the same handling discipline that applies to any
  cleartext protocol ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)) applies to the decrypted content —
  credentials, tokens, and personal data are now fully visible in the
  capture.

## References and Knowledge Checks

**References**

- [Wireshark User's Guide, "TLS Decryption" and protocol reference
  appendix (HTTP, HTTP/2, TLS dissectors) (current for the 4.4.x release
  line).](https://www.wireshark.org/docs/wsug_html_chunked/)
- IETF [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)/9112 (HTTP semantics/HTTP\1.1), [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) (HTTP/2), RFC
  8446 (TLS 1.3).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. Why does TLS 1.3 typically establish a connection in fewer round trips
   than TLS 1.2, and how is that difference directly observable in a
   capture?
2. What must be captured at the time of a TLS session — not after — for
   Wireshark to be able to decrypt it, and why does this requirement exist
   for modern cipher suites?
3. What does the `http.time` field measure, and why does the capture
   point (client-side vs. server-side) change how that measurement should
   be interpreted?
4. Why can SNI remain visible even in an otherwise fully encrypted TLS
   1.3 session, and what deployment changes that?

## Hands-On Lab

**Objective:** Capture an HTTPS session with a session-key log enabled,
decrypt it in Wireshark, and measure the underlying HTTP response time.

**Prerequisites**

- Wireshark and `tshark` installed with capture rights ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)).
- A TLS-capable client that honors `SSLKEYLOGFILE` (most Chromium- and
  Firefox-based browsers, and `curl` built against a compatible TLS
  library).
- Network access to an HTTPS site for the lab request.

**Steps**

1. Set the key log environment variable and start the capture:

   ```bash
   export SSLKEYLOGFILE=~/lab07-tls-keys.log
   rm -f ~/lab07-tls-keys.log
   tshark -i <INTERFACE_NUMBER> -f "tcp port 443" -w lab07.pcapng &
   ```

2. Generate an HTTPS request using the instrumented client (browser
   navigation to an HTTPS site, or `curl` if built with key-log support):

   ```bash
   curl -o /dev/null -s -w "%{http_code}\n" https://example.com/
   ```

3. Stop the capture:

   ```bash
   kill %1
   ```

4. Confirm the key log file was populated:

   ```bash
   wc -l ~/lab07-tls-keys.log
   ```

   **Expected result:** at least one line, typically beginning with
   `CLIENT_HANDSHAKE_TRAFFIC_SECRET` or `CLIENT_RANDOM` depending on TLS
   version.

5. Open `lab07.pcapng` in Wireshark and configure the key log path
   (**Edit > Preferences > Protocols > TLS > (Pre)-Master-Secret log
   filename**), pointing to `~/lab07-tls-keys.log`.
6. Apply the filter:

   ```text
   http
   ```

   **Expected result:** decrypted HTTP request/response frames appear
   (rather than only opaque `Application Data` records), confirming
   successful decryption.
7. Check the response timing:

   ```text
   http.time
   ```

   **Expected result:** the matched response shows a populated
   `http.time` value in the Packet Detail pane under the HTTP layer.
8. **Negative test:** Clear the TLS key log preference
   (**Edit > Preferences > Protocols > TLS**, clear the filename field),
   reload the capture, and re-apply the `http` filter.

   **Expected result:** no HTTP-layer matches — the same
   `Application Data` records now dissect only as encrypted TLS, confirming
   that decryption genuinely depended on the configured key log rather
   than some other mechanism.
9. **Cleanup:** Remove the lab capture and the key log file, and unset the
   environment variable:

   ```bash
   rm -f lab07.pcapng ~/lab07-tls-keys.log
   unset SSLKEYLOGFILE
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

HTTP and TLS dissection turns an encrypted application conversation into
readable request/response pairs and a measurable handshake timeline, but
only when the analyst captures the right decryption material at the right
time — after the fact is too late for modern, forward-secret cipher
suites. Service response time measured directly from a capture (`http.time`
and its equivalents) is frequently a more trustworthy source of truth than
application-level logging, because it reflects what was actually observed
on the wire rather than what the application reported about itself.
[Chapter 08](08-security-investigation-command-line-analysis-and-automation.md) moves from protocol analysis to security investigation and
command-line automation, building on every filter and field introduced in
Chapters 04 through 07.

- [ ] Can decode an HTTP/1.1 request/response pair and explain HTTP/2's
      stream-multiplexed framing.
- [ ] Can read a TLS handshake and identify the round-trip difference
      between TLS 1.2 and TLS 1.3.
- [ ] Configured and validated TLS decryption using a session-key log.
- [ ] Can measure application-layer response time using `http.time` and
      explain how capture point changes its interpretation.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
