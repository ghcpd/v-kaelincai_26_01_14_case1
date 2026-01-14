"""Basic functionality tests for fake_useragent."""

import pytest
from fake_useragent import UserAgent


class TestBasicFunctionality:
    """Test basic functionality of the UserAgent class."""

    def test_initialization(self):
        """Test UserAgent initialization with default parameters."""
        ua = UserAgent()
        assert ua.browsers is not None
        assert ua.os is not None
        assert ua.min_version == 0.0

    def test_random_property(self):
        """Test the random property returns a string."""
        ua = UserAgent()
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 10  # Basic sanity check

    def test_chrome_property(self):
        """Test the chrome property."""
        ua = UserAgent()
        agent = ua.chrome
        assert isinstance(agent, str)
        assert "Chrome" in agent

    def test_firefox_property(self):
        """Test the firefox property."""
        ua = UserAgent()
        agent = ua.firefox
        assert isinstance(agent, str)
        assert agent != ua.fallback  # Should not be fallback

    def test_edge_property(self):
        """Test the edge property."""
        ua = UserAgent()
        agent = ua.edge
        assert isinstance(agent, str)
        assert "Edge" in agent or "Edg" in agent

    def test_safari_property(self):
        """Test the safari property."""
        ua = UserAgent()
        agent = ua.safari
        assert isinstance(agent, str)
        assert "Safari" in agent

    def test_get_browser_method(self):
        """Test getBrowser method."""
        ua = UserAgent()
        data = ua.getBrowser("random")
        assert isinstance(data, dict)
        assert "useragent" in data
        assert "percent" in data

    def test_filter_useragents(self):
        """Test _filter_useragents method."""
        ua = UserAgent(browsers=["Chrome"], os=["Windows"])
        filtered = ua._filter_useragents()
        assert isinstance(filtered, list)
        assert len(filtered) > 0
        for item in filtered:
            assert item["browser"] == "Chrome"
            assert item["os"] == "Windows"

    def test_min_version_filter(self):
        """Test min_version filtering."""
        ua_low = UserAgent(min_version=0.0)
        ua_high = UserAgent(min_version=130.0)

        filtered_low = ua_low._filter_useragents()
        filtered_high = ua_high._filter_useragents()

        assert len(filtered_high) <= len(filtered_low)

        for item in filtered_high:
            assert item["browser_version_major_minor"] >= 130.0

    def test_safe_attrs(self):
        """Test safe_attrs functionality."""
        ua = UserAgent(safe_attrs=["nonexistent_attr"])

        # Should raise AttributeError for safe_attr that doesn't exist
        with pytest.raises(AttributeError):
            _ = ua.nonexistent_attr

        # Should work for safe attrs that exist
        ua.test_attr = "value"
        assert ua.test_attr == "value"