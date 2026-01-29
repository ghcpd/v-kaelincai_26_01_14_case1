"""Demonstrate the Issue #446 fix."""

from fake_useragent import UserAgent

print("Demonstrating the fix for Issue #446\n")
print("=" * 80)

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

print("Generate 10 random user-agents (fixed dataset used in tests):\n")
for i in range(1, 11):
    print(f"{i}. {ua.random}")

print("\nDone.")