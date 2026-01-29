# fake-useragent (fixed for Issue #446)

This repository contains a small, self-contained fix for Issue #446 from the
`fake-useragent` project. The problem: when creating a `UserAgent` with a
constrained set of filters the library sometimes returned identical user-agent
strings frequently — the bundled dataset contained duplicate lines which made
random selection look non-random.

Quickstart

1. Install in editable mode:

   pip install -e .

2. Run tests:

   pytest -v

3. Run the quick demonstration:

   python fixed_version.py

The fix is small and backwards compatible: duplicates in the bundled dataset are
removed during load and a small attribute-access bug was corrected.
