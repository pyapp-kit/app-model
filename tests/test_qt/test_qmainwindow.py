from typing import TYPE_CHECKING

from qtpy.QtCore import Qt

from app_model.backends.qt import QModelMainWindow

if TYPE_CHECKING:
    from ..conftest import FullApp


def test_qmodel_main_window(qtbot, full_app: "FullApp"):
    win = QModelMainWindow(full_app)
    qtbot.addWidget(win)

    win.addModelToolBar(full_app.Menus.FILE)
    win.addModelToolBar(full_app.Menus.EDIT, area=Qt.ToolBarArea.RightToolBarArea)
