"""Edge case tests for fake_useragent."""

import pytest
from fake_useragent import UserAgent


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_browsers_list(self):
        """Test with empty browsers list."""
        ua = UserAgent(browsers=[])
        # Should use default browsers
        agent = ua.random
        assert isinstance(agent, str)

    def test_empty_os_list(self):
        """Test with empty os list."""
        ua = UserAgent(os=[])
        # Should use default os
        agent = ua.random
        assert isinstance(agent, str)

    def test_very_high_min_version(self):
        """Test with very high min_version that filters out most browsers."""
        ua = UserAgent(min_version=999.0)
        agent = ua.random
        # Should return fallback
        assert agent == ua.fallback

    def test_single_browser_single_os(self):
        """Test with single browser and single os."""
        ua = UserAgent(browsers=["Chrome"], os=["Windows"], min_version=131)
        filtered = ua._filter_useragents()
        assert len(filtered) > 0
        for item in filtered:
            assert item["browser"] == "Chrome"
            assert item["os"] == "Windows"
            assert item["browser_version_major_minor"] >= 131

    def test_nonexistent_browser(self):
        """Test requesting a nonexistent browser."""
        ua = UserAgent()
        data = ua.getBrowser("NonExistentBrowser")
        # Should return fallback data
        assert data["useragent"] == ua.fallback

    def test_min_percentage_filter(self):
        """Test min_percentage filtering."""
        ua = UserAgent(min_percentage=1.0)  # Very high percentage
        filtered = ua._filter_useragents()
        # Should have fewer results
        ua_default = UserAgent()
        filtered_default = ua_default._filter_useragents()
        assert len(filtered) <= len(filtered_default)

    def test_platform_filtering(self):
        """Test platform filtering."""
        ua = UserAgent(platforms=["mobile"])
        filtered = ua._filter_useragents()
        for item in filtered:
            assert item["type"] == "mobile"

    def test_multiple_calls_consistency(self):
        """Test that multiple calls work consistently."""
        ua = UserAgent()
        agents = [ua.random for _ in range(5)]
        # All should be strings
        assert all(isinstance(agent, str) for agent in agents)
        # Should have some variation (not guaranteed, but likely)
        unique = set(agents)
        assert len(unique) >= 1

    def test_fallback_useragent(self):
        """Test fallback user agent."""
        custom_fallback = "Custom Fallback UA"
        ua = UserAgent(fallback=custom_fallback, min_version=999)
        agent = ua.random
        assert agent == custom_fallback

    def test_invalid_fallback_type(self):
        """Test invalid fallback type raises error."""
        with pytest.raises(TypeError):
            UserAgent(fallback=123)

    def test_invalid_safe_attrs_type(self):
        """Test invalid safe_attrs type raises error."""
        with pytest.raises(TypeError):
            UserAgent(safe_attrs=123)

    def test_safe_attrs_with_non_str(self):
        """Test safe_attrs with non-string values raises error."""
        with pytest.raises(TypeError):
            UserAgent(safe_attrs=[123])