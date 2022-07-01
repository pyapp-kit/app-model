import pytest

try:
    pass
except ImportError:
    pytest.skip("No Qt backend", allow_module_level=True)
