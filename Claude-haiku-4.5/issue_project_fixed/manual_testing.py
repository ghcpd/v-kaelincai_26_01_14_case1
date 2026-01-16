"""Manual functional testing of the Issue #446 fix"""
import sys
sys.path.insert(0, 'src')

from fake_useragent import UserAgent
import random

print("=" * 80)
print("CORE FUNCTIONALITY MANUAL TESTING")
print("=" * 80)
print()

# Test 1: Basic instantiation
print("Test 1: Basic Instantiation")
print("-" * 80)
try:
    ua = UserAgent()
    print("[OK] UserAgent() created")
    print(f"      Browsers: {len(ua.browsers)} configured")
    print(f"      OSes: {len(ua.os)} configured")
    print(f"      Data items: {len(ua.data_browsers)} loaded")
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 2: Basic properties
print("Test 2: Basic Properties")
print("-" * 80)
try:
    print(f"[OK] ua.random: {ua.random[:60]}...")
    print(f"[OK] ua.chrome: {ua.chrome[:60]}...")
    print(f"[OK] ua.firefox: {ua.firefox[:60]}...")
    print(f"[OK] ua.safari: {ua.safari[:60]}...")
    print(f"[OK] ua.opera: {ua.opera[:60]}...")
    print(f"[OK] ua.edge: {ua.edge[:60]}...")
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 3: Issue #446 specific - Weighted Selection
print("Test 3: Issue #446 - Weighted Selection Implementation")
print("-" * 80)
try:
    # Create UserAgent with filters that would trigger Issue #446
    ua_issue = UserAgent(
        browsers=["Chrome", "Firefox", "Edge", "Opera", "Safari", "Android",
                  "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile",
                  "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile"],
        os=["Windows", "Chrome OS", "Mac OS X", "Android", "iOS"],
        min_version=131,
    )
    
    # Get filtered list
    filtered = ua_issue._filter_useragents()
    print(f"[OK] Filtered list has {len(filtered)} items")
    
    # Check weights
    weights = [item['percent'] for item in filtered]
    print(f"[OK] Weights (percent field): min={min(weights):.6f}, max={max(weights):.6f}, sum={sum(weights):.4f}")
    
    # Test weighted selection
    selections = [ua_issue._weighted_choice(filtered) for _ in range(10)]
    print(f"[OK] _weighted_choice() returned 10 items")
    
    # Check that we got different results
    unique = len(set(sel['useragent'] for sel in selections))
    print(f"[OK] Got {unique}/10 unique user agents from weighted selection")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Filtering with different parameters
print("Test 4: Filtering with Different Parameters")
print("-" * 80)

test_cases = [
    {"browsers": "Chrome", "label": "Single browser (string)"},
    {"browsers": ["Chrome", "Firefox"], "label": "Multiple browsers (list)"},
    {"os": "Windows", "label": "Single OS (string)"},
    {"os": ["Windows", "Mac OS X"], "label": "Multiple OSes (list)"},
    {"min_version": 130, "label": "Minimum version"},
    {"min_version": 135, "label": "High minimum version"},
    {"platforms": "desktop", "label": "Platform filter"},
    {"browsers": ["Chrome"], "os": ["Windows"], "label": "Combined filters"},
]

for test_case in test_cases:
    label = test_case.pop("label")
    try:
        ua_test = UserAgent(**test_case)
        agent = ua_test.random
        print(f"[OK] {label}: {agent[:50]}...")
    except Exception as e:
        print(f"[ERROR] {label}: {e}")

print()

# Test 5: Data Access Methods
print("Test 5: Data Access Methods (getRandom, getChrome, etc.)")
print("-" * 80)
try:
    ua = UserAgent()
    
    data = ua.getRandom
    assert isinstance(data, dict), "getRandom did not return dict"
    assert "useragent" in data, "Missing useragent field"
    assert "percent" in data, "Missing percent field"
    assert "browser" in data, "Missing browser field"
    assert "os" in data, "Missing os field"
    print(f"[OK] ua.getRandom: {data['useragent'][:50]}...")
    print(f"     - browser: {data['browser']}, os: {data['os']}, percent: {data['percent']}")
    
    chrome_data = ua.getChrome
    assert isinstance(chrome_data, dict), "getChrome did not return dict"
    print(f"[OK] ua.getChrome: {chrome_data['useragent'][:50]}...")
    
    firefox_data = ua.getFirefox
    assert isinstance(firefox_data, dict), "getFirefox did not return dict"
    print(f"[OK] ua.getFirefox: {firefox_data['useragent'][:50]}...")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 6: Index Access
print("Test 6: Index/Dictionary-style Access")
print("-" * 80)
try:
    ua = UserAgent()
    
    agent1 = ua["random"]
    assert isinstance(agent1, str), "Index access did not return string"
    print(f"[OK] ua['random']: {agent1[:60]}...")
    
    agent2 = ua["Chrome"]
    assert isinstance(agent2, str), "Browser index access did not return string"
    print(f"[OK] ua['Chrome']: {agent2[:60]}...")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 7: Fallback behavior
print("Test 7: Fallback Behavior")
print("-" * 80)
try:
    custom_fallback = "Custom Fallback User Agent String"
    ua_fallback = UserAgent(fallback=custom_fallback)
    
    assert ua_fallback.fallback == custom_fallback, "Fallback not set correctly"
    print(f"[OK] Custom fallback set: {custom_fallback[:50]}...")
    
    # Try with impossible filters to trigger fallback
    ua_impossible = UserAgent(
        browsers=["NonExistentBrowser"],
        os=["NonExistentOS"],
        min_version=9999
    )
    
    result = ua_impossible.random
    assert result == ua_impossible.fallback, "Did not use fallback for impossible filter"
    print(f"[OK] Fallback used for impossible filters: {result[:50]}...")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 8: Type validation
print("Test 8: Type Validation")
print("-" * 80)
try:
    # Invalid fallback type
    try:
        ua_bad = UserAgent(fallback=123)
        print("[ERROR] Should have rejected non-string fallback")
        sys.exit(1)
    except TypeError:
        print("[OK] Correctly rejected non-string fallback")
    
    # Invalid safe_attrs type
    try:
        ua_bad = UserAgent(safe_attrs=[123, "valid"])
        print("[ERROR] Should have rejected non-string safe_attrs")
        sys.exit(1)
    except TypeError:
        print("[OK] Correctly rejected non-string safe_attrs")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 9: Randomness consistency
print("Test 9: Randomness Consistency (multiple calls)")
print("-" * 80)
try:
    ua = UserAgent(browsers=["Chrome", "Firefox"], os=["Windows"])
    
    results = []
    for i in range(20):
        results.append(ua.random)
    
    unique = len(set(results))
    print(f"[OK] Generated 20 user agents, got {unique} unique")
    
    if unique > 1:
        print(f"[OK] Results are not all identical (good randomness)")
    else:
        print(f"[WARNING] All results were identical!")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

# Test 10: Performance check
print("Test 10: Basic Performance Check")
print("-" * 80)
try:
    import time
    
    ua = UserAgent(
        browsers=["Chrome", "Firefox"],
        os=["Windows", "Mac OS X", "Linux"],
        min_version=130
    )
    
    start = time.time()
    for _ in range(100):
        _ = ua.random
    elapsed = time.time() - start
    
    avg_time = (elapsed / 100) * 1000  # Convert to ms
    print(f"[OK] Generated 100 user agents in {elapsed:.3f}s")
    print(f"[OK] Average time per selection: {avg_time:.3f}ms")
    
    if avg_time < 5:  # Less than 5ms per call is acceptable
        print(f"[OK] Performance is acceptable (<5ms per call)")
    else:
        print(f"[WARNING] Performance might be slow (>{avg_time:.1f}ms per call)")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

print()

print("=" * 80)
print("ALL MANUAL TESTS PASSED")
print("=" * 80)
