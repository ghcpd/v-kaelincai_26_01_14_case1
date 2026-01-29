"""Demonstrate the fix for Issue #446.

This script attempts to create a UserAgent with the same parameters used in
the bug report and prints multiple values to show that they are not all the
same.
"""
from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError


def main() -> None:
    browsers = [
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
    ]

    try:
        ua = UserAgent(browsers=browsers, os=["Windows", "Android", "iOS"], min_version=131)
    except FakeUserAgentError as exc:
        print("Requested browser list contained names not present in bundled dataset:", exc)
        print("Falling back to a permissive UserAgent to demonstrate randomness.")
        ua = UserAgent()  # permissive fallback for demo

    print("Generating 10 user-agents (should not all be identical):")
    for _ in range(10):
        print(ua.random)


if __name__ == "__main__":
    main()
