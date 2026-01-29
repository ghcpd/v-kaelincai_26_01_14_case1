import os
import sys
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from fake_useragent.utils import load
from fake_useragent import UserAgent


def test_load_deduplicates_by_useragent():
    data = load()
    uas = [d["useragent"] for d in data]
    assert len(uas) == len(set(uas)), "load() must deduplicate identical useragent strings"


def test_issue_446_filtered_has_no_duplicate_useragents():
    ua = UserAgent(
        browsers=[
            "Chrome",
            "Firefox",
            "Edge",
            "Opera",
            "Safari",
            "Android",
            "Samsung Internet",
            "Opera Mobile",
            "Mobile Safari",
            "Firefox Mobile",
            "Chrome Mobile",
            "Chrome Mobile iOS",
            "Mobile Safari UI/WKWebView",
            "Edge Mobile",
        ],
        os=["Windows", "Chrome OS", "Mac OS X", "Android", "iOS"],
        min_version=131,
    )

    filtered = ua._filter_useragents()
    uas = [d["useragent"] for d in filtered]
    assert len(uas) == len(set(uas)), "_filter_useragents() should not return duplicate useragent strings"

    # calling .random multiple times should not always return the fallback
    results = [ua.random for _ in range(10)]
    assert any(r != ua.fallback for r in results)
    # expect at least 2 unique values from 10 draws given the fixture dataset
    assert len(set(results)) >= 2


def test_safe_attr_shape_does_not_invoke_browser_lookup():
    ua = UserAgent()
    with pytest.raises(AttributeError):
        _ = ua.shape
