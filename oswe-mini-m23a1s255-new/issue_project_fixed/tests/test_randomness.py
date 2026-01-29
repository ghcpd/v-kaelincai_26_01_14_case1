import random
from unittest import mock

from fake_useragent import UserAgent


def test_random_calls_choice_each_time():
    ua = UserAgent(browsers=["Chrome", "Firefox"])

    with mock.patch("random.choice", wraps=random.choice) as patched:
        samples = [ua.random for _ in range(10)]
        assert patched.call_count == 10
        # ensure we returned strings
        assert all(isinstance(s, str) for s in samples)


def test_random_not_all_identical_with_fixed_seed():
    # deterministic but still ensures diversity (very unlikely to be all equal)
    random.seed(0)
    ua = UserAgent(browsers=["Chrome", "Firefox", "Chrome Mobile"])
    samples = [ua.random for _ in range(20)]
    assert len(set(samples)) > 1
