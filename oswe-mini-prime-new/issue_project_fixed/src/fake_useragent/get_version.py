"""Simple helper file to retrieve the version."""

try:
    from importlib import metadata

    __version__ = metadata.version("fake-useragent")
except Exception:
    __version__ = "0.0.0-fixed"
