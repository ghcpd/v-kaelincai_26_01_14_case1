SOLUTION for Issue #446

1) Problem analysis

- Root cause: the original implementation sometimes cached a single user-agent
  value when the `UserAgent` instance was created with restrictive filters
  (for example `browsers=[...]` and `min_version=...`). That meant repeated
  accesses to `ua.random` returned the same string.

- Where it went wrong: selection was performed (or memoized) at construction
  time instead of at access time.

- Why duplicates appeared: a single candidate was chosen and reused for every
  call instead of sampling from the (possibly multi-element) candidate list.

2) Fix implemented

- Files changed/added:
  - `src/fake_useragent/fake.py` — ensure `UserAgent.random` selects a value
    on every access (no caching of the selected value).
  - `src/fake_useragent/utils.py` — robust candidate-building with
    well-documented fallback behaviour and explicit errors for unknown
    browser names.
  - Tests added under `tests/` to validate randomness, filtering and edge
    cases.

- Key implementation notes:
  - Candidate list is precomputed for performance, but random.choice is
    invoked on every `random` property access.
  - If `min_version` filtering would yield an empty set, the code falls back
    to a less restrictive candidate set (preserves usability).
  - If the caller explicitly requests browser names that are not present in
    the dataset, raise an error to fail-fast and avoid silent misconfiguration.

3) Test strategy

- Unit tests cover:
  - The original failure mode (verify that `random` doesn't return a cached
    value by asserting `random.choice` is called each time).
  - Deterministic checks for diversity using a fixed RNG seed.
  - Edge cases: unknown browsers, overly-strict `min_version` (fallback),
    and basic API compatibility.

- Tests are written to be non-flaky: they patch `random.choice` where
  appropriate and use deterministic seeds where randomness must be observed.

4) How to verify locally

- Install in editable mode and run the demo:
  - python -m pip install -e .
  - python fixed_version.py

- Run the full test-suite:
  - pytest -v

5) Backwards compatibility

- Public API remains the same: `UserAgent(...).random` still returns a
  string. Behavioural change is limited to fixing the bug and making
  failure modes explicit (unknown browser names now raise).

6) Additional notes

- The fix is intentionally small and well-covered by tests so it can be
  backported or cherry-picked into upstream releases.
