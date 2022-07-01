import pytest

try:
    import qtpy  # noqa
except ImportError:
    pytest.skip("No Qt backend", allow_module_level=True)
