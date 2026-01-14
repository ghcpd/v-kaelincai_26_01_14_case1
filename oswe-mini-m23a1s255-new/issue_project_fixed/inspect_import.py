import fake_useragent
import pkgutil
from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError

print('fake_useragent module file:', getattr(fake_useragent, '__file__', None))
print('package loader:', pkgutil.get_loader('fake_useragent'))

try:
    ua = UserAgent(browsers=['__definitely_not_present__'])
    print('UserAgent created with candidates count =', len(ua._candidates))
except FakeUserAgentError as e:
    print('Raised FakeUserAgentError:', e)
