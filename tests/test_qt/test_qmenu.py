import sys
from typing import TYPE_CHECKING

import pytest
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QAction, QMainWindow

from app_model.backends.qt import QMenuItemAction, QModelMenu
from app_model.types import MenuItem

if TYPE_CHECKING:
    from pytestqt.plugin import QtBot

    from conftest import FullApp

SEP = ""
LINUX = sys.platform.startswith("linux")


def test_menu(qtbot: "QtBot", full_app: "FullApp") -> None:
    app = full_app

    menu = QModelMenu(app.Menus.EDIT, app)
    qtbot.addWidget(menu)

    # The "" are separators, according to our group settings in full_app
    menu_texts = [a.text() for a in menu.actions()]
    assert menu_texts == ["AtTop", SEP, "Undo", "Redo", SEP, "Copy", "Paste"]

    # check that triggering the actions calls the associated commands
    for cmd in (app.Commands.UNDO, app.Commands.REDO):
        action: QAction = menu.findAction(cmd)
        with qtbot.waitSignal(action.triggered):
            action.trigger()
            getattr(app.mocks, cmd).assert_called_once()

    redo_action: QAction = menu.findAction(app.Commands.REDO)

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

    submenu = menu.findChild(QModelMenu, app.Menus.FILE_OPEN_FROM)
    assert isinstance(submenu, QModelMenu)
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
    # assert not submenu.isVisible()
    assert not submenu.isEnabled()

    menu.update_from_context({"something_open": True, "friday": True})
    # assert not submenu.isVisible()
    assert submenu.isEnabled()


@pytest.mark.filterwarnings("ignore:QPixmapCache.find:")
@pytest.mark.skipif(LINUX, reason="Linux keytest not working")
def test_shortcuts(qtbot: "QtBot", full_app: "FullApp") -> None:
    app = full_app

    win = QMainWindow()
    menu = QModelMenu(app.Menus.EDIT, app=app, title="Edit", parent=win)
    win.menuBar().addMenu(menu)
    qtbot.addWidget(win)
    qtbot.addWidget(menu)

    with qtbot.waitExposed(win):
        win.show()

    copy_action = menu.findAction(app.Commands.COPY)

    with qtbot.waitSignal(copy_action.triggered, timeout=1000):
        qtbot.keyClicks(win, "C", Qt.KeyboardModifier.ControlModifier)

    paste_action = menu.findAction(app.Commands.PASTE)
    with qtbot.waitSignal(paste_action.triggered, timeout=1000):
        qtbot.keyClicks(win, "V", Qt.KeyboardModifier.ControlModifier)


def test_cache_action(full_app: "FullApp") -> None:
    action = next(
        i for k, items in full_app.menus for i in items if isinstance(i, MenuItem)
    )
    a1 = QMenuItemAction(action, full_app)
    a2 = QMenuItemAction(action, full_app)
    assert a1 is a2


def test_toggled_menu_item(qtbot: "QtBot", full_app: "FullApp") -> None:
    app = full_app
    menu = QModelMenu(app.Menus.HELP, app)
    qtbot.addWidget(menu)

    menu.update_from_context({"thing_toggled": True})
    action = menu.findAction(app.Commands.TOGGLE_THING)
    assert action.isChecked()

    menu.update_from_context({"thing_toggled": False})
    assert not action.isChecked()
