import pytest

from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError


def test_min_version_filters_but_falls_back_if_too_high():
    # min_version too high would filter out all entries; implementation
    # should fall back to a permissive result rather than failing.
    ua = UserAgent(browsers=["Chrome", "Firefox"], min_version=9999)
    # still able to produce a UA (fallback behavior)
    assert isinstance(ua.random, str) and ua.random


def test_unknown_browser_raises_when_strict():
    # The library should raise if caller asks for a browser that doesn't
    # exist in the dataset (to fail fast). We simulate that by passing
    # a browser name unlikely to exist.
    with pytest.raises(FakeUserAgentError):
        UserAgent(browsers=["__definitely_not_present__"])


def test_backwards_compatibility_property_access():
    ua = UserAgent(browsers=["Chrome"])
    first = ua.random
    second = ua.random
    # Can be equal by chance, but ensure random.choice is being used (i.e.
    # property access works and returns strings).
    assert isinstance(first, str) and isinstance(second, str)
