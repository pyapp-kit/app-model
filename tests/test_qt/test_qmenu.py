from typing import TYPE_CHECKING

import pytest
from qtpy.QtWidgets import QAction

from app_model.qt import QModelMenu

if TYPE_CHECKING:
    from pytestqt.plugin import QtBot

    from conftest import FullApp

SEP = ""


def test_menu(qtbot: "QtBot", full_app: "FullApp") -> None:
    app = full_app

    menu = QModelMenu(app.Menus.EDIT, app)
    qtbot.addWidget(menu)

    # The "" are separators, according to our group settings in full_app
    menu_texts = [a.text() for a in menu.actions()]
    assert menu_texts == ["AtTop", SEP, "Undo", "Redo", SEP, "Copy", "Paste"]

    # check that triggering the actions calls the associated commands
    for cmd in (app.Commands.UNDO, app.Commands.REDO):
        action: QAction = menu.findChild(QAction, cmd)
        with qtbot.waitSignal(action.triggered):
            action.trigger()
            getattr(app.mocks, cmd).assert_called_once()

    redo_action: QAction = menu.findChild(QAction, app.Commands.REDO)
    assert redo_action.isVisible()
    assert redo_action.isEnabled()

    # change that visibility and enablement follows the context
    menu.update_from_context({"allow_undo_redo": True, "something_to_undo": False})
    assert redo_action.isVisible()
    assert redo_action.isEnabled()

    menu.update_from_context({"allow_undo_redo": False, "something_to_undo": False})
    assert redo_action.isVisible()
    assert not redo_action.isEnabled()

    menu.update_from_context({"allow_undo_redo": False, "something_to_undo": True})
    assert not redo_action.isVisible()
    assert not redo_action.isEnabled()

    menu.update_from_context({"allow_undo_redo": True, "something_to_undo": False})
    assert redo_action.isVisible()
    assert redo_action.isEnabled()

    # usefull error when we forget a required name
    with pytest.raises(NameError, match="Names required to eval this expression"):
        menu.update_from_context({})


def test_submenu(qtbot: "QtBot", full_app: "FullApp") -> None:
    app = full_app

    menu = QModelMenu(app.Menus.FILE, app)
    qtbot.addWidget(menu)

    menu_texts = [a.text() for a in menu.actions()]
    assert menu_texts == ["Open From...", "Open..."]

    submenu: QModelMenu = menu.findChild(QModelMenu, app.Menus.FILE_OPEN_FROM)
    submenu.setVisible(True)
    assert submenu.isVisible()
    assert submenu.isEnabled()

    # "not something_open" is the when clause
    # "friday" is the enablement clause

    menu.update_from_context({"something_open": False, "friday": True})
    assert submenu.isVisible()
    assert submenu.isEnabled()

    menu.update_from_context({"something_open": False, "friday": False})
    assert submenu.isVisible()
    assert not submenu.isEnabled()

    menu.update_from_context({"something_open": True, "friday": False})
    assert not submenu.isVisible()
    assert not submenu.isEnabled()

    menu.update_from_context({"something_open": True, "friday": True})
    assert not submenu.isVisible()
    assert submenu.isEnabled()
