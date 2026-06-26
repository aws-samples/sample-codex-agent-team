# Concurrent + Cached Fetch — Implementation Patterns

Ready-to-adapt building blocks. Pick the language/HTTP-client pair that matches the
project. Each pattern combines a **bounded concurrency** primitive with a **content-keyed
disk cache (no expiry, manual bypass)**. Adapt names and error handling to the
surrounding code; don't paste verbatim if the project has its own conventions.

## Table of contents
- [Cache key + atomic write (language-agnostic recipe)](#cache-key--atomic-write)
- [Python: threaded + cached `requests`](#python-threaded--cached-requests) ← most common
- [Python: asyncio + cached `httpx`](#python-asyncio--cached-httpx)
- [JS/TS: `Promise` pool + cached `fetch`](#jsts-promise-pool--cached-fetch)
- [Go: bounded goroutines + cached `net/http`](#go-bounded-goroutines--cached-nethttp)
- [Java: `ExecutorService` + cached `HttpClient`](#java-executorservice--cached-httpclient)

---

## Cache key + atomic write

The key is a stable hash of everything that determines the response. The write is atomic
so a crash never leaves a corrupt entry that later reads as valid.

- **Key inputs:** HTTP method, full URL, sorted query params, and request body (for
  POST/PUT). Serialize them canonically (sorted keys), then SHA-256.
- **Filename:** `<cache_dir>/<hexdigest>.json`.
- **Atomic write:** write to `<file>.tmp.<pid>`, then `rename()` onto the final path —
  rename is atomic on POSIX, so readers see either the old file or the complete new one,
  never a partial.
- **No expiry:** if the file exists, use it. The only bypass is an explicit
  `refresh`/`CACHE_BYPASS` flag, which forces a live call and overwrites.
- **Never cache failures:** only write after a confirmed-success response.

---

## Python: threaded + cached `requests`

The default for code already using the blocking `requests` library. Threads are the
right tool — these calls are I/O-bound, so the GIL is released during the socket wait and
threads give real concurrency.

```python
import os, json, hashlib, threading
from concurrent.futures import ThreadPoolExecutor
import requests

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache", "api")
os.makedirs(CACHE_DIR, exist_ok=True)
_MAX_WORKERS = 12  # bounded: enough to collapse wait, polite to public APIs

def _cache_key(method, url, params=None, body=None):
    blob = json.dumps(
        {"m": method.upper(), "u": url, "p": params or {}, "b": body},
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(blob.encode()).hexdigest()

def cached_get(url, params=None, *, refresh=False, timeout=10):
    """GET with content-keyed disk cache (no expiry). Returns parsed JSON or text.
    Only successful responses are cached; failures raise so the caller can apply
    its own error contract and so the failure is never persisted."""
    bypass = refresh or os.environ.get("CACHE_BYPASS") == "1"
    key = _cache_key("GET", url, params)
    path = os.path.join(CACHE_DIR, f"{key}.json")

    if not bypass and os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()  # don't cache errors — let the caller retry live next run
    try:
        data = resp.json()
    except ValueError:
        data = {"_text": resp.text}

    tmp = f"{path}.tmp.{os.getpid()}.{threading.get_ident()}"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, path)  # atomic
    return data

def fetch_all(items, fetch_one, max_workers=_MAX_WORKERS):
    """Map fetch_one over items concurrently, preserving input order.
    fetch_one(item) should return a result or raise; exceptions are captured
    per-item so one failure never aborts the batch."""
    results = [None] * len(items)
    def work(i_item):
        i, item = i_item
        try:
            results[i] = fetch_one(item)
        except Exception as e:
            results[i] = {"error": str(e), "item": item}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        list(pool.map(work, enumerate(items)))
    return results
```

Applied to a two-step lookup tool: the per-ID details loop becomes
`fetch_all(id_list, lambda i: cached_get(DETAILS_API_URL.format(id=i)))`, and the
top-level term→IDs lookup uses `cached_get`. Keep the tool's existing return shape and
error encoding — wrap the helpers, don't change the public contract.

---

## Python: asyncio + cached `httpx`

When the project is already async (FastAPI, `httpx.AsyncClient`, `aiohttp`). A `Semaphore`
provides the bound; `asyncio.gather` fans out.

```python
import os, json, hashlib, asyncio, httpx

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache", "api")
os.makedirs(CACHE_DIR, exist_ok=True)
_SEM = asyncio.Semaphore(12)  # bounded concurrency

def _cache_key(method, url, params=None, body=None):
    blob = json.dumps({"m": method.upper(), "u": url, "p": params or {}, "b": body},
                      sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()

async def cached_get(client, url, params=None, *, refresh=False):
    bypass = refresh or os.environ.get("CACHE_BYPASS") == "1"
    key = _cache_key("GET", url, params)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if not bypass and os.path.exists(path):
        return json.load(open(path))
    async with _SEM:  # cap in-flight requests
        resp = await client.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    tmp = f"{path}.tmp.{os.getpid()}"
    json.dump(data, open(tmp, "w"))
    os.replace(tmp, path)
    return data

async def fetch_all(items, build_call):
    """build_call(client, item) -> coroutine. Returns results in input order;
    failures become {'error': ...} instead of aborting the batch."""
    async with httpx.AsyncClient() as client:
        async def guarded(item):
            try:
                return await build_call(client, item)
            except Exception as e:
                return {"error": str(e), "item": item}
        return await asyncio.gather(*(guarded(it) for it in items))
```

---

## JS/TS: `Promise` pool + cached `fetch`

No native bounded-pool primitive, so cap manually (a small worker-drain loop, or a
library like `p-limit` if it's already a dependency). Cache to disk with `fs`.

```ts
import { createHash } from "node:crypto";
import { promises as fs } from "node:fs";
import * as path from "node:path";

const CACHE_DIR = path.join(process.cwd(), ".cache", "api");
const MAX_CONCURRENCY = 12;

const cacheKey = (method: string, url: string, params?: object, body?: unknown) =>
  createHash("sha256")
    .update(JSON.stringify({ m: method.toUpperCase(), u: url, p: params ?? {}, b: body ?? null }))
    .digest("hex");

export async function cachedGet(url: string, refresh = false): Promise<any> {
  await fs.mkdir(CACHE_DIR, { recursive: true });
  const bypass = refresh || process.env.CACHE_BYPASS === "1";
  const file = path.join(CACHE_DIR, `${cacheKey("GET", url)}.json`);
  if (!bypass) {
    try { return JSON.parse(await fs.readFile(file, "utf8")); } catch { /* miss */ }
  }
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`); // don't cache failures
  const data = await resp.json();
  const tmp = `${file}.tmp.${process.pid}`;
  await fs.writeFile(tmp, JSON.stringify(data));
  await fs.rename(tmp, file); // atomic
  return data;
}

// Bounded fan-out preserving input order.
export async function fetchAll<T, R>(items: T[], one: (x: T) => Promise<R>,
                                     limit = MAX_CONCURRENCY): Promise<(R | { error: string })[]> {
  const results = new Array(items.length);
  let next = 0;
  const worker = async () => {
    while (next < items.length) {
      const i = next++;
      try { results[i] = await one(items[i]); }
      catch (e: any) { results[i] = { error: String(e?.message ?? e) }; }
    }
  };
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
```

---

## Go: bounded goroutines + cached `net/http`

A buffered channel is the idiomatic semaphore; `sync.WaitGroup` joins.

```go
package fetch

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
)

const maxConcurrency = 12

var cacheDir = filepath.Join(".cache", "api")

func cacheKey(method, url string) string {
	sum := sha256.Sum256([]byte(method + " " + url))
	return hex.EncodeToString(sum[:])
}

// CachedGet returns the raw body, served from disk on a hit. Failures are not cached.
func CachedGet(url string, refresh bool) ([]byte, error) {
	_ = os.MkdirAll(cacheDir, 0o755)
	path := filepath.Join(cacheDir, cacheKey("GET", url)+".json")
	if !refresh && os.Getenv("CACHE_BYPASS") != "1" {
		if b, err := os.ReadFile(path); err == nil {
			return b, nil
		}
	}
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP %d", resp.StatusCode) // don't cache errors
	}
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	tmp := fmt.Sprintf("%s.tmp.%d", path, os.Getpid())
	if err := os.WriteFile(tmp, body, 0o644); err == nil {
		_ = os.Rename(tmp, path) // atomic
	}
	return body, nil
}

// FetchAll maps one() over items with bounded concurrency, preserving order.
func FetchAll[T any, R any](items []T, one func(T) (R, error)) []R {
	results := make([]R, len(items))
	sem := make(chan struct{}, maxConcurrency)
	var wg sync.WaitGroup
	for i, item := range items {
		wg.Add(1)
		go func(i int, item T) {
			defer wg.Done()
			sem <- struct{}{}        // acquire
			defer func() { <-sem }() // release
			r, _ := one(item)        // apply your own per-item error handling
			results[i] = r
		}(i, item)
	}
	wg.Wait()
	return results
}
```

(For body-encoded JSON output, marshal the cached bytes back via `json.Unmarshal`.)

---

## Java: `ExecutorService` + cached `HttpClient`

A fixed thread pool bounds concurrency; `invokeAll` fans out and preserves order.

```java
import java.net.URI;
import java.net.http.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;

public final class CachedFetch {
    private static final Path CACHE_DIR = Path.of(".cache", "api");
    private static final int MAX_CONCURRENCY = 12;
    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    private static String cacheKey(String method, String url) throws Exception {
        var md = MessageDigest.getInstance("SHA-256");
        byte[] d = md.digest((method + " " + url).getBytes());
        var sb = new StringBuilder();
        for (byte b : d) sb.append(String.format("%02x", b));
        return sb.toString();
    }

    /** GET with content-keyed disk cache (no expiry). Failures are not cached. */
    public static String cachedGet(String url, boolean refresh) throws Exception {
        Files.createDirectories(CACHE_DIR);
        Path path = CACHE_DIR.resolve(cacheKey("GET", url) + ".json");
        boolean bypass = refresh || "1".equals(System.getenv("CACHE_BYPASS"));
        if (!bypass && Files.exists(path)) return Files.readString(path);

        var req = HttpRequest.newBuilder(URI.create(url)).GET().build();
        HttpResponse<String> resp = CLIENT.send(req, HttpResponse.BodyHandlers.ofString());
        if (resp.statusCode() != 200) throw new RuntimeException("HTTP " + resp.statusCode());

        Path tmp = CACHE_DIR.resolve(path.getFileName() + ".tmp." + ProcessHandle.current().pid());
        Files.writeString(tmp, resp.body());
        Files.move(tmp, path, StandardCopyOption.ATOMIC_MOVE);
        return resp.body();
    }

    /** Map one() over items with bounded concurrency, preserving input order. */
    public static <T, R> List<R> fetchAll(List<T> items, java.util.function.Function<T, R> one)
            throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(MAX_CONCURRENCY);
        try {
            List<Callable<R>> tasks = new ArrayList<>();
            for (T item : items) tasks.add(() -> one.apply(item));
            List<Future<R>> futures = pool.invokeAll(tasks); // order preserved
            List<R> out = new ArrayList<>();
            for (Future<R> f : futures) {
                try { out.add(f.get()); } catch (ExecutionException e) { out.add(null); }
            }
            return out;
        } finally {
            pool.shutdown();
        }
    }
}
```

---

## Checklist before you call the fetch code done

- [ ] Independent calls run concurrently with a **bounded** pool (~10–20).
- [ ] Every successful response is written to a **disk** cache, keyed by request content.
- [ ] Cache has **no expiry**; a `refresh` arg / `CACHE_BYPASS=1` env var forces a live call.
- [ ] Failures are **not** cached; one item's error doesn't abort the batch.
- [ ] Cache writes are **atomic** (temp + rename).
- [ ] Cache dir is in **`.gitignore`**.
- [ ] The surrounding code's **error/return contract** is preserved per item.
