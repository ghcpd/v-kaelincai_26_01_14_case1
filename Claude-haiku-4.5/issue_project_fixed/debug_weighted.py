import sys
sys.path.insert(0, 'src')
from fake_useragent import UserAgent
import random

# Set seed for reproducibility
random.seed(42)

ua = UserAgent(os=['Windows'])
filtered = ua._filter_useragents()
print(f'Filtered list size: {len(filtered)}')

# Show the actual percent values
percents = [item['percent'] for item in filtered]
print(f'Min percent: {min(percents)}, Max percent: {max(percents)}, Sum: {sum(percents)}')

# Test weighted_choice
selections = []
for i in range(10):
    sel = ua._weighted_choice(filtered)
    selections.append(sel['useragent'])
    print(f'{i}: {sel["useragent"][:70]}...')

unique = len(set(selections))
print(f'\nUnique out of 10: {unique}')
