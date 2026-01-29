import random
import pytest

from fake_useragent import UserAgent


def make_test_ua():
    return UserAgent(
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


def test_safe_attr_does_not_trigger_fallback():
    ua = make_test_ua()
    # Accessing `shape` should raise AttributeError rather than be treated as a browser
    with pytest.raises(AttributeError):
        _ = ua.shape


def test_random_generates_variety():
    random.seed(0)
    ua = make_test_ua()

    samples = [ua.random for _ in range(20)]
    unique = set(samples)

    # Ensure we actually sample multiple different user agents (not only fallback)
    assert len(unique) > 1
    assert not (len(unique) == 1 and next(iter(unique)) == ua.fallback)


def test_getbrowser_and_filtering():
    ua = make_test_ua()
    filtered = ua._filter_useragents()
    assert isinstance(filtered, list)
    assert len(filtered) > 0

    # getRandom should not return fallback when filtered list exists
    assert ua.getRandom["useragent"] != ua.fallback


def test_browser_properties_return_strings():
    ua = make_test_ua()
    assert isinstance(ua.chrome, str)
    assert isinstance(ua.firefox, str)
    assert isinstance(ua.random, str)
