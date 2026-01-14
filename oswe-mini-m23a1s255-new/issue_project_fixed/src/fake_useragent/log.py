import logging

logger = logging.getLogger("fake_useragent")
logger.addHandler(logging.NullHandler())
