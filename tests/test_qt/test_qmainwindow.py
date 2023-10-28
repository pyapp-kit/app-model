from typing import TYPE_CHECKING

from qtpy.QtCore import Qt

from app_model.backends.qt import QModelMainWindow

if TYPE_CHECKING:
    from ..conftest import FullApp  # noqa: TID252


def test_qmodel_main_window(qtbot, full_app: "FullApp"):
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

    win.addModelToolBar(full_app.Menus.FILE)
    win.addModelToolBar(full_app.Menus.EDIT, area=Qt.ToolBarArea.RightToolBarArea)
