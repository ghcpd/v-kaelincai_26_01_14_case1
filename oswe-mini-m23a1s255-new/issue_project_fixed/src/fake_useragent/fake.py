"""Core fake_useragent implementation (fixed).

Main fixes:
- Do NOT cache a single user-agent when filters are provided; return a
  new random choice on each access.
- Ensure filtering by min_version does not accidentally return a single
  candidate due to improper filtering logic.
- Provide a clear, testable candidate-building pipeline.
"""
from __future__ import annotations

from typing import List, Optional
import random

from .errors import FakeUserAgentError
from .utils import build_candidates, load_data


class UserAgent:
    """Lightweight UserAgent generator.

    Usage is intentionally compatible with common fake-useragent patterns:
    - `UserAgent().random` returns a random user-agent string on each access
      (no caching of a single value).
    - Filters can be provided at construction time.
    """

    def __init__(
        self,
        browsers: Optional[List[str]] = None,
        os: Optional[List[str]] = None,
        min_version: Optional[int] = None,
    ) -> None:
        self._data = load_data()
        self._browsers = list(browsers) if browsers is not None else None
        self._os = list(os) if os is not None else None
        self._min_version = min_version

        # Validate explicit browser names early and fail-fast if none match
        # the bundled dataset. This duplicates the defensive check in
        # utils.build_candidates but guarantees the behaviour cannot be
        # bypassed by other code paths or stateful changes.
        if self._browsers is not None:
            known = set(self._data.keys())
            if not (set(self._browsers) & known):
                raise FakeUserAgentError(f"no matching browsers found for: {sorted(self._browsers)}")

        # Build candidate list once for performance, but selection is done
        # on every access to `random` to avoid the original bug (caching a
        # single UA value).
        self._candidates = build_candidates(
            self._data, browsers=self._browsers, os=self._os, min_version=self._min_version
        )

        if not self._candidates:
            raise FakeUserAgentError("no user-agent candidates available")

    @property
    def random(self) -> str:
        """Return a randomly selected user-agent string each time.

        Important: do not cache/remember the returned value — the caller
        expects a new (random) value on every access.
        """
        # Always pick at call-time (fix for Issue #446: previous versions
        # sometimes returned the same UA repeatedly when filters were set).
        return random.choice(self._candidates)

    # convenience API used by some consumers
    def __call__(self) -> str:  # pragma: no cover - trivial
        return self.random
