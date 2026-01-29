from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError

def attempt_long_list():
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
    print("== Attempt: long browser list + min_version=131 ==")
    try:
        ua = UserAgent(browsers=browsers, min_version=131)
        samples = [ua.random for _ in range(10)]
        print("Created UA, samples:")
        for s in samples:
            print(s)
        print("unique_count=", len(set(samples)))
    except FakeUserAgentError as exc:
        print("Raised FakeUserAgentError:", exc)


def attempt_known_browsers_high_min():
    print("\n== Attempt: known browsers + min_version=131 (should fallback) ==")
    ua = UserAgent(browsers=["Chrome", "Firefox", "Chrome Mobile"], min_version=131)
    samples = [ua.random for _ in range(20)]
    for s in samples:
        print(s)
    print("unique_count=", len(set(samples)))


if __name__ == "__main__":
    attempt_long_list()
    attempt_known_browsers_high_min()
