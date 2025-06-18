from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QAction, QApplication

from app_model.backends.qt import QModelMainWindow, QModelToolBar
from app_model.types._action import Action

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot

    from ..conftest import FullApp  # noqa: TID252


def test_qmodel_main_window(
    qtbot: QtBot, qapp: QApplication, full_app: FullApp
) -> None:
    win = QModelMainWindow(full_app)
    qtbot.addWidget(win)

    win.setModelMenuBar(
        {
            full_app.Menus.FILE: "File",
            full_app.Menus.EDIT: "Edit",
            full_app.Menus.HELP: "Help",
        }
    )
    assert [a.text() for a in win.menuBar().actions()] == ["File", "Edit", "Help"]

    tb = win.addModelToolBar(
        full_app.Menus.FILE,
        toolbutton_style=Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
    )
    assert isinstance(tb, QModelToolBar)
    win.addModelToolBar(full_app.Menus.EDIT, area=Qt.ToolBarArea.RightToolBarArea)

    full_app.register_action(
        Action(
            id="late-action",
            title="Late Action",
            keybindings=[{"primary": "Shift+L"}],
            menus=[{"id": full_app.Menus.FILE}],
            callback=lambda: None,
        )
    )

    action = qapp.findChild(QAction, "late-action")
    assert action.shortcut().toString() == "Shift+L"
