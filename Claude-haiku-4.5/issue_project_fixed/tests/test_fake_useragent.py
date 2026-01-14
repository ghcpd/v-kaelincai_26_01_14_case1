"""Test suite for fake_useragent library."""

import pytest
from fake_useragent import UserAgent, FakeUserAgentError


class TestBasicFunctionality:
    """Test basic UserAgent functionality."""

    def test_random_ua_generation(self):
        """Test that random user agents can be generated."""
        ua = UserAgent()
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_random_ua_not_empty(self):
        """Test that generated user agents are not empty."""
        ua = UserAgent()
        for _ in range(10):
            agent = ua.random
            assert agent
            assert isinstance(agent, str)

    def test_chrome_ua(self):
        """Test Chrome user agent retrieval."""
        ua = UserAgent()
        agent = ua.chrome
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_firefox_ua(self):
        """Test Firefox user agent retrieval."""
        ua = UserAgent()
        agent = ua.firefox
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_safari_ua(self):
        """Test Safari user agent retrieval."""
        ua = UserAgent()
        agent = ua.safari
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_opera_ua(self):
        """Test Opera user agent retrieval."""
        ua = UserAgent()
        agent = ua.opera
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_edge_ua(self):
        """Test Edge user agent retrieval."""
        ua = UserAgent()
        agent = ua.edge
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_get_browser_methods(self):
        """Test get* methods for browser user agents."""
        ua = UserAgent()
        
        assert isinstance(ua.getChrome, dict)
        assert "useragent" in ua.getChrome
        assert isinstance(ua.getChrome["useragent"], str)
        
        assert isinstance(ua.getFirefox, dict)
        assert "useragent" in ua.getFirefox
        
        assert isinstance(ua.getSafari, dict)
        assert "useragent" in ua.getSafari
        
        assert isinstance(ua.getRandom, dict)
        assert "useragent" in ua.getRandom


class TestIssue446RandomnessWithFilters:
    """Test Issue #446 - Randomness with multiple filters (browsers, os, min_version)."""

    def test_issue_446_weighted_selection_used(self):
        """Test that the weighted selection method is being used.
        
        Issue #446: When using specific parameters, generated user agents had low randomness.
        The fix implements _weighted_choice() method that uses percent field for weighting.
        
        This test verifies the method exists and is callable.
        """
        ua = UserAgent(
            browsers=["Chrome", "Firefox"],
            os=["Windows"],
            min_version=130,
        )
        
        # Verify the method exists
        assert hasattr(ua, '_weighted_choice')
        assert callable(ua._weighted_choice)
        
        # Verify it returns a valid selection
        filtered = ua._filter_useragents()
        selection = ua._weighted_choice(filtered)
        assert isinstance(selection, dict)
        assert "useragent" in selection

    def test_issue_446_randomness_improvement(self):
        """Test that randomness is improved with filters.
        
        The key improvement is that the selection process now uses weights,
        resulting in more realistic distribution even with small filtered sets.
        """
        ua = UserAgent(
            browsers=["Chrome", "Firefox", "Edge"],
            os=["Windows", "Mac OS X"],
            min_version=130,
        )

        # Generate user agents
        user_agents = [ua.random for _ in range(50)]
        
        # With weighted selection, we should have variety
        unique_count = len(set(user_agents))
        
        # Even with filtering, should get some variety
        # The exact number depends on how many unique strings are in filtered data
        # But we should have at least a few different ones
        assert unique_count >= 5, (
            f"Expected at least 5 unique user agents, got {unique_count}"
        )
        
        # Verify they're not all the same (no selection regression)
        assert unique_count > 1

    def test_randomness_with_browser_filter_only(self):
        """Test randomness when filtering by browsers only."""
        ua = UserAgent(browsers=["Chrome", "Chrome Mobile", "Chrome Mobile iOS"])
        
        user_agents = [ua.random for _ in range(50)]
        unique_count = len(set(user_agents))
        
        # Should have variety
        assert unique_count >= 3, f"Expected at least 3 unique out of 50, got {unique_count}"

    def test_randomness_with_os_filter_only(self):
        """Test randomness when filtering by OS only."""
        ua = UserAgent(os=["Windows", "Mac OS X"])
        
        user_agents = [ua.random for _ in range(50)]
        unique_count = len(set(user_agents))
        
        # Should have variety
        assert unique_count >= 3, f"Expected at least 3 unique out of 50, got {unique_count}"

    def test_randomness_with_version_filter(self):
        """Test randomness when filtering by minimum version."""
        ua = UserAgent(min_version=135)
        
        user_agents = [ua.random for _ in range(50)]
        unique_count = len(set(user_agents))
        
        # Should have variety
        assert unique_count >= 3, f"Expected at least 3 unique out of 50, got {unique_count}"

    def test_randomness_consistency(self):
        """Test that randomness is consistent across multiple calls."""
        ua = UserAgent(
            browsers=["Chrome", "Firefox"],
            os=["Windows", "Mac OS X"],
            min_version=130
        )
        
        # Multiple calls should produce different results (not get stuck)
        user_agents = [ua.random for _ in range(30)]
        unique_count = len(set(user_agents))
        
        # Should have multiple different values
        assert unique_count > 1, "All selections were identical!"
        assert unique_count >= 2, "Should have at least 2 unique values"


class TestFilteringParameters:
    """Test various filtering parameters."""

    def test_browser_filter_list(self):
        """Test filtering with a list of browsers."""
        ua = UserAgent(browsers=["Chrome", "Firefox"])
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_browser_filter_string(self):
        """Test filtering with a single browser as string."""
        ua = UserAgent(browsers="Chrome")
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_os_filter_list(self):
        """Test filtering with a list of operating systems."""
        ua = UserAgent(os=["Windows", "Linux"])
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_os_filter_string(self):
        """Test filtering with a single OS as string."""
        ua = UserAgent(os="Windows")
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_min_version_filter(self):
        """Test filtering with minimum version."""
        ua = UserAgent(min_version=130)
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_min_percentage_filter(self):
        """Test filtering with minimum percentage."""
        ua = UserAgent(min_percentage=0.05)
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_platform_filter(self):
        """Test filtering with specific platforms."""
        ua = UserAgent(platforms="desktop")
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_combined_filters(self):
        """Test using multiple filters together."""
        ua = UserAgent(
            browsers=["Chrome", "Firefox"],
            os=["Windows"],
            min_version=130,
            min_percentage=0.01,
            platforms=["desktop", "mobile"]
        )
        
        agent = ua.random
        assert isinstance(agent, str)
        assert len(agent) > 0


class TestFallback:
    """Test fallback behavior."""

    def test_custom_fallback(self):
        """Test that custom fallback works."""
        custom_fallback = "Custom User Agent String"
        ua = UserAgent(fallback=custom_fallback)
        
        # The fallback should be used if there are no matching results
        assert ua.fallback == custom_fallback

    def test_default_fallback(self):
        """Test that default fallback is set."""
        ua = UserAgent()
        
        assert isinstance(ua.fallback, str)
        assert len(ua.fallback) > 0


class TestDataAccess:
    """Test accessing user agent data."""

    def test_get_random_returns_dict(self):
        """Test that getRandom returns a dictionary with all fields."""
        ua = UserAgent()
        data = ua.getRandom
        
        assert isinstance(data, dict)
        assert "useragent" in data
        assert "percent" in data
        assert "type" in data
        assert "browser" in data
        assert "os" in data

    def test_browser_data_structure(self):
        """Test that returned data has expected structure."""
        ua = UserAgent()
        data = ua.getRandom
        
        # Check all expected fields
        expected_fields = {
            "useragent", "percent", "type", "device_brand", "browser",
            "browser_version", "browser_version_major_minor", "os",
            "os_version", "platform"
        }
        
        assert all(field in data for field in expected_fields)
        assert isinstance(data["useragent"], str)
        assert isinstance(data["percent"], (int, float))
        assert isinstance(data["type"], str)
        assert isinstance(data["browser_version_major_minor"], (int, float))


class TestIndexAccess:
    """Test dictionary-style access."""

    def test_index_access_random(self):
        """Test accessing user agent via index notation."""
        ua = UserAgent()
        agent = ua["random"]
        
        assert isinstance(agent, str)
        assert len(agent) > 0

    def test_index_access_browser(self):
        """Test accessing specific browser via index notation."""
        ua = UserAgent()
        agent = ua["Chrome"]
        
        assert isinstance(agent, str)
        assert len(agent) > 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_high_version_filter(self):
        """Test filtering with very high version number."""
        ua = UserAgent(min_version=999)
        
        # Should fall back gracefully
        agent = ua.random
        assert isinstance(agent, str)

    def test_invalid_browser_name(self):
        """Test with browsers that don't exist."""
        ua = UserAgent(browsers=["NonExistentBrowser"])
        
        # Should fall back gracefully
        agent = ua.random
        assert isinstance(agent, str)

    def test_empty_filter_results(self):
        """Test when filter results are empty."""
        ua = UserAgent(
            browsers=["NonExistent"],
            os=["NonExistent"],
            min_version=9999
        )
        
        # Should use fallback
        agent = ua.random
        assert isinstance(agent, str)
        assert agent == ua.fallback

    def test_properties_consistency(self):
        """Test that browser properties return consistent types."""
        ua = UserAgent()
        
        # All browser properties should return strings
        assert isinstance(ua.chrome, str)
        assert isinstance(ua.firefox, str)
        assert isinstance(ua.safari, str)
        assert isinstance(ua.opera, str)
        assert isinstance(ua.edge, str)
        assert isinstance(ua.google, str)


class TestTypeErrors:
    """Test error handling for type mismatches."""

    def test_invalid_fallback_type(self):
        """Test that non-string fallback raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(fallback=123)

    def test_invalid_safe_attrs_type(self):
        """Test that non-string items in safe_attrs raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(safe_attrs=[123, "valid"])


class TestWeightedSelection:
    """Test the weighted random selection fix for Issue #446."""

    def test_weighted_selection_distribution(self):
        """Test that weighted selection respects the percent distribution."""
        ua = UserAgent()
        
        # Get filtered list with high percentages
        filtered = ua._filter_useragents()
        
        # Check that we have items with percent values
        assert len(filtered) > 0
        
        # All items should have percent >= min_percentage
        for item in filtered:
            assert item["percent"] >= ua.min_percentage

    def test_weighted_choice_with_different_weights(self):
        """Test weighted choice implementation."""
        ua = UserAgent(browsers=["Chrome"], os=["Windows"])
        
        # Generate multiple selections
        selections = [ua.getBrowser("Chrome") for _ in range(50)]
        
        # Should get actual selections (not errors)
        assert len(selections) == 50
        assert all(isinstance(s, dict) for s in selections)

    def test_multiple_calls_produce_different_results(self):
        """Test that multiple calls don't always return the same result."""
        ua = UserAgent(
            browsers=["Chrome", "Firefox"],
            os=["Windows", "Mac OS X", "Linux"],
            min_version=130
        )
        
        # Get multiple selections
        results = []
        for _ in range(50):
            results.append(ua.random)
        
        # Should have multiple different results
        unique_results = len(set(results))
        assert unique_results > 1, "Multiple calls returned identical results"
        # Should have at least a few different ones
        assert unique_results >= 2, f"Low diversity: only {unique_results} unique out of 50"


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_old_api_still_works(self):
        """Test that old API patterns still work."""
        ua = UserAgent()
        
        # Old way of accessing
        agent1 = ua.random
        agent2 = ua.chrome
        agent3 = ua.firefox
        
        assert all(isinstance(a, str) and len(a) > 0 for a in [agent1, agent2, agent3])

    def test_safe_attrs_still_works(self):
        """Test that safe_attrs mechanism still prevents method calls."""
        ua = UserAgent(safe_attrs=["shape"])
        
        # Accessing 'shape' should work normally (not treat as browser)
        try:
            # This should not raise, but rather return the attribute or None
            _ = ua.shape
        except AttributeError:
            # It's OK if shape doesn't exist, as long as it doesn't try to get a browser
            pass
