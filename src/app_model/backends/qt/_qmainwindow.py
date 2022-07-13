from typing import Collection, List, Optional, Union

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QWidget

from app_model import Application

from ._qmenu import QModelMenuBar, QModelToolBar


class QModelMainWindow(QMainWindow):
    """QMainWindow with app-model support."""

    def __init__(
        self, app: Union[str, Application], parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self._app = Application.get_or_create(app) if isinstance(app, str) else app

    def setModelMenuBar(self, menu_ids: List[str]) -> QModelMenuBar:
        """Set the menu bar to a list of menu ids."""
        menu_bar = QModelMenuBar(menu_ids, self._app, self)
        self.setMenuBar(menu_bar)
        return menu_bar

    def addModelToolBar(
        self,
        menu_id: str,
        *,
        exclude: Optional[Collection[str]] = None,
        area: Optional[Qt.ToolBarArea] = None
    ) -> None:
        """Add a tool bar to the main window."""
        menu_bar = QModelToolBar(menu_id, self._app, exclude=exclude, parent=self)
        if area is not None:
            self.addToolBar(area, menu_bar)
        else:
            self.addToolBar(menu_bar)
