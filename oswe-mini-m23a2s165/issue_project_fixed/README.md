# fake-useragent (fixed for Issue #446)

This is a small, fixed copy of the `fake-useragent` package used to demonstrate
and test a fix for Issue #446 (poor randomness / repeated user-agent strings
when restrictive filters are used).

Quick start

- Install editable: pip install -e .
- Run tests: pytest -q
- Demo: python fixed_version.py

What's changed

- Deduplicate identical `useragent` entries when loading/filtering data to
  avoid repeated identical strings showing up in `ua.random`.
- Make attribute-safe lookup more robust so safe attributes (eg. `shape`)
  won't be treated as browser names.
