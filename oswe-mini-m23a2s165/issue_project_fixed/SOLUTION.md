# Solution for Issue #446

## Problem analysis

- Root cause: the in-memory dataset (and the filtered results) could contain
  multiple identical `useragent` strings (the source `browsers` data sometimes
  contains repeated entries for the same `useragent`). Picking randomly from
  that list increased the chance of returning identical strings repeatedly.
- Symptom: calling `ua.random` with restrictive filters (e.g. `min_version=131`)
  produced many repeated user-agent strings and sometimes triggered fallback
  when attribute lookups were misrouted.

## Fix implemented

- Deduplicate `useragent` entries during `load()` and again during
  `_filter_useragents()` so the in-memory lists only contain unique
  `useragent` strings.
- Make attribute lookup (`__getattr__`) more robust by using
  `object.__getattribute__` for safe attributes.

Files changed

- `fake.py` — dedupe filtered results and harden attribute lookup
- `utils.py` — dedupe during load; accept `browsers.json` and `browsers.jsonl`

## Test strategy

- Unit tests reproduce the original symptom by loading a dataset that would
  previously produce duplicate `useragent` strings.
- Tests verify `load()` and `_filter_useragents()` return unique `useragent`s.
- Tests assert `ua.shape` does not fall back to `getBrowser` and instead
  raises an AttributeError (safe attribute behavior).

## How to verify

1. pip install -e .
2. pytest -q
3. python fixed_version.py — you should see varied user-agent strings
   (duplicates from identical source lines will not appear).
