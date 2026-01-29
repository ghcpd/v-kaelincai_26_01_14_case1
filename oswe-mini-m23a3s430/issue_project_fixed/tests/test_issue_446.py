import random
import pytest

from fake_useragent import UserAgent
from fake_useragent.utils import load


def test_load_deduplicates() -> None:
    """Loading the bundled data should remove duplicate `useragent` strings."""
    data = load()
    uas = [row["useragent"] for row in data]
    assert len(uas) == len(set(uas))


def test_random_repetition_reduced_by_deduplication() -> None:
    """Demonstrate the root cause: when the dataset contains repeated rows the
    same `useragent` string appears multiple times. After deduplication the
    number of unique picks increases.

    This test explicitly constructs a small dataset with heavy duplication and
    compares selection behaviour between the raw (duplicated) dataset and the
    deduplicated one. We fix the RNG to keep the sample deterministic.
    """
    # Construct a small dataset where one user-agent appears repeatedly.
    raw = [
        {"useragent": "UA-1", "percent": 10.0, "type": "desktop", "device_brand": None, "browser": "Chrome", "browser_version": "137.0.0.0", "browser_version_major_minor": 137.0, "os": "Windows", "os_version": "10", "platform": "Win32"},
        {"useragent": "UA-1", "percent": 5.0, "type": "desktop", "device_brand": None, "browser": "Chrome", "browser_version": "137.0.0.0", "browser_version_major_minor": 137.0, "os": "Windows", "os_version": "10", "platform": "Win32"},
        {"useragent": "UA-1", "percent": 2.0, "type": "desktop", "device_brand": None, "browser": "Chrome", "browser_version": "137.0.0.0", "browser_version_major_minor": 137.0, "os": "Windows", "os_version": "10", "platform": "Win32"},
        {"useragent": "UA-2", "percent": 8.0, "type": "desktop", "device_brand": None, "browser": "Chrome", "browser_version": "137.0.0.0", "browser_version_major_minor": 137.0, "os": "Windows", "os_version": "10", "platform": "Win32"},
        {"useragent": "UA-3", "percent": 7.0, "type": "desktop", "device_brand": None, "browser": "Chrome", "browser_version": "137.0.0.0", "browser_version_major_minor": 137.0, "os": "Windows", "os_version": "10", "platform": "Win32"},
        {"useragent": "UA-4", "percent": 6.0, "type": "desktop", "device_brand": None, "browser": "Chrome", "browser_version": "137.0.0.0", "browser_version_major_minor": 137.0, "os": "Windows", "os_version": "10", "platform": "Win32"},
    ]

    deduped = []
    seen = set()
    for row in raw:
        ua = row["useragent"]
        if ua in seen:
            continue
        seen.add(ua)
        deduped.append(row)

    # Create two UserAgent instances and inject the datasets directly.
    ua_raw = UserAgent(browsers=["Chrome"], os=["Windows"], min_version=131)
    ua_raw.data_browsers = raw

    ua_dedup = UserAgent(browsers=["Chrome"], os=["Windows"], min_version=131)
    ua_dedup.data_browsers = deduped

    random.seed(0)
    picks_raw = [ua_raw.random for _ in range(10)]

    random.seed(0)
    picks_dedup = [ua_dedup.random for _ in range(10)]

    # The deduplicated dataset should produce more unique user-agents for the
    # same fixed RNG seed (i.e. duplicates were the root cause).
    assert len(set(picks_dedup)) > len(set(picks_raw))


def test_safe_attrs_prevent_browser_lookup() -> None:
    """Accessing an attribute listed in `safe_attrs` (the default contains
    "shape") must not be treated as a browser lookup and therefore should
    raise a normal AttributeError instead of triggering the fallback.
    """
    ua = UserAgent(browsers=["Chrome"], os=["Windows"], min_version=131)
    with pytest.raises(AttributeError):
        _ = ua.shape