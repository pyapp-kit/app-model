from typing import TYPE_CHECKING

from qtpy.QtWidgets import QAction

from app_model.qt import QModelMenu

if TYPE_CHECKING:
    from pytestqt.plugin import QtBot

    from conftest import FullApp


def test_menu(qtbot: "QtBot", full_app: "FullApp"):
    app = full_app

    menu = QModelMenu(app.Menus.EDIT, app)
    qtbot.addWidget(menu)

    # The "" are separators, according to our group settings in full_app
    menu_texts = [a.text() for a in menu.actions()]
    assert menu_texts == ["AtTop", "", "Undo", "Redo", "", "Copy", "Paste", ""]

    # check that triggering the actions calls the associated commands
    for cmd in (app.Commands.UNDO, app.Commands.REDO):
        action: QAction = menu.findChild(QAction, cmd)
        with qtbot.waitSignal(action.triggered):
            action.trigger()
            getattr(app.mocks, cmd).assert_called_once()

    menu.show()
