from __future__ import annotations

from typing import Collection, Mapping, Sequence

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QWidget

from app_model import Application

from ._qmenu import QModelMenuBar, QModelToolBar


class QModelMainWindow(QMainWindow):
    """QMainWindow with app-model support."""

    def __init__(self, app: Application | str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = Application.get_or_create(app) if isinstance(app, str) else app

    def setModelMenuBar(
        self, menu_ids: Mapping[str, str] | Sequence[str | tuple[str, str]]
    ) -> QModelMenuBar:
        """Set the menu bar to a list of menu ids.

        Parameters
        ----------
        menu_ids : Mapping[str, str] | Sequence[str | tuple[str, str]]
            A mapping of menu ids to menu titles or a sequence of menu ids.
        """
        menu_bar = QModelMenuBar(menu_ids, self._app, self)
        self.setMenuBar(menu_bar)
        return menu_bar

    def addModelToolBar(
        self,
        menu_id: str,
        *,
        exclude: Collection[str] | None = None,
        area: Qt.ToolBarArea | None = None,
        toolbutton_style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonIconOnly,
    ) -> QModelToolBar:
        """Add a tool bar to the main window."""
        toolbar = QModelToolBar(menu_id, self._app, exclude=exclude, parent=self)
        toolbar.setToolButtonStyle(toolbutton_style)
        if area is not None:
            self.addToolBar(area, toolbar)
        else:
            self.addToolBar(toolbar)
        return toolbar
