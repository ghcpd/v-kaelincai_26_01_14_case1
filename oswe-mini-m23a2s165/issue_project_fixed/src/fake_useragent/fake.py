"""Fixed Fake User Agent retriever (Issue #446).

Changes:
- Make attribute-safe lookup more robust (use object.__getattribute__)
- Ensure filtered user-agent lists do not contain duplicate `useragent` strings
  (dedupe during filtering) so `ua.random` returns varied strings even when
  the source data contains repeated entries for the same `useragent`.
"""

import random
from collections.abc import Iterable
from typing import Any, Optional, Union

from fake_useragent.log import logger
from fake_useragent.utils import BrowserUserAgentData, load


def _ensure_iterable(
    *, default: Iterable[str], **kwarg: Optional[Iterable[str]]
) -> list[str]:
    if len(kwarg) != 1:
        raise ValueError(
            f"ensure_iterable expects exactly one keyword argument but got {len(kwarg)}."
        )

    param_name, value = next(iter(kwarg.items()))

    if value is None:
        return list(default)
    if isinstance(value, str):
        return [value]

    try:
        return list(value)
    except TypeError as te:
        raise TypeError(
            f"'{param_name}' must be an iterable of str, a single str, or None but got "
            f"{type(value).__name__}."
        ) from te


def _ensure_float(value: Any) -> float:
    try:
        return float(value)
    except ValueError as ve:
        msg = f"Value must be convertible to float but got {value}."
        raise ValueError(msg) from ve


def _is_magic_name(attribute_name: str) -> bool:
    magic_min_length = 2 * len("__") + 1
    return (
        len(attribute_name) >= magic_min_length
        and attribute_name.isascii()
        and attribute_name.startswith("__")
        and attribute_name.endswith("__")
    )


class FakeUserAgent:
    """Fake User Agent retriever."""

    def __init__(
        self,
        browsers: Optional[Iterable[str]] = None,
        os: Optional[Iterable[str]] = None,
        min_version: float = 0.0,
        min_percentage: float = 0.0,
        platforms: Optional[Iterable[str]] = None,
        fallback: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        ),
        safe_attrs: Optional[Iterable[str]] = None,
    ):
        self.browsers = _ensure_iterable(
            browsers=browsers,
            default=[
                "Google",
                "Chrome",
                "Firefox",
                "Edge",
                "Opera",
                "Safari",
                "Android",
                "Yandex Browser",
                "Samsung Internet",
                "Opera Mobile",
                "Mobile Safari",
                "Firefox Mobile",
                "Firefox iOS",
                "Chrome Mobile",
                "Chrome Mobile iOS",
                "Mobile Safari UI/WKWebView",
                "Edge Mobile",
                "DuckDuckGo Mobile",
                "MiuiBrowser",
                "Whale",
                "Twitter",
                "Facebook",
                "Amazon Silk",
            ],
        )

        self.os = _ensure_iterable(
            os=os,
            default=[
                "Windows",
                "Linux",
                "Ubuntu",
                "Chrome OS",
                "Mac OS X",
                "Android",
                "iOS",
            ],
        )
        self.min_percentage = _ensure_float(min_percentage)
        self.min_version = _ensure_float(min_version)

        self.platforms = _ensure_iterable(
            platforms=platforms, default=["desktop", "mobile", "tablet"]
        )

        if not isinstance(fallback, str):
            msg = f"fallback must be a str but got {type(fallback).__name__}."
            raise TypeError(msg)
        self.fallback = fallback

        if safe_attrs is None:
            safe_attrs = ["shape"]
        safe_attrs = _ensure_iterable(safe_attrs=safe_attrs, default=set())
        str_safe_attrs = [isinstance(attr, str) for attr in safe_attrs]
        if not all(str_safe_attrs):
            bad_indices = [idx for idx, is_str in enumerate(str_safe_attrs) if not is_str]
            msg = f"safe_attrs must be an iterable of str but indices {bad_indices} are not."
            raise TypeError(msg)
        self.safe_attrs = set(safe_attrs)

        # Load local data file into memory
        self.data_browsers = load()

    def getBrowser(self, browsers: Union[str, list[str]]) -> BrowserUserAgentData:
        try:
            if browsers == "random":
                filtered_browsers = self._filter_useragents()
            else:
                filtered_browsers = self._filter_useragents(browsers_to_filter=browsers)

            # Ensure we don't pick from duplicate `useragent` strings (dataset can
            # contain repeated lines with the same `useragent`), that causes poor
            # apparent randomness for `ua.random` — dedupe by `useragent` here.
            unique_by_ua = {}
            for item in filtered_browsers:
                unique_by_ua.setdefault(item["useragent"], item)
            deduped = list(unique_by_ua.values())

            return random.choice(deduped)  # noqa: S311
        except (KeyError, IndexError):
            logger.warning(
                f"Error occurred during getting browser(s): {browsers}, "
                "but was suppressed with fallback.",
            )
            return {
                "useragent": self.fallback,
                "percent": 100.0,
                "type": "desktop",
                "device_brand": None,
                "browser": "Edge",
                "browser_version": "122.0.0.0",
                "browser_version_major_minor": 122.0,
                "os": "win32",
                "os_version": "10",
                "platform": "Win32",
            }

    def _filter_useragents(
        self, browsers_to_filter: Optional[Union[str, list[str]]] = None
    ) -> list[BrowserUserAgentData]:
        filtered_useragents = list(
            filter(
                lambda x: x["browser"] in self.browsers
                and x["os"] in self.os
                and x["type"] in self.platforms
                and x["browser_version_major_minor"] >= self.min_version
                and x["percent"] >= self.min_percentage,
                self.data_browsers,
            )
        )

        if browsers_to_filter:
            if isinstance(browsers_to_filter, str):
                browsers_to_filter = [browsers_to_filter]

            filtered_useragents = list(
                filter(
                    lambda x: x["browser"] in browsers_to_filter, filtered_useragents
                )
            )

        # Deduplicate by `useragent` to avoid repeated identical strings coming
        # from the source dataset (this was the root cause observed in #446).
        seen = set()
        deduped = []
        for entry in filtered_useragents:
            ua = entry.get("useragent")
            if ua in seen:
                continue
            seen.add(ua)
            deduped.append(entry)

        return deduped

    def __getitem__(self, attr: str) -> Union[str, Any]:
        return self.__getattr__(attr)

    def __getattr__(self, attr: Union[str, list[str]]) -> Union[str, Any]:
        # Use object.__getattribute__ for clarity and to avoid subtle name-resolution
        # issues when using `super(...)` with alias names.
        if isinstance(attr, str):
            if _is_magic_name(attr) or attr in self.safe_attrs:
                return object.__getattribute__(self, attr)
        elif isinstance(attr, list):
            for a in attr:
                if a in self.safe_attrs:
                    return object.__getattribute__(self, a)

        return self.getBrowser(attr)["useragent"]

    @property
    def chrome(self) -> str:
        return self.__getattr__(["Chrome", "Chrome Mobile", "Chrome Mobile iOS"])

    @property
    def googlechrome(self) -> str:
        return self.chrome

    @property
    def ff(self) -> str:
        return self.firefox

    @property
    def firefox(self) -> str:
        return self.__getattr__(["Firefox", "Firefox Mobile", "Firefox iOS"])

    @property
    def safari(self) -> str:
        return self.__getattr__(["Safari", "Mobile Safari"])

    @property
    def opera(self) -> str:
        return self.__getattr__(["Opera", "Opera Mobile"])

    @property
    def google(self) -> str:
        return self.__getattr__(["Google"])

    @property
    def edge(self) -> str:
        return self.__getattr__(["Edge", "Edge Mobile"])

    @property
    def random(self) -> str:
        return self.__getattr__("random")

    @property
    def getChrome(self) -> BrowserUserAgentData:
        return self.getBrowser(["Chrome", "Chrome Mobile", "Chrome Mobile iOS"])

    @property
    def getFirefox(self) -> BrowserUserAgentData:
        return self.getBrowser("Firefox")

    @property
    def getSafari(self) -> BrowserUserAgentData:
        return self.getBrowser(["Safari", "Mobile Safari"])

    @property
    def getOpera(self) -> BrowserUserAgentData:
        return self.getBrowser(["Opera", "Opera Mobile"])

    @property
    def getGoogle(self) -> BrowserUserAgentData:
        return self.getBrowser(["Google"])

    @property
    def getEdge(self) -> BrowserUserAgentData:
        return self.getBrowser(["Edge", "Edge Mobile"])

    @property
    def getRandom(self) -> BrowserUserAgentData:
        return self.getBrowser("random")


# common alias
UserAgent = FakeUserAgent
