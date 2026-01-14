"""General utils for the fake_useragent package (fixed)."""

import json
import sys
from typing import TypedDict, Union

# We need files() from Python 3.10 or higher
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
    """Find the path to the browsers.jsonl file.

    Improved resilience: try package resources first, fall back to local data folder
    relative to this module (useful during tests and editable installs).
    """
    # Primary: package resource lookup
    try:
        # Try to locate within package resources
        try:
            file_path = ilr.files("fake_useragent").joinpath("data", "browsers.jsonl")
            return Path(str(file_path))
        except Exception:
            # Older layout (fake_useragent.data)
            file_path = ilr.files("fake_useragent.data").joinpath("browsers.jsonl")
            return Path(str(file_path))
    except Exception as exc:
        logger.warning(
            "Unable to find local data/jsonl file using importlib-resources.",
            exc_info=exc,
        )

    # Fallback: local relative path (this file's directory)
    local_path = Path(__file__).parent.joinpath("data", "browsers.jsonl")
    if local_path.exists():
        return local_path

    raise FakeUserAgentError("Could not locate browsers.jsonl file")


def load() -> list[BrowserUserAgentData]:
    data = []
    try:
        json_path = find_browser_json_path()
        for line in json_path.read_text().splitlines():
            data.append(json.loads(line))
    except Exception as exc:
        raise FakeUserAgentError("Failed to load or parse browsers.jsonl") from exc

    if not data:
        raise FakeUserAgentError("Data list is empty", data)

    if not isinstance(data, list):
        raise FakeUserAgentError("Data is not a list", data)
    return data
