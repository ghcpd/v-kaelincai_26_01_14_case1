"""Demonstrate the fix for Issue #446."""
from fake_useragent import UserAgent


def main():
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

    print("Generate 10 random user agents:")
    for i in range(10):
        print(i + 1, ua.random)


if __name__ == "__main__":
    main()
