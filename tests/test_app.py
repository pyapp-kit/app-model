from typing import TYPE_CHECKING

import pytest

from app_model import Application

if TYPE_CHECKING:
    from conftest import FullApp


def test_app_create():
    app = Application("my_app")

    # NOTE: for some strange reason, this test fails if I move this line
    # below the error assertion below... I don't know why.
    assert Application.get_or_create("my_app") is app

    with pytest.raises(ValueError, match="Application 'my_app' already exists"):
        Application("my_app")

    assert repr(app) == "Application('my_app')"


def test_app(full_app: "FullApp"):
    app = full_app

    app.commands.execute_command(app.Commands.OPEN)
    app.mocks.open.assert_called_once()
    app.commands.execute_command(app.Commands.COPY)
    app.mocks.copy.assert_called_once()
    app.commands.execute_command(app.Commands.PASTE)
    app.mocks.paste.assert_called_once()
