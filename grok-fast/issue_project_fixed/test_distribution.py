import sys
sys.path.insert(0, 'src')
from fake_useragent import UserAgent
from collections import Counter

ua = UserAgent(
    browsers=['Chrome', 'Firefox', 'Edge'], 
    os=['Windows', 'Mac OS X'], 
    min_version=131
)

samples = [ua.random for _ in range(100)]
counter = Counter(samples)

print(f'100 samples generated')
print(f'Unique UAs: {len(counter)}')
print(f'Top 5 most common:')
for ua_str, count in counter.most_common(5):
    print(f'  {count}x: {ua_str[:60]}...')
