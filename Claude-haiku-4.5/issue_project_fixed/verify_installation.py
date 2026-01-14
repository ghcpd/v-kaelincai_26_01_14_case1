"""Verification script for Installation and Imports"""
import sys

print("=" * 80)
print("INSTALLATION AND IMPORT VERIFICATION")
print("=" * 80)
print()

# Check Python version
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print()

# Test imports
print("Testing Imports:")
print("-" * 80)

try:
    from fake_useragent import UserAgent
    print("[OK] from fake_useragent import UserAgent")
except Exception as e:
    print(f"[ERROR] Failed to import UserAgent: {e}")
    sys.exit(1)

try:
    from fake_useragent import FakeUserAgent
    print("[OK] from fake_useragent import FakeUserAgent")
except Exception as e:
    print(f"[ERROR] Failed to import FakeUserAgent: {e}")
    sys.exit(1)

try:
    from fake_useragent import FakeUserAgentError
    print("[OK] from fake_useragent import FakeUserAgentError")
except Exception as e:
    print(f"[ERROR] Failed to import FakeUserAgentError: {e}")
    sys.exit(1)

try:
    from fake_useragent import __version__
    print(f"[OK] from fake_useragent import __version__ ({__version__})")
except Exception as e:
    print(f"[ERROR] Failed to import __version__: {e}")

print()
print("Testing Package Structure:")
print("-" * 80)

# Test that the package can be instantiated
try:
    ua = UserAgent()
    print("[OK] UserAgent() instantiated successfully")
except Exception as e:
    print(f"[ERROR] Failed to instantiate UserAgent: {e}")
    sys.exit(1)

# Test that methods exist
try:
    assert hasattr(ua, 'random'), "Missing 'random' property"
    assert hasattr(ua, 'chrome'), "Missing 'chrome' property"
    assert hasattr(ua, 'firefox'), "Missing 'firefox' property"
    assert hasattr(ua, 'getRandom'), "Missing 'getRandom' property"
    assert hasattr(ua, 'getBrowser'), "Missing 'getBrowser' method"
    assert hasattr(ua, '_weighted_choice'), "Missing '_weighted_choice' method (fix not applied!)"
    print("[OK] All expected properties and methods are present")
except AssertionError as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

# Test that the fix is actually implemented
try:
    assert callable(ua._weighted_choice), "_weighted_choice is not callable"
    print("[OK] _weighted_choice method is callable (Issue #446 fix implemented)")
except AssertionError as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()
print("Testing Basic Functionality:")
print("-" * 80)

# Test that we can get a user agent
try:
    agent = ua.random
    assert isinstance(agent, str), "random property did not return a string"
    assert len(agent) > 0, "random property returned empty string"
    print(f"[OK] ua.random returned string: {agent[:60]}...")
except Exception as e:
    print(f"[ERROR] Failed to get random user agent: {e}")
    sys.exit(1)

# Test with filters
try:
    ua_filtered = UserAgent(browsers=["Chrome"], os=["Windows"])
    agent_filtered = ua_filtered.random
    assert isinstance(agent_filtered, str), "Filtered random property did not return a string"
    assert len(agent_filtered) > 0, "Filtered random property returned empty string"
    print(f"[OK] Filtered ua.random returned string: {agent_filtered[:60]}...")
except Exception as e:
    print(f"[ERROR] Failed to get filtered user agent: {e}")
    sys.exit(1)

print()
print("=" * 80)
print("VERIFICATION COMPLETE: ALL CHECKS PASSED")
print("=" * 80)
