# fake-useragent (fixed for Issue #446)

This repository contains a fixed variant of the `fake-useragent` library addressing Issue #446.

Quick start

- Install in editable mode:

    pip install -e .

- Run tests:

    pytest -v

- Demonstrate the fix:

    python fixed_version.py

Purpose

- Fix incorrect attribute handling that erroneously treated certain attribute names as "browsers" (resulting in fallbacks and reduced randomness).
- Improve selection to use weighted sampling by the `percent` field.

Project layout

- `src/fake_useragent/` - fixed package
- `tests/` - pytest suite
- `fixed_version.py` - demo script
- `SOLUTION.md` - explanation and tests
