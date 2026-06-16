---
name: concurrent-cached-fetch
description: Write or refactor product code that performs many independent external API, HTTP, SDK, lookup, enrichment, or scraping calls so it uses bounded concurrency and a content-keyed disk cache. Use when Codex sees loops over `fetch`, `requests`, `httpx`, `urllib`, `axios`, SDK calls, per-item lookups, batch enrichment, slow sequential network code, or requests to cache repeated external calls.
---

# Concurrent Cached Fetch

Use this skill when product code performs more than a few independent external calls. The default pattern is:

1. Factor one request into a cached helper.
2. Key the cache by all request inputs.
3. Run independent calls through a bounded worker pool.
4. Preserve the caller's existing return shape and error contract.
5. Add the cache directory to `.gitignore`.

## Non-Negotiables

- Use bounded concurrency, typically 10-20 in-flight calls unless the upstream API has a stricter limit.
- Persist successful responses to disk using a content-keyed cache.
- Do not cache failures, timeouts, throttles, or malformed responses.
- Write cache entries atomically with a temporary file and rename.
- Provide an explicit bypass such as `refresh=true` or `CACHE_BYPASS=1`.
- Keep cache data out of version control.

## When Not To Use It

- Only one or two external calls happen in total.
- Calls are genuinely sequential because each request depends on the previous response.
- The project already has an equivalent cache and concurrency helper; use that local convention instead.
- The upstream API forbids caching or parallel requests.

## Implementation Workflow

1. Identify the fan-out collection and confirm requests are independent.
2. Find the existing HTTP or SDK style in the codebase.
3. Implement or reuse a single-call helper that checks disk cache, performs the live call on miss, and writes only successful responses.
4. Add bounded concurrency around the collection while preserving input order if downstream code expects it.
5. Keep per-item failures isolated unless the existing API intentionally fails the whole batch.
6. Add cache directory hygiene to `.gitignore`.
7. Verify with a small run, a cached re-run, and a bypass run when practical.

## Cache Key Requirements

The cache key must include everything that determines the response:

- HTTP method
- full URL
- sorted query parameters
- request body for POST, PUT, or PATCH
- relevant headers only when they affect the response and are safe to hash

Use a stable serialization and SHA-256 or an equivalent strong hash. Do not include secrets in logged cache keys or cache filenames.

## Reference Patterns

Read `references/patterns.md` when writing the actual code. It contains ready-to-adapt patterns for:

- Python with `requests` and `ThreadPoolExecutor`
- Python async with `httpx`
- JavaScript/TypeScript with `fetch`
- Go with bounded goroutines
- Java with `ExecutorService`

Adapt the pattern to the repository's existing conventions rather than pasting it blindly.
