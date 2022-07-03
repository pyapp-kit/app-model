from __future__ import annotations

import sys
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


def test_app(full_app: FullApp):
    app = full_app

    app.commands.execute_command(app.Commands.OPEN)
    app.mocks.open.assert_called_once()
    app.commands.execute_command(app.Commands.COPY)
    app.mocks.copy.assert_called_once()
    app.commands.execute_command(app.Commands.PASTE)
    app.mocks.paste.assert_called_once()


def test_sorting(full_app: FullApp):
    groups = list(full_app.menus.iter_menu_groups(full_app.Menus.EDIT))
    assert len(groups) == 3
    [g0, g1, g2] = groups
    assert all(i.group == "1_undo_redo" for i in g1)
    assert all(i.group == "2_copy_paste" for i in g2)

    assert [i.command.title for i in g1] == ["Undo", "Redo"]
    assert [i.command.title for i in g2] == ["Copy", "Paste"]


def test_action_import_by_string(full_app: FullApp):
    """the REDO command is declared as a string in the conftest.py file

    This tests that it can be lazily imported at callback runtime and executed
    """
    assert "fake_module" not in sys.modules
    assert full_app.commands.execute_command(full_app.Commands.REDO).result()
    assert "fake_module" in sys.modules
    full_app.mocks.redo.assert_called_once()

    # tests what happens when the module cannot be found
    with pytest.raises(
        ModuleNotFoundError, match="Command 'unimportable' was not importable"
    ):
        full_app.commands.execute_command(full_app.Commands.UNIMPORTABLE)
    # the second time we try within a session, nothing should happen
    full_app.commands.execute_command(full_app.Commands.UNIMPORTABLE)

    # tests what happens when the object is not callable cannot be found
    with pytest.raises(
        TypeError,
        match="Command 'not.callable' did not resolve to a callble object",
    ):
        full_app.commands.execute_command(full_app.Commands.NOT_CALLABLE)
    # the second time we try within a session, nothing should happen
    full_app.commands.execute_command(full_app.Commands.NOT_CALLABLE)


def test_action_raises_exception(full_app: FullApp):
    result = full_app.commands.execute_command(full_app.Commands.RAISES)
    with pytest.raises(ValueError):
        result.result()

    # the function that raised the exception is `_raise_an_error` in conftest.py
    assert str(result.exception()) == "This is an error"
