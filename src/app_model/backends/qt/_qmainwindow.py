from typing import List, Optional, Union

from qtpy.QtWidgets import QMainWindow, QWidget

from app_model import Application

from ._qmenubar import QModelMenuBar


class QModelMainWindow(QMainWindow):
    """QMainWindow with app-model support."""

    def __init__(
        self, app: Union[str, Application], parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self._app = Application.get_or_create(app) if isinstance(app, str) else app

    def setModelMenuBar(self, menu_ids: List[str]) -> None:
        """Set the menu bar to a list of menu ids."""
        menu_bar = QModelMenuBar(menu_ids, self._app, self)
        self.setMenuBar(menu_bar)
