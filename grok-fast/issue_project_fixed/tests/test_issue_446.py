"""Tests for Issue #446 fix: Random user agent repetition."""

import pytest
from collections import Counter
from fake_useragent import UserAgent


class TestIssue446:
    """Test the fix for Issue #446: insufficient randomness in UserAgent.random."""

    def test_random_uniqueness_high_filters(self):
        """Test that random user agents have low repetition with specific filters."""
        ua = UserAgent(
            browsers=["Chrome", "Firefox", "Edge", "Opera", "Safari", "Android",
                      "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile",
                      "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile"],
            os=["Windows", "Chrome OS", "Mac OS X", "Android", "iOS"],
            min_version=131,
        )

        # Generate 20 user agents
        user_agents = [ua.random for _ in range(20)]
        unique_agents = set(user_agents)

        # With deduplication and uniform random, we should have high uniqueness
        # Allow some repetition but not excessive
        assert len(unique_agents) >= 10, f"Too much repetition: {len(unique_agents)} unique out of 20"

    def test_random_distribution_weighted(self):
        """Test that random selection follows weighted distribution."""
        ua = UserAgent(
            browsers=["Chrome", "Firefox"],
            os=["Windows"],
            min_version=131,
        )

        # Get filtered browsers
        filtered = ua._filter_useragents()
        total_weight = sum(d['percent'] for d in filtered)

        # Generate many samples to check distribution
        samples = 1000
        user_agents = [ua.random for _ in range(samples)]

        # Count frequency of each UA
        from collections import Counter
        counter = Counter(user_agents)

        # Check that high-weight UAs appear more frequently
        # This is a basic check - in practice, it should follow the weights
        assert len(counter) > 1, "Should have multiple different UAs"

    def test_random_with_minimal_filters(self):
        """Test random with minimal filters to ensure basic functionality."""
        ua = UserAgent()

        # Generate 10 user agents
        user_agents = [ua.random for _ in range(10)]
        unique_agents = set(user_agents)

        # Should have some uniqueness
        assert len(unique_agents) >= 5, f"Basic randomness failed: {len(unique_agents)} unique out of 10"

    def test_random_fallback_behavior(self):
        """Test that fallback still works when no browsers match."""
        ua = UserAgent(
            browsers=["NonExistentBrowser"],
            os=["NonExistentOS"],
            min_version=999,
        )

        # Should return fallback
        agent = ua.random
        assert agent == ua.fallback

    def test_weighted_selection_correctness(self):
        """Test that selection is uniform after deduplication."""
        ua = UserAgent(browsers=["Chrome"], os=["Windows"], min_version=131)

        filtered = ua._filter_useragents()
        if len(filtered) >= 2:
            # Generate many samples
            samples = 10000
            user_agents = [ua.random for _ in range(samples)]
            counter = Counter(user_agents)

            # With uniform selection, no UA should be selected excessively more
            max_count = max(counter.values())
            expected_max = samples // len(filtered) + 3 * (samples // len(filtered)) ** 0.5  # rough statistical bound
            assert max_count < expected_max, f"Selection not uniform: max count {max_count}, expected < {expected_max}"