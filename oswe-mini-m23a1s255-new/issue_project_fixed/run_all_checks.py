import sys
import pytest

if __name__ == '__main__':
    # Run tests programmatically so we can capture exit code reliably
    print('Running pytest...')
    ret = pytest.main(['-q'])
    print('\npytest exit code:', ret)
    sys.exit(ret)
