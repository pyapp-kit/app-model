import pytest

from app_model import Application


def test_app_create():
    app = Application("my_app")

    # NOTE: for some strange reason, this test fails if I move this line
    # below the error assertion below... I don't know why.
    assert Application.get_or_create("my_app") is app

    with pytest.raises(ValueError, match="Application 'my_app' already exists"):
        Application("my_app")

    assert repr(app) == "Application('my_app')"
