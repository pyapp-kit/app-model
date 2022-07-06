from typing import List, Optional, Union

from qtpy.QtWidgets import QMenuBar, QWidget

from ..._app import Application
from ._qmenu import QModelMenu


class QModelMenuBar(QMenuBar):
    def __init__(
        self,
        menus: List[str],
        app: Union[str, Application],
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        for menu_id in menus:
            self.addMenu(QModelMenu(menu_id, app, "File", self))
