"""Quick test to verify Issue #446 fix - check for duplicates in random samples."""
import sys
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from fake_useragent import UserAgent

ua = UserAgent(
    browsers=["Chrome"],
    os=["Windows"],
    min_version=131,
)

results = [ua.random for _ in range(20)]
unique = set(results)

print("Issue #446 Duplicate Check:")
print(f"Total samples: {len(results)}")
print(f"Unique values: {len(unique)}")
print(f"Duplicates found: {len(results) - len(unique)}")
print(f"Duplicate rate: {((len(results) - len(unique)) / len(results) * 100):.1f}%")
print("\nSample values:")
for i, val in enumerate(list(unique)[:5]):
    print(f"  {i+1}. {val}")
