# SOLUTION for Issue #446

## 1. 问题分析

- Root cause: `__getattr__` used `super(UserAgent, self).__getattribute__` to return "safe" attributes. This is incorrect and could cause attribute lookups (e.g., `shape`) to be handled improperly, eventually calling `getBrowser("shape")` and returning a fallback user-agent when the filters didn't match.
- Symptom: Accessing common attribute names sometimes returned the fallback user agent or caused a warning. Also users observed reduced randomness because fallback was used or filtered list small.

## 2. 解决方案

- Replaced the incorrect `super(UserAgent, self).__getattribute__` calls with `object.__getattribute__(self, attr)`. This ensures safe attribute lookups do not get treated as browser requests and avoids accidental fallbacks.
- Switched to `random.choices(..., weights=...)` to select user agents according to the `percent` field (weighted sampling). This makes selection more realistic.
- Fixed `find_browser_json_path` to look in package resources and fall back to local `data/` folder for better test/install behavior.

Files changed:
- `src/fake_useragent/fake.py` — main fixes (attribute lookup + weighted sampling).
- `src/fake_useragent/utils.py` — resilient resource lookup.
- Added tests in `tests/` targeting the bug and general behavior.

## 3. 测试策略

- `test_safe_attr_does_not_trigger_fallback` ensures that attribute names like `shape` are not treated as browsers and do not return fallback values.
- `test_random_generates_variety` verifies multiple different user agents are returned across many calls.
- `test_getbrowser_and_filtering` ensures filtering yields data and that `getRandom` does not return fallback when data exists.
- Property tests ensure `.chrome`, `.firefox`, `.random` return strings.

## 4. 使用说明

- Install & test:

    pip install -e .
    pytest -v

- Run demo:

    python fixed_version.py


