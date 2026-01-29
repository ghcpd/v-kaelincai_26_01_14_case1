import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from fake_useragent import UserAgent


def test_basic_properties():
    ua = UserAgent()
    assert isinstance(ua.chrome, str) and any(k in ua.chrome for k in ("Chrome", "CriOS", "Chromium"))
    assert isinstance(ua.firefox, str) and ("Firefox" in ua.firefox or "FxiOS" in ua.firefox)
    assert isinstance(ua.random, str)
