from __future__ import annotations

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
