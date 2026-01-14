import os
import sys

# Ensure `src` is on the import path for tests and unload any already-imported
# `fake_useragent` modules so the local package is used during tests.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
# Put our local src at the front of sys.path
if SRC in sys.path:
    sys.path.remove(SRC)
sys.path.insert(0, SRC)

# Remove any pre-imported fake_useragent modules from sys.modules so imports
# inside tests load the local package from `SRC`.
for mod_name in list(sys.modules.keys()):
    if mod_name == "fake_useragent" or mod_name.startswith("fake_useragent."):
        del sys.modules[mod_name]
