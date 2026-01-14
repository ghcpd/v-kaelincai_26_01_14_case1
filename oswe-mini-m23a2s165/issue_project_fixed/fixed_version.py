"""Demo script to show the fix for Issue #446."""
import os
import sys
# ensure local `src` is preferred when running the demo
ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from fake_useragent import UserAgent

print("Demo: Issue #446 — generate 10 random user-agents with restrictive filters")
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

for i in range(10):
    print(f"{i+1}. {ua.random}")
