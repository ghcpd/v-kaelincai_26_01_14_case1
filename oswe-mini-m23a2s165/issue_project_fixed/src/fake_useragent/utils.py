"""General utils for the fake_useragent package (fixed).

Fixes:
- `load()` now deduplicates entries by `useragent` to avoid multiple identical
  user-agent strings in-memory (root cause of poor apparent randomness).
- `find_browser_json_path()` accepts either `browsers.jsonl` or `browsers.json`.
"""

import json
import sys
from typing import TypedDict, Union

# importlib.resources API compatibility
if sys.version_info >= (3, 10):
    import importlib.resources as ilr
else:
    import importlib_resources as ilr  # noqa: F401

from pathlib import Path

from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger


class BrowserUserAgentData(TypedDict):
    useragent: str
    percent: float
    type: str
    device_brand: Union[str, None]
    browser: Union[str, None]
    browser_version: str
    browser_version_major_minor: float
    os: Union[str, None]
    os_version: Union[str, None]
    platform: str


def find_browser_json_path() -> Path:
    """Find the path to the browsers data file (supports .jsonl or .json).

    This prefers a data file colocated with this module (useful for local
    test fixtures). If not found, fall back to importlib.resources.

    Raises FakeUserAgentError if neither file is present.
    """
    candidates = ("browsers.jsonl", "browsers.json")

    # 1) Prefer a data file next to this module (ensures tests use the
    #    fixture inside this package directory instead of another package on
    #    sys.path).
    package_dir = Path(__file__).resolve().parent
    for name in candidates:
        local = package_dir.joinpath("data", name)
        if local.exists():
            return local

    # 2) Fall back to importlib.resources lookup
    last_exc = None
    for name in candidates:
        try:
            file_path = ilr.files("fake_useragent.data").joinpath(name)
            if file_path.exists():
                return Path(str(file_path))
        except Exception as exc:
            last_exc = exc
            logger.debug("looking for %s: %s", name, exc)

    logger.warning(
        "Unable to find local data file using importlib-resources.",
    )
    raise FakeUserAgentError("Could not locate browsers.jsonl or browsers.json")


def load() -> list[BrowserUserAgentData]:
    """Load the included browsers data into memory and deduplicate by `useragent`.

    Returns a list of unique BrowserUserAgentData entries (first occurrence
    preserved).
    """
    data = []
    try:
        json_path = find_browser_json_path()
        text = json_path.read_text()

        # Accept either a JSON-lines file or a JSON array file.
        if json_path.suffix == ".jsonl":
            for line in text.splitlines():
                if not line.strip():
                    continue
                data.append(json.loads(line))
        else:
            parsed = json.loads(text)
            if not isinstance(parsed, list):
                raise FakeUserAgentError("browsers.json must contain a JSON array")
            data.extend(parsed)
    except Exception as exc:
        raise FakeUserAgentError("Failed to load or parse browsers.json") from exc

    if not data:
        raise FakeUserAgentError("Data list is empty", data)

    if not isinstance(data, list):
        raise FakeUserAgentError("Data is not a list", data)

    # Deduplicate by exact `useragent` string. Preserve the first occurrence.
    seen = set()
    deduped = []
    for entry in data:
        ua = entry.get("useragent")
        if ua in seen:
            # duplicate in source dataset; skip to avoid poor apparent randomness
            continue
        seen.add(ua)
        deduped.append(entry)

    return deduped
