# Chapter 05: Working with APIs and HTTP

## Learning Objectives

- Call REST APIs with `requests`.
- Send authentication and handle JSON responses.
- Page through large result sets.
- Add timeouts and retries for reliability.
- Complete a walkthrough for each API skill.

## Theory and Architecture

Most infrastructure automation is **API calls** — to cloud providers, NetBox, Prometheus,
CI systems. The de-facto library is **`requests`** (or `httpx` for async): it makes HTTP
methods, headers, query params, and JSON handling simple. Production API code adds
**authentication** (bearer tokens/API keys in headers), **pagination** (following
`next` links or offset/limit), **timeouts** (never hang forever), and **retries** with
backoff (transient failures happen). A **`Session`** reuses connections and default
headers across calls.

## Design Considerations

Use a **`Session`** with default auth headers, always set a **timeout**, **page** through
all results rather than assuming one response, and **retry** idempotent requests with
backoff on 5xx/timeouts. Raise on error with `response.raise_for_status()`.

## Implementation and Automation

The labs use `requests` for GET/JSON, auth, pagination, and retries.

## Validation and Troubleshooting

Confirm the patterns:

```text
requests.get(url, headers={"Authorization": f"Bearer {t}"}, timeout=10)
-> r.raise_for_status(); r.json(). Pagination: follow 'next' / offset+limit.
Retries: urllib3 Retry on a Session adapter (backoff on 5xx/timeouts).
```

Common pitfalls: no **timeout** (hangs); and reading only the first page.

## Security and Best Practices

Use a **Session** with auth headers, always set **timeouts**, **page** fully, **retry**
idempotent calls with backoff, and `raise_for_status()`. Keep tokens in env vars, and
send them in headers (never in URLs).

## Hands-On Lab

API walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install requests`); a
reachable HTTP test endpoint (or a local service). **Cost:** none.

### Lab 5.1 — GET and parse JSON

**Objective:** Fetch and decode a JSON response.

```python
import requests
r = requests.get("https://httpbin.org/json", timeout=10)
r.raise_for_status()
print(type(r.json()))   # <class 'dict'>
```

**Expected result:** a parsed **dict** from the JSON body — the basic API call.

**Negative test:** call without `timeout`; a hung server **blocks forever** — always set
a timeout.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Authenticated session

**Objective:** Reuse auth across calls with a Session.

```python
import requests, os
s = requests.Session()
s.headers.update({"Authorization": f"Bearer {os.environ.get('API_TOKEN','x')}"})
r = s.get("https://httpbin.org/headers", timeout=10)
print("sent auth:", "Authorization" in r.json()["headers"])
```

**Expected result:** **`sent auth: True`** — auth headers applied via the Session.

**Negative test:** set auth per-request by hand each time; a **Session** applies defaults
consistently — use it.

**Rollback:** `s.close()`.

### Lab 5.3 — Paginate results

**Objective:** Follow pages to collect all items.

```python
def all_items(session, url):
    items = []
    while url:
        r = session.get(url, timeout=10); r.raise_for_status()
        body = r.json()
        items += body.get("results", [])
        url = body.get("next")          # follow the 'next' link
    return items
# print(len(all_items(s, "https://api.example/things")))
```

**Expected result:** all items across pages (following `next`) — complete pagination.

**Negative test:** return only the first page's `results`; you **miss data** — page until
`next` is null.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Retries with backoff

**Objective:** Retry transient failures automatically.

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
s = requests.Session()
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[502,503,504])
s.mount("https://", HTTPAdapter(max_retries=retry))
print("retries configured:", s.get_adapter("https://").max_retries.total)   # 3
```

**Expected result:** **`retries configured: 3`** — automatic backoff on 5xx.

**Negative test:** fail the whole run on one transient 503; **retry with backoff** rides
out blips.

**Rollback:** `s.close()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

API automation uses `requests` with a Session for auth, always-set timeouts, full
pagination, and retries with backoff — raising on error. This chapter called a JSON API,
applied auth, paginated, and configured retries.

- [ ] I can GET and parse JSON with a timeout.
- [ ] I can apply auth via a Session.
- [ ] I can paginate through all results.
- [ ] I can configure retries with backoff.
- [ ] I completed Labs 5.1–5.4 including each negative test.
