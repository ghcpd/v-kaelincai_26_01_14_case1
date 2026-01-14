"""Utility functions for fake_useragent-fixed.

Focus: safe data loading and candidate building with clear, testable behavior.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .errors import FakeUserAgentError


def load_data() -> Dict[str, List[Dict[str, Any]]]:
    """Load bundled browsers.json from package data directory.

    This function uses a relative path so it works both installed and in-tree.
    """
    data_path = Path(__file__).resolve().parent / "data" / "browsers.json"
    try:
        with data_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError as exc:
        raise FakeUserAgentError(f"browsers.json not found at {data_path}") from exc


def build_candidates(
    data: Dict[str, List[Dict[str, Any]]],
    browsers: Optional[List[str]] = None,
    os: Optional[List[str]] = None,
    min_version: Optional[int] = None,
) -> List[str]:
    """Return a list of user-agent strings that match the provided filters.

    Behavior and guarantees:
    - If `browsers` is None, consider all browsers in the dataset.
    - `os` is currently informational (kept for API compatibility) — dataset
      in this kata doesn't include separate OS keys; future-proofing only.
    - `min_version` filters entries with entry['version'] >= min_version.
    - If filters would produce an empty candidate set, fall back to the
      least-restrictive candidate set (i.e. ignore the restrictive filter)
      to preserve usability (backwards-compatible behavior).
    """
    if not data:
        return []

    # Normalize browser filter
    browsers_filter = None if not browsers else set(browsers)

    # If caller passed explicit browser names that do not exist in the
    # dataset, fail fast — this indicates a user error (keeps behaviour
    # explicit and avoids silently ignoring caller intent).
    if browsers_filter is not None:
        known = set(data.keys())
        requested_known = browsers_filter & known
        if not requested_known:
            raise FakeUserAgentError(f"no matching browsers found for: {sorted(browsers_filter)}")

    # Collect matching entries
    matched: List[Dict[str, Any]] = []
    for browser_name, entries in data.items():
        if browsers_filter is not None and browser_name not in browsers_filter:
            continue
        for entry in entries:
            # version is optional in dataset but most entries include it
            version = entry.get("version")
            if min_version is not None and version is not None:
                if version < min_version:
                    continue
            matched.append(entry)

    # If os filtering were supported in the dataset we'd apply it here.

    if matched:
        return [e["ua"] for e in matched if "ua" in e]

    # Fallback behavior: be permissive rather than returning nothing.
    # Try: ignore min_version first (most common restrictive filter).
    if min_version is not None:
        for browser_name, entries in data.items():
            if browsers_filter is not None and browser_name not in browsers_filter:
                continue
            for entry in entries:
                if "ua" in entry:
                    matched.append(entry)
        if matched:
            return [e["ua"] for e in matched]

    # Last resort: return every UA in dataset
    all_entries = [e for entries in data.values() for e in entries if "ua" in e]
    return [e["ua"] for e in all_entries]
