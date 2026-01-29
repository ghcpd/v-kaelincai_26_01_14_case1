SOLUTION — Issue #446

1. Problem analysis

- Root cause: the bundled `browsers.jsonl` dataset contains repeated lines with
  identical `useragent` strings. The library selected a random row from the
  filtered dataset but many rows were duplicates, so repeated selections often
  produced the same final `user-agent` string.
- Secondary issue: attribute access used `super(UserAgent, self).__getattribute__`
  which is fragile; in some cases attributes listed in `safe_attrs` (eg. "shape")
  were still being treated like browser lookups and could trigger unexpected
  behavior.

2. Changes made

- `src/fake_useragent/utils.py` — `load()` now deduplicates entries by the
  exact `useragent` string while preserving file order. This removes the
  excessive repetition that made subsequent random picks look non-random.
- `src/fake_useragent/fake.py` — fixed `__getattr__` to call
  `super().__getattribute__` (correct and robust) instead of the previous
  `super(UserAgent, self).__getattribute__` call.

3. Testing strategy

- `tests/test_issue_446.py` contains three tests:
  - `test_load_deduplicates` asserts the loader removes duplicate user agents.
  - `test_random_returns_unique_sample_with_fixed_seed` seeds the RNG and
    verifies a deterministic, non-repeating sample when enough unique entries
    are available.
  - `test_safe_attrs_prevent_browser_lookup` ensures that `safe_attrs`
    (the default includes `shape`) are not interpreted as browsers, which
    previously caused an unintended lookup.

4. How to verify

- Install: `pip install -e .`
- Run tests: `pytest -v` (all tests included here are expected to pass)
- Demo: `python fixed_version.py` — the script shows the `random` property
  producing diverse user-agents with the filters used in the original issue.

Notes

- The fix is intentionally conservative: it de-duplicates the bundled data on
  load (so there is no change to the public API) and corrects a small attribute
  lookup bug. This preserves backwards compatibility while addressing the root
  cause of the reported behaviour.