from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError

try:
    ua = UserAgent(browsers=['__definitely_not_present__'])
    print('UserAgent created with candidates count =', len(ua._candidates))
except FakeUserAgentError as e:
    print('Raised FakeUserAgentError:', e)
