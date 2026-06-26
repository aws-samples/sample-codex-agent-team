---
name: concurrent-cached-fetch
description: >-
  Write product code that fetches from external APIs concurrently and caches every
  response to disk, instead of looping calls one-at-a-time with no reuse. Use this
  skill WHENEVER you are writing or refactoring code that makes more than a handful
  of independent network calls — REST/HTTP APIs, terminology or lookup services,
  third-party SDKs, web scraping, batch enrichment, fan-out over a list of terms/IDs.
  Trigger it the moment you see (or are about to write) a `for` loop with a
  `requests.get` / `fetch` / `httpx` / `urllib` call inside, repeated lookups over a
  collection, or any "enrich each item by calling service X" pattern. Also use it when
  asked to speed up slow sequential API code, add caching to network calls, or make a
  tool/function that hits an external endpoint per item. Default to this pattern even
  if the user only says "fetch these" or "look these up" — sequential uncached I/O is
  the thing to avoid.
---

# Concurrent + Cached External Fetching

Sequential, uncached external calls are the single most common avoidable performance
sink in agent-written code. Ten lookups that each take 300 ms run in 3 seconds when
serialized; fanned out they finish in ~300 ms. And on the *next* run — a re-analysis, a
follow-up question, a re-run after an unrelated bug fix — uncached code pays that cost
all over again, plus hammers a public endpoint that may rate-limit or ban you.

This skill exists to make two properties the default for any code that touches the
network in bulk:

1. **Concurrency** — independent calls run in parallel, at least ~10 in flight at once.
2. **Disk caching** — every response is persisted, keyed by request content, so an
   identical call is served from disk and never re-issued unless explicitly refreshed.

These are *code patterns you write into the product*, not something you do by hand. The
goal is that the code stays fast and cache-warm every time it runs, including in
follow-up work.

## When this applies

Reach for this skill whenever the work involves **N independent external calls where N
is more than a few** and the calls don't depend on each other's results. Concrete tells:

- A loop body contains `requests.get/post`, `httpx`, `urllib`, `fetch`, `axios`, an SDK
  client call, or any HTTP/RPC to a service you don't control.
- "Enrich / look up / resolve / annotate **each** of these <items>."
- Refactoring code that already loops calls sequentially and feels slow.
- A two-step API (find an ID, then fetch details per ID) — the inner per-ID fetches are
  the fan-out.

If the calls are genuinely dependent (call B needs call A's result), you can't
parallelize *those two*, but you can usually still parallelize across the outer items.

If only one or two calls happen total, don't over-engineer — a single cached call is
fine, concurrency buys nothing.

**Apply this even when the user never says "slow" or "cache".** A prompt like "look up
the details for each ID in this list" or "get the price for each of these 80 SKUs"
*is* a bulk-fetch task — the fan-out and the disk cache are the right default, not an
optimization to bolt on later when someone complains. The model will usually parallelize
on its own once a task is framed as slow; the durable win this skill adds is the
**persistent, content-keyed disk cache plus the hygiene around it** (don't cache
failures, atomic writes, gitignore), which survives across runs and follow-up analysis.
That payoff only happens if you build it in from the first version, so reach for this
skill the moment you see "for each <item>: call <external service>", regardless of how
the request is phrased.

## The two non-negotiables (and the why)

### 1. Fan out — at least ~10 concurrent

Serialized network I/O wastes wall-clock time doing nothing but waiting on sockets. The
fix is to issue independent requests concurrently with a **bounded** worker pool. Bounded
matters: unbounded concurrency over a public API gets you throttled or blocked, and
exhausts local file descriptors. A cap of ~10–20 is the sweet spot for most public
endpoints — enough to collapse the wait, polite enough not to trip rate limits.

Pick the idiom that fits the codebase's language and existing style — see
`references/patterns.md` for ready-to-adapt implementations in Python (threads for the
common `requests`-style blocking client; asyncio for `httpx`/`aiohttp`), JS/TS, Go, and
Java. Match what the project already uses rather than introducing a new async stack.

### 2. Cache every response to disk, keyed by request content

The cache key is a hash of everything that determines the response — method, full URL,
query params, and (for POST) the body. Identical request → same key → served from disk.
This makes re-runs and follow-up analysis instant and keeps you off the wire.

**Default cache policy: content-keyed, no expiry.** Entries do not auto-expire. They are
reused indefinitely until explicitly invalidated, because the data these calls return
(reference data, code systems, catalogs, documentation) is typically stable on the
timescale of a work session and re-fetching it buys nothing. Provide a single escape
hatch — a `refresh=True` argument or a `CACHE_BYPASS=1` env var — that forces a live call
and overwrites the cached entry, for the rare case where you know the upstream changed.
Don't build TTL/expiry machinery unless the data is genuinely time-sensitive; for stable
reference data it's complexity you don't need.

Cache location and hygiene:
- Store under a project-local dir such as `.cache/api/` (or honor an existing project
  cache convention if one exists).
- **Add the cache dir to `.gitignore`** — cached responses are derived data, never
  committed.
- Write atomically (temp file + rename) so a crashed run can't leave a half-written
  entry that later parses as valid.
- Only cache successful responses. Caching an error (a 500, a timeout) poisons the cache
  — a later run would replay the failure forever. On failure, don't write; let the next
  run retry live.

See `references/patterns.md` for a drop-in disk-cache wrapper in each language.

## How to apply it

1. **Spot the fan-out.** Identify the collection being iterated and confirm the calls
   are independent. That collection is what you parallelize over.
2. **Wrap the single call in a cached fetch.** Factor the one-item network call into a
   function `fetch(request) -> response` that checks disk first, calls live on a miss,
   and writes the result on success. This keeps caching in one place.
3. **Run the collection through a bounded pool.** Map the cached fetch over all items
   with a concurrency cap (~10–20). Preserve input order in the results if downstream
   code expects it.
4. **Keep the existing error contract.** If the surrounding code has a convention for
   failures (e.g. tools that always return a structured result and never raise),
   preserve it per item. One item's failure must not abort the whole batch or corrupt
   the cache.
5. **Make the cache visible and bypassable.** Ensure the cache dir is gitignored and the
   `refresh`/`CACHE_BYPASS` escape hatch works.

## Worked trigger: a two-step lookup service

The canonical case is a "find, then fetch details per result" tool. Picture a function
that resolves a search term to a list of IDs, then issues **one `requests.get` per ID
sequentially** in a loop to fetch each ID's details — and nothing anywhere is cached, so
every run re-hits the upstream service for terms it already resolved seconds ago.

The fix has two parts:
- A shared cached-GET helper used by both the term→IDs call and every per-ID details
  call, so identical requests are served from disk.
- A bounded thread pool over the per-ID inner calls (and over batches of terms when
  several are looked up at once), so the fan-out runs ~10–20 in flight instead of one at
  a time.

Keep the tool's existing return shape and error encoding — wrap the network helpers,
don't change the public contract. See `references/patterns.md` →
"Python: threaded + cached `requests`" for the shape to apply.

## Anti-patterns to avoid

- **Sequential loop of network calls** with no concurrency — the thing this skill
  replaces.
- **Unbounded concurrency** — spawning a task per item with no cap; trips rate limits and
  exhausts fds.
- **In-memory-only caching** (a dict that dies with the process) — doesn't survive across
  runs or follow-up sessions, which is the whole point here.
- **Caching failures** — persisting error responses, which replays them forever.
- **TTL/expiry scaffolding for stable data** — for reference data that doesn't change on
  a session timescale, cache without expiry and expose a manual refresh instead.
- **Committing the cache** — derived data doesn't belong in version control.

## Reference

`references/patterns.md` — ready-to-adapt concurrent + disk-cache implementations per
language (Python threads, Python asyncio, JS/TS, Go, Java), plus the atomic-write and
content-key-hashing snippets. Read it when you're about to write the actual code so you
match the project's language and HTTP client.
